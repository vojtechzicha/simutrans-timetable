"""VDV live map poll (01_live_poll.py, data/raw/live/<day>/info.jsonl) -> data/raw/<snapshot>/live_compact.json, the shape the
ODIS regional scripts read: {plates: {key: [[first minute, last minute, licence, line, trip, depot], ...]}, files, span}.

The key is the bus's fleet number (3-4515, 64-10021), so data/derived/fleet.json is keyed the same way (its `plate` is the
fleet number, `reg_plate` the number plate). The map shows each line-250 bus twice, as a row with the fleet number and as a
row with the plate (7J96315) at the same place; rows are paired by licence, trip and position, so a plate row counts for
its fleet number. A plate the poll never pairs stays under the plate.
A sighting is an info window: licence / trip and vehicle at the time it was read. A trip's first and last minute are the
first and last time the bus was seen on it (the poller re-reads an id every 15 min, and every new id at once), stretched by
the point snapshots in between: every snapshot that still shows the same point id on the same licence extends the span.
usage: python -X utf8 01_live.py   (reads config.vehicle_day)
"""
import collections, glob, gzip, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
C = json.load(open(os.path.join(ROOT, 'config.json'), encoding='utf-8'))
day = C['vehicle_day']; src = os.path.join(ROOT, 'data', 'raw', 'live', day)
out = os.path.join(ROOT, 'data', 'raw', C['snapshot'], 'live_compact.json')
LNO = C['jdf'].get('line_numbers', {})
# the depot a sighting counts at: the area's branch (the map names no depot)
BR = lambda lic: next((a['branch'] for a in C['areas'] if lic.startswith(a['prefix'])), '')
if not os.path.exists(os.path.join(src, 'info.jsonl')):
    sys.exit(print('no poll for', day, 'yet:', src))
mins = lambda iso: int(iso[11:13]) * 60 + int(iso[14:16])
rows = [json.loads(l) for l in open(os.path.join(src, 'info.jsonl'), encoding='utf-8') if l.strip()]
rows = [r for r in rows if r.get('licence') and r.get('vehicle') and r['fetched'][:10] == day]
# point id -> (licence, trip, vehicle); the snapshots stretch each id's span
byid = {}
for r in rows:
    byid.setdefault(r['id'], []).append(r)
span = collections.defaultdict(lambda: [10 ** 6, -1])
files = sorted(glob.glob(os.path.join(src, 'points', '*.json.gz')))
ids = set(byid)
pos = collections.defaultdict(dict)       # minute -> id -> (lat, lng, licence)
for f in files:
    d = json.load(gzip.open(f, 'rt', encoding='utf-8'))
    m = mins(d['fetched'])
    for p in d['points']:
        if p['id'] in ids:
            s = span[p['id']]; s[0] = min(s[0], m); s[1] = max(s[1], m)
            pos[m][p['id']] = (round(p['lat'], 3), round(p['lng'], 3), p['text'])
for i, rs in byid.items():
    for r in rs:
        s = span[i]; m = mins(r['fetched']); s[0] = min(s[0], m); s[1] = max(s[1], m)
# plate rows -> fleet numbers: two ids on the same licence and trip seen at the same place in one snapshot
is_fleet = lambda v: '-' in v
alias = {}
for m, ps in pos.items():
    for i, (la, ln, lic) in ps.items():
        for j, (la2, ln2, lic2) in ps.items():
            if i >= j or lic != lic2: continue
            if abs(la - la2) > 0.002 or abs(ln - ln2) > 0.002: continue
            vi = {r['vehicle'] for r in byid[i]}; vj = {r['vehicle'] for r in byid[j]}
            ti = {r['trip'] for r in byid[i]}; tj = {r['trip'] for r in byid[j]}
            if not ti & tj: continue
            for a in vi:
                for b in vj:
                    if is_fleet(a) != is_fleet(b):
                        pl, fl = (b, a) if is_fleet(a) else (a, b)
                        alias.setdefault(pl, collections.Counter())[fl] += 1
alias = {pl: c.most_common(1)[0][0] for pl, c in alias.items()}
plates = {}
for i, rs in byid.items():
    for r in rs:
        key = alias.get(r['vehicle'], r['vehicle'])
        line = LNO.get(r['licence'], r['licence'][-3:])
        lst = plates.setdefault(key, [])
        f, l = span[i]
        row = [f, l, r['licence'], line, r['trip'], BR(r['licence'])]
        if any(x[2:5] == row[2:5] for x in lst):
            for x in lst:
                if x[2:5] == row[2:5]: x[0] = min(x[0], f); x[1] = max(x[1], l)
        else: lst.append(row)
for k in plates: plates[k].sort()
os.makedirs(os.path.dirname(out), exist_ok=True)
json.dump(dict(files=len(files), span=[min((s[0] for s in span.values()), default=0), max((s[1] for s in span.values()), default=0)],
               plates=plates, plate_to_fleet=alias), open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('live', day, len(files), 'snapshots,', len(rows), 'info windows,', len(plates), 'buses;', len(alias), 'plates paired with fleet numbers ->', out)
