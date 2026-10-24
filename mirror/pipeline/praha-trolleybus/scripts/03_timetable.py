"""GTFS -> routes, Simutrans schedules and tram counts -> data/derived/<state>/timetable.json

For every tram line on the service date:
  * patterns = (first stop, last stop) of the trips departing 15:00-17:59 (loop stops merged by stop_aliases).
    Main patterns have at least half as many departures as the line's busiest pattern; the rest are depot
    runs (a depot at either end) or short workings, listed as "not modelled".
  * route header: headway = median gap of the 16:00-16:59 departures, runtime = median 15:00-17:59.
  * schedule: common.runfit (the shared rule in pipeline/README.md) on the pattern's departures 13:00-20:00;
    if nothing fits, common.best_offset (approximate, largest deviation shown).
    Loop termini (assets/termini.json kind == "loop") get the values to type in = real - 1 (mod interval).
  * trams at 16:00: common.chain_at on the line's trips (and on each pool's lines together; FIFO chaining
    tends to overcount where layovers are long), the minimum by runtime (round trip / headway, rounded up),
    and the cycle need (shared rule, common.cycle_need from pipeline/brno): follow a tram leaving around 16:00
    round the line, taking the first departure at least 3 min after each arrival; the departures in that round
    trip = trams needed (worst of both directions). Split lines (state "splits") get one need per branch.

Usage: python 03_timetable.py --state 2026-09-27
"""
import argparse, collections, math, os, statistics
from common import state, load, save, RAW, DER, ASSETS, gtfs_trips, chain_at, runfit, best_offset, loop_shift, cycle_need, pool_need

WIN = (900, 1080)          # 15:00-17:59, the peak window shown on the sheet

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--state', required=True)
    s = state(ap.parse_args().state); g = s['gtfs']
    alias = s.get('stop_aliases', {}); n = lambda x: alias.get(x, x)
    dstops = s.get('depot_stops', {'prefix': ['Vozovna'], 'names': []})
    isdep = lambda x: any(x.startswith(p) for p in dstops.get('prefix', [])) or x in dstops.get('names', [])
    kinds = load(os.path.join(ASSETS, 'termini.json'))['termini']
    trips = [t for t in gtfs_trips(os.path.join(RAW, 'gtfs', g['raw'], 'gtfs.zip'), g['service_date'], route_type=s.get('route_type', '0')) if t['line'].isdigit() and int(t['line']) < s.get('night_from', 90)]
    for t in trips: t['o'], t['d'] = n(t['o']), n(t['d'])
    by_line = collections.defaultdict(list)
    for t in trips: by_line[t['line']].append(t)
    out = {}
    for L, ts in sorted(by_line.items(), key=lambda kv: int(kv[0])):
        win = [t for t in ts if WIN[0] <= t['dep'] < WIN[1]]
        pats = collections.defaultdict(list)
        for t in win: pats[(t['o'], t['d'])].append(t)
        if not pats: continue
        top = max(len(v) for v in pats.values())
        routes, sched, minors = [], [], []
        for (o, d), pt in sorted(pats.items(), key=lambda kv: -len(kv[1])):
            deps = sorted(t['dep'] for t in pt)
            # a short working is its own Simutrans line only if it is a real peak service: >= 3 trips, no depot at
            # either end, AND it runs in the 16:00 reference hour (user, 28 Sep: 3 Nádraží Braník, 9 Hotel Golf and
            # 22 Nad Džbánem end before 16:00 and are not peak trips)
            main_deps = sorted(t['dep'] for t in max(pats.values(), key=len))
            short = (len(pt) < 0.5 * top and len(pt) >= 3 and not (isdep(o) or isdep(d))
                     and any(960 <= x < 1020 for x in deps)
                     # shared rule (Brno, 28 Sep): it must run alongside the main pattern, not be the line's
                     # post-peak form that replaces it -> the main pattern still departs after the short working's last trip
                     and any(x > deps[-1] for x in main_deps))
            if len(pt) < 0.5 * top and not short:
                minors.append(dict(o=o, d=d, deps=deps, depot=isdep(o) or isdep(d), loop=kinds.get(o, {}).get('kind') == 'loop'))
                continue
            d16 = [x for x in deps if 960 <= x < 1020]
            gaps = sorted([b - a for a, b in zip(d16, d16[1:])] + ([d16[0] + 60 - d16[-1]] if d16 else []))
            hw = gaps[len(gaps) // 2] if len(gaps) > 1 else None
            rt = round(statistics.median(t['arr'] - t['dep'] for t in pt))
            if not short: routes.append(dict(o=o, d=d, headway=hw, runtime=rt, n=len(pt)))
            alld = sorted(t['dep'] for t in ts if (t['o'], t['d']) == (o, d))
            core = tuple(s.get('fit_core', (930, 990)))
            f = runfit(alld, core=core) if not short else runfit(deps, lo=WIN[0], hi=WIN[1], core=WIN)   # short workings: fit only their peak trips
            loop = kinds.get(o, {}).get('kind') == 'loop'
            ov = s.get('schedule_override', {}).get(L)
            if ov:   # one-vehicle lines with irregular gaps: approximate pattern at a given interval, deviation over 15:00-17:59
                I = ov['every']; off, dev = best_offset(alld, I, lo=WIN[0], hi=WIN[1]); R = [off]; exact = False
                f = dict(first=deps[0], last=deps[-1], n=len(deps))
            elif f:
                I, R = f['I'], f['R']; exact = True; dev = 0
            else:
                I = hw or 60; off, dev = best_offset(alld, I); R = [off]; exact = False
                f = dict(first=deps[0], last=deps[-1], n=len(deps))
            # where the peak window differs from the pattern (inside the pattern's run)
            lo, hi = max(WIN[0], f['first']), min(WIN[1] - 1, f['last'])
            real = {x for x in alld if WIN[0] <= x < WIN[1]}
            slots = {k * I + r for r in R for k in range(1440 // I + 2) if lo <= k * I + r <= hi}
            outside = sorted(x for x in real if not (lo <= x <= hi))
            sched.append(dict(o=o, d=d, short=short, every=I, real=R, set=loop_shift(I, R, loop), loop=loop,
                              kind=kinds.get(o, {}).get('kind', 'unknown'), kind_desc=kinds.get(o, {}).get('description', ''), exact=exact, max_dev=dev, override=(ov or {}).get('why'),
                              first=f['first'], last=f['last'], n=f['n'],
                              missing=sorted(real & set(range(lo, hi + 1)) - slots), extra=sorted(slots - real), outside=outside))
        # tram counts
        c16, _ = chain_at(ts, 960)
        mn = None
        if routes:
            a = routes[0]; b = next((r for r in routes if r['o'] == a['d'] and r['d'] == a['o']), None)
            if a['headway'] and b: mn = math.ceil((a['runtime'] + b['runtime']) / a['headway'])
        cyc = None
        if routes:
            a = routes[0]; bk = next((r for r in routes if r['o'] == a['d'] and r['d'] == a['o']), None)
            if bk:
                lay = s.get('turnaround_min', {}).get(L, 3)
                cs = [cycle_need(ts, a['o'], a['d'], lay=lay), cycle_need(ts, a['d'], a['o'], lay=lay)]
                cs = [x[0] for x in cs if x]
                cyc = max(cs) if cs else None
        out[L] = dict(routes=routes, schedule=sched, minors=minors, chain16=c16, min_runtime=mn, cycle_need=cyc)
    pools = {}
    for k, p in s.get('pools', {}).items():
        pt = [t for l in p['lines'] for t in by_line[l]]
        legs = [tuple(x) for x in p.get('simutrans', {}).get('legs', [])]
        pn = pool_need(pt, legs) if legs else None
        pools[k] = dict(chain16=chain_at(pt, 960)[0], need=pn[0] if pn else None, cycle=pn[1] if pn else None,
                        legs=[list(x) for x in legs], label=p.get('simutrans', {}).get('label'))
    branches = {}
    for key, brs in s.get('splits', {}).items():
        for br in brs:
            x, y = br['route']; ts = by_line[br.get('line', key)]
            lay = s.get('turnaround_min', {}).get(br.get('line', key), 3)
            cs = [c for c in (cycle_need(ts, x, y, lay=lay), cycle_need(ts, y, x, lay=lay)) if c]
            branches.setdefault(key, {})[br['label']] = dict(need=max(c[0] for c in cs) if cs else None,
                                                            cycle=max(c[1] for c in cs) if cs else None, route=br['route'], line=br.get('line', key))
    metro = {}
    m = s.get('metro')
    if m:
        MT = gtfs_trips(os.path.join(RAW, 'gtfs', g['raw'], 'gtfs.zip'), g['service_date'], route_type=m.get('route_type', '1'))
        for L in sorted({t['line'] for t in MT}):
            ts = [t for t in MT if t['line'] == L]
            pats = collections.Counter((t['o'], t['d']) for t in ts if WIN[0] <= t['dep'] < WIN[1])
            top = max(pats.values())
            rows, seen, need, need_hi = [], set(), 0, 0
            for (o, d), cnt in pats.most_common():
                if cnt < 0.3 * top or frozenset((o, d)) in seen: continue      # depot pull-outs / pull-ins (e.g. C from Kačerov)
                seen.add(frozenset((o, d)))
                d16 = sorted(t['dep'] for t in ts if (t['o'], t['d']) == (o, d) and 960 <= t['dep'] < 1020)
                gaps = [b - a for a, b in zip(d16, d16[1:])]
                rt = round(statistics.median(t['arr'] - t['dep'] for t in ts if (t['o'], t['d']) == (o, d) and WIN[0] <= t['dep'] < WIN[1]))
                # Metro termini all reverse behind the station, so the timetable does not show the reversing time
                # (arrival and next departure there are different trains). Give the need for the range in the state.
                rng = m.get('reverse_min', [3, 5])
                by_lay = {}
                for lay in rng:
                    cc = [c for c in (cycle_need(ts, o, d, lay=lay), cycle_need(ts, d, o, lay=lay)) if c]
                    by_lay[lay] = max(c[0] for c in cc) if cc else None
                cs = [c for c in (cycle_need(ts, o, d, lay=rng[0]), cycle_need(ts, d, o, lay=rng[0])) if c]
                n = max(c[0] for c in cs) if cs else None; need += n or 0; need_hi = need_hi + (by_lay[rng[-1]] or 0)
                # Simutrans schedule for both directions (shared fit rule; metro termini reverse on stub tracks -> no loop shift)
                simu = []
                for x, y in ((o, d), (d, o)):
                    dx = sorted(t['dep'] for t in ts if (t['o'], t['d']) == (x, y))
                    f = runfit(dx)
                    if f and f['first'] <= 965 and f['last'] >= 1015:     # exact over (practically) the whole 16:00 hour
                        simu.append(dict(o=x, d=y, every=f['I'], set=list(f['R']), first=f['first'], last=f['last'], n=f['n'], exact=True,
                                         per_hour=sum(1 for t in dx if 960 <= t < 1020)))
                    else:
                        # approximate (shared rule: label the largest deviation): an interval I with k = trains per hour * I / 60
                        # slots (k <= 8); slots = the 16:00-hour departures from 16:00 on, mod I; deviation checked 15:00-17:59
                        h = sorted(t for t in dx if 960 <= t < 1020); win = [t for t in dx if WIN[0] <= t < WIN[1]]; best = None
                        for I in (4, 5, 6, 8, 10, 12, 15, 20, 30, 60):       # same intervals runfit can use
                            k = round(len(h) * I / 60)            # slots per cycle (rounded when the hourly count does not divide)
                            if not 1 <= k <= 8: continue
                            R = sorted({t % I for t in h[:k]})
                            dev = max(min(min((t - r) % I, (r - t) % I) for r in R) for t in win)
                            key = (abs(len(R) * 60 / I - len(h)), dev, I)     # keep the real trains per hour first, then accuracy
                            if best is None or key < best[3]: best = (dev, I, R, key)
                        if best:
                            simu.append(dict(o=x, d=y, every=best[1], set=best[2], exact=False, max_dev=best[0], per_hour=len(h)))
                        else:
                            off, dev = best_offset(dx, 3); simu.append(dict(o=x, d=y, every=3, set=[off], exact=False, max_dev=dev))
                rows.append(dict(o=o, d=d, simutrans=simu, need_by_reverse=by_lay, per_hour=len(d16), gap_min=min(gaps) if gaps else None, gap_max=max(gaps) if gaps else None,
                                 runtime=rt, need=n, cycle=max(c[1] for c in cs) if cs else None))
            minor = [dict(o=o, d=d, n=cnt) for (o, d), cnt in pats.items() if cnt < 0.3 * top]
            metro[L] = dict(patterns=rows, need=need, need_hi=need_hi, reverse_min=rng, chain16=chain_at(ts, 960)[0], depot_runs=minor)
        print('metro', {L: (v['need'], [(p['o'], p['d'], p['per_hour']) for p in v['patterns']]) for L, v in metro.items()})
    print('branches', {k: {l: b['need'] for l, b in v.items()} for k, v in branches.items()})
    save(dict(lines=out, pools=pools, branches=branches, metro=metro, service_date=g['service_date'], gtfs_raw=g['raw']), os.path.join(DER, s['name'], 'timetable.json'))
    for L, v in out.items():
        print(L.rjust(3), 'trams@16', v['chain16'], 'min', v['min_runtime'], 'cycle', v['cycle_need'], [(x['o'][:12], x['every'], x['set'], 'exact' if x['exact'] else f'~{x["max_dev"]}') for x in v['schedule']])
    print('pools', pools)

if __name__ == '__main__':
    main()
