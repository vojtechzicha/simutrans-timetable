"""Poll DPO's live vehicle feed and store every bus snapshot.

usage: python 01b_live_poll.py [until YYYY-MM-DDTHH:MM]
Writes data/raw/<date of the poll>/live/<YYYYMMDD-HHMM>.json (one file per poll: number, line,
course, trip, from/to, model, length hint). Every 1 min between 13:00 and 19:30, otherwise every 10 min.
Same feed as the tram poller (pipeline/ostrava), filtered to vehicleType 'bus'.
Run it in the background over a real weekday peak to get an observed roster.
"""
import datetime, json, os, sys, time, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = 'https://dashboard.dpo.cz/api/server'
BODY = json.dumps({"endpoint": "transport/vehicle/list?page=dashboard&withTripId=1&vehicleStates=ride",
                   "apiMethod": "GET", "data": {}, "host": None}).encode()

end = datetime.datetime.fromisoformat(sys.argv[1]) if len(sys.argv) > 1 else datetime.datetime.now() + datetime.timedelta(hours=24)
while datetime.datetime.now() < end:
    now = datetime.datetime.now()
    folder = os.path.join(ROOT, 'data', 'raw', now.date().isoformat(), 'live'); os.makedirs(folder, exist_ok=True)
    try:
        req = urllib.request.Request(URL, data=BODY, headers={'Content-Type': 'application/json'})
        d = json.load(urllib.request.urlopen(req, timeout=30))
        slim = []
        for v in d['data']:
            x = v.get('data', {})
            if x.get('vehicleType') != 'bus': continue
            td = v.get('transportData') or {}
            pos = ((v.get('config') or {}).get('map') or {}).get('position') or {}
            slim.append(dict(n=x.get('vehicleNumber'), ag=x.get('agencyID'), r=x.get('routeID'), s=x.get('serviceID'), trip=x.get('tripID'),
                             fr=x.get('startStopName'), to=x.get('finalStopName'), last=x.get('lastStopName'),
                             delay=x.get('delay'), eng=x.get('engineType'),
                             model=td.get('model'), mname=(v.get('model') or {}).get('name'),
                             joints=td.get('jointCount'), seat=td.get('seating'), stand=td.get('standing'),
                             comm=td.get('commissioning'), lat=pos.get('lat'), lng=pos.get('lng')))
        json.dump(slim, open(os.path.join(folder, now.strftime('%Y%m%d-%H%M') + '.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    except Exception as e:
        open(os.path.join(folder, 'errors.log'), 'a').write(f'{now} {e}\n')
    time.sleep(60 if (13 <= now.hour < 19 or (now.hour == 19 and now.minute < 30)) else 600)
