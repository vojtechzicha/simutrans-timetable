"""What the VZ pak session (simutrans-custom-czech-pak128-bd) needs -> pipeline/pardubice/pak_request.md.

  python 06_pak_request.py --state 2026-09-29

Every object the sheet needs that is not in assets/pak_installed.json: type x livery, the peak cars (counted at 16:00)
and the other active DPMP cars of that type in that paint, the operator and the length. Nothing is sent: the user
forwards the file. When the pak session reports the objects built, run 00_pak_objects.py and run.py again and the
"requested" marks go away.
"""
import argparse, collections, os, re
from common import BASE, ASSETS, state, load, der

ap = argparse.ArgumentParser(); ap.add_argument('--state', required=True); S = state(ap.parse_args().state)
FL = load(der(S, 'fleet.json')); V = load(der(S, 'vehicles.json'))
PM = load(os.path.join(ASSETS, 'pak_map.json')); INST = load(os.path.join(ASSETS, 'pak_installed.json'))
need = collections.defaultdict(list)
for sid, us in FL['lines'].items():
    for u in us:
        if not u.get('spare') and u['pak']['status'] == 'requested': need[u['pak']['obj']].append((sid, u))

def obj_of(v):
    t = PM['types'].get(v['type'])
    if not t: return None
    liv = t['default']
    for rx, lv, _w in PM['paint_rules']:
        if re.search(rx, v['paint']):
            if lv: liv = lv
            break
    return f"VZ-DPPardubice-{t['token']}-{liv}-{t['core']}"

L = [f"# Pak request: Pardubice (DPMP), {S['title']}", '',
     f"From pipeline/pardubice (state {S['name']}), for the VZ pak session simutrans-custom-czech-pak128-bd. "
     f"Pak checkout read: {INST['pak']} at {INST['commit']}.", '',
     'Operator of every car: Dopravní podnik města Pardubic a.s. (DPMP), the only operator of the city lines. '
     'Naming follows the existing VZ-DPPardubice objects: VZ-DPPardubice-<type>-<livery>-<core>. '
     'Liveries from the seznam-autobusu.cz register (paint field, read ' + S['register_date'] + '). '
     'Full advert wraps (CVR) are mapped to the type\'s normal DPMP livery and need nothing new.', '']
if not need:
    L.append('Nothing to request: every vehicle on the sheet has an installed object.')
for obj, lst in sorted(need.items()):
    u0 = lst[0][1]; t = PM['types'][u0['type']]
    peak = sorted({u['num'] for _, u in lst}, key=int)
    others = sorted({v['num'] for v in V.values() if v['state'] == 'zar' and obj_of(v) == obj and v['num'] not in peak}, key=lambda x: int(x) if x.isdigit() else 0)
    paints = sorted({u['paint'] for _, u in lst} | {v['paint'] for v in V.values() if v['state'] == 'zar' and obj_of(v) == obj})
    L += [f"## {obj}", '',
          f"- Package: {PM['package'][t['mode']]} (next to the existing {t['token']} objects in {', '.join(sorted({k.split('-')[3] for k in INST['objects'] if k.split('-')[2] == t['token']})) or 'no other livery'})",
          f"- Type: {t['full']} ({u0['type']} in the register), {t['m']:g} m, car units {t['len']} like the existing object",
          f"- Livery: {PM['liveries'].get(u0['pak']['livery'], u0['pak']['livery'])} (register paint: {'; '.join(paints)})",
          f"- Cars at the 16:00 peak: {', '.join(peak)} (Simutrans lines {', '.join(sorted({sid for sid, _ in lst}))})",
          f"- Other active DPMP cars in this paint: {', '.join(others) or 'none'}", '']
open(os.path.join(BASE, 'pak_request.md'), 'w', encoding='utf-8').write('\n'.join(L))
print('pak_request.md:', len(need), 'objects requested:', ', '.join(sorted(need)))
