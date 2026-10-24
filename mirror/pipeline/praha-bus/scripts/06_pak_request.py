"""What the VZ pak session needs for Prague city buses -> data/derived/<state>/pak_request.json (+ a text summary on stdout)

  * VZ-Praha (every operator but DPP): each type x livery seen on a PID city line (100-299) on any recorded day
    (data/raw/vypravenost/*), with the distinct cars seen, their operators, the car count of that type and livery in the
    operators' active fleets, and the object name it gets. Advert wraps and liveries the pak has no slug for are mapped to
    the type's normal livery (04_courses.make_livery) and listed separately.
  * VZ-DPPraha: every type x livery of the active DPP fleet (register state "zar", not museum/service cars) whose object is not in
    the pak yet (the pak rule: the full active DPP fleet is in VZ), with the car count and whether it ran a city line.

Usage: python 06_pak_request.py --state 2026-09-29
"""
import argparse, collections, glob, importlib, os, re
from common import state, load, save, RAW, DER, ASSETS

C = importlib.import_module('04_courses')

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--state', required=True); s = state(ap.parse_args().state)
    V = load(os.path.join(DER, f'vehicles_{s["register_raw"]}.json'))
    PR = load(os.path.join(ASSETS, 'pak_requested.json')); OBJ = load(os.path.join(ASSETS, 'pak_objects.json'))['objects']
    BT = load(os.path.join(ASSETS, 'bus_types.json'))
    livery = C.make_livery(V)
    P = load(os.path.join(DER, s['name'], 'gtfs_lines.json'))['lines']
    bus = {L for L, p in P.items() if p['route_type'] == '3'}

    def objname(v, liv):
        t = v['maker_type']
        tok = (v['operator'] == 'DPP' and PR.get('dpp_type_tokens', {}).get(t)) or PR['type_tokens'].get(t) or re.sub(r'[^A-Za-z0-9]+', '_', t.replace('’', '')).strip('_')
        pkg = 'DPPraha' if v['operator'] == 'DPP' else 'Praha'
        name = f'VZ-{pkg}-{tok}-{liv}-{PR["id_tokens"].get(tok, tok)}'
        art = name + '-A' in OBJ or (BT['length_m'].get(t) or 0) >= 17
        chain = [name + '-A', name + '-B'] if art else [name]
        return chain, all(c in OBJ for c in chain)

    seen = collections.defaultdict(lambda: dict(days=set(), lines=set()))
    days = set()
    for path in glob.glob(os.path.join(RAW, 'vypravenost', '*', '*.html')):
        d = os.path.basename(os.path.dirname(path)); L = os.path.basename(path)[:-5]
        if L not in bus: continue
        for r in C.parse_records(path):
            days.add(d)
            for cid in r['ids']:
                if cid in V: seen[cid]['days'].add(d); seen[cid]['lines'].add(L)

    active = lambda v: v['state'] == 'zar'
    fleet = collections.Counter()
    for v in V.values():
        if active(v): fleet[(v['operator'], v['maker_type'], livery(v)[0])] += 1

    groups = {}
    for cid, x in seen.items():
        v = V[cid]; liv, why = livery(v)
        chain, have = objname(v, liv)
        g = groups.setdefault(chain[0], dict(package='VZ-DPPraha-bus' if v['operator'] == 'DPP' else 'VZ-Praha-bus', type=v['maker_type'],
                                             length_m=BT['length_m'].get(v['maker_type']), livery=liv, objects=chain, in_pak=have,
                                             cars_on_city_lines=0, operators=collections.Counter(), mapped=[], lines=set(), years=set(), cars=[]))
        g['cars'].append(dict(car=v['num'], operator=v['operator'], year=v.get('year', ''), paint=v['paint'], days=len(x['days'])))
        g['cars_on_city_lines'] += 1; g['operators'][v['operator']] += 1; g['lines'] |= x['lines']
        if v.get('year'): g['years'].add(v['year'])
        if why: g['mapped'].append(dict(car=v['num'], operator=v['operator'], paint=v['paint'], why=why))
    for g in groups.values():
        g['fleet_cars'] = {op: fleet[(op, g['type'], g['livery'])] for op in g['operators']}
        g['operators'] = dict(g['operators']); g['lines'] = sorted(g['lines'], key=int); g['years'] = f'{min(g["years"])}-{max(g["years"])}' if g['years'] else ''

    # active DPP fleet types x liveries without an object
    dpp_missing = collections.defaultdict(lambda: dict(cars=0, on_city_lines=0, mapped=0))
    for cid, v in V.items():
        if v['operator'] != 'DPP' or not active(v): continue
        liv, why = livery(v); chain, have = objname(v, liv)
        if have: continue
        m = dpp_missing[(v['maker_type'], liv, chain[0])]
        m['cars'] += 1; m['on_city_lines'] += cid in seen; m['mapped'] += bool(why)
    out = dict(days=sorted(days), pak_commit=load(os.path.join(ASSETS, 'pak_objects.json'))['commit'],
               praha=sorted([g for g in groups.values() if g['package'] == 'VZ-Praha-bus'], key=lambda g: -g['cars_on_city_lines']),
               dpp_seen=sorted([g for g in groups.values() if g['package'] == 'VZ-DPPraha-bus'], key=lambda g: -g['cars_on_city_lines']),
               dpp_missing=[dict(type=t, livery=l, object=o, **m) for (t, l, o), m in sorted(dpp_missing.items(), key=lambda kv: -kv[1]['cars'])])
    save(out, os.path.join(DER, s['name'], 'pak_request.json'))
    print('days', out['days'])
    print(f'VZ-Praha: {len(out["praha"])} type x livery objects, {sum(g["cars_on_city_lines"] for g in out["praha"])} cars')
    for g in out['praha']:
        print(f'  {g["cars_on_city_lines"]:3d} {g["type"]} | {g["livery"]} | {g["length_m"]} m | {g["objects"][0]} | ' +
              ', '.join(f'{o} {n} (fleet {g["fleet_cars"][o]})' for o, n in g['operators'].items()) + f' | {g["years"]}' +
              (f' | mapped: {len(g["mapped"])}' if g['mapped'] else ''))
    print('DPPraha seen but not in the pak:', [(g['type'], g['livery'], g['cars_on_city_lines']) for g in out['dpp_seen'] if not g['in_pak']])
    print('DPPraha active fleet not in the pak:')
    for m in out['dpp_missing']: print(f'  {m["cars"]:3d} {m["type"]} | {m["livery"]} | {m["object"]} | ran city lines {m["on_city_lines"]} | mapped {m["mapped"]}')

if __name__ == '__main__':
    main()
