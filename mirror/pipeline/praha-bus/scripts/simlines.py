"""Simutrans lines of a card with branches (owner, 28 Oct 2026: "Is it truly one line as you describe? Or are those two
independent lines? Look at Ostrava, that shows it." / "103 will remain one line", "102 stays one line as well, the lines from
109 above will trust your algorithm").

A card's hand-set rows (state schedule_overrides) are grouped into the Simutrans lines the owner types, each sized from its
own schedule, as the Ostrava bus sheet does. The Ostrava bus lib is reused read-only (../../ostrava-bus/scripts/lib.py):
  * state simlines.circuit[L] = row order: one circuit line, owner-set (102, 103);
  * state simlines.auto: rows paired two by two are the separate branch lines; lib.circuitize runs the branches as circuits
    instead where that saves >= 1 bus (owner rule, 20 Oct 2026); it searches at most 8 departures per period.
Sizing: a plain line by lib.slot_need (arrivals matched to departures at each terminus, exact for uneven slots), a circuit by
lib.pattern_need (one bus followed round the entries in running order). Running time = median of the 15:00-17:59 trips.
Minimum wait at a terminus = min(3, its shortest timetabled turnaround in 15:00-17:59), never below 2: departures at loops are
typed 1 min early, so a 0 or 1 min timetabled turn (Dolní Počernice on 109) cannot be driven in the game.
"""
import collections, importlib.util, math, os, statistics

_lib = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'ostrava-bus', 'scripts', 'lib.py')
_spec = importlib.util.spec_from_file_location('ostrava_bus_lib', _lib)
obl = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(obl)

WIN = (900, 1080)
LAY_FLOOR = 2

def build(L, ts, rows, s):
    """ts: the line's trips (o, d, dep, arr); rows: the state's override rows. Returns a list of Simutrans lines, each
    dict(kind, entries=[override-style rows in running order], need, cycle, waits, rts, period), or None."""
    cfg = s.get('simlines', {})
    alias = cfg.get('terminus_alias', {}).get(L, {})
    A = lambda x: alias.get(x, x)
    if L in cfg.get('circuit', {}): mode = 'circuit'
    elif L in cfg.get('auto', []): mode = 'auto'
    else: return None

    def rt(o, d):
        v = [t['arr'] - t['dep'] for t in ts if (t['o'], t['d']) == (o, d) and WIN[0] <= t['dep'] < WIN[1]] or \
            [t['arr'] - t['dep'] for t in ts if (t['o'], t['d']) == (o, d)]
        return round(statistics.median(v))
    deps_at = collections.defaultdict(list)
    for t in ts: deps_at[A(t['o'])].append(t['dep'])
    lay = {}
    for t in ts:
        if not WIN[0] <= t['arr'] < WIN[1]: continue
        n = [x - t['arr'] for x in deps_at[A(t['d'])] if x >= t['arr']]
        if n: lay[A(t['d'])] = min(lay.get(A(t['d']), 3), min(n))
    lay = {k: max(LAY_FLOOR, v) for k, v in lay.items()}
    ly = lambda x: lay.get(A(x), 3)

    def plain(ents):
        P = math.lcm(*[e['every'] for e in ents])
        legs = [(A(e['o']), A(e['d']), sorted({x + k * e['every'] for x in e['real'] for k in range(P // e['every'])}), rt(e['o'], e['d']), ly(e['d'])) for e in ents]
        n, w = obl.slot_need(P, legs)
        return dict(kind='plain', entries=ents, need=n, waits={k: v for k, v in w.items()}, rts=[rt(e['o'], e['d']) for e in ents], period=P,
                    cycle=sum(l[3] * len(l[2]) for l in legs) + sum(sum(v) for v in w.values()))
    def circuit(ents):
        n, cyc, w = obl.pattern_need([dict(every=e['every'], real=e['real']) for e in ents], [rt(e['o'], e['d']) for e in ents], [ly(e['o']) for e in ents])
        return dict(kind='circuit', entries=ents, need=n, cycle=cyc, waits=w, rts=[rt(e['o'], e['d']) for e in ents], period=ents[0]['every'])

    if mode == 'circuit':
        return [circuit([rows[i] for i in cfg['circuit'][L]])]
    pairs = [[rows[i], rows[i + 1]] for i in range(0, len(rows), 2)]
    seps = [plain(p) for p in pairs]
    # circuitize on synthetic trips at the typed slots with the median running time (its own rt takes the max of the trips)
    R = [dict(fr=A(r['o']), to=A(r['d']), every=r['every'], real=r['real']) for r in rows]
    syn = [dict(o=A(r['o']), d=A(r['d']), dep=t, arr=t + rt(r['o'], r['d'])) for r in rows for t in range(840, 1140) if t % r['every'] in r['real']]
    brs = [dict(a=A(p[0]['o']), b=A(p[0]['d']), need=sp['need']) for p, sp in zip(pairs, seps)]
    circ = obl.circuitize(brs, R, syn, lay, 960, lambda x: x)
    if not circ: return seps
    def orig(fr, to):   # the override row behind a leg, by its aliased ends
        return next(r for r in rows if A(r['o']) == fr and A(r['d']) == to)
    out = []
    for c in circ:
        Ys = [g['Y'] for g in c['legs']]; I = c['period']
        if len(set(Ys)) == 1:   # the cycles stay on one branch: a plain line
            ro, rb = orig(c['a'], Ys[0]), orig(Ys[0], c['a'])
            ents = [dict(ro, every=I, real=sorted(g['out_slot'] for g in c['legs'])), dict(rb, every=I, real=sorted(g['back_slot'] for g in c['legs']))]
            for e, r in zip(ents, (ro, rb)):
                if (e['every'], e['real']) != (r['every'], sorted(r['real'])):
                    e['why'] = (f'Every {I} at ' + ', '.join(f':{x:02d}' for x in e['real']) + f'; the other {r["o"]} → {r["d"]} slots run on the circuit.')
            out.append(plain(ents))
        else:
            ents = []
            for k, g in enumerate(c['legs'], 1):
                ro, rb = orig(c['a'], g['Y']), orig(g['Y'], c['a'])
                for r, sl_, txt in ((ro, g['out_slot'], f'Circuit trip {k}'), (rb, g['back_slot'], f'Circuit trip {k}, back')):
                    whole = (r['every'], sorted(r['real'])) == (I, [sl_])   # the leg is the whole row: keep its own note
                    e = dict(o=r['o'], d=r['d'], every=I, real=[sl_], why=f'{txt}: ' + (r['why'] if whole else f'the :{sl_ % 60:02d} departure of the {r["o"]} → {r["d"]} trips.'))
                    if r.get('extra'): e['extra'] = r['extra']
                    ents.append(e)
            out.append(circuit(ents))
    return out
