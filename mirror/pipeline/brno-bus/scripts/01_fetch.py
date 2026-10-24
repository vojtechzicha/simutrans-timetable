"""Download raw data for Brno buses into data/raw/<kind>/<date>/.

  python 01_fetch.py --vehicles 2026-09-25        per-line vypravenost pages (bmhd.cz), the city bus lines
  python 01_fetch.py --register                   bus garage pages + type listings (Medlánky m, Slatina s), dated today

The GTFS is the tram pipeline's (pipeline/brno/scripts/01_fetch.py --gtfs). bmhd.cz needs browser headers
(common.fetch); requests are spaced 2 s apart.
"""
import argparse, datetime, html, os, re
from common import RAW, fetch

LINES = ['40', '41', '42', '44', '46', '47', '48', '49', '50', '52', '54', '55', '57', '58', '62', '63', '64', '65', '66',
         '67', '68', '69', '70', '72', '74', '75', '77', '78', '84', 'E50', 'E56', 'E75', 'x75', '56']   # 56 = the kurzy of E56 (bmhd files them as 56)
GARAGES = ('m', 's')           # Medlánky, Slatina

p = argparse.ArgumentParser()
p.add_argument('--vehicles', action='append', default=[], help='vypravenost date YYYY-MM-DD (repeatable)')
p.add_argument('--lines', nargs='*', default=LINES)
p.add_argument('--register', action='store_true')
p.add_argument('--external', metavar='DATE', help='fetch seznam-autobusu.cz pages of non-DPMB vehicles seen in the vypravenost of that day')
p.add_argument('--date', default=datetime.date.today().isoformat(), help='folder date for the register')
a = p.parse_args()

for d in a.vehicles:
    for line in a.lines:
        url = f'https://www.bmhd.cz/vypravenost/vypravenost.php?datum={d}&linka={line}'
        fetch(url, os.path.join(RAW, 'vypravenost', d, f'L{line}.html')); print('vypravenost', d, 'line', line)

if a.register:
    folder = os.path.join(RAW, 'register', a.date)
    links = set()
    for code in GARAGES:
        s = fetch(f'https://www.bmhd.cz/evidence-dpmb/vozovna/{code}', os.path.join(folder, f'voz_{code}.html')).decode('utf-8', 'replace')
        links |= {html.unescape(u) for u in re.findall(r'href="(/evidence-dpmb/vozp\.php[^"]*trakce=autobus[^"]*)"', s)}
    n = 0
    for u in sorted(links):
        n += 1; s = fetch('https://www.bmhd.cz' + u, os.path.join(folder, f'types_{n}.html')).decode('utf-8', 'replace')
        for page in sorted(set(html.unescape(x) for x in re.findall(r'href="(/evidence-dpmb/vozp\.php\?page=\d+[^"]*)"', s))):
            n += 1; fetch('https://www.bmhd.cz' + page, os.path.join(folder, f'types_{n}.html'))
    print('register pages saved to', folder, n)

if a.external:
    # vehicles of other operators (48, 74) have no BMHD register entry; their record links to seznam-autobusu.cz
    import glob
    ids = set()
    for fn in glob.glob(os.path.join(RAW, 'vypravenost', a.external, 'L*.html')):
        ids |= set(re.findall(r'seznam-autobusu\.cz/vuz/(\d+)', open(fn, encoding='utf-8', errors='replace').read()))
    for i in sorted(ids):
        fetch(f'https://seznam-autobusu.cz/vuz/{i}', os.path.join(RAW, 'external', f'{i}.html'), pause=3.0)
    print('external vehicle pages', len(ids))
