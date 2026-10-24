"""Afternoon-peak fleet for one state: which vehicle worked each kurz on the vehicle day, per Simutrans line.

  python 04_fleet.py --state 2026-09-29                          trolleybus sheet
  python 04_fleet.py --state 2026-09-29 --base ../../plzen-bus   bus sheet

Record rules (seznam-autobusu.cz notes, as on the Plzeň tram sheet):
- "ráno": morning-only car, not counted ("Not counted" list);
- "odpoledne": the afternoon car of a kurz; "ráno i odpoledne": a split duty out in both peaks; no note: all day;
- a car logged on two lines with no note is counted once, on the line the state prefers ("fleet.secondary": the
  line whose record is dropped, e.g. 18, a Škoda-shift line whose cars also work another line);
- a record line may feed several Simutrans lines: explicit "kurzy" first, then later lines take their need from the
  highest kurz numbers (peak-only kurzy are the high ones), the line named like the record line keeps the rest.
Shortfall (user rule, 29 Sep): designed vehicles with REAL car numbers from the line's own history
(data/derived/history.json), active in the register, not out anywhere on the vehicle day (day overview), of the
right traction; on a battery line only battery-capable cars. The picks first cover every type of the line's
roster (history + logged) that the counted cars lack, then go newest first. Leftover free history cars are listed
as "not needed". Surplus logged (user rule, 29 Sep): mark_spares from pipeline/brno-trolleybus keeps exactly the
need - one of every type first, then drops afternoon-only kurzy, then the highest kurz numbers.
Writes <base>/data/derived/<state>/fleet.json.
"""
import argparse, collections, datetime, os
from common import BASE, DER as TDER, RAW, state, load, save, mark_spares, busy_ids

p = argparse.ArgumentParser(); p.add_argument('--state', required=True); p.add_argument('--base', default=BASE); a = p.parse_args()
base = os.path.abspath(a.base); S = state(a.state, base); FL = S['fleet']; DER = os.path.join(base, 'data', 'derived')
vd = S['vehicles_date']
vyp = load(os.path.join(TDER, f'vypravenost_{vd}.json'))
veh = load(os.path.join(TDER, f"vehicles_{S['register_date']}.json"))
TT = load(os.path.join(DER, S['name'], 'timetable.json'))
need = {s['id']: (s['need'] or {}).get('vehicles') or s['min_run'] for s in TT['schedule']}
hist_all = load(os.path.join(TDER, 'history.json')) if os.path.exists(os.path.join(TDER, 'history.json')) else {}
busy = busy_ids(os.path.join(RAW, 'vypravenost-days', f'{vd}.html'))
TRACTION = S['traction']                       # 'trolleybus' or 'bus'
OFFWIRE = load(os.path.join(DER, S['name'], 'offwire.json'))['lines'] if os.path.exists(os.path.join(DER, S['name'], 'offwire.json')) else {}

def battery(v):
    """'battery', 'diesel' (auxiliary diesel unit) or '' by the state's rules (type and number range)."""
    n = int(v['num']) if (v.get('num') or '').isdigit() else -1
    for kind in ('battery', 'diesel'):
        for r in S.get(kind + '_rules', []):
            if v['type'] == r['type'] and r.get('from', -1) <= n <= r.get('to', 10 ** 9): return kind
    return ''

def vinfo(cid):
    v = veh.get(cid, {})
    return dict(id=cid, car=v.get('num') or '?', type=v.get('type') or 'not in the register', garage=v.get('garage', ''),
                livery=v.get('livery', ''), operator=v.get('operator') or '?', year=v.get('year', ''),
                traction=v.get('traction', ''), battery=battery(v) if v else '')

lines_of_rec = collections.defaultdict(list)
for sl in S['simutrans_lines']: lines_of_rec[sl['records']].append(sl)
recs = {r for r in lines_of_rec} | set(FL.get('secondary', []))

# ---- kurz -> afternoon vehicle -----------------------------------------------------------------------
by_rec, excluded = {}, []
for rl in sorted(recs, key=lambda x: (len(x), x)):
    byk = collections.defaultdict(list)
    for r in vyp.get(rl, []): byk[r['kurz']].append(r)
    out = []
    for k in sorted(byk, key=lambda x: (isinstance(x, str), x)):
        rs = byk[k]; pm = [r for r in rs if r['note'] != 'ráno']
        for r in rs:
            if r['note'] == 'ráno': excluded.append(dict(line=rl, kurz=k, ids=r['ids'], why='morning only (ráno)'))
        if not pm: continue
        assert len(pm) == 1, (rl, k, pm)
        r = pm[0]; u = dict(kurz=k, rec=rl, src=r['note'], note='', **vinfo(r['ids'][0]))
        if len(r['ids']) > 1: u['note'] = 'Coupled set logged: ' + ' + '.join(r['cars'])
        out.append(u)
    by_rec[rl] = out
# a car on two record lines (no note on either): counted once, off the state's secondary line
where = collections.defaultdict(list)
for rl, o in by_rec.items():
    for u in o: where[u['id']].append(rl)
for cid, rls in where.items():
    if len(rls) < 2: continue
    drop = [rl for rl in rls if rl in FL.get('secondary', [])]
    assert drop and len(rls) - len(drop) == 1, (cid, rls)
    keep = next(rl for rl in rls if rl not in drop)
    for rl in drop:
        u = next(u for u in by_rec[rl] if u['id'] == cid); by_rec[rl].remove(u)
        ku = next(x for x in by_rec[keep] if x['id'] == cid)
        excluded.append(dict(line=rl, kurz=u['kurz'], ids=[cid], why=f"also logged on {keep}/{ku['kurz']}, counted there: {FL['secondary_why']}"))
        ku['note'] = (ku['note'] + ' ' if ku['note'] else '') + f"Also logged on {rl}/{u['kurz']} (not counted twice)."
dup = [c for c, rls in where.items() if sum(1 for rl in rls if any(u['id'] == c for u in by_rec[rl])) > 1]
assert not dup, dup

# notes
morning = collections.defaultdict(list)
for x in excluded:
    if x['why'].startswith('morning'): morning[(x['line'], x['kurz'])] += x['ids']
where = {u['id']: f"{rl}/{u['kurz']}" for rl, o in by_rec.items() for u in o}
for rl, o in by_rec.items():
    for u in o:
        if u['src'] == 'odpoledne':
            am = morning.get((rl, u['kurz']))
            bits = [vinfo(c)['car'] + (f" (afterwards on {where[c]})" if c in where else '') for c in am or []]
            u['note'] = (u['note'] + ' ' if u['note'] else '') + ('Afternoon car. Morning: ' + '; '.join(bits) + '.' if bits else 'Afternoon-only kurz.')
        elif u['src'] == 'ráno i odpoledne':
            u['note'] = (u['note'] + ' ' if u['note'] else '') + 'Split duty, out in both peaks.'
        u['note'] = FL.get('note_overrides', {}).get(f"{rl}/{u['kurz']}", u['note'])

# ---- allocate kurzy to Simutrans lines ----------------------------------------------------------------
lines = {sl['id']: [] for sl in S['simutrans_lines']}; split_of = {}
for rl, sls in lines_of_rec.items():
    pool = list(by_rec.get(rl, []))
    for sl in sls:
        if 'kurzy' in sl:
            lines[sl['id']] = [u for u in pool if u['kurz'] in sl['kurzy']]; pool = [u for u in pool if u['kurz'] not in sl['kurzy']]
    auto = sorted((sl for sl in sls if 'kurzy' not in sl), key=lambda sl: sl['id'] != rl)
    for sl in auto[1:]:
        take = pool[-need[sl['id']]:] if need[sl['id']] and pool else []
        lines[sl['id']] = sorted(take, key=lambda u: u['kurz']); pool = [u for u in pool if u not in take]
    if auto: lines[auto[0]['id']] += pool
    if len(sls) > 1:
        for sl in sls: split_of[sl['id']] = rl

# ---- battery lines -----------------------------------------------------------------------------------
def battery_line(sl):
    """Stretches off the wire on the modelled legs of a Simutrans line (03b_offwire.py), else []."""
    out = []
    for e in sl['entries']:
        for pt in OFFWIRE.get(e[0], []):
            if (pt['o'], pt['d']) == (e[1], e[2]) and pt['stretches']:
                out += [s for s in pt['stretches'] if s not in out]; break
    return out
bat_line = {sl['id']: battery_line(sl) for sl in S['simutrans_lines']}

# ---- shortfalls: designed vehicles from the line's history --------------------------------------------
holidays = set(S.get('holidays', []))
def days3(ds):
    xs = [datetime.date.fromisoformat(d) for d in ds[:3]]
    return ', '.join(f"{x.day} {x:%b}" for x in xs) + (f" {xs[-1].year}" if xs else '')
workday = lambda d: bool(d) and datetime.date.fromisoformat(d).weekday() < 5 and d not in holidays
taken = busy | {u['id'] for o in lines.values() for u in o}
designed_log = {}
for sl in S['simutrans_lines']:
    sid = sl['id']; o = lines[sid]; short = (need.get(sid) or 0) - len(o)
    if short <= 0: continue
    H = [r for r in hist_all.get(sl.get('history', sl['records']), []) if workday(r['date'])]
    roster = {}
    for r in H:
        for cid in r['ids']:
            v = veh.get(cid)
            if not v or v.get('state') != 'zar' or v.get('traction') != TRACTION: continue
            e = roster.setdefault(cid, dict(id=cid, dates=[], n=0)); e['n'] += 1
            if r['date'] not in e['dates']: e['dates'].append(r['date'])
    ok = lambda cid: not bat_line[sid] or battery(veh[cid]) == 'battery'
    free = sorted((e for e in roster.values() if e['id'] not in taken and ok(e['id'])), key=lambda e: (e['dates'][0], e['n']), reverse=True)
    have = {u['type'] for u in o}
    tfreq = collections.Counter()
    for e in roster.values(): tfreq[veh[e['id']]['type']] += e['n']
    for u in o: tfreq[u['type']] += 0
    picks = []
    for ty, _ in tfreq.most_common():
        if len(picks) >= short: break
        if ty in have: continue
        e = next((e for e in free if veh[e['id']]['type'] == ty and e not in picks), None)
        if e: picks.append(e); have.add(ty)
    for e in free:
        if len(picks) >= short: break
        if e not in picks: picks.append(e)
    for i, e in enumerate(picks):
        taken.add(e['id'])
        d3 = days3(e['dates'])
        o.append(dict(kurz=f'+{i + 1}', rec=sl['records'], src='designed', designed=True, hist=e['dates'][:3],
                      note=f"Designed, not recorded: the line needs {need[sid]} and {need[sid] - short} were logged on the vehicle day. "
                           f"This car last ran {sl.get('history', sl['records'])} on {d3}; it was not out anywhere on the vehicle day.", **vinfo(e['id'])))
    rest = [e for e in free if e not in picks]
    for e in rest:
        d3 = days3(e['dates'])
        o.append(dict(kurz='', rec=sl['records'], src='history', spare='not needed', hist=e['dates'][:3],
                      note=f"Free car from the line's history (last on {sl.get('history', sl['records'])}: {d3}), not needed: the designed picks already cover the need and every type.", **vinfo(e['id'])))
    designed_log[sid] = dict(short=short, picked=len(picks), history_days=len({r['date'] for r in H}),
                             history_span=[H[-1]['date'], H[0]['date']] if H else None, spares=len(rest))
    if len(picks) < short: designed_log[sid]['still_short'] = short - len(picks)

# ---- surplus: keep exactly the need (user rule) --------------------------------------------------------
spares = {}
for sid, o in lines.items():
    live = [u for u in o if not u.get('spare')]
    for u in live: u['sub'] = bool(bat_line[sid]) and u.get('battery') != 'battery'   # on a battery line a car without a battery goes first
    n = mark_spares(live, need.get(sid), pm_notes=('odpoledne',), type_of=lambda u: u['type'])
    if n: spares[sid] = n

# ---- battery check: only battery-capable vehicles on lines with an off-wire stretch --------------------
check = {}
for sid, o in lines.items():
    if not bat_line[sid]: continue
    cnt = [u for u in o if not u.get('spare')]
    bad = [u['car'] for u in cnt if u['battery'] != 'battery']
    check[sid] = dict(stretches=bat_line[sid], counted=len(cnt), battery=len(cnt) - len(bad), not_battery=bad)
    for u in cnt:
        if u['battery'] != 'battery': u['note'] = ('NOT battery-capable on a battery line. ' + u['note']).strip()

short = {sid: need[sid] - sum(1 for u in o if not u.get('spare')) for sid, o in lines.items() if need.get(sid) and sum(1 for u in o if not u.get('spare')) < need[sid]}
save(dict(lines=lines, excluded=excluded, split_of=split_of, spares=spares, designed=designed_log, short=short,
          battery_check=check, battery_lines=bat_line, by_record_line={k: len(v) for k, v in by_rec.items()}),
     os.path.join(DER, S['name'], 'fleet.json'))
cnt = lambda o: sum(1 for u in o if not u.get('spare'))
print('fleet', S['name'], sum(cnt(o) for o in lines.values()), 'counted,', sum(spares.values()), 'logged not needed;',
      'designed', {k: v['picked'] for k, v in designed_log.items()}, 'short', short)
print('  per line (counted/need/logged+designed):', {k: f"{cnt(v)}/{need.get(k)}/{len([u for u in v if u['src'] != 'history'])}" for k, v in lines.items()})
print('  battery check:', {k: (v['battery'], v['counted'], v['not_battery']) for k, v in check.items()})
