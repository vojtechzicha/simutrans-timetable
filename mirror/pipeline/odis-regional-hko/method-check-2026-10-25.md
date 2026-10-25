# Bus schedule method, applied to the HKO regional sheet line by line (25 Oct 2026)

The owner asked for every regional sheet to be checked at the level of the Hlučínsko hand check
(`../odis-regional-opavsko/method-check-2026-10-25.md`): "verify all sheets with this level of detail", and "that's the point of
you doing it, so you'll not produce incorrect results". This sheet's lines were all set by hand with the method (v3) on 21 Oct,
but the Step 4 audit of 25 Oct (`../audit/audit-regional-2026-10-25.md`) found 28 of its 71 timed legs failing, on 20 Simutrans
lines of 19 ODIS lines.
Each failing line was read again over the whole day and set against `../bus-schedule-method.md` v4.

- **Data:** the sheet's JDF trips for Tue 20 Oct 2026 (`data/derived/trips.json`), the whole-day reading
  (`data/derived/reading/<L>.txt`) and the ODIS live-map plate chains (13:00–19:30).
- **Step 4 test**, per direction, in the Simutrans line's model window (the line's anchor −30 to +90 min): the window slots
  must equal the real departures ±1, and at least 80 % of the slots need a real departure within 3 min.
- **Typed values** are (real − 61) mod every: every terminus here is a loop. Each real time below is worked out from its
  typed value, (value + 61) mod every.
- **Result:** 68 of 71 timed legs pass (43 before). 25 failing legs are fixed; 3 are left approximate (452 towards Havířov, 543
  back, 543B). Coverage stays 0 uncovered. The sheet needs 63 buses (was 67).

## The rule used for every line

1. Slots sit on real departures (exact minutes), at the line's terminals; a knot gets no timetable.
2. Both directions of a Simutrans line use the same interval and the same number of slots (Step 7).
3. The line keeps its afternoon rate. A candidate that passes Step 4 only by halving the line (an hourly line every 120,
   because the 2-hour window happens to hold one departure) is not taken.
4. Among the candidates that pass: the fewest slots first, then the most departures on the minute over the day, then fewer
   buses. A row that passes only through the window's edges is not taken (583's every 240: its 17:30 slot is the window's end,
   and three of its eight afternoon slots are 9 min off, no better than the failing every 60); there the exact long row is used
   (583 every 480, as 290 on Opavsko), with the simple row on the owner checks.
5. Where nothing passes, the even pattern at the real rate stays, approximate, with the reason (452, 543, 543B).
6. Where a line's busiest two hours come from short trips whose stops are on its Simutrans lines anyway, it is timed in its
   own pattern's hour (282's rule): 369 (anchor 16:00) and 565 (its own window 15:30–17:30).

## Summary

| Line | Published (v3) | Step 4 | Now | Buses |
|---|---|---|---|---|
| 365 | every 90, F-M 15:00 / Podlesí 15:00 | Podlesí 16:30 slot empty (real 16:45, 17:24) | every 80, F-M 16:30 / Podlesí 16:45 | 2 → 2 |
| 366 | every 60, F-M :10 / Podlesí :25 | 17:10 and 17:25 empty | every 120, two slots each way, exact | 2 → 3 |
| 368 | every 180, F-M 12:40 / Podlesí 13:35 | F-M 15:40 empty (real 15:30) | every 180, F-M 15:30 / Podlesí 13:35 | 1 → 1 |
| 369 | every 60, F-M :30 / Podlesí :45, model 14:40 | all four window slots empty | model 16:00, every 120, two slots each way, exact | 3 → 3 |
| 445 | every 60, Podlesí :12 / Poruba :32 | 16:12 and 17:12 empty | every 96, Podlesí 16:47 / Poruba 16:32 | 3 → 2 |
| 448 | every 60, Podlesí :05 / Poliklinika :50 | 15:50 empty (real 15:55) | every 120, two slots each way, exact | 2 → 2 |
| 451 | every 30, Podlesí :00 / Lutyně :16 | 17:00 and 16:46 empty (452 runs them) | same row, read with 452's trips (Step 5) | 3 → 3 |
| 452 | every 60, Podlesí :45 / Lutyně :48 | all four window slots empty | every 120, Podlesí 14:35 / Lutyně 15:35; approximate | 2 → 1 |
| 465 | every 60, Třanovice :16 / Podlesí :40 | 14:40 empty | every 120, Třanovice 14:16 / Podlesí 13:40 | 2 → 1 |
| 532 | every 60, Karviná :20 / Ostrava :39 | 17:20 empty | every 120, two slots each way, exact | 3 → 3 |
| 552 | every 60, Lutyně :30 / Ostrava :35 | 14:30 and 13:35 empty | every 240, two slots each way, exact | 2 → 2 |
| 553 Orlová | every 60, Ostrava :52, empty return | 13:52 empty | every 120, Ostrava 14:52, empty return | 2 → 1 |
| 558 | every 60, Lutyně :02 / Bohumín žst :16 | 14:16 empty | every 120, two slots each way, exact | 2 → 2 |
| 559 | every 480, seven hourly slots :00 / :50 | 16:00, 17:00, 15:50 empty | every 240, two slots each way, exact | 2 → 1 |
| 560 | every 60, Lutyně :40 / Bohumín :00 | 15:40 and 15:00 empty | every 120, two slots each way, exact | 2 → 2 |
| 565 | every 90, Věřňovice 15:15 / Bohumín 14:35, window 13:00–15:00 | 13:45 and 13:05 empty | every 90, Věřňovice 15:15 / Bohumín 16:10, window 15:30–17:30 | 1 → 1 |
| 582 | every 480, back seven slots :39 at Albrechtice | 16:39 empty (real 16:34) | the same, 16:34 | 2 → 2 |
| 583 | every 60, Karviná :21 / nemocnice :31 | 17:21 empty (real 17:30) | every 480, eight slots each way, exact | 2 → 2 |
| 543, 543B | every 120 | 17:04 / 17:12 empty: no evening trip | unchanged, approximate | 2 → 2 |
| **Total** | | **28 failing legs** | **3 left** | **67 → 63** |

Unchanged and passing: 367, 443, 453, 460, 533, 537, 538, 546, 553 (trunk), 553 Autopal, 558 Pudlov, 559 Kovošrot, 563, 565
Kopytov, 581, 582 ČSM, 451 Elektrárna. The Hranečník lines 440, 441, 442, 531, 534, 535 are on the Ostrava sheet.

## The Frýdek-Místek corridor (365–369)

The README's finding stands: the buses rotate between all five lines at both ends (42-1013 runs 369, 365, 366, 365, 369 in one
afternoon), so no line is balanced on its own and Step 5b cannot pair them into clean circuits. One Simutrans line per real
line is kept (pooling stays the owner's choice). Within that, a passing pattern exists for every corridor line, so each was
set by Step 4; 367 already passed.

### 365 Frýdek-Místek – Domaslavice – Soběšovice – Havířov

- **(a) Core points:** F-M, Místek, Anenská; Dobrá, střed; Soběšovice, Na husarůvce; Žermanice, rozcestí; Podlesí. Window 15:30–17:30.
- **(b) Afternoon:** from F-M 13:40 (to Žermanice), 15:00, **16:30**, 17:50; from Podlesí 12:25, 14:05, 15:00, **16:45, 17:24**.
- **(c) Step 4:**

  | Candidate | F-M | Podlesí | Buses |
  |---|---|---|---|
  | every 90, 15:00 / 15:00 (published) | 1/1 slot, ok; 2 exact | 1 slot (16:30) for 2 real, 0 within 3: FAIL | 2 |
  | every 90, 15:00 / 16:45 | ok; 2 exact | ok; 1 exact | 2 |
  | **every 80, 16:30 / 16:45** | ok; 3 exact (9:50, 16:30, 17:50) | ok; 2 exact (14:05, 16:45) | 2 |
  | every 160, 16:30 / 16:45 | ok; 1 exact | ok; 2 exact | 2 |

- **(d) Simutrans line 365:** every 80. F-M Offset 49 (real 12:30, 13:50, 15:10, 16:30, 17:50); Podlesí Offset 64 (real 12:45, 14:05, 15:25, 16:45, 18:05).
- **(e) Knots:** Dobrá 16:48, Soběšovice 17:11, Žermanice 17:14, Podlesí 17:24 out; Žermanice 16:56, Dobrá 17:24, F-M 17:40 back: all on the real minute.
- **(f) Off the pattern:** F-M 15:00 (10 min); Podlesí 12:25 (20), 15:00 (25), 17:24 (39).
- **(g) Need:** 2 (waits F-M 10, Podlesí 41).

### 366 Frýdek-Místek – Lučina – Žermanice – Havířov

- **(a) Core points:** F-M; Dobrá; Lučina; Žermanice (read point, where short trips turn and start); Podlesí. Window 15:30–17:30.
- **(b) Afternoon:** from F-M 12:35 (to Žermanice), 13:20, 14:30, 15:10, **16:10, 16:58**, 18:58; towards F-M at Žermanice
  12:36, 13:47, 14:31 (these three start at Žermanice), **15:41, 16:36** (Podlesí 15:30, 16:25).
- **(c) Step 4:** every 60 :10 / :25 (published): 17:10 and 17:25 empty, FAIL both. No hourly minute fits both 16:10 and 16:58.
  Every 120 one slot (16:58 / 16:25) passes but halves the line (rule 3). **Every 120, F-M 16:10 + 16:58, Podlesí 15:30 + 16:25:**
  2/2 slots filled both ways; exact 3 (F-M) and 5 (back) over the day.
- **(d) Simutrans line 366:** every 120. F-M Offset 69, Also at 117 (real 12:10/14:10/16:10/18:10 and 12:58/14:58/16:58/18:58);
  Podlesí Offset 29, Also at 84 (real 13:30/15:30/17:30 and 12:25/14:25/16:25/18:25), so the bus passes Žermanice at 15:41 and 16:36.
- **(e) Knots:** out all on the minute (Dobrá 16:28 / 17:16, Žermanice 16:46 / 17:34, Podlesí 16:56 / 17:44); back Dobrá 15:59 / 16:54
  exact, F-M 16:15 / 17:10 (real 16:12 / 17:10).
- **(f) Off the pattern:** out 12:35, 13:20, 14:30, 15:10; back the Žermanice starts 13:47 (6 min) and 14:31 (5).
- **(g) Need:** 3, one more (waits F-M 44 / 61, Podlesí 34 / 41): the two slots each way are 48 and 55 min apart and do not chain
  as tightly as the hourly row did. On the owner checks with every 60 (2 buses, fails Step 4).

### 368 Frýdek-Místek – Sedliště – Havířov (direct)

- **(a)** F-M; Sedliště, pošta; Podlesí. **(b)** F-M 6:10, 12:40, **15:30**; Podlesí 7:05, 13:35, **16:35** (the 16:22 from Město).
- **(c) Step 4:** published F-M 0:40 (12:40 / 15:40): 15:40 empty. **F-M 0:30 (12:30 / 15:30):** exact in the window. 12:40 and 15:30
  are 170 min apart, so no interval holds both; the model hour wins.
- **(d)** every 180. F-M Offset 149 (real 12:30, 15:30, 18:30); Podlesí Offset 34, unchanged (real 13:35, 16:35, 19:35).
- **(e)** Sedliště 15:47, Podlesí 16:05; back Sedliště 16:54, F-M 17:10: exact. **(f)** F-M 12:40 (10 min). **(g)** 1 (waits 80, 30).

### 369 Frýdek-Místek – Sedliště – Šenov – Havířov

- **(a) Core points:** F-M; Sedliště; Šenov, náměstí; Havířov, Město, železniční stanice (read point back: the trips start at
  Podlesí, half the trips out end there); Podlesí.
- **(b) Whole day:** F-M :30 hourly 10:30–13:30 and 16:30–18:30, but **14:45, 15:40** in between; back at Město :57 hourly
  (Podlesí :45) 8:57–12:57 and 16:57–18:57, but **14:22, 14:52, 15:52** (Podlesí 14:10, 14:40, 15:40) in between.
- **Model hour:** line_anchor puts it at 14:40 (window 14:10–16:10: 6 departures against 4 at 15:00–17:00). One of the 6 is
  the 14:25 Frýdek-Místek, Frýdek – Kaňovice short, whose stops are all on 369; without it the count is 5 against 4 and the line
  stays at 16:00. So the anchor is set by hand to 16:00, as for 282 (v4 rule).
- **(c) Step 4:**

  | Candidate | F-M | Podlesí (at Město) | Buses |
  |---|---|---|---|
  | every 60 :30 / :45 (published, window 14:10–16:10) | 0 of 2 within 3: FAIL | 0 of 2: FAIL | 3 |
  | every 60 :30 / :45 at 16:00 | 15:30 empty: FAIL | 15:45 empty: FAIL | 3 |
  | every 120, 14:45 + 15:40 / 14:40 + 15:40 (window 14:10–16:10) | ok; 3 exact | ok; 3 exact | 2 |
  | **every 120, 15:40 + 16:30 / 15:40 + 16:45 (at 16:00)** | ok; 9 exact | ok; 7 exact | 3 |

  The 14:40 window option saves a bus but puts 16:30–18:45 5–15 min off; it is on the owner checks.
- **(d) Simutrans line 369:** every 120. F-M Offset 39, Also at 89 (real 13:40/15:40/17:40 and 12:30/14:30/16:30/18:30); Podlesí
  Offset 39, Also at 104 (real 13:40/15:40/17:40 and 12:45/14:45/16:45/18:45), so the bus passes Město at :52 and :57.
- **(e) Knots:** back Šenov 16:03 / 17:08, Sedliště 16:18 / 17:23, F-M 16:35 / 17:40, all exact. Out, the sheet's knot check shows
  2–3 h: it compares with the few trips that run on to Podlesí, while the afternoon trips end at Město (as before).
- **(f) Off the pattern:** out 13:30 and 17:30 (10 min), 14:45 (15); back 14:10 (30), 14:40 and 17:45 (5).
- **(g) Need:** 3 (waits F-M 65 / 50, Podlesí 14 / 19).

## Havířov – Ostrava

### 445 Havířov – Ostrava, Poruba

- **(a)** Podlesí; Havířov, Město; Zábřeh, AVION; Poruba, Opavská. Window 15:30–17:30.
- **(b)** Podlesí 12:57, 14:12, 15:12, **16:47**; Poruba 12:44, 14:14, **15:32, 16:32**, 18:10. Each bus runs one round (42-1003, 42-1009,
  42-1017) and goes on to other lines at Podlesí.
- **(c) Step 4:** every 60 :12 / :32 (published): Podlesí 16:12 and 17:12 empty, FAIL. The window has one departure out, so one
  slot each way: every 80, 90, 96 and 120 at 16:47 / 16:32 all pass with 2 buses. **Every 96** hits the most trips: 16:47 and 16:32
  exact, 15:11 for the real 15:12 and 18:08 for the real 18:10 (most within ±1 over the day, Step 4 rule 3; every 80, 90 and
  120 hit no other afternoon trip within 3 min).
- **(d)** every 96. Podlesí Offset 82 (real 13:35, 15:11, 16:47, 18:23); Poruba Offset 67 (real 13:20, 14:56, 16:32, 18:08).
- **(e)** Město 16:59, AVION 17:22, Poruba 17:41 (real 17:40); back AVION 16:53, Podlesí 17:25 (real 17:27).
- **(f)** Podlesí 12:57, 14:12; Poruba 12:44, 14:14, 15:32 (36 min). **(g)** 2, one fewer (waits Podlesí 56, Poruba 27).

### 448 Havířov – Vratimov – Ostrava, Hrabůvka

- **(a)** Podlesí; Město; Vratimov, náměstí; Hrabůvka, Poliklinika. **(b)** Podlesí 12:05, 13:03, 14:05, 15:05, **16:05, 17:03**, 18:50
  (the :03 run via Kartonážka and Hrabová, průmyslová zóna); Poliklinika 12:50, 14:00, 14:50, **15:55, 16:50**, 18:05.
- **(c) Step 4:** every 60 :05 / :50 (published): back 15:50 empty (real 15:55), FAIL. **Every 120, 16:05 + 17:03 / 15:55 + 16:50:** exact
  both ways (7 and 4 exact over the day), 2 buses. Every 60 :05 / :52 passes too, within 3 min, but has no departure on its real
  minute back (0 exact); it is named on the card.
- **(d)** every 120. Podlesí Offset 2, Also at 64 (real 13:03/15:03/17:03 and 12:05/14:05/16:05/18:05); Poliklinika Offset 54, Also at
  109 (real 13:55/15:55/17:55 and 12:50/14:50/16:50/18:50).
- **(e)** Město exact; Vratimov and Poliklinika 1 min for 16:05, 4 and 7 min for 17:03 (the real 17:03 takes the longer Kartonážka
  path; the line runs the direct one). Back Podlesí and Vratimov within 1.
- **(f)** Podlesí 18:50; Poliklinika 14:00 (5), 18:05 (10). **(g)** 2 (waits Podlesí 37 / 44, Poliklinika 8 / 15).

## Havířov – Orlová (451, 452)

### 451 Havířov – Orlová, Lutyně (every 30)

- **(a)** Podlesí; Město; Lutyně; Elektrárna Dětmarovice. Model hour 16:00 (set on 21 Oct, owner check), window 15:30–17:30.
- **(b)** Podlesí :00 / :30 all day, but in the window 15:30, 16:00, 16:30 and no 17:00; Lutyně 15:46, 16:16, no 16:46, 17:18.
  The missing two are run by **452**: Podlesí 17:00 (51-1202) and Lutyně 16:48 (51-1114), on 452's path via Prostřední Suchá; both
  buses run 451 before and after. So in that hour the every 30 is 451 + 452 together (Step 5, as 503 in 504's slot).
- **(c) Step 4:** 451's own trips: 3 of 4 slots each way, 75 %, FAIL. Every 120 with three slots each way (15:30, 16:00, 16:30 /
  15:46, 16:16, 17:18) passes on 451 alone with 3 buses, but drops a quarter of the trunk. **Every 30, read with 452's trips**
  (`lines: ["451", "452"]`): 4 of 4 both ways; 24 and 16 exact over the day.
- **(d)** unchanged typed values: every 30, Podlesí Offset 29 (real :00 / :30), Lutyně Offset 15 (real :16 / :46). The two legs
  now read 451 + 452 and carry `rt` 41 / 40 (451's own running times, as before; 452's trips would make them 40 / 39). Stops are
  unchanged (451's path).
- **(e)** Lutyně arrivals within 1 min, Podlesí within 3. The knot check at Havířov, Město shows 29 and 31 min for the 17:00 and
  16:46 slots: those stand for 452 trips, which do not pass Město, železniční stanice.
- **(f)** out the shift extras 13:08, 13:20, 13:45, 14:35; back 14:06 (10), 15:01 (15); and 452's own trips 12:45, 13:50, 14:35,
  14:40, 15:35, 18:20 (read here, timed on 452).
- **(g)** 3 (waits Podlesí 4, Lutyně 5). 451 Elektrárna is unchanged.

### 452 Havířov – Prostřední Suchá – Orlová

- **(a)** Podlesí; Lutyně. Window 13:50–15:50 (its anchor).
- **(b)** One bus shuttles (51-1013): Podlesí 12:45, **14:35**; Lutyně **13:50, 15:35**. 451 buses run the rest: Lutyně **14:40**
  (51-1201, between 451 trips), 16:48; Podlesí 17:00, 18:20.
- **(c) Step 4:** every 60 :45 / :48 (published): all four window slots empty. The window has 1 departure from Podlesí and 3 from
  Lutyně, so no balanced pattern passes (Step 7): IRREGULAR. Kept at the shuttle's rate, **every 120, Podlesí 14:35, Lutyně 15:35**
  (Podlesí passes; Lutyně has 1 slot for 3 real, FEWER). The 14:40 is a 451 bus going back to Havířov on 452's path (Step 5b),
  and the 13:50 is the shuttle's earlier run, 105 min before 15:35, which every 120 cannot hold with it.
- **(d)** every 120. Podlesí Offset 94 (real 12:35, 14:35, 16:35, 18:35); Lutyně Offset 34 (real 13:35, 15:35, 17:35).
- **(e)** Lutyně 15:15 (real 15:18), Podlesí 16:14 (real 16:12). **(f)** Podlesí 12:45 (10), 17:00, 18:20; Lutyně 13:50 (15), 14:40, 16:48.
- **(g)** 1, one fewer (waits 22, 17).

## Havířov – Třanovice

### 465 Havířov – Žermanice – Dolní Domaslavice – Třanovice

- **(a)** Podlesí; Žermanice; Třanovice, křižovatka. Window 13:10–15:10 (its anchor).
- **(b)** About every 2 h: Podlesí 11:25, **13:40**, 15:30, 19:24 (the 14:45 ends at Třanovice, U Paverů); Třanovice **13:16, 14:16**,
  16:11, 20:11. The 13:16 is the return of the 11:12 from Město (42-1017 waited at Třanovice); 43-1105 runs 13:40 and 14:16.
- **(c) Step 4:** every 60 :16 / :40 (published): Podlesí 14:40 empty, FAIL. The window holds one Podlesí departure, so one slot
  each way: **every 120, Třanovice 14:16, Podlesí 13:40** passes, 1 bus; with Třanovice 13:16 instead it needs 2.
- **(d)** every 120. Třanovice Offset 75 (real 12:16, 14:16, 16:16, 18:16); Podlesí Offset 39 (real 13:40, 15:40, 17:40).
- **(e)** Žermanice 13:50, Třanovice 14:11; back Žermanice 14:38, Podlesí 14:49 (real 14:47).
- **(f)** Třanovice 13:16, 16:11 (5); Podlesí 15:30 (10), 19:24. **(g)** 1, one fewer (waits Třanovice 5, Podlesí 52).

## Karviná, Orlová – Ostrava

### 532 Karviná – Ostrava, Náměstí Republiky

- **(b)** Karviná 12:23, 12:53, 13:28, 14:28, 15:20, **16:20, 16:51**, 20:36; Náměstí Republiky :39 hourly 13:39–18:39 and 14:09.
- **(c) Step 4:** every 60 :20 / :39 (published): Karviná 17:20 empty. No hourly minute holds 16:20 and 16:51. **Every 120, Karviná
  16:20 + 16:51, Ostrava 15:39 + 16:39:** exact; 3 buses as before. The audit's every 144 for Karviná passes with 15:39 / 16:39
  back as well, but hits 4 trips on the minute over the day against 10.
- **(d)** every 120. Karviná Offset 79, Also at 110 (real 12:20/14:20/16:20/18:20 and 12:51/14:51/16:51/18:51); Ostrava Offset 38,
  Also at 98 (real :39 every hour).
- **(e)** the knot check puts Ostrava at 17:21 / 17:52 with the day's median of 61 min; the afternoon trips take 53–54 min (real
  17:14 / 17:44), as the leg's own running time (54) says. Back Karviná 16:37 / 17:37 (real 16:42 / 17:38). **(f)** Karviná 13:28, 14:28 (8), 15:20; Ostrava 14:09. **(g)** 3 (waits Karviná 11 / 40, Ostrava 25 / 54).

### 552 Orlová – Ostrava, Náměstí Republiky

- **(b)** A midday line ending at 15:35: Lutyně 12:30, **13:30, 14:45**; Ostrava 12:50, **13:30, 14:35**, 15:35. Each bus goes out
  and back once (51-1105, 51-1106, 51-1003).
- **(c) Step 4:** every 60 :30 / :35 (published): 14:30 and 13:35 empty. **Every 240, 13:30 + 14:45 / 13:30 + 14:35:** exact, 2 buses.
  Every 120 with the same slots is as exact but needs 3; every 240 is the longer interval of the two (Step 4 rule 3).
- **(d)** every 240. Lutyně Offset 29, Also at 104 (real 13:30/17:30 and 14:45/18:45); Ostrava Offset 29, Also at 94 (real 13:30/17:30
  and 14:35/18:35).
- **(e)** Ostrava 14:20 / 15:35 (real 14:22 / 15:30), Lutyně 14:19 / 15:24 (real 14:20 / 15:31). **(f)** 12:30, 12:50, 15:35.
- **(g)** 2 (waits Lutyně 23 / 123, Ostrava 15 / 115).

### 553 Orlová (Ostrava – Orlová short trips)

- **(b)** Ostrava → Lutyně shorts 14:52, 15:52, then 17:02, 18:02, 19:02 (the trunk leaves :32 to Karviná). In the window 13:00–15:00
  only 14:52.
- **(c) Step 4:** every 60 :52 (published): 13:52 empty. **Every 120, 14:52:** exact, empty return as before, 1 bus.
- **(d)** every 120, Ostrava Offset 111 (real 12:52, 14:52, 16:52, 18:52); Lutyně → Ostrava untimed.
- **(f)** 17:02, 19:02 (10); 15:52 and 18:02 now fall to the trunk's slots and are off there (20, 30). **(g)** 1, one fewer.
- See "Empty-return lines" below: it serves no stop of its own.

## Orlová – Bohumín (558, 559, 560, 565)

### 558 Orlová – Rychvald – Bohumín, železniční stanice

- **(b)** Lutyně :02 hourly (14:12 in the window); Bohumín žst :04 in the morning, then 13:44, **15:16, 15:50**, 17:16, 18:16.
- **(c) Step 4:** every 60 :02 / :16 (published): Bohumín 14:16 empty. **Every 120, Lutyně 15:02 + 16:02 (the hourly :02), Bohumín
  15:16 + 15:50:** exact, 2 buses.
- **(d)** every 120. Lutyně Offset 1, Also at 61 (real :02 every hour); Bohumín Offset 15, Also at 49 (real 13:16/15:16/17:16 and
  13:50/15:50/17:50). **(e)** Rychvald and both ends exact. **(f)** Lutyně 14:12 (10); Bohumín 12:04, 13:44 (6), 18:16.
- **(g)** 2 (waits Lutyně 2 / 28, Bohumín 28 / 2). 558 Pudlov unchanged.

### 559 Orlová – Dolní Lutyně – Bohumín, autobusová stanice

- **(b)** Lutyně 14:00, 15:15, **16:55**, 19:00; Bohumín 13:05, 14:05, **15:40, 16:50, 17:20**, 18:50 (Kovošrot trips apart).
  Bohumín sends more than Lutyně: the 15:40 and 16:50 buses (51-1008, 51-1106) came out on 557 to Bohumín, žst (unmodelled) and go
  home to Orlová on 559; 51-1109 runs 15:15 out, 560 back, then 16:55 out and 17:20 back.
- **(c) Step 4:** the published hourly row (every 480, seven slots :00 / :50): 16:00, 17:00 and 15:50 empty. Every 120 with one
  slot (16:55 / 17:20) leaves Bohumín 1 slot for 3 real (FEWER). **Every 240, Lutyně 15:15 + 16:55, Bohumín 15:40 + 17:20:** passes
  both ways (Bohumín 2 slots for 3 real), exact, 1 bus.
- **(d)** every 240. Lutyně Offset 134, Also at 234 (real 15:15/19:15 and 12:55/16:55); Bohumín Offset 19, Also at 159 (real
  13:20/17:20 and 15:40/19:40). 559 Kovošrot's 13:00 leaves 5 min after the 12:55 slot (the `why` is updated).
- **(e)** both ends exact. **(f)** Lutyně 14:00, 19:00 (15); Bohumín 13:05, 14:05, 16:50 (30), 18:50. **(g)** 1, one fewer (waits 52 / 92, 2 / 2).

### 560 Orlová – Dolní Lutyně – Bohumín (559's other path)

- **(b)** Lutyně 12:40, **14:40, 15:45**, 17:50; Bohumín 13:31, **14:35, 15:10, 16:00**, 17:50.
- **(c) Step 4:** every 60 :40 / :00 (published): 15:40 and 15:00 empty. **Every 120, Lutyně 14:40 + 15:45, Bohumín 14:35 + 16:00:**
  exact, 2 buses. The 15:10 is left off rather than 14:35 by the plates: 51-1107 runs 14:35 back and 15:45 out (the line's own
  rotation), 51-1111 runs the 15:10 between 558 and 553.
- **(d)** every 120. Lutyně Offset 44, Also at 99 (real 13:45/15:45/17:45 and 12:40/14:40/16:40/18:40); Bohumín Offset 59, Also at 94
  (real 12:00/14:00/16:00/18:00 and 12:35/14:35/16:35/18:35). **(e)** exact. **(f)** Bohumín 13:31, 15:10 (35), 17:50 (10); Lutyně 17:50 (5).
- **(g)** 2 (waits Lutyně 16 / 46, Bohumín 26 / 56).

### 565 Dolní Lutyně, Věřňovice – Kopytov – Bohumín

- **(b)** Věřňovice 10:00, 13:00, 15:15, 16:45; Bohumín 11:50, 14:35, 16:10, 18:30. From 14:35 one bus (51-1001) runs it about
  every 90 min: Bohumín 14:35 (coming from Pudlov), Věřňovice 15:15, Bohumín 16:10, Věřňovice 16:45. The 13:00 from Věřňovice
  runs the direct path, not via Kopytov, with a 564 bus that goes on as 559 (51-1008).
- **Model hour:** line_anchor puts 565 at 13:30, because the Kopytov short trips (13:10, 13:25, 14:05; 565 Kopytov) make 13:00–15:00
  the busiest; without them 13:00–15:00 has 2 departures against 3 at 15:00–17:00. In that window the only Věřňovice departure is
  the direct 13:00, which the Simutrans line (via Kopytov) would run 14 min slower. So 565 gets its own window 15:30–17:30, as 285
  Štítina on the Opavsko sheet; 565 Kopytov keeps 13:00–15:00, where its trips run.
- **(c) Step 4:** every 90, 15:15 / 14:35 (published): at 13:00–15:00 the 13:45 and 13:05 slots are empty; at 15:30–17:30 its 16:05
  slot is 5 min before the real 16:10. Every 180, 13:00 / 14:35 passes at 13:00–15:00 (1 bus) but leaves 15:15–16:45 45 min off; it
  is on the owner checks. **Every 90, Věřňovice 15:15 / 16:45, Bohumín 16:10:** passes at 15:30–17:30, exact.
- **(d)** every 90. Věřňovice Offset 44, unchanged (real 12:15, 13:45, 15:15, 16:45, 18:15); Bohumín Offset 9, was 4 (real 13:10,
  14:40, 16:10, 17:40; was 13:05, 14:35, 16:05).
- **(e)** Kopytov 17:05, Bohumín 17:20; back Kopytov 16:23, Věřňovice 16:44: all exact. **(f)** 13:00 (45), 14:35 (5), 18:30, 11:50.
- **(g)** 1 (waits Věřňovice 1, Bohumín 20; the real bus turns at Věřňovice in 1 min).

## Karviná – Havířov (582, 583)

### 582 Karviná – Stonava – Albrechtice – Horní Suchá

- **(b)** Back towards Karviná the afternoon has only 15:30 (Horní Suchá, škola) and 16:28 (Horní Suchá, dvůr), at Albrechtice
  **15:39** and **16:34**; the row is timed at Albrechtice (knot).
- **(c) Step 4:** the published seven slots at :39 left 16:39 empty (16:34 is 5 min earlier). **The 16:00 slot becomes 16:34**,
  exact; the other six stay. Out of Karviná (:40) passed and is unchanged.
- **(d)** every 480. Horní Suchá, dvůr Offset 32, Also at 92, 152, 212, 332, 392, **447** (was 452): real 17:33, 18:33, 19:33,
  12:33, 14:33, 15:33, **16:28** (was 16:33), passing Albrechtice 6 min later.
- **(e)** Karviná 16:12 / 17:07 exact. **(g)** 2, unchanged.

### 583 Karviná – Stonava – Havířov, Město, nemocnice

- **(b)** Karviná :21 hourly to nemocnice until 16:21, then **:30** to Podlesí (17:30, 18:30, 19:30); back from Město :22 (Podlesí :20
  in the evening), passing nemocnice at **:31** from 13:31 to 20:31. The window 15:30–17:30 holds one Karviná departure (16:21):
  15:21 is before it and 17:30 is its end.
- **(c) Step 4:**

  | Candidate | Karviná | nemocnice | Buses |
  |---|---|---|---|
  | every 60 :21 / :31 (published) | 17:21 empty (real 17:30, 9 min): FAIL | ok, 8 exact | 2 |
  | every 120 :21 / :31 (the audit's) | passes, but half the line | passes | 1 |
  | every 240, 14:21 15:21 16:21 17:30 / :31 | passes; 7 exact; 13:30, 18:21, 19:21 slots 9 min off | ok | 2 |
  | **every 480, eight slots each way** | passes; 11 exact (12:21–19:30 all) | ok, 8 exact | 2 |

  At the line's rate (hourly) the only simpler row that passes is the every 240, and it passes only through the window's edges
  (rule 4), so the exact long row (as 290). The two-value every 60 is on the owner checks.
- **(d)** every 480. Karviná Offset 29, Also at 89, 149, 200, 260, 320, 380, 440 (real 17:30, 18:30, 19:30, 12:21, 13:21, 14:21,
  15:21, 16:21); nemocnice Offset 30, Also at 90, 150, 210, 270, 330, 390, 450 (real 17:31, 18:31, 19:31, 12:31, 13:31, 14:31, 15:31,
  16:31; the same as every 60 at :31).
- **(e)** Horní Suchá 16:56, nemocnice 17:04; back Horní Suchá 15:39 / 16:39, Karviná 16:09 / 17:09: exact.
- **(f)** the morning :38 trips to Podlesí (8:38–11:38), 12:26 (5). **(g)** 2 (waits Karviná 12–21, nemocnice 18–27).

## Left approximate (no passing pattern)

- **452 towards Havířov (FEWER):** the model hour has 1 departure from Podlesí and 3 from Lutyně, so no balanced row passes; the
  14:40 is a 451 bus (Step 5b) and 13:50 the shuttle's earlier run. The audit's per-direction candidate (every 480, three slots)
  has no partner row from Podlesí.
- **543 back from Dětmarovice (17:04 slot):** Dětmarovice has no departure after 15:04 (real 5:04, 7:04, 13:04, 15:04), while Ostrava
  sends 16:12. One bus every 120 is the line's rate (the 14:12 bus comes back as the 15:04); any row has an empty slot in
  15:30–17:30 or drops the 16:12. Unchanged.
- **543B (17:12 slot):** Ostrava 13:12, 15:12 out; 17:12 has no trip (17:32 is 20 min later). Unchanged; see below.

## Empty-return lines

The method's v4 text says 543B and 553 Orlová "kept their reasons". Checked against the coverage map (`schedule.json` →
`_coverage.by`), neither has a stop of its own:

- **553 Orlová** (Ostrava, hlavní nádraží → Lutyně, 20 stops): every stop is also on 553 and 553 Autopal (Ostrava hl. n., Muglinovská,
  sad B. Němcové, Muglinov, Hrušov, Heřmanice, Rychvald zámek / Skříšovský / Městský úřad / u závor / Dělnický dům, Orlová Poruba
  u rybníku / čisticí stanice, Lutyně Zátiší to the bus station). Its reason on the README is why its return is empty (the real
  buses go on as other lines), not a stop. It adds only frequency: **for removal, 1 bus** (owner checks).
- **543B** (Ostrava → Dětmarovice, 22 stops): every stop is also on 543 (Ostrava to Rychvald, Dolní Lutyně, Dětmarovice, obecní úřad
  and železniční stanice). It adds only frequency (Ostrava hourly instead of every 2 h): **for removal, 1 bus** (owner checks).
- **558 Pudlov** keeps its reason: Bohumín, Pudlov, střed has no other line.

Neither was removed (the owner decides). Removing both would make the sheet 61 buses.

## Shared terminals (model departures 15:30–17:30)

At Podlesí several lines leave on the same minute, each a real departure on its own route: 15:30 (366, 451), 15:40 (367, 369, 465
repeat, 533), 16:45 (365, 369), 16:35 (368; 452's 16:35 is a repeat, outside its own window), 17:30 (366 repeat, 451). The old rows
had as many (15:00 365 / 451, 16:45 369 / 452). At Lutyně 560 15:45 and 451 15:46 leave a minute apart, as in reality (15:45 and
15:46). The every-30 of 451 now includes 452's 17:00 / 16:48 slots, so 452's own row (14:35 / 15:35) no longer doubles them.

## For the roster and the README (not changed here)

- **451's evidence now includes 452 trips** (`lines`): the roster may see 51-1013 (452 15:35), 51-1202 (452 17:00) and 51-1114
  (452 16:48) as 451 candidates. The latter two are 451 buses anyway; `keep_roster` should hold the published buses.
- **Needs:** 366 +1; 445, 452, 465, 553 Orlová, 559 −1 each: 67 → 63. The roster and the in-game change list follow from 04/06.
- **README "Decisions" now stale:** 451 and 452 (452's 17:00 / 16:48 in 451's every 30; 452 every 120); 559 "every 480 with seven
  slots" (now every 240; 582's seven-slot rule stands); the approximate list (365, 366, 368, 369, 445, 448, 452, 465, 532, 559, 560,
  565 are no longer approximate; 452, 543, 543B are); 543B and 553 Orlová for removal; 369's model hour 16:00 and 565's own window.
