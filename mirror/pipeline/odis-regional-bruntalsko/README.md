# ODIS Bruntálsko, Krnovsko, Rýmařovsko (regional + town buses, vypravenost sheet)

Output: `ODIS Bruntalsko Krnovsko Rymarovsko.html` in the project root, published at the URL in `config.json` → `artifact_url` (republish to the same URL). Built on 21 Oct 2026 after the owner's "Yes, do those next sheets" (the ODIS segments list: Krnovsko, Bruntálsko and Rýmařovsko with the Krnov town lines).

This folder holds the sheet's config, data and authoring scripts. The pipeline scripts are the shared ones in `../odis-regional-hko/scripts/`, run with `--base odis-regional-bruntalsko`. The method is `../bus-schedule-method.md` (v3), as on the HKO and Těšínsko sheets; the two town networks take the same method.

## Scope

| Section | Licences | Operator | Fleet | Town pak |
|---|---|---|---|---|
| Krnovsko | 852xxx | Transdev Morava, pr. Bruntál | 82- | – |
| Bruntálsko | 853xxx | Transdev Morava, pr. Bruntál | 83- | – |
| Rýmařovsko | 854xxx | Transdev Morava, pr. Bruntál | 84- | – |
| MHD Krnov | 856xxx | Transdev Morava | 81- | VZ-MHDKrnov-bus |
| MHD Bruntál | 855xxx | Transdev Morava | (regional buses that day) | – |

- The kraj's contract areas have no prefix in the ministry report; the prefix → area match comes from the fleet numbers on the live map (82- buses run 852, 83- run 853, 84- run 854, 81- are the Krnov town buses) and the line names.
- 47 ODIS numbers. 40 are modelled as 51 Simutrans lines, 63 buses (58 seen on the live map, 5 designed).
- 260 and 920 also hold Opavsko licences (902260, 902920) with most of their trips there, so they are on the Opavsko/Vítkovsko/Hlučínsko sheet (`other_sheets.opavsko`; the parent fills its derived/schedule/url in the ordered roster pass).
- Not modelled (`config.unmodelled`): 803, 876, 914 (no afternoon trips), 815 and 852 (sparse; stops on other lines).
- Lines into the Olomouc region (913, 921 to Olomouc, 922 Uničov, 912 Šternberk) run to their ends: no other line in this data serves those stops.

## Sources

As the HKO and Těšínsko sheets (CIS JŘ JDF and ODIS live map of Tue 20 Oct 2026, stored by the Havířov/Karviná/Orlová pipeline). The fleet is the Transdev Morava register (seznam-autobusu carrier 7546), fetched by `01c_fleet.py` into `data/raw/2026-10-20/fleet/` → `data/derived/fleet.json`. `authoring/brn_config.py` corrects the bus lengths there (01c's `tlen()` reads lengths only from "10,5M"-style names, so SOR "CN 10,5" came out as 12 m); rerunning 01c_fleet.py needs that script rerun too until the shared fix lands.

pak128: the fleet desk confirmed on 21 Oct 2026 that every bus has its object (VZ-ODIS-bus `transdev` livery for Transdev Morava's white with the red Transdev figure and the kraj ring; VZ-MHDKrnov-bus `krnovbila` for the Krnov town buses). `pak_request.md` is empty.

## Decisions (21 Oct 2026)

- **Network state:** diversions to the timetable change or beyond (824, 880, 901, 907, 861) as they run; 876, 912 and 921 ran diversions ending within days, so `regular_not_diversion` keeps their regular timetables. A new 909 version starts 22 Oct; the sheet keeps the vehicle day's.
- **Hand-set after review** (`authoring/brn_spec.py`): real-minute slots where the auto fit or the shortest-round pairing left trips far off (811 Sosnová, 832, 861, 862, 872, 878, 902, 907, 909, 909 Leskovec, 805, 806); shift and school variants every 480 on their real trips (814 Zátor, 818 Neplachovice, 824, 865, 866, 873, 877 KARLA, 806 CLO, 807, 921, 922 Uničov); 801's industrial-zone trips as a Petrův důl – zone shuttle (as 302 Tesco on the Těšínsko sheet); knots where trips start beyond a terminal (910 at Moravský Beroun, náměstí; 922 at Rýmařov bus station; 801 PZ at the zone točna).
- **Dropped variants** (Step 8, no stop of their own): 863 Karlova Studánka, 874 Heřmanice, 921 Ryžoviště.
- **Owner checks** on the page: 877 at :34/:24 with two buses (real :40/:20 needs three); the 801 PZ shuttle; 913 out at 12:07 (one bus) instead of 5:55; 832 on the real minutes with two buses instead of the one-bus shortest round.

## Authoring and review tools (`authoring/`)

- `brn_spec.py` writes `config.lines` (notes from `brn_notes.py`); `brn_config.py` writes everything else. Both are idempotent: rerun them after editing, then the pipeline.
- `trips.py L,...` (whole-day trip list), `stops.py L 'stop'` (stop sequences of trips through a stop), `dump.py [L,...]` and `review.py L,...` (slots, joint moves, fit, real departures) for the hand review.

## How to update

1. A new poll day: the Havířov/Karviná/Orlová poller must run 13:00–19:30 (whole region). Point `snapshot`, `vehicle_day`, labels, `jdf.zip`, `live.dir` at it.
2. From `../odis-regional-hko/scripts`: `python -X utf8 01c_fleet.py --base odis-regional-bruntalsko` (register, kept on disk), then `python -X utf8 ../../odis-regional-bruntalsko/authoring/brn_config.py`, then `python -X utf8 run.py --base odis-regional-bruntalsko`.
3. Re-check diversions (`data/derived/versions.json`) and the network state; review the To check list and each changed line with `authoring/dump.py`; adjust `brn_spec.py`, rerun it and the pipeline. Coverage must stay at 0 uncovered.
4. Sheets build in order (Ostrava → HKO town → HKO regional → Těšínsko → Opavsko → Novojičínsko → this one) so a bus stays on one sheet.
5. Republish to `artifact_url`.
