"""Run the Most–Litvínov bus pipeline.  python run.py [--fetch]
Without flags it rebuilds from data/raw/ (no network). --fetch downloads the register, the records, the car pages and
the dpmost.cz pages first, then (after 03_fleet.py has listed the photos) the newest photos of every city bus.
The timetables are read from the JDF zips named in config.jdf (see 01_fetch.py --jdf to store a fresh copy here).
New photos need their line read by eye into assets/photo_lines.json before 04_roster.py can use them."""
import os, subprocess, sys
here = os.path.dirname(os.path.abspath(__file__))
def run(*a):
    print('==', ' '.join(a), flush=True)
    subprocess.run([sys.executable, os.path.join(here, a[0])] + list(a[1:]), cwd=here, check=True)
if '--fetch' in sys.argv:
    run('01_fetch.py', '--fleet', '--records', '--cars', '--operator')
run('02_timetable.py'); run('03_fleet.py')
if '--fetch' in sys.argv:
    run('01_fetch.py', '--photos'); run('03_fleet.py')
for s in ('04_needs.py', '04_roster.py', '05_schedule.py', '06_render.py'): run(s)
