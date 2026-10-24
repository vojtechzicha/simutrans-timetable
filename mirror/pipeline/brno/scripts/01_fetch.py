"""Download raw data for Brno into data/raw/<kind>/<date>/.

  python 01_fetch.py --vehicles 2026-09-25        per-line vypravenost pages (bmhd.cz), lines 1-12
  python 01_fetch.py --register                   depot pages + type listings (bmhd.cz evidence DPMB), dated today
  python 01_fetch.py --gtfs                       IDS JMK GTFS (kordis-jmk.cz), dated today

bmhd.cz needs browser headers (see common.fetch); requests are spaced 2 s apart.
"""
import argparse, datetime, html, os, re
from common import RAW, fetch

p = argparse.ArgumentParser()
p.add_argument('--vehicles', action='append', default=[], help='vypravenost date YYYY-MM-DD (repeatable)')
p.add_argument('--register', action='store_true')
p.add_argument('--gtfs', action='store_true')
p.add_argument('--date', default=datetime.date.today().isoformat(), help='folder date for register/gtfs')
a = p.parse_args()

for d in a.vehicles:
    for line in range(1, 13):
        url = f'https://www.bmhd.cz/vypravenost/vypravenost.php?datum={d}&linka={line}'
        dest = os.path.join(RAW, 'vypravenost', d, f'L{line}.html')
        fetch(url, dest); print('vypravenost', d, 'line', line)

if a.register:
    folder = os.path.join(RAW, 'register', a.date)
    for code in ('M', 'P', 'K'):          # Medlánky, Pisárky (trams), Komín (trolleybuses, for reference)
        fetch(f'https://www.bmhd.cz/evidence-dpmb/vozovna/{code}', os.path.join(folder, f'voz_{code}.html'))
    links = set()
    for code in ('M', 'P'):
        s = open(os.path.join(folder, f'voz_{code}.html'), encoding='utf-8', errors='replace').read()
        links |= {html.unescape(u) for u in re.findall(r'href="(/evidence-dpmb/vozp\.php[^"]*trakce=tramvaj[^"]*)"', s)}
    n = 0
    for u in sorted(links):
        n += 1; dest = os.path.join(folder, f'types_{n}.html')
        s = fetch('https://www.bmhd.cz' + u, dest).decode('utf-8', 'replace')
        for page in sorted(set(html.unescape(x) for x in re.findall(r'href="(/evidence-dpmb/vozp\.php\?page=\d+[^"]*)"', s))):
            n += 1; fetch('https://www.bmhd.cz' + page, os.path.join(folder, f'types_{n}.html'))
    print('register pages saved to', folder)

if a.gtfs:
    dest = os.path.join(RAW, 'gtfs', a.date, 'gtfs.zip')
    fetch('https://kordis-jmk.cz/gtfs/gtfs.zip', dest, pause=0); print('gtfs saved to', dest)
