# Pardubice (DPMP): trolleybuses and buses, afternoon-peak fleet sheet

Output: `Pardubice MHD Peak Sheet.html` in the project root (title "Pardubice MHD Peak Sheet"). Published at https://claude.ai/artifact/KrzshkuVv9T5GqpiUKLJ7y (version 2 = this per-vehicle rebuild, 29 Sep 2026; version 1 = the old per-line sheet, kept in legacy/); republish to the same URL. Shared rules for all cities are in `../README.md`.

One sheet for both modes: trolleybus lines and bus lines are separate groups, and line badges are blue for trolleybuses and red for buses. The page looks like the Brno bus and trolleybus sheets: it uses their style (`../brno/assets/style.css.html`), their sticky bar and marks (`../brno-trolleybus/assets/extra.css.html`), and `assets/page_extra.css.html` for the mode colours.

| State file | Network | Vehicles | Built |
|---|---|---|---|
| `states/2026-09-29.json` | Tue 29 Sep 2026 (CIS JŘ JDF export of 28 Sep) | Fri 25 Sep 2026 | 29 Sep 2026, session simutrans-timetable-a2 |

```
cd pipeline/pardubice/scripts
python run.py --state 2026-09-29              # rebuild from data/raw (no network)
python run.py --state 2026-09-29 --fetch      # fetch whatever raw data is missing first
python run.py --state 2026-09-29 --pak        # also re-read the pak checkout (00_pak_objects.py)
```

Python 3, standard library only. Playwright (python, channel `msedge`) is used only to check the page by hand.

## The old sheet

`legacy/` holds the two old per-line reference sheets, unchanged: `Pardubice MHD Peak Sheet.html` (26 Sep 2026, the newest) and `pardubice-mhd.html` (25 Sep 2026). Their text (line notes, specials, battery sections, fleet notes, sources, lines left out) is in `assets/reference.json`. It was extracted from the old page's embedded JSON, the per-line vehicle counts ("seen") were dropped, and abbreviations were written out ("Kpt." as "Kapitána", "nám." as "náměstí"). The new sheet shows that reference below the vehicle cards: battery sections, stops and their lines, termini, and specials and closures.

## Sources

| What | Where | Stored in |
|---|---|---|
| Timetable | CIS JŘ JDF: the city export `https://portal.cisjr.cz/pub/draha/mestske/JDF.zip` (trolleybus lines, traction T) and the bus export `https://portal.cisjr.cz/pub/jdf/JDF.zip` (bus lines, traction A), both exported 28 Sep 2026 19:00. Nothing was downloaded: `01_fetch.py --jdf` copies DPMP's inner zips (licences 655xxx, IČO 63217066), byte for byte, out of the copies the Ostrava pipelines already hold (`../ostrava-trolleybus/data/raw/2026-09-29/JDF.zip`, `../ostrava-bus/data/raw/2026-09-29/JDF.zip`). | `data/raw/jdf/2026-09-28/city/` (49 files), `.../bus/` (54 files) |
| Vehicles on the day | seznam-autobusu.cz "MHD Pardubice" (slug `mhd-pardubice`, data from tram-bus.cz): `vypravenost/mhd-pardubice/vypis?datum=D` (3 pages of 50) and the day overview `vypravenost/mhd-pardubice?datum=D` | `data/raw/vypravenost/2026-09-25/` |
| Line history | `vypravenost/mhd-pardubice/vypis?linka=N&since=2026-09-01`, all pages, for every line. The site's line id is the line number, except the night pair 98/99 (id 49), which is not needed. Lines with no record since then (18, 22, 33, 88) also get the latest 2 pages of any date. | `data/raw/vypravenost/history/2026-09-01/`, `.../history/latest/` |
| Fleet register | `seznam-autobusu.cz/seznam?prov=1&trakce={trolejbus,autobus}&iddopravce=47&vcetneSluzebnich=1` (DP města Pardubic; one page each). This gives the number, type, year, paint, state and depot. Records are matched to the register by the site's car id (`/vuz/<id>`). | `data/raw/register/2026-09-29/` |
| Battery sections, battery cars, specials, closures, lines left out | The old sheet (its sources: DPMP line timetables and notices, pardubice.eu, Pardubice ŽIVĚ, Deník, trolejbus.cz fleet list of 18 Mar 2026, Czech Wikipedia) | `assets/reference.json`, `states/…json` (`battery_sections`, `battery_required`, `left_out`), `assets/pak_map.json` (`battery_cars`) |
| Pak objects | Local checkout `C:\Users\vojte\Developer\simutrans-custom-czech-pak128`, `build/VZ-DPPardubice-trolleybus` and `build/VZ-DPPardubice-bus` (main b84c15c, 28 Sep 2026), read only | `assets/pak_installed.json` (from `00_pak_objects.py`), `assets/pak_map.json` (hand-written rules) |

dpmp.cz was not used: it rate-limits hard (429, then refused connections). seznam-autobusu.cz needs a plain browser User-Agent with Accept headers. `common.fetch` waits 2 s between requests, and no personal data goes into any request.

## Steps (`scripts/`)

| Script | Does |
|---|---|
| `00_pak_objects.py` | Lists the VZ-DPPardubice objects (name, length, engine) and the checkout's commit into `assets/pak_installed.json`. |
| `01_fetch.py` | `--jdf` extracts DPMP's inner zips (`--jdf-download` fetches fresh exports first). `--records` gets the day list and overview, `--register` the register, and `--history` the line histories. |
| `02_timetable.py` | Picks one JDF version per line for the day and classifies the lines (peak, morning, night, school, none). Writes `trips.json`. |
| `03_network.py` | Writes variant tables, Simutrans lines (branches by rule), the need at 16:00, the schedule fit per stop entry, and the stop and terminus reference tables to `network.json`. |
| `04_fleet.py` | Builds the register, the afternoon car per kurz, the kurz split, logged surplus, and designed cars with the leftover history cars. Checks battery cars. Writes `fleet.json` and `vehicles.json`. |
| `05_render.py` | Writes the page into the project root. |
| `06_pak_request.py` | Writes `pak_request.md` (this folder) for the VZ pak session. |
| `run.py` | Runs 02–06 (with `--fetch` also 01, with `--pak` also 00). |

`common.py` imports the shared helpers:
- from `../ostrava/scripts/lib.py`: the seznam-autobusu parsers, the JDF table reader and version rule, `blocks`, `min_turnaround`, `runfit` and `loop_shift`;
- from `../ostrava-trolleybus/scripts/lib.py`: `cycle_need_peak`;
- from `../brno-trolleybus/scripts/common.py`: `mark_spares`.

It has its own `jdf_trips`, which differs from the tram lib in two ways:
1. DPMP's JDF 1.10 `Zasspoje` rows have 12 fields (arrival at index 9, departure at 10), and the tram lib reads them as 1.11 (10/11) and crashes.
2. DPMP marks its school-holiday trips with Caskody type 1 ("runs in") date ranges. The tram lib ignores type 1, so those trips ran every day and doubled lines 1, 2, 5 and 13. Type 1 and type 3 ranges now restrict a trip, OR-ed together.

## Decisions

Earlier decisions of the user (from the old sheet), kept:
- **Lines on the sheet:** every DPMP day line with afternoon service: trolleybus lines 1, 2, 3, 4, 5, 7, 11, 13, 17, 18, 21, 27, 30 and 33, and bus lines 6, 8, 9, 10, 12, 14, 15, 16, 20, 22, 23, 24, 25, 28 and 88. The airport line **90** is included although it runs only to the flight schedule. Its trips are the Monday ones (5 Oct 2026, `service_date_overrides`), as on the old sheet, because it has no service on Tuesdays.
- **Left out:** night lines 98 and 99, school line 29, the non-public Škola Svítání service 910, and the bridge replacement lines 902 and 906 (cancelled 1 Sep 2026, still in CIS JŘ). They are in `left_out` and on the page.
- **Line 20** ends at 14:43 and has no afternoon peak. As before, it uses its morning timetable: reference time 7:30 (`line_t0`), fit window 5:30–10:00. Its one midibus (21, logged on the day) is counted.
- **Closures:** long-term closures are modelled as they run: the provisional Kapitána Bartoše bridge with lines 2, 6 and 18 back on it, line 13's detour via Bělehradská until about 2028, new line 21, and the Tuněchody works on line 12. Short-term closures are ignored (line 9 Počaply, the 2–4 Oct events).
- **Mode:** line 12 is licensed as a trolleybus line (traction T in JDF), but buses run it in practice, so it sits in the bus group. Line 18 is a trolleybus line since 1 Sep 2026. The version from 1 Sep in the city export beats the bus version from 1 Jan in the bus export. Its Živanice trips (by bus, per the old sheet) are merged into 18.
- **Battery sections:** taken from the old sheet, not from OSM: 1 (Jesničánky – Dražkovice – Mikulovice), 17 (Semtín / Ohrazenice – Srch), 18 (Rybitví – Černá u Bohdanče, inferred), 27 (the Zdravotnická škola end, inferred) and 30 (beyond U Josefa to Cihelna, Staré Hradiště and Ohrazenice). Battery cars: the 30 Tr 480–483 and the 32 Tr 460–469 and 476–497 (`pak_map.json` `battery_cars`). The Simutrans lines 1D, 17, 18, 27 and 30C get only battery cars (`battery_required`), and `04_fleet.py` checks it (`battery_issues` must be empty).
- **Specials** (through-running 2 → 12 in the evening, the 22 connection at Pardubičky, the express trips of 23, the 8 + 88 pair, 12 and Úhřetice): shown as on the old sheet.

New decisions (29 Sep 2026):
- **Days:** the network is the timetable in force on Tue 29 Sep 2026, a school day (the brief's target date). The vehicles are from Fri 25 Sep 2026 (104 records, 96 kurzy), one real day. The old sheet used Tue 6 Oct because line 29 changes on 1 Oct, but 29 is left out, so the modelled lines are the same.
- **Simutrans lines by rule** (the Ostrava bus rule, `branch_rule`). Per DPMP line, the terminus pair with the most trips in 15:00–17:59 is the main line. Another pair becomes its own line when it has at least 6 trips (3 for a loop), a 16:xx departure and no depot end. That gives 37 Simutrans lines on 30 DPMP lines:
  - branch lines 1D (Dražkovice), 2P (Pardubičky), 6H (Vápenka – Hlavní nádraží), 8S (the Svítkov loop), 9S (Spojil), 12M (Mnětice) and 30C (Cihelna);
  - everything else is merged into the line leaving the same terminus: 3 to U Mlýnů, 7 and 11 to Rybitví, 4 to Globus, 10 to Nemošice and Ostřešany park, 12 to Tuněchody, 18 to Živanice, 28 to Sezemice, 30 to Ohrazenice, and 1 to Mikulovice.
  - Chaining trips shows that vehicles switch between branches irregularly on 2, 6, 9, 12 and 30, never A–B–A–B, so these are branch lines, not one line with the terminus twice. On 1, the Dražkovice cars stay on Dražkovice.
- **Pools:** 33 runs on line 3's kurzy and 88 on line 8's (`records_of`). Neither has a record since 2020 and 2024 respectively. The old sheet says 33 shares vehicles with 3, and DPMP publishes 8 + 88 together.
- **Kurz split** (a choice, and said so on each card): a line's own branches take their need first, from the highest kurzy, battery cars first where needed. Then the main line takes the lowest kurzy, then the pooled line takes the rest. Any remainder goes to the main line.
- **Need** (brief rule d):
  - `cycle_need_peak` per Simutrans line, with each terminus's own shorter turnaround (at most 3 min) and max_wait = max(30, 1.5 × headway). A loop counts the departures in one round trip.
  - Each DPMP line gets at least its most trips on the road at once in 16:00–16:59; the extra goes to the main line (3, 7, 10, 11, 12, 14, 18, 30, 88).
  - Every Simutrans line gets at least 1 (the thin lines 16, 22, 23, 25 and 90).
  - Total need: 87.
- **Afternoon car per kurz:**
  - A "ráno" row is a morning duty.
  - "nahrazen X" gives way to X: 30/1 is 476, which replaced bus 209.
  - A car with no note that works another kurz "odpoledne" is the morning car there: 8/6 (220) and 8/7 (103).
  - The 98/99 night cars are not counted.
  - All of these are listed under "Not counted".
- **Logged surplus:** `mark_spares`. 32 vehicles are "not needed" in all: 18 logged cars (on 3, 6, 7, 10, 13, 14, 15, 17, 23, 27, 28 and 30; 30 alone has 4) and 14 leftover free history cars (on 2, 22 and 88).
- **Designed cars (9):**
  - 2 (413, 461): the cycle need of 5 + 4 for 2 + 2P is above the 7 logged.
  - 18 (460, 465): no trolleybus history since 1 Sep; free battery 32 Tr, newest first.
  - 88 (192, 216): from line 8's history.
  - 16 (116): its weekend records.
  - 22 (113): its June records.
  - 90 (218): its September records.

  History means the days before the vehicle day only (records fetched on 29 Sep that are newer than 25 Sep are ignored). Every designed car is active in the register and not out anywhere on 25 Sep (checked against the day records and the overview). The picks cover the line's roster types first, then weekday records, then the latest date.
- **Schedule** (shared runfit, then the Brno bus requirement): every entry reproduces the whole 16:00–16:59 hour, from an exact pattern on the core or the hour, or else the hour's own minutes repeated hourly (DPMP timetables are irregular). An entry with at most 8 departures a day gets every 1440 with all of them. Every terminus is a turning loop or point, so every value is −1 min.
- **Pak:** one object per type exists, in `dpmpbilocervena` (the 32 Tr object is the black-front scheme of the 2023–25 cars). Full advert wraps (CVR) and side stickers keep the normal livery. Plain white ("bílá") is its own livery, so three objects are requested: 26Tr (329 on 5), Crossway LE City 12M (70 on 28) and Urbanway 12M (113 on 22, designed) in `bila` (see `pak_request.md`). No stand-ins.
- **No subcontractors:** every Pardubice city line in JDF and every record is DPMP's. The register has one depot, Dukla (`Duk`).

## How to update

1. **New timetable:** run `01_fetch.py --state <new> --jdf-download` (or point `jdf.sources` at newer exports another pipeline downloaded, and use `--jdf`), then set `jdf.export_date` and `network_date`.
   - Run `02_timetable.py` and check the version table and the classes. A line changing class (for example, line 20 gaining afternoon trips) needs `groups` / `line_t0` edits.
   - Run `03_network.py` and compare the Simutrans lines and needs with the previous state. `branches_forced` / `branches_dropped` override the rule for one line.
2. **New vehicles:** set `vehicles_date` and `records.days` (the last weekday with complete records, preferably a Friday), `register_date`, and `history.since` (about 4 weeks back). Then run `01_fetch.py --state <new> --records --register --history`.
   - Check the "Not counted" list: new note words go in `fleet.morning_notes` / `afternoon_notes`.
   - Check `pool_text` and `short_text` against the new counts.
3. **Pak:** when the pak session reports new objects, run `run.py --pak`. Requested marks disappear on their own; send any new `pak_request.md` to the session.
4. `python run.py --state <new>`, check the page with Playwright at 1400 and 390 px (sticky bar about 120 px at 390, no horizontal scroll), and republish to the artifact URL above.
