"""One oblast's sheet: python 06_render.py <oblast id>  ->  "<config.output_html>" in the working folder root.

schedule.json (05_schedule of odis-regional-hko), roster.json (04_vehicles), game.json (05b_game), line_class.json and
config.json. The page is the ODIS regional sheets' (style.html, copied from odis-regional-hko/templates), with the shared
sticky bar (line badges, section links, a vehicle search over every [data-v]); the display helpers slot_clock, leg_rows,
day_line and knot_text are those of odis-regional-hko/scripts/06_render.py (a script, so not importable).
Every bus is a 3-line cell: PID number · operator / full type · length / pak core · livery.
"""
import collections, html, json, os, re, sys
from common import HOME, DER, PIPE

OID = sys.argv[1]; BASE = os.path.join(HOME, 'oblasti', OID); D = os.path.join(BASE, 'data', 'derived')
PROJECT = os.path.dirname(PIPE)
E = lambda s: html.escape(str(s), quote=True)
ld = lambda n, dflt=None: json.load(open(os.path.join(D, n), encoding='utf-8')) if os.path.exists(os.path.join(D, n)) else dflt
CF = json.load(open(os.path.join(BASE, 'config.json'), encoding='utf-8'))
SH = json.load(open(os.path.join(HOME, 'config.json'), encoding='utf-8'))
S = ld('schedule.json'); COV = S.pop('_coverage'); C = ld('line_class.json'); R = ld('roster.json', dict(lines={}, totals={}))
GM = ld('game.json', {}); T = ld('trips.json')
LOOP = CF['all_termini_are_loops']
hm = lambda t: '%d:%02d' % (t // 60 % 24, t % 60)
LAB = lambda L: C[L].get('label', L) if L in C else L
def lkey(L): lab = LAB(L); return (0 if lab.isdigit() else 1, int(lab) if lab.isdigit() else 0, lab)

def slot_clock(P, r):
    if 60 % P == 0: return ':%02d' % (r % 60)
    ts = sorted(t % 1440 for t in range(r, r + 1440, P))
    if P >= 240: return ' · '.join(hm(t) for t in ts)
    return ' · '.join(hm(t) for t in ts if 720 <= t < 1200) + ' …'

def leg_rows(s):
    P = s['every']; rows = []
    for g in s['legs']:
        stop = f"{E(g['fr'])} <span class=\"arr\">→ {E(g['to'])}</span>"
        if g['untimed']:
            rows.append(f'<tr><td>{stop}</td><td class="n sv">0</td><td class="n">–</td><td>–</td><td class="fit">no timetable (empty return; leaves on arrival), {g["rt"]} min</td></tr>')
            continue
        sets = g['set']; P_ = P
        rs_ = sorted(((v + 60 + (1 if LOOP else 0)) % P) for v in sets)
        if len(rs_) >= 2 and P % len(rs_) == 0 and all((rs_[(i + 1) % len(rs_)] - rs_[i]) % P == P // len(rs_) for i in range(len(rs_))):
            P_ = P // len(rs_); sets = [sets[0] % P_]
        reals = [((v + 60 + (1 if LOOP else 0)) % P_) for v in sets]
        off = f'<span class="sv">{sets[0]}</span><small class="real">{slot_clock(P_, reals[0])}</small>'
        also = ' '.join(f'<span class="sv">{v}</span><small class="real">{slot_clock(P_, r)}</small>' for v, r in zip(sets[1:], reals[1:])) or '–'
        st = g['stat']; win = g['window']
        fit = f"{st['exact']} of {st['n']} real departures on the minute, {st['w3']} within 3 min; {g['rt']} min to {E(g['to'].split(', ')[-1])}"
        if g.get('knot'): fit += f"; timed at the terminal so the bus passes {E(g['knot']['stop'])} at {', '.join(slot_clock(P, r) for r in g['knot']['at'])} ({g['knot']['rt']} min on)"
        if g.get('joint'): fit += f"; set {g['joint']['moved']} min off its best fit ({slot_clock(P, g['joint']['fit'])}) so the buses turn in the shortest round"
        chk = f'<small>window slot without a real departure: {", ".join(hm(t) for t in win["empty"])}</small>' if win['empty'] else ''
        if P_ != P: fit += f"; written as every {P_}: its {P // P_} slots of the every-{P} line are evenly spaced"
        rows.append(f'<tr{" class=chk" if win["empty"] else ""}><td>{stop}</td><td class="n sv">{P_}</td><td class="n">{off}</td><td>{also}</td><td class="fit">{fit}{chk}</td></tr>')
    return ''.join(rows)

def day_line(g):
    out = []; kn = g.get('knot')
    for t in sorted(g.get('trips', []), key=lambda t: t['d']):
        if not 300 <= t['d'] < 1380: continue
        lab = (f"[{kn['stop'].split(', ')[-1]} {hm(t['dk'])}]" if kn and t['fr0'] != g['fr'] else hm(t['d'])) + ('' if t['line'] == g['lines'][0] else f" ({LAB(t['line'])})")
        if t['dev'] == 0: out.append(f'<b>{lab}</b>')
        elif t['dev'] <= 3: out.append(f'{lab}<sup>±{t["dev"]}</sup>')
        else: out.append(f'<span class="warn">{lab}<sup>{t["dev"]}</sup></span>')
    return ' '.join(out)

def knot_text(g, P):
    """the time the modelled bus passes each core point. On a leg with no slot in the window, 05_schedule's model times are
    the slots' minutes of the cycle, not clock times, so its deviations are read mod the interval and the passing times
    are written as clock times of the day"""
    out = []
    for k in g.get('knots', []):
        if not k['model']: continue
        ds = [min(d % P, P - d % P) for d in k['dev'] if d is not None]
        ts = k['model'] if g['window']['slots'] else sorted({(t + n * P) % 1440 for t in k['model'] for n in range(1440 // P)})
        ts = [t for t in ts if 300 <= t % 1440 < 1380] or ts
        out.append(f"{E(k['stop'])} {', '.join(hm(t) for t in ts[:4])}" + (f" (real within {max(ds)} min)" if ds else ''))
    return '; '.join(out)

def vcell(v, kind):
    p = v.get('pak') or {}
    cls = {'seen': 'v seen', 'designed': 'v added', 'nn': 'v spare'}[kind]
    paks = (f'<span class="pak">{E(p.get("core", "?"))} · {E(p.get("liv", "?"))}</span>' if p.get('ok') else
            f'<span class="pak subst">requested: {E(p.get("want") or p.get("core") or "?")}</span>')
    why = (f'<span class="addn" style="color:var(--ok)">seen on {E(v["seen"])}</span>' if kind == 'seen' else
           f'<span class="addn">{E(v.get("why", ""))}</span>' if kind == 'designed' else
           f'<span class="addn">not needed here: seen on {E(v.get("seen", ""))}' + (f'; counted on {E(v["elsewhere"])}' if v.get('elsewhere') else '') + '</span>')
    return (f'<li class="{cls}"><span class="num veh" data-v="{E(v["num"])}"><b>{E(v["num"])}</b> · {E(v.get("operator", ""))}</span>'
            f'<span class="vt">{E(v.get("full") or v.get("type"))} · {E(v.get("len", ""))}</span>{paks}{why}</li>')

def game_block(L, sims):
    g = GM.get(L) or {}; rows = g.get('game', [])
    if not rows and LAB(L).startswith('MHD'):
        return f'<p class="lnote"><b>In the game:</b> a town line; the save export of 30 Oct 2026 holds only the lines named 100300–100999, so check it in the game.</p>'
    if not rows:
        return f'<p class="lnote"><b>In the game:</b> no line {E(LAB(L))} in the save (export of 30 Oct 2026): a line to build.</p>'
    parts = []
    for r in rows:
        bits = [f"{r['convoys']} bus{'es' if r['convoys'] != 1 else ''}" if r['convoys'] else 'no buses', f"{r['stops']} stops"]
        if r['missing']: bits.append('missing ' + ', '.join(r['missing'][:12]) + (' …' if len(r['missing']) > 12 else ''))
        if r['extra']: bits.append('not served by the real line: ' + ', '.join(r['extra'][:8]) + (' …' if len(r['extra']) > 8 else ''))
        if not r['missing'] and not r['extra']: bits.append('stops match')
        if r['fixes']: bits.append(f"{len(r['fixes'])} halt name{'s' if len(r['fixes']) > 1 else ''} spelt differently")
        parts.append(f"<b>{E(r['name'])}</b>: " + '; '.join(E(b) for b in bits))
    extra = ''
    if len(sims) > len(rows): extra = f' The card has {len(sims)} Simutrans lines and the save {len(rows)}: the others are lines to build (or the owner may extend a game line).'
    return f'<p class="lnote"><b>In the game:</b> ' + ' · '.join(parts) + E(extra) + '</p>'

checks = []
def card(L):
    x = S[L]; c = C[L]; ros = {r['name']: r for r in R['lines'].get(L, [])}
    need = sum(s['need'] for s in x['sim']); an = x['anchor']
    head = (f'<header><a class="badge" href="#l-{E(L)}">{E(LAB(L))}</a><div class="hd"><h3>{E(c["name"])}</h3>'
            f'<p>{E(", ".join(c.get("operators", [])))} · licence {", ".join(c["lics"])} · {c["trips"]} trips on the day, {c["first"]}–{c["last"]} · modelled at {hm(an["anchor"])}'
            + (f' (busiest {hm(an["busiest"][0])}–{hm(an["busiest"][1])})' if an.get('busiest') and an.get('moved') else '') + '</p></div>'
            f'<div class="cnt"><b>{need}</b><span>buses needed</span></div></header>')
    n = len(x['sim'])
    body = f'<p class="lnote"><b>{n} Simutrans line{"s" if n != 1 else ""}:</b> ' + '; '.join(f"{E(s['name'])} every {s['every']}, {s['need']} bus{'es' if s['need'] != 1 else ''}" for s in x['sim']) + '.</p>'
    if not c.get('why', '').startswith('district'): body += f'<p class="lnote"><b>Why on this sheet:</b> {E(c.get("why", ""))}.</p>'
    if x.get('note'): body += f'<p class="lnote">{E(x["note"])}</p>'
    if x.get('core'): body += f'<p class="lnote"><b>Core points:</b> {" · ".join(E(s) for s in x["core"])}</p>'
    body += game_block(L, x['sim'])
    for s in x['sim']:
        P = s['every']; r = ros.get(s['name'], {})
        body += (f'<div class="sched"><h4>Simutrans line {E(s["name"])} · every {P} min · {s["need"]} bus{"es" if s["need"] != 1 else ""}</h4>'
                 + (f'<p class="lnote">{E(s["why"])}</p>' if s.get('why') else '')
                 + f'<div class="tw0"><table class="st2"><thead><tr><th>Entry</th><th class="n">Every</th><th class="n">Offset</th><th>Also at</th><th>Fit</th></tr></thead><tbody>{leg_rows(s)}</tbody></table></div>')
        dets = []
        for g in s['legs']:
            if g['untimed']: continue
            kt = knot_text(g, P)
            dets.append(f'<p><b>{E(g["fr"].split(", ")[-1])} →</b> real departures, whole day (at the terminal; bold = on the minute, orange = off the pattern, min off in superscript'
                        + (f'; [brackets] = a trip that starts beyond the terminal, at its time at {E(g["knot"]["stop"])}' if g.get('knot') else '') + f'): {day_line(g)}</p>'
                        + (f'<p class="win">Passes: {kt}</p>' if kt else '') + f'<p class="win">Stops: {" – ".join(E(z) for z in g["stops"])}</p>')
            if g['window']['empty'] or any(t['dev'] > 3 and s['window'][0] <= t['d'] < s['window'][1] for t in g.get('trips', [])):
                checks.append((L, s['name'], g, s))
        waits = '; '.join(f"{E(k.split(', ')[-1] if isinstance(k, str) else k)} {', '.join(str(w) for w in v)} min" for k, v in s['waits'].items())
        body += f'<p class="need">Window {hm(s["window"][0])}–{hm(s["window"][1])}. Buses: {s["need"]}, following each bus round the slots with the real running times (waits at the terminals: {waits}).</p>'
        body += f'<details><summary>Whole day and stops</summary>{"".join(dets)}</details></div>'
        vs = ''.join(vcell(v, 'seen') for v in r.get('seen', [])) + ''.join(vcell(v, 'designed') for v in r.get('designed', []))
        body += f'<p class="brsub">Buses on {E(s["name"])}</p><ul class="vs">{vs or "<li>pending</li>"}</ul>'
        if r.get('not_needed'):
            body += f'<details class="nn"><summary>{len(r["not_needed"])} more seen, not needed on {E(s["name"])}</summary><ul class="vs">{"".join(vcell(v, "nn") for v in r["not_needed"])}</ul></details>'
    return f'<article class="card" id="l-{E(L)}">{head}{body}</article>'

mod = sorted(S, key=lkey)
other = CF['other_sheets']; comp = other.get('praha_bus', {}).get('lines', [])
unm = sorted((L for L in C if L not in S and L not in comp), key=lkey)
cards = ''.join(card(L) for L in mod)
nav = ''.join(f'<a class="badge sm" href="#l-{E(L)}">{E(LAB(L))}</a>' for L in mod)

comp_html = ''
if comp:
    comp_html = (f'<h2 id="prague">On the Prague bus sheet</h2><p class="sub">{E(other["praha_bus"]["why"])}. They are listed here and not repeated; '
                 f'their buses are counted there. <a href="{E(other["praha_bus"]["url"])}">Prague Bus Lines Check</a>.</p>'
                 '<div class="types"><table class="tlist"><thead><tr><th>Line</th><th>Route</th><th>On the day</th></tr></thead><tbody>'
                 + ''.join(f'<tr><td><a class="badge sm" href="{E(other["praha_bus"]["url"])}">{E(LAB(L))}</a></td><td>{E(C[L]["name"])}</td><td>{C[L]["trips"]} trips</td></tr>' for L in sorted(comp, key=lkey))
                 + '</tbody></table></div>')
unm_html = ''
if unm:
    unm_html = ('<h2 id="unmodelled">Not modelled</h2><p class="sub">Lines of this oblast with no Simutrans line, each with the reason (bus schedule method Step 8: a long-interval line only where it is a place’s only service).</p>'
                '<div class="types"><table class="tlist"><thead><tr><th>Line</th><th>Route</th><th>On the day</th><th>Why</th></tr></thead><tbody>'
                + ''.join(f'<tr><td><span class="badge sm" style="background:var(--muted)">{E(LAB(L))}</span></td><td>{E(C[L]["name"])}</td><td>{C[L]["trips"]} trips{(", " + C[L]["first"] + "–" + C[L]["last"]) if C[L]["first"] else ""}</td><td>{E(CF["unmodelled"].get(L, ""))}</td></tr>' for L in unm)
                + '</tbody></table></div>')

def chk_badge(L):
    """an owner check names a line (badge linking to its card) or the whole sheet (plain label)"""
    k = (L.split() or [''])[0]
    return f'<a class="badge sm" href="#l-{E(k)}">{E(LAB(k))}</a>' if k in S else f'<span class="badge sm" style="background:var(--muted)">{E(L)}</span>'
chk_rows = ''.join(f'<tr class="chk"><td>{chk_badge(L)}</td><td colspan="2"><b>Chosen here, to confirm:</b> {E(t)}</td><td colspan="2"><b>Alternative:</b> {E(alt)}</td></tr>'
                   for L, t, alt in CF.get('owner_checks', []))
for L, name, g, s in checks:
    P = s['every']; W = s['window']
    off = [t for t in g['trips'] if t['dev'] > 3 and W[0] <= t['d'] < W[1]]
    chk_rows += (f'<tr><td><a class="badge sm" href="#l-{E(L)}">{E(LAB(L))}</a></td><td>{E(name)}</td><td>{E(g["fr"])} → {E(g["to"].split(", ")[-1])}</td>'
                 f'<td>every {P} at {", ".join(slot_clock(P, r) for r in g["real"])}</td><td>'
                 + '; '.join([f"slot {hm(t)} has no real departure" for t in g['window']['empty']] + [f"{hm(t['d'])} is {t['dev']} min off" for t in off]) + '</td></tr>')

# in the game: lines to build, game lines to fix
gl_rows = ''
for L in mod:
    g = GM.get(L, {}); rows = g.get('game', [])
    if not rows and LAB(L).startswith('MHD'): gl_rows += f'<tr><td><a class="badge sm" href="#l-{E(L)}">{E(LAB(L))}</a></td><td>not in the export (town line)</td><td>check it in the game</td></tr>'; continue
    if not rows: gl_rows += f'<tr><td><a class="badge sm" href="#l-{E(L)}">{E(LAB(L))}</a></td><td>none</td><td>build {len(S[L]["sim"])} Simutrans line{"s" if len(S[L]["sim"]) > 1 else ""}</td></tr>'; continue
    for r in rows:
        todo = (['add buses'] if not r['convoys'] else []) + (['stops differ'] if r['missing'] or r['extra'] else []) + ['set the timetable']
        gl_rows += f'<tr><td><a class="badge sm" href="#l-{E(L)}">{E(LAB(L))}</a></td><td>{E(r["name"])} ({r["convoys"]} buses, {E(r["state"])})</td><td>{E(", ".join(todo))}</td></tr>'

# operators, types, pak
units = []
for L, rs in R['lines'].items():
    for r in rs:
        for v in r['seen']: units.append((v.get('operator') or '?', L, r['name'], v, 'seen'))
        for v in r['designed']: units.append((v.get('operator') or '?', L, r['name'], v, 'designed'))
dep = collections.defaultdict(list)
for u in units: dep[u[0]].append(u)
dep_html = ''; depnav = []
for b in sorted(dep, key=lambda b: (-len(dep[b]), b)):
    k = re.sub(r'\W+', '', b.lower())
    depnav.append(f'<a href="#d-{k}" data-dep="{k}">{E(b)} <b>{len(dep[b])}</b></a>')
    byt = collections.defaultdict(list)
    for u in dep[b]: byt[u[3].get('full') or u[3].get('type')].append(u)
    rows = ''.join(f'<div class="dl"><span class="dc">{len(us)}</span><span></span><div><p class="mixline">{E(ty)}</p><ul class="vs">'
                   + ''.join(f'<li class="v {"seen" if kd == "seen" else "added"}"><span class="num veh" data-v="{E(v["num"])}"><b>{E(v["num"])}</b> · line {E(nm_)}</span><span class="pak">{E((v.get("pak") or {}).get("core", "?"))}</span></li>'
                             for _, L, nm_, v, kd in sorted(us, key=lambda u: str(u[3]['num']))) + '</ul></div></div>'
                   for ty, us in sorted(byt.items(), key=lambda x: -len(x[1])))
    dep_html += f'<div class="depot" id="d-{k}" data-depot="{k}"><header><h3>{E(b)}<small>operator</small></h3><b class="core">{len(dep[b])}</b></header>{rows}</div>'
pk = collections.Counter(); pinfo = {}
for _, L, nm_, v, kd in units:
    p = v.get('pak') or {}; kk = (v.get('full') or v.get('type'), v.get('paint', ''), p.get('obj') or p.get('want'))
    pk[kk] += 1; pinfo[kk] = p
pak_rows = ''.join(f'<tr><td>{E(t)}<br><span class="pak">{E(paint or "paint not in the register")}</span></td><td class="mono">{"" if pinfo[k]["ok"] else "requested: "}{E(o or "none")}</td><td>{E(pinfo[k].get("liv", ""))}</td><td class="n">{pinfo[k].get("length") or ""}</td><td class="n">{n}</td></tr>'
                   for k, n in sorted(pk.items(), key=lambda x: -x[1]) for t, paint, o in [k])

cov_html = (f'<h2 id="coverage">Coverage</h2><p class="sub">Every stop this sheet\'s lines serve in 13:00–19:00 on {E(CF["vehicle_day_label_en"])} is on a modelled Simutrans line '
            f'(owner, 20 Oct 2026: "501 is the only line running to Dětmarovice, how can we not model that?"). {COV["served"]} stops: {COV["here"]} on this sheet\'s Simutrans lines, '
            f'{len(COV["elsewhere"])} on lines of other sheets (the other oblasts, the Prague bus sheet), {len(COV["uncovered"])} uncovered.</p>')
if COV['uncovered']:
    cov_html += '<div class="types"><table class="tlist"><tbody>' + ''.join(f'<tr><td>{E(s)}</td><td>{", ".join(E(LAB(x)) for x in v["lines"])}</td><td>{E(v["why"])}</td></tr>' for s, v in COV['uncovered'].items()) + '</tbody></table></div>'

tot_need = sum(s['need'] for L in mod for s in S[L]['sim'])
tot_seen = sum(len(r['seen']) for L in mod for r in R['lines'].get(L, [])); tot_des = sum(len(r['designed']) for L in mod for r in R['lines'].get(L, []))
nsim = sum(len(S[L]['sim']) for L in mod)
style = open(os.path.join(HOME, 'scripts', 'style.html'), encoding='utf-8').read().replace('{{TITLE}}', E(CF['title']))
intro = CF.get('notes') or ''
page = f'''{style}
<header class="top">
  <div style="flex:1;min-width:min(100%,420px)">
    <p class="eyebrow">PID regional buses · {E(CF["oblast_name"])} (okres {E(CF["okres"])}) · {E(CF["vehicle_day_label_en"])}</p>
    <h1>{E(CF["title"])}</h1>
    <p class="lede">Every PID bus line of okres {E(CF["okres"])} (licences {E(CF["prefix"][:2])}xxxx) and the Prague and other lines whose outer end lies here, set as Simutrans lines with the owner's regional method: each line read over the whole day at its core points, a repeating interval, destination and shift variants on their own longer intervals (at most 480 min), timetables at the terminals worked back from the knots, every afternoon stop on a line, buses sized from the pattern. {E(intro)}</p>
  </div>
  <div class="stats">
    <div class="stat"><b>{tot_need}</b><span>buses needed</span></div>
    <div class="stat"><b>{tot_seen}</b><span>seen on the live map</span></div>
    <div class="stat"><b>{tot_des}</b><span>designed</span></div>
    <div class="stat"><b>{len(mod)}</b><span>lines modelled</span></div>
    <div class="stat"><b>{nsim}</b><span>Simutrans lines</span></div>
  </div>
</header>
<div class="controls">
  <nav class="nav lines" aria-label="Lines"><span class="lab">Lines</span>{nav}</nav>
  <nav class="nav dnav" aria-label="Sections"><a href="#checks">To check</a><a href="#game">In the game</a>{'<a href="#prague">On the Prague sheet</a>' if comp else ''}{'<a href="#unmodelled">Not modelled</a>' if unm else ''}<a href="#coverage">Coverage</a><span class="lab">Operators</span>{"".join(depnav)}<a href="#pak">Pak128 objects</a><a href="#method">How this was built</a></nav>
  <input type="search" id="q" placeholder="Find vehicle, e.g. 9513" aria-label="Find vehicle number"><span id="hits" aria-live="polite"></span>
</div>

<h2>How to read the line cards</h2>
<p class="sub"><b>Typing the timetable.</b> Values go into the Scheduling tab of the terminal entry, with the calendar on: Departure every, Offset, Also at (at most 7). Offsets count from 01:00 and every terminal is set as a loop, so each value is (real departure − 61) mod interval; the real clock minute is under every value. A row with Every 0 has no timetable: the bus leaves on arrival.</p>
<p class="sub"><b>Core points and knots.</b> Each line was read over the whole operating day (5:00–23:00) at its core points: terminals, knots where variants split, shared hubs. A trip counts at the time it passes a core point, wherever it starts. Where a slot is defined at a knot, the terminal departure is the knot time minus the running time, and the knot gets no timetable.</p>
<p class="sub"><b>Variants.</b> Each destination, path or shift variant is its own Simutrans line on a longer interval (the save game's Ex4). Shift lines repeat every 480 (8 h), the longest interval allowed. Trips more than 3 min off every slot are off the pattern, in orange.</p>
<p class="sub"><b>Buses needed.</b> One bus followed round the line's own slots with the real running times and at least 3 min at each terminal. Real buses swap lines at the terminals, so per-line totals are higher than what the operators run; pooling lines is the owner's choice and is not done.</p>
<p class="sub"><b>In the game.</b> Each card compares the save's line (export of 30 Oct 2026) with the modelled stops. The save's buses are shown as a check; the sheet is built from the real timetable and the buses seen running, so a game line may need buses added or moved.</p>

<h2 id="checks">To check</h2>
<p class="sub">Choices made here that you may want to flip, each with its alternative; then the Simutrans lines whose model window has a slot without a real departure, or a real departure more than 3 min off.</p>
<div class="types"><table class="tlist"><thead><tr><th>Line</th><th>Simutrans line</th><th>Entry</th><th>Pattern</th><th>In the window</th></tr></thead><tbody>{chk_rows}</tbody></table></div>

<h2 id="lines">Lines</h2>
<div class="grid">{cards}</div>

<h2 id="game">In the game</h2>
<p class="sub">What the save (export of 30 Oct 2026) needs for this sheet: lines to build, and game lines whose stops, buses or timetable differ.</p>
<div class="types"><table class="tlist"><thead><tr><th>Line</th><th>Game line</th><th>To do</th></tr></thead><tbody>{gl_rows}</tbody></table></div>

{comp_html}
{unm_html}
{cov_html}

<h2 id="depots">Operators</h2>
<p class="sub">Buses by operator (the live map's "Dopravce") and type. A seen bus counts at its operator; a designed bus too.</p>
<div class="depots">{dep_html}</div>

<h2 id="pak">Pak128 objects</h2>
<p class="sub">Regional PID buses use the VZ-PID-bus objects, town lines the VZ-MHD&lt;Town&gt; ones (pak rules); objects are read from the installed pak. "requested" marks a type with no object yet (pak_request.md).</p>
<div class="types"><table><thead><tr><th>Real type and paint</th><th>Pak128 object</th><th>Livery</th><th class="n">Length</th><th class="n">Buses</th></tr></thead><tbody>{pak_rows}</tbody></table></div>

<h2 id="method">How this was built</h2>
<div class="notes">
<p><b>Scope.</b> {E(SH["gtfs"]["why"])} The Středočeský kraj licenses each district's lines with its own prefix ({E(CF["prefix"][:2])}xxxx = okres {E(CF["okres"])}); a line licensed by Prague or by another kraj is on the sheet of the okres of its outer end (the first stop, coming in from the far end, in a Středočeský municipality), or, with no Prague end, of the okres most of its stops lie in. {len(C)} lines: {len(mod)} modelled here, {len(comp)} on the Prague bus sheet, {len(unm)} listed with the reason.</p>
<p><b>Method.</b> pipeline/bus-schedule-method.md (v4): whole-day reading at core points, repeating interval, Ex4 variants, timing at terminals worked back from the knots, no daily lines (at most every 480), every afternoon stop on a line, buses from the pattern, every line checked by hand (method-check file in the pipeline folder).</p>
<p><b>Buses.</b> {E(SH["live"]["note"])} A bus fills one Simutrans line it ran in that line's window, by matching, across all twelve oblast sheets; buses on the Prague bus sheet are not used here.</p>
<p>Sources: <a href="https://data.pid.cz/PID_GTFS.zip">PID GTFS</a>, <a href="https://mapa.pid.cz/">PID live map</a>, the save-game export of 30 Oct 2026 (engine session).</p>
</div>
<script>
(function(){{
  var c=document.querySelector('.controls'); function h(){{document.documentElement.style.setProperty('--stick',(c.offsetHeight+8)+'px')}} h(); addEventListener('resize',h);
  const q=document.getElementById('q'), hits=document.getElementById('hits');
  const all=[...document.querySelectorAll('.veh[data-v]')];
  q.addEventListener('input',()=>{{
    const s=q.value.trim(); let first=null, n=0;
    for(const el of all){{
      const on = s.length>=2 && el.dataset.v.split('+').some(c=>c.toLowerCase().startsWith(s.toLowerCase()));
      el.classList.toggle('hit',on);
      if(on){{ n++; const hid=el.closest('details:not([open])'); if(!first || (first.closest('details:not([open])') && !hid)) first=el; }}
    }}
    hits.textContent = s.length>=2 ? (n? n+' found':'not found') : '';
    if(first){{ const d=first.closest('details'); if(d) d.open=true; first.scrollIntoView({{block:'center'}}); }}
  }});
  [].forEach.call(c.querySelectorAll('a[data-dep]'),function(a){{
    a.addEventListener('click',function(e){{
      var t=document.querySelector('[data-depot="'+a.getAttribute('data-dep')+'"]');
      if(t){{ e.preventDefault(); t.scrollIntoView({{block:'start'}}); }}
    }});
  }});
}})();
</script>
'''
out = os.path.join(PROJECT, CF['output_html'])
open(out, 'w', encoding='utf-8').write(page)
print('wrote', out, len(page), 'bytes;', tot_need, 'buses,', tot_seen, 'seen,', tot_des, 'designed;', len(checks), 'rows to check')
