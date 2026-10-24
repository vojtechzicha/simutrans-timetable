"""trips -> derived/lines.json (variant tables) and needs.json (Simutrans lines per DPmML line and the buses each needs).

1. Branches, found by rule as on the Ostrava bus sheet (config.branch_rule). A line's trips in 15:00–18:00 are grouped
   by terminus pair (unordered; a loop line that starts and ends at one stop is a pair of one). A pair is its own
   Simutrans line when it has >= 2 × min_trips trips in the window, a departure in the 16 o'clock hour and no garage
   end. The pair with the most trips is always a branch. Smaller pairs (extensions, short workings, garage runs)
   are not separate lines; 05_schedule folds their minutes into the main row from the same terminus.
2. Need per branch at 16:00 (brief rule d):
   - two termini: cycle_need_peak (Ostrava trolleybus lib): follow a bus leaving around 16:00 round the branch,
     taking at each end the first departure at least the layover later; the layover is 3 min, or the terminus's own
     shorter timetabled turnaround. A round trip waiting over max(30, 1.5 × headway) is skipped (the buses leave as
     another line).
   - a loop line (one terminus): the same idea on one end: a bus leaving around 16:00 returns after the loop's
     runtime and takes the first departure at least the layover later; the departures in between are the buses.
   - no complete round trip: the chained turns of that pair on the road at 16:00, at least 1.
   The line's need is the larger of the branch sum and the buses on the road: every trip (no garage end) holds its
   bus from departure to arrival + min(3 min, the terminus's shortest timetabled turnaround), the most at once in
   16:00–16:59. The difference goes to the main branch (it carries the extensions' and short workings' buses).
"""
import collections, math
from lib import CONFIG, load, save, make_nm, hhmm, cycle_need_peak, min_turnaround, blocks, active_at

C = CONFIG; nm = make_nm(C); BRW = C['branch_rule']; DEPOTS = set(C['depot_stops']); TW = C['table_window']
trips = load('trips.json')

# ---- variant tables (display)
lines = {}
for L, tr in trips.items():
    var = collections.defaultdict(list)
    for t in tr:
        if TW[0] <= t['dep'] < TW[1]: var[(nm(t['fr']), nm(t['to']))].append(t)
    V = []
    for (a, b), ts in sorted(var.items(), key=lambda x: -len(x[1])):
        deps = sorted(t['dep'] for t in ts); gaps = [y - x for x, y in zip(deps, deps[1:])]
        seq = collections.Counter(tuple(nm(s) for s in t['stops']) for t in ts).most_common(1)[0][0]
        V.append(dict(fr=a, to=b, n=len(ts), hw=collections.Counter(gaps).most_common(1)[0][0] if gaps else None,
                      deps=[hhmm(d) for d in deps], min_peak_hour=sorted(set(d % 60 for d in deps if 960 <= d < 1020)),
                      rt=round(sum(t['arr'] - t['dep'] for t in ts) / len(ts)), stops=list(seq)))
    lines[L] = dict(variants=V)
save('lines.json', lines)

def headway(deps):
    g = [y - x for x, y in zip(deps, deps[1:])]
    return collections.Counter(g).most_common(1)[0][0] if g else None

def loop_need(tr, a, t0, lay, max_wait):
    A = sorted((t['dep'], t['arr']) for t in tr if t['o'] == a and t['d'] == a)
    deps = [d for d, _ in A]; res = []
    for s, arr in A:
        if not (t0 - 30 <= s < t0 + 30): continue
        nx = next((d for d in deps if d >= arr + lay.get(a, 3)), None)
        if nx is None or nx - arr > max_wait: continue
        res.append((sum(1 for d in deps if s <= d < nx), nx - s))
    return max(res) if res else None

needs = {}
for L, tr in trips.items():
    tr = [dict(t, o=nm(t['fr']), d=nm(t['to'])) for t in tr]
    win = [t for t in tr if BRW['window'][0] <= t['dep'] < BRW['window'][1]]
    pairs = collections.defaultdict(list)
    for t in win: pairs[frozenset((t['o'], t['d']))].append(t)
    ranked = sorted(pairs.items(), key=lambda x: (-len(x[1]), sorted(x[0])))
    chosen = []
    for p, ts in ranked:
        hour = any(BRW['hour'][0] <= t['dep'] < BRW['hour'][1] for t in ts)
        big = len(ts) >= (BRW['min_trips'] if len(p) == 1 else 2 * BRW['min_trips'])
        if not chosen or (big and hour and not (p & DEPOTS)): chosen.append((p, ts))
    lay = {k: min(C['cycle_lay'], v) for k, v in min_turnaround(tr).items()}
    brs = []
    for p, ts in chosen:
        cnt = collections.Counter(t['o'] for t in ts)
        a = max(p, key=lambda x: (cnt[x], x)); b = next((x for x in p if x != a), a)
        dA = sorted(t['dep'] for t in tr if t['o'] == a and t['d'] == b)
        hw = headway([x for x in dA if 900 <= x < 1080]) or 30
        mw = max(30, int(1.5 * hw))
        if a == b: cn = loop_need(tr, a, C['cycle_t0'], lay, mw); kind = 'loop'
        else:
            cn = cycle_need_peak(tr, a, b, C['cycle_t0'], lay, max_wait=mw) or cycle_need_peak(tr, b, a, C['cycle_t0'], lay, max_wait=mw); kind = 'round trip'
        how = kind
        if not cn:
            act = len(active_at(blocks([t for t in tr if {t['o'], t['d']} == set(p)]), C['cycle_t0']))
            cn = (max(1, act), None); how = 'turns at 16:00'
        rts = [t['arr'] - t['dep'] for t in ts]
        brs.append(dict(a=a, b=b, loop=a == b, need=cn[0], cycle=cn[1], how=how, headway=hw if dA else None, trips=len(ts),
                        lay={a: lay.get(a, C['cycle_lay']), b: lay.get(b, C['cycle_lay'])}))
    others = [dict(pair=sorted(p), trips=len(ts)) for p, ts in ranked if all(p != q for q, _ in chosen)]
    rt_ = [t for t in tr if not ({t['o'], t['d']} & DEPOTS)]
    onroad = max(sum(1 for t in rt_ if t['dep'] <= m < t['arr'] + lay.get(t['d'], C['cycle_lay'])) for m in range(960, 1020))
    extra = onroad - sum(b['need'] for b in brs)
    if extra > 0: brs[0]['need'] += extra; brs[0]['variant_extra'] = extra
    needs[L] = dict(branches=brs, others=others, onroad=onroad)
    print(L, 'on road', onroad, [(b['a'], b['b'], b['need'], b['how'], b['cycle']) for b in brs], 'others', [(o['pair'], o['trips']) for o in others])
save('needs.json', needs)
print('need', sum(b['need'] for n in needs.values() for b in n['branches']), 'Simutrans lines', sum(len(n['branches']) for n in needs.values()))
