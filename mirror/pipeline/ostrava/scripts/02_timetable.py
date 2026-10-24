"""JDF.zip -> derived/trips.json: every trip of every tram line running on the vehicle day.

Version rule: among a line's versions valid on the day, the latest "valid from" wins; ties go to the
shortest validity (a short-term version overrides the long one it sits inside).
"""
from lib import CONFIG, RAW, jdf_open, jdf_versions, pick_version, jdf_tables, jdf_trips, day, save
import os

# config.timetable (optional): a newer JDF snapshot and the day its versions are picked for, while vehicle_day keeps the
# roster day (20 Oct 2026: Don Bosco served again from 20 Oct; the trams stay those of 25 Sep)
TT = CONFIG.get('timetable') or {}
d = day(TT.get('day', CONFIG['vehicle_day']))
outer = jdf_open(os.path.join(os.path.dirname(RAW), TT['snapshot'], 'JDF.zip') if TT.get('snapshot') else os.path.join(RAW, 'JDF.zip'))
lines = CONFIG['jdf']['lines']
vers = jdf_versions(outer, set(lines))
trips, chosen = {}, {}
for code, L in lines.items():
    v = pick_version([x for x in vers if x['line'] == code], d)
    if not v: print('no valid version for', code); continue
    chosen[L] = v
    trips[L] = jdf_trips(jdf_tables(outer, v['inner']), d)
    print(L, v['inner'], v['valid_from'], '–', v['valid_to'], len(trips[L]), 'trips')
save('versions.json', dict(all=vers, chosen=chosen))
save('trips.json', trips)
