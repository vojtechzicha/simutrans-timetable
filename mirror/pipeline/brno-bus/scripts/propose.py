"""Propose Simutrans circuits from the timetable (a helper for writing the state file; not part of run.py).

  python propose.py --groups 40 41 57+66 ...            print the leg transitions and the proposed circuits
  python propose.py --groups ... --draft draft.json     also write the circuits as simutrans_lines entries

The IDS JMK GTFS has no vehicle blocks and splits long workings into several trips at timing points (40 runs
Tovární > Úzká > Tuřany > Úzká > Tovární as four trips). For each group of lines this chains the in-service
trips first-in-first-out at each stop (never waiting over --maxwait min) and counts, for every leg with at least
3 trips in 15:00-18:00, which leg the vehicle works next (15:00-17:30). Following each leg's most frequent
successor gives cycles: each cycle is a candidate Simutrans line. Legs left outside every cycle (minor branches,
depot-bound workings, one-way peak trips) are listed for a manual decision. Chaining only decides the order of
legs; vehicles are sized later by circuit_need.
"""
import argparse, collections, json
from common import gtfs_trips, gtfs_path, ROUTE_TYPE

p = argparse.ArgumentParser()
p.add_argument('--gtfs', default='2026-09-28'); p.add_argument('--service', default='20261002')
p.add_argument('--groups', nargs='+', required=True); p.add_argument('--maxwait', type=int, default=30)
p.add_argument('--draft'); p.add_argument('--quiet', action='store_true')
a = p.parse_args()
trips = [t for t in gtfs_trips(gtfs_path({'gtfs_date': a.gtfs}), a.service, ROUTE_TYPE)
         if not (t['o'].startswith('Vozovna') or t['d'].startswith('Vozovna'))]
draft = []
for g in a.groups:
    lines = set(g.split('+'))
    ts = sorted((t for t in trips if t['line'] in lines and 780 <= t['dep'] < 1170), key=lambda t: t['dep'])
    n3 = collections.Counter((t['line'], t['o'], t['d']) for t in ts if 900 <= t['dep'] < 1080)
    veh = []
    for t in ts:
        c = [v for v in veh if v['loc'] == t['o'] and v['free'] <= t['dep'] <= v['free'] + a.maxwait]
        v = min(c, key=lambda v: v['free']) if c else None
        if not v: v = dict(legs=[]); veh.append(v)
        v['legs'].append((t['line'], t['o'], t['d'], t['dep'])); v['loc'] = t['d']; v['free'] = t['arr']
    nxt = collections.defaultdict(collections.Counter)
    for v in veh:
        for x, y in zip(v['legs'], v['legs'][1:]):
            if 900 <= x[3] < 1050: nxt[x[:3]][y[:3]] += 1
    main = {k for k, n in n3.items() if n >= 3}
    succ = {k: nxt[k].most_common(1)[0][0] for k in main if nxt[k] and nxt[k].most_common(1)[0][0] in main}
    cycles, seen = [], set()
    for k in sorted(main):
        path, x = [], k
        while x in succ and x not in path: path.append(x); x = succ[x]
        if x in path:
            c = path[path.index(x):]; r = min(range(len(c)), key=lambda i: c[i]); c = c[r:] + c[:r]
            if tuple(c) not in seen: seen.add(tuple(c)); cycles.append(c)
    inside = {x for c in cycles for x in c}
    if not a.quiet:
        print(f'== {g}')
        for k in sorted(main):
            alts = ', '.join(f'{n}x {y[0]}:{y[1][:16]}>{y[2][:16]}' for y, n in nxt[k].most_common(3))
            print(f"   {n3[k]:>2} trips {k[0]}:{k[1][:20]}>{k[2][:20]}   next: {alts}")
    for c in cycles:
        print(f'   CIRCUIT {g}: ' + ' > '.join(f'{l}:{o}' for l, o, d in c) + f' > {c[0][1]}   ({[n3[x] for x in c]} trips 15-18)')
        draft.append(dict(id=g, name=g, entries=[list(x) for x in c]))
    left = sorted(main - inside)
    if left: print(f'   OUTSIDE ANY CIRCUIT: ' + '; '.join(f'{l}:{o}>{d} ({n3[(l, o, d)]})' for l, o, d in left))
if a.draft:
    json.dump(draft, open(a.draft, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
