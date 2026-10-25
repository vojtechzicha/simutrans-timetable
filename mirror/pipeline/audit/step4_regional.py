"""Step 4 audit of the ODIS regional sheets (bus-schedule-method.md, Step 4), from each sheet's derived/schedule.json:
python -X utf8 step4_regional.py [sheet folder ...] [--md out.md]

Per timed leg, in its Simutrans line's model window: slots vs real departures (must be equal ±1), and slots with a real
departure within 3 min (at least 80 %). Classes:
  EMPTY  a window slot has no real departure within 3 min (fill under 80 %): the pattern is off the timetable
  MORE   more slots than real departures + 1: too dense
  FEWER  fewer slots than real departures - 1: too sparse, unless an outstation line timed at its inbound rate (owner,
         25 Oct 2026: no empty-return lines for frequency); judged by hand
  ok     passes both
A failing leg is then searched (Step 4, this direction alone, its own trips over the day): every interval dividing 1440 up
to 480 with 1-8 slots placed on the window's real departures. FIXABLE = some candidate passes both tests (the sheet missed
it; the best by exact hits over the day is shown); IRREGULAR = none passes (an approximation is the method's answer, rule
4: the simplest even pattern at the real rate, on the To check list). The search ignores the other direction and the bus
count, so a FIXABLE leg still needs a joint design (both ends at the same rate, Step 7).
'auto' marks a leg the builder fitted (at: 'auto'), never checked by hand."""
import collections, itertools, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); PIPE = os.path.dirname(HERE)
SHEETS = ['odis-regional-hko', 'odis-regional-tfj', 'odis-regional-opavsko', 'odis-regional-novojicinsko', 'odis-regional-bruntalsko']
ALLOWED = [d for d in range(10, 481) if 1440 % d == 0]
hm = lambda t: '%d:%02d' % (t // 60 % 24, t % 60)

def search(D, W):
    """best passing (P, slots) for real departures D (minutes, whole day) in window W, else None"""
    wd = [d for d in D if W[0] <= d < W[1]]; day = [d for d in D if 300 <= d < 1380]
    best = None
    for P in ALLOWED:
        res = sorted({d % P for d in wd})
        for k in range(1, 9):
            if k > max(1, len(res)) or k * 5 > P: break
            for R in itertools.combinations(res, k):
                sl = [t for t in range(W[0], W[1]) if t % P in R]
                if not sl or abs(len(sl) - len(wd)) > 1: continue
                if sum(1 for t in sl if any(abs(t - d) <= 3 for d in D)) < 0.8 * len(sl): continue
                cd = lambda d: min(min((d - r) % P, (r - d) % P) for r in R)
                key = (sum(1 for d in day if cd(d) == 0), sum(1 for d in day if cd(d) <= 1), -k, P)
                if best is None or key > best[0]: best = (key, P, R)
    return None if best is None else dict(P=best[1], slots=[hm(r) if best[1] > 60 else ':%02d' % r for r in best[2]], exact=best[0][0])

def audit(sh):
    S = json.load(open(os.path.join(PIPE, sh, 'data', 'derived', 'schedule.json'), encoding='utf-8'))
    cnt = collections.Counter(); rows = []
    for L, x in S.items():
        if L.startswith('_'): continue
        for s in x['sim']:
            W = s.get('window') or [0, 1440]
            for g in s['legs']:
                if g['untimed']: continue
                w = g.get('window') or {}; sl, dp, em = w.get('slots', []), w.get('deps', []), w.get('empty', [])
                fill = len(sl) - len(em)
                c = ('EMPTY' if sl and fill < 0.8 * len(sl) else 'MORE' if len(sl) > len(dp) + 1 else 'FEWER' if len(sl) < len(dp) - 1 else 'ok')
                cnt[c] += 1; cnt['auto' if g.get('auto') else 'hand'] += 1
                if c == 'ok': continue
                best = search(sorted({t['d'] for t in g.get('trips', [])}), W)
                cnt['FIXABLE' if best else 'IRREGULAR'] += 1
                rows.append(dict(L=L, sim=s['name'], P=s['every'], fr=g['fr'], to=g['to'], c=c, auto=bool(g.get('auto')), sl=sl, dp=dp, em=em, best=best))
    return cnt, rows

if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    md = sys.argv[sys.argv.index('--md') + 1] if '--md' in sys.argv else None
    if md in args: args.remove(md)
    out = []; tot = collections.Counter()
    for sh in args or SHEETS:
        cnt, rows = audit(sh); tot.update(cnt)
        n = sum(cnt[k] for k in ('ok', 'EMPTY', 'MORE', 'FEWER'))
        out.append(f"\n## {sh}: {n} timed legs, {cnt['ok']} ok, {cnt['EMPTY']} EMPTY, {cnt['MORE']} MORE, {cnt['FEWER']} FEWER "
                   f"({cnt['auto']} auto, {cnt['hand']} hand); failing: {cnt['FIXABLE']} FIXABLE, {cnt['IRREGULAR']} IRREGULAR\n")
        if rows:
            out.append('| Line | Simutrans line | Every | Entry | Class | Fit | Window slots | Real in window | Passing candidate |\n|---|---|---|---|---|---|---|---|---|')
            for r in rows:
                b = r['best']
                out.append(f"| {r['L']} | {r['sim']} | {r['P']} | {r['fr']} → {r['to'].split(', ')[-1]} | {r['c']} | {'auto' if r['auto'] else 'hand'} | "
                           f"{' '.join(hm(t) + ('(-)' if t in r['em'] else '') for t in r['sl'])} | {' '.join(hm(t) for t in r['dp'])} | "
                           + (f"FIXABLE: every {b['P']} {' '.join(b['slots'])} ({b['exact']} exact over the day)" if b else 'IRREGULAR') + ' |')
    n = sum(tot[k] for k in ('ok', 'EMPTY', 'MORE', 'FEWER'))
    head = (f"# Step 4 audit, ODIS regional sheets\n\nTimed legs: {n}; ok {tot['ok']}, EMPTY {tot['EMPTY']}, MORE {tot['MORE']}, FEWER {tot['FEWER']}; "
            f"failing legs FIXABLE {tot['FIXABLE']}, IRREGULAR {tot['IRREGULAR']}. (-) = window slot without a real departure within 3 min.\n")
    if md: open(md, 'w', encoding='utf-8').write(head + '\n'.join(out) + '\n')
    print(head); [print(l.strip()) for l in out if l.startswith('\n##')]
