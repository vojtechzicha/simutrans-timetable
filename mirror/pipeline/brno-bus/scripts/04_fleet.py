"""Afternoon-peak fleet for one state (Brno buses): which bus worked each kurz between about 15:00 and 17:00.

  python 04_fleet.py --state 2026-09-29

Same record rules as the trolleybus 04_fleet.py (morning-only notes left out, swaps keep the replacement).
Bus additions:
- One DPMB record line can feed several Simutrans lines (49 -> 49M + 49P, 57 -> 57L + 57U + 57V, or a pool such as
  50 -> 50 + 54). Kurzy go to the lines in the state's order: explicit "kurzy" first; the rest, lowest kurz first,
  each line taking what its timetable cycle needs, and the first line keeping any surplus (the operator's slack).
  The records never say which branch a kurz ran, so every such allocation is marked as a choice.
- A Simutrans line whose records fall short is listed with its shortfall ("designed" vehicles come from
  fleet.designed in the state, each checked against that day's records).
Writes data/derived/<state>/fleet.json.
"""
import argparse, collections, os
from common import DER, state, load, save, mark_spares

p = argparse.ArgumentParser(); p.add_argument('--state', required=True); a = p.parse_args()
S = state(a.state); FL = S['fleet']
vyp = load(os.path.join(DER, f"vypravenost_{S['vehicles_date']}.json"))
veh = load(os.path.join(DER, f"vehicles_{S['register_date']}.json"))
TT = load(os.path.join(DER, S['name'], 'timetable.json'))
need = {s['id']: (s['need'] or {}).get('vehicles') or s['min_run'] for s in TT['schedule']}
AM, PM, BOTH = set(FL['morning_notes']), set(FL['afternoon_notes']), set(FL['both_notes'])

def vinfo(c):
    v = veh.get(c, {})
    return dict(type=v.get('type') or v.get('group') or 'not in the register', depot=v.get('depot', '?'),
                livery=v.get('livery', ''), operator=v.get('operator', 'DPMB'))

by_rec, excluded, used = {}, [], collections.Counter()
for rl in vyp:
    byk = collections.defaultdict(list)
    for r in vyp[rl]: byk[r['kurz']].append(r)
    out = []
    for k in sorted(byk, key=int):
        rs = byk[k]; pm = [r for r in rs if r['note'] not in AM]
        for r in rs:
            if r['note'] in AM: excluded.append(dict(line=rl, kurz=int(k), car=r['cars'], why='morning only (' + r['note'] + ')'))
        pre = [r for r in pm if 'před výměnou' in r['note']]; post = [r for r in pm if 'po výměně' in r['note']]
        note = ''
        kb = FL.get('keep_before', {}).get(f'{rl}/{k}')
        if pre and post and kb:                         # the replacement was busy elsewhere in the peak
            for r in post: excluded.append(dict(line=rl, kurz=int(k), car=r['cars'], why='took over after the peak (po výměně)'))
            pm = pre; note = kb
        elif pre and post:
            for r in pre: excluded.append(dict(line=rl, kurz=int(k), car=r['cars'], why='replaced during the day (před výměnou)'))
            pm = post
            note = FL['resolved_swaps'].get(f'{rl}/{k}') or \
                f"Swapped during the day; {pre[0]['cars']} ran before the swap. The swap time is not recorded, so the replacement is listed."
        if not pm: continue
        assert len(pm) == 1, (rl, k, pm)
        r = pm[0]; c = r['cars']; used[c] += 1
        out.append(dict(kurz=int(k), car=c, rec=rl, src=r['note'], note=note, bus=True, **vinfo(c)))
    by_rec[rl] = out
dup = [c for c, n in used.items() if n > 1]
assert not dup, dup

# notes (as for the trolleybuses)
where = collections.defaultdict(list)
for rl, o in by_rec.items():
    for u in o: where[u['car']].append(f"{rl}/{u['kurz']}")
morning = collections.defaultdict(list)
for x in excluded:
    if x['why'].startswith('morning'): morning[(x['line'], x['kurz'])].append(x['car'])
for rl, o in by_rec.items():
    for u in o:
        src = u['src']
        if any(n in src for n in PM) and 'ráno' not in src:
            am = morning.get((rl, u['kurz']))
            if am:
                bits = [c + (f" (afterwards on {', '.join(where[c])})" if where.get(c) else '') for c in am]
                u['note'] = (u['note'] + ' ' if u['note'] else '') + 'Afternoon car. Morning: ' + '; '.join(bits) + '.'
            elif not u['note']:
                prev = sorted({f"{x['line']}/{x['kurz']}" for x in excluded if x['why'].startswith('morning') and x['car'] == u['car']})
                u['note'] = 'Afternoon-only kurz' + (f"; the bus ran {', '.join(prev)} in the morning." if prev else '.')
        elif any(n in src for n in BOTH) and not u['note']:
            u['note'] = 'Split duty, out in both peaks.'
        u['note'] = FL['note_overrides'].get(f"{rl}/{u['kurz']}", u['note'])

# allocate kurzy to Simutrans lines
lines = {sl['id']: [] for sl in S['simutrans_lines']}
alloc_note = {}
groups = collections.defaultdict(list)
for sl in S['simutrans_lines']: groups[sl['records']].append(sl)
for rl, sls in groups.items():
    pool = list(by_rec.get(rl, []))
    for sl in sls:
        if 'kurzy' in sl:
            lines[sl['id']] = [u for u in pool if u['kurz'] in sl['kurzy']]
            pool = [u for u in pool if u['kurz'] not in sl['kurzy']]
    # the record line's own Simutrans lines first (they keep the surplus), then the lines it pools
    auto = sorted((sl for sl in sls if 'kurzy' not in sl), key=lambda sl: not sl['id'].startswith(rl))
    for sl in auto[1:]:                               # later lines take their need first, from the highest kurzy
        take = pool[-need[sl['id']]:] if need[sl['id']] and pool else []
        lines[sl['id']] = sorted(take, key=lambda u: u['kurz']); pool = [u for u in pool if u not in take]
    if auto: lines[auto[0]['id']] += pool
    if len(sls) > 1:
        for sl in sls: alloc_note[sl['id']] = rl
for d in FL.get('designed', []):                     # designed vehicles (state), checked against the day
    assert d['car'] not in used, ('designed car was out that day', d)
    lines[d['line']].append(dict(kurz=d.get('kurz', 0), car=d['car'], rec=d.get('rec', '—'), src='designed', bus=True,
                                 note='Designed, not recorded: ' + d['why'], designed=True, **vinfo(d['car'])))
short = {sid: need[sid] - len(o) for sid, o in lines.items() if need.get(sid) and len(o) < need[sid]}
spares = {sid: mark_spares(o, need.get(sid)) for sid, o in lines.items()}   # user rule: surplus marked "not needed"
spares = {k: v for k, v in spares.items() if v}
save(dict(lines=lines, excluded=excluded, by_record_line={k: len(v) for k, v in by_rec.items()}, split_of=alloc_note, short=short, spares=spares),
     os.path.join(DER, S['name'], 'fleet.json'))
print('fleet', S['name'], sum(len(o) for o in lines.values()), 'buses logged,', sum(spares.values()), 'marked not needed; short:', short)
print('  per line', {k: f"{len(v)}/{need.get(k)}" for k, v in lines.items()})
