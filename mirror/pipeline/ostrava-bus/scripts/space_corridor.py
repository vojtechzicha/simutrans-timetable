"""Hand tool, not a run.py step:  python scripts/space_corridor.py LINE [LINE ...] [--fixline L] [--fix L:fr>to] [--free L:fr>to]
Spaces the rows of the given lines on their shared sections (owner, 22 Oct 2026: "solve the problems that are only in the
model, not in reality"). Each timed row may shift its slots by a constant within its interval; every branch keeps its
current need (pattern_need, as 04_roster sizes it). Pairs: rows in the same direction sharing >= 5 consecutive stops,
within a line and across lines. Score: per-stop smallest gap as a share of the even spacing (capped at 0.9, rounded to 0.05), worst stop first; then the
deviation from the real departures; then the fewest rows moved. Rows of other lines that touch the corridor can be
added as fixed with --fix (as they stand). Prints the proposal; nothing is written."""
import os, sys, math, itertools, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import CONFIG, load, make_nm, min_turnaround, pattern_need

C = CONFIG; nm0 = make_nm(C); AL = C['terminus_alias']
def nm(s): n = nm0(s); return AL.get(n, n)
S = load('schedule.json'); T = load('trips.json'); PK = load('peaks.json'); R = load('roster.json')
args = [a for k, a in enumerate(sys.argv[1:], 1) if not a.startswith('--') and not sys.argv[k - 1].startswith('--')]
def opt(flag): return [sys.argv[i + 1] for i, a in enumerate(sys.argv) if a == flag]
LINES = [a for a in args if a in S]; FIX = set(opt('--fix')); FREE = set(opt('--free')); FIXL = set(opt('--fixline')); MINSH = 5
hm = lambda m: '%02d:%02d' % divmod(m % 1440, 60)

rows = []   # dict(L, r, key, I, slots, prof, stops, deps)
for L in LINES + sorted(({k.split(':')[0] for k in FIX} | FIXL) - set(LINES)):
    A = PK[L]['anchor']
    for r in S[L]:
        if not (r.get('every') and r.get('real')) or r['every'] > 120: continue
        key = f"{L}:{r['fr']}>{r['to']}"
        if L not in LINES and key not in FIX and L not in FIXL: continue
        ts = [t for t in T[L] if nm0(t['fr']) == r['fr'] and nm0(t['to']) == r['to'] and t.get('times')]
        if not ts: continue
        ts.sort(key=lambda t: abs(t['dep'] - A)); t = max(ts[:4], key=lambda t: len(t['stops']))
        deps = [x['dep'] for x in ts if A - 60 <= x['dep'] <= A + 120]
        rows.append(dict(L=L, r=r, key=key, I=r['every'], slots=list(r['real']), prof=dict(zip(t['stops'], [x - t['dep'] for x in t['times']])),
                         stops=t['stops'], deps=deps, fixed=(L not in LINES) or key in FIX and key not in FREE))
idx = {x['key']: i for i, x in enumerate(rows)}

def dev(x, s):   # worst distance of a real departure from the shifted slots
    I = x['I']; sl = [(v + s) % I for v in x['slots']]
    return max((min(min((d - v) % I, (v - d) % I) for v in sl) for d in x['deps']), default=0)

pairs = []   # rows in the same direction sharing >= MINSH consecutive stops
for i, j in itertools.combinations(range(len(rows)), 2):
    a, b = rows[i], rows[j]; pos = {s: k for k, s in enumerate(b['stops'])}; best = []
    for p in range(len(a['stops'])):
        q = pos.get(a['stops'][p])
        if q is None: continue
        k = 0
        while p + k < len(a['stops']) and q + k < len(b['stops']) and a['stops'][p + k] == b['stops'][q + k]: k += 1
        if k > len(best): best = a['stops'][p:p + k]
    if len(best) >= MINSH: pairs.append(dict(i=i, j=j, shared=best))
# stop groups: at each shared stop, every row that runs a shared section through it (the buses a passenger sees)
comp = list(range(len(rows)))   # rows linked by pairs run the same direction; never group the two directions at a stop
def root(i):
    while comp[i] != i: i = comp[i]
    return i
for p in pairs: comp[root(p['i'])] = root(p['j'])
groups = {}
for p in pairs:
    for st in p['shared']:
        groups.setdefault((st, root(p['i'])), set()).update((p['i'], p['j']))
G = []
for (st, _c), mem in groups.items():
    mem = sorted(mem); P = 1
    for i in mem: P = P * rows[i]['I'] // math.gcd(P, rows[i]['I'])
    if P > 240: continue
    n = sum(len(rows[i]['slots']) * P // rows[i]['I'] for i in mem)
    G.append(dict(st=st, mem=mem, P=P, ideal=P / n, off={i: rows[i]['prof'][st] for i in mem}))
def gaps_at(g, sh):
    ev = sorted(((v + sh.get(i, 0) + g['off'][i] + k * rows[i]['I']) % g['P'], i) for i in g['mem'] for v in rows[i]['slots'] for k in range(g['P'] // rows[i]['I']))
    return min(((ev[(k + 1) % len(ev)][0] - ev[k][0]) % g['P'] for k in range(len(ev)) if ev[(k + 1) % len(ev)][1] != ev[k][1] and not (rows[ev[k][1]]['fixed'] and rows[ev[(k + 1) % len(ev)][1]]['fixed'])), default=g['P'])   # two fixed rows: not ours to change (48/78 bunch in reality)

# branches whose need must not grow
branches = []
for L in LINES:
    tr = [dict(t, o=nm(t['fr']), d=nm(t['to'])) for t in T[L]]
    lay = {k: min(C['cycle_lay'], v) for k, v in min_turnaround(tr).items()}; T0 = PK[L]['anchor']
    for b in R['branches'][L]['branches']:
        if b.get('how') != 'pattern': continue
        ia = next((i for i, x in enumerate(rows) if x['L'] == L and nm(x['r']['fr']) == b['a'] and nm(x['r']['to']) == b['b']), None)
        ib = next((i for i, x in enumerate(rows) if x['L'] == L and nm(x['r']['fr']) == b['b'] and nm(x['r']['to']) == b['a']), None)
        if ia is None or ib is None: continue
        def rt_(x, y):
            r_ = [t['arr'] - t['dep'] for t in tr if t['o'] == x and t['d'] == y and T0 - 60 <= t['dep'] < T0 + 120] or [t['arr'] - t['dep'] for t in tr if t['o'] == x and t['d'] == y]
            return round(sum(r_) / len(r_))
        rts = [rt_(b['a'], b['b']), rt_(b['b'], b['a'])]; lays = [lay.get(b['a'], C['cycle_lay']), lay.get(b['b'], C['cycle_lay'])]
        branches.append(dict(L=L, ia=ia, ib=ib, rts=rts, lays=lays, T0=T0, need=b['need'], memo={}))
def need(br, sa, sb):
    k = (sa, sb)
    if k not in br['memo']:
        ra, rb = rows[br['ia']], rows[br['ib']]
        br['memo'][k] = pattern_need([dict(every=ra['I'], real=[(v + sa) % ra['I'] for v in ra['slots']]),
                                      dict(every=rb['I'], real=[(v + sb) % rb['I'] for v in rb['slots']])], br['rts'], br['lays'], br['T0'])[0]
    return br['memo'][k]

V = [i for i, x in enumerate(rows) if not x['fixed']]
rng = {i: list(range(-(rows[i]['I'] // 2), rows[i]['I'] - rows[i]['I'] // 2)) for i in V}
def score(sh):
    for br in branches:
        if need(br, sh.get(br['ia'], 0), sh.get(br['ib'], 0)) > br['need']: return None
    rs = [min(gaps_at(g, sh) / g["ideal"], 0.9) for g in G]
    devs = sum(dev(rows[i], sh.get(i, 0)) for i in V)
    moved = sum(1 for i in V if sh.get(i, 0))
    lex = tuple(sorted(round(r * 20) / 20 for r in rs))   # leximin: the worst stop first, then the next (a plateau of zeros must not stall the search)
    return (lex, -moved, -devs)   # every moved row is an in-game edit for the owner
start = {i: 0 for i in V}; best = (score(start), dict(start)); random.seed(1)
for rep in range(40):
    cur = dict(start) if rep == 0 else {i: random.choice(rng[i]) for i in V}
    sc = score(cur)
    while sc is None:
        cur = {i: random.choice(rng[i]) for i in V}; sc = score(cur)
    improved = True
    while improved:
        improved = False
        for i in V:
            for s in rng[i]:
                c2 = dict(cur); c2[i] = s; s2 = score(c2)
                if s2 is not None and s2 > sc: cur, sc, improved = c2, s2, True
    if sc > best[0]: best = (sc, dict(cur))
sc, sh = best
print('worst stops (gap / even):', sc[0][:6], 'moved', -sc[1], 'dev', -sc[2], ' | before:', score(start)[0][:6])
for i, x in enumerate(rows):
    s = sh.get(i, 0); I = x['I']; new = sorted((v + s) % I for v in x['slots'])
    mark = 'fixed' if x['fixed'] else ('MOVE' if s else 'keep')
    print(f"  [{mark}] {x['key']}: every {I} {sorted(x['slots'])} -> {new}  dev {dev(x, 0)} -> {dev(x, s)}  real {' '.join(hm(d) for d in sorted(x['deps']))}")
for br in branches:
    print(f"  need {br['L']} {rows[br['ia']]['r']['fr']} <-> {rows[br['ia']]['r']['to']}: {br['need']} -> {need(br, sh.get(br['ia'], 0), sh.get(br['ib'], 0))}")
worst = {}
for g in G:
    k = tuple(g['mem']); r0 = gaps_at(g, {}); r1 = gaps_at(g, sh)
    if k not in worst or r1 / g['ideal'] < worst[k][1] / worst[k][3]: worst[k] = (g['st'], r1, r0, g['ideal'])
for k, (st, r1, r0, ideal) in sorted(worst.items(), key=lambda x: x[1][1] / x[1][3]):
    print(f"  worst stop for {' + '.join(rows[i]['key'] for i in k)}: {st} closest {r0} -> {r1} min (even {ideal:.1f})")
