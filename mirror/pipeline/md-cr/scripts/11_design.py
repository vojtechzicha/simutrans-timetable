"""MD-CR v3, step 2: build the Simutrans lines from assets/v3_lines.json and data/derived/corridor.json.

For every line it merges the Czech stops of each real train with the foreign stops given in the design file.
It then derives:
  - the timed stops: terminus departures, the first station after the border, and every stay of 5 min or more;
  - the fork values: offset = (real time - 60) mod interval (odd hours first);
  - the round trips and the vehicle count.
Output: data/derived/v3.json (read by 12_render.py) and a readable data/derived/_v3.txt.
Rules: pipeline/rail-design-rules.md.
"""
import json, os
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
DER = os.path.join(BASE, 'data', 'derived')
MIN_TURN = 10      # minutes a train needs at a terminus before it can leave again
LONG_STAY = 5      # stays of this many minutes or more get a timetable entry

NAMES = json.load(open(os.path.join(BASE, 'assets', 'names.json'), encoding='utf-8'))


REPL = sorted(NAMES.get('replace', []), key=lambda r: -len(r[0]))


def full(name):
    for a, b in REPL:
        if a in name:
            name = name.replace(a, b)
    return name


def tmin(s):
    if s is None:
        return None
    h, m = s.split(':')
    return int(h) * 60 + int(m)


def hm(m):
    m = int(round(m))
    return f"{m // 60 % 24}:{m % 60:02d}"


def find_record(corr, num):
    for r in corr:
        if any(s['num'] == num for s in r['stops']):
            return r
    raise SystemExit(f'train {num} not found in corridor.json')


def merged_stops(corr, num, foreign, outbound):
    """Stops of one train in its running order, Czech data plus the foreign leg, with monotonic minutes."""
    rec = find_record(corr, num)
    cz = [{'name': s['name'], 'arr': s['arr'], 'dep': s['dep'], 'req': s['req']} for s in rec['stops']]
    fl = [{'name': n, 'arr': tmin(a), 'dep': tmin(d), 'req': False} for n, a, d in foreign.get(num, [])]
    if fl:
        if outbound:
            names = [f['name'] for f in fl]
            while cz and cz[-1]['name'] in names:
                cz.pop()
            stops = cz + fl
        else:
            names = [f['name'] for f in fl]
            while cz and cz[0]['name'] in names:
                cz.pop(0)
            stops = fl + cz
    else:
        stops = cz
    stops[0]['arr'] = None
    stops[-1]['dep'] = None
    # make times monotonic (overnight runs)
    last = None
    for s in stops:
        for k in ('arr', 'dep'):
            if s[k] is None:
                continue
            v = s[k]
            while last is not None and v < last - 1:
                v += 1440
            s[k] = v
            last = v
    for s in stops:
        s['name'] = full(s['name'])
    return {'num': num, 'cat': rec['cat'], 'stops': stops}


def stays(train, border):
    """Timed stops of one train: (name, arr, dep, reason)."""
    out = []
    for s in train['stops'][1:-1]:
        if s['arr'] is None or s['dep'] is None:
            continue
        stay = s['dep'] - s['arr']
        if stay >= LONG_STAY:
            out.append((s['name'], s['arr'], s['dep'], f'{stay:g} min'))
        elif border and s['name'] == full(border):
            out.append((s['name'], s['arr'], s['dep'], 'first station after the border' + (f', {stay:g} min' if stay else '')))
    return out


def offset(t, interval):
    return int((round(t) - 60) % interval)


def daily_chains(outs, ins):
    """Periodic (1440) vehicle assignment: each arrival takes a departure at the other end (min total wait)."""
    def best(arrs, deps):
        a = sorted(arrs, key=lambda x: x[0] % 1440)
        d = sorted(deps, key=lambda x: x[0] % 1440)
        n = len(a)
        assert n == len(d), 'line needs the same number of trains each way'
        best = None
        for k in range(n):
            pairs, tot = [], 0
            for j in range(n):
                ta, ia = a[j]
                td, idd = d[(j + k) % n]
                w = (td - ta) % 1440
                if w < MIN_TURN:
                    w += 1440
                pairs.append((ia, idd, w))
                tot += w
            if best is None or tot < best[0]:
                best = (tot, pairs)
        return best
    # arrivals at B = out trains' end, departures at B = in trains' start
    arrB = [(t['stops'][-1]['arr'], ('out', i)) for i, t in enumerate(outs)]
    depB = [(t['stops'][0]['dep'], ('in', i)) for i, t in enumerate(ins)]
    arrA = [(t['stops'][-1]['arr'], ('in', i)) for i, t in enumerate(ins)]
    depA = [(t['stops'][0]['dep'], ('out', i)) for i, t in enumerate(outs)]
    wB, pB = best(arrB, depB)
    wA, pA = best(arrA, depA)
    nxt = {}
    for ia, idd, w in pB + pA:
        nxt[ia] = (idd, w)
    run = sum(t['stops'][-1]['arr'] - t['stops'][0]['dep'] for t in outs + ins)
    total = run + wA + wB
    assert total % 1440 == 0, total
    # chains (vehicle cycles)
    seen, cycles = set(), []
    for start in [('out', i) for i in range(len(outs))]:
        if start in seen:
            continue
        cyc, cur = [], start
        while cur not in seen:
            seen.add(cur)
            cyc.append((cur, nxt[cur][1]))
            cur = nxt[cur][0]
        cycles.append(cyc)
    return total // 1440, cycles


def main():
    design = json.load(open(os.path.join(BASE, 'assets', 'v3_lines.json'), encoding='utf-8'))
    corr = json.load(open(os.path.join(DER, 'corridor.json'), encoding='utf-8'))
    result = []
    txt = []
    for ln in design['lines']:
        fo = ln.get('foreign', {})
        outs = [merged_stops(corr, n, fo, True) for n in ln['out']]
        ins = [merged_stops(corr, n, fo, False) for n in ln['in']]
        iv = ln['interval']
        rep_o = next(t for t in outs if t['num'] == ln.get('rep_out', outs[0]['num']))
        rep_i = next(t for t in ins if t['num'] == ln.get('rep_in', ins[0]['num']))
        A, B = rep_o['stops'][0]['name'], rep_o['stops'][-1]['name']
        for t in (outs if iv == 1440 else []):
            assert t['stops'][0]['name'] == A and t['stops'][-1]['name'] == B, (ln['id'], t['num'], t['stops'][0]['name'], t['stops'][-1]['name'])
        for t in (ins if iv == 1440 else []):
            assert t['stops'][0]['name'] == B and t['stops'][-1]['name'] == A, (ln['id'], t['num'], t['stops'][0]['name'], t['stops'][-1]['name'])
        stations = [{'name': s['name'], 'req': s['req']} for s in rep_o['stops']]

        # timetable entries
        entries = []
        def add(stop, direction, times, stay, arrs=None):
            times = sorted(set(int(round(t)) % 1440 for t in times))
            if iv == 1440:
                offs = [offset(t, iv) for t in times]
                entries.append({'stop': stop, 'dir': direction, 'every': iv, 'offset': offs[0], 'also': offs[1:],
                                'real': [hm(t) for t in times], 'stay': stay})
            else:
                t = times[0]
                lab = ('L' if (t // 60) % 2 == 1 else 'S') + f":{t % 60:02d}"
                entries.append({'stop': stop, 'dir': direction, 'every': iv, 'offset': offset(t, iv), 'also': [],
                                'real': [lab], 'stay': stay})
        towards_B, towards_A = 'towards ' + B, 'towards ' + A
        use_o = outs if iv == 1440 else [rep_o]
        use_i = ins if iv == 1440 else [rep_i]
        add(A, towards_B, [t['stops'][0]['dep'] for t in use_o], 'terminus')
        # timed stops per direction, in running order
        for group, direction in ((use_o, towards_B), (use_i, towards_A)):
            per = defaultdict(list)
            order = []
            for t in group:
                for name, a, d, why in stays(t, ln.get('border')):
                    if name not in per:
                        order.append(name)
                    per[name].append((a, d, why))
            for name in order:
                lst = per[name]
                whys = sorted(set(w for _, _, w in lst))
                add(name, direction, [d for _, d, _ in lst], ' / '.join(whys))
            if direction == towards_B:
                add(B, towards_A, [t['stops'][0]['dep'] for t in use_i], 'terminus')
        # vehicles
        if iv == 1440:
            veh, cycles = daily_chains(outs, ins)
            rt = None
        else:
            t0 = rep_o['stops'][0]['dep']
            tb = rep_o['stops'][-1]['arr']
            bslot = rep_i['stops'][0]['dep'] % iv
            nb = tb + MIN_TURN
            nb = nb + ((bslot - nb) % iv)
            ta = nb + (rep_i['stops'][-1]['arr'] - rep_i['stops'][0]['dep'])
            aslot = t0 % iv
            na = ta + MIN_TURN
            na = na + ((aslot - na) % iv)
            cyc = na - t0
            veh = cyc // iv
            cycles = None
            rt = {'t0': t0, 'arrB': tb, 'depB': nb, 'arrA': ta, 'depA': na, 'cycle': cyc}
        line = dict(ln)
        line.update({'A': A, 'B': B, 'stations': stations, 'entries': entries, 'vehicles': veh,
                     'outs': outs, 'ins': ins, 'cycles': cycles, 'rt': rt})
        result.append(line)
        txt.append(f"{ln['id']}: {A} – {B}  every {iv}  vehicles {veh}")
        for e in entries:
            txt.append(f"   {e['stop']:28} {e['dir']:36} off {e['offset']:>4} also {e['also']} real {e['real']} ({e['stay']})")
        if cycles:
            for c in cycles:
                txt.append('   cycle: ' + ' → '.join(f"{k[0]}{(outs if k[0]=='out' else ins)[k[1]]['num']} wait {w}" for k, w in c))
        if rt:
            txt.append(f"   round trip: {rt}")
    json.dump({'lines': result, 'not_modelled': design['not_modelled']}, open(os.path.join(DER, 'v3.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    open(os.path.join(DER, '_v3.txt'), 'w', encoding='utf-8').write('\n'.join(txt) + '\n')
    print('\n'.join(txt))


if __name__ == '__main__':
    main()
