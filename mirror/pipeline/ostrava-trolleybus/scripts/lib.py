"""Shared helpers for the Ostrava trolleybus pipeline (stdlib only).

Reuses the Ostrava tram pipeline's helpers (../../ostrava/scripts/lib.py): the seznam-autobusu parsers and WAF
headers, the JDF reader and version rule, trip chaining, cycle_need, runfit, loop_shift, plans and make_nm.
Only the paths and the config are this folder's own, so a fix to runfit or cycle_need there applies here too.
"""
import importlib.util, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))          # pipeline/ostrava-trolleybus
PROJECT = os.path.dirname(os.path.dirname(ROOT))                             # Simutrans-Timetable
_spec = importlib.util.spec_from_file_location('tramlib', os.path.join(os.path.dirname(ROOT), 'ostrava', 'scripts', 'lib.py'))
tramlib = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(tramlib)

HEADERS = tramlib.HEADERS
http, parse_vypravenost, parse_fleet_list, next_page, record_date = tramlib.http, tramlib.parse_vypravenost, tramlib.parse_fleet_list, tramlib.next_page, tramlib.record_date
jdf_open, jdf_tables, jdf_versions, pick_version, jdf_trips = tramlib.jdf_open, tramlib.jdf_tables, tramlib.jdf_versions, tramlib.pick_version, tramlib.jdf_trips
blocks, active_at, min_turnaround, cycle_need = tramlib.blocks, tramlib.active_at, tramlib.min_turnaround, tramlib.cycle_need
runfit, loop_shift, plans, make_nm, hm, hhmm, day = tramlib.runfit, tramlib.loop_shift, tramlib.plans, tramlib.make_nm, tramlib.hm, tramlib.hhmm, tramlib.day

_bs = importlib.util.spec_from_file_location('brnotrolleylib', os.path.join(os.path.dirname(ROOT), 'brno-trolleybus', 'scripts', 'common.py'))
_bl = importlib.util.module_from_spec(_bs); _bs.loader.exec_module(_bl)
mark_spares = _bl.mark_spares          # logged-surplus rule (user, 29 Sep 2026), Brno's reference implementation

CONFIG = json.load(open(os.path.join(ROOT, 'config.json'), encoding='utf-8'))
RAW = os.path.join(ROOT, 'data', 'raw', CONFIG['snapshot'])
DERIVED = os.path.join(ROOT, 'data', 'derived')
os.makedirs(DERIVED, exist_ok=True)

def dpath(name): return os.path.join(DERIVED, name)
def save(name, obj): json.dump(obj, open(dpath(name), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
def load(name): return json.load(open(dpath(name), encoding='utf-8'))

def cycle_need_peak(trips, a, b, t0=960, lay=3, max_wait=30):
    """cycle_need (tram lib) restricted to round trips that stay on the branch: a start is skipped when the
    tram would wait more than max_wait min at either terminus for its next trip. Such a wait means the branch's
    return trips have ended and the vehicles leave as another line. On DPO trolleybuses, 107 to Hranečník
    continues as line 101 from 16:33. Otherwise identical to cycle_need."""
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
