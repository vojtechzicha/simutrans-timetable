"""ODIS lines of other operators at the hub (config.odis; owner, 20 Oct 2026) -> derived/odis.json, rendered by 06_render.py
as the last section of the sheet in the same style as the DPO lines.

Same rules as the DPO lines:
1. Lines: every non-DPO line in the national JDF with a stop at the hub (01c_fetch_odis.py --scan); the version valid on
   the vehicle day by the shared version rule; trips of the whole line, not only those via the hub.
2. Branches: the bus branch rule (config.branch_rule) on unordered terminus pairs.
3. Schedule: the shared fit (plans: both ends at the same rate, approximate rows flagged).
4. Need: pattern_need on the suggested schedule; where a branch has no timed pattern at both ends, the turns the
   timetable chains at 16:00 (at least 1).
5. Vehicles: no record of these lines exists for the vehicle day (seznam-autobusu holds mostly weekend and holiday records
   for them), so every bus is designed: real buses from the line's own records, active in the register, covering the
   line's types by share and then by recency, one bus on one line only.
"""
import collections, csv, glob, io, json, math, os, re, zipfile
from lib import (CONFIG, RAW, load, save, make_nm, hm, jdf_open, pick_version, jdf_tables, jdf_trips, day, plans,
                 min_turnaround, blocks, active_at, pattern_need, parse_fleet_list, record_date, branch_pairs, line_anchor, interleave, circuitize, path_variants, simplify_rows, slot_need, hand_lines, mark_spares)

C = CONFIG; O = C['odis']; OUT = os.path.join(os.path.dirname(RAW), O['snapshot'], 'odis')
nm0 = make_nm(C); AL = C['terminus_alias']
def nm(s): n = nm0(s); return AL.get(n, n)
d = day(C['vehicle_day']); BRW = C['branch_rule']; F = C['fit']
DEPOTS = set(C['depot_stops'])

vers = json.load(open(os.path.join(OUT, 'lines.json'), encoding='utf-8'))
recs = json.load(open(os.path.join(OUT, 'records.json'), encoding='utf-8'))['lines']
reg = {}
for f in sorted(glob.glob(os.path.join(OUT, 'fleet_*_p*.html'))):
    for vid, v in parse_fleet_list(open(f, encoding='utf-8').read()).items(): reg[str(vid)] = v
TY = O['types']                                   # real type -> [length, pak object key of the nearest DPO object]

outer = jdf_open(os.path.join(RAW, 'JDF.zip'))
codes = sorted({v['line'] for v in vers})
lines, sched, branches, roster, fleet, added, meta, trips_out, peaks = {}, {}, {}, {}, {}, [], {}, {}, {}
usedv = set(); HIST, SHARE, OPN = {}, {}, {}
_srv = collections.defaultdict(set)   # stops only one line serves in 13:00-19:00 (path_variants keep_stops)
for L_, tr_ in load('trips.json').items():
    for t in tr_:
        if 780 <= t['dep'] < 1140:
            for s_ in t['stops']: _srv[nm0(s_)].add(L_)
_odt = {}
for code in sorted({v['line'] for v in vers}):
    v_ = pick_version([x for x in vers if x['line'] == code], d)
    if v_:
        _odt[code[-3:]] = jdf_trips(jdf_tables(outer, v_['inner']), d)
        for t in _odt[code[-3:]]:
            if 780 <= t['dep'] < 1140:
                for s_ in t['stops']: _srv[nm0(s_)].add(code[-3:])
def own_stops(L, tr): return {s_ for t in tr for s_ in t['stops'] if _srv.get(nm0(s_)) == {L}}
for code in codes:
    L = code[-3:]
    v = pick_version([x for x in vers if x['line'] == code], d)
    if not v: continue
    tr = [dict(t, o=nm(t['fr']), d=nm(t['to'])) for t in jdf_trips(jdf_tables(outer, v['inner']), d)]
    if not any(780 <= t['dep'] < 1140 for t in tr): continue
    op = C['odis']['carriers'].get(v['ic'], {}).get('name', v['ic'])
    meta[L] = dict(code=code, name=v['name'], operator=op, version=f"{v['valid_from']} – {v['valid_to']}", inner=v['inner'],
                   diversion_versions=sum(1 for x in vers if x['line'] == code and x['diversion'] and x['valid_from'] <= C['vehicle_day'] <= x['valid_to']))
    peaks[L] = A = line_anchor(tr, C); T0 = A['anchor']; dl = T0 - C['peak_minute']
    FL = dict(F, window=[x + dl for x in F['window']], core=[x + dl for x in F['core']])
    # timetable table, the hour before to the hour after the anchor, as the DPO cards
    var = collections.defaultdict(list)
    for t in tr:
        if T0 - 60 <= t['dep'] < T0 + 60: var[(t['o'], t['d'])].append(t)
    V = []
    for (a, b), ts in sorted(var.items(), key=lambda x: -len(x[1])):
        deps = sorted(t['dep'] for t in ts); gaps = [y - x for x, y in zip(deps, deps[1:])]
        seq = collections.Counter(tuple(nm0(s) for s in t['stops']) for t in ts).most_common(1)[0][0]
        V.append(dict(fr=a, to=b, n=len(ts), hw=collections.Counter(gaps).most_common(1)[0][0] if gaps else None,
                      min_peak_hour=sorted(set(x % 60 for x in deps if T0 <= x < T0 + 60)), rt=round(sum(t['arr'] - t['dep'] for t in ts) / len(ts)), stops=list(seq)))
    lines[L] = dict(variants=V)
    trips_out[L] = [dict(fr=t['fr'], to=t['to'], dep=t['dep'], arr=t['arr'], stops=t['stops']) for t in tr]
    # schedule (shared fit) and branches (bus branch rule)
    chosen, ranked = branch_pairs(tr, C, T0)
    KEEP = {p_ for p_, _ in chosen}
    nma = lambda s: AL.get(nm0(s), nm0(s))   # aliased termini so both ends pair up (as 05_schedule; 441 Havířov loop)
    sched[L] = plans([dict(t, fr=t['fr'], to=t['to']) for t in tr], nma, FL, DEPOTS, loop=C['all_termini_are_loops'], peak=T0,
                     keep=lambda a, b: frozenset((AL.get(a, a), AL.get(b, b))) in KEEP)
    for r_ in sched[L]:
        ts_ = [t for t in tr if nma(t['fr']) == r_['fr'] and nma(t['to']) == r_['to']]
        if ts_:
            r_['fr'] = collections.Counter(nm0(t['fr']) for t in ts_).most_common(1)[0][0]
            r_['to'] = collections.Counter(nm0(t['to']) for t in ts_).most_common(1)[0][0]
    for r_ in sched[L]: r_['_o'], r_['_d'] = AL.get(r_['fr'], r_['fr']), AL.get(r_['to'], r_['to'])
    interleave(sched[L], tr, chosen, loop=C['all_termini_are_loops'], peak=T0)
    for r_ in sched[L]: r_.pop('_o', None); r_.pop('_d', None)
    simplify_rows(sched[L], C['all_termini_are_loops'])
    lay = {k: min(C['cycle_lay'], x) for k, x in min_turnaround(tr).items()}
    brs = []
    for p, ts in chosen:
        cnt = collections.Counter(t['o'] for t in ts)
        a = max(p, key=lambda x: (cnt[x], x)); b = next(x for x in p if x != a)
        pa = next((q for q in sched[L] if q.get('every') and nm(q['fr']) == a and nm(q['to']) == b), None)
        pb = next((q for q in sched[L] if q.get('every') and nm(q['fr']) == b and nm(q['to']) == a), None)
        br = dict(a=a, b=b, trips=len(ts), min_runtime=None, observed=0, surplus=0)
        cnt = cnt or collections.Counter(t['o'] for t in tr if {t['o'], t['d']} == set(p))
        if pa and pb:
            def rt_(x, y):
                r = [t['arr'] - t['dep'] for t in tr if t['o'] == x and t['d'] == y and T0 - 60 <= t['dep'] < T0 + 120] or [t['arr'] - t['dep'] for t in tr if t['o'] == x and t['d'] == y]
                return round(sum(r) / len(r))
            rts = [rt_(a, b), rt_(b, a)]; lays = [lay.get(a, C['cycle_lay']), lay.get(b, C['cycle_lay'])]
            n_, cyc_, w_ = pattern_need([pa, pb], rts, lays, T0)
            br.update(need=n_, cycle=cyc_, how='pattern', waits=w_, runtimes=rts, pattern_every=pa['every'], approx='approx' in pa or 'approx' in pb)
            if pa.get('alt') and pb.get('alt'): br['alt_need'] = pattern_need([pa['alt'], pb['alt']], rts, lays, T0)[0]
        else:
            act = len(active_at(blocks([t for t in tr if {t['o'], t['d']} == set(p)]), T0))
            br.update(need=max(1, act), cycle=None, how='turns at 16:00')
        brs.append(br)
    circ = circuitize(brs, sched[L], tr, lay, T0, lambda x: AL.get(x, x), paths=path_variants(tr, T0, lambda x: AL.get(x, x), own_stops(L, tr)))
    if circ:
        print('circuit', L, [(c['b'], c['need'], c['cycle']) for c in circ], 'separate', circ[0]['sep_need']); brs = circ
    if L in C.get('hand_lines', {}):   # hand-set Simutrans lines (bus schedule method; config.hand_lines_rule)
        brs = hand_lines(C['hand_lines'][L], L, T0, _odt, nm, C)
        print('hand-set', L, [(b['name'], b['need'], b['waits']) for b in brs])
    branches[L] = dict(branches=brs, others=[dict(pair=sorted(p), trips=len(ts)) for p, ts in ranked if all(p != q for q, _ in chosen) and len(p) == 2])
    # the line's records, for designed buses (after the observed pass below)
    hist = collections.defaultdict(lambda: dict(n=0, last=None, plate=''))
    for r in recs.get(L, []):
        vid = r.get('vid'); dt = record_date(r['date'])
        if not vid or vid not in reg or reg[vid]['state'] != 'zar' or not dt: continue
        h = hist[vid]; h['n'] += 1; h['plate'] = r['car']
        if not h['last'] or dt > h['last']: h['last'] = dt
    share = collections.Counter()
    for vid, h in hist.items(): share[reg[vid]['type']] += h['n']
    HIST[L], SHARE[L], OPN[L] = hist, share, op

# ---- vehicles. 1. Buses seen on the ODIS live map at the line's peak (config.odis.live; owner, 20 Oct 2026: "yes - and ask
# it to capture ALL LINES in Odis"). The feed's trip number is the JDF trip number, so each bus at the anchor gives the exact
# trip: it goes to the Simutrans line whose slot that trip runs (a leg's out_lines/back_lines, its slot ±3 min mod the
# period), on whichever card that line is (the 442/441 circuit takes 441 buses). Buses of a card's lines that match no slot
# fill the branch with the largest shortfall, the card's own line first. Cards at 16:00 go first, then the others (534 at
# 14:40), and a bus is on one card only. Beyond a branch's need: one of each type kept, then the lowest trip numbers.
# 2. Designed buses for the rest, as before, from the line's records, not seen on the live map that afternoon.
def mkfleet(vid, plate, op):
    v = reg[vid]; num = v['num']
    area = re.search(r'provozní oblast[i]? ([^\xa0*{]*)', v['note']); paint = re.search(r'nátěr:\s*([^*{]*)', v['note'])
    fleet[num] = dict(state='odis', num=num, full=v['type'], type=v['type'], cat=v['type'], depot=op, depot_code='OD', plate=plate, vid=vid,
                      area=area.group(1).strip() if area else '', paint=paint.group(1).strip() if paint else '', note=v['note'],
                      len=TY.get(v['type'], ['?'])[0])
    return num
LVc = O.get('live'); observed = {}; surplus = {}; seen_any = set(); ROOT_ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for L in branches: roster[L] = []
if LVc and os.path.exists(os.path.join(ROOT_, LVc['out'])):
    LP = json.load(open(os.path.join(ROOT_, LVc['out']), encoding='utf-8'))['plates']
    byplate = {re.sub(r'\s', '', v['plate']).upper(): v for v in json.load(open(os.path.join(ROOT_, LVc['fleet']), encoding='utf-8')).values() if v.get('plate')}
    tripof = {(L_, t['sp']): t for L_, ts in _odt.items() for t in ts}
    seen_any = {str(byplate[pl]['vid']) for pl in LP if pl in byplate}
    def at(pl, T0):   # the sighting at the anchor, else the nearest one in the window
        w0, w1 = T0 + LVc['window'][0], T0 + LVc['window'][1]
        rows = [r for r in LP[pl] if r[0] <= w1 and r[1] >= w0 and (r[2], r[3]) in tripof]
        return min(rows, key=lambda r: 0 if r[0] <= T0 <= r[1] else min(abs(r[0] - T0), abs(r[1] - T0))) if rows else None
    def slot_of(L, b, line, t):
        P = b.get('period') or 60
        for g in b.get('legs', []):
            for X, Y, lns, sl in ((g['X'], g['Y'], g.get('out_lines') or [L], g['out_slot']), (g['Y'], g['X'], g.get('back_lines') or [L], g['back_slot'])):
                if sl is not None and line in lns and nm(t['fr']) == X and nm(t['to']) == Y and min((t['dep'] - sl) % P, (sl - t['dep']) % P) <= 3: return True
        return False
    def feeds(L): return [L] + sorted({x for b in branches[L]['branches'] for g in b.get('legs', []) for x in (g.get('out_lines') or []) + (g.get('back_lines') or [])} - {L})
    used = set(); claim = collections.defaultdict(list)   # (L, bi) -> [(plate, row)]
    ANC = {L: LVc['anchor'].get(L, peaks[L]['anchor']) for L in branches}
    for T0 in sorted(set(ANC.values()), key=lambda x: abs(x - C['peak_minute'])):
        grp = sorted((L for L in branches if ANC[L] == T0), key=int)
        now = {pl: at(pl, T0) for pl in LP if pl in byplate and str(byplate[pl]['vid']) in reg}
        now = {pl: r for pl, r in now.items() if r}
        slotted = set()
        for L in grp:
            for bi, b in enumerate(branches[L]['branches']):
                for pl, r in sorted(now.items()):
                    if pl not in used and slot_of(L, b, r[2], tripof[(r[2], r[3])]): claim[(L, bi)].append((pl, r)); used.add(pl); slotted.add(pl)
        for pl, r in now.items():   # a bus that runs a slot of any card at this hour is not used to fill another card
            if any(slot_of(L, b, r[2], tripof[(r[2], r[3])]) for L in grp for b in branches[L]['branches']): slotted.add(pl)
        for L in grp:
            for ln in feeds(L):
                for pl, r in sorted(now.items(), key=lambda x: x[1][3]):
                    if pl in used or pl in slotted or r[2] != ln: continue
                    k, nbi = max((b['need'] - len(claim[(L, bi)]), -bi) for bi, b in enumerate(branches[L]['branches']))
                    if k <= 0 and ln != L: continue
                    claim[(L, -nbi)].append((pl, r)); used.add(pl)
    for (L, bi), cl in sorted(claim.items()):
        b = branches[L]['branches'][bi]
        units = [dict(type=reg[str(byplate[pl]['vid'])]['type'], kurz=r[3], u=(pl, r)) for pl, r in cl]
        mark_spares(units, b['need'])
        for x in units:
            pl, r = x['u']; t = tripof[(r[2], r[3])]; vid = str(byplate[pl]['vid'])
            num = mkfleet(vid, byplate[pl]['plate'], OPN[L])
            observed[num] = dict(line=L, branch=bi, plate=byplate[pl]['plate'], real_line=r[2], trip=r[3], dep=hm(t['dep']), fr=nm0(t['fr']), to=nm0(t['to']),
                                 seen=hm(max(r[0], ANC[L] + LVc['window'][0])), anchor=hm(ANC[L]), spare=bool(x.get('spare')))
            (surplus.setdefault(L, []) if x.get('spare') else roster[L]).append([reg[vid]['type'], [num], '', bi, r[3]])
    usedv.update(str(byplate[pl]['vid']) for pl in used)
for L in branches:
    brs = branches[L]['branches']; hist, share, op = HIST[L], SHARE[L], OPN[L]
    slots = [bi for bi, b in enumerate(brs) for _ in range(max(0, b['need'] - sum(1 for u in roster[L] if u[3] == bi)))]
    need = len(slots); picks = []
    while len(picks) < need:
        pool = [vid for vid in hist if vid not in usedv and vid not in picks and vid not in seen_any]
        if not pool:   # no further bus with records on the line: the line's main type from its operating area
            mt = share.most_common(1)[0][0] if share else None
            areas = collections.Counter((re.search(r'provozní oblast ([^ *{]*)', reg[x]['note']) or [None, ''])[1].strip() for x in hist)
            ar = areas.most_common(1)[0][0] if areas else ''
            extra = sorted([x for x in reg if reg[x]['state'] == 'zar' and reg[x]['type'] == mt and x not in usedv and x not in picks and x not in seen_any and ar in reg[x]['note']], key=lambda x: reg[x]['num'])
            if not extra: break
            hist[extra[0]] = dict(n=0, last=None, plate='', why=f"no further bus with records on line {L}; the line's main type ({mt}) from its operating area ({ar})")
            picks.append(extra[0]); continue
        have = collections.Counter(reg[x]['type'] for x in picks) + collections.Counter(u[0] for u in roster[L])
        tot = sum(b['need'] for b in brs)
        lack = [t for t, c in share.most_common() if have[t] < max(1, round(tot * c / sum(share.values()))) and any(reg[x]['type'] == t for x in pool)]
        cand = [x for x in pool if not lack or reg[x]['type'] == lack[0]]
        cand.sort(key=lambda x: (hist[x]['last'], hist[x]['n']), reverse=True)
        picks.append(cand[0])
    usedv.update(picks)
    nots = f"not seen on the ODIS live map at the line's peak on {LVc['label']}; " if LVc else ''
    for bi, vid in zip(slots, picks):
        num = mkfleet(vid, hist[vid]['plate'], op)
        roster[L].append([reg[vid]['type'], [num], 'designed', bi, None])
        added.append(dict(line=L, branch=bi, car=num, why=nots + (hist[vid].get('why') or f"{hist[vid]['n']} records on line {L} at seznam-autobusu, last {hist[vid]['last'].isoformat()} (plate {hist[vid]['plate']})")))
    for bi, b in enumerate(brs):
        b['assigned'] = sum(1 for u in roster[L] if u[3] == bi); b['observed'] = sum(1 for u in roster[L] if u[3] == bi and u[2] != 'designed')
        b['surplus'] = sum(1 for u in surplus.get(L, []) if u[3] == bi)
    print(L, meta[L]['name'][:40], [(b['a'][:14], b['b'][:14], b['need'], b['how'][:7], b['observed']) for b in brs], 'buses', [(u[1][0], u[2] or 'seen') for u in roster[L]])
save('odis.json', dict(order=sorted(lines, key=int), meta=meta, trips=trips_out, peaks=peaks, lines=lines, schedule=sched, branches=branches, roster=roster, fleet=fleet, added=added, observed=observed, surplus=surplus, live=LVc,
                       source=dict(records=f"seznam-autobusu.cz ODIS vypravenost, fetched {O['snapshot']}", register='seznam-autobusu.cz register, carrier 28')))
