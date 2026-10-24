---
name: city-pipelines
description: City tram sheets are rebuilt from pipeline/<city>/ in the project folder; read the READMEs there before any timetable update
metadata:
  node_type: memory
  type: project
  originSessionId: 4aeb8def-dec3-4568-afbf-a2ae309db52e
  modified: 2026-09-28T17:21:51.762Z
---

Since 2026-09-28 every city tram sheet has a reproducible pipeline in the project folder `pipeline/`. The shared rules are in `pipeline/README.md`; each city has `README.md`, states or config, stdlib-only `scripts/` with `run.py`, `data/raw` snapshots and `data/derived`.

| City | Folder | Session |
|---|---|---|
| Brno, Plzeň | `pipeline/brno`, `pipeline/plzen` | this session |
| Praha, Olomouc | `pipeline/praha`, `pipeline/olomouc` | simutrans-timetable-9e |
| Ostrava, Most–Litvínov | `pipeline/ostrava`, `pipeline/most-litvinov` | simutrans-timetable-10 |
| Praha trolleybuses | `pipeline/praha-trolleybus` | simutrans-timetable-5a |
| Praha buses (game check) | `pipeline/praha-bus` | simutrans-timetable-5a |

**Why:** the user asked for the method and data to be stored in the folder, not in memory or scratchpad, so they can say "the timetable changed, update" later.

**How to apply:**
- On an update request, follow the "How to update" recipe in the city README: fetch new raw data, copy the state file, run, compare, then re-publish to the same artifact URL.
- Use trams-needed by timetable cycle (`common.cycle_need`), not trip chaining, which miscounts around depots.

Related: [[brno-tram-peak-fleet]], [[plzen-tram-peak-fleet]], [[simutrans-fork-schedule-spec]]
