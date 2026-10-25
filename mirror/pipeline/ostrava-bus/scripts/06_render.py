"""derived/*.json + config + templates/page.html -> the published HTML in the project root.

Same layout, vehicle cell and sticky controls as the Ostrava tram and trolleybus sheets. Two states:
- pending (no live snapshots of the vehicle day yet): each Simutrans line shows its need, and the depots list
  their active fleet grouped by type;
- observed: each Simutrans line lists its buses (number · depot / full type · length / pak core, with the course),
  the depots list them per line, and the spares follow.
"""
import collections, glob, html, json, os, re
from lib import CONFIG, ROOT, PROJECT, load, make_nm, hm, loop_shift, even_interval

C = CONFIG; E = html.escape; nm0 = make_nm(C); PK = C['pak']; AL = C['terminus_alias']
def al(s): return AL.get(s, s)
fleet = {int(k): v for k, v in load('fleet.json').items()}
lines = load('lines.json'); R = load('roster.json'); SCH = load('schedule.json'); CLS = load('line_class.json')
LIVE = {int(k): v for k, v in load('live.json')['cars'].items()}
BR = {L: B['branches'] for L, B in R['branches'].items()}; OTH = {L: B['others'] for L, B in R['branches'].items()}
roster = R['roster']; OBS = {int(k): v for k, v in R['observed'].items()}
PENDING = not roster or not any(roster.values())
MODE = R.get('mode', 'peak'); PROV = MODE == 'provisional'; LDAY = R.get('live_day')
WHY = {(a['line'], a['car']): a['why'] for a in R['added']}
PL = C['live']['provisional']['label']
# ODIS lines of other operators at the hub (07_odis.py; owner, 20 Oct 2026): rendered with the same card code, last
OD = load('odis.json') if os.path.exists(os.path.join(ROOT, 'data', 'derived', 'odis.json')) else None
ODO = OD['order'] if OD else []
if OD:
    for L in ODO:
        lines[L] = OD['lines'][L]; SCH[L] = OD['schedule'][L]; BR[L] = OD['branches'][L]['branches']; OTH[L] = OD['branches'][L]['others']; roster[L] = OD['roster'][L]
    for n, v in OD['fleet'].items(): fleet[n] = v
    for a in OD['added']: WHY[(a['line'], a['car'])] = a['why']
    for L, us in (OD.get('surplus') or {}).items(): R.setdefault('surplus', {})[L] = us
OBSO = (OD or {}).get('observed', {}); ODLV = (OD or {}).get('live') or {}   # ODIS buses seen on the ODIS live map (07_odis.py)
def seen_at(n): return OBS[n]['first'] if n in OBS else OBSO[n]['seen']
order = sorted([L for L in BR if L not in ODO], key=int); PEAK = C['peak_label']; W = R.get('window') or C['live']['window']
DEPS = list(C['fleet']['depots'].items())                     # [(code, name)]
TORD = list(C['types'])

def tkey(u): return (TORD.index(u[0]) if u[0] in TORD else 99, u[1])
def length(n): return fleet[n].get('len') or next((r[3] for r in C['type_rules'] if r[0] == fleet[n]['type']), '?')
def paint(n):
    m = re.search(r'nátěr:\s*(.*?)\s*(\*|\{|$)', fleet[n]['note']); p = m.group(1) if m else ''
    if p.startswith('CVR'): return 'advertising wrap ' + p[3:].strip(' ,').split(',')[0], None
    for key, name, liv in PK['paint_rules']:
        if key in p: return name, liv
    return (p or 'unknown paint'), None
LIVN = PK['livery_names']
def pak(n):
    fn = fleet[n]['full']
    if fleet[n].get('state') == 'odis' and fn in PK.get('odis_objects', {}):   # VZ-ODIS-bus (pak session, 20 Oct 2026)
        pn = fleet[n].get('paint') or 'unknown paint'
        want = next((l for k, l in PK['odis_paint'] if k in pn), '3csadbilozelena')
        o = PK['odis_objects'][fn]; e = o.get(want) or next(iter(o.values()))
        liv = e[3] if len(e) > 3 else want; full = f"VZ-ODIS-{e[0]}-{liv}-{e[0]}"
        PK['lengths'][e[0]] = e[1]
        return dict(head=full, chain=full, paint=pn, liv=liv, fam=e[0], exact=e[2] and liv == want,
                    core=('≈ ' if not (e[2] and liv == want) else '') + e[0] + ' · ' + LIVN[liv].split(' (')[0],
                    typereason='' if e[2] else PK['subst_reason'].get(fn, 'nearest object'))
    d = PK['objects'].get(fn); pn, want = paint(n)
    if not d: return dict(head=None, paint=pn, core='no object', exact=False, typereason='the pak has no object for ' + fn)
    fam, livs, parts, exact = d
    liv = want if want in livs else livs[0]
    return dict(head=f"{PK['prefix']}{fam}-{liv}-{parts[0]}", chain=' → '.join(f"{PK['prefix']}{fam}-{liv}-{x}" for x in parts),
                paint=pn, liv=liv, fam=fam, exact=exact, core=('≈ ' if not exact else '') + parts[0] + (f' · {LIVN[liv].split(" (")[0]}' if len(livs) > 1 else ''),
                typereason='' if exact else PK['subst_reason'].get(fn, 'nearest object'))
def depcode(n): return fleet[n].get('depot_code') or 'AH'
def vnum(nums): return f'<span class="veh" data-v="{"+".join(map(str, nums))}">{" + ".join(map(str, nums))}</span>'
def cell(nums):
    ps = [pak(n) for n in nums]
    return (f'<div class="num">{vnum(nums)} <span class="dp d-{depcode(nums[0])}">{E(fleet[nums[0]]["depot"])}</span></div>'
            f'<div class="vt">{E(" + ".join(fleet[n]["full"] for n in nums))} · {E(" + ".join(length(n) for n in nums))}{(" · plate " + E(fleet[nums[0]]["plate"])) if fleet[nums[0]].get("plate") else ""}</div>'
            f'<div class="pak{"" if all(p["exact"] for p in ps) else " subst"}">{E(" + ".join(p["core"] for p in ps))}</div>')
def brname(b): return f"{b['a']} ⇄ {b['b']}"
def slname(L, bi):
    un = [i for i, b in enumerate(BR[L]) if not b.get('name')]   # automatic branches; a hand-set line carries its own name
    return BR[L][bi].get('name') or (f"{L}{'ABCDEF'[un.index(bi)]}" if len(un) > 1 else L)
def title(L):
    bs = BR[L]; a0 = bs[0]['a']
    if all(a0 in (b['a'], b['b']) for b in bs):
        return a0 + ' – ' + ' / '.join(b['b'] if b['a'] == a0 else b['a'] for b in bs)
    return ' / '.join(f"{b['a']} – {b['b']}" for b in bs)
def later_lines(n, L):
    out = []
    for x in LIVE.get(n, []):
        if x[0] > W[1] and x[1] != L and x[1] not in out: out.append(x[1])
    return out

CHECKS = []; CCHECKS = []   # circuit legs off the real departures
TRIPS = load('trips.json'); TRIPS.update(OD['trips'] if OD else {}); FW = (C['peak_minute'] - 30, C['peak_minute'] + 90)
PEAKS = load('peaks.json'); PEAKS.update(OD.get('peaks', {}) if OD else {})
def vt(g, k):
    """label of a circuit leg's path (two paths between the same termini, lib.path_variants)"""
    sk = g.get(k + '_skip')
    return (('not via ' if sk == 'notvia' else 'non-stop to ' if sk else 'via ') + nm0(g[k + '_via'])) if g.get(k + '_via') else None
def T0_(L): return PEAKS.get(L, {}).get('anchor', C['peak_minute'])
def FW_(L): return (T0_(L) - 30, T0_(L) + 90)
def hwtext(L, v):
    """headway as the Simutrans pattern models it (gaps between its slots), else the timetable's commonest gap"""
    if any(b.get('hand') for b in BR[L]):   # hand-set lines: the slots of every Simutrans line in this direction
        f_, t_ = al(nm0(v['fr'])), al(nm0(v['to'])); sl = collections.defaultdict(int)
        for b in BR[L]:
            for g in b.get('legs', []):
                if (g['X'], g['Y']) == (f_, t_): sl[b['period']] += 1
                elif (g['Y'], g['X']) == (f_, t_) and g['back_slot'] is not None: sl[b['period']] += 1
        if len(sl) == 1:
            (I, k), = list(sl.items())
            return f"every {I} min" if k == 1 else (f"{k} an hour" if I == 60 else f"{k} every {I} min")
        if not sl and all(b.get('hand') for b in BR[L]): return 'not on a Simutrans line'
    p = next((p for p in SCH[L] if nm0(p['fr']) == nm0(v['fr']) and nm0(p['to']) == nm0(v['to']) and p['every']), None)
    if p:
        r = p['real']; gaps = sorted({((r[(i + 1) % len(r)] - r[i]) % p['every']) or p['every'] for i in range(len(r))})
        return ('about ' if 'approx' in p else '') + 'every ' + '/'.join(map(str, gaps)) + ' min'
    return f"every {v['hw']} min" if v['hw'] else 'single trip'
def srow_fit(L, p):
    """one schedule row: typed values with the real minute under them (Prague style) and a Fit cell"""
    if p.get('circuit_leg') and len(p['real']) > 1:   # evenly spaced circuit slots as a plain interval (owner, 20 Oct 2026)
        I_, r_ = even_interval(p['every'], p['real'])
        if I_ != p['every']: p = dict(p, every=I_, real=r_, set=loop_shift(I_, r_, C['all_termini_are_loops']))
    deps = sorted(set([t['dep'] for t in TRIPS[L] if nm0(t['fr']) == p['fr'] and nm0(t['to']) == p['to']] + p.get('merged', [])))
    if p.get('circuit_leg'):
        A_ = lambda x: AL.get(x, x)
        ts_ = [t for t in TRIPS[L] if A_(nm0(t['fr'])) == A_(p['fr']) and A_(nm0(t['to'])) == A_(p['to'])]
        if not p.get('vdeps'): deps = sorted(t['dep'] for t in ts_)
        if ts_:   # the stops the trips really start and end at (49: out to sad B. Němcové, back from Vozovna trolejbusů)
            p = dict(p, fr=collections.Counter(nm0(t['fr']) for t in ts_).most_common(1)[0][0], to=collections.Counter(nm0(t['to']) for t in ts_).most_common(1)[0][0])
    if p.get('vdeps'): deps = p['vdeps']   # a leg on one of two paths between the same termini (28)
    W_ = p.get('fitwin') or FW_(L)   # sparse branches are fitted over 13:00-19:00
    band = [x for x in deps if W_[0] <= x < W_[1]]
    if p.get('circuit_leg'):
        w_ = p.get('fitwin') or FW_(L); realw = [x for x in deps if w_[0] <= x < w_[1]]
        sl = [t for t in range(w_[0], w_[1]) if t % p['every'] in p['real']]
        hit = sum(1 for t in sl if deps and min(abs(t - x) for x in deps) <= 3)
        if hit < len(sl): p['_miss'] = (hit, len(sl))
        lead = 'set by hand; ' if p.get('hand') else f"stop {p['circuit_leg']} of the circuit; "
        fit = (f"{lead}{hit} of {len(sl)} slots in {hm(w_[0])}–{hm(w_[1])} on a real departure (±3 min)"
               + f"<small>real {hm(w_[0])}–{hm(w_[1])}: {', '.join(hm(x) for x in realw) or 'none'}</small>")
    elif p.get('interleave'):
        il = p['interleave']; w_ = il.get('window') or list(FW_(L))
        realw = [x for x in deps if w_[0] <= x < w_[1]]
        fit = (f"{'far end of a branch ' if il.get('far') else ''}interleaved at {E(il['at'])} with {E(', '.join(il['with_']) or 'the other branches')}"
               + (f"; placed between the other branch&#x27;s buses passing here at {', '.join(f':{x:02d}' for x in il['passing'])}" if il.get('passing') else '') +
               f"{': exact' if not il['dev'] else ', up to ' + str(il['dev']) + ' min off'} in {hm(w_[0])}–{hm(w_[1])}"
               f"<small>real {hm(w_[0])}–{hm(w_[1])}: {', '.join(hm(x) for x in realw) or 'none'}</small>")
    elif p.get('override'):
        ow_ = p['override'].get('window') or [T0_(L), T0_(L) + 90]
        fit = (f"set by the owner: every {p['every']}, spaced from the other branch on the shared section; real departures "
               f"{'exact' if not p['override']['dev'] else 'up to ' + str(p['override']['dev']) + ' min off a slot'} in {hm(ow_[0])}–{hm(ow_[1])}"
               f"<small>real {hm(ow_[0])}–{hm(ow_[1])}: {', '.join(hm(x) for x in deps if ow_[0] <= x <= ow_[1]) or 'none'}"
               + (f"; more than 3 min off: {', '.join(hm(x) for x in p['override']['extra'])}" if p['override'].get('extra') else '') + "</small>")
    elif p.get('manual'):
        fit = f"set by the owner: the 14:00 pattern, exact {hm(p['first'])}–{hm(p['last'])} ({p['n']} dep.)"
    elif 'approx' in p:
        fit = (f"approximate, up to {p['approx']} min off" + (" (irregular: no even pattern fits)" if p['approx'] >= p['every'] // 3 else '') +
               f"<small>real {hm(W_[0])}–{hm(W_[1])}: {', '.join(hm(x) for x in band) or 'none'}</small>")
    else:
        out = [x for x in deps if FW[0] - 30 <= x < FW[1] + 30 and not p['first'] <= x <= p['last']]
        ex_ = p.get('exactified') or {}
        fit = (f"exact {hm(p['first'])}–{hm(p['last'])} ({p['n']} dep.)"
               + (f", read over the whole day as it repeats" + (f"; {', '.join(hm(x) for x in ex_['displaced'])} is a few minutes off its slot" if ex_.get('displaced') else '')
                  if ex_.get('whole_day') else '')
               + (f"<small>outside the run: {', '.join(hm(x) for x in out)}</small>" if out else ''))
    slots = len(p['real']) * (W_[1] - W_[0]) // p['every']; chk = 'approx' in p and slots > len(band)
    if p.get('_miss'):
        chk = True; CCHECKS.append((L, p))
        fit += (f"<div class='chkn'><b>Check:</b> {p['_miss'][1] - p['_miss'][0]} slot{'s' if p['_miss'][1] - p['_miss'][0] > 1 else ''} more than 3 min off a real departure (real times above). "
                + ("The real timetable is irregular here; the slots follow the method&#x27;s best fit (see the line note).</div>" if p.get('hand') else
                   "A merged row would serve one path only.</div>" if p.get('paths') else f"As separate branch lines: {p['sep']} buses.</div>"))
    if chk and 'approx' in p:
        al = p.get('alt'); fmt = lambda x: f"every {x['every']}, Offset {x['set'][0]}" + (f", Also at {', '.join(map(str, x['set'][1:]))}" if len(x['set']) > 1 else '')
        alt = (f" Slower option: {fmt(al)} (real {', '.join(f':{(v + 1) % al['every']:02d}' for v in al['set'])}), up to {al['approx']} min off."
               if al and al['every'] > p['every'] else '')
        fit += (f"<div class='chkn'><b>Check:</b> {slots} slots in {hm(W_[0])}–{hm(W_[1])} against {len(band)} real departures, so "
                f"{slots - len(band)} slot{'s' if slots - len(band) > 1 else ''} would run empty or spread the buses thinner.{E(alt)} "
                f"Switch both ends of the line together.</div>")
        CHECKS.append((L, p, slots, band, al))
    if p.get('refit'):
        rf = p['refit']; nh = len(p['real']) * 60 / p['every']
        fit += (f"<small>matched to the other end ({nh:g} an hour); this end alone fitted every {rf['every']} "
                f"({', '.join(f':{x:02d}' for x in rf['real'])}) {hm(rf['first'])}–{hm(rf['last'])}</small>")
    lp_ = p.get('loop', C['all_termini_are_loops'])
    real_o = f"<small class='real'>real {rtxt(p, p['set'][0], lp_)}</small>"
    real_a = f"<small class='real'>real {', '.join(rtxt(p, v, lp_) for v in p['set'][1:])}</small>" if len(p['set']) > 1 else ''
    return (f"<tr{' class=chk' if chk else ''}><td>{E(p['fr'])} &rarr; {E(p['to'])}{f"<span class='lp lnt'>{E(p['note'])}</span>" if p.get('note') else ''}<span class='lp'>{'1 min early' if lp_ else 'timetable minute'}</span></td>"
            f"<td class='n sv'>{p['every']}</td><td class='n sv'>{p['set'][0]}{real_o}</td><td class='sv'>{', '.join(map(str, p['set'][1:])) or '&mdash;'}{real_a}</td><td class='n'>auto</td><td class='fit'>{fit}</td></tr>")

def rtxt(p, v, loop):
    """real departure for a typed value: the minute where the interval divides 60, else the first clock time from 15:30"""
    I = p['every']; r = (v + 60 + (1 if loop else 0)) % I
    if 60 % I == 0: return str(r)
    s0 = (p.get('fitwin') or [930])[0]; t = s0 + ((r - s0) % I); return f"{t // 60}:{t % 60:02d}, every {I}"
cards = []; perline = {}; pertype = collections.Counter()
for L in order + ODO:
    ros = roster[L]; V = lines[L]['variants']; perline[L] = len(ros)
    for u in ros: pertype[u[0]] += 1
    rows = ''.join(f"<tr><td>{E(v['fr'])}</td><td class='arr'>&rarr;</td><td>{E(v['to'])}</td><td class='n'>{hwtext(L, v)}</td>"
                   f"<td class='n mono'>{' '.join(f':{m:02d}' for m in v['min_peak_hour']) or '&mdash;'}</td><td class='n'>{v['rt']} min</td></tr>" for v in V)
    lh = f'{T0_(L) // 60:02d}'
    if L in C.get('line_overrides', {}):      # the owner's model hour: the table shows the trips of that window
        def ohw(ts):
            d = sorted(t['dep'] for t in ts); g = collections.Counter(y - x for x, y in zip(d, d[1:]))
            return (f"every {g.most_common(1)[0][0]} min" if g.most_common(1)[0][0] <= 60 else f"{len(d)} trips") if g else "single trip"
        ow = C['line_overrides'][L]['window']; lh = None; grp = collections.defaultdict(list)
        for t in TRIPS[L]:
            if ow[0] <= t['dep'] <= ow[1]: grp[(nm0(t['fr']), nm0(t['to']))].append(t)
        rows = ''.join(f"<tr><td>{E(a)}</td><td class='arr'>&rarr;</td><td>{E(b)}</td><td class='n'>{ohw(ts)}</td>"
                       f"<td class='n mono'>{' '.join(hm(d) for d in sorted(t['dep'] for t in ts))}</td>"
                       f"<td class='n'>{round(sum(t['arr'] - t['dep'] for t in ts) / len(ts))} min</td></tr>" for (a, b), ts in sorted(grp.items(), key=lambda x: min(t['dep'] for t in x[1])))
    sch = ''; placed = set()
    def srow(p):
        if not p['every']:
            into = f" Its minutes are folded into the {E(p['fr'])} &rarr; {E(p['into'])} row." if p.get('into') else ''
            return f"<tr class='all'><td>{E(p['fr'])} &rarr; {E(p['to'])}</td><td colspan='5'>variant or garage run at {', '.join(hm(x) for x in p['single'])}, not scheduled.{into}</td></tr>"
        return srow_fit(L, p)
    if L in C.get('line_overrides', {}):
        sch += f"<tr class='brh'><td colspan='6'>Simutrans line {L}, one circuit: {E(' → '.join(C['line_overrides'][L]['route']))}</td></tr>"
        placed = set(range(len(SCH[L])))
        sch += ''.join(srow(p) for p in SCH[L])
    if any(b.get('legs') for b in BR[L]):
        LP = C['all_termini_are_loops']
        for bi, b in enumerate(BR[L]):
            if not b.get('legs'): continue   # an automatic branch beside a hand-set line (57): rendered below
            I = b['period']; legs = b['legs']; Ys = list(dict.fromkeys(g['Y'] for g in legs))
            if len(Ys) == 1 and not b.get('paths'):   # one branch: its slots as one row each way
                sch += f"<tr class='brh'><td colspan='6'>Simutrans line {slname(L, bi)}: {E(legs[0]['X'])} ⇄ {E(Ys[0])}</td></tr>"
                outs = sorted(g['out_slot'] for g in legs); backs = sorted(dict.fromkeys(g['back_slot'] for g in legs if g['back_slot'] is not None))
                hd = dict(hand=True, vdeps=legs[0]['out_deps'], fitwin=b.get('fitwin')) if b.get('hand') else {}
                sch += srow_fit(L, dict(fr=legs[0]['X'], to=Ys[0], every=I, real=outs, set=loop_shift(I, outs, LP), circuit_leg=1, sep=b['sep_need'], **hd))
                if legs[0].get('back_untimed'):   # empty return (bus schedule method, Step 6)
                    sch += (f"<tr><td>{E(Ys[0])} &rarr; {E(legs[0]['X'])}<span class='lp'>empty return</span></td><td class='n sv'>0</td><td class='n sv'>&mdash;</td><td class='sv'>&mdash;</td><td class='n'>auto</td>"
                            f"<td class='fit'>no timetable: no trip runs back in the afternoon, so the bus returns empty ({legs[0]['rt_back']} min, {'as the trips back at other times' if legs[0]['back_deps'] else 'as long as the way out: no trip ever runs back that way'}) and waits at {E(legs[0]['X'])} for its next slot</td></tr>")
                else:
                    if b.get('hand'): hd['vdeps'] = legs[0]['back_deps']
                    sch += srow_fit(L, dict(fr=Ys[0], to=legs[0]['X'], every=I, real=backs, set=loop_shift(I, backs, LP), circuit_leg=2, sep=b['sep_need'], **hd))
            else:
                vv = lambda g, k: f" ({vt(g, k)})" if g.get(k + '_via') else ''
                route = [legs[0]['X']] + [x for g in legs for x in (g['Y'] + vv(g, 'out'), g['X'] + vv(g, 'back'))]
                sch += f"<tr class='brh'><td colspan='6'>Simutrans line {slname(L, bi)}, one circuit: {E(' → '.join(route))}</td></tr>"
                k = 0
                for g in legs:
                    k += 1; sch += srow_fit(L, dict(fr=g['X'], to=g['Y'], every=I, real=[g['out_slot']], set=loop_shift(I, [g['out_slot']], LP), circuit_leg=k, sep=b['sep_need'], paths=b.get('paths'),
                                                    note=vt(g, 'out') if not b.get('hand') else f"{vt(g, 'out')} (as {'/'.join(g['out_lines'])})", vdeps=g.get('out_deps'), hand=b.get('hand')))
                    k += 1; sch += srow_fit(L, dict(fr=g['Y'], to=g['X'], every=I, real=[g['back_slot']], set=loop_shift(I, [g['back_slot']], LP), circuit_leg=k, sep=b['sep_need'], paths=b.get('paths'),
                                                    note=vt(g, 'back') if not b.get('hand') else f"{vt(g, 'back')} (as {'/'.join(g['back_lines'])})", vdeps=g.get('back_deps'), hand=b.get('hand')))
        pairs_ = {frozenset((g['X'], g['Y'])) for b in BR[L] for g in b.get('legs', [])}
        placed = {i for i, p in enumerate(SCH[L]) if frozenset((al(p['fr']), al(p['to']))) in pairs_}
    for bi, b in enumerate(BR[L] if L not in C.get('line_overrides', {}) else []):
        if b.get('legs'): continue
        if len(BR[L]) > 1: sch += f"<tr class='brh'><td colspan='6'>Simutrans line {slname(L, bi)}: {E(brname(b))}</td></tr>"
        for i, p in enumerate(SCH[L]):
            if i not in placed and {al(p['fr']), al(p['to'])} == {b['a'], b['b']}: sch += srow(p); placed.add(i)
    rest = [p for i, p in enumerate(SCH[L]) if i not in placed]
    if rest: sch += "<tr class='brh'><td colspan='6'>Other variants</td></tr>" + ''.join(srow(p) for p in rest)
    stopsd = ''; seen = set(); ppairs = set()
    for b in BR[L]:
        for g in b.get('legs', []):
            for k, a_, b_ in (('out', g['X'], g['Y']), ('back', g['Y'], g['X'])):
                if g.get(k + '_stops') and tuple(g[k + '_stops']) not in seen:
                    seen.add(tuple(g[k + '_stops'])); ppairs.add((a_, b_)); st = [nm0(x) for x in g[k + '_stops']]
                    stopsd += f"<p><b>{E(a_)} &rarr; {E(b_)} {E(vt(g, k) or "")}</b> ({len(st)} stops): {E(' · '.join(st))}</p>"
    for v in V:
        if tuple(v['stops']) in seen or v['n'] < 2 or (al(v['fr']), al(v['to'])) in ppairs: continue
        seen.add(tuple(v['stops']))
        stopsd += f"<p><b>{E(v['fr'])} &rarr; {E(v['to'])}</b> ({len(v['stops'])} stops): {E(' · '.join(v['stops']))}</p>"
    chips = ''
    for bi, b in enumerate(BR[L]):
        head = f"Simutrans line {slname(L, bi)}: " if len(BR[L]) > 1 else ''
        how = (f"round {b['cycle']} min on its suggested slots (every {b['period']}): out on one path, back on the other, as the real buses alternate between the two paths at the far end; one Simutrans line, so both paths are served" if b.get('how') == 'circuit' and b.get('paths') and any(g.get('back_via') for g in b['legs']) else
               f"round {b['cycle']} min on its suggested slots (every {b['period']}): out via {', '.join(dict.fromkeys(nm0(g['out_via']) for g in b['legs'] if g.get('out_via')))}, back on the line's common route; the real departures alternate between the outward paths, and each path is its own Simutrans line" if b.get('how') == 'circuit' and b.get('paths') else
               f"round {b['cycle']} min on its suggested slots (every {b['period']}); the line as {len(BR[L])} Simutrans line{'s' if len(BR[L]) > 1 else ''} needs {sum(x['need'] for x in BR[L])} against {b['sep_need']} as separate branch lines" if b.get('how') == 'circuit' else
               b['how'] if b.get('override') or b.get('hand') else
               f"round {b['cycle']} min on the suggested {'approximate ' if b.get('approx') else ''}pattern (every {b['pattern_every']}): {b['runtimes'][0]} + {b['runtimes'][1]} min running, waits {b['waits'][1]} and {b['waits'][0]} min at the termini" if b['how'] == 'pattern' else
               f"round trip {b['cycle']} min with 3 min layovers" if b['cycle'] else 'buses the timetable chains at 16:00')
        ext = f"; includes {b['variant_extra']} for the line's other variants" if b.get('variant_extra') else ''
        if PENDING:
            sub = f"{head}{brname(b)} · {b['need']} needed ({how}{ext})"
            chips += f'<p class="brsub">{E(sub)}</p><p class="need">Vehicles pending: filled from the live feed on {E(C["vehicle_day_label_en"])}.</p>'
        else:
            us = [u for u in ros if u[3] == bi]
            seenw = f"seen {PL}" if PROV else 'seen live at the peak'
            if L in ODO: seenw = f"seen on the ODIS live map at {hm(T0_(L))} on {ODLV.get('label', '')}" if ODLV else 'recorded on the vehicle day: no record exists, all designed from the line’s records'
            ownw = f", {b['owner']} the owner's choice of type" if b.get('owner') else ''
            sub = f"{head}{brname(b)} · {b['assigned']} assigned ({b['observed']} {seenw}{ownw}), {b['need']} needed ({how}{ext})" + (f" · {b['surplus']} more seen, not needed" if b.get('surplus') else '')
            def chip(u):
                t, nums, flag, _, course = u
                seen_ = any(OBS.get(n, {}).get('line') == L or OBSO.get(n, {}).get('line') == L for n in nums)
                if flag == 'designed':
                    extra = f'<div class="addn">designed, not recorded: {E(WHY.get((L, nums[0]), "").split(";")[0])}</div>'
                elif flag == 'owner':
                    rep = next((x for x in R.get('surplus', {}).get(L, []) if len(x) > 5 and x[5] == nums[0]), None)
                    extra = '<div class="addn">owner’s choice of type' +(f', in place of {rep[1][0]} (course {rep[4]})' if rep else '') + '</div>'
                elif flag == 'evening':
                    extra = f'<div class="vt">course {course} · seen {E(OBS[nums[0]]["first"])} on {E(PL.split(" ")[0] + " " + " ".join(PL.split(" ")[1:3]))}, not yet confirmed at the peak</div>'
                elif nums[0] in OBSO:
                    o_ = OBSO[nums[0]]
                    extra = f'<div class="vt">trip {o_["trip"]} of {E(o_["real_line"])}, {E(o_["dep"])} {E(o_["fr"])} → {E(o_["to"])}</div>'
                else:
                    extra = f'<div class="vt">course {course}</div>' if course is not None else ''
                cls = ' added' if flag == 'designed' else ' own' if flag == 'owner' else (' eve' if flag == 'evening' else (' seen' if seen_ else ''))
                return f'<li class="v{cls}">{cell(nums)}{extra}</li>'
            sur = [u for u in R.get('surplus', {}).get(L, []) if u[3] == bi]
            surli = ''.join(f'<li class="v spare">{cell(u[1])}<div class="vt">not needed · {"trip" if L in ODO else "course"} {u[4]} · seen {E(seen_at(u[1][0]))}; ' +
                            (f"replaced by {u[5]} {E(fleet[u[5]]['full'])}, the owner's choice of type" if len(u) > 5 else f'more buses seen than this line needs (one of each type kept, then the lowest {"trip numbers" if L in ODO else "courses"})') + '</div></li>' for u in sur)
            chips += f'<p class="brsub">{E(sub)}</p><ul class="vs">' + ''.join(chip(u) for u in sorted(us, key=tkey)) + '</ul>'
            if sur:   # collapsed (user, 20 Oct 2026): extra buses seen at the peak, not counted
                chips += f'<details class="nn"><summary>Not needed: {len(sur)} more bus{"es" if len(sur) > 1 else ""} seen at the peak</summary><ul class="vs">{surli}</ul></details>'
    sp = R.get('spares', {}).get(L, [])
    if sp and not PENDING:
        chips += (f'<details class="nn"><summary>Not needed: {len(sp)} more bus{"es" if len(sp) > 1 else ""} from the line’s history, {"not seen in the live feed that evening" if PROV else "free that day"} (not counted)</summary><ul class="vs">' +
                  ''.join(f'<li class="v spare">{cell([x["car"]])}<div class="vt">not needed · last on line {L} {E(x["last"])} · {x["records"]} records · {"not seen that evening" if PROV else "free that day"}</div></li>' for x in sp) + '</ul></details>')
    oth = [o for o in OTH[L]]
    othtxt0 = ''
    if L in C.get('line_overrides', {}): othtxt0 = f'<p class="lnote"><b>Modelled as at 14:00.</b> {E(C["line_overrides"][L]["why"])}</p>'
    elif PEAKS.get(L, {}).get('moved'):
        pk_ = PEAKS[L]
        othtxt0 = (f'<p class="lnote"><b>Modelled at its afternoon peak, {hm(pk_["busiest"][0])}–{hm(pk_["busiest"][1])}.</b> Its busiest 2 hours are {hm(pk_["busiest"][0])}–{hm(pk_["busiest"][1])} '
                   f'({pk_["n"]} departures, against {pk_["at_peak"]} in 15:00–17:00), so the schedule and the need follow that stretch, not 16:00. '
                   f'Buses seen live at 16:00 count; any further bus the peak needs is designed from the line&#x27;s history.</p>')
    if L in C.get('hand_lines', {}):
        h_ = C['hand_lines'][L]
        othtxt0 += (f'<p class="lnote"><b>{"Exception approved by the owner." if h_.get("exception") else "Set by hand from the whole day."}</b> {E(h_["note"])} Core points: {E(", ".join(h_["core"]))}. '
                    f'The timetables sit on the terminals only (bus schedule method, 20 Oct 2026).</p>')
    if L in ODO:
        m_ = OD['meta'][L]
        othtxt0 += (f'<p class="lnote"><b>ODIS line {L}</b> ({E(m_["operator"])}, licence {m_["code"]}, timetable version {m_["version"]}). '
                   + (f'Not in DPO&#x27;s live feed; the buses are the ones seen on the ODIS live map at {hm(T0_(L))} on {E(ODLV["label"])}, by their trip; any bus not seen is designed from the line&#x27;s seznam-autobusu records.' if ODLV else
                    f'Not in DPO&#x27;s live feed; the buses are designed from the line&#x27;s seznam-autobusu records.')
                   + (f' {m_["diversion_versions"]} diversion version(s) of the line are also valid on the day; the regular version is used.' if m_['diversion_versions'] else '') + '</p>')
    othtxt = ('<p class="lnote">Not separate Simutrans lines: ' + E('; '.join(f"{' ⇄ '.join(o['pair'])} ({o['trips']} trip{'s' if o['trips'] != 1 else ''} 15:00–18:00)" for o in oth)) + '.</p>') if oth else ''
    need = sum(b['need'] for b in BR[L])
    cnt = (need, 'buses needed at 16:00') if PENDING else (len(ros), f'buses at {hm(T0_(L))}' if L not in C.get('line_overrides', {}) else 'buses, modelled as at 14:00')
    mix = '' if PENDING else ', '.join(f"{c}× {C['types'][t][0]}" for t, c in collections.Counter(u[0] for u in ros).most_common() if t in C['types'])
    if L in ODO: mix = ', '.join(f"{c}× {t}" for t, c in collections.Counter(u[0] for u in ros).most_common()) + ' · ' + OD['meta'][L]['operator']
    sub_h = (mix + ' · ' if mix else '') + f"{len(BR[L])} Simutrans line{'s' if len(BR[L]) > 1 else ''}"
    cards.append(f"""<article class="card" id="l{L}"><header><span class="badge">{L}</span><div class="hd"><h3>{E(title(L))}</h3><p>{E(sub_h)}</p></div><div class="cnt"><b>{cnt[0]}</b><span>{cnt[1]}</span></div></header>
<div class="tw"><table class="tt"><thead><tr><th>From</th><th></th><th>To</th><th class="n">Headway</th><th class="n">{f'Leaves {lh}:xx' if lh else f'Leaves {hm(ow[0])}–{hm(ow[1])}'}</th><th class="n">Runtime</th></tr></thead><tbody>{rows}</tbody></table></div>
<div class="sched"><h4>Simutrans schedule · departures set 1 min early</h4><div class="tw0"><table class="st2"><thead><tr><th>Terminus entry</th><th class="n">Departure every (min)</th><th class="n">Offset (min)</th><th>Also at (min)</th><th class="n">Leave up to</th><th>Fit</th></tr></thead><tbody>{sch}</tbody></table></div></div>
{othtxt0}{othtxt}{chips}
<details><summary>Stops</summary>{stopsd}</details></article>""")

ocards = cards[len(order):]; cards = cards[:len(order)]

# all lines at the hub: DPO lines that stop there (links to their cards) and the ODIS cards
HUBM = C['odis']['hub_stop_match'] if OD else None
hub_dpo = [L for L in order if any(any(HUBM in nm0(x) for x in t['stops']) for t in TRIPS.get(L, []))] if OD else []
def hubrow(L, odis):
    bs = BR[L]; nd = sum(b['need'] for b in bs)
    who = OD['meta'][L]['operator'] if odis else 'DPO'
    return (f"<tr><td><a class='badge sm' href='#l{L}'>{E(L)}</a></td><td>{E(title(L))}</td><td>{E(who)}</td>"
            f"<td class='n'>{len(bs)}</td><td class='n'>{nd}</td><td>{'below' if odis else 'in Lines above'}</td></tr>")
ODISVEH = (f"They are not in DPO&#x27;s live feed. Their buses are the ones seen on the ODIS live map (mpvnet.cz) on {E(ODLV['label'])}, a different day from the DPO cards: "
           f"{E(ODLV['source'])}. Each bus at the line&#x27;s peak gives its exact trip (the map&#x27;s trip number is the timetable&#x27;s), and it goes to the Simutrans line whose slot that trip runs, "
           f"so the 442/441 circuit holds buses seen on 441. {len([n for n, o in OBSO.items() if not o['spare']])} buses are seen; "
           f"{sum(1 for a in OD['added'])} more are designed where none was seen, a real bus from the line&#x27;s own records, not seen on the map that afternoon." if ODLV else
           "They are not in DPO&#x27;s live feed, and seznam-autobusu.cz holds no record of them for the vehicle day (mostly weekend and holiday records), so every bus is designed: a real bus from the line&#x27;s own records, active in the operator&#x27;s register, covering the line&#x27;s types.")
hub = (f'''<h2 id="hranecnik">All lines at Hranečník ({len(hub_dpo) + len(ODO)})</h2>
<p class="sub">Every bus line with a stop at Hranečník on {E(C['vehicle_day_label_en'])}: the {len(hub_dpo)} DPO lines (their cards are in Lines above) and {len(ODO)} ODIS lines of other operators, whose cards follow in the same style. ODIS lines: CIS JŘ national JDF (the same export as the DPO lines), versions valid on the day; schedule, branches and needs by the same rules as the DPO lines. {ODISVEH} Their pak objects are in VZ-ODIS-bus (installed 20 Oct 2026): each bus has its own type in its real livery, 3ČSAD white-green or Havířovsko white. Trams 4, 10, 12, 13 and trolleybuses 101, 107 also serve Hranečník; they are on the tram and trolleybus sheets.</p>
<div class="types"><table class="tlist"><thead><tr><th>Line</th><th>Route</th><th>Operator</th><th class="n">Simutrans lines</th><th class="n">Needed</th><th>Card</th></tr></thead><tbody>{''.join(hubrow(L, False) for L in hub_dpo)}{''.join(hubrow(L, True) for L in ODO)}</tbody></table></div>
<div class="grid" style="margin-top:18px">{''.join(ocards)}</div>''') if OD else ''

# all lines at a hub whose ODIS lines are modelled on the regional sheets (08_hubs.py, config.hubs; owner, 25 Oct 2026): the
# DPO lines link to their cards; each ODIS line is shown as its home sheet sets it and links there. Its buses are counted on
# that sheet, not in this sheet's totals, depots or nav, so no bus is on two sheets.
CLSN = {'morning': 'morning only', 'night': 'night only', 'none': 'no trips on this day (weekend or holiday service)'}
HB = load('hubs.json')['hubs'] if os.path.exists(os.path.join(ROOT, 'data', 'derived', 'hubs.json')) else []
def slot_txt(P, r, w0=780):
    """the real departure a typed slot stands for, as on the DPO cards: the minute where P divides 60, else the first clock
    time from the start of the model hours (w0), every P"""
    if 60 % P == 0: return ':%02d' % (r % 60)
    t = w0 + (r - w0) % P; return f"{hm(t)}, every {P}"
def times_txt(ts): return ', '.join(hm(t) for t in ts) or '&mdash;'
def short_sheet(h): return h['title'].replace('ODIS Regional ', '').replace('ODIS ', '')
def mirror_card(H, x):
    hs = x['home']; sims = x['sims']; nb = sum(len(s['buses']) for s in sims); sh_ = short_sheet(hs)
    link = f'<a href="{E(hs["url"])}">{E(sh_)} sheet</a>'
    rows = chips = ''
    for s in sims:
        P = s['every']; ends = list(dict.fromkeys([s['legs'][0]['fr'], s['legs'][0]['to']]))
        rows += f"<tr class='brh'><td colspan='5'>Simutrans line {E(s['name'])}: {E(' ⇄ '.join(ends))}</td></tr>"
        for g in s['legs']:
            hb = g['hub']
            vb = {'from': 'leaves', 'to': 'reaches', 'via': 'passes'}[hb['kind']] if hb else ''
            at = (f"<b>{vb} {E(H['nav'])} {times_txt(hb['model'])}</b> (real {times_txt(hb['real'])}). " if hb and hb['model'] else
                  f"<b>{vb} {E(H['nav'])} outside the model hours.</b> " if hb else '')
            pth = (' via ' + ', '.join(g['via'])) if g['via'] else (' not via ' + ', '.join(g['notvia'])) if g['notvia'] else ''
            if g['untimed']:
                rows += (f"<tr><td>{E(g['fr'])} &rarr; {E(g['to'])}<span class='lp'>empty return</span></td><td class='n sv'>0</td><td class='n sv'>&mdash;</td><td class='sv'>&mdash;</td>"
                         f"<td class='fit'>no timetable: the bus returns empty ({g['rt']} min) and waits at the terminal for its next slot</td></tr>")
                continue
            st = g['stat']; sets = g['set']
            def rl(v): return (v + 60 + (1 if s['loop'] else 0)) % P   # the real minute of each typed value, never zipped by order
            fit = f"{st['exact']} of {st['n']} real departures over the day on the minute, {st['w3']} within 3 min (worst {st['worst']}); {g['rt']} min to the far end"
            if g.get('knot'): fit += f"; timed so the bus passes {E(g['knot']['stop'])} at {', '.join(slot_txt(P, r, s['window'][0]) for r in g['knot']['at'])}"
            if g['empty']: fit += f"<small>slot without a real departure in the model hours: {', '.join(hm(t) for t in g['empty'])}</small>"
            rows += (f"<tr{' class=chk' if g['empty'] else ''}><td>{E(g['fr'])} &rarr; {E(g['to'])}{f'<span class=\"lp lnt\">{E(pth.strip())}</span>' if pth else ''}<span class='lp'>{'1 min early' if s['loop'] else 'timetable minute'}</span></td>"
                     f"<td class='n sv'>{P}</td><td class='n sv'>{sets[0]}<small class='real'>real {slot_txt(P, rl(sets[0]), s['window'][0])}</small></td>"
                     f"<td class='sv'>{', '.join(map(str, sets[1:])) or '&mdash;'}{f'<small class=\"real\">real {'; '.join(slot_txt(P, rl(v), s['window'][0]) for v in sets[1:])}</small>' if len(sets) > 1 else ''}</td>"
                     f"<td class='fit'>{at}{fit}</td></tr>")
        nseen = sum(1 for b in s['buses'] if b['kind'] == 'seen')
        chips += (f'<p class="brsub">Simutrans line {E(s["name"])} · {len(s["buses"])} bus{"es" if len(s["buses"]) != 1 else ""} on the {E(sh_)} sheet '
                  f'({nseen} seen on the ODIS live map on {E(hs["day"])}), {s["need"]} needed · not counted on this sheet</p><ul class="vs">'
                  + ''.join(f'<li class="v {"seen" if b["kind"] == "seen" else "added"} there"><div class="num"><span class="veh" data-v="{E(b["num"])}">{E(b["num"])}</span> <span class="dp">{E(x["operator"])}</span></div>'
                            f'<div class="vt">{E(b["full"])} · {E(b["len"] or "?")}{(" · plate " + E(b["plate"])) if b.get("plate") else ""}</div>'
                            f'<div class="addn">{E(("seen " + b["why"]) if b["kind"] == "seen" else (b["why"] if (b["why"] or "").startswith("designed") else "designed: " + (b["why"] or "")))}; pak object on the {E(sh_)} sheet</div></li>' for b in s['buses']) + '</ul>')
    a_ = x.get('anchor') or {}
    when = (f" Modelled at {hm(a_['anchor'])}, set by hand on that sheet." if a_.get('set') else
            f" Modelled at its afternoon peak, {hm(a_['busiest'][0])}–{hm(a_['busiest'][1])}." if a_.get('moved') and a_.get('busiest') else '')
    note = (f'<p class="lnote"><b>Modelled, with its buses, on the {link}</b> ({E(hs["day"])}), and shown here as set there: the values are read from that sheet&#x27;s data, so the two cannot disagree. '
            f'{E(x["note"])}{when} Core points: {E(", ".join(x["core"]))}.</p>')
    if any((g['hub'] or {}).get('kind') == 'via' for s in sims for g in s['legs']):
        note += f'<p class="lnote">The line does not turn at {E(H["name"])}: it passes it, so its timetables sit on its terminals, and the minutes it passes are worked out from each slot and its own trips&#x27; running time.</p>'
    return f"""<article class="card mirror" id="h{H['id']}-{x['line']}"><header><span class="badge">{x['line']}</span><div class="hd"><h3>{E(x['name'])}</h3><p>{E(x['operator'])} · licence{'s' if len(x['codes']) > 1 else ''} {', '.join(x['codes'])} · {len(sims)} Simutrans line{'s' if len(sims) > 1 else ''} on the {link}</p></div><div class="cnt"><b>{nb}</b><span>buses, counted there</span></div></header>
<div class="sched"><h4>Simutrans schedule, as on the {E(sh_)} sheet</h4><div class="tw0"><table class="st2"><thead><tr><th>Terminus entry</th><th class="n">Departure every (min)</th><th class="n">Offset (min)</th><th>Also at (min)</th><th>At {E(H['nav'])} · fit</th></tr></thead><tbody>{rows}</tbody></table></div></div>
{note}{chips}</article>"""
hubs_html = ''
for H in HB:
    mods = [x for x in H['odis'] if x['status'] == 'modelled']; rest = [x for x in H['odis'] if x['status'] != 'modelled']
    dpo = [L for L in H['dpo'] if L in BR]
    bysheet = collections.defaultdict(list)
    for x in mods: bysheet[short_sheet(x['home'])].append(x['line'])
    def hrow(x):
        where = (f"below; modelled on the <a href=\"{E(x['home']['url'])}\">{E(short_sheet(x['home']))} sheet</a>" if x['status'] == 'modelled' else
                 f"not modelled: {E(x['reason'])} (<a href=\"{E(x['home']['url'])}\">{E(short_sheet(x['home']))} sheet</a>)" if x['status'] == 'unmodelled' else
                 '<b>on no sheet yet</b>: it would have to be modelled here')
        sims = x.get('sims', [])
        return (f"<tr><td><a class='badge sm' href='#h{H['id']}-{x['line']}'>{E(x['line'])}</a></td><td>{E(x['name'])}</td><td>{E(x['operator'])}</td>"
                f"<td class='n'>{len(sims) or '&mdash;'}</td><td class='n'>{sum(s['need'] for s in sims) or '&mdash;'}</td><td>{where}</td></tr>")
    offr = ''.join(f"<tr><td><b>{E(o['line'])}</b></td><td>{E(nm0(CLS[o['line']]['name'].split(' - ')[0]) + ' – ' + nm0(CLS[o['line']]['name'].split(' - ')[-1]) if ' - ' in CLS[o['line']]['name'] else CLS[o['line']]['name'])}</td><td>DPO</td>"
                   f"<td class='n'>&mdash;</td><td class='n'>&mdash;</td><td>{E(CLSN.get(o['cls'], o['cls'] or ''))}: see <a href='#offpeak'>Not in the afternoon peak</a></td></tr>" for o in H['dpo_off'] if o['line'] in CLS)
    oth = '; '.join(f"{m} {', '.join(v)}" for m, v in H['other'].items() if v)
    nott = [m for m, v in H['other'].items() if not v]
    unrows = ''.join(f"<tr><td><span class='badge sm' style='background:var(--muted)'>{E(x['line'])}</span></td><td>{E(x['name'])}</td><td>{E(x['operator'])}</td><td>{E(x.get('reason', 'on no regional sheet'))}"
                     + (f" (<a href=\"{E(x['home']['url'])}\">{E(short_sheet(x['home']))} sheet</a>)" if x.get('home') else '') + '</td></tr>' for x in rest)
    hubs_html += (f'''<h2 id="{H['id']}">All lines at {E(H['name'])} ({len(dpo) + len(H['dpo_off']) + len(H['odis'])})</h2>
<p class="sub">Every bus line with a stop at {E(H['stop'])}: the {len(dpo)} DPO lines of the afternoon (their cards are in Lines above), {len(H['dpo_off'])} DPO line{'s' if len(H['dpo_off']) != 1 else ''} outside it, and {len(H['odis'])} ODIS lines of other operators, found by scanning the national JDF ({E(H['snapshot'])}). Unlike the Hranečník lines, which are modelled on this sheet, every ODIS line here was already on a regional sheet, with its buses: {E('; '.join(f'{k}: {", ".join(v)}' for k, v in bysheet.items()))}. Lines shared between sheets are listed and linked, not repeated. So the cards below show each line as its home sheet sets it (typed values, real minutes, buses), read from that sheet&#x27;s data; its buses are counted there, not in this sheet&#x27;s totals, depots or line bar, and no bus is on two sheets. Those sheets model {E(mods[0]['home']['day'] if mods else '')} with the ODIS live map, not DPO&#x27;s 30 Sep. The column “At {E(H['name'])}” gives the minutes each leg leaves, passes or reaches the stop: the slot plus the median running time of the leg&#x27;s own trips, against the real times in the model hours.{(' ' + E(oth[0].upper() + oth[1:]) + ' also stop here (their own sheets).') if oth else ''}{(' No ' + ' or '.join(m.rstrip('s') for m in nott) + ' stops here.') if nott else ''}</p>
<div class="types"><table class="tlist"><thead><tr><th>Line</th><th>Route</th><th>Operator</th><th class="n">Simutrans lines</th><th class="n">Needed</th><th>Card</th></tr></thead><tbody>{''.join(hubrow(L, False) for L in dpo)}{offr}{''.join(hrow(x) for x in H['odis'])}</tbody></table></div>
<div class="grid" style="margin-top:18px">{''.join(mirror_card(H, x) for x in mods)}</div>'''
                  + (f'<h3 style="margin-top:22px">Not modelled</h3><div class="types"><table class="tlist"><thead><tr><th>Line</th><th>Route</th><th>Operator</th><th>Why (home sheet)</th></tr></thead><tbody>{unrows}</tbody></table></div>' if rest else ''))
HUBNAV = ''.join(f'<a href="#{H["id"]}">{E(H["nav"])}</a>' for H in HB)

# not in the afternoon peak
offpeak = ''.join(f"<tr><td><b>{L}</b></td><td>{E(nm0(v['name'].split(' - ')[0]) + ' – ' + nm0(v['name'].split(' - ')[-1]) if ' - ' in v['name'] else v['name'])}</td>"
                  f"<td>{E(CLSN[v['cls']])}{(', ' + str(v['trips']) + ' trips, ' + v['first'] + '–' + v['last']) if v.get('first') else ''}</td></tr>"
                  for L, v in sorted(CLS.items(), key=lambda x: int(x[0])) if v['cls'] != 'peak')

# depots
active = {n: c for n, c in fleet.items() if c['state'] == 'zar' and c['cat'] != '?'}
used = {n for L in roster for u in roster[L] for n in u[1]}
dsec = ''
for code, dname in DEPS:
    if PENDING:
        g = collections.defaultdict(list)
        for n, c in sorted(active.items()):
            if c['depot_code'] == code: g[c['full']].append(n)
        body = ''.join(f"<tr><td class='vc'><div class='vt'><b>{E(t)}</b> · {E(length(ns[0]))}</div><div class='pak{'' if pak(ns[0])['exact'] else ' subst'}'>{E(pak(ns[0])['core'])}</div></td>"
                       f"<td><div class='fl'>{''.join(vnum([n]) for n in ns)}</div></td></tr>" for t, ns in sorted(g.items(), key=lambda x: -len(x[1])))
        tot = sum(len(v) for v in g.values())
        dsec += f"""<section class="depot" id="d{code}"><header><h3>{E(dname)}</h3><div class="cnt"><b>{tot}</b><span>active buses</span></div></header>
<div class="tw0"><table class="dt"><thead><tr><th>Type · length / pak core</th><th>Buses</th></tr></thead><tbody>{body}</tbody></table></div></section>"""
    else:
        rows = ''; tot = 0
        for L in order:
            for bi, b in enumerate(BR[L]):
                us = [u for u in roster[L] if u[3] == bi and depcode(u[1][0]) == code]
                if not us: continue
                tot += len(us)
                rows += f"<tr class='brh'><td colspan='2'><a class='badge sm' href='#l{L}'>{L}</a> {E(brname(b))}{' (Simutrans line ' + slname(L, bi) + ')' if len(BR[L]) > 1 else ''} · {len(us)}</td></tr>"
                for u in sorted(us, key=tkey):
                    n = u[1][0]; st = []
                    if u[2] == 'designed': st.append('designed, not recorded: ' + WHY.get((L, n), ''))
                    elif u[2] == 'owner': st.append("owner's choice of type: " + C['owner_types'][L]['why'])
                    elif n in OBS: st.append(f"live {LDAY} {OBS[n]['first']}: course {OBS[n]['course']}" + ('; not yet confirmed at the peak' if PROV else ''))
                    ll = later_lines(n, L)
                    if ll and u[2] not in ('designed', 'owner'): st.append('later on line ' + ', '.join(ll))
                    rows += f"<tr><td class='vc'>{cell(u[1])}</td><td class='stc'>{E('; '.join(st) or '—')}</td></tr>"
        dsec += f"""<section class="depot" id="d{code}"><header><h3>{E(dname)}</h3><div class="cnt"><b>{tot}</b><span>buses out at {PEAK}</span></div></header>
<div class="tw0"><table class="dt"><thead><tr><th>Vehicle</th><th>Live feed {E(C['live']['label'])}</th></tr></thead><tbody>{rows}</tbody></table></div></section>"""
depcount = {code: (sum(1 for n, c in active.items() if c['depot_code'] == code) if PENDING else
                   sum(1 for L in roster for u in roster[L] if depcode(u[1][0]) == code)) for code, _ in DEPS}
DEPNAV = ''.join(f"<a href='#d{code}'>{E(dname)} <b>{depcount[code]}</b></a>" for code, dname in DEPS)

# spares (observed state only)
spsec = ''; sparehead = ''
if not PENDING:
    sparehead = f'<h2>Not in service at {PEAK}</h2><p class="sub">The rest of the active fleet, per garage, with any line the live feed showed it on that afternoon.</p>'
    for code, dname in DEPS:
        items = []
        for n, c in sorted(active.items()):
            if c['depot_code'] != code or n in used: continue
            ll = []
            for x in LIVE.get(n, []):
                if x[1] not in ll: ll.append(x[1])
            items.append(f"{n} {c['full']}" + (f" (live on line {', '.join(ll)})" if ll else ''))
        spsec += f"<div class='sp'><h4>{E(dname)}</h4><p><b>reserve</b> ({len(items)}) <span>{' · '.join(E(x) for x in items)}</span></p></div>"

# pak table
scope = (lambda: [n for n in active]) if PENDING else (lambda: [n for L in roster for u in roster[L] for n in u[1]])
agg = collections.Counter(); info = {}; pnt = collections.defaultdict(collections.Counter)
for n in scope():
    p = pak(n); key = (fleet[n]['full'], p.get('head')); agg[key] += 1; info[key] = p
    pnt[key]['advertising wrap' if p['paint'].startswith('advertising') else p['paint']] += 1
OWN = {liv: {name for key, name, l in PK['paint_rules'] if l == liv} for _, _, liv in PK['paint_rules'] if liv}
paks = ''
for key, c in sorted(agg.items()):
    p = info[key]; objliv = LIVN.get(p.get('liv'), '')
    notes = [p['typereason']] if p.get('typereason') else []
    other = [k for k in pnt[key] if k not in OWN.get(p.get('liv'), set())]
    if other: notes.append('real paint ' + ', '.join(other) + ' is shown in ' + objliv.split(' (')[0])
    near = f"<div class='pak subst'>nearest: {E('; '.join(notes))}</div>" if notes else ''
    paks += (f"<tr><td>{E(key[0])}</td><td><b class='core'>{E(p['core'])}</b><div class='pak'>{E(p.get('chain') or 'no object')}</div>{near}</td>"
             f"<td>{E(objliv)}<div class='lv'>real: {E(', '.join(f'{v}× {k}' for k, v in pnt[key].most_common()))}</div></td>"
             f"<td class='n'>{PK['lengths'].get(p.get('fam'), '')}</td><td class='n'>{c}</td></tr>")

# types table, capacity from every stored live snapshot
cap = collections.defaultdict(set)
for f in glob.glob(os.path.join(ROOT, 'data', 'raw', '*', 'live', '*.json')):
    for v in json.load(open(f, encoding='utf-8')):
        if v['n'] in fleet and v.get('seat') is not None: cap[fleet[v['n']]['cat']].add((v['seat'], v['stand']))
def rng(xs): xs = sorted(set(xs)); return str(xs[0]) if len(xs) == 1 else f'{xs[0]}–{xs[-1]}'
def captxt(t): s = cap.get(t); return f"{rng(a for a, b in s)} + {rng(b for a, b in s)}" if s else '—'
dc = collections.Counter((c['cat'], c['depot_code']) for c in active.values())
trows = ''.join(f"<tr><td><b>{E(v[0])}</b></td><td class='n'>{v[1]}</td><td>{E(v[2])}</td><td class='n'>{captxt(k)}</td><td class='n'>{dc[(k, 'AH')]}</td><td class='n'>{dc[(k, 'AP')]}</td><td class='n'>{'—' if PENDING else pertype.get(k, 0)}</td></tr>" for k, v in C['types'].items())
state = '\n'.join(f'  <div class="st"><h4><span class="tag {io}">{"modelled" if io == "in" else "not modelled"}</span>{E(h)}</h4><p>{E(p)}</p></div>' for io, h, p in C['network_state'])
need = sum(b['need'] for L in order for b in BR[L])
PROVTXT = (f"<b>Provisional roster.</b> {E(C['live']['provisional']['why'])} {len(OBS)} buses were on their lines at {W[0]}–{W[1]} on {E(LDAY)}. "
           f"The rest of each line's need is designed from the line's record history (Mar–Jun 2026) with real car numbers, marked “designed, not recorded”. "
           f"Everything is replaced by the buses observed at the peak of {E(C['vehicle_day_label_en'])}.")
PENDTXT = (f"<b>Vehicles pending.</b> The timetable, branches, needs and Simutrans schedules are complete. The buses on each line are filled in from DPO's live feed "
           f"during the afternoon peak of {E(C['vehicle_day_label_en'])}. Until then, each line shows how many buses it needs, and the garages list their active fleet by type.")
pending = f'<div class="pending">{PENDTXT}</div>' if PENDING else (f'<div class="pending">{PROVTXT}</div>' if PROV else '')
added = R['added']
if PENDING: rostertxt = 'Not yet observed: the page will be regenerated after the peak.'
elif PROV:
    rostertxt = (f"Until then the roster is provisional: {len(OBS)} buses seen on their lines at {W[0]}–{W[1]} on {LDAY}, the evening before, "
                 f"plus {len(added)} designed buses with real car numbers. They are chosen by their weekday records on the line (Mar–Jun 2026, when tram-bus.cz "
                 f"stopped logging), the line's home garage and main type, and none was seen anywhere in the live feed that day. The need is {need}.")
else:
    rostertxt = (f"That is {len(OBS)} buses, against a timetable need of {need}. " + (f"{len(added)} buses are designed where a Simutrans line had fewer buses than it needs, "
                 "each with the reason on its row." if added else 'Every Simutrans line had at least its need in observed buses, so nothing is designed.'))

tpl = open(os.path.join(ROOT, 'templates', 'page.html'), encoding='utf-8').read()
def bneed(L, p):
    b = next((b for b in BR[L] if {b['a'], b['b']} == {AL.get(p['fr'], p['fr']), AL.get(p['to'], p['to'])}), None)
    return (b['need'], b.get('alt_need')) if b else (None, None)
chk_rows = ''.join(
    f"<tr><td><a class='badge sm' href='#l{L}'>{E(L)}</a></td><td>{E(p['fr'])} &rarr; {E(p['to'])}</td><td class='n'>every {p['every']} · Offset {p['set'][0]} · up to {p['approx']} min off{(' · ' + str(bneed(L, p)[0]) + ' buses') if bneed(L, p)[0] else ''}</td>"
    f"<td class='mono'>{', '.join(hm(x) for x in band) or '—'}</td><td class='n'>{slots} / {len(band)}</td>"
    f"<td>{(f'every {al[chr(101)+chr(118)+chr(101)+chr(114)+chr(121)]} · Offset {al[chr(115)+chr(101)+chr(116)][0]} · up to {al[chr(97)+chr(112)+chr(112)+chr(114)+chr(111)+chr(120)]} min off') + ((' · ' + str(bneed(L, p)[1]) + ' buses') if bneed(L, p)[1] else '') if al and al['every'] > p['every'] else '—'}</td></tr>"
    for L, p, slots, band, al in CHECKS)
cchk_rows = ''.join(f"<tr><td><a class='badge sm' href='#l{L}'>{E(L)}</a></td><td>{E(p['fr'])} &rarr; {E(p['to'])}{(' (' + E(p['note']) + ')') if p.get('note') else ''}</td>"
                    f"<td class='n'>every {p['every']} · Offset {p['set'][0]} · stop {p['circuit_leg']} of a circuit</td><td class='n'>{p['_miss'][0]} of {p['_miss'][1]} slots on a real departure</td><td>{'none: a merged row serves one path only' if p.get('paths') else f'separate branch lines: {p[chr(115)+chr(101)+chr(112)]} buses'}</td></tr>" for L, p in CCHECKS)
cchecks = (f'''<h3 style="margin-top:18px">Circuit legs off the timetable ({len(CCHECKS)})</h3>
<p class="sub">Circuits across branches (or across two paths) run on the line&#x27;s fitted slots. These legs have slots more than 3 min from any real departure in the line&#x27;s window, because the real timetable is irregular there. The alternative is the separate branch lines, at the bus count shown.</p>
<div class="types"><table class="tlist"><thead><tr><th>Line</th><th>Leg</th><th class="n">Set now</th><th class="n">On the timetable</th><th>Alternative</th></tr></thead><tbody>{cchk_rows}</tbody></table></div>''') if CCHECKS else ''
checks = (f'''<h2 id="checks">Approximate schedules to check ({len(CHECKS)})</h2>
<p class="sub">These rows have an irregular real timetable, so they get an even approximate pattern with the same rate at both ends of the line. Each one has more slots in {hm(FW[0])}–{hm(FW[1])} than real departures, so the extra slots would run empty or spread the buses thinner. Where a slower pattern exists, it is shown with its own worst deviation. If you pick it, switch both ends of that Simutrans line together. The rows are also marked on their line cards.</p>
<div class="types"><table class="tlist"><thead><tr><th>Line</th><th>Terminus entry</th><th class="n">Set now</th><th>Real departures {hm(FW[0])}–{hm(FW[1])}</th><th class="n">Slots / real</th><th>Slower option</th></tr></thead><tbody>{chk_rows}</tbody></table></div>''' + cchecks) if CHECKS else cchecks
# stop coverage (owner rule, 20 Oct 2026, via the Havířov/Karviná/Orlová sheet: "501 is the only line running to Dětmarovice,
# how can we not model that?"): every stop the sheet's lines serve 13:00-19:00 is on a modelled Simutrans line, or listed here
COV = set(); SRV = collections.defaultdict(lambda: collections.defaultdict(list))
for L in order + ODO:
    trs = TRIPS.get(L, []); T0L = T0_(L)
    for t in trs:
        if 780 <= t['dep'] < 1140:
            for s_ in t['stops']: SRV[nm0(s_)][L].append(t)
    for b in BR[L]:
        if b.get('override'):
            COV.update(nm0(s_) for t in trs if 780 <= t['dep'] < 1140 for s_ in t['stops']); continue
        for g in b.get('legs', []):
            for k in ('out_stops', 'back_stops'): COV.update(nm0(s_) for s_ in g.get(k) or [])
        ends = {b['a']} | set(b['b'].split(' / '))
        for d_ in [(x, y) for x in ends for y in ends if x != y]:
            ts = ([t for t in trs if (al(nm0(t['fr'])), al(nm0(t['to']))) == d_ and T0L - 60 <= t['dep'] < T0L + 120]
                  or [t for t in trs if (al(nm0(t['fr'])), al(nm0(t['to']))) == d_ and 780 <= t['dep'] < 1140])
            if ts: COV.update(collections.Counter(tuple(nm0(s_) for s_ in t['stops']) for t in ts).most_common(1)[0][0])
UNC = {s_: v for s_, v in SRV.items() if s_ not in COV}
def uncrow(s_, v):
    ts = sorted({(t['dep'], nm0(t['fr']), nm0(t['to'])) for L in v for t in v[L]})
    badges = ', '.join(f"<a class='badge sm' href='#l{L}'>{E(L)}</a>" for L in v)
    trips_ = '; '.join(f'{hm(d)} {E(a)} → {E(b)}' for d, a, b in ts)
    dep_ = all(a in C['depot_stops'] or b in C['depot_stops'] for _, a, b in ts)   # DPO's depots (Kunčice, Nová huť garáže is a public stop)
    why = ("a depot run (to or from the garage); depot runs are never modelled" if dep_ else
           f"{len(ts)} trip{'s' if len(ts) > 1 else ''} in 13:00–19:00, outside the line&#x27;s afternoon peak pattern; local lines are modelled at their afternoon peak")
    return f"<tr><td>{E(s_)}</td><td>{badges}</td><td>{trips_}</td><td>{why}</td></tr>"
cov_head = (f'<h2 id="coverage">Stop coverage</h2>\n<p class="sub">{len(SRV)} stops are served by the sheet&#x27;s lines between 13:00 and 19:00. '
            f'{len(SRV) - len(UNC)} of them are on a modelled Simutrans line, including every path of the lines that alternate between two '
            '(28, 32, 49 and ODIS 531) and the Havířov Město loop of ODIS 441. ')
if UNC:
    coverage = (cov_head + f'The {len(UNC)} below are only on single trips.</p>\n<div class="types"><table class="tlist"><thead><tr><th>Stop</th>'
                '<th>Line</th><th>Trips 13:00–19:00</th><th>Why not modelled</th></tr></thead><tbody>'
                + ''.join(uncrow(s_, v) for s_, v in sorted(UNC.items())) + '</tbody></table></div>')
else:
    coverage = cov_head + 'Every one of them is on a modelled line.</p>'
rep = dict(HUB=hub + hubs_html, HUBNAV=HUBNAV, CHECKS=checks + coverage, TITLE=C['title'], VEHICLE_DAY_LABEL=C['vehicle_day_label'], VEHICLE_DAY_EN=C['vehicle_day_label_en'], PEAK=PEAK,
           STATE_LABEL=C['network_state_label'], STATE=state, BRANCHES_WHY=E(C['branches_why']), CARDS='\n'.join(cards),
           DEPOTS=dsec, DEPNAV=DEPNAV, SPARE=spsec, SPAREHEAD=sparehead, PAKS=paks, TYPES=trows, NEED=str(need),
           NOBS='pending' if PENDING else str(len(OBS)), NOBSLAB=('seen ' + PL + '–' + W[1]) if PROV else 'observed live at the peak', NLINES=str(len(order)), NSIM=str(sum(len(BR[L]) for L in order)),
           NAV=''.join(f"<a href='#l{L}' class='badge sm'>{L}</a>" for L in order), PAK_FILE_NOTE=PK['file'].split('(')[1].rstrip(')'),
           WIN=f"{W[0]} and {W[1]}", JDF_LABEL=C['jdf']['export_label'], NALL=str(len(CLS)), OFFPEAK=offpeak, PENDING=pending,
           DEPOT_SUB=E('Each garage lists its active fleet, grouped by type.' if PENDING else 'Each garage lists the buses it sends to each line, with what the live feed showed, or why a bus is designed.'),
           PAKSCOPE='in the active fleet' if PENDING else f'at the {PEAK} peak', PAKCOL='Active buses' if PENDING else f'Buses at {PEAK}',
           ROSTERTXT=E(rostertxt))
for k, v in rep.items(): tpl = tpl.replace('{{' + k + '}}', v)
left = re.findall(r'\{\{[A-Z_0-9]+\}\}', tpl)
assert not left, left
out = os.path.join(PROJECT, C['output_html'])
open(out, 'w', encoding='utf-8').write(tpl)
print('wrote', out, 'need', need, 'observed', len(OBS), 'pending' if PENDING else '')
