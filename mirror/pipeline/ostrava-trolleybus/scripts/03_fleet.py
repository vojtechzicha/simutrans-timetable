"""Raw register pages, day records and live snapshots -> derived/fleet.json, records.json, live.json.

fleet.json   {number: {state, type, year, note, cat, full, battery, depot}}  state: zar active, sluz service
             vehicle (driving school), muz museum (seznam-autobusu CSS classes); cat/full from config.type_rules
records.json {date: [{line, kurz, cars, note, bus}]}  every ODIS row of a DPO trolleybus line (101–113) that day;
             bus = True when the row is a bus on a trolleybus line (class car-on-line-bus)
live.json    {number: [[HH:MM, line, course, from, to, longitude, last stop], ...]} every sighting of the vehicle day, in time order
"""
import collections, glob, json, os, re
from lib import CONFIG, RAW, parse_fleet_list, save, record_date, day

C = CONFIG
def battery(n): return any(a <= n <= b for a, b in C['battery_cars']['ranges'])
fleet = {}
for f in sorted(glob.glob(os.path.join(RAW, 'fleet', 'p*.html'))):
    for c in parse_fleet_list(open(f, encoding='utf-8').read()).values():
        m = re.match(r'\d{4}$', c['num'])
        if not m: continue
        n = int(m.group())
        rule = next((r for r in C['type_rules'] if c['type'] == r[0]), None)
        fleet[n] = dict(c, cat=rule[1] if rule else '?', full=rule[2] if rule else c['type'], battery=battery(n), depot=C['fleet']['depot'])
save('fleet.json', fleet)
print('fleet', len(fleet), collections.Counter((c['state'], c['cat']) for c in fleet.values()))

lines = set(C['jdf']['lines'].values()) | {v.split()[-1] for v in C['jdf']['excluded_lines'].values()}
recs = {}
for f in sorted(glob.glob(os.path.join(RAW, 'records_*.json'))):
    d = os.path.basename(f)[8:18]; out = []
    for r in json.load(open(f, encoding='utf-8')):
        if r['line'] not in lines or not ('trolley' in r['cls'] or 'bus' in r['cls']): continue
        out.append(dict(line=r['line'], kurz=r['kurz'], cars=[int(x) for x in re.findall(r'\d{3,4}', r['car'])], note=r['note'], bus='bus' in r['cls']))
    recs[d] = out
    print('records', d, len(out), 'rows', sum(x['bus'] for x in out), 'buses')
save('records.json', recs)

live = collections.defaultdict(list)
files = sorted(glob.glob(os.path.join(RAW, 'live', '*.json')))
for f in files:
    t = os.path.basename(f)[9:13]; t = t[:2] + ':' + t[2:]
    for v in json.load(open(f, encoding='utf-8')):
        live[v['n']].append([t, v['r'], v['s'], v['fr'], v['to'], v.get('lng'), v.get('last')])
save('live.json', dict(files=len(files), first=os.path.basename(files[0])[:13] if files else None,
                       last=os.path.basename(files[-1])[:13] if files else None, cars=live))
print('live cars', len(live), 'from', len(files), 'snapshots')

# history: weekday ODIS records per line since config.history.since → [[line, car, course, date, note], ...]
hist = []
hp = os.path.join(RAW, 'history.json')
if os.path.exists(hp):
    since = day(C['history']['since'])
    for L, rows in json.load(open(hp, encoding='utf-8')).items():
        for r in rows:
            d = record_date(r['date'])
            if not d or d < since or r['date'][:2] not in ('PO', 'ÚT', 'ST', 'ČT', 'PÁ'): continue
            nums = [int(x) for x in re.findall(r'\d{4}', r['car'])]
            if nums: hist.append([L, nums[0], r['kurz'], d.isoformat(), r['note']])
save('history.json', hist)
print('history weekday records', len(hist))
