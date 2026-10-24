"""JDF.zip (CIS JŘ bus export) -> derived/trips.json, versions.json, line_class.json.

Lines: the MHD licences of config.jdf.licences (Havířov 876401–876421 and 876434, Karviná 877511–877520, Orlová
878501–878505; the ODIS number is the last three digits), operator IČO config.jdf.operator_ic. Found by scanning the
export (about 13,000 inner zips), so the versions need no config edit.
Version rule (shared): among a line's versions valid on the day, the latest "valid from" wins; ties go to the shortest
validity. Diversion versions (Linky field 6 = 1) valid on the day are counted for the card note; the regular rule
still decides.
Class on the vehicle day: "peak" if it has a trip in 13:00–19:00, "morning" if its day service ends before 13:00,
"night" if it runs only 22:00–04:30, "none" if nothing runs. Only "peak" lines go on the sheet.
"""
import csv, datetime, io, os, re, zipfile
from lib import CONFIG, RAW, jdf_open, pick_version, jdf_tables, jdf_trips, day, save, hm

d = day(CONFIG['vehicle_day']); J = CONFIG['jdf']
want = set()
for x in J['licences']:
    a, _, b = x.partition('-'); want |= {str(i) for i in range(int(a), int(b or a) + 1)}
outer = jdf_open(os.path.join(RAW, 'JDF.zip'))
vers = []
for n in outer.namelist():
    try: inner = zipfile.ZipFile(io.BytesIO(outer.read(n)))
    except zipfile.BadZipFile: continue
    ln = [x for x in inner.namelist() if x.lower().startswith('linky')]
    if not ln: continue
    for r in csv.reader(io.StringIO(inner.read(ln[0]).decode('cp1250').replace(';\r\n', '\n').replace(';\n', '\n'))):
        if not r or r[0] not in want or r[2] != J['operator_ic']: continue
        ds = [datetime.datetime.strptime(x, '%d%m%Y').date() for x in r[3:] if re.fullmatch(r'\d{8}', x)]
        vers.append(dict(inner=n, line=r[0], name=r[1], valid_from=ds[0].isoformat(), valid_to=ds[1].isoformat(),
                         diversion=len(r) > 5 and r[5] == '1'))
codes = sorted({v['line'] for v in vers})
trips, chosen, cls = {}, {}, {}
for code in codes:
    L = code[-3:]
    vs = [x for x in vers if x['line'] == code]
    v = pick_version(vs, d)
    if not v: cls[L] = dict(cls='none', name=vs[0]['name'], why='no version valid on the day'); continue
    tb = jdf_tables(outer, v['inner'])
    bad = [r for r in tb['Caskody'] if len(r) < 7 or not re.fullmatch(r'\d{8}', r[5])]   # text-only date rows (no range): no effect on running
    if bad: print(L, 'Caskody rows without a date range, ignored:', bad[:3]); tb['Caskody'] = [r for r in tb['Caskody'] if r not in bad]
    tr = jdf_trips(tb, d)
    deps = sorted(t['dep'] for t in tr)
    if any(780 <= x < 1140 for x in deps): c = 'peak'
    elif any(270 <= x < 1320 for x in deps): c = 'morning'
    elif deps: c = 'night'
    else: c = 'none'
    v = dict(v, diversion_valid=sum(1 for x in vs if x['diversion'] and x['valid_from'] <= CONFIG['vehicle_day'] <= x['valid_to']))
    cls[L] = dict(cls=c, name=v['name'], code=code, trips=len(tr), first=hm(deps[0]) if deps else None, last=hm(deps[-1]) if deps else None)
    chosen[L] = v
    if c == 'peak': trips[L] = tr
    print(L, v['inner'], v['valid_from'], '–', v['valid_to'], len(tr), 'trips', c, 'diversion' if v['diversion'] else '')
save('versions.json', dict(all=vers, chosen=chosen))
save('line_class.json', cls)
save('trips.json', trips)
print('lines', len(codes), {k: sum(1 for x in cls.values() if x['cls'] == k) for k in ('peak', 'morning', 'night', 'none')})
