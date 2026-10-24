"""MD-CR v4: the simplified clock-face design (assets/v4_lines.json) -> data/derived/v4.json.

Each line copies one real train each way (rep_out, rep_in). slot_A / slot_B move that train to the line's slot.
The timed stops come from those two trains: terminus departures and every stay of 5 min or more.
The round trip uses a 10 min minimum turn and waits for the line's next slot, so it is a whole number of
intervals, and vehicles = round trip / interval.
Offsets: (real time - 60) mod interval, i.e. counted from 01:00 with odd hours first (user, 3 Oct 2026).
Render with: python scripts/12_render.py v4
"""
import copy, json, os, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
DER = os.path.join(BASE, 'data', 'derived')
spec = importlib.util.spec_from_file_location('d11', os.path.join(HERE, '11_design.py'))
d11 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(d11)
MIN_TURN, LONG_STAY = d11.MIN_TURN, d11.LONG_STAY
tmin = d11.tmin


def hm(m):
    m = int(m)  # Czech timetables print the minute rounded down
    return f"{m // 60 % 24}:{m % 60:02d}"


def offset(t, interval):
    return int((int(t) - 60) % interval)


def shift(train, to):
    d = to - train['stops'][0]['dep']
    while d < -720:
        d += 1440
    while d > 720:
        d -= 1440
    return {'num': train['num'], 'cat': train['cat'],
            'stops': [dict(s, arr=None if s['arr'] is None else s['arr'] + d,
                           dep=None if s['dep'] is None else s['dep'] + d) for s in train['stops']]}


HOP = 10  # user, 4 Oct 2026: each station beyond the first foreign one counts 10 min


def extend(rep_o, rep_i, beyond):
    """Run the line on past the first foreign station: each further station 10 min, no dwell."""
    o = {'num': rep_o['num'], 'cat': rep_o['cat'], 'stops': [dict(s) for s in rep_o['stops']]}
    last = o['stops'][-1]
    t = last['arr']
    last['dep'] = t
    for name in beyond:
        t += HOP
        o['stops'].append({'name': name, 'arr': t, 'dep': t, 'req': False})
    o['stops'][-1]['dep'] = None
    i = {'num': rep_i['num'], 'cat': rep_i['cat'], 'stops': [dict(s) for s in rep_i['stops']]}
    first = i['stops'][0]
    t = first['dep']
    first['arr'] = t
    pre = []
    for name in beyond:
        t -= HOP
        pre.insert(0, {'name': name, 'arr': t, 'dep': t, 'req': False})
    pre[0]['arr'] = None
    i['stops'] = pre + i['stops']
    return o, i


DEPOT_RUN = 15   # user, 4 Oct 2026: the odstavné nádraží is 15 min from the hl. n., dwell at the hl. n. and travel together


RAW = None


def raw_locs(num):
    """All locations of a real train from trains.json, depot moves included (no passenger filter)."""
    global RAW
    if RAW is None:
        RAW = json.load(open(os.path.join(DER, 'trains.json'), encoding='utf-8'))
    return next(t for t in RAW if any(l['num'] == num for l in t['locs']))['locs']


def real_depot_ends(starts, ends, hub, name, real):
    """Depot runs with the real times (user, 4 Oct 2026: option 1): the real trains start and end their passenger run
    at `hub` (Praha-Vršovice) and come from / go to the depot `real` (Praha Jih) in the data. Times are taken as
    differences from the hub so slot shifts carry over."""
    st = starts['stops']
    assert st[0]['name'] == hub, (starts['num'], st[0]['name'])
    locs = raw_locs(starts['num'])
    h = next(l for l in locs if d11.full(l['name']) == hub)
    dp = next(l for l in locs if l['name'] == real)
    st[0]['arr'] = st[0]['dep'] - (h['dep'] - h['arr'])
    st.insert(0, {'name': name, 'arr': None, 'dep': st[0]['dep'] - (h['dep'] - dp['dep']), 'req': False})
    st = ends['stops']
    assert st[-1]['name'] == hub, (ends['num'], st[-1]['name'])
    locs = raw_locs(ends['num'])
    h = next(l for l in locs if d11.full(l['name']) == hub)
    dp = next(l for l in locs if l['name'] == real)
    st[-1]['dep'] = st[-1]['arr'] + (h['dep'] - h['arr'])
    st.append({'name': name, 'arr': st[-1]['arr'] + (dp['arr'] - h['arr']), 'dep': None, 'req': False})
    return hub, starts, ends


def depot_ends(rep_o, rep_i, side, depot):
    """Run the line from/to a depot (odstavné nádraží) beyond the hub, the real terminus.
    side 'A' = start of rep_o and end of rep_i; side 'B' = end of rep_o and start of rep_i.
    The hub keeps its real departure (start) or real arrival (end); the depot departs 15 min before the real
    departure and is reached 15 min after the real arrival. No dwell at the hub is invented: the 15 min hold it.
    Real stops beyond the hub (e.g. Praha-Vršovice) are dropped."""
    hub, name = depot['hub'], depot['name']
    starts, ends = (rep_o, rep_i) if side == 'A' else (rep_i, rep_o)
    if depot.get('real'):
        return real_depot_ends(starts, ends, hub, name, depot['real'])
    st = starts['stops']
    i = [x['name'] for x in st].index(hub)
    st[:] = st[i:]
    st[0]['arr'] = st[0]['dep']
    st.insert(0, {'name': name, 'arr': None, 'dep': st[0]['dep'] - DEPOT_RUN, 'req': False})
    st = ends['stops']
    i = [x['name'] for x in st].index(hub)
    st[:] = st[:i + 1]
    st[-1]['dep'] = st[-1]['arr']
    st.append({'name': name, 'arr': st[-1]['arr'] + DEPOT_RUN, 'dep': None, 'req': False})
    return hub, starts, ends


def stop_before(train, station):
    """The stop before `station` in this direction, or None (user, 4 Oct 2026: the stop before Brno hl. n.
    gets a timed entry; the stay at Brno itself stays real and is timed by the usual rule)."""
    st = train['stops']
    for i, s in enumerate(st):
        if s['name'] == station and i > 0:
            return st[i - 1]['name']
    return None


def label(t, iv):
    t = int(t) % 1440
    if iv == 120:
        return ('L' if (t // 60) % 2 == 1 else 'S') + f':{t % 60:02d}'
    if iv == 60:
        return f':{t % 60:02d}'
    times = sorted((t + k * iv) % 1440 for k in range(1440 // iv))
    return ', '.join(hm(x) for x in times)


def main():
    design = json.load(open(os.path.join(BASE, 'assets', 'v4_lines.json'), encoding='utf-8'))
    corr = json.load(open(os.path.join(DER, 'corridor.json'), encoding='utf-8'))
    out, txt = [], []
    for ln in design['lines']:
        fo = ln.get('foreign', {})
        iv = ln['interval']
        def get(nums, outbound):
            res = []
            for n in nums:
                try:
                    res.append(d11.merged_stops(corr, n, fo, outbound))
                except SystemExit:
                    print('   (not in corridor.json, listed only by number):', n)
            return res
        outs = get(ln['out'], True)
        ins = get(ln['in'], False)
        rep_o = copy.deepcopy(next(t for t in outs if t['num'] == ln['rep_out']))  # copies: the real-train lists stay real
        rep_i = copy.deepcopy(next(t for t in ins if t['num'] == ln['rep_in']))
        if ln.get('slot_A'):
            rep_o = shift(rep_o, tmin(ln['slot_A']))
        if ln.get('slot_B'):
            rep_i = shift(rep_i, tmin(ln['slot_B']))
        if ln.get('beyond'):
            rep_o, rep_i = extend(rep_o, rep_i, ln['beyond'])
        before = {id(rep_o): {}, id(rep_i): {}}
        for side, depot in ln.get('depot', {}).items():
            hub, tr, te = depot_ends(rep_o, rep_i, side, depot)
            before[id(tr)][hub] = 'real terminus, real departure' + ('' if depot.get('real') else ' (depot run and dwell 15 min before it)')
            before[id(te)][hub] = ('real terminus, real departure to the depot' if depot.get('real')
                                   else 'real terminus, real arrival (dwell and run to the depot 15 min after it)')
        for station in ln.get('time_before', []):
            for tr in (rep_o, rep_i):
                prev = stop_before(tr, station)
                if prev:
                    before[id(tr)][prev] = f'stop before {station}'
        A, B = rep_o['stops'][0]['name'], rep_o['stops'][-1]['name']
        assert rep_i['stops'][0]['name'] == B and rep_i['stops'][-1]['name'] == A, (ln['id'], rep_i['stops'][0]['name'], rep_i['stops'][-1]['name'])
        entries = []

        def add(stop, direction, t, stay):
            entries.append({'stop': stop, 'dir': direction, 'every': iv, 'offset': offset(t, iv), 'also': [],
                            'real': [label(t, iv)], 'stay': stay})
        tB, tA = 'towards ' + B, 'towards ' + A
        add(A, tB, rep_o['stops'][0]['dep'], 'terminus')
        def timed(train, direction):
            force = dict(ln.get('force_timed', {}))
            force.update(before[id(train)])
            for s in train['stops'][1:-1]:
                if s['arr'] is None or s['dep'] is None:
                    continue
                stay = s['dep'] - s['arr']
                if s['name'] in force:
                    add(s['name'], direction, s['dep'], force[s['name']] + (f", {stay:g} min" if stay else ''))
                elif stay >= LONG_STAY:
                    add(s['name'], direction, s['dep'], f"{stay:g} min")
                elif s['name'] in ln.get('timed', []):  # important stations chosen per line
                    add(s['name'], direction, s['dep'], f"important station, {stay:g} min")
        timed(rep_o, tB)
        add(B, tA, rep_i['stops'][0]['dep'], 'terminus')
        timed(rep_i, tA)
        # round trip
        t0 = rep_o['stops'][0]['dep']
        tb = rep_o['stops'][-1]['arr']
        nb = tb + MIN_TURN
        nb += (rep_i['stops'][0]['dep'] - nb) % iv
        ta = nb + rep_i['stops'][-1]['arr'] - rep_i['stops'][0]['dep']
        na = ta + MIN_TURN
        na += (t0 - na) % iv
        cyc = na - t0
        if ln.get('max_turn_A'):
            assert na - ta <= ln['max_turn_A'], (ln['id'], 'turn at', A, na - ta)
        # stay at the termini (shown in the stay column)
        entries[0]['stay'] = f'terminus, waits {int(na - ta)} min'
        for e in entries:
            if e['stop'] == B and e['stay'] == 'terminus':
                e['stay'] = f'terminus, waits {int(nb - tb)} min'
        line = dict(ln)
        line.update({'A': A, 'B': B, 'stations': [{'name': s['name'], 'req': s['req']} for s in rep_o['stops']],
                     'entries': entries, 'vehicles': int(cyc // iv), 'outs': outs, 'ins': ins,
                     'rep_out_t': rep_o, 'rep_in_t': rep_i, 'cycles': None,
                     'rt': {'t0': t0, 'arrB': tb, 'depB': nb, 'arrA': ta, 'depA': na, 'cycle': cyc}})
        out.append(line)
        txt.append(f"{ln['id']}: {A} – {B} every {iv}: round trip {cyc} min, {int(cyc // iv)} vehicles")
        for e in entries:
            txt.append(f"   {e['stop']:30} {e['dir']:38} off {e['offset']:>4}  {e['real'][0]}  ({e['stay']})")
    json.dump({'meta': design['meta'], 'lines': out, 'not_modelled': design['not_modelled']},
              open(os.path.join(DER, 'v4.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    open(os.path.join(DER, '_v4.txt'), 'w', encoding='utf-8').write('\n'.join(txt) + '\n')
    print('\n'.join(txt))
    print('total vehicles', sum(l['vehicles'] for l in out))


if __name__ == '__main__':
    main()
