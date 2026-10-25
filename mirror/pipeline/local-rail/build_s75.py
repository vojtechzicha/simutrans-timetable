"""S75 Beroun – Nižbor – Křivoklát – Rakovník (PID, KJŘ 174): the trains north of Beroun, up to S5 (not included).

Designed 13 Oct 2026 with the rules in ../rail-design-rules.md and the builder in build_012_014_235.py (real JR2026
times from CIS JŘ, trains that run on all five days Mon–Fri 5–9 Oct 2026). Service number 1075 in CIS JŘ.
Scope (user, 13 Oct 2026): only S75. Kladno – Rakovník (S50, R24) counts as the S5 family; all track is built in the game.
Writes "S75 Beroun Rakovník.html" in the project root.
Run: python pipeline/local-rail/build_s75.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_012_014_235 as base  # noqa: E402

OUT = os.path.join(base.ROOT, 'S75 Beroun Rakovník.html')
AREA = 'S75 Beroun – Křivoklát – Rakovník'

LINES = [
    {
        'id': 's75', 'name': 'S75', 'area': AREA, 'svc': '1075', 'every': 60,
        # out: Os 7745 (Beroun 14:59, Rakovník 15:55), not Os 7717 (15:59, Rakovník 16:57): with 7717's minutes the
        # train reaches Rakovník a minute after the :56 back has left, so the two would meet on the single track
        # Chlum u Rakovníka - Rakovník (check_meetings.py 7717 7718 Beroun Rakovník 60: CONFLICT). 25 Oct 2026.
        'rep_out': '7745', 'rep_in': '7718',
        'extra_real': {'out': ['7703', '7713', '7725']},
        'wait_points': {('out', 'Zbečno'): 'crossing with the train to Beroun'},
        'notes': [
            'PID S75 (KJŘ 174), along the Berounka through Nižbor, Zbečno and Křivoklát. In the afternoon peak a train leaves Beroun every hour at :59 (14:59, 15:59, 16:59; Rakovník 15:55, 16:57, 17:53) and Rakovník at :56 (14:57, 15:56; Beroun :49). The game runs that pattern every hour all day.',
            'The line is single track. The two directions cross at Zbečno: the train to Rakovník waits there 3 min (:23 – :26, Os 7745; Os 7717 waits :22 – :26) for the train to Beroun (:25 – :26), so Zbečno is timed towards Rakovník. The other direction waits only 1 min there and is not timed.',
            'Three vehicles. It turns in 10 min at Beroun (in :49, out :59) and 61 min at Rakovník (in :55, out :56 an hour later): the real minutes. The train arriving at :55 does not take the :56 a minute later (that is the train that came in an hour before); in reality Os 7745 arrives 15:55 and Os 7718 leaves 15:56.',
            'Why the :56 return and not the :12 (17:12, 19:12): the :12 trains cross the :59 at Roztoky u Křivoklátu instead (the 16:59 waits there 17:31 – 17:33). That pattern also needs 3 vehicles, but it puts the long wait at Beroun (54 min) instead of Rakovník. Beroun is the main-line station, so its stay stays short.',
            '<b>Corrected 25 October 2026 (method check):</b> the out trip is now Os 7745 (Beroun 14:59, Rakovník 15:55), not Os 7717 (Beroun 15:59, Rakovník 16:57). With the minutes of Os 7717 the train reached Rakovník at :57, a minute after the :56 back had left, so every hour the two would have met on the single track between Chlum u Rakovníka and Rakovník (check_meetings.py: conflict there). With 7745 they meet only at Zbečno, as the real trains do (Os 7745 and Os 7716 at Zbečno 15:25 – 15:26; Os 7717 and Os 7718 at 16:25 – 16:26). Nothing changes in the game: Beroun :59, Zbečno :26 and Rakovník :56 stay the same. Only the round trip below and the Zbečno and Rakovník stays (3 and 61 min) are different.',
            'Vehicles: ČD 847 RegioFox (vagonweb 2026, planned on Os 7717, 7718, 7745, 7716 and 7720; 847 019 seen on Os 7718).',
        ],
    },
]

LISTED = set()
NOT_MODELLED = [
    '<b>S75 outside the hourly pattern:</b> the real S75 is hourly only in the afternoon peak, and the game runs :59 / :56 all day. Real afternoon trains at other minutes: from Beroun 14:17 (Os 7715, an extra train that crosses Rakovník 14:11 at Zbečno and stops 2 min at Lašovice), 18:12, 19:14, 20:15, 21:55 and 23:12; from Rakovník 14:11, 17:12, 18:05, 19:12, 20:30 and 22:35. Morning and midday: from Beroun 4:11, 6:19, 7:52, 9:01, 10:56 and 12:15; from Rakovník 4:03, 5:09, 5:52, 6:34, 8:03, 10:01, 11:48 and 13:13.',
    '<b>Rakovník západ:</b> Os 7713 (Beroun 12:15) and Os 7725 (Beroun 20:15) run one stop further, to Rakovník západ. In the game every S75 ends at Rakovník.',
    '<b>Os 7703 Zdice 4:36 → Beroun → Rakovník:</b> the early S60 train that runs on to Rakovník (it waits at Beroun 4:47 – 5:14).',
    '<b>Engineering works (checked on pid.cz on 25 October 2026):</b> Rakovník – Roztoky u Křivoklátu is replaced by buses from 29 September to 8 November 2026 (track repair; minibuses serve Chlum u Rakovníka, Lašovice and Pustověty; ČD works timetable cz-k174-2026vyluka02). It ends in early November, so the regular timetable is modelled (your rule of 14 October: works that end in early November are not modelled; it is also listed on the S5 sheet). Rakovník – Rakovník západ – Blatno u Jesenice is replaced by buses by day (19 – 31 October, about 8:00 – 18:30); on this line it touches only the trains that run on to Rakovník západ, in practice Os 7713 (Beroun 12:15, not modelled); Os 7725 runs after the daily window.',
    '<b>Not part of this sheet (your choice, 13 October: only S75):</b> in JR2026, S5 is Praha Masarykovo nádraží – Kladno – Kralupy nad Vltavou (CIS 1005, with 1045 and R45 = 1145 on the same track). Kladno – Rakovník is S50 (1050) together with R24 Praha – Kladno – Rakovník; they count as the S5 family. Also out: S54 Hostivice – Středokluky – Noutonice, and every line beyond Rakovník (Jesenice – Žlutice / Bečov nad Teplou, Louny – Most, Lužná u Rakovníka – Žatec – Chomutov). Rakovník – Kralovice u Rakovníka (S58, CIS 1058) has no workday trains (weekends and holidays only), so it is not modelled either.',
]
SHARED = {
    AREA: [
        'S75 meets the Praha – Plzeň line at Beroun. It turns there in 10 min: in at :49, out at :59. Beyond Beroun-Závodí it has the track to itself, all the way up the Berounka to Rakovník.',
        'At Rakovník it meets the lines to Kladno and Praha (S50, R24), to Jesenice and Žlutice, to Louny and to Žatec. None of them are on this sheet.',
    ],
}
HEAD = [
    '<title>S75 Beroun Rakovník</title>',
    '<h1>S75 · Beroun – Nižbor – Křivoklát – Rakovník</h1>',
    '<p class="muted">Simutrans design for the workday S75 (PID, KJŘ 174), the trains north of Beroun up to S5 (S5 not included). '
    'Times are real JR2026 times from the national CIS JŘ timetable, for trains that run on all five days Mon–Fri 5–9 October 2026. Unit types are from vagonweb.cz. '
    'All the track is built in the game, so the line runs to its real termini.</p>',
    '<p class="fix"><b>25 October 2026 (method check):</b> no change in the game (Beroun :59, Zbečno :26, Rakovník :56, 3 vehicles). The out trip shown is now Os 7745 (14:59), which reaches Rakovník at :55, before the :56 back leaves; the Os 7717 minutes shown before (Rakovník :57) would have met the :56 between Chlum u Rakovníka and Rakovník. The engineering works on the line are now listed under Not modelled.</p>',
    '<p>Notation: every 60, the offset is the minute of every hour. (x) = request stop. <span class="wait">Highlighted</span> rows are timed stops with a longer stay. "Leave up to" is automatic.</p>',
]

if __name__ == '__main__':
    base.run(LINES, OUT, LISTED, along=True, inv_svcs={'1075', '1060'}, head=HEAD, shared=SHARED, not_modelled=NOT_MODELLED)
