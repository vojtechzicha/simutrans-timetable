# Method check: PID Praha-východ (okres Praha-východ), 1–2 Nov 2026

The hand design of every line of the oblast (`lines.json`), checked step by step against the bus schedule method v4
(`mirror/pipeline/bus-schedule-method.md`), the design brief (`pid-regional/DESIGN_BRIEF.md`, with the pilot's lessons) and the
owner's corrections in `kb/lessons.md`.

- **Data:** PID GTFS of 1 Nov 2026, service day Mon 2 Nov 2026 (`data/derived/trips.json`), read over the whole day at the core
  points (`data/derived/reading/<L>.txt`; my compact views of the same data, and the generator of `lines.json`, in the session scratchpad's `praha-vychod/` folder). The live map of 2 Nov had only the
  early-morning buses when this was written (about 5:00–6:00): no afternoon plate chains. Every Step 5b statement below rests on the
  reading's 0-minute chain test; the decisions that the plates could change are collected in one owner check.
- **Step 4**, per timed leg: in the model window (anchor −30 to +90) the slots must equal the real departures ±1, and at least
  80 % of the slots need a real departure within 3 min; then most exact over the day, then the simplest. The numbers per leg below
  are the builder's (`05_schedule.py` via `run_oblast.py praha-vychod`, last run at the end of the session) and the audits
  (`audit-step4.md`, `audit-branch.txt`, `audit-path.txt`).
- **Typed values** are (real − 61) mod every (every terminus is a loop); the builder computes them. Checked by hand on one leg per
  line (for example 375 Brandýs :03 → typed 2; 335 Budějovická 16:06 and 17:20 on every 120 → (966 − 61) mod 120 = 65 and
  (1040 − 61) mod 120 = 19, typed 19, 65; 482 Rožkovo údolí 15:01 on every 480 → (901 − 61) mod 480 = 360).
- **Anchor:** the line's busiest 2 h in 13:00–18:00 or 16:00 (`line_anchor`); set by hand only where the window would otherwise
  hold extras on the line's own stops or the end of a pattern (the 282 / 305 precedent), each case named below.
- Every slot below is a real departure minute unless the line's text says otherwise (411 Brnky's 17:25; the 469 16:07 for
  16:04; the knot-read legs, whose terminal minute is the knot time minus the running time).

## Changed on 2 Nov, after the independent review (`review-2026-11-01.md`: 48 PASS, 7 FIX, 1 ASK)

Applied as the coordinator ruled; every changed line has its own "Changed on 2 Nov" entry below.
- **482:** the anchor owner check removed (the 15:00 anchor applies the busiest-two-hours rule); the 4-bus hourly alternative is in
  `notes`. No slot changes.
- **669:** out slots 15:05, 15:35, 16:05 (typed 4, 34, 64) instead of 15:35, 16:05, 16:35: 3 → 2 buses.
- **761:** the real :55 (typed 54) instead of :53, anchor 16:30 by hand; 15:50 listed 5 min off.
- **469:** the roadside owner check kept, as the coordinator ruled (unlike the review): the design brief collects roadside stops
  into one sheet-wide owner check with the bus cost, and the pilot kept its one. Reworded as that check; core point corrected to
  Strančice, Všechromy, náves.
- **397, 557, 671:** unmodelled reasons corrected (Modletice, rozcestí on 363; Světice, škola on 494; Podolanka on 375, the
  Jenštejn stops on 367, 376, 378 and 396).
- **Notes:** the pairings 379 / 367 → 669 / 666 at Brandýs, autobusové stanoviště, 321 → 657 at Mratín, 655 → 823 and 391 → 484 /
  823 at Úvaly (and 686 → 435 at Wolkerova) added for the live map.
- In-game change list: 669 Brandýs, autobusové stanoviště entry (every 120: Offset 34, Also at 64, 94 → Offset 4, Also at 34, 64;
  one bus fewer); 761 Todice entry (every 60: Offset 52 → 54). Nothing else changes in the game.
- Totals 128 → 127 buses, 68 Simutrans lines; owner checks 3 → 2 (411 Brnky; the sheet's roadside stops).
- **X391** (later on 2 Nov, coordinator: long works are modelled as they run): designed, every 60, Radlická čtvrť :23 / station :03,
  1 bus; the Radlická čtvrť coverage exception removed. In the game: a new line X391. Totals 69 Simutrans lines, 128 buses.

## Line by line


### 302 Praha,Letňany - Veleň, U Pomníku

- **Core points:** Praha, Letňany; Přezletice, Vinořská; Veleň, u pomníku. Model window 15:30–17:30 (the line's anchor).
- Whole day: Letňany → Veleň hourly :04 / :01 (9:04–19:04; 13:04 and 14:00 via Přezletice, Panská pole), Veleň → Letňany :36 / :32
  (8:38–19:35). Letňany → Vinořská :24 / :44 (14:24–18:44; peak mornings every 15–20), Vinořská → Letňany :12 / :52. One Simutrans
  line per destination; the Vinořská legs use `notvia` Veleň, because the Veleň trips pass Vinořská both ways.
- Panská pole (a stop the 671 school line also starts from) is put on 302's way back with `stops_via` (the 7:32 trip's path,
  about 2 min longer); putting it on the way out broke the real 2-min turn at Veleň (2 → 3 buses).
- Step 5b: 29 of 39 departures at Letňany follow a 158 arrival (city line, Prague bus sheet); the Veleň bus waits 57 min at
  Letňany in the game. Pooling 302 with 302 Vinořská could save a bus (owner option, not applied).
- **302** every 60, need 2 (waits Letňany 57, u pomníku 2):
  - Praha, Letňany → Veleň, u pomníku: slots :01, typed 0, running 29 min. Window: slots 16:01, 17:01 against real 16:01, 17:01 → Step 4 ok. Day 5–23: 4 exact, 12 within 3 of 14.
  - Veleň, u pomníku → Praha, Letňany: slots :32, typed 31, running 32 min. Window: slots 15:32, 16:32 against real 15:32, 16:32 → Step 4 ok. Day 5–23: 6 exact, 8 within 3 of 14. Off 12–20 h: 12:36, 13:37.
- **302 Vinořská** every 60, need 2 (waits Letňany 10/10, Vinořská 8/8):
  - Praha, Letňany → Přezletice, Vinořská: slots :24 / :44, typed 23, 43, running 20 min. Window: slots 15:44, 16:24, 16:44, 17:24 against real 15:44, 16:24, 16:44, 17:24 → Step 4 ok. Day 5–23: 12 exact, 13 within 3 of 23. Off 12–20 h: 13:34, 19:34.
  - Přezletice, Vinořská → Praha, Letňany: slots :12 / :52, typed 11, 51, running 22 min. Window: slots 15:52, 16:12, 16:52, 17:12 against real 15:52, 16:12, 16:52, 17:12 → Step 4 ok. Day 5–23: 9 exact, 13 within 3 of 24. Off 12–20 h: 14:04.

### 303 Praha,Černý Most - Křenice

- **Core points:** Praha, Černý Most; Šestajovice, Pražská; Praha, Újezd nad Lesy; Sibřina; Křenice. Model window 15:30–17:30 (the line's anchor).
- Every 30 all afternoon (Černý Most :03 / :33, Křenice :07 / :37 from 15:37; :04 / :37 before, the :04 trips via Sibřina, škola
  and Na Paloučku). 4 buses. Sibřina, škola is also on 765 (modelled).
- **303** every 30, need 4 (waits Černý Most 12, Křenice 17):
  - Praha, Černý Most → Křenice: slots :03 / :33, typed 2, running 47 min. Window: slots 15:33, 16:03, 16:33, 17:03 against real 15:33, 16:03, 16:33, 17:03 → Step 4 ok. Day 5–23: 13 exact, 16 within 3 of 26.
  - Křenice → Praha, Černý Most: slots :07 / :37, typed 6, running 44 min. Window: slots 15:37, 16:07, 16:37, 17:07 against real 15:37, 16:07, 16:37, 17:07 → Step 4 ok. Day 5–23: 9 exact, 19 within 3 of 27.

### 321 Praha,Letňany - Mratín - Brandýs nad Labem-Stará Boleslav

- **Core points:** Praha, Letňany; Veleň, u pomníku; Mratín; Brandýs n.L.-St.Bol., Pražská; Brandýs n.L.-St.Bol., nádraží. Model window 15:30–17:30 (the line's anchor).
- Brandýs, Pražská :04 hourly 14:04–18:04 (:10 at 11:10–13:10), Letňany :11 (14:11–17:11). The buses arrive at Brandýs, nádraží and
  leave from Pražská (two stops apart; no terminus alias, because nádraží is the terminus of five other lines). The builder sizes
  the line by following the bus (pattern_need). The morning Mratín / Polerady shorts are listed.
- **321** every 60, need 2 (waits Pražská (1) 7, Letňany (2) 20):
  - Brandýs n.L.-St.Bol., Pražská → Praha, Letňany: slots :04, typed 3, running 47 min. Window: slots 16:04, 17:04 against real 16:04, 17:04 → Step 4 ok. Day 5–23: 5 exact, 5 within 3 of 16. Off 12–20 h: 12:10, 13:10.
  - Praha, Letňany → Brandýs n.L.-St.Bol., nádraží: slots :11, typed 10, running 46 min. Window: slots 16:11, 17:11 against real 16:11, 17:11 → Step 4 ok. Day 5–23: 4 exact, 4 within 3 of 14. Off 12–20 h: 12:20, 13:05, 18:21, 19:18.

### 328 Praha,Opatov - Čestlice - Modletice

- **Core points:** Praha, Opatov; Čestlice; Dobřejovice, Na Návsi; Modletice; Modletice, Doubravice. Model window 15:30–17:30 (the line's anchor).
- 328 hourly (Opatov :25, Doubravice :03) and Opatov – Čestlice shorts hourly (Opatov :55, Čestlice :59); `notvia` Doubravice on the
  short legs. The short line waits about 50 min at Čestlice (as the timetable), so 2 buses; sharing the buses with 328 at Opatov
  (arrivals :34 and :12, departures :55 and :25) would need 3 for both, an owner pooling option.
- **328** every 60, need 2 (waits Opatov 51, Doubravice 9):
  - Praha, Opatov → Modletice, Doubravice: slots :25, typed 24, running 29 min. Window: slots 16:25, 17:25 against real 16:25, 17:25 → Step 4 ok. Day 5–23: 5 exact, 6 within 3 of 20. Off 12–20 h: 12:19, 13:19.
  - Modletice, Doubravice → Praha, Opatov: slots :03, typed 2, running 31 min. Window: slots 16:03, 17:03 against real 16:03, 17:03 → Step 4 ok. Day 5–23: 9 exact, 12 within 3 of 20.
- **328 Čestlice** every 60, need 2 (waits Opatov 43, Čestlice 53):
  - Praha, Opatov → Čestlice: slots :55, typed 54, running 11 min. Window: slots 15:55, 16:55 against real 15:55, 16:55 → Step 4 ok. Day 5–23: 4 exact, 4 within 3 of 12. Off 12–20 h: 13:49, 19:49.
  - Čestlice → Praha, Opatov: slots :59, typed 58, running 13 min. Window: slots 15:59, 16:59 against real 15:59, 16:59 → Step 4 ok. Day 5–23: 2 exact, 3 within 3 of 9. Off 12–20 h: 14:51, 18:51.

### 335 Praha,Budějovická - Kamenice

- **Core points:** Praha, Budějovická; Vestec, Šátalka; Jesenice [PZ]; Sulice, Hlubočinka, obchodní centrum; Sulice, Želivec; Kamenice, kulturní dům. Model window 15:30–17:30 (the line's anchor).
- Out of Budějovická every 30–35 min on two alternating routes (via Hlubočinka and Sulice: 14:05, 15:05, 16:06, 17:20, 18:20; via
  Radějovice and Křížkový Újezdec: 13:34, 14:40, 15:31, 16:33, 17:52); back about hourly (13:16, 14:23, 15:10, 16:24, 17:09, 18:38),
  each the long way round both routes (71 min). Outstation line (buses sleep at Kamenice; 10 of 21 arrivals there go on as 444).
  At the inbound rate every 120 with two slots each way: back 16:24 / 17:09 (also 14:23 / 15:10 within a minute); out two
  Hlubočinka trips 16:06 / 17:20, so Sulice, Hlubočinka (also on 337 / 339) is on the line, and the waits at Kamenice are 10 / 11
  min. FEWER on the out leg (2 slots, 4 departures): the outstation case. Rejected out pairs: 15:31 / 16:33 (a 107-min wait).
- **335** every 120, need 3 (waits Budějovická 60/31, kulturní dům 11/10):
  - Praha, Budějovická → Kamenice, kulturní dům: slots 13:20, 14:06, 15:20, 16:06, 17:20, 18:06, typed 19, 65, running 53 min. Window: slots 16:06, 17:20 against real 15:31, 16:06, 16:33, 17:20 → Step 4 FAIL. Day 5–23: 2 exact, 4 within 3 of 18. Off 12–20 h: 12:23, 13:34, 14:40, 15:05, 15:31, 16:33, 17:52, 18:20, 18:52, 19:51.
  - Kamenice, kulturní dům → Praha, Budějovická: slots 13:09, 14:24, 15:09, 16:24, 17:09, 18:24, typed 8, 83, running 71 min. Window: slots 16:24, 17:09 against real 16:24, 17:09 → Step 4 ok. Day 5–23: 2 exact, 4 within 3 of 11. Off 12–20 h: 13:16, 18:38.

### 343 Praha,Nádraží Klánovice-sever - Nehvizdy/Svémyslice

- **Core points:** Praha, Nádraží Klánovice-sever; Šestajovice, Balkán; Jirny; Jirny, Nové Jirny, hájovna; Horoušany, u rybníka; Nehvizdy, škola. Model window 13:40–15:40 (the line's anchor).
- Klánovice-sever – Jirny, Nové Jirny, hájovna hourly exact (:10 / :36). The Horoušany – Nehvizdy trips are the 344 buses'
  through-runs (below) and are modelled in the 344 circuit. 343 Zeleneč (every 480, 13:05 / 13:29, the real round) is the only
  service of Zeleneč, železniční zastávka. Anchor 14:10 (the line's own).
- **343** every 60, need 1 (waits Nádraží Klánovice-sever 20, hájovna 12):
  - Praha, Nádraží Klánovice-sever → Jirny, Nové Jirny, hájovna: slots :10, typed 9, running 14 min. Window: slots 14:10, 15:10 against real 14:10, 15:10 → Step 4 ok. Day 5–23: 7 exact, 7 within 3 of 12.
  - Jirny, Nové Jirny, hájovna → Praha, Nádraží Klánovice-sever: slots :36, typed 35, running 14 min. Window: slots 14:36, 15:36 against real 14:36, 15:36 → Step 4 ok. Day 5–23: 6 exact, 6 within 3 of 11.
- **343 Zeleneč** every 480, need 1 (waits Nádraží Klánovice-sever 440, Svémyslice 10):
  - Praha, Nádraží Klánovice-sever → Svémyslice: slots 13:05, typed 244, running 14 min. Window: slots none against real none → Step 4 ok. Day 5–23: 1 exact, 1 within 3 of 2. Off 12–20 h: 12:15. Knot check, model vs real (worst, min): Balkán 430.
  - Svémyslice → Praha, Nádraží Klánovice-sever: slots 13:29, typed 268, running 16 min. Window: slots none against real none → Step 4 ok. Day 5–23: 1 exact, 1 within 3 of 3. Off 12–20 h: 12:49. Knot check, model vs real (worst, min): Nádraží Klánovice-sever 111; Balkán 111.

### 344 Praha,Černý Most - Horoušany

- **Core points:** Praha, Černý Most; Šestajovice, u školy; Jirny; Horoušany, u rybníka; Nehvizdy, škola. Model window 15:30–17:30 (the line's anchor).
- 344 every 30 both ways (Černý Most :18 / :48, Horoušany :07 / :37). The chain test at Horoušany, u rybníka: every 343 trip to
  Nehvizdy leaves within 0–5 min of a 344 arrival (9 of 9) and 8 of 9 come back to a 344 departure: the :18 bus runs 344 → 343 →
  343 → 344 (arrive :50, Nehvizdy :57 / :00, leave Horoušany :07). Modelled as one circuit every 60 with Černý Most twice: Černý
  Most :18 → Horoušany → Nehvizdy → Horoušany → Černý Most, then :48 → Horoušany → Černý Most. 3 buses, against 4 for 344 plus a
  separate Nehvizdy shuttle (the Nehvizdy round fills the 17-min wait the bus has at Horoušany): the brief's cross-line circuit case
  (chain evidence, saves a bus), as the pilot's 581 Senomaty ring. The two 0-minute turns carry `lay` 0. The 343 extras at :20 /
  :30 (until 15:30) are off the pattern.
- **344** every 60, need 3 (waits Černý Most (1) 11, Černý Most (5) 11, u rybníka (2) 0, u rybníka (4) 0, u rybníka (6) 17, škola (3) 3):
  - Praha, Černý Most → Horoušany, u rybníka: slots :18, typed 17, running 32 min. Window: slots 16:18, 17:18 against real 16:18, 17:18 → Step 4 ok. Day 5–23: 6 exact, 6 within 3 of 9.
  - Horoušany, u rybníka → Nehvizdy, škola: slots :50, typed 49, running 7 min. Window: slots 15:50, 16:50 against real 15:50, 16:50 → Step 4 ok. Day 5–23: 5 exact, 5 within 3 of 11. Off 12–20 h: 12:17, 13:15, 14:20, 15:20.
  - Nehvizdy, škola → Horoušany, u rybníka: slots :00, typed 59, running 7 min. Window: slots 16:00, 17:00 against real 15:30, 16:00, 17:00 → Step 4 ok. Day 5–23: 5 exact, 5 within 3 of 10. Off 12–20 h: 12:10, 12:55, 13:30, 14:30, 15:30.
  - Horoušany, u rybníka → Praha, Černý Most: slots :07, typed 6, running 30 min. Window: slots 16:07, 17:07 against real 16:07, 17:07 → Step 4 ok. Day 5–23: 7 exact, 8 within 3 of 18. Off 12–20 h: 13:02.
  - Praha, Černý Most → Horoušany, u rybníka: slots :48, typed 47, running 32 min. Window: slots 15:48, 16:48 against real 15:48, 16:48 → Step 4 ok. Day 5–23: 6 exact, 8 within 3 of 18. Off 12–20 h: 12:38, 19:35.
  - Horoušany, u rybníka → Praha, Černý Most: slots :37, typed 36, running 30 min. Window: slots 15:37, 16:37 against real 15:37, 16:37 → Step 4 ok. Day 5–23: 7 exact, 8 within 3 of 13.

### 346 Praha,Černý Most - Brandýs nad Labem-Stará Boleslav - Praha,Černý Most

- **Core points:** Praha, Černý Most; Brandýs n.L.-St.Bol., Pražská; Brandýs n.L.-St.Bol., nemocnice. Model window 15:30–17:30 (the line's anchor).
- A one-way loop Černý Most – Brandýs – Černý Most, every 30 at :25 / :55 from 12:55 to 18:55. One leg Černý Most → Černý Most,
  exact 17 of 30; 2 buses.
- **346** every 30, need 2 (waits Černý Most 20):
  - Praha, Černý Most → Praha, Černý Most: slots :25 / :55, typed 24, running 40 min. Window: slots 15:55, 16:25, 16:55, 17:25 against real 15:55, 16:25, 16:55, 17:25 → Step 4 ok. Day 5–23: 17 exact, 18 within 3 of 30. Off 12–20 h: 12:05.

### 353 Praha,Černý Most - Brandýs nad Labem-Stará Boleslav/Horoušany,Horoušánky

- **Core points:** Praha, Černý Most; Praha, Čertousy; Zeleneč; Svémyslice; Brandýs n.L.-St.Bol., nádraží. Model window 15:30–17:30 (the line's anchor).
- Out of Černý Most every 30 at :13 / :43 all afternoon, to Brandýs on 13:43, 15:13, 16:13, 18:13 and to Svémyslice otherwise;
  back from Brandýs :22 hourly (13:22–17:22) and Svémyslice :10. Two Simutrans lines: 353 (Svémyslice, :43 / :10) and 353 Brandýs
  (:13 / :22). 353 Brandýs's out leg is read at Svémyslice (`core_to`): its 17:13 window slot is a Svémyslice short, which runs on to
  Brandýs in the game (a short turn on the line's own path, as the pilot's 304 Zličín shorts). The 353 back leg uses `notvia`
  Brandýs, nádraží so the Brandýs trips passing Svémyslice at :40 stay on 353 Brandýs.
- Rejected: Brandýs at :43 (only 13:43 is a Brandýs trip at :43). Real imbalance: 4 out / 5 back to Brandýs over 13–18 (buses
  reach Brandýs on other lines: 3 of 7 departures follow a 376 arrival there).
- 353 Mstětice (every 480) is the only service of Zeleneč, Mstětice (the Horoušánky trips 16:28 out; 7:24, 14:06 otherwise).
- **353** every 60, need 1 (waits Černý Most 13, Svémyslice 7):
  - Praha, Černý Most → Svémyslice: slots :43, typed 42, running 20 min. Window: slots 15:43, 16:43 against real 15:43, 16:43 → Step 4 ok. Day 5–23: 6 exact, 8 within 3 of 12. Off 12–20 h: 12:53.
  - Svémyslice → Praha, Černý Most: slots :10, typed 9, running 20 min. Window: slots 16:10, 17:10 against real 16:10, 17:10 → Step 4 ok. Day 5–23: 7 exact, 7 within 3 of 21. Off 12–20 h: 12:20, 14:55, 18:40, 19:40.
- **353 Brandýs** every 60, need 2 (waits Černý Most 13, nádraží 32):
  - Praha, Černý Most → Brandýs n.L.-St.Bol., nádraží: slots :13, typed 12, running 37 min. Window: slots 16:13, 17:13 against real 16:13, 17:13 → Step 4 ok. Day 5–23: 6 exact, 11 within 3 of 15. Knot check, model vs real (worst, min): nádraží 60.
  - Brandýs n.L.-St.Bol., nádraží → Praha, Černý Most: slots :22, typed 21, running 38 min. Window: slots 16:22, 17:22 against real 16:22, 17:22 → Step 4 ok. Day 5–23: 5 exact, 5 within 3 of 7.
- **353 Mstětice** every 480, need 1 (waits Černý Most 33, U Tří svatých 386):
  - Praha, Černý Most → Horoušany, Horoušánky, U Tří svatých: slots 16:28, typed 447, running 30 min. Window: slots 16:28 against real 16:28 → Step 4 ok. Day 5–23: 1 exact, 1 within 3 of 1.
  - Horoušany, Horoušánky, U Tří svatých → Praha, Černý Most: slots 15:24, typed 383, running 31 min. Window: slots none against real none → Step 4 ok. Day 5–23: 1 exact, 1 within 3 of 1.

### 354 Praha,Černý Most - Mochov

- **Core points:** Praha, Černý Most; Jirny, Logistický park; Nehvizdy; Nehvizdy, Mochovská; Mochov. Model window 15:00–17:00 (anchor set by hand).
- Hourly to Mochov (Černý Most :00, Mochov :31) and hourly to Nehvizdy, Mochovská in between (:30 / :06); the Mochovská legs use
  `notvia` Mochov. Anchor 15:30 by hand (window 15:00–17:00): the automatic 13:40 window is extra trips (Mochov 13:11, 13:41, 14:41,
  14:51; Jirny, LE&CO 13:30 / 14:20), and at 16:00 Mochovská's 17:01 is 5 min off :06. At Mochov 12 of 17 trips meet 662
  (Kolínsko sheet) within 0–5 min both ways: through-running across sheets, for the live map. 354 LE&CO (every 480, the real
  17:10 / 17:35 round) is the only line to Jirny, LE&CO besides two Mochov trips passing it.
- **354** every 60, need 1 (waits Černý Most 1, Mochov 4):
  - Praha, Černý Most → Mochov: slots :00, typed 59, running 27 min. Window: slots 15:00, 16:00 against real 15:00, 16:00 → Step 4 ok. Day 5–23: 5 exact, 5 within 3 of 16. Off 12–20 h: 12:15, 13:15, 18:15, 18:30, 19:50.
  - Mochov → Praha, Černý Most: slots :31, typed 30, running 28 min. Window: slots 15:31, 16:31 against real 15:31, 16:31 → Step 4 ok. Day 5–23: 2 exact, 2 within 3 of 15. Off 12–20 h: 12:41, 13:11, 13:41, 14:41, 14:51, 17:45, 18:13, 19:13.
- **354 Mochovská** every 60, need 1 (waits Černý Most 1, Mochovská 13):
  - Praha, Černý Most → Nehvizdy, Mochovská: slots :30, typed 29, running 23 min. Window: slots 15:30, 16:30 against real 15:30, 16:30 → Step 4 ok. Day 5–23: 4 exact, 4 within 3 of 13. Off 12–20 h: 17:35, 19:15.
  - Nehvizdy, Mochovská → Praha, Černý Most: slots :06, typed 5, running 23 min. Window: slots 15:06, 16:06 against real 15:06, 16:06 → Step 4 ok. Day 5–23: 2 exact, 4 within 3 of 13. Off 12–20 h: 17:01, 19:44. Knot check, model vs real (worst, min): Černý Most 4; Logistický park 4.
- **354 LE&CO** every 480, need 1 (waits Černý Most 438, LE&CO 6):
  - Praha, Černý Most → Jirny, LE&CO: slots 17:10, typed 9, running 19 min. Window: slots none against real none → Step 4 ok. Day 5–23: 1 exact, 1 within 3 of 6. Off 12–20 h: 13:30, 17:00. Knot check, model vs real (worst, min): Logistický park 249.
  - Jirny, LE&CO → Praha, Černý Most: slots 17:35, typed 34, running 17 min. Window: slots none against real 15:16 → Step 4 ok. Day 5–23: 1 exact, 1 within 3 of 8. Off 12–20 h: 14:20, 15:16, 18:00. Knot check, model vs real (worst, min): Černý Most 205; Logistický park 205.

### 357 Praha,Opatov - Nupaky

- **Core points:** Praha, Opatov; Praha, Šeberov; Průhonice; Čestlice. Model window 15:00–17:00 (anchor set by hand).
- 357 hourly (Opatov :45, Čestlice :11 until 16:11, then 16:56, 17:57); peak shorts Opatov :15 → Průhonice / Průhonice :33 → Opatov
  15:15–17:33: 357 Průhonice (`notvia` Čestlice). Anchor 15:30 by hand (window 15:00–17:00): at 16:00 the main line's 17:11 slot
  has the 16:56 trip 15 min before it.
- **357** every 60, need 1 (waits Opatov 10, Čestlice 5):
  - Praha, Opatov → Čestlice: slots :45, typed 44, running 21 min. Window: slots 15:45, 16:45 against real 15:45, 16:45 → Step 4 ok. Day 5–23: 16 exact, 16 within 3 of 18.
  - Čestlice → Praha, Opatov: slots :11, typed 10, running 24 min. Window: slots 15:11, 16:11 against real 15:11, 16:11, 16:56 → Step 4 ok. Day 5–23: 8 exact, 10 within 3 of 20. Off 12–20 h: 16:56, 17:57.
- **357 Průhonice** every 60, need 1 (waits Opatov 25, Průhonice 3):
  - Praha, Opatov → Průhonice: slots :15, typed 14, running 15 min. Window: slots 15:15, 16:15 against real 15:15, 16:15 → Step 4 ok. Day 5–23: 3 exact, 3 within 3 of 3.
  - Průhonice → Praha, Opatov: slots :33, typed 32, running 17 min. Window: slots 15:33, 16:33 against real 15:33, 16:33 → Step 4 ok. Day 5–23: 3 exact, 3 within 3 of 3.

### 367 Praha,Černý Most - Radonice - Brandýs nad Labem-Stará Boleslav

- **Core points:** Brandýs n.L.-St.Bol., autobusové stanoviště; Jenštejn; Praha, Černý Most. Model window 15:30–17:30 (the line's anchor).
- Every 30 both ways in the afternoon (Černý Most :05 / :35 13:05–19:05; Brandýs :17 / :47 13:47–17:47). The evening trips
  (18:05, 19:45 on) skip Radonice, Penny Market; the line's path is the afternoon one with it.
- **367** every 30, need 3 (waits Černý Most 18, autobusové stanoviště 15):
  - Praha, Černý Most → Brandýs n.L.-St.Bol., autobusové stanoviště: slots :05 / :35, typed 4, running 27 min. Window: slots 15:35, 16:05, 16:35, 17:05 against real 15:35, 16:05, 16:35, 17:05 → Step 4 ok. Day 5–23: 25 exact, 25 within 3 of 28. Off 12–20 h: 19:45.
  - Brandýs n.L.-St.Bol., autobusové stanoviště → Praha, Černý Most: slots :17 / :47, typed 16, running 30 min. Window: slots 15:47, 16:17, 16:47, 17:17 against real 15:47, 16:17, 16:47, 17:17 → Step 4 ok. Day 5–23: 9 exact, 23 within 3 of 26.

### 371 Praha,Kobylisy - Klecany,Klecánky/Husinec,Řež

- **Core points:** Praha, Kobylisy; Klecany, u hřbitova; Husinec, Řež, závod; Klecany, Astrapark; Klecany, Klecánky; Vodochody, Hoštice. Model window 15:30–17:30 (the line's anchor).
- Kobylisy – Klecany, u hřbitova, then three ends (Řež; Astrapark; Klecánky) and two Vodochody, Hoštice trips. Řež: every 30
  both ways, exact (:15 / :45 out, :05 / :35 back). Klecany side: out 4 an hour (Astrapark :08 / :23 / :53, Klecánky :38), back 2
  (u hřbitova :07 / :37): an outstation end, timed at the inbound rate. 371 Astrapark every 120 (Kobylisy 15:08, 15:23; Astrapark
  15:33, 16:03) and 371 Klecánky every 120 (Kobylisy :38 hourly, written folded; Klecánky 16:26, 17:02) together give exactly the
  real :07 / :37 at u hřbitova. The Astrapark out slots were chosen by the waits (8 and 23 min at Astrapark against 83 for 15:53 /
  16:23). FEWER on the Astrapark out leg (2 slots, 6 real departures in the window): the outstation case.
- Rejected: one Klecany line every 30 (two different terminals, Astrapark and Klecánky).
- 371 Vodochody (every 480, 14:08 / 14:35, the real 2-min turn): the only service of Vodochody, Hoštice.
- **371** every 30, need 3 (waits Kobylisy 13, závod 25):
  - Praha, Kobylisy → Husinec, Řež, závod: slots :15 / :45, typed 14, running 25 min. Window: slots 15:45, 16:15, 16:45, 17:15 against real 15:45, 16:15, 16:45, 17:15 → Step 4 ok. Day 5–23: 7 exact, 7 within 3 of 26. Off 12–20 h: 12:40, 13:20, 13:50, 17:50, 18:20, 18:50, 19:25, 19:55.
  - Husinec, Řež, závod → Praha, Kobylisy: slots :05 / :35, typed 4, running 27 min. Window: slots 15:35, 16:05, 16:35, 17:05 against real 15:35, 16:05, 16:35, 17:05 → Step 4 ok. Day 5–23: 7 exact, 10 within 3 of 25. Off 12–20 h: 12:25, 13:15, 13:55, 14:25, 19:20.
- **371 Astrapark** every 120, need 2 (waits Kobylisy 46/91, Astrapark 8/23):
  - Praha, Kobylisy → Klecany, Astrapark: slots 13:08, 13:23, 15:08, 15:23, 17:08, 17:23, typed 7, 22, running 17 min. Window: slots 17:08, 17:23 against real 15:53, 16:08, 16:23, 16:53, 17:08, 17:23 → Step 4 FAIL. Day 5–23: 5 exact, 5 within 3 of 27. Off 12–20 h: 12:00, 14:08, 14:23, 14:53, 15:53, 16:08, 16:23, 16:53, 17:40, 18:10, 18:40, 19:12.
  - Klecany, Astrapark → Praha, Kobylisy: slots 13:33, 14:03, 15:33, 16:03, 17:33, 18:03, typed 32, 62, running 19 min. Window: slots 15:33, 16:03 against real 15:33, 16:03, 16:33 → Step 4 ok. Day 5–23: 3 exact, 3 within 3 of 26. Off 12–20 h: 12:53, 13:38, 14:43, 16:33, 18:58.
- **371 Klecánky** every 120, need 2 (waits Kobylisy 112/16, Klecánky 7/31):
  - Praha, Kobylisy → Klecany, Klecánky: slots 13:38, 14:38, 15:38, 16:38, 17:38, 18:38, typed 37, 97, running 17 min. Window: slots 15:38, 16:38 against real 15:38, 16:38 → Step 4 ok. Day 5–23: 3 exact, 5 within 3 of 15. Off 12–20 h: 12:00, 19:12. Knot check, model vs real (worst, min): Klecánky 3.
  - Klecany, Klecánky → Praha, Kobylisy: slots 13:02, 14:26, 15:02, 16:26, 17:02, 18:26, typed 1, 85, running 20 min. Window: slots 16:26, 17:02 against real 16:26, 17:02 → Step 4 ok. Day 5–23: 3 exact, 3 within 3 of 16. Off 12–20 h: 12:46, 14:12, 18:03, 19:45. Knot check, model vs real (worst, min): Kobylisy 6; u hřbitova 6.
- **371 Vodochody** every 480, need 1 (waits Kobylisy 426, Hoštice 2):
  - Praha, Kobylisy → Vodochody, Hoštice: slots 14:08, typed 307, running 25 min. Window: slots none against real 17:23 → Step 4 ok. Day 5–23: 1 exact, 1 within 3 of 3. Off 12–20 h: 17:23. Knot check, model vs real (worst, min): u hřbitova 147; Astrapark 147; Hoštice 147.
  - Vodochody, Hoštice → Praha, Kobylisy: slots 14:35, typed 334, running 27 min. Window: slots none against real none → Step 4 ok. Day 5–23: 1 exact, 1 within 3 of 2. Knot check, model vs real (worst, min): Kobylisy 145; u hřbitova 145; Astrapark 145.

### 373 Praha,Kobylisy - Veliká Ves

- **Core points:** Praha, Kobylisy; Klíčany; Veliká Ves; Úžice, Netřeba; Odolena Voda, Ke Stadionu. Model window 15:30–17:30 (the line's anchor).
- Out of Kobylisy every 40 from 15:32 to 18:52 (:32 / :12 / :52), hourly :55 before; back 15:38, 16:24, 17:11, 17:45, 18:21, 19:07
  (about 40 min apart, no fixed minute). Half the trips run via Neratovice, Korycany and Úžice (16:12, 18:12 out; 15:38, 16:24 back),
  the only service of the two Úžice stops (okres Mělník) and Korycany. Every 40 fails back (16:18, 16:58 empty); every 120 with three
  slots each way is exact in the window. Path variants on one line (Step 5): out direct, back via Úžice, the combination that
  matches 4 of the 6 window slots; the 16:12 out (via Úžice) and the 17:11 back (direct) run the other road in the game (path audit
  flag on 16:12, explained). `rt` 39 set by hand on the way out (the direct trips' own time; the median mixed in the Úžice trips).
- **373** every 120, need 3 (waits Kobylisy 27/21/14, Ke Stadionu 13/20/7):
  - Praha, Kobylisy → Odolena Voda, Ke Stadionu: slots 13:32, 14:12, 14:52, 15:32, 16:12, 16:52, 17:32, 18:12, 18:52, typed 31, 71, 111, running 39 min. Window: slots 15:32, 16:12, 16:52 against real 15:32, 16:12, 16:52 → Step 4 ok. Day 5–23: 6 exact, 11 within 3 of 23. Off 12–20 h: 13:55, 14:42. Knot check, model vs real (worst, min): Ke Stadionu 9.
  - Odolena Voda, Ke Stadionu → Praha, Kobylisy: slots 13:11, 13:38, 14:24, 15:11, 15:38, 16:24, 17:11, 17:38, 18:24, typed 10, 37, 83, running 47 min. Window: slots 15:38, 16:24, 17:11 against real 15:38, 16:24, 17:11 → Step 4 ok. Day 5–23: 4 exact, 6 within 3 of 22. Off 12–20 h: 12:50, 13:52, 14:50, 17:45, 19:07, 19:57. Knot check, model vs real (worst, min): Kobylisy 7; Klíčany 7; Veliká Ves 7; Netřeba 47.

### 374 Praha,Kobylisy - Odolena Voda

- **Core points:** Praha, Kobylisy; Klecany, u kostela; Vodochody; Máslovice; Odolena Voda, závod. Model window 15:30–17:30 (the line's anchor).
- Out every 30 at :00 / :30 (15:00–19:00); back from Máslovice 15:11, 15:41 (the Odolena Voda trip passing), 16:11, 16:38, 17:11,
  17:38. Every 60 with :11 / :38 beats every 30 :11 on exact hits over the day (5 against 3). The :38 trips run via Klecany, Ahold
  (its only service), so the way back takes that path (`stops_via`).
- The Odolena Voda, závod round (14:30 out, 15:31 back via Postřižín) is listed: Postřižín, u kapličky (okres Mělník) is served all
  afternoon by 370 (Mělnicko sheet, modelled there), Odolena Voda, závod by 657. A Máslovice – Odolena Voda shuttle (1 bus) was
  dropped for that reason.
- **374** every 60, need 3 (waits Kobylisy 18/15, Máslovice 11/14):
  - Praha, Kobylisy → Máslovice: slots :00 / :30, typed 29, 59, running 27 min. Window: slots 15:30, 16:00, 16:30, 17:00 against real 15:30, 16:00, 16:30, 17:00 → Step 4 ok. Day 5–23: 14 exact, 14 within 3 of 28. Off 12–20 h: 12:20, 12:55, 19:40.
  - Máslovice → Praha, Kobylisy: slots :11 / :38, typed 10, 37, running 34 min. Window: slots 15:38, 16:11, 16:38, 17:11 against real 15:41, 16:11, 16:38, 17:11 → Step 4 ok. Day 5–23: 7 exact, 12 within 3 of 27. Off 12–20 h: 12:01, 12:56, 19:01. Knot check, model vs real (worst, min): Kobylisy 3; u kostela 3; Vodochody 3.

### 375 Praha,Českomoravská - Brandýs nad Labem-Stará Boleslav

- **Core points:** Brandýs n.L.-St.Bol., železniční stanice; Brandýs n.L.-St.Bol., autobusové stanoviště; Brandýs n.L.-St.Bol., náměstí; Praha, Českomoravská. Model window 15:30–17:30 (the line's anchor).
- Every 15 at both ends from 13:13 to 17:48 (Brandýs, železniční stanice) and 13:00 to 18:30 (Českomoravská), one path. Every 15 at
  :03 / :00 is exact on 30 and 38 trips of the day. The 1-min wait at Brandýs is the real quick turn (26 of 63 arrivals leave
  again within 5 min). At Českomoravská 46 of 61 departures follow a 152 arrival (through-running with a city line).
- **375** every 15, need 7 (waits železniční stanice 1, Českomoravská 6):
  - Brandýs n.L.-St.Bol., železniční stanice → Praha, Českomoravská: slots :03 / :18 / :33 / :48, typed 2, running 51 min. Window: slots 15:33, 15:48, 16:03, 16:18, 16:33, 16:48, 17:03, 17:18 against real 15:33, 15:48, 16:03, 16:18, 16:33, 16:48, 17:03, 17:18 → Step 4 ok. Day 5–23: 30 exact, 50 within 3 of 57. Off 12–20 h: 12:53, 13:13, 18:08.
  - Praha, Českomoravská → Brandýs n.L.-St.Bol., železniční stanice: slots :00 / :15 / :30 / :45, typed 14, running 47 min. Window: slots 15:30, 15:45, 16:00, 16:15, 16:30, 16:45, 17:00, 17:15 against real 15:30, 15:45, 16:00, 16:15, 16:30, 16:45, 17:00, 17:15 → Step 4 ok. Day 5–23: 38 exact, 44 within 3 of 57. Off 12–20 h: 18:50, 19:10, 19:50.

### 379 Praha,Černý Most - Brandýs nad Labem-Stará Boleslav

- **Core points:** Brandýs n.L.-St.Bol., autobusové stanoviště; Praha, Černý Most. Model window 15:30–17:30 (the line's anchor).
- Afternoon every 30 both ways (Brandýs :14 / :44 from 14:14, Černý Most :15 / :45 from 13:45), nothing 9:00–13:45. 2 buses.
- **379** every 30, need 2 (waits autobusové stanoviště 13, Černý Most 15):
  - Brandýs n.L.-St.Bol., autobusové stanoviště → Praha, Černý Most: slots :14 / :44, typed 13, running 16 min. Window: slots 15:44, 16:14, 16:44, 17:14 against real 15:44, 16:14, 16:44, 17:14 → Step 4 ok. Day 5–23: 10 exact, 10 within 3 of 22.
  - Praha, Černý Most → Brandýs n.L.-St.Bol., autobusové stanoviště: slots :15 / :45, typed 14, running 16 min. Window: slots 15:45, 16:15, 16:45, 17:15 against real 15:45, 16:15, 16:45, 17:15 → Step 4 ok. Day 5–23: 14 exact, 14 within 3 of 23.

### 385 Praha,Opatov - Zvánovice

- **Core points:** Praha, Opatov; Nupaky, hotel; Říčany, Masarykovo náměstí; Říčany, Olivovna; Mukařov [PH]; Zvánovice. Model window 15:30–17:30 (the line's anchor).
- Three ends, each its own Simutrans line, together every 15 out of Opatov: Zvánovice (:02 / :45), Nupaky, hotel (every 30, :17 /
  :18) and Říčany, Olivovna (:32 / :42). The short lines use `notvia` (Říčany, Masarykovo náměstí for Nupaky; Zvánovice for
  Olivovna) so the longer trips passing their terminals stay on their own lines. The Mukařov trips end before 13:34; at Olivovna 385
  meets MHD Říčany 7 and 9 (5 and 6 of 11).
- **385** every 60, need 3 (waits Opatov 11, Zvánovice 39):
  - Praha, Opatov → Zvánovice: slots :02, typed 1, running 64 min. Window: slots 16:02, 17:02 against real 16:02, 17:02 → Step 4 ok. Day 5–23: 5 exact, 8 within 3 of 9. Knot check, model vs real (worst, min): Olivovna 1; Mukařov [PH] 1; Zvánovice 1.
  - Zvánovice → Praha, Opatov: slots :45, typed 44, running 66 min. Window: slots 15:45, 16:45 against real 15:45, 16:45 → Step 4 ok. Day 5–23: 6 exact, 6 within 3 of 11.
- **385 Nupaky** every 30, need 2 (waits Opatov 11, hotel 13):
  - Praha, Opatov → Nupaky, hotel: slots :17 / :47, typed 16, running 18 min. Window: slots 15:47, 16:17, 16:47, 17:17 against real 15:47, 16:17, 16:47, 17:17 → Step 4 ok. Day 5–23: 9 exact, 9 within 3 of 18. Off 12–20 h: 12:34, 19:34.
  - Nupaky, hotel → Praha, Opatov: slots :18 / :48, typed 17, running 18 min. Window: slots 15:48, 16:18, 16:48, 17:18 against real 15:48, 16:18, 16:48, 17:18 → Step 4 ok. Day 5–23: 5 exact, 5 within 3 of 22. Off 12–20 h: 12:03, 13:03, 14:03, 14:53, 15:13, 19:03.
- **385 Říčany** every 60, need 2 (waits Opatov 11, Olivovna 31):
  - Praha, Opatov → Říčany, Olivovna: slots :32, typed 31, running 39 min. Window: slots 15:32, 16:32 against real 15:32, 16:32 → Step 4 ok. Day 5–23: 5 exact, 8 within 3 of 17. Off 12–20 h: 12:04, 19:04.
  - Říčany, Olivovna → Praha, Opatov: slots :42, typed 41, running 39 min. Window: slots 15:42, 16:42 against real 15:42, 16:42 → Step 4 ok. Day 5–23: 3 exact, 3 within 3 of 13. Off 12–20 h: 12:12, 13:12, 14:12.

### 391 Praha,Nádraží Klánovice - Úvaly

- **Core points:** Praha, Nádraží Klánovice; Květnice, náves; Škvorec, náměstí; Úvaly, železniční stanice; Úvaly, OC Pražská. Model window 15:30–17:30 (the line's anchor).
- Hourly: Klánovice :07, Úvaly, železniční stanice :54. The trips that start or end at Úvaly, OC Pražská (12:37, 13:07 out;
  12:50, 13:50, 16:20 back) take the loop past Elektromechanika, OC Pražská and MŠ Pražská (also served by X391). The Simutrans line runs that loop on every
  trip, as its own trips there do (costs no bus: 2 either way); the way back is read at the
  station (:54) whichever stop the trip starts from. The 16:20 from OC Pražská is off the pattern.
- **391** every 60, need 2 (waits Nádraží Klánovice 45, OC Pražská 5):
  - Praha, Nádraží Klánovice → Úvaly, OC Pražská: slots :07, typed 6, running 38 min. Window: slots 16:07, 17:07 against real 16:07, 17:07 → Step 4 ok. Day 5–23: 9 exact, 9 within 3 of 15. Off 12–20 h: 12:37. Knot check, model vs real (worst, min): železniční stanice 1; OC Pražská 209.
  - Úvaly, OC Pražská → Praha, Nádraží Klánovice (read at Úvaly, železniční stanice: 0:54, terminal = knot − 4): slots :50, typed 49, running 32 min. Window: slots 15:50, 16:50 against real 15:50, 16:20, 16:50 → Step 4 ok. Day 5–23: 8 exact, 9 within 3 of 16. Off 12–20 h: 16:20.

### 411 Praha,Kobylisy - Zdiby,Holosmetky/Brnky

- **Core points:** Praha, Kobylisy; Zdiby; Zdiby, Holosmetky; Zdiby, Brnky. Model window 15:30–17:30 (the line's anchor).
- Two ends from Zdiby: Holosmetky hourly exact (Kobylisy :55, Holosmetky :16), and the Brnky loop, hourly with a drift (Kobylisy
  13:15, 14:15, 15:25, 16:25, 17:35; Brnky 13:42, 14:38, 15:42, 16:44, 17:58). No hourly Brnky row passes Step 4 in the 16:00
  window (17:25 has the 17:35 trip 10 min later); every 120 at 16:25 / 16:42 passes but halves an hourly line (the method's 409 /
  411 mistake). Kept hourly :25 / :42, approximate, on the owner checks. Brnky turns at once (`lay` 0, as the real 16:25 → 16:42 →
  16:44); 1 bus either way.
- **411** every 60, need 1 (waits Kobylisy 23, Holosmetky 7):
  - Praha, Kobylisy → Zdiby, Holosmetky: slots :55, typed 54, running 14 min. Window: slots 15:55, 16:55 against real 15:55, 16:55 → Step 4 ok. Day 5–23: 3 exact, 4 within 3 of 13. Off 12–20 h: 12:30, 13:05, 14:05, 18:31.
  - Zdiby, Holosmetky → Praha, Kobylisy: slots :16, typed 15, running 16 min. Window: slots 16:16, 17:16 against real 16:16, 17:16 → Step 4 ok. Day 5–23: 3 exact, 3 within 3 of 12. Off 12–20 h: 12:48, 13:28, 14:20, 18:46.
- **411 Brnky** every 60, need 1 (waits Kobylisy 24, Brnky 0):
  - Praha, Kobylisy → Zdiby, Brnky: slots :25, typed 24, running 17 min. Window: slots 16:25, 17:25 against real 16:25 → Step 4 FAIL (empty 17:25). Day 5–23: 2 exact, 2 within 3 of 11. Off 12–20 h: 13:15, 14:15, 17:35, 19:18. Knot check, model vs real (worst, min): Zdiby 10; Brnky 10.
  - Zdiby, Brnky → Praha, Kobylisy: slots :42, typed 41, running 19 min. Window: slots 15:42, 16:42 against real 15:42, 16:44 → Step 4 ok. Day 5–23: 2 exact, 4 within 3 of 12. Off 12–20 h: 14:38, 17:58, 19:34. Knot check, model vs real (worst, min): Kobylisy 2; Zdiby 2.

### 461 Strančice - Velké Popovice - Kamenice

- **Core points:** Strančice, železniční stanice; Kunice; Velké Popovice, Todice; Velké Popovice, pivovar; Kamenice, Všedobrovice; Kamenice, kulturní dům. Model window 15:30–17:30 (anchor set by hand).
- Two hourly services every 30 between Strančice and Velké Popovice: Kamenice (:07 / :50) and Velké Popovice, pivovar (:37 / :32, most
  trips out via Kunice, Dolní Lomnice; back read at Kunice :44, where the 14:17 and 16:26 Dolní Lomnice trips meet the :32 pattern).
  Anchor 16:00 by hand: the automatic 13:30 window holds the midday extras (13:02, 13:07, 14:17) and the Kamenice line's 13:07 slot
  has no trip. Strančice: the Kamenice buses arrive :18, the Popovice buses :48 (departures :07 / :37): swapping there would need
  3 buses instead of 4 (pooling, for the live map).
- Path audit: the 16:32 window slot back from pivovar stands for the real 16:26 via Dolní Lomnice (read at Kunice :44, where it
  meets the pattern; the card's note names it). The game bus runs direct; Dolní Lomnice is on the way out.
- **461** every 60, need 2 (waits železniční stanice 49, kulturní dům 17):
  - Strančice, železniční stanice → Kamenice, kulturní dům: slots :07, typed 6, running 26 min. Window: slots 16:07, 17:07 against real 16:07, 17:07 → Step 4 ok. Day 5–23: 7 exact, 7 within 3 of 13. Off 12–20 h: 12:37.
  - Kamenice, kulturní dům → Strančice, železniční stanice: slots :50, typed 49, running 28 min. Window: slots 15:50, 16:50 against real 15:50, 16:50 → Step 4 ok. Day 5–23: 6 exact, 6 within 3 of 16. Off 12–20 h: 13:20.
- **461 Velké Popovice** every 60, need 2 (waits železniční stanice 49, pivovar 36):
  - Strančice, železniční stanice → Velké Popovice, pivovar: slots :37, typed 36, running 19 min. Window: slots 15:37, 16:37 against real 15:37, 16:37 → Step 4 ok. Day 5–23: 7 exact, 9 within 3 of 12. Off 12–20 h: 13:07, 19:07. Knot check, model vs real (worst, min): Todice 5; pivovar 5.
  - Velké Popovice, pivovar → Strančice, železniční stanice (read at Kunice: 0:44, terminal = knot − 12): slots :32, typed 31, running 16 min. Window: slots 15:32, 16:32 against real 15:32, 16:32 → Step 4 ok. Day 5–23: 6 exact, 6 within 3 of 10. Off 12–20 h: 13:02, 14:23. Knot check, model vs real (worst, min): Todice 6.

### 462 Mnichovice - Strančice - Kunice,Všešímy

- **Core points:** Strančice, železniční stanice; Kunice, Všešímy, Pardálov; Kunice, Všešímy; Kunice, Všešímy, SŠŘ. Model window 15:30–17:30 (the line's anchor).
- One bus's afternoon: Strančice 14:55 → Všešímy, SŠŘ, back 15:08; 15:37 → Všešímy, back 16:04; then 17:07 / 17:17 and 18:37 /
  18:50. Two ends after Pardálov (Všešímy and the school SŠŘ), all the stops only 462's. A circuit every 240 visiting Strančice
  twice, on the first round (the 418 / 579 rule: a one-bus sequence becomes a circuit on the shortest period that holds it).
  Rejected: every 90 out (15:37, 17:07, 18:37 exact) fails back; two lines (Všešímy, SŠŘ) need 2 buses.
- **462** every 240, need 1 (waits železniční stanice (1) 158, železniční stanice (3) 17, SŠŘ (2) 1, Všešímy (4) 14):
  - Strančice, železniční stanice → Kunice, Všešímy, SŠŘ: slots 14:55, 18:55, typed 114, running 12 min. Window: slots none against real 15:37 → Step 4 ok. Day 5–23: 1 exact, 1 within 3 of 5. Off 12–20 h: 15:37, 18:37. Knot check, model vs real (worst, min): Pardálov 227; SŠŘ 227.
  - Kunice, Všešímy, SŠŘ → Strančice, železniční stanice: slots 15:08, typed 127, running 12 min. Window: slots none against real 16:08 → Step 4 ok. Day 5–23: 1 exact, 1 within 3 of 5. Off 12–20 h: 16:08, 18:50. Knot check, model vs real (worst, min): železniční stanice 200; Pardálov 200.
  - Strančice, železniční stanice → Kunice, Všešímy: slots 15:37, typed 156, running 13 min. Window: slots 15:37 against real 15:37, 17:07 → Step 4 ok. Day 5–23: 1 exact, 1 within 3 of 5. Off 12–20 h: 17:07. Knot check, model vs real (worst, min): Všešímy 6.
  - Kunice, Všešímy → Strančice, železniční stanice: slots 16:04, typed 183, running 13 min. Window: slots 16:04 against real 16:04, 17:17 → Step 4 ok. Day 5–23: 1 exact, 1 within 3 of 5. Off 12–20 h: 17:17. Knot check, model vs real (worst, min): železniční stanice 6; Pardálov 6.

### 469 Strančice - Říčany

- **Core points:** Strančice, železniční stanice; Strančice, Předboř; Strančice, Všechromy, náves; Říčany, Olivovna. Model window 15:30–17:30 (the line's anchor).
- Every 2 h: Strančice :07 even hours (14:07, 18:07 exact, 16:04), Olivovna :02 odd hours (15:02, 17:02, 19:02 exact). 1 bus.
  Strančice, Všechromy is on the three loop trips only: the sheet's one roadside stop, in the sheet-wide roadside owner check.
- **Changed on 2 Nov (independent review):** core point "Strančice, Všechromy" corrected to "Strančice, Všechromy, náves" (the main
  path's stop; the other is only on the loop trips); the roadside owner check reworded as the one sheet-wide check with its bus cost
  (1 bus). Slots unchanged.
- **469** every 120, need 1 (waits železniční stanice 24, Olivovna 13):
  - Strančice, železniční stanice → Říčany, Olivovna: slots 14:07, 16:07, 18:07, typed 66, running 42 min. Window: slots 16:07 against real 16:04 → Step 4 ok. Day 5–23: 2 exact, 3 within 3 of 7. Off 12–20 h: 13:37. Knot check, model vs real (worst, min): Předboř 3; náves 3; Olivovna 3.
  - Říčany, Olivovna → Strančice, železniční stanice: slots 13:02, 15:02, 17:02, typed 1, running 41 min. Window: slots 17:02 against real 17:02 → Step 4 ok. Day 5–23: 3 exact, 3 within 3 of 7. Off 12–20 h: 12:39.

### 482 Brandýs nad Labem-Stará Boleslav - Kostelec nad Labem - Neratovice - Mělník

- **Core points:** Brandýs n.L.-St.Bol., autobusové stanoviště; Brandýs n.L.-St.Bol., Pražská; Záryby; Neratovice, Kojetická; Mělník, autobusové nádraží; Mělník, Rožkovo údolí. Model window 14:30–16:30 (anchor set by hand).
- Hourly all day (Brandýs, autobusové stanoviště :39, Mělník :45), every 30 in the afternoon peak through extra trips that start at
  Brandýs, Pražská (14:22, 15:22, 16:22) and end at Brandýs, nádraží (Mělník 14:15, 15:15) or Neratovice, Kojetická (16:15). Both are
  short turns on the line's own path: Pražská lies on the way out, nádraží on the way back. One Simutrans line every 30, the way out
  read at Pražská (`knot`, :22 / :52), the way back counting the short trips (`core_to` Neratovice, Kojetická).
- Anchor 15:00 (window 14:30–16:30), the rule "model the line's own busiest two hours" applied: departures per two hours are 6 in
  13:00–15:00, 8 in 13:30–15:30, 14:00–16:00, 14:30–16:30 and 15:00–17:00, and 6 in the 16:00 window 15:30–17:30, so the peak runs
  every 30 from 14:15 to 16:52 (the 442 case: a line modelled at its peak rate). The extras are near-full-line trips on the line's
  own path, not the 282 shuttles. At 16:00 every 30 fails by one slot each way (17:22 / 17:15). For information: hourly :39 / :45 at
  16:00 would be 4 buses instead of 6, with the six extras listed (in the sheet's notes). Rejected: hourly 482 + a separate hourly 482
  Pražská (7 buses; the extras' line waits 52 min at Mělník).
- 482 Rožkovo údolí: the only service of Mělník, Rožkovo údolí and Strážnická (okres Mělník; no other PID line). The two real trips
  (Brandýs 12:24, 13:39 out; Rožkovo údolí 14:33, 15:33 back) are the :39 / :45 slots of the trunk extended through Mělník, so a
  separate every-480 line from Brandýs would duplicate a trunk slot; as a shuttle from Mělník, autobusové nádraží it holds the real
  15:01 / 15:33 segments and leaves the trunk alone. 1 bus.
- **Changed on 2 Nov (independent review):** the owner check on the anchor is removed (it re-asked the busiest-two-hours rule); the
  4-bus hourly alternative is in `notes` as information. Slots, typed values and buses unchanged.
- The knot check at Brandýs, autobusové stanoviště on the way back shows 30 for the :15 slots: those real trips end at nádraží.
- **482** every 30, need 6 (waits autobusové stanoviště 8, autobusové nádraží 15):
  - Brandýs n.L.-St.Bol., autobusové stanoviště → Mělník, autobusové nádraží (read at Brandýs n.L.-St.Bol., Pražská: 0:22, terminal = knot − 13): slots :09 / :39, typed 8, running 81 min. Window: slots 14:39, 15:09, 15:39, 16:09 against real 14:39, 15:09, 15:39, 16:09 → Step 4 ok. Day 5–23: 8 exact, 9 within 3 of 18. Off 12–20 h: 12:24. Knot check, model vs real (worst, min): autobusové nádraží 4.
  - Mělník, autobusové nádraží → Brandýs n.L.-St.Bol., autobusové stanoviště: slots :15 / :45, typed 14, running 76 min. Window: slots 14:45, 15:15, 15:45, 16:15 against real 14:45, 15:15, 15:45, 16:15 → Step 4 ok. Day 5–23: 13 exact, 13 within 3 of 20. Knot check, model vs real (worst, min): autobusové stanoviště 30; Záryby 30.
- **482 Rožkovo údolí** every 480, need 1 (waits autobusové nádraží 436, Rožkovo údolí 23):
  - Mělník, autobusové nádraží → Mělník, Rožkovo údolí: slots 15:01, typed 360, running 9 min. Window: slots 15:01 against real 15:01 → Step 4 ok. Day 5–23: 1 exact, 1 within 3 of 4. Off 12–20 h: 13:46.
  - Mělník, Rožkovo údolí → Mělník, autobusové nádraží: slots 15:33, typed 392, running 12 min. Window: slots 15:33 against real 14:33, 15:33 → Step 4 ok. Day 5–23: 1 exact, 1 within 3 of 3. Off 12–20 h: 14:33.

### 484 Úvaly - Horoušany - Úvaly

- **Core points:** Úvaly, železniční stanice; Horoušany; Tuklaty, Tlustovousy. Model window 15:30–17:30 (the line's anchor).
- A 30-min one-way loop from Úvaly, železniční stanice, every 30 from 15:44 to 17:44 and hourly :44 otherwise; one bus turns at once
  (16:14 arrival = 16:14 departure), so `lay` 0: 1 bus. The 15:14 and evening Horoušany shorts are listed.
- **484** every 30, need 1 (waits železniční stanice 0):
  - Úvaly, železniční stanice → Úvaly, železniční stanice: slots :14 / :44, typed 13, running 30 min. Window: slots 15:44, 16:14, 16:44, 17:14 against real 15:44, 16:14, 16:44, 17:14 → Step 4 ok. Day 5–23: 11 exact, 11 within 3 of 18. Off 12–20 h: 12:56, 14:04.

### 489 Strančice - Struhařov - Klokočná - Louňovice

- **Core points:** Strančice, železniční stanice; Mnichovice, náměstí; Struhařov [PH]; Klokočná, náves; Mukařov [PH]; Louňovice. Model window 13:40–15:40 (the line's anchor).
- Hourly both ways (Strančice :34, Louňovice :29; the 14:26 is 3 min early). The trips use two roads through Všestary and the
  Svojetice, Na Moklině / Mnichovice, požární dům variants in no fixed order: the line takes the Vávrov road out and the Menčice road
  back so both are covered (path audit flags on 15:34 out and 14:29 back, explained). The Louňovice – Mukařov shuttles and the
  18:34 to Klokočná are listed (their stops are on 489). Anchor 14:10 (the line's own).
- **489** every 60, need 2 (waits železniční stanice 11, Louňovice 8):
  - Strančice, železniční stanice → Louňovice: slots :34, typed 33, running 47 min. Window: slots 14:34, 15:34 against real 14:34, 15:34 → Step 4 ok. Day 5–23: 6 exact, 7 within 3 of 11. Off 12–20 h: 12:04. Knot check, model vs real (worst, min): náměstí 6; Struhařov [PH] 6; náves 13; Mukařov [PH] 11; Louňovice 10.
  - Louňovice → Strančice, železniční stanice: slots :29, typed 28, running 54 min. Window: slots 14:29, 15:29 against real 14:26, 15:29 → Step 4 ok. Day 5–23: 8 exact, 9 within 3 of 13. Off 12–20 h: 12:16. Knot check, model vs real (worst, min): náměstí 6; Struhařov [PH] 6; náves 6.

### 490 Strančice - Ondřejov - Stříbrná Skalice

- **Core points:** Strančice, železniční stanice; Mnichovice, náměstí; Hrusice; Ondřejov, náměstí; Stříbrná Skalice, náměstí. Model window 15:30–17:30 (the line's anchor).
- The Ondřejov trips are short turns on the way to Stříbrná Skalice, so one line read at Ondřejov: out `core_to` Ondřejov, back
  `knot` Ondřejov. Every 30 fails (16:34 out and 15:58 back have no trip); every 120 with three slots each way is exact in the window
  (out 15:34, 16:04, 17:02; back at Ondřejov 15:28, 16:28, 16:58). 3 buses. 653 arrivals at Ondřejov meet 490 (3 of 8).
- **490** every 120, need 3 (waits železniční stanice 9/11/11, náměstí 30/30/32):
  - Strančice, železniční stanice → Stříbrná Skalice, náměstí: slots 13:02, 13:34, 14:04, 15:02, 15:34, 16:04, 17:02, 17:34, 18:04, typed 1, 33, 63, running 39 min. Window: slots 15:34, 16:04, 17:02 against real 15:34, 16:04, 17:02 → Step 4 ok. Day 5–23: 9 exact, 12 within 3 of 18. Off 12–20 h: 14:34, 18:34. Knot check, model vs real (worst, min): náměstí 32.
  - Stříbrná Skalice, náměstí → Strančice, železniční stanice (read at Ondřejov, náměstí: 0:28, 0:58, 1:28, terminal = knot − 15): slots 13:13, 14:13, 14:43, 15:13, 16:13, 16:43, 17:13, 18:13, 18:43, typed 12, 72, 102, running 40 min. Window: slots 16:13, 16:43, 17:13 against real 16:13, 16:43, 17:15 → Step 4 ok. Day 5–23: 11 exact, 13 within 3 of 19. Off 12–20 h: 13:43, 17:43, 19:44. Knot check, model vs real (worst, min): železniční stanice 2; náměstí 2; Hrusice 2; náměstí 2.

### 492 Kostelec nad Černými lesy - Jevany - Černé Voděrady

- **Core points:** Kostelec nad Černými lesy, náměstí; Jevany; Černé Voděrady. Model window 15:30–17:30 (the line's anchor).
- Hourly (Kostelec :54, 16:57; Černé Voděrady :52). 2 buses (39 / 36 min waits, as the timetable's two alternating buses).
- **492** every 60, need 2 (waits náměstí 42, Černé Voděrady 36):
  - Kostelec nad Černými lesy, náměstí → Černé Voděrady: slots :54, typed 53, running 22 min. Window: slots 15:54, 16:54 against real 15:54, 16:57 → Step 4 ok. Day 5–23: 3 exact, 5 within 3 of 11. Off 12–20 h: 13:04, 13:49.
  - Černé Voděrady → Kostelec nad Černými lesy, náměstí: slots :52, typed 51, running 20 min. Window: slots 15:52, 16:52 against real 15:52, 16:52 → Step 4 ok. Day 5–23: 5 exact, 5 within 3 of 9. Off 12–20 h: 18:37. Knot check, model vs real (worst, min): náměstí 2.

### 494 Strančice - Tehov - Říčany

- **Core points:** Strančice, železniční stanice; Tehov; Říčany, Wolkerova. Model window 15:30–17:30 (the line's anchor).
- Strančice 14:34, back 14:41 and 16:41: every 240 on 14:34 / 16:41 (one bus), the only service of Tehov, Lada.
- **494** every 240, need 1 (waits železniční stanice 71, Wolkerova 85):
  - Strančice, železniční stanice → Říčany, Wolkerova: slots 14:34, 18:34, typed 93, running 42 min. Window: slots none against real none → Step 4 ok. Day 5–23: 1 exact, 1 within 3 of 4. Knot check, model vs real (worst, min): Tehov 191; Wolkerova 191.
  - Říčany, Wolkerova → Strančice, železniční stanice: slots 16:41, typed 220, running 42 min. Window: slots 16:41 against real 16:41 → Step 4 ok. Day 5–23: 1 exact, 1 within 3 of 3. Off 12–20 h: 14:41.

### 582 Strančice - Tehov - Světice - Říčany

- **Core points:** Strančice, železniční stanice; Tehov, Hačálka; Světice; Všestary; Říčany, Olivovna. Model window 15:30–17:30 (the line's anchor).
- Strančice 12:34, 16:34, 17:34, 19:04; Olivovna 12:20, 15:54, 18:24, 19:54: every 120 at 16:34 / 15:54 (one bus), the only
  service of Světice. The Olivovna – Všestary pair (13:10 / 14:43) is listed (Všestary is on 489).
- **582** every 120, need 1 (waits železniční stanice 11, Olivovna 51):
  - Strančice, železniční stanice → Říčany, Olivovna: slots 14:34, 16:34, 18:34, typed 93, running 29 min. Window: slots 16:34 against real 16:34 → Step 4 ok. Day 5–23: 2 exact, 2 within 3 of 6. Off 12–20 h: 17:34, 19:04.
  - Říčany, Olivovna → Strančice, železniční stanice: slots 13:54, 15:54, 17:54, typed 53, running 29 min. Window: slots 15:54 against real 15:54 → Step 4 ok. Day 5–23: 3 exact, 3 within 3 of 5. Off 12–20 h: 12:20, 18:24.

### 652 Kostelec nad Černými lesy - Oleška,Krymlov

- **Core points:** Kostelec nad Černými lesy, náměstí; Oleška; Oleška, Krymlov. Model window 15:30–17:30 (the line's anchor).
- Every 120: Kostelec :20 odd hours (15:20, 17:20, 19:20 exact), Krymlov :17 even hours (16:17, 18:17 exact). 1 bus.
- **652** every 120, need 1 (waits náměstí 38, Krymlov 32):
  - Kostelec nad Černými lesy, náměstí → Oleška, Krymlov: slots 13:20, 15:20, 17:20, typed 19, running 25 min. Window: slots 17:20 against real 17:20 → Step 4 ok. Day 5–23: 3 exact, 3 within 3 of 7. Off 12–20 h: 12:50, 14:10.
  - Oleška, Krymlov → Kostelec nad Černými lesy, náměstí: slots 14:17, 16:17, 18:17, typed 76, running 25 min. Window: slots 16:17 against real 16:17 → Step 4 ok. Day 5–23: 2 exact, 2 within 3 of 6. Off 12–20 h: 13:17, 14:47.

### 653 Ondřejov - Kaliště,Poddubí

- **Core points:** Ondřejov, náměstí; Kaliště; Kaliště, Poddubí. Model window 15:30–17:30 (the line's anchor).
- Ondřejov 14:02, 15:50, 18:52; Poddubí 14:40, 16:47 (the bus sleeps at Poddubí). Every 120 at 15:50 / 16:47, one bus; the 14:02 /
  14:40 round is off (12 / 7 min). 3 of 5 Poddubí arrivals at Ondřejov go on as 490.
- **653** every 120, need 1 (waits náměstí 46, Poddubí 40):
  - Ondřejov, náměstí → Kaliště, Poddubí: slots 13:50, 15:50, 17:50, typed 49, running 17 min. Window: slots 15:50 against real 15:50 → Step 4 ok. Day 5–23: 1 exact, 1 within 3 of 4. Off 12–20 h: 14:02, 18:52.
  - Kaliště, Poddubí → Ondřejov, náměstí: slots 14:47, 16:47, 18:47, typed 106, running 17 min. Window: slots 16:47 against real 16:47 → Step 4 ok. Day 5–23: 1 exact, 1 within 3 of 5. Off 12–20 h: 14:40.

### 655 Brandýs nad Labem-Stará Boleslav - Čelákovice - Úvaly

- **Core points:** Úvaly, železniční stanice; Jirny; Nehvizdy; Čelákovice, železniční stanice; Brandýs n.L.-St.Bol., nádraží. Model window 15:30–17:30 (the line's anchor).
- Úvaly – Brandýs hourly (Úvaly :35, Brandýs :38) and Brandýs – Čelákovice hourly in between (Brandýs :21, Čelákovice :55). The
  short legs use `notvia` Úvaly, železniční stanice and Nehvizdy, škola so the through trips passing Čelákovice stay on 655.
- The Brandýs → Nehvizdy, škola evening trips (18:39, 19:39; back 19:17) are listed: every stop is on 655.
- **655** every 60, need 2 (waits železniční stanice 6, nádraží 7):
  - Úvaly, železniční stanice → Brandýs n.L.-St.Bol., nádraží: slots :35, typed 34, running 56 min. Window: slots 15:35, 16:35 against real 15:35, 16:35 → Step 4 ok. Day 5–23: 7 exact, 10 within 3 of 15. Knot check, model vs real (worst, min): železniční stanice 4; nádraží 4.
  - Brandýs n.L.-St.Bol., nádraží → Úvaly, železniční stanice: slots :38, typed 37, running 51 min. Window: slots 15:38, 16:38 against real 15:38, 16:38 → Step 4 ok. Day 5–23: 10 exact, 11 within 3 of 15.
- **655 Čelákovice** every 60, need 1 (waits nádraží 5, železniční stanice 14):
  - Brandýs n.L.-St.Bol., nádraží → Čelákovice, železniční stanice: slots :21, typed 20, running 20 min. Window: slots 16:21, 17:21 against real 16:21, 17:21 → Step 4 ok. Day 5–23: 5 exact, 5 within 3 of 6.
  - Čelákovice, železniční stanice → Brandýs n.L.-St.Bol., nádraží: slots :55, typed 54, running 21 min. Window: slots 15:55, 16:55 against real 15:55, 16:55 → Step 4 ok. Day 5–23: 4 exact, 5 within 3 of 5.

### 656 Hovorčovice - Zlonín - Hovorčovice

- **Core points:** Hovorčovice, U Kostela; Líbeznice, škola; Čakovičky; Zlonín. Model window 13:30–15:30 (anchor set by hand).
- A loop from Hovorčovice, U Kostela, hourly :02 from 13:02 to 15:02 (12:13 before; 16:02 ends at Zlonín). Anchor 14:00 by hand
  (at 16:00 the window holds only the shortened last trip). The only service of Líbeznice, zdrav.stř.; Čakovičky is also on
  351 (Mělnicko sheet).
- **656** every 60, need 1 (waits U Kostela 17):
  - Hovorčovice, U Kostela → Hovorčovice, U Kostela: slots :02, typed 1, running 43 min. Window: slots 14:02, 15:02 against real 14:02, 15:02 → Step 4 ok. Day 5–23: 3 exact, 4 within 3 of 7. Off 12–20 h: 12:13. Knot check, model vs real (worst, min): Čakovičky 2; Zlonín 4.

### 657 Brandýs nad Labem-Stará Boleslav - Odolena Voda

- **Core points:** Brandýs n.L.-St.Bol., nádraží; Mratín; Líbeznice, pošta; Bašť, Baštěk; Odolena Voda, závod. Model window 13:30–15:30 (anchor set by hand).
- Brandýs :25 hourly 12:25–15:25 (two end at Bašť, Baštěk), then 16:20, 17:20 (Mratín, cukrovar short), 18:28; back at Bašť, Baštěk
  :24 / :25 hourly 12:25–17:25. Anchor 14:00 by hand (window 13:30–15:30): at 16:00 the window holds only 16:20 and the Mratín short,
  where :25 fails and :20 would put the line 5 min off its own pattern all day (4 trips at :25 against 2 at :20). The way back is
  read at Bašť, Baštěk (`knot_rt` 9, the slot trips' own time) because two trips start there.
- **657** every 60, need 2 (waits nádraží 21, závod 3):
  - Brandýs n.L.-St.Bol., nádraží → Odolena Voda, závod: slots :25, typed 24, running 47 min. Window: slots 14:25, 15:25 against real 14:25, 15:25 → Step 4 ok. Day 5–23: 4 exact, 6 within 3 of 9. Off 12–20 h: 16:20. Knot check, model vs real (worst, min): závod 55.
  - Odolena Voda, závod → Brandýs n.L.-St.Bol., nádraží (read at Bašť, Baštěk: 0:24, terminal = knot − 9): slots :15, typed 14, running 49 min. Window: slots 14:15, 15:15 against real 14:15, 15:15 → Step 4 ok. Day 5–23: 3 exact, 7 within 3 of 9. Knot check, model vs real (worst, min): nádraží 1; Mratín 1; pošta 1; Baštěk 1.

### 666 Brandýs nad Labem-Stará Boleslav - Káraný

- **Core points:** Brandýs n.L.-St.Bol., autobusové stanoviště; Nový Vestec; Káraný, pošta. Model window 15:30–17:30 (the line's anchor).
- Out 13:05, 14:05, 15:35, 16:35, 18:03, 19:03, each bus back 17 min later: pairs an hour apart with 90-min gaps. Every 30
  :05 / :35 fails Step 4 (16:05, 17:05 empty), hourly :05 fails (16:05, 17:05 empty); hourly :35 / :52 passes with 2 / 2 window slots
  filled, 1 bus. The four other pairs are 30 min off the pattern.
- **666** every 60, need 1 (waits autobusové stanoviště 28, pošta 5):
  - Brandýs n.L.-St.Bol., autobusové stanoviště → Káraný, pošta: slots :35, typed 34, running 12 min. Window: slots 15:35, 16:35 against real 15:35, 16:35 → Step 4 ok. Day 5–23: 2 exact, 3 within 3 of 12. Off 12–20 h: 13:05, 14:05, 18:03, 19:03.
  - Káraný, pošta → Brandýs n.L.-St.Bol., autobusové stanoviště: slots :52, typed 51, running 15 min. Window: slots 15:52, 16:52 against real 15:52, 16:52 → Step 4 ok. Day 5–23: 2 exact, 3 within 3 of 12. Off 12–20 h: 13:22, 14:22, 18:22, 19:22.

### 667 Brandýs nad Labem-Stará Boleslav - Horky nad Jizerou

- **Core points:** Brandýs n.L.-St.Bol., nádraží; Brandýs n.L.-St.Bol., autobusové stanoviště; Skorkov; Benátky nad Jizerou, autobusové stanoviště; Horky nad Jizerou. Model window 15:30–17:30 (anchor set by hand).
- Brandýs :26 hourly from 14:26 (12:56, 13:56 via Skorkov, Otradovice), Benátky :15 hourly from 16:15 (14:15, 15:45; Horky 12:55,
  14:57). Anchor 16:00 by hand: the busiest stretch 13:50–15:50 is the Otradovice and Horky trips; at the automatic 14:20 no hourly
  row passes back (14:15, 15:10, 15:45). The way out takes Skorkov, Otradovice (`stops_via`, the only service of that stop) as the
  12:56 / 13:56 trips do; the :26 trips run straight. The Horky trips' stops (Benátky, Kbel; Dražice, Ovčín; Horky) are served by
  699, 775 and 315 (Mladoboleslavsko sheet).
- **667** every 60, need 2 (waits nádraží 39, autobusové stanoviště 10):
  - Brandýs n.L.-St.Bol., nádraží → Benátky nad Jizerou, autobusové stanoviště: slots :26, typed 25, running 39 min. Window: slots 16:26, 17:26 against real 16:26, 17:26 → Step 4 ok. Day 5–23: 6 exact, 6 within 3 of 15. Off 12–20 h: 12:56, 13:56.
  - Benátky nad Jizerou, autobusové stanoviště → Brandýs n.L.-St.Bol., nádraží: slots :15, typed 14, running 32 min. Window: slots 16:15, 17:15 against real 15:45, 16:15, 17:15 → Step 4 ok. Day 5–23: 4 exact, 4 within 3 of 14. Off 12–20 h: 13:05, 15:07, 15:45.

### 669 Brandýs nad Labem-Stará Boleslav - Dřísy - Mečeříž

- **Core points:** Brandýs n.L.-St.Bol., autobusové stanoviště; Dřísy; Sudovo Hlavno; Kostelní Hlavno, u kostela; Mečeříž. Model window 15:30–17:30 (the line's anchor).
- Afternoon Brandýs → Sudovo Hlavno every 30 from 15:05 to 17:35 (six departures), back only 15:33, 16:18, 16:48, 17:33, 18:13: an
  outstation line (the first trips 4:18–6:06 start in the villages). At the inbound rate: every 120 with three slots each way, out
  15:05, 15:35, 16:05 (typed 4, 34, 64; in the game also 17:05, 17:35, 18:05), back 15:33, 16:18, 16:48 (17:33 ≡ 15:33): all exact.
  Every 30 / 60 with two slots fail back (15:48, 17:18 empty). By the waits (the 290 rule) 16:35 is the departure left off: with
  15:05, 15:35, 16:05 the buses turn in 8–28 min and the line needs 2 buses; 15:35, 16:05, 16:35 would need 3 (16:35 → 16:55 waits
  until 17:33).
- **Changed on 2 Nov (independent review):** out slots 15:35, 16:05, 16:35 → 15:05, 15:35, 16:05 (typed 34, 64, 94 → 4, 34, 64), 3 → 2
  buses; the earlier text's "any three consecutive departures need the same 3 buses" was wrong (15:05, 15:35, 16:05 need 2). In the
  game the Brandýs, autobusové stanoviště entry changes (Also at 94 → Offset 4); the Sudovo Hlavno entry and 669 Mečeříž are unchanged.
- The 15:35, 17:35 and 19:35 run via Dřísy, železniční stanice and Křenek (31 min instead of 18); routing all three slots that way
  costs 13 min a trip, so the line runs direct and Křenek is on 669 Mečeříž (path audit flag on the 15:35 slot, explained).
- 669 Mečeříž (every 240): the Sudovo Hlavno – Kostelní Hlavno – Mečeříž road and Kostelní Hlavno, u kostela (otherwise only two 670
  short trips). Out Brandýs 14:35 (the real 14:35 turns at Kostelní Hlavno; 18:35 runs to Mečeříž), via Křenek; back Mečeříž 17:43,
  the real 13:43 one period later (the 19:05 would leave before the bus arrives: 2 buses).
- **669** every 120, need 2 (waits autobusové stanoviště 28/28/13, Sudovo Hlavno 23/8/23):
  - Brandýs n.L.-St.Bol., autobusové stanoviště → Sudovo Hlavno: slots 13:05, 13:35, 14:05, 15:05, 15:35, 16:05, 17:05, 17:35, 18:05, typed 4, 34, 64, running 20 min. Window: slots 15:35, 16:05, 17:05 against real 15:35, 16:05, 16:35, 17:05 → Step 4 ok. Day 5–23: 6 exact, 6 within 3 of 9. Off 12–20 h: 16:35. Knot check, model vs real (worst, min): Dřísy 11; Sudovo Hlavno 11.
  - Sudovo Hlavno → Brandýs n.L.-St.Bol., autobusové stanoviště: slots 13:33, 14:18, 14:48, 15:33, 16:18, 16:48, 17:33, 18:18, 18:48, typed 32, 77, 107, running 19 min. Window: slots 15:33, 16:18, 16:48 against real 15:33, 16:18, 16:48 → Step 4 ok. Day 5–23: 4 exact, 5 within 3 of 8. Off 12–20 h: 18:13.
- **669 Mečeříž** every 240, need 1 (waits autobusové stanoviště 25, Mečeříž 150):
  - Brandýs n.L.-St.Bol., autobusové stanoviště → Mečeříž: slots 14:35, 18:35, typed 94, running 38 min. Window: slots none against real none → Step 4 ok. Day 5–23: 2 exact, 2 within 3 of 11. Off 12–20 h: 12:20, 13:05, 14:05. Knot check, model vs real (worst, min): Dřísy 241; Sudovo Hlavno 241; u kostela 241; Mečeříž 241.
  - Mečeříž → Brandýs n.L.-St.Bol., autobusové stanoviště: slots 13:43, 17:43, typed 42, running 27 min. Window: slots none against real none → Step 4 ok. Day 5–23: 1 exact, 1 within 3 of 7. Off 12–20 h: 12:50, 14:50, 19:05. Knot check, model vs real (worst, min): autobusové stanoviště 155; Dřísy 155; Sudovo Hlavno 155; u kostela 155.

### 670 Brandýs nad Labem-Stará Boleslav - Sudovo Hlavno - Mečeříž

- **Core points:** Brandýs n.L.-St.Bol., autobusové stanoviště; Hlavenec; Kostelní Hlavno, u pomníku; Mečeříž. Model window 15:30–17:30 (the line's anchor).
- Brandýs 15:37, 16:37, 18:05; Mečeříž 16:02, 17:02, 18:32 (and Kostelní Hlavno / Sudovo Hlavno shorts). Hourly :37 / :02 passes in
  the window, 1 bus. Kostelní Hlavno, u kostela → Brandýs 13:40 and 15:07 follow a 669 arrival (2 of 3): 669 buses going back.
- **670** every 60, need 1 (waits autobusové stanoviště 19, Mečeříž 8):
  - Brandýs n.L.-St.Bol., autobusové stanoviště → Mečeříž: slots :37, typed 36, running 17 min. Window: slots 15:37, 16:37 against real 15:37, 16:37 → Step 4 ok. Day 5–23: 2 exact, 2 within 3 of 6. Off 12–20 h: 13:07, 18:05.
  - Mečeříž → Brandýs n.L.-St.Bol., autobusové stanoviště: slots :02, typed 1, running 16 min. Window: slots 16:02, 17:02 against real 16:02, 17:02 → Step 4 ok. Day 5–23: 2 exact, 4 within 3 of 7. Off 12–20 h: 18:32.

### 685 Strančice - Mnichovice - Zvánovice - Černé Voděrady

- **Core points:** Strančice, železniční stanice; Mnichovice, náměstí; Ondřejov, Třemblat; Zvánovice; Černé Voděrady. Model window 15:30–17:30 (the line's anchor).
- Hourly :32 / :58 in the peak (15:32, 16:32; 15:58, 16:58), the bus turning at once at Černé Voděrady (`lay` 0): 1 bus.
- **685** every 60, need 1 (waits železniční stanice 6, Černé Voděrady 0):
  - Strančice, železniční stanice → Černé Voděrady: slots :32, typed 31, running 26 min. Window: slots 15:32, 16:32 against real 15:32, 16:32 → Step 4 ok. Day 5–23: 2 exact, 6 within 3 of 9. Off 12–20 h: 19:04.
  - Černé Voděrady → Strančice, železniční stanice: slots :58, typed 57, running 28 min. Window: slots 15:58, 16:58 against real 15:58, 16:58 → Step 4 ok. Day 5–23: 2 exact, 5 within 3 of 7. Off 12–20 h: 14:25, 18:25.

### 686 Úvaly - Říčany

- **Core points:** Říčany, Wolkerova; Říčany, Masarykovo náměstí; Křenice; Škvorec, Třebohostice; Úvaly, železniční stanice. Model window 15:30–17:30 (the line's anchor).
- Hourly exact both ways (Říčany, Wolkerova :00; Úvaly :11). 8 of 13 arrivals at Wolkerova leave again within 5 min.
- **686** every 60, need 2 (waits Wolkerova 3, železniční stanice 24):
  - Říčany, Wolkerova → Úvaly, železniční stanice: slots :00, typed 59, running 47 min. Window: slots 16:00, 17:00 against real 16:00, 17:00 → Step 4 ok. Day 5–23: 10 exact, 10 within 3 of 13.
  - Úvaly, železniční stanice → Říčany, Wolkerova: slots :11, typed 10, running 46 min. Window: slots 16:11, 17:11 against real 16:11, 17:11 → Step 4 ok. Day 5–23: 7 exact, 9 within 3 of 12.

### 761 Velké Popovice - Kamenice,Všedobrovice - Velké Popovice

- **Core points:** Velké Popovice, Todice; Velké Popovice, pivovar; Velké Popovice, Lojovice; Kamenice, Všedobrovice. Model window 16:00–18:00 (anchor set by hand).
- A 30-min loop from Velké Popovice, Todice: 13:21, 14:21, 14:55, 15:50, 16:55, 17:55, 18:27. The real minute is :55 (14:55, 16:55,
  17:55 exact). Modelled hourly at :55 with the anchor at 16:30 by hand (window 16:00–18:00, both slots exact); 15:50 is 5 min off
  the pattern, 13:21, 14:21 and 18:27 off. 1 bus.
- **Changed on 2 Nov (independent review):** slot :53 (a minute no trip leaves at, chosen so Step 4 passed at 16:00: the method's "504
  at :01 instead of :06" mistake) → the real :55 (typed 52 → 54), anchor 16:30. In the game: Todice Offset 52 → 54.
- **761** every 60, need 1 (waits Todice 30):
  - Velké Popovice, Todice → Velké Popovice, Todice: slots :55, typed 54, running 30 min. Window: slots 16:55, 17:55 against real 16:55, 17:55 → Step 4 ok. Day 5–23: 4 exact, 4 within 3 of 8. Off 12–20 h: 13:21, 14:21, 15:50, 18:27. Knot check, model vs real (worst, min): Lojovice 7; Všedobrovice 16.

### 765 Sibřina - Říčany - Jesenice

- **Core points:** Jesenice [PZ]; Modletice, Doubravice; Říčany, Masarykovo náměstí; Křenice; Sibřina; Sibřina, škola. Model window 15:30–17:30 (the line's anchor).
- Timed at the Sibřina end: back from Sibřina :19 all afternoon (the trips until 16:17 start 2 min earlier at Sibřina, škola); out
  passing Křenice :46 every trip from 15:46, while the Jesenice departure moves from :45 (via Říčany, Olivovna, 79 min) to :52
  (shorter way, 72 min) at 16:52. The way out is read at Křenice (`knot_rt` 61, the window trips' own time), the line takes the
  Olivovna way of the window trips 14:45 / 15:45 and ends at Sibřina, škola (explicit stop list from the 14:45 trip, `rt` 81 =
  79 + 2). 3 buses. Sibřina, škola is also on 303's school trips.
- **765** every 60, need 3 (waits Jesenice [PZ] 13, škola 11):
  - Jesenice [PZ] → Sibřina, škola (read at Křenice: 0:46, terminal = knot − 61): slots :45, typed 44, running 81 min. Window: slots 15:45, 16:45 against real 15:45, 16:45 → Step 4 ok. Day 5–23: 5 exact, 5 within 3 of 10. Off 12–20 h: 12:15, 13:15. Knot check, model vs real (worst, min): Doubravice 623; Masarykovo náměstí 623; Křenice 7; Sibřina 7; škola 623.
  - Sibřina, škola → Jesenice [PZ] (read at Sibřina: 0:19, terminal = knot − 2): slots :17, typed 16, running 75 min. Window: slots 16:17, 17:17 against real 16:17, 17:17 → Step 4 ok. Day 5–23: 7 exact, 7 within 3 of 10.

### 823 Jirny - Úvaly - Škvorec - Doubravčice

- **Core points:** Úvaly, železniční stanice; Škvorec, náměstí; Přišimasy; Doubravčice. Model window 15:30–17:30 (the line's anchor).
- Úvaly – Škvorec every 30 (:03 / :17) and Úvaly – Doubravčice hourly (:43 / :52). The Škvorec legs use `notvia` Doubravčice.
  823 waits 46 min at Doubravčice (real: the slots are fixed by the timetable): 2 buses.
- **823** every 60, need 2 (waits železniční stanice 28, Doubravčice 46):
  - Úvaly, železniční stanice → Doubravčice: slots :43, typed 42, running 23 min. Window: slots 15:43, 16:43 against real 15:43, 16:43 → Step 4 ok. Day 5–23: 11 exact, 11 within 3 of 14. Off 12–20 h: 13:03.
  - Doubravčice → Úvaly, železniční stanice: slots :52, typed 51, running 23 min. Window: slots 15:52, 16:52 against real 15:52, 16:52 → Step 4 ok. Day 5–23: 7 exact, 7 within 3 of 13. Off 12–20 h: 12:22, 13:32.
- **823 Škvorec** every 30, need 1 (waits železniční stanice 8, náměstí 6):
  - Úvaly, železniční stanice → Škvorec, náměstí: slots :03 / :33, typed 2, running 8 min. Window: slots 15:33, 16:03, 16:33, 17:03 against real 15:33, 16:03, 16:33, 17:03 → Step 4 ok. Day 5–23: 14 exact, 14 within 3 of 17.
  - Škvorec, náměstí → Úvaly, železniční stanice: slots :17 / :47, typed 16, running 8 min. Window: slots 15:47, 16:17, 16:47, 17:17 against real 15:47, 16:17, 16:47, 17:17 → Step 4 ok. Day 5–23: 13 exact, 13 within 3 of 18.

### X391 Úvaly - Úvaly,Radlická čtvrť

- **Core points:** Úvaly, Radlická čtvrť; Úvaly, náměstí Arnošta z Pardubic; Úvaly, železniční stanice; Úvaly, OC Pražská. Model window 15:30–17:30 (the line's anchor).
- Replacement line X391, in both the 29 Sep and the 1 Nov PID feeds, so long works, modelled as they run (owner's rule;
  `00_config.py` now lists only the rail XS / XR lines automatically). Whole day: Radlická čtvrť :38 hourly until 11:38, then :23
  (12:23–21:23); station :18 until 11:18, then :03 (12:03–23:03). Every trip runs the station loop (Elektromechanika, OC Pražská,
  MŠ Pražská) as well. Hourly :23 / :03, exact on every afternoon trip; 1 bus, as the live map shows (bus 7981 on every trip
  11:38–17:23 on 2 Nov). The out leg's path and running time are set to the whole trip (`stops` from the 16:23 trip, `rt` 13): the
  builder would end it at the first station passing (4 min).
- **Changed on 2 Nov (coordinator):** designed (was listed automatically as a replacement bus); the coverage exception for Úvaly,
  Radlická čtvrť is removed. 391's card no longer calls X391 unmodelled (no slot change).
- **X391** every 60, need 1 (waits Radlická čtvrť 4, železniční stanice 27):
  - Úvaly, Radlická čtvrť → Úvaly, železniční stanice: slots :23, typed 22, running 13 min. Window: slots 16:23, 17:23 against real 16:23, 17:23 → Step 4 ok. Day 5–23: 10 exact, 10 within 3 of 20.
  - Úvaly, železniční stanice → Úvaly, Radlická čtvrť: slots :03, typed 2, running 16 min. Window: slots 16:03, 17:03 against real 16:03, 17:03 → Step 4 ok. Day 5–23: 11 exact, 11 within 3 of 18.

### MHD Říčany 1 Oáza/Kuří - Strašín

- **Core points:** Říčany, Kuří; Říčany, Masarykovo náměstí; Říčany, nádraží; Říčany, Olivovna; Říčany, Strašín. Model window 15:30–17:30 (the line's anchor).
- Every 30 exact (Kuří :05 / :35, Strašín :03 / :33, 12:33–17:35). 2 buses.
- **MHD Říčany 1** every 30, need 2 (waits Kuří 8, Strašín 2):
  - Říčany, Kuří → Říčany, Strašín: slots :05 / :35, typed 4, running 26 min. Window: slots 15:35, 16:05, 16:35, 17:05 against real 15:35, 16:05, 16:35, 17:05 → Step 4 ok. Day 5–23: 25 exact, 25 within 3 of 25.
  - Říčany, Strašín → Říčany, Kuří: slots :03 / :33, typed 2, running 24 min. Window: slots 15:33, 16:03, 16:33, 17:03 against real 15:33, 16:03, 16:33, 17:03 → Step 4 ok. Day 5–23: 25 exact, 25 within 3 of 25.

### MHD Říčany 2 Strašín,Pastelkov - Oáza

- **Core points:** Říčany, Strašín, Pastelkov; Říčany, Radošovice, Haškova; Říčany, nádraží; Říčany, OÁZA. Model window 15:00–17:00 (anchor set by hand).
- Every 30 (Pastelkov :20 / :50 to 16:50, OÁZA :21 / :51 to 17:21), hourly after. Anchor 15:30 by hand: at 16:00 Pastelkov's 17:20
  slot falls after the switch to hourly (3 of 4 window slots, Step 4 fails by one).
- **MHD Říčany 2** every 30, need 2 (waits Pastelkov 6, OÁZA 11):
  - Říčany, Strašín, Pastelkov → Říčany, OÁZA: slots :20 / :50, typed 19, running 20 min. Window: slots 15:20, 15:50, 16:20, 16:50 against real 15:20, 15:50, 16:20, 16:50 → Step 4 ok. Day 5–23: 25 exact, 25 within 3 of 25.
  - Říčany, OÁZA → Říčany, Strašín, Pastelkov: slots :21 / :51, typed 20, running 23 min. Window: slots 15:21, 15:51, 16:21, 16:51 against real 15:21, 15:51, 16:21, 16:51 → Step 4 ok. Day 5–23: 25 exact, 25 within 3 of 25.

### MHD Říčany 3 Jažlovice - Pacov

- **Core points:** Říčany, Jažlovice; Říčany, Masarykovo náměstí; Říčany, nádraží; Říčany, Pacov. Model window 15:30–17:30 (the line's anchor).
- Every 30 exact at both ends (:02 / :32). 2 buses.
- **MHD Říčany 3** every 30, need 2 (waits Jažlovice 3, Pacov 4):
  - Říčany, Jažlovice → Říčany, Pacov: slots :02 / :32, typed 1, running 26 min. Window: slots 15:32, 16:02, 16:32, 17:02 against real 15:32, 16:02, 16:32, 17:02 → Step 4 ok. Day 5–23: 25 exact, 25 within 3 of 25.
  - Říčany, Pacov → Říčany, Jažlovice: slots :02 / :32, typed 1, running 27 min. Window: slots 15:32, 16:02, 16:32, 17:02 against real 15:32, 16:02, 16:32, 17:02 → Step 4 ok. Day 5–23: 25 exact, 25 within 3 of 25.

### MHD Říčany 7 Olivovna - Srnčí

- **Core points:** Říčany, Olivovna; Říčany, Masarykovo náměstí; Říčany, nádraží; Říčany, Srnčí. Model window 15:30–17:30 (the line's anchor).
- Hourly exact (Olivovna :14, Srnčí :42), one bus turning at once at both ends.
- **MHD Říčany 7** every 60, need 1 (waits Olivovna 5, Srnčí 1):
  - Říčany, Olivovna → Říčany, Srnčí: slots :14, typed 13, running 27 min. Window: slots 16:14, 17:14 against real 16:14, 17:14 → Step 4 ok. Day 5–23: 15 exact, 15 within 3 of 15.
  - Říčany, Srnčí → Říčany, Olivovna: slots :42, typed 41, running 27 min. Window: slots 15:42, 16:42 against real 15:42, 16:42 → Step 4 ok. Day 5–23: 15 exact, 15 within 3 of 15.

### MHD Říčany 9 Olivovna - Obchodní

- **Core points:** Říčany, Obchodní; Říčany, Pod Lihovarem; Říčany, nádraží; Říčany, Olivovna. Model window 15:00–17:00 (anchor set by hand).
- Every 30 (Obchodní :22 / :52 to 17:22, Olivovna :23 / :53 to 16:53), hourly after. Anchor 15:30 by hand, as MHD 2.
- **MHD Říčany 9** every 30, need 2 (waits Obchodní 10, Olivovna 12):
  - Říčany, Obchodní → Říčany, Olivovna: slots :22 / :52, typed 21, running 19 min. Window: slots 15:22, 15:52, 16:22, 16:52 against real 15:22, 15:52, 16:22, 16:52 → Step 4 ok. Day 5–23: 23 exact, 23 within 3 of 23.
  - Říčany, Olivovna → Říčany, Obchodní: slots :23 / :53, typed 22, running 19 min. Window: slots 15:23, 15:53, 16:23, 16:53 against real 15:23, 15:53, 16:23, 16:53 → Step 4 ok. Day 5–23: 23 exact, 23 within 3 of 23.

### 397 Praha,Opatov - Modletice — not modelled

- Shift line of the Modletice warehouses (Opatov – D1 – Modletice, Kaufland / Doubravice): in the afternoon out of Opatov 13:30, 14:20, 16:20, 17:50 and back 14:53, 15:23, 15:53 from Doubravice and 16:45, 17:20, 18:12 from Kaufland, no repeating pattern and twice as many trips back as out. Step 8: every stop it serves 13:00–19:00 (Modletice, Doubravice, rozcestí, V hůrce, Kaufland) is on modelled lines: Modletice, Doubravice, V hůrce and Kaufland on 328 and 765, Modletice, rozcestí on 363 (Prague bus sheet).
- DPP's shift line to the Modletice warehouses: no pattern (out 13:30, 14:20, 16:20, 17:50; back 14:53, 15:23, 15:53, 16:45, 17:20,
  18:12) and its stops are all covered: Modletice, Doubravice, V hůrce and Kaufland on 328 and 765, Modletice, rozcestí on 363
  (Prague bus sheet). Listed, as Step 8 says for a shift line whose stops are covered.
- **Changed on 2 Nov (independent review):** reason corrected: Modletice, rozcestí is on 363 (Prague bus sheet), not 765 (765 serves the
  different stop Modletice, rozcestí Doubravice).

### 557 Světice - Svojetice - Louňovice — not modelled

- School line: in the afternoon only Louňovice, I.hráz → Mukařov → Tehovec → Svojetice → Svojetice, na vyhlídce (12:34, 13:29, 14:24, 15:49, 16:44) and one Světice, škola → Mukařov trip (15:10); no trip back after 7:32. Step 8: every stop it serves 13:00–19:00 is on modelled lines: Louňovice, Mukařov and Svojetice on 489, Tehovec, Svojetice, K Tehovci and Svojetice, na vyhlídce on 385, Klokočná on 489, Všestary on 489, 494 and 582, Světice, škola on 494.
- One-way school trips towards Svojetice; every stop is on 489, 385, 494 and 582.
- **Changed on 2 Nov (independent review):** reason corrected: Světice, škola is on 494, not 582 (582 serves Světice).

### 671 Jenštejn - Přezletice - Záryby — not modelled

- School line: in the afternoon only trips out of Přezletice, Panská pole (13:30–17:10, to Jenštejn, Hradní or Dehtáry and to Veleň – Brázdim – Polerady – Záryby), none back (its three back trips run at 7:19–7:30). Step 8: every stop it serves 13:00–19:00 is on modelled lines: Přezletice, Panská pole on 302 (its way to Veleň runs via Panská pole), Podolanka on 375, Jenštejn on 367, Jenštejn, Hradní, Dehtáry and Domov seniorů on 376, 378 and 396 (Prague bus sheet), Veleň, Brázdim and Polerady on 321, Záryby on 482, Polerady, rozcestí on 377 Brázdim (Mělnicko sheet; a coverage exception here).
- Its afternoon is one-way school trips out of Přezletice, Panská pole; Panská pole was put on 302's way back so it keeps a modelled
  line. Polerady, rozcestí (only 671 here) is served all afternoon by 377 Brázdim on the Mělnicko sheet (coverage exception).
- **Changed on 2 Nov (independent review):** reason reworded: Podolanka is on 375, Jenštejn on 367, Jenštejn, Hradní, Dehtáry and
  Domov seniorů on 376, 378 and 396 (Prague bus sheet) (the earlier text named 396 / 367 for Podolanka).

### 677 Úvaly - Jirny - Vyšehořovice - Nehvizdy — not modelled

- School line from Nehvizdy, škola: in the afternoon only one way (Nehvizdy 13:00, 14:05, 15:15, 16:20 → Mochov – Vyšehořovice – Tuklaty → Úvaly; 12:05 to Vyšehořovičky), no trip back after 7:18. Step 8: every stop it serves 13:00–19:00 is on modelled lines: Nehvizdy on 655 and 354, Mochov on 354, Tuklaty and Úvaly on 484 and 655; the three Vyšehořovice stops are served all afternoon by 662 (about every 20 min, modelled on the Kolínsko sheet; coverage exceptions here, checked in the cross-sheet pass).
- One-way school line Nehvizdy → Úvaly in the afternoon. The three Vyšehořovice stops are served about every 20 min by 662,
  modelled on the Kolínsko sheet (checked in their schedule.json on 2 Nov: all three on the 662 line); coverage exceptions here. An
  every-480 677 line (Nehvizdy 16:20 / Úvaly 7:00, 1 bus) was built and dropped for that reason.

### 876 Brandýs nad Labem-Stará Boleslav - Neratovice — not modelled

- School line Brandýs nad Labem, autobusové stanoviště – Kostelec nad Labem – Neratovice, Lobkovice, škola, one trip each way (8:08 out, 14:05 back). Step 8: its stops are on 482 (Brandýs, náměstí, Pražská, nádraží, Kostelec nad Labem, u váhy), and Neratovice, Lobkovice, škola (okres Mělník) is on 480 (Mělnicko sheet).
- One school trip each way; Neratovice, Lobkovice, škola (okres Mělník) is on 480 (Mělnicko sheet: checked in its schedule.json),
  the other stops on 482. An every-480 876 line (1 bus) was built and dropped.

### MHD Říčany 91 Obchodní - Olivovna — not modelled

- No afternoon trip: one morning trip (Obchodní 7:23 → Srnčí → Radošovice → Olivovna), a school run; its stops are on MHD Říčany 2, 3, 7 and 9 and 385.

### MHD Říčany 92 Pod Lihovarem - Strašín,Pampelišková — not modelled

- No afternoon trip: two morning trips (7:36 Pod Lihovarem → Strašín, Pampelišková; 8:08 back), a school run; its stops are on MHD Říčany 1, 2 and 9.

## Summary

| Line | Simutrans line | Every | Slots (real minutes, both ends) | Buses |
|---|---|---|---|---|
| 302 | 302 | 60 | Letňany :01 · u pomníku :32 | 2 |
| 302 | 302 Vinořská | 60 | Letňany :24 / :44 · Vinořská :12 / :52 | 2 |
| 303 | 303 | 30 | Černý Most :03 / :33 · Křenice :07 / :37 | 4 |
| 321 | 321 | 60 | Pražská :04 · Letňany :11 | 2 |
| 328 | 328 | 60 | Opatov :25 · Doubravice :03 | 2 |
| 328 | 328 Čestlice | 60 | Opatov :55 · Čestlice :59 | 2 |
| 335 | 335 | 120 | Budějovická 13:20, 14:06, 15:20, 16:06, 17:20, 18:06 · kulturní dům 13:09, 14:24, 15:09, 16:24, 17:09, 18:24 | 3 |
| 343 | 343 | 60 | Nádraží Klánovice-sever :10 · hájovna :36 | 1 |
| 343 | 343 Zeleneč | 480 | Nádraží Klánovice-sever 13:05 · Svémyslice 13:29 | 1 |
| 344 | 344 | 60 | Černý Most :18 · u rybníka :50 · škola :00 · u rybníka :07 · Černý Most :48 · u rybníka :37 | 3 |
| 346 | 346 | 30 | Černý Most :25 / :55 | 2 |
| 353 | 353 | 60 | Černý Most :43 · Svémyslice :10 | 1 |
| 353 | 353 Brandýs | 60 | Černý Most :13 · nádraží :22 | 2 |
| 353 | 353 Mstětice | 480 | Černý Most 16:28 · U Tří svatých 15:24 | 1 |
| 354 | 354 | 60 | Černý Most :00 · Mochov :31 | 1 |
| 354 | 354 Mochovská | 60 | Černý Most :30 · Mochovská :06 | 1 |
| 354 | 354 LE&CO | 480 | Černý Most 17:10 · LE&CO 17:35 | 1 |
| 357 | 357 | 60 | Opatov :45 · Čestlice :11 | 1 |
| 357 | 357 Průhonice | 60 | Opatov :15 · Průhonice :33 | 1 |
| 367 | 367 | 30 | Černý Most :05 / :35 · autobusové stanoviště :17 / :47 | 3 |
| 371 | 371 | 30 | Kobylisy :15 / :45 · závod :05 / :35 | 3 |
| 371 | 371 Astrapark | 120 | Kobylisy 13:08, 13:23, 15:08, 15:23, 17:08, 17:23 · Astrapark 13:33, 14:03, 15:33, 16:03, 17:33, 18:03 | 2 |
| 371 | 371 Klecánky | 120 | Kobylisy 13:38, 14:38, 15:38, 16:38, 17:38, 18:38 · Klecánky 13:02, 14:26, 15:02, 16:26, 17:02, 18:26 | 2 |
| 371 | 371 Vodochody | 480 | Kobylisy 14:08 · Hoštice 14:35 | 1 |
| 373 | 373 | 120 | Kobylisy 13:32, 14:12, 14:52, 15:32, 16:12, 16:52, 17:32, 18:12, 18:52 · Ke Stadionu 13:11, 13:38, 14:24, 15:11, 15:38, 16:24, 17:11, 17:38, 18:24 | 3 |
| 374 | 374 | 60 | Kobylisy :00 / :30 · Máslovice :11 / :38 | 3 |
| 375 | 375 | 15 | železniční stanice :03 / :18 / :33 / :48 · Českomoravská :00 / :15 / :30 / :45 | 7 |
| 379 | 379 | 30 | autobusové stanoviště :14 / :44 · Černý Most :15 / :45 | 2 |
| 385 | 385 | 60 | Opatov :02 · Zvánovice :45 | 3 |
| 385 | 385 Nupaky | 30 | Opatov :17 / :47 · hotel :18 / :48 | 2 |
| 385 | 385 Říčany | 60 | Opatov :32 · Olivovna :42 | 2 |
| 391 | 391 | 60 | Nádraží Klánovice :07 · OC Pražská :50 | 2 |
| 411 | 411 | 60 | Kobylisy :55 · Holosmetky :16 | 1 |
| 411 | 411 Brnky | 60 | Kobylisy :25 · Brnky :42 | 1 |
| 461 | 461 | 60 | železniční stanice :07 · kulturní dům :50 | 2 |
| 461 | 461 Velké Popovice | 60 | železniční stanice :37 · pivovar :32 | 2 |
| 462 | 462 | 240 | železniční stanice 14:55, 18:55 · SŠŘ 15:08 · železniční stanice 15:37 · Všešímy 16:04 | 1 |
| 469 | 469 | 120 | železniční stanice 14:07, 16:07, 18:07 · Olivovna 13:02, 15:02, 17:02 | 1 |
| 482 | 482 | 30 | autobusové stanoviště :09 / :39 · autobusové nádraží :15 / :45 | 6 |
| 482 | 482 Rožkovo údolí | 480 | autobusové nádraží 15:01 · Rožkovo údolí 15:33 | 1 |
| 484 | 484 | 30 | železniční stanice :14 / :44 | 1 |
| 489 | 489 | 60 | železniční stanice :34 · Louňovice :29 | 2 |
| 490 | 490 | 120 | železniční stanice 13:02, 13:34, 14:04, 15:02, 15:34, 16:04, 17:02, 17:34, 18:04 · náměstí 13:13, 14:13, 14:43, 15:13, 16:13, 16:43, 17:13, 18:13, 18:43 | 3 |
| 492 | 492 | 60 | náměstí :54 · Černé Voděrady :52 | 2 |
| 494 | 494 | 240 | železniční stanice 14:34, 18:34 · Wolkerova 16:41 | 1 |
| 582 | 582 | 120 | železniční stanice 14:34, 16:34, 18:34 · Olivovna 13:54, 15:54, 17:54 | 1 |
| 652 | 652 | 120 | náměstí 13:20, 15:20, 17:20 · Krymlov 14:17, 16:17, 18:17 | 1 |
| 653 | 653 | 120 | náměstí 13:50, 15:50, 17:50 · Poddubí 14:47, 16:47, 18:47 | 1 |
| 655 | 655 | 60 | železniční stanice :35 · nádraží :38 | 2 |
| 655 | 655 Čelákovice | 60 | nádraží :21 · železniční stanice :55 | 1 |
| 656 | 656 | 60 | U Kostela :02 | 1 |
| 657 | 657 | 60 | nádraží :25 · závod :15 | 2 |
| 666 | 666 | 60 | autobusové stanoviště :35 · pošta :52 | 1 |
| 667 | 667 | 60 | nádraží :26 · autobusové stanoviště :15 | 2 |
| 669 | 669 | 120 | autobusové stanoviště 13:05, 13:35, 14:05, 15:05, 15:35, 16:05, 17:05, 17:35, 18:05 · Sudovo Hlavno 13:33, 14:18, 14:48, 15:33, 16:18, 16:48, 17:33, 18:18, 18:48 | 2 |
| 669 | 669 Mečeříž | 240 | autobusové stanoviště 14:35, 18:35 · Mečeříž 13:43, 17:43 | 1 |
| 670 | 670 | 60 | autobusové stanoviště :37 · Mečeříž :02 | 1 |
| 685 | 685 | 60 | železniční stanice :32 · Černé Voděrady :58 | 1 |
| 686 | 686 | 60 | Wolkerova :00 · železniční stanice :11 | 2 |
| 761 | 761 | 60 | Todice :55 | 1 |
| 765 | 765 | 60 | Jesenice [PZ] :45 · škola :17 | 3 |
| 823 | 823 | 60 | železniční stanice :43 · Doubravčice :52 | 2 |
| 823 | 823 Škvorec | 30 | železniční stanice :03 / :33 · náměstí :17 / :47 | 1 |
| X391 | X391 | 60 | Radlická čtvrť :23 · železniční stanice :03 | 1 |
| MHD Říčany 1 | MHD Říčany 1 | 30 | Kuří :05 / :35 · Strašín :03 / :33 | 2 |
| MHD Říčany 2 | MHD Říčany 2 | 30 | Pastelkov :20 / :50 · OÁZA :21 / :51 | 2 |
| MHD Říčany 3 | MHD Říčany 3 | 30 | Jažlovice :02 / :32 · Pacov :02 / :32 | 2 |
| MHD Říčany 7 | MHD Říčany 7 | 60 | Olivovna :14 · Srnčí :42 | 1 |
| MHD Říčany 9 | MHD Říčany 9 | 30 | Obchodní :22 / :52 · Olivovna :23 / :53 | 2 |
| 397 | not modelled | | Shift line of the Modletice warehouses (Opatov – D1 – Modletice, Kaufland / Doubravice): i… | 0 |
| 557 | not modelled | | School line: in the afternoon only Louňovice, I.hráz → Mukařov → Tehovec → Svojetice → Svo… | 0 |
| 671 | not modelled | | School line: in the afternoon only trips out of Přezletice, Panská pole (13:30–17:10, to J… | 0 |
| 677 | not modelled | | School line from Nehvizdy, škola: in the afternoon only one way (Nehvizdy 13:00, 14:05, 15… | 0 |
| 876 | not modelled | | School line Brandýs nad Labem, autobusové stanoviště – Kostelec nad Labem – Neratovice, Lo… | 0 |
| 953 | not modelled | | Night line: the sheets model the weekday afternoon (owner, 25 Sep 2026: no night lines).… | 0 |
| 958 | not modelled | | Night line: the sheets model the weekday afternoon (owner, 25 Sep 2026: no night lines).… | 0 |
| 959 | not modelled | | Night line: the sheets model the weekday afternoon (owner, 25 Sep 2026: no night lines).… | 0 |
| MHD Říčany 91 | not modelled | | No afternoon trip: one morning trip (Obchodní 7:23 → Srnčí → Radošovice → Olivovna), a sch… | 0 |
| MHD Říčany 92 | not modelled | | No afternoon trip: two morning trips (7:36 Pod Lihovarem → Strašín, Pampelišková; 8:08 bac… | 0 |
| XS9 | not modelled | | Rail replacement bus (NAD) for engineering works on the railway: the rail sheets model the… | 0 |
| 325 | on the Prague bus sheet | | companion line (owner, 30 Oct 2026) | – |
| 329 | on the Prague bus sheet | | companion line (owner, 30 Oct 2026) | – |
| 363 | on the Prague bus sheet | | companion line (owner, 30 Oct 2026) | – |
| 364 | on the Prague bus sheet | | companion line (owner, 30 Oct 2026) | – |
| 366 | on the Prague bus sheet | | companion line (owner, 30 Oct 2026) | – |
| 376 | on the Prague bus sheet | | companion line (owner, 30 Oct 2026) | – |
| 378 | on the Prague bus sheet | | companion line (owner, 30 Oct 2026) | – |
| 396 | on the Prague bus sheet | | companion line (owner, 30 Oct 2026) | – |

**Totals: 69 Simutrans lines, 128 buses** (50 lines modelled, 7 not modelled by hand, 4 listed automatically, 8 on the Prague bus sheet).

## Shared terminals, trunks and bunching (Step 5, check 6)

All slots are real departure minutes except the ones named in the head of this file, so every same-minute departure in the game
is also real: Strančice 14:07 / 16:07 / 18:07 (461 to Kunice and 469 to Svojšovice, different roads); Strančice :34 (489 and the
490 15:34 share Všestary, Vávrov – Mnichovice, as in the timetable) and :32 (685, same road); Brandýs, autobusové stanoviště :35 –
:39 (666, 669, 670, 482 on four different roads); Černý Most :03 / :13 / :18 (303, 353, 344 on the Horní Počernice trunk, 5 min
apart as real). The model's own minutes: 411 Brnky
:25 (10 min after 371 Řež's :15 out of Kobylisy, different roads after Zdiby); 469 16:07 (real 16:04). Interleaving holds
where the timetable interleaves: 385's three ends every 15 at Opatov, 461's two every 30 at Velké Popovice and Kunice, 371
Astrapark + Klecánky every 30 at Klecany, u hřbitova, 353 + 353 Brandýs every 30 out of Černý Most, 655 + 655 Čelákovice between
Brandýs and Čelákovice, 823 + 823 Škvorec at Škvorec. The companions on the Prague bus sheet (325, 329, 363, 364, 366, 376, 378, 396)
were not changed and are timed from real minutes there, so a coincidence with them is real too.

## Through-running and pooling seen in the 0-minute chain test (for the 2 Nov live map)

- Modelled: 343's Horoušany – Nehvizdy trips inside the 344 circuit (9 of 9 / 8 of 9).
- Named, not modelled: 354 ↔ 662 at Mochov (12 of 17 both ways, across sheets); 335 → 444 at Kamenice (10 of 21) and the 335
  Želivec shorts → 339 (7 of 7); 482's extra trips ending at Brandýs, nádraží → 353 / 655 (2 of 3); 653 → 490 at Ondřejov (3 of 5);
  761 after 363 at Todice (4 of 11); MHD Říčany 7 ↔ 9 and 385 at Olivovna (8 and 5 of 15); 669 → 670 at Kostelní Hlavno (2 of 3);
  at Brandýs, autobusové stanoviště 669 departures after a 379 arrival (12 of 19) or a 367 arrival (10 of 19) and 666 departures
  after a 367 (8 of 14) or 379 (6 of 14) arrival: the Prague buses run on into the villages (why 669 is an outstation line);
  321 → 657 at Mratín (2 of 2, the morning Mratín shorts); at Úvaly, železniční stanice 655 → 823 (6 of 15) and 391 → 484 / 823
  (7 of 11); 686 → 435 at Říčany, Wolkerova (5 of 13, another sheet). All in the sheet's notes (added 2 Nov after the review);
  the Prague ends (302 → 158 at Letňany, 375 → 152 at Českomoravská, 371 / 373 / 374 / 411 with 144 / 200 at Kobylisy, the
  Černý Most lines with 201 / 240): city lines, Prague bus sheet.
- Pooling options inside one real line (not applied; one Simutrans line per destination): 461 at Strančice (3 buses instead of 4),
  328 + 328 Čestlice at Opatov (3 instead of 4), 302 + 302 Vinořská at Letňany (the Veleň bus waits 57 min), 823 + 823 Škvorec at
  Úvaly (the Doubravčice bus waits 46 min at Doubravčice and 28 at Úvaly while the shuttle idles; about 2 buses instead of 3).

## Coverage (Step 9)

- Okres Praha-východ: every stop served 13:00–19:00 is on a Simutrans line of this sheet, or a coverage exception with a reason:
  Polerady, rozcestí (377 Brázdim, Mělnicko sheet);
  Vyšehořovice, Vyšehořovice, Kozovazy and Vyšehořovičky (662, Kolínsko sheet); Strančice, Všechromy (roadside, the sheet-wide
  roadside owner check).
- Outside the Středočeský kraj: none of this oblast's lines leaves the kraj.
- Other Středočeský okresy, stops only this oblast's lines serve (all covered here): Doubravčice, Na Čtvrtích and Masojedy (823),
  Tuklaty, Tlustovousy (484; okres Kolín), Skorkov, Skorkov, Podbrahy, Skorkov, Otradovice and its křižovatka (667; okres Mladá
  Boleslav), Kostelec nad Labem, Na Cihelně and Neratovice, Lobkovice, hřbitov (482), Mělník, Rožkovo údolí and Strážnická (482
  Rožkovo údolí), Úžice, Kopeč and Netřeba (373; okres Mělník), Průhonice, Rozkoš, Tovární, hájovna (357; okres Praha-západ).
  Left to their own sheets (checked in the cross-sheet pass): Postřižín, u kapličky (370 Mělnicko), Neratovice, Lobkovice, škola
  (480 Mělnicko), Benátky nad Jizerou, Kbel, Dražice, Ovčín and Horky nad Jizerou (315 / 699 / 775 Mladoboleslavsko).

## Owner checks

1. 411 Brnky: hourly approximate (1 bus) or every 120 exact in the window (1 bus, half the service).
2. The sheet's roadside stops (one sheet-wide check, as the design brief asks): Strančice, Všechromy, the only one, left as a
   coverage exception (one afternoon trip, 2 min from Všechromy, náves on 469); serving it is a 469 loop line every 480, 1 bus more.

The 482 anchor check of 1 Nov was removed after the review (2 Nov): the 15:00 anchor applies the busiest-two-hours rule; the 4-bus
hourly alternative is in the notes.

## Script problems seen

- `run_oblast.py` line 40 had a literal newline inside an f-string from about 05:20 on 2 Nov (SyntaxError); the coordinator fixed it.
  For the first two runs I used a copy of a wrapper another designer had left in the shared scratchpad (`run_wrap.py`, read in full
  first: it compiles the script in memory with the one character fixed and changes no file); every result here is from the fixed
  script, run directly. `lines.json` is generated from my own design files and was checked byte-identical after the last run.
- `run_oblast.py`'s coverage split puts Prague stops a line serves (Praha, Sychrov; Praha, Tuháňská; Praha, Pramenná; Praha, Betáň)
  into "another Středočeský okres" before they are covered: the `startswith('Praha, ')` test is applied only to the outside-the-kraj
  bucket. Harmless once the Prague bus sheet's coverage is loaded; mislabelled in the draft run.
- `05_schedule.py`: a leg read at a midpoint whose `match` also catches longer trips of the same real line (the short lines 328
  Čestlice, 357 Průhonice, 385 Nupaky, 385 Říčany) needs `notvia` by hand, or the Step 4 audit counts the long trips as the short
  line's departures (it reported FEWER until `notvia` was added). Not a bug, but worth a line in the HKO README.
- The step-4 audit's "FIXABLE" suggestions for the outstation legs (371 Astrapark: every 60 :08 / :23 / :53; 335: every 160 with
  four slots) ignore the inbound rate; they are not taken.

## Open questions

- The live map's afternoon chains were not available (at 06:10 on 2 Nov the poll held only the first morning buses). Before the
  sheet is published, read them against the outstation choices made by the waits (335: Budějovická 15:31 / 16:33 left off; 669:
  Brandýs 16:35; 371 Astrapark: Kobylisy 15:53, 16:08, 16:23, 16:53) and the pooling candidates above. Another choice of
  the departures left off changes no bus count.
- Sibling sheets this design relies on, for the `--final` pass to confirm: Vyšehořovice, Vyšehořovice, Kozovazy and
  Vyšehořovičky on 662 (Kolínsko); Polerady, rozcestí on 377 Brázdim (Mělnicko); Postřižín, u kapličky on 370 (Mělnicko);
  Neratovice, Lobkovice, škola on 480 (Mělnicko); Benátky nad Jizerou, Kbel, Dražice, Ovčín and Horky nad Jizerou on 315 / 699 / 775
  (Mladoboleslavsko). Each was checked in that sheet's draft `schedule.json` on 2 Nov (all on a Simutrans line there except the
  Mladoboleslavsko ones, which were not checked). If one fails: 677 every 480 (Nehvizdy 16:20 / Úvaly 7:00, 1 bus) and 876 every
  480 (Brandýs 8:08 / Lobkovice, škola 14:05, 1 bus) are built and tested in this session's history and come back as they were; a
  Máslovice – Odolena Voda shuttle every 480 (Máslovice 14:57 / Odolena Voda, závod 15:31, 1 bus) for Postřižín; Polerady, rozcestí
  goes into the roadside owner check with Všechromy.

