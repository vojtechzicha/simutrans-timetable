"""Run the Ostrava bus pipeline.  python run.py [--fetch]
Without flags it rebuilds from data/raw/<snapshot>/ (no network). --fetch downloads the bus JDF (~107 MB), the registers and the
day records first. The live feed has no history: poll it with 01b_live_poll.py on the vehicle day itself."""
import os, subprocess, sys
here = os.path.dirname(os.path.abspath(__file__))
steps = []
if '--fetch' in sys.argv: steps += [['01_fetch.py'], ['01c_fetch_odis.py']]
steps += [['02_timetable.py'], ['03_fleet.py'], ['05_schedule.py'], ['04_roster.py'], ['07_odis.py'], ['06_render.py']]   # schedule first: needs are sized from it
for s in steps:
    print('==', ' '.join(s), flush=True)
    subprocess.run([sys.executable, os.path.join(here, s[0])] + s[1:], cwd=here, check=True)
