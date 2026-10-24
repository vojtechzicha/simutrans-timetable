"""Post-step between 04_roster.py and 06_render.py for this sheet: fill Simutrans lines the shared roster leaves short
(config.fill_designed) with designed vehicles of a given carrier and type that are on no line of any sheet and not running
in the line's window (the live map). Needed for trolleybus 204: on 20 Oct 2026 it ran with replacement buses (Vrchní
street closure 12-23 Oct), the trolleybuses that normally work it were idle, and the shared rules can only design buses
that ran the area's lines that day or carry a fleet-number prefix (MDPO numbers have none).

config.fill_designed = {L: {carrier, type_contains, why, alt?}}; alt = the auxiliary drives the line needs, best first
(authoring/alt_drive.py marks them; it runs first). Run: python -X utf8 authoring/fill_designed.py (after 04).
"""
import collections, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
os.environ['ODIS_BASE'] = os.path.join(HERE, '..')
sys.path.insert(0, os.path.join(HERE, '..', '..', 'odis-regional-hko', 'scripts'))
from lib import CONFIG, RAW, load, save, rel, hm

R = load('roster.json'); S = load('schedule.json')
fleet = json.load(open(rel(CONFIG['live']['fleet']), encoding='utf-8'))
live = json.load(open(os.path.join(RAW, 'live_compact.json'), encoding='utf-8'))['plates']
busy = collections.defaultdict(list)
for pl, rows in live.items():
    for f, l, lic, line, sp, br in rows: busy[pl].append((f, l))
used = {v['plate'] for ss in R['lines'].values() for s in ss for v in s['seen'] + s['designed']} | set(R.get('other_sheet_plates', {}))
seen_on = collections.Counter()
for L, spec in CONFIG.get('fill_designed', {}).items():
    for si, s in enumerate(S[L]['sim']):
        r = R['lines'][L][si]
        if spec.get('alt'):       # the shared roster's designed picks must also have the drive
            r['designed'] = [v for v in r['designed'] if fleet.get(v['num'], {}).get('alt') in spec['alt']]
        short = s['need'] - len(r['seen']) - len(r['designed'])
        if short <= 0: continue
        W = s['window']
        # the line's own real trips: the types seen on them at any time of the day rank first (308 and 326 ran early 204 trips)
        tys = collections.Counter()
        for g in s['legs']:
            for t in g.get('trips', []):
                for pl, rows in live.items():
                    if any(rw[2] == t['lic'] and rw[4] == t['sp'] for rw in rows):
                        n = next((k for k, v in fleet.items() if v.get('plate') == pl), None)
                        if n: tys[fleet[n]['type']] += 1
        pool = [n for n, f in fleet.items() if f.get('carrier') == spec['carrier'] and spec['type_contains'] in f.get('type', '')
                and f.get('state') == 'zar' and f.get('plate') and f['plate'] not in used
                and not any(a < W[1] and b > W[0] for a, b in busy.get(f['plate'], []))
                and (not spec.get('alt') or fleet[n].get('alt') in spec['alt'])]
        # spec.alt: the line leaves the wire, so only trolleybuses with that auxiliary drive, in that order of preference
        pool.sort(key=lambda n: (spec['alt'].index(fleet[n]['alt']) if spec.get('alt') else 0, -tys.get(fleet[n]['type'], 0), n))
        for n in pool[:short]:
            f = fleet[n]
            r['designed'].append(dict(plate=f['plate'], num=n, type=f.get('cat') or f['type'], full=f.get('full') or f['type'], len=f.get('len', ''),
                                      paint=f.get('paint', ''), year=f.get('year', ''), note=f.get('note', ''), **({'alt': f['alt']} if f.get('alt') else {}),
                                      why=spec['why'].format(w0=hm(W[0]), w1=hm(W[1]), alt=f.get('alt', '')), branch=CONFIG['areas'][[a['id'] for a in CONFIG['areas']].index(S[L]['areas'][0])]['branch']))
            used.add(f['plate'])
        print(L, s['name'], 'short', short, '-> designed', [d['num'] for d in r['designed']])
R['totals']['designed'] = sum(len(s['designed']) for ss in R['lines'].values() for s in ss)
save('roster.json', R)
