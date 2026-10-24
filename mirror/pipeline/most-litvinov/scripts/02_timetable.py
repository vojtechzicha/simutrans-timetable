"""JDF.zip -> derived/trips.json for the vehicle day, trips cut where the trams really turn.
Version rule as in pipeline/README.md (latest valid-from wins, ties -> shortest validity).
Cut: trips to/from Citadela are cut at the stop containing config.cut_trips.stop_contains (Chempark)."""
import os
from lib import CONFIG, RAW, jdf_open, jdf_versions, pick_version, jdf_tables, jdf_trips, day, save

d = day(CONFIG['vehicle_day']); cut = CONFIG['cut_trips']
outer = jdf_open(os.path.join(RAW, 'JDF.zip'))
lines = CONFIG['jdf']['lines']; vers = jdf_versions(outer, set(lines))
trips, chosen = {}, {}
for code, L in lines.items():
    v = pick_version([x for x in vers if x['line'] == code], d); chosen[L] = v
    res = []
    for t in jdf_trips(jdf_tables(outer, v['inner']), d):
        st, tm = t['stops'], t['times']
        idx = [i for i, s in enumerate(st) if cut['stop_contains'] in s]
        if cut['beyond'] in t['to'] and idx: st, tm = st[:idx[0] + 1], tm[:idx[0] + 1]
        elif cut['beyond'] in t['fr'] and idx: st, tm = st[idx[0]:], tm[idx[0]:]
        elif cut['beyond'] in t['fr'] or cut['beyond'] in t['to']: continue
        if len(st) < 2: continue
        res.append(dict(t, stops=st, times=tm, fr=st[0], to=st[-1], dep=tm[0], arr=tm[-1]))
    trips[L] = res
    print(L, v['inner'], v['valid_from'], '–', v['valid_to'], 'diversion version' if v['diversion'] else '', len(res), 'trips')
save('versions.json', dict(all=vers, chosen=chosen)); save('trips.json', trips)
