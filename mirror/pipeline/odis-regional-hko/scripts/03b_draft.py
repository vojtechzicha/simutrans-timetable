"""A first draft of config.lines for lines that have none yet (bus schedule method Steps 2-5, 8), to be checked by hand.

For each line: the main terminal pair (the two ends with the most trips passing both), the trips read at each end over
the whole day, the anchor (line_anchor), and the simplest repeating pattern at the rate of the model window: candidate
intervals 10-480, the slot count the window's real departures call for, slots on the minutes most real departures hit
exactly (then within 1, then 3). A line with one trip a direction in each 8-hour shift block is drafted every 480 at its
afternoon trip. Lines with fewer than 3 trips each way 13:00-19:00 are marked sparse (Step 8: model only for a stop no other
line serves). The draft goes to derived/draft.json and is printed; nothing is written to config.json.
"""
import collections, itertools, json
from lib import CONFIG, load, save, nm, AL, hm, line_anchor

T = load('trips.json'); C = load('line_class.json')
ALLOWED = [10, 12, 15, 20, 30, 60, 90, 120, 180, 240, 480]
def cd(a, b, P): return min((a - b) % P, (b - a) % P)

def ends_pair(tr):
    ends = collections.Counter()
    for t in tr: ends[AL(nm(t['fr']))] += 1; ends[AL(nm(t['to']))] += 1
    best = None
    for a, b in itertools.combinations([e for e, _ in ends.most_common(8)], 2):
        n = sum(1 for t in tr for st in [[AL(nm(x)) for x in t['stops']]] if a in st and b in st)
        if best is None or n > best[0]: best = (n, a, b)
    loops = [t for t in tr if AL(nm(t['fr'])) == AL(nm(t['to']))]
    if len(loops) > len(tr) / 2:
        a = collections.Counter(AL(nm(t['fr'])) for t in loops).most_common(1)[0][0]; return a, a
    return (best[1], best[2]) if best else (None, None)

def times(tr, a, b):
    out = []
    for t in tr:
        st = [AL(nm(x)) for x in t['stops']]
        if a == b:
            if st[0] == a: out.append(t['times'][0])
            continue
        if a in st and b in st[st.index(a) + 1:]: out.append(t['times'][st.index(a)])
    return sorted(out)

def pick(D, P, k):
    """k residues mod P on the minutes most real departures hit exactly, then within 1 and 3, at least 4 min apart"""
    cand = sorted({d % P for d in D})
    def score(R): return (sum(1 for d in D if min(cd(d, r, P) for r in R) == 0), sum(1 for d in D if min(cd(d, r, P) for r in R) <= 1),
                          sum(1 for d in D if min(cd(d, r, P) for r in R) <= 3))
    R = []
    for _ in range(k):
        best = max((c for c in cand if all(cd(c, r, P) >= 4 for r in R)), key=lambda c: score(R + [c]), default=None)
        if best is None: break
        R.append(best)
    return sorted(R), score(R)

out = {}
for L in sorted(T, key=int):
    if L in CONFIG.get('lines', {}) or L in CONFIG.get('unmodelled', {}): continue
    tr = T[L]; a, b = ends_pair(tr)
    if a is None: continue
    an = line_anchor(tr, dict(peak_minute=960)); W = (an['anchor'] - 30, an['anchor'] + 90)
    DA = [d for d in times(tr, a, b) if 300 <= d < 1380]; DB = [d for d in times(tr, b, a) if 300 <= d < 1380] if a != b else []
    aft = (sum(1 for d in DA if 780 <= d < 1140), sum(1 for d in DB if 780 <= d < 1140))
    wn = [sum(1 for d in D if W[0] <= d < W[1]) for D in (DA, DB) if D]
    rate = max(1, round(sum(wn) / len(wn))) if wn else 1          # departures in the 2-h window
    sparse = min(aft) < 3 if a != b else aft[0] < 3
    shift = lambda D: sum(1 for x in D for y in D if 470 <= y - x <= 490) >= 1 and len(D) <= 6
    # the interval nearest the afternoon's average headway (divisors of 60 preferred), one slot each way on the minute the
    # afternoon's real departures hit most (then within 3 min, then the whole day); a line with one or two trips in the
    # afternoon whose trips repeat 8 h apart is a shift line, every 480 at its afternoon trip
    n13 = [sum(1 for d in D if 780 <= d < 1080) for D in (DA, DB) if D]
    h = 300 / max(0.5, sum(n13) / len(n13)) if n13 else 480
    P = min(ALLOWED, key=lambda x: abs(__import__('math').log(x / h)) - (0.2 if 60 % x == 0 else 0))
    if all(shift(D) for D in (DA, DB) if D) and max(n13 or [0]) <= 2: P = 480
    Rs = []; sc = []
    for D in (DA, DB):
        if not D: continue
        A_ = [d for d in D if 780 <= d < 1140] or D
        R = max(range(P), key=lambda r: (sum(1 for d in A_ if cd(d, r, P) == 0), sum(1 for d in A_ if cd(d, r, P) <= 3),
                                          sum(1 for d in D if cd(d, r, P) == 0), -r))
        Rs.append([R]); _, s_ = pick(D, P, 1)
        ws = [t for t in range(W[0], W[1]) if t % P == R]
        fill = sum(1 for t in ws if any(abs(t - d) <= 3 for d in D)) / len(ws) if ws else 0
        sc.append(((sum(1 for d in D if cd(d, R, P) == 0), sum(1 for d in D if cd(d, R, P) <= 1), sum(1 for d in D if cd(d, R, P) <= 3)), fill, len(ws)))
    if not Rs: print(f"{L:4} no trip runs between {a} and {b} in 5:00-23:00; draft by hand"); continue
    best = (None, P, Rs, sc)
    _, P, Rs, sc = best
    def fmt(R): return [(':%02d' % r if 60 % P == 0 else hm(r)) for r in R]
    legs = ([dict(fr=a, to=a, at=[hm(Rs[0][0]) if P > 60 else Rs[0][0]])] if a == b else
            [dict(fr=a, to=b, at=[hm(Rs[0][0]) if P > 60 else Rs[0][0]]), dict(fr=b, to=a, at=[hm(Rs[1][0]) if P > 60 else Rs[1][0]])] if len(Rs) == 2 else
            [dict(fr=a, to=b, at=[hm(Rs[0][0]) if P > 60 else Rs[0][0]]), dict(fr=b, to=a, untimed=True)])
    out[L] = dict(spec=dict(core=[a] if a == b else [a, b], sim=[dict(name=L, every=P, legs=legs)]), a=a, b=b, P=P, R=Rs, anchor=hm(an['anchor']), rate=rate, aft=aft, sparse=sparse,
                  stats=[dict(exact=s[0][0], w1=s[0][1], w3=s[0][2], fill=round(s[1], 2)) for s in sc], n=(len(DA), len(DB)))
    print(f"{L:4} {C[L]['name'][:38]:38} {a.split(', ')[-1][:16]:16}{'↺' if a == b else '↔ ' + b.split(', ')[-1][:16]:18} "
          f"anchor {hm(an['anchor'])} rate {rate}/2h aft {aft} -> every {P} {[fmt(R) for R in Rs]} "
          + ' '.join(f"[{s['exact']}/{s['w3']}/{n} fill {s['fill']}]" for s, n in zip(out[L]['stats'], out[L]['n'])) + (' SPARSE' if sparse else ''))
save('draft.json', out)
