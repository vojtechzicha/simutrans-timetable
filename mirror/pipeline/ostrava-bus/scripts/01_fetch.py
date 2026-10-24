"""Download the raw inputs into data/raw/<snapshot>/ exactly as fetched.

usage: python 01_fetch.py [--jdf] [--fleet] [--records] [--history]      (no flag = the first three)
  --jdf      CIS JŘ bus timetable export JDF.zip (~107 MB, one request; all Czech bus lines, DPO's are 915xxx)
  --fleet    seznam-autobusu register of DPO buses: trakce=autobus (3 pages) and trakce=elektrobus (1 page),
             saved as fleet/p<N>.html and fleet/e_p<N>.html; the depot cell is AH (Hranečník) or AP (Poruba)
  --records  seznam-autobusu ODIS vypravenost for each day in config.records.days (few DPO bus rows; a cross-check)
  --history  seznam-autobusu ODIS vypravenost per line since config.history.since (weekday records up to
             28 Jun 2026, when tram-bus.cz stopped), saved as history.json; several hundred pages at 2 s each
The live feed is polled separately by 01b_live_poll.py (it has no history).
"""
import json, os, sys
from lib import CONFIG, RAW, http, parse_vypravenost, next_page, record_date, day, load

args = set(sys.argv[1:]) or {'--jdf', '--fleet', '--records'}
os.makedirs(RAW, exist_ok=True)
if '--jdf' in args:
    b = http(CONFIG['jdf']['url'], binary=True, pause=0)
    open(os.path.join(RAW, 'JDF.zip'), 'wb').write(b); print('JDF.zip', len(b), 'bytes')
if '--fleet' in args:
    os.makedirs(os.path.join(RAW, 'fleet'), exist_ok=True)
    for prefix, url in CONFIG['fleet']['list_urls'].items():
        p = 1
        while True:
            s = http(url + (f'&page={p}' if p > 1 else ''))
            open(os.path.join(RAW, 'fleet', f'{prefix}{p}.html'), 'w', encoding='utf-8').write(s)
            print('fleet', prefix, p)
            if not next_page(s, p): break
            p += 1
if '--records' in args:
    for d in CONFIG['records']['days']:
        rows, p = [], 1
        while True:
            s = http(CONFIG['records']['url'].format(date=d) + (f'&strana={p}' if p > 1 else ''))
            rows += parse_vypravenost(s)
            if not next_page(s, p): break
            p += 1
        json.dump(rows, open(os.path.join(RAW, f'records_{d}.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
        print('records', d, len(rows), 'rows')
if '--history' in args:
    since = day(CONFIG['history']['since']); out = {}
    for line in sorted((L for L, v in load('line_class.json').items() if v['cls'] == 'peak'), key=int):
        rows = []; p = 1
        while True:
            s = http(CONFIG['history']['url'].format(line=line) + (f'&strana={p}' if p > 1 else ''))
            r = [x for x in parse_vypravenost(s) if x['line'] == line]
            rows += r
            last = record_date(r[-1]['date']) if r else None
            if not last or last < since or not next_page(s, p): break
            p += 1
        out[line] = rows
        print('history line', line, len(rows), 'records', flush=True)
        json.dump(out, open(os.path.join(RAW, 'history.json'), 'w', encoding='utf-8'), ensure_ascii=False)
