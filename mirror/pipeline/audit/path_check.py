"""Every timed leg of every regional sheet: does the real trip each window slot stands for run on the leg's modelled path?
For the slot's trip (nearest own trip within 3 min), the stops it serves between where the leg is read and where it leaves
the leg (the terminal, or its own end if it ends before) that are NOT on the modelled stop list, and where it really ends /
starts if that is off the path. Flags a slot when its trip ends or starts off the path, or serves 2+ stops the line skips.
usage: python -X utf8 audit/path_check.py [pipeline dir] (25 Oct 2026, after the 292 split)"""
import json, os, sys, importlib
PIPE = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHEETS = ['odis-regional-hko', 'odis-regional-tfj', 'odis-regional-opavsko', 'odis-regional-novojicinsko', 'odis-regional-bruntalsko']
def hm(t): return '%d:%02d' % (t // 60 % 24, t % 60)
sys.path.insert(0, os.path.join(PIPE, 'odis-regional-hko', 'scripts'))
tot = 0
for sh in SHEETS:
    base = os.path.join(PIPE, sh); os.environ['ODIS_BASE'] = base
    import lib; importlib.reload(lib)
    S = json.load(open(os.path.join(base, 'data', 'derived', 'schedule.json'), encoding='utf-8'))
    T = json.load(open(os.path.join(base, 'data', 'derived', 'trips.json'), encoding='utf-8'))
    byid = {(t['lic'], t['sp']): t for ts in T.values() for t in ts}
    flags = []
    for L, v in S.items():
        if L.startswith('_'): continue
        for ss in v['sim']:
            for g in ss['legs']:
                if g.get('untimed') or not g.get('trips'): continue
                path = list(g['stops']); P = set(path)
                for s_ in g['window']['slots']:
                    near = min(g['trips'], key=lambda tr: abs(tr['d'] - s_))
                    if abs(near['d'] - s_) > 3: continue
                    t = byid.get((near['lic'], near['sp']))
                    if not t: continue
                    st = [lib.AL(lib.nm(x)) for x in t['stops']]
                    # the part of the trip the leg stands for: from the leg's start (fr, or the knot, or the trip's own start)
                    # to the leg's end (to, or the trip's own end)
                    i = next((k for k, x in enumerate(st) if x == g['fr']), None)
                    if i is None: i = next((k for k, x in enumerate(st) if x == g.get('knot_stop')), 0)
                    j = next((k for k in range(i, len(st)) if st[k] == g['to']), len(st) - 1)
                    seg = st[i:j + 1]
                    off = [x for x in seg if x not in P]
                    start_off = g['fr'] not in st and st[0] not in P
                    end_off = g['to'] not in st[i:] and st[-1] not in P
                    if off and (len(off) >= 2 or start_off or end_off):
                        flags.append((L, ss['name'], g['fr'], g['to'], hm(s_), hm(near['d']), lib.nm(t['fr']), lib.nm(t['to']), off, start_off, end_off))
    tot += len(flags)
    print('=' * 8, sh, len(flags), 'slots whose trip leaves the modelled path')
    for f in flags:
        L, nmn, fr, to, s_, d, a, b, off, so, eo = f
        print(f"  {nmn}: {fr.split(', ',1)[-1][:26]} -> {to.split(', ',1)[-1][:26]} slot {s_} = trip {a.split(', ',1)[-1][:24]} -> {b.split(', ',1)[-1][:24]}"
              f"{' [starts off path]' if so else ''}{' [ends off path]' if eo else ''}; off-path stops: {', '.join(x.split(', ',1)[-1] for x in off)}")
print('total', tot)
