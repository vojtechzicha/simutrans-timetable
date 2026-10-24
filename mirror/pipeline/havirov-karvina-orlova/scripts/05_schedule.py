"""trips -> derived/schedule.json and peaks.json: Simutrans departure settings per line and terminus (fork fields
"Departure every", "Offset", "Also at", "Leave up to"), by the Ostrava bus rules (imported from ostrava-bus/scripts/lib.py
and the tram lib, so they stay in step):
- each line at its own afternoon peak (line_anchor), branches by branch_pairs (peak rule + afternoon rule);
- plans(): both ends of a branch at the same rate, approximate rows flagged with a slower alternative;
- interleave(): branches sharing a terminus fitted on one interval, as the real timetable alternates them.
Every terminus is set as a loop (−1 min), as agreed for all bus sheets on 29 Sep 2026.

Circular lines (Karviná 511, 512, 516, 518, 519: Fryštát, autobusové nádraží → … → Fryštát, autobusové nádraží) have
one terminus. branch_pairs needs two, so they get one branch (a = b) here, one row on the start stop, and no end pairing
(plans' pair check finds the row itself, so the rate always agrees)."""
import collections
from lib import CONFIG, load, save, plans, nm_for, hm, branch_pairs, interleave, line_anchor, simplify_rows, thin_rows

F = CONFIG['fit']; AL = CONFIG['terminus_alias']; DEP = set(CONFIG['depot_stops'])
def al(x): return AL.get(x, x)
trips = load('trips.json'); out = {}; PEAKS = {}; CIRC = {}
for L, tr in trips.items():
    nm = nm_for(L)
    trn = [dict(t, o=al(nm(t['fr'])), d=al(nm(t['to']))) for t in tr]
    PEAKS[L] = A = line_anchor(trn, CONFIG)
    if L in CONFIG.get('anchor_overrides', {}):   # owner rule (Ostrava bus 23, 20 Oct 2026): a line's anchor set by hand
        A.update(anchor=CONFIG['anchor_overrides'][L]['anchor'], moved=True, override=CONFIG['anchor_overrides'][L].get('why', ''))
    T0 = A['anchor']; dl = T0 - CONFIG['peak_minute']
    FL = dict(F, window=[x + dl for x in F['window']], core=[x + dl for x in F['core']])
    chosen = branch_pairs(trn, CONFIG, T0)[0]
    KEEP = {p_ for p_, _ in chosen}
    aft = collections.Counter((t['o'], t['d']) for t in trn if 780 <= t['dep'] < 1140)
    loops = [o for (o, d), n in aft.most_common() if o == d and n >= 3]
    if loops and (not chosen or aft[(loops[0], loops[0])] >= max(len(ts) for _, ts in chosen)):
        CIRC[L] = loops[0]
    # fitted on aliased termini, so both ends of a line pair up for rate matching (Ostrava rule, 20 Oct 2026); rows then get
    # the commonest real stop name back
    nma = lambda s, nm=nm: al(nm(s))
    out[L] = plans(tr, nma, FL, DEP, loop=CONFIG['all_termini_are_loops'], peak=T0,
                   keep=lambda a, b: frozenset((al(a), al(b))) in KEEP or (L in CIRC and al(a) == al(b) == CIRC[L]))
    for r_ in out[L]:
        ts_ = [t for t in tr if nma(t['fr']) == r_['fr'] and nma(t['to']) == r_['to']]
        if ts_:
            r_['fr'] = collections.Counter(nm(t['fr']) for t in ts_).most_common(1)[0][0]
            r_['to'] = collections.Counter(nm(t['to']) for t in ts_).most_common(1)[0][0]
    for r_ in out[L]: r_['_o'], r_['_d'] = al(r_['fr']), al(r_['to'])
    interleave(out[L], trn, chosen, loop=CONFIG['all_termini_are_loops'], peak=T0)
    for r_ in out[L]: r_.pop('_o', None); r_.pop('_d', None)
    for r_ in out[L]:   # the row's own departures in its run, for thin_rows
        if r_.get('every'):
            W_ = r_.get('fitwin') or [min(T0 - 30, r_.get('first', T0)), max(T0 + 90, r_.get('last', T0) + 1)]
            r_['deps_win'] = list(W_)
            r_['deps_'] = [t['dep'] for t in tr if nm(t['fr']) == r_['fr'] and nm(t['to']) == r_['to'] and W_[0] <= t['dep'] < W_[1]]
    simplify_rows(out[L], CONFIG['all_termini_are_loops'])   # "every 60, Offset 17, Also at 47" -> "every 30, Offset 17"; :02 + :03 -> one slot
    thin_rows(out[L], CONFIG['all_termini_are_loops'])       # more slots than real departures (2+ per slot) -> one approximate slot
    for r_ in out[L]: r_.pop('deps_', None); r_.pop('deps_win', None)
    for p in out[L]:
        if p['every']: print(L, p['fr'], '->', p['to'], 'every', p['every'], 'real', p['real'], hm(p['first']), '-', hm(p['last']), 'approx' if 'approx' in p else '')
save('schedule.json', out); save('peaks.json', PEAKS); save('circular.json', CIRC)
print('circular', CIRC)
