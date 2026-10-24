# Ostrava trolleybuses (DPO): peak vypravenost sheet

Output: `Ostrava Trolleybus Vypravenost.html` in the project root, published at
https://claude.ai/artifact/HFHXt2UZ1NE1SE6KYQAMXp (also in `config.json` → `artifact_url`;
republish to the same URL). Shared rules for all cities are in `../README.md`. The sister tram sheet is `../ostrava/`, and
this pipeline **imports its helpers** (`scripts/lib.py` loads `../ostrava/scripts/lib.py`): the WAF headers and parsers, the
JDF reader and version rule, `blocks`, `cycle_need`, `runfit`, `loop_shift`, `plans` and `make_nm`. A fix there applies here.

## What the sheet shows

- **Vehicle day:** Tuesday 29 Sep 2026, trolleybuses observed live at the afternoon peak (first sighting 16:29–16:50).
- **Network state:** 29 Sep 2026 (the JDF versions are valid 1 Sep – 12 Dec 2026, so they are the same as on the tram sheet's 27 Sep).
- **Per line:** branches, headway, departure minutes, battery section, the Simutrans schedule (all termini are loops, so
  departures are set 1 min early), and the trolleybuses: number · depot / full type · length (+ battery) / pak core, with the course.
- **Battery sections** table, **depot** table (one depot, with the live course, later lines and the Fri 25 Sep record),
  spares, Pak128 objects, vehicle types and method.

## Sources

| What | URL | Notes |
|---|---|---|
| Timetable | https://portal.cisjr.cz/pub/draha/mestske/JDF.zip | Trolleybus lines 915101–915109 (JDF 1.8). 915111–915113 are night lines and are excluded. Line 107 has two identical inner zips. |
| Fleet register | https://seznam-autobusu.cz/seznam?prov=1&trakce=trolejbus&iddopravce=133&vcetneSluzebnich=1 | Same WAF as for trams (`lib.HEADERS`). One page. Depot cell "TR" = Vozovna trolejbusů, Sokolská třída. |
| Day records | https://seznam-autobusu.cz/vypravenost/odis/vypis?datum=YYYY-MM-DD | tram-bus.cz **still feeds DPO trolleybuses** (unlike trams), class `car-on-line-trolley`. Rows give bus, first line, course and "přejezd na linky …" but no time, so they are a cross-check, not the roster. |
| Live feed | POST https://dashboard.dpo.cz/api/server (body in `01b_live_poll.py`) | `vehicleType` "troll". Gives vehicleNumber, routeID, serviceID (course), trip start/final stop, last stop and position. The trip start/final names do **not** follow the JDF branches (107 shows Bartovice ⇄ Hranečník), so the branch comes from the position. No history. |
| Battery sections | https://mhd-ostrava.cz/?s=nasazeni_parcialnich_trolejbusu, https://mhd-ostrava.cz/?s=tt_dedicna_michalkovicka, cs.wikipedia "Trolejbusová doprava v Ostravě" | JDF does not mark them. Hand-written in `config.battery_sections`. |
| Battery cars | same + https://mhd-ostrava.cz/?clanek=s27tr_iv&s=typ_vozu | 26Tr 3731–3740 and all 36Tr have traction batteries; the 27Tr (including the fourth generation 3813–3818) have supercapacitors only. `config.battery_cars`. |
| Disruptions | https://www.dpo.cz/aktualne/vyluky.html | Read by hand, in `config.network_state`. |
| pak128 | local repo `C:\Users\vojte\Developer\simutrans-custom-czech-pak128`, `build/VZ-DPOstrava-trolleybus/` (main b84c15c) | Objects 26TrSolaris, 26TrSolaris_partial (battery), 27TrSolaris (+_2), 36TrSolaris (battery), SolarisTrollino_12AC; all length 8, waytype road. In `config.pak`. |

## Steps (`scripts/`, stdlib-only Python)

1. **`01_fetch.py [--jdf] [--fleet] [--records]`** saves JDF.zip, fleet/p1.html and records_<date>.json for each day in `config.records.days`.
2. **`01b_live_poll.py <until ISO time>`** polls the live feed into `data/raw/<date>/live/<YYYYMMDD-HHMM>.json`: every 1 min from 13:00 to 19:30, otherwise every 10 min. **Start it before the peak on the vehicle day** (it has no history).
3. **`02_timetable.py`**: one JDF version per line on the vehicle day → `trips.json`, `versions.json`.
4. **`03_fleet.py`**: `fleet.json` (type from `config.type_rules`, battery flag), `records.json`, `live.json` (per bus: time, line, course, from, to, longitude, last stop).
5. **`04_roster.py`** (algorithm in its docstring):
   - It builds the branch tables and sizes each branch by `lib.cycle_need_peak`. This is the tram `cycle_need`, but it skips a round trip that would wait over 30 min for a return trip; without that, 107 to Hranečník came out at 5 instead of 3, because its return trips stop at 16:33 and its buses leave as 101.
   - The roster is the buses seen live in `config.live.window`.
   - On 101 and 107, the branch is decided by position: a bus seen east of longitude 18.322 (Hranečník) in `branch_by_position.window` is on the battery branch. A short branch takes surplus buses from the other one, and only battery buses may move onto a battery branch.
   - Any branch still short gets designed buses ("designed, not recorded"): an active car not seen at the peak, battery-capable where needed, preferring cars recorded on the line.
   - Last, it checks that every bus on a battery branch is battery-capable.
6. **`05_schedule.py`**: runfit per terminus, real minutes and the values to type in (−1 at loops).
7. **`06_render.py`** fills `templates/page.html` (the tram page's style plus battery styles).

`python scripts/run.py` runs steps 3–7 from the stored snapshot, with no network.

## Decisions (all in `config.json`)

- **Vehicle day = observed live day, not the tram sheet's Friday.** The Friday records exist (42 buses) but give no time, and the duties interline heavily, so a bus's line at 16:00 cannot be read from them. The live feed gives line and course at the peak moment. The timetable demand is flat 15:00–17:00, so observing at 16:29–16:50 is equivalent to 16:00.
- **Branches:** 101 (A Hranečník / B Radvanice, Ludvíkova, battery) and 107 (A Hranečník / B Bartovice, Ještěrka, battery) are two Simutrans lines each. The other lines have one branch; their depot runs to Vozovna trolejbusů are pull-ins (`pullin_branches`).
- **Interlining:** the duty groups hand buses between lines (1xx: 101/106/107, 2xx: 102/103/105/108/109, 8xx: 104 and 101). Each bus goes on the line it was working at the peak. No shared pools.
- **All termini are loops**, including the battery termini, so the schedule is set 1 min early everywhere.
- **Pak livery:** the pak has 26Tr/27Tr/36Tr only in dpotyrkysova and the Trollino 12 only in dpomodrozluta; other real paints are listed as nearest in the pak table. SOR TNB 12 has no object (≈ SolarisTrollino_12AC).
- **Stop names:** tram expansions plus trolleybus ones (Hornická poliklinika, Revírní bratrská pokladna, Léčebna dlouhodobě nemocných, …).

## How to update

1. On a normal weekday, start the poller before 15:00: `python scripts/01b_live_poll.py <date>T19:30` (in the background).
2. In `config.json`, set `snapshot`, `vehicle_day` (+ both labels), `network_state_day`/`network_state_label` and `live.label` to that date. Set `records.days` to the day and the previous Friday.
3. After 19:00, run `python scripts/01_fetch.py` (JDF, register and the day records).
4. Re-read the DPO výluky and battery news: update `network_state`, `battery_sections`, `battery_cars` and `line_notes`, and the JDF line list if it changed. If a new battery section or wire opens, also update `battery_branches` and `branch_by_position`.
5. Check the pak (`build/VZ-DPOstrava-trolleybus/`) for new objects, for example the 14 new battery 26Tr ordered in Oct 2025, and update `config.pak` and `type_rules`.
6. Run `python scripts/run.py`. Check the version choice, "need vs observed" per branch, "battery issues" (must be empty) and any designed buses.
7. Republish to the artifact URL.

## Data snapshots

- **`data/raw/2026-09-29/`:** JDF.zip (export of 28 Sep 2026 19:00), fleet/p1.html, records_2026-09-25.json and records_2026-09-29.json, and live/ (polled from 16:29 to 20:00 on Tue 29 Sep 2026).

## Schedule fit and sheet changes of 20 Oct 2026

- **Both ends at the same rate:** `plans` in the tram lib (`../ostrava/scripts/lib.py`) is shared. Where the two ends of a branch differ in departures per hour, or either end's exact run misses the peak band (15:30–17:30, overlap < 30 min, fewer than 4 departures (3 if hourly), interval not dividing 1440), every rate either end offers is tried exactly on both ends. Otherwise both ends get one even slot at the averaged rate, marked "approximate, up to N min off", with the real band minutes in the Fit column. A direction whose opposite direction is scheduled is never merged away (bus 27, Proskovice → Hrabová).
- **Rows to check:** an approximate row with more slots in 15:30–17:30 than real departures is marked on its card and listed under "Approximate schedules to check", with the slower alternative (`alt` in schedule.json). It is the owner's choice; switch both ends of a line together.
- **Display:** as on Prague, the typed Offset/Also at values carry the real minute under them (worked out from each typed value + 1 at loops), plus a Fit column. The Headway column shows the fitted pattern's gaps.
- Only 05_schedule and 06_render were rerun on 20 Oct; the roster (vehicles) is unchanged and identical to the published sheet.
- **Network state checked 20 Oct 2026:** line 106's Dědičná repair has ended. The schedule fit is unchanged (every pair already had the same rate and a run over the peak).

- **Needs come from the suggested pattern (user rule, 20 Oct 2026, all lines):** `pattern_need` in `ostrava/scripts/lib.py` follows a vehicle round the sheet's own schedule slots (real running times, at least the terminus layover) and counts the slots of one round. 05_schedule therefore runs before 04_roster. Lines without a timed pattern at both ends keep the timetable sizing. The variant extra (buses of unmodelled variants) is dropped.
  Trolleybus, 20 Oct 2026: every branch's timetable need already equals its pattern need (46), so nothing changed. The trolleybus 04 still sizes by cycle_need_peak; switch it to pattern_need if its schedules change.
- **Pak objects, 20 Oct 2026 (pak main 2cdf3f3):** 27Tr Solaris uses the paint to pick the livery (3805–3810 blue-yellow `dpomodrozluta`, 3811–3812 turquoise). The fourth-generation 3813–3818 use `27TrSolaris_partial` (Urbino IV body; engine_type electric, no battery; '27Tr (2024)' in game). The 27Tr rear section is length 6, per the dat.
