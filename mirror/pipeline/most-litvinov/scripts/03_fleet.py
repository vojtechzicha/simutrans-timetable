"""Raw fleet pages -> derived/fleet.json {number: {state, type, year, note}}; live polls -> derived/live.json."""
import glob, json, os, re, collections
from lib import RAW, parse_fleet_list, save

fleet = {}
for f in sorted(glob.glob(os.path.join(RAW, 'fleet', 'p*.html'))):
    for c in parse_fleet_list(open(f, encoding='utf-8').read()).values():
        m = re.match(r'\d+', c['num'])
        if m: fleet[int(m.group())] = c
save('fleet.json', fleet)
print('fleet', len(fleet), collections.Counter(c['state'] for c in fleet.values()))

live = collections.defaultdict(set); files = sorted(glob.glob(os.path.join(RAW, 'live', '*.json')))
for f in files:
    for x in json.load(open(f, encoding='utf-8')).get('features', []):
        a = x['attributes']; live[a['CISLO_VOZIDLA']].add(a['CISLO_LINKY'])
save('live.json', dict(files=len(files), cars={n: sorted(s) for n, s in live.items()}))
print('live polls', len(files), 'cars seen', len(live))
