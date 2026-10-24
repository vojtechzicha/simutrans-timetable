"""R49 Praha – Benešov – Tábor and the local trains around Benešov: 223 Sedlčany, 222 Vlašim and the Os on 220
between Olbramovice and Tábor.

Designed 9 Oct 2026 with the rules in ../rail-design-rules.md and the builder in build_012_014_235.py (same data:
real JR2026 times from CIS JŘ, trains that run on all five days Mon–Fri 5–9 Oct 2026; offsets odd hours first).
Writes "archive/Local Trains R49 Benešov.html" (archived 9 Oct 2026).
Run: python pipeline/local-rail/build_benesov.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_012_014_235 as base  # noqa: E402

OUT = os.path.join(base.ROOT, 'archive', 'Local Trains R49 Benešov.html')  # archived 9 Oct 2026

# vagonweb (2026): R49 (Sp "Sázava", relace CZ-220, needs the train name) is a 362 locomotive with five coaches
# (4 × Bdmtee, AB). The local trains are all planned 841.3 RegioSpider; R49 and the locals are separate pools.
LINES = [
    # R49 (user, 9 Oct 2026): hourly between Praha and Benešov in the afternoon peak (hl. n. 14:15 – 18:15), every
    # 2 h on to Tábor, "far from the local train" (220 Os: Tábor S:39 -> Olbramovice L:15, Olbramovice S:42 -> Tábor
    # L:19). Tábor in the even hours keeps R49 31 – 39 min from the Os both ways (odd hours: only 21 – 26 min).
    # The other hours turn at Olbramovice, the real afternoon short terminus (Sp 2481 / 2480).
    # Praha end (user, 9 Oct 2026: the Malešice bypass is fine if it is in the data). Every afternoon R49 that ends at
    # Holešovice runs Hostivař -> Malešice -> Libeň (7 min, no passengers) -> Holešovice (Sp 2478 from Tábor, Sp 2480
    # from Olbramovice). R49 Tábor does so too, on the minutes of Sp 2478; R49 Olbramovice keeps the route via hl. n.
    # (minutes of Sp 2474), so hl. n. still has an R49 towards Praha every 2 h. Out of Praha all run via hl. n. (Sp 2483).
    {
        'id': 'r49', 'name': 'R49 Tábor', 'area': 'R49 Praha – Tábor', 'svc': '1149', 'every': 120, 'step': 60,
        'cat': 'Sp',
        'rep_out': '2483', 'rep_in': '2478',
        'extra_real': {'out': ['2475'], 'in': ['2470', '2472']},  # from / to Praha hl. n.
        'wait_points': {('out', 'Praha hl. n.'): 'important station',
                        ('out', 'Benešov u Prahy'): 'important station',
                        ('in', 'Benešov u Prahy'): 'important station'},
        'notes': [
            'PID R49, Sp "Sázava", a peak line. In the afternoon it leaves Praha hl. n. every hour at :15 (14:15, 15:15, then 16:15, 17:15 and 18:15 coming from Holešovice at :05). The first goes to Benešov, the second to Olbramovice, the last three to Tábor.',
            'The game has two R49 lines every 2 h that alternate. Together they leave Praha-Holešovice every hour at :05 (Praha hl. n. :15, Benešov :07). R49 Tábor takes the even hours to Tábor: Holešovice S:05 (16:05 = Sp 2483, 18:05 = Sp 2487), Tábor L:50, back from Tábor S:05. R49 Olbramovice takes the odd hours and turns at Olbramovice.',
            'Far from the local train: the 220 Os leaves Olbramovice for Tábor at S:42; R49 follows 37 min later (L:19) and reaches Tábor 31 min after it. Towards Praha R49 leaves Tábor at S:05, 34 min before the Os (S:39), and is 39 min ahead of it at Olbramovice. R49 in the odd hours would run only 21 – 26 min from the Os.',
            'Two vehicles. It turns in 15 min at Tábor (in L:50, out S:05) and 20 min at Holešovice (in L:45, out S:05), as the real set does (Sp 2478 in 16:45, Sp 2485 out 17:05).',
            'Real Tábor departures to Praha are at :05 too, but in odd hours (7:05, 15:05, 19:05; Sp 2474, 2478): the game runs them an hour earlier or later, to keep the even-hour pattern.',
            'Towards Praha it runs via the Malešice bypass, as every real afternoon R49 to Holešovice does (Sp 2478 Tábor 15:05, Sp 2480 Olbramovice 16:36): Říčany L:16 → Praha-Hostivař → Praha-Malešice → Praha-Libeň (a 7-min stop without passengers, :32 – :39) → Praha-Holešovice L:45. It does not call at Praha hl. n. Out of Praha it runs via hl. n. (Holešovice S:05, hl. n. S:13 – :15), as the real trains do.',
            'In the game the Libeň stop has no timetable entry (no passengers), and the line is timed at Holešovice. If the train takes the route via hl. n. instead, put a waypoint at Praha-Malešice in its schedule.',
            'Timed: Praha-Holešovice and Tábor (termini), Praha hl. n. going out, Benešov u Prahy both ways (important stations), and the real 5 min at Říčany going out.',
            'vagonweb (2026): a 362 locomotive with four Bdmtee coaches and an AB, on every R49 train except Praha hl. n. 14:15 – Benešov (Sp 2479, a 471 CityElefant).',
        ],
    },
    {
        'id': 'r49o', 'name': 'R49 Olbramovice', 'area': 'R49 Praha – Tábor', 'svc': '1149', 'every': 120, 'step': 60,
        'cat': 'Sp',
        'legs': [{'cut': ('2483', 'Praha-Holešovice', 'Olbramovice')}, {'cut': ('2474', 'Olbramovice', 'Praha-Holešovice')}],
        'shift': -60,  # Holešovice L:05 (15:05 = the real 2481 at hl. n. 15:15); R49 Tábor has S:05
        'turns': [60, 10],  # Olbramovice: S:36 belongs to R49 Tábor coming through, so L:36 (see notes)
        'extra_real': {'out': ['2481', '2479'], 'in': ['2480']},
        'wait_points': {('out', 'Praha hl. n.'): 'important station',
                        ('out', 'Benešov u Prahy'): 'important station',
                        ('in', 'Benešov u Prahy'): 'important station',
                        ('in', 'Praha hl. n.'): 'important station'},
        'notes': [
            'The odd hours: Praha-Holešovice L:05 (Praha hl. n. L:15, Benešov S:07) to Olbramovice, back from Olbramovice L:36. Two vehicles.',
            'Real trains it stands for: Praha hl. n. 15:15 → Olbramovice 16:18 (Sp 2481) and back 16:36 → Holešovice (Sp 2480), Praha hl. n. 14:15 → Benešov (Sp 2479), and Holešovice 17:05 → Tábor (Sp 2485), which in the game turns at Olbramovice.',
            'Olbramovice is the turning point because the real afternoon short train turns there, 11 min beyond Benešov. It has room: no train starts there, while S9 turns at Benešov every 30 min. Benešov keeps an hourly R49 both ways.',
            'Each train waits 1 h 18 min at Olbramovice (in S:18, out L:36). The real 2481 / 2480 turn in 18 min, but S:36 is R49 Tábor coming through towards Praha. One R49 set stands there at a time, next to the 220 Os (27 min) and the Sedlčany trains reversing.',
            'Both directions via Praha hl. n. to Holešovice: out on the minutes of Sp 2483 (Holešovice :05, hl. n. :13 – :15), back on the minutes of Sp 2474, the real train that runs on through hl. n. (hl. n. :39 – :41, Holešovice :53). It turns at Holešovice in 12 min. The real 2480 takes the Malešice bypass; this line keeps hl. n. so that Praha hl. n. has an R49 towards Praha every 2 h (R49 Tábor bypasses it).',
            'vagonweb (2026): the same 362 locomotive with five coaches as R49 Tábor. The real 14:15 to Benešov is a 471 CityElefant; in the game it runs as an R49 set.',
        ],
    },
    {
        'id': 's223', 'name': '223 Sedlčany', 'area': 'Local trains around Benešov', 'svc': '1098', 'every': 60,
        'rep_out': '26124', 'rep_in': '26123',
        'wait_points': {('out', 'Olbramovice'): 'reverses here',
                        ('in', 'Olbramovice'): 'reverses here',
                        ('in', 'Štětkovice'): 'crossing with the train to Sedlčany'},
        'notes': [
            'A train every hour all afternoon, as in reality: from Benešov at :33, from Sedlčany at :53. Three trains.',
            'It runs on the main line from Benešov to Olbramovice and reverses there onto the Sedlčany branch (1 min). Olbramovice is timed in both directions because the train reverses.',
            'The trains cross at Štětkovice every hour: the train to Benešov waits there (:05 – :07) for the train to Sedlčany.',
            'At Sedlčany it turns in 33 min (in :20, out :53). At Benešov it stays 52 min (in :41, out :33), the real minutes.',
            'vagonweb (2026): planned 841.3 RegioSpider. Sightings show 841 3xx units and sometimes an 810 (810 007 on 14 May, 810 545 on 20 April 2026).',
        ],
    },
    {
        'id': 's222', 'name': '222 Vlašim', 'area': 'Local trains around Benešov', 'svc': '1099', 'every': 60,
        'rep_out': '19143', 'rep_in': '19142',
        'wait_points': {('in', 'Postupice'): 'crossing with the train to Vlašim'},
        'notes': [
            'A train every hour all afternoon, as in reality: from Benešov at :32, from Vlašim at :26. Two trains. JR2026 has no passenger trains beyond Vlašim (to Trhový Štěpánov).',
            'The trains cross at Postupice every hour (:47 – :48), so Postupice is timed towards Benešov.',
            'At Vlašim it turns in 17 min (in :09, out :26). At Benešov it stays 29 min (in :03, out :32), the real minutes.',
            'vagonweb (2026): planned 841.3 RegioSpider (841 303 seen on 8 July, 810 289 on 6 August 2026).',
        ],
    },
    {
        'id': 's220', 'name': '220 Os', 'area': 'Local trains around Benešov', 'svc': '1090', 'every': 120,
        'legs': ['8268', '8273', '8270', '8275'],
        'terminal': ['Olbramovice', 'Votice'],
        'wait_points': {},
        'notes': [
            'The Os on the main line between Tábor and Olbramovice, every 2 h as in reality: Tábor S:39 → Olbramovice L:15, back Olbramovice S:42 → Tábor L:19. They call at the small stations R49 passes (Mezno, Červený Újezd u Votic zastávka, Ješetice and the other request stops).',
            'Between the two runs the train goes Olbramovice L:42 → Votice L:46 and back Votice S:11 → Olbramovice S:15, as in reality (Os 8273 and 8270 in the afternoon). Nothing else could run these trips (the Sedlčany trains are on the move then), so it is one circuit line. The Olbramovice and Votice entries are stop type terminal.',
            'At Tábor it waits 1 h 20 min (in L:19, out S:39). Two trains.',
            'vagonweb (2026): planned 841.3 RegioSpider.',
        ],
    },
]

LISTED = {
    # other sheets: Praha trains, S9, R17 and the long-distance trains
    ('Praha hl. n.', 'Praha-Vršovice'), ('Praha-Vršovice', 'Praha hl. n.'),
    ('Praha hl. n.', 'Praha-Holešovice'), ('Praha-Holešovice', 'Praha hl. n.'),
    ('Praha hl. n.', 'Praha-Zahradní Město'), ('Praha-Zahradní Město', 'Praha hl. n.'),
    ('Praha hl. n.', 'Tábor'), ('Tábor', 'Praha hl. n.'),
    ('Benešov u Prahy', 'Olbramovice'), ('Olbramovice', 'Benešov u Prahy'),
    ('Olbramovice', 'Praha hl. n.'), ('Benešov u Prahy', 'Praha hl. n.'),  # R17 and Ex on R49 Olbramovice
    # the Os from the south that turn at Chotoviny
    ('Tábor', 'Chotoviny'), ('Chotoviny', 'Tábor'),
    # R49 short trains and the early / late Os
    ('Benešov u Prahy', 'Tábor'), ('Tábor', 'Benešov u Prahy'), ('Votice', 'Benešov u Prahy'),
    ('Praha hl. n.', 'Votice'), ('Votice', 'Praha hl. n.'), ('Praha hl. n.', 'Benešov u Prahy'),
    ('Olbramovice', 'Praha-Holešovice'), ('Praha hl. n.', 'Olbramovice'),
}
NOT_MODELLED = [
    '<b>Other sheets:</b> R17 Praha – Benešov – Tábor – České Budějovice and the other long-distance trains (R 324 and 326 from Gmünd, Ex 544), S9 Praha – Benešov u Prahy, and the other Praha trains that share only Praha hl. n. – Praha-Vršovice, Praha-Zahradní Město or Praha-Holešovice with R49.',
    '<b>South of Tábor:</b> the Os from České Budějovice, Veselí nad Lužnicí and Jindřichův Hradec that run through Tábor and turn at Chotoviny, one stop north (6 trains each way). They belong to the lines south of Tábor.',
    '<b>R49:</b> the morning trains outside the game pattern (Tábor 5:05 and 6:03 to Praha hl. n., Benešov 5:40 – Tábor, Praha hl. n. 6:45 – Votice and Votice 8:32 – Praha hl. n., Praha hl. n. 8:15 – Tábor), and the afternoon Tábor 19:05 – Benešov (Sp 2484); the hourly lines cover those hours. The real Tábor departures to Praha are in odd hours (7:05, 15:05, 19:05); the game has them in even hours. Sp 2480 Olbramovice 16:36 – Holešovice takes the Malešice bypass; the game runs the Olbramovice trains via hl. n. The early Sp 2473 Praha hl. n. 6:45 – Votice also runs via Libeň and Malešice.',
    '<b>220 Os:</b> the early and late trains Benešov 4:04 and 6:23 – Tábor (Os 8251, 8253), Tábor 4:39 – Benešov (8250), Votice 23:21 – Benešov (8286) and Olbramovice 23:12 – Votice (8287). The line slots cover the others (e.g. Tábor 21:05).',
    '<b>223:</b> Čerčany 4:43 – Benešov – Sedlčany (Os 26100), which starts on line 221.',
    '<b>All lines:</b> the game runs every line all day at its afternoon pattern. Real early-morning and late-evening trains outside that pattern are covered by the line slots.',
]
SHARED = {
    'R49 Praha – Tábor': [
        'R49 leaves Praha-Holešovice every hour at :05 (Praha hl. n. :15, Benešov :07) and runs at least to Olbramovice; every other train goes on to Tábor (Holešovice S:05: 16:05, 18:05, …). Back it leaves Olbramovice every hour at :36 and Benešov at :49. The trains from Tábor (Tábor S:05) take the Malešice bypass to Holešovice (L:45) without calling at hl. n.; the trains from Olbramovice run via Praha hl. n. (S:41) to Holešovice (S:53). Two lines every 2 h, 2 vehicles each: R49 Tábor and R49 Olbramovice.',
        'Why this split: the real afternoon R49 leaves Praha hl. n. every hour (14:15, 15:15, 16:15, 17:15, 18:15). Between Benešov and Tábor the game runs R49 every 2 h, in the even hours, so it keeps 31 – 39 min away from the 220 Os every 2 h; R17 runs every hour there too. The other R49 turn at Olbramovice, the real afternoon short terminus (Sp 2481 / 2480), which has room, unlike Benešov, where S9 turns every 30 min.',
        'R49 shares Praha – Benešov with S9 (every 30 min) and R17 (every hour), and Benešov – Tábor with R17 and the 220 Os (every 2 h). Of these, the 220 Os is on this sheet too.',
        'At Tábor R49 leaves at S:05 and comes in at L:50; the 220 Os leaves at S:39 and comes in at L:19. Between Olbramovice and Tábor they run in the same hours, about half an hour apart.',
    ],
    'Local trains around Benešov': [
        'At Benešov u Prahy, Vlašim leaves at :32 (east, line 222) and Sedlčany at :33 (south, on the main line). They come in from Vlašim at :03 and from Sedlčany at :41. R49 calls every hour, at :07 going out and :49 going to Praha.',
        'The two Benešov lines stay separate. Both are planned 841.3, but one circuit would not shorten the stays at Benešov: Vlašim in :03 → Sedlčany out :33 is 30 min, and Sedlčany in :41 → Vlašim out :32 is 51 min, the same 81 min as now (29 + 52).',
        'At Olbramovice the Sedlčany trains reverse (:49 – :50 going out, :24 – :25 coming back). 220 Os comes in from Tábor at L:15, goes to Votice at L:42 and leaves for Tábor at S:42. R49 calls every hour: towards Tábor L:19 (R49 Tábor), towards Praha :36 (R49 Tábor S:36; R49 Olbramovice, which waits there from S:18, at L:36).',
    ],
}
HEAD = [
    '<title>Local Trains R49 Benešov</title>',
    '<h1>R49 · local trains around Benešov</h1>',
    '<p class="muted">Simutrans design for R49 Praha – Benešov u Prahy – Tábor and the workday Os trains around Benešov: 223 Benešov – Olbramovice – Sedlčany, 222 Benešov – Vlašim, and the Os on 220 between Olbramovice and Tábor. '
    'Times are real JR2026 times from the national CIS JŘ timetable, for trains that run on all five days Mon–Fri 5–9 October 2026.</p>',
    '<p>Notation: <b>L</b> = odd hours, <b>S</b> = even hours. On the lines every 60 the offset is the minute of every hour. On the lines every 120 odd hours come first: offset 39 means every 2 h at L:39, and even hours add 60 (offset 99 means S:39). The R49 lines run every 120 too. (x) = request stop. '
    '<span class="wait">Highlighted</span> rows are timed stops with a longer stay. "Leave up to" is 30 min on every entry of the lines every 120, and automatic on the lines every 60.</p>',
]

if __name__ == '__main__':
    base.run(LINES, OUT, LISTED, along=True, head=HEAD, shared=SHARED, not_modelled=NOT_MODELLED)
