"""Shared helpers for the Ostrava bus pipeline (stdlib only).

Reuses the Ostrava tram pipeline's helpers (../../ostrava/scripts/lib.py: parsers, WAF headers, JDF reader and
version rule, blocks, cycle_need, runfit, plans, make_nm) and the trolleybus pipeline's cycle_need_peak
(../../ostrava-trolleybus/scripts/lib.py), and mark_spares from ../../brno-trolleybus/scripts/common.py. Only the paths and the config are this folder's own.
"""
import importlib.util, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))          # pipeline/ostrava-bus
PROJECT = os.path.dirname(os.path.dirname(ROOT))                             # Simutrans-Timetable
def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
tramlib = _load('tramlib', os.path.join(os.path.dirname(ROOT), 'ostrava', 'scripts', 'lib.py'))
trolleylib = _load('trolleylib', os.path.join(os.path.dirname(ROOT), 'ostrava-trolleybus', 'scripts', 'lib.py'))

HEADERS = tramlib.HEADERS
http, parse_vypravenost, parse_fleet_list, next_page, record_date = tramlib.http, tramlib.parse_vypravenost, tramlib.parse_fleet_list, tramlib.next_page, tramlib.record_date
jdf_open, jdf_tables, jdf_versions, pick_version, jdf_trips = tramlib.jdf_open, tramlib.jdf_tables, tramlib.jdf_versions, tramlib.pick_version, tramlib.jdf_trips
blocks, active_at, min_turnaround = tramlib.blocks, tramlib.active_at, tramlib.min_turnaround
runfit, loop_shift, plans, make_nm, hm, hhmm, day = tramlib.runfit, tramlib.loop_shift, tramlib.plans, tramlib.make_nm, tramlib.hm, tramlib.hhmm, tramlib.day
real_of = tramlib.real_of
pattern_need = tramlib.pattern_need
cycle_need_peak = trolleylib.cycle_need_peak
# logged-surplus rule (user, 29 Sep 2026): Brno's reference implementation, reused as is
mark_spares = _load('brnotrolleylib', os.path.join(os.path.dirname(ROOT), 'brno-trolleybus', 'scripts', 'common.py')).mark_spares

CONFIG = json.load(open(os.path.join(ROOT, 'config.json'), encoding='utf-8'))
RAW = os.path.join(ROOT, 'data', 'raw', CONFIG['snapshot'])
DERIVED = os.path.join(ROOT, 'data', 'derived')
os.makedirs(DERIVED, exist_ok=True)

def dpath(name): return os.path.join(DERIVED, name)
def save(name, obj): json.dump(obj, open(dpath(name), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
def load(name): return json.load(open(dpath(name), encoding='utf-8'))

def branch_pairs(tr, cfg, anchor=None):
    """Branches of a line = its Simutrans lines (shared by 04_roster, 05_schedule, 07_odis). tr: trips with o, d (alias names).
    1. Peak rule: terminus pairs with >= 2 x min_trips trips in branch_rule.window and a departure in branch_rule.hour; the
       pair with the most trips is always one.
    2. Afternoon rule (owner, 20 Oct 2026: 23 to Bohumín, Záblatí runs every 60-80 min all afternoon, but not at 16:00):
       a pair with >= branch_rule.afternoon_min trips in each direction in branch_rule.afternoon is a branch too.
    Depot ends never are. Returns [(frozenset pair, trips in the window)] in rank order."""
    import collections as _c
    B = cfg['branch_rule']; DEP = set(cfg['depot_stops'])
    dl = (anchor or cfg['peak_minute']) - cfg['peak_minute']        # every window follows the line's own peak anchor
    B = dict(B, window=[x + dl for x in B['window']], hour=[x + dl for x in B['hour']],
             afternoon=B.get('afternoon'))   # the afternoon rule keeps its absolute 13:00-19:00 (shifting it let 34's Rovniny in)
    win = [t for t in tr if B['window'][0] <= t['dep'] < B['window'][1]]
    pairs = _c.defaultdict(list)
    for t in win: pairs[frozenset((t['o'], t['d']))].append(t)
    ranked = sorted(pairs.items(), key=lambda x: -len(x[1])); chosen = []
    for p_, ts in ranked:
        if len(p_) < 2: continue
        hour = any(B['hour'][0] <= t['dep'] < B['hour'][1] for t in ts)
        if not chosen or (len(ts) >= 2 * B['min_trips'] and hour and not (p_ & DEP)): chosen.append((p_, ts))
    aw = B.get('afternoon'); am = B.get('afternoon_min', 3)
    if aw:
        dirs = _c.Counter((t['o'], t['d']) for t in tr if aw[0] <= t['dep'] < aw[1] and t['o'] != t['d'])
        have = {p_ for p_, _ in chosen}
        for (a, b), n in sorted(dirs.items(), key=lambda x: -x[1]):
            p_ = frozenset((a, b))
            if p_ in have or (p_ & DEP) or dirs.get((b, a), 0) < am or n < am: continue
            chosen.append((p_, pairs.get(p_, []))); have.add(p_)
    return chosen, ranked


def interleave(rows, tr, chosen, loop=True, peak=960, tol=5):
    """Branches leaving a shared terminus are fitted together (owner, 20 Oct 2026: "if the real timetable interleaves, you
    should interleave"; 23A/23B had bunched 7 min apart at Hranečník). For each terminus X shared by >= 2 branches:
    for each window (15:30-17:30, 16:00-18:30) and common interval I (dividing 1440), each branch's real departures from X
    must form clusters (spread <= 2 x tol) - one slot each - whose count matches its trips in the window (+-1), with no two
    branches on the same slot. The simplest accepted combination (smallest I, then smallest deviation) sets every branch's
    row at X; its far end gets the same interval and slot count, shifted by one constant that best fits the far end's real
    departures. rows: plans() output (names via nm already); tr: trips with o, d (alias names) and dep, arr; chosen: the
    branch pairs. Rows set this way carry 'interleave' = dict(at, with_, dev, window, far_dev). Returns the rows."""
    import collections as _c
    pairs = [tuple(p_) for p_, _ in chosen]
    ends = _c.defaultdict(list)
    for p_ in pairs:
        for x in p_: ends[x].append(p_)
    def row(a, b): return next((r for r in rows if r.get('every') and r['_o'] == a and r['_d'] == b), None)
    def clusters(res, I):
        """circular 1-D clusters of residues; returns [(centre, half spread)]"""
        if not res: return []
        s = sorted(set(res)); gaps = [((s[(i + 1) % len(s)] - s[i]) % I or I, i) for i in range(len(s))]
        g, i0 = max(gaps); start = (i0 + 1) % len(s)
        order = [s[(start + j) % len(s)] for j in range(len(s))]
        out_, cur = [], [order[0]]
        for v in order[1:]:
            if (v - cur[0]) % I <= 2 * tol: cur.append(v)
            else: out_.append(cur); cur = [v]
        out_.append(cur)
        return [((c[0] + ((c[-1] - c[0]) % I) // 2) % I, ((c[-1] - c[0]) % I + 1) // 2) for c in out_]
    for X, ps in ends.items():
        if len(ps) < 2: continue
        others = {p_: (p_[1] if p_[0] == X else p_[0]) for p_ in ps}
        best = None
        for W in ((peak - 30, peak + 90), (peak, peak + 150)):
            for I in (10, 12, 15, 20, 30, 40, 60, 80, 90, 120):
                if (W[1] - W[0]) < 1.5 * I: continue      # a pattern must repeat inside the window, not just list it (34 had I=120)
                fit = {}; ok = True
                for p_, Y in others.items():
                    rX_ = row(X, Y)       # the row's merged minutes count too (34: Rovniny trips take Hlučín AN slots)
                    D = sorted(set([t['dep'] for t in tr if t['o'] == X and t['d'] == Y] + ((rX_ or {}).get('merged') or [])))
                    D = [x for x in D if W[0] <= x < W[1]]
                    if not D: ok = False; break
                    cl = clusters([x % I for x in D], I)
                    k = len(cl); expect = k * (W[1] - W[0]) / I
                    if k > 8 or abs(expect - len(D)) > 1 or max(h for _, h in cl) > tol: ok = False; break
                    fit[p_] = cl
                if not ok: continue
                slots = sorted(c for cl in fit.values() for c, _ in cl)
                if any(((slots[(i + 1) % len(slots)] - slots[i]) % I or I) < 3 for i in range(len(slots))) and len(slots) > 1: continue
                dev = max(h for cl in fit.values() for _, h in cl)
                key = (I, dev)
                if best is None or key < best[0]: best = (key, W, I, fit)
        if not best: continue
        _, W, I, fit = best
        def rawstops(Y): return {t['stops'][0] for t in tr if t['o'] == Y} | {t['stops'][-1] for t in tr if t['d'] == Y}
        def passing(p_, Y, I):
            """minutes (mod I) at which other branches' buses towards X pass Y: their set far row + running time to Y"""
            rawY = rawstops(Y); out_ = set()
            for q in fit:
                if q == p_: continue
                Z = others[q]; rz = row(Z, X)
                ts = [t for t in tr if t['o'] == Z and t['d'] == X and t.get('times') and any(x in rawY for x in t['stops'][1:-1])
                      and W[0] - 60 <= t['dep'] < W[1] + 60]
                if not ts or not rz or rz.get('every') != I: continue
                off = sorted(t['times'][next(i for i, x in enumerate(t['stops']) if x in rawY)] - t['dep'] for t in ts)[len(ts) // 2]
                out_ |= {(z + off) % I for z in rz['real']}
            return sorted(out_)
        order_ = sorted(fit, key=lambda q: any(any(x in rawstops(others[q]) for x in t['stops'][1:-1]) for t in tr
                                                if t['o'] in (others[q2] for q2 in fit if q2 != q)))
        for p_ in order_:
            cl = fit[p_]
            Y = others[p_]; rX = row(X, Y); rY = row(Y, X)
            if not rX or not rY: continue
            R = sorted(c for c, _ in cl)
            rt = [t['arr'] - t['dep'] for t in tr if t['o'] == X and t['d'] == Y and peak - 60 <= t['dep'] < peak + 120] or [t['arr'] - t['dep'] for t in tr if t['o'] == X and t['d'] == Y]
            if rY.get('interleave') and not rY['interleave'].get('far'): continue   # set at its own shared terminus: keep it
            DY = sorted(t['dep'] for t in tr if t['o'] == Y and t['d'] == X and W[0] <= t['dep'] < W[1] + 30)   # same window (27: an 18:07 outlier)
            # far end: the same slots shifted by one constant >= running time + 3 min; the shift that fits its departures best
            def fdev(sft): return max((min(min((x - (r + sft)) % I, ((r + sft) - x) % I) for r in R) for x in DY), default=0)
            base = max(rt) + 3 if rt else 3
            rtY = [t['arr'] - t['dep'] for t in tr if t['o'] == Y and t['d'] == X and peak - 60 <= t['dep'] < peak + 120] or [t['arr'] - t['dep'] for t in tr if t['o'] == Y and t['d'] == X] or [0]
            def rnd(s_):                                   # round of a vehicle: out, wait at Y, back, wait for its next slot at X
                arr = s_ + max(rtY) + 3
                return min(((r2 - (R[0] + arr)) % I) for r2 in R) + arr
            fmin = min(fdev(s_) for s_ in range(base, base + I))
            tolY = 3 if len(ends.get(Y, [])) >= 2 else max(5, I // 6)   # a shared far end keeps its own alternation (27 Proskovice)
            cand = [s_ for s_ in range(base, base + I) if fdev(s_) <= fmin + tolY]
            pz = passing(p_, Y, I); moved_ = False
            if pz:   # other branches' buses pass this far end on their way to X: fit between them (owner, 20 Oct 2026: 23 at
                     # Rychvald, rozcestí, where the rozcestí departures had sat on the minute the Záblatí bus passes)
                def gap(s_):
                    u = sorted(list(pz) + [(r + s_) % I for r in R])   # a slot on a passing minute is a gap of 0
                    return min(((u[(i + 1) % len(u)] - u[i]) % I) for i in range(len(u))) if len(u) > 1 else I
                sft = min(cand, key=lambda s_: (rnd(s_), fdev(s_)))
                if gap(sft) < 3 and len(DY) >= 2 * len(R):   # a far end leaving within 2 min of a passing bus is moved; not a
                                                              # sparse one, whose slots are approximate anyway (59 Klimkovice: 1 trip)
                    moved_ = True
                    cand = [s_ for s_ in range(base, base + I) if fdev(s_) <= fdev(sft) + 3] or [sft]   # no further from the timetable
                    sft = min(cand, key=lambda s_: (-gap(s_), fdev(s_), rnd(s_)))
            else:
                sft = min(cand, key=lambda s_: (rnd(s_), fdev(s_)))
            RY = sorted((r + sft) % I for r in R)
            if rX.get('interleave') and rX['interleave'].get('far') is None and rX['interleave'].get('at') != X: pass
            for r_, RR in ((rX, R), (rY, RY)):
                for k_ in ('approx', 'alt', 'refit'): r_.pop(k_, None)
                r_.update(every=I, real=RR, set=loop_shift(I, RR, loop))
            rX['interleave'] = dict(at=X, with_=[others[q] for q in fit if q != p_], dev=max(h for _, h in cl), window=list(W))
            rY['interleave'] = dict(at=X, far=True, with_=[others[q] for q in fit if q != p_], dev=fdev(sft), window=[W[0], W[1] + 30])
            if moved_: rY['interleave']['passing'] = sorted(pz)
    return rows

def even_interval(I, real):
    """(interval, slots) with evenly spaced slots folded: every 60 at :17 and :47 is every 30 at :17 (owner, 20 Oct 2026,
    27A: "why is this not just departure every 30 minutes?"). Uneven slots stay as they are."""
    r = sorted(set(x % I for x in real)); k = len(r)
    if k > 1 and I % k == 0 and all((r[(i + 1) % k] - r[i]) % I == I // k for i in range(k)):
        return I // k, [r[0] % (I // k)]
    return I, r


def exact_run(deps, W, tol=1, off=0):
    """The regular pattern a row's own departures keep exactly: (every, slots, first, last, n, displaced) with every departure of
    the run within tol of a slot and every slot of the run taken, >= 6 departures (3 for an hourly single slot) over >= 2 h,
    covering at least half of the model window W, and no other departure inside the run; the longest such run, else None.
    off > 0 (whole-day reading) lets a slot be taken by a departure up to off min away, one in six at most (96: hourly :38
    all day, 13:43 once); those are returned as displaced."""
    import collections as _c
    best = None
    for I in (10, 12, 15, 20, 30, 40, 60):
        for k in (1, 2, 3):
            for slots in [sorted(x for x, _ in _c.Counter(d % I for d in deps).most_common(k))]:
                dist = lambda d: min(min((d - s_) % I, (s_ - d) % I) for s_ in slots)
                on = [d for d in deps if dist(d) <= max(tol, off)]
                # longest stretch of consecutive slots all taken
                run, cur, prev = [], [], None
                for d in on:
                    if cur and d - cur[-1] > I // len(slots) + 2 * max(tol, off): run = max(run, cur, key=len); cur = []   # a missing slot ends the run
                    cur.append(d)
                run = max(run, cur, key=len)
                if len(run) < (3 if I >= 60 and len(slots) == 1 else 6) or run[-1] - run[0] < 120: continue   # hourly: 3 (as plans' ok())
                exp = len([t for t in range(run[0] - max(tol, off), run[-1] + max(tol, off) + 1) if t % I in slots])
                if len(run) < exp: continue
                disp = [d for d in run if dist(d) > tol]
                if len(disp) > len(run) // 6: continue
                if off and any(run[0] < d < run[-1] and d not in run for d in deps): continue   # the run is the whole service there
                cover = max(0, min(run[-1], W[1]) - max(run[0], W[0]))
                if cover * 2 < W[1] - W[0]: continue
                key = (len(run), -I)
                if best is None or key > best[0]: best = (key, (I, slots, run[0], run[-1], len(run), disp))
    return best[1] if best else None


def exactify(rows, trips, nm, W, loop, al=lambda x: x, day=None):
    """Rows made approximate by a wind-down in the model window or by folded-in variant minutes, whose own trips keep an exact
    pattern (owner's intent, 20 Oct 2026; found with the Havířov/Karviná/Orlová sheet: 49 to sad B. Němcové is every 20 until
    16:45 but was averaged to every 30; 76 is hourly both ways but 2 Polanka trips folded in made it every 30): both ends of
    the pair take their exact patterns when they run at the same rate. Returns the list of pairs changed.
    day=(start, end): the owner's whole-day reading (20 Oct 2026, from the save game's Ex4: "I defined it in core points, created
    a repeating interval and it suddenly made sense"): the pattern is read over the whole operating day, a single displaced
    departure allowed, when the 13:00-19:00 reading finds none."""
    done = []
    for a in rows:
        if not a.get('every') or a in done: continue
        b = next((r for r in rows if r.get('every') and al(r['fr']) == al(a['to']) and al(r['to']) == al(a['fr'])), None)
        if not b: continue
        if not (any(x.get('approx', 0) >= 5 or x.get('merged') or x.get('refit') for x in (a, b))): continue
        fits = []
        for r in (a, b):
            deps = sorted(t['dep'] for t in trips if nm(t['fr']) == r['fr'] and nm(t['to']) == r['to'] and 780 <= t['dep'] < 1140)
            fits.append(exact_run(deps, W))
        if not all(fits) and day:
            fits = []
            for r in (a, b):
                deps = sorted(t['dep'] for t in trips if nm(t['fr']) == r['fr'] and nm(t['to']) == r['to'] and day[0] <= t['dep'] < day[1])
                fits.append(exact_run(deps, W, off=5))
        if not all(fits): continue
        (Ia, sa, *_), (Ib, sb, *_) = fits
        if len(sa) * 60 / Ia != len(sb) * 60 / Ib: continue
        if all(r['every'] == f[0] and sorted(r['real']) == f[1] for r, f in zip((a, b), fits)): continue
        for r, (I, sl, f0, f1, n, disp) in zip((a, b), fits):
            for k in ('approx', 'alt', 'refit', 'interleave'): r.pop(k, None)
            r['exactified'] = dict(old_every=r['every'], old_real=r['real'], dropped_merged=r.get('merged') or [], displaced=disp,
                                   whole_day=bool(day and (disp or f0 < 780 or f1 >= 1140)))
            r.update(every=I, real=sl, set=loop_shift(I, sl, loop), first=f0, last=f1, n=n, merged=[])
        done += [a, b]
    return done


def thin_rows(rows, loop):
    """A row whose slots outnumber its real departures (at least two per slot) is one slot, approximate (62: two shift trips
    at 14:10 and 15:02 had been written as every 60 at :02 and :10, two buses an hour for a one-bus line)."""
    for p in rows:
        if not p.get('every') or len(p.get('real', [])) < 2 or not p.get('deps_win'): continue
        I = p['every']; W = p['deps_win']; deps = p.get('deps_') or []
        slots = sum(1 for t in range(W[0], W[1]) if t % I in p['real'])
        if not deps or slots <= len(deps) + 1 or len(deps) >= 2 * len(p['real']): continue
        best = min(range(I), key=lambda c: max(min((x - c) % I, (c - x) % I) for x in deps))
        dev = max(min((x - best) % I, (best - x) % I) for x in deps)
        p['thinned_from'] = p['real']; p.update(real=[best], set=loop_shift(I, [best], loop), approx=dev)
        p.pop('alt', None)
    return rows


def simplify_rows(rows, loop):
    """even_interval on every timed row (interleaved branches share one interval at their terminus, so a branch that runs
    two or three times as often got several evenly spaced slots)"""
    for p in rows:
        if not p.get('every') or len(p.get('real', [])) < 2: continue
        # slots 1-2 min apart are one departure whose minute drifts (54: every 10 at :x3, then :x2 from 16:02; it was written
        # as every 60 with 7 slots); keep the member that leaves an even pattern
        I0, r0 = p['every'], sorted(p['real'])
        dup = [(r0[i], r0[(i + 1) % len(r0)]) for i in range(len(r0)) if 0 < (r0[(i + 1) % len(r0)] - r0[i]) % I0 <= 2]
        if dup:
            opts = []
            for keep in ([a for a, _ in dup], [b for _, b in dup]):
                drop = {x for pr in dup for x in pr} - set(keep)
                rr = [x for x in r0 if x not in drop]
                opts.append((even_interval(I0, rr)[0] if rr else I0, rr))
            rr = min(opts, key=lambda o: (o[0] == I0, -len(o[1])))[1]
            p['merged_slots'] = sorted(set(r0) - set(rr)); p.update(real=rr, set=loop_shift(I0, rr, loop))
        I, r = even_interval(p['every'], p['real'])
        if I != p['every']:
            p['folded_from'] = p['every']; p.update(every=I, real=r, set=loop_shift(I, r, loop))
    return rows


def line_anchor(tr, cfg):
    """The minute a line is modelled at (owner, 20 Oct 2026: "for 23 I see 20 minutes as the most common afternoon peak
    pattern"; 23 runs every 20 until 16:10 and every 40 after, and many Ostrava lines peak 14:00-16:00 with the shifts).
    All departures of the line, both directions. If its busiest 2 hours in 13:00-18:00 have at most one departure more
    than 15:00-17:00, it stays at the sheet's peak (16:00, where the live roster was observed); otherwise it moves to
    30 min into that busiest window (ties: nearest 16:00), so every fit band covers that window."""
    deps = sorted(t['dep'] for t in tr); base = cfg['peak_minute']
    cnt = lambda a, b: sum(1 for x in deps if a <= x < b)
    at = cnt(base - 60, base + 60)
    best = max(range(780, 961, 10), key=lambda s0: (cnt(s0, s0 + 120), -abs(s0 + 60 - base)))
    n = cnt(best, best + 120)
    moved = n - at > 1
    # the anchor sits 30 min into the busiest stretch, so the fit band (anchor - 30 to anchor + 90) is exactly that stretch
    return dict(anchor=best + 30 if moved else base, busiest=[best, best + 120], n=n, at_peak=at, moved=moved)


def path_variants(tr, T0, nm_, keep_stops=()):
    """Directions that run on two or more paths between the same termini around the anchor (owner, 20 Oct 2026: 28 runs
    Šenov – Václavovice alternately via U Blažka and via Václavovice střed; one merged row lets Simutrans buses take one
    path only). Trips T0-60..T0+120 of one direction are grouped as one path when their stop sets differ by at most one
    stop (a skipped stop); a direction counts when at least two such paths have 2+ trips each (32: one path via
    Hlučínská, the other via Hálkova / Přednádraží / Na Mlýnici / Palackého).
    keep_stops: raw stop names only this line serves in the afternoon; a trip differing by one of them is its own path, not
    a skipped stop, so the stop stays on a modelled line (49: every second bus Poruba -> Michálkovice via Hrušov, Růžová).
    Returns {(o, d): [dict(via=label, deps=[...], stops=[...])]}; the label is the path's first stop no other path has."""
    import collections as _c
    by = _c.defaultdict(list)
    for t in tr:
        if T0 - 60 <= t['dep'] < T0 + 120: by[(nm_(t['o']), nm_(t['d']))].append(t)
    out = {}
    for k, ts in by.items():
        grp = []
        for t in sorted(ts, key=lambda t: t['dep']):
            st = frozenset(t['stops'])
            g = next((g for g in grp if len(st ^ g['set']) <= 1 and not (st ^ g['set']) & set(keep_stops)), None)
            if g: g['trips'].append(t)
            else: grp.append(dict(set=st, trips=[t]))
        big = [g for g in grp if len(g['trips']) >= 2]
        if len(big) < 2: continue
        allst = [frozenset(x for t in g['trips'] for x in t['stops']) for g in big]
        ps = []
        for i, g in enumerate(big):
            oth = frozenset().union(*(b for j, b in enumerate(allst) if j != i))
            seq = _c.Counter(tuple(t['stops']) for t in g['trips']).most_common(1)[0][0]
            own = next((x for x in reversed(seq) if x not in oth), None)   # its own stop nearest the end (32: Hálkova)
            miss = [x for t in big[1 - i if len(big) == 2 else 0]['trips'][:1] for x in t['stops'] if x not in g['set']] if own is None else []
            if own is None and 0 < len(miss) <= 2:   # skips one or two stops the other path serves (49: not via Hrušov, Růžová)
                ps.append(dict(via=miss[0], skip='notvia', deps=sorted(t['dep'] for t in g['trips']), stops=list(seq)))
            else:   # skips a whole stretch: "non-stop to" its next stop (531 from Hranečník)
                ps.append(dict(via=own or seq[1], skip=own is None, deps=sorted(t['dep'] for t in g['trips']), stops=list(seq)))
        # trips of the small groups go to the path sharing the most stops
        for g in grp:
            if g in big: continue
            j = max(range(len(big)), key=lambda i: len(g['set'] & big[i]['set']))
            ps[j]['deps'] = sorted(ps[j]['deps'] + [t['dep'] for t in g['trips']])
        out[k] = ps
    # one label per path in both directions: a stop only that path has, shared with the matching reverse path
    for (o, d), ps in out.items():
        rv = out.get((d, o))
        if not rv: continue
        for q in ps:
            oth = set().union(*(set(x['stops']) for x in ps if x is not q))
            dist = [x for x in q['stops'] if x not in oth]
            r = max(rv, key=lambda r_: len(set(dist) & set(r_['stops'])))
            roth = set().union(*(set(x['stops']) for x in rv if x is not r))
            sh = [x for x in dist if x in r['stops'] and x not in roth]
            if sh and not q.get('skip'): q['via'] = sh[-1] if o < d else sh[0]
    return out


def circuitize(brs, rows, tr, lay, T0, nm_, paths=None):
    """Branches sharing one terminus X, run as circuits (owner, 20 Oct 2026: "where it significantly shortens wait, do it";
    23 needed 2 + 2 buses as separate branch lines, while real buses swap branches at Hranečník and run with 3).
    Only for lines whose branches all share one terminus (a star). Jobs = X's departure slots in one period I (from the
    interleaved rows); each job is a trip out on its branch, the first real departure back at least the layover later, and
    the trip back. A vehicle finishing a job takes a next job at X; the assignment (all permutations, <= 8 jobs) with the least
    total waiting splits into cycles, and each cycle is one Simutrans line (a circuit, or a plain branch when it stays on one
    branch). Vehicles = total cycle time / I. Used only when it saves >= 1 vehicle over the separate branches.
    A single branch whose directions run on two paths (path_variants; 28) is a circuit too: the bus leaves the far end on
    the first departure of either path, and the circuit is used even without saving a vehicle, so every path is served.
    Returns a list of branch dicts, or None."""
    import itertools as _it
    paths = paths or {}
    single = len(brs) == 1 and any({o, d} == {brs[0]['a'], brs[0]['b']} for o, d in paths)
    if len(brs) < 2 and not single: return None
    common = {brs[0]['a'], brs[0]['b']}
    for b in brs[1:]: common &= {b['a'], b['b']}
    if single: common = {brs[0]['b']}   # the oriented far end: jobs are its slots
    if len(common) != 1: return None
    X = common.pop(); other = {(b['b'] if b['a'] == X else b['a']): b for b in brs}
    pathy = {Y for Y in other if paths.get((X, Y)) or paths.get((Y, X))}   # branches with two paths (28, 32, 49)
    rX = {Y: next((r for r in rows if r.get('every') and nm_(r['fr']) == X and nm_(r['to']) == Y), None) for Y in other}
    if any(v is None for v in rX.values()): return None
    Is = {rX[Y]['every'] for Y in other}
    import math as _m
    I = _m.lcm(*Is)   # rows every 20 and every 30 (49) run as one period of 60
    if I > 120 or 1440 % I: return None
    def rt(a, b):
        r = [t['arr'] - t['dep'] for t in tr if t['o'] == a and t['d'] == b and T0 - 60 <= t['dep'] < T0 + 120] or [t['arr'] - t['dep'] for t in tr if t['o'] == a and t['d'] == b]
        return max(r) if r else None
    def rt_at(a, b, slot):   # longest running time of the real trips a -> b departing within 2 min of the slot
        r = [t['arr'] - t['dep'] for t in tr if t['o'] == a and t['d'] == b and T0 - 60 <= t['dep'] < T0 + 120
             and min((t['dep'] - slot) % I, (slot - t['dep']) % I) <= 2]
        return max(r) if r else None
    def far_res(Y):   # the far row's fitted pattern (rate-matched like the rest of the sheet), else the real residues
        r = next((r for r in rows if r.get('every') and nm_(r['fr']) == Y and nm_(r['to']) == X), None)
        if r and I % r['every'] == 0: return sorted(x + k * r['every'] for x in r['real'] for k in range(I // r['every']))
        return sorted({t['dep'] % I for t in tr if t['o'] == Y and t['d'] == X and T0 - 30 <= t['dep'] < T0 + 90})
    realX = {Y: sorted(r + k * rX[Y]['every'] for r in rX[Y]['real'] for k in range(I // rX[Y]['every'])) for Y in other}
    PX = [Y for Y in pathy if paths.get((X, Y))]
    if PX:   # paths alternating at a multiple of the row's interval (32: every 30 at Křižíkova = each path every 60)
        def pth(Y, sl, P):
            ps = paths[(X, Y)]
            return min(range(len(ps)), key=lambda i: min(min((x - sl) % P, (sl - x) % P) for x in ps[i]['deps']))
        for m in (1, 2, 3, 4):
            P = I * m
            if 1440 % P: continue
            sl = {Y: sorted(r + k * I for r in realX[Y] for k in range(m)) for Y in other}
            if all(len({pth(Y, x, P) for x in sl[Y]}) >= 2 for Y in PX): I = P; realX = sl; break
    jobs = sorted((r, Y) for Y in other for r in realX[Y])
    if len(jobs) > 8 or len(jobs) < 2: return None
    J = []
    for r, Y in jobs:
        a, b = rt(X, Y), rt(Y, X); fr_ = far_res(Y)
        if a is None or b is None or not fr_: return None
        if Y in pathy: a = rt_at(X, Y, r) or a   # path variants: the running time of the slot's own path
        ready = r + a + lay.get(Y, 3)
        back = next(x for x in range(ready, ready + I + 1) if x % I in fr_)
        if Y in pathy: b = rt_at(Y, X, back % I) or b
        J.append(dict(r=r, Y=Y, out=a, back=back % I, rt_back=b, done=back + b + lay.get(X, 3)))   # done: absolute, from r
    def wait(j, k):   # j's vehicle, ready at done_j, takes job k's next departure
        return (J[k]['r'] - J[j]['done']) % I
    n = len(J); best = None
    for perm in _it.permutations(range(n)):
        tot = sum(J[j]['done'] - J[j]['r'] + wait(j, perm[j]) for j in range(n))
        # vehicles first; at equal vehicles keep each branch's buses on it (no swap without a saving), then least waiting
        key = (-(-tot // I), sum(1 for j in range(n) if J[perm[j]]['Y'] != J[j]['Y']), tot)
        if best is None or key < best[0]: best = (key, perm, tot)
    _, perm, tot = best
    sep = sum(b['need'] for b in brs); need = tot // I
    if need > sep or (need == sep and not pathy): return None
    def via(o, d, slot):   # the path of the real departure nearest the slot, for directions with path variants
        ps = paths.get((o, d))
        if not ps: return None
        return min(ps, key=lambda q: min(min((x - slot) % I, (slot - x) % I) for x in q['deps']))
    seen = set(); out = []
    for j0 in range(n):
        if j0 in seen: continue
        cyc = []; j = j0
        while j not in seen: seen.add(j); cyc.append(j); j = perm[j]
        legs = [dict(X=X, Y=J[j]['Y'], out_slot=J[j]['r'], back_slot=J[j]['back'], rt_out=J[j]['out'], rt_back=J[j]['rt_back'],
                     wait_next=wait(j, perm[j])) for j in cyc]
        for g in legs:
            for k, (o, d, sl) in (('out', (g['X'], g['Y'], g['out_slot'])), ('back', (g['Y'], g['X'], g['back_slot']))):
                q = via(o, d, sl)
                if q: g[k + '_via'] = q['via']; g[k + '_skip'] = q.get('skip', False); g[k + '_deps'] = q['deps']; g[k + '_stops'] = q['stops']
        ctime = sum(J[j]['done'] - J[j]['r'] + wait(j, perm[j]) for j in cyc)
        Ys = [J[j]['Y'] for j in cyc]
        out.append(dict(a=X, b=' / '.join(dict.fromkeys(Ys)), circuit=len(set(Ys)) > 1 or len(cyc) > 1, paths=bool(pathy & set(Ys)), legs=legs, period=I,
                        need=ctime // I, cycle=ctime, how='circuit', sep_need=sep, trips=0, observed=0, surplus=0, min_runtime=None))
    # cycles that stay on one plain branch are one Simutrans line (49: two 1-bus Vozovna cycles = Vozovna every 30, 2 buses)
    merged = []
    for c in out:
        m = next((x for x in merged if not c['paths'] and not x['paths'] and {g['Y'] for g in c['legs']} == {g['Y'] for g in x['legs']}
                  and len({g['Y'] for g in c['legs']}) == 1), None)
        if m: m['legs'] += c['legs']; m['need'] += c['need']; m['cycle'] += c['cycle']; m['circuit'] = True
        else: merged.append(c)
    return merged


def slot_need(P, legs):
    """Buses a hand-set line needs (bus schedule method, Step 10): legs = (from, to, departures mod P, running time,
    min wait at `to` before the next departure). At each terminal the arrivals are matched to the departures in turn,
    each wait at least that minimum, the matching with the least total wait; buses = (running + waits) / P. Exact for
    uneven slots (442: :20 :40 :50 out, :21 :36 :51 back is 4 buses), where following one bus round over-counts or not."""
    T = {x for l in legs for x in l[:2]}; tot = sum(l[3] * len(l[2]) for l in legs); waits = {}
    for t in T:
        arr = sorted(((d + l[3]) % P, l[4]) for l in legs if l[1] == t for d in l[2])
        dep = sorted(d % P for l in legs if l[0] == t for d in l[2])
        if len(arr) != len(dep): raise ValueError(f'unbalanced at {t}: {len(arr)} arrivals, {len(dep)} departures')
        best = None
        for k in range(len(dep)):
            w = []
            for i, (a, ly) in enumerate(arr):
                x = (dep[(i + k) % len(dep)] - a) % P
                while x < ly: x += P
                w.append(x)
            if best is None or sum(w) < sum(best): best = w
        waits[t] = best; tot += sum(best)
    return round(tot / P), waits


def hand_lines(H_, L, T0, by_line, nm, C):
    """config.hand_lines[L]: the Simutrans lines set by hand from the whole-day core-point reading. Each becomes a branch with
    legs (as lib.circuitize gives), so the card, the fit cells, the coverage check and the roster read them as any circuit."""
    import collections
    out = []
    for sl in H_['lines']:
        I = sl['every']; X, Y = sl['X'], sl['Y']
        def mins(v): return [(int(x.split(':')[0]) * 60 + int(x.split(':')[1])) % I if isinstance(x, str) else x % I for x in v]
        def ts_(lines_, a, b):
            return [t for l_ in lines_ for t in by_line.get(l_, []) if nm(t['fr']) == a and nm(t['to']) == b]
        def rt(ts):
            w = [t['arr'] - t['dep'] for t in ts if T0 - 60 <= t['dep'] < T0 + 120] or [t['arr'] - t['dep'] for t in ts]
            return round(sum(w) / len(w)) if w else None
        def seq(ts):
            w = [t for t in ts if 780 <= t['dep'] < 1140] or ts
            return list(collections.Counter(tuple(t['stops']) for t in w).most_common(1)[0][0]) if w else []
        outs = mins(sl['out']); backs = mins(sl['back']) if sl.get('back') is not None else None
        def near(ts, sl_):   # another line's trips count only where they run in this line's slots (534 in 535's :25)
            return [t for t in ts if any(min((t['dep'] - s_) % I, (s_ - t['dep']) % I) <= 3 for s_ in sl_)]
        to_ = ts_([L], X, Y) + near(ts_([l_ for l_ in sl['out_lines'] if l_ != L], X, Y), outs)
        back_ = ts_([L], Y, X) + (near(ts_([l_ for l_ in sl['back_lines'] if l_ != L], Y, X), backs) if backs else [])
        if L not in sl['out_lines']: to_ = ts_(sl['out_lines'], X, Y)
        if L not in sl['back_lines']: back_ = ts_(sl['back_lines'], Y, X)
        # the line's own short turns in a slot (535 17:25 to Lutyně): a real departure of that slot, turning short
        seq0 = {nm(x) for t in to_ for x in t['stops']}
        to_ += [t for t in by_line.get(L, []) if nm(t['fr']) == X and nm(t['to']) != Y and nm(t['to']) in seq0 and t not in to_ and any(min((t['dep'] - s_) % I, (s_ - t['dep']) % I) <= 3 for s_ in outs)]
        r_out, r_back = rt([t for t in to_ if nm(t['to']) == Y and t in ts_([L], X, Y)] or [t for t in to_ if nm(t['to']) == Y]), rt(back_ or ts_(sl['back_lines'] + [L], Y, X))
        if r_back is None: r_back = sl.get('back_rt', r_out)   # no trip ever runs back (57 from the garage): as the way out
        tr_l = [dict(t, o=nm(t['fr']), d=nm(t['to'])) for l_ in set(sl['out_lines'] + sl['back_lines']) for t in by_line.get(l_, [])]
        mt = min_turnaround(tr_l)
        lay = lambda x: max(1, min(C['cycle_lay'], mt.get(x, C['cycle_lay'])))   # Step 10: real turnaround when shorter, never < 1
        if backs is None:      # empty, untimed return: leaves on arrival (Step 10: 0 min before it)
            n_, w_ = slot_need(I, [(X, Y, outs, r_out, 0), (Y, X, [(o + r_out) % I for o in outs], r_back, lay(X))])
        else:
            n_, w_ = slot_need(I, [(X, Y, outs, r_out, lay(Y)), (Y, X, backs, r_back, lay(X))])
        legs = []
        for i, o in enumerate(outs):
            g = dict(X=X, Y=Y, out_slot=o, back_slot=backs[i % len(backs)] if backs else None, rt_out=r_out, rt_back=r_back,
                     out_deps=sorted(t['dep'] for t in to_), back_deps=sorted(t['dep'] for t in back_), out_stops=seq([t for t in to_ if nm(t['to']) == Y]), back_stops=seq(back_ or ts_(sl['back_lines'], Y, X)),
                     back_untimed=backs is None, out_lines=sl['out_lines'], back_lines=sl['back_lines'])
            if sl.get('out_via'): g['out_via'] = sl['out_via']
            if sl.get('back_via'): g['back_via'] = sl['back_via']
            legs.append(g)
        if backs and len(backs) > len(outs): raise ValueError(f'{L} {sl["name"]}: more back slots than out slots')
        W_ = [int(x.split(':')[0]) * 60 + int(x.split(':')[1]) for x in sl['window']] if sl.get('window') else None
        out.append(dict(a=X, b=Y, name=sl['name'], hand=True, legs=legs, period=I, fitwin=W_, need=n_, cycle=None, sep_need=n_, waits=w_,
                        paths=bool(sl.get('out_via') or sl.get('back_via')), trips=len(to_) + len(back_), observed=0, surplus=0,
                        how=(f"set by hand from the whole-day reading at its core points ({', '.join(H_['core'])}); every {I}, "
                             f"{len(outs)} slot{'s' if len(outs) > 1 else ''} each way; {r_out} + {r_back} min running"
                             + (" (back empty, untimed)" if backs is None else '') + f"; buses from matching each terminal's arrivals to its departures (waits "
                             + '; '.join(f"{k}: {', '.join(map(str, v))}" for k, v in w_.items()) + " min)"
                             + (f"; {sl['why']}" if sl.get('why') else ''))))
    return out
