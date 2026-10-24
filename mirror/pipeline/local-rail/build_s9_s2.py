"""S9, S2, R49, R17 and Ex7: the Praha – Benešov – Tábor – Veselí corridor and Praha – Lysá – Nymburk – Kolín / Milovice,
with the Praha-Uhříněves – Říčany works (12 Oct – 3 Nov 2026) as extra 'temporary' lines.

User (16 Oct 2026): "There should be file/artifact with S9/R17/R49/Ex7 (if some lines are not modelled in our files,
model them to common state). Well I'd like to keep the existing variants - but for each of them add the variant with
the current exclusion between Uhrineves and Ricany (or whatever), so I can model. If S9 is not modelled, please model
including S2 with more timetabled stops in good passing loops (otherwise it is too fast - similar problem to S4)."
Then: "those lines were done without looking at timetable so some positions may need updating" (the game's S9 and S2).

- R17 and Ex7 are the lines of build_ex7_r17.py (imported unchanged; its load() wrapper adds Veselí to Ex7).
- R49 Tábor and R49 Olbramovice are the lines of the archived build_benesov.py (imported unchanged; the local trains
  220 / 222 / 223 of that sheet stay archived).
- S9 and S2 are new on our sheets. The game already had them (save of 16 Oct, 08:36: Os221/1, Os221/2, Os231/1,
  Os231/2), set up without the timetable. They get the real minutes and timing points ('TP') at stations with passing
  loops, chosen so that no faster train follows closer than about 6 min there (follower check in the session notes).
- Works (PID, ČD works timetable VJR-vlaky-221, workdays 12 – 16, 19 – 23, 26, 27, 29, 30 Oct and 2, 3 Nov,
  5:20 – 21:30): single track Praha-Uhříněves – Říčany. Os 91xx (S9 Milovice) cut at Praha-Uhříněves; R49 out of Praha
  (and Sp 2474 in) also stop at Praha-Kolovraty and Strančice; R 728 / 730 / 732 stop at Říčany in the morning.
  Everything else keeps its minutes. load() makes copies '<train> výluka' with those changes (not in the workday
  list, so the inventory counts each train once).

Designed with ../rail-design-rules.md and build_012_014_235.py (real JR2026 CIS JŘ times, trains that run on all five
days Mon–Fri 5–9 Oct 2026). Writes "S9 S2 R17 R49 Ex7.html" in the project root.
Run: python pipeline/local-rail/build_s9_s2.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_012_014_235 as base  # noqa: E402
import build_ex7_r17 as ex7r17  # noqa: E402  (patches base.load: Veselí as a stop on Ex7)
import build_benesov as benesov  # noqa: E402

base.FULL.update({'P.-Hor. Počernice': 'Praha-Horní Počernice'})
OUT = os.path.join(base.ROOT, 'S9 S2 R17 R49 Ex7.html')
PH, UH, KO, RI, ST = 'Praha hl. n.', 'Praha-Uhříněves', 'Praha-Kolovraty', 'Říčany', 'Strančice'
IMP = 'important station'
TP = 'timing point, waits for its real minute'
WORKS = 'until 3 November'
A_S9 = 'S9 Milovice – Praha – Strančice / Benešov u Prahy'
A_S2 = 'S2 Praha – Lysá nad Labem – Nymburk – Kolín'
A_R49 = 'R49 Praha – Benešov – Tábor'
A_R17 = ex7r17.AREA

# works timetable (VJR-vlaky-221): extra stops, as {train: {station: departure minute}}; the arrival is the CIS passing time
WORKS_STOPS = {
    '2483': {KO: 16 * 60 + 31, ST: 16 * 60 + 44},
    '2474': {ST: 8 * 60 + 11, KO: 8 * 60 + 20},
}
WORKS_ARR = {('2474', PH): 8 * 60 + 40}  # Sp 2474 reaches Praha hl. n. at 8:40 instead of 8:39
WORKS_CUT = {'9147': (None, UH, 16 * 60 + 52), '9142': (UH, None, None)}  # Os 91xx start / end at Uhříněves (PDF: in 16:52)
# XS9 replacement bus (PID / ČD works timetable JR-linka-XS9, workdays 12 Oct – 3 Nov 2026; same minutes in the PID GTFS of
# 16 Oct). Afternoon pattern 12:32 – 19:47 from Háje every 15 min (:02 :17 :32 :47), from Říčany :10 :25 :40 :55.
# One trip each way as the line's legs; the stop names are the PID bus stop names.
XS9_OUT = [('Praha, Háje', None, 902), ('Praha, Háje (ul. Opatovská)', 904, 904), ('Praha, Sídliště Petrovice', 908, 908),
           ('Praha, Nádraží Uhříněves', 915, 915), ('Praha, Tehovičky', 925, 925), ('Praha, Škola Kolovraty', 926, 926),
           ('Říčany, Masarykovo nám.', 933, 933), ('Říčany, nádraží', 939, None)]
XS9_IN = [('Říčany, nádraží', None, 955), ('Praha, Škola Kolovraty', 961, 961), ('Praha, Tehovičky', 962, 962),
          ('Praha, Picassova', 969, 969), ('Praha, Nádraží Uhříněves', 970, 970), ('Praha, Sídliště Petrovice', 979, 979),
          ('Praha, Háje', 983, None)]
_load = base.load


def load():
    """the real data (with Ex7 at Veselí), plus works copies '<train> výluka'"""
    by_num, wd = _load()
    for num, extra in WORKS_STOPS.items():
        r = by_num[num]
        st = [dict(s_) for s_ in r['stops']]
        for nm, dep in extra.items():
            p = next(l for l in r['raw'] if base.full(l['name']) == nm)
            k = next(i for i, s_ in enumerate(st) if (s_['dep'] if s_['dep'] is not None else s_['arr']) > p['arr'])
            st.insert(k, {'name': nm, 'arr': p['arr'], 'dep': dep, 'req': False})
        for s_ in st:
            if (num, s_['name']) in WORKS_ARR:
                s_['arr'] = WORKS_ARR[(num, s_['name'])]
        by_num[num + ' výluka'] = dict(r, num=num, stops=st)
    for num, (a, b, arr) in WORKS_CUT.items():
        r = by_num[num]
        nm = [s_['name'] for s_ in r['stops']]
        st = [dict(s_) for s_ in r['stops'][nm.index(a) if a else 0:(nm.index(b) + 1) if b else len(nm)]]
        st[0]['arr'] = None
        st[-1]['dep'] = None
        if arr:
            st[-1]['arr'] = arr
        by_num[num + ' výluka'] = dict(r, num=num, stops=st)
    for num, st in (('XS9 Háje 15:02', XS9_OUT), ('XS9 Říčany 15:55', XS9_IN)):
        by_num[num] = {'num': num, 'svc': 'XS9', 'all5': True, 'raw': [],
                       'stops': [{'name': n, 'arr': a, 'dep': d, 'req': True} for n, a, d in st]}
    return by_num, wd


base.load = load


def pick(lines, i):
    return dict(next(L for L in lines if L['id'] == i))


r17, ex7 = pick(ex7r17.LINES, 'r17'), pick(ex7r17.LINES, 'ex7')
r49, r49o = pick(benesov.LINES, 'r49'), pick(benesov.LINES, 'r49o')
for L in (r49, r49o):
    L['area'] = A_R49
    L['inv_svcs'] = {'1149'}
WORKS_NOTE_UNCHANGED = 'During the Uhříněves – Říčany works (12 October – 3 November): unchanged. '

r17['notes'] = r17['notes'] + [
    WORKS_NOTE_UNCHANGED + 'The works timetable keeps every R17 minute. Only the morning R 732, 730 and 728 (Veselí 5:38, 6:38, 7:38 in the game\'s pattern) also stop at Říčany (6:52, 7:52, 8:52); a line running all day at one pattern cannot do that, so it is not modelled. ČD expects 5 – 10 min delays on the single track.']
ex7['notes'] = ex7['notes'] + [
    WORKS_NOTE_UNCHANGED + 'Ex7 is not in the works timetable (it covers regional trains only). Expect the same 5 – 10 min delays on the single track.']
r49['notes'] = r49['notes'] + [
    'During the Uhříněves – Říčany works: out of Praha it also stops at Praha-Kolovraty and Strančice; see R49 Tábor until 3 November. Towards Praha the afternoon trains (Sp 2478, 2480) are unchanged.']
r49o['notes'] = r49o['notes'] + [
    'During the Uhříněves – Říčany works: it also stops at Praha-Kolovraty and Strančice both ways; see R49 Olbramovice until 3 November.']

S9_OUT_TP = {('out', s): TP for s in ['Praha-Vršovice', 'Praha-Hostivař', UH, RI, ST, 'Senohraby', 'Čerčany']}
S9_IN_TP = {('in', s): TP for s in ['Čerčany', 'Senohraby', ST, RI]}
S9M_OUT_TP = {('out', s): TP for s in ['Čelákovice', 'Praha-Horní Počernice', 'Praha-Vysočany', 'Praha-Hostivař', UH]}
S9M_IN_TP = {('in', s): TP for s in [RI, UH, 'Praha-Hostivař', 'Praha-Vysočany', 'Praha-Horní Počernice']}

S9_LINES = [
    {
        'id': 's9b', 'name': 'S9 Benešov', 'area': A_S9, 'svc': '1009', 'every': 30, 'inv_svcs': {'1009'},
        'rep_out': '2549', 'rep_in': '2548',
        'wait_points': {**S9_OUT_TP, **S9_IN_TP},
        'notes': [
            'PID S9, the trains that run the whole way Praha hl. n. – Benešov u Prahy (KJŘ 221, CIS 1009, train numbers 25xx). Every 30 min all day: from Praha hl. n. at :21 and :51 (Benešov :23 and :53), from Benešov at :05 and :35 (Praha hl. n. :05 and :35). They start and end at Praha hl. n.; they do not run on to Lysá or Milovice.',
            'Five vehicles. 12 min at Benešov u Prahy (in :23, out :35) and 16 min at Praha hl. n. (in :35, out :51): the real minutes. The game line Os221/1 has 4 convoys; with the real minutes it needs 5.',
            'Timing points (real minutes, all at stations with passing loops): towards Benešov Praha-Vršovice :26, Praha-Hostivař :36, Praha-Uhříněves :42, Říčany :49, Strančice :56, Senohraby :05, Čerčany :13; towards Praha Čerčany :43, Senohraby :52, Strančice :02, Říčany :09. No faster train passes S9 Benešov after Praha-Hostivař going out: Ex7 (also :21 from Praha hl. n., on the parallel track) is past it by Vršovice, R49 and R17 leave Praha before it and stay ahead. R17 follows 6 – 9 min behind from Senohraby to Benešov.',
            'Towards Praha the last timing point is Říčany. After it R49 from Tábor (Sp 2478, 2480) closes in: it passes Uhříněves 4½ min and Hostivař 1 min after S9, and Ex7 is 4 min behind at Vršovice. So S9 is not held at Uhříněves, Hostivař or Vršovice towards Praha (the game line had Hostivař :22, dropped for that reason).',
            'Ex7 and S9 Benešov both leave Praha hl. n. at :21, in reality too: Ex7 passes Praha-Vršovice at :25 while S9 stands there :25 – :26 (four tracks to Hostivař). This is the one exception to the same-minute rule on this sheet; the real minutes are kept.',
            'During the Uhříněves – Říčany works: unchanged (the works timetable keeps every 25xx train). ČD expects 5 – 10 min delays on the single track.',
            'Vehicles: ČD 471 CityElefant, usually two units (vagonweb 2026, Os 2549).',
        ],
    },
    {
        'id': 's9m', 'name': 'S9 Milovice', 'area': A_S9, 'svc': '1009', 'every': 30, 'inv_svcs': {'1009'},
        'rep_out': '9147', 'rep_in': '9142',
        'wait_points': {**S9M_OUT_TP, **S9M_IN_TP},
        'notes': [
            'PID S9, the through trains Milovice – Lysá nad Labem – Praha hl. n. – Strančice (CIS 1009, train numbers 91xx). In the afternoon every 30 min: from Milovice at :03 and :33 (Praha hl. n. :22 – :31, Strančice :07 and :37), from Strančice at :22 and :52 (Praha hl. n. :28 – :34, Milovice :17 / :19 and :47).',
            'Seven vehicles. 15 min at Strančice (in :07, out :22) and 14 min at Milovice (in :19, out :33): the real minutes. The game line Os221/2 has 6 convoys; with the real minutes it needs 7.',
            'Timed both ways at Lysá nad Labem (7 min going out, :39 – :46) and Praha hl. n. (9 and 6 min): the real long stops.',
            'Timing points (real minutes, at stations with passing loops): towards Strančice Čelákovice :55, Praha-Horní Počernice :07, Praha-Vysočany :16, Praha-Hostivař :46, Praha-Uhříněves :52; towards Milovice Říčany :00, Praha-Uhříněves :08, Praha-Hostivař :14, Praha-Vysočany :41, Praha-Horní Počernice :50. The nearest faster trains: R17 passes Uhříněves 10 min after S9 going out (and stays behind it to Strančice); R49 Sp 2478 passes Hostivař 9½ min after it going in; R42 passes Horní Počernice 11½ min after it towards Lysá.',
            'Not timed, too close to a faster train: Praha-Vršovice going out (a train passes 3 min behind), Říčany going out (R17 6½ min behind), Praha-Vršovice going in (1 min), Čelákovice and Lysá going in (R42 6½ and 3 min behind).',
            'Midday the 91xx trains run Praha hl. n. – Říčany and Říčany – Milovice instead; in the afternoon peak all run Milovice – Strančice (listed below).',
            'During the Uhříněves – Říčany works: cut at Praha-Uhříněves, see S9 Milovice until 3 November.',
            'Vehicles: ČD 471 CityElefant (vagonweb 2026, Os 9147).',
        ],
    },
    {
        'id': 's9mv', 'name': 'S9 Milovice until 3 November', 'area': A_S9, 'svc': '1009', 'every': 30, 'inv_svcs': {'1009'},
        'temporary': 'the S9 Milovice vehicles, ' + WORKS, 'same_vehicles_as': 'S9 Milovice',
        'legs': ['9147 výluka', '9142 výluka'], 'cut_at': [UH],
        'wait_points': {k: v for k, v in {**S9M_OUT_TP, **S9M_IN_TP}.items() if k[1] not in (UH, RI)},
        'notes': [
            'S9 Milovice during the works between Praha-Uhříněves and Říčany (12 – 16, 19 – 23, 26, 27, 29, 30 October and 2, 3 November 2026, workdays 5:20 – 21:30; PID and the ČD works timetable VJR-vlaky-221). The Os 91xx trains do not run Praha-Uhříněves – Říčany – Strančice; they start and end at Praha-Uhříněves at their normal minutes (in :22 and :52, out :08 and :38).',
            'Six vehicles instead of seven: 16 min at Praha-Uhříněves (in :52, out :08), 14 min at Milovice. Uhříněves is a station with loops; the train turns there every 15 min, so it needs a free platform track for 16 min each time.',
            'The same timing points as S9 Milovice, except Uhříněves (now the terminus) and Říčany.',
            'Replacement: bus XS9 Háje (metro C) – Uhříněves – Říčany, every 15 min in the afternoon (see XS9).',
        ],
    },
]

S2K_OUT_TP = {('out', s): TP for s in ['Praha-Vysočany', 'Praha-Horní Počernice', 'Čelákovice', 'Lysá nad Labem', 'Poděbrady', 'Velký Osek']}
S2K_IN_TP = {('in', s): TP for s in ['Velký Osek', 'Poděbrady', 'Kostomlaty nad Labem', 'Lysá nad Labem', 'Čelákovice']}
S2N_OUT = ['Praha-Vysočany', 'Praha-Horní Počernice', 'Čelákovice', 'Lysá nad Labem']
S2N_IN = ['Lysá nad Labem', 'Čelákovice']
S2N_TP = {**{(n, s): TP for n in ('5831', '5843') for s in S2N_OUT}, **{(n, s): TP for n in ('5838', '5850') for s in S2N_IN}}

S2_LINES = [
    {
        'id': 's2k', 'name': 'S2 Kolín', 'area': A_S2, 'svc': '1002', 'every': 60, 'inv_svcs': {'1002'},
        'rep_out': '25837', 'rep_in': '25840', 'min_turn': 6,
        'wait_points': {**S2K_OUT_TP, **S2K_IN_TP},
        'notes': [
            'PID S2 Praha hl. n. – Lysá nad Labem – Nymburk hl. n. – Kolín (KJŘ 231, CIS 1002). Every hour from Praha hl. n. at :54 (Lysá :29 – :32, Nymburk :49 – :01, Kolín :26) and from Kolín at :32 (Nymburk :57 – :07, Lysá :24 – :26, Praha hl. n. :02).',
            'Four vehicles, as in the game (Os231/1). 6 min at Kolín (in :26, out :32) and 52 min at Praha hl. n. (in :02, out :54): the real minutes. CIS JŘ has no empty run to the Kolín sidings for these trains, so the game\'s depot stop (Kolín - odstavné koleje sever, offset 25) is not real; with the real 6-min turn there is no time for it. Drop it and set Kolín (offset 32) as the terminus.',
            'Nymburk hl. n. is timed both ways by the 5-minute rule (12 min going out, 10 min going in): R10 overtakes S2 there in both directions.',
            'Timing points (real minutes, at stations with passing loops): towards Kolín Praha-Vysočany :01, Praha-Horní Počernice :10, Čelákovice :22, Lysá nad Labem :32, Poděbrady :10, Velký Osek :18; towards Praha Velký Osek :40, Poděbrady :48, Kostomlaty nad Labem :14, Lysá nad Labem :26, Čelákovice :35.',
            'Not timed: Kostomlaty and Kamenné Zboží going out (R10 passes 5 – 6 min behind and overtakes at Nymburk), Praha-Horní Počernice and Praha-Vysočany going in (R42 7 and 6½ min behind, all the way into Praha). Going in, R10 follows 6 – 7 min behind at Velký Osek and Poděbrady and overtakes at Nymburk, where S2 waits 10 min; R10 is timed at Nymburk in the game, so a held S2 costs it nothing.',
            'During the Uhříněves – Říčany works: not affected (another line).',
            'Vehicles: ČD 471 CityElefant (vagonweb 2026, Os 25837, Os 25840).',
        ],
    },
    {
        'id': 's2n', 'name': 'S2 Nymburk', 'area': A_S2, 'svc': '1002', 'every': 120, 'step': 60, 'inv_svcs': {'1002'},
        'legs': ['5831', '5838', '5843', '5850'],
        'wait_points': S2N_TP,
        'notes': [
            'PID S2, the trains that end at Nymburk hl. n. Every hour from Praha hl. n. at :19, in two real patterns that alternate: in even hours to Nymburk :13 (Lysá :54 – :56), in odd hours to Nymburk :19 (8 min at Lysá, :54 – :02). Back from Nymburk at :37 in odd hours (7 min at Lysá, :54 – :01) and at :43 in even hours (Lysá :00 – :01), both to Praha hl. n. :37.',
            'One circuit through both patterns, as one real unit does it: Praha S:19 → Nymburk L:13, back L:37 → Praha S:37; Praha L:19 → Nymburk S:19, back S:43 → Praha L:37. Every 120, so Praha hl. n. has an S2 to Nymburk every hour at :19. Real afternoon: 14:19 → 15:13, 15:37 → 16:37, 17:19 → 18:19, 18:43 → 19:37 (Os 5831, 5838, 5843, 5850).',
            'Three vehicles (the game line Os231/2 has 2). 24 min at Nymburk each time, 42 min at Praha hl. n. each time: the real minutes. The alternation is real: the long Lysá stops are where R23 (every 2 h) overtakes S2.',
            'Timing points: towards Nymburk Praha-Vysočany :26, Praha-Horní Počernice :35, Čelákovice :47, Lysá nad Labem (:56 or :02); towards Praha Lysá nad Labem (:01) and Čelákovice :10. Not timed going in after Čelákovice: R10 follows into Praha 3½ – 5½ min behind.',
            'The S2 Kolín and S2 Nymburk trains are all 471s, but vagonweb has no unit sightings that show the two moving between each other, so they stay two lines as in the game. One circuit Praha → Nymburk → Praha → Kolín → Praha would cut the Praha hl. n. stays to 17 min (in :02 → out :19, in :37 → out :54); say if you want it.',
            'During the Uhříněves – Říčany works: not affected (another line).',
            'Vehicles: ČD 471 CityElefant (vagonweb 2026, Os 5831, 5838, 5843, 5850). After Os 5850 the unit runs empty to Praha Jih for the night.',
        ],
    },
]

R49_WORKS = [
    dict(r49, id='r49v', name='R49 Tábor until 3 November', temporary='the R49 Tábor vehicles, ' + WORKS, same_vehicles_as='R49 Tábor',
         rep_out='2483 výluka', rep_in='2478',
         notes=['R49 Tábor during the Uhříněves – Říčany works: out of Praha it also stops at Praha-Kolovraty (:31) and Strančice (:44), at its normal minutes (it passed both at :30½ and :44). Every other minute is the same (Říčany :33 – :38 going out). Towards Praha it is unchanged: Sp 2478 and 2480 are not on the works list.',
                'Timetable entries: the same as R49 Tábor. Only the stop list changes (two more stops going out).']),
    dict(r49o, id='r49ov', name='R49 Olbramovice until 3 November', temporary='the R49 Olbramovice vehicles, ' + WORKS, same_vehicles_as='R49 Olbramovice',
         legs=[{'cut': ('2483 výluka', 'Praha-Holešovice', 'Olbramovice')}, {'cut': ('2474 výluka', 'Olbramovice', 'Praha-Holešovice')}],
         notes=['R49 Olbramovice during the Uhříněves – Říčany works: it also stops at Praha-Kolovraty and Strančice both ways (out :31 and :44, back Strančice :11 and Kolovraty :20, the minutes of Sp 2483 and Sp 2474 in the works timetable). Back it reaches Praha hl. n. 1 min later (:40 instead of :39) and still leaves at :41.',
                'Timetable entries: the same as R49 Olbramovice. Only the stop list changes (two more stops each way).']),
]
for L in R49_WORKS:
    L.pop('extra_real', None)

A_XS9 = 'XS9 replacement bus Praha, Háje – Říčany (until 3 November)'
XS9_LINE = {
    'id': 'xs9', 'name': 'XS9', 'area': A_XS9, 'svc': 'XS9', 'every': 15, 'cat': 'bus', 'inv_svcs': {'XS9'},
    'temporary': 'buses, only until 3 November', 'min_turn': 5,
    'legs': ['XS9 Háje 15:02', 'XS9 Říčany 15:55'],
    'wait_points': {('out', 'Praha, Nádraží Uhříněves'): 'transfer to S9, waits for its real minute',
                    ('in', 'Praha, Nádraží Uhříněves'): 'transfer to S9, waits for its real minute'},
    'notes': [
        'PID XS9, the replacement bus for the S9 trains cut at Praha-Uhříněves (PID / ČD works timetable JR-linka-XS9; the same minutes are in the PID open data of 16 October). Workdays 12 October – 3 November 2026, about 5:15 – 21:15: every 10 min in the morning peak, every 15 min in the afternoon (12:32 – 19:47 from Háje), every 30 min otherwise. The game runs the afternoon pattern all day.',
        'Every 15 min from Praha, Háje (metro C) at :02, :17, :32, :47: Sídliště Petrovice +6, Nádraží Uhříněves +13, Tehovičky +23, Škola Kolovraty +24, Říčany, Masarykovo nám. +31, Říčany, nádraží +37 (it goes through Uhříněves and Kolovraty on the town roads, near the railway, not on the D1). Back from Říčany, nádraží at :10, :25, :40, :55: Škola Kolovraty +6, Tehovičky +7, Picassova +14, Nádraží Uhříněves +15, Sídliště Petrovice +24, Háje +28. Opatovská and Masarykovo nám. are served only towards Říčany, Picassova only towards Háje. Every stop is a request stop.',
        'Six buses (round trip 1 h 30 min at every 15). It turns 16 min at Říčany, nádraží (in :39, out :55) and 9 min at Háje (in :23, out :32), with a 5-min minimum turn. The real bus count is not published: seznam-autobusu.cz has no XS9 records (nor for the same closure in November 2025), and the PID open data has no vehicle blocks. With a 1-min turn at Říčany (in :39, out :40) five buses would do; I assumed the bus needs at least 5 min there.',
        'Timed at Praha, Nádraží Uhříněves both ways, the stop for the trains (S9 Milovice ends there during the works: trains in :22 / :52, out :08 / :38). The bus is untimed elsewhere; it waits at Uhříněves for its real minute.',
        'Game stops: Praha, Háje [C]; Praha, Sídliště Petrovice; Praha, Nádraží Uhříněves and Praha, Picassova (the Uhříněves station halt); Praha, Tehovičky (the Kolovraty station halt); Praha, Škola Kolovraty; Říčany, Masarykovo náměstí; Říčany, Nádraží (the Říčany station halt). The save already has an empty line "100999 {XS9} Říčany,žel.st.-Praha,Háje" (no buses, via Wolkerova): replace its schedule with this one.',
        'Vehicle: MAN Lion\'s Intercity LE 12, PID grey-red (pak object VZ-Praha-Lions_Intercity_LE_12-pidsedocervena-Lions_Intercity_LE_12; depot name "Praha MAN Lion\'s Intercity LE 12 autobus (PID šedo-červená · Vega Tour)"), 90 passengers, 100 km/h. The carrier is České dráhy, which hires the buses; no source names the bus company or its buses, so this is the pakset session\'s suggestion for a 12 m suburban bus, not a confirmed match. If 12 m is too small: MAN Lion\'s City L (14.7 m, 125 passengers).',
    ],
}

LINES = S9_LINES + S2_LINES + [r49, r49o] + R49_WORKS + [r17, ex7, XS9_LINE]


def single_track():
    """who uses Praha-Uhříněves – Říčany in one hour of the works (both directions), from the real minutes"""
    by_num, wd = base.load()
    rows = []
    for num in ['2549', '2551', '2548', '2550', '2483 výluka', '2478', '537', '530', '721', '712']:
        r = by_num[num]
        t = {base.full(l['name']): (l.get('arr'), l.get('dep')) for l in r['raw']}
        if num in WORKS_STOPS or num.endswith('výluka'):
            t.update({s_['name']: (s_['arr'], s_['dep']) for s_ in r['stops']})
        u, ri = t[UH], t[RI]
        if (u[1] or u[0]) < (ri[0] or ri[1]):
            rows.append((u[1] if u[1] is not None else u[0], ri[0] if ri[0] is not None else ri[1], 'towards Říčany', r))
        else:
            rows.append((ri[1] if ri[1] is not None else ri[0], u[0] if u[0] is not None else u[1], 'towards Uhříněves', r))
    name = {'1009': 'S9', '1149': 'R49', '17': 'R17', '7': 'Ex7'}
    occ = sorted(((int(a) % 60, int(b) % 60 + (60 if int(b) % 60 < int(a) % 60 else 0), d, name[r['svc']], r['num']) for a, b, d, r in rows))
    print('Uhříněves – Říčany, minutes in each hour (works):')
    for a, b, d, c, n in occ:
        print(f'   :{a:02d} – :{b % 60:02d}  {d:18} {c} {n}')
    clashes = [(x, y) for i, x in enumerate(occ) for y in occ[i + 1:] if x[2] != y[2] and x[0] < y[1] and y[0] < x[1]]
    print('   opposite trains on the section at the same time:', [(f'{x[3]} {x[4]}', f'{y[3]} {y[4]}') for x, y in clashes])
    return occ, clashes


LISTED = {
    # S9: midday shorts and odd workings
    ('Praha hl. n.', RI), (RI, PH), (RI, 'Milovice'), ('Milovice', RI), (PH, ST), (ST, PH),
    ('Praha-Horní Počernice', ST), (ST, 'Praha-Horní Počernice'), (ST, 'Lysá nad Labem'), ('Čerčany', 'Benešov u Prahy'),
    ('Praha-Vysočany', PH), (PH, 'Praha-Vysočany'), ('Milovice', PH), (PH, 'Milovice'), ('Milovice', 'Lysá nad Labem'), ('Lysá nad Labem', 'Milovice'),
    ('Lysá nad Labem', PH), (PH, 'Lysá nad Labem'), ('Milovice', 'Praha-Vysočany'), ('Praha-Vysočany', 'Milovice'),
    # S2 odd workings
    ('Kolín', 'Nymburk hl. n.'), ('Nymburk hl. n.', 'Kolín'), ('Poděbrady', PH), (PH, 'Poděbrady'),
    ('Nymburk hl. n.', PH), (PH, 'Nymburk hl. n.'), ('Kolín', PH), (PH, 'Kolín'),
    ('Velký Osek', 'Nymburk hl. n.'), ('Nymburk hl. n.', 'Velký Osek'),  # Kolín – Nymburk peak trains (also stop at Veltruby)
    # the S9 shorts and odd workings as seen from S9 Milovice until 3 November (Praha – Uhříněves part)
    (PH, UH), (UH, PH), (UH, 'Lysá nad Labem'), (UH, 'Praha-Horní Počernice'), ('Praha-Horní Počernice', UH),
    # R49 short and morning trains, R17 / Ex7 short trains (as on the earlier sheets)
} | benesov.LISTED | ex7r17.LISTED

NOT_MODELLED = [
    '<b>Works, not modelled:</b> the morning R17 stops at Říčany (R 732, 730, 728 at 6:52, 7:52, 8:52) and the early R49 Sp 2470, 2472, 2476 stops at Strančice and Praha-Kolovraty (morning only). XS9 runs every 10 min in the morning and every 30 min outside the peaks; the game runs its afternoon 15-min pattern all day. The works timetable covers only 5:20 – 21:30.',
    '<b>S9 outside the afternoon pattern:</b> midday Praha hl. n. :01 / :31 – Říčany and Říčany :29 / :59 – Milovice (Os 9129 – 9136), the evening Milovice – Říčany and Strančice – Praha hl. n. trains, and single odd workings (Praha-Horní Počernice 14:37 – Strančice, Strančice – Lysá, Os 26100 Čerčany – Benešov – Sedlčany). The line slots cover those hours.',
    '<b>S22 Praha – Lysá – Milovice:</b> no trains in the afternoon peak (see the S4 sheet); S9 Milovice serves Milovice then.',
    '<b>S2 outside the afternoon pattern:</b> the peak Kolín – Nymburk trains (Os 5870 17:59, 5872 18:59), Lysá nad Labem 15:01 – Praha (Os 5834), the Poděbrady trains, the evening 18:54 → Kolín and 19:54 → Nymburk (Os 5849, 5853) at other minutes, and the morning and evening trains.',
    '<b>Other lines on this track, not on this sheet:</b> R42 Praha – Kolín, R10, R22, R23, S32, S12, S21, S23 (already in the game or on the S4 sheet), S8 / Posázavský pacifik (210) from Praha hl. n. to Čerčany, the local trains 220 / 222 / 223 around Benešov (archived R49 / Benešov sheet), and the branches at Benešov, Olbramovice, Tábor and Veselí.',
] + [s_ for s_ in ex7r17.NOT_MODELLED if not s_.startswith(('<b>Engineering works', '<b>Not part of this sheet'))] + [
    s_ for s_ in benesov.NOT_MODELLED if s_.startswith('<b>R49')]

SHARED = {
    A_S9: [
        'Praha hl. n. – Strančice has S9 every 15 min: towards Strančice S9 Benešov :21 and :51, S9 Milovice :01 and :31 (from Praha hl. n.); towards Praha from Strančice S9 Milovice :22 and :52, S9 Benešov :02 and :32. Beyond Strančice S9 Benešov runs alone, every 30 min.',
        'At Praha hl. n. S9 Benešov ends and starts (in :05 / :35, out :21 / :51); S9 Milovice runs through with 9 min (in :22, out :31) and 6 min (in :28, out :34).',
        'R49 (:15 from Praha hl. n.), R17 (:46) and Ex7 (:21) share Praha – Benešov. None of them overtakes S9 after Praha-Hostivař, so S9 can be timed at the stations in between; the details are under each line.',
        'During the works (12 October – 3 November): Praha-Uhříněves – Říčany is single track. S9 Milovice ends at Uhříněves (S9 Milovice until 3 November); S9 Benešov keeps its minutes. See "Single track" below.',
    ],
    A_S2: [
        'From Praha hl. n. S2 leaves at :19 (to Nymburk) and :54 (to Kolín); into Praha at :02 (from Kolín) and :37 (from Nymburk). Praha hl. n. – Lysá also has S9 Milovice every 30 min (from Praha :04 and :34 towards Milovice).',
        'At Nymburk hl. n. S2 Kolín waits 12 min going out (:49 – :01) and 10 min coming back (:57 – :07); S2 Nymburk turns there (in :13 / :19, out :37 / :43).',
        'Checked against the game lines that share this track: R10 leaves Nymburk at :55 (towards Hradec) and :02 (towards Praha), R42 :28 / :27, R23 L:45 / S:12, R22 L:08 / S:49; S2 leaves Nymburk at :01 (S2 Kolín), :07 (S2 Kolín back) and :37 / :43 (S2 Nymburk). No two leave in the same minute.',
    ],
    A_R49: benesov.SHARED['R49 Praha – Tábor'][:2] + [
        'R49 shares Praha – Benešov with S9 (every 30 min) and R17 and Ex7 (every hour), all on this sheet.',
        'During the works: both R49 lines also stop at Praha-Kolovraty and Strančice going out of Praha, and R49 Olbramovice also coming back. The minutes stay the same; the "until 3 November" versions only add the stops.',
    ],
    A_XS9: [
        'XS9 meets S9 at Praha, Nádraží Uhříněves (the Uhříněves station): during the works S9 Milovice ends there (in :22 / :52, out :08 / :38) and the bus leaves for Říčany at :00, :15, :30, :45. Towards Praha the bus reaches Uhříněves at :10, :25, :40, :55 and Háje (metro C) 13 min later.',
        'Its vehicles are extra buses for the works only; they are not counted in the sheet total.',
    ],
    A_R17: ex7r17.SHARED[A_R17] + [
        'During the works: both unchanged in the afternoon. They run over the single track between Praha-Uhříněves and Říčany, where ČD expects 5 – 10 min delays.',
    ],
}


def head(occ, clashes):
    ot = '; '.join(f'{d}: ' + ', '.join(f'{c} :{a:02d} – :{b % 60:02d}' for a, b, d_, c, n in occ if d_ == d)
                   for d in ('towards Říčany', 'towards Uhříněves'))
    cl = '; '.join(f'{x[3]} :{x[0]:02d} – :{x[1] % 60:02d} {x[2]} and {y[3]} :{y[0]:02d} – :{y[1] % 60:02d} {y[2]}' for x, y in clashes)
    return [
        '<title>S9 S2 R17 R49 Ex7</title>',
        '<h1>S9 · S2 · R49 · R17 · Ex7</h1>',
        '<p class="muted">Simutrans design for the Praha – Benešov u Prahy – Tábor – Veselí nad Lužnicí corridor (S9, R49, R17, Ex7) and Praha – Lysá nad Labem – Nymburk – Kolín / Milovice (S2, S9 Milovice). '
        'Times are real JR2026 times from the national CIS JŘ timetable, for trains that run on all five days Mon–Fri 5–9 October 2026. R17 and Ex7 are as on the Ex7 · R17 sheet, R49 as on the archived R49 / Benešov sheet; S9 and S2 are new here. Unit types are from vagonweb.cz.</p>',
        '<p class="fix"><b>16 October 2026:</b> S9 and S2 were in the game (save of 16 October, 08:36: Os221/1, Os221/2, Os231/1, Os231/2) but set up without the timetable, so they ran too fast, as S4 did. They now have the real minutes and timing points at stations with passing loops. Changes against the game: S9 Benešov 4 → 5 vehicles, S9 Milovice 6 → 7, S2 Nymburk 2 → 3 (one circuit through both real patterns), S2 Kolín stays 4 but loses the depot stop at Kolín.</p>',
        '<p class="fix"><b>Works Praha-Uhříněves – Říčany, 12 October – 3 November 2026</b> (workdays 12 – 16, 19 – 23, 26, 27, 29, 30 October and 2, 3 November, 5:20 – 21:30; PID and ČD works timetable VJR-vlaky-221): one track only. Each line has its normal version, and where the works change it, a second version "until 3 November" (not counted again in the totals): '
        'S9 Milovice ends at Praha-Uhříněves (6 vehicles instead of 7); R49 also stops at Praha-Kolovraty and Strančice; the replacement bus XS9 Háje – Říčany is added (6 buses). Unchanged: S9 Benešov, R17, Ex7 (afternoon) and S2.</p>',
        '<h2 id="works">What the works are</h2><ul>'
        '<li><b>Why:</b> the Pražský okruh (D0) motorway ring is being built across the Praha – Benešov railway (KJŘ 221) near Říčany. For the construction, Správa železnic moved the railway onto a temporary alignment (provizorní přeložka) around the building site; that switch was the previous closure, 1 – 14 November 2025, with the same pattern of restrictions and the same XS9 bus. Now, about a year later, the line goes back from the temporary alignment to its original (final) position.</li>'
        '<li><b>Where and what:</b> between Praha-Uhříněves and Říčany (the stretch with the Praha-Kolovraty halt). Only one main-line track is in use; the other is being moved and connected. Trains in both directions share the one track, so they must wait for each other at Uhříněves or Říčany.</li>'
        '<li><b>When:</b> 11 October – 3 November 2026. The changed train timetable applies on workdays 12 – 16, 19 – 23, 26, 27, 29, 30 October and 2, 3 November, 5:20 – 21:30 (not 28 October, a holiday). Weekends and late evenings keep the normal timetable, with possible delays.</li>'
        '<li><b>Effect on trains (ČD works timetable VJR-vlaky-221):</b> the S9 trains numbered Os 91xx (the Milovice / Praha – Říčany / Strančice trains, about half of S9) do not run Praha-Uhříněves – Říčany – Strančice; they start and end at Uhříněves at their normal minutes. S9 to Benešov (Os 25xx) runs normally. R49 (Sp 2470 – 2476, 2479 – 2487) also stops at Strančice and Praha-Kolovraty, at its normal minutes. R 732, 730 and 728 (morning, towards Praha) also stop at Říčany. R17, Ex7 and the afternoon R49 from Tábor keep their timetable. ČD expects 5 – 10 min delays on the single track.</li>'
        '<li><b>Replacement:</b> bus XS9 Praha, Háje (metro C) – Uhříněves – Kolovraty – Říčany, every 10 / 15 / 30 min on workdays, PID and ČD tickets valid (modelled below).</li>'
        '<li><b>Sources:</b> <a href="https://pid.cz/vyluka-mezi-uhrinevsi-a-ricany-omezeni-s9-a-autobusova-linka-xs9/">PID notice</a>, <a href="https://pid.cz/wp-content/uploads/2026/10/VJR-vlaky-221.pdf">ČD works timetable (PDF)</a>, <a href="https://pid.cz/wp-content/uploads/2026/10/JR-linka-XS9.pdf">XS9 timetable (PDF)</a>, <a href="https://mhd86.cz/2026/10/10/mezi-uhrinevsi-a-ricany-zacne-jednokolejny-provoz-vlaky-s9-doplni-autobusova-linka-xs9-na-haje/">mhd86.cz</a>, <a href="https://www.ceskedrahy.cz/tiskove-centrum/tiskove-zpravy/stavebni-prace-omezi-provoz-vlaku-v-oblasti-rican-lyse-nad-labem">ČD press release on the 2025 closure</a>.</li></ul>',
        '<p><b>Single track:</b> in one hour these trains use Uhříněves – Říčany (minutes from the real timetable): ' + ot + '. '
        + (f'{len(clashes)} times an hour two trains would be on it in opposite directions at once ({cl}), which is why ČD expects 5 – 10 min delays; the works timetable does not change these minutes. If you make the section single track in the game, the signals will hold trains in the same way, and the timing points after it (Strančice and Senohraby towards Benešov; Praha-Hostivař for S9 Milovice towards Praha) win some of the time back.' if clashes else 'They never meet.')
        + '</p>',
        '<p>Notation: <b>L</b> = odd hours, <b>S</b> = even hours. On the lines every 15, 30 and 60 the offset is the minute (every 15 and 30: the first of the minutes). On the lines every 120 odd hours come first: offset 19 means every 2 h at L:19, and even hours add 60 (offset 79 means S:19). '
        '<span class="wait">Highlighted</span> rows are timed stops with a longer stay. "Timing point" entries hold the train to its real minute at a station with a passing loop. "Leave up to" is 30 min on every entry of the lines every 120, and automatic on the lines every 15, 30 and 60.</p>',
    ]


if __name__ == '__main__':
    occ, clashes = single_track()
    base.run(LINES, OUT, LISTED, along=True, inv_svcs={'7', '17', '1149', '1009', '1002'}, head=head(occ, clashes),
             shared=SHARED, not_modelled=NOT_MODELLED)
