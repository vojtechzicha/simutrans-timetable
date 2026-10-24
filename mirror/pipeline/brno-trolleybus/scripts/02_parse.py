"""Parse raw bmhd.cz pages into JSON (same page formats as the tram pipeline).

  python 02_parse.py --vehicles 2026-09-25 --register 2026-09-29

-> data/derived/vypravenost_<date>.json   {line: [ {kurz, cars, note, author, traction} ]}
   traction comes from the row class: car-on-line-trolley, car-on-line-bus, ... (a bus on a trolleybus
   line is kept, marked, and never counted as a trolleybus)
-> data/derived/vehicles_<regdate>.json    {number: {type, depot, livery, id, state, group}}
"""
import argparse, glob, html, os, re
from common import RAW, DER, save

p = argparse.ArgumentParser()
p.add_argument('--vehicles', action='append', default=[])
p.add_argument('--register')
a = p.parse_args()

def txt(s): return html.unescape(re.sub(r'<!--.*?-->|<[^>]+>', '', s, flags=re.S)).strip()

for d in a.vehicles:
    out = {}
    for fn in sorted(glob.glob(os.path.join(RAW, 'vypravenost', d, 'L*.html'))):
        line = re.search(r'L(\d+)\.html$', fn).group(1)
        s = open(fn, encoding='utf-8', errors='replace').read()
        rows = []
        for cls, r in re.findall(r'<tr class="row ([^"]*)">(.*?)</tr>', s, re.S):
            cell = lambda c: (re.search(r'<td class="' + c + r'">(.*?)</td>', r, re.S) or [None, ''])[1]
            car = re.sub(r"data-bmhd-context-box='.*?'", '', cell('car'), flags=re.S)
            if txt(cell('route')) != line: continue
            tr = re.search(r'car-on-line-(\w+)', cls)
            rows.append(dict(kurz=txt(cell('order-on-line')), cars=re.sub(r'\s+', '', txt(car)),
                             note=re.sub(r'\s+', ' ', txt(cell('note'))), author=txt(cell('authors')),
                             traction=tr.group(1) if tr else cls))
        if rows: out[line] = rows
    save(out, os.path.join(DER, f'vypravenost_{d}.json'))
    print('vypravenost', d, {k: len(v) for k, v in out.items()},
          'non-trolley rows:', [(l, r['kurz'], r['cars'], r['traction']) for l, v in out.items() for r in v if r['traction'] != 'trolley'])

if a.register:
    folder = os.path.join(RAW, 'register', a.register)
    veh = {}
    for code, depot in (('k', 'Komín'), ('h', 'Husovice'), ('s', 'Slatina')):
        s = open(os.path.join(folder, f'voz_{code}.html'), encoding='utf-8', errors='replace').read()
        for part in re.split(r'<div class="row-wrapper type">', s)[1:]:
            m = re.search(r'<a href="(/evidence-dpmb/vozp\.php[^"]*)">(.*?)</a>', part, re.S)
            if not m or 'trakce=trolejbus' not in m.group(1): continue
            group = re.sub(r'\s+', ' ', txt(m.group(2)))
            for vid, st, num in re.findall(r'href="/evidence-dpmb/vuz\.php\?id=(\d+)" class="car car-state-background ([^"]*)"\s*>\s*<span class="number">(\d+)', part):
                veh.setdefault(num, dict(depot=depot, group=group, id=vid, state=st))
    # buses that turned up on trolleybus lines (01_fetch --bus-types): Slatina bus groups
    s = open(os.path.join(folder, 'voz_s.html'), encoding='utf-8', errors='replace').read()
    for part in re.split(r'<div class="row-wrapper type">', s)[1:]:
        m = re.search(r'<a href="(/evidence-dpmb/vozp\.php[^"]*)">(.*?)</a>', part, re.S)
        if not m or 'trakce=autobus' not in m.group(1): continue
        group = re.sub(r'\s+', ' ', txt(m.group(2)))
        for vid, st, num in re.findall(r'href="/evidence-dpmb/vuz\.php\?id=(\d+)" class="car car-state-background ([^"]*)"\s*>\s*<span class="number">(\d+)', part):
            veh.setdefault(num, dict(depot='Slatina', group=group, id=vid, state=st, bus=True))
    byid = {}
    for fn in glob.glob(os.path.join(folder, 'types_*.html')) + glob.glob(os.path.join(folder, 'bustypes_*.html')):
        s = open(fn, encoding='utf-8', errors='replace').read()
        for cid, body in re.findall(r'<tr class="car-line [^"]*"[^>]*data-car-id="(\d+)"[^>]*>(.*?)</tr>', s, re.S):
            act = re.findall(r'<span class="type active">([^<]*)</span>', body)
            pm = re.search(r'<span class="paint">\s*<span class="label">[^<]*</span>(.*?)</span>', body, re.S)
            if act:
                byid[cid] = dict(type=html.unescape(act[-1]).strip(),
                                 livery=re.sub(r'\s+', ' ', txt(pm.group(1)).replace('*', '')).strip() if pm else '')
    for num, v in veh.items():
        v.update(byid.get(v['id'], dict(type=None, livery='')))
    buses = {n: v for n, v in veh.items() if v.get('bus') and v['type']}      # keep only buses with a fetched exact type
    veh = {n: v for n, v in veh.items() if not v.get('bus')}; veh.update(buses)
    save(veh, os.path.join(DER, f'vehicles_{a.register}.json'))
    print('vehicles', len(veh), 'buses', {n: v['type'] for n, v in buses.items()}, 'without exact type:', sorted(n for n, v in veh.items() if not v['type'])[:20])
