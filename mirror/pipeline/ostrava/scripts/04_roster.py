"""trips + fleet + records + live -> derived/lines.json (peak counts, branch tables) and roster.json.

1. Turns: trips chained at termini (lib.blocks); a line's demand = turns running at peak_minute.
2. Type mix per line = weighted history shares (T3R.P folded into Vario LF; single Vario LF on the 2×T
   lines 1 and 2 becomes a coupled pair), rounded by largest remainder.
3. Caps: per type, active cars (register state zar, or seen in the live feed) minus a reserve;
   overflow moves to the line where that type's share is lowest, onto its next type with room.
4. Picking: best score per slot; score = history weight on this line + 15 if the car's depot is the
   line's home depot + 40 if seen on this line live (+8 if live on another line) + 0.05 x all its
   history + 3 if recorded since 2026-04-01. Pairs reuse pairs seen in the records.
"""
import collections, json, math
from lib import CONFIG, load, save, blocks, active_at, make_nm, hhmm, cycle_need, min_turnaround, pattern_need

C = CONFIG; nm = make_nm(C)
trips = load('trips.json'); SCH = load('schedule.json')
fleet = {int(k): v for k, v in load('fleet.json').items()}
R = load('records.json'); recs = R['records']; lastseen = {int(k): v for k, v in R['lastseen'].items()}
live = {int(k): v for k, v in load('live.json')['cars'].items()}
T = C['peak_minute']; TW = C['table_window']

# ---- lines: demand and branch tables
lines = {}
for L, tr in trips.items():
    bl = blocks(tr)
    var = collections.defaultdict(list)
    for t in tr:
        if TW[0] <= t['dep'] < TW[1]: var[(nm(t['fr']), nm(t['to']))].append(t)
    V = []
    for (a, b), ts in sorted(var.items(), key=lambda x: -len(x[1])):
        deps = sorted(t['dep'] for t in ts)
        gaps = [y - x for x, y in zip(deps, deps[1:])]
        seq = collections.Counter(tuple(nm(s) for s in t['stops']) for t in ts).most_common(1)[0][0]
        V.append(dict(fr=a, to=b, n=len(ts), hw=collections.Counter(gaps).most_common(1)[0][0] if gaps else None,
                      deps=[hhmm(d) for d in deps], min_peak_hour=sorted(set(d % 60 for d in deps if T <= d < T + 60)),
                      rt=round(sum(t['arr'] - t['dep'] for t in ts) / len(ts)), stops=list(seq)))
    lines[L] = dict(at_peak=len(active_at(bl, T)), turns=len(bl), variants=V)
save('lines.json', lines)
DEM = {L: v['at_peak'] for L, v in lines.items() if v['at_peak'] > 0}

# ---- availability and caps
def cat(n): return fleet[n]['cat']
def available(n): return n in fleet and (n in live or fleet[n]['state'] == 'zar')
pool = collections.defaultdict(list)
for n in fleet:
    if available(n) and cat(n) not in ('?',) + tuple(C['types_not_planned']): pool[cat(n)].append(n)
CAP = {t: len(v) for t, v in pool.items()}
LIM = {t: c - (0 if c < 4 else max(1, round(c * 0.08))) for t, c in CAP.items()}
TWO = set(C['two_t_lines'])

def shares(L, ls=None):
    c = collections.Counter()
    for l, t, nums, w, k, no in recs:
        if l not in (ls or [L]): continue
        # T3R.P counts as Vario LF, a coupled T3 pair as a coupled Vario pair. A coupled pair stays a pair on every
        # line (user, 18 Oct 2026: line 7 ran 1360 + 1359 coupled; the old rule split pairs into singles off 1 and 2)
        if t.replace('2×', '') in C['types_not_planned']: t = ('2×' if t.startswith('2×') else '') + 'Vario LF'
        if L in TWO and t == 'Vario LF': t = '2×Vario LF'
        c[t] += w
    tot = sum(c.values())
    return {t: v / tot for t, v in c.items()} if tot else {'Vario LF': 0.5, 'Tango NF2': 0.5}
def units(t): return 2 if t.startswith('2×') else 1

alloc = {}
for L in C['line_order_for_picking']:
    if L not in DEM: continue
    N = DEM[L]; raw = {t: N * s for t, s in shares(L).items()}
    base = {t: int(v) for t, v in raw.items()}
    for t, _ in sorted(raw.items(), key=lambda x: -(x[1] - int(x[1])))[:N - sum(base.values())]: base[t] += 1
    alloc[L] = {t: c for t, c in base.items() if c > 0}
def used(t): return sum(c * units(tt) for L in alloc for tt, c in alloc[L].items() if tt.replace('2×', '') == t)
for _ in range(500):
    over = [t for t in LIM if used(t) > LIM[t]]
    if not over: break
    t = over[0]
    s, L, tt = min((shares(L).get(tt, 0), L, tt) for L in alloc for tt, c in alloc[L].items() if c > 0 and tt.replace('2×', '') == t)
    alt = [a for a, _ in sorted(shares(L).items(), key=lambda x: -x[1]) if a.replace('2×', '') != t and used(a.replace('2×', '')) + units(a) <= LIM.get(a.replace('2×', ''), 0)]
    alt = alt or (['39T'] if L in TWO else ['Vario LF'])
    alloc[L][tt] -= 1; alloc[L][alt[0]] = alloc[L].get(alt[0], 0) + 1
    alloc[L] = {a: c for a, c in alloc[L].items() if c > 0}

# ---- picking
aff = collections.defaultdict(collections.Counter); pairs = collections.Counter()
for l, t, nums, w, k, no in recs:
    for n in nums: aff[n][l] += w
    if len(nums) == 2: pairs[tuple(sorted(nums))] += 1
HOME = {}
for L in DEM:
    c = collections.Counter()
    for n, a in aff.items():
        if n in fleet and a[L]: c[fleet[n]['depot']] += a[L]
    HOME[L] = c.most_common(1)[0][0] if c else None
def score(n, L):
    s = aff[n][L] + (15 if fleet[n]['depot'] == HOME.get(L) else 0)
    s += 40 if L in live.get(n, {}) else (8 if n in live else 0)
    s += 0.05 * sum(aff[n].values()) + (3 if lastseen.get(n, '') >= '2026-04-01' else 0)
    return s
usedv, roster = set(), {}
for L in C['line_order_for_picking']:
    if L not in alloc: continue
    out = []
    for t, c in sorted(alloc[L].items(), key=lambda x: -x[1]):
        b = t.replace('2×', '')
        for _ in range(c):
            cand = [n for n in pool[b] if n not in usedv]
            if t.startswith('2×'):
                best = next(((x, y) for (x, y), _ in pairs.most_common() if x in cand and y in cand and cat(x) == b
                             and fleet[x]['depot'] == fleet[y]['depot'] == HOME.get(L)), None)
                if not best:
                    cand.sort(key=lambda n: -score(n, L)); x = cand[0]
                    y = sorted([n for n in cand[1:] if fleet[n]['depot'] == fleet[x]['depot']], key=lambda n: -score(n, L))[0]
                    best = (x, y)
                usedv.update(best); out.append([t, list(best)])
            else:
                cand.sort(key=lambda n: -score(n, L)); usedv.add(cand[0]); out.append([t, [cand[0]]])
    roster[L] = out
# ---- branches: each is its own Simutrans line, sized by its round trip (cycle_need, lay 3, t0)
# Units from the chaining count are shared out so that every branch gets at least its need; where the
# line has fewer units than the branches need, cars are added (designed: best-scoring unused active car
# of the line's most common type) and marked "added".
branches = {}; added_log = []
for L, units_ in roster.items():
    T0 = C['cycle_t0']
    tr = [dict(t, o=nm(t['fr']), d=nm(t['to'])) for t in trips[L]]
    # layover at each terminus: 3 min, or the timetable's own shorter turnaround there (14:00-18:00)
    mt = min_turnaround(tr)
    lay = {k: min(C['cycle_lay'], v) for k, v in mt.items()}
    brs = []
    for a, b in C['branches'][L]:
        cn = cycle_need(tr, a, b, T0, lay) or cycle_need(tr, b, a, T0, lay)
        rts = [t['arr'] - t['dep'] for t in tr if {t['o'], t['d']} == {a, b} and 900 <= t['dep'] < 1080]
        deps = sorted(t['dep'] for t in tr if t['o'] == a and t['d'] == b and 900 <= t['dep'] < 1080)
        gaps = [y - x for x, y in zip(deps, deps[1:])]
        hw = collections.Counter(gaps).most_common(1)[0][0] if gaps else None
        rt2 = 2 * sum(rts) / len(rts) if rts else None
        brs.append(dict(a=a, b=b, need=cn[0] if cn else 0, cycle=cn[1] if cn else None, lay_a=lay.get(a, C['cycle_lay']), lay_b=lay.get(b, C['cycle_lay']),
                        min_runtime=math.ceil(rt2 / hw) if (rt2 and hw) else None, headway=hw))
        # size from the schedule pattern the sheet suggests (user rule, 20 Oct 2026), where both ends are scheduled
        pa = next((p for p in SCH.get(L, []) if p.get('every') and p['fr'] == a and p['to'] == b), None)
        pb = next((p for p in SCH.get(L, []) if p.get('every') and p['fr'] == b and p['to'] == a), None)
        if pa and pb:
            def rt_(x, y):
                r = [t['arr'] - t['dep'] for t in tr if t['o'] == x and t['d'] == y and 900 <= t['dep'] < 1080]
                return round(sum(r) / len(r))
            rts_ = [rt_(a, b), rt_(b, a)]
            n_, cyc_, w_ = pattern_need([pa, pb], rts_, [lay.get(a, C['cycle_lay']), lay.get(b, C['cycle_lay'])], T0)
            brs[-1].update(need=n_, cycle=cyc_, how='pattern', waits=w_, runtimes=rts_, pattern_every=pa['every'])
    need = sum(x['need'] for x in brs)
    short = need - len(units_)
    for _ in range(max(0, short)):
        t = collections.Counter(u[0] for u in units_).most_common(1)[0][0]; base = t.replace('2×', '')
        cand = sorted([n for n in pool[base] if n not in usedv], key=lambda n: -score(n, L))
        if t.startswith('2×'):
            x = cand[0]; y = [n for n in cand[1:] if fleet[n]['depot'] == fleet[x]['depot']][0]; nums = [x, y]
        else: nums = [cand[0]]
        usedv.update(nums); units_.append([t, nums, 'added'])
        added_log.append(dict(line=L, cars=nums, type=t, why=f'best-scoring unused active {t} for line {L} (history on the line, home depot, seen live); not used on any other line that day'))
    # every branch its need first, then the extra units by largest remainder of need share
    alloc_b = [x['need'] for x in brs]
    extra = len(units_) - sum(alloc_b)
    if extra > 0:
        tot = sum(alloc_b) or 1
        raw = [extra * x / tot for x in alloc_b]; add = [int(r) for r in raw]
        for i in sorted(range(len(raw)), key=lambda i: -(raw[i] - int(raw[i])))[:extra - sum(add)]: add[i] += 1
        alloc_b = [a + b for a, b in zip(alloc_b, add)]
    k = 0
    for i, x in enumerate(brs):
        x['assigned'] = alloc_b[i]
        for u in units_[k:k + alloc_b[i]]:
            if len(u) == 2: u.append('')
            u.append(i)
        k += alloc_b[i]
    branches[L] = brs
    print('branches', L, [(x['a'][:10], x['b'][:12], 'need', x['need'], 'assigned', x['assigned'], 'min by runtime', x['min_runtime']) for x in brs],
          f'added {short}' if short > 0 else '')
# ---- circuits (config.circuits; user, 18 Oct 2026): lines whose every tram runs through at a hub (1 -> 2 -> 1 at
# Hlavní nádraží) are one Simutrans line. The member lines' units are pooled under the circuit's key (its first line)
# as one branch, sized by circuit_need: one tram followed round all legs at cycle_t0, 3 min layovers at the outer
# termini (or their shorter timetabled turnaround), at least 3 min at the hub, where the wait is between two lines.
from lib import circuit_need
MEMBERS = {}
for G, cc in C.get('circuits', {}).items():
    ms = [L for L in cc['lines'] if L in roster]
    if len(ms) < 2: continue
    MEMBERS[G] = ms
    trs = {L: [dict(t, o=nm(t['fr']), d=nm(t['to'])) for t in trips[L]] for L in ms}
    lay = {}
    for L in ms:
        for k, v in min_turnaround(trs[L]).items(): lay[k] = min(lay.get(k, C['cycle_lay']), v)
    lay[cc['hub']] = C['cycle_lay']
    legs = cc['legs']
    cn = circuit_need([(trs[l], a, b) for l, a, b in legs], C['cycle_t0'], lay)
    rts = []
    for l, a, b in legs:
        r = [t['arr'] - t['dep'] for t in trs[l] if t['o'] == a and t['d'] == b and 900 <= t['dep'] < 1080]
        rts.append(round(sum(r) / len(r)))
    l0, a0, b0 = legs[0]
    deps = sorted(t['dep'] for t in trs[l0] if t['o'] == a0 and t['d'] == b0 and 900 <= t['dep'] < 1080)
    gaps = [y - x for x, y in zip(deps, deps[1:])]
    hw = collections.Counter(gaps).most_common(1)[0][0]
    units_ = [u for L in ms for u in roster[L]]
    for u in units_: u[3] = 0
    for _ in range(max(0, cn[0] - len(units_))):
        t = collections.Counter(u[0] for u in units_).most_common(1)[0][0]; base = t.replace('2×', '')
        cand = sorted([n for n in pool[base] if n not in usedv], key=lambda n: -max(score(n, m) for m in ms))
        nums = [cand[0], next(n for n in cand[1:] if fleet[n]['depot'] == fleet[cand[0]]['depot'])] if t.startswith('2×') else [cand[0]]
        usedv.update(nums); units_.append([t, nums, 'added', 0])
        added_log.append(dict(line=cc['title'], cars=nums, type=t, why=f'best-scoring unused active {t} for the {cc["title"]} circuit'))
    roster[G] = units_
    for L in ms[1:]: del roster[L]; del branches[L]
    branches[G] = [dict(a=a0, b=legs[len(legs) // 2][1], circuit=G, title=cc['title'], legs=legs, runtimes=rts, waits=cn[2],
                        need=cn[0], cycle=cn[1], lay=lay, min_runtime=math.ceil(sum(rts) / hw), headway=hw, assigned=len(units_))]
    print('circuit', cc['title'], 'need', cn[0], 'cycle', cn[1], 'waits', cn[2], 'runtimes', rts, 'units', len(units_))
def mem(L): return MEMBERS.get(L, [L])
def gscore(n, L): return max(score(n, m) for m in mem(L))

# ---- roster coverage and spares (user, 29 Sep 2026; pipeline/README.md "Roster coverage and spares", applied by
# session simutrans-timetable-b5). Per Simutrans line (branch): where more units are assigned than its need, exactly
# the need is counted - one of every unit type first, then the best-scoring picks (Brno's mark_spares, reused); the
# rest are "not needed", shown but not counted. Then every type in the line's history roster (types with at least
# config.coverage_min_share of the line's weighted records; rarer ones are one-off stand-ins) must be among the
# counted units: a missing type swaps in its best free car for one unit of the line's most frequent type. The free
# history cars left over are listed as "not needed" (spares) with their last date on the line.
import importlib.util, os as _os
from lib import RAW, record_date
_bs = importlib.util.spec_from_file_location('brnotrolleylib', _os.path.join(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))), 'brno-trolleybus', 'scripts', 'common.py'))
_bl = importlib.util.module_from_spec(_bs); _bs.loader.exec_module(_bl)
surplus, coverage, spares = {}, [], {}
for L, units_ in roster.items():
    for i, b in enumerate(branches[L]):
        us = [dict(type=u[0], kurz=k, src='', u=u) for k, u in enumerate(units_) if u[3] == i]
        if _bl.mark_spares(us, b['need']):
            surplus.setdefault(L, []).extend(x['u'] for x in us if x.get('spare'))
    if L in surplus: roster[L] = [u for u in units_ if u not in surplus[L]]
counted = {n for L in roster for u in roster[L] for n in u[1]}
for L in roster:
    have = collections.Counter(u[0] for u in roster[L])
    for t, sh in sorted(shares(L, mem(L)).items(), key=lambda x: -x[1]):
        if sh < C.get('coverage_min_share', 0) or have[t] or t.replace('2×', '') not in pool: continue
        big, c = have.most_common(1)[0]
        if c < 2: break
        base = t.replace('2×', '')
        cand = sorted([n for n in pool[base] if n not in counted], key=lambda n: -gscore(n, L))
        if t.startswith('2×'):
            if len(cand) < 2: continue
            x = cand[0]; y = next((n for n in cand[1:] if fleet[n]['depot'] == fleet[x]['depot']), None)
            if y is None: continue
            nums = [x, y]
        elif cand: nums = [cand[0]]
        else: continue
        out = [u for u in roster[L] if u[0] == big][-1]
        roster[L][roster[L].index(out)] = [t, nums, 'covers', out[3]]
        counted.difference_update(out[1]); counted.update(nums)
        have[big] -= 1; have[t] += 1
        coverage.append(dict(line=L, cars=nums, type=t, replaced=out[1]))
last = {}
hp = _os.path.join(RAW, 'history.json')
if _os.path.exists(hp):
    for L_, rows in json.load(open(hp, encoding='utf-8')).items():
        for r in rows:
            d = record_date(r['date'])
            if not d: continue
            for n in [int(x) for x in __import__('re').findall(r'\d{3,4}', r['car'])]:
                last[(n, L_)] = max(last.get((n, L_), ''), d.isoformat())
for L in roster:
    hist = [n for n in aff if any(aff[n][m] for m in mem(L)) and available(n) and cat(n) not in C['types_not_planned'] and n not in counted]
    lst = lambda n: max(last.get((n, m), '') for m in mem(L))
    spares[L] = [dict(car=n, last=lst(n), weight=round(sum(aff[n][m] for m in mem(L)), 1)) for n in sorted(hist, key=lst, reverse=True)]
for L, brs in branches.items():
    for i, b in enumerate(brs):
        b['surplus'] = sum(1 for u in surplus.get(L, []) if u[3] == i)
        b['assigned'] = sum(1 for u in roster[L] if u[3] == i)
print('surplus', {L: len(v) for L, v in surplus.items()}, 'coverage swaps', coverage, 'spares', sum(len(v) for v in spares.values()))
save('roster.json', dict(members=MEMBERS, demand=DEM, alloc=alloc, cap=CAP, lim=LIM, home=HOME, roster=roster, branches=branches, added=added_log,
                         surplus=surplus, coverage=coverage, spares=spares))
print('demand', DEM, 'total', sum(DEM.values()))
for L in C['line_order_for_picking']:
    if L in roster: print(L, [('+'.join(map(str, u[1])), u[0], u[2]) for u in roster[L]])
