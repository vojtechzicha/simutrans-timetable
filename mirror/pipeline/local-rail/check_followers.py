"""Follower check for timing points (method check, 25 Oct 2026; redoes the 16 Oct scratchpad check of the S9 sheet).
Run from the working folder:  python -X utf8 pipeline/local-rail/check_followers.py build_s9_s2 [line_id ...] [all]

For every timed entry labelled "timing point" (with 'all': every timed intermediate stop), the real workday trains
that are not Os (R, Sp, Ex, IC, EC, SC, rj, RJ, LE ...) passing the same station in the same direction 0 - 8 min after
the held train's real departure minute, 13:00 - 19:59, folded on the line's interval (the game runs the slot every
interval all day). Prints the closest follower per entry. Design rule (README, S9 / S4 sheets): a timing point only
where no faster train follows within about 6 min. A follower that leaves the line at that station is still listed
(direction = same previous or next location), so read each hit by hand.
"""
import importlib
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
mod = importlib.import_module(sys.argv[1])
import build_012_014_235 as base  # noqa: E402

args = sys.argv[2:]
want_all = 'all' in args
ids = {a for a in args if a != 'all'}
by_num, wd = base.load()
T = json.load(open(base.TRAINS, encoding='utf-8'))
real = []
for t in T:
    if not base.runs(t, base.WEEK[2]):
        continue
    locs = [l for l in t['locs'] if (l.get('dep') if l.get('dep') is not None else l.get('arr')) is not None]
    if not locs:
        continue
    num = next((l['num'] for l in locs if l.get('num')), '?')
    ctt = next((l.get('ctt') for l in locs if l.get('ctt')), None)
    real.append((num, ctt, locs))
CAT = {'84': 'Os', '122': 'Sp', '157': 'R', '63': 'IC', '50': 'EC', '94': 'SC', '209': 'rj', '69': 'Ex', '70': 'EN',
       '9003': 'LE', '9004': 'RJ', '9001': 'TLX', '9002': 'TL'}
for L in mod.LINES:
    if ids and L['id'] not in ids:
        continue
    x = base.build_line(L, by_num, wd)
    iv = L['every']
    for k, leg in enumerate(x['legs']):
        if leg.get('depot') or not leg.get('raw'):
            continue
        raw = leg['raw']
        names = [base.full(l['name']) for l in raw]
        stops = {s_['name']: s_ for s_ in leg['stops'][1:-1]}
        for nm, s_ in stops.items():
            key = (leg['num'], nm)
            lab = x['wp'].get(key)
            if not (want_all or (lab and lab.startswith('timing point'))):
                continue
            if lab is None and not want_all:
                continue
            i = next((j for j, n in enumerate(names) if n == nm), None)
            if i is None or i == 0 or i + 1 >= len(raw):
                continue
            code, pc, nc = raw[i]['code'], raw[i - 1]['code'], raw[i + 1]['code']
            m = s_['dep'] + x['shifts'][k]
            best = []
            for num, ctt, locs in real:
                if ctt == '84':
                    continue
                cs = [l['code'] for l in locs]
                if code not in cs:
                    continue
                j = cs.index(code)
                if not ((pc in cs[max(0, j - 6):j]) or (nc in cs[j + 1:j + 7])):
                    continue
                l = locs[j]
                t = l.get('dep') if l.get('dep') is not None else l.get('arr')
                if not (13 * 60 <= t < 20 * 60):
                    continue
                gap = (t - m) % iv
                if 0 < gap <= 8:
                    best.append((gap, f"{CAT.get(ctt, ctt)} {num} {int(t)//60}:{int(t)%60:02d}{'½' if t % 1 else ''}"))
            best.sort()
            g = f"closest {best[0][0]:g} min: " + ', '.join(b for _, b in best[:3]) if best else 'none within 8 min'
            print(f"{L['name']:24} {nm:30} towards {leg['stops'][-1]['name']:24} dep :{int(m) % 60:02d} [{(lab or 'timed')[:12]}]  {g}")
