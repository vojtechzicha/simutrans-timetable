"""derived/*.json + config + templates/page.html -> the published HTML in the project root.
Same layout and vehicle cell as the Ostrava tram sheet (pipeline/ostrava/scripts/06_render.py), plus the battery
sections and the course / later-line / Friday-record status of each trolleybus."""
import collections, html, os, re
from lib import CONFIG, ROOT, PROJECT, load, make_nm, hm

C = CONFIG; E = html.escape; nm = make_nm(C); PK = C['pak']
fleet = {int(k): v for k, v in load('fleet.json').items()}
lines = load('lines.json'); R = load('roster.json'); SCH = load('schedule.json'); RECS = load('records.json')
LIVE = {int(k): v for k, v in load('live.json')['cars'].items()}
WHY = {(a['line'], a['car']): a['why'] for a in R['added']}
roster = R['roster']; BR = R['branches']; OBS = {int(k): v for k, v in R['observed'].items()}
order = sorted(roster, key=int); PEAK = C['peak_label']; DEPOT = C['fleet']['depot']
TORD = list(C['types'])
W = C['live']['window']

def tkey(u): return (TORD.index(u[0]) if u[0] in TORD else 99, u[1])
def length(n): return C['types'].get(fleet[n]['cat'], ['', '?'])[1]
def objkey(n):
    f = fleet[n]['full']
    return f + ' battery' if f == 'Škoda 26Tr Solaris' and fleet[n]['battery'] else f
def paint(n):
    m = re.search(r'nátěr:\s*(.*?)\s*(\*|\{|$)', fleet[n]['note']); p = m.group(1) if m else ''
    if p.startswith('CVR'): return 'advertising wrap ' + p[3:].strip(' ,').split(',')[0], None
    for key, name, liv in PK['paint_rules']:
        if key in p: return name, liv
    return (p or 'unknown paint'), None
LIVN = PK['livery_names']
def pak(n):
    fn = objkey(n); d = PK['objects'].get(fn); pn, want = paint(n)
    if not d: return dict(head=None, paint=pn, core='no object', exact=False, typereason='the pak has no object for ' + fn)
    fam, livs, parts, exact, eng = d
    liv = want if want in livs else livs[0]
    return dict(head=f"{PK['prefix']}{fam}-{liv}-{parts[0]}", chain=' → '.join(f"{PK['prefix']}{fam}-{liv}-{x}" for x in parts),
                paint=pn, liv=liv, fam=fam, exact=exact, eng=eng, core=('≈ ' if not exact else '') + parts[0],
                livtag=LIVN[liv].split(' (')[0] if len(livs) > 1 else '',
                typereason='' if exact else f'no {fleet[n]["full"]} object; nearest 12 m two-axle object is {fam}')
def cell(nums):
    """shared 3-line cell: numbers · depot / full type · length (+ battery) / pak core"""
    ps = [pak(n) for n in nums]
    core = ' + '.join(p['core'] for p in ps)
    bat = ' <span class="bat">battery</span>' if all(fleet[n]['battery'] for n in nums) else ''
    return (f'<div class="num"><span class="veh" data-v="{"+".join(map(str, nums))}">{" + ".join(map(str, nums))}</span> <span class="dp d-TR">{E(DEPOT)}</span></div>'
            f'<div class="vt">{E(" + ".join(fleet[n]["full"] for n in nums))} · {E(" + ".join(length(n) for n in nums))}{bat}</div>'
            f'<div class="pak{"" if all(p["exact"] for p in ps) else " subst"}">{E(core)}</div>')
def title(L):
    bs = C['branches'][L]
    return bs[0][0] + ' – ' + ' / '.join(b for a, b in bs) if len({a for a, b in bs}) == 1 else ' / '.join(f'{a} – {b}' for a, b in bs)
def brname(b): return f"{b['a']} ⇄ {b['b']}"
def slname(L, bi): return f"{L}{'AB'[bi]}" if len(BR[L]) > 1 else L
REC25 = collections.defaultdict(list)
for r in RECS.get('2026-09-25', []):
    for n in r['cars']: REC25[n].append(r)
def later_lines(n, L):
    s = [x[1] for x in LIVE.get(n, []) if x[0] > W[1]]
    out = []
    for x in s:
        if x != L and x not in out: out.append(x)
    return out
def status(n, L, flag):
    parts = []
    if flag == 'designed': parts.append('designed, not recorded: not seen live on this line at the peak')
    elif n in OBS:
        o = OBS[n]; parts.append(f"live {o['first']}: course {o['course']}")
        ll = later_lines(n, L)
        if ll: parts.append('later on line ' + ', '.join(ll))
    for r in REC25.get(n, []):
        parts.append(f"Fri 25 Sep: line {r['line']}, course {r['kurz']}" + (f" ({r['note']})" if r['note'] else ''))
    return '; '.join(parts) or '—'

bat_by_line = collections.defaultdict(list)
for L, br, stretch, which, since in C['battery_sections']: bat_by_line[L].append((br, stretch, which, since))

TRIPS = load('trips.json'); FW = (C['peak_minute'] - 30, C['peak_minute'] + 90)
def hwtext(L, v):
    """headway as the Simutrans pattern models it (gaps between its slots), else the timetable's commonest gap"""
    p = next((p for p in SCH[L] if nm(p['fr']) == nm(v['fr']) and nm(p['to']) == nm(v['to']) and p['every']), None)
    if p:
        r = p['real']; gaps = sorted({((r[(i + 1) % len(r)] - r[i]) % p['every']) or p['every'] for i in range(len(r))})
        return ('about ' if 'approx' in p else '') + 'every ' + '/'.join(map(str, gaps)) + ' min'
    return f"every {v['hw']} min" if v['hw'] else 'single trip'
def srow_fit(L, p):
    """one schedule row: typed values with the real minute under them (Prague style) and a Fit cell"""
    deps = sorted(set([t['dep'] for t in TRIPS[L] if nm(t['fr']) == p['fr'] and nm(t['to']) == p['to']] + p.get('merged', [])))
    band = [x for x in deps if FW[0] <= x < FW[1]]
    if 'approx' in p:
        fit = (f"approximate, up to {p['approx']} min off" + (" (irregular: no even pattern fits)" if p['approx'] >= p['every'] // 3 else '') +
               f"<small>real {hm(FW[0])}–{hm(FW[1])}: {', '.join(hm(x) for x in band) or 'none'}</small>")
    else:
        out = [x for x in deps if FW[0] - 30 <= x < FW[1] + 30 and not p['first'] <= x <= p['last']]
        fit = f"exact {hm(p['first'])}–{hm(p['last'])} ({p['n']} dep.)" + (f"<small>outside the run: {', '.join(hm(x) for x in out)}</small>" if out else '')
    if p.get('refit'):
        rf = p['refit']; nh = len(p['real']) * 60 / p['every']
        fit += (f"<small>matched to the other end ({nh:g} an hour); this end alone fitted every {rf['every']} "
                f"({', '.join(f':{x:02d}' for x in rf['real'])}) {hm(rf['first'])}–{hm(rf['last'])}</small>")
    real_o = f"<small class='real'>real {rtxt(p, p['set'][0], C['all_termini_are_loops'])}</small>"
    real_a = f"<small class='real'>real {', '.join(rtxt(p, v, C['all_termini_are_loops']) for v in p['set'][1:])}</small>" if len(p['set']) > 1 else ''
    return (f"<tr><td>{E(p['fr'])} &rarr; {E(p['to'])}<span class='lp'>loop · 1 min early</span></td>"
            f"<td class='n sv'>{p['every']}</td><td class='n sv'>{p['set'][0]}{real_o}</td><td class='sv'>{', '.join(map(str, p['set'][1:])) or '&mdash;'}{real_a}</td><td class='n'>auto</td><td class='fit'>{fit}</td></tr>")

def rtxt(p, v, loop):
    """real departure for a typed value: the minute where the interval divides 60, else the first clock time from 15:30"""
    I = p['every']; r = (v + 60 + (1 if loop else 0)) % I
    if 60 % I == 0: return str(r)
    t = 930 + ((r - 930) % I); return f"{t // 60}:{t % 60:02d}, every {I}"
cards = []; pertype = collections.Counter(); perline = {}
for L in order:
    ros = roster[L]; V = lines[L]['variants']; perline[L] = len(ros)
    for u in ros: pertype[u[0]] += 1
    rows = ''.join(f"<tr><td>{E(v['fr'])}</td><td class='arr'>&rarr;</td><td>{E(v['to'])}</td><td class='n'>{hwtext(L, v)}</td>"
                   f"<td class='n mono'>{' '.join(f':{m:02d}' for m in v['min_peak_hour']) or '&mdash;'}</td><td class='n'>{v['rt']} min</td></tr>" for v in V)
    sch = ''; placed = set()
    def srow(p):
        if not p['every']:
            into = f" Its slot is included in the {E(p['fr'])} &rarr; {E(p['into'])} row." if p.get('into') else ''
            return f"<tr class='all'><td>{E(p['fr'])} &rarr; {E(p['to'])}</td><td colspan='5'>depot run or one-off at {', '.join(hm(x) for x in p['single'])}, not scheduled.{into}</td></tr>"
        return srow_fit(L, p)
    for bi, b in enumerate(BR[L]):
        if len(BR[L]) > 1: sch += f"<tr class='brh'><td colspan='6'>Simutrans line {slname(L, bi)}: {E(brname(b))}</td></tr>"
        for i, p in enumerate(SCH[L]):
            if {p['fr'], p['to']} == {b['a'], b['b']}: sch += srow(p); placed.add(i)
    rest = [p for i, p in enumerate(SCH[L]) if i not in placed]
    if rest and len(BR[L]) > 1: sch += "<tr class='brh'><td colspan='6'>Other trips</td></tr>"
    sch += ''.join(srow(p) for p in rest)
    stopsd = ''; seen = set()
    for v in V:
        if tuple(v['stops']) in seen or v['n'] < 2: continue
        seen.add(tuple(v['stops']))
        stopsd += f"<p><b>{E(v['fr'])} &rarr; {E(v['to'])}</b> ({len(v['stops'])} stops): {E(' · '.join(v['stops']))}</p>"
    mix = collections.Counter(u[0] for u in ros)
    mixs = ', '.join(f"{c}× {C['types'][t][0]}" for t, c in sorted(mix.items(), key=lambda x: -x[1]))
    lens = sorted({C['types'][u[0]][1] for u in ros})
    batt = ''.join(f"<div class='battbox'><b>Battery section</b> ({E(br)}): {E(st)}. {E(wh[0].upper() + wh[1:])}; {E(si)}.</div>" for br, st, wh, si in bat_by_line.get(L, []))
    def chip(u):
        t, nums, flag, bi, course = u
        seen_ = any(OBS.get(n, {}).get('line') == L for n in nums)
        extra = f'<div class="addn">designed, not recorded: {E(WHY.get((L, nums[0]), "").split("; not seen")[0])}</div>' if flag == 'designed' else (f'<div class="vt">course {course}</div>' if course is not None else '')
        return f'<li class="v{" seen" if seen_ else ""}{" added" if flag == "designed" else ""}">{cell(nums)}{extra}</li>'
    chips = ''
    for bi, b in enumerate(BR[L]):
        us = [u for u in ros if u[3] == bi]
        head = f"Simutrans line {slname(L, bi)}: " if len(BR[L]) > 1 else ''
        bt = ' · battery branch' if b['battery'] else ''
        sub = f"{head}{brname(b)} · {b['assigned']} assigned ({b['observed']} seen live), {b['need']} needed (round trip {b['cycle']} min with 3 min layovers; minimum by runtime {b['min_runtime']}){bt}" + (f" · {b['surplus']} more seen, not needed" if b.get('surplus') else '')
        sur = [u for u in R.get('surplus', {}).get(L, []) if u[3] == bi]
        surli = ''.join(f'<li class="v spare">{cell(u[1])}<div class="vt">not needed · course {u[4]} · seen {E(OBS[u[1][0]]["first"])}; more seen than this line needs (one of each type kept, then the lowest courses)</div></li>' for u in sur)
        chips += f'<p class="brsub">{E(sub)}</p><ul class="vs">' + ''.join(chip(u) for u in sorted(us, key=tkey)) + surli + '</ul>'
    sp = R.get('spares', {}).get(L, [])
    if sp:
        chips += (f'<p class="brsub">Not needed: {len(sp)} more trolleybus{"es" if len(sp) > 1 else ""} from the line’s history (weekday records Mar–Jun 2026), free that day (not counted)</p><ul class="vs">' +
                  ''.join(f'<li class="v spare">{cell([x["car"]])}<div class="vt">not needed · last on line {L} {E(x["last"])} · {x["records"]} records · free that day</div></li>' for x in sp) + '</ul>')
    nadd = sum(1 for u in ros if u[2] == 'designed')
    addnote = (f'<p class="lnote">{nadd} trolleybus{"es" if nadd > 1 else ""} designed: fewer were seen live at the peak than the round trips need.</p>') if nadd else ''
    note = C['line_notes'].get(L, '')
    cards.append(f"""<article class="card" id="l{L}"><header><span class="badge">{L}</span><div class="hd"><h3>{E(title(L))}</h3><p>{E(mixs)} · {' / '.join(lens)}</p></div><div class="cnt"><b>{len(ros)}</b><span>trolleybuses at {PEAK}</span></div></header>
<div class="tw"><table class="tt"><thead><tr><th>From</th><th></th><th>To</th><th class="n">Headway</th><th class="n">Leaves 16:xx</th><th class="n">Runtime</th></tr></thead><tbody>{rows}</tbody></table></div>
{batt}<div class="sched"><h4>Simutrans schedule · loop departures set 1 min early</h4><div class="tw0"><table class="st2"><thead><tr><th>Terminus entry</th><th class="n">Departure every (min)</th><th class="n">Offset (min)</th><th>Also at (min)</th><th class="n">Leave up to</th><th>Fit</th></tr></thead><tbody>{sch}</tbody></table></div></div>
{('<p class="lnote">' + E(note) + '</p>') if note else ''}{addnote}{chips}
<details><summary>Stops</summary>{stopsd}</details></article>""")

# depot table
rows = ''
for L in order:
    for bi, b in enumerate(BR[L]):
        us = [u for u in roster[L] if u[3] == bi]
        if not us: continue
        sl = f" (Simutrans line {slname(L, bi)})" if len(BR[L]) > 1 else ''
        rows += f"<tr class='brh'><td colspan='2'><a class='badge sm' href='#l{L}'>{L}</a> {E(brname(b))}{sl} · {len(us)}</td></tr>"
        rows += ''.join(f"<tr><td class='vc'>{cell(u[1])}</td><td class='stc'>{E(status(u[1][0], L, u[2]))}</td></tr>" for u in sorted(us, key=tkey))
tot = sum(perline.values())
active = [n for n, c in fleet.items() if c['state'] == 'zar' and c['cat'] != '?']
tc = collections.Counter(u[0] for L in roster for u in roster[L])
dsec = f"""<section class="depot"><header><h3>{E(DEPOT)} <small>Sokolská třída, Moravská Ostrava</small></h3><div class="cnt"><b>{tot}</b><span>trolleybuses out at {PEAK} · {len(active)} active</span></div></header>
<p class="mixline">{E(', '.join(f"{c}× {C['types'][t][0]}" for t, c in tc.most_common()))}</p><div class="tw0"><table class="dt"><thead><tr><th>Vehicle</th><th>Live feed {E(C['live']['label'])} · record Fri 25 Sep</th></tr></thead><tbody>{rows}</tbody></table></div></section>"""

# pak table
agg = collections.Counter(); info = {}; pnt = collections.defaultdict(collections.Counter)
for L in roster:
    for u in roster[L]:
        for n in u[1]:
            p = pak(n); key = (objkey(n).replace(' battery', ' with traction battery'), p.get('head')); agg[key] += 1; info[key] = p
            pnt[key]['advertising wrap' if p['paint'].startswith('advertising') else p['paint']] += 1
OWN = {liv: {name for key, name, l in PK['paint_rules'] if l == liv} for _, _, liv in PK['paint_rules'] if liv}
paks = ''
for key, c in sorted(agg.items()):
    p = info[key]; objliv = LIVN.get(p.get('liv'), '')
    notes = [p['typereason']] if p.get('typereason') else []
    other = [k for k in pnt[key] if k not in OWN.get(p.get('liv'), set())]
    if other: notes.append('real paint ' + ', '.join(other) + ' is shown in ' + objliv.split(' (')[0])
    near = f"<div class='pak subst'>nearest: {E('; '.join(notes))}</div>" if notes else ''
    eng = f" · engine_type={p['eng']}" if p.get('eng') else ''
    paks += (f"<tr><td>{E(key[0])}</td><td><b class='core'>{E(p['core'])}</b><div class='pak'>{E((p.get('chain') or 'no object') + eng)}</div>{near}</td>"
             f"<td>{E(objliv)}<div class='lv'>real: {E(', '.join(f'{v}× {k}' for k, v in pnt[key].most_common()))}</div></td>"
             f"<td class='n'>{PK['lengths'].get(p.get('fam'), '')}</td><td class='n'>{c}</td></tr>")

# spares
used = {n for L in roster for u in roster[L] for n in u[1]}
spare = collections.defaultdict(list)
for n, c in sorted(fleet.items()):
    if n in used: continue
    if c['state'] == 'zar':
        ll = []
        for x in LIVE.get(n, []):
            if x[1] not in ll: ll.append(x[1])
        st = 'reserve' if not ll else 'reserve at the peak'
        spare[st].append(f"{n} {c['full']}" + (f" (live after {W[1]} on line {', '.join(ll)})" if ll else ''))
    else:
        spare[{'sluz': 'driving school', 'muz': 'museum'}.get(c['state'], c['state'])].append(f"{n} {c['full']}")
spsec = "<div class='sp'>" + ''.join(f"<p><b>{E(k)}</b> ({len(v)}) <span>{' · '.join(E(x) for x in v)}</span></p>" for k, v in spare.items()) + '</div>'
act = collections.Counter(fleet[n]['cat'] for n in active)
trows = ''.join(f"<tr><td><b>{E(v[0])}</b></td><td class='n'>{v[1]}</td><td>{E(v[2])}</td><td class='n'>{v[3]}</td><td class='n'>{act.get(k, 0)}</td><td class='n'>{pertype.get(k, 0)}</td></tr>" for k, v in C['types'].items())
state = '\n'.join(f'  <div class="st"><h4><span class="tag {io}">{"modelled" if io == "in" else "not modelled"}</span>{E(h)}</h4><p>{E(p)}</p></div>' for io, h, p in C['network_state'])
battrows = ''
for L, br, stretch, which, since in C['battery_sections']:
    bi = next((i for i, b in enumerate(BR[L]) if brname(b) == br), None)
    cnt = sum(1 for u in roster[L] if u[3] == bi) if bi is not None else 0
    battrows += f"<tr><td><a class='badge sm' href='#l{L}'>{L}</a></td><td>{E(br)}</td><td>{E(stretch)}</td><td>{E(which)}</td><td>{E(since)}</td><td class='n'>{cnt}</td></tr>"
need = sum(b['need'] for L in BR for b in BR[L])
added = R['added']
addtxt = (f"Where fewer buses were seen than the round trip needs, the gap is filled with a designed trolleybus (dashed border): {len(added)} in all. " +
          'Each is an active car not seen at the peak, battery-capable where the branch needs it, preferring cars recorded on the line. ' +
          '; '.join(f"line {a['line']}: {a['car']} ({a['why']})" for a in added) + '.') if added else 'Every Simutrans line had at least its need in observed buses, so nothing is designed.'
nbat = sum(1 for n in used if fleet[n]['battery'])

tpl = open(os.path.join(ROOT, 'templates', 'page.html'), encoding='utf-8').read()
rep = dict(TITLE=C['title'], VEHICLE_DAY_LABEL=C['vehicle_day_label'], VEHICLE_DAY_EN=C['vehicle_day_label_en'], PEAK=PEAK,
           STATE_LABEL=C['network_state_label'], STATE=state, BATTROWS=battrows, WHO=E(C['who_text']),
           BRANCHES_WHY=E(C['branches_why']), POOLS=E(C['interlining']), CARDS='\n'.join(cards), DEPOTS=dsec, SPARE=spsec,
           PAKS=paks, TYPES=trows, TOT=str(tot), NOBS=str(len(OBS)), NLINES=str(len(order)), NBAT=str(nbat),
           NAV=''.join(f"<a href='#l{L}' class='badge sm'>{L}</a>" for L in order), DEPNAV=f"<a href='#depots'>{E(DEPOT)} <b>{tot}</b></a>", PAK_FILE_NOTE=PK['file'].split('(')[1].rstrip(')'),
           UNUSED=E(', '.join(PK['unused_objects'])), WIN=f"{W[0]} and {W[1]}", NEED=str(need), JDF_LABEL=C['jdf']['export_label'],
           NREC25=str(len(RECS.get('2026-09-25', []))), NREC29=str(len(RECS.get('2026-09-29', []))), ADDTXT=E(addtxt))
for k, v in rep.items(): tpl = tpl.replace('{{' + k + '}}', v)
left = re.findall(r'\{\{[A-Z_0-9]+\}\}', tpl)
assert not left, left
out = os.path.join(PROJECT, C['output_html'])
open(out, 'w', encoding='utf-8').write(tpl)
print('wrote', out, 'trolleybuses', tot, 'observed', len(OBS), 'battery', nbat)
