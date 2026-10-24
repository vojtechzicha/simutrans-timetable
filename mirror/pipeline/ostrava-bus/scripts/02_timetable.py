"""JDF.zip (CIS JŘ bus export) -> derived/trips.json, versions.json, line_class.json.

Lines: every line whose number starts with config.jdf.line_prefix (915) and whose operator IČO is DPO's.
Found by scanning the export (about 13,000 inner zips, a minute or two), so new or removed lines need no config edit.
Version rule (shared): among a line's versions valid on the day, the latest "valid from" wins; ties go to the
shortest validity.
Class of a line on the vehicle day: "peak" if it has a trip in the afternoon (13:00–19:00), "morning" if its
day service ends before 13:00, "night" if it runs only between 22:00 and 04:30, "none" if nothing runs.
Only "peak" lines go on the sheet; the others are listed under "Not in the afternoon peak".
"""
import csv, io, os, re, zipfile
from lib import CONFIG, RAW, jdf_open, pick_version, jdf_tables, jdf_trips, day, save, hm

d = day(CONFIG['vehicle_day']); J = CONFIG['jdf']
outer = jdf_open(os.path.join(RAW, 'JDF.zip'))
vers = []
for n in outer.namelist():
    try: inner = zipfile.ZipFile(io.BytesIO(outer.read(n)))
    except zipfile.BadZipFile: continue
    ln = [x for x in inner.namelist() if x.lower().startswith('linky')]
    if not ln: continue
    for r in csv.reader(io.StringIO(inner.read(ln[0]).decode('cp1250').replace(';\r\n', '\n').replace(';\n', '\n'))):
        if not r or not r[0].startswith(J['line_prefix']) or r[2] != J['operator_ic'] or r[0] in J['exclude']: continue
        dates = [x for x in r[3:] if re.fullmatch(r'\d{8}', x)]
        import datetime
        ds = [datetime.datetime.strptime(x, '%d%m%Y').date() for x in dates]
        vers.append(dict(inner=n, line=r[0], name=r[1], valid_from=ds[0].isoformat(), valid_to=ds[1].isoformat()))
codes = sorted({v['line'] for v in vers})
trips, chosen, cls = {}, {}, {}
for code in codes:
    L = str(int(code[3:]))
    v = pick_version([x for x in vers if x['line'] == code], d)
    if not v: cls[L] = dict(cls='none', name=vers[0]['name'], why='no version valid on the day'); continue
    tr = jdf_trips(jdf_tables(outer, v['inner']), d)
    deps = sorted(t['dep'] for t in tr)
    day_deps = [x for x in deps if 270 <= x < 1320]
    if any(780 <= x < 1140 for x in deps): c = 'peak'
    elif day_deps: c = 'morning'
    elif deps: c = 'night'
    else: c = 'none'
    cls[L] = dict(cls=c, name=v['name'], trips=len(tr), first=hm(deps[0]) if deps else None, last=hm(deps[-1]) if deps else None)
    chosen[L] = v
    if c == 'peak': trips[L] = tr
    print(L, v['inner'], v['valid_from'], '–', v['valid_to'], len(tr), 'trips', c)
save('versions.json', dict(all=vers, chosen=chosen))
save('line_class.json', cls)
save('trips.json', trips)
print('lines', len(codes), {k: sum(1 for x in cls.values() if x['cls'] == k) for k in ('peak', 'morning', 'night', 'none')})
