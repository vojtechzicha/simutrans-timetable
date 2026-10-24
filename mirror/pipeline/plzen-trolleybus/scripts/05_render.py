"""Render one Plzeň fleet sheet (trolleybus, or bus with --base ../../plzen-bus) into the project root.

  python 05_render.py --state 2026-09-29
  python 05_render.py --state 2026-09-29 --base ../../plzen-bus

The page is the Brno trolleybus / bus sheet's: page style from pipeline/brno/assets/style.css.html, the sticky bar,
search and chips from pipeline/brno-trolleybus/assets/extra.css.html, plus assets/extra.css.html here (all read only).
Every vehicle is a 3-line cell: number · depot / full type · length (+ battery, designed, operator marks) / pak core.
Texts that differ between the two sheets come from the state ("texts", "words").
"""
import argparse, collections, html, os, re
from common import BASE, PIPE, PROJECT, DER as TDER, ASSETS as TASSETS, state, load, mm, hm, nice

p = argparse.ArgumentParser(); p.add_argument('--state', required=True); p.add_argument('--base', default=BASE); a = p.parse_args()
base = os.path.abspath(a.base); S = state(a.state, base); X = S['texts']; W = S['words']; DER = os.path.join(base, 'data', 'derived')
TT = load(os.path.join(DER, S['name'], 'timetable.json'))
FL = load(os.path.join(DER, S['name'], 'fleet.json'))
PAK = load(os.path.join(base, 'assets', 'pak_map.json'))
OFF = load(os.path.join(DER, S['name'], 'offwire.json'))['lines'] if os.path.exists(os.path.join(DER, S['name'], 'offwire.json')) else {}
E = lambda s: html.escape(str(s), quote=True)
LINES = FL['lines']; NET = TT['network']; SCHED = TT['schedule']; SL = {sl['id']: sl for sl in S['simutrans_lines']}
GAR = S['garages']; DCLS = {d: ('kar' if i == 0 else 'ext') for i, d in enumerate(S['depots'])}
aid = lambda s: 'line-' + s.replace('+', '-')
sl_of = collections.defaultdict(list)
for sl in S['simutrans_lines']:
    for e in sl['entries']:
        if sl['id'] not in sl_of[e[0]]: sl_of[e[0]].append(sl['id'])
def depot(u):
    return GAR.get(u.get('garage'), u.get('garage')) if u.get('operator') == 'PMDP' else u.get('operator') or '?'
TYPES = S['pak']['types']
def pk(u):
    k = PAK['by_car'].get(u.get('id', ''))
    if k: return PAK['objects'][k]
    return next((x for k, x in PAK['objects'].items() if k.split('|')[:2] == [u.get('operator'), u['type']]), None)
def pakcore(u):
    x = pk(u)
    if not x: return '<span class="pakmiss">no object</span>'
    return E(x['core_shown']) + (' <span class="chip req">requested</span>' if x['status'] == 'requested' else '')
def length(u):
    t = TYPES.get(u['type']); return f"{t['m']} m" if t else '?'
def marks(u):
    m = ''
    if S['traction'] == 'trolleybus':
        m += '<span class="batmark">battery</span>' if u.get('battery') == 'battery' else ('<span class="dieselmark">diesel auxiliary</span>' if u.get('battery') == 'diesel' else '')
    if u.get('designed'): m += ' <span class="chip des">designed</span>'
    if u.get('operator', 'PMDP') != 'PMDP': m += f' <span class="chip opx">{E(u["operator"])}</span>'
    return m
def cell(u, dep=True):
    d = depot(u)
    num = (f'<span class="dot {DCLS.get(d, "ext")}"></span>' if dep else '') + f'<span class="veh" data-v="{E(u["car"])}">{E(u["car"])}</span>' + \
          (f' <span class="vd">· {E(d)}</span>' if dep else '')
    return (f'<div class="vb"><span class="vn">{num}</span><span class="vt">{E(u["type"])} <span class="muted">· {length(u)}</span>{marks(u)}</span>'
            f'<span class="vp">{pakcore(u)}</span></div>')
allunits = [u for o in LINES.values() for u in o]
units = [u for u in allunits if not u.get('spare')]
NSP = len(allunits) - len(units); NDES = sum(1 for u in units if u.get('designed'))
ops = collections.Counter(u['operator'] for u in units)

out = []; w = out.append
style = open(os.path.join(PIPE, 'brno', 'assets', 'style.css.html'), encoding='utf-8').read()
w(re.sub(r'<title>.*?</title>', f"<title>{E(S['title'])}</title>", style))
w(open(os.path.join(PIPE, 'brno-trolleybus', 'assets', 'extra.css.html'), encoding='utf-8').read())
w(open(os.path.join(TASSETS, 'extra.css.html'), encoding='utf-8').read())
ac = S['accent']
w(f'<style>:root{{--accent:{ac["light"][0]};--accent-soft:{ac["light"][1]}}}@media (prefers-color-scheme: dark){{:root:not([data-theme="light"]){{--accent:{ac["dark"][0]};--accent-soft:{ac["dark"][1]}}}}}:root[data-theme="dark"]{{--accent:{ac["dark"][0]};--accent-soft:{ac["dark"][1]}}}</style>')
bat = S['traction'] == 'trolleybus'
nav = [('network', 'Network at 16:00')] + ([('battery', 'Battery sections')] if bat else []) + [
       ('schedule', 'Simutrans schedule'), ('lines', W['Vehicles'] + ' by line'), ('pak', 'Pak128 objects'), ('depots', 'Depots'),
       ('termini', 'Termini at 16:00'), ('excluded', 'Not counted'), ('method', 'Method')]
stats = [(len(S['line_order']), 'PMDP lines'), (len(SCHED), 'Simutrans lines'), (len(units), W['vehicles'] + ' counted'),
         (NDES, 'designed'), (NSP, 'not needed')]
if len(ops) > 1: stats.insert(3, (len(units) - ops.get('PMDP', 0), 'other operators'))
w(f'''<header class="top"><div class="intro"><div class="eyebrow">{E(X['eyebrow'])}</div>
<h1>{E(S['title'])}</h1>
<p class="lede">{E(X['lede'])}</p></div>
<div class="stats">''' + ''.join(f'<div class="stat"><b>{n}</b><span>{E(t)}</span></div>' for n, t in stats) + '</div></header>\n')
dep_n = collections.Counter(depot(u) for u in units)
deps_all = list(S['depots']) + sorted(d for d in dep_n if d not in S['depots'])
DCLS.update({d: 'ext' for d in deps_all if d not in DCLS})
w('<div class="controls"><nav class="nav lines" aria-label="Lines"><span class="lab">Lines</span>'
  + ''.join(f'<a class="badge" href="#{aid(s["id"])}">{E(s["id"])}</a>' for s in SCHED) + '</nav>'
  + '<nav class="nav dnav" aria-label="Depots and sections"><span class="lab">Depots</span>'
  + ''.join(f'<a href="#depot-{i}">{E(d)} <b>{dep_n[d]}</b></a>' for i, d in enumerate(deps_all))
  + ''.join(f'<a href="#{i}">{E(t)}</a>' for i, t in nav) + '</nav>'
  + f'<input type="search" id="q" placeholder="Find {W["vehicle"]}, e.g. {E(W["example"])}" aria-label="Find vehicle number" inputmode="numeric"><span id="hits" aria-live="polite"></span></div>')

# ---- network ------------------------------------------------------------------------------------------
w(f'<h2 id="network">Network at 16:00</h2><p class="sub">{E(X["network"])}</p>')
w('<div class="scroll"><table><tr><th>Line</th><th>From</th><th>To</th><th>Every</th><th>Leaves at (16:xx)</th><th>Runtime</th>'
  + ('<th>Battery</th>' if bat else '') + '<th>Simutrans line</th></tr>')
for l in S['line_order']:
    t = [x for x in NET[l] if x['n3h'] >= 3]
    if not t: continue
    stretches = []
    for sid in sl_of[l]:
        for s_ in FL['battery_lines'].get(sid, []):
            if not any(set(s_[:2]) == set(x) for x in stretches): stretches.append(tuple(s_[:2]))
    for i, x in enumerate(t):
        w('<tr>')
        if i == 0: w(f'<td rowspan="{len(t)}"><span class="badge">{E(l)}</span></td>')
        w(f'<td>{E(x["o"])}</td><td>{E(x["d"])}</td><td class="n">{("%g min" % x["hw"]) if x["hw"] else ""}</td><td class="mins">{" ".join(mm(m) for m in x["m16"]) or "–"}</td><td class="n">{x["run"]} min</td>')
        if i == 0:
            if bat:
                w(f'<td rowspan="{len(t)}" class="note">' + ('<span class="chip bat">battery</span> ' + '; '.join(f'{E(a2)} – {E(b)}' for a2, b in stretches) if stretches else '<span class="muted">under wire</span>') + '</td>')
            w(f'<td rowspan="{len(t)}">' + ' '.join(f'<a href="#{aid(s)}"><span class="badge sm">{E(s)}</span></a>' for s in sl_of[l]) + '</td>')
        w('</tr>')
w('</table></div>')
nm = [x for x in TT['not_modelled'] if x['n'] >= 2]
w('<p class="sub" style="margin-top:12px"><b>Not modelled.</b> ' + E(X.get('not_modelled', ''))
  + (' Minor patterns in 15:00–18:00 left out of the Simutrans lines: ' + '; '.join(f'{E(x["line"])} {E(x["o"])} → {E(x["d"])} ({x["n"]} trips)' for x in nm) + '.' if nm else '') + '</p>')

# ---- battery ------------------------------------------------------------------------------------------
if bat:
    BR = S['battery_text']
    w(f'<h2 id="battery">Battery sections</h2><p class="sub">{E(BR["intro"])}</p><div class="batgrid">')
    for l in S['line_order']:
        pats = [pt for pt in OFF.get(l, []) if pt['stretches'] and pt['trips'] >= 5]
        if not pats: continue
        sids = sl_of[l]; chk = [FL['battery_check'][s] for s in sids if s in FL['battery_check']]
        w(f'<article class="batcard"><h3><span class="badge">{E(l)}</span><small class="muted">Simutrans {E(", ".join(sids))}</small></h3>')
        legs = {(e[1], e[2]) for sid in sids for e in SL[sid]['entries']}
        shown = [pt for pt in pats if (pt['o'], pt['d']) in legs] or pats[:2]     # the modelled legs, else the busiest patterns
        seen = set()
        for pt in shown:
            for s in pt['stretches']:
                if (pt['d'], s[0], s[1]) in seen: continue
                seen.add((pt['d'], s[0], s[1]))
                w(f'<div class="sec">{E(s[0])} – {E(s[1])} <small class="muted">about {s[2]:g} km, on the way to {E(pt["d"])}</small></div>')
        if BR['lines'].get(l): w(f'<p>{E(BR["lines"][l])}</p>')
        if chk:
            for s, c in zip([s for s in sids if s in FL['battery_check']], chk):
                if c['not_battery']:
                    w(f'<p><span class="checkbad">Check failed on {E(s)}:</span> {E(", ".join(c["not_battery"]))} not battery-capable.</p>')
                else:
                    tys = collections.Counter(u['type'] for u in LINES[s] if not u.get('spare'))
                    w(f'<p><span class="checkok">Check passed on {E(s)}:</span> all {c["counted"]} counted trolleybuses are battery-capable (' + ', '.join(f'{n}× {E(t)}' for t, n in tys.most_common()) + ').</p>')
        else:
            w('<p class="muted">Not in the modelled peak: ' + E(BR['unmodelled'].get(l, 'this pattern is not a peak trip.')) + '</p>')
        w('</article>')
    w(f'</div><p class="sub">{E(BR["outro"])}</p>')

# ---- schedule -----------------------------------------------------------------------------------------
def match(r):
    if r['exact']: return f'<span class="chip ok">exact</span> {r["span"]}'
    t = f'<span class="chip warn">approximate, ±{r["dev"]} min</span> real 16:xx {" ".join(mm(m) for m in r["hour"])}'
    if r['missing']: t += f'; not reproduced: {" ".join(mm(m) for m in r["missing"])}'
    if r['extra']: t += f'; modelled but not in the timetable: {" ".join(mm(m) for m in r["extra"])}'
    return t
w(f'<h2 id="schedule">Simutrans schedule</h2><p class="sub">{E(X["schedule"])}</p>')
w(f'<div class="scroll"><table class="sched"><tr><th>Line</th><th>Stop entry</th><th>Departure every</th><th>Offset</th><th>Also at</th><th>Stop type</th><th>Leave up to</th><th>Per hour</th><th>Matches real timetable</th><th>{W["Vehicles"]}</th></tr>')
short = FL['short']
for s in SCHED:
    n = len(s['rows']); ne = s['need']
    for i, r in enumerate(s['rows']):
        w('<tr>')
        if i == 0:
            nm_ = s['name'].split(' ', 1)[1] if ' ' in s['name'] else s['name']
            kind = {'circuit': 'one line, both branches', 'pool': 'pool', 'oneway': 'one-way working', 'branch': 'branch'}.get(s['kind'], '')
            w(f'<td rowspan="{n}" class="sl"><a href="#{aid(s["id"])}"><span class="badge">{E(s["id"])}</span></a><small>{E(nm_)}</small>'
              + (f'<small><span class="chip pool">{E(kind)}</span></small>' if kind else '') + '</td>')
        lbl = f'<b>{E(r["stop"])}</b><br><span class="muted">to {E(r["to"])}' + (f' · as {E(r["line"])}' if r['line'] != s['id'].rstrip('ABCDEFGHIJKLMNOPQRSTUVWXYZ') and not r.get('untimed') else '') + '</span>'
        if r.get('untimed'):
            w(f'<td>{lbl}</td><td class="big">0</td><td class="big">–</td><td class="big">–</td><td><span class="chip">no timetable</span></td><td class="muted">–</td><td class="n">–</td><td class="note">Empty back to {E(r["to"])}, about {r["run"]} min (out of service in reality).</td>')
        else:
            real = (f'<small class="real">real {r["real"][0]}' + (f'; {", ".join(map(str, r["real"][1:]))}' if r['real'][1:] else '') + '</small>') if r['loop'] else ''
            term = '<span class="chip loop">loop −1 min</span>' if r['loop'] else '<span class="chip">through stop</span><br><small class="muted">real minute</small>'
            w(f'<td>{lbl}</td><td class="big">{r["every"]}</td><td class="big wrap">{r["set"][0]}{real}</td><td class="big wrap">{", ".join(map(str, r["set"][1:])) or "–"}</td><td>{term}</td><td class="muted">auto</td><td class="n">{r["perh"]:g}</td><td class="note">{match(r)}</td>')
        if i == 0:
            nn = sum(1 for u in LINES[s['id']] if not u.get('spare')); sh = short.get(s['id'])
            nlog = sum(1 for u in LINES[s['id']] if u['src'] not in ('designed', 'history'))
            nd = sum(1 for u in LINES[s['id']] if u.get('designed'))
            nsp_ = sum(1 for u in LINES[s['id']] if u.get('spare'))
            w(f'<td rowspan="{n}" class="note"><b>{ne["vehicles"] if ne else "?"}</b> needed'
              + (f' (timetable cycle {ne["minutes"]} min' + (f', +{ne["onroad_extra"]} for the most on the road at once' if ne.get('onroad_extra') else '') + ')' if ne else '')
              + (f'<br><span class="muted">{E(s["need_why"])}</span>' if s.get('need_why') else '')
              + f'<br><b>{nlog}</b> logged' + (f', <b>{nd}</b> designed' if nd else '') + (f', {nsp_} not needed' if nsp_ else '')
              + (f' <span class="chip warn">{sh} short</span>' if sh else '') + '</td>')
        w('</tr>')
    for t in (s['note'], s.get('text')):
        if t: w(f'<tr><td></td><td colspan="9" class="note" style="white-space:normal;max-width:0">{E(t)}</td></tr>')
w('</table></div>')
w(f'<p class="sub" style="margin-top:12px">{E(X["need"])}</p>')

# ---- vehicles by line ---------------------------------------------------------------------------------
w(f'<h2 id="lines">{W["Vehicles"]} by line</h2><p class="sub">{E(X["lines"])}</p><div class="grid">')
kz = lambda u: (bool(u.get('spare')), u['src'] == 'history', bool(u.get('designed')), u['rec'], (0, u['kurz']) if isinstance(u['kurz'], int) else (1, str(u['kurz'])))
for s in SCHED:
    o = sorted(LINES[s['id']], key=kz); sl = SL[s['id']]
    oc = [u for u in o if not u.get('spare')]
    mix = collections.Counter(u['type'] for u in oc)
    w(f'<article class="card" id="{aid(s["id"])}"><header><span class="badge">{E(s["id"])}</span><div class="t"><h3>{E(s["name"].split(" ", 1)[1] if " " in s["name"] else s["name"])}</h3><div class="chips">')
    for k, c in mix.most_common(): w(f'<span class="tchip"><b>{c}×</b> {E(k)} · {length(dict(type=k))}</span>')
    w(f'</div></div><div class="count"><b>{len(oc)}</b><span>{W["vehicles"]}</span></div></header>')
    if s['id'] in FL['split_of']:
        sibs = [x['id'] for x in S['simutrans_lines'] if x['records'] == sl['records']]
        w(f'<p class="pooltext"><span class="chip">split, a choice</span> PMDP records line {E(sl["records"])} as one set of kurzy, shared here between Simutrans lines {E(", ".join(sibs))} by timetable need: the branch takes the highest kurz numbers (the peak-only split duties), the main line the rest. The records do not say which kurz ran the branch.</p>')
    if sl.get('text'):
        chip = {'pool': 'pool', 'circuit': 'one line, both branches', 'branch': 'branch', 'oneway': 'one-way working'}.get(sl.get('kind'), '')
        w(f'<p class="pooltext">' + (f'<span class="chip pool">{E(chip)}</span> ' if chip else '') + ('<span class="chip warn">not confirmed</span> ' if sl['text'].startswith('Inferred') else '') + f'{E(sl["text"])}</p>')
    ne = s['need']['vehicles'] if s['need'] else None
    nlog = [u for u in o if u['src'] not in ('designed', 'history')]
    nsp = sum(1 for u in nlog if u.get('spare'))
    if nsp:
        w(f'<p class="pooltext"><span class="chip spare">not needed</span> {len(nlog)} logged against {ne} needed; {nsp} marked not needed, keeping one of every type of the line first, then dropping afternoon-only kurzy and the highest kurz numbers.</p>')
    dl = FL['designed'].get(s['id'])
    if dl:
        span = f"{nice(dl['history_span'][0])} – {nice(dl['history_span'][1])}" if dl['history_span'] else 'no history'
        w(f'<p class="pooltext"><span class="chip des">designed</span> {dl["short"]} fewer logged than needed on {E(nice(S["vehicles_date"]))}. {dl["picked"]} designed from the line’s own records ({dl["history_days"]} working days, {E(span)}): real cars, active in the register, not out anywhere on the vehicle day, first one of each roster type the logged cars lack, then the most recent.'
          + (f' {dl["spares"]} more free history cars are listed as not needed.' if dl['spares'] else '') + (f' <span class="chip warn">still {dl["still_short"]} short</span>' if dl.get('still_short') else '') + '</p>')
    if short.get(s['id']) and not dl:
        w(f'<p class="pooltext"><span class="chip warn">{short[s["id"]]} short</span></p>')
    w(f'<div class="scroll flat"><table><tr><th>Kurz</th><th>{W["Vehicle"]} · depot / type / pak object</th><th>Note</th></tr>')
    for u in o:
        sp = u.get('spare'); cls = 'spare' if sp else ('designed' if u.get('designed') else '')
        kk = f"{E(u['rec'])}/{E(u['kurz'])}" if u['kurz'] != '' else '<span class="muted">history</span>'
        w(f'<tr{f" class=\"{cls}\"" if cls else ""}><td class="n">{kk}</td><td>{cell(u)}</td><td class="note">' + ('<span class="chip spare">not needed</span> ' if sp else '') + f'{E(u["note"])}</td></tr>')
    w('</table></div></article>')
w('</div>')

# ---- pak ----------------------------------------------------------------------------------------------
w(f'<h2 id="pak">Pak128 objects</h2><p class="sub">{E(X["pak"])} {E(PAK["_source"])}</p>')
w(f'<div class="scroll"><table><tr><th>Operator · type</th><th>Length</th><th>Pak core</th><th>{W["Vehicles"]} counted</th><th>Real liveries ({W["vehicles"]})</th><th>Pak128 objects, in order</th><th>Car units</th><th>Status</th></tr>')
keyf = lambda u: (u['operator'], u['type'])
for (op, t), n in sorted(collections.Counter(keyf(u) for u in units).items(), key=lambda kv: (kv[0][0] != 'PMDP', TYPES.get(kv[0][1], {}).get('m', 0), kv[0][1])):
    us = [u for u in units if keyf(u) == (op, t)]; x = pk(us[0])
    lv = collections.Counter(u['livery'] or 'not recorded' for u in us)
    lvtxt = '<br>'.join(f'{k}× {E(v)}' for v, k in lv.most_common())
    objs = '<br>'.join(f'<span class="pak">{E(o)}</span>' for o in x['objs']) if x else '<span class="pakmiss">no object</span>'
    stt = ('<span class="chip req">requested</span> not in the pak yet; asked for in pak_request.md' if x['status'] == 'requested' else '<span class="chip ok">installed</span>') if x else ''
    extra = ' <span class="muted">(advert wraps map to the normal livery)</span>' if any(not v.startswith(tuple(S['pak']['liveries'])) for v in lv) else ''
    w(f'<tr><td><b>{E(t)}</b><br><span class="muted">{E(op)}</span></td><td class="n">{length(us[0])}</td><td class="vp big2">{pakcore(us[0])}</td><td class="n">{n}</td><td class="note">{lvtxt}{extra}</td><td>{objs}</td><td class="n">{x["len"] if x else "–"}</td><td class="note">{stt}</td></tr>')
w('</table></div>')

# ---- depots -------------------------------------------------------------------------------------------
w(f'<h2 id="depots">Depots</h2><p class="sub">{E(X["depots"])}</p><div class="depots">')
for i, dep in enumerate(deps_all):
    rows = collections.defaultdict(list)
    for s in SCHED:
        for u in LINES[s['id']]:
            if depot(u) == dep and not u.get('spare'): rows[s['id']].append(u)
    nv = sum(len(v) for v in rows.values()); tm = collections.Counter(u['type'] for v in rows.values() for u in v)
    w(f'<article class="card depot" id="depot-{i}"><header><div class="t"><h3><span class="dot big {DCLS.get(dep, "ext")}"></span>{E(W["depot_prefix"] if dep in S["depots"] else "")}{E(dep)}</h3><small>{"PMDP" if dep in S["depots"] else "other operator"}</small></div><div class="count"><b>{nv}</b><span>{W["vehicles"]} counted</span></div></header>')
    w('<div class="mix">' + ''.join(f'<span><b>{k}</b> {E(t)}</span>' for t, k in tm.most_common()) + '</div>')
    for s in SCHED:
        if s['id'] not in rows: continue
        v = sorted(rows[s['id']], key=kz)
        w(f'<div class="dline"><div class="lhead"><span class="badge">{E(s["id"])}</span><small>{len(v)} {W["vehicle"] if len(v) == 1 else W["vehicles"]}</small></div><div class="scroll flat"><table class="dt"><tr><th>Kurz</th><th>{W["Vehicle"]} · type · pak object</th></tr>')
        for u in v: w(f'<tr><td class="n">{E(u["rec"])}/{E(u["kurz"])}</td><td>{cell(u, dep=False)}</td></tr>')
        w('</table></div></div>')
    w('</article>')
w('</div>')

# ---- termini --------------------------------------------------------------------------------------------
w(f'<h2 id="termini">Termini at 16:00</h2><p class="sub">{E(X["termini"])}</p>')
dep16 = collections.defaultdict(list)
for l in S['line_order']:
    for x in NET[l]:
        if x['m16'] and x['n3h'] >= 3: dep16[x['o']].append((l, x))
w('<div class="scroll"><table><tr><th>Terminus</th><th>Departures 16:00–16:59</th></tr>')
for nm_ in sorted(dep16, key=lambda n: (-sum(len(x['m16']) for l, x in dep16[n]), n)):
    deps = '<br>'.join(f'<span class="badge sm">{E(l)}</span> to {E(x["d"])} <span class="mins">{" ".join(mm(v) for v in x["m16"])}</span>' for l, x in dep16[nm_])
    w(f'<tr><td><b>{E(nm_)}</b></td><td>{deps}</td></tr>')
w('</table></div>')

# ---- not counted ----------------------------------------------------------------------------------------
veh = load(os.path.join(TDER, f"vehicles_{S['register_date']}.json"))
w(f'<h2 id="excluded">Not counted</h2><p class="sub">Records from {E(nice(S["vehicles_date"]))} left out of the afternoon count: morning-only duties (ráno), and cars counted on another line.</p><div class="scroll"><table><tr><th>Kurz</th><th>{W["Vehicle"]} · depot / type / pak object</th><th>Why</th></tr>')
for x in sorted(FL['excluded'], key=lambda x: (len(x['line']), x['line'], str(x['kurz']))):
    v = veh.get(x['ids'][0], {})
    u = dict(id=x['ids'][0], car=v.get('num', '?'), type=v.get('type', '?'), garage=v.get('garage', ''), operator=v.get('operator', '?'), livery=v.get('livery', ''))
    w(f'<tr><td class="n">{E(x["line"])}/{E(x["kurz"])}</td><td>{cell(u)}</td><td class="note">{E(x["why"])}</td></tr>')
w('</table></div>')

# ---- method -----------------------------------------------------------------------------------------------
w('<h2 id="method">Method and sources</h2><div class="notes">' + ''.join(f'<p><b>{E(k)}.</b> {v}</p>' for k, v in X['method']) + '</div>')
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
print('rendered', dest, len(units), W['vehicles'], 'counted,', NDES, 'designed,', NSP, 'not needed')
