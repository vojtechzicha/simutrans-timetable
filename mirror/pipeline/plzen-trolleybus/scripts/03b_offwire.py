"""Off-wire (battery) sections of every trolleybus stop pattern: GTFS stops against the OpenStreetMap overhead wire.

  python 03b_offwire.py --state 2026-09-29

Adapted from pipeline/praha-trolleybus/scripts/03b_offwire.py. The PMDP GTFS has no shapes.txt, and the OSM
trolleybus route relations of Plzeň are out of date (11 ends at CAN Husova, 10 at Černice, no 49), so the test is
made per stop instead of along a shape:
- a stop is under the wire when an OSM trolley_wire=yes way lies within `osm.tolerance_m` (state: 60 m) of its
  platform (GTFS stop position); a platform is on the kerb of the wired road, a few metres from the wire;
- consecutive stops away from the wire form an off-wire stretch, named from the last stop under the wire to the
  last stop of the stretch (or from the first stop of the stretch to the first stop under the wire again);
- one terminus stop within `osm.loop_m` (default 200 m) of the wire, alone, is a turning loop whose platform lies
  off the wire (Lobzy, Na Dlouhých, Nová Hospoda): not a battery stretch;
- stretch length = the straight-line distance between its stops (an underestimate of the road distance).
Output data/derived/<state>/offwire.json {line: [dict(o, d, trips, stretches=[[from, to, km]], stops=[[name, metres]])]}.
"""
import argparse, collections, csv, io, math, os, zipfile
from common import state, load, save, RAW, DER, gtfs_path

ap = argparse.ArgumentParser(); ap.add_argument('--state', required=True)
S = state(ap.parse_args().state); osm = S.get('osm', {})
tol = osm.get('tolerance_m', 40); loop_m = osm.get('loop_m', 200)
lat0 = math.radians(49.74)
xy = lambda la, lo: (math.radians(lo) * 6371000 * math.cos(lat0), math.radians(la) * 6371000)
W = load(os.path.join(RAW, 'osm', S['osm_date'], 'trolley_wire.json'))['elements']
grid = collections.defaultdict(list)
for e in W:
    pts = [xy(p['lat'], p['lon']) for p in e.get('geometry', [])]
    for a, b in zip(pts, pts[1:]):
        for gx in range(int(min(a[0], b[0]) // 100) - 1, int(max(a[0], b[0]) // 100) + 2):
            for gy in range(int(min(a[1], b[1]) // 100) - 1, int(max(a[1], b[1]) // 100) + 2):
                grid[(gx, gy)].append((a, b))
segs = [s for v in grid.values() for s in v]
def dist(p, a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]; L = dx * dx + dy * dy
    t = 0 if L == 0 else max(0, min(1, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / L))
    return math.hypot(p[0] - a[0] - t * dx, p[1] - a[1] - t * dy)
def wire_m(p):
    near = grid.get((int(p[0] // 100), int(p[1] // 100)))
    if near: d = min(dist(p, a, b) for a, b in near)
    else: d = 999999
    return d if d <= 100 else min(dist(p, a, b) for a, b in segs)

z = zipfile.ZipFile(gtfs_path(S))
rd = lambda f: csv.DictReader(io.TextIOWrapper(z.open(f), encoding='utf-8-sig'))
routes = {r['route_id']: r['route_short_name'] for r in rd('routes.txt') if r['route_type'] == S['route_type']}
trips = {t['trip_id']: routes[t['route_id']] for t in rd('trips.txt') if t['route_id'] in routes}
stops = {r['stop_id']: (r['stop_name'], xy(float(r['stop_lat']), float(r['stop_lon']))) for r in rd('stops.txt')}
st = collections.defaultdict(list)
for r in rd('stop_times.txt'):
    if r['trip_id'] in trips: st[r['trip_id']].append((int(r['stop_sequence']), r['stop_id']))
pat = collections.Counter()
for tid, rs in st.items():
    rs.sort(); pat[(trips[tid], tuple(s for _, s in rs))] += 1
depots = set(S.get('depot_stops', []))
res = collections.defaultdict(list); mcache = {}
for (L, seq), n in pat.most_common():
    if L not in S['line_order']: continue
    names = [stops[s][0] for s in seq]
    if names[0] in depots or names[-1] in depots: continue
    m = [mcache.setdefault(s, wire_m(stops[s][1])) for s in seq]
    off = [x > tol for x in m]
    for i in (0, len(seq) - 1):                 # a lone terminus platform near the wire: a turning loop
        nb = i + 1 if i == 0 else i - 1
        if off[i] and m[i] <= loop_m and not off[nb]: off[i] = False
    stretches, i = [], 0
    while i < len(seq):
        if not off[i]: i += 1; continue
        j = i
        while j + 1 < len(seq) and off[j + 1]: j += 1
        a = i - 1 if i > 0 else i; b = j + 1 if j + 1 < len(seq) else j   # include the wired stop at each side
        km = sum(math.hypot(stops[seq[k + 1]][1][0] - stops[seq[k]][1][0], stops[seq[k + 1]][1][1] - stops[seq[k]][1][1]) for k in range(a, b)) / 1000
        stretches.append([names[a], names[b], round(km, 1)])
        i = j + 1
    res[L].append(dict(o=names[0], d=names[-1], trips=n, stretches=stretches, stops=[[nm, round(x)] for nm, x in zip(names, m)]))
save(dict(lines=res, osm=S['osm_date'], tolerance_m=tol), os.path.join(DER, S['name'], 'offwire.json'))
for L, ps in res.items():
    for p in ps:
        if p['stretches'] and p['trips'] >= 5: print(L.rjust(3), p['trips'], f"{p['o']} -> {p['d']}", p['stretches'])
