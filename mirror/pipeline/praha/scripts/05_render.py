"""Render the sheet: data/derived/<state>/{courses,timetable}.json + assets -> <project root>/<output_html>

Vehicle cell (shared rule): 1) numbers · depot  2) full types · length  3) pak core (livery added only where
the pak has several liveries for that type; "≈" = stand-in, reason in the pak table).

Usage: python 05_render.py --state 2026-09-27
"""
import argparse, collections, html, os
from common import state, load, DER, ASSETS, PROJECT

esc = html.escape
hm = lambda m: '%02d:%02d' % (m // 60, m % 60)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--state', required=True)
    s = state(ap.parse_args().state)
    CO = load(os.path.join(DER, s['name'], 'courses.json'))['courses']
    TT = load(os.path.join(DER, s['name'], 'timetable.json'))
    V = load(os.path.join(DER, f'vehicles_{s["register"]["raw"]}.json')); V.update(s.get('vehicle_overrides', {}))
    TY = load(os.path.join(ASSETS, 'types.json')); PK = load(os.path.join(ASSETS, 'pak_map.json'))
    CLASS, ORDER = TY['classes'], TY['class_order']
    museum = set(s.get('museum_lines', []))
    OUT = ('am', 'spare', 'withdrawn')      # logged but not counted; 'withdrawn' = back to the depot (change states)
    CH = s.get('changes')                    # change state: the sheet shows what to redo in game against CH['base']
    LEAVING = load(os.path.join(DER, s['name'], 'courses.json')).get('leaving', [])
    CO = [c for c in CO if c.get('change') != 'gone']
    gtitle = lambda G: s.get('pools', {}).get(G, {}).get('title') or G.replace('/', ' + ')

    def tget(d, t):
        if t in d: return d[t]
        for k, v in d.items():
            if k.endswith('*') and t.startswith(k[:-1]): return v
        return None
    def fullname(t):
        f = tget(TY['full_names'], t); return f.format(t=t) if f else t
    def length(types):
        ls = [tget(TY['car_length_m'], t) for t in types]
        if any(x is None for x in ls): return ''
        return (f'{len(ls)} × {ls[0]:g} m' if len(set(ls)) == 1 and len(ls) > 1 else ' + '.join(f'{x:g} m' for x in ls))
    def unit_class(types):
        if 'class_by_type' in TY: return TY['class_by_type'].get(types[0], TY.get('class_default', 'OTHER'))
        if any(x.startswith('série') or x in ('T1', 'T2R', '?') for x in types) or types == ['T3M.2']: return 'HIST'
        t = types[0]
        if t.startswith('15T'): return '15T'
        if t in ('14T', '52T'): return t
        if t.startswith('KT8'): return 'KT8'
        if len(types) == 1: return 'T3S'
        return 'T3LF' if 'T3R.PLF' in types else 'T3'

    def match(car, typ, pos=1):
        paint = V.get(car, {}).get('paint', '')
        for r in PK['rules']:
            if 'position' in r and r['position'] != pos: continue
            if 'type' in r and r['type'] != typ: continue
            if 'type_prefix' in r and not typ.startswith(r['type_prefix']): continue
            if 'paint_contains' in r and r['paint_contains'] not in paint: continue
            return dict(object=r['object'], sections=r.get('sections', 1), exact=r.get('exact', True), note=r.get('note', ''), typ=typ, paint=paint)
        return dict(object=None, sections=0, exact=False, note='no object in the pak', typ=typ, paint=paint)
    def objects(setstr, types):
        cars = setstr.split('+')
        if setstr in PK['sets']:
            return [dict(object=o['object'], sections=1, exact=o['exact'], note=o['note'], typ=t, paint=V.get(c, {}).get('paint', ''))
                    for o, c, t in zip(PK['sets'][setstr], cars, types)]
        return [match(c, t, k + 1) for k, (c, t) in enumerate(zip(cars, types))]
    LW = PK['livery_words']
    def split_obj(o):
        parts = o.split('-'); liv = next((p for p in parts if p in LW), '')
        return (o.split(liv + '-', 1)[1] if liv else parts[-1]), liv
    def core_label(r):
        if not r['object']: return '<b class="bad">no object</b>'
        core, liv = split_obj(r['object'])
        txt = core + (' ' + LW.get(liv, liv) if r['typ'] in PK['multi_livery_types'] else '')
        return ('≈ ' if not r['exact'] else '') + esc(txt)
    def unit_html(setstr, types, depot=None):
        cls = unit_class(types)
        pk = ' <b class="plus">+</b> '.join(core_label(r) for r in objects(setstr, types))
        dep = f' <span class="dp">· {esc(depot)}</span>' if depot else ''
        ln = length(types)
        return (f'<div class="unit u-{cls}"><span class="veh" data-v="{esc(setstr)}">{esc(setstr.replace("+", " + "))}{dep}</span>'
                f'<span class="vt">{esc(" + ".join(fullname(t) for t in types))}{" · " + ln if ln else ""}</span><span class="pk">{pk}</span></div>')

    # ---------- schedule block ----------
    def sched_block(ids, G):
        rows, notes = [], []
        pool = TT.get('pools', {}).get(G)
        brs = TT.get('branches', {}).get(G, {})
        def brlabel(r, i=None):
            for lab, b in brs.items():
                if {r['o'], r['d']} == set(b['route']) and b.get('line', i) == i: return lab
            return ''
        order = []
        if pool and pool.get('legs'):
            for k, (li, o, d) in enumerate(pool['legs']):
                r = next((x for x in TT['lines'].get(li, {}).get('schedule', []) if x['o'] == o and x['d'] == d), None)
                if r: order.append((li, r, f'stop {k + 1} of the circulation'))
        else:
            order = [(i, r, brlabel(r, i)) for i in ids for r in TT['lines'].get(i, {}).get('schedule', [])]
        for i, r, sub in order:
            if True:
                ltag = '<span class="lp">loop · 1 min early</span>' if r['loop'] else '<span class="lp st">no loop · as timetabled</span>'
                also = ', '.join(str(a) for a in r['set'][1:]) or '—'
                real_o = f'<small class="real">real {r["real"][0]}</small>' if r['loop'] else ''
                real_a = f'<small class="real">real {", ".join(str(x) for x in r["real"][1:])}</small>' if r['loop'] and len(r['real']) > 1 else ''
                fit = (f'exact {hm(r["first"])}–{hm(r["last"])} ({r["n"]} dep.)' if r['exact'] else f'approximate, up to {r["max_dev"]} min off')
                if r.get('override'): fit = f'set by hand, {hm(r["first"])}–{hm(r["last"])}: {esc(r["override"])}'
                d = []
                ex = [] if r.get('override') else list(r['extra']); mi = list(r['missing'])   # an override explains its empty slots
                for e in list(ex):
                    near = [m for m in mi if abs(m - e) <= 2]
                    if near: d.append(f'{hm(e)} runs at {hm(near[0])}'); mi.remove(near[0]); ex.remove(e)
                d += [f'no departure at {hm(e)}' for e in ex] + [f'extra departure {hm(m)}' for m in mi]
                if r['outside']: d.append('outside the run: ' + ', '.join(hm(x) for x in r['outside']))
                dtxt = f'<small>{esc("; ".join(d))}</small>' if d else ''
                lab = f'<td class="k">{i}</td>' if len(ids) > 1 else ''
                if r.get('short'): sub = 'short working · own Simutrans line (trams enter service here)'
                subt = f'<span class="lp st">{esc(sub)}</span>' if sub else ''
                rows.append(f'<tr>{lab}<td>{esc(r["o"])} <span class="arr">→</span> {esc(r["d"])}{subt}{ltag}</td><td class="num sv">{r["every"]}</td>'
                            f'<td class="num sv">{r["set"][0]}{real_o}</td><td class="sv">{esc(also)}{real_a}</td><td class="sv">auto</td><td class="fit">{fit}{dtxt}</td></tr>')
        for i in ids:
            for x in TT['lines'].get(i, {}).get('minors', []):
                times = ', '.join(hm(m) for m in x['deps'])
                if x.get('why'):
                    notes.append(f'<li><span class="k">{i}</span> {esc(x["o"])} → {esc(x["d"])}: {times}. {esc(x["why"][0].upper() + x["why"][1:])}</li>')
                elif x['depot']:
                    notes.append(f'<li><span class="k">{i}</span> depot run {esc(x["o"])} → {esc(x["d"])}: {times}</li>')
                else:
                    notes.append(f'<li><span class="k">{i}</span> short working {esc(x["o"])} → {esc(x["d"])}: {times}. Not a peak trip (no departure in the 16:00 hour), so not modelled.</li>')
        lh = '<th>Line</th>' if len(ids) > 1 else ''
        head = ''
        if pool and pool.get('legs') and s['pools'].get(G, {}).get('head'):
            head = (f'<p class="lpn">{esc(s["pools"][G]["head"])} Round trip about {pool["cycle"]} min, so <b>{pool["need"]} trams</b> '
                    f'at a {order[0][1]["every"]}-minute interval.</p>')
        elif pool and pool.get('legs'):
            head = (f'<p class="lpn"><b>One Simutrans line for the shared pool</b>, with the four timed stops below in this order. '
                    f'At Nádraží Holešovice the tram only changes its number (through stop, no loop, no shift). '
                    f'Round trip about {pool["cycle"]} min, so {pool["need"]} trams at an 8-minute interval (at least 3 min turnaround at each timed stop).</p>')
        elif brs:
            head = '<p class="lpn"><b>' + str(len(brs)) + ' separate Simutrans lines</b>, one per branch: ' + '; '.join(f'{esc(l)} needs {b["need"]} trams (round trip about {b["cycle"]} min)' for l, b in brs.items()) + '.</p>'
        nt = f'<details class="nm"><summary>Not modelled in 15:00–17:59 ({len(notes)})</summary><ul>{"".join(notes)}</ul></details>' if notes else ''
        return (f'<div class="sch"><h4>Simutrans schedule</h4><p class="lpn">Loop terminus: Offset and Also at are set 1 min before the timetable departure, so the tram clears the loop on time. Stub, triangle and through termini keep the timetable minute. Put the values on the boarding stop the tram departs from, not on the arrival stop.</p>'
                f'{head}<div class="tw"><table class="st"><thead><tr>{lh}<th>Terminus entry</th><th class="num">Departure every</th><th class="num">Offset</th><th>Also at</th><th>Leave up to</th><th>Fit</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div>{nt}</div>')

    # ---------- line cards ----------
    by_group = collections.defaultdict(list)
    for c in CO:
        if c['line'] in museum: continue
        by_group[c['group']].append(c)
    pools = s.get('pools', {}); flags = s.get('flags', {})
    TAG = {'swap': '<span class="flag swap">swap</span>', 'am': '<span class="flag am">not counted</span>', 'spare': '<span class="flag am">not needed</span>',
           'moved': '<span class="flag mv">moved line</span>', 'added': '<span class="flag mv">added</span>', 'designed': '<span class="flag ds">designed</span>'}
    cards, summ, notcounted = [], [], []
    cards_by = collections.defaultdict(list)      # change states: cards per change kind (route / new / minor / None)
    if CH:
        BCO = load(os.path.join(DER, CH['base'], 'courses.json'))['courses']
        BT = load(os.path.join(DER, CH['base'], 'timetable.json'))
        bcount = lambda g: sum(1 for c in BCO if c['group'] == g and c['uncertain'] not in OUT)
        def was_sched(L):
            return '; '.join(f'{esc(r["o"])} → every {r["every"]}, offset {r["set"][0]}' + (f', also at {", ".join(str(a) for a in r["set"][1:])}' if len(r['set']) > 1 else '')
                             for r in BT['lines'].get(L, {}).get('schedule', []) if not r.get('short'))
        def leaving_row(e):
            c0 = next(c for c in BCO if c['id'] == e['id'])
            v = next(v for v in c0['veh'] if v['set'] == e['set'])
            dest = (f'<span class="flag mv">moves to line {esc(e["to"].split("/")[0])}</span><span class="nt">as {esc(e["to"])}</span>' if e['to']
                    else f'<span class="flag wd">back to the depot</span><span class="nt">{esc(e["why"])}</span>')
            return f'<tr class="out"><td class="k">{esc(e["id"])}</td><td class="v">{unit_html(v["set"], v["types"], v["depot"])}</td><td class="n">{dest}</td></tr>'
    depot = collections.defaultdict(lambda: collections.defaultdict(list))
    for G in s['line_order']:
        ids = pools[G]['lines'] if G in pools else [G]
        cs = sorted(by_group.get(G, []), key=lambda c: (c['uncertain'] == 'spare', c['line'] != ids[0] and c['pm_line'] == c['line'], int(c['line']), c['course']))
        routes, seen_pairs = '', set()
        for i in ids:
            rs = TT['lines'].get(i, {}).get('routes', [])
            for r in rs:
                if (i, frozenset((r['o'], r['d']))) in seen_pairs: continue
                seen_pairs.add((i, frozenset((r['o'], r['d']))))
                back = next((x for x in rs if x['o'] == r['d'] and x['d'] == r['o']), None)
                lab = f'<span class="rl">{i}</span>' if len(ids) > 1 else ''
                rt = f"{r['runtime']}" + (f"/{back['runtime']}" if back and back['runtime'] != r['runtime'] else '')
                hw = f"every {r['headway']} min · " if r['headway'] else ''
                routes += f'<li>{lab}<b>{esc(r["o"])} – {esc(r["d"])}</b> <span class="muted">· {hw}{rt} min</span></li>'
        rows, rows_chg, mix = [], [], collections.Counter()
        brcfg = {b['label']: b for b in s.get('splits', {}).get(G, [])}
        if brcfg:
            cs = sorted(cs, key=lambda c: (c['uncertain'] == 'spare', list(brcfg).index(c['branch']) if c.get('branch') in brcfg else 99, int(c['line']), c['course']))
        cur = None
        for c in cs:
            if brcfg and c.get('branch') != cur:
                cur = c.get('branch'); b = brcfg.get(cur, {}); nb = TT.get('branches', {}).get(G, {}).get(cur, {})
                na = sum(1 for x in cs if x.get('branch') == cur and x['uncertain'] not in OUT)
                rows.append(f'<tr class="brh"><td colspan="3"><b>{esc(cur or "no branch")}</b> · {na} assigned, {nb.get("need", "?")} needed by round trip<br><span class="muted">{esc(b.get("why", ""))}</span></td></tr>')
            final = next(v for v in c['veh'] if v['set'] == c['final'])
            if c['uncertain'] not in OUT: mix[unit_class(final['types'])] += 1
            elif c['uncertain'] == 'am': notcounted.append(c)
            chain = '<div class="arr">then</div>'.join(unit_html(x, next(v for v in c['veh'] if v['set'] == x)['types'], next(v for v in c['veh'] if v['set'] == x)['depot']) for x in c['chain'])
            tr = f'<span class="tag">→{c["transfer"]}</span>' if c['transfer'] and G in pools and c['transfer'] in pools[G]['lines'] else ''
            if G in pools and not pools[G].get('title'): tr += '<span class="flag pool">pool</span>'
            split = '<span class="flag pm">PM part</span>' if c['split'] else ''
            tag, rc = TAG.get(c['uncertain'], ''), ('spare' if c['uncertain'] == 'spare' else ('unc' if c['uncertain'] else ''))
            if c.get('change') == 'in':
                tag, rc = f'<span class="flag in">moved here from {esc(c["moved_from"])}</span>', 'in'
            elif c.get('change') == 'withdrawn':
                tag, rc = '<span class="flag wd">back to the depot</span>', 'out'
            row = f'<tr class="{rc}"><td class="k">{c["id"]}{tr}</td><td class="v">{chain}</td><td class="n">{split}{tag}<span class="nt">{esc(c["note"])}</span></td></tr>'
            (rows_chg if CH and c.get('change') in ('in', 'withdrawn') else rows).append(row)
            for v in c['veh']:
                replaced = c['swap'] and v['set'] != c['final']
                depot[v['depot']][c.get('branch') or G].append(dict(set=v['set'], types=v['types'], course=c['id'], u=c['uncertain'], replaced=replaced, moved_from=c.get('moved_from')))
        n = sum(mix.values())
        tl = [TT['lines'][i] for i in ids if i in TT['lines']]
        if G in pools and TT['pools'][G].get('need'): needtxt = f'<span class="need">{"circle" if pools[G].get("title") else "shared pool"}: {TT["pools"][G]["need"]} trams needed for the whole circulation</span>'
        elif TT.get('branches', {}).get(G): needtxt = '<span class="need">' + '; '.join(f'{esc(l)}: {b["need"]} needed' for l, b in TT['branches'][G].items()) + '</span>'
        else: needtxt = f'<span class="need">timetable at 16:00: {tl[0]["cycle_need"]} sets needed by round trip</span>' if tl and tl[0]['cycle_need'] else ''
        mix_html = ' '.join(f'<span class="mx u-{k}"><b>{mix[k]}</b>× {CLASS[k][0]}</span>' for k in ORDER if mix[k])
        fl = flags.get(G); fl_html = f'<p class="callout {fl[0]}">{esc(fl[1])}</p>' if fl else ''
        pnote = f'<p class="callout info">{esc(pools[G]["note"])}</p>' if G in pools else ''
        title = gtitle(G)
        pooltag = (f'<span class="flag pool big">{esc(pools[G]["simutrans"]["label"]) if pools[G].get("title") else "shared pool"}</span>') if G in pools else ''
        THEAD = '<thead><tr><th>Course</th><th>Vehicle · depot / type · length / pak128 core</th><th>Notes</th></tr></thead>'
        kind = CH['lines'].get(G, {}).get('kind') if CH else None
        chg_html = ''
        if CH and kind:
            cl = CH['lines'][G]
            old = cl.get('was', G)
            lv = [e for e in LEAVING if e['group'] == G]
            before = bcount(old) if kind != 'new' else 0
            KL = {'route': 'Route changed', 'new': 'New line', 'minor': 'Small edit'}[kind]
            rr = ''
            if cl.get('old_route') or cl.get('new_route'):
                rr = ('<div class="rr">' + (f'<span class="was">{esc(cl["old_route"])}</span><span class="arr">→</span>' if cl.get('old_route') else '') +
                      f'<b>{esc(cl.get("new_route", ""))}</b></div>')
            moves_in = sum(1 for c in cs if c.get('change') == 'in'); moves_out = sum(1 for e in lv if e['to']); wd_n = sum(1 for e in lv if not e['to'])
            parts = [f'<b>Trams {before} → {n}</b>'] + ([f'{n - moves_in} stay'] if kind == 'route' else []) +                     ([f'{moves_in} come in'] if moves_in else []) + ([f'{moves_out} move to other lines'] if moves_out else []) + ([f'{wd_n} back to the depot'] if wd_n else [])
            tt = f'<p class="tt">{" · ".join(parts)}</p>' if kind != 'minor' else ''
            ws = was_sched(old) if kind == 'route' else ''
            ws = f'<p class="muted small">Schedule before: {ws}. The new values are in the Simutrans schedule below.</p>' if ws else ''
            chg_html = f'<div class="chg k-{kind}"><span class="ck">{KL}</span>{rr}<p>{esc(cl["what"])}</p>{tt}{ws}</div>'
        if CH and kind in ('route', 'new'):
            lv_rows = [leaving_row(e) for e in LEAVING if e['group'] == G]
            vis = rows_chg + lv_rows
            table = (f'<h4 class="todo">Trams to change ({len(vis)})</h4><div class="tw"><table class="ct">{THEAD}<tbody>{"".join(vis)}</tbody></table></div>' if vis else
                     '<p class="muted small">No tram changes on this line: only the route and schedule.</p>')
            if rows:
                nst = sum(1 for c in cs if c.get('change') is None and c['uncertain'] not in OUT)
                extra = sum(1 for c in cs if c.get('change') is None and c['uncertain'] in OUT)
                table += (f'<details class="stay"><summary>Trams that stay on the line ({nst}' + (f', plus {extra} not needed or not counted' if extra else '') +
                          f')</summary><div class="tw"><table class="ct">{THEAD}<tbody>{"".join(rows)}</tbody></table></div></details>')
        else:
            table = f'<div class="tw"><table class="ct">{THEAD}<tbody>{"".join(rows_chg + rows)}</tbody></table></div>'
        card = f'''
<article class="lc{' changed' if kind in ('route', 'new') else ''}" id="l{G.replace('/', '-')}">
  <header><span class="lb">{title}</span><div class="lh">{pooltag}<ul class="routes">{routes}</ul>{needtxt}</div><div class="cnt"><b>{n}</b><span>trams</span></div></header>
  {chg_html}
  <div class="mix">{mix_html}</div>
  {pnote}{fl_html}
  {sched_block(ids, G)}
  {table}
</article>'''
        cards.append(card); cards_by[kind].append((G, title, n, card))
        summ.append((G, title, n, mix))

    # museum lines (42)
    rowsm = []
    for c in sorted([c for c in CO if c['line'] in museum], key=lambda c: c['course']):
        v = c['veh'][0]
        rowsm.append(f'<tr><td class="k">{c["id"]}</td><td class="v">{unit_html(v["set"], v["types"], v["depot"])}</td></tr>')
        depot[v['depot']][c['line']].append(dict(set=v['set'], types=v['types'], course=c['id'], u='', replaced=False))

    # depots
    dep_cards, dep_summ = [], []
    order_all = []
    for G in s['line_order']:
        order_all += [b['label'] for b in s.get('splits', {}).get(G, [])] + [G]
    order_all += sorted(museum)
    for D in s['depot_order']:
        lines = depot.get(D, {})
        if not lines: continue
        cnt = collections.Counter(); nunits = 0; trs = []
        order = [l for l in order_all if l in lines]
        for G in order:
            items = sorted(lines[G], key=lambda x: (int(x['course'].split('/')[0]), int(x['course'].split('/')[1])))
            for j, it in enumerate(items):
                real = it['u'] not in OUT and not it['replaced']
                if real and G not in museum: cnt[unit_class(it['types'])] += 1; nunits += 1
                st = ''
                if it['replaced']: st = '<span class="flag swap">replaced during the day</span>'
                elif it['u'] == 'am': st = '<span class="flag am">not counted: probably morning only</span>'
                elif it['u'] == 'spare': st = '<span class="flag am">not needed at 16:00</span>'
                elif it['u'] == 'withdrawn': st = '<span class="flag wd">back to the depot</span>'
                elif it.get('moved_from'): st = f'<span class="flag mv">moved here from {esc(it["moved_from"])}</span>'
                elif it['u'] == 'swap': st = '<span class="flag swap">replacement, time not recorded</span>'
                elif it['u'] == 'moved': st = '<span class="flag mv">moved from another line</span>'
                elif it['u'] == 'added': st = '<span class="flag mv">added for the new route</span>'
                elif it['u'] == 'designed': st = '<span class="flag ds">designed addition</span>'
                if G in pools: lbl = f'<span class="lb sm">{gtitle(G)}</span><span class="lsub">{"circle" if pools[G].get("title") else "shared pool"}</span>'
                elif ' ' in G: lbl = f'<span class="lb sm">{esc(G.split(" ")[0])}</span><span class="lsub">{esc(G.split(" ", 1)[1])}</span>'
                else: lbl = f'<span class="lb sm">{G}</span>'
                lc = f'<td class="lcell" rowspan="{len(items)}">{lbl}</td>' if j == 0 else ''
                trs.append(f'<tr class="{"first" if j == 0 else ""}{" dim" if not real else ""}">{lc}<td class="k">{esc(it["course"])}</td><td class="v">{unit_html(it["set"], it["types"])}</td><td class="n">{st}</td></tr>')
        mix_html = ' '.join(f'<span class="mx u-{k}"><b>{cnt[k]}</b>× {CLASS[k][0]}</span>' for k in ORDER if cnt[k])
        note = f'<p class="muted small">{esc(s["depot_notes"][D])}</p>' if D in s.get('depot_notes', {}) else ''
        dep_cards.append(f'''
<article class="dc" id="d-{D}">
  <header><h3>Vozovna {esc(D)}</h3><div class="cnt"><b>{nunits}</b><span>trams</span></div></header>
  <p class="dlines">Lines {esc(", ".join(sorted({(gtitle(o.split(" ")[0]) + ((" (circle)" if pools[o].get("title") else " (shared pool)") if o in pools else "")) for o in order}, key=lambda x: int(x.split(" ")[0]))))}</p>
  <div class="mix">{mix_html}</div>{note}
  <div class="tw"><table class="dt"><thead><tr><th>Line</th><th>Course</th><th>Vehicle / type · length / pak128 core</th><th></th></tr></thead><tbody>{''.join(trs)}</tbody></table></div>
</article>''')
        dep_summ.append((D, nunits))

    # summary + pak table
    tot = collections.Counter()
    for *_, m in summ: tot.update(m)
    sum_rows = ''.join(f'<tr><td><a class="lb sm" href="#l{G.replace("/", "-")}">{t}</a>{("<span class=lsub>circle</span>" if pools[G].get("title") else "<span class=lsub>shared pool</span>") if G in pools else ""}</td><td class="num">{n}</td>' + ''.join(f'<td class="num">{m[k] or ""}</td>' for k in ORDER) + '</tr>' for G, t, n, m in summ)
    sum_rows += '<tr class="tot"><td>Total</td><td class="num">' + str(sum(tot.values())) + '</td>' + ''.join(f'<td class="num">{tot[k] or ""}</td>' for k in ORDER) + '</tr>'
    cls_head = ''.join(f'<th class="num"><span class="cls u-{k}">{esc(CLASS[k][0])}</span></th>' for k in ORDER)
    cls_legend = ''.join(f'<tr><td><span class="cls u-{k}">{esc(CLASS[k][0])}</span></td><td>{esc(CLASS[k][1])}</td><td>{esc(CLASS[k][2])}</td><td>{esc(CLASS[k][3])}</td></tr>' for k in ORDER)
    pk = collections.Counter(); reasons = collections.defaultdict(set)
    for c in CO:
        if c['uncertain'] in OUT: continue
        v = next(x for x in c['veh'] if x['set'] == c['final'])
        for r in objects(v['set'], v['types']):
            if PK.get('livery_from_object') and r['object']:   # one-livery paks: group by the object's livery, not the real paint
                liv = LW.get(split_obj(r['object'])[1], '')
            else:
                liv = 'advert wraps' if r['paint'].startswith('CVR') else PK['paint_names'].get(r['paint'], r['paint'] or '?')
            k = ('Škoda 15T ForCity Alfa' if r['typ'].startswith('15T') else fullname(r['typ']), liv, r['object'] or '', r['sections'], r['exact'])
            pk[k] += 1
            if r['note']: reasons[k].add(r['note'])
    def chainnames(o, n):
        if not o: return '<b class="bad">no object</b>'
        return ' + '.join(f'<code>{esc(x)}</code>' for x in [o] + [o + PK.get('section_suffix', '_{i}').format(i=i) for i in range(2, n + 1)])
    pak_rows = ''
    for (t, l, o, n, ex), k in sorted(pk.items(), key=lambda kv: (kv[0][0], not kv[0][4], -kv[1])):
        core = split_obj(o)[0] if o else ''
        pak_rows += (f'<tr><td>{esc(t)}</td><td>{esc(l)}</td><td class="core">{("≈ " if not ex and o else "") + esc(core) if o else ""}</td>'
                     f'<td class="chain">{chainnames(o, n)}</td><td class="num">{PK["carunits"].get(core, "")}</td>'
                     f'<td>{"exact" if ex else ("substitute: " + esc("; ".join(sorted(reasons[(t, l, o, n, ex)]))) if o else "")}</td><td class="num">{k}</td></tr>')
    nc = ''.join(f'<li><b>{c["id"]}</b> {esc(c["final"].replace("+", " + "))}: {esc(c["note"])}</li>' for c in notcounted) or '<li>None.</li>'
    dep_nav = ''.join(f'<a href="#d-{D}">{esc(D)} <b>{n}</b></a>' for D, n in dep_summ)
    line_nav = ''.join(f'<a class="lb sm" href="#l{G.replace("/", "-")}">{t}</a>' for G, t, _, _ in summ)

    crosscheck = ''.join(f'<tr><td class="k">{esc(k)}</td><td class="v">{unit_html(x, [V.get(c, {}).get("type", "?") for c in x.split("+")])}</td></tr>'
                         for k, x in s.get('cross_check', {}).get('sets', []))
    metro_rows = ''
    if s.get('metro') and TT.get('metro'):
        mr = load(os.path.join(DER, f'metro_records_{s["vehicle_date"]}.json'))
        for L, v in TT['metro'].items():
          pats = v['patterns']
          rec = mr.get(L, [])
          rect = f'{len(rec)} <span class="muted small">incomplete record; courses numbered up to {max(rec)}</span>' if rec else '—'
          dep = '; '.join(f'{esc(x["o"])} → {esc(x["d"])} ×{x["n"]}' for x in v['depot_runs'])
          for k, p in enumerate(pats):
            lo_, hi_ = v['reverse_min'][0], v['reverse_min'][-1]
            nb = p['need_by_reverse']; n_lo, n_hi = nb[str(lo_)] if str(lo_) in nb else nb.get(lo_), nb[str(hi_)] if str(hi_) in nb else nb.get(hi_)
            need = f'<b>{n_lo}</b>' + (f'–<b>{n_hi}</b>' if n_hi != n_lo else '')
            gi = '—' if p['gap_min'] is None else ((f"every {p['gap_min']} min" if p['gap_min'] == p['gap_max'] else f"every {p['gap_min']}–{p['gap_max']} min") + f" ({p['per_hour']} per hour)")
            sim = ''
            for x in p['simutrans']:
                also = ', '.join(str(a) for a in x['set'][1:]) or '—'
                run = f"exact {hm(x['first'])}–{hm(x['last'])}" if x['exact'] else f"approximate, up to {x['max_dev']} min off"
                ph = f' · {x["per_hour"]}/h' if x.get('per_hour') else ''
                sim += (f'<div class="msim"><span class="muted">{esc(x["o"])} →</span> every <b>{x["every"]}</b> · offset <b>{x["set"][0]}</b> · also at <b>{esc(also)}</b>{ph}'
                        f' <span class="muted small">({run})</span></div>')
            first = k == 0
            span = f' rowspan="{len(pats)}"' if len(pats) > 1 else ''
            metro_rows += ('<tr>' + (f'<td{span}><span class="ml m{L}">{L}</span></td>' if first else '') +
                           f'<td>{esc(p["o"])} – {esc(p["d"])}' + (f'<br><span class="muted small">branch {k + 1} of {len(pats)}</span>' if len(pats) > 1 else '') + '</td>'
                           f'<td>{gi}</td><td>{sim}</td><td>{p["runtime"]} min</td><td class="num">{need}</td>' +
                           (f'<td class="num"{span}>{rect}' + (f'<br><span class="muted small">line total {v["need"]}–{v["need_hi"]} needed</span>' if len(pats) > 1 else '') + f'</td><td{span}>{esc(s["metro"]["stock"].get(L, ""))}</td><td class="muted small"{span}>{("occasional trips not counted (depot runs, single trips): " + dep) if dep else ""}</td>' if first else '') +
                           '</tr>')
    ferry_rows = ''
    def opname(n):   # PID sub-agency -> company name without the legal form
        for suf in (', s.r.o.', ' s.r.o.', ', a.s.', ' a.s.'):
            n = n.replace(' ,', ',').split(suf)[0]
        return n.strip(' ,')
    for L, v in TT.get('ferry', {}).items():
        ds = v['dirs']
        span = f' rowspan="{len(ds)}"' if len(ds) > 1 else ''
        for k, x in enumerate(ds):
            sm = x['simutrans']
            also = ', '.join(str(a) for a in sm['set'][1:]) or '—'
            run = f"exact {hm(sm['first'])}–{hm(sm['last'])} ({sm['n']} departures)" if sm['exact'] else f"approximate, up to {sm['max_dev']} min off"
            gi = ('every ' + (f"{x['gap'][0]}" if x['gap'][0] == x['gap'][1] else f"{x['gap'][0]}–{x['gap'][1]}") + ' min') if x['gap'] else '—'
            ferry_rows += ('<tr>' + (f'<td{span}><span class="lb sm">{esc(L)}</span></td>' if k == 0 else '') +
                           f'<td>{esc(x["o"])} → {esc(x["d"])}</td><td>{gi}</td>'
                           f'<td><div class="msim">every <b>{sm["every"]}</b> · offset <b>{sm["set"][0]}</b> · also at <b>{esc(also)}</b> <span class="muted small">({run})</span></div></td>'
                           f'<td>{x["crossing"]} min</td><td>{hm(x["first"])}–{hm(x["last"])}</td>' +
                           (f'<td class="num"{span}><b>{v["need"]}</b></td><td{span}>{esc(", ".join(opname(o) for o in v["operators"]))}</td>'
                            f'<td class="muted small"{span}>{esc(s.get("ferry", {}).get("boats", {}).get(L, "not known yet"))}</td>' if k == 0 else '') + '</tr>')
    # ---------- change state: summary, move list, cancelled lines, collapsed unchanged lines ----------
    chg = dict(CHANGES='', MOVES='', CANCELLED='', LINES_NEW='', LINES_MINOR='', LINES_SAME='', N_MOVES='0', N_SAME='0', NAD='', NADPAK='', NADNOT='', N_NAD='0')
    # ---------- replacement buses (NAD): bus-sheet style cards (data from 03c_nad.py) ----------
    nadp = os.path.join(DER, s['name'], 'nad.json')
    if s.get('nad') and os.path.exists(nadp):
        NAD = load(nadp)
        BLIV = {'pidsedocervena': 'PID grey-red', 'pidcervenomodrobila': 'PID red-white-blue', 'dppcervenobila': 'DPP red-white',
                'mestskacervenobila': 'city red-white', 'veoliacervenoseda': 'Veolia red-grey', 'bila': 'white'}
        bcls = lambda ln: 'UNK' if not ln else 'ART' if ln >= 17 else 'LONG' if ln >= 13.5 else 'STD' if ln >= 11.5 else 'MIDI' if ln >= 9 else 'MINI'
        BCN = {'ART': 'Articulated', 'LONG': 'Long', 'STD': 'Standard', 'MIDI': 'Midibus', 'MINI': 'Minibus', 'UNK': 'Not known'}
        blivs = collections.defaultdict(set)
        for v in NAD['lines'].values():
            for c in v['courses']:
                for x in c['cars']:
                    if x['pak']: blivs[x['pak']['core']].add(x['pak']['livery'])
        def bus_unit(x):
            where = ' · '.join(w for w in (('' if x['operator'] == 'DPP' else x['operator'].title()), x['garage']) if w and w != '?')
            pk = x['pak']
            if pk:
                core = f'<code>{esc(pk["core"])}</code>' + (f' {esc(BLIV.get(pk["livery"], pk["livery"]))}' if len(blivs[pk['core']]) > 1 or pk['mapped'] else '')
                if pk['mapped']: core += f' <span class="mp">({esc(pk["mapped"])} → normal livery)</span>'
                if pk['status'] != 'in pak': core += '<span class="rq">requested</span>'
            else: core = '<b class="bad">no object: vehicle not in the register</b>'
            ln = f' · {x["length"]:g} m' if x['length'] else ''
            return (f'<div class="unit u-{bcls(x["length"])}"><span class="veh" data-v="{esc(x["num"])}">{esc(x["num"])}' + (f' <span class="dp">· {esc(where)}</span>' if where else '') +
                    f'</span><span class="vt">{esc(x["type"])}{ln}</span><span class="pk">{core}</span></div>')
        def dd(d): return f'{int(d[8:10])} Oct' if d[5:7] == '10' else d
        cards_n, pakc = [], collections.Counter(); pinfo = {}
        for L, v in NAD['lines'].items():
            routes = ''.join(f'<li><b>{esc(m["o"])} → {esc(m["d"])}</b> <span class="muted">· every {m["headway"]} min · {m["runtime"]} min</span></li>' for m in v['main'])
            how = 'on the road at once (circular line)' if v['circular'] else ('by round trip' if (v['need_cycle'] or 0) >= v['need_on_road'] else 'on the road at once')
            sched = ''
            for m in v['main']:
                sc = m['schedule']
                if not sc: continue
                also = ', '.join(str(a) for a in sc['set'][1:]) or '—'
                sched += (f'<tr><td>{esc(m["o"])} <span class="arr">→</span> {esc(m["d"])}<span class="lp">terminus · 1 min early</span></td><td class="num sv">{sc["every"]}</td>'
                          f'<td class="num sv">{sc["set"][0]}<small class="real">real {sc["real"][0]}</small></td><td class="sv">{esc(also)}</td><td class="sv">auto</td>'
                          f'<td class="fit">exact {hm(sc["first"])}–{hm(sc["last"])} ({sc["n"]} departures)</td></tr>')
            stops = ''.join(f'<div><h5>{esc(m["o"])} → {esc(m["d"])} ({len(m["stops"])})</h5><ol>' + ''.join(f'<li>{esc(x)}</li>' for x in m['stops']) + '</ol></div>' for m in v['main'])
            rows, mix = [], collections.Counter()
            for c in v['courses']:
                notes = []
                if c['source'] != NAD['vehicle_date']: notes.append(f'Not logged on {dd(NAD["vehicle_date"])}; this bus ran the course on {dd(c["source"])} and was not out anywhere in PID on {dd(NAD["vehicle_date"])}.')
                if c['spare']: notes.append(f'Logged, but not needed at 16:00 (the line needs {v["need"]}). Not counted.')
                else:
                    for x in c['cars']:
                        mix[bcls(x['length'])] += 1
                        if x['pak']:
                            pakc[x['pak']['object']] += 1; pinfo[x['pak']['object']] = (x['type'], x['pak'])
                flag = '<span class="flag am">not needed</span>' if c['spare'] else ''
                src = f'<span class="src">logged {dd(c["source"])}</span> '
                rows.append(f'<tr class="{"spare" if c["spare"] else ""}"><td class="k">{esc(L)}/{esc(c["course"])}</td><td class="v">{"".join(bus_unit(x) for x in c["cars"])}</td>'
                            f'<td class="n">{flag}{src}<span class="nt">{esc(" ".join(notes))}</span></td></tr>')
            mixh = ' '.join(f'<span class="mx u-{k}"><b>{mix[k]}</b>× {BCN[k]}</span>' for k in BCN if mix[k])
            st_ = '<span class="ck sm k-new">New with this closure</span>' if v['status'] == 'new' else '<span class="ck sm k-minor">Already running before 27 Sep</span>'
            opn = ', '.join(o.split(',')[0].replace('Dopravní podnik hl. m. Prahy', 'Dopravní podnik hlavního města Prahy') for o in v['operators'])
            cards_n.append(f'''
<article class="lc bus" id="n{L}">
  <header><span class="lb nad">{esc(L)}</span><div class="lh">{st_}<ul class="routes">{routes}</ul><span class="opn">{esc(opn)} · replaces trams: {esc(v["for"])}</span>
  <span class="need">timetable at 16:00: {v["need"]} buses needed {how}</span></div><div class="cnt"><b>{v["counted"]}</b><span>buses</span></div></header>
  <div class="mix">{mixh}</div>
  <p class="callout info">{esc(v["what"])}</p>
  <div class="sch"><h4>Simutrans schedule</h4><p class="lpn">Buses turn at every terminus, so Offset and Also at are set 1 min before the timetable departure, with the real minute under each value (bus sheet rule). Service {hm(v["first"] % 1440)}–{hm(v["last"] % 1440)}.</p>
  <div class="tw"><table class="st"><thead><tr><th>Terminus entry</th><th class="num">Departure every</th><th class="num">Offset</th><th>Also at</th><th>Leave up to</th><th>Fit</th></tr></thead><tbody>{sched}</tbody></table></div></div>
  <details class="stops"><summary>PID stops of the main pattern{"s" if len(v["main"]) > 1 else ""}</summary><div class="pc">{stops}</div></details>
  <div class="tw"><table class="ct"><thead><tr><th>Course</th><th>Vehicle · garage / type · length / pak128 core</th><th>Notes</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div>
</article>''')
        chg['NAD'] = ''.join(cards_n); chg['N_NAD'] = str(len(cards_n))
        chg['NADPAK'] = ''.join(f'<tr><td>{esc(ty)}</td><td>{esc(BLIV.get(pk["livery"], pk["livery"]))}</td><td class="core">{esc(pk["core"])}</td>'
                                f'<td class="chain">{" + ".join(f"<code>{esc(o)}</code>" for o in pk["chain"])}</td><td>{esc(pk["status"])}</td><td class="num">{n}</td></tr>'
                                for o, n in pakc.most_common() for ty, pk in [pinfo[o]])
        chg['NADNOT'] = ''.join(f'<li>{esc(x)}</li>' for x in NAD.get('not_modelled', []))
    if CH:
        def short(G):
            rs = []
            for i in (pools[G]['lines'][:1] if G in pools else [G]):
                for r in TT['lines'].get(i, {}).get('routes', [])[:1]: rs.append(f'{r["o"]} – {r["d"]}')
            return ', '.join(rs)
        n_of = {G: n for G, _, n, _ in summ}
        out_of = collections.Counter(e['group'] for e in LEAVING if e['to']); wd_of = collections.Counter(e['group'] for e in LEAVING if not e['to'])
        in_of = collections.Counter(c['group'] for c in CO if c.get('change') == 'in')
        KL = {'route': 'Route changed', 'new': 'New line', 'minor': 'Small edit', 'cancelled': 'Cancelled'}
        rows = []
        items = [(G, CH['lines'][G]) for G in s['line_order'] if G in CH['lines']] + list(CH.get('cancelled', {}).items())
        order = {'route': 0, 'cancelled': 1, 'new': 2, 'minor': 3}
        for G, cl in sorted(items, key=lambda kv: order[kv[1].get('kind', 'cancelled')]):
            kind = cl.get('kind', 'cancelled'); old = cl.get('was', G)
            before = bcount(old) if kind != 'new' else 0
            after = n_of.get(G, 0) if kind != 'cancelled' else 0
            todo = []
            if kind == 'route': todo.append('edit route and schedule' if G not in pools or not pools[G].get('title') else f'turn Simutrans line {old} into the circle')
            if kind == 'new': todo.append('new line: route, schedule')
            if kind == 'cancelled': todo.append(f'delete Simutrans line {G}')
            if in_of[G]: todo.append(f'{in_of[G]} tram{"s" if in_of[G] > 1 else ""} come{"" if in_of[G] > 1 else "s"} in')
            if out_of[G]: todo.append(f'{out_of[G]} trams leave to ' + ', '.join(sorted({e["to"].split("/")[0] for e in LEAVING if e["group"] == G and e["to"]}, key=int)))
            if wd_of[G]: todo.append(f'{wd_of[G]} tram{"s" if wd_of[G] > 1 else ""} back to the depot')
            if kind == 'minor': todo.append(cl['what'].split('. ')[0])
            route = ((f'<span class="was">{esc(cl["old_route"])}</span> → ' if cl.get('old_route') else '') + ('<b>no service</b>' if kind == 'cancelled' else '') + (f'<b>{esc(cl["new_route"])}</b>' if cl.get('new_route') else '')) or esc(short(G))
            link = f'#l{G.replace("/", "-")}' if kind != 'cancelled' else f'#x{G}'
            rows.append(f'<tr class="k-{kind}"><td><a class="lb sm{" gone" if kind == "cancelled" else ""}" href="{link}">{esc(gtitle(G))}</a></td><td><span class="ck sm k-{kind}">{KL[kind]}</span></td>'
                        f'<td>{route}</td><td class="num">{before if kind != "minor" else after} → <b>{after}</b></td><td>{esc("; ".join(todo))}</td></tr>')
        if chg['NAD']:     # replacement buses go in the same table, linked to their cards at the bottom
            for L, v in NAD['lines'].items():
                m0 = v['main'][0]
                rows.append(f'<tr class="k-{"new" if v["status"] == "new" else "minor"}"><td><a class="lb sm nad" href="#n{L}">{esc(L)}</a></td>'
                            f'<td><span class="ck sm k-{"new" if v["status"] == "new" else "minor"}">{"New NAD bus" if v["status"] == "new" else "NAD bus, not new"}</span></td>'
                            f'<td><b>{esc(m0["o"])} – {esc(m0["d"] if not v["circular"] else "loop via " + m0["stops"][len(m0["stops"]) // 2])}</b></td><td class="num">{"0 → " if v["status"] == "new" else ""}<b>{v["counted"]}</b></td>'
                            f'<td>{"new bus line: route, schedule, " + str(v["counted"]) + " buses (see NAD at the bottom)" if v["status"] == "new" else "add only if your game lacks it (see NAD at the bottom)"}</td></tr>')
        chg['CHANGES'] = ''.join(rows)
        # one move list, grouped by destination
        mv = []
        bco = {c['id']: c for c in BCO}
        dests = collections.OrderedDict()
        for e in LEAVING:
            dests.setdefault(e['to'].split('/')[0] if e['to'] else 'depot', []).append(e)
        def dkey(k): return (k == 'depot', int(k) if k.isdigit() else 0)
        for d in sorted(dests, key=dkey):
            es = sorted(dests[d], key=lambda e: (int(e['to'].split('/')[1]) if e['to'] else 0, e['id']))
            why = CH.get('move_why', {}).get(d, '')
            for j, e in enumerate(es):
                v = next(v for v in bco[e['id']]['veh'] if v['set'] == e['set'])
                lead = (f'<td class="lcell" rowspan="{len(es)}">' + (f'<span class="lb sm">{esc(gtitle(next((g for g in s["line_order"] if g == d or pools.get(g, {}).get("recorded_as") == d), d)))}</span>' if d != 'depot' else '<b>Back to the depot</b>') +
                        f'<p class="muted small">{esc(why)}</p></td>') if j == 0 else ''
                fromg = bco[e['id']]['group']
                mv.append(f'<tr class="{"first" if j == 0 else ""}">{lead}<td class="v">{unit_html(v["set"], v["types"], v["depot"])}</td>'
                          f'<td class="k">{esc(e["id"])}<span class="lsub">line {esc(gtitle(CH.get("group_map", {}).get(fromg, fromg)) if fromg not in CH.get("cancelled", {}) else fromg + " (cancelled)")}</span></td>'
                          f'<td class="k">{esc(e["to"] or "—")}</td>' + (f'<td class="n muted small">{esc(e["why"])}</td>' if not e['to'] else '<td></td>') + '</tr>')
        chg['MOVES'] = ''.join(mv); chg['N_MOVES'] = str(len(LEAVING))
        # cancelled lines: where every tram went
        cx = []
        for G, cl in CH.get('cancelled', {}).items():
            lr = ''.join(leaving_row(e) for e in LEAVING if bco[e['id']]['group'] == G)
            gone = [c for c in BCO if c['group'] == G and c['uncertain'] in OUT]
            gn = ''.join(f'<li>{esc(c["id"])} {esc(c["final"].replace("+", " + "))}: already marked not needed on the old sheet, so not in the game.</li>' for c in gone)
            cx.append(f'''
<article class="lc gone" id="x{G}">
  <header><span class="lb gone">{esc(G)}</span><div class="lh"><span class="flag wd big">cancelled</span><ul class="routes"><li><b>{esc(cl["old_route"])}</b></li></ul></div><div class="cnt"><b>0</b><span>trams</span></div></header>
  <div class="chg k-cancelled"><span class="ck">Cancelled</span><p>{esc(cl["what"])}</p><p class="tt"><b>Trams {bcount(G)} → 0</b></p></div>
  <h4 class="todo">Where each tram goes ({lr.count("<tr")})</h4>
  <div class="tw"><table class="ct"><thead><tr><th>Course</th><th>Vehicle · depot / type · length / pak128 core</th><th>Goes to</th></tr></thead><tbody>{lr}</tbody></table></div>
  {f'<ul class="muted small">{gn}</ul>' if gn else ''}
</article>''')
        chg['CANCELLED'] = ''.join(cx)
        chg['LINES_NEW'] = ''.join(c for _, _, _, c in cards_by['new'])
        def wrap(G, title, n, card, txt):
            return (f'<details class="same" id="w{G.replace("/", "-")}"><summary><span class="lb sm">{esc(title)}</span><span class="sr">{esc(short(G))}</span>'
                    f'<span class="sn">{n} trams</span>{txt}</summary>{card}</details>')
        chg['LINES_MINOR'] = ''.join(wrap(G, ti, n, c, f'<span class="ck sm k-minor">{esc(CH["lines"][G]["what"])}</span>') for G, ti, n, c in cards_by['minor'])
        chg['LINES_SAME'] = ''.join(wrap(G, ti, n, c, '<span class="sn muted">no change</span>') for G, ti, n, c in cards_by[None])
        chg['N_SAME'] = str(len(cards_by[None]))
        cards = [c for _, _, _, c in cards_by['route']]
        kind_of = {G: CH['lines'].get(G, {}).get('kind') for G in s['line_order']}
        line_nav = ''.join(f'<a class="lb sm{" redo" if kind_of[G] in ("route", "new") else ""}" href="#l{G.replace("/", "-")}">{t_}</a>' for G, t_, _, _ in summ)
    tpl = open(os.path.join(ASSETS, s.get('template', 'page.html')), encoding='utf-8').read()
    rep = {'%%PAKROWS%%': pak_rows, '%%LINES%%': ''.join(cards), '%%DEPOTS%%': ''.join(dep_cards), '%%SUMROWS%%': sum_rows,
           '%%CLSHEAD%%': cls_head, '%%CLSLEGEND%%': cls_legend, '%%LINENAV%%': line_nav, '%%DEPNAV%%': dep_nav,
           '%%ROWS42%%': ''.join(rowsm), '%%NOTCOUNTED%%': nc, '%%N_UNITS%%': str(sum(tot.values())), '%%N_LINES%%': str(len(summ)),
           '%%N_DEPOTS%%': str(len([d for d in dep_summ if d[0] not in s.get('museum_depots', [])])), '%%CROSSCHECK%%': crosscheck, '%%METRO%%': metro_rows, '%%FERRY%%': ferry_rows, '%%PAK_COMMIT%%': PK['pak_commit'],
           '%%SERVICE_DATE%%': TT['service_date'], '%%GTFS_RAW%%': TT['gtfs_raw']}
    rep.update({f'%%{k}%%': v for k, v in chg.items()})
    if CH: rep.update({'%%N_LINES%%': str(len(summ) + sum(len(v) - 1 for v in s.get('splits', {}).values())),'%%CLOSURE%%': esc(CH['closure']), '%%SHORTCLOSURE%%': esc(CH.get('short_closure', '')), '%%VERIFY%%': esc(CH.get('verification', '')),
                       '%%NOTICE%%': esc(CH.get('notice', ''))})
    for k, v in rep.items(): tpl = tpl.replace(k, v)
    out = os.path.join(PROJECT, s['output_html'])
    open(out, 'w', encoding='utf-8').write(tpl)
    print('wrote', out, '| trams', sum(tot.values()), dict(tot))

if __name__ == '__main__':
    main()
