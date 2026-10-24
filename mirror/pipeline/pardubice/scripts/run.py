"""Rebuild the Pardubice sheet from the stored raw data (no network unless --fetch).

  python run.py --state 2026-09-29            # timetable, network, fleet, page, pak request
  python run.py --state 2026-09-29 --fetch    # first download whatever raw data is missing (01_fetch.py)
  python run.py --state 2026-09-29 --pak      # also re-read the pak checkout (00_pak_objects.py)
"""
import argparse, os, subprocess, sys

ap = argparse.ArgumentParser(); ap.add_argument('--state', required=True)
ap.add_argument('--fetch', action='store_true'); ap.add_argument('--pak', action='store_true')
a = ap.parse_args()
here = os.path.dirname(os.path.abspath(__file__))
steps = (['00_pak_objects.py'] if a.pak else []) + (['01_fetch.py'] if a.fetch else []) + \
        ['02_timetable.py', '03_network.py', '04_fleet.py', '05_render.py', '06_pak_request.py']
for s in steps:
    args = [sys.executable, os.path.join(here, s)] + ([] if s == '00_pak_objects.py' else ['--state', a.state])
    print('==', s, flush=True)
    r = subprocess.run(args, cwd=here)
    if r.returncode: sys.exit(r.returncode)
