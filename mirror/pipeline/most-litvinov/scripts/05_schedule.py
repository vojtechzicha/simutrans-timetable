"""trips -> derived/schedule.json: fork fields per branch, shared runfit rule around each line's peak
(config.fit per line); every DPmML terminus is a loop, so the values to type in are real minute - 1.
config.schedule_override replaces the fit for a line with designed rows (Most line 1: one tram, every 60);
that line's other branches are then listed as not modelled.
Peak rule (user, 28 Sep 2026): a branch is scheduled only with >= 3 trips in 15:00-17:59 and a departure in
16:00-16:59 (for the morning-only line 3 the same rule is applied to its own morning window)."""
import collections
from lib import CONFIG, load, save, plans, make_nm, hm, loop_shift

nm = make_nm(CONFIG); F = CONFIG['fit']; OV = CONFIG.get('schedule_override', {})
trips = load('trips.json'); out = {}
for L, tr in trips.items():
    fc = F.get(L, F['default'])
    if L in OV:
        rows = [dict(r, set=loop_shift(r['every'], r['real'], CONFIG['all_termini_are_loops']), designed=True, first=None, last=None) for r in OV[L]['rows']]
        keep = {(r['fr'], r['to']) for r in rows}
        g = collections.defaultdict(list)
        for t in tr: g[(nm(t['fr']), nm(t['to']))].append(t['dep'])
        for k, d in g.items():
            if k in keep: continue
            dd = [x for x in d if 780 <= x < 1200]
            if dd: rows.append(dict(fr=k[0], to=k[1], every=None, single=dd, reason='not in the 16:00 peak'))
        out[L] = rows
    else:
        out[L] = plans(tr, nm, fc, set(CONFIG['pullin_branches'].get(L, [])), loop=CONFIG['all_termini_are_loops'])
        a, b = fc['core'][0] + 30, fc['core'][0] + 90       # the peak hour (16:00-16:59, or 06:00-06:59)
        g = collections.defaultdict(list)
        for t in tr: g[(nm(t['fr']), nm(t['to']))].append(t['dep'])
        for p in out[L]:
            if p['every'] and not any(a <= x < b for x in g[(p['fr'], p['to'])]):
                p.update(every=None, single=[x for x in g[(p['fr'], p['to'])] if fc['lo'] <= x < fc['hi']], reason='no departure in the peak hour')
    for p in out[L]:
        if p['every']: print(L, p['fr'], '->', p['to'], 'every', p['every'], 'real', p['real'], 'set', p['set'], 'DESIGNED' if p.get('designed') else f"{hm(p['first'])}-{hm(p['last'])}")
        else: print(L, p['fr'], '->', p['to'], 'not modelled', p.get('reason', ''), [hm(x) for x in p['single']])
save('schedule.json', out)
