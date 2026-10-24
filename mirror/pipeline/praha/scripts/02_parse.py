"""Parse raw pages into dated JSON in data/derived/.

  records_<date>.json    {line: [dict(car, line, course, note, ...)]} for the vehicle date and the extra days
  history.json           {line: [records]} from vypravenost/history (coverage of lines 6, 13, 31)
  vehicles_<date>.json   {fleet number: dict(type, types, paint, depot, year, state)} from the depot register

Usage: python 02_parse.py --state 2026-09-27
"""
import argparse, glob, os
from common import state, save, RAW, DER, parse_vypis, parse_register
import importlib; slug = importlib.import_module('01_fetch').slug

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--state', required=True)
    s = state(ap.parse_args().state); vy = s['vypravenost']
    days = [s['vehicle_date']] + list(vy.get('extra_days', {}))
    for d in days:
        rec = {}
        for p in sorted(glob.glob(os.path.join(RAW, 'vypravenost', d, '*.html'))):
            l = os.path.splitext(os.path.basename(p))[0]
            if l == 'overview': continue
            rec[l] = parse_vypis(p)
        save(rec, os.path.join(DER, f'records_{d}.json'))
        print(d, sum(len(v) for v in rec.values()), 'records')
    m = s.get('metro')
    if m:
        import re
        t = open(os.path.join(RAW, 'vypravenost', s['vehicle_date'], 'overview.html'), encoding='utf-8').read()
        rec = {}
        for mm in re.finditer(r'<span class="route ' + m.get('overview_class', 'vlakden') + r'"><!--\s*--><a href="[^"]*">([^<]+)</a>(.*?)(?=<span class="route )', t, flags=re.S):
            rec[mm.group(1)] = sorted({int(c) for c in re.findall(r'<span class="course">(\d+)</span>', mm.group(2))})
        save(rec, os.path.join(DER, f'metro_records_{s["vehicle_date"]}.json'))
        print('metro records', {k: len(v) for k, v in rec.items()})
    hist = {os.path.splitext(os.path.basename(p))[0]: parse_vypis(p)
            for p in glob.glob(os.path.join(RAW, 'vypravenost', 'history', '*.html'))}
    save(hist, os.path.join(DER, 'history.json'))
    reg = s['register']; veh = {}
    for name in reg['depots']:
        pages = sorted(glob.glob(os.path.join(RAW, 'register', reg['raw'], f'l_{slug(name)}_*.html')))
        v = parse_register(pages, name); veh.update(v)
        print(name, len(v), 'trams')
    save(veh, os.path.join(DER, f'vehicles_{reg["raw"]}.json'))

if __name__ == '__main__':
    main()
