"""MD-CR v3, step 1: list every workday long-distance train on the Praha – Ostrava corridor and Ex2.

Reads data/derived/trains.json (from 01_parse.py) and writes data/derived/corridor.json plus a readable
data/derived/_corridor.txt. A train is kept when it runs on all five days of config.json "v3_week"
(an ordinary Mon–Fri week) and either stops at Ostrava-Svinov / Ostrava hl. n. / Bohumín / Havířov / Brno hl. n. /
Břeclav or is on state line Ex2 (service number 2). Categories: config.json "included_categories" (no night trains).
"""
import json, os, sys, datetime as dt
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
cfg = json.load(open(os.path.join(BASE, 'config.json'), encoding='utf-8'))
PA = set(cfg['passenger_activities'])
CATS = cfg['categories']
INC = set(cfg['included_categories'])
WEEK = [dt.date.fromisoformat(x) for x in cfg['v3_week']]
OSTRAVA = {'Ostrava-Svinov', 'Ostrava hl. n.', 'Bohumín', 'Havířov'}
BRNO = {'Brno hl. n.', 'Břeclav'}  # added 4 Oct 2026 for the Brno pass


def runs(t, day):
    i = (day - dt.date.fromisoformat(t['start'])).days
    return 0 <= i < len(t['bitmap']) and t['bitmap'][i] == '1'


def main():
    trains = json.load(open(os.path.join(BASE, 'data', 'derived', 'trains.json'), encoding='utf-8'))
    out = []
    for t in trains:
        if not all(runs(t, d) for d in WEEK):
            continue
        locs = t['locs']
        stops = [l for l in locs if PA & set(l['act'])]
        if len(stops) < 2:
            continue
        cats = Counter(l['ctt'] for l in stops if l['ctt'])
        if not cats:
            continue
        cat = cats.most_common(1)[0][0]
        if cat not in INC:
            continue
        names = {l['name'] for l in stops}
        svcs = Counter(l['svc'] for l in stops if l['svc'])
        svc = svcs.most_common(1)[0][0] if svcs else None
        if not (names & OSTRAVA or names & BRNO or svc == '2'):
            continue
        rec = {
            'file': t['file'], 'num': stops[0]['num'], 'cat': CATS.get(cat, cat), 'ru': stops[0]['ru'], 'svc': svc,
            'foreign': t['foreign'],
            'stops': [{'name': l['name'], 'cc': l['cc'], 'arr': l.get('arr'), 'dep': l.get('dep'),
                       'req': '0030' in l['act'], 'num': l['num']} for l in stops],
        }
        out.append(rec)
    out.sort(key=lambda r: (r['ru'], r['svc'] or '', r['stops'][0]['dep'] or 0))
    json.dump(out, open(os.path.join(BASE, 'data', 'derived', 'corridor.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

    def hm(m):
        return '' if m is None else f"{int(m) // 60 % 24}:{int(m) % 60:02d}"
    lines = []
    for r in out:
        s = r['stops']
        lines.append(f"{r['cat']} {r['num']} ru={r['ru']} svc={r['svc']} foreign={r['foreign']} {r['file']}")
        lines.append('   ' + ' – '.join(f"{x['name']}{'(x)' if x['req'] else ''}{'['+x['cc']+']' if x['cc'] != 'CZ' else ''} {hm(x['arr'])}/{hm(x['dep'])}" for x in s))
    open(os.path.join(BASE, 'data', 'derived', '_corridor.txt'), 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
    print(len(out), 'trains', Counter((r['ru'], r['cat'], r['svc']) for r in out))


if __name__ == '__main__':
    main()
