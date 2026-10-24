"""Check, not a run.py step:  python scripts/check_trunks.py
Rows of one line that run >= 3 consecutive stops in the same direction: how close do their buses come on the shared
section? "!!" marks a closest gap <= 5 min and under half the even spacing (21 Oct 2026: 59 had two branches 4 min apart
all through Polanka, which the far-end `passing` rule did not see). Compare a flag with the real times at the junction."""
import os, sys, math, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import CONFIG, load, make_nm
nm = make_nm(CONFIG)
S = load('schedule.json'); T = load('trips.json'); PK = load('peaks.json')
out = []
for L, rows in S.items():
    rs = [r for r in rows if r.get('every') and r.get('real')]
    if len(rs) < 2: continue
    A = PK[L]['anchor']; prof = {}
    for i, r in enumerate(rs):
        ts = [t for t in T[L] if nm(t['fr']) == r['fr'] and nm(t['to']) == r['to'] and t.get('times')]
        if not ts: continue
        ts.sort(key=lambda t: abs(t['dep'] - A))
        t = max(ts[:4], key=lambda t: len(t['stops']))   # fullest trip near the anchor
        prof[i] = (t['stops'], [x - t['dep'] for x in t['times']])
    for i, j in itertools.combinations(prof, 2):
        si, oi = prof[i]; sj, oj = prof[j]
        # longest run of consecutive stops the two trips share in the same order
        best = []
        for a in range(len(si)):
            for b in range(len(sj)):
                k = 0
                while a + k < len(si) and b + k < len(sj) and si[a + k] == sj[b + k]: k += 1
                if k > len(best): best = [(a + q, b + q) for q in range(k)]
        if len(best) < 3: continue
        ri, rj = rs[i], rs[j]
        P = ri['every'] * rj['every'] // math.gcd(ri['every'], rj['every'])
        if P > 240: continue
        mi = ri['real']; mj = rj['real']
        ni, nj = len(mi) * P // ri['every'], len(mj) * P // rj['every']
        ideal = P / (ni + nj)
        worst = None
        for a, b in best:
            ti = sorted((x + oi[a] + ri['every'] * k) % P for x in mi for k in range(P // ri['every']))
            tj = sorted((x + oj[b] + rj['every'] * k) % P for x in mj for k in range(P // rj['every']))
            g = min(min((u - v) % P, (v - u) % P) for u in ti for v in tj)
            if worst is None or g < worst[0]: worst = (g, si[a], ti, tj)
        flag = worst[0] <= 5 and worst[0] < 0.5 * ideal
        out.append((flag, L, ri['fr'], ri['to'], rj['fr'], rj['to'], len(best), si[best[0][0]], si[best[-1][0]], worst[0], round(ideal, 1)))
for o in sorted(out, key=lambda o: (not o[0], o[1])):
    f, L, a1, b1, a2, b2, n, s0, s1, g, ideal = o
    print(('!! ' if f else '   ') + f"{L}: {a1} -> {b1}  |  {a2} -> {b2}  shared {n} stops ({s0} .. {s1}): closest {g} min (even would be {ideal})")
