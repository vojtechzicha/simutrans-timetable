# Praha (DPP trams): pipeline

Output: `Prague Tram Peak Fleet.html` in the project root, published at https://claude.ai/artifact/5Dt65EJ7F8YJnMbJugLGTi.
Maintained by session simutrans-timetable-9e. Shared rules: `../README.md`.

```
python scripts/run.py --state 2026-09-27            # rebuild from stored raw data
python scripts/run.py --state <new> --fetch         # download missing raw data first
```

## Sources

| What | URL | Stored in |
|---|---|---|
| Deployment records (vypravenost) per line and day | `https://seznam-autobusu.cz/vypravenost/pid/vypis?datum=YYYY-MM-DD&linka=N` | `data/raw/vypravenost/<date>/<line>.html` |
| Day overview (all lines) | `https://seznam-autobusu.cz/vypravenost/pid?datum=YYYY-MM-DD` | `data/raw/vypravenost/<date>/overview.html` |
| Coverage history of a line | `…/vypis?linka=N&since=YYYY-MM-DD` | `data/raw/vypravenost/history/<line>.html` |
| Fleet register per depot (type, paint, depot) | `https://seznam-autobusu.cz/seznam?page=N&iddopravce=106&trakce=tramvaj&depotId=<id>&prov=1&vcetneSluzebnich=1&onlyCurrentDepot=1` (100 per page; `page=`, not `strana=`) | `data/raw/register/<date>/l_<depot>_<page>.html` |
| Timetable | `https://data.pid.cz/PID_GTFS.zip` (ROPID; covers only about two weeks from its export date, so keep each export) | `data/raw/gtfs/<export date>/gtfs.zip` |

seznam-autobusu.cz needs no special headers; keep about 1 s between requests. Depot IDs: Hloubětín 904, Kobylisy 1227, Motol 905,
Pankrác 1314, Strašnice 1360, Střešovice 1867 (museum), Vokovice 907, Žižkov 1342. PID GTFS has no block_id or course numbers,
so courses come only from the deployment records.

## Steps (scripts/)

1. `01_fetch.py`: downloads what the state needs (missing files only).
2. `02_parse.py`: records → `data/derived/records_<date>.json`, line history → `history.json`, register → `vehicles_<date>.json` (type, paint, depot, state).
3. `03_timetable.py` (runs before the courses step, because the designed trams and the branch sizes need its counts): GTFS service date → routes (headway, runtime), Simutrans schedule per terminus (shared fit rule via `common.runfit`, loop −1 via `assets/termini.json`), not-modelled depot runs and short workings, and trams needed at 16:00 (`cycle_need` = runtime both ways + median turnaround at both ends, / headway; `chain16` = FIFO chaining, which overcounts where layovers are long) → `data/derived/<state>/timetable.json`.
4. `04_courses.py`: per course, the afternoon vehicle (split / swap / transfer rules in the script docstring), pools, transfers, `added_courses`, designed courses for `fill_to_cycle` lines, and branch labels for `splits` → `data/derived/<state>/courses.json`.
5. `05_render.py`: HTML from `assets/page.html`, `assets/types.json` (names, lengths, classes) and `assets/pak_map.json` (car type + paint → pak object).

## Assets

- `assets/termini.json`: terminus kind for the loop rule, from the Prague Tram Termini sheet with overrides: Hotel Golf and Nad Džbánem are loops; Bílá labuť (street stop after the Těšnov loop), Nádraží Holešovice (line-number change, no loop), Libuš and Pankrác (stubs) and Zvonařka (triangle) keep the timetable minute. Watch the word "no loop" when adding termini (it was once matched as a loop by mistake).
- `assets/pak_map.json`: first matching rule wins; `exact: false` marks a stand-in with its reason. Confirmed with the pak128 session (simutrans-custom-czech-pak128-77), pak128 main 340c936. `livery_words`, `multi_livery_types` and `carunits` drive the core names and the pak table.
- `assets/types.json`: full names, car lengths and the colour/summary classes.

## Manual decisions (state 2026-09-27)

- **Day:** the user chose Fri 25 Sep for vehicles (yesterday, Sun 27 Sep, has no peak and thin records) on the 27 Sep network.
- **Pools and moves:** lines 5 and 6 are one pool, recorded as line 5 (they run through each other at Nádraží Holešovice); 19 of 25 courses say "přejezd na linku 6". Course 22/42 "přejezd na linku 7" is shown on line 7 (the move time isn't recorded).
- **Swaps** (1/8, 3/13, 5/10, 11/13, 17/8, 20/17, 22/1, 22/3): all vehicles shown in order; the last one counts. 9328 ran 20/17 before 1/8. Courses 18/6 and 26/9 are "not counted", because their sets later replaced cars on 11/13 and 22/3.
- **Long line 2** (user: "prepare for the to-be network with long 2 and switched 23"): 25 Sep had courses 1–10 (short route); long-route days 9–11 Sep had 1–12. Added 2/11 = 8779 + 8442 (ran it on 11 Sep, free on 25 Sep); 2/12 = stand-in 9229 (Pankrác 15T3, free on 25 Sep; the cars that usually run 2/12 were busy).
- **Line 23:** already on the switched route on 25 Sep with its usual 4 courses: no change.
- **Designed trams** (user: "if real data do not have enough trams, design the additions yourself"; verified by the Brno session): the need per line is `cycle_need` from pipeline/brno (follow a tram round the line, taking the first departure at least `lay` min after each arrival; worst of both directions). `lay` is 3 by default; `turnaround_min` in the state lowers it where the timetable itself turns trams faster (31: 1 min at Vysočanská). `fill_to_cycle` adds designed courses up to the need, using cars from the line's history that were in service and not used anywhere on the vehicle day: 13/2–4 (8786, 8787, 8765) and 31/4–5 (8276, 8284). Every designed tram is marked "designed, not recorded", with its source dates.
- **Splits** (`splits` in the state; verified by the Brno session): 17 by course range (17/1–17 are bidirectional KT8D5.RN2P for the Libuš stub; 17/21–37 are single-direction sets for Vozovna Kobylisy – Levského), 15 needed on each branch. 22 has no range: both branches need 17, and the 40 courses are split evenly as a stated choice (1–17, 35–37 / 18–34, 41, 43, 44). Chaining shows no tram switching between the 22 branches, so they are two separate Simutrans lines.
- **Shared pool 5 + 6** (user: "shared tram pools are OKAY (and preferred for 5/6), just need to be marked throughout the document and timings must be designed for it"): one Simutrans line over the circulation Slivenec → Nádraží Holešovice → Kubánské náměstí → Nádraží Holešovice → Slivenec (`pools.5/6.simutrans.legs`). Sized by `pool_need` (the same method round the whole circulation): 24 needed, 25 recorded. It is a modelling choice: in reality 19 of 25 courses run through. Nádraží Holešovice keeps the real minute (through stop).
- **Short workings**: a short working is its own Simutrans line only if it has at least 3 trips in 15:00–17:59, no depot at either end, runs in the 16:00 hour, and runs alongside the main pattern rather than replacing it after the peak (shared rule). The user ruled on 28 Sep that 3 from Nádraží Braník (end of its midday branch, last 15:38), 9 from Hotel Golf (last 15:45) and 22 from Nad Džbánem (last 15:47) are not peak trips, so they are listed as not modelled.
- **Pak:** 14T "stříbrno-červená" = the pak's silver-red-black (exact); advert wraps get the nearest standard livery (≈); line-42 pre-war sets use Trabuko + Trabuko_vlek (≈).

## Change state 2026-10-12 (closure Nákladové nádraží Žižkov – Ohrada, 11 Oct – 18 Dec 2026)

User, 13 Oct: "regenerate the file, but be smart with the changes – I'll be redoing it in game, so reduce the workload. Mark which routes changed and how, the new lines in full; if a line only changed, mark which trams must change; the non-changed under the line, not primary visible."

- `python scripts/run.py --state 2026-10-12` (run.py swaps `04_courses.py` for `04b_rebase.py` when the state has a `changes` block). The template is `assets/page_changes.html` (made from `page.html`; keep both in step). `--state 2026-09-27` still rebuilds the old sheet unchanged.
- **Timetable:** GTFS export 2026-10-13, service date 20261020 (inside the long closure, after the short Na Knížecí – Smíchovské nádraží closure of 3–18 Oct, which is short-term and so stays regular).
- **No re-roster.** `04b_rebase.py` takes the 27 Sep courses (the trams already in the game) and applies only `changes.moves` / `changes.withdraw` / `changes.group_map`. Moves were chosen as the minimum (24 moves + 3 to the depot), matched by type and depot to the Mon 12 Oct records (`data/raw/vypravenost/2026-10-12`, lines 7, 9, 11, 26, 30, 37; 9/10 are recorded together as 9).
- **9/10:** GTFS block pairs show every 9 arriving at Nákladové nádraží Žižkov leaving as 10 in the same minute and vice versa, so two circles (`pools` 9/10 and 10/9, 25 trams each, cycle 97–98 min at 4 min). The old Simutrans lines 9 and 10 become the two circles and keep their trams; 8 T3 pairs leave 9 (to 30), 7 Motol 15T from 16 join 10. Nákladové nádraží Žižkov is `through` in `assets/termini.json`. `schedule_overrides` sets 9 from Sídliště Řepy to every 4 (the :09/:29/:49 slots start at Hotel Golf, pull-outs) and drops the Hotel Golf short workings of 9 and 10 as not modelled.
- **26** is listed as changed although not in this closure: the 27 Sep sheet had it on the diversion of the Olšanské náměstí – NNŽ closure (ended 10 Oct); now it is back via Olšanská – NNŽ – Mezi Hřbitovy, need 20 → 19.
- **Small edits:** new stop Hodkovičky on 3, 17, 20; 23 from Královka 1 min earlier. Route-order-only differences (13, 18, 31) count as unchanged.
- **Verification:** not yet sent to the Brno session.
- **NAD (user, 13 Oct: "add the NAD, if any, at the bottom, similar style to buses"):** `03c_nad.py` (state block `nad`) builds bus-sheet-style cards for the daytime tram replacement lines X9 (new, this closure) and X25 (Libeňský most, long-term, already on 29 Sep). It imports `pipeline/praha-bus` (its common.py and 04_courses.py) for the register, liveries, pak objects and the bus need rule (max of round trip and buses on the road, termini −1 min). Vehicles: records of Mon 12 Oct (`data/raw/vypravenost/2026-10-12/X9.html`, `X25.html`; 13 Oct as fill-in), surplus marked “not needed”. Night X lines and the short Smíchov closure's X12 are listed as not modelled.

## Metro summary

The state's `metro` block adds one summary table at the bottom (user, 28 Sep: "Prague needs also a metro mention. I need intervals, lines and number of trains"). It comes from the same GTFS (route_type 1): per line and pattern, the departures in the 16:00 hour (interval and trains per hour), the median runtime, and trains needed per branch by `cycle_need` for a reversing time of 3–5 min (`metro.reverse_min`; all metro termini reverse behind the station and the timetable does not show that time: arrival and next departure there are different trains) (line A = Depo Hostivař branch + Skalka branch). Patterns with under 30 % of the main pattern's trips (e.g. C to and from the Kačerov depot) are not counted. "Recorded" = metro courses entered on seznam-autobusu.cz for the vehicle day (the overview's `vlakden` rows), which are incomplete. Each branch is one row (line A: Depo Hostivař and Skalka separately, each with its own train count; user, 28 Sep). The Simutrans values (Departure every / Offset / Also at) are given for both directions: the shared `runfit` when its exact run covers the 16:00 hour (starting by 16:05 at the latest), otherwise an approximate pattern that keeps the real trains per hour (interval 4, 5, 6, 8, 10, 12, 15, 20, 30 or 60 min, the same set runfit uses; up to 8 slots, the 16:00-hour departures modulo the interval), labelled with its largest deviation. Metro termini reverse on stub tracks, so there is no loop shift. Train types are given in `metro.stock`. Calibration tried on 28 Sep (Brno's suggestion): cs.wikipedia "Metro v Praze" only gives a network total, "V ranní špičce se vypravuje 89 souprav" (morning peak, undated). That is below even the 3-minute total of 93 (24 + 36 + 33), so it looks out of date and gives no per-line figure. The 3–5 min range stays until a per-line peak count is published.


## Ferries summary

Added 29 Sep 2026 by session simutrans-timetable-5a. The user asked: "Keep the separate files bus only, add ferries to the tram/metro one". The state's `ferry` block adds a table after the metro one. It uses the same GTFS and service date, route_type 4, lines P1, P2, P4, P5 and P6.

Each direction gets one row, showing:
- the interval in 16:00–16:59,
- the median crossing time,
- the first and last departure,
- the Simutrans values from the shared `runfit` (core 16:00–17:00).

Piers are stub termini, because the boat reverses, so there is no loop shift.

Boats needed is `cycle_need` with `ferry.turn_min` = 0. The timetable turns the boat round in the minute it lands (P4: Dostihová 16:00 → Belárie 16:02, back 16:02), so every line needs 1 boat. Operators come from `route_sub_agencies.txt`: Pražské Benátky, and Pražská paroplavební společnost on P4.

`ferry.boats` holds the boat and pak object from the VZ pak session (VZ-Praha-water):
- P1 / P5 / P6: Naomi class (Břehule, Břehouš, Ledňáček)
- P2: Kazi class (Baba)
- P4: Holka 2

Each is marked "(requested)" until the object is in the pak build. seznam-autobusu.cz has no ferry records.

## How to update when the timetable changes

1. Download the new GTFS into `data/raw/gtfs/<export date>/gtfs.zip` (or set `gtfs.raw` to the new date and run `01_fetch.py`).
2. Copy `states/2026-09-27.json` to `states/<new date>.json`. Set `network_date`, `gtfs.raw` and `gtfs.service_date` (a normal weekday on the new network). If the vehicles should follow, set `vehicle_date` to the last weekday with good records (check the day overview: about 500 tram courses on a complete weekday) and `register.raw` to today, and run with `--fetch`.
3. Review the manual parts of the state: `pools`, `transfers`, `added_courses` (only for routes the vehicle day did not run), `fill_to_cycle`, `flags` (texts on the line cards), `course_notes`, `stop_aliases` for new loops, and new termini in `assets/termini.json`.
4. `python scripts/run.py --state <new date>`; check the printed counts and the schedule table; republish to the same artifact URL.

## Not needed (29 Sep 2026, session simutrans-timetable-5a)

Under the user's roster rule (`../README.md`, "Roster coverage and spares"), logged units beyond each Simutrans line's need at 16:00 are marked `uncertain = 'spare'`. A Simutrans line here is a line, a branch of `splits`, or a pool. The kept units cover every type on the line first (most frequent first), then recorded before added or designed, then the lowest course numbers. The spares are dimmed, and left out of counts, depots and pak totals. The code is at the end of `scripts/04_courses.py`, with the `'spare'` handling in `05_render.py`. Result on the 27 Sep state: 47 not needed, 380 counted. That includes 2/12, the designed Pankrác 15T: line 2 needs 11.
