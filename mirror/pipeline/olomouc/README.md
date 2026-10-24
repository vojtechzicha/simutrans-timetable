# Olomouc (DPMO trams): pipeline

Output: `Olomouc Tram Peak Fleet.html` in the project root, published at https://claude.ai/artifact/EQDL7ZoM9ENcFuj6LHHn7F.
Maintained by session simutrans-timetable-a2 (taken over from 9e/5a on 29 Sep 2026). Shared rules: `../README.md`. The scripts are the same as `../praha/scripts`
(city-neutral; everything city-specific is in `states/` and `assets/`). Keep the two copies in sync when changing a script.

```
python scripts/run.py --state 2026-09-27            # rebuild from stored raw data
python scripts/run.py --state <new> --fetch         # download missing raw data first
```

## Sources

| What | URL | Stored in |
|---|---|---|
| Deployment records per line and day | `https://seznam-autobusu.cz/vypravenost/mhd-ol/vypis?datum=YYYY-MM-DD&linka=N` | `data/raw/vypravenost/<date>/<line>.html` |
| Day overviews (coverage check) | `https://seznam-autobusu.cz/vypravenost/mhd-ol?datum=YYYY-MM-DD` | `data/raw/vypravenost/overview/<date>.html` |
| Fleet register (one depot, Koželužská) | `https://seznam-autobusu.cz/seznam?page=N&iddopravce=134&trakce=tramvaj&prov=1&vcetneSluzebnich=1` | `data/raw/register/<date>/l_kozeluzska_<page>.html` |
| One withdrawn car (156) | `https://seznam-autobusu.cz/vuz/28793` | `data/raw/register/<date>/car_156.html` (used as `vehicle_overrides` in the state) |
| Timetable | `https://www.dpmo.cz/doc/dpmo-olomouc-cz.zip` (DPMO's own GTFS; version 17 Sep 2026 valid to 12 Dec 2026) | `data/raw/gtfs/<version date>/gtfs.zip` |

Coverage of Olomouc records is uneven: some days have 1–7 sets, others the full ~26. Always check the day overviews
before choosing the vehicle day.

## Steps

As in `../praha/README.md`: 01_fetch → 02_parse → 03_timetable → 04_courses → 05_render (run.py runs 02–05).

## Manual decisions (state 2026-09-27)

- **Day:** Fri 25 Sep has only 7 sets recorded, so the vehicles are from Fri 18 Sep (26 sets, every line, matching the timetable need). One real day, not a mix of days: cars rotate between courses (147 + 148 ran 7/3 on the 18th, 1/2 on the 25th). The 25 Sep sets are shown as a cross-check (`cross_check`).
- **Network:** the DPMO timetable of 18 Sep is identical, trip by trip, to 29 Sep (the first weekday after 27 Sep), so the 18 Sep service date stands for the current network.
- **Shared pool 3 + 5** (verified by the Brno session): 6 line-3 courses serve both lines, and line 5 is never recorded on its own. 3 and 5 run every 15 and every 30 min between the same termini, so one alternating circulation cannot work: they are two Simutrans lines drawing on one pool (`splits.3/5`): 3 = courses 3/1–4 (needs 4), 5 = 3/5–6 (needs 2), as a stated choice. Both need bidirectional sets (U Kapličky is a stub).
- **Designed trams:** none needed (recorded ≥ cycle need on every line); recorded = need exactly on every line on 18 Sep).
- **Not needed (user, 29 Sep 2026; `../README.md` "Roster coverage and spares"):** `04_courses.py` marks logged surplus per Simutrans line (branch, pool or line need from `timetable.json`) as `uncertain = 'spare'`: one set of each type kept first, then recorded before designed, then the lowest course numbers. `05_render.py` dims them, flags "not needed" and leaves them out of counts, depots and pak totals. None on 18 Sep. Patch shared with praha / praha-trolleybus (session 5a).
- **Designed trams, if ever needed:** real car numbers from the line's own history (older `vypis` days), checked against that day's overview, every roster type covered first, leftover history cars shown as "not needed".
- **Phone header (29 Sep 2026):** under 700 px the line-badge and depot rows scroll sideways (`.nav.lines` / `.nav.dnav`), so the sticky bar stays about 120 px tall on a 390 px phone.
- **Car 156** was withdrawn on 18 Sep 2026 (its last day); it is not in the in-service register list, so `vehicle_overrides` supplies its type and paint.
- **Pak:** VZ-DPOlomouc-tram.pak, pak128 main 7be7413 (pak128 session). One real car = one object; the 2nd car of an EVO1/o or VarioLF plus/o pair is the "-reverse" object (`position: 2` rules). VarioLFR.S, VarioLFR.E and VarioLF.E are the VarioLF object (exact). One livery; advert wraps ignored.
- **Termini:** Fibichova, Nová Ulice, Neředín and Pavlovičky are loops (−1 min); U Kapličky is a stub (real minute). `stop_aliases` merges Hlavní nádraží into Fibichova and spells out "Neředín,kremat.".

## How to update when the timetable changes

1. Save the new DPMO GTFS in `data/raw/gtfs/<version date>/gtfs.zip` (or set `gtfs.raw` and run `01_fetch.py`).
2. Copy `states/2026-09-27.json` to `states/<new date>.json`; set `network_date`, `gtfs.raw`, `gtfs.service_date`. For new vehicles, check the day overviews for a complete weekday and set `vehicle_date`.
3. Review `pools` / `splits` (course choice for 3 and 5), `course_notes`, `flags`, `cross_check`, `vehicle_overrides`, and `assets/termini.json` for new termini.
4. `python scripts/run.py --state <new date>`; check the counts; republish to the same artifact URL.
