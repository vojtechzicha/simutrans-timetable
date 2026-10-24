# Brno trams (DPMB)

The Brno tram sheets are built from stored raw data by the scripts in this folder. The shared rules (day choice, fit rule, loop −1, vehicle cell, pak sync) are in `../README.md`.

| State file | Network | Output (project root) | Artifact |
|---|---|---|---|
| `states/closure-2026-09-27.json` | 27 Sep 2026, Kníničská closure (line 10 at Sochorova) | Brno Tram Peak Fleet.html | https://claude.ai/artifact/5ntT3kwFmuEU3Bo3RbvvZD |
| `states/from-2026-09-29.json` | from Tue 29 Sep 2026 (line 10 back to Komín) | Brno Tram Fleet from 29 Sep.html | https://claude.ai/artifact/3ps2U3Ac81p5h3ABRwgQVg |

Rebuild everything offline:

```
cd pipeline/brno/scripts
python run.py --state closure-2026-09-27
python run.py --state from-2026-09-29
```

Python 3, standard library only.

## Sources

| What | URL | Stored in |
|---|---|---|
| Vehicle per kurz (vypravenost), one page per line | `https://www.bmhd.cz/vypravenost/vypravenost.php?datum=YYYY-MM-DD&linka=N` | `data/raw/vypravenost/<date>/L<N>.html` |
| Depot register (Medlánky, Pisárky; Komín = trolleybuses) | `https://www.bmhd.cz/evidence-dpmb/vozovna/{M,P,K}` | `data/raw/register/<date>/voz_*.html` |
| Exact subtype + livery per car | the `vozp.php?...trakce=tramvaj&depotId=..` listings linked from the depot pages (some have a `page=2`) | `data/raw/register/<date>/types_*.html` |
| Timetable | `https://kordis-jmk.cz/gtfs/gtfs.zip` (IDS JMK GTFS) | `data/raw/gtfs/<date>/gtfs.zip` |
| Terminus layouts (track counts, loop/stub) | the older "Brno Tram Termini.html" sheet | `assets/termini_meta.json` |
| Pak objects | the pak128 session (simutrans-custom-czech-pak128-77) | `assets/pak.json` |

- **bmhd.cz firewall:** it returns *403 Access Denied* to plain HTTP clients. `common.fetch` sends a full Chrome User-Agent plus Accept and Accept-Language headers, and waits 2 s between requests.
- **GTFS feed:** exported 25 Sep 2026, stored 28 Sep. It covers 25 Sep to December, including the timetable change on 29 Sep.

## Steps

1. `01_fetch.py`: downloads the raw data (`--vehicles <date>`, `--register`, `--gtfs`).
2. `02_parse.py`: turns the pages into `data/derived/vypravenost_<date>.json` (line → kurz, cars, note) and `vehicles_<date>.json` (car → exact type, depot, livery).
3. `03_timetable.py --state X`:
   - Takes the GTFS tram trips of the state's `service_date`: first and last stop, departure, arrival.
   - Builds the network table (16:00 departures, headway, runtime).
   - Fits the schedule per terminus pair and applies the loop −1 rule.
   - Counts trams needed by runtime and by timetable cycle (`common.cycle_need`).
   - Writes `data/derived/X/timetable.json`.
4. `04_fleet.py --state X`: picks the afternoon car per kurz, writes the notes, assigns split lines (5S, 8S) and applies the tram moves. Writes `fleet.json`.
5. `05_render.py --state X`: writes the HTML into the project root.

## Decisions (all in the state files unless noted)

- **Vehicles:** Fri 25 Sep 2026, the last weekday before 27 Sep (28 Sep is a holiday).
- **Afternoon car per kurz:**
  - Records noted *ráno*, *ranní kurz*, *ráno, před/po výměně* are morning-only and listed under "Not counted".
  - *Odpoledne* marks the afternoon car; *ráno i odpoledne* is a split duty.
  - For *před/po výměně* without resolution, the replacement is listed.
  - Resolved swaps are in `fleet.resolved_swaps`:
    - 1/11: 1827 turns up on 1/23 in the afternoon.
    - 9/6: 1765 and 1777 swapped with 8/48 in the morning.
  - The chain swap 9/22 → 2/18 has its wording in `fleet.note_overrides`.
- **Depots:** on weekdays, odd kurzy are Pisárky and even kurzy are Medlánky (`fleet.kurz_depot`). The BMHD register disagrees for 20 cars: EVO2 1822–1835, T3R.EV 1531/1560/1562/1569 and 13T 1940 are registered Medlánky but ran only odd kurzy. The sheet shows both views and treats the kurz view as the better guess.
- **Split Simutrans lines (`fleet.splits`):**
  - **5S** = line 5 kurzy ≥ 21: the Mendlovo náměstí short workings, run by 20 m single cars.
  - **8S** = line 8 kurzy 20, 26, 32, 42, 44, 46, 48. Its size comes from the round trip: 28 + 4 + 29 + 2 = 63 min at every 10 min, so 7 trams. Line 8 needs 16 (73-min round trip, 2 departures every 10 min) plus 1 spare. The records don't say which kurz ran the short trips. 8S takes the five peak-only kurzy (car changed between morning and afternoon) plus 44 and 46.
- **Schedule:**
  - The fit uses the shared rule over the core 15:30–16:30.
  - **Line 8 from Bohunice:** fixed in `fit.overrides`. One 15:50 short trip runs through to Mifkova and would otherwise break the pattern.
  - **Line 12 in the closure timetable:** approximate (`fit.approx`: every 6, best offset, ±3 min).
  - **Line 12 from 29 Sep:** exact at every 14 (`fit.any_interval_lines`).
  - **Non-loop termini (`nonloop`):** Mifkova and Nemocnice Bohunice (stubs), and Sochorova (the temporary turn-back during the closure). Every other terminus gets real − 1.
  - **Line 10 from 29 Sep:** arrivals are named "Vozovna Komín" but it's the Komín loop, so `stop_alias` maps them to "Komín, smyčka".
- **From 29 Sep, tram moves (`fleet.moves`):** the timetable cycle at 16:00 gives line 3 12 trams instead of 15 and line 12 14 instead of 12. Keeping Friday's slack, line 3 goes 19 → 16 and line 12 14 → 16:
  - 3/21 (1235 + 1236) and 3/24 (1930) move to line 12.
  - 3/7 (1245 + 1246) goes to reserve.
  - These are suggestions until the first vypravenost after 29 Sep.
- **Trip chaining:** `common.chain_at` (FIFO trip chaining) is kept for reference only. Around depots it miscounts (it gave line 10 7 trams from 29 Sep), so use `cycle_need`.

## How to update when the timetable changes

1. Download the new GTFS: `python 01_fetch.py --gtfs`. It lands in `data/raw/gtfs/<today>/`.
2. Copy the latest state file to `states/<new-name>.json`, then set:
   - `gtfs_date` to the new folder, and `service_date` to a Friday of the new timetable;
   - `compare_with` to the previous state;
   - `output`, `title` and the `texts` (eyebrow, lede, network intro, `changes_why`).
3. Run `python 03_timetable.py --state <new>` and read:
   - the printed schedule;
   - `cycle_need` against the previous state. A line whose number changes needs `fleet.moves` (take cars off, or move them between lines).
4. Check `simutrans_lines`: new termini or branches need new entries. A new stub or turn-back terminus goes in `nonloop`. Check `stop_alias` too.
5. Run `python run.py --state <new>`, open the HTML, and look at the "What changes" table.
6. **If the fleet should follow as well:** `python 01_fetch.py --vehicles <new Friday> --register`, then set `vehicles_date` and `register_date`. Re-check `resolved_swaps`, `note_overrides` and the 8S kurzy (`fleet.splits`) against the new records: kurz numbers can change with a new timetable.
7. **If the pak changed:** update `assets/pak.json` from the pak128 session's message.
8. Re-publish to the artifact URL in the table above, or add a new row for a new sheet.

## Spares (user rule, 29 Sep 2026; applied by session simutrans-timetable-3a)

- Every Simutrans line counts exactly its need; logged trams beyond it are marked "not needed". They leave the counted lists (`fleet.json` `spares`), so they are out of every count, depot list and pak total, and are listed dimmed at the bottom of their line card.
- **Need** (`timetable.json` `sline_need`): `common.cycle_need` where the state has a cycle pair, otherwise `circuit_need` over the line's schedule entries (from `../brno-trolleybus/scripts/common.py`, 3-min layover), raised to the most trams on the road at once 16:00–16:59 for unsplit lines (line 1: 21 → 22). `fleet.need_overrides`: 8S = 7 (its short trips don't close a circuit in the feed), 7 = 8 (the closure-day 7 turns into Zemědělská before a guarded circuit closes).
- **Which are marked** (`mark_spares`): one of every unit type of the line first (a type is the set's types; 13T subtypes count as one), then all-day kurzy before afternoon-only ones, lowest kurz first.
- **From 29 Sep:** the earlier tram moves (3/21 and 3/24 to line 12, 3/7 to reserve) are dropped. Line 12 is covered by its own 14 logged trams (need 14), and line 3's surplus over its need of 12 is marked not needed. This supersedes the "keep the operator's slack" ruling.
- **5S designed tram:** 5S needs 5 (every 10 min, 61-min round trip) and 4 were logged. By the roster rule, a real car from its own history, free that day, is added and marked 'designed, not recorded' (`fleet.designed`, checked in 04_fleet.py against the day's records and the register). The only free car in the 5S history (line 5 kurzy 21+, 16–24 Sep, raw pages in data/raw/vypravenost) is **1088** (Pragoimex VarioLF2R.E; 5S on 24 and 17 Sep). The logged 4 already cover both 5S types, and there are no other free history cars to mark not needed.
- Result: closure 151 counted (incl. 1 designed) + 23 not needed; from 29 Sep 150 + 24.
