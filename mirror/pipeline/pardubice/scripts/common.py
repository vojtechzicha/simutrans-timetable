"""Shared helpers for the Pardubice pipeline (DPMP trolleybuses and buses; stdlib only).

The generic helpers are imported from the sister pipelines, so a fix there applies here too:
- ../ostrava/scripts/lib.py: seznam-autobusu parsers (parse_vypravenost, parse_fleet_list, next_page, record_date),
  the JDF reader and version rule (jdf_tables, jdf_trips, pick_version), trip chaining (blocks, active_at,
  min_turnaround), runfit (with the 28 Sep de-duplication fix) and loop_shift.
- ../ostrava-trolleybus/scripts/lib.py: cycle_need_peak (cycle_need that skips round trips waiting over max_wait).
- ../brno-trolleybus/scripts/common.py: mark_spares (the logged-surplus rule, user 29 Sep 2026).
- ../brno/scripts/sticky.py is not imported: the page uses the Brno bus sheet's bar (brno-trolleybus/assets/extra.css.html).
Only the paths, the state loading and polite HTTP live here.
"""
import collections, datetime, gzip, importlib.util, json, os, sys, time, urllib.request

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))    # pipeline/pardubice
PIPE = os.path.dirname(BASE)                                          # pipeline/
PROJECT = os.path.dirname(PIPE)                                       # project root (HTML output)
RAW = os.path.join(BASE, 'data', 'raw')
DER = os.path.join(BASE, 'data', 'derived')
ASSETS = os.path.join(BASE, 'assets')

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

tl = _load('ostrava_tramlib', os.path.join(PIPE, 'ostrava', 'scripts', 'lib.py'))
parse_vypravenost, parse_fleet_list, next_page, record_date = tl.parse_vypravenost, tl.parse_fleet_list, tl.next_page, tl.record_date
jdf_tables, jdf_trips, pick_version = tl.jdf_tables, tl.jdf_trips, tl.pick_version
blocks, active_at, min_turnaround = tl.blocks, tl.active_at, tl.min_turnaround
runfit, loop_shift, hm, hhmm = tl.runfit, tl.loop_shift, tl.hm, tl.hhmm
cycle_need_peak = _load('ostrava_trolleylib', os.path.join(PIPE, 'ostrava-trolleybus', 'scripts', 'lib.py')).cycle_need_peak
_bt = _load('brno_trolleybus_common', os.path.join(PIPE, 'brno-trolleybus', 'scripts', 'common.py'))
mark_spares = _bt.mark_spares
BRNO_STYLE = os.path.join(PIPE, 'brno', 'assets', 'style.css.html')
BRNO_EXTRA = os.path.join(PIPE, 'brno-trolleybus', 'assets', 'extra.css.html')

def load(path):
    with open(path, encoding='utf-8') as f: return json.load(f)

def save(obj, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f: json.dump(obj, f, ensure_ascii=False, indent=1)

def state(name):
    """Load states/<name>.json (name may include .json)."""
    p = os.path.join(BASE, 'states', name if name.endswith('.json') else name + '.json')
    s = load(p); s.setdefault('name', os.path.splitext(os.path.basename(p))[0]); return s

def der(S, name):
    return os.path.join(DER, S['name'], name)

def day(s): return datetime.date.fromisoformat(s)

# ---- polite HTTP ---------------------------------------------------------------------------------------
# seznam-autobusu.cz answers 403 to bare clients; a plain browser User-Agent with Accept / Accept-Language
# works. At most one request every 2 s (the brief allows about 1/s). No personal data in any header or URL.
UA = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
      'Chrome/140.0.0.0 Safari/537.36')
HEADERS = {'User-Agent': UA, 'Accept': 'text/html,application/xhtml+xml,*/*;q=0.8',
           'Accept-Language': 'cs-CZ,cs;q=0.9,en;q=0.8', 'Accept-Encoding': 'gzip'}

def fetch(url, dest=None, pause=2.0):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=180) as r:
        b = r.read()
        if r.headers.get('Content-Encoding') == 'gzip': b = gzip.decompress(b)
    if dest:
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, 'wb') as f: f.write(b)
    time.sleep(pause)
    return b

# ---- time helpers -----------------------------------------------------------------------------------------
mm = lambda m: ':%02d' % (m % 60)

# ---- JDF ----------------------------------------------------------------------------------------------------
class Folder:
    """Stand-in for the outer JDF.zip: DPMP's inner zips are stored one by one in data/raw/jdf/<date>/<kind>/."""
    def __init__(self, path): self.path = path
    def read(self, name): return open(os.path.join(self.path, name), 'rb').read()

def _t(s):
    if not s or not s[:1].isdigit() or len(s) < 4: return None
    return int(s[:2]) * 60 + int(s[2:4])

def jdf_trips(tables, d):
    """Trips of one JDF line version running on date d.
    Differs from the Ostrava tram lib's jdf_trips in two points: (1) the Zasspoje columns are found by row length,
    because DPMP's JDF 1.10 rows have 12 fields (km 8, arrival 9, departure 10), the 1.11 rows 15 (9, 10, 11) and
    1.8 rows 10 (7, 8, 9) - the tram lib reads 1.10 as 1.11; (2) Caskody type 1 ("runs in", DPMP's school-holiday
    trips) and type 3 ("runs only in") ranges both restrict the trip to those ranges, OR-ed - the tram lib ignores
    type 1 and lets the last type-3 range decide. Fixed codes of the trip are kept (codes), so school-day trips (those
    with "does not run" ranges in the school holidays) and low-floor marks stay visible."""
    zast = {r[0]: ','.join(x for x in r[1:4] if x) for r in tables['Zastavky']}
    pk = {r[0]: r[1] for r in tables['Pevnykod']}
    cas = collections.defaultdict(list)
    for r in tables['Caskody']: cas[r[1]].append(r)
    stops = collections.defaultdict(list)
    for r in tables['Zasspoje']:
        ia, idp = (10, 11) if len(r) >= 15 else (9, 10) if len(r) >= 12 else (8, 9)
        a = _t(r[ia]); dp = _t(r[idp]); t = dp if dp is not None else a
        if t is None: continue
        stops[r[1]].append((int(r[2]), zast[r[3]], a if a is not None else t, t))
    wd = str(d.isoweekday()); trips = []
    for r in tables['Spoje']:
        sp = r[1]; codes = [pk.get(c, '') for c in r[2:12] if c]
        dayc = [c for c in codes if c and c in 'X+1234567']
        ok = (not dayc) or ('X' in dayc and d.isoweekday() <= 5) or wd in dayc
        only = []; school = False
        for c in cas.get(sp, []):
            typ = c[4]
            od = datetime.datetime.strptime(c[5], '%d%m%Y').date()
            do = datetime.datetime.strptime(c[6], '%d%m%Y').date() if c[6] else od
            inr = od <= d <= do
            if typ == '4':
                if inr: ok = False
                if od.month in (7, 8) and do.month in (8, 9): school = True     # "does not run in the summer holidays"
            if typ in ('1', '3'): only.append(inr)     # 1 = runs (only) in, 3 = runs only in
            if typ == '2' and inr: ok = True
        if only and not any(only): ok = False
        if not ok or sp not in stops: continue
        st = sorted(stops[sp], key=lambda x: (x[3], x[0]))
        trips.append(dict(sp=int(sp), dep=st[0][3], arr=st[-1][2], fr=st[0][1], to=st[-1][1],
                          stops=[s[1] for s in st], times=[s[3] for s in st], codes=codes, school=school))
    return trips

def jdf_version_rows(folder):
    """[(inner zip name, Linky row)] of every inner zip in a folder."""
    import csv, io, zipfile
    out = []
    for n in sorted(os.listdir(folder)):
        inner = zipfile.ZipFile(os.path.join(folder, n))
        ln = [x for x in inner.namelist() if x.lower().startswith('linky')]
        for r in csv.reader(io.StringIO(inner.read(ln[0]).decode('cp1250').replace(';\r\n', '\n').replace(';\n', '\n'))):
            if r: out.append((n, r))
    return out
