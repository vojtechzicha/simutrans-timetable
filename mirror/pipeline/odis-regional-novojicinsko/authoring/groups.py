"""compact whole-day view per line: trips grouped by first -> last stop (alias applied), with departure times and the
stop count; groups.py L[,L2...] [--stops] (--stops prints each group's commonest stop list)"""
import os, sys, collections
os.environ.setdefault('ODIS_BASE', os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'odis-regional-hko', 'scripts'))
from lib import load, nm, AL, hm
T = load('trips.json'); C = load('line_class.json')
for L in sys.argv[1].split(','):
    tr = sorted(T.get(L, []), key=lambda t: t['dep'])
    print(f"== {L} {C[L]['name'][:70]} | {C[L]['lics']} | {len(tr)} trips")
    g = collections.defaultdict(list)
    for t in tr:
        st = [AL(nm(x)) for x in t['stops']]
        g[(st[0], st[-1])].append((t, st))
    for (a, b), xs in sorted(g.items(), key=lambda kv: kv[1][0][0]['dep']):
        paths = collections.Counter(tuple(s) for _, s in xs)
        print(f"  {a} -> {b} [{len(xs)}; {len(paths)} paths; rt {xs[0][0]['times'][-1]-xs[0][0]['times'][0]}]: " + ' '.join(hm(t['dep']) for t, _ in xs))
        if '--stops' in sys.argv:
            for p, n in paths.most_common(3): print(f"      {n}x: " + ' > '.join(x.split(', ', 1)[-1][:18] for x in p))
