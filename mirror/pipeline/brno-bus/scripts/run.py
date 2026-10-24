"""Run the Brno bus pipeline for one state.

  python run.py --state 2026-09-29            rebuild from stored raw data
  python run.py --state 2026-09-29 --fetch    download fresh vypravenost and register first
                                              (then point the state's dates at the new folders)
"""
import argparse, os, subprocess, sys
from common import state

p = argparse.ArgumentParser(); p.add_argument('--state', required=True); p.add_argument('--fetch', action='store_true')
a = p.parse_args(); S = state(a.state)
here = os.path.dirname(os.path.abspath(__file__))
def run(*args):
    print('>', ' '.join(args)); subprocess.run([sys.executable, os.path.join(here, args[0]), *args[1:]], check=True, cwd=here)
if a.fetch:
    run('01_fetch.py', '--vehicles', S['vehicles_date'], '--register', '--external', S['vehicles_date'])
    print('Fetched. The GTFS is shared with pipeline/brno '
          '(its 01_fetch.py --gtfs). Point the state dates at the new folders, then run again without --fetch.')
    sys.exit(0)
run('02_parse.py', '--vehicles', S['vehicles_date'], '--register', S['register_date'])
run('03_timetable.py', '--state', S['name'])
run('04_fleet.py', '--state', S['name'])
run('05_render.py', '--state', S['name'])
