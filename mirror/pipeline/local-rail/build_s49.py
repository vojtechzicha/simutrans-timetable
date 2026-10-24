"""S49 Praha-Hostivař – Praha-Libeň – Praha-Holešovice – Roztoky u Prahy (PID).

Designed 9 Oct 2026 with the rules in ../rail-design-rules.md and the builder in build_012_014_235.py (real JR2026
times from CIS JŘ, trains that run on all five days Mon–Fri 5–9 Oct 2026). Service number 1049 in CIS JŘ.
Writes "S49 Hostivař Roztoky.html" in the project root.
Run: python pipeline/local-rail/build_s49.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_012_014_235 as base  # noqa: E402

OUT = os.path.join(base.ROOT, 'archive', 'S49 Hostivař Roztoky.html')  # archived 10 Oct 2026

LINES = [
    {
        'id': 's49', 'name': 'S49', 'area': 'S49 Praha-Hostivař – Roztoky u Prahy', 'svc': '1049', 'every': 30,
        'rep_out': '28144', 'rep_in': '28145',
        'wait_points': {},
        'notes': [
            'PID S49. In the afternoon (from Praha-Hostivař 13:33 to 18:33, from Roztoky 13:45 to 18:15) a train runs every 30 min the whole way: Praha-Hostivař :03 and :33, Roztoky u Prahy :15 and :45. The morning peak is the same (Praha-Hostivař 5:33 to 8:33). The game runs that pattern all day.',
            'Three vehicles. It turns in 12 min at Roztoky u Prahy (in :33 / :00, out :45 / :15) and 20 min at Praha-Hostivař (in :13 / :43, out :33 / :03), the real minutes.',
            'Route: from Praha-Hostivař via Praha-Malešice (no stop) to Praha-Libeň, then Praha-Holešovice, Praha-Podbaba, Praha-Sedlec and Roztoky u Prahy. 30 min end to end. It does not call at Praha hl. n.',
            'Interval 30: the offset is the minute of the first departure in each half hour (3 means :03 and :33), and "Leave up to" stays automatic. Only the two termini are timed; no stop has a stay of 5 min or more.',
            'Vehicles: vagonweb.cz has no composition for the S49 train numbers (it lists only named and long-distance trains on these lines), so the unit type is open.',
        ],
    },
]

LISTED = {('Praha-Libeň', 'Roztoky u Prahy'), ('Roztoky u Prahy', 'Praha-Libeň')}
NOT_MODELLED = [
    '<b>Off-peak and evening:</b> outside the afternoon S49 runs every 30 min only between Praha-Libeň and Roztoky. Every other train turns at Libeň (Libeň :17 → Roztoky :33, Roztoky :45 → Libeň :01), and only the hourly :33 / :15 trains run to and from Praha-Hostivař. The game runs the afternoon pattern all day, so these short trains are not a line of their own. Also the first train, Praha-Libeň 5:17 – Roztoky.',
    '<b>Other trains</b> on Praha-Libeň – Praha-Holešovice – Roztoky u Prahy (S4, S41, R and Ex towards Kralupy and Děčín) and through Praha-Malešice (R49 afternoon trains to Holešovice): not part of this sheet.',
]
SHARED = {
    'S49 Praha-Hostivař – Roztoky u Prahy': [
        'S49 crosses Praha without Praha hl. n.: Praha-Hostivař – Praha-Malešice – Praha-Libeň on the freight line, then the main line to Holešovice and up the Vltava to Roztoky u Prahy.',
        'The real R49 afternoon trains to Praha-Holešovice (archived R49 sheet) use the same Hostivař – Malešice – Libeň link.',
    ],
}
HEAD = [
    '<title>S49 Hostivař Roztoky</title>',
    '<h1>S49 · Praha-Hostivař – Praha-Libeň – Roztoky u Prahy</h1>',
    '<p class="muted">Simutrans design for the workday S49 (PID). Times are real JR2026 times from the national CIS JŘ timetable, for trains that run on all five days Mon–Fri 5–9 October 2026.</p>',
    '<p>Notation: every 30, the offset is the minute of the first departure in each half hour. (x) = request stop. "Leave up to" is automatic.</p>',
]

if __name__ == '__main__':
    base.run(LINES, OUT, LISTED, inv_svcs={'1049'}, head=HEAD, shared=SHARED, not_modelled=NOT_MODELLED)
