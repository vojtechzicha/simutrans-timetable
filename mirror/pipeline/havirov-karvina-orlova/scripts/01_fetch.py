"""Raw inputs -> data/raw/<snapshot>/: the bus JDF, Transdev Slezsko's register and every line's seznam-autobusu records.

usage: python 01_fetch.py [--jdf] [--fleet] [--records]   (no flag = all)
- --jdf: the CIS JŘ bus export (~107 MB).
- --fleet: carrier 28 register pages (autobus and elektrobus traction), paginated with &page=N.
- --records: each line's ODIS vypravenost back to config.records.since, and every ODIS record of the vehicle day.
The live feed has no history: poll it with 01b_live_poll.py on the vehicle day itself."""
import json, os, sys, urllib.request
from lib import CONFIG, RAW, http, parse_vypravenost, next_page, record_date, day, load

args = set(sys.argv[1:]) or {'--jdf', '--fleet', '--records'}
os.makedirs(RAW, exist_ok=True)
if '--jdf' in args:
    req = urllib.request.Request(CONFIG['jdf']['url'], headers={'User-Agent': 'Mozilla/5.0'})
    open(os.path.join(RAW, 'JDF.zip'), 'wb').write(urllib.request.urlopen(req, timeout=900).read()); print('JDF')
if '--fleet' in args:
    os.makedirs(os.path.join(RAW, 'fleet'), exist_ok=True)
    for k, url in CONFIG['fleet']['list_urls'].items():
        p = 1
        while True:
            s = http(url + (f'&page={p}' if p > 1 else ''))
            open(os.path.join(RAW, 'fleet', f'{k}{p}.html'), 'w', encoding='utf-8').write(s); print('fleet', k, p)
            if not next_page(s, p) or p >= 30: break
            p += 1
if '--records' in args:
    R = CONFIG['records']; since = day(R['since']); recs = {}
    lines = sorted(load('line_class.json'))
    for L in lines:
        p = 1; recs[L] = []
        while True:
            s = http(R['line_url'].format(line=L) + (f'&strana={p}' if p > 1 else ''))
            got = parse_vypravenost(s); recs[L] += got
            # the pages are not in date order, so every page is read (filtered by date in 03_fleet.py)
            if not got or not next_page(s, p) or p >= 60: break
            p += 1
        print('line', L, len(recs[L]), 'records')
    dayr = []; p = 1
    while True:
        s = http(R['day_url'].format(date=CONFIG['vehicle_day']) + (f'&strana={p}' if p > 1 else ''))
        dayr += parse_vypravenost(s)
        if not next_page(s, p) or p >= 40: break
        p += 1
    print('day', CONFIG['vehicle_day'], len(dayr))
    json.dump(dict(lines=recs, day=dayr), open(os.path.join(RAW, 'records.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
