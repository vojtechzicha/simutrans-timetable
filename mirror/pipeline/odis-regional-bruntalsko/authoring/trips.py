"""compact whole-day trip list of lines: trips.py L[,L2...] — time, from > to, arrival, stops count, path signature"""
import os, sys, json, collections
os.environ.setdefault('ODIS_BASE', os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'odis-regional-hko', 'scripts'))
from lib import load, nm, hm, AL
T = load('trips.json')
for L in sys.argv[1].split(','):
    tr = sorted(T.get(L, []), key=lambda t: t['dep'])
    ends = collections.Counter((AL(nm(t['fr'])), AL(nm(t['to']))) for t in tr)
    print(f"== {L}: {len(tr)} trips; ends:", '; '.join(f"{a.split(', ',1)[-1][:22]}>{b.split(', ',1)[-1][:22]} {n}" for (a, b), n in ends.most_common(6)))
    for t in tr:
        print(f"   {hm(t['dep']):>5} {AL(nm(t['fr']))[:34]:34} > {AL(nm(t['to']))[:34]:34} {hm(t['times'][-1]):>5} ({len(t['stops'])})")
