"""Shared helpers for the Brno bus pipeline (stdlib only).

Everything generic comes from the trolleybus pipeline (pipeline/brno-trolleybus/scripts/common.py), which in turn
takes fetch, GTFS, cycle_need and runfit from the tram pipeline (pipeline/brno). Only paths, state loading and
the bus route type are local.
"""
import importlib.util, os, sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # pipeline/brno-bus
PROJECT = os.path.dirname(os.path.dirname(BASE))
RAW = os.path.join(BASE, 'data', 'raw')
DER = os.path.join(BASE, 'data', 'derived')
ASSETS = os.path.join(BASE, 'assets')
PIPE = os.path.dirname(BASE)
TRAM = os.path.join(PIPE, 'brno')
TROLL = os.path.join(PIPE, 'brno-trolleybus')

_spec = importlib.util.spec_from_file_location('brno_trolleybus_common', os.path.join(TROLL, 'scripts', 'common.py'))
_c = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(_c)
for _n in ('fetch', 'mins', 'hm', 'mm', 'gtfs_trips', 'chain_at', 'cycle_need', 'runfit', 'runfit_rate', 'best_offset',
           'loop_shift', 'circuit_need', 'turnarounds', 'mark_spares', 'DIV60', 'DIV1440', 'ANY', 'load', 'save'):
    globals()[_n] = getattr(_c, _n)

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROUTE_TYPE = '3'     # IDS JMK GTFS: buses (trams 0, trolleybuses 800)

def state(name):
    p = os.path.join(BASE, 'states', name if name.endswith('.json') else name + '.json')
    s = load(p); s.setdefault('name', os.path.splitext(os.path.basename(p))[0]); return s

def gtfs_path(S):
    """Same IDS JMK feed as the tram and trolleybus sheets: data/raw/gtfs/<date>/ here, else pipeline/brno's."""
    own = os.path.join(RAW, 'gtfs', S['gtfs_date'], 'gtfs.zip')
    return own if os.path.exists(own) else os.path.join(TRAM, 'data', 'raw', 'gtfs', S['gtfs_date'], 'gtfs.zip')
