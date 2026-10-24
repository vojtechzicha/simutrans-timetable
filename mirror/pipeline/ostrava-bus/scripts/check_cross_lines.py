"""Check, not a run.py step:  python scripts/check_cross_lines.py [min_shared_stops]
Like check_trunks.py, but across lines: two rows of different DPO lines that run >= N (default 8) consecutive stops in the
same direction. "!!" marks a closest gap <= 3 min where an even spacing would give >= 6 (owner, 21 Oct 2026: 35 and 39
left Dům energetiky 1 min apart towards Otakara Jeremiáše)."""
import os, sys, math, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import CONFIG, load, make_nm
nm = make_nm(CONFIG); N = int(sys.argv[1]) if len(sys.argv) > 1 else 8
S = load('schedule.json'); T = load('trips.json'); PK = load('peaks.json')
prof = []
for L, rows in S.items():
    if L not in T: continue
    A = PK[L]['anchor']
    for r in rows:
        if not (r.get('every') and r.get('real')) or r['every'] > 120: continue
        ts = [t for t in T[L] if nm(t['fr']) == r['fr'] and nm(t['to']) == r['to'] and t.get('times')]
        if not ts: continue
        ts.sort(key=lambda t: abs(t['dep'] - A)); t = max(ts[:4], key=lambda t: len(t['stops']))
        prof.append((L, r, t['stops'], [x - t['dep'] for x in t['times']]))
out = []
for (L1, r1, s1, o1), (L2, r2, s2, o2) in itertools.combinations(prof, 2):
    if L1 == L2 or not set(s1) & set(s2): continue
    best = []; pos2 = {s: i for i, s in enumerate(s2)}
    for a in range(len(s1)):
        b = pos2.get(s1[a])
        if b is None: continue
        k = 0
        while a + k < len(s1) and b + k < len(s2) and s1[a + k] == s2[b + k]: k += 1
        if k > len(best): best = [(a + q, b + q) for q in range(k)]
    if len(best) < N: continue
    P = r1['every'] * r2['every'] // math.gcd(r1['every'], r2['every'])
    if P > 240: continue
    n = len(r1['real']) * P // r1['every'] + len(r2['real']) * P // r2['every']; ideal = P / n
    worst = None
    for a, b in best:
        t1 = [(x + o1[a] + r1['every'] * k) % P for x in r1['real'] for k in range(P // r1['every'])]
        t2 = [(x + o2[b] + r2['every'] * k) % P for x in r2['real'] for k in range(P // r2['every'])]
        g = min(min((u - v) % P, (v - u) % P) for u in t1 for v in t2)
        if worst is None or g < worst[0]: worst = (g, s1[a], sorted(t1), sorted(t2))
    out.append((worst[0] <= 3 and ideal >= 6, L1, r1['fr'], r1['to'], L2, r2['fr'], r2['to'], len(best), s1[best[0][0]], s1[best[-1][0]], worst, round(ideal, 1)))
for o in sorted(out, key=lambda o: (not o[0], o[10][0], -o[7])):
    if not o[0] and '--all' not in sys.argv: continue
    f, L1, a1, b1, L2, a2, b2, n, x0, x1, w, ideal = o
    print(('!! ' if f else '   ') + f"{L1} {a1} -> {b1}  |  {L2} {a2} -> {b2}: {n} stops ({x0} .. {x1}); closest {w[0]} min at {w[1]} (even {ideal})")
