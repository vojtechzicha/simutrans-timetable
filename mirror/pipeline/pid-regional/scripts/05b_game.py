"""The save game's regional PID lines against this sheet: python 05b_game.py <oblast id>
-> oblasti/<id>/data/derived/game.json, per PID line: its game lines (the export of FORK-CZR-VZ.sve of 30 Oct 2026, lines
named 100300..100999, read by the engine session), each with its buses, state and stops, and
  missing = stops of the line's modelled Simutrans lines that the game line does not serve,
  extra   = game stops the real line does not serve on the day (none of its trips),
  fixes   = game halts matched only by a misspelling or abbreviation (praha-bus 03_compare's rules: every " / " part of a
            halt name, "[stand]" and "Praha, " dropped, abbreviated tokens as prefixes, else similarity >= 0.85).
A PID line with no game line, or a Simutrans line (a variant) that no game line runs, is "a line to build".
The game's lines and buses are shown as a check, not rebased on: the sheet is built from the real timetable and buses
(as the Prague bus sheet), and the in-game change list says what to change.
"""
import importlib.util, json, os, re, sys
from common import HOME, DER, PIPE

OID = sys.argv[1]; BASE = os.path.join(HOME, 'oblasti', OID); D = os.path.join(BASE, 'data', 'derived')
SH = json.load(open(os.path.join(HOME, 'config.json'), encoding='utf-8'))
# praha-bus 03_compare imports its own `common`: load it with that module in place, then put ours back
_own = sys.modules.pop('common'); sys.path.insert(0, os.path.join(PIPE, 'praha-bus', 'scripts'))
spec = importlib.util.spec_from_file_location('pbcompare', os.path.join(PIPE, 'praha-bus', 'scripts', '03_compare.py'))
cmp_ = importlib.util.module_from_spec(spec); spec.loader.exec_module(cmp_)
sys.path.pop(0); sys.modules['common'] = _own
G = json.load(open(os.path.join(PIPE, SH['game_regional']), encoding='utf-8'))
T = json.load(open(os.path.join(D, 'trips.json'), encoding='utf-8'))
S = json.load(open(os.path.join(D, 'schedule.json'), encoding='utf-8'))
C = json.load(open(os.path.join(D, 'line_class.json'), encoding='utf-8'))

def key(n):
    """our stop name in the compare form: no okres tag, no 'Praha, ', ', ' -> ','"""
    n = re.sub(r'\s*\[[^\]]*\]', '', n); n = re.sub(r'^Praha,\s*', '', n)
    return re.sub(r',\s+', ',', n).strip()

byL = {}
for gl in G['lines']:
    m = re.match(r'100(\d{3})', gl['name'])
    if m: byL.setdefault(str(int(m.group(1))), []).append(gl)
out = {}
for L, c in C.items():
    lab = c.get('label', L); num = lab if lab.isdigit() else None
    gls = byL.get(num, []) if num else []
    day = {key(x): x for t in T.get(L, []) for x in t['stops']}
    model = {key(x): x for s in S.get(L, {}).get('sim', []) for g in s['legs'] for x in g['stops']}
    rows = []
    for gl in gls:
        halts = [e['halt_name'] for e in gl['entries'] if e.get('halt_name') and not e.get('is_depot')]
        matched, extra, fixes = set(), [], {}
        for h in dict.fromkeys(halts):
            hit = None
            for cnd in cmp_.cands(h):
                if cnd in day: hit = cnd; break
            if not hit:
                for cnd in cmp_.cands(h):
                    f = cmp_.fuzzy(cnd, list(day))
                    if f: hit = f; fixes[h] = day[f]; break
            if hit: matched.add(hit)
            else: extra.append(h)
        missing = [model[k] for k in model if k not in matched and not model[k].startswith('Praha, ')]
        rows.append(dict(name=gl['name'], convoys=gl['convoy_count'], vehicles=gl['vehicle_count'], state=gl['state'],
                         stops=len(set(halts)), missing=missing, extra=extra, fixes=fixes,
                         timetabled=any(e.get('departure_interval_min') for e in gl['entries'])))
    out[L] = dict(game=rows, build=not rows and L in S)
json.dump(out, open(os.path.join(D, 'game.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(OID, 'game lines', sum(len(v['game']) for v in out.values()), '| PID lines with no game line among the modelled:',
      [C[L].get('label', L) for L, v in out.items() if v['build']])
