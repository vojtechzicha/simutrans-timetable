"""Afternoon-peak fleet for one state: which bus runs each Simutrans line, with pak objects.

  python 04_fleet.py --state 2026-09-29

1. Logged buses: the vehicle day's per-line records (seznam-autobusu.cz, mhd-ol). DPMO bus records carry no kurz and no
   time of day, so every logged bus of a line counts for that line. A real line split into several Simutrans lines (11)
   gives its logged buses to its first (main) Simutrans line; the split is a choice.
2. Logged surplus (user, 29 Sep): where a Simutrans line has more buses logged than it needs, exactly the need stays
   counted (common.mark_spares: one of every type first, most frequent type first; with no kurz numbers the buses
   listed later on the record page are dropped first); the rest are "not needed".
3. Designed buses (user, 29 Sep: never ship without vehicles; real car numbers): where a Simutrans line has fewer buses
   than it needs, active DPMO buses that were not out anywhere on the vehicle day (day overview) are added, marked
   "designed, not recorded" with the dates the car last ran the line. Candidates, in order:
     A. weekday records on the line since 2026-01-01; B. weekday records on the line in 2025;
     C. free buses of the line's roster types (fleet register); D. free buses of the line's size (12 m or 18 m).
   The picks first cover every roster type the line's used buses lack (roster = the logged types plus every type with at
   least two weekday records on the line since 1 Jan 2026, or in 2025 when 2026 has fewer than five records; a single
   record is a one-off substitute), taking the type with the most records first; then they go by recency (latest record
   first, then the number of records). Lines are served in order of their need, largest first.
   Free history cars left over (A or B, not used anywhere) are listed as "not needed" on the line they last ran (once).
4. Pak object per bus: assets/pak_map.json (family by type, livery by paint, advert wrap -> normal livery); an object not in
   the pak checkout (assets/pak_objects.json snapshot, refreshed from the checkout when it is present) is "requested".
Writes data/derived/<state>/fleet.json and data/derived/<state>/pak_request.json.
"""
import argparse, collections, datetime, glob, os, re
from common import DER, ASSETS, state, load, save, mark_spares

p = argparse.ArgumentParser(); p.add_argument('--state', required=True); a = p.parse_args()
S = state(a.state); D = S['vehicle_date']
V = load(os.path.join(DER, f"vehicles_{S['register']['raw']}.json"))
REC = load(os.path.join(DER, f'records_{D}.json'))
DAY = set(load(os.path.join(DER, f'day_{D}.json'))['cars'])
HIST = load(os.path.join(DER, 'history.json'))
TT = load(os.path.join(DER, S['name'], 'timetable.json'))
PM = load(os.path.join(ASSETS, 'pak_map.json'))
need = {s['id']: s['need']['vehicles'] for s in TT['schedule']}
SL = S['simutrans_lines']

# ---- pak objects: installed names from the checkout (snapshot kept in assets) ---------------------------------------
snap = os.path.join(ASSETS, 'pak_objects.json')
if os.path.isdir(PM['pak_dir']):
    names = sorted({m for f in glob.glob(os.path.join(PM['pak_dir'], '*.dat'))
                    for m in re.findall(r'^name=(\S+)', open(f, encoding='utf-8', errors='ignore').read(), flags=re.M)})
    save(dict(source=PM['pak_dir'], read=datetime.date.today().isoformat(), objects=names), snap)
INSTALLED = set(load(snap)['objects'])

def livery(v):
    p_ = v.get('paint', '')
    if p_ in PM['paint_livery']: return PM['paint_livery'][p_], ''
    if p_.startswith('CVR'): return PM['normal_livery'], 'advert wrap (' + p_[4:].split(',')[0] + ') → normal livery'
    return PM['normal_livery'], f'paint "{p_}" not in the map → normal livery'
def pak(car):
    v = V[car]; t = PM['types'].get(v['full'])
    if not t: return None
    liv, why = livery(v)
    objs = [f"VZ-DPOlomouc-{t['family']}-{liv}-{c}" for c in t['cores']]
    return dict(objs=objs, family=t['family'], livery=liv, core=t['cores'][0].replace('-A', ''), m=t['m'], len=t['len'],
                requested=not all(o in INSTALLED for o in objs), mapped=why, note=t['note'])
def unit(car, **kw):
    v = V[car]
    return dict(car=car, type=v['full'], depot=v['depot'], paint=v['paint'], year=v['year'], state=v['state'], pak=pak(car), **kw)

# ---- 1. logged buses ------------------------------------------------------------------------------------------------
lines = {sl['id']: [] for sl in SL}
main_of = {}
for sl in SL: main_of.setdefault(sl['records'], sl['id'])
used = set()
for rl, rs in REC.items():
    if rl not in main_of:
        if rs: print('WARNING: records on a line not modelled', rl, [r['car'] for r in rs])
        continue
    for i, r in enumerate(rs):
        for c in r['car'].split('+'):
            assert c in V, ('car not in the register', c)
            assert c not in used, ('car twice', c)
            used.add(c)
            lines[main_of[rl]].append(unit(c, rec=rl, kurz=i + 1, src='logged', note=r['note'],
                                           logged_course=r['course'], author=r['author']))

# ---- history (weekday records per line) and roster types ----------------------------------------------------------
def weekday(d): return datetime.date.fromisoformat(d).weekday() < 5
def dd(d):
    x = datetime.date.fromisoformat(d); return f"{x.day} {x.strftime('%b')} {x.year}"
aff = collections.defaultdict(lambda: collections.defaultdict(list))     # line -> car -> [dates]
for L, rs in HIST.items():
    for r in rs:
        if r['date'] and weekday(r['date']) and r['date'] < D:
            for c in r['car'].split('+'): aff[L][c].append(r['date'])
def roster(L):
    rec = {c: [d for d in ds if d >= '2026-01-01'] for c, ds in aff[L].items() if c in V}
    if sum(len(x) for x in rec.values()) < 5:
        rec = {c: ds for c, ds in aff[L].items() if c in V}
    cnt = collections.Counter()
    for c, ds in rec.items(): cnt[V[c]['full']] += len(ds)
    return collections.Counter({t: n for t, n in cnt.items() if n >= 2})
# ---- 2. logged surplus ------------------------------------------------------------------------------------------------
# ties between types are broken by the line's roster (weekday history), so the type the line runs most is kept first
for sl in SL:
    R0 = roster(sl['records']); us = lines[sl['id']]
    us.sort(key=lambda u: -R0.get(u['type'], 0))                     # stable: record order within a type
spares = {sid: mark_spares(us, need[sid]) for sid, us in lines.items()}
for sid, us in lines.items(): us.sort(key=lambda u: u['kurz'])
for sid, us in lines.items():
    for u in us:
        if u.get('spare'): u['spare_why'] = f"{len(us)} logged on the line against {need[sid]} needed; kept one of every type first"

# ---- 3. designed buses --------------------------------------------------------------------------------------------------
def free(c): return c in V and V[c]['active'] and c not in used and c not in DAY
def size(t): return PM['types'].get(t, {}).get('m', 12)
designed, picked_from_hist = [], collections.defaultdict(set)
order = sorted(SL, key=lambda sl: -need[sl['id']])
for sl in order:
    sid, L = sl['id'], sl['records']
    have = [u for u in lines[sid] if not u.get('spare')]
    slots = need[sid] - len(have)
    if slots <= 0: continue
    R = roster(L)
    for u in have: R[u['type']] += 1
    main_t = R.most_common(1)[0][0] if R else None
    for _ in range(slots):
        types_now = {u['type'] for u in lines[sid] if not u.get('spare')}
        A = [c for c, ds in aff[L].items() if free(c) and max(ds) >= '2026-01-01']
        B = [c for c, ds in aff[L].items() if free(c) and c not in A]
        C = [c for c in V if free(c) and V[c]['full'] in R]
        Dd = [c for c in V if free(c) and main_t and size(V[c]['full']) == size(main_t)]
        lack = [t for t, _ in R.most_common() if t not in types_now]
        pick, tier = None, None
        for want in lack + [None]:
            for nm, pool in (('A', A), ('B', B), ('C', C), ('D', Dd)):
                cand = [c for c in pool if want is None or V[c]['full'] == want]
                if nm in 'CD' and want is None:        # fleet fallback: the line's main type first
                    cand.sort(key=lambda c: (V[c]['full'] != main_t, c))
                elif nm in 'AB':
                    cand.sort(key=lambda c: (max(aff[L][c]), len(aff[L][c])), reverse=True)
                else:
                    cand.sort()
                if cand: pick, tier = cand[0], nm; break
            if pick:
                if want: tier += '+type'
                break
        if not pick:
            print('WARNING: no free bus for', sid); break
        used.add(pick)
        ds = sorted(set(aff[L].get(pick, [])), reverse=True)
        if tier[0] in 'AB':
            why = f"{len(aff[L][pick])} weekday record{'s' if len(aff[L][pick]) != 1 else ''} on line {L}, last {', '.join(dd(x) for x in ds[:3])}"
            picked_from_hist[sid].add(pick)
        elif tier[0] == 'C':
            why = f"no free bus with a record on line {L}; a free bus of the line's roster type"
        else:
            why = f"no free bus of the line's types; a free bus of the same size"
        if tier.endswith('+type'): why = f"covers the {V[pick]['full']} type of the line roster; " + why
        why += f"; not logged anywhere on {dd(D)}"
        u = unit(pick, rec=L, kurz=0, src='designed', designed=True, note='Designed, not recorded: ' + why, last=ds[:3], tier=tier[0])
        lines[sid].append(u); designed.append(dict(line=sid, car=pick, why=why, tier=tier[0]))

# leftover free history cars -> "not needed", once, on the Simutrans line (with designed picks) where the car last ran
hist_sids = [sl for sl in SL if picked_from_hist.get(sl['id']) or any(u.get('designed') for u in lines[sl['id']])]
left = {}
for sl in hist_sids:
    for c, ds in aff[sl['records']].items():
        if free(c):
            k = (max(ds), len(ds))
            if c not in left or k > left[c][0]: left[c] = (k, sl['id'], sl['records'])
for c, ((last, n), sid, L) in sorted(left.items(), key=lambda kv: int(kv[0])):
    ds = sorted(set(aff[L][c]), reverse=True)
    lines[sid].append(unit(c, rec=L, kurz=0, src='history', spare='not needed', last=ds[:3],
                           note=f"Free, not needed: {len(aff[L][c])} weekday record{'s' if len(aff[L][c]) != 1 else ''} on line {L}, last {', '.join(dd(x) for x in ds[:3])}"))

# ---- 4. pak request ---------------------------------------------------------------------------------------------------------
req = collections.defaultdict(list)
for sid, us in lines.items():
    for u in us:
        if u.get('spare') or not u['pak']: continue
        if u['pak']['requested']: req[tuple(u['pak']['objs'])].append(u)
save(dict(requests=[dict(objs=list(k), type=us[0]['type'], livery=us[0]['pak']['livery'], m=us[0]['pak']['m'],
                         cars=sorted({u['car'] for u in us}, key=int), paint=sorted({u['paint'] for u in us})) for k, us in req.items()]),
     os.path.join(DER, S['name'], 'pak_request.json'))
short = {sid: need[sid] - sum(1 for u in us if not u.get('spare')) for sid, us in lines.items() if sum(1 for u in us if not u.get('spare')) < need[sid]}
save(dict(lines=lines, designed=designed, short=short, logged=sorted(used & DAY, key=int)),
     os.path.join(DER, S['name'], 'fleet.json'))
cnt = lambda f: sum(1 for us in lines.values() for u in us if f(u))
print('fleet', S['name'], 'need', sum(need.values()), 'logged counted', cnt(lambda u: u['src'] == 'logged' and not u.get('spare')),
      'logged not needed', cnt(lambda u: u['src'] == 'logged' and u.get('spare')), 'designed', len(designed),
      'history not needed', cnt(lambda u: u['src'] == 'history'), 'short', short)
for sid, us in lines.items():
    print(f"  {sid:>4} need {need[sid]}: " + ', '.join(f"{u['car']}{'*' if u.get('designed') else ''}{'(nn)' if u.get('spare') else ''} {u['type'].replace('Solaris ', '')}" for u in us))
print('  requested objects:', [(r[0], len(v)) for r, v in req.items()])

# ---- pak_request.md (for the VZ pak session, sent by the user) ---------------------------------------------------------------
from common import BASE
grp = collections.defaultdict(list)
for us in lines.values():
    for u in us:
        if u['pak']: grp[(u['type'], u['pak']['livery'])].append(u)
md = ['# Olomouc buses (DPMO): pak objects for the peak sheet', '',
      f"State {S['name']}, vehicles of {D}. Operator of every bus: DPMO (Dopravní podnik města Olomouce); no subcontractor runs a city line.",
      'Package VZ-DPOlomouc-bus. Status is read from the local pak checkout (assets/pak_objects.json). Advert wraps (CVR) use the type\'s normal livery.', '',
      '| Type | Livery | Length | Objects | Status | Buses counted in the peak | Not needed (shown dimmed) |', '|---|---|---|---|---|---|---|']
for (t, liv), us in sorted(grp.items()):
    x = us[0]['pak']
    cnt_ = sorted({u['car'] for u in us if not u.get('spare')}, key=int); nn = sorted({u['car'] for u in us if u.get('spare')}, key=int)
    md.append(f"| {t} | {PM['livery_words'].get(liv, liv)} | {x['m']:g} m ({x['len']} car units) | {' + '.join('`' + o + '`' for o in x['objs'])} | "
              f"{'**requested**' if x['requested'] else 'installed'} | {', '.join(cnt_) or '-'} | {', '.join(nn) or '-'} |")
reqs = [k for k, us in grp.items() if us[0]['pak']['requested'] and any(not u.get('spare') for u in us)]
md += ['', '## Requests', '']
md += [f"- {t}, {PM['livery_words'].get(l, l)}: `{grp[(t, l)][0]['pak']['objs'][0]}`" for t, l in reqs] or \
      ['- None: every bus counted in the peak has an installed object.']
opt = [k for k, us in grp.items() if us[0]['pak']['requested'] and all(u.get('spare') for u in us)]
if opt:
    md += ['', 'Optional (only on buses marked not needed now; needed if they are counted after a data refresh):']
    md += [f"- {t}, {PM['livery_words'].get(l, l)} ({', '.join(sorted({u['car'] for u in grp[(t, l)]}, key=int))}; paint {', '.join(sorted({u['paint'] for u in grp[(t, l)]}))}): `{grp[(t, l)][0]['pak']['objs'][0]}`" for t, l in opt]
open(os.path.join(BASE, 'pak_request.md'), 'w', encoding='utf-8').write('\n'.join(md) + '\n')
