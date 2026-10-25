"""Render the Plzeň sheet for one state into the project root.

  python 05_render.py --state 2026-09-27
"""
import argparse, collections, datetime, html, os
from common import DER, ASSETS, PROJECT, state, load, mm
import sticky

p = argparse.ArgumentParser(); p.add_argument('--state', required=True); a = p.parse_args()
S = state(a.state); X = S['texts']; PAK = S['pak']; LEN = S['length_m']
TT = load(os.path.join(DER, S['name'], 'timetable.json')); FL = load(os.path.join(DER, S['name'], 'fleet.json'))
E = lambda s: html.escape(str(s), quote=True)
ORDER = S['line_order']; pm = FL['pm']; exc = FL['excluded']
byline = collections.defaultdict(list)
for q in pm: byline[q['line']].append(q)

def cell(cars, types):
    ln = sum(LEN[t] for t in types)
    return (f'<div class="vb"><span class="vn">{" + ".join(f'<span data-v="{c}">{c}</span>' for c in cars)} <span class="vd">· {E(S["depot"])}</span></span>'
            f'<span class="vt">{E(" + ".join(types))} <span class="muted">· {ln} m</span></span>'
            f'<span class="vp">{E(" + ".join(PAK[t]["core"] for t in types))}</span></div>')

tot = len(pm); cars = sum(len(q['cars']) for q in pm)
out = []; w = out.append
w(open(os.path.join(ASSETS, 'style.css.html'), encoding='utf-8').read())
w(sticky.CSS)
w('<style>@media (max-width:700px){  /* phones: keep the sticky bar short, badge and depot rows scroll sideways (as on the Olomouc and Prague sheets; added here so the shared sticky.py copies stay identical) */.controls{gap:6px 12px;padding-block:8px}.controls>.nav{flex:1 1 100%}.controls .nav.lines,.controls .nav.dnav{flex-wrap:nowrap;overflow-x:auto;min-width:0;scrollbar-width:none;-webkit-overflow-scrolling:touch}.controls .nav.lines::-webkit-scrollbar,.controls .nav.dnav::-webkit-scrollbar{display:none}.controls .nav.lines>*,.controls .nav.dnav>*{flex-shrink:0;white-space:nowrap}.controls input[type=search]{flex:1 1 150px;padding:4px 8px}}tr.subhead .keep{position:sticky;left:10px;display:inline-block;max-width:calc(100vw - 72px)}</style>')
w('<style>tr.spare td{opacity:.55}.chip.spare{background:var(--surface2);color:var(--muted)}</style>')
w(f'''<header class="top"><div class="intro"><div class="eyebrow">{E(X['eyebrow'])}</div>
<h1>{E(S['title'])}</h1>
<p class="lede">{E(X['lede'])}</p></div>
<div class="stats"><div class="stat"><b>{len(ORDER)}</b><span>lines</span></div><div class="stat"><b>{tot}</b><span>trams out</span></div><div class="stat"><b>{cars}</b><span>cars</span></div><div class="stat"><b>1</b><span>depot</span></div></div></header>
{sticky.controls([(f'#line-{l}', l) for l in ORDER], [(S['depot'], S['depot'], tot)],
                 [('#network', X['nav_network']), ('#schedule', 'Simutrans schedule'), ('#pak', 'Pak128 objects'), ('#excluded', 'Not counted'), ('#method', 'Method')], '378')}
''')
# network
w(f'<h2 id="network">{E(X["network_heading"])}</h2><p class="sub">{E(X["network_intro"])}</p>')
w('<div class="scroll"><table><tr><th>Line</th><th>From</th><th>To</th><th>Every</th><th>Leaves at (16:xx)</th><th>Runtime</th><th>Trams</th><th>Note</th></tr>')
for l in ORDER:
    t = TT['network'][l]
    for i, x in enumerate(t):
        w('<tr>')
        if i == 0: w(f'<td rowspan="{len(t)}"><span class="badge">{l}</span></td>')
        w(f'<td>{E(x["o"])}</td><td>{E(x["d"])}</td><td class="n">{x["hw"]:g} min</td><td class="mins">{" ".join(mm(m) for m in x["m16"])}</td><td class="n">{x["run"]} min</td>')
        if i == 0: w(f'<td rowspan="{len(t)}" class="n"><b>{len(byline[l])}</b></td><td rowspan="{len(t)}" class="note">{E(S["line_notes"][l])}</td>')
        w('</tr>')
w('</table></div>')
# schedule
w('<h2 id="schedule">Simutrans schedule</h2><p class="sub">Values to type into the fork’s Scheduling tab, on the terminus entries of each line. Units are calendar minutes. The offset counts from 01:00, as the fork does: minutes after 01:00 modulo the interval (the same as after midnight for every interval that divides 60); every interval divides 1440, so the pattern runs unchanged all day. Leave up to stays automatic (half the gap). <b>Loop terminus: every departure is set 1 min before the timetable departure, so the tram clears the loop on time. The fork counts offsets from 01:00, so on an interval that does not divide 60 the typed value is (real − 60 − 1) mod the interval: the real minute is under each value.</b> Every Plzeň terminus is a loop, so every offset is the real minute − 1 (mod the interval); the real minutes are shown underneath. Put the timetable on the entry the tram leaves from: where a loop has a separate alighting stop set to All off, use the boarding (departure) entry. Each pattern reproduces the real departures exactly over the span shown. Depot runs are not modelled.</p>')
w('<div class="scroll"><table class="sched"><tr><th>Line</th><th>Stop entry</th><th>Departure every</th><th>Offset</th><th>Also at</th><th>Terminus</th><th>Leave up to</th><th>Per hour</th><th>Matches real timetable</th><th>Trams</th></tr>')
vd = S['vehicles_date']
for s in TT['schedule']:
    n = len(s['rows'])
    for i, r in enumerate(s['rows']):
        w('<tr>')
        if i == 0: w(f'<td rowspan="{n}" class="sl"><span class="badge">{s["id"]}</span><small>{E(s["name"].split(" ", 1)[1])}</small></td>')
        real = f'<small class="real">real {r["real"][0]}' + (f'; {",".join(map(str, r["real"][1:]))}' if r['real'][1:] else '') + '</small>' if r['loop'] else ''
        term = '<span class="chip loop">loop −1 min</span>' if r['loop'] else '<span class="chip">real minute</span>'
        w(f'<td><b>{E(r["stop"])}</b><br><span class="muted">to {E(r["to"])}</span></td><td class="big">{r["every"]}</td><td class="big">{r["set"][0]}{real}</td>'
          f'<td class="big">{",".join(map(str, r["set"][1:])) or "–"}</td><td>{term}</td><td class="muted">auto</td><td class="n">{r["perh"]:g}</td><td class="note"><span class="chip ok">exact</span> {r["span"]}</td>')
        if i == 0: w(f'<td rowspan="{n}" class="note"><b>≥ {s["min_trams"]}</b> by runtime<br><b>{FL.get("need", {}).get(s["id"], "?")}</b> needed (cycle / on the road)<br>{len(byline[s["id"]])} counted on {int(vd[8:])} Sep' + (f', {nsp} not needed' if (nsp := sum(1 for q in FL.get('spares', []) if q['line'] == s['id'])) else '') + '</td>')
        w('</tr>')
    if s['note']: w(f'<tr><td></td><td colspan="9" class="note">{E(s["note"])}</td></tr>')
w('</table></div>')
# lines
w(f'<h2 id="lines">Trams by line</h2><p class="sub">One row per kurz out between about 15:00 and 17:00 on {datetime.date(*map(int, vd.split("-"))).strftime("%a")} {int(vd[8:])} Sep, with the cars in the order they were coupled. Each cell gives the car numbers and depot, the full types, and the pak core. Kurzy 21 and up are peak-only split duties. Where more trams were logged than a line needs (the larger of its timetable cycle and the most trams on the road at once, 16:00–16:59), exactly the need is counted, keeping every tram type of the line, and the rest are listed at the bottom of the card as <span class="chip spare">not needed</span>, afternoon-only kurzy first (user rule, 29 Sep).</p><div class="grid">')
for l in ORDER:
    o = sorted(byline[l], key=lambda q: q['kurz'])
    mix = collections.Counter(' + '.join(q['types']) for q in o)
    w(f'<article class="card" id="line-{l}"><header><span class="badge">{l}</span><div class="t"><h3>{E(S["route"][l])}</h3><div class="chips">')
    for k, c in mix.most_common(): w(f'<span class="tchip"><b>{c}×</b> {E(k)}</span>')
    w(f'</div></div><div class="count"><b>{len(o)}</b><span>trams</span></div></header><div class="scroll flat"><table><tr><th>Kurz</th><th>Tram · depot / type / pak object</th><th>Note</th></tr>')
    for q in o: w(f'<tr><td class="n">{q["kurz"]}</td><td>{cell(q["cars"], q["types"])}</td><td class="note">{E(q["note"])}</td></tr>')
    sp = sorted((q for q in FL.get('spares', []) if q['line'] == l), key=lambda q: q['kurz'])
    if sp:
        w(f'<tr class="subhead"><td colspan="3"><span class="keep">Not needed · {len(sp)} tram{"s" if len(sp) != 1 else ""} beyond the need of {FL["need"].get(l, "?")}, not counted</span></td></tr>')
        for q in sp: w(f'<tr class="spare"><td class="n">{q["kurz"]}</td><td>{cell(q["cars"], q["types"])}</td><td class="note"><span class="chip spare">not needed</span> {E(q["note"])}</td></tr>')
    w('</table></div></article>')
w('</div>')
# pak
LVC = collections.defaultdict(collections.Counter)
for q in pm:
    for t, lv in zip(q['types'], q['liveries']): LVC[t][lv] += 1
w(f'<h2 id="pak">Pak128 objects</h2><p class="sub">{E(X["pak_intro"])}</p><div class="scroll"><table><tr><th>Type</th><th>Pak core</th><th>Cars in the peak</th><th>Real liveries (cars)</th><th>Object, in order</th><th>Pak</th><th>Status</th></tr>')
for t in sorted(LVC, key=lambda t: -sum(LVC[t].values())):
    pk = PAK[t]; n = sum(LVC[t].values()); top = LVC[t].most_common(1); rest = n - top[0][1]
    lv = f'{top[0][1]}× {E(top[0][0])}' + (f'<br>{rest}× advertising wraps' if rest else '')
    st = '<span class="chip ok">installed</span> ' if pk['status'] == 'installed' else '<span class="pakmiss">stand-in</span> '
    w(f'<tr><td><b>{E(t)}</b></td><td class="vp big2">{E(pk["core"])}</td><td class="n">{n}</td><td class="note">{lv}</td><td><span class="pak">{E(pk["objs"])}</span></td><td>{E(pk["pak"])}</td><td class="note">{st}{E(pk["note"])}</td></tr>')
w('</table></div>')
# depot
w(f'<h2 id="depots">Depot</h2><p class="sub">PMDP has one tram depot, Vozovna {E(S["depot"])}, next to the Slovany terminus of line 1. Every car in the peak is based there.</p>')
tm = collections.Counter(t for q in pm for t in q['types'])
w(f'<div class="depots"><article class="card depot" id="d-{E(S["depot"])}" data-depot="{E(S["depot"])}"><header><div class="t"><h3>Vozovna {E(S["depot"])}</h3><small>all lines</small></div><div class="count"><b>{cars}</b><span>cars on {tot} trams</span></div></header>')
w('<div class="mix">' + ''.join(f'<span><b>{c}</b> {E(t)}</span>' for t, c in tm.most_common()) + '</div>')
for l in ORDER:
    o = sorted(byline[l], key=lambda q: q['kurz'])
    w(f'<div class="dline"><div class="lhead"><span class="badge">{l}</span><small>{len(o)} trams</small></div><div class="scroll flat"><table class="dt"><tr><th>Kurz</th><th>Tram · type · pak object</th></tr>')
    for q in o: w(f'<tr><td class="n">{q["kurz"]}</td><td>{cell(q["cars"], q["types"])}</td></tr>')
    w('</table></div></div>')
w('</article></div>')
# not counted
w(f'<h2 id="excluded">Not counted</h2><p class="sub">Records from {int(vd[8:])} Sep left out of the afternoon count: morning-only duties and cars replaced during the day.</p><div class="scroll"><table><tr><th>Line</th><th>Kurz</th><th>Tram · type · pak object</th><th>Why</th></tr>')
for x in exc: w(f'<tr><td><span class="badge">{x["line"]}</span></td><td class="n">{x["kurz"]}</td><td>{cell(x["cars"], x["types"])}</td><td class="note">{E(x["why"])}</td></tr>')
w('</table></div>')
w('<h2 id="method">Method and sources</h2><div class="notes">\n' + '\n'.join(X['method']) + '\n</div>')
w(sticky.SCRIPT)
dest = os.path.join(PROJECT, S['output']); open(dest, 'w', encoding='utf-8').write(''.join(out).replace('<nav class="nav" aria-label="Lines">', '<nav class="nav lines" aria-label="Lines">', 1))
print('rendered', dest, tot, 'trams', cars, 'cars')
