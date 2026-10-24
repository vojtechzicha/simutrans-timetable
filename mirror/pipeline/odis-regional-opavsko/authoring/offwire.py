"""Off-wire (battery / auxiliary drive) sections of the Opava trolleybus routes: OSM route relations against the OSM wire.

  input   data/raw/osm/<osm>/trolleybus_routes.json  (Overpass: relation["route"="trolleybus"](Opava box); out geom;)
          data/raw/osm/<osm>/trolley_wire.json       (Overpass: way["trolley_wire"="yes"](Opava box); out geom tags;)
          data/raw/osm/<osm>/stops.json              (Overpass: bus_stop / platform / stop_position nodes; out body;)
  output  data/derived/offwire.json  {line: [dict(o, d, km, off_km, stretches=[[from stop, to stop, km, km with no wire]], sections=[...])]}

Same test as pipeline/praha-trolleybus/scripts/03b_offwire.py, with the OSM route relation as the path (the JDF has no
shapes): the path is sampled every 10 m, a sample is under the wire if a trolley_wire way lies within 25 m, and a
stop-to-stop section is off-wire when under a third of its samples are. Stops are the relation's stop/platform members,
placed on the path by projection.

Usage: python authoring/offwire.py [--osm 2026-10-22]
"""
import argparse, collections, json, math, os
HERE = os.path.dirname(os.path.abspath(__file__)); BASE = os.path.dirname(HERE)
TOL = 25

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--osm', default='2026-10-22'); a = ap.parse_args()
    raw = os.path.join(BASE, 'data', 'raw', 'osm', a.osm)
    ld = lambda f: json.load(open(os.path.join(raw, f), encoding='utf-8'))['elements']
    lat0 = math.radians(49.94)
    xy = lambda p: (math.radians(p['lon']) * 6371000 * math.cos(lat0), math.radians(p['lat']) * 6371000)
    grid = collections.defaultdict(list)
    for e in ld('trolley_wire.json'):
        pts = [xy(p) for p in e.get('geometry', [])]
        for p, q in zip(pts, pts[1:]):
            for gx in range(int(min(p[0], q[0]) // 100) - 1, int(max(p[0], q[0]) // 100) + 2):
                for gy in range(int(min(p[1], q[1]) // 100) - 1, int(max(p[1], q[1]) // 100) + 2):
                    grid[(gx, gy)].append((p, q))
    def dist(p, s, t):
        dx, dy = t[0] - s[0], t[1] - s[1]; L = dx * dx + dy * dy
        u = 0 if L == 0 else max(0, min(1, ((p[0] - s[0]) * dx + (p[1] - s[1]) * dy) / L))
        return math.hypot(p[0] - s[0] - u * dx, p[1] - s[1] - u * dy)
    under = lambda p: any(dist(p, s, t) <= TOL for s, t in grid.get((int(p[0] // 100), int(p[1] // 100)), ()))
    names = {e['id']: e.get('tags', {}).get('name') for e in ld('stops.json')}

    res = collections.defaultdict(list)
    for r in ld('trolleybus_routes.json'):
        t = r['tags']
        # path: member ways in relation order, each flipped to continue from the previous end
        ways = [[xy(p) for p in m['geometry']] for m in r['members'] if m['type'] == 'way' and m.get('role') in ('', None)]
        D = lambda p, q: math.hypot(p[0] - q[0], p[1] - q[1])
        if len(ways) > 1 and min(D(ways[0][0], ways[1][0]), D(ways[0][0], ways[1][-1])) < min(D(ways[0][-1], ways[1][0]), D(ways[0][-1], ways[1][-1])):
            ways[0] = ways[0][::-1]      # the first way is stored against the direction of travel
        path = []
        for g in ways:
            if path and D(g[-1], path[-1]) < D(g[0], path[-1]): g = g[::-1]
            path += g if not path else g[1:]
        cum = [0.0]
        for p, q in zip(path, path[1:]): cum.append(cum[-1] + math.hypot(q[0] - p[0], q[1] - p[1]))
        def proj(p):
            best = (1e18, 0)
            for i, (s, q) in enumerate(zip(path, path[1:])):
                d = dist(p, s, q)
                if d < best[0]:
                    dx, dy = q[0] - s[0], q[1] - s[1]; L = dx * dx + dy * dy
                    u = 0 if L == 0 else max(0, min(1, ((p[0] - s[0]) * dx + (p[1] - s[1]) * dy) / L))
                    best = (d, cum[i] + u * math.sqrt(L))
            return best
        stops = []
        for m in r['members']:
            if m['type'] == 'node' and m.get('role', '').startswith(('stop', 'platform')):
                n = names.get(m['ref']) or '?'
                d, at = proj(xy(m))
                if not stops or stops[-1][0] != n: stops.append([n, at, round(d)])
                else: stops[-1][1] = min(stops[-1][1], at)
        # samples every 10 m along the path
        smp = []
        for i, (p, q) in enumerate(zip(path, path[1:])):
            L = cum[i + 1] - cum[i]; k = max(1, int(L // 10))
            for j in range(k):
                u = j / k; smp.append((cum[i] + u * L, under((p[0] + u * (q[0] - p[0]), p[1] + u * (q[1] - p[1])))))
        secs = []
        for (sa, da, _), (sb, db, _) in zip(stops, stops[1:]):
            ss = [w for d, w in smp if da <= d <= db]
            frac = sum(ss) / len(ss) if ss else 1
            secs.append(dict(a=sa, b=sb, km=round((db - da) / 1000, 3), wire=frac >= 1 / 3, frac=round(frac, 2)))
        # ends of the path beyond the first / last stop (terminal loops)
        head = [w for d, w in smp if d < stops[0][1]] if stops else []
        tail = [w for d, w in smp if d > stops[-1][1]] if stops else []
        stretches, cur = [], None
        for x in secs:
            if not x['wire']:
                if cur: cur[1] = x['b']; cur[2] += x['km']
                else: cur = [x['a'], x['b'], x['km']]
            elif cur: stretches.append(cur); cur = None
        if cur: stretches.append(cur)
        at = {n: d for n, d, _ in stops}
        # the wire itself: metres of the stretch with no wire within TOL (a stretch's end sections can be partly wired)
        for st in stretches: st.append(round(sum(10 for d, w in smp if at[st[0]] <= d <= at[st[1]] and not w) / 1000, 1))
        tot = sum(x['km'] for x in secs); off = sum(x['km'] for x in secs if not x['wire'])
        res[t.get('ref')].append(dict(osm=r['id'], o=t.get('from'), d=t.get('to'), km=round(tot, 1), off_km=round(off, 1),
                                      path_km=round(cum[-1] / 1000, 1), wire_share=round(sum(w for _, w in smp) / max(1, len(smp)), 2),
                                      head_off=round(sum(not w for w in head) * 10), tail_off=round(sum(not w for w in tail) * 10),
                                      stretches=[[x, y, round(k, 1), w] for x, y, k, w in stretches], stops=stops, sections=secs))
    # Ends the relation leaves out (both 204 relations are complete=no and stop at Kylešovice, Bílovecká): the modelled
    # line's own stops beyond the relation's first / last stop. Such a stop is off the wire when every OSM platform of
    # that name is over 60 m from it; the stretch runs from it to the relation's end stop, measured in a straight line
    # between the stops' platforms (a lower bound for the road).
    key = lambda s: ''.join(ch for ch in s.lower().replace('opava,', '', 1) if ch.isalnum())
    pts = collections.defaultdict(list)
    for e in ld('stops.json'):
        if e.get('tags', {}).get('name') and e['tags'].get('public_transport') == 'platform': pts[key(e['tags']['name'])].append(xy(e))
    near = lambda k: min((min((dist(p, s, t) for s, t in grid.get((int(p[0] // 100), int(p[1] // 100)), ())), default=1e9) for p in pts[k]), default=None)
    S = json.load(open(os.path.join(BASE, 'data', 'derived', 'schedule.json'), encoding='utf-8'))
    for L, ps in res.items():
        for p in ps:
            ks = [key(n) for n, _, _ in p['stops']]
            for sm in S.get(L, {}).get('sim', []):
                for g in sm['legs']:
                    js = g['stops']; jk = [key(z) for z in js]
                    if not (key(p['o']) in jk or ks[0] in jk) or jk[-1] == ks[0] or jk[0] == ks[-1]: continue
                    for side in ('head', 'tail'):
                        end = ks[0] if side == 'head' else ks[-1]
                        if end not in jk: continue
                        i = jk.index(end)
                        extra = js[:i] if side == 'head' else js[i + 1:]
                        if not extra or (side == 'head' and jk[0] != key(p['o']) and key(p['o']) not in jk[:i]): continue
                        if side == 'tail' and key(p['d']) not in jk[i + 1:]: continue
                        far = [z for z in extra if (near(key(z)) or 0) > 60]
                        if len(far) != len(extra): continue
                        seq = extra + [js[i]] if side == 'head' else [js[i]] + extra
                        km = sum(math.hypot(pts[key(b)][0][0] - pts[key(a)][0][0], pts[key(b)][0][1] - pts[key(a)][0][1]) for a, b in zip(seq, seq[1:])) / 1000
                        names = [z.replace('Opava, ', '', 1) for z in seq]
                        st = [names[0], names[-1], round(km, 1), round(km, 1)]
                        if st in p['stretches']: continue
                        p['stretches'] = ([st] if side == 'head' else []) + p['stretches'] + ([st] if side == 'tail' else [])
                        p['off_km'] = round(p['off_km'] + km, 1); p['km'] = round(p['km'] + km, 1)
                        p.setdefault('added', []).append(dict(side=side, stops=names, km=round(km, 2), wire_m={z: (round(near(key(z))) if near(key(z)) < 1e8 else '>100') for z in extra},
                                                              why='not in the OSM relation (complete=no); stops from the timetable, wire distance from the OSM stops'))
    out = dict(lines=res, osm=a.osm, tolerance_m=TOL)
    json.dump(out, open(os.path.join(BASE, 'data', 'derived', 'offwire.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    for L, ps in sorted(res.items()):
        for p in ps:
            print(L, f"{p['o']} -> {p['d']}", p['km'], 'km (path', p['path_km'], ') wire', p['wire_share'], 'off', p['off_km'], p['stretches'],
                  'ends off m', p['head_off'], p['tail_off'])
            for s in p['sections']:
                if s['frac'] < 0.9: print('    ', s)

if __name__ == '__main__':
    main()
