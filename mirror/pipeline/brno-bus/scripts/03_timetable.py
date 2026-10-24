"""Timetable for one network state: network table, schedule fits, Simutrans rows and sizes (Brno buses).

  python 03_timetable.py --state 2026-09-29

The trolleybus 03_timetable.py with three bus additions:
- entries may be minute subsets of a leg ({"mod": 60, "keep": [..]}) for lines that alternate between branches;
- "empty_return": {stop: [back to stop, minutes]} for one-way peak workings (E50, E75, 77 from Areál Slatina):
  the far end gets no timetable (Departure every 0), and the empty run counts in the cycle;
- through stops: a timing point the bus passes without turning (Úzká on 40, Haškova on 57 + 66) keeps the real
  minute. An entry is a turn when the leg before it came from the stop this one goes to; the state can force
  either with "through" / "turn" (["<line id>|<stop>"]).
Writes data/derived/<state>/timetable.json.
"""
import argparse, collections, math, os, statistics
from common import DER, state, save, gtfs_trips, gtfs_path, circuit_need, turnarounds, runfit, runfit_rate, loop_shift, DIV1440, ROUTE_TYPE, hm

p = argparse.ArgumentParser(); p.add_argument('--state', required=True); a = p.parse_args()
S = state(a.state); F = S['fit']
trips = gtfs_trips(gtfs_path(S), S['service_date'], ROUTE_TYPE)
trips = [t for t in trips if t['line'] in S['line_order'] and not (t['o'].startswith('Vozovna') or t['d'].startswith('Vozovna'))]

# ---- network table: 15:00-18:00 trips per terminus pair --------------------------------------------
network = {}
for line in S['line_order']:
    pairs = collections.defaultdict(list)
    for t in trips:
        if t['line'] == line and 900 <= t['dep'] < 1080: pairs[(t['o'], t['d'])].append(t)
    rows = []
    for (o, d), xs in sorted(pairs.items(), key=lambda kv: -len(kv[1])):
        ts = sorted(x['dep'] for x in xs); gaps = [b - a for a, b in zip(ts, ts[1:])]
        rows.append(dict(o=o, d=d, n3h=len(xs), m16=[x - 960 for x in ts if 960 <= x < 1020],
                         hw=statistics.median(gaps) if gaps else None,
                         run=round(statistics.mean(x['arr'] - x['dep'] for x in xs))))
    network[line] = rows

# ---- Simutrans lines ---------------------------------------------------------------------------------
sched, used = [], set()
for sl in S['simutrans_lines']:
    E = sl['entries']; legs = [tuple(e[:3]) for e in E]
    def entry_deps(e):
        xs = [t for t in trips if (t['line'], t['o'], t['d']) == tuple(e[:3])]
        return [t for t in xs if t['dep'] % e[3]['mod'] in e[3]['keep']] if len(e) > 3 else xs
    # One rate for the whole line: the number of real departures 16:00-16:59 that most entries have (on a tie the
    # lower, as the other end can't return more). The 16:00 hour is the reference hour of the shared rules.
    hour = {i: sorted(t['dep'] for t in entry_deps(e) if 960 <= t['dep'] < 1020) for i, e in enumerate(E)}
    cnt = collections.Counter(len(h) for h in hour.values() if h); top = max(cnt.values())
    rate = sl.get('rate') or min(r for r, n in cnt.items() if n == top)
    def pattern_hour(I, R):                           # the pattern's departures 16:00-16:59
        return sorted(m for m in range(960, 1020) if m % I in R)
    rows = []
    for i, e in enumerate(E):
        l, o, d = e[:3]
        xs = entry_deps(e); D = [t['dep'] for t in xs]
        used |= {t['id'] for t in xs}
        key = '|'.join([sl['id'], l, o, d])
        H = hour[i]
        if key in F['overrides']:
            ov = F['overrides'][key]; f = dict(I=ov['I'], R=ov['R'], first=ov['first'], last=ov['last'])
        else:
            # the longest exact run at the line's rate that reproduces the whole 16:00 hour; tried on the shared
            # core first, then on the 16:00 hour itself; failing both, the 16:xx minutes repeated hourly
            f = None
            for core in (tuple(F['core']), (960, 1020)):
                for g in (runfit(D, DIV1440, core), runfit_rate(D, rate, DIV1440, core)):
                    if g and len(g['R']) * 60 == rate * g['I'] and pattern_hour(g['I'], set(g['R'])) == H:
                        f = g; break
                if f: break
            if not f and len(H) == rate:
                f = dict(I=60, R=sorted(m % 60 for m in H), first=H[0], last=H[-1])
            if not f:                                  # the 16:xx departures differ from the line's rate
                g = runfit_rate(D, rate, DIV1440, (960, 1020)) or runfit(D, DIV1440, (960, 1020))
                f = g
        I, R = f['I'], list(f['R'])
        # report the exact run that holds the 16:00 hour (a fit found elsewhere, e.g. 48 at 14:04-15:04, still
        # reproduces 16:xx when repeated; its printed span should say so)
        Dset = set(D); Rs = set(R); lo_, hi_ = 960, 1019
        while lo_ - 1 >= 780 and ((lo_ - 1) in Dset) == ((lo_ - 1) % I in Rs): lo_ -= 1
        while hi_ + 1 < 1200 and ((hi_ + 1) in Dset) == ((hi_ + 1) % I in Rs): hi_ += 1
        run16 = [m for m in sorted(Dset) if lo_ <= m <= hi_]
        if all((m in Dset) == (m % I in Rs) for m in range(960, 1020)) and len(run16) >= 2:
            f = dict(f, first=run16[0], last=run16[-1])
        P = pattern_hour(I, set(R))
        missing = [m for m in H if m not in P]; extra = [m for m in P if m not in H]
        prev = legs[i - 1] if len(legs) > 1 else None
        turn = prev is None or prev[1] == d or o == d or (prev[0], prev[1]) == (l, d)
        tag = f"{sl['id']}|{o}"
        if tag in S.get('through', []): turn = False
        if tag in S.get('turn', []): turn = True
        if len(legs) == 1 and o != d: turn = True
        run = round(statistics.mean(t['arr'] - t['dep'] for t in xs if 900 <= t['dep'] < 1080))
        rows.append(dict(line=l, stop=o, to=d, every=I, real=R, set=loop_shift(I, R, turn), loop=turn,
                         perh=len(R) * 60 / I, span=f"{hm(f['first'])}–{hm(f['last'])}", run=run,
                         exact=not missing and not extra, missing=[m - 960 for m in missing], extra=[m - 960 for m in extra],
                         hour=[m - 960 for m in H], deps=sorted(x for x in D if 900 <= x < 1080)))
    links = dict(S.get('links', {})); links.update(sl.get('empty_return', {}))
    for st, (back, mn) in sl.get('empty_return', {}).items():
        rows.append(dict(line=sl['id'].split('+')[0].rstrip('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz') or sl['id'],
                         stop=st, to=back, every=0, real=[], set=[], loop=False, untimed=True, perh=0, span='', run=mn,
                         exact=True, deps=[]))
    # circuit_need works on (line, from, to) legs; an entry that is a minute subset of a leg gets its own copy
    # of those trips under a private line name, so each entry counts only its own departures
    own, klegs = [], []
    for i, e in enumerate(E):
        tag = f"{e[0]}#{i}"; own += [dict(t, line=tag) for t in entry_deps(e)]; klegs.append((tag, e[1], e[2]))
    lay = turnarounds(own, klegs, S.get('turnaround_default', 3), links) if len(klegs) > 1 else {0: S.get('turnaround_default', 3)}
    for st in sl.get('empty_return', {}):                 # after an empty run the bus leaves at the next slot
        for i in range(len(klegs)):
            if klegs[i - 1][2] == st: lay[i] = 0
    wait = max(30, max(r['every'] for r in rows))          # never wait longer than the line's own interval (or 30 min)
    need = circuit_need(own, klegs, lay=lay, links=links, period=sl.get('period'), maxwait=wait)
    sched.append(dict(id=sl['id'], name=sl['name'], rate=rate, note=sl.get('note', ''), kind=sl.get('kind', ''),
                      text=sl.get('text', ''), rows=rows,
                      min_run=math.ceil(sum(r['run'] * (r['perh'] or rate) / 60 for r in rows)),
                      need=dict(vehicles=need[0], minutes=need[1]) if need else None))

# "On the road" (the Prague/Ostrava bus rule): per record group, the most trips holding a bus at once 16:00-16:59,
# each from departure to arrival + layover, the layover being min(3, the terminus's shortest timetabled turnaround
# 15:00-18:00). Need = max(circuit need, on the road); the extra goes to the group's main line. It catches workings
# folded into another line (75: 3 by cycle, 4 on the road).
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
        gaps = [next((d for d in dep if d >= a), a + 99) - a for a in arr]
        lay[st] = min(3, min(gaps)) if gaps else 3
    onroad = max(sum(1 for t in ts if t['dep'] <= m < t['arr'] + lay[t['d']]) for m in range(960, 1020))
    total = sum((byid[sl['id']]['need'] or {}).get('vehicles') or byid[sl['id']]['min_run'] for sl in sls)
    main = next((sl['id'] for sl in sls if sl['id'].startswith(rec)), sls[0]['id'])
    if onroad > total and byid[main]['need']:
        byid[main]['need']['onroad_extra'] = onroad - total; byid[main]['need']['vehicles'] += onroad - total

# trips in 15:00-18:00 not covered by any Simutrans line (for the "Not modelled" list)
left = collections.Counter((t['line'], t['o'], t['d']) for t in trips if 900 <= t['dep'] < 1080 and t['id'] not in used)
save(dict(network=network, schedule=sched, not_modelled=[dict(line=k[0], o=k[1], d=k[2], n=n) for k, n in sorted(left.items())]),
     os.path.join(DER, S['name'], 'timetable.json'))
print('timetable', S['name'], 'trips', len(trips))
for s in sched:
    n = s['need']
    print(f"  {s['id']:>6} rate {s['rate']}/h: need {n['vehicles'] if n else '?'} (cycle {n['minutes'] if n else '?'}), runtime >= {s['min_run']}")
    for r in s['rows']:
        if r.get('untimed'): print(f"        {r['stop'][:24]:24} no timetable, empty back to {r['to']} ({r['run']} min)"); continue
        print(f"        {r['stop'][:24]:24} -> {r['to'][:20]:20} every {r['every']:>2} set {r['set']} real {r['real']} {'turn' if r['loop'] else 'through'} {r['span']}{'' if r['exact'] else f' MISSING {r["missing"]} EXTRA {r["extra"]}'}")
print('  not modelled:', {f"{k[0]} {k[1]}>{k[2]}": n for k, n in left.items() if n >= 2})
