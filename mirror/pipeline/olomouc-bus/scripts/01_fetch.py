"""Download raw inputs into data/raw/ (only files that are missing, unless --refresh). About one request a second.

  vypravenost/overview/<date>.html        seznam-autobusu.cz/vypravenost/mhd-ol?datum=<date>   (day overview, all modes)
  vypravenost/<date>/<line>.html          .../vypravenost/mhd-ol/vypis?datum=<date>&linka=<line>
  vypravenost/history/<since>/<line>_p<n>.html   .../vypis?strana=<n>&linka=<line>&since=<since>  (line history, all pages)
  register/<date>/<traction>_<n>.html     seznam-autobusu.cz/seznam?page=<n>&iddopravce=134&trakce=<traction>&prov=1&vcetneSluzebnich=1
  car/<car id>.html                       seznam-autobusu.cz/vuz/<id>  (cars in the records that are not in the DPMO register)
The DPMO GTFS is not fetched here: the tram pipeline's stored copy is read (common.gtfs_path). --gtfs downloads it
into data/raw/gtfs/<state gtfs.raw>/ only if you ask.

Usage:
  python 01_fetch.py --state 2026-09-29 --overviews 2026-09-01 2026-09-29
  python 01_fetch.py --state 2026-09-29 --register --history --day
  python 01_fetch.py --state 2026-09-29 --cars
"""
import argparse, datetime, glob, os, re
from common import state, fetch, RAW, parse_vypis, parse_register, load, DER

SA = 'https://seznam-autobusu.cz'

def get(url, dest, refresh=False):
    if os.path.exists(dest) and not refresh:
        return open(dest, 'rb').read()
    print('fetch', url)
    return fetch(url, dest)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--state', required=True); ap.add_argument('--refresh', action='store_true')
    ap.add_argument('--overviews', nargs=2, metavar=('FROM', 'TO')); ap.add_argument('--register', action='store_true')
    ap.add_argument('--history', action='store_true'); ap.add_argument('--day', action='store_true')
    ap.add_argument('--cars', action='store_true'); ap.add_argument('--gtfs', action='store_true')
    a = ap.parse_args(); s = state(a.state); vy = s['vypravenost']; slug = vy['slug']
    if a.overviews:
        d = datetime.date.fromisoformat(a.overviews[0]); end = datetime.date.fromisoformat(a.overviews[1])
        while d <= end:
            if d.weekday() < 5:
                get(f'{SA}/vypravenost/{slug}?datum={d}', os.path.join(RAW, 'vypravenost', 'overview', f'{d}.html'), a.refresh)
            d += datetime.timedelta(days=1)
    if a.day:
        D = s['vehicle_date']
        for l in s['lines']:
            get(f'{SA}/vypravenost/{slug}/vypis?datum={D}&linka={l}', os.path.join(RAW, 'vypravenost', D, f'{l}.html'), a.refresh)
    if a.history:
        since = vy['history_since']
        for l in s['lines']:
            page = 1
            while True:
                dest = os.path.join(RAW, 'vypravenost', 'history', since, f'{l}_p{page}.html')
                t = get(f'{SA}/vypravenost/{slug}/vypis?strana={page}&linka={l}&since={since}', dest, a.refresh).decode('utf-8', 'ignore')
                if f'strana={page + 1}&amp;' not in t or page >= vy.get('history_max_pages', 12): break
                page += 1
    if a.register:
        reg = s['register']
        for tr in reg['tractions']:
            page = 1
            while True:
                dest = os.path.join(RAW, 'register', reg['raw'], f'{tr}_{page}.html')
                t = get(f'{SA}/seznam?page={page}&iddopravce={reg["operator_id"]}&trakce={tr}&prov=1&vcetneSluzebnich=1', dest, a.refresh).decode('utf-8', 'ignore')
                if f'page={page + 1}&' not in t: break
                page += 1
    if a.cars:
        # vehicle pages of cars in the records that the DPMO register does not list (other operators, withdrawn cars)
        reg = s['register']; known = set()
        for tr in reg['tractions']:
            known |= {v['id'] for v in parse_register(sorted(glob.glob(os.path.join(RAW, 'register', reg['raw'], f'{tr}_*.html')))).values()}
        ids = set()
        for p in glob.glob(os.path.join(RAW, 'vypravenost', '**', '*.html'), recursive=True):
            if os.sep + 'overview' + os.sep in p: continue
            for r in parse_vypis(p): ids |= set(r['ids'])
        for i in sorted(ids - known, key=int):
            get(f'{SA}/vuz/{i}', os.path.join(RAW, 'car', f'{i}.html'), a.refresh)
    if a.gtfs:
        g = s['gtfs']; get(g['url'], os.path.join(RAW, 'gtfs', g['raw'], 'gtfs.zip'), a.refresh)

if __name__ == '__main__':
    main()
