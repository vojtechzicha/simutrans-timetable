"""per line: the (from, to) pairs of its trips on the vehicle day with departure times, afternoon ones marked: ends.py L[,L2]"""
import os, sys, collections
os.environ['ODIS_BASE'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'odis-regional-hko', 'scripts'))
from lib import load, nm, AL, hm
T = load('trips.json'); C = load('line_class.json')
for L in sys.argv[1].split(','):
    tr = T.get(L, [])
    print(f"== {L} {C[L]['name'][:70]} ({len(tr)} trips, {C[L]['lics']})")
    g = collections.defaultdict(list)
    for t in tr: g[(AL(nm(t['fr'])), AL(nm(t['to'])))].append(t['dep'])
    for (a, b), ds in sorted(g.items(), key=lambda x: -len(x[1])):
        print(f"   {len(ds):3} {a[:34]:34} > {b[:34]:34} " + ' '.join(('*' if 780 <= d < 1140 else '') + hm(d) for d in sorted(ds)))
