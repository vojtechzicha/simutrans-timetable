"""Afternoon-peak fleet for one Plzeň state.

  python 04_fleet.py --state 2026-09-27

seznam-autobusu notes: "ráno" = morning-only car; "odpoledne" = the afternoon car; "ráno i odpoledne" =
split duty; "výměna za X" = this car was replaced by X; "náhrada za Y" = this car replaced Y.
The afternoon car of a kurz is every record that is neither morning-only nor replaced (výměna za).
Writes data/derived/<state>/fleet.json.
"""
import argparse, collections, os
from common import DER, state, load, save

p = argparse.ArgumentParser(); p.add_argument('--state', required=True); a = p.parse_args()
S = state(a.state); FL = S['fleet']
vyp = load(os.path.join(DER, f"vypravenost_{S['vehicles_date']}.json"))
reg = load(os.path.join(DER, f"vehicles_{S['register_date']}.json"))
byk = collections.defaultdict(list)
for r in vyp: byk[(r['line'], r['kurz'])].append(r)
pm, exc, used = [], [], collections.Counter()
for k in sorted(byk, key=lambda k: (int(k[0]), k[1])):
    rs = byk[k]
    keep = [r for r in rs if r['note'] not in FL['morning_notes'] and not r['note'].startswith('výměna za')]
    for r in rs:
        if r not in keep:
            why = 'morning only (ráno)' if r['note'] in FL['morning_notes'] else f"replaced during the day ({r['note']})"
            exc.append(dict(line=k[0], kurz=k[1], cars=r['cars'], ids=r['ids'], why=why))
    assert len(keep) == 1, (k, rs)
    r = keep[0]; n = r['note']
    if n == 'ráno i odpoledne': txt = 'Split duty, out in both peaks.'
    elif n == 'odpoledne':
        m = [x for x in exc if (x['line'], x['kurz']) == k and x['why'].startswith('morning')]
        txt = 'Afternoon car; the morning car on this kurz was ' + ' + '.join(m[0]['cars']) + '.' if m else 'Afternoon car.'
    elif n.startswith('náhrada za'):
        rep = n.replace('náhrada za', '').strip().replace('+', ' + ')
        txt = f'Replacement for {rep} (náhrada). The swap time is not recorded, so the replacement is listed.'
    else: txt = ''
    txt += FL.get('note_extra', {}).get(f'{k[0]}/{k[1]}', '')
    for c in r['cars']: used[c] += 1
    pm.append(dict(line=k[0], kurz=k[1], cars=r['cars'], ids=r['ids'], note=txt, src=n,
                   types=[reg[i]['type'] for i in r['ids']], liveries=[reg[i]['livery'] for i in r['ids']]))
assert all(v == 1 for v in used.values()), [c for c, v in used.items() if v > 1]
for x in exc: x['types'] = [reg[i]['type'] for i in x['ids']]
# spares (user rule, 29 Sep 2026; pipeline/README.md "Roster coverage and spares"): per line keep exactly its need,
# one of every unit type first, afternoon-only kurzy dropped first; the rest leave pm and are listed as "not needed"
import importlib.util as _ilu
_sp = _ilu.spec_from_file_location('tb_common', os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'brno-trolleybus', 'scripts', 'common.py'))
_tb = _ilu.module_from_spec(_sp); _sp.loader.exec_module(_tb)
NEED = load(os.path.join(DER, S['name'], 'timetable.json')).get('sline_need', {})
for l in dict.fromkeys(q['line'] for q in pm):
    grp = [q for q in pm if q['line'] == l]
    for q in grp: q['kurz'] = int(q['kurz'])
    _tb.mark_spares(grp, NEED.get(l), type_of=lambda q: ' + '.join('Škoda ForCity Smart 40T' if t.startswith('Škoda ForCity Smart 40T') else t for t in q['types']))   # 40T0/1/2: one type (one pak object)
spares = [q for q in pm if q.get('spare')]; pm = [q for q in pm if not q.get('spare')]
save(dict(pm=pm, excluded=exc, spares=spares, need=NEED), os.path.join(DER, S['name'], 'fleet.json'))
print('fleet', len(pm), 'trams counted,', len(spares), 'not needed,', sum(len(p['cars']) for p in pm), 'cars; excluded', len(exc))
