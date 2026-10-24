"""Shared helpers for the ODIS regional lines of Havířovsko, Karvinsko and Orlovsko (stdlib only).

Rule-bearing code is imported, not copied (pipeline README):
- ../../ostrava/scripts/lib.py (tram lib): JDF reader and version rule, loop_shift, pattern_need, make_nm, hm;
- ../../ostrava-bus/scripts/lib.py: line_anchor (the line's own afternoon peak);
- ../../brno-trolleybus/scripts/common.py: mark_spares.
The schedule method is ../bus-schedule-method.md (v3): every line here is a regional line, so every line is read over the
whole day at its core points and set by hand in config.json -> lines.
"""
import importlib.util, json, os, re, sys

HOME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))          # pipeline/odis-regional-hko: the scripts and templates
PIPE = os.path.dirname(HOME)
def _base():
    """the sheet folder: this one, or another sheet's given as --base <folder> (or ODIS_BASE), which keeps its own config.json
    and data/ and runs these scripts (as plzen-bus runs the plzen-trolleybus scripts)"""
    a = sys.argv
    if '--base' in a:
        i = a.index('--base'); b = a[i + 1]; del a[i:i + 2]
        return os.path.abspath(b if os.path.isabs(b) else os.path.join(PIPE, b))
    return os.path.abspath(os.environ['ODIS_BASE']) if os.environ.get('ODIS_BASE') else HOME
ROOT = _base()
PROJECT = os.path.dirname(PIPE)
def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
tramlib = _load('tramlib', os.path.join(PIPE, 'ostrava', 'scripts', 'lib.py'))
buslib = _load('ostravabuslib', os.path.join(PIPE, 'ostrava-bus', 'scripts', 'lib.py'))

jdf_open, jdf_tables, pick_version, jdf_trips = tramlib.jdf_open, tramlib.jdf_tables, tramlib.pick_version, tramlib.jdf_trips
loop_shift, pattern_need, make_nm, hm, day = tramlib.loop_shift, tramlib.pattern_need, tramlib.make_nm, tramlib.hm, tramlib.day
line_anchor = buslib.line_anchor
mark_spares = _load('brnotrolleylib', os.path.join(PIPE, 'brno-trolleybus', 'scripts', 'common.py')).mark_spares

CONFIG = json.load(open(os.path.join(ROOT, 'config.json'), encoding='utf-8'))
RAW = os.path.join(ROOT, 'data', 'raw', CONFIG['snapshot'])
DERIVED = os.path.join(ROOT, 'data', 'derived')
os.makedirs(DERIVED, exist_ok=True)
def rel(p): return os.path.normpath(os.path.join(ROOT, p))

def dpath(name): return os.path.join(DERIVED, name)
def save(name, obj): json.dump(obj, open(dpath(name), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
def load(name): return json.load(open(dpath(name), encoding='utf-8'))

_nm = make_nm(CONFIG)
def nm(s):
    """a JDF stop name with its town kept (regional lines cross towns) and every abbreviation expanded"""
    s = re.sub(r',\s*,', ',', s)
    return re.sub(r'\s+', ' ', _nm(s)).replace(' ,', ',').strip()
def AL(s): return CONFIG['terminus_alias'].get(s, s)

def area_of(code, ic=None):
    """contract area (or town network) of a licence: config.areas prefix, and the area's operator (ic, default jdf.operator_ic)"""
    return next((a for a in CONFIG['areas'] if code.startswith(a['prefix']) and (ic is None or ic == a.get('ic', CONFIG['jdf']['operator_ic']))), None)

def plate_key(s): return re.sub(r'\s', '', s or '').upper()
def tlen(ty):
    # a bus's length from its register type (01c_fleet for the registers, 04_roster for looked-up plates): "Urbanway 10,5M",
    # "Crossway LE CITY 12M", and SOR's "CN 10,5", "BN 9,5", "C 12", "ICNG 12,3", "NBG 18" (no M); 12 m when it says none
    m = (re.search(r'(\d+)[,.](\d)\s*M', ty or '') or re.search(r'\b(\d{2})M\b', ty or '')
         or re.search(r'\bSOR\s+[A-Z]+\s+(\d{1,2})(?:,(\d))?\b', ty or ''))
    if 'Dekstra' in (ty or '') or 'Midi' in (ty or ''): return 'midibus'
    return (f"{m.group(1)}.{m.group(2)} m" if m.lastindex == 2 and m.group(2) else f"{m.group(1)} m") if m else '12 m'
def tmin(s):
    if isinstance(s, int): return s
    h, m = s.split(':'); return int(h) * 60 + int(m)
