"""JDF -> derived/trips.json, versions.json, line_class.json.

Bus lines: every line in the CIS JŘ bus export whose number starts with one of config.jdf.line_prefixes (575 Most,
576 Litvínov) and whose operator IČO is DPmML's, found by scanning the export (about 13,000 inner zips), so new or
removed lines need no config edit. Only DPmML appears under these numbers; no other operator runs a city line.
The line number shown is the JDF number without the town prefix (575005 -> 5, 576013 -> 13).

Tram replacement buses ("NAD", config.nad): since 1 Mar 2026 Záluží, Chempark – Litvínov, Citadela is run by buses that
"copy the current tram timetables" (dpmost.cz/zvd2026001). The tram timetables in the city export still list every
tram trip to and from Citadela, so the replacement bus trips are the Chempark – Citadela part of those tram trips
(lines in config.jdf.tram_lines), at the tram's minutes. The tram sheet cuts the same trips at Chempark.

Version rule (shared): among a line's versions valid on the service day, the latest "valid from" wins; ties go to the
shortest validity.
Class of a line on the service day, by its trips:
  peak       a trip is on the road at some time in 16:00–16:59 (departure before 17:00, arrival at 16:00 or later)
  preak      afternoon trips (13:00–16:00) that all end before 16:00 (school and shift trips): not in the peak
  morning    day service ends before 13:00
  evening    trips only after 17:00
  none       no trip on the day
Only "peak" lines go on the sheet as Simutrans lines; the others are listed under "Not in the afternoon peak".
"""
import collections, csv, datetime, io, re, zipfile
from lib import CONFIG, src, jdf_open, jdf_versions, pick_version, jdf_tables, jdf_trips, day, save, hm

C = CONFIG; J = C['jdf']; d = day(C['service_day'])
outer = jdf_open(src(J['bus_zip']))
vers = []
for n in outer.namelist():
    try: inner = zipfile.ZipFile(io.BytesIO(outer.read(n)))
    except zipfile.BadZipFile: continue
    ln = [x for x in inner.namelist() if x.lower().startswith('linky')]
    if not ln: continue
    for r in csv.reader(io.StringIO(inner.read(ln[0]).decode('cp1250').replace(';\r\n', '\n').replace(';\n', '\n'))):
        if not r or r[2] != J['operator_ic'] or not any(r[0].startswith(p) for p in J['line_prefixes']): continue
        ds = [datetime.datetime.strptime(x, '%d%m%Y').date() for x in r[3:] if re.fullmatch(r'\d{8}', x)]
        vers.append(dict(inner=n, line=r[0], name=r[1], valid_from=ds[0].isoformat(), valid_to=ds[1].isoformat(),
                         diversion=len(r) > 5 and r[5] == '1', one_way=len(r) > 8 and r[8] == '1'))

def classify(tr):
    deps = sorted(t['dep'] for t in tr)
    if not deps: return 'none'
    if any(t['dep'] < 1020 and t['arr'] >= 960 for t in tr): return 'peak'
    if any(780 <= x < 960 for x in deps): return 'prepeak'
    if all(x >= 1020 for x in deps): return 'evening'
    return 'morning'

trips, chosen, cls = {}, {}, {}
for code in sorted({v['line'] for v in vers}):
    L = str(int(code[3:]))
    v = pick_version([x for x in vers if x['line'] == code], d)
    if not v: cls[L] = dict(cls='none', code=code, name=vers[0]['name'], why='no version valid on the day'); continue
    tr = jdf_trips(jdf_tables(outer, v['inner']), d)
    c = classify(tr); deps = sorted(t['dep'] for t in tr)
    cls[L] = dict(cls=c, code=code, name=v['name'], trips=len(tr), first=hm(deps[0]) if deps else None, last=hm(deps[-1]) if deps else None)
    chosen[L] = v
    if c == 'peak': trips[L] = tr
    print(L, code, v['inner'], v['valid_from'], '–', v['valid_to'], len(tr), 'trips', c)

# ---- tram replacement buses: the Chempark – Citadela part of the tram trips
N = C['nad']; touter = jdf_open(src(J['tram_zip']))
tvers = jdf_versions(touter, set(J['tram_lines']))
nad = []
for code, TL in J['tram_lines'].items():
    v = pick_version([x for x in tvers if x['line'] == code], d); chosen['tram ' + TL] = v
    for t in jdf_trips(jdf_tables(touter, v['inner']), d):
        st, tm = t['stops'], t['times']
        i = next((k for k, s in enumerate(st) if N['cut_stop'] in s), None)
        if i is None: continue
        if N['far_end'] in t['to']: st, tm = st[i:], tm[i:]
        elif N['far_end'] in t['fr']: st, tm = st[:i + 1], tm[:i + 1]
        else: continue
        keep = [k for k, s in enumerate(st) if s not in N['drop_stops'] and not (s in N['drop_stops_towards_most'] and N['far_end'] in t['fr'])]
        st, tm = [st[k] for k in keep], [tm[k] for k in keep]
        nad.append(dict(t, sp=t['sp'], tram_line=TL, stops=st, times=tm, fr=st[0], to=st[-1], dep=tm[0], arr=tm[-1]))
    print('replacement buses for tram', TL, v['inner'], v['valid_from'], sum(1 for x in nad if x['tram_line'] == TL), 'trips')
c = classify(nad); deps = sorted(t['dep'] for t in nad)
cls[N['label']] = dict(cls=c, code='tram ' + ', '.join(J['tram_lines'].values()), name=N['title'], trips=len(nad), first=hm(deps[0]), last=hm(deps[-1]))
if c == 'peak': trips[N['label']] = nad
save('versions.json', dict(all=vers, chosen=chosen))
save('line_class.json', cls)
save('trips.json', trips)
print('lines', len(cls), collections.Counter(x['cls'] for x in cls.values()))
