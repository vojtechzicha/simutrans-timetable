"""Post-step after 04_roster.py (before fill_designed.py): mark MDPO trolleybuses that can leave the wire.

The register's vehicle pages (seznam-autobusu.cz/vuz/<id>, saved in data/raw/2026-10-22/vuz/<number>_<id>.html) give
"alternativní pohon: baterie" (32 Tr 314-323) or "alternativní pohon: dieselagregát ..." (26 Tr 305, 306); the other
trolleybuses have none. Line 204 runs off the wire (Vrchní street, Kylešovice škola), so only these can work it.

Writes `alt` ('battery' / 'diesel generator') onto data/derived/fleet.json and onto the roster's MDPO entries.
Run: python -X utf8 authoring/alt_drive.py (run.py runs it via config.post_roster).
"""
import glob, json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
os.environ['ODIS_BASE'] = os.path.join(HERE, '..')
sys.path.insert(0, os.path.join(HERE, '..', '..', 'odis-regional-hko', 'scripts'))
from lib import CONFIG, load, save, rel

alt = {}
for fn in glob.glob(os.path.join(HERE, '..', 'data', 'raw', '2026-10-22', 'vuz', '*.html')):
    t = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', open(fn, encoding='utf-8').read()))
    m = re.search(r'alternativní pohon: (\w+)', t)
    if m: alt[os.path.basename(fn).split('_')[0]] = {'baterie': 'battery', 'dieselagregát': 'diesel generator'}.get(m.group(1), m.group(1))
FP = rel(CONFIG['live']['fleet'])
fleet = json.load(open(FP, encoding='utf-8'))
for n, f in fleet.items():
    if f.get('carrier') == 'MDPO':
        if n in alt: f['alt'] = alt[n]
        else: f.pop('alt', None)
json.dump(fleet, open(FP, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
R = load('roster.json')
for ss in R['lines'].values():
    for s in ss:
        for v in s['seen'] + s['designed'] + s.get('not_needed', []):
            if v['plate'].startswith('MDPO') and v['num'] in alt: v['alt'] = alt[v['num']]
save('roster.json', R)
print('alt drive:', ', '.join(f'{n} {a}' for n, a in sorted(alt.items())))
