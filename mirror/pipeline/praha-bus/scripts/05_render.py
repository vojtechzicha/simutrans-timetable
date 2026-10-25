"""Render the Prague bus sheet: data/derived/<state>/{gtfs_lines,compare,courses}.json + assets -> <project root>/<output_html>

Sections: game check (every game line against the current PID timetable, filterable to the lines to fix), network (every
PID bus line 100-299), pak128 objects, one card per line (routes, game comparison, Simutrans schedule, courses with
vehicles, PID stop lists), operators and garages, how it was built.
Vehicle cell (shared rule): 1) number · garage (other operators: operator · garage)  2) full type · length  3) pak core
with livery where the type has more than one; "requested" = the object is not in the pak yet (VZ pak session is making it).

Usage: python 05_render.py --state 2026-09-29
"""
import argparse, collections, html, os, re
from common import state, load, DER, ASSETS, PROJECT, RAW
import sticky

esc = html.escape
hm = lambda m: '%02d:%02d' % (m // 60 % 24, m % 60)
OPN = {'DPP': 'Dopravní podnik hlavního města Prahy', 'ARRIVA CITY': 'Arriva City', 'STENBUS': 'Stenbus', 'ABOUT ME': 'About Me',
       'ČSAD Střední Čechy': 'ČSAD Střední Čechy', 'MARTIN UHER': 'Martin Uher', 'ČSAD POLKOST': 'ČSAD Polkost', 'Vega Tour': 'Vega Tour',
       'ARRIVA STŘEDNÍ ČECHY': 'Arriva Střední Čechy', 'UMBRELLA CITY LINES': 'Umbrella City Lines', 'ČSAD Benešov': 'ČSAD Benešov',
       'ARANEA': 'Aranea', '?': 'operator not known'}
LIV = {'pidsedocervena': 'PID grey-red', 'pidcervenomodrobila': 'PID red-white-blue', 'dppcervenobila': 'DPP red-white',
       'mestskacervenobila': 'city red-white', 'veoliacervenoseda': 'Veolia red-grey', 'bila': 'white', 'tyrkysovozluta': 'turquoise-yellow', 'fashionarena': 'Fashion Arena wrap', 'dppcervena': 'DPP coach red'}
CLASSES = [('ART', 'Articulated', '18 m'), ('LONG', 'Long', '13.5–15 m'), ('STD', 'Standard', '12–13 m'),
           ('MIDI', 'Midibus', '9–11 m'), ('MINI', 'Minibus', 'under 9 m'), ('UNK', 'Not known', '')]
CN = {k: n for k, n, _ in CLASSES}

def ucls(length):
    if not length: return 'UNK'
    if length >= 17: return 'ART'
    if length >= 13.5: return 'LONG'
    if length >= 11.5: return 'STD'
    if length >= 9: return 'MIDI'
    return 'MINI'

def gtfs_op(name):
    n = re.sub(r',?\s*(akciová společnost|a\.\s?s\.|spol\. s r\.\s?o\.|s\.\s?r\.\s?o\.)\s*$', '', name.replace(' ,', ',')).strip(' ,')
    return {'Dopravní podnik hl. m. Prahy': 'Dopravní podnik hlavního města Prahy'}.get(n, n)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--state', required=True)
    s = state(ap.parse_args().state)
    G = load(os.path.join(DER, s['name'], 'gtfs_lines.json')); P = G['lines']
    CMP = load(os.path.join(DER, s['name'], 'compare.json'))
    CO = load(os.path.join(DER, s['name'], 'courses.json'))
    OBJ = load(os.path.join(ASSETS, 'pak_objects.json'))
    GAME = load(os.path.join(RAW, 'game', s['game_raw'], 'lines.json'))
    bus = [L for L, p in P.items() if p['route_type'] == '3']
    game_by = collections.defaultdict(list)
    for r in CMP['lines']: game_by[r['pid']].append(r)
    courses = collections.defaultdict(list)
    for c in CO['courses']: courses[c['line']].append(c)
    vd = CO['vehicle_date']

    # livery shown in the core only where a type has more than one livery object (pak or requested)
    livs = collections.defaultdict(set)
    for c in CO['courses']:
        for ch in c['chain']:
            for x in ch['cars']:
                if x['pak']: livs[(x['operator'] == 'DPP', x['pak']['core'])].add(x['pak']['livery'])

    def core_html(x):
        pk = x['pak']
        if not pk: return '<b class="bad">no object: vehicle not in the register</b>'
        multi = len(livs[(x['operator'] == 'DPP', pk['core'])]) > 1 or pk['mapped']
        txt = f'<code>{esc(pk["core"])}</code>' + (f' {esc(LIV.get(pk["livery"], pk["livery"]))}' if multi else '')
        if pk['mapped']: txt += f' <span class="mp">({esc(pk["mapped"])} → normal livery)</span>'
        if pk['status'] != 'in pak': txt += '<span class="rq">requested</span>'
        return txt

    def unit_html(x, designed=False):
        cl = ucls(x['length'])
        op = '' if x['operator'] == 'DPP' else OPN.get(x['operator'], x['operator'].title())
        where = ' · '.join(w for w in (op, x['garage']) if w and w != '?')
        if designed and not x.get('num'):
            first = f'<span class="ds">designed, not recorded</span>' + (f' <span class="dp">· {esc(where)}</span>' if where else '')
        else:
            first = f'<span class="veh" data-v="{esc(x["num"])}">{esc(x["num"])}' + (f' <span class="dp">· {esc(where)}</span>' if where else '') + '</span>'
        ln = f' · {x["length"]:g} m' if x['length'] else ''
        typ = x['type'] if x['type'] != '?' else 'type not known'
        return f'<div class="unit u-{cl}">{first}<span class="vt">{esc(typ)}{ln}</span><span class="pk">{core_html(x)}</span></div>'

    MONTHS = ['', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    hist_any = {c['line']: True for c in CO['courses'] if c['source'] == 'designed' and c.get('why') == 'history'}
    def counted(L):
        return [c for c in courses.get(L, []) if not c['am_only']]

    # ---------- game comparison ----------
    def half_html(h):
        bits = []
        if h['missing']: bits.append('<span class="miss">missing in the game: ' + esc(', '.join(h['missing'])) + '</span>')
        if h['extra']: bits.append('<span class="xtra">extra in the game: ' + esc(', '.join(h['extra'])) + '</span>')
        if h['replaced']: bits.append('<span class="repl">in place of the PID stop: ' + esc('; '.join(f'{a} instead of {b}' for a, b in h['replaced'])) + '</span>')
        if not h['order_ok']: bits.append('<span class="miss">stops in a different order</span>')
        ok = not bits
        return (f'<div class="half"><b>{esc(h["pattern"])}</b> · game {h["game_stops"]} stops, PID {h["pid_stops"]} · '
                + ('<span class="chip st-ok">same stops</span>' if ok else '<br>' + '<br>'.join(bits)) + '</div>')

    def game_status(r):
        chips = []
        if not r['convoys']: chips.append('<span class="chip st-bad">no vehicles</span>')
        if r['status'] == 'aligned': chips.append('<span class="chip st-ok">stops match</span>')
        elif r['status'] == 'stops differ': chips.append('<span class="chip st-bad">stops differ</span>')
        else: chips.append(f'<span class="chip st-warn">{esc(r["status"])}</span>')
        if r.get('name_fixes'): chips.append(f'<span class="chip st-info">{len(r["name_fixes"])} stop name{"s" if len(r["name_fixes"]) > 1 else ""} to fix</span>')
        return ''.join(chips)

    def needs_fix(r):
        return (not r['convoys']) or r['status'] != 'aligned'

    def diff_summary(r):
        if not r.get('halves'): return esc(r['status'])
        n = lambda k: sum(len(h[k]) for h in r['halves'])
        parts = []
        if n('missing'): parts.append(f'{n("missing")} missing')
        if n('extra'): parts.append(f'{n("extra")} extra')
        if n('replaced'): parts.append(f'{n("replaced")} in place of another')
        if not all(h['order_ok'] for h in r['halves']): parts.append('order differs')
        if r.get('unknown_halts'): parts.append(f'{len(r["unknown_halts"])} halt{"s" if len(r["unknown_halts"]) > 1 else ""} not on the PID line')
        return ', '.join(parts) or 'same stops as PID'

    def game_block(L):
        rs = game_by.get(L, [])
        p = P[L]
        if not rs:
            if not p.get('peak'): return ''
            return '<div class="game"><h4>In the game</h4><p><span class="chip st-warn">not built</span> No game line has this number.</p></div>'
        out = []
        for r in sorted(rs, key=lambda r: (r['variant'], r['name'])):
            fx = ''
            if r.get('name_fixes'):
                fx = '<ul>' + ''.join(f'<li>stop name <code>{esc(a)}</code> → PID <b>{esc(b)}</b></li>' for a, b in r['name_fixes'].items()) + '</ul>'
            wl = f' · {r["wait_for_load"]} stop{"s" if r["wait_for_load"] != 1 else ""} wait for load' if r.get('wait_for_load') else ''
            halves = ''.join(half_html(h) for h in r.get('halves', []))
            out.append(f'<div class="gl">{esc(r["name"])}</div><div class="half">{game_status(r)} {r["convoys"]} bus{"es" if r["convoys"] != 1 else ""} · '
                       f'{r["stop_entries"]} stop entries on {r["unique_halts"]} halts · {r["waypoints"]} waypoints{wl}</div>{halves}{fx}')
        return '<div class="game"><h4>In the game</h4>' + ''.join(out) + '</div>'

    # ---------- schedule ----------
    def sched_block(L):
        p = P[L]; rows = []
        hand = p.get('schedule_rows')      # hand-set rows (state schedule_overrides, method check 25 Oct 2026) replace the main rows
        for m in (hand or p.get('main', [])):
            sc = m.get('schedule')
            if not sc: continue
            also = ', '.join(str(a) for a in sc['set'][1:]) or '—'
            real_o = f'<small class="real">real {sc["real"][0]}</small>'
            real_a = f'<small class="real">real {", ".join(str(x) for x in sc["real"][1:])}</small>' if len(sc['real']) > 1 else ''
            fit = (f'exact {hm(sc["first"])}–{hm(sc["last"])} ({sc["n"]} departures)' if sc['exact'] else f'approximate, up to {sc["max_dev"]} min off')
            if sc.get('override'):
                fit = (f'set by hand' + (', approximate' if sc.get('approx') else '') + (f', exact {hm(sc["first"])}–{hm(sc["last"])} ({sc["n"]} departures)' if sc['n'] >= 4 else '') +
                       (f', up to {sc["max_dev"]} min off in 15:00–17:59' if sc['max_dev'] else ', every 15:00–17:59 departure on a slot') +
                       f'<small>{esc(sc["override"])}</small>')
            if not p.get('peak'): fit += '<small>no trips in 15:00–17:59; fitted over the whole day</small>'
            rows.append(f'<tr><td>{esc(m["o"])} <span class="arr">→</span> {esc(m["d"])}<span class="lp">terminus · 1 min early</span></td>'
                        f'<td class="num sv">{sc["every"]}</td><td class="num sv">{sc["set"][0]}{real_o}</td><td class="sv">{esc(also)}{real_a}</td><td class="sv">auto</td><td class="fit">{fit}</td></tr>')
        if not rows: return ''
        others = [x for x in p.get('patterns', []) if not any(x['stops'] == m['stops'] for m in p['main'])]
        handod = {(m['o'], m['d']) for m in (hand or [])}
        pat = ''
        if others:
            pat = ('<details class="pats"><summary>Other stop patterns in 15:00–17:59 (' + str(len(others)) + ')</summary><ul>' +
                   ''.join(f'<li>{esc(x["o"])} → {esc(x["d"])}: {x["n"]} trip{"s" if x["n"] != 1 else ""} in the peak, {len(x["stops"])} stops'
                           + (' · its terminus entry is in the table above' if (x['o'], x['d']) in handod else ' · a peak trip: own Simutrans line' if x['n'] >= 3 else ' · not a peak trip, not modelled') + '</li>' for x in others) + '</ul></details>')
        odd = sorted({m['schedule']['every'] for m in (hand or p.get('main', [])) if m.get('schedule') and 60 % m['schedule']['every']})
        orig = (f' The fork counts offsets from 01:00, so on an interval that does not divide 60 (every {", ".join(map(str, odd))}) the typed value is (real − 60 − 1) mod the interval.' if odd else '')
        return (f'<div class="sch"><h4>Simutrans schedule</h4><p class="lpn">Buses turn at every terminus (loop, bus-station circuit or block), so Offset and Also at are set 1 min before the timetable departure, with the real minute under each value.{orig} Put the values on the departure stand.</p>'
                f'<div class="tw"><table class="st"><thead><tr><th>Terminus entry</th><th class="num">Departure every</th><th class="num">Offset</th><th>Also at</th><th>Leave up to</th><th>Fit</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div>{pat}</div>')

    def stops_block(L):
        p = P[L]
        cols = ''.join(f'<div><h5>{esc(m["o"])} → {esc(m["d"])} ({len(m["stops"])})</h5><ol>' + ''.join(f'<li>{esc(x)}</li>' for x in m['stops']) + '</ol></div>' for m in p.get('main', []))
        return f'<details class="stops"><summary>PID stops of the main patterns</summary><div class="pc">{cols}</div></details>' if cols else ''

    # ---------- line cards ----------
    cards, net_rows, nav = [], [], []
    per_class_total = collections.Counter()
    depot = collections.defaultdict(lambda: collections.defaultdict(list))
    pak_count = collections.Counter(); pak_info = {}
    for L in sorted(bus, key=int):
        p = P[L]
        rs = [m for m in p.get('main', [])]
        routes = ''.join(f'<li><b>{esc(m["o"])} → {esc(m["d"])}</b> <span class="muted">· ' + (f'every {m["headway"]} min · ' if m.get('headway') else '') +
                         (f'{m["runtime"]} min' if m.get('runtime') else '') + '</span></li>' for m in rs) or f'<li><b>{esc(p["long_name"])}</b></li>'
        ops = ', '.join(gtfs_op(o) for o in p['operators'])
        cs = sorted(courses.get(L, []), key=lambda c: bool(c.get('spare')))
        cnt = counted(L)
        mix = collections.Counter(ucls(x['length']) for c in cnt for x in c['chain'][-1]['cars'])
        per_class_total.update(mix)
        rows = []
        for c in cs:
            des = c['source'] == 'designed'; spare = c.get('spare')
            chain = '<div class="arr">then</div>'.join(''.join(unit_html(x, des) for x in ch['cars']) for ch in c['chain'])
            notes = []
            if c['split']: notes.append('Afternoon part of a split course; morning part ran ' + ', '.join(c['am']) + '.')
            if c['swap']: notes.append('Vehicle exchanged during the day, time not recorded: ' + ' → '.join(ch['set'] for ch in c['chain']) + '. The last one counts.')
            if c['am_only'] and not spare: notes.append('The same bus later replaced a vehicle on another course, so this course probably ends before the afternoon peak (not counted).')
            for ch in c['chain']:
                m = re.search(r'přejezd na linku (\d+)', ch['note'])
                if m: notes.append(f'Continues as line {m.group(1)} (přejezd na linku {m.group(1)}).')
            dd = lambda ds: ', '.join(f'{int(d[8:10])} {MONTHS[int(d[5:7])]} {d[:4]}' for d in ds)
            nlog = len([x for x in cnt if x['source'] != 'designed'])
            if des and c.get('why') == 'history':
                notes.append(f'{nlog} courses are logged against {p.get("need")} needed at 16:00. This bus ran line {L} on {dd(c["hist"])} '
                             f'and was not out anywhere in PID on {int(vd[8:])} Sep (day overview).')
            if des and c.get('why') == 'fleet':
                notes.append(f'{nlog} courses are logged against {p.get("need")} needed at 16:00, and the line history has no free car left'
                             f'{"" if hist_any.get(L) else " (no record of the line since January 2025)"}. A free active bus of the line\'s type from the operator, '
                             f'not out anywhere in PID on {int(vd[8:])} Sep.')
            if spare == 'surplus':
                notes.append(f'Logged on {int(c["source"][8:10])} Sep; not needed at 16:00 (the line needs {p.get("need")}). Not counted.')
            if spare == 'not needed':

                notes.append(f'In the line\'s history (last on {dd(c["hist"])}) and free on {int(vd[8:])} Sep, but not needed at 16:00. Not counted.')
            flag = ''
            if des: flag = '<span class="flag ds">designed, not recorded</span>'
            elif spare: flag = '<span class="flag am">not needed</span>'
            elif c['am_only']: flag = '<span class="flag am">not counted</span>'
            elif c['swap']: flag = '<span class="flag swap">swap</span>'
            if c['split']: flag += '<span class="flag pm">PM part</span>'
            src = '' if des or spare == 'not needed' or c['source'] == vd else f'<span class="src">logged {int(c["source"][8:10])} Sep</span> '
            rows.append(f'<tr class="{"sp" if spare else ("unc" if (des or c["am_only"] or c["swap"]) else "")}"><td class="k">{esc(c["course"] if not des else "")}</td><td class="v">{chain}</td>'
                        f'<td class="n">{flag}{src}<span class="nt">{esc(" ".join(notes))}</span></td></tr>')
            for k, ch in enumerate(c['chain'] if not spare else []):
                for x in ch['cars']:
                    key = ('DPP ' + (x['garage'] or 'garage not known')) if x['operator'] == 'DPP' else OPN.get(x['operator'], x['operator'])
                    depot[key][L].append(dict(x=x, course=c['course'], des=des, replaced=c['swap'] and k < len(c['chain']) - 1, am=c['am_only']))
            if not c['am_only']:
                for x in c['chain'][-1]['cars']:
                    if x['pak']:
                        kk = x['pak']['object']; pak_count[kk] += 1
                        pak_info[kk] = dict(pak=x['pak'], type=x['type'], length=x['length'], ops=pak_info.get(kk, {}).get('ops', set()) | {OPN.get(x['operator'], x['operator'])},
                                            mapped=pak_info.get(kk, {}).get('mapped', 0) + bool(x['pak']['mapped']))
        need = p.get('need')
        n = len(cnt)
        extra_note = ''
        nsur = sum(1 for c in cs if c.get('spare') == 'surplus')
        if nsur:
            extra_note = (f'<p class="callout info">{n + nsur} courses are logged against {need} needed at 16:00. {nsur} are marked “not needed” and dimmed at the '
                          'bottom. The counted buses keep one of every type on the line first, then the lowest course numbers. The records carry no times, '
                          'so morning-only or school courses cannot be picked out.</p>')
        how = 'by round trip' if (p.get('need_cycle') or 0) >= (p.get('need_on_road') or 0) else f'on the road at once over all patterns (the main round trip alone needs {p.get("need_cycle") or "fewer"})'
        needtxt = f'<span class="need">timetable at 16:00: {need} bus{"es" if need != 1 else ""} needed {how}{" (circular line)" if p.get("circular") else ""}</span>' if need else \
                  ('<span class="need">no trips in the afternoon peak</span>' if not p.get('peak') else '<span class="need">too few peak trips to size by round trip</span>')
        gr = game_by.get(L, [])
        gconv = sum(r['convoys'] for r in gr)
        mix_html = ' '.join(f'<span class="mx u-{k}"><b>{mix[k]}</b>× {CN[k]}</span>' for k, _, _ in CLASSES if mix[k])
        table = (f'<div class="tw"><table class="ct"><thead><tr><th>Course</th><th>Vehicle · garage / type · length / pak128 core</th><th>Notes</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div>'
                 if rows else '<p class="callout warn">No vehicle logged on this line on any fetched day.</p>' if p.get('peak') else '')
        cards.append(f'''
<article class="lc{' nopeak' if not p.get('peak') else ''}" id="l{L}">
  <header><a class="lb" href="#l{L}">{L}</a><div class="lh"><ul class="routes">{routes}</ul><span class="opn">{esc(ops)}</span>{needtxt}</div>
  <div class="cntx"><div class="cnt"><b>{n}</b><span>buses</span></div><div class="cnt"><b>{gconv if gr else '–'}</b><span>in game</span></div></div></header>
  <div class="mix">{mix_html}</div>{extra_note}
  {game_block(L)}
  {sched_block(L)}
  {stops_block(L)}
  {table}
</article>''')
        nav.append((f'#l{L}', L))
        hw = ' / '.join(str(m['headway']) for m in rs if m.get('headway')) or ('–' if p.get('peak') else 'no peak')
        rt = ' / '.join(str(m['runtime']) for m in rs if m.get('runtime'))
        gst = ''.join(game_status(r) for r in gr) if gr else ('<span class="chip st-warn">not built</span>' if p.get('peak') else '')
        net_rows.append(f'<tr><td><a class="lb sm" href="#l{L}">{L}</a></td><td>{esc(p["long_name"])}</td><td class="small">{esc(ops)}</td><td class="num">{hw}</td>'
                        f'<td class="num">{rt}</td><td class="num">{need or ""}</td><td class="num"><b>{n or ""}</b></td><td class="num">{gconv if gr else ""}</td><td>{gst}</td></tr>')

    # ---------- game check table ----------
    gc_rows = []; nfix = 0
    for r in sorted(CMP['lines'], key=lambda r: (int(r['pid']) if r['pid'].isdigit() else 999, r['variant'], r['name'])):
        fix = needs_fix(r); nfix += fix
        p = P.get(r['pid'])
        pst = ' / '.join(str(len(m['stops'])) for m in p.get('main', [])) if p else '–'
        link = f'<a class="lb sm" href="#l{r["pid"]}">{r["pid"]}</a>' if p and p['route_type'] == '3' else f'<span class="lb sm">{esc(r["pid"])}</span>'
        gc_rows.append(f'<tr class="{"fix" if fix else "ok"}"><td>{link}</td><td class="gn">{esc(r["name"])}</td><td class="num"><b>{r["convoys"]}</b></td>'
                       f'<td class="num">{r["stop_entries"]} / {r["unique_halts"]}</td><td class="num">{pst}</td><td>{game_status(r)}</td><td class="d">{diff_summary(r)}</td></tr>')
    absent = [a for a in CMP['absent_in_game'] if a['route_type'] == '3']
    for a in sorted(absent, key=lambda a: int(a['pid'])):
        p = P[a['pid']]
        pst = ' / '.join(str(len(m['stops'])) for m in p.get('main', []))
        cls = 'fix' if a.get('peak') else 'ok'
        nfix += cls == 'fix'
        gc_rows.append(f'<tr class="{cls}"><td><a class="lb sm" href="#l{a["pid"]}">{a["pid"]}</a></td><td class="gn muted">— {esc(a["long_name"])}</td><td class="num">–</td><td class="num">–</td>'
                       f'<td class="num">{pst}</td><td><span class="chip st-warn">not built</span></td><td class="d">'
                       + (f'PID runs {a["trips"]} trips on {G["service_date"][6:].lstrip("0")} Sep, {a["need"]} buses at 16:00.' if a.get('peak') and a.get('need') else
                          f'PID runs {a["trips"]} trips on {G["service_date"][6:].lstrip("0")} Sep, none in the afternoon peak.' if a['trips'] else 'no trips on the service date') + '</td></tr>')

    # ---------- garages and operators ----------
    dep_cards, dep_nav = [], []
    def dkey(k): return (not k.startswith('DPP'), k == 'DPP garage not known', -sum(len(v) for v in depot[k].values()))
    for D in sorted(depot, key=dkey):
        lines = depot[D]; n = 0; blocks = []
        mix = collections.Counter()
        for L in sorted(lines, key=int):
            units = []
            for it in sorted(lines[L], key=lambda it: (it['des'], it['course'])):
                real = not it['am'] and not it['replaced']
                if real: n += 1; mix[ucls(it['x']['length'])] += 1
                st = ' style="opacity:.6"' if not real else ''
                units.append(f'<div{st}>{unit_html(it["x"], it["des"])}</div>')
            blocks.append(f'<div class="vl"><a class="lb sm" href="#l{L}">{L}</a><div class="units">{"".join(units)}</div></div>')
        slug = re.sub(r'[^a-z0-9]+', '-', D.lower().encode('ascii', 'ignore').decode()).strip('-') or 'x'
        label = (('Garage ' + D[4:]) if D != 'DPP garage not known' else 'Garage not known') if D.startswith('DPP ') else D
        sub = 'Dopravní podnik hlavního města Prahy' if D.startswith('DPP ') else 'operator (all its garages)'
        mix_html = ' '.join(f'<span class="mx u-{k}"><b>{mix[k]}</b>× {CN[k]}</span>' for k, _, _ in CLASSES if mix[k])
        dep_cards.append(f'<article class="dc" id="d-{slug}"><header><div class="lh"><h3>{esc(label)}</h3><span class="opn">{esc(sub)}</span></div><div class="cnt"><b>{n}</b><span>buses</span></div></header>'
                         f'<div class="mix">{mix_html}</div>{"".join(blocks)}</article>')
        dep_nav.append((slug, D[4:] if D.startswith('DPP ') else D, n))

    # ---------- pak table ----------
    pak_rows = ''
    for kk, k in sorted(pak_count.items(), key=lambda kv: (not kv[0].startswith('VZ-DPPraha'), pak_info[kv[0]]['type'], -kv[1])):
        i = pak_info[kk]; pk = i['pak']
        chain = ' + '.join(f'<code>{esc(x)}</code>' for x in pk['chain'])
        st = '<span class="chip st-ok">in the pak</span>' if pk['status'] == 'in pak' else '<span class="chip st-warn">requested</span>'
        mp = f'<br><span class="muted small">{i["mapped"]} with an advert wrap or another livery, shown in this one</span>' if i['mapped'] else ''
        pak_rows += (f'<tr><td>{esc(i["type"])}</td><td>{esc(LIV.get(pk["livery"], pk["livery"]))}{mp}</td><td class="core">{esc(pk["core"])}</td><td class="chain">{chain}</td>'
                     f'<td>{esc(", ".join(sorted(i["ops"])))}</td><td>{st}</td><td class="num">{k}</td></tr>')
    n_req = sum(k for kk, k in pak_count.items() if pak_info[kk]['pak']['status'] != 'in pak')

    tot = sum(per_class_total.values())
    cls_rows = ''.join(f'<tr><td><span class="cls u-{k}">{esc(n)}</span></td><td>{esc(l)}</td><td class="num">{per_class_total[k]}</td></tr>' for k, n, l in CLASSES if per_class_total[k])
    ctrl = sticky.controls(nav, [(k, t, n) for k, t, n in dep_nav], [('#check', 'Game check'), ('#network', 'Network'), ('#pak', 'Pak128 objects')], '3012', 'Garages and operators')
    ctrl = ctrl.replace('<nav class="nav" aria-label="Lines">', '<nav class="nav lines" aria-label="Lines">', 1)
    head = open(os.path.join(ASSETS, 'page_head.html'), encoding='utf-8').read()
    gsrc = GAME['source']
    n_lines_game = len(CMP['lines'])
    n_zero = sum(1 for r in CMP['lines'] if not r['convoys'])
    n_diff = sum(1 for r in CMP['lines'] if r['status'] == 'stops differ')
    n_notpid = sum(1 for r in CMP['lines'] if r['status'].startswith('not in'))
    n_absent_peak = sum(1 for a in absent if a.get('peak'))
    body = f'''<title>{esc(s["title"])}</title>
{head}{sticky.CSS}
<header class="top">
  <div>
    <div class="eyebrow">Praha · autobusy MHD · linky 100–299 · hra proti jízdnímu řádu PID</div>
    <h1>{esc(s["title"])}</h1>
    <p class="lede">Every Prague city bus line (PID 100–299) against the save game. The game check below lists every game line with its buses and stops against the PID timetable of {int(G["service_date"][6:])} September 2026. It shows which lines have no vehicles, which serve other stops, and which PID lines are not built. Each line card then gives the timetable, the Simutrans schedule, the stops, and the buses that ran it on Friday {int(vd[8:])} September (seznam-autobusu.cz deployment records) with their liveries and pak128 objects, for DPP and every other operator alike. Companion to the Prague tram and trolleybus sheets.</p>
  </div>
  <div class="stats">
    <div class="stat"><b>{len(bus)}</b><span>PID bus lines</span></div>
    <div class="stat"><b>{n_lines_game}</b><span>game lines</span></div>
    <div class="stat"><b>{nfix}</b><span>to fix</span></div>
    <div class="stat"><b>{tot}</b><span>buses at peak</span></div>
  </div>
</header>
{ctrl}

<h2 id="check">Game check</h2>
<p class="lede" style="margin-bottom:6px">Save {esc(os.path.basename(gsrc["save_file"]))} (saved {esc(gsrc["save_file_mtime"][:16].replace("T", " "))}), exported with {esc(gsrc["exported_with"].split(",")[0])}. {n_lines_game} game lines are numbered 100100–100299: {n_zero} ha{"s" if n_zero == 1 else "ve"} no vehicles, {n_diff} serve stops that differ from PID, and {n_notpid} {"is" if n_notpid == 1 else "are"} no longer in the PID timetable. {len(absent)} PID bus lines have no game line, {n_absent_peak} of them with afternoon-peak trips. Stops: the game counts entries on its round trip and distinct halts; PID counts the stops of each direction's main pattern.</p>
<div class="filter"><label><input type="checkbox" id="onlyfix" checked> Only lines to fix ({nfix})</label><span class="muted small">To fix: no vehicles, stops that differ from PID, a line no longer in PID, or a PID line with peak trips that is not built. Stop names the game abbreviates are listed but do not count as a difference.</span></div>
<div class="tw sumt"><table class="gc onlyfix" id="gct"><thead><tr><th>Line</th><th>Game line</th><th class="num">Buses</th><th class="num">Game stops / halts</th><th class="num">PID stops</th><th>Status</th><th>Difference</th></tr></thead><tbody>{"".join(gc_rows)}</tbody></table></div>

<h2 id="network">Network</h2>
<p class="lede" style="margin-bottom:10px">Every PID bus line in 100–299 on {int(G["service_date"][6:])} September. Headway and runtime per main direction, in minutes (16:00–17:00). Needed = buses at 16:00 (round trip or on the road, the larger); Buses = counted courses on the sheet (logged, from nearby days, or designed); Game = buses on the game line.</p>
<div class="tw sumt"><table class="nw"><thead><tr><th>Line</th><th>Route</th><th>Operator</th><th class="num">Every</th><th class="num">Runtime</th><th class="num">Needed</th><th class="num">Buses</th><th class="num">Game</th><th>Game status</th></tr></thead><tbody>{"".join(net_rows)}</tbody></table></div>

<h2>Buses by size</h2>
<div class="two"><div class="tw sumt"><table><thead><tr><th>Class</th><th>Length</th><th class="num">Buses at peak</th></tr></thead><tbody>{cls_rows}<tr class="tot"><td>Total</td><td></td><td class="num">{tot}</td></tr></tbody></table></div>
<p class="muted small" style="max-width:60ch">One bus = one vehicle on one course. When a bus was replaced during the day, both appear on the course and only the replacement counts. Courses probably run only in the morning are shown dimmed and not counted.</p></div>

<h2 id="pak">Pak128 objects</h2>
<p class="lede" style="margin-bottom:10px">Full object names, one per type and livery. DPP buses use VZ-DPPraha-bus; every other operator's buses share the Prague package VZ-Praha-bus, one object per type and livery whatever the operator. Advert wraps have no object: they use the type's normal livery. <b>Requested</b> objects ({n_req} buses) are not in the pak yet (checkout {esc(OBJ["commit"].split(" ")[0])}); the VZ pak session is making them under these names.</p>
<div class="tw sumt"><table class="pt"><thead><tr><th>Real type</th><th>Livery</th><th>Core</th><th>Objects, in order</th><th>Operators</th><th>Status</th><th class="num">Buses at peak</th></tr></thead><tbody>{pak_rows}</tbody></table></div>

<h2 id="lines">Lines</h2>
<p class="lede">One card per PID bus line. Each shows the game line or lines with their differences, the Simutrans schedule per terminus, the PID stops, and one row per course (kurz) with the bus that ran it. Each vehicle shows three lines: number · garage (other operators: operator · garage), full type · length, and the pak128 core.</p>
<div class="legend"><span><span class="flag swap">swap</span> bus exchanged during the day, the last one counts</span><span><span class="flag ds">designed, not recorded</span> a real bus from the line's history, free that day</span><span><span class="flag am">not needed</span> in the line's history and free, not needed at 16:00 (dimmed, not counted)</span><span><span class="flag am">not counted</span> probably morning only</span><span><span class="rq" style="font:600 10px var(--font-display);color:var(--warn);background:var(--warn-soft);padding:0 5px;border-radius:3px">requested</span> object not in the pak yet</span></div>
<div class="grid">{"".join(cards)}</div>

<h2 id="depots">Garages and operators</h2>
<p class="lede">DPP garages from the register, then every other operator with all its buses on Prague city lines.</p>
<div class="grid">{"".join(dep_cards)}</div>

<h2>How this was built</h2>
<div class="notes"><ul>
  <li><b>Game.</b> The save-game session exported every line of the save numbered 100100–100299 (PID licence numbers; the name's first six digits), with buses, schedule entries and halts. A game line is compared with the PID line of the same number. Variants (e.g. 100102K) are compared with the same PID line.</li>
  <li><b>Stops.</b> A game halt matches a PID stop when one of its names (the parts between “/”, without “Praha,” and the stand letter) equals the PID name. Abbreviated or misspelt names count as the same stop and are listed as names to fix. Layover stands (“odstav”) are skipped. The game's round trip is split at the PID termini and each half is compared with the busiest PID pattern of that direction: missing stops, extra stops, a stop in place of another, and order.</li>
  <li><b>Timetable.</b> PID GTFS (<code>data.pid.cz/PID_GTFS.zip</code>, export {esc(G["gtfs_raw"])}), service date {esc(G["service_date"])}, routes whose licence number is 100100–100299 with route type 3 (bus); trolleybus 275 is on the trolleybus sheet. Main pattern = the busiest stop sequence per direction in 15:00–17:59. Buses needed = the larger of <code>cycle_need</code> (a bus leaving around 16:00 followed round the main round trip, at least 3 minutes at each terminus) and the most buses on the road at once in 16:00–17:00 over every pattern of the line (each trip plus its terminus layover: 3 minutes, or less where the timetable turns faster). The second decides on lines with branches and short workings, which the main round trip misses (191: 6 by round trip, 15 on the road).</li>
  <li><b>Simutrans schedule.</b> The shared rule in <code>pipeline/README.md</code>: the longest exact run of one Departure every / Offset / Also at pattern around 16:00, at most 8 departures per cycle; approximate fits give their largest deviation. Every bus terminus is a turn, so all values are 1 minute early, with the real minute printed under each. Other patterns with at least 3 peak trips are separate Simutrans lines.</li>
  <li><b>Vehicles.</b> seznam-autobusu.cz, <code>vypravenost/pid/vypis</code> per line for Friday {int(vd[8:])} September, and for 21–24 and 29 September on lines not run by DPP or not logged on the 25th. Where the logged courses are fewer than the buses needed, courses logged on the nearest other day fill in, if that bus was not out anywhere in PID on the 25th (seznam-autobusu.cz day overview). Any still missing are designed, not recorded, with real buses. They come from the line's own history since 1 September (since January 2025 for lines with no September record), are active in the register, and were not out anywhere on the 25th. The picks first cover every bus type in the line's history that the logged buses lack, then take the most recent. The free history buses left over are listed dimmed as "not needed" and are not counted. Where the history has too few free buses, a free active bus of the line's type from its operator fills in. Each car is matched by its register id to type, garage, paint and year (all DPP buses and the registers of every PID city operator).</li>
  <li><b>Liveries.</b> PID grey-red, PID red-white-blue, DPP red-white, city red-white (Stenbus), Veolia red-grey, white, turquoise-yellow (Stenbus 1700) and the Fashion Arena wrap of Vega Tour's line 238 buses (kept as its own objects at the user's request), from the register's current paint. An advert wrap or another livery maps to the most common normal livery of the same operator, type and year (the pak session's rule).</li>
  <li><b>Pak128.</b> Object names follow the VZ pak session's scheme of 29 September: <code>VZ-DPPraha-&lt;type&gt;-&lt;livery&gt;-&lt;id&gt;</code> for DPP and <code>VZ-Praha-&lt;type&gt;-&lt;livery&gt;-&lt;id&gt;</code> for every other operator; articulated buses are -A + -B. Which objects exist is read from the pak checkout ({esc(OBJ["commit"])}).</li>
  <li><b>Rebuilding.</b> <code>pipeline/praha-bus</code>: <code>python scripts/run.py --state {esc(s["name"])}</code>. The README there explains how to refresh the game export, the timetable and the vehicles.</li>
</ul></div>
<script>
(function(){{
  var t=document.getElementById('gct'), c=document.getElementById('onlyfix');
  c.addEventListener('change',function(){{ t.classList.toggle('onlyfix',c.checked); }});
}})();
</script>
{sticky.SCRIPT}
'''
    out = os.path.join(PROJECT, s['output_html'])
    open(out, 'w', encoding='utf-8').write(body)
    print('wrote', out, '| lines', len(bus), '| buses', tot, dict(per_class_total), '| to fix', nfix, '| requested', n_req)

if __name__ == '__main__':
    main()
