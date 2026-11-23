"""Poll the VDV live vehicle map (mapavdv.kr-vysocina.cz, Kraj Vysočina) -> data/raw/live/<date>/.

The map keeps no history: poll on the vehicle day. Every minute 05:00-20:00, otherwise every 5 min, until the end time.
- points/<HHMMSS>.json.gz: the whole GetPoints answer as fetched (every VDV vehicle: id, lat/lng, text = licence,
  finalStopName, delay; a few rows also carry `number`, a fleet number or plate). A bus shows up twice, as a BUS row and
  an UNKNOWN row at the same place.
- info.jsonl: for every point on the sheet's licences, the info window (OpenInfoWindow) parsed to licence / trip and
  "Číslo vozidla" (fleet number such as 3-4515, or a plate such as 7J96315); fetched when the id is new and again every
  15 min while it stays on the map. The raw window text is kept in the row.
The poller asks Windows not to sleep while it runs.

usage: python -X utf8 01_live_poll.py 2026-11-24T20:00"""
import ctypes, datetime, gzip, html, json, os, re, sys, time, urllib.request

BASE = 'https://mapavdv.kr-vysocina.cz/'
HEAD = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest', 'Referer': BASE, 'Accept-Language': 'cs,en;q=0.8'}
LICENCES = {'355001', '355002', '355003', '355004', '357250'}
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'raw', 'live')
REFETCH = 15 * 60


def get(path, timeout=30):
    req = urllib.request.Request(BASE + path, headers=HEAD)
    return urllib.request.urlopen(req, timeout=timeout).read().decode('utf-8-sig')


def parse_info(raw):
    text = html.unescape(re.sub(r'<[^>]+>', ' ', raw))
    text = re.sub(r'\s+', ' ', text).strip()
    m = re.search(r'Linka / spoj (\d+) / (\d+)', text)
    v = re.search(r'Číslo vozidla (\S+)', text)
    last = re.search(r'Poslední zastávka (.+?) Linka / spoj', text)
    return dict(licence=m and m.group(1), trip=m and int(m.group(2)), vehicle=v and v.group(1),
                last_stop=last and last.group(1).strip(), text=text[:600])


until = datetime.datetime.fromisoformat(sys.argv[1])
try: ctypes.windll.kernel32.SetThreadExecutionState(0x80000000 | 0x00000001)   # ES_CONTINUOUS | ES_SYSTEM_REQUIRED
except Exception: pass
seen = {}   # point id -> last info fetch (epoch)
while datetime.datetime.now() < until:
    now = datetime.datetime.now()
    day = os.path.join(ROOT, now.strftime('%Y-%m-%d'))
    os.makedirs(os.path.join(day, 'points'), exist_ok=True)
    n_info = 0
    try:
        raw = get('Ajax/GetPoints')
        pts = json.loads(raw)
        with gzip.open(os.path.join(day, 'points', now.strftime('%H%M%S') + '.json.gz'), 'wt', encoding='utf-8') as f:
            f.write(json.dumps(dict(fetched=now.isoformat(timespec='seconds'), points=pts), ensure_ascii=False))
        for p in pts:
            if p.get('text') not in LICENCES: continue
            if time.time() - seen.get(p['id'], 0) < REFETCH: continue
            try:
                info = parse_info(get('Ajax/OpenInfoWindow?id=%d' % p['id']))
            except Exception as e:
                info = dict(error=str(e))
            seen[p['id']] = time.time()
            n_info += 1
            row = dict(fetched=datetime.datetime.now().isoformat(timespec='seconds'), id=p['id'], point=p, **info)
            with open(os.path.join(day, 'info.jsonl'), 'a', encoding='utf-8') as f:
                f.write(json.dumps(row, ensure_ascii=False) + '\n')
            time.sleep(1)
        print(now.strftime('%H:%M:%S'), len(pts), 'points,', n_info, 'info windows', flush=True)
    except Exception as e:
        print(now.strftime('%H:%M:%S'), 'error', e, flush=True)
    busy = 5 * 60 <= now.hour * 60 + now.minute < 20 * 60
    step = 60 if busy else 300
    time.sleep(max(5, step - (datetime.datetime.now() - now).total_seconds()))
try: ctypes.windll.kernel32.SetThreadExecutionState(0x80000000)
except Exception: pass
