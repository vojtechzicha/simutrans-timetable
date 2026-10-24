"""Shared helpers for the Most–Litvínov bus pipeline (stdlib only).

Reuses, read-only, the Most–Litvínov tram pipeline's helpers (../../most-litvinov/scripts/lib.py: WAF headers, the
seznam-autobusu parsers, the JDF reader that handles JDF 1.11, the version rule, blocks, cycle_need, runfit, plans,
make_nm), the Ostrava trolleybus pipeline's cycle_need_peak (../../ostrava-trolleybus/scripts/lib.py) and mark_spares
from ../../brno-trolleybus/scripts/common.py. Only the paths and the config are this folder's own. Nothing here writes
into those folders: the tram lib only reads its own config when imported.
"""
import importlib.util, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))          # pipeline/most-litvinov-bus
PROJECT = os.path.dirname(os.path.dirname(ROOT))                             # Simutrans-Timetable
PIPE = os.path.dirname(ROOT)
def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
tramlib = _load('mltramlib', os.path.join(PIPE, 'most-litvinov', 'scripts', 'lib.py'))
trolleylib = _load('otrolleylib', os.path.join(PIPE, 'ostrava-trolleybus', 'scripts', 'lib.py'))
mark_spares = _load('brnotrolleylib', os.path.join(PIPE, 'brno-trolleybus', 'scripts', 'common.py')).mark_spares

HEADERS = tramlib.HEADERS
http, parse_vypravenost, parse_fleet_list, next_page, record_date, clean = tramlib.http, tramlib.parse_vypravenost, tramlib.parse_fleet_list, tramlib.next_page, tramlib.record_date, tramlib._clean
jdf_open, jdf_tables, jdf_versions, pick_version, jdf_trips = tramlib.jdf_open, tramlib.jdf_tables, tramlib.jdf_versions, tramlib.pick_version, tramlib.jdf_trips
blocks, active_at, min_turnaround, cycle_need = tramlib.blocks, tramlib.active_at, tramlib.min_turnaround, tramlib.cycle_need
runfit, loop_shift, plans, make_nm, hm, hhmm, day = tramlib.runfit, tramlib.loop_shift, tramlib.plans, tramlib.make_nm, tramlib.hm, tramlib.hhmm, tramlib.day
cycle_need_peak = trolleylib.cycle_need_peak

CONFIG = json.load(open(os.path.join(ROOT, 'config.json'), encoding='utf-8'))
RAWROOT = os.path.join(ROOT, 'data', 'raw')
def raw(kind, date=None):
    """data/raw/<kind>/<date>/ (date defaults to config.snapshot)"""
    p = os.path.join(RAWROOT, kind, date or CONFIG['snapshot']); os.makedirs(p, exist_ok=True); return p
def src(path):
    """a path in config, relative to this pipeline folder"""
    return os.path.normpath(os.path.join(ROOT, path))
DERIVED = os.path.join(ROOT, 'data', 'derived')
os.makedirs(DERIVED, exist_ok=True)

def dpath(name): return os.path.join(DERIVED, name)
def save(name, obj): json.dump(obj, open(dpath(name), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
def load(name): return json.load(open(dpath(name), encoding='utf-8'))
def asset(name): return json.load(open(os.path.join(ROOT, 'assets', name), encoding='utf-8'))
