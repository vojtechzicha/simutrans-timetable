"""Download raw data for Plzeň into data/raw/<kind>/<date>/.

  python 01_fetch.py --days 2026-09-18 2026-09-25     day overviews (to see which days have tram records)
  python 01_fetch.py --vehicles 2026-09-18            per-line vypravenost lists (lines 1, 2, 4) with notes
  python 01_fetch.py --register                       PMDP tram register (all pages), dated today
  python 01_fetch.py --gtfs                           PMDP GTFS, dated today

seznam-autobusu.cz: send browser headers (common.fetch), 2 s between requests.
"""
import argparse, datetime, os, re
from common import RAW, fetch

p = argparse.ArgumentParser()
p.add_argument('--days', nargs='*', default=[])
p.add_argument('--vehicles', action='append', default=[])
p.add_argument('--register', action='store_true')
p.add_argument('--gtfs', action='store_true')
p.add_argument('--date', default=datetime.date.today().isoformat())
a = p.parse_args()
SA = 'https://seznam-autobusu.cz'
for d in a.days:
    fetch(f'{SA}/vypravenost/mhd-plzen?datum={d}', os.path.join(RAW, 'vypravenost-days', f'{d}.html')); print('day', d)
for d in a.vehicles:
    for line in (1, 2, 4):
        fetch(f'{SA}/vypravenost/mhd-plzen/vypis?datum={d}&linka={line}', os.path.join(RAW, 'vypravenost', d, f'L{line}.html'))
        print('vypravenost', d, 'line', line)
if a.register:
    folder = os.path.join(RAW, 'register', a.date)
    s = fetch(f'{SA}/seznam?iddopravce=71&trakce=tramvaj', os.path.join(folder, 'page1.html')).decode('utf-8', 'replace')
    last = max([int(x) for x in re.findall(r'page=(\d+)', s)] or [1])
    for n in range(2, last + 1):
        fetch(f'{SA}/seznam?iddopravce=71&trakce=tramvaj&page={n}', os.path.join(folder, f'page{n}.html'))
    print('register pages', last)
if a.gtfs:
    dest = os.path.join(RAW, 'gtfs', a.date, 'gtfs.zip')
    fetch('https://jizdnirady.pmdp.cz/jr/gtfs', dest, pause=0)   # the URL returns the zip directly
    print('gtfs saved', dest)
