# City tram sheets: data pipeline

Each city's tram sheet ("<City> Tram Peak Fleet.html" or "<City> Tram Vypravenost.html" in the project root) is
built by a pipeline in `pipeline/<city>/`. The pipeline re-runs from stored raw data, so a sheet can be
refreshed when the timetable, the fleet or the pak changes.

| City | Folder | Maintained by session | Output |
|---|---|---|---|
| Brno | `brno/` | simutrans-timetable-c6 | Brno Tram Peak Fleet.html (closure state 27 Sep), Brno Tram Fleet from 29 Sep.html |
| Plzeň | `plzen/` | simutrans-timetable-c6 | Plzeň Tram Peak Fleet.html |
| Praha | `praha/` | simutrans-timetable-9e | Prague Tram Peak Fleet.html |
| Olomouc | `olomouc/` | simutrans-timetable-a2 (smaller cities, from 29 Sep) | Olomouc Tram Peak Fleet.html |
| Ostrava | `ostrava/` | simutrans-timetable-10 | Ostrava Tram Vypravenost.html |
| Most–Litvínov | `most-litvinov/` | simutrans-timetable-10 | Most-Litvinov Tram Vypravenost.html |
| Brno buses | `brno-bus/` (imports `brno-trolleybus/scripts/common.py`) | simutrans-timetable-3a | Brno Bus Peak Fleet.html |
| Brno trolleybuses | `brno-trolleybus/` (imports `brno/scripts/common.py`) | simutrans-timetable-3a | Brno Trolleybus Peak Fleet.html |
| Praha trolleybuses | `praha-trolleybus/` | simutrans-timetable-5a | Prague Trolleybus Peak Fleet.html |
| Praha buses (PID 100–299, game check) | `praha-bus/` | simutrans-timetable-5a | Prague Bus Lines Check.html |
| Pardubice (trolleybuses + buses) | `pardubice/` (imports the Ostrava tram and trolleybus libs and Brno `mark_spares`) | simutrans-timetable-a2 | Pardubice MHD Peak Sheet.html (https://claude.ai/artifact/KrzshkuVv9T5GqpiUKLJ7y) |
| Plzeň trolleybuses / buses | `plzen-trolleybus/` (imports `plzen/scripts/common.py` and `brno-trolleybus/scripts/common.py`; stores the raw data for both), `plzen-bus/` (runs the `plzen-trolleybus` scripts with `--base`) | simutrans-timetable-a2 | Plzeň Trolleybus Peak Fleet.html (https://claude.ai/artifact/B9vVcHutYdXdg4sscpA1gR), Plzeň Bus Peak Fleet.html (https://claude.ai/artifact/LE4trKFDZjkAjpX2EhvJCa) |
| Olomouc buses | `olomouc-bus/` | simutrans-timetable-a2 | Olomouc Bus Peak Fleet.html (https://claude.ai/artifact/MJz5Q7xYehTCPKhpBDfLHG) |
| Most–Litvínov buses | `most-litvinov-bus/` (imports the most-litvinov tram lib, read-only) | simutrans-timetable-a2 | Most-Litvinov Bus Vypravenost.html (https://claude.ai/artifact/TUU9pmZU3fcjJK95Fe4ZPN) |
| Ostrava trolleybuses | `ostrava-trolleybus/` (imports `ostrava/scripts/lib.py`) | simutrans-timetable-f5 | Ostrava Trolleybus Vypravenost.html |
| Ostrava buses | `ostrava-bus/` (imports the tram and trolleybus libs) | simutrans-timetable-f5 | Ostrava Bus Vypravenost.html |
| Havířov, Karviná, Orlová buses (Transdev Slezsko MHD 401–421, 434, 501–505, 511–520) | `havirov-karvina-orlova/` (imports `ostrava/scripts/lib.py` and the pure functions of `ostrava-bus/scripts/lib.py`) | simutrans-timetable-a4 | Havirov-Karvina-Orlova Bus Vypravenost.html |
| ODIS regional buses of Havířovsko, Karvinsko, Orlovsko (Transdev Slezsko licences 912xxx, 873xxx, 874xxx; 440–442, 531, 534, 535 stay on the Ostrava sheet) | `odis-regional-hko/` (imports the Ostrava tram/bus libs; reads the Havířov/Karviná/Orlová JDF, live poll and fleet) | simutrans-timetable-6b | ODIS Regional Havirovsko Karvinsko Orlovsko.html |
| ODIS regional and town buses of Českotěšínsko, Frýdecko-Místecko, Frýdlantsko, Jablunkovsko–Třinecko + MHD Český Těšín, Frýdek-Místek, Třinec (licences 871, 863, 864, 861, 875, 865, 866; 383/387 on the Ostrava sheet, 365 on the HKO regional sheet, 655 on the Novojičínsko sheet) | `odis-regional-tfj/` (config + data only; built by `odis-regional-hko/scripts` with `--base odis-regional-tfj`) | simutrans-timetable-6b | ODIS Tesinsko Trinecko Frydecko.html |
| ODIS Opavsko, Vítkovsko, Hlučínsko + MHD Opava buses and trolleybuses (licences 902, 903, 904, 905; trolleybuses 905201–905204 from the city-transport JDF) | `odis-regional-opavsko/` (built by `odis-regional-hko/scripts --base odis-regional-opavsko`; `post_roster` fill_designed for 204) | simutrans-timetable-6b | ODIS Opavsko Vitkovsko Hlucinsko.html |
| ODIS Novojičínsko Východ + Západ, Bílovecko + MHD Nový Jičín, Studénka (licences 883, 882, 884, 886, 887; 351/355/980/985 on the TFJ sheet, 261/263/270/285/678 on the Opavsko sheet) | `odis-regional-novojicinsko/` (built by `odis-regional-hko/scripts --base odis-regional-novojicinsko`) | simutrans-timetable-6b | ODIS Novojicinsko Bilovecko.html |
| ODIS Krnovsko, Bruntálsko, Rýmařovsko + MHD Krnov, Bruntál (licences 852, 853, 854, 856, 855; 260/920 on the Opavsko sheet) | `odis-regional-bruntalsko/` (built by `odis-regional-hko/scripts --base odis-regional-bruntalsko`) | simutrans-timetable-6b | ODIS Bruntalsko Krnovsko Rymarovsko.html |
| Czech long-distance rail (R, Ex, IC, EC, SC, rj, RegioJet, Leo Express; timetable only, no fleet) | `md-cr/` (own rail rules in its README) | simutrans-timetable-b2 | MD-CR.html |

## Bus schedule method (regional lines and small-town networks; not Ostrava, Prague, Olomouc)

`bus-schedule-method.md` holds the owner's method from 20 Oct 2026: read the whole day; read trips at core points; find the repeating interval; give destination variants their own longer, offset intervals (the owner's Ex4); time terminals worked back from the knots (buses, unlike trains, wait only at terminals); fold sparse lines into the line they belong to; put every stop on a Simutrans line; size from the pattern; review by hand. Its check list must pass before any regional or small-town bus sheet is published. Big-city sheets (Ostrava, Prague, Olomouc) model local lines at their afternoon peak with their unique stops (owner, 20 Oct 2026). Reference implementation: `havirov-karvina-orlova/` (`lib.build_overrides`, `override_need`).

## Layout of a city folder

```
pipeline/<city>/
  README.md          sources, steps, every manual decision, and "How to update"
  states/<name>.json one file per network state: vehicle date, GTFS service date, line definitions,
                     overrides, pak object map, output file name, texts
  scripts/           numbered Python scripts (stdlib only) and run.py
  assets/            fixed inputs: page style, terminus layouts, pak map
  data/raw/<kind>/<date>/   downloads exactly as fetched (HTML pages, GTFS zip, scraped record JSON)
  data/derived/<state>/     JSON produced by the scripts
```

`python scripts/run.py --state <name>` rebuilds a sheet from the stored raw data.
`--fetch` downloads fresh raw data first. Every script can also be run on its own.

## Shared rules

These rules come from the user, or were agreed between the sessions on 28 Sep 2026. Apply them in every city.

### Which day
- **Vehicles:** the afternoon peak of the last weekday before the target date. When a city has no records for that day, use the latest complete weekday, preferably a Friday, and say so on the sheet.
- **Network:** the timetable in force on the target date. Short-term closures are modelled as the regular state; long-term closures are modelled as they run.
- **Peak:** about 15:00–17:00, with 16:00 as the reference hour. Morning-only duties are left out and listed under "Not counted".
- **Swaps:** the notes give no time. Resolve a swap from where the cars turned up later that day; otherwise list the replacement car and name the replaced one in the note.

### Vehicle display
- Use full type names; no shorthand anywhere.
- Write a coupled set as `A + B`, with the numbers and the types in the same order.
- Every vehicle is a 3-line cell:
  1. numbers · depot
  2. full types · length
  3. pak core
- The type must be visible next to every vehicle, never only in a hover tooltip or a summary count.
- Full object names, section chains, real liveries and car units appear once, in the "Pak128 objects" table.

### Page header (user request, 29 Sep 2026)
- Every fleet sheet has the Prague tram sheet's sticky bar under the page header: line badges, depot links with counts plus the main section links, and a vehicle search (`#q`) that highlights every `[data-v]` vehicle number.
- Anchors must land below the bar at any width: `scroll-margin-top: var(--stick)`, with `--stick` set by script to the bar's height + 8 px on load and resize. A fixed margin hides headings on phones, where the bar is 120–240 px tall.
- Drop-in implementation: `brno/scripts/sticky.py` (CSS, `controls()`, script). The same file is copied into plzen, ostrava and most-litvinov; the praha, olomouc and praha-trolleybus templates have their own copy of the bar.

### Pak objects (custom Czech pak128)
- **Sync:** send the pak128 session (simutrans-custom-czech-pak128-77) the exact peak types and car numbers. Impossible sets (missing objects, couplings that don't work) are the pak's job to fix: ask for them.
- **Pak core:** the last segment of the object name, after the `VZ-<city>-<type>-<livery>-` prefix. Examples: `VZ-DPBrno-EVO2-dpmbbilocervena-EVO2` → `EVO2`, and a pair → `T6A5 + T6A5b`.
- **Multi-section trams:** show the first core only.
- **Livery in the core:** append the livery to the core only where the pak has more than one livery object for that type.
- **Meaningless core:** if the last segment says nothing (e.g. `A`), show the family name instead.
- **Stand-ins:** a nearest or other-city object is written `≈ core`, and its reason is given once in the pak table.

### Simutrans schedule (the user's fork)
- **Fields:** set per stop entry on the Scheduling tab: Departure every, Offset, Also at (up to 7 extra offsets, so at most 8 departures per cycle), and Leave up to (default automatic, half the gap). Everything is in whole calendar minutes. Offsets count from midnight and must be less than the interval.
- **Fit:** for each terminus and destination, take the longest stretch of the afternoon peak that one interval, offset and Also-at set reproduces exactly.
  - Clip the stretch to the pattern's first and last real departure.
  - A stretch with fewer than 2 departures is never a fit.
  - Prefer the simplest pattern (fewest slots, then the shortest interval) among fits covering at least 80 % of the best one.
  - Prefer intervals that divide 60, then those that divide 1440. Other intervals are allowed where only they are exact (the fork then restarts the pattern at midnight).
  - Anything approximate is labelled with its largest deviation.
  - De-duplicate candidate runs on (slots, start, end), never on the slot set alone. Otherwise a pattern that also runs earlier in the day, outside the peak, hides the peak run. This is a bug fixed on 28 Sep in every copy of `runfit`.
- **Loop termini:** set every departure 1 min before the timetable departure, so the tram clears the loop on time. Offset and each Also at become (real − 1) mod interval; the interval stays the same. Stub and turn-back termini keep the real minute. Every sheet says this visibly and shows the real minutes under the set values.
- **Which entry:** put the timetable on the entry the tram leaves from (the boarding stop of a loop).
- **Separate lines:** short workings and branches are separate Simutrans lines, because Also at cannot change the route. Their offsets interleave. The exception is a line whose trams alternate between branches: model it as one line with the shared terminus in the schedule twice (Plzeň 4).
- **Depot runs:** not modelled. Branches with fewer than 3 trips in the window, and pull-in branches listed in the config, are merged into the main branch from the same terminus.
- **Trams per line:** use `cycle_need` (in brno/plzen/praha/olomouc `scripts/common.py`). Follow a tram leaving around 16:00 through its round trip, taking at each end the first departure at least the layover later. The layover is 3 min by default, or the terminus's own shorter turnaround where the timetable shows one (Prague 31 at Vysočanská: 1 min).
  - Don't size lines by FIFO trip chaining. Depot pull-outs and pull-ins make it miscount (Brno 10 came out at 7 instead of 4–5). Chaining is still fine for asking whether trams switch between branches, on in-service trips only.
  - Keep the operator's slack. If the recorded courses exceed the cycle need, carry the same surplus into a new timetable (Brno from 29 Sep: line 3 19 → 16, line 12 14 → 16).
- **Split lines:**
  - Where course numbers mark a branch, split by range (Brno 5S = kurzy 21–27; Prague 17/21–37).
  - Otherwise, size each branch by `cycle_need` and pick the cars. Prefer peak-only courses, and say on the sheet that the pick is a choice (Brno 8S).
  - Spares: keep them on the main line when the other branch is a reinforcement (Brno 8); split them evenly between two full branches (Prague 22).
- **Short workings:** a variant is modelled as its own line only when it is a peak trip. That means all of:
  - ≥ 3 trips between 15:00 and 17:59;
  - no depot at either end;
  - at least one departure between 16:00 and 16:59 (user ruling of 28 Sep: Prague's 3 Nádraží Braník, 9 Hotel Golf and 22 Nad Džbánem end at 15:38–15:47 and are not peak trips);
  - it runs alongside the main pattern in the peak, not as the line's post-peak form that replaces it (Brno 7 Zemědělská from 16:24, Brno 2 Ústřední hřbitov from 16:41).

  Anything else is listed as "not a peak trip, not modelled", with no values for a separate line.
- **Shared pools:** one Simutrans line covering two real lines (Prague 5 + 6), or two lines drawing from one pool of trams (Olomouc 3 + 5), are the user's modelling choice. Mark them as such, with the real share that runs through.
- **Designed trams:** when the recorded courses are fewer than the need, the user allows adding trams. Each is marked "designed, not recorded" on the sheet, with the date of the line history it comes from and a check that the car wasn't used anywhere that day.
- **Roster coverage and spares (user, 29 Sep 2026):** when the line history holds more free cars than the designed slots need, choose so that no type is skipped. Every vehicle type in the line's full roster (history plus logged cars) must be represented among the vehicles actually used. The free history cars left over are shown on the sheet with a "not needed" marker, and are not counted. Reference implementation: `praha-bus/scripts/04_courses.py`. **Logged surplus too (user, 29 Sep, confirmed in the Brno session):** the rule also covers lines with more vehicles *logged* that day than the need: keep exactly the need counted, one of every roster type first, drop afternoon-only kurzy first (then the highest kurz numbers), and mark the rest "not needed". Brno implementation: `brno-trolleybus/scripts/common.py` `mark_spares` (both Brno bus and trolleybus sheets).

### Timetable sources
- **GTFS:** use the calendar and calendar_dates of the service day.
- **JDF (CIS JŘ):** among the line versions valid on the day, the latest "valid from" wins, and ties go to the shortest validity.
- **Stored feed:** keep the feed's export date in the raw folder name.

## City decisions at a glance

The details and reasons are in each city's README and state or config files.

| City | Vehicle day / network | Split and pooled lines | Designed or moved trams | Other |
|---|---|---|---|---|
| Brno (closure) | Fri 25 Sep / 27 Sep | 5S = kurzy 21–27; 8S = kurzy 20, 26, 32, 42, 44, 46, 48 (7 of 24, sized by cycle) | — | Kurz parity is the depot (odd = Pisárky); 20 cars disagree with the register. Line 12 fit ±3 min. |
| Brno (from 29 Sep) | Fri 25 Sep / 29 Sep | as above | Surplus over each line's need marked not needed (spares rule, 29 Sep); the earlier 3 → 12 moves are dropped | Line 10 back to Komín; line 12 exact at every 14 |
| Plzeň | Fri 18 Sep (no records 23–25 Sep) / 27 Sep | Line 4 is one line with Košutka twice (trams alternate between Bory and Univerzita) | — | All termini are loops; the depot runs from Bolevec count in the pattern |
| Praha | Fri 25 Sep / 27 Sep | 17 by course range (1–17 / 21–37); 22 as two lines (0 of 41 trams switch; even split, a choice); 5 + 6 as one pooled line (user's choice; 19 of 25 run through). Short workings 3 Nádraží Braník, 9 Hotel Golf and 22 Nad Džbánem end before 16:00, so they're not peak trips and not modelled (user ruling). | 13/2–4 and 31/4–5 designed; 2/11 from 11 Sep; 2/12 a designed stand-in (9229); 22/42 → line 7 | 31 turnaround 1 min at Vysočanská. Nádraží Holešovice is a through stop (the 5 ↔ 6 number change), so it keeps the real minute; the loop rule once caught it by mistake through the words “no loop”. |
| Olomouc | Fri 18 Sep (25 Sep has 7 sets) / 27 Sep | 3 + 5 as separate lines from one pool (3/1–4 → 3, 3/5–6 → 5) | — | U Kapličky is a stub (real minute, bidirectional sets only) |
| Ostrava | 25 Sep / 27 Sep (no recorded courses on the day, so the chaining count is the baseline) | 4, 7, 8, 17 as branch lines. On in-service trips 8 and 17 keep to one end, and 4 and 7 mix irregularly, never A–B–A–B. Real minutes are kept, so the branches interleave. | None: with each terminus's own turnaround (`min_turnaround`), 3 needs 4 and 12 needs 8, equal to chaining. The "added to meet the round-trip need" mechanism stays. | JDF version choice |
| Most–Litvínov | see most-litvinov/README.md (no recorded courses) | One Simutrans line per DPmML line, no pools | Designed roster (config.json): needs 4/3/3/4, assigned 5/3/3/4 | — |
| Brno buses | Fri 25 Sep / 29 Sep (IDS JMK GTFS, route_type 3); 40–84, E50/E56/E75, x75 | Feed splits workings at timing points, so each line's leg order comes from `propose.py` (FIFO chaining → successor cycles): 40 one circuit via Úzká; 41, 49, 57, 58, 68, 72, 77, 78 split into branch lines (kurz allocation by need, a choice); 57 + 66 Lesná loop one line | Lines filed under other kurzy: 54→52, E50→50, 55/E75→58, 46/66→57, 70→42 (IDS PDFs, jrbrno); E56 has own kurzy filed as 56. 63 starts 1 Oct, left out; service day 29 Sep | Through stops keep the real minute (turn −1 elsewhere). One-way peak lines (E50, E75, 77A): untimed far end (every 0). BDS-BUS on 48/74 via seznam-autobusu.cz; pak stand-ins. |
| Brno trolleybuses | Fri 25 Sep / 29 Sep (IDS JMK GTFS, route_type 800) | 25 + 26 and 35 + 38 + 39 as one circuit line each (DPMB pools: only 25 and 39 kurzy exist); 30 and 37 split by kurz, a choice | 33: a designed return slot at Slatina, sídliště (9/h out, 6/h back in the feed) | All termini loops (−1), block turns included. `circuit_need` = `cycle_need` for N legs, with the timetable's own shorter turnarounds; one rate per Simutrans line (`runfit_rate`). Battery only on 21 and 30. 2 buses on trolleybus kurzy, marked and not counted. |
| Praha trolleybuses | Fri 25 Sep / 27 Sep (PID GTFS 29 Sep, route_type 11) | 52 and 58 as two branch lines each (course order, a choice; pooled alternative 9 / 13) | — (52/9, 59/6, 59/14 unrecorded, need still met) | All termini loops (−1). Battery sections from OSM trolley_wire vs GTFS shapes (`03b_offwire.py`). Fit core 16:00–17:00 (58 pattern starts 16:20). 51 and 53 hourly approximations. |
| Ostrava trolleybuses | Tue 29 Sep, observed in the DPO live feed 16:29–16:50 / 29 Sep (JDF versions as on 27 Sep). The Friday records carry no time and the duties interline, so they are a cross-check only. | 101 and 107 split into A (Hranečník, under the wire) and B (the battery branch to Radvanice / Bartovice); the branch is decided by live position (east of 18.322). No pools; the 1xx/2xx/8xx duties interline between lines. | 103 and 109: one designed bus each (the feed showed one fewer than cycle_need) | All termini loops (−1). `cycle_need_peak` skips round trips waiting over 30 min (107A: 5 → 3). Battery sections from mhd-ostrava.cz; the page checks that only battery buses run battery trips. |
| Ostrava buses | Wed 30 Sep, observed in the DPO live feed 15:50–16:15 (167 buses) / 30 Sep (CIS JŘ bus JDF export) | 47 of 57 DPO lines run in the afternoon: 56 Simutrans lines, branches by rule (≥ 6 trips 15–18 h, a 16:xx departure, no garage end), variant minutes folded into the main row | 16 designed from ODIS history (real cars, type coverage first); 10 not needed (logged surplus) | All termini −1. `cycle_need_peak` with max_wait max(30, 1.5 × headway); need = max(round trip, on the road with the cycle layover). Branches of a line rebalanced before surplus (34). |
| Plzeň trolleybuses | Fri 18 Sep (23–25 and 29 Sep have ≤ 1 record) / 29 Sep (PMDP GTFS, route_type 11) | 10 and 11 one line each with the shared terminus twice (branches alternate); 15N Nová Hospoda branch (highest kurzy, a choice); 22 one-way Malvíny → Koterov → Škoda VIII. brána with an empty return | None needed (56 counted, 26 not needed) | All termini loops (−1). Battery sections from OSM trolley_wire vs GTFS stops (the feed has no shapes; `03b_offwire.py` per-stop variant); only battery cars (26 TrNU, 27 TrNU, 26 Tr 565–582) on 11, 13, 22, 49, checked on the page. 18's cars also on 10/12/13 are counted there. All pak objects requested (VZ-PMDP-trolleybus). |
| Plzeň buses | Fri 18 Sep / 29 Sep (route_type 3); 20 lines | 33 + 40 a loop, two lines (both on 33 kurzy; 40 unlogged since Sep); 42 on 26 kurzy (inferred, marked not confirmed); 28 one line with CAN Husova twice; branches 26N, 30P, 41K | None needed (69 counted, 14 not needed); no subcontractor in the peak | All termini −1. All pak objects requested (VZ-PMDP-bus, two liveries). |
| Most–Litvínov buses | nominal Fri 25 Sep (no DPmML record exists) / 29 Sep (CIS JŘ bus JDF 5750xx/5760xx + tram replacement from the tram JDF) | Branches by the Ostrava bus rule: 5 and 30 split; 13 one line with its branches folded in; NAD (Chempark – Citadela replacement buses) one line at the tram minutes | All 49 designed with real numbers: evidence = 29 records (mostly 2023, by plate) + destination displays read off 114 photos (`assets/photo_lines.json`); then every fleet type × livery on a line (user, 29 Sep): 189 (NB 18 Prague red-white) on the tram replacement for 196, weekend-only double-decker 153 on line 16 for 24; displaced buses "not needed" | Pak requests: NB 12 and NB 18 in Prague red-white, Lion's City DD in BVG yellow |
| Havířov, Karviná, Orlová buses | Tue 20 Oct, observed in the ODIS live map (mpvnet.cz; plate → fleet number), each line in its own window ±20 min around its anchor / 20 Oct (CIS JŘ bus JDF of 20 Oct) | Branches, schedule, sizing by the Ostrava bus rules (imported); Karviná circular lines 511, 512, 516, 518, 519 one row each; 414 occasional, not modelled; 520 on 514's circuit; hand-set lines (`line_overrides`) for rotating buses, the 401/406 ring and sparse branches that are a place's only service (coverage rule: every afternoon stop on a Simutrans line) | Designed from line records since 2025 (town fleet first) | All termini −1. VZ-MHDHavirov/-Karvina/-Orlova objects only (pak session f3); ≈ substitutes in pak_request.md. 420 diversion modelled. |
| ODIS regional Havířovsko, Karvinsko, Orlovsko | Tue 20 Oct, ODIS live map (each bus's trips by licence and trip number) / 20 Oct (CIS JŘ bus JDF) | Every line hand-set with the bus schedule method v3 (`config.lines`): whole-day core points, Ex4 variant lines (shift variants every 480; a main line with seven slots of 480 where a variant takes the eighth hour), terminals worked back from knots; 553's two licences merged; shift and sparse lines whose stops other lines serve are listed (Step 8) | 58 seen, 9 designed (same line at another time, else a free regional bus of the nearest area); no bus on the HKO or Ostrava sheets | All termini −1. VZ-ODIS-bus objects, all exact. 582 diversion (to 30 Nov) left out; 532/552 diversions modelled. |
| Pardubice (DPMP, trolleybuses + buses, one sheet) | Fri 25 Sep / 29 Sep (CIS JŘ JDF export of 28 Sep: city export for trolleybus lines, bus export for bus lines) | 37 Simutrans lines on 30 DPMP lines, branches by the Ostrava bus rule (1D, 2P, 6H, 8S, 9S, 12M, 30C); 33 pooled on 3's kurzy, 88 on 8's (no records of their own) | 9 designed from line history before the vehicle day (2, 18, 88, 16, 22, 90); 32 not needed | All termini −1. Entries reproduce the 16:00 hour (Brno bus rule); ≤ 8 departures a day → every 1440 with all of them. Line 20 (morning) and 90 (flights, Monday trips) on their own times (old sheet decisions). Battery sections from the old sheet; own `jdf_trips` (JDF 1.10 columns, Caskody type 1). Plain-white liveries requested from the pak. |

## Updating a sheet
Each city README has a "How to update" recipe. It always comes down to:
1. Fetch the new GTFS or JDF (and new vypravenost if the fleet should follow), into new dated raw folders.
2. Add or copy a state file pointing at the new dates.
3. Run `run.py --state <name>`.
4. Compare the "What changes" table (states can name a `compare_with` state) and the schedule against the previous state.
5. Re-publish to the same artifact URL, and tell the user what changed.
