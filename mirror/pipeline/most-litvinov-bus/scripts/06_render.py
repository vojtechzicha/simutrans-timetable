"""derived/*.json + config + assets + templates/page.html -> the HTML in the project root.

Same family as the Ostrava bus and the Most–Litvínov tram sheets: sticky bar (line badges, garage links with
counts, section links, vehicle search on [data-v]), line cards with the variant table, the Simutrans schedule and the
buses as 3-line cells (number · garage / full type · length / pak core), the garages, the reserve, the pak table,
the types, the evidence and the method. Every bus is designed (nothing is logged for DPmML), and every designed bus
says why it is there; "not needed" history buses are dimmed and left out of every count.
"""
import collections, html, json, os, re
from lib import CONFIG, ROOT, PROJECT, load, asset, make_nm, hm

C = CONFIG; E = html.escape; nm = make_nm(C); PM = asset('pak_map.json'); TY = asset('types.json')['types']
fleet = {int(k): v for k, v in load('fleet.json').items()}
lines = load('lines.json'); NE = load('needs.json'); R = load('roster.json'); SCH = load('schedule.json'); CLS = load('line_class.json')
EV = {int(k): v for k, v in load('evidence.json').items()}; REC = load('records.json')
roster = R['roster']; spares = R['spares']; HIST = R['history']
NOTES = C.get('line_notes', {}); TITLES = C.get('line_titles', {})
DEPS = list(C['fleet']['depots'].items())
def lkey(L): return (1, 0) if L == C['nad']['label'] else (0, int(L))
order = sorted(roster, key=lkey)
TORD = ['SOR NB 12', 'SOR NS 12', 'SOR NB 18', 'SOR NS 18', 'Irisbus Citelis 18M', 'Iveco Urbanway 18M', 'MAN ND 313 Lion’s City DD']
PEAK = C['peak_label']

# ---------------------------------------------------------------- pak
def rule(n):
    c = fleet[n]
    for r in PM['rules']:
        if r['type'] == c['type'] and ('paint_contains' not in r or r['paint_contains'] in c['paint']): return r
    return None
def paintname(n):
    p = fleet[n]['paint']
    if p.startswith('CVR'): return 'advertising wrap ' + p[3:].split(',')[0].strip()
    return next((v for k, v in PM['paint_names'].items() if k in p), p or 'unknown paint')
def pak(n):
    r = rule(n)
    if not r: return dict(core='no object', head=None, chain='', exact=False, status='missing', fam=None, liv=None)
    pre = f"{PM['prefix']}{r['family']}-{r['livery']}-"
    return dict(core=r['chain'][0], head=pre + r['chain'][0], chain=' → '.join(pre + x for x in r['chain']), status=r['status'],
                fam=r['family'], liv=r['livery'], units=r['units'], note=r.get('note', ''), exact=r['status'] == 'exists')

# ---------------------------------------------------------------- vehicle cell
def depname(n): return C['fleet']['depots'].get(fleet[n]['depot_code'], fleet[n]['depot'])
def vnum(n): return f'<span class="veh" data-v="{n}">{n}</span>'
def cell(n):
    p = pak(n); req = p['status'] == 'requested'
    return (f'<div class="num">{vnum(n)} <span class="dp d-{fleet[n]["depot_code"]}">{E(depname(n))}</span></div>'
            f'<div class="vt">{E(fleet[n]["full"])} · {E(fleet[n]["length"])}</div>'
            f'<div class="pak{" req" if req else ""}">{E(p["core"])}{" <em>requested</em>" if req else ""}</div>')
def tkey(n): return (TORD.index(fleet[n]['type']) if fleet[n]['type'] in TORD else 99, n)

# ---------------------------------------------------------------- line cards
BR = {L: NE[L]['branches'] for L in NE}
def brname(b): return f"{b['a']} (loop)" if b['loop'] else f"{b['a']} ⇄ {b['b']}"
def slname(L, bi): return f"{L}{'ABCDEF'[bi]}" if len(BR[L]) > 1 else L
def title(L):
    if L in TITLES: return TITLES[L]
    bs = BR[L]; a0 = bs[0]['a']
    if all(b['loop'] for b in bs): return a0 + ' (loop)'
    if all(a0 in (b['a'], b['b']) for b in bs):
        return a0 + ' – ' + ' / '.join((b['b'] if b['a'] == a0 else b['a']) + (' (loop)' if b['loop'] else '') for b in bs)
    return ' / '.join(f"{b['a']} – {b['b']}" for b in bs)
def ev_short(u):
    w = u['why']
    return w.split('; ')[0] if u['kind'] == 'garage' else w
cards = []; pertype = collections.Counter(); perdep = collections.Counter()
for L in order:
    V = lines[L]['variants']; ros = roster[L]
    for u in ros: pertype[fleet[u['car']]['type']] += 1; perdep[fleet[u['car']]['depot_code']] += 1
    rows = ''.join(f"<tr><td>{E(v['fr'])}</td><td class='arr'>&rarr;</td><td>{E(v['to'])}</td><td class='n'>{('every ' + str(v['hw']) + ' min') if v['hw'] else 'single trip'}</td>"
                   f"<td class='n mono'>{' '.join(f':{m:02d}' for m in v['min_peak_hour']) or '&mdash;'}</td><td class='n'>{v['rt']} min</td></tr>" for v in V)
    sch = ''; placed = set()
    def srow(p):
        if not p['every']:
            if p.get('into'):
                return f"<tr class='all'><td>{E(p['fr'])} &rarr; {E(p['to'])}</td><td colspan='4'>variant at {', '.join(hm(x) for x in p['single'])}, not scheduled; its minutes are folded into the {E(p['fr'])} &rarr; {E(p['into'])} row.</td></tr>"
            alld = p.get('all_day') or p['single']
            if not any({p['fr'], p['to']} == {b['a'], b['b']} for b in BR[L]):
                return (f"<tr class='all'><td>{E(p['fr'])} &rarr; {E(p['to'])}</td><td colspan='4'>variant at {', '.join(hm(x) for x in p['single'])}: not a Simutrans line of its own, not scheduled; "
                        f"its bus is counted in the main branch.</td></tr>")
            return (f"<tr class='all'><td>{E(p['fr'])} &rarr; {E(p['to'])}</td><td class='n sv'>0</td><td colspan='3'>no timetable (Departure every 0): too few trips for a pattern. "
                    f"Real departures {', '.join(hm(x) for x in alld)}.</td></tr>")
        # intervals not dividing 60: the real clock times of one cycle from the first exact departure (25 Oct 2026; it had
        # printed the minutes mod the interval, e.g. "11, 41 (mod 45)")
        real = (', '.join(f':{m:02d}' for m in range(60) if m % p['every'] in p['real']) if 60 % p['every'] == 0 else
                ', '.join(hm(m) for m in range(p['first'], p['first'] + p['every']) if m % p['every'] in p['real']) + f', repeating every {p["every"]} min')
        sp = ' · sparse line, fitted over 15:00–20:00' if p.get('sparse') else ''
        return (f"<tr><td>{E(p['fr'])} &rarr; {E(p['to'])}<div class='win'>1 min before timetable {real} · exact {hm(p['first'])}–{hm(p['last'])}{sp}</div></td>"
                f"<td class='n sv'>{p['every']}</td><td class='n sv'>{p['set'][0]}</td><td class='mono'>{', '.join(map(str, p['set'][1:])) or '&mdash;'}</td><td class='n'>auto</td></tr>")
    for bi, b in enumerate(BR[L]):
        if len(BR[L]) > 1: sch += f"<tr class='brh'><td colspan='5'>Simutrans line {slname(L, bi)}: {E(brname(b))}</td></tr>"
        for i, p in enumerate(SCH[L]):
            if i not in placed and {p['fr'], p['to']} == {b['a'], b['b']}: sch += srow(p); placed.add(i)
    rest = [p for i, p in enumerate(SCH[L]) if i not in placed]
    if rest: sch += "<tr class='brh'><td colspan='5'>Other variants</td></tr>" + ''.join(srow(p) for p in rest)
    stopsd = ''; seen = set()
    for v in V:
        if tuple(v['stops']) in seen: continue
        seen.add(tuple(v['stops']))
        stopsd += f"<p><b>{E(v['fr'])} &rarr; {E(v['to'])}</b> ({len(v['stops'])} stops): {E(' · '.join(v['stops']))}</p>"
    chips = ''
    for bi, b in enumerate(BR[L]):
        head = f"Simutrans line {slname(L, bi)}: " if len(BR[L]) > 1 else ''
        if b['how'] == 'round trip': how = f"round trip {b['cycle']} min"
        elif b['how'] == 'loop': how = f"loop {b['cycle']} min"
        else: how = 'the buses the timetable chains at 16:00'
        ext = f"; includes {b['variant_extra']} for the line's other variants (buses on the road 16:00–16:59)" if b.get('variant_extra') else ''
        us = [u for u in ros if u['branch'] == bi]
        sub = f"{head}{brname(b)} · {b['need']} needed ({how}{ext}) · {len(us)} designed"
        def chip(u):
            n = u['car']; cls = {'history': ' added', 'garage': ' added garage', 'coverage': ' added cover'}[u['kind']]
            lab = 'designed, not recorded: ' + ev_short(u)
            return f'<li class="v{cls}">{cell(n)}<div class="addn{" cov" if u["kind"] == "coverage" else ""}">{E(lab)}</div></li>'
        chips += f'<p class="brsub">{E(sub)}</p><ul class="vs">' + ''.join(chip(u) for u in sorted(us, key=lambda u: tkey(u['car']))) + '</ul>'
    sp = spares.get(L, [])
    if sp:
        chips += (f'<p class="brsub">Not needed: {len(sp)} more bus{"es" if len(sp) > 1 else ""} from the line’s history, free that day (not counted)</p><ul class="vs">' +
                  ''.join(f'<li class="v spare">{cell(x["car"])}<div class="vt">not needed · {E(x["how"])}</div></li>' for x in sorted(sp, key=lambda x: tkey(x['car']))) + '</ul>')
    oth = NE[L]['others']
    othtxt = ('<p class="lnote">Not separate Simutrans lines: ' + E('; '.join(f"{' ⇄ '.join(o['pair'])} ({o['trips']} trip{'s' if o['trips'] != 1 else ''} 15:00–18:00)" for o in oth)) + '.</p>') if oth else ''
    note = f'<p class="lnote">{E(NOTES[L])}</p>' if L in NOTES else ''
    mix = ', '.join(f"{c}× {t}" for t, c in collections.Counter(fleet[u['car']]['type'] for u in ros).most_common())
    code = CLS[L]['code']
    sub_h = f"{mix} · {len(BR[L])} Simutrans line{'s' if len(BR[L]) > 1 else ''} · CIS JŘ {code}"
    badge = C['nad'].get('badge', 'Tram replacement') if L == C['nad']['label'] else L
    cards.append(f"""<article class="card" id="l{L}"><header><span class="badge{' nad' if L == C['nad']['label'] else ''}">{badge}</span><div class="hd"><h3>{E(title(L))}</h3><p>{E(sub_h)}</p></div><div class="cnt"><b>{len(ros)}</b><span>buses at {PEAK}</span></div></header>
{note}<div class="tw"><table class="tt"><thead><tr><th>From</th><th></th><th>To</th><th class="n">Headway</th><th class="n">Leaves 16:xx</th><th class="n">Runtime</th></tr></thead><tbody>{rows}</tbody></table></div>
<div class="sched"><h4>Simutrans schedule · departures set 1 min early · offsets count from 01:00 ((real − 61) mod the interval)</h4><div class="tw0"><table class="st2"><thead><tr><th>Terminus entry</th><th class="n">Departure every (min)</th><th class="n">Offset (min)</th><th>Also at (min)</th><th class="n">Leave up to</th></tr></thead><tbody>{sch}</tbody></table></div></div>
{othtxt}{chips}
<details><summary>Stops</summary>{stopsd}</details></article>""")

# ---------------------------------------------------------------- not in the peak
CLSN = {'morning': 'morning only (school trips)', 'prepeak': 'afternoon trips that all end before 16:00 (school or shift trips); nothing on the road in 16:00–16:59',
        'evening': 'evening only', 'none': 'no trips on this day'}
def rname(v): return ' – '.join(nm(x.strip()) for x in v['name'].split(' - ')) if ' - ' in v['name'] else nm(v['name'])
offpeak = ''.join(f"<tr><td><b>{L}</b></td><td>{E(rname(v))}</td><td>{E(CLSN[v['cls']])}{(', ' + str(v['trips']) + ' trip' + ('s' if v['trips'] != 1 else '') + ', ' + v['first'] + '–' + v['last']) if v.get('first') else ''}</td></tr>"
                  for L, v in sorted(CLS.items(), key=lambda x: lkey(x[0])) if v['cls'] != 'peak')

# ---------------------------------------------------------------- garages
used = {u['car'] for L in roster for u in roster[L]}
city = {n: c for n, c in fleet.items() if c['city']}
dsec = ''
for code, dname in DEPS:
    rows = ''; tot = 0
    for L in order:
        for bi, b in enumerate(BR[L]):
            us = [u for u in roster[L] if u['branch'] == bi and fleet[u['car']]['depot_code'] == code]
            if not us: continue
            tot += len(us)
            rows += f"<tr class='brh'><td colspan='2'><a class='badge sm' href='#l{L}'>{C['nad'].get('badge', 'Tram replacement') if L == C['nad']['label'] else L}</a> {E(brname(b))}{' (Simutrans line ' + slname(L, bi) + ')' if len(BR[L]) > 1 else ''} · {len(us)}</td></tr>"
            for u in sorted(us, key=lambda u: tkey(u['car'])):
                rows += f"<tr><td class='vc'>{cell(u['car'])}</td><td class='stc'>{E('designed, not recorded: ' + u['why'])}</td></tr>"
    dsec += f"""<section class="depot" id="d{code}"><header><h3>{E(C['fleet']['depot_names'][code])}</h3><div class="cnt"><b>{tot}</b><span>buses out at {PEAK}</span></div></header>
<div class="tw0"><table class="dt"><thead><tr><th>Vehicle</th><th>Why this bus</th></tr></thead><tbody>{rows}</tbody></table></div></section>"""
DEPNAV = ''.join(f"<a href='#d{code}'>{E(dname)} <b>{perdep[code]}</b></a>" for code, dname in DEPS)

# reserve: the rest of the city fleet per garage, grouped by type (type always visible)
spset = {x['car'] for v in spares.values() for x in v}
spsec = ''
for code, dname in DEPS:
    g = collections.defaultdict(list)
    for n, c in sorted(city.items()):
        if c['depot_code'] == code and n not in used: g[c['full']].append(n)
    body = ''
    for t, ns in sorted(g.items(), key=lambda x: TORD.index(fleet[x[1][0]]['type']) if fleet[x[1][0]]['type'] in TORD else 99):
        items = []
        for n in ns:
            o = R['own'].get(str(n), '')
            tag = (' (not needed on the tram replacement)' if o == C['nad']['label'] else f' (not needed on line {o})') if n in spset else ''
            items.append(f"{vnum(n)}{E(tag)}")
        body += f"<p><b>{E(t)}</b> · {E(fleet[ns[0]]['length'])} ({len(ns)}) <span class='fl'>{' · '.join(items)}</span></p>"
    spsec += f"<div class='sp'><h4>{E(C['fleet']['depot_names'][code])}</h4>{body}</div>"
notcity = ''.join(f"<li>{vnum(n)} {E(c['full'])}: {E(c['why_not'])}</li>" for n, c in sorted(fleet.items()) if not c['city'] and n not in used)

# ---------------------------------------------------------------- pak table
agg = collections.Counter(); info = {}; pnt = collections.defaultdict(collections.Counter); cars = collections.defaultdict(list)
for n in sorted(used):
    p = pak(n); key = (fleet[n]['full'], p['head']); agg[key] += 1; info[key] = p
    pnt[key][paintname(n)] += 1; cars[key].append(n)
paks = ''
for key, c in sorted(agg.items(), key=lambda x: (x[0][0] not in TORD, x[0])):
    p = info[key]; lv = PM['livery_names'].get(p['liv'], '')
    st = "<span class='req'>requested</span> " if p['status'] == 'requested' else ''
    notes = [p['note']] if p.get('note') else []
    other = [k for k in pnt[key] if k.startswith('advertising')]
    if other: notes.append('advertising wraps (' + ', '.join(other) + ') are shown in the normal livery')
    nt = f"<div class='pak'>{E('; '.join(notes))}</div>" if notes else ''
    paks += (f"<tr><td>{E(key[0])}</td><td>{st}<b class='core'>{E(p['core'])}</b><div class='pak'>{E(p['chain'])}</div>{nt}</td>"
             f"<td>{E(lv)}<div class='lv'>real: {E(', '.join(f'{v}× {k}' for k, v in pnt[key].most_common()))}</div></td>"
             f"<td class='n'>{E(p.get('units', ''))}</td><td class='n'>{c}</td></tr>")

# ---------------------------------------------------------------- types table
dc = collections.Counter((c['type'], c['depot_code']) for c in fleet.values() if c['city'] or c.get('weekend_only'))
trows = ''.join(f"<tr><td><b>{E(TY[t]['full'])}</b></td><td class='n'>{E(TY[t]['length'])}</td><td>{E(TY[t]['drive'])}</td><td class='n'>{dc[(t, 'Mos')]}</td><td class='n'>{dc[(t, 'Lit')]}</td><td class='n'>{pertype.get(t, 0)}</td></tr>"
                for t in TORD if t in TY)

# ---------------------------------------------------------------- evidence table: what is observed
evrows = ''
for L in sorted(HIST, key=lkey):
    H = HIST[L]
    items = []
    for n, h in sorted(H.items(), key=lambda x: x[1]['last'], reverse=True):
        n = int(n)
        items.append(f"{vnum(n)} {E(fleet[n]['full'])} <span class='muted'>({E(', '.join(sorted({d for d, _ in h['how']}, reverse=True)))})</span>")
    lab = C['nad'].get('badge', 'Tram replacement') if L == C['nad']['label'] else L
    evrows += f"<tr><td><b>{lab}</b></td><td>{'<br>'.join(items)}</td></tr>"
nrec = len(REC['records']); nrec23 = sum(1 for r in REC['records'] if r['date'] < '2024-01-01')
nph = sum(len(e['photo_lines']) for e in EV.values()); nphl = sum(1 for e in EV.values() for p in e['photo_lines'] if p['line'])

state = '\n'.join(f'  <div class="st"><h4><span class="tag {io}">{"modelled" if io == "in" else "not modelled"}</span>{E(h)}</h4><p>{E(p)}</p></div>' for io, h, p in C['network_state'])
need = sum(b['need'] for L in BR for b in BR[L])
nhist = sum(1 for L in roster for u in roster[L] if u['kind'] == 'history'); ngar = sum(1 for L in roster for u in roster[L] if u['kind'] == 'garage')
ncov = sum(1 for L in roster for u in roster[L] if u['kind'] == 'coverage')
COVTXT = ', '.join(f"{c['car']} ({c['combo'][0]}, {c['combo'][1]}) on {'the tram replacement' if c['line'] == C['nad']['label'] else 'line ' + c['line']} in place of {c['replaces']}" for c in R.get('coverage', []))
# per-line summary near the top (user, 29 Sep): line, Simutrans lines, needed, assigned (logged / designed), not needed
ltab = ''
for L in order:
    need_ = sum(b['need'] for b in BR[L]); asg = len(roster[L])
    assert asg == need_, L
    lab_ = C['nad'].get('badge', 'Tram replacement') if L == C['nad']['label'] else L
    kinds = collections.Counter(u['kind'] for u in roster[L])
    det = ', '.join(f"{v} {k}" for k, v in (('from history', kinds['history']), ('from the garage', kinds['garage']), ('fleet coverage', kinds['coverage'])) if v)
    ltab += (f"<tr><td><a class='badge sm{' nad' if L == C['nad']['label'] else ''}' href='#l{L}'>{E(lab_)}</a></td><td>{E(title(L))}</td>"
             f"<td>{E(lab_ if L == C['nad']['label'] else ', '.join(slname(L, i) for i in range(len(BR[L]))))}</td><td class='n'><b>{need_}</b></td><td class='n'>{asg} (0 logged / {asg} designed)<div class='lv'>{E(det)}</div></td><td class='n'>{len(spares.get(L, []))}</td></tr>")
ltab += (f"<tr class='tot'><td></td><td><b>All lines</b></td><td>{sum(len(BR[L]) for L in order)}</td><td class='n'><b>{sum(b['need'] for L in order for b in BR[L])}</b></td>"
         f"<td class='n'>{len(used)} (0 logged / {len(used)} designed)</td><td class='n'>{sum(len(v) for v in spares.values())}</td></tr>")
nsp = sum(len(v) for v in spares.values())
tpl = open(os.path.join(ROOT, 'templates', 'page.html'), encoding='utf-8').read()
rep = dict(TITLE=C['title'], VEHICLE_DAY_LABEL=C['vehicle_day_label'], VEHICLE_DAY_EN=C['vehicle_day_label_en'], PEAK=PEAK,
           STATE_LABEL=C['network_state_label'], STATE=state, BRANCHES_WHY=E(C['branches_why']), CARDS='\n'.join(cards),
           DEPOTS=dsec, DEPNAV=DEPNAV, SPARE=spsec, NOTCITY=notcity, PAKS=paks, TYPES=trows, NEED=str(need), NDES=str(len(used)),
           NHIST=str(nhist), NGAR=str(ngar), NCOV=str(ncov), COVTXT=E(COVTXT), LINETABLE=ltab, NSP=str(nsp), NLINES=str(len(order)), NSIM=str(sum(len(BR[L]) for L in order)),
           NAV=''.join(f"<a href='#l{L}' class='badge sm{' nad' if L == C['nad']['label'] else ''}'>{C['nad'].get('badge', 'Tram replacement') if L == C['nad']['label'] else L}</a>" for L in order),
           PAK_COMMIT=PM['pak_commit'], BUS_LABEL=E(C['jdf']['bus_label']), TRAM_LABEL=E(C['jdf']['tram_label']), NALL=str(len(CLS)),
           OFFPEAK=offpeak, EVROWS=evrows, NREC=str(nrec), NREC23=str(nrec23), NPH=str(nph), NPHL=str(nphl), NCITY=str(len(city)),
           NREG=str(len(fleet)), NAD_WHY=E(C['nad']['why']), SERVICE_DAY=C['service_day'])
for k, v in rep.items(): tpl = tpl.replace('{{' + k + '}}', v)
left = re.findall(r'\{\{[A-Z_0-9]+\}\}', tpl)
assert not left, left
out = os.path.join(PROJECT, C['output_html'])
open(out, 'w', encoding='utf-8').write(tpl)
print('wrote', out, 'need', need, 'designed', len(used), '(history', nhist, 'garage', ngar, ') not needed', nsp)
