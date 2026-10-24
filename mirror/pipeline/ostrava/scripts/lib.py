"""Shared helpers for the Ostrava tram pipeline (stdlib only)."""
import collections, fractions, csv, datetime, gzip, html, io, json, os, re, time, urllib.request, zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))          # pipeline/ostrava
PROJECT = os.path.dirname(os.path.dirname(ROOT))                             # Simutrans-Timetable
CONFIG = json.load(open(os.path.join(ROOT, 'config.json'), encoding='utf-8'))
RAW = os.path.join(ROOT, 'data', 'raw', CONFIG['snapshot'])
DERIVED = os.path.join(ROOT, 'data', 'derived')
os.makedirs(DERIVED, exist_ok=True)

def dpath(name): return os.path.join(DERIVED, name)
def save(name, obj): json.dump(obj, open(dpath(name), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
def load(name): return json.load(open(dpath(name), encoding='utf-8'))
def hm(m): return '%d:%02d' % (m // 60, m % 60)
def hhmm(m): return '%02d:%02d' % (m // 60, m % 60)
def day(s): return datetime.date.fromisoformat(s)

# ---------------------------------------------------------------- HTTP
# seznam-autobusu.cz sits behind a WAF that answers 403/466 to bare clients;
# a full browser User-Agent plus Accept / Accept-Language gets through.
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'cs-CZ,cs;q=0.9,en;q=0.8',
    'Accept-Encoding': 'gzip',
}
def http(url, data=None, headers=None, pause=2.0, binary=False):
    h = dict(HEADERS); h.update(headers or {})
    req = urllib.request.Request(url, data=data, headers=h)
    with urllib.request.urlopen(req, timeout=120) as r:
        b = r.read()
        if r.headers.get('Content-Encoding') == 'gzip': b = gzip.decompress(b)
    time.sleep(pause)                      # be gentle: 2 s between requests
    return b if binary else b.decode('utf-8', 'replace')

# ---------------------------------------------------------------- seznam-autobusu parsers
def _clean(t):
    t = re.sub(r'<!--.*?-->', '', t, flags=re.S)
    t = re.sub(r"data-bmhd-context-box='.*?'", '', t, flags=re.S)
    return html.unescape(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', t))).strip()

def parse_vypravenost(s):
    """rows of a /vypravenost/.../vypis page -> dicts"""
    out = []
    for m in re.finditer(r'<tr class="row ([^"]*)">(.*?)</tr>', s, flags=re.S):
        cls, b = m.group(1), m.group(2)
        def cell(c):
            mm = re.search(r'<td class="%s">(.*?)</td>' % c, b, flags=re.S)
            return _clean(mm.group(1)) if mm else ''
        out.append(dict(cls=cls.replace(' even', ''), date=cell('date'), car=cell('car'), line=cell('route'),
                        kurz=cell('order-on-line'), note=cell('note'), by=cell('authors'),
                        vid=(re.search(r'/vuz/(\d+)', b) or [None, None])[1]))   # register id (buses are recorded by plate)
    return out

def parse_fleet_list(s):
    """rows of a /seznam?... fleet list page -> {car_id: dict(state,num,type,year,note)}"""
    cars = {}
    for m in re.finditer(r'<tr class="car-line ([a-z-]+) [^"]*first-line" data-car-id="(\d+)"(.*?)(?=<tr class="car-line [a-z-]+ [^"]*first-line"|</table>)', s, flags=re.S):
        st, cid, b = m.groups()
        num = re.search(r'class="bold \d+ number">(.*?)</span>', b, flags=re.S)
        mt = re.search(r'<td class="manufacturer-type">(.*?)</td>', b, flags=re.S)
        yr = re.search(r'<td class="font085">(\d{4})', b)
        note = re.search(r"<td class='note[^']*'[^>]*>(.*?)</td>", b, flags=re.S)
        cars[cid] = dict(state=st, num=_clean(num.group(1)) if num else '', type=_clean(mt.group(1)) if mt else '',
                         year=yr.group(1) if yr else '', note=_clean(note.group(1)) if note else '')
    return cars

def next_page(s, p):
    return f'page={p + 1}&' in s.replace('&amp;', '&') or f'strana={p + 1}&' in s.replace('&amp;', '&')

def record_date(s):
    m = re.search(r'(\d\d)\.(\d\d)\. (\d{4})', s)
    return datetime.date(int(m.group(3)), int(m.group(2)), int(m.group(1))) if m else None

# ---------------------------------------------------------------- JDF (CIS JŘ city timetables)
def jdf_open(zpath):
    """outer JDF.zip holds one inner zip per line version"""
    return zipfile.ZipFile(zpath)

def jdf_tables(outer, inner_name, wanted=('VerzeJDF', 'Linky', 'Zastavky', 'Pevnykod', 'Caskody', 'Spoje', 'Zasspoje')):
    inner = zipfile.ZipFile(io.BytesIO(outer.read(inner_name)))
    names = {n.split('.')[0].lower(): n for n in inner.namelist()}
    out = {}
    for w in wanted:
        n = names.get(w.lower())
        if not n: out[w] = []; continue
        t = inner.read(n).decode('cp1250')
        t = t.replace(';\r\n', '\n').replace(';\n', '\n')
        out[w] = [r for r in csv.reader(io.StringIO(t)) if r]
    return out

def jdf_versions(outer, line_numbers):
    """all inner zips whose Linky row is one of the line numbers -> list of dicts"""
    res = []
    for n in outer.namelist():
        inner = zipfile.ZipFile(io.BytesIO(outer.read(n)))
        ln = [x for x in inner.namelist() if x.lower().startswith('linky')]
        if not ln: continue
        rows = [r for r in csv.reader(io.StringIO(inner.read(ln[0]).decode('cp1250').replace(';\r\n', '\n').replace(';\n', '\n'))) if r]
        for r in rows:
            if r[0] in line_numbers:
                dates = []
                for x in r[2:]:                       # validity from/to; skip the 8-digit IČO
                    if re.fullmatch(r'\d{8}', x):
                        try: dates.append(datetime.datetime.strptime(x, '%d%m%Y').date())
                        except ValueError: pass
                od, do = dates[0], dates[1]
                res.append(dict(inner=n, line=r[0], name=r[1], valid_from=od.isoformat(), valid_to=do.isoformat(), diversion=len(r) > 5 and r[5] == '1'))
    return res

def pick_version(versions, d):
    """among versions valid on day d: latest valid_from wins, ties -> shortest validity"""
    ok = [v for v in versions if day(v['valid_from']) <= d <= day(v['valid_to'])]
    ok.sort(key=lambda v: (-day(v['valid_from']).toordinal(), day(v['valid_to']).toordinal()))
    return ok[0] if ok else None

def _mins(s):
    if not s or not s[:1].isdigit(): return None
    return int(s[:2]) * 60 + int(s[2:4])

def jdf_trips(tables, d):
    """trips running on date d. The Zasspoje time columns are found by row length (JDF 1.8: 10 fields, times at
    8/9; 1.10: 12 fields, 9/10; 1.11: 15 fields, 10/11). Caskody: type 4 "does not run" in a range; types 1 ("runs
    in") and 3 ("runs only in") restrict the trip to their ranges, OR-ed; type 2 "also runs". Both fixes ported on
    29 Sep 2026 from pipeline/pardubice/scripts/common.py (session a2): the old reader read 1.10 as 1.11 and ignored
    type 1, which counted school-holiday-only trips on school days."""
    zast = {r[0]: ','.join(x for x in r[1:4] if x) for r in tables['Zastavky']}
    pk = {r[0]: r[1] for r in tables['Pevnykod']}
    cas = collections.defaultdict(list)
    for r in tables['Caskody']: cas[r[1]].append(r)
    stops = collections.defaultdict(list)
    for r in tables['Zasspoje']:
        ia, idp = (10, 11) if len(r) >= 15 else (9, 10) if len(r) >= 12 else (8, 9)
        a = _mins(r[ia]); dp = _mins(r[idp])
        t = dp if dp is not None else a
        if t is None: continue
        stops[r[1]].append((int(r[2]), zast[r[3]], a if a is not None else t, t))
    wd = str(d.isoweekday())
    trips = []
    for r in tables['Spoje']:
        sp = r[1]; codes = [pk.get(c, '') for c in r[2:12] if c]
        dayc = [c for c in codes if c and c in 'X+1234567']
        ok = (not dayc) or ('X' in dayc and d.isoweekday() <= 5) or wd in dayc
        only = []
        for c in cas.get(sp, []):
            typ = c[4]
            od = datetime.datetime.strptime(c[5], '%d%m%Y').date()
            do = datetime.datetime.strptime(c[6], '%d%m%Y').date() if c[6] else od
            inr = od <= d <= do
            if typ == '4' and inr: ok = False
            if typ in ('1', '3'): only.append(inr)
            if typ == '2' and inr: ok = True
        if only and not any(only): ok = False
        if not ok or sp not in stops: continue
        st = sorted(stops[sp], key=lambda x: x[3])
        trips.append(dict(sp=int(sp), lf='@' in codes, dep=st[0][3], arr=st[-1][2], fr=st[0][1], to=st[-1][1],
                          stops=[s[1] for s in st], times=[s[3] for s in st]))
    return trips

# ---------------------------------------------------------------- vehicle turns
def blocks(trips, maxlay=40):
    """chain trips into vehicle turns at their termini: FIFO, layover up to maxlay min"""
    trips = sorted(trips, key=lambda t: t['dep'])
    free = collections.defaultdict(list); bl = []
    for t in trips:
        cand = [(a, b) for a, b in free[t['fr']] if a <= t['dep'] <= a + maxlay]
        if cand:
            a, b = min(cand, key=lambda x: x[0]); free[t['fr']].remove((a, b))
        else:
            b = len(bl); bl.append([])
        bl[b].append(t); free[t['to']].append((t['arr'], b))
    return bl

def active_at(bl, T): return [b for b in bl if b[0]['dep'] <= T <= b[-1]['arr']]

# ---------------------------------------------------------------- round-trip need (shared, as pipeline/brno common.py)
def min_turnaround(trips, lo=840, hi=1080, maxlay=40):
    """shortest timetabled turnaround per terminus (arrival -> next departure of a chained turn), lo..hi"""
    out = {}
    for b in blocks(trips, maxlay):
        for x, y in zip(b, b[1:]):
            if lo <= y['dep'] < hi: out[y['o'] if 'o' in y else y['fr']] = min(out.get(y['o'] if 'o' in y else y['fr'], 99), y['dep'] - x['arr'])
    return out

def cycle_need(trips, a, b, t0=960, lay=3):
    """Trams a two-terminus branch needs around t0: follow a tram leaving a within +-30 min of t0 through
    a -> b -> a, always taking the first departure at least `lay` min after arriving. The departures from a
    during that round trip = trams. Worst case over the window. trips need keys o, d (names), dep, arr."""
    la, lb = (lay.get(a, 3), lay.get(b, 3)) if isinstance(lay, dict) else (lay, lay)   # per-terminus layover
    A = sorted(t['dep'] for t in trips if t['o'] == a and t['d'] == b)
    B = sorted(t['dep'] for t in trips if t['o'] == b and t['d'] == a)
    ra = {t['dep']: t['arr'] - t['dep'] for t in trips if t['o'] == a and t['d'] == b}
    rb = {t['dep']: t['arr'] - t['dep'] for t in trips if t['o'] == b and t['d'] == a}
    res = []
    for s in [x for x in A if t0 - 30 <= x < t0 + 30]:
        nb = next((x for x in B if x >= s + ra[s] + lb), None)
        if nb is None: continue
        na = next((x for x in A if x >= nb + rb[nb] + la), None)
        if na is None: continue
        res.append((sum(1 for x in A if s <= x < na), na - s))
    return max(res) if res else None

def circuit_need(legs, t0=960, lay=3):
    """Trams a circuit over several lines needs around t0. legs = [(trips, a, b), ...] in circulation order, the
    last leg ending where the first starts; trips need keys o, d, dep, arr. Follow a tram leaving the first leg's
    start within +-30 min of t0, always taking the first departure of the next leg at least `lay` (per stop) min
    after arriving. Departures of the first leg during the circuit = trams. Worst case over the window.
    Returns (trams, cycle, waits per leg start)."""
    lay_ = (lambda s: lay.get(s, 3)) if isinstance(lay, dict) else (lambda s: lay)
    D = [sorted((t['dep'], t['arr']) for t in tr if t['o'] == a and t['d'] == b) for tr, a, b in legs]
    res = []
    for s, arr in [x for x in D[0] if t0 - 30 <= x[0] < t0 + 30]:
        waits = [0]; ok = True
        for k in list(range(1, len(legs))) + [0]:
            nx = next((x for x in D[k] if x[0] >= arr + lay_(legs[k][1])), None)
            if nx is None: ok = False; break
            if k: waits.append(nx[0] - arr); arr = nx[1]
            else: res.append((sum(1 for x in D[0] if s <= x[0] < nx[0]), nx[0] - s, waits))
        if not ok: continue
    return max(res, key=lambda r: r[:2]) if res else None

# ---------------------------------------------------------------- Simutrans schedule fit (shared rule, pipeline/README.md)
DIV60 = [d for d in range(1, 61) if 60 % d == 0]
DIV1440 = [d for d in range(1, 61) if 1440 % d == 0]      # divisors of 60 come first in this list's use below
def _norm(I, R, divs):
    R = set(R)
    for d in divs:
        if I % d: continue
        base = {r % d for r in R}
        if {r for r in range(I) if r % d in base} == R: return d, sorted(base)
    return I, sorted(R)

def runfit(deps, core=(930, 990), lo=780, hi=1200, divs=DIV1440, rate=None):
    """Longest exact run of one Departure-every/Offset/Also-at pattern (<= 8 slots) around the core window,
    clipped to its first and last real departure; >= 2 departures; among runs covering >= 80 % of the best,
    the simplest (fewest slots, then shortest interval). As pipeline/brno/scripts/common.py, with the
    de-duplication fixed (per run, not per slot set)."""
    D = sorted(set(t for t in deps if lo <= t < hi)); S = set(D); cands = []
    for I in divs:
        seen = set()
        for t0 in D:
            R = tuple(sorted({t % I for t in D if t0 <= t < t0 + I}))
            if len(R) > 8: continue
            In, Rn = _norm(I, R, divs)
            a = t0
            while a - 1 >= lo and ((a - 1) in S) == ((a - 1) % I in R): a -= 1
            b = t0
            while b + 1 < hi and ((b + 1) in S) == ((b + 1) % I in R): b += 1
            run = [t for t in D if a <= t <= b]
            # de-duplicate on the run, not on R alone: the same slot set can recur in a later run
            # (e.g. a 10-min pattern broken by peak extras and resumed), which must still be a candidate
            if len(run) < 2 or (R, a, b) in seen: continue
            seen.add((R, a, b))
            ov = max(0, min(run[-1], core[1]) - max(run[0], core[0]))
            cands.append(dict(I=In, R=Rn, first=run[0], last=run[-1], n=len(run), core=ov >= 30))
    if rate is not None: cands = [c for c in cands if fractions.Fraction(len(c['R']) * 60, c['I']) == rate]   # departures per hour
    if not cands: return None
    if any(c['core'] for c in cands): cands = [c for c in cands if c['core']]
    mx = max(c['n'] for c in cands)
    ok = [c for c in cands if c['n'] >= 0.8 * mx]
    return min(ok, key=lambda c: (len(c['R']), c['I'], -c['n']))

def loop_shift(I, R, loop=True):
    """values to type into the fork: R are departure times mod I counted from midnight; the fork counts its offsets
    from 01:00 (offset = (real - 60) mod interval, simutrans-fork-schedule-spec), and a loop terminus (smyčka) is
    entered 1 min before the timetable. For intervals dividing 60 the 01:00 origin changes nothing; for 40 it is 20 min."""
    return sorted((r - 60 - (1 if loop else 0)) % I for r in R)
def real_of(I, v, loop=True):
    """inverse of loop_shift for one typed value: the departure time mod I from midnight"""
    return (v + 60 + (1 if loop else 0)) % I

def plans(trips, nm, fitcfg, pullin_dests, loop=True, peak=960, keep=None):
    """per (from,to) branch of one line. fitcfg = dict(window=[a,b], core=[c0,c1], lo, hi).
    Branches with <3 trips in the window, or listed as pull-ins, are not scheduled; their minutes are
    merged into the main branch from the same terminus."""
    a0, b0 = fitcfg['window']
    g = collections.defaultdict(list)
    for t in trips: g[(nm(t['fr']), nm(t['to']))].append(t['dep'])
    pk = lambda d: sum(1 for x in d if a0 <= x < b0)
    # keep(fr, to): directions of a branch the caller models as its own Simutrans line (bus: regular afternoon branches
    # like 23 to Bohumín, Záblatí, owner 20 Oct 2026) always get a row, however few trips 15:00-18:00 they have
    small0 = lambda k: (pk(g[k]) < 3 or k[1] in pullin_dests or (keep is not None and not keep(*k))) and not (keep and keep(*k))
    stp = collections.defaultdict(set)
    for t in trips:
        if t.get('stops'): stp[(nm(t['fr']), nm(t['to']))].update(t['stops'])
    # a direction whose opposite direction is scheduled is scheduled too, so both ends of a branch get a row (bus 27:
    # Proskovice -> Hrabová, statek runs 2x in 15:00-18:00 against 3x the other way; merging it doubled another row)
    small = lambda k: small0(k) and not (k[1] not in pullin_dests and (k[1], k[0]) in g and not small0((k[1], k[0])) and pk(g[k]) > 0)
    out = []
    for (fr, to), d in sorted(g.items(), key=lambda x: -len(x[1])):
        kept = bool(keep and keep(fr, to))
        if pk(d) == 0 and not (kept and any(peak - 180 <= x < peak + 180 for x in d)): continue
        if small((fr, to)):
            sib = sorted([k for k in g if k[0] == fr and k != (fr, to) and not small(k)], key=lambda k: -len(stp[k] & stp[(fr, to)]))
            out.append(dict(fr=fr, to=to, every=None, single=[x for x in d if a0 <= x < b0], into=sib[0][1] if sib else None)); continue
        def home(k):   # the branch row a merged direction belongs to: most shared stops (34: Rovniny -> Hlučín, autobusové nádraží)
            sib_ = sorted([q for q in g if q[0] == k[0] and q != k and not small(q)], key=lambda q: -len(stp[q] & stp[k]))
            return sib_[0] if sib_ else None
        extra = [x for k, dd in g.items() if k[0] == fr and k != (fr, to) and pk(dd) > 0 and small(k) and (keep is None or home(k) == (fr, to)) for x in dd if a0 <= x < b0]
        f = runfit(d + extra, tuple(fitcfg['core']), fitcfg['lo'], fitcfg['hi'])
        if not f:   # a sparse kept direction with no exact run: a placeholder the pair check below refits
            dd = sorted(x for x in d if peak - 180 <= x < peak + 180) or sorted(d)
            f = dict(I=60, R=[dd[0] % 60], first=dd[0], last=dd[0], n=1)
        out.append(dict(fr=fr, to=to, every=f['I'], real=f['R'], set=loop_shift(f['I'], f['R'], loop),
                        first=f['first'], last=f['last'], n=f['n'], merged=extra, deps=d + extra))
    # Both ends of a two-terminus branch must send the same number of vehicles per hour (user, 18 Oct 2026: tram 4 left
    # Hranečník 3 an hour against 4 arriving; tram 5 had 3 and 4 uneven slots an hour). Where the two fits differ:
    # 1. every rate either fit (or the real 16:00 hour) offers is fitted exactly on both ends; a candidate counts only if
    #    each end's interval divides 1440 (bus 40 runs exactly every 40), its exact run has >= 4 departures (3 if hourly) and overlaps the peak band (PB, 15:30-17:30)
    #    by >= 30 min. The candidate with the longest combined runs wins (tram 4: 4 an hour, :01 :11 :31 :41).
    # 2. otherwise (irregular bus timetables, 20 Oct 2026) both ends get one even slot at the averaged rate of the peak
    #    band, offset to the smallest worst deviation, marked approximate with that deviation.
    # The same is done where the rates agree but either end's run misses the peak band (bus 68: 13:57-14:37).
    # The fit it replaces is kept in 'refit' for the sheet.
    PB = (peak - 30, peak + 90)
    rate = lambda p: fractions.Fraction(len(p['real']) * 60, p['every'])
    ok = lambda f: f and 1440 % f['I'] == 0 and (f['n'] >= 4 or (f['I'] >= 60 and len(f['R']) == 1 and f['n'] >= 3)) and min(f['last'] + 1, PB[1]) - max(f['first'], PB[0]) >= 30
    def even(deps):
        D = sorted(set(x for x in deps if PB[0] <= x < PB[1])); return D
    for p in out:
        q = next((q for q in out if q['fr'] == p['to'] and q['to'] == p['fr'] and q.get('every')), None)
        if not p.get('every') or not q or p.get('refit') or q.get('refit'): continue
        cur = lambda x_: dict(I=x_['every'], R=x_['real'], n=x_['n'], first=x_['first'], last=x_['last'])
        if rate(p) == rate(q) and ok(cur(p)) and ok(cur(q)): continue   # same rate and both runs cover the peak band
        rates = {rate(p), rate(q)} | {fractions.Fraction(sum(1 for x in set(x_['deps']) if peak <= x < peak + 60)) for x_ in (p, q)}
        best = None
        for r in rates:
            fs = [runfit(x_['deps'], tuple(fitcfg['core']), fitcfg['lo'], fitcfg['hi'], rate=r) for x_ in (p, q)]
            if all(ok(f) for f in fs) and (best is None or fs[0]['n'] + fs[1]['n'] > best[0]): best = (fs[0]['n'] + fs[1]['n'], fs)
        if best: fits = best[1]
        else:
            Ds = [even(x_['deps']) for x_ in (p, q)]; win = PB
            IS = [60 // r for r in (1, 2, 3, 4, 5, 6, 10, 12)]
            if min(len(D) for D in Ds) < 2:   # a sparse branch: fit over 13:00-19:00, intervals up to 120 (dividing 1440)
                win = (peak - 180, peak + 180); IS = [10, 12, 15, 20, 30, 40, 60, 80, 90, 120]
                Ds = [sorted(set(x for x in x_['deps'] if win[0] <= x < win[1])) for x_ in (p, q)]
            per_h = sum(len(D) for D in Ds) / 2 / ((win[1] - win[0]) / 60)
            # the two even intervals next to the averaged rate; keep the one with the smaller combined worst deviation
            near = sorted(IS, key=lambda I: abs(60 / I - per_h))[:2]
            best_a = None; cands_a = []
            # running times of the two directions, for choosing the two offsets together (below)
            def rt_(a, b):   # the longest running time 15:00-18:00 (else 13:00-19:00): the slots then hold for every trip
                r = [t['arr'] - t['dep'] for t in trips if nm(t['fr']) == a and nm(t['to']) == b and t.get('arr') is not None and peak - 60 <= t['dep'] < peak + 120]                     or [t['arr'] - t['dep'] for t in trips if nm(t['fr']) == a and nm(t['to']) == b and t.get('arr') is not None and win[0] <= t['dep'] < win[1]]
                return max(r) if r else 0
            rtA, rtB = rt_(p['fr'], p['to']), rt_(q['fr'], q['to'])
            for I in near:
                r = 60 / I; fs_ = []
                devf = [lambda o, I=I, D=D: max((min((x - o) % I, (o - x) % I) for x in D), default=0) for D in Ds]
                tot = [lambda o, I=I, D=D: sum(min((x - o) % I, (o - x) % I) for x in D) for D in Ds]
                # each end's offsets within a few minutes of its best fit; of those, the pair with the shortest round,
                # so a vehicle does not wait a whole interval at each end (owner, 20 Oct 2026: sparse branches sized
                # from patterns fitted end by end needed up to 3 buses for a bus every 80 min)
                slack = max(3, I // 10) if win == PB else I // 3   # sparse branches: shortest round within a third of the interval
                ok_ = [[o for o in range(I) if devf[j](o) <= min(devf[j](x) for x in range(I)) + slack] for j in (0, 1)]
                def rnd(oA, oB):
                    wB = (oB - (oA + rtA + 3)) % I + 3; wA = (oA - (oB + rtB + 3)) % I + 3
                    return rtA + wB + rtB + wA
                oA, oB = min(((a_, b_) for a_ in ok_[0] for b_ in ok_[1]), key=lambda x: (rnd(*x), devf[0](x[0]) + devf[1](x[1]), tot[0](x[0]) + tot[1](x[1])))
                for D, o, j in ((Ds[0], oA, 0), (Ds[1], oB, 1)):
                    fs_.append(dict(I=I, R=[o], first=D[0] if D else win[0], last=D[-1] if D else win[1], n=len(D), approx=devf[j](o), fitwin=list(win)))
                # slots without a real departure behind them count against a candidate (a pattern with more slots always has
                # one near every real trip: bus 56 Darkovičky, 2 trips in 2 h, came out every 30); 5 min per missing trip
                miss = sum(abs(len(f['R']) * (win[1] - win[0]) / I - len(D)) for f, D in zip(fs_, Ds))
                k_ = (max(f['approx'] for f in fs_) + 5 * miss, abs(r - per_h))
                cands_a.append(fs_)
                if best_a is None or k_ < best_a[0]: best_a = (k_, fs_)
            fits = best_a[1]
            # keep the other rate for the sheet, so the owner can choose it (e.g. hourly where the band is hourly)
            for j, f in enumerate(fits):
                o_ = next((c[j] for c in cands_a if c[j]['I'] != f['I']), None)
                if o_: f['alt'] = dict(every=o_['I'], real=o_['R'], set=loop_shift(o_['I'], o_['R'], loop), approx=o_['approx'])
        for x_, f in zip((p, q), fits):
            old = dict(every=x_['every'], real=x_['real'], first=x_['first'], last=x_['last'])
            x_.update(every=f['I'], real=f['R'], set=loop_shift(f['I'], f['R'], loop), first=f['first'], last=f['last'], n=f['n'])
            if 'approx' in f: x_['approx'] = f['approx']; x_['fitwin'] = f['fitwin']
            if 'alt' in f: x_['alt'] = f['alt']
            x_['refit'] = old if (old['every'], old['real']) != (f['I'], f['R']) else 'kept'
    for p in out:
        p.pop('deps', None)
        if p.get('refit') == 'kept': p.pop('refit')
    return out

def pattern_need(rows, rts, lays, t0=960):
    """Vehicles a Simutrans line needs to run the schedule pattern the sheet suggests (user rule, 20 Oct 2026: size every
    line from its suggested pattern). rows = the timed entries in running order, each dict(every, real) with real = the
    departure times mod every (from midnight); rts[i] = running time from entry i to the next entry (the last one back to
    the first); lays[i] = minimum wait before departing entry i. A vehicle leaving entry 0 at a slot in the hour from
    t0 - 30 is followed round, always taking the first slot of the next entry at least lays[i] after it arrives; the slots
    of entry 0 inside one round = vehicles. Worst case over the starting slots. Returns (vehicles, round in min, waits)."""
    def slots(row, lo, hi): return [t for t in range(lo, hi) if t % row['every'] in row['real']]
    best = None
    for s0 in slots(rows[0], t0 - 30, t0 - 30 + max(60, rows[0]['every'])):   # a whole interval: every-80/120 branches
        t = s0; waits = []
        for i in range(len(rows)):
            arr = t + rts[i]; nxt = rows[(i + 1) % len(rows)]; lay = lays[(i + 1) % len(rows)]
            t = next(x for x in range(arr + lay, arr + lay + nxt['every'] + 1) if x % nxt['every'] in nxt['real'])
            waits.append(t - arr)
        cyc = t - s0; n = len(slots(rows[0], s0, t))
        if best is None or (n, cyc) > best[:2]: best = (n, cyc, waits)
    return best

# ---------------------------------------------------------------- stop names: expand every abbreviation
def make_nm(cfg):
    exp = cfg['stop_name_expansions']; fixed = cfg.get('stop_name_fixed', {})
    strip = cfg.get('stop_name_strip_prefix')
    def nm(s):
        if strip and s.startswith(strip): s = s[len(strip):]
        s = fixed.get(s, s)
        if ',' in s and ', ' not in s: s = s.replace(',', ', ')
        for a, b in exp: s = s.replace(a, b)
        return s.replace('  ', ' ')
    return nm
