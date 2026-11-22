"""The PID operators the praha-bus register of 29 Sep 2026 does not cover, read on 22 Nov 2026:
python register_2026_11_22.py -> data/derived/register_2026-11-22.json  ({car id: operator, garage, number, type, source})

Owner, 22 Nov 2026: "The PID files do not say which Arriva City - only arriva city. Look at prague local buses, do it everywhere
with the proper amount of information." The 29 Sep register holds the Prague city operators only, and seznam-autobusu.cz has
answered scripted requests with HTTP 429 since 1 Nov; on 22 Nov the owner's own Chrome (Claude in Chrome) loads it, so the pages
were read there, 2 s apart, and only what the sheets need was kept (data/raw/register/2026-11-22/browser_read.json):
- lists: seznam?iddopravce=<id>&trakce=autobus&prov=1&vcetneSluzebnich=1&page=N of 32 operators (their ids found from one vehicle
  card each), every bus on a PID sheet that the 29 Sep register lacks: [operator id, depot code, number, maker and type];
- codes: one vehicle card per (operator, depot code), its current depot ("<name> <since>-dosud") = the code's full name;
- cards: the vehicle card of every such bus no list holds (operators with no register list, buses sold since): operator, depot, type.
06_render.py shows the garage only where the operator here is the live map's operator.
"""
import json, os
from common import HOME, RAW

src = json.load(open(os.path.join(RAW, 'register', '2026-11-22', 'browser_read.json'), encoding='utf-8'))
names = {str(k): v for k, v in src['operators'].items()}          # operator id -> the live map's operator name
out = {}
for cid, (op, code, num, mt) in src['cars'].items():
    out[cid] = dict(operator=names[str(op)], garage=src['codes'].get(f'{op}|{code}', '') if code else '', num=num, maker_type=mt,
                    code=code, source='list 22 Nov 2026')
for cid, c in src['cards'].items():
    out[cid] = dict(operator=c['op'], garage=c['depot'], num='', maker_type=c['type'], code='', source='vehicle card 22 Nov 2026')
# buses whose live-map vehicle card had no register link: found by fleet number in their operator's list ("num:<operator>|<num>")
bt = json.load(open(os.path.join(HOME, '..', 'praha-bus', 'assets', 'bus_types.json'), encoding='utf-8'))
for key, (cid, code, mt) in src.get('by_number', {}).items():
    op, num = key.split('|', 1)
    name = src['codes'].get(f'{op}|{code}') or {**bt['garages'], **bt['garages_by_operator'].get(names[op], {})}.get(code, '')
    out[f'num:{names[op]}|{num}'] = dict(operator=names[op], garage=name if code else '', num=num, maker_type=mt, code=code, car_id=cid,
                                         source='list 22 Nov 2026, by fleet number')
# buses whose 29 Sep register entry names another operator (sold or moved since): their current vehicle card
for cid, c in src.get('moved_cards', {}).items():
    out[cid] = dict(operator=c['op'], garage=c['depot'], num='', maker_type=c['type'], code='', source='vehicle card 22 Nov 2026 (operator changed)')
missing = sorted({f'{names[str(op)]} {code}' for op, code, *_ in src['cars'].values() if code and not src['codes'].get(f'{op}|{code}')})
dst = os.path.join(HOME, 'data', 'derived', 'register_2026-11-22.json')
json.dump(out, open(dst, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(out), 'buses;', sum(1 for v in out.values() if v['garage']), 'with a garage;', dst)
if missing: print('WARNING depot codes without a name:', ', '.join(missing))
