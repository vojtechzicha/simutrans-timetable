"""each chosen diversion version: stops dropped/added vs the regular version valid on the day (for the network state)"""
import os, sys, re
HERE = os.path.dirname(os.path.abspath(__file__))
os.environ['ODIS_BASE'] = os.path.join(HERE, '..')
sys.path.insert(0, os.path.join(HERE, '..', '..', 'odis-regional-hko', 'scripts'))
from lib import CONFIG, rel, jdf_open, pick_version, jdf_tables, jdf_trips, day, load, hm
V = load('versions.json'); d = day(CONFIG['vehicle_day'])
outers = [jdf_open(rel(z)) for z in [CONFIG['jdf']['zip']] + CONFIG['jdf'].get('extra_zips', [])]
def stops(v):
    tb = jdf_tables(outers[v.get('zip', 0)], v['inner'])
    tb['Caskody'] = [r for r in tb['Caskody'] if len(r) >= 7 and re.fullmatch(r'\d{8}', r[5])]
    tr = jdf_trips(tb, d); return tr, {s for t in tr for s in t['stops']}
for code, v in sorted(V['chosen'].items()):
    if not v['diversion']: continue
    regs = [x for x in V['all'] if x['lic'] == code and not x['diversion']]
    r = pick_version(regs, d)
    tv, sv = stops(v)
    print(f"\n{code} {v['name'][:60]} DIVERSION {v['valid_from']}–{v['valid_to']} ({len(tv)} trips)")
    if not r: print('   no regular version valid on the day:', [(x['valid_from'], x['valid_to']) for x in regs]); continue
    tr_, sr = stops(r)
    print(f"   regular {r['valid_from']}–{r['valid_to']} ({len(tr_)} trips); dropped {sorted(sr - sv)}; added {sorted(sv - sr)}")
