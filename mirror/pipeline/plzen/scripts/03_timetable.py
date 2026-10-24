"""Timetable for one Plzeň state: network table, schedule fits and Simutrans schedule rows.

  python 03_timetable.py --state 2026-09-27

Rules specific to Plzeň (state file):
- fit.core: the peak window each fit must overlap - 15:00-16:00 for lines 1 and 2 (the 5-min peak ends
  about 16:05/16:20), 16:00-17:30 for line 4 (before 16:00 the two branches run an irregular 3/6/9 pattern).
- fit.depot_trips_counted: trips from Bolevec that end at Vozovna Slovany leave Bolevec in the 5-min
  pattern, so they count as Bolevec -> Slovany. Every other depot run is ignored.
- Every terminus is a loop (the fleet is single-ended except the KT8D5), so all entries get real - 1.
Writes data/derived/<state>/timetable.json.
"""
import argparse, collections, math, os, statistics
from common import RAW, DER, state, save, gtfs_trips, chain_at, runfit, loop_shift, DIV1440, hm

p = argparse.ArgumentParser(); p.add_argument('--state', required=True); a = p.parse_args()
S = state(a.state); F = S['fit']
trips = gtfs_trips(os.path.join(RAW, 'gtfs', S['gtfs_date'], 'gtfs.zip'), S['service_date'])

network = {}
for line in S['line_order']:
    pairs = collections.defaultdict(list)
    for t in trips:
        if t['line'] == line and 'Vozovna' not in t['o'] + t['d'] and 900 <= t['dep'] < 1080: pairs[(t['o'], t['d'])].append(t)
    rows = []
    for (o, d), xs in sorted(pairs.items(), key=lambda kv: -len(kv[1])):
        ts = sorted(x['dep'] for x in xs); gaps = [b - a for a, b in zip(ts, ts[1:])]
        rows.append(dict(o=o, d=d, m16=[x - 960 for x in ts if 960 <= x < 1020], hw=statistics.median(gaps),
                         run=round(statistics.mean(x['arr'] - x['dep'] for x in xs))))
    network[line] = rows

deps = collections.defaultdict(list); runs = collections.defaultdict(list)
for t in trips:
    if 'Vozovna' in t['o']: continue
    d = t['d']
    if 'Vozovna' in d:
        d = F.get('depot_trips_counted', {}).get(t['o'])
        if not d: continue
    deps[(t['line'], t['o'], d)].append(t['dep'])
    if 900 <= t['dep'] < 1080: runs[(t['line'], t['o'], d)].append(t['arr'] - t['dep'])
fits = {}
for k, D in deps.items():
    core = tuple(F['core'].get(k[0], F['core_default']))
    g = runfit(D, DIV1440, core)
    fits['|'.join(k)] = dict(I=g['I'], R=g['R'], first=g['first'], last=g['last'], run=round(statistics.mean(runs[k])),
                             deps=sorted(x for x in D if 840 <= x < 1140))

sched = []
for sl in S['simutrans_lines']:
    rows = []
    for l, o, d in sl['entries']:
        f = fits['|'.join([l, o, d])]; loop = o not in S['nonloop']
        rows.append(dict(stop=o, to=d, every=f['I'], real=f['R'], set=loop_shift(f['I'], f['R'], loop), loop=loop,
                         perh=len(f['R']) * 60 / f['I'], span=f"{hm(f['first'])}–{hm(f['last'])}", run=f['run']))
    tot = sum(r['run'] for r in rows)
    if sl.get('circuit'):   # one tram runs every entry in turn: the round trip is the sum, one slot per interval
        mint = math.ceil(tot / rows[0]['every'])
    else:
        mint = math.ceil(tot / min(r['every'] / len(r['real']) for r in rows))
    sched.append(dict(id=sl['id'], name=sl['name'], note=sl.get('note', ''), rows=rows, min_trams=mint))

need = {line: chain_at([t for t in trips if t['line'] == line])[0] for line in S['line_order']}

def _onroad(ts):
    """Most trams on the road at once 16:00-16:59: each trip holds its tram from departure to arrival + layover,
    the layover being min(3, the terminus's shortest timetabled turnaround 15:00-18:00) (the Prague/Ostrava rule)."""
    lay = {}
    for st in {t['d'] for t in ts}:
        arr = [t['arr'] for t in ts if t['d'] == st and 900 <= t['arr'] < 1080]
        dep = sorted(t['dep'] for t in ts if t['o'] == st)
        g = [next((d for d in dep if d >= a), a + 99) - a for a in arr]
        lay[st] = min(3, min(g)) if g else 3
    return max((sum(1 for t in ts if t['dep'] <= m < t['arr'] + lay[t['d']]) for m in range(960, 1020)), default=0)

import importlib.util as _ilu
_sp = _ilu.spec_from_file_location('tb_common', os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'brno-trolleybus', 'scripts', 'common.py'))
_tb = _ilu.module_from_spec(_sp); _sp.loader.exec_module(_tb)
sline_need = {}
for sl in S['simutrans_lines']:
    legs = [tuple(e[:3]) for e in sl['entries']]
    r = _tb.circuit_need(trips, legs, lay=3)
    o = _onroad([t for t in trips if t['line'] in {e[0] for e in sl['entries']}])
    sline_need[sl['id']] = max(r[0] if r else 0, o)
save(dict(network=network, fits=fits, schedule=sched, chain_at_16=need, sline_need=sline_need), os.path.join(DER, S['name'], 'timetable.json'))
print('timetable', S['name'], len(trips), 'trips; trams at 16:00 by chaining', need)
for s in sched:
    for r in s['rows']: print(f"  {s['id']:>2} {r['stop'][:20]:20} every {r['every']:>2} set {r['set']} (real {r['real']}) exact {r['span']}")
