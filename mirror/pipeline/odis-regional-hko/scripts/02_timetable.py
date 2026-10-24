"""JDF.zip (CIS JŘ bus export) -> derived/trips.json, versions.json, line_class.json.

Lines: every licence whose number starts with an area prefix (config.areas, e.g. 912 Havířovsko, 873 Karvinsko,
874 Orlovsko) and whose operator is the area's (area ic, default config.jdf.operator_ic: Transdev Slezsko). Found by scanning the export, so new versions need no config edit.
One ODIS line can hold licences of two areas (553 = 873553 + 874553): trips are merged by ODIS number (the last three
digits) and keep their licence in 'lic'. config.jdf.extra_lics {licence: area id} reads a licence of another sheet's area
into this sheet's line of the same number (TFJ: 883980 and 883985, Z-Group's trips of 980 and 985), whatever its operator.
Version rule (shared): among a licence's versions valid on the day, the latest "valid from" wins; ties go to the shortest
validity. Diversion versions (Linky field 6 = 1) are noted for the network state.
Class on the vehicle day: "afternoon" if it has a trip in 13:00–19:00, "day" if it runs only outside it, "none" if
nothing runs.
"""
import csv, datetime, io, os, re, zipfile
from lib import CONFIG, rel, jdf_open, pick_version, jdf_tables, jdf_trips, day, save, hm, area_of

d = day(CONFIG['vehicle_day']); J = CONFIG['jdf']
# the bus export, plus config.jdf.extra_zips: CIS JŘ's city-transport export (draha/mestske/JDF.zip) holds the trolleybus lines
# (Opava 905201-905204, traction T), which the bus export leaves out; same licence numbers, same version rule
outers = [jdf_open(rel(z)) for z in [J['zip']] + J.get('extra_zips', [])]
XL = J.get('extra_lics', {}); AID = {a['id']: a for a in CONFIG['areas']}
area = lambda code, ic=None: area_of(code, ic) or (AID[XL[code]] if code in XL else None)
vers = []
for zi, outer in enumerate(outers):
  for n in outer.namelist():
    try: inner = zipfile.ZipFile(io.BytesIO(outer.read(n)))
    except zipfile.BadZipFile: continue
    ln = [x for x in inner.namelist() if x.lower().startswith('linky')]
    if not ln: continue
    for r in csv.reader(io.StringIO(inner.read(ln[0]).decode('cp1250').replace(';\r\n', '\n').replace(';\n', '\n'))):
        if not r or not area(r[0], r[2]): continue
        ds = [datetime.datetime.strptime(x, '%d%m%Y').date() for x in r[3:] if re.fullmatch(r'\d{8}', x)]
        vers.append(dict(inner=n, lic=r[0], name=r[1], valid_from=ds[0].isoformat(), valid_to=ds[1].isoformat(),
                         diversion=len(r) > 5 and r[5] == '1', **({'zip': zi, 'traction': r[4] if len(r) > 4 else ''} if zi else {})))
trips, chosen, cls = {}, {}, {}
for code in sorted({v['lic'] for v in vers}):
    L = code[-3:]
    vs = [x for x in vers if x['lic'] == code]
    if code in CONFIG.get('regular_not_diversion', {}): vs = [x for x in vs if not x['diversion']]   # a short diversion: the regular route
    v = pick_version(vs, d)
    if not v: print(code, 'no version valid on the day'); continue
    tb = jdf_tables(outers[v.get('zip', 0)], v['inner'])
    bad = [r for r in tb['Caskody'] if len(r) < 7 or not re.fullmatch(r'\d{8}', r[5])]   # text-only rows: no effect on running
    if bad: tb['Caskody'] = [r for r in tb['Caskody'] if r not in bad]
    tr = jdf_trips(tb, d)
    for t in tr: t['lic'] = code
    ar = area(code)
    if ar.get('town'):
        # a town network's JDF writes its own stops without the town ("Lyžbice,škola", "Místek,Anenská", "aut.st."); the regional
        # JDFs write "Třinec,Lyžbice,..." — so a stop whose first part is not a town gets the town in front (as the HKO sheet does)
        tw = ar['town']; towns = set(CONFIG.get('towns', [])) | {tw}
        def full(x):
            x = x.replace(',,', ',')
            return x if x.split(',')[0] in towns else tw + ',' + x
        for t in tr:
            t['stops'] = [full(x) for x in t['stops']]; t['fr'] = full(t['fr']); t['to'] = full(t['to'])
    chosen[code] = dict(v, area=ar['id'], trips=len(tr))
    trips.setdefault(L, []).extend(tr)
    print(code, v['valid_from'], '–', v['valid_to'], 'DIVERSION' if v['diversion'] else '', len(tr), 'trips', v['name'][:70])
for L, tr in trips.items():
    tr.sort(key=lambda t: t['dep'])
    deps = [t['dep'] for t in tr]
    c = 'afternoon' if any(780 <= x < 1140 for x in deps) else 'day' if deps else 'none'
    lics = sorted({c_ for c_, v in chosen.items() if c_[-3:] == L})
    cls[L] = dict(cls=c, lics=lics, areas=sorted({chosen[x]['area'] for x in lics}), name=chosen[lics[0]]['name'], traction=chosen[lics[0]].get('traction') or 'A',
                  trips=len(tr), first=hm(deps[0]) if deps else None, last=hm(deps[-1]) if deps else None,
                  afternoon=sum(1 for x in deps if 780 <= x < 1140))
save('versions.json', dict(all=vers, chosen=chosen))
save('line_class.json', cls)
save('trips.json', {L: tr for L, tr in trips.items() if tr})
print('ODIS lines', len(cls), {k: sum(1 for x in cls.values() if x['cls'] == k) for k in ('afternoon', 'day', 'none')})
print('two licences:', {L: c['lics'] for L, c in cls.items() if len(c['lics']) > 1})
