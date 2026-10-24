"""derived/*.json + config + templates/page.html -> the published HTML in the project root."""
import collections, html, os, re
from lib import CONFIG, ROOT, PROJECT, load, make_nm, hm, hhmm
import sticky

C = CONFIG; E = html.escape; nm = make_nm(C); PK = C['pak']
fleet = {int(k): v for k, v in load('fleet.json').items()}
lines = load('lines.json'); R = load('roster.json'); SCH = load('schedule.json')
recs = load('records.json')['records']
LIVE = {int(k): v for k, v in load('live.json')['cars'].items()}
roster = R['roster']; BR = R['branches']; order = sorted(roster, key=int)
MEMB = R.get('members', {}); CIRC = C.get('circuits', {})
FIXED = {tuple(x['cars']): f"replaces {' + '.join(map(str, x['out']))} ({C['type_full_names'].get(x['out_type'], x['out_type'])}): that type runs on line {x['line']} only on late-evening courses, not at {C['peak_label']}" for x in R.get('rebase', []) if x['cars']}
TRIPS = load('trips.json'); FW = C['fit']['window']
def mem(L): return MEMB.get(L, [L])
def ltitle(L): return CIRC[L]['title'] if L in MEMB else L
def onlive(n, L): return any(m in LIVE.get(n, {}) for m in mem(L))
TORD = list(C['types']); PEAK = C['peak_label']
DEPS = list(C['fleet']['depots']); DEPSHORT = {DEPS[0]: 'VP', DEPS[1]: 'VMO'}   # CSS class only, never shown

def tkey(x): return (TORD.index(x[0]) if x[0] in TORD else 99, x[1])
def clen(n):
    return C['types'].get(fleet[n]['cat'], ['', '?'])[1]
def fullname(n):
    t = fleet[n]['type']
    if '»' in t: t = t.split('»')[0].strip().rsplit(' ', 1)[0].replace('ČKD ', '') + ' ' + t.split('»')[1].strip()
    return t.replace('ČKD Tatra', 'Tatra')
def paint(n):
    m = re.search(r'nátěr:\s*(.*?)\s*(\*|\{|$)', fleet[n]['note']); p = m.group(1) if m else ''
    if p.startswith('CVR'): return 'advertising wrap ' + p[3:].strip(' ,').split(',')[0], None
    for key, name, liv in PK['paint_rules']:
        if key in p: return name, liv
    return (p or 'unknown paint'), None
LIVN = PK['livery_names']
def pak(n):
    fn = fullname(n); d = PK['objects'].get(fn); pn, want = paint(n)
    if not d: return dict(head=None, paint=pn, reason='the pak has no object for ' + fn, core='no object', exact=False)
    fam, livs, parts, exact = d; reasons = []
    if not exact: reasons.append(f'no {fn} object, nearest is the {fam} object')
    liv = want if want in livs else livs[0]
    if want not in livs:
        reasons.append(f'{pn} is not in the pak' if want is None else f'the pak has this type only in {", ".join(LIVN[l].split(" (")[0] for l in livs)}')
    return dict(head=f"{PK['prefix']}{fam}-{liv}-{parts[0]}", chain=' → '.join(f"{PK['prefix']}{fam}-{liv}-{x}" for x in parts),
                paint=pn, liv=liv, fam=fam, exact=exact, core=('≈ ' if not exact else '') + (fam if parts[0] == 'A' else parts[0]),
                livtag=LIVN[liv].split(' (')[0] if len(livs) > 1 else '', typereason=reasons[0] if not exact else '')
def cell(nums, depot=True):
    """shared 3-line cell: numbers · depot / full types · length / pak core"""
    ps = [pak(n) for n in nums]
    tags = sorted(set(p.get('livtag', '') for p in ps) - {''})
    core = ' + '.join(p['core'] for p in ps) + (f" · {', '.join(tags)}" if tags else '')
    d = fleet[nums[0]]['depot']
    return (f'<div class="num">{" + ".join(f'<span data-v="{n}">{n}</span>' for n in nums)} <span class="dp d-{DEPSHORT[d]}">{E(d)}</span></div>'
            f'<div class="vt">{E(" + ".join(fullname(n) for n in nums))} · {E(" + ".join(clen(n) for n in nums))}</div>'
            f'<div class="pak{"" if all(p["exact"] for p in ps) else " subst"}">{E(core)}</div>')
def hwtext(v):
    """headway as the Simutrans pattern models it (gaps between its slots, e.g. 10/20 on 4A), else the timetable's commonest gap"""
    p = next((p for p in SCH[v['line']] if p['fr'] == v['fr'] and p['to'] == v['to'] and p['every']), None)
    if p:
        r = p['real']; gaps = sorted({((r[(i + 1) % len(r)] - r[i]) % p['every']) or p['every'] for i in range(len(r))})
        return 'every ' + '/'.join(map(str, gaps)) + ' min'
    return f"every {v['hw']} min" if v['hw'] else 'single trip'
def brname(b): return ' → '.join([b['legs'][0][1]] + [x[2] for x in b['legs']]) if b.get('circuit') else f"{b['a']} ⇄ {b['b']}"
def slname(L, bi): return f"{L}{'ABCD'[bi]}" if len(BR[L]) > 1 else L
def status(nums, L):
    out = []
    for n in nums:
        on = [m for m in mem(L) if m in LIVE.get(n, {})]
        if on: out.append(f"{n} on {'this line' if len(mem(L)) == 1 else 'line ' + ' and '.join(on)}, course {', '.join(str(c) for m in on for c in LIVE[n][m])}")
        elif n in LIVE: out.append(f"{n} on line {', '.join(sorted(LIVE[n], key=int))}")
    return '; '.join(out) or '—'

def rtxt(p, v, loop):
    """real departure for a typed value: the minute where the interval divides 60, else the first clock time from 15:30"""
    I = p['every']; r = (v + 60 + (1 if loop else 0)) % I
    if 60 % I == 0: return str(r)
    t = 930 + ((r - 930) % I); return f"{t // 60}:{t % 60:02d}, every {I}"
cards = []; perdepot = collections.Counter(); pertype = collections.Counter()
depot_lines = collections.defaultdict(lambda: collections.defaultdict(list))
for L in order:
    ros = roster[L]; V = [dict(v, line=m) for m in mem(L) for v in lines[m]['variants']]
    for t, nums, flag, bi in ros:
        d = fleet[nums[0]]['depot']; perdepot[d] += 1; pertype[t] += 1; depot_lines[d][L].append((t, nums, flag, bi))
    ltag = lambda m: f"<span class='badge xs'>{m}</span> " if len(mem(L)) > 1 else ''
    rows = ''.join(f"<tr><td>{ltag(v['line'])}{E(v['fr'])}</td><td class='arr'>&rarr;</td><td>{E(v['to'])}</td><td class='n'>{hwtext(v)}</td>"
                   f"<td class='n mono'>{' '.join(f':{m:02d}' for m in v['min_peak_hour']) or '&mdash;'}</td><td class='n'>{v['rt']} min</td></tr>" for v in V)
    sch = ''; placed = set()
    def srow(p, m=L, note=''):
        tag = ltag(m)
        if not p['every']:
            into = f" Its slot is included in the {E(p['fr'])} &rarr; {E(p['into'])} row." if p.get('into') else ''
            return f"<tr class='all'><td>{tag}{E(p['fr'])} &rarr; {E(p['to'])}</td><td colspan='5'>depot run or one-off at {', '.join(hm(x) for x in p['single'])}, not scheduled.{into}</td></tr>"
        deps = [t['dep'] for t in TRIPS[m] if nm(t['fr']) == p['fr'] and nm(t['to']) == p['to']] + p.get('merged', [])
        outside = sorted(x for x in set(deps) if FW[0] <= x < FW[1] and not p['first'] <= x <= p['last'])
        fit = f"exact {hm(p['first'])}–{hm(p['last'])} ({p['n']} dep.)" + (f"<small>outside the run: {', '.join(hm(x) for x in outside)}</small>" if outside else '')
        if p.get('refit'):
            rf = p['refit']; nh = len(p['real']) * 60 // p['every']
            fit += f"<small>matched to the other end, {nh} an hour; this end alone fits best every {rf['every']} ({', '.join(f':{x:02d}' for x in rf['real'])}) {hm(rf['first'])}–{hm(rf['last'])}</small>"
        real_o = f"<small class='real'>real {rtxt(p, p['set'][0], C['all_termini_are_loops'])}</small>"
        real_a = f"<small class='real'>real {', '.join(rtxt(p, v, C['all_termini_are_loops']) for v in p['set'][1:])}</small>" if len(p['set']) > 1 else ''
        sub = f"<span class='lp st'>{E(note)}</span>" if note else ''
        return (f"<tr><td>{tag}{E(p['fr'])} &rarr; {E(p['to'])}{sub}<span class='lp'>loop · 1 min early</span></td>"
                f"<td class='n sv'>{p['every']}</td><td class='n sv'>{p['set'][0]}{real_o}</td><td class='sv'>{', '.join(map(str, p['set'][1:])) or '&mdash;'}{real_a}</td><td class='n'>auto</td><td class='fit'>{fit}</td></tr>")
    if L in MEMB:
        cc = CIRC[L]; placed = set()
        sch += f"<tr class='brh'><td colspan='6'>Simutrans line {E(cc['title'])}, one circuit: the stops in this order</td></tr>"
        for k, (m, a, b) in enumerate(cc['legs']):
            for i, p in enumerate(SCH[m]):
                if p['fr'] == a and p['to'] == b:
                    sch += srow(p, m, f"stop {k + 1} of the circuit" + (f" · {cc['leg_notes'][k]}" if cc['leg_notes'][k] else '')); placed.add((m, i))
        rest = [(m, p) for m in mem(L) for i, p in enumerate(SCH[m]) if (m, i) not in placed]
        if rest: sch += "<tr class='brh'><td colspan='6'>Other trips</td></tr>" + ''.join(srow(p, m) for m, p in rest)
    for bi, b in enumerate(BR[L] if L not in MEMB else []):
        if len(BR[L]) > 1: sch += f"<tr class='brh'><td colspan='6'>Simutrans line {slname(L, bi)}: {E(brname(b))}</td></tr>"
        for i, p in enumerate(SCH[L]):
            if {p['fr'], p['to']} == {b['a'], b['b']}: sch += srow(p); placed.add(i)
    if L not in MEMB:
        rest = [p for i, p in enumerate(SCH[L]) if i not in placed]
        if rest and len(BR[L]) > 1: sch += "<tr class='brh'><td colspan='6'>Other trips</td></tr>"
        sch += ''.join(srow(p) for p in rest)
    stopsd = ''; seen = set()
    for v in V:
        if tuple(v['stops']) in seen or v['n'] < 2: continue
        seen.add(tuple(v['stops']))
        stopsd += f"<p>{ltag(v['line'])}<b>{E(v['fr'])} &rarr; {E(v['to'])}</b> ({len(v['stops'])} stops): {E(' · '.join(v['stops']))}</p>"
    mix = collections.Counter(u[0] for u in ros)
    mixs = ', '.join(f"{c}× {C['type_full_names'][t]}" for t, c in sorted(mix.items(), key=lambda x: -x[1]))
    dtxt = ' + '.join(f'{d} {c}' for d, c in collections.Counter(fleet[u[1][0]]['depot'] for u in ros).most_common())
    def chip(t, nums, flag):
        seen = any(onlive(n, L) for n in nums)
        extra = ('<div class="addn">added to meet the round-trip need</div>' if flag == 'added' else
                 '<div class="addn">covers a roster type of the line (roster coverage rule)</div>' if flag == 'covers' else
                 f'<div class="addn">{E(FIXED.get(tuple(nums), ""))}</div>' if flag == 'fixed' else '')
        return f'<li class="v{" seen" if seen else ""}{" added" if flag == "added" else ""}">{cell(nums)}{extra}</li>'
    chips = ''
    for bi, b in enumerate(BR[L]):
        us = [u for u in ros if u[3] == bi]
        head = f"Simutrans line {slname(L, bi)}: " if len(BR[L]) > 1 else ''
        sub = f"{head}{brname(b)} · {b['assigned']} counted, {b['need']} needed ({f"round {b['cycle']} min on the suggested pattern (every {b['pattern_every']}): {b['runtimes'][0]} + {b['runtimes'][1]} min running, waits {b['waits'][1]} and {b['waits'][0]} min at the termini" if b.get('how') == 'pattern' else f"round trip {b['cycle']} min with 3 min layovers"}; minimum by runtime {b['min_runtime']})"
        if b.get('circuit'):
            hub = CIRC[L]['hub']; hw = [w for (m, a, _), w in zip(b['legs'], b['waits']) if a == hub]
            sub = (f"Simutrans line {b['title']}: {brname(b)} · {b['assigned']} counted, {b['need']} needed for the whole circuit (round {b['cycle']} min at {PEAK}: "
                   f"waits of {' and '.join(map(str, hw))} min at {hub} where the tram changes line, 3 min at the outer loops; minimum by runtime {b['min_runtime']})")
        sub += f" · {b['surplus']} more from the timetable chaining, not needed" if b.get('surplus') else ''
        sur = [u for u in R.get('surplus', {}).get(L, []) if u[3] == bi]
        surli = ''.join(f'<li class="v spare">{cell(u[1])}<div class="vt">' + (f'not needed since 20 Oct 2026: the suggested pattern needs {b["need"]} (it was counted on the sheet before; park it)' if u[2] == 'unneeded' else f'not needed · the chaining at {PEAK} gives more units than this line needs (one of each type kept, then the best picks)') + '</div></li>' for u in sur)
        chips += f'<p class="brsub">{E(sub)}</p><ul class="vs">' + ''.join(chip(t, nums, flag) for t, nums, flag, _ in sorted(us, key=tkey)) + surli + '</ul>'
    sp = R.get('spares', {}).get(L, [])
    if sp:
        chips += (f'<p class="brsub">Not needed: {len(sp)} more car{"s" if len(sp) > 1 else ""} from the line’s history (weekday records Sep 2025 – Jun 2026), active and free that day (not counted)</p><ul class="vs">' +
                  ''.join(f'<li class="v spare">{cell([x["car"]])}<div class="vt">not needed · last on line {" or ".join(mem(L))} {E(x["last"] or "—")} · free that day</div></li>' for x in sp) + '</ul>')
    nadd = sum(1 for u in ros if u[2] == 'added')
    addnote = (f'<p class="lnote">{nadd} car{"s" if nadd > 1 else ""} added: the timetable chaining at {PEAK} gives fewer trams than the round trips need.</p>') if nadd else ''
    note = C['line_notes'].get(L, '')
    cards.append(f"""<article class="card" id="l{L}"><header><span class="badge">{E(ltitle(L))}</span><div class="hd"><h3>{E(' – '.join([CIRC[L]['legs'][0][1]] + [x[2] for x in CIRC[L]['legs'][:len(CIRC[L]['legs']) // 2]]) if L in MEMB else V[0]['fr'] + ' – ' + V[0]['to'])}</h3><p>{E(mixs)} · depot {dtxt}</p></div><div class="cnt"><b>{len(ros)}</b><span>trams at {PEAK}</span></div></header>
<div class="tw"><table class="tt"><thead><tr><th>From</th><th></th><th>To</th><th class="n">Headway</th><th class="n">Leaves {PEAK[:2]}:xx</th><th class="n">Runtime</th></tr></thead><tbody>{rows}</tbody></table></div>
<div class="sched"><h4>Simutrans schedule · loop departures set 1 min early</h4><div class="tw0"><table class="st2"><thead><tr><th>Terminus entry</th><th class="n">Departure every (min)</th><th class="n">Offset (min)</th><th>Also at (min)</th><th class="n">Leave up to</th><th>Fit</th></tr></thead><tbody>{sch}</tbody></table></div></div>
{('<p class="lnote">' + E(note) + '</p>') if note else ''}{addnote}{chips}
<details><summary>Stops</summary>{stopsd}</details></article>""")

dsec = ''
for d in DEPS:
    rows = ''
    for L in sorted(depot_lines[d], key=int):
        for bi, b in enumerate(BR[L]):
            us = [u for u in depot_lines[d][L] if u[3] == bi]
            if not us: continue
            sl = f" (Simutrans line {slname(L, bi)})" if len(BR[L]) > 1 else ' (one circuit)' if L in MEMB else ''
            rows += f"<tr class='brh'><td colspan='2'><a class='badge sm' href='#l{L}'>{E(ltitle(L))}</a> {E(brname(b))}{sl} · {len(us)} from this depot</td></tr>"
            rows += ''.join(f"<tr><td class='vc'>{cell(nums)}</td><td class='stc'>{'added to meet the round-trip need; ' if flag == 'added' else ''}{E(status(nums, L))}</td></tr>" for t, nums, flag, _ in sorted(us, key=tkey))
    tc = collections.Counter(u[0] for L in depot_lines[d] for u in depot_lines[d][L])
    act = sum(1 for n, c in fleet.items() if c['depot'] == d and c['cat'] not in ['?'] + C['types_not_planned'] and (c['state'] == 'zar' or n in LIVE))
    dsec += f"""<section class="depot" id="d-{E(d)}" data-depot="{E(d)}"><header><h3>Vozovna {E(d)}</h3><div class="cnt"><b>{perdepot[d]}</b><span>units out at {PEAK} · {act} active cars</span></div></header>
<p class="mixline">{E(', '.join(f"{c}× {C['type_full_names'][t]}" for t, c in tc.most_common()))}</p><div class="tw0"><table class="dt"><thead><tr><th>Vehicle</th><th>Seen on {E(C['live']['label'])}</th></tr></thead><tbody>{rows}</tbody></table></div></section>"""

agg = collections.Counter(); info = {}; pnt = collections.defaultdict(collections.Counter)
for L in roster:
    for t, nums, *_ in roster[L]:
        for n in nums:
            p = pak(n); key = (fullname(n), p.get('head')); agg[key] += 1; info[key] = p
            pnt[key]['advertising wrap' if p['paint'].startswith('advertising') else p['paint']] += 1
OWN = {liv: {name for key, name, l in PK['paint_rules'] if l == liv} for _, _, liv in PK['paint_rules']}
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

used = {n for L in roster for u in roster[L] for n in u[1]}
spare = collections.defaultdict(lambda: collections.defaultdict(list))
for n, c in sorted(fleet.items()):
    if c['cat'] == '?' or n in used: continue
    if c['cat'] in C['types_not_planned']: st = c['cat'] + ', not planned' if c['state'] == 'zar' else 'in workshops'
    elif c['state'] == 'zar' or n in LIVE: st = 'reserve'
    else: st = {'dilny': 'in workshops', 'doco': 'out of service'}.get(c['state'], c['state'])
    spare[c['depot']][st].append(f'{n} {fullname(n)}')
spsec = ''.join(f"<div class='sp'><h4>{E(d)}</h4>" + ''.join(f"<p><b>{E(k)}</b> ({len(v)}) <span>{' · '.join(E(x) for x in v)}</span></p>" for k, v in spare[d].items()) + '</div>' for d in DEPS)
trows = ''.join(f"<tr><td><b>{E(v[0])}</b></td><td class='n'>{v[1]}</td><td>{E(v[2])}</td><td class='n'>{v[3]}</td><td class='n'>{v[4]}</td><td class='n'>{pertype.get(k, 0)}</td></tr>" for k, v in C['types'].items())
state = '\n'.join(f'  <div class="st"><h4><span class="tag {io}">{"modelled" if io == "in" else "not modelled"}</span>{E(h)}</h4><p>{E(p)}</p></div>' for io, h, p in C['network_state'])

tpl = open(os.path.join(ROOT, 'templates', 'page.html'), encoding='utf-8').read()
rep = dict(BRANCHES_WHY=E(C['branches_why']), POOLS=E(C['shared_pools']), NADDED=str(sum(1 for L in roster for u in roster[L] if u[2] == 'added')), TITLE=C['title'], VEHICLE_DAY_LABEL=C['vehicle_day_label'], VEHICLE_DAY_EN=C['vehicle_day_label_en'], PEAK=PEAK, PEAK_HH=PEAK[:2], STATE_LABEL=C['network_state_label'],
           STATE=state, LIVE_LABEL=C['live']['label'], JDF_LABEL=C['jdf']['export_label'], NREC=f'{round(len(recs), -2):,}',
           PAK_FILE_NOTE=PK['file'].split('(')[1].rstrip(')') if '(' in PK['file'] else PK['file'],
           PAKS=paks, CARDS='\n'.join(cards), DEPOTS=dsec, SPARE=spsec, TYPES=trows, TOT=str(sum(perdepot.values())), NLINES=str(len(order)),
           VP=str(perdepot[DEPS[0]]), VMO=str(perdepot[DEPS[1]]), CONTROLS=sticky.controls(sorted([(f'#l{L}', m) for L in order for m in mem(L)], key=lambda x: int(x[1])), [(d, d, perdepot[d]) for d in DEPS], [('#pak', 'Pak128 objects'), ('#fleet', 'Vehicle types'), ('#method', 'How this was built')], str(roster[order[0]][0][1][0])), LIVE=str(len(LIVE)))
for k, v in rep.items(): tpl = tpl.replace('{{' + k + '}}', v)
tpl = tpl.replace('</style>', '</style>\n' + sticky.CSS, 1)
tpl = tpl.replace('</body>', sticky.SCRIPT + '\n</body>') if '</body>' in tpl else tpl + '\n' + sticky.SCRIPT
left = re.findall(r'\{\{[A-Z_]+\}\}', tpl)
assert not left, left
out = os.path.join(PROJECT, C['output_html'])
open(out, 'w', encoding='utf-8').write(tpl)
print('wrote', out, 'units', sum(perdepot.values()), dict(perdepot))
