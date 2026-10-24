"""The fleet registers of a sheet's carriers (config.fleet) -> data/raw/<snapshot>/fleet/*.html and data/derived/fleet.json,
in the Havířov/Karviná/Orlová fleet.json shape {fleet number: {state, num, type, year, note, plate, vid, cat, full, len,
paint}}, so 04_roster reads it through config.live.fleet. Only for sheets whose carriers that register does not hold
(Z-Group bus, Transdev Morava, MDPO); the HKO and TFJ sheets use the Transdev Slezsko list of the Havířov pipeline.

config.fleet = {carriers: [{id, name, tractions: [autobus, elektrobus, ...], live_plate?: 'MDPO{num}'}]}
- seznam-autobusu register pages /seznam?prov=1&trakce=<t>&iddopravce=<id>&vcetneSluzebnich=1&page=N, kept on disk (a rebuild
  makes no request; --refresh fetches again).
- live_plate: a carrier whose buses send no number plate to the live map but a code with the fleet number (MDPO307): the
  entry's plate is that code (the register plate stays in reg_plate), so the live join works by plate as everywhere else.
- A fleet number two carriers share gets the carrier's name after it.
"""
import collections, glob, json, os, re, sys
from lib import CONFIG, RAW, save, tramlib, plate_key, tlen

F = CONFIG.get('fleet')
if not F: sys.exit(print('no config.fleet: this sheet reads config.live.fleet as it is'))
D = os.path.join(RAW, 'fleet'); os.makedirs(D, exist_ok=True)
for c in F['carriers']:
    for t in c.get('tractions', ['autobus']):
        p = 1
        while True:
            fn = os.path.join(D, f"{c['id']}_{t}_p{p}.html")
            if not os.path.exists(fn) or '--refresh' in sys.argv:
                s = tramlib.http(f"https://seznam-autobusu.cz/seznam?prov=1&trakce={t}&iddopravce={c['id']}&vcetneSluzebnich=1&page={p}")
                open(fn, 'w', encoding='utf-8').write(s); print('fetched', os.path.basename(fn))
            s = open(fn, encoding='utf-8').read()
            if not tramlib.next_page(s, p): break
            p += 1


fleet = {}
for c in F['carriers']:
    for fn in sorted(glob.glob(os.path.join(D, f"{c['id']}_*.html"))):
        s = open(fn, encoding='utf-8').read()
        cars = tramlib.parse_fleet_list(s)
        for vid, x in cars.items():
            if not x['num']: continue
            m = re.search(r'data-car-id="%s">\s*<td class=\'plates\'>(.*?)</td>' % vid, s, flags=re.S)
            plate = plate_key(tramlib._clean(m.group(1))) if m else ''
            paint = re.search(r'nátěr:\s*([^*{]*)', x['note'])
            e = dict(x, vid=vid, carrier=c['name'], cat=x['type'], full=x['type'], len=tlen(x['type']), plate=plate,
                     paint=re.sub(r'\s+', ' ', paint.group(1)).strip(' *') if paint else '')
            if c.get('live_plate'): e['reg_plate'] = plate; e['plate'] = plate_key(c['live_plate'].format(num=x['num']))
            k = x['num'] if x['num'] not in fleet else f"{x['num']} ({c['name']})"
            fleet[k] = e
save('fleet.json', fleet)
print('fleet', len(fleet), dict(collections.Counter((v['carrier'], v['state']) for v in fleet.values())))
