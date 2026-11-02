"""The buses of every Simutrans line of every oblast sheet, from the PID live map: python 04_vehicles.py
-> oblasti/<id>/data/derived/roster.json for every oblast with a schedule.json, and data/derived/vehicles.json.

The ODIS roster rules (odis-regional-hko/scripts/04_roster.py), applied to all twelve sheets at once, so a bus is on one
sheet only:
1. Evidence: the live map (01_live_poll.py) gives each bus's trips on the vehicle day (GTFS trip ids). A Simutrans line's
   trips are the real trips its legs stand for (05_schedule: own trips). It is observed on all of them departing in its
   window (anchor -30 .. +90) widened by 30 min, and on its pattern trips (within 3 min of a slot) 12:30-19:30, so a shift
   line every 480 is observed too. Closer sightings rank first; an off-pattern trip counts 10 min further.
2. One bus, one Simutrans line, by augmenting-path matching over all sheets, each bus's closest sighting first.
3. Buses of the Prague bus sheet (its courses) are not used: a bus stays on one sheet.
4. One of every type seen on a line before a second of a type (spares rule); the surplus is "not needed".
5. Short lines get designed buses, each with its reason: (a) a bus seen on the same line's trips at another time of the
   vehicle day, free in the line's window; (b) one seen on the line on the second poll day (Tue 3 Nov: the owner, 1 Nov
   2026: "Use more than a sample day - working day assumption holds from September to November"); (c) a free bus of the
   line's operator that ran this oblast's lines that day, of the line's commonest type; (d) any free bus of the operator.
Each bus: PID number, operator, type (the live map's vehicle window), length from the type, paint from the
seznam-autobusu register (praha-bus registers of 29 Sep, joined by the car id of the vehicle card) where it has the car,
and its pak object (pak_rules in pid-regional/config.json; town lines use their VZ-MHD<Town> package).
"""
import collections, glob, json, os, re
from common import HOME, DER, PIPE

SH = json.load(open(os.path.join(HOME, 'config.json'), encoding='utf-8'))
LIVE = os.path.join(HOME, SH['live']['dir']); DAYS = SH['live']['days']
hm = lambda t: '%d:%02d' % (t // 60 % 24, t % 60)

# ---------------------------------------------------------------- live map
def read_day(day):
    seen = collections.defaultdict(list); busy = collections.defaultdict(list); info = {}
    pd = os.path.join(LIVE, day)
    if not os.path.exists(os.path.join(pd, 'polls.jsonl')): return seen, busy, info
    span = {}
    for ln in open(os.path.join(pd, 'polls.jsonl'), encoding='utf-8'):
        r = json.loads(ln); t = int(r['t'][11:13]) * 60 + int(r['t'][14:16])
        for v, route, tid, stp, *_ in r['buses']:
            if stp not in ('on_track', 'at_stop'): continue          # before / after the trip: the bus is not on it yet
            k = (v, tid)
            if k not in span: span[k] = [t, t, route]
            else: span[k][1] = t
    for (v, tid), (f, l, route) in span.items():
        seen[tid].append((v, f, l)); busy[v].append((f, l, route, tid))
    if os.path.exists(os.path.join(pd, 'vehicles.jsonl')):
        for ln in open(os.path.join(pd, 'vehicles.jsonl'), encoding='utf-8'):
            w = json.loads(ln)
            # a later retry with a type wins over an earlier row without one (vehicle windows that failed at first)
            if w['vehicle'] not in info or (w.get('type') and not info[w['vehicle']].get('type')): info[w['vehicle']] = w
    return seen, busy, info
SEEN, BUSY, INFO = read_day(DAYS[0])
SEEN2, BUSY2, INFO2 = read_day(DAYS[1]) if len(DAYS) > 1 else ({}, {}, {})
for v, w in INFO2.items():
    if v not in INFO or (w.get('type') and not INFO[v].get('type')): INFO[v] = w

REG = json.load(open(os.path.join(PIPE, 'praha-bus', 'data', 'derived', 'vehicles_2026-09-29.json'), encoding='utf-8'))
# the Prague bus sheet's buses
pb = json.load(open(os.path.join(PIPE, 'praha-bus', 'data', 'derived', '2026-09-29', 'courses.json'), encoding='utf-8'))
PRAGUE_IDS = {c_['id'] for c in pb['courses'] if not c.get('spare') for ch in c['chain'] for c_ in ch['cars'] if c_.get('id')}
# buses the Prague bus sheet took from the PID live map since (fleet numbers, config.praha_bus.live_buses; e.g. 318 on v19)
PRAGUE_NUMS = {int(n) for n in SH['praha_bus'].get('live_buses', {}).get('nums', [])}
def prague_bus(v): return v in PRAGUE_NUMS or INFO.get(v, {}).get('car_id') in PRAGUE_IDS

def tlen(ty):
    m = (re.search(r'(\d+)[,._](\d)\s*M\b', ty or '', re.I) or re.search(r'\b(\d{2})\s*M\b', ty or '', re.I)
         or re.search(r'\b(?:NB|NBG|CN|BN|C|ICN|CNG|NS|NC|ICNG|EBN)\s+(\d{1,2})(?:[,.](\d))?\b', ty or '')
         or re.search(r'\bLE\s+(\d{2})\b', ty or '') or re.search(r'Urbino\s+(\d{2})', ty or ''))
    if re.search(r'Dekstra|Stratos|Midi|Sprinter|Master|Rosero|Neocity', ty or '', re.I): return 'midibus'
    if not m: return '12 m'
    return f"{m.group(1)}.{m.group(2)} m" if m.lastindex and m.lastindex >= 2 and m.group(2) else f"{m.group(1)} m"

# ---------------------------------------------------------------- pak objects
PAKDIR = os.path.join(SH['pak']['repo'], 'build')
INST = {}
for pk in SH['pak']['packages']:
    for f in glob.glob(os.path.join(PAKDIR, pk, '*.dat')):
        t = open(f, encoding='utf-8', errors='replace').read()
        for m in re.finditer(r'(?im)^name=(\S+)\s*$', t):
            ln = re.search(r'(?im)^length=(\d+)', t[m.end():]); INST[m.group(1)] = int(ln.group(1)) if ln else 8
def livery(paint):
    p = (paint or '').lower()
    for k, v in SH['pak']['paints']:
        if k in p: return v
    return SH['pak']['default_livery']
def objs(pre):
    """installed objects of one type and livery: 'VZ-PID-<tok>-<liv>-<tok>', articulated '...-<tok>-A' + '-B'"""
    return sorted(n for n in INST if n.startswith(pre))
def pak_of(ty, paint, town, op='', num=None):
    """The pak object of a bus (fleet desk, 2 Nov 2026: regional PID lines use VZ-Praha-bus and VZ-DPPraha-bus objects as they
    are; VZ-PID-bus holds only the type x livery combinations those lack): 1. config pak.objects, the exact objects the fleet
    desk named (type and operator substrings); 2. a town line: VZ-MHD<Town>-<token>-<its livery>; 3. VZ-PID / VZ-Praha /
    VZ-DPPraha-<token>-<livery> (DPP's own buses look in VZ-DPPraha first). A type with none stays "requested" (no
    stand-ins); a fleet desk candidate that holds only for a plain white bus (pak.if_white) is named, still requested."""
    def found(ns, core, liv):
        return dict(ok=True, core=core + (' A + B' if any(n.endswith('-B') for n in ns) else ''), liv=liv, obj=ns[0], length=sum(INST[n] for n in ns))
    # 0. the object the fleet desk set for this very bus (config pak.by_vehicle, by fleet number; 'OUT: why' = out of scope)
    bv = SH['pak'].get('by_vehicle', {}).get(str(num)) if num is not None else None
    if bv and bv.startswith('OUT:'): return dict(ok=False, core='out of scope', liv='', obj=None, want=bv[4:].strip(), out=True)
    if bv:
        ns = objs(bv + '-')
        if ns:
            parts = bv.split('-'); return found(ns, parts[-2], parts[-1])
    for sub, osub, base in SH['pak'].get('objects', []):
        if sub.lower() in (ty or '').lower() and osub.lower() in (op or '').lower():
            ns = objs(base + '-')
            if ns:
                parts = base.split('-'); return found(ns, parts[-2], parts[-1])
    tok = next((t for sub, t in SH['pak']['rules'] if sub.lower() in (ty or '').lower()), None)
    if not tok: return dict(ok=False, core='?', liv='', obj=None, want=f'{ty} ({paint or "paint unknown"})')
    # a town pack holds only the town's own paint (fleet desk, 2 Nov 2026); a town-line bus in PID paint uses the PID object
    if town and 'pid' not in (paint or '').lower():
        pk = SH['pak']['towns'].get(town, town); ns = [n for n in INST if n.startswith(f"VZ-MHD{pk}-{tok}-")]
        if ns:
            liv = ns[0][len(f"VZ-MHD{pk}-{tok}-"):].split('-')[0]
            return found(objs(f"VZ-MHD{pk}-{tok}-{liv}-"), tok, liv)
        # not in PID paint: the town's own paint, never the PID grey object of the same type (fleet desk, 2 Nov 2026: the
        # white-and-green MHD Říčany NovoCitis had silently become VZ-Praha-NovoCiti_Life-pidsedocervena)
        return dict(ok=False, core=tok, liv='', obj=None, want=f"VZ-MHD{pk}-{tok}-<town livery> ({ty}, town line of {town}; {paint or 'paint not in the register'})")
    liv = livery(paint)
    packs = ['VZ-DPPraha', 'VZ-PID', 'VZ-Praha'] if 'Dopravní podnik' in (op or '') else ['VZ-PID', 'VZ-Praha', 'VZ-DPPraha']
    for pre in packs:
        ns = objs(f"{pre}-{tok}-{liv}-")
        if ns: return found(ns, tok, liv)
    if not paint:
        for pre in packs:
            alt = [n for n in INST if n.startswith(f"{pre}-{tok}-")]
            if alt:
                liv2 = alt[0][len(f"{pre}-{tok}-"):].split('-')[0]; return found(objs(f"{pre}-{tok}-{liv2}-"), tok, liv2)
    cand = next((b for sub, b in SH['pak'].get('if_white', []) if sub.lower() in (ty or '').lower()), None)
    want = (f"VZ-MHD{SH['pak']['towns'].get(town, town)}-{tok}-<town livery>" if town else f"VZ-PID-{tok}-{liv}")
    if cand: want += f" (fleet desk: {cand} if the bus is plain white; photo to confirm)"
    return dict(ok=False, core=tok, liv=liv, obj=None, want=want)
def opn(o):
    """one spelling per operator: the live map writes some with the legal form ('ČSAD Benešov s.r.o.'), most without"""
    return re.sub(r',?\s*(spol\. s r\.\s*o\.|s\.\s*r\.\s*o\.|a\.\s*s\.)\s*$', '', (o or '').strip()).strip(' ,')
def info(v, town=None):
    w = INFO.get(v, {}); r = REG.get(w.get('car_id') or '', {})
    ty = w.get('type') or r.get('maker_type') or ''
    op = opn(w.get('operator') or r.get('operator', ''))
    note = ''
    if not ty and op in SH['pak'].get('untyped', {}) and town:
        # MHD Kolín: the live map gives no type; the fleet desk's fleet list (17 Conecto LF II, 2 NovoCiti Life, all white)
        ty = SH['pak']['untyped'][op]; note = 'type not reported by the live map; the town fleet is 17 Conecto LF II and 2 NovoCiti Life (fleet desk)'
    ty = ty or '?'
    return dict(num=str(v), operator=op, type=ty, full=ty + (' (probable)' if note else ''), len=tlen(ty),
                paint=r.get('paint', ''), garage=r.get('garage', ''), course=w.get('course', ''), car_id=w.get('car_id'),
                pak=pak_of(ty, r.get('paint', ''), town, op, v), note=note)

# ---------------------------------------------------------------- the Simutrans lines of every sheet
sims = []; TOWN = {}; OPS = {}
for o in SH['oblasti']:
    d = os.path.join(HOME, 'oblasti', o['id'], 'data', 'derived')
    if not os.path.exists(os.path.join(d, 'schedule.json')): continue
    S = json.load(open(os.path.join(d, 'schedule.json'), encoding='utf-8'))
    T = json.load(open(os.path.join(d, 'trips.json'), encoding='utf-8'))
    C = json.load(open(os.path.join(d, 'line_class.json'), encoding='utf-8'))
    tid = {(t['lic'], t['sp']): t['tid'] for tr in T.values() for t in tr}
    for L, x in S.items():
        if L.startswith('_'): continue
        TOWN[(o['id'], L)] = C[L].get('town'); OPS[(o['id'], L)] = C[L].get('operators', [])
        for i, s in enumerate(x['sim']):
            for g in s['legs']:
                for t in g.get('trips', []): t['tid'] = tid.get((t['lic'], t['sp']))
            sims.append((o['id'], L, i, s, x))

def evidence(s, seen):
    W = s['window']; ev = {}
    for g in s['legs']:
        if g['untimed']: continue
        for t in g.get('trips', []):
            if not (W[0] - 30 <= t['d'] < W[1] + 30 or (t['dev'] <= 3 and 750 <= t['d'] < 1170)): continue
            for v, f, l in seen.get(t['tid'], []):
                if prague_bus(v): continue
                dd = (0 if W[0] <= t['d'] < W[1] else min(abs(t['d'] - W[0]), abs(t['d'] - W[1]))) + (0 if t['dev'] <= 3 else 10)
                lab = f"{t['line']} {hm(t['dep0'])} from {t['fr0'].split(', ', 1)[-1] if t['fr0'].count(', ') else t['fr0']}"
                if v not in ev or dd < ev[v][0]: ev[v] = (dd, lab)
    return ev
K = [(oid, L, i) for oid, L, i, s, x in sims]; SM = {(oid, L, i): s for oid, L, i, s, x in sims}
EV = {k: evidence(SM[k], SEEN) for k in K}
NEED = {k: SM[k]['need'] for k in K}
cand = collections.defaultdict(list)
for k, ev in EV.items():
    for v, (dd, lab) in ev.items(): cand[v].append((dd, k))
for v in cand: cand[v].sort()
owner = {}
def try_assign(v, vis):
    for dd, k in cand[v]:
        for j in range(NEED[k]):
            sl = (k, j)
            if sl in vis: continue
            vis.add(sl)
            if sl not in owner or try_assign(owner[sl], vis): owner[sl] = v; return True
    return False
import sys; sys.setrecursionlimit(20000)
for v in sorted(cand, key=lambda v: (len(cand[v]), cand[v][0][0], v)):
    if v not in owner.values(): try_assign(v, set())
assigned = collections.defaultdict(list)
for (k, j), v in owner.items(): assigned[k].append(v)
used = {v: k for k, vs in assigned.items() for v in vs}
# one of every type before a second
for k, ev in EV.items():
    for v in [v for v in ev if v not in used]:
        ty = info(v)['type']; mine = assigned[k]
        if ty in {info(p)['type'] for p in mine}: continue
        cnt = collections.Counter(info(p)['type'] for p in mine)
        dup = [p for p in mine if cnt[info(p)['type']] > 1]
        if dup:
            out_ = max(dup, key=lambda p: ev[p][0]); mine[mine.index(out_)] = v; used[v] = k; used.pop(out_, None)

def free_in(v, W, busy):
    return v not in used and not prague_bus(v) and not any(f < W[1] and l > W[0] for f, l, *_ in busy.get(v, []))
def op_short(o): return re.sub(r'\b(a\.s\.|s\.r\.o\.|spol\. s r\.o\.|, )', '', o).strip(' ,').upper()
designed = collections.defaultdict(list)
OBL_BUSES = collections.defaultdict(set)    # buses that ran an oblast's lines on the day
for oid, L, i, s, x in sims:
    for g in s['legs']:
        for t in g.get('trips', []):
            for v, f, l in SEEN.get(t['tid'], []): OBL_BUSES[oid].add(v)
for oid, L, i, s, x in sims:
    k = (oid, L, i); short = s['need'] - len(assigned[k])
    if short <= 0: continue
    W = s['window']; town = TOWN[(oid, L)]
    tys = collections.Counter(info(v)['type'] for v in EV[k]) or collections.Counter(
        info(v)['type'] for g in s['legs'] for t in g.get('trips', []) for v, *_ in SEEN.get(t['tid'], []))
    def add(v, why):
        designed[k].append(dict(info(v, town), why=why)); used[v] = k
    # (a) the same line at another time of the day
    pool = sorted({(abs(f - W[0]), v, f, t['line']) for g in s['legs'] for t in g.get('trips', []) for v, f, l in SEEN.get(t['tid'], []) if free_in(v, W, BUSY)})
    for _, v, f, ln in pool:
        if short <= 0: break
        if v in used: continue
        add(v, f"seen on {ln} at {hm(f)}, free in this line's window {hm(W[0])}–{hm(W[1])}"); short -= 1
    # (b) the same line on the second poll day
    pool = sorted({(abs(f - W[0]), v, f, t['line']) for g in s['legs'] for t in g.get('trips', []) for v, f, l in SEEN2.get(t['tid'], []) if free_in(v, W, BUSY)})
    for _, v, f, ln in pool:
        if short <= 0: break
        if v in used: continue
        add(v, f"seen on {ln} at {hm(f)} on {DAYS[1]}, free on {DAYS[0]} in this line's window"); short -= 1
    # (c) / (d) a free bus of the line's operator: first one that ran this oblast's lines that day
    ops = {op_short(o) for o in OPS[(oid, L)]}
    for scope, vs in (('ran this oblast\'s lines that day', OBL_BUSES[oid]), ('ran PID lines that day', set(INFO))):
        if short <= 0: break
        c_ = sorted((v for v in vs if free_in(v, W, BUSY) and any(op_short(info(v)['operator'])[:8] in o or o[:8] in op_short(info(v)['operator']) for o in ops)),
                    key=lambda v: (-tys.get(info(v)['type'], 0), v))
        for v in c_:
            if short <= 0: break
            add(v, f"designed: a free {info(v)['operator']} bus that {scope}, not on any line {hm(W[0])}–{hm(W[1])}"); short -= 1
    if short > 0: print('STILL SHORT', oid, L, s['name'], short)

tot = collections.Counter()
for o in SH['oblasti']:
    d = os.path.join(HOME, 'oblasti', o['id'], 'data', 'derived')
    if not os.path.exists(os.path.join(d, 'schedule.json')): continue
    out = {}
    for oid, L, i, s, x in sims:
        if oid != o['id']: continue
        k = (oid, L, i); ev = EV[k]; town = TOWN[(oid, L)]
        out.setdefault(L, []).append(dict(
            name=s['name'], need=s['need'],
            seen=[dict(info(v, town), seen=ev[v][1], dist=ev[v][0]) for v in assigned[k]],
            designed=designed[k],
            not_needed=[dict(info(v, town), seen=ev[v][1], elsewhere=(f"{used[v][0]} {used[v][1]}" if v in used else '')) for v in ev if used.get(v) != k]))
    n = sum(r['need'] for rs in out.values() for r in rs); ns = sum(len(r['seen']) for rs in out.values() for r in rs); nd = sum(len(r['designed']) for rs in out.values() for r in rs)
    json.dump(dict(lines=out, totals=dict(need=n, seen=ns, designed=nd)), open(os.path.join(d, 'roster.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    tot.update(need=n, seen=ns, designed=nd)
    print(f"{o['name']:18} need {n:4}: seen {ns:4}, designed {nd:3}")
# the fleet desk's list (pak rules: one inventory per sheet family; the fleet desk answers which objects exist and draws the
# missing ones): every type x livery a sheet bus needs that has no installed object, with operators, numbers and sheets
req = collections.defaultdict(lambda: dict(n=0, ops=collections.Counter(), nums=[], sheets=set(), paint=collections.Counter()))
for v, k in used.items():
    r = info(v, TOWN.get((k[0], k[1])))
    if r['pak']['ok'] or r['pak'].get('out'): continue
    e = req[(r['type'], r['pak'].get('want'))]; e['n'] += 1; e['ops'][r['operator']] += 1; e['nums'].append(r['num'])
    e['sheets'].add(k[0]); e['paint'][r['paint'] or 'paint not in the register'] += 1
lines_ = ['# Pak requests from the PID regional sheets', '',
          f'From pipeline/pid-regional/scripts/04_vehicles.py ({DAYS[0]} live map). Buses on the twelve oblast sheets whose type and '
          'livery have no object in VZ-PID-bus (regional) or VZ-MHD<Town>-bus (town lines). They are shown as "requested" on the '
          'sheets, never as a stand-in (rules/pak-objects.md). "?" = the vehicle window of the live map names no type for the bus '
          '(and the bus is not in the register); the second poll day may name it.', '',
          '| Real type | Wanted object | Buses | Operators | Paint (register) | Example numbers | Sheets |', '|---|---|---|---|---|---|---|']
for (ty, want), e in sorted(req.items(), key=lambda x: -x[1]['n']):
    lines_.append(f"| {ty} | {want} | {e['n']} | {', '.join(f'{o} {n}' for o, n in e['ops'].most_common())} | "
                  f"{', '.join(f'{p} {n}' for p, n in e['paint'].most_common(3))} | {', '.join(sorted(e['nums'])[:8])} | {', '.join(sorted(e['sheets']))} |")
open(os.path.join(HOME, 'pak_request.md'), 'w', encoding='utf-8').write('\n'.join(lines_) + '\n')
print('total', dict(tot), '| buses with no pak object (by type, town lines included):', sorted(((k[0], e['n']) for k, e in req.items()), key=lambda x: -x[1]))
