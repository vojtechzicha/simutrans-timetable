# Ostrava trams (DPO): peak vypravenost sheet

Output: `Ostrava Tram Vypravenost.html` in the project root, published at
https://claude.ai/artifact/4JYPMdmaxEzKhkxg37fd8e (republish to the same URL).
Shared rules for all cities are in `../README.md`; this file holds only what is specific to Ostrava.

## What the sheet shows

- **Vehicle day:** Friday 25 Sep 2026, trams at 16:00.
- **Network state:** as of Sunday 27 Sep 2026.
- **Per line:** branches, headway, departure minutes, the Simutrans schedule (fork fields, loop termini 1 min early), and the trams with number, full type and pak128 core.
- **Per depot:** Poruba and Moravská Ostrava, each with line | vehicle | course seen live.
- **Also:** spare fleet, the Pak128 objects table and the method notes.

## Sources

| What | URL | Notes |
|---|---|---|
| Timetable | https://portal.cisjr.cz/pub/draha/mestske/JDF.zip | CIS JŘ city export, one inner zip per line version. DPO trams are lines 915001–915017 (JDF 1.8). 915018/915019 are night lines and are excluded. No login, about 30 MB. |
| Fleet register | `https://seznam-autobusu.cz/seznam?onlyCurrentDepot=1&depotId={534 Poruba, 616 Moravská Ostrava}&prov=1&trakce=tramvaj&iddopravce=133&vcetneSluzebnich=1` | WAF: needs a full Chrome User-Agent plus Accept and Accept-Language headers (see `lib.HEADERS`), and 2 s between requests. Pages use `&page=N`. The row CSS class is the state: `zar` active, `dilny` in workshops, `doco` out of service. |
| Allocation history | `https://seznam-autobusu.cz/vypravenost/odis/vypis?linka={line}&strana=N` | Same WAF. Fed by tram-bus.cz until **26 Jun 2026**, with nothing for DPO trams since. Kept as a school-year prior. Notes like "odpoledne", "ráno" and "přejezd na linku X" are used. |
| Live feed | POST https://dashboard.dpo.cz/api/server with body `{"endpoint":"transport/vehicle/list?page=dashboard&withTripId=1&vehicleStates=ride","apiMethod":"GET","data":{},"host":null}` | No headers needed. Gives vehicleNumber, routeID (line) and serviceID (course). **No history**, so it must be polled (`01b_live_poll.py`). |
| Disruptions | https://www.dpo.cz/aktualne/vyluky.html | Read by hand; its conclusions are in `config.network_state`. |
| Fleet changes | https://mhd-ostrava.cz/ | Read by hand (for example, T3R.P 962, 975, 983, 1015 were offered for sale on 17 Sep 2026). |
| pak128 | pak128 session `simutrans-custom-czech-pak128-77` | Object chains, liveries and lengths are in `config.pak`. |

## Steps (`scripts/`, stdlib-only Python)

1. **`01_fetch.py [--jdf] [--fleet] [--history]`** saves the raw inputs to `data/raw/<snapshot>/`: JDF.zip, fleet/<depot>_p<N>.html, and history.json (the parsed rows of the vypravenost pages; about 270 pages, around 10 min).
2. **`01b_live_poll.py <until ISO time>`** polls the DPO live feed into `data/raw/<date>/live/<YYYYMMDD-HHMM>.json`: every 2 min from 13:00 to 19:00, otherwise every 10 min. Run it in the background.
3. **`02_timetable.py`** picks one version per line and writes `derived/trips.json` (all trips on the vehicle day) and `versions.json`. The rule: among versions valid on the day, the latest valid-from wins, and ties go to the shortest validity. For 25 Sep this picks the 17 Sep – 19 Oct "Don Bosco not served" versions of 1, 2, 10 and 13.
4. **`03_fleet.py`** writes `derived/fleet.json`, `records.json` (weekday history records with weights) and `live.json` (car → line → courses).
5. **`04_roster.py`** works in three stages and writes `lines.json` and `roster.json` (the algorithm is in the script's docstring):
   - It chains trips into turns (layover ≤ 40 min) and counts the turns at 16:00: this is the unit count per line.
   - It allocates types per line from the history shares, capped by active cars minus a reserve, and picks cars by score.
   - It splits each line into its **branches** (`config.branches`; each branch is one Simutrans line) and sizes each by **cycle_need**: one tram followed round the branch at 16:00, with a 3 min layover, or the terminus's own shorter timetabled turnaround (`min_turnaround`). Every branch gets at least its need, and extra units are shared out by need. If a line has fewer units than its branches need, cars are **added**, marked on the sheet: the best-scoring unused active car of the line's main type.
6. **`05_schedule.py`** writes `derived/schedule.json`, fitted with the shared **runfit** rule (see `../README.md`), with the de-duplication fix from 28 Sep 2026. It stores the real minutes and the values to type in (real − 1 at loops). **Both ends of a Simutrans line send the same number of trams an hour** (user, 18 Oct 2026): where the two ends' fits differ (line 4 Hranečník was every 20 before 16:15 and 4 an hour after; line 5 had 3 and 4 uneven slots an hour), every rate either end offers, or the real 16:00 hour, is fitted on both ends, and the rate with the longest combined exact runs wins. The replaced fit is kept as `refit` and shown in the Fit column.
7. **`06_render.py`** fills `templates/page.html` and writes the HTML to the project root. Each vehicle is shown as a 3-line cell: numbers · depot / full types · length / pak core. Each line card has one sub-heading per Simutrans line ("N assigned, M needed"), schedule rows grouped per Simutrans line, and the depot tables grouped per line and branch. The schedule table follows Prague: the typed Offset and Also-at values carry the real minute underneath (“real 15”), and a Fit column gives the exact run, departures outside it and any refit. The Headway column shows the gaps of the fitted Simutrans pattern (e.g. 10/20 on 4A, where 4B fills the gaps), or the timetable's commonest gap if that direction is not scheduled.

`python scripts/run.py` runs steps 3–7 from the raw snapshot with no network. `--fetch` also refreshes JDF and fleet first, and `--history` re-scrapes the history too.

## Decisions and overrides (all in `config.json`)

- **Peak moment:** 16:00 (`peak_minute` 960). The table window is 15:00–17:00. The fit uses core 15:30–16:30, search 13:00–20:00 (`config.fit`), and a branch needs ≥ 3 trips in 15:00–18:00 to be scheduled.
- **Branches:** lines 4, 7, 8 and 17 are split into Simutrans lines A and B (`config.branches`, reason in `branches_why`). Chaining in arrival order, in-service trips only, shows 8 and 17 keeping to one end. On 4 and 7 the ends mix irregularly, and none alternates strictly A–B–A–B, which is what the one-line exception (Plzeň 4) needs. The real minutes are kept, so the branches interleave as in the timetable.
- **Shared pools:** none at the peak (`shared_pools`). Lines 1 and 2 share course numbers and swap trams at Hlavní nádraží at some time of day (weekday records; on the holiday of 28 Sep every tram alternated). But at the weekday peak each line turns there in 3 min, against 8 min for a swap. The user's rule (18 Oct 2026) is the **shortest wait at the terminus**, so they stay separate (15 trams, not 16). The circuit is ready in `config.circuits_off` (with `circuits_why`), and `04_roster.py`/`06_render.py` support it: rename the key to `circuits` only if a weekday-peak live poll shows the swap.
- **Evening courses and coupled pairs (user, 18 Oct 2026):** 9xx courses are late-evening runs (`history.exclude_course_prefixes`) and are left out of the type history. Line 7's own 7xx courses ran a single Vario LF once in ~1,000 records, and its single cars (1359, 1368) appeared only on 918/919/921. 1359 by day ran coupled (1360 + 1359 on 707). Coupled pairs (Vario or T3R.P) now stay pairs on every line; before, they were split into singles everywhere except 1 and 2.
- **Rebase, fewest moves (`04b_rebase.py`, `keep_roster`):** the published roster (`data/published/roster_2026-09-28.json`) is what the owner built in the game. 04b keeps it and replaces only units whose type is under `coverage_min_share` of the line's corrected records. Coupled Vario pairs on 1 and 2 are kept. On 18 Oct this was 5 swaps: 7B 1359 → 1758 and 1368 → 1771 (39T), 4B 1361 → 1211 (Astra), 8B 1362 → 1756 (39T), and 2 Astra 1207 → 1511 (KT8D5R.N1; its Astra records on line 2 were evening runs only). A full rebuild without the rebase moves 16–22 trams, so keep `keep_roster` until the owner rebuilds Ostrava from scratch.
- **Live snapshot cut-off:** `live_until` = 20260928-1912. The poller kept writing until 23:36 after the sheet was built; the later snapshots shuffled single Vario LF picks. The cut-off reproduces the published roster exactly.
- **Round-trip need vs chaining:** with per-terminus turnarounds, every line has at least its need, so there are no added cars on 25 Sep 2026. The mechanism stays for future timetables.
- **Pull-in branches, not scheduled** (their minutes are merged into the main branch): lines 10 and 13 → Moravská Ostrava, Plynárny, the late-afternoon run-in towards the depot, and line 5 → Poruba, vozovna.
- **Every Ostrava terminus is a loop**, so every departure entry is set 1 min early.
- **Types not planned:** T3R.P. The 8 survivors are hardly used in 2026; history records of them count as Vario LF (on the 2×T lines 1 and 2, as a coupled Vario LF pair).
- **2×T lines:** 1 and 2. Single Vario LF records there become coupled pairs.
- **Reserve per type:** none if the type has fewer than 4 cars, otherwise max(1, round(8 %)).
- **Register overrides:** a car marked in workshops or out of service that is seen running in the live feed counts as active.
- **Stop names:** every JDF abbreviation is expanded (`stop_name_expansions`), for example Mor. → Moravská Ostrava and NH → Nová huť.
- **pak mapping:** full type → object family, liveries, parts and whether it is exact. The livery follows the register's paint (`paint_rules`: blue with white stripe → dpotyrkysova; blue-white-yellow and the old yellow-door scheme → dpomodrozluta; silver-gold → stribrna). Advertising wraps use the type's first livery and are listed as nearest.
- **Line notes and network-state cards:** hand-written in `line_notes` and `network_state`.
- **The roster is designed, not observed:** no public record for 25 Sep exists. The method text says so; edit `templates/page.html` if the situation changes (for example, when an observed live day replaces it).

## Roster coverage and spares (user rule of 29 Sep 2026, applied by session simutrans-timetable-b5)

- **Not needed:** where a Simutrans line (branch) has more units than its need, exactly the need is counted. The rest are "not needed", shown dimmed but not counted, and left out of depot and pak totals. The choice is Brno's `mark_spares`, imported from `../brno-trolleybus/scripts/common.py`: one of every unit type first, then the best-scoring picks. On 25 Sep, 14 units are not needed (8: 4, 2: 5, 1, 17: 2, 13, 5), so 95 units are counted instead of the 109 from chaining.
- **Type coverage:** every type of a line's regular roster must be among its counted units. A missing type swaps in its best free car for one unit of the line's most frequent type (flag `covers`). "Regular" means at least `coverage_min_share` (2 %) of the line's weighted records. A whole school year of history is full of one-off stand-ins, and the literal rule would put single 39T, Tango and Vario LF2 cars on the 2×T line 2. This threshold is a choice, stated in `config.coverage_why`.
- **Spares:** the active cars from the line's history that are not used anywhere are listed per line as "not needed", with their last date on the line.

## How to update when the timetable changes

1. In `config.json`, set `snapshot` to today's date. Set `vehicle_day` (+ both labels) to the weekday you want and `network_state_day`/`network_state_label` to the day the network state is taken from.
2. Run `python scripts/01_fetch.py --jdf --fleet`. Add `--history` only if seznam-autobusu has started receiving DPO tram records again; check https://seznam-autobusu.cz/vypravenost/odis/vypis?linka=8.
3. Optional but best: run `python scripts/01b_live_poll.py <date>T19:30` over a real weekday afternoon. Copy that day's `live/` folder into the snapshot, or point `snapshot` at that date, and the ranking will prefer cars actually seen on each line.
4. Re-read https://www.dpo.cz/aktualne/vyluky.html. Update `network_state`, `pullin_branches` and `line_notes`, and the JDF line list if lines were added or removed. Long-term closures are modelled; short ones are ignored.
5. Ask the pak128 session whether `VZ-DPOstrava-tram.pak` changed, and update `config.pak`.
6. Run `python scripts/run.py`. Check the printed version choice (one version per line, the expected validity) and the demand per line. Look for any "CLOSEST" schedule fit.
7. Republish `Ostrava Tram Vypravenost.html` to the artifact URL above.

## Data snapshots

- **`data/raw/2026-09-28/`:** JDF.zip (the export of 25 Sep 2026 19:54), the fleet pages, history.json (15,083 rows, 11,632 used after filtering) and live/ (the holiday of 28 Sep, polled from 16:42).
- **`data/raw/2026-09-29/live/`:** planned for the Tuesday weekday peak, but not in the folder (checked 18 Oct 2026). The only tram live data is the holiday of 28 Sep. A weekday-peak poll is still needed to settle the 1 + 2 question.

## Changes of 20 Oct 2026

- **Timetable from 20 Oct:** `config.timetable` points 02_timetable at `data/raw/2026-10-20/JDF.zip` and picks versions for Wed 21 Oct. The roster day stays Fri 25 Sep (`vehicle_day`, with the 28 Sep fleet, history and live snapshot). Don Bosco is served again by 1, 2, 10 and 13, and 10 and 13 no longer serve Dolní Vítkovice Hlubina. Departures and running times are identical to the closure versions, so the schedule, needs and trams are unchanged.
- **Network state checked on dpo.cz** (20 Oct): Hlučínská (to 31 Oct 2027) and the Náměstí Republiky stops still apply. The weekend and line 5 works of September have ended.
- **Shared fit rule:** see "Schedule fit and sheet changes of 20 Oct 2026" in `../ostrava-bus/README.md`. The tram schedule is identical under the refined rule.
- **Real minutes in the sheet** are worked out from each typed value + 1. They were listed in fit order, which mislabelled patterns that wrap past :00, e.g. trolleybus 101 Offset 19 was labelled "real 0".
- **04b_rebase.py** prints `WARNING need changed` if a new timetable changes a branch's need. The published branches are copied, so such a change must be handled by hand.

- **Needs come from the suggested pattern (user rule, 20 Oct 2026, all lines):** `pattern_need` in `ostrava/scripts/lib.py` follows a vehicle round the sheet's own schedule slots (real running times, at least the terminus layover) and counts the slots of one round. 05_schedule therefore runs before 04_roster. Lines without a timed pattern at both ends keep the timetable sizing. The variant extra (buses of unmodelled variants) is dropped.
  Tram, 20 Oct 2026: 95 → 93. Line 5 needs 2 (every 30, 60 min round; 1723 not needed). 8B needs 8 (1362 not needed, so the 1756 swap-in is dropped). 04b_rebase takes the needs from the fresh branches and marks extra units 'unneeded', dropping swapped-in units first.
