# Bus schedule method, applied to the failing legs of the Bruntálsko sheet (25 Oct 2026)

The owner, after the hand check of the four Hlučínsko lines (`../odis-regional-opavsko/method-check-2026-10-25.md`), asked for
every sheet to be checked at that level: "that's the point of you doing it, so you'll not produce incorrect results". The Step 4
audit of this sheet (`../audit/audit-regional-2026-10-25.md`) listed 36 failing legs on 23 lines (35 EMPTY, 1 FEWER; 32 FIXABLE,
4 IRREGULAR). Each line was read again over the whole day with its plates, both directions together, against
`../bus-schedule-method.md` (v4), and set by hand in `authoring/brn_spec.py`. Legs the audit did not list were left alone.

- **Data:** the sheet's JDF trips for Tue 20 Oct 2026 (`data/derived/trips.json`), the whole-day reading with the 20 Oct
  live-map plates (`data/derived/reading/<L>.txt`), and the builder's own trip ownership (`data/derived/schedule.json`).
- **Step 4 test,** per direction in the line's model window (anchor −30 to +90): window slots = real departures ±1, and at least
  80 % of the slots have a real departure within 3 min. Then most departures exact over the day (5–23), then within 1, then fewer
  slots, then the longer interval. Verified by rerunning `05_schedule.py` and `../audit/step4_regional.py`.
- **Tie rule used here:** among patterns that pass Step 4 both ways at the same rate, the method's order above, but **never more
  buses than the line had** unless nothing passes at that count (the 290 case). A more exact pattern that costs buses is on the
  owner checks with its cost (819, 861, 863, 877). Going below the published count was not a goal either (862 keeps 2). **One
  deliberate exception:** the 801 trunk, where nothing passes at 2 buses and the passing patterns (4 buses) fold the
  industrial-zone shift trips into the trunk; it stays every 30 on the real minutes, approximate by rule 4, with the passing
  pattern on the owner checks (see "Left approximate").
  "Exact" counts real departures over the whole day; where two candidates tie, the plates (which bus really runs which trip) and
  the waits decide which departures fall off the pattern.
- **Typed values** are (real − 61) mod every: every terminus is a loop. The real time of each value is (value + 61) mod every,
  placed in the afternoon.

## What the reading showed (common to several lines)

- **Most failures were narrow windows on sparse lines.** Where a direction has one real departure (or none) in the two-hour
  window, an interval of 90–180 puts a slot there with no bus. The fix is an interval whose slots land only on the real trips:
  every 240 or 480 on the line's real afternoon rounds (833, 902 Zlaté Hory, 872, 878, 907, 922, 805, 806, 851). The four
  IRREGULAR legs (901, 902 Zlaté Hory, 816, 907) were all of this kind; none is left irregular.
- **Variant trips counted twice.** The builder gives a trip to every leg it passes, so the school trips Úblo – Neplachovice (818),
  the KARLA trips (877) and the Uničov trips (922) were also real departures of the main legs, and a main slot near them would run
  a second bus beside the variant's own Simutrans line. They are now left out of the main legs (`notvia`); each has its own
  line, unchanged. 872's 14:10 back ends at Bruntál, station, so the way back is counted there (`core_to`).
- **Model hour by hand** (the 282 precedent): 901 and 877 were anchored early by shorts whose stops are on the line anyway
  (Město Albrechtice – Holčovice; Břidličná, Kovohutě – Rýmařov) and, for 877, the KARLA variant. Without those trips their
  busiest two hours are no busier than 15:00–17:00, so the default 16:00 applies.
- **0-min turns.** Purkartice (822), Čaková (814) and Anenská Huť (880) are loops where the real bus leaves as it arrives. The
  builder needs at least 1 min, else a second bus: 822's run out is 29 min (as most of its day's trips), and 814 and 880 leave
  1 min early (15:24, 15:59).
- **Outstation patterns** (more buses out than back, the extra ones going home or on to other lines): 833 (Krnov → Jindřichov),
  818 (Úblo is where 83-2006 sleeps) and 877 (Rýmařov → Bruntál, back on 920 and 877 KARLA). These run at their return rate,
  and the extra departures are off the pattern and named on the cards.

## Summary

| Line | Published (v2) | Step 4 | Now | Buses |
|---|---|---|---|---|
| 822 | every 90, Krnov 14:24 / Purkartice 14:55 | Krnov 15:54 slot empty (real 15:45) | every 80, Krnov 14:25 / Purkartice 14:55, exact | 1 → 1 |
| 833 | every 180, Krnov 14:25 / Jindřichov 16:46 | 17:25 and 16:46 slots empty | every 240, Krnov 15:45 / Jindřichov 17:20 | 1 → 1 |
| 901 | every 120, Krnov 15:15 / Zlaté Hory :44, window 13:20–15:20 | 15:15 slot empty; no trip back in the window | same values, model hour 16:00 by hand | 2 → 2 |
| 902 Zlaté Hory | every 240, Jindřichov 13:21 / Zlaté Hory 14:36 | 17:21 slot empty | every 480 on that round | 1 → 1 |
| 811 | every 120, Krnov 13:00 / Horní Benešov 14:16 | 15:00 and 14:16 slots empty | every 90, Krnov 15:05 / Horní Benešov 14:20, 15:50 | 1 → 1 |
| 814 | every 180, Krnov 15:19 / Čaková 15:50 | Čaková 15:50 empty (real 15:55) | every 180, Krnov 15:24 / Čaková 15:55 | 1 → 1 |
| 816 | every 180, Krnov žst 13:50 / Krasov 15:45 | Krnov 16:50 slot empty | every 180, Krnov 15:10 / Krasov 15:45 | 1 → 1 |
| 818 | every 180, Krnov 15:10 / Úblo 14:37 | Úblo 14:37 empty (real 15:03) | every 240, Krnov 17:40 / Úblo 15:03 | 1 → 1 |
| 818 Skrochovice | every 90, Úblo 14:30 / most 14:50 | Úblo 16:00 empty; most 1 slot for 3 (FEWER) | every 240, two rounds each way, exact | 1 → 1 |
| 819 | every 60, Krnov :54 / Bruntál :42 | Krnov 14:54, 15:54 empty | every 160, two slots each way, exact | 2 → 2 |
| 861 | every 60, Bruntál :40 / zámeček :54 | zámeček 15:54 empty (real 15:44) | every 160, two slots each way, exact | 3 → 3 |
| 862 | every 60, :10 / :10 | 16:10, 17:10 empty both ways | every 240, two rounds each way, exact | 2 → 2 |
| 863 | every 90, Bruntál :00 / Ludvíkov :15 / :45 | 13:30, 13:15, 14:45 empty | every 120, Bruntál 14:20 / Ludvíkov 14:15 | 2 → 2 |
| 872 | every 90, Bruntál 13:50 / Milotice 14:10 | 15:20, 14:10, 15:40 empty | every 480, both rounds, exact | 1 → 1 |
| 907 | every 120, Vrbno 15:15 / Zlaté Hory 16:25 | 17:15 and 16:25 empty | every 480, three rounds each way, exact | 1 → 1 |
| 877 | every 60, Rýmařov :34 / Bruntál :24 | 14:34, 15:34, 15:24 empty | every 120, Rýmařov 15:40 / Bruntál 16:20, model hour 16:00 | 2 → 2 |
| 878 | every 90, Rýmařov 15:30 / Karlov 16:10 | Rýmařov 17:00 empty | every 480, both rounds, exact | 1 → 1 |
| 880 | every 90, Rýmařov 14:25 / Anenská Huť 14:45 | Rýmařov 15:55 empty (real 16:00) | every 180, three rounds each way | 1 → 1 |
| 922 | every 90, station 14:15 / Ruda 14:50 | 14:15 and 14:50 empty | every 480, three rounds each way, exact | 1 → 1 |
| 801 | every 30, Nemocnice :06 / Petrův důl :07 | Petrův důl 14:07, 14:37 empty | every 30 at :05 / :05; way back approximate | 2 → 2 |
| 802 | every 60, bus stand :55 / Ježník :15 | Ježník 15:15 empty (real 15:19) | every 160, three rounds each way, exact | 1 → 1 |
| 805 | every 90, Hlubčická 14:40 / Chomýž 15:35 | Chomýž 17:05 empty | every 480, three each way, exact | 1 → 1 |
| 806 | every 90, bus stand 14:45 / Cvilín 15:05 | 16:15 and 16:35 empty | every 480, both rounds, exact | 1 → 1 |
| 851 | every 180, station 13:26 / KARLA 14:12 | 16:26 and 17:12 empty | every 480, both pairs, exact | 1 → 1 |
| **Total** | | **36 legs failing** | **35 pass, 1 approximate** | **32 → 32** |

The sheet still needs 63 buses. The re-audit: 100 timed legs, 99 ok, 1 EMPTY (801 Petrův důl → Nemocnice, below); coverage
0 uncovered. The 21 `auto` legs that remain are on lines the audit passed (817, 831, 833 Osoblaha, 873, 874, 879, 885, 910,
911, 912, 913) and were not changed.

## Krnovsko

### 822 Krnov – Hošťálkovy, Staré Purkartice
- **(a)** Core points: Krnov, autobusová stanice; Staré Purkartice, točna (loop). Model hours 14:20–16:20.
- **(b)** Krnov 11:45, **14:25, 15:45**, 17:25, 19:15; Purkartice 12:45, **14:55, 16:15**, 17:55, 19:55. One bus, 83-2009, all
  afternoon; it leaves the Purkartice loop the minute it arrives.
- **(c)** Published every 90 (Krnov 14:24 / 15:54): Krnov 1 of 2 FAIL. **Every 80** Krnov 14:25 (2 of 2, 4 exact over the day:
  7:45, 11:45, 14:25, 15:45) and Purkartice 14:55 (2 of 2, 2 exact). Every 90 fits 17:25 / 17:55 better but fails the window.
- **(d)** Simutrans line 822: every 80. Krnov Offset 4 (real 14:25, 15:45); Purkartice Offset 34 (real 14:55, 16:15). The run
  out is set to 29 min (`rt`): the path-0 trips take 29 except the two in the window (30); with 30 the 0-min turn needs a second bus.
- **(e)** Knots: none between; the model reaches Purkartice 14:54 / 16:14 and Krnov 15:34 / 16:54 (real 15:26 / 16:54; the
  median includes the Chomýž path).
- **(f)** Off the pattern 12–20 h: Krnov 17:25 (20), 19:15 (30); Purkartice 12:45 (30), 17:55 (20), 19:55 (20).
- **(g)** Need 1 (waits Krnov 15, Purkartice 1).

### 833 Krnov – Město Albrechtice – Jindřichov (– Osoblaha)
- **(a)** Core points: Krnov AS; Jindřichov, železniční stanice; Osoblaha AS. Model hours 15:30–17:30.
- **(b)** Krnov → Jindřichov 12:35, 14:25, **15:45**, 18:05 (Vysoká), 21:10; Jindřichov → Krnov **17:20** (the Osoblaha 16:44),
  19:20 (from Vysoká), 21:01. Plates: 82-2005 out 12:35 and on to Osoblaha, 831 and 902; 82-1005 out 14:25 → 833 Osoblaha 15:39 →
  Osoblaha 16:44 → Krnov 17:56; 83-1205 out 15:45, its day ends at Jindřichov 16:25. More buses go out than come back on 833.
- **(c)** Published every 180 (Krnov 14:25 / 17:25, Jindřichov 16:46): 0 of 1 both ways FAIL. Every 120 (15:45 / 17:20) passes
  but needs 2 buses and puts 13:45 / 17:45 and 15:20 slots on no trip. **Every 240** Krnov 15:45 (1 of 1), Jindřichov 17:20 (1 of
  1, also 9:20 exact).
- **(d)** Simutrans line 833: every 240. Krnov Offset 164 (real 15:45), stops via Město Albrechtice, rozcestí Dakon; Jindřichov
  Offset 19 (real 17:20). 833 Osoblaha (every 180, Jindřichov 15:39 / Osoblaha 16:44) passed and is unchanged.
- **(e)** Model reaches Jindřichov 16:24 (real 16:25) and Krnov 17:56 (real 17:56).
- **(f)** Off: Krnov 12:35, 14:25 (it is the 833 Osoblaha bus), 18:05; Jindřichov 19:20, 21:01.
- **(g)** Need 1 (waits Krnov 109, Jindřichov 52).

### 901 Krnov – Heřmanovice – Zlaté Hory
- **(a)** Core points: Krnov AS; Město Albrechtice AS; Zlaté Hory AS. Model hours were 13:20–15:20, now 15:30–17:30.
- **(b)** Krnov 13:45, 15:05, **17:15** (also 9:15); Zlaté Hory 12:19, **15:44**, 17:44, 19:44. Two buses (82-1002, 82-2004).
- **(c)** The anchor 13:50 came from the Město Albrechtice – Holčovice shorts (13:24, 13:59); their stops (Hynčice, Hejnov,
  Holčovice) are all on the main path. Without them 13:20–15:20 has 2 departures, as 15:00–17:00: default 16:00, set by hand
  (`anchor`). The back direction had no trip at all in 13:20–15:20, so no slot could pass there. At 16:00 the published values
  pass: Krnov 1 of 1 (exact 9:15, 17:15), Zlaté Hory 1 of 1 (exact 15:44, 17:44, 19:44).
- **(d)** Simutrans line 901: every 120, Krnov Offset 14 (real 17:15), Zlaté Hory Offset 43 (real 15:44). **No in-game change.**
- **(f)** Off: Krnov 13:45 (30), 15:05 (10); Zlaté Hory 12:19 (35). **(g)** Need 2.

### 902 Zlaté Hory (Jindřichov – Zlaté Hory)
- **(b)** One round a day in the afternoon: Jindřichov 13:21 → Zlaté Hory 13:56, back 14:36 → 15:08 (82-2002); also 4:41, 6:17.
- **(c)** Published every 240: the 17:21 slot has no trip (IRREGULAR in the audit: the search cannot place zero slots in the
  window). **Every 480** on the round leaves no slot in 15:30–17:30, and there is no trip there: passes both ways.
- **(d)** 902 Zlaté Hory: every 480, Jindřichov Offset 260 (real 13:21), Zlaté Hory Offset 335 (real 14:36). **(g)** Need 1.

## Bruntálsko

### 811 Krnov – Horní Benešov
- **(a)** Core points: Krnov AS; Horní Benešov AS. Model hours 14:10–16:10.
- **(b)** Krnov 13:00, **15:05**, 17:40, 19:45; Horní Benešov 12:45, **14:20, 15:50**, 18:40. Each Krnov departure comes back on the
  same bus about 75 min later (82-2006 13:00 → 14:17, 83-1007 15:05 → 15:50, 82-2003 17:40 → 18:37).
- **(c)** Published every 120 (Krnov 15:00, Horní Benešov 14:16): 0 of 1 both ways FAIL. **Every 90**: Krnov 15:05 (1 of 1),
  Horní Benešov 14:20, 15:50 (2 of 2, 3 exact with 6:50). Every 120 at 15:05 / 15:50 also passes, with 1 + 1 exact.
- **(d)** 811: every 90, Krnov Offset 34 (real 15:05); Horní Benešov Offset 79 (real 14:20, 15:50), back via Dubnice as before.
- **(e)** Model reaches Horní Benešov 15:45 (real 15:45) and Krnov 15:00 / 16:30 (real 15:00 / 16:30).
- **(f)** Off: Krnov 13:00 (35), 17:40 (25), 19:45 (10); Horní Benešov 12:45 (5), 18:40 (10). 811 Sosnová unchanged.
- **(g)** Need 1 (waits Krnov 4, Horní Benešov 5).

### 814 Krnov – Zátor – Čaková
- **(b)** Rounds Krnov 13:40 → Čaková 14:10 / 14:15 → 14:45 (82-2003, then 814 Zátor 15:00); **15:25** → 15:55 / **15:55** → 16:25
  (83-2015); 18:20 / 18:50 (84-1005). Every Krnov → Čaková trip takes 30 min, and the bus leaves Čaková as it arrives.
- **(c)** Published every 180 (Krnov 15:19, Čaková 15:50): Čaková 0 of 1 FAIL. **Every 180** on the 15:25 / 15:55 round: no Krnov
  slot in the window, Čaková 1 of 1 exact.
- **(d)** 814: every 180, Krnov Offset 143 (real 15:24, 1 min before the real 15:25, for the 0-min turn), Čaková Offset 174 (real
  15:55).
- **(f)** Off: the 13:40 / 14:15 round; 18:20 (4), 18:50 (5). 814 Zátor unchanged. **(g)** Need 1.

### 816 Krnov – Krasov
- **(b)** Rounds from Krnov, station: 11:55 / 12:30, 13:50 / (815 14:30), **15:10 / 15:45** (83-1008), 17:45 / 19:00. In the window
  only Krasov 15:45.
- **(c)** Published every 180 at Krnov 13:50 puts 16:50 in the window with no trip (IRREGULAR in the audit). **Every 180** on the
  15:10 round: no Krnov slot in the window, Krasov 1 of 1 exact.
- **(d)** 816: every 180, Krnov žst Offset 129 (real 15:10), Krasov Offset 164 (real 15:45, unchanged).
- **(f)** Off: Krnov 11:55, 13:50 (exact before), 17:45; Krasov 12:30, 19:00. **(g)** Need 1 (waits Krnov 115, Krasov 3).

### 818 Krnov – Brumovice, Úblo (and its two Úblo lines)
- **(a)** Core points: Krnov AS; Brumovice, Úblo, točna; Skrochovice, most. Model hours 14:10–16:10.
- **(b)** Krnov → Úblo 11:05, **15:10**, 17:40, 23:00; Úblo → Krnov 6:44, **15:03**, 17:40, 19:40. Úblo shuttle to Skrochovice
  14:30, 15:40 (back 14:50, 16:00), 19:00 / 19:20. Plates: 83-2006 sleeps at Úblo (4:25 out, 23:00 back) and in the afternoon runs
  the Neplachovice school trips, the 14:30 shuttle, Úblo 15:03 → Krnov, then Krnov 17:40 → Úblo; 82-2006 runs Krnov 15:10 → Úblo,
  the 15:40 shuttle and Úblo 17:40 → Krnov.
- **(c)** 818: published every 180 (Úblo 14:37) 0 of 1 FAIL. Both window trips exact (Krnov 15:10, Úblo 15:03) need 2 buses at any
  interval, as the bus arriving at 15:38 cannot leave at 15:03. At one bus, every 240 on 83-2006's two trips (Úblo 15:03,
  Krnov 17:40) and every 240 on 82-2006's (Krnov 15:10, Úblo 17:40) both pass (1 + 1 exact). 83-2006's is kept: the way back to
  Krnov is the one exact in the window (the outstation direction), and its 19:03 slot lands nearer the real 19:40.
  818 Skrochovice: the Neplachovice school trips pass Skrochovice, most (12:45 out, 14:16 back), so the shuttle legs counted
  them (the FEWER: 14:16, 14:50, 16:00 for one slot). Without them: **every 240** Úblo 14:30, 15:40 (2 of 2, 3 exact with 11:40)
  and most 14:50, 16:00 (2 of 2, 3 exact with 12:00); every 120 with the same slots ties on exact hits and runs twice as often.
- **(d)** 818: every 240, Krnov Offset 39 (real 17:40), Úblo Offset 122 (real 15:03). 818 Skrochovice: every 240, Úblo Offset 89,
  Also at 159 (real 14:30, 15:40), most Offset 109, Also at 179 (real 14:50, 16:00), both `notvia` Neplachovice. 818 Neplachovice
  unchanged.
- **(e)** Shuttle: the model reaches most 14:46 / 15:56 and Úblo 15:03 / 16:13, all as real.
- **(f)** Off: Krnov 15:10 (its bus works the shuttle), 11:05; Úblo 17:40, 19:40; shuttle 19:00 / 19:20.
- **(g)** Need 1 + 1 (+ 1 Neplachovice), as before.

### 819 Krnov – Bruntál
- **(a)** Core points: Krnov AS; Bruntál AS. Model hours 14:20–16:20.
- **(b)** Krnov 12:00, 12:40, **14:25, 14:35, 16:00**, 17:15, 20:15, 20:50; Bruntál 12:00, 13:20, **14:20, 14:40, 15:40**, 16:50, 18:40.
  Four buses touch the line in the window and work 811, 862, 814 and 909 too (83-2004 does one round, 14:25 → 15:40).
- **(c)** Published every 60 (Krnov :54, Bruntál :42): Krnov 0 of 2 FAIL, 0 exact all day. Every 60 at any minute fails (14:25 /
  14:35 / 16:00). Passing, at the same rate both ways:

  | Candidate | Krnov (window, exact day) | Bruntál | Need |
  |---|---|---|---|
  | **every 160, Krnov 14:35 16:00 / Bruntál 14:20 15:40** | 2 of 2, 4 exact | 2 of 2, 4 exact | **2** |
  | every 160, Krnov 14:25 16:00 / same | 2 of 2, 3 | 2 of 2, 4 | 2 |
  | every 240, two slots | 2 of 2, 3 | 2 of 2, 3 | 2 |
  | every 80, Krnov 14:37 / Bruntál 14:20 | 2 of 2, 0 (within 3) | 2 of 2, 4 | 2 |
  | every 160, three slots each way | 3 of 3, 5 | 3 of 3, 6 | 4 |
  | every 120, three slots each way | 3 of 3, 4 | 3 of 3, 5 | 5 |
- **(d)** 819: every 160. Krnov Offset 14, Also at 99 (real 14:35, 16:00; also 17:15, 10:40 exact); Bruntál Offset 79, Also at
  159 (real 15:40, 14:20; also 5:00, 22:20 exact).
- **(e)** Model reaches Bruntál 15:18 / 16:43 (real 15:22 / 16:43) and Krnov 15:04 / 16:24 (real 15:02 / 16:27).
- **(f)** Off 12–20 h: Krnov 12:00, 12:40, 14:25; Bruntál 12:00, 13:20, 14:40, 16:50, 18:40.
- **(g)** Need 2 (waits Krnov 48, 53; Bruntál 15, 20). Owner check: three slots each way, four buses.

### 861 Bruntál – Vrbno – Karlova Studánka – Vrbno, zámeček
- **(a)** Core points: Bruntál, železniční stanice; Vrbno, zámeček. Model hours 15:30–17:30.
- **(b)** Bruntál 12:30, 14:30 (from KARLA), **15:40, 16:40**, 17:45, 19:40 (also 9:40, 10:40); zámeček 12:09, 14:14, 14:49,
  **15:44, 16:54**, 19:09, 20:09, 21:09, 22:14. The zámeček departures are 70 min apart, so every 60 cannot pass there.
- **(c)** Published every 60 (zámeček :54): 1 of 2 FAIL. Passing, all exact in the window:

  | Candidate | Bruntál exact day | zámeček exact day | Need |
  |---|---|---|---|
  | **every 160, Bruntál 15:40 16:40 / zámeček 15:44 16:54** | 2 | 4 (14:14, 22:14 too) | **3** |
  | every 240, same slots | 3 | 2 | 3 |
  | every 120, same slots (Bruntál hourly :40) | 5 | 2 | 4 |
- **(d)** 861: every 160. Bruntál Offset 79, Also at 139 (real 15:40, 16:40); zámeček Offset 83, Also at 153 (real 15:44, 16:54).
- **(e)** Model reaches zámeček 16:51 / 17:51 and Bruntál 16:51 / 18:01, all as real.
- **(f)** Off 12–20 h: Bruntál 12:30, 14:30, 17:45, 19:40; zámeček 12:09, 14:49, 19:09.
- **(g)** Need 3 (as before). Owner check: every 120, a fourth bus; the Bruntál row is then hourly at :40 and can be typed as
  every 60, Offset 39, as now.

### 862 Bruntál – Malá Morávka – Karlova Studánka, dolní parkoviště
- **(b)** Bruntál 12:05, 15:15, **16:05**, 18:20, 19:10; Karlova Studánka 12:40, 15:10, **16:05, 17:15**, 19:15. Rounds: 83-2011
  15:15 → 16:05 back, 84-1006 16:05 → 17:15 back, 84-2007 18:20 → 19:15.
- **(c)** Published every 60 at :10: 0 of 2 both ways FAIL. **Every 240** Bruntál 15:15, 16:05 (1 of 1 in the window, 3 exact with
  12:05) and Karlova Studánka 16:05, 17:15 (2 of 2, 2 exact): 2 buses. Every 120 (Bruntál 16:05, Karlova Studánka 17:15) passes
  with 1 bus and 2 + 2 exact, leaving the 15:15 round off; every 90 at 16:05 / 16:05 passes with 2 buses, 1 + 3 exact.
- **(d)** 862: every 240. Bruntál Offset 134, Also at 184 (real 15:15, 16:05); Karlova Studánka Offset 14, Also at 184 (real 17:15,
  16:05).
- **(e)** Model reaches Bruntál 16:45 / 17:55 (real 16:45 / 17:55).
- **(f)** Off: Bruntál 18:20, 19:10; Karlova Studánka 12:40, 15:10, 19:15. **(g)** Need 2 (as before).

### 863 Bruntál – Široká Niva – Vrbno, rozcestí Ludvíkov
- **(a)** Core points: Bruntál AS; rozcestí Ludvíkov; Karlova Studánka, Hvězda. Model hours 13:10–15:10.
- **(b)** Bruntál 12:45 (Hvězda), **14:20, 15:00**, 16:25, 18:25; Ludvíkov 12:35, **14:15, 14:40** (the Hvězda 14:25), 16:15, 18:15,
  20:30, 22:15. Each bus does one round in 2–3 h (84-1009 14:20 → Ludvíkov 15:10, back 16:15; 83-1009 Ludvíkov 14:15 → Bruntál
  15:08 → 16:25; 83-2013 15:00 out).
- **(c)** Published every 90: Bruntál 1 of 2, Ludvíkov 0 of 2 FAIL. Passing:

  | Candidate | Bruntál exact | Ludvíkov exact | Need |
  |---|---|---|---|
  | **every 120, Bruntál 14:20 / Ludvíkov 14:15** | 2 (22:20) | 4 (16:15, 18:15, 22:15) | **2** |
  | every 120, Bruntál 15:00 / Ludvíkov 14:15 | 2 (7:00) | 4 | 2 |
  | every 120, both rounds each way | 4 | 5 | 4 |
  | every 240 / 160 / 480, both rounds | 4 | 3–4 | 4 |

  The two one-slot options tie; 14:20 is 84-1009's own round (out 14:20, back 16:15).
- **(d)** 863: every 120, Bruntál Offset 79 (real 14:20), Ludvíkov Offset 74 (real 14:15, and 16:15 for the bus's return).
- **(e)** Model reaches Ludvíkov 15:10 and Bruntál 15:08, as real.
- **(f)** Off: Bruntál 12:45, 15:00, 16:25, 18:25; Ludvíkov 12:35, 14:40. **(g)** Need 2. Owner check: both rounds, 4 buses.

### 872 Bruntál – Milotice nad Opavou
- **(b)** Two afternoon rounds, one bus each: Bruntál 13:50 → 14:09 / Milotice 14:10 → Bruntál, station 14:24 (84-1012); 15:15 →
  15:34 / 15:35 → 15:54 (83-1006). The 14:10 ends at Bruntál, station, so the published back leg never counted it.
- **(c)** Published every 90: Bruntál 1 of 2, Milotice 0 of 2 FAIL. With the back counted at the station: the rounds are 85 min apart
  (no interval), so two slots on 240, 360 or 480 all pass with 2 + 2 exact (240 and 480 checked: 1 bus); 480 is the longer and
  matches the line's five rounds a day.
- **(d)** 872: every 480, Bruntál Offset 289, Also at 374 (real 13:50, 15:15); Milotice Offset 309, Also at 394 (real 14:10, 15:35),
  `core_to` Bruntál, station.
- **(f)** Off: the morning rounds (4:45, 10:30; back 5:05, 7:05, 10:50). **(g)** Need 1 (waits Milotice 1, 1).

### 907 Vrbno – Vidly – Zlaté Hory
- **(b)** Vrbno 12:50, 15:15, 17:30 (also 5:35); Zlaté Hory 14:25, 16:30, 18:20 (also 6:25). In 15:30–17:30 only Zlaté Hory 16:30
  (17:30 is the window's end).
- **(c)** Published every 120 (Vrbno 15:15 / 17:15, Zlaté Hory 16:25): 0 of 1 both ways FAIL (IRREGULAR for Vrbno). Every 240 on
  the 15:15 / 16:30 round passes (1 + 1 exact). **Every 480 on all three rounds** passes too (no Vrbno slot in the window, Zlaté
  Hory 1 of 1) with 3 + 4 exact, and one bus chains them all (Vrbno 15:08 → 15:15, 17:13 → 17:30).
- **(d)** 907: every 480. Vrbno Offset 29, Also at 229, 374 (real 17:30, 12:50, 15:15); Zlaté Hory Offset 79, Also at 324, 449
  (real 18:20, 14:25, 16:30).
- **(f)** Off: Vrbno 5:35 only. **(g)** Need 1 (waits Vrbno 17, 107, 7; Zlaté Hory 9, 54, 34).

## Rýmařovsko

### 877 Rýmařov – Břidličná – Bruntál, station
- **(a)** Core points: Rýmařov AS; Bruntál, železniční stanice; Bruntál, KARLA. Model hours were 14:00–16:00, now 15:30–17:30.
- **(b)** Rýmařov → Bruntál 13:20, 14:00, 14:40, **15:40, 16:40**, 17:40, 22:20 (KARLA 12:40, 20:40); Bruntál → Rýmařov 12:05, 13:20,
  **15:40, 16:20**, 18:20, 20:20, 21:20 (KARLA 14:17, at the station 14:25). Plates: 84-2004 out 14:00, back on 920 15:21; 84-2009
  out 13:20, back as KARLA 14:17; 84-2008 out 14:40, back 15:40; 84-1001 back 16:20 from 909.
- **(c)** The KARLA trips were counted on 877 too; a main slot at 14:25 or 12:40 would run beside 877 KARLA, so they are left out
  (`notvia` KARLA). The 14:30 anchor came from the KARLA 14:17 and the Kovohutě → Rýmařov short (14:31, on the line's own
  stops); without them 14:00–16:00 equals 15:00–17:00, so 16:00 by hand. At the old window, with KARLA left out, nothing passes
  (3 out, 1 back). At 16:00, Bruntál's 15:40 and 16:20 are 40 min apart: every 60 fails at Bruntál (16:40 slot empty).

  | Candidate | Rýmařov exact | Bruntál exact | Need |
  |---|---|---|---|
  | every 120, Rýmařov 16:40 / Bruntál 16:20 | 3 | 3 | 2, but leaves Rýmařov with 877 KARLA at 12:40, 20:40 |
  | **every 120, Rýmařov 15:40 / Bruntál 16:20** | 2 | 3 | **2** |
  | every 120, Rýmařov 15:40 16:40 / Bruntál 15:40 16:20 | 5 | 4 | 3, same KARLA clash |
- **(d)** 877: every 120. Rýmařov Offset 39 (real 15:40, also 17:40), Bruntál Offset 79 (real 16:20, also 18:20, 20:20).
  877 KARLA unchanged (every 480, 12:40 / 14:17).
- **(e)** Model reaches Bruntál 16:27 and Rýmařov 17:06, as real.
- **(f)** Off: Rýmařov 13:20, 14:00, 14:40, 16:40 (buses back on 920 and 877 KARLA); Bruntál 12:05, 13:20, 15:40.
- **(g)** Need 2 (as before). Owner check rewritten: the published :34 / :24 failed Step 4; Rýmařov hourly :40 costs a third bus.

### 878 Rýmařov – Malá Morávka, Karlov
- **(b)** Rounds Rýmařov 6:00 / 6:45, **14:10 / 14:55** (84-1008), **15:30 / 16:10** (84-1002).
- **(c)** Published every 90 (Rýmařov 15:30, 17:00): 1 of 2 FAIL. **Every 480 on both afternoon rounds**: 2 + 2 exact (every 240 at
  15:30 / 16:10: 1 + 1), and the morning 6:00 / 6:45 falls 10 min from the 6:10 / 6:55 repeats.
- **(d)** 878: every 480, Rýmařov Offset 309, Also at 389 (real 14:10, 15:30); Karlov Offset 354, Also at 429 (real 14:55, 16:10).
- **(g)** Need 1.

### 880 Rýmařov – Stará Ves, Anenská Huť
- **(b)** Three back-to-back rounds, three buses that also work 922 and 912: Rýmařov **14:25** (from the station 14:20), **15:15,
  16:00**; Anenská Huť **14:45, 15:35, 16:15**. Every trip takes 15 min; after the 16:00 the bus turns in 0 min.
- **(c)** Published every 90 (Rýmařov 14:25, 15:55): 1 of 2 FAIL. Every 90 at any minutes fails (the gaps are 50 and 45). Three
  slots each way pass: every 180 (Rýmařov 3 of 3, 2 exact + 15:59; Anenská Huť 3 of 3, 5 exact with 6:35, 7:15), every 240 / 480
  (2 + 3), every 120 (2 buses). With the real 16:00 the 0-min turn needs a second bus; at 15:59 one bus works it.
- **(d)** 880: every 180. Rýmařov Offset 84, Also at 134, 178 (real 14:25, 15:15, 15:59); Anenská Huť Offset 14, Also at 104, 154
  (real 16:15, 14:45, 15:35).
- **(f)** Off: 12:50 / 13:05 and the Stará Ves, škola shorts. **(g)** Need 1 (waits Rýmařov 15, 9, 55; Anenská Huť 5, 1, 5).

### 922 Rýmařov – Tvrdkov, Ruda (and 922 Uničov)
- **(a)** Core points: Rýmařov, station; Rýmařov AS (the knot); Tvrdkov, Ruda; Uničov AS. Model hours 13:50–15:50.
- **(b)** Bus station → Ruda **13:55** (from the station 13:50), **15:50** (from the station 15:45), 17:25; Ruda → Rýmařov **14:20**,
  16:20, 17:50. One bus per round (84-2005, 84-1205, 84-2001). The Uničov trips pass Ruda at 12:53 and 15:48; they were counted on
  922 too and are now left out (`notvia` Uničov).
- **(c)** Published every 90 (station 14:15, Ruda 14:50): 1 of 2 and 0 of 1 FAIL. **Every 480 on the three rounds**: out 2 of 2, back
  1 of 1, 3 + 3 exact, 1 bus; every 240 on the window's rounds 2 + 2; every 120 1 + 2.
- **(d)** 922: every 480. Timed at the bus station 13:55, 15:50, 17:25 (`knot_at`), so the station gets Offset 19, Also at 289, 404
  (real 17:20, 13:50, 15:45); Ruda Offset 49, Also at 319, 439 (real 17:50, 14:20, 16:20). 922 Uničov unchanged.
- **(e)** Model passes Ruda 14:18 / 16:13, as real. The knot line on the way back compares with trips that run on to the station
  (the 14:20 ends at the bus station 14:45, which the model reaches at 14:45).
- **(g)** Need 1.

## MHD Krnov and Bruntál

### 801 Nemocnice – bus stand – Petrův důl
- **(a)** Core points: Nemocnice, hlavní brána; Petrův důl; průmyslová zóna II, točna. Model hours 13:40–15:40.
- **(b)** Nemocnice 13:48, 14:08, **14:35, 15:05, 15:35** (and :05 / :35 all morning, 8:35–11:35); Petrův důl 13:46, 14:20, 14:47,
  **15:05**, 15:37 (and :05 / :35 from 8:35 to 12:05). In 12:48–16:05 most trips run on to the industrial zone; the ones back pass
  Petrův důl at 13:20, 13:46, 14:20, 14:47, 15:37, 16:10 — these are 801 PZ's trips at the točna.
- **(c)** Only Petrův důl → Nemocnice failed (14:07, 14:37 empty). Every 30 at any minute fails there (at best 3 of 4). Passing
  patterns copy the zone shift times into the trunk all day: every 90 with four slots each way (13 + 8 exact, 4 buses, 8 typed
  values), every 120 with five each way (all ten window departures exact, 4 buses, 10 typed values). The trunk is kept every 30, now
  on the real :05 / :35 at both ends (the auto fit had :06 / :07): Nemocnice 11 exact over the day (was 0), Petrův důl 10 (was 3).
  Rule 4: approximate in the window, on the To check list.
- **(d)** 801: every 30, Nemocnice Offset 4 (real :05, :35), Petrův důl Offset 4 (real :05, :35). 801 PZ unchanged.
- **(f)** Off on the way back in the window: 13:46 (11), 14:20 (15), 14:47 (12). **(g)** Need 2 (as before). Owner check: every 120
  with five slots each way, 4 buses.

### 802 bus stand – Ježník, sanatorium
- **(b)** Three 45-min rounds: bus stand 13:10 / 13:30 (83-1008), 13:55 / 14:15 and 14:55 / 15:19 (81-1005), then 16:34 / 16:55.
  The 13:10 is just before the window, so the way back has three trips in it and the way out two.
- **(c)** Published every 60 (:55 / :15): Ježník 15:15 empty (real 15:19), 1 of 2 FAIL. **Every 160 with the three rounds**: out 2 of 2,
  back 3 of 3, 3 + 4 exact (16:35 / 16:55 within 1 / exact), 1 bus; every 160 with two rounds 2 + 3.
- **(d)** 802: every 160. Bus stand Offset 34, Also at 89, 134 (real 14:55, 13:10, 13:55); Ježník Offset 58, Also at 109, 154 (real
  15:19, 13:30, 14:15).
- **(g)** Need 1 (waits Ježník 1, 1, 5: the real turns).

### 805 Hlubčická, Na špici – Chomýž, točna
- **(b)** One bus (83-2010) alternates: Hlubčická 13:25, 14:40, 16:10; Chomýž 14:03, 15:35. The morning bus does Chomýž 10:30.
- **(c)** Published every 90 (Chomýž 17:05 slot): 1 of 2 FAIL. Every 240 / 480 with the two afternoon rounds: 2 + 2 exact. **Every
  480 with three each way** (Chomýž 10:30 as the third): 3 + 3 exact, 1 bus.
- **(d)** 805: every 480. Hlubčická Offset 264, Also at 339, 429 (real 13:25, 14:40, 16:10); Chomýž Offset 89, Also at 302, 394 (real
  10:30, 14:03, 15:35).
- **(g)** Need 1.

### 806 bus stand – Cvilín
- **(b)** Two 1-bus rounds 75 min apart: bus stand 14:45 / Cvilín 15:05 (81-1002), 16:00 / 16:20 (81-1005). 806 CLO's bus arrives at
  Cvilín 18:20 and goes straight back.
- **(c)** Published every 90: 0 of 1 both ways FAIL. Every 120 at 16:00 / 16:20 passes (1 + 3 exact) but leaves Cvilín at 18:20
  together with 806 CLO. **Every 480 on both rounds**: 2 + 2 exact, 1 bus, no shared minute.
- **(d)** 806: every 480. Bus stand Offset 344, Also at 419 (real 14:45, 16:00); Cvilín Offset 364, Also at 439 (real 15:05, 16:20).
  806 CLO unchanged.
- **(g)** Need 1.

### 851 Bruntál town loop (station – nový hřbitov – KARLA)
- **(b)** One bus (83-2001): station 12:50 → KARLA, back 14:12; station 16:40 → KARLA, back 17:27 (it then loops as 852).
- **(c)** Published every 180 (16:26, 17:12): 0 of 1 both ways FAIL. **Every 480 on both pairs**: 2 + 3 exact (KARLA 22:12 too),
  1 bus; every 240 the same exact count and twice as many runs.
- **(d)** 851: every 480. Station Offset 229, Also at 459 (real 12:50, 16:40), stops via nový hřbitov; KARLA Offset 26, Also at 311
  (real 17:27, 14:12).
- **(g)** Need 1.

## Left approximate

- **801 Petrův důl → Nemocnice** (every 30 at :05 / :35): the zone shift returns at 13:46, 14:20 and 14:47 are 11–15 min off.
  Passing patterns exist (every 90 / 120 with four or five slots each way) but fold the zone extension, which is its own
  Simutrans line (801 PZ, owner check), into the trunk all day, for 4 buses and 8–10 typed values. Kept at the real rate on the
  real minutes (rule 4) and offered to the owner.

## For the owner and the next steps

- **Owner checks** (`brn_config.py`): 877 rewritten; new 819, 861, 863, 801; 801 PZ, 913, 832 unchanged.
- **In-game changes:** 23 Simutrans lines get new values (901 keeps its own; 877 KARLA's window moved, values unchanged); they
  go from 46 typed values to 82 (907, 880, 922, 802 and 805 from 2 to 6 each). The
  change list (old → new per entry) is in the final report of this check; buses in / out follow from the orchestrator's roster
  rerun with `keep_roster` (no need changed, so no bus is added or freed by this check).
- **Same minute at a shared stop** (Step 5, checked over 12:00–19:00 for every Simutrans line of the sheet): 18 pairs, all
  different routes from one bus station or station (most are real, e.g. 822 and 833 at Krnov 15:45; 851, 861, 885 at Bruntál,
  station 16:40) or opposite directions (801 / 801 PZ at Petrův důl); no variant leaves with its main line. The 909 / 910 pairs
  at Bruntál, station (12:45, 14:45 …) were there before and are unchanged.
- **Not run here:** `04_roster.py`, `06_render.py`, the cross-sheet checks and publishing (the orchestrator's). The knot lines on
  the page show large deviations where a leg has no slot in its window (e.g. 814 Krnov, 816 Krnov, 907 Vrbno): there the check
  compares the slot's residue, not a modelled bus.
- **Shared-script observations (not changed):** the builder gives a trip to every leg it passes, so a variant's trips are also
  counted on the main line's legs unless `notvia` is set (818, 877, 922 here); the minimum 1-min turn makes a real 0-min loop
  cost a second bus (822, 814, 880); and an every-120 row with two slots 60 min apart (the 861 owner option) is really every 60.
