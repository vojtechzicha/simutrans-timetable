# PID regional — work status (Mon 2 Nov 2026, 20:30)

Coordinator: session simutrans-timetable-4d. **Version 1 of all 13 sheets is published** (URLs in each `oblasti/<id>/lines.json`
→ `artifact_url`, in `config.index.sheets` and in the repo's `data/catalog.json`; index: `config.index.url`).

## State
| Oblast | PID lines | Simutrans lines | Buses (seen / designed) | Owner checks |
|---|---|---|---|---|
| benesovsko | 63 | 75 | 138 (137 / 1) | 0 |
| berounsko | 28 | 40 | 65 (63 / 2) | 1 (545, 825 near stops) |
| kladensko | 45 | 62 | 155 (153 / 0; 597 and 623 one bus short) | 1 (306 587 708 coverage) |
| kolinsko | 32 | 39 | 71 (69 / 2) | 2 (821 Horní Kruty, 660 Štíhlice) |
| kutnohorsko | 32 | 41 | 67 (62 / 5) | 1 (805 shorts) |
| melnicko | 34 | 45 | 108 (105 / 3) | 1 (roadside stops) |
| mladoboleslavsko | 45 | 55 | 93 (92 / 1) | 3 (near stops, 722, 737) |
| nymbursko | 31 | 37 | 68 (67 / 1) | 1 (585, 833 near stops) |
| praha-vychod | 50 | 69 | 128 (126 / 2) | 2 (411, roadside) |
| praha-zapad | 36 | 45 | 88 (83 / 5) | 0 |
| pribramsko | 58 | 81 | 127 (120 / 7) | 2 (472, coverage) |
| rakovnicko | 22 | 30 | 47 (46 / 1) | 1 (roadside) |

Settled tonight by the 2 Nov live map (checks → notes, model unchanged): 534+535 (Kolínsko), 430+436 and 433+434 (Nymbursko).
Untyped buses: 11 sheet buses have no type (the live map names none; not in the register): pak_request.md.

## Tuesday 3 Nov, morning: the branch re-check (owner on 381)
Owner, 3 Nov: "381 you haven't done the Zásmuky branch … you may have to correct everywhere." 381 fixed by the coordinator
(381 Zásmuky every 60, 3 buses; Kutnohorsko lines.json). New audit `../audit/passing_check.py` (run by `run_oblast.py`):
86 lines with ≥ 3 off-pattern trips each way at one stop (`audit-passing-2026-11-03-before.txt`). Brief: `BRANCH_BRIEF.md`.
Six Sonnet designers (two oblasts each) write `oblasti/<id>/branch-check-2026-11-03.md`; then a Fable reviewer per pair writes
`branch-review-2026-11-03.md`. When all are done: `run_oblast.py <id> --final` for each, then the Tuesday steps below (the v2
build picks up the new lines and their buses). Also changed: `04_vehicles.py` no longer puts a bus of known non-PID paint
on the grey-red object (requested instead); `paint_check_2026-11-03.md` went to the fleet desk.

## Tuesday 3 Nov
1. The poller (`01_live_poll.py 2026-11-03T20:15`, started 20:03 Mon, logs `data/raw/live/poll2.log`) and `keep_awake.py`
   (until 20:20) run. It now also records trolleybuses (route type 11) and Prague city line 232 for the Prague session.
2. Before 20:00 write a trips-free variant of `observed.py` for 51 / 53 / 232 (not in any oblast trips.json): per bus and trip
   id from `polls.jsonl` + `vehicles.jsonl`: route, course, type, first/last seen. Send it to the Prague bus session
   (simutrans-timetable-13) with the 317/318 Tuesday files (`observed.py 317 2026-11-03`, `318`), and the type of 7965 if
   Tuesday names it.
3. After 20:15: `scripts/final_build.py 20:20 2026-11-03` (04 then uses day 2: designed buses filled, day-2 types win over
   day-1 empty ones), check STILL SHORT and the "?" count, re-render, republish the 12 + index to the same URLs, bump
   `publishes` in the catalog (`catalog_pid.py urls.json "Tuesday fill-ins"`), `pnpm sync` (keep other sessions' unsynced
   sheets at HEAD), commit, push.
4. Tell the fleet desk of any type still missing after Tuesday; give the owner the change list of v1 → v2 (buses in/out).
