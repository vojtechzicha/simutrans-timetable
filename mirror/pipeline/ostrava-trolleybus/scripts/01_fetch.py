"""Download the raw inputs into data/raw/<snapshot>/ exactly as fetched.

usage: python 01_fetch.py [--jdf] [--fleet] [--records] [--history]      (no flag = the first three)
  --jdf      CIS JŘ city timetable export JDF.zip (~30 MB, one request; the same file as the tram pipeline's)
  --fleet    seznam-autobusu register of DPO trolleybuses (trakce=trolejbus, all depots; one depot "TR")
  --records  seznam-autobusu ODIS vypravenost for each day in config.records.days (/vypravenost/odis/vypis?datum=),
             every row of the day saved as records_<date>.json; the scripts keep the "car-on-line-trolley" rows
Set "snapshot" in config.json to today's date first, so an update never overwrites older raw data.
  --history  ODIS vypravenost per line since config.history.since → history.json (line rosters)
The live feed is polled separately by 01b_live_poll.py (it has no history).
"""
import json, os, sys
from lib import CONFIG, RAW, http, parse_vypravenost, next_page, record_date, day

args = set(sys.argv[1:]) or {'--jdf', '--fleet', '--records'}
os.makedirs(RAW, exist_ok=True)

if '--jdf' in args:
    b = http(CONFIG['jdf']['url'], binary=True, pause=0)
    open(os.path.join(RAW, 'JDF.zip'), 'wb').write(b)
    print('JDF.zip', len(b), 'bytes')

if '--fleet' in args:
    os.makedirs(os.path.join(RAW, 'fleet'), exist_ok=True)
    p = 1
    while True:
        s = http(CONFIG['fleet']['list_url'] + (f'&page={p}' if p > 1 else ''))
        open(os.path.join(RAW, 'fleet', f'p{p}.html'), 'w', encoding='utf-8').write(s)
        print('fleet page', p)
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
        print('records', d, len(rows), 'rows,', sum('trolley' in r['cls'] for r in rows), 'trolleybus')

if '--history' in args:
    since = day(CONFIG['history']['since']); out = {}
    for line in CONFIG['jdf']['lines'].values():
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
