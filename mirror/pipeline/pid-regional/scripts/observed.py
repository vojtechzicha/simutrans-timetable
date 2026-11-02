"""Every trip of one PID line on a poll day with the bus the live map saw on it:
python observed.py <line> <YYYY-MM-DD> [--from 13:00 --to 19:00]  ->  data/derived/<line>_observed_<date>.json

Per trip of the line (PID GTFS of the service day, any oblast or the Prague city lines): dep, o, d, trip id, and each bus
seen on it while on the trip (statePosition on_track / at_stop): num, type, operator, course (the vehicle window's
"Vůz, oběh": the line/course the bus runs, e.g. 317/5). Also: the 15:00-17:59 subset, and per course the trips of this line
it ran in the window and whether it ran other lines' trips in between (does a course alternate, or run only this line).
"""
import collections, json, os, sys
from common import HOME, DER

L, day = sys.argv[1], sys.argv[2]
a = lambda k, d: sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d
tm = lambda s: int(s.split(':')[0]) * 60 + int(s.split(':')[1]); hm = lambda t: '%d:%02d' % (t // 60 % 24, t % 60)
W = (tm(a('--from', '13:00')), tm(a('--to', '19:00')))
SH = json.load(open(os.path.join(HOME, 'config.json'), encoding='utf-8'))
pd = os.path.join(HOME, SH['live']['dir'], day)
# the line's trips: from the oblast trips files (tid, dep, fr, to), else from ends.json for city lines
trips = {}
for o in SH['oblasti']:
    p = os.path.join(HOME, 'oblasti', o['id'], 'data', 'derived', 'trips.json')
    if not os.path.exists(p): continue
    for k, tr in json.load(open(p, encoding='utf-8')).items():
        for t in tr:
            if t['tid'].split('_')[0] == L or k == L: trips[t['tid']] = dict(dep=t['dep'], o=t['fr'], d=t['to'], tid=t['tid'])
info = {}
for ln in open(os.path.join(pd, 'vehicles.jsonl'), encoding='utf-8'):
    w = json.loads(ln)
    if w['vehicle'] not in info or (w.get('type') and not info[w['vehicle']].get('type')): info[w['vehicle']] = w
span = {}; byveh = collections.defaultdict(dict)
for ln in open(os.path.join(pd, 'polls.jsonl'), encoding='utf-8'):
    r = json.loads(ln); t = tm(r['t'][11:16])
    for v, route, tid, stp, *_ in r['buses']:
        if stp not in ('on_track', 'at_stop'): continue
        k = (v, tid); span.setdefault(k, [t, t, route])[1] = t
        byveh[v].setdefault(tid, [t, t, route])[1] = t
out = []
for tid, x in sorted(trips.items(), key=lambda kv: kv[1]['dep']):
    buses = [v for (v, t_), _ in span.items() if t_ == tid]
    for v in buses or [None]:
        w = info.get(v, {})
        out.append(dict(x, dep=hm(x['dep']), num=v, type=w.get('type'), operator=w.get('operator'), course=w.get('course', '').split(' na ')[-1] if w else None))
inw = [r for r in out if W[0] <= tm(r['dep']) < W[1]]
peak = [r for r in out if 900 <= tm(r['dep']) < 1080]
courses = collections.defaultdict(list)
for r in inw:
    if r['num']: courses[r['course'] or '?'].append(r['num'])
alt = {}
for c, vs in courses.items():
    for v in set(vs):
        seq = sorted((f, route) for tid, (f, l, route) in byveh[v].items() if W[0] - 60 <= f < W[1] + 60)
        alt[f'{c} bus {v}'] = ' '.join(f'{hm(f)}:{route}' for f, route in seq)
res = dict(line=L, day=day, window=[hm(W[0]), hm(W[1])], trips=inw, peak_15_18=peak,
           courses={c: sorted(set(vs)) for c, vs in courses.items()}, bus_days=alt,
           unobserved=[r['dep'] + ' ' + r['o'] for r in inw if not r['num']],
           note='bus_days: each bus seen on the line, its trips 1 h around the window as start time:line (from the live map); '
                'course = the vehicle window\'s "Vůz, oběh" (line/course), read once per bus and line')
p = os.path.join(DER, f'{L}_observed_{day}.json')
json.dump(res, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(p, len(inw), 'trips in the window,', sum(1 for r in inw if r['num']), 'observed;', len(courses), 'courses:', dict(courses))
