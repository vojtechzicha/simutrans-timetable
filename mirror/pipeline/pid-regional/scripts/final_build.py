"""The evening build after a poll day: wait until the given time, then rebuild the readings (bus chains), the buses of every
sheet, the game checks, every page and the index, and the 317 / 318 extracts for the Prague bus session.
usage: python final_build.py 20:02 2026-11-02"""
import datetime, subprocess, sys, time, os
HERE = os.path.dirname(os.path.abspath(__file__))
hh, mm = map(int, sys.argv[1].split(':')); day = sys.argv[2]
t = datetime.datetime.now().replace(hour=hh, minute=mm, second=0)
while datetime.datetime.now() < t: time.sleep(30)
OB = ['benesovsko', 'berounsko', 'kladensko', 'kolinsko', 'kutnohorsko', 'melnicko', 'mladoboleslavsko', 'nymbursko', 'praha-vychod',
      'praha-zapad', 'pribramsko', 'rakovnicko']
def run(*a):
    r = subprocess.run([sys.executable, '-X', 'utf8'] + list(a), cwd=HERE, capture_output=True, text=True, encoding='utf-8')
    if r.returncode: print('FAILED', a, r.stderr[-1500:], flush=True)
    return r.stdout
for o in OB: run('00_config.py', o, '--final'); run('03_read.py', o)
print(run('04_vehicles.py')[-2500:], flush=True)
for o in OB:
    run('05b_game.py', o); print(run('06_render.py', o).strip()[-200:], flush=True)
print(run('07_index.py').strip(), flush=True)
for L in ('317', '318'): print(run('observed.py', L, day).strip()[-600:], flush=True)
print('done', datetime.datetime.now().strftime('%H:%M'))
