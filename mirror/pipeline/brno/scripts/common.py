"""Shared helpers for the Brno tram pipeline (stdlib only)."""
import csv, datetime, io, json, os, sys, time, urllib.request, zipfile, collections, statistics

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # pipeline/brno
PROJECT = os.path.dirname(os.path.dirname(BASE))                        # project root (HTML outputs)
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

# ---- polite HTTP -------------------------------------------------------------------------------
# bmhd.cz sits behind a web application firewall that answers 403 "Access Denied" to plain
# clients. A full browser User-Agent plus Accept / Accept-Language headers work. Keep >= 2 s
# between requests.
UA = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
      'Chrome/140.0.0.0 Safari/537.36')
def fetch(url, dest, pause=2.0):
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

# ---- GTFS ----------------------------------------------------------------------------------------
def gtfs_trips(zip_path, service_date, route_type='0'):
    """All trips of the given route_type running on service_date (YYYYMMDD):
    list of dict(line, o, d, dep, arr) with first/last stop names and minutes after midnight."""
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
    fl = {}
    for r in rd('stop_times.txt'):
        if r['trip_id'] not in trips: continue
        q = int(r['stop_sequence']); cur = fl.get(r['trip_id'])
        f = (q, r['stop_id'], r['departure_time']); l = (q, r['stop_id'], r['arrival_time'])
        if not cur: fl[r['trip_id']] = [f, l]
        else:
            if q < cur[0][0]: cur[0] = f
            if q > cur[1][0]: cur[1] = l
    return [dict(id=k, line=routes[t['route_id']], o=stops[fl[k][0][1]], d=stops[fl[k][1][1]],
                 dep=mins(fl[k][0][2]), arr=mins(fl[k][1][2])) for k, t in trips.items() if k in fl]

def chain_at(trips, at=960):
    """Chain trips of one line into vehicles (FIFO at each terminus) and count vehicles
    whose working spans minute `at`."""
    veh = []
    for t in sorted(trips, key=lambda t: t['dep']):
        c = [v for v in veh if v['loc'] == t['o'] and v['free'] <= t['dep']]
        v = min(c, key=lambda v: v['free']) if c else None
        if not v: v = dict(first=t['dep'], trips=[]); veh.append(v)
        v['loc'] = t['d']; v['free'] = t['arr']; v['last'] = t['arr']; v['trips'].append(t)
    return sum(1 for v in veh if v['first'] <= at <= v['last']), veh

def cycle_need(trips, a, b, t0=960, lay=3):
    """Trams a two-terminus line needs around t0: follow a tram leaving a within +-30 min of t0 through
    a -> b -> a, always taking the first departure at least `lay` minutes after arriving. The number of
    departures from a during that round trip is the number of trams in the cycle. Depot runs do not
    distort it (unlike chain_at). Returns (trams, cycle minutes) - the worst case over the window."""
    A = sorted(t['dep'] for t in trips if t['o'] == a and t['d'] == b)
    B = sorted(t['dep'] for t in trips if t['o'] == b and t['d'] == a)
    ra = {t['dep']: t['arr'] - t['dep'] for t in trips if t['o'] == a and t['d'] == b}
    rb = {t['dep']: t['arr'] - t['dep'] for t in trips if t['o'] == b and t['d'] == a}
    res = []
    for s in [x for x in A if t0 - 30 <= x < t0 + 30]:
        nb = next((x for x in B if x >= s + ra[s] + lay), None)
        if nb is None: continue
        na = next((x for x in A if x >= nb + rb[nb] + lay), None)
        if na is None: continue
        res.append((sum(1 for x in A if s <= x < na), na - s))
    return max(res) if res else None

# ---- schedule fit (shared rule, see pipeline/README.md) ------------------------------------------
DIV60 = [d for d in range(1, 61) if 60 % d == 0]
DIV1440 = [d for d in range(1, 61) if 1440 % d == 0]
ANY = list(range(1, 61))

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
            # de-duplicate on the run, not on R alone: the same slot set can recur in a later run
            # (e.g. every 10 before the peak and again after it); skipping it lost the peak run.
            if len(run) < 2 or (R, a, b) in seen: continue
            seen.add((R, a, b)); In, Rn = _norm(I, R, divs)
            ov = max(0, min(run[-1], core[1]) - max(run[0], core[0]))
            cands.append(dict(I=In, R=Rn, first=run[0], last=run[-1], n=len(run), core=ov >= 30))
    if not cands: return None
    if any(c['core'] for c in cands): cands = [c for c in cands if c['core']]
    mx = max(c['n'] for c in cands)
    ok = [c for c in cands if c['n'] >= 0.8 * mx]
    return min(ok, key=lambda c: (len(c['R']), c['I'], -c['n']))

def best_offset(deps, I, lo=900, hi=990):
    """Approximate fit: single-slot interval I with the offset of least total deviation."""
    ds = [t for t in deps if lo <= t < hi]; best = None
    for o in range(I):
        dev = [min(abs(t - s) for s in range(lo - I, hi + I) if s % I == o) for t in ds]
        k = (sum(dev), max(dev))
        if best is None or k < best[0]: best = (k, o, max(dev))
    return best[1], best[2]

def loop_shift(I, R, loop):
    """Values to type in: real minute - 1 at loop termini (mod interval)."""
    return [(r - 1) % I for r in R] if loop else list(R)
