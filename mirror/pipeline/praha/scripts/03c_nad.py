"""Replacement buses (NAD) for the tram closures of a state -> data/derived/<state>/nad.json

User, 13 Oct: "add the NAD, if any, at the bottom, with a similar style to buses". The state's "nad" block lists the
daytime X lines (PID route_type 3, is_substitute_transport) that stand in for trams on the service date; night lines and
lines of short closures are only named in the block, not modelled.

Per line, the same method as pipeline/praha-bus (its scripts are imported, so the bus rules stay in one place):
  * main stop pattern per direction in 15:00-17:59, headway (16:00 hour), runtime;
  * Simutrans schedule: common.runfit, all bus termini 1 min early (bus sheet rule);
  * buses needed: max(cycle_need at the main terminus pair, buses on the road at once in 16:00-16:59 with the layover
    min(3 min, shortest timetabled turnaround)); a circular line uses the second count only;
  * vehicles: seznam-autobusu.cz records of nad.vehicle_date (courses in order; surplus beyond the need marked
    "not needed", keeping one of every type first); missing courses come from nad.extra_days if the car was not out in
    PID on the vehicle date (day overview); type, garage, livery and pak object from the bus sheet's register and rules.

Usage: python 03c_nad.py --state 2026-10-12
"""
import argparse, collections, csv, datetime, importlib, io, json, os, re, statistics, sys, zipfile
from common import state, load, save, RAW, DER

BUS = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'praha-bus')

def bus_modules():
    """The bus pipeline's common and 04_courses, loaded under their own names (both pipelines have a common.py)."""
    import importlib.util
    def mod(name, file):
        spec = importlib.util.spec_from_file_location(name, os.path.join(BUS, 'scripts', file))
        m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
    bc = mod('bus_common', 'common.py')
    tram_common = sys.modules['common']; sys.modules['common'] = bc       # 04_courses does "from common import ..."
    try: bco = mod('bus_courses', '04_courses.py')
    finally: sys.modules['common'] = tram_common
    return bc, bco

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--state', required=True)
    s = state(ap.parse_args().state); N = s.get('nad')
    if not N: return
    bc, bco = bus_modules()
    g = s['gtfs']; zp = os.path.join(RAW, 'gtfs', g['raw'], 'gtfs.zip'); sd = g['service_date']
    z = zipfile.ZipFile(zp); rd = lambda n: csv.DictReader(io.TextIOWrapper(z.open(n), encoding='utf-8-sig'))
    want = {l['line'] for l in N['lines']}
    routes = {r['route_id']: r['route_short_name'] for r in rd('routes.txt') if r['route_short_name'] in want and r['route_type'] == '3'}
    ops = collections.defaultdict(set)
    for r in rd('route_sub_agencies.txt'):
        if r['route_id'] in routes: ops[routes[r['route_id']]].add(r['sub_agency_name'])
    cal = {r['service_id']: r for r in rd('calendar.txt')}
    cd = collections.defaultdict(dict)
    for r in rd('calendar_dates.txt'): cd[r['service_id']][r['date']] = r['exception_type']
    wd = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'][datetime.date(int(sd[:4]), int(sd[4:6]), int(sd[6:])).weekday()]
    def active(sid):
        e = cd[sid].get(sd)
        if e: return e == '1'
        c = cal.get(sid); return bool(c) and c['start_date'] <= sd <= c['end_date'] and c[wd] == '1'
    trips = {t['trip_id']: t for t in rd('trips.txt') if t['route_id'] in routes and active(t['service_id'])}
    stops = {r['stop_id']: r['stop_name'] for r in rd('stops.txt')}
    st = collections.defaultdict(list)
    for r in rd('stop_times.txt'):
        if r['trip_id'] in trips: st[r['trip_id']].append((int(r['stop_sequence']), stops[r['stop_id']], bc.mins(r['arrival_time']), bc.mins(r['departure_time'])))
    T = collections.defaultdict(list)
    for k, v in st.items():
        v.sort(); seq = [x[1] for x in v]
        seq = [x for i, x in enumerate(seq) if i == 0 or x != seq[i - 1]]      # double entries (arrival + departure stand)
        T[routes[trips[k]['route_id']]].append(dict(o=v[0][1], d=v[-1][1], dep=v[0][3], arr=v[-1][2], stops=seq))

    # vehicles: register + bus livery / pak rules
    V = load(os.path.join(BUS, 'data', 'derived', f'vehicles_{N["register_raw"]}.json'))
    BT = load(os.path.join(BUS, 'assets', 'bus_types.json')); PR = load(os.path.join(BUS, 'assets', 'pak_requested.json'))
    OBJ = load(os.path.join(BUS, 'assets', 'pak_objects.json'))['objects']
    livery = bco.make_livery(V)
    def pak(v):       # = pipeline/praha-bus/scripts/04_courses.py pak()
        liv, why = livery(v); t = v['maker_type']
        tok = (v['operator'] == 'DPP' and PR.get('dpp_type_tokens', {}).get(t)) or PR['type_tokens'].get(t) or re.sub(r'[^A-Za-z0-9]+', '_', t.replace('’', '')).strip('_')
        name = f'VZ-{"DPPraha" if v["operator"] == "DPP" else "Praha"}-{tok}-{liv}-{PR["id_tokens"].get(tok, tok)}'
        chain = [name + '-A', name + '-B'] if (name + '-A' in OBJ or (BT['length_m'].get(t) or 0) >= 17) else [name]
        return dict(object=chain[0], chain=chain, core=PR['id_tokens'].get(tok, tok), livery=liv, mapped=why,
                    status='in pak' if all(c in OBJ for c in chain) else 'requested')
    def car(num, cid):
        v = V.get(cid) if cid else None
        if not v: return dict(num=num, id=cid, type='?', length=None, operator='?', garage='?', paint='', pak=None)
        return dict(num=num, id=cid, type=v['maker_type'], length=BT['length_m'].get(v['maker_type']), operator=v['operator'],
                    garage=v['garage'], paint=v['paint'], pak=pak(v))
    vd = N['vehicle_date']
    ov = os.path.join(RAW, 'vypravenost', vd, 'overview.html')
    busy = set(re.findall(r'/vuz/(\d+)/', open(ov, encoding='utf-8').read())) if os.path.exists(ov) else set()

    out = {}
    for cfg in N['lines']:
        L = cfg['line']; ts = T[L]
        win = [t for t in ts if 900 <= t['dep'] < 1080]
        pats = collections.defaultdict(list)
        for t in win: pats[tuple(t['stops'])].append(t)
        main = []
        for seq, pt in sorted(pats.items(), key=lambda kv: -len(kv[1])):
            if len(pt) < 0.5 * max(len(x) for x in pats.values()): continue
            o, d = seq[0], seq[-1]
            if any((m['o'], m['d']) == (o, d) for m in main): continue
            d16 = sorted(t['dep'] for t in pt if 960 <= t['dep'] < 1020)
            gaps = sorted(b - a for a, b in zip(d16, d16[1:]))
            alld = sorted(t['dep'] for t in ts if (t['o'], t['d']) == (o, d))
            f = bc.runfit(alld, core=(960, 1020))
            sc = dict(every=f['I'], real=list(f['R']), set=bc.loop_shift(f['I'], f['R'], True), exact=True, first=f['first'], last=f['last'], n=f['n']) if f else None
            main.append(dict(o=o, d=d, stops=list(seq), n=len(pt), headway=gaps[len(gaps) // 2] if gaps else None,
                             runtime=round(statistics.median(t['arr'] - t['dep'] for t in pt)), schedule=sc))
        circular = len(main) == 1 and main[0]['o'] == main[0]['d']
        # buses needed (bus sheet rule)
        def lay_at(x):
            m = bc.min_turnaround(ts, x); return min(3, m) if m is not None else 3
        on_road = 0
        for tt in range(960, 1020):
            on_road = max(on_road, sum(1 for t in ts if t['dep'] <= tt < t['arr'] + lay_at(t['d'])))
        cyc = None
        if not circular and len(main) >= 2:
            a, b = main[0]['o'], main[0]['d']
            r = bc.cycle_need_ab(ts, a, b, lay_at(a), lay_at(b)); cyc = r[0] if r else None
        need = max(x for x in (cyc, on_road) if x is not None)
        # courses
        def day(dte):
            p = os.path.join(RAW, 'vypravenost', dte, f'{L}.html')
            return {r['course']: r for r in bco.parse_records(p)} if os.path.exists(p) else {}
        logged = day(vd)
        courses = []
        for k, r in sorted(logged.items(), key=lambda kv: int(kv[0])):
            courses.append(dict(course=k, cars=[car(n, i) for n, i in zip(r['car'].split('+'), r['ids'] + [None] * 3)], source=vd, note=r['note']))
        for dte in N.get('extra_days', []):
            if len(courses) >= need: break
            for k, r in sorted(day(dte).items(), key=lambda kv: int(kv[0])):
                if len(courses) >= need: break
                if any(c['course'] == k for c in courses) or set(r['ids']) & busy: continue
                courses.append(dict(course=k, cars=[car(n, i) for n, i in zip(r['car'].split('+'), r['ids'] + [None] * 3)], source=dte, note=r['note']))
        # surplus: keep one of every type first, then the lowest course numbers
        keep, seen = [], set()
        for c in courses:
            if c['cars'][0]['type'] not in seen: keep.append(c); seen.add(c['cars'][0]['type'])
        for c in courses:
            if len(keep) >= need: break
            if c not in keep: keep.append(c)
        keep = keep[:max(need, len(seen))]
        for c in courses: c['spare'] = c not in keep
        courses.sort(key=lambda c: (c['spare'], int(c['course'])))
        out[L] = dict(cfg, main=main, circular=circular, need=need, need_cycle=cyc, need_on_road=on_road, operators=sorted(ops[L]),
                      courses=courses, counted=sum(1 for c in courses if not c['spare']), first=min(t['dep'] for t in ts), last=max(t['dep'] for t in ts))
        print(L, 'need', need, '(cycle', cyc, 'on road', on_road, ')', 'courses', len(courses), 'counted', out[L]['counted'],
              [(m['o'], m['headway'], m['runtime'], m['schedule'] and (m['schedule']['every'], m['schedule']['set'])) for m in main])
    save(dict(lines=out, vehicle_date=vd, not_modelled=N.get('not_modelled', [])), os.path.join(DER, s['name'], 'nad.json'))

if __name__ == '__main__':
    main()
