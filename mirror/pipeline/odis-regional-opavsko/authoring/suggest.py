"""Step 4 of the bus schedule method as a suggestion: suggest.py LINES A_stop B_stop [win_from win_to] [--via X] [--notvia Y]
For trips of LINES passing A then B (time at A) and B then A (time at B), over the whole day 5-23, try every allowed interval
P and k slots (1..8): slots in the model window must equal the real departures there +-1, >=80% of window slots need a real
departure within 3 min; rank by exact hits over the day, then within 1, then simplest, then worst deviation. Same P,k both ways."""
import sys, itertools
import os
os.environ['ODIS_BASE'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'odis-regional-hko', 'scripts'))
from lib import load, nm, hm, AL, line_anchor
T = load('trips.json')
args = [a for a in sys.argv[1:] if not a.startswith('--')]
opts = {}
for i, a in enumerate(sys.argv):
    if a.startswith('--'): opts.setdefault(a[2:], []).append(sys.argv[i + 1])
lines = args[0].split(','); A, B = args[1], args[2]
def deps(x, y):
    out = []
    for L in lines:
        for t in T[L]:
            st = [AL(nm(s)) for s in t['stops']]
            if x in st and y in st[st.index(x) + 1:]:
                i = st.index(x); j = st.index(y, i + 1); seg = st[i:j + 1]
                if any(v not in seg for v in opts.get('via', [])) or any(v in seg for v in opts.get('notvia', [])): continue
                out.append((t['times'][i], t['times'][j] - t['times'][i]))
    return sorted(out)
DA, DB = deps(A, B), deps(B, A)
if len(args) > 3: W = (int(args[3]), int(args[4]))
else:
    an = line_anchor([t for L in lines for t in T[L]], dict(peak_minute=960)); W = (an['anchor'] - 30, an['anchor'] + 90)
print('A->B', ' '.join(hm(d) for d, _ in DA)); print('B->A', ' '.join(hm(d) for d, _ in DB)); print('window', hm(W[0]), hm(W[1]))
ALLOWED = [d for d in range(10, 481) if 1440 % d == 0]
def cd(a, b, P): return min((a - b) % P, (b - a) % P)
def best_res(D, P, k):
    D = [d for d in D if 300 <= d < 1380]; best = None
    for r0 in range(P):
        # k slots: try evenly spaced and the k commonest residues around the exact hits
        pass
    return best
def score(D, P, R, W):
    D = [d for d, _ in D]
    Dd = [d for d in D if 300 <= d < 1380]
    dev = [min(cd(d, r, P) for r in R) for d in Dd]
    ws = [t for t in range(W[0], W[1]) if t % P in R]; wd = [d for d in D if W[0] <= d < W[1]]
    filled = sum(1 for s in ws if any(abs(s - d) <= 3 for d in D))
    span = (min(Dd) - 30, max(Dd) + 30) if Dd else (300, 1380)
    sd = [t for t in range(span[0], span[1]) if t % P in R]
    hit = {r: sum(1 for d in Dd if cd(d, r, P) <= 3) for r in R}
    return dict(exact=sum(1 for v in dev if v == 0), w1=sum(1 for v in dev if v <= 1), w3=sum(1 for v in dev if v <= 3), n=len(Dd),
                worst=max(dev, default=0), ws=len(ws), wd=len(wd), filled=filled, sd=len(sd), min_hit=min(hit.values()))
res = []
for P in ALLOWED:
    for k in range(1, 9):
        if k > 1 and P <= 30 and k * 10 > P: continue
        out = []
        for D in (DA, DB):
            if not D: out.append(None); continue
            # candidate residues: residues of real departures (exact hits), choose k maximizing exact hits then w1
            from collections import Counter
            cnt = Counter(d % P for d, _ in D if 300 <= d < 1380)
            cand = [r for r, _ in cnt.most_common(12)]
            bestR = None
            for R in itertools.combinations(sorted(set(cand)), min(k, len(set(cand)))):
                if len(R) < k: continue
                s = score(D, P, R, W)
                key = (s['ws'] in (s['wd'] - 1, s['wd'], s['wd'] + 1) and s['ws'] > 0, s['filled'] >= 0.8 * s['ws'] and s['min_hit'] >= 2, s['exact'], s['w1'], -s['worst'])
                if bestR is None or key > bestR[0]: bestR = (key, R, s)
            out.append(bestR)
        if any(o is None for o in out if o is not None) or all(o is None for o in out): continue
        ok = all(o is None or (o[0][0] and o[0][1]) for o in out)
        tot_ex = sum(o[2]['exact'] for o in out if o); tot1 = sum(o[2]['w1'] for o in out if o)
        sc = sum(o[2]['w3'] - 0.5 * o[2]['sd'] for o in out if o)
        res.append((ok, round(sc, 1), tot_ex, -k, P, out))
res.sort(key=lambda x: (x[0], x[1], x[2], x[3], x[4]), reverse=True)
for ok, sc, ex, k, P, out in res[:int(opts.get('top', ['10'])[0])]:
    print(('OK ' if ok else '-- ') + f"every {P:3} k={-k}: score {sc} exact {ex} | " + ' || '.join(
        (f"{','.join(hm(r) if P > 60 else ':%02d' % r for r in o[1])} ex{o[2]['exact']}/{o[2]['n']} w3 {o[2]['w3']} worst {o[2]['worst']} win {o[2]['ws']}s/{o[2]['wd']}d fill {o[2]['filled']} sd {o[2]['sd']} mh {o[2]['min_hit']}") if o else '-' for o in out))
