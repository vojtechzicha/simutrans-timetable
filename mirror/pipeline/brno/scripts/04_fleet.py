"""Afternoon-peak fleet for one state: which car worked each kurz between about 15:00 and 17:00.

  python 04_fleet.py --state closure-2026-09-27

Rules (see README): morning-only records (ráno, ranní kurz) are left out; a kurz with
"před výměnou"/"po výměně" keeps the replacement unless the state resolves the swap; split
Simutrans lines (5S, 8S) and trams taken off come from the state file.
Writes data/derived/<state>/fleet.json.
"""
import argparse, collections, os, re
from common import DER, state, load, save

p = argparse.ArgumentParser(); p.add_argument('--state', required=True); a = p.parse_args()
S = state(a.state); FL = S['fleet']
vyp = load(os.path.join(DER, f"vypravenost_{S['vehicles_date']}.json"))
veh = load(os.path.join(DER, f"vehicles_{S['register_date']}.json"))

LEN = FL['length_m']            # exact type -> metres (13T variants share 'Škoda 13T')
def car_len(c):
    t = veh[c]['type']; return LEN.get(t) or LEN['Škoda 13T' if t.startswith('Škoda 13T') else t]

AM = set(FL['morning_notes'])
lines, excluded, used = {}, [], collections.Counter()
for l in S['line_order']:
    byk = collections.defaultdict(list)
    for r in vyp.get(l, []): byk[r['kurz']].append(r)
    out = []
    for k in sorted(byk, key=int):
        rs = byk[k]; pm = [r for r in rs if r['note'] not in AM]
        for r in rs:
            if r['note'] in AM: excluded.append(dict(line=l, kurz=int(k), cars=r['cars'], why='morning only (' + r['note'] + ')'))
        pre = [r for r in pm if r['note'] == 'před výměnou']; post = [r for r in pm if r['note'] == 'po výměně']
        note = ''
        if pre and post:
            for r in pre: excluded.append(dict(line=l, kurz=int(k), cars=r['cars'], why='replaced during the day (před výměnou)'))
            pm = post
            note = FL['resolved_swaps'].get(f'{l}/{k}') or \
                f"Swapped during the day; {pre[0]['cars']} ran before the swap. The swap time is not recorded, so the replacement is listed."
        if not pm: continue
        assert len(pm) == 1, (l, k, pm)
        r = pm[0]; cars = r['cars'].split('+')
        for c in cars: used[c] += 1
        out.append(dict(kurz=int(k), cars=cars, src=r['note'], note=note, len=sum(car_len(c) for c in cars),
                        regs=[veh[c]['depot'] for c in cars]))
    lines[l] = out
assert all(n == 1 for n in used.values()), [c for c, n in used.items() if n > 1]

# notes for afternoon cars and split duties
morning = collections.defaultdict(list); where = collections.defaultdict(list)
for x in excluded:
    if x['why'].startswith('morning'): morning[(x['line'], x['kurz'])].append(x['cars'])
for l, o in lines.items():
    for u in o:
        for c in u['cars']: where[c].append(f"{l}/{u['kurz']}")
kurz_depot = lambda k: FL['kurz_depot']['odd'] if k % 2 else FL['kurz_depot']['even']
for l, o in lines.items():
    for u in o:
        if u['src'] == 'odpoledne':
            am = morning.get((l, u['kurz']))
            if am:
                bits = [c + (f" (afterwards on {', '.join(sorted({w for car in c.split('+') for w in where.get(car, [])}))})"
                             if any(where.get(car) for car in c.split('+')) else '') for c in am]
                u['note'] = 'Afternoon car. Morning: ' + '; '.join(bits) + '.'
            else:
                prev = sorted({f"{x['line']}/{x['kurz']}" for x in excluded if x['why'].startswith('morning')
                               and set(x['cars'].split('+')) & set(u['cars'])})
                u['note'] = 'Afternoon car' + (f", ran {', '.join(prev)} in the morning." if prev else '. No morning record for this kurz.')
        elif u['src'] == 'ráno i odpoledne' and not u['note']:
            u['note'] = 'Split duty, out in both peaks.'
        u['note'] = FL['note_overrides'].get(f"{l}/{u['kurz']}", u['note'])
        u['note'] = re.sub(r'(\d{3,4})\+(\d{3,4})', r'\1 + \2', u['note'])
        u['kdep'] = kurz_depot(u['kurz'])
        u['mismatch'] = any(r != u['kdep'] for r in u['regs'])

# Simutrans split lines and trams taken off
def sline(l, k):
    for sid, sp in FL.get('splits', {}).items():
        if sp['line'] == l and (k in sp.get('kurzy', []) or ('kurz_min' in sp and k >= sp['kurz_min'])): return sid
    return l
# "moves": trams taken off a line for a new timetable. to=None -> depot reserve; to=<line> -> the tram
# works that line instead (shown there as an extra tram, kurz label "new"), keeping its own depot.
removed = []
mv = {(x['line'], x['kurz']): x.get('to') for x in FL.get('moves', [])}
for l in list(lines):
    for u in lines[l]:
        u['sline'] = sline(l, u['kurz'])
        if (l, u['kurz']) in mv: removed.append(dict(line=l, to=mv[(l, u['kurz'])], **u))
    lines[l] = [u for u in lines[l] if (l, u['kurz']) not in mv]
for i, r in enumerate(x for x in removed if x['to']):
    u = {k: v for k, v in r.items() if k not in ('line', 'to')}
    u.update(kurz=1000 + i, kurz_label='new', sline=r['to'],
             note=f"Moved from line {r['line']} (kurz {r['kurz']}) for the new timetable. DPMB's real kurz number is not known yet.")
    lines[r['to']].append(u)
# ---- designed trams (user rule, 29 Sep 2026): a Simutrans line short of its need gets real cars from its own recent
# history, active in the register and not out anywhere on the vehicle day (checked here against that day's records),
# marked "designed, not recorded" (state fleet.designed; picked by roster coverage, then recency)
day_busy = {c for rs in vyp.values() for r in rs for c in r['cars'].split('+')}
for i, d in enumerate(FL.get('designed', [])):
    assert not set(d['cars']) & day_busy, ('designed car was out that day', d)
    assert all(veh[c]['state'] == 'zar' for c in d['cars']), ('designed car not active', d)
    k = 900 + i
    u = dict(kurz=k, kurz_label='designed', cars=d['cars'], src='designed', note='Designed, not recorded: ' + d['why'],
             len=sum(car_len(c) for c in d['cars']), regs=[veh[c]['depot'] for c in d['cars']], sline=d['sline'],
             kdep=FL['kurz_depot']['odd'], mismatch=False, designed=True)
    lines[d['line']].append(u)

# ---- spares (user rule, 29 Sep 2026; pipeline/README.md "Roster coverage and spares"): per Simutrans line, keep
# exactly its need counted - one of every unit type first (a type is the set's types, 13T subtypes as one), then
# all-day kurzy before afternoon-only ones, lowest kurz first - and mark the rest "not needed". They leave the
# counted lists (so every count, depot and pak total skips them) and are listed dimmed on their line card.
import importlib.util as _ilu
_sp = _ilu.spec_from_file_location('tb_common', os.path.join(os.path.dirname(os.path.dirname(DER)), '..', 'brno-trolleybus', 'scripts', 'common.py'))
_tb = _ilu.module_from_spec(_sp); _sp.loader.exec_module(_tb)
TT = load(os.path.join(DER, S['name'], 'timetable.json')); NEED = TT.get('sline_need', {})
utype = lambda u: ' + '.join('Škoda 13T' if veh[c]['type'].startswith('Škoda 13T') else veh[c]['type'] for c in u['cars'])
spares = []
for l in list(lines):
    for sid in dict.fromkeys(u['sline'] for u in lines[l]):
        grp = [u for u in lines[l] if u['sline'] == sid]
        _tb.mark_spares(grp, NEED.get(sid), type_of=utype)
    spares += [dict(line=l, **u) for u in lines[l] if u.get('spare')]
    lines[l] = [u for u in lines[l] if not u.get('spare')]
save(dict(lines=lines, excluded=excluded, removed=removed, spares=spares, need=NEED), os.path.join(DER, S['name'], 'fleet.json'))
units = sum(len(o) for o in lines.values()); cars = sum(len(u['cars']) for o in lines.values() for u in o)
print('fleet', S['name'], units, 'trams', cars, 'cars; per line', {l: len(o) for l, o in lines.items()}, 'removed', len(removed), 'not needed', len(spares))
