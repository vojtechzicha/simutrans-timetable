"""Shared helpers for the Plzeň trolleybus pipeline (stdlib only).

Generic helpers are imported, never copied:
- from the Plzeň tram pipeline (pipeline/plzen/scripts/common.py, read only; maintained by another session):
  fetch (browser headers, 2 s pause), GTFS reader, cycle_need, runfit, loop_shift;
- from the Brno trolleybus pipeline (pipeline/brno-trolleybus/scripts/common.py): circuit_need, turnarounds,
  runfit_rate and mark_spares (the user's "not needed" rule).
The Plzeň bus pipeline (pipeline/plzen-bus) imports this file in turn, and reads the raw data stored here.
"""
import collections, datetime, glob, html, importlib.util, json, os, re, sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # pipeline/plzen-trolleybus
PIPE = os.path.dirname(BASE)
PROJECT = os.path.dirname(PIPE)                                         # project root (HTML outputs)
RAW = os.path.join(BASE, 'data', 'raw')
DER = os.path.join(BASE, 'data', 'derived')
ASSETS = os.path.join(BASE, 'assets')
TRAM = os.path.join(PIPE, 'plzen')
BRNO_TB = os.path.join(PIPE, 'brno-trolleybus')

def _imp(name, path):
    sp = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
_t = _imp('plzen_tram_common', os.path.join(TRAM, 'scripts', 'common.py'))
_b = _imp('brno_trolleybus_common', os.path.join(BRNO_TB, 'scripts', 'common.py'))
fetch, mins, hm, mm, load, save = _t.fetch, _t.mins, _t.hm, _t.mm, _t.load, _t.save
gtfs_trips, chain_at, cycle_need, runfit, best_offset, loop_shift = _t.gtfs_trips, _t.chain_at, _t.cycle_need, _t.runfit, _t.best_offset, _t.loop_shift
DIV60, DIV1440, ANY = _t.DIV60, _t.DIV1440, _t.ANY
circuit_need, turnarounds, runfit_rate, mark_spares = _b.circuit_need, _b.turnarounds, _b.runfit_rate, _b.mark_spares

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

SA = 'https://seznam-autobusu.cz'
SLUG = 'mhd-plzen'
PMDP = 71                       # seznam-autobusu operator id of PMDP
ROUTE_TYPE = '11'               # PMDP GTFS: trolleybus 11, bus 3, tram 0

def state(name, base=BASE):
    p = os.path.join(base, 'states', name if name.endswith('.json') else name + '.json')
    s = load(p); s.setdefault('name', os.path.splitext(os.path.basename(p))[0]); return s

def gtfs_path(S):
    """PMDP GTFS stored here (data/raw/gtfs/<date>/gtfs.zip); the bus pipeline reads the same file."""
    return os.path.join(RAW, 'gtfs', S['gtfs_date'], 'gtfs.zip')

txt = lambda s: re.sub(r'\s+', ' ', html.unescape(re.sub(r'<!--.*?-->|<[^>]+>', '', s, flags=re.S))).strip()

# ---- seznam-autobusu.cz pages ------------------------------------------------------------------------
def parse_overview(path):
    """Day overview -> {(kind, line): [(kurz, [car ids], [numbers])]}, kind = trolden/busden/tramden/busnoc."""
    s = open(path, encoding='utf-8', errors='replace').read(); out = {}
    for block in re.split(r'<div class="route-data">', s)[1:]:
        m = re.search(r'<span class="route (\w+)">.*?linka=([^"&]+)"', block, re.S)
        if not m: continue
        items = []
        for it in re.findall(r'<span class="item">(.*?)</span>\s*(?=<span class="item">|</div>)', block, re.S):
            k = re.search(r'<span class="course">([^<]*)</span>', it)
            cars = re.findall(r'class="context-box" href="https://seznam-autobusu.cz/vuz/(\d+)/vypravenost">([^<]+)</a>', it)
            items.append((k.group(1).strip() if k else '', [c for c, _ in cars], [n for _, n in cars]))
        out[(m.group(1), html.unescape(m.group(2)))] = items
    return out

def busy_ids(path):
    """Every car id out anywhere on a day overview (for the "not out that day" check of designed cars)."""
    return set(re.findall(r'/vuz/(\d+)/vypravenost', open(path, encoding='utf-8', errors='replace').read()))

def parse_vypis(path):
    """Per-line list (vypis?datum=..&linka=N, or the history form vypis?linka=N&...): rows with date, line, kurz,
    car numbers, car ids and note."""
    s = open(path, encoding='utf-8', errors='replace').read(); out = []
    for r in re.findall(r'<tr[^>]*>(.*?)</tr>', s, re.S):
        cars = re.findall(r'class="context-box" href="https://seznam-autobusu.cz/vuz/(\d+)/vypravenost">([^<]+)</a>', r)
        if not cars: continue
        cell = {c.split()[0]: txt(v) for c, v in re.findall(r'<td[^>]*class="([^"]*)"[^>]*>(.*?)</td>', r, re.S)}
        d = re.search(r'(\d{1,2})\.\s*(\d{1,2})\.\s*(\d{4})', cell.get('date', ''))
        out.append(dict(date=f'{d.group(3)}-{int(d.group(2)):02d}-{int(d.group(1)):02d}' if d else '',
                        line=cell.get('route', ''), kurz=cell.get('order-on-line', ''), cars=[n for _, n in cars],
                        ids=[i for i, _ in cars], note=cell.get('note', ''), cells=cell))
    return out

def parse_register(folder, pattern='*.html'):
    """seznam?iddopravce=..&trakce=.. listing pages -> {car id: {num, type, livery, garage, state, operator, year}}."""
    reg = {}
    for fn in sorted(glob.glob(os.path.join(folder, pattern))):
        s = open(fn, encoding='utf-8', errors='replace').read(); groups = {}
        for cls, cid, body in re.findall(r'<tr class="car-line ([^"]*)"[^>]*data-car-id="(\d+)"[^>]*>(.*?)</tr>', s, re.S):
            g = groups.setdefault(cid, {'cls': cls, 'html': ''}); g['html'] += body
        for cid, g in groups.items():
            b = g['html']
            cell = {}
            for c, v in re.findall(r'<td[^>]*class=["\']([^"\']*)["\'][^>]*>(.*?)</td>', b, re.S):
                cell.setdefault(c.split()[-1] if c.startswith('no-mobile') or c.startswith('font085') else c.split()[0], v)
            num = re.search(r'class="[^"]*number"><!--\s*-->([^<]+)(?:<sup>[IVX]+</sup>)?<!--', b)   # 634<sup>II</sup>: the second 634
            paint = re.search(r'<span class="paint"><span class="label">[^<]*</span>(.*?)</span>', b, re.S)
            op = re.search(r"<td class='current-operator'[^>]*>\s*<b>(.*?)</b>", b, re.S)
            yr = re.search(r'<td class="font085">(\d{4})', b)
            reg[cid] = dict(num=num.group(1).strip() if num else None, type=txt(cell.get('manufacturer-type', '')),
                            livery=txt(paint.group(1)).replace('*', '').strip() if paint else '',
                            garage=txt(cell.get('depots', '')).rstrip('*').strip(), operator=txt(op.group(1)) if op else '',
                            year=yr.group(1) if yr else '', state=g['cls'].split()[0], file=os.path.basename(fn))
    return reg

def nice(d):
    d = d.replace('-', ''); x = datetime.date(int(d[:4]), int(d[4:6]), int(d[6:]))
    return f"{x.strftime('%a')} {x.day} {x.strftime('%b')} {x.year}"
