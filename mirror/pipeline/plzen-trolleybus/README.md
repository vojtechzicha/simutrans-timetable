# Plzeň trolleybuses (PMDP)

Published at https://claude.ai/artifact/B9vVcHutYdXdg4sscpA1gR (republish to the same URL after a rebuild). Maintained by session simutrans-timetable-a2.

The Plzeň trolleybus sheet is built from stored raw data by the scripts in this folder. The shared rules are in `../README.md`. The same scripts also build the Plzeň bus sheet (`../plzen-bus`, run with `--base ../../plzen-bus`), and the raw data both sheets use is stored here once.

| State file | Network | Vehicles | Output (project root) |
|---|---|---|---|
| `states/2026-09-29.json` | Tue 29 Sep 2026 (GTFS service day 29 Sep) | Fri 18 Sep 2026 | Plzeň Trolleybus Peak Fleet.html |

```
cd pipeline/plzen-trolleybus/scripts
python run.py --state 2026-09-29
```

Python 3, standard library only. Built by session simutrans-timetable-a2 on 29 Sep 2026. Not published yet (the user reviews and publishes).

Imports, read only (never modified here):
- `../plzen/scripts/common.py` (Plzeň tram pipeline, session simutrans-timetable-3a): `fetch`, `gtfs_trips`, `cycle_need`, `runfit`, `best_offset`, `loop_shift`.
- `../brno-trolleybus/scripts/common.py`: `circuit_need`, `turnarounds`, `runfit_rate`, `mark_spares`.
- Page style: `../brno/assets/style.css.html` and `../brno-trolleybus/assets/extra.css.html`, plus `assets/extra.css.html` here.

## Sources

| What | URL | Stored in |
|---|---|---|
| Day overviews (which lines have records on which day; every car out that day) | `https://seznam-autobusu.cz/vypravenost/mhd-plzen?datum=YYYY-MM-DD` | `data/raw/vypravenost-days/<date>.html` |
| Vehicle per kurz with notes, one list per line (trolleybus and bus lines) | `https://seznam-autobusu.cz/vypravenost/mhd-plzen/vypis?datum=YYYY-MM-DD&linka=N` | `data/raw/vypravenost/<date>/L<N>.html` |
| Line history (for designed vehicles) | `…/mhd-plzen/vypis?linka=N&since=YYYY-MM-DD`, pages `&strana=N` (50 records a page, newest first) | `data/raw/history/<fetch date>/L<N>_since<date>_<page>.html` |
| PMDP register (in service): trolleybuses, buses | `https://seznam-autobusu.cz/seznam?iddopravce=71&trakce={trolejbus,autobus,elektrobus}&prov=1&vcetneSluzebnich=1&page=N` | `data/raw/register/<date>/pmdp_<trakce>_<page>.html` |
| Timetable | `https://jizdnirady.pmdp.cz/jr/gtfs` (returns the zip directly). Trolleybus `route_type` 11, bus 3, tram 0. No `shapes.txt`, no blocks. The 29 Sep download is byte-identical to the tram pipeline's 28 Sep copy. | `data/raw/gtfs/2026-09-29/gtfs.zip` |
| Overhead wire | Overpass: `way["trolley_wire"="yes"]` and `way["railway"="trolleybus_wire"]` in (49.68, 13.25, 49.80, 13.50), `out geom`; also the `route=trolleybus` relations (out of date, not used) | `data/raw/osm/2026-09-29/trolley_wire.json`, `trolleybus_routes.json` |
| Battery-capable cars, battery stretches (cross-check) | cs.wikipedia: Škoda 26Tr, Škoda 27Tr, Trolejbusová doprava v Plzni | the state (`battery_rules`, `diesel_rules`, `battery_text`) |
| Pak objects | local pak128 checkouts (`C:/Users/vojte/Developer/simutrans-custom-czech-pak128`, `-mhd`), read only: no `VZ-PMDP-trolleybus` package exists | `assets/pak_map.json`, `pak_request.md` |

- seznam-autobusu.cz: browser headers, 2 s between requests (`common.fetch` from the tram pipeline). No personal data is sent.
- Overpass answers 406 to a browser User-Agent: `01_fetch.py --osm` sends `simutrans-timetable-pipeline/1.0` and `Accept: application/json`.
- Car ids are the key everywhere: PMDP trolleybus and bus numbers overlap (559 is a Škoda 26 Tr and a SOR NB 12). One register number carries a suffix (`634<sup>II</sup>`); the parser keeps `634`.

## Steps

1. `01_fetch.py`: `--days`, `--vehicles <date> --lines …`, `--history <lines> --since <date>`, `--register trolejbus autobus`, `--operator <id> <trakce>` (another operator's register, for subcontractors), `--car <id>`, `--gtfs`, `--osm`.
2. `02_parse.py`: per-line lists → `vypravenost_<date>.json`; registers → `vehicles_<date>.json` (by car id, with type, livery, garage, operator, year, state, traction); day overviews → `day_counts.json`; histories → `history.json`.
3. `03_timetable.py --state X [--base …]`: network table, schedule fits and needs (see Decisions). Writes `<base>/data/derived/X/timetable.json`.
4. `03b_offwire.py --state X`: battery stretches per stop pattern (trolleybus only). Copied from `../praha-trolleybus/scripts/03b_offwire.py` and changed from shape sampling to a per-stop test, because the PMDP GTFS has no shapes.
5. `04_fleet.py --state X [--base …]`: afternoon vehicle per kurz, allocation to Simutrans lines, designed vehicles for shortfalls, `mark_spares`, and the battery check.
6. `04b_pak.py --state X [--base …]`: `assets/pak_map.json` and `pak_request.md`.
7. `05_render.py --state X [--base …]`: the HTML, into the project root.
8. `propose.py --route-type 11|3 --groups …` (not in `run.py`): the Brno bus helper, chaining trips FIFO to show which leg follows which. The circuits in the states come from its output.

## Decisions

- **Day.** Vehicles from Fri 18 Sep 2026. `day_counts.json`: 76–80 trolleybus and 124–130 bus records on every weekday 10–22 Sep, but 1 / 1 / 1 / 0 on 23 / 24 / 25 / 29 Sep (28 Sep was a holiday). 18 Sep is the latest complete Friday and the Plzeň tram sheet's day. Mon 21 and Tue 22 Sep are complete too (a fallback). Network: the GTFS service day Tue 29 Sep itself, because line 12 has a separate calendar from 1 Oct (every trip a minute later).
- **Lines.** Every trolleybus route with afternoon service: 10, 11, 12, 13, 14, 15, 16, 18, 22, 49. seznam-autobusu.cz files 22 and 49 among the buses, but their cars are trolleybuses and the GTFS says route_type 11. 17 (3 trips in 15–18 h), 19 (none) and N7 are left out.
- **Structure (from `propose.py`):**
  - **10** is one Simutrans line Tylova → Čechurov → Tylova → Černice (→ Tylova): the branches alternate (6 of 7, 4 of 6). Fitted every 24 per branch (`fit.overrides`, `auto` = least-deviation offset), its real pattern; approximate, ±12 min.
  - **11** is one line Ústřední hřbitov → Křimice → Ústřední hřbitov → Malesice: the branches alternate (5 of 6 each way); exact every 30.
  - **15N** (Lobzy – Nová Hospoda) is a peak branch (4 + 3 trips in 15–18 h, a 16:xx departure, no depot): its own line, taking the highest 15 kurzy (11, 12). Its need is set to 2 in the state (`need`, with the reason): the real branch trips wait almost an hour at Nová Hospoda, so the cycle gives 156 min.
  - **22** runs Malvíny → Koterov → Škoda VIII. brána in the 16:00 hour and returns empty to Malvíny (`empty_return`, 5 min, a guess): no trip leaves Škoda VIII. brána after 15:22, and Koterov → Malvíny runs only outside the 16:00 hour.
  - **12** Letkov branch (5 trips a day, none 15–18 h) and **13** Černice short workings (2) are not peak trips, not modelled.
  - Rates set in the state: 12 at 8 an hour, 13 at 5 (every 12, the real peak pattern). 22 Koterov fitted every 30 (`auto`).
- **Loop −1 everywhere** (`all_loops`), as on the other trolleybus sheets.
- **Line 18** (Škoda-shift line): three cars logged on 18 with no note also worked 10/6, 12/19 and 13/1. They are counted there (`fleet.secondary`), and their 18 records are listed under Not counted.
- **Need** = max(`circuit_need` with the timetable's own turnarounds, most on the road 16:00–16:59 per record line); the on-road rule adds one on 13, 16 and 22. Surplus logged → `mark_spares` (one of every type first; afternoon-only kurzy, then the highest kurz numbers dropped first; on a battery line a car without a battery goes first). On 18 Sep: 56 counted, 26 not needed, none short, none designed.
- **Battery sections.** A stop more than 60 m from an OSM wire is off the wire (40 m put the CAN Husova terminus and a Tylova platform off the wire; 60 m matches Wikipedia's stretches). A lone terminus platform within 200 m of the wire is a turning loop. Results: 11 CAN Husova – Malesice / Křimice, 12 Božkov – Letkov (not modelled), 13 U Staré Kovárny – NC Černice, 22 Vodárna – Koterov, 49 U Práce – Areál FN. Wikipedia also lists 22 Tyršův most – Vodárna; OSM shows wire there.
- **Battery-capable cars** (`battery_rules`): every Škoda 26 TrNU and 27 TrNU, and the Škoda 26 Tr 565–582. Auxiliary diesel (`diesel_rules`, shown but not battery): 26 Tr 551–552, 27 Tr 527–530 and 540. The check passes on 11, 13, 22 and 49.
- **Pak.** No PMDP trolleybus objects exist, so all six types are "requested" in `VZ-PMDP-trolleybus`: `VZ-PMDP-<token>-pmdpzelenobila-<core>`, articulated `<core>` + `<core>-B` (the Brno trolleybus convention). 26 Tr / 26 TrNU and 27 Tr / 27 TrNU are separate objects (Urbino III vs IV body). The request list is `pak_request.md`, for the user to send to the pak session (simutrans-custom-czech-pak128-bd). When the pak installs the objects, `04b_pak.py` finds the names in the checkout build and marks them installed.

## How to update

1. `python run.py --state 2026-09-29 --fetch`: the day overviews of the last two weeks, the per-line lists of the state's vehicle day, the registers, the GTFS and the OSM wire, all dated today. It prints records per day (`data/derived/day_counts.json`).
2. Copy the state to `states/<new>.json`. Set `vehicles_date` (the latest complete weekday, preferably a Friday), `register_date`, `gtfs_date`, `service_date`, `osm_date`. Fetch the lists of the new day: `python 01_fetch.py --vehicles <date> --lines 10 11 12 13 14 15 16 18 22 49`.
3. `python 03_timetable.py --state <new>`: check the rates, the approximate entries and `not modelled`. If a branch pattern changed, run `propose.py --route-type 11 --groups …` and update `simutrans_lines`.
4. `python run.py --state <new>`. If a line is short, `04_fleet.py` designs vehicles from `data/derived/history.json`: fetch the line history first (`01_fetch.py --history <line> --since <date>`).
5. Update the texts (`texts`, `battery_text`) for the new dates. Then do the bus sheet (`../plzen-bus/README.md`).
