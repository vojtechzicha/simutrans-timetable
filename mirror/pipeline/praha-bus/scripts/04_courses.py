"""Deployment records + register -> vehicle per course, with livery and pak object -> data/derived/<state>/courses.json

Records: data/raw/vypravenost/<vehicle_date>/<line>.html (course, car numbers, register car ids, note).
Day: the vehicle date; a line nobody logged that day takes the nearest extra day that has it. When the counted courses are fewer
than the line needs at 16:00 (gtfs_lines "need"), courses logged on other days fill in (nearest day first, marked with their
date, and only if the car was not out anywhere on the vehicle date: day overview), and any still missing are "designed, not
recorded" with real car numbers: active cars from the line's history (vypis?linka=L&since=..., working days preferred), not out
anywhere on the vehicle date. The picks first cover every type in the line's roster that the used cars lack, then go newest first;
the free roster cars left over are listed as "not needed" (user, 29 Sep). When the history has too few free cars, free active cars
of the line's own types, then the operator's usual city-line types, fill the rest (garages of the line's cars first).
Per course: all vehicles in record order; notes "náhrada za X" / "nahrazen vozem Y" order a swap (the replacement is
counted, the replaced vehicle is shown and not counted), "ranní/odpolední část" keeps the afternoon part.
Per vehicle: register type, length (bus_types.json), operator, garage, paint -> livery slug:
  schéma PID šedá s červenými pruhy -> pidsedocervena, schéma PID červeno-bílo-modrá -> pidcervenomodrobila,
  městské schéma červeno-bílá -> dppcervenobila (DPP) / mestskacervenobila (other operators), Veolia -> veoliacervenoseda,
  bílá -> bila; advert wraps (CVR, celolep) -> the operator's normal livery: pidsedocervena for cars from 2020 on,
  otherwise pidcervenomodrobila (DPP: dppcervenobila for SOR NB/BN, pidsedocervena for newer types).
Pak object: DPP cars use the VZ-DPPraha-bus objects in bus_types.json "rules"; every other car gets the object the VZ pak
session is making for it in the shared Prague package VZ-Praha-bus: VZ-Praha-<Type>-<livery>-<id> (its scheme, 29 Sep 2026;
the operator is not part of the name, operators share an object per type and livery; articulated buses are -A/-B), marked
"requested" until pak_requested.json "in_pak" lists it. Type tokens reuse DPP tokens for the same model.

Usage: python 04_courses.py --state 2026-09-29
"""
import argparse, collections, datetime, glob, json, os, re
from common import state, load, save, RAW, DER, ASSETS, _txt, parse_vypis

LIVERY_NAMES = {'pidsedocervena': 'PID grey-red', 'pidcervenomodrobila': 'PID red-white-blue', 'dppcervenobila': 'DPP red-white',
                'mestskacervenobila': 'city red-white', 'veoliacervenoseda': 'Veolia red-grey', 'bila': 'white'}

def parse_records(path):
    t = open(path, encoding='utf-8').read(); out = []
    for tr in re.findall(r'<tr class="row[^"]*">(.*?)</tr>', t, flags=re.S):
        ids = list(dict.fromkeys(re.findall(r'/vuz/(\d+)/vypravenost', tr)))
        tr2 = re.sub(r"data-bmhd-context-box='.*?'", '', tr, flags=re.S)
        cell = lambda c: _txt(m.group(1)) if (m := re.search(r'<td class="%s">(.*?)</td>' % c, tr2, flags=re.S)) else ''
        out.append(dict(car=cell('car').replace(' + ', '+'), ids=ids, course=cell('order-on-line'), note=cell('note')))
    return out

KNOWN = [('schéma PID, šedá', 'pidsedocervena'), ('schéma PID, červeno-bílo-modrá', 'pidcervenomodrobila'), ('Veolia', 'veoliacervenoseda'),
         ('bílá', 'bila'), ('tyrkysová se žlutým pruhem', 'tyrkysovozluta'),
         ('CVR Fashion Arena', 'fashionarena')]   # line 238 wrap kept as its own objects (user, via the pak session, 29 Sep)

def base_livery(v):
    """The car's own livery slug, or None for an advert wrap or a livery the pak does not have."""
    p = v['paint'].split(' & ')[0].strip()
    if p.startswith('městské schéma, červeno-bílá'): return 'dppcervenobila' if v['operator'] == 'DPP' else 'mestskacervenobila'
    if p == 'červená' and v['operator'] == 'DPP': return 'dppcervena'   # DPP coach red with the gold Praha skyline (8002 II; pak session, 29 Sep)
    for k, slug in KNOWN:
        if p == k or p.startswith(k + ' ') or p.startswith(k + ','): return slug
    return None

def make_livery(V):
    """Advert wraps and other liveries -> the same type's normal livery (the pak session's rule): the most common own livery of
    the operator's cars of that type and year, else of that type, else pidsedocervena from 2020, else the operator's older scheme."""
    by = {}
    for v in V.values():
        s = base_livery(v)
        if s: by.setdefault((v['operator'], v['maker_type'], v.get('year')), []).append(s); by.setdefault((v['operator'], v['maker_type']), []).append(s)
    def livery(v):
        s = base_livery(v)
        if s: return s, ''
        why = 'advert wrap' if v['paint'].startswith('CVR') or 'polep' in v['paint'] else 'livery not in the pak'
        for k in ((v['operator'], v['maker_type'], v.get('year')), (v['operator'], v['maker_type'])):
            if by.get(k): return max(set(by[k]), key=by[k].count), why
        if (v.get('year') or '0') >= '2020': return 'pidsedocervena', why
        return ('dppcervenobila' if v['operator'] == 'DPP' else 'pidcervenomodrobila'), why
    return livery

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--state', required=True); s = state(ap.parse_args().state)
    V = load(os.path.join(DER, f'vehicles_{s["register_raw"]}.json'))
    BT = load(os.path.join(ASSETS, 'bus_types.json')); PR = load(os.path.join(ASSETS, 'pak_requested.json'))
    P = load(os.path.join(DER, s['name'], 'gtfs_lines.json'))['lines']
    OBJ = load(os.path.join(ASSETS, 'pak_objects.json'))['objects']
    livery = make_livery(V)
    def pak(v, pkg=None):
        liv, why = livery(v)
        t = v['maker_type']
        if pkg == 'PID':   # a regional companion's non-DPP car: the PID regional package's own tokens (fleet desk, 30 Oct 2026)
            tok = PR.get('pid_type_tokens', {}).get(t) or re.sub(r'[^A-Za-z0-9]+', '_', t.replace('’', '')).strip('_')
        else:
            tok = (v['operator'] == 'DPP' and PR.get('dpp_type_tokens', {}).get(t)) or PR['type_tokens'].get(t) or re.sub(r'[^A-Za-z0-9]+', '_', t.replace('’', '')).strip('_')
        pkg = pkg or ('DPPraha' if v['operator'] == 'DPP' else 'Praha')
        name = f'VZ-{pkg}-{tok}-{liv}-{PR["id_tokens"].get(tok, tok)}'
        art = name + '-A' in OBJ or (BT['length_m'].get(t) or 0) >= 17
        chain = [name + '-A', name + '-B'] if art else [name]
        have = all(c in OBJ for c in chain)
        return dict(object=chain[0], chain=chain, core=PR['id_tokens'].get(tok, tok), livery=liv, mapped=why, status='in pak' if have else 'requested')
    def car(num, cid):
        v = V.get(cid) if cid else None
        if not v: return dict(num=num, id=cid, type='?', length=None, operator='?', garage='?', paint='', year='', pak=None)
        return dict(num=num, id=cid, type=v['maker_type'], length=BT['length_m'].get(v['maker_type']), operator=v['operator'],
                    garage=v['garage'], paint=v['paint'], year=v.get('year', ''), pak=pak(v))
    def courses_of(recs):
        by = collections.defaultdict(list)
        for r in recs: by[r['course']].append(r)
        res = {}
        for k, rr in by.items():
            am = [r for r in rr if 'ranní' in r['note']]
            pm = [r for r in rr if 'odpolední' in r['note']]
            use = pm or [r for r in rr if r not in am] or rr
            use = sorted(use, key=lambda r: 1 if 'náhrada za' in r['note'] else 0)
            chain = []
            for r in use:
                nums = r['car'].split('+'); ids = r['ids'] + [None] * (len(nums) - len(r['ids']))
                chain.append(dict(set=r['car'], cars=[car(n, i) for n, i in zip(nums, ids)], note=r['note']))
            res[k] = dict(course=k, chain=chain, swap=len(chain) > 1, split=bool(pm), am=[r['car'] for r in am])
        return res
    vd = s['vehicle_date']
    days = [vd] + sorted(s.get('extra_days_non_dpp', []), key=lambda d: abs((datetime.date.fromisoformat(d) - datetime.date.fromisoformat(vd)).days))
    ckey = lambda x: (not x.isdigit(), int(x) if x.isdigit() else 0, x)
    def reg_op(gtfs_name):       # PID sub-agency name -> the register's operator name
        if gtfs_name.startswith('Dopravní podnik'): return 'DPP'
        g = re.sub(r'[^A-ZÁ-Ž ]', ' ', gtfs_name.upper()).split()
        for op in sorted({v['operator'] for v in V.values()}, key=len, reverse=True):
            o = re.sub(r'[^A-ZÁ-Ž ]', ' ', op.upper()).split()
            if o and g[:len(o)] == o: return op
        return None
    def fin_key(x): return (x['type'], x['operator'], x['garage'], x['length'], json.dumps(x['pak'], ensure_ascii=False))
    # every vehicle out anywhere in PID on the vehicle date (day overview): a filled-in or designed car must not be among them
    ov = os.path.join(RAW, 'vypravenost', vd, 'overview.html')
    busy = set(re.findall(r'/vuz/(\d+)/', open(ov, encoding='utf-8').read())) if os.path.exists(ov) else set()
    holidays = set(s.get('holidays', []))
    def workday(iso):
        return bool(iso) and datetime.date.fromisoformat(iso).weekday() < 5 and iso not in holidays
    def hist_rows(L):
        H = os.path.join(RAW, 'vypravenost', 'history')
        for pat in (f'{L}.html', f'{L}_p*.html'), (f'{L}_y.html', f'{L}_y_p*.html'):
            fs = [f for g in pat for f in sorted(glob.glob(os.path.join(H, g)))]
            rows = [dict(r2, ids=r['ids']) for f in fs for r, r2 in zip(parse_records(f), parse_vypis(f))]
            if rows: break
        for r in rows:
            m = re.search(r'(\d{2})\.(\d{2})\.\s*(\d{4})', r['date']); r['iso'] = f'{m.group(3)}-{m.group(2)}-{m.group(1)}' if m else ''
        return rows
    def roster(L, ops):
        """Active cars that ran line L in its history (working days preferred), newest first."""
        rows = hist_rows(L); wk = [r for r in rows if workday(r['iso'])] or rows
        cars = {}
        for r in wk:
            for num, cid in zip(r['car'].split('+'), r['ids']):
                v = V.get(cid)
                if not v or v['state'] != 'zar': continue
                e = cars.setdefault(cid, dict(num=num, id=cid, dates=[], n=0, type=v['maker_type'], operator=v['operator']))
                e['n'] += 1
                if r['iso'] not in e['dates']: e['dates'].append(r['iso'])
        mine = {k: e for k, e in cars.items() if e['operator'] in ops}
        return mine or cars
    def designed_car(L, i, e, why, dates):
        return dict(line=L, course=f'+{i + 1}', chain=[dict(set=e['num'], cars=[car(e['num'], e['id'])], note='')], swap=False, split=False, am=[],
                    am_only=False, source='designed', why=why, hist=dates)
    def spare_car(L, e, state_):
        return dict(line=L, course='', chain=[dict(set=e['num'], cars=[car(e['num'], e['id'])], note='')], swap=False, split=False, am=[],
                    am_only=True, spare=state_, source='history', hist=e['dates'][:3])
    regional = set(s.get('regional', {}).get('interleaved', {}))
    def overview_recs(d, L):
        """A regional companion's courses from the day overview (vypravenost/pid?datum=D): no per-line page was fetched for it."""
        f = os.path.join(RAW, 'vypravenost', d, 'overview.html')
        if not os.path.exists(f): return []
        out_ = []
        for sec in open(f, encoding='utf-8').read().split('<div class="route-data">')[1:]:
            m = re.search(r'linka=[^"&]+">([^<]+)</a>', sec)
            if not m or m.group(1).strip() != L: continue
            for it in sec.split('<span class="item">')[1:]:
                c = re.search(r'class="course">([^<]*)<', it)
                vs = re.findall(r'class="context-box" href="https://seznam-autobusu.cz/vuz/(\d+)/vypravenost">([^<]+)</a>', it)
                if vs: out_.append(dict(car='+'.join(n for _, n in vs), ids=[i for i, _ in vs], course=c.group(1) if c else '', note=''))
        return out_
    out, logged = [], {}
    for L, p in P.items():
        if p['route_type'] != '3': continue
        per_day = {}
        for d in days:
            path = os.path.join(RAW, 'vypravenost', d, f'{L}.html')
            recs = parse_records(path) if os.path.exists(path) else []
            if not recs and L in regional and d == vd: recs = overview_recs(d, L)
            if recs: per_day[d] = courses_of(recs)
        got = {}
        if per_day:
            base = next(d for d in days if d in per_day)
            got = {k: dict(c, source=base) for k, c in per_day[base].items()}
            # a car that later replaced another course's vehicle probably ran its own course only in the morning
            later = {x['set'] for c in got.values() for x in c['chain'][1:]}
            for c in got.values(): c['am_only'] = not c['swap'] and c['chain'][0]['set'] in later
            need = p.get('need') or 0
            counted = lambda: sum(1 for c in got.values() if not c['am_only'])
            used = {x['set'] for c in got.values() for x in c['chain']}
            for d in days:            # courses not logged on the base day, from the nearest day that logged them (car free on the base day)
                if counted() >= need: break
                if d == base or d not in per_day: continue
                for k in sorted(per_day[d], key=ckey):
                    if counted() >= need: break
                    c = per_day[d][k]
                    ids = {x['id'] for x in c['chain'][-1]['cars'] if x['id']}
                    if k in got or c['chain'][-1]['set'] in used or (d != vd and ids & busy): continue
                    got[k] = dict(c, source=d, am_only=False); used |= {x['set'] for x in c['chain']}
        logged[L] = got
        for k in sorted(got, key=ckey):
            out.append(dict(line=L, **got[k]))
    taken = busy | {x['id'] for c in out for ch in c['chain'] for x in ch['cars'] if x['id']}
    # the operators' city-line types (fallback for lines without any history)
    by_op = collections.defaultdict(collections.Counter)
    for c in out:
        if not c['am_only']:
            for x in c['chain'][-1]['cars']:
                if x['type'] != '?': by_op[x['operator']][x['type']] += 1
    # lines sized from their Simutrans lines (gtfs_lines simlines, 28 Oct 2026) design last: their larger need must not take the
    # free cars other lines were already given (146's +1 had shifted the fleet picks of 208, 211 and 220)
    # the regional companions (owner, 30 Oct 2026) design after every city line, so they cannot take a city line's free cars
    for L, p in sorted(P.items(), key=lambda kv: (kv[0] in regional, bool(kv[1].get('simlines')))):
        if p['route_type'] != '3' or not p.get('need'): continue
        got = logged.get(L, {})
        short = p['need'] - sum(1 for c in got.values() if not c['am_only'])
        if short <= 0: continue
        # designed, not recorded: real cars from the line's history, free on the vehicle date. Every type in the line's roster
        # (history + logged) is represented among the used cars first (user, 29 Sep); the free cars left over are listed as
        # "not needed".
        ops = {o for o in (reg_op(x) for x in p['operators']) if o} | {x['operator'] for c in got.values() for x in c['chain'][-1]['cars']}
        R = roster(L, ops)
        have = {x['type'] for c in got.values() if not c['am_only'] for x in c['chain'][-1]['cars']}
        free = sorted((e for e in R.values() if e['id'] not in taken), key=lambda e: (e['dates'][0] if e['dates'] else '', e['n']), reverse=True)
        tfreq = collections.Counter()
        for e in R.values(): tfreq[e['type']] += e['n']
        picks = []
        for ty, _ in tfreq.most_common():
            if len(picks) >= short: break
            if ty in have: continue
            e = next((e for e in free if e['type'] == ty and e not in picks), None)
            if e: picks.append(e); have.add(ty)
        for e in free:
            if len(picks) >= short: break
            if e not in picks: picks.append(e)
        for i, e in enumerate(picks):
            taken.add(e['id']); out.append(designed_car(L, i, e, 'history', e['dates'][:3]))
        n0 = len(picks)
        if n0 < short:            # no (or too little) line history: free active cars of the operator's usual city-line types
            op = next((o for o in (reg_op(x) for x in p['operators']) if o), None)
            types = [ty for ty, _ in tfreq.most_common()]           # the line's own types first, then the operator's
            types += [ty for ty, _ in by_op.get(op, collections.Counter()).most_common() if ty not in types]
            if L in regional:      # a companion with no record at all (318): the operator's most common active type, numbered cars only
                types += [ty for ty, _ in collections.Counter(v['maker_type'] for v in V.values() if v['operator'] == op and v['state'] == 'zar').most_common() if ty not in types]
            garages = collections.Counter(x['garage'] for c in got.values() for x in c['chain'][-1]['cars'] if x['garage'])
            garages.update(V[e['id']]['garage'] for e in R.values())
            rank = lambda cid: (types.index(V[cid]['maker_type']) if V[cid]['maker_type'] in types else len(types), -garages.get(V[cid]['garage'], 0), V[cid]['num'])
            pool = sorted((cid for cid, v in V.items() if v['operator'] == op and v['state'] == 'zar' and cid not in taken
                           and BT['length_m'].get(v['maker_type']) and (v['num'] or L not in regional)), key=rank)   # any city-sized type last, if its usual types are all out
            for i, cid in enumerate(pool[:short - n0]):
                taken.add(cid); out.append(designed_car(L, n0 + i, dict(num=V[cid]['num'], id=cid), 'fleet', []))
        for e in free:
            if e not in picks and e['id'] not in taken: out.append(spare_car(L, e, 'not needed'))
    # logged surplus (user, 29 Sep, confirmed via the Brno session): where more courses are logged than the line needs, keep exactly
    # the need counted - one of every type among the line's vehicles first (most frequent type first), then the lowest course
    # numbers - and mark the rest "not needed" (not counted; shown dimmed). Same rule as brno-trolleybus common.mark_spares.
    by_line = collections.defaultdict(list)
    for c in out:
        if not c['am_only'] and c['source'] != 'designed': by_line[c['line']].append(c)
    typ = lambda c: ' + '.join(x['type'] for x in c['chain'][-1]['cars'])
    for L, cs in by_line.items():
        need = P[L].get('need') or 0
        if not need or len(cs) <= need: continue
        order = sorted(cs, key=lambda c: (c['source'] != vd, ckey(c['course'])))      # best to keep first
        keep = []
        for ty, _ in collections.Counter(typ(c) for c in cs).most_common():
            if len(keep) >= need: break
            keep.append(next(c for c in order if typ(c) == ty))
        for c in order:
            if len(keep) >= need: break
            if c not in keep: keep.append(c)
        for c in cs:
            if c not in keep: c['am_only'] = True; c['spare'] = 'surplus'
    # a line's own surplus courses logged going over to another line (přejezd na linku B) are B's real buses: they replace B's designed
    # ones, course order first (owner, 30 Oct 2026: "I see all 117 written as continues to 203 - isn't there something to consider?";
    # 117's ten courses run 203 too, 203 has no record of its own). The designed picks of every other line stay as they were.
    for B in sorted({c['line'] for c in out if c['source'] == 'designed'}, key=ckey):
        des = [c for c in out if c['line'] == B and c['source'] == 'designed']
        donors = [c for c in out if c.get('spare') == 'surplus' and c['line'] != B
                  and any(re.search(r'přejezd na link\S* [^.]*\b' + B + r'\b', ch['note']) for ch in c['chain'])]
        donors.sort(key=lambda c: (ckey(c['line']), ckey(c['course'])))
        for d_, c in zip(des, donors):
            out[out.index(d_)] = dict(c, line=B, am_only=False, spare=None, moved_from=c['line'])
            c['spare'] = 'moved'; c['moved_to'] = B
    # the regional companions' non-DPP cars are in VZ-PID-bus, not VZ-Praha-bus (fleet desk, 30 Oct 2026: "VZ-Praha-bus is only for
    # city lines (100-299, 900s) run by non-DPP operators")
    for c in out:
        if c['line'] in regional:
            for ch in c['chain']:
                for x in ch['cars']:
                    if x['pak'] and x['operator'] != 'DPP': x['pak'] = pak(V[x['id']], 'PID')
    save(dict(courses=out, vehicle_date=vd, days=days), os.path.join(DER, s['name'], 'courses.json'))
    st = collections.Counter(c['pak']['status'] for x in out for c in x['chain'][-1]['cars'] if c['pak'])
    src = collections.Counter(x.get('spare') or ('designed ' + x['why'] if x['source'] == 'designed' else ('base day' if x['source'] == vd else 'other day')) for x in out)
    print(len(out), 'courses on', len({x['line'] for x in out}), 'lines;', dict(st), dict(src))

if __name__ == '__main__':
    main()
