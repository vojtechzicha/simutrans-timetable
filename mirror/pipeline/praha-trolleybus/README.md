# Praha (DPP trolleybuses): pipeline

Output: `Prague Trolleybus Peak Fleet.html` in the project root, published at https://claude.ai/artifact/7P7BZSczRixGop15Fd6zmX.
Built by session simutrans-timetable-5a on 29 Sep 2026. Shared rules: `../README.md`. The scripts are copies of `../praha/scripts` with these changes:

- `route_type` (11 = trolleybus) and `trakce` (trolejbus) come from the state.
- `parse_register` reads the register's depot cell (`depot_codes`), because one list covers every garage.
- `03_timetable.py` adds `fit_core` and `schedule_override`, and applies `turnaround_min` to the branch needs.
- `03b_offwire.py` is new: it finds the battery sections.
- `05_render.py` adds pak `core`/`chain`, a battery block on each card, the network table and the not-modelled list, and uses trolleybus wording.

```
python scripts/run.py --state 2026-09-27            # rebuild from stored raw data
python scripts/run.py --state <new> --fetch         # download missing raw data first (not the OSM wire: see below)
```

## Sources

| What | URL | Stored in |
|---|---|---|
| Deployment records per line and day | `https://seznam-autobusu.cz/vypravenost/pid/vypis?datum=YYYY-MM-DD&linka=N` (trolleybus rows have the class `route trolden` in the day overview) | `data/raw/vypravenost/<date>/<line>.html` |
| Coverage history of a line | `…/vypis?linka=N&since=YYYY-MM-DD` | `data/raw/vypravenost/history/<line>.html` |
| Fleet register (all garages in one list) | `https://seznam-autobusu.cz/seznam?page=1&iddopravce=106&trakce=trolejbus&prov=1&vcetneSluzebnich=1` | `data/raw/register/<date>/l_all_1.html` |
| Timetable | `https://data.pid.cz/PID_GTFS.zip`, route_type 11 (the same export as the tram sheet) | `data/raw/gtfs/<export date>/gtfs.zip` |
| Overhead wire | Overpass `way["trolley_wire"="yes"](49.94,14.22,50.18,14.71); out geom tags;` (query in the state) | `data/raw/osm/<date>/trolley_wire.json` |

seznam-autobusu.cz returns 403 to plain curl, so use `common.fetch` (full browser headers). overpass-api.de returns 406 unless the request sends `Accept: application/json`. The garage codes in the register are Klí = Klíčov, Řep = Řepy and Stře = Střešovice (museum). `01_fetch.py` does not download the OSM wire; fetch it by hand with the query in `states/*.json` → `osm.query` into a new dated folder.

## Steps (scripts/)

01_fetch → 02_parse → 03_timetable → **03b_offwire** → 04_courses → 05_render (run.py runs 02–05). Steps 02, 03, 04 and 05 work as in `../praha/README.md`.

`03b_offwire.py` samples every stop-to-stop section of each GTFS shape every 10 m. A section is off-wire when less than a third of its samples lie within 25 m of an OSM `trolley_wire=yes` way. Consecutive off-wire sections are joined into stretches named by stop. The card shows the busiest stop sequence of each direction.

## Manual decisions (state 2026-09-27)

- **Day:** as for the trams. Vehicles are from Fri 25 Sep, the network is the 27 Sep one, and the timetable is PID's for Tue 29 Sep (service date 20260929).
- **Lines:** 51, 52, 53, 58 and 59. Line 275 (Sídliště Čakovice – Náměstí Jiřího Berana, 5 trips, the last at 14:05) has no peak service and is listed as not modelled. No bus was recorded on a trolleybus line, and no trolleybus on a bus line.
- **Coverage:** courses 52/9, 59/6 and 59/14 are missing on 25 Sep; they are recorded on 24 and 29 Sep. The recorded vehicles still reach the cycle need on every line (52: 9 ≥ 8, 58: 14 = 14, 59: 15 ≥ 14, 51 and 53: 1 = 1), so no trolleybus is designed.
- **Branches** (`splits`): 52 (Na Knížecí – Jinonice needs 5, – Waltrovka needs 3) and 58 (Palmovka – Miškovice 7, – Čakovice 7). Both branches of each line run all week and the course numbers do not mark them, so the courses are assigned in course order as a stated choice. For 52 the spare 52/10 goes to the longer Jinonice branch. For 58, courses 8–14 are the weekday-only ones and go to Čakovice. A single line alternating the branches (`common.pool_need`) would need 9 for 52 and 13 for 58; the flags say so.
- **Line 51** turns in 2 min at Hradčanská in the timetable (`turnaround_min`), so it needs 1 vehicle, and 1 is recorded.
- **Fit core** (`fit_core` = 16:00–17:00 instead of the runfit default 15:30–16:30): line 58's inbound 12-minute pattern starts at 16:20. The default core picked a 40-minute pattern with 3–4 slots fitted to 4 departures. Lines 52 and 59 give identical values either way.
- **Lines 51 and 53** (`schedule_override`): one trolleybus with gaps of 44–83 min. The exact fit is only 2 departures, so an hourly pattern (`best_offset`) is given with its largest deviation in 15:00–17:59.
- **Termini** (`assets/termini.json`): all are loops, so they are set 1 min early. A trolleybus cannot reverse; in the GTFS every terminus has different arrival and departure stands. The Prague tram sheet counts block loops as loops (Březiněveská). The airport is one loop: trips end at Letiště and start at Terminál 1 (`stop_aliases`).
- **Pak:** VZ-DPPraha-trolleybus.pak, pak128 main b84c15c (read from `C:\Users\vojte\Developer\simutrans-custom-czech-pak128\build\VZ-DPPraha-trolleybus`). Every peak type has an exact object: TNS_18 (A + B), TNS_12, SNG_12T, Skoda_Solaris_24m (A + B + C) and 36Tr. The objects are waytype=road with an electric engine, so the wire does not matter in the game.
- **Display:** follows the trolleybus rules agreed on 29 Sep with the Brno (3a) and Ostrava (f5) trolleybus sessions: the tram 3-line cell, per-line battery sections, and a bus on a trolleybus line counted separately (class BUS). There is one difference. Their rule (d) keeps the real minute at a block turn, but here block turns count as loops, following the Prague tram sheet.

## How to update when the timetable changes

1. Save the new PID GTFS in `data/raw/gtfs/<export date>/gtfs.zip` (or copy it from `../praha/data/raw/gtfs`, which gets the same feed).
2. Copy `states/2026-09-27.json` to `states/<new>.json`. Set `network_date`, `gtfs.raw` and `gtfs.service_date`. For new vehicles, set `vehicle_date` (check the day overview for about 55 trolleybus courses) and `register.raw`, and run `01_fetch.py`. If the wire changed, fetch the Overpass query into `data/raw/osm/<today>/` and set `osm.raw`.
3. Review `splits` (branch sizes are printed by 03_timetable), `schedule_override`, `turnaround_min`, `flags`, `not_modelled_lines` and `assets/termini.json` for new termini.
4. `python scripts/run.py --state <new>`; compare the counts and the schedule; republish to the same artifact URL.

## Spares (29 Sep 2026)

The user's roster rule is in `../README.md` under "Roster coverage and spares". Under it, logged surplus is marked "not needed": dimmed, and left out of the counts, garages and pak totals. Each Simutrans line (a branch of 52/58, or a whole line) keeps exactly its need. It keeps one vehicle of every type first, then recorded before added, then the lowest course numbers. Result: 52/10 (SNG 12T, surplus to both 52 branches) and 59/17 (Škoda-Solaris 24m, 15 logged against 14 needed), so 38 trolleybuses are counted. The code is at the end of `scripts/04_courses.py`, with `uncertain = 'spare'` in `05_render.py`.
