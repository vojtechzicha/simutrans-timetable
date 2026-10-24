"""stops of the trips of a line that pass a given stop: stops.py L 'substring' [HH:MM-HH:MM]"""
import os, sys
os.environ.setdefault('ODIS_BASE', os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'odis-regional-hko', 'scripts'))
from lib import load, nm, hm, AL
T = load('trips.json'); L, sub = sys.argv[1], sys.argv[2]
for t in sorted(T[L], key=lambda t: t['dep']):
    st = [AL(nm(s)) for s in t['stops']]
    if not any(sub in s for s in st): continue
    print(f"{hm(t['dep'])}: " + ' > '.join(f"{s.split(', ', 1)[-1][:18]} {hm(x)}" for s, x in zip(st, t['times'])))
