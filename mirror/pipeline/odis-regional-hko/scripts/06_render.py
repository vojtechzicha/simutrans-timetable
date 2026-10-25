"""schedule + roster + config -> the sheet (config.output_html in the project root).

The page style is the Havířov/Karviná/Orlová sheet's (templates/style.html, copied), with the shared sticky bar: line
badges, area and depot links, section links and a vehicle search over every [data-v] (pipeline README, "Page header").
Every vehicle is a 3-line cell: number · branch / full type · length (plate) / pak core and livery.
"""
import collections, glob, html, json, os, re
from lib import CONFIG, PROJECT, ROOT, HOME, load, hm, rel, tmin

E = lambda s: html.escape(str(s), quote=True)
S = load('schedule.json'); R = load('roster.json'); C = load('line_class.json'); V = load('versions.json')
COV = S.pop('_coverage')
CF = CONFIG; LOOP = CF['all_termini_are_loops']
AREAS = CF['areas']; AID = {a['id']: a for a in AREAS}
OST = json.load(open(rel(CF['other_sheets']['ostrava']['derived']), encoding='utf-8')) if 'ostrava' in CF['other_sheets'] else dict(branches={}, roster={})

# ---------------------------------------------------------------- pak objects
PAK = CF['pak']
installed = {}
for f in [x for pk in PAK.get('packages', [PAK['package']]) for x in glob.glob(os.path.join(PAK['repo'], 'build', pk, '*.dat'))]:
    t = open(f, encoding='utf-8', errors='replace').read()
    for m in re.finditer(r'(?im)^name=(\S+)\s*$', t):
        ln = re.search(r'(?im)^length=(\d+)', t[m.end():])
        installed[m.group(1)] = int(ln.group(1)) if ln else 8
def pak_of(v, L=None):
    if PAK.get('rules'):
        # config pak.rules: [areas ('*', 'regional', 'mhd' or ids), type substring, paint substring, object]; first match wins;
        # an object starting with '~' is a stand-in (another paint or body), listed in pak_request.md
        ar = AID[C[L]['areas'][0]] if L in C else None
        for areas, ty, pt, obj in PAK['rules']:
            if areas != '*' and not (ar and (areas == ar.get('kind') or (isinstance(areas, list) and ar['id'] in areas))): continue
            # the type text includes a trolleybus's auxiliary drive (alt: 'battery', 'diesel generator'), so '32 Tr battery' picks its object
            if ty.lower() not in f"{v.get('type')} {v.get('full')} {v.get('alt', '')}".lower() or pt.lower() not in (v.get('paint') or '').lower(): continue
            sub = obj.startswith('~'); name = obj.lstrip('~'); parts = name.split('-')
            core, liv = parts[-1], parts[-2]
            if name in installed and not sub: return dict(obj=name, core=core, liv=liv, ok=True, length=installed[name])
            return dict(obj=name if name in installed else None, core=core, liv=liv, ok=False, length=installed.get(name), want=f"{v.get('type')} in {v.get('paint')}")
        return dict(obj=None, core='?', liv='?', ok=False, length=None, want=f"{v.get('type')} in {v.get('paint')}")
    core = PAK['types'].get(v['type'])
    liv = PAK['special'].get(v['num']) or next((k for p, k in PAK['paints'] if p in (v.get('paint') or '')), '3csadbilozelena')
    if not core: return dict(obj=None, core='?', liv=liv, ok=False, length=None)
    name = f"VZ-ODIS-{core}-{liv}-{core}"
    if name in installed: return dict(obj=name, core=core, liv=liv, ok=True, length=installed[name])
    alt = next((n for n in installed if n.startswith(f"VZ-ODIS-{core}-")), None)
    return dict(obj=alt, core=core, liv=(alt.split('-')[3] if alt else liv), ok=False, length=installed.get(alt), want=name)

def short_stop(s):
    return s
def slot_clock(P, r):
    """the real departures a typed value stands for: the minute for intervals dividing 60; the clock times of the day for
    every 240 or longer; the afternoon's (12:00-20:00) for shorter odd intervals"""
    if 60 % P == 0: return ':%02d' % (r % 60)
    ts = sorted(t % 1440 for t in range(r, r + 1440, P))
    if P >= 240: return ' · '.join(hm(t) for t in ts)
    return ' · '.join(hm(t) for t in ts if 720 <= t < 1200) + ' …'
def slots_text(P, R_):
    if 60 % P == 0: return ' '.join(':%02d' % m for m in sorted({x % 60 for r in R_ for x in range(r, r + 60, P)}))
    return ', '.join(hm(t) for t in sorted(t % 1440 for r in R_ for t in range(r, r + 1440, P)))

def vcell(v, kind, L=None):
    p = pak_of(v, L)
    cls = {'seen': 'v seen', 'designed': 'v added', 'nn': 'v spare'}[kind]
    paks = (f'<span class="pak">{E(p["core"])} · {E(p["liv"])}</span>' if p['ok'] else
            f'<span class="pak subst">≈ {E(p["core"])} · {E(p["liv"])} <em>(no {E(v["type"])} object in this paint)</em></span>')
    why = ''
    if kind == 'seen': why = f'<span class="addn" style="color:var(--ok)">seen on {E(v["seen"])}</span>'
    elif kind == 'designed': why = f'<span class="addn">{E(v["why"])}</span>'
    elif kind == 'nn': why = f'<span class="addn">not needed here: seen on {E(v["seen"])}' + (f'; counted on {E(v["elsewhere"])}' if v.get('elsewhere') else '') + '</span>'
    ln = 'midibus' if 'Dekstra' in v['type'] else v['len']     # the register list gives the Dekstra LE 37 L as 12 m; it is a midibus
    return (f'<li class="{cls}"><span class="num veh" data-v="{E(v["num"])}"><b>{E(v["num"])}</b> · {E(v.get("branch") or "")}</span>'
            f'<span class="vt">{E(v["full"])}{(" + " + E(v["alt"])) if v.get("alt") else ""} · {E(ln)} <span class="pak">({E(v["plate"])})</span></span>{paks}{why}</li>')

# ---------------------------------------------------------------- per line card
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
            # evenly spaced slots are typed as the plain interval (owner rule: "every 60, Offset 17, Also at 47" is every 30);
            # the same typed value reduced mod the shorter interval (fold added 25 Oct 2026)
            P_ = P // len(rs_); sets = [sets[0] % P_]
        reals = [((v + 60 + (1 if LOOP else 0)) % P_) for v in sets]
        off = f'<span class="sv">{sets[0]}</span><small class="real">{slot_clock(P_, reals[0])}</small>'
        also = ' '.join(f'<span class="sv">{v}</span><small class="real">{slot_clock(P_, r)}</small>' for v, r in zip(sets[1:], reals[1:])) or '–'
        st = g['stat']; win = g['window']
        fit = f"{st['exact']} of {st['n']} real departures on the minute, {st['w3']} within 3 min; {g['rt']} min to {E(g['to'].split(', ')[-1])}"
        if g.get('knot'): fit += f"; timed at the terminal so the bus passes {E(g['knot']['stop'])} at {', '.join(slot_clock(P, r) for r in g['knot']['at'])} ({g['knot']['rt']} min on)"
        if g.get('joint'): fit += f"; set {g['joint']['moved']} min off its best fit ({slot_clock(P, g['joint']['fit'])}) so the buses turn in the shortest round"
        chk = ''
        if win['empty']: chk += f'<small>window slot without a real departure: {", ".join(hm(t) for t in win["empty"])}</small>'
        if P_ != P: fit += f"; written as every {P_}: its {P // P_} slots of the every-{P} line are evenly spaced"
        rows.append(f'<tr{" class=chk" if win["empty"] else ""}><td>{stop}</td><td class="n sv">{P_}</td><td class="n">{off}</td><td>{also}</td><td class="fit">{fit}{chk}</td></tr>')
    return ''.join(rows)

def day_line(g, P):
    """the leg's own real departures over the whole day, at the terminal, marked against the slots"""
    out = []
    kn = g.get('knot')
    for t in sorted(g.get('trips', []), key=lambda t: t['d']):
        if not 300 <= t['d'] < 1380: continue
        # a trip read at the knot that does not start at the terminal: its real time at the knot, not a made-up terminal time
        lab = (f"[{kn['stop'].split(', ')[-1] if kn['stop'].count(',') > 1 else kn['stop']} {hm(t['dk'])}]" if kn and t['fr0'] != g['fr'] else hm(t['d']))               + ('' if t['line'] == g['lines'][0] else f" ({t['line']})")
        if t['dev'] == 0: out.append(f'<b>{lab}</b>')
        elif t['dev'] <= 3: out.append(f'{lab}<sup>±{t["dev"]}</sup>')
        else: out.append(f'<span class="warn">{lab}<sup>{t["dev"]}</sup></span>')
    return ' '.join(out)

def knot_text(g):
    out = []
    for k in g.get('knots', []):
        if not k['model']: continue
        ds = [d for d in k['dev'] if d is not None]
        worst = max(ds) if ds else None
        out.append(f"{E(k['stop'])} {', '.join(hm(t) for t in k['model'][:4])}" + (f" (real within {worst} min)" if worst is not None else ''))
    return '; '.join(out)

OW = load('offwire.json')['lines'] if os.path.exists(rel('data/derived/offwire.json')) else {}
def wire_block(L):
    """off-wire stretches per direction (authoring/offwire.py of the sheet: OSM route relation against the OSM wire)"""
    if L not in OW: return ''
    rows = ''.join(f'<tr><td>{E(p["o"])} <span class="arr">→ {E(p["d"])}</span></td><td class="n">{p["km"]:g} km</td><td>'
                   + ('; '.join(f'{E(a)} → {E(b)} ({w:g} km)' for a, b, k, w in p['stretches']) or 'none: under the wire all the way') + '</td></tr>'
                   for p in OW[L])
    return (f'<div class="sched"><h4>Overhead wire</h4><div class="tw0"><table class="st2"><thead><tr><th>Direction</th><th class="n">Route</th>'
            f'<th>Without wire (battery or diesel generator)</th></tr></thead><tbody>{rows}</tbody></table></div></div>')

checks = []
def card(L):
    x = S[L]; c = C[L]; ros = {r['name']: r for r in R['lines'].get(L, [])}
    need = sum(s['need'] for s in x['sim'])
    an = x['anchor']
    ar = ', '.join(AID[a]['name'] for a in x['areas'])
    head = (f'<header><a class="badge" href="#l-{L}">{L}</a><div class="hd"><h3>{E(c["name"])}</h3>'
            f'<p>{E(ar)} · licence {", ".join(c["lics"])} · {c["trips"]} trips on the day, {c["first"]}–{c["last"]} · modelled at {hm(an["anchor"])}'
            + (f' (busiest {hm(an["busiest"][0])}–{hm(an["busiest"][1])})' if an.get('busiest') and an.get('moved') else '') + '</p></div>'
            f'<div class="cnt"><b>{need}</b><span>{"trolleybuses" if c.get("traction") == "T" else "buses"} needed</span></div></header>')
    body = f'<p class="lnote">{E(x["note"])}</p>' if x.get('note') else ''
    if x.get('core'): body += f'<p class="lnote"><b>Core points:</b> {" · ".join(E(s) for s in x["core"])}</p>'
    for s in x['sim']:
        P = s['every']; r = ros.get(s['name'], {})
        body += (f'<div class="sched"><h4>Simutrans line {E(s["name"])} · every {P} min · {s["need"]} {"trolley" if c.get("traction") == "T" else ""}bus{"es" if s["need"] != 1 else ""}</h4>'
                 f'<div class="tw0"><table class="st2"><thead><tr><th>Entry</th><th class="n">Every</th><th class="n">Offset</th><th>Also at</th><th>Fit</th></tr></thead><tbody>{leg_rows(s)}</tbody></table></div>')
        dets = []
        for g in s['legs']:
            if g['untimed']: continue
            kt = knot_text(g)
            dets.append(f'<p><b>{E(g["fr"].split(", ")[-1])} →</b> real departures, whole day (at the terminal; bold = on the minute, orange = off the pattern, min off in superscript'
                        + (f'; [brackets] = a trip that starts beyond the terminal, at its time at {E(g["knot"]["stop"])}' if g.get('knot') else '') + f'): {day_line(g, P)}</p>'
                        + (f'<p class="win">Passes: {kt}</p>' if kt else '')
                        + f'<p class="win">Stops: {" – ".join(E(z) for z in g["stops"])}</p>')
            if g['window']['empty'] or any(t['dev'] > 3 and s['window'][0] <= t['d'] < s['window'][1] for t in g.get('trips', [])):
                checks.append((L, s['name'], g, s))
        waits = '; '.join(f"{E(k.split(', ')[-1] if isinstance(k, str) else k)} {', '.join(str(w) for w in v)} min" for k, v in s['waits'].items())
        body += f'<p class="need">Window {hm(s["window"][0])}–{hm(s["window"][1])}. Buses: {s["need"]}, following each bus round the slots with the real running times (waits at the terminals: {waits}).</p>'
        body += f'<details><summary>Whole day and stops</summary>{"".join(dets)}</details></div>'
        vs = ''.join(vcell(v, 'seen', L) for v in r.get('seen', [])) + ''.join(vcell(v, 'designed', L) for v in r.get('designed', []))
        body += f'<p class="brsub">Buses on {E(s["name"])}</p><ul class="vs">{vs}</ul>'
        if r.get('not_needed'):
            body += f'<details class="nn"><summary>{len(r["not_needed"])} more seen, not needed on {E(s["name"])}</summary><ul class="vs">{"".join(vcell(v, "nn", L) for v in r["not_needed"])}</ul></details>'
    return f'<article class="card" id="l-{L}">{head}{body}{wire_block(L)}</article>'

# ---------------------------------------------------------------- sections
def area_lines(aid):
    """lines of an area: modelled here, on the Ostrava sheet, not modelled (553 goes with Orlovsko, its larger part)"""
    home = CF.get('area_home', {'553': 'orlovsko'})
    mod = [L for L in S if aid in S[L]['areas'] and home.get(L, aid) == aid]
    ost = [L for k_, v_ in CF['other_sheets'].items() for L in v_.get('lines', []) if L in C and aid in C[L]['areas']]
    un = [L for L in C if aid in C[L]['areas'] and L not in S and L not in ost]
    return sorted(mod, key=int), sorted(ost, key=int), sorted(un, key=int)

def ost_card(L):
    b = OST['branches'].get(L, {}).get('branches', [])
    ro = OST['roster'].get(L, [])
    sims = ', '.join(f"{E(x.get('name', L))} ({x.get('need', '?')})" for x in b)
    buses = ', '.join(f'<span class="veh" data-v="{E(n)}">{E(n)}</span> {E(u[0])}' for u in ro for n in u[1])
    return (f'<tr><td><a class="badge sm" href="{E(CF["other_sheets"]["ostrava"]["url"])}">{L}</a></td><td>{E(C[L]["name"])}</td>'
            f'<td>{sims}</td><td>{buses}</td></tr>')

OTH = {k: (json.load(open(rel(v['derived']), encoding='utf-8')), json.load(open(rel(v['schedule']), encoding='utf-8')))
       for k, v in CF['other_sheets'].items() if v.get('lines') and v.get('schedule') and v.get('derived')}
def other_card(k, L):
    if k == 'ostrava': return ost_card(L)
    if k not in OTH:      # a sibling sheet built in parallel: linked, its Simutrans lines and buses are there
        sh = CF['other_sheets'][k]
        return (f'<tr><td><a class="badge sm" href="{E(sh.get("url") or "#")}">{L}</a></td><td>{E(C[L]["name"])}</td>'
                f'<td colspan="2">modelled on the {E(sh["label"])} sheet</td></tr>')
    r, s_ = OTH[k]
    sims = ', '.join(f"{E(x['name'])} ({x['need']})" for x in s_[L]['sim'])
    buses = ', '.join(f'<span class="veh" data-v="{E(v["num"])}">{E(v["num"])}</span> {E(v["full"])}' for x in r['lines'].get(L, []) for v in x['seen'] + x['designed'])
    return (f'<tr><td><a class="badge sm" href="{E(CF["other_sheets"][k]["url"])}">{L}</a></td><td>{E(C[L]["name"])}</td>'
            f'<td>{sims}</td><td>{buses}</td></tr>')

def unmod_row(L):
    why = CF['unmodelled'].get(L, '')
    c = C[L]
    return f'<tr><td><span class="badge sm" style="background:var(--muted)">{L}</span></td><td>{E(c["name"])}</td><td>{c["trips"]} trips{(", " + c["first"] + "–" + c["last"]) if c["first"] else ""}</td><td>{E(why)}</td></tr>'

LIVE = json.load(open(os.path.join(rel('data/raw/' + CF['snapshot']), 'live_compact.json'), encoding='utf-8'))['plates']
def on_road(lines, T0=960):
    lic = {x for L in lines for x in C[L]['lics']}
    return len({pl for pl, rows in LIVE.items() for f, l, li, line, sp, br in rows if li in lic and f <= T0 <= l})
areas_html = ''; nav = []; areanav = []
tot_need = 0; tot_seen = 0; tot_des = 0
for a in AREAS:
    mod, ost, un = area_lines(a['id'])
    need = sum(s['need'] for L in mod for s in S[L]['sim'])
    seen = sum(len(r['seen']) for L in mod for r in R['lines'].get(L, []))
    des = sum(len(r['designed']) for L in mod for r in R['lines'].get(L, []))
    tot_need += need; tot_seen += seen; tot_des += des
    nsim = sum(len(S[L]['sim']) for L in mod)
    areanav.append(f'<a href="#a-{a["id"]}">{E(a["name"])} <b>{need}</b></a>')
    nav += [f'<a class="badge sm" href="#l-{L}">{L}</a>' for L in mod]
    areas_html += (f'<h2 class="town" id="a-{a["id"]}">{E(a["name"])}</h2><p class="townsub">{E(a.get("licences", "Licences " + a["prefix"] + "xxx"))}, {E(a.get("operator", "Transdev Slezsko"))} {E(a["depot"])}{(" (fleet numbers " + ", ".join(p + "-" for p in a["fleet"]) + ")") if a["fleet"] else ""}. '
                   f'{len(mod)} lines on this sheet as {nsim} Simutrans lines, {need} buses: {seen} seen on the ODIS live map, {des} designed. '
                   f'At 16:00 {E(a.get("operator_short") or a.get("operator", "Transdev Slezsko").split()[0])} had {on_road(mod)} {"trolleybuses" if a.get("traction") == "T" else "buses"} on the road on these lines: the real buses swap lines at the terminals, while each Simutrans line here has its own (pooling would be the owner’s choice).'
                   + (' 553 is here with its Orlovsko licence; its Karvinsko licence (873553) is the same line.' if a['id'] == 'orlovsko' else '')
                   + (' 553 (licence 873553) is with Orlovsko.' if a['id'] == 'karvinsko' else '') + (' ' + E(a['note']) if a.get('note') else '') + '</p>')
    areas_html += '<div class="grid">' + ''.join(card(L) for L in mod) + '</div>'
    for k, sh in CF['other_sheets'].items():
        ls = [L for L in ost if L in sh.get('lines', [])]
        if not ls: continue
        head, why = (('On the Ostrava sheet', f'These {a["name"]} lines stop at Ostrava, Hranečník and are modelled, with their buses, on the '
                      f'<a href="{E(sh["url"])}">Ostrava bus sheet</a> (section All lines at Hranečník). They are not repeated here, and no bus is on both sheets.')
                     if k == 'ostrava' else (sh.get('heading', 'On the ' + sh['label'] + ' sheet'), E(sh.get('why', '')) + f' <a href="{E(sh["url"])}">{E(sh["label"])}</a>.'))
        areas_html += (f'<h3 style="margin-top:22px">{E(head)}</h3><p class="townsub">{why}</p>'
                       f'<div class="types"><table class="tlist"><thead><tr><th>Line</th><th>Route</th><th>Simutrans lines (buses)</th><th>Buses there</th></tr></thead><tbody>{"".join(other_card(k, L) for L in ls)}</tbody></table></div>')
    if un:
        areas_html += (f'<h3 style="margin-top:22px">Not modelled</h3><p class="townsub">{E(CF.get("texts", {}).get("unmodelled_intro", "Shift lines and sparse lines whose stops other lines already serve (method Step 8: a long-interval line only where it is a place’s only service), and lines with no trips on the day."))}</p>'
                       f'<div class="types"><table class="tlist"><thead><tr><th>Line</th><th>Route</th><th>On the day</th><th>Why</th></tr></thead><tbody>{"".join(unmod_row(L) for L in un)}</tbody></table></div>')

# ---------------------------------------------------------------- to check
chk_rows = ''.join(f'<tr class="chk"><td><a class="badge sm" href="#l-{L.split()[0]}">{L.split()[0]}</a></td><td colspan="2"><b>Chosen here, to confirm{" (" + E(L) + ")" if " " in L else ""}:</b> {E(t)}</td><td colspan="2"><b>Alternative:</b> {E(alt)}</td></tr>'
                   for L, t, alt in CF.get('owner_checks', []))
for L, name, g, s in checks:
    P = s['every']; W = s['window']
    off = [t for t in g['trips'] if t['dev'] > 3 and W[0] <= t['d'] < W[1]]
    chk_rows += (f'<tr><td><a class="badge sm" href="#l-{L}">{L}</a></td><td>{E(name)}</td><td>{E(g["fr"])} → {E(g["to"].split(", ")[-1])}</td>'
                 f'<td>every {P} at {slot_clock(P, g["real"][0]) if len(g["real"]) == 1 else ", ".join(slot_clock(P, r) for r in g["real"])}</td><td>' + ('; '.join(
                     ([f"slot {hm(t)} has no real departure" for t in g['window']['empty']]) + [f"{hm(t['d'])} is {t['dev']} min off" for t in off])) + '</td></tr>')

# ---------------------------------------------------------------- depots, types, pak
units = []   # (branch, line, sim name, vehicle, kind)
for L, rs in R['lines'].items():
    for r in rs:
        for v in r['seen']: units.append((v.get('branch') or '?', L, r['name'], v, 'seen'))
        for v in r['designed']: units.append((v.get('branch') or '?', L, r['name'], v, 'designed'))
dep = collections.defaultdict(list)
for u in units: dep[u[0]].append(u)
dep_html = ''; depnav = []
for b in sorted(dep, key=lambda b: (-len(dep[b]), b)):
    key = re.sub(r'\W+', '', b.lower())
    depnav.append(f'<a href="#d-{key}" data-dep="{key}">{E(b)} <b>{len(dep[b])}</b></a>')
    bytype = collections.defaultdict(list)
    for u in dep[b]: bytype[u[3]['full']].append(u)
    rows = ''
    for ty, us in sorted(bytype.items(), key=lambda x: -len(x[1])):
        rows += (f'<div class="dl"><span class="dc">{len(us)}</span><span></span><div><p class="mixline">{E(ty)}</p><ul class="vs">'
                 + ''.join(f'<li class="v {"seen" if k == "seen" else "added"}"><span class="num veh" data-v="{E(v["num"])}"><b>{E(v["num"])}</b> · line {E(nm_)}</span><span class="pak">{E(pak_of(v, L)["core"])} · {E(pak_of(v, L)["liv"])}</span></li>' for _, L, nm_, v, k in sorted(us, key=lambda u: u[3]['num']))
                 + '</ul></div></div>')
    dep_html += f'<div class="depot" id="d-{key}" data-depot="{key}"><header><h3>{E(b)}<small>{"garage" if b.startswith("ARRIVA") else "provozovna"}</small></h3><b class="core">{len(dep[b])}</b></header>{rows}</div>'

pk = collections.Counter(); pinfo = {}
for _, L, nm_, v, k in units:
    p = pak_of(v, L); key = (v['full'], v.get('paint', ''), p['obj'] or p.get('want'))
    pk[key] += 1; pinfo[key] = (p, v)
pak_rows = ''.join(f'<tr><td>{E(t)}<br><span class="pak">{E(paint)}</span></td><td class="mono">{"" if pinfo[k][0]["ok"] else "≈ "}{E(o or "none")}</td><td>{E(pinfo[k][0]["liv"])}</td><td class="n">{pinfo[k][0]["length"] or ""}</td><td class="n">{n}</td></tr>'
                   for k, n in sorted(pk.items(), key=lambda x: -x[1]) for t, paint, o in [k])
miss = [k for k in pk if not pinfo[k][0]['ok']]
open(os.path.join(ROOT, 'pak_request.md'), 'w', encoding='utf-8').write(
    f'# Pak requests from the {CF.get("title", "ODIS regional sheet (Havířovsko, Karvinsko, Orlovsko)")} sheet\n\n' +
    ('\n'.join(f'- {k[0]} in "{k[1]}": wanted {pinfo[k][0].get("want")}, used {k[2] or "nothing"}' for k in miss) if miss else 'None: every bus has its exact pak object.\n'))

tys = collections.defaultdict(collections.Counter)
for b, L, nm_, v, k in units: tys[(v['full'], 'midibus' if 'Dekstra' in v['type'] else v['len'])][b] += 1
branches = sorted(dep, key=lambda b: (-len(dep[b]), b))
type_rows = ''.join(f'<tr><td>{E(t)}</td><td class="n">{E(l)}</td>' + ''.join(f'<td class="n">{cnt.get(b, "") }</td>' for b in branches) + f'<td class="n">{sum(cnt.values())}</td></tr>'
                    for (t, l), cnt in sorted(tys.items(), key=lambda x: -sum(x[1].values())))

# ---------------------------------------------------------------- coverage
cov_html = (f'<h2 id="coverage">Coverage</h2><p class="sub">Every stop that this sheet\'s lines serve in 13:00–19:00 on {E(CF["vehicle_day_label_en"])} is on a modelled Simutrans line '
            f'(owner, 20 Oct 2026: "501 is the only line running to Dětmarovice, how can we not model that?"). {COV["served"]} stops: {COV["here"]} on this sheet\'s Simutrans lines, '
            f'{len(COV["elsewhere"])} on lines of the other sheets, {len(COV["uncovered"])} uncovered.</p>')
if COV['uncovered']:
    cov_html += '<div class="types"><table class="tlist"><tbody>' + ''.join(f'<tr><td>{E(s)}</td><td>{", ".join(v["lines"])}</td><td>{E(v["why"])}</td></tr>' for s, v in COV['uncovered'].items()) + '</tbody></table></div>'
cov_html += ('<details><summary>Stops covered by the other sheets\' lines</summary><div class="types"><table class="tlist"><thead><tr><th>Stop</th><th>Served here by</th><th>Modelled on</th></tr></thead><tbody>'
             + ''.join(f'<tr><td>{E(s)}</td><td>{", ".join(COV["served_by"][s])}</td><td>{E("; ".join(w))}</td></tr>' for s, w in sorted(COV['elsewhere'].items())) + '</tbody></table></div></details>')

state = ''.join(f'<div class="st"><h4><span class="tag {k}">{"modelled" if k == "in" else "left out"}</span>{E(t)}</h4><p>{E(d)}</p></div>' for k, t, d in CF['network_state'])

nlines = len(S); nsim = sum(len(x['sim']) for x in S.values())
style = open(os.path.join(HOME, 'templates', 'style.html'), encoding='utf-8').read().replace('{{TITLE}}', E(CF['title']))
page = f'''{style}
<header class="top">
  <div style="flex:1;min-width:min(100%,420px)">
    <p class="eyebrow">{E(CF.get("texts", {}).get("eyebrow", "ODIS regional buses · Havířovsko · Karvinsko · Orlovsko · vypravenost"))} · {E(CF["vehicle_day_label_en"])}</p>
    <h1>{E(CF["title"])}</h1>
    <p class="lede">{E(CF.get("texts", {}).get("lede_who", "The ODIS regional bus lines of three contract areas run by Transdev Slezsko (Havířovsko, Karvinsko, Orlovsko)"))}, set as Simutrans lines with the owner's regional method: each line read over the whole day at its core points, a repeating interval, destination and shift variants on their own longer intervals (at most 480 min), timetables at the terminals worked back from the knots, every afternoon stop on a line, buses sized from the pattern. Buses are the ones seen on each line on the ODIS live map on {E(CF["vehicle_day_label_en"])}.</p>
  </div>
  <div class="stats">
    <div class="stat"><b>{tot_need}</b><span>buses needed</span></div>
    <div class="stat"><b>{tot_seen}</b><span>seen on the live map</span></div>
    <div class="stat"><b>{tot_des}</b><span>designed</span></div>
    <div class="stat"><b>{nlines}</b><span>lines modelled</span></div>
    <div class="stat"><b>{nsim}</b><span>Simutrans lines</span></div>
  </div>
</header>
<div class="controls">
  <nav class="nav lines" aria-label="Lines"><span class="lab">Lines</span>{"".join(nav)}</nav>
  <nav class="nav dnav" aria-label="Sections"><span class="lab">Areas</span>{"".join(areanav)}<span class="lab">Depots</span>{"".join(depnav)}<a href="#checks">To check</a><a href="#coverage">Coverage</a><a href="#pak">Pak128 objects</a><a href="#method">How this was built</a></nav>
  <input type="search" id="q" placeholder="Find vehicle, e.g. {E(CF.get("texts", {}).get("search_example", "51-1104"))}" aria-label="Find vehicle number"><span id="hits" aria-live="polite"></span>
</div>

<h2>Network state, {E(CF["network_state_label"])}</h2>
<p class="sub">What is in the model and what is left out, with the reason.</p>
<div class="state">{state}</div>
<div class="legend"><span>Each bus shows its fleet number and branch, full type and length (with its number plate), and pak128 core with livery. <b style="color:var(--ok)">Green border</b>: seen running this line on the live map that afternoon (the line's window first; the trip is named). <b style="color:var(--warn)">Dashed border</b>: designed, not seen in the window, with the reason. <b>Dimmed, dotted</b>: seen, not needed on this line.</span></div>

<h2>How to read the line cards</h2>
<p class="sub"><b>Typing the timetable.</b> Values go into the Scheduling tab of the terminal entry, with the calendar on: Departure every, Offset, Also at (at most 7). Offsets count from 01:00 and every terminal is set as a loop, so each value is (real departure − 61) mod interval; the real clock minute is under every value. A row with Every 0 has no timetable: the bus leaves on arrival.</p>
<p class="sub"><b>Core points and knots.</b> Each line was read over the whole operating day (5:00–23:00) at its core points: terminals, knots where variants split, shared hubs. A trip counts at the time it passes a core point, wherever it starts. Where a slot is defined at a knot, the terminal departure is the knot time minus the running time, and the knot gets no timetable.</p>
<p class="sub"><b>Variants.</b> Each destination, path or shift variant is its own Simutrans line on a longer interval (the save game's Ex4). Shift lines repeat every 480 (8 h), the longest interval allowed. Trips more than 3 min off every slot of the line are off the pattern and shown in orange.</p>
<p class="sub"><b>Buses needed.</b> One bus followed round the line's own slots with the real running times and at least 3 min at each terminal (less where the slots chain closer, as the real timetable turns). Real buses swap lines at {E(CF.get("texts", {}).get("swap_places", "Frýdek-Místek, Podlesí, Karviná and Lutyně"))} all afternoon, so per-line totals are higher than what Transdev runs; pooling lines would be the owner's choice and is not done.</p>

<h2 id="checks">To check</h2>
<p class="sub">First, {(["no", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve"] + [str(i) for i in range(13, 100)])[len(CF.get("owner_checks", []))]} choices made here that you may want to flip, each with its alternative. Then the Simutrans lines whose model window has a slot without a real departure, or a real departure more than 3 min off: mostly the real timetable is irregular there, and the card says why.</p>
<div class="types"><table class="tlist"><thead><tr><th>Line</th><th>Simutrans line</th><th>Entry</th><th>Pattern</th><th>In the window</th></tr></thead><tbody>{chk_rows}</tbody></table></div>

{areas_html}

{cov_html}

<h2 id="depots">Depots</h2>
<p class="sub">{E(CF.get("texts", {}).get("depots", "Transdev Slezsko branches (provozovny). A seen bus counts at the branch the live map reports for it; a designed bus at its home branch. Český Těšín (73-) buses also work Karvinsko lines."))}</p>
<div class="depots">{dep_html}</div>

<h2 id="pak">Pak128 objects</h2>
<p class="sub">{E(PAK["why"])} Objects are read from the installed pak ({E(", ".join(PAK.get("packages", [PAK["package"]])))}); “≈” marks a stand-in, listed in pak_request.md. Length is in car units (16 = one tile).</p>
<div class="types"><table><thead><tr><th>Real type and paint</th><th>Pak128 object</th><th>Livery</th><th class="n">Length</th><th class="n">Buses</th></tr></thead><tbody>{pak_rows}</tbody></table></div>

<h2 id="fleet">Vehicle types</h2>
<div class="types"><table><thead><tr><th>Vehicle type</th><th class="n">Length</th>{"".join(f'<th class="n">{E(b)}</th>' for b in branches)}<th class="n">On the sheet</th></tr></thead><tbody>{type_rows}</tbody></table></div>

<h2 id="method">How this was built</h2>
<div class="notes">
<p><b>Scope.</b> {E(CF.get("texts", {}).get("scope", "Transdev Slezsko licences with the area prefixes 912 (Havířovsko I and II), 873 (Karvinsko) and 874 (Orlovsko)"))} in the CIS JŘ bus export ({E(CF["jdf"]["export_label"])}), evaluated for {E(CF["vehicle_day_label_en"])} with the shared version rule. {E(CF.get("texts", {}).get("scope_check", "The prefixes match the live map (provozovna Havířov, Karviná, Orlová) and the register notes (provozní oblast Karvinsko …)."))} {len(C)} ODIS lines; {nlines} are modelled here, {sum(len(v.get("lines", [])) for v in CF["other_sheets"].values())} are on other sheets, the rest are listed with the reason.</p>
<p><b>Method.</b> pipeline/bus-schedule-method.md (v3, the owner's regional rules of 20 Oct 2026): whole-day reading at core points, repeating interval, Ex4 variants, timing at terminals worked back from knots, no daily lines (at most every 480), every afternoon stop on a line, buses from the pattern, every line checked by hand. Each line's choices are in config.json → lines and in the README.</p>
<p><b>Buses.</b> The ODIS live map (mpvnet.cz) polled every minute 13:05–19:30 on {E(CF["vehicle_day_label_en"])} by the Havířov/Karviná/Orlová pipeline gives every bus's trips (licence and trip number), joined to fleet numbers by number plate (seznam-autobusu.cz register). A bus fills one Simutrans line it ran in that line's window, by matching. Buses already on another sheet ({E("; ".join(v["label"] for v in CF["other_sheets"].values()))}) are not used here.{E(CF.get("texts", {}).get("buses_extra", ""))}</p>
<p>Sources: <a href="https://portal.cisjr.cz/pub/jdf/JDF.zip">CIS JŘ bus JDF</a>, <a href="https://mapa.kodis.cz/">ODIS live map</a>, <a href="https://seznam-autobusu.cz/seznam?prov=1&amp;trakce=autobus&amp;iddopravce=28&amp;vcetneSluzebnich=1">Transdev Slezsko register</a>{CF.get("texts", {}).get("sources_extra", "")}.</p>
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
print('wrote', out, len(page), 'bytes;', tot_need, 'buses', tot_seen, 'seen', tot_des, 'designed;', len(checks), 'rows to check;', len(miss), 'pak stand-ins')
