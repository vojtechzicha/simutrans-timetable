"""Rebase on the published roster (config.keep_roster): the trams the owner has built in the game stay where they are;
only units that the corrected history no longer supports are replaced (user, 18 Oct 2026: fewest moves).

A unit is replaced when its type has less than config.coverage_min_share of the line's weekday records once the 9xx
evening courses are left out (history.exclude_course_prefixes). Coupled Vario pairs on the 2×T lines 1 and 2 are kept:
coupled pairs run there by day. The replacement is the best free active car of the line's regular type that is most
short of its share, on the same Simutrans line (branch). Spares are recomputed against the final counted set.
Writes derived/roster.json (replaces the fresh 04 roster) with a 'rebase' list of the swaps."""
import collections, json, os, re
from lib import CONFIG, RAW, ROOT, load, save, record_date

C = CONFIG
if not C.get('keep_roster'):
    print('no keep_roster, nothing to rebase'); raise SystemExit
fresh = load('roster.json')
P = json.load(open(os.path.join(ROOT, C['keep_roster']), encoding='utf-8'))
fleet = {int(k): v for k, v in load('fleet.json').items()}
recs = load('records.json')['records']
live = {int(k): v for k, v in load('live.json')['cars'].items()}
TWO = set(C['two_t_lines']); MIN = C['coverage_min_share']

def norm(t, L):
    if t.replace('2×', '') in C['types_not_planned']: t = ('2×' if t.startswith('2×') else '') + 'Vario LF'
    if L in TWO and t == 'Vario LF': t = '2×Vario LF'
    return t
def shares(L):
    c = collections.Counter()
    for l, t, nums, w, k, no in recs:
        if l == L: c[norm(t, l)] += w
    tot = sum(c.values()); return {t: v / tot for t, v in c.items()}
aff = collections.defaultdict(collections.Counter)
for l, t, nums, w, k, no in recs:
    for n in nums: aff[n][l] += w
def cat(n): return fleet[n]['cat']
def available(n): return n in fleet and (n in live or fleet[n]['state'] == 'zar') and cat(n) not in ('?',) + tuple(C['types_not_planned'])
HOME = fresh['home']
def score(n, L):
    s = aff[n][L] + (15 if fleet[n]['depot'] == HOME.get(L) else 0)
    s += 40 if L in live.get(n, {}) else (8 if n in live else 0)
    return s + 0.05 * sum(aff[n].values())

roster = {L: [list(u) for u in us] for L, us in P['roster'].items()}
# the published branches carry the needs; a new timetable that changes a need must be handled by hand (add or drop units)
for L_, brs in fresh['branches'].items():
    for i_, b_ in enumerate(brs):
        pb = P['branches'].get(L_, [])
        if i_ >= len(pb) or pb[i_]['need'] != b_['need']:
            print('WARNING need changed', L_, i_, pb[i_]['need'] if i_ < len(pb) else None, '->', b_['need'])
surplus = {L: [list(u) for u in us] for L, us in P.get('surplus', {}).items()}
used = {n for d in (roster, surplus) for us in d.values() for u in us for n in u[1]}
log = []
for L in sorted(roster, key=int):
    sh = shares(L); N = len(roster[L])
    for i, u in enumerate(roster[L]):
        t = u[0]
        if sh.get(t, 0) >= MIN or (L in TWO and t == '2×Vario LF'): continue
        have = collections.Counter(x[0] for x in roster[L])
        for nt, s_ in sorted(sh.items(), key=lambda x: -(x[1] * N - have[x[0]])):
            if s_ < MIN or nt == t: continue
            base = nt.replace('2×', '')
            cand = sorted([n for n in fleet if available(n) and cat(n) == base and n not in used], key=lambda n: -score(n, L))
            if nt.startswith('2×'):
                y = next((m for m in cand[1:] if cand and fleet[m]['depot'] == fleet[cand[0]]['depot']), None)
                nums = [cand[0], y] if cand and y else None
            else: nums = [cand[0]] if cand else None
            if not nums: continue
            why = (f"{'+'.join(map(str, u[1]))} ({t}) replaced: {t} is {sh.get(t, 0):.1%} of line {L}'s weekday day-course records "
                   f"(9xx evening runs left out); {nt} is {s_:.0%}")
            log.append(dict(line=L, branch=u[3], out=u[1], out_type=t, cars=nums, type=nt, why=why))
            used.difference_update(u[1]); used.update(nums)
            roster[L][i] = [nt, nums, 'fixed', u[3]]
            break
    surplus[L] = [u for u in surplus.get(L, []) if sh.get(u[0], 0) >= MIN or (L in TWO and u[0] == '2×Vario LF')]
# needs come from the fresh branches (sized from the suggested pattern, user rule 20 Oct 2026). Units beyond a branch's need
# become "not needed" (shown, not counted): the unit of the branch's most frequent type, latest in the list, goes first,
# so every type stays. A branch short of its need is reported (none on 20 Oct 2026).
BRS = fresh['branches']
for L in roster:
    for i, b in enumerate(BRS.get(L, [])):
        mine = [u for u in roster[L] if u[3] == i]
        while len(mine) > b['need']:
            fx = [x for x in mine if x[2] == 'fixed']
            if fx:   # a unit swapped in above is simply not brought in: the tram it replaced is the one not needed
                u = fx[-1]; sw = next(x for x in log if x['cars'] == u[1])
                log.remove(sw); used.difference_update(u[1])
                roster[L].remove(u); mine.remove(u)
                surplus.setdefault(L, []).append([sw['out_type'], sw['out'], 'unneeded', i])
                log.append(dict(line=L, branch=i, out=sw['out'], out_type=sw['out_type'], cars=[], type='', why=f"not needed: the suggested pattern needs {b['need']}"))
                continue
            tc = collections.Counter(u[0] for u in mine); big = tc.most_common(1)[0][0]
            u = [x for x in mine if x[0] == big][-1]
            roster[L].remove(u); mine.remove(u); surplus.setdefault(L, []).append([u[0], u[1], 'unneeded', u[3]])
            log.append(dict(line=L, branch=i, out=u[1], out_type=u[0], cars=[], type='', why=f"not needed: the suggested pattern needs {b['need']}"))
        if len(mine) < b['need']: print('WARNING branch short', L, i, len(mine), '<', b['need'])
        b['assigned'] = len(mine); b['surplus'] = sum(1 for u in surplus.get(L, []) if u[3] == i)
counted = {n for us in roster.values() for u in us for n in u[1]}
# a car counted on one line is not also listed as a not-needed extra on another (the coverage swaps of 29 Sep left 6 such)
surplus = {L: [u for u in us if not counted & set(u[1])] for L, us in surplus.items()}
last = {}
hp = os.path.join(RAW, 'history.json')
if os.path.exists(hp):
    for L_, rows in json.load(open(hp, encoding='utf-8')).items():
        for r in rows:
            d = record_date(r['date'])
            if not d: continue
            for n in [int(x) for x in re.findall(r'\d{3,4}', r['car'])]:
                last[(n, L_)] = max(last.get((n, L_), ''), d.isoformat())
spares = {}
for L in roster:
    hist = [n for n in aff if aff[n][L] and available(n) and n not in counted]
    spares[L] = [dict(car=n, last=last.get((n, L), ''), weight=round(aff[n][L], 1)) for n in sorted(hist, key=lambda n: last.get((n, L), ''), reverse=True)]
out = dict(fresh, branches=BRS, roster=roster, surplus=surplus, spares=spares, rebase=log, rebased_on=C['keep_roster'],
           coverage=[c for c in P.get('coverage', []) if any(u[1] == c['cars'] for u in roster.get(c['line'], []))])
save('roster.json', out)
for x in log: print('rebase', x['line'], 'branch', x['branch'], x['out'], '->', x['cars'], x['type'])
print('units', sum(len(v) for v in roster.values()), 'swaps', len(log))
