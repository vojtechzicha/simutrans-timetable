"""Render the MD-CR sheet (project root "MD-CR.html") from data/derived/schedule.json.

Timetable only: no vehicles, no depots (user, 29 Sep 2026).
"""
import html, json, os, datetime as D

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PROJECT = os.path.dirname(os.path.dirname(ROOT))
CFG = json.load(open(os.path.join(ROOT, 'config.json'), encoding='utf-8'))
NAMES = json.load(open(os.path.join(ROOT, 'assets', 'names.json'), encoding='utf-8'))['replace']
OUT = os.path.join(PROJECT, 'archive', 'MD-CR.html')  # archived 5 Oct 2026
E = lambda s: html.escape(str(s), quote=True)

CATNAME = {'R': 'Rychlík', 'Ex': 'Expres', 'IC': 'InterCity', 'EC': 'EuroCity', 'SC': 'SuperCity Pendolino',
           'rj': 'railjet', 'RJ': 'RegioJet', 'LE': 'Leo Express', 'EN': 'EuroNight', 'NJ': 'Nightjet',
           'ES': 'European Sleeper', 'TLX': 'Trilex-express'}
GROUPS = [('Ex', 'Expres lines (state contract)'), ('R', 'Rychlík lines (state and regional contracts)'),
          ('C', 'Commercial lines (open access)')]


def full(n):
    if not n:
        return n
    for a, b in NAMES:
        n = n.replace(a, b)
    return n


def slug(code):
    return 'l-' + code.lower().replace(' ', '-')


def group(l):
    if l['kind'] == 'commercial':
        return 'C'
    return 'Ex' if l['code'].startswith('Ex') else 'R'


def badge(l, sm=False):
    txt = l['code'] if l['kind'] == 'state' and not l['code'].endswith('-R') else l['badge']
    return f'<span class="badge {group(l).lower()}{" sm" if sm else ""}">{E(txt)}</span>'


def hm_off(I, s):
    return f"{s // 60:02d}:{s % 60:02d}" if I > 60 else f":{s:02d}"


def minutes(v):
    return f"{v} min" if v is not None else '—'


def ext_row(x, end):
    return (f'<tr class="abroad"><th scope="row">{E(x["terminal"])}</th>'
            f'<td class="ra"><span class="chip">abroad</span> Departure every 0: the Czech timetable has no times here. '
            f'Trains are held at {E(full(end))} instead (row above or below, and the long stops).</td>'
            f'<td class="n">0</td><td class="n">—</td><td class="n">—</td><td class="n">—</td></tr>')


def tt_rows(sim):
    out = []
    for end in (sim['a'], sim['b']):
        x = sim['ext'].get(end)
        if x and end == sim['a']:
            out.append(ext_row(x, end))
        t = sim['tt'][end]
        if t['kind'] == 'untimed':
            later = ', '.join(t.get('later') or [])
            out.append(f'<tr><th scope="row">{E(full(end))}</th>'
                       f'<td class="ra"><span class="chip">no timetable</span> no departure here between 12:00 and 20:00; trains return at {E(later) or "other times"}</td>'
                       f'<td class="n">0</td><td class="n">—</td><td class="n">—</td><td class="n">—</td></tr>')
            continue
        I = t['I']
        also = '—'
        leave = f"{t['leave']['set']} min" if t['leave']['set'] else f"automatic ({t['leave']['auto']} min)"
        notes = []
        if t['kind'] == 'exact':
            notes.append('<span class="chip ok">exact</span>')
        else:
            notes.append(f'<span class="chip warn">approximate, up to {t["maxdev"]} min off</span>')
        if t.get('forced'):
            notes.append('<span class="chip">rate of the other end</span>')
        if t.get('basis') and t['basis'] != 'afternoon':
            notes.append(f'<span class="chip warn">{E(t["basis"])}</span>')
        span = f"{t['fits']} of {t['of']} departures 12:00–20:00 keep it" if t['I'] < 1440 else ''
        extra = []
        if t.get('offpattern'):
            extra.append('off the standard: ' + ', '.join(t['offpattern']))
        if t.get('empty'):
            extra.append('no train in the slot at ' + ', '.join(t['empty']))
        lab = f'<div class="small muted">last Czech station, trains to and from {E(x["terminal"])}</div>' if x else ''
        out.append(f'<tr><th scope="row">{E(full(end))}{lab}</th>'
                   f'<td class="ra"><b class="cz">{E(t["text"])}</b> <span class="muted small">{E(span)}</span> {"".join(notes)}'
                   + (f'<div class="small muted">{E("; ".join(extra))}</div>' if extra else '') + '</td>'
                   f'<td class="n">{I}</td><td class="n">{t["offset"]}</td><td class="n">{E(also)}</td><td class="n">{E(leave)}</td></tr>')
        if x and end == sim['b']:
            out.append(ext_row(x, end))
    return ''.join(out)


def dep_list(rows, end):
    items = []
    for r in rows:
        cls = ['dep']
        if not (CFG['window']['search_from'] <= r['m'] < CFG['window']['search_to']):
            cls.append('off')
        if r['merged']:
            cls.append('mg')
        nums = ' + '.join(r['nums'])
        dest = full(r['to'])
        if r['dest']:
            dest += ' → ' + full(r['dest'])
        title = f"{CATNAME.get(r['cat'], r['cat'])} {nums}, {r['op']}, arrives {dest.split(' → ')[0]} {r['arr']}"
        items.append(f'<li class="{" ".join(cls)}" data-v="{E(nums.replace(" + ", "+"))}"><span class="n t">{r["t"]}</span> '
                     f'<span class="tn">{E(r["cat"])} {E(nums)}</span> <span class="to">{E(dest)}</span>'
                     f'<span class="sr">{E(title)}</span></li>')
    return f'<ol class="deps">{"".join(items)}</ol>'


def pattern_html(sim):
    main = [p for p in sim['pattern'] if p['main']]
    other = [p for p in sim['pattern'] if not p['main']]
    rows = []
    for k, p in enumerate(main):
        dwell = (p['dep'] - p['arr']) if (p['dep'] is not None and p['arr'] is not None) else None
        part = '' if p['served'] == p['of'] else f'<span class="chip">{p["served"]} of {p["of"]} trains</span>'
        req = '<span class="chip">request stop</span>' if p['req'] else ''
        t = p['dep'] if k < len(main) - 1 else p['arr']
        rows.append(f'<li data-v="{E(full(p["name"]))}"><span class="n km">{"+" + str(t) if t is not None else "—"}</span>'
                    f'<span class="st">{E(full(p["name"]))}</span>{" <span class=\"muted small\">" + str(dwell) + " min stop</span>" if dwell and dwell >= 3 else ""} {part}{req}</li>')
    extra = ''
    if other:
        extra = ('<p class="small muted">Also served by a minority of trains, not in the Simutrans schedule: '
                 + ', '.join(f'{E(full(p["name"]))} ({p["served"]} of {p["of"]})' for p in other) + '.</p>')
    xa, xb = sim['ext'].get(sim['a']), sim['ext'].get(sim['b'])

    def ab(x):
        brd = (f'<li class="abroad"><span class="n km">·</span><span class="st">{E(x["border"])}</span> '
               f'<span class="muted small">first station abroad</span></li>') if x.get('border') else ''
        term = (f'<li class="abroad"><span class="n km">·</span><span class="st">{E(x["terminal"])}</span> '
                f'<span class="chip">terminal abroad, {x["trips"]} of {x["of"]} trains</span></li>')
        return brd, term
    if xa:
        brd, term = ab(xa)
        rows = [term, brd] + rows
    if xb:
        brd, term = ab(xb)
        rows = rows + [brd, term]
    others = []
    for x in (xa, xb):
        if x and x['others']:
            others.append('other trains continue to ' + ', '.join(f'{E(o)} ({n})' for o, n in x['others']))
    if others:
        extra += '<p class="small muted">Beyond the border: ' + '; '.join(others) + ' (tails abroad, not modelled).</p>'
    return f'<ol class="stops">{"".join(rows)}</ol>{extra}'


def simname(sim):
    xa, xb = sim['ext'].get(sim['a']), sim['ext'].get(sim['b'])
    return ((xa['terminal'] + ' – ') if xa else '') + full(sim['a']) + ' – ' + full(sim['b']) + ((' – ' + xb['terminal']) if xb else '')


WHY = {'passengers': 'long passenger stop', 'no passengers': 'stop without passengers (crossing, engine or crew change)',
       'before the border': 'stay before leaving the Czech Republic', 'from abroad': 'stay after arriving from abroad'}


def stays_html(sim):
    rows = []
    for start in (sim['a'], sim['b']):
        for x in sim['stays'][start]:
            # at a Czech terminus with no foreign design the stay is the terminus entry itself
            if x['kind'] in ('before the border', 'from abroad') and not sim['ext'].get(x['name']):
                continue
            d = x['dep']
            leave = f"{d['leave']['set']} min" if d['leave']['set'] else f"automatic ({d['leave']['auto']} min)"
            stay = f"{x['dwell_min']}" + (f"–{x['dwell_max']}" if x['dwell_max'] != x['dwell_min'] else '') + ' min'
            note = '<span class="chip ok">exact</span>' if d['kind'] == 'exact' else f'<span class="chip warn">up to {d["maxdev"]} min off</span>'
            trains = ', '.join(f'{c} {a}→{b}' for c, a, b in x['trains'][:6]) + (' …' if len(x['trains']) > 6 else '')
            arr = x['arr']['text'].replace('every ', '')
            rows.append(f'<tr><td>from {E(full(start))}</td><th scope="row" data-v="{E(full(x["name"]))}">{E(full(x["name"]))}</th>'
                        f'<td>{E(WHY[x["kind"]])}<div class="small muted">{x["n"]} of {x["of"]} trains · {E(trains)}</div></td>'
                        f'<td class="n">{E(stay)}</td>'
                        f'<td class="ra">arrive <span class="cz">{E(arr)}</span>, leave <b class="cz">{E(d["text"])}</b> {note}</td>'
                        f'<td class="n">{d["I"]}</td><td class="n">{d["offset"]}</td><td class="n">{E(leave)}</td></tr>')
    if not rows:
        return ''
    return ('<h5>Long stops: give these entries a timetable too</h5><div class="scroll"><table class="tt"><thead><tr><th>Direction</th><th>Stop</th><th>Why</th>'
            '<th>Stay</th><th>Reads as</th><th>Departure every</th><th>Offset</th><th>Leave up to</th></tr></thead><tbody>' + ''.join(rows) + '</tbody></table></div>')


def sim_block(l, sim, k):
    a, b = full(sim['a']), full(sim['b'])
    cats = ', '.join(f'{CATNAME.get(c, c)} {n}' for c, n in sim['cats'])
    ops = ', '.join(f'{o} {n}' for o, n in sim['ops'])
    foreign = ', '.join(full(f) for f, _ in sim['foreign'])
    merged = ''
    if sim['merged']:
        merged = ('<div class="tails"><b>Tails, not modelled as their own line</b> <span class="muted small">(below the branch threshold: '
                  'at least 3 trips 12:00–20:00, a departure 14:00–18:00 and a clock-face rhythm). Their departure minute from the shared '
                  'terminus is folded into this line (◇ below); the part beyond it is not modelled.</span><ul>' + ''.join(
                      f'<li><b>{E(full(m["a"]))} – {E(full(m["b"]))}</b>: {m["trips"]} trip{"s" if m["trips"] > 1 else ""} · '
                      + ', '.join(f'{r["t"]} {E(r["cat"])} {E("+".join(r["nums"]))} → {E(full(r["to"]))}' for r in m['rows']) + '</li>'
                      for m in sim['merged']) + '</ul></div>')
    runtime = next((p['arr'] for p in reversed(sim['pattern']) if p['main'] and p['arr'] is not None), None)
    return f'''<section class="sim" id="{slug(l['code'])}-{k}">
<header><h4>{E(simname(sim))}</h4>
<div class="chips"><span class="chip">{sim['trips']} trips a day</span><span class="chip">{sim['n_window']} between 12:00 and 20:00</span>{f'<span class="chip">{runtime} min end to end</span>' if runtime else ''}</div></header>
<p class="small muted">{E(cats)} · {E(ops)}{(' · beyond the border: ' + E(foreign)) if foreign else ''}</p>
<div class="scroll"><table class="tt"><thead><tr><th>Timetable on</th><th>Reads as</th><th>Departure every</th><th>Offset</th><th>Also at</th><th>Leave up to</th></tr></thead><tbody>{tt_rows(sim)}</tbody></table></div>
{stays_html(sim)}
{merged}
<div class="two">
<div><h5>Stops from {E(a)}</h5>{pattern_html(sim)}</div>
<div><h5>Departures from {E(a)}</h5>{dep_list(sim['deps'][sim['a']], sim['a'])}
<h5>Departures from {E(b)}</h5>{dep_list(sim['deps'][sim['b']], sim['b'])}</div>
</div>
</section>'''


VERDICT = {
    'stay': 'Chaining at {x}: {s} of {n} trains leave on another branch than they came from, so the branches are separate Simutrans lines with interleaved offsets.',
    'mixed': 'Chaining at {x}: {s} of {n} trains switch branch, with no strict A–B–A–B order, so the branches are separate Simutrans lines with interleaved offsets (a modelling choice).',
    'alternate': 'Chaining at {x}: {s} of {n} trains switch branch in turn, so the line is modelled with {x} entered twice.'}


def linename(l):
    if l['kind'] == 'commercial' or l['code'].endswith('-R'):
        return full(l['name'])
    return ' / '.join(simname(x) for x in l['sims'][:3])


def line_card(l):
    cats = ', '.join(f'{CATNAME.get(c, c)}' for c, _ in l['cats'])
    un = ''
    if l['unmodelled']:
        un = '<p class="small"><b>Not modelled</b> (no shared terminus with a modelled line, outside the afternoon): ' + '; '.join(
            f'{E(full(v["a"]))} – {E(full(v["b"]))} at ' + ', '.join(r['t'] + ' ' + r['cat'] + ' ' + '+'.join(r['nums']) for r in v['rows']) for v in l['unmodelled']) + '.</p>'
    sims = ''.join(sim_block(l, s, k) for k, s in enumerate(l['sims']))
    trunk = ''
    for tr in l.get('trunks', []):
        t = tr['tt']
        to = ', '.join(f'{E(full(x))} {n}×' for x, n in tr['to'])
        far = ', '.join(E(full(x)) for x, _ in tr['foreign'][:4])
        trunk += (f'<p class="trunk"><span class="lab">Common standard</span> from <b>{E(full(tr["from"]))}</b> '
                  f'<b class="cz">{E(t["text"])}</b>{f" <span class=\"chip warn\">±{t['dev']} min</span>" if t['dev'] else ""} '
                  f'<span class="muted small">({t["fits"]} of {t["of"]} afternoon departures) — trains to {to}{("; beyond the border " + far) if far else ""}</span>'
                  f'<span class="small">{E(VERDICT[tr["verdict"]].format(x=full(tr["from"]), s=tr["switch"], n=tr["links"]))}</span></p>')
    return f'''<article class="line" id="{slug(l['code'])}">
<header>{badge(l)}<div><h3>{E(linename(l))}</h3><p class="small muted">{E(cats)} · {l['trips']} trips a day · {len(l['sims'])} Simutrans line{'s' if len(l['sims']) > 1 else ''}</p></div></header>
{trunk}{sims}{un}
</article>'''


CSS = r'''
/* Layout: one column of line cards; each Simutrans line = timetable table, then stops and departures side by side. */
:root{
  --bg:#f2f4f3; --surface:#ffffff; --surface2:#e7ebea; --ink:#1a1f1e; --ink2:#414a48; --muted:#6c7573; --rule:#d9dfdd; --rule2:#c3cbc9;
  --accent:#0b5f7a; --accent-ink:#ffffff; --accent-soft:#d7eaf0;
  --ex:#0b5f7a; --r:#a33b2b; --c:#5b4a8a; --warn:#8f5c10; --warn-soft:#fbefd9; --info:#2b5f9e;
  --font-display:"Barlow Condensed","Arial Narrow","Helvetica Neue",Arial,sans-serif;
  --font-body:"Barlow","Helvetica Neue",Arial,sans-serif;
  --font-mono:"IBM Plex Mono","SFMono-Regular",Consolas,monospace;
  color-scheme:light;
}
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){
    --bg:#111617; --surface:#1a2021; --surface2:#242c2d; --ink:#e9efee; --ink2:#c1cac8; --muted:#8e9896; --rule:#2e3738; --rule2:#404a4b;
    --accent:#5fb7d4; --accent-ink:#06222b; --accent-soft:#16323b;
    --ex:#5fb7d4; --r:#e58a78; --c:#b5a3ea; --warn:#e0a94a; --warn-soft:#3b2d14; --info:#7fb0ea;
    color-scheme:dark;
  }
}
:root[data-theme="dark"]{
  --bg:#111617; --surface:#1a2021; --surface2:#242c2d; --ink:#e9efee; --ink2:#c1cac8; --muted:#8e9896; --rule:#2e3738; --rule2:#404a4b;
  --accent:#5fb7d4; --accent-ink:#06222b; --accent-soft:#16323b;
  --ex:#5fb7d4; --r:#e58a78; --c:#b5a3ea; --warn:#e0a94a; --warn-soft:#3b2d14; --info:#7fb0ea;
  color-scheme:dark;
}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--font-body);font-size:15px;line-height:1.45;padding-inline:clamp(16px,3vw,40px);padding-block:0 64px}
h1,h2,h3,h4,h5{font-family:var(--font-display);text-wrap:balance;margin:0;line-height:1.1}
h1{font-size:clamp(40px,6vw,64px);font-weight:700;letter-spacing:.01em}
h2{font-size:28px;font-weight:600;margin-block:40px 10px}
h3{font-size:24px;font-weight:700}
h4{font-size:19px;font-weight:700}
h5{font-size:13px;font-weight:600;text-transform:uppercase;letter-spacing:.1em;color:var(--muted);margin-block:12px 6px}
p{margin:0}
a{color:var(--info)}
.muted{color:var(--muted)} .small{font-size:13px}
.lede{max-width:72ch;color:var(--ink2);font-size:16px}
header.top{display:flex;flex-wrap:wrap;gap:20px 40px;align-items:flex-end;justify-content:space-between;padding-block:36px 20px;border-bottom:3px solid var(--accent)}
header.top .intro{display:flex;flex-direction:column;gap:10px;max-width:780px;min-width:0}
.eyebrow{font-family:var(--font-display);font-weight:600;text-transform:uppercase;letter-spacing:.12em;font-size:13px;color:var(--accent)}
.stats{display:flex;gap:28px;flex-wrap:wrap}
.stat{display:flex;flex-direction:column}
.stat b{font-family:var(--font-display);font-size:34px;font-weight:700;line-height:1;font-variant-numeric:tabular-nums}
.stat span{font-size:12px;text-transform:uppercase;letter-spacing:.08em;color:var(--muted)}
.controls{position:sticky;top:env(safe-area-inset-top,0px);z-index:5;background:var(--bg);padding-block:10px;border-bottom:1px solid var(--rule);display:flex;flex-wrap:wrap;gap:8px 20px;align-items:center}
.controls .nav{display:flex;flex-wrap:wrap;gap:4px;align-items:center}
.controls .lab{font:600 12px var(--font-display);text-transform:uppercase;letter-spacing:.1em;color:var(--muted);padding-inline:2px 6px}
.controls .sec a{font:600 14px var(--font-display);text-decoration:none;color:var(--ink2);background:var(--surface2);padding:3px 8px;border-radius:4px}
.controls input[type=search]{font:14px var(--font-body);padding:6px 10px;border:1px solid var(--rule2);border-radius:6px;background:var(--surface);color:var(--ink);width:min(100%,260px)}
.controls a:focus-visible,.controls input:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
#hits{font-size:13px;color:var(--muted)}
[id]{scroll-margin-top:var(--stick,120px)}
[data-v].hit{background:color-mix(in srgb,var(--accent) 22%,transparent);outline:2px solid var(--accent);border-radius:3px}
.badge{display:inline-flex;align-items:center;justify-content:center;min-width:44px;height:28px;padding-inline:7px;border-radius:4px;color:var(--accent-ink);font:700 17px var(--font-display);font-variant-numeric:tabular-nums;flex-shrink:0;text-decoration:none}
.badge.ex{background:var(--ex)} .badge.r{background:var(--r)} .badge.c{background:var(--c)}
.badge.sm{height:22px;min-width:34px;font-size:14px;padding-inline:5px}
.chip{display:inline-block;font:600 11px var(--font-display);text-transform:uppercase;letter-spacing:.08em;padding:2px 8px;border-radius:999px;background:var(--surface2);color:var(--ink2);white-space:nowrap;margin-inline-start:4px}
.chip.warn{background:var(--warn-soft);color:var(--warn)}
.chips{display:flex;flex-wrap:wrap;gap:4px}
.box{background:var(--surface);border:1px solid var(--rule);border-radius:8px;padding:14px 16px;display:flex;flex-direction:column;gap:8px;max-width:980px}
.box ul{margin:0;padding-inline-start:20px;display:flex;flex-direction:column;gap:4px}
.cz{font-family:var(--font-mono);font-weight:500;font-size:14px}
.n{font-family:var(--font-mono);font-variant-numeric:tabular-nums;white-space:nowrap}
.scroll{overflow-x:auto;background:var(--surface);border:1px solid var(--rule);border-radius:6px}
table{border-collapse:collapse;width:100%;font-size:14px}
th,td{text-align:left;padding:7px 10px;border-bottom:1px solid var(--rule);vertical-align:top}
thead th{font:600 12px var(--font-display);text-transform:uppercase;letter-spacing:.1em;color:var(--muted);background:var(--surface2);white-space:nowrap}
tbody th{font-weight:600;white-space:nowrap}
tr:last-child td,tr:last-child th{border-bottom:0}
.gh{display:flex;align-items:baseline;gap:12px;flex-wrap:wrap}
.lines{display:flex;flex-direction:column;gap:22px}
article.line{background:var(--surface);border:1px solid var(--rule);border-radius:8px;padding:16px;display:flex;flex-direction:column;gap:16px;min-width:0}
article.line>header{display:flex;gap:12px;align-items:flex-start}
section.sim{border-top:1px solid var(--rule);padding-top:14px;display:flex;flex-direction:column;gap:10px;min-width:0}
section.sim>header{display:flex;flex-wrap:wrap;gap:6px 12px;align-items:baseline}
.two{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.1fr);gap:8px 28px}
@media (max-width:760px){.two{grid-template-columns:minmax(0,1fr)}}
ol.stops{list-style:none;margin:0;padding:0;display:flex;flex-direction:column}
ol.stops li{display:flex;gap:10px;align-items:baseline;padding-block:2px;border-left:3px solid var(--rule2);padding-inline-start:10px;flex-wrap:wrap}
ol.stops li:first-child,ol.stops li:last-child{border-left-color:var(--accent);font-weight:600}
ol.stops .km{min-width:4.2em;color:var(--muted);font-size:13px}
ol.deps{list-style:none;margin:0;padding:0;columns:2 220px;column-gap:16px}
ol.deps li{display:flex;gap:8px;align-items:baseline;font-size:13px;min-width:0;break-inside:avoid;padding-block:1px}
td.ra{min-width:min(60vw,300px)}
ol.deps li .t{font-weight:500}
ol.deps li .tn{color:var(--ink2);white-space:nowrap}
ol.deps li .to{color:var(--muted);overflow-wrap:anywhere}
ol.deps li.off{opacity:.55}
ol.deps li.mg .t::after{content:" ◇";color:var(--accent)}
.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}
.trunk{background:var(--accent-soft);border-radius:6px;padding:8px 12px;display:flex;flex-wrap:wrap;gap:4px 8px;align-items:baseline}
.trunk .lab{font:600 12px var(--font-display);text-transform:uppercase;letter-spacing:.1em;color:var(--accent)}
.chip.ok{background:var(--accent-soft);color:var(--accent)}
ol.stops li.abroad{border-left-style:dashed;color:var(--muted);font-style:italic}
tr.abroad th,tr.abroad td{color:var(--muted)}
.tails{font-size:13px;border-left:3px solid var(--rule2);padding-inline-start:10px}
.tails ul{margin:4px 0 0;padding-inline-start:18px}
.trunk>.small{flex-basis:100%}
.legend{display:flex;flex-wrap:wrap;gap:6px 18px;font-size:13px;color:var(--ink2)}
details{max-width:980px}
summary{cursor:pointer;font-family:var(--font-display);font-weight:600;font-size:17px}
@media (prefers-reduced-motion:no-preference){html{scroll-behavior:smooth}}
'''

SCRIPT = '''<script>
(function(){
  var c=document.querySelector('.controls'); if(!c) return;
  function h(){ document.documentElement.style.setProperty('--stick',(c.offsetHeight+8)+'px'); }
  h(); window.addEventListener('resize',h);
  var q=document.getElementById('q'), hits=document.getElementById('hits');
  var all=[].slice.call(document.querySelectorAll('[data-v]'));
  q.addEventListener('input',function(){
    var s=q.value.trim().toLowerCase(), first=null, n=0;
    all.forEach(function(el){
      var v=el.getAttribute('data-v').toLowerCase();
      var on=s.length>=3 && v.split('+').some(function(x){return x.indexOf(s)===0;});
      el.classList.toggle('hit',on);
      if(on){ n++; if(!first) first=el; }
    });
    hits.textContent = s.length>=3 ? (n ? n+' found' : 'not found') : '';
    if(first) first.scrollIntoView({block:'center'});
  });
})();
</script>'''


def main():
    d = json.load(open(os.path.join(ROOT, 'data', 'derived', 'schedule.json'), encoding='utf-8'))
    excluded = json.load(open(os.path.join(ROOT, 'data', 'derived', 'excluded.json'), encoding='utf-8'))
    lines = d['lines']
    nsim = sum(len(l['sims']) for l in lines)
    ntrips = sum(l['trips'] for l in lines) + len(d['not_lines'])
    day = D.date.fromisoformat(CFG['service_day'])
    def barlabel(l):
        if l['code'].endswith('-R'):
            return 'R Žilina'
        if l['kind'] == 'state':
            return l['code']
        return l['badge'] + ' ' + ('Ostrava' if 'OVA' in l['code'] else 'Břeclav')
    badges = ''.join(f'<a class="badge sm {group(l).lower()}" href="#{slug(l["code"])}">{E(barlabel(l))}</a>' for l in lines)
    body = []
    for g, title in GROUPS:
        ls = [l for l in lines if group(l) == g]
        if ls:
            body.append(f'<h2 id="g-{g.lower()}">{E(title)}</h2><div class="lines">' + ''.join(line_card(l) for l in ls) + '</div>')
    # not modelled
    ex = ''.join(f'<tr><td>{E(e["cat"])} {E(e["num"])}</td><td>{E(full(e["origin"] or e["from"]))} → {E(full(e["destination"] or e["to"]))}</td><td>{E(e["why"])}</td></tr>' for e in excluded)
    page = f'''<title>MD-CR</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700&family=Barlow:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>{CSS}</style>
<header class="top"><div class="intro">
<span class="eyebrow">Czech long-distance rail · Simutrans timetable sheet</span>
<h1>MD-CR</h1>
<p class="lede">Every Rychlík, Expres, InterCity, EuroCity, SuperCity, railjet, RegioJet and Leo Express train in the Czech Republic, grouped by the line it runs on in the afternoon peak, with the Simutrans schedule for each line. Timetable only: no vehicles, no depots. Network of {day.strftime('%A')} {day.day} {day.strftime('%B %Y')} from the national timetable (CIS JŘ 2026).</p>
</div>
<div class="stats"><div class="stat"><b>{len(lines)}</b><span>peak lines</span></div><div class="stat"><b>{nsim}</b><span>Simutrans lines</span></div><div class="stat"><b>{ntrips}</b><span>trains that day</span></div></div>
</header>
<div class="controls">
<nav class="nav" aria-label="Lines"><span class="lab">Lines</span>{badges}</nav>
<nav class="nav sec" aria-label="Sections"><span class="lab">Sections</span><a href="#read">How to read</a><a href="#g-ex">Expres</a><a href="#g-r">Rychlík</a><a href="#g-c">Commercial</a><a href="#left-out">Left out</a><a href="#method">Method</a></nav>
<input type="search" id="q" placeholder="Find train or station, e.g. 982" aria-label="Find train number or station">
<span id="hits" aria-live="polite"></span>
</div>
<h2 id="read">How to read</h2>
<div class="box">
<ul>
<li><b>Peak line</b> is the line number the trains carry in the national timetable (Ex1–Ex7, Ex32, R8–R94), or the commercial carrier and corridor for trains without one. Each peak line is split into <b>Simutrans lines</b>, one per distinct path, because the fork's “Also at” cannot change the route.</li>
<li>The timetable goes on the two termini only, on the entry the train leaves from. Intermediate stops carry no timetable, so a late train does not wait a whole interval there (engine session advice).</li>
<li>Rail termini keep the <b>real minute</b>. The city −1 min loop rule does not apply, because trains reverse at the platform.</li>
<li><b>Reads as</b> uses the Czech notation: <span class="cz">every 2 h at L:07</span> means odd hours (liché) at :07, <span class="cz">S</span> means even hours (sudé). Offset and Also at are minutes after midnight modulo the interval.</li>
<li><b>Leave up to</b>: automatic at intervals up to 60 min; 30 min at longer intervals, because automatic would be half the gap, 60 min or more (engine session advice).</li>
<li><b>Standard, not one hour:</b> each terminus gets the common clock-face pattern of the whole afternoon (12:00–20:00): the headway (1 h, 2 h or 4 h) and the minute most trains keep, within ±5 min. Trains off the standard and standard slots with no train are listed under it. Paler departure times fall outside 12:00–20:00. ◇ marks a merged train that really runs to or from another terminus.</li>
<li><b>Common standard</b> (tinted bar): where several Simutrans lines leave the same terminus, the combined pattern of all their trains, e.g. Ex1 from Praha every 2 h, alternately to Bohumín and Návsí. Under it, the chaining test says whether the branches are separate lines or one line with the shared terminus entered twice.</li>
<li><b>Abroad:</b> a line whose trains mostly cross the border is designed to its most common terminal outside the Czech Republic (in italics). The Czech data has no times abroad, so that entry gets Departure every 0 and the train is held at the last Czech station.</li>
<li><b>Long stops</b>: stops where the train stands for more than loading passengers (5 min or more at a passenger stop, 2 min or more where it takes no passengers, the stay at a border station). Each gets its own timetable entry, per direction, so the wait isn't lost.</li>
</ul>
<div class="legend"><span><span class="badge sm ex">Ex</span> Expres line</span><span><span class="badge sm r">R</span> Rychlík line</span><span><span class="badge sm c">RJ</span> commercial line</span><span><span class="chip ok">exact</span> every train keeps the standard</span><span><span class="chip warn">approximate, up to 4 min off</span> the largest deviation</span><span><span class="chip">rate of the other end</span> one headway for the whole Simutrans line</span></div>
</div>
{''.join(body)}
<h2 id="left-out">Left out</h2>
<p class="lede">Trains in the requested categories that are not a peak line, and trains in other long-distance categories that were not requested.</p>
<div class="scroll" style="max-width:980px"><table><thead><tr><th>Train</th><th>Route</th><th>Why</th></tr></thead><tbody>
{''.join(f'<tr><td>{E(n["trip"]["cat"])} {E("+".join(n["trip"]["nums"]))} at {E(n["trip"]["t"])}</td><td>{E(full(n["from"]))} → {E(full(n["trip"]["to"]))}</td><td>one train a day on its own corridor, not a peak line</td></tr>' for n in d['not_lines'])}
{ex}
</tbody></table></div>
<h2 id="method">Method</h2>
<div class="box">
<ul>
<li><b>Source:</b> CIS JŘ national rail timetable 2026 (ftp.cisjr.cz, draha/celostatni/szdc/2026/JR2026.zip, 13,252 train files), trains running on {day.isoformat()}. Monthly engineering-work variants are ignored: short-term closures are modelled as the regular state.</li>
<li><b>Categories:</b> R, Ex, IC, EC, SC, rj, RegioJet and Leo Express. Local trains (Os, Sp) are not included. Night trains (EuroNight, Nightjet, European Sleeper) and the regional Trilex-express are listed under “Left out”.</li>
<li><b>Czech part only:</b> a train is cut to its Czech stops. Its foreign continuation is named next to the departure.</li>
<li><b>Branches</b> (agreed with the city sessions, 29 Sep): the route with the most trips is always a Simutrans line. Another route is its own line when it has at least 3 trips between 12:00 and 20:00, a departure between 14:00 and 18:00, and a clock-face rhythm (1, 2 or 4 h). Chaining the trains at the shared terminus (turnaround 15–240 min) decides between separate branch lines and one line with the terminus entered twice (strict A–B–A–B, like Plzeň 4); none of the rail lines alternates strictly. Rarer routes are tails: their minute from the shared terminus is folded into the line, and they are listed with their trains.</li>
<li><b>Foreign terminal:</b> when at least half of a line's trains continue abroad at one end, the line runs on to their most common terminal. The data names stabling points for some (Grochów, Langenfelde); the sheet names the city with the stabling point.</li>
<li><b>Long stops:</b> per direction, stops where at least half the trains (or at least 2) stand 5 min or more with passengers, or 2 min or more without, plus stays at the border station. The fork values are the standard of their departure minutes at the line's headway.</li>
<li><b>Rychlík trains under an Expres line number</b> (Ostrava – Žilina under line 1) form their own line.</li>
<li><b>Standard:</b> for each headway of 1 h, 2 h and 4 h (30 min where trains run that often), the minute that most afternoon departures keep within ±5 min. Each departure kept counts 1 and each empty slot counts −0.75; the best headway wins. One slot per terminus, no Also at.</li>
<li><b>One headway per line:</b> chosen on the afternoon departures of both ends together; each end then takes its own best minute at that headway, so one extra train at one end (Kysučan's 19:21 from Návsí) doesn't turn a 4-hourly line into a 2-hourly one.</li>
<li><b>Station names</b> are written in full (CIS JŘ abbreviates them).</li>
<li>Rules agreed with the other timetable sessions on 29 Sep 2026; pipeline and update recipe in <span class="n">pipeline/md-cr/</span>.</li>
</ul>
</div>
{SCRIPT}
'''
    open(OUT, 'w', encoding='utf-8').write(page)
    print('wrote', OUT, len(page) // 1024, 'KB')


if __name__ == '__main__':
    main()
