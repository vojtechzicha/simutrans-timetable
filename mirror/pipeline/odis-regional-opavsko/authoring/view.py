"""compact whole-day view of one or more lines at given core points: view.py L[,L2] CODE=stop-substring ..."""
import sys, json, collections
import os
os.environ['ODIS_BASE'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'odis-regional-hko', 'scripts'))
from lib import load, nm, hm
T = load('trips.json'); R = load('reading.json')
lines = sys.argv[1].split(','); codes = []
for a in sys.argv[2:]:
    c, s = a.split('=', 1); codes.append((c, s))
def code_of(stop):
    for c, s in codes:
        if s == stop or (s.endswith('*') and stop.startswith(s[:-1])): return c
    return None
rows = []
for L in lines:
    for r in R[L]['rows']:
        seq = []
        for st, tm in zip(r['stops'], [None] * len(r['stops'])): pass
        t = next(t for t in T[L] if t['sp'] == r['sp'] and t['lic'] == r['lic'])
        cells = []
        for st, tm in zip([nm(x) for x in t['stops']], t['times']):
            c = code_of(st)
            if c and (not cells or cells[-1][0] != c): cells.append((c, tm))
        obs = ' '.join(o[0] for o in r['obs'])
        key = '>'.join(c for c, _ in cells)
        rows.append((t['dep'], L, r['sp'], cells, len(r['stops']), obs, nm(t['fr']), nm(t['to'])))
rows.sort()
for dep, L, sp, cells, n, obs, fr, to in rows:
    s = ' '.join(f"{c}{hm(tm)}" for c, tm in cells)
    ex = ''
    if not cells or code_of(fr) is None: ex += f" [from {fr}]"
    if not cells or code_of(to) is None: ex += f" [to {to}]"
    print(f"{L}/{sp:<3} {s:60} n{n}{ex}  {obs}")
