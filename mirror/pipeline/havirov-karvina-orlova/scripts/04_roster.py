"""trips + schedule + fleet + live -> derived/lines.json (variant tables) and roster.json (branches, needs, buses).

Same rules as the Ostrava bus sheet (pipeline/ostrava-bus/scripts/04_roster.py), with this sheet's data:
1. Lines: every line of the vehicle day with >= config.min_afternoon_trips trips in 13:00-19:00. Lines with fewer
   (Havířov 414, Orlová 503: one afternoon trip) are listed as "occasional trips only", not modelled.
2. Branches: lib.branch_pairs (peak rule + afternoon rule) around the line's anchor (05_schedule.py, peaks.json).
   Circular lines (circular.json: Karviná 511, 512, 516, 518, 519) are one branch, a = b.
3. Need: lib.pattern_need on the sheet's own schedule rows (user rule, 20 Oct 2026: size every line from the pattern the
   sheet suggests); a circular line is one row and one running time round the loop. Without a timed pattern at both
   ends, the turns the timetable chains at the anchor (at least 1). lib.circuitize where a circuit across branches saves
   a bus (or serves two paths).
4. Observed buses (live.json, ODIS live map): each line is observed in its own window, config.live.half_window either side
   of its anchor. A bus seen on several lines goes to the line whose anchor its sighting is nearest. Branch: the branch whose
   far terminus matches the trip's start or final stop, else the branch with the largest shortfall; then extras move to a
   short branch of the same line. Before the afternoon is observed, config.live.provisional (the morning peak) stands in.
5. Logged surplus: mark_spares (one of every type first, then the lowest courses); the rest are "not needed".
6. Designed buses where a branch is short: real buses from the line's weekday records since config.records.since, free
   (not seen on any line in config.live.busy_window), covering the line's roster types first, then by recency; then the
   line's main type from the line's town branch. Leftover free record buses are "not needed".
"""
import collections, math, re, unicodedata
from lib import (CONFIG, load, save, nm_for, hhmm, hm, min_turnaround, blocks, active_at, mark_spares, pattern_need,
                 branch_pairs, circuitize, path_variants, town_of, build_overrides, override_need)

C = CONFIG; AL = C['terminus_alias']
def al(x): return AL.get(x, x)
SCH = load('schedule.json'); PEAKS = load('peaks.json'); CIRC = load('circular.json')
trips = load('trips.json'); fleet = load('fleet.json'); LV = load('live.json'); LIVE = LV['cars']
TW = C['table_window']; DEPOTS = set(C['depot_stops'])
def T0_(L):
    ov = C.get('line_overrides', {}).get(L)
    if ov and ov.get('mode') == 'replace':   # a hand-set line is read in its own window (514: 15:00-19:00, not the automatic 13:30)
        w = ov['lines'][0].get('window', [900, 1080]); return C['peak_minute'] if w[0] <= C['peak_minute'] < w[1] else min(w[0] + 60, (w[0] + w[1]) // 2)
    return PEAKS.get(L, {}).get('anchor', C['peak_minute'])
def mins(s): return int(s[:2]) * 60 + int(s[3:5])

occasional = {L: sum(1 for t in tr if 780 <= t['dep'] < 1140) for L, tr in trips.items() if sum(1 for t in tr if 780 <= t['dep'] < 1140) < C['min_afternoon_trips']}
OV = C.get('line_overrides', {})
carried = {L: OV[L]['by'] for L in OV if OV[L].get('mode') == 'carried'}          # 520: the return leg of the 514 circuit
occasional = {L: n for L, n in occasional.items() if L not in OV}                   # a hand-set line is modelled however sparse
order = sorted([L for L in trips if L not in occasional and L not in carried], key=int)
def owner(L): return carried.get(L, L)

# ---- 1. variant tables (the hour before to the hour after the anchor)
lines = {}
for L in order:
    nm = nm_for(L); var = collections.defaultdict(list); dl = T0_(L) - C['peak_minute']
    for t in trips[L]:
        if TW[0] + dl <= t['dep'] < TW[1] + dl: var[(nm(t['fr']), nm(t['to']))].append(t)
    V = []
    for (a, b), ts in sorted(var.items(), key=lambda x: -len(x[1])):
        deps = sorted(t['dep'] for t in ts); gaps = [y - x for x, y in zip(deps, deps[1:])]
        seq = collections.Counter(tuple(nm(s) for s in t['stops']) for t in ts).most_common(1)[0][0]
        V.append(dict(fr=a, to=b, n=len(ts), hw=collections.Counter(gaps).most_common(1)[0][0] if gaps else None,
                      deps=[hhmm(d) for d in deps], min_peak_hour=sorted(set(d % 60 for d in deps if T0_(L) <= d < T0_(L) + 60)),
                      rt=round(sum(t['arr'] - t['dep'] for t in ts) / len(ts)), stops=list(seq)))
    lines[L] = dict(variants=V)
save('lines.json', lines)

# ---- 2 + 3. branches and needs
# stops only one line serves in 13:00-19:00: path_variants never merges them away as skipped stops (Ostrava rule via 0b)
_srv = collections.defaultdict(set)
for L_, ts_ in trips.items():
    for t in ts_:
        if 780 <= t['dep'] < 1140:
            for x in t['stops']: _srv[x].add(L_)
ONLY = {L_: tuple(x for x, ls in _srv.items() if ls == {L_}) for L_ in trips}
branches = {}
for L in order:
    nm = nm_for(L); T0 = T0_(L)
    tr = [dict(t, o=al(nm(t['fr'])), d=al(nm(t['to']))) for t in trips[L]]
    lay = {k: min(C['cycle_lay'], v) for k, v in min_turnaround(tr).items()}
    def rt_(x, y):
        r = [t['arr'] - t['dep'] for t in tr if t['o'] == x and t['d'] == y and T0 - 60 <= t['dep'] < T0 + 120] or [t['arr'] - t['dep'] for t in tr if t['o'] == x and t['d'] == y]
        return round(sum(r) / len(r)) if r else None
    def row(x, y): return next((p for p in SCH.get(L, []) if p.get('every') and al(nm(p['fr'])) == x and al(nm(p['to'])) == y), None)
    chosen, ranked = branch_pairs(tr, C, T0)
    brs = []
    if L in CIRC:
        X = CIRC[L]; p = row(X, X); rt = rt_(X, X)
        br = dict(a=X, b=X, circular=True, trips=sum(1 for t in tr if t['o'] == X and t['d'] == X and 900 <= t['dep'] < 1080), observed=0, surplus=0)
        if p and rt:
            n_, cyc_, w_ = pattern_need([p], [rt], [lay.get(X, C['cycle_lay'])], T0)
            br.update(need=n_, cycle=cyc_, how='pattern', waits=w_ + [0], runtimes=[rt, 0], pattern_every=p['every'], approx='approx' in p)
        else:
            br.update(need=max(1, len(active_at(blocks([t for t in tr if t['o'] == X and t['d'] == X]), T0))), cycle=None, how='turns')
        brs.append(br); chosen = [c for c in chosen if X not in c[0]]
    for p_, ts in chosen:
        cnt = collections.Counter(t['o'] for t in ts)
        a = max(p_, key=lambda x: (cnt[x], x)); b = next(x for x in p_ if x != a)
        br = dict(a=a, b=b, trips=len(ts), observed=0, surplus=0)
        pa, pb = row(a, b), row(b, a)
        if pa and pb and rt_(a, b) and rt_(b, a):
            rts = [rt_(a, b), rt_(b, a)]; lays = [lay.get(a, C['cycle_lay']), lay.get(b, C['cycle_lay'])]
            n_, cyc_, w_ = pattern_need([pa, pb], rts, lays, T0)
            br.update(need=n_, cycle=cyc_, how='pattern', waits=w_, runtimes=rts, pattern_every=pa['every'], approx='approx' in pa or 'approx' in pb)
            if pa.get('alt') and pb.get('alt'): br['alt_need'] = pattern_need([pa['alt'], pb['alt']], rts, lays, T0)[0]
        else:
            br.update(need=max(1, len(active_at(blocks([t for t in tr if {t['o'], t['d']} == set(p_)]), T0))), cycle=None, how='turns')
        brs.append(br)
    if L not in CIRC:
        circ = circuitize(brs, SCH.get(L, []), tr, lay, T0, al, paths=path_variants(tr, T0, al, keep_stops=ONLY.get(L, ())))
        if circ:
            print('circuit', L, [(c['b'], c['need'], c['cycle']) for c in circ], 'separate', circ[0]['sep_need']); brs = circ
    mode, sls = build_overrides(L, trips)
    if sls:      # hand-set Simutrans lines (coverage rule): replace the automatic branches, or add to them
        obrs = []
        for sl in sls:
            t0 = sl['window'][0] + 30 if sl['every'] < 1440 else sl['window'][0]
            n_, cyc_, w_ = override_need(sl, t0)
            ends = list(dict.fromkeys(x for g in sl['legs'] for x in (g['fr'], g['to'])))
            obrs.append(dict(a=ends[0], b=' → '.join(ends[1:]) if len(ends) > 2 else ends[-1], name=sl['name'], override=True, how='override', legs=sl['legs'],
                             every=sl['every'], window=sl['window'], fitwin=sl['fitwin'], why=sl['why'], need=n_, cycle=cyc_, waits=w_, ends=ends, trips=0, observed=0, surplus=0))
        brs = obrs if mode == 'replace' else brs + obrs
    others = [dict(pair=sorted(p_), trips=len(ts)) for p_, ts in ranked if all(p_ != frozenset((b['a'], b['b'])) for b in brs) and len(p_) == 2]
    branches[L] = dict(branches=brs, others=others)

# ---- 4. observed buses
PEAKMODE = any(C['live']['busy_window'][0] <= mins(r[0]) <= C['live']['busy_window'][1] for rs in LIVE.values() for r in rs)
MODE = 'peak' if PEAKMODE else 'provisional'
HW = C['live']['half_window']; PW = C['live']['provisional']['window']
def key(s):
    s = unicodedata.normalize('NFKD', s or '').encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]', '', s)
def win(L): return (T0_(L) - HW, T0_(L) + HW) if MODE == 'peak' else tuple(PW)
def bwins(L, b):
    """where and when a Simutrans line is observed: automatic branches in the line's window; hand-set ones in their own
    window (daily timetables: each departure until arrival), so the midday 402B or the evening 417B get their own buses"""
    if MODE != 'peak' or not b.get('override'): return [win(L)]
    if b['every'] == 1440: return [(d - 5, d + g['rt']) for g in b['legs'] for d in g['real']]
    # each slot departure in the line's window, until it arrives (501B's only afternoon run leaves Lazy 17:06, 409 starts 16:46)
    w = b['window']
    return [(t - 5, t + g['rt']) for g in b['legs'] if not g['untimed'] for t in range(w[0], w[1]) if t % g['every'] in g['real']]
def ends_of(b): return b.get('ends') or ([b['a']] if b.get('circular') else [b['a'], b['b']])
def path_keys(b):   # every stop on a hand-set line's route: its real trips are often split at a core point (501 at Lutyně)
    return {key(x) for g in b.get('legs', []) for x in g.get('stops', [])} | {key(e) for e in ends_of(b)}
# every place a bus was seen that fits a Simutrans line: (distance to the line's slot or anchor, line, branch, sighting)
cands = collections.defaultdict(dict)
for n, rs in LIVE.items():
    if n not in fleet: continue
    for r in rs:
        L = owner(r[1])
        if L not in branches: continue
        t = mins(r[0]); nm = nm_for(L); tn = town_of(L)['name'] + ','
        ks = {key(al(nm(r[3].replace(tn, '')))), key(al(nm(r[4].replace(tn, ''))))}   # with the terminus alias (Podlesí, Těšínská)
        for bi, b in enumerate(branches[L]['branches']):
            if b.get('override'):
                # a hand-set line takes a bus whose trip runs along its route (both ends on it: 417 and 417C share Těrlicko,
                # but Šumbark is not on 417C), anywhere in its window, nearest its slot
                pk = path_keys(b)
                if not (ks and all(k and any(k == x or (len(k) > 6 and (k in x or x in k)) for x in pk) for k in ks)): continue
                if MODE == 'peak':
                    if not b['window'][0] - 30 <= t <= b['window'][1] + 30: continue
                    d = min((abs(t - (w[0] + w[1]) // 2) for w in bwins(L, b)), default=60)
                else:
                    w = win(L)
                    if not w[0] <= t <= w[1]: continue
                    d = 0
            else:
                hit = any(k and (key(e) in k or k in key(e)) for k in ks for e in ends_of(b)[1:] or ends_of(b))
                both = bool(ks) and all(k and any(key(e) in k or k in key(e) for e in ends_of(b)) for k in ks)   # 410: Podlesí vs Šumbark
                ws = [w for w in bwins(L, b) if w[0] <= t <= w[1]]
                if not ws: continue
                d = (0 if both else 10 if hit else 30) + (abs(t - (ws[0][0] + ws[0][1]) // 2) if MODE == 'peak' else 0)
            k_ = (L, bi)
            if k_ not in cands[n] or d < cands[n][k_][0]: cands[n][k_] = (d, r)
# The buses swap lines all afternoon (Havířov 401/406/413/403/417/402; Karviná's circulars), so each bus goes to one
# Simutrans line it was seen on, chosen to fill as many line needs as possible (augmenting paths over the branches' needs),
# trying for each bus its closest candidates first. Buses left over are "not needed" on their closest line.
need_of = {(L, bi): b['need'] for L in branches for bi, b in enumerate(branches[L]['branches'])}
holders = collections.defaultdict(list); assign = {}
def try_assign(n, seen_):
    for k_ in sorted(cands[n], key=lambda k_: cands[n][k_][0]):
        if k_ in seen_: continue
        seen_.add(k_)
        if len(holders[k_]) < need_of[k_]:
            holders[k_].append(n); assign[n] = k_; return True
        for m in sorted(holders[k_], key=lambda m: -cands[m][k_][0]):   # move a holder that can go elsewhere
            if try_assign_from(m, seen_):
                holders[k_].remove(m); holders[k_].append(n); assign[n] = k_; return True
    return False
def try_assign_from(m, seen_):
    old = assign.get(m)
    for k_ in sorted(cands[m], key=lambda k_: cands[m][k_][0]):
        if k_ == old or k_ in seen_: continue
        seen_.add(k_)
        if len(holders[k_]) < need_of[k_]:
            holders[k_].append(m); assign[m] = k_; return True
    return False
for n in sorted(cands, key=lambda n: min(v[0] for v in cands[n].values())):
    try_assign(n, set())
obs = {}; obs_br = {}; leftover = {}
for n in cands:
    k_ = assign.get(n) or min(cands[n], key=lambda k_: cands[n][k_][0])
    d, r = cands[n][k_]
    obs[n] = dict(line=k_[0], real_line=r[1], course=r[2], first=r[0], fr=r[3], to=r[4], depot=r[5], dist=d)
    obs_br[n] = k_[1]
    if n not in assign: leftover[n] = k_
FLAG = '' if MODE == 'peak' else 'morning'
roster = {L: [] for L in order}
for n, o in sorted(obs.items()):
    if n not in leftover: roster[o['line']].append([fleet[n]['cat'], [n], FLAG, obs_br[n], o['course']])
moved = []

# ---- 5. logged surplus: buses seen that no line still needed after the assignment (one bus, one Simutrans line)
surplus = {}
for n, (L, bi) in sorted(leftover.items()):
    surplus.setdefault(L, []).append([fleet[n]['cat'], [n], FLAG, bi, obs[n]['course']])

# ---- 6. designed buses and spare record buses
H = load('history.json')
aff = collections.defaultdict(collections.Counter); last = {}
for L, n, d, note in H:
    aff[n][L] += 1; last[(n, L)] = max(last.get((n, L), ''), d)
BW = C['live']['busy_window']
busy = {n for n, rs in LIVE.items() if any(BW[0] <= mins(r[0]) <= BW[1] for r in rs)}
def active(n): return n in fleet and fleet[n]['state'] == 'zar' and fleet[n]['cat'] != '?'
used = {n for us in list(roster.values()) + list(surplus.values()) for u in us for n in u[1]}
def free(n): return active(n) and n not in used and n not in busy and n not in obs
REGIONAL = C['regional_paints']
def townbus(n): return not any(k in fleet[n].get('paint', '') for k in REGIONAL)
def town_home(n):
    """the branch a bus belongs to: where the live feed saw it that day, else the town of the lines it has most records on"""
    for r in LIVE.get(n, []): return r[5]
    c = collections.Counter()
    for L_, k in aff[n].items(): c[town_of(L_)['name']] += k
    return c.most_common(1)[0][0] if c else None
added = []; spares = {}
for L, B in sorted(branches.items(), key=lambda x: -sum(b['need'] for b in x[1]['branches'])):
    short = [(i, max(0, b['need'] - sum(1 for u in roster[L] if u[3] == i))) for i, b in enumerate(B['branches'])]
    slots = [i for i, k in short for _ in range(k)]
    hist_cars = [n for n in aff if aff[n][L] and active(n)]
    def bw(i):   # when a designed bus must be free: the Simutrans line's own windows (402B at midday, 417B in the evening), else the peak
        b = B['branches'][i]
        return bwins(L, b) if (b.get('override') and MODE == 'peak') else [tuple(BW)]
    def free_in(n, i): return active(n) and n not in used and n not in obs and not any(w[0] <= mins(r[0]) <= w[1] for r in LIVE.get(n, []) for w in bw(i))
    rtypes = collections.Counter()
    for n in hist_cars: rtypes[fleet[n]['cat']] += aff[n][L]
    for u in roster[L]: rtypes[u[0]] += 1
    picks = []
    for slot_i in slots:
        have = {fleet[u[1][0]]['cat'] for u in roster[L]} | {fleet[n]['cat'] for n, _w in picks}
        pool = [n for n in hist_cars if free_in(n, slot_i) and n not in [p for p, _w in picks]]
        # town fleet first: regional buses (kraj or ODIS paint) in a line's records stood in for a day; they design only when no town bus is left
        pool = [n for n in pool if townbus(n)] or pool
        lack = [t for t, _c in rtypes.most_common() if t not in have and any(fleet[n]['cat'] == t for n in pool)]
        if lack: cand = [n for n in pool if fleet[n]['cat'] == lack[0]]; why = f'covers the {fleet[cand[0]]["full"]} type of the line roster; '
        else: cand = pool; why = ''
        cand.sort(key=lambda n: (last[(n, L)], aff[n][L]), reverse=True)
        if cand:
            n = cand[0]; why += f"{aff[n][L]} weekday records on line {L} since {C['records']['since']}, last {last[(n, L)]}"
        else:
            tn = town_of(L)['name']
            mt = collections.Counter(u[0] for u in roster[L]) + rtypes
            mt = mt.most_common(1)[0][0] if mt else None
            cand = sorted([n for n in fleet if free_in(n, slot_i) and n not in [p for p, _w in picks] and town_home(n) == tn],
                          key=lambda n: (not townbus(n), -(10 if fleet[n]['cat'] == mt else 0), n))
            if not cand: print('no free bus for', L); break
            n = cand[0]; why = f"no free bus with records on line {L}; {'the line’s main type' if fleet[n]['cat'] == mt else 'a free bus'} from the {tn} branch"
        picks.append((n, why)); used.add(n)
    for i, (n, why) in zip(slots, picks):
        roster[L].append([fleet[n]['cat'], [n], 'designed', i, None])
        added.append(dict(line=L, branch=i, car=n, why=why + f"; not on any line at " + ', '.join(f'{hm(a)}–{hm(b)}' for a, b in bw(i)) + f" in the live feed on {LV['day']}"))
    spares[L] = [dict(car=n, last=last[(n, L)], records=aff[n][L]) for n in sorted(hist_cars, key=lambda n: last[(n, L)], reverse=True) if free(n) and townbus(n)]
for L, B in branches.items():
    for i, b in enumerate(B['branches']):
        b['observed'] = sum(1 for u in roster[L] if u[3] == i and u[2] != 'designed')
        b['surplus'] = sum(1 for u in surplus.get(L, []) if u[3] == i)
        b['assigned'] = sum(1 for u in roster[L] if u[3] == i)
# ---- 7. coverage (owner rule, 20 Oct 2026): every stop the sheet's lines serve in 13:00-19:00 is on a modelled
# Simutrans line, or listed with the reason. A trip is "on" a Simutrans line when its termini are that line's pair (automatic
# branches, circuit legs) or a hand-set leg's termini (or its departure is one the leg carries); a stop is covered when a trip
# on a Simutrans line passes it.
def names_line(src, L): return re.search(r'\b' + L + r'\b', src) is not None
def sl_name(L, bi):
    b = branches[L]['branches'][bi]
    if b.get('name'): return b['name']
    auto = [i for i, x in enumerate(branches[L]['branches']) if not x.get('name')]
    return f"{L}{'ABCDEF'[auto.index(bi)]}" if len(auto) > 1 else L
on = {}; covered = collections.defaultdict(set)
for L in list(trips):
    LL = owner(L)
    if LL not in branches: continue
    nm = nm_for(L)
    for t in trips[L]:
        o, d = al(nm(t['fr'])), al(nm(t['to'])); hit = None
        cands = [(LL, bi, b) for bi, b in enumerate(branches[LL]['branches'])] + [(L2, bi, b) for L2 in branches if L2 != LL for bi, b in enumerate(branches[L2]['branches']) if b.get('override')]
        for L2, bi, b in cands:
            if b.get('override'):
                ok = any((L in g['lines'] and ((g['fr'] == o and g['to'] == d) or (o in g['stops'] and d in g['stops'] and g['stops'].index(o) < g['stops'].index(d)))) or (names_line(g['src'], L) and hm(t['dep']) in g['src']) for g in b['legs'])
            else: ok = {o, d} == {b['a'], b['b']} or (b.get('circular') and o == d == b['a']) or any({o, d} == {g['X'], g['Y']} for g in b.get('legs', []))
            if ok: hit = (L2, bi); break
        on[(L, t['sp'])] = hit
        if hit is not None: covered.update({nm(x): covered[nm(x)] | {sl_name(*hit)} for x in t['stops']})
    for bi, b in enumerate(branches[LL]['branches']):
        for g in b.get('legs', []):
            for x in g.get('stops', []): covered[x].add(sl_name(LL, bi))
unmodelled = {}; uncovered = {}
for L in list(trips):
    nm = nm_for(L); LL = owner(L)
    rows_ = []
    for t in sorted(trips[L], key=lambda t: t['dep']):
        if not 780 <= t['dep'] < 1140 or on.get((L, t['sp'])) is not None: continue
        miss = [nm(x) for x in t['stops'] if not covered.get(nm(x))]
        rows_.append(dict(dep=hm(t['dep']), fr=nm(t['fr']), to=nm(t['to']), miss=miss))
        for x in miss: uncovered.setdefault(x, []).append(f"{L} {hm(t['dep'])}")
    if rows_: unmodelled[L] = rows_
print('uncovered stops', len(uncovered), dict(list(uncovered.items())[:6]))
save('roster.json', dict(anchors={L: T0_(L) for L in order}, order=order, occasional=occasional, carried=carried, unmodelled=unmodelled, uncovered=uncovered, covered={k: sorted(v) for k, v in covered.items()}, moved=moved, surplus=surplus, spares=spares, mode=MODE, live_day=LV['day'],
                         observed=obs, roster=roster, branches=branches, added=added, live_files=LV['files'],
                         windows={L: list(win(L)) for L in order}))
need = sum(b['need'] for B in branches.values() for b in B['branches'])
print('mode', MODE, 'lines', len(branches), 'simutrans lines', sum(len(B['branches']) for B in branches.values()), 'need', need,
      'observed', len(obs), 'designed', len(added), 'not needed', sum(len(v) for v in surplus.values()), 'occasional', occasional)
for L in order:
    print(L, [(b['a'][:16], b['b'][:16], b['need'], b['how'][:5], b['observed']) for b in branches[L]['branches']])
