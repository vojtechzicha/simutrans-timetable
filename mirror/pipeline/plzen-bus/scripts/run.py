"""Run the Plzeň bus pipeline for one state.

  python run.py --state 2026-09-29            rebuild from stored raw data
  python run.py --state 2026-09-29 --fetch    download fresh data first (into ../../plzen-trolleybus/data/raw, shared)

The scripts and the raw data live in the Plzeň trolleybus pipeline (../../plzen-trolleybus): the PMDP GTFS, the
seznam-autobusu.cz day overviews, per-line lists, line histories and the PMDP register are stored there once for
both sheets. This folder holds the bus state (states/), the derived data (data/derived/), the pak map
(assets/pak_map.json), pak_request.md and the README. Every script runs with --base <this folder>.
"""
import argparse, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
TB = os.path.join(os.path.dirname(BASE), 'plzen-trolleybus', 'scripts')          # ../../plzen-trolleybus/scripts
p = argparse.ArgumentParser(); p.add_argument('--state', required=True); p.add_argument('--fetch', action='store_true')
a = p.parse_args()
S = json.load(open(os.path.join(BASE, 'states', a.state + '.json'), encoding='utf-8'))
def run(*args):
    print('>', ' '.join(args)); subprocess.run([sys.executable, os.path.join(TB, args[0]), *args[1:]], check=True, cwd=TB)
if a.fetch:
    run('01_fetch.py', '--vehicles', S['vehicles_date'], '--lines', *sorted({sl['records'] for sl in S['simutrans_lines']}))
    run('01_fetch.py', '--register', 'trolejbus', 'autobus')
    print('Fetched into ../../plzen-trolleybus/data/raw. For the GTFS and day overviews use the trolleybus run.py --fetch. '
          'Set the state dates, then run again without --fetch.')
    sys.exit(0)
run('02_parse.py', '--vehicles', S['vehicles_date'], '--register', S['register_date'], '--history')
for s in ('03_timetable.py', '04_fleet.py', '04b_pak.py', '05_render.py'):
    run(s, '--state', a.state, '--base', BASE)
