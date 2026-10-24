"""Render the HTML sheet for one state into the project root.

  python 05_render.py --state closure-2026-09-27

Inputs: data/derived/<state>/{timetable,fleet}.json, data/derived/vehicles_<register_date>.json,
assets/{style.css.html, pak.json, termini_meta.json}; with compare_with, also the other state's
timetable.json (for the "What changes" table).
"""
import argparse, collections, html, os, re
from common import DER, ASSETS, PROJECT, state, load, mm
import sticky

p = argparse.ArgumentParser(); p.add_argument('--state', required=True); a = p.parse_args()
S = state(a.state); X = S['texts']; FLc = S['fleet']
TT = load(os.path.join(DER, S['name'], 'timetable.json'))
FL = load(os.path.join(DER, S['name'], 'fleet.json'))
veh = load(os.path.join(DER, f"vehicles_{S['register_date']}.json"))
PAKT = load(os.path.join(ASSETS, 'pak.json')); META = load(os.path.join(ASSETS, 'termini_meta.json'))
E = lambda s: html.escape(str(s), quote=True)
ORDER = S['line_order']; LINES = FL['lines']; NET = TT['network']; EXC = FL['excluded']
DEPOT_OF = FLc['kurz_depot']
dcls = lambda d: 'pis' if d == 'Pisárky' else 'med'

# ---- vehicle cell ------------------------------------------------------------------------------
FULL = lambda c: veh[c]['type']
TYPES = lambda cs: ' + '.join(FULL(c) for c in cs)
def core(o): return re.search(r'-dpmb[a-z]+-(.+)$', o).group(1)
def pakobj(cs, i):
    t = PAKT[FULL(cs[i])]
    if t.get('missing'): return None, t
    if t.get('pair'): return (t['objs'][1] if i > 0 and PAKT.get(FULL(cs[i - 1]), {}).get('objs') == t['objs'] else t['objs'][0]), t
    return t['objs'][0], t
def pakcore(cs):
    return ' + '.join('<span class="near">≈ missing</span>' if pakobj(cs, i)[0] is None else E(core(pakobj(cs, i)[0])) for i in range(len(cs)))
def cell(cs, regs=None, ln=None, extra='', dep=''):
    nums = ' + '.join((f'<span class="dot {dcls(r)}"></span>' if regs else '') + f'<span data-v="{c}">{c}</span>' for c, r in zip(cs, regs or [None] * len(cs)))
    ty = E(TYPES(cs)) + (f' <span class="muted">· {ln} m</span>' if ln else '') + extra
    return f'<div class="vb"><span class="vn">{nums}{dep}</span><span class="vt">{ty}</span><span class="vp">{pakcore(cs)}</span></div>'
klabel = lambda u: u.get('kurz_label') or str(u['kurz'])
import datetime
def nice(d):
    d = d.replace('-', ''); x = datetime.date(int(d[:4]), int(d[4:6]), int(d[6:]))
    return f"{x.day} {x.strftime('%b')} {x.year}"
day_short = lambda d: datetime.date(*map(int, d.split('-'))).strftime('%a') + ' ' + nice(d).rsplit(' ', 1)[0]

out = []; w = out.append
units = sum(len(LINES[l]) for l in ORDER); cars = sum(len(u['cars']) for l in ORDER for u in LINES[l])
w(open(os.path.join(ASSETS, 'style.css.html'), encoding='utf-8').read().replace('<title>Brno Tram Peak Fleet</title>', f"<title>{E(S['title'])}</title>"))
w(sticky.CSS)
w('<style>@media (max-width:700px){  /* phones: keep the sticky bar short, badge and depot rows scroll sideways (as on the Olomouc and Prague sheets; added here so the shared sticky.py copies stay identical) */.controls{gap:6px 12px;padding-block:8px}.controls>.nav{flex:1 1 100%}.controls .nav.lines,.controls .nav.dnav{flex-wrap:nowrap;overflow-x:auto;min-width:0;scrollbar-width:none;-webkit-overflow-scrolling:touch}.controls .nav.lines::-webkit-scrollbar,.controls .nav.dnav::-webkit-scrollbar{display:none}.controls .nav.lines>*,.controls .nav.dnav>*{flex-shrink:0;white-space:nowrap}.controls input[type=search]{flex:1 1 150px;padding:4px 8px}}tr.subhead .keep{position:sticky;left:10px;display:inline-block;max-width:calc(100vw - 72px)}</style>')
w('<style>tr.spare td{opacity:.55}.chip.spare{background:var(--surface2);color:var(--muted)}</style>')
nav = ([('changes', 'What changes')] if S.get('compare_with') else []) + [
    ('network', X['nav_network']), ('schedule', 'Simutrans schedule'), ('lines', 'Trams by line'), ('pak', 'Pak128 objects'),
    ('depots', 'Depots'), ('termini', 'Termini at 16:00'), ('excluded', 'Not counted'), ('method', 'Method')]
w(f'''<header class="top"><div class="intro"><div class="eyebrow">{E(X['eyebrow'])}</div>
<h1>{E(S['title'])}</h1>
<p class="lede">{E(X['lede'])}</p></div>
<div class="stats"><div class="stat"><b>{len(ORDER)}</b><span>lines</span></div><div class="stat"><b>{units}</b><span>trams out</span></div><div class="stat"><b>{cars}</b><span>cars</span></div><div class="stat"><b>{len(S['depots'])}</b><span>depots</span></div></div></header>
{sticky.controls([(f'#line-{l}', l) for l in ORDER],
                 [(d, d, sum(1 for l in ORDER for u in LINES[l] if u['kdep'] == d)) for d in S['depots']],
                 [('#' + i, t) for i, t in nav if i not in ('lines', 'depots')], S['vehicles_example'] if 'vehicles_example' in S else '1822')}
''')

# ---- what changes (only with compare_with) -----------------------------------------------------------
if S.get('compare_with'):
    old = {s['id']: s for s in load(os.path.join(DER, S['compare_with'], 'timetable.json'))['schedule']}
    txt = lambda r: f"every {r['every']} · offset {r['set'][0]}" + (f" · also {','.join(map(str, r['set'][1:]))}" if r['set'][1:] else '')
    why = X.get('changes_why', {})
    w('<h2 id="changes">What changes</h2><p class="sub">Starting from the Simutrans model of the previous sheet, these are all the edits for this timetable. Values are the ones to type in, with the loop −1 rule already applied. Every schedule entry not listed stays as it is.</p>')
    w('<div class="scroll"><table class="sched"><tr><th>Line</th><th>Stop entry</th><th>Now</th><th>New</th><th>Why</th></tr>')
    for s in TT['schedule']:
        orow = {r['stop']: r for r in old.get(s['id'], {}).get('rows', [])}
        for r in s['rows']:
            o = orow.get(r['stop'])
            if o and (o['every'], o['set']) == (r['every'], r['set']): continue
            w(f'<tr><td><span class="badge">{s["id"]}</span></td><td><b>{E(r["stop"])}</b><br><span class="muted">to {E(r["to"])}</span></td>'
              f'<td class="mins">{txt(o) if o else "— (new entry)"}</td><td class="mins"><b>{txt(r)}</b></td><td class="note">{E(why.get(s["id"], ""))}</td></tr>')
        for st, o in orow.items():
            if st not in {r['stop'] for r in s['rows']}:
                w(f'<tr><td><span class="badge">{s["id"]}</span></td><td><b>{E(st)}</b></td><td class="mins">{txt(o)}</td><td class="mins"><b>remove this entry</b></td><td class="note">{E(why.get(s["id"], ""))}</td></tr>')
    w('</table></div>')
    if X.get('changes_route'): w(f'<p class="sub" style="margin-top:14px">{X["changes_route"]}</p>')
    if FL['removed']:
        w(f'<h3 style="margin-block:18px 8px">Trams moved</h3><p class="sub">{E(X["removed_intro"])}</p>')
        w('<div class="scroll"><table><tr><th>From line</th><th>Kurz</th><th>Tram · type · pak object</th><th>Goes to</th></tr>')
        for u in FL['removed']:
            dep = ' <span class="vd">· ' + E('/'.join(dict.fromkeys(u['regs']))) + '</span>'
            goes = f'line {u["to"]} (extra tram, {E(u["kdep"])} depot)' if u['to'] else 'depot reserve'
            w(f'<tr><td><span class="badge">{u["line"]}</span></td><td class="n">{u["kurz"]}</td><td>{cell(u["cars"], u["regs"], u["len"], dep=dep)}</td><td class="note">{goes}</td></tr>')
        w('</table></div>')

# ---- network ---------------------------------------------------------------------------------
w(f'<h2 id="network">{E(X["network_heading"])}</h2><p class="sub">{E(X["network_intro"])} Departures are the trips starting from each terminus between 16:00 and 16:59. Headway is the median gap between 15:00 and 18:00. Runtime is the average scheduled time from first to last stop. Depot runs are left out.</p>')
w('<div class="scroll"><table><tr><th>Line</th><th>From</th><th>To</th><th>Every</th><th>Leaves at (16:xx)</th><th>Runtime</th><th>Trams</th><th>State</th></tr>')
for l in ORDER:
    t = [x for x in NET[l] if x['n3h'] >= 3]
    note = S.get('line_notes', {}).get(l) or META['lines'].get(l, {}).get('note', '')
    st = S.get('status', {}).get(l)
    for i, x in enumerate(t):
        w('<tr>')
        if i == 0: w(f'<td rowspan="{len(t)}"><span class="badge">{l}</span></td>')
        w(f'<td>{E(x["o"])}</td><td>{E(x["d"])}</td><td class="n">{("%g min" % x["hw"]) if x["hw"] else ""}</td><td class="mins">{" ".join(mm(m) for m in x["m16"]) or "–"}</td><td class="n">{x["run"]} min</td>')
        if i == 0:
            chip = f'<span class="chip {st[1]}">{E(st[0])}</span>' if st else '<span class="chip">regular</span>'
            w(f'<td rowspan="{len(t)}" class="n"><b>{len(LINES[l])}</b></td><td rowspan="{len(t)}" class="note">{chip} {E(note)}</td>')
        w('</tr>')
w('</table></div>')

# ---- Simutrans schedule --------------------------------------------------------------------------
nl = S['nonloop']
w('<h2 id="schedule">Simutrans schedule</h2><p class="sub">Values to type into the fork’s Scheduling tab, on the two terminus entries of each line. Units are calendar minutes. The offset is minutes after midnight modulo the interval. Leave up to stays automatic (half the gap). <b>Loop terminus: every departure is set 1 min before the timetable departure, so the tram clears the loop on time.</b> Offset and each Also at value are the real minute − 1 (mod the interval; the interval is unchanged). The real minutes are shown underneath. '
  + E(X['schedule_extra']) + ' Put the timetable on the entry the tram leaves from: where a loop has a separate alighting stop set to All off, use the boarding (departure) entry. ' + E(X['schedule_exact'])
  + ' Short workings are separate lines, because Also at cannot change the route. Lines do not coordinate slots with each other, so their offsets are chosen to interleave. Depot runs are not modelled.</p>')
w('<div class="scroll"><table class="sched"><tr><th>Line</th><th>Stop entry</th><th>Departure every</th><th>Offset</th><th>Also at</th><th>Terminus</th><th>Leave up to</th><th>Per hour</th><th>Matches real timetable</th><th>Trams</th></tr>')
sl_count = collections.Counter(u['sline'] for l in ORDER for u in LINES[l])
cyc = TT.get('cycle_need', {})
for s in TT['schedule']:
    n = len(s['rows'])
    for i, r in enumerate(s['rows']):
        w('<tr>')
        if i == 0: w(f'<td rowspan="{n}" class="sl"><span class="badge">{E(s["id"])}</span><small>{E(s["name"].split(" ", 1)[1])}</small></td>')
        real = f'<small class="real">real {r["real"][0]}' + (f'; {",".join(map(str, r["real"][1:]))}' if r['real'][1:] else '') + '</small>' if r['loop'] else ''
        term = '<span class="chip loop">loop −1 min</span>' if r['loop'] else f'<span class="chip">{E(r["terminus"])}</span><br><small class="muted">real minute</small>'
        match = (f'<span class="chip ok">exact</span> {r["span"]}' + (f' <span class="muted">(except {E(r["skip"])})</span>' if r.get('skip') else '')) \
            if r['exact'] else f'<span class="chip warn">±{r["dev"]} min</span> {E(r.get("approx_note", ""))}'
        w(f'<td><b>{E(r["stop"])}</b><br><span class="muted">to {E(r["to"])}</span></td><td class="big">{r["every"]}</td><td class="big">{r["set"][0]}{real}</td>'
          f'<td class="big">{",".join(map(str, r["set"][1:])) or "–"}</td><td>{term}</td><td class="muted">auto</td><td class="n">{r["perh"]:g}</td><td class="note">{match}</td>')
        if i == 0:
            nn = sl_count.get(s['id'], 0)
            real_txt = FLc.get('trams_text', {}).get(s['id'], '{n} out on ' + day_short(S['vehicles_date']).split(' ')[0]).format(n=nn)
            c = cyc.get(s['id'])
            w(f'<td rowspan="{n}" class="note"><b>≥ {s["min_trams"]}</b> by runtime' + (f'<br>{c["trams"]} by timetable cycle' if c else '') + f'<br>{E(real_txt)}</td>')
        w('</tr>')
    if s['note']: w(f'<tr><td></td><td colspan="9" class="note">{E(s["note"])}</td></tr>')
w('</table></div>')

# ---- trams by line -------------------------------------------------------------------------------
split_of = {sp['line']: sid for sid, sp in FLc.get('splits', {}).items()}
w('<h2 id="lines">Trams by line</h2><p class="sub">One row per kurz out between about 15:00 and 17:00 on Friday, with the cars in the order they were coupled. Where more trams were logged than a Simutrans line needs by its timetable cycle, exactly the need is counted, keeping every tram type of the line, and the rest are listed at the bottom of the card as <span class="chip spare">not needed</span> (afternoon-only kurzy first; user rule, 29 Sep). The dot before each car number is its depot in the BMHD fleet register: <span class="dot pis"></span>Pisárky, <span class="dot med"></span>Medlánky. <span class="flagmark">◆</span> marks a Medlánky-registered car that ran an odd-numbered kurz, which is a Pisárky kurz; see Depots.</p><div class="grid">')
for l in ORDER:
    o = sorted(LINES[l], key=lambda u: (u['sline'] != l, u['kurz']))
    a_, b_ = NET[l][0]['o'], NET[l][0]['d']
    mix = collections.Counter(TYPES(u['cars']) for u in o)
    w(f'<article class="card" id="line-{l}"><header><span class="badge">{l}</span><div class="t"><h3>{E(a_)} – {E(b_)}</h3><div class="chips">')
    for k, n in mix.most_common(): w(f'<span class="tchip"><b>{n}×</b> {E(k)}</span>')
    w(f'</div></div><div class="count"><b>{len(o)}</b><span>trams</span></div></header><div class="scroll flat"><table><tr><th>Kurz</th><th>Tram · depot / type / pak object</th><th>Note</th></tr>')
    if l in FLc.get('line_card_notes', {}): w(f'<tr><td colspan="3" class="note s8"><b>{l} / {split_of.get(l, "")}.</b> {E(FLc["line_card_notes"][l])}</td></tr>')
    prev = None
    for u in o:
        if l in split_of and u['sline'] != prev:
            prev = u['sline']; cnt = sum(1 for x in o if x['sline'] == prev)
            lab = FLc['splits'][prev]['label'] if prev in FLc['splits'] else FLc['main_labels'][l][0]
            w(f'<tr class="subhead"><td colspan="3"><span class="badge sm">{prev}</span> {E(lab)}, {cnt} trams</td></tr>')
        dep = '/'.join(dict.fromkeys(u['regs']))
        flag = ' <span class="flagmark" title="Registered to Medlánky, ran an odd (Pisárky) kurz">◆</span>' if u['mismatch'] else ''
        w(f'<tr><td class="n">{klabel(u)}</td><td>{cell(u["cars"], u["regs"], u["len"], dep=f" <span class=vd>· {E(dep)}{flag}</span>")}</td><td class="note">{E(u["note"])}</td></tr>')
    sp = sorted((u for u in FL.get('spares', []) if u['line'] == l), key=lambda u: (u['sline'], u['kurz']))
    if sp:
        w(f'<tr class="subhead"><td colspan="3"><span class="keep">Not needed · {len(sp)} tram{"s" if len(sp) != 1 else ""} beyond the need, not counted</span></td></tr>')
        for u in sp:
            dep = '/'.join(dict.fromkeys(u['regs']))
            w(f'<tr class="spare"><td class="n">{klabel(u)}</td><td>{cell(u["cars"], u["regs"], u["len"], dep=f" <span class=vd>· {E(dep)}</span>")}</td><td class="note"><span class="chip spare">not needed</span> {E(u["sline"])}: {FL["need"].get(u["sline"], "?")} needed. {E(u["note"])}</td></tr>')
    w('</table></div></article>')
w('</div>')

# ---- pak table -------------------------------------------------------------------------------------
used_types = sorted({FULL(c) for l in ORDER for u in LINES[l] for c in u['cars']})
w('<h2 id="pak">Pak128 objects</h2><p class="sub">Each DPMB type in the peak, mapped to the vehicle objects in VZ-DPBrno-tram.pak of the custom Czech pak128. The lists above show only the pak core, the last part of the object name. The full names below all follow VZ-DPBrno-&lt;type&gt;-&lt;livery&gt;-&lt;core&gt;. A multi-section tram is several objects that the depot builds as one vehicle, in the order listed; the lists show its first core only. Length is in car units per object (16 = one tile). The pak has one livery per type, so the real livery never changes the object: newer types carry the DPMB white-red livery (dpmbbilocervena), the rest the grey-white-red one (dpmbsedobilocervena).</p><div class="scroll"><table><tr><th>Type</th><th>Pak core</th><th>Cars in the peak</th><th>Real liveries (cars)</th><th>Pak128 objects, in order</th><th>Length</th><th>Status</th></tr>')
for t in used_types:
    pk = PAKT[t]; n = sum(1 for l in ORDER for u in LINES[l] for c in u['cars'] if FULL(c) == t)
    lvc = collections.Counter(veh[c]['livery'] for l in ORDER for u in LINES[l] for c in u['cars'] if FULL(c) == t)
    top = lvc.most_common(2); rest = sum(lvc.values()) - sum(k for _, k in top)
    lvtxt = '<br>'.join(f'{k}× {E(v)}' for v, k in top) + (f'<br>{rest}× in {len(lvc) - 2} other liveries (mostly advertising)' if rest else '')
    objs = '<br>'.join(f'<span class="pak">{E(o)}</span>' for o in pk['objs']) or '<span class="pakmiss">missing</span>'
    st = '<span class="pakmiss">missing</span> ' if pk.get('missing') else ('<span class="pakmiss">limitation</span> ' if pk.get('warn') else '<span class="chip ok">installed</span> ')
    cr = (' + '.join(core(o) for o in pk['objs']) if pk.get('pair') else core(pk['objs'][0])) if pk['objs'] else '–'
    w(f'<tr><td><b>{E(t)}</b></td><td class="vp big2">{E(cr)}</td><td class="n">{n}</td><td class="note">{lvtxt}</td><td>{objs}</td><td class="n">{pk["len"] or "–"}</td><td class="note">{st}{E(pk["note"])}</td></tr>')
w('</table></div>')

# ---- depots ------------------------------------------------------------------------------------------
def depot_block(mode):
    res = []
    for dep in S['depots']:
        rows = collections.defaultdict(list)
        for l in ORDER:
            for u in LINES[l]:
                if mode == 'reg':
                    cs = [c for c, r in zip(u['cars'], u['regs']) if r == dep]
                    if cs: rows[u['sline']].append((u, cs))
                elif u['kdep'] == dep: rows[u['sline']].append((u, u['cars']))
        nu = sum(len(v) for v in rows.values()); nc = sum(len(c) for v in rows.values() for u, c in v)
        tm = collections.Counter(FULL(c) for v in rows.values() for u, cs in v for c in cs)
        sub = 'cars registered here' if mode == 'reg' else ('odd-numbered kurzy' if dep == DEPOT_OF['odd'] else 'even-numbered kurzy')
        s = [f'<article class="card depot" data-depot="{E(dep)}"' + (f' id="d-{E(dep)}"' if mode == 'kurz' else '') + '><header><div class="t"><h3><span class="dot big {dcls(dep)}"></span>Vozovna {dep}</h3><small>{sub}</small></div><div class="count"><b>{nc}</b><span>cars on {nu} trams</span></div></header>',
             '<div class="mix">' + ''.join(f'<span><b>{k}</b> {E(t)}</span>' for t, k in sorted(tm.items(), key=lambda x: (-x[1], x[0]))) + '</div>']
        for l in S['sline_order']:
            if l not in rows: continue
            v = sorted(rows[l], key=lambda x: x[0]['kurz'])
            if l in FLc.get('splits', {}): lab = FLc['splits'][l]['depot_label'] + f', {len(v)} trams'
            elif l in FLc.get('main_labels', {}): lab = FLc['main_labels'][l][1] + f', {len(v)} trams'
            else: lab = f'{len(v)} tram' + ('s' if len(v) != 1 else '')
            s.append(f'<div class="dline"><div class="lhead"><span class="badge">{l}</span><small>{lab}</small></div><div class="scroll flat"><table class="dt"><tr><th>Kurz</th><th>Tram · type · pak object</th></tr>')
            for u, cs in v:
                other = [c for c in u['cars'] if c not in cs]
                extra = f' <span class="muted">(coupled with {" + ".join(other)}, {veh[other[0]]["depot"]})</span>' if other else ''
                fl = ' <span class="flagmark">◆</span>' if u['mismatch'] else ''
                s.append(f'<tr><td class="n">{klabel(u)}</td><td>{cell(cs, extra=extra)}{fl}</td></tr>')
            s.append('</table></div></div>')
        s.append('</article>'); res.append(''.join(s))
    return ''.join(res)
w('<h2 id="depots">Depots</h2><p class="sub">Brno has two tram depots in service, Pisárky and Medlánky; Komín holds trolleybuses only. The kurz numbers and the fleet register disagree for 20 cars, so there are two views. <b>By kurz</b> uses the DPMB numbering. On this Friday every Pisárky-registered car ran an odd kurz and every even kurz ran with Medlánky cars. <b>By fleet register</b> uses the BMHD register. The 20 cars marked <span class="flagmark">◆</span> are registered to Medlánky but ran only odd kurzy: Pragoimex EVO 2 1822–1835, Pragoimex T3R.EV 1531, 1560, 1562 and 1569, and Škoda 13T6 1940. 1835 runs coupled with 1839, which the register moved to Pisárky in 9/2025. For where these trams start from, the kurz view is the better guess.</p>')
w('<div class="seg" role="group" aria-label="Group depots by"><button type="button" id="by-kurz" aria-pressed="true">By kurz (odd = Pisárky)</button><button type="button" id="by-reg" aria-pressed="false">By fleet register</button></div>')
w('<div class="depots" id="dep-kurz">' + depot_block('kurz') + '</div><div class="depots" id="dep-reg" hidden>' + depot_block('reg') + '</div>')

# ---- termini -------------------------------------------------------------------------------------------
w(f'<h2 id="termini">Termini at 16:00</h2><p class="sub">{E(X["termini_intro"])}</p>')
dep16 = collections.defaultdict(list)
for l in ORDER:
    for x in NET[l]:
        if x['m16']: dep16[x['o']].append((l, x))
w('<div class="scroll"><table><tr><th>Terminus</th><th>Tracks</th><th>Layout</th><th>Departures 16:00–16:59</th></tr>')
alias_meta = S.get('meta_alias', {})
for n in sorted(dep16, key=lambda n: (-sum(len(x['m16']) for l, x in dep16[n]), n)):
    m = META.get(alias_meta.get(n, n), {})
    deps = '<br>'.join(f'<span class="badge sm">{l}</span> to {E(x["d"])} <span class="mins">{" ".join(mm(v) for v in x["m16"])}</span>' for l, x in dep16[n])
    w(f'<tr><td><b>{E(n)}</b></td><td class="n">{m.get("tracks", "?")}</td><td class="note">{E(m.get("type", ""))}</td><td>{deps}</td></tr>')
w('</table></div>')

# ---- not counted ----------------------------------------------------------------------------------------
w(f'<h2 id="excluded">Not counted</h2><p class="sub">Records from {nice(S["vehicles_date"]).rsplit(' ', 1)[0]} left out of the afternoon count: morning-only duties and cars replaced during the day.</p><div class="scroll"><table><tr><th>Line</th><th>Kurz</th><th>Tram · type · pak object</th><th>Why</th></tr>')
for x in EXC:
    w(f'<tr><td><span class="badge">{x["line"]}</span></td><td class="n">{x["kurz"]}</td><td>{cell(x["cars"].split("+"))}</td><td class="note">{E(x["why"])}</td></tr>')
w('</table></div>')

# ---- method -----------------------------------------------------------------------------------------------
vd = S['vehicles_date']
byl = collections.defaultdict(list)
for t_, m_ in FLc['length_m'].items(): byl[m_].append(t_)
lengths = ', '.join(('15 m per car for ' if m_ == 15 else f'{m_} m: ') + ', '.join(sorted(ts)) for m_, ts in sorted(byl.items(), reverse=True))
w(f'''<h2 id="method">Method and sources</h2><div class="notes">
<p><b>Vehicles.</b> BMHD.cz vypravenost for {nice(vd)}, lines 1–12, one page per line (<a href="https://www.bmhd.cz/vypravenost/vypravenost.php?datum={vd}&amp;linka=1">line 1</a>). The records come mostly automatically from DPMB/KORDIS vehicle positions. <i>Ráno</i> and <i>ranní kurz</i> mark morning-only duties. <i>Odpoledne</i> marks the afternoon car, and <i>ráno i odpoledne</i> a split duty that works both peaks.</p>
<p><b>Swaps.</b> The notes <i>před výměnou</i> and <i>po výměně</i> carry no time. Swaps settled by where the cars turned up later: {" and ".join(FLc["resolved_swaps"])}. For the others the sheet lists the replacement car and names the replaced one in the note.</p>
<p><b>Types and depots.</b> BMHD fleet register (evidence DPMB), exact subtype, depot and livery as read on {nice(S["register_date"])}. Lengths for the model: {E(lengths)}.</p>
<p><b>Timetable.</b> IDS JMK GTFS (kordis-jmk.cz/gtfs/gtfs.zip, stored {nice(S["gtfs_date"])}), tram trips of service day {day_short(S["service_date"][:4]+"-"+S["service_date"][4:6]+"-"+S["service_date"][6:])}. Trams per line: the minimum by runtime, and the number a tram followed through its round trip at 16:00 needs (timetable cycle, at least 3 min layover at each end).</p>
<p><b>Simutrans schedule.</b> Fitted to the afternoon peak in whole calendar minutes with the fork’s Departure every / Offset / Also at fields (shared rule in pipeline/README.md). Loop terminus: set 1 min before the timetable departure so the tram clears the loop on time; {E(X["schedule_extra"][0].lower() + X["schedule_extra"][1:])}</p>
{X.get("method_extra", "")}
{X["method_state"]}
<p><b>Rebuild.</b> This sheet is generated by pipeline/brno (state “{E(S["name"])}”); see pipeline/brno/README.md.</p>
</div>
<script>
(function(){{
  var bk=document.getElementById('by-kurz'), br=document.getElementById('by-reg'), dk=document.getElementById('dep-kurz'), dr=document.getElementById('dep-reg');
  function set(reg){{ bk.setAttribute('aria-pressed',String(!reg)); br.setAttribute('aria-pressed',String(reg)); dk.hidden=reg; dr.hidden=!reg; try{{localStorage.setItem('brno-depot-view',reg?'reg':'kurz')}}catch(e){{}} }}
  bk.addEventListener('click',function(){{set(false)}}); br.addEventListener('click',function(){{set(true)}});
  try{{ if(localStorage.getItem('brno-depot-view')==='reg') set(true) }}catch(e){{}}
}})();
</script>''' + sticky.SCRIPT)
dest = os.path.join(PROJECT, S['output'])
open(dest, 'w', encoding='utf-8').write(''.join(out).replace('<nav class="nav" aria-label="Lines">', '<nav class="nav lines" aria-label="Lines">', 1))
print('rendered', dest, units, 'trams', cars, 'cars')
