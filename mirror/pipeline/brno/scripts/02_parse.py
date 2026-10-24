"""Parse raw bmhd.cz pages into JSON.

  python 02_parse.py --vehicles 2026-09-25 --register 2026-09-28

-> data/derived/vypravenost_<date>.json   {line: [ {kurz, cars "1093+1605", note, author} ]}
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
            cars = re.sub(r'\s+', '', txt(car))
            rline = txt(cell('route'))
            if rline != line: continue          # safety: only the requested line
            rows.append(dict(kurz=txt(cell('order-on-line')), cars=cars,
                             note=re.sub(r'\s+', ' ', txt(cell('note'))), author=txt(cell('authors'))))
        if rows: out[line] = rows
    save(out, os.path.join(DER, f'vypravenost_{d}.json'))
    print('vypravenost', d, {k: len(v) for k, v in out.items()})

if a.register:
    folder = os.path.join(RAW, 'register', a.register)
    veh = {}
    for code, depot in (('M', 'Medlánky'), ('P', 'Pisárky')):
        s = open(os.path.join(folder, f'voz_{code}.html'), encoding='utf-8', errors='replace').read()
        for part in re.split(r'<div class="row-wrapper type">', s)[1:]:
            m = re.search(r'<a href="(/evidence-dpmb/vozp\.php[^"]*)">(.*?)</a>', part, re.S)
            if not m or 'trakce=tramvaj' not in m.group(1): continue
            group = re.sub(r'\s+', ' ', txt(m.group(2)))
            for vid, st, num in re.findall(r'href="/evidence-dpmb/vuz\.php\?id=(\d+)" class="car car-state-background ([^"]*)"\s*>\s*<span class="number">(\d+)', part):
                veh.setdefault(num, dict(depot=depot, group=group, id=vid, state=st))
    # exact subtype + livery from the type listings, joined by car id
    byid = {}
    for fn in glob.glob(os.path.join(folder, 'types_*.html')):
        s = open(fn, encoding='utf-8', errors='replace').read()
        for cid, body in re.findall(r'<tr class="car-line [^"]*"[^>]*data-car-id="(\d+)"[^>]*>(.*?)</tr>', s, re.S):
            act = re.findall(r'<span class="type active">([^<]*)</span>', body)
            pm = re.search(r'<span class="paint">\s*<span class="label">[^<]*</span>(.*?)</span>', body, re.S)
            if act:
                byid[cid] = dict(type=html.unescape(act[-1]).strip(),
                                 livery=re.sub(r'\s+', ' ', txt(pm.group(1)).replace('*', '')).strip() if pm else '')
    for num, v in veh.items():
        v.update(byid.get(v['id'], dict(type=None, livery='')))
    save(veh, os.path.join(DER, f'vehicles_{a.register}.json'))
    print('vehicles', len(veh), 'without exact type:', sorted(n for n, v in veh.items() if not v['type'])[:20])
