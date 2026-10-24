"""Download the raw inputs of a state into data/raw/ (only files that are missing, unless --refresh).

  vypravenost/<date>/<line>.html    seznam-autobusu.cz/vypravenost/pid/vypis?datum=<date>&linka=<line>
  vypravenost/<date>/overview.html  seznam-autobusu.cz/vypravenost/pid?datum=<date>
  vypravenost/history/<line>.html   ...vypis?linka=<line>&since=<history_since>  (coverage check)
  register/<date>/l_<depot>_<n>.html  seznam-autobusu.cz/seznam?...depotId=<id>... page n (100 per page)
  gtfs/<date>/gtfs.zip              data.pid.cz/PID_GTFS.zip (the feed only covers ~2 weeks from its export date)

Usage: python 01_fetch.py --state 2026-09-27 [--refresh]
"""
import argparse, os, re, unicodedata
from common import state, fetch, RAW

SA = 'https://seznam-autobusu.cz'

def slug(name):
    return unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode().lower()

def get(url, dest, refresh):
    if os.path.exists(dest) and not refresh:
        return open(dest, 'rb').read()
    print('fetch', url)
    return fetch(url, dest, pause=1.0)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--state', required=True); ap.add_argument('--refresh', action='store_true')
    a = ap.parse_args(); s = state(a.state); vy = s['vypravenost']
    d = s['vehicle_date']
    get(f'{SA}/vypravenost/{vy["slug"]}?datum={d}', os.path.join(RAW, 'vypravenost', d, 'overview.html'), a.refresh)
    for l in vy['lines']:
        get(f'{SA}/vypravenost/{vy["slug"]}/vypis?datum={d}&linka={l}', os.path.join(RAW, 'vypravenost', d, f'{l}.html'), a.refresh)
    for day, lines in vy.get('extra_days', {}).items():
        for l in lines:
            get(f'{SA}/vypravenost/{vy["slug"]}/vypis?datum={day}&linka={l}', os.path.join(RAW, 'vypravenost', day, f'{l}.html'), a.refresh)
    for l in vy.get('history_lines', []):
        get(f'{SA}/vypravenost/{vy["slug"]}/vypis?linka={l}&since={vy["history_since"]}', os.path.join(RAW, 'vypravenost', 'history', f'{l}.html'), a.refresh)
    reg = s['register']
    for name, did in reg['depots'].items():
        page = 1
        while True:
            dest = os.path.join(RAW, 'register', reg['raw'], f'l_{slug(name)}_{page}.html')
            dep = f'&depotId={did}&onlyCurrentDepot=1' if did else ''   # one-depot operators: no depot filter
            t = get(f'{SA}/seznam?page={page}&iddopravce={reg["operator_id"]}&trakce=tramvaj&prov=1&vcetneSluzebnich=1{dep}',
                    dest, a.refresh).decode('utf-8', 'ignore')
            if f'page={page + 1}&' not in t: break
            page += 1
    g = s['gtfs']
    get(g['url'], os.path.join(RAW, 'gtfs', g['raw'], 'gtfs.zip'), a.refresh)

if __name__ == '__main__':
    main()
