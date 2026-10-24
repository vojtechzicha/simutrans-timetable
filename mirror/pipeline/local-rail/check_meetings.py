"""Single-track meeting check for a repeating pattern: one out train (real times) against the back train repeated
every P min. Prints where each back train meets the out train: "cross at" a station where both stand, or CONFLICT on
the stretch where they would meet on open line. Used 14 Oct 2026 to pick the hourly S57 and U12 pairs (build_s5.py).
Run: python pipeline/local-rail/check_meetings.py 6714 6707 "Rakovník" "Osek město" 60
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_012_014_235 as base
by_num, wd = base.load()
o, i, A, B, P = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], int(sys.argv[5])
def seg(n, a, b):
    st = by_num[n]['stops']; nm = [s['name'] for s in st]
    st = st[nm.index(a):nm.index(b) + 1]
    return [(s['name'], int(s['arr'] if s['arr'] is not None else s['dep']), int(s['dep'] if s['dep'] is not None else s['arr'])) for s in st]
out, inn = seg(o, A, B), seg(i, B, A)
order = [s[0] for s in out]
inn = [s for s in inn if s[0] in order]
pos = {n: k for k, n in enumerate(order)}
# occupancy intervals: at station k [arr,dep]; on segment k..k+1 (dep_k, arr_k+1)
def occ(tr):
    r = []
    for k, (n, a, d) in enumerate(tr):
        r.append(('st', pos[n], a, d))
        if k + 1 < len(tr):
            r.append(('seg', min(pos[n], pos[tr[k+1][0]]), d, tr[k+1][1]))
    return r
O = occ(out)
t0, t1 = out[0][2], out[-1][1]
for k in range(-6, 7):
    I = [(t, p, a + k * P, d + k * P) for t, p, a, d in occ(inn)]
    if I[-1][3] < t0 or I[0][2] > t1: continue
    # find first overlap: same segment overlapping in time -> conflict; same station overlapping -> crossing
    hits = []
    for t, p, a, d in O:
        for t2, p2, a2, d2 in I:
            if t == t2 and p == p2 and max(a, a2) < min(d, d2) + (1 if t == 'st' else 0):
                hits.append((t, order[p] + ('' if t == 'st' else ' – ' + order[p+1]), base.hm(max(a, a2))))
    # crossing happens where they pass; report station hits, or segment conflicts
    segs = [h for h in hits if h[0] == 'seg']
    sts = [h for h in hits if h[0] == 'st']
    print(f"in train leaving {base.hm(inn[0][2] + k*P)}:", 'CONFLICT ' + str(segs) if segs else 'cross at ' + str(sts))
