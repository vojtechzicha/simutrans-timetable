"""All lines at a hub whose ODIS lines are modelled on the regional sheets (config.hubs; owner, 25 Oct 2026) -> derived/hubs.json,
rendered by 06_render.py after the Hranečník section.

Hranečník's ODIS lines were modelled here (20 Oct, before the regional sheets existed), and the regional sheets link to them.
At a hub added later the regional sheets came first, so it is the other way round: each ODIS line is shown as its home sheet
sets it, read from that sheet's derived data, and linked. Lines shared between sheets are listed and linked, not repeated, and
no bus is on two sheets (kb/rules/bus-sheets.md). Nothing here changes the regional sheets.

1. Lines: every non-DPO line in the national JDF with a stop at the hub (01c_fetch_odis.py --hubs), merged by ODIS number
   (the last three digits of the licence); the DPO lines with a trip stopping there on the vehicle day; the trams and
   trolleybuses of the sister sheets (config.hubs_other_modes) that stop there.
2. Home sheet: the first of config.regional_sheets (build order) whose derived schedule.json models the line, else the first
   whose config.unmodelled lists it (with its reason). A line on no sheet is flagged: it would have to be modelled here.
3. For each Simutrans line of the home sheet: its legs (typed values, real minutes, fit), the minutes it leaves, passes or
   reaches the hub (the slot plus the median time from the leg's terminal to the hub on its own trips), and its buses
   (home roster.json), which are counted there, not here.
"""
import collections, json, os, re, statistics
from lib import CONFIG, RAW, ROOT, load, save, make_nm, hm, day, pick_version

C = CONFIG; nm0 = make_nm(C); d = day(C['vehicle_day'])
OUT = os.path.join(os.path.dirname(RAW), C['odis']['snapshot'], 'odis')
PIPE = os.path.dirname(ROOT)
def rel(p): return os.path.normpath(os.path.join(ROOT, p))
def jl(p): return json.load(open(p, encoding='utf-8'))

SHEETS = []
for p in C.get('regional_sheets', []):
    cf = jl(os.path.join(rel(p), 'config.json')); dv = os.path.join(rel(p), 'data', 'derived')
    SHEETS.append(dict(dir=p, key=os.path.basename(p), title=cf['title'], url=cf.get('artifact_url'), day=cf.get('vehicle_day_label_en'),
                       loop=cf.get('all_termini_are_loops', True), areas=cf.get('areas', []), unmodelled=cf.get('unmodelled', {}),
                       S={k: v for k, v in jl(os.path.join(dv, 'schedule.json')).items() if not k.startswith('_')},
                       R=jl(os.path.join(dv, 'roster.json'))['lines'], T=jl(os.path.join(dv, 'trips.json'))))

def home_of(L):
    for sh in SHEETS:
        if sh['S'].get(L, {}).get('sim'): return sh, 'modelled'
    for sh in SHEETS:
        if L in sh['unmodelled']: return sh, 'unmodelled'
    return None, 'none'

def operator(sh, lic):
    a = next((a for a in (sh or {}).get('areas', []) if lic.startswith(a.get('prefix', '-'))), {})
    return a.get('operator') or C['odis']['carriers'].get('45192081', {}).get('name', '')

def first_at(t, match):
    i = next((i for i, s in enumerate(t['stops']) if match in s), None)
    return t['times'][i] if i is not None and t.get('times') else None

def leg_at_hub(sh, L, g, match, win):
    """when the leg's buses are at the hub: from the hub (offset 0), to it (arrival) or through it, model and real"""
    if g['untimed'] or not g.get('trips'): return None
    by = {(t.get('lic'), t['sp']): t for ln in g['lines'] for t in sh['T'].get(ln, [])}
    offs, real = [], []
    for x in g['trips']:
        t = by.get((x.get('lic'), x['sp']))
        th = first_at(t, match) if t else None
        if th is None: continue
        offs.append(th - x['d'])
        if win[0] <= x['d'] < win[1]: real.append(th)
    if not offs: return None
    off = round(statistics.median(offs))
    kind = 'from' if match in g['fr'] else 'to' if match in g['to'] else 'via'
    return dict(kind=kind, off=off, model=[s + off for s in g['window']['slots']], real=sorted(real))

hubs = []
for H in C.get('hubs', []):
    match = H['match']
    vers = jl(os.path.join(OUT, f"hub_{H['id']}.json"))
    T = load('trips.json'); CLS = load('line_class.json'); DIC = C['odis']['dpo_ic']
    dpo = sorted((L for L, ts in T.items() if any(match in s for t in ts for s in t['stops'])), key=int)
    dpo_off = [dict(line=L, cls=CLS.get(L, {}).get('cls')) for L in sorted({str(int(v['line'][3:])) for v in vers if v['ic'] == DIC}, key=int) if L not in dpo]
    vers = [v for v in vers if v['ic'] != DIC]
    other = {}
    for mode, p in C.get('hubs_other_modes', {}).items():
        tt = jl(rel(p))
        other[mode] = sorted((L for L, ts in tt.items() if any(match in s for t in ts for s in t.get('stops', []))), key=int)
    nums = collections.defaultdict(list)
    for v in vers: nums[v['line'][-3:]].append(v)
    odis = []
    for L in sorted(nums, key=int):
        codes = sorted({v['line'] for v in nums[L]})
        valid = [pick_version([v for v in nums[L] if v['line'] == c], d) for c in codes]
        v0 = next((v for v in valid if v), nums[L][0])
        sh, status = home_of(L)
        x = dict(line=L, codes=codes, name=re.sub(r'\s*-\s*', ' – ', v0['name']), operator=operator(sh, codes[0]), status=status,
                 diversion=any(v and v['diversion'] for v in valid),
                 home=dict(key=sh['key'], title=sh['title'], url=sh['url'], day=sh['day']) if sh else None)
        if status == 'unmodelled': x['reason'] = sh['unmodelled'][L]
        if status == 'modelled':
            s = sh['S'][L]; x.update(core=s.get('core', []), note=s.get('note', ''), anchor=s.get('anchor', {}), sims=[])
            ros = {r['name']: r for r in sh['R'].get(L, [])}
            for sim in s['sim']:
                win = sim.get('window') or [0, 1440]
                legs = [dict(fr=g['fr'], to=g['to'], untimed=g['untimed'], every=g.get('every') or 0, set=g.get('set', []), real=g.get('real', []),
                             rt=g.get('rt'), stat=g.get('stat'), empty=(g.get('window') or {}).get('empty', []), knot=g.get('knot'),
                             via=g.get('via', []), notvia=g.get('notvia', []), hub=leg_at_hub(sh, L, g, match, win)) for g in sim['legs']]
                r = ros.get(sim['name'], {})
                bus = lambda v, k: dict(num=v['num'], full=v.get('full') or v.get('type'), len=v.get('len'), plate=v.get('plate'),
                                        paint=v.get('paint'), kind=k, why=v.get('seen') if k == 'seen' else v.get('why'))
                x['sims'].append(dict(name=sim['name'], every=sim['every'], need=sim['need'], window=win, waits=sim.get('waits'),
                                      loop=sh['loop'], legs=legs, buses=[bus(v, 'seen') for v in r.get('seen', [])] + [bus(v, 'designed') for v in r.get('designed', [])],
                                      not_needed=len(r.get('not_needed', []))))
        odis.append(x)
        print(H['id'], L, status, sh['key'] if sh else '-', [(s_['name'], s_['every'], s_['need'], [(g['hub'] or {}).get('kind') for g in s_['legs']]) for s_ in x.get('sims', [])])
    hubs.append(dict(id=H['id'], name=H['name'], stop=H['stop'], nav=H['nav'], dpo=dpo, dpo_off=dpo_off, other=other, odis=odis,
                     snapshot=f"CIS JŘ bus JDF export of {C['snapshot']}"))
    print(H['id'], 'DPO', dpo, 'other modes', other)
save('hubs.json', dict(why=C.get('hubs_why'), hubs=hubs))
