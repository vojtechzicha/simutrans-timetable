"""Trains from S4 to the S3 corridor: the lines that the game does not have yet (user, 14 Oct 2026: "finish all pid
trains and related branch lines with what's missing (it should be the S4 - S3 corridor but some might have slipped
up. The main tracks are built all the way to Usti (so include even some fast trains on the corridor to usti)").

Scope (user answers, 14 Oct 2026):
- The game's lines come from the save (export by the pak128 session, FORK-CZR-VZ.sve 19:44): S3, S30, S34, R43, R21,
  S35 and the whole east sector already run there, so they are not on this sheet. Missing: S4, S43, S32, S23 and the
  fast trains to Ústí.
- Fast trains: R20, Ex5 (EC Praha – Dresden) and R15 only "in praha-usti sense" (cut at Ústí nad Labem hl. n.), R23
  Kolín – Mělník – Ústí "in full". "R20, R5/Ex5 should definitely go to Praha jih": both run from and to the depot
  Praha Jih on the real empty-run minutes.
- Track built: Mělník – Štětí – Ústí západ, Neratovice – Všetaty – Mladá Boleslav, Mělník – Mšeno. Not built: the
  Lovosice branches. S23 in; S22 "only if they actually have any trains" (none in the afternoon: not modelled); S27 out.
Engineering works: S4 starts and ends at Praha-Bubny while Masarykovo nádraží is closed (1 June – 12 December 2026,
PID), at its annual Bubny minutes, as on the S5 sheet. Everything else on these lines is short (listed).
Ex5 data: the EC trains run Tue–Fri under one record and on Mondays under another (Monday works, ending at Děčín) with
the same minutes Praha – Ústí, so load() merges them into one workday train.
Designed 14 Oct 2026 with ../rail-design-rules.md and build_012_014_235.py (real JR2026 CIS JŘ times, trains that run
on all five days Mon–Fri 5–9 Oct 2026). Writes "Trains S4 to S3.html" in the project root.
Run: python pipeline/local-rail/build_s4.py
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_012_014_235 as base  # noqa: E402

base.FULL.update({'Kralupy n.V.': 'Kralupy nad Vltavou', 'Praha Masaryk. n.': 'Praha Masarykovo nádraží',
                  'Ústí n. L. hl. n.': 'Ústí nad Labem hl. n.', 'Ústí n.L. západ': 'Ústí nad Labem západ',
                  'Ústí n.L.-Střekov': 'Ústí nad Labem-Střekov', 'Litoměřice hor.n.': 'Litoměřice horní nádraží'})
base.DEPOTS.add('Praha Jih')

OUT = os.path.join(base.ROOT, 'Trains S4 to S3.html')
PB, PH, KR, UL, UZ = 'Praha-Bubny', 'Praha hl. n.', 'Kralupy nad Vltavou', 'Ústí nad Labem hl. n.', 'Ústí nad Labem západ'
JIH = 'Praha Jih'
# depot runs that CIS JŘ does not have (user, 14 Oct 2026: "R15 should go to Praha jih"; "Usti also can store trains
# at its depot run (11 minutes)"; then "R23 in reality goes back to západ to stable then returns to hl.n."). R15 uses the minutes of the real Ex5 runs, which have the same Praha hl. n. minutes
# in the other hours (from the depot :06 -> :15, out :31; in :25, to the depot :42 -> :51).
R15_D1, R15_D2 = 'empty R15 Praha Jih – Praha hl. n.', 'empty R15 Praha hl. n. – Praha Jih'
R23_D1, R23_D2 = 'empty R23 Ústí nad Labem hl. n. – Ústí nad Labem západ', 'empty R23 Ústí nad Labem západ – Ústí nad Labem hl. n.'
DEPOT_RUNS = [(R15_D1, JIH, 13 * 60 + 6, PH, 13 * 60 + 15), (R15_D2, PH, 16 * 60 + 42, JIH, 16 * 60 + 51),
              (R23_D1, UL, 15 * 60 + 31, UZ, 15 * 60 + 34), (R23_D2, UZ, 16 * 60 + 20, UL, 16 * 60 + 23)]
EX5 = ['170', '171', '172', '173', '174', '175', '176', '177', '178', '179', '382', '383', '384', '385', '458', '459']
_load = base.load


def load():
    """the real data, plus the EC Praha – Dresden trains whose Monday variant (to Děčín) has the same minutes on
    Praha-Holešovice – Ústí nad Labem hl. n. as the Tue–Fri one: merged into one workday train"""
    by_num, wd = _load()
    T = json.load(open(base.TRAINS, encoding='utf-8'))
    var = {}
    for t in T:
        st = [l for l in t['locs'] if base.PA & set(l['act'])]
        if st and st[0]['num'] in EX5:
            days = {d for d in base.WEEK if base.runs(t, d)}
            if days:
                var.setdefault(st[0]['num'], []).append((days, t, st))
    for num, vs in var.items():
        if any(len(d) == 5 for d, _, _ in vs):
            continue
        if set().union(*(d for d, _, _ in vs)) != set(base.WEEK):
            continue

        def seg(st):
            nm = [base.full(l['name']) for l in st]
            if 'Praha-Holešovice' not in nm or UL not in nm:
                return None
            a, b = sorted((nm.index('Praha-Holešovice'), nm.index(UL)))
            return [(nm[i], st[i].get('arr') if i > a else None, st[i].get('dep') if i < b else None) for i in range(a, b + 1)]
        segs = [seg(st) for _, _, st in vs]
        if None in segs or any(s_ != segs[0] for s_ in segs):
            print('Ex5 variants not merged:', num)
            continue
        days, t, st = max(vs, key=lambda v: len(v[0]))
        rec = {'num': num, 'svc': st[0]['svc'], 'all5': True, 'raw': t['locs'],
               'stops': [{'name': base.full(l['name']), 'arr': l.get('arr'), 'dep': l.get('dep'), 'req': '0030' in l['act']} for l in st]}
        rec['stops'][0]['arr'] = None
        rec['stops'][-1]['dep'] = None
        by_num[num] = rec
        wd.append(rec)
    for num, a, t0, b, t1 in DEPOT_RUNS:
        by_num[num] = {'num': num, 'svc': None, 'all5': True, 'depot': True, 'raw': [],
                       'stops': [{'name': a, 'arr': None, 'dep': t0, 'req': False}, {'name': b, 'arr': t1, 'dep': None, 'req': False}]}
    return by_num, wd


base.load = load
IMP = 'important station'
TP = 'timing point, waits for its real minute'
CROSS = 'crossing with the train the other way'
A_S4 = 'Praha – Kralupy – Ústí nad Labem (S4 and the fast trains)'
A_LB = 'Kolín / Lysá – Mělník – Ústí nad Labem západ (right bank of the Labe)'
A_NR = 'Kralupy – Neratovice – Čelákovice'
R20_OUT, R20_IN = f'684 {PH} – {UL}', f'685 {UL} – {PH}'
EX_OUT, EX_IN = f'176 {PH} – {UL}', f'173 {UL} – {PH}'

LINES = [
    # --- S4 and the fast trains -------------------------------------------------------------------------------------
    {
        'id': 's4', 'name': 'S4', 'area': A_S4, 'svc': '1004', 'every': 60,
        'legs': [{'cut': ('9636', PB, KR)}, {'cut': ('9635', KR, PB)}], 'cut_at': [PB],
        'wait_points': {},
        'notes': [
            'PID S4 Praha – Roztoky u Prahy – Kralupy nad Vltavou (KJŘ 091), the trains that end at Kralupy. Masarykovo nádraží is closed from 1 June to 12 December 2026 (PID: S4, S5, S54, R24 and R45 start and end at Praha-Bubny), so the line runs from Praha-Bubny at its annual minutes there: every hour from Praha-Bubny at :14 (Kralupy :45) and from Kralupy at :12 (Praha-Bubny :42).',
            'With S4 Ústí (:44 from Bubny, :42 from Kralupy) this is the real half-hourly S4 Praha – Kralupy.',
            'Two vehicles. 27 min at Kralupy (in :45, out :12) and 32 min at Praha-Bubny (in :42, out :14): the real minutes.',
            'The ČD works timetable for the closure (cz-k120-2026vyluka03) says that all S4 trains start and end at Praha-Bubny, but it prints times only for the Kladno line. So the S4 Bubny minutes here are the annual ones; on S5 the works timetable kept the annual Bubny minutes too.',
            '<b>Corrected 14 October (v2):</b> Praha-Bubny holds at most two trains at a time, not four or five as v1 said. Counted minute by minute over 2 h with S5, R45 and R24 from the S5 sheet: S4 and S4 Ústí together at :12 – :14 and :42 – :44, S4 Ústí and S5 at :16 – :34, S4 with R45 or R24 at :48 – :03. A station with four platform tracks is enough. The S4 Ústí second unit (below) stands coupled on the same track.',
            'Vehicles: ČD 471 CityElefant (vagonweb 2026, Os 9636: 471 + 071 + 971).',
        ],
    },
    {
        'id': 's4u', 'name': 'S4 Ústí', 'area': A_S4, 'svc': ['1004', '4004'], 'every': 60,
        'legs': [{'cut': ('6918', PB, UL)}, {'cut': ('6917', UL, PB)}], 'cut_at': [PB],
        # timing points (user, 15 Oct 2026: in the game the train reached Lovosice 21 min and Kralupy 36 min before its
        # departure there); real minutes, only where no faster train follows closely (see the notes)
        'wait_points': {('out', 'Lovosice'): IMP, ('in', 'Lovosice'): IMP,
                        ('out', 'Nelahozeves'): TP, ('out', 'Vraňany'): TP, ('out', 'Hněvice'): TP, ('out', 'Roudnice nad Labem'): TP,
                        ('in', 'Bohušovice nad Ohří'): TP, ('in', 'Roudnice nad Labem'): TP, ('in', 'Hněvice'): TP,
                        ('in', 'Vraňany'): TP, ('in', 'Nelahozeves'): TP},
        'notes': [
            'The S4 trains that run through to Ústí nad Labem (KJŘ 090; CIS 1004 out of Praha, 4004 from Ústí, U4 in the Ústí region). Every hour from Praha-Bubny at :44 (Kralupy :15 – :23, Roudnice nad Labem :02 – :03, Lovosice :24 – :29, Ústí nad Labem hl. n. :51) and from Ústí at :05 (Lovosice :27 – :31, Roudnice :51 – :52, Kralupy :33 – :42, Praha-Bubny :12).',
            'Kralupy is timed both ways (8 and 9 min: R20 overtakes there), and Lovosice as the important station (junction, 5 and 4 min).',
            '<b>Timing points (added 15 October, your report from the game):</b> the game train runs Kralupy – Lovosice – Ústí much faster than the real one with its 21 stops, so it reached Lovosice 21 min and Kralupy 36 min before its departure there. The departures are certain: every S4 Ústí train of the day leaves Ústí nad Labem hl. n. at :05 and Lovosice at :31 towards Praha, and Lovosice at :29 towards Ústí (CIS JŘ; the only works on the line are single days). So the line now also waits for its real minute at stations in the middle. Towards Ústí: Nelahozeves :30, Vraňany :38, Hněvice :53, Roudnice nad Labem :03. Towards Praha: Bohušovice nad Ohří :39, Roudnice nad Labem :52, Hněvice :02, Vraňany :17, Nelahozeves :25. All are stations with more than one track.',
            'Why these and not more: a waiting S4 must never be in the way of a faster train. Towards Ústí, R15 or Ex5 (every hour between them, not timed before Ústí) passes Kralupy at :01, 38 min after S4, and overtakes it at Lovosice (S4 :24 – :29, R15 / Ex5 through at :27). As both run faster in the game, the last timing point before Lovosice is Roudnice (S4 out :03, R15 / Ex5 through at :20 in reality). Bohušovice (:16, the fast train at :25) would be too close. R20 is ahead of S4 all the way. Towards Praha, R15 / Ex5 overtakes S4 at Lovosice and is then ahead. R20 leaves Lovosice 26 min after S4 (timed :57) and overtakes it at Kralupy (S4 :33 – :42, R20 :38 – :40); at Vraňany it passes 12 min and at Nelahozeves 8 min after S4 leaves, and it has slack to Kralupy anyway.',
            'Five vehicles. 14 min at Ústí nad Labem hl. n. (in :51, out :05) and 32 min at Praha-Bubny (in :12, out :44): the real minutes.',
            'Vehicles: one ČD 640.2 RegioPanter (vagonweb 2026, Os 6918 and Os 6917). In the afternoon peak the real trains run two units between Praha and Kralupy; the second unit is the coupled line S4 Ústí 2nd unit. This line is its primary and carries no coupling setting.',
        ],
    },
    {
        'id': 's4k', 'name': 'S4 Ústí 2nd unit', 'area': A_S4, 'svc': ['1004', '4004'], 'every': 60, 'couple_with': 'S4 Ústí',
        'legs': [{'cut': ('6918', PB, KR)}, {'cut': ('6917', KR, PB)}], 'cut_at': [PB, KR],
        'couple': {('out', PB): ('S4 Ústí', 5), ('in', KR): ('S4 Ústí', 10)},
        'wait_points': {},
        'notes': [
            'The second RegioPanter of the S4 Ústí trains between Praha and Kralupy, as on the real workday afternoon trains (vagonweb 2026: Os 6916, 6918, 6920, 6922, 6924 from Praha run 640.2 Praha – Ústí plus 640.2 Praha – Kralupy; Os 6917, 6919, 6921, 6923 back run 640.2 Kralupy – Praha plus 640.2 Ústí – Praha). Your idea (14 October): use the fork coupling at Kralupy.',
            'How it works in the game (fork coupling, rail): this line is the joining train, S4 Ústí the primary. Its Praha-Bubny entry and its Kralupy entry towards Praha say "Couple with S4 Ústí, wait up to 5 / 10 min". From Bubny at :44 the pair runs coupled; at Kralupy (in :15) the schedules part, because S4 Ústí goes on to Nelahozeves zámek and this line turns back. S4 Ústí leaves at :23; this unit stands at Kralupy until the next S4 Ústí from Ústí comes in at :33, couples, and the pair leaves at :42. At Bubny (in :12) both schedules go on to the same next stop, Praha-Podbaba, so the pair stays coupled through the turn and leaves together at :44.',
            'Two vehicles (2 h ÷ 1 h): 31 min to Kralupy, 27 min at Kralupy, 30 min back, 32 min at Bubny coupled. Both lines have the same slots on the coupled part (Bubny :44, Kralupy :42).',
            '<b>Required for the coupling (engine session simutrans-122-0-36, from simconvoi.cc, 14 October):</b> this line must list exactly the same stops as S4 Ústí between Bubny and Kralupy, both ways and in the same order: Praha-Bubny, Praha-Podbaba, Praha-Sedlec, Roztoky u Prahy, Roztoky-Žalov, Úholičky, Řež, Libčice nad Vltavou-Letky, Libčice nad Vltavou, Dolany nad Vltavou, Kralupy nad Vltavou, and back the same way. Two trains couple only when their next stop is the same, and a coupled pair parts at any stop the joining train skips or where its next stop differs. A two-entry Bubny – Kralupy schedule would never couple, and would part at Podbaba. The coupling setting goes only on the Bubny entry (:44, wait up to 5) and the Kralupy entry towards Praha (:42, wait up to 10); the other entries have none. Keep the Bubny :44 and Kralupy :42 offsets identical on both lines.',
            'Platforms: a train looking for a platform at a coupling stop counts its partner too, so Praha-Bubny and the Kralupy platform where the pair couples must hold both RegioPanters. At the stops in between a short platform only leaves the rear standing off it.',
            '<b>Tested by the engine session (14 October, test layout with these exact offsets, 3 × S4 Ústí + 2 units):</b> it works with the real minutes. Every hour the pair leaves Bubny :44, parts at Kralupy (S4 Ústí on at :23), the unit couples with the next S4 Ústí from Ústí, a different train, and the pair leaves :42 and stays coupled through the Bubny turn. Save / load while the unit waits is fine. An engine fix for a late S4 Ústí (it waited 10 more min for a unit that had already left, and left a stale missed-coupling slot) is committed on the engine main branch (cc6f047). It is not installed yet, so install it before building this.',
            'Kralupy platform room: the outbound pair stops with its front at the platform end, so after S4 Ústí leaves, the room in front of the unit is exactly one S4 Ústí long. In the test that was not enough, so the inbound S4 Ústí took another track, and the engine moved the unit across behind it. The coupling is still on time; the jump across is cosmetic. For a real same-track coupling, give the Kralupy platform about one tile of slack beyond one 640.2 at the Ústí end. Otherwise make sure the platform the inbound S4 Ústí uses holds both units.',
            'Why not use the coupling to run the S4 trains to Kralupy as well, saving a vehicle: the fork parts a pair only where the two schedules go on to different next stops. S4 and S4 Ústí stop at exactly the same stations between Bubny and Kralupy, so a unit coupled in at Bubny could never leave for the :14 S4 on its own. The S4 trains also are 471 CityElefant, not RegioPanter.',
            'Vehicles: ČD 640.2 RegioPanter (vagonweb 2026). In pak128.cs 640.2 + 640.2 couple by line coupling (the coupling ignores vehicle constraints; pak128 session, 14 October).',

        ],
    },
    {
        'id': 'r20', 'name': 'R20', 'area': A_S4, 'svc': '20', 'every': 60, 'cat': 'R', 'inv_svcs': {'20'},
        # user, 14 Oct 2026: "R20, R5/Ex5 should definitely go to Praha jih"
        'legs': [{'raw': ('684', JIH, PH), 'route': [JIH, PH], 'name': ''},
                 {'cut': ('684', PH, UL)}, {'cut': ('685', UL, PH)},
                 {'raw': ('695', PH, JIH), 'route': [PH, JIH], 'name': ''}],
        'cut_at': [UL],
        'wait_points': {(R20_OUT, KR): IMP, (R20_IN, KR): IMP, (R20_OUT, 'Lovosice'): IMP, (R20_IN, 'Lovosice'): IMP},
        'notes': [
            'R20 Praha hl. n. – Kralupy – Roudnice – Lovosice – Ústí nad Labem, cut at Ústí nad Labem hl. n., where the game\'s main track ends. In reality it runs on to Děčín. Every hour from Praha hl. n. at :47 (Kralupy :17 – :19, Lovosice :57 – :59, Ústí :14) and from Ústí at :42 (Lovosice :56 – :57, Kralupy :38 – :40, Praha hl. n. :10).',
            'Depot Praha Jih (your call, 14 October), the same depot the R9 / R19 sheet calls Praha odstavné nádraží, so use the depot halt that is already in the game: the line runs from and to the depot on the real empty-run minutes. R 684 comes from Praha Jih (out 14:28, Praha hl. n. 14:37, leaves 14:47); R 695 goes there after Praha hl. n. (in 20:10, out 20:27, Praha Jih 20:35). Praha hl. n. is timed both ways.',
            'Five vehicles. 28 min at Ústí nad Labem hl. n. (in :14, out :42) and 53 min in the depot (in :35, out :28). Turning at Praha hl. n. instead (in :10, out :47) would need 4.',
            'Timed as important stations: Kralupy nad Vltavou and Lovosice, both ways.',
            'Vehicles: R20 "Labe", a ČD 162 locomotive with five push-pull coaches (Bfhpvee driving coach, Aee, Bee, Bpee; vagonweb 2026, R 686 and R 685).',
        ],
    },
    {
        'id': 'ex5', 'name': 'Ex5', 'area': A_S4, 'svc': ['5', None], 'every': 120, 'cat': 'rj', 'inv_svcs': {'5', None},
        'legs': [{'raw': ('176', JIH, PH), 'route': [JIH, PH], 'name': ''},
                 {'cut': ('176', PH, UL)}, {'cut': ('173', UL, PH)},
                 {'raw': ('173', PH, JIH), 'route': [PH, JIH], 'name': ''}],
        'cut_at': [UL, PH],
        'wait_points': {},
        'notes': [
            'Ex5, the ČD railjet "Berliner" Praha – Dresden – Berlin (– Hamburg, Kiel), cut at Ústí nad Labem hl. n., where the game\'s main track ends. Every 2 h from Praha hl. n. at S:31 (Praha-Holešovice S:39 – S:41, Ústí L:41) and from Ústí at S:13 (in from Dresden at :11; Praha-Holešovice L:15 – L:17, Praha hl. n. L:25). It runs non-stop between Praha-Holešovice and Ústí.',
            'Depot Praha Jih (your call, 14 October), the same depot as R20 (Praha odstavné nádraží on the R9 / R19 sheet), on the real empty-run minutes: EC 176 comes from Praha Jih (out 12:06, Praha hl. n. 12:15, leaves 12:31); EC 173 goes there after Praha hl. n. (in 13:25, out 13:42, Praha Jih 13:51).',
            'Two vehicles (4 h ÷ 2 h). 32 min at Ústí (in L:41, out S:13) and 15 min in the depot (in L:51, out S:06).',
            'Some EC run through Praha to and from Kúty or Břeclav and call only at Praha-Holešovice (EC 174 Holešovice 14:41, EC 175 and EC 177 Holešovice L:15); their Ústí minutes are the same, and in the game they start and end at Praha hl. n. like the others.',
            'Data note: on Mondays these trains run under a separate record (works in Germany, ending at Děčín) with the same Praha – Ústí minutes; the script merges the two.',
            'Vehicles: a ČD 193 Vectron with nine ČD ComfortJet coaches (Bdmpz, Bmpz, Bbmpz, BRmpz, Ampz, Afmpz; the ČD 384 takes over once approved; vagonweb 2026, rj 176 and rj 173).',
        ],
    },
    {
        'id': 'r15', 'name': 'R15', 'area': A_S4, 'svc': '15', 'every': 120, 'cat': 'R', 'inv_svcs': {'15'},
        'legs': [R15_D1, {'cut': ('610', PH, UL)}, {'cut': ('613', UL, PH)}, R15_D2], 'cut_at': [UL],
        'wait_points': {},
        'notes': [
            'R15 "Krušnohor" Praha hl. n. – Ústí nad Labem (– Most – Chomutov – Karlovy Vary – Cheb), cut at Ústí nad Labem hl. n. Every 2 h from Praha hl. n. at L:31 (Praha-Holešovice L:39 – L:41, Ústí S:42) and from Ústí at L:14 (Praha-Holešovice S:14 – S:17, Praha hl. n. S:25), non-stop between Holešovice and Ústí.',
            'Depot Praha Jih (your call, 14 October): "R15 should go to Praha jih". CIS JŘ has no empty runs for R15, so the depot runs copy the real Ex5 runs, which have the same Praha hl. n. minutes in the other hours: from Praha Jih at L:06 (Praha hl. n. L:15, out L:31) and after Praha hl. n. (in S:25, out S:42, Praha Jih S:51). These depot minutes are not real R15 minutes. Praha hl. n. is timed both ways.',
            'Two vehicles, as before (4 h ÷ 2 h). 32 min at Ústí (in S:42, out L:14) and 15 min in the depot (in S:51, out L:06), instead of 66 min at Praha hl. n.',
            'Vehicles: a RAILL 193 Vectron with ČD InterJet coaches (vagonweb 2026, R 610: Bdmpz, Bmpz, Bbmpz, Ampz).',
        ],
    },
    # --- right bank of the Labe -----------------------------------------------------------------------------------
    {
        'id': 'r23', 'name': 'R23', 'area': A_LB, 'svc': '23', 'every': 120, 'cat': 'R', 'inv_svcs': {'23'},
        'legs': ['1306', R23_D1, R23_D2, '1311'],
        'wait_points': {('1306', 'Nymburk hl. n.'): IMP, ('1311', 'Nymburk hl. n.'): IMP, ('1306', 'Mělník'): IMP,
                        ('1311', 'Mělník'): IMP, ('1306', UZ): IMP, ('1311', UZ): IMP},
        'notes': [
            'R23 (RegioJet) Kolín – Nymburk – Lysá nad Labem – Všetaty – Mělník – Štětí – Litoměřice město – Ústí nad Labem západ – Ústí nad Labem hl. n., in full (your call). Every 2 h from Kolín at L:20 (Nymburk L:41 – L:45, Mělník S:22 – S:24, Ústí západ L:14 – L:18, Ústí hl. n. L:21) and from Ústí hl. n. at S:33 (Ústí západ S:36 – S:40, Mělník L:31 – L:32, Nymburk S:10 – S:12, Kolín S:36).',
            'Three vehicles (6 h ÷ 2 h). Between its arrival and departure at Ústí nad Labem hl. n. (in L:21, out S:33, 72 min) the real train goes back empty to Ústí nad Labem západ and stands there (your note, 14 October). In the game: in L:21, 10 min, empty out L:31, Ústí západ L:34 (3 min, the train\'s own running time); stabled 46 min; empty out S:20, Ústí hl. n. S:23, 10 min, out S:33. CIS JŘ has no empty runs, so these minutes are a design. The empty entries at Ústí západ should take no passengers (stop type all off / no loading), as the R18 depot entries do.',
            'Ústí nad Labem západ while R23 stands there (L:34 – S:20): S32 also turns there (in L:52, out S:03), so two trains stand at Ústí západ L:52 – S:03.',
            '44 min at Kolín (in S:36, out L:20): the real minutes.',
            'Timed as important stations: Nymburk hl. n., Mělník and Ústí nad Labem západ, both ways.',
            'Vehicles: RegioJet 665, a six-car electric unit (vagonweb 2026, R 1306 and R 1311, operator RJ).',
        ],
    },
    {
        'id': 's32', 'name': 'S32', 'area': A_LB, 'svc': ['1032', '4032'], 'every': 120,
        'rep_out': '6412', 'rep_in': '6413',
        'wait_points': {('out', 'Mělník'): IMP, ('in', 'Mělník'): IMP},
        'notes': [
            'PID S32 Lysá nad Labem – Všetaty – Mělník – Štětí – Litoměřice město – Ústí nad Labem západ (KJŘ 072; CIS 1032 out of Lysá, 4032 back, U32 in the Ústí region). Every 2 h from Lysá at S:18 (Mělník S:51 – S:52, Štětí L:04 – L:05, Ústí západ L:52) and from Ústí nad Labem západ at S:03 (Štětí S:50 – S:51, Mělník L:03 – L:04, Lysá L:37).',
            'Two vehicles. 11 min at Ústí nad Labem západ (in L:52, out S:03) and 41 min at Lysá nad Labem (in L:37, out S:18): the real minutes.',
            'Vehicles: a ČD 162 locomotive with three push-pull coaches (two Bdmtee double-deck coaches and a Bfhpvee driving coach); from 1 July 2026 a ČD 362 instead of the 162 on some trains (vagonweb 2026, Os 6412 and Os 6413).',
        ],
    },
    {
        'id': 'u32', 'name': 'U32 Štětí', 'area': A_LB, 'svc': '4032', 'every': 120,
        'rep_out': '6457', 'rep_in': '6458',
        'wait_points': {},
        'notes': [
            'The Ústí region trains Ústí nad Labem západ – Litoměřice město – Štětí (CIS 4032), in the hours between S32: from Ústí západ at L:03 (Litoměřice město L:29 – L:30, Štětí L:51) and from Štětí at S:04 (Litoměřice město S:25 – S:26, Ústí západ S:52). With S32 this gives Ústí západ – Štětí a train every hour.',
            'One vehicle. 13 min at Štětí (in L:51, out S:04) and 11 min at Ústí nad Labem západ (in S:52, out L:03).',
            'Vehicles: the same ČD 162 push-pull set as S32 (two Bdmtee and a Bfhpvee; vagonweb 2026, Os 6457 and Os 6458).',
        ],
    },
    # --- Kralupy – Neratovice – Čelákovice --------------------------------------------------------------------------
    {
        'id': 's43', 'name': 'S43', 'area': A_NR, 'svc': '1043', 'every': 60,
        'rep_out': '19521', 'rep_in': '19520', 'turns': [8, 5],  # Neratovice: in :51, out :59; Kralupy: in :22, out :27
        'wait_points': {},
        'notes': [
            'PID S43 Kralupy nad Vltavou – Neratovice (KJŘ 092). Every hour from Kralupy at :27 (Neratovice :51) and from Neratovice at :59 (Kralupy :22).',
            'One vehicle. 8 min at Neratovice and 5 min at Kralupy: the real minutes. With the usual 10-min turns it would need 2.',
            'Vehicles: ČD 810 (vagonweb 2026, Os 19521; 810 620 and 810 341 seen).',
        ],
    },
    {
        'id': 's23', 'name': 'S23', 'area': A_NR, 'svc': '1023', 'every': 60,
        'rep_out': '19420', 'rep_in': '19423', 'turns': [9, 10],  # Neratovice: in :25, out :34
        'wait_points': {('in', 'Brandýs nad Labem'): CROSS},
        'notes': [
            'PID S23 Čelákovice – Brandýs nad Labem – Neratovice (KJŘ 074). Every hour from Čelákovice at :36 (Brandýs :53 – :00, Neratovice :25) and from Neratovice at :34 (Brandýs :58 – :01, Čelákovice :18).',
            'The trains cross at Brandýs nad Labem every hour: towards Neratovice it waits 7 min, towards Čelákovice 3 min (timed as the crossing).',
            'Two vehicles. 9 min at Neratovice (in :25, out :34) and 18 min at Čelákovice (in :18, out :36): the real minutes.',
            'Vehicles: ČD 810 (vagonweb 2026, Os 19420; 810 570 and 810 585 seen).',
        ],
    },
]

LISTED = {
    ('Praha-Podbaba', KR), (KR, 'Praha-Podbaba'), ('Praha-Podbaba', UL), (UL, 'Praha-Holešovice'), ('Praha-Holešovice', UL),
    (UL, 'Roudnice nad Labem'), ('Roudnice nad Labem', UL), ('Lovosice', UL), (UL, 'Lovosice'), ('Roudnice nad Labem', PB),
    (KR, UL), ('Lovosice', 'Hněvice'), ('Hněvice', UL), (KR, 'Vraňany'), ('Vraňany', KR), (KR, 'Roudnice nad Labem'),
    ('Roudnice nad Labem', KR), (PB, 'Vraňany'),
    ('Litoměřice město', UZ), (UZ, 'Litoměřice město'), (UZ, 'Mělník'), ('Mělník', 'Lysá nad Labem'), ('Mělník', UZ),
    ('Ústí nad Labem-Střekov', 'Litoměřice město'),
    ('Brandýs nad Labem', 'Čelákovice'), ('Čelákovice', 'Brandýs nad Labem'), ('Brandýs nad Labem', 'Neratovice'),
    ('Neratovice', 'Brandýs nad Labem'),
}
NOT_MODELLED = [
    '<b>Note on Praha times below:</b> they are the annual times. While Masarykovo nádraží is closed (until 12 December 2026), the S4 trains listed "from Praha Masarykovo nádraží" start and end at Praha-Bubny instead.',
    '<b>Engineering works (checked 14 October 2026):</b> only the Masarykovo closure is long-term, and it is modelled (S4 at Praha-Bubny). Short ones, not modelled: S4 Roztoky – Kralupy on 17 October (8:00 – 17:00), Roudnice – Ústí on 29 and 30 October (day), R20 at night 13/14 – 16/17 October, and the Monday works in Germany until 7 December, when Ex5 ends at Děčín instead of Bad Schandau (same minutes to Ústí). <b>Re-checked on pid.cz on 25 October:</b> the Masarykovo closure (to 12 December) is still the only PID works on these lines; the 17 October S4 works and the R20 night works are over. The ČD-only items (Roudnice – Ústí, the German Monday works) and the Ústí region lines were not re-checked.',
    '<b>Other trains on this track, not on this sheet (added 25 October):</b> S49 Praha-Hostivař – Praha-Holešovice – Praha-Podbaba – Roztoky u Prahy (CIS 1049, 34 trains each way on Praha-Podbaba – Roztoky; its own sheet, S49 Hostivař – Roztoky, archived 10 October); the S40 pair Sp 1494 Praha-Holešovice 16:26 → Kralupy → Slaný and Sp 1495 Slaný 6:26 → Kralupy → Praha-Holešovice (listed on the S5 sheet); R49 on Praha hl. n. – Praha-Holešovice (S9 · S2 sheet); and U52 (CIS 4052), the Sp Žatec – Postoloprty – Libochovice – Lovosice – Ústí nad Labem hl. n., every 2 h on Lovosice – Ústí (from Lovosice 13:21, 15:21, 17:21; from Ústí 14:17, 16:17, 18:17). U52 comes off the Lovosice branch to Libochovice, which is not built in the game, so it is not modelled; a Lovosice – Ústí cut would be a new line (ask if you want it).',
    # S4 corridor
    '<b>S4 outside the pattern:</b> Os 9600 Praha hl. n. 0:30 → Kralupy, Os 6902 Praha hl. n. 4:36 → Ústí and Os 6900 Kralupy 4:23 → Ústí; Os 9663 and Os 9665 Kralupy 22:42 and 23:12 → Praha hl. n.; the Vraňany shorts Os 9672 Kralupy 7:50 → Vraňany, Os 9673 Vraňany 8:19 → Kralupy and Os 9662 Praha 22:43 → Vraňany; the early Os 9605 and Os 6903 Roudnice 4:13 and 4:52 → Praha; Os 6989 Roudnice 21:48 → Kralupy; Os 6988 Neratovice 19:59 → Kralupy → Roudnice (the last S43, run on).',
    '<b>U4 Roudnice – Ústí shorts:</b> in the morning and at midday, every 2 h from Roudnice at 8:02, 10:03, 12:03 (Os 6944, 6946, 6948) and from Ústí at 7:05, 9:05, 11:05 (Os 6943, 6945, 6947); in the afternoon only Os 6951 Ústí 18:05 → Roudnice (the game runs it to Praha like the other :05 trains) and Os 6959 23:05. Also Os / Sp 4054: Sp 1970 Lovosice 13:07 → Ústí, Sp 1971 Ústí 12:42 → Lovosice, Sp 1972 Roudnice 22:23 → Ústí, Sp 1973 Ústí 21:03 → Roudnice, and the early Os 6940, 6941, 6942, 6931, 6932, 6970.',
    '<b>Ex5 through trains via Praha-Holešovice:</b> rj 174 (Kúty → Praha-Holešovice 14:26 – 14:41 → Ústí 15:41), rj 175 (Ústí 14:13 → Holešovice 15:15 – 15:36 → Kúty) and rj 177 (Ústí 18:13 → Holešovice 19:15 – 19:36 → Břeclav) have the line\'s Ústí minutes but call only at Holešovice; the game\'s Ex5 covers their slots from Praha hl. n.',
    '<b>Ex5 / EC outside the pattern:</b> EC 170 Praha hl. n. 20:47 and EC 179 Ústí 22:11 (Praha 23:31), the evening pair at other minutes; EC 251 Ústí 9:16 → Praha-Holešovice → Břeclav and EC 250 Břeclav → Praha-Holešovice 17:38 → Ústí 18:42 → Děčín (the Budapest trains, which call only at Holešovice); the night EC 456 / 457 Břeclav – Bad Schandau (Praha 3:14 and 0:26).',
    '<b>R15 outside the pattern:</b> the morning and evening trains R 600, 601, 602, 603, 618 and 620 (Praha 21:31 to Teplice, 22:37 to Ústí, and the early ones from Teplice and Klášterec), at other minutes.',
    '<b>R20:</b> the trains that start or end at Ústí (R 674, 682, 694 to Ústí; R 687 and R 695 from Ústí) run the line\'s minutes and are covered by it. In the morning and evening some R20 run from or to Praha Jih at other minutes (R 698, 670, 677, 697).',
    # right bank
    '<b>Litoměřice město shorts:</b> Os 6426 Litoměřice město 12:26, Os 6428 17:12 and Os 6432 19:50 → Ústí nad Labem západ; Os 6427 Ústí západ 15:35 and Os 6429 19:03 → Litoměřice město; the early Os 6420, 6422, 6424, 6425, 6437 and Os 6423 from Ústí nad Labem-Střekov. No clock-face; Ústí západ – Litoměřice město already has S32 and U32 every hour.',
    '<b>S32 / U32 outside the pattern:</b> Os 6431 Ústí západ 17:03 → Mělník (the U32 slot, run on to Mělník), Os 6433 23:01 → Mělník, Os 6443 Mělník 5:02 → Lysá, Os 6430 Mělník 4:51 → Ústí západ, Os 6450 Štětí 4:03, Os 6459 Ústí západ 21:35 → Štětí, and the morning S32 at other minutes (Os 6404 Lysá 6:54, Os 6405 Ústí západ 7:03 → Lysá 8:43).',
    '<b>S23 Brandýs shorts:</b> Čelákovice – Brandýs nad Labem in the hours without a Neratovice train (from Čelákovice 8:36, 10:36, 18:36, 20:36, 21:36, 22:36, 23:48; from Brandýs 9:01, 11:01, 20:01, 22:01, 23:01 and early). In the afternoon only the 18:36 is short; the game runs it to Neratovice. Also Os 19442 Brandýs 22:00 → Neratovice and Os 19443 Neratovice 22:34 → Brandýs.',
    # scope
    '<b>S22 Praha – Lysá – Milovice (your call: only if it really runs):</b> it has no trains in the afternoon peak. S22 runs only in the morning, at midday and in the evening (Praha hl. n. :19 → Milovice :04 from 8:19 to 13:19 and 20:19 – 21:19; Milovice :48 / :51 → Praha; the Lysá – Milovice shuttle :33 / :16). In the afternoon Milovice is served by S9 Milovice – Strančice, which is already in the game. So it is not modelled.',
    '<b>S27 Čáslav – Třemošnice:</b> left out (your call).',
    '<b>Mělník – Mšeno – Mladá Boleslav (KJŘ 076, CIS 1033 / 1036):</b> built in the game, but there are no workday trains: it runs only on weekends and holidays (and the summer Sp 1272 / 1273 Praha – Mšeno). Not modelled.',
    '<b>The Lovosice branches</b> (not built in the game): Litoměřice – Lovosice – Most (CIS 4010) and Česká Lípa – Litoměřice – Lovosice – Libochovice – Postoloprty (CIS 4011).',
    '<b>Beyond Ústí nad Labem</b> (the end of the game\'s track): R20, Ex5 and R15 onwards, Ústí – Děčín, Ústí západ – Děčín (CIS 4007), the lines to Teplice, Most and Chomutov (4001, 4003, 4005, 4051) and R94 Ústí – Liberec.',
    '<b>Already in the game (save of 14 October, 19:44), so not on this sheet:</b> S3 (Os070/1, 3 vehicles), S30 (Os070/2), S34 (Os071, 2), R43 (Sp070/1, 2), R21 Praha – Tanvald (R21/1, 4), S35 (Os070/4), R22 Kolín – Šluknov, and the lines east of Praha (S1, S2, S9, S12, S21, S61, R41, R42).',
]
SHARED = {
    A_S4: [
        'Praha – Kralupy is shared by the two S4 lines and the fast trains. From Praha: S4 from Praha-Bubny :14 and S4 Ústí :44; from Praha hl. n. R15 L:31, Ex5 S:31 and R20 :47. R15 and Ex5 alternate hours and both run non-stop Praha-Holešovice – Ústí.',
        'At Kralupy R20 overtakes S4 Ústí both ways: towards Ústí S4 Ústí stands :15 – :23 while R20 calls :17 – :19; towards Praha S4 Ústí stands :33 – :42 while R20 calls :38 – :40. S43 meets S4 there (in :22, out :27).',
        'Ústí nad Labem hl. n.: towards Praha S4 Ústí :05, Ex5 S:13, R15 L:14, R20 :42; arrivals S4 Ústí :51, R20 :14, Ex5 L:41, R15 S:42. R23 also starts and ends there (in L:21, out S:33). All of them turn at Ústí. With R23 stabled at Ústí západ between L:31 and S:23, at most two of them stand at Ústí hl. n. at a time (counted minute by minute over 2 h; three without the empty run).',
        'R20, Ex5 and R15 run empty from and to the depot Praha Jih (your call, 14 October): R20 out :28, in :35; Ex5 out S:06, in L:51; R15 out L:06, in S:51, the Ex5 minutes in the other hours.',
        'At Kralupy the S4 Ústí second unit parts from S4 Ústí towards Ústí (in :15) and couples again towards Praha (out :42); it stands at Kralupy :15 – :42.',
    ],
    A_LB: [
        'R23 and S32 share Lysá nad Labem – Mělník – Štětí – Litoměřice město – Ústí nad Labem západ in alternate hours: from Lysá R23 L:58, S32 S:18; from Ústí západ R23 S:40, S32 S:03. Between Ústí západ and Štětí U32 adds the odd-hour train (L:03 from Ústí západ, S:04 from Štětí), so that stretch has S32 or U32 every hour.',
        'Only R23 runs on to Ústí nad Labem hl. n. (in L:21, out S:33). Lysá nad Labem, Všetaty and Mělník are also on lines that are already in the game (S2, S9, S3).',
    ],
    A_NR: [
        'S43 and S23 both end at Neratovice, where S3 (in the game as Os070/1, Praha hl. n. :44, Mělník :11, the real minutes) calls: S43 in :51 / out :59, S23 in :25 / out :34. S3 is at Neratovice :30 – :31 towards Mělník and :29 – :35 towards Praha (real minutes; the game line has no entry there).',
        'Checked against the lines in the save: R23 leaves Kolín at L:20, Nymburk at L:45 and S:12; S2 (Os231/1, Os231/2) leaves Kolín at :32 and Nymburk at :01, :07 and :37, and R22 leaves Kolín at S:45 and Nymburk at L:08 and S:49. No two of them leave the same station in the same direction in the same minute.',
        'At Kralupy S43 connects with S4 (S4 from Praha :45, S43 out :27; S43 in :22, S4 to Praha :12).',
    ],
}
HEAD = [
    '<title>Trains S4 to S3</title>',
    '<h1>Trains from S4 to the S3 corridor</h1>',
    '<p class="muted">Simutrans design for the workday trains of the S4 – S3 corridor that the game does not have yet: S4 Praha – Kralupy – Ústí nad Labem, the fast trains to Ústí (R20, Ex5, R15), R23 Kolín – Mělník – Ústí, S32 Lysá – Mělník – Ústí západ, S43 Kralupy – Neratovice and S23 Čelákovice – Neratovice. '
    'S3, S30, S34, R43, R21 and the lines east of Praha already run in the game (save of 14 October, 19:44) and are not on this sheet. '
    'Times are real JR2026 times from the national CIS JŘ timetable, for trains that run on all five days Mon–Fri 5–9 October 2026. Unit types are from vagonweb.cz.</p>',
    '<p class="small"><b>14 October 2026, v2:</b> your notes. Praha-Bubny holds at most 2 trains at a time (v1 wrongly said 4 – 5). S4 Ústí gets its real second RegioPanter between Bubny and Kralupy as a coupled line (fork coupling: it parts at Kralupy towards Ústí and couples there again towards Praha), +2 vehicles. R15 now runs from and to Praha Jih (2 vehicles, as before). R23 stables at Ústí nad Labem západ between its trips, as the real train does, instead of standing 72 min at Ústí hl. n. (3, as before). 25 → 27 vehicles.</p>',
    '<p class="small"><b>15 October 2026:</b> your report from the game: S4 Ústí reached Lovosice 21 min and Kralupy 36 min before its departure there. The Ústí :05 and Lovosice :29 / :31 departures are confirmed for every train of the day. <a href="#s4u">S4 Ústí</a> now also waits for its real minute at Nelahozeves, Vraňany, Hněvice and Roudnice nad Labem towards Ústí, and at Bohušovice nad Ohří, Roudnice, Hněvice, Vraňany and Nelahozeves towards Praha. They stop where a faster train would come up behind it. No other change; 27 vehicles.</p>'
    '<p class="fix"><b>25 October 2026 (method check):</b> every line was checked again against the real timetable (patterns, offsets, timed stops, round trips, and where the trains meet on single track); no timetable entry and no vehicle count changes, 27 vehicles. Added under Not modelled: S49, the S40 Sp 1494 / 1495, R49 and U52 on this track, and the 25 October works check.</p>'
    '<p>Notation: <b>L</b> = odd hours, <b>S</b> = even hours. With every 120, odd hours come first: offset 55 means L:55, offset 114 means S:54. With every 60 the offset is the minute of every hour. '
    '(x) = request stop. <span class="wait">Highlighted</span> rows are timed stops with a longer stay. "Leave up to" is 30 min on every entry of the lines every 120, and automatic on the lines every 60.</p>',
]

INV = {'1004', '4004', '1043', '1023', '1032', '4032', '4054', '20', '15', '23', '5'}

if __name__ == '__main__':
    base.run(LINES, OUT, LISTED, along=True, inv_svcs=INV, head=HEAD, shared=SHARED, not_modelled=NOT_MODELLED)
