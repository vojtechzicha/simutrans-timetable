"""Shared helpers for the Olomouc bus pipeline (stdlib only).

Self-contained copies of the helpers the other city pipelines use, so that edits in those folders cannot change
this sheet silently:
- fetch, GTFS reader, cycle_need, runfit, loop_shift: pipeline/brno/scripts/common.py (identical to the copy in
  pipeline/olomouc/scripts/common.py, the shared fit rule of pipeline/README.md);
- runfit_rate, mark_spares: pipeline/brno-trolleybus/scripts/common.py;
- cycle_need_peak: pipeline/ostrava-trolleybus/scripts/lib.py;
- parse_vypis, parse_register: pipeline/olomouc/scripts/common.py (seznam-autobusu.cz pages).
Keep them in step with those files when the shared rules change.
"""
import collections, csv, datetime, html as _html, io, json, os, re, sys, time, urllib.request, zipfile

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # pipeline/olomouc-bus
PIPE = os.path.dirname(BASE)                                          # pipeline/
PROJECT = os.path.dirname(PIPE)                                       # project root (HTML outputs)
RAW = os.path.join(BASE, 'data', 'raw')
DER = os.path.join(BASE, 'data', 'derived')
ASSETS = os.path.join(BASE, 'assets')

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def load(path):
    with open(path, encoding='utf-8') as f: return json.load(f)

def save(obj, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f: json.dump(obj, f, ensure_ascii=False, indent=1)

def state(name):
    """Load states/<name>.json (name may include .json)."""
    p = os.path.join(BASE, 'states', name if name.endswith('.json') else name + '.json')
    s = load(p); s.setdefault('name', os.path.splitext(os.path.basename(p))[0]); return s

def gtfs_path(S):
    """The DPMO feed: data/raw/gtfs/<date>/gtfs.zip here if present, otherwise the tram pipeline's stored copy
    (pipeline/olomouc/data/raw/gtfs/<date>/gtfs.zip, the same file; read only)."""
    own = os.path.join(RAW, 'gtfs', S['gtfs']['raw'], 'gtfs.zip')
    return own if os.path.exists(own) else os.path.join(PIPE, 'olomouc', 'data', 'raw', 'gtfs', S['gtfs']['raw'], 'gtfs.zip')

# ---- polite HTTP -------------------------------------------------------------------------------
# A plain browser User-Agent; no personal identifier in any header. At most about one request a second.
UA = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
      'Chrome/140.0.0.0 Safari/537.36')
def fetch(url, dest, pause=1.2):
    req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept': 'text/html,application/xhtml+xml,*/*;q=0.8',
                                               'Accept-Language': 'cs,en;q=0.8'})
    with urllib.request.urlopen(req, timeout=120) as r: data = r.read()
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, 'wb') as f: f.write(data)
    time.sleep(pause)
    return data

# ---- time helpers ------------------------------------------------------------------------------
def mins(t):  # 'HH:MM:SS' (may exceed 24 h) -> minutes after midnight
    h, m = t.split(':')[:2]; return int(h) * 60 + int(m)
hm = lambda m: f'{m // 60}:{m % 60:02d}'
mm = lambda m: ':%02d' % m

def nice(d):
    d = d.replace('-', ''); x = datetime.date(int(d[:4]), int(d[4:6]), int(d[6:]))
    return f"{x.strftime('%a')} {x.day} {x.strftime('%b')} {x.year}"

# ---- GTFS ----------------------------------------------------------------------------------------
def gtfs_trips(zip_path, service_date, route_type='3'):
    """All trips of the given route_type running on service_date (YYYYMMDD):
    list of dict(id, line, o, d, dep, arr, stops, times) with first/last stop names and minutes after midnight;
    times = the departure minute at each stop (added 25 Oct 2026, for reading a trip at a terminus it passes)."""
    z = zipfile.ZipFile(zip_path)
    rd = lambda n: csv.DictReader(io.TextIOWrapper(z.open(n), encoding='utf-8-sig'))
    routes = {r['route_id']: r['route_short_name'] for r in rd('routes.txt') if r['route_type'] == route_type}
    cal = {r['service_id']: r for r in rd('calendar.txt')}
    cd = collections.defaultdict(dict)
    for r in rd('calendar_dates.txt'): cd[r['service_id']][r['date']] = r['exception_type']
    wd = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'][
        datetime.date(int(service_date[:4]), int(service_date[4:6]), int(service_date[6:])).weekday()]
    def active(sid):
        e = cd[sid].get(service_date)
        if e: return e == '1'
        c = cal.get(sid)
        return bool(c) and c['start_date'] <= service_date <= c['end_date'] and c[wd] == '1'
    trips = {t['trip_id']: t for t in rd('trips.txt') if t['route_id'] in routes and active(t['service_id'])}
    stops = {r['stop_id']: r['stop_name'].replace('\xa0', ' ') for r in rd('stops.txt')}
    st = collections.defaultdict(list)
    for r in rd('stop_times.txt'):
        if r['trip_id'] in trips: st[r['trip_id']].append((int(r['stop_sequence']), r['stop_id'], r['arrival_time'], r['departure_time']))
    out = []
    for k, t in trips.items():
        s = sorted(st.get(k, []))
        if len(s) < 2: continue
        out.append(dict(id=k, line=routes[t['route_id']], o=stops[s[0][1]], d=stops[s[-1][1]], dep=mins(s[0][3]), arr=mins(s[-1][2]),
                        stops=[stops[x[1]] for x in s], times=[mins(x[3]) for x in s]))
    return out

def cycle_need_peak(trips, a, b, t0=960, lay=3, max_wait=30):
    """cycle_need (the shared tram rule) restricted to round trips that stay on the branch: follow a vehicle
    leaving a within +-30 min of t0 through a -> b -> a, always taking the first departure at least the layover
    later (lay: minutes, or {terminus: minutes}); the departures from a during that round trip are the vehicles.
    A start is skipped when the vehicle would wait more than max_wait min at either end (the branch's return trips
    have ended, the vehicle leaves as another line). Returns (vehicles, cycle minutes), the worst case."""
    la, lb = (lay.get(a, 3), lay.get(b, 3)) if isinstance(lay, dict) else (lay, lay)
    A = sorted(t['dep'] for t in trips if t['o'] == a and t['d'] == b)
    B = sorted(t['dep'] for t in trips if t['o'] == b and t['d'] == a)
    ra = {t['dep']: t['arr'] - t['dep'] for t in trips if t['o'] == a and t['d'] == b}
    rb = {t['dep']: t['arr'] - t['dep'] for t in trips if t['o'] == b and t['d'] == a}
    res = []
    for s in [x for x in A if t0 - 30 <= x < t0 + 30]:
        nb = next((x for x in B if x >= s + ra[s] + lb), None)
        if nb is None or nb - (s + ra[s]) > max_wait: continue
        na = next((x for x in A if x >= nb + rb[nb] + la), None)
        if na is None or na - (nb + rb[nb]) > max_wait: continue
        res.append((sum(1 for x in A if s <= x < na), na - s))
    return max(res) if res else None

# circuit_need and turnarounds: verbatim from pipeline/brno-trolleybus/scripts/common.py
def circuit_need(trips, legs, t0=960, lay=1, links=None, period=None, core=(900, 1020), maxwait=None):
    """Vehicles a circulation of several legs needs around t0 - cycle_need generalised to N legs
    (through-running pairs such as 25 + 26, or 38 + 39). legs = [(line, from, to), ...], in order, the last
    leg ending where the first starts. Follow a vehicle leaving leg 0 within +-30 min of t0 through every
    leg, always taking the first departure at least `lay` minutes (plus any empty run in `links`:
    {stop: [next stop, minutes]}) after arriving. Vehicles = departures of leg 0 during that cycle.
    period: a circuit longer than the peak (25 + 26 takes over 4 hours) runs out of peak trips before it
    closes; with period=P the peak pattern of each leg (departures and runtimes within `core`) is repeated
    every P minutes, i.e. the vehicle count of the peak timetable run as a steady state.
    lay: minutes, or {leg index: minutes} for the turnaround before that leg (see turnarounds()).
    maxwait: skip a start whose round trip waits longer than this anywhere (the Ostrava trolleybus guard,
    cycle_need_peak: on a sparse line the last peak trip otherwise waits for the next day's).
    Returns (vehicles, cycle minutes, [(leg, dep, arr), ...]) - the worst case over the window."""
    links = links or {}
    deps = [sorted((t['dep'], t['arr']) for t in trips if (t['line'], t['o'], t['d']) == tuple(l)) for l in legs]
    if period:
        deps = [sorted((d + k * period, a + k * period) for d, a in D if core[0] <= d < core[1]
                       for k in range(-2, 40)) for D in deps]
        deps = [[x for i, x in enumerate(D) if i == 0 or x[0] != D[i - 1][0]] for D in deps]
    res = []
    for s, a in [x for x in deps[0] if t0 - 30 <= x[0] < t0 + 30]:
        path = [(0, s, a)]; ok = True
        for i in range(1, len(legs) + 1):
            prev = legs[i - 1][2]; dh = links.get(prev, [prev, 0])[1]
            ly = lay.get(i % len(legs), 3) if isinstance(lay, dict) else lay
            nxt = next((x for x in deps[i % len(legs)] if x[0] >= path[-1][2] + dh + ly), None)
            if nxt is None or (maxwait and nxt[0] - (path[-1][2] + dh) > maxwait): ok = False; break
            path.append((i % len(legs), *nxt))
        if not ok: continue
        end = path[-1][1]
        res.append((sum(1 for x in deps[0] if s <= x[0] < end), end - s, path[:-1]))
    return max(res, key=lambda r: (r[0], r[1])) if res else None

def turnarounds(trips, legs, default=3, links=None, window=(900, 1020)):
    """Turnaround before each leg of a circuit: the default layover, or the terminus's own shorter one where
    the timetable shows it - the smallest gap between an arrival of the previous leg and the first departure
    of this leg after it (Barvičova, Preslova and Pálavské náměstí turn in the same minute).
    Returns {leg index: minutes}."""
    links = links or {}; out = {}
    for i in range(len(legs)):
        prev = legs[i - 1]; dh = links.get(prev[2], [prev[2], 0])[1]
        arr = [t['arr'] + dh for t in trips if (t['line'], t['o'], t['d']) == tuple(prev) and window[0] <= t['arr'] < window[1]]
        dep = sorted(t['dep'] for t in trips if (t['line'], t['o'], t['d']) == tuple(legs[i]))
        gaps = [next((d for d in dep if d >= a), a + 99) - a for a in arr]
        out[i] = min(default, min(gaps)) if gaps else default
    return out

def min_turnaround(trips, lo=900, hi=1080):
    """{terminus: shortest timetabled turnaround in lo..hi} - each arrival to the first departure at or after it."""
    out = {}
    for st in {t['d'] for t in trips}:
        arr = [t['arr'] for t in trips if t['d'] == st and lo <= t['arr'] < hi]
        dep = sorted(t['dep'] for t in trips if t['o'] == st)
        gaps = [next((d for d in dep if d >= a), a + 99) - a for a in arr]
        if gaps: out[st] = min(gaps)
    return out

# ---- schedule fit (shared rule, see pipeline/README.md) ------------------------------------------
DIV60 = [d for d in range(1, 61) if 60 % d == 0]
DIV1440 = [d for d in range(1, 61) if 1440 % d == 0]

def _norm(I, R, divs):
    R = set(R)
    for d in divs:
        if I % d: continue
        base = {r % d for r in R}
        if {r for r in range(I) if r % d in base} == R: return d, sorted(base)
    return I, sorted(R)

def runfit(deps, divs=DIV1440, core=(930, 990), lo=780, hi=1200):
    """Longest exact run of one Departure-every/Offset/Also-at pattern (<= 8 slots) around the core
    window. Returns dict(I, R, first, last, n, core) - R[0] is the offset, R[1:] the Also-at values."""
    D = sorted(set(t for t in deps if lo <= t < hi)); S = set(D); cands = []
    for I in divs:
        seen = set()
        for t0 in D:
            R = tuple(sorted({t % I for t in D if t0 <= t < t0 + I}))
            if len(R) > 8: continue
            a = t0
            while a - 1 >= lo and ((a - 1) in S) == ((a - 1) % I in R): a -= 1
            b = t0
            while b + 1 < hi and ((b + 1) in S) == ((b + 1) % I in R): b += 1
            run = [t for t in D if a <= t <= b]
            # de-duplicate on the run, not on R alone (bug fixed 28 Sep in every copy of runfit)
            if len(run) < 2 or (R, a, b) in seen: continue
            seen.add((R, a, b)); In, Rn = _norm(I, R, divs)
            ov = max(0, min(run[-1], core[1]) - max(run[0], core[0]))
            cands.append(dict(I=In, R=Rn, first=run[0], last=run[-1], n=len(run), core=ov >= 30))
    if not cands: return None
    if any(c['core'] for c in cands): cands = [c for c in cands if c['core']]
    mx = max(c['n'] for c in cands)
    ok = [c for c in cands if c['n'] >= 0.8 * mx]
    return min(ok, key=lambda c: (len(c['R']), c['I'], -c['n']))

def runfit_rate(deps, rate, divs=None, core=(930, 990), lo=780, hi=1200):
    """runfit restricted to patterns with `rate` departures an hour (brno-trolleybus): both ends of a Simutrans
    line must send the same number of vehicles an hour."""
    divs = divs or DIV1440
    D = sorted(set(t for t in deps if lo <= t < hi)); S = set(D); cands = []
    for I in divs:
        if (rate * I) % 60 or rate * I // 60 > 8: continue
        k = rate * I // 60; seen = set()
        for t0 in D:
            R = tuple(sorted({t % I for t in D if t0 <= t < t0 + I}))
            if len(R) != k: continue
            a = t0
            while a - 1 >= lo and ((a - 1) in S) == ((a - 1) % I in R): a -= 1
            b = t0
            while b + 1 < hi and ((b + 1) in S) == ((b + 1) % I in R): b += 1
            run = [t for t in D if a <= t <= b]
            if len(run) < 2 or (R, a, b) in seen: continue
            seen.add((R, a, b)); In, Rn = _norm(I, R, divs)
            ov = max(0, min(run[-1], core[1]) - max(run[0], core[0]))
            cands.append(dict(I=In, R=Rn, first=run[0], last=run[-1], n=len(run), core=ov >= 30))
    if not cands: return None
    if any(c['core'] for c in cands): cands = [c for c in cands if c['core']]
    mx = max(c['n'] for c in cands)
    ok = [c for c in cands if c['n'] >= 0.8 * mx]
    return min(ok, key=lambda c: (len(c['R']), c['I'], -c['n']))

def loop_shift(I, R, loop):
    """Values to type in. R are departure times mod I counted from midnight; the fork counts its offsets from 01:00 (owner,
    3 Oct 2026; kb/rules/fork-schedule.md), so typed = (real - 60) mod I, and a loop terminus is entered 1 min early. For
    intervals dividing 60 the 01:00 origin changes nothing; for 8 it is 4 min. Fixed here 25 Oct 2026 (it had been left out of
    this copy when the Ostrava lib was fixed on 20 Oct). The order of R is kept, so set[i] stays paired with real[i]."""
    return [(r - 60 - (1 if loop else 0)) % I for r in R]

def mark_spares(units, need, pm_notes=('odpoledne', 'odpolední kurz'), type_of=lambda u: u['type']):
    """User rule (29 Sep 2026; brno-trolleybus common.py): keep exactly `need` counted, one of every roster type first
    (most frequent type first), then drop afternoon-only kurzy first, then the highest kurz numbers. Sets
    u['spare'] = 'not needed' on the surplus; returns the count."""
    if not need or len(units) <= need: return 0
    def drop_first(u):
        return (bool(u.get('sub')), any(n in u.get('src', '') for n in pm_notes) and 'ráno' not in u.get('src', ''), u['kurz'])
    keep_order = sorted(units, key=drop_first)
    freq = collections.Counter(type_of(u) for u in units if not u.get('sub'))
    keep = []
    for t, _ in freq.most_common():
        if len(keep) >= need: break
        keep.append(next(u for u in keep_order if type_of(u) == t))
    for u in keep_order:
        if len(keep) >= need: break
        if u not in keep: keep.append(u)
    n = 0
    for u in units:
        if u not in keep: u['spare'] = 'not needed'; n += 1
    return n

# ---- seznam-autobusu.cz parsing ----------------------------------------------------------------------------
def _txt(s):
    return re.sub(r'\s+', ' ', _html.unescape(re.sub(r'<!--.*?-->|<[^>]+>', ' ', s, flags=re.S))).strip()

def parse_vypis(path):
    """One vypravenost/<slug>/vypis page -> list of dict(date, car, ids, line, course, note, author)."""
    t = open(path, encoding='utf-8').read(); out = []
    for tr in re.findall(r'<tr class="row[^"]*">(.*?)</tr>', t, flags=re.S):
        ids = list(dict.fromkeys(re.findall(r'/vuz/(\d+)/vypravenost', tr)))
        tr = re.sub(r"data-bmhd-context-box='.*?'", '', tr, flags=re.S)
        cell = lambda c: _txt(m.group(1)) if (m := re.search(r'<td class="%s">(.*?)</td>' % c, tr, flags=re.S)) else ''
        d = cell('date'); md = re.search(r'(\d{2})\.(\d{2})\.\s*(\d{4})', d)
        out.append(dict(date=f'{md.group(3)}-{md.group(2)}-{md.group(1)}' if md else d, car=cell('car').replace(' + ', '+'), ids=ids,
                        line=cell('route'), course=cell('order-on-line'), note=cell('note'), author=cell('authors')))
    return out

def parse_overview(path):
    """A day overview (vypravenost/<slug>?datum=D) -> {(mode class, line): [(course or '', car)]}."""
    t = open(path, encoding='utf-8').read(); out = {}
    for m in re.finditer(r'<span class="route (\w+)"><!--\s*--><a href="[^"]*">([^<]+)</a>(.*?)(?=<span class="route |<h2|<footer|$)', t, flags=re.S):
        items = []
        for it in re.findall(r'<span class="item">(.*?)</span>\s*(?=<span class="item">|</div>|$)', m.group(3), flags=re.S):
            c = re.search(r'<span class="course">([^<]*)</span>', it)
            cars = re.findall(r'class="context-box" href="[^"]*">([^<]+)</a>', it)
            items.append((c.group(1).strip() if c else '', '+'.join(cars)))
        out[(m.group(1), m.group(2).strip())] = items
    return out

def parse_register(paths):
    """Pages of /seznam?iddopravce=... -> {fleet number: dict(id, type, types, paint, depot, year, state, reg)}."""
    t = ''.join(open(p, encoding='utf-8').read() for p in paths); veh = {}
    for b in re.split(r'(?=<tr class="car-line [^"]*first-line" data-car-id)', t)[1:]:
        m = re.search(r'<span class="bold 1 number"><!--\s*-->(\d+)', b)
        if not m: continue
        cid = re.search(r'data-car-id="(\d+)"', b)
        mt = re.search(r'<td class="manufacturer-type">(.*?)</td>', b, re.S)
        typ = re.findall(r'<b>([^<]+)</b>', mt.group(1)) if mt else []
        pm = re.search(r'<span class="label">nátěr:</span>(.*?)</span>', b, re.S)
        paint = _txt(pm.group(1)).rstrip('*').strip() if pm else ''
        yr = re.search(r'<td class="font085">(\d{4})', b)
        veh[m.group(1)] = dict(id=cid.group(1) if cid else '', type=typ[-1] if typ else '', types=typ, paint=paint,
                               year=yr.group(1) if yr else '', state=re.search(r'<tr class="car-line (\w+)', b).group(1))
    return veh
