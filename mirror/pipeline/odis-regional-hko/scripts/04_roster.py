"""schedule + live map + fleet -> derived/roster.json: the buses of every Simutrans line.

1. Evidence: the live map gives each bus's trips (licence + trip number = JDF spoj). A Simutrans line's trips are the real
   trips its legs stand for (05_schedule: its own trips). The line is observed on all its trips departing in its window
   (anchor -30 .. +90) widened by 30 min each side, and on its pattern trips (within 3 min of a slot) 12:30-19:30, so a shift
   line every 480 is observed too. Closer sightings rank first; an off-pattern trip counts 10 min further.
2. One bus, one Simutrans line: buses swap lines all afternoon (365-369 at Frýdek-Místek and Podlesí, 533/445/448 at
   Podlesí), so each bus may fill any line it was seen on in that line's window; an augmenting-path matching fills as many
   needs as possible, trying each bus's closest sighting first (the Havířov/Karviná/Orlová sheet's rule).
3. Buses on the other sheets on Tue 20 Oct (the Havířov/Karviná/Orlová town lines, the Hranečník ODIS cards of the Ostrava
   sheet) are not used here: a bus stays on one sheet.
4. Surplus: buses seen in a line's window that the matching did not need are "not needed" on that line, unless they fill
   another line; one of every type seen on the line is kept before a second of a type (spares rule).
5. Short lines get designed buses: (a) a bus seen on the same line's trips at another time of the day and free in this
   line's window; (b) a free bus of the line's area fleet with the line's commonest type that day; each marked with its
   reason. Free = not on any line of any sheet in the line's window.
"""
import collections, json, os
from lib import CONFIG, RAW, load, save, hm, rel, PIPE, plate_key, tlen

S = load('schedule.json'); C = load('line_class.json')
live = json.load(open(os.path.join(RAW, 'live_compact.json'), encoding='utf-8'))['plates']
fleet = json.load(open(rel(CONFIG['live']['fleet']), encoding='utf-8'))
p2n = {v['plate']: k for k, v in fleet.items() if v.get('plate')}
n2p = {k: v['plate'] for k, v in fleet.items() if v.get('plate')}
# buses of other operators (ARRIVA's town buses) and unlisted plates, looked up by 01b_plates.py; guesses in config.plate_guess
pp = os.path.join(RAW, 'plates.json')
extra = {pl: x for pl, x in (json.load(open(pp, encoding='utf-8')) if os.path.exists(pp) else {}).items() if x}
extra.update(CONFIG.get('plate_guess', {}))

# ---- buses on the other sheets (a bus stays on one sheet): the town sheet and the Ostrava cards keep [type, [numbers], ...]
# rosters; another regional sheet of this pipeline keeps {lines: {L: [{seen: [...], designed: [...]}]}, totals}
other = {}
for key, sh in CONFIG['other_sheets'].items():
    if not sh.get('derived') or not os.path.exists(rel(sh['derived'])): continue    # a sibling sheet not built yet
    r = json.load(open(rel(sh['derived']), encoding='utf-8'))
    if 'totals' in r:
        for L, ss in r['lines'].items():
            for s_ in ss:
                for v in s_['seen'] + s_['designed']: other[v['plate']] = (key, L)
        continue
    for L, units in r['roster'].items():
        for u in units:
            for num in u[1]:
                if num in n2p: other[n2p[num]] = (key, L)

# ---- sightings by trip: (licence, spoj) -> [(plate, first, last, branch)]
seen = collections.defaultdict(list); busy = collections.defaultdict(list)   # plate -> [(first, last, line)]
seen_by_plate = collections.defaultdict(list)
for pl, rows in live.items():
    for f, l, lic, line, sp, br in rows:
        seen[(lic, sp)].append((pl, f, l, br)); busy[pl].append((f, l, line)); seen_by_plate[pl].append((f, l, lic, br))

sims = []   # (L, sim index, sim)
for L, x in S.items():
    if L.startswith('_'): continue
    for i, s in enumerate(x['sim']): sims.append((L, i, s))

def evidence(L, s):
    """plates seen on the line's own pattern trips in its window: plate -> (distance from the window, label)"""
    W = s['window']; ev = {}
    trips = [(g, t) for g in s['legs'] if not g['untimed'] for t in g['trips']]
    inw = lambda t: W[0] - 30 <= t['d'] < W[1] + 30; aft = lambda t: 750 <= t['d'] < 1170
    # every own trip in the window, and the pattern trips of the afternoon (a shift line every 480 has none in the window);
    # ranked below by distance from the window, off-pattern trips 10 min further
    pick = [(g, t) for g, t in trips if inw(t) or (t['dev'] <= 3 and aft(t))]
    for g, t in pick:
        for pl, f, l, br in seen.get((t['lic'], t['sp']), []):
            if pl in other: continue
            d = (0 if W[0] <= t['d'] < W[1] else min(abs(t['d'] - W[0]), abs(t['d'] - W[1]))) + (0 if t['dev'] <= 3 else 10)
            lab = f"{t['line']}/{t['sp']} {hm(t['dep0'])} from {t['fr0'].split(', ', 1)[-1]}"
            if pl not in ev or d < ev[pl][0]: ev[pl] = (d, lab, br)
    return ev

EV = {(L, i): evidence(L, s) for L, i, s in sims}
NEED = {(L, i): s['need'] for L, i, s in sims}
# ---- matching: each bus one line; lines expanded to their need
slots = [(k, j) for k in NEED for j in range(NEED[k])]
cand = collections.defaultdict(list)
for k, ev in EV.items():
    for pl, (d, lab, br) in ev.items(): cand[pl].append((d, k))
for pl in cand: cand[pl].sort()
owner = {}       # slot -> plate
def try_assign(pl, vis):
    for d, k in cand[pl]:
        for j in range(NEED[k]):
            sl = (k, j)
            if sl in vis: continue
            vis.add(sl)
            if sl not in owner or try_assign(owner[sl], vis):
                owner[sl] = pl; return True
    return False
for pl in sorted(cand, key=lambda p: (len(cand[p]), cand[p][0][0])):
    try_assign(pl, set())
assigned = collections.defaultdict(list)
for (k, j), pl in owner.items(): assigned[k].append(pl)
used = {pl: k for k, pls in assigned.items() for pl in pls}

def info(pl):
    num = p2n.get(pl); f = fleet.get(num, {}) if num else {}
    if not f and pl in extra:      # not in the Transdev register: the looked-up vehicle page (or a guess)
        x = extra[pl]
        return dict(plate=pl, num=x.get('num') or pl, type=x.get('type') or '?', full=x.get('type') or '?', len=tlen(x.get('type')),
                    paint=x.get('paint', ''), year='', note=x.get('note', ''), operator=x.get('operator', ''), guess=bool(x.get('guess')))
    cat = f.get('cat') if f.get('cat') not in (None, '', '?') else None     # the register's type class; '?' when it has none
    return dict(plate=pl, num=num or pl, type=cat or f.get('type') or '?', full=f.get('full') or f.get('type') or '?',
                len=f.get('len', ''), paint=f.get('paint', ''), year=f.get('year', ''), note=f.get('note', ''))

# ---- 4. one of every type before a second: swap a seen surplus bus of a missing type for a duplicate-type bus
for k, ev in EV.items():
    surplus = [pl for pl in ev if pl not in used]
    for pl in surplus:
        ty = info(pl)['type']; mine = assigned[k]
        if ty in {info(p)['type'] for p in mine}: continue
        cnt = collections.Counter(info(p)['type'] for p in mine)
        dup = [p for p in mine if cnt[info(p)['type']] > 1]
        if dup:
            out_ = max(dup, key=lambda p: ev[p][0]); mine[mine.index(out_)] = pl; used[pl] = k; used.pop(out_, None)

# ---- 5. designed buses for short lines
def free_in(pl, W):
    return not any(f < W[1] and l > W[0] for f, l, line in busy.get(pl, [])) and pl not in other and pl not in used
designed = collections.defaultdict(list)
for L, i, s in sims:
    k = (L, i); short = s['need'] - len(assigned[k])
    if short <= 0: continue
    W = s['window']
    # (a) seen on the same ODIS line at another time of the day
    sameline = []
    for g in s['legs']:
        for t in g.get('trips', []):
            for pl, f, l, br in seen.get((t['lic'], t['sp']), []):
                if free_in(pl, W) and pl not in sameline and pl not in [d['plate'] for d in designed[k]]: sameline.append((pl, f, t, br))
    for pl, f, t, br in sorted(sameline, key=lambda x: abs(x[1] - W[0]))[:short]:
        designed[k].append(dict(info(pl), why=f"seen on {t['line']} at {hm(f)} ({t['line']}/{t['sp']}), free in this line's window {hm(W[0])}–{hm(W[1])}", branch=br))
        used[pl] = k; short -= 1
    if short <= 0: continue
    # (b) a free bus of the line's area fleet, of the commonest type seen on the line that day
    area = [a for a in CONFIG['areas'] if a['id'] in C[L]['areas']]
    tys = collections.Counter(info(pl)['type'] for g in s['legs'] for t in g.get('trips', []) for pl, *_ in seen.get((t['lic'], t['sp']), []))
    if CONFIG.get('designed_same_area'):
        # (b) a bus that ran the same area's lines that day (any line of the area, any time), free in this line's window:
        # the town networks' own buses (ARRIVA in Třinec) have no fleet-number prefix to pick them by
        alic = {c for x_ in C.values() if set(x_['areas']) & {a['id'] for a in area} for c in x_['lics']}
        cands = sorted({pl for (lic, sp), rows in seen.items() if lic in alic for pl, *_ in rows if free_in(pl, W) and pl not in other},
                       key=lambda pl: (-tys.get(info(pl)['type'], 0), info(pl)['num']))
        for pl in cands[:short]:
            br = next((r[3] for r in seen_by_plate[pl] if r[2] in alic), '')
            designed[k].append(dict(info(pl), why=f"designed: ran {area[0]['name']} lines that day, free in this line's window {hm(W[0])}–{hm(W[1])}", branch=br))
            used[pl] = k; short -= 1
        if short <= 0: continue
    # (c) a free bus of the area fleet, then the nearest areas' (config areas[].near: fleet-number prefixes in order)
    near = area[0].get('near') or {'havirovsko': ['42', '43', '52', '51', '73'], 'karvinsko': ['52', '51', '73', '42', '43'], 'orlovsko': ['51', '52', '73', '42', '43']}.get(area[0]['id'], [p for a in area for p in a['fleet']])
    pool = [n for n, f in fleet.items() if n[:2] in near and n[2:3] == '-' and f.get('state') == 'zar' and f.get('plate') and free_in(f['plate'], W)]
    pool.sort(key=lambda n: (near.index(n[:2]), -tys.get(fleet[n].get('cat') or fleet[n].get('type'), 0), n))
    for n in pool[:short]:
        pl = fleet[n]['plate']
        home = next((a for a in CONFIG['areas'] if n[:2] in a['fleet']), None)
        hn = home['name'] if home else {'73': 'Český Těšín', '74': 'Jablunkovsko', '33': 'Frýdek-Místek', '32': 'Frýdlantsko', '42': 'Havířovsko', '43': 'Havířovsko', '51': 'Orlovsko', '52': 'Karvinsko'}.get(n[:2], n[:2] + '-')
        designed[k].append(dict(info(pl), why=f"designed: a free {hn} bus" + (" of the line's commonest type" if tys.get(info(pl)['type']) else '') + f", not on any line {hm(W[0])}–{hm(W[1])}",
                                branch=(home['branch'].replace('Transdev Slezsko pr. ', '') if home else hn)))
        used[pl] = k; short -= 1
    if short > 0: print('STILL SHORT', L, s['name'], short)

out = {}
for L, i, s in sims:
    k = (L, i); ev = EV[k]
    out.setdefault(L, []).append(dict(
        name=s['name'], need=s['need'],
        seen=[dict(info(pl), seen=ev[pl][1], dist=ev[pl][0], branch=ev[pl][2]) for pl in assigned[k]],
        designed=designed[k],
        not_needed=[dict(info(pl), seen=ev[pl][1], branch=ev[pl][2], elsewhere=(f"{used[pl][0]} {S[used[pl][0]]['sim'][used[pl][1]]['name']}" if pl in used else '')) for pl in ev if used.get(pl) != k and pl not in assigned[k]]))
tot = sum(s['need'] for _, _, s in sims); ns = sum(len(v) for v in assigned.values()); nd = sum(len(v) for v in designed.values())
save('roster.json', dict(lines=out, other_sheet_plates={p: list(v) for p, v in other.items()}, totals=dict(need=tot, seen=ns, designed=nd)))
print(f"need {tot}: seen {ns}, designed {nd}; buses excluded as on other sheets: {len(other)}")
