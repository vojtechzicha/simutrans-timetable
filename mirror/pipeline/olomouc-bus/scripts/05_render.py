"""Render the Olomouc bus sheet for one state into the project root.

  python 05_render.py --state 2026-09-29

The page is the Brno bus sheet's (pipeline/brno-bus/scripts/05_render.py): the Brno tram style (assets/style.css.html,
copied) plus the trolleybus sheet's extra CSS with the sticky header and search (assets/extra.css.html, copied).
Vehicle cell (shared rule): 1) number · depot  2) full type · length  3) pak core (livery added only where the pak has
more than one livery object for that family).
"""
import argparse, collections, html, os, re
from common import DER, ASSETS, PROJECT, state, load, mm, hm, nice

p = argparse.ArgumentParser(); p.add_argument('--state', required=True); a = p.parse_args()
S = state(a.state); X = S['texts']
TT = load(os.path.join(DER, S['name'], 'timetable.json'))
FL = load(os.path.join(DER, S['name'], 'fleet.json'))
PM = load(os.path.join(ASSETS, 'pak_map.json'))
COV = load(os.path.join(DER, 'coverage.json'))
E = lambda s: html.escape(str(s), quote=True)
LINES = FL['lines']; NET = TT['network']; SCHED = TT['schedule']; SL = {sl['id']: sl for sl in S['simutrans_lines']}
VD = S['vehicle_date']
aid = lambda s: 'line-' + s
sl_of = collections.defaultdict(list)
for s in SCHED: sl_of[s['records']].append(s['id'])

allunits = [u for o in LINES.values() for u in o]
units = [u for u in allunits if not u.get('spare')]
NSP = len(allunits) - len(units)
LW = PM['livery_words']
fam_liv = collections.defaultdict(set)                  # family -> liveries with an object (installed or requested)
for u in allunits:
    if u['pak']: fam_liv[u['pak']['family']].add(u['pak']['livery'])
for o in load(os.path.join(ASSETS, 'pak_objects.json'))['objects']:
    m = re.match(r'VZ-DPOlomouc-(.+?)-([a-z]+)-', o)
    if m: fam_liv[m.group(1)].add(m.group(2))

def pakcore(u):
    x = u['pak']
    if not x: return '<span class="pakmiss">no object</span>'
    c = E(x['core']) + (f' <span class="muted">{E(LW.get(x["livery"], x["livery"]))}</span>' if len(fam_liv[x['family']]) > 1 else '')
    if x['requested']: c += ' <span class="chip spare">no object yet</span>' if u.get('spare') else ' <span class="chip req">requested</span>'
    return c
def length(u): return f"{u['pak']['m']:g} m" if u['pak'] else '?'
def cell(u, dep=True):
    num = (f'<span class="dot dh"></span>' if dep else '') + f'<span class="veh" data-v="{E(u["car"])}">{E(u["car"])}</span>' + \
          (f' <span class="vd">· {E(u["depot"])}</span>' if dep else '')
    ty = E(u['type']) + f' <span class="muted">· {length(u)}</span>'
    return f'<div class="vb"><span class="vn">{num}</span><span class="vt">{ty}</span><span class="vp">{pakcore(u)}</span></div>'
def src(u):
    if u.get('designed'): return '<span class="chip des">designed</span>'
    if u['src'] == 'logged': return f'<span class="chip ok">logged</span>'
    return '<span class="chip spare">history</span>'

out = []; w = out.append
style = open(os.path.join(ASSETS, 'style.css.html'), encoding='utf-8').read()
w('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">')
w(re.sub(r'<title>.*?</title>', f"<title>{E(S['title'])}</title>", style))
w(open(os.path.join(ASSETS, 'extra.css.html'), encoding='utf-8').read())
w('<style>:root{--dh:#2b5f9e}@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--dh:#7fb0ea}}:root[data-theme="dark"]{--dh:#7fb0ea}'
  '.dot.dh{background:var(--dh)}.chip.des{background:var(--warn-soft);color:var(--warn)}td.src{white-space:nowrap}'
  'body{overflow-x:hidden}.cov td.n b{color:var(--accent)}</style></head><body>')
nlog = sum(1 for u in units if u['src'] == 'logged'); ndes = sum(1 for u in units if u.get('designed'))
w(f'''<header class="top"><div class="intro"><div class="eyebrow">{E(X['eyebrow'])}</div>
<h1>{E(S['title'])}</h1>
<p class="lede">{X['lede']}</p></div>
<div class="stats"><div class="stat"><b>{len(sl_of)}</b><span>bus lines</span></div><div class="stat"><b>{len(SCHED)}</b><span>Simutrans lines</span></div><div class="stat"><b>{len(units)}</b><span>buses needed</span></div><div class="stat"><b>{nlog}</b><span>logged</span></div><div class="stat"><b>{ndes}</b><span>designed</span></div><div class="stat"><b>{NSP}</b><span>not needed</span></div></div></header>
''')
nav = [('day', 'Which day'), ('network', 'Network at 16:00'), ('schedule', 'Simutrans schedule'), ('lines', 'Buses by line'), ('pak', 'Pak128 objects'),
       ('depots', 'Depot'), ('termini', 'Termini at 16:00'), ('notcounted', 'Not counted'), ('method', 'Method')]
w('<div class="controls"><nav class="nav lines" aria-label="Lines"><span class="lab">Lines</span>'
  + ''.join(f'<a class="badge" href="#{aid(s["id"])}">{E(s["id"])}</a>' for s in SCHED) + '</nav>'
  + '<nav class="nav dnav" aria-label="Depot and sections"><span class="lab">Depot</span>'
  + f'<a href="#depot-dh">Dolní Hejčínská <b>{len(units)}</b></a>'
  + ''.join(f'<a href="#{i}">{E(t)}</a>' for i, t in nav) + '</nav>'
  + '<input type="search" id="q" placeholder="Find bus, e.g. 424" aria-label="Find vehicle number" inputmode="numeric"><span id="hits" aria-live="polite"></span></div>')

# ---- which day -------------------------------------------------------------------------------------------------------
w(f'<h2 id="day">Which day</h2><p class="sub">{X["day"]}</p>')
w('<div class="scroll"><table class="cov"><tr><th>Weekday</th><th>Bus records</th><th>Bus lines recorded</th><th>Tram sets</th></tr>')
for d, c in sorted(COV.items(), reverse=True):
    nb = sum(c['bus'].values())
    if not nb and not c['tram'] and d not in (VD, '2026-09-25'): continue
    lbl = E(nice(d)) + (' <span class="chip ok">used</span>' if d == VD else '')
    w(f'<tr><td>{lbl}</td><td class="n">{"<b>%d</b>" % nb if d == VD else nb}</td><td class="note">{" ".join(f"{E(k)} ({v})" for k, v in c["bus"].items()) or "–"}</td><td class="n">{c["tram"]}</td></tr>')
w('</table></div><p class="sub" style="margin-top:8px">Weekdays of September 2026 with at least one record (seznam-autobusu.cz day overviews, MHD Olomouc). Records carry no time of day and no kurz for DPMO buses.</p>')

# ---- network ---------------------------------------------------------------------------------------------------------
w(f'<h2 id="network">Network at 16:00</h2><p class="sub">{X["network"]}</p>')
w('<div class="scroll"><table><tr><th>Line</th><th>From</th><th>To</th><th>Trips 15–18</th><th>Every</th><th>Leaves at (16:xx)</th><th>Runtime</th><th>Simutrans line</th></tr>')
for l in sorted(NET, key=int):
    if l not in sl_of: continue
    t = [x for x in NET[l]['rows'] if not x['depot']]
    for i, x in enumerate(t):
        w('<tr>')
        if i == 0: w(f'<td rowspan="{len(t)}"><span class="badge">{E(l)}</span></td>')
        w(f'<td>{E(x["o"])}</td><td>{E(x["d"])}</td><td class="n">{x["n3h"]}</td><td class="n">{("%g min" % x["hw"]) if x["hw"] else "–"}</td><td class="mins">{" ".join(mm(m) for m in x["m16"]) or "–"}</td><td class="n">{x["run"]} min</td>')
        if i == 0:
            w(f'<td rowspan="{len(t)}">' + ' '.join(f'<a href="#{aid(s)}"><span class="badge sm">{E(s)}</span></a>' for s in sl_of[l]) + '</td>')
        w('</tr>')
w('</table></div>')
nopeak = [l for l in sorted(NET, key=int) if l not in sl_of]
w('<p class="sub" style="margin-top:12px"><b>Not in the afternoon peak.</b> ' + '; '.join(
    f'{E(l)} ({E(S["not_peak"].get(l, "no departure 16:00–16:59"))}; {NET[l]["trips"]} trips, {hm(NET[l]["first"])}–{hm(NET[l]["last"])})' for l in nopeak) + '.</p>')
nm_ = [x for x in TT['not_modelled']]
if nm_:
    w('<p class="sub"><b>Not modelled</b> (15:00–18:00; short workings, garage runs and odd variants with fewer than 3 trips; their buses are counted by the on-the-road rule): '
      + '; '.join(f'{E(x["line"])} {E(x["o"])} → {E(x["d"])} ({x["n"]}{", garage" if x["depot"] else ""})' for x in nm_) + '.</p>')

def match(r):
    a_, b_ = r['span'].split('–')
    if r['exact'] and a_ == b_:   # one departure in the hour, no repeating run (method check 25 Oct 2026: it read "exact 16:38–16:38")
        oth = [hm(x) for x in r['deps'] if hm(x) != a_]
        return (f'<span class="chip warn">single</span> hourly at the only 16:xx departure ({a_}); no repeating pattern'
                + (f'; other real departures 15:00–17:59: {" ".join(oth)}' if oth else ''))
    if r['exact']: return f'<span class="chip ok">exact</span> {r["span"]}'
    t = (f'<span class="chip">set by hand</span> exact {r["span"]}; ' if r.get('override') else '') +         f'<span class="chip warn">partial</span> real 16:xx {" ".join(mm(m) for m in r["hour"]) or "none"}'
    if r['missing']: t += f'; not modelled: {" ".join(mm(m) for m in r["missing"])} (the other end runs fewer buses an hour)'
    if r['extra']: t += f'; added: {" ".join(mm(m) for m in r["extra"])} (not in the timetable)'
    return t

# ---- schedule --------------------------------------------------------------------------------------------------------
w(f'<h2 id="schedule">Simutrans schedule</h2><p class="sub">{X["schedule"]}</p>')
w('<div class="scroll"><table class="sched"><tr><th>Line</th><th>Stop entry</th><th>Departure every</th><th>Offset</th><th>Also at</th><th>Stop type</th><th>Leave up to</th><th>Per hour</th><th>Matches real timetable</th><th>Buses</th></tr>')
for s in SCHED:
    n = len(s['rows']); ne = s['need']
    for i, r in enumerate(s['rows']):
        w('<tr>')
        if i == 0:
            nm2 = s['name'].split(' ', 1)[1]
            w(f'<td rowspan="{n}" class="sl"><a href="#{aid(s["id"])}"><span class="badge">{E(s["id"])}</span></a><small>{E(nm2)}</small></td>')
        mg = ''.join(f'<br><span class="muted">+ {E(x[0])} → {E(x[1])}</span>' for x in r['merged'])
        lbl = f'<b>{E(r["stop"])}</b><br><span class="muted">to {E(r["to"])}</span>{mg}'
        real = f'<small class="real">real {r["real"][0]}' + (f'; {",".join(map(str, r["real"][1:]))}' if r['real'][1:] else '') + '</small>' if r['loop'] else ''
        term = '<span class="chip loop">turn −1 min</span>' if r['loop'] else '<span class="chip">through stop</span><br><small class="muted">real minute</small>'
        if 60 % r['every']: term += f'<br><small class="muted">offsets count from 01:00: typed = (real − 60{" − 1" if r["loop"] else ""}) mod {r["every"]}</small>'   # fork rule, fixed 25 Oct 2026
        w(f'<td>{lbl}</td><td class="big">{r["every"]}</td><td class="big">{r["set"][0]}{real}</td><td class="big">{",".join(map(str, r["set"][1:])) or "–"}</td><td>{term}</td><td class="muted">auto</td><td class="n">{round(r["perh"], 2):g}</td><td class="note">{match(r)}</td>')
        if i == 0:
            nn = sum(1 for u in LINES[s['id']] if not u.get('spare'))
            w(f'<td rowspan="{n}" class="note"><b>{ne["vehicles"]}</b> needed<br>{ne["cycle"]} by timetable cycle' + (f' ({ne["minutes"]} min)' if ne['minutes'] else ' (no complete round trip near 16:00)')
              + (f'<br>+{ne["onroad_extra"]} for the most buses on the road at once' if ne.get('onroad_extra') else '')
              + f'<br><b>{nn}</b> assigned</td>')
        w('</tr>')
    txt = SL[s['id']].get('note') or ''
    if txt: w(f'<tr><td></td><td colspan="9" class="note">{E(txt)}</td></tr>')
w('</table></div>')
w(f'<p class="sub" style="margin-top:12px">{X["need"]}</p>')

# ---- buses by line -----------------------------------------------------------------------------------------------------
w(f'<h2 id="lines">Buses by line</h2><p class="sub">{X["lines"]}</p><div class="grid">')
for s in SCHED:
    o = sorted(LINES[s['id']], key=lambda u: (bool(u.get('spare')), u['src'] == 'history', bool(u.get('designed')), u['kurz'], int(u['car'])))
    oc = [u for u in o if not u.get('spare')]
    mix = collections.Counter(u['type'] for u in oc)
    w(f'<article class="card" id="{aid(s["id"])}"><header><span class="badge">{E(s["id"])}</span><div class="t"><h3>{E(s["name"].split(" ", 1)[1])}</h3><div class="chips">')
    for k, c in mix.most_common(): w(f'<span class="tchip"><b>{c}×</b> {E(k)}</span>')
    w(f'</div></div><div class="count"><b>{len(oc)}</b><span>buses</span></div></header>')
    txt = SL[s['id']].get('text')
    if txt: w(f'<p class="pooltext"><span class="chip">{E(SL[s["id"]].get("chip", "note"))}</span> {E(txt)}</p>')
    nl = sum(1 for u in o if u['src'] == 'logged'); nd = sum(1 for u in oc if u.get('designed'))
    w(f'<p class="pooltext">{s["need"]["vehicles"]} needed · {nl} logged on {E(nice(VD))}' + (f' · {nd} designed from the line history' if nd else '') + '</p>')
    w('<div class="scroll flat"><table><tr><th>Source</th><th>Bus · depot / type / pak object</th><th>Note</th></tr>')
    for u in o:
        sp = u.get('spare')
        note = u['note'] if u['src'] != 'logged' else (u['note'] or 'Logged on the line (no time of day recorded).')
        if sp and u['src'] == 'logged': note = 'Logged, not needed: ' + u['spare_why'] + '.'
        w(f'<tr{" class=\"spare\"" if sp else ""}><td class="src">{src(u)}</td><td>{cell(u)}</td><td class="note">' + ('<span class="chip spare">not needed</span> ' if sp else '') + f'{E(note)}</td></tr>')
    w('</table></div></article>')
w('</div>')

# ---- pak --------------------------------------------------------------------------------------------------------------------
req = load(os.path.join(DER, S['name'], 'pak_request.json'))['requests']
w(f'<h2 id="pak">Pak128 objects</h2><p class="sub">{X["pak"]}</p>')
w('<div class="scroll"><table><tr><th>Type</th><th>Length</th><th>Livery (object)</th><th>Pak core</th><th>Buses in the peak</th><th>Real paint (buses)</th><th>Pak128 objects, in order</th><th>Car units</th><th>Status</th></tr>')
keyf = lambda u: (u['type'], u['pak']['livery'] if u['pak'] else '')
for (t, liv), k in sorted(collections.Counter(keyf(u) for u in units).items(), key=lambda kv: (kv[0][0], -kv[1])):
    us = [u for u in units if keyf(u) == (t, liv)]; x = us[0]['pak']
    pt = collections.Counter(u['paint'] or 'not recorded' for u in us)
    pttxt = '<br>'.join(f'{n}× {E(v)}' for v, n in pt.most_common())
    objs = '<br>'.join(f'<span class="pak">{E(o)}</span>' for o in x['objs'])
    stt = '<span class="chip req">requested</span>' if x['requested'] else '<span class="chip ok">installed</span>'
    w(f'<tr><td><b>{E(t)}</b><br><span class="muted">DPMO</span></td><td class="n">{x["m"]:g} m</td><td>{E(LW.get(liv, liv))}</td><td class="vp big2">{pakcore(us[0]).replace(" <span class=\"chip req\">requested</span>", "")}</td><td class="n">{k}</td><td class="note">{pttxt}</td><td>{objs}</td><td class="n">{x["len"]}</td><td class="note">{stt} {E(x["note"])}</td></tr>')
w('</table></div>')
if req:
    w('<p class="sub" style="margin-top:12px"><b>Requested from the pak session:</b> ' + '; '.join(
        f'{E(r["objs"][0])} for {E(r["type"])} {", ".join(r["cars"])} ({E(", ".join(r["paint"]))})' for r in req) + '. The sheet shows these objects as they will be named; nothing stands in for them.</p>')

# ---- depot ------------------------------------------------------------------------------------------------------------------
w(f'<h2 id="depots">Depot</h2><p class="sub">{X["depot"]}</p><div class="depots">')
tm = collections.Counter(u['type'] for u in units)
w(f'<article class="card depot" id="depot-dh"><header><div class="t"><h3><span class="dot big dh"></span>Garáže Dolní Hejčínská</h3><small>every DPMO bus</small></div><div class="count"><b>{len(units)}</b><span>buses out</span></div></header>')
w('<div class="mix">' + ''.join(f'<span><b>{k}</b> {E(t)}</span>' for t, k in tm.most_common()) + '</div>')
for s in SCHED:
    v = sorted([u for u in LINES[s['id']] if not u.get('spare')], key=lambda u: int(u['car']))
    if not v: continue
    w(f'<div class="dline"><div class="lhead"><span class="badge">{E(s["id"])}</span><small>{len(v)} bus{"es" if len(v) != 1 else ""}</small></div><div class="scroll flat"><table class="dt"><tr><th>Source</th><th>Bus · type · pak object</th></tr>')
    for u in v: w(f'<tr><td class="src">{src(u)}</td><td>{cell(u, dep=False)}</td></tr>')
    w('</table></div></div>')
w('</article></div>')

# ---- termini ------------------------------------------------------------------------------------------------------------------
w('<h2 id="termini">Termini at 16:00</h2><p class="sub">Every point buses of the peak lines leave from between 16:00 and 16:59, busiest first (garage runs left out).</p>')
dep16 = collections.defaultdict(list)
for l in sorted(NET, key=int):
    if l not in sl_of: continue
    for x in NET[l]['rows']:
        if x['m16'] and not x['depot']: dep16[x['o']].append((l, x))
w('<div class="scroll"><table><tr><th>Stop</th><th>Departures 16:00–16:59</th></tr>')
for st in sorted(dep16, key=lambda n: (-sum(len(x['m16']) for l, x in dep16[n]), n)):
    deps = '<br>'.join(f'<span class="badge sm">{E(l)}</span> to {E(x["d"])} <span class="mins">{" ".join(mm(v) for v in x["m16"])}</span>' for l, x in dep16[st])
    w(f'<tr><td><b>{E(st)}</b></td><td>{deps}</td></tr>')
w('</table></div>')

# ---- not counted ----------------------------------------------------------------------------------------------------------------
w(f'<h2 id="notcounted">Not counted</h2><p class="sub">{X["notcounted"]}</p><div class="scroll"><table><tr><th>Line</th><th>Bus · type · pak object</th><th>Why</th></tr>')
for s in SCHED:
    for u in sorted([u for u in LINES[s['id']] if u.get('spare')], key=lambda u: (u['src'] != 'logged', int(u['car']))):
        why = ('Logged, not needed: ' + u['spare_why']) if u['src'] == 'logged' else u['note']
        w(f'<tr class="spare"><td><span class="badge sm">{E(s["id"])}</span></td><td>{cell(u)}</td><td class="note">{E(why)}</td></tr>')
w('</table></div>')

# ---- method --------------------------------------------------------------------------------------------------------------------
w(f'<h2 id="method">Method and sources</h2><div class="notes">' + ''.join(f'<p>{t}</p>' for t in X['method']) + '</div>')
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
</script></body></html>''')
dest = os.path.join(PROJECT, S['output'])
open(dest, 'w', encoding='utf-8').write(''.join(out))
print('rendered', dest, len(units), 'buses,', NSP, 'not needed')
