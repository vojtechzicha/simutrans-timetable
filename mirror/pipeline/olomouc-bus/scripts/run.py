"""Rebuild the Olomouc bus sheet from stored raw data.

  python run.py --state 2026-09-29            # 02_parse -> 03_timetable -> 04_fleet -> 05_render
  python run.py --state 2026-09-29 --fetch    # first download what is missing (day pages, histories, register, car pages)

The day overviews are fetched separately (01_fetch.py --overviews FROM TO) when choosing a new vehicle day.
"""
import argparse, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ap = argparse.ArgumentParser(); ap.add_argument('--state', required=True); ap.add_argument('--fetch', action='store_true')
a = ap.parse_args()
steps = []
if a.fetch:
    steps += [['01_fetch.py', '--day', '--history', '--register'], ['01_fetch.py', '--cars']]
steps += [['02_parse.py'], ['03_timetable.py'], ['04_fleet.py'], ['05_render.py']]
for st in steps:
    cmd = [sys.executable, os.path.join(HERE, st[0]), '--state', a.state] + st[1:]
    print('>>', ' '.join(st))
    r = subprocess.run(cmd, cwd=HERE)
    if r.returncode: sys.exit(r.returncode)
