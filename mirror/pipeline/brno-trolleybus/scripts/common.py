"""Shared helpers for the Brno trolleybus pipeline (stdlib only).

The HTTP, GTFS, cycle and schedule-fit helpers are the tram pipeline's own (pipeline/brno/scripts/common.py),
imported from there so both sheets follow the same rules; only the paths and state loading are local.
"""
import collections, importlib.util, json, os, sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # pipeline/brno-trolleybus
PROJECT = os.path.dirname(os.path.dirname(BASE))                        # project root (HTML outputs)
RAW = os.path.join(BASE, 'data', 'raw')
DER = os.path.join(BASE, 'data', 'derived')
ASSETS = os.path.join(BASE, 'assets')
TRAM = os.path.join(os.path.dirname(BASE), 'brno')                     # pipeline/brno

_spec = importlib.util.spec_from_file_location('brno_tram_common', os.path.join(TRAM, 'scripts', 'common.py'))
_t = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(_t)
fetch, mins, hm, mm = _t.fetch, _t.mins, _t.hm, _t.mm
gtfs_trips, chain_at, cycle_need = _t.gtfs_trips, _t.chain_at, _t.cycle_need
runfit, best_offset, loop_shift, DIV60, DIV1440, ANY = _t.runfit, _t.best_offset, _t.loop_shift, _t.DIV60, _t.DIV1440, _t.ANY
load, save = _t.load, _t.save

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROUTE_TYPE = '800'   # IDS JMK GTFS marks trolleybus routes 800 (trams 0, buses 3)

def state(name):
    """Load states/<name>.json (name may include .json)."""
    p = os.path.join(BASE, 'states', name if name.endswith('.json') else name + '.json')
    s = load(p); s.setdefault('name', os.path.splitext(os.path.basename(p))[0]); return s

def gtfs_path(S):
    """The trolleybus sheet reads the same IDS JMK feed as the tram sheet: data/raw/gtfs/<date>/ here if
    present, otherwise pipeline/brno/data/raw/gtfs/<date>/."""
    own = os.path.join(RAW, 'gtfs', S['gtfs_date'], 'gtfs.zip')
    return own if os.path.exists(own) else os.path.join(TRAM, 'data', 'raw', 'gtfs', S['gtfs_date'], 'gtfs.zip')

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

def runfit_rate(deps, rate, divs=None, core=(930, 990), lo=780, hi=1200):
    """runfit (the shared rule) restricted to patterns with `rate` departures an hour. A Simutrans line's
    entries must all send the same number of vehicles an hour, or cars pile up at one end: 34, 36, 37 and 35
    change frequency inside the peak, and plain runfit then picks a different stretch at each end.
    Candidates, the core test, the 80 % rule and the simplest-pattern choice are runfit's."""
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
            seen.add((R, a, b)); In, Rn = _t._norm(I, R, divs)
            ov = max(0, min(run[-1], core[1]) - max(run[0], core[0]))
            cands.append(dict(I=In, R=Rn, first=run[0], last=run[-1], n=len(run), core=ov >= 30))
    if not cands: return None
    if any(c['core'] for c in cands): cands = [c for c in cands if c['core']]
    mx = max(c['n'] for c in cands)
    ok = [c for c in cands if c['n'] >= 0.8 * mx]
    return min(ok, key=lambda c: (len(c['R']), c['I'], -c['n']))

def mark_spares(units, need, pm_notes=('odpoledne', 'odpolední kurz'), type_of=lambda u: u['type']):
    """User rule (29 Sep 2026): when a line has more vehicles logged than it needs, keep exactly `need` counted and
    mark the rest "not needed", choosing so that no type of the line's roster is skipped - every type among the
    line's vehicles stays represented among the counted ones, most frequent type first. Within that, afternoon-only
    kurzy are dropped first (user's choice), then the highest kurz numbers; a substitute bus on a trolleybus line
    (u['sub']) is dropped before any trolleybus. Sets u['spare'] = 'not needed' on the surplus; returns the count."""
    if not need or len(units) <= need: return 0
    def drop_first(u):          # higher = dropped earlier
        return (bool(u.get('sub')), any(n in u.get('src', '') for n in pm_notes) and 'ráno' not in u.get('src', ''), u['kurz'])
    keep_order = sorted(units, key=drop_first)          # best to keep first
    freq = collections.Counter(type_of(u) for u in units if not u.get('sub'))   # a substitute bus is no roster type
    keep = []
    for t, _ in freq.most_common():                     # one of every type first
        if len(keep) >= need: break
        keep.append(next(u for u in keep_order if type_of(u) == t))
    for u in keep_order:
        if len(keep) >= need: break
        if u not in keep: keep.append(u)
    n = 0
    for u in units:
        if u not in keep: u['spare'] = 'not needed'; n += 1
    return n
