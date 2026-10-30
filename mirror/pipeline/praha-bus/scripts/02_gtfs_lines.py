"""PID GTFS -> the reference for every Prague bus line in the licence range -> data/derived/<state>/gtfs_lines.json

Lines: routes whose route_licence_number (route_sub_agencies.txt) is in the state's licence range (100100-100299 = PID 100-280).
For each line on the service date:
  * patterns = distinct (first stop, last stop, stop-name sequence) with trip counts, whole day and 15:00-17:59;
  * main patterns = the busiest sequence per direction in the peak (or all day if the line has no peak trips);
  * headway (median 16:00-16:59 gap), runtime (median), vehicles needed at 16:00: the larger of common.cycle_need (3 min layover,
    main terminus pair) and the most buses on the road at once in 16:00-16:59 over all patterns (trip + the terminus layover:
    min(3, the shortest timetabled turnaround there));
    Simutrans values per terminus (common.runfit; every bus terminus is a turn, so loop -1 min like the trolleybuses);
  * operator (sub_agency_name) and route type (3 bus, 11 trolleybus).

Usage: python 02_gtfs_lines.py --state 2026-09-29
"""
import argparse, collections, csv, io, os, statistics, zipfile, datetime
from common import state, save, RAW, DER, mins, runfit, best_offset, loop_shift, cycle_need
import simlines

WIN = (900, 1080)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--state', required=True)
    s = state(ap.parse_args().state); g = s['gtfs']; lo, hi = s['licence_range']
    # regional companions (state "regional", owner 30 Oct 2026): through and pooled lines become trips of their city line's card,
    # interleaved lines get their own card
    RG = s.get('regional', {})
    comp = collections.defaultdict(list)
    for how in ('through', 'pooled'):
        for C, Rs in RG.get(how, {}).items(): comp[C] += [(how, R) for R in Rs]
    inside = {R: C for C, v in comp.items() for _, R in v}
    extra = {'100' + R for R in list(inside) + list(RG.get('interleaved', {}))}
    z = zipfile.ZipFile(os.path.join(RAW, 'gtfs', g['raw'], 'gtfs.zip'))
    rd = lambda n: csv.DictReader(io.TextIOWrapper(z.open(n), encoding='utf-8-sig'))
    routes = {r['route_id']: r for r in rd('routes.txt')}
    lic = {}
    for r in rd('route_sub_agencies.txt'):
        n = r['route_licence_number']
        if n.isdigit() and (lo <= int(n) <= hi or n in extra) and r['route_id'] in routes:
            lic.setdefault(r['route_id'], dict(licence=n, operators=set()))['operators'].add(r['sub_agency_name'])
    sd = g['service_date']
    cal = {r['service_id']: r for r in rd('calendar.txt')}
    cd = collections.defaultdict(dict)
    for r in rd('calendar_dates.txt'): cd[r['service_id']][r['date']] = r['exception_type']
    wd = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'][datetime.date(int(sd[:4]), int(sd[4:6]), int(sd[6:])).weekday()]
    def active(sid):
        e = cd[sid].get(sd)
        if e: return e == '1'
        c = cal.get(sid); return bool(c) and c['start_date'] <= sd <= c['end_date'] and c[wd] == '1'
    trips = {t['trip_id']: t for t in rd('trips.txt') if t['route_id'] in lic and active(t['service_id'])}
    stops = {r['stop_id']: r['stop_name'].replace('\xa0', ' ') for r in rd('stops.txt')}
    st = collections.defaultdict(list)
    for r in rd('stop_times.txt'):
        if r['trip_id'] in trips: st[r['trip_id']].append((int(r['stop_sequence']), r['stop_id'], r['departure_time'], r['arrival_time']))
    by_route = collections.defaultdict(list)
    for tid, rs in st.items():
        rs.sort(); seq = []; tm = []
        for _, sid, dt, _ in rs:
            nm = stops[sid]
            if not seq or seq[-1] != nm: seq.append(nm); tm.append(mins(dt))      # a stop served twice in a row (two stands) counts once
        by_route[trips[tid]['route_id']].append(dict(seq=tuple(seq), tm=tm, o=seq[0], d=seq[-1], dep=mins(rs[0][2]), arr=mins(rs[-1][3]), dir=trips[tid]['direction_id']))
    rid_of = {routes[rid]['route_short_name']: rid for rid in lic if routes[rid]['route_type'] == '3'}
    def with_companions(C, ts):
        """C's trips plus its pooled lines' trips; a through line's trip is joined to the C trip it continues (same stop, same
        minute), so it runs as one trip. Companion trips take C's direction by the terminus they leave or reach."""
        ts = [dict(t) for t in ts]
        dir_from = {}; dir_to = {}
        for t in ts: dir_from.setdefault(t['o'], t['dir']); dir_to.setdefault(t['d'], t['dir'])
        for how, Rl in comp[C]:
            rt = [dict(t, via=Rl) for t in by_route.get(rid_of.get(Rl), [])]
            for t in rt: t['dir'] = dir_from.get(t['o'], dir_to.get(t['d'], t['dir']))
            if how == 'pooled': ts += rt; continue
            used = set()
            for i, c in enumerate(ts):
                if c.get('via'): continue
                j = next((j for j, r in enumerate(rt) if j not in used and r['o'] == c['d'] and r['dep'] == c['arr']), None)
                if j is not None:
                    r = rt[j]; used.add(j); ts[i] = dict(c, seq=c['seq'] + r['seq'][1:], tm=c['tm'] + r['tm'][1:], d=r['d'], arr=r['arr'], via=Rl); continue
                j = next((j for j, r in enumerate(rt) if j not in used and r['d'] == c['o'] and r['arr'] == c['dep']), None)
                if j is not None:
                    r = rt[j]; used.add(j); ts[i] = dict(c, seq=r['seq'] + c['seq'][1:], tm=r['tm'] + c['tm'][1:], o=r['o'], dep=r['dep'], via=Rl)
            ts += [r for j, r in enumerate(rt) if j not in used]
        return ts
    out = {}; TS = {}
    for rid, info in sorted(lic.items(), key=lambda kv: int(kv[1]['licence'])):
        R = routes[rid]; L = R['route_short_name']; ts = by_route.get(rid, [])
        if L in inside and R['route_type'] == '3': continue          # on its city line's card
        if L in comp and R['route_type'] == '3': ts = with_companions(L, ts)
        TS[L] = ts
        rec = dict(line=L, licence=info['licence'], route_type=R['route_type'], long_name=R['route_long_name'],
                   operators=sorted(info['operators']), trips=len(ts), night=R.get('is_night') == '1', regional=R.get('is_regional') == '1')
        if L in comp and R['route_type'] == '3':
            rec['companions'] = [dict(line=Rl, how=how, long_name=routes[rid_of[Rl]]['route_long_name'] if Rl in rid_of else '',
                                      trips=sum(1 for t in ts if t.get('via') == Rl)) for how, Rl in comp[L]]
        if L in RG.get('interleaved', {}): rec['interleaved_with'] = RG['interleaved'][L]
        if not ts:
            rec['status'] = 'no trips on the service date'; out[L] = rec; continue
        peak = [t for t in ts if WIN[0] <= t['dep'] < WIN[1]]
        base = peak or ts; rec['peak'] = bool(peak)
        seqs = collections.Counter((t['dir'], t['seq']) for t in base)
        pats = []
        for (dr, sq), n in seqs.most_common():
            pats.append(dict(dir=dr, o=sq[0], d=sq[-1], n=n, stops=list(sq), all_day=sum(1 for t in ts if t['seq'] == sq)))
            via = collections.Counter(t.get('via') for t in base if (t['dir'], t['seq']) == (dr, sq)).most_common(1)[0][0]
            if via: pats[-1]['via'] = via            # a companion's trips (state "regional"): 03_compare matches its game line to these
        main = {}
        for p in pats:
            main.setdefault(p['dir'], p)                   # busiest sequence per direction
        rec['patterns'] = pats; rec['main'] = [main[k] for k in sorted(main)]
        # headway / runtime / schedule per main direction (by terminus pair so short-turn trips don't mix in)
        for m in rec['main']:
            deps = sorted(t['dep'] for t in ts if (t['o'], t['d']) == (m['o'], m['d']))
            d16 = [x for x in deps if 960 <= x < 1020]
            gaps = sorted(b - a for a, b in zip(d16, d16[1:]))
            m['headway'] = gaps[len(gaps) // 2] if gaps else None
            m['per_hour_16'] = len(d16)
            rts = [t['arr'] - t['dep'] for t in base if t['seq'] == tuple(m['stops'])]
            m['runtime'] = round(statistics.median(rts)) if rts else None
            f = runfit(deps, core=(960, 1020))
            if f:
                m['schedule'] = dict(every=f['I'], real=f['R'], set=loop_shift(f['I'], f['R'], True), exact=True, first=f['first'], last=f['last'], n=f['n'])
            elif deps:
                I = m['headway'] or 60
                w = WIN if any(WIN[0] <= x < WIN[1] for x in deps) else (0, 1800)   # off-peak-only line: whole day
                off, dev = best_offset(deps, I, lo=w[0], hi=w[1])
                m['schedule'] = dict(every=I, real=[off], set=loop_shift(I, [off], True), exact=False, max_dev=dev)
        # hand-set Simutrans rows (state schedule_overrides, method check 25 Oct 2026): they replace the main-pattern rows on the
        # card where the fit broke the shared rules (different rates at the two ends, more slots than departures, or a pair made
        # of two different branches, which then get all their rows). Each row: o, d, every, real (timetable minutes mod every),
        # why; optional extra = peak extras listed in the why and left out of the model (HH:MM), approx = no exact run to show.
        # The exact run (as runfit walks it: no extra departure, no empty slot) and the largest deviation in 15:00-17:59 are
        # worked out here from the trips, so the card can say how well the row fits.
        ov = s.get('schedule_overrides', {}).get(L)
        if ov:
            # cards with branches: the rows grouped into the Simutrans lines the owner types (simlines.py, 28 Oct 2026); a row
            # then counts only the departures nearest its own slots, as its siblings on other lines (same o, d) take the rest
            sls = simlines.build(L, ts, ov['rows'], s)
            ents = [dict(e, sl=k) for k, sl in enumerate(sls) for e in sl['entries']] if sls else ov['rows']
            def near(x, I, R): return min(min((x - y) % I, (y - x) % I) for y in R)
            rows = []
            for o_ in ents:
                I, R = o_['every'], o_['real']; skip = {mins(x) for x in o_.get('extra', [])}
                sib = [e for e in ents if e is not o_ and (e['o'], e['d']) == (o_['o'], o_['d'])]
                deps = sorted(t['dep'] for t in ts if (t['o'], t['d']) == (o_['o'], o_['d']) and t['dep'] not in skip
                              and all(near(t['dep'], I, R) <= near(t['dep'], e['every'], e['real']) for e in sib))
                S = set(deps); pk = [x for x in deps if WIN[0] <= x < WIN[1]]
                runs, a = [], None
                for t in range(780, 1201):                       # maximal stretches where departures and slots agree
                    okm = t < 1200 and ((t in S) == (t % I in R))
                    if okm and a is None: a = t
                    if not okm and a is not None: runs.append([x for x in deps if a <= x < t]); a = None
                runs = [r_ for r_ in runs if len(r_) >= 2]
                run = max(runs, key=lambda r_: (max(0, min(r_[-1] + 1, 1050) - max(r_[0], 930)), len(r_))) if runs and not o_.get('approx') else []
                dev = max((min(abs(x - k * I - y) for y in R for k in range(-1, 1440 // I + 2)) for x in pk), default=0)
                rows.append(dict(o=o_['o'], d=o_['d'], schedule=dict(every=I, real=R, set=loop_shift(I, R, True), exact=False, override=o_['why'], approx=bool(o_.get('approx')),
                                 max_dev=dev, first=run[0] if run else None, last=run[-1] if run else None, n=len(run)), sl=o_.get('sl')))
                via = collections.Counter(t.get('via') for t in ts if (t['o'], t['d']) == (o_['o'], o_['d'])).most_common(1)
                if via and via[0][0]: rows[-1]['via'] = via[0][0]    # the row's trips are a companion's (state "regional")
            rec['schedule_rows'] = rows
            if sls:
                rec['simlines'] = [dict(kind=x['kind'], need=x['need'], cycle=x['cycle'], waits=x['waits'], rts=x['rts'], period=x['period'],
                                        rows=[i for i, r in enumerate(rows) if r['sl'] == k]) for k, x in enumerate(sls)]
        if len(rec['main']) == 2:
            # cycle_need by direction, not by stop name: a terminus often has a separate alighting stop
            # (100: trips end at Letiste and start at Terminal 1), so match the two main terminus pairs as A and B
            a, b = rec['main']
            simple = []
            for t in ts:
                if (t['o'], t['d']) == (a['o'], a['d']): simple.append(dict(o='A', d='B', dep=t['dep'], arr=t['arr']))
                elif (t['o'], t['d']) == (b['o'], b['d']): simple.append(dict(o='B', d='A', dep=t['dep'], arr=t['arr']))
            cs = [c for c in (cycle_need(simple, 'A', 'B'), cycle_need(simple, 'B', 'A')) if c]
            rec['need'] = max(c[0] for c in cs) if cs else None
            rec['cycle'] = max(c[1] for c in cs) if cs else None
        if len(rec['main']) == 1 and rec['main'][0]['o'] == rec['main'][0]['d']:
            m = rec['main'][0]                               # circular line: one loop = runtime + 3 min layover
            rec['circular'] = True
            if m.get('headway') and m.get('runtime'):
                rec['need'] = -(-(m['runtime'] + 3) // m['headway']); rec['cycle'] = m['runtime'] + 3
        # buses on the road: every trip of the line (all patterns) holds a bus from departure to arrival + 3 min, peak count in 16:00-16:59.
        # cycle_need follows only the main terminus pair, so it undercounts lines with branches and short workings (191: 6 vs 15)
        # layover at each terminus = min(3, the shortest timetabled turnaround there in 15:00-18:00), as for cycle_need:
        # a flat +3 overcounts lines that turn in 0-2 min (Ostrava 99: 1 bus, flat +3 said 2; b5 session, 29 Sep)
        deps_at = collections.defaultdict(list)
        for t in ts: deps_at[t['o']].append(t['dep'])
        lay = {}
        for t in ts:
            if not (900 <= t['arr'] < 1080): continue
            nxt = [x - t['arr'] for x in deps_at.get(t['d'], []) if x >= t['arr']]
            if nxt: lay[t['d']] = min(lay.get(t['d'], 3), min(nxt))
        occ = max(sum(1 for t in ts if t['dep'] <= m < t['arr'] + lay.get(t['d'], 3)) for m in range(960, 1020))
        if occ:
            rec['need_cycle'] = rec.get('need'); rec['need_on_road'] = occ
            rec['need'] = max(rec.get('need') or 0, occ)
        if rec.get('simlines'):   # a card with Simutrans lines needs what its lines need, each run on its own buses
            rec['need'] = sum(x['need'] for x in rec['simlines'])
        out[L] = rec
    # interleaved companions: the longest stretch a regional line's peak pattern shares with one of its city line's, touching the
    # regional line's own end, and the two lines' departures merged at the stretch's first stop in 15:00-17:59 (real minutes)
    def peak_pats(L):
        c = collections.Counter(t['seq'] for t in TS.get(L, []) if WIN[0] <= t['dep'] < WIN[1])
        return [p for p, n in c.items() if n >= 3]
    def shared(a, b):
        best = (0, 0, 0)
        for i in range(len(a)):
            for j in range(len(b)):
                k = 0
                while i + k < len(a) and j + k < len(b) and a[i + k] == b[j + k]: k += 1
                if k > best[0]: best = (k, i, j)
        return best
    for Rl, Cs in RG.get('interleaved', {}).items():
        if Rl not in out: continue
        rows = []
        for C in Cs:
            for rp in peak_pats(Rl):
                best = None
                for cp in peak_pats(C):
                    k, i, j = shared(rp, cp)
                    if k >= 3 and (i == 0 or i + k == len(rp)) and (best is None or k > best[0]): best = (k, i, j, cp)
                if not best: continue
                k, i, j, cp = best; run = rp[i:i + k]
                def deps(L, pats):
                    return sorted(t['tm'][t['seq'].index(run[0])] for t in TS[L] if t['seq'] in pats and WIN[0] <= t['tm'][t['seq'].index(run[0])] < WIN[1])
                dr = deps(Rl, {rp}); dc = deps(C, {p for p in peak_pats(C) if any(p[x:x + k] == run for x in range(len(p) - k + 1))})
                both = sorted(dr + dc); gaps = [b - a for a, b in zip(both, both[1:])]
                rows.append(dict(city=C, stops=k, first=run[0], last=run[-1], n_reg=len(dr), n_city=len(dc), gap_min=min(gaps) if gaps else None, gap_max=max(gaps) if gaps else None))
        out[Rl]['interleave'] = rows
        for r_ in rows:
            if r_['city'] in out: out[r_['city']].setdefault('interleaved_by', []).append(dict(r_, line=Rl, long_name=out[Rl]['long_name'], operators=out[Rl]['operators']))
    save(dict(lines=out, service_date=sd, gtfs_raw=g['raw']), os.path.join(DER, s['name'], 'gtfs_lines.json'))
    print(len(out), 'lines;', sum(1 for r in out.values() if r.get('peak')), 'with peak trips;',
          sum(1 for r in out.values() if not r.get('trips')), 'without trips on', sd)

if __name__ == '__main__':
    main()
