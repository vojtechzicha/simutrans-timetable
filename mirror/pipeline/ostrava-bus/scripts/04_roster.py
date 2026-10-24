"""trips + fleet + live -> derived/lines.json (branch tables) and roster.json (branches, needs, observed buses).

1. Branches, found automatically (57 lines are too many to list by hand). A line's variants in
   config.branch_rule.window (15:00–18:00) are grouped by unordered terminus pair. The Vozovna trolejbusů /
   sad Boženy Němcové pair is one terminus (config.terminus_alias): buses arrive at one stop and leave from the next.
   A pair is its own Simutrans line when it has >= 2 × min_trips trips in the window (about 3 each way), at least
   one departure in the 16 o'clock hour, and no depot end (config.depot_stops). The pair with the most trips is
   always a branch. Smaller pairs (extensions, short workings, depot runs) are not separate lines; 05_schedule
   merges their minutes into the main row from the same terminus.
2. Need per branch: lib.cycle_need_peak at 16:00, with the terminus's own shorter turnaround where the timetable
   has one. A round trip that waits longer than max(30 min, 1.5 × the headway) for a return trip is skipped,
   because there the buses leave as another line. Fallback when there is no complete round trip (one-way loops,
   sparse lines): the number of chained turns of that pair running at 16:00, at least 1.
   The line's need is then the larger of that sum and the buses on the road (every non-depot trip holds a bus
   from departure to arrival + the layover used for cycle_need, the most at once in 16:00–16:59), as on the Prague bus sheet. The
   difference goes to the main branch; it covers the buses of extensions and short workings.
3. Roster from the live feed (live.json): mode "peak" = the vehicle day's peak window; mode "provisional" = the
   evening before (config.live.provisional), marked "seen in the evening, not yet confirmed at the peak". The first
   sighting in the window gives line, course and trip. Branch: the branch whose far terminus
   matches the trip's start or final stop, else the branch with the largest shortfall.
4. Designed buses where a branch has fewer buses than its need: real car numbers from the line's record history,
   covering every type of the line roster first, then by recency; the free history cars left over are listed as
   "not needed" (see step 4 below).
"""
import collections, math, re, unicodedata
from lib import CONFIG, load, save, make_nm, hhmm, cycle_need_peak, min_turnaround, blocks, active_at, mark_spares, pattern_need, branch_pairs, circuitize, path_variants, dpath, hand_lines

C = CONFIG; nm0 = make_nm(C); AL = C['terminus_alias']
def nm(s): n = nm0(s); return AL.get(n, n)
SCH = load('schedule.json'); PEAKS = load('peaks.json')
def T0_(L): return PEAKS.get(L, {}).get('anchor', CONFIG['peak_minute'])
# keep_roster (config): the roster published last. Fewest moves (user rule): a bus keeps its branch when its line still has
# that branch, and a designed bus stays on its line, while the line still needs it.
import os as _os, json as _json
PREV = _json.load(open(_os.path.join(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))), CONFIG['keep_roster']), encoding='utf-8')) if CONFIG.get('keep_roster') else None
PREV_BR = {(L_, n_): u_[3] for L_, us_ in (PREV or {}).get('roster', {}).items() for u_ in us_ for n_ in u_[1]}
PREV_DES = {n_: L_ for L_, us_ in (PREV or {}).get('roster', {}).items() for u_ in us_ if u_[2] == 'designed' for n_ in u_[1]}
trips = load('trips.json'); fleet = {int(k): v for k, v in load('fleet.json').items()}
LV = load('live.json'); LIVE = {int(k): v for k, v in LV['cars'].items()}
TW = C['table_window']; BRW = C['branch_rule']; DEPOTS = set(C['depot_stops'])

# ---- lines: variant tables (display uses the real names, not the alias)
lines = {}
for L, tr in trips.items():
    var = collections.defaultdict(list); dl = T0_(L) - C['peak_minute']
    for t in tr:
        if TW[0] + dl <= t['dep'] < TW[1] + dl: var[(nm0(t['fr']), nm0(t['to']))].append(t)
    V = []
    for (a, b), ts in sorted(var.items(), key=lambda x: -len(x[1])):
        deps = sorted(t['dep'] for t in ts); gaps = [y - x for x, y in zip(deps, deps[1:])]
        seq = collections.Counter(tuple(nm0(s) for s in t['stops']) for t in ts).most_common(1)[0][0]
        V.append(dict(fr=a, to=b, n=len(ts), hw=collections.Counter(gaps).most_common(1)[0][0] if gaps else None,
                      deps=[hhmm(d) for d in deps], min_peak_hour=sorted(set(d % 60 for d in deps if T0_(L) <= d < T0_(L) + 60)),
                      rt=round(sum(t['arr'] - t['dep'] for t in ts) / len(ts)), stops=list(seq)))
    lines[L] = dict(variants=V)
save('lines.json', lines)

# ---- 1 + 2. branches and needs
def headway(deps):
    g = [y - x for x, y in zip(deps, deps[1:])]
    return collections.Counter(g).most_common(1)[0][0] if g else None
# stops only one line serves in 13:00-19:00 (DPO lines and the ODIS lines of the last 07_odis run), for path_variants
_srv = collections.defaultdict(set)
for L_, tr_ in list(trips.items()) + (list(load('odis.json')['trips'].items()) if _os.path.exists(dpath('odis.json')) else []):
    for t in tr_:
        if 780 <= t['dep'] < 1140:
            for s_ in t['stops']: _srv[nm0(s_)].add(L_)
def own_stops(L, tr): return {s_ for t in tr for s_ in t['stops'] if _srv.get(nm0(s_)) == {L}}
branches = {}
for L, tr in trips.items():
    tr = [dict(t, o=nm(t['fr']), d=nm(t['to'])) for t in tr]
    win = [t for t in tr if BRW['window'][0] <= t['dep'] < BRW['window'][1]]
    T0 = T0_(L)
    chosen, ranked = branch_pairs(tr, C, T0)   # peak rule + afternoon rule (lib), around the line's anchor
    lay = {k: min(C['cycle_lay'], v) for k, v in min_turnaround(tr).items()}
    brs = []
    for p, ts in chosen:
        # orient the branch from the terminus with the most departures in the window
        cnt = collections.Counter(t['o'] for t in ts)
        a = max(p, key=lambda x: (cnt[x], x)); b = next(x for x in p if x != a)
        dA = sorted(t['dep'] for t in tr if t['o'] == a and t['d'] == b); dB = sorted(t['dep'] for t in tr if t['o'] == b and t['d'] == a)
        hw = headway([x for x in dA if T0 - 60 <= x < T0 + 120]) or 30
        mw = max(30, int(1.5 * hw))
        cn = cycle_need_peak(tr, a, b, T0, lay, max_wait=mw) or cycle_need_peak(tr, b, a, T0, lay, max_wait=mw)
        how = 'round trip'
        if not cn:
            act = len(active_at(blocks([t for t in tr if {t['o'], t['d']} == set(p)]), T0))
            cn = (max(1, act), None); how = 'turns at 16:00'
        rts = [t['arr'] - t['dep'] for t in ts] or [t['arr'] - t['dep'] for t in tr if {t['o'], t['d']} == set(p)]
        rt2 = 2 * sum(rts) / len(rts) if rts else None
        brs.append(dict(a=a, b=b, need=cn[0], cycle=cn[1], how=how, headway=hw if dA else None, trips=len(ts),
                        min_runtime=math.ceil(rt2 / hw) if (rt2 and hw) else None))
    others = [dict(pair=sorted(p), trips=len(ts)) for p, ts in ranked if all(p != q for q, _ in chosen)]
    # buses on the road (as pipeline/praha-bus): every non-depot trip holds a bus from departure to arrival + the
    # layover (3 min, or the terminus's own shorter timetabled turnaround, as for cycle_need; a flat 3 min doubled
    # line 99, which runs one bus on a 30-min round trip with 2 and 0 min layovers);
    # the most at once in 16:00–16:59. It catches the buses of extensions and short workings that round trips on
    # the branch pairs miss. The line's need is the larger count; the difference goes to the main branch.
    rt_ = [t for t in tr if not ({t['o'], t['d']} & DEPOTS)]
    onroad = max(sum(1 for t in rt_ if t['dep'] <= m < t['arr'] + lay.get(t['d'], C['cycle_lay'])) for m in range(T0, T0 + 60))
    extra = onroad - sum(b['need'] for b in brs)
    if extra > 0: brs[0]['need'] += extra; brs[0]['variant_extra'] = extra
    # Size every branch from the schedule pattern the sheet suggests (user rule, 20 Oct 2026: 21 was sized at 4 from the
    # every-20 timetable around 16:00 while the sheet suggests every 40, which 2 buses run). Both ends must be scheduled;
    # otherwise the timetable sizing above stays. The variant extra is dropped: variants are not modelled.
    for b in brs:
        pa = next((p for p in SCH.get(L, []) if p.get('every') and nm(p['fr']) == b['a'] and nm(p['to']) == b['b']), None)
        pb = next((p for p in SCH.get(L, []) if p.get('every') and nm(p['fr']) == b['b'] and nm(p['to']) == b['a']), None)
        if not (pa and pb): continue
        def rt_(x, y):
            r = [t['arr'] - t['dep'] for t in tr if t['o'] == x and t['d'] == y and T0 - 60 <= t['dep'] < T0 + 120] or [t['arr'] - t['dep'] for t in tr if t['o'] == x and t['d'] == y]
            return round(sum(r) / len(r))
        rts = [rt_(b['a'], b['b']), rt_(b['b'], b['a'])]
        lays = [lay.get(b['a'], C['cycle_lay']), lay.get(b['b'], C['cycle_lay'])]
        n_, cyc_, waits_ = pattern_need([pa, pb], rts, lays, T0)
        b.update(need=n_, cycle=cyc_, how='pattern', waits=waits_, runtimes=rts, pattern_every=pa['every'], approx='approx' in pa or 'approx' in pb)
        b.pop('variant_extra', None)
        if pa.get('alt') and pb.get('alt'):   # what the slower option of a row to check would need
            b['alt_need'] = pattern_need([pa['alt'], pb['alt']], rts, lays, T0)[0]
    # one circuit where it saves a bus over separate branch lines (owner, 20 Oct 2026; lib.circuitize)
    circ = circuitize(brs, SCH.get(L, []), tr, lay, T0, lambda x: AL.get(x, x), paths=path_variants(tr, T0, lambda x: AL.get(x, x), own_stops(L, tr)))
    if circ:
        print('circuit', L, [(c['b'], c['need'], c['cycle']) for c in circ], 'separate', circ[0]['sep_need'])
        brs = circ
    if L in C.get('hand_lines', {}):   # hand-set Simutrans lines (bus schedule method; config.hand_lines_rule)
        hb = hand_lines(C['hand_lines'][L], L, T0, trips, nm, C)
        brs = brs + hb if C['hand_lines'][L].get('mode') == 'add' else hb
        print('hand-set', L, [(b['name'], b['need'], b['waits']) for b in hb])
    branches[L] = dict(branches=brs, others=others)
    # config.line_overrides: the owner sets a line's model by hand (bus 41 as it runs at 14:00, one circuit)
    if L in C.get('line_overrides', {}):
        ov = C['line_overrides'][L]
        branches[L] = dict(branches=[dict(ov['branch'], trips=len(win), min_runtime=None, override=True)], others=[])

# ---- 3. observed roster (peak) or provisional roster (evening before)
MODE = LV['mode']; W = LV['window']
def key(s):
    s = unicodedata.normalize('NFKD', s or '').encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]', '', s)
def inwin(t): return W[0] <= t <= W[1]
obs = {}
for n, s_ in LIVE.items():
    s_ = [x for x in s_ if inwin(x[0]) and x[1] in trips]
    if s_ and n in fleet: obs[n] = dict(line=s_[0][1], course=s_[0][2], first=s_[0][0], fr=s_[0][3], to=s_[0][4])
FLAG = '' if MODE == 'peak' else 'evening'
roster = {L: [] for L in trips}
for n, o in sorted(obs.items()):
    brs = branches[o['line']]['branches']
    ends = {key(o['fr']), key(o['to'])}
    match = [i for i, b in enumerate(brs) if any(k and (k in key(b['b']) or key(b['b']).endswith(k)) for k in ends)]
    roster[o['line']].append([fleet[n]['cat'], [n], FLAG, match[0] if len(match) == 1 else None, o['course']])
for L, us in roster.items():
    brs = branches[L]['branches']
    for u in us:
        if u[3] is None:
            have = collections.Counter(x[3] for x in us if x[3] is not None)
            u[3] = max(range(len(brs)), key=lambda i: (brs[i]['need'] - have[i], -i))

# ---- 3a. rebalance within a line: the live trip names match the branch termini only loosely, so where one branch
# of a line has more buses than its need and another has fewer, the highest-course extras move to the short branch
# (as the trolleybus sheet does); moved buses are listed in roster.json "moved".
moved = []
for L, us in roster.items():
    brs = branches[L]['branches']
    if len(brs) < 2: continue
    while True:
        cnt = [sum(1 for u in us if u[3] == i) for i in range(len(brs))]
        over = [i for i in range(len(brs)) if cnt[i] > brs[i]['need']]; under = [i for i in range(len(brs)) if cnt[i] < brs[i]['need']]
        if not over or not under: break
        u = max((u for u in us if u[3] == over[0]), key=lambda u: int(u[4]) if str(u[4]).isdigit() else 0)
        u[3] = under[0]; moved.append(dict(line=L, car=u[1][0], course=u[4], to=under[0]))

# ---- 3b. logged surplus (user, 29 Sep 2026, "Logged surplus too"): where a Simutrans line has more buses seen than
# it needs, exactly the need is counted: one of every type first, then the lowest course numbers (the live feed gives
# no afternoon-only mark); the rest are "not needed", shown but not counted. Brno's mark_spares does the choice.
# fewest moves: two buses that changed branch in opposite directions swap back to the branches they were published on
for L, us in roster.items():
    if len(branches[L]['branches']) < 2: continue
    for u in us:
        pu = PREV_BR.get((L, u[1][0]))
        if pu is None or pu == u[3]: continue
        v = next((v for v in us if v is not u and PREV_BR.get((L, v[1][0])) == u[3] and v[3] == pu), None)
        if v: u[3], v[3] = pu, u[3]
surplus = {}
for L, us in roster.items():
    for i, b in enumerate(branches[L]['branches']):
        units = [dict(type=u[0], kurz=int(u[4]) if str(u[4]).isdigit() else 9999, src='', u=u) for u in us if u[3] == i]
        if mark_spares(units, b['need']):
            for x in units:
                if x.get('spare'): surplus.setdefault(L, []).append(x['u'])
    if L in surplus: roster[L] = [u for u in us if u not in surplus[L]]

# ---- 4. designed buses with real car numbers, and the spare history cars (shared rule, user 29 Sep 2026:
# "Roster coverage and spares" in pipeline/README.md; reference pipeline/praha-bus/scripts/04_courses.py)
# The line's roster = every active car with weekday ODIS records on the line (since config.history.since) plus the
# cars seen on it in the live window. "Free" = not seen anywhere in the live feed that day and not used on a line.
# Picking for the shortfall: first one free car of each roster type the used cars lack (the type with the most
# records first), then by recency (last record date), then by record count. Lines with no history take the line's
# main type from its home garage. The free roster cars left over are "not needed": shown, not counted.
# ---- 3c. owner's type choices (config.owner_types_rule): named buses replace seen buses of another type on a branch,
# highest course first; a replaced bus goes to "not needed" with the car that took its place as a 6th field
for L, o in C.get('owner_types', {}).items():
    for n in o['cars']:
        cands = [u for u in roster[L] if u[2] == FLAG and u[3] == o['branch'] and fleet[u[1][0]]['cat'] != fleet[n]['cat']]
        u = max(cands, key=lambda u: int(u[4]) if str(u[4]).isdigit() else 0)
        roster[L].remove(u); surplus.setdefault(L, []).append(u + [n])
        roster[L].append([fleet[n]['cat'], [n], 'owner', u[3], u[4]])

H = load('history.json')
aff = collections.defaultdict(collections.Counter); last = {}
for L, n, k, d, note in H:
    aff[n][L] += 1; last[(n, L)] = max(last.get((n, L), ''), d)
def home(L):
    c = collections.Counter()
    for n, a in aff.items():
        if n in fleet and a[L]: c[fleet[n]['depot_code']] += a[L]
    for u in roster[L]: c[fleet[u[1][0]]['depot_code']] += 3
    return c.most_common(1)[0][0] if c else None
def maintype(L):
    c = collections.Counter(fleet[u[1][0]]['cat'] for u in roster[L])
    for n, a in aff.items():
        if n in fleet and a[L]: c[fleet[n]['cat']] += a[L] / 10
    return c.most_common(1)[0][0] if c else 'Urbino 12 CNG'
def active(n): return n in fleet and fleet[n]['state'] == 'zar' and fleet[n]['cat'] != '?'
added = []; spares = {}
used = {n for us in list(roster.values()) + list(surplus.values()) for u in us for n in u[1]}
def free(n): return active(n) and n not in used and n not in LIVE
for L, B in sorted(branches.items(), key=lambda x: -sum(b['need'] for b in x[1]['branches'])):
    short = [(i, max(0, b['need'] - sum(1 for u in roster[L] if u[3] == i))) for i, b in enumerate(B['branches'])]
    slots = [i for i, k in short for _ in range(k)]
    hist_cars = [n for n in aff if aff[n][L] and active(n)]
    rtypes = collections.Counter()
    for n in hist_cars: rtypes[fleet[n]['cat']] += aff[n][L]
    for u in roster[L]: rtypes[u[0]] += 1
    picks = []
    for _ in slots:
        have = {fleet[u[1][0]]['cat'] for u in roster[L]} | {fleet[n]['cat'] for n, _w in picks}
        pool = [n for n in hist_cars if free(n) and n not in [p for p, _w in picks] and PREV_DES.get(n, L) == L]
        mine = [n for n in pool if PREV_DES.get(n) == L]
        lack = [t for t, _c in rtypes.most_common() if t not in have and any(fleet[n]['cat'] == t for n in pool)]
        if mine:
            cand = mine; why = 'designed for this line on the sheet published before (kept, fewest moves); '
        elif lack:
            cand = [n for n in pool if fleet[n]['cat'] == lack[0]]; why = f'covers the {fleet[cand[0]]["full"].split(" (")[0]} type of the line roster; '
        else:
            cand = pool; why = ''
        cand.sort(key=lambda n: (last[(n, L)], aff[n][L]), reverse=True)
        if cand:
            n = cand[0]
            why += f"{aff[n][L]} weekday records on line {L}, last {last[(n, L)]}"
        else:
            hd, mt = home(L), maintype(L)
            cand = sorted([n for n in fleet if free(n) and n not in [p for p, _w in picks]],
                          key=lambda n: -((15 if fleet[n]['depot_code'] == hd else 0) + (10 if fleet[n]['cat'] == mt else 0)))
            n = cand[0]; why = f"no free car with history on line {L}; the line's main type from its home garage"
        picks.append((n, why)); used.add(n)
    for i, (n, why) in zip(slots, picks):
        roster[L].append([fleet[n]['cat'], [n], 'designed', i, None])
        added.append(dict(line=L, branch=i, car=n, why=why + f"; not seen in the live feed on {LV['day']}"))
    spares[L] = [dict(car=n, last=last[(n, L)], records=aff[n][L]) for n in sorted(hist_cars, key=lambda n: last[(n, L)], reverse=True) if free(n)]
for L, B in branches.items():
    for i, b in enumerate(B['branches']):
        b['observed'] = sum(1 for u in roster[L] if u[3] == i and u[2] not in ('designed', 'owner'))
        b['owner'] = sum(1 for u in roster[L] if u[3] == i and u[2] == 'owner')
        b['surplus'] = sum(1 for u in surplus.get(L, []) if u[3] == i)
        b['assigned'] = sum(1 for u in roster[L] if u[3] == i)
save('roster.json', dict(moved=moved, surplus=surplus, spares=spares, mode=MODE, live_day=LV['day'], window=W, observed=obs, roster=roster, branches=branches, added=added, live_files=LV['files']))
need = sum(b['need'] for B in branches.values() for b in B['branches'])
print('lines', len(branches), 'simutrans lines', sum(len(B['branches']) for B in branches.values()), 'need', need,
      'observed', len(obs), 'designed', len(added))
for L in sorted(branches, key=int):
    print(L, [(b['a'][:18], b['b'][:18], b['need'], b['how'][:5], b['observed']) for b in branches[L]['branches']])
