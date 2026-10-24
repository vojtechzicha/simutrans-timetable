"""Rebuild an ODIS regional sheet from the stored raw data: python scripts/run.py [--base <sheet folder>]
(no --base: this folder's sheet, Havířovsko/Karvinsko/Orlovsko; --base odis-regional-tfj: Těšínsko, Frýdecko-Místecko,
Jablunkovsko-Třinecko and the three town networks). 01_live.py only refreshes the compact live file when the poll folder
is still there."""
import os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
extra = sys.argv[sys.argv.index('--base'):sys.argv.index('--base') + 2] if '--base' in sys.argv else []
for s in ('01_live.py', '01b_plates.py', '01c_fleet.py', '02_timetable.py', '03_read.py', '05_schedule.py', '04_roster.py', '06_render.py'):
    print('==', s, flush=True)
    r = subprocess.run([sys.executable, '-X', 'utf8', os.path.join(HERE, s)] + extra, cwd=HERE)
    if r.returncode and s not in ('01_live.py', '01b_plates.py', '01c_fleet.py'): sys.exit(r.returncode)
    if s == '04_roster.py':
        # config.post_roster: sheet-local steps between the roster and the page (Opava: designed trolleybuses for 204)
        import json
        base = os.path.join(os.path.dirname(os.path.dirname(HERE)), extra[1]) if extra else os.path.dirname(HERE)
        for p in json.load(open(os.path.join(base, 'config.json'), encoding='utf-8')).get('post_roster', []):
            print('==', p, flush=True)
            r = subprocess.run([sys.executable, '-X', 'utf8', os.path.join(base, p)], cwd=base)
            if r.returncode: sys.exit(r.returncode)
