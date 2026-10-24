"""Shared helpers for the Havířov / Karviná / Orlová bus pipeline (stdlib only).

Everything rule-bearing is imported, not copied, so the sheet follows the Ostrava bus rules as they change
(coordination with the Ostrava bus session, simutrans-timetable-0b, 20 Oct 2026):
- ../../ostrava/scripts/lib.py (tram lib): parsers, WAF headers, JDF reader and version rule, blocks, runfit, plans,
  loop_shift, pattern_need, make_nm;
- ../../ostrava-bus/scripts/lib.py: branch_pairs, line_anchor, interleave, path_variants, circuitize. That module loads
  the Ostrava bus config and paths at import; only its pure functions are used here, never its save()/load();
- ../../brno-trolleybus/scripts/common.py: mark_spares (logged-surplus rule).
Only the paths and the config are this folder's own.
"""
import importlib.util, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))          # pipeline/havirov-karvina-orlova
PIPE = os.path.dirname(ROOT)
PROJECT = os.path.dirname(PIPE)
def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
tramlib = _load('tramlib', os.path.join(PIPE, 'ostrava', 'scripts', 'lib.py'))
buslib = _load('ostravabuslib', os.path.join(PIPE, 'ostrava-bus', 'scripts', 'lib.py'))

HEADERS = tramlib.HEADERS
http, parse_vypravenost, next_page, record_date = tramlib.http, tramlib.parse_vypravenost, tramlib.next_page, tramlib.record_date
jdf_open, jdf_tables, pick_version, jdf_trips = tramlib.jdf_open, tramlib.jdf_tables, tramlib.pick_version, tramlib.jdf_trips
blocks, active_at, min_turnaround = tramlib.blocks, tramlib.active_at, tramlib.min_turnaround
runfit, loop_shift, plans, make_nm, hm, hhmm, day = tramlib.runfit, tramlib.loop_shift, tramlib.plans, tramlib.make_nm, tramlib.hm, tramlib.hhmm, tramlib.day
pattern_need = tramlib.pattern_need
branch_pairs, line_anchor, interleave, path_variants, circuitize = buslib.branch_pairs, buslib.line_anchor, buslib.interleave, buslib.path_variants, buslib.circuitize
simplify_rows, thin_rows = buslib.simplify_rows, buslib.thin_rows   # owner rule via 0b, 20 Oct 2026: evenly spaced slots at the plain interval
mark_spares = _load('brnotrolleylib', os.path.join(PIPE, 'brno-trolleybus', 'scripts', 'common.py')).mark_spares

CONFIG = json.load(open(os.path.join(ROOT, 'config.json'), encoding='utf-8'))
RAW = os.path.join(ROOT, 'data', 'raw', CONFIG['snapshot'])
DERIVED = os.path.join(ROOT, 'data', 'derived')
os.makedirs(DERIVED, exist_ok=True)

def dpath(name): return os.path.join(DERIVED, name)
def save(name, obj): json.dump(obj, open(dpath(name), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
def load(name): return json.load(open(dpath(name), encoding='utf-8'))

def town_of(L):
    """the town section of a line number (config.towns: line ranges)"""
    L = int(L)
    return next(t for t in CONFIG['towns'] if any(a <= L <= b for a, b in t['lines']))

_NM = {}
def nm_for(L):
    """stop-name function of a line: the line's own town prefix is dropped (Havířov, Podlesí, … → Podlesí, …); other
    towns keep theirs; every abbreviation is expanded (config.stop_name_expansions)"""
    t = town_of(L)['name']
    if t not in _NM:
        f = make_nm(dict(CONFIG, stop_name_strip_prefix=t + ','))
        _NM[t] = lambda s, f=f: re.sub(r'\s+', ' ', f(s.replace(',,', ','))).replace(' ,', ',').strip()   # "Dětmarovice,,žel.st."
    return _NM[t]

def plate_key(s): return re.sub(r'\s', '', s or '').upper()

def parse_fleet_list(s):
    """rows of a /seznam?... fleet list page -> {car_id: dict(state, num, type, year, note, plate)}; the tram lib's parser
    plus the number plate (the live feed's join key)"""
    cars = tramlib.parse_fleet_list(s)
    for cid in cars:
        m = re.search(r'data-car-id="%s">\s*<td class=\'plates\'>(.*?)</td>' % cid, s, flags=re.S)
        cars[cid]['plate'] = plate_key(tramlib._clean(m.group(1))) if m else ''
    return cars

# ---------------------------------------------------------------- hand-set Simutrans lines (config.line_overrides)
def tmin(s): h, m = s.split(':'); return int(h) * 60 + int(m)

def build_overrides(L, trips):
    """config.line_overrides[L] -> list of Simutrans lines for line L, each a cycle of legs (owner, 20 Oct 2026: "501 is
    the only line running to Dětmarovice, how can we not model that?"; the Ostrava 41 hand-set circuit is the precedent).
    A leg is fr -> to with the real departures it carries: given in 'deps' (with 'src' naming the real trips, which may
    belong to other lines of the town), or found as the trips of 'lines' (default: L) between those termini in the window.
    'every' 1440 = a daily timetable with all the departures (Pardubice precedent: <= 8 a day). Otherwise one slot per
    leg and period ('slots' for more), at the residue with the smallest worst deviation from the real departures.
    'untimed' legs have no real trips (the real bus goes on as another line): Departure every 0, running time 'rt' or the
    trips of 'rt_from' = [line, fr, to]. Stops of a leg: the commonest stop list of its trips, or 'stops_from' =
    [[line, 'HH:MM'], ...] (the trips whose stops make the leg, joined)."""
    import statistics
    AL = CONFIG['terminus_alias']; al = lambda x: AL.get(x, x)
    ov = CONFIG.get('line_overrides', {}).get(L)
    if not ov: return None, None
    def match(l, fr, to): nm = nm_for(l); return [t for t in trips.get(l, []) if al(nm(t['fr'])) == fr and al(nm(t['to'])) == to]
    out = []
    for sl in ov['lines']:
        P = sl['every']; W = sl.get('window', [0, 1440]); legs = []
        FW = sl.get('fitwin', W)   # where the slots are fitted: the whole day for a line regular at its core points (owner, Ex4)
        for lg in sl['legs']:
            src = lg.get('lines', [L]); fr, to = lg['fr'], lg['to']
            ts = [t for l in src for t in match(l, fr, to)]
            if lg.get('core'):   # core points (owner, Ex4): every trip of the lines that passes fr and then to, at its time at fr
                deps = []
                for l in src:
                    nm_ = nm_for(l)
                    for t in trips.get(l, []):
                        st_ = [al(nm_(x)) for x in t['stops']]
                        if fr in st_ and to in st_ and st_.index(fr) < st_.index(to):
                            d_ = t['times'][st_.index(fr)]
                            if FW[0] <= d_ < FW[1]: deps.append(d_)
                deps = sorted(set(deps))
                if 'rt' not in lg:
                    rr = []
                    for l in src:
                        nm_ = nm_for(l)
                        for t in trips.get(l, []):
                            st_ = [al(nm_(x)) for x in t['stops']]
                            if fr in st_ and to in st_ and st_.index(fr) < st_.index(to): rr.append(t['times'][st_.index(to)] - t['times'][st_.index(fr)])
                    lg = dict(lg, rt=round(statistics.median(rr))) if rr else lg
            elif 'deps' in lg: deps = sorted(tmin(x) for x in lg['deps'])
            else: deps = sorted(t['dep'] for t in ts if FW[0] <= t['dep'] < FW[1])
            if 'rt' in lg: rt = lg['rt']
            elif lg.get('rt_from'): rt = round(statistics.median([t['arr'] - t['dep'] for t in match(*lg['rt_from'])]))
            else:
                rr = [t['arr'] - t['dep'] for t in ts if W[0] - 60 <= t['dep'] < W[1] + 60] or [t['arr'] - t['dep'] for t in ts]
                rt = round(statistics.median(rr))
            if lg.get('stops_from'):
                st = []
                for l, hhmm_ in lg['stops_from']:
                    t = next(t for t in trips[l] if t['dep'] == tmin(hhmm_)); s_ = [nm_for(l)(x) for x in t['stops']]
                    st += s_ if not st or st[-1] != s_[0] else s_[1:]
            else:
                import collections as _c
                st = list(_c.Counter(tuple(nm_for(L)(x) for x in t['stops']) for t in ts).most_common(1)[0][0]) if ts else [fr, to]
            if lg.get('stops_cut'):   # a leg that ends or starts at a core point inside a longer real trip (501 to Dětmarovice, železniční stanice)
                a_, b_ = lg['stops_cut']
                st = st[st.index(a_) if a_ in st else 0: (st.index(b_) + 1) if b_ in st else len(st)]
            leg = dict(fr=fr, to=to, lines=src, rt=rt, deps=deps, stops=st, src=lg.get('src', ''), untimed=bool(lg.get('untimed')), note=lg.get('note', ''))
            if leg['untimed']: leg.update(every=0, real=[], set=[], dev=0)
            elif P == 1440: leg.update(every=1440, real=sorted(set(deps)), set=loop_shift(1440, sorted(set(deps)), CONFIG['all_termini_are_loops']), dev=0)
            elif 'at' in lg:   # the real minutes given (uneven slots, e.g. 401 leaves Šumbark at :14 and :59)
                R = sorted(x % P for x in lg['at'])
                devs = [min(min((d - x) % P, (x - d) % P) for x in R) for d in deps] or [0]
                leg.update(every=P, real=R, set=loop_shift(P, R, CONFIG['all_termini_are_loops']), dev=max(devs))
            else:
                k = lg.get('slots', 1)
                def cd(a, b): return min((a - b) % P, (b - a) % P)
                # the slot follows the regular run: most real departures within 1 min, then the smallest worst deviation;
                # the odd trips are listed as off the pattern (504 leaves Lazy at :06; its 18:56 is the odd one)
                best = None
                for r in range(P):
                    R = sorted((r + i * P // k) % P for i in range(k))
                    devs = [min(cd(d, x) for x in R) for d in deps] or [0]
                    key = (-sum(1 for x in devs if x == 0), -sum(1 for x in devs if x <= 1), max(devs), sum(devs), r)
                    if best is None or key < best[0]: best = (key, R)
                leg.update(every=P, real=best[1], set=loop_shift(P, best[1], CONFIG['all_termini_are_loops']), dev=best[0][2])
            if lg.get('knot') and not leg['untimed']:
                # buses wait only at a terminal (owner, 20 Oct 2026; trains can be held at a junction): the slots and real
                # departures given at the knot are moved back to the terminal by the running time terminal -> knot, so the bus
                # passes the knot on time, and the knot itself gets no timetable (501B leaves Koukolná :09 to pass the station :18)
                kr = lg.get('knot_rt')
                if kr is None:
                    kk = []
                    for l in src:
                        nm_ = nm_for(l)
                        for t in trips.get(l, []):
                            st_ = [al(nm_(x)) for x in t['stops']]
                            if fr in st_ and lg['knot'] in st_ and st_.index(fr) < st_.index(lg['knot']):
                                kk.append(t['times'][st_.index(lg['knot'])] - t['times'][st_.index(fr)])
                    kr = round(statistics.median(kk)) if kk else 0
                leg['knot'] = dict(stop=lg['knot'], rt=kr, real=list(leg['real']), deps=list(leg['deps']))
                leg['real'] = sorted((x - kr) % P for x in leg['real'])
                leg['set'] = loop_shift(P, leg['real'], CONFIG['all_termini_are_loops'])
                leg['deps'] = sorted(d - kr for d in leg['deps'])
            if not leg['untimed'] and leg['every'] and P != 1440:
                leg['off'] = [d for d in deps if min(min((d - x) % P, (x - d) % P) for x in leg['real']) > 3]   # ±3 min, as for circuit legs
            legs.append(leg)
        for g in legs:   # a trip is off the pattern only if no leg of this line between the same stops has a slot for it (504's two paths)
            if g['untimed'] or not g.get('every') or P == 1440: continue
            slots_ = [x for h in legs if not h['untimed'] and h['fr'] == g['fr'] and h['to'] == g['to'] for x in h['real']]
            g['off'] = [d for d in g['deps'] if min(min((d - x) % P, (x - d) % P) for x in slots_) > 3]
        if P == 1440:   # a daily timetable must send as many buses each way, or buses pile up at one end day by day
            n_ = {len(g['real']) for g in legs if not g['untimed']}
            if len(n_) > 1: print('WARNING daily line', sl['name'], 'unbalanced', [len(g['real']) for g in legs])
        out.append(dict(name=sl['name'], every=P, window=W, fitwin=FW, why=sl.get('why', ''), legs=legs, carries=sl.get('carries', '')))
    return ov.get('mode', 'replace'), out

def override_need(sl, t0):
    """pattern_need round the legs of a hand-set line; untimed legs leave at once"""
    rows = [dict(every=1, real=[0]) if g['untimed'] else dict(every=g['every'], real=g['real']) for g in sl['legs']]
    # the wait before each timed leg: the usual 3 min, or less where the fitted slots chain closer, as the real timetable
    # turns (505 at Lutyně, pošta: 2 min; 402 at Stonava: 2 min); otherwise a bus would wait a whole interval
    lays = []
    for i, g in enumerate(sl['legs']):
        pv = sl['legs'][i - 1]
        if g['untimed']: lays.append(0); continue
        lay = CONFIG['cycle_lay']
        if not pv['untimed'] and pv['real']:
            arr = [(r + pv['rt']) % g['every'] for r in pv['real']]
            gap = min((s - a) % g['every'] for a in arr for s in g['real'])
            lay = min(lay, gap)
        lays.append(lay)
    return pattern_need(rows, [g['rt'] for g in sl['legs']], lays, t0)
