"""Branch check for legs read at a midpoint (core_to before the terminal, or knot after the terminal), every regional sheet.
For each such leg: its own trips (schedule.json, the trips the leg stands for), classed by where they really end (out legs
read to core_to) or start (legs read at a knot):
  term  = at the leg's terminal (or its alias)
  path  = at a stop on the leg's own path (a short working; nothing hidden)
  beyond = it passes the leg's terminal and runs on (an extension: the line is cut where they meet)
  branch = it never reaches the terminal and ends / starts off the path  <- what hid 292's Strahovice trips
Printed per leg: afternoon (13-18) counts per class, the window slots and the trip each stands for, and the 'other' ends.
usage: python -X utf8 audit/branch_check.py [pipeline dir] (25 Oct 2026, after the 292 split)"""
import json, os, sys, collections
PIPE = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHEETS = ['odis-regional-hko', 'odis-regional-tfj', 'odis-regional-opavsko', 'odis-regional-novojicinsko', 'odis-regional-bruntalsko']
def hm(t): return '%d:%02d' % (t // 60 % 24, t % 60)
out = {}
for sh in SHEETS:
    base = os.path.join(PIPE, sh)
    cfg = json.load(open(os.path.join(base, 'config.json'), encoding='utf-8'))
    AL = lambda s, a=cfg.get('terminus_alias', {}): a.get(s, s)
    S = json.load(open(os.path.join(base, 'data', 'derived', 'schedule.json'), encoding='utf-8'))
    T = json.load(open(os.path.join(base, 'data', 'derived', 'trips.json'), encoding='utf-8'))
    sys.path.insert(0, os.path.join(PIPE, 'odis-regional-hko', 'scripts'))
    os.environ['ODIS_BASE'] = base
    import importlib, lib; importlib.reload(lib)
    nm = lib.nm
    byid = {(t['lic'], t['sp']): t for L, ts in T.items() for t in ts}
    rows = []
    for L, spec in cfg['lines'].items():
        if L not in S: continue
        for si, (sl, ss) in enumerate(zip(spec.get('sim', []), S[L]['sim'])):
            for lg, g in zip(sl['legs'], ss['legs']):
                if g.get('untimed'): continue
                mid_to = 'core_to' in lg and AL(lg['core_to']) != AL(lg['to'])
                mid_fr = 'knot' in lg and AL(lg['knot']) != AL(lg['fr'])
                if not (mid_to or mid_fr): continue
                path = set(AL(x) for x in g['stops'])
                cls = collections.Counter(); oth = collections.Counter(); slots = []
                trips = g.get('trips', [])
                def end_of(tr):
                    t = byid.get((tr['lic'], tr['sp']))
                    e = AL(nm(t['to'] if mid_to else t['fr'])) if t else AL(tr['to0'] if mid_to else tr['fr0'])
                    term = AL(g['to'] if mid_to else g['fr'])
                    if e == term: return 'term', e
                    if e in path: return 'path', e
                    st = [AL(nm(x)) for x in t['stops']] if t else []
                    return ('beyond' if term in st else 'branch'), e
                for tr in trips:
                    if 780 <= tr['d'] < 1080:
                        c, e = end_of(tr); cls[c] += 1
                        if c in ('beyond', 'branch'): oth[(c, e)] += 1
                W = ss['window']
                for sl_t in g['window']['slots']:
                    near = min(trips, key=lambda tr: abs(tr['d'] - sl_t), default=None)
                    if near and abs(near['d'] - sl_t) <= 3:
                        c, e = end_of(near); slots.append((hm(sl_t), c, e))
                    else: slots.append((hm(sl_t), 'empty', ''))
                rows.append(dict(sheet=sh.replace('odis-regional-', ''), line=L, sim=ss['name'], fr=g['fr'], to=g['to'],
                                 read=('core_to ' + lg['core_to']) if mid_to else ('knot ' + lg['knot']), cls=dict(cls),
                                 other={f'{c}: {e}': n for (c, e), n in oth.items()}, slots=slots))
    out[sh] = rows
for sh, rows in out.items():
    print('=' * 8, sh, len(rows), 'legs read at a midpoint')
    for r in rows:
        flag = 'SLOT-BRANCH' if any(c == 'branch' for _, c, _ in r['slots']) else ('BRANCH' if r['cls'].get('branch') else ('beyond' if r['cls'].get('beyond') else 'ok'))
        print(f"[{flag}] {r['sim']}: {r['fr'].split(', ',1)[-1][:28]} -> {r['to'].split(', ',1)[-1][:28]} ({r['read'][:45]})")
        print(f"      afternoon trips {r['cls']}; window slots {r['slots']}")
        if r['other']: print(f"      ends off the path: {r['other']}")
