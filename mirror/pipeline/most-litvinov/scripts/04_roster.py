"""trips + fleet + config.roster -> derived/lines.json and roster.json.
The roster is a manual design (config.roster, see its "why" per line). This step checks it:
the number of units per line must equal the turns running at that line's peak minute, every car must
exist and be active (register state zar), and no car may be used twice."""
import collections
import math
from lib import CONFIG, load, save, blocks, active_at, make_nm, hhmm, cycle_need, min_turnaround

C = CONFIG; nm = make_nm(C)
trips = load('trips.json'); fleet = {int(k): v for k, v in load('fleet.json').items()}
lines, problems, used = {}, [], set()
for L, tr in trips.items():
    T = C['peak_minute'][L]; bl = blocks(tr); act = active_at(bl, T)
    var = collections.defaultdict(list)
    for t in tr:
        if T - 60 <= t['dep'] < T + 60: var[(nm(t['fr']), nm(t['to']))].append(t)
    V = []
    for (a, b), ts in sorted(var.items(), key=lambda x: -len(x[1])):
        deps = sorted(t['dep'] for t in ts); gaps = [y - x for x, y in zip(deps, deps[1:])]
        seq = collections.Counter(tuple(nm(s) for s in t['stops']) for t in ts).most_common(1)[0][0]
        V.append(dict(fr=a, to=b, n=len(ts), hw=collections.Counter(gaps).most_common(1)[0][0] if gaps else None,
                      deps=[hhmm(d) for d in deps], min_peak_hour=[d % 60 for d in deps if T <= d < T + 60],
                      rt=round(sum(t['arr'] - t['dep'] for t in ts) / len(ts)), stops=list(seq)))
    lf = [sum(t['lf'] for t in b) for b in act]
    lines[L] = dict(at_peak=len(act), turns=len(bl), low_floor_trips_per_active_turn=lf, variants=V)
    cars = C['roster'][L]['cars']
    if len(cars) != len(act): problems.append(f'line {L}: roster has {len(cars)} units, timetable has {len(act)} turns at {hhmm(T)}')
    for u in cars:
        for n in u:
            if n not in fleet: problems.append(f'{n} not in fleet register')
            elif fleet[n]['state'] != 'zar': problems.append(f'{n} is {fleet[n]["state"]} in the register')
            if n in used: problems.append(f'{n} used twice')
            used.add(n)
save('lines.json', lines)
branches = {}
for L, tr in trips.items():
    T = [dict(t, o=nm(t['fr']), d=nm(t['to'])) for t in tr]; t0 = C['peak_minute'][L]
    lay = {k: min(C['cycle_lay'], v) for k, v in min_turnaround(T, t0 - 120, t0 + 60).items()}
    brs = []
    ov = C.get('schedule_override', {}).get(L)
    for a, b in C['branches'][L]:
        cn = (ov['need'], ov['cycle']) if ov else (cycle_need(T, a, b, t0, lay) or cycle_need(T, b, a, t0, lay))
        rts = [t['arr'] - t['dep'] for t in T if {t['o'], t['d']} == {a, b} and t0 - 60 <= t['dep'] < t0 + 60]
        deps = sorted(t['dep'] for t in T if t['o'] in (a, b) and t['d'] in (a, b) and t['o'] == a and t0 - 60 <= t['dep'] < t0 + 60)
        gaps = [y - x for x, y in zip(deps, deps[1:])]; hw = collections.Counter(gaps).most_common(1)[0][0] if gaps else None
        rt2 = 2 * sum(rts) / len(rts) if rts else None
        brs.append(dict(a=a, b=b, need=cn[0] if cn else 0, cycle=cn[1] if cn else None, headway=hw,
                        min_runtime=1 if ov else (math.ceil(rt2 / hw) if (rt2 and hw) else None), assigned=len(C['roster'][L]['cars'])))
        if cn and cn[0] > len(C['roster'][L]['cars']):
            problems.append(f'line {L}: branch needs {cn[0]} trams, roster has {len(C["roster"][L]["cars"])}: add designed cars to config.roster')
    branches[L] = brs
    print('branch', L, [(x['a'], x['b'], 'need', x['need'], 'assigned', x['assigned'], 'min by runtime', x['min_runtime']) for x in brs])
save('roster.json', dict(roster={L: C['roster'][L]['cars'] for L in C['roster']}, branches=branches, problems=problems))
for L in sorted(lines): print(L, 'turns at peak', lines[L]['at_peak'], 'low-floor trips per turn', lines[L]['low_floor_trips_per_active_turn'])
print('PROBLEMS:' if problems else 'roster OK', *problems, sep='\n  ')
