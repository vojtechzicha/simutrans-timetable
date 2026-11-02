"""Poll the PID live vehicle map (mapa.pid.cz, getData.php) -> data/raw/live/<date>/polls.jsonl and vehicles.jsonl.

Every minute 12:00-20:00, every 3 min 5:00-12:00 and 20:00-23:00, every 10 min at night, until the end time given.
Each poll keeps the buses (routeType 3) and, from 2 Nov evening, the trolleybuses (11): [vehicle, route, tripId (= GTFS
trip_id), statePosition, delay s, lat, lon, routeType] (rows before that have no routeType).
The first time a bus is seen on a line (not a Prague city line 100-299), its vehicle window (getVehicleWindow.php) is read once, at most one every 3 s:
operator ("Dopravce"), type ("Typ vozu"), course ("Vůz, oběh: #9513 na 737/64" = vehicle 9513 runs course 64 of line 737)
and the seznam-autobusu car id from the vehicle card link. The poller asks Windows not to sleep while it runs (the Ostrava
bus poll of 30 Sep lost half its peak to sleep).

usage: python 01_live_poll.py 2026-11-03T20:15          (start it detached; it writes poll.log beside the data)
"""
import ctypes, datetime, html, http.cookiejar, json, os, queue, re, sys, threading, time, urllib.request

BASE = 'https://mapa.pid.cz/'
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
BOUNDS = [11.9, 48.9, 16.4, 51.15]          # every PID line, with the far ends of the long lines
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'raw', 'live')
until = datetime.datetime.fromisoformat(sys.argv[1])
jar = http.cookiejar.CookieJar()
op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
HEAD = {'User-Agent': UA, 'Content-Type': 'application/json', 'Origin': BASE.rstrip('/'), 'Referer': BASE,
        'X-Requested-With': 'XMLHttpRequest', 'Accept': 'application/json, text/javascript, */*; q=0.01'}

def awake():
    try: ctypes.windll.kernel32.SetThreadExecutionState(0x80000000 | 0x00000001)   # ES_CONTINUOUS | ES_SYSTEM_REQUIRED
    except Exception: pass
def session():
    op.open(urllib.request.Request(BASE, headers={'User-Agent': UA}), timeout=60).read()
def post(path, body):
    req = urllib.request.Request(BASE + path, data=json.dumps(body).encode(), headers=HEAD)
    return json.loads(op.open(req, timeout=90).read().decode('utf-8-sig'))
def log(*a):
    print(datetime.datetime.now().strftime('%m-%d %H:%M:%S'), *a, flush=True)

def tx(h): return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' | ', h)))
def window(v, rt=3):
    d = post('getVehicleWindow.php', dict(route_type=rt, vehicle=v, past_time=False))
    h = d.get('infowindow_content') or ''; t = tx(h)
    g = lambda lab: (m.group(1).strip() if (m := re.search(lab + r':\s*\|[\s|]*([^|]+)', t)) else '')
    car = re.search(r'seznam-autobusu\.cz/vuz/(\d+)', h)
    return dict(vehicle=v, trip=d.get('trip_id'), operator=g('Dopravce'), type=g('Typ vozu'), course=g('Vůz, oběh'),
                car_id=car.group(1) if car else None)

asked = set(); wq = queue.Queue()
def window_worker():
    while True:
        day, v, route, rt = wq.get()
        try:
            w = window(v, rt); w.update(seen_route=route, route_type=rt, at=datetime.datetime.now().isoformat(timespec='seconds'))
            out = os.path.join(ROOT, day); os.makedirs(out, exist_ok=True)
            with open(os.path.join(out, 'vehicles.jsonl'), 'a', encoding='utf-8') as f: f.write(json.dumps(w, ensure_ascii=False) + '\n')
        except Exception as e:
            log('window error', v, e); asked.discard((day, v, route))
        time.sleep(3)
threading.Thread(target=window_worker, daemon=True).start()

awake(); session(); fails = 0
while datetime.datetime.now() < until:
    now = datetime.datetime.now(); awake()
    day = now.strftime('%Y-%m-%d'); out = os.path.join(ROOT, day); os.makedirs(out, exist_ok=True)
    try:
        d = post('getData.php', dict(action='getData', dimensions=[1920, 1080], bounds=BOUNDS, filter_lin='',
                                     openedVehicleWindow=None, show_delay_sections=False, past_time=False))
        # buses (routeType 3) and, from 2 Nov evening, trolleybuses (11) for the Prague trolleybus sheet (51 and 53 take over 131
        # and 176 from 2 Nov); the route type is the row's last field
        rows = [[t['vehicle'], t['route'], t['tripId'], t.get('statePosition'), t.get('delay'), round(t['lat'], 5), round(t['lon'], 5), t['routeType']]
                for t in d.get('trips') or [] if t.get('routeType') in (3, 11) and t.get('vehicle')]
        with open(os.path.join(out, 'polls.jsonl'), 'a', encoding='utf-8') as f:
            f.write(json.dumps(dict(t=now.isoformat(timespec='seconds'), buses=rows), ensure_ascii=False) + '\n')
        m = now.hour * 60 + now.minute
        if 300 <= m < 1380:
            for v, route, *rest in rows:
                rt = rest[-1]
                # Prague city bus lines are the Prague bus sheet's, except 232, listed as a trolleybus line from 2 Nov (the Prague
                # session asked which vehicles really run it)
                if rt == 3 and route.isdigit() and 100 <= int(route) < 300 and route != '232': continue
                if (day, v, route) not in asked: asked.add((day, v, route)); wq.put((day, v, route, rt))
        log('poll', len(rows), 'buses; window queue', wq.qsize()); fails = 0
    except Exception as e:
        fails += 1; log('poll error', e)
        if fails % 3 == 0:
            try: session()
            except Exception as e2: log('session error', e2)
    m = now.hour * 60 + now.minute
    step = 60 if 720 <= m < 1200 else 180 if 300 <= m < 1380 else 600
    time.sleep(max(5, step - (datetime.datetime.now() - now).total_seconds()))
try: ctypes.windll.kernel32.SetThreadExecutionState(0x80000000)
except Exception: pass
log('done')
