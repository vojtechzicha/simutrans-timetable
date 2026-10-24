"""DPMP JDF inner zips -> data/derived/<state>/trips.json, versions.json, line_class.json.

  python 02_timetable.py --state 2026-09-29

Lines: every licence 655xxx of DPMP (IČO 63217066) in either export (trolleybus lines are in the city export, bus
lines in the bus export; line 18 is in both). Version rule (shared, pipeline/README.md): among a line's versions valid
on the network day, the latest "valid from" wins; ties go to the shortest validity. The traction is the Linky row's
fifth field (T trolleybus, A bus). A line can take its trips from another day (state.service_date_overrides) when it
does not run on the network day at all (line 90 runs only to the flight schedule).
Class of a line on its day: "peak" = trips 13:00-19:00; "morning" = day service ending before 13:00; "night";
"school" = every trip is a school-day trip; "none".
"""
import argparse, collections, datetime, os, re
from common import RAW, state, save, der, day, Folder, jdf_version_rows, jdf_trips, tl, hm

ap = argparse.ArgumentParser(); ap.add_argument('--state', required=True); S = state(ap.parse_args().state)
J = S['jdf']; ND = day(S['network_date'])
vers = []
for kind in ('city', 'bus'):
    folder = os.path.join(RAW, 'jdf', J['export_date'], kind)
    for n, r in jdf_version_rows(folder):
        if not r[0].startswith(J['line_prefix']) or r[2] != J['operator_ic']: continue
        ds = [datetime.datetime.strptime(x, '%d%m%Y').date() for x in r[3:] if re.fullmatch(r'\d{8}', x)]
        vers.append(dict(kind=kind, inner=n, code=r[0], line=str(int(r[0][3:])), name=r[1], traction=r[4],
                         valid_from=ds[0].isoformat(), valid_to=ds[1].isoformat()))
trips, chosen, cls = {}, {}, {}
for L in sorted({v['line'] for v in vers}, key=int):
    d = day(S.get('service_date_overrides', {}).get(L, S['network_date']))
    v = tl.pick_version([x for x in vers if x['line'] == L], d)
    if not v: cls[L] = dict(cls='none', why='no version valid on the day'); continue
    T = tl.jdf_tables(Folder(os.path.join(RAW, 'jdf', J['export_date'], v['kind'])), v['inner'])
    tr = jdf_trips(T, d)
    deps = sorted(t['dep'] for t in tr)
    day_deps = [x for x in deps if 270 <= x < 1320]
    if tr and all(t['school'] for t in tr): c = 'school'
    elif any(780 <= x < 1140 for x in deps): c = 'peak'
    elif day_deps: c = 'morning'
    elif deps: c = 'night'
    else: c = 'none'
    cls[L] = dict(cls=c, name=v['name'], traction=v['traction'], day=d.isoformat(), trips=len(tr),
                  first=hm(deps[0]) if deps else None, last=hm(deps[-1]) if deps else None)
    chosen[L] = v; trips[L] = dict(traction=v['traction'], day=d.isoformat(), trips=tr)
    print(f"{L:>4} {v['kind']:4} {v['inner']:>10} {v['traction']} {v['valid_from']}–{v['valid_to']} {len(tr):4} trips {c}"
          + (f" (day {d})" if d != ND else ''))
save(dict(all=vers, chosen=chosen), der(S, 'versions.json'))
save(cls, der(S, 'line_class.json'))
save(trips, der(S, 'trips.json'))
print(collections.Counter(x['cls'] for x in cls.values()))
