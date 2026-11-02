"""PID GTFS -> every PID bus line with its oblast, and per oblast the trips of the service day in the ODIS schema.

Writes:
- data/derived/lines.json: every PID route of the feed (all modes), with key, label, licences, operators, mode, night /
  substitute flags, trips on the service day, and for bus lines the oblast and why.
- oblasti/<id>/data/derived/trips.json, line_class.json, versions.json: the ODIS regional schema (trip dict sp, lic, dep,
  arr, fr, to, stops, times), so odis-regional-hko/scripts 03b_draft.py and 05_schedule.py run on them with --base.

Oblast (the Středočeský kraj licenses each district's lines with its own prefix, the first two digits of the six-digit
licence: 20 Benešov, 21 Beroun, 22 Kladno, 23 Kolín, 24 Kutná Hora, 25 Mělník, 26 Mladá Boleslav, 27 Nymburk,
28 Praha-východ, 29 Praha-západ, 30 Příbram, 31 Rakovník):
- a line with a district licence: that district (the lowest prefix when it has two, e.g. 300519 + 301519);
- a line licensed by Prague (100xxx-104xxx: the lines that enter Prague) or by another kraj: the district of its outer end,
  the first stop from the end away from Prague that a district's own lines serve (votes of those lines' trips);
  a line with no Prague end: the district whose own lines serve most of its stops.
Stop names: the GTFS name with its common abbreviations written out, the town written as the save writes it where one
save halt town matches word by word (Benátky n.Jiz. -> Benátky nad Jizerou), and Prague stops (zone P/0/B, no town)
prefixed 'Praha, '. Usage: python 02_gtfs.py   (reads config.json of pid-regional)
"""
import collections, csv, datetime, io, json, os, re, zipfile
from common import HOME, RAW, DER, PIPE

CFG = json.load(open(os.path.join(HOME, 'config.json'), encoding='utf-8'))
G = CFG['gtfs']; SD = G['service_date']; D = datetime.date(int(SD[:4]), int(SD[4:6]), int(SD[6:]))
z = zipfile.ZipFile(os.path.join(HOME, G['zip']))
rd = lambda n: csv.DictReader(io.TextIOWrapper(z.open(n), encoding='utf-8-sig'))
OBL = {o['prefix']: o for o in CFG['oblasti']}

# ---------------------------------------------------------------- service day
cal = {r['service_id']: r for r in rd('calendar.txt')}
cdx = collections.defaultdict(dict)
for r in rd('calendar_dates.txt'): cdx[r['service_id']][r['date']] = r['exception_type']
WD = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'][D.weekday()]
def active(sid):
    e = cdx[sid].get(SD)
    if e: return e == '1'
    c = cal.get(sid)
    return bool(c) and c['start_date'] <= SD <= c['end_date'] and c[WD] == '1'

routes = {r['route_id']: r for r in rd('routes.txt')}
subs = collections.defaultdict(list)
for r in rd('route_sub_agencies.txt'): subs[r['route_id']].append(r)
trips = {t['trip_id']: t for t in rd('trips.txt') if active(t['service_id'])}
stops = {r['stop_id']: r for r in rd('stops.txt')}
st = collections.defaultdict(list)
for r in rd('stop_times.txt'):
    if r['trip_id'] in trips: st[r['trip_id']].append(r)

def mins(t): h, m = t.split(':')[:2]; return int(h) * 60 + int(m)

# ---------------------------------------------------------------- stop names
game = json.load(open(os.path.join(PIPE, CFG['game_regional']), encoding='utf-8'))['lines']
game_city = json.load(open(os.path.join(PIPE, CFG['game_city']), encoding='utf-8'))
gl = game_city['lines'] if isinstance(game_city, dict) and 'lines' in game_city else game_city
towns_game = set()
for l in list(game) + list(gl):
    for e in l.get('entries', []):
        for part in (e.get('halt_name') or '').split(' / '):
            t = re.sub(r'\s*\[[^\]]*\]', '', part.split(', ')[0]).strip()
            t = re.sub(r'\s*<[^>]*>', '', t).strip()
            if t and not any(ch.isdigit() for ch in t): towns_game.add(t)
WORDS = [(r'\baut\.st\.', 'autobusové stanoviště'), (r'\baut\.nádr\.', 'autobusové nádraží'), (r'\bžel\.st\.', 'železniční stanice'),
         (r'\bžel\.zast\.', 'železniční zastávka'), (r'\bnám\.', 'náměstí '), (r'\brozc\.', 'rozcestí '), (r'\bodb\.', 'odbočka '),
         (r'\bkřiž\.', 'křižovatka'), (r'\bhl\.sil\.', 'hlavní silnice'), (r'\bzast\.', 'zastávka'), (r'\bnádr\.', 'nádraží'),
         (r'\bsídl\.', 'sídliště '), (r'\bnem\.', 'nemocnice'), (r'\bzáv\.', 'závod'), (r'\bkult\.dům', 'kulturní dům'),
         (r'\bObch\.', 'Obchodní '), (r'\bhost\.', 'hostinec'), (r'\brest\.', 'restaurace')]
_town = {}
def town_full(t):
    """the save's spelling of an abbreviated town ('Benátky n.Jiz.', 'Brandýs n.L.-St.Bol.'), when exactly one save town
    matches word by word (each abbreviation a prefix of its word)"""
    if '.' not in t: return t
    if t in _town: return _town[t]
    toks = re.findall(r'[^\s.\-]+\.?|-', t)
    pat = ''
    for k in toks:
        if k == '-': pat += r'\s*-\s*'; continue
        w = re.escape(k.rstrip('.'))
        pat += (r'\s*' if pat and not pat.endswith(r'-\s*') else '') + (w + r'\w*' if k.endswith('.') else w)
    rx = re.compile('^' + pat + '$')
    hits = sorted({g for g in towns_game if rx.match(g)})
    _town[t] = hits[0] if len(hits) == 1 else t
    return _town[t]
def name_of(sid):
    s = stops[sid]; n = s['stop_name'].replace('\xa0', ' ').strip()
    if ',' not in n and s.get('zone_id', '').split(',')[0] in ('P', '0', 'B'): return 'Praha, ' + n
    parts = n.split(',')
    parts[0] = town_full(parts[0].strip())
    out = ', '.join(p.strip() for p in parts if p.strip())
    for a, b in WORDS: out = re.sub(a, b.strip() + ' ', out)
    return re.sub(r'\s+', ' ', out).replace(' ,', ',').strip()

# ---------------------------------------------------------------- lines
MODE = {'0': 'tram', '1': 'metro', '2': 'rail', '3': 'bus', '4': 'ferry', '7': 'funicular', '11': 'trolleybus'}
def lic_list(rid): return [s['route_licence_number'] for s in subs.get(rid, []) if s['route_licence_number']]
def district(lic):
    return lic[:2] + '0' if len(lic) == 6 and lic[:2] + '0' in OBL else None
TOWNMHD = CFG.get('town_mhd', {})
by_route = collections.defaultdict(list)
for tid, t in trips.items(): by_route[t['route_id']].append(tid)

def trip_rec(tid):
    t = trips[tid]; rs = sorted(st[tid], key=lambda r: int(r['stop_sequence']))
    if len(rs) < 2: return None
    sa = {s['sub_agency_id']: s['route_licence_number'] for s in subs.get(t['route_id'], [])}
    lic = sa.get(t['sub_agency_id']) or (lic_list(t['route_id']) or ['0'])[0]
    names = [FINAL[r['stop_id']] for r in rs]; times = [mins(r['departure_time']) for r in rs]
    m = re.match(r'[^_]+_(\d+)_', tid)
    return dict(sp=int(m.group(1)) if m else abs(hash(tid)) % 10 ** 6, lf=t.get('wheelchair_accessible') == '1',
                dep=times[0], arr=mins(rs[-1]['arrival_time']), fr=names[0], to=names[-1], stops=names, times=times, lic=lic,
                sids=[r['stop_id'] for r in rs], trip_id=tid)

# ---------------------------------------------------------------- where each stop is: its okres, and unique names
import math
bus_routes = {rid for rid, r in routes.items() if r['route_type'] == '3'}
bus_sids = {r['stop_id'] for tid, rs in st.items() if trips[tid]['route_id'] in bus_routes for r in rs}
BASE = {sid: name_of(sid) for sid in bus_sids}
COORD = {sid: (float(stops[sid]['stop_lat']), float(stops[sid]['stop_lon'])) for sid in bus_sids}
CENTRE = (50.0875, 14.4214)
def dist(a, b):
    (la1, lo1), (la2, lo2) = a, b
    return math.hypot((la1 - la2) * 111.2, (lo1 - lo2) * 111.2 * math.cos(math.radians(50)))
# municipalities of each okres (cs.wikipedia "Kategorie:Obce v okrese X", data/raw/obce/<date>/); a name that several okresy
# have ("Lhota") is resolved by the district lines that serve the place
OKR = {o['okres']: o['prefix'] for o in CFG['oblasti']}
OBEC = collections.defaultdict(set)
for f in sorted(os.listdir(os.path.join(HOME, CFG['obce']))):
    ok = f[4:-5].replace('_', ' ')
    for m in json.load(open(os.path.join(HOME, CFG['obce'], f), encoding='utf-8'))['query']['categorymembers']:
        t = m['title']
        if t.startswith('Seznam '): continue
        OBEC[re.sub(r'\s*\(.*\)$', '', t)].add(OKR[ok])
_obec = {}
def obec_of(town):
    """okres prefixes of a GTFS town, written out or abbreviated ('Brandýs n.L.-St.Bol.'): exact name, else the one
    municipality name matching word by word (each abbreviation a prefix of its word)"""
    if town in _obec: return _obec[town]
    if town in OBEC: _obec[town] = OBEC[town]; return OBEC[town]
    r = set()
    if '.' in town:
        toks = re.findall(r'[^\s.\-]+\.?|-', town); pat = ''
        for k in toks:
            if k == '-': pat += r'\s*-\s*'; continue
            w = re.escape(k.rstrip('.'))
            pat += (r'\s*' if pat and not pat.endswith(r'-\s*') else '') + (w + r'\w*' if k.endswith('.') else w)
        rx = re.compile('^' + pat + '$'); hits = [g for g in OBEC if rx.match(g)]
        if len(hits) == 1: r = OBEC[hits[0]]
    _obec[town] = r; return r
# places: stops of one written name more than 4 km apart are different places (Bohemia has five Chrášťany)
byname = collections.defaultdict(list)
for sid in sorted(bus_sids): byname[BASE[sid]].append(sid)
PLACE = {}
for n, ss in byname.items():
    cl = []
    for sid in ss:
        hit = [c for c in cl if any(dist(COORD[sid], COORD[x]) <= 4 for x in c)]
        for c in hit: cl.remove(c)
        cl.append(sum(hit, []) + [sid])
    cl.sort(key=lambda c: min(c))
    for k, c in enumerate(cl):
        for sid in c: PLACE[sid] = (n, k, len(cl))
# district votes per place: each district-licensed line once per place it serves
pvotes = collections.defaultdict(collections.Counter)
for tid, rs in st.items():
    rid = trips[tid]['route_id']
    if rid not in bus_routes: continue
    ds = sorted({district(l) for l in lic_list(rid)} - {None})
    if ds:
        for r in rs: pvotes[PLACE[r['stop_id']][:2]][(ds[0], rid)] = 1
def place_okres(sid, nearest=True):
    n, k, _ = PLACE[sid]
    if n.startswith('Praha, '): return None
    # only places in the Středočeský kraj (GTFS zone_region_type 2): Doksy, Slatina, Vrbice and Lety of other kraje share
    # their names with Středočeský municipalities
    if not any((stops[x].get('zone_region_type') or '') == '2' for x in byname[n] if PLACE[x][1] == k): return None
    cand = obec_of(n.split(', ')[0])
    v = collections.Counter()
    for (d, _rid), one in pvotes.get((n, k), {}).items(): v[d] += one
    if len(cand) == 1: return next(iter(cand))
    if cand and any(v.get(d) for d in cand): return max(sorted(cand), key=lambda d: v.get(d, 0))
    if cand and nearest:
        # a name two okresy have (Roztoky u Prahy, Roztoky on the Berounka) and no district line there: the okres whose
        # uniquely named places are nearest
        return min(sorted(cand), key=lambda d: min((dist(COORD[sid], c) for c in UNIQ.get(d, [])), default=9e9))
    return None        # not a Středočeský municipality (a part of one, or a name the lists don't hold)
UNIQ = collections.defaultdict(list)
for sid_ in bus_sids:
    if len(obec_of(PLACE[sid_][0].split(', ')[0])) == 1:
        o_ = place_okres(sid_, nearest=False)
        if o_: UNIQ[o_].append(COORD[sid_])
TAG = {'200': 'BN', '210': 'BE', '220': 'KD', '230': 'KO', '240': 'KH', '250': 'ME', '260': 'MB', '270': 'NB', '280': 'PH',
       '290': 'PZ', '300': 'PB', '310': 'RA'}
FINAL, STOKRES = {}, {}
for sid in sorted(bus_sids):
    n, k, ncl = PLACE[sid]; ok = place_okres(sid)
    if ncl > 1:
        tag = TAG.get(ok) or ('pásmo ' + (stops[sid].get('zone_id') or '?').split(',')[0])
        others = [place_okres(x) for x in byname[n] if PLACE[x][1] != k]
        if ok in others or not ok: tag += f' {k + 1}'
        FINAL[sid] = f"{n} [{tag}]"
    else: FINAL[sid] = n
    STOKRES[FINAL[sid]] = ok

recs = {rid: [x for x in (trip_rec(tid) for tid in tids) if x] for rid, tids in by_route.items() if routes[rid]['route_type'] == '3'}
NCOORD = {FINAL[sid]: COORD[sid] for sid in bus_sids}

lines = {}
short_count = collections.Counter(r['route_short_name'] for r in routes.values())
for rid, r in routes.items():
    sn = r['route_short_name']; mode = MODE.get(r['route_type'], r['route_type'])
    lics = lic_list(rid); ops = sorted({s['sub_agency_name'].strip() for s in subs.get(rid, [])})
    tr = recs.get(rid, []) if mode == 'bus' else []
    ntr = len(by_route.get(rid, []))
    e = dict(route_id=rid, short=sn, long=r['route_long_name'].strip(), mode=mode, licences=lics, operators=ops,
             night=r['is_night'] == '1', regional=r['is_regional'] == '1', substitute=r['is_substitute_transport'] == '1',
             trips=ntr, afternoon=sum(1 for t in tr if 780 <= t['dep'] < 1140))
    # key: the PID number for plain numbered lines; the licence for town lines named 'MHD n' and for a number the feed
    # uses twice (630: Kladno - Beroun and Liberec - Świeradów)
    pre = (lics[0][:3] if lics else '')
    if pre in TOWNMHD and not sn.isdigit():
        e['key'] = lics[0]; e['label'] = f"MHD {TOWNMHD[pre]} {sn.replace('MHD ', '')}"; e['town'] = TOWNMHD[pre]
    elif sn.isdigit() and short_count[sn] == 1:
        e['key'] = sn; e['label'] = sn
    else:
        e['key'] = lics[0] if lics else rid; e['label'] = sn
    if pre in TOWNMHD: e['town'] = TOWNMHD[pre]
    if mode == 'bus':
        ds = sorted({district(l) for l in lics} - {None})
        if ds:
            e['oblast'] = OBL[ds[0]]['id']; e['why'] = f"district licence {', '.join(l for l in lics if district(l))}"
        elif tr and not e['regional'] and not pre in TOWNMHD:
            e['why'] = 'a Prague city line'
        elif tr:
            # its okres where it leaves Prague's surroundings: from the outer end inwards (the end farthest from the centre of
            # Prague over its trips that reach Prague), the first stop in a Středočeský municipality; a line with no Prague end goes to the
            # okres most of its places lie in
            pr = [t for t in tr if t['stops'][0].startswith('Praha, ') or t['stops'][-1].startswith('Praha, ')]
            # Prague-licensed lines (100xxx-104xxx) go by their outer end; a line licensed by another kraj that runs to Prague
            # goes, like a line with no Prague end, to the okres most of its Středočeský places lie in (408 Tábor - Votice - Benešov)
            ends_praha = bool(pr) and any(l[:2] == '10' for l in lics)
            far = max(pr or tr, key=lambda t: max(dist(NCOORD[t['stops'][0]], CENTRE), dist(NCOORD[t['stops'][-1]], CENTRE)))
            seq = far['stops'] if dist(NCOORD[far['stops'][0]], CENTRE) >= dist(NCOORD[far['stops'][-1]], CENTRE) else far['stops'][::-1]
            if ends_praha:
                hit = next(((n, STOKRES[n]) for n in seq if STOKRES.get(n)), None)
                if hit:
                    e['oblast'] = OBL[hit[1]]['id']
                    e['why'] = f"licence {', '.join(lics) or '?'}; outer end {seq[0]}; first stop inwards in a Středočeský municipality: {hit[0]} (okres {OBL[hit[1]]['okres']})"
            else:
                c = collections.Counter(STOKRES[n] for n in {x for t in tr for x in t['stops']} if STOKRES.get(n))
                if c:
                    o = c.most_common(1)[0][0]; e['oblast'] = OBL[o]['id']
                    e['why'] = (f"licence {', '.join(lics) or '?'}; no Prague end; its stops by okres: "
                                + ', '.join(f"{OBL[k]['okres']} {n}" for k, n in c.most_common(3)))
        if 'oblast' not in e:
            k3 = sn.isdigit() and (100 <= int(sn) < 300 or 900 <= int(sn) < 950)
            if 'why' not in e:
                e['why'] = ('a Prague city line' if k3 else 'no stop in a Středočeský municipality' if tr else 'no trips on the service day')
    lines[e['key'] if mode == 'bus' else rid] = e
json.dump(dict(service_date=SD, feed=G['zip'], lines=lines), open(os.path.join(DER, 'lines.json'), 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)

# every bus trip of the day by its ends (any line, Prague city lines too): the 0-minute chain test (a trip that leaves the
# stop where another ends, the minute it ends) and the coverage of Prague stops by the city lines
ends = []
for rid, tr in recs.items():
    k = next((v['key'] for v in lines.values() if v['route_id'] == rid), rid)
    for t in tr: ends.append([k, t['sp'], t['lic'], t['fr'], t['dep'], t['to'], t['arr']])
json.dump(ends, open(os.path.join(DER, 'ends.json'), 'w', encoding='utf-8'), ensure_ascii=False)
city = {}
for rid, tr in recs.items():
    v = next((v for v in lines.values() if v['route_id'] == rid), None)
    if v and v['why'] == 'a Prague city line':
        city[v['key']] = sorted({x for t in tr for x, tm in zip(t['stops'], t['times']) if 780 <= tm < 1140})
json.dump(city, open(os.path.join(DER, 'city_stops.json'), 'w', encoding='utf-8'), ensure_ascii=False)
# every stop with the lines that serve it 13:00-19:00 (any PID bus line), for the reading's "only this line" list
sl = collections.defaultdict(set)
for rid, tr in recs.items():
    k = next((v['key'] for v in lines.values() if v['route_id'] == rid), rid)
    for t in tr:
        for x, tm in zip(t['stops'], t['times']):
            if 780 <= tm < 1140: sl[x].add(k)
json.dump({x: sorted(v) for x, v in sl.items()}, open(os.path.join(DER, 'stop_lines.json'), 'w', encoding='utf-8'), ensure_ascii=False)
# each stop's okres (licence prefix of its district; null for Prague and outside the Středočeský kraj)
json.dump(STOKRES, open(os.path.join(DER, 'stop_okres.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)

# ---------------------------------------------------------------- per oblast: ODIS schema
excluded = CFG.get('exclude_from_model', {})
for o in CFG['oblasti']:
    base = os.path.join(HOME, 'oblasti', o['id']); der = os.path.join(base, 'data', 'derived'); os.makedirs(der, exist_ok=True)
    T, C, chosen = {}, {}, {}
    for rid, e in sorted(((v['route_id'], v) for v in lines.values() if v.get('oblast') == o['id']), key=lambda x: (len(x[1]['key']), x[1]['key'])):
        tr = sorted(recs.get(rid, []), key=lambda t: (t['dep'], t['sp']))
        seen = set(); out = []
        for t in tr:
            k = (t['lic'], t['sp'])
            while k in seen: t['sp'] += 100000; k = (t['lic'], t['sp'])
            seen.add(k); out.append(dict({x: t[x] for x in ('sp', 'lf', 'dep', 'arr', 'fr', 'to', 'stops', 'times', 'lic')}, tid=t['trip_id']))
        L = e['key']
        deps = [t['dep'] for t in out]
        cls_ = 'afternoon' if any(780 <= x < 1140 for x in deps) else 'day' if deps else 'none'
        C[L] = dict(cls=cls_, lics=e['licences'] or [L], areas=[o['id']], name=e['long'], label=e['label'], traction='A',
                    trips=len(out), first=f"{deps[0] // 60}:{deps[0] % 60:02d}" if deps else None,
                    last=f"{deps[-1] // 60 % 24}:{deps[-1] % 60:02d}" if deps else None,
                    afternoon=sum(1 for x in deps if 780 <= x < 1140), operators=e['operators'], why=e['why'],
                    night=e['night'], substitute=e['substitute'], town=e.get('town'))
        if out: T[L] = out
        for lic in e['licences'] or [L]:
            chosen[lic] = dict(lic=lic, name=e['long'], valid_from=SD, valid_to=SD, diversion=False, area=o['id'], trips=len(out))
    for n, obj in (('trips.json', T), ('line_class.json', C), ('versions.json', dict(all=list(chosen.values()), chosen=chosen))):
        json.dump(obj, open(os.path.join(der, n), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f"{o['name']:18} {len(C):3} lines, {sum(1 for c in C.values() if c['cls'] == 'afternoon'):3} with afternoon trips, {sum(len(v) for v in T.values()):5} trips")
nob = [v for v in lines.values() if v['mode'] == 'bus' and 'oblast' not in v]
print('bus lines without an oblast:', len(nob), [(v['label'], v['why']) for v in nob][:60])
print('towns expanded:', sum(1 for k, v in _town.items() if k != v), 'of', len(_town), 'abbreviated; not found:', sorted(k for k, v in _town.items() if k == v)[:80])
