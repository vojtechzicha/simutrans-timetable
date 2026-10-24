"""Rebuild the MD-CR sheet: python scripts/run.py [--fetch]

Since v3 (3 Oct 2026) MD-CR.html comes from 10_corridor.py, 11_design.py and 12_render.py.
v4 (same day) is the simplified clock-face design: 13_simple.py, then `python scripts/12_render.py v4` writes MD-CR.html.

--fetch downloads JR<year>.zip again into data/raw/jr<year>/ first (year from config service_day).
"""
import json, os, subprocess, sys, urllib.request
sys.stdout.reconfigure(encoding='utf-8')

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CFG = json.load(open(os.path.join(ROOT, 'config.json'), encoding='utf-8'))

if '--fetch' in sys.argv:
    y = CFG['service_day'][:4]
    d = os.path.join(ROOT, 'data', 'raw', 'jr' + y)
    os.makedirs(d, exist_ok=True)
    url = f'ftp://ftp.cisjr.cz/draha/celostatni/szdc/{y}/JR{y}.zip'
    print('fetch', url)
    urllib.request.urlretrieve(url, os.path.join(d, f'JR{y}.zip'))

for s in ('01_parse.py', '02_trips.py', '03_lines.py', '04_schedule.py', '05_render.py', '10_corridor.py', '11_design.py', '13_simple.py'):
    print('==', s)
    r = subprocess.run([sys.executable, os.path.join(HERE, s)], env=dict(os.environ, PYTHONIOENCODING='utf-8'),
                       capture_output=True, text=True, encoding='utf-8')
    if s == '04_schedule.py':
        open(os.path.join(ROOT, 'data', 'derived', '_schedule_summary.txt'), 'w', encoding='utf-8').write(r.stdout)
    print(r.stdout.strip().splitlines()[-1] if r.stdout.strip() else '')
    if r.returncode:
        print(r.stderr)
        sys.exit(r.returncode)

subprocess.run([sys.executable, os.path.join(HERE, '12_render.py'), 'v4'], env=dict(os.environ, PYTHONIOENCODING='utf-8'))
