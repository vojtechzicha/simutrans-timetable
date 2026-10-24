"""Run the Havířov / Karviná / Orlová bus pipeline.  python run.py [--fetch]
Without flags it rebuilds from data/raw/<snapshot>/ (no network except 01d_plates.py for plates not yet looked up).
--fetch downloads the bus JDF (~107 MB), the register and every line's records first. The live feed has no history: poll it
with 01b_live_poll.py on the vehicle day itself (it runs detached, see README)."""
import os, subprocess, sys
here = os.path.dirname(os.path.abspath(__file__))
steps = []
if '--fetch' in sys.argv: steps += [['01_fetch.py']]
steps += [['02_timetable.py'], ['03_fleet.py'], ['01d_plates.py'], ['03_fleet.py'], ['05_schedule.py'], ['04_roster.py'], ['06_render.py']]   # schedule first: needs are sized from it
for s in steps:
    print('==', ' '.join(s), flush=True)
    subprocess.run([sys.executable, '-X', 'utf8', os.path.join(here, s[0])] + s[1:], cwd=here, check=True)
