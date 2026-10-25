# Praha (city buses, PID 100–299): pipeline

Output: `Prague Bus Lines Check.html` in the project root, published at https://claude.ai/artifact/BvCHHf2Wb56SsjMuQgA9ZF. Built by session simutrans-timetable-5a on 29 Sep 2026. Shared rules: `../README.md`.

The user asked for three things. First, every Prague city bus line in the save game (numbered 100100–100299), with its buses and stops, checked against the current PID timetable, filterable to the lines to fix: no vehicles, or stops that don't match. Second, all PID bus lines, not only the broken ones. Third, the same line cards as the tram and trolleybus sheets, with other operators' lines treated exactly like DPP's. Trolleybus 275 is on the trolleybus sheet and the ferries are on the tram sheet, so this sheet is buses only.

```
python scripts/run.py --state 2026-09-29            # rebuild from stored raw data (also refreshes pak_objects.json from the pak checkout)
python scripts/run.py --state <new> --fetch         # download missing timetable, registers and deployment records first
```

## Sources

| What | Where | Stored in |
|---|---|---|
| Game lines | Export from the save-game session (simutrans-122-0-58): every line named 100100–100299 with its buses, entries, halts and waypoints | `data/raw/game/<date>/lines.json` |
| Timetable | `https://data.pid.cz/PID_GTFS.zip`. Lines come from `route_sub_agencies.txt` → `route_licence_number` 100100–100299 with route_type 3 | `data/raw/gtfs/<export date>/gtfs.zip` |
| Deployment records per line and day | `https://seznam-autobusu.cz/vypravenost/pid/vypis?datum=YYYY-MM-DD&linka=N` (car ids in `/vuz/<id>/vypravenost` links) | `data/raw/vypravenost/<date>/<line>.html` |
| Fleet registers (in-service buses, 100 a page) | `https://seznam-autobusu.cz/seznam?iddopravce=<id>&trakce=autobus&prov=1&vcetneSluzebnich=1&page=N`: DPP 106, Arriva City 89, Stenbus 77, About Me 209, ČSAD Střední Čechy 398, Martin Uher 64, ČSAD Polkost 459, Vega Tour 1224, Arriva Střední Čechy 1329, Umbrella City Lines 11174, ČSAD Benešov 27 | `data/raw/register/<date>/dpp_bus_N.html`, `op_<slug>_N.html` |
| Single cars missing from the lists | `https://seznam-autobusu.cz/vuz/<id>` (Aranea cars, new DPP electric buses) | `data/raw/register/<date>/vuz_<id>.html` |
| Pak objects | pak checkout `C:\Users\vojte\Developer\simutrans-custom-czech-pak128\build\VZ-DPPraha-bus`, `VZ-Praha-bus`, `VZ-Praha-water` | `assets/pak_objects.json` (with the commit) |

seznam-autobusu.cz returns 403 to plain curl, so use `common.fetch` (full browser headers) and keep 2 s between requests. Garage codes in the register: Klí Klíčov, Kač Kačerov, Řep Řepy, Hos Hostivař, Vrš Vršovice, Stře Střešovice, Mal Malešice (Arriva City; the register's own count "Praha-Malešice"), BnL Brandýs nad Labem, Kla Kladno. Stenbus's "PID" is a division, not a garage, so it stays blank. The date-range search on the records site is a POST form that keeps its state in the session; GET parameters for it return 403, so the pipeline asks per day.

## Steps (scripts/)

| Script | Does |
|---|---|
| `00_pak_objects.py` | Lists the object names in the Prague bus and ferry packages of the pak checkout into `assets/pak_objects.json`. |
| `01_fetch_sources.py` | Fetches the GTFS and the registers. With `--cars`, also the single car pages for record ids the lists lack. |
| `01_fetch_records.py` | Fetches deployment records for every line on `vehicle_date`. It also fetches `extra_days_non_dpp` for lines not run by DPP (for the pak session) and for lines with fewer courses logged than they need. |
| `02_gtfs_lines.py` | Per line: stop patterns, the main pattern per direction, headway, runtime, the Simutrans schedule (`runfit`, core 16:00–17:00, all termini −1 min) and the buses needed. |
| `02_register.py` | Registers and car pages → `data/derived/vehicles_<date>.json`, keyed by the register's car id. |
| `03_compare.py` | Game lines against PID: stops missing, extra, in place of another, order, and misspelt names. |
| `04_courses.py` | Courses → vehicles with livery and pak object. Fills in courses from other days, then designs any still missing. |
| `05_render.py` | The page. |
| `06_pak_request.py` | What the VZ pak session needs, in `data/derived/<state>/pak_request.json`. |
| `07_halt_renames.py` | Proposed game halt renames (misspellings of the PID name), in the save-game session's TSV format. Nothing is sent. |

## Decisions (state 2026-09-29)

- **Days:**
  - The timetable is PID's export of 29 Sep, service date Wed 30 Sep.
  - Vehicles are from Fri 25 Sep. Records from 21–24 and 29 Sep fill in lines and courses nobody logged on the 25th; the card marks them "logged <day> Sep".
  - The game export is autosave04 of 29 Sep, 17:22.
- **Buses needed:**
  - The need is the larger of two counts.
    - `cycle_need`: the main terminus pair, with a 3-min layover.
    - Buses on the road: every trip of every pattern holds a bus from departure to arrival plus the terminus layover, taking the peak count in 16:00–16:59. The layover is min(3 min, the shortest timetabled turnaround at that terminus in 15:00–18:00), as in `cycle_need`; a flat 3 min overcounted lines that turn in 0–2 min (from the Ostrava bus session, 29 Sep: total 805 → 796).
  - The first count alone misses branches and short workings. Line 191 needs 6 by round trip but 15 on the road; 139 needs 8 against 16. These lines are listed in the card's need text.
  - Where more courses are logged than needed, all are shown. The records have no times, so courses that run only in the morning peak or on school trips can't be told apart.
- **Designed buses:** courses still missing after the other days are "designed, not recorded", always with a real car. User, 29 Sep: real car numbers, and the line's whole roster.
  - Other-day fill-ins, and every designed car, must be active in the register. They must also not be out anywhere in PID on the vehicle date; `data/raw/vypravenost/<date>/overview.html` (the seznam-autobusu.cz day overview) is the check.
  - Designed cars come from the line's own history, `vypis?linka=L&since=2026-09-01`, all pages, working days preferred.
  - A line with no September record falls back to the latest 3 pages since 2025-01-01 (`history_fallback_*` in the state).
  - The picks first cover every bus type in the line's history that the logged buses lack, so each roster type is represented. They then take the newest first.
  - The free history cars left over are listed on the card, dimmed, as "not needed". They are not counted.
  - When the history has too few free cars, free active buses of the line's own types come next, then the operator's usual city-line types, then any city-sized type. The garages of the line's cars go first. Line 226 needed the last step.
  - Result on 29 Sep: 18 designed from history, 27 from the operator's fleet, 33 "not needed". Eight lines have no record at all since 2025: 186, 203, 211, 220, 226, 235, 243, 248.
- **Logged surplus (user, 29 Sep, confirmed via the Brno session):** where more courses are logged than a line needs, exactly the need stays counted. One of every type among the line's buses is kept first (most frequent type first), then the lowest course numbers. The rest are marked "not needed", dimmed at the bottom of the card, and left out of the counts, garages and pak totals. On 29 Sep that is 213 buses, so 797 are counted. This replaces the earlier "keep the operator's slack" on this sheet.
- **Game check:**
  - A game halt matches a PID stop by any of its " / " names, ignoring "Praha," and the stand letter. Abbreviations and misspellings match fuzzily (similarity ≥ 0.85) and are listed as names to fix, without counting as a difference.
  - `halt_aliases` in the state covers names PID abbreviates: VÚ Běchovice.
  - Layover stands (a name containing "odstav") are skipped.
  - The round trip is split at the PID termini and each half is compared with the best PID pattern of that direction. Circular lines are compared whole.
  - Terminus hand-over is allowed: trips end at Letiště and start at Terminál 1.
  - "To fix" means any of: no vehicles, stops that differ, a line not in PID, or a PID line with peak trips and no game line.
- **Liveries** come from the register's current paint:
  - schéma PID šedá → `pidsedocervena`
  - schéma PID červeno-bílo-modrá → `pidcervenomodrobila`
  - městské schéma červeno-bílá → `dppcervenobila` for DPP, `mestskacervenobila` for other operators
  - Veolia → `veoliacervenoseda`
  - bílá → `bila`
  - DPP červená (coach red with the gold Praha skyline, Tourismo RHD 8002) → `dppcervena`.
- CVR Fashion Arena → `fashionarena`: the one advert wrap with its own objects (Vega Tour 8420 and 8421 on line 238; user, via the pak session, 29 Sep). Stenbus 1700 turquoise with a yellow stripe → `tyrkysovozluta`.
- Advert wraps (CVR) and liveries the pak has no slug for get no object of their own; this is the pak session's rule. They take the most common normal livery of the same operator, type and year. Failing that, `pidsedocervena` for cars from 2020 on, else the operator's older scheme.
- **Pak objects:** named by the VZ pak session's scheme (29 Sep 2026, revised the same day).
  - DPP cars: `VZ-DPPraha-<Type>-<livery>-<id>` in VZ-DPPraha-bus.
  - Every other operator: `VZ-Praha-<Type>-<livery>-<id>` in one shared package, VZ-Praha-bus. The operator is not part of the name, and operators share an object per type and livery.
  - Articulated buses are `-A` + `-B`.
  - Type tokens reuse the DPP ones for the same model (`assets/pak_requested.json`). The id differs only for the DPP SOR objects: NB_12, NB_18, BN_12.
  - A name missing from `pak_objects.json` is shown as "requested". Stand-ins from DPP or other cities are not used (user, 29 Sep).
- **Vehicle cell:** number · garage (other operators: operator · garage) / full type · length / pak core. The livery is added where the type has more than one.

## Hand-set schedule rows (method check 25 Oct 2026)

`schedule_overrides` in the state (`02_gtfs_lines.py` applies it, `05_render.py` shows it) replaces a line's terminus rows with hand-set ones: `rows` = list of `{o, d, every, real, why}` with optional `extra` (peak trips left out of the model, HH:MM) and `approx` (no exact run shown). The script works out each row's exact run and its largest deviation in 15:00–17:59 from the trips. Write-up: `../praha/method-check-2026-10-25.md`.

- Different rates at the two ends: 107 (every 4 both ends), 110 (every 15), 122 (hourly), 143 and 157 (every 15 with 2 slots), 189 (every 6), 211 (3 an hour), 232 (every 30; the 5 peak extras have no trip back).
- More slots than departures: 176 (every 15 with 2 slots, not every 60 with 7), 187 (every 90 with 8 slots, the timetable's own 90-min repeat), 207 (every 6).
- The card's two rows were the ends of two different routes: 102 (long line and short working interworked: one circuit line), 103, 111, 139, 226 (line plus its short working), 191 (three lines); all their rows are given.
- Not changed, for the owner: the school lines 251–280 (1–4 trips a day) still show an hourly fit; lines 109, 113, 120, 138, 146, 160, 174, 177, 186, 197 and 221 have branches with ≥ 3 peak trips that are listed as own Simutrans lines but have no rows (values proposed in the write-up).
- The card text now says how the 01:00 origin changes typed values where a row's interval does not divide 60 (116, 131, 187, 218).

## Pak session hand-off

`06_pak_request.py` writes, for the pak session (simutrans-custom-czech-pak128-bd):
- VZ-Praha: every type × livery seen on a city line on any recorded day, with car numbers, operators, the operators' fleet counts, and the cars mapped from wraps.
- VZ-DPPraha: the active DPP fleet types × liveries that have no object. The pak rule is that the whole active DPP fleet is in VZ.

When the pak session reports new objects, run `00_pak_objects.py` (or `run.py`) and the "requested" marks disappear on their own.

## How to update

1. Ask the save-game session for a new export → `data/raw/game/<date>/lines.json`, then set `game_raw`.
2. New timetable: set `gtfs.raw` and `gtfs.service_date` (a normal weekday on the feed).
3. New vehicles: set `vehicle_date`, `extra_days_non_dpp` and `register_raw`.
4. Run `python scripts/run.py --state <new> --fetch`.
5. Check the printed counts (courses by source, designed lines, requested objects) and republish to the same artifact URL.
