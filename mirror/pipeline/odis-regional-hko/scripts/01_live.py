"""ODIS live map snapshots (mpvnet.cz, polled every minute on Tue 20 Oct 2026 by the Havířov/Karviná/Orlová pipeline)
-> data/raw/<snapshot>/live_compact.json, so this sheet keeps its observation if that raw folder goes.

Each transmitter row: cn = 'licence|line|trip|..|start|final|1|PLATE|..'; the trip number is the JDF trip (spoj) of the
licence, so a sighting gives the exact trip. Kept: every bus of config.live.carriers (default Transdev Slezsko), the whole poll, one row per licence and trip.
Output: {plates: {plate: [[first minute, last minute, licence, line, trip, branch], ...]}, files, span}.
"""
import glob, json, os
from lib import CONFIG, RAW, rel

src = rel(CONFIG['live']['dir'])
files = sorted(glob.glob(os.path.join(src, '*.json')))
out = os.path.join(RAW, 'live_compact.json')
if not files: raise SystemExit('no snapshots in ' + src + '; the compact file is kept as it is')
os.makedirs(RAW, exist_ok=True)
pl_ = {}; mins = []
for f in files:
    b = os.path.basename(f); m = int(b[9:11]) * 60 + int(b[11:13]); mins.append(m)
    for v in json.load(open(f, encoding='utf-8-sig'))['transmitters']:
        if v.get('t') != 'H' or not v.get('cn') or not any((v.get('cr') or '').startswith(c) for c in CONFIG['live'].get('carriers', ['Transdev Slezsko'])): continue
        p = v['cn'].split('|')
        if len(p) < 12 or not p[2].isdigit(): continue
        pl = p[11].replace(' ', '').upper(); r = pl_.setdefault(pl, [])
        key = [p[0], p[1], int(p[2])]
        if r and r[-1][2:5] == key: r[-1][1] = m
        else: r.append([m, m] + key + [v['cr'].replace('Transdev Slezsko pr. ', '')])
json.dump(dict(files=len(files), span=[min(mins), max(mins)], plates=pl_), open(out, 'w', encoding='utf-8'), ensure_ascii=False)
print('live', len(files), 'snapshots', min(mins), '-', max(mins), ',', len(pl_), 'Transdev Slezsko plates ->', out)
