# Bus schedule method, applied to the Hlučínsko lines at sad B. Němcové (25 Oct 2026)

The owner asked for the lines 281, 282, 290 and 292 to be checked by hand, step by step against
`../bus-schedule-method.md` (v3), as the Hranečník lines were (`../ostrava-bus/method-check-odis-2026-10-20.md`):
"Yes, I want you to check - that's the point of you doing it, so you'll not produce incorrect results."
Their published rows (21 Oct, sheet v6) were the builder's automatic fits (`at: 'auto'`), and every one of them failed
Step 4. Final state: sheet v8.

- **Data:** the sheet's own JDF trips for Tue 20 Oct 2026 (`data/derived/trips.json`), the whole-day reading
  (`data/derived/reading/<L>.txt`) and the ODIS live-map plate chains (`chains.json`, 13:00–19:30).
- **Step 4 test**, per direction: in the model window the slots must equal the real departures ±1, and at least 80 % of
  the slots need a real departure within 3 min. Then most exact over the day, then the simplest.
- **Typed values** are (real − 61) mod every: every terminus is a loop.

## What the plates show: outstation lines

The buses of these lines sleep at the far ends: the Hať garage, Třebom, Strahovice, Chuchelná and Píšť. The first morning
trips start there (290 Hať 4:02–5:54, 281 Třebom 3:51, 292 Strahovice 3:46 / 4:48 / 6:03), and in the afternoon the
buses go home on the peak trips out of Ostrava. Between 14:00 and 17:00, 19 departures leave sad B. Němcové on the four
lines and 12 arrive. The deficit cannot be paired across the four lines (Step 5b): every one of them sends more out than
it brings back, and the live map shows the extra buses ending their day at the far end or running back empty for another
line (24-1105: out on 290 at 14:16, then back empty for 281 at 15:45).

So each line is timed both ways at its inbound rate, and the extra peak departures out of Ostrava (buses going home) are
off the pattern. That breaks Step 4's "slots = real departures ±1" out of Ostrava for 281 and 292, by the owner's choice:
- **v7 (withdrawn)** put the extra departures on B lines with an empty return (281B, 290B, 292B, the 387 / 543B
  precedent): 5 more buses, shuttling back empty all day in the game.
- **Owner, 25 Oct 2026:** "Unless those empty runs add something really needed and specific, don't add them just for
  frequency." The B lines ran the same stops as their core lines (coverage stays 0 uncovered without them), so they were
  dropped in v8.

Step 5b does pair two trips at Píšť. 282 out at 14:53 comes back as 292 at 15:53 (via Vřesina). 292 out of Hlučín at 14:30
comes back as 282 at 15:55 (via Bohuslavice). That is a 1:1 swap of paths, so it changes no count, and each line stays
balanced on its own path.

## Summary

| Line | Published (v6) | Step 4 | Now (v8) | Buses |
|---|---|---|---|---|
| 281 | every 60, Třebom :16 / Ostrava :18 | Třebom :16 is 15–20 min off the afternoon (15:01, 15:56) | every 60, Třebom :58 (Kobeřice :13) / Ostrava :18 | 3 → 3 |
| 282 | every 180, Píšť 15:55 / Ostrava 13:54 slot, model hour 13:00–15:00 | the 13:54 slot has no trip | every 120, Píšť :55 / Ostrava :53, model hour 16:00 | 1 → 1 |
| 290 | every 40, Hať :07 / Ostrava :19 | 3 slots for 5 departures out; 15:39 and 15:27 slots empty | every 120, four slots each way, exact | 3 → 4 |
| 292 | every 90, Ostrava 14:04 / Chuchelná 14:21 | 14:04 slot empty; 15:51 slot empty | every 80, Ostrava 14:33 / 15:53, back timed at Hlučín :59 | 2 → 2 |
| **Total** | | | | **9 → 10** |

The sheet needs 126 buses (was 125). The published buses stay where they are still seen on their line
(`config.keep_roster` = `data/published/roster_v6.json`): 281 takes 24-0002 in place of 24-0004 (whose 13:16 trip is now
off the pattern), and 290 adds 24-1111. The seven rows these lines had on the To check list are gone from the "slot without
a real departure" kind; 290's four slots are an owner check with the every-40 option.

## 290 Hať – Hlučín – Ostrava, Přívoz

- **(a) Core points:** Hať, točna; Hlučín, autobusové nádraží; Ostrava, Přívoz, sad B. Němcové. Model hours 14:40–16:40.
- **(b) Afternoon:** out of Ostrava (at sad B. Němcové) 13:59, 14:19, **14:44, 14:59, 15:24, 15:49, 16:19**, 16:54,
  17:29; from Hať 13:49, **14:47, 15:31, 16:07, 16:37**, 17:37 (to Hlučín), 18:08.
- **(c) Step 4 out of Ostrava** (window 5 real):

  | Candidate | Window slots | Within 3 min |
  |---|---|---|
  | every 40 :19 (published) | 3 | 2 of 3, FAIL |
  | every 30 :19 | 4 | 2 of 4, FAIL |
  | every 60 :19 :44 | 4 | 2 of 4, FAIL |
  | every 60 :24 :49 | 4 | 2 of 4, FAIL |
  | **every 120, 14:44 14:59 15:24 15:49** | 4 | 4 of 4, exact |

  From Hať (window 4 real): every 40 :07 2 of 3 FAIL; every 60 :07 :37 2 of 4 FAIL; every 60 :07 :47 2 of 4 FAIL;
  **every 120, 14:47 15:31 16:07 16:37**: 4 of 4, exact.
- **(d) Simutrans line 290:** every 120. Hať Offset 30, Also at 66, 96, 106 (real 15:31, 16:07, 16:37, 14:47); Ostrava
  Offset 23, Also at 48, 103, 118 (real 15:24, 15:49, 14:44, 14:59). The plates pair 14:44 → 15:31 (24-1104), 15:24 →
  16:07 (24-1006) and 15:49 → 16:37 (24-1111). The fifth departure is left off: 16:19 (24-1115 goes home to the garage),
  not 14:59; with 16:19 in the pattern instead, one bus waits 108 min at Hať and the line needs 5 buses, not 4.
- **(e) Knots:** Hlučín within 1 min of the real passing times (3 for 14:44); the model reaches sad B. Němcové 2 min after the
  real arrivals.
- **(f) Off the pattern 12–20 h:** out 12:09, 13:19 (5), 13:59 (10), 14:19, 16:19 (home runs), 16:54 (5), 17:29 (5); from
  Hať 12:29 (8), 13:49 (18), 19:58 (9); the Hlučín – Hať trips (17:37, 18:40) and the 13:39 to Hať, garáž ČSAD.
- **(g) Need:** 4 (waits Hať 33, 18, 7, 28; Ostrava 32, 11, 6, 21).

## 281 Třebom – Kobeřice – Hlučín – Ostrava, Přívoz

- **(a) Core points:** Třebom, náměstí; Kobeřice, autobusová stanice (the knot where the Třebom, Strahovice and Kobeřice
  trips split); Hlučín; sad B. Němcové. Model hours 14:10–16:10.
- **(b) Afternoon:** out of Ostrava 13:43, **14:18, 14:48, 15:18, 15:48** (Strahovice), 16:13 (Strahovice), 17:18; towards
  Ostrava, read at Kobeřice: 13:31, **14:11** (starts there), **15:16**, 16:11, 17:38 (Třebom 13:16, 15:01, 15:56, 17:16).
  Hlučín – Bolatice shuttles 13:40, 14:40, 15:10, and Bolatice 15:23 → Ostrava.
- **(c) Step 4:** back at Kobeřice: every 60 :11 1 of 2 FAIL; :16 1 of 2 FAIL; **:13** 2 of 2 within 3 min (14:11, 15:16;
  also 16:11). The published Třebom :16 is 15–20 min off every afternoon trip. Out of Ostrava the timetable is exactly every
  30 (:18 / :48); the line runs at the inbound rate, hourly at :18 (14:18, 15:18 exact).
- **(d) Simutrans line 281:** every 60, Třebom Offset 57 (real :58, so the bus passes Kobeřice at :13), Ostrava Offset 17
  (real :18).
- **(e) Knots:** out exact at Kobeřice and Třebom; back Hlučín 15:48 / 16:48 against 15:46 / 16:41 (the model's median
  running time to Hlučín includes the longer Bolatice path).
- **(f) Off the pattern:** out the :48 departures (12:48, 13:43, 14:48, 15:48; their buses go home), 16:13, 18:43; back
  Třebom 13:16, 17:16, 19:37; the Hlučín – Bolatice shuttles (Bolatice stops are on 252, 254 and 284).
- **(g) Need:** 3 (waits Třebom 35, Ostrava 22).

## 282 Píšť – Bohuslavice – Hlučín – Ostrava, Přívoz

- **(a) Core points:** Píšť, kostel; Hlučín; sad B. Němcové.
- **(b) Afternoon:** Píšť leaves exactly every 2 h at :55: 13:55 (to Dolní Benešov), **15:55** (to Ostrava), 17:55,
  19:55, 21:55 (to Hlučín). Ostrava → Píšť 14:18, **14:53**, **16:54**; Hlučín → Píšť 16:10, 18:10, 19:15 (with the
  Ostrava trips, hourly at :10 at Hlučín from 15:10 to 18:10). Hlučín – Závada shuttles 13:05 / 13:28, 14:05 / 14:28.
- **Model hour:** the line's busiest stretch, 13:00–15:00, is the Závada shuttles, whose stops are all on 282. Its
  pattern runs later, so the anchor is set by hand to 16:00 (window 15:30–17:30), as was done for 451 and 533.
- **(c) Step 4:** published every 180 (Ostrava 13:54 slot): 0 of 1 FAIL. **Every 120:** Píšť :55 exact 4 times
  over the day; Ostrava :53 (14:53, 16:54).
- **(d) Simutrans line 282:** every 120, Píšť Offset 54 (real 13:55, 15:55, 17:55; read to Hlučín, as the later trips end
  there), Ostrava Offset 112 (real 14:53, 16:53).
- **(e) Knots:** Hlučín within 1–3 min.
- **(f) Off the pattern:** Ostrava 14:18; Hlučín → Píšť 16:10, 18:10 (their stops are on 282); the Závada shuttles.
- **(g) Need:** 1 (waits Píšť 16, Ostrava 13). Bohuslavice has no other line.

## 292 Ostrava, Přívoz – Hlučín – Vřesina – Píšť – Chuchelná / Strahovice

- **(a) Core points:** sad B. Němcové; Hlučín (the knot for the way back: the trips start at Píšť, Chuchelná or
  Strahovice); Píšť, Mýto (where the Chuchelná and Strahovice paths split); Chuchelná, železniční stanice. Model hours
  14:00–16:00.
- **(b) Afternoon:** out of Ostrava 13:29 (Píšť only), 13:53, **14:33, 14:58, 15:33, 15:53**, 17:04, 18:49; towards
  Ostrava, at Hlučín 13:39 (Píšť), **15:02** (Chuchelná), 16:16 (Píšť), 17:26 (Strahovice), 19:34 (Strahovice).
- **(c) Step 4:** back at Hlučín: every 80 :59 (13:39, 14:59, 16:19; within 3, 17:26 is 13 off) and every 72 (15:02, 16:14,
  17:26; 13:39 11 off) both pass in the window; 72 hits one more on the minute, but only 80 lets the line leave Ostrava on
  two exact departures (14:33, 15:53), so 80. The published every 90 (Ostrava 14:04) 1 of 2 FAIL, Chuchelná 15:51 slot
  empty. Out of Ostrava the timetable is every 30 (:33 and :53–:58); the line runs at the inbound rate.
- **(d) Simutrans line 292:** every 80, Ostrava Offset 12 (real 14:33, 15:53), Chuchelná Offset 77 (real 14:18, 15:38; the
  bus passes Hlučín at 14:59 / 16:19). Out trips are counted to Píšť, Mýto, so the Strahovice runs (15:53) count.
- **(e) Knots:** out Hlučín 14:49 / 16:09 (real 14:50 / 16:10). The sheet's knot check shows 18–19 min for the 15:53 slot and 77
  at sad B. Němcové for the 15:38 slot. Those compare only with trips that run the whole Chuchelná path; the 15:53 runs to
  Strahovice by the other path and the 15:38 slot stands for the Píšť 15:53 trip, both within 1–3 min at Hlučín.
- **(f) Off the pattern:** out 12:34, 13:29 (Píšť only), 13:53, 14:58 and 15:33 (their buses go home to Chuchelná /
  Strahovice), 17:04, 18:49; back at Hlučín 17:26 (13), 19:34; the Hlučín – Vřesina / Píšť Mýto shorts and the
  Chuchelná – Strahovice and Bělá shuttles (stops on 292 and 282).
- **(g) Need:** 2 (waits Ostrava 39, Chuchelná 9).

## Shared stop: sad B. Němcové (Step 5)

Model departures 14:00–16:20 of the four lines: 14:18 (281), 14:33 (292), 14:44 (290), 14:53 (282), 14:59 (290), 15:18
(281), 15:24 (290), 15:49 (290), 15:53 (292), 16:18 (281). Every one but 281's 16:18 (real 16:13, a Strahovice trip) is a
real departure, and no two leave within 3 min. The DPO lines at the same stop (34, 56, 67, 68 …) were not changed.

## Buses and other sheets

- 281: 24-1103, 24-1010, 24-0002 (in place of 24-0004). 282: 24-1001. 290: 24-1104, 24-1102, 24-1009, 24-1111 (added).
  292: 24-1116, 24-1007. All seen on these lines on 20 Oct; every other line of the sheet keeps its buses.
- No bus is on two sheets: checked against the HKO, TFJ, Novojičínsko and Bruntálsko rosters, the Ostrava Hranečník cards
  and the Havířov/Karviná/Orlová town sheet (the roster step excludes the 304 plates of the earlier sheets).
- `keep_roster` is new in the shared `odis-regional-hko/scripts/04_roster.py` (step 6, opt-in per sheet): published buses
  stay on their Simutrans line wherever they are still evidence for it, so a rebuild moves the fewest buses.
- **Pooling (not applied):** the real buses swap between these lines at sad B. Němcové all afternoon. One pool for the
  corridor would need fewer buses than 10 separate ones. That is the owner's choice.
