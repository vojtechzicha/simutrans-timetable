"""Run the Ostrava pipeline.  python run.py [--fetch] [--history]
Without flags it rebuilds from data/raw/<snapshot>/ (no network). --fetch downloads JDF + fleet first,
--history also re-scrapes the vypravenost history (~10 min)."""
import os, subprocess, sys
here = os.path.dirname(os.path.abspath(__file__))
steps = []
if '--fetch' in sys.argv or '--history' in sys.argv:
    steps.append(['01_fetch.py', '--jdf', '--fleet'] + (['--history'] if '--history' in sys.argv else []))
steps += [['02_timetable.py'], ['03_fleet.py'], ['05_schedule.py'], ['04_roster.py'], ['04b_rebase.py'], ['06_render.py']]   # schedule first: needs are sized from it
for s in steps:
    print('==', ' '.join(s), flush=True)
    subprocess.run([sys.executable, os.path.join(here, s[0])] + s[1:], cwd=here, check=True)
