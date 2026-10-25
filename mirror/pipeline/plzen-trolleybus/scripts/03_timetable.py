"""Timetable for one network state: network table, schedule fits, Simutrans rows and sizes (Plzeň trolleybuses and buses).

  python 03_timetable.py --state 2026-09-29                          trolleybus sheet (this pipeline)
  python 03_timetable.py --state 2026-09-29 --base ../../plzen-bus   bus sheet (states and derived data of plzen-bus)

The Brno bus 03_timetable.py (pipeline/brno-bus), which extends the Brno trolleybus one, with the same rules:
- one rate per Simutrans line: the number of real 16:00-16:59 departures most entries share (on a tie the lower);
- every entry must reproduce the whole 16:00 hour: runfit on the shared core, then on the 16:00 hour, then at the
  line's rate (runfit_rate); failing that, the 16:xx minutes repeated hourly (at most 8 slots), else a partial fit
  whose missing and extra minutes are listed;
- entries may be minute subsets of a leg ({"mod": 60, "keep": [..]});
- "empty_return": {stop: [back to stop, minutes]}: a one-way working whose far end gets no timetable (every 0);
- turn -1 at every turning point; a timing point passed without turning keeps the real minute ("through"/"turn" in
  the state force either). Trolleybus state: "all_loops": every terminus is a loop (-1), block turns included;
- need = max(circuit_need with the timetable's own turnarounds, vehicles on the road 16:00-16:59 per record group,
  each trip holding its vehicle until arrival + min(3, the terminus's shortest timetabled turnaround)) - the rule
  used on the Brno bus and Plzeň tram sheets.
Depot runs (to or from Karlov, the PMDP trolleybus depot and bus garage) are left out.
Writes <base>/data/derived/<state>/timetable.json.
"""
import argparse, collections, math, os, statistics
from common import BASE, state, save, gtfs_trips, gtfs_path, circuit_need, turnarounds, runfit, runfit_rate, best_offset, loop_shift, DIV1440, hm

p = argparse.ArgumentParser(); p.add_argument('--state', required=True); p.add_argument('--base', default=BASE); a = p.parse_args()
base = os.path.abspath(a.base); S = state(a.state, base); F = S['fit']; DER = os.path.join(base, 'data', 'derived')
DEPOTS = set(S.get('depot_stops', ['Karlov']))
trips = gtfs_trips(gtfs_path(S), S['service_date'], S['route_type'])
trips = [t for t in trips if t['line'] in S['line_order'] and t['o'] not in DEPOTS and t['d'] not in DEPOTS]

# ---- network table: 15:00-18:00 trips per terminus pair --------------------------------------------
network = {}
for line in S['line_order']:
    pairs = collections.defaultdict(list)
    for t in trips:
        if t['line'] == line and 900 <= t['dep'] < 1080: pairs[(t['o'], t['d'])].append(t)
    rows = []
    for (o, d), xs in sorted(pairs.items(), key=lambda kv: -len(kv[1])):
        ts = sorted(x['dep'] for x in xs); gaps = [b - a2 for a2, b in zip(ts, ts[1:])]
        rows.append(dict(o=o, d=d, n3h=len(xs), m16=[x - 960 for x in ts if 960 <= x < 1020],
                         hw=statistics.median(gaps) if gaps else None,
                         run=round(statistics.mean(x['arr'] - x['dep'] for x in xs))))
    network[line] = rows

def pattern_hour(I, R):
    return sorted(m for m in range(960, 1020) if m % I in R)

# ---- Simutrans lines ---------------------------------------------------------------------------------
sched, used = [], set()
for sl in S['simutrans_lines']:
    E = sl['entries']; legs = [tuple(e[:3]) for e in E]
    def entry_deps(e):
        xs = [t for t in trips if (t['line'], t['o'], t['d']) == tuple(e[:3])]
        return [t for t in xs if t['dep'] % e[3]['mod'] in e[3]['keep']] if len(e) > 3 else xs
    hour = {i: sorted(t['dep'] for t in entry_deps(e) if 960 <= t['dep'] < 1020) for i, e in enumerate(E)}
    cnt = collections.Counter(len(h) for h in hour.values() if h); top = max(cnt.values())
    rate = sl.get('rate') or min(r for r, n in cnt.items() if n == top)
    rows = []
    for i, e in enumerate(E):
        l, o, d = e[:3]
        xs = entry_deps(e); D = [t['dep'] for t in xs]
        used |= {t['id'] for t in xs}
        key = '|'.join([sl['id'], l, o, d]); H = hour[i]
        if key in F.get('overrides', {}):
            ov = F['overrides'][key]
            if ov.get('auto'):          # one slot every I, offset of least total deviation over 15:30-16:59 (best_offset)
                off, _ = best_offset(D, ov['I'], 930, 1020); dd = [x for x in D if 930 <= x < 1020]
                f = dict(I=ov['I'], R=[off], first=dd[0], last=dd[-1])
            else:
                f = dict(I=ov['I'], R=ov['R'], first=ov['first'], last=ov['last'])
        else:
            f = None
            for core in (tuple(F['core']), (960, 1020)):
                for g in (runfit(D, DIV1440, core), runfit_rate(D, rate, DIV1440, core)):
                    if g and len(g['R']) * 60 == rate * g['I'] and pattern_hour(g['I'], set(g['R'])) == H:
                        f = g; break
                if f: break
            if not f and len(H) == rate and rate <= 8:
                f = dict(I=60, R=sorted(m % 60 for m in H), first=H[0], last=H[-1])
            if not f and len(H) == rate and rate <= 16:           # more than 8 an hour: the best 30-minute pattern
                best = None
                for R30 in [sorted({m % 30 for m in H})]:
                    if len(R30) <= 8:
                        P = pattern_hour(30, set(R30)); dev = len(set(P) ^ set(H))
                        best = dict(I=30, R=R30, first=H[0], last=H[-1])
                f = best
            if not f:
                f = runfit_rate(D, rate, DIV1440, (960, 1020)) or runfit(D, DIV1440, (960, 1020))
        I, R = f['I'], list(f['R'])
        Dset = set(D); Rs = set(R); lo_, hi_ = 960, 1019
        while lo_ - 1 >= 780 and ((lo_ - 1) in Dset) == ((lo_ - 1) % I in Rs): lo_ -= 1
        while hi_ + 1 < 1200 and ((hi_ + 1) in Dset) == ((hi_ + 1) % I in Rs): hi_ += 1
        run16 = [m for m in sorted(Dset) if lo_ <= m <= hi_]
        if all((m in Dset) == (m % I in Rs) for m in range(960, 1020)) and len(run16) >= 2:
            f = dict(f, first=run16[0], last=run16[-1])
        P = pattern_hour(I, set(R))
        missing = [m for m in H if m not in P]; extra = [m for m in P if m not in H]
        # nearest real departure for each modelled one (largest deviation, for approximate fits)
        # largest deviation (approximate fits): each modelled 16:xx departure to the nearest real one, and each real
        # 16:xx departure to the nearest modelled one
        PP = [m for m in range(900, 1080) if m % I in set(R)]
        dev = max([min(abs(m - x) for x in D) for m in P] + [min(abs(m - x) for x in PP) for m in H] or [0]) if (missing or extra) and D else 0
        # a hand-set row (fit.overrides, not 'auto') whose first-last stretch it reproduces exactly: the sheet then says
        # "partial, exact <span>" instead of "approximate" (added 25 Oct 2026)
        ovk = F.get('overrides', {}).get(key, {})
        stretch = bool(ovk) and not ovk.get('auto') and f['last'] > f['first'] and all((m in Dset) == (m % I in Rs) for m in range(f['first'], f['last'] + 1))
        prev = legs[i - 1] if len(legs) > 1 else None
        turn = prev is None or prev[1] == d or o == d or (prev[0], prev[1]) == (l, d)
        tag = f"{sl['id']}|{o}"
        if tag in S.get('through', []): turn = False
        if tag in S.get('turn', []): turn = True
        if len(legs) == 1 and o != d: turn = True
        if S.get('all_loops'): turn = True
        run = round(statistics.mean(t['arr'] - t['dep'] for t in xs if 900 <= t['dep'] < 1080))
        rows.append(dict(line=l, stop=o, to=d, every=I, real=R, set=loop_shift(I, R, turn), loop=turn,
                         perh=len(R) * 60 / I, span=f"{hm(f['first'])}–{hm(f['last'])}", run=run,
                         exact=not missing and not extra, missing=[m - 960 for m in missing], extra=[m - 960 for m in extra],
                         dev=dev, hour=[m - 960 for m in H], deps=sorted(x for x in D if 900 <= x < 1080),
                         **({'stretch': True} if stretch else {})))
    links = dict(S.get('links', {})); links.update(sl.get('empty_return', {}))
    for st, (back, mn) in sl.get('empty_return', {}).items():
        rows.append(dict(line=E[0][0], stop=st, to=back, every=0, real=[], set=[], loop=False, untimed=True, perh=0, span='',
                         run=mn, exact=True, deps=[]))
    own, klegs = [], []
    for i, e in enumerate(E):
        tag = f"{e[0]}#{i}"; own += [dict(t, line=tag) for t in entry_deps(e)]; klegs.append((tag, e[1], e[2]))
    lay = turnarounds(own, klegs, S.get('turnaround_default', 3), links) if len(klegs) > 1 else {0: S.get('turnaround_default', 3)}
    for st in sl.get('empty_return', {}):
        for i in range(len(klegs)):
            if klegs[i - 1][2] == st: lay[i] = 0
    wait = max(30, max(r['every'] for r in rows))
    need = circuit_need(own, klegs, lay=lay, links=links, period=sl.get('period'), maxwait=wait)
    if sl.get('need'):              # stated in the state, with its reason (a sparse branch whose real trips wait long)
        need = (sl['need']['vehicles'], need[1] if need else 0, need[2] if need else [])
    sched.append(dict(id=sl['id'], name=sl['name'], rate=rate, note=sl.get('note', ''), kind=sl.get('kind', ''),
                      text=sl.get('text', ''), rows=rows, records=sl['records'],
                      min_run=math.ceil(sum(r['run'] * (r['perh'] or rate) / 60 for r in rows)),
                      need_why=(sl.get('need') or {}).get('why', ''),
                      need=dict(vehicles=need[0], minutes=need[1],
                                path=[[klegs[j][1], klegs[j][2], hm(dd), hm(aa)] for j, dd, aa in need[2]]) if need else None,
                      lay={f'{legs[k - 1][2]} → {legs[k][2]}': v for k, v in lay.items()}))

# On the road: per record group, the most trips holding a vehicle at once in 16:00-16:59. Need = max(cycle, on the road);
# the extra goes to the group's main line (the Prague/Ostrava/Brno bus rule, and the Plzeň tram sheet's sline_need).
grp = collections.defaultdict(list)
for sl in S['simutrans_lines']: grp[sl['records']].append(sl)
byid = {x['id']: x for x in sched}
for rec, sls in grp.items():
    lines_ = {e[0] for sl in sls for e in sl['entries']}
    ts = [t for t in trips if t['line'] in lines_]
    lay = {}
    for st in {t['d'] for t in ts}:
        arr = [t['arr'] for t in ts if t['d'] == st and 900 <= t['arr'] < 1080]
        dep = sorted(t['dep'] for t in ts if t['o'] == st)
        gaps = [next((d for d in dep if d >= a2), a2 + 99) - a2 for a2 in arr]
        lay[st] = min(3, min(gaps)) if gaps else 3
    onroad = max(sum(1 for t in ts if t['dep'] <= m < t['arr'] + lay[t['d']]) for m in range(960, 1020))
    total = sum((byid[sl['id']]['need'] or {}).get('vehicles') or byid[sl['id']]['min_run'] for sl in sls)
    main = next((sl['id'] for sl in sls if sl['id'] == rec), sls[0]['id'])
    for sl in sls: byid[sl['id']]['onroad_group'] = onroad
    if onroad > total and byid[main]['need']:
        byid[main]['need']['onroad_extra'] = onroad - total; byid[main]['need']['vehicles'] += onroad - total

left = collections.Counter((t['line'], t['o'], t['d']) for t in trips if 900 <= t['dep'] < 1080 and t['id'] not in used)
save(dict(network=network, schedule=sched, not_modelled=[dict(line=k[0], o=k[1], d=k[2], n=n) for k, n in sorted(left.items())]),
     os.path.join(DER, S['name'], 'timetable.json'))
print('timetable', S['name'], 'trips', len(trips))
for s in sched:
    n = s['need']
    print(f"  {s['id']:>6} rate {s['rate']}/h: need {n['vehicles'] if n else '?'} (cycle {n['minutes'] if n else '?'}{', +%d on the road' % n['onroad_extra'] if n and n.get('onroad_extra') else ''}), runtime >= {s['min_run']}")
    for r in s['rows']:
        if r.get('untimed'): print(f"        {r['stop'][:24]:24} no timetable, empty back to {r['to']} ({r['run']} min)"); continue
        print(f"        {r['stop'][:24]:24} -> {r['to'][:20]:20} every {r['every']:>2} set {r['set']} real {r['real']} {'turn' if r['loop'] else 'through'} {r['span']}{'' if r['exact'] else f' MISSING {r['missing']} EXTRA {r['extra']} dev {r['dev']}'}")
print('  not modelled:', {f"{k[0]} {k[1]}>{k[2]}": n for k, n in left.items() if n >= 2})
