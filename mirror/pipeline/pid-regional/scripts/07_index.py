"""Every PID line in one list, with the sheet it is on: python 07_index.py  ->  "PID All Lines.html" in the working folder root.

The owner, 1 Nov 2026: "all PID lines should be in". Every route of the PID GTFS (data/derived/lines.json, all modes) is
listed with where it is modelled: an oblast sheet of this pipeline (modelled, or listed with the reason), the Prague bus
sheet (city lines 100-299 and its regional companions), the Prague tram sheet (trams, metro, ferries, funicular), the
Prague trolleybus sheet, a rail sheet (a line is taken as on a rail sheet when the sheet's page names it), or no sheet,
with the reason. Sheet links are the artifact URLs in config.index.sheets.
"""
import collections, html, json, os, re
from common import HOME, DER, PIPE

PROJECT = os.path.dirname(PIPE); E = lambda s: html.escape(str(s), quote=True)
SH = json.load(open(os.path.join(HOME, 'config.json'), encoding='utf-8')); IX = SH['index']
L = json.load(open(os.path.join(DER, 'lines.json'), encoding='utf-8'))['lines']
OB = {o['id']: o for o in SH['oblasti']}
sched, conf, cls = {}, {}, {}
for oid in OB:
    d = os.path.join(HOME, 'oblasti', oid)
    if os.path.exists(os.path.join(d, 'data', 'derived', 'schedule.json')):
        sched[oid] = json.load(open(os.path.join(d, 'data', 'derived', 'schedule.json'), encoding='utf-8'))
    if os.path.exists(os.path.join(d, 'config.json')): conf[oid] = json.load(open(os.path.join(d, 'config.json'), encoding='utf-8'))
# rail sheets: the PID rail lines their page text names
rail_on = collections.defaultdict(list)
for name, sh in IX['sheets'].items():
    if sh.get('mode') != 'rail' or not sh.get('file'): continue
    p = os.path.join(PROJECT, sh['file'])
    if not os.path.exists(p): continue
    t = re.sub(r'<[^>]+>', ' ', open(p, encoding='utf-8').read())
    for v in L.values():
        if v['mode'] == 'rail' and re.search(r'(?<![\w/])' + re.escape(v['short']) + r'(?![\w])', t): rail_on[v['short']].append(name)

def where(v):
    """(status, sheet name or None, text)"""
    m, sn = v['mode'], v['short']
    if m == 'bus':
        if v.get('oblast'):
            oid = v['oblast']; k = v['key']; c = conf.get(oid, {})
            if k in c.get('other_sheets', {}).get('praha_bus', {}).get('lines', []):
                return 'modelled', 'Prague Bus Lines Check', f"regional companion of a city line (placed in {OB[oid]['name']})"
            if oid in sched and k in sched[oid]:
                n = len(sched[oid][k]['sim']); b = sum(s['need'] for s in sched[oid][k]['sim'])
                return 'modelled', f"PID {OB[oid]['name']}", f"{n} Simutrans line{'s' if n > 1 else ''}, {b} bus{'es' if b != 1 else ''}"
            if k in c.get('unmodelled', {}): return 'listed', f"PID {OB[oid]['name']}", c['unmodelled'][k]
            return 'pending', f"PID {OB[oid]['name']}", 'not designed yet'
        if v['why'] == 'a Prague city line':
            if v['night']: return 'out', None, 'Prague night line: the sheets model the weekday afternoon (no night lines)'
            if sn.isdigit() and 100 <= int(sn) < 300: return 'modelled', 'Prague Bus Lines Check', 'Prague city bus line'
            if v['substitute'] or sn.startswith('X'): return 'out', None, 'replacement bus for engineering works: short works are modelled as the regular network'
            return 'out', None, IX['other_city'].get(sn, 'Prague city special line (shuttle / airport express): not on a sheet')
        return 'out', None, v['why']
    if m in ('tram', 'metro', 'ferry', 'funicular'):
        if v['night']: return 'out', None, 'night line: no night lines on the sheets'
        if v['substitute'] or sn.startswith('X'): return 'out', None, 'replacement service for works'
        return ('modelled' if m != 'funicular' else 'out'), ('Prague Tram Peak Fleet' if m != 'funicular' else None), \
               {'tram': 'tram line', 'metro': 'metro (intervals and trains per branch)', 'ferry': 'ferry (on the tram sheet)',
                'funicular': 'funicular: not modelled'}[m]
    if m == 'trolleybus': return 'modelled', 'Prague Trolleybus Peak Fleet', 'trolleybus line'
    if m == 'rail':
        if rail_on.get(sn): return 'modelled', rail_on[sn][0], 'rail line' + (f" (also on {', '.join(rail_on[sn][1:])})" if len(rail_on[sn]) > 1 else '')
        return 'gap', None, 'rail line not on any active rail sheet yet'
    return 'out', None, m

rows = collections.defaultdict(list); cnt = collections.Counter()
for v in L.values():
    st, sheet, why = where(v); cnt[st] += 1
    grp = ('Regional buses · ' + OB[v['oblast']]['name']) if v['mode'] == 'bus' and v.get('oblast') else \
          ('Prague city buses' if v['mode'] == 'bus' else {'tram': 'Trams', 'metro': 'Metro', 'trolleybus': 'Trolleybuses', 'rail': 'Rail',
                                                         'ferry': 'Ferries', 'funicular': 'Funicular'}.get(v['mode'], v['mode']))
    rows[grp].append((v, st, sheet, why))
def sk(x):
    s = x[0]['label'] if x[0].get('label') else x[0]['short']
    return (0 if s.isdigit() else 1, int(s) if s.isdigit() else 0, s)
order = ['Metro', 'Trams', 'Trolleybuses', 'Prague city buses'] + [f"Regional buses · {o['name']}" for o in SH['oblasti']] + ['Rail', 'Ferries', 'Funicular']
CHIP = {'modelled': ('ok', 'modelled'), 'listed': ('muted', 'listed'), 'pending': ('warn', 'pending'), 'out': ('muted', 'not modelled'), 'gap': ('warn', 'no sheet')}
body = ''
for g in order + sorted(set(rows) - set(order)):
    if g not in rows: continue
    rs = sorted(rows[g], key=sk)
    n_mod = sum(1 for r in rs if r[1] == 'modelled')
    body += (f'<h2 id="{E(re.sub(r"[^a-z]+", "-", g.lower()))}">{E(g)} <small>{len(rs)} lines, {n_mod} modelled</small></h2>'
             '<div class="types"><table class="tlist"><thead><tr><th>Line</th><th>Route</th><th>Sheet</th><th>Status</th></tr></thead><tbody>')
    for v, st, sheet, why in rs:
        url = IX['sheets'].get(sheet, {}).get('url') if sheet else None
        sh_ = (f'<a href="{E(url)}">{E(sheet)}</a>' if url else E(sheet)) if sheet else '–'
        cl, lab = CHIP[st]
        body += (f'<tr><td><b>{E(v.get("label") or v["short"])}</b></td><td>{E(v["long"])}</td><td>{sh_}</td>'
                 f'<td><span class="tag {cl}">{lab}</span> {E(why)}</td></tr>')
    body += '</tbody></table></div>'
style = open(os.path.join(HOME, 'scripts', 'style.html'), encoding='utf-8').read().replace('{{TITLE}}', 'PID All Lines')
nav = ''.join(f'<a href="#{E(re.sub(r"[^a-z]+", "-", g.lower()))}">{E(g.replace("Regional buses · ", ""))}</a>' for g in order if g in rows)
page = f'''{style}
<style>.tag.ok{{background:var(--ok);color:#fff}}.tag.warn{{background:var(--warn);color:#000}}.tag.muted{{background:var(--muted);color:#fff}}.tag{{padding:1px 6px;border-radius:4px;font-size:12px}}h2 small{{font-weight:400;color:var(--muted);font-size:14px}}</style>
<header class="top"><div style="flex:1;min-width:min(100%,420px)">
<p class="eyebrow">PID · every line of the feed · {E(SH["network_state_label"])}</p><h1>PID: all lines</h1>
<p class="lede">Every route in the PID GTFS of 1 Nov 2026 (service day Mon 2 Nov) and the sheet it is modelled on, or why it is not. Regional buses are on one sheet per oblast (okres), by licence prefix; Prague-licensed and other kraje's lines go to the okres of their outer end.</p></div>
<div class="stats"><div class="stat"><b>{len(L)}</b><span>PID lines</span></div><div class="stat"><b>{cnt["modelled"]}</b><span>modelled</span></div><div class="stat"><b>{cnt["listed"] + cnt["out"]}</b><span>listed with the reason</span></div><div class="stat"><b>{cnt["gap"] + cnt["pending"]}</b><span>no sheet yet</span></div></div></header>
<div class="controls"><nav class="nav dnav">{nav}</nav></div>
{body}
<script>(function(){{var c=document.querySelector('.controls');function h(){{document.documentElement.style.setProperty('--stick',(c.offsetHeight+8)+'px')}}h();addEventListener('resize',h)}})();</script>
'''
open(os.path.join(PROJECT, 'PID All Lines.html'), 'w', encoding='utf-8').write(page)
print('PID All Lines:', len(L), 'lines', dict(cnt))
