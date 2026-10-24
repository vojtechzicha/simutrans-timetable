"""ODIS live map snapshots (mpvnet.cz, polled by the Havířov/Karviná/Orlová pipeline) -> a compact file for 07_odis.py.

config.odis.live: raw = the poll's snapshot folder, out = the compact file. Each transmitter row: cn = 'licence|line|trip|..|
start|final|1|PLATE|..' (pipeline/havirov-karvina-orlova/scripts/01b_live_poll.py); the trip number is the JDF trip (spoj)
number of the line, so a sighting gives the exact trip. Kept: 13:00-19:00, one row per line and trip.
Output: {plate: [[first minute, last minute, line, trip], ...]}.
"""
import glob, json, os
from lib import CONFIG

LV = CONFIG['odis']['live']; HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
out = {}
files = sorted(glob.glob(os.path.join(HERE, LV['raw'], '*.json')))
if not files: raise SystemExit('no snapshots in ' + LV['raw'] + '; the compact file is kept as it is')
for f in files:
    b = os.path.basename(f); m = int(b[9:11]) * 60 + int(b[11:13])
    if not 780 <= m <= 1140: continue
    for v in json.load(open(f, encoding='utf-8'))['transmitters']:
        if v.get('t') != 'H' or not v.get('cn'): continue
        p = v['cn'].split('|')
        if len(p) < 12 or not p[2].isdigit(): continue
        pl = p[11].replace(' ', '').upper(); r = out.setdefault(pl, [])
        if r and r[-1][2:] == [p[1], int(p[2])]: r[-1][1] = m
        else: r.append([m, m, p[1], int(p[2])])
json.dump(dict(files=len(files), plates=out), open(os.path.join(HERE, LV['out']), 'w', encoding='utf-8'), ensure_ascii=False)
print('odis live', len(files), 'snapshots,', len(out), 'plates ->', LV['out'])
