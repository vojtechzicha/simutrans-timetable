"""Render the Pardubice sheet for one state into the project root.

  python 05_render.py --state 2026-09-29

The page is the Brno bus / trolleybus sheet's (style from pipeline/brno/assets/style.css.html, the sticky bar and marks
from pipeline/brno-trolleybus/assets/extra.css.html) plus assets/page_extra.css.html (mode colours: trolleybus blue,
bus red). Sections: network at 16:00, Simutrans schedule, vehicles by line (trolleybus and bus groups), pak128 objects,
depot, and the reference kept from the old per-line sheet (battery sections, stops and their lines, termini, specials and
closures, lines left out), then "Not counted" and the method.
"""
import argparse, collections, datetime, html, os, re
from common import ASSETS, PROJECT, BRNO_STYLE, BRNO_EXTRA, state, load, der, mm, hm

ap = argparse.ArgumentParser(); ap.add_argument('--state', required=True); S = state(ap.parse_args().state)
X = S['texts']
NET = load(der(S, 'network.json')); FL = load(der(S, 'fleet.json'))
PM = load(os.path.join(ASSETS, 'pak_map.json')); INST = load(os.path.join(ASSETS, 'pak_installed.json'))
REF = load(os.path.join(ASSETS, 'reference.json'))
SIM = NET['simutrans']; LINES = FL['lines']; DL = NET['lines']
E = lambda s: html.escape(str(s), quote=True)
aid = lambda s: 'line-' + s
GRP = {'trolleybus': 'tb', 'bus': 'bus'}
DEPOT_NAME = S['depot_names']

def nice(d):
    x = datetime.date.fromisoformat(d); return f"{x.strftime('%a')} {x.day} {x.strftime('%b')} {x.year}"
def badge(sid, grp, sm=False, link=True):
    b = f'<span class="badge {GRP[grp]}{" sm" if sm else ""}">{E(sid)}</span>'
    return f'<a href="#{aid(sid)}">{b}</a>' if link else b
sgrp = {s['id']: s['group'] for s in SIM}
lgrp = {L: v['group'] for L, v in DL.items()}

# pak: types with more than one livery object (installed + requested on this sheet) show the livery in the core
allunits = [u for us in LINES.values() for u in us]
objs = set(INST['objects']) | {u['pak']['obj'] for u in allunits if u['pak'].get('obj')}
livs = collections.defaultdict(set)
for o in objs:
    m = re.match(r'VZ-DPPardubice-(.+?)-([a-z]+)-(.+)$', o)
    if m: livs[(m.group(1), m.group(3))].add(m.group(2))
def pakcore(u):
    p = u['pak']
    if not p.get('obj'): return '<span class="pakmiss">no object</span>'
    t = PM['types'][u['type']]
    c = E(p['core']) + (f' <span class="muted">({E(PM["liveries"].get(p["livery"], p["livery"]))})</span>' if len(livs[(t['token'], p['core'])]) > 1 else '')
    return c + (' <span class="chip req">requested</span>' if p['status'] == 'requested' else '')
def length(u):
    return f"{u['pak']['m']:g} m" if u['pak'].get('m') else '?'
def cell(u, dep=True):
    num = (f'<span class="dot dk"></span>' if dep else '') + f'<span class="veh" data-v="{E(u["num"])}">{E(u["num"])}</span>' + \
          (f' <span class="vd">· {E(DEPOT_NAME.get(u["depot"], u["depot"]))}</span>' if dep else '')
    marks = (' <span class="batmark">traction battery</span>' if u['battery'] else '') + \
            (' <span class="chip des">designed</span>' if u.get('designed') and not u.get('spare') else '') + \
            (' <span class="chip bus">bus</span>' if u.get('sub') else '')
    ty = E(u['pak'].get('full') or u['type']) + f' <span class="muted">· {length(u)}</span>' + marks
    return f'<div class="vb"><span class="vn">{num}</span><span class="vt">{ty}</span><span class="vp">{pakcore(u)}</span></div>'
units = [u for u in allunits if not u.get('spare')]
NSP = len(allunits) - len(units)
ndes = sum(1 for u in units if u.get('designed'))
mode_n = collections.Counter(u['mode'] for u in units)

out = []; w = out.append
style = open(BRNO_STYLE, encoding='utf-8').read()
w(re.sub(r'<title>.*?</title>', f"<title>{E(S['title'])}</title>", style))
w(open(BRNO_EXTRA, encoding='utf-8').read())
w(open(os.path.join(ASSETS, 'page_extra.css.html'), encoding='utf-8').read())
nav = [('network', 'Network at 16:00'), ('schedule', 'Simutrans schedule'), ('lines', 'Vehicles by line'), ('pak', 'Pak128 objects'),
       ('depots', 'Depot'), ('battery', 'Battery sections'), ('stops', 'Stops and lines'), ('termini', 'Termini'),
       ('specials', 'Specials and closures'), ('excluded', 'Not counted'), ('method', 'Method')]
w(f'''<header class="top"><div class="intro"><div class="eyebrow">{E(X['eyebrow'])}</div>
<h1>{E(S['title'])}</h1>
<p class="lede">{X['lede']}</p></div>
<div class="stats"><div class="stat"><b>{len(DL)}</b><span>DPMP lines</span></div><div class="stat"><b>{len(SIM)}</b><span>Simutrans lines</span></div><div class="stat"><b>{len(units)}</b><span>vehicles at 16:00</span></div><div class="stat"><b>{mode_n['trolleybus']}</b><span>trolleybuses</span></div><div class="stat"><b>{mode_n['bus']}</b><span>buses</span></div><div class="stat"><b>{ndes}</b><span>designed</span></div><div class="stat"><b>{NSP}</b><span>not needed</span></div></div></header>
''')
dep_n = collections.Counter(u['depot'] for u in units)
w('<div class="controls"><nav class="nav lines" aria-label="Lines"><span class="lab">Lines</span>'
  + ''.join(f'<a class="badge {GRP[s["group"]]}" href="#{aid(s["id"])}">{E(s["id"])}</a>' for s in SIM) + '</nav>'
  + '<nav class="nav dnav" aria-label="Depot and sections"><span class="lab">Depot</span>'
  + ''.join(f'<a href="#depot-{E(d)}">{E(DEPOT_NAME.get(d, d))} <b>{n}</b></a>' for d, n in dep_n.most_common())
  + ''.join(f'<a href="#{i}">{E(t)}</a>' for i, t in nav) + '</nav>'
  + '<input type="search" id="q" placeholder="Find vehicle, e.g. 478" aria-label="Find vehicle number" inputmode="numeric"><span id="hits" aria-live="polite"></span></div>')

# ---- network --------------------------------------------------------------------------------------------------------
w(f'<h2 id="network">Network at 16:00</h2><p class="sub">{X["network"]}</p>')
w('<p class="legend"><span><span class="badge tb sm">1</span> trolleybus line</span><span><span class="badge bus sm">6</span> bus line</span>'
  '<span><span class="batmark">traction battery</span> a trolleybus that can run off the wire</span><span><span class="chip des">designed</span> not recorded on the day, a real car from the line’s history</span>'
  '<span><span class="chip spare">not needed</span> surplus, not counted</span></p>')
w('<div class="scroll"><table><tr><th>Line</th><th>From</th><th>To</th><th>Trips</th><th>Every</th><th>Leaves at (reference hour)</th><th>Runtime</th><th>Simutrans line</th></tr>')
for grp in S['groups']:
    w(f'<tr class="subhead"><td colspan="8">{"Trolleybus lines" if grp == "trolleybus" else "Bus lines"}</td></tr>')
    for L in S['groups'][grp]:
        d = DL[L]; V = [v for v in d['variants'] if not v['depot']]
        sims = {s['id']: s for s in SIM if s['line'] == L}
        pairs = {frozenset((s['a'], s['b'])): sid for sid, s in sims.items()}
        for i, v in enumerate(V):
            w('<tr>')
            if i == 0:
                note = '' if d['t0'] == S['t0'] else f'<br><small class="muted">reference {hm(d["t0"])}</small>'
                w(f'<td rowspan="{len(V)}">{badge(L, grp, link=False)}{note}</td>')
            sid = pairs.get(frozenset((v['o'], v['d'])))
            cellsl = badge(sid, grp, sm=True) if sid else '<span class="muted">merged, not a line of its own</span>'
            w(f'<td>{E(v["o"])}</td><td>{E(v["d"])}</td><td class="n">{v["n"]}</td><td class="n">{("%g min" % v["hw"]) if v["hw"] else "–"}</td>'
              f'<td class="mins">{" ".join(mm(x) for x in v["m16"]) or "–"}</td><td class="n">{v["run"]} min</td><td>{cellsl}</td></tr>')
w('</table></div>')
w(f'<p class="sub" style="margin-top:12px">{X["network_after"]}</p>')

# ---- schedule -------------------------------------------------------------------------------------------------------
def match(r):
    if r['how'] == 'daily':
        return '<span class="chip ok">exact all day</span> every departure of the day (at most 8), as Offset + Also at of a 1440-minute interval'
    if r['how'] == 'hour':
        t = '<span class="chip warn">16:00 hour</span> the reference hour’s own minutes, repeated hourly'
        return t + (f'; off by up to {r["dev"]} min elsewhere in {r["window"][0]}–{r["window"][1]}' if r['dev'] else '')
    if r['exact']:
        return f'<span class="chip ok">exact</span> {r["span"]}' + (f'; up to {r["dev"]} min off outside it ({r["window"][0]}–{r["window"][1]})' if r['dev'] else '')
    t = f'<span class="chip warn">partial</span> exact {r["span"]}; reference hour real {" ".join(mm(x) for x in r["hour"]) or "none"}'
    if r['missing']: t += f'; not modelled {" ".join(mm(x) for x in r["missing"])}'
    if r['extra']: t += f'; added {" ".join(mm(x) for x in r["extra"])}'
    return t
w(f'<h2 id="schedule">Simutrans schedule</h2><p class="sub">{X["schedule"]}</p>')
w('<div class="scroll"><table class="sched"><tr><th>Line</th><th>Stop entry</th><th>Departure every</th><th>Offset</th><th>Also at</th><th>Leave up to</th><th>Per hour</th><th>Matches real timetable</th><th>Vehicles</th></tr>')
for grp in S['groups']:
    w(f'<tr class="subhead"><td colspan="9">{"Trolleybus lines" if grp == "trolleybus" else "Bus lines"}</td></tr>')
    for s in [x for x in SIM if x['group'] == grp]:
        n = len(s['rows'])
        for i, r in enumerate(s['rows']):
            w('<tr>')
            if i == 0: w(f'<td rowspan="{n}" class="sl">{badge(s["id"], grp)}<small>{E(s["name"])}</small></td>')
            lbl = f'<b>{E(r["stop"])}</b><br><span class="muted">to {E(r["to"])}</span><br><span class="chip loop">turn −1 min</span>'
            if not r.get('every'):
                w(f'<td>{lbl}</td><td class="big">0</td><td class="big">–</td><td class="big">–</td><td class="muted">–</td><td class="n">–</td><td class="note">No pattern: real departures {" ".join(r["deps"])}</td>')
            else:
                real = f'<small class="real">real {", ".join(hm(x) if r["every"] == 1440 else str(x) for x in r["real"][:1])}' + (f'; {", ".join(hm(x) if r["every"] == 1440 else str(x) for x in r["real"][1:])}' if r['real'][1:] else '') + '</small>'
                setv = r['set']; daily = r['every'] == 1440
                if daily:      # minutes from midnight: show the clock time under each value
                    also = ' '.join(f'<span class="dv">{x}<small class="real">{hm(x + 1)} real</small></span>' for x in setv[1:]) or '–'
                    real = f'<small class="real">{hm(r["real"][0])} real</small>'
                else:
                    also = ', '.join(map(str, setv[1:])) or '–'
                w(f'<td>{lbl}</td><td class="big">{r["every"]}</td><td class="big">{setv[0]}{real}</td><td class="big{" wrapv" if daily else ""}">{also}</td><td class="muted">auto</td>'
                  f'<td class="n">{("%g" % r["perh"]) if r.get("perh") is not None else "–"}</td><td class="note">{match(r)}'
                  + (f'<br><span class="muted">merged minutes of other patterns from this stop: {" ".join(r["merged"])}</span>' if r.get('merged') else '') + '</td>')
            if i == 0:
                us = LINES.get(s['id'], []); nn = sum(1 for u in us if not u.get('spare')); nd = sum(1 for u in us if u.get('designed') and not u.get('spare'))
                how = {'round trip': 'by timetable cycle', 'loop round trip': 'by timetable cycle (loop)'}.get(s['how'], s['how'])
                w(f'<td rowspan="{n}" class="note"><b>{s["need"]}</b> needed ' + E(how) + (f' ({s["cycle"]} min)' if s.get('cycle') else '')
                  + (f', incl. +{s["onroad_extra"]} for the most on the road at once' if s.get('onroad_extra') else '')
                  + (', at least 1 for a thin line' if s.get('min_one') else '')
                  + f'<br><b>{nn - nd}</b> logged' + (f' + <b>{nd}</b> designed' if nd else '')
                  + (f', {sum(1 for u in us if u.get("spare"))} not needed' if any(u.get('spare') for u in us) else '') + '</td>')
            w('</tr>')
w('</table></div>')
w(f'<p class="sub" style="margin-top:12px">{X["schedule_after"]}</p>')

# ---- vehicles by line -------------------------------------------------------------------------------------------------
w(f'<h2 id="lines">Vehicles by line</h2><p class="sub">{X["lines"]}</p>')
groups_of = collections.defaultdict(list)
for s in SIM: groups_of[S.get('records_of', {}).get(s['line'], s['line'])].append(s['id'])
for grp in S['groups']:
    w(f'<h3 class="grouphead">{"Trolleybus lines" if grp == "trolleybus" else "Bus lines"}</h3><div class="grid">')
    for s in [x for x in SIM if x['group'] == grp]:
        us = sorted(LINES.get(s['id'], []), key=lambda u: (bool(u.get('spare')), u['kurz'] is None, u['kurz'] or 0, u['num']))
        uc = [u for u in us if not u.get('spare')]
        mix = collections.Counter(PM['types'][u['type']]['full'] for u in uc)
        w(f'<article class="card" id="{aid(s["id"])}"><header>{badge(s["id"], grp, link=False)}<div class="t"><h3>{E(s["name"])}</h3><div class="chips">')
        for k, c in mix.most_common(): w(f'<span class="tchip"><b>{c}×</b> {E(k)}</span>')
        w(f'</div></div><div class="count"><b>{len(uc)}</b><span>{"trolleybuses" if grp == "trolleybus" else "buses"}</span></div></header>')
        ref = REF['lines'].get(s['line'], {})
        if s['main'] and ref.get('note'): w(f'<p class="pooltext">{ref["note"]}</p>')
        if s['id'] in S['battery_required']:
            w(f'<p class="pooltext"><span class="chip bat">battery</span> {E(S["battery_required"][s["id"]])}: only trolleybuses with a traction battery run this line.</p>')
        R = S.get('records_of', {}).get(s['line'])
        if R:
            w(f'<p class="pooltext"><span class="chip pool">pool</span> {E(S["pool_text"][s["line"]])}</p>')
        elif len([x for x in groups_of[s['line']]]) > 1:
            sibs = groups_of[s['line']]
            w(f'<p class="pooltext"><span class="chip">split, a choice</span> DPMP records line {E(s["line"])} as one set of kurzy, shared here between Simutrans lines {", ".join(sibs)} by timetable need'
              + (' (battery cars to the battery line first)' if any(x in S['battery_required'] for x in sibs) else '') + '. The records do not say which branch a kurz ran.</p>')
        nsp = len(us) - len(uc); nlog = sum(1 for u in us if not u.get('designed')); nd = sum(1 for u in uc if u.get('designed'))
        if nd:
            w(f'<p class="pooltext"><span class="chip des">designed</span> {nlog} logged against {s["need"]} needed. {nd} designed, not recorded: real cars from the line’s history that were not out anywhere on {E(nice(S["vehicles_date"]))}. {E(S.get("short_text", {}).get(s["id"], ""))}</p>')
        if nsp:
            nlog_sp = sum(1 for u in us if u.get('spare') and not u.get('designed'))
            if nlog_sp: w(f'<p class="pooltext"><span class="chip spare">not needed</span> {len([u for u in us if not u.get("designed")])} logged against {s["need"]} needed; {nlog_sp} marked not needed, keeping every type of the line among the counted vehicles and dropping afternoon-only kurzy, then the highest kurz numbers, first.</p>')
            if nsp - nlog_sp: w(f'<p class="pooltext"><span class="chip spare">not needed</span> {nsp - nlog_sp} more free cars of the line’s history, not used.</p>')
        w('<div class="scroll flat"><table><tr><th>Kurz</th><th>Vehicle · depot / type / pak object</th><th>Note</th></tr>')
        for u in us:
            sp = u.get('spare')
            k = f'{E(u["rec"])}/{u["kurz"]}' if u['kurz'] is not None else '–'
            if u.get('designed'):
                note = ('<span class="chip spare">not needed</span> ' if sp else '<b>designed, not recorded.</b> ') + E(u['why'])
            else:
                note = ('<span class="chip spare">not needed</span> ' if sp else '') + E(u['note'])
            w(f'<tr{" class=\"spare\"" if sp else ""}><td class="n">{k}</td><td>{cell(u)}</td><td class="note">{note}</td></tr>')
        if not us: w('<tr><td colspan="3" class="note">no vehicle</td></tr>')
        w('</table></div></article>')
    w('</div>')

# ---- pak -------------------------------------------------------------------------------------------------------------
w(f'<h2 id="pak">Pak128 objects</h2><p class="sub">{X["pak"]} Read from the pak checkout at {E(INST["commit"])}.</p>')
w('<div class="scroll"><table><tr><th>Type · livery</th><th>Length</th><th>Pak core</th><th>Vehicles at 16:00</th><th>Real paint (vehicles)</th><th>Pak128 object</th><th>Car units</th><th>Status</th></tr>')
key = lambda u: (u['pak']['obj'], u['type'])
for (obj, t), us in sorted(collections.defaultdict(list, {k: [u for u in units if key(u) == k] for k in {key(u) for u in units}}).items(), key=lambda kv: (PM['types'][kv[0][1]]['mode'] != 'trolleybus', -len(kv[1]), kv[0][0])):
    ex = us[0]; p = ex['pak']
    pc = collections.Counter(u['paint'] or 'not recorded' for u in us)
    ptxt = '<br>'.join(f'{k}× {E(v)}' for v, k in pc.most_common(4)) + (f'<br>{sum(pc.values()) - sum(k for _, k in pc.most_common(4))}× other advert wraps' if len(pc) > 4 else '')
    st = '<span class="chip req">requested</span>' if p['status'] == 'requested' else '<span class="chip ok">installed</span>'
    w(f'<tr><td class="ty"><b>{E(p["full"])}</b><br><span class="muted">{E(PM["liveries"].get(p["livery"], p["livery"]))} · {E(p["package"])}</span></td><td class="n">{length(ex)}</td><td class="vp big2">{pakcore(ex)}</td>'
      f'<td><span class="n">{len(us)}</span><span class="nums">{" ".join(sorted((u["num"] for u in us), key=int))}</span></td><td class="note">{ptxt}</td><td><span class="pak">{E(obj)}</span></td><td class="n">{p["len"]}</td>'
      f'<td class="note">{st} {E(PM["types"][t].get("note", ""))}</td></tr>')
w('</table></div>')
w(f'<p class="sub" style="margin-top:12px">{X["pak_after"]}</p>')

# ---- depot -----------------------------------------------------------------------------------------------------------
w(f'<h2 id="depots">Depot</h2><p class="sub">{X["depot"]}</p><div class="depots">')
for dep, nv in dep_n.most_common():
    tm = collections.Counter(PM['types'][u['type']]['full'] for u in units if u['depot'] == dep)
    w(f'<article class="card depot" id="depot-{E(dep)}" data-depot="{E(dep)}"><header><div class="t"><h3><span class="dot big dk"></span>{E(DEPOT_NAME.get(dep, dep))}</h3><small>every DPMP trolleybus and bus</small></div><div class="count"><b>{nv}</b><span>vehicles at 16:00</span></div></header>')
    w('<div class="mix">' + ''.join(f'<span><b>{k}</b> {E(t)}</span>' for t, k in tm.most_common()) + '</div>')
    for s in SIM:
        v = [u for u in LINES.get(s['id'], []) if u['depot'] == dep and not u.get('spare')]
        if not v: continue
        v.sort(key=lambda u: (u['kurz'] is None, u['kurz'] or 0))
        w(f'<div class="dline"><div class="lhead">{badge(s["id"], s["group"])}<small>{len(v)}</small></div><div class="scroll flat"><table class="dt"><tr><th>Kurz</th><th>Vehicle · type · pak object</th></tr>')
        for u in v: w(f'<tr><td class="n">{E(u["rec"]) + "/" + str(u["kurz"]) if u["kurz"] is not None else "designed"}</td><td>{cell(u, dep=False)}</td></tr>')
        w('</table></div></div>')
    w('</article>')
w('</div>')

# ---- battery sections (reference) -------------------------------------------------------------------------------------
w(f'<h2 id="battery">Battery sections</h2><p class="sub">{X["battery"]}</p><div class="batgrid">')
for L, sec in S['battery_sections'].items():
    sids = [s['id'] for s in SIM if s['line'] == L]
    req = [x for x in sids if x in S['battery_required']]
    cars = [u for x in req for u in LINES.get(x, []) if not u.get('spare')]
    w(f'<article class="batcard" id="bat-{E(L)}"><h3>{badge(L, lgrp[L], link=False)} <span class="sec">{E(sec["section"])}</span></h3><p>{sec["detail"]}</p>'
      + (f'<p><b>Simutrans:</b> {" ".join(badge(x, sgrp[x], sm=True) for x in req)} need battery cars: ' + ', '.join(f'<span class="veh" data-v="{E(u["num"])}">{E(u["num"])}</span> {E(PM["types"][u["type"]]["full"])}' for u in cars) + '.</p>' if req else '<p class="muted">No Simutrans line of this DPMP line leaves the wire in the model (the off-wire trips are merged or outside the reference hour).</p>')
      + '</article>')
w('</div>')
w(f'<p class="sub">{X["battery_after"]}</p>')

# ---- stops and lines (reference) ------------------------------------------------------------------------------------------
w(f'<h2 id="stops">Stops and their lines</h2><p class="sub">{X["stops"]}</p><div class="scroll"><table><tr><th>Stop</th><th>Lines</th><th>Trips 15:00–17:59 towards</th></tr>')
for st in sorted(NET['stops'], key=lambda x: x.lower()):
    ls = NET['stops'][st]
    order = [L for g in S['groups'].values() for L in g if L in ls]
    w(f'<tr><td><b>{E(st)}</b></td><td>{" ".join(badge(L, lgrp[L], sm=True, link=False) for L in order)}</td><td class="note">'
      + '<br>'.join(f'{E(L)}: ' + ', '.join(f'{E(d)} {n}' for d, n in sorted(ls[L].items(), key=lambda x: -x[1])) for L in order) + '</td></tr>')
w('</table></div>')

# ---- termini (reference) -------------------------------------------------------------------------------------------------
w(f'<h2 id="termini">Termini</h2><p class="sub">{X["termini"]}</p><div class="scroll"><table><tr><th>Stop</th><th>Departures 15:00–17:59 (line: times)</th><th>Trips ending here</th></tr>')
for st in sorted(NET['termini'], key=lambda n: (-sum(len(x) for x in NET['termini'][n]['dep'].values()), n)):
    t = NET['termini'][st]; order = [L for g in S['groups'].values() for L in g if L in t['dep']]
    w(f'<tr><td><b>{E(st)}</b></td><td>' + '<br>'.join(f'{badge(L, lgrp[L], sm=True, link=False)} <span class="mins">{" ".join(t["dep"][L])}</span>' for L in order)
      + f'</td><td class="note">{", ".join(f"{E(L)}: {n}" for L, n in t["arr"].items()) or "–"}</td></tr>')
w('</table></div>')

# ---- specials (reference) --------------------------------------------------------------------------------------------------
w(f'<h2 id="specials">Specials, connections and closures</h2><p class="sub">{X["specials"]}</p><div class="batgrid">')
for sp in REF['specials']:
    tag = f' <span class="chip">{E(sp["tag"][1])}</span>' if sp.get('tag') else ''
    w(f'<article class="batcard"><h3>{E(sp["title"])}{tag}</h3><div class="chips">' + ' '.join(badge(L, lgrp[L], sm=True, link=False) if L in lgrp else f'<span class="badge sm off">{E(L)}</span>' for L in sp['lines']) + '</div>'
      + ''.join(f'<p>{b}</p>' for b in sp['body']) + '</article>')
w('</div>')

# ---- not counted ---------------------------------------------------------------------------------------------------------
V = load(der(S, 'vehicles.json'))
w(f'<h2 id="excluded">Not counted</h2><p class="sub">Records from {E(nice(S["vehicles_date"]))} left out of the afternoon count: morning duties, replaced cars and the night lines.</p>'
  '<div class="scroll"><table><tr><th>Kurz</th><th>Vehicle · type · pak object</th><th>Why</th></tr>')
for x in FL['excluded']:
    v = V.get(x['cid'], {})
    u = dict(num=x['num'], type=v.get('type', '?'), depot=v.get('depot', ''), battery=False, pak=dict(full=PM['types'].get(v.get('type'), {}).get('full', v.get('type')), m=PM['types'].get(v.get('type'), {}).get('m')))
    u['pak'].update(obj=None)
    w(f'<tr><td class="n">{E(x["line"])}/{E(x["kurz"])}</td><td><div class="vb"><span class="vn"><span class="veh">{E(u["num"])}</span> <span class="vd">· {E(DEPOT_NAME.get(u["depot"], u["depot"]))}</span></span><span class="vt">{E(u["pak"]["full"])} <span class="muted">· {length(u)}</span></span></div></td><td class="note">{E(x["why"])}</td></tr>')
w('</table></div>')
w(f'<p class="sub" style="margin-top:16px"><b>DPMP lines left out of the model</b> (earlier user decisions, kept):</p><div class="scroll"><table><tr><th>Line</th><th>Why</th></tr>')
for L, why in S['left_out'].items(): w(f'<tr><td><span class="badge sm off">{E(L)}</span></td><td class="note">{why}</td></tr>')
w('</table></div>')

# ---- method -------------------------------------------------------------------------------------------------------------
w(f'<h2 id="method">Method and sources</h2><div class="notes">' + ''.join(f'<p>{p}</p>' for p in X['method']) + '</div>')
w('''<script>
(function(){
  var c=document.querySelector('.controls'); function h(){document.documentElement.style.setProperty('--stick',(c.offsetHeight+8)+'px')} h(); addEventListener('resize',h);
  const q=document.getElementById('q'), hits=document.getElementById('hits');
  const all=[...document.querySelectorAll('.veh[data-v]')];
  q.addEventListener('input',()=>{
    const s=q.value.trim().replace(/\\s+/g,'');
    let first=null, n=0;
    for(const el of all){
      const on = s.length>=2 && el.offsetParent!==null && el.dataset.v.split('+').some(c=>c.startsWith(s));
      el.classList.toggle('hit',on);
      if(on){ n++; if(!first) first=el; }
    }
    hits.textContent = s.length>=2 ? (n? n+' found':'not found') : '';
    if(first) first.scrollIntoView({block:'center'});
  });
})();
</script>''')
dest = os.path.join(PROJECT, S['output'])
open(dest, 'w', encoding='utf-8').write(''.join(out))
print('rendered', dest, len(units), 'vehicles,', ndes, 'designed,', NSP, 'not needed')
