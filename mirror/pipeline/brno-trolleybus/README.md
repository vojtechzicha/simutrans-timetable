# Brno trolleybuses (DPMB)

The Brno trolleybus sheet is built from stored raw data by the scripts in this folder. It follows the tram sheet (`../brno`) and the shared rules in `../README.md`. The HTTP, GTFS, `cycle_need` and `runfit` helpers are imported from `../brno/scripts/common.py`, and so is the page style (`../brno/assets/style.css.html`). Only the paths, the state loading and the trolleybus additions live here.

| State file | Network | Vehicles | Output (project root) | Artifact |
|---|---|---|---|---|
| `states/2026-09-29.json` | from Tue 29 Sep 2026 (same as 25 Sep and 2 Oct) | Fri 25 Sep 2026 | Brno Trolleybus Peak Fleet.html | https://claude.ai/artifact/NdYdvPQK1v2sVZ8cGmoW81 |

```
cd pipeline/brno-trolleybus/scripts
python run.py --state 2026-09-29
```

Python 3, standard library only. Maintained by session simutrans-timetable-3a (Prague trolleybuses: simutrans-timetable-5a; Ostrava trolleybuses: simutrans-timetable-f5).

## Sources

| What | URL | Stored in |
|---|---|---|
| Vehicle per kurz, one page per line (21, 25–27, 30–39) | `https://www.bmhd.cz/vypravenost/vypravenost.php?datum=YYYY-MM-DD&linka=N` | `data/raw/vypravenost/<date>/L<N>.html` |
| Depot register: Komín `k`, Husovice `h`, Slatina `s` | `https://www.bmhd.cz/evidence-dpmb/vozovna/{k,h,s}` | `data/raw/register/<date>/voz_*.html` |
| Exact type + livery per vehicle | the `vozp.php?...trakce=trolejbus` listings from the depot pages | `data/raw/register/<date>/types_*.html` |
| Types of buses seen on trolleybus kurzy | the Slatina `trakce=autobus` listings holding those numbers (`01_fetch.py --bus-types 7010 7082`) | `data/raw/register/<date>/bustypes_*.html` |
| Timetable | IDS JMK GTFS, `route_type` 800 = trolleybus. The feed is shared with the tram pipeline: `common.gtfs_path` reads `data/raw/gtfs/<date>/` here if present, else `../brno/data/raw/gtfs/<date>/`. | `../brno/data/raw/gtfs/2026-09-28/gtfs.zip` |
| Battery sections, terminus layouts, line pools | dpmb.cz, cs.wikipedia (Trolejbusová doprava v Brně; Seznam trolejbusových linek v Brně), BMHD wire map 6/2015, bmhd.cz articles 1723 and “Kurzy a nasazení”, jrbrno.cz | in the state file (`battery`, `termini`, `pool_text`) |
| Pak objects | local pak128 checkout `C:\Users\vojte\Developer\simutrans-custom-czech-pak128\build\VZ-DPBrno-trolleybus` and `...-bus` (main b84c15c), read only | `assets/pak.json` |

The bmhd.cz firewall rules are the same as for the trams: browser headers and 2 s between requests (`common.fetch`).

## Steps

1. `01_fetch.py`: `--vehicles <date>` (all 14 lines, or `--lines`), `--register`, `--bus-types <cars>`, `--gtfs`.
2. `02_parse.py`: vypravenost → `data/derived/vypravenost_<date>.json`. Each row keeps its traction from the row class (`car-on-line-trolley` / `car-on-line-bus`). The register → `vehicles_<date>.json`.
3. `03_timetable.py --state X`:
   - Takes the trolleybus trips of `service_date`, without depot runs, and builds the network table.
   - For each Simutrans line in `simutrans_lines`, fits every stop entry. All entries share one rate: each entry's plain `runfit` gives a rate, the most common one wins, and a tie goes to the lower. An entry at another rate is refitted with `common.runfit_rate`.
   - Adds designed slots and applies loop −1.
   - Sizes the line with `common.circuit_need`: `cycle_need` generalised to N legs. It uses `turnarounds()`, the terminus's own shorter turnaround where the timetable shows one, and `links` for empty runs.
   - The 25 + 26 circuit is longer than the peak, so it runs on the peak pattern repeated every 20 min (`period`).
4. `04_fleet.py --state X`: picks the afternoon vehicle per kurz, marks buses, and assigns kurzy to Simutrans lines (`records` + `kurzy`).
5. `05_render.py --state X`: writes the HTML into the project root.

## Decisions

- **Day:** vehicles from Fri 25 Sep 2026, the last weekday before 29 Sep (28 Sep was a holiday). The same day as the tram sheet. Thu 24 and Tue 29 Sep have the same record counts per line, so gaps in kurz numbers are DPMB's, not missing records.
- **Pools (DPMB practice, confirmed by sources):**
  - **25 + 26** is one Simutrans line. 25 kurzy work every 26 trip, and bmhd.cz has no weekday 26 records. The circuit is Osová → Jírova → Nemocnice Bohunice → Štefánikova čtvrť (25) → Kamenný vrch → Štefánikova čtvrť → Kamenný vrch (26) → empty to Nemocnice Bohunice (5 min, `links`) → Pálavské náměstí → Osová (25).
    - All legs run every 20 min. The feed has no blocks: the circuit follows from matching arrivals and departures. Kamenný vrch has 6 arrivals and 3 departures an hour, and Nemocnice Bohunice has 3 more departures than arrivals.
    - The two Štefánikova čtvrť → Kamenný vrch entries are told apart by minute (`{"mod": 20, "keep": [4]}` and `[14]`).
  - **35 + 38 + 39** is one Simutrans line. DPMB has only 39 kurzy. The circuit is Preslova → Komenského náměstí → Barvičova → Mendlovo náměstí → Barvičova → Komenského náměstí → Preslova, all every 15.
- **Splits (choices):**
  - **30:** Klarisky branch = kurzy 1–13, Sadová branch = 15–27 (29 is morning only).
  - **37:** Nemocnice Bohunice branch = kurzy 1, 3, 4, 6, 8, 9; Jírovcova branch = the afternoon-only kurzy 10–13.

  The records don't name branches. Sizes come from the cycle (30: 6 + 5 needed, 7 + 7 out; 37: 4 + 4 needed, 6 + 4 out).
- **Line 33, designed slot:** Hlavní nádraží sends 9 an hour to Slatina, sídliště, but only 6 come back in the feed. The :14, :34 and :54 departures return out of service. A third return slot at real :12 every 20 is designed and marked on the sheet (`designed_slots`).
- **Loop −1 everywhere:** every terminus is a loop or a turn around a block (Česká, Komenského náměstí, Pálavské náměstí). As on the Prague trolleybus sheet and the tram sheets, a block turn counts as a loop. `nonloop` is empty.
- **Buses on trolleybus kurzy:** 27/3 (7082 Iveco Urbanway 12M CNG) and 31/7 (7010 Irisbus Citelis 12M CNG). They are listed with a “bus” mark and are not counted as trolleybuses.
- **Battery sections:** only 21 (Řípská – Letiště Tuřany, since 18 May 2026) and 30 (beyond Královo Pole, nádraží, since 27 Apr 2024). The rest is under wire. The pak objects are all `engine_type=electric` road vehicles, so battery sections are information only.
- **Fit core:** 15:30–16:30, the Brno tram value. The Prague trolleybus sheet uses 16:00–17:00. Tried here, it made 32 worse and changed nothing else, so the tram value was kept.
- **Surplus:** 25 + 26 needs 19 by cycle and had 25 out, so 6 are marked not needed; 27 needs 4 and had 5 trolleybuses + 1 bus out, so the bus and 1 trolleybus are marked (see Spares).
- **Spares (user, 29 Sep):** where more vehicles were logged than a Simutrans line needs, exactly the need stays counted and the rest is marked "not needed" (`common.mark_spares` in brno-trolleybus): one of every vehicle type of the line is kept first (most frequent type first; a substitute bus on a trolleybus line is no type and goes first), then afternoon-only kurzy and the highest kurz numbers are dropped first. Not-needed vehicles are dimmed at the bottom of their card and left out of all counts, the depots and the pak totals. This replaces the earlier "operator's slack" rule.

## How to update

1. **New timetable:** refresh the GTFS in the tram pipeline (`../brno/scripts/01_fetch.py --gtfs`), or here with `01_fetch.py --gtfs`. Copy the state, set `gtfs_date` and a Friday `service_date`, and run `03_timetable.py`.
   - Check the printed rates and spans.
   - Check the 25 + 26 and 35 + 38 + 39 legs: a changed frequency breaks the circuit, and `circuit_need` then returns nothing.
   - Check the 33 imbalance (`designed_slots`).
2. **New vehicles:** run `01_fetch.py --vehicles <Friday> --register`. If `02_parse.py` reports non-trolley rows, add `--bus-types <cars>`.
   - Set `vehicles_date` and `register_date`.
   - Re-check the 30 and 37 kurz splits against the new kurz numbers.
3. `python run.py --state <new>`, then re-publish to the same artifact URL.
4. **Shortfalls:** if `04_fleet.py` ever leaves a Simutrans line short, design the missing vehicles by the user's roster rule (pipeline/README.md, "Roster coverage and spares"): take the line's history roster, first one free car of each type the used cars lack, then fill by recency. Show the leftover free history cars as "not needed" rows. On 29 Sep no line was short, so no vehicles were designed.
