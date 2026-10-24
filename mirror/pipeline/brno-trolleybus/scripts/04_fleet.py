"""Afternoon-peak fleet for one state: which vehicle worked each kurz between about 15:00 and 17:00.

  python 04_fleet.py --state 2026-09-29

Rules (as for the trams, see ../README.md): morning-only records (ráno, ranní kurz, pouze ranní služba) are left
out; "odpoledne"/"odpolední kurz" marks the afternoon car; "před výměnou"/"po výměně" keeps the replacement unless
the state resolves the swap. A bus on a trolleybus line (row class car-on-line-bus) is kept, marked, and never
counted as a trolleybus. Kurzy go to Simutrans lines by the state's simutrans_lines (records + kurzy).
Writes data/derived/<state>/fleet.json.
"""
import argparse, collections, os, re
from common import DER, state, load, save, mark_spares

p = argparse.ArgumentParser(); p.add_argument('--state', required=True); a = p.parse_args()
S = state(a.state); FL = S['fleet']
vyp = load(os.path.join(DER, f"vypravenost_{S['vehicles_date']}.json"))
veh = load(os.path.join(DER, f"vehicles_{S['register_date']}.json"))
AM, PM, BOTH = set(FL['morning_notes']), set(FL['afternoon_notes']), set(FL['both_notes'])

by_rec, excluded, used = {}, [], collections.Counter()
for rl in sorted(vyp, key=int):
    byk = collections.defaultdict(list)
    for r in vyp[rl]: byk[r['kurz']].append(r)
    out = []
    for k in sorted(byk, key=int):
        rs = byk[k]; pm = [r for r in rs if r['note'] not in AM]
        for r in rs:
            if r['note'] in AM: excluded.append(dict(line=rl, kurz=int(k), car=r['cars'], why='morning only (' + r['note'] + ')'))
        pre = [r for r in pm if r['note'] == 'před výměnou']; post = [r for r in pm if r['note'] == 'po výměně']
        note = ''
        if pre and post:
            for r in pre: excluded.append(dict(line=rl, kurz=int(k), car=r['cars'], why='replaced during the day (před výměnou)'))
            pm = post
            note = FL['resolved_swaps'].get(f'{rl}/{k}') or \
                f"Swapped during the day; {pre[0]['cars']} ran before the swap. The swap time is not recorded, so the replacement is listed."
        if not pm: continue
        assert len(pm) == 1, (rl, k, pm)
        r = pm[0]; c = r['cars']; v = veh.get(c, {})
        bus = r['traction'] == 'bus'
        if not bus: used[c] += 1
        out.append(dict(kurz=int(k), car=c, type=v.get('type') or v.get('group') or '?', depot=v.get('depot', '?'),
                        livery=v.get('livery', ''), bus=bus, src=r['note'], note=note))
    by_rec[rl] = out
assert all(n == 1 for n in used.values()), [c for c, n in used.items() if n > 1]

# notes: afternoon cars, split duties, buses
where = collections.defaultdict(list)
for rl, o in by_rec.items():
    for u in o: where[u['car']].append(f"{rl}/{u['kurz']}")
morning = collections.defaultdict(list)
for x in excluded:
    if x['why'].startswith('morning'): morning[(x['line'], x['kurz'])].append(x['car'])
for rl, o in by_rec.items():
    for u in o:
        if u['src'] in PM:
            am = morning.get((rl, u['kurz']))
            if am:
                bits = [c + (f" (afterwards on {', '.join(where[c])})" if where.get(c) else '') for c in am]
                u['note'] = 'Afternoon car. Morning: ' + '; '.join(bits) + '.'
            else:
                prev = sorted({f"{x['line']}/{x['kurz']}" for x in excluded if x['why'].startswith('morning') and x['car'] == u['car']})
                u['note'] = 'Afternoon car' + (f", ran {', '.join(prev)} in the morning." if prev else '. No morning record for this kurz.')
        elif u['src'] in BOTH and not u['note']:
            u['note'] = 'Split duty, out in both peaks.'
        if u['bus']:
            u['note'] = (f"Bus on a trolleybus kurz ({u['src']}); counted separately, not as a trolleybus. " + u['note']).strip()
        u['note'] = FL['note_overrides'].get(f"{rl}/{u['kurz']}", u['note'])

# Simutrans lines
lines, taken = {}, set()
for sl in S['simutrans_lines']:
    ks = sl.get('kurzy')
    lines[sl['id']] = [u for u in by_rec.get(sl['records'], []) if ks is None or u['kurz'] in ks]
    taken |= {(sl['records'], u['kurz']) for u in lines[sl['id']]}
TT = load(os.path.join(DER, S['name'], 'timetable.json'))
need = {x['id']: (x['need'] or {}).get('vehicles') or x['min_run'] for x in TT['schedule']}
for o in lines.values():
    for u in o: u['sub'] = u['bus']                   # a substitute bus goes before any trolleybus
spares = {sid: mark_spares(o, need.get(sid)) for sid, o in lines.items()}   # user rule: surplus marked "not needed"
spares = {k: v for k, v in spares.items() if v}
left = [(rl, u['kurz']) for rl, o in by_rec.items() for u in o if (rl, u['kurz']) not in taken]
assert not left, left
save(dict(lines=lines, excluded=excluded, by_record_line={k: len(v) for k, v in by_rec.items()}, spares=spares),
     os.path.join(DER, S['name'], 'fleet.json'))
tb = sum(1 for o in lines.values() for u in o if not u['bus']); bs = sum(1 for o in lines.values() for u in o if u['bus'])
print('fleet', S['name'], tb, 'trolleybuses +', bs, 'buses; per line', {k: len(v) for k, v in lines.items()}, 'excluded', len(excluded))
