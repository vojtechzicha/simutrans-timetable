"""In-game change list of the 25 Oct 2026 offset-origin fix on the city sheets: per row whose typed values changed, old
(midnight origin: real - 1 at loops) -> new ((real - 60 - 1 at loops) mod every). python -X utf8 city_changes.py > md"""
import glob, json, os, sys
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); PIPE = os.path.dirname(HERE)
sys.path.insert(0, HERE); from city_systemic import rows_of, newest
SHEET = {'praha': 'Prague Tram Peak Fleet', 'praha-trolleybus': 'Prague Trolleybus Peak Fleet', 'brno': 'Brno Tram Fleet from 29 Sep',
         'plzen': 'Plzeň Tram Peak Fleet', 'plzen-trolleybus': 'Plzeň Trolleybus Peak Fleet', 'olomouc-bus': 'Olomouc Bus Peak Fleet',
         'most-litvinov-bus': 'Most-Litvinov Bus Vypravenost', 'pardubice': 'Pardubice MHD Peak Sheet', 'praha-bus': 'Prague Bus Lines Check'}
def extra_rows(p):
    d = newest(p); out = []
    if p == 'praha':
        T = json.load(open(os.path.join(d, 'timetable.json'), encoding='utf-8'))
        for L, m in T.get('metro', {}).items():
            for pt in m['patterns']:
                for s in pt['simutrans']: out.append((f'metro {L}', s['o'], s['d'], s['every'], s.get('real', s['set']), s['set'], False))
    if p == 'praha-bus':
        G = json.load(open(os.path.join(d, 'gtfs_lines.json'), encoding='utf-8'))
        for L, x in G['lines'].items():
            for m in x.get('patterns', []):
                s = m.get('schedule') if isinstance(m, dict) else None
                if s and s.get('every'): out.append((L, m.get('o'), m.get('d'), s['every'], s['real'], s['set'], True))
    if p == 'pardubice':
        N = json.load(open(os.path.join(d, 'network.json'), encoding='utf-8'))
        lp = json.load(open(os.path.join(PIPE, p, 'states', os.path.basename(d) + '.json'), encoding='utf-8')).get('all_termini_are_loops', True)
        for x in (N.get('simutrans', N.get('lines', [])) if isinstance(N, dict) else N):
            for r in (x.get('rows', []) if isinstance(x, dict) else []):
                if r.get('every'): out.append((x.get('id'), r['stop'], r['to'], r['every'], r['real'], r['set'], lp))
    return out
print('# City sheets: in-game changes of the offset-origin fix (25 Oct 2026)\n')
print('The fork counts offsets from 01:00. These sheets typed (real − 1) mod every, which is right only when the interval divides 60.')
print('Only the typed values change; every real minute, vehicle and need stays as it was.\n')
for p, name in SHEET.items():
    rows, _ = rows_of(p) if p not in ('pardubice', 'praha-bus') else ([], None)
    rows = [(L, a, b, P, real, st, lp) for L, a, b, P, real, st, lp, ex in (rows or [])] + extra_rows(p)
    ch = []
    for L, a, b, P, real, st, lp in rows:
        old = [(r - (1 if lp else 0)) % P for r in real]
        if sorted(old) != sorted(st): ch.append((L, a, b, P, old, st))
    if not ch: continue
    print(f'\n## {name} ({len(ch)} entries)\n\n| Line | Entry | Every | Was (Offset, Also at) | Now |\n|---|---|---|---|---|')
    for L, a, b, P, old, st in ch: print(f"| {L} | {a} → {b} | {P} | {', '.join(map(str, old))} | **{', '.join(map(str, st))}** |")
