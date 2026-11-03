"""Passing check: real afternoon trips (13:00-19:00) that no modelled slot of their line passes, read at every stop they pass.
A trip counts as on the pattern for the stops of a slot it meets within 3 min somewhere on the slot's leg (same direction);
the rest of its stops are off the pattern. Flags each line where >= 3 such trips pass one stop each way (EACH WAY: the
afternoon-branch rule, 20/30 Oct 2026) or >= 3 one way (ONE WAY: buses going out or home; the card must say which). Read at
the stops the trips pass, not by where they start or end: the 381 Zásmuky branch (3 Nov 2026) was filed as garage buses
because its trips towards Prague start at Kutná Hora, hlavní nádraží and pass Zásmuky.
usage: python -X utf8 audit/passing_check.py [pipeline dir] [line ...]   (sheets: AUDIT_SHEETS=a,b, folders under the pipeline dir)"""
import json, os, sys, statistics
from collections import defaultdict
PIPE = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ONLY = set(sys.argv[2:])
SHEETS = os.environ.get('AUDIT_SHEETS', '').split(',') if os.environ.get('AUDIT_SHEETS') else \
    [f'pid-regional/oblasti/{x}' for x in sorted(os.listdir(os.path.join(PIPE, 'pid-regional', 'oblasti')))]
W0, W1 = 780, 1140
def hm(m): return '%d:%02d' % (m // 60 % 24, m % 60)

for sh in SHEETS:
    der = os.path.join(PIPE, sh, 'data', 'derived')
    if not os.path.exists(os.path.join(der, 'schedule.json')): continue
    S = json.load(open(os.path.join(der, 'schedule.json'), encoding='utf-8')); S.pop('_coverage', None)
    T = json.load(open(os.path.join(der, 'trips.json'), encoding='utf-8'))
    legs_for = defaultdict(list)
    for L, v in S.items():
        for sm in v.get('sim', []):
            for g in sm['legs']:
                for l in g.get('lines') or [L]: legs_for[l].append((sm['name'], g))
    rows = []
    for L in S:
        if ONLY and L not in ONLY: continue
        trips = T.get(L, [])
        if not trips: continue
        R = max(trips, key=lambda t: len(t['stops']))['stops']; Ri = {s: i for i, s in enumerate(R)}
        def orient(st):
            com = [s for s in st if s in Ri]
            return 0 if len(com) < 2 else (1 if Ri[com[-1]] > Ri[com[0]] else -1)
        # every slot of every leg carrying L, with its time at each stop of the leg (offset = median of the trips on a slot)
        slots = []
        for name, g in legs_for.get(L, []):
            st = g['stops']; P = g['every']; cand = [t for l in set(g.get('lines') or [L]) for t in T.get(l, [])]
            base = [r % P for r in g['real']]
            def onslot(x): return any(min((x - b) % P, (b - x) % P) <= 3 for b in base)
            offs = {}
            for i, s in enumerate(st):
                d1, d2 = [], []
                for t in cand:
                    # a loop passes its terminal twice: time fr at its first passing, s at the first passing after it
                    ts, tm = t['stops'], t['times']
                    if g['fr'] in ts:
                        a = ts.index(g['fr']); b = next((j for j in range(a + (1 if i else 0), len(ts)) if ts[j] == s), None)
                        if b is not None:
                            (d1 if onslot(tm[a]) else d2).append(tm[b] - tm[a]); continue
                    # a leg read at a knot: only trips that pass the knot and s in the leg's own order (same direction)
                    if g.get('knot_stop') and g['knot_stop'] in ts and s in ts and g['knot_stop'] in st:
                        a = ts.index(g['knot_stop']); b = ts.index(s); ka = st.index(g['knot_stop'])
                        if (b - a) * (i - ka) < 0 or (b == a) != (i == ka): continue
                        (d1 if onslot(tm[a] - g['kr']) else d2).append(g['kr'] + tm[b] - tm[a])
                ds = d1 or d2
                offs[s] = statistics.median(ds) if ds else g['rt'] * i / max(1, len(st) - 1)
            o = orient(st)
            for b in base:
                m = b
                while m < 1440 + 300:
                    slots.append((set(st), {s: m + offs[s] for s in st}, o, {(st[0], m)})); m += P
        unm = defaultdict(lambda: defaultdict(set)); info = {}
        for k, t in enumerate(trips):
            o = orient(t['stops']); info[k] = (t['dep'], t['fr'], t['to'], o)
            covered = set()
            for sset, mt, so, _ in slots:
                if so and o and so != o: continue
                if any(s in mt and abs(mt[s] - x) <= 3 for s, x in zip(t['stops'], t['times'])): covered |= sset
            for s, tm in zip(t['stops'], t['times']):
                if W0 <= tm < W1 and s not in covered: unm[s][o].add(k)
        each = max(((min(len(d.get(1, ())), len(d.get(-1, ()))), s) for s, d in unm.items()), default=(0, None))
        one = max(((len(v), s) for s, d in unm.items() for o, v in d.items() if o), default=(0, None))
        if each[0] < 3 and one[0] < 3: continue
        at = each[1] if each[0] >= 3 else one[1]
        ks = sorted(set().union(*unm[at].values()), key=lambda k: info[k][0])
        rows.append((each[0], one[0], L, at, sorted({n for n, _ in legs_for.get(L, [])}),
                     [f"{'→' if info[k][3] > 0 else '←' if info[k][3] < 0 else '·'} {hm(info[k][0])} {info[k][1]} → {info[k][2]}" for k in ks]))
    print(f'======== {sh}: {sum(1 for r in rows if r[0] >= 3)} lines EACH WAY, {sum(1 for r in rows if r[0] < 3)} ONE WAY')
    for e, o, L, at, sims, ts in sorted(rows, key=lambda r: (-r[0], -r[1], r[2])):
        print(f"[{'EACH WAY' if e >= 3 else 'ONE WAY'}] {L} ({', '.join(sims)}): {e} each way, {o} one way at {at}; off the pattern there:")
        for x in ts: print('      ' + x)
