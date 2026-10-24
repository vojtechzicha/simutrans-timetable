"""Parse raw seznam-autobusu pages into JSON.

  python 02_parse.py --vehicles 2026-09-18 --register 2026-09-28 [--days]

-> data/derived/vypravenost_<date>.json  [ {line, kurz, cars:[num], ids:[car id], note} ]
-> data/derived/vehicles_<date>.json     {car id: {num, type, depot, livery, state}}
-> data/derived/day_counts.json           tram records per day (with --days), to pick the vehicle day
"""
import argparse, glob, html, os, re
from common import RAW, DER, save

p = argparse.ArgumentParser()
p.add_argument('--vehicles', action='append', default=[])
p.add_argument('--register')
p.add_argument('--days', action='store_true')
a = p.parse_args()
txt = lambda s: re.sub(r'\s+', ' ', html.unescape(re.sub(r'<!--.*?-->|<[^>]+>', '', s, flags=re.S))).strip()

for d in a.vehicles:
    out = []
    for fn in sorted(glob.glob(os.path.join(RAW, 'vypravenost', d, 'L*.html'))):
        line = re.search(r'L(\d+)\.html$', fn).group(1)
        s = open(fn, encoding='utf-8', errors='replace').read()
        for r in re.findall(r'<tr[^>]*>(.*?)</tr>', s, re.S):
            cars = re.findall(r'class="context-box" href="https://seznam-autobusu.cz/vuz/(\d+)/vypravenost">(\d+)</a>', r)
            if not cars: continue
            cell = {c.split()[0]: txt(v) for c, v in re.findall(r'<td[^>]*class="([^"]*)"[^>]*>(.*?)</td>', r, re.S)}
            out.append(dict(line=line, kurz=int(cell.get('order-on-line') or 0), cars=[n for _, n in cars],
                            ids=[i for i, _ in cars], note=cell.get('note', '')))
    save(out, os.path.join(DER, f'vypravenost_{d}.json')); print('vypravenost', d, len(out), 'records')

if a.register:
    reg = {}
    for fn in sorted(glob.glob(os.path.join(RAW, 'register', a.register, 'page*.html'))):
        s = open(fn, encoding='utf-8', errors='replace').read(); groups = {}
        for cls, cid, body in re.findall(r'<tr class="car-line ([^"]*)"[^>]*data-car-id="(\d+)"[^>]*>(.*?)</tr>', s, re.S):
            g = groups.setdefault(cid, {'cls': cls, 'html': ''}); g['html'] += body
        for cid, g in groups.items():
            b = g['html']
            mt = re.search(r'<td class="manufacturer-type">(.*?)</td>', b, re.S)
            num = re.search(r'class="[^"]*number"><!--\s*-->(\d+)<!--', b)
            paint = re.search(r'<span class="paint"><span class="label">[^<]*</span>(.*?)</span>', b, re.S)
            typ = txt(mt.group(1)) if mt else ''
            if 'KT8D5.RN2P' in typ: typ = 'ČKD Tatra KT8D5.RN2P'   # listing shows "ČKD Tatra KT8D5 » KT8D5.RN2P"
            reg[cid] = dict(num=num.group(1) if num else None, type=typ, depot='Slovany',
                            livery=txt(paint.group(1)).replace('*', '').strip() if paint else '', state=g['cls'].split()[0])
    save(reg, os.path.join(DER, f'vehicles_{a.register}.json')); print('register', len(reg), 'cars')

if a.days:
    counts = {}
    for fn in sorted(glob.glob(os.path.join(RAW, 'vypravenost-days', '*.html'))):
        s = open(fn, encoding='utf-8', errors='replace').read()
        counts[os.path.basename(fn)[:-5]] = len(re.findall(r'class="route tramden"', s))
    save(counts, os.path.join(DER, 'day_counts.json')); print('tram lines with records per day', counts)
