"""needs + fleet + evidence -> derived/roster.json: the buses on every Simutrans line.

Nothing is logged. seznam-autobusu.cz has no DPmML record for the vehicle day (its day overview lists no 575xxx or
576xxx line), and only 29 records of DPmML bus lines exist at all (27 of them from September 2023, by plate). So
every bus on the sheet is DESIGNED, with a real car number, from the line's own history (brief rule b; shared rule
"Designed trams" and "Roster coverage and spares" in pipeline/README.md):

1. Line history = every city bus with evidence on the line: a seznam-autobusu record (per-line lists and the car
   pages), or a photo whose destination display shows the line (assets/photo_lines.json, read by eye from the
   newest photos of every city bus). Each car's evidence has a date; its "own line" is the line of its newest
   evidence, so a car photographed on 30 in 2024 and on 12 in 2026 belongs to 12 first.
2. Every car must be active (register state "zar", a city bus of the Most or Litvínov garage) and not out on any other
   line that day. With no records for the day, the second check is empty for every car; it is still applied (a car
   is used once on the sheet).
3. Lines are filled in order of need (largest first). Per line, the picks first cover every type of the line's roster
   (history types, most evidence first) that the picked buses lack, then go by recency of the car's evidence on the
   line: (a) cars whose own line this is, (b) other free cars with history on the line.
4. Where the history runs out: free cars of the line's home garage (the garage of most of its history cars; the
   town's garage when there is no history), of the line's main type (its most frequent history type, else the
   garage's most common type), cars with no evidence anywhere first, then those whose own line is already full.
   Marked "designed, not recorded: no history on the line" with the reason.
5. Fleet coverage (user, 29 Sep 2026): every type AND livery of the active fleet must be on a line at 16:00; a
   missing one replaces a designed bus of a fitting line (see step 5 in the code). The weekend-only double-deckers
   take part here only.
6. The line's free history cars left over are listed under their own line as "not needed" (dimmed, not counted,
   left out of the depots and the pak totals), and so are buses displaced in step 5. A car appears once.
The picks fill the line's Simutrans lines (branches) in order: main branch first.
"""
import collections
from lib import CONFIG, load, save, asset

C = CONFIG
needs = load('needs.json'); fleet = {int(k): v for k, v in load('fleet.json').items()}
ev = {int(k): v for k, v in load('evidence.json').items()}
REC = load('records.json')

def usable(n): return n in fleet and fleet[n]['city']
# ---- 1. line history
hist = collections.defaultdict(dict)        # line -> car -> dict(last, n, how)
for n, e in ev.items():
    if not usable(n): continue
    items = [(r['line'], r['date'], f"logged on line {r['line']} on {r['date']}" + (f" (kurz {r['kurz']})" if r['kurz'] else '')) for r in e['records']]
    items += [(p['line'], p['date'], (f"photographed on the tram replacement on {p['date']} ({p['read']})" if p['line'] == 'NAD' else f"photographed on line {p['line']} on {p['date']} ({p['read']})")) for p in e['photo_lines'] if p['line']]
    for L, d, how in items:
        h = hist[L].setdefault(n, dict(last='', n=0, how=[]))
        h['n'] += 1; h['how'].append((d, how))
        h['last'] = max(h['last'], d)
for L in hist:
    for h in hist[L].values(): h['how'].sort(reverse=True)
own = {}
for L, cars in hist.items():
    for n, h in cars.items():
        if n not in own or h['last'] > hist[own[n]][n]['last']: own[n] = L

def home(L):
    c = collections.Counter(fleet[n]['depot_code'] for n in hist.get(L, {}))
    if c: return c.most_common(1)[0][0]
    return C['home_garage'].get(L, 'Mos')
def rtypes(L):
    c = collections.Counter()
    for n, h in hist.get(L, {}).items(): c[fleet[n]['type']] += h['n']
    return c

order = sorted(needs, key=lambda L: -sum(b['need'] for b in needs[L]['branches']))
used = set(); roster = {}; notes = {}
for L in order:
    need = sum(b['need'] for b in needs[L]['branches'])
    H = hist.get(L, {}); RT = rtypes(L); picks = []
    def free(n): return usable(n) and n not in used and n not in [p for p, _ in picks]
    for _ in range(need):
        have = {fleet[p]['type'] for p, _ in picks}
        tiers = [[n for n in H if free(n) and own.get(n) == L], [n for n in H if free(n)]]
        pick = None
        for pool in tiers:
            if not pool: continue
            lack = [t for t, _c in RT.most_common() if t not in have and any(fleet[n]['type'] == t for n in pool)]
            cand = [n for n in pool if fleet[n]['type'] == lack[0]] if lack else pool
            cand.sort(key=lambda n: (H[n]['last'], H[n]['n'], -n), reverse=True)
            n = cand[0]; d, how = H[n]['how'][0]
            why = (f"covers the {fleet[n]['full']} of the line's roster; " if lack else '') + how
            if H[n]['n'] > 1: why += f"; {H[n]['n']} sightings on the line in all"
            if own.get(n) != L: why += f" (its newest evidence is on {'the tram replacement' if own[n] == 'NAD' else 'line ' + own[n]})"
            pick = (n, dict(kind='history', why=why, last=H[n]['last'])); break
        if not pick:
            hd = home(L); mt = RT.most_common(1)[0][0] if RT else collections.Counter(
                fleet[n]['type'] for n in fleet if usable(n) and fleet[n]['depot_code'] == hd).most_common(1)[0][0]
            cand = [n for n in fleet if free(n)]
            cand.sort(key=lambda n: (fleet[n]['depot_code'] != hd, fleet[n]['type'] != mt, n in own, n))
            n = cand[0]
            why = (f"no free bus with history on line {L}: a free {fleet[n]['full']} of the {C['fleet']['depots'][fleet[n]['depot_code']]} garage"
                   + (f", the line's main type" if RT and fleet[n]['type'] == mt else (", the garage's usual type" if fleet[n]['type'] == mt else '')))
            why += ", with no record or readable photo on any line" if n not in own else f" (its newest evidence is on line {own[n]}, already covered)"
            pick = (n, dict(kind='garage', why=why, last=None))
        picks.append(pick)
    used |= {p for p, _ in picks}
    # fill the branches in order
    i = 0; out = []
    for bi, b in enumerate(needs[L]['branches']):
        for _ in range(b['need']):
            n, w = picks[i]; i += 1
            out.append(dict(car=n, branch=bi, **w))
    roster[L] = out
    notes[L] = dict(home=home(L), types=RT.most_common(), history=len(H))

# ---- 5. fleet coverage (user, 29 Sep 2026: "each type should be represented"): every city-bus type AND livery of the
# active DPmML fleet must be on a line at 16:00. A missing type x livery puts one of its buses (newest evidence first)
# on a line: its own evidence line if that is on the sheet, else a line of its home garage; articulated buses only on
# lines where articulated buses already run; a double-decker (weekend-only) on its own line if it runs at 16:00,
# else a 12 m line. It replaces a designed bus of that line whose type x livery stays on the sheet without it: same
# type first, then garage picks, then the oldest evidence. The line's count stays exactly its need; the displaced bus
# becomes "not needed" on that line.
TY = asset('types.json')['types']
def liv(n):
    p = fleet[n]['paint']
    return 'Prague red-white' if 'městské schéma' in p else ('BVG yellow' if 'BVG' in p else 'white-yellow-red')
def combo(n): return (fleet[n]['type'], liv(n))
def cls(n): return TY.get(fleet[n]['type'], {}).get('cls', '')
eligible = [n for n in fleet if fleet[n]['city'] or fleet[n].get('weekend_only')]
def evidence(n):
    e = ev.get(n, {'records': [], 'photo_lines': []})
    it = [(r['date'], r['line'], f"logged on line {r['line']} on {r['date']}") for r in e['records']]
    it += [(p['date'], p['line'], (f"photographed on the tram replacement on {p['date']}" if p['line'] == 'NAD' else f"photographed on line {p['line']} on {p['date']}") + f" ({p['read']})") for p in e['photo_lines'] if p['line']]
    return sorted(it, reverse=True)
def on_sheet(): return collections.Counter(combo(u['car']) for L in roster for u in roster[L])
coverage = []; displaced = collections.defaultdict(list)
for cb in sorted({combo(n) for n in eligible}):
    if on_sheet()[cb]: continue
    cands = sorted([n for n in eligible if combo(n) == cb and n not in used], key=lambda n: (evidence(n)[0][0] if evidence(n) else '', -n), reverse=True)
    if not cands: continue
    n = cands[0]; evl = [L for _d, L, _h in evidence(n) if L in roster]
    if cls(n) == '18 m': ok = [L for L in roster if any(cls(u['car']) == '18 m' for u in roster[L])]
    elif cls(n) == 'double-deck': ok = [L for L in evl] or [L for L in roster if all(cls(u['car']) == '12 m' for u in roster[L])]
    else: ok = list(roster)
    def lrank(L):
        return (0 if L in evl else 1, evl.index(L) if L in evl else 0, 0 if notes[L]['home'] == fleet[n]['depot_code'] else 1,
                -sum(1 for u in roster[L] if cls(u['car']) == cls(n)), lkey_(L))
    lkey_ = lambda L: (1, 0) if not L.isdigit() else (0, int(L))
    placed = False
    for L in sorted(ok, key=lrank):
        cnt = on_sheet()
        vict = [u for u in roster[L] if u['kind'] != 'coverage' and cnt[combo(u['car'])] > 1]
        if not vict: continue
        vict.sort(key=lambda u: (fleet[u['car']]['type'] != fleet[n]['type'], u['kind'] != 'garage', u['last'] or '', -u['car']))
        v = vict[0]
        why = 'every fleet type and livery represented (user rule, 29 Sep): the only ' + f"{fleet[n]['full']} in {cb[1]}" + (' on the sheet' if len([m for m in eligible if combo(m) == cb]) > 1 else ' in the fleet')
        if fleet[n].get('weekend_only'): why += '; normally weekends only (DPmML runs its double-deckers on Saturdays, Sundays and holidays)'
        if evidence(n): why += '; ' + evidence(n)[0][2]
        else: why += f"; no record or readable photo on a line yet; placed on a line with {'articulated' if cls(n) == '18 m' else 'such'} buses of its {C['fleet']['depots'][fleet[n]['depot_code']]} garage"
        why += f"; replaces {v['car']} ({fleet[v['car']]['full']})"
        i = roster[L].index(v)
        roster[L][i] = dict(car=n, branch=v['branch'], kind='coverage', why=why, last=evidence(n)[0][0] if evidence(n) else None)
        used.discard(v['car']); used.add(n)
        vw = v['why'].split('; covers')[0]
        displaced[L].append(dict(car=v['car'], last=v['last'] or '', n=0, how=f"displaced by {n} so that every fleet type and livery is on a line (user rule, 29 Sep); it was designed for this line: {v['why']}"))
        coverage.append(dict(combo=list(cb), car=n, line=L, replaces=v['car']))
        print('coverage', cb, n, '-> line', L, 'replacing', v['car']); placed = True; break
    if not placed: print('coverage FAILED for', cb)
for L in roster:
    assert len(roster[L]) == sum(b['need'] for b in needs[L]['branches']), L

# ---- 6. the free history cars left over: "not needed", under their own line; displaced buses under their line
spares = collections.defaultdict(list)
for L, v in displaced.items(): spares[L] += v
dis = {x['car'] for v in displaced.values() for x in v}
for n, L in own.items():
    if n in used or n in dis or L not in roster: continue
    d, how = hist[L][n]['how'][0]
    spares[L].append(dict(car=n, last=hist[L][n]['last'], n=hist[L][n]['n'], how=how))
for L in spares: spares[L].sort(key=lambda x: x['last'], reverse=True)
off = {n: own[n] for n in own if own[n] not in roster}          # evidence only on lines not on the sheet

save('roster.json', dict(roster=roster, spares=spares, coverage=coverage, notes=notes, history={L: {str(n): h for n, h in H.items()} for L, H in hist.items()},
                         own={str(n): L for n, L in own.items()}, off_sheet=off, day_lines=REC['vehicle_day_lines']))
tot = sum(len(v) for v in roster.values())
print('designed', tot, 'from history', sum(1 for v in roster.values() for u in v if u['kind'] == 'history'),
      'from the garage', sum(1 for v in roster.values() for u in v if u['kind'] == 'garage'), 'fleet coverage', len(coverage), 'not needed', sum(len(v) for v in spares.values()))
for L in order:
    print(L, [(u['car'], fleet[u['car']]['type'], u['kind'][0]) for u in roster[L]], 'spares', [s['car'] for s in spares.get(L, [])])
