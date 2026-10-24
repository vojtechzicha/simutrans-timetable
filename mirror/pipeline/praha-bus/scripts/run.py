"""Rebuild the Prague bus sheet for one state: python run.py --state 2026-09-29 [--fetch]

  --fetch    download missing raw files first (timetable, registers, deployment records, single car pages);
             the game export is not fetched: ask the save-game session for it (README)
Also refreshes assets/pak_objects.json from the pak checkout and writes data/derived/<state>/pak_request.json.
"""
import argparse, subprocess, sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
FETCH = [('01_fetch_sources.py', []), ('02_gtfs_lines.py', []), ('01_fetch_records.py', []), ('02_register.py', []), ('01_fetch_sources.py', ['--cars'])]
STEPS = [('00_pak_objects.py', None), ('02_gtfs_lines.py', []), ('02_register.py', []), ('03_compare.py', []), ('04_courses.py', []),
         ('05_render.py', []), ('06_pak_request.py', []), ('07_halt_renames.py', [])]

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--state', required=True); ap.add_argument('--fetch', action='store_true')
    a = ap.parse_args()
    for st, extra in (FETCH if a.fetch else []) + STEPS:
        cmd = [sys.executable, os.path.join(HERE, st)] + ([] if extra is None else ['--state', a.state] + extra)
        print('==', st, *(extra or []))
        r = subprocess.run(cmd, cwd=HERE, env=dict(os.environ, PYTHONIOENCODING='utf-8'))
        if r.returncode: sys.exit(r.returncode)

if __name__ == '__main__':
    main()
