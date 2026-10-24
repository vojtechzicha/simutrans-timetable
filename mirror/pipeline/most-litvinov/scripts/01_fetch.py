"""Download raw inputs into data/raw/<snapshot>/.   python 01_fetch.py [--jdf] [--fleet] [--live]  (no flag = all)
  --jdf    CIS JŘ city timetable export JDF.zip
  --fleet  seznam-autobusu list of DPmML operational trams (all pages)
  --live   one poll of the city of Most live vehicle layer -> live/<time>.json (was empty so far)
Set "snapshot" in config.json to today's date first."""
import datetime, os, sys
from lib import CONFIG, RAW, http, next_page

args = set(sys.argv[1:]) or {'--jdf', '--fleet', '--live'}
os.makedirs(RAW, exist_ok=True)
if '--jdf' in args:
    b = http(CONFIG['jdf']['url'], binary=True, pause=0)
    open(os.path.join(RAW, 'JDF.zip'), 'wb').write(b); print('JDF.zip', len(b))
if '--fleet' in args:
    os.makedirs(os.path.join(RAW, 'fleet'), exist_ok=True); p = 1
    while True:
        s = http(CONFIG['fleet']['list_url'] + (f'&page={p}' if p > 1 else ''))
        open(os.path.join(RAW, 'fleet', f'p{p}.html'), 'w', encoding='utf-8').write(s); print('fleet page', p)
        if not next_page(s, p): break
        p += 1
if '--live' in args:
    os.makedirs(os.path.join(RAW, 'live'), exist_ok=True)
    s = http(CONFIG['live']['url'], pause=0)
    f = os.path.join(RAW, 'live', datetime.datetime.now().strftime('%Y%m%d-%H%M') + '.json')
    open(f, 'w', encoding='utf-8').write(s); print('live', f, len(s), 'bytes')
