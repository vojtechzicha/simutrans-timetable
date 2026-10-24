"""Poll DPO's live vehicle feed and store every tram snapshot.

usage: python 01b_live_poll.py [until YYYY-MM-DDTHH:MM]
Writes data/raw/<date of the poll>/live/<YYYYMMDD-HHMM>.json (one file per poll: number, line,
course, trip, model). Every 2 min between 13:00 and 19:00, otherwise every 10 min.
Run it in the background over a real weekday peak to get an observed roster.
"""
import datetime, json, os, sys, time, urllib.request
from lib import ROOT, CONFIG

end = datetime.datetime.fromisoformat(sys.argv[1]) if len(sys.argv) > 1 else datetime.datetime.now() + datetime.timedelta(hours=24)
body = json.dumps(CONFIG['live']['body']).encode()
while datetime.datetime.now() < end:
    now = datetime.datetime.now()
    folder = os.path.join(ROOT, 'data', 'raw', now.date().isoformat(), 'live'); os.makedirs(folder, exist_ok=True)
    try:
        req = urllib.request.Request(CONFIG['live']['url'], data=body, headers={'Content-Type': 'application/json'})
        d = json.load(urllib.request.urlopen(req, timeout=30))
        slim = []
        for v in d['data']:
            x = v.get('data', {})
            if x.get('vehicleType') != 'tram': continue
            td = v.get('transportData') or {}
            slim.append(dict(n=x.get('vehicleNumber'), r=x.get('routeID'), s=x.get('serviceID'), trip=x.get('tripID'),
                             fr=x.get('startStopName'), to=x.get('finalStopName'), model=td.get('model'),
                             mname=(v.get('model') or {}).get('name'), car=td.get('carriage'), comm=td.get('commissioning'),
                             cap=(x.get('occupancy') or {}).get('technicalCapacity')))
        json.dump(slim, open(os.path.join(folder, now.strftime('%Y%m%d-%H%M') + '.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    except Exception as e:
        open(os.path.join(folder, 'errors.log'), 'a').write(f'{now} {e}\n')
    time.sleep(120 if 13 <= now.hour < 19 else 600)
