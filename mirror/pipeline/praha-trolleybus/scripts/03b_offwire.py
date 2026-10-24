"""Off-wire (battery) sections of every trolleybus route: GTFS shapes against the OpenStreetMap overhead wire.

  input   data/raw/gtfs/<raw>/gtfs.zip (shapes + stop_times.shape_dist_traveled)
          data/raw/osm/<osm.raw>/trolley_wire.json (Overpass: way["trolley_wire"="yes"] in the Prague box, out geom)
  output  data/derived/<state>/offwire.json  {line: [dict(o, d, km, off_km, stretches=[[from stop, to stop, km]], stops=[...])]}

Method: every stop-to-stop section of the pattern's shape is sampled every 10 m; a sample is under the wire if an OSM
trolley_wire way lies within `osm.tolerance_m` (default 25 m, which covers the road width and GTFS/OSM offsets).
A section is off-wire when under a third of its samples are under the wire. Consecutive off-wire sections are joined
into stretches named by their first and last stop. Terminus loops without wire in OSM show up as a short off-wire end.

Usage: python 03b_offwire.py --state 2026-09-27
"""
import argparse, collections, csv, io, json, math, os, zipfile
from common import state, load, save, RAW, DER

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--state', required=True)
    s = state(ap.parse_args().state); g = s['gtfs']; osm = s['osm']
    tol = osm.get('tolerance_m', 25)
    alias = s.get('stop_aliases', {}); n = lambda x: alias.get(x, x)
    lat0 = math.radians(50.08)
    xy = lambda la, lo: (math.radians(lo) * 6371000 * math.cos(lat0), math.radians(la) * 6371000)
    # wire segments in a 100 m grid
    W = load(os.path.join(RAW, 'osm', osm['raw'], 'trolley_wire.json'))['elements']
    grid = collections.defaultdict(list)
    for e in W:
        pts = [xy(p['lat'], p['lon']) for p in e.get('geometry', [])]
        for a, b in zip(pts, pts[1:]):
            for gx in range(int(min(a[0], b[0]) // 100) - 1, int(max(a[0], b[0]) // 100) + 2):
                for gy in range(int(min(a[1], b[1]) // 100) - 1, int(max(a[1], b[1]) // 100) + 2):
                    grid[(gx, gy)].append((a, b))
    def dist(p, a, b):
        dx, dy = b[0] - a[0], b[1] - a[1]; L = dx * dx + dy * dy
        t = 0 if L == 0 else max(0, min(1, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / L))
        return math.hypot(p[0] - a[0] - t * dx, p[1] - a[1] - t * dy)
    under = lambda p: any(dist(p, a, b) <= tol for a, b in grid.get((int(p[0] // 100), int(p[1] // 100)), ()))

    z = zipfile.ZipFile(os.path.join(RAW, 'gtfs', g['raw'], 'gtfs.zip'))
    rd = lambda f: csv.DictReader(io.TextIOWrapper(z.open(f), encoding='utf-8-sig'))
    rt = s.get('route_type', '11')
    routes = {r['route_id']: r['route_short_name'] for r in rd('routes.txt') if r['route_type'] == rt}
    trips = {t['trip_id']: t for t in rd('trips.txt') if t['route_id'] in routes}
    stops = {r['stop_id']: r['stop_name'] for r in rd('stops.txt')}
    st = collections.defaultdict(list)
    for r in rd('stop_times.txt'):
        if r['trip_id'] in trips: st[r['trip_id']].append((int(r['stop_sequence']), r['stop_id'], float(r['shape_dist_traveled'] or 0)))
    # one representative trip per (line, stop sequence); keep the sequence used most
    pat = collections.Counter(); rep = {}
    for tid, rs in st.items():
        rs.sort(); k = (routes[trips[tid]['route_id']], tuple(x[1] for x in rs)); pat[k] += 1; rep[k] = (trips[tid]['shape_id'], rs)
    need = {rep[k][0] for k in pat}
    shp = collections.defaultdict(list)
    for r in rd('shapes.txt'):
        if r['shape_id'] in need: shp[r['shape_id']].append((int(r['shape_pt_sequence']), float(r['shape_dist_traveled']), xy(float(r['shape_pt_lat']), float(r['shape_pt_lon']))))
    for v in shp.values(): v.sort()
    def sample(sid, d0, d1):
        pts = shp[sid]; out = []
        for (_, da, pa), (_, db, pb) in zip(pts, pts[1:]):
            if db < d0 or da > d1 or db == da: continue
            seg = math.hypot(pb[0] - pa[0], pb[1] - pa[1]); k = max(1, int(seg // 10))
            for i in range(k):
                t = i / k; d = da + t * (db - da)
                if d0 <= d <= d1: out.append((pa[0] + t * (pb[0] - pa[0]), pa[1] + t * (pb[1] - pa[1])))
        return out
    res = collections.defaultdict(list)
    for (L, seq), cnt in pat.most_common():
        sid, rs = rep[(L, seq)]
        # PID shape_dist_traveled is in km
        secs = []
        for (_, a, da), (_, b, db) in zip(rs, rs[1:]):
            smp = sample(sid, da, db); frac = sum(map(under, smp)) / len(smp) if smp else 1
            secs.append(dict(a=stops[a], b=stops[b], km=round(db - da, 3), wire=frac >= 1 / 3, frac=round(frac, 2)))
        stretches, cur = [], None
        for x in secs:
            if not x['wire']:
                if cur: cur[1] = x['b']; cur[2] += x['km']
                else: cur = [x['a'], x['b'], x['km']]
            elif cur: stretches.append(cur); cur = None
        if cur: stretches.append(cur)
        tot = sum(x['km'] for x in secs); off = sum(x['km'] for x in secs if not x['wire'])
        res[L].append(dict(o=n(stops[seq[0]]), d=n(stops[seq[-1]]), trips=cnt, km=round(tot, 1), off_km=round(off, 1),
                           stretches=[[a, b, round(k, 1)] for a, b, k in stretches], sections=secs))
    save(dict(lines=res, osm=osm['raw'], tolerance_m=tol), os.path.join(DER, s['name'], 'offwire.json'))
    for L, ps in res.items():
        for p in ps:
            print(L.rjust(3), p['trips'], f"{p['o']} -> {p['d']}", p['km'], 'km, off', p['off_km'], p['stretches'])

if __name__ == '__main__':
    main()
