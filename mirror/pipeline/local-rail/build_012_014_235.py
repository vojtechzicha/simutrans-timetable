"""Local trains 012 (Pečky – Kouřim), 014 (Kolín – Ledečko), 235 (Kutná Hora – Zruč nad Sázavou) and the
Posázavský pacifik: 210 (Praha – Vrané nad Vltavou – Čerčany / Dobříš) and 212 (Čerčany – Zruč nad Sázavou –
Světlá nad Sázavou, with the Zruč trains running on to Havlíčkův Brod).

Designed 5 Oct 2026 (012, 014, 235) and 8 Oct 2026 (210, 212) with the rules in ../rail-design-rules.md. Every time on the page is a real JR2026 time from
../md-cr/data/derived/trains.json (CIS JŘ), for trains that run on all five days Mon–Fri 5–9 Oct 2026.
Offsets follow the user-confirmed rule: odd hours first, offset = (time − 60) mod interval.
Writes "archive/Local Trains 012 014 210 212 235.html" (archived 9 Oct 2026).
Run: python pipeline/local-rail/build_012_014_235.py
"""
import datetime as dt
import html
import math
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
TRAINS = os.path.join(ROOT, 'pipeline', 'md-cr', 'data', 'derived', 'trains.json')
OUT = os.path.join(ROOT, 'archive', 'Local Trains 012 014 210 212 235.html')  # archived 9 Oct 2026
PA = {'0001', '0028', '0029', '0030'}
WEEK = [dt.date(2026, 10, d) for d in range(5, 10)]
LONG_STAY = 5
WAIT = ' class="wait"'
MIN_TURN = 10
DEPOTS = {'Praha odstavné nádraží', 'Praha-Malešice'}  # stops without passengers (depot ends; Malešice: R26)

FULL = {
    'Kutná Hora hl. n.': 'Kutná Hora hl. n.',
    'Zruč n.S.': 'Zruč nad Sázavou',
    'St. Město u U.H.': 'Staré Město u Uherského Hradiště',
    'Ledeč n.S.': 'Ledeč nad Sázavou',
    'Rožmitál p.Třemšínem': 'Rožmitál pod Třemšínem',
    'Světlá n.S.': 'Světlá nad Sázavou',
}

# The design: one representative real train each way; everything else is derived from the data.
LINES = [
    {
        'id': 'l012', 'name': '012', 'area': 'Kolín area', 'svc': '1011', 'every': 120,
        'rep_out': '19328', 'rep_in': '19325',
        'wait_points': {('in', 'Plaňany'): 'crossing with the train to Bošice'},
        'notes': [
            'Real afternoon trains to Kouřim leave Pečky at 16:12 and 18:12 and Kouřim at 17:10 and 19:10; the line runs that 2-hour pattern all day. The real midday pair (Pečky 13:12, Kouřim 14:10) is in the other hours, where the game runs 012 short.',
            'It crosses 012 short at Plaňany: the train to Pečky waits there (17:27 – 17:29) for the train to Bošice (17:29), so Plaňany is timed in that direction.',
        ],
    },
    {
        'id': 'l012b', 'name': '012 short', 'area': 'Kolín area', 'svc': '1011', 'every': 120,
        'rep_out': '19324', 'rep_in': '19321',
        'wait_points': {('in', 'Plaňany'): 'crossing with the train to Kouřim'},
        'notes': [
            'In reality a train leaves Pečky at :12 every hour in the afternoon, to alternating ends: 13:12 Kouřim, 14:12 and 15:12 Bošice, 16:12 Kouřim, 17:12 Plaňany zastávka, 18:12 Kouřim, 19:12 Bošice. 012 short carries the Bošice trains in the odd hours (Pečky L:12, Bošice S:16), between the Kouřim trains.',
            'It crosses 012 at Plaňany: the train to Pečky waits there (16:27 – 16:29) for the train to Kouřim (16:29).',
            'The real 17:12 Plaňany zastávka train and the 14:12 Bošice train in an even hour run in the game as 012 short and 012.',
            'vagonweb (2026): all 012 trains are 810; unit 810 298 ran both Kouřim and Bošice trains on 18 June. One shared line would not shorten the Pečky stay, because every train comes in at :46 and leaves at :12, so 012 and 012 short stay separate lines (same vehicle count).',
        ],
    },
    {
        # one circuit (user, 5 Oct 2026: keep the stays at the main-line stations short; share a line only where the
        # same vehicles really run both parts). vagonweb 2026: all 014 trains are planned 814 RegioNova, and on Thu
        # 18 Jun 2026 units 814 078, 113 and 009 were seen alternating Ledečko and Uhlířské Janovice runs at Kolín.
        'id': 'l014', 'name': '014', 'area': 'Kolín area', 'svc': '1018', 'every': 120,
        'legs': ['22212', '22213', '22222', '22225'],
        'terminal': ['Kolín'],
        'wait_points': {('22213', 'Ratboř'): 'crossing with the train to Ledečko',
                        ('22225', 'Ratboř'): 'crossing with the train to Uhlířské Janovice'},
        'notes': [
            'One line for both branches, as the real vehicles run: a train comes in from Ledečko at L:16 and leaves for Uhlířské Janovice at L:47; it comes back at S:16 and leaves for Ledečko at S:47. So it stays 31 min at Kolín each time instead of 1 h 31 min, and the line needs 3 vehicles instead of 4.',
            'vagonweb (2026): all these trains are planned as 814 RegioNova. On Thursday 18 June 2026 unit 814 078 ran Ledečko 12:07 → Kolín → Uhlířské Janovice 13:47 → Kolín 16:16 → Ledečko 16:47, and 814 113 ran Kolín 12:47 → Ledečko → Kolín 15:16 → Uhlířské Janovice 15:47 → Kolín 18:16.',
            'Both Kolín entries are set to stop type terminal, so everyone gets off and nobody rides through from one branch to the other.',
            'Kolín has a train every hour at :47 (Ledečko in even hours, Uhlířské Janovice in odd hours), as in reality.',
            'The trains cross at Ratboř every hour: the train to Kolín waits there 4 min (:58 – :02) for the train going out (:01), so Ratboř is timed towards Kolín on both branches.',
            'At Uhlířské Janovice the train waits 1 h 06 min (in S:27, out L:33), as the real trains do; at Ledečko 14 min.',
        ],
    },
    {
        'id': 'l235', 'name': '235', 'area': 'Kutná Hora area', 'svc': '1028', 'every': 120,
        'rep_out': '19217', 'rep_in': '19222',
        'extra_real': {'out': ['19221', '19223'], 'in': ['19206']},  # run on to / start at Zruč nad Sázavou zastávka
        'wait_points': {},
        'notes': [
            'Two trains, as in reality. They cross at Zbraslavice: the train to Kutná Hora waits 17 min there (15:44 – 16:01) for the train to Zruč.',
            'At Malešov the train to Kutná Hora waits 5 min (16:23 – 16:28) and crosses 235 short going out to Zbraslavice.',
            'The real 17:05 and 19:05 trains from Kutná Hora run one stop further, to Zruč nad Sázavou zastávka; the line ends at Zruč nad Sázavou like the other trains.',
        ],
    },
    {
        'id': 'l235z', 'name': '235 short', 'area': 'Kutná Hora area', 'svc': '1028', 'every': 120,
        'rep_out': '19219', 'rep_in': '19226',
        'wait_points': {},
        'notes': [
            'The real afternoon short trains Kutná Hora – Zbraslavice (Zbraslavice 15:01 and 17:01, Kutná Hora 16:05) run in the hours between the Zruč trains, so Kutná Hora – Zbraslavice has a train every hour, as it does in the real afternoon. One train, as in reality.',
            'This train starts its afternoon as Os 19215 from Kolín (13:41, via Kutná Hora hl. n. 13:56, at Zbraslavice 14:49). That one through run from Kolín is not modelled; the line covers its Zbraslavice return.',
            'At Malešov it waits 5 min going to Kutná Hora (15:23 – 15:28) and crosses the 235 train to Zruč.',
        ],
    },
    {
        'id': 'l235m', 'name': '235 město', 'area': 'Kutná Hora area', 'svc': '1028', 'every': 120,
        'rep_out': '19275', 'rep_in': '19270',
        'wait_points': {},
        'notes': [
            'The real Kutná Hora hl. n. – Kutná Hora město shuttles: in the afternoon from hl. n. 15:16, 17:14, 19:14 and from město 14:32, 16:32, 18:32. One train, every 2 h: hl. n. L:14, město S:32.',
            'It waits 1 h 10 min at Kutná Hora město and 34 min at hl. n. At město it stands while the 235 trains pass (L:13 and S:13 towards Zruč or Zbraslavice, :40 – :44 towards hl. n.).',
            'From Kutná Hora hl. n. towards město this line (L:14) follows the 235 train to Zruč (L:05) by 9 min.',
            'Kept as its own line (vagonweb 2026): the shuttles are seen with 810 units (810 097 on 18 June, 810 220 on 25 September), which also run Kutná Hora město – Kolín, while the Zruč and Zbraslavice trains keep their own units (814 115 and 810 026 on the Zruč trains, 814 087 on the Zbraslavice trains). The 34 min at Kutná Hora hl. n. is the real stay: in at :40, out at :14.',
        ],
    },
    # Posázavský pacifik (8 Oct 2026). 212 Čerčany – Zruč runs 810s (the Sázava trains 814s), and Zruč – Havlíčkův
    # Brod runs 841s, so those stay separate lines.
    # 210: the user did not want the long real stays at Praha hl. n. (51 min for Čerčany, 41 min for the Dobříš branch)
    # and asked to connect the lines, so 210 is two circuits through Praha hl. n.: Čerčany in :04 -> Dobříš branch out
    # :15, Dobříš branch in :34 -> Čerčany out :55. Both branches are planned 847 RegioFox (vagonweb 2026), though the
    # same-day sightings show the real units mostly staying on one branch (847 095: Os 9010 -> 9009, 847 097: Os 19012 ->
    # 19013, both 3 Sep). Every 240: Dobříš takes one hour in four (user: at most one vehicle on the branch), Čisovice
    # the other three through Also at.
    {
        'id': 'l210c', 'name': '210 Čerčany + Čisovice', 'area': 'Posázavský pacifik', 'svc': ['1008', '1088'],
        'every': 240, 'step': 60, 'also': [120, 180],
        'legs': ['19013', '19020', '9017', '9018'],
        'turns': [60, 5, 5, 5],  # Čisovice: the :37 of the arrival hour belongs to the train before (1 h 15 min, as in reality)
        'terminal': ['Praha hl. n.'],
        'extra_real': {'19013': ['19017', '19019'], '19020': ['19014'], '9018': ['9014']},  # start / end at Praha-Vršovice
        'wait_points': {('9017', 'Týnec nad Sázavou'): 'crossing with the train to Praha',
                        ('9018', 'Jílové u Prahy'): 'crossing with the train to Čerčany'},
        'notes': [
            'One circuit for both lines out of Praha hl. n., so the trains do not stand there long. A train comes in from Čerčany at :04 and leaves for Čisovice at :15 (11 min). It comes back from Čisovice at :34 and leaves for Čerčany at :55 (21 min). Before, the stays were 51 and 41 min. Both Praha hl. n. entries are stop type terminal, so nobody rides through from one branch to the other.',
            'Every 240 with Also at: each timed entry has three departures every 4 h (Offset, then Offset + 120 and + 180). The fourth hour belongs to 210 Čerčany + Dobříš, so between them Praha – Čerčany and Praha – Skochovice have a train every hour each way.',
            'Čisovice gets a train every hour except when the Dobříš train runs: from Praha hl. n. 13:15, 15:15, 16:15, 17:15, 19:15, 20:15, and back from Čisovice at :37 except 16:37 and 20:37, when the Dobříš train comes through. The real afternoon is the same except 17:15, which really goes to Dobříš.',
            'At Čisovice each train waits 1 h 15 min (in :22, out at :37 an hour later), as the real trains do. The :37 in the hour it arrives already belongs to the train before it, because the Dobříš train takes one slot in four.',
            'The real 15:30 and 16:30 to Čisovice start at Praha-Vršovice, coming from the depot there. Os 19014 (Čisovice 13:47) and Os 9014 (Čerčany 14:17) end at Vršovice. Also at can only add departures on the same route; it cannot end a train at Vršovice. In the circuit these run as ordinary Praha hl. n. trains with the real 11 min at Vršovice, and no depot runs are needed.',
            'Čerčany branch: single track, and the trains cross every hour. The train to Čerčany waits 38 min at Týnec nad Sázavou (:15 – :53), where the train to Praha passes at :32. The train to Praha waits 12 min at Jílové u Prahy (:51 – :03) for the train to Čerčany (:57). At Čerčany the train turns in 8 min (in :09, out :17). All are real minutes, every hour.',
            'vagonweb (2026): both branches are planned 847 RegioFox, so the circuit keeps one vehicle type. The same-day sightings show the real units mostly staying on one branch (847 095 on two Čerčany trains and 847 097 on two Čisovice trains on 3 September 2026), so sharing the units is a game simplification for the short stays at Praha hl. n.',
        ],
    },
    {
        'id': 'l210d', 'name': '210 Čerčany + Dobříš', 'area': 'Posázavský pacifik', 'svc': ['1008', '1088'],
        'every': 240, 'step': 60,
        'legs': ['19015', '19018', '9019', '9022'],
        'min_turn': 5,
        'terminal': ['Praha hl. n.'],
        'wait_points': {('9019', 'Týnec nad Sázavou'): 'crossing with the train to Praha',
                        ('9022', 'Jílové u Prahy'): 'crossing with the train to Čerčany'},
        'notes': [
            'The fourth hour of the circuit. Every 4 h a train from Čerčany (in at Praha hl. n. 14:04, 18:04) leaves for Dobříš at 14:15 and 18:15. It comes back from Dobříš at 16:06, is in Praha at 17:34 and leaves for Čerčany at 17:55.',
            'Dobříš has one train on the branch at a time, as you asked: Praha hl. n. 14:15 and 18:15, Dobříš 16:06. The 14:15 / 16:06 pair is exact; the real 17:15 runs at 18:15 in the game. The line has 2 vehicles because each also runs a Čerčany round trip in its 8-hour cycle.',
            'At Dobříš it turns in 13 min (in 15:53, out 16:06), like the real 14:15. At Praha hl. n. it stays 11 min (Čerčany → Dobříš) and 21 min (Dobříš → Čerčany); both entries are stop type terminal. Every train waits the real 11 min at Praha-Vršovice (:19 – :30).',
        ],
    },
    {
        'id': 'l212', 'name': '212', 'area': 'Posázavský pacifik', 'svc': '1080', 'every': 120,
        'rep_out': '9223', 'rep_in': '9226',
        'wait_points': {('in', 'Ledečko'): 'crossing with the train to Zruč nad Sázavou',
                        ('in', 'Samechov'): 'crossing with 212 Sázava going out'},
        'notes': [
            'The real Čerčany – Zruč nad Sázavou trains run every 2 h in the odd hours: Čerčany 9:16, 11:16, 13:16, 15:16, 17:16, and Zruč 9:08, 11:08, 13:06, 15:08, 17:08, 19:05. Two trains, as in reality.',
            'vagonweb (2026): planned 810, with a BDtax trailer in the season. On 18 June 2026 unit 810 501 ran Zruč 13:06 → Čerčany 14:59 → 15:16 → Zruč 16:54 → 17:08 → Čerčany 18:59, and 810 545 ran Čerčany 13:16 → Zruč 14:54 → 15:08 → Čerčany 16:59. They turn in 14 min at Zruč and 17 min at Čerčany, as in the game.',
            'The trains cross at Ledečko: the train to Čerčany waits 6 min there (:59 – :05) for the train to Zruč (:02). It then waits 8 min at Sázava (:14 – :22) and 4 min at Samechov (:34 – :38), where it crosses 212 Sázava going out.',
            'Differences from reality: the real Čerčany 17:16 (Os 9227, an 814) waits 7 min at Ledečko and reaches Zruč at 18:59; the game runs it like the other trains. The real Zruč 14:06 (Os 9222) runs once, in an even hour, to bring the 814s to Čerčany for 212 Sázava; it is not in the game.',
        ],
    },
    {
        'id': 'l212s', 'name': '212 Sázava', 'area': 'Posázavský pacifik', 'svc': '1080', 'every': 120,
        'rep_out': '9247', 'rep_in': '9248',
        'wait_points': {('in', 'Samechov'): 'crossing with the 212 train to Zruč nad Sázavou'},
        'notes': [
            'The real afternoon short trains Čerčany – Sázava (Čerčany 16:16 and 18:16, Sázava 17:22) run in the even hours between the Zruč trains, so Čerčany – Sázava has a train every hour, as in reality. One train.',
            'It waits 32 min at Sázava (in S:50, out L:22). On the way back it crosses the 212 train to Zruč at Samechov, where it waits 4 min (:34 – :38). At Čerčany it stays 17 min (in L:59, out S:16), the real minutes.',
            'Kept as its own line: vagonweb plans these trains as 814 RegioNova, while the Zruč trains run 810s.',
            'Only one even-hour train from Čerčany goes to Ledečko on workdays: 14:16 (Os 9245, back to Čerčany coupled to the Zruč train, see Not modelled). The 16:16 and 18:16 end at Sázava in CIS JŘ and on vagonweb. The other Ledečko trains are early or late (Čerčany 5:23, 23:16; Ledečko 4:24, 6:24).',
        ],
    },
    {
        'id': 'l212h', 'name': '212 Havlíčkův Brod', 'area': 'Posázavský pacifik', 'svc': ['1082', None], 'every': 60,
        'rep_out': '24875', 'rep_in': '24876', 'min_turn': 5,
        'wait_points': {('out', 'Ledeč nad Sázavou'): 'crossing with the train to Zruč nad Sázavou'},
        'notes': [
            'The real Zruč nad Sázavou – Ledeč – Světlá nad Sázavou – Havlíčkův Brod trains run every hour in the afternoon: Zruč :56 (12:56 – 16:56, then 19:01), and Havlíčkův Brod 13:37, 14:39, 15:32, 16:37, 18:37. The game runs Zruč :56 and Havlíčkův Brod :37 every hour. After Světlá nad Sázavou the trains run on the Kolín – Havlíčkův Brod line (230) to their real terminus at Havlíčkův Brod.',
            'The trains cross at Ledeč nad Sázavou: the train to Havlíčkův Brod waits 9 min there (:22 – :31) for the train to Zruč (:24).',
            'It turns in 5 min at Zruč (in :51, out :56), as the real trains do. vagonweb shows unit 841 009 on 18 June 2026 running Havlíčkův Brod 13:37 → Zruč 14:51 → 14:56 → Havlíčkův Brod 16:16 → 16:37 → Zruč 17:51. At Havlíčkův Brod it stays 21 min.',
            'Kept as its own line: these are 841 RegioSpider units, while 212 Čerčany – Zruč runs 810s and 814s. Nothing runs through at Zruč.',
            'Differences from reality: there is no real train from Havlíčkův Brod at 17:37 or from Zruč at 17:56. The real 15:32 from Havlíčkův Brod waits 9 min at Světlá nad Sázavou; the game runs it at :37 like the others.',
        ],
    },
]

# stretches decided as not modelled (each also explained in NOT_MODELLED)
LISTED = {('Pečky', 'Plaňany zastávka'), ('Plaňany zastávka', 'Pečky'), ('Pečky', 'Plaňany'), ('Plaňany', 'Pečky'),
          # Posázavský pacifik
          ('Praha hl. n.', 'Praha-Vršovice'), ('Praha-Vršovice', 'Praha hl. n.'),
          ('Čerčany', 'Jílové u Prahy'), ('Jílové u Prahy', 'Čerčany'), ('Týnec nad Sázavou', 'Čerčany'),
          ('Čerčany', 'Týnec nad Sázavou'), ('Vrané nad Vltavou', 'Čerčany'), ('Vrané nad Vltavou', 'Skochovice'),
          ('Praha hl. n.', 'Davle'), ('Davle', 'Praha hl. n.'), ('Praha hl. n.', 'Skochovice'), ('Skochovice', 'Praha hl. n.'),
          ('Čerčany', 'Ledečko'), ('Ledečko', 'Čerčany'), ('Ledečko', 'Sázava'), ('Sázava', 'Ledečko'),
          ('Kácov', 'Zruč nad Sázavou'),
          ('Zruč nad Sázavou', 'Zruč nad Sázavou zastávka'), ('Zruč nad Sázavou zastávka', 'Zruč nad Sázavou'),
          ('Světlá nad Sázavou', 'Havlíčkův Brod'), ('Havlíčkův Brod', 'Světlá nad Sázavou'),
          ('Ledeč nad Sázavou', 'Zruč nad Sázavou'), ('Zruč nad Sázavou', 'Ledeč nad Sázavou'),
          ('Havlíčkův Brod', 'Ledeč nad Sázavou'), ('Ledeč nad Sázavou', 'Havlíčkův Brod'),
          ('Ledeč nad Sázavou', 'Světlá nad Sázavou'), ('Světlá nad Sázavou', 'Ledeč nad Sázavou')}

NOT_MODELLED = [
    '<b>012:</b> the short trains to and from Plaňany and Plaňany zastávka (Pečky 4:30, 6:06, 11:12, 17:12, 23:06; back 5:24, 7:15, 12:24, 18:24) and the early Bošice 4:34; the line slots cover them.',
    '<b>014:</b> the early trains that run through from or to Sázava on line 212 (Os 22200 Kolín 4:01 and 22202 Kolín 6:28 to Sázava; Os 22203 Sázava 6:00 and 22205 Sázava 7:51 to Kolín).',
    '<b>014:</b> the morning Uhlířské Janovice 5:38 – Kolín and the evening Kolín 20:47 – Uhlířské Janovice (the line runs all day anyway).',
    '<b>235 město:</b> the extra shuttles hl. n. 7:17, 7:42, 8:18, 9:35, 11:35, 18:05, 20:01 and město 6:32, 7:29, 8:06, 9:23, 11:23, 19:44, 22:43 (the line runs all day every 2 h); the Kutná Hora město – Kolín through trains (město 9:47, 11:47, 13:47, 17:31, 20:31 to Kolín; Kolín 5:24, 9:41, 11:41, 22:17 to město), which reverse at Kutná Hora hl. n.',
    '<b>235:</b> Os 19215 Kolín 13:41 – Kutná Hora hl. n. – Zbraslavice (one train, svc 1020); the morning short trains Kutná Hora 6:05 – Zbraslavice and Zbraslavice 8:07 – Kutná Hora (the line runs all day anyway); the extension of the 17:05 and 19:05 trains and the Zruč nad Sázavou – Zruč nad Sázavou zastávka shuttles of line 212.',
    '<b>210:</b> the short trains Praha hl. n. 7:15 – Davle and Davle 8:21 – Praha hl. n. (Os 9041, 9040); the early Čerčany 4:09 – Jílové u Prahy, Týnec nad Sázavou 4:23 – Čerčany, Jílové u Prahy 5:27 – Čerčany and the night Vrané nad Vltavou 1:07 – Čerčany; the evening Čerčany 18:17 – Týnec nad Sázavou (Os 9034, the game runs that slot to Praha). The peak trains Os 9011, 9013 and 9015 come out from Praha-Libeň to Praha hl. n. (in at :29 or :35), and Os 9020 goes back there after 19:04: these are depot runs.',
    '<b>210 Dobříš and Čisovice:</b> the real 17:15 Praha hl. n. – Dobříš runs in the game at 18:15 (and 17:15 goes to Čisovice). The trains that really start or end at Praha-Vršovice (15:30 and 16:30 to Čisovice, Os 19014 and Os 9014) run in the game from and to Praha hl. n. The night and early Dobříš trains (Praha 0:30, 5:15; Dobříš 3:36, 4:36, 6:06, 7:06) and the 20-min wait of the Čisovice 13:47 at Měchenice (Os 19014, to Praha-Vršovice) are covered by the line slots.',
    '<b>Praha hl. n. – Praha-Vršovice:</b> all the main-line trains that share only this stretch with 210 (S9 and the Os to Benešov u Prahy and Tábor, the R and Ex trains towards České Budějovice and Brno, the Os to Strančice and Říčany). They are not part of this sheet.',
    '<b>212, the moves of the 814s around 14:00:</b> they get the two 814s of 212 Sázava to Čerčany for the afternoon, and happen once a day, so a game line (which repeats all day) can\'t carry them. One 814 (814 108 on 18 June 2026) comes from Zruč: it runs Zruč → Kácov attached to Os 9218, Kácov 13:34 → Zruč (Os 9271) and Zruč 14:06 → Čerčany (Os 9222). The other runs Čerčany 14:16 → Ledečko (Os 9245) and waits there for the same Os 9222 (Ledečko 15:04 – 15:11, planned "814 Ledečko – Čerčany"), which brings both to Čerčany at 15:59. In the game 212 Sázava simply starts its afternoon at Čerčany.',
    '<b>212, other:</b> the early and late Čerčany – Ledečko trains (Čerčany 5:23, 23:16; Ledečko 4:24, 6:24), the early Sázava trains (Čerčany 6:46, Sázava 8:21) and the Zruč nad Sázavou – Zruč nad Sázavou zastávka shuttles (5:09, 18:23, 20:23).',
    '<b>212 Havlíčkův Brod:</b> the short trains Ledeč nad Sázavou – Zruč (4:37, 13:25), Zruč – Ledeč (21:16), Havlíčkův Brod – Ledeč (6:50, 20:32), Ledeč – Havlíčkův Brod (4:43) and the evening pair Ledeč – Světlá nad Sázavou (22:10, back 22:44).',
    '<b>Světlá nad Sázavou – Havlíčkův Brod:</b> the Os Kolín – Havlíčkův Brod trains of line 230 and the R trains Praha – Havlíčkův Brod – Brno, which share only this stretch with 212 Havlíčkův Brod. They are not part of this sheet.',
    '<b>All lines:</b> the game runs every line all day at its afternoon pattern. Real early-morning and late-evening trains outside that pattern (e.g. 012 Pečky 6:54, 21:08; 235 Kutná Hora 5:13, 23:01; Zruč 3:51, 4:45, 6:43) are covered by the line\'s slots.',
]


def runs(t, day):
    i = (day - dt.date.fromisoformat(t['start'])).days
    return 0 <= i < len(t['bitmap']) and t['bitmap'][i] == '1'


def full(n):
    return FULL.get(n, n)


def hm(m):
    m = int(m)  # Czech timetables print the minute rounded down
    return f'{m // 60 % 24}:{m % 60:02d}'


def dur(m):
    """a round trip as '4 h' or '1 h 30 min'"""
    m = int(m)
    return f'{m // 60} h' + (f' {m % 60} min' if m % 60 else '')


def hmx(m):
    # whole minutes only (user, 5 Oct 2026: the game has no half minutes); rounded down like the printed timetable
    return hm(m)


def mm(m):
    """only the minute, e.g. ':58' (the arrival minute repeats every interval)"""
    return f':{int(m) % 60:02d}'


def ls(m):
    m = int(m) % 1440
    return ('L' if (m // 60) % 2 == 1 else 'S') + f':{m % 60:02d}'


def offset(m, iv):
    return int((int(m) - 60) % iv)


CATS = {'84': 'Os', '122': 'Sp', '157': 'R'}


def cat_of(r, L):
    """the train's own category from the data (a circuit can mix Os and Sp), else the line's"""
    c = next((l.get('ctt') for l in r.get('raw') or [] if l.get('ctt')), None)
    return CATS.get(c, L.get('cat', 'Os'))


def e(s):
    return html.escape(str(s), quote=False)


def load():
    T = json.load(open(TRAINS, encoding='utf-8'))
    by_num, workday = {}, []
    for t in T:
        stops = [l for l in t['locs'] if PA & set(l['act'])]
        if not stops:
            continue
        rec = {'num': stops[0]['num'], 'svc': stops[0]['svc'], 'all5': all(runs(t, d) for d in WEEK), 'raw': t['locs'],
               'stops': [{'name': full(l['name']), 'arr': l.get('arr'), 'dep': l.get('dep'), 'req': '0030' in l['act']} for l in stops]}
        rec['stops'][0]['arr'] = None
        rec['stops'][-1]['dep'] = None
        if rec['all5'] or rec['num'] not in by_num:  # a number can have several date variants; keep the workday one
            by_num[rec['num']] = rec
        if rec['all5']:
            workday.append(rec)
    return by_num, workday


def depot_leg(spec, by_num):
    """An empty run between the passenger terminus and the depot, as a leg with two stops, on the real times of a
    train's non-public locations: {'raw': (train, from, to), 'route': [...], 'name': depot name}, 'DEPOT' in route
    standing for the depot (R18: Praha Jih -> Praha-Vršovice before, Vršovice -> Praha Jih after)."""
    num, a, b = spec['raw']
    locs = by_num[num]['raw']
    la = next(l for l in locs if l['name'] == a)
    lb = next(l for l in locs if l['name'] == b)
    names = [spec['name'] if x == 'DEPOT' else x for x in spec['route']]
    return {'num': f'empty {num} {names[0]} – {names[1]}', 'svc': None, 'all5': True, 'depot': True,
            'stops': [{'name': names[0], 'arr': None, 'dep': la['dep'], 'req': False},
                      {'name': names[1], 'arr': lb['arr'], 'dep': None, 'req': False}]}


def cut_leg(spec, by_num):
    """Part of a real train, from one station to another: {'cut': (train, from, to)}. R49 Olbramovice runs the
    Holešovice – Olbramovice part of Sp 2483 (the same minutes as the real Sp 2481 from Praha hl. n.)."""
    num, a, b = spec['cut']
    t = by_num[num]
    names = [s_['name'] for s_ in t['stops']]
    st = [dict(s_) for s_ in t['stops'][names.index(a):names.index(b) + 1]]
    st[0]['arr'] = None
    st[-1]['dep'] = None
    return dict(t, num=f'{num} {a} – {b}', stops=st)


def build_line(L, by_num, workday):
    legs_n = L.get('legs') or [L['rep_out'], L['rep_in']]
    legs = [by_num[n] if isinstance(n, str) else cut_leg(n, by_num) if 'cut' in n else depot_leg(n, by_num) for n in legs_n]
    legs_n = [t['num'] for t in legs]
    alias = {'out': legs_n[0], 'in': legs_n[1]}
    wp = {(alias.get(k, k), st): v for (k, st), v in L['wait_points'].items()}
    # coupling (fork): {(leg, stop): (primary line, max wait)} on the joining line's entries
    couple = {(alias.get(k, k), st): v for (k, st), v in L.get('couple', {}).items()}
    for k, t in enumerate(legs):
        assert t['all5'] or L.get('season'), (L['id'], t['num'])  # season: a line with no workday trains (build_beroun.py: Rožmitál)
        assert t['stops'][0]['name'] == legs[k - 1]['stops'][-1]['name'], (L['id'], 'legs do not chain', t['num'])
    iv = L['every']
    step = L.get('step', iv)  # an hourly real pattern can be moved by whole hours inside a longer interval
    also = L.get('also', [])  # Also at: extra departures at offset + each value, on every timed entry
    turn = L.get('min_turn', MIN_TURN)  # a real tight turn (Čerčany 8 min, Zruč 5 min) may stay
    turns = L.get('turns', [turn] * len(legs))  # turn before the next leg, per leg
    # every leg leaves at its real minute, in the first slot after the previous arrival + the turn time
    sh0 = L.get('shift', 0)  # move the whole line by whole hours (R49 Olbramovice: Sp 2483's minutes, an hour earlier)
    shifts, t0 = [sh0], legs[0]['stops'][0]['dep'] + sh0
    arr = legs[0]['stops'][-1]['arr'] + sh0
    for k, t in enumerate(legs[1:]):
        d = t['stops'][0]['dep']
        sh = math.ceil((arr + turns[k] - d) / step) * step
        shifts.append(sh)
        arr = t['stops'][-1]['arr'] + sh
    depA = t0 + math.ceil((arr + turns[-1] - t0) / iv) * iv
    cycle = depA - t0
    entries = []
    terminal = set(L.get('terminal', []))

    def add(stop, d, t, stay, hl):
        if also:  # the departures in one 4-hour block of the afternoon, 13:00 – 16:59
            real = ', '.join(hm(m_) for m_ in sorted(780 + (int(t) + a - 780) % iv for a in [0] + also)) + ', then every 4 h'
        else:
            real = (ls(t) if iv == 120 else f'{mm(t)} every hour' if iv == 60
                    else ' and '.join(sorted(mm(int(t) + k * iv) for k in range(60 // iv))) + ' every hour' if iv < 60
                    else ', '.join(hm(int(t) % iv + k * iv) for k in range(1440 // iv)))
        slots = sorted({(offset(t, iv) + a) % iv for a in [0] + also})  # the game: smallest as Offset, the rest as Also at
        entries.append({'stop': stop, 'dir': d, 'off': slots[0], 'also': slots[1:], 'real': real,
                        'stay': stay, 'hl': hl})

    for k, t in enumerate(legs):
        sh = shifts[k]
        j = k
        while t['stops'][-1]['name'] in L.get('mid', {}) and j + 1 < len(legs) and legs[j]['stops'][-1]['name'] in L.get('mid', {}):
            j += 1  # the direction runs on through a mid-route leg boundary
        d = 'towards ' + legs[j]['stops'][-1]['name']
        dep = t['stops'][0]['dep'] + sh
        prev_arr = (legs[k - 1]['stops'][-1]['arr'] + shifts[k - 1]) if k else (arr - cycle)
        o = t['stops'][0]['name']
        tt = ', stop type terminal (everyone gets off)' if o in terminal else ''
        cp = couple.get((t['num'], o))
        cp = f', couple with {cp[0]}, wait up to {cp[1]} min' if cp else ''
        mid = L.get('mid', {})  # a leg boundary that is not a terminus (build_beroun.py: Rokycany on Os Hořovice – Přeštice)
        if k and o in mid:
            add(o, d, dep, f"{mid[o]}, arrives {mm(prev_arr)}, {int(dep) - int(prev_arr)} min" + cp, True)
        elif t.get('depot') and o not in DEPOTS:  # the real arrival minute at the terminus, then to the depot
            add(o, d, dep, f"arrives {mm(prev_arr)}, leaves for {t['stops'][-1]['name']} after {int(dep) - int(prev_arr)} min" + tt + cp, True)
        else:
            add(o, d, dep, 'terminus' + tt + f', {int(dep) - int(prev_arr)} min' + cp, True)
        for s_ in t['stops'][1:-1]:
            stay = int(s_['dep']) - int(s_['arr'])  # whole minutes, as the game shows them
            st = f'{stay} min'
            cp = couple.get((t['num'], s_['name']))
            cp = f', couple with {cp[0]}, wait up to {cp[1]} min' if cp else ''
            if (t['num'], s_['name']) in wp:
                add(s_['name'], d, s_['dep'] + sh, f"{wp[(t['num'], s_['name'])]}, arrives {mm(s_['arr'] + sh)}, {st}" + cp, stay >= LONG_STAY)
            elif stay >= LONG_STAY or cp:
                add(s_['name'], d, s_['dep'] + sh, f"arrives {mm(s_['arr'] + sh)}, {st}" + cp, True)
    timed_names = {x['stop'] for x in entries}
    # real trains of each leg pattern in the data
    ex = {alias.get(k, k): v for k, v in L.get('extra_real', {}).items()}
    real = []
    for k, t in enumerate(legs):
        o, de = t['stops'][0]['name'], t['stops'][-1]['name']
        if t.get('depot') or any(r[0] == o and r[1] == de for r in real):
            continue
        svcs = L['svc'] if isinstance(L['svc'], list) else [L['svc']]
        cut_at = set(L.get('cut_at', []))  # where the game's track ends; real trains may run on past it (build_beroun.py)

        def match(r):
            nm = [s_['name'] for s_ in r['stops']]
            if o not in nm or de not in nm or nm.index(o) > nm.index(de):
                return False
            return (o in cut_at or nm[0] == o) and (de in cut_at or nm[-1] == de)
        rs = [r for r in workday if r['svc'] in svcs and match(r)]
        rs += [by_num[n] for n in ex.get(legs_n[k], [])]
        real.append((o, de, sorted(rs, key=lambda r: r['stops'][0]['dep'])))
    pl = [t for t in legs if not t.get('depot')]  # passenger legs
    A = pl[0]['stops'][0]['name']
    ends = []
    for t in pl:
        n = t['stops'][-1]['name']
        if n != A and n not in ends and n not in L.get('mid', {}):
            ends.append(n)
    return {'L': L, 'A': A, 'B': L.get('B', ' / '.join(ends)), 'legs': legs, 'shifts': shifts, 'entries': entries, 'cycle': cycle,
            'vehicles': int(cycle // iv) * (1 + len(also)), 'depA': depA, 'real': real, 'timed': timed_names, 'wp': wp}


def page(lines, head=None, shared=None, not_modelled=None):
    """head: [<title>, then the paragraphs before the nav] for another sheet (build_benesov.py); default is this sheet's."""
    css = open(os.path.join(ROOT, 'archive', 'Local Trains 010 062 064 260.html'), encoding='utf-8').read()
    css = css[css.index('<style>'):css.index('</style>') + len('</style>')]
    h = ['<title>Local Trains 012 014 210 212 235</title>', css, '<main>',
         '<h1>Local trains 012 · 014 · 235 · Posázavský pacifik 210 · 212</h1>',
         '<p class="muted">Simutrans design for the workday Os trains on 012 Pečky – Kouřim, 014 Kolín – Ledečko, 235 Kutná Hora – Zruč nad Sázavou, '
         'and the Posázavský pacifik: 210 Praha – Čerčany / Dobříš and 212 Čerčany – Zruč nad Sázavou – Havlíčkův Brod. '
         'Times are real JR2026 times from the national CIS JŘ timetable, for trains that run on all five days Mon–Fri 5–9 October 2026. '
         'There are no workday Sp trains on these lines; long-distance trains share only Praha hl. n. – Praha-Vršovice and Světlá nad Sázavou – Havlíčkův Brod.</p>',
         '<p class="small"><b>8 October 2026:</b> added the Posázavský pacifik lines (210, 212). Then, at your request: Dobříš has one train on the branch, Čisovice is filled in with Also at, and 210 runs as two circuits through Praha hl. n. (stays 11 and 21 min). The Kolín and Kutná Hora lines are unchanged.</p>',
         '<p>Notation: <b>L</b> = odd hours, <b>S</b> = even hours. "Offset" in the fork: odd hours come first, so offset 4 means every 2 h at L:04, and even hours add 60 (offset 66 means S:06). '
         'On 212 Havlíčkův Brod (every 60) the offset is simply the minute of every hour. The 210 lines run every 240: offset = (time − 60) mod 240, so 14:15 is offset 75; "Also at" adds more departures in the same 4 hours. (x) = request stop. '
         '<span class="wait">Highlighted</span> rows are timed stops with a longer stay, which the train needs to keep to time. "Leave up to" is 30 min on every entry of the lines every 120 and 240, and automatic on the line every 60.</p>',
         '<nav><a href="#vehicles">Vehicles</a>' + ''.join(f'<a href="#{x["L"]["id"]}">{e(x["L"]["name"])}</a>' for x in lines) + '<a href="#coverage">Every train</a><a href="#notmodelled">Not modelled</a></nav>']
    if head is not None:
        h = [head[0], css, '<main>'] + head[1:] + [h[-1]]
    rows = ''

    def cnt(y):  # a temporary line (build_beroun.py: S6 from Praha-Zlíchov during works) uses another line's vehicles
        return 0 if y['L'].get('temporary') else y['vehicles']
    for k, x in enumerate(lines):
        vc = f'({x["vehicles"]}, {e(x["L"]["temporary"])})' if x['L'].get('temporary') else x['vehicles']
        rows += (f'<tr><td><a href="#{x["L"]["id"]}">{e(x["L"]["name"])}</a></td><td>{e(x["A"])} – {e(x["B"])}</td><td class="n">{x["L"]["every"]}</td>'
                 f'<td class="n">{dur(x["cycle"])}</td><td class="n">{vc}</td></tr>')
        area = x['L']['area']
        if k + 1 == len(lines) or lines[k + 1]['L']['area'] != area:
            n_ = sum(cnt(y) for y in lines if y['L']['area'] == area)
            rows += f'<tr class="total"><td colspan="4">{e(area)}</td><td class="n">{n_}</td></tr>'
    tot = sum(cnt(x) for x in lines)
    h.append('<h2 id="vehicles">Vehicles</h2><div class="scroll"><table><thead><tr><th>Line</th><th>Route</th><th class="n">Every</th><th class="n">Round trip</th><th class="n">Vehicles</th></tr></thead>'
             f'<tbody>{rows}<tr class="total"><td colspan="4">All lines</td><td class="n">{tot}</td></tr></tbody></table></div>')
    h.append('<p class="small muted">Vehicles = round trip ÷ interval. A train waits at the terminus for its line\'s next slot, so the round trip is a whole number of intervals.</p>')
    areas = {}
    for x in lines:
        areas.setdefault(x['L']['area'], []).append(x)
    shared = shared or {
        'Kolín area': ['012 and 014 do not share track. 012 meets the Praha – Kolín line at Pečky, 014 starts at Kolín.',
                       '012 and 012 short share Pečky – Bošice and run in alternate hours: from Pečky S:12 to Kouřim and L:12 to Bošice, so Pečky has a train every hour at :12 as in reality. They cross at Plaňany, where the train to Pečky waits.',
                       '014 is one line for both branches: from Kolín S:47 to Ledečko and L:47 to Uhlířské Janovice, back at Kolín L:16 and S:16. Kolín – Uhlířské Janovice has a train every hour.',
                       'The stays at the main-line stations are kept as short as the real times allow: Kolín 31 min (014), Pečky 26 min (012, every train comes in at :46 and leaves at :12).'],
        'Kutná Hora area': ['From Kutná Hora hl. n. towards Kutná Hora město: L:05 (235 to Zruč), S:05 (235 short to Zbraslavice) and L:14 (235 město shuttle).',
                            '235 and 235 short share Kutná Hora hl. n. – Zbraslavice and run in alternate hours: from Kutná Hora L:05 to Zruč and S:05 to Zbraslavice; from Zbraslavice S:01 (the Zruč train) and L:01 (the short train).',
                            'Going out, both lines meet the other one coming back at Malešov, where the train to Kutná Hora waits 5 min.'],
        'Posázavský pacifik': [
            'Both 210 lines are circuits through Praha hl. n. Every hour a train comes in from Čerčany at :04 and leaves for Čisovice or Dobříš at :15. Another comes in from Čisovice or Dobříš at :34 and leaves for Čerčany at :55. So the trains stay 11 and 21 min at Praha hl. n. instead of the real 51 and 41 min.',
            'The two circuits never use the same minute. 210 Čerčany + Dobříš takes one hour in four (Dobříš 14:15 and 18:15 from Praha; Čerčany 17:55 and 21:55 from Praha), 210 Čerčany + Čisovice the other three.',
            'On Praha hl. n. – Vrané nad Vltavou – Skochovice there is a train from Praha every hour at :55 to Čerčany and at :15 to the Dobříš branch (waiting at Praha-Vršovice until :30). Towards Praha they leave Vrané at :01 (Dobříš branch) and :31 (Čerčany).',
            '212 and 212 Sázava share Čerčany – Sázava and alternate hours: from Čerčany L:16 to Zruč and S:16 to Sázava, and back into Čerčany every hour at :59. Both leave Sázava towards Čerčany at :22 (212 in even hours, 212 Sázava in odd hours), and each crosses the other line going out at Samechov.',
            'At Čerčany the 210 train from Praha comes in at :09 and leaves back at :17. The 212 trains leave at :16, so every hour there is a 7-min change from Praha to the Sázava valley. Čerčany is on the Praha – Benešov main line; the stays there are the real minutes: 8 min for 210, 17 min for 212 and 212 Sázava.',
            'Three lines meet at Zruč nad Sázavou. 212 from Čerčany comes in at L:54 and leaves at L:08. 212 Havlíčkův Brod comes in every hour at :51 and leaves at :56. 235 from Kutná Hora (Kutná Hora area) comes in at S:13 and leaves at L:21. No line runs through, as in reality.',
            '014 from Kolín (Kolín area) meets 212 at Ledečko. Its early through trains to Sázava are listed under Not modelled.',
        ],
    }
    for area, ls_ in areas.items():
        h.append(f'<h2>{e(area)}</h2><ul>' + ''.join(f'<li>{e(s)}</li>' for s in shared[area]) + '</ul>')
        for x in ls_:
            L = x['L']
            iv = L['every']
            h.append(f'<h3 id="{L["id"]}">{e(L["name"])} · {e(x["A"])} – {e(x["B"])} · {x["vehicles"]} vehicle{"s" if x["vehicles"] != 1 else ""}</h3>')
            vlegs = []  # legs joined at a mid-route boundary (build_beroun.py: Hořovice – Rokycany + Rokycany – Přeštice)
            for t in x['legs']:
                if vlegs and t['stops'][0]['name'] in L.get('mid', {}) and vlegs[-1]['stops'][-1]['name'] == t['stops'][0]['name']:
                    vlegs[-1] = dict(vlegs[-1], stops=vlegs[-1]['stops'] + t['stops'][1:])
                else:
                    vlegs.append(t)
            out_legs = [t for t in vlegs if t['stops'][0]['name'] == x['A'] and not t.get('depot')]
            parts = [' – '.join(e(s_['name']) + (' (x)' if s_['req'] else '') for s_ in t['stops']) for t in out_legs]
            back = [t for t in vlegs if not t.get('depot') and t['stops'][-1]['name'] == x['A']]
            same_back = len(back) == 1 and [s_['name'] for s_ in back[0]['stops']][::-1] == [s_['name'] for s_ in out_legs[0]['stops']]
            if L.get('circuit'):  # every leg in order (build_beroun.py: Hořovice – Přeštice with the Sp shuttles)
                cl = [t for t in x['legs'] if not t.get('depot')]
                h.append('<p class="stations"><b>Stations, in order:</b> ' + '; then '.join(
                    ' – '.join(e(s_['name']) + (' (x)' if s_['req'] else '') for s_ in t['stops']) + f' ({cat_of(t, L)})' for t in cl) + '; and again.</p>')
            elif len(out_legs) == 1 and (len(back) != 1 or same_back):
                h.append(f'<p class="stations"><b>Stations:</b> {parts[0]}, then the same back.</p>')
            elif len(out_legs) == 1:  # the way back calls at other stations (R49 to Praha skips hl. n.)
                bk = ' – '.join(e(s_['name']) + (' (x)' if s_['req'] else '') for s_ in back[0]['stops'])
                h.append(f'<p class="stations"><b>Stations:</b> {parts[0]}.<br><b>Back:</b> {bk}.</p>')
            else:
                h.append('<p class="stations"><b>Stations:</b> ' + '; then '.join(p_ + ', and back' for p_ in parts) + '; and so on.</p>')
            has_also = bool(L.get('also'))
            r = ''.join(f'<tr><td>{e(t["stop"])}</td><td>{e(t["dir"])}</td><td class="n">{iv}</td><td class="n">{t["off"]}</td>'
                        + (f'<td class="n">{", ".join(str(a) for a in t["also"])}</td>' if has_also else '')
                        + f'<td class="t">{t["real"]}</td><td>{e(t["stay"])}</td></tr>' for t in x['entries'])
            h.append('<h4>Timetable entries</h4><div class="scroll"><table><thead><tr><th>Stop</th><th>Direction</th><th class="n">Departure every</th><th class="n">Offset</th>'
                     + ('<th class="n">Also at</th>' if has_also else '') + '<th>Real time</th><th>Stay</th></tr></thead>'
                     f'<tbody>{r}</tbody></table></div>')
            # round trip: one vehicle through every leg and back to its first departure
            rt = []
            keep = x['timed'] | {t['stops'][0]['name'] for t in x['legs']} | {t['stops'][-1]['name'] for t in x['legs']}
            nlegs = len(x['legs'])
            for k, t in enumerate(x['legs']):
                sh = x['shifts'][k]
                nxt = (x['legs'][k + 1]['stops'][0]['dep'] + x['shifts'][k + 1]) if k + 1 < nlegs else x['depA']
                for j, s_ in enumerate(t['stops']):
                    if s_['name'] not in keep or (j == 0 and k > 0):
                        continue
                    a_ = '' if s_['arr'] is None else hmx(s_['arr'] + sh)
                    d_ = hm(nxt) if s_['dep'] is None else hmx(s_['dep'] + sh)
                    long = (s_['dep'] is None) or (s_['arr'] is not None and int(s_['dep']) - int(s_['arr']) >= LONG_STAY) or (t['num'], s_['name']) in x['wp']
                    cls = WAIT if long else ''
                    rt.append(f'<tr{cls}><td>{e(s_["name"])}</td><td class="n">{a_}</td><td class="n">{d_}</td></tr>')
            n = x['vehicles']
            per = 1 + len(L.get('also', []))
            how = (f'{per} departures every {iv} min, so {n} vehicles' if per > 1
                   else f'so {n} vehicle{"s" if n != 1 else ""} at every {iv}')
            h.append(f'<h4>Round trip ({dur(x["cycle"])}, {how})</h4><div class="scroll"><table><thead><tr><th>Station</th><th class="n">Arrives</th><th class="n">Departs</th></tr></thead>'
                     f'<tbody>{"".join(rt)}</tbody></table></div>')
            h.append('<ul class="small">' + ''.join(f'<li>{e(s_)}</li>' for s_ in L['notes']) + '</ul>')

            def lab(r, o, de):
                ro_, rd_ = r['stops'][0]['name'], r['stops'][-1]['name']
                extra = '' if (ro_, rd_) == (o, de) else (f', to {rd_}' if ro_ == o else f', from {ro_}')
                at_o = r['stops'][0]['dep']
                if L.get('cut_at'):  # a through train beyond the game's track end: its time at o (build_beroun.py)
                    at_o = next((s_['dep'] for s_ in r['stops'] if s_['name'] == o and s_['dep'] is not None), at_o)
                return f'{hm(at_o)} ({cat_of(r, L)} {r["num"]}{extra})'
            txt = ' '.join(f'From {e(o)} to {e(de)}: ' + ', '.join(lab(r, o, de) for r in rs) + '.' for o, de, rs in x['real'] if rs)
            kind = 'Real trains, weekends and holidays only' if L.get('season') else 'Real workday trains'
            h.append(f'<p class="small muted">{kind}. {txt}</p>')
    # coverage: every workday train pattern on each area's track
    seen, rows = set(), []
    for x in lines:
        for a, b, n, tag, ends in x.get('inv', []):
            if (a, b, tag) in seen:
                continue
            seen.add((a, b, tag))
            rows.append(f'<tr><td>{e(a)} – {e(b)}</td><td class="n">{n}</td><td>{e("; ".join(ends))}</td><td>{e(tag)}</td></tr>')
    h.append('<h2 id="coverage">Every workday train on these lines</h2>'
             '<p class="small muted">Each row is a stretch of these lines that real workday trains run, with how many trains a day and where they really start and end. Every stretch is either modelled or listed under Not modelled.</p>'
             '<div class="scroll"><table><thead><tr><th>Stretch</th><th class="n">Trains</th><th>Real ends</th><th>In the game</th></tr></thead><tbody>'
             + ''.join(rows) + '</tbody></table></div>')
    h.append('<h2 id="notmodelled">Not modelled</h2><ul>' + ''.join(f'<li>{s}</li>' for s in (not_modelled or NOT_MODELLED)) + '</ul>')
    h.append('</main>')
    return '\n'.join(h)


def inventory(lines, workday, listed=None, along=None, svcs=None):
    """Every workday train that serves two or more stations of a line, grouped by the stretch it runs there
    (user, 5 Oct 2026: short workings such as Kolín – Uhlířské Janovice were missed because only trains reaching
    the far terminus were searched). A stretch that is neither a modelled line nor listed as not modelled is
    reported as a gap: decide on it before presenting the design.
    A stretch is a run of consecutive stops on the line, so a train that leaves the line and comes back (S9 Praha
    hl. n. – Benešov stops at Praha hl. n., Praha-Vršovice and Čerčany) is not taken for a Praha – Čerčany train.
    A stretch counts as modelled when it is a modelled leg, or when all its trains are listed as real trains of a
    modelled line (e.g. the Dobříš trains on the Praha – Skochovice part of 210).
    along: stations of the sheet's other lines on the same track; a stop there does not end the run (an Os stopping at
    Mezno, which R49 passes, is still on the R49 route)."""
    covered = {(t['stops'][0]['name'], t['stops'][-1]['name']) for x in lines for t in x['legs']}
    real_nums = {r['num'] for x in lines for _, _, rs in x['real'] for r in rs}
    gaps = {}
    for x in lines:
        idx = {s_['name'] for t in x['legs'] for s_ in t['stops']}
        groups = {}
        lsvcs = x['L'].get('inv_svcs', svcs)  # a line can name its own services (build_beroun.py: R16 and R26)
        for r in workday:
            if lsvcs and r['svc'] not in lsvcs:
                continue
            run = []
            for s in r['stops'] + [None]:
                if s is not None and s['name'] in idx:
                    run.append(s)
                    continue
                if s is not None and along and s['name'] in along:
                    continue
                if len(run) >= 2:
                    groups.setdefault((run[0]['name'], run[-1]['name']), []).append(r)
                run = []
        # on a stretch that is not a modelled leg, the trains of modelled lines and the others get separate rows
        rows = []
        for (a, b), rs in groups.items():
            if (a, b) in covered:
                rows.append((a, b, rs, 'modelled'))
                continue
            mod = [r for r in rs if r['num'] in real_nums]
            rest = [r for r in rs if r['num'] not in real_nums]
            if mod:
                rows.append((a, b, mod, 'modelled'))
            if rest:
                rows.append((a, b, rest, 'not modelled (listed)' if (a, b) in (LISTED if listed is None else listed) else 'GAP'))
        print(f"  stretches on {x['L']['name']} ({x['A']} – {x['B']}):")
        for a, b, rs, tag in sorted(rows, key=lambda r_: -len(r_[2])):
            ends = sorted({f"{r['stops'][0]['name']} – {r['stops'][-1]['name']}" for r in rs})
            print(f"    {len(rs):3} × {a} – {b}  [{tag}]  real ends: {'; '.join(ends)}")
            if tag == 'GAP':
                gaps[(a, b)] = rs
            x.setdefault('inv', []).append((a, b, len(rs), tag, ends))
    return gaps


def main():
    run(LINES, OUT, LISTED)


def run(line_defs, out, listed, along=False, inv_svcs=None, **page_kw):
    """Build, check and write one sheet (also used by build_benesov.py)."""
    by_num, workday = load()
    lines = [build_line(L, by_num, workday) for L in line_defs]
    print('Inventory of every workday train on the lines:')
    stations = {s_['name'] for x in lines for t in x['legs'] for s_ in t['stops']} if along else None
    gaps = inventory(lines, workday, listed, stations, inv_svcs)
    if gaps:
        sys.exit('Undecided stretches (model them or add them to LISTED and NOT_MODELLED): ' + ', '.join(f'{a} – {b}' for a, b in gaps))
    for x in lines:
        print(f"{x['L']['name']}: {x['A']} – {x['B']} every {x['L']['every']}, round trip {x['cycle']:g} min, {x['vehicles']} vehicles")
        for t in x['entries']:
            print(f"   {t['stop']:28} {t['dir']:34} off {t['off']:>4} {t['real']}  ({t['stay']})")
    # same-minute check per stop and direction
    seen = {}
    for x in lines:
        iv = x['L']['every']
        for t in x['entries']:
            for o_ in [t['off']] + t['also']:
                for k in range(240 // iv):  # compare all lines over a 4-hour cycle
                    grp = x['L'].get('couple_with', x['L'].get('same_vehicles_as', x['L']['name']))  # same_vehicles_as: a temporary version of a line
                    seen.setdefault((t['stop'], (o_ + k * iv) % 240), set()).add(grp)
    clash = {k: v for k, v in seen.items() if len(v) > 1}
    print('same stop, same offset:', clash or 'none')
    open(out, 'w', encoding='utf-8').write(page(lines, **page_kw))
    print('wrote', out, 'vehicles', sum(x['vehicles'] for x in lines if not x['L'].get('temporary')))


if __name__ == '__main__':
    main()
