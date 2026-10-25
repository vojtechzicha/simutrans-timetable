"""Step 4 evaluator, one direction of one line: python -X utf8 step4.py LINES A B W0 W1 P slot[,slot..] [--sheet <folder>] [--via X] [--notvia Y] [--rd K]
A and B are substrings of the raw JDF stop names (spaces ignored, e.g. "sad B.N", "Kobeřice,aut.st"); slots are H:MM or minutes.
Times are read at A (or at --rd K, a knot passed between A and B) for trips of LINES passing A then B.
Prints the real times (whole day 5-23, window marked), then for the slots: window slots vs real departures,
slots with a real departure within 3 min, exact / within 1 / within 3 over the day, worst, and the off-pattern trips."""
import json, sys
import os
SHEET = next((sys.argv[i + 1] for i, a in enumerate(sys.argv) if a == '--sheet'), 'odis-regional-opavsko')
P0 = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), SHEET, 'data', 'derived', 'trips.json')
T = json.load(open(P0, encoding='utf-8'))
a = [x for x in sys.argv[1:]]
opts = {}
pos = []
i = 0
while i < len(a):
    if a[i].startswith('--'): opts[a[i][2:]] = a[i + 1]; i += 2
    else: pos.append(a[i]); i += 1
lines, A, B, W0, W1, P, sl = pos[0].split(','), pos[1], pos[2], pos[3], pos[4], int(pos[5]), pos[6]
def tm(s): h, m = s.split(':'); return int(h) * 60 + int(m)
def hm(t): return '%d:%02d' % (t // 60 % 24, t % 60)
W = (tm(W0), tm(W1))
R = sorted({(tm(x) if ':' in x else int(x)) % P for x in sl.split(',')})
rd = opts.get('rd')
def n(s): return s.replace(' ', '')
deps = []
for L in lines:
    for t in T[L]:
        st = [n(x) for x in t['stops']]
        ia = next((i for i, x in enumerate(st) if n(A) in x), None)
        if ia is None: continue
        ib = next((i for i in range(ia + 1, len(st)) if n(B) in st[i]), None)
        if ib is None: continue
        if 'via' in opts and not any(n(opts['via']) in x for x in st): continue
        if 'notvia' in opts and any(n(opts['notvia']) in x for x in st): continue
        k = ia
        if rd:
            k = next((i for i in range(ia, ib + 1) if n(rd) in st[i]), None)
            if k is None: continue
        deps.append((t['times'][k], L, t['sp'], t['fr'].split(',')[-1][:14], t['to'].split(',')[-1][:14]))
deps.sort()
cd = lambda x, r: min((x - r) % P, (r - x) % P)
day = [d for d in deps if 300 <= d[0] < 1380]
print(f"{'+'.join(lines)} {A} -> {B}" + (f" read at {rd}" if rd else '') + f": {len(day)} trips 5-23")
print('  ' + ' '.join(('[' if W[0] <= d[0] < W[1] else '') + hm(d[0]) + ('' if d[1] == lines[0] else f'({d[1]})') + (']' if W[0] <= d[0] < W[1] else '') for d in day))
ws = [t for t in range(W[0], W[1]) if t % P in R]
wd = [d[0] for d in day if W[0] <= d[0] < W[1]]
fill = [s for s in ws if any(abs(s - d[0]) <= 3 for d in day)]
dev = [(min(cd(d[0], r) for r in R), d) for d in day]
print(f"  every {P} slots {','.join(hm(r) if P > 60 else ':%02d' % r for r in R)}: window {len(ws)} slots / {len(wd)} real"
      f" ({'ok' if abs(len(ws) - len(wd)) <= 1 else 'FAIL'}); filled within 3: {len(fill)}/{len(ws)}"
      f" ({'ok' if ws and len(fill) >= 0.8 * len(ws) else 'FAIL'}) | day: exact {sum(1 for v, _ in dev if v == 0)}, <=1 {sum(1 for v, _ in dev if v <= 1)}, <=3 {sum(1 for v, _ in dev if v <= 3)} of {len(dev)}, worst {max((v for v, _ in dev), default=0)}")
print('  window slots: ' + ' '.join(hm(s) + ('' if s in fill else '(-)') for s in ws))
off = [(v, d) for v, d in dev if v > 3 and 720 <= d[0] < 1200]
print('  off >3 min 12-20h: ' + (', '.join(f"{hm(d[0])} ({v})" for v, d in off) or 'none'))
