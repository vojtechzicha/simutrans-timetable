"""Render the HTML sheet for one state into the project root.

  python 05_render.py --state 2026-09-29

Inputs: data/derived/<state>/{timetable,fleet}.json, data/derived/vehicles_<register_date>.json, assets/pak.json,
assets/extra.css.html, and the tram sheet's page style (pipeline/brno/assets/style.css.html), so the two Brno
sheets look alike.
"""
import argparse, collections, datetime, html, os, re
from common import DER, ASSETS, PROJECT, TRAM, state, load, mm

p = argparse.ArgumentParser(); p.add_argument('--state', required=True); a = p.parse_args()
S = state(a.state); X = S['texts']
TT = load(os.path.join(DER, S['name'], 'timetable.json'))
FL = load(os.path.join(DER, S['name'], 'fleet.json'))
PAK = load(os.path.join(ASSETS, 'pak.json'))
E = lambda s: html.escape(str(s), quote=True)
LINES = FL['lines']; NET = TT['network']; SCHED = TT['schedule']; SL = {sl['id']: sl for sl in S['simutrans_lines']}
LEN = S['lengths']; BATT = set(S['battery_types'])
DCLS = {'Komín': 'kom', 'Husovice': 'hus', 'Slatina': 'sla'}
sl_of = collections.defaultdict(list)                     # GTFS line -> Simutrans line ids
for sl in S['simutrans_lines']:
    for e in sl['entries']:
        if sl['id'] not in sl_of[e[0]]: sl_of[e[0]].append(sl['id'])

def nice(d):
    d = d.replace('-', ''); x = datetime.date(int(d[:4]), int(d[4:6]), int(d[6:]))
    return f"{x.strftime('%a')} {x.day} {x.strftime('%b')} {x.year}"
core = lambda o: re.search(r'-dpmb[a-z]+-(.+)$', o).group(1)
def pakcore(t):
    pk = PAK.get(t)
    return E(core(pk['objs'][0])) if pk else '<span class="near">≈ missing</span>'
def cell(u, dep=True):
    t = u['type']; ln = LEN.get(t)
    num = (f'<span class="dot {DCLS.get(u["depot"], "")}"></span>' if dep else '') + f'<span class="veh" data-v="{E(u["car"])}">{E(u["car"])}</span>' + \
          (f' <span class="vd">· {E(u["depot"])}</span>' if dep else '')
    marks = (' <span class="chip bus">bus</span>' if u.get('bus') else '') + \
            ('<span class="batmark">battery</span>' if t in BATT else '')
    ty = E(t) + (f' <span class="muted">· {ln} m</span>' if ln else '') + marks
    return f'<div class="vb"><span class="vn">{num}</span><span class="vt">{ty}</span><span class="vp">{pakcore(t)}</span></div>'
tbs = lambda o: [u for u in o if not u['bus'] and not u.get('spare')]
allunits = [u for o in LINES.values() for u in o]
units = [u for u in allunits if not u.get('spare')]          # counted vehicles
NSP = len(allunits) - len(units)
n_tb = sum(1 for u in units if not u['bus']); n_bus = len(units) - n_tb

out = []; w = out.append
style = open(os.path.join(TRAM, 'assets', 'style.css.html'), encoding='utf-8').read()
w(re.sub(r'<title>.*?</title>', f"<title>{E(S['title'])}</title>", style))
w(open(os.path.join(ASSETS, 'extra.css.html'), encoding='utf-8').read())
nav = [('network', 'Network at 16:00'), ('battery', 'Battery sections'), ('schedule', 'Simutrans schedule'),
       ('lines', 'Trolleybuses by line'), ('pak', 'Pak128 objects'), ('depots', 'Depots'), ('termini', 'Termini at 16:00'),
       ('excluded', 'Not counted'), ('method', 'Method')]
w(f'''<header class="top"><div class="intro"><div class="eyebrow">{E(X['eyebrow'])}</div>
<h1>{E(S['title'])}</h1>
<p class="lede">{E(X['lede'])}</p></div>
<div class="stats"><div class="stat"><b>{len(S['line_order'])}</b><span>DPMB lines</span></div><div class="stat"><b>{len(SCHED)}</b><span>Simutrans lines</span></div><div class="stat"><b>{n_tb}</b><span>trolleybuses out</span></div><div class="stat"><b>{n_bus}</b><span>buses on trolleybus kurzy</span></div><div class="stat"><b>{NSP}</b><span>not needed</span></div><div class="stat"><b>{len(S['depots'])}</b><span>depots</span></div></div></header>
''')
# sticky controls (as on the Prague tram sheet): lines, depots + sections, vehicle search
dep_n = collections.Counter(u['depot'] for u in units if not u['bus'])   # trolleybuses per depot
w('<div class="controls"><nav class="nav lines" aria-label="Lines"><span class="lab">Lines</span>'
  + ''.join(f'<a class="badge" href="#line-{E(s["id"].replace("+", "-"))}">{E(s["id"])}</a>' for s in SCHED) + '</nav>'
  + '<nav class="nav dnav" aria-label="Depots and sections"><span class="lab">Depots</span>'
  + ''.join(f'<a href="#depot-{DCLS[d]}">{E(d)} <b>{dep_n[d]}</b></a>' for d in S['depots'])
  + ''.join(f'<a href="#{i}">{E(t)}</a>' for i, t in nav) + '</nav>'
  + '<input type="search" id="q" placeholder="Find vehicle, e.g. 3618" aria-label="Find vehicle number" inputmode="numeric"><span id="hits" aria-live="polite"></span></div>')

# ---- network ------------------------------------------------------------------------------------------
w('<h2 id="network">Network at 16:00</h2><p class="sub">The trolleybus timetable in force from Tue 29 Sep 2026 (IDS JMK GTFS, the same on 25 Sep and 2 Oct). Departures are the trips starting from each terminus between 16:00 and 16:59. Headway is the median gap between 15:00 and 18:00, and runtime is the average scheduled time from first to last stop. Depot runs and patterns with fewer than 3 trips in 15:00–18:00 are left out. 26 is worked by 25 kurzy, and 35 and 38 by 39 kurzy, so those lines show their vehicles under the Simutrans pool.</p>')
w('<div class="scroll"><table><tr><th>Line</th><th>From</th><th>To</th><th>Every</th><th>Leaves at (16:xx)</th><th>Runtime</th><th>Battery</th><th>Simutrans line</th></tr>')
for l in S['line_order']:
    t = [x for x in NET[l] if x['n3h'] >= 3]
    bat = S['battery'].get(l)
    for i, x in enumerate(t):
        w('<tr>')
        if i == 0: w(f'<td rowspan="{len(t)}"><span class="badge">{l}</span></td>')
        w(f'<td>{E(x["o"])}</td><td>{E(x["d"])}</td><td class="n">{("%g min" % x["hw"]) if x["hw"] else ""}</td><td class="mins">{" ".join(mm(m) for m in x["m16"]) or "–"}</td><td class="n">{x["run"]} min</td>')
        if i == 0:
            w(f'<td rowspan="{len(t)}" class="note">' + (f'<span class="chip bat">battery</span> {E(bat["section"])}' if bat else '<span class="muted">under wire</span>') + '</td>')
            w(f'<td rowspan="{len(t)}">' + ' '.join(f'<a href="#line-{E(s.replace("+", "-"))}"><span class="badge sm">{E(s)}</span></a>' for s in sl_of[l]) + '</td>')
        w('</tr>')
w('</table></div>')

# ---- battery ------------------------------------------------------------------------------------------
w('<h2 id="battery">Battery sections</h2><p class="sub">Stretches run off the wire, on the traction battery. In the pak, every trolleybus object is a road vehicle with electric traction, so the game needs no wire and the sections are information only. Battery-capable types in this peak: ' + ', '.join(E(t) for t in sorted(BATT)) + ' (marked <span class="batmark" style="margin:0">battery</span> in the vehicle lists).</p><div class="batgrid">')
for l, b in S['battery'].items():
    tys = collections.Counter(u['type'] for s in sl_of[l] for u in LINES[s])
    w(f'<article class="batcard"><h3><span class="badge">{l}</span><small class="muted">Simutrans {E(", ".join(sl_of[l]))}</small></h3><div class="sec">{E(b["section"])}</div><p>{E(b["detail"])}</p>'
      f'<p><b>Out on {E(nice(S["vehicles_date"]))}:</b> ' + ', '.join(f'{n}× {E(t)}' for t, n in tys.most_common()) + f'</p><p class="muted"><a href="{E(b["source"])}">Source</a></p></article>')
w(f'</div><p class="sub">{E(S["no_battery_note"])}</p>')

# ---- Simutrans schedule ---------------------------------------------------------------------------------
w('<h2 id="schedule">Simutrans schedule</h2><p class="sub">Values to type into the fork’s Scheduling tab, on the stop entries listed for each Simutrans line. Units are calendar minutes; the offset is minutes after midnight, modulo the interval. Leave up to stays automatic (half the gap). <b>Every terminus here is a turning loop or a turn around a block, so every departure is set 1 min before the timetable departure, letting the trolleybus clear the loop on time.</b> Offset and each Also at value are the real minute − 1 (mod the interval; the interval is unchanged), with the real minutes shown underneath. This follows the Brno and Prague tram sheets and the Prague trolleybus sheet: a block turn counts as a loop. Put the timetable on the entry the trolleybus leaves from. Branches are separate lines, because Also at cannot change the route. The two DPMB pools (25 + 26, and 35 + 38 + 39) are one Simutrans line each, running the whole circuit, with some stops entered twice. Each Simutrans line is fitted at one rate: every entry sends the same number of vehicles an hour, or they would pile up at one end. Depot runs are not modelled.</p>')
w('<div class="scroll"><table class="sched"><tr><th>Line</th><th>Stop entry</th><th>Departure every</th><th>Offset</th><th>Also at</th><th>Terminus</th><th>Leave up to</th><th>Per hour</th><th>Matches real timetable</th><th>Vehicles</th></tr>')
for s in SCHED:
    n = len(s['rows']); ne = s['need']
    for i, r in enumerate(s['rows']):
        w('<tr>')
        if i == 0:
            w(f'<td rowspan="{n}" class="sl"><a href="#line-{E(s["id"].replace("+", "-"))}"><span class="badge">{E(s["id"])}</span></a><small>{E(s["name"].split(" ", 1)[1] if s["name"].startswith(s["id"].split("+")[0]) else s["name"])}</small>'
              + ('<small><span class="chip pool">pool</span></small>' if s['pool'] else '') + '</td>')
        real = f'<small class="real">real {r["real"][0]}' + (f'; {",".join(map(str, r["real"][1:]))}' if r['real'][1:] else '') + '</small>' if r['loop'] else ''
        term = '<span class="chip loop">loop −1 min</span>' if r['loop'] else f'<span class="chip">{E(r["terminus"])}</span><br><small class="muted">real minute</small>'
        lbl = f'<b>{E(r["stop"])}</b><br><span class="muted">to {E(r["to"])}' + (f' · as {E(r["line"])}' if '+' in s['id'] else '') + '</span>'
        match = f'<span class="chip ok">exact</span> {r["span"]}'
        if r['designed']:
            match += f'<br><span class="chip des">designed slot</span> real :{",:".join("%02d" % x for x in r["designed"])} is not in the timetable. {E(r["designed_why"])}'
        w(f'<td>{lbl}</td><td class="big">{r["every"]}</td><td class="big">{r["set"][0]}{real}</td>'
          f'<td class="big">{",".join(map(str, r["set"][1:])) or "–"}</td><td>{term}</td><td class="muted">auto</td><td class="n">{r["perh"]:g}</td><td class="note">{match}</td>')
        if i == 0:
            out_tb = len(tbs(LINES[s['id']])); out_bus = sum(1 for u in LINES[s['id']] if u['bus'] and not u.get('spare'))
            nsp_ = sum(1 for u in LINES[s['id']] if u.get('spare'))
            w(f'<td rowspan="{n}" class="note"><b>≥ {s["min_run"]}</b> by runtime'
              + (f'<br><b>{ne["vehicles"]}</b> by timetable cycle ({ne["minutes"]} min)' if ne else '')
              + f'<br><b>{out_tb}</b> trolleybuses out on Friday' + (f' + {out_bus} bus' if out_bus else '') + (f', {nsp_} not needed' if nsp_ else '') + '</td>')
        w('</tr>')
    if s['note']: w(f'<tr><td></td><td colspan="9" class="note">{E(s["note"])}</td></tr>')
w('</table></div>')
w('<p class="sub" style="margin-top:12px">Surplus vehicles are marked <span class="chip spare">not needed</span> (dimmed at the bottom of each card): where more were logged than the line needs, exactly the need stays counted, chosen so that every vehicle type of the line stays represented, and afternoon-only kurzy (then the highest kurz numbers) are dropped first. Not-needed vehicles are left out of every count, the depots and the pak totals (user rule, 29 Sep). Vehicles by timetable cycle: follow a vehicle leaving the first entry around 16:00 through every leg of its line, taking at each terminus the first departure at least 3 min after arriving, or less where the timetable itself turns faster (at Černého, Barvičova, Preslova and Pálavské náměstí the arrival and the next departure fall in the same minute). The empty run from Kamenný vrch to Nemocnice Bohunice is taken as 5 min. The 25 + 26 circuit lasts over six hours, longer than the peak, so it is followed on the peak pattern repeated every 20 min. Where more vehicles were out than the need, the surplus is marked not needed (above).</p>')

# ---- vehicles by line ---------------------------------------------------------------------------------------
w(f'<h2 id="lines">Trolleybuses by line</h2><p class="sub">One row per kurz out between about 15:00 and 17:00 on {E(nice(S["vehicles_date"]))}, grouped by Simutrans line. Each vehicle shows its number and depot (<span class="dot kom"></span>Komín, <span class="dot hus"></span>Husovice, <span class="dot sla"></span>Slatina), its full type and length, and the pak128 core. Kurz numbers are DPMB’s, per record line: 25 for the 25 + 26 pool, 39 for the 35 + 38 + 39 pool. Buses that worked a trolleybus kurz are listed with a <span class="chip bus">bus</span> mark and are not counted as trolleybuses.</p><div class="grid">')
for s in SCHED:
    o = sorted(LINES[s['id']], key=lambda u: (bool(u.get('spare')), u['kurz'])); sl = SL[s['id']]
    oc = [u for u in o if not u.get('spare')]
    mix = collections.Counter(u['type'] for u in oc)
    w(f'<article class="card" id="line-{E(s["id"].replace("+", "-"))}"><header><span class="badge">{E(s["id"])}</span><div class="t"><h3>{E(s["name"].split(" ", 1)[1] if s["name"][0].isdigit() and not "+" in s["id"] else s["name"])}</h3><div class="chips">')
    for k, n in mix.most_common(): w(f'<span class="tchip"><b>{n}×</b> {E(k)} · {LEN.get(k, "?")} m</span>')
    nb = len(oc) - len(tbs(o))
    w(f'</div></div><div class="count"><b>{len(tbs(o))}</b><span>trolleybuses{f" + {nb} bus" if nb else ""}</span></div></header>')
    txt = sl.get('pool_text') or S['splits_text'].get(sl['records']) if (sl.get('pool') or sl.get('kurzy')) else ''
    if txt: w(f'<p class="pooltext">{"<span class=\"chip pool\">pool</span> " if sl.get("pool") else "<span class=\"chip\">split, a choice</span> "}{E(txt)}</p>')
    nsp = len(o) - len(oc)
    if nsp:
        need_ = next((x['need']['vehicles'] for x in SCHED if x['id'] == s['id'] and x['need']), None)
        w(f'<p class="pooltext"><span class="chip spare">not needed</span> {len(o)} logged against {need_} needed by the timetable cycle; {nsp} marked not needed, keeping every trolleybus type of the line among the counted ones and dropping a substitute bus, then afternoon-only kurzy, first.</p>')
    w(f'<div class="scroll flat"><table><tr><th>Kurz</th><th>Vehicle · depot / type / pak object</th><th>Note</th></tr>')
    for u in o:
        sp = u.get('spare'); cls = ' '.join(c for c, on in (('busrow', u['bus']), ('spare', sp)) if on)
        w(f'<tr{f" class=\"{cls}\"" if cls else ""}><td class="n">{sl["records"]}/{u["kurz"]}</td><td>{cell(u)}</td><td class="note">' + ('<span class="chip spare">not needed</span> ' if sp else '') + f'{E(u["note"])}</td></tr>')
    w('</table></div></article>')
w('</div>')

# ---- pak -------------------------------------------------------------------------------------------------
w(f'<h2 id="pak">Pak128 objects</h2><p class="sub">Each type in the peak, mapped to the objects of the custom Czech pak128: VZ-DPBrno-trolleybus.pak for trolleybuses, VZ-DPBrno-bus.pak for the two buses. The lists above show only the pak core, the last part of the object name; full names follow VZ-DPBrno-&lt;type&gt;-&lt;livery&gt;-&lt;core&gt;. An articulated trolleybus is two objects that the depot builds as one vehicle (front, then -B); the lists show the first core only. Length is in car units per vehicle (16 = one tile). The pak has one livery per type (DPMB white-red, dpmbbilocervena), so the real livery never changes the object. {E(PAK["_source"])}</p>')
w('<div class="scroll"><table><tr><th>Type</th><th>Length</th><th>Pak core</th><th>Vehicles in the peak</th><th>Real liveries (vehicles)</th><th>Pak128 objects, in order</th><th>Car units</th><th>Status</th></tr>')
for t in sorted({u['type'] for u in units}, key=lambda t: (t not in LEN or LEN[t], t)):
    pk = PAK.get(t); us = [u for u in units if u['type'] == t]
    lv = collections.Counter(u['livery'] or 'not recorded' for u in us)
    lvtxt = '<br>'.join(f'{k}× {E(v)}' for v, k in lv.most_common(3)) + (f'<br>{sum(lv.values()) - sum(k for _, k in lv.most_common(3))}× in other liveries' if len(lv) > 3 else '')
    objs = '<br>'.join(f'<span class="pak">{E(x)}</span>' for x in pk['objs']) if pk else '<span class="pakmiss">missing</span>'
    kind = ' <span class="chip bus">bus</span>' if any(u['bus'] for u in us) else ('<span class="batmark">battery</span>' if t in BATT else '')
    w(f'<tr><td><b>{E(t)}</b>{kind}</td><td class="n">{LEN.get(t, "?")} m</td><td class="vp big2">{pakcore(t)}</td><td class="n">{len(us)}</td><td class="note">{lvtxt}</td><td>{objs}</td><td class="n">{pk["len"] if pk else "–"}</td>'
      f'<td class="note">{"<span class=\"chip ok\">installed</span> " if pk else ""}{E(pk["note"]) if pk else ""}</td></tr>')
w('</table></div>')

# ---- depots ------------------------------------------------------------------------------------------------
sla_lines = sorted({SL[s['id']]['records'] for s in SCHED for u in LINES[s['id']] if u['depot'] == 'Slatina' and not u['bus']}, key=int)
w('<h2 id="depots">Depots</h2><p class="sub">By the BMHD fleet register (evidence DPMB), read on ' + E(nice(S['register_date'])) + '. Komín and Husovice are trolleybus depots. Slatina is a bus garage that also keeps Škoda 32 Tr trolleybuses; on Friday they worked kurzy of ' + ', '.join(sla_lines) + '. DPMB’s trolleybus kurz numbers do not encode the depot the way odd and even tram kurzy do, so the register is the only view. Both buses came from Slatina.</p><div class="depots">')
for dep in S['depots']:
    rows = collections.defaultdict(list)
    for s in SCHED:
        for u in LINES[s['id']]:
            if u['depot'] == dep and not u.get('spare'): rows[s['id']].append(u)
    nv = sum(len(v) for v in rows.values())
    tm = collections.Counter(u['type'] for v in rows.values() for u in v)
    w(f'<article class="card depot" id="depot-{DCLS[dep]}"><header><div class="t"><h3><span class="dot big {DCLS[dep]}"></span>Vozovna {E(dep)}</h3><small>vehicles registered here</small></div><div class="count"><b>{nv}</b><span>vehicles out</span></div></header>')
    w('<div class="mix">' + ''.join(f'<span><b>{k}</b> {E(t)}</span>' for t, k in tm.most_common()) + '</div>')
    for s in SCHED:
        if s['id'] not in rows: continue
        v = sorted(rows[s['id']], key=lambda u: u['kurz'])
        w(f'<div class="dline"><div class="lhead"><span class="badge">{E(s["id"])}</span><small>{len(v)} vehicle{"s" if len(v) != 1 else ""}</small></div><div class="scroll flat"><table class="dt"><tr><th>Kurz</th><th>Vehicle · type · pak object</th></tr>')
        for u in v: w(f'<tr><td class="n">{SL[s["id"]]["records"]}/{u["kurz"]}</td><td>{cell(u, dep=False)}</td></tr>')
        w('</table></div></div>')
    w('</article>')
w('</div>')

# ---- termini -------------------------------------------------------------------------------------------------
w('<h2 id="termini">Termini at 16:00</h2><p class="sub">Every terminus served between 16:00 and 16:59, with its layout as far as the sources show it (Wikipedia, the BMHD wire map, bmhd.cz articles; “inferred” where the sources are indirect). Busiest first.</p>')
dep16 = collections.defaultdict(list)
for l in S['line_order']:
    for x in NET[l]:
        if x['m16'] and x['n3h'] >= 3: dep16[x['o']].append((l, x))
w('<div class="scroll"><table><tr><th>Terminus</th><th>Layout</th><th>Departures 16:00–16:59</th></tr>')
for nm in sorted(dep16, key=lambda n: (-sum(len(x['m16']) for l, x in dep16[n]), n)):
    deps = '<br>'.join(f'<span class="badge sm">{l}</span> to {E(x["d"])} <span class="mins">{" ".join(mm(v) for v in x["m16"])}</span>' for l, x in dep16[nm])
    w(f'<tr><td><b>{E(nm)}</b></td><td class="note">{E(S["termini"].get(nm, "?"))}</td><td>{deps}</td></tr>')
w('</table></div>')

# ---- not counted ------------------------------------------------------------------------------------------------
w(f'<h2 id="excluded">Not counted</h2><p class="sub">Records from {E(nice(S["vehicles_date"]))} left out of the afternoon count: morning-only duties.</p><div class="scroll"><table><tr><th>Kurz</th><th>Vehicle · type · pak object</th><th>Why</th></tr>')
veh = load(os.path.join(DER, f"vehicles_{S['register_date']}.json"))
for x in FL['excluded']:
    v = veh.get(x['car'], {})
    u = dict(car=x['car'], type=v.get('type') or '?', depot=v.get('depot', '?'))
    w(f'<tr><td class="n">{x["line"]}/{x["kurz"]}</td><td>{cell(u)}</td><td class="note">{E(x["why"])}</td></tr>')
w('</table></div>')

# ---- method ------------------------------------------------------------------------------------------------------
vd = S['vehicles_date']
w(f'''<h2 id="method">Method and sources</h2><div class="notes">
<p><b>Which day.</b> The network is the timetable in force from Tue 29 Sep 2026. Vehicles are from Fri 25 Sep, the last weekday before it (28 Sep was a public holiday), as on the Brno tram sheet. The timetable did not change between the two days.</p>
<p><b>Vehicles.</b> BMHD.cz vypravenost for {E(nice(vd))}, one page per line (<a href="https://www.bmhd.cz/vypravenost/vypravenost.php?datum={vd}&amp;linka=25">line 25</a>). <i>Ráno</i>, <i>ranní kurz</i> and <i>pouze ranní služba</i> mark morning-only duties. <i>Odpoledne</i> and <i>odpolední kurz</i> mark the afternoon car, and <i>ráno i odpoledne</i> a split duty. The row class tells a trolleybus from a bus. Thu 24 and Tue 29 Sep have the same number of records per line, so the gaps in kurz numbering are DPMB’s, not missing records.</p>
<p><b>Pools and splits.</b> 26 has no records of its own on weekdays: 25 kurzy work it. Likewise 35 and 38 are worked by 39 kurzy (bmhd.cz “Kurzy a nasazení”; jrbrno.cz combined 25 + 26 timetable). Lines 30 and 37 have two branches each, and which kurz ran which branch is not recorded, so the split is a stated choice sized by the timetable cycle.</p>
<p><b>Types and depots.</b> BMHD fleet register (evidence DPMB), exact type, depot and livery as read on {E(nice(S["register_date"]))}. Lengths: 12 m for Škoda 26 Tr, 32 Tr and SOR TNS 12; 18 m for the articulated Škoda 27 Tr and 31 Tr.</p>
<p><b>Timetable.</b> IDS JMK GTFS (kordis-jmk.cz/gtfs/gtfs.zip, exported 25 Sep, stored {E(nice(S["gtfs_date"]))}), trolleybus routes (route_type 800), service day {E(nice(S["service_date"]))}. The feed has no vehicle blocks, so the 25 + 26 and 35 + 38 + 39 circuits come from matching arrivals and departures at each terminus. Line 33 sends 9 an hour out and brings 6 back, and the feed has no trip for the other 3.</p>
<p><b>Simutrans schedule.</b> Fitted to the afternoon peak in whole calendar minutes with the fork’s Departure every / Offset / Also at fields, using the shared rule in pipeline/README.md (core 15:30–16:30, longest exact run, simplest pattern), at one rate per Simutrans line. Every terminus is treated as a loop (−1 min), block turns included.</p>
<p><b>Battery sections.</b> dpmb.cz (21, since 18 May 2026) and Wikipedia’s list of Brno trolleybus lines (30, since 27 Apr 2024). The rest of the network is under wire.</p>
<p><b>Rebuild.</b> This sheet is generated by pipeline/brno-trolleybus (state “{E(S["name"])}”), which imports the tram pipeline’s helpers from pipeline/brno; see pipeline/brno-trolleybus/README.md.</p>
</div>''')
w('''<script>
(function(){
  var c=document.querySelector('.controls'); function h(){document.documentElement.style.setProperty('--stick',(c.offsetHeight+8)+'px')} h(); addEventListener('resize',h);
  const q=document.getElementById('q'), hits=document.getElementById('hits');
  const all=[...document.querySelectorAll('.veh[data-v]')];
  q.addEventListener('input',()=>{
    const s=q.value.trim();
    let first=null, n=0;
    for(const el of all){
      const on = s.length>=3 && el.dataset.v.split('+').some(c=>c.startsWith(s));
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
print('rendered', dest, n_tb, 'trolleybuses', n_bus, 'buses')
