"""Resolve which vehicle ran each course in the afternoon peak -> data/derived/<state>/courses.json

Rules (from the record notes, which carry no times):
  * "ranní část" / "odpolední část": a split course; the afternoon part is the peak vehicle.
  * "náhrada za X" / "nahrazen vlakem Y": a swap. The chain is ordered by how many cars each record says
    it replaced (0 = the original). "opět" / "zpět" = the original came back at the end.
  * "přejezd na linku N": the course moves to line N. Pools (lines sharing courses) and transfers come
    from the state file.
  * A car that turns up later as a replacement on another (swapped) course means its own course probably
    ended before the peak ("am" = not counted).
  * added_courses from the state file (courses the target network has but the vehicle day did not run).

Usage: python 04_courses.py --state 2026-09-27
"""
import argparse, collections, os, re
from common import state, load, save, DER

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--state', required=True)
    s = state(ap.parse_args().state)
    REC = load(os.path.join(DER, f'records_{s["vehicle_date"]}.json'))
    V = load(os.path.join(DER, f'vehicles_{s["register"]["raw"]}.json')); V.update(s.get('vehicle_overrides', {}))
    pool_of = {l: k for k, p in s.get('pools', {}).items() for l in p['lines']}
    transfers = {t['course']: t for t in s.get('transfers', [])}

    def vinfo(setstr):
        cars = setstr.split('+'); info = [V.get(c, {}) for c in cars]
        return dict(set=setstr, cars=cars, types=[i.get('type', '?') for i in info], depots=[i.get('depot', '?') for i in info],
                    depot=info[0].get('depot', '?'))

    courses = []
    for L, rs in REC.items():
        by = collections.defaultdict(list)
        for r in rs: by[int(r['course'])].append(r)
        for k in sorted(by):
            rr = by[k]
            am = [r for r in rr if 'ranní část' in r['note']]
            pm = [r for r in rr if 'odpolední část' in r['note']]
            rest = [r for r in rr if r not in am and r not in pm]
            use = pm if pm else rest
            def nrepl(r):
                if 'náhrada za' not in r['note']: return 0
                return len(re.findall(r'\d{3,4}(?:\+\d{3,4})?', r['note'].split('náhrada za')[1].split(',')[0]))
            use = sorted(use, key=nrepl)
            chain = [r['car'] for r in use]
            if any(('opět' in r['note'] or 'zpět' in r['note']) for r in use): chain.append(chain[0])
            transfer = None
            for r in rr:
                m = re.search(r'přejezd na linku (\d+)', r['note'])
                if m: transfer = m.group(1)
            cid = f'{L}/{k}'
            pm_line = transfers[cid]['to_line'] if cid in transfers else L
            courses.append(dict(id=cid, line=L, course=k, pm_line=pm_line, group=pool_of.get(pm_line, pm_line),
                                chain=chain, am=[r['car'] for r in am], split=bool(pm), swap=len(chain) > 1,
                                transfer=transfer, raw_notes=[r['note'] for r in rr if r['note']],
                                veh=[vinfo(x) for x in dict.fromkeys(chain)], source=s['vehicle_date']))
    for a in s.get('added_courses', []):
        L = a['line']
        courses.append(dict(id=f'{L}/{a["course"]}', line=L, course=a['course'], pm_line=L, group=pool_of.get(L, L),
                            chain=[a['set']], am=[], split=False, swap=False, transfer=None, raw_notes=[],
                            veh=[vinfo(a['set'])], source=a['source'], added_note=a['note']))

    # lines whose records are always incomplete: design the missing courses (user instruction, 28 Sep)
    TT = load(os.path.join(DER, s['name'], 'timetable.json'))['lines']
    HIST = load(os.path.join(DER, 'history.json'))
    used = {car for c in courses for x in c['chain'] + c['am'] for car in x.split('+')}   # also morning-part cars
    for L, cfg in s.get('fill_to_cycle', {}).items():
        need = TT[L]['cycle_need']; have = [c for c in courses if c['line'] == L]
        cands = []
        for r in HIST.get(L, []):          # newest first on the page
            if r['car'] not in cands and not (set(r['car'].split('+')) & used) and all(V.get(x, {}).get('state') == 'zar' for x in r['car'].split('+')):
                cands.append(r['car'])
        nxt = max(c['course'] for c in have) + 1
        for i in range(max(0, need - len(have))):
            car = cands[i]; used |= set(car.split('+'))
            seen_days = sorted({r['date'] for r in HIST[L] if r['car'] == car})
            courses.append(dict(id=f'{L}/{nxt + i}', line=L, course=nxt + i, pm_line=L, group=pool_of.get(L, L), chain=[car], am=[], split=False,
                                swap=False, transfer=None, raw_notes=[], veh=[vinfo(car)], source='designed',
                                added_note=f'Designed addition: the records never show more than {len(have)} course(s) on line {L}, but the timetable needs {need} sets at 16:00 (runtime both ways plus turnaround, every {TT[L]["routes"][0]["headway"]} min). {car.replace("+", " + ")} ran line {L} on {", ".join(seen_days)} and was not in service on {s["vehicle_date"]}.'))
    seen = collections.defaultdict(list)
    for c in courses:
        for x in dict.fromkeys(c['chain']): seen[x].append(c)
    for c in courses:
        u = ''
        if c['swap']: u = 'swap'
        elif any(o is not c and o['swap'] and x in o['chain'][1:] for x in c['chain'] for o in seen[x]): u = 'am'
        elif c['id'] in transfers: u = 'moved'
        elif c.get('added_note'): u = 'designed' if c['source'] in ('designed', 'stand-in') else 'added'
        c['uncertain'] = u
        n = []
        if c['id'] in transfers: n.append(transfers[c['id']]['note'])
        elif c['transfer'] and pool_of.get(c['line']) and pool_of.get(c['transfer']) == pool_of.get(c['line']):
            n.append(f'Through to line {c["transfer"]} (přejezd na linku {c["transfer"]}).')
        if c['split']: n.append('Afternoon part of a split course; morning part ran ' + ', '.join(x.replace('+', ' + ') for x in c['am']) + '.')
        if c['swap']: n.append('Vehicle exchanged during the day, time not recorded: ' + ' → '.join(x.replace('+', ' + ') for x in c['chain']) + '.')
        if u == 'am':
            o = next(o for x in c['chain'] for o in seen[x] if o is not c and o['swap'] and x in o['chain'][1:])
            n.append(f'Same set later replaced a car on {o["id"]}, so this course probably ends before the afternoon peak (not counted).')
        if c.get('added_note'): n.append(c['added_note'])
        if c['id'] in s.get('course_notes', {}): n.append(s['course_notes'][c['id']])
        c['note'] = ' '.join(n)
        c['final'] = c['chain'][-1]
    # branches of split lines (state "splits"): which course runs which branch
    for key, brs in s.get('splits', {}).items():
        for br in brs:
            for c in courses:
                if c['group'] == key and c['line'] == br.get('course_line', br.get('line', key)) and c['course'] in br['courses']:
                    c['branch'] = br['label']
        miss = [c['id'] for c in courses if c['group'] == key and 'branch' not in c]
        if miss: print('WARNING: courses without a branch on', key, miss)
    # logged surplus -> "not needed" (user, 29 Sep 2026; pipeline/README.md "Roster coverage and spares"): per Simutrans line
    # (branch, shared pool or line) keep exactly its need counted - one unit of every type first (most frequent type first), then
    # recorded before added/designed, then the lowest course numbers - and mark the rest uncertain = 'spare' (not counted).
    museum = set(s.get('museum_lines', []))
    TTF = load(os.path.join(DER, s['name'], 'timetable.json'))
    groups = collections.defaultdict(list)
    for c in courses:
        if c['uncertain'] == 'am' or c['line'] in museum: continue
        groups[(c['group'], c.get('branch'))].append(c)
    nspare = 0
    for (G, br), cs in groups.items():
        if br: need = TTF.get('branches', {}).get(G, {}).get(br, {}).get('need')
        elif G in TTF.get('pools', {}): need = TTF['pools'][G].get('need')
        else: need = TTF['lines'].get(G, {}).get('cycle_need')
        if not need or len(cs) <= need: continue
        typ = lambda c: tuple(next(v for v in c['veh'] if v['set'] == c['final'])['types'])
        order = sorted(cs, key=lambda c: (c['uncertain'] in ('designed', 'added', 'stand-in'), int(c['line']), int(c['course'])))
        keep = []
        for ty, _ in collections.Counter(typ(c) for c in cs).most_common():
            if len(keep) >= need: break
            keep.append(next(c for c in order if typ(c) == ty))
        for c in order:
            if len(keep) >= need: break
            if c not in keep: keep.append(c)
        for c in cs:
            if c not in keep:
                c['uncertain'] = 'spare'; nspare += 1
                c['note'] = (c['note'] + ' ' if c['note'] else '') + f'Not needed at 16:00: the Simutrans line needs {need}. Not counted.'
    print('not needed (logged surplus):', nspare)
    dup = {x: [c['id'] for c in cs] for x, cs in seen.items() if len(cs) > 1}
    out = os.path.join(DER, s['name'], 'courses.json')
    save(dict(courses=courses, shared_sets=dup), out)
    print(len(courses), 'courses;', sum(1 for c in courses if c['uncertain'] != 'am' and c['line'] not in s.get('museum_lines', [])), 'counted at the peak; sets on two courses:', dup)

if __name__ == '__main__':
    main()
