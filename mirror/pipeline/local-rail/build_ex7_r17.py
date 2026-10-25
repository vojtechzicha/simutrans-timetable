"""Ex7 "Jižní expres" and R17 "Vltava" / "Lužnice": Praha hl. n. – Benešov – Tábor – Veselí nad Lužnicí, cut at
Veselí nad Lužnicí, where the game's track ends (user, 14 Oct 2026: "for both the track ends in Veselí nad Lužnicí;
neither has access to depot unless you have concrete evidence of one in Prague").

Depot check: CIS JŘ has no empty runs for these trains (every Ex7 and R17 starts and ends at Praha hl. n. among its
own locations, unlike R26 to Praha-Malešice or R9/R19 to Praha Jih), so there are no depot runs.
Ex7 passes Veselí nad Lužnicí without stopping. In the game it has to end there, so the script adds Veselí as a stop
at the train's real passing minute (from the CIS location list); everything else is the real timetable.

Designed 14 Oct 2026 with the rules in ../rail-design-rules.md and the builder in build_012_014_235.py (real JR2026
times from CIS JŘ, trains that run on all five days Mon–Fri 5–9 Oct 2026). Ex7 = CIS line 7, R17 = CIS line 17.
Writes "Ex7 R17 Praha Veselí.html" in the project root.
Run: python pipeline/local-rail/build_ex7_r17.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_012_014_235 as base  # noqa: E402

OUT = os.path.join(base.ROOT, 'Ex7 R17 Praha Veselí.html')
VE = 'Veselí nad Lužnicí'
IMP = 'important station'
AREA = 'Praha – Tábor – Veselí nad Lužnicí'
_load = base.load


def load():
    """the real data, plus Veselí nad Lužnicí as a stop on Ex7 at its passing minute (the game's end of track)"""
    by_num, wd = _load()
    for r in list(by_num.values()) + wd:
        if r['svc'] != '7' or any(s_['name'] == VE for s_ in r['stops']):
            continue
        p = next((l for l in r['raw'] if l['name'] == VE and l.get('arr') is not None), None)
        if p is None:
            continue
        k = next(i for i, s_ in enumerate(r['stops']) if (s_['dep'] if s_['dep'] is not None else s_['arr']) > p['arr'])
        r['stops'].insert(k, {'name': VE, 'arr': p['arr'], 'dep': p['arr'], 'req': False})
    return by_num, wd


base.load = load

LINES = [
    {
        'id': 'r17', 'name': 'R17', 'area': AREA, 'svc': '17', 'every': 60, 'cat': 'R', 'inv_svcs': {'17'},
        'legs': [{'cut': ('721', 'Praha hl. n.', VE)}, {'cut': ('712', VE, 'Praha hl. n.')}],
        'cut_at': [VE],
        # R 326 and R 324 Gmünd - Praha run the line's minutes from Veselí; CIS JŘ gives them no line number at their
        # first (Austrian) stop, so the svc-17 inventory does not see them (method check, 25 Oct 2026)
        'extra_real': {'in': ['326', '324']},
        'wait_points': {('out', 'Benešov u Prahy'): IMP, ('in', 'Benešov u Prahy'): IMP,
                        ('out', 'Tábor'): IMP, ('in', 'Tábor'): IMP},
        'notes': [
            'R17 Praha hl. n. – Benešov u Prahy – Tábor – Veselí nad Lužnicí, cut at Veselí, where the game\'s track ends. In reality most trains run on to České Budějovice ("Vltava"); the "Lužnice" trains (11:46, 15:46, and 7:46 / 17:46 to Gmünd) run on to České Velenice. Every hour from Praha hl. n. at :46 (Benešov :27 – :29, Tábor :58 – :00, Veselí :19) and from Veselí nad Lužnicí at :38 (Tábor :58 – :00, Benešov :29 – :31, Praha hl. n. :10).',
            'Four vehicles. 19 min at Veselí nad Lužnicí (in :19, out :38) and 36 min at Praha hl. n. (in :10, out :46): the real minutes fix both stays. No depot: the trains really start and end at Praha hl. n., and CIS JŘ has no empty runs for them.',
            'The two "Lužnice" trains from Gmünd, R 326 (Veselí 12:38) and R 324 (Veselí 18:38), run the line\'s minutes towards Praha (Tábor :58 – :00, Benešov :29 – :31, Praha hl. n. :10). CIS JŘ gives them no line number at their first stop in Austria, so they were missing from the real-train list until 25 October; they are listed below now.',
            'At Veselí the stay joins two real trains: the one that runs on to České Budějovice, and the one coming back from there. On the České Velenice trains it is close to reality: the locomotive and coaches from Praha stand at Veselí 12 – 23 min while a 754 takes the train on (vagonweb, R 723).',
            'Benešov u Prahy and Tábor are timed both ways as the important stations (2 min each). Praha-Vršovice, Praha-Zahradní Město and Olbramovice are 1-min stops in both directions.',
            'Vehicles: a locomotive with six or seven coaches (Bdpee, Bmz, Bbdgmee, Aee): on workdays a 193 Vectron (RAILL) since 14 June 2026, before that a ČD 380 (vagonweb 2026, R 721, R 712, R 725, R 708).',
        ],
    },
    {
        'id': 'ex7', 'name': 'Ex7', 'area': AREA, 'svc': '7', 'every': 60, 'cat': 'Ex', 'inv_svcs': {'7'},
        'legs': [{'cut': ('537', 'Praha hl. n.', VE)}, {'cut': ('530', VE, 'Praha hl. n.')}],
        'cut_at': [VE],
        'wait_points': {('out', 'Tábor'): IMP, ('in', 'Tábor'): IMP},
        'notes': [
            'Ex7 "Jižní expres" Praha hl. n. – Tábor – České Budějovice (some on to Linz or Český Krumlov), cut at Veselí nad Lužnicí, where the game\'s track ends. In the afternoon from Praha hl. n. at :21 (14:21 – 18:21; Tábor :21 – :23) and from České Budějovice at :58 (Tábor :35 – :37, Praha hl. n. :39).',
            'Ex7 does not stop at Veselí nad Lužnicí in reality: it passes at :34 towards České Budějovice and at :23 towards Praha. In the game it ends there, at those real passing minutes. Its only stop on the way is Tábor, timed both ways as the important station (2 min).',
            'Four vehicles. 49 min at Veselí (in :34, out :23 the next hour) and 42 min at Praha hl. n. (in :39, out :21): the real minutes. No depot: the trains start and end at Praha hl. n., with no empty runs in CIS JŘ.',
            'The real afternoon has gaps that the game fills: no Ex7 from Praha at 13:21 or after 18:21, and none from České Budějovice at 16:58 or between 17:58 and 21:52. The game runs every hour all day.',
            'Vehicles: a locomotive with seven or eight coaches (Bmz, Bbdgmee, ARmpee dining car): a 193 Vectron (RAILL) since 14 June 2026, before that a ČD 380; the Linz trains run with a ČD 380 (vagonweb 2026, IC 537, IC 530, EC 335, EC 332).',
        ],
    },
]

LISTED = {('Praha hl. n.', 'Tábor'), ('Tábor', 'Praha hl. n.'), ('Tábor', VE)}
NOT_MODELLED = [
    '<b>Engineering works (checked 14 October 2026):</b> none long-term on this line. Until 3 November, on workdays, R17 trains may run up to 10 min late between Praha-Uhříněves and Říčany, and the morning R 728, 730 and 732 also stop at Říčany (PID). It ends in early November, so it is not modelled (your call). Re-checked on pid.cz on 25 October: still in force and still the only works on this line, apart from a night closure Strančice – Praha-Uhříněves on 6 – 9 November (R17, S9; nights only, not modelled). The S9 · S2 sheet has the works versions of S9 and R49.',
    '<b>R17 short trains:</b> R 731 Praha 19:46 → Tábor 20:59 and R 737 23:46 → Tábor, R 734 Tábor 5:00 → Praha, and R 703 Tábor 7:00 → České Budějovice (Veselí 7:19). The evening R 735 at 22:16 is a different minute.',
    '<b>R17 Veselí departures in the morning:</b> the České Velenice trains R 730 and R 726 leave Veselí at 6:38 and 8:38, the same :38 as the line.',
    '<b>Ex7 outside the afternoon:</b> Ex 544 České Budějovice 4:56 → Praha (stops at Veselí, Benešov and Praha-Vršovice), Ex 501 5:58 and the other morning and evening trains, all at the same :21 / :58 minutes or close to them. Also SC 500, the evening Pendolino Ostrava hl. n. – Praha hl. n. (20:26 – 20:31) – České Budějovice, which stops at Tábor (21:25 – 21:27) and Veselí nad Lužnicí (21:38); one train, at other minutes, with no line number in CIS JŘ.',
    '<b>Everything beyond Veselí nad Lužnicí:</b> Veselí – České Budějovice, Veselí – Třeboň – České Velenice (– Gmünd), and the line to Jindřichův Hradec are outside the game\'s track.',
    '<b>Not part of this sheet:</b> the Os and Sp on Praha – Benešov – Tábor (S9 and the local trains, the archived R49 / Benešov sheet), the trains that share only Praha hl. n. – Praha-Vršovice – Praha-Zahradní Město (S8 / S88 to Čerčany and Dobříš, R9, R18, R19, Ex3 and the other long-distance trains towards Brno and Ostrava), and the branches at Benešov (Vlašim, Trhový Štěpánov), Olbramovice (Sedlčany), Tábor (Bechyně, Písek, Pelhřimov – Horní Cerekev) and Veselí (Jindřichův Hradec).',
]
SHARED = {
    AREA: [
        'R17 and Ex7 share the whole route, and neither overtakes the other. Towards Veselí: from Praha hl. n. Ex7 :21, R17 :46; from Tábor R17 :00, Ex7 :23; at Veselí R17 arrives :19, Ex7 :34.',
        'Towards Praha: from Veselí Ex7 :23, R17 :38; from Tábor Ex7 :37, R17 :00; at Praha hl. n. Ex7 arrives :39, R17 :10.',
    ],
}
HEAD = [
    '<title>Ex7 R17 Praha Veselí</title>',
    '<h1>Ex7 · R17 · Praha – Tábor – Veselí nad Lužnicí</h1>',
    '<p class="muted">Simutrans design for the workday Ex7 "Jižní expres" and R17 "Vltava" / "Lužnice", cut at Veselí nad Lužnicí, where the game\'s track ends. '
    'Times are real JR2026 times from the national CIS JŘ timetable, for trains that run on all five days Mon–Fri 5–9 October 2026. Unit types are from vagonweb.cz. '
    'Neither line has a depot run: CIS JŘ shows no empty runs to or from a Praha depot for these trains, so both turn at Praha hl. n.</p>',
    '<p>Notation: every 60, the offset is the minute of every hour. <span class="wait">Highlighted</span> rows are timed stops with a longer stay. "Leave up to" is automatic.</p>',
]

if __name__ == '__main__':
    base.run(LINES, OUT, LISTED, along=True, inv_svcs={'7', '17'}, head=HEAD, shared=SHARED, not_modelled=NOT_MODELLED)
