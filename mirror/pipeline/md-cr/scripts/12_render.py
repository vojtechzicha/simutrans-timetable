"""MD-CR v3, step 3: render MD-CR.html (simple, chat-style tables) from data/derived/v3.json."""
import json, os, html
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
ROOT = os.path.dirname(os.path.dirname(BASE))
DER = os.path.join(BASE, 'data', 'derived')
OUT = os.path.join(ROOT, 'archive', 'MD-CR.html')  # archived 5 Oct 2026

CSS = open(os.path.join(BASE, 'assets', 'simple.css'), encoding='utf-8').read()
CATNAME = {'EC': 'EC', 'IC': 'IC', 'SC': 'SC', 'RJ': 'RJ', 'LE': 'LE', 'rj': 'rj', 'R': 'R'}
DAYS = ['', ' (next day)', ' (day 3)', ' (day 4)']


def e(s):
    return html.escape(str(s))


def hm(m):
    m = int(m)
    return f"{m // 60 % 24}:{m % 60:02d}"


def hmd(m, base):
    """clock time plus a day note relative to the start of a round trip"""
    d = int((round(m) - (base - base % 1440)) // 1440)
    return hm(m) + (DAYS[d] if 0 <= d < len(DAYS) else f' (day {d + 1})')


def dur(m):
    m = int(round(m))
    h, mm = divmod(m, 60)
    return (f'{h} h ' if h else '') + (f'{mm:02d} min' if h else f'{mm} min') if mm else f'{h} h'


def key_stops(line, train):
    timed = {x['stop'] for x in line['entries']}
    keep = timed | {line['A'], line['B'], 'Ostrava hlavní nádraží', 'Ostrava-Svinov', 'Praha hlavní nádraží', 'Brno hlavní nádraží'}
    return [s for s in train['stops'] if s['name'] in keep]


def entries_table(line):
    rows = []
    daily = line['interval'] == 1440
    for x in line['entries']:
        also = ', '.join(str(a) for a in x['also']) if x['also'] else '—'
        nums = [float(x) for x in __import__('re').findall(r'(\d+(?:\.\d+)?) min', x['stay'])]
        hl = ' class="wait"' if any(n >= 5 for n in nums) or 'reverses' in x['stay'] else ''
        rows.append(f"<tr{hl}><td>{e(x['stop'])}</td><td>{e(x['dir'])}</td><td class=\"n\">{x['every']}</td><td class=\"n\">{x['offset']}</td>"
                    + (f"<td class=\"n\">{e(also)}</td>" if daily else '')
                    + f"<td class=\"t\">{e(', '.join(x['real']))}</td><td>{e(x['stay'])}</td></tr>")
    head = ('<tr><th>Stop</th><th>Direction</th><th class="n">Departure every</th><th class="n">Offset</th>'
            + ('<th class="n">Also at</th>' if daily else '') + '<th>Real time</th><th>Stay</th></tr>')
    return f'<div class="scroll"><table><thead>{head}</thead><tbody>{"".join(rows)}</tbody></table></div>'


def trip_rows(line, train, base, wait_after=None, wait_until=None):
    rows = []
    ks = key_stops(line, train)
    for i, s in enumerate(ks):
        arr = '' if s['arr'] is None else hmd(s['arr'], base)
        dep = '' if s['dep'] is None else hmd(s['dep'], base)
        long = s['arr'] is not None and s['dep'] is not None and s['dep'] - s['arr'] >= 5
        if i == len(ks) - 1 and wait_until is not None:
            dep = hmd(wait_until, base)
            long = True
        cls = ' class="wait"' if long else ''
        rows.append(f'<tr{cls}><td>{e(s["name"])}</td><td class="n">{arr}</td><td class="n">{dep}</td></tr>')
    return rows


def round_trip_daily(line):
    outs, ins = line['outs'], line['ins']
    parts = []
    for vi, cyc in enumerate(line['cycles']):
        trains = [(outs if k[0] == 'out' else ins)[k[1]] for k, _ in cyc]
        waits = [w for _, w in cyc]
        base = trains[0]['stops'][0]['dep']
        rows = []
        t = base
        for j, tr in enumerate(trains):
            shift = 0
            dep0 = tr['stops'][0]['dep']
            # place this trip at the right absolute time
            while dep0 + shift < t - 1:
                shift += 1440
            shifted = {'num': tr['num'], 'stops': [dict(s, arr=None if s['arr'] is None else s['arr'] + shift,
                                                        dep=None if s['dep'] is None else s['dep'] + shift) for s in tr['stops']]}
            end = shifted['stops'][-1]['arr']
            nxt = end + waits[j]
            rows.append(f'<tr class="trip"><td colspan="3">{e(tr["cat"])} {e(tr["num"])}</td></tr>')
            rows += trip_rows(line, shifted, base, wait_until=nxt)
            t = nxt
        days = round((t - base) / 1440)
        if len(line['cycles']) > 1:
            label = f'Vehicle {vi + 1}: round trip {days} day{"s" if days != 1 else ""}'
        else:
            label = f'Round trip: {days} day{"s" if days != 1 else ""}, so {days} vehicle{"s" if days != 1 else ""} (each one runs this chain, a day apart)'
        parts.append(f'<h4>{label}</h4>'
                     f'<div class="scroll"><table><thead><tr><th>Station</th><th class="n">Arrives</th><th class="n">Departs</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div>')
    return ''.join(parts)


def round_trip_clock(line):
    rt = line['rt']
    rep_o = line.get('rep_out_t') or next(t for t in line['outs'] if t['num'] == line['rep_out'])
    rep_i = line.get('rep_in_t') or next(t for t in line['ins'] if t['num'] == line['rep_in'])
    base = rt['t0']
    shift_i = rt['depB'] - rep_i['stops'][0]['dep']
    ri = {'num': rep_i['num'], 'stops': [dict(s, arr=None if s['arr'] is None else s['arr'] + shift_i,
                                              dep=None if s['dep'] is None else s['dep'] + shift_i) for s in rep_i['stops']]}
    rows = [f'<tr class="trip"><td colspan="3">{e(rep_o["cat"])} {e(rep_o["num"])} times</td></tr>']
    rows += trip_rows(line, rep_o, base, wait_until=rt['depB'])
    rows.append(f'<tr class="trip"><td colspan="3">{e(rep_i["cat"])} {e(rep_i["num"])} times</td></tr>')
    rows += trip_rows(line, ri, base, wait_until=rt['depA'])
    return (f'<h4>Round trip: {dur(rt["cycle"])}, so {int(line["vehicles"])} vehicles at every {line["interval"]}</h4>'
            f'<div class="scroll"><table><thead><tr><th>Station</th><th class="n">Arrives</th><th class="n">Departs</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div>')


def real_list(line):
    items = []
    for t in line['outs'] + line['ins']:
        s0, s1 = t['stops'][0], t['stops'][-1]
        items.append(f'<li>{e(t["cat"])} {e(t["num"])}: {e(s0["name"])} {hm(s0["dep"])} → {e(s1["name"])} {hm(s1["arr"])}</li>')
    return '<ul class="small muted">' + ''.join(items) + '</ul>'


def stations(line):
    return ' – '.join(e(s['name']) + (' (x)' if s['req'] else '') for s in line['stations'])


def main():
    import sys
    ver = sys.argv[1] if len(sys.argv) > 1 else 'v4'
    data = json.load(open(os.path.join(DER, ver + '.json'), encoding='utf-8'))
    meta = data.get('meta')
    hidden = [l for l in data['lines'] if l.get('hidden')]  # user, 4 Oct 2026: kept in the pipeline, not shown
    lines = [l for l in data['lines'] if not l.get('hidden')]
    groups = defaultdict(list)
    for l in lines:
        groups[l['group']].append(l)

    # clash check: two lines leaving the same stop, same direction, same minute
    seen = defaultdict(list)
    for l in lines:
        for x in l['entries']:
            for t in ([x['offset']] + x['also']):
                for k in range(1440 // x['every']):
                    seen[(x['stop'], x['dir'], (t + 60 + k * x['every']) % 1440)].append(l['id'])
    clashes = {k: v for k, v in seen.items() if len(set(v)) > 1}

    out = [f'<title>MD-CR</title>\n<style>\n{CSS}\n</style>\n<main>']
    if meta:
        out.append(f'<h1>{e(meta["title"])}</h1>')
        out.append(f'<p class="muted">{e(meta["intro"])}</p>')
        out.append('<p>Notation: <b>L</b> = odd hours, <b>S</b> = even hours, (x) = request stop. <span class="wait">Highlighted</span> rows are stops with a stay of 5 min or more; they need a timetable entry so the train keeps time. "Leave up to" is 30 min on every entry.</p>')
        out.append(f'<p class="fix"><b>Offsets:</b> {e(meta["offsets"])}</p>')
        if hidden:
            out.append(f'<p class="fix"><b>Hidden for now:</b> {e(meta.get("hidden_note", ""))} '
                       f'({len(hidden)} lines, {sum(int(l["vehicles"]) for l in hidden)} vehicles: '
                       + e(', '.join(f'{l["badge"]} {l["B"]}' for l in hidden)) + ')</p>')
    else:
        out.append('<h1>MD-CR · Praha – Ostrava corridor and Ex2</h1>')
        out.append('<p class="muted">Simutrans design for the workday long-distance trains via Ostrava: ČD Ex1 (EC, IC), the ČD SC Pendolino, RegioJet and Leo Express. Ex2 (Praha – Vsetín – Žilina) is included too. '
                   'Czech times come from the national CIS JŘ timetable JR2026. Each train runs on all five days Mon–Fri, 5–9 October 2026. '
                   'Foreign times come from vagonweb.cz and the Leo Express timetable. The only foreign termini are Warszawa, Kraków, Žilina and Košice. Trains via Brno are left for a later pass.</p>')
        out.append('<p>Notation: <b>L</b> = odd hours, <b>S</b> = even hours, (x) = request stop. <span class="wait">Highlighted</span> rows are stops with a stay of 5 min or more that need a timetable entry. '
                   'Every line also has an entry at the first station after the border. "Leave up to" is 30 min on every entry.</p>')
        out.append('<p class="fix"><b>Offsets:</b> lines every 120 min use your rule: odd hours first, even hours +60. '
                   'Lines that run only a few trains a day use <b>Departure every 1440</b> with "Also at", so the game runs exactly the real trains. '
                   'For those I applied the same rule, counting the day from 01:00: offset = real time − 60 min (6:08 → 308). <b>Please confirm this is how the fork counts a 1440 cycle.</b> The real times are in every table, so the offsets are easy to correct.</p>')
    out.append('<nav>' + ''.join(f'<a href="#{l["id"]}">{e(l.get("nav") or l["badge"] + " " + l["B"].split(" ")[0])}</a>' for l in lines) + '<a href="#notmodelled">Not modelled</a></nav>')

    # vehicles
    rows, total = [], 0
    for g, ls in groups.items():
        sub = 0
        for l in ls:
            rows.append(f'<tr><td><a href="#{l["id"]}">{e(l["badge"])}</a></td><td>{e(l["A"])} – {e(l["B"])}</td><td>{e(l["trainname"])}</td>'
                        f'<td class="n">{l["interval"]}</td><td class="n">{len(l["outs"]) if l["interval"] == 1440 else {60: "every hour", 120: "every 2 h", 240: "every 4 h", 480: "every 8 h"}.get(l["interval"], "")}</td><td class="n">{int(l["vehicles"])}</td></tr>')
            sub += int(l['vehicles'])
        rows.append(f'<tr class="total"><td colspan="5">{e(g)}</td><td class="n">{sub}</td></tr>')
        total += sub
    rows.append(f'<tr class="total"><td colspan="5">All lines</td><td class="n">{total}</td></tr>')
    out.append('<h2 id="vehicles">Vehicles</h2><div class="scroll"><table><thead><tr><th>Line</th><th>Route</th><th>Trains</th><th class="n">Every</th><th class="n">Trains each way</th><th class="n">Vehicles</th></tr></thead><tbody>'
               + ''.join(rows) + '</tbody></table></div>')
    out.append('<p class="small muted">Vehicles come from each line\'s full round trip. A vehicle waits at the terminus for the line\'s next departure, so the round trip is a whole number of intervals (or days for the daily lines).</p>')

    # corridor overview
    if meta and meta.get('overview'):
        for sec in [x for x in meta['overview'] if not x.get('hidden')]:
            out.append(f'<h2>{e(sec["title"])}</h2><ul>' + ''.join(f'<li>{it}</li>' for it in sec['items']) + '</ul>')
    else:
        out.append('<h2>How the corridor works at Praha</h2><ul>'
                   '<li><b>ČD Ex1</b> leaves Praha hl. n. every 2 h at S:08. The branches alternate: Žilina at 8:08, 12:08 and 16:08, Warszawa at 6:08 and 14:08, Kraków at 10:08 and Návsí at 18:08.</li>'
                   '<li><b>ČD Ex2</b> leaves every 2 h at L:08, towards Vsetín and Žilina.</li>'
                   '<li><b>ČD SC Pendolino</b> leaves every 2 h at L:31 to Ostrava hl. n. The Košice Pendolino leaves at 5:52.</li>'
                   '<li><b>RegioJet</b> starts at Praha-Zahradní Město at :21 and leaves Praha hl. n. at :41. The ends vary: Havířov, Košice, Bohumín, Návsí and Opava východ. Each end is its own line with its real trains.</li>'
                   '<li><b>Leo Express</b> leaves Praha hl. n. at :23 for Kraków, Warszawa, Košice and Bohumín. It stops at Přerov instead of Česká Třebová.</li>'
                   '</ul>')

    if clashes:
        out.append('<p class="fix"><b>Same-minute departures:</b> ' + '; '.join(f'{e(k[0])} {e(k[1])} {hm(k[2])}: {", ".join(sorted(set(v)))}' for k, v in sorted(clashes.items())) + '</p>')

    for g, ls in groups.items():
        out.append(f'<h2>{e(g)}</h2>')
        for l in ls:
            out.append(f'<h3 id="{l["id"]}">{e(l["badge"])} · {e(l["A"])} – {e(l["B"])} · {int(l["vehicles"])} vehicle{"s" if l["vehicles"] != 1 else ""}</h3>')
            out.append(f'<p class="muted">{e(l["trainname"])}. ' + (f'Every {l["interval"]} min, copying {e(l["rep_out"])} and {e(l["rep_in"])}.' if l['interval'] != 1440 else f'{len(l["outs"])} train{"s" if len(l["outs"]) != 1 else ""} a day each way, exactly as in reality.') + '</p>')
            out.append(f'<p class="stations"><b>Stations:</b> {stations(l)}, then the same back.</p>')
            out.append('<h4>Timetable entries</h4>' + entries_table(l))
            out.append(round_trip_daily(l) if l['interval'] == 1440 else round_trip_clock(l))
            if l.get('folded'):
                out.append(f'<p class="small"><b>Folded in:</b> {e(l["folded"])}</p>')
            if l.get('note'):
                out.append(f'<p class="small">{e(l["note"])}</p>')
            out.append('<p class="small muted">Real trains this line stands for:</p>' + real_list(l))

    out.append('<h2 id="notmodelled">Not modelled</h2><ul>' + ''.join(f'<li>{e(x)}</li>' for x in data['not_modelled']) + '</ul>')
    out.append('</main>')
    open(OUT, 'w', encoding='utf-8').write('\n'.join(out))
    print('wrote', OUT, 'vehicles', total, 'clashes', clashes)


if __name__ == '__main__':
    main()
