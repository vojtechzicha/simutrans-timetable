"""chosen diversion versions vs the regular version: stops dropped/added and trip counts on the vehicle day"""
import os, sys, re
os.environ['ODIS_BASE'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'odis-regional-hko', 'scripts'))
from lib import CONFIG, rel, jdf_open, pick_version, jdf_tables, jdf_trips, day, load
V = load('versions.json'); d = day(CONFIG['vehicle_day'])
outer = jdf_open(rel(CONFIG['jdf']['zip']))
def stops(v):
    tb = jdf_tables(outer, v['inner'])
    tb['Caskody'] = [r for r in tb['Caskody'] if len(r) >= 7 and re.fullmatch(r'\d{8}', r[5])]
    tr = jdf_trips(tb, d)
    return tr, {s for t in tr for s in t['stops']}
for code, v in sorted(V['chosen'].items()):
    if not v['diversion']: continue
    regs = [x for x in V['all'] if x['lic'] == code and not x['diversion']]
    r = pick_version(regs, d)
    tv, sv = stops(v)
    print(f"{code} DIV {v['valid_from']}–{v['valid_to']} {len(tv)} trips | regular valid on day: {r['valid_from'] + '–' + r['valid_to'] if r else None}", end='')
    if not r: print(); continue
    tr_, sr = stops(r)
    print(f" {len(tr_)} trips | dropped {sorted(sr - sv)[:6]} added {sorted(sv - sr)[:6]}")
