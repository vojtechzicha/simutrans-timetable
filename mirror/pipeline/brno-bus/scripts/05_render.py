"""Render the Brno bus sheet for one state into the project root.

  python 05_render.py --state 2026-09-29

Same page as the trolleybus sheet (tram style from pipeline/brno, extra CSS and sticky header from
pipeline/brno-trolleybus/assets/extra.css.html), with bus additions: operators, through stops, one-way peak lines,
split record lines, shortfalls and pak stand-ins.
"""
import argparse, collections, datetime, html, os, re
from common import DER, ASSETS, PROJECT, TRAM, TROLL, state, load, mm

p = argparse.ArgumentParser(); p.add_argument('--state', required=True); a = p.parse_args()
S = state(a.state); X = S['texts']
TT = load(os.path.join(DER, S['name'], 'timetable.json'))
FL = load(os.path.join(DER, S['name'], 'fleet.json'))
PAK = load(os.path.join(ASSETS, 'pak.json'))
E = lambda s: html.escape(str(s), quote=True)
LINES = FL['lines']; NET = TT['network']; SCHED = TT['schedule']; SL = {sl['id']: sl for sl in S['simutrans_lines']}
DCLS = {'Medlánky': 'kom', 'Slatina': 'sla', 'BDS-BUS': 'ext'}
aid = lambda s: 'line-' + s.replace('+', '-')
sl_of = collections.defaultdict(list)
for sl in S['simutrans_lines']:
    for e in sl['entries']:
        if sl['id'] not in sl_of[e[0]]: sl_of[e[0]].append(sl['id'])

def nice(d):
    d = d.replace('-', ''); x = datetime.date(int(d[:4]), int(d[4:6]), int(d[6:]))
    return f"{x.strftime('%a')} {x.day} {x.strftime('%b')} {x.year}"
def pk(u):
    return PAK.get(f"{u['operator']}|{u['type']}") or PAK.get(u['type'])
core = lambda o: re.sub(r'-A$', '', re.search(r'^VZ-[^-]+-[^-]+-[^-]+-(.+)$', o).group(1))   # articulated: first core, no section letter
def pakcore(u):
    x = pk(u)
    if not x: return '<span class="near">≈ missing</span>'
    c = E(core(x['objs'][0]))
    if x.get('requested'): return f'{c} <span class="chip req">requested</span>'
    return f'<span class="near">≈ {c}</span>' if x.get('near') else c
def length(u):
    x = pk(u); return f"{x['m']:g} m" if x else '?'
def cell(u, dep=True):
    num = (f'<span class="dot {DCLS.get(u["depot"], "")}"></span>' if dep else '') + f'<span class="veh" data-v="{E(u["car"])}">{E(u["car"])}</span>' + \
          (f' <span class="vd">· {E(u["depot"])}</span>' if dep else '')
    marks = (' <span class="chip des">designed</span>' if u.get('designed') else '') + \
            (f' <span class="chip ext">{E(u["operator"])}</span>' if u.get('operator', 'DPMB') != 'DPMB' else '')
    ty = E(u['type']) + f' <span class="muted">· {length(u)}</span>' + marks
    return f'<div class="vb"><span class="vn">{num}</span><span class="vt">{ty}</span><span class="vp">{pakcore(u)}</span></div>'
allunits = [u for o in LINES.values() for u in o]
units = [u for u in allunits if not u.get('spare')]          # counted vehicles
NSP = len(allunits) - len(units)
ops = collections.Counter(u['operator'] for u in units)

out = []; w = out.append
style = open(os.path.join(TRAM, 'assets', 'style.css.html'), encoding='utf-8').read()
w(re.sub(r'<title>.*?</title>', f"<title>{E(S['title'])}</title>", style))
w(open(os.path.join(TROLL, 'assets', 'extra.css.html'), encoding='utf-8').read())
nav = [('network', 'Network at 16:00'), ('schedule', 'Simutrans schedule'), ('lines', 'Buses by line'), ('pak', 'Pak128 objects'),
       ('depots', 'Depots'), ('termini', 'Termini at 16:00'), ('excluded', 'Not counted'), ('method', 'Method')]
short = FL['short']
w(f'''<header class="top"><div class="intro"><div class="eyebrow">{E(X['eyebrow'])}</div>
<h1>{E(S['title'])}</h1>
<p class="lede">{E(X['lede'])}</p></div>
<div class="stats"><div class="stat"><b>{len(S['line_order'])}</b><span>bus lines</span></div><div class="stat"><b>{len(SCHED)}</b><span>Simutrans lines</span></div><div class="stat"><b>{len(units)}</b><span>buses out</span></div><div class="stat"><b>{ops.get('DPMB', 0)}</b><span>DPMB</span></div><div class="stat"><b>{len(units) - ops.get('DPMB', 0)}</b><span>other operators</span></div><div class="stat"><b>{NSP}</b><span>not needed</span></div></div></header>
''')
dep_n = collections.Counter(u['depot'] for u in units)
w('<div class="controls"><nav class="nav lines" aria-label="Lines"><span class="lab">Lines</span>'
  + ''.join(f'<a class="badge" href="#{aid(s["id"])}">{E(s["id"])}</a>' for s in SCHED) + '</nav>'
  + '<nav class="nav dnav" aria-label="Depots and sections"><span class="lab">Depots</span>'
  + ''.join(f'<a href="#depot-{DCLS[d]}">{E(d)} <b>{dep_n[d]}</b></a>' for d in S['depots'])
  + ''.join(f'<a href="#{i}">{E(t)}</a>' for i, t in nav) + '</nav>'
  + '<input type="search" id="q" placeholder="Find bus, e.g. 7737" aria-label="Find vehicle number" inputmode="numeric"><span id="hits" aria-live="polite"></span></div>')

# ---- network ------------------------------------------------------------------------------------------
opline = {}
for s in SCHED:
    for u in LINES[s['id']]: opline.setdefault(SL[s['id']]['records'], set()).add(u['operator'])
w('<h2 id="network">Network at 16:00</h2><p class="sub">The Brno city bus lines with afternoon-peak service in the timetable in force from Tue 29 Sep 2026 (IDS JMK GTFS, unchanged since 25 Sep). Night lines (N89–N99), school lines (š85, š86, š88), rail replacement buses and lines without afternoon service (73, 80) are left out. Departures are the trips starting from each point between 16:00 and 16:59. The feed splits long workings at timing points (Úzká, Královo Pole, nádraží, Haškova, Maloměřický most), so those appear as their own rows. Headway is the median gap between 15:00 and 18:00, and runtime the average scheduled time. Depot runs and patterns with fewer than 3 trips in 15:00–18:00 are left out.</p>')
w('<div class="scroll"><table><tr><th>Line</th><th>From</th><th>To</th><th>Every</th><th>Leaves at (16:xx)</th><th>Runtime</th><th>Operator (Friday)</th><th>Simutrans line</th></tr>')
for l in S['line_order']:
    t = [x for x in NET[l] if x['n3h'] >= 3]
    if not t: continue
    op = ', '.join(sorted(opline.get(l, set()))) or '<span class="muted">not recorded</span>'
    for i, x in enumerate(t):
        w('<tr>')
        if i == 0: w(f'<td rowspan="{len(t)}"><span class="badge">{E(l)}</span></td>')
        w(f'<td>{E(x["o"])}</td><td>{E(x["d"])}</td><td class="n">{("%g min" % x["hw"]) if x["hw"] else ""}</td><td class="mins">{" ".join(mm(m) for m in x["m16"]) or "–"}</td><td class="n">{x["run"]} min</td>')
        if i == 0:
            w(f'<td rowspan="{len(t)}" class="note">{op}</td><td rowspan="{len(t)}">' + ' '.join(f'<a href="#{aid(s)}"><span class="badge sm">{E(s)}</span></a>' for s in sl_of[l]) + '</td>')
        w('</tr>')
w('</table></div>')
nm = [x for x in TT['not_modelled'] if x['n'] >= 2]
if nm or S.get('not_peak'):
    w('<p class="sub" style="margin-top:12px"><b>Not modelled.</b> ' + ' '.join(f'{E(k)}: {E(v)}' for k, v in S.get('not_peak', {}).items())
      + (' Minor patterns merged into their line (fewer than 3 trips, or one-way returns): ' + '; '.join(f'{E(x["line"])} {E(x["o"])} → {E(x["d"])} ({x["n"]} trips)' for x in nm) + '.' if nm else '') + '</p>')

def match(r):
    if r['exact']: return f'<span class="chip ok">exact</span> {r["span"]}'
    t = f'<span class="chip warn">partial</span> real 16:xx {" ".join(mm(m) for m in r["hour"])}'
    if r['missing']: t += f'; not modelled: {" ".join(mm(m) for m in r["missing"])} (the other end runs fewer buses an hour; in reality the extra bus comes or goes out of service or as another line)'
    if r['extra']: t += f'; added: {" ".join(mm(m) for m in r["extra"])} (not in the timetable)'
    return t

# ---- schedule -----------------------------------------------------------------------------------------
w('<h2 id="schedule">Simutrans schedule</h2><p class="sub">Values to type into the fork’s Scheduling tab, on the stop entries listed for each Simutrans line. Units are calendar minutes, the offset is minutes after midnight modulo the interval, and Leave up to stays automatic. <b>Where the bus turns (a loop, turning point or terminus), every departure is set 1 min before the timetable departure</b> so it leaves the turning point on time; offset and Also at values are the real minute − 1, with the real minutes underneath. <b>Through stops</b> (timing points the bus passes without turning, such as Úzká on 40 or Haškova on the Lesná loop) keep the real minute. <b>One-way peak lines</b> (E50, E75, 77 from Areál Slatina) have real departures at their origin only; the far end gets Departure every 0 (no timetable), so the bus heads back at once, as it does out of service in reality. Branches are separate lines, and 57 + 66 around Lesná is one circuit line. Each Simutrans line is fitted at one rate so that no end sends more buses than the other.</p>')
w('<div class="scroll"><table class="sched"><tr><th>Line</th><th>Stop entry</th><th>Departure every</th><th>Offset</th><th>Also at</th><th>Stop type</th><th>Leave up to</th><th>Per hour</th><th>Matches real timetable</th><th>Buses</th></tr>')
for s in SCHED:
    n = len(s['rows']); ne = s['need']
    for i, r in enumerate(s['rows']):
        w('<tr>')
        if i == 0:
            nm_ = s['name'].split(' ', 1)[1] if ' ' in s['name'] else s['name']
            w(f'<td rowspan="{n}" class="sl"><a href="#{aid(s["id"])}"><span class="badge">{E(s["id"])}</span></a><small>{E(nm_)}</small>'
              + ('<small><span class="chip pool">pool</span></small>' if s['kind'] == 'pool' else '') + ('<small><span class="chip">one-way</span></small>' if s['kind'] == 'oneway' else '') + '</td>')
        lbl = f'<b>{E(r["stop"])}</b><br><span class="muted">to {E(r["to"])}' + (f' · as {E(r["line"])}' if r['line'] != s['id'] and not r.get('untimed') else '') + '</span>'
        if r.get('untimed'):
            w(f'<td>{lbl}</td><td class="big">0</td><td class="big">–</td><td class="big">–</td><td><span class="chip">no timetable</span></td><td class="muted">–</td><td class="n">–</td><td class="note">Empty back to {E(r["to"])}, about {r["run"]} min (out of service in reality).</td>')
        else:
            real = f'<small class="real">real {r["real"][0]}' + (f'; {",".join(map(str, r["real"][1:]))}' if r['real'][1:] else '') + '</small>' if r['loop'] else ''
            term = '<span class="chip loop">turn −1 min</span>' if r['loop'] else '<span class="chip">through stop</span><br><small class="muted">real minute</small>'
            w(f'<td>{lbl}</td><td class="big">{r["every"]}</td><td class="big">{r["set"][0]}{real}</td><td class="big">{",".join(map(str, r["set"][1:])) or "–"}</td><td>{term}</td><td class="muted">auto</td><td class="n">{r["perh"]:g}</td><td class="note">{match(r)}</td>')
        if i == 0:
            nn = sum(1 for u in LINES[s['id']] if not u.get('spare')); sh = short.get(s['id'])
            w(f'<td rowspan="{n}" class="note"><b>≥ {s["min_run"]}</b> by runtime' + (f'<br><b>{ne["vehicles"]}</b> by timetable cycle ({ne["minutes"]} min)' + (f', incl. +{ne["onroad_extra"]} for the most buses on the road at once' if ne.get('onroad_extra') else '') if ne else '')
              + f'<br><b>{nn}</b> out on Friday' + (f', {nsp_} not needed' if (nsp_ := sum(1 for u in LINES[s['id']] if u.get('spare'))) else '') + (f' <span class="chip warn">{sh} short</span>' if sh else '') + '</td>')
        w('</tr>')
    if s['note']: w(f'<tr><td></td><td colspan="9" class="note">{E(s["note"])}</td></tr>')
w('</table></div>')
w('<p class="sub" style="margin-top:12px">Surplus vehicles are marked <span class="chip spare">not needed</span> (dimmed at the bottom of each card): where more were logged than the line needs, exactly the need stays counted, chosen so that every vehicle type of the line stays represented, and afternoon-only kurzy (then the highest kurz numbers) are dropped first. Not-needed vehicles are left out of every count, the depots and the pak totals (user rule, 29 Sep). Buses by timetable cycle: follow a bus leaving the first entry around 16:00 through every leg of its line, taking the first departure at least 3 min after arriving, or less where the timetable itself turns faster; a round trip that would wait longer than the line’s interval (at least 30 min) is skipped. As on the Prague and Ostrava bus sheets, the need is never below the most buses on the road at once between 16:00 and 16:59 (each trip holding its bus until arrival plus the terminus’s shortest turnaround, at most 3 min); this raises only 75, from 3 to 4. Where more buses were out than the need, the surplus is marked not needed (above).</p>')

# ---- buses by line ------------------------------------------------------------------------------------
w(f'<h2 id="lines">Buses by line</h2><p class="sub">One row per kurz out between about 15:00 and 17:00 on {E(nice(S["vehicles_date"]))}, grouped by Simutrans line. Each bus shows its number (or registration) and depot (<span class="dot kom"></span>Medlánky, <span class="dot sla"></span>Slatina, <span class="dot ext"></span>BDS-BUS), its full type and length, and the pak128 core . Kurz numbers are DPMB’s, written record line / kurz. Where one DPMB line feeds several Simutrans lines, the records don’t say which branch a kurz ran: kurzy are shared out by timetable need, lowest numbers to the main line, and that split is a choice.</p><div class="grid">')
for s in SCHED:
    o = sorted(LINES[s['id']], key=lambda u: (bool(u.get('spare')), u['rec'], u['kurz'])); sl = SL[s['id']]
    oc = [u for u in o if not u.get('spare')]
    mix = collections.Counter(u['type'] for u in oc)
    w(f'<article class="card" id="{aid(s["id"])}"><header><span class="badge">{E(s["id"])}</span><div class="t"><h3>{E(s["name"].split(" ", 1)[1] if " " in s["name"] else s["name"])}</h3><div class="chips">')
    for k, c in mix.most_common(): w(f'<span class="tchip"><b>{c}×</b> {E(k)}</span>')
    w(f'</div></div><div class="count"><b>{len(oc)}</b><span>buses</span></div></header>')
    txt = sl.get('text') or ''
    if s['id'] in FL['split_of'] and not txt:
        sibs = [x for x in S['simutrans_lines'] if x['records'] == sl['records']]
        txt = f"DPMB records line {sl['records']} as one set of kurzy, shared here between Simutrans lines {', '.join(x['id'] for x in sibs)} by timetable need. This split is a choice."
    if txt: w(f'<p class="pooltext"><span class="chip">{"pool" if sl.get("kind") == "pool" else "split, a choice"}</span>' + (' <span class="chip warn">not confirmed</span>' if sl.get('unconfirmed') else '') + f' {E(txt)}</p>')
    ne = s['need']['vehicles'] if s['need'] else None
    nsp = len(o) - len(oc)
    if nsp:
        w(f'<p class="pooltext"><span class="chip spare">not needed</span> {len(o)} logged against {ne} needed by the timetable cycle; {nsp} marked not needed, keeping every type of the line among the counted buses and dropping afternoon-only kurzy first. {E(S.get("slack_text", {}).get(s["id"], ""))}</p>')
    if short.get(s['id']):
        w(f'<p class="pooltext"><span class="chip warn">{short[s["id"]]} short</span> {"No kurz of this line is recorded on the day" if not o else "Fewer kurzy recorded than the timetable cycle needs"}. {E(S.get("short_text", {}).get(s["id"], ""))}</p>')
    w('<div class="scroll flat"><table><tr><th>Kurz</th><th>Bus · depot / type / pak object</th><th>Note</th></tr>')
    for u in o:
        sp = u.get('spare')
        w(f'<tr{" class=\"spare\"" if sp else ""}><td class="n">{E(u["rec"])}/{u["kurz"]}</td><td>{cell(u)}</td><td class="note">' + ('<span class="chip spare">not needed</span> ' if sp else '') + f'{E(u["note"])}</td></tr>')
    w('</table></div></article>')
w('</div>')

# ---- pak ----------------------------------------------------------------------------------------------
w(f'<h2 id="pak">Pak128 objects</h2><p class="sub">Each type in the peak, mapped to the objects of the custom Czech pak128: VZ-DPBrno-bus.pak for DPMB, and VZ-Brno-bus.pak for other operators (BDS-BUS). The lists above show only the pak core; full names follow VZ-&lt;package&gt;-&lt;type&gt;-&lt;livery&gt;-&lt;core&gt;. An articulated bus is two objects built as one vehicle (front -A, then rear -B); the lists show the first core only. Car units per vehicle (16 = one tile). ≈ marks a stand-in, with the reason. {E(PAK["_source"])}</p>')
w('<div class="scroll"><table><tr><th>Operator · type</th><th>Length</th><th>Pak core</th><th>Buses in the peak</th><th>Real liveries (buses)</th><th>Pak128 objects, in order</th><th>Car units</th><th>Status</th></tr>')
keyf = lambda u: (u['operator'], u['type'])
for (op, t), us in sorted(collections.Counter(keyf(u) for u in units).items(), key=lambda kv: (kv[0][0] != 'DPMB', -kv[1])):
    ex = next(u for u in units if keyf(u) == (op, t)); x = pk(ex)
    lv = collections.Counter(u['livery'] or 'not recorded' for u in units if keyf(u) == (op, t))
    lvtxt = '<br>'.join(f'{k}× {E(v)}' for v, k in lv.most_common(3)) + (f'<br>{sum(lv.values()) - sum(k for _, k in lv.most_common(3))}× in other liveries' if len(lv) > 3 else '')
    objs = '<br>'.join(f'<span class="pak">{E(o)}</span>' for o in x['objs']) if x else '<span class="pakmiss">missing</span>'
    stt = ('<span class="chip req">requested</span> ' if x.get('requested') else '<span class="pakmiss">stand-in</span> ' if x.get('near') else '<span class="chip ok">installed</span> ') if x else ''
    w(f'<tr><td><b>{E(t)}</b><br><span class="muted">{E(op)}</span></td><td class="n">{length(ex)}</td><td class="vp big2">{pakcore(ex)}</td><td class="n">{us}</td><td class="note">{lvtxt}</td><td>{objs}</td><td class="n">{x["len"] if x else "–"}</td><td class="note">{stt}{E(x["note"]) if x else ""}</td></tr>')
w('</table></div>')

# ---- depots ---------------------------------------------------------------------------------------------
w('<h2 id="depots">Depots</h2><p class="sub">DPMB buses by the BMHD fleet register, read on ' + E(nice(S['register_date'])) + ': Medlánky and Slatina are the two bus garages. BDS-BUS (Pozořice) runs 48 and 74 for IDS JMK with its own buses (seznam-autobusu.cz).</p><div class="depots">')
for dep in S['depots']:
    rows = collections.defaultdict(list)
    for s in SCHED:
        for u in LINES[s['id']]:
            if u['depot'] == dep and not u.get('spare'): rows[s['id']].append(u)
    nv = sum(len(v) for v in rows.values()); tm = collections.Counter(u['type'] for v in rows.values() for u in v)
    w(f'<article class="card depot" id="depot-{DCLS[dep]}"><header><div class="t"><h3><span class="dot big {DCLS[dep]}"></span>{"Vozovna " if dep != "BDS-BUS" else ""}{E(dep)}</h3><small>{"buses registered here" if dep != "BDS-BUS" else "other operator"}</small></div><div class="count"><b>{nv}</b><span>buses out</span></div></header>')
    w('<div class="mix">' + ''.join(f'<span><b>{k}</b> {E(t)}</span>' for t, k in tm.most_common()) + '</div>')
    for s in SCHED:
        if s['id'] not in rows: continue
        v = sorted(rows[s['id']], key=lambda u: (u['rec'], u['kurz']))
        w(f'<div class="dline"><div class="lhead"><span class="badge">{E(s["id"])}</span><small>{len(v)} bus{"es" if len(v) != 1 else ""}</small></div><div class="scroll flat"><table class="dt"><tr><th>Kurz</th><th>Bus · type · pak object</th></tr>')
        for u in v: w(f'<tr><td class="n">{E(u["rec"])}/{u["kurz"]}</td><td>{cell(u, dep=False)}</td></tr>')
        w('</table></div></div>')
    w('</article>')
w('</div>')

# ---- termini ------------------------------------------------------------------------------------------
w('<h2 id="termini">Termini at 16:00</h2><p class="sub">Every point buses leave from between 16:00 and 16:59, busiest first. Timing points that the feed splits trips at are included.</p>')
dep16 = collections.defaultdict(list)
for l in S['line_order']:
    for x in NET[l]:
        if x['m16'] and x['n3h'] >= 3: dep16[x['o']].append((l, x))
w('<div class="scroll"><table><tr><th>Stop</th><th>Departures 16:00–16:59</th></tr>')
for nm_ in sorted(dep16, key=lambda n: (-sum(len(x['m16']) for l, x in dep16[n]), n)):
    deps = '<br>'.join(f'<span class="badge sm">{E(l)}</span> to {E(x["d"])} <span class="mins">{" ".join(mm(v) for v in x["m16"])}</span>' for l, x in dep16[nm_])
    w(f'<tr><td><b>{E(nm_)}</b></td><td>{deps}</td></tr>')
w('</table></div>')

# ---- not counted ----------------------------------------------------------------------------------------
veh = load(os.path.join(DER, f"vehicles_{S['register_date']}.json"))
w(f'<h2 id="excluded">Not counted</h2><p class="sub">Records from {E(nice(S["vehicles_date"]))} left out of the afternoon count: morning-only duties and buses swapped out.</p><div class="scroll"><table><tr><th>Kurz</th><th>Bus · type · pak object</th><th>Why</th></tr>')
for x in FL['excluded']:
    v = veh.get(x['car'], {})
    u = dict(car=x['car'], type=v.get('type') or v.get('group') or '?', depot=v.get('depot', '?'), operator=v.get('operator', 'DPMB'))
    w(f'<tr><td class="n">{E(x["line"])}/{x["kurz"]}</td><td>{cell(u)}</td><td class="note">{E(x["why"])}</td></tr>')
w('</table></div>')

# ---- method -----------------------------------------------------------------------------------------------
vd = S['vehicles_date']
w(f'''<h2 id="method">Method and sources</h2><div class="notes">
<p><b>Which day.</b> Network from Tue 29 Sep 2026; buses from Fri 25 Sep, the last weekday before it (28 Sep was a holiday), as on the tram and trolleybus sheets. The bus timetable did not change between the two days.</p>
<p><b>Buses.</b> BMHD.cz vypravenost for {E(nice(vd))}, one page per line (<a href="https://www.bmhd.cz/vypravenost/vypravenost.php?datum={vd}&amp;linka=52">line 52</a>). <i>Ráno</i>, <i>ranní kurz</i> and <i>pouze ranní služba</i> mark morning-only duties; <i>odpoledne</i> and <i>odpolední kurz</i> the afternoon bus; <i>ráno i odpoledne</i> a split duty. Buses of other operators are identified on seznam-autobusu.cz.</p>
<p><b>Types and depots.</b> BMHD fleet register (evidence DPMB), exact type, garage and livery as read on {E(nice(S["register_date"]))}.</p>
<p><b>Timetable.</b> IDS JMK GTFS (exported 25 Sep, stored {E(nice(S["gtfs_date"]))}), bus routes (route_type 3), service day {E(nice(S["service_date"]))}. The feed has no vehicle blocks and splits long workings at timing points, so each Simutrans line’s order of legs comes from chaining trips at each stop (pipeline/brno-bus/scripts/propose.py), and its size from the timetable cycle.</p>
<p><b>Simutrans schedule.</b> Fitted to the afternoon peak (core 15:30–16:30) in whole calendar minutes with the fork’s Departure every / Offset / Also at fields, one rate per line (shared rule in pipeline/README.md).</p>
<p><b>Rebuild.</b> Generated by pipeline/brno-bus (state “{E(S["name"])}”), which reuses the trolleybus and tram pipelines’ helpers and page style; see pipeline/brno-bus/README.md.</p>
</div>''')
w('''<script>
(function(){
  var c=document.querySelector('.controls'); function h(){document.documentElement.style.setProperty('--stick',(c.offsetHeight+8)+'px')} h(); addEventListener('resize',h);
  const q=document.getElementById('q'), hits=document.getElementById('hits');
  const all=[...document.querySelectorAll('.veh[data-v]')];
  q.addEventListener('input',()=>{
    const s=q.value.trim().toUpperCase().replace(/\\s+/g,'');
    let first=null, n=0;
    for(const el of all){
      const on = s.length>=3 && el.dataset.v.split('+').some(c=>c.toUpperCase().startsWith(s));
      el.classList.toggle('hit',on);
      if(on){ n++; if(!first) first=el; }
    }
    hits.textContent = s.length>=3 ? (n? n+' found':'not found') : '';
    if(first) first.scrollIntoView({block:'center'});
  });
})();
</script>''')
dest = os.path.join(PROJECT, S['output'])
open(dest, 'w', encoding='utf-8').write(''.join(out))
print('rendered', dest, len(units), 'buses')
