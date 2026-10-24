"""Download the raw inputs into data/raw/<snapshot>/ exactly as fetched.

usage: python 01_fetch.py [--jdf] [--fleet] [--history]      (no flag = --jdf --fleet)
  --jdf      CIS JŘ city timetable export JDF.zip (~30 MB, one request)
  --fleet    seznam-autobusu fleet list of each tram depot (a few pages)
  --history  seznam-autobusu vypravenost records per tram line since config.history.since
             (~270 pages at 2 s each, ~10 min). Saved as history.json = the parsed table rows.
Set "snapshot" in config.json to today's date first, so an update never overwrites older raw data.
"""
import json, os, sys
from lib import CONFIG, RAW, http, parse_vypravenost, next_page, record_date, day

args = set(sys.argv[1:]) or {'--jdf', '--fleet'}
os.makedirs(RAW, exist_ok=True)

if '--jdf' in args:
    b = http(CONFIG['jdf']['url'], binary=True, pause=0)
    open(os.path.join(RAW, 'JDF.zip'), 'wb').write(b)
    print('JDF.zip', len(b), 'bytes')

if '--fleet' in args:
    os.makedirs(os.path.join(RAW, 'fleet'), exist_ok=True)
    for name, depot in CONFIG['fleet']['depots'].items():
        p = 1
        while True:
            url = CONFIG['fleet']['list_url'].format(depot=depot) + (f'&page={p}' if p > 1 else '')
            s = http(url)
            open(os.path.join(RAW, 'fleet', f'{depot}_p{p}.html'), 'w', encoding='utf-8').write(s)
            print('fleet', name, 'page', p)
            if not next_page(s, p): break
            p += 1

if '--history' in args:
    since = day(CONFIG['history']['since']); out = {}
    for line in CONFIG['history']['lines']:
        rows = []; p = 1
        while True:
            s = http(CONFIG['history']['url'].format(line=line) + (f'&strana={p}' if p > 1 else ''))
            r = [x for x in parse_vypravenost(s) if x['line'] == line]
            rows += r
            last = record_date(r[-1]['date']) if r else None
            if not last or last < since or not next_page(s, p): break
            p += 1
        out[line] = rows
        print('history line', line, len(rows), 'records')
        json.dump(out, open(os.path.join(RAW, 'history.json'), 'w', encoding='utf-8'), ensure_ascii=False)
