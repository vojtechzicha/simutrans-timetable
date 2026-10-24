"""Run the Plzeň pipeline for one state.

  python run.py --state 2026-09-27            rebuild from stored raw data
  python run.py --state 2026-09-27 --fetch    download fresh day overviews, vypravenost, register and GTFS
                                              first (then point the state's dates at the new folders)
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
    days = [(today - datetime.timedelta(d)).isoformat() for d in range(1, 11)]
    run('01_fetch.py', '--days', *days, '--vehicles', S['vehicles_date'], '--register', '--gtfs')
    run('02_parse.py', '--days')
    print('Fetched. Pick the vehicle day from data/derived/day_counts.json (latest complete Friday), set vehicles_date,')
    print("register_date and gtfs_date in the state file, fetch that day's lists with 01_fetch.py --vehicles, and run again.")
    sys.exit(0)
run('02_parse.py', '--vehicles', S['vehicles_date'], '--register', S['register_date'])
run('03_timetable.py', '--state', S['name'])
run('04_fleet.py', '--state', S['name'])
run('05_render.py', '--state', S['name'])
