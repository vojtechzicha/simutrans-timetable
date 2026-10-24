"""Download raw data for the Plzeň trolleybus AND bus sheets into data/raw/<kind>/<date>/ (stored once, here).

  python 01_fetch.py --days 2026-09-14 2026-09-29          day overviews (which lines have records on which day)
  python 01_fetch.py --vehicles 2026-09-22 --lines 10 11   per-line lists with kurz, car and note
  python 01_fetch.py --history 40 42 --since 2026-06-01    per-line history since a date (newest first, up to --max-pages x 50)
  python 01_fetch.py --register trolejbus autobus          PMDP register listings (all pages), dated today
  python 01_fetch.py --operator 1234 autobus               another operator's register (subcontractors), dated today
  python 01_fetch.py --car 12345                           one vehicle page (seznam-autobusu.cz/vuz/<id>)
  python 01_fetch.py --gtfs                                PMDP GTFS (jizdnirady.pmdp.cz/jr/gtfs returns the zip), dated today
  python 01_fetch.py --osm                                 OpenStreetMap trolley_wire ways + trolleybus route relations (Overpass)

seznam-autobusu.cz: browser headers and 2 s between requests (common.fetch). No personal data is sent anywhere.
"""
import argparse, datetime, os, re, time, urllib.parse, urllib.request
from common import RAW, SA, SLUG, PMDP, fetch

p = argparse.ArgumentParser()
p.add_argument('--days', nargs='*', default=[])
p.add_argument('--vehicles', action='append', default=[])
p.add_argument('--lines', nargs='*', default=[])
p.add_argument('--history', nargs='*', default=[])
p.add_argument('--since', default='2026-06-01')
p.add_argument('--max-pages', type=int, default=6)
p.add_argument('--register', nargs='*', default=None)
p.add_argument('--operator', nargs=2, action='append', default=[], metavar=('ID', 'TRAKCE'))
p.add_argument('--car', nargs='*', default=[])
p.add_argument('--gtfs', action='store_true')
p.add_argument('--osm', action='store_true')
p.add_argument('--date', default=datetime.date.today().isoformat())
a = p.parse_args()

def pages(first_url, folder, stem):
    s = fetch(first_url, os.path.join(folder, f'{stem}_1.html')).decode('utf-8', 'replace')
    last = max([int(x) for x in re.findall(r'[?&;]page=(\d+)', s)] or [1])
    for n in range(2, last + 1):
        sep = '&' if '?' in first_url else '?'
        fetch(f'{first_url}{sep}page={n}', os.path.join(folder, f'{stem}_{n}.html'))
    return last

for d in a.days:
    fetch(f'{SA}/vypravenost/{SLUG}?datum={d}', os.path.join(RAW, 'vypravenost-days', f'{d}.html')); print('day', d)
for d in a.vehicles:
    for line in a.lines:
        fetch(f'{SA}/vypravenost/{SLUG}/vypis?datum={d}&linka={urllib.parse.quote(line)}', os.path.join(RAW, 'vypravenost', d, f'L{line}.html'))
        print('vypravenost', d, 'line', line)
for line in a.history:          # 50 records a page (?strana=N), "celkem N" on the first page; newest first
    folder = os.path.join(RAW, 'history', a.date); q = urllib.parse.quote(line)
    s = fetch(f'{SA}/vypravenost/{SLUG}/vypis?linka={q}&since={a.since}', os.path.join(folder, f'L{line}_since{a.since}_1.html')).decode('utf-8', 'replace')
    m = re.search(r'celkem\s*(\d+)', s); last = min(-(-int(m.group(1)) // 50) if m else 1, a.max_pages)
    for n in range(2, last + 1):
        fetch(f'{SA}/vypravenost/{SLUG}/vypis?strana={n}&linka={q}&since={a.since}', os.path.join(folder, f'L{line}_since{a.since}_{n}.html'))
    print('history', line, 'since', a.since, last, 'pages', m.group(1) if m else '?', 'records')
if a.register is not None:
    folder = os.path.join(RAW, 'register', a.date)
    for tr in a.register or ['trolejbus', 'autobus']:
        n = pages(f'{SA}/seznam?iddopravce={PMDP}&trakce={tr}&prov=1&vcetneSluzebnich=1', folder, f'pmdp_{tr}')
        print('register', tr, n, 'pages')
for oid, tr in a.operator:
    folder = os.path.join(RAW, 'register', a.date)
    n = pages(f'{SA}/seznam?iddopravce={oid}&trakce={tr}&prov=1&vcetneSluzebnich=1', folder, f'op{oid}_{tr}')
    print('operator', oid, tr, n, 'pages')
for cid in a.car:
    fetch(f'{SA}/vuz/{cid}', os.path.join(RAW, 'register', a.date, f'vuz_{cid}.html')); print('car', cid)
if a.gtfs:
    dest = os.path.join(RAW, 'gtfs', a.date, 'gtfs.zip')
    fetch('https://jizdnirady.pmdp.cz/jr/gtfs', dest, pause=0); print('gtfs saved', dest)
if a.osm:
    # Overpass needs Accept: application/json and a non-browser User-Agent (406 otherwise). Plzeň box.
    q = ('[out:json][timeout:120];(way["trolley_wire"="yes"](49.68,13.25,49.80,13.50);'
         'way["railway"="trolleybus_wire"](49.68,13.25,49.80,13.50););out geom;')
    q2 = ('[out:json][timeout:180];relation["route"="trolleybus"](49.68,13.25,49.80,13.50);out geom;')
    for name, qq in (('trolley_wire.json', q), ('trolleybus_routes.json', q2)):
        req = urllib.request.Request('https://overpass-api.de/api/interpreter', data=urllib.parse.urlencode({'data': qq}).encode(),
                                     headers={'User-Agent': 'simutrans-timetable-pipeline/1.0', 'Accept': 'application/json'})
        data = urllib.request.urlopen(req, timeout=300).read()
        dest = os.path.join(RAW, 'osm', a.date, name); os.makedirs(os.path.dirname(dest), exist_ok=True)
        open(dest, 'wb').write(data); print('osm', name, len(data)); time.sleep(2)
