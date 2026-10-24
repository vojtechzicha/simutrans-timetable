"""Timetable for one network state: network table, schedule fits, Simutrans rows and sizes.

  python 03_timetable.py --state 2026-09-29

Reads the IDS JMK GTFS (route_type 800 = trolleybus) for <service_date> and writes data/derived/<state>/timetable.json.
Simutrans lines come from the state: plain two-terminus lines, branch lines (30, 37) and pooled circuits
(25 + 26, 35 + 38 + 39), each sized by common.circuit_need.
"""
import argparse, collections, math, os, statistics
from common import DER, state, save, gtfs_trips, gtfs_path, circuit_need, turnarounds, runfit, runfit_rate, loop_shift, DIV1440, ROUTE_TYPE, hm

p = argparse.ArgumentParser(); p.add_argument('--state', required=True); a = p.parse_args()
S = state(a.state); F = S['fit']
trips = gtfs_trips(gtfs_path(S), S['service_date'], ROUTE_TYPE)
trips = [t for t in trips if not (t['o'].startswith('Vozovna') or t['d'].startswith('Vozovna'))]   # depot runs

# ---- network table: 15:00-18:00 trips per terminus pair ------------------------------------------
network = {}
for line in S['line_order']:
    pairs = collections.defaultdict(list)
    for t in trips:
        if t['line'] == line and 900 <= t['dep'] < 1080: pairs[(t['o'], t['d'])].append(t)
    rows = []
    for (o, d), xs in sorted(pairs.items(), key=lambda kv: -len(kv[1])):
        ts = sorted(x['dep'] for x in xs); gaps = [b - a for a, b in zip(ts, ts[1:])]
        rows.append(dict(o=o, d=d, n3h=len(xs), m16=[x - 960 for x in ts if 960 <= x < 1020],
                         hw=statistics.median(gaps) if gaps else None,
                         run=round(statistics.mean(x['arr'] - x['dep'] for x in xs))))
    network[line] = rows

# ---- Simutrans lines: fit each stop entry, loop -1, size by circuit ------------------------------
nonloop = S['nonloop']; sched = []
for sl in S['simutrans_lines']:
    legs = [tuple(e[:3]) for e in sl['entries']]
    rows = []
    # one rate for the whole line: each entry's plain fit gives departures an hour; take the value most entries
    # share. Entries with designed slots don't vote; on a tie the lower rate wins (the other end can't return more).
    def entry_deps(e):
        xs = [t for t in trips if (t['line'], t['o'], t['d']) == tuple(e[:3])]
        return [t for t in xs if t['dep'] % e[3]['mod'] in e[3]['keep']] if len(e) > 3 else xs
    des_stops = sl.get('designed_slots', {})
    per = []
    for e in sl['entries']:
        if e[1] in des_stops: continue
        g = runfit([t['dep'] for t in entry_deps(e)], DIV1440, tuple(F['core'])); per.append(len(g['R']) * 60 // g['I'])
    cnt = collections.Counter(per); top = max(cnt.values())
    rate = sl.get('rate') or min(r for r, n in cnt.items() if n == top)
    for e in sl['entries']:
        l, o, d = e[:3]; sub = e[3] if len(e) > 3 else None
        xs = entry_deps(e); D = [t['dep'] for t in xs]
        key = '|'.join([sl['id'], l, o, d] + ([str(sub['keep'][0])] if sub else []))
        if key in F['overrides']:
            ov = F['overrides'][key]; f = dict(I=ov['I'], R=ov['R'], first=ov['first'], last=ov['last'])
        else:
            f = runfit(D, DIV1440, tuple(F['core']))
            if len(f['R']) * 60 != rate * f['I'] and o not in des_stops:          # other rate than the line: fit at the line's rate
                f = runfit_rate(D, rate, DIV1440, tuple(F['core'])) or f
        I, R = f['I'], list(f['R'])
        des = sl.get('designed_slots', {}).get(o); added = []
        if des:                                   # designed slots are given on their own interval
            if des['every'] != I:
                assert des['every'] % I == 0, (sl['id'], o, I)
                R = sorted({r + k * I for r in R for k in range(des['every'] // I)}); I = des['every']
            added = [x for x in des['add'] if x not in R]; R = sorted(R + added)
        loop = o not in nonloop
        run = round(statistics.mean(t['arr'] - t['dep'] for t in xs if 900 <= t['dep'] < 1080))
        rows.append(dict(line=l, stop=o, to=d, every=I, real=R, set=loop_shift(I, R, loop), loop=loop,
                         terminus=('loop' if loop else nonloop[o]), perh=len(R) * 60 / I,
                         span=f"{hm(f['first'])}–{hm(f['last'])}", designed=added,
                         designed_why=des['why'] if des else '', run=run,
                         deps=sorted(x for x in D if 900 <= x < 1080)))
    lay = turnarounds(trips, legs, S.get('turnaround_default', 3), S.get('links'))
    need = circuit_need(trips, legs, lay=lay, links=S.get('links'), period=sl.get('period'))
    sched.append(dict(id=sl['id'], name=sl['name'], rate=rate, note=sl.get('note', ''), pool=sl.get('pool', False),
                      pool_text=sl.get('pool_text', ''), rows=rows,
                      min_run=math.ceil(sum(r['run'] * r['perh'] / 60 for r in rows)),
                      need=dict(vehicles=need[0], minutes=need[1],
                                path=[[legs[i][1], legs[i][2], hm(d), hm(a2)] for i, d, a2 in need[2]]) if need else None,
                      lay={f'{legs[i - 1][2]} → {legs[i][2]}': v for i, v in lay.items()}))

save(dict(network=network, schedule=sched), os.path.join(DER, S['name'], 'timetable.json'))
print('timetable', S['name'], 'trips', len(trips))
for s in sched:
    n = s['need']
    print(f"  {s['id']:>9}: need {n['vehicles'] if n else '?'} (cycle {n['minutes'] if n else '?'} min), by runtime >= {s['min_run']}")
    for r in s['rows']:
        print(f"      {r['stop'][:26]:26} -> {r['to'][:22]:22} every {r['every']:>2} set {r['set']} (real {r['real']}) {r['span']}"
              + (f" designed {r['designed']}" if r['designed'] else ''))
