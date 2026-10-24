---
name: plzen-trolleybus-bus-peak-fleet
description: "Plzeň trolleybus + bus sheets (2026-09-29): pipeline/plzen-trolleybus holds scripts+raw for both; plzen-bus runs them with --base; no GTFS shapes; 40/42 pools"
metadata:
  type: project
---

"Plzeň Trolleybus Peak Fleet.html" and "Plzeň Bus Peak Fleet.html" (project root) were built on 2026-09-29 by session a2, not yet published. Vehicles Fri 18 Sep 2026 (23–25, 29 Sep have ≤ 4 records), network Tue 29 Sep (line 12 has a separate calendar from 1 Oct).

- `pipeline/plzen-trolleybus` holds all scripts and all raw data; `pipeline/plzen-bus` has only state, derived, pak map, README, and a run.py calling the trolleybus scripts with `--base`. Imports `plzen/scripts/common.py` (owned by session 3a, read only) and `brno-trolleybus/scripts/common.py`.
- PMDP GTFS: trolleybus route_type 11, no shapes.txt, no blocks. Battery sections = per-stop test against OSM trolley_wire (60 m). Overpass rejects a browser UA (406); a plain tool UA works.
- seznam-autobusu files trolleybus lines 22 and 49 as buses; car ids are the key (trolleybus and bus numbers overlap).
- Bus pools: 40 is logged under 33 kurzy since Sep (33+40 loop, two Simutrans lines); 42 never logged, taken on 26 kurzy (inferred, marked not confirmed).
- No VZ-PMDP-trolleybus / VZ-PMDP-bus objects exist: all requested via each pipeline's pak_request.md.

Related: [[plzen-tram-peak-fleet]], [[brno-bus-peak-fleet]], [[prague-trolleybus-peak-fleet]]
