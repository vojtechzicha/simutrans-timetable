"""Timetable for one network state: network table, schedule fits, Simutrans rows and bus needs (Olomouc buses).

  python 03_timetable.py --state 2026-09-29

Follows pipeline/brno-bus/scripts/03_timetable.py (the shared fit rule of pipeline/README.md), with two Olomouc additions:
- "alias" {line: {stop: terminus}}: a stop folded into a nearby terminus of that line (12 and 19 turn at Holice or run on
  to Průmyslová, two stops further; 28 ends at Tržnice, plocha). Applied to the trips before anything else. A trip that
  starts at the folded stop and passes the terminus is fitted at its time there (dep_fit; method check 25 Oct 2026: the
  12 trips from Průmyslová pass Holice 4 min after they start, which had made the Holice row approximate).
- an entry may carry {"merge": [[line, from, to], ...]}: departures of a variant from the same terminus that are run by the
  same buses (25 from Kaufland next to Hlavní nádraží, 21 to Tabulový vrch after 16:30, 14 Ahold to Hlavní nádraží only).
Each entry is fitted at one rate per Simutrans line (the 16:00-16:59 departures most entries share). Where the bus turns,
the values are the real minute - 1; a stop the bus passes without turning (16 at Nové Sady) keeps the real minute.
Need per Simutrans line: circuit_need (cycle_need for N legs, the terminus's own shorter turnaround where the timetable has
one, a round trip waiting longer than max(30 min, the line's interval) skipped). Then, per real line, the larger of the
summed needs and the most buses on the road at once in 16:00-16:59 (each non-depot trip holds its bus until arrival +
min(3 min, the shortest timetabled turnaround at that terminus)); the extra goes to the real line's main Simutrans line.
Writes data/derived/<state>/timetable.json.
"""
import argparse, collections, math, os, statistics
from common import DER, state, save, gtfs_trips, gtfs_path, circuit_need, turnarounds, runfit, runfit_rate, loop_shift, DIV1440, hm

p = argparse.ArgumentParser(); p.add_argument('--state', required=True); a = p.parse_args()
S = state(a.state); F = S['fit']; DEP = set(S['depot_stops']); AL = S.get('alias', {})
raw = gtfs_trips(gtfs_path(S), S['gtfs']['service_date'], '3')
trips = []
for t in raw:
    al = AL.get(t['line'], {})
    o = al.get(t['o'], t['o'])
    fit = t['times'][t['stops'].index(o)] if o != t['o'] and o in t['stops'] else t['dep']   # read at the terminus it passes
    trips.append(dict(t, o=o, d=al.get(t['d'], t['d']), o_real=t['o'], d_real=t['d'], dep_fit=fit))
alltrips = trips
trips = [t for t in trips if not ({t['o'], t['d']} & DEP)]
peak_lines = [sl['records'] for sl in S['simutrans_lines']]

# ---- network table: 15:00-18:00 trips per terminus pair, for every bus line of the day ----------------------
network = {}
for line in sorted({t['line'] for t in alltrips}, key=int):
    pairs = collections.defaultdict(list)
    for t in alltrips:
        if t['line'] == line and 900 <= t['dep'] < 1080: pairs[(t['o_real'], t['d_real'])].append(t)
    rows = []
    for (o, d), xs in sorted(pairs.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        ts = sorted(x['dep'] for x in xs); gaps = [b - a for a, b in zip(ts, ts[1:])]
        rows.append(dict(o=o, d=d, n3h=len(xs), deps=ts, m16=[x - 960 for x in ts if 960 <= x < 1020],
                         hw=statistics.median(gaps) if gaps else None, depot=bool({o, d} & DEP),
                         run=round(statistics.mean(x['arr'] - x['dep'] for x in xs))))
    ds = [t['dep'] for t in alltrips if t['line'] == line]
    network[line] = dict(rows=rows, first=min(ds), last=max(ds), trips=len(ds))

# ---- Simutrans lines ---------------------------------------------------------------------------------------------
sched, used = [], set()
for sl in S['simutrans_lines']:
    E = sl['entries']; legs = [tuple(e[:3]) for e in E]
    def entry_trips(e):
        keys = [tuple(e[:3])] + [tuple(x) for x in (e[3].get('merge', []) if len(e) > 3 else [])]
        return [t for t in trips if (t['line'], t['o'], t['d']) in keys]
    hour = {i: sorted(t['dep_fit'] for t in entry_trips(e) if 960 <= t['dep_fit'] < 1020) for i, e in enumerate(E)}
    cnt = collections.Counter(len(h) for h in hour.values() if h); top = max(cnt.values())
    rate = sl.get('rate') or min(r for r, n in cnt.items() if n == top)
    def pattern_hour(I, R): return sorted(m for m in range(960, 1020) if m % I in R)
    rows = []
    for i, e in enumerate(E):
        l, o, d = e[:3]
        xs = entry_trips(e); D = sorted(set(t['dep_fit'] for t in xs))
        used |= {t['id'] for t in xs}
        H = hour[i]; key = '|'.join([sl['id'], o])
        if key in F['overrides']:
            ov = F['overrides'][key]; f = dict(I=ov['I'], R=ov['R'], first=ov['first'], last=ov['last'])
        else:
            f = None
            for core in (tuple(F['core']), (960, 1020)):
                for g in (runfit(D, DIV1440, core), runfit_rate(D, rate, DIV1440, core)):
                    if g and (len(E) == 1 or len(g['R']) * 60 == rate * g['I']) and pattern_hour(g['I'], set(g['R'])) == H:
                        f = g; break
                if f: break
            if not f and len(H) == rate:
                f = dict(I=60, R=sorted(m % 60 for m in H), first=H[0], last=H[-1])
            if not f:
                f = runfit_rate(D, rate, DIV1440, (960, 1020)) or runfit(D, DIV1440, (960, 1020))
            if not f:                                   # fewer than 2 departures near the peak: the 16:xx minutes hourly
                near = [m for m in D if 900 <= m < 1080]
                m0 = min(near, key=lambda m: abs(m - 990)) if near else 960
                f = dict(I=60, R=[m0 % 60], first=m0, last=m0)
        I, R = f['I'], list(f['R'])
        Dset = set(D); Rs = set(R); lo_, hi_ = 960, 1019
        while lo_ - 1 >= 780 and ((lo_ - 1) in Dset) == ((lo_ - 1) % I in Rs): lo_ -= 1
        while hi_ + 1 < 1200 and ((hi_ + 1) in Dset) == ((hi_ + 1) % I in Rs): hi_ += 1
        run16 = [m for m in sorted(Dset) if lo_ <= m <= hi_]
        if all((m in Dset) == (m % I in Rs) for m in range(960, 1020)) and len(run16) >= 2:
            f = dict(f, first=run16[0], last=run16[-1])
        P = pattern_hour(I, set(R))
        missing = [m for m in H if m not in P]; extra = [m for m in P if m not in H]
        prev = legs[i - 1] if len(legs) > 1 else None
        turn = prev is None or prev[1] == d or o == d or len(legs) == 1
        tag = f"{sl['id']}|{o}"
        if tag in S.get('through', []): turn = False
        if tag in S.get('turn', []): turn = True
        pk = [t for t in xs if 900 <= t['dep'] < 1080] or xs
        run = round(statistics.mean(t['arr'] - t['dep'] for t in pk))
        rows.append(dict(line=l, stop=o, to=d, every=I, real=R, set=loop_shift(I, R, turn), loop=turn,
                         perh=len(R) * 60 / I, span=f"{hm(f['first'])}–{hm(f['last'])}", run=run,
                         exact=not missing and not extra, missing=[m - 960 for m in missing], extra=[m - 960 for m in extra], override=key in F['overrides'],
                         hour=[m - 960 for m in H], deps=[x for x in D if 900 <= x < 1080],
                         merged=[x[1:] for x in (e[3].get('merge', []) if len(e) > 3 else [])]))
    own, klegs = [], []
    for i, e in enumerate(E):
        tg = f"{e[0]}#{i}"; own += [dict(t, line=tg, o=e[1], d=e[2]) for t in entry_trips(e)]; klegs.append((tg, e[1], e[2]))
    lay = turnarounds(own, klegs, S.get('turnaround_default', 3)) if len(klegs) > 1 else {0: S.get('turnaround_default', 3)}
    wait = max(30, max(r['every'] for r in rows))
    need = circuit_need(own, klegs, lay=lay, maxwait=wait)
    how = 'round trip'
    if not need:                                         # no complete round trip near 16:00: buses of the line at 16:00
        need = (1, None); how = 'at least one bus'
    sched.append(dict(id=sl['id'], name=sl['name'], records=sl['records'], rate=rate, note=sl.get('note', ''), text=sl.get('text', ''),
                      rows=rows, min_run=math.ceil(sum(r['run'] * (r['perh'] or rate) / 60 for r in rows)),
                      need=dict(vehicles=need[0], minutes=need[1], how=how, cycle=need[0])))

# ---- on the road (shared rule d): per real line, the most trips holding a bus at once 16:00-16:59 -------------------
grp = collections.defaultdict(list)
for s in sched: grp[s['records']].append(s)
for rec, ss in grp.items():
    ts = [t for t in trips if t['line'] == rec]
    lay = {}
    for st in {t['d'] for t in ts}:
        arr = [t['arr'] for t in ts if t['d'] == st and 900 <= t['arr'] < 1080]
        dep = sorted(t['dep'] for t in ts if t['o'] == st)
        gaps = [next((d for d in dep if d >= a), a + 99) - a for a in arr]
        lay[st] = min(3, min(gaps)) if gaps else 3
    onroad = max(sum(1 for t in ts if t['dep'] <= m < t['arr'] + lay[t['d']]) for m in range(960, 1020))
    total = sum(s['need']['vehicles'] for s in ss)
    for s in ss: s['need']['onroad_line'] = onroad
    if onroad > total:
        main = ss[0]; main['need']['onroad_extra'] = onroad - total; main['need']['vehicles'] += onroad - total

left = collections.Counter((t['line'], t['o_real'], t['d_real']) for t in alltrips
                           if 900 <= t['dep'] < 1080 and t['id'] not in used and t['line'] in peak_lines)
save(dict(network=network, schedule=sched,
          not_modelled=[dict(line=k[0], o=k[1], d=k[2], n=n, depot=bool({k[1], k[2]} & DEP)) for k, n in sorted(left.items(), key=lambda kv: (int(kv[0][0]), kv[0][1:]))]),
     os.path.join(DER, S['name'], 'timetable.json'))
print('timetable', S['name'], 'trips', len(alltrips), 'need', sum(s['need']['vehicles'] for s in sched))
for s in sched:
    n = s['need']
    print(f"  {s['id']:>4} rate {s['rate']}/h: need {n['vehicles']} (cycle {n['cycle']} in {n['minutes']} min, on road {n['onroad_line']}), runtime >= {s['min_run']}")
    for r in s['rows']:
        print(f"        {r['stop'][:24]:24} -> {r['to'][:20]:20} every {r['every']:>2} set {r['set']} real {r['real']} {'turn' if r['loop'] else 'through'} {r['span']}{'' if r['exact'] else f' MISSING {r['missing']} EXTRA {r['extra']}'}")
print('  not modelled:', {f"{k[0]} {k[1]}>{k[2]}": n for k, n in left.items()})
