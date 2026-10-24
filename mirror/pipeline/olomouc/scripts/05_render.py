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
                d = []
                ex = list(r['extra']); mi = list(r['missing'])
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
                if x['depot']:
                    notes.append(f'<li><span class="k">{i}</span> depot run {esc(x["o"])} → {esc(x["d"])}: {times}</li>')
                else:
                    notes.append(f'<li><span class="k">{i}</span> short working {esc(x["o"])} → {esc(x["d"])}: {times}. Not a peak trip (no departure in the 16:00 hour), so not modelled.</li>')
        lh = '<th>Line</th>' if len(ids) > 1 else ''
        head = ''
        if pool and pool.get('legs'):
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
        rows, mix = [], collections.Counter()
        brcfg = {b['label']: b for b in s.get('splits', {}).get(G, [])}
        if brcfg:
            cs = sorted(cs, key=lambda c: (c['uncertain'] == 'spare', list(brcfg).index(c['branch']) if c.get('branch') in brcfg else 99, int(c['line']), c['course']))
        cur = None
        for c in cs:
            if brcfg and c.get('branch') != cur:
                cur = c.get('branch'); b = brcfg.get(cur, {}); nb = TT.get('branches', {}).get(G, {}).get(cur, {})
                na = sum(1 for x in cs if x.get('branch') == cur and x['uncertain'] not in ('am', 'spare'))
                rows.append(f'<tr class="brh"><td colspan="3"><b>{esc(cur or "no branch")}</b> · {na} assigned, {nb.get("need", "?")} needed by round trip<br><span class="muted">{esc(b.get("why", ""))}</span></td></tr>')
            final = next(v for v in c['veh'] if v['set'] == c['final'])
            if c['uncertain'] not in ('am', 'spare'): mix[unit_class(final['types'])] += 1
            elif c['uncertain'] == 'am': notcounted.append(c)
            chain = '<div class="arr">then</div>'.join(unit_html(x, next(v for v in c['veh'] if v['set'] == x)['types'], next(v for v in c['veh'] if v['set'] == x)['depot']) for x in c['chain'])
            tr = f'<span class="tag">→{c["transfer"]}</span>' if c['transfer'] and G in pools and c['transfer'] in pools[G]['lines'] else ''
            if G in pools: tr += '<span class="flag pool">pool</span>'
            split = '<span class="flag pm">PM part</span>' if c['split'] else ''
            rows.append(f'<tr class="{"spare" if c["uncertain"] == "spare" else ("unc" if c["uncertain"] else "")}"><td class="k">{c["id"]}{tr}</td><td class="v">{chain}</td><td class="n">{split}{TAG.get(c["uncertain"], "")}<span class="nt">{esc(c["note"])}</span></td></tr>')
            for v in c['veh']:
                replaced = c['swap'] and v['set'] != c['final']
                depot[v['depot']][c.get('branch') or G].append(dict(set=v['set'], types=v['types'], course=c['id'], u=c['uncertain'], replaced=replaced))
        n = sum(mix.values())
        tl = [TT['lines'][i] for i in ids if i in TT['lines']]
        if G in pools and TT['pools'][G].get('need'): needtxt = f'<span class="need">shared pool: {TT["pools"][G]["need"]} trams needed for the whole circulation</span>'
        elif TT.get('branches', {}).get(G): needtxt = '<span class="need">' + '; '.join(f'{esc(l)}: {b["need"]} needed' for l, b in TT['branches'][G].items()) + '</span>'
        else: needtxt = f'<span class="need">timetable at 16:00: {tl[0]["cycle_need"]} sets needed by round trip</span>' if tl and tl[0]['cycle_need'] else ''
        mix_html = ' '.join(f'<span class="mx u-{k}"><b>{mix[k]}</b>× {CLASS[k][0]}</span>' for k in ORDER if mix[k])
        fl = flags.get(G); fl_html = f'<p class="callout {fl[0]}">{esc(fl[1])}</p>' if fl else ''
        pnote = f'<p class="callout info">{esc(pools[G]["note"])}</p>' if G in pools else ''
        title = G.replace('/', ' + ') if G in pools else G
        pooltag = '<span class="flag pool big">shared pool</span>' if G in pools else ''
        cards.append(f'''
<article class="lc" id="l{G.replace('/', '-')}">
  <header><span class="lb">{title}</span><div class="lh">{pooltag}<ul class="routes">{routes}</ul>{needtxt}</div><div class="cnt"><b>{n}</b><span>trams</span></div></header>
  <div class="mix">{mix_html}</div>
  {pnote}{fl_html}
  {sched_block(ids, G)}
  <div class="tw"><table class="ct"><thead><tr><th>Course</th><th>Vehicle · depot / type · length / pak128 core</th><th>Notes</th></tr></thead><tbody>{''.join(rows)}</tbody></table></div>
</article>''')
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
                real = it['u'] not in ('am', 'spare') and not it['replaced']
                if real and G not in museum: cnt[unit_class(it['types'])] += 1; nunits += 1
                st = ''
                if it['replaced']: st = '<span class="flag swap">replaced during the day</span>'
                elif it['u'] == 'am': st = '<span class="flag am">not counted: probably morning only</span>'
                elif it['u'] == 'spare': st = '<span class="flag am">not needed at 16:00</span>'
                elif it['u'] == 'swap': st = '<span class="flag swap">replacement, time not recorded</span>'
                elif it['u'] == 'moved': st = '<span class="flag mv">moved from another line</span>'
                elif it['u'] == 'added': st = '<span class="flag mv">added for the new route</span>'
                elif it['u'] == 'designed': st = '<span class="flag ds">designed addition</span>'
                if G in pools: lbl = f'<span class="lb sm">{G.replace("/", " + ")}</span><span class="lsub">shared pool</span>'
                elif ' ' in G: lbl = f'<span class="lb sm">{esc(G.split(" ")[0])}</span><span class="lsub">{esc(G.split(" ", 1)[1])}</span>'
                else: lbl = f'<span class="lb sm">{G}</span>'
                lc = f'<td class="lcell" rowspan="{len(items)}">{lbl}</td>' if j == 0 else ''
                trs.append(f'<tr class="{"first" if j == 0 else ""}{" dim" if not real else ""}">{lc}<td class="k">{esc(it["course"])}</td><td class="v">{unit_html(it["set"], it["types"])}</td><td class="n">{st}</td></tr>')
        mix_html = ' '.join(f'<span class="mx u-{k}"><b>{cnt[k]}</b>× {CLASS[k][0]}</span>' for k in ORDER if cnt[k])
        note = f'<p class="muted small">{esc(s["depot_notes"][D])}</p>' if D in s.get('depot_notes', {}) else ''
        dep_cards.append(f'''
<article class="dc" id="d-{D}">
  <header><h3>Vozovna {esc(D)}</h3><div class="cnt"><b>{nunits}</b><span>trams</span></div></header>
  <p class="dlines">Lines {esc(", ".join(sorted({(o.split(" ")[0].replace("/", " + ") + (" (shared pool)" if o in pools else "")) for o in order}, key=lambda x: int(x.split(" ")[0]))))}</p>
  <div class="mix">{mix_html}</div>{note}
  <div class="tw"><table class="dt"><thead><tr><th>Line</th><th>Course</th><th>Vehicle / type · length / pak128 core</th><th></th></tr></thead><tbody>{''.join(trs)}</tbody></table></div>
</article>''')
        dep_summ.append((D, nunits))

    # summary + pak table
    tot = collections.Counter()
    for *_, m in summ: tot.update(m)
    sum_rows = ''.join(f'<tr><td><a class="lb sm" href="#l{G.replace("/", "-")}">{t}</a>{"<span class=lsub>shared pool</span>" if G in pools else ""}</td><td class="num">{n}</td>' + ''.join(f'<td class="num">{m[k] or ""}</td>' for k in ORDER) + '</tr>' for G, t, n, m in summ)
    sum_rows += '<tr class="tot"><td>Total</td><td class="num">' + str(sum(tot.values())) + '</td>' + ''.join(f'<td class="num">{tot[k] or ""}</td>' for k in ORDER) + '</tr>'
    cls_head = ''.join(f'<th class="num"><span class="cls u-{k}">{esc(CLASS[k][0])}</span></th>' for k in ORDER)
    cls_legend = ''.join(f'<tr><td><span class="cls u-{k}">{esc(CLASS[k][0])}</span></td><td>{esc(CLASS[k][1])}</td><td>{esc(CLASS[k][2])}</td><td>{esc(CLASS[k][3])}</td></tr>' for k in ORDER)
    pk = collections.Counter(); reasons = collections.defaultdict(set)
    for c in CO:
        if c['uncertain'] in ('am', 'spare'): continue
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
    tpl = open(os.path.join(ASSETS, 'page.html'), encoding='utf-8').read()
    rep = {'%%PAKROWS%%': pak_rows, '%%LINES%%': ''.join(cards), '%%DEPOTS%%': ''.join(dep_cards), '%%SUMROWS%%': sum_rows,
           '%%CLSHEAD%%': cls_head, '%%CLSLEGEND%%': cls_legend, '%%LINENAV%%': line_nav, '%%DEPNAV%%': dep_nav,
           '%%ROWS42%%': ''.join(rowsm), '%%NOTCOUNTED%%': nc, '%%N_UNITS%%': str(sum(tot.values())), '%%N_LINES%%': str(len(summ)),
           '%%N_DEPOTS%%': str(len([d for d in dep_summ if d[0] not in s.get('museum_depots', [])])), '%%CROSSCHECK%%': crosscheck, '%%METRO%%': metro_rows, '%%FERRY%%': ferry_rows, '%%PAK_COMMIT%%': PK['pak_commit'],
           '%%SERVICE_DATE%%': TT['service_date'], '%%GTFS_RAW%%': TT['gtfs_raw']}
    for k, v in rep.items(): tpl = tpl.replace(k, v)
    out = os.path.join(PROJECT, s['output_html'])
    open(out, 'w', encoding='utf-8').write(tpl)
    print('wrote', out, '| trams', sum(tot.values()), dict(tot))

if __name__ == '__main__':
    main()
