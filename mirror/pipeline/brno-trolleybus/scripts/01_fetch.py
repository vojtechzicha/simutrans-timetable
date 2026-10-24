"""Download raw data for Brno trolleybuses into data/raw/<kind>/<date>/.

  python 01_fetch.py --vehicles 2026-09-25        per-line vypravenost pages (bmhd.cz), trolleybus lines
  python 01_fetch.py --register                   trolleybus depot pages + type listings (bmhd.cz evidence DPMB), dated today
  python 01_fetch.py --gtfs                       IDS JMK GTFS (kordis-jmk.cz), dated today

bmhd.cz needs browser headers (see common.fetch); requests are spaced 2 s apart.
"""
import argparse, datetime, html, os, re
from common import RAW, fetch

LINES = ['21', '25', '26', '27', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39']
DEPOTS = ('k', 'h', 's')      # Komín, Husovice, Slatina (Slatina is a bus garage with a few 32 Tr)

p = argparse.ArgumentParser()
p.add_argument('--vehicles', action='append', default=[], help='vypravenost date YYYY-MM-DD (repeatable)')
p.add_argument('--lines', nargs='*', default=LINES)
p.add_argument('--register', action='store_true')
p.add_argument('--gtfs', action='store_true')
p.add_argument('--bus-types', nargs='*', default=None, metavar='CAR',
               help='also fetch the Slatina bus type listings that hold these car numbers (buses seen on trolleybus lines)')
p.add_argument('--date', default=datetime.date.today().isoformat(), help='folder date for register/gtfs')
a = p.parse_args()

for d in a.vehicles:
    for line in a.lines:
        url = f'https://www.bmhd.cz/vypravenost/vypravenost.php?datum={d}&linka={line}'
        fetch(url, os.path.join(RAW, 'vypravenost', d, f'L{line}.html')); print('vypravenost', d, 'line', line)

if a.register:
    folder = os.path.join(RAW, 'register', a.date)
    links = set()
    for code in DEPOTS:
        s = fetch(f'https://www.bmhd.cz/evidence-dpmb/vozovna/{code}', os.path.join(folder, f'voz_{code}.html')).decode('utf-8', 'replace')
        links |= {html.unescape(u) for u in re.findall(r'href="(/evidence-dpmb/vozp\.php[^"]*trakce=trolejbus[^"]*)"', s)}
    n = 0
    for u in sorted(links):
        n += 1; s = fetch('https://www.bmhd.cz' + u, os.path.join(folder, f'types_{n}.html')).decode('utf-8', 'replace')
        for page in sorted(set(html.unescape(x) for x in re.findall(r'href="(/evidence-dpmb/vozp\.php\?page=\d+[^"]*)"', s))):
            n += 1; fetch('https://www.bmhd.cz' + page, os.path.join(folder, f'types_{n}.html'))
    print('register pages saved to', folder)

if a.bus_types:
    folder = os.path.join(RAW, 'register', a.date)
    s = open(os.path.join(folder, 'voz_s.html'), encoding='utf-8', errors='replace').read()
    n = 0
    for part in re.split(r'<div class="row-wrapper type">', s)[1:]:
        m = re.search(r'<a href="(/evidence-dpmb/vozp\.php[^"]*trakce=autobus[^"]*)">', part)
        nums = set(re.findall(r'<span class="number">(\d+)', part))
        if not m or not nums & set(a.bus_types): continue
        n += 1; u = html.unescape(m.group(1))
        t = fetch('https://www.bmhd.cz' + u, os.path.join(folder, f'bustypes_{n}.html')).decode('utf-8', 'replace')
        for page in sorted(set(html.unescape(x) for x in re.findall(r'href="(/evidence-dpmb/vozp\.php\?page=\d+[^"]*)"', t))):
            n += 1; fetch('https://www.bmhd.cz' + page, os.path.join(folder, f'bustypes_{n}.html'))
    print('bus type pages', n)

if a.gtfs:
    dest = os.path.join(RAW, 'gtfs', a.date, 'gtfs.zip')
    fetch('https://kordis-jmk.cz/gtfs/gtfs.zip', dest, pause=0); print('gtfs saved to', dest)
