"""Poll the ODIS live vehicle map (mpvnet.cz, the map behind mapa.kodis.cz) -> data/raw/<date>/live/<YYYYMMDD-HHMM>.json.
Every minute in 13:00-19:30, otherwise every 10 min, until the given end time. The whole ODIS region is fetched, so the
snapshots also serve the Ostrava sheets. Each transmitter row: cr = carrier and branch, cn = 'licence|line|trip|from stop|
delay|...|start|final|1|PLATE|...', dt/tm = last fix. The plate maps to the seznam-autobusu register (fleet number).
The poller asks Windows not to sleep while it runs (the Ostrava bus poller lost most of its peak to sleep).

usage: python 01b_live_poll.py 2026-10-20T19:45"""
import ctypes, datetime, json, os, sys, time, urllib.request

URL = 'https://mpvnet.cz/Odis/map/mapData'
BODY = json.dumps(dict(w=16.7, s=49.4, e=18.84, n=50.45, zoom=13, showStops=False, mapFilterId=None)).encode()
HEAD = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0 Safari/537.36',
        'Content-Type': 'application/json; charset=utf-8', 'Origin': 'https://mpvnet.cz', 'Referer': 'https://mpvnet.cz/odis/map'}
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'raw')
until = datetime.datetime.fromisoformat(sys.argv[1])
try: ctypes.windll.kernel32.SetThreadExecutionState(0x80000000 | 0x00000001)   # ES_CONTINUOUS | ES_SYSTEM_REQUIRED
except Exception: pass
while datetime.datetime.now() < until:
    now = datetime.datetime.now()
    out = os.path.join(ROOT, now.strftime('%Y-%m-%d'), 'live'); os.makedirs(out, exist_ok=True)
    try:
        req = urllib.request.Request(URL, data=BODY, headers=HEAD)
        b = urllib.request.urlopen(req, timeout=60).read()
        d = json.loads(b.decode('utf-8-sig'))
        open(os.path.join(out, now.strftime('%Y%m%d-%H%M') + '.json'), 'w', encoding='utf-8').write(
            json.dumps(dict(fetched=now.isoformat(timespec='seconds'), transmitters=d.get('transmitters') or []), ensure_ascii=False))
        print(now.strftime('%H:%M'), len(d.get('transmitters') or []), flush=True)
    except Exception as e:
        print(now.strftime('%H:%M'), 'error', e, flush=True)
    busy = 13 * 60 <= now.hour * 60 + now.minute < 19 * 60 + 30
    step = 60 if busy else 600
    time.sleep(max(5, step - (datetime.datetime.now() - now).total_seconds()))
