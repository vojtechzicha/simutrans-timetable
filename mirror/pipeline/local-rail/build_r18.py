"""R18 "Slovácký expres" Praha – Staré Město u Uherského Hradiště – Luhačovice, with coupled trains.

Designed 9 Oct 2026 with the rules in ../rail-design-rules.md and the builder in build_012_014_235.py (real JR2026
times from CIS JŘ, trains that run on all five days Mon–Fri 5–9 Oct 2026; offsets odd hours first).
Writes "R18 Slovácký expres.html" in the project root.
Run: python pipeline/local-rail/build_r18.py

The real train (vagonweb 2026, the same on every workday R18): a RAILL 193 (Vectron) Praha-Vršovice – Staré Město,
a ČD 750.7 Staré Město – Luhačovice; five coaches run through Praha – Luhačovice (Ampz, Bbdgmee, Bmz, Bdpee, Bmz)
and one Bmz only Praha – Staré Město. Simutrans cannot hand coaches from one train to another, so the game uses the
fork's coupling (simutrans-122.0 CLAUDE.md, "Coupling trains", the R12a / R12b example): R18 (the 193 with the
Staré Město coach) is the primary, R18 Luhačovice (the 750.7 with the through coaches) couples behind it from Praha
to Staré Město and back. Under the wire the fork's mixed traction leaves the 750.7 idle.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_012_014_235 as base  # noqa: E402

OUT = os.path.join(base.ROOT, 'archive', 'R18 Slovácký expres.html')  # archived 10 Oct 2026
SM = 'Staré Město u Uherského Hradiště'
DEPOT = 'Praha odstavné nádraží'  # Praha Jih, as for R9 / R19 on the MD-CR sheet
OUT_A = f'891 Praha-Vršovice – {SM}'  # R18's legs: the Praha – Staré Město parts of R 891 and R 884
IN_A = f'884 {SM} – Praha-Vršovice'
DEP_OUT = {'raw': ('891', 'Praha Jih', 'Praha-Vršovice'), 'route': ['DEPOT', 'Praha-Vršovice'], 'name': DEPOT}
DEP_IN = {'raw': ('884', 'Praha-Vršovice', 'Praha Jih'), 'route': ['Praha-Vršovice', 'DEPOT'], 'name': DEPOT}
DEP_OUT_NUM = f'empty 891 {DEPOT} – Praha-Vršovice'


def important(out_leg, in_leg):
    return {(out_leg, 'Pardubice hl. n.'): 'important station', (out_leg, 'Olomouc hl. n.'): 'important station',
            (in_leg, 'Olomouc hl. n.'): 'important station', (in_leg, 'Pardubice hl. n.'): 'important station',
            (in_leg, 'Praha hl. n.'): 'important station'}


LINES = [
    {
        'id': 'r18', 'name': 'R18', 'area': 'R18 Slovácký expres', 'svc': '18', 'every': 120, 'step': 60,
        'cat': 'R', 'min_turn': 5,
        'legs': [DEP_OUT, {'cut': ('891', 'Praha-Vršovice', SM)}, {'cut': ('884', SM, 'Praha-Vršovice')}, DEP_IN],
        'turns': [5, 60, 5, 5],  # Staré Město: the real 1 h 18 min (in S:18, out L:36), where R18 Luhačovice comes back
        'terminal': [SM],
        'extra_real': {OUT_A: ['887', '889', '893', '883'], IN_A: ['888', '886', '884', '882', '890']},
        'wait_points': important(OUT_A, IN_A),
        'notes': [
            'R18 "Slovácký expres", every 2 h as in reality: Praha-Vršovice S:47 (Praha hl. n. :58), Staré Město u Uherského Hradiště S:18; back from Staré Město L:36, Praha hl. n. :11, Praha-Vršovice L:15. Every real workday R18 runs through to Luhačovice; this line is its Praha – Staré Město part.',
            'In the game this line is the RAILL 193 (Vectron) with the Staré Město coach (a Bmz), the front of the real train. It is the primary train: R18 Luhačovice couples behind it.',
            'At Staré Město it ends (stop type terminal): the coupled train parts there, R18 Luhačovice goes on at S:33, and this train waits 1 h 18 min (in S:18, out L:36) for the next R18 Luhačovice coming back. The real 193 and the Staré Město coach do the same (Bmz 366 runs Praha – Staré Město on R 889 and back on R 884).',
            'Praha end, on the real empty runs to and from the depot Praha Jih (Praha odstavné nádraží, as for R9 and R19): depot S:34, Praha-Vršovice in :38, out S:47; back in Praha-Vršovice L:15, out to the depot L:21, at the depot L:25. The train waits 1 h 09 min at the depot, not at a platform. Five vehicles.',
            'Timed: the termini, Praha hl. n. both ways (7 min going out), Pardubice hl. n. and Olomouc hl. n. both ways (important stations), and Přerov towards Praha (5 min).',
        ],
    },
    {
        'id': 'r18l', 'name': 'R18 Luhačovice', 'area': 'R18 Slovácký expres', 'svc': '18', 'every': 120, 'step': 60,
        'cat': 'R', 'min_turn': 5, 'couple_with': 'R18',
        'legs': [DEP_OUT, '891', '884', DEP_IN],
        'turns': [5, 60, 5, 5],  # Luhačovice: the real 1 h 11 min (in L:20, out S:31), so it is back at Staré Město L:36
        'couple': {(DEP_OUT_NUM, DEPOT): ('R18', 10), ('884', SM): ('R18', 10)},
        'extra_real': {'891': ['887', '889', '893', '883'], '884': ['888', '886', '882', '890']},
        'wait_points': important('891', '884'),
        'notes': [
            'The five through coaches (Ampz, Bbdgmee, Bmz, Bdpee, Bmz) with the ČD 750.7 diesel. Between Praha and Staré Město it runs coupled behind R18; from Staré Město to Luhačovice and back it runs alone, as the real 750.7 hauls the coaches.',
            'Coupling (fork, rail): its Praha odstavné nádraží entry and its Staré Město entry towards Praha say "Couple with R18, wait up to 10 min". Only this line carries the setting; R18 is the primary. The pair stays together through the Praha end (both schedules go on to the same stops) and parts at Staré Město going out, where R18 ends. Both lines have the same slots on the coupled part.',
            'Staré Město: in S:18 (coupled), out S:33 to Luhačovice, 15 min as in reality (the real loco change). Coming back: in L:20, coupled with the R18 that waits there, out L:36.',
            'Luhačovice: in L:20, out S:31, 1 h 11 min as in reality. On the way back it waits 8 min at Uherský Brod (:49 – :57), where it crosses the train to Luhačovice. Going out it waits 4 min at Újezdec u Luhačovic (:03 – :07).',
            'Not like reality: the 750.7 runs to Praha and back with the coaches, idle behind the 193 under the wire (the fork\'s mixed traction pulls with the electric engine there and adds no running cost for the idle diesel). In reality it stays on the branch and the coaches change engine at Staré Město; Simutrans cannot move coaches from one train to another. Six vehicles.',
            'The real Thursday, Friday and Sunday extra coaches to Staré Město are not modelled (workday base composition).',
        ],
    },
]

LISTED = {
    # the other R18 trains: Zlínský expres to / from Zlín střed (leaves the line at Otrokovice), Veselí nad Moravou,
    # the early start at Staré Město and at Praha hl. n.
    ('Praha-Vršovice', 'Otrokovice'), ('Otrokovice', 'Praha-Vršovice'),
    (SM, 'Praha-Vršovice'), ('Praha-Vršovice', SM),
    ('Praha hl. n.', 'Luhačovice'), ('Praha hl. n.', SM),
    ('Praha-Vršovice', 'Uherské Hradiště'), ('Uherské Hradiště', 'Praha-Vršovice'),
    # the R18 trains that do not start or end in Praha: Přerovský zubr Přerov – Praha, Olomouc – Luhačovice,
    # Olomouc – Otrokovice, Luhačovice – Staré Město
    ('Přerov', 'Olomouc hl. n.'), ('Olomouc hl. n.', 'Přerov'), ('Česká Třebová', 'Praha hl. n.'),
    ('Praha hl. n.', 'Česká Třebová'), ('Olomouc hl. n.', SM), (SM, 'Olomouc hl. n.'),
    ('Olomouc hl. n.', 'Luhačovice'), ('Luhačovice', 'Olomouc hl. n.'), ('Olomouc hl. n.', 'Otrokovice'),
    ('Luhačovice', SM),
}
NOT_MODELLED = [
    '<b>R18 to and from Zlín:</b> R 894 "Zlínský Expres" Zlín střed 5:28 – Praha-Vršovice and R 897 Praha-Vršovice 18:47 – Zlín střed (they leave the line at Otrokovice). One train each way.',
    '<b>R18 to and from Veselí nad Moravou:</b> R 892 Veselí nad Moravou 7:00 – Praha-Vršovice and R 895 Praha-Vršovice 16:47 – Veselí nad Moravou. One train each way; the game runs that 16:47 slot to Luhačovice.',
    '<b>Early R18:</b> R 896 Staré Město 4:12 – Praha-Vršovice, R 883 Praha-Vršovice 4:47 – Luhačovice and R 885 Praha hl. n. 6:58 – Luhačovice. The line slots cover them.',
    '<b>R18 without Praha:</b> R 898 / 899 "Přerovský zubr" Přerov 4:00 – Praha hl. n. and Praha hl. n. 21:32 – Přerov; R 881 Olomouc 5:57 – Luhačovice and R 880 Luhačovice 18:03 – Olomouc; R 2020 Olomouc 6:31 – Otrokovice; R 858 Luhačovice 19:41 – Staré Město. One train each.',
    '<b>Other trains</b> on Praha – Kolín – Pardubice – Česká Třebová – Olomouc – Přerov – Staré Město and on the Luhačovice branch (Ex, other R, Os, RegioJet, Leo Express): not part of this sheet.',
]
SHARED = {
    'R18 Slovácký expres': [
        'The real R18 is one train Praha – Luhačovice: a RAILL 193 (Vectron) as far as Staré Město u Uherského Hradiště, a ČD 750.7 diesel from there, five coaches through to Luhačovice and one Bmz only to Staré Město (vagonweb 2026, the same on every workday R18).',
        'The game uses the fork\'s coupling, as for R12a / R12b Brno – Zábřeh – Šumperk / Jeseník: R18 (the 193 with the Staré Město coach) and R18 Luhačovice (the 750.7 with the through coaches) keep their own schedules. R18 Luhačovice says "Couple with R18" at Praha odstavné nádraží and at Staré Město towards Praha. Coupled, they run as one train: the 193 in front pulls, the 750.7 is idle under the wire.',
        'Going out the pair leaves the depot at S:34 and Praha-Vršovice at S:47, and parts at Staré Město (in S:18). R18 Luhačovice goes on at S:33 to Luhačovice (L:20). Coming back R18 Luhačovice leaves Luhačovice at S:31, reaches Staré Město at L:20, couples with the R18 that has waited there since S:18, and the pair leaves at L:36 for Praha (Vršovice L:15, depot L:25).',
        'Every real slot is used: the game runs the 2-hourly R18 all day, as the real trains run from 6:58 / 8:47 to 14:47 from Praha and 8:31 to 16:31 from Luhačovice.',
    ],
}
HEAD = [
    '<title>R18 Slovácký expres</title>',
    '<h1>R18 Slovácký expres · Praha – Staré Město – Luhačovice</h1>',
    '<p class="muted">Simutrans design for the workday R18 Praha – Kolín – Pardubice – Olomouc – Přerov – Staré Město u Uherského Hradiště – Luhačovice, as two coupled lines. '
    'Times are real JR2026 times from the national CIS JŘ timetable, for trains that run on all five days Mon–Fri 5–9 October 2026; compositions from vagonweb.cz.</p>',
    '<p>Notation: <b>L</b> = odd hours, <b>S</b> = even hours. Every 120, odd hours come first: offset 47 means every 2 h at L:47, and even hours add 60 (offset 107 means S:47). '
    '<span class="wait">Highlighted</span> rows are timed stops. "Leave up to" is 30 min on every entry. "Couple with" is set on the joining line\'s entry (schedule dialog row "Couple with"; rail only, needs the calendar).</p>',
]

if __name__ == '__main__':
    base.run(LINES, OUT, LISTED, inv_svcs={'18'}, head=HEAD, shared=SHARED, not_modelled=NOT_MODELLED)
