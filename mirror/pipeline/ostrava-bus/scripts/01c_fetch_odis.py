"""ODIS lines at the hub (config.odis) -> data/raw/<odis.snapshot>/odis/: the lines, their seznam-autobusu records and the
operators' fleet lists. Lines are found by scanning the national JDF (the bus snapshot) for every non-DPO line with a stop
matching config.odis.hub_stop_match in hub_town, so new or removed ODIS lines need no config edit. The ODIS number of a
line is the last three digits of its licence number; each one is checked against the records (operator rows on that line).

usage: python 01c_fetch_odis.py [--scan] [--records] [--fleet]   (no flag = all)"""
import csv, datetime, io, json, os, re, sys, zipfile
from lib import CONFIG, RAW, http, parse_vypravenost, next_page, record_date, day

O = CONFIG['odis']; OUT = os.path.join(os.path.dirname(RAW), O['snapshot'], 'odis'); os.makedirs(OUT, exist_ok=True)
args = set(sys.argv[1:]) or {'--scan', '--records', '--fleet'}

def rows(inner, prefix):
    n = [x for x in inner.namelist() if x.lower().startswith(prefix)]
    return [r for r in csv.reader(io.StringIO(inner.read(n[0]).decode('cp1250').replace(';\r\n', '\n').replace(';\n', '\n'))) if r] if n else []

if '--scan' in args:
    outer = zipfile.ZipFile(os.path.join(RAW, 'JDF.zip')); res = []
    for name in outer.namelist():
        try: inner = zipfile.ZipFile(io.BytesIO(outer.read(name)))
        except zipfile.BadZipFile: continue
        if not any(O['hub_stop_match'] in ','.join(r[1:4]) and O['hub_town'] in r[1] for r in rows(inner, 'zastavky')): continue
        for r in rows(inner, 'linky'):
            if r[2] == O['dpo_ic']: continue
            ds = []
            for x in r[2:]:
                if re.fullmatch(r'\d{8}', x):
                    try: ds.append(datetime.datetime.strptime(x, '%d%m%Y').date().isoformat())
                    except ValueError: pass
            res.append(dict(inner=name, line=r[0], name=r[1], ic=r[2], valid_from=ds[0], valid_to=ds[1], diversion=len(r) > 5 and r[5] == '1'))
    json.dump(res, open(os.path.join(OUT, 'lines.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('ODIS line versions', len(res), 'lines', sorted({x['line'] for x in res}))

lines = sorted({x['line'][-3:] for x in json.load(open(os.path.join(OUT, 'lines.json'), encoding='utf-8'))})
if '--records' in args:
    recs = {}
    for ln in lines:                       # each line back to config.odis.line_since
        p = 1; recs[ln] = []
        while True:
            s = http(O['line_url'].format(line=ln) + (f'&strana={p}' if p > 1 else ''))
            got = parse_vypravenost(s); recs[ln] += got
            old = [r for r in got if record_date(r['date']) and record_date(r['date']) < day(O['line_since'])]
            if old or not next_page(s, p) or p >= 30: break
            p += 1
        print('line', ln, len(recs[ln]), 'records')
    day_recs = []; p = 1                   # every ODIS record of the vehicle day
    while True:
        s = http(O['day_url'].format(date=CONFIG['vehicle_day']) + (f'&strana={p}' if p > 1 else ''))
        day_recs += parse_vypravenost(s)
        if not next_page(s, p) or p >= 40: break
        p += 1
    print('day', CONFIG['vehicle_day'], len(day_recs), 'records')
    json.dump(dict(lines=recs, day=day_recs), open(os.path.join(OUT, 'records.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

if '--fleet' in args:
    for ic, cr in O['carriers'].items():
        p = 1
        while True:
            s = http(cr['fleet_url'] + (f'&page={p}' if p > 1 else ''))
            open(os.path.join(OUT, f"fleet_{cr['seznam_id']}_p{p}.html"), 'w', encoding='utf-8').write(s)
            print('fleet', cr['name'], 'page', p)
            if not next_page(s, p) or p >= 30: break
            p += 1
