# Most–Litvínov trams (DPmML): peak vypravenost sheet

Output: `Most-Litvinov Tram Vypravenost.html` in the project root, published at
https://claude.ai/artifact/FxHCAC84oCJA7qkbCKiQZi (republish to the same URL).
Shared rules for all cities are in `../README.md`.

## What the sheet shows

- **Vehicle day:** Friday 25 Sep 2026. Lines 1, 2 and 4 are shown at **15:00** (the Chempark shift change, when the most trams are out; line 1 stops about 16:00). Line 3 runs only in the morning, so it is shown at 06:00.
- **Network state:** as of 27 Sep 2026.
- **Per line:** branches, headway, minutes, the Simutrans schedule (loops 1 min early), and trams shown as number / full type / pak core.
- **Depot and fleet:** one depot table (Most, Dopravní podnik), the spare fleet and the Pak128 objects table.

## Sources

| What | URL | Notes |
|---|---|---|
| Timetable | https://portal.cisjr.cz/pub/draha/mestske/JDF.zip | Lines 575001–575004, JDF **1.11**: stop times sit at a different index than Ostrava's 1.8, and `lib.jdf_trips` detects which. The 14 Jun 2026 versions of 1, 3 and 4 are marked as diversion versions. |
| Fleet register | https://seznam-autobusu.cz/seznam?trakce=tramvaj&iddopravce=399&prov=1 | Same WAF headers as Ostrava. There is one depot, so no depot filter. |
| Allocation | none exists | seznam-autobusu has 0 records for every DPmML tram, and dpmost.cz has no vehicle map. |
| Live layer | https://mapy.mesto-most.cz/koop/rest/services/mhd/FeatureServer/0/query?where=1%3D1&outFields=*&f=json | City of Most, "Poloha vozidel MHD" (fields CISLO_VOZIDLA, CISLO_LINKY). It returned **0 features** on 16 Sep and 28 Sep 2026. `01_fetch.py --live` stores one poll so this can be checked again. |
| Closures | https://www.dpmost.cz/doprava-zmeny, https://www.dpmost.cz/zvd2026001 | Since 1 Mar 2026 (23:15), Záluží, Chemopetrol – Litvínov, Citadela is run by replacement buses (the Litvínov modernisation). |
| pak128 | pak128 session `simutrans-custom-czech-pak128-77` | VZ-DPMostLitvinov-tram.pak: one livery (mostzlutocervena) and 5 exact types. |

## Steps (`scripts/`, stdlib-only Python)

1. **`01_fetch.py [--jdf] [--fleet] [--live]`** saves the raw inputs to `data/raw/<snapshot>/`.
2. **`02_timetable.py`** picks versions (the shared rule) and **cuts the trips at Záluží, Chempark** (`config.cut_trips`), where the trams turn today. Output: `derived/trips.json`.
3. **`03_fleet.py`** writes `derived/fleet.json` and `live.json`.
4. **`04_roster.py`** counts the turns at each line's peak minute and **checks the designed roster** in `config.roster`: the unit counts must match, every car must be active, and none may be used twice. It then computes each line's **round-trip need** (cycle_need at the line's peak, 3 min or the terminus's shorter turnaround) and flags it if the roster is below it. Problems are printed, and `06_render.py` refuses to run while any remain.
5. **`05_schedule.py`** writes the Simutrans fields with the shared runfit rule around each line's peak (`config.fit`: core 14:30–15:30, and 05:30–06:30 for line 3). The real minutes are stored, plus the values to type in (real − 1 at loops).
6. **`06_render.py`** fills `templates/page.html` and writes the HTML to the project root.

`python scripts/run.py` runs steps 2–6 offline; `--fetch` refreshes the raw data first.

## Decisions (all in `config.json`)

- **Line 1 (user decision, 28 Sep 2026):** the Chempark shift line has 5 trams at 15:00 but 1 at 16:00. It is kept with that one tram (T3M.3 pair 236 + 237) on a **designed** every-60 shuttle, Dopravní podnik :08 / Chempark :42 (the timetable's last minutes), set in `config.schedule_override`. Its pre-peak trips are listed as not modelled (peak rule: at least 3 trips in 15:00–17:59, no depot end, and a departure in the 16:00 hour).
- **The roster is designed by hand** (`roster`, with a "why" for each line):
  - Line 4: EVO2 325–328. The type was bought for line 4, and 2 of its 4 turns are guaranteed low-floor.
  - Line 2: VarioLF plus 314 and 315 (registered as line-2-only) and VarioLFR.S 253.
  - Line 1: the five fixed T3M.3 pairs 236+237, 244+245, 247+282, 205+240 and 301+306.
  - Line 3: solo T3M.3 302, 305 and 308.
  - EVO2 329 and 330 are in the workshops after their 3 Aug 2026 collision (`car_notes`).
- **Trip cut:** at the first stop containing "Chempark" on trips to or from Citadela. Night line 40 is all buses and is left out.
- **All termini are loops**, so every departure is set 1 min early.
- **One Simutrans line per DPmML line** (`branches`). Needs on 25 Sep: line 1 needs 4 (5 assigned; the fifth came in from Velebudická), 2 needs 3, 3 needs 3, 4 needs 4. There are no shared pools.
- **Lengths** for the vehicle cell are in `type_lengths`: EVO2 21.7 m (Czech Wikipedia), the other types are single cars of 15.1 m.
- **Stop-name expansions:** 1.nám. → 1. náměstí, Čs.mládeže → Československé mládeže.
- **pak:** everything is exact. Advertising wraps appear in yellow-red. The T3M.3 art is a placeholder (the classic Most T3 body).

## How to update when the timetable changes

1. In `config.json`, set `snapshot`, `vehicle_day` (+ labels) and `network_state_label`.
2. Run `python scripts/01_fetch.py`.
3. Check https://www.dpmost.cz/doprava-zmeny. Is Chempark – Citadela still run by buses? If trams run to Citadela again, remove `cut_trips` and update `network_state`, `line_titles` and `line_notes`.
4. Run `python scripts/run.py`. If `04_roster.py` reports a count mismatch, for example because the timetable added a turn, edit `config.roster`: add cars from the spare list and keep the rules above. If a car went to the workshops, swap it for a spare of the same type.
5. If the live layer ever returns vehicles (`derived/live.json` has cars), poll it through a weekday peak and replace the designed roster with the observed one.
6. Republish to the artifact URL.

## Data snapshot

`data/raw/2026-09-28/`: JDF.zip (the export of 25 Sep 2026), fleet/p1.html and live/ (one empty poll).
