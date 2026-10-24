# Bus schedule method, applied to the Hranečník ODIS lines (20 Oct 2026)

This is a dry run of `pipeline/bus-schedule-method.md`, steps 1–11, on the Ostrava sheet's ODIS cards. Nothing on the published sheet has changed yet.

- **Data:** JDF trips for Tue 20 Oct, 5:00–23:00. Scripts are in the session scratchpad: `odis_core.py`, `step4run.py`, `pneed.py`.
- **Typed values:** (real − 61) mod every, because every terminus is a loop.
- **Need:** each terminal's arrivals matched to its departures, at least 3 min apart, with the least total wait. Need = (running + waits) / period. On these lines it gives the same numbers as `pattern_need`.

## Summary

| Line(s) | Now | Method | Change |
|---|---|---|---|
| 383 | 2 | 2 | better offsets (out worst 21 → 5 min) |
| 387 | 1 | 2 | one-way line + empty return |
| 440 | 3 | 3 | (+1 if Kartonážka every 480 is wanted) |
| 441 + 442 | 8 | 11 | 442 :05/:10 run on as 441 :32/:47 (new circuit) |
| 531 | 4 | 4 | — |
| 534 + 535 | 9 | 6 | one corridor, every 30 at Hranečník |
| **Total** | **27** | **28** | |

## Per line

### 442 + 441 (one corridor: Hranečník – Havířov)

- **(a) Core points:** Hranečník; Havířov, Město, žel.st. (441 knot, where the Město variant turns); Havířov, Podlesí, aut. nádr.
- **(b) Variants (trips, whole day):**
  - 442 Hranečník → Podlesí, express via Magistrát: 35.
  - 442 Podlesí → Hranečník: 33, plus 2 from Těšínská (morning only).
  - 441 Hranečník → Podlesí: 30.
  - 441 Podlesí → Hranečník: 32.
  - 441 Hranečník → žel.st.: 9.
  - 441 nemocnice → Hranečník: 8.
  - 441 night trips via Náměstí Republiky: 13.
- **Afternoon repeating hour (14:00–17:30):**
  - Hranečník → Podlesí: 442 :05 :10 :20 :40 :50, 441 :30.
  - Podlesí → Hranečník: 442 :21 :36 :51, 441 :17 :32 :47.
  - Each line alone is unbalanced: 442 sends 5 an hour out and 3 back, 441 sends 1 out and 3 back. Together they balance, with 6 each way. So the 442 :05/:10 buses come back as the 441 :32/:47 (Step 3: "the same bus goes on as another line number"). The live-log plates (promised after 17:46) can confirm this.
- **(c) Simutrans lines:**
  - **442:** every 60, Hranečník 19, Also at 39, 49 (real :20 :40 :50); Podlesí 20, Also at 35, 50 (real :21 :36 :51).
  - **442/441 circuit:** every 60.
    - Hranečník 4, Also at 9 (real :05 :10), on the 442 path.
    - Podlesí 31, Also at 46 (real :32 :47), on the 441 path via Šumbark.
  - **441:** every 60, Hranečník 29 (:30) / Podlesí 16 (:17).
  - **441 Město:** every 60, Hranečník 59 (:00) / nemocnice 4 (:05). nemocnice is the loop end, aliased to žel.st.
- **(d) Knots:** every model time equals the real time.
  - Hranečník out: :00 :05 :10 :20 :30 :40 :50.
  - Podlesí out: :17 :21 :32 :36 :47 :51.
  - žel.st.:
    - 441 out passes at :51.
    - Circuit back passes at :44 and :59.
    - 441 back passes at :29.
    - Město out arrives :21; Město back passes :14.
- **(e) Off the pattern, 13–19:**
  - The evening every-30 on 441: out 18:00, back 18:02.
  - From 17:20 the 442 :05/:10/:40 trips stop.
  - The morning is a different pattern: every 15/30 both ways.
- **(f) Need:** 442 4, circuit 3, 441 2, Město 2, so 11 (now 8). The corridor as one pool would need 8 + 2 = 10.
- **(g) Not covered:** Podlesí, Těšínská has no afternoon trip.

### 534 + 535 (one corridor: Hranečník – Orlová – Karviná)

- **(a) Core points:** Hranečník; Orlová, Poruba, rest. Horník (shared); Orlová, Lutyně, aut. nádr. (535 only); Karviná, Fryštát, aut. nádr.
- **(b) Variants:**
  - 534 Hranečník → Karviná: 22 + 1.
  - 534 Karviná → Hranečník: 21.
  - 535 Karviná → Hranečník: 6 (35 stops) + 3 others.
  - 535 Hranečník → Lutyně AN: 5 + 1.
  - 535 Hranečník → Karviná: 2 (36 stops) + 3 others.
  - 535 Horník ↔ Karviná shuttles: 7 + 2 (morning/midday).
  - 535 Lutyně AN → Hranečník: 2 (morning).
- **Corridor:**
  - Leaving Hranečník it is every 30 at :25/:55 from 12:55 to 18:55, all 534 until 15:55; from 16:25 the :25 slot is 535.
  - Arriving at Hranečník it is every 30 at :03/:33 from 13:34 to 18:33, 534 and 535 alternating (plus 15:12, a 535 short trip).
  - Each line alone is unbalanced (534 sends 2 out an hour but brings 1 back); together they balance.
- **(c) Simutrans lines:**
  - **534:** every 60, Hranečník 54 (:55) / Fryštát 19 (:20).
  - **535:** every 60, Hranečník 24 (:25) / Fryštát 0 (:01).
- **(d) Knots:**
  - Horník:
    - Out: 534 :13, 535 :44 (real 16:13 / 16:44).
    - Back: 534 :13, 535 :44 (real 18:13 / 16:44).
  - Lutyně AN, 535: out :00, back :30 (real 17:00 / 16:30).
  - Hranečník arrivals: :33 / :04 (real).
  - Petřvald is shared with 531: at Hranečník 531 :10/:40 and 534/535 :25/:55, so they interleave every 15.
- **(e) Off the pattern:**
  - 534 out 13:25, 14:25, 15:25 (in 535's :25 slot) and 18:25.
  - 534 back 14:48 and 18:08.
  - 535 out 15:17 (24 stops, short path) and 17:25 / 18:55 (to Lutyně AN only).
  - 535 back 13:51 and 14:14.
- **(f) Need:** 3 + 3 = 6 (now 534 6 + 535 3 = 9).
- **(g) Not covered:** none. Lutyně AN, Karviná Doly Jánská and Nové Město Osvobození are on 535; Doubrava Špluchov and Doly Děl. dům are on 534.

### 531

- **(a) Core points:** Hranečník; Karviná, Nové Město, obch. dům (where the express rejoins); Karviná, Fryštát, aut. nádr.
- **(b) Variants:** normal 25 + 23; express 4 + 3; 3 early trips from Nové Město stadion.
- **(c) Simutrans lines:** as now. Two circuits alternate the paths, period 60:
  - Normal: Hranečník 9 (:10) / Fryštát 30 (:31).
  - Express: Hranečník 39 (:40) / Fryštát 0 (:01).
- **(d) Knot at obch. dům:**
  - Out: normal :37, express :02.
  - Back: express :19, normal :49, so every 30.
  - All exact.
- **(e) Off the pattern:** none 13–19. Before 15:40 the :40 slot is a normal trip.
- **(f) Need:** 4 (unchanged).
- **(g) Not covered:** none.

### 440

- **(a) Core points:** Hranečník; Šenov, křižovatka (where the paths join); Havířov, Šumbark, točna 2.etapa; Vratimov, Kartonážka.
- **(b) Variants:**
  - Main (15 stops, via Radvanice škola): 13 + 15.
  - Via Šenov náměstí (19 stops): 9 + 7.
  - Kartonážka: 3 + 3, exactly every 480 (2.etapa 5:05/13:05/21:05, Kartonážka 6:15/14:15/22:15).
- **(c) Simutrans lines:**
  - **440:** every 30, Hranečník 12 (:13/:43) / 2.etapa 26 (:27/:57).
  - **Option:** 440 Kartonážka every 480, 2.etapa 244 (13:05) / Kartonážka 314 (14:15), 1 bus. Its stop is on DPO 41, so I list it instead.
- **(d) Knot at Šenov křižovatka:** out :22/:52 (real 15:22…), back :43/:13 (real).
- **(e) Off the pattern:**
  - Out 13:48 and 14:28 (19-stop path), 18:18, 18:58.
  - Back 13:17 and 16:47 (19-stop path, 10 min before its slot).
  - 14:13 and 17:43 sit on the :13/:43 slots by the other path.
- **(f) Need:** 3 (unchanged).
- **(g) Not covered:** none. The 19-stop path's stops are on 383; Kartonážka is on DPO 41.

### 383

- **(a) Core points:** Hranečník; Šenov, Škrbeň (where the paths split); Havířov, Dolní Datyně, rozcestí Bludovice (where they rejoin; the long path passes it twice); Kaňovice, rest. U Magerů (short turn); Řepiště, u kříže.
- **(b) Variants:**
  - Long path via Havířov Bludovice: 5 + 7.
  - Lapačka path: 4 + 4.
  - Kaňovice short turns: 2.
  - Trips starting in Sedliště: 2.
- **No repeating interval over the whole day.**
  - The afternoon out trips 14:13 / 15:28 / 16:43 are exactly 75 apart, but 75 does not divide 1440.
  - Every 72 does divide 1440 (worst 3 out / 9 back) but isn't on the method's list.
- **(c) Simutrans lines:**
  - **383:** every 72 (method v2 allows every divisor of 1440).
    - Hranečník 3 (real 15:28; slots 14:16, 15:28, 16:40, worst 3).
    - Řepiště 19 (real 14:32; slots 14:32, 15:44, 16:56, worst 9).
    - Round 144, so 2 buses.
  - The every-80 alternative: Hranečník 67 / Řepiště 6, worst 5 out / 20 back.
  - Now it is out :34-slot, 21 min off.
- **(d) Knots:** exact on the 15:28 out / 15:47 back trips (Škrbeň 15:43, rozcestí Bludovice 15:51, Kaňovice 16:05). Elsewhere up to 5 min off out and up to 20 min off back (16:47 against the 17:07 slot).
- **(e) Off the pattern:**
  - Out 13:33, 14:13 (+5), 16:43 (−5), 18:33 (Kaňovice).
  - Back 12:32, 13:12, 14:32 (+5), 16:47 (−20), 18:17.
  - The line goes on the To check list.
- **(f) Need:** 2.
- **(g) Not covered:** none.

### 387

- **(a) Core points:** Hranečník; Kaňovice, U Magerů; Lučina, přehrada; Soběšovice, Na husarůvce.
- **(b) Variants:**
  - Hranečník → Soběšovice: 5.
  - Soběšovice → Hranečník: 4 (morning/midday).
  - Lučina → Hranečník: 1.
  - Evening Kaňovice → Lučina: 2; Lučina → Sedliště: 1.
- **In the afternoon it only runs out:** 14:45 and 15:45, with nothing back.
- **(c) Simutrans lines:** **387**, every 60, Hranečník 44 (:45); the return to Hranečník is empty and untimed (Step 6).
- **(d) Knots:** Kaňovice :07, Lučina :28 (real).
- **(e) Off the pattern:** the evening trips 19:07, 20:22, 23:07.
- **(f) Need:** 2. A 49 min trip out plus an empty return of about 45 min is about a 120 min round. The sheet shows 1 now ("turns at 16:00").
- **(g) Not covered:** none.

## Where the write-up needed judgement

- **Step 2:**
  - It doesn't say what counts as a knot when a loop end has two stop names (441 žel.st. / nemocnice).
  - Nor when a path passes the same stop twice (383 rozcestí Bludovice).
- **Step 3:** it doesn't say how to read trips that never touch the main hub (535 Horník ↔ Karviná shuttles).
- **Step 4:**
  - It says to choose the minutes for each interval, but not how to choose between intervals. Every 15 always wins on exact hits and leaves empty slots.
  - It doesn't say how many slots to try.
  - The interval list leaves out other divisors of 1440 (72, 48, 36, 45, 96, 144, 160, 180, 288, 360). 72 fits 383 best.
- **Step 5:**
  - It covers destination variants only. 442 :05/:10 go to the same destination but come back as another line (441).
  - It doesn't say to pair the surpluses and deficits of two lines at a shared terminal into one circuit. That pairing is what found 442→441 and 534/535.
- **Step 6:** the knot check is undefined for an approximate line (383): which slot do you compare against which real trip?
- **Step 7:**
  - It checks each line on its own. Two lines can each be unbalanced and still balance together (441/442, 534/535). The method should say to check the sum at shared terminals first.
- **Step 8:** for 440 Kartonážka it doesn't say whether to give the line every 480 (1 bus) or just list it when the stop is already on another line.
- **Steps 4/5 (model hour):**
  - Step 1 reads the whole day, but it doesn't say which hour the repeating Simutrans pattern should be.
  - 442 is hourly at midday and 5 an hour in the afternoon.
  - 534/535's :25 slot is 534 until 15:25 and 535 from 16:25.
  - I used the afternoon peak hour (the sheet's anchor).
- **Step 10:**
  - Empty returns: the wait at the far end isn't specified. I used 3 min before the untimed leg.
  - The "at least 3 min" rule versus the real turnaround is unclear where the real one is shorter (442 Hranečník :03 → :05).

## Update, 20 Oct 2026 evening: 442/441 settled with the plates

Plate chains from session a4 (ODIS live map, 14:00–17:50): :05 → 441 :31 (14:04, 16:04) or :46 (15:04); :40 → 441 :16
(14:39, 15:39); :50 → 441 :31 (14:49); :10 → 443 (14:09), the others unknown; :20 stays on 442. The circuit 442/441 is now
:05 → :32 and :40 → :17 (was :05/:10 → :32/:47); 442 keeps :10 :20 :50 out, 441's own bus :30 out, :47 back.
441 + 442 need 10 buses (was 11). Real 441 departures from Podlesí in 15:30–17:30 are 15:32 15:47 16:17 16:32, so one :17
and one :47 slot stay off a real departure either way.
