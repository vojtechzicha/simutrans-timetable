# Most–Litvínov buses (DPmML): peak vypravenost sheet

Output: `Most-Litvinov Bus Vypravenost.html` in the project root (published at https://claude.ai/artifact/TUU9pmZU3fcjJK95Fe4ZPN; republish to the same URL).
Built by session simutrans-timetable-a2 on 29 Sep 2026. Shared rules for all cities are in `../README.md`.

This pipeline **imports, read-only**, the Most–Litvínov tram pipeline's helpers (`../most-litvinov/scripts/lib.py`:
WAF headers, seznam-autobusu parsers, the JDF 1.11 reader, the version rule, blocks, cycle_need, runfit, plans,
make_nm), `cycle_need_peak` from `../ostrava-trolleybus/scripts/lib.py` and `mark_spares` from
`../brno-trolleybus/scripts/common.py`. It never writes into those folders (most-litvinov belongs to session b5).

## What the sheet shows

- **17 DPmML lines in the 16:00 peak** (5, 9, 10, 12, 13, 14, 15, 16, 17, 20, 22, 23, 25, 27, 30, 31) plus **NAD**, the
  tram replacement buses Záluží, Chempark – Litvínov, Citadela: 19 Simutrans lines, **49 buses needed at 16:00**.
- **Every bus is designed, with a real fleet number** (nothing is logged, see below): 36 from the line's own history,
  11 from the line's home garage, 2 placed for fleet coverage (189 on the tram replacement, 153 on line 16), and 18
  more buses shown as "not needed" (history leftovers plus the 2 displaced buses 196 and 24).
- A "Lines at a glance" table near the top: line, Simutrans lines, buses needed, assigned (logged / designed), not
  needed. Every line has exactly its need (`04_roster.py` asserts it).
- Per line: variants, headway, 16:xx minutes, runtime; the Simutrans schedule (all termini −1 min); the buses as
  3-line cells (number · garage / full type · length / pak core) with the reason for each.
- Garages (Most, Litvínov), reserve by type, off-peak lines, the evidence table (every record and photo sighting), pak
  table, vehicle types, method. Sticky bar with line badges, garage counts, sections and a `#q` search (fleet numbers
  have 1–3 digits: 1–2 typed digits match the whole number, 3 match a prefix).

## Sources

| What | Where | Notes |
|---|---|---|
| Bus timetables | CIS JŘ bus export `https://portal.cisjr.cz/pub/jdf/JDF.zip` (export of 28 Sep 2026) | **Read by path** from `../ostrava-bus/data/raw/2026-09-29/JDF.zip` (config `jdf.bus_zip`), not downloaded twice. DPmML lines are 5750xx (Most) and 5760xx (Litvínov), IČO 62242504; `02_timetable.py` finds them by prefix + IČO. No other operator has a 575/576 line. |
| Tram timetables (for the replacement buses) | CIS JŘ city export `https://portal.cisjr.cz/pub/draha/mestske/JDF.zip` (25 Sep 2026) | Read by path from `../most-litvinov/data/raw/2026-09-28/JDF.zip`. Lines 575001/3/4. |
| Fleet register | `seznam-autobusu.cz/seznam?prov=1&trakce=autobus&iddopravce=399&vcetneSluzebnich=1` (1 page, 96 vehicles) | Depot cell: `Mos` Most, `Lit` Litvínov, `ZD-M`/`ZD-L` coach and contract fleet. |
| Records | `seznam-autobusu.cz/vypravenost/cr?datum=2026-09-25` (day overview) and `/vypravenost/cr/vypis?linka=<JDF number>` per line | seznam-autobusu logs JDF-numbered lines in its nationwide "cr" section (there is no Most slug). The day overview of Fri 25 Sep has **no** DPmML line. The per-line lists hold **29 records** in all (27 from Sep 2023, by plate; 1 from Sep 2024; 1 from a Saturday in Mar 2026). |
| Car pages | `seznam-autobusu.cz/vuz/<id>` for every active register car | Their own records (the same few) and their photo lists (date, place). |
| Photos | `foto-busy.eu-central-1.linodeobjects.com/<id>.jpg` | The newest photos of every city bus (up to 3 since 2024, else the newest since 2023): 107 images. The line on the destination display was **read by eye** into `assets/photo_lines.json` (114 entries incl. second buses in a photo; 66 with a line). |
| Operator | `dpmost.cz/zvd2026001` (tram closure), `/zvd2026002`, `/zvd2026006` (summer Jezero service, weekend double-decker), `/zvd2026016` (line 27), `/zvd2026020` (station forecourt from 1 Oct), `/doprava-zmeny`, `/vozovy-park` | Stored in `data/raw/operator/2026-09-29/`. |
| pak128 | `C:\Users\vojte\Developer\simutrans-custom-czech-pak128\build\VZ-DPMostLitvinov-bus\*.dat` (main b84c15c) | NB_12, SOR_NS_12, SOR_NB_18, SOR_NS_18, Citelis_18M, Urbanway_18M, Citelis_12M, E_Way_12M (demo); one livery `mostzlutocervena`. |

## Steps (`scripts/`, stdlib-only Python)

1. `01_fetch.py [--jdf] [--fleet] [--records] [--cars] [--photos] [--operator]` → `data/raw/<kind>/<snapshot>/`.
   About 1 request/s, browser User-Agent, nothing personal. `--photos` needs `03_fleet.py` first (it lists them).
2. `02_timetable.py` → `trips.json`, `versions.json`, `line_class.json`: DPmML lines, version per line for the
   service day (29 Sep 2026), class (peak = something on the road in 16:00–16:59); **the replacement-bus trips** =
   the Chempark – Citadela part of the tram trips of 1, 3, 4, at the tram minutes.
3. `03_fleet.py` → `fleet.json` (city flag and reason), `records.json` (plates matched to fleet numbers),
   `evidence.json` (per car: records, photo list, photo lines).
4. `04_needs.py` → `lines.json`, `needs.json`: branches by rule (as Ostrava buses; a loop line is a pair of one),
   need = `cycle_need_peak` (or a loop version), topped up to the buses on the road in 16:00–16:59.
5. `04_roster.py` → `roster.json`: designed buses (rules in its docstring), "not needed" history buses.
6. `05_schedule.py` → `schedule.json`: runfit per terminus, −1 min everywhere; sparse lines get a 15:00–20:00 fit
   where a pattern exists, else "Departure every 0" with the real departures.
7. `06_render.py` fills `templates/page.html` → the HTML in the project root.

`python scripts/run.py` rebuilds offline; `--fetch` refreshes the seznam-autobusu and dpmost.cz data first.

## Decisions

- **Vehicle day Fri 25 Sep 2026** (the tram sheet's day) is only nominal: no DPmML record exists for it, or for any
  weekday of 2026. **Network: the timetable in force on Tue 29 Sep 2026** (the service day for the JDF).
- **All buses designed** (user rule: never ship without vehicles; designed = real numbers from line history).
  Evidence = records + photo displays. A car's "own line" is the line of its newest evidence. Lines are filled from
  the largest need down; picks cover the line's history types first (most evidence first), then recency (own-line
  cars, then other history cars); then the home garage's free cars of the main type, no-evidence cars first.
  Leftover history cars: "not needed" under their own line. Home garage: the garage of most history cars, else
  `config.home_garage` (575xxx Most, 576xxx and NAD Litvínov).
- **Fleet coverage (user, 29 Sep 2026)**: every city-bus type AND livery of the active fleet must be on a line at
  16:00 ("put somewhere where other long buses are used, each type should be represented"). `04_roster.py` step 5:
  a missing type × livery puts one of its buses (newest evidence first) on its own evidence line if that is on the
  sheet, else a line of its home garage; articulated buses only on lines where articulated buses run; the
  weekend-only double-deckers on their own line 16 (it runs at 16:00), marked "normally weekends only". The bus
  replaces a designed bus of that line whose type × livery stays on the sheet without it (same type first, then a
  garage pick, then the oldest evidence); the displaced bus becomes "not needed" on that line. Result on 29 Sep:
  **189** (SOR NB 18, Prague red-white) on the tram replacement in place of 196; **153** (Lion's City DD, BVG yellow)
  on line 16 in place of 24. The other type × liveries were already on lines: NB 12 white-yellow-red and Prague
  red-white (83, line 30), NS 12, NB 18 white-yellow-red (194, line 30), NS 18 (97), Citelis 18M (98), Urbanway 18M
  (99). Advertising wraps count as the normal livery.
- **mark_spares** (logged surplus) is imported but has nothing to do: nothing is logged.
- **Not city buses** (`assets/types.json` `not_city` + register): coaches and contract fleet (ZD-M, ZD-L), service
  and museum buses, driving-school buses (120, 503), and the **double-deckers 153 and 154**, which since 1 May 2026
  run only on Saturdays, Sundays and holidays on line 16 (dpmost.cz/zvd2026006). They are left out of the roster but
  take part in the fleet-coverage step (`types.json` `weekend_only`), so one of them (153) is on line 16.
- **Tram replacement badge** reads "Tram replacement" (`config.nad.badge`, coordinator's change on publishing).
- **Replacement buses (NAD internally; the page shows the full name “Tram replacement”, `config.nad.badge`, because the sheets use no abbreviations)**: one Simutrans line, Chempark ⇄ Citadela, at the tram minutes (every 15 min at 16:00,
  tram line 4 only). The stop names are the tram stops of the JDF (the bus stops sit at or next to them;
  dpmost.cz lists the exact positions). Night line 40 is off the sheet.
- **Branches**: only line 5 splits (5A Okružní Shell, 5B Zázvorová, 2 buses each) and line 30 (30A Jezero Most every
  30, 5 buses; 30B the Nádraží – Nemocnice loop every 15, 4 buses). Line 13 is one Simutrans line on Janov ⇄ Loučná
  with 7 buses (the Osek and Lom, Československé armády trips are folded in).
- **Summer timetables** of 16 and 30 (to 30 Sep) are the ones in force on 29 Sep; from 1 Oct both change and the
  station forecourt closes (line 30 ends at Rudolická). Listed as not modelled.
- **Stop names** expanded (config `stop_name_expansions`): 1. náměstí, Československé mládeže/armády, 14. základní
  škola, rozcestí, náměstí Míru, městský úřad, Josefa Skupy, Zdeňka Štěpánka, Svatopluka Čecha, věžové domy, Karla
  Hynka Máchy, požární zbrojnice, odbočka Centrum, Prokopa Holého. Company names (MUS a.s., JOSEPH II, DUK, KSK) stay.
- **pak**: exact objects for every type in white-yellow-red; advertising wraps → normal livery. **Requested**
  (`pak_request.md`): NB_12 in Prague red-white (83, on line 30), SOR_NB_18 in Prague red-white (189, reserve), MAN
  Lion's City DD in BVG yellow (153 on line 16, 154 weekend only). Since the coverage rule, all three are on the sheet
  except 154.
- **Published** by the coordinator at https://claude.ai/artifact/TUU9pmZU3fcjJK95Fe4ZPN (republish to the same URL).
- **Open question**: dpmost.cz's own fleet summary (7 Apr 2026) lists no SOR NB 18 but 7 Citelis, 9 "City Bus" and 8
  Crossway LE, while the register lists 10 NB 18 (bought from DPP 2024–2026, photographed on the replacement
  service) and 1 Citelis 18M. The sheet follows the register.

## How to update

1. New timetable: store a fresh bus JDF (`01_fetch.py --jdf` puts it in `data/raw/jdf/<snapshot>/`) and point
   `config.jdf.bus_zip` / `tram_zip` at it; set `service_day`, `network_state_label`, `snapshot`.
2. `python scripts/run.py --fetch` (register, records, car pages, operator pages, new photos).
3. Read the line off every new photo (`data/raw/photos/<snapshot>/`, the ones missing from
   `assets/photo_lines.json`; `03_fleet.py` prints the count) and add them to `assets/photo_lines.json`.
4. Check dpmost.cz/doprava-zmeny: is Chempark – Citadela still run by buses? If trams run to Citadela again, drop
   `config.nad` handling (02_timetable) and the NAD notes. Update `network_state` and `line_notes`.
5. If seznam-autobusu ever logs DPmML lines for a weekday (check `records.json` `vehicle_day_lines`), switch the
   roster to observed vehicles and apply `mark_spares` to logged surplus, as on the Ostrava bus sheet.
6. `python scripts/run.py`, compare, and send the user the changes.

## Data snapshot

`data/raw/*/2026-09-29/`: fleet (register page), records (day overview + 25 line lists), cars (92 car pages, every active register car),
photos (107 images), operator (7 dpmost.cz pages).
