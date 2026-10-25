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
a real departure" kind. The owner chose 290's four slots (4 buses) over every 40 (3 buses): "290 uses more buses".

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

## The rest of the sheet

Owner, after the four lines above: "verify all sheets with this level of detail". The work list was this sheet's part of
`../audit/audit-regional-2026-10-25.md`: 58 failing legs on 34 Simutrans lines (55 EMPTY, 3 FEWER). 281, 282, 290 and 292
stay as above (their FEWER rows are the owner-approved outstation case). Every other failing line was read over the whole
day (`data/derived/reading/<L>.txt`, plates from the 20 Oct live map) and set by hand in `authoring/opa_spec.py`; the cards
are in `authoring/opa_notes.py`, the new owner checks in `authoring/opa_config.py`. Typed values are (real − 61) mod every
(every terminus is a loop); each real time below is worked out from its own value. Model windows are each line's anchor
−30 to +90 (`05_schedule`), except where set by hand (075, 555, 285).

**How the candidates were chosen.** For each line both directions were searched together: every interval of the method's
list (10 … 480) and 1–8 slots per direction, the slots placed on the window's real departures, both directions on the
same interval with the same number of slots (Step 7), and the need from the slot matching of `05_schedule`. Then:
1. **Gate:** Step 4 in each direction (window slots = real departures ±1; at least 80 % of the slots with a real departure
   within 3 min). Where a direction has two or more departures in the window the interval is at most 120, so the pattern
   repeats at least as often as the window it stands for (every 160 with three slots also "fits" a 2-hour window, at
   three quarters of the real rate).
2. **Order among passing rows:** most departures exactly on the minute over the day (5–23), then within 1 min, then fewest
   slots, then fewest buses. On one-departure-per-window lines these counts are 1–3 and mostly tie; there the real
   13:00–18:00 headway decides, never "the longer interval" (a 2-hourly line is not pulled to 240 or 480).
3. **More buses than a passing cheaper row** (the cheaper one has one slot fewer than the window's departures, or is the
   earlier approximate row): the exact row goes on the sheet, the cheaper one on the owner checks with its saving (the
   290 precedent: "290 uses more buses").
4. **Window imbalance** (more out than back): the outstation rule of 25 Oct, inbound rate, the departures that fall off
   chosen by the plates and the waits.
5. **Hourly line, narrow window** (mistakes table: 409 and 411): an hourly row with one stray trip stays hourly,
   approximate, rather than be halved by a passing every 120.
6. **No pattern passes both ways:** the simplest even row at the real rate, approximate, on the To check list.

Rebuilt with `05_schedule.py --base odis-regional-opavsko`: coverage 633 afternoon stops, 0 uncovered. Re-audit
(`step4_regional.py odis-regional-opavsko`): 141 timed legs, 128 ok (was 85 of 143), 10 EMPTY, 3 FEWER; the failing ones
are the approximate rows and owner checks listed at the end, and the three FEWER rows are 281, 292 and 236 (outstation).

### Summary

| Line | Published (v8) | Step 4 | Now | Buses |
|---|---|---|---|---|
| 075 | every 20, Hlučín :12 / Poruba :19, model hour 14:10 | Hlučín 6 slots for 8 departures (the :02 / :22 extras) | the same row, model hour 16:00 by hand | 4 → 4 |
| 212 | every 40, Divadlo :14 / Vlaštovičky :27 | 16:14, 15:47, 17:07 empty | every 120, three slots each way, exact | 2 → 2 |
| 215 | every 60, Liliová :09 / Globus :39 | all four window slots empty | every 80, two slots each way, exact | 1 → 2 |
| 216 | every 30, Dolní nám. :04 / Držkovice :00 | half the slots empty | every 120, four slots each way, exact | 2 → 2 |
| 218 | every 60, Koupaliště :19 / Chvalíkovice :09 | 17:19, 17:09 empty | every 120, two slots each way, exact | 2 → 2 |
| 219 | every 30, Malé Hoštice :16 / Otice :12 | 16:46, 17:16, 17:12 empty (4 min) | every 120, four slots each way, exact | 2 → 2 |
| 220 | every 30, Praskova :15 / Přerovec :18 | half the slots empty | every 60, two slots each way | 2 → 2 |
| 233 | every 90, Vítkov 16:15 / Melč 15:30, 17:00 | Melč slots empty | every 120, Vítkov 16:15 / Melč 15:45 | 1 → 2 |
| 236 | every 40, Vítkov :00 / Budišov :10 | 4 of 6 slots empty | every 120, inbound rate (outstation) | 2 → 2 |
| 238 | every 60, Vítkov :12 / Odry :30 | all four slots empty | every 90, Vítkov 16:32 / Odry 16:10 | 2 → 2 |
| 240 | every 60, Opava :06 / Vítkov :40 | 15:06, 14:40, 15:40 empty | every 120, two slots each way, exact | 3 → 3 |
| 241 | every 90, Opava 15:04 / Vítkov 15:07 | Vítkov slot 8 min off | every 120, two slots each way, exact | 2 → 4 |
| 242 | every 60, Opava :40 / Vítkov :15 | 14:40, 15:40, 15:15 empty | every 120, two slots each way, express pair listed | 3 → 3 |
| 245 | every 180, Opava 15:23 / Benkovice 15:55 | Opava slot empty | every 80, Opava 14:08 / Benkovice 14:35 | 1 → 1 |
| 248 | every 60, Opava :53 / Heřmanice :45 | Heřmanice 13:45 empty | kept (hourly, approximate; owner check) | 2 → 2 |
| 249 | every 120, Opava 14:33 / V. Heraltice 13:52 | both slots empty | every 120, Opava 15:02 / V. Heraltice 14:07 | 1 → 1 |
| 251 | every 60, Opava :35 / Chlebičov :05 | Opava 15:35 empty | kept (hourly, approximate) | 1 → 1 |
| 252 | every 60, Opava :25 / Kobeřice :45 | Opava 14:25 (5 min), 15:25 empty | every 120, two slots each way, exact | 2 → 3 |
| 254 | every 90, Opava 16:28 / Chuchelná 14:30 | 14:58, 16:00 empty | kept (no pattern passes; approximate) | 2 → 2 |
| 262 | every 90, Opava 14:13 / Bílovec 14:10 | 15:43, 14:10, 15:40 empty | every 120, two slots each way, exact | 2 → 3 |
| 263 | every 120, Opava 16:38 / Těškovice 17:13 | both slots empty | every 120, inbound rate (outstation) | 2 → 2 |
| 264 | every 120, Opava 16:21 / Těškovice 17:29 | both slots empty | every 120, Opava 16:44 / Těškovice 16:03 | 1 → 2 |
| 270 | every 90, Opava 16:49 / Svinov 15:38, 17:08 | all slots empty | every 80, Opava 16:19 / Svinov 16:26 | 2 → 2 |
| 284 | every 120, Hlučín 15:52 / Štěpánkovice 16:24 | Hlučín slot empty | every 120, inbound rate, Hlučín 17:28 | 1 → 1 |
| 285 | every 90, Poruba 16:11 / Štítina 16:48 | both slots empty (the line ends at 15:50) | every 120 in its own window 13:00–15:00 | 1 → 2 |
| 285 Dobroslavice | every 60, Poruba :08 / Dobroslavice :21 | 3 of 4 slots empty | dropped: all its stops are on 285 | 1 → 0 |
| 293 | every 90, Hlučín 16:55 / Bohumín 16:11 | both slots empty | every 96, Hlučín 17:05 / Bohumín 16:22 | 1 → 1 |
| 555 | every 30, Bohumín :28 / Ostrava :20, model hour 14:00 | 13:58, 13:50, 14:20 empty | every 60 two slots each way, model hour 16:00 | 4 → 4 |
| 678 | every 120, Svinov 16:55 / Vítkov 16:45 | both slots empty | every 144, Svinov 16:35 / Vítkov 17:20 | 2 → 2 |
| 217, 920 | (owner checks) | slots empty | not changed (see the end) | 1, 8 |
| **Total** | | | | **126 → 133** |

The seven extra buses: 241 +2, 215, 233, 252, 262, 264 +1 each, 285 +1 and 285 Dobroslavice −1. Three owner checks offer the
cheaper rows: 241/252/262 (4 buses fewer), 215/233/264 (3 fewer) and 248 (1 fewer).

### Opava town lines (MDPO buses)

**212 Divadlo – Milostovice – Vlaštovičky**
- (a) Core points: Divadlo; Milostovice (the knot: the short trips turn there; read there both ways); Vlaštovičky.
  Window 15:30–17:30.
- (b) Out of Divadlo 13:30, 14:38, 15:00 (to Milostovice), **15:37, 16:02, 16:54** (to Milostovice), 17:32, 18:34; back
  at Milostovice (terminal time = Milostovice − 6) 12:55, 14:10, 15:08, **15:35** (starts at Milostovice 15:41), **16:27,
  16:39, 17:15**, 18:03. Two buses: 408 and 160 (160 also runs the Milostovice shorts).
- (c) Published every 40: Divadlo 3 slots / 3 real, 2 filled FAIL; Vlaštovičky 3 / 4, 1 filled FAIL. Every 120 with three
  slots: Divadlo 15:37 / 16:02 / 16:54 3 / 3 filled 3, 3 exact over the day; Vlaštovičky 15:35 / 16:27 / 16:39 3 / 4,
  filled 3, 3 exact; need 2 (the other back triples need 3). Nothing at 120 or less passes with fewer slots.
- (d) **212** every 120. Divadlo Offset 36 (15:37), Also at 61 (16:02), 113 (16:54); Vlaštovičky Offset 34 (15:35),
  Also at 86 (16:27), 98 (16:39).
- (e) Milostovice out 15:53 / 16:18 exact; Divadlo back 16:49 / 17:01 exact. 16:54 out and 15:35 back stand for
  Milostovice shorts (the model bus runs them to Vlaštovičky), so the card's knot check, which compares with whole trips,
  shows 38 and 27 there.
- (f) Off the pattern 12–20 h: out 12:17, 13:30, 14:38, 15:00, 17:32, 18:34; back 12:55, 14:10, 15:08, 17:15, 18:03,
  19:03.
- (g) Need 2 (waits Divadlo 5, 36, 5; Vlaštovičky 16, 20, 29).

**215 Liliová – Kylešovice, škola – Globus**
- (a) Liliová; Kylešovice, škola (the knot; short trips end there); Globus. Window 15:30–17:30.
- (b) Out of Liliová 14:09, 15:23, **15:57** (short), **16:45, 17:16** (short), 18:07; back at škola 13:45, 14:58 (short),
  **16:20, 16:52** (short), 17:42. On 20 Oct 405 ran the whole line and 403 the Liliová – škola shorts (15:42 – 17:38).
- (c) Published hourly: Liliová 2 slots / 3 real, 0 filled; Globus 2 / 2, 0 filled; FAIL. No hourly phase passes either
  way. Every 80 with two slots: Liliová 15:57 / 16:45 (window 15:57, 16:45, 17:17 for 15:57, 16:45, 17:16) 3 / 3 filled 3,
  2 exact, 4 within 1; Globus 16:14 / 16:46 2 / 2 filled 2, 3 exact; need 2. Every 120 with 15:57 / 17:16 and the same
  Globus pair: 2 + 2 exact, need 2 (fewer hits).
- (d) **215** every 80. Liliová Offset 16 (15:57), Also at 64 (16:45); Globus Offset 33 (16:14), Also at 65 (16:46),
  timed so the bus passes Kylešovice, škola at 16:20 / 16:52.
- (e) škola and Globus exact for 16:45; the 15:57 and 17:17 slots stand for the shorts (the knot check against whole
  trips shows 32–34 there).
- (f) Off: out 12:49, 14:09, 19:17; back 12:19, 13:39, 18:48, 19:48.
- (g) Need 1 → 2 (waits Liliová 4, 4; Globus 21, 21). Owner check: the earlier hourly :09 / :39, 1 bus, approximate.

**216 Dolní náměstí – Vávrovice, Držkovice**
- (a) Dolní náměstí; Vávrovice, Držkovice. Window 14:00–16:00 (anchor 14:30).
- (b) Out 12:26, 13:05, 13:55, **14:34, 14:57, 15:34, 15:54**, 16:42, 17:21, 18:06, 18:42; back 12:35, 13:00, **14:00,
  14:26, 15:01, 15:24**, 16:09, 16:47, 17:34.
- (c) Published every 30: 4 slots / 4 real, 2 filled, FAIL both ways. Every 120 with four slots: 4 / 4 filled 4 both
  ways, 4 + 4 exact over the day, need 2. Every 60 :34 / :54, :00 / :26: passes too, 3 + 4 exact, need 2.
- (d) **216** every 120. Dolní náměstí Offset 33 (15:34), Also at 53 (15:54), 93 (14:34), 116 (14:57); Držkovice Offset
  0 (15:01), Also at 23 (15:24), 59 (14:00), 85 (14:26). Out via Vávrovice, OPAVIA as before.
- (e) Držkovice arrivals exact; Dolní náměstí arrivals within 3.
- (f) Off: out 12:26, 13:05, 16:42, 17:21, 18:06, 18:42, 19:12; back 12:35, 16:09, 16:47, 17:34, 18:08, 18:42, 19:12.
- (g) Need 2 (waits 11, 8, 10, 7 and 10, 5, 5, 4).

**218 Koupaliště – Dolní náměstí – Chvalíkovice**
- (a) Koupaliště; Dolní náměstí; Chvalíkovice. Window 15:30–17:30.
- (b) Out of Koupaliště 13:34, 14:17, 15:11, **15:38, 16:19, 17:10**, 18:29; back 14:09, 14:54, 15:19, **15:46, 16:10**,
  17:51 (407 also runs Chvalíkovice → Praskova 16:54, not via Koupaliště).
- (c) Published hourly: 2 / 3 filled 1 and 2 / 2 filled 1, FAIL. Every 120: Koupaliště 16:19 / 17:10 2 / 3 filled 2,
  Chvalíkovice 15:46 / 16:10 2 / 2 filled 2, 2 + 2 exact, need 2 (15:38 / 17:10 also passes, same counts, worse worst
  deviation).
- (d) **218** every 120. Koupaliště Offset 9 (17:10), Also at 78 (16:19); Chvalíkovice Offset 45 (15:46), Also at 69
  (16:10).
- (e) Dolní náměstí and both ends exact.
- (f) Off: out 12:34, 13:34, 15:38, 18:29, 19:52; back 12:29, 13:09, 14:54, 15:19, 17:51, 19:11.
- (g) Need 2 (waits Koupaliště 4, 31; Chvalíkovice 81, 6).

**219 Malé Hoštice – Praskova – Otice, kaple**
- (a) Malé Hoštice; Praskova; Otice, kaple. Window 15:30–17:30.
- (b) Malé Hoštice every 30 at :16 / :46 until 16:16, then **16:42, 17:12**, 17:52; Otice :12 / :42 until 16:42, then
  **17:08**, 17:42.
- (c) Published every 30: 4 / 4 filled 2 and 3, FAIL (16:46, 17:16 and 17:12 are 4 min off). Every 120 with four slots:
  4 / 4 filled 4 both ways, 7 + 10 exact over the day, need 2. Every 30 moved 2 min (:14 / :10) passes too, 2 + 0 exact.
- (d) **219** every 120. Malé Hoštice Offset 11 (17:12), Also at 45 (15:46), 75 (16:16), 101 (16:42); Otice Offset 7
  (17:08), Also at 41 (15:42), 71 (16:12), 101 (16:42).
- (e) Praskova and both ends exact.
- (f) Off: Malé Hoštice 14:46, 15:16 (4 min), 12:06, 12:36, 13:06 (6–10 min), 17:52, 18:57, 19:58; Otice 15:12 (4 min),
  12:02, 12:32, 13:12, 18:22, 19:22.
- (g) Need 2 (waits Malé Hoštice 14, 10, 10, 18; Otice 3, 3, 3, 7).

**220 Praskova – Suché Lazce, Přerovec**
- (a) Praskova; Přerovec. Window 15:30–17:30.
- (b) Out **15:40, 16:15, 16:37, 17:15, 17:29**; back **15:50, 16:12, 16:50, 17:10**.
- (c) Published every 30 (:15 / :18): 4 / 5 and 4 / 4, 2 filled each, FAIL. Hourly with two slots, Praskova :15 / :40,
  Přerovec :12 / :50: 4 / 5 filled 4, 4 / 4 filled 4, 8 + 4 exact, need 2 (every 120 with four slots: 7 + 4).
- (d) **220** every 60. Praskova Offset 14 (:15), Also at 39 (:40); Přerovec Offset 11 (:12), Also at 49 (:50).
- (e) Within 3 at both ends.
- (f) Off: Praskova 17:29, 12:49, 13:20, 13:50, 14:20; Přerovec 13:18, 13:55, 17:41, 18:05.
- (g) Need 2 (waits Praskova 3, 6; Přerovec 10, 13).

### Vítkovsko

**233 Vítkov – Moravice – Melč**
- (a) Vítkov AS; Melč, střed. Window 15:30–17:30.
- (b) Vítkov 12:00, 14:45, **16:15**, 18:35; Melč 13:00, 14:01, 15:02, **15:45**, 19:15 (14:01 and 15:02 are Opava buses
  off 247 and 240 going to Vítkov).
- (c) Published every 90: Vítkov 16:15 1 / 1 filled; Melč 15:30 and 17:00 2 / 1, 0 filled, FAIL. Every 120, Vítkov 16:15
  / Melč 15:45: 1 / 1 filled both, 2 + 1 exact, need 2. Every 90 cannot hold 15:45 without an empty 17:15; every 144, 160,
  180 pass with fewer hits, all need 2.
- (d) **233** every 120. Vítkov Offset 74 (16:15); Melč Offset 44 (15:45).
- (e) Melč and Vítkov arrivals within 2.
- (f) Off: Vítkov 12:00, 14:45, 18:35; Melč 13:00, 14:01, 15:02, 19:15.
- (g) Need 1 → 2: Melč 15:45 leaves before the 16:15 bus gets there (on 20 Oct 23-1013 and 23-2001 ran them). Owner
  check: the earlier every 90, 1 bus.

**236 Vítkov – Budišov**
- (a) Vítkov AS; Budišov AS. Window 15:30–17:30.
- (b) Out of Vítkov 14:15, 14:40, **15:35, 16:00, 16:20, 17:25**, 19:55; back 14:05, 14:25, **15:40, 16:50**, 17:30, 19:30.
- Plates: 23-1007 out 15:35, 237 to Staré Oldřůvky, back 16:50; 23-1008 out 16:00, 237 to Dvorce, back 17:30; the bus of
  15:40 back goes out at 16:20 and ends at Budišov; 23-1020 out 17:25 ends at Budišov; 23-2006 sleeps there after the
  Podlesí trips. The buses sleep at Budišov (236 / 237 start there in the morning): an outstation line.
- (c) Published every 40: 3 / 4 filled 1 and 3 / 2 filled 1, FAIL. No row passes both ways (4 out, 2 back). At the
  inbound rate, every 120: Budišov 15:40 / 16:50 2 / 2 filled 2, 4 exact; Vítkov pairs tested: 15:35 / 16:00 (the two
  buses that come back) 6 exact, need 2; 15:35 / 16:20 4 exact, need 2; 16:00 / 16:20 4, need 2; any pair with 17:25
  needs 2–3.
- (d) **236** every 120. Vítkov Offset 34 (15:35), Also at 59 (16:00); Budišov Offset 39 (15:40), Also at 109 (16:50).
- (e) Both ends exact.
- (f) Off: Vítkov 16:20, 17:25 (buses going home), 13:20, 14:15, 14:40, 19:55; Budišov 13:15, 14:05, 14:25, 17:30, 19:30.
  The Vítkov row has two slots for four departures (FEWER in the audit; the outstation case).
- (g) Need 2 (waits Vítkov 29, 4; Budišov 34, 109). 236 Podlesí unchanged (trips and need checked).

**238 Vítkov – Jakubčovice – Odry**
- (a) Vítkov AS; Odry AS. Window 15:30–17:30.
- (b) Vítkov 12:57, 13:50, 14:12, 15:23, **16:32**, 17:55; Odry 12:20, 14:40, **16:10**, 17:30, 18:30 (every 70–90).
- (c) Published hourly: 2 / 1 filled 0 both ways, FAIL. Every 90 (16:32 / 16:10): 1 / 1 filled, 1 + 2 exact, 2 + 3
  within 1, need 2; every 80: 1 + 2 exact, 2 + 2 within 1, need 2; every 96: 2 + 1, need 2.
- (d) **238** every 90. Vítkov Offset 31 (16:32); Odry Offset 9 (16:10). Routed via Klokočůvek and Loučky as before.
- (e) Odry 17:08 (real 17:11), Vítkov 16:44 (real 16:49): the model's median running time.
- (f) Off: Vítkov 12:57, 13:50, 14:12, 15:23, 17:55; Odry 12:20, 17:30, 18:30.
- (g) Need 2 (waits Vítkov 78, Odry 23).

**678 Ostrava, Svinov – Fulnek – Vítkov**
- (a) Svinov nádraží; Fulnek, náměstí; Vítkov AS. Window 15:30–17:30.
- (b) Svinov 13:05, 15:25, **16:35**, 18:55; Vítkov 14:45, **17:20**, 19:39 (about every 2 h 20).
- (c) Published every 120 (16:55 / 16:45): 0 of 1 filled both ways, FAIL. Every 144 (16:35 / 17:20): 1 / 1 filled, 1 + 1
  exact, need 2; every 120 with the same two departures needs 3; 160 and 180 need 2 with the same hits.
- (d) **678** every 144. Svinov Offset 70 (16:35); Vítkov Offset 115 (17:20). Back via Bravantice, Lidl as before.
- (e) Fulnek and both ends exact.
- (f) Off: Svinov 13:05, 15:25, 18:55 (4); Vítkov 14:45, 19:39 (5).
- (g) Need 2 (waits Svinov 9, Vítkov 102).

### Opavsko (Opava, Bílovecká TQM)

**240 Opava – Hradec – Melč – Vítkov**
- (a) Opava TQM; Hradec žst; Melč; Vítkov. Window 14:00–16:00.
- (b) Opava **14:06, 14:58**, 16:34 (and Melč shorts 13:19, 14:24); Vítkov 12:37, 13:40, **14:32, 15:16, 15:51**, 17:22.
- Step 5b: 240, 241 and 242 share their buses at both ends. 23-1010 runs 242 out (Opava 12:40, 14:45 express) and 240 back
  (Vítkov 13:40, 15:51): a 242-out / 240-back circuit. Not built as its own line (05 competes trips within one line, so it
  would count 15:51 twice); 15:51 is listed as its return.
- (c) Published hourly: 2 / 2 filled 1 and 2 / 3 filled 0, FAIL. Every 120, Opava 14:06 / 14:58, Vítkov 14:32 / 15:16:
  2 / 2 and 2 / 3, all filled, 2 + 2 exact, need 3 (with 15:51 instead of 15:16 or 14:32: need 3 or 4).
- (d) **240** every 120. Opava Offset 65 (14:06), Also at 117 (14:58); Vítkov Offset 15 (15:16), Also at 91 (14:32).
- (e) Hradec, Melč, Vítkov within 5; back exact at Melč, Hradec and Opava.
- (f) Off: Opava 16:34; Vítkov 12:37, 13:40, 15:51, 17:22; the Melč shorts.
- (g) Need 3 (waits Opava 44, 36; Vítkov 31, 7).

**241 Opava – Štáblovice – Melč – Vítkov**
- (a) Opava TQM; Melč; Vítkov. Window 14:00–16:00.
- (b) Opava 12:53, **14:14, 15:04**, 18:40; Vítkov 13:03, 13:37, **14:51, 15:15**, 16:41, 18:47. Four buses ran the four
  window trips (23-2010, 22-1055 out; 23-2002, 23-1004 back), all from the Opava – Vítkov pool.
- (c) Published every 90 (15:04 / 15:07): Opava 1 / 2 filled; Vítkov 1 / 2, 0 filled (8 min off), FAIL. Every 120 with
  both pairs: 2 / 2 filled both ways, 2 + 2 exact, need 4. Every 90 with Opava 15:04 / Vítkov 15:15: passes, 1 / 2
  filled 1 each way, 1 + 1 exact, need 2. Every 80 with the same pair passes too (1 + 1, need 2).
- (d) **241** every 120. Opava Offset 3 (15:04), Also at 73 (14:14); Vítkov Offset 14 (15:15), Also at 110 (14:51). Back
  via Vítkov, Zálužné as before.
- (e) Melč within 1, Vítkov 1 / 6; back exact.
- (f) Off: Opava 12:53, 18:40; Vítkov 13:03, 13:37, 16:41, 18:47.
- (g) Need 2 → 4 (waits Opava 3, 77; Vítkov 45, 119). Owner check: every 90 with one slot each way, 2 buses. 241 Lipina
  unchanged.

**242 Opava – Hradec – Březová – Vítkov**
- (a) Opava TQM; Vítkov AS. Window 14:30–16:30.
- (b) Opava **14:35, 15:30, 16:25**, 18:40 and the express 14:45 (9 stops, via Vítkov, Jelenice); Vítkov 14:15, **15:33,
  16:15** and the express 14:30 (7 stops). Plates: 22-1019 out 14:35, back 16:15; 23-1002 out 15:30 and 22-1052 out 16:25
  go on as 238 at Vítkov; 22-2002 back 15:33 came out on 240.
- (c) Published hourly: Opava 2 / 4 filled 0; Vítkov 2 / 3 filled 1, FAIL. The express pair is a variant folded into the
  row (Step 11): taken out with `via` Branka u Opavy (every express skips it), listed on the card (Jelenice is on 234).
  Then every 120 with two slots each way: all need 3; Opava 15:30 / 16:25 3 exact, 14:35 / 16:25 3 exact, 14:35 / 15:30 2.
  By the plates the departure left off is one whose bus goes on to 238 (15:30 or 16:25); keeping 16:25 puts one more on
  the minute, so 15:30 is off (the plain ranking would keep 15:30 / 16:25: the same 3 exact, a smaller worst deviation).
- (d) **242** every 120. Opava Offset 84 (16:25), Also at 94 (14:35); Vítkov Offset 32 (15:33), Also at 74 (16:15).
- (e) Vítkov arrivals 2–4 off (median running time); Opava arrivals exact.
- (f) Off: Opava 12:40, 15:30, 18:40 and the express 14:45; Vítkov 12:50 and the express 14:30.
- (g) Need 3 (waits Opava 1, 89; Vítkov 54, 2).

**245 Opava – Hradec – Benkovice**
- (a) Opava TQM; Benkovice, střed. Window 14:00–16:00.
- (b) Opava 12:48, **14:08, 15:28**, 18:23; Benkovice **14:35, 15:55**: exactly every 80.
- (c) Published every 180 (15:23 / 15:55): Opava 0 of 1 filled, FAIL. Every 80: 2 / 2 filled both ways, 3 + 2 exact, need
  1.
- (d) **245** every 80. Opava Offset 67 (14:08); Benkovice Offset 14 (14:35).
- (e) Exact both ways.
- (f) Off: Opava 18:23 (to Žimrovice). The Benkovice slot also falls on 13:15, the minute 245 zámek leaves Benkovice for
  the zámek (other direction; noted on the card).
- (g) Need 1 (waits Opava 29, Benkovice 2). 245 zámek unchanged.

**249 Opava – Jaktař – Velké Heraltice**
- (a) Opava TQM; Velké Heraltice AS. Window 13:30–15:30 (the lib's anchor), one departure each way.
- (b) Opava 11:43, **15:02**, 16:33, 18:43; Velké Heraltice 12:55, **14:07**, 15:50, 17:12.
- (c) Published every 120 (14:33 / 13:52): both 0 of 1, FAIL. Every 120 (15:02 / 14:07): 1 / 1 filled both, 1 + 1 exact,
  need 1; 144 and 160 the same hits, need 1.
- (d) **249** every 120. Opava Offset 1 (15:02); Velké Heraltice Offset 66 (14:07).
- (e) Velké Heraltice exact; Opava 2.
- (f) Off: Opava 16:33, 18:43; Velké Heraltice 12:55, 15:50, 17:12.
- (g) Need 1 (waits 17, 23). 249 Tábor unchanged.

**252 Opava – Kravaře – Štěpánkovice – Kobeřice**
- (a) Opava TQM; Kravaře; Kobeřice AS. Window 13:40–15:40.
- (b) Opava 12:45, **14:20, 14:50**, 15:45, 16:25, 17:25, 18:25 (hourly :25 outside the peak); Kobeřice 12:15, **13:45,
  14:45**, 16:45, 19:45 (hourly :45). The Opava – Štěpánkovice shorts (13:45, 14:45 out, 14:22, 15:22 back) stop short of
  Kobeřice. At Kobeřice 252's buses go on as 255 and come back from it (22-1050, 22-0003).
- (c) Published hourly: Opava 2 / 2 filled 0 (14:25 is 5 min off, 15:25 empty), FAIL; Kobeřice passes. No hourly phase
  passes out of Opava. Every 120 with two slots each way: 2 / 2 filled both, 2 + 8 exact, need 3. Every 120 with one slot
  (14:50 / 13:45) passes too but halves the line.
- (d) **252** every 120. Opava Offset 79 (14:20), Also at 109 (14:50); Kobeřice Offset 44 (13:45), Also at 104 (14:45)
  (the same as every 60 at :45, Offset 44).
- (e) Kravaře and Kobeřice 6–7 off (the model takes the commonest path's running time); back exact at Opava for 14:45.
- (f) Off: Opava 12:45, 15:45, 16:25, 17:25, 18:25; Kobeřice 12:15.
- (g) Need 2 → 3 (waits Opava 28, 58; Kobeřice 98, 8). Owner check: the earlier hourly row, 2 buses, approximate.

**262 Opava – Hradec – Skřipov – Bílovec**
- (a) Opava TQM; Hradec žst; Bílovec žst. Window 13:50–15:50.
- (b) Opava 12:21, **14:15, 14:43**, 16:38, 18:43 (about every 80); Bílovec 12:20, **14:45, 15:45**, 17:25, 18:40.
- (c) Published every 90 (14:13 / 14:10): 2 / 2 filled 1 and 2 / 2 filled 0, FAIL. Every 120 with two slots each way: all
  filled, 3 + 2 exact, need 3. Every 80 with one slot (14:43 / 14:45): passes, 2 + 2 exact, need 2.
- (d) **262** every 120. Opava Offset 74 (14:15), Also at 102 (14:43); Bílovec Offset 44 (15:45), Also at 104 (14:45) (the
  same as every 60 at :45, Offset 44). Out via Slatina as before.
- (e) Hradec within 2, Bílovec 0 / 6; back within 2.
- (f) Off: Opava 12:21, 16:38; Bílovec 12:20, 17:25, 18:40.
- (g) Need 2 → 3 (waits Opava 1, 33; Bílovec 28, 60). Owner check: every 80, 2 buses. 262 Skřipov unchanged.

**263 Opava – Hrabyně – Pustá Polom – Těškovice**
- (a) Opava TQM; Pustá Polom AS (the knot: most trips turn there; the way back is read there); Těškovice. Window
  15:30–17:30.
- (b) Opava 12:14, **15:31, 16:59**, 18:38, 19:46; back at Pustá Polom 15:27 (from Hlubočec), **16:12**, 17:54.
- Plates: 22-0101 out 15:31, back 16:12; 22-1008 out 16:59 ends at Pustá Polom; the morning trips start there (4:38, 6:00,
  7:00): the buses sleep at Pustá Polom.
- (c) Published every 120 (16:38 / 17:13): both 0 of 1, FAIL. Inbound rate, every 120: Opava 15:31 (or 16:59) with
  Těškovice 15:58: both pass, 1 / 2 and 1 / 1 filled, 1 + 1 exact, need 2. 16:59 is the bus going home, so 15:31 stays.
- (d) **263** every 120. Opava Offset 30 (15:31); Těškovice Offset 57 (15:58), so the bus passes Pustá Polom at 16:12.
- (e) Pustá Polom 16:12 exact. The card's knot check compares with whole Opava – Těškovice trips (few in the afternoon:
  18:38 out, 17:40 back), so it shows 94–190 there.
- (f) Off: Opava 16:59, 18:38, 19:46; Těškovice 17:40; the Budišovice and Hlubočec trips.
- (g) Need 2 (waits Opava 34, Těškovice 86).

**264 Opava – Hlubočec – Pustá Polom – Těškovice**
- (a) Opava TQM; Těškovice. Window 15:30–17:30.
- (b) Opava 14:21, 15:01, **16:44**; Těškovice 12:40, 13:30, **16:03**. 22-1011 runs 15:01 out / 16:03 back; 22-0106 runs
  16:44 out and goes on as 263 (Těškovice 17:40).
- (c) Published every 120 (16:21 / 17:29): both 0 of 1, FAIL. Every 120 (16:44 / 16:03): both 1 / 1 filled, 1 + 1 exact,
  need 2; every passing row needs 2 (Těškovice 16:03 leaves before the Opava bus arrives).
- (d) **264** every 120. Opava Offset 103 (16:44); Těškovice Offset 62 (16:03).
- (e) Těškovice 3, Opava exact.
- (f) Off: Opava 14:21, 15:01; Těškovice 12:40, 13:30.
- (g) Need 1 → 2 (waits 112, 23). Owner check: the earlier 1-bus row.

**270 Opava – Mokré Lazce – Ostrava, Svinov**
- (a) Opava TQM; Svinov nádraží. Window 15:30–17:30.
- (b) Opava 12:59, 15:19, **16:19**; Svinov 13:21, 14:21, **16:26**, 17:45.
- (c) Published every 90 (16:49 / 15:38, 17:08): 0 of 1 and 0 of 2, FAIL. Every 80 (16:19 / 16:26): 1 + 1 exact, 1 + 2
  within 1 (17:46 for 17:45), need 2; every 90 the same exact, 1 + 1 within 1, need 2.
- (d) **270** every 80. Opava Offset 38 (16:19); Svinov Offset 45 (16:26).
- (e) Svinov exact, Opava 2.
- (f) Off: Opava 12:59, 15:19; Svinov 13:21, 14:21.
- (g) Need 2 (waits 5, 23).

### Hlučínsko and Bohumín

**075 Hlučín, sídliště OKD – Ostrava, Poruba, Studentská**
- (a) Hlučín, sídliště OKD; Poruba, Studentská. Model hour 16:00 by hand (was 14:10).
- (b) Every 20 all day (Hlučín :12 / :32 / :52, Poruba :19 / :39 / :59) with extras at :02 / :22 until 14:02 and at
  Poruba :29 / :49 until 14:29, on the same path. They made 13:40–15:40 the busiest stretch: there Hlučín has 8 departures
  for 6 slots (FEWER).
- (c) The v4 rule for 282 (busiest hours are extras on the line's own stops): model hour 16:00. Every 20 there: 6 / 6
  filled 6 both ways, 25 + 24 exact.
- (d) **075** every 20, unchanged: Hlučín Offset 11 (:12), Poruba Offset 18 (:19); now hand-set (was `auto`).
- (e) Exact at both ends.
- (f) Off: the :02 / :22 extras (12:02, 13:02, 13:22, 13:42, 14:02) and Poruba 12:29, 13:49, 14:29.
- (g) Need 4 (unchanged).

**284 Hlučín – Kravaře – Štěpánkovice**
- (a) Hlučín AN; Štěpánkovice, Svoboda. Window 15:30–17:30.
- (b) Hlučín 14:45, 15:15, **16:15, 17:28**, 19:05; Štěpánkovice only **16:24** all afternoon (then 20:05). Plates:
  24-1005 out 15:15, back 16:24; 2TD2679 (16:15) and 24-1008 (14:45) end at Štěpánkovice; 24-1116 (17:28) goes on as 283.
- (c) Published every 120 (15:52 / 16:24): Hlučín 0 of 1, FAIL. Inbound rate, every 120 with Štěpánkovice 16:24: Hlučín
  17:28 passes, need 1; Hlučín 16:15 passes, need 2; every 90 with 16:15 / 16:24 passes (2 + 1 exact), need 2. By the
  waits (the 290 rule), 17:28.
- (d) **284** every 120. Hlučín Offset 27 (17:28); Štěpánkovice Offset 83 (16:24), unchanged.
- (e) Exact both ways.
- (f) Off: Hlučín 14:45, 15:15, 16:15, 19:05.
- (g) Need 1 (waits Hlučín 34, Štěpánkovice 27).

**285 Ostrava, Poruba, Dílny DP – Dobroslavice – Štítina**
- (a) Poruba, Dílny DP Ostrava; Dobroslavice; Štítina, škola. Window 13:00–15:00 by hand (`window`).
- (b) The Štítina trips run 13:03–15:50 only: Poruba **13:09, 14:09**, 15:09; Štítina **13:03, 13:48, 14:53**, 15:50, by
  two buses alternating (24-1112: 13:09 / 13:48, 15:09 / 15:50; 22-0005: 13:03, 14:09 / 14:53). The 16:00 model hour of
  the line came from the Dobroslavice short trips.
- (c) Published every 90 (16:11 / 16:48) in 15:30–17:30, where the trunk has no departures: 1 / 0 and 1 / 1, 0 filled,
  FAIL. In 13:00–15:00: every 120, Poruba 13:09 / 14:09 and Štítina 13:48 / 14:53: 2 / 2 and 2 / 3 filled, 3 + 2 exact,
  need 2; hourly :09 / :50 passes with 3 + 1, need 2.
- **285 Dobroslavice** (Poruba – Dobroslavice shorts) counted the Štítina trips past Dobroslavice (:09 → :21) as its own.
  With them taken out, its afternoon is out 15:49 (to Mokré Lazce), 16:49, 17:19 (to Háj) and back 17:01: no pattern
  passes, and all its stops are on 285 (Step 8: a variant whose stops another line serves is listed, not a line).
  Dropped; the shorts (hourly :09 / :41 at midday) are listed on the 285 card.
- (d) **285** every 120. Poruba Offset 8 (13:09), Also at 68 (14:09) (the same as every 60 at :09); Štítina Offset 47
  (13:48), Also at 112 (14:53).
- (e) Štítina 0 / 6, Dobroslavice exact; back Poruba within 3.
- (f) Off: Štítina 13:03; the shorts.
- (g) 285 1 → 2 (waits Poruba 39, 34; Štítina 8, 3), 285 Dobroslavice 1 → 0.

**293 Hlučín – Šilheřovice – Bohumín**
- (a) Hlučín AN; Bohumín, Nový Bohumín AS. Window 15:30–17:30.
- (b) Hlučín 13:05 (293 ŽD), 13:55, 15:10, **17:05**; Bohumín 14:19 (ŽD), 15:02, **16:22**, 18:17 (about every 95).
- (c) Published every 90 (16:55 / 16:11): both 0 of 1, FAIL. Every 120 (17:05 / 16:22) passes, 2 + 1 exact, but one of the
  two is 293 ŽD's 13:05: every 120 at odd hours :05 leaves Hlučín at 13:05 with 293 ŽD (check 6). Every 96 (17:05 /
  16:22): 1 + 1 exact, need 1, no shared minute, and the real headway is about 95.
- (d) **293** every 96. Hlučín Offset 4 (17:05); Bohumín Offset 57 (16:22).
- (e) Exact both ways.
- (f) Off: Hlučín 15:10; Bohumín 15:02, 18:17.
- (g) Need 1 (waits 2, 15). 293 ŽD unchanged.

**555 Bohumín, Starý Bohumín – Ostrava, Náměstí Republiky**
- (a) Starý Bohumín, nám. Svobody; Ostrava, Náměstí Republiky. Model hour 16:00 by hand (was 14:00).
- (b) From 15:00 Bohumín **:01 / :28** (15:01 – 17:28) and Ostrava **:20 / :50** (14:50 – 17:50); before that 13:08, 13:41,
  14:28 and 13:20, 14:00, 14:30. Two Nový Bohumín AS shorts (13:35, 14:03, stops on the line) made 13:30–15:30 the
  busiest; without them 15:00–17:00 ties it, so the v4 rule (as 282) sets 16:00.
- (c) Published every 30 at 14:00: 4 / 4 filled 3 and 2, FAIL. At 14:00 the passing rows are every 120 with three or four
  slots (exact there, but :28 / :01 / :41 every 2 h, wrong from 15:30 on). At 16:00: hourly with :01 / :28 and :20 / :50, 4 / 4 filled 4 both ways, 7 + 10 exact, need 4; every
  30 (:28 / :20) passes with 4 + 10.
- (d) **555** every 60. Bohumín Offset 0 (:01), Also at 27 (:28); Ostrava Offset 19 (:20), Also at 49 (:50) (that entry is
  every 30 at :20; the sheet prints the line's every 60).
- (e) Within 2 at both ends.
- (f) Off: Bohumín 13:08, 13:41, 18:15, 19:05; Ostrava 12:30, 14:00, 14:30, 19:10.
- (g) Need 4 (waits Bohumín 26, 29; Ostrava 10, 7).

### Failing legs left approximate

- **217** (both ways, hand-set hourly :04 / :25): the window's Koupaliště slots and Slavkov 15:25 have no trip because the
  early-afternoon trips run Divadlo – Slavkov; that is the open owner check. Not changed.
- **920** (four legs): the :17 pattern from Svinov holds 10:17–15:17; in the 16:00 window the Šumperk trip leaves at 16:47
  (not 16:17), there is no 17:17 Rýmařov trip, and the Šumperk 16:35 and Rýmařov 15:32 slots have no trip. This is the
  open 920 owner check (the split); no single minute is wrong within the chosen design. Not changed.
- **248** (Heřmanice → Opava): hourly with gaps, kept hourly (rule 5); owner check offers every 120 with 1 bus.
- **251** (Opava → Chlebičov): hourly, 7 of 9 on the minute, the 15:35 runs at 15:05; kept hourly (rule 5). Every 120
  (16:35 / 17:05) would pass with the same bus.
- **254** (both ways): out 14:38, 15:18, 16:28 and back 14:30 in the window (16:30 sits on its end), so no pattern passes
  both ways; the published every 90 is already the best phase (Opava 16:28, Chuchelná 14:30 / 17:30 exact, 16:28 → 17:30 is
  one bus, 22-1040). Kept, approximate; 14:58 and 16:00 slots have no trip. Not moved to the outstation every 120 (it
  would need 1 bus), because the 16:28 bus does come back at 17:30.
- **236** (Vítkov → Budišov) is FEWER by design (outstation), as 281 and 292.

### For the orchestrator

- **Fold:** four entries are evenly spaced on their line's interval and are every 30 / every 60 in the fork's terms: 555
  Ostrava (every 60 at :20 / :50 = every 30, Offset 19), 285 Poruba (every 120 at 13:09 / 14:09 = every 60, Offset 8), 252
  Kobeřice and 262 Bílovec (every 120 at 13:45 / 14:45 and 14:45 / 15:45 = every 60, Offset 44).
  `06_render` prints one every per line and does not fold; fork-schedule.md says to type the folded form.
- **Owner checks:** the sheet now has seven, and `06_render` writes their number as a word from a list that ends at
  "seven": an eighth would fail the render.
- **Roster:** 285 Dobroslavice no longer exists (its bus is free); 215, 233, 241, 252, 262, 264 and 285 need more buses
  (`keep_roster` keeps the published ones where they are still seen). 04_roster, 06_render and publishing were not run.
- **Pooling (not applied):** the Opava – Vítkov lines 240 / 241 / 242 share one pool at both ends (241 alone needs 4 buses
  for four trips run by four pool buses); 252 / 255 hand buses over at Kobeřice.
