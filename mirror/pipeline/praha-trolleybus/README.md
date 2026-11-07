# Praha (DPP trolleybuses): pipeline

Output: `Prague Trolleybus Peak Fleet.html` in the project root, published at https://claude.ai/artifact/7P7BZSczRixGop15Fd6zmX.
Built by session simutrans-timetable-5a on 29 Sep 2026. Shared rules: `../README.md`. The scripts are copies of `../praha/scripts` with these changes:

- `route_type` (11 = trolleybus) and `trakce` (trolejbus) come from the state.
- `parse_register` reads the register's depot cell (`depot_codes`), because one list covers every garage.
- `03_timetable.py` adds `fit_core` and `schedule_override`, and applies `turnaround_min` to the branch needs.
- `03b_offwire.py` is new: it finds the battery sections.
- `05_render.py` adds pak `core`/`chain`, a battery block on each card, the network table and the not-modelled list, and uses trolleybus wording.

```
python scripts/run.py --state 2026-11-02            # the published sheet (51 and 53 on the 2 Nov network)
python scripts/run.py --state 2026-09-27            # the 29 Sep sheet (writes the same file name)
python scripts/01b_live.py --state 2026-11-02       # re-extract the live-map trolleybuses from pipeline/pid-regional (not run by run.py)
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

## Method check 25 Oct 2026

All 14 rows checked against the trips (`../praha/method-check-2026-10-25.md`); nothing changed. Both ends of every line run at one rate; 52's branches alternate 4 min apart at Na Knížecí. For the owner to decide: 51 fits exactly at every 120 with 2 slots (Hradčanská real 92 and 44, i.e. 15:32, 16:44, 17:32: Offset 31, Also at 103; Bořislavka real 72 and 24, i.e. 15:12, 16:24, 17:12: Offset 11, Also at 83; loop −1 and the 01:00 origin included), against the hourly approximation (up to 16 min off) on the sheet.

## State 2026-11-02 (published 7 Nov 2026): lines 51 and 53 on the 2 Nov network

From Mon 2 Nov 2026 04:00 (PID "Posílení trolejbusů v Praze", permanent) every trip of bus 131 runs as trolleybus 51 and every trip of
bus 176 as trolleybus 53. The bus sheet dropped 131/176 the same day (v18). Owner, 2 Nov: "You're okay for changed lines to move to 2 Nov
network, do not move vehicles in lines not affected if possible".

- **Timetable** (`gtfs_lines_from`): 51 and 53 from the PID export of 2 Nov (`data/raw/gtfs/2026-11-02`, copied from praha-bus), Wed 4 Nov.
  52, 58 and 59 stay on the 28 Sep export; their cards and the Klíčov garage are byte-identical to the 29 Sep publish (checked).
  `03_timetable.py` and `03b_offwire.py` read the listed lines from the later feed. 51: every 6 min, 8 needed by round trip
  (3 min turnaround; the old 2-min `turnaround_min` was for the one-trolleybus line and is gone, as are both `schedule_override`s).
  53: every 15 min with two slots (:02/:09 and :00/:08 real), 6 needed.
- **232** is route type 11 in the 2 Nov export, but buses run it (live map 3 Nov: SOR NB 12 3678). Listed as not modelled; it stays on
  the bus sheet.
- **Vehicles** (`observed_lines`, `04_courses.py`): seznam-autobusu.cz refuses scripted requests since 1 Nov, so 51 and 53 drop their
  25 Sep records and take a hand-picked list from the PID live map. The PID regional session polled the map on Mon 2 Nov (20:00–23:50)
  and all of Tue 3 Nov; `scripts/01b_live.py` extracts the trolleybuses into `data/raw/live/<day>/trolleybus.json` (the map has no
  history, so these are the only copies besides pid-regional's). The map drops vehicles for long stretches (509 in 11 of 180 peak polls)
  and showed 53 poorly (58 of 230 trips), so "not seen" is not "not running".
  The fleet rotates daily between 51, 52 and 53, and the published 52 card holds most of the SNG 12Ts the map showed on 51/53. 52 keeps
  them (owner's rule). Order of picks: the map's cars on the line that the 52 card doesn't have → the car the line already has in the game
  (511 on 51, 512 on 53) → free SNG 12Ts seen in service that week (53: 542, 543, 544, marked designed).
  51 = 511, 509, 514, 515, 516, 518, 533, 513. 53 = 530, 512, 537, 542, 543, 544. 534/536 (51) and 527/529/531/538/539/540 (53) stay on 52.
- **Register**: cars 515–526 and 541–544 were delivered after the 29 Sep register; the ones used are in `vehicle_overrides` with the
  live map's type (516 and 518: no type on the map, taken as SNG 12T like every typed car of the 515–544 series).
- **Pak**: pak128 main c6f4b44. 509 (purple "90 let trolejbusů") runs 51/2 and uses `VZ-DPPraha-36Tr-fialova-36Tr`; 36Tr is now a
  two-livery type, so its core names the livery.
- **Page text** (`page_replace` in the state, applied by `05_render.py`): the lede and "How this was built" say which lines are on
  which day, so `assets/page.html` still renders the 29 Sep state unchanged.

## 52 two lines, 58 one line (published 7 Nov 2026, v8)

Owner, 7 Nov 2026: "you say 52 has two branches, courses show three, timetable say one, I am dissapointed. Study buses", then, after v7
had made both lines one line each, "if it needs more, keep it as two lines - just it was not clear. If two lines, look how buses do it.
Decide again". The PID live map of Tue 3 Nov gives every trolleybus's trips (trip id → GTFS ends): every 52 trolleybus alternates
Waltrovka and Jinonice, and the 58 trolleybuses run both Miškovice and Čakovice (most switch during the afternoon, 102 and 104 stay on one).
The rule now: one Simutrans line over both branches only where it needs fewer trolleybuses than one line per branch.
- 58: one line (state `circuits`, `03_timetable.py` sizes it with `common.pool_need`: one trolleybus round the four legs, 3 min at each
  terminus): 13 against 7 + 7; 58/14 (110) not needed.
- 52: two lines, 52A Na Knížecí – Jinonice (5) and 52B Na Knížecí – Waltrovka (3), as on 29 Sep (`splits`, with `short` labels); one line
  would need 9. Courses split in course order, a choice; 52/10 not needed.
- Two-line cards are laid out like the bus sheet's: a "2 Simutrans lines" box up front, a heading row per line in the schedule
  (`tr.slh`, CSS in `assets/page.html`) and over its vehicles, and the not-needed ones once at the bottom (the spare 52/10 had printed a
  third branch heading).

## How to update when the timetable changes

1. Save the new PID GTFS in `data/raw/gtfs/<export date>/gtfs.zip` (or copy it from `../praha/data/raw/gtfs`, which gets the same feed).
2. Copy the latest state (`states/2026-11-02.json`) to `states/<new>.json` (drop `gtfs_lines_from`, `observed_lines` and `page_replace` once every line is on the new day). Set `network_date`, `gtfs.raw` and `gtfs.service_date`. For new vehicles, set `vehicle_date` (check the day overview for about 55 trolleybus courses) and `register.raw`, and run `01_fetch.py`. If the wire changed, fetch the Overpass query into `data/raw/osm/<today>/` and set `osm.raw`.
3. Review `splits` (branch sizes are printed by 03_timetable), `schedule_override`, `turnaround_min`, `flags`, `not_modelled_lines` and `assets/termini.json` for new termini.
4. `python scripts/run.py --state <new>`; compare the counts and the schedule; republish to the same artifact URL.

## Spares (29 Sep 2026)

The user's roster rule is in `../README.md` under "Roster coverage and spares". Under it, logged surplus is marked "not needed": dimmed, and left out of the counts, garages and pak totals. Each Simutrans line (a branch of 52/58, or a whole line) keeps exactly its need. It keeps one vehicle of every type first, then recorded before added, then the lowest course numbers. Result: 52/10 (SNG 12T, surplus to both 52 branches) and 59/17 (Škoda-Solaris 24m, 15 logged against 14 needed), so 38 trolleybuses are counted. The code is at the end of `scripts/04_courses.py`, with `uncertain = 'spare'` in `05_render.py`.
