"""config.lines -> derived/schedule.json: the Simutrans lines of every ODIS line, set by hand with the bus schedule method
(../../bus-schedule-method.md v3; every line here is regional, so every line is read over the whole day at its core points).

A Simutrans line (config.lines[L].sim[]) is a cycle of legs on one interval `every` (divides 1440, at most 480). A leg runs
fr -> to; its real trips are every trip of its `lines` (default L) that passes fr (or the knot `knot`) and later `core_to`
(default to), optionally only those passing all of `via` and none of `notvia`: the time is read at that core point,
wherever the trip starts or ends (Step 3). Its slots are `at` (minutes, or 'H:MM' clock times, taken mod every) at fr, or
`knot_at` at the knot, moved back by the running time fr -> knot (Step 6: buses wait only at terminals; the knot gets no
timetable). An `untimed` leg is an empty or unmodelled return: Departure every 0, it leaves on arrival.
Trips of one line read between the same points belong to the leg whose slot is nearest (Ex4: one Simutrans line per
variant, each with its own slots); a trip more than 3 min from every slot is off the pattern.
For each line: its anchor (lib.line_anchor: the busiest 2 h in 13:00-18:00, or 16:00; config `anchor` overrides) and model
window anchor-30..+90. For each leg: typed values (offset = (real - 60 - 1 at loops) mod every), running time (median of its
own trips that run fr -> to around the anchor), stops (its own trips' commonest path in the afternoon), the real trips it
stands for and their deviation from the slots, slots of the model window without a real departure, and the time the
modelled bus passes every core point against the real times there (knot check).
Need (Step 10): lib.slot_need (each terminal's arrivals matched to its departures) where every terminal is left by one leg,
otherwise the bus followed round the legs (pattern_need). Minimum wait 3 min, less where the slots chain closer as the real
timetable turns (never under 1); 0 before an untimed leg.
"""
import collections, statistics
from lib import CONFIG, load, save, nm, AL, hm, loop_shift, pattern_need, line_anchor, tmin, buslib

T = load('trips.json'); C = load('line_class.json')
LOOP = CONFIG['all_termini_are_loops']; LAY = CONFIG['cycle_lay']; FW = CONFIG['fitwin']
ALLOWED = [d for d in range(10, 481) if 1440 % d == 0]
ALLOWED_AUTO = [10, 12, 15, 20, 30, 40, 60, 90, 120, 180, 240, 480]   # 'auto': the plain intervals the owner uses

def cd(a, b, P): return min((a - b) % P, (b - a) % P)

def match(L, leg):
    """the real trips a leg stands for, read at its core points: [dict(t, d=time at fr, a=time at to, st=stops fr..to)].
    core_to: the core point a trip must pass to count (default to); a trip that ends there (369 ends at Havířov, Město,
    železniční stanice, short of the Podlesí terminal) still counts, with full=False."""
    fr, to = leg['fr'], leg.get('core_to', leg['to']); out = []   # via / notvia are checked on the whole trip
    for l in leg.get('lines', [L]):
        for t in T.get(l, []):
            st = [AL(nm(x)) for x in t['stops']]
            if fr not in st: continue
            i = st.index(fr)
            if to not in st[i + 1:]: continue
            j = st.index(to, i + 1)
            k = st.index(leg['to'], i + 1) if leg['to'] in st[i + 1:] else j
            seg = st[i:max(j, k) + 1]
            # via / notvia: the whole trip (a variant may differ beyond the leg: 451's Elektrárna trips go on past Lutyně)
            if any(v not in st for v in leg.get('via', [])) or any(v in st for v in leg.get('notvia', [])): continue
            if leg.get('starts') and i != 0: continue          # only trips that start at fr
            out.append(dict(line=l, lic=t['lic'], sp=t['sp'], d=t['times'][i], a=t['times'][k], st=seg, times=t['times'][i:max(j, k) + 1],
                            fr0=nm(t['fr']), to0=nm(t['to']), dep0=t['dep'], full=leg['to'] in st[i + 1:]))
    return sorted(out, key=lambda x: x['d'])

def med(xs): return round(statistics.median(xs)) if xs else None

def prep(L, lg, P):
    """one leg: its candidate trips (timed at the terminal: the knot time minus the running time fr -> knot) and slots"""
    fr, to = lg['fr'], lg['to']; ra = lg.get('knot', fr)
    mt = [x for x in match(L, dict(lg, core_to=to)) if x['full']]          # trips that run the whole leg fr -> to
    g = dict(fr=fr, to=to, core_to=lg.get('core_to', to), knot_stop=ra if ra != fr else None, lines=lg.get('lines', [L]),
             via=lg.get('via', []), notvia=lg.get('notvia', []), untimed=bool(lg.get('untimed')), note=lg.get('note', ''),
             src=lg.get('src', ''), spec=lg, mt=mt)
    if g['untimed']:
        g.update(every=0, real=[], set=[], cand=[], kr=0); return g
    kk = [x['times'][x['st'].index(ra)] - x['d'] for x in mt if ra in x['st']] if ra != fr else [0]
    kr = lg.get('knot_rt', med(kk) or 0)
    cand = [dict(x, d0=x['d'] - kr) for x in match(L, dict(lg, fr=ra))]
    if lg.get('at') == 'auto':
        # the slot on the minute the afternoon's real departures hit most, then within 3 min, then the whole day (Step 4)
        A_ = [x['d0'] for x in cand if 780 <= x['d0'] < 1140] or [x['d0'] for x in cand]
        D_ = [x['d0'] for x in cand if FW[0] <= x['d0'] < FW[1]]
        r = max(range(P), key=lambda r: (sum(1 for d in A_ if cd(d, r, P) == 0), sum(1 for d in A_ if cd(d, r, P) <= 3),
                                          sum(1 for d in D_ if cd(d, r, P) == 0), -r)) if A_ else 0
        lg = dict(lg, at=[r]); g['spec'] = lg; g['auto'] = True
    R = sorted({(tmin(v) - kr) % P for v in lg['knot_at']}) if 'knot_at' in lg else sorted({tmin(v) % P for v in lg['at']})
    assert len(R) <= 8, f'{L}: more than 8 slots at {fr} (Also at holds 7)'
    g.update(every=P, real=R, set=loop_shift(P, R, LOOP), cand=cand, kr=kr)
    if ra != fr: g['knot'] = dict(stop=ra, rt=kr, at=sorted({(r + kr) % P for r in R}))
    return g

def finish(L, sl, legs, W, anchor):
    """running times, stops, statistics, waits and need of one Simutrans line whose legs have their own trips"""
    P = sl['every']
    for g in legs:
        own = g.get('own', [])
        full = [x for x in own if x['full']] or [x for x in g['mt']]
        sv = g['spec'].get('stops_via', [])
        if sv: full = [x for x in (full + [y for y in g['mt'] if y not in full]) if all(v in x['st'] for v in sv)] or full
        near = [x for x in full if W[0] - 60 <= x['d'] < W[1] + 60] or full
        rt = g['spec'].get('rt')
        if rt is None and near:
            # the running time of the whole leg: own trips fr -> to; a leg read at a knot uses the trips that pass fr
            rt = med([x['a'] - x['d'] for x in near]) if (x0 := near[0]) and x0['st'][0] == g['fr'] else med([x['a'] - x['d'] + g['kr'] for x in near])
        if rt is None:
            rev = next((h for h in legs if h['fr'] == g['to'] and h['to'] == g['fr'] and h is not g), None)
            rt = rev['rt'] if rev and rev.get('rt') else None
        if rt is None: raise ValueError(f'{L} {sl["name"]}: no trip for leg {g["fr"]} -> {g["to"]} and no rt given')
        g['rt'] = rt
        # stops: the commonest path of the leg's own trips in the afternoon; `stops_via` picks the path through a stop only a
        # variant serves (367 back via Bruzovice, Zámostí and Lučina, as its evening trips run, so Zámostí is on a line).
        # A leg read at a knot takes its path from the trips that run it from its terminal (mt): its own trips are read from
        # the knot, so their path starts there (until 25 Oct 2026 such legs listed only the stops from the knot on)
        ps = ([x for x in g['mt'] if all(v in x['st'] for v in sv)] or g['mt']) if g['knot_stop'] and g['mt'] else full
        aft = [x for x in ps if 780 <= x['d'] < 1140] or ps
        g['stops'] = g['spec'].get('stops') or (list(collections.Counter(tuple(x['st']) for x in aft).most_common(1)[0][0]) if aft else [g['fr'], g['to']])
        if g['untimed']: continue
        D = [(x['d0'], min(cd(x['d0'], r, P) for r in g['real'])) for x in own if FW[0] <= x['d0'] < FW[1]]
        g['stat'] = dict(n=len(D), exact=sum(1 for _, v in D if v == 0), w1=sum(1 for _, v in D if v <= 1), w3=sum(1 for _, v in D if v <= 3),
                         worst=max((v for _, v in D), default=0))
        g['off'] = sorted(d for d, v in D if v > 3)
        ws = [t for t in range(W[0], W[1]) if t % P in g['real']]
        wd = [x['d0'] for x in own]
        g['window'] = dict(slots=ws, deps=sorted(d for d in wd if W[0] <= d < W[1]), empty=[s for s in ws if not any(abs(s - d) <= 3 for d in wd)])
        g['_own'] = own
        g['trips'] = [dict(line=x['line'], lic=x['lic'], sp=x['sp'], d=x['d0'], dk=x['d'], fr0=x['fr0'], to0=x['to0'], dep0=x['dep0'],
                           dev=min(cd(x['d0'], r, P) for r in g['real'])) for x in own]
    # both ends of an auto-fitted two-terminal line chosen together for the shortest round (shortest-wait rule, as the Ostrava
    # lib's plans): each end within a few minutes of its best fit (a third of the interval on sparse lines), then the pair
    # that needs the fewest buses, then the one closest to the best fits; otherwise a bus waits most of an interval
    timed = [g for g in legs if not g['untimed']]
    if len(legs) == 2 and len(timed) == 2 and all(g.get('auto') for g in timed) and all(len(g['real']) == 1 for g in timed):
        import math
        a, b = timed; a0, b0 = a['real'][0], b['real'][0]
        slack = max(3, P // 10) if P <= 60 else P // 3
        # the wait at each end is at least 3 min, or less where the best fits already turn closer (the real timetable's
        # turn, as the need below allows): a slot is not moved off a real timetable that turns in 1 min (738 at Slovenská)
        la = max(1, min(LAY, (a0 - (b0 + b['rt'])) % P)); lb = max(1, min(LAY, (b0 - (a0 + a['rt'])) % P))
        def rnd(ra, rb):
            wb = (rb - (ra + a['rt'] + lb)) % P + lb; wa = (ra - (rb + b['rt'] + la)) % P + la
            return a['rt'] + wb + b['rt'] + wa
        pairs = [((a0 + i) % P, (b0 + j) % P) for i in range(-slack, slack + 1) for j in range(-slack, slack + 1)]
        ra, rb = min(pairs, key=lambda x: (math.ceil(rnd(*x) / P), cd(x[0], a0, P) + cd(x[1], b0, P)))
        if (ra, rb) != (a0, b0):
            for g, r, r0 in ((a, ra, a0), (b, rb, b0)):
                if r == r0: continue
                g['joint'] = dict(fit=r0, moved=cd(r, r0, P))
                g['real'] = [r]; g['set'] = loop_shift(P, [r], LOOP)
                if g.get('knot'): g['knot']['at'] = [(r + g['kr']) % P]
                D = [(x['d0'], cd(x['d0'], r, P)) for x in g.get('_own', []) if FW[0] <= x['d0'] < FW[1]]
                g['stat'] = dict(n=len(D), exact=sum(1 for _, v in D if v == 0), w1=sum(1 for _, v in D if v <= 1), w3=sum(1 for _, v in D if v <= 3),
                                 worst=max((v for _, v in D), default=0))
                g['off'] = sorted(d for d, v in D if v > 3)
                ws = [t for t in range(W[0], W[1]) if t % P == r]; wd = [x['d0'] for x in g.get('_own', [])]
                g['window'] = dict(slots=ws, deps=sorted(d for d in wd if W[0] <= d < W[1]), empty=[t for t in ws if not any(abs(t - d) <= 3 for d in wd)])
                for t in g['trips']: t['dev'] = cd(t['d'], r, P)
    # minimum waits before each leg: 3 min, less where the slots chain closer (never under 1); 0 before an untimed leg
    for i, g in enumerate(legs):
        pv = legs[i - 1]
        if g['untimed']: g['lay'] = 0; continue
        lay = g['spec'].get('lay', LAY)
        if not pv['untimed'] and 'lay' not in g['spec']:
            arr = [(r + pv['rt']) % P for r in pv['real']]
            gap = min((s - a) % P for a in arr for s in g['real'])
            lay = max(1, min(lay, gap))
        g['lay'] = lay
    # the time the modelled bus passes each core point of a leg, against the real times there
    core = CONFIG['lines'][L].get('core', [])
    for g in legs:
        if g['untimed']: continue
        m = g['mt'] or g['cand']; ks = []
        for c in core:
            if c not in g['stops'][1:]: continue
            off = [x['times'][x['st'].index(c)] - x['d'] for x in m if c in x['st']]
            if not off: continue
            # the real times there: the trips that run the leg, and every trip it stands for that passes c (a leg read at a
            # knot stands for trips that start beyond its terminal: 292 Strahovice's Píšť trips at Hlučín)
            o = med(off); real = sorted({x['times'][x['st'].index(c)] for x in m + g['cand'] if c in x['st']})
            model = [s + o for s in g['window']['slots']] or [r + o for r in g['real']]
            ks.append(dict(stop=c, rt=o, model=model, dev=[min((abs(t - r) for r in real), default=None) for t in model]))
        g['knots'] = ks
    # need
    frs = [g['fr'] for g in legs]; need = None
    if len(set(frs)) == len(frs):
        tl = []
        for i, g in enumerate(legs):
            nx = legs[(i + 1) % len(legs)]
            deps = [(r + legs[i - 1]['rt']) % P for r in legs[i - 1]['real']] if g['untimed'] else g['real']
            tl.append((g['fr'], g['to'], deps, g['rt'], nx['lay']))
        try: need, waits = buslib.slot_need(P, tl); how = 'slot_need'
        except ValueError as e: how = str(e)
    if need is None:
        i0 = next(i for i, g in enumerate(legs) if not g['untimed'])
        lg_ = legs[i0:] + legs[:i0]
        rows = [dict(every=1, real=[0]) if g['untimed'] else dict(every=P, real=g['real']) for g in lg_]
        need, cyc, w = pattern_need(rows, [g['rt'] for g in lg_], [g['lay'] for g in lg_], anchor)
        waits = {f"{g['fr']} ({k + 1})": [w[k - 1]] for k, g in enumerate(lg_)}; how = 'pattern_need'
    # the waits in leg order (slot_need returns them in set order, which differs from run to run)
    waits = {k: waits[k] for k in sorted(waits, key=lambda k: (next((i for i, g in enumerate(legs) if k == g['fr'] or str(k).startswith(g['fr'] + ' (')), 99), str(k)))}
    for g in legs:
        for k in ('spec', 'mt', 'cand', 'own', '_own'): g.pop(k, None)
    return dict(name=sl['name'], every=P, window=W, legs=legs, need=need, waits=waits, how=how, why=sl.get('why', ''), auto=bool(sl.get('auto_every')) or any(g.get('auto') for g in legs))

def build(L, spec, anchor):
    sims = []
    for sl in spec.get('sim', []):
        P = sl['every']
        if P == 'auto':
            # the interval nearest the afternoon's average headway of the timed legs (13:00-18:00), divisors of 60 preferred
            ns = []
            for lg in sl['legs']:
                if lg.get('untimed'): continue
                ns.append(sum(1 for x in match(L, dict(lg, fr=lg.get('knot', lg['fr']))) if 780 <= x['d'] < 1080))
            h = 300 / max(0.5, sum(ns) / len(ns)) if ns else 480
            import math
            P = min(ALLOWED_AUTO, key=lambda x: abs(math.log(x / h)) - (0.2 if 60 % x == 0 else 0))
            sl = dict(sl, every=P, auto_every=True)
        assert P in ALLOWED, f'{L} {sl["name"]}: every {P} must divide 1440 and be at most 480'
        W = [tmin(x) for x in sl['window']] if sl.get('window') else [anchor - 30, anchor + 90]
        sims.append((sl, W, [prep(L, lg, P) for lg in sl['legs']]))
    # every trip read between the same points goes to the leg whose slot is nearest
    groups = collections.defaultdict(list)
    for sl, W, legs in sims:
        for g in legs:
            if not g['untimed']: groups[(g['knot_stop'] or g['fr'], g['core_to'], tuple(g['via']), tuple(g['notvia']))].append(g)
    for gs in groups.values():
        # compared at the read point (the knot time against each leg's slots there), so legs timed from different
        # terminals share one reading (553: Karviná trips and Orlová trips both read at Lutyně)
        byk = [{(x['lic'], x['sp']): x for x in g['cand']} for g in gs]
        for g in gs: g['own'] = []
        for k in sorted(set().union(*byk)):          # sorted: the same result on every run
            cs = [(min(cd(b[k]['d'], r + g['kr'], g['every']) for r in g['real']), i) for i, (g, b) in enumerate(zip(gs, byk)) if k in b]
            i = min(cs)[1]; gs[i]['own'].append(byk[i][k])
        for g in gs: g['own'].sort(key=lambda x: (x['d'], x['lic'], x['sp']))
    return [finish(L, sl, legs, W, anchor) for sl, W, legs in sims]

def clock(P, R):
    """the slots as written on the sheet: minutes for intervals dividing 60, else the clock times 5:00-23:00"""
    if 60 % P == 0: return ' '.join(':%02d' % (r % 60) for r in sorted({r % 60 for r in R for r in range(r, 60, P)}))
    return ' '.join(hm(t) for t in range(300, 1380) if t % P in R)

out = {}
for L, spec in CONFIG['lines'].items():
    if L not in T: print(L, 'has no trips on the day'); continue
    an = spec.get('anchor')
    a = dict(anchor=tmin(an), busiest=None, moved=True, set=True) if an else line_anchor(T[L], dict(peak_minute=960))
    sims = build(L, spec, a['anchor'])
    out[L] = dict(anchor=a, core=spec.get('core', []), note=spec.get('note', ''), sim=sims, listed=spec.get('listed', []),
                  name=C[L]['name'], areas=C[L]['areas'], lics=C[L]['lics'])
    for s in sims:
        print(f"{L:4} {s['name']:12} every {s['every']:3} need {s['need']}  " + ' | '.join(
            f"{g['fr'].split(', ')[-1][:10]}: " + ('untimed' if g['untimed'] else f"{clock(s['every'], g['real'])[:40]} ({g['stat']['exact']}/{g['stat']['w3']}/{g['stat']['n']}, off {len(g['off'])}, empty {len(g['window']['empty'])}, rt {g['rt']})")
            for g in s['legs']))

# ---------------------------------------------------------------- Step 9: every afternoon stop on a Simutrans line
# Covered here: the stops of every leg of this sheet's Simutrans lines. Covered elsewhere: stops the other sheets model in the
# afternoon (their own coverage checks are complete): the Hranečník ODIS lines on the Ostrava sheet, every DPO line there, and
# the Havířov/Karviná/Orlová town lines. The town JDFs of Karviná and Orlová write their own stops without the town name.
import json, os
from lib import rel, PIPE
here = {}
for L, x in out.items():
    for s in x['sim']:
        for g in s['legs']:
            for st in g['stops']: here.setdefault(st, set()).add(s['name'])
towns = {nm(st).split(',')[0] for tr in T.values() for t in tr for st in t['stops']}
els = {}
def mark(name, where): els.setdefault(name, set()).add(where)
for key, sh in CONFIG['other_sheets'].items():
    if not sh.get('schedule'): continue
    # another regional sheet of this pipeline (other_sheets.<key>.schedule): the stops of its Simutrans lines
    short = sh.get('short', 'ODIS regional Havířovsko sheet' if key == 'hko_regional' else sh['label'] + ' sheet')
    for L_, x_ in json.load(open(rel(sh['schedule']), encoding='utf-8')).items():
        if L_.startswith('_'): continue
        for s_ in x_['sim']:
            for g_ in s_['legs']:
                for st_ in g_['stops']: mark(st_, f"{s_['name']} ({short})")
for key, sh in CONFIG['other_sheets'].items():
    # lines another sheet models (the Ostrava Hranečník cards; a sibling regional sheet not built yet): their afternoon stops
    if key != 'ostrava' and sh.get('schedule'): continue
    for L in sh.get('lines', []):
        for t in T.get(L, []):
            for st, tm in zip(t['stops'], t['times']):
                if 780 <= tm < 1140: mark(AL(nm(st)), f"{L} ({'Ostrava sheet' if key == 'ostrava' else sh.get('short', sh['label'] + ' sheet')})")
for L, tr in json.load(open(os.path.join(PIPE, 'ostrava-bus/data/derived/trips.json'), encoding='utf-8')).items():
    for t in tr:
        for st, tm in zip(t['stops'], t['times']):
            if 780 <= tm < 1140: mark(AL(nm(st)), f'DPO {L} (Ostrava sheet)')
for L, tr in json.load(open(os.path.join(PIPE, 'havirov-karvina-orlova/data/derived/trips.json'), encoding='utf-8')).items():
    town = 'Havířov' if L.startswith('4') else 'Karviná' if int(L) >= 511 else 'Orlová'
    for t in tr:
        for st, tm in zip(t['stops'], t['times']):
            s_ = st.replace(',,', ',')
            if s_.split(',')[0] not in towns and not s_.startswith(town): s_ = town + ',' + s_
            if 780 <= tm < 1140: mark(AL(nm(s_)), f'MHD {L} (Havířov/Karviná/Orlová sheet)')
served = {}
for L, tr in T.items():
    for t in tr:
        for st, tm in zip(t['stops'], t['times']):
            if 780 <= tm < 1140: served.setdefault(AL(nm(st)), set()).add(L)
why = CONFIG.get('coverage_exceptions', {})
cov = dict(served=len(served), here=sum(1 for s in served if s in here), elsewhere={s: sorted(els[s]) for s in served if s not in here and s in els},
           by={s: sorted(here.get(s, set())) + sorted(els.get(s, set())) for s in served},
           served_by={s: sorted(ls) for s, ls in served.items()},
           uncovered={s: dict(lines=sorted(ls), why=why.get(s, '')) for s, ls in served.items() if s not in here and s not in els})
print(f"coverage: {cov['served']} afternoon stops, {cov['here']} on this sheet's lines, {len(cov['elsewhere'])} on other sheets' lines, "
      f"{len(cov['uncovered'])} uncovered: " + '; '.join(f"{s} ({', '.join(v['lines'])})" for s, v in cov['uncovered'].items()))
out['_coverage'] = cov
save('schedule.json', out)
