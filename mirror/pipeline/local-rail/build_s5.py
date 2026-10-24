"""Trains from S5 to the S4 corridor (S4 itself not included): S5 Praha – Kladno – Kralupy with S45, R45, S50 and R24,
S54, S40 Kralupy – Slaný – Louny, S44 Kralupy – Velvary, the Rakovník lines (to Blatno u Jesenice, to Most,
Lužná u Rakovníka – Žatec – Jirkov) and the Straškov lines (Vraňany – Straškov / Horní Beřkovice, Roudnice – Bříza obec).

Designed 14 Oct 2026 with the rules in ../rail-design-rules.md and the builder in build_012_014_235.py (real JR2026
times from CIS JŘ, trains that run on all five days Mon–Fri 5–9 Oct 2026). PID labels come from the CIS line number
(S = 1000 + n, R = 1100 + n). Unit types from vagonweb.cz (vagonweb.py; R24 is Arriva, zeme ARV; the Rakovník – Most
and Lužná – Jirkov lines are Die Länderbahn, zeme DLB).
Scope (user, 14 Oct 2026): the PID core plus all four outer groups offered; the game's track ends at Blatno u Jesenice,
everything else runs to its real termini. 4021 Roudnice – Bříza obec runs every 72 (user's choice).
Simplified 14 Oct 2026 (user: "simplify the S57 and U12 lines - pick the best pattern to be more uniform"; S57 = 1057 to
Blatno u Jesenice, U12 = 4012 Rakovník – Most): both every 60 on one real pair that crosses at real crossing stations each
hour. S57 = Os 16716 (cut at Blatno) / Os 16773, crossing at Oráčov; U12 = Os 6718 / Os 6711 (cut at Most), crossing at
Svojetín, Hřivice and Lenešice. They were 2-hourly circuits through all the real families (4 and 5 vehicles).
The game's U12 track ends at Most (user, 14 Oct 2026: "now U12 I have built only to Most").
Engineering works (user, 14 Oct 2026: "don't they end at Praha-Bubny because of engineering works?" and "don't do those
ending in early november, do include the Masarykovo one"): from 1 June to 12 December 2026 Praha Masarykovo nádraží –
Praha-Bubny is closed (PID; ČD works timetable cz-k120-2026vyluka03). S5, R45, R24 and S54 start and end at Praha-Bubny;
R24 and R45 also stop at Praha-Výstaviště. The works timetable keeps the annual minutes from Bubny on, so the lines are
cut legs from Bubny, Výstaviště is added at its real passing minute, and R45/R24 leave Bubny at their annual arrival
minute (works timetable: Sp 1570 Bubny 14:03, Výstaviště 14:06). Not modelled (user): the works that end in early
November, U14 Měcholupy – Žatec by bus (13 Jul – 9 Nov) and S75 Rakovník – Roztoky by bus (29 Sep – 8 Nov).
U13 (user, 15 Oct 2026: "then add to it U13 in full?"): CIS 4013 Most – Žatec západ (KJŘ 123, RegioJet ÚK), the whole
line, every 60 on Os 6519 / Os 6520 (Most :42, Žatec západ :30), crossing at Volevčice every hour; 2 vehicles.
Writes "Trains S5 to S4.html" in the project root.
Run: python pipeline/local-rail/build_s5.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_012_014_235 as base  # noqa: E402

# full names for the data abbreviations on this sheet (only here, so the other sheets rebuild unchanged)
base.FULL.update({'Kralupy n.V.': 'Kralupy nad Vltavou', 'Praha Masaryk. n.': 'Praha Masarykovo nádraží'})

OUT = os.path.join(base.ROOT, 'Trains S5 to S4.html')
PB, VY = 'Praha-Bubny', 'Praha-Výstaviště'
_load = base.load


def load():
    """the real data, adjusted for the Masarykovo nádraží closure (1 June – 12 December 2026): R45 and R24 stop at
    Praha-Výstaviště (at their passing minute) and leave Praha-Bubny at their annual arrival minute there"""
    by_num, wd = _load()
    for r in list(by_num.values()) + wd:
        if r['svc'] not in ('1145', '24') or any(s_['name'] == VY for s_ in r['stops']):
            continue
        names = [s_['name'] for s_ in r['stops']]
        p = next((l for l in r['raw'] if l['name'] == VY and l.get('arr') is not None), None)
        if p is None or PB not in names:
            continue
        i = names.index(PB)
        b = r['stops'][i]
        tb = b['arr'] if b['arr'] is not None else b['dep']
        out = p['arr'] > tb  # Výstaviště after Bubny: towards Kladno
        if out and b['arr'] is not None and b['dep'] is not None:
            b['dep'] = b['arr']  # towards Kladno: the works timetable leaves Bubny at the minute the annual one arrives
        r['stops'].insert(i + 1 if out else i, {'name': VY, 'arr': p['arr'], 'dep': p['arr'], 'req': False})
    return by_num, wd


base.load = load
INV = {'1005', '1045', '1145', '1050', '24', '1054', '1040', '4040', '1144', '1044', '1057', None, '4012', '4013', '4014', '4021', '4022'}
IMP = 'important station'
REV = 'reverses, the driver changes cabs'
BL = 'Blatno u Jesenice'
A_S5 = 'Praha – Kladno – Rakovník (S5 family) and S54'
A_RK = 'Rakovník lines'
A_KR = 'Kralupy nad Vltavou – Slaný – Louny and Velvary'
A_ST = 'Straškov lines'

LINES = [
    # --- S5 family ---------------------------------------------------------------------------------------------
    {
        'id': 's5', 'name': 'S5 + S45', 'area': A_S5, 'svc': ['1005', '1045'], 'every': 60,
        'legs': [{'cut': ('9822', PB, 'Kralupy nad Vltavou')}, {'cut': ('9829', 'Kralupy nad Vltavou', PB)}], 'cut_at': [PB],
        'wait_points': {('out', 'Kladno'): IMP, ('in', 'Kladno'): IMP},
        'notes': [
            'Two PID lines run as one train: S5 Praha – Kladno – Kladno-Ostrovec (CIS 1005, KJŘ 120) and S45 Kladno-Ostrovec – Zákolany – Kralupy nad Vltavou (CIS 1045, KJŘ 093). On workdays every S5 runs through as S45 under the same train number, every hour; on weekends S5 ends at Kladno-Ostrovec. So the line is the real through train, not two lines joined by the design.',
            'Masarykovo nádraží is closed from 1 June to 12 December 2026 (station modernisation), so the line starts and ends at Praha-Bubny. The works timetable keeps every other minute: from Praha-Bubny every hour at :34 (Kladno :23 – :25, Kralupy nad Vltavou :04), from Kralupy at :49 (Kladno :28 – :31, Praha-Bubny :16).',
            'Four vehicles. 18 min at Praha-Bubny (in :16, out :34) and 45 min at Kralupy nad Vltavou (in :04, out :49): the real minutes fix both stays. Kladno is timed both ways as the important station (junction for S50, R24 and the Kladno-Ostrovec shuttle). Praha-Dejvice towards Praha (5 min, :05 – :10) is timed by the 5-min rule.',
            'Vehicles: 814 RegioNova, usually two units (vagonweb 2026, Os 9822 and Os 9829; 814 064 + 814 102 seen on Os 9829).',
        ],
    },
    {
        'id': 's45', 'name': 'S45 Kladno-Ostrovec', 'area': A_S5, 'svc': '1045', 'every': 120,
        'rep_out': '17166', 'rep_in': '17167',
        'wait_points': {},
        'notes': [
            'Besides the through trains (see S5 + S45), S45 (CIS 1045) has the shuttle Kladno – Kladno město – Kladno-Ostrovec: every 2 h from Kladno at L:45 (13:45, 15:45, 17:45, 19:45; Ostrovec L:50) and from Kladno-Ostrovec at S:03 (14:03, 16:03, 18:03; Kladno S:10). The S45 trains Kladno – Kralupy run only before 7:00 (listed under Not modelled).',
            'One vehicle. 13 min at Kladno-Ostrovec and 1 h 35 min at Kladno (in S:10, out L:45): the real minutes.',
            'Vehicles: 814 RegioNova (vagonweb 2026, Os 17166 and Os 17167).',
        ],
    },
    {
        'id': 'r45', 'name': 'R45', 'area': A_S5, 'svc': '1145', 'every': 120, 'inv_svcs': {'1145'},
        'legs': [{'cut': ('1570', PB, 'Kladno-Ostrovec')}, {'cut': ('1577', 'Kladno-Ostrovec', PB)}], 'cut_at': [PB],
        'wait_points': {('out', 'Kladno'): IMP, ('in', 'Kladno'): IMP},
        'notes': [
            'PID R45 (CIS 1145), the Sp Praha-Bubny – Praha-Výstaviště – Hostivice – Kladno – Kladno-Ostrovec. During the Masarykovo nádraží closure (1 June – 12 December 2026) it starts and ends at Praha-Bubny and also stops at Praha-Výstaviště. Every 2 h from Praha-Bubny at S:03 (14:03, 16:04, 18:03, 20:03; Kladno-Ostrovec S:49) and from Kladno-Ostrovec at L:06 (13:06, 15:06, 17:06, 19:06; Praha-Bubny L:49).',
            'One vehicle. 17 min at Kladno-Ostrovec (in S:49, out L:06) and 14 min at Praha-Bubny (in L:49, out S:03): the real minutes of the works timetable (Sp 1570: Bubny 14:03, Výstaviště 14:06).',
            'The extra peak R45 from Praha-Bubny at L:21 (15:21, 17:21, 18:21, and 16:21 to Blatno u Jesenice) run only out of Praha in the afternoon; their units come back in the morning peak. They are listed under Not modelled.',
            'Vehicles: 814.2 RegioNova Trio, sometimes two units (vagonweb 2026, Sp 1570 and Sp 1575; 814 246 + 814 064 seen, and pairs of 854 on some days).',
        ],
    },
    {
        'id': 's50', 'name': 'S50', 'area': A_S5, 'svc': '1050', 'every': 120,
        'rep_out': '19708', 'rep_in': '19715',
        'wait_points': {},
        'notes': [
            'PID S50 (KJŘ 120), Kladno – Stochov – Nové Strašecí – Lužná u Rakovníka – Rakovník. Every 2 h from Kladno at S:45 (14:45, 16:45; Rakovník L:42) and from Rakovník at S:09 (16:09, 18:09; Kladno L:01).',
            'Lužná u Rakovníka is timed towards Rakovník: the train waits there 6 min (:26 – :32), where the line to Žatec branches off.',
            'Two vehicles. 27 min at Rakovník (in L:42, out S:09) and 1 h 44 min at Kladno (in L:01, out S:45). The real minutes fix this: there is no S50 from Kladno in the odd hours.',
            'Vehicles: 814 RegioNova (vagonweb 2026, Os 19708 and Os 19715; 814 101 seen on Os 19715).',
        ],
    },
    {
        'id': 'r24', 'name': 'R24', 'area': A_S5, 'svc': '24', 'every': 120, 'cat': 'R', 'inv_svcs': {'24'},
        'legs': [{'cut': ('1236', PB, 'Rakovník')}, {'cut': ('1239', 'Rakovník', PB)}], 'cut_at': [PB],
        'wait_points': {('out', 'Kladno'): IMP, ('in', 'Kladno'): IMP},
        'notes': [
            'R24 Praha-Bubny – Kladno – Rakovník, run by Arriva. During the Masarykovo nádraží closure (1 June – 12 December 2026) it starts and ends at Praha-Bubny and also stops at Praha-Výstaviště (PID). Every 2 h from Praha-Bubny at L:03 (13:03, 15:03, 17:03, 19:03; Rakovník S:28) and from Rakovník at L:22 (13:22, 15:22, 17:22; Praha-Bubny S:48).',
            'Confirmed by the Arriva works timetable linked from PID (14 October 2026): R24 leaves Praha-Bubny at L:03 (13:03, 15:03, 17:03, 19:03) and calls at Praha-Výstaviště at L:06; towards Praha it calls at Výstaviště at S:46 and reaches Bubny at S:48.',
            'Two vehicles. 54 min at Rakovník (in S:28, out L:22) and 15 min at Praha-Bubny (in S:48, out L:03): the real minutes. Kladno is timed both ways as the important station. Stochov towards Praha stands 4 min (:54 – :58), under the 5-min rule.',
            'Vehicles: Arriva 845 units, often two, sometimes with a 945 trailer (vagonweb 2026, operator ARV; 845 320 + 845 118 seen on R 1236).',
        ],
    },
    {
        'id': 's54', 'name': 'S54', 'area': A_S5, 'svc': '1054', 'every': 120, 'circuit': True,
        'legs': ['19758', '19757', '19760', '19759'], 'turns': [3, 10, 10, 10],
        'terminal': ['Hostivice'],
        'wait_points': {},
        'notes': [
            'PID S54 (KJŘ 121), Hostivice – Středokluky – Noutonice, a peak line. One unit runs it every hour from Hostivice at :31, alternately to Noutonice and to Středokluky: in reality 15:31 Noutonice, 16:31 Středokluky, 18:31 Noutonice, 19:31 Středokluky (at 17:31 there is the Praha-Bubny train instead, listed).',
            'So the line is one circuit every 2 h: Hostivice L:31 → Noutonice L:53, back at L:56 → Hostivice S:18; Hostivice S:31 → Středokluky S:47, back at S:58 → Hostivice L:13. One vehicle.',
            'The turn at Noutonice is the real 3 min (in :53, out :56). With the usual 10 min the train would miss its Hostivice slot and the line would need 2 vehicles. Hostivice is stop type terminal in both entries, so nobody rides through from one trip to the next. 13 and 18 min at Hostivice, 11 min at Středokluky.',
            'Vehicles: 810 (vagonweb 2026; 810 349 ran Os 19758 and Os 19757 on 24 April 2026). At Hostivice S54 meets S5 and S65.',
        ],
    },
    # --- Rakovník lines --------------------------------------------------------------------------------------------
    {
        'id': 'p161', 'name': 'S57', 'area': A_RK, 'svc': ['1057', None], 'every': 60,
        'legs': [{'cut': ('16716', 'Rakovník', BL)}, '16773'], 'turns': [10, 8],  # Rakovník: in :40, out :48
        'cut_at': [BL],
        'wait_points': {('in', 'Oráčov'): 'crossing with the train to Blatno u Jesenice'},
        'notes': [
            'S57 is KJŘ 161 Rakovník – Jesenice – Blatno u Jesenice (CIS 1057), cut at Blatno u Jesenice, where the game\'s track ends. In reality many trains run on to Žlutice and Bečov nad Teplou; the Bečov trains have no CIS line number.',
            '<b>Simplified 14 October 2026 (your request: one uniform pattern):</b> every hour, from Rakovník at :48 (Jesenice :22 – :23, Blatno :33) and from Blatno u Jesenice at :53 (Jesenice :02 – :04, Rakovník :40). The out trip is Os 16716 (Rakovník 14:48, the train to Bečov) and the back trip Os 16773 (Blatno 16:53), both real minutes.',
            'Why this pair: the line is single track, and an hourly pattern only works if each pair of trains crosses at a station with a loop. These two cross at Oráčov every hour (to Blatno :13 – :14, to Rakovník :12 – :14, as Os 16720 and Os 16773 really do at 17:12). The back train is timed there. Of the other real families, these pairs also work every hour, all crossing at Pšovlky: Rakovník :31 with Blatno :26, :01 with :53, and :17 with :12. These would meet on open line: :48 with :12 or :26, :01 with :12 or :26, and :31 with :12 or :53. The :48 / :53 pair is used because it puts the short stay at Rakovník (see below).',
            'Two vehicles. 20 min at Blatno u Jesenice (in :33, out :53) and 8 min at Rakovník (in :40, out :48). The 8 min joins two real minutes; no unit really turns at Rakovník in 8 min. A 10-min turn would push the line to 3 vehicles. The short stay is at Rakovník, the junction, and the long one at Blatno, the end of the track.',
            'The alternative, if you prefer it: Rakovník :31 (Os 16774) and Blatno :26 (Os 16719), crossing at Pšovlky every hour. It also needs 2 vehicles and matches a few more real afternoon trains (Blatno 14:25, 16:26, 18:26), but it turns in 9 min at Blatno and stands 21 min at Rakovník.',
            'Compared with reality: the real afternoon has three trains every 2 h each way (from Rakovník S:01, S:48 and L:31; from Blatno L:12, S:26 and S:53); the game runs two. The :48 trains are real every 2 h (8:49, 10:48, 14:48, 16:47), and in the other hours the game adds a train at the same minute. The other trains are listed under Not modelled.',
            'Vehicles: 810 and 814 RegioNova both run here (vagonweb 2026: Os 16773 planned 810, Os 16716 planned 814; 810 436 ran Os 16774 and Os 16773 on 25 March 2026).',
        ],
    },
    {
        'id': 'p126', 'name': 'U12', 'area': A_RK, 'svc': '4012', 'every': 60,
        'legs': ['6718', {'cut': ('6711', 'Most', 'Rakovník')}], 'turns': [10, 10],  # Most: in :53, out :03
        'cut_at': ['Most'],
        'wait_points': {('out', 'Louny'): REV, ('in', 'Louny'): REV,
                        ('out', 'Svojetín'): 'crossing with the train to Rakovník',
                        ('in', 'Svojetín'): 'crossing with the train to Most',
                        ('out', 'Hřivice'): 'crossing with the train to Rakovník',
                        ('in', 'Hřivice'): 'crossing with the train to Most'},
        'notes': [
            'U12 is KJŘ 126 Rakovník – Louny – Most (CIS 4012, Die Länderbahn), cut at Most, where the game\'s track ends (your note, 14 October 2026). In reality most trains run on to Osek město.',
            '<b>Simplified 14 October 2026 (your request: one uniform pattern):</b> every hour, from Rakovník at :09 (Svojetín :26 – :28, Hřivice :53 – :00, Louny :18 – :22, Most :53) and from Most at :03 (Louny :33 – :37, Hřivice :54 – :02, Svojetín :26 – :27, Rakovník :44). The out trip is Os 6718 (Rakovník 16:09 → Most 17:53, a real train that ends at Most) and the back trip Os 6711 from Most (Osek město 14:30, Most 15:03, Rakovník 16:44), both real minutes.',
            'Why this pair: the line is single track, and every hour each train meets the opposite one three times on the way. These two meet at real crossing stations every time: Svojetín (:26 – :27), Hřivice (:54 – :00) and Lenešice (:27). The common Rakovník :19 would meet the train back from Hřivice at :02 on open line between Chrášťany and Svojetín; in reality the :19 trains cross a different back train, the one from Hřivice at :56, at Chrášťany (Os 6716 and Os 6709 at 15:28). Os 6714 :12 with Os 6707 :30 also works (same 4 vehicles); the :09 / :44 pair is used because more real back trains have its minutes (Os 6705, 6711, 6715, 6717 all reach Rakovník at :44).',
            'Four vehicles (5 when it ran to Osek město). 10 min at Most (in :53, out :03) and 25 min at Rakovník (in :44, out :09). The 10 min at Most joins two real minutes: Os 6718 ends at Most at :53, and the back train leaves at :03.',
            'Compared with reality: the real Rakovník :19 trains (13:20, 15:19, 17:19, 19:19) leave 10 min later and do not wait at Hřivice, so from Hřivice on they have the same minutes. Os 6713 and Os 6709 (Most :03) are the same up to Hřivice, then leave at :56 and reach Rakovník at :38.',
            'The trains reverse at Louny (vagonweb: "změna směru jízdy"), so it is timed both ways. Hřivice (7 and 8 min) and Svojetín (2 and 1 min) are timed both ways as crossings.',
            'Vehicles: Die Länderbahn 654 RegioShuttle (vagonweb 2026, operator DLB, Os 6713 – 6716).',
        ],
    },
    {
        'id': 'p124', 'name': 'Os Lužná – Jirkov', 'area': A_RK, 'svc': '4014', 'every': 120,
        'rep_out': '16806', 'rep_in': '16805', 'turns': [6, 10], 'cut_at': ['Lužná u Rakovníka'],
        'wait_points': {},
        'notes': [
            'KJŘ 124 Lužná u Rakovníka – Žatec – Chomutov – Jirkov (CIS 4014, Die Länderbahn). In the afternoon peak every 2 h from Lužná at S:22 (16:22, 18:22; Žatec L:06 – L:23, Jirkov L:56) and from Jirkov at S:02 (16:02; Lužná L:24).',
            'Žatec is timed towards Jirkov: the train stands there 17 min. Towards Lužná it stands 3 min.',
            'Two vehicles. 6 min at Jirkov (in L:56, out S:02): the real minutes. With 10 min it would miss the slot and need 3 vehicles. 58 min at Lužná u Rakovníka (in L:24, out S:22).',
            'Some trains start or end at Rakovník or Rakovník západ (14:26, 20:07 out; 12:02, 20:02 back) and pass Lužná at the same minutes; in the game every train ends at Lužná, as the peak trains do.',
            'Vehicles: Die Länderbahn 654 RegioShuttle (vagonweb 2026, operator DLB, Os 16804 – 16806).',
        ],
    },
    {
        'id': 'p123', 'name': 'U13', 'area': A_RK, 'svc': '4013', 'every': 60,
        'legs': ['6519', '6520'], 'turns': [5, 10],  # Žatec západ: in :25, out :30 (the real turn)
        'wait_points': {('out', 'Obrnice'): 'timing point, before the crossing at Volevčice',
                        ('in', 'Počerady'): 'timing point, before the crossing at Volevčice'},
        'notes': [
            'U13 is KJŘ 123 Most – Obrnice – Postoloprty – Žatec – Žatec západ (CIS 4013, RegioJet ÚK), in full. Every hour from Most at :42 (Obrnice :46 – :48, Postoloprty :06 – :07, Žatec :21 – :23, Žatec západ :25) and from Žatec západ at :30 (Žatec :32 – :33, Postoloprty :47 – :48, Obrnice :06 – :08, Most :13). These are Os 6519 and Os 6520; almost every train of the day has the same minutes, from Most 4:42 to 19:42 and from Žatec západ 5:30 to 19:30.',
            'The line is single track. Each hour the two trains cross at Volevčice: both pass it at :57 (in reality without stopping). There is no other passing place between Obrnice and Počerady, so in the game Volevčice needs a passing track. Obrnice towards Žatec (:48) and Počerady towards Most (:55) are timing points. Without them the faster game trains would reach the single track early and meet somewhere else.',
            'At Obrnice U13 meets U12 every hour, as in reality: towards Žatec it stands :46 – :48 while U12 towards Most stands there :46 – :48; towards Most it stands :06 – :08 while U12 from Most stands :07 – :08.',
            'Two vehicles. 5 min at Žatec západ (in :25, out :30): the real turn, the same unit runs back. 29 min at Most (in :13, out :42).',
            'Vehicles: RegioJet 654 RegioShuttle (vagonweb 2026, operator RJ, planned on Os 6519 – 6522). Same line in the game save: Os123 "[U13] Most - Žatec západ" (no vehicles yet).',
        ],
    },
    # --- Kralupy -------------------------------------------------------------------------------------------------
    {
        'id': 's40l', 'name': 'S40 Louny', 'area': A_KR, 'svc': ['1040', '4040'], 'every': 120,
        'rep_out': '9710', 'rep_in': '9713',
        'wait_points': {('out', 'Slaný'): IMP, ('in', 'Slaný'): IMP},
        'notes': [
            'The S40 trains that run through to Louny (KJŘ 110; CIS 1040 out of Kralupy, 4040 from Louny). Every 2 h from Kralupy nad Vltavou at L:55 (13:55, 15:55, 17:55; Slaný S:27, Louny L:18) and from Louny at S:37 (14:37, 16:37; Slaný L:30 – L:34, Kralupy S:03).',
            'Three vehicles. 1 h 19 min at Louny (in L:18, out S:37) and 1 h 52 min at Kralupy (in S:03, out L:55): the real minutes. Slaný is timed both ways as the important station (4 min towards Kralupy).',
            'Vehicles: the trains to Louny are planned 814 RegioNova (Os 9710, 814 130 seen), the trains back 810 (Os 9713, 810 333 seen) – so the real units do not simply shuttle. S40 Louny and S40 stay separate lines for that reason; one circuit through both would need 4 vehicles instead of 5.',
        ],
    },
    {
        'id': 's40', 'name': 'S40', 'area': A_KR, 'svc': '1040', 'every': 120,
        'rep_out': '9712', 'rep_in': '9735',
        'wait_points': {},
        'notes': [
            'PID S40 Kralupy nad Vltavou – Podlešín – Slaný, in the hours between the Louny trains: from Kralupy at S:55 (12:55, 14:54; Slaný L:25) and from Slaný at S:29 (16:29, 18:29, and 14:31; Kralupy L:00). With S40 Louny this gives Kralupy – Slaný a train every hour at :55 and Slaný – Kralupy every hour at :29 – :34, as in reality outside the 16 – 19 peak.',
            'Two vehicles. 1 h 4 min at Slaný (in L:25, out S:29) and 1 h 54 min at Kralupy (in L:00, out S:54). A shorter turn at Slaný is not possible: the odd-hour slot towards Kralupy (L:34) belongs to the Louny train.',
            'The 16 – 19 peak has extra trains at other minutes (Kralupy 16:22, 17:23, 18:22, 18:52; Slaný 17:00); they are listed under Not modelled.',
            'Vehicles: 814 RegioNova (vagonweb 2026, Os 9712 and Os 9711; 814 124 seen).',
        ],
    },
    {
        'id': 's44', 'name': 'S44', 'area': A_KR, 'svc': '1044', 'every': 60,
        'rep_out': '20324', 'rep_in': '20327', 'turns': [4, 10],
        'wait_points': {},
        'notes': [
            'PID S44 Kralupy nad Vltavou – Velvary (KJŘ 111). Every hour from Kralupy at :26 (Velvary :45) and from Velvary at :49 (Kralupy :07), from 13:49 to 21:49.',
            'One vehicle. It turns in the real 4 min at Velvary (in :45, out :49) and 19 min at Kralupy. With a 10-min turn at Velvary it would need 2 vehicles.',
            'Vehicles: 810 (vagonweb 2026, Os 20324; 810 070 seen).',
        ],
    },
    # --- Straškov ------------------------------------------------------------------------------------------------
    {
        'id': 'p095', 'name': 'Os Vraňany – Straškov', 'area': A_ST, 'svc': '4022', 'every': 120, 'circuit': True,
        'legs': ['12314', '12325', '12338', '12339'], 'turns': [3, 5, 10, 10],  # Vraňany: in 15:35½, out 15:41
        'terminal': ['Vraňany'],
        'wait_points': {},
        'notes': [
            'KJŘ 095 from Vraňany (on the S4 line) to Horní Beřkovice and Straškov (CIS 4022). One unit runs it all afternoon, alternately to Straškov and to Horní Beřkovice: Vraňany S:39 → Straškov L:06, back at L:09 → Vraňany L:35; Vraňany L:41 → Horní Beřkovice L:47, back at S:08 → Vraňany S:14; then S:39 again (14:39, 16:40, 18:39 to Straškov).',
            'So the line is one circuit every 2 h with one vehicle. The 3-min turn at Straškov and the 6 min at Vraňany are the real minutes; 21 min at Horní Beřkovice and 25 min at Vraňany.',
            'Vehicles: 841 RegioShuttle (vagonweb 2026, Os 12314, 12325, 12338, 12339; 841 201 was seen on Os 12314 to Straškov on 7 May 2026 and on Os 12325 back on 5 and 11 May). The same units also run Roudnice – Bříza obec.',
        ],
    },
    {
        'id': 'p096', 'name': 'Os Roudnice – Bříza', 'area': A_ST, 'svc': '4021', 'every': 72,
        'rep_out': '19614', 'rep_in': '19619', 'turns': [4, 10],
        'wait_points': {},
        'notes': [
            'KJŘ 096 Roudnice nad Labem – Straškov – Bříza obec (CIS 4021). It has no clock-face: one unit shuttles all day, leaving Roudnice at 13:03, 14:14, 15:20, 16:26, 17:57, 19:00, 20:14 and Bříza obec at 13:38, 14:47, 15:53, 17:10, 18:28. A round trip takes 66 – 71 min with 4 – 7 min turns.',
            'Your choice (14 October 2026): every 72, one vehicle. 72 divides 1440, so the pattern repeats exactly every day: 20 trains a day each way. The offset uses the same rule as the lines every 240: offset = (time − 60) mod 72. It starts from the real 14:14 (Os 19614).',
            'The game times against the real ones from Roudnice: 13:02 (13:03), 14:14 (14:14), 15:26 (15:20), 16:38 (16:26), 17:50 (17:57), 19:02 (19:00), 20:14 (20:14).',
            'Turns: the real 4 min at Bříza obec (in :43, out :47), and 10 min at Roudnice. Straškov, where the Vraňany line ends, is passed with a 1-min stop.',
            'Vehicles: 841 RegioShuttle (vagonweb 2026, Os 19614 and Os 19619; 841 237 also ran Os 12338 to Horní Beřkovice). On some days an 814 runs it.',
        ],
    },
]

PB, PM, KO, KD, KR = 'Praha-Bubny', 'Praha Masarykovo nádraží', 'Kladno-Ostrovec', 'Kladno-Dubí', 'Kralupy nad Vltavou'
LISTED = {
    ('Kladno', PM), (PB, KO), (KD, PM), ('Kladno', KR), (PM, 'Kladno'), (PM, KD), ('Kladno', PB), (KD, 'Kladno'),
    (PB, 'Kladno'), ('Hostivice', PM), (PM, 'Hostivice'), ('Hostivice', PB), (PB, 'Hostivice'), (KR, 'Brandýsek'),
    (KR, 'Kladno'), ('Kladno', KD), (KD, PB), (PB, KD),
    ('Rakovník', 'Lužná u Rakovníka'), ('Lužná u Rakovníka', 'Rakovník'), ('Rakovník západ', 'Rakovník'),
    ('Rakovník', 'Rakovník západ'), ('Rakovník', 'Jesenice'), ('Jesenice', 'Rakovník'),
    ('Louny město', 'Osek město'), ('Rakovník', 'Most'), ('Osek město', 'Louny město'), ('Louny', 'Rakovník'),
    ('Most', 'Rakovník'), ('Most', 'Louny město'), ('Most', 'Hřivice'), ('Hřivice', 'Osek město'), ('Hřivice', 'Most'),
    ('Louny město', 'Most'), ('Most', 'Louny'), ('Rakovník', 'Louny'), ('Osek město', 'Louny'), ('Louny', 'Most'), ('Most', 'Osek město'),
    ('Most', 'Žatec západ'), ('Žatec západ', 'Most'),
    ('Most', 'Obrnice'), ('Obrnice', 'Most'),  # on U13's line: the Rakovník – Osek trains outside the U12 pattern (listed there)
    ('Jirkov', 'Žatec'), ('Žatec', 'Jirkov'), ('Žatec', 'Lužná u Rakovníka'), ('Jirkov', 'Chomutov'), ('Lužná u Rakovníka', 'Žatec'),
    ('Kralupy nad Vltavou předměstí', KR), (KR, 'Kralupy nad Vltavou předměstí'),
    ('Straškov', 'Roudnice nad Labem'), ('Bříza obec', 'Straškov'),
}
NOT_MODELLED = [
    '<b>Note on Praha times below:</b> they are the annual times. While Masarykovo nádraží is closed (until 12 December 2026), trains listed "from Praha" or "to Praha" start and end at Praha-Bubny instead.',
    '<b>Engineering works not modelled (your call, 14 October):</b> the works that end in early November. On Lužná – Jirkov, Měcholupy – Žatec runs by bus until 9 November (Die Länderbahn, track repair). On S75 (its own sheet), Rakovník – Roztoky u Křivoklátu runs by bus until 8 November. The short works (single days, nights, Rakovník – Blatno by day 19 – 31 October, R17 delays near Říčany until 3 November) are not modelled either.',
    # S5 family
    '<b>R45 peak trains from Praha-Bubny:</b> Sp 1572 (15:21), Sp 1578 (17:21) and Sp 1582 (18:21) to Kladno-Ostrovec (:13), and Sp 1576 (16:21) via Kladno and Rakovník to Blatno u Jesenice (18:46). They run only out of Praha in the afternoon; their units come back in the morning peak (Sp 1561 and Sp 1563 from Kladno-Dubí 5:23 and 6:20, Sp 1567 from Kladno-Ostrovec 7:39). A game line needs a way back, so they are not modelled.',
    '<b>R45 and Sp to and from Blatno u Jesenice:</b> Sp 1565 (Blatno 5:21 → Praha 7:53) and Os 1585 (Blatno 10:25 → Praha 12:53) in the morning, Sp 1576 (Praha-Bubny 16:21 → Blatno 18:46) in the afternoon, and R24\'s Sp 1590 (Praha 11:00 → Blatno 13:14 → Bečov nad Teplou). Single trains, no pattern; Rakovník – Blatno is covered by the Os line.',
    '<b>Evening and morning R45:</b> Sp 1583 Kladno 21:14 → Praha, Sp 1588 Praha 22:00 → Kladno-Dubí, Os 17161 Kladno-Dubí 6:50 → Kladno.',
    '<b>S5 outside the pattern:</b> the morning and evening trains that start or end at Kladno, Kladno-Ostrovec or Kladno-Dubí (Os 9817 Kladno 7:31, Os 9851 / 9855 / 9861 / 9863 from Kladno-Ostrovec, Os 9854 / 9856 / 9860 / 9862 / 9850 to Kladno-Ostrovec, Os 9858 Praha 20:30 → Kladno-Dubí, Os 9865 Kladno-Dubí 22:25 → Praha, Os 9834 22:30 with 8 min at Kladno), and Os 9800 Praha 5:02 → Rakovník.',
    '<b>S45 Kladno – Kralupy:</b> only early morning (Os 17100 4:29, 17104 5:37, 17108 6:37 from Kladno; Os 17105 Kralupy 6:37 → Kladno, Os 17160 Kladno 6:18 → Kladno-Dubí) and Os 17103 Kralupy 22:23 → Kladno. In the afternoon S45 is only the Kladno-Ostrovec shuttle; its extra 17:09 (Os 17170) is not modelled.',
    '<b>S50 outside the pattern:</b> Os 19726 Kladno 12:25, Os 19724 20:44, Os 19716 22:45, Os 19711 Rakovník 12:08, Os 19719 20:29; Os 19713 from Rakovník západ 14:05 (one stop before Rakovník); Os 9801 / 9803 / 9805, the S50 trains that run through to Praha (4:42, 5:40, and 22:20 from Rakovník západ to Praha hl. n.).',
    '<b>S54 extras:</b> Os 19736 Praha-Bubny 16:42 → Středokluky 17:32 and Os 19735 Středokluky 17:44 → Praha-Bubny 18:32 (the 17:31 hour); morning trains to and from Praha (Os 19731, 19732, 19733 to Praha-Smíchov, 19745 to Praha-Zličín) and the early Hostivice – Středokluky shorts. The weekend S54 runs on from Noutonice via Zákolany to Slaný (Os 19750 / 19751 / 19754 / 19757, and Os 9784 – 9787 Praha – Slaný); no workday service there, so not modelled.',
    # Rakovník
    '<b>S57 Rakovník – Blatno, the trains at other minutes (since the hourly simplification, 14 October):</b> from Rakovník the S:01 Žlutice trains (Os 16768 8:01, 16770 10:01, 16772 11:59, 16714 13:59, 16718 16:01) and the L:31 Blatno trains (Os 16774 15:31, Os 16776 17:17); from Blatno the L:12 Bečov trains (Os 16709, 16717, 16721, 16725: 11:12, 15:12, 17:12, 19:19), the S:26 Žlutice trains (Os 16719 16:26, Os 16723 18:26) and the other Blatno starters (Os 16765 9:13, Os 16769 12:21, Os 16771 14:25, Os 16711 13:15). The game runs every hour at :48 and :53 instead.',
    '<b>Rakovník – Blatno outside the pattern:</b> Rakovník 18:32 (to Žlutice) and 20:47; Blatno 19:40; the morning trains; the short Os 16766 Rakovník 7:12 → Jesenice and Os 16779 Jesenice 8:03 → Rakovník. Everything beyond Blatno u Jesenice (Lubenec, Žlutice, Toužim, Bečov nad Teplou) is outside the game\'s track; so are Blatno – Žihle – Plzeň (KJŘ 160) and R25\'s single Most – Blatno train.',
    '<b>U12 Rakovník – Most, the trains at other minutes (since the hourly simplification, 14 October):</b> the Rakovník :19 trains (Os 6712 13:20, Os 6716 15:19, Os 6720 17:19, Os 6722 19:19) leave 10 min later than the game\'s :09 and have the same minutes from Hřivice on; Os 6714 (14:12) leaves 3 min later. Os 6707 (Most 13:03) waits 3 min at Svojetín and reaches Rakovník at :46. Os 6713 (Most 16:03) and Os 6709 (Most 14:03) leave Hřivice at :56 and reach Rakovník at :38. They are covered by the hourly line, not modelled one by one.',
    '<b>Most – Osek město:</b> beyond the end of the game\'s track (your note, 14 October). Every U12 train to or from Osek město ends or starts at Most in the game; also Os 6750 Most 4:00 → Osek město and the Osek ends of the Louny město trains below.',
    '<b>Rakovník – Osek outside the pattern:</b> the Most – Hřivice shorts (Os 6741 Most 12:03, Os 6743 18:03 → Hřivice; Os 6740 Hřivice 13:00 → Osek město, Os 6742 19:00 → Most); the Louny město – Most / Osek město trains (Os 6752, 6756, 6758, 6760, 6762 and back 6751, 6755, 6757, 6759, 6761, 6763); the morning and evening Louny – Rakovník and Rakovník – Most trains (Os 6704 – 6710, 6731 – 6735, 6730, 6703, 6719, 6753, 6750, Sp 1294 Louny 6:36 → Most).',
    '<b>U13 Most – Žatec západ outside the pattern:</b> there is no real train at Most 8:42 and 10:42 or from Žatec západ 8:30 and 10:30; the game runs those hours too. Os 6504 Žatec západ 6:30 waits 12 min at Postoloprty (Most 7:23), and Os 6500 4:31 runs 1 min later. The evening trains have other minutes: Os 6529 Most 21:08, Os 6531 22:16, Os 6528 Žatec západ 21:13, Os 6530 22:23.',
    '<b>Other trains on the U13 line:</b> R25 Most – Žatec – Plzeň (from Most at L:10, every 2 h) runs over the whole of U13\'s line. Sp 4052 Žatec – Postoloprty – Ústí nad Labem (U52) and the 4011 trains from Česká Lípa and Litoměřice to Postoloprty share parts of it. None of them is on this sheet. Your save has them as R25/1, R25/2 and Sp114, with no vehicles.',
    '<b>Lužná – Jirkov outside the pattern:</b> the Žatec – Jirkov shorts (Os 16821 10:02, 16823 14:02, 16827 22:02 from Jirkov; Os 16814 13:23, 16820 5:04 from Žatec), Os 16813 Žatec 15:34 → Lužná 16:17, Os 17680 Jirkov 4:48 → Chomutov, and the early and late Rakovník západ – Žatec trains (Os 16811, 16812).',
    '<b>No workday service:</b> Rakovník – Kralovice u Rakovníka (CIS 1058, weekends and holidays), Lužná u Rakovníka – Krupá – Kolešovice (summer weekends), the Zlonice – Straškov specials, and Libochovice – Straškov – Roudnice (CIS 4105, weekends).',
    # Kralupy and Straškov
    '<b>S40 peak extras (16 – 19):</b> from Kralupy 16:22, 17:23 (waits 4 min at Zvoleněves), 18:22, 18:52 to Slaný; from Slaný 17:00 (waits 4 min at Kralupy nad Vltavou předměstí) and 12:34. The pair Sp 1494 Praha-Holešovice 16:26 → Slaný and Sp 1495 Slaný 6:26 → Praha-Holešovice (one way each, morning and afternoon), and Os 9721 Slaný 4:24 → Neratovice.',
    '<b>Os Vraňany – Straškov extra round:</b> in the peak the unit runs one more trip to Horní Beřkovice, Vraňany 16:19 → 16:25 and back 16:29 → 16:35, between its 16:14 arrival and the 16:40 to Straškov. Morning trains at other minutes are not modelled either.',
    '<b>Os Roudnice – Bříza shorts:</b> Os 19641 Bříza obec 19:30 → Straškov and Os 19627 Straškov 19:35 → Roudnice.',
    '<b>Not part of this sheet:</b> S4 Praha – Kralupy – Vraňany – Roudnice nad Labem – Ústí (your scope: S4 excluded), Kralupy – Neratovice (CIS 1043, east of the Vltava), Louny – Postoloprty – Česká Lípa and Louny – Libochovice – Lovosice (CIS 4011), the other lines from Žatec (R25, 4052), Chomutov and Most, S65 at Hostivice and S75 Beroun – Rakovník (its own sheet).',
]
SHARED = {
    A_S5: [
        'Masarykovo nádraží is closed from 1 June to 12 December 2026, so every Praha train on this sheet starts and ends at Praha-Bubny (PID and the ČD works timetable). This is long-term, so it is modelled; the works that end in early November are not (your call, 14 October): Měcholupy – Žatec by bus until 9 November, and S75 Rakovník – Roztoky by bus until 8 November.',
        'S5 + S45 and R45 share Praha-Bubny – Hostivice – Kladno – Kladno-Ostrovec; R24 shares Praha-Bubny – Kladno, S50 and R24 share Kladno – Rakovník. From Praha-Bubny: R45 S:03, R24 L:03, S5 :34 every hour. From Kladno towards Rakovník: R24 L:43, S50 S:45.',
        'Towards Praha from Kladno: R45 L:14, R24 S:14, S5 :31. At Kladno-Ostrovec S5 + S45, R45 and the S45 shuttle meet: R45 in S:49 / out L:06, the shuttle in L:50 / out S:03.',
        'Rakovník: S50 in L:42 / out S:09, R24 in S:28 / out L:22. S75 from Beroun (its own sheet) and the Rakovník lines below also meet there.',
        'S54 meets S5 at Hostivice (S5 :01 – :02 out, :49 – :50 in; S54 out :31).',
    ],
    A_RK: [
        'S57, U12 and the Jirkov line start at Rakovník or Lužná u Rakovníka, on the S50 / R24 line. They share no track with each other beyond Rakovník. U13 (added 15 October) starts at Most, where U12 ends.',
        'Most: U12 stands :53 – :03, U13 :13 – :42, so one platform track is enough for both. Žatec: U13 stands :21 – :23 towards Žatec západ and :32 – :33 towards Most; the Jirkov line stands L:06 – L:23 (towards Jirkov) and S:36 – S:39, so at L:21 – L:23 there are two trains.',
        'Every hour from Rakovník: S57 to Blatno :48, U12 to Most :09. Into Rakovník: S57 from Blatno :40, U12 from Most :44.',
        'At Rakovník U12 to Most leaves at :09 every hour, the same minute as S50 to Kladno in the even hours. They leave on different lines (U12 via Chrášťany, S50 via Rakovník zastávka); in reality Os 6718 and Os 19715 both leave at 16:09.',
        'At Louny U12 towards Rakovník leaves at :37 every hour, the same minute as S40 Louny towards Slaný in the even hours. They leave on different lines (U12 via Louny předměstí, S40 via Cítoliby), so they do not meet; in reality Os 6713 and Os 9713 leave at 16:38 and 16:37.',
        'Lužná u Rakovníka: the Jirkov line comes in at L:24 and leaves at S:22. S50 towards Rakovník waits there :26 – :32.',
    ],
    A_KR: [
        'S40 Louny and S40 share Kralupy nad Vltavou – Slaný and run in alternate hours: from Kralupy L:55 to Louny, S:54 to Slaný; from Slaný L:34 (Louny train) and S:29.',
        'S44 shares Kralupy – Kralupy nad Vltavou předměstí with S40, then branches to Velvary: from Kralupy :26 every hour.',
        'Kralupy nad Vltavou is on the S4 line (not on this sheet). S5 from Kladno comes in at :04 and leaves at :49.',
    ],
    A_ST: [
        'The two lines meet at Straškov. The Vraňany line ends there (in L:06, out L:09); the Roudnice line passes it one stop before its end at Bříza obec.',
        'Vraňany and Roudnice nad Labem are on the S4 line, which is not on this sheet.',
    ],
}
HEAD = [
    '<title>Trains S5 to S4</title>',
    '<h1>Trains from S5 to the S4 corridor</h1>',
    '<p class="muted">Simutrans design for the workday trains between the S5 line (included) and the S4 line (not included): S5 Praha – Kladno – Kralupy with S45, R45, S50 and R24, S54, S40 Kralupy – Slaný – Louny, S44 Kralupy – Velvary, the lines from Rakovník (to Blatno u Jesenice, to Most, Lužná u Rakovníka – Žatec – Jirkov, U13 Most – Žatec západ) and the Straškov lines (Vraňany – Straškov, Roudnice – Bříza obec). '
    'Times are real JR2026 times from the national CIS JŘ timetable, for trains that run on all five days Mon–Fri 5–9 October 2026. Unit types are from vagonweb.cz. '
    'In the game the track ends at Blatno u Jesenice and, on the Rakovník – Louny line, at Most; every other line runs to its real termini.</p>',
    '<p class="small"><b>15 October 2026, v6:</b> U13 Most – Žatec západ added in full (your request): every hour Most :42 → Žatec západ :25, back :30 → Most :13, crossing at Volevčice (Os 6519 and Os 6520). 2 vehicles, 27 → 29 in all.</p>'
    '<p class="small"><b>14 October 2026, v5:</b> U12 now ends at Most, where the game\'s track ends (your note). Every hour Rakovník :09 → Most :53, Most :03 → Rakovník :44 (Os 6718 and Os 6711): 5 → 4 vehicles, 28 → 27 in all.</p>'
    '<p class="small"><b>14 October 2026, v4:</b> S57 (Rakovník – Blatno u Jesenice) and U12 (Rakovník – Osek město) are simplified to one uniform hourly pattern each, on real trains that cross at real crossing stations every hour (your request). S57: 4 → 2 vehicles, U12: still 5. 30 → 28 vehicles.</p>'
    '<p class="small"><b>14 October 2026, v3:</b> Masarykovo nádraží is closed until 12 December 2026, so S5 + S45, R45 and R24 now start and end at Praha-Bubny (R45 and R24 also stop at Praha-Výstaviště). S5 is shown as S5 + S45: the hourly train is one real train, S5 to Kladno-Ostrovec and S45 on to Kralupy. Vehicle counts are unchanged.</p>',
    '<p>Notation: <b>L</b> = odd hours, <b>S</b> = even hours. With every 120, odd hours come first: offset 55 means L:55, offset 114 means S:54. With every 60 the offset is the minute of every hour. '
    'Every 72 (Roudnice – Bříza obec) uses offset = (time − 60) mod 72. (x) = request stop. <span class="wait">Highlighted</span> rows are timed stops with a longer stay. '
    '"Leave up to" is 30 min on every entry of the lines every 120, and automatic on the lines every 60 and 72.</p>',
]

if __name__ == '__main__':
    base.run(LINES, OUT, LISTED, along=True, inv_svcs=INV, head=HEAD, shared=SHARED, not_modelled=NOT_MODELLED)
