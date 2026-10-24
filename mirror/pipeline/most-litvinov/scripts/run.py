"""Run the Most–Litvínov pipeline.  python run.py [--fetch]
Without flags it rebuilds from data/raw/<snapshot>/ (no network). --fetch downloads JDF, fleet and one
live poll first. There is no allocation history for DPmML, so the roster is config.roster."""
import os, subprocess, sys
here = os.path.dirname(os.path.abspath(__file__))
steps = []
if '--fetch' in sys.argv:
    steps.append(['01_fetch.py'])
steps += [['02_timetable.py'], ['03_fleet.py'], ['04_roster.py'], ['05_schedule.py'], ['06_render.py']]
for s in steps:
    print('==', ' '.join(s), flush=True)
    subprocess.run([sys.executable, os.path.join(here, s[0])] + s[1:], cwd=here, check=True)
