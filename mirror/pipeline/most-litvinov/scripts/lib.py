"""Shared helpers for the Most–Litvínov tram pipeline (stdlib only; same as pipeline/ostrava/scripts/lib.py)."""
import collections, csv, datetime, gzip, html, io, json, os, re, time, urllib.request, zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))          # pipeline/most-litvinov
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
                        kurz=cell('order-on-line'), note=cell('note'), by=cell('authors')))
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
    """trips running on date d. Handles JDF 1.8 (times at idx 8/9) and 1.11 (idx 10/11)."""
    ver = tables['VerzeJDF'][0][0] if tables['VerzeJDF'] else '1.8'
    ia, idp = (10, 11) if ver.startswith('1.1') and ver != '1.1' else (8, 9)
    zast = {r[0]: ','.join(x for x in r[1:4] if x) for r in tables['Zastavky']}
    pk = {r[0]: r[1] for r in tables['Pevnykod']}
    cas = collections.defaultdict(list)
    for r in tables['Caskody']: cas[r[1]].append(r)
    stops = collections.defaultdict(list)
    for r in tables['Zasspoje']:
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
        for c in cas.get(sp, []):
            typ = c[4]
            od = datetime.datetime.strptime(c[5], '%d%m%Y').date()
            do = datetime.datetime.strptime(c[6], '%d%m%Y').date() if c[6] else od
            inr = od <= d <= do
            if typ == '4' and inr: ok = False
            if typ == '3': ok = inr
            if typ == '2' and inr: ok = True
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

def runfit(deps, core=(930, 990), lo=780, hi=1200, divs=DIV1440):
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
    if not cands: return None
    if any(c['core'] for c in cands): cands = [c for c in cands if c['core']]
    mx = max(c['n'] for c in cands)
    ok = [c for c in cands if c['n'] >= 0.8 * mx]
    return min(ok, key=lambda c: (len(c['R']), c['I'], -c['n']))

def loop_shift(I, R, loop=True):
    """loop terminus (smyčka): enter every departure 1 min before the timetable minute"""
    return sorted((r - 1) % I for r in R) if loop else list(R)

def plans(trips, nm, fitcfg, pullin_dests, loop=True):
    """per (from,to) branch of one line. fitcfg = dict(window=[a,b], core=[c0,c1], lo, hi).
    Branches with <3 trips in the window, or listed as pull-ins, are not scheduled; their minutes are
    merged into the main branch from the same terminus."""
    a0, b0 = fitcfg['window']
    g = collections.defaultdict(list)
    for t in trips: g[(nm(t['fr']), nm(t['to']))].append(t['dep'])
    pk = lambda d: sum(1 for x in d if a0 <= x < b0)
    small = lambda k: pk(g[k]) < 3 or k[1] in pullin_dests
    out = []
    for (fr, to), d in sorted(g.items(), key=lambda x: -len(x[1])):
        if pk(d) == 0: continue
        if small((fr, to)):
            sib = [k for k in g if k[0] == fr and k != (fr, to) and not small(k)]
            out.append(dict(fr=fr, to=to, every=None, single=[x for x in d if a0 <= x < b0], into=sib[0][1] if sib else None)); continue
        extra = [x for k, dd in g.items() if k[0] == fr and k != (fr, to) and pk(dd) > 0 and small(k) for x in dd if a0 <= x < b0]
        f = runfit(d + extra, tuple(fitcfg['core']), fitcfg['lo'], fitcfg['hi'])
        out.append(dict(fr=fr, to=to, every=f['I'], real=f['R'], set=loop_shift(f['I'], f['R'], loop),
                        first=f['first'], last=f['last'], n=f['n'], merged=extra))
    return out

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
