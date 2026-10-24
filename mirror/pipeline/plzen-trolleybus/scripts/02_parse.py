"""Parse raw seznam-autobusu.cz pages into JSON (shared by the trolleybus and bus sheets).

  python 02_parse.py --vehicles 2026-09-18 --register 2026-09-29 --days

-> data/derived/vypravenost_<date>.json   {line: [ {kurz, cars:[num], ids:[car id], note} ]}  (per-line lists)
-> data/derived/vehicles_<regdate>.json   {car id: {num, type, livery, garage, operator, year, state, traction}}
   PMDP register listings (pmdp_<trakce>_N.html), other operators' listings (op<id>_<trakce>_N.html) and single
   vehicle pages (vuz_<id>.html). Car ids are the key: PMDP trolleybus and bus numbers overlap (559 is both).
-> data/derived/day_counts.json           records per day and traction (trolden / busden), to pick the vehicle day
-> data/derived/history.json              {line: [ {date, kurz, cars, ids, note} ]} from data/raw/history/*/ (newest first)
"""
import argparse, collections, glob, os, re
from common import RAW, DER, save, parse_vypis, parse_register, parse_overview, txt

p = argparse.ArgumentParser()
p.add_argument('--vehicles', action='append', default=[])
p.add_argument('--register')
p.add_argument('--days', action='store_true')
p.add_argument('--history', action='store_true')
a = p.parse_args()

for d in a.vehicles:
    out = {}
    for fn in sorted(glob.glob(os.path.join(RAW, 'vypravenost', d, 'L*.html'))):
        line = re.search(r'L([^\\/]+)\.html$', fn).group(1)
        rows = [dict(kurz=int(r['kurz']) if r['kurz'].isdigit() else r['kurz'], cars=r['cars'], ids=r['ids'], note=r['note'])
                for r in parse_vypis(fn) if r['line'] == line]
        if rows: out[line] = rows
    save(out, os.path.join(DER, f'vypravenost_{d}.json'))
    print('vypravenost', d, {k: len(v) for k, v in out.items()})

def vuz_page(fn):
    """seznam-autobusu.cz/vuz/<id>: one vehicle of any operator."""
    s = open(fn, encoding='utf-8', errors='replace').read()
    t = re.search(r'<h1[^>]*>(.*?)</h1>', s, re.S)
    row = lambda lab: (re.search(r'<th[^>]*>\s*' + lab + r'[^<]*</th>\s*<td[^>]*>(.*?)</td>', s, re.S) or [None, ''])[1]
    return dict(title=txt(t.group(1)) if t else '', type=txt(row('typ')), operator=txt(row('dopravce')), garage=txt(row('vozovna|garáž')),
                livery=txt(row('nátěr')).replace('*', '').strip(), year=txt(row('rok výroby'))[:4], num=txt(row('ev')), raw=True)

if a.register:
    folder = os.path.join(RAW, 'register', a.register)
    veh = {}
    for fn in sorted(glob.glob(os.path.join(folder, '*_1.html'))):
        stem = os.path.basename(fn)[:-len('_1.html')]
        tr = stem.split('_')[-1]
        for cid, v in parse_register(folder, stem + '_*.html').items():
            v['traction'] = 'trolleybus' if tr == 'trolejbus' else 'bus'
            if stem.startswith('pmdp_'): v['operator'] = v['operator'] or 'PMDP'
            veh[cid] = v
    for fn in sorted(glob.glob(os.path.join(folder, 'vuz_*.html'))):
        cid = re.search(r'vuz_(\d+)', fn).group(1)
        if cid not in veh: veh[cid] = dict(vuz_page(fn), traction='bus')
    save(veh, os.path.join(DER, f'vehicles_{a.register}.json'))
    print('vehicles', a.register, len(veh), collections.Counter((v['traction'], v['state'] if 'state' in v else 'page') for v in veh.values()))

if a.days:
    counts = {}
    for fn in sorted(glob.glob(os.path.join(RAW, 'vypravenost-days', '*.html'))):
        o = parse_overview(fn); c = collections.Counter()
        for (kind, line), items in o.items(): c[kind] += len(items)
        counts[os.path.basename(fn)[:-5]] = dict(c)
    save(counts, os.path.join(DER, 'day_counts.json')); print('records per day', counts)

if a.history:
    hist = collections.defaultdict(list); seen = set()
    for fn in sorted(glob.glob(os.path.join(RAW, 'history', '*', 'L*.html'))):
        for r in parse_vypis(fn):
            k = (r['date'], r['line'], r['kurz'], tuple(r['ids']), r['note'])
            if k in seen: continue
            seen.add(k); hist[r['line']].append(dict(date=r['date'], kurz=r['kurz'], cars=r['cars'], ids=r['ids'], note=r['note']))
    for L in hist: hist[L].sort(key=lambda r: r['date'], reverse=True)
    save(hist, os.path.join(DER, 'history.json'))
    print('history', {L: (len(v), v[-1]['date'], v[0]['date']) for L, v in sorted(hist.items())})
