"""Rule checks on the city sheets' Simutrans rows (fork-schedule rules; the 18-20 Oct 2026 fixes made on the Ostrava sheets):
python -X utf8 city_systemic.py [--md out.md]

Per row (one terminus entry): interval P, slots `real` (clock minutes mod P from midnight) and typed `set`.
  ORIGIN  typed values are not (real - 60 - 1 at loops) mod P: the fork counts offsets from 01:00 (owner, 3 Oct; fixed on the
          Ostrava sheets 20 Oct). Only intervals not dividing 60 can differ; the error is (60 mod P) minutes.
  RANGE   a typed value outside 0..P-1, not a whole minute, or more than 8 slots (Offset + 7 Also at)
  FOLD    two or more evenly spaced slots not written as the plain interval ("every 60, Offset 17, Also at 47" is every 30)
  RATE    the two directions of one terminus pair have different departures per hour (both ends at the same rate)
Approximate rows (exact = false) are counted, not judged here."""
import collections, glob, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); PIPE = os.path.dirname(HERE)

def newest(p):
    ds = sorted(d for d in glob.glob(os.path.join(PIPE, p, 'data', 'derived', '*')) if os.path.isdir(d))
    return ds[-1] if ds else None

def rows_of(p):
    """[(line, from, to, P, real, set, loop, exact)] for one pipeline, whatever its format"""
    out = []
    if os.path.exists(os.path.join(PIPE, p, 'data', 'derived', 'schedule.json')):          # Ostrava lib family
        cfg = json.load(open(os.path.join(PIPE, p, 'config.json'), encoding='utf-8'))
        lp = cfg.get('all_termini_are_loops', False)
        S = json.load(open(os.path.join(PIPE, p, 'data', 'derived', 'schedule.json'), encoding='utf-8'))
        for L, rs in S.items():
            if L.startswith('_') or not isinstance(rs, list): continue
            for r in rs:
                if r.get('every'): out.append((L, r['fr'], r['to'], r['every'], r['real'], r['set'], lp, 'approx' not in r))
        od = os.path.join(PIPE, p, 'data', 'derived', 'odis.json')                     # Ostrava bus: Hranečník ODIS cards
        if os.path.exists(od):
            for L, rs in json.load(open(od, encoding='utf-8'))['schedule'].items():
                for r in rs:
                    if r.get('every'): out.append((L, r['fr'], r['to'], r['every'], r['real'], r['set'], lp, 'approx' not in r))
        return out, 'derived/schedule.json'
    d = newest(p)
    if not d or not os.path.exists(os.path.join(d, 'timetable.json')): return None, None
    T = json.load(open(os.path.join(d, 'timetable.json'), encoding='utf-8'))
    if isinstance(T, dict) and 'lines' in T:                                                  # Prague family
        for L, x in T['lines'].items():
            for r in x.get('schedule', []):
                if r.get('every'): out.append((L, r['o'], r['d'], r['every'], r['real'], r['set'], r.get('loop', False), r.get('exact', True)))
    else:                                                                                     # Brno / Plzeň / Olomouc family
        for x in (T if isinstance(T, list) else T.get('schedule', [])):
            for r in x.get('rows', []):
                if r.get('every'): out.append((x['id'], r['stop'], r['to'], r['every'], r['real'], r['set'], r.get('loop', False), r.get('exact', True)))
    return out, os.path.relpath(os.path.join(d, 'timetable.json'), os.path.join(PIPE, p))

def check(rows):
    bad = collections.defaultdict(list)
    for L, a, b, P, real, st, lp, ex in rows:
        exp = sorted((r - 60 - (1 if lp else 0)) % P for r in real)
        if sorted(st) != exp: bad['ORIGIN'].append((L, a, b, P, real, st, exp))
        if len(st) > 8 or any((not isinstance(v, int)) or v < 0 or v >= P for v in st): bad['RANGE'].append((L, a, b, P, real, st, None))
        rs = sorted(real)
        if len(rs) >= 2 and P % len(rs) == 0 and all((rs[(i + 1) % len(rs)] - rs[i]) % P == P // len(rs) for i in range(len(rs))):
            bad['FOLD'].append((L, a, b, P, real, st, f'every {P // len(rs)}'))
    by = collections.defaultdict(dict)
    for L, a, b, P, real, st, lp, ex in rows: by[(L, frozenset((a, b)))][(a, b)] = len(real) * 60 / P
    for (L, pair), d in by.items():
        if len(d) == 2 and abs(list(d.values())[0] - list(d.values())[1]) > 1e-9:
            (a, b), (c, e) = list(d)
            bad['RATE'].append((L, a, b, None, None, None, f"{d[(a, b)]:.2f} vs {d[(c, e)]:.2f} an hour"))
    return bad

if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    md = sys.argv[sys.argv.index('--md') + 1] if '--md' in sys.argv else None
    P_ = ['praha', 'praha-trolleybus', 'brno', 'brno-bus', 'brno-trolleybus', 'plzen', 'plzen-bus', 'plzen-trolleybus', 'olomouc',
          'olomouc-bus', 'most-litvinov', 'most-litvinov-bus', 'ostrava', 'ostrava-trolleybus', 'ostrava-bus', 'havirov-karvina-orlova']
    lines = ['# City sheets: rule checks\n', __doc__.split('\n', 2)[2], '| Pipeline | Source | Rows | Approximate | ORIGIN | RANGE | FOLD | RATE |', '|---|---|---|---|---|---|---|---|']
    detail = []
    for p in P_:
        rows, src = rows_of(p)
        if rows is None: lines.append(f'| {p} | no timetable found | | | | | | |'); continue
        bad = check(rows)
        lines.append(f"| {p} | {src} | {len(rows)} | {sum(1 for r in rows if not r[7])} | {len(bad['ORIGIN'])} | {len(bad['RANGE'])} | {len(bad['FOLD'])} | {len(bad['RATE'])} |")
        for k in ('ORIGIN', 'RANGE', 'FOLD', 'RATE'):
            for L, a, b, P, real, st, x in bad[k]:
                detail.append(f"| {p} | {k} | {L} | {a} → {b} | {P or ''} | {real if real is not None else ''} | {st if st is not None else ''} | {x if x is not None else ''} |")
    txt = '\n'.join(lines) + '\n\n## Rows\n\n| Pipeline | Check | Line | Entry | Every | Real | Typed | Expected / note |\n|---|---|---|---|---|---|---|---|\n' + '\n'.join(detail) + '\n'
    if md: open(md, 'w', encoding='utf-8').write(txt)
    print('\n'.join(lines))
