"""Register, day records and line history -> data/derived/<state>/fleet.json (vehicles per Simutrans line).

  python 04_fleet.py --state 2026-09-29

1. Register (seznam-autobusu.cz, DPMP = iddopravce 47): number, type, year, paint, state, depot, keyed by the site's car id
   (the records link every car to its id, so the numbers never have to be guessed).
2. Day records (state.vehicles_date): one afternoon vehicle per line/kurz. "ráno" rows and a car that works another
   kurz "odpoledne" the same day are morning duties; "nahrazen X" gives way to X ("náhrada za ..."). They go to
   "Not counted" with the reason.
3. Kurzy -> Simutrans lines. A DPMP line's kurzy feed its own Simutrans lines, plus the lines pooled onto it
   (state.records_of: 33 runs on line 3's kurzy, 88 on line 8's). The line's own branches take their need first,
   from the highest kurz numbers, battery-capable cars first where the line needs them (state.battery_required);
   then the main line takes its need from the lowest kurzy, then the pooled lines take theirs from what is left, and
   any rest goes to the main line. The records never name a branch, so this split is a choice.
4. Logged surplus (user, 29 Sep): where a Simutrans line has more vehicles than its need, exactly the need stays
   counted - mark_spares from pipeline/brno-trolleybus: one of every type first (most frequent first), then
   afternoon-only kurzy and the highest kurz numbers are dropped first. The rest is "not needed".
5. Shortfall -> designed vehicles with real car numbers (user, 29 Sep): active cars of the line's own history
   (days before the vehicle day, since history.since; lines with none then take the latest records of any date;
   weekday records first), of the
   line's traction, battery-capable where needed, and not out anywhere on the vehicle day (day records + overview).
   Picks first cover every type of the line's roster (history + logged) that the counted vehicles lack, then go by
   the latest record on the line. If the history runs out: free active cars of the line's own types, then the
   operator's usual types for that traction. The free history cars left over are listed as "not needed".
"""
import argparse, collections, datetime, glob, html, json, os, re
from common import RAW, ASSETS, state, load, save, der, parse_vypravenost, record_date, mark_spares

ap = argparse.ArgumentParser(); ap.add_argument('--state', required=True); S = state(ap.parse_args().state)
NET = load(der(S, 'network.json')); SIM = NET['simutrans']
PM = load(os.path.join(ASSETS, 'pak_map.json')); INST = load(os.path.join(ASSETS, 'pak_installed.json'))['objects']
VD = S['vehicles_date']
def nice(d):
    x = datetime.date.fromisoformat(d); return f"{x.strftime('%a')} {x.day} {x.strftime('%b')} {x.year}"

# ---- 1. register
def clean(t): return html.unescape(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', t))).strip()
veh = {}
for f in sorted(glob.glob(os.path.join(RAW, 'register', S['register_date'], '*_p*.html'))):
    s = open(f, encoding='utf-8').read()
    for block in re.split(r'(?=<tr class="car-line [^"]*first-line")', s)[1:]:
        cid = re.search(r'data-car-id="(\d+)"', block).group(1)
        st = re.search(r'car-line (\S+)', block).group(1)
        ty = clean(re.search(r'<td class="manufacturer-type">(.*?)</td>', block, re.S).group(1))
        yr = re.search(r'<td class="font085">(\d{4})', block)
        paint = re.search(r'<span class="paint"><span class="label">nátěr:</span>(.*?)</span>\s*</td>', block, re.S)
        num = re.search(r'class="bold \d+ number"><!--\s*-->(\d+)', block)
        dep = re.search(r'<td class="no-mobile depots">(.*?)</td>', block, re.S)
        veh[cid] = dict(num=num.group(1) if num else '', type=ty, year=yr.group(1) if yr else '', state=st,
                        paint=clean(paint.group(1)).rstrip(' *') if paint else '', depot=clean(dep.group(1)).rstrip('*') if dep else '')
save(veh, der(S, 'vehicles.json'))
BAT = [tuple(x) for x in PM['battery_cars']['numbers']]
def battery(v): return v['type'].endswith(' Tr') and v['num'].isdigit() and any(a <= int(v['num']) <= b for a, b in BAT)
def mode(v): return 'trolleybus' if v['type'].endswith(' Tr') else 'bus'

def pak(v):
    t = PM['types'].get(v['type'])
    if not t: return dict(obj=None, core=None, status='missing', livery=None)
    liv = t['default']
    for rx, lv, _why in PM['paint_rules']:
        if re.search(rx, v['paint']):
            if lv: liv = lv
            break
    obj = f"VZ-DPPardubice-{t['token']}-{liv}-{t['core']}"
    return dict(obj=obj, core=t['core'], livery=liv, status='installed' if obj in INST else 'requested',
                package=PM['package'][t['mode']], len=t['len'], m=t['m'], full=t['full'])

# ---- 2. records (with the site's car id)
def rows_of(path):
    s = open(path, encoding='utf-8').read(); out = []
    for m in re.finditer(r'<tr class="row ([^"]*)">(.*?)</tr>', s, flags=re.S):
        b = m.group(2); cid = re.search(r'/vuz/(\d+)/vypravenost', b)
        r = parse_vypravenost(m.group(0))[0]
        r['cid'] = cid.group(1) if cid else None
        out.append(r)
    return out
day_rows = [r for f in sorted(glob.glob(os.path.join(RAW, 'vypravenost', VD, 'vypis_p*.html'))) for r in rows_of(f)]
ov = open(os.path.join(RAW, 'vypravenost', VD, 'overview.html'), encoding='utf-8').read()
out_that_day = {r['cid'] for r in day_rows} | set(re.findall(r'/vuz/(\d+)/vypravenost', ov))
FL = S['fleet']
def is_morning(n): return any(n.strip().lower().startswith(x) for x in FL['morning_notes'])
def is_pm(n): return any(n.strip().lower().startswith(x) for x in FL['afternoon_notes'])
bykurz = collections.defaultdict(list)
for r in day_rows: bykurz[(r['line'], r['kurz'])].append(r)
pm_cars = {r['cid'] for r in day_rows if is_pm(r['note']) or r['note'].lower().startswith('náhrada za')}
kurz_car, excluded = {}, []
for (L, k), rs in sorted(bykurz.items(), key=lambda x: (x[0][0], int(x[0][1] or 0))):
    keep = []
    for r in rs:
        v = veh.get(r['cid'], {})
        if is_morning(r['note']): why = f"morning duty ({r['note']})"
        elif r['note'].lower().startswith('nahrazen'): why = f"replaced during the day ({r['note']})"
        elif not is_pm(r['note']) and r['cid'] in pm_cars and len(rs) == 1: why = f"morning duty: the car works another kurz in the afternoon"
        elif L not in {s['line'] for s in SIM} and L not in S.get('records_of', {}).values(): why = f"line {L} is not on the sheet"
        else: keep.append(r); continue
        excluded.append(dict(line=L, kurz=k, cid=r['cid'], num=v.get('num', r['car']), why=why))
    if len(keep) > 1: keep = [r for r in keep if is_pm(r['note'])] or keep[:1]
    if keep: kurz_car[(L, k)] = keep[0]

# ---- 3. kurzy -> Simutrans lines
units = collections.defaultdict(list)
def unit(r, L, k, **kw):
    v = veh[r['cid']]
    u = dict(cid=r['cid'], num=v['num'], type=v['type'], paint=v['paint'], year=v['year'], depot=v['depot'], mode=mode(v),
             battery=battery(v), rec=L, kurz=int(k), note=r['note'], src=r['note'], pak=pak(v))
    u.update(kw); return u
REQ = S['battery_required']
groups = collections.defaultdict(list)
for s in SIM: groups[S.get('records_of', {}).get(s['line'], s['line'])].append(s)
for R, sims in groups.items():
    pool = [unit(r, L, k) for (L, k), r in kurz_car.items() if L == R]
    pool.sort(key=lambda u: -u['kurz'])                      # highest kurz first
    main = next(s for s in sims if s['line'] == R and s['main'])
    def take(s, n, low=False):
        cand = sorted(pool, key=lambda u: (not (u['battery'] or s['id'] not in REQ), u['kurz'] if low else -u['kurz']))
        for u in cand[:n]:
            if s['id'] in REQ and not u['battery']: continue
            units[s['id']].append(u); pool.remove(u)
    # the record line's own branches first (highest kurzy), then its main line (lowest kurzy), then the lines pooled
    # onto it (33 on 3, 88 on 8) from what is left; any rest goes to the main line (its surplus is marked not needed)
    for s in [x for x in sims if x is not main and x['line'] == R]: take(s, s['need'])
    take(main, main['need'], low=True)
    for s in [x for x in sims if x['line'] != R]: take(s, s['need'])
    units[main['id']] += pool
for s in SIM:
    units[s['id']].sort(key=lambda u: u['kurz'])
    # a bus on a trolleybus kurz is a substitute, not a roster type (dropped first by mark_spares)
    for u in units[s['id']]:
        if s['group'] == 'trolleybus' and u['mode'] == 'bus': u['sub'] = True
    mark_spares(units[s['id']], s['need'], type_of=lambda u: u['type'])

# ---- 5. designed vehicles from the line's history
def hist_rows(L):
    rows = []
    for f in glob.glob(os.path.join(RAW, 'vypravenost', 'history', S['history']['since'], f'L{L}_p*.html')): rows += rows_of(f)
    src = 'since'
    if not rows:
        for f in glob.glob(os.path.join(RAW, 'vypravenost', 'history', 'latest', f'L{L}_p*.html')): rows += rows_of(f)
        src = 'latest'
    rows = [r for r in rows if r['line'] == L and r['cid']]
    for r in rows:
        d = record_date(r['date']); r['d'] = d.isoformat() if d else ''; r['weekday'] = r['date'][:2] in ('PO', 'ÚT', 'ST', 'ČT', 'PÁ')
    rows = [r for r in rows if r['d'] and r['d'] < VD]      # older days only: the history before the vehicle day
    return rows, src
used = {u['cid'] for us in units.values() for u in us}
def free(cid, need_mode, need_bat):
    v = veh.get(cid)
    return bool(v) and v['state'] == 'zar' and cid not in out_that_day and cid not in used and mode(v) == need_mode \
        and (battery(v) or not need_bat) and v['type'] in PM['types']
designed, spares_hist, shortfalls = [], {}, {}
allhist = {}
for L in S['history']['lines']: allhist[L] = hist_rows(L)
for s in SIM:
    counted = [u for u in units[s['id']] if not u.get('spare')]
    k = s['need'] - len(counted)
    if k <= 0: continue
    shortfalls[s['id']] = k
    need_mode = s['group'] if s['line'] not in S.get('mode_override', {}) else S['mode_override'][s['line']]
    need_bat = s['id'] in REQ
    rows, src = allhist.get(s['line'], ([], 'none'))
    R = S.get('records_of', {}).get(s['line'])
    if R and not [r for r in rows if free(r['cid'], need_mode, need_bat)]: rows, src = allhist.get(R, ([], 'none')); src += f' (line {R})'
    last, cnt, wkd = {}, collections.Counter(), {}
    for r in rows:
        last[r['cid']] = max(last.get(r['cid'], ''), r['d']); cnt[r['cid']] += 1
        if r['weekday']: wkd[r['cid']] = True
    hist = [c for c in last if veh.get(c) and veh[c]['state'] == 'zar' and mode(veh[c]) == need_mode]
    rtypes = collections.Counter(veh[c]['type'] for c in hist)
    for u in units[s['id']]: rtypes[u['type']] += 1
    picks = []
    for _ in range(k):
        have = {u['type'] for u in units[s['id']] if not u.get('spare')} | {veh[c]['type'] for c, _w in picks}
        pool = [c for c in hist if free(c, need_mode, need_bat) and c not in [p for p, _w in picks]]
        lack = [t for t, _n in rtypes.most_common() if t not in have and any(veh[c]['type'] == t for c in pool)]
        why = ''
        if lack:
            pool = [c for c in pool if veh[c]['type'] == lack[0]]; why = f"covers the {PM['types'][lack[0]]['full']} type of the line's roster; "
        pool.sort(key=lambda c: (wkd.get(c, False), last[c], cnt[c]), reverse=True)   # weekday records first, then the latest
        if pool:
            c = pool[0]; ds = sorted({r['d'] for r in rows if r['cid'] == c}, reverse=True)[:3]
            why += f"last ran line {s['line'] if ' (line ' not in src else R} on {', '.join(nice(x) for x in ds)}"
            lastrun = ds
        else:
            own = collections.Counter(veh[c]['type'] for c in last if veh.get(c)) or collections.Counter(S['usual_types'][need_mode])
            cand = [c for c in veh if free(c, need_mode, need_bat) and c not in [p for p, _w in picks]]
            cand.sort(key=lambda c: (-own.get(veh[c]['type'], 0), -int(veh[c]['year'] or 0), int(veh[c]['num'] or 0)))
            if not cand: break
            c = cand[0]; lastrun = []
            why = (f"no free car in the line's own history; a free {PM['types'][veh[c]['type']]['full']}"
                   + (' with traction battery' if need_bat else '') + " (the line's usual type" + (", newest first)" if True else ")"))
        picks.append((c, why)); used.add(c)
        v = veh[c]
        units[s['id']].append(dict(cid=c, num=v['num'], type=v['type'], paint=v['paint'], year=v['year'], depot=v['depot'], mode=mode(v),
                                   battery=battery(v), rec=s['line'], kurz=None, note='', src='', designed=True, why=why,
                                   lastrun=lastrun, pak=pak(v)))
        designed.append(dict(line=s['id'], cid=c, num=v['num'], why=why))
    spares_hist[s['id']] = (hist, last, need_mode, need_bat, R)
# the free history cars left over, once every line has its designed cars (a car designed for one line is no spare of another)
spared = set()                       # a free car is listed once, on the first line whose history holds it
for sid, (hist, last, need_mode, need_bat, R) in spares_hist.items():
    s = next(x for x in SIM if x['id'] == sid)
    for c in sorted(hist, key=lambda c: last[c], reverse=True):
        if free(c, need_mode, need_bat) and c not in spared:
            spared.add(c)
            v = veh[c]
            units[sid].append(dict(cid=c, num=v['num'], type=v['type'], paint=v['paint'], year=v['year'], depot=v['depot'], mode=mode(v),
                                   battery=battery(v), rec=s['line'], kurz=None, note='', src='', designed=True, spare='not needed',
                                   why=f"free car of the line's history, last on line {R or s['line']} on {nice(last[c])}", lastrun=[last[c]], pak=pak(v)))

# ---- battery check: a battery-required line must only have battery cars counted
issues = [dict(line=s['id'], num=u['num']) for s in SIM if s['id'] in REQ for u in units[s['id']] if not u.get('spare') and not u['battery']]
save(dict(lines=units, excluded=excluded, designed=designed, shortfalls=shortfalls, battery_issues=issues,
          out_that_day=len(out_that_day), records=len(day_rows)), der(S, 'fleet.json'))
n = sum(1 for us in units.values() for u in us if not u.get('spare'))
print('records', len(day_rows), 'kurzy', len(kurz_car), 'excluded', len(excluded), '| counted', n,
      'designed', len(designed), 'not needed', sum(1 for us in units.values() for u in us if u.get('spare')))
for s in SIM:
    us = units[s['id']]
    print(f"{s['id']:>4} need {s['need']:2}  " + ' '.join(f"{u['num']}{'*' if u.get('designed') else ''}{'(x)' if u.get('spare') else ''}{'b' if u['battery'] else ''}" for u in us))
print('battery issues', issues)
for x in excluded: print('excluded', x)
