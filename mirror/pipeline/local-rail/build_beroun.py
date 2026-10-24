"""Trains west and south-west of Praha (west of the Vltava, not north of Beroun): S7 Praha – Beroun, S76 Liteňka,
S6 and S65 from Praha-Smíchov, R16 and the Os Beroun – Rokycany, the Příbram line (S60 Beroun – Blatná,
Březnice – Čimelice) and R26 Praha – Čimelice. Added the same day: S20 Kolín – Čáslav – Havlíčkův Brod
(only these trains, at their real termini; no branches).
13 Oct 2026 (user): in the game the track ends at Rokycany, Blatná and Čimelice, so those lines are cut there
('cut' legs of the real trains, 'cut_at' so the real through trains still count as the line's trains).

Designed 10 Oct 2026 with the rules in ../rail-design-rules.md and the builder in build_012_014_235.py (real JR2026
times from CIS JŘ, trains that run on all five days Mon–Fri 5–9 Oct 2026). PID labels come from the CIS line number
(S = 1000 + n). Unit types from vagonweb.cz (vagonweb.py; R16 is "Berounka", R26 is Arriva, zeme ARV).
Engineering works at Praha-Smíchov (user, 15 Oct 2026: "I want to model both please - you need to validate that in
Zlíchov only one vehicle occupies the track"): S6 starts and ends at the temporary stop Praha-Zlíchov (1 Jul – 19 Oct
2026, 21:00; ČD works timetable cz-k173-2026vyluka07, which keeps the CIS passing minutes at Zlíchov), and S65 runs
only Praha-Zličín – Rudná (Praha-Smíchov – Praha-Zličín closed 13 Aug – 30 Nov 2026, trains cancelled without
replacement; ČD closure 22963). Both checked against the PID GTFS of 29 Sep (Wed 7 Oct). S6 becomes one line for both
branches (10-min turns at Zlíchov, as the real units: 847 006 + 847 018 ran Os 19923 then Os 19968 on 4 Jun 2026), and
the build checks that Praha-Zlíchov and the track from Praha-Hlubočepy hold one train at a time (`one_at_a_time`).
Final S6 (user, 15 Oct 2026: "prepare the final S6 after exclusion but with the combined line"): S6_WORKS = False.
S6 runs from Praha-Smíchov again (from 19 Oct 2026, 21:00) as the same combined line, turning in 5 min at Smíchov
(in :11 → out :16, in :41 → out :46) instead of 35 min on two lines; 4 vehicles. S65 stays at Praha-Zličín until
30 Nov. S6_WORKS = True rebuilds the Zlíchov version.
Both S6 on one page (user, 15 Oct 2026: "why isn't there big table for S6 befor the end of works?"): with
S6_WORKS = False the Zlíchov version is a second, 'temporary' line (s6z) on copies of the S6 trains that start and end
at Praha-Zlíchov (keys "<train> Zlíchov", only in by_num, so the inventory sees the real trains once). It uses the
same 4 vehicles as S6, so the totals leave it out.
Ex6 (user, 15 Oct 2026: "add me to the latest file Ex6 to Rokycany please"): the hourly Ex6 path Praha-Vysočany –
Praha hl. n. – Plzeň is two lines every 2 h with their own coaches, the IC "Západní expres" to Cheb (55x/56x) and the
EC / alex trains to München (35x). The real trains pass Rokycany without stopping; `load()` makes copies that end
there at the passing minute (keys "<train> Rokycany", only in by_num, like the Zlíchov copies). S70 is timed at
Hořovice both ways, where the München trains overtake it.
Writes "Trains Beroun Plzeň Příbram.html" in the project root.
Run: python pipeline/local-rail/build_beroun.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_012_014_235 as base  # noqa: E402

OUT = os.path.join(base.ROOT, 'archive', 'Trains Beroun Plzeň Příbram.html')  # archived 13 Oct 2026
SM, ZL, HL, ZC = 'Praha-Smíchov', 'Praha-Zlíchov', 'Praha-Hlubočepy', 'Praha-Zličín'
S6_WORKS = False  # True: S6 at Praha-Zlíchov (works until 19 Oct 2026, 21:00); False: the final S6 from Praha-Smíchov
S6_END = ZL if S6_WORKS else SM
_load = base.load
base.CATS.update({'63': 'IC', '50': 'EC'})  # Ex6: IC Západní expres, EC to München
RTAG = ' Rokycany'
RCOPIES = []  # Ex6 trains cut at Rokycany, which they pass without stopping: (key, record)
_cache = []
ZTAG = ' Zlíchov'
ZCOPIES = []  # the workday S6 trains as they run from Praha-Zlíchov (S6_WORKS = False: for the s6z line)


def load():
    """the real data, adjusted for the Praha-Smíchov works: with S6_WORKS, S6 (1006) starts and ends at Praha-Zlíchov
    at its CIS passing minute there (the works timetable's minutes); S65 (1065) is cut at Praha-Zličín"""
    if _cache:
        return _cache[0]
    by_num, wd = _load()
    for r in {id(r): r for r in list(by_num.values()) + wd}.values():
        names = [s_['name'] for s_ in r['stops']]
        if SM not in names or names.index(SM) not in (0, len(names) - 1):
            continue
        first = names.index(SM) == 0
        if r['svc'] == '1006':
            z = next((l for l in r['raw'] if l['name'] == ZL), None)
            if z is not None:
                k = 0 if first else -1
                zs = {'name': ZL, 'arr': None if first else z['arr'], 'dep': z['dep'] if first else None, 'req': False}
                if S6_WORKS:
                    r['stops'][k] = zs
                else:  # the works version as its own line (s6z), on copies of the trains
                    c = dict(r, stops=[dict(s_) for s_ in r['stops']])  # keeps its real number; the key is "<train> Zlíchov"
                    c['stops'][k] = zs
                    by_num[r['num'] + ZTAG] = c
                    if r['all5']:
                        ZCOPIES.append((r['num'] + ZTAG, c))
        elif r['svc'] == '1065' and ZC in names:
            j = names.index(ZC)
            r['stops'] = [dict(s_) for s_ in (r['stops'][j:] if first else r['stops'][:j + 1])]
            r['stops'][0 if first else -1]['arr' if first else 'dep'] = None
    for r in {id(r): r for r in list(by_num.values()) + wd}.values():
        names = [s_['name'] for s_ in r['stops']]
        rok = next((l for l in r['raw'] if l['name'] == 'Rokycany'), None)
        if 'Praha hl. n.' not in names or 'Rokycany' in names or rok is None or r['num'].endswith((RTAG, ZTAG)):
            continue
        if not any(str(l.get('svc')) == '6' for l in r['raw']):
            continue
        out = [l['name'] for l in r['raw']].index('Rokycany') > [l['name'] for l in r['raw']].index('Praha hl. n.')
        j = names.index('Praha hl. n.')
        st = [dict(s_) for s_ in (r['stops'][:j + 1] if out else r['stops'][j:])]
        if out:
            st.append({'name': 'Rokycany', 'arr': rok['arr'], 'dep': None, 'req': False})
        else:
            st.insert(0, {'name': 'Rokycany', 'arr': None, 'dep': rok['dep'], 'req': False})
        st[0]['arr'], st[-1]['dep'] = None, None
        c = dict(r, svc='6', stops=st)  # keeps its real number (the RE from München has no line number in the data)
        by_num[r['num'] + RTAG] = c
        if r['all5']:
            RCOPIES.append((r['num'] + RTAG, c))
    _cache.append((by_num, wd))
    return by_num, wd


base.load = load


def one_at_a_time(lines, station, before=None):
    """Every stay at `station` (from the arrival there to the departure from there), over 4 hours of all the sheet's
    lines. With `before`, the stretch before -> station -> before counts as well (the stub Praha-Hlubočepy – Praha-Zlíchov):
    from the departure at `before` towards the station to the arrival back at `before`. Returns the stays and the clashes."""
    stays = []
    for x in lines:
        iv, legs, sh = x['L']['every'], x['legs'], x['shifts']
        for k, t in enumerate(legs):
            nk = (k + 1) % len(legs)
            nsh = sh[nk] if nk else sh[0] + x['cycle']  # after the last leg the vehicle starts its next round
            for j, s_ in enumerate(t['stops']):
                if s_['name'] != station or j == 0:
                    continue
                out, osh = (legs[nk]['stops'], nsh) if j == len(t['stops']) - 1 else (t['stops'][j:], sh[k])
                a, d = s_['arr'] + sh[k], out[0]['dep'] + osh
                if before:
                    a = next(p['dep'] for p in reversed(t['stops'][:j]) if p['name'] == before) + sh[k]
                    d = next(p['arr'] for p in out[1:] if p['name'] == before) + osh
                for m in range(-480 // iv, 720 // iv):  # 8 h before to 12 h after the leg's real train
                    stays.append((int(a) + m * iv, int(d) + m * iv, x['L']['name'], t['num']))
    stays.sort()
    w0 = 780  # 13:00 – 16:59, inside the unrolled range of every line
    win = [s_ for s_ in stays if w0 <= s_[0] < w0 + 240]
    clash = [(p, q) for i, p in enumerate(stays) for q in stays[i + 1:] if q[0] < p[1] and p in win]
    return win, clash
# the inventory looks at these services on the local lines; R16 and R26 look only at their own (inv_svcs)
LOCAL = {'1007', '1006', '1065', '1076', '1070', '3202', '1060', '3160', '3166'}
IMP = 'important station'
A_S7 = 'S7 Praha – Beroun and Liteňka'
A_SM = f'{S6_END} and Praha-Zličín – Rudná – Beroun'
A_PL = 'Beroun – Rokycany'
A_PB = 'Příbram line'
A_KH = 'Kolín – Čáslav – Havlíčkův Brod'

LINES = [
    # --- S7 Praha – Beroun -------------------------------------------------------------------------------------
    {
        'id': 's7', 'name': 'S7', 'area': A_S7, 'svc': '1007', 'every': 30,
        'rep_out': '8848', 'rep_in': '8853', 'turns': [9, 8],
        'wait_points': {},
        'notes': [
            'PID S7. All day a train leaves Praha hl. n. at :16 and :46 (Beroun :06 and :36) and Beroun at :15 and :45 (Praha hl. n. :08 and :38). Only in the late morning and late evening every other train turns at Řevnice (listed under Not modelled).',
            'Four vehicles. It turns in 9 min at Beroun (in :06 / :36, out :15 / :45) and 8 min at Praha hl. n. (in :08 / :38, out :16 / :46), the real minutes. No stop on the way has a stay of 5 min or more, so only the two ends are timed.',
            'Vehicles: 471 CityElefant units (vagonweb 2026, Os 8848 runs as two units).',
        ],
    },
    {
        'id': 's7r', 'name': 'S7 Řevnice', 'area': A_S7, 'svc': '1007', 'every': 30,
        'rep_out': '9950', 'rep_in': '9953',
        'wait_points': {},
        'notes': [
            'The peak S7 trains Praha-Smíchov – Řevnice: from Smíchov :04 and :34, from Řevnice :13 and :43. They run every 30 min in the morning (Smíchov 5:04 – 8:34) and the afternoon (Smíchov 13:04 – 19:34). With S7 that makes a train every 15 min on Praha-Smíchov – Řevnice.',
            'Three vehicles. 12 min at Řevnice; 24 min at Praha-Smíchov (in :10 / :40, out :04 / :34), the real minutes.',
            'Its own line, not part of S7: these trains are a class 162 locomotive with double-deck push-pull coaches (Bdmteeo, vagonweb 2026, Os 9950), while S7 runs CityElefants.',
        ],
    },
    {
        'id': 's76', 'name': 'S76 Liteňka', 'area': A_S7, 'svc': '1076', 'every': 120,
        'rep_out': '27720', 'rep_in': '27723',
        'wait_points': {('out', 'Liteň'): 'reverses, the driver changes cabs', ('in', 'Liteň'): 'reverses, the driver changes cabs',
                        ('in', 'Všeradice'): 'crossing with the train to Lochovice'},
        'notes': [
            'PID S76, the Liteňka (KJŘ 172). In the afternoon a train leaves Zadní Třebaň every 2 h at S:32 (14:32, 16:32, 18:32) and Lochovice at S:35 (14:35, 16:35, 18:35); both arrive at L:20.',
            'Two trains, as in reality. They cross at Všeradice: the train to Zadní Třebaň waits there 2 min (:55 – :57), so Všeradice is timed in that direction. The trains reverse at Liteň and stand there 3 min both ways (S:42 – S:45 towards Lochovice, L:08 – L:11 towards Zadní Třebaň) while the driver changes cabs, so Liteň is timed both ways (user, 11 Oct 2026). Each train then waits 1 h 15 min at Lochovice and 1 h 12 min at Zadní Třebaň: the real minutes.',
            'Vehicles: 814 RegioNova (vagonweb 2026).',
        ],
    },
    # --- Praha-Zlíchov / Praha-Zličín – Rudná – Beroun (Praha-Smíchov works, user 15 Oct 2026) --------------------
    {
        # one line for both branches: the stub at Praha-Zlíchov holds one train, and the real units alternate
        'id': 's6', 'name': 'S6', 'area': A_SM, 'svc': '1006', 'every': 60,
        'legs': ['19916', '19923', '19966', '19967'], 'terminal': [S6_END],
        'inv_svcs': {'1006'},  # its own trains only: from Smíchov the S7 trains to Beroun would count as Smíchov – Beroun
        'turns': [10, 10, 10, 10] if S6_WORKS else [10, 5, 10, 5],  # Smíchov: in :11 → out :16, in :41 → out :46
        'wait_points': {},
        'notes': [
            'PID S6 (KJŘ 173), the final state after the Praha-Smíchov works (from 19 October 2026, 21:00, the trains are back at Praha-Smíchov, annual JR2026 minutes). Every hour from Praha-Smíchov at :46 to Beroun (:38) and at :16 to Nučice zastávka (:47); back from Beroun at :22 (Smíchov :11) and from Nučice zastávka at :11 (Smíchov :41).',
            'One line for the Beroun and the Nučice trains (your choice, 15 October 2026), as the real units run: the train in from Beroun at :11 leaves for Nučice at :16, and the train in from Nučice at :41 leaves for Beroun at :46. vagonweb: on Thursday 4 June 2026 units 847 006 + 847 018 ran Os 19923 Beroun 16:22 → Praha-Smíchov 17:11 and then Os 19968 Praha-Smíchov 17:16 → Nučice zastávka, exactly this 5-min turn.',
            'It turns in 5 min at Praha-Smíchov each time, instead of 35 min on the two old lines (S6 and S6 Nučice, 3 + 2 vehicles). Four vehicles. 44 min at Beroun, 24 min at Nučice zastávka, the real minutes. Both Praha-Smíchov entries are stop type terminal, so nobody rides through from one branch to the other. No stop on the way has a stay of 5 min or more.',
            'Vehicles: 847 RegioFox (vagonweb 2026).',
            'Until 19 October, 21:00 (works) the same line starts and ends at the temporary stop Praha-Zlíchov: see S6 until 19 October below.',
        ] if not S6_WORKS else [
            'PID S6 (KJŘ 173) during the Praha-Smíchov works (1 July – 19 October 2026, 21:00): every train starts and ends at the temporary stop Praha-Zlíchov, near the Hlubočepy tram stop (ČD works timetable cz-k173-2026vyluka07; the PID feed has the same minutes). Every hour from Praha-Zlíchov at :48 to Beroun (:38) and at :18 to Nučice zastávka (:47); back from Beroun at :22 (Zlíchov :08) and from Nučice zastávka at :11 (Zlíchov :38). From Praha-Hlubočepy on, every minute is the annual one.',
            'One line for the Beroun and the Nučice trains, as the real units run: the train in from Beroun at :08 leaves for Nučice at :18, and the train in from Nučice at :38 leaves for Beroun at :48. vagonweb: on Thursday 4 June 2026 units 847 006 + 847 018 ran Os 19923 Beroun 16:22 → Praha-Smíchov 17:11 and then Os 19968 Praha-Smíchov 17:16 → Nučice zastávka.',
            'Praha-Zlíchov holds one train at a time, checked by the build (see the area notes): each train stands there 10 min, :08 – :18 and :38 – :48. With the two old lines each train would stand 40 min (Beroun trains :08 – :48, Nučice trains :38 – :18), so two trains would stand there together for 10 min every half hour.',
            'Four vehicles (was 3 + 2 as two lines from Praha-Smíchov). 44 min at Beroun, 24 min at Nučice zastávka and 10 min at Praha-Zlíchov each time, the real minutes. Both Praha-Zlíchov entries are stop type terminal, so nobody rides through from one branch to the other. No stop on the way has a stay of 5 min or more.',
            'Vehicles: 847 RegioFox (vagonweb 2026).',
            'From 19 October, 21:00, the trains are back at Praha-Smíchov: annual minutes Smíchov :46 to Beroun and :16 to Nučice zastávka, in at :11 and :41.',
        ],
    },
] + ([] if S6_WORKS else [
    {
        # the works version next to the final one (user, 15 Oct 2026); the same 4 vehicles, so not in the totals
        'id': 's6z', 'name': 'S6 until 19 October', 'area': A_SM, 'svc': '1006', 'every': 60, 'temporary': 'the S6 vehicles, until 19 October', 'same_vehicles_as': 'S6',
        'legs': [n + ZTAG for n in ['19916', '19923', '19966', '19967']], 'terminal': [ZL],
        'inv_svcs': {'-'},  # no inventory of its own: the real trains are counted once, on S6
        'turns': [10, 10, 10, 10],
        'wait_points': {},
        'notes': [
            'PID S6 (KJŘ 173) during the Praha-Smíchov works (1 July – 19 October 2026, 21:00): every train starts and ends at the temporary stop Praha-Zlíchov, near the Hlubočepy tram stop (ČD works timetable cz-k173-2026vyluka07; the PID feed has the same minutes). Every hour from Praha-Zlíchov at :48 to Beroun (:38) and at :18 to Nučice zastávka (:47); back from Beroun at :22 (Zlíchov :08) and from Nučice zastávka at :11 (Zlíchov :38). From Praha-Hlubočepy on, every minute is the annual one.',
            'The same line and the same 4 vehicles as S6, so it is not counted in the totals: until 19 October, 21:00, set the S6 line to these entries, then switch it to the S6 entries above. Only the two Praha entries change (Praha-Zlíchov instead of Praha-Smíchov, offsets 48 and 18 instead of 46 and 16); Beroun 22 and Nučice zastávka 11 stay.',
            'One line for the Beroun and the Nučice trains, as the real units run: the train in from Beroun at :08 leaves for Nučice at :18, and the train in from Nučice at :38 leaves for Beroun at :48.',
            'Praha-Zlíchov holds one train at a time, checked by the build (see the area notes): each train stands there 10 min, :08 – :18 and :38 – :48. Both Praha-Zlíchov entries are stop type terminal, so nobody rides through from one branch to the other. 44 min at Beroun, 24 min at Nučice zastávka, the real minutes.',
            'Vehicles: 847 RegioFox (vagonweb 2026), the S6 units.',
        ],
    },
]) + [
    {
        'id': 's65', 'name': 'S65', 'area': A_SM, 'svc': '1065', 'every': 60,
        'rep_out': '25920', 'rep_in': '25921',
        'wait_points': {},
        'notes': [
            'PID S65 during the Praha-Smíchov works: Praha-Smíchov – Praha-Zličín is closed from 13 August to 30 November 2026, and those trains are cancelled without replacement (PID; ČD closure 22963). So S65 runs Praha-Zličín – Hostivice – Rudná u Prahy at its annual minutes, the same as in the PID feed. Every hour from Praha-Zličín at :19 (Rudná u Prahy :48), back from Rudná at :10 (Zličín :36).',
            'It reverses at Hostivice and stays there 9 min going out and 8 min coming back, so Hostivice is timed both ways.',
            'Two vehicles (was 3 from Praha-Smíchov). 22 min at Rudná u Prahy and 43 min at Praha-Zličín (in :36, out :19), the real minutes. Only S65 uses Praha-Zličín, one train at a time (checked by the build).',
            'Vehicles: 810 (vagonweb 2026; 810 511 seen on 18 September).',
        ],
    },
    # --- Beroun – Rokycany (the game's track ends at Rokycany, user 13 Oct 2026) ----------------------------------
    {
        'id': 'r16', 'name': 'R16', 'area': A_PL, 'svc': '16', 'every': 60, 'cat': 'R', 'inv_svcs': {'16'},
        'legs': [{'cut': ('762', 'Praha hl. n.', 'Rokycany')}, {'cut': ('771', 'Rokycany', 'Praha hl. n.')}],
        'turns': [7, 12], 'cut_at': ['Rokycany'],
        'wait_points': {('out', 'Beroun'): IMP, ('in', 'Beroun'): IMP},
        'notes': [
            'R16 "Berounka", cut at Rokycany, where the game\'s track ends. In reality it runs on via Plzeň hl. n. to Klatovy. Every hour from Praha hl. n. at :05 (Rokycany :26) and from Rokycany at :33 (Praha hl. n. :53).',
            'Three vehicles. It turns in 7 min at Rokycany (in :26, out :33) and 12 min at Praha hl. n. (in :53, out :05). Beroun (2 min) is timed as an important station.',
            'The 7 min at Rokycany are not a real turn: the real train in :26 runs on to Plzeň, and the :33 back is another train coming from Klatovy. The game simply joins the two real minutes. If 7 min is too tight for a locomotive and coaches in the game, the train waits for the next :33 instead: 1 h 7 min at Rokycany and 4 vehicles.',
            'Vehicles: a ČD 193 Vectron with five or six coaches (ABmz, Bbdgmee, Bmz, Bpee; vagonweb 2026, R 762 and R 771).',
        ],
    },
    {
        'id': 's70', 'name': 'S70', 'area': A_PL, 'svc': ['1070', '3202'], 'every': 120,
        'legs': [{'cut': ('7820', 'Beroun', 'Rokycany')}, {'cut': ('7823', 'Rokycany', 'Beroun')}],
        'turns': [10, 10], 'cut_at': ['Rokycany'],
        'wait_points': {('out', 'Hořovice'): 'Ex6 overtakes', ('in', 'Hořovice'): 'Ex6 overtakes'},
        'notes': [
            'The Os Beroun – Rokycany (PID S70 on the Beroun – Kařez part, KJŘ 170), cut at Rokycany. In reality they run on to Plzeň hl. n. and Přeštice. Every 2 h from Beroun at S:14 (Rokycany L:02) and from Rokycany at S:56 (Beroun L:46).',
            'Two vehicles. The train stands 1 h 54 min at Rokycany (in L:02, out S:56): the next train towards Beroun in the real timetable leaves at S:56, because the L:56 from Rokycany is the Hořovice train. 28 min at Beroun, the real minutes. Hořovice (3 min out, 4 min back) is not timed.',
            'Timed at Hořovice both ways (added 15 October with Ex6): Ex6 to and from München overtakes it there, through at S:34 while S70 stands S:33 – S:36 towards Rokycany, and through at L:25 while S70 stands L:22 – L:26 towards Beroun. Without the timing the faster game train would leave early and hold Ex6 up to Rokycany or Beroun.',
            'Vehicles: 650 RegioPanter (vagonweb 2026, Os 7820 and Os 7823).',
        ],
    },
    {
        'id': 'ex6c', 'name': 'Ex6 Cheb', 'area': A_PL, 'svc': '6', 'every': 120, 'cat': 'IC', 'inv_svcs': {'-'},
        'legs': ['560' + RTAG, '561' + RTAG], 'cut_at': ['Rokycany'],
        'turns': [21, 10],
        'wait_points': {},
        'notes': [
            'Ex6, the ČD IC "Západní expres" Praha – Plzeň – Cheb (CIS line 6), cut at Rokycany. Every 2 h from Praha-Vysočany at S:22, Praha hl. n. S:28 – S:35 (Rokycany L:49); back from Rokycany at S:10, Praha hl. n. L:21 – L:28 (Praha-Vysočany L:34).',
            'No stop between Praha hl. n. and Plzeň. The real trains pass Rokycany without stopping (Cheb trains out L:49, back S:10; München trains out S:49, back L:10); in the game the line ends there, where the track ends, and turns in 21 min, joining the two real passing minutes. The Praha end is the real one: from Praha hl. n. the trains run on to Praha-Vysočany (6 min) and stand there until their next trip, 48 – 51 min. That costs no extra vehicle: turning at Praha hl. n. instead would mean 74 min there.',
            'Route: the real trains run Praha hl. n. – Praha-Vršovice – Praha-Krč – Praha-Velká Chuchle – Praha-Radotín (the Krč connection), not via Praha-Smíchov. In the game the schedule has no stop in between, so the train takes whichever way is built.',
            'Two vehicles (4 h ÷ 2 h): 21 min at Rokycany (in L:49, out S:10), 7 min at Praha hl. n. both ways, 48 min at Praha-Vysočany (in L:34, out S:22). Same line in the game save: Ex6/2 "Praha hl.n. - Cheb" (no vehicles yet).',
            'Vehicles: a ČD 193 Vectron with InterJet coaches Ampz, Bbmpz, 2 × Bmpz, Bdmpz and a Bdmpee (vagonweb 2026, IC 560 and IC 561).',
        ],
    },
    {
        'id': 'ex6m', 'name': 'Ex6 München', 'area': A_PL, 'svc': '6m',  # '6m': its real trains come only from extra_real (IC 551 stops at Rokycany and is a Cheb train)
        'every': 120, 'cat': 'EC', 'inv_svcs': {'-'},
        'legs': ['352' + RTAG, '357' + RTAG], 'cut_at': ['Rokycany'],
        'turns': [21, 10],
        'wait_points': {},
        'notes': [
            'Ex6, the trains Praha – Plzeň – Furth im Wald – München (EC from Praha, alex RE of Die Länderbahn back; CIS line 6), cut at Rokycany. Every 2 h from Praha-Vysočany at L:22, Praha hl. n. L:28 – L:35 (Rokycany S:49); back from Rokycany at L:10, Praha hl. n. S:21 – S:25 (Praha-Vysočany S:31).',
            'No stop between Praha hl. n. and Plzeň. The real trains pass Rokycany without stopping (Cheb trains out L:49, back S:10; München trains out S:49, back L:10); in the game the line ends there, where the track ends, and turns in 21 min, joining the two real passing minutes. The Praha end is the real one: from Praha hl. n. the trains run on to Praha-Vysočany (6 min) and stand there until their next trip, 48 – 51 min. That costs no extra vehicle: turning at Praha hl. n. instead would mean 74 min there.',
            'Route: the real trains run Praha hl. n. – Praha-Vršovice – Praha-Krč – Praha-Velká Chuchle – Praha-Radotín (the Krč connection), not via Praha-Smíchov. In the game the schedule has no stop in between, so the train takes whichever way is built.',
            'Two vehicles (4 h ÷ 2 h): 21 min at Rokycany (in S:49, out L:10), 7 min at Praha hl. n. out and 4 min back, 51 min at Praha-Vysočany (in S:31, out L:22). Same line in the game save: Ex6/1 "Praha hl.n. - München Hbf" (no vehicles yet).',
            'Vehicles: between Praha and Plzeň a ČD 362 with ČD Bdmpee and Die Länderbahn Bmz and ABbmdz coaches (vagonweb 2026, EC 352 and RE 357; DLB 223 from Plzeň on). Back from Plzeň the RE also carries a ČD ABmz and Bmz for Plzeň – Praha.',
            'It overtakes S70 at Hořovice both ways (S70 is timed there).',
        ],
    },
    {
        'id': 'p170h', 'name': 'Os Hořovice – Rokycany', 'area': A_PL, 'svc': ['3202', '1070'], 'every': 120,
        'legs': [{'cut': ('7818', 'Hořovice', 'Rokycany')}, {'cut': ('7825', 'Rokycany', 'Hořovice')}],
        'turns': [10, 10], 'cut_at': ['Rokycany'],
        'wait_points': {},
        'notes': [
            'The Os that start and end at Hořovice, cut at Rokycany. In reality they run on to Plzeň hl. n. (and from Přeštice). Every 2 h from Hořovice at L:12 (Rokycany L:38) and from Rokycany at L:56 (Hořovice S:22).',
            'One vehicle. 18 min at Rokycany (in L:38, out L:56) and 50 min at Hořovice (in S:22, out L:12), the real minutes.',
            'This replaces the Os/Sp Hořovice – Plzeň – Přeštice chain: everything of it beyond Rokycany (the Sp Plzeň – Rokycany shuttles and the Os to Přeštice) is outside the game.',
            'Vehicles: 650.2 RegioPanter (vagonweb 2026, Os 7818).',
        ],
    },
    # --- Příbram line (the game's track ends at Blatná and Čimelice, user 13 Oct 2026) ---------------------------
    {
        'id': 's60', 'name': 'S60', 'area': A_PB, 'svc': ['1060', '3160'], 'every': 120,
        'rep_out': '7914', 'rep_in': '7913', 'turns': [10, 8], 'cut_at': ['Blatná'],
        'wait_points': {('out', 'Příbram'): IMP, ('in', 'Příbram'): IMP},
        'notes': [
            'The Os Beroun – Zdice – Příbram – Březnice – Blatná (KJŘ 200 and 203), ending at Blatná, where the game\'s track ends. PID S60 (line 1060) is Beroun – Březnice; the trains run on to Blatná as 3160. Every 2 h from Beroun at L:01 (Příbram L:46, Blatná S:46) and from Blatná at L:11 (Příbram L:07, Beroun S:53).',
            'The line uses the real trains that end and start at Blatná (Os 7914 Beroun 17:01 → Blatná 18:46, Os 7913 Blatná 13:11 → Beroun 14:53). The trains that run on to Strakonice have the same minutes to Blatná and from Blatná (arriving S:45, leaving L:11).',
            'Two vehicles. 25 min at Blatná (in S:46, out L:11) and 8 min at Beroun (in S:53, out L:01), the real minutes. Příbram (1 min) is timed as an important station.',
            'Vehicles: 814 RegioNova (vagonweb 2026, Os 7910).',
        ],
    },
    {
        'id': 'p200', 'name': 'Os Březnice – Čimelice', 'area': A_PB, 'svc': '3166', 'every': 120,
        'legs': [{'cut': ('7954', 'Březnice', 'Čimelice')}, {'cut': ('7955', 'Čimelice', 'Březnice')}],
        'turns': [10, 10], 'cut_at': ['Čimelice'],
        'wait_points': {},
        'notes': [
            'The southern part of KJŘ 200, cut at Čimelice, where the game\'s track ends. In reality the trains run on via Písek to Protivín. Every 2 h from Březnice at S:16 (Čimelice S:36) and from Čimelice at L:20 (Březnice L:40).',
            'At Březnice it connects with S60 both ways: from Beroun in at S:13, on at S:16; from Čimelice in at L:40, S60 to Beroun out at L:43.',
            'One vehicle. 44 min at Čimelice (in S:36, out L:20) and 36 min at Březnice (in L:40, out S:16), the real minutes.',
            'Vehicles: 814 RegioNova (vagonweb 2026, Os 7954).',
        ],
    },
    {
        'id': 'r26', 'name': 'R26', 'area': A_PB, 'svc': '26', 'every': 120, 'cat': 'R', 'inv_svcs': {'26'},
        # the afternoon-peak R26 really run from and to the depot at Praha-Malešice (via Vršovice, Eden, Zahradní Město)
        'legs': [{'raw': ('1172', 'Praha-Malešice', 'Praha hl. n.'), 'route': ['Praha-Malešice', 'Praha hl. n.'], 'name': ''},
                 {'cut': ('1172', 'Praha hl. n.', 'Čimelice')}, {'cut': ('1171', 'Čimelice', 'Praha hl. n.')},
                 {'raw': ('1171', 'Praha hl. n.', 'Praha-Malešice'), 'route': ['Praha hl. n.', 'Praha-Malešice'], 'name': ''}],
        'turns': [10, 10, 7, 10], 'cut_at': ['Čimelice'],
        'wait_points': {('1172 Praha hl. n. – Čimelice', 'Beroun'): IMP, ('1171 Čimelice – Praha hl. n.', 'Beroun'): IMP,
                        ('1171 Čimelice – Praha hl. n.', 'Příbram'): IMP},
        'notes': [
            'R26, run by Arriva, cut at Čimelice, where the game\'s track ends. In reality it runs on via Písek to České Budějovice. Every 2 h from Praha hl. n. at L:22 (Čimelice L:35) and from Čimelice at S:21 (Praha hl. n. S:22), via Beroun and Příbram.',
            'Praha end (user, 10 Oct 2026: 1 h at Praha hl. n. is too much; model Malešice if the peak trains really go there, even with an extra vehicle). The afternoon-peak R26 do: R 1172 comes empty from the depot at Praha-Malešice (out 14:53, Praha hl. n. 15:03, leaves 15:22). R 1171 goes there after Praha hl. n. (in 18:22, out 18:29, Malešice 19:01). The route is Praha hl. n. – Praha-Vršovice – Praha-Eden – Zahradní Město – Praha-Malešice, never via Libeň.',
            'The line uses those real minutes: depot out S:53 → Praha hl. n. L:03, 19 min there, out L:22. In at S:22, 7 min, empty out S:29, Malešice L:01. The empty run back takes 32 min because R 1171 stands 21 min at Praha-Vršovice on the way. In the game the empty run has no timetable entry at Vršovice; it simply arrives at Malešice at L:01.',
            'Four vehicles (8 h ÷ 2 h). 46 min at Čimelice (in L:35, out S:21), the real minutes of the two directions there. Malešice L:01 misses the S:53 depot departure by 8 min, so the train waits 1 h 52 min in the depot for the next one. Without the depot runs it would be 3 vehicles with 1 h at Praha hl. n.',
            'Timed: Příbram towards Čimelice (6 min), and as important stations Beroun both ways and Příbram towards Praha.',
            'Vehicles: Arriva 845 units (vagonweb 2026, operator ARV; 845 122 and 845 123 seen, sometimes with a 945 trailer).',
        ],
    },
    # --- Kolín – Čáslav – Havlíčkův Brod (added 10 Oct 2026) ---------------------------------------------------
    {
        # the Vysočina part (Světlá – Havlíčkův Brod) has no CIS line number, so the trains from Havlíčkův Brod start with svc None
        'id': 's20', 'name': 'S20', 'area': A_KH, 'svc': ['1020', None], 'every': 120, 'inv_svcs': {'1020', None},
        'rep_out': '5919', 'rep_in': '5922', 'turns': [10, 10],
        'wait_points': {('out', 'Čáslav'): IMP, ('in', 'Čáslav'): IMP},
        'notes': [
            'The Os Kolín – Kutná Hora – Čáslav – Světlá nad Sázavou – Havlíčkův Brod (KJŘ 230; PID S20 from the CIS line number 1020, which ends at Světlá). On workdays the Kolín trains have two termini: in the even hours they run to Havlíčkův Brod, in the odd hours only to Čáslav (S20 Čáslav). From Kolín at S:34 (14:34, 16:34, 18:34; Havlíčkův Brod L:53), from Havlíčkův Brod at L:05 (13:05, 15:05, 17:05, 19:05; Kolín S:22).',
            'Two vehicles. 12 min at Kolín (in S:22, out S:34) and 1 h 12 min at Havlíčkův Brod (in L:53, out L:05 two hours later): the real minutes. No train leaves Havlíčkův Brod for Kolín in the even afternoon hours, so the train waits there. No stop has a stay of 5 min or more; Čáslav (1 min), where S20 Čáslav ends, is timed as an important station.',
            'Real trains outside the pattern: Kolín 13:35 → Havlíčkův Brod (an odd hour) and Havlíčkův Brod 14:05 → Kolín (an even hour); the game runs the 2-hour pattern. The weekend trains through to Žďár nad Sázavou are not workday trains.',
            'Vehicles: 650.2 RegioPanter (vagonweb 2026, Os 5919 and Os 5920).',
        ],
    },
    {
        'id': 's20c', 'name': 'S20 Čáslav', 'area': A_KH, 'svc': '1020', 'every': 120, 'inv_svcs': {'1020', None},
        'rep_out': '5921', 'rep_in': '5954', 'turns': [10, 10],
        'wait_points': {},
        'notes': [
            'The S20 trains that end at Čáslav, in the odd hours between the Havlíčkův Brod trains: from Kolín at L:34 (15:34, 17:34, 19:34; Čáslav L:56), from Čáslav at S:58 (16:58, 18:58; Kolín L:19).',
            'One vehicle. 1 h 2 min at Čáslav (in L:56, out S:58) and 15 min at Kolín (in L:19, out L:34), the real minutes.',
            'With S20 this gives Kolín → Čáslav a train every hour at :34. Towards Kolín: S20 from Čáslav at S:01, S20 Čáslav at S:58.',
            'Vehicles: 650.2 RegioPanter, the same type as S20 (vagonweb 2026, Os 5921 and Os 5954). The two lines meet only at Kolín, where both stay 12–15 min anyway, so one shared line would save nothing and they stay separate.',
        ],
    },
]

LISTED = {
    ('Praha-Radotín', 'Praha-Smíchov'), ('Praha-Smíchov', 'Praha-Radotín'), ('Praha hl. n.', 'Praha-Radotín'),
    ('Řevnice', 'Praha hl. n.'), ('Praha hl. n.', 'Řevnice'), ('Beroun', 'Zadní Třebaň'),
    ('Zadní Třebaň', 'Liteň'), ('Liteň', 'Zadní Třebaň'), ('Beroun', 'Beroun-Závodí'),
    ('Praha-Zličín', 'Hostivice'), ('Hostivice', 'Praha-Zličín'), ('Rudná u Prahy', 'Hostivice'),
    ('Beroun', 'Zdice'), ('Zdice', 'Beroun'),
    ('Zdice', 'Blatná'), ('Blatná', 'Zdice'), ('Beroun', 'Březnice'), ('Březnice', 'Zdice'),
    ('Kolín', 'Kutná Hora hl. n.'), ('Kutná Hora hl. n.', 'Kolín'), ('Čáslav', 'Havlíčkův Brod'), ('Havlíčkův Brod', 'Čáslav'),
}
NOT_MODELLED = [
    '<b>Beyond the end of the game\'s track (13 October 2026).</b> In the game the track ends at Rokycany, Blatná and Čimelice, so every line that went further now ends there:'
    '<br>• <b>Rokycany:</b> R16 really runs on via Plzeň hl. n. to Klatovy (and twice a day to Železná Ruda-Alžbětín); S70 and the Hořovice Os run on to Plzeň hl. n. and Přeštice. Gone completely: the Sp Plzeň hl. n. – Rokycany shuttles (part of the old Os/Sp Hořovice – Plzeň – Přeštice chain, 3 vehicles, now 1) and the branch Rokycany – Mirošov – Příkosice (KJŘ 175, 1 vehicle), which also starts at Rokycany.'
    '<br>• <b>Blatná:</b> about half the S60 trains really run on to Strakonice. Gone completely: the Blatná – Strakonice shuttle (1 vehicle) and Blatná – Nepomuk.'
    '<br>• <b>Čimelice:</b> R26 really runs on via Písek to České Budějovice, and the Os from Březnice via Písek to Protivín. Gone completely: the R26 shuttles Písek – České Budějovice.',
    '<b>S7:</b> in the late morning and evening every other train runs Praha hl. n. – Řevnice instead of Praha-Smíchov – Řevnice (Praha hl. n. 9:46, 10:46, 11:46, 20:46, 21:46, 22:46; Řevnice 10:33, 11:33, 12:33, 21:33, 22:33, 23:33). The morning peak shorts Praha-Radotín → Praha-Smíchov (5:40 to 8:10 every 30 min, and 13:30). Also Praha-Smíchov 12:34 → Praha-Radotín, the night Praha hl. n. 23:56 → Praha-Radotín, and Os 27740 Beroun 4:32 → Zadní Třebaň → Liteň.',
    '<b>S76 Liteňka:</b> the morning shorts Zadní Třebaň – Liteň (Zadní Třebaň 5:26, 5:56, 6:56, 7:33, 7:58; Liteň 5:11, 5:41, 6:41, 7:11, 7:46). Also the evening pair Zadní Třebaň 19:33 → Liteň and Liteň 20:11 → Zadní Třebaň, and Liteň 9:11 → Zadní Třebaň. The game runs the 2-hourly Lochovice trains all day.',
    '<b>Praha-Smíchov works (user 15 October 2026).</b> '
    + ('S6: Praha-Smíchov – Praha-Zlíchov is closed 1 July – 19 October 2026, 21:00, and every S6 train starts and ends at Praha-Zlíchov (no replacement; trams 5, 12, 15 and 94 Hlubočepy – Smíchovské nádraží). ' if S6_WORKS else
       'S6 is shown in its final state, from Praha-Smíchov after the works end on 19 October 2026, 21:00. Until then every S6 train starts and ends at the temporary stop Praha-Zlíchov (no replacement; trams 5, 12, 15 and 94 Hlubočepy – Smíchovské nádraží); S6 until 19 October gives that version in full. ')
    + 'S65 (modelled): Praha-Smíchov – Praha-Zličín is closed 13 August – 30 November 2026, and those trains are cancelled without replacement. '
    'Not modelled, as they last only days: the S7 and R16 works at Praha-Smíchov on 20 – 24 October, 25 – 27 October and 2 – 13 November, and the night closures there (PID).',
    '<b>S65:</b> the trains that turn at Hostivice, from Praha-Zličín during the works (Zličín 9:19, 13:19, 21:19; Hostivice 10:31, 13:31, 21:31), and the early and late ones (Hostivice 4:33 to Zličín; Zličín 4:55 and 6:44 to Rudná; Rudná 23:10 to Hostivice). Also S54 Os 19746 Praha-Zličín 7:04 → Hostivice → Noutonice (Kladno direction, outside this sheet).',
    '<b>S70 and Os Hořovice – Rokycany:</b> Os 7880 Beroun 4:21 → Zdice. Every other train on Beroun – Rokycany is one of the two lines in the game, whatever its real end beyond Rokycany.',
    '<b>Březnice – Rožmitál pod Třemšínem</b> (KJŘ 204): no workday trains. It runs only on weekends and public holidays, 25 April – 28 September 2026 (Březnice 8:17, 10:43, 14:17, 16:17; Rožmitál 8:57, 11:22, 15:22, 16:57), so it is not in the game (user, 13 October).',
    '<b>S60:</b> the early trains from or to Zdice (Zdice 4:36 → Strakonice, 6:04 → Blatná; Blatná 4:11 and Březnice 3:35 → Zdice) and the late Beroun 23:15 → Březnice. On Beroun – Zdice also Os 7703 Zdice 4:36 → Beroun → Rakovník (north of Beroun, outside this sheet).',
    '<b>S20 and S20 Čáslav:</b> the morning and evening trains outside the 2-hour pattern. From Kolín: 5:35 and 6:35 → Havlíčkův Brod, 7:03 → Čáslav, 7:30 → Kutná Hora hl. n., 9:35 → Žďár nad Sázavou, 11:35 → Jihlava město, 13:35 → Havlíčkův Brod, 20:34 and 23:59 → Čáslav. Towards Kolín: Havlíčkův Brod 5:05, 6:05, 9:05, 11:05, 14:05; Kutná Hora hl. n. 7:45; Čáslav 7:56, 21:01, 22:08. Also Čáslav 3:57 → Jihlava město, Čáslav 4:57 → Havlíčkův Brod and Havlíčkův Brod 22:23 → Čáslav.',
    '<b>Ex6 hours run by through trains:</b> four Ex6 slots a day are taken by trains that run through Praha once a day: SC / IC Pendolino 503 and 504 Ostrava – Karlovy Vary (from Praha 9:31 towards Ostrava, 18:35 towards Karlovy Vary) and rj 512 and 515 Ostravan Bohumín – Františkovy Lázně (10:35 and 17:31). In the game the two Ex6 lines run in those slots too. Ex 568 Plzeň – Cheb does not reach Rokycany.',
    '<b>Other trains, not part of this sheet:</b> Beroun – Rakovník (north of Beroun). On Kolín – Havlíčkův Brod: R9 Praha – Brno, the Sp Praha – Kutná Hora hl. n., the Os Kolín – Kutná Hora město / Zbraslavice (the 235 branch) and the branch Čáslav – Třemošnice. Světlá nad Sázavou – Havlíčkův Brod also has the 212 trains from Zruč nad Sázavou (in the archived Posázavský pacifik sheet).',
]
SHARED = {
    A_S7: [
        'S7 and S7 Řevnice share Praha-Smíchov – Řevnice. Towards Řevnice they leave Praha-Smíchov at :04 and :34 (S7 Řevnice) and at :23 and :53 (S7). Towards Praha they leave Řevnice at :13 and :43 (S7 Řevnice) and at :03 and :33 (S7). So the peak has a train about every 15 min, as in reality.',
        'S76 Liteňka meets S7 at Zadní Třebaň: in at L:20, out at S:32. S7 calls there towards Beroun at :23 and :53 and towards Praha at :29 and :59. At Lochovice it meets the Příbram line (S60 and R26).',
    ],
    A_SM: ([
        'Praha-Smíchov is being rebuilt, and neither line reaches it (modelled at your request, 15 October 2026). S6 starts and ends at the temporary stop Praha-Zlíchov until 19 October, 21:00. S65 runs only from Praha-Zličín until 30 November.',
        'S6 is one line for both branches: from Praha-Zlíchov at :18 (Nučice zastávka) and :48 (Beroun), so every 30 min to Nučice zastávka; back into Zlíchov at :08 (from Beroun) and :38 (from Nučice). Corrected 15 October: until now S6 and S6 Nučice were two lines from Praha-Smíchov. The shared line follows the real units (847 006 + 847 018 ran Os 19923 from Beroun and then Os 19968 to Nučice on 4 June 2026), and it is the only way to keep Praha-Zlíchov to one train.',
    ] if S6_WORKS else [
        'S6 is one line for both branches (your choice, 15 October 2026), shown twice. S6: the final state, back at Praha-Smíchov after the works (from 19 October 2026, 21:00): from Praha-Smíchov at :16 (Nučice zastávka) and :46 (Beroun), so every 30 min to Nučice zastávka; back into Smíchov at :11 (from Beroun) and :41 (from Nučice). The train turns in 5 min at Smíchov instead of 35, and S6 needs 4 vehicles instead of 5. S6 until 19 October: the same line and vehicles from the temporary stop Praha-Zlíchov (out :18 and :48, in :08 and :38), not counted again in the totals.',
        'S65 is still cut: Praha-Smíchov – Praha-Zličín stays closed until 30 November 2026, so S65 runs only from Praha-Zličín.',
    ]) + [
        'S65 runs Praha-Zličín – Hostivice – Rudná u Prahy and meets S6 only at Rudná u Prahy.',
    ],
    A_PL: [
        'Beroun – Zdice is shared by four lines. Towards Zdice: S60 L:01, R26 S:12, S70 S:14 and R16 at :52 every hour. R26 and S70 are 2 min apart, as in reality, and part at Zdice: R26 towards Příbram, S70 towards Hořovice.',
        'Hořovice – Rokycany has an Os every hour towards Hořovice: both lines leave Rokycany at :56 (S70 in the even hours, on to Beroun; the Hořovice Os in the odd hours). Towards Rokycany the Os leaves Hořovice at L:12 and S70 at S:36. R16 runs every hour on top.',
        'Rokycany is the end of the game\'s track. Trains stand there: R16 :26 – :33 every hour, S70 L:02 – S:56, the Hořovice Os L:38 – L:56, and since 15 October Ex6 :49 – :10 every hour (Cheb in the odd hours, München in the even ones). So up to three trains stand there at the same time, at L:49 – L:56 (S70, the Hořovice Os and Ex6 Cheb); the rest of the time at most two. Rokycany needs three platform tracks.',
        'Ex6 (every hour, Cheb and München trains alternating) runs Praha hl. n. – Rokycany without stopping. It passes the slower trains where they stand: R16 is ahead of it all the way (both directions), S70 is overtaken at Hořovice (timed there), and S7, S60 and R26 have left its track or are behind it. Towards Praha it follows the S7 Řevnice train by 3 min at Praha-Radotín, as in reality, then turns off towards Praha-Krč.',
        'Praha-Vysočany: an Ex6 stands there from :34 (Cheb) or :31 (München) until :22, so one platform track is taken almost all hour. The two lines never stand there together.',
    ],
    A_KH: [
        'Kolín → Čáslav has a train every hour at :34: S20 to Havlíčkův Brod in the even hours, S20 Čáslav in the odd hours. Towards Kolín S20 leaves Čáslav at S:01 and S20 Čáslav at S:58 (16:01, 16:58, 18:01, 18:58), so Čáslav → Kolín also has a train about every hour, as in the real workday timetable.',
        'Beyond Čáslav (Golčův Jeníkov, Světlá nad Sázavou, Havlíčkův Brod) there is an S20 every 2 h each way.',
    ],
    A_PB: [
        'S60 and R26 share Beroun – Zdice – Příbram – Březnice in alternate hours. From Beroun S60 leaves at L:01 and R26 at S:12. Towards Beroun R26 leaves Příbram at L:01 and S60 at S:08.',
        'Březnice – Čimelice has the Os (from Březnice S:16, from Čimelice L:20) and R26 (from Březnice L:19, from Čimelice S:21). At Březnice the Os connects with S60 both ways (3 min each way).',
        'Čimelice and Blatná are the ends of the game\'s track. At Čimelice the Os stands S:36 – L:20 and R26 L:35 – S:21, never at the same time, so one platform is enough. At Blatná only S60 turns (S:46 – L:11).',
    ],
}
HEAD = [
    '<title>Trains Beroun Plzeň Příbram</title>',
    '<h1>Trains west of Praha · S7 · Liteňka · S6 · S65 · Beroun – Rokycany · Příbram line · R16 · R26 · and S20 Kolín – Havlíčkův Brod</h1>',
    '<p class="muted">Simutrans design for the workday trains west and south-west of Praha: S7 Praha – Beroun, the Liteňka, ' + ('S6 (from Praha-Zlíchov) and S65 (from Praha-Zličín) during the Praha-Smíchov works' if S6_WORKS else 'S6 from Praha-Smíchov (final state, after the works end on 19 October) and S65 from Praha-Zličín (closed to Smíchov until 30 November)') + ', R16 and the Os Beroun – Rokycany, the Příbram line (Beroun – Příbram – Blatná, Březnice – Čimelice) and R26 Praha – Čimelice. '
    'Also, added on 10 October, S20 Kolín – Kutná Hora – Čáslav – Světlá nad Sázavou – Havlíčkův Brod: only these trains, each to its real terminus (Havlíčkův Brod or Čáslav), without the branch lines. '
    'West of Praha: not north of Beroun (no Rakovník line) and nothing east of the Vltava except the S7 and R terminus Praha hl. n. '
    'Times are real JR2026 times from the national CIS JŘ timetable, for trains that run on all five days Mon–Fri 5–9 October 2026. Unit types are from vagonweb.cz. '
    'PID labels (S6, S20, S60, S70, S76) come from the CIS line numbers.</p>',
    '<p class="small"><b>Changed 13 October 2026:</b> in the game the track ends at <b>Rokycany</b>, <b>Blatná</b> and <b>Čimelice</b>, so the lines that went further now end there, at their real minutes: '
    'R16 Praha – Rokycany (was Klatovy, 6 → 3 vehicles), S70 Beroun – Rokycany (was Přeštice, 2), Os Hořovice – Rokycany (was the Os/Sp chain via Plzeň to Přeštice, 3 → 1), '
    'S60 Beroun – Blatná (was Strakonice, 3 → 2), Os Březnice – Čimelice (was Protivín, 2 → 1) and R26 Praha – Čimelice (was České Budějovice, 5 → 4). '
    'Dropped, as they lie beyond the track: Os Rokycany – Příkosice (1) and Os Blatná – Strakonice (1). 43 → 33 vehicles. S7, Liteňka, S6, S65 and S20 are unchanged.</p>',
    '<p class="small"><b>Changed 15 October 2026 (your request): the Praha-Smíchov works.</b> '
    '<b>S6</b> starts and ends at the temporary stop <b>Praha-Zlíchov</b> (until 19 October, 21:00; ČD works timetable). The Beroun and Nučice trains are now one line, turning in 10 min at Zlíchov (5 → 4 vehicles). '
    '<b>S65</b> runs only <b>Praha-Zličín</b> – Hostivice – Rudná u Prahy (Smíchov – Zličín closed until 30 November; 3 → 2 vehicles). '
    'Every S6 and S65 time on the sheet matches the PID feed, and the build checks that Praha-Zlíchov holds one train at a time (see the S6 area notes). 33 → 31 vehicles.</p>',
    '<p class="small"><b>Changed 15 October 2026, later (your request): the final S6.</b> S6 is shown as it runs after the works, from <b>Praha-Smíchov</b> again (from 19 October, 21:00), and stays one combined line: it turns in <b>5 min</b> at Smíchov (in :11 → out :16, in :41 → out :46) instead of 35 min on two separate lines. Still 4 vehicles. The Zlíchov version for the days until then went into the S6 notes (now its own section, below). S65 is unchanged (Praha-Zličín until 30 November). 31 vehicles.</p>'
    '<p class="small"><b>Changed 15 October 2026, later still (your question):</b> the Zlíchov S6 for the days until 19 October now has its own full section, <a href="#s6z">S6 until 19 October</a>, with its entries and round trip, next to the final S6. It uses the same 4 vehicles as S6, so the total stays 31.</p>'
    if not S6_WORKS else '',
    '<p class="small"><b>Changed 15 October 2026 (your request): Ex6 to Rokycany.</b> Two lines every 2 h, together a train every hour, at their real minutes: <a href="#ex6c">Ex6 Cheb</a> (IC Západní expres) and <a href="#ex6m">Ex6 München</a> (EC / alex), each from Praha-Vysočany via Praha hl. n. to Rokycany, where the game\'s track ends (2 + 2 vehicles). S70 is now timed at Hořovice, where Ex6 overtakes it. Rokycany then holds up to three trains. 31 → 35 vehicles.</p>',
    '<p>Notation: <b>L</b> = odd hours, <b>S</b> = even hours. Every 120: offset = minute for odd hours (L:01 → 1) and minute + 60 for even hours (S:14 → 74). Every 60: the offset is the minute of every hour. Every 30: the offset is the minute of the first departure in each half hour (16 means :16 and :46). (x) = request stop. '
    '<span class="wait">Highlighted</span> rows are timed stops with a longer stay. "Leave up to" is 30 min on every entry of the lines every 120 and automatic on the lines every 60 and 30.</p>',
]


def track_checks():
    """one train at a time at the Praha ends of S6 and S65 (user, 15 Oct 2026); stops the build on a clash"""
    by_num, wd = load()
    lines = [base.build_line(L, by_num, wd) for L in LINES]
    out, bad = [], []
    checks = [(ZL, None, 'Praha-Zlíchov'), (ZL, HL, 'The track Praha-Hlubočepy – Praha-Zlíchov and back')]  # S6 until 19 October
    for station, before, what in checks + [(ZC, None, 'Praha-Zličín')]:
        win, clash = one_at_a_time(lines, station, before)
        print(f'one train at a time on {what}:', 'OK' if not clash else 'CLASH')
        for a, d, ln, num in win:
            print(f'   {base.hm(a)} – {base.hm(d)}  {ln} ({num})')
        for p, q in clash:
            print(f'   CLASH {base.hm(p[0])}–{base.hm(p[1])} {p[2]} with {base.hm(q[0])}–{base.hm(q[1])} {q[2]}')
        bad += clash
        occ = '; '.join(f'{base.mm(a)} – {base.mm(d)}' for a, d, _, _ in sorted({(a % 60, d % 60 + (60 if d % 60 < a % 60 else 0), ln, '') for a, d, ln, _ in win}))
        out.append(f'{what}: {occ} every hour')
    if bad:
        sys.exit('more than one train at a time at the Praha end of S6 or S65')
    return out


def ex6_real():
    """the real workday trains of the Ex6 lines: the Rokycany copies, Cheb trains (IC 55x / 56x) and München trains (35x)"""
    by_num = load()[0]
    ends = lambda r: (r['stops'][0]['name'], r['stops'][-1]['name'])
    for L in LINES:
        if L['id'] not in ('ex6c', 'ex6m'):
            continue
        pre = ('55', '56') if L['id'] == 'ex6c' else ('35', '36')  # the once-a-day through trains (50x, 51x) are not Ex6 lines
        mine = [(k, c) for k, c in RCOPIES if c['num'][:2] in pre]
        # by direction; a train that starts or ends at Praha hl. n. instead of Praha-Vysočany is listed with its real end
        L['extra_real'] = {by_num[n]['num']: [k for k, c in mine if (ends(c)[-1] == 'Rokycany') == (ends(by_num[n])[-1] == 'Rokycany')]
                           for n in L['legs']}


def s6z_real():
    """the real workday trains of S6 until 19 October: the Zlíchov copies, by leg"""
    load()
    L = next((L for L in LINES if L['id'] == 's6z'), None)
    if L is None:
        return
    ends = lambda r: (r['stops'][0]['name'], r['stops'][-1]['name'])
    by = {}
    for key, c in ZCOPIES:
        by.setdefault(ends(c), []).append(key)
    by_num = load()[0]
    L['extra_real'] = {by_num[n]['num']: by.get(ends(by_num[n]), []) for n in L['legs']}  # build_line keys it by the leg's number


if __name__ == '__main__':
    ex6_real()
    s6z_real()
    occ = track_checks()
    SHARED[A_SM] = SHARED[A_SM] + ['One train at a time, checked by the build over the whole afternoon (13:00 – 16:59, every line of the sheet): ' + '. '.join(occ) + '. No two of these ever overlap.']
    base.run(LINES, OUT, LISTED, along=True, inv_svcs=LOCAL, head=HEAD, shared=SHARED, not_modelled=NOT_MODELLED)
