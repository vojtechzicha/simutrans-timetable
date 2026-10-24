"""Run the Plzeň trolleybus pipeline for one state.

  python run.py --state 2026-09-29            rebuild from stored raw data
  python run.py --state 2026-09-29 --fetch    download the day overviews of the last two weeks, the per-line lists of
                                              the state's vehicle day, the register, the GTFS and the OSM wire first
                                              (dated today; point the state's dates at the new folders, then run again)
The Plzeň bus sheet (pipeline/plzen-bus) runs the same scripts with --base ../../plzen-bus.
"""
import argparse, datetime, os, subprocess, sys
from common import state

p = argparse.ArgumentParser(); p.add_argument('--state', required=True); p.add_argument('--fetch', action='store_true')
a = p.parse_args(); S = state(a.state)
here = os.path.dirname(os.path.abspath(__file__))
def run(*args):
    print('>', ' '.join(args)); subprocess.run([sys.executable, os.path.join(here, args[0]), *args[1:]], check=True, cwd=here)
if a.fetch:
    today = datetime.date.today()
    days = [(today - datetime.timedelta(days=i)).isoformat() for i in range(14, -1, -1) if (today - datetime.timedelta(days=i)).weekday() < 5]
    run('01_fetch.py', '--days', *days)
    run('01_fetch.py', '--vehicles', S['vehicles_date'], '--lines', *sorted({sl['records'] for sl in S['simutrans_lines']} | set(S['fleet'].get('secondary', []))))
    run('01_fetch.py', '--register', 'trolejbus', 'autobus', '--gtfs', '--osm')
    run('02_parse.py', '--days')
    print('Fetched. Pick the vehicle day from data/derived/day_counts.json, set the state dates, then run without --fetch.')
    sys.exit(0)
run('02_parse.py', '--vehicles', S['vehicles_date'], '--register', S['register_date'], '--days', '--history')
run('03_timetable.py', '--state', S['name'])
run('03b_offwire.py', '--state', S['name'])
run('04_fleet.py', '--state', S['name'])
run('04b_pak.py', '--state', S['name'])
run('05_render.py', '--state', S['name'])
