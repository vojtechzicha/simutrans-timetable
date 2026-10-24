"""Fetch the timetable and the fleet registers into data/raw (only files that are missing).

  * PID GTFS -> data/raw/gtfs/<gtfs.raw>/gtfs.zip
  * seznam-autobusu.cz registers of in-service buses (trakce=autobus, service cars included), 100 cars a page:
    DPP -> data/raw/register/<register_raw>/dpp_bus_<page>.html, every other PID city operator -> op_<slug>_<page>.html
  * with --cars: single car pages (vuz_<id>.html) for every car id in the deployment records that the lists do not have
    (run after 01_fetch_records.py and 02_register.py; then run 02_register.py again).
The game export (data/raw/game/<game_raw>/lines.json) comes from the save-game session (simutrans-122-0-58), see README.

Usage: python 01_fetch_sources.py --state 2026-09-29 [--cars]
"""
import argparse, glob, os, re
from common import state, fetch, load, RAW, DER

OPERATORS = {'dpp': 106, 'arriva-city': 89, 'stenbus': 77, 'about-me': 209, 'csad-stredni-cechy': 398, 'martin-uher': 64, 'csad-polkost': 459,
             'vega-tour': 1224, 'arriva-stredni-cechy': 1329, 'umbrella-city-lines': 11174, 'csad-benesov': 27}

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--state', required=True); ap.add_argument('--cars', action='store_true')
    a = ap.parse_args(); s = state(a.state)
    g = os.path.join(RAW, 'gtfs', s['gtfs']['raw'], 'gtfs.zip')
    if not os.path.exists(g): fetch(s['gtfs']['url'], g)
    d = os.path.join(RAW, 'register', s['register_raw'])
    for slug, oid in OPERATORS.items():
        page = 1
        while True:
            dest = os.path.join(d, f'dpp_bus_{page}.html' if slug == 'dpp' else f'op_{slug}_{page}.html')
            t = open(dest, encoding='utf-8').read() if os.path.exists(dest) else \
                fetch(f'https://seznam-autobusu.cz/seznam?iddopravce={oid}&trakce=autobus&prov=1&vcetneSluzebnich=1&page={page}', dest).decode('utf-8')
            if t.count('first-line" data-car-id') < 100: break
            page += 1
    if a.cars:
        V = load(os.path.join(DER, f'vehicles_{s["register_raw"]}.json'))
        ids = set()
        for p in glob.glob(os.path.join(RAW, 'vypravenost', '*', '*.html')):
            ids |= set(re.findall(r'/vuz/(\d+)/vypravenost', open(p, encoding='utf-8').read()))
        for cid in sorted(ids - set(V)):
            dest = os.path.join(d, f'vuz_{cid}.html')
            if not os.path.exists(dest): fetch(f'https://seznam-autobusu.cz/vuz/{cid}', dest)
    print('sources ok')

if __name__ == '__main__':
    main()
