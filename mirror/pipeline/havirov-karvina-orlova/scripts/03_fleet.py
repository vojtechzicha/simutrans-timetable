"""Register pages, live snapshots and line records -> derived/fleet.json, live.json, history.json.

fleet.json   {fleet number: {state, num, type, year, note, plate, vid, cat, full, len, paint}}  carrier 28 (Transdev
             Slezsko), both tractions; state zar active, dilny workshops, sluz service; cat/full/len from config.type_rules.
live.json    {day, files, cars: {fleet number: [[HH:MM, line, course, start, final, branch, licence], ...]}}  every Transdev
             Slezsko bus in the ODIS live map (mpvnet.cz) on the vehicle day, joined by number plate; plates the register
             doesn't know are listed in 'unknown' with their lines.
history.json [[line, fleet number, date, note], ...]  weekday records of the sheet's lines since config.records.since,
             by register id (seznam-autobusu records carry the plate and the vuz id).
"""
import collections, glob, json, os, re
from lib import CONFIG, RAW, parse_fleet_list, save, load, record_date, day, plate_key

C = CONFIG
fleet = {}; byplate = {}; byvid = {}
for f in sorted(glob.glob(os.path.join(RAW, 'fleet', '*.html'))):
    for vid, c in parse_fleet_list(open(f, encoding='utf-8').read()).items():
        if not c['num']: continue
        rule = next((r for r in C['type_rules'] if c['type'] == r[0]), None)
        paint = re.search(r'nátěr:\s*([^*{]*)', c['note'])
        fleet[c['num']] = dict(c, vid=vid, cat=rule[1] if rule else '?', full=rule[2] if rule else c['type'], len=rule[3] if rule else '?',
                               paint=re.sub(r'\s+', ' ', paint.group(1)).strip(' *') if paint else '')
        if c['plate']: byplate[c['plate']] = c['num']
        byvid[vid] = c['num']
pp = os.path.join(RAW, 'plates.json')   # 01d_plates.py: buses seen live that the register list leaves out
for pl, x in (json.load(open(pp, encoding='utf-8')) if os.path.exists(pp) else {}).items():
    if not x: continue
    if x['num'] in fleet:      # in the list under another plate or state (40-1001): the live plate maps to it, and it runs
        byplate[pl] = x['num']; f_ = fleet[x['num']]
        if f_['state'] != 'zar': f_['note'] += f" (register state {f_['state']}; seen live)"; f_['state'] = 'zar'
        continue
    rule = next((r for r in C['type_rules'] if x['type'] == r[0]), None)
    fleet[x['num']] = dict(state='zar', num=x['num'], type=x['type'], year='', note=x['note'] + ' (not in the register list; seen live)', plate=pl, vid=x['vid'],
                           cat=rule[1] if rule else '?', full=rule[2] if rule else x['type'], len=rule[3] if rule else '?', paint=x['paint'], lookup=True)
    byplate[pl] = x['num']; byvid[x['vid']] = x['num']
save('fleet.json', fleet)
print('fleet', len(fleet), collections.Counter(c['state'] for c in fleet.values()))
print('unmapped active types', collections.Counter(c['type'] for c in fleet.values() if c['cat'] == '?' and c['state'] == 'zar').most_common())

lic = set()
for x in C['jdf']['licences']:
    a, _, b = x.partition('-'); lic |= {str(i) for i in range(int(a), int(b or a) + 1)}
files = sorted(glob.glob(os.path.join(os.path.dirname(RAW), C['vehicle_day'], 'live', '*.json')))
live = collections.defaultdict(list); unknown = collections.defaultdict(set)
for f in files:
    t = os.path.basename(f)[9:13]; t = t[:2] + ':' + t[2:]
    for v in json.load(open(f, encoding='utf-8'))['transmitters']:
        if v.get('t') != 'H' or not v.get('cn') or not v.get('cr', '').startswith('Transdev Slezsko'): continue
        p = v['cn'].split('|')
        if len(p) < 12: continue
        pl = plate_key(p[11]); n = byplate.get(pl)
        if not n:
            if p[0] in lic: unknown[pl].add(p[1])
            continue
        row = [t, p[1], p[2], p[8], p[9], v['cr'].replace('Transdev Slezsko pr. ', ''), p[0]]
        if not live[n] or live[n][-1][:3] != row[:3]: live[n].append(row)
save('live.json', dict(day=C['vehicle_day'], files=len(files), cars=live, unknown={k: sorted(v) for k, v in unknown.items()}))
print('live', len(files), 'snapshots,', len(live), 'Transdev buses;', len(unknown), 'unknown plates on the sheet lines', dict(list(unknown.items())[:10]))

recs = json.load(open(os.path.join(RAW, 'records.json'), encoding='utf-8'))['lines']
since = day(C['records']['since']); hist = []; miss = collections.Counter()
for L, rows in recs.items():
    for r in rows:
        d = record_date(r['date'])
        if not d or d < since or r['date'][:2] not in ('PO', 'ÚT', 'ST', 'ČT', 'PÁ'): continue
        n = byvid.get(r.get('vid') or '') or byplate.get(plate_key(r['car']))
        if n: hist.append([L, n, d.isoformat(), r['note']])
        else: miss[r['car']] += 1
save('history.json', hist)
print('history weekday records', len(hist), 'not in the register', sum(miss.values()), miss.most_common(5))
