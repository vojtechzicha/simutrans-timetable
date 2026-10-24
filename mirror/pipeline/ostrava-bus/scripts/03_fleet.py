"""Raw register pages, day records and live snapshots -> derived/fleet.json, records.json, live.json.

fleet.json   {number: {state, type, year, note, cat, full, depot, length}}  state: zar active, dilny workshops,
             sluz service, muz museum; depot from the register's depot cell (AH Hranečník, AP Poruba; a trailing
             * is dropped); cat/full/length from config.type_rules
records.json {date: [{line, kurz, cars, note}]}  ODIS rows of DPO bus lines (class car-on-line-bus)
live.json    {mode, day, window, cars: {number: [[HH:MM, line, course, from, to, longitude, last stop], ...]}}
             mode 'peak' = the vehicle day's peak; 'provisional' = config.live.provisional (evening before)
history.json [[line, car, course, date, note], ...] weekday ODIS records since config.history.since
"""
import collections, glob, json, os, re
from lib import CONFIG, RAW, parse_fleet_list, save, load, record_date, day

C = CONFIG
fleet = {}
for f in sorted(glob.glob(os.path.join(RAW, 'fleet', '*.html'))):
    s = open(f, encoding='utf-8').read()
    for cid, c in parse_fleet_list(s).items():
        m = re.match(r'\d{4}$', c['num'])
        if not m: continue
        dm = re.search(r'data-car-id="%s">\s*<td class=\'plates\'>.*?<td class="depots">(.*?)</td>' % cid, s, flags=re.S)
        dep = re.sub(r'<[^>]+>|\s|\*', '', dm.group(1)) if dm else ''
        rule = next((r for r in C['type_rules'] if c['type'] == r[0]), None)
        fleet[int(m.group())] = dict(c, cat=rule[1] if rule else '?', full=rule[2] if rule else c['type'],
                                     depot=C['fleet']['depots'].get(dep, dep), depot_code=dep)
save('fleet.json', fleet)
print('fleet', len(fleet), collections.Counter((c['state'], c['depot']) for c in fleet.values()))
print('unmapped active types', collections.Counter(c['type'] for c in fleet.values() if c['cat'] == '?' and c['state'] == 'zar'))

lines = set(load('line_class.json'))
recs = {}
for f in sorted(glob.glob(os.path.join(RAW, 'records_*.json'))):
    d = os.path.basename(f)[8:18]
    recs[d] = [dict(line=r['line'], kurz=r['kurz'], cars=[int(x) for x in re.findall(r'\d{4}', r['car'])], note=r['note'])
               for r in json.load(open(f, encoding='utf-8')) if r['line'] in lines and 'bus' in r['cls']]
    print('records', d, len(recs[d]))
save('records.json', recs)

# live: the vehicle day's peak if it has snapshots in config.live.window, else the provisional evening observation
def snaps(d): return sorted(glob.glob(os.path.join(os.path.dirname(RAW), d, 'live', '*.json')))
def hhmm_of(f): t = os.path.basename(f)[9:13]; return t[:2] + ':' + t[2:]
W = C['live']['window']; P = C['live']['provisional']
if any(W[0] <= hhmm_of(f) <= W[1] for f in snaps(C['vehicle_day'])): mode, vd, win = 'peak', C['vehicle_day'], W
else: mode, vd, win = 'provisional', P['day'], P['window']
live = collections.defaultdict(list)
files = snaps(vd)
for f in files:
    t = hhmm_of(f)
    for v in json.load(open(f, encoding='utf-8')):
        live[v['n']].append([t, v['r'], v['s'], v['fr'], v['to'], v.get('lng'), v.get('last')])
save('live.json', dict(mode=mode, day=vd, window=win, files=len(files), cars=live))
print('live', mode, vd, win, 'cars', len(live), 'from', len(files), 'snapshots')

# history: weekday records per line since config.history.since (school year, to 28 Jun 2026)
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
