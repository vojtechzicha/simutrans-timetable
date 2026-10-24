"""Rebuild the Prague sheet for one state: python run.py --state 2026-09-27 [--fetch] [--refresh]

  --fetch    run 01_fetch.py first (downloads only missing raw files)
  --refresh  with --fetch: download everything again (new dated folders are better: see README)
"""
import argparse, subprocess, sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
STEPS = ['02_parse.py', '03_timetable.py', '03c_nad.py', '04_courses.py', '05_render.py']

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--state', required=True)
    ap.add_argument('--fetch', action='store_true'); ap.add_argument('--refresh', action='store_true')
    a = ap.parse_args()
    steps = (['01_fetch.py'] if a.fetch else []) + STEPS
    import json
    st = json.load(open(os.path.join(HERE, '..', 'states', a.state + '.json'), encoding='utf-8'))
    if st.get('changes'):   # change state: carry the base state's trams over instead of re-rostering (04b_rebase.py)
        steps = [x if x != '04_courses.py' else '04b_rebase.py' for x in steps]
    for st in steps:
        cmd = [sys.executable, os.path.join(HERE, st), '--state', a.state] + (['--refresh'] if st == '01_fetch.py' and a.refresh else [])
        print('==', st)
        r = subprocess.run(cmd, cwd=HERE, env=dict(os.environ, PYTHONIOENCODING='utf-8'))
        if r.returncode: sys.exit(r.returncode)

if __name__ == '__main__':
    main()
