# Havířov, Karviná, Orlová buses (Transdev Slezsko MHD): peak vypravenost sheet

Output: `Havirov-Karvina-Orlova Bus Vypravenost.html` in the project root, published at the URL in `config.json` → `artifact_url` (republish to the same URL). Built by session simutrans-timetable-a4 on 20 Oct 2026, at the owner's request: "Similar to Ostrava and in coordination". Shared rules for all cities are in `../README.md`.

## Coordination with the Ostrava bus sheet

- **Rules are imported, not copied.** `scripts/lib.py` loads `../ostrava/scripts/lib.py` (JDF reader, runfit, plans, loop_shift, pattern_need, make_nm) and `../ostrava-bus/scripts/lib.py` (branch_pairs, line_anchor, interleave, path_variants, circuitize). When the Ostrava bus session (simutrans-timetable-0b) changes a rule there, this sheet follows on the next run. The Ostrava bus lib loads its own config at import. Only its pure functions are used here, never its `save()`/`load()`.
- **Agreed 20 Oct 2026 with 0b:** 0b messages before any signature change. Owner rules for Ostrava buses are forwarded and applied here too. Rules received so far: anchor per line, both ends at the same rate, interleaving at shared termini and at junctions, sizing from the suggested pattern, circuits only where they save a bus, path variants, `anchor_overrides` (supported in `05_schedule.py`).
- **Vehicles on both sheets:** 0b's Hranečník ODIS cards (Transdev regional lines 383, 387, 440–442, 531, 534, 535) also use Tue 20 Oct. If a plate turns up on both, the bus stays with the line it ran at that line's peak anchor. 0b sends its plate list before publishing.
- **The live poll is shared.** It is the whole ODIS region, unfiltered, every carrier (owner's request via 0b). 0b reads `data/raw/2026-10-20/live/` for its cards.

## State on 20 Oct 2026, 20:05: observed at the afternoon peak and the evening runs (version 11)

- 60 buses observed on their lines at each line's own peak, plus the evening lines' own runs (409, 411B, 417B, 501B). 11 are designed, each with its reason, and 3 more seen are "not needed". The poll ran 05:01–19:50 with no gap: 436 snapshots of the whole ODIS region, one a minute 13:05–19:30. Need 68, coverage complete, every bus on an exact pak object.
- **One bus, one Simutrans line, by matching** (`04_roster.py` step 4). The buses swap lines all afternoon: in Havířov the 401/406 ring buses also run 413, 403, 417 and 402, and Karviná's circulars swap constantly. So each bus may fill any Simutrans line it was seen on, and an augmenting-path assignment fills as many line needs as possible, trying each bus's closest candidates first. The earlier "nearest line per bus" left 406 with no seen bus while 401 had 2 spare.
- Still designed: 419/420 share one real bus; 421's trips were run by ring buses; 434 never appeared under its own number; 403, 405, 412, 415 and 512 are one short; 501B's 17:06 bus is the one that ran 501 at 16:18. After 20:00: 409, 411B, 417B (17:03) and 501B got their real buses. 417B's second bus (18:03) is designed because it is a 417 bus. 501 is designed because its 16:18 bus went on to 501B.
- The 442 plate chains for the Ostrava session are in its inbox: 442's :05 buses go on as 441 from Podlesí.

## Sources## Sources

| What | Where | Notes |
|---|---|---|
| Timetable | https://portal.cisjr.cz/pub/jdf/JDF.zip (bus export of 20 Oct 2026) | Licences 876401–876421 + 876434 (Havířov), 877511–877520 (Karviná), 878501–878505 (Orlová); IČO 45192081. ODIS number = last 3 digits. Karviná and Orlová JDFs write their own town's stops without the town ("Fryštát,aut.nádr."); Havířov's carry "Havířov,". |
| Live vehicles | POST https://mpvnet.cz/Odis/map/mapData (the map behind mapa.kodis.cz) | Body `{"w":16.7,"s":49.4,"e":18.84,"n":50.45,"zoom":13,"showStops":false,"mapFilterId":null}`. Send the headers Content-Type JSON, Origin https://mpvnet.cz and Referer https://mpvnet.cz/odis/map, or it returns 400. Decode as utf-8-sig. Transmitter `cn` = `licence\|line\|course\|last stop\|…\|start\|final\|1\|PLATE\|…`, `cr` = carrier and branch ("Transdev Slezsko pr. Havířov"). **No history.** |
| Fleet register | seznam-autobusu.cz `seznam?prov=1&trakce=autobus&iddopravce=28` (5 pages) + `trakce=elektrobus` | Plates are parsed from `td.plates` (lib `parse_fleet_list`) and are the live-feed join key. Buses missing from the list (e.g. Orlová Dekstra 448, ran 501/503 on 20 Oct) are looked up by `01d_plates.py` (plate search → vehicle page). |
| Line records | seznam-autobusu ODIS vypravenost `?linka=NNN` (all pages; they are not in date order) | Weekday records since `records.since` (2025-01-01) pick designed buses. 2026 records are sparse (401 has none). |
| Disruptions | JDF diversion versions (Linky field 6 = 1); kodis.cz/changes is a JS app and showed nothing for these lines | 420 diverted from 14 Oct (Horní Bludovice, Záguří not served), modelled. |
| pak128 | local repo `C:\Users\vojte\Developer\simutrans-custom-czech-pak128` (main 966cb16, 20 Oct 2026): `dist/text/en.VZ-MHD<Town>-bus.tab` and `build/VZ-MHD<Town>-bus/*.dat` | Pak session f3: town lines use only VZ-MHDHavirov/-Karvina/-Orlova objects, never CZ-ODIS / CZR-ODIS. `06_render.py` reads the installed objects, so new objects clear the "≈" marks by themselves. |

## Steps (`scripts/`, stdlib-only Python; run with `-X utf8`)

1. `01_fetch.py [--jdf] [--fleet] [--records]`: raw inputs.
2. `01b_live_poll.py <until>`: the live poller. On the vehicle day, start it **detached** so it survives the session and the machine stays awake (it calls SetThreadExecutionState):
   `Start-Process python -ArgumentList '-I','01b_live_poll.py','2026-10-20T20:00' -WorkingDirectory <scripts> -WindowStyle Hidden -RedirectStandardOutput ..\data\raw\poll_<date>.log`
3. `02_timetable.py`: versions and classes (peak / morning / night / none). Calendar rows without a date range (transfer notes) are skipped.
4. `03_fleet.py`: fleet.json (register + plate lookups), live.json (every Transdev bus by fleet number), history.json.
5. `01d_plates.py`: looks up plates seen on the sheet's lines that the register list lacks; then `03_fleet.py` again.
6. `05_schedule.py`: anchors, branches, schedule rows (shared rules). Circular lines get one row on their start stop.
7. `04_roster.py`: needs (pattern_need on the suggested rows), observed buses, surplus, designed buses.
8. `06_render.py`: the sheet and `pak_request.md`.

`python scripts/run.py` runs 2–8.

## Decisions

- **Vehicle day Tue 20 Oct 2026, observed live.** Each line is counted in its own window, `live.half_window` (20) min either side of its anchor. A bus seen on several lines counts on the line whose anchor its sighting is nearest. Before the afternoon is observed, the morning peak (`live.provisional`, 6:30–8:00) stands in, marked "seen this morning".
- **Lines:** 37 licences. 407 and 408 are night lines. 414 has one afternoon trip over 410's stops ("occasional", fewer than `min_afternoon_trips` = 3) and is not modelled. 503 runs as a leg of 504 (its 14:00 trip is the trunk's even-hour departure by the Důl Lazy path), and 520 as the return leg of 514. 32 lines have cards.
- **Circular lines** (Karviná 511, 512, 516, 518, 519, all from Fryštát, autobusové nádraží): `branch_pairs` needs two termini, so `05_schedule.py` adds one branch with a = b and one row. Its need is `pattern_need` with one entry and the loop running time.
- **Stop names:** each line drops its own town's prefix, and every abbreviation is expanded (`stop_name_expansions`). "J.Kotase" is Josefa Kotase (street in Dolní Datyně). "čist.st." is written "čisticí stanice". "EDĚ aut.st." is Elektrárna Dětmarovice, autobusová stanice.
- **Depots** are the Transdev branches (provozovna Havířov / Karviná / Orlová). For a seen bus it is the live feed's `cr`, for a designed bus its town.
- **Designed buses:** real buses with weekday records on the line, free (not on any line 14:30–17:30 in the live feed), covering the line's types first. Town-fleet buses come first. Regional buses (kraj or ODIS paint, `regional_paints`) that stood in on a line design only when no town bus is left.
- **Pak:** a bus gets its type's object in its own paint from any of the three town packages, preferring its line's town. A regional bus (kraj or ODIS paint) working a town line takes its exact object from VZ-ODIS-bus (pak main 6f7b639; `odis_types`, `odis_paint_rules`, white kraj ring green in Havířovsko, red in Hlučínsko), as pak session f3 announced on 20 Oct 2026. Otherwise it shows "≈": the same family in another paint, or the Urbanway 12M CNG for regional types. Each "≈" is listed in `pak_request.md`.

## Coverage rule and hand-set lines (owner, 20 Oct 2026)

- **Rule:** "501 is the only line running to Dětmarovice, how can we not model that?" Every stop the sheet's lines serve in 13:00–19:00 must be on a modelled Simutrans line, or be listed with the reason. `04_roster.py` step 7 checks this on every run: `roster.json` → `uncovered` must be empty. The page has a Coverage section, and each card lists its afternoon trips that are not on one of its Simutrans lines.
- **Why the branch rule wasn't enough:** in Orlová and Karviná the buses rotate between branches and lines. One bus runs 505 to Věřňovice, then Rychvald, then Věřňovice. The Dětmarovice trips are split at Lutyně and shared by 501 and 504. 401 and 406 are two halves of one ring (406 Podlesí → Pašůvka goes on as 401 → Šumbark → Prostřední Suchá, then as 406 back to Podlesí). 514 returns from Staré Město as 520. A per-pair rule drops all of these.
- **`config.line_overrides`** (as Ostrava 41): `mode` is `replace` (the line's automatic branches are dropped), `add` (one more Simutrans line beside them) or `carried` (the line runs on another line's circuit: 520 on 514). Each Simutrans line is a cycle of legs. A leg's real departures are given (`deps`, with `src` naming the real trips, which may be another line's) or found from `lines` between its termini in `window`. `at` fixes uneven slot minutes. `every` 1440 is a daily timetable (Pardubice precedent). `untimed` legs (Departure every 0) are where the real bus goes on as another line. `lib.build_overrides` builds them and `lib.override_need` sizes them. The wait before a leg is the usual 3 min, or less where the slots chain closer, as the real turnarounds do.
- **On 20 Oct (final):** 401 (ring half, :14/:59 from Šumbark) + 401B (hourly shuttle to Prostřední Suchá); 406 (other ring half); 402B (Stonava, every 480); 405 (whole day :22/:44); 409 (hourly evening line); 411 (hourly) + 411B (Šenov, Lapačka, every 480); 417 (hourly) + 417B (Hradiště, from 17:00) + 417C (Podlesí shuttle); 418 (circuit every 240); 420 (every 160); 513 carried by 514; 501 + 501B and 504 (the Orlová trunk by core points, see below; 503 a leg of 504); 502 (daytime Lutyně – Město); 505 (Věřňovice / Rychvald circuit every 120); 514 (Fryštát → Ráj → Staré Město → back as 520, whole day :27/:48/:25, 2 buses); 515 + 515B (mine shift, every 480); 516 (whole day :50); 517 (whole day :15/:36); 520 carried by 514; 503 carried by 504.
- **Bus totals:** per-line Simutrans lines need more buses than the operator runs, because real buses swap lines at the termini. Each town header gives the timetable's own chaining at 16:00 (Havířov about 33 against 51 as separate lines, including the hand-set lines that don't run at 16:00). Pooling lines (401 + 406 as one ring, Karviná's Fryštát loops) is the owner's choice and is not done.
- **Ostrava rules adopted the same day (via 0b):** evenly spaced slots at the plain interval and drifting 1–2 min slots merged (`simplify_rows`); rows with more slots than real departures thinned to one approximate slot (`thin_rows`); fits on aliased termini with the real names restored. Later the same day: `path_variants(..., keep_stops=)` gets the stops only one line serves in 13:00–19:00, and "not via X" path labels are rendered. No line of this sheet has path variants, so the page didn't change. The Ostrava alias Havířov, Město, nemocnice → železniční stanice (ODIS 441) isn't needed: 410's nemocnice trips are morning-only.

## Hand review of every schedule (owner, 20 Oct 2026)

The owner asked: "Is the lines the best schedule that fits my intent (not necessarily the scripts)? Or can you do a version that fits better". I checked every line against its real departures at its peak and against how its buses chain their trips.
- **Already right (exact patterns, no change):** 402, 403, 404, 412, 413, 415, 416, 421, 434 (Havířov); 511, 512, 518, 519 (Karviná); the coverage hand-sets 401, 406, 502, 505, 515. 405 and 419 are approximate within 1–5 min, which is the real irregularity.
- **Changed by hand:**
  - 417: exactly hourly (Šumbark :01, Těrlicko :37). The automatic fit had folded the shuttle and evening trips into it. 417C is the real Podlesí :50 / Těrlicko :00 shuttle.
  - 409: exactly hourly evening line, Podlesí :46 / Šumbark :52, 2 buses. Was every 120, 30 min off.
  - 411: hourly, Podlesí :05 / Adámek :33, 1 bus. Was every 120, 28 min off.
  - 418: one daily circuit at the bus's real afternoon minutes. Was every 90, 14 min off, plus a separate Podlesí line.
  - 420 and 513: daily timetables at the exact minutes of their few trips. Were 20 and 11 min off.
- **Slot rule for hand-set legs:** the slot follows the regular run: the most real departures exactly on the minute, then within 1 min, then the smallest worst deviation. Odd trips (more than 3 min off any slot of the line between the same two stops) are listed as "off the pattern". This replaced a smallest-worst-deviation rule that put 504 at :01 instead of its real :06 and 514 6–9 min off on every leg.
- **Daily timetables must be balanced:** each leg of a daily line sends as many buses as the others, or buses pile up at one end day after day. `build_overrides` warns when they don't.
- **Tables of hand-set lines** are read in the hand-set window (`roster.json` → `anchors`), so 514 shows its 16:00 pattern, not the automatic 13:30.
- **Cross-check with the Ostrava lib's `exactify` (0b, 20 Oct):** it changes none of the remaining automatic rows. It also wouldn't catch the hand-set ones: it needs ≥ 6 departures over ≥ 2 h, and these hourly town lines have 3–4 in the window. So the hand-sets stay, and exactify isn't called here.
- **Left as approximate on purpose:** 517 (one bus, irregular round trips about every 65 min; every 60 is up to 18 min off, on the To check list) and 516 (hourly :50 until 15:50, then 17:05 and 18:10).

## Core points and repeating intervals (owner, 20 Oct 2026: Ex4)

The owner: "Look at how I did in the save game Ex4 - there is also a very irregular service, but I defined it in core points, created a repeating interval and it suddenly made sense. 501 mostly goes to Dětmarovice, žel.st. some elsewhere." Then: "Could we take 503 to be one of the legs of the 501/504?"
- **Ex4 in the save (FORK-CZR-VZ.sve, line ids 2157, 2624, 2625):** one line per destination: Ex4/1 Warszawa – Wien every 240; Ex4/2 Kraków – Wien and Ex4/3 Warszawa – Budapest every 480. Each is timetabled only at core points (termini, Bohumín, Břeclav), some with a departure window. Together they reproduce the irregular real service.
- **Method here:** read a line's trips at its core points, by the time each trip passes them (`core: true` legs), not by where it starts or ends, over the whole operating day (`fitwin` 5:00–23:00, not only the afternoon band). Find the interval that repeats there. Give each destination variant its own Simutrans line on a longer interval, offset so the lines don't run together.
- **The Orlová trunk (501, 504, 503):** at Lazy, Lutyně and Dětmarovice, železniční stanice it is one hourly bus.
  - Lazy at :06 in odd hours runs to Dětmarovice: Simutrans line 501, every 480 with three slots (11:06, 13:06, 15:06 …), via 501's path (Poruba, kulturní dům; Lutyně, Zátiší).
  - Lazy 9:06 and 17:06 run on beyond the station to Elektrárna and Koukolná: 501B, every 480. It is the fourth slot, as Ex4/2 and Ex4/3 run beside Ex4/1.
  - Dětmarovice, železniční stanice at :18 in even hours: both lines, including trips that start further out.
  - Lazy at :06 in even hours turns at Lutyně: 504, one circuit every 240 that alternates via Poruba, škola (8:06, 12:06, 16:06) and via Důl Lazy, the 503 leg (10:06, 14:06, 18:06; 503's real trip is 14:00).
  - Lutyně → Lazy at :35 in odd hours: 504.
  - 1 bus each for 501, 501B and 504. The real operator runs it with one bus. Pooling them into one circuit would be the owner's choice.
- **Accepted differences:** 504's own Dětmarovice trips (8:06 and 18:06 to the railway station, 9:06 to Elektrárna) are on the Dětmarovice lines' slots, not 504's. 501's 13:06 and 14:18 slots have no real trip (its 12:58 turns at Lutyně). The 501/504 split by hour parity, not by line number. Lutyně itself is untimed on 501; it could be added as a timed core point (towards Dětmarovice :33, towards Lazy :30), as Ex4 times Bohumín and Břeclav.
- **Other lines read over the whole day:** 405 is exact at :22/:44 all day. 514 runs :27 / :48 and back as 520 at :25 (9:25, 10:25, 11:25, 19:25), so 2 buses, not 3. 516 runs :50 from 8:50 to 15:50. 517's commonest minutes are :15 / :36.
- **Timed at terminals, worked back from knots (owner, 20 Oct 2026: "Time the Koukolná branch from the terminal, just calculate the departure so it is in correct time in the knot at nádraží"):** a bus waits only at its terminal, unlike a train held at a junction. A leg option `knot` (+ `knot_rt`) moves the slots and real times given at the knot back by the running time terminal → knot, and the knot gets no timetable. 501B leaves Koukolná :09 (10:09, 18:09) to pass Dětmarovice, železniční stanice at :18. 406 leaves Pašůvka :26 / :56 to pass Prostřední Suchá, železniční stanice at :28 / :58. Empty returns (no real trip) stay untimed, and the bus waits at the next terminal (417B, 418, 515B). The general method for all bus sheets is `../bus-schedule-method.md`.
- **Matching live buses (tested on the 14:53 data, 20 Oct):** a hand-set line takes only buses whose trip has both ends on its termini, anywhere in its window (±30 min), nearest its slot. 417 and 417C share Těrlicko, so one end isn't enough. A surplus on a hand-set line keeps the bus nearest its slot (402B Stonava). Automatic branches prefer a both-end match (410 Podlesí vs Šumbark, both to Dolní Datyně). Only automatic branches of one route trade buses in the rebalance step. Live stop names get the terminus alias (Podlesí, Těšínská).
- **Observation:** a hand-set line is observed at each of its slot departures in its window (departure − 5 min until arrival), so 501B's 17:06 and 409's 16:46 runs get the buses actually on them.

## Method test by the Ostrava session (20 Oct 2026)

The owner asked to test the written method (`../bus-schedule-method.md`) by having the Ostrava bus session apply it to its regional ODIS lines; it runs on a smaller model. Its report is `../ostrava-bus/method-check-odis-2026-10-20.md`. It applied the method correctly and found two corridor pairings: 534 + 535 every 30 at Hranečník (9 → 6 buses), and 442's :05/:10 returning as 441's :32/:47. It listed 9 points where it had to use judgement, and all are answered in method version 2 (model hour, interval choice, Step 5b pairing at shared terminals, and others). Step 5b re-run on this sheet finds only pairings already modelled (401/406, 501/504, 514/520).

## No daily lines (owner, 20 Oct 2026)

"Now I don't like 1440 lines - in game that is not found. 8 hrs should be the very maximal interval (still not preferred). If the only way to model 1440 is 1440 reconsider - we can bend the reality a bit."
- 402B Stonava: every 480, Šumbark 12:23 / Stonava 13:05 (repeats at 4:23 and 20:23, clear of the afternoon).
- 411B Lapačka: every 480, Podlesí 18:25 / Lapačka 19:05.
- 418: circuit every 240, Podlesí 13:30 / 14:18, Šenov 15:15 / 15:45, 1 bus. 12:45, 18:10 Šenov and 16:50 Bludovice are off the pattern; other lines serve Bludovice.
- 420: every 160 (its 12:30 and 15:10 trips are exactly 160 apart), back 13:03 (15:38 is 5 min off).
- 513: no own line. All its stops are on other lines, and its Staré Město trips are 514 buses going back, so it is carried by 514.
- 515 / 515B: every 480, because the mine shifts change every 8 hours. Fryštát :54 / Důl Darkov :10; Staré Město, Nové pole :15.
- Need 71 → 68. Coverage still complete. The renderer and builder no longer produce 1440 lines (`config.max_interval_rule`).

## Save game

- Per the pak session (f3, 20 Oct 2026, save FORK-CZR-VZ.sve of 05:33), the save has **no** Havířov, Karviná or Orlová MHD lines yet, so every Simutrans line on this sheet is new in the game. f3's ODIS migration plan for the regional lines doesn't touch them.
- The Havířovsko III regional lines 441/442/445/448 change to the red kraj livery from 12/2027 (not drawn yet). They are regional lines, not on this sheet.

## How to update

1. On a normal weekday, start the detached poller before 13:00 (step 2 above).
2. Set `snapshot`, `vehicle_day`, both labels and `network_state_*` in `config.json`. Re-read the diversion versions and the výluky, and update `network_state`.
3. `python scripts/run.py --fetch` after the peak (~17:45).
4. Check the To check list and any line with many designed buses.
5. Republish to `artifact_url`. Send `pak_request.md` to the pak session if it lists anything new.
