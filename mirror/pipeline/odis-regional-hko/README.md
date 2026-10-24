# ODIS regional buses: Havířovsko, Karvinsko, Orlovsko (vypravenost sheet)

Output: `ODIS Regional Havirovsko Karvinsko Orlovsko.html` in the project root, published at the URL in `config.json` → `artifact_url` (republish to the same URL). Built on 21 Oct 2026, when the owner asked: "Now we've done regional lines - study deeply the rules. Can you do ODIS Regionals - "Orlovsko", "Karvinsko", "Havířovsko"?" Shared rules are in `../README.md`. The schedule method is `../bus-schedule-method.md` (v3), which applies in full here: every line on this sheet is a regional line.

## Scope

- **The three areas are kraj contract areas** of Transdev Slezsko (IČO 45192081). The kraj gives each area its own licence prefix: 912xxx Havířovsko (I and II), 873xxx Karvinsko, 874xxx Orlovsko. For comparison, 871 is Českotěšínsko, 863 Frýdecko-Místecko and 904 Hlučínsko. The prefixes were checked three ways:
  - On the live map, 912 lines run from provozovna Havířov with 42-/43- buses, 873 from Karviná with 52-, and 874 from Orlová with 51-.
  - The register notes say "provozní oblast Karvinsko", "Havířovsko I a Havířovsko II", and so on.
  - The kodis.cz line groups (440–465, 531–583) cover the same ODIS numbers.
- **The ODIS number** is the last three digits of the licence. One line can hold licences in two areas: 553 is 873553 + 874553. `02_timetable.py` merges trips by ODIS number, and each trip keeps its licence (`lic`). 553 is shown under Orlovsko.
- **53 ODIS numbers.** 47 have afternoon trips on Tue 20 Oct 2026; 555 and 566 only run in the morning; 391, 392, 562 and 990 have no Tuesday trips.
- **On the Ostrava sheet already:** 440, 441, 442 (Havířovsko), 531, 534 (Karvinsko) and 535 (Orlovsko). They stop at Ostrava, Hranečník and are modelled with their buses in that sheet's "All lines at Hranečník" section. Here they are listed with a link and not repeated. Their stops count as covered.
- **Not modelled (method Step 8, listed with the reason in `config.unmodelled`):** shift and sparse lines whose afternoon stops are all on other lines. These are 444, 446, 455, 457, 461, 463, 540, 541, 550, 554, 557 and 564.
- **Modelled:** 29 lines as 37 Simutrans lines, needing 67 buses.

## Sources

| What | Where | Notes |
|---|---|---|
| Timetable | CIS JŘ bus JDF export of 20 Oct 2026, stored by the Havířov/Karviná/Orlová pipeline (`config.jdf.zip` points to it) | The licence scan is by prefix and IČO. Version rule as shared. `02_timetable.py` needs that zip; if the other pipeline's raw folder goes, `data/derived/trips.json` is the durable copy (run from `03_read.py` on). |
| Live vehicles | ODIS live map (mpvnet.cz), polled every minute 13:05–19:30 on Tue 20 Oct 2026 by the Havířov/Karviná/Orlová pipeline (whole region, every carrier) | `01_live.py` writes the compact `data/raw/2026-10-20/live_compact.json`, so this sheet keeps its observation if that folder goes. `cn` = licence\|line\|trip\|…\|PLATE; the trip number is the JDF spoj. |
| Fleet | the Havířov/Karviná/Orlová pipeline's `fleet.json` (seznam-autobusu register of Transdev Slezsko, carrier 28, with plates) | It covers every Transdev Slezsko bus. Its "Dekstra LE 37 L CNG · 12 m" is shown as a midibus. |
| pak128 | `C:/Users/vojte/Developer/simutrans-custom-czech-pak128`, `build/VZ-ODIS-bus/*.dat` | `06_render.py` reads the installed objects. Every bus has its exact object; `pak_request.md` is empty. |

## Steps (`scripts/`, stdlib-only Python; run with `-X utf8`; `python scripts/run.py` runs them all)

1. `01_live.py`: the live poll → `live_compact.json` (every Transdev Slezsko bus, one row per licence and trip).
2. `02_timetable.py`: licences by area prefix → `trips.json` (merged by ODIS number), `line_class.json`, `versions.json`. `config.regular_not_diversion` forces the regular version for a short diversion (582).
3. `03_read.py`: the whole-day reading (Steps 1–3) → `reading.json` and `derived/reading/<L>.txt`. It lists every trip with its time at each core point, its path (the differences from the main path), the bus seen on it, and the afternoon plate chains. Read these before changing a line. It also writes `chains.json`, each plate's trips in order.
4. `05_schedule.py`: `config.lines` → `schedule.json`. It builds the hand-set Simutrans lines (see below), the stats, the knot checks, the needs and the coverage check (Step 9, `_coverage`, which must have no uncovered stop).
5. `04_roster.py`: the buses of every Simutrans line (see Roster).
6. `06_render.py`: the sheet and `pak_request.md`.

## How a line is set (`config.lines[L]`)

- `core`: the core points, shown on the card and used for the knot check.
- `note`: the reading in words, for the card.
- `anchor`: optional; overrides `line_anchor` (451 and 533 at 16:00, see below).
- `sim`: the Simutrans lines, each `{name, every, legs, why?, window?}`.

A leg is `{fr, to}` plus these optional keys:
- `at`: slots at `fr`, as minutes or 'H:MM', taken mod every.
- `knot` + `knot_at`: slots at a knot. The terminal departure is the knot time minus the running time fr → knot (Step 6).
- `core_to`: the core point a trip must pass to count, when it may end short of `to` (369 ends at Havířov, Město).
- `via` / `notvia`: on the whole trip; they separate variants (Autopal, Kovošrot, Mexico, Elektrárna).
- `untimed`: an empty return, Departure every 0.
- `stops_via`: the path the Simutrans line takes, when a variant's own stop must be on it (367 back via Zámostí).
- `rt` / `lay`: running time and wait, when the computed ones must be overridden.

What the builder does with these:
- **Trip ownership.** A trip read between the same core points goes to the leg whose slot is nearest, compared at the read point. More than 3 min from every slot is off the pattern.
- **Running time and stops** come from the leg's own trips that run the whole leg, around the window.
- **Need.** `slot_need` from the Ostrava bus lib, which matches arrivals to departures at each terminal. Lines that visit a terminal twice use `pattern_need` instead.

## Decisions (21 Oct 2026)

- **Model hour:** each line's anchor (`line_anchor`).
  - 451 and 533 are set to 16:00. Their busiest stretch, 13:00–15:00, is shift extras on top of a regular every-30 pattern, and the extras are listed.
- **Ex4 variants:**
  - Shift variants are their own line every 480, as in reality: 451 Elektrárna, 553 Autopal, 559 Kovošrot, 582 ČSM.
  - Short-turn and route variants are their own line: 553 Orlová, 543B, 558 Pudlov, 565 Kopytov.
  - Where a variant takes one hour of an hourly line, the main line is written as every 480 with seven slots, so the two never leave together (559, 582; as the HKO 501/501B trunk).
  - The every-30 trunk of 451 can't drop one slot (16 a period is more than the 8 an entry holds), so 451 Elektrárna leaves 15 min early: 12:45, real 13:00.
- **Step 5b (plates):**
  - 543: the 14:12 bus comes back as the 15:04, and the 13:12 and 15:12 buses go on as 546 short trips to Bohumín. So 543 is every 120, both ways, one bus; 543B is out only with an empty return.
  - 553 Orlová has an empty return, because its real buses go on as other lines at Lutyně.
  - The Frýdek-Místek corridor (365–369) rotates its buses between all five lines at both ends. One Simutrans line per real line is kept. Pooling would be the owner's choice.
- **Coverage:** every place served 13:00–19:00 is on a line here or on another sheet.
  - The variant lines above exist because each is the only service somewhere: Dětmarovice, V polích; Rychvald, Autopal; Kovošrot; Stonava, Mexico; Pudlov (453 and 558 Pudlov); Vrchlického.
  - 367 runs back via Bruzovice, Zámostí.
- **Network state:**
  - 532 and 552 run on diversion timetables (1 Aug – 12 Dec, same stops), modelled as they run.
  - 582's diversion (28 Aug – 30 Nov) is short, so the regular route is modelled.
- **Approximate lines** are on the page's To check list, with their slots and the real departures: 365, 366, 368, 369, 445, 448, 452, 465, 532, 538, 559, 560, 565 and others. These real timetables run at no fixed minute. Each card names its off-pattern trips.

## Roster (`04_roster.py`)

- **Evidence:** the line's own trips in its window (anchor −30 to +90, widened by 30 min), or its pattern trips 12:30–19:30 for a shift line. The live map gives the plate on each trip.
- **Assignment:** one bus to one Simutrans line, by augmenting-path matching, closest sighting first (the Havířov/Karviná/Orlová rule). Then one of every seen type is kept before a second of the same type.
- **Exclusions:** buses on the Havířov/Karviná/Orlová town sheet (its `roster.json`) or on the Ostrava sheet's Hranečník cards (`odis.json`) are not used here. Today that is 95 plates.
- **Designed buses** fill short lines:
  - first a bus seen on the same line at another time that day, free in this line's window;
  - else a free regional bus (not on any line in the window), from the line's area first, then the nearest areas (Orlovsko → Karvinsko → Český Těšín → Havířovsko);
  - each one carries its reason.
- **Totals on 21 Oct:** 65 seen, 2 designed. Depots are the live map's branch for seen buses, and the home area for designed ones (Český Těšín 73- buses also work Karvinsko).

## Coordination

- This pipeline imports the Ostrava tram/bus libs and the Brno trolleybus `mark_spares`. It reads, and never writes, the Havířov/Karviná/Orlová pipeline (JDF, live poll, fleet) and the Ostrava bus pipeline (`odis.json`, DPO trips for coverage).
- If either of those sheets changes its roster, re-run `04_roster.py` here: a bus stays on one sheet.

## How to update

1. On a normal weekday, the Havířov/Karviná/Orlová pipeline's detached poller must run 13:00–19:30 (its README, step 2), whole region.
2. Point `config.snapshot`, `vehicle_day`, the labels, `jdf.zip` and `live.dir` at the new day.
3. Re-check diversions (`versions.json`, diversion flag) and update `network_state` and `regular_not_diversion`.
4. `python scripts/run.py`.
5. Read `derived/reading/<L>.txt` for each line whose timetable changed, and adjust `config.lines`.
6. Check the To check list and the coverage section (no uncovered stop).
7. Republish to `artifact_url`.

## A second sheet from the same scripts (`--base`)

`scripts/` also builds the Těšínsko/Třinecko/Frýdecko sheet: `python -X utf8 scripts/run.py --base odis-regional-tfj` (see `../odis-regional-tfj/README.md`). Every script reads `config.json`, `data/` and the output name from the base folder. Keys a sheet may add, all optional (this sheet uses none of them, so its output is unchanged):
- `areas[]`: `kind` (regional / mhd), `town` (town JDFs write stops without the town name), `ic` (another operator's IČO), `operator`, `note`, `near` (designed-bus fleet prefixes); `towns` lists the place names that are not a town stop's prefix.
- `other_sheets.<key>`: `lines`, `schedule`, `heading`, `why` for another regional sheet whose lines are shown and whose stops and buses count as taken.
- `pak.packages` and `pak.rules` (rule-based objects across several packages), `texts` (page wording), `area_home`, `plate_lookup` + `plate_guess` (`01b_plates.py`), `designed_same_area`.

Added 21 Oct 2026 for the Opavsko, Novojičínsko and Bruntálsko sheets (built in parallel):
- `new_sheet.py <spec.json>` writes a skeleton config from a short spec (folder, title, areas, operator IČO, live carriers, fleet carriers); it copies the JDF/live/version settings from the TFJ sheet, derives `towns` from the JDF and the Ostrava-card lines, and never overwrites a config.
- `01c_fleet.py`: `fleet.carriers = [{id, name, tractions, live_plate?}]` fetches the seznam-autobusu registers (Z-Group bus 240, Transdev Morava 7546, MDPO 338, Transdev Slezsko 28) into the sheet's `data/derived/fleet.json`; `live_plate` ("MDPO{num}") maps a carrier that sends a fleet-number code instead of a plate. Pages are kept; `--refresh` fetches again.
- `jdf.extra_zips`: more CIS JŘ exports read with the same version rule (the city-transport `draha/mestske/JDF.zip` holds the Opava trolleybus lines 905201–905204); `line_class.json` records `traction` (A bus, T trolleybus). An area may take a longer prefix (`90520` for the trolleybuses) listed before the general one.
- `other_sheets.<key>` may name a sibling sheet that has no outputs yet (`lines`, `label`, `short`, `heading`, `why`, `url` null): 05 counts those lines' afternoon stops as covered, 04 skips it, 06 lists the lines as modelled there. Fill `derived`/`schedule`/`url` once that sheet exists and rerun 04–06 in precedence order (Ostrava → HKO town → HKO regional → TFJ → Opavsko → Novojičínsko → Bruntálsko).
- 05 lists terminal waits in leg order (deterministic output); 03b skips a line with no end-to-end trip instead of failing.
- `run.py` runs `01c_fleet.py` too (offline once the register pages are kept; a sheet without `config.fleet` skips it) and, right after `04_roster.py`, every script in `config.post_roster` (paths relative to the sheet folder; Opava: `authoring/offwire.py`, `authoring/alt_drive.py`, `authoring/fill_designed.py`).
- 22 Oct: `06_render.py` shows a vehicle's `alt` after its type ("+ battery", set by a sheet's post_roster step) and, when the sheet has `data/derived/offwire.json`, an Overhead wire table on each trolleybus card. Sheets without either render byte-identical (checked on HKO, TFJ, Novojičínsko and Bruntálsko).
- `01b_plates.py` keeps every current paint layer of a looked-up plate ("bílá & červené logo Transdev & logo dopravy …"), not only the last one; `01c_fleet.py` reads SOR lengths without "M" ("CN 10,5" → 10.5 m).
- 22 Oct: `jdf.extra_lics` {licence: area id} reads a licence of another sheet's area into this sheet's line of the same number, whatever its operator (TFJ: 883980, 883985). `01b_plates.py` also tries a vanity plate number first (TESIN001 → "001 TESIN", the register's spelling), and `--refresh` now asks again only for the plates not found.
- 22 Oct: `lib.tlen` is the one length reader (01c for the registers, 04 for looked-up plates); 04's old copy wanted an "M" and showed SOR BN 10,5 / EBN 9,5 / CN 9,5 as 12 m.
- 06 shows "trolleybuses" for traction T lines and takes optional area keys `licences` (the intro's licence text) and `operator_short` (the "At 16:00 … had" name).

