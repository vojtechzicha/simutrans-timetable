"""Whole-day reading of every line of one oblast (bus schedule method, Steps 1-3), for the hand design and the cards.

-> oblasti/<id>/data/derived/reading.json and reading/<L>.txt, per line:
- the core points (lines.json core, else the line's ends by use, then the oblast's hubs) and the paths, the commonest of
  each direction in full and the others as differences;
- every trip of the day with its time at each core point it passes (Step 3), its GTFS trip id, and the bus the live map
  saw on it (when the poll exists: vehicle number, type, course);
- the 0-minute chain test at the line's ends (owner, 30 Oct 2026, Prague 174/301: "I am 100% sure 301/352 are
  continuations of 174"): for each other line, how many of this line's arrivals at a stop are followed by that line's
  departure from the same stop within 0-2 min, and how many departures are preceded by its arrival (100 % = through
  running; under ~50 % is chance at a hub);
- with the poll: each afternoon bus's trips in order (where the buses came from and went on to; Step 5b).
usage: python 03_read.py <oblast id>
"""
import collections, glob, json, os, sys
from common import HOME, DER, PIPE

OID = sys.argv[1]; BASE = os.path.join(HOME, 'oblasti', OID); D = os.path.join(BASE, 'data', 'derived')
CFG = json.load(open(os.path.join(BASE, 'config.json'), encoding='utf-8'))
SH = json.load(open(os.path.join(HOME, 'config.json'), encoding='utf-8'))
T = json.load(open(os.path.join(D, 'trips.json'), encoding='utf-8'))
C = json.load(open(os.path.join(D, 'line_class.json'), encoding='utf-8'))
AL = lambda s: CFG.get('terminus_alias', {}).get(s, s)
hm = lambda t: '%d:%02d' % (t // 60 % 24, t % 60)

# ---------------------------------------------------------------- live map (if polled): trip id -> buses, bus -> trips
seen = collections.defaultdict(list); bus_trips = collections.defaultdict(list); info = {}
for day in SH.get('live', {}).get('days', [])[:1]:          # the vehicle day
    pd = os.path.join(HOME, SH['live']['dir'], day)
    if not os.path.exists(os.path.join(pd, 'polls.jsonl')): continue
    first = {}
    for ln in open(os.path.join(pd, 'polls.jsonl'), encoding='utf-8'):
        r = json.loads(ln); t = int(r['t'][11:13]) * 60 + int(r['t'][14:16])
        for v, route, tid, stp, *_ in r['buses']:
            k = (v, tid)
            if k not in first: first[k] = [t, t, route]
            else: first[k][1] = t
    for (v, tid), (f, l, route) in first.items():
        seen[tid].append((v, f, l)); bus_trips[v].append((f, l, route, tid))
    if os.path.exists(os.path.join(pd, 'vehicles.jsonl')):
        for ln in open(os.path.join(pd, 'vehicles.jsonl'), encoding='utf-8'):
            w = json.loads(ln)
            # a later retry with a type wins over an earlier row without one (vehicle windows that failed at first)
            if w['vehicle'] not in info or (w.get('type') and not info[w['vehicle']].get('type')): info[w['vehicle']] = w
tid_line = {}
ends = json.load(open(os.path.join(DER, 'ends.json'), encoding='utf-8'))
alltid = {}
for oid in [o['id'] for o in SH['oblasti']]:
    tp = os.path.join(HOME, 'oblasti', oid, 'data', 'derived', 'trips.json')
    if os.path.exists(tp):
        for L_, tr in json.load(open(tp, encoding='utf-8')).items():
            for t in tr: alltid[t['tid']] = (L_, t)

# ---------------------------------------------------------------- 0-minute chains at the ends
dep_at = collections.defaultdict(list); arr_at = collections.defaultdict(list)
for L_, sp, lic, fr, dep, to, arr in ends:
    dep_at[AL(fr)].append((dep, L_, sp)); arr_at[AL(to)].append((arr, L_, sp))
def chain_test(L, tr):
    """per (end stop, other line): this line's arrivals followed by its departure within 0-2 min, and departures preceded"""
    out = []
    by_end = collections.defaultdict(list); by_start = collections.defaultdict(list)
    for t in tr: by_end[AL(t['to'])].append(t['arr']); by_start[AL(t['fr'])].append(t['dep'])
    for stop, arrs in by_end.items():
        c = collections.Counter()
        for a in arrs:
            for L2 in {L2 for d, L2, _ in dep_at.get(stop, []) if 0 <= d - a <= 5}: c[L2] += 1
        for L2, n in c.items():
            if n >= 2 and n / len(arrs) >= 0.3: out.append(f"  at {stop}: {n} of {len(arrs)} arrivals of {C[L].get('label', L)} are followed within 0-5 min by a {L2} departure")
    for stop, deps in by_start.items():
        c = collections.Counter()
        for d in deps:
            for L2 in {L2 for a, L2, _ in arr_at.get(stop, []) if 0 <= d - a <= 5}: c[L2] += 1
        for L2, n in c.items():
            if n >= 2 and n / len(deps) >= 0.3: out.append(f"  at {stop}: {n} of {len(deps)} departures of {C[L].get('label', L)} follow a {L2} arrival within 0-5 min")
    return out

SL = json.load(open(os.path.join(DER, 'stop_lines.json'), encoding='utf-8'))
SO = json.load(open(os.path.join(DER, 'stop_okres.json'), encoding='utf-8'))
OKN = {o['prefix']: o['okres'] for o in SH['oblasti']}
def short(s):
    for a, b in (('autobusové stanoviště', 'AS'), ('autobusové nádraží', 'AN'), ('železniční stanice', 'žst'), ('železniční zastávka', 'žz'),
                 ('náměstí', 'nám.'), ('rozcestí', 'rozc.')):
        s = s.replace(a, b)
    return s[:30]
# the oblast's hubs: the stops where most of its lines end
endc = collections.Counter()
for L, tr in T.items():
    for st in {AL(t['fr']) for t in tr} | {AL(t['to']) for t in tr}: endc[st] += 1
HUBS = CFG.get('hubs') or [s for s, n in endc.most_common(8) if n >= 3]

os.makedirs(os.path.join(D, 'reading'), exist_ok=True)
out = {}
def lkey(L): return (len(L), L)
for L in sorted(T, key=lkey):
    tr = T[L]; cfg = CFG.get('lines', {}).get(L, {})
    endsL = collections.Counter(AL(x) for t in tr for x in (t['fr'], t['to']))
    core = cfg.get('core') or [s for s, _ in endsL.most_common(4)] + [h for h in HUBS if h not in endsL and any(h in t['stops'] for t in tr)]
    rows = []
    for t in tr:
        st = [AL(x) for x in t['stops']]
        at = {c: hm(t['times'][st.index(c)]) for c in core if c in st}
        obs = [(v, hm(f), hm(l)) for v, f, l in seen.get(t['tid'], [])]
        rows.append(dict(sp=t['sp'], lic=t['lic'], tid=t['tid'], dep=t['dep'], arr=t['arr'], fr=AL(t['fr']), to=AL(t['to']), n=len(st), at=at, obs=obs, stops=st))
    out[L] = dict(core=core, rows=rows)
    c = C[L]
    with open(os.path.join(D, 'reading', f'{L}.txt'), 'w', encoding='utf-8') as f:
        f.write(f"{c.get('label', L)}  {c['name']}  (licence {', '.join(c['lics'])}; {', '.join(c.get('operators', []))}; {c['trips']} trips, "
                f"{c['afternoon']} in 13-19, {c['first']}-{c['last']})\nwhy here: {c.get('why', '')}\ncore: " + ' | '.join(short(x) for x in core) + '\n')
        # full stop names from here on (lines.json legs must use them exactly; the trip rows below shorten them)
        f.write('core (full names): ' + ' | '.join(core) + '\n')
        own = sorted({x for t in tr for x, tm in zip([AL(y) for y in t['stops']], t['times']) if 780 <= tm < 1140 and SL.get(x) == [L]})
        f.write('stops only this line serves 13:00-19:00 (okres): ' + ('; '.join(
            f"{x} ({OKN.get(SO.get(x)) or ('Prague' if x.startswith('Praha, ') else 'outside the Středočeský kraj')})" for x in own) or 'none') + '\n')
        stopsets = collections.Counter(tuple(r['stops']) for r in rows)
        pid = {k: i for i, (k, _) in enumerate(stopsets.most_common())}
        main = {}
        for k, n in stopsets.most_common():
            d_ = (k[0], k[-1]); i = pid[k]
            if d_ not in main and (d_[1], d_[0]) not in main:
                main[d_] = k; f.write(f"  path {i}: {n} trips, {len(k)} stops: {' > '.join(k)}\n"); continue
            ref = main.get(d_) or main.get((d_[1], d_[0])) or max(main.values(), key=lambda m: len(set(m) & set(k)))
            add = [x for x in k if x not in ref]; miss = [x for x in ref if x not in k]
            f.write(f"  path {i}: {n} trips, {k[0]} > {k[-1]}, {len(k)} stops; +[{'; '.join(add)}] -[{'; '.join(miss)}]\n")
        for r in rows:
            cells = '  '.join(f"{short(x)}={r['at'][x]}" for x in core if x in r['at'])
            bus = ' '.join(f"{v}" + (f"({info[v]['type'][:18]}; {info[v]['course']})" if v in info else '') for v, _, _ in r['obs'])
            f.write(f"{hm(r['dep']):>5} {short(r['fr']):30} > {short(r['to']):30} {hm(r['arr']):>5} p{pid[tuple(r['stops'])]} [{r['sp']}] {cells}"
                    + (f"  BUS {bus}" if bus else '') + '\n')
        ch = chain_test(L, tr)
        f.write('\n0-5 minute chains at the ends (through-running test; 100 % at 0 min = through running):\n' + ('\n'.join(ch) if ch else '  none at 30 % or more') + '\n')
        if seen:
            vs = sorted({v for r in rows if 720 <= r['dep'] < 1200 for v, _, _ in r['obs']})
            f.write('\nafternoon buses of the line, all their trips in order (12:00-20:00, from the live map):\n')
            for v in vs:
                seq = sorted(x for x in bus_trips[v] if x[1] >= 700)
                cells = []
                for fz, lz, route, tid in seq:
                    lt = alltid.get(tid)
                    cells.append(f"{route} {hm(lt[1]['dep']) if lt else hm(fz)} {short(lt[1]['fr']) + '>' + short(lt[1]['to']) if lt else ''}")
                f.write(f"  {v:>5} {info.get(v, {}).get('type', '')[:22]:22} " + ' ; '.join(cells) + '\n')
json.dump(out, open(os.path.join(D, 'reading.json'), 'w', encoding='utf-8'), ensure_ascii=False)
print(OID, 'read', len(out), 'lines; hubs:', ' | '.join(HUBS), '; live:', 'yes' if seen else 'not yet')
