"""Whole-day reading of every line (bus schedule method, Steps 1-3), for the hand design and for the cards.

-> derived/reading.json: per ODIS line, every trip of the vehicle day with its time at each core point it passes (the core
points are config.lines[L].core when set, else the line's termini and the area hubs), the bus seen on it (live map: licence +
trip number), and the afternoon plate chains (where the buses of the line came from and went on to).
-> derived/reading/<L>.txt: the same as text, for reading.
Also derived/chains.json: every Transdev Slezsko plate's sightings 5:00-19:50 in order, with the trip's ends.
"""
import collections, json, os
from lib import CONFIG, RAW, load, save, nm, AL, hm, rel, dpath

T = load('trips.json'); C = load('line_class.json')
live = json.load(open(os.path.join(RAW, 'live_compact.json'), encoding='utf-8'))['plates']
fleet = json.load(open(rel(CONFIG['live']['fleet']), encoding='utf-8'))
p2n = {v['plate']: k for k, v in fleet.items() if v.get('plate')}
HUBS = CONFIG.get('hubs', ["Havířov, Podlesí, autobusové nádraží", "Havířov, Město, železniční stanice", "Karviná, Fryštát, autobusové nádraží",
                           "Orlová, Lutyně, autobusové nádraží", "Bohumín, Nový Bohumín, autobusová stanice", "Bohumín, Nový Bohumín, železniční stanice"])

# every trip of the sheet's lines by (licence, trip) -> its line, for naming the trips of a plate chain
bykey = {}
for L, tr in T.items():
    for t in tr: bykey[(t['lic'], t['sp'])] = (L, t)
seen = collections.defaultdict(list)    # (licence, trip) -> [(plate, first, last)]
chains = {}
for pl, rows in live.items():
    ch = []
    for f, l, lic, line, sp, br in rows:
        seen[(lic, sp)].append((pl, f, l))
        k = bykey.get((lic, sp))
        ch.append(dict(f=f, l=l, lic=lic, line=line, sp=sp, br=br, fr=nm(k[1]['fr']) if k else None, to=nm(k[1]['to']) if k else None,
                       dep=k[1]['dep'] if k else None, arr=k[1]['arr'] if k else None))
    chains[pl] = dict(num=p2n.get(pl, ''), seen=ch)
save('chains.json', chains)

def label(pl): return f"{p2n.get(pl, '?')}" if pl in p2n else pl
SHORT = [('autobusové nádraží', 'AN'), ('autobusová stanice', 'AS'), ('železniční stanice', 'žst'), ('železniční zastávka', 'žz'),
         ('Frýdek-Místek', 'F-M'), ('Nový Bohumín', 'NB'), ('Mor.Ostrava', 'MO'), ('Petrovice u Karv.', 'Petrovice')]
def short(s):
    """a compact label for a stop in the reading text: town + last part, common words abbreviated"""
    p = s.split(', '); x = p[0] + (' ' + ' '.join(p[1:]) if len(p) > 1 else '')
    for a, b in SHORT: x = x.replace(a, b)
    return x[:26]

os.makedirs(dpath('reading'), exist_ok=True)
out = {}
for L in sorted(T):
    tr = T[L]; cfg = CONFIG.get('lines', {}).get(L, {})
    ends = collections.Counter(AL(nm(x)) for t in tr for x in (t['fr'], t['to']))
    core = cfg.get('core') or [s for s, _ in ends.most_common()] + [h for h in HUBS if h not in ends]
    rows = []
    for t in tr:
        st = [AL(nm(x)) for x in t['stops']]
        at = {c: hm(t['times'][st.index(c)]) for c in core if c in st}
        obs = [(label(p), hm(f), hm(l)) for p, f, l in seen.get((t['lic'], t['sp']), [])]
        rows.append(dict(sp=t['sp'], lic=t['lic'], dep=t['dep'], arr=t['arr'], fr=nm(t['fr']), to=nm(t['to']), n=len(st), at=at, obs=obs, stops=st))
    out[L] = dict(core=core, rows=rows)
    with open(dpath(f'reading/{L}.txt'), 'w', encoding='utf-8') as f:
        f.write(f"{L} {C[L]['name']}  ({', '.join(C[L]['lics'])}; {C[L]['trips']} trips)\ncore: " + ' | '.join(short(c) for c in core) + '\n')
        stopsets = collections.Counter(tuple(r['stops']) for r in rows)
        pid = {k: i for i, (k, _) in enumerate(stopsets.most_common())}
        main = {}
        for k, n in stopsets.most_common():   # the commonest path of each direction is written in full, the others as differences
            d_ = (k[0], k[-1]); i = pid[k]
            if d_ not in main and (d_[1], d_[0]) not in main:
                main[d_] = k; f.write(f"  path {i}: {n} trips, {len(k)} stops: {' > '.join(short(x) for x in k)}\n"); continue
            ref = main.get(d_) or main.get((d_[1], d_[0])) or max(main.values(), key=lambda m: len(set(m) & set(k)))
            add = [short(x) for x in k if x not in ref]; miss = [short(x) for x in ref if x not in k]
            f.write(f"  path {i}: {n} trips, {short(k[0])} > {short(k[-1])}, {len(k)} stops; +[{', '.join(add)}] -[{', '.join(miss)}]\n")
        for r in rows:
            cells = '  '.join(f"{short(c)}={r['at'][c]}" for c in core if c in r['at'])
            f.write(f"{hm(r['dep']):>5} {short(r['fr']):26} > {short(r['to']):26} {hm(r['arr']):>5} p{pid[tuple(r['stops'])]} [{r['lic'][-3:]}/{r['sp']}] {cells}"
                    + (f"  BUS {' '.join(o[0] for o in r['obs'])}" if r['obs'] else '') + '\n')
        # afternoon plate chains of the buses seen on this line
        pls = sorted({o[0] for r in rows if 780 <= r['dep'] < 1140 for o in [(p,) for p, _, _ in seen.get((r['lic'], r['sp']), [])]})
        f.write('\nchains (13:00-19:50):\n')
        for pl in pls:
            seq = [c for c in chains[pl]['seen'] if c['l'] >= 760]
            f.write(f"  {label(pl):9} " + ' ; '.join(f"{c['line']}/{c['sp']} {hm(c['dep']) if c['dep'] is not None else hm(c['f'])} {short(c['fr']) if c['fr'] else '?'}>{short(c['to']) if c['to'] else '?'}" for c in seq) + '\n')
save('reading.json', out)
print('read', len(out), 'lines; chains for', len(chains), 'plates')
