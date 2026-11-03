# PID regional buses: one sheet per oblast (okres) + "PID: all lines"

Owner, 1 Nov 2026: "Do the full PID. Divide it per "oblast" (like Mladoboleslavsko), all PID lines should be in. Then use Fable
and/or subagents to comb line by line, look at my usual notes (there seems to be lot of them usually) and make sure it is
polished." Built by session simutrans-timetable-4d (1–3 Nov 2026) with one designer subagent per oblast and an independent
line-by-line reviewer (Fable) per oblast.

Outputs (working folder root): `PID <Oblast>.html` × 12 (Benešovsko, Berounsko, Kladensko, Kolínsko, Kutnohorsko, Mělnicko,
Mladoboleslavsko, Nymbursko, Praha-východ, Praha-západ, Příbramsko, Rakovnicko) and `PID All Lines.html`. Artifact URLs are in
each `oblasti/<id>/lines.json` → `artifact_url` and in the repo's `data/catalog.json`.

## Scope and the division into oblasti
- **Every bus route of the PID GTFS** (`data/derived/lines.json`) is placed: a regional line on exactly one oblast sheet; the
  Prague city lines 100–299 are the Prague bus sheet's; night lines, replacement buses (X…), PID Haló on-demand lines, the
  airport express and shopping shuttles are listed with the reason on the index. Trams, metro, ferries, trolleybuses and
  trains are listed on the index with the sheet they are on (or "no sheet yet").
- **Oblast = okres.** The Středočeský kraj licenses each district's lines with its own prefix (first two digits of the
  six-digit licence): 20 Benešov, 21 Beroun, 22 Kladno, 23 Kolín, 24 Kutná Hora, 25 Mělník, 26 Mladá Boleslav, 27 Nymburk,
  28 Praha-východ, 29 Praha-západ, 30 Příbram, 31 Rakovník (third digits are sub-areas and town networks: 205 MHD Benešov,
  235 MHD Kolín, 289 MHD Říčany, 305 MHD Příbram, 287/297 …).
- **Lines licensed by Prague (100xxx–104xxx)** go to the okres of their **outer end**: from the end farthest from the centre
  of Prague (over the trips that reach Prague), the first stop in a Středočeský municipality. **Lines licensed by another
  kraj** (Tábor, Pelhřimov, Liberec, Jičín …) and lines with no Prague end go to the okres most of their Středočeský stops lie
  in. Each card says why its line is on that sheet.
- **A stop's okres** (`02_gtfs.py`): the municipality lists of cs.wikipedia ("Kategorie:Obce v okrese X", 12 lists in
  `data/raw/obce/<date>/`), matched on the GTFS town (abbreviations as word prefixes: "Brandýs n.L.-St.Bol."); only stops with
  GTFS `zone_region_type` 2 (Středočeský kraj) — Doksy, Slatina, Vrbice, Lety of other kraje share names with Středočeský
  municipalities; a name several okresy have (Lhota, Roztoky) goes by the district lines serving the place, else the okres
  whose uniquely named places are nearest. Places of one name more than 4 km apart are different places and get the save's
  style of tag ("Chrášťany [RA]", "Dalovice [MB]"). OSM boundaries were tried first; Overpass timed out.
- **The 13 regional companions on the Prague bus sheet** (301, 352, 396, 329, 312, 364, 366, 333, 318, 363, 325, 376, 378;
  read from `praha-bus/states/2026-09-29.json` → `regional`) are listed on their oblast's sheet with a link, not repeated.

## Sources
| What | Where | Stored in |
|---|---|---|
| Timetable | PID GTFS `https://data.pid.cz/PID_GTFS.zip`, downloaded Sun 1 Nov 2026 (feed 1–14 Nov); service day **Mon 2 Nov 2026** (a school weekday: 28 Oct was a holiday and 29–30 Oct autumn school holidays) | `data/raw/gtfs/2026-11-01/gtfs.zip` |
| Vehicles | PID live map `mapa.pid.cz` (getData.php every minute 12:00–20:00, every 3 min 5:00–12:00 and 20:00–23:00; getVehicleWindow.php once per bus and line: operator, type, course "#9513 na 737/64", seznam-autobusu car id), **Mon 2 and Tue 3 Nov 2026** | `data/raw/live/<date>/polls.jsonl`, `vehicles.jsonl` |
| Paint of a bus | praha-bus register pages of 29 Sep (ARRIVA City/Střední Čechy, ČSAD Střední Čechy/Benešov/Polkost, Martin Uher, Umbrella, …), joined by the car id | `../praha-bus/data/derived/vehicles_2026-09-29.json` |
| Save game | export of FORK-CZR-VZ.sve of 30 Oct 2026 (engine session), lines 100300–100960 | `../praha-bus/data/raw/game/2026-10-30-regional/lines.json` |
| Okres of a municipality | cs.wikipedia category lists | `data/raw/obce/2026-11-01/` |
| Pak objects | `simutrans-custom-czech-pak128/build/`: `VZ-Praha-bus` and `VZ-DPPraha-bus` (regional PID buses use these objects as they are), `VZ-PID-bus` (combinations those lack), the town packs `VZ-MHDBenesov-bus`, `VZ-MHDKolin-bus`, `VZ-MHDPribram-bus`, `VZ-MHDRicany-bus` (only the town's own paint) and the neighbouring regions' `VZ-DUK-bus`, `VZ-IDOL-bus`, `VZ-JIKORD-bus`, `VZ-IREDO-bus`; the exact basenames the fleet desk named are in `config.pak.objects` / `by_vehicle` | read on each run |

The owner first asked to pool the seznam-autobusu.cz records of every working day of Sep–Oct ("Use more than a sample day -
working day assumption holds from September to November"). Since 1 Nov 2026 that site answers every scripted request with a
JavaScript browser check (Websupport) that also fails in an automated Chrome tab; the pipeline does not try to get round it.
The PID live map observes every bus on every line instead, on two working days.

## Steps (`scripts/`, stdlib Python, run with `-X utf8` from the pipeline folder or here)
| Script | Does |
|---|---|
| `01_live_poll.py <until>` | The live-map poller (start detached; asks Windows not to sleep). `keep_awake.py <until>` is a second guard that also keeps the display on (Modern Standby). |
| `02_gtfs.py` | GTFS → `data/derived/lines.json` (every route, oblast and why), `ends.json`, `city_stops.json`, `stop_okres.json`, `stop_lines.json`; per oblast `oblasti/<id>/data/derived/trips.json`, `line_class.json`, `versions.json` in the ODIS regional schema. **Do not run while designers work** (it rewrites every trips.json). |
| `00_config.py <id> [--final]` | `oblasti/<id>/lines.json` (the hand design) + shared settings → `oblasti/<id>/config.json` for the ODIS scripts. `--final` adds every sibling sheet's coverage (only when no designer is running). |
| `03_read.py <id>` | The whole-day reading per line (`reading/<L>.txt`): core points, paths in full names, every trip at the core points, the stops only this line serves, the 0–5 min chain test at the ends, and (after the poll) each bus seen and the afternoon bus chains. |
| `run_oblast.py <id> [--draft] [--final]` | 00 → 03 → (`odis-regional-hko/scripts/03b_draft.py`) → `odis-regional-hko/scripts/05_schedule.py --base pid-regional/oblasti/<id>` → audits (`../audit/step4_regional.py`, `branch_check.py`, `path_check.py`, `passing_check.py` with `AUDIT_SHEETS`), coverage split by okres, slots with no real trip. |
| `04_vehicles.py` | All oblasts at once: the buses of every Simutrans line from the live map by augmenting-path matching (one bus, one line, one sheet), starting from the published roster (`roster_published.json`, keep_roster), designed buses with reasons, pak objects (`config.pak.rules`, `by_vehicle`, `paint_by_vehicle`; a known non-PID paint is requested, never grey-red). |
| `05b_game.py <id>` | The save's lines against the sheet (missing / extra stops, buses, name fixes; "a line to build"). |
| `06_render.py <id>` | The sheet. `07_index.py`: "PID All Lines". `observed.py <line> <date>`: one line's trips with the buses seen (for the Prague session's 317/318). |

The schedule method is `../bus-schedule-method.md` (v4) in full: every PID regional line is a regional line, and the town
networks (MHD Benešov, Kolín, Příbram, Říčany, Vlašim, Beroun) are small towns. Designers work from `DESIGN_BRIEF.md`,
reviewers from `REVIEW_BRIEF.md`; each oblast keeps `method-check-2026-11-01.md` and `review-2026-11-01.md`. The 3 Nov
branch re-check (`BRANCH_BRIEF.md`) added `branch-check-2026-11-03.md` (designer) and `branch-review-2026-11-03.md` (reviewer)
per oblast, and `audit-passing-2026-11-03-before.txt` / `-after.txt` for the whole sheet set.

## Decisions
- **Owner, 2 Nov 2026 — "Yes, serve every place":** a stop no other modelled line serves gets a Simutrans line (at most
  every 480), also outside the Středočeský kraj (asked on 571 Rakovník – Slatina – Chříč, Plzeňský kraj).
- **Owner, 1 Nov 2026 — "I will swap them all, no issue":** the save's 500 regional lines carry 795 buses; the sheets assign
  buses from the live map and show the save's line only as a check (stops, buses, timetable), not rebased on it.
- **Owner, 2 Nov 2026 — PID Haló: "Yes, model a line":** villages whose only afternoon service is the on-demand PID Haló get
  a Simutrans line from their fixed trips (Benešovsko: folded into 848 Zdiměřice's round; Kolínsko: 889 Chotutice).
- **Bus replacement lines are modelled as they run** (X384, X390, X391): they run for months (X390, the Slapy dam closure,
  2 Mar 2026 – 31 Dec 2027; all were in the 29 Sep and the 1 Nov feeds); long works are modelled as run (shared rule). Rail
  replacement buses (XS…/XR…) stay listed: the rail sheets model the trains.
- **0-minute real turns** keep their real slots, with `lay: 0` on the departing leg (tested: 573 needs 1 bus, not 2). This
  assumes the fork's automatic "Leave up to" (half the gap) lets a bus arriving on the real minute leave although the loop
  rule typed the departure 1 min early; to confirm with an engine session.
- **owner_checks only for real choices** (the pilot's 13 were cut to 1 by the review: outstation rate, no empty returns,
  exact beats approximate, only-service lines, Step 5b and pooling are decided by the rules).
- **Owner, 3 Nov 2026 — "381 you haven't done the Zásmuky branch":** branches are read where the trips pass, never by trip
  ends; ≥ 3 each way 13:00–19:00 at a repeating minute is a line of its own; the outstation rule applies only to what is
  left. Re-check of all twelve sheets: 14 new Simutrans lines (381 Zásmuky, 865 Pacov, 631 u lípy, 342 Knovíz, 365 Unhošť,
  389 Chomutov, 306 Jeneč, 857 Minice, 466 Nelahozeves, 767 Krpy, 716 Sychrov, 390 Štěchovice, 340 Masarykova, 415 Žatec),
  6 changed (382 :50 → :20, 361 every 120 → 60, 369 second slot, 466 town end, 340 split, 659 path), 1155 → 1184 buses.
- **Republish keeps the published buses** (keep_roster; owner on the Prague sheet, 2 Nov: "do not move vehicles in lines not
  affected if possible"): copy `roster.json` → `roster_published.json` after each publish.
- **Pooling options go on the cards, never on owner_checks** (307, 631 + 649, 365, 389, 865 are named there
  with the buses seen doing it).
- Pilot lessons (Rakovnicko, 1–2 Nov) are in `DESIGN_BRIEF.md` → "Learned on the pilot".

## How to update
1. New timetable: download the GTFS into `data/raw/gtfs/<date>/`, set `config.gtfs` (a school weekday), run `02_gtfs.py`, then
   per oblast `run_oblast.py <id>` and read the changed lines' readings; adjust `oblasti/<id>/lines.json`.
2. New vehicles: run `01_live_poll.py` detached over a weekday (with `keep_awake.py`), set `config.live.days`, run
   `03_read.py` per oblast and `04_vehicles.py`.
3. `run_oblast.py <id> --final` for every oblast (cross-sheet coverage), `05b_game.py`, `06_render.py`, `07_index.py`.
4. Republish each sheet to its artifact URL; copy each `roster.json` to `roster_published.json`; `pnpm sync` in the repo; give the
   owner the in-game change list (old → new: typed values, buses in / out).
