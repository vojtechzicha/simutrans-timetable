# MD-CR: Czech long-distance rail timetable sheet

> **ARCHIVED (user, 5 Oct 2026).** Work moved to local lines (012, 014, 235: `../local-rail/`). The page now lives in `archive/MD-CR.html`; the renderers write there. The artifact https://claude.ai/artifact/DH4KCxqbx1KLvVvnxUNAQL is left as it was (version 16). Don't continue this sheet unless the user brings it back.
>
> Open points at archiving:
> - The user's game had LE Bohumín (LE1/2) still on every 240. It should be 480 (Praha 83, Přerov 245, Bohumín 329, Přerov 397).
> - The fork source (`simline.cc`) counts slots from midnight. The user's LE 1215 left Praha at 21:23 on offset 323/480, which fits the midnight rule; the sheet labels it 22:23 under the −60 rule. Not resolved.

## v4 (3 Oct 2026, current): simplified, game-friendly

The user asked for a "gamey", more compact model. They wanted the same kind of simplification as 010/260 and Nymburk, while keeping some variety.

**Network:** 8 clock-face lines, 29 vehicles. Design in `assets/v4_lines.json`; built by `scripts/13_simple.py`, then `scripts/12_render.py v4`.
- Every operator leaves Praha every 2 h:
  - Ex1 S:08, Ex2 L:08, SC L:31, RegioJet L:21 from Zahradní Město, Leo Express S:23.
  - Branches run every 240 min and alternate within the operator.
- **Lines end at the first station after the border** (user). That station is the game's end for the city beyond:
  - Čadca: Ex1 and RegioJet, for Žilina and Košice;
  - Chałupki: Ex1, for Warszawa;
  - Zebrzydowice: Leo Express, for Kraków;
  - Púchov: Ex2, where most of its trains really end.
- **Vehicles** are counted on that basis.
  - The user checked that Ex1 Poland and Ex1 Slovakia come out equal: 3 vehicles each.
- **Each line copies one real train each way** (`rep_out`, `rep_in`). `slot_A`/`slot_B` move that train to the line's slot.
  - The line lists the real trains it stands for, and the ones folded into it.
- **Offsets:** (real − 60) mod interval, confirmed by the user for 120 and 240.
- **The EC Ostravan stays on Ex1, not on the SC line.** It has a different stop pattern, minute and terminus.

### Brno pass (4 Oct 2026)
**Scope:** the user chose ČD Ex3, plus RegioJet and Leo Express to the south. Not included: Ex4 and the Ex3 north through trains. R9 and R19 were added in a second pass (below).
**10_corridor.py** now also keeps trains that stop at Brno hl. n. or Břeclav.

**South ends.** Real times run up to the first station after the border: Kúty towards Bratislava, Hohenau towards Wien. From there each further station counts 10 min (`beyond` and `HOP` in 13_simple.py):
- Kúty – Bratislava – Budapest;
- Hohenau – Wien – Budapest.

**Lines** (5 new, 18 vehicles; MD-CR total 44):
| Line | Every | Praha minute | Vehicles |
|---|---|---|---|
| Ex3 Budapest via Bratislava | 120 | L:37 | 5 |
| Ex3 Wien | 120 | S:37 | 5 |
| RJ Budapest via Wien | 240 | ZM S:47, hours ≡0 mod 4 | 3 |
| RJ Bratislava | 240 | ZM S:47, hours ≡2 | 3 |
| LE Bratislava | 480 | 6:23, 14:23, 22:23 | 2 |

**Leo Express:** LE Bohumín changed to every 480 (2:23, 10:23, 18:23, 1 vehicle) and now alternates with LE Bratislava. To keep the 20-min Praha turn, the LE Bratislava return is modelled 3 h 13 min later than reality.

**Focus on rychlíky and Leo Express (user, 4 Oct 2026).**
- **Ex, SC and RegioJet lines are frozen.** They carry `"hidden": true` in `v4_lines.json`; their old overview sections and not-modelled items are hidden too (`not_modelled_hidden`). 12_render.py skips them.
  - **Do not edit them.** `meta.title_all` / `meta.intro_all` keep the old page title and intro.
- **Leo Express is back on the page,** unchanged. All LE Bratislava entries are every 480: the user's 207-min delay at Břeclav came from Bratislava and Kúty typed in as 240.
- **R lines are timed at important stations only** (`timed` per line): the hl. n. termini both ways, stays of 5 min or more, and the stop before Brno hl. n. R9 adds Kolín, Havlíčkův Brod and Tišnov.
  - An every-stop version was rejected.
- **Depot rule.**
  - **Praha** (user's option 1): the real trains start and end their passenger run at **Praha-Vršovice**. In the data they come from and go to the depot Praha Jih. The line runs Praha odstavné nádraží – Praha-Vršovice – Praha hl. n. on those real times, read from the raw `trains.json` locations (`depot.real`, `real_depot_ends()`).
  - Vršovice is timed both ways as the real terminus, and Praha hl. n. as an important station.
  - **Brno** (the real trains start and end at Brno hl. n.): the 15 min cover the dwell and the run together. The depot departs at the hl. n. departure − 15 and is reached at the hl. n. arrival + 15. No dwell is invented.
- **Engine note.** In the fork source (`simline.cc`), slots are counted from midnight: offset = minute of day mod interval. The sheet uses the user-confirmed (time − 60) mod interval. A constant shift keeps each line consistent, but it moves every line by 1 h against the clock if the source is right.

**R lines Praha – Brno (4 Oct 2026, second pass).** The user asked for the two R lines between Praha and Brno and to consider branches. Total 57 vehicles.
| Line | Every | Hub departures | Vehicles |
|---|---|---|---|
| R9 Praha – Havlíčkův Brod – Brno | 120 | Praha hl. n. S:04, Brno hl. n. S:13 | 6 |
| R9 Havlíčkův Brod – Brno (branch) | 240 | Havlíčkův Brod L:01, Brno hl. n. L:13 | 2 |
| R19 Praha – Česká Třebová – Brno | 120 | Praha hl. n. L:58, Brno hl. n. S:56 | 5 |
- **Depot ends.** Both ends run from and to "Praha odstavné nádraží" and "Brno odstavné nádraží", 15 min beyond the hl. n. This is `depot` in `v4_lines.json` and `depot_ends()` in 13_simple.py.
  - The real trains start and end at Praha-Vršovice, which is dropped.
  - The 15 min include the dwell at the hl. n. (third pass; the second pass invented 5/3 min dwells at Brno, and the user rejected them).
  - The depot runs cost R9 2 vehicles and R19 1 compared with turning at the hl. n.
- **The R9 branch** carries the off-hour R9 trains: 971, 974, and the peak extras 985/978. Together with R9 it gives Brno – Havlíčkův Brod the hourly peak service. It was my recommendation; the user may drop it.
- **Not modelled:** R 861 Česká Třebová – Brno (one train), and the other Brno R lines (R8 RegioJet, R11, R12, R13).

**Stop before Brno hl. n. (user, 4 Oct 2026).** On the lines via Brno (`time_before` in `v4_lines.json`), the stop before Brno hl. n. gets a timed entry in each direction, at its real departure.
- Do **not** move any of the Brno stay onto that stop. An earlier `move_wait` did that by cutting Brno to 1 min, and the user rejected it.
- Brno hl. n. keeps its real stay. It is timed by the usual rule (5 min or more).

## v3 (3 Oct 2026, replaced by v4): Praha – Ostrava corridor and Ex2, designed with the rail design rules

The user asked for MD-CR to be redone with the careful method from the local lines (`../rail-design-rules.md`).
They want only Ex1 and the other ČD IC/EC/SC trains between Praha and Ostrava, plus Ex2, RegioJet and Leo Express.
The pass covers only trains via Ostrava; trains via Brno come later.
Foreign ends are limited to Warszawa, Kraków, Žilina and Košice, and they are timed from the first station after the border.
The page is simple: chat-style tables, no fleet.

Steps:
- `scripts/10_corridor.py` writes `data/derived/corridor.json`. It holds every train that runs on all five days of `config.json` `v3_week` (5–9 Oct 2026) and stops at Ostrava-Svinov, Ostrava hl. n., Bohumín or Havířov, or is on Ex2.
- `assets/v3_lines.json` is the design, one entry per Simutrans line:
  - the real train numbers out and in;
  - the foreign legs with their sources: vagonweb.cz 2026 routes, the Leo Express table valid 30 Aug – 24 Oct 2026, and estimates marked in the notes;
  - the "Not modelled" list.
- `scripts/11_design.py` merges the Czech and foreign stops and derives:
  - the timed stops: termini, the first station after the border, and every stay of 5 min or more;
  - the offsets: (real time − 60) mod interval, i.e. odd hours first;
  - the round trips and vehicles. Daily lines pair each terminus arrival with a departure for the least total waiting.
  - It writes `data/derived/v3.json` and `_v3.txt`.
- `scripts/12_render.py` writes `MD-CR.html`. Its style is in `assets/simple.css`.

Design decisions:
- Lines with a few trains a day use interval 1440 with "Also at", so they run exactly the real trains. The user still has to confirm the 1440 offset convention.
- Ex2 runs to Žilina although most real trains end at Púchov.
- The SC line is the 2-hourly Pendolino slot Praha – Ostrava hl. n. Its Bohumín extensions and the Ex6/Ex7 through trains are listed as not modelled.
- Each RegioJet and Leo Express end is its own line.

Update: for a new timetable, re-run `run.py`. Then check every train number in `assets/v3_lines.json` against `_corridor.txt`, and refresh the foreign times.

## v2 (29 Sep 2026, replaced)

Output: `MD-CR.html` in the project root. It covers every R, Ex, IC, EC, SC, rj, RegioJet and Leo Express train in the
Czech Republic, grouped by peak line, with the fork's Simutrans schedule for each Simutrans line.
**Timetable only.** The user asked for no vehicles and no depots (29 Sep 2026). Local trains (Os, Sp) are not included.

Built 29 Sep 2026 by session simutrans-timetable-b2. The rules were checked with sessions 5a, 3a, a2, b5 and the engine session 122-0-58 that day.

## Source
- CIS JŘ national rail timetable: `ftp://ftp.cisjr.cz/draha/celostatni/szdc/<year>/JR<year>.zip`, with one CZPTT XML file per train.
  It is stored in `data/raw/jr2026/`.
- The monthly folders (`2026-09/` …) hold engineering-work variants and cancellations, and they are ignored.
  The shared rule is that short-term closures are modelled as the regular state.
- Service day: `config.json` `service_day` (2026-09-29, a Tuesday). A train runs on that day when its `BitmapDays` bit is set,
  with day 0 = `ValidityPeriod/StartDateTime`.

## Codes found in the data
- CommercialTrafficType values: 50 EC, 63 IC, 69 Ex, 70 EN, 84 Os, 94 SC, 122 Sp, 157 R, 209 rj, 9001 TLX, 9002 TL, 9003 LE,
  9004 RJ, 9006 NJ, 9010 ES.
- `CZPassengerServiceNumber` is the state line number (1–7 and 32 = Ex lines, 8–31 and 94 = R lines, 5902 = Trilex regional).
  Commercial trains don't carry one.
- ResponsibleRU: see `config.json` `carriers`. RegioJet runs its Slovak and Austrian sections under 3949 and 3990.
- Passenger stop = TrainActivityType 0001, 0028, 0029 or 0030 (0030 = request stop). 0002 is a technical stop, and CZ02 is not a stop.
- A location's CommercialTrafficType describes the train **from** that location, so the last stop has none.
  A stop counts as long-distance when the train arrives or departs there in an included category.

## Steps (`python scripts/run.py [--fetch]`)
1. `01_parse.py` turns the zip into `data/derived/trains.json` (every train file, all locations).
2. `02_trips.py` keeps the trains running on the service day that are in an included category, cuts them to their Czech
   stops, and writes `trips.json`. It writes the excluded trains to `excluded.json`: night trains, TLX, and IC trains
   with only Bohumín in the Czech Republic.
3. `03_lines.py` sorts trips into lines. A trip goes to a state line when at least half its stops carry a line number
   (the majority number wins); otherwise it goes to a commercial line (carrier group + corridor: via Brno or Břeclav = `BRV`,
   via Olomouc, Ostrava or Bohumín = `OVA`). A variant is an unordered pair of Czech termini. The A end is Praha, else
   the biggest hub, with overrides in `overrides.json` `line_A`. Output: `lines.json`.
4. `04_schedule.py` applies the rail rules below and writes `schedule.json` and `_schedule_summary.txt`
   (a plain-text summary to diff after an update).
5. `05_render.py` writes `MD-CR.html`, with station names expanded through `assets/names.json`.

## Rail rules (revised 29 Sep 2026 on the user's feedback; branch rules agreed with sessions 5a, 3a, a2 and b5)
- **Practical standard, not one hour:** each terminus gets the common clock-face pattern of the afternoon, 12:00–19:59.
  - The headway comes from 1 h, 2 h or 4 h (30 min only where trains run that often).
  - The minute is the one most departures keep within ±5 min.
  - Each departure kept counts 1 and each standard slot without a train counts −0.75; the best headway wins.
  - One slot per terminus, no Also at.
  - The sheet says "exact" only when every train keeps the minute; otherwise "approximate, up to N min off".
    It lists departures off the standard and slots without a train.
- **One headway per Simutrans line:** chosen on the afternoon departures of both ends together (the headway with the best summed score), then each end takes its best minute at it; ties go to the minute nearest 16:30. User correction 29 Sep: Kysučan (R Ostrava – Žilina) is 4-hourly; letting the busier end decide made it 2-hourly because of one extra 19:21 train.
- **Rychlík trains under an Expres line number** (R Ostrava – Žilina, state line 1) form their own line, `R1-R`.
- **Branches:** the route with the most trips is always a Simutrans line. Another route is its own line when it has all of:
  ≥ 3 trips in 12:00–20:00, a departure in 14:00–18:00, and a clock-face rhythm (its own 1/2/4 h standard keeps ≥ 2 departures).
  This is the rail adaptation of the city short-working rule.
- **Chaining** (FIFO at the shared terminus, turnaround 15–240 min) decides between two forms:
  - One line with the shared terminus entered twice, only when trains switch branch at ≥ 75 % of turns (Plzeň 4).
  - Separate branch lines otherwise.
  - Between 30 and 75 % the result is "mixed": still separate lines, and the sheet calls it a modelling choice.
  - In JR2026 no line alternates strictly. Ex1 switches 3 of 6, R10 4 of 15, R17 11 of 17.
- **Tails** (routes below the threshold): their departure minute from the shared terminus is folded into the modelled line (◇).
  The tail itself is listed with its trains, never dropped (the majority view: 5a, 3a, b5; a2 preferred listing only).
- **Foreign terminal (user):** when ≥ half of a line's trains cross the border at one end, the line is designed on to their most
  common foreign terminal (`assets/foreign.json`). The data sometimes names a stabling point (Grochów, Langenfelde),
  so the sheet names the city and the stabling point.
  - The foreign entry gets Departure every 0, because the Czech data has no times abroad.
  - The train is held at the last Czech station.
  - Other foreign terminals are listed as tails abroad.
- **Long stops (user):** per direction, flag the stops below, and give each one a timetable entry at the line's headway (the standard of its departure minutes):
  - passenger stops of ≥ 5 min;
  - stops without passengers of ≥ 2 min (TrainActivityType 0002, or any wait at a location with no passenger activity);
  - the stay at the border station before leaving or after arriving from abroad.

  A stop is flagged when at least half the trains, or at least 2, stay that long.
  - Examples: Ex1 Bohumín 29–39 min, Ex4 Bohumín 12–28 min, R17 Veselí nad Lužnicí 11–22 min, R9 Sázava u Žďáru 9 min (no passengers).
  - R17 stops at Tábor for only 2 min in JR2026.
- **Real minute:** rail termini keep it, with no −1 loop rule. Timetables go on the termini and the long stops only.
- **Leave up to:** automatic at 60 min or less, 30 min at longer headways (engine session advice).
- **Czech notation:** at 120 min, "every 2 h at L:07" (L = odd hours) and S (even hours).

## How to update
1. For a new timetable year (JR2027 from 13 Dec 2026), set `service_day` in `config.json` to a Tuesday–Thursday in the new
   year, then run `python scripts/run.py --fetch`.
2. Check the new codes: unknown CommercialTrafficType values or RUs show up in `02_trips.py` and in the line summary.
   Add them to `config.json`.
3. Compare `data/derived/_schedule_summary.txt` with the previous run.
4. Add any new abbreviated station names to `assets/names.json`. Search the page for "." inside names.
5. Re-publish `MD-CR.html` to the same artifact URL.
