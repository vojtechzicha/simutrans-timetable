"""trips + fleet + live + records -> derived/lines.json (branch tables) and roster.json (observed vehicles).

1. Lines: the 15:00–17:00 variants of every line (headway, minutes, runtime, stop pattern), as in the tram
   pipeline.
2. Need: every branch (config.branches, one Simutrans line each) is sized by cycle_need at 16:00 (lib.cycle_need_peak:
   round trips that wait over 30 min for a return are skipped), with a 3 min
   layover or the terminus's own shorter timetabled turnaround (min_turnaround), as for the trams.
3. Observed roster: every trolleybus the DPO live feed shows on a line in config.live.window (the first
   sighting in the window decides the line and course). This is the roster; nothing is designed unless a branch
   has fewer observed vehicles than its need.
4. Branch of an observed vehicle on 101 and 107: the live trip names do not follow the JDF branches, so the
   position decides. A vehicle seen east of Hranečník (longitude > config.branch_by_position.lng) during
   config.branch_by_position.window is on the battery branch (Radvanice or Bartovice); otherwise on the Hranečník
   branch. Where that leaves a branch short and the other over its need, vehicles move over (only
   battery-capable ones onto a battery branch).
5. Designed additions (only if a branch is still short): the best unused active car, battery-capable where the
   branch runs on battery, of the line's observed main type, preferring cars recorded on the line in the day
   records. Marked "designed, not recorded".
"""
import collections, math
from lib import CONFIG, load, save, make_nm, hhmm, cycle_need_peak as cycle_need, min_turnaround, mark_spares

C = CONFIG; nm = make_nm(C)
trips = load('trips.json')
fleet = {int(k): v for k, v in load('fleet.json').items()}
LIVE = {int(k): v for k, v in load('live.json')['cars'].items()}
RECS = load('records.json')
TW = C['table_window']; W = C['live']['window']; BP = C['branch_by_position']
BATTERY_BRANCH = {(L, i) for L, i in C['battery_branches']}

# ---- 1. lines: branch tables (as pipeline/ostrava 04_roster.py)
lines = {}
for L, tr in trips.items():
    var = collections.defaultdict(list)
    for t in tr:
        if TW[0] <= t['dep'] < TW[1]: var[(nm(t['fr']), nm(t['to']))].append(t)
    V = []
    for (a, b), ts in sorted(var.items(), key=lambda x: -len(x[1])):
        deps = sorted(t['dep'] for t in ts)
        gaps = [y - x for x, y in zip(deps, deps[1:])]
        seq = collections.Counter(tuple(nm(s) for s in t['stops']) for t in ts).most_common(1)[0][0]
        V.append(dict(fr=a, to=b, n=len(ts), hw=collections.Counter(gaps).most_common(1)[0][0] if gaps else None,
                      deps=[hhmm(d) for d in deps], min_peak_hour=sorted(set(d % 60 for d in deps if 960 <= d < 1020)),
                      rt=round(sum(t['arr'] - t['dep'] for t in ts) / len(ts)), stops=list(seq)))
    lines[L] = dict(variants=V)
save('lines.json', lines)

# ---- 2. need per branch
branches = {}
for L, tr in trips.items():
    tr = [dict(t, o=nm(t['fr']), d=nm(t['to'])) for t in tr]
    lay = {k: min(C['cycle_lay'], v) for k, v in min_turnaround(tr).items()}
    brs = []
    for a, b in C['branches'][L]:
        cn = cycle_need(tr, a, b, C['cycle_t0'], lay) or cycle_need(tr, b, a, C['cycle_t0'], lay)
        rts = [t['arr'] - t['dep'] for t in tr if {t['o'], t['d']} == {a, b} and 900 <= t['dep'] < 1080]
        deps = sorted(t['dep'] for t in tr if t['o'] == a and t['d'] == b and 900 <= t['dep'] < 1080)
        gaps = [y - x for x, y in zip(deps, deps[1:])]
        hw = collections.Counter(gaps).most_common(1)[0][0] if gaps else None
        rt2 = 2 * sum(rts) / len(rts) if rts else None
        brs.append(dict(a=a, b=b, need=cn[0] if cn else 0, cycle=cn[1] if cn else None,
                        lay_a=lay.get(a, C['cycle_lay']), lay_b=lay.get(b, C['cycle_lay']),
                        min_runtime=math.ceil(rt2 / hw) if (rt2 and hw) else None, headway=hw,
                        battery=(L, len(brs)) in BATTERY_BRANCH))
    branches[L] = brs

# ---- 3. observed roster
def inwin(t, w): return w[0] <= t <= w[1]
obs = {}
for n, s in LIVE.items():
    s = [x for x in s if inwin(x[0], W) and x[1] in trips]
    if s: obs[n] = dict(line=s[0][1], course=s[0][2], first=s[0][0])
by_line = collections.defaultdict(list)
for n, o in sorted(obs.items()): by_line[o['line']].append(n)

# ---- 4. branch by position (lines with two branches)
def east(n):
    return any(inwin(x[0], BP['window']) and x[1] == obs[n]['line'] and x[5] and x[5] > BP['lng'] for x in LIVE[n] if len(x) > 5)
roster = {}; moved = []
for L, brs in branches.items():
    ns = by_line.get(L, [])
    if len(brs) == 1:
        roster[L] = [[fleet[n]['cat'], [n], '', 0, obs[n]['course']] for n in ns]; continue
    side = {n: (1 if east(n) else 0) for n in ns}
    for i in (0, 1):                               # fill a short branch from the other one's surplus
        short = brs[i]['need'] - sum(1 for v in side.values() if v == i)
        pool = [n for n in ns if side[n] == 1 - i and (fleet[n]['battery'] or not brs[i]['battery'])]
        surplus = sum(1 for n in ns if side[n] == 1 - i) - brs[1 - i]['need']
        for n in sorted(pool, key=lambda n: obs[n]['course'])[:max(0, min(short, surplus))]:
            side[n] = i; moved.append(dict(line=L, car=n, to=i))
    roster[L] = [[fleet[n]['cat'], [n], '', side[n], obs[n]['course']] for n in ns]

# ---- 5a. logged surplus (user, 29 Sep 2026, "Logged surplus too" in pipeline/README.md): where a Simutrans line
# has more trolleybuses seen than it needs, exactly the need is counted: one of every type first, then the lowest
# course numbers (the live feed has no afternoon-only mark); the rest are "not needed". Brno's mark_spares chooses.
surplus = {}
for L, brs in branches.items():
    for i, b in enumerate(brs):
        units = [dict(type=u[0], kurz=int(u[4]) if str(u[4]).isdigit() else 9999, src='', u=u) for u in roster[L] if u[3] == i]
        if mark_spares(units, b['need']):
            surplus.setdefault(L, []).extend(x['u'] for x in units if x.get('spare'))
    if L in surplus: roster[L] = [u for u in roster[L] if u not in surplus[L]]

# ---- 5b. designed additions where a branch is still short, and the line's spare history cars (user, 29 Sep 2026,
# "Roster coverage and spares"). Roster = active cars with weekday ODIS records on the line since
# config.history.since, plus the cars seen on it. Free = not seen anywhere in the live feed that day, not used.
# Pick: battery-capable where the branch needs it; first one free car of each roster type the used cars lack (most
# records first), then by recency and record count. The free roster cars left over are "not needed", not counted.
H = load('history.json')
aff = collections.defaultdict(collections.Counter); last = {}
for L_, n, k, d, note in H:
    aff[n][L_] += 1; last[(n, L_)] = max(last.get((n, L_), ''), d)
def active(n): return n in fleet and fleet[n]['state'] == 'zar' and fleet[n]['cat'] != '?'
used = {n for us in list(roster.values()) + list(surplus.values()) for u in us for n in u[1]}
def free(n): return active(n) and n not in used and n not in LIVE
added = []; spares = {}
for L, brs in branches.items():
    hist_cars = [n for n in aff if aff[n][L] and active(n)]
    rtypes = collections.Counter()
    for n in hist_cars: rtypes[fleet[n]['cat']] += aff[n][L]
    for u in roster[L]: rtypes[u[0]] += 1
    for i, b in enumerate(brs):
        b['observed'] = sum(1 for u in roster[L] if u[3] == i)
        b['surplus'] = sum(1 for u in surplus.get(L, []) if u[3] == i)
        for _ in range(max(0, b['need'] - b['observed'])):
            ok = lambda n: free(n) and (fleet[n]['battery'] or not b['battery'])
            have = {u[0] for u in roster[L]}
            pool = [n for n in hist_cars if ok(n)]
            lack = [t for t, _c in rtypes.most_common() if t not in have and any(fleet[n]['cat'] == t for n in pool)]
            cand = [n for n in pool if fleet[n]['cat'] == lack[0]] if lack else pool
            cand.sort(key=lambda n: (last[(n, L)], aff[n][L]), reverse=True)
            if cand:
                n = cand[0]
                why = (f"covers the {fleet[n]['full']} type of the line roster; " if lack else '') + f"{aff[n][L]} weekday records on line {L}, last {last[(n, L)]}"
            else:
                main = collections.Counter(u[0] for u in roster[L]).most_common(1)
                main = main[0][0] if main else '26Tr'
                cand = sorted([n for n in fleet if ok(n)], key=lambda n: (fleet[n]['cat'] != main, n))
                n = cand[0]; why = f"no free car with history on line {L}; the line's main type"
            used.add(n)
            roster[L].append([fleet[n]['cat'], [n], 'designed', i, None])
            added.append(dict(line=L, branch=i, car=n, why=why + ('; battery-capable' if b['battery'] else '') + f"; not seen in the live feed on {C['vehicle_day']}"))
        b['assigned'] = sum(1 for u in roster[L] if u[3] == i)
    spares[L] = [dict(car=n, last=last[(n, L)], records=aff[n][L]) for n in sorted(hist_cars, key=lambda n: last[(n, L)], reverse=True) if free(n)]

# battery check: every vehicle on a battery branch must be battery-capable
battery_issues = [dict(line=L, car=u[1][0], branch=u[3]) for L in roster for u in roster[L]
                  if branches[L][u[3]]['battery'] and not fleet[u[1][0]]['battery']]
save('roster.json', dict(surplus=surplus, spares=spares, observed=obs, roster=roster, branches=branches, moved=moved, added=added, battery_issues=battery_issues))
for L in sorted(roster, key=int):
    print(L, [(b['a'][:12], b['b'][:14], 'need', b['need'], 'obs', b['observed'], 'assigned', b['assigned'], 'cycle', b['cycle']) for b in branches[L]])
print('observed', len(obs), 'surplus', {L: [u[1][0] for u in v] for L, v in surplus.items()}, 'spares', sum(len(v) for v in spares.values()), 'added', added, 'moved', moved, 'battery issues', battery_issues)
