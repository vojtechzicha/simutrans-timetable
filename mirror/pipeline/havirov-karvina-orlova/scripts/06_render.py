"""derived/*.json + config + templates/page.html -> the published HTML in the project root.

The Ostrava bus sheet's layout, vehicle cell, schedule table and sticky controls (pipeline/ostrava-bus/scripts/06_render.py),
with this sheet's data: three town sections (Havířov, Karviná, Orlová), Transdev Slezsko branches as depots, fleet numbers
as strings (40-1017, 448), the course from the ODIS live map, and the VZ-MHD<Town> pak objects read from the pak repo.
Two roster states: provisional (morning peak sightings) and peak (each line at its own afternoon peak).
"""
import collections, glob, html, json, os, re
from lib import CONFIG, ROOT, PROJECT, load, nm_for, hm, loop_shift, town_of

C = CONFIG; E = html.escape; AL = C['terminus_alias']
def al(s): return AL.get(s, s)
fleet = load('fleet.json'); lines = load('lines.json'); R = load('roster.json'); SCH = load('schedule.json'); CLS = load('line_class.json')
LIVE = load('live.json')['cars']; TRIPS = load('trips.json'); PEAKS = load('peaks.json')
BR = {L: B['branches'] for L, B in R['branches'].items()}; OTH = {L: B['others'] for L, B in R['branches'].items()}
roster = R['roster']; OBS = R['observed']; order = R['order']; WIN = R['windows']
MODE = R['mode']; PROV = MODE == 'provisional'; LDAY = R['live_day']
WHY = {(a['line'], a['car']): a['why'] for a in R['added']}
DEPN = C['depots']; DCODE = {'Havířov': 'H', 'Karviná': 'K', 'Orlová': 'O'}

# ---- pak objects: the installed VZ-MHD<Town>-bus packages (names from the en tab files, lengths from the dat files)
PR = C['pak']['repo']; OBJ = {}          # (family, livery) -> {town: dict(head, parts, len, desc)}
for pkg in C['pak']['packages']:
    town = pkg.split('-')[1]                # MHDHavirov, or ODIS
    tab = os.path.join(PR, 'dist', 'text', f'en.{pkg}.tab')
    if not os.path.exists(tab): continue
    ls = open(tab, encoding='utf-8-sig').read().splitlines()
    names = dict(zip(ls[0::2], ls[1::2]))
    lens = {}
    for f in glob.glob(os.path.join(PR, 'build', pkg, '*.dat')):
        cur = None
        for ln in open(f, encoding='utf-8', errors='replace'):
            if ln.startswith('name='): cur = ln[5:].strip()
            elif ln.startswith('length=') and cur: lens[cur] = int(ln[7:].strip())
    for n in names:
        m = re.match(r'VZ-(MHD\w+|ODIS)-(.+?)-([a-z0-9]+)-(.+)$', n)
        if not m: continue
        _, fam, liv, part = m.groups()
        d = OBJ.setdefault((fam, liv), {}).setdefault(town, dict(parts=[], len=[], desc=names[n], prefix=f'VZ-{m.group(1)}-{fam}-{liv}-'))
        d['parts'].append(part); d['len'].append(lens.get(n))
for v in OBJ.values():
    for d in v.values():
        z = sorted(zip(d['parts'], d['len'])); d['parts'] = [a for a, _ in z]; d['len'] = [b for _, b in z]
TOWNPAK = {'Havířov': 'MHDHavirov', 'Karviná': 'MHDKarvina', 'Orlová': 'MHDOrlova'}
LIVN = {'odiscervenocerna': 'ODIS red-black', 'bilazelenykruh': 'white, green kraj ring', 'bilacervenykruh': 'white, red kraj ring', 'transdev': 'Transdev Morava', 'havirovmodra': 'Havířov city blue', 'karvinabilocerna': 'Karviná white-black', '3csadbilozelena': '3ČSAD white-green',
        'zelenametaliza': 'metallic green', 'bila': 'white'}
def livery(n):
    p = fleet[n].get('paint', '')
    return next((liv for key, liv in C['paint_rules'] if key in p), None), p
def family(n): return next((r[4] for r in C['type_rules'] if r[0] == fleet[n]['type']), None)
def odis_object(n):
    """the exact VZ-ODIS object of a regional bus (kraj or ODIS paint) working a town line, or None"""
    of = C.get('odis_types', {}).get(fleet[n]['type']); p_ = fleet[n].get('paint', '')
    rule = next((liv for key, liv in C.get('odis_paint_rules', []) if key in p_), None)
    if not of or not rule: return None
    liv = rule.split('|')[0]
    for alt in rule.split('|')[1:]:
        area, l2 = alt.split(':')
        if area in fleet[n].get('note', ''): liv = l2
    d = OBJ.get((of, liv), {}).get('ODIS')
    return (of, liv, d) if d else None
def pak(n, L):
    fam = family(n); want, paint = livery(n); home = TOWNPAK[town_of(L)['name']]
    exact_fam = fam and fleet[n]['type'] in [r[0] for r in C['type_rules'] if r[4] == fam] and \
        not any(x in fleet[n]['type'] for x in ('Crossway LE CITY', 'Crossway LE LINE 12', 'SOR CNG 12', 'SOR BNG 12', 'Dekstra LE', 'ICNG', 'EBN', 'Citywide LE 12', 'Suburban', 'Urbanway 10,5', 'Rošero-P First FCLLI (diesel)', 'Stratos LF 38 (diesel)'))
    def pick(f, liv):
        d = {t: v for t, v in OBJ.get((f, liv), {}).items() if t != 'ODIS'}
        if not d: return None
        t = home if home in d else sorted(d)[0]
        return t, d[t]
    hit = pick(fam, want) if fam and want else None
    if hit and hit[0] == 'ODIS': hit = None          # a town object first; VZ-ODIS only for the bus's own regional type and paint
    reason = ''
    od = None if (hit and exact_fam) else odis_object(n)
    if od: hit = ('ODIS', od[2]); exact = True
    elif hit and exact_fam: exact = True
    else:
        exact = False
        if hit: reason = f'no {fleet[n]["type"]} object: the {fam.replace("_", " ")} in the same paint'
        else:
            liv_any = next((liv for (f, liv) in OBJ if f == fam and any(t != 'ODIS' for t in OBJ[(f, liv)])), None) if fam else None
            if liv_any:
                hit = pick(fam, liv_any)
                reason = (f'no {fleet[n]["type"]} object in this paint ({paint or "unknown"})' if exact_fam else
                          f'no {fleet[n]["type"]} object: the {fam.replace("_", " ")}') + f', shown in {LIVN.get(liv_any, liv_any)}'
            else:
                hit = pick('Urbanway_12M_CNG', want if (('Urbanway_12M_CNG', want) in OBJ) else '3csadbilozelena')
                reason = f'no {fleet[n]["type"]} object: the Urbanway 12M CNG stands in'
    t, d = hit; liv = d['prefix'].split('-')[-2]
    core = d['parts'][0].replace('-A', '')
    multi = len([1 for (f, l) in OBJ if f == (d['prefix'].split('-')[2])]) > 1
    return dict(head=d['prefix'] + d['parts'][0], chain=' → '.join(d['prefix'] + x for x in d['parts']), pkg=f'VZ-{t}-bus', liv=liv,
                exact=exact, core=('≈ ' if not exact else '') + core + (f' · {LIVN.get(liv, liv)}' if multi else ''), reason=reason,
                length=' + '.join(str(x) for x in d['len'] if x), paint=paint)
PAKREQ = collections.defaultdict(set)

def depot(n, L=None):
    o = OBS.get(n)
    if o: return o['depot']
    for r in LIVE.get(n, []): return r[5]
    return town_of(L)['name'] if L else '?'
def vnum(nums): return f'<span class="veh" data-v="{"+".join(nums)}">{" + ".join(nums)}</span>'
def cell(nums, L):
    ps = [pak(n, L) for n in nums]
    for n, p in zip(nums, ps):
        if not p['exact']: PAKREQ[(fleet[n]['type'], p['paint'] or 'unknown paint')].add(n)
    dp = depot(nums[0], L)
    return (f'<div class="num">{vnum(nums)} <span class="dp d-{DCODE.get(dp, "H")}">{E(DEPN.get(dp, dp))}</span></div>'
            f'<div class="vt">{E(" + ".join(fleet[n]["full"] for n in nums))} · {E(" + ".join(fleet[n]["len"] for n in nums))}{(" · plate " + E(fleet[nums[0]]["plate"])) if fleet[nums[0]].get("plate") else ""}</div>'
            f'<div class="pak{"" if all(p["exact"] for p in ps) else " subst"}">{E(" + ".join(p["core"] for p in ps))}</div>')
def brname(b):
    if b.get('override'):
        e = b['ends']
        if len(e) == 2 and len(b['legs']) == 2: return ' ⇄ '.join(e)
        lg_ = b['legs']; return ' → '.join([lg_[0]['fr']] + [g['to'] + (f" ({g['note']})" if g.get('note') and not g['untimed'] else '') for g in lg_])
    return f"{b['a']} (circular)" if b.get('circular') else f"{b['a']} ⇄ {b['b']}"
def slname(L, bi):
    b = BR[L][bi]
    if b.get('name'): return b['name']
    auto = [i for i, x in enumerate(BR[L]) if not x.get('name')]
    return f"{L}{'ABCDEF'[auto.index(bi)]}" if len(auto) > 1 else L
def title(L):
    bs = BR[L]; a0 = bs[0]['a']
    if all(b.get('override') for b in bs):
        return ' – '.join(dict.fromkeys(e for b in bs for e in b['ends']))
    if len(bs) == 1 and bs[0].get('circular'):
        v = max(lines[L]['variants'], key=lambda v: v['n']) if lines[L]['variants'] else None
        mid = v['stops'][len(v['stops']) // 2] if v else ''
        return f"{a0} – {mid} – {a0} (circular)"
    if all(a0 in (b['a'], b['b']) for b in bs):
        return a0 + ' – ' + ' / '.join(b['b'] if b['a'] == a0 else b['a'] for b in bs)
    return ' / '.join(f"{b['a']} – {b['b']}" for b in bs)
def later_lines(n, L):
    w = WIN[L][1]; out = []
    for x in LIVE.get(n, []):
        if int(x[0][:2]) * 60 + int(x[0][3:]) > w and x[1] != L and x[1] not in out: out.append(x[1])
    return out
def T0_(L): return R.get('anchors', {}).get(L) or PEAKS.get(L, {}).get('anchor', C['peak_minute'])
def FW_(L): return (T0_(L) - 30, T0_(L) + 90)

CHECKS = []; CCHECKS = []; HCHECKS = []   # hand-set legs off the pattern or with more slots than real departures
def vt(g, k):
    if not g.get(k + '_via'): return None
    sk = g.get(k + '_skip')
    return ('not via ' if sk == 'notvia' else 'non-stop to ' if sk else 'via ') + g[k + '_via']
def hwtext(L, v):
    nm = nm_for(L)
    if all(b.get('override') for b in BR[L]): return f"every {v['hw']} min" if v['hw'] else 'single trip'   # hand-set: the timetable, not auto rows
    p = next((p for p in SCH[L] if nm(p['fr']) == v['fr'] and nm(p['to']) == v['to'] and p['every']), None)
    if p:
        r = p['real']; gaps = sorted({((r[(i + 1) % len(r)] - r[i]) % p['every']) or p['every'] for i in range(len(r))})
        return ('about ' if 'approx' in p else '') + 'every ' + '/'.join(map(str, gaps)) + ' min'
    return f"every {v['hw']} min" if v['hw'] else 'single trip'
def rtxt(p, v, loop):
    I = p['every']; r = (v + 60 + (1 if loop else 0)) % I
    if I == 1440: return hm(r) + ' daily'
    if I >= 120 and 1440 % I == 0:   # long intervals (Ex4 style): the clock times in the operating day, or the hour parity
        ts = [t for t in range(r, 1440, I) if 300 <= t < 1380]
        if I == 120: return f":{r % 60:02d} in {'even' if (r // 60) % 2 == 0 else 'odd'} hours"
        return ', '.join(hm(t) for t in ts)
    if 60 % I == 0: return str(r)
    t = 930 + ((r - 930) % I); return f"{t // 60}:{t % 60:02d}, every {I}"
def srow_fit(L, p):
    nm = nm_for(L)
    deps = sorted(set([t['dep'] for t in TRIPS[L] if nm(t['fr']) == nm(p['fr']) and nm(t['to']) == nm(p['to'])] + p.get('merged', [])))
    if p.get('vdeps'): deps = p['vdeps']
    W_ = p.get('fitwin') or FW_(L)
    band = [x for x in deps if W_[0] <= x < W_[1]]
    if p.get('circuit_leg'):
        w_ = FW_(L); realw = [x for x in deps if w_[0] <= x < w_[1]]
        sl = [t for t in range(w_[0], w_[1]) if t % p['every'] in p['real']]
        hit = sum(1 for t in sl if deps and min(abs(t - x) for x in deps) <= 3)
        if hit < len(sl): p['_miss'] = (hit, len(sl))
        fit = (f"stop {p['circuit_leg']} of the circuit; {hit} of {len(sl)} slots in {hm(w_[0])}–{hm(w_[1])} on a real departure (±3 min)"
               + f"<small>real {hm(w_[0])}–{hm(w_[1])}: {', '.join(hm(x) for x in realw) or 'none'}</small>")
    elif p.get('interleave'):
        il = p['interleave']; w_ = il.get('window') or list(FW_(L))
        realw = [x for x in deps if w_[0] <= x < w_[1]]
        fit = (f"{'far end of a branch ' if il.get('far') else ''}interleaved at {E(nm(il['at']))} with {E(', '.join(nm(x) for x in il['with_']) or 'the other branches')}"
               f"{': exact' if not il['dev'] else ', up to ' + str(il['dev']) + ' min off'} in {hm(w_[0])}–{hm(w_[1])}"
               f"<small>real {hm(w_[0])}–{hm(w_[1])}: {', '.join(hm(x) for x in realw) or 'none'}</small>")
    elif 'approx' in p:
        fit = (f"approximate, up to {p['approx']} min off" + (" (irregular: no even pattern fits)" if p['approx'] >= p['every'] // 3 else '') +
               f"<small>real {hm(W_[0])}–{hm(W_[1])}: {', '.join(hm(x) for x in band) or 'none'}</small>")
    else:
        out = [x for x in deps if FW_(L)[0] - 30 <= x < FW_(L)[1] + 30 and not p['first'] <= x <= p['last']]
        fit = f"exact {hm(p['first'])}–{hm(p['last'])} ({p['n']} dep.)" + (f"<small>outside the run: {', '.join(hm(x) for x in out)}</small>" if out else '')
    slots = len(p['real']) * (W_[1] - W_[0]) // p['every']; chk = 'approx' in p and slots > len(band)
    if p.get('_miss'):
        chk = True; CCHECKS.append((L, p))
        fit += (f"<div class='chkn'><b>Check:</b> {p['_miss'][1] - p['_miss'][0]} slot{'s' if p['_miss'][1] - p['_miss'][0] > 1 else ''} more than 3 min off a real departure (real times above). "
                + ("A merged row would serve one path only.</div>" if p.get('paths') else f"As separate branch lines: {p['sep']} buses.</div>"))
    if chk and 'approx' in p:
        al_ = p.get('alt'); fmt = lambda x: f"every {x['every']}, Offset {x['set'][0]}" + (f", Also at {', '.join(map(str, x['set'][1:]))}" if len(x['set']) > 1 else '')
        alt = (f" Slower option: {fmt(al_)}, up to {al_['approx']} min off." if al_ and al_['every'] > p['every'] else '')
        fit += (f"<div class='chkn'><b>Check:</b> {slots} slots in {hm(W_[0])}–{hm(W_[1])} against {len(band)} real departures, so "
                f"{slots - len(band)} slot{'s' if slots - len(band) > 1 else ''} would run empty or spread the buses thinner.{E(alt)} "
                f"Switch both ends of the line together.</div>")
        CHECKS.append((L, p, slots, band, al_))
    if p.get('refit') and isinstance(p['refit'], dict):
        rf = p['refit']; nh = len(p['real']) * 60 / p['every']
        fit += (f"<small>matched to the other end ({nh:g} an hour); this end alone fitted every {rf['every']} "
                f"({', '.join(f':{x:02d}' for x in rf['real'])}) {hm(rf['first'])}–{hm(rf['last'])}</small>")
    lp_ = p.get('loop', C['all_termini_are_loops'])
    real_o = f"<small class='real'>real {rtxt(p, p['set'][0], lp_)}</small>"
    real_a = f"<small class='real'>real {', '.join(rtxt(p, v, lp_) for v in p['set'][1:])}</small>" if len(p['set']) > 1 else ''
    fr, to = nm(p['fr']), nm(p['to'])
    lab = f"{E(fr)} &rarr; round the loop" if fr == to else f"{E(fr)} &rarr; {E(to)}"
    return (f"<tr{' class=chk' if chk else ''}><td>{lab}{f'<span class=\"lp lnt\">{E(p[chr(110)+chr(111)+chr(116)+chr(101)])}</span>' if p.get('note') else ''}<span class='lp'>{'1 min early' if lp_ else 'timetable minute'}</span></td>"
            f"<td class='n sv'>{p['every']}</td><td class='n sv'>{p['set'][0]}{real_o}</td><td class='sv'>{', '.join(map(str, p['set'][1:])) or '&mdash;'}{real_a}</td><td class='n'>auto</td><td class='fit'>{fit}</td></tr>")

def orow(L, b, g, k):
    """one leg of a hand-set Simutrans line (config.line_overrides): typed values, real minutes, and what it carries"""
    lp_ = C['all_termini_are_loops']
    if g['untimed']:
        return (f"<tr><td>{E(g['fr'])} &rarr; {E(g['to'])}<span class='lp lnt'>stop {k} of the line</span></td><td class='n sv'>0</td><td class='n sv'>&mdash;</td><td class='sv'>&mdash;</td>"
                f"<td class='n'>auto</td><td class='fit'>no timetable (Departure every 0): {E(g['note'])}; {g['rt']} min</td></tr>")
    I = g['every']; W = b['window']
    # legs of this line between the same two stops share their real departures (504: two paths Lazy -> Lutyně), so
    # counts and checks are made on the slots of all of them together, and only once, on the first such leg
    peers = [h for h in b['legs'] if not h['untimed'] and h['fr'] == g['fr'] and h['to'] == g['to']]
    slots_ = sorted({x for h in peers for x in h['real']})
    first = peers[0] is g
    with_ = [str(b['legs'].index(h) + 1) for h in peers if h is not g]
    band = [d for d in g['deps'] if I == 1440 or W[0] <= d < W[1]]
    if I == 1440: fit = f"daily timetable: every departure of the day in the window ({len(band)})"
    else:
        offs = [x for x in (g.get('off') or []) if x in band]
        on_ = sum(1 for d in band if min(min((d - x) % I, (x - d) % I) for x in slots_) <= 3)
        fit = ((f"together with stop {', '.join(with_)}: " if with_ else '')
               + (f"{on_} of {len(band)} real departures {hm(W[0])}–{hm(W[1])} on the slots (±3 min)" + (f"; off the pattern: {', '.join(hm(x) for x in offs)}" if offs else ''))
               if (first or not with_) else f"its departures are counted at stop {with_[0]}")
    if b.get('fitwin') and b['fitwin'] != b['window'] and I < 1440 and (first or not with_):   # owner, Ex4: the pattern over the whole day
        alld = g['deps']; ex = sum(1 for d in alld if min(min((d - x) % I, (x - d) % I) for x in slots_) <= 1)
        fit += f"<small>whole day {hm(b['fitwin'][0])}–{hm(b['fitwin'][1])}: {ex} of {len(alld)} real departures on the slots (±1 min)</small>"
    if g.get('knot'):   # timed at the terminal, worked back from the knot (buses wait only at terminals)
        kn = g['knot']
        fit = (f"timed at the terminal so the bus passes {E(kn['stop'])} at "
               + (', '.join(f":{(x + k * I) % 60:02d}" for x in kn['real'] for k in range(60 // I)) if 60 % I == 0 else
                  ', '.join(rtxt(dict(g, every=I), (x - 60 - (1 if lp_ else 0)) % I, lp_) for x in kn['real']))
               + f" ({kn['rt']} min from here); no timetable at {E(kn['stop'])}. " + fit)
    fit += f"<small>{E(g['src'])}</small>"
    # slots across the span of the real departures (not the whole window: 409 starts at 16:46)
    nslots = sum(1 for t in range(min(band) - I // 2, max(band) + I // 2 + 1) if t % I in slots_ and W[0] <= t < W[1]) if band and I < 1440 else len(band)
    offw = [x for x in (g.get('off') or []) if x in band]
    if (first or not with_) and I < 1440 and (offw or nslots > len(band)):   # owner rule: doubtful rows are listed, never silently kept
        alt = None
        if nslots > len(band) and 1440 % (2 * I) == 0 and len(slots_) == 1:
            I2 = 2 * I; cd = lambda a, b: min((a - b) % I2, (b - a) % I2)
            r2 = min(range(I2), key=lambda r: (-sum(1 for d in band if cd(d, r) <= 1), max([cd(d, r) for d in band] or [0])))
            alt = dict(every=I2, real=[r2], set=loop_shift(I2, [r2], lp_), dev=max([cd(d, r2) for d in band] or [0]))
            if alt['dev'] > max(3, g['dev']): alt = None   # a slower option only where it really fits
        HCHECKS.append((L, slname(L, BR[L].index(b)), dict(g, off=offw), nslots, band, alt))
        fit += (f"<div class='chkn'><b>Check:</b> " + (f"off the pattern: {', '.join(hm(x) for x in offw)}. " if offw else '')
                + (f"{nslots} slots against {len(band)} real departures. " if nslots > len(band) else '')
                + (f"Slower option: every {alt['every']}, Offset {alt['set'][0]}, up to {alt['dev']} min off." if alt else '') + "</div>")
    real_o = f"<small class='real'>real {rtxt(g, g['set'][0], lp_)}</small>"
    if I >= 240 and len(g['set']) > 1:   # long intervals: all the clock times of the Also-at slots in time order
        ts_ = sorted(t for v in g['set'][1:] for t in range((v + 60 + (1 if lp_ else 0)) % I, 1440, I) if 300 <= t < 1380)
        real_a = f"<small class='real'>real {', '.join(hm(t) for t in ts_)}</small>"
    else:
        real_a = f"<small class='real'>real {', '.join(rtxt(g, v, lp_) for v in g['set'][1:])}</small>" if len(g['set']) > 1 else ''
    return (f"<tr><td>{E(g['fr'])} &rarr; {E(g['to'])}{(' <i>' + E(g['note']) + '</i>') if g.get('note') else ''}<span class='lp lnt'>stop {k} of the line</span><span class='lp'>1 min early</span></td>"
            f"<td class='n sv'>{I}</td><td class='n sv'>{g['set'][0]}{real_o}</td><td class='sv'>{', '.join(map(str, g['set'][1:])) or '&mdash;'}{real_a}</td><td class='n'>auto</td><td class='fit'>{fit}</td></tr>")

TRIPSTOPS = {}
for L_, ts_ in TRIPS.items():
    for t in ts_: TRIPSTOPS[(R.get('carried', {}).get(L_, L_), hm(t['dep']), nm_for(L_)(t['fr']))] = [nm_for(L_)(x) for x in t['stops']]
cards = {}; perline = {}; pertype = collections.Counter()
for L in order:
    nm = nm_for(L)
    ros = roster[L]; V = lines[L]['variants']; perline[L] = len(ros)
    for u in ros: pertype[(u[0], depot(u[1][0], L))] += 1
    rows = ''.join(f"<tr><td>{E(v['fr'])}</td><td class='arr'>&rarr;</td><td>{E(v['to'])}</td><td class='n'>{hwtext(L, v)}</td>"
                   f"<td class='n mono'>{' '.join(f':{m:02d}' for m in v['min_peak_hour']) or '&mdash;'}</td><td class='n'>{v['rt']} min</td></tr>" for v in V)
    lh = f'{T0_(L) // 60:02d}'
    sch = ''; placed = set()
    def srow(p):
        if not p['every']:
            into = f" Its minutes are folded into the {E(nm(p['fr']))} &rarr; {E(nm(p['into']))} row." if p.get('into') else ''
            return f"<tr class='all'><td>{E(nm(p['fr']))} &rarr; {E(nm(p['to']))}</td><td colspan='5'>variant at {', '.join(hm(x) for x in p['single'])}, not scheduled.{into}</td></tr>"
        return srow_fit(L, p)
    if all(b.get('override') for b in BR[L]): placed = set(range(len(SCH[L])))
    if any(b.get('legs') and not b.get('override') for b in BR[L]):
        LP = C['all_termini_are_loops']
        for bi, b in enumerate(BR[L]):
            I = b['period']; legs = b['legs']; Ys = list(dict.fromkeys(g['Y'] for g in legs))
            if len(Ys) == 1 and not b.get('paths'):
                sch += f"<tr class='brh'><td colspan='6'>Simutrans line {slname(L, bi)}: {E(legs[0]['X'])} ⇄ {E(Ys[0])}</td></tr>"
                outs = sorted(g['out_slot'] for g in legs); backs = sorted(g['back_slot'] for g in legs)
                sch += srow_fit(L, dict(fr=legs[0]['X'], to=Ys[0], every=I, real=outs, set=loop_shift(I, outs, LP), circuit_leg=1, sep=b['sep_need']))
                sch += srow_fit(L, dict(fr=Ys[0], to=legs[0]['X'], every=I, real=backs, set=loop_shift(I, backs, LP), circuit_leg=2, sep=b['sep_need']))
            else:
                vv = lambda g, k: f" ({vt(g, k)})" if g.get(k + '_via') else ''
                route = [legs[0]['X']] + [x for g in legs for x in (g['Y'] + vv(g, 'out'), g['X'] + vv(g, 'back'))]
                sch += f"<tr class='brh'><td colspan='6'>Simutrans line {slname(L, bi)}, one circuit: {E(' → '.join(route))}</td></tr>"
                k = 0
                for g in legs:
                    k += 1; sch += srow_fit(L, dict(fr=g['X'], to=g['Y'], every=I, real=[g['out_slot']], set=loop_shift(I, [g['out_slot']], LP), circuit_leg=k, sep=b['sep_need'], paths=b.get('paths'), note=vt(g, 'out'), vdeps=g.get('out_deps')))
                    k += 1; sch += srow_fit(L, dict(fr=g['Y'], to=g['X'], every=I, real=[g['back_slot']], set=loop_shift(I, [g['back_slot']], LP), circuit_leg=k, sep=b['sep_need'], paths=b.get('paths'), note=vt(g, 'back'), vdeps=g.get('back_deps')))
        pairs_ = {frozenset((g['X'], g['Y'])) for b in BR[L] if not b.get('override') for g in b['legs']}
        placed = {i for i, p in enumerate(SCH[L]) if frozenset((al(nm(p['fr'])), al(nm(p['to'])))) in pairs_}
    for bi, b in enumerate(BR[L] if not any(b_.get('legs') and not b_.get('override') for b_ in BR[L]) else []):
        if b.get('override'): continue
        if len(BR[L]) > 1: sch += f"<tr class='brh'><td colspan='6'>Simutrans line {slname(L, bi)}: {E(brname(b))}</td></tr>"
        for i, p in enumerate(SCH[L]):
            if i not in placed and {al(nm(p['fr'])), al(nm(p['to']))} == {b['a'], b['b']}: sch += srow(p); placed.add(i)
    for bi, b in enumerate(BR[L]):
        if not b.get('override'): continue
        sch += f"<tr class='brh'><td colspan='6'>Simutrans line {E(slname(L, bi))}{', one circuit' if len(b['legs']) > 2 else ''}: {E(brname(b))}</td></tr>"
        sch += ''.join(orow(L, b, g, k + 1) for k, g in enumerate(b['legs']))
    rest = [p for i, p in enumerate(SCH[L]) if i not in placed] if not all(b.get('override') for b in BR[L]) else []
    if rest: sch += "<tr class='brh'><td colspan='6'>Other variants</td></tr>" + ''.join(srow(p) for p in rest)
    stopsd = ''; seen = set(); ppairs = set()
    for b in BR[L]:
        for g in (b['legs'] if b.get('override') else []):
            if len(g.get('stops', [])) > 2 and tuple(g['stops']) not in seen:
                seen.add(tuple(g['stops'])); ppairs.add((g['fr'], g['to']))
                stopsd += f"<p><b>{E(slname(L, BR[L].index(b)))}: {E(g['fr'])} &rarr; {E(g['to'])}</b> ({len(g['stops'])} stops): {E(' · '.join(g['stops']))}</p>"
        for g in ([] if b.get('override') else b.get('legs', [])):
            for k, a_, b_ in (('out', g['X'], g['Y']), ('back', g['Y'], g['X'])):
                if g.get(k + '_stops') and tuple(g[k + '_stops']) not in seen:
                    seen.add(tuple(g[k + '_stops'])); ppairs.add((a_, b_)); st = [nm(x) for x in g[k + '_stops']]
                    stopsd += f"<p><b>{E(a_)} &rarr; {E(b_)} {E(vt(g, k))}</b> ({len(st)} stops): {E(' · '.join(st))}</p>"
    for v in V:
        if tuple(v['stops']) in seen or v['n'] < 2 or (al(v['fr']), al(v['to'])) in ppairs: continue
        seen.add(tuple(v['stops']))
        stopsd += f"<p><b>{E(v['fr'])} &rarr; {E(v['to'])}</b> ({len(v['stops'])} stops): {E(' · '.join(v['stops']))}</p>"
    chips = ''
    W = WIN[L]
    for bi, b in enumerate(BR[L]):
        head = f"Simutrans line {slname(L, bi)}: " if len(BR[L]) > 1 else ''
        how = (f"round {b['cycle']} min on its hand-set slots ({'daily timetable' if b['every'] == 1440 else 'every ' + str(b['every'])})" if b.get('override') else
               f"round {b['cycle']} min on its suggested slots (every {b.get('period')}): out on one path, back on the other; one Simutrans line, so both paths are served" if b.get('how') == 'circuit' and b.get('paths') else
               f"round {b['cycle']} min on its suggested slots (every {b['period']}); the line as {len(BR[L])} Simutrans line{'s' if len(BR[L]) > 1 else ''} needs {sum(x['need'] for x in BR[L])} against {b['sep_need']} as separate branch lines" if b.get('how') == 'circuit' else
               f"round {b['cycle']} min on the suggested {'approximate ' if b.get('approx') else ''}pattern (every {b['pattern_every']}): {b['runtimes'][0]} min round the loop, waits {b['waits'][0]} min at the start" if b['how'] == 'pattern' and b.get('circular') else
               f"round {b['cycle']} min on the suggested {'approximate ' if b.get('approx') else ''}pattern (every {b['pattern_every']}): {b['runtimes'][0]} + {b['runtimes'][1]} min running, waits {b['waits'][1]} and {b['waits'][0]} min at the termini" if b['how'] == 'pattern' else
               f"buses the timetable chains at {hm(T0_(L))}")
        us = [u for u in ros if u[3] == bi]
        seenw = f"seen {hm(W[0])}–{hm(W[1])} this morning" if PROV else f"seen live {hm(W[0])}–{hm(W[1])}"
        sub = f"{head}{brname(b)} · {b['assigned']} assigned ({b['observed']} {seenw}), {b['need']} needed ({how})" + (f" · {b['surplus']} more seen, not needed" if b.get('surplus') else '')
        def chip(u):
            t, nums, flag, _, course = u
            if flag == 'designed':
                extra = f'<div class="addn">designed, not recorded: {E(WHY.get((L, nums[0]), "").split(";")[0])}</div>'
            elif flag == 'morning':
                extra = f'<div class="vt">course {course} · seen {E(OBS[nums[0]]["first"])} this morning, not yet confirmed in the afternoon</div>'
            else:
                extra = f'<div class="vt">course {course} · seen {E(OBS[nums[0]]["first"])}</div>' if course is not None else ''
            cls = ' added' if flag == 'designed' else (' eve' if flag == 'morning' else ' seen')
            return f'<li class="v{cls}">{cell(nums, L)}{extra}</li>'
        sur = [u for u in R.get('surplus', {}).get(L, []) if u[3] == bi]
        surli = ''.join(f'<li class="v spare">{cell(u[1], L)}<div class="vt">not needed · course {u[4]} · seen {E(OBS[u[1][0]]["first"])}; more buses seen than this line needs (one of each type kept, then the lowest courses)</div></li>' for u in sur)
        chips += f'<p class="brsub">{E(sub)}</p><ul class="vs">' + ''.join(chip(u) for u in sorted(us, key=lambda u: (u[0], u[1]))) + '</ul>'
        if sur: chips += f'<details class="nn"><summary>Not needed: {len(sur)} more bus{"es" if len(sur) > 1 else ""} seen at the peak</summary><ul class="vs">{surli}</ul></details>'
    sp = R.get('spares', {}).get(L, [])
    if sp:
        chips += (f'<details class="nn"><summary>Not needed: {len(sp)} more bus{"es" if len(sp) > 1 else ""} from the line’s records, free that afternoon (not counted)</summary><ul class="vs">' +
                  ''.join(f'<li class="v spare">{cell([x["car"]], L)}<div class="vt">not needed · last on line {L} {E(x["last"])} · {x["records"]} records · free that afternoon</div></li>' for x in sp) + '</ul></details>')
    othtxt0 = ''
    pk_ = PEAKS.get(L, {})
    if pk_.get('moved') and not all(b.get('override') for b in BR[L]):
        othtxt0 = (f'<p class="lnote"><b>Modelled at its afternoon peak, {hm(pk_["busiest"][0])}–{hm(pk_["busiest"][1])}.</b> Its busiest 2 hours have {pk_["n"]} departures, '
                   f'against {pk_["at_peak"]} in 15:00–17:00, so the schedule, the need and the observation window follow that stretch.</p>')
    v_ = load('versions.json')['chosen'][L]
    if v_.get('diversion'): othtxt0 += f'<p class="lnote"><b>Diversion timetable</b> valid {v_["valid_from"]} – {v_["valid_to"]} (see Network state).</p>'
    for bi, b in enumerate(BR[L]):
        if b.get('override'): othtxt0 += f'<p class="lnote"><b>Simutrans line {E(slname(L, bi))}, set by hand.</b> {E(b["why"])}</p>'
    for L2, by in R.get('carried', {}).items():
        if by == L: othtxt0 += f'<p class="lnote"><b>Line {L2} runs on this line.</b> {E(C["line_overrides"][L2]["why"])}</p>'
    um = R['unmodelled'].get(L, []) + [x for L2, by in R.get('carried', {}).items() if by == L for x in R['unmodelled'].get(L2, [])]
    own = {slname(L, bi) for bi in range(len(BR[L]))}
    def ontxt(x):
        if x['miss']: return 'NOT COVERED: ' + ', '.join(x['miss'])
        st = TRIPSTOPS.get((L, x['dep'], x['fr']), [])
        extra = [y for y in st if not set(R['covered'].get(y, [])) & own]
        if not extra: return 'all its stops are on this line’s Simutrans lines'
        return ', '.join(extra[:3]) + (' …' if len(extra) > 3 else '') + ' on Simutrans line ' + ', '.join(sorted({n for y in extra for n in R['covered'].get(y, [])}))
    def _unused(x):
        ls = sorted({n for st in [x['fr'], x['to']] for n in R['covered'].get(st, [])})
        return 'its stops are on Simutrans lines ' + ', '.join(sorted({n for st in TRIPSTOPS.get((L, x['dep'], x['fr']), []) for n in R['covered'].get(st, [])})) if not x['miss'] else 'NOT COVERED: ' + ', '.join(x['miss'])
    othtxt = ('<p class="lnote">Afternoon trips not on a Simutrans line of this line (13:00–19:00): ' + E('; '.join(f"{x['dep']} {x['fr']} → {x['to']} ({ontxt(x)})" for x in um)) + '.</p>') if um else ''
    cnt = (len(ros), 'buses' if any(b.get('override') for b in BR[L]) else f'buses at {hm(T0_(L))}')
    mix = ', '.join(f"{c}× {t}" for t, c in collections.Counter(u[0] for u in ros).most_common())
    sub_h = (mix + ' · ' if mix else '') + f"{len(BR[L])} Simutrans line{'s' if len(BR[L]) > 1 else ''}"
    cards[L] = (f"""<article class="card" id="l{L}"><header><span class="badge">{L}</span><div class="hd"><h3>{E(title(L))}</h3><p>{E(sub_h)}</p></div><div class="cnt"><b>{cnt[0]}</b><span>{cnt[1]}</span></div></header>
<div class="tw"><table class="tt"><thead><tr><th>From</th><th></th><th>To</th><th class="n">Headway</th><th class="n">Leaves {lh}:xx</th><th class="n">Runtime</th></tr></thead><tbody>{rows}</tbody></table></div>
<div class="sched"><h4>Simutrans schedule · departures set 1 min early</h4><div class="tw0"><table class="st2"><thead><tr><th>Terminus entry</th><th class="n">Departure every (min)</th><th class="n">Offset (min)</th><th>Also at (min)</th><th class="n">Leave up to</th><th>Fit</th></tr></thead><tbody>{sch}</tbody></table></div></div>
{othtxt0}{othtxt}{chips}
<details><summary>Stops</summary>{stopsd}</details></article>""")

# ---- buses the timetable itself chains at 16:00 per town (trips joined at the same terminus within 25 min, across lines):
# what the real operator needs when buses swap lines, against the sum of the per-line needs
def chained_at(Ls, T=960):
    AL_ = C['terminus_alias']; tr = []
    for L_ in Ls:
        nm = nm_for(L_)
        tr += [dict(o=AL_.get(nm(t['fr']), nm(t['fr'])), d=AL_.get(nm(t['to']), nm(t['to'])), dep=t['dep'], arr=t['arr']) for t in TRIPS[L_] if 600 <= t['dep'] < 1260]
    bl = []
    for t in sorted(tr, key=lambda t: t['dep']):
        c_ = [b for b in bl if b[-1]['d'] == t['o'] and 0 <= t['dep'] - b[-1]['arr'] <= 25]
        if c_: min(c_, key=lambda b: t['dep'] - b[-1]['arr']).append(t)
        else: bl.append([t])
    return sum(1 for b in bl if b[0]['dep'] <= T <= b[-1]['arr'])

# ---- town sections
towns = ''; townnav = ''
for t in C['towns']:
    Ls = [L for L in order if town_of(L)['name'] == t['name']]
    need = sum(b['need'] for L in Ls for b in BR[L]); nb = sum(len(roster[L]) for L in Ls)
    allL = [L_ for L_ in TRIPS if town_of(L_)['name'] == t['name']]
    ch = chained_at(allL)
    off16 = sum(b['need'] for L_ in Ls for b in BR[L_] if b.get('override') and (b['every'] == 1440 or not b['window'][0] <= 960 < b['window'][1]))
    carried_ = [f"{L2} (on {by})" for L2, by in R.get('carried', {}).items() if town_of(L2)['name'] == t['name']]
    towns += (f'<h2 class="town" id="t-{t["id"]}">{E(t["name"])} · {len(Ls)} lines, {need} buses needed</h2>'
              f'<p class="townsub">MHD {E(t["name"])}: lines {", ".join(Ls)}{"; " + ", ".join(carried_) if carried_ else ""}. {nb} buses on the sheet ({E(DEPN[t["name"]])} and others, see each bus). '
              f'The timetable itself chains its trips into about {ch} buses at 16:00, with buses swapping lines at the termini; as separate Simutrans lines the town needs {need}'
              + (f', of which {off16} are on hand-set lines that do not run at 16:00 (midday, shift and evening forms on long intervals). ' if off16 else '. ')
              + ''
              + ('Karviná’s buses change line at almost every trip at Fryštát, so pooling some lines would be the owner’s choice; the sheet keeps one Simutrans line per real line.' if t['id'] == 'karvina' else '') + '</p>'
              f'<div class="grid">{"".join(cards[L] for L in Ls)}</div>')
    townnav += f"<a href='#t-{t['id']}'>{E(t['name'])}</a>"

# ---- not in the afternoon peak
def rname(L, v): nm = nm_for(L); ps = v['name'].split('-'); return nm(ps[0]) + ' – ' + nm(ps[-1]) if len(ps) > 1 else v['name']
offpeak = ''.join(f"<tr><td><b>{L2}</b></td><td>{E(rname(L2, CLS[L2]))}</td><td>runs on Simutrans line {by}: {E(C['line_overrides'][L2]['why'])}</td></tr>" for L2, by in R.get('carried', {}).items())
for L, v in sorted(CLS.items(), key=lambda x: int(x[0])):
    if v['cls'] == 'peak' and L not in R['occasional']: continue
    what = 'night only' if v['cls'] == 'night' else ('occasional: ' + str(R['occasional'][L]) + ' trip in 13:00–19:00, over stops other lines serve (' + ', '.join(sorted({n for x in R['unmodelled'].get(L, []) for st in TRIPSTOPS.get((L, x['dep'], x['fr']), []) for n in R['covered'].get(st, [])})) + ')' if L in R['occasional'] else v['cls'])
    offpeak += f"<tr><td><b>{L}</b></td><td>{E(rname(L, v))}</td><td>{E(what)}{(', ' + str(v['trips']) + ' trips a day, ' + v['first'] + '–' + v['last']) if v.get('first') else ''}</td></tr>"

# ---- depots (Transdev branches)
dsec = ''; depcount = {}
for dname in DEPN:
    rows = ''; tot = 0
    for L in order:
        for bi, b in enumerate(BR[L]):
            us = [u for u in roster[L] if u[3] == bi and depot(u[1][0], L) == dname]
            if not us: continue
            tot += len(us)
            rows += f"<tr class='brh'><td colspan='2'><a class='badge sm' href='#l{L}'>{L}</a> {E(brname(b))}{' (Simutrans line ' + slname(L, bi) + ')' if len(BR[L]) > 1 else ''} · {len(us)}</td></tr>"
            for u in sorted(us, key=lambda u: (u[0], u[1])):
                n = u[1][0]; st = []
                if u[2] == 'designed': st.append('designed, not recorded: ' + WHY.get((L, n), ''))
                elif n in OBS: st.append(f"live {LDAY} {OBS[n]['first']}: course {OBS[n]['course']}" + ('; seen in the morning, not yet confirmed in the afternoon' if PROV else ''))
                ll = later_lines(n, L)
                if ll and u[2] != 'designed': st.append('later on line ' + ', '.join(ll))
                rows += f"<tr><td class='vc'>{cell(u[1], L)}</td><td class='stc'>{E('; '.join(st) or '—')}</td></tr>"
    depcount[dname] = tot
    dsec += f"""<section class="depot" id="d{DCODE[dname]}"><header><h3>{E(DEPN[dname])}</h3><div class="cnt"><b>{tot}</b><span>buses on the sheet</span></div></header>
<div class="tw0"><table class="dt"><thead><tr><th>Vehicle</th><th>Live feed {E(C['live']['label'])}</th></tr></thead><tbody>{rows}</tbody></table></div></section>"""
DEPNAV = ''.join(f"<a href='#d{DCODE[d]}'>{E(d)} <b>{depcount[d]}</b></a>" for d in DEPN)

# ---- not in service: free buses of the town types, per branch
used = {n for L in roster for u in roster[L] for n in u[1]}
sparehead = f'<h2>Other buses of the town fleets</h2><p class="sub">Buses in the town paints (Havířov blue, Karviná white-black) or with records on these lines that are not on the sheet, per branch, with any line the live feed showed them on that day.</p>'
spsec = ''
hist_cars = {n for L_, n, d, note in load('history.json')}
for dname in DEPN:
    items = []
    for n, c in sorted(fleet.items()):
        if c['state'] != 'zar' or n in used: continue
        town = any(k in c.get('paint', '') for k in ('Havířov', 'bílo-černá')) or n in hist_cars
        if not town or depot(n, None) not in (dname, '?'): continue
        if depot(n, None) == '?' and not any(town_of(L_)['name'] == dname for L_, n_, d, note in load('history.json') if n_ == n): continue
        ll = list(dict.fromkeys(x[1] for x in LIVE.get(n, [])))
        items.append(f"{n} {c['full']}" + (f" (live on line {', '.join(ll)})" if ll else ''))
    spsec += f"<div class='sp'><h4>{E(DEPN[dname])}</h4><p><b>not on the sheet</b> ({len(items)}) <span>{' · '.join(E(x) for x in items)}</span></p></div>"

# ---- pak table (after the cards, so every vehicle has been through pak())
agg = collections.Counter(); info = {}
for L in order:
    for u in roster[L]:
        for n in u[1]:
            p = pak(n, L); key = (fleet[n]['full'], p['paint'], p['head']); agg[key] += 1; info[key] = p
paks = ''
for key, c in sorted(agg.items()):
    p = info[key]
    near = f"<div class='pak subst'>nearest: {E(p['reason'])}</div>" if not p['exact'] else ''
    paks += (f"<tr><td>{E(key[0])}<div class='lv'>{E(key[1] or 'paint unknown')}</div></td><td><b class='core'>{E(p['core'])}</b><div class='pak'>{E(p['chain'])} ({E(p['pkg'])})</div>{near}</td>"
             f"<td>{E(LIVN.get(p['liv'], p['liv']))}</td><td class='n'>{E(p['length'])}</td><td class='n'>{c}</td></tr>")

# ---- types table
cats = {}
for r in C['type_rules']: cats.setdefault(r[1], r[3])
tc = collections.Counter();
for (cat, dp), k in pertype.items(): tc[cat] += k
trows = ''.join(f"<tr><td><b>{E(cat)}</b></td><td class='n'>{E(cats.get(cat, '?'))}</td>" + ''.join(f"<td class='n'>{pertype.get((cat, d), 0) or ''}</td>" for d in DEPN) + f"<td class='n'>{tc[cat]}</td></tr>"
                for cat in sorted(tc, key=lambda c: -tc[c]))

state = '\n'.join(f'  <div class="st"><h4><span class="tag {io}">{"modelled" if io == "in" else "not modelled"}</span>{E(h)}</h4><p>{E(p)}</p></div>' for io, h, p in C['network_state'])
need = sum(b['need'] for L in order for b in BR[L])
added = R['added']
PROVTXT = (f"<b>Provisional roster.</b> {E(C['live']['provisional']['why'])} {len(OBS)} buses were on the sheet's lines at {hm(C['live']['provisional']['window'][0])}–{hm(C['live']['provisional']['window'][1])}. "
           f"The rest of each line's need is designed with real fleet numbers from the line's records, marked “designed, not recorded”. Everything is replaced by the buses observed at each line's afternoon peak today.")
if PROV and not OBS:   # published before the morning peak: every bus is designed until the feed shows the lines running
    PROVTXT = (f"<b>Provisional roster, before today's peaks.</b> The timetable, branches, needs and Simutrans schedules are complete. Every bus is designed for now: "
               f"a real bus with weekday records on its line (since {C['records']['since']}), covering the line's types, marked “designed, not recorded”. "
               f"The ODIS live map is being polled all day; the sheet is rebuilt with the buses seen in the morning peak, then with the buses seen at each line's afternoon peak.")
pending = f'<div class="pending">{PROVTXT}</div>' if PROV else ''
if PROV:
    rostertxt = (f"Until the afternoon is observed the roster is provisional: {len(OBS)} buses seen on their lines in the morning peak, plus {len(added)} designed buses with real fleet numbers. The need is {need}.")
else:
    rostertxt = (f"Each line's buses are those on it in its own window, {C['live']['half_window']} min either side of its peak anchor; a bus seen on several lines counts on the line whose anchor its sighting is nearest. "
                 f"That is {len(OBS)} buses, against a need of {need}. " + (f"{len(added)} buses are designed where a Simutrans line had fewer buses than it needs, each with the reason on its row: a free bus (not on any line at {hm(C['live']['busy_window'][0])}–{hm(C['live']['busy_window'][1])}) with weekday records on the line since {C['records']['since']}, covering the line's types first." if added else 'Every Simutrans line had at least its need in observed buses, so nothing is designed.'))

def bneed(L, p):
    nm = nm_for(L)
    b = next((b for b in BR[L] if {b['a'], b['b']} == {al(nm(p['fr'])), al(nm(p['to']))}), None)
    return (b['need'], b.get('alt_need')) if b else (None, None)
chk_rows = ''
for L, p, slots, band, al_ in CHECKS:
    nm = nm_for(L); bn = bneed(L, p)
    slower = (f"every {al_['every']} · Offset {al_['set'][0]} · up to {al_['approx']} min off" + (f" · {bn[1]} buses" if bn[1] else '')) if al_ and al_['every'] > p['every'] else '—'
    chk_rows += (f"<tr><td><a class='badge sm' href='#l{L}'>{E(L)}</a></td><td>{E(nm(p['fr']))} &rarr; {E(nm(p['to']))}</td><td class='n'>every {p['every']} · Offset {p['set'][0]} · up to {p['approx']} min off{(' · ' + str(bn[0]) + ' buses') if bn[0] else ''}</td>"
                 f"<td class='mono'>{', '.join(hm(x) for x in band) or '—'}</td><td class='n'>{slots} / {len(band)}</td><td>{slower}</td></tr>")
cchk = ''.join(f"<tr><td><a class='badge sm' href='#l{L}'>{E(L)}</a></td><td>{E(p['fr'])} &rarr; {E(p['to'])}</td><td class='n'>every {p['every']} · Offset {p['set'][0]} · stop {p['circuit_leg']} of a circuit</td><td class='n'>{p['_miss'][0]} of {p['_miss'][1]} slots on a real departure</td></tr>" for L, p in CCHECKS)
checks = (f'''<h2 id="checks">Approximate schedules to check ({len(CHECKS)})</h2>
<p class="sub">These rows have an irregular real timetable, so they get an even approximate pattern with the same rate at both ends of the line. Each has more slots in its fit window than real departures, so the extra slots would run empty or spread the buses thinner. Where a slower pattern exists, it is shown with its own worst deviation. If you pick it, switch both ends of that Simutrans line together. The rows are also marked on their line cards.</p>
<div class="types"><table class="tlist"><thead><tr><th>Line</th><th>Terminus entry</th><th class="n">Set now</th><th>Real departures in the window</th><th class="n">Slots / real</th><th>Slower option</th></tr></thead><tbody>{chk_rows}</tbody></table></div>'''
          + (f'<h3 style="margin-top:18px">Circuit legs off the timetable ({len(CCHECKS)})</h3><div class="types"><table class="tlist"><thead><tr><th>Line</th><th>Leg</th><th class="n">Set now</th><th class="n">On the timetable</th></tr></thead><tbody>{cchk}</tbody></table></div>' if CCHECKS else ''))

# ---- coverage (owner rule, 20 Oct 2026: "501 is the only line running to Dětmarovice, how can we not model that?")
COVD = R['covered']; UNC = R['uncovered']
hand = ''.join(f"<tr><td><a class='badge sm' href='#l{L}'>{E(L)}</a></td><td><b>{E(slname(L, bi))}</b></td><td>{E(brname(b))}</td><td>{'daily' if b['every'] == 1440 else 'every ' + str(b['every'])}</td><td class='n'>{b['need']}</td><td>{E(b['why'])}</td></tr>"
               for L in order for bi, b in enumerate(BR[L]) if b.get('override'))
stoprows = ''.join(f"<tr><td>{E(st)}</td><td>{E(', '.join(ls))}</td></tr>" for st, ls in sorted(COVD.items()))
nst = len({st for L_ in TRIPS for t in TRIPS[L_] if 780 <= t['dep'] < 1140 for st in [nm_for(L_)(x) for x in t['stops']]})
coverage = (f'''<h2 id="coverage">Coverage</h2>
<p class="sub">Every stop the sheet's lines serve between 13:00 and 19:00 must be on a Simutrans line. {('All ' + str(nst) + ' of them are.') if not UNC else str(len(UNC)) + ' stops are not: ' + E(', '.join(UNC))} Where the branch rule misses a place (a branch run a few times a day, a bus that rotates through several branches, a line split into halves of a ring), the line is set by hand, listed below with the real trips it carries. Each card also lists its afternoon trips that are not on one of its Simutrans lines, with the Simutrans lines that cover their stops.</p>
<div class="types"><table class="tlist"><thead><tr><th>Line</th><th>Simutrans line</th><th>Route</th><th>Timetable</th><th class="n">Buses</th><th>Why set by hand</th></tr></thead><tbody>{hand}</tbody></table></div>
<details class="nn" style="margin:10px 0 0"><summary>Every stop and the Simutrans lines that serve it ({len(COVD)})</summary><div class="types"><table class="tlist"><thead><tr><th>Stop</th><th>Simutrans lines</th></tr></thead><tbody>{stoprows}</tbody></table></div></details>''')

hrows = ''.join(f"<tr><td><a class='badge sm' href='#l{L}'>{E(L)}</a></td><td><b>{E(nm_)}</b>: {E(g['fr'])} &rarr; {E(g['to'])}</td><td class='n'>every {g['every']} · Offset {g['set'][0]}</td>"
                f"<td class='mono'>{', '.join(hm(x) for x in band) or '—'}</td><td>{', '.join(hm(x) for x in g.get('off') or []) or '—'}</td><td class='n'>{ns} / {len(band)}</td>"
                f"<td>{(f'every {a_[chr(101)+chr(118)+chr(101)+chr(114)+chr(121)]} · Offset {a_[chr(115)+chr(101)+chr(116)][0]} · up to {a_[chr(100)+chr(101)+chr(118)]} min off') if a_ else '—'}</td></tr>" for L, nm_, g, ns, band, a_ in HCHECKS)
if HCHECKS:
    checks += (f'''<h3 style="margin-top:18px">Hand-set rows to check ({len(HCHECKS)})</h3>
<p class="sub">Hand-set lines follow the regular run of their real departures. These legs have trips more than 3 min off that pattern, or more slots in their window than real departures. Where halving the frequency fits, the slower option is shown with its worst deviation; if you pick it, switch every leg of that Simutrans line together.</p>
<div class="types"><table class="tlist"><thead><tr><th>Line</th><th>Simutrans line and leg</th><th class="n">Set now</th><th>Real departures in the window</th><th>Off the pattern</th><th class="n">Slots / real</th><th>Slower option</th></tr></thead><tbody>{hrows}</tbody></table></div>''')
tpl = open(os.path.join(ROOT, 'templates', 'page.html'), encoding='utf-8').read()
rep = dict(COVERAGE=coverage, CHECKS=checks, TITLE=C['title'], VEHICLE_DAY_LABEL=C['vehicle_day_label'], VEHICLE_DAY_EN=C['vehicle_day_label_en'],
           STATE_LABEL=C['network_state_label'], STATE=state, BRANCHES_WHY=E(C['branches_why']), TOWNS=towns, TOWNNAV=townnav,
           DEPOTS=dsec, DEPNAV=DEPNAV, SPARE=spsec, SPAREHEAD=sparehead, PAKS=paks, TYPES=trows, NEED=str(need),
           NOBS=str(len(OBS)), NOBSLAB='seen this morning (provisional)' if PROV else 'seen live at their line’s peak', NLINES=str(len(order)), NSIM=str(sum(len(BR[L]) for L in order)),
           NAV=''.join(f"<a href='#l{L}' class='badge sm'>{L}</a>" for L in order), PAK_FILE_NOTE=f"pak repo main {C['pak']['commit']}",
           JDF_LABEL=C['jdf']['export_label'], NALL=str(len(CLS)), OFFPEAK=offpeak, PENDING=pending,
           DEPOT_SUB=E('Each branch lists the buses it sends to each line, with what the live feed showed, or why a bus is designed.'),
           PAKSCOPE='on the sheet', PAKCOL='Buses', ROSTERTXT=E(rostertxt))
for k, v in rep.items(): tpl = tpl.replace('{{' + k + '}}', v)
left = re.findall(r'\{\{[A-Z_0-9]+\}\}', tpl)
assert not left, left
out = os.path.join(PROJECT, C['output_html'])
open(out, 'w', encoding='utf-8').write(tpl)
# pak request: every type x paint shown as a substitute
req = ['# Pak request: Havířov / Karviná / Orlová bus sheet', '', f'From session simutrans-timetable-a4, {C["vehicle_day"]}. Buses on the sheet whose type and paint have no exact object in VZ-MHDHavirov/-Karvina/-Orlova-bus or VZ-ODIS-bus (pak main {C["pak"]["commit"]}).', '',
       '| Real type | Real paint | Fleet numbers | Shown now as |', '|---|---|---|---|']
for (t, pnt), ns in sorted(PAKREQ.items()):
    n0 = sorted(ns)[0]; L0 = next(L for L in order for u in roster[L] if n0 in u[1]) if any(n0 in u[1] for L in order for u in roster[L]) else order[0]
    req.append(f"| {t} | {pnt} | {', '.join(sorted(ns))} | {pak(n0, L0)['core']} ({pak(n0, L0)['reason']}) |")
if not PAKREQ: req = req[:4] + ['None: every bus on the sheet has an exact object.']
open(os.path.join(ROOT, 'pak_request.md'), 'w', encoding='utf-8').write('\n'.join(req) + '\n')
print('wrote', out, 'need', need, 'observed', len(OBS), 'mode', MODE, 'pak substitutes', len(PAKREQ))
