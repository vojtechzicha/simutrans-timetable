---
name: ostrava-bus-vypravenost
description: Ostrava DPO bus sheet (started 2026-09-29) — pipeline/ostrava-bus, bus JDF export, automatic branches, vehicles pending live observation Wed 30 Sep
metadata:
  type: project
---

"Ostrava Bus Vypravenost.html" (project root, artifact https://claude.ai/artifact/6rNwavbbnG4H2aJVZPNx8R), built by `pipeline/ostrava-bus`. The user asked on 2026-09-29 for "a separate file … for all the bus lines" after [[ostrava-trolleybus-vypravenost]].

- **30 Sep 2026: final, observed at the peak** (15:50–16:15, 167 buses, 16 designed, 10 not needed). The poller machine sleeps. Only 16:01–16:15 was covered, so keep the machine awake during peak polls.
- First published 29 Sep in a "vehicles pending" state; the user objected ("you are missing the vehicle assignment to lines") and pointed to the Prague bus session. Now: provisional roster (buses seen live 17:40–17:50 Tue 29 Sep) + designed buses with real car numbers from ODIS history Mar–Jun 2026. Rule: a fleet sheet never ships without vehicles on lines.
- Earlier: published 29 Sep in the **prepared** state: timetable, 56 Simutrans lines on 47 afternoon DPO lines, a need of 169 buses, schedules, fleet, pak, network state. **Vehicles are pending.** The bus live poller runs until Wed 30 Sep 19:45 (it is a background task of the building session). After Wednesday's peak, run `python scripts/run.py` in pipeline/ostrava-bus and republish to the same URL.
- Buses are in the CIS JŘ **bus** export (pub/jdf/JDF.zip, ~107 MB), not the city export. Electric buses sit in the seznam-autobusu register under trakce=elektrobus.
- The branches are found by rule, not by hand. Lines with merged variants are topped up to the chaining count (otherwise Hlučín 56 got 1 bus instead of 5).

**20 Oct 2026:** schedule refit only (roster untouched). 29 rows changed, and 16 approximate rows are listed for the owner to check (e.g. 68, 58 → Plesná run hourly in reality). Network state now includes Klimkovice centrum (59/64/76, modelled, not in the CIS export) and line 45 Most Mládeže (not modelled). Artifact version 5.
**20 Oct (later):** owner asked to model line 41 as at 14:00, half-hourly alternating to Vratimov, náměstí and Kartonážka. It is done via `config.line_overrides` as one circuit with 3 buses, and is the pattern for future hand-set lines. Artifact version 6.
**20 Oct (Hranečník):** the sheet ends with "All lines at Hranečník": 10 DPO lines plus 8 Transdev Slezsko ODIS lines (383, 387, 440–442, 531, 534, 535) as cards, built by 01c_fetch_odis.py and 07_odis.py. Buses are designed from seznam-autobusu records, keyed by plate → register id `vid`, carrier 28. The pak has no Transdev objects (nearest DPO ≈); the tram and trolleybus pak lengths changed on 20 Oct too, and those sheets are not yet updated.
- **E-buses (20 Oct 2026):** DPO 5008–5031 (Urbino 12 IV electric) map to `VZ-DPOstrava-SolarisUrbino12_s4_electric-dpotyrkysova-SolarisUrbino12_s4_electric` (battery, 85 pax, intro 3/2022), exact object, no longer ≈ s4 CNG. Confirmed installed by the pak session (simutrans-custom-czech-pak128-95).
- **ODIS objects (20 Oct 2026):** Hranečník ODIS cards use VZ-ODIS-bus via config.pak.odis_objects. Real paint picks the livery: 3ČSAD → 3csadbilozelena, white → bilazelenykruh.
- **Pak 2cdf3f3 (20 Oct 2026):** Urbino 12 III CNG -> SolarisUrbino12_s3_CNG and Urbino 18 III CNG -> SolarisUrbino18_s3_CNG. Turquoise variants exist for repainted cars (12 III CNG, 18 III). SOR EBN 10,5 object added. The turquoise Urbino 10 was removed.

Owner type choices (20 Oct 2026, v29): config.owner_types puts DPO's five Urbino 10 III on 50 (7521/7523/7524) and 40C Plesná (7518/7519) in place of seen 12 m buses; owner said "do not do 23". Replaced buses listed as not needed.

**21 Oct 2026 (v32):** owner asked that the 59 branches not meet at Polanka. The Svinov branch runs through Klimkovice centrum, so the whole Klimkovice–Polanka–Vítkovice run is shared, and the `passing` rule (≥3 min at the far terminus only) had left them 4 min apart. Fixed via `config.schedule_overrides["59"]`: inbound Klimkovice :00 and Svinov :09, 25/35 like outbound; needs 2+3 unchanged. The override code now takes a `window`, and its dev means real departures vs slot. A shared-trunk scan also flagged 34, 39, 40 (Alšovo row 9 min off the real every 20 at :04) and 56. These were reported to the owner and not changed; the README lists them under "Shared-trunk scan".
**22 Oct 2026 (v33):** the owner's screenshot showed 39/35/39 leaving Dům energetiky within 4 min. Bunching across lines counts too, so run scripts/check_cross_lines.py alongside check_trunks.py and fix only artefacts (real timetable spaced). Changed via schedule_overrides:
- 34: Hlučín AN → :00.
- 39: statek :21/:41, Paskov :50.
- 40A: every 20; 3 buses, +7124.
- 34B: 3 buses; 7771 dropped.

Still open: 56+67/68 (Hlučínská), 26/59, 27/78, 44/46. The owner has these lines in game: always tell them which lines (rows, set minutes, buses) to re-enter after a change.
**22 Oct 2026 (v34):** the owner asked for "the problems that are only in the model, not in reality" to be solved. Done with scripts/space_corridor.py:
- 35 → :13.
- 26 Dubina → :07.
- 44 Svinov, Dubí → :42.
- 46 → :16 / :12.
- 56 Ludgeřovice → :11/:49, Darkovičky → :18.

No needs changed. Open for the owner: Hlučínská 56/67/68 can't be fixed by offsets while 68 is every 80 and the others every 60; offer 68 on a 60-min pattern. 27/41 and 27/78 are left (41 is a hand line at 14:00; 27/78 runs on a dense trunk).
