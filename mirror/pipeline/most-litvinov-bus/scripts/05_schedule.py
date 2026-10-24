"""trips -> derived/schedule.json: Simutrans departure settings per line and terminus (fork fields "Departure
every", "Offset", "Also at", "Leave up to"), fitted with the shared runfit rule (tram lib, around 15:30–16:30).
Directed variants with fewer than 3 trips in 15:00–18:00 are not scheduled; their minutes are folded into the main
row from the same terminus.
Sparse lines (12, 27, 31): a terminus of a Simutrans line (branch) whose every variant is too thin for that rule gets a wider fit over
15:00–20:00 (runfit, >= 2 departures, one of them in 15:00–18:00), marked "sparse"; where no pattern of at most
60 minutes is exact, the entry keeps "Departure every 0" (no timetable) and the real departures are listed.
Every terminus is set as a loop (−1 min), as agreed for all bus and trolleybus sheets on 29 Sep 2026 (block turns
and turning points included); the real minutes are kept next to the values."""
import collections
from lib import CONFIG, load, save, plans, make_nm, hm, runfit, loop_shift

nm = make_nm(CONFIG); F = CONFIG['fit']; LOOP = CONFIG['all_termini_are_loops']
trips = load('trips.json'); NEEDS = load('needs.json'); out = {}
for L, tr in trips.items():
    ps = plans(tr, nm, F, set(CONFIG['depot_stops']), loop=LOOP)
    g = collections.defaultdict(list)
    for t in tr: g[(nm(t['fr']), nm(t['to']))].append(t['dep'])
    for p in ps:
        if p['every'] or p.get('into'): continue
        if any(q['every'] and q['fr'] == p['fr'] for q in ps): continue
        if not any({p['fr'], p['to']} == {b['a'], b['b']} for b in NEEDS[L]['branches']): continue   # only a Simutrans line's own ends
        deps = sorted(x for x in g[(p['fr'], p['to'])] if F['window'][0] <= x < F['hi'])
        f = runfit(deps, tuple(F['core']), F['window'][0], F['hi'])
        if f and any(F['window'][0] <= x < F['window'][1] and f['first'] <= x <= f['last'] for x in deps):
            p.update(every=f['I'], real=f['R'], set=loop_shift(f['I'], f['R'], LOOP), first=f['first'], last=f['last'], n=f['n'], merged=[], sparse=True)
        else:
            p['all_day'] = deps
    out[L] = ps
    for p in ps:
        if p['every']: print(L, p['fr'], '->', p['to'], 'every', p['every'], 'real', p['real'], 'set', p['set'], hm(p['first']), '-', hm(p['last']), 'SPARSE' if p.get('sparse') else '')
        else: print(L, p['fr'], '->', p['to'], 'not scheduled', [hm(x) for x in p['single']], 'into', p.get('into'), [hm(x) for x in p.get('all_day', [])])
save('schedule.json', out)
