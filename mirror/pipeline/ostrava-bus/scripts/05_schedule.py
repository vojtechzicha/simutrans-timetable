"""trips -> derived/schedule.json: Simutrans departure settings per line and terminus (fork fields "Departure
every", "Offset", "Also at", "Leave up to"), fitted with the shared runfit rule (tram lib). Directed variants with
fewer than 3 trips in 15:00–18:00, or ending at a depot, are not scheduled; their minutes are merged into the
main row from the same terminus. Every terminus is set as a loop (−1 min), as agreed for all bus and trolleybus
sheets on 29 Sep 2026 (block turns included)."""
import collections
from lib import CONFIG, load, save, plans, make_nm, hm, loop_shift, branch_pairs, interleave, line_anchor, simplify_rows, thin_rows, exactify

nm = make_nm(CONFIG); F = CONFIG['fit']
trips = load('trips.json'); out = {}; PEAKS = {}
for L, tr in trips.items():
    AL = CONFIG['terminus_alias']; al = lambda x: AL.get(x, x)
    trn = [dict(t, o=al(nm(t['fr'])), d=al(nm(t['to']))) for t in tr]
    PEAKS[L] = A = line_anchor(trn, CONFIG)
    if L in CONFIG.get('anchor_overrides', {}):   # owner's anchor for a line the rule keeps at 16:00 by a single departure
        PEAKS[L] = A = dict(A, anchor=CONFIG['anchor_overrides'][L]['anchor'], moved=True, override=CONFIG['anchor_overrides'][L]['why'])
    T0 = A['anchor']; dl = T0 - CONFIG['peak_minute']
    FL = dict(F, window=[x + dl for x in F['window']], core=[x + dl for x in F['core']])
    KEEP = {p_ for p_, _ in branch_pairs(trn, CONFIG, T0)[0]}      # every branch (Simutrans line) gets its own rows
    # fitted on aliased termini, so both ends of a line pair up for rate matching (owner, 20 Oct 2026, 31: out to Nová huť
    # jižní brána, back from Nová huť garáže; 49/54: sad Boženy Němcové / Vozovna trolejbusů); rows then get the real stop
    nma = lambda s: al(nm(s))
    out[L] = plans(tr, nma, FL, set(CONFIG['depot_stops']), loop=CONFIG['all_termini_are_loops'], peak=T0,
                   keep=lambda a, b: frozenset((al(a), al(b))) in KEEP)
    for r_ in out[L]:
        ts_ = [t for t in tr if nma(t['fr']) == r_['fr'] and nma(t['to']) == r_['to']]
        if ts_:
            r_['fr'] = collections.Counter(nm(t['fr']) for t in ts_).most_common(1)[0][0]
            r_['to'] = collections.Counter(nm(t['to']) for t in ts_).most_common(1)[0][0]
    for r_ in out[L]: r_['_o'], r_['_d'] = al(r_['fr']), al(r_['to'])
    interleave(out[L], trn, branch_pairs(trn, CONFIG, T0)[0], loop=CONFIG['all_termini_are_loops'], peak=T0)
    for r_ in out[L]: r_.pop('_o', None); r_.pop('_d', None)
    if L in CONFIG.get('line_overrides', {}):          # owner's model (bus 41 at 14:00): rows as set in config
        ov = CONFIG['line_overrides'][L]; rows = []
        for r in ov['schedule']:
            I = r['every']; deps = sorted(t['dep'] for t in tr if nm(t['fr']) == r['fr'] and nm(t['to']) == r['to'] and ov['window'][0] <= t['dep'] <= ov['window'][1])
            rows.append(dict(r, set=loop_shift(I, r['real'], r['loop']), first=deps[0] if deps else ov['window'][0],
                             last=deps[-1] if deps else ov['window'][1], n=len(deps), manual=True))
        out[L] = rows
    for p in out[L]:
        if p['every']: print(L, p['fr'], '->', p['to'], 'every', p['every'], 'real', p['real'], hm(p['first']), '-', hm(p['last']))
# config.schedule_overrides: rows set by hand (owner, 20 Oct 2026: 21 and 81 every 40, interleaved on the shared trunk).
# The fit cell reports how far each real departure in the window (default anchor..+90; 'window' in the row) is from a slot.
# 59 (owner, 21 Oct 2026): both inbound branches had passed Polanka 4 min apart; rows set 25/35 apart on the shared trunk.
for L, rows in CONFIG.get('schedule_overrides', {}).items():
    for r in rows:
        p = next(p for p in out[L] if p['fr'] == r['fr'] and p['to'] == r['to'])
        T0 = PEAKS[L]['anchor']; W = r.get('window') or [T0, T0 + 90]
        I = r['every']; deps = sorted(t['dep'] for t in trips[L] if nm(t['fr']) == r['fr'] and nm(t['to']) == r['to'] and W[0] <= t['dep'] <= W[1])
        slots = [t for t in range(W[0] - I, W[1] + I + 1) if t % I in r['real']]
        dev = max((min(abs(t - x) for t in slots) for x in deps), default=0)
        extra = [x for x in deps if min(abs(t - x) for t in slots) > 3]
        for k in ('approx', 'alt', 'refit', 'interleave', 'fitwin'): p.pop(k, None)
        p.update(every=I, real=r['real'], set=loop_shift(I, r['real'], CONFIG['all_termini_are_loops']), first=deps[0] if deps else W[0],
                 last=deps[-1] if deps else W[1], n=len(deps), override=dict(why=r['why'], dev=dev, extra=extra, window=W, **({'label': r['label']} if r.get('label') else {})))
for L in out:
    T0_ = PEAKS[L]['anchor']; AL_ = CONFIG['terminus_alias']
    ch = exactify(out[L], trips[L], nm, (T0_ - 30, T0_ + 90), CONFIG['all_termini_are_loops'], lambda x: AL_.get(x, x))   # no whole-day reading: local lines are modelled at their afternoon peak (owner, 20 Oct 2026)
    if ch: print('exactified', L, [(r['fr'], r['to'], r['every'], r['real']) for r in ch])
    for r_ in out[L]:   # the row's own departures in its run, for thin_rows
        if r_.get('every'):
            T0_ = PEAKS[L]['anchor']; W_ = r_.get('fitwin') or [min(T0_ - 30, r_.get('first', T0_)), max(T0_ + 90, r_.get('last', T0_) + 1)]
            r_['deps_win'] = list(W_)
            r_['deps_'] = [t['dep'] for t in trips[L] if nm(t['fr']) == r_['fr'] and nm(t['to']) == r_['to'] and W_[0] <= t['dep'] < W_[1]]
    simplify_rows(out[L], CONFIG['all_termini_are_loops'])   # every 60 at :17 and :47 -> every 30; :02 + :03 -> one slot
    thin_rows(out[L], CONFIG['all_termini_are_loops'])
    for r_ in out[L]: r_.pop('deps_', None); r_.pop('deps_win', None)
save('schedule.json', out); save('peaks.json', PEAKS)
