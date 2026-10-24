"""Raw fleet pages, history records and live snapshots -> derived/fleet.json, records.json, live.json.

fleet.json   {number: {depot, state, type, year, note}}   state: zar = active, dilny = in workshops,
             doco = out of service, sluz = service vehicle (seznam-autobusu CSS classes)
records.json weekday history records usable for type shares: [line, unit type, [numbers], weight, course, note]
             weight: 2 for records from history.weight_from on, x1.5 when marked "odpoledne" (afternoon);
             morning-only records ("ráno") are left out
live.json    {number: {line: [courses]}} from every live snapshot of the snapshot day
"""
import collections, glob, json, os, re
from lib import CONFIG, RAW, parse_fleet_list, record_date, day, save

def tcat(n):
    for t, a, b in CONFIG['type_ranges']:
        if a <= n <= b: return t
    return '?'

fleet = {}
for name, depot in CONFIG['fleet']['depots'].items():
    for f in sorted(glob.glob(os.path.join(RAW, 'fleet', f'{depot}_p*.html'))):
        for c in parse_fleet_list(open(f, encoding='utf-8').read()).values():
            m = re.match(r'\d+', c['num'])
            if m: fleet[int(m.group())] = dict(c, depot=name, cat=tcat(int(m.group())))
save('fleet.json', fleet)
print('fleet', len(fleet), collections.Counter((c['depot'], c['state']) for c in fleet.values()))

recs, lastseen = [], {}
hpath = os.path.join(RAW, 'history.json')
if os.path.exists(hpath):
    since, wfrom = day(CONFIG['history']['since']), day(CONFIG['history']['weight_from'])
    for L, rows in json.load(open(hpath, encoding='utf-8')).items():
        for r in rows:
            d = record_date(r['date'])
            nums = [int(x) for x in re.findall(r'\d{3,4}', r['car'])]
            for n in nums: lastseen[n] = max(lastseen.get(n, ''), d.isoformat() if d else '')
            if not d or d < since or r['date'][:2] not in ('PO', 'ÚT', 'ST', 'ČT', 'PÁ') or not nums: continue
            if 'ráno' in r['note'] and 'odpoledne' not in r['note']: continue
            # 9xx courses are the late-evening runs (out to the night lines 18/19 and to 8, 11 after the peak); their
            # single cars on 4 and 7 never run there at 16:00 (user, 18 Oct 2026), so they are left out of the type history
            if str(r['kurz']).startswith(tuple(CONFIG['history'].get('exclude_course_prefixes', []))): continue
            t = tcat(nums[0])
            if t == '?': continue
            if len(nums) > 1: t = '2×' + t
            w = (2.0 if d >= wfrom else 1.0) * (1.5 if 'odpoledne' in r['note'] else 1.0)
            recs.append([L, t, nums, w, r['kurz'], r['note']])
save('records.json', dict(records=recs, lastseen=lastseen))
print('history records used', len(recs))

live = collections.defaultdict(lambda: collections.defaultdict(set))
files = sorted(glob.glob(os.path.join(RAW, 'live', '*.json')))
# config.live_until (YYYYMMDD-HHMM): ignore snapshots the poller wrote after the published roster was built
files = [f for f in files if os.path.basename(f)[:13] <= CONFIG.get('live_until', '99999999-9999')]
for f in files:
    for v in json.load(open(f, encoding='utf-8')):
        live[v['n']][v['r']].add(v['s'])
save('live.json', dict(files=len(files), cars={n: {L: sorted(x for x in s if x is not None) for L, s in d.items()} for n, d in live.items()}))
print('live cars', len(live), 'from', len(files), 'snapshots')
