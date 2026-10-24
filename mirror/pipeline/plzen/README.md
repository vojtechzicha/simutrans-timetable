# Plzeň trams (PMDP)

The Plzeň tram sheet is built from stored raw data by the scripts in this folder. The shared rules are in `../README.md`.

| State file | Network | Output (project root) | Artifact |
|---|---|---|---|
| `states/2026-09-27.json` | 27 Sep 2026 | Plzeň Tram Peak Fleet.html | https://claude.ai/artifact/J5W3n79YLXAjgruuhtSjam |

Rebuild offline:

```
cd pipeline/plzen/scripts
python run.py --state 2026-09-27
```

Python 3, standard library only.

## Sources

| What | URL | Stored in |
|---|---|---|
| Which days have tram records | `https://seznam-autobusu.cz/vypravenost/mhd-plzen?datum=YYYY-MM-DD` | `data/raw/vypravenost-days/<date>.html` |
| Vehicle per kurz with notes, one list per line (1, 2, 4) | `https://seznam-autobusu.cz/vypravenost/mhd-plzen/vypis?datum=YYYY-MM-DD&linka=N` | `data/raw/vypravenost/<date>/L<N>.html` |
| PMDP tram register: type, livery, state (5 pages, includes historic cars) | `https://seznam-autobusu.cz/seznam?iddopravce=71&trakce=tramvaj&page=N` | `data/raw/register/<date>/page<N>.html` |
| Timetable | `https://jizdnirady.pmdp.cz/jr/gtfs`, which returns the zip directly | `data/raw/gtfs/<date>/gtfs.zip` |
| Pak objects | the pak128 session, VZ-PMDP-tram.pak (pak128 main 6547eb6) | `pak` in the state file |

- **Records:** the vypravenost is crowd-sourced. Plzeň has no tram records for Wed 23 to Fri 25 Sep 2026; Fri 18, Mon 21 and Tue 22 Sep are complete. `02_parse.py --days` writes the per-day counts to `data/derived/day_counts.json`.
- **seznam-autobusu.cz:** send browser headers (`common.fetch`) and wait 2 s between requests.
- **GTFS feed:** valid from 22 Sep 2026, so it covers 25 Sep and the 27 Sep network, but not 18 Sep.

## Steps

1. `01_fetch.py`: downloads the raw data (`--days`, `--vehicles <date>`, `--register`, `--gtfs`).
2. `02_parse.py`: writes `vypravenost_<date>.json` (line, kurz, cars, car ids, note) and `vehicles_<date>.json` (car id → number, exact type, livery). The register shows the KT8 as "ČKD Tatra KT8D5 » KT8D5.RN2P"; it's normalised to "ČKD Tatra KT8D5.RN2P".
3. `03_timetable.py --state X`: GTFS tram trips of `service_date` → network table, schedule fits, Simutrans rows with the loop −1 rule, minimum trams by runtime, and trams at 16:00 by trip chaining.
4. `04_fleet.py --state X`: the afternoon car per kurz, with notes.
5. `05_render.py --state X`: writes the HTML.

## Decisions

- **Vehicles:** Fri 18 Sep 2026, the latest complete Friday, because 23–25 Sep have no records. **Network:** 27 Sep, using the GTFS service day Fri 25 Sep.
- **Notes:**
  - *ráno*: morning-only car.
  - *odpoledne*: the afternoon car.
  - *ráno i odpoledne*: split duty (kurzy 21 and up are peak-only split duties).
  - *výměna za X*: this car was replaced by X (not counted).
  - *náhrada za Y*: this car replaced Y (counted). The swap time isn't recorded.
  - Extra note for 1/3: 361 had worked 1/25 in the morning (`fleet.note_extra`).
- **Depot:** one tram depot, Vozovna Slovany.
- **Termini:** all loops, because the whole fleet except the KT8D5 is single-ended. Every schedule entry is real − 1.
- **Fit windows (`fit.core`):**
  - Lines 1 and 2: 15:00–16:00, their 5-minute peak. It ends about 16:05 (line 1) and 16:20 (line 2); after that the real lines run every 6 min.
  - Line 4: 16:00–17:30, because before 16:00 the two branches run an irregular 3/6/9-minute pattern.
- **Bolevec:** the 15:46 and 15:56 departures end at Vozovna Slovany but leave Bolevec in the 5-minute pattern, so they count as Bolevec → Slovany (`fit.depot_trips_counted`). Every other depot run is ignored.
- **Line 4:** one Simutrans line, Košutka → Bory → Košutka → Univerzita, because 17 of 22 trams alternate between the branches. Košutka is in the schedule twice (offsets 4 min apart, every 8 each). The minimum trams count as a circuit (`circuit: true`).

## How to update when the timetable changes

1. Fetch the new data: `python run.py --state 2026-09-27 --fetch`. It downloads:
   - day overviews for the last 10 days;
   - the register;
   - the GTFS;
   - and it prints which days have tram records.
2. Copy the state file to `states/<new>.json`, then set:
   - `gtfs_date`, and `service_date` to a Friday of the new timetable;
   - `register_date`;
   - `vehicles_date` to the latest complete Friday in `data/derived/day_counts.json`. Fetch its lists with `python 01_fetch.py --vehicles <date>`.
3. Run `python 03_timetable.py --state <new>` and check the printed schedule. If a line's peak pattern moved, adjust `fit.core`. Check line 4's branch structure too.
4. Run `python run.py --state <new>`. Update `texts` (dates in the eyebrow, lede and method) and the swap notes in `fleet.note_extra`.
5. If the pak changed, update `pak` from the pak128 session.
6. Re-publish to the artifact URL above.

## Spares (user rule, 29 Sep 2026; applied by session simutrans-timetable-3a)

- Each line counts exactly its need; logged trams beyond it are marked "not needed", left out of all counts, the depot and the pak totals, and listed dimmed on the line card (`fleet.json` `spares`).
- **Need** (`timetable.json` `sline_need`): the larger of `circuit_need` over the line's schedule entries (from `../brno-trolleybus/scripts/common.py`, 3-min layover; line 4 as its one-line circuit) and the most trams on the road at once 16:00–16:59, counting the Bolevec depot runs as the pattern does: 1 = 11, 2 = 12, 4 = 18.
- **Which are marked:** one of every unit type of the line first (40T0/1/2 count as one type, one pak object), then all-day kurzy before afternoon-only ones, lowest kurz first. Result: 41 counted + 10 not needed (1: 3, 2: 3, 4: 4).
