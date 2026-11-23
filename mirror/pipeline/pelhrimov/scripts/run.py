"""Rebuild the MHD Pelhřimov + VDV 250 sheet from the stored raw data: python -X utf8 scripts/run.py

Sheet-local steps (this folder): 01_live.py (VDV live poll -> live_compact.json), 01c_fleet.py (register -> fleet.json),
06_render.py (the page). The schedule, roster and coverage steps are the ODIS regional pipeline's, run unchanged with
--base pelhrimov: 02_timetable, 03_read, 05_schedule, 04_roster (pipeline/odis-regional-hko/scripts).
The live poller (01_live_poll.py) runs on its own, detached, on the vehicle day."""
import os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); PIPE = os.path.dirname(os.path.dirname(HERE))
HKO = os.path.join(PIPE, 'odis-regional-hko', 'scripts')
steps = [(HERE, '01_live.py', True), (HERE, '01c_fleet.py', False), (HKO, '02_timetable.py', False), (HKO, '03_read.py', False),
         (HKO, '05_schedule.py', False), (HKO, '04_roster.py', False), (HERE, '06_render.py', False)]
for d, s, optional in steps:
    print('==', s, flush=True)
    r = subprocess.run([sys.executable, '-X', 'utf8', os.path.join(d, s), '--base', 'pelhrimov'], cwd=d)
    if r.returncode and not optional: sys.exit(r.returncode)
