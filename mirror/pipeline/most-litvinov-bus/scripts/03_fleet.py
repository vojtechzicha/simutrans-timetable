"""Raw register, car pages, record pages and photo pages -> derived/fleet.json, evidence.json, records.json.

fleet.json     {number: {cid, state, num, gen, type, year, plates, depot_code, depot, paint, note, full, length,
                         city (True = a city bus of the Most or Litvínov garage, usable on the sheet), why_not}}
               The register lists 96 vehicles in service (prov=1). City buses are those of the Most (Mos) and
               Litvínov (Lit) garages in state "zar" (in service); the coach and contract fleet (ZD-M, ZD-L), service
               vehicles, museum buses and the two driving-school buses are not.
records.json   every seznam-autobusu record of a DPmML line, from the per-line lists (/vypravenost/cr/vypis?linka=
               <JDF number>) and from the cars' own pages: [{line, car, date, weekday, kurz, note, how}]. The old
               records name the bus by its registration plate only; plates are matched to register cars.
               The day overview of config.vehicle_day is checked for any DPmML line (none on 25 Sep 2026).
evidence.json  per car: records on DPmML lines, the photo list (date, place) and the lines read off photo displays
               (assets/photo_lines.json, read by eye), used by 04_roster.py to place designed buses.
"""
import collections, glob, json, os, re
from lib import CONFIG, raw, clean, parse_fleet_list, parse_vypravenost, record_date, save, asset

C = CONFIG; F = C['fleet']; TR = asset('types.json')
ROMAN = re.compile(r'^(\d+)\s*([IVX]+)?$')

# ---- register
fleet = {}; bycid = {}
for f in sorted(glob.glob(os.path.join(raw('fleet'), 'p*.html'))):
    s = open(f, encoding='utf-8').read()
    for cid, c in parse_fleet_list(s).items():
        m = re.search(r'data-car-id="%s">\s*<td class=\'plates\'>(.*?)</td>.*?<td class="depots">(.*?)</td>' % cid, s, flags=re.S)
        plates = re.findall(r'[0-9A-Z]{3} ?[0-9A-Z]{4}', clean(m.group(1))) if m else []
        dep = re.sub(r'[\s*]', '', clean(m.group(2))) if m else ''
        mm = ROMAN.match(c['num'])
        paint = re.search(r'nátěr:\s*(.*?)\s*\*?$', c['note']); paint = paint.group(1).strip(' *') if paint else ''
        rule = TR['types'].get(c['type'])
        car = dict(cid=cid, state=c['state'], num=c['num'], gen=(mm.group(2) or '') if mm else '', type=c['type'], year=c['year'],
                   plates=plates, depot_code=dep, depot=F['depots'].get(dep, F['other_depot_codes'].get(dep, dep)), paint=paint,
                   note=c['note'], full=rule['full'] if rule else c['type'], length=rule['length'] if rule else '?')
        why = []
        if c['state'] != 'zar': why.append({'sluz': 'service vehicle', 'muz': 'museum bus'}.get(c['state'], c['state']))
        if dep not in F['depots']: why.append(car['depot'])
        if 'autoškol' in c['note']: why.append('driving-school bus')
        if not rule and not why: why.append('not a city bus type (assets/types.json)')
        for k, v in TR.get('not_city', {}).items():
            if mm and mm.group(1) == k: why.append(v)
        car['city'] = not why; car['why_not'] = '; '.join(why)
        car['weekend_only'] = bool(mm) and mm.group(1) in TR.get('weekend_only', [])
        bycid[cid] = car
        if mm: fleet[int(mm.group(1))] = car
plate2car = {p.replace(' ', ''): n for n, c in fleet.items() for p in c['plates']}
print('register', len(bycid), 'numbered', len(fleet), 'city buses', sum(c['city'] for c in fleet.values()))
print(collections.Counter((c['type'], c['depot_code']) for c in fleet.values() if c['city']))

# ---- records: per-line lists and the cars' own pages
codes = {c: str(int(c[3:])) for c in C['jdf']['all_codes']}
recs = []; seen = set()
def add(line_code, car, date, kurz, note, how):
    d = record_date(date)
    k = (line_code, car, d)
    if not d or k in seen: return
    seen.add(k)
    recs.append(dict(line=codes.get(line_code, line_code), code=line_code, car=car, date=d.isoformat(), weekday=date[:2], kurz=kurz, note=note, how=how))
for f in sorted(glob.glob(os.path.join(raw('records'), 'line_*.html'))):
    code = os.path.basename(f)[5:11]
    for r in parse_vypravenost(open(f, encoding='utf-8').read()):
        p = r['car'].replace(' ', '')
        n = plate2car.get(p) or (int(r['car']) if r['car'].isdigit() and int(r['car']) in fleet else None)
        add(code, n, r['date'], r['kurz'], r['note'], f'line list, plate {r["car"]}' if n else f'line list, plate {r["car"]} not in the register')
carpages = {}
for f in sorted(glob.glob(os.path.join(raw('cars'), '*.html'))):
    cid = os.path.basename(f)[:-5]; s = open(f, encoding='utf-8').read(); carpages[cid] = s
    n = next((k for k, c in fleet.items() if c['cid'] == cid), None)
    for m in re.finditer(r'<tr class="row car-on-line-[a-z]+[^"]*">(.*?)</tr>', s, flags=re.S):
        b = m.group(1)
        cell = lambda c: clean(re.search(r'<td class="[^"]*%s[^"]*">(.*?)</td>' % c, b, flags=re.S).group(1)) if re.search(r'<td class="[^"]*%s' % c, b) else ''
        route = cell('route'); code = re.sub(r'\D', '', route)
        if code in codes: add(code, n, cell('date'), cell('order-on-line'), cell('note'), 'car page')
day_s = open(os.path.join(raw('records'), f"day_{C['vehicle_day']}.html"), encoding='utf-8').read()
day_lines = sorted(set(re.findall(r'linka=(57[56]\d{3})', day_s)))
save('records.json', dict(records=sorted(recs, key=lambda r: r['date'], reverse=True), vehicle_day_lines=day_lines))
print('records', len(recs), 'matched to cars', sum(1 for r in recs if r['car']), 'DPmML lines in the day overview', day_lines)

# ---- evidence per car: records, photos (date, place), lines read off photos
PL = asset('photo_lines.json')['photos']
ev = {}
for n, c in fleet.items():
    s = carpages.get(c['cid'], '')
    ph = []
    for m in re.finditer(r'id="photo-(\d+)".*?<div class="info">(.*?)</div>', s, flags=re.S):
        info = m.group(2)
        city = re.search(r'<span class="city">(.*?)</span>', info, flags=re.S)
        street = re.search(r'<span class="street">(.*?)</span>', info, flags=re.S)
        dt = re.search(r'(\d+)\. (\d+)\. (\d{4})', info)
        ph.append(dict(id=m.group(1), date=f'{dt.group(3)}-{int(dt.group(2)):02d}-{int(dt.group(1)):02d}' if dt else '',
                       place=', '.join(x for x in (clean(city.group(1)) if city else '', clean(street.group(1)) if street else '') if x)))
    ph.sort(key=lambda x: x['date'], reverse=True)
    seen_lines = [dict(p, **PL[k]) for p in ph for k in (p['id'], f"{p['id']}#{n}") if k in PL and PL[k]['car'] == n]
    ev[n] = dict(records=[r for r in recs if r['car'] == n], photos=ph, photo_lines=seen_lines)
save('fleet.json', fleet)
save('evidence.json', ev)
print('photos listed', sum(len(e['photos']) for e in ev.values()), 'photos with a line read', sum(len(e['photo_lines']) for e in ev.values()))
