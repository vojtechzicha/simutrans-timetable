"""Timetable for one network state: network table, schedule fits and Simutrans schedule rows.

  python 03_timetable.py --state closure-2026-09-27

Reads data/raw/gtfs/<gtfs_date>/gtfs.zip, keeps the tram trips of <service_date>, and writes
data/derived/<state>/timetable.json.
"""
import argparse, collections, math, os, statistics
from common import BASE, RAW, DER, state, save, gtfs_trips, chain_at, cycle_need, runfit, best_offset, loop_shift, DIV1440, ANY, hm

p = argparse.ArgumentParser(); p.add_argument('--state', required=True); a = p.parse_args()
S = state(a.state); F = S['fit']
trips = gtfs_trips(os.path.join(RAW, 'gtfs', S['gtfs_date'], 'gtfs.zip'), S['service_date'])
alias = S.get('stop_alias', {})            # e.g. line 10 arrivals "Vozovna Komín" -> the Komín loop
for t in trips:
    for k in ('o', 'd'):
        t[k] = alias.get(t['line'], {}).get(t[k], t[k])
skip = lambda t: any(x.startswith('Vozovna') or x in F.get('ignore_stops', []) for x in (t['o'], t['d']))

# ---- network table: 15:00-18:00 trips per terminus pair --------------------------------------
network = {}
for line in S['line_order']:
    pairs = collections.defaultdict(list)
    for t in trips:
        if t['line'] == line and not skip(t) and 900 <= t['dep'] < 1080: pairs[(t['o'], t['d'])].append(t)
    rows = []
    for (o, d), xs in sorted(pairs.items(), key=lambda kv: -len(kv[1])):
        ts = sorted(x['dep'] for x in xs); gaps = [b - a for a, b in zip(ts, ts[1:])]
        rows.append(dict(o=o, d=d, n3h=len(xs), m16=[x - 960 for x in ts if 960 <= x < 1020],
                         hw=statistics.median(gaps) if gaps else None,
                         run=round(statistics.mean(x['arr'] - x['dep'] for x in xs))))
    network[line] = rows

# ---- fits per terminus pair ------------------------------------------------------------------------
deps = collections.defaultdict(list)
for t in trips:
    if not skip(t): deps[(t['line'], t['o'], t['d'])].append(t['dep'])
runs = {(l, x['o'], x['d']): x['run'] for l, xs in network.items() for x in xs}
fits = {}
for k, D in deps.items():
    if sum(1 for x in D if 900 <= x < 1080) < 3: continue
    key = '|'.join(k)
    divs = ANY if k[0] in F.get('any_interval_lines', []) else DIV1440
    if key in F.get('overrides', {}):
        o = F['overrides'][key]; f = dict(I=o['I'], R=o['R'], first=o['first'], last=o['last'], exact=True, skip=o.get('skip'))
    elif k[0] in F.get('approx', {}):
        I = F['approx'][k[0]]; off, dev = best_offset(D, I)
        f = dict(I=I, R=[off], first=900, last=990, exact=False, dev=dev, note=F.get('approx_note', {}).get(k[0], ''))
    else:
        g = runfit(D, divs, tuple(F.get('core', [930, 990])))
        f = dict(I=g['I'], R=g['R'], first=g['first'], last=g['last'], exact=True, core=g['core'])
    f['deps'] = sorted(x for x in D if 840 <= x < 1140)
    fits[key] = f

# ---- Simutrans schedule rows ------------------------------------------------------------------
nonloop = S['nonloop']
sched = []
for sl in S['simutrans_lines']:
    rows = []
    for l, o, d in sl['entries']:
        f = fits['|'.join([l, o, d])]; I = f['I']; loop = o not in nonloop
        setv = loop_shift(I, f['R'], loop)
        rows.append(dict(stop=o, to=d, every=I, real=f['R'], set=setv, loop=loop, terminus=('loop' if loop else nonloop[o]),
                         perh=len(f['R']) * 60 / I, exact=f['exact'], span=f"{hm(f['first'])}–{hm(f['last'])}",
                         dev=f.get('dev'), skip=f.get('skip'), approx_note=f.get('note', ''), run=runs[(l, o, d)]))
    hw = min(r['every'] / len(r['real']) for r in rows)
    sched.append(dict(id=sl['id'], name=sl['name'], note=sl.get('note', ''), rows=rows,
                      min_trams=math.ceil(sum(r['run'] for r in rows) / hw)))

need = {line: chain_at([t for t in trips if t['line'] == line])[0] for line in S['line_order']}
cyc = {}
for line, (x, y) in S.get('cycle_pairs', {}).items():
    r = cycle_need([t for t in trips if t['line'] == line], x, y)
    if r: cyc[line] = dict(trams=r[0], minutes=r[1])

# ---- needs per Simutrans line (for the spares rule): circuit_need over each line's schedule entries, with the
# helper shared from pipeline/brno-trolleybus (a 3-min layover, as cycle_need); state fleet.need_overrides wins
import importlib.util as _ilu
_sp = _ilu.spec_from_file_location('tb_common', os.path.join(os.path.dirname(BASE), 'brno-trolleybus', 'scripts', 'common.py'))
_tb = _ilu.module_from_spec(_sp); _sp.loader.exec_module(_tb)
sline_need = {}
for sl in S['simutrans_lines']:
    legs = [tuple(e[:3]) for e in sl['entries']]
    r = _tb.circuit_need([t for t in trips if not skip(t)], legs, lay=3)
    if r: sline_need[sl['id']] = r[0]

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
sline_need.update({k: v['trams'] for k, v in cyc.items()})
onroad = {}
for sl in S['simutrans_lines']:
    ls = {e[0] for e in sl['entries']}
    if sum(1 for x in S['simutrans_lines'] if {e[0] for e in x['entries']} & ls) > 1: continue   # split lines (5/5S, 8/8S)
    onroad[sl['id']] = _onroad([t for t in trips if t['line'] in ls and not skip(t)])
    if sl['id'] in sline_need and onroad[sl['id']] > sline_need[sl['id']]: sline_need[sl['id']] = onroad[sl['id']]
sline_need.update(S['fleet'].get('need_overrides', {}))
save(dict(network=network, fits=fits, schedule=sched, chain_at_16=need, cycle_need=cyc, sline_need=sline_need),
     os.path.join(DER, S['name'], 'timetable.json'))
print('timetable', S['name'], 'trips', len(trips))
print('  trams needed by timetable cycle at 16:00:', {k: v['trams'] for k, v in cyc.items()})
for s in sched:
    for r in s['rows']:
        print(f"  {s['id']:>3} {r['stop'][:24]:24} every {r['every']:>2} set {r['set']} (real {r['real']}) "
              f"{'exact ' + r['span'] if r['exact'] else 'approx ±%s' % r['dev']}")
