"""Register (data/raw/register/2026-11-23/browser_read.json) + live poll -> data/derived/fleet.json, keyed like live_compact.json.

The VDV live map names a bus by its VDV vehicle number (ICOM 3-4515, ČSAD AUTOBUSY ČB 64-10021); for the ČSAD buses it also
shows a second row with the number plate, which 01_live.py pairs (plate_to_fleet). The register (seznam-autobusu.cz, read in
the owner's Chrome on 23 Nov 2026) has no fleet numbers for either operator, only plates. So:
- a VDV number paired with a plate takes that plate's register entry (type, year, paint, depot);
- a plate seen alone is its own key;
- a VDV number with no plate (the ICOM town buses on 23 Nov) is entered with type '?' and the note that the map gave no
  plate; config.vdv_numbers {VDV number: plate} names it once known.
Shape as the Havířov/Karviná/Orlová fleet.json: {key: {num, plate, reg_plate, type, cat, full, len, year, paint, note, state,
depot, operator, car_id}}.
"""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
C = json.load(open(os.path.join(ROOT, 'config.json'), encoding='utf-8'))
reg = json.load(open(os.path.join(ROOT, 'data', 'raw', 'register', '2026-11-23', 'browser_read.json'), encoding='utf-8'))
lc = os.path.join(ROOT, 'data', 'raw', C['snapshot'], 'live_compact.json')
live = json.load(open(lc, encoding='utf-8')) if os.path.exists(lc) else dict(plates={}, plate_to_fleet={})
byplate = {c['plate']: c for c in reg['cars']}
p2f = dict(live.get('plate_to_fleet', {})); f2p = {f: p for p, f in p2f.items()}
f2p.update(C.get('vdv_numbers', {}))
def length(ty):
    m = re.search(r'(\d+)[,.](\d)\s*M\b', ty) or re.search(r'\b(\d{2})M\b', ty)
    if m: return f"{m.group(1)}.{m.group(2)} m" if m.lastindex == 2 else f"{m.group(1)} m"
    if 'NOVO Citi Life' in ty: return '7.5 m (midibus)'
    if 'Setra S 415' in ty: return '12.2 m'
    return '?'
def entry(key, c, vdv=None):
    ty = c['type']
    return dict(num=key, plate=key, reg_plate=c['plate'][:3] + ' ' + c['plate'][3:], vdv=vdv, type=ty, cat=ty, full=ty, len=length(ty),
                year=c['year'], paint=c['paint'], note='', state='zar', depot=c['depot'], operator=c['operator'], car_id=c['car_id'])
fleet = {}
for key in live.get('plates', {}):
    pl = f2p.get(key) or (key if key in byplate else None)
    if pl and pl in byplate: fleet[key] = entry(key, byplate[pl], vdv=key if key != pl else None); continue
    fleet[key] = dict(num=key, plate=key, reg_plate='', vdv=key, type='?', cat='?', full='type not known (the live map gives no plate for this bus)',
                      len='?', year='', paint='', note='VDV vehicle number; the register (seznam-autobusu) lists plates only', state='zar',
                      depot='', operator='', car_id='')
json.dump(fleet, open(os.path.join(ROOT, 'data', 'derived', 'fleet.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('fleet', len(fleet), 'buses seen;', sum(1 for v in fleet.values() if v['type'] != '?'), 'with their register entry')
