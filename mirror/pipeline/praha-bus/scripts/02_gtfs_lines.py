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

WIN = (900, 1080)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--state', required=True)
    s = state(ap.parse_args().state); g = s['gtfs']; lo, hi = s['licence_range']
    z = zipfile.ZipFile(os.path.join(RAW, 'gtfs', g['raw'], 'gtfs.zip'))
    rd = lambda n: csv.DictReader(io.TextIOWrapper(z.open(n), encoding='utf-8-sig'))
    routes = {r['route_id']: r for r in rd('routes.txt')}
    lic = {}
    for r in rd('route_sub_agencies.txt'):
        n = r['route_licence_number']
        if n.isdigit() and lo <= int(n) <= hi and r['route_id'] in routes:
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
        rs.sort(); seq = []
        for _, sid, _, _ in rs:
            nm = stops[sid]
            if not seq or seq[-1] != nm: seq.append(nm)      # a stop served twice in a row (two stands) counts once
        by_route[trips[tid]['route_id']].append(dict(seq=tuple(seq), o=seq[0], d=seq[-1], dep=mins(rs[0][2]), arr=mins(rs[-1][3]), dir=trips[tid]['direction_id']))
    out = {}
    for rid, info in sorted(lic.items(), key=lambda kv: int(kv[1]['licence'])):
        R = routes[rid]; L = R['route_short_name']; ts = by_route.get(rid, [])
        rec = dict(line=L, licence=info['licence'], route_type=R['route_type'], long_name=R['route_long_name'],
                   operators=sorted(info['operators']), trips=len(ts), night=R.get('is_night') == '1', regional=R.get('is_regional') == '1')
        if not ts:
            rec['status'] = 'no trips on the service date'; out[L] = rec; continue
        peak = [t for t in ts if WIN[0] <= t['dep'] < WIN[1]]
        base = peak or ts; rec['peak'] = bool(peak)
        seqs = collections.Counter((t['dir'], t['seq']) for t in base)
        pats = []
        for (dr, sq), n in seqs.most_common():
            pats.append(dict(dir=dr, o=sq[0], d=sq[-1], n=n, stops=list(sq), all_day=sum(1 for t in ts if t['seq'] == sq)))
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
        out[L] = rec
    save(dict(lines=out, service_date=sd, gtfs_raw=g['raw']), os.path.join(DER, s['name'], 'gtfs_lines.json'))
    print(len(out), 'lines;', sum(1 for r in out.values() if r.get('peak')), 'with peak trips;',
          sum(1 for r in out.values() if not r.get('trips')), 'without trips on', sd)

if __name__ == '__main__':
    main()
