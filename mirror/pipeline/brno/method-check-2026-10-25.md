# City sheets: row-by-row method check (25 Oct 2026)

Sheets: Brno Tram Fleet from 29 Sep (`brno`, state from-2026-09-29), Brno Bus Peak Fleet (`brno-bus`), Brno Trolleybus Peak Fleet
(`brno-trolleybus`), Plzeň Tram Peak Fleet (`plzen`, 2026-09-27), Plzeň Trolleybus Peak Fleet (`plzen-trolleybus`), Plzeň Bus Peak Fleet
(`plzen-bus`, scripts of plzen-trolleybus with `--base`), Pardubice MHD Peak Sheet (`pardubice`). Built on top of today's offset-origin fix
(`pipeline/audit/city-changes-2026-10-25.md`), which is unchanged.

Owner's request: "verify all sheets with this level of detail … that's the point of you doing it, so you'll not produce incorrect results".

## 1. What was checked, and how

Every Simutrans row (Brno tram 26, Brno trolleybus 36, Brno bus 90, Plzeň tram 8, Plzeň trolleybus 26, Plzeň bus 47, Pardubice 69) was
re-read against the real departures of its entry for the whole afternoon (13:00–20:00), taken from the same GTFS / JDF data and filters
the pipeline uses (depot runs out, minute subsets and aliases as in the state, Pardubice merged minutes as in network.json). Per row:

- **Typed values**: every value = (real − 60 − 1) mod every at turns/loops (all entries on these sheets except Brno tram Mifkova and
  Nemocnice Bohunice, which keep real − 60). Checked from each value, never by zipping lists.
- **Exact stretch**: the longest contiguous stretch where the pattern's slots and the real departures coincide minute for minute; flagged
  when it has fewer than 2 departures, or when a multi-slot pattern is exact for less than one interval (a "one-cycle" fit: any 8
  departures inside 48 min are trivially "exact" every 48 with 8 slots).
- **Peak**: the line's own busiest 2 h in 13:00–18:00, or 15:00–17:00 when that is within one departure of it (kb city-fleet-sheets);
  departures of that window outside the exact stretch were listed.
- **Better pattern**: every interval dividing 1440 up to 60 (and 72–120), ≤ 8 slots, at the line's rate and at every other rate, ranked
  by how much of the peak window its exact stretch covers; the pattern's bus need (follow a bus round the slots, real running times,
  3-min layover) compared with the sheet's need.
- **Same rate at both ends** of every Simutrans line (all legs of a circuit), folding, ≤ 8 slots, offset < interval.
- Approximate rows: largest deviation, and whether an exact or simpler pattern was missed.

Rule for changing a row (owner's rules; the sheets are already in the game, so as few moves as possible):
change it when it breaks a hard rule (rate, < 2 departures, one-cycle fit, missed exact pattern behind an approximate label) **and** a
better pattern exists that needs **the same vehicles**. Where the better pattern costs vehicles, the row is kept and the option is listed
for the owner (section 5). No vehicle was moved: every rebuilt sheet's `fleet.json` has the same content as before.

## 2. Findings by sheet

### Brno Tram Fleet from 29 Sep — no change
- All 26 rows exact, typed values right, both ends at one rate.
- 1, 4, 6, 9 run every 5 until about 16:30 (exact for 1.5–2 h ending 16:20–16:40), then every 6–7: the departures "outside the
  run" are the after-peak form. 5/5S, 7, 10, 2, 3 exact for 1.5–5 h.
- 8 Bohunice → Mifkova: exact 14:47–16:37 except the 15:50 short trip that runs through to Mifkova (state `skip`, said on the sheet);
  8S stops at 16:30 (peak reinforcement).
- 12 every 14 (3 slots, 5-5-4 cycle): exact 14:41–16:24 and 14:55–16:29; values from the 01:00 origin (today's fix) verified.

### Brno Trolleybus Peak Fleet — 1 entry changed
- All 36 rows exact over 1–5 h, one rate per line (circuits 25 + 26 and 35 + 38 + 39 included).
- **37N Mendlovo náměstí → Nemocnice Bohunice** (bunching at a shared terminus): the row was the branch's irregular pre-16:33
  minutes (every 60, :07 :20 :33 :53, exact 15:20–16:33) while 37J is in its post-16:41 form (every 15 :11), so in the game the two
  branches left Mendlovo náměstí 3–4 min apart (:07/:11, :53/:56) with a 12-min gap. After 16:33 37 alternates N :03 :18 :33 :48 /
  J :11 :26 :41 :56. Changed to every 15 :03 (exact 16:48–18:03), the same rate as its Bohunice end (every 15, exact 14:35–17:05).
  Need 4 (unchanged).
- 33 Slatina → Hlavní nádraží: real :05/:18/:25/:38/:45/:58 is exact every 20 [5, 18]; the :12 slot is the documented designed return
  (`designed_slots`, 9 out against 6 back).
- 34, 36, 37J change frequency inside the peak (README): their rows are the post-16:00 form (34 exact 16:00–18:00, 36 15:59–17:40,
  37J 15:53–18:11 / 16:41–18:11). Their earlier forms are irregular (5 departures an hour with gaps; 34 every 10 with 15:08 and 15:20
  missing). 34's every-10 form would need the same 4 trolleybuses but is exact only 15:18–16:18 / 15:30–16:00 — listed in section 5.

### Plzeň Tram Peak Fleet — no change
- 1 and 2 every 5 in their 5-min peak (1 exact 13:41–16:21; 2 exact one hour each end, the minute drifts by 1 at 15:16/15:22 and
  15:43/15:49 — one drifting departure, same pattern).
- 4 (one line, Košutka twice, every 8): exact 16:04–17:44 from Košutka, 16:48–17:50 from Bory/Univerzita. Before 16:00 (and at the far
  ends until about 16:45) the two branches run an irregular 3/6/9 pattern; no repeating pattern (any interval ≤ 60, ≤ 8 slots) is exact
  there. Documented state decision (core 16:00–17:30); kept.

### Brno Bus Peak Fleet — 3 lines changed
| Line | Finding | Change |
|---|---|---|
| 48 Úzká – Prace, točna | Úzká row approximate (every 60, :43 "not modelled"). The line runs every 30 at both core points all afternoon: Úzká :13/:43 13:13–18:13, Prace, točna :04/:34 13:34–18:34; every other hour the :43 / :34 trip starts or ends two stops further at Prace, Mohyla míru (GTFS: leaves Prace, točna 14:34, 16:34, 18:34; Úzká 15:43, 17:43 runs on). | Both ends every 30, exact. New override field `passing` counts those departures for the match. Need 3 (unchanged; `period: 60` lets the cycle close past the 17:43 extension trip, otherwise the 30-min wait guard drops the need). |
| 72L Poliklinika Lesná – Technologický park | Rate 3 voted from the 16:00 hour (Technologický park 3 departures because 16:48 runs to Královo Pole). The Lesná section runs 4 an hour all afternoon: Lesná :15/:25/:45/:55 exact 13:45–16:55 (14 departures), Technologický park :08/:18/:38/:48 exact 14:08–16:38 (13). | Rate 4, every 30 [15, 25] / [8, 18]. Need 4 (unchanged). The 16:48 slot is the bus that goes to Královo Pole in reality (note on the sheet). With 72S (:28/:58) Technologický park now runs every 10. |
| 75 Tomkovo náměstí – Slatina, nádraží | Slatina row approximate (16:14 = tail of the every-15 form). Its peak form is every 15: Tomkovo :01 exact 14:16–15:46, Slatina :14 exact 14:29–16:29; it needs 4 buses, the sheet's need (3 + 1 on the road). | Both ends every 15. Need 4 (unchanged). |

Checked and kept: 47, 49P, 77L run every 15 / every 30 in 13:30–16:00 and thin out at 16:00 — their peak form costs one bus each
(section 5). 77L Letiště stays approximate (Letiště 2 an hour against Úzká 1 from 16:08). 77A, E50, E75 (one-way peak lines) exact
2–4 h. All other rows: no exact pattern at the same rate covers more of the line's peak.

### Plzeň Trolleybus Peak Fleet — 2 lines changed
| Line | Finding | Change |
|---|---|---|
| 12 Nová Hospoda – Božkov (8 an hour) | Rows were every 60 with 8 slots and every 45 with 6 slots: "exact" only for one cycle (16:30–17:22, 15:59–16:44), ±4 min. The real headway thins steadily from 5 to 8 min, so nothing repeats exactly. | Every 15 with two slots 7–8 min apart: Nová Hospoda :00 :08, Božkov :00 :07; ±2 min in the 16:00 hour, ±3 over 15:30–17:00 (better than before, 2 values instead of 8). Need 10 (unchanged). |
| 16 Sídliště Bory → Doubravka (10 an hour) | Every 48 with 8 slots, exact for one 48-min cycle only (the row type the owner rejected on Ostrava: "why is this not just…"). | Every 6, real :00 mod 6 (±2 in the 16:00 hour, ±3 over 15:30–17:00), the same form as the Doubravka end. Need 12 (unchanged). |

Checked and kept: 10 (Tylova every 12 combined, the two branches alternate exactly 15:20–16:32; the far ends shift by half an interval
at 16:00 — approximate ±12, as labelled); 11, 14, 18, 49 exact; 13 Na Dlouhých exact 14:05–16:29 (16:41 slot is the short trip to
Černice); 15 Borská pole drops the :07 bus that continues as 15N (correct); 15N, 22 Koterov irregular Škoda-shift trips (approximate,
labelled). 15 at 5 an hour (+1 trolleybus) and 14 at 2 an hour (+2) would cost vehicles (section 5).

### Plzeň Bus Peak Fleet — 6 lines changed
| Line | Finding | Change |
|---|---|---|
| 26 Bory – Lhota | **RATE**: Bory 1 an hour (:30) against Lhota 2 (:04 :54). Real: 2 an hour Bory :20/:40, Lhota :04/:44 until the 16:04 return, then hourly; the 16:30 bus turns at Lhota for 16:54 (and 17:40 → 18:04). | Both ends hourly: Lhota :54 (the 16:30 bus's turn). 16:04 not modelled. Need 1 (unchanged). Option: half-hourly form (+1 bus), section 5. |
| 25 Bory – Bolevec | Bolevec :15 was a single departure (the return of 15:37, earlier form). | Bolevec :00, the turn of the hourly Bory :07 trips (16:07 → 17:00, 17:07 → 18:00); exact 17:00–18:00. Need 3. |
| 29 Borská pole – Doubravka | Rate 3 from the 16:00 hour; Doubravka approximate ±14. The line runs every 15 at both ends (Borská pole :04 exact 14:49–16:19, Doubravka :04 exact 15:49–16:49, 15:03–15:33 one min early). Its pattern needs 6 buses = the sheet's need. | Both ends every 15 :04. Need 6. |
| 33, 40 (33 + 40 loop, both directions) | Rows were the 16:xx minutes as every 60 with 3–4 uneven slots, exact for under one hour. The loop runs every 15 both ways until about 16:30: 33 Hlavní nádraží :11 (14:26–16:26), 40 Sídliště Košutka :10 (15:10–16:40), 40 Hlavní nádraží :04 (14:34–16:34), 33 Sídliště Košutka :02 (15:02–16:32). Pattern need 4 each = the sheet's need. | All four entries every 15 (33 rate 4). Need 4 + 4. Hlavní nádraží and Košutka now alternate 33/40 every 7–8 min, as in reality. |
| 38 Doubravka – Červený Hrádek | Červený Hrádek :08 was a single departure. A 6-min run: one bus does every 30 (or every 15). | Every 30 both ends (Doubravka :00, Červený Hrádek :08, exact 15:00–16:08). Need 1. |

Checked and kept: 21 Litice (every 60 :05/:20/:40 is the 16:00 hour; every 20 :00 would be exact 16:20–18:00 but matches fewer peak
departures — marginal, left); 24 Bolevec (irregular, approximate); 32, 41, 41K approximate (irregular; no exact pattern at their rate);
51, 31, 35, 39, 20, 27, 28, 30, 26N exact; 42 consistent with 26 (Bory :00 26N, :15/:45 42, :30 26 = every 15, as after 16:00).
Many rows reproduce only the 16:00 hour because these lines thin out at 16:00 (21, 24, 25, 26/42, 30P, 34, 41K): section 5.

A rebuild of either Plzeň sheet also rewrites one sentence in the pak table: it lists the local pak checkouts it read, and the
`-mhd` and `-pidops` checkouts no longer exist on this machine. No object status changes (all still "requested").

### Pardubice MHD Peak Sheet — 17 lines changed (`fit_overrides`, new)
city_systemic does not read Pardubice; checked here from network.json. Before: **16 Simutrans lines broke "both ends at one rate"** —
2 (5 vs 3 an hour), 2P (1 vs 3), 3 (4 vs 3), 6 (4 vs 2), 9 (2 vs 1), 9S (1 vs 2), 10 (2 vs 1), 11 (3 vs 2), 12M (2 vs 1), 13 (6 vs 5),
14 (1.5 vs 2), 17 (1 vs 2), 30 (3 vs 2), and the daily 23, 24, 25 — and many rows were the 16:xx minutes repeated hourly (every 60 with
up to 6 slots for every-10 lines), exact for under an hour, some for a single departure. Causes: the 16:00-hour fallback, minutes of
other patterns merged into one end only, and no pair step. After: every non-daily line at one rate (checked), every typed value
(real − 61) mod every, no fold, ≤ 8 slots. Vehicles and needs unchanged (`cycle_need_peak` sizes from the real trips). Every changed
line was also sized from its new pattern (follow a bus round the slots, real running times, the stop's own turnaround up to 3 min):
none needs more vehicles than the sheet gives it; 2, 3, 5, 10, 11 and 30 would need fewer (the sheet keeps the real-trip numbers).

- Exact patterns missed: **13** every 10 both ends (exact 14:07–16:47 / 14:08–16:38; the hour fit failed on 16:59 vs 16:57),
  **5** Dubina every 10 (14:01–16:41), **1** Jesničánky :06/:30/:54 (14:30–16:30, was :58), **8** Dubinská every 30 :11 (14:41–16:11).
- Merged minutes on one end only: **3** Hlavní nádraží :12/:27/:42 (own trips, 3 an hour like the return; the U Mlýnů :57 trips not
  modelled), **10** Hlavní nádraží hourly :22 (Nemošice/park :52 not modelled), **11** Dubina every 30 :15 (Rybitví trips and 16:35
  not), **30** Hlavní nádraží every 30 :25 (3 Ohrazenice trips not).
- Transition hour (the 16:00 hour is where the peak form ends): **2 + 2P** in their peak form, exact 14:33–16:24 — 2 every 30
  (Polabiny :13, Zámeček :12), 2P 4 an hour (Polabiny :03 :23 :33 :53, Pardubičky :04 :24 :34 :54); together every 10 from Polabiny
  as in reality. **6 + 6H** every 20 (6 Vápenka :00, Rosice :16; 6H Vápenka :10; exact 14:10–16:20), together every 10 from
  Vápenka. 6H Hlavní nádraží is set at :18, 2 min after the real :16 :36 :56: at the real minute the pattern needs 4 buses, at :18
  the bus from Vápenka (arriving :35) leaves at once and 3 do it, the sheet's need.
- Irregular lines, one even pattern at the rate the need allows, set at a real bus turn, labelled approximate with the largest
  deviation (15:00–18:00): **9** hourly Hlavní nádraží :23 / Hůrka :48 (±29; every 30 would need a 2nd bus), **9S** hourly :01 / Spojil
  :22 (±22), **12M** hourly :51 / Mnětice :22 (±22; :51 is 1 min after the real 15:50 so one bus closes the 60-min round), **14** every 30 Polabiny :16 / Staré Čívice :10 (±7; slower option every 40, ±19),
  **17** every 30 :15 / Srch :13 (±13; within 3 min 15:13–16:46).
- Kept: 4, 7, 18, 33, 30C, 1D, 21, 27, 20 (exact); 12, 15, 28, 8S, 88 (16:00-hour rows, rates equal, irregular timetables).
- The sheet's method text said "Offset counts from midnight"; corrected to 01:00 (also on both Plzeň sheets).
- Bunching scan at shared termini (all sheets): every pair of lines the model sends from one stop within 2 min also leaves that close in
  the real 15:00–17:00 timetable, except Pardubice Hlavní nádraží 17 (:45, approximate) and 15 (:45) — different routes, so left.

## 3. The Pardubice question for the owner (rows NOT changed)

Lines 16, 22, 23, 24, 25 (and the airport line 90) are every-1440 rows with each departure of the day as Offset + Also at. That breaks
"no 1440 on bus sheets", and 23, 24, 25 also fail "both ends at one rate" as typed (5 vs 4, 8 vs 6, 3 vs 8 departures a day — buses
pile up at one end). Pardubice is a city network, but these are its thin outer and shift lines. **Which method should Pardubice use?**

| | Option A — small-town method: bend onto a repeating ≤ 480 pattern | Option B — big-city method: list, don't model |
|---|---|---|
| 16 Hlavní nádraží – Dříteč (6 + 6 trips) | every 480, the afternoon trips exact: Hlavní nádraží 12:00 14:04 17:10 19:25 (Offset 9, Also at 144, 179, 303), Dříteč 12:30 14:37 17:40 19:53 (Offset 39, Also at 172, 209, 336); 12 a day each way, the morning 5:55/8:29 bent to 6:04/9:10 (+9/+41). 1 bus (116). | not modelled: −1 bus (116); its 8 stops lose service (Staré Hradiště, Psinek; Staré Hradiště, Brozany; Ráby, křižovatka; Ráby, prodejna; Ráby, Kunětická hora; Němčice, chaloupky; Němčice, rybníček; Dříteč) |
| 22 Závodu míru – Nemošice | runs hourly 13:24–16:50: every 60, Závodu míru :24 (Offset 23), Nemošice :50 (Offset 49), exact 4 trips each way; the 6:11/7:10 morning trips not modelled. 1 bus (113). Recommended under either option. | same as A (an ordinary hourly afternoon line) |
| 23 Staré Čívice – Hlavní nádraží (shift line) | every 480: Staré Čívice 14:14 17:20 (Offset 19, Also at 313), Hlavní nádraží 13:28 17:55 (Offset 54, Also at 267); 6 a day each way, mornings bent (5:30 +44, 5:55 −27). 1 bus (67). The 12 Polabiny – Staré Čívice trips are not on it either way. | not modelled: −1 bus (67); no stop served only by 23 |
| 24 Čepí, prodejna – Hlavní nádraží | every 480: Čepí 14:57 15:47 16:53 (Offset 356, Also at 406, 472), Hlavní nádraží 14:30 15:20 16:25 (Offset 329, Also at 379, 444); 9 a day each way, early/late trips bent up to 2 h (4:56). 1 bus (68). The Starý Mateřov trips are not on it either way. | not modelled: −1 bus (68); 3 stops lose service (Čepí, prodejna; Starý Mateřov, točna; Starý Mateřov, náves) |
| 25 Dubina, sever – Staré Čívice (shift line, 8 out / 3 back) | every 480: Staré Čívice 14:15 15:38 (Offset 314, Also at 397), Dubina 13:00 13:35 (Offset 239, Also at 274); 6 a day each way, the 5 morning shift trips bent to 5:00/5:35 (up to 95 min). 1 bus (188). | not modelled: −1 bus (188); no stop served only by 25 |
| 90 airport (flight times) | every 1440 was asked for by the owner (flight-bound); no ≤ 480 pattern fits 8:50/9:20 and 19:20/19:50. Keep as the one exception? | same |

Option A keeps every stop and bus but runs about twice the real trips a day on 16, 23, 24, 25 (each bus shuttles all day in the game).
Option B is the rule for big cities (Ostrava, Prague, Brno, Plzeň): 4 Simutrans lines and 4 buses fewer, and 11 village stops
(16, 24) without service on the sheet.

## 4. In-game changes (typed values; real minutes = value + 61 mod every, all entries are turns)

Brno trolleybus
- 37N Mendlovo náměstí → Nemocnice Bohunice: every 60, Offset 6, Also at 19, 32, 52 → **every 15, Offset 2** (real :03 :18 :33 :48).

Brno bus
- 48 Úzká → Prace, točna: every 60, Offset 12 → **every 30**, Offset 12 (real :13 :43). Prace, točna → Úzká: every 60, Offset 3 →
  **every 30**, Offset 3 (real :04 :34).
- 72L Poliklinika Lesná: every 60, Offset 24, Also at 44, 54 → **every 30, Offset 14, Also at 24** (real :15 :25 :45 :55).
  Technologický park → Lesná: every 60, Offset 7, Also at 17, 37 → **every 30, Offset 7, Also at 17** (real :08 :18 :38 :48).
- 75 Tomkovo náměstí: every 30, Offset 15 → **every 15, Offset 0** (real :01 :16 :31 :46). Slatina, nádraží: every 30, Offset 28 →
  **every 15, Offset 13** (real :14 :29 :44 :59).

Plzeň trolleybus
- 12 Nová Hospoda: every 60, Offset 5, Also at 13, 21, 29, 36, 43, 50, 57 → **every 15, Offset 14, Also at 7** (real :00 :08 :15 :23 …).
  Božkov: every 45, Offset 35, Also at 43, 5, 12, 19, 27 → **every 15, Offset 14, Also at 6** (real :00 :07 :15 :22 …).
- 16 Sídliště Bory → Doubravka: every 48, Offset 41, Also at 0, 5, 11, 16, 22, 28, 34 → **every 6, Offset 5** (real :00 :06 :12 …).

Plzeň bus
- 25 Bolevec → Bory: every 60, Offset 14 → Offset **59** (real :00).
- 26 Lhota → Bory: every 60, Offset 3, Also at 53 → Offset **53**, no Also at (real :54).
- 29 Borská pole: every 60, Offset 3, Also at 18, 32 → **every 15, Offset 3** (real :04 :19 :34 :49). Doubravka: every 60, Offset 2,
  Also at 17, 47 → **every 15, Offset 3** (real :04 …).
- 33 Hlavní nádraží: every 60, Offset 10, Also at 25, 43 → **every 15, Offset 10** (real :11 :26 :41 :56); Sídliště Košutka (as 40):
  every 60, Offset 9, Also at 24, 39 → **every 15, Offset 9** (real :10 :25 :40 :55).
- 40 Hlavní nádraží: every 60, Offset 3, Also at 18, 33, 53 → **every 15, Offset 3** (real :04 :19 :34 :49); Sídliště Košutka (as 33):
  every 60, Offset 1, Also at 16, 31, 49 → **every 15, Offset 1** (real :02 :17 :32 :47).
- 38 Doubravka: every 60, Offset 59 → **every 30, Offset 29** (real :00 :30). Červený Hrádek: every 60, Offset 7 → **every 30**,
  Offset 7 (real :08 :38).

Pardubice
- 1 Jesničánky → Slovany: every 60, Offset 5, Also at 29, 57 → Also at 29, **53** (real :06 :30 :54).
- 2 Polabiny → Zámeček: every 60, Offset 2, Also at 22, 32, 42, 57 → **every 30, Offset 12** (real :13 :43). Zámeček: every 60,
  Offset 11, Also at 31, 56 → **every 30, Offset 11** (real :12 :42).
- 2P Polabiny → Pardubičky: every 60, Offset 12 → **every 30, Offset 2, Also at 22** (real :03 :23 :33 :53). Pardubičky: every 60,
  Offset 3, Also at 23, 43 → **every 30, Offset 3, Also at 23** (real :04 :24 :34 :54).
- 3 Hlavní nádraží → Lázně Bohdaneč: every 15, Offset 11 → **every 60, Offset 11, Also at 26, 41** (real :12 :27 :42).
- 5 Dubina → Dukla: every 60, Offset 0, Also at 10, 20, 30, 40, 51 → **every 10, Offset 0** (real :01 :11 …).
- 6 Vápenka → Rosice: every 60, Offset 19, Also at 29, 56, 59 → **every 20, Offset 19** (real :00 :20 :40). Rosice: every 60, Offset 15,
  Also at 42 → **every 20, Offset 15** (real :16 :36 :56).
- 6H Vápenka → Hlavní nádraží: every 60, Offset 9, Also at 41 → **every 20, Offset 9** (real :10 :30 :50). Hlavní nádraží → Vápenka:
  every 60, Offset 15, Also at 37 → **every 20, Offset 17** (real :18 :38 :58).
- 8 Dubinská → Hlavní nádraží: every 60, Offset 10, Also at 52 → **every 30, Offset 10** (real :11 :41).
- 9 Hlavní nádraží → Hůrka: every 60, Offset 22, Also at 51 → Offset 22, **no Also at** (real :23).
- 9S Spojil → Hlavní nádraží: every 60, Offset 0, Also at 21 → Offset **21**, no Also at (real :22).
- 10 Hlavní nádraží → Ostřešany: every 30, Offset 21 → **every 60**, Offset 21 (real :22).
- 11 Dubina → Globus: every 60, Offset 14, Also at 34, 56 → **every 30, Offset 14** (real :15 :45).
- 12M Hlavní nádraží → Mnětice: every 30, Offset 2 → **every 60, Offset 50** (real :51).
- 13 Dubina → Ohrazenice: every 60, Offset 6, Also at 16, 26, 36, 46, 58 → **every 10, Offset 6** (real :07 :17 …). Ohrazenice:
  every 60, Offset 7, Also at 17, 27, 37, 48 → **every 10, Offset 7** (real :08 :18 …).
- 14 Polabiny → Staré Čívice: every 40, Offset 0 → **every 30, Offset 15** (real :16 :46). Staré Čívice → Polabiny: every 60, Offset 10,
  Also at 35 → **every 30, Offset 9** (real :10 :40).
- 17 Hlavní nádraží → Srch: every 60, Offset 15 → **every 30, Offset 14** (real :15 :45). Srch: every 60, Offset 12, Also at 45 →
  **every 30, Offset 12** (real :13 :43).
- 30 Hlavní nádraží → Univerzita: every 60, Offset 9, Also at 24, 54 → **every 30, Offset 24** (real :25 :55).

Vehicles: none in, none out, on any sheet (fleet.json unchanged; needs unchanged — only 48's and 38's cycle minutes changed). Every
changed line on every sheet was sized from its new pattern as well: none needs more than the sheet assigns.

## 5. Lines modelled in their wind-down (owner's choice; not changed)

These lines run their peak earlier than 16:00 and thin out in the 16:00 hour the Brno bus and Plzeň pipelines fit to. Their peak form is
exact for 1–3 h but needs more buses than the sheet has (pattern sizing, 3-min layover), so it was not applied:

| Line | Peak form (exact) | Buses |
|---|---|---|
| Brno bus 47 | every 15 (Hlavní nádraží :04 14:19–15:34) | +1 |
| Brno bus 49P | every 15 (Mariánské náměstí :05 14:35–15:50) | +1 |
| Brno bus 77L | every 30 (Úzká :08 13:08–16:08, Letiště :12 14:12–17:12) | +1 |
| Plzeň bus 21 | every 15 (Bory :10 14:10–16:10, Litice :05 14:20–16:20) | +1 |
| Plzeň bus 25 / 24 | 2 an hour (25 Bory :07/:37 14:07–16:07) | +1 each |
| Plzeň bus 26 and 42 | 26 every 60 :20 :40 / :04 :44 (14:20–16:04), 42 every 20 (14:30–15:50 / 14:34–16:14) | +1 each |
| Plzeň bus 34 | every 15 (14:03–15:40) | +0–2 (2-min turns) |
| Plzeň bus 30P | every 7–8 13:29–15:16 (shift-change peak; 61-min run) | +5 or more |
| Plzeň bus 41K | 4–5 an hour 14:05–15:37, irregular | +3 |
| Plzeň trolleybus 12 / 15 / 14 | 12 every 6 (14:21–15:27); 15 5 an hour; 14 2 an hour before 15:15 | +2 / +1 / +2 |
| Brno trolleybus 34 | every 10 (Česká :08 15:18–16:18, Vychodilova :00 15:30–16:00; gaps at 15:08 and 15:20) | 0 (same 4) |

## 6. Verification
- Rebuilt with `python -X utf8 scripts/run.py --state <state>`: brno-trolleybus, brno-bus, plzen-trolleybus, plzen-bus, pardubice.
  Brno tram and Plzeň tram not rebuilt (no change, and no code they load changed; their pages are identical to this morning's).
- `htmldiff.py` against this morning's pages: only the rows above and their notes, plus the Plzeň bus pak sentence (checkout list) and
  the method-text wording; against `_snapshots/2026-10-25` the offset-fix rows in addition.
- `city_systemic.py`: RATE, ORIGIN, RANGE, FOLD = 0 on all six GTFS sheets (rerun after the last rebuild). Approximate counts:
  Brno bus 4, Plzeň bus 14 (was 6), Plzeň trolleybus 11 — the Plzeň bus increase is labelling: the new rows are exact over a longer stretch of the peak (shown on the
  sheet as "partial, exact <span>"), the old ones were exact only inside the 16:00 hour.
- Pardubice (own check): RATE 0 on every non-daily line; ORIGIN/RANGE/FOLD 0. Hand-set rows no longer print the "merged minutes"
  line (their note says what is not modelled).
- Not done: the README's Playwright look at 1400/390 px (only text cells changed).
- Code changed (all pipeline-local, no shared common.py touched; brno-trolleybus only got a state override):
  `brno-bus/scripts/03_timetable.py` (override `passing`, `stretch` flag), `brno-bus/scripts/05_render.py` (label), `plzen-trolleybus/scripts/03_timetable.py` + `05_render.py` (`stretch` flag and label;
  used by plzen-bus too), `pardubice/scripts/03_network.py` (`fit_overrides`) + `05_render.py` (approx label, row note). READMEs updated.
