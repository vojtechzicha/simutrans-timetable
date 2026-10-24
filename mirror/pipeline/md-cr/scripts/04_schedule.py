"""Decide which variants are Simutrans lines, merge the rest, and set each terminus to its common standard pattern.

Rules (README "Rail rules", revised 29 Sep 2026 after the user asked for a practical standard, not one hour):
- Window: the afternoon 12:00-19:59. No single reference hour.
- A line's main variant (most trips) is always a Simutrans line. Another variant is one when it has >= 3 trips
  in the window (both directions). Other variants are merged into the modelled variant sharing a terminus and the most
  stops; their departures from that terminus count in its standard.
- Standard at a terminus: the typical headway (median gap between departures in the window, rounded to
  30 / 60 / 120 / 180 / 240 min) and the minute most departures keep within +-5 min. One slot, no Also at.
  One interval per Simutrans line: the end with more departures sets it; the other end gets its best minute.
- Rail termini keep the real minute (no loop rule). Timetables only on the two termini.
Output: data/derived/schedule.json
"""
import json, os, collections, statistics, math

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CFG = json.load(open(os.path.join(ROOT, 'config.json'), encoding='utf-8'))
OV = json.load(open(os.path.join(ROOT, 'overrides.json'), encoding='utf-8'))
W = CFG['window']
S0, S1 = W['search_from'], W['search_to']
HEADWAYS = [30, 60, 120, 240]  # Czech clock-face headways
EMPTY = 0.75  # a standard slot without a train costs this much against a pattern
TOL = W.get('tolerance', 5)
BRANCH_PEAK = (840, 1080)  # a branch needs a departure 14:00-17:59 (rail adaptation agreed 29 Sep)
FOREIGN = json.load(open(os.path.join(ROOT, 'assets', 'foreign.json'), encoding='utf-8'))['terminal']


def fterm(x):
    return FOREIGN.get(x, x) if x else x


def chain(trips, X, tmin=15, tmax=240):
    """FIFO-link in-service arrivals at X to the next departures from X (>= tmin, <= tmax later).
    Returns (links, switches): how often a train leaves X on a different route than it came in on."""
    arr = sorted((t['stops'][-1]['arr'], t['key']) for t in trips if t['stops'][-1]['name'] == X)
    dep = sorted((t['stops'][0]['dep'], t['key']) for t in trips if t['stops'][0]['name'] == X)
    used, links, sw = set(), 0, 0
    for a, ka in arr:
        for i, (d, kd) in enumerate(dep):
            if i in used or d < a + tmin:
                continue
            if d > a + tmax:
                break
            used.add(i)
            links += 1
            sw += ka != kd
            break
    return links, sw


def hm(m):
    m %= 1440
    return f"{m // 60:02d}:{m % 60:02d}"


def notation(I, off):
    if I < 60:
        return f"every {I} min at " + ' '.join(f":{s:02d}" for s in sorted({off % I + k * I for k in range(60 // I)}))
    if I == 60:
        return f'every 1 h at :{off:02d}'
    if I == 120:
        return f"every 2 h at {'L' if (off // 60) % 2 else 'S'}:{off % 60:02d}"
    if I == 1440:
        return 'once a day at ' + hm(off)
    return f"every {I // 60} h at " + ', '.join(hm(off + k * I) for k in range(1440 // I) if 360 <= off + k * I < 1320)


def leave_up_to(I):
    return {'set': 30, 'auto': I // 2} if I > 60 else {'set': None, 'auto': I // 2}


def cdist(x, off, I):
    r = (x - off) % I
    return min(r, I - r)


def best_minute(d, I):
    """The minute (mod I) that most departures keep within TOL; ties to the smallest total deviation."""
    best = None
    for off in range(I):
        dev = [cdist(x, off, I) for x in d]
        fit = [v for v in dev if v <= TOL]
        near = min((abs(x - 990) for x in d if cdist(x, off, I) <= TOL), default=9999)  # ties: nearest 16:30
        key = (len(fit), -sum(fit), -max(fit, default=0), -near)
        if best is None or key > best[0]:
            best = (key, off)
    return best[1]


def slots_empty(use, off, I):
    """Standard slots between the first and last departure that no train keeps."""
    out = []
    k0 = (use[0] - TOL - off) // I
    for k in range(k0, (use[-1] + TOL - off) // I + 1):
        slot = k * I + off
        if use[0] - TOL <= slot <= use[-1] + TOL and not any(abs(x - slot) <= TOL for x in use):
            out.append(slot)
    return out


def score(use, I):
    off = best_minute(use, I)
    fits = sum(1 for x in use if cdist(x, off, I) <= TOL)
    return fits - EMPTY * len(slots_empty(use, off, I))


def pick_headway(ends):
    """The clock-face interval that the departures of all given ends keep best together."""
    ends = [e for e in ends if len(e) >= 2]
    if not ends:
        return 1440
    gaps = [b - a for e in ends for a, b in zip(e, e[1:])]
    cands = [h for h in HEADWAYS if h >= 60 or statistics.median(gaps) <= 40]
    return max(cands, key=lambda h: (sum(score(e, h) for e in ends), -h))


def standard(deps, I=None, other_has_window=False):
    """Common standard pattern of one terminus. I forces the interval (one rate per line)."""
    d = sorted(set(deps))
    win = [x for x in d if S0 <= x < S1]
    if not win and other_has_window:
        return {'kind': 'untimed', 'window': [], 'later': [hm(x) for x in d]}
    basis = 'afternoon'
    use = win
    if len(use) < 2 and I is None:
        day = [x for x in d if 360 <= x < 1320]
        if len(day) >= 2 and not win:
            use, basis = day, 'daytime'
    if not use:
        use, basis = d, 'daytime'
    if I is None:
        if len(use) < 2:
            I = 1440
        else:
            # the headway whose best minute keeps the most departures, each empty slot counting against it;
            # 30 min only when trains really run that often
            I = pick_headway([use])
    off = best_minute(use, I) if I != 1440 else use[0]
    fits = [x for x in use if cdist(x, off, I) <= TOL]
    offp = [x for x in use if cdist(x, off, I) > TOL]
    dev = max((cdist(x, off, I) for x in fits), default=0)
    empty = slots_empty(use, off, I) if I < 1440 else []
    maxdev = max((cdist(x, off, I) for x in use), default=0)
    return {'kind': 'exact' if maxdev == 0 else 'approx', 'maxdev': maxdev, 'I': I, 'offset': off, 'also': [],
            'text': notation(I, off), 'dev': dev, 'fits': len(fits), 'of': len(use), 'basis': basis,
            'offpattern': [hm(x) for x in offp], 'empty': [hm(x) for x in empty],
            'window': [hm(x) for x in win], 'leave': leave_up_to(I)}


LONG_PAX = 5   # a passenger stop of at least 5 min is a long stay
LONG_TECH = 2  # a stop without passengers of at least 2 min


def long_stays(own, start, I):
    """Long stays of the trips leaving `start`, by stop, with the fork values for a timetable entry there."""
    by = collections.defaultdict(list)
    trips = [t for t in own if t['stops'][0]['name'] == start]
    for t in trips:
        st = t['stops']
        if st[0].get('cont_arr') is not None:
            by[(st[0]['name'], 'from abroad')].append((0, st[0]['dep'] - st[0]['cont_arr'], st[0]['cont_arr'], st[0]['dep'], t))
        for k, s in enumerate(st[1:-1], 1):
            if s['arr'] is not None and s['dep'] is not None:
                by[(s['name'], 'passengers')].append((k, s['dep'] - s['arr'], s['arr'], s['dep'], t))
        if st[-1].get('cont_dep') is not None:
            by[(st[-1]['name'], 'before the border')].append((len(st), st[-1]['cont_dep'] - st[-1]['arr'], st[-1]['arr'], st[-1]['cont_dep'], t))
        for x in t.get('tech', []):
            by[(x['name'], 'no passengers')].append((x['after'] + 0.5, x['dep'] - x['arr'], x['arr'], x['dep'], t))
    out = []
    for (name, kind), rows in by.items():
        pos = statistics.median(r[0] for r in rows)
        rows = [r[1:] for r in rows]
        lim = LONG_TECH if kind == 'no passengers' else LONG_PAX
        longr = [r for r in rows if r[0] >= lim]
        if not longr or (len(longr) * 2 < len(trips) and len(longr) < 2):
            continue
        dw = sorted(r[0] for r in longr)
        st = standard([r[2] for r in longr], I=I) if I and I < 1440 else standard([r[2] for r in longr])
        arr = standard([r[1] for r in longr], I=st['I'])
        out.append({'name': name, 'kind': kind, 'pos': pos, 'n': len(longr), 'of': len(trips),
                    'dwell_min': dw[0], 'dwell_max': dw[-1], 'dwell_med': dw[len(dw) // 2],
                    'arr': arr, 'dep': st,
                    'trains': [[t['cat'] + ' ' + '+'.join(t['nums']), hm(a), hm(d)] for dd, a, d, t in sorted(longr, key=lambda r: r[2])]})
    out.sort(key=lambda x: x['pos'])
    return out


def in_win(t):
    return S0 <= t['stops'][0]['dep'] < S1


def stop_pattern(trips, a):
    """Stops in order from terminus a, with how many trips serve them and median times from a."""
    seqs = []
    for t in trips:
        st = t['stops'] if t['stops'][0]['name'] == a else list(reversed(t['stops']))
        seqs.append((t, st))
    order, count = [], collections.Counter()
    for t, st in seqs:
        for k, s in enumerate(st):
            count[s['name']] += 1
            if s['name'] not in order:
                prev = [x['name'] for x in st[:k] if x['name'] in order]
                pos = order.index(prev[-1]) + 1 if prev else 0
                order.insert(pos, s['name'])
    n = len(trips)
    out = []
    for name in order:
        rel, relb = [], []
        for t, st in seqs:
            if t['stops'][0]['name'] == a:
                base = st[0]['dep']
                for s in st:
                    if s['name'] == name:
                        arr = s['arr'] if s['arr'] is not None else s['dep']
                        dep = s['dep'] if s['dep'] is not None else s['arr']
                        rel.append((arr - base, dep - base, s['req']))
            else:
                # opposite direction: time before arrival at a
                end = st[0]['arr']
                for s in st:
                    if s['name'] == name:
                        arr = s['arr'] if s['arr'] is not None else s['dep']
                        dep = s['dep'] if s['dep'] is not None else s['arr']
                        relb.append((end - dep, end - arr, s['req']))
        out.append({'name': name, 'served': count[name], 'of': n, 'main': count[name] * 2 >= n,
                    'arr': round(statistics.median(r[0] for r in rel)) if rel else None,
                    'dep': round(statistics.median(r[1] for r in rel)) if rel else None,
                    'back_dep': round(statistics.median(r[0] for r in relb)) if relb else None,
                    'req': bool(rel + relb) and all(r[2] for r in rel + relb)})
    return out


def trip_row(t, merged):
    return {'t': hm(t['stops'][0]['dep']), 'm': t['stops'][0]['dep'], 'nums': t['nums'], 'cat': t['cat'],
            'to': t['stops'][-1]['name'], 'arr': hm(t['stops'][-1]['arr']),
            'dest': t['destination'] or t['to_foreign'], 'orig': t['origin'] or t['from_foreign'],
            'op': CFG['carriers'].get(t['rus'][0][0], t['rus'][0][0]), 'merged': merged}


def main():
    lines = json.load(open(os.path.join(ROOT, 'data', 'derived', 'lines.json'), encoding='utf-8'))
    res, not_lines = [], []
    for l in lines:
        ntrips = sum(len(v['trips']) for v in l['variants'])
        badge, name = OV['line_names'].get(l['code'], [None, None])
        mv = l['variants'][0]
        if not name:
            name = f"{mv['a']} – {mv['b']}"
        if ntrips < 2:
            t = mv['trips'][0]
            not_lines.append({'code': l['code'], 'name': name, 'trip': trip_row(t, False), 'from': t['stops'][0]['name']})
            continue
        modelled, merged = [], []
        for k, v in enumerate(l['variants']):
            v['n_window'] = len([t for t in v['trips'] if in_win(t)])
            ends_deps = collections.defaultdict(list)
            for t in v['trips']:
                ends_deps[t['stops'][0]['name']].append(t['stops'][0]['dep'])
            busiest = max(ends_deps.values(), key=lambda d: len([x for x in d if S0 <= x < S1]))
            rhythm = standard(busiest)
            v['rhythm'] = rhythm.get('fits', 0) >= 2 and rhythm.get('I', 1440) <= 240
            v['peakdep'] = any(BRANCH_PEAK[0] <= t['stops'][0]['dep'] < BRANCH_PEAK[1] for t in v['trips'])
            if k == 0 or (v['n_window'] >= 3 and v['peakdep'] and v['rhythm']):
                modelled.append(v)
            else:
                merged.append(v)
        for v in modelled:
            v['merged'] = []
        unmodelled = []
        for v in merged:
            names = {s['name'] for t in v['trips'] for s in t['stops']}
            cand = [m for m in modelled if {v['a'], v['b']} & {m['a'], m['b']}]
            if not cand:
                unmodelled.append(v)
                continue
            m = max(cand, key=lambda m: len(names & {s['name'] for t in m['trips'] for s in t['stops']}))
            m['merged'].append(v)
        sims = []
        for v in modelled:
            a, b = v['a'], v['b']
            own = v['trips']
            deps = {a: [], b: []}
            rows = {a: [], b: []}
            for t in own:
                e = t['stops'][0]['name']
                deps[e].append(t['stops'][0]['dep'])
                rows[e].append(trip_row(t, False))
            for mv2 in v['merged']:
                for t in mv2['trips']:
                    e = t['stops'][0]['name']
                    if e in deps:
                        deps[e].append(t['stops'][0]['dep'])
                        rows[e].append(trip_row(t, True))
            win = {e: [x for x in deps[e] if S0 <= x < S1] for e in (a, b)}
            tt = {e: standard(deps[e], other_has_window=bool(win[b if e == a else a])) for e in (a, b)}
            for e in (a, b):
                rows[e].sort(key=lambda r: r['m'])
            # one interval per Simutrans line, chosen on both ends together (user, 29 Sep: Kysučan is 4-hourly,
            # the busier end alone made it 2-hourly); each end then takes its best minute at that interval
            timed = [e for e in (a, b) if tt[e]['kind'] != 'untimed' and len(win[e]) >= 2]
            if len(timed) == 2 and tt[a]['I'] != tt[b]['I']:
                I = pick_headway([sorted(set(win[e])) for e in timed])
                for e in (a, b):
                    if tt[e]['I'] != I:
                        tt[e] = standard(deps[e], I=I) | {'forced': True}
            elif tt[a]['kind'] != 'untimed' and tt[b]['kind'] != 'untimed' and tt[a]['I'] != tt[b]['I']:
                lead, follow = (a, b) if len(win[a]) >= len(win[b]) else (b, a)
                tt[follow] = standard(deps[follow], I=tt[lead]['I']) | {'forced': True}
            pattern = stop_pattern(own, a)
            foreign = collections.Counter()
            for t in own:
                for x in (t['destination'] or t['to_foreign'], t['origin'] or t['from_foreign']):
                    if x:
                        foreign[x] += 1
            ops = collections.Counter(CFG['carriers'].get(t['rus'][0][0], t['rus'][0][0]) for t in own)
            # most common terminal outside the Czech Republic at each end (user, 29 Sep): design the line to it
            ext = {}
            for e in (a, b):
                far, border = collections.Counter(), collections.Counter()
                for t in own:
                    if t['stops'][-1]['name'] == e and (t['destination'] or t['to_foreign']):
                        far[fterm(t['destination'] or t['to_foreign'])] += 1
                        if t['to_foreign']:
                            border[t['to_foreign']] += 1
                    elif t['stops'][0]['name'] == e and (t['origin'] or t['from_foreign']):
                        far[fterm(t['origin'] or t['from_foreign'])] += 1
                        if t['from_foreign']:
                            border[t['from_foreign']] += 1
                n = sum(far.values())
                if n * 2 >= len(own):
                    term, c = far.most_common(1)[0]
                    ext[e] = {'terminal': term, 'trips': c, 'crossing': n, 'of': len(own),
                              'border': border.most_common(1)[0][0] if border else None,
                              'others': [[x, k2] for x, k2 in far.most_common()[1:]]}
            rate = next((tt[e]['I'] for e in (a, b) if tt[e]['kind'] != 'untimed'), None)
            stays = {e: long_stays(own, e, rate) for e in (a, b)}
            sims.append({'a': a, 'b': b, 'trips': len(own), 'n_window': v['n_window'], 'ext': ext, 'stays': stays,
                         'cats': collections.Counter(t['cat'] for t in own).most_common(),
                         'ops': ops.most_common(), 'foreign': foreign.most_common(),
                         'tt': tt, 'deps': rows, 'pattern': pattern,
                         'merged': [{'a': m['a'], 'b': m['b'], 'trips': len(m['trips']),
                                     'rows': [trip_row(t, True) for t in m['trips']]} for m in v['merged']]})
        # common standard at a terminus shared by several Simutrans lines: all the line's departures from it
        ends = collections.Counter(e for v in modelled for e in (v['a'], v['b']))
        for v in l['variants']:
            for t in v['trips']:
                t['key'] = v['a'] + '|' + v['b']
        trunks = []
        for x, n in ends.most_common():
            if n < 2:
                continue
            ts = [t for v in l['variants'] for t in v['trips'] if t['stops'][0]['name'] == x]
            st = standard([t['stops'][0]['dep'] for t in ts])
            dest = collections.Counter(t['stops'][-1]['name'] for t in ts if in_win(t))
            far = collections.Counter(t['destination'] or t['to_foreign'] for t in ts if (t['destination'] or t['to_foreign']))
            links, sw = chain([t for v in l['variants'] for t in v['trips']], x)
            share = sw / links if links else 0
            verdict = ('alternate' if share >= 0.75 else 'mixed' if share > 0.3 else 'stay')
            trunks.append({'from': x, 'tt': st, 'to': dest.most_common(), 'foreign': [[fterm(k), n] for k, n in far.most_common()],
                           'links': links, 'switch': sw, 'verdict': verdict})
        if not OV['line_names'].get(l['code']):
            outs = []
            for v in modelled:
                if l['A'] in (v['a'], v['b']):
                    b = v['b'] if v['a'] == l['A'] else v['a']
                    if b not in outs:
                        outs.append(b)
            name = f"{l['A']} – {' / '.join(outs)}" if outs else name
        res.append({'code': l['code'], 'trunks': trunks, 'badge': badge or ('R' if l['code'].startswith('R') else 'Ex'), 'kind': l['kind'],
                    'name': name, 'cats': l['cats'], 'trips': ntrips, 'sims': sims,
                    'unmodelled': [{'a': v['a'], 'b': v['b'], 'rows': [trip_row(t, False) for t in v['trips']]} for v in unmodelled]})
    json.dump({'lines': res, 'not_lines': not_lines}, open(os.path.join(ROOT, 'data', 'derived', 'schedule.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    for l in res:
        print(l['code'], l['name'], l['trips'])
        for s in l['sims']:
            print('   ', s['a'], '–', s['b'], s['trips'], '| merged', [(m['a'], m['b'], m['trips']) for m in s['merged']])
            for e in (s['a'], s['b']):
                t = s['tt'][e]
                print('       ', e, '|', t['kind'], t.get('text'), f"{t.get('fits')}/{t.get('of')} ±{t.get('dev')}", t.get('basis'), 'FORCED' if t.get('forced') else '', '| win', ' '.join(t.get('window', [])), '| off', t.get('offpattern'), '| empty', t.get('empty'))
        if l['unmodelled']:
            print('    NOT MODELLED', [(v['a'], v['b']) for v in l['unmodelled']])
    print('not lines', [(n['code'], n['trip']['nums']) for n in not_lines])


if __name__ == '__main__':
    main()
