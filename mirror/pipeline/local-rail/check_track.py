"""Where do a sheet's game trains meet each other on the track?  (method check, 25 Oct 2026)
Run from the working folder:  python -X utf8 pipeline/local-rail/check_track.py build_s5 [works]

Every line of the sheet is laid out as the game runs it: each leg repeated at the line's interval (departures
12:00 - 21:00), on the real minutes of the real train behind the leg, at all its raw CIS locations (passing points
too). For every pair of trains going opposite ways over shared locations it finds where they meet:
- at a station (both there at once): flagged only if no real workday trains from opposite sides are ever there at
  the same time (one may pass while the other stands), or it is a request-stop halt, and no real train meets
  another on the open line next to it (that would show double track);
- on the open line between two consecutive shared locations: flagged unless real workday trains also meet on open
  line on that segment (evidence of double track).
So a flag means "the game pattern makes two trains meet where the real timetable never does": on single track that
is a conflict (S75 Os 7717 x Os 7718 between Chlum u Rakovníka and Rakovník; S40 Os 9712 x Os 9735 between
Kralupy and Kralupy předměstí; both fixed 25 Oct 2026). Check each flag by hand with check_meetings.py.
Known limitation: two trains that take different routes between the same two locations (R49 via Praha-Malešice
and via Praha hl. n. between Praha-Hostivař and Rokytka odbočka) are taken for one segment (false flag).
'works': use each 'temporary' line instead of the line it replaces (same_vehicles_as); buses are left out.
Depot legs without raw locations are left out.
"""
import importlib
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
mod = importlib.import_module(sys.argv[1])
import build_012_014_235 as base  # noqa: E402

works = 'works' in sys.argv[2:]
by_num, wd = base.load()
defs = mod.LINES
if works:
    repl = {L['same_vehicles_as']: L for L in defs if L.get('same_vehicles_as')}
    defs = [repl.get(L['name'], L) for L in defs if not L.get('temporary') or L.get('same_vehicles_as')]
    defs = [L for L in defs if L.get('cat') != 'bus']
    seen = set()
    defs = [L for L in defs if not (L['id'] in seen or seen.add(L['id']))]
    # drop the normal lines that have a works version
    defs = [L for L in defs if L['name'] not in repl]
else:
    defs = [L for L in defs if not L.get('temporary')]
lines = [base.build_line(L, by_num, wd) for L in defs]


def hm(m):
    return f'{int(m) // 60 % 24}:{int(m) % 60:02d}' + ('½' if m % 1 else '')


def leg_locs(leg):
    """the raw locations of a leg between its first and last stop, as [(code, name, arr, dep)]"""
    st = leg['stops']
    raw = leg.get('raw') or []
    if not raw:
        return [(s_['name'], s_['name'], s_['arr'] if s_['arr'] is not None else s_['dep'],
                 s_['dep'] if s_['dep'] is not None else s_['arr']) for s_ in st]
    t0, t1 = st[0]['dep'], st[-1]['arr']
    n0, n1 = st[0]['name'], st[-1]['name']
    out = []
    started = False
    for l in raw:
        nm = base.full(l['name'])
        a, d = l.get('arr'), l.get('dep')
        a = a if a is not None else d
        d = d if d is not None else a
        if a is None:
            continue
        if not started:
            if nm == n0 and d is not None and abs(d - t0) < 0.01 or nm == n0 and d is not None and d >= t0 - 0.01 and not out:
                started = True
                out.append((l['code'], nm, t0, t0))
            continue
        if nm == n1 and a is not None and a >= t1 - 0.01:
            out.append((l['code'], nm, t1, t1))
            break
        out.append((l['code'], nm, a, d))
    # works copies: the extra stops' departures
    stopdep = {s_['name']: (s_['arr'], s_['dep']) for s_ in st}
    res = []
    for c, nm, a, d in out:
        if nm in stopdep and stopdep[nm][1] is not None and stopdep[nm][0] is not None:
            a, d = stopdep[nm]
        res.append((c, nm, a, d))
    return res


runs = []  # (line name, leg num, [(code, name, arr, dep)])
for x in lines:
    L = x['L']
    iv = L['every']
    also = L.get('also', [])
    for k, leg in enumerate(x['legs']):
        if leg.get('depot'):
            continue
        locs = leg_locs(leg)
        if len(locs) < 2:
            continue
        sh = x['shifts'][k]
        base_dep = locs[0][3] + sh
        for a_ in [0] + also:
            for j in range(-12, 13):
                off = sh + a_ + j * iv
                dep = locs[0][3] + off
                if 12 * 60 <= dep < 21 * 60:
                    runs.append((L['name'], leg['num'], [(c, n, a + off, d + off) for c, n, a, d in locs]))
print(f'{len(runs)} game runs 12:00 - 21:00 on {len(lines)} lines' + (' (works state)' if works else ''))

# real evidence: workday trains by location code
T = json.load(open(base.TRAINS, encoding='utf-8'))
real = []
for t in T:
    if not base.runs(t, base.WEEK[2]):
        continue
    locs = []
    for l in t['locs']:
        a, d = l.get('arr'), l.get('dep')
        a = a if a is not None else d
        d = d if d is not None else a
        if a is None:
            continue
        locs.append((l['code'], l['name'], a, d, bool(base.PA & set(l['act'])), '0030' in l['act']))
    real.append(locs)
by_code = {}
for i, locs in enumerate(real):
    for j, l in enumerate(locs):
        by_code.setdefault(l[0], []).append((i, j))
halt = {}  # code -> request-stop halt (all stops there are request stops)
for locs in real:
    for l in locs:
        if l[4]:
            halt.setdefault(l[0], set()).add(l[5])


def real_open_meeting(ca, cb):
    """do real workday trains ever meet on open line between consecutive locations ca and cb?"""
    segs = {+1: [], -1: []}
    for i, j in by_code.get(ca, []):
        locs = real[i]
        if j + 1 < len(locs) and locs[j + 1][0] == cb:
            segs[+1].append((locs[j][3], locs[j + 1][2]))
        if j > 0 and locs[j - 1][0] == cb:
            segs[-1].append((locs[j - 1][3], locs[j][2]))
    for a0, a1 in segs[+1]:
        for b0, b1 in segs[-1]:
            if max(a0, b0) < min(a1, b1) - 0.01:
                return True
    return False


def real_station_meeting(c):
    """do two real trains from opposite sides ever stand / pass at location c at the same time (one may pass
    while the other stands)?"""
    iv_ = []
    for i, j in by_code.get(c, []):
        locs = real[i]
        l = locs[j]
        pv = locs[j - 1][0] if j > 0 else None
        nx = locs[j + 1][0] if j + 1 < len(locs) else None
        iv_.append((l[2], l[3], pv, nx))
    for x in iv_:
        for y in iv_:
            if x is y or x[2] is None or x[2] != y[3]:
                continue
            if max(x[0], y[0]) <= min(x[1], y[1]) and (x[1] - x[0] > 0.01 or y[1] - y[0] > 0.01):
                return True
    return False


cache = {}
flags = []
for p in range(len(runs)):
    for q in range(p + 1, len(runs)):
        A, B = runs[p], runs[q]
        ia = {c: k for k, (c, *_r) in enumerate(A[2])}
        common = [(k, ia[c]) for k, (c, *_r) in enumerate(B[2]) if c in ia]
        if len(common) < 2:
            continue
        # opposite direction on the common part: B's order reversed in A
        if common[0][1] < common[-1][1]:
            continue  # same direction
        # walk along A's order
        pts = sorted((ka, kb) for kb, ka in common)
        prev = None
        for ka, kb in pts:
            ca, na, aa, da = A[2][ka]
            _, _, ab, db = B[2][kb]
            if max(aa, ab) < min(da, db) + 0.01 and min(da, db) - max(aa, ab) >= -0.01:
                if max(aa, ab) <= min(da, db):
                    key = ('st', ca)
                    if key not in cache:
                        cache[key] = real_station_meeting(ca)
                    req = halt.get(ca) == {True}
                    dbl = False
                    for kk in (ka - 1, ka + 1):
                        if 0 <= kk < len(A[2]):
                            sk = ('seg',) + tuple(sorted((A[2][kk][0], ca)))
                            if sk not in cache:
                                cache[sk] = real_open_meeting(A[2][kk][0], ca) or real_open_meeting(ca, A[2][kk][0])
                            dbl = dbl or cache[sk]
                    if not dbl and (req or not cache[key]):
                        flags.append((hm(max(aa, ab)), f'STATION {na}', A[0], A[1], B[0], B[1],
                                      'request-stop halt' if req else 'no real train ever stands there with another'))
                    prev = None
                    break
            # A at ka is before B gets there?  sign of who is first
            s = aa - db  # A arrives after B left? (B already passed) -> they met before ka
            if prev is not None and (prev[2] < 0) != (s < 0):
                kp = prev[0]
                cpa, npa = A[2][kp][0], A[2][kp][1]
                key = ('seg', cpa, ca)
                if key not in cache:
                    cache[key] = real_open_meeting(cpa, ca)
                if not cache[key]:
                    flags.append((hm(A[2][kp][3]), f'OPEN LINE {npa} – {na}', A[0], A[1], B[0], B[1], 'no real open-line meeting there'))
                break
            prev = (ka, kb, s)
seen = set()
for f in sorted(flags, key=lambda f: (f[1], f[0])):
    k = (f[1], f[2], f[4])
    if k in seen:
        continue
    seen.add(k)
    print(f'{f[0]:>6}  {f[1]:60} {f[2]} ({f[3]}) x {f[4]} ({f[5]})  [{f[6]}]')
print(f'{len(flags)} flagged meetings ({len(seen)} distinct place / line pairs)')
