"""trips.json -> data/derived/<state>/network.json: variant tables, Simutrans lines (branches), needs and schedules.

  python 03_network.py --state 2026-09-29

1. Names. Stop names get the full forms in state.stop_names (no abbreviations on the sheet).
2. Simutrans lines, by rule (as pipeline/ostrava-bus 04_roster.py, state.branch_rule), per DPMP line on the sheet:
   the line's trips in 15:00-18:00 are grouped by unordered terminus pair (a loop is a pair of one stop). The pair with
   the most trips is the main line. Another pair is a branch line of its own when it has at least min_trips trips in
   the window (both directions; half that for a loop), a departure in the 16 o'clock hour, and no depot end.
   state.branches_forced / branches_dropped override the rule for a line. Everything else (extensions, short workings,
   depot runs, the post-peak or pre-peak form of a line) is not a separate line: its minutes are merged into the row of
   the main line leaving the same terminus, and it is listed as "not modelled".
   A line whose afternoon has no pattern at all (state.line_t0) is sized and fitted around its own reference time.
3. Need (vehicles at 16:00):
   - two termini: cycle_need_peak (the tram cycle_need that skips a round trip waiting over max_wait for its next trip,
     max_wait = max(30, 1.5 x headway)), with each terminus's own shorter timetabled turnaround (min_turnaround, at most
     3 min); if there is no complete round trip, the chained turns of that pair running at 16:00;
   - a loop: the departures during one round trip (leave around 16:00, arrive, next departure at least the layover
     later);
   - the line's need is then at least the most trips on the road at once in 16:00-16:59 (every non-depot trip of the
     DPMP line holds its vehicle until arrival + that terminus's layover); the difference goes to the main line
     (brief rule d, Prague / Ostrava bus rule);
   - every Simutrans line gets at least 1 vehicle (a thin line still needs its bus in the game).
4. Schedule per stop entry (the terminus a vehicle leaves from): runfit (shared rule, Ostrava tram lib) on the entry's
   departures plus the merged minutes. A terminus with no exact stretch of 2+ departures but at most 8 departures in the
   whole day gets "Departure every 1440" with every departure of the day as Offset + Also at (exact, the fork allows
   intervals dividing 1440). Every terminus is a turning loop or turning point, so every value is set 1 min early (-1).
"""
import argparse, collections, math, re
from common import state, load, save, der, runfit, loop_shift, cycle_need_peak, min_turnaround, blocks, active_at, hm, hhmm

ap = argparse.ArgumentParser(); ap.add_argument('--state', required=True); S = state(ap.parse_args().state)
T = load(der(S, 'trips.json'))
BR = S['branch_rule']; F = S['fit']; DEPOTS = set(S['depot_stops'])

def nm(s):
    s = S['stop_names'].get(s, s)
    for a, b in S['stop_name_expansions']: s = s.replace(a, b)
    if ',' in s and ', ' not in s: s = s.replace(',', ', ')
    return re.sub(r'\s+', ' ', s).strip()

def headway(deps):
    g = [y - x for x, y in zip(deps, deps[1:])]
    return collections.Counter(g).most_common(1)[0][0] if g else None

def loop_need(tr, a, t0, lay):
    A = sorted(t['dep'] for t in tr if t['o'] == a and t['d'] == a)
    rt = {t['dep']: t['arr'] - t['dep'] for t in tr if t['o'] == a and t['d'] == a}
    res = []
    for s in [x for x in A if t0 - 30 <= x < t0 + 30]:
        nx = next((x for x in A if x >= s + rt[s] + lay), None)
        if nx is None or nx - (s + rt[s]) > 60: continue
        res.append((sum(1 for x in A if s <= x < nx), nx - s))
    return max(res) if res else None

def fit(deps, core, lo, hi, dayall, t0):
    """Brno bus rule (after the Prague trolleybus review, 29 Sep): an entry must reproduce the whole reference hour.
    Try runfit on the shared core, then on the reference hour itself; if neither reproduces every real departure of
    the hour, set the hour's own minutes repeated hourly (every 60, at most 8 slots). An entry with at most 8
    departures in the whole day gets every 1440 with all of them (exact all day); an entry with no departure in the
    hour and more than 8 a day keeps plain runfit (approximate)."""
    real = sorted(x for x in deps if t0 <= x < t0 + 60)
    if 0 < len(dayall) <= 8 and set(dayall) >= set(real):      # a thin entry: the whole day, exact
        return dict(I=1440, R=sorted(dayall), first=min(dayall), last=max(dayall), n=len(dayall), core=True, how='daily')
    def hour_of(f): return sorted(x for x in range(t0, t0 + 60) if x % f['I'] in set(f['R']))
    cands = [runfit(deps, core, lo, hi), runfit(deps, (t0, t0 + 60), lo, hi)]
    if real:
        for f in cands:
            if f and f['n'] >= 2 and hour_of(f) == real: return dict(f, how='runfit')
        if len(real) <= 8:
            return dict(I=60, R=sorted({x % 60 for x in real}), first=real[0], last=real[-1], n=len(real), core=True, how='hour')
    if 0 < len(dayall) <= 8:
        return dict(I=1440, R=sorted(dayall), first=min(dayall), last=max(dayall), n=len(dayall), core=True, how='daily')
    f = cands[0]
    return dict(f, how='runfit') if f and f['n'] >= 2 else None

def deviation(f, deps, lo, hi):
    """largest distance from a real departure in [lo, hi) to the nearest set departure (real minutes)"""
    slots = [x for x in range(lo - 60, hi + 60) if (x in f['R'] if f['I'] == 1440 else x % f['I'] in set(f['R']))]
    ds = [min(abs(x - y) for y in slots) for x in deps if lo <= x < hi] if slots else []
    return max(ds) if ds else 0

out = {}; sim = []
order = [(g, L) for g, ls in S['groups'].items() for L in ls]
for grp, L in order:
    raw = T[L]['trips']
    tr = [dict(t, o=nm(t['fr']), d=nm(t['to'])) for t in raw]
    t0 = S.get('line_t0', {}).get(L, S['t0'])
    W = [t0 - 60, t0 + 120]
    fw = S.get('fit_windows', {}).get(L, F)
    # --- variant table: every directed pattern in the table window (display)
    var = collections.defaultdict(list)
    for t in tr:
        if W[0] <= t['dep'] < W[1]: var[(t['o'], t['d'])].append(t)
    V = []
    for (a, b), ts in sorted(var.items(), key=lambda x: -len(x[1])):
        deps = sorted(t['dep'] for t in ts)
        seq = collections.Counter(tuple(nm(s) for s in t['stops']) for t in ts).most_common(1)[0][0]
        V.append(dict(o=a, d=b, n=len(ts), hw=headway(deps), deps=[hhmm(x) for x in deps],
                      m16=sorted(x % 60 for x in deps if t0 <= x < t0 + 60), run=round(sum(t['arr'] - t['dep'] for t in ts) / len(ts)),
                      depot=bool({a, b} & DEPOTS), school=sum(1 for t in ts if t['school']), stops=list(seq)))
    # --- Simutrans lines: pairs in the branch window
    win = [t for t in tr if t0 + BR['window'][0] <= t['dep'] < t0 + BR['window'][1]]     # window relative to t0
    pairs = collections.defaultdict(list)
    for t in win: pairs[frozenset((t['o'], t['d']))].append(t)
    ranked = sorted(pairs.items(), key=lambda x: (-len(x[1]), sorted(x[0])))
    forced = [frozenset(nm(x) for x in p) for p in S.get('branches_forced', {}).get(L, [])]
    dropped = [frozenset(nm(x) for x in p) for p in S.get('branches_dropped', {}).get(L, [])]
    chosen = []
    for p, ts in ranked:
        if p & DEPOTS or p in dropped: continue
        hour = any(t0 <= t['dep'] < t0 + 60 for t in ts)
        need_n = BR['min_trips'] if len(p) == 2 else math.ceil(BR['min_trips'] / 2)
        if not chosen or p in forced or (not forced and len(ts) >= need_n and hour): chosen.append((p, ts))
    for p in forced:
        if p not in [q for q, _ in chosen]: chosen.append((p, pairs.get(p, [])))
    lay = {k: min(S['layover'], v) for k, v in min_turnaround(tr).items()}
    brs = []
    for i, (p, ts) in enumerate(chosen):
        if len(p) == 1:
            a = b = next(iter(p)); cn = loop_need(tr, a, t0, lay.get(a, S['layover'])); how = 'loop round trip'
            dA = sorted(t['dep'] for t in tr if t['o'] == a and t['d'] == a)
        else:
            cnt = collections.Counter(t['o'] for t in ts)
            a = max(p, key=lambda x: (cnt[x], x)); b = next(x for x in p if x != a)
            if brs and (brs[0]['a'] in p or brs[0]['b'] in p) and b in (brs[0]['a'], brs[0]['b']):
                a, b = b, a             # a branch leaves from the terminus it shares with the main line
            dA = sorted(t['dep'] for t in tr if t['o'] == a and t['d'] == b)
            hw = headway([x for x in dA if t0 - 60 <= x < t0 + 120]) or 30
            mw = max(30, int(1.5 * hw))
            cn = cycle_need_peak(tr, a, b, t0, lay, max_wait=mw) or cycle_need_peak(tr, b, a, t0, lay, max_wait=mw)
            how = 'round trip'
        if not cn:
            act = len(active_at(blocks([t for t in tr if {t['o'], t['d']} == set(p)]), t0))
            cn = (act, None); how = 'turns running at %s' % hm(t0)
        rts = [t['arr'] - t['dep'] for t in ts]
        brs.append(dict(a=a, b=b, loop=len(p) == 1, need=cn[0], cycle=cn[1], how=how, trips=len(ts),
                        runtime=round(sum(rts) / len(rts)) if rts else None))
    # on the road at once in the reference hour (brief rule d)
    rt_ = [t for t in tr if not ({t['o'], t['d']} & DEPOTS)]
    onroad = max(sum(1 for t in rt_ if t['dep'] <= m < t['arr'] + lay.get(t['d'], S['layover'])) for m in range(t0, t0 + 60))
    extra = onroad - sum(b['need'] for b in brs)
    if extra > 0: brs[0]['need'] += extra; brs[0]['onroad_extra'] = extra
    for b in brs:
        if b['need'] < 1: b['need'] = 1; b['min_one'] = True
    # --- ids and names
    for i, b in enumerate(brs):
        far = b['b'] if not b['loop'] else b['a']
        b['id'] = L if i == 0 else S.get('branch_ids', {}).get(f"{L}|{far}", L + far[0])
        b['name'] = f"{b['a']} – {b['b']}" if not b['loop'] else f"{b['a']} (loop)"
    # --- not modelled patterns (not in any chosen pair), and merged minutes per origin
    chosen_p = [p for p, _ in chosen]
    notm = []
    for (a, b_), ts in var.items():
        if frozenset((a, b_)) in chosen_p: continue
        notm.append(dict(o=a, d=b_, n=len(ts), deps=sorted(hhmm(t['dep']) for t in ts), depot=bool({a, b_} & DEPOTS)))
    # --- schedule rows
    for i, b in enumerate(brs):
        ents = [(b['a'], b['b'])] if b['loop'] else [(b['a'], b['b']), (b['b'], b['a'])]
        rows = []
        for o, d in ents:
            own = sorted(t['dep'] for t in tr if t['o'] == o and t['d'] == d)
            merged = []
            main_from_o = next((x for x in brs if o in (x['a'], x['b'])), None)
            if main_from_o is b:        # only the first Simutrans line leaving this terminus takes the extra minutes
                for (a2, d2), ts in var.items():
                    if a2 == o and frozenset((a2, d2)) not in chosen_p and not ({a2, d2} & DEPOTS):
                        merged += [t['dep'] for t in ts]
            allm = sorted(set(own + merged))
            dayall = [t['dep'] for t in tr if t['o'] == o and t['d'] == d]
            f = fit(allm, tuple(fw['core']), fw['lo'], fw['hi'], dayall, t0)
            # hand-set rows (state.fit_overrides, "<Simutrans id>|<from>|<to>": {I, R, first, last, how, note}; added 25 Oct
            # 2026 for the both-ends-same-rate check): how 'override' = an exact stretch first-last, 'approx' = an even pattern
            fo = S.get('fit_overrides', {}).get(f"{b['id']}|{o}|{d}")
            if fo:
                f = dict(I=fo['I'], R=sorted(fo['R']), first=fo['first'], last=fo['last'], core=True, how=fo.get('how', 'override'),
                         n=sum(1 for x in allm if fo['first'] <= x <= fo['last']))
            h0, h1 = t0, t0 + 60
            real16 = sorted(x for x in allm if h0 <= x < h1)
            if f:
                setm = sorted(x for x in range(h0, h1) if (x % f['I']) in set(f['R']) or (f['I'] == 1440 and x in f['R']))
                row = dict(stop=o, to=d, every=f['I'], real=f['R'], set=loop_shift(f['I'], f['R'], S['all_termini_are_loops']),
                           span=f"{hm(f['first'])}–{hm(f['last'])}", n=f['n'], how=f['how'],
                           perh=round(60 * len(f['R']) / f['I'], 2) if f['I'] <= 60 else None,
                           exact=setm == real16, missing=[x % 60 for x in real16 if x not in setm], extra=[x % 60 for x in setm if x not in real16],
                           hour=[x % 60 for x in real16], merged=sorted(set(hhmm(x) for x in merged if W[0] <= x < W[1])),
                           dev=deviation(f, allm, W[0], W[1]), window=[hhmm(W[0]), hhmm(W[1])],
                           deps=[hhmm(x) for x in allm if W[0] <= x < W[1]], note=fo.get('note', '') if fo else '')
            else:
                row = dict(stop=o, to=d, every=None, hour=[x % 60 for x in real16], deps=[hhmm(x) for x in allm if W[0] <= x < W[1]])
            rows.append(row)
        b['rows'] = rows
        sim.append(dict(id=b['id'], line=L, group=grp, main=i == 0, **{k: v for k, v in b.items() if k != 'id'}))
    out[L] = dict(group=grp, traction=T[L]['traction'], day=T[L]['day'], t0=t0, variants=V, simutrans=[b['id'] for b in brs],
                  not_modelled=notm, onroad=onroad)
    print(f"{L:>3} {grp[:5]:5} on-road {onroad:2}  " + '  '.join(f"{b['id']}: {b['a'][:14]}–{b['b'][:14]} need {b['need']} ({b['how'][:10]}{', +%d on road' % b['onroad_extra'] if b.get('onroad_extra') else ''})" for b in brs))
# ---- reference tables (kept from the old sheet): stops and their lines, termini with their departures
stops = collections.defaultdict(lambda: collections.defaultdict(collections.Counter))
term = collections.defaultdict(lambda: dict(dep=collections.defaultdict(list), arr=collections.Counter()))
for grp, L in order:
    t0 = S.get('line_t0', {}).get(L, S['t0'])
    for t in T[L]['trips']:
        o, d = nm(t['fr']), nm(t['to'])
        if {o, d} & DEPOTS or not (t0 - 60 <= t['dep'] < t0 + 120): continue
        for st in t['stops'][:-1]: stops[nm(st)][L][d] += 1
        term[o]['dep'][L].append(hhmm(t['dep'])); term[d]['arr'][L] += 1
stops = {k: {L: dict(c) for L, c in v.items()} for k, v in stops.items()}
term = {k: dict(dep={L: sorted(x) for L, x in v['dep'].items()}, arr=dict(v['arr'])) for k, v in term.items() if v['dep']}
save(dict(lines=out, simutrans=sim, stops=stops, termini=term), der(S, 'network.json'))
print('Simutrans lines', len(sim), 'need', sum(s['need'] for s in sim))
