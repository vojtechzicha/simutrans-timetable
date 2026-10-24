"""JDF.zip -> derived/trips.json: every trip of every trolleybus line running on the vehicle day.

Version rule (shared): among a line's versions valid on the day, the latest "valid from" wins; ties go to the
shortest validity. Line 107 has two identical inner zips in the export; either gives the same trips.
"""
from lib import CONFIG, RAW, jdf_open, jdf_versions, pick_version, jdf_tables, jdf_trips, day, save
import os

d = day(CONFIG['vehicle_day'])
outer = jdf_open(os.path.join(RAW, 'JDF.zip'))
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
