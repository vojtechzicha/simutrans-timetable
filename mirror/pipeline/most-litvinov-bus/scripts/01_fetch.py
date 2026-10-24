"""Download the raw inputs into data/raw/<kind>/<snapshot>/ exactly as fetched. About 1 request/s, browser-like
User-Agent and nothing personal in any request (brief rule h).

usage: python 01_fetch.py [--jdf] [--fleet] [--records] [--cars] [--photos] [--operator]   (no flag = all but --jdf)
  --jdf       CIS JŘ bus export JDF.zip (~107 MB) and the city export (trams, for the replacement buses) into
              data/raw/jdf/<snapshot>/. Without it, the zips named in config.jdf (another pipeline's raw folder,
              read only) are used, so the 107 MB file is not downloaded twice.
  --fleet     seznam-autobusu register of DPmML buses (iddopravce=399, prov=1: vehicles in service), fleet/p<N>.html
  --records   seznam-autobusu vypravenost: the day overview of the nationwide 'cr' section for config.vehicle_day
              (where JDF-numbered lines such as 575005 are logged) and each DPmML line's full record list
              (/vypravenost/cr/vypis?linka=<JDF number>), records/day_<date>.html and records/line_<n>.html
  --cars      the detail page of every active register car (/vuz/<id>): its own records and its photo list,
              cars/<id>.html
  --photos    for every city bus, its newest photos (config.photos: up to per_car taken since `since`, else the newest
              one since `fallback_since`) as full images, photos/<photo id>.jpg (run 03_fleet.py first: it lists the
              photos from the car pages). The line number on the destination display is read by eye into
              assets/photo_lines.json (see README).
  --operator  dpmost.cz pages: the replacement-bus notice, the fleet summary, the timetable index
"""
import glob, json, os, re, sys
from lib import CONFIG, raw, http, parse_fleet_list

args = set(sys.argv[1:]) or {'--fleet', '--records', '--cars', '--photos', '--operator'}
C = CONFIG; SA = 'https://seznam-autobusu.cz'
def put(path, s, binary=False):
    open(path, 'wb' if binary else 'w', **({} if binary else {'encoding': 'utf-8'})).write(s)
    print(os.path.relpath(path, raw('')), len(s), flush=True)

if '--jdf' in args:
    for k in ('bus_url', 'tram_url'):
        b = http(C['jdf'][k], binary=True, pause=1)
        put(os.path.join(raw('jdf'), k.split('_')[0] + '_JDF.zip'), b, True)
if '--fleet' in args:
    p = 1
    while True:
        s = http(C['fleet']['list_url'] + (f'&page={p}' if p > 1 else ''), pause=1.1)
        put(os.path.join(raw('fleet'), f'p{p}.html'), s)
        if not re.search(r'page=%d\b' % (p + 1), s): break
        p += 1
if '--records' in args:
    s = http(f"{SA}/vypravenost/cr?datum={C['vehicle_day']}", pause=1.1)
    put(os.path.join(raw('records'), f"day_{C['vehicle_day']}.html"), s)
    for code in C['jdf']['all_codes']:
        s = http(f'{SA}/vypravenost/cr/vypis?linka={code}', pause=1.1)
        put(os.path.join(raw('records'), f'line_{code}.html'), s)
if '--cars' in args:
    cars = {}
    for f in glob.glob(os.path.join(raw('fleet'), 'p*.html')):
        cars.update(parse_fleet_list(open(f, encoding='utf-8').read()))
    for cid, c in sorted(cars.items(), key=lambda x: int(x[0])):
        if c['state'] != 'zar': continue
        put(os.path.join(raw('cars'), f'{cid}.html'), http(f'{SA}/vuz/{cid}', pause=1.1))
if '--photos' in args:
    # needs derived/fleet.json and evidence.json (03_fleet.py): city buses only, newest photos first
    from lib import load
    P = C['photos']; fleet = load('fleet.json'); ev = load('evidence.json')
    for n, e in sorted(ev.items(), key=lambda x: int(x[0])):
        if not fleet[n]['city']: continue
        ph = [p for p in e['photos'] if p['date'] >= P['since']][:P['per_car']] or [p for p in e['photos'] if p['date'] >= P['fallback_since']][:1]
        for p in ph:
            out = os.path.join(raw('photos'), f"{p['id']}.jpg")
            if os.path.exists(out) or os.path.exists(out[:-4] + 'n.jpg'): continue
            try: put(out, http(P['image_url'].format(id=p['id']), binary=True, pause=1.1), True)
            except Exception as ex:       # a few full images answer 403: take the thumbnail instead
                print('full image refused', p['id'], ex, flush=True)
                try: put(os.path.join(raw('photos'), f"{p['id']}n.jpg"), http(P['image_url'].format(id=p['id'] + 'n'), binary=True, pause=1.1), True)
                except Exception as ex2: print('thumbnail refused too', p['id'], ex2, flush=True)
if '--operator' in args:
    for name, url in C['operator_pages'].items():
        put(os.path.join(raw('operator'), f'{name}.html'), http(url, pause=1.5))
