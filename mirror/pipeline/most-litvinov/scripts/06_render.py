"""derived/*.json + config + templates/page.html -> the published HTML in the project root."""
import collections, html, os, re
from lib import CONFIG, ROOT, PROJECT, load, hm
import sticky

C = CONFIG; E = html.escape; PK = C['pak']
fleet = {int(k): v for k, v in load('fleet.json').items()}
lines = load('lines.json'); SCH = load('schedule.json'); R = load('roster.json'); VER = load('versions.json')['chosen']
assert not R['problems'], R['problems']
roster = R['roster']; BR = R['branches']; ORDER = sorted(roster, key=int)

def fullname(n):
    t = fleet[n]['type']
    if '»' in t: t = 'Tatra ' + t.split('»')[1].strip()
    return t.replace('VarioLF+', 'VarioLF plus').replace('EVO 1', 'EVO1').replace('EVO 2', 'EVO2')
def paint(n):
    m = re.search(r'nátěr:\s*(.*?)\s*(\*|\{|$)', fleet[n]['note']); p = m.group(1) if m else ''
    if p.startswith('CVR'): return 'advertising wrap ' + p[3:].strip(' ,').split(',')[0]
    return 'DPmML yellow-red' if 'žluto-červená' in p else (p or 'unknown paint')
def core(n): return PK['objects'][fullname(n)][1][0]
def unitname(nums):
    fn = [fullname(n) for n in nums]
    return ('coupled pair of ' + fn[0]) if len(nums) == 2 and fn[0] == fn[1] else ' + '.join(fn)
def cell(nums):
    """shared 3-line cell: numbers · depot / full types · length / pak core"""
    return (f'<div class="num">{" + ".join(f'<span data-v="{n}">{n}</span>' for n in nums)} <span class="dp">Most (Dopravní podnik)</span></div>'
            f'<div class="vt">{E(" + ".join(fullname(n) for n in nums))} · {E(" + ".join(C["type_lengths"][fullname(n)] for n in nums))}</div>'
            f'<div class="pak">{E(" + ".join(core(n) for n in nums))}</div>')
def brline(L):
    b = BR[L][0]
    return f"{b['a']} ⇄ {b['b']} · {b['assigned']} assigned, {b['need']} needed (round trip {b['cycle']} min with 3 min layovers; minimum by runtime {b['min_runtime']})"

cards = []
for L in ORDER:
    ln = lines[L]; T = C['peak_minute'][L]; PL = C['peak_label'][L]; ros = roster[L]
    rows = ''.join(f"<tr><td>{E(v['fr'])}</td><td class='arr'>&rarr;</td><td>{E(v['to'])}</td><td class='n'>{('every ' + str(v['hw']) + ' min') if v['hw'] else 'single trip'}</td>"
                   f"<td class='n mono'>{' '.join(f':{m:02d}' for m in v['min_peak_hour']) or '&mdash;'}</td><td class='n'>{v['rt']} min</td></tr>" for v in ln['variants'])
    sch = ''
    for p in SCH[L]:
        if not p['every']:
            why = p.get('reason') or 'one-off'
            sch += f"<tr class='all'><td>{E(p['fr'])} &rarr; {E(p['to'])}</td><td colspan='4'>not modelled ({E(why)}): {', '.join(hm(x) for x in p['single'])}</td></tr>"; continue
        real = ', '.join(f':{m:02d}' for m in range(60) if m % p['every'] in p['real']) if 60 % p['every'] == 0 else ', '.join(map(str, p['real'])) + f' (mod {p["every"]})'
        sch += (f"<tr><td>{E(p['fr'])} &rarr; {E(p['to'])}<div class='win'>loop: 1 min before timetable {real} · {'designed frequency, see the line note' if p.get('designed') else 'exact ' + hm(p['first']) + '–' + hm(p['last'])}</div></td>"
                f"<td class='n sv'>{p['every']}</td><td class='n sv'>{p['set'][0]}</td><td class='mono'>{', '.join(map(str, p['set'][1:])) or '&mdash;'}</td><td class='n'>auto</td></tr>")
    stopsd = ''; seen = set()
    for v in ln['variants']:
        if tuple(v['stops']) in seen or v['n'] < 2: continue
        seen.add(tuple(v['stops'])); stopsd += f"<p><b>{E(v['fr'])} &rarr; {E(v['to'])}</b> ({len(v['stops'])} stops): {E(' · '.join(v['stops']))}</p>"
    mix = collections.Counter(unitname(u) for u in ros)
    chips = ''.join(f'<li class="v">{cell(u)}</li>' for u in ros)
    nn = C.get('not_needed', {}).get(L)
    if nn:   # roster coverage and spares rule (user, 29 Sep 2026): the line's other roster cars, shown but not counted
        chips += ''.join(f'<li class="v spare">{cell(u)}<div class="vt">not needed · {E(nn["why"].split(".")[0])}</div></li>' for u in nn['cars'])
    cards.append(f"""<article class="card" id="l{L}"><header><span class="badge">{L}</span><div class="hd"><h3>{E(C['line_titles'][L])}</h3><p>{E(', '.join(f'{c}× {t}' for t, c in mix.items()))}</p></div><div class="cnt"><b>{len(ros)}</b><span>tram{"s" if len(ros) != 1 else ""} at {PL}</span></div></header>
<div class="tw"><table class="tt"><thead><tr><th>From</th><th></th><th>To</th><th class="n">Headway</th><th class="n">Leaves {PL[:2]}:xx</th><th class="n">Runtime</th></tr></thead><tbody>{rows}</tbody></table></div>
<div class="sched"><h4>Simutrans schedule · loop departures set 1 min early</h4><div class="tw0"><table class="st2"><thead><tr><th>Terminus entry</th><th class="n">Departure every (min)</th><th class="n">Offset (min)</th><th>Also at (min)</th><th class="n">Leave up to</th></tr></thead><tbody>{sch}</tbody></table></div></div>
<p class="lnote">{E(C['line_notes'][L])}</p><p class="brsub">{E(brline(L))}</p><ul class="vs">{chips}</ul>
<details><summary>Stops</summary>{stopsd}</details></article>""")

depot = ''
for L in ORDER:
    b = BR[L][0]
    depot += f"<tr class='brh'><td colspan='2'><a class='badge sm' href='#l{L}'>{L}</a> {E(b['a'])} ⇄ {E(b['b'])} · {len(roster[L])} trams, {'morning peak' if C['peak_minute'][L] < 720 else 'afternoon peak'} {C['peak_label'][L]}</td></tr>"
    depot += ''.join(f"<tr><td class='vc'>{cell(u)}</td><td class='stc'>designed</td></tr>" for u in roster[L])
used = {n for L in roster for u in roster[L] for n in u}
spare = collections.defaultdict(list)
for n, c in sorted(fleet.items()):
    if n in used or fullname(n) not in PK['objects']: continue
    st = {'zar': 'reserve', 'dilny': 'in workshops'}.get(c['state'], c['state'])
    extra = f" ({C['car_notes'][str(n)]})" if str(n) in C.get('car_notes', {}) else ''
    spare[st].append(f'{n} {fullname(n)}{extra}')
spsec = ''.join(f"<p><b>{E(k)}</b> ({len(v)}) {' · '.join(E(x) for x in v)}</p>" for k, v in spare.items())
agg = collections.Counter(); pnt = collections.defaultdict(collections.Counter)
for L in roster:
    for u in roster[L]:
        for n in u:
            agg[fullname(n)] += 1; p = paint(n); pnt[fullname(n)]['advertising wrap' if p.startswith('advertising') else p] += 1
paks = ''
for k, (fam, parts, length) in PK['objects'].items():
    chain = ' → '.join(f"{PK['prefix']}{fam}-{PK['livery']}-{x}" for x in parts)
    notes = (['advertising wraps are shown in the DPmML yellow-red livery'] if 'advertising wrap' in pnt[k] else []) + ([PK['notes'][k]] if k in PK['notes'] else [])
    near = f"<div class='pak subst'>{E('; '.join(notes))}</div>" if notes else ''
    real = ', '.join(f'{v}× {x}' for x, v in pnt[k].most_common()) or 'none at the peak'
    paks += (f"<tr><td>{E(k)}</td><td><b class='core'>{E(parts[0])}</b><div class='pak'>{E(chain)}</div>{near}</td>"
             f"<td>yellow-red ({PK['livery']})<div class='lv'>real: {E(real)}</div></td><td class='n'>{length}</td><td class='n'>{agg.get(k, 0)}</td></tr>")
state = '\n'.join(f'  <div class="st"><h4><span class="tag {io}">{"modelled" if io == "in" else "not modelled"}</span>{E(h)}</h4><p>{E(p)}</p></div>' for io, h, p in C['network_state'])
why = ''.join(f"<li>Line {L}: {E(C['roster'][L]['why'])} Cars: {E(', '.join(' + '.join(map(str, u)) for u in C['roster'][L]['cars']))}.</li>" for L in sorted(C['roster'], key=lambda x: {'4': 0, '2': 1, '1': 2, '3': 3}.get(x, 9)))
inactive = [f'{n} ({fullname(n)})' for n, c in sorted(fleet.items()) if c['state'] == 'dilny' and fullname(n) in PK['objects']]
import datetime
versions = ' and '.join(datetime.date.fromisoformat(x).strftime('%-d %b %Y') if os.name != 'nt' else datetime.date.fromisoformat(x).strftime('%#d %b %Y') for x in sorted(set(v['valid_from'] for v in VER.values())))
tpl = open(os.path.join(ROOT, 'templates', 'page.html'), encoding='utf-8').read()
rep = dict(PEAK_WHY=E(C['peak_why'] + ' ' + C['peak_rule']), BRANCHES_WHY=E(C['branches_why'] + ' ' + C['fit_why']), POOLS=E(C['shared_pools']), TITLE=C['title'], VEHICLE_DAY_LABEL=C['vehicle_day_label'], VEHICLE_DAY_EN=C['vehicle_day_label_en'], STATE_LABEL=C['network_state_label'], STATE=state,
           CONTROLS=sticky.controls([(f'#l{L}', L) for L in ORDER], [('most', 'Most (Dopravní podnik)', sum(len(roster[L]) for L in roster))], [('#pak', 'Pak128 objects'), ('#method', 'How this was built')], str(roster[ORDER[0]][0][0])),
           JDF_LABEL=C['jdf']['export_label'], VERSIONS='valid from ' + versions, CARDS='\n'.join(cards), DEPOT=depot, SPARE=spsec, PAKS=paks,
           TOT=str(sum(len(roster[L]) for L in roster)), CARS=str(len(used)), ROSTER_WHY=why,
           INACTIVE_NOTE=('In the workshops: ' + ', '.join(inactive) + '.') if inactive else '')
for k, v in rep.items(): tpl = tpl.replace('{{' + k + '}}', v)
tpl = tpl.replace('</style>', '</style>\n' + sticky.CSS, 1)
tpl = tpl.replace('</body>', sticky.SCRIPT + '\n</body>') if '</body>' in tpl else tpl + '\n' + sticky.SCRIPT
assert not re.findall(r'\{\{[A-Z_]+\}\}', tpl)
out = os.path.join(PROJECT, C['output_html']); open(out, 'w', encoding='utf-8').write(tpl)
print('wrote', out, 'units', rep['TOT'], 'cars', rep['CARS'])
