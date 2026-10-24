"""trips -> derived/schedule.json: Simutrans departure settings per line and branch (fork fields
"Departure every", "Offset", "Also at", "Leave up to"), fitted with the shared runfit rule.
Every Ostrava terminus is a loop, so the values to type in are the real minutes - 1."""
from lib import CONFIG, load, save, plans, make_nm, hm

nm = make_nm(CONFIG); F = CONFIG['fit']
trips = load('trips.json'); out = {}
for L, tr in trips.items():
    out[L] = plans(tr, nm, F, set(CONFIG['pullin_branches'].get(L, [])), loop=CONFIG['all_termini_are_loops'], peak=CONFIG['peak_minute'])
    for p in out[L]:
        if p['every']: print(L, p['fr'], '->', p['to'], 'every', p['every'], 'real', p['real'], 'set', p['set'], hm(p['first']), '-', hm(p['last']))
        else: print(L, p['fr'], '->', p['to'], 'not scheduled', [hm(x) for x in p['single']])
save('schedule.json', out)
