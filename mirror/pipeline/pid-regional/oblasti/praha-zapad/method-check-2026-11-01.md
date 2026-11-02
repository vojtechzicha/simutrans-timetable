# Method check: PID Praha-západ (okres Praha-západ, prefix 290/297), designed 2 Nov 2026

Designed by hand line by line with `../../DESIGN_BRIEF.md` (including "Learned on the pilot") and the bus schedule method v4
(`../../../bus-schedule-method.md`). The design is `lines.json` in this folder; `python -X utf8
pid-regional/scripts/run_oblast.py praha-zapad` rebuilds `data/derived/schedule.json` and the three audits.

- **Data:** PID GTFS of 1 Nov 2026, service day Mon 2 Nov 2026 (school day): `data/derived/trips.json` and the whole-day
  reading `data/derived/reading/<L>.txt` (every trip at its core points, the paths, the 0–5 minute chain test). The live-map
  bus chains were not in the reading files yet; the chain test is the only Step 5b evidence used, and no decision here
  hangs on the live map.
- **Step 4** per leg: in the Simutrans line's model window (anchor −30 … +90, or a window set by hand, below) the slots
  equal the real departures ±1, and at least 80 % of the slots have a real departure within 3 min; then most exact over the
  day (5–23), then within 1, then the simplest, then fewest buses; on one-departure-per-window lines the real 13–18 h
  headway decides. Every two-leg line was searched both ways together with a scratch helper (every interval dividing 1440
  up to 480, 1–8 slots placed on the window's real departures, same count both ways, buses by cyclic matching), then set
  by hand and rebuilt.
- **Typed values** are (real − 61) mod every: every terminus is a loop. The builder writes them; the table below gives each
  leg's slots (for intervals over 60, `0:xx` = even hours, `1:xx` = odd hours on every 120) and the typed values.
- **Result (after the review of 2 Nov, below):** 52 lines → 36 designed as **45 Simutrans lines, 88 buses**; 308 and 362
  not modelled (Step 8), 751 not modelled (one trip a day, none in the afternoon);
  301, 312, 318, 333, 352 are the Prague bus sheet's companions; the six night lines, X438 (290438) and CYK1 (290996, no
  trips) are listed automatically. `run_oblast.py` runs clean. Step 4 audit: 97 timed legs, 95 ok, 2 FEWER (340 out of
  Dejvická and 356 Velká Brána out of Bořislavka, both timed at the inbound rate). Branch audit: 12 legs read at a midpoint,
  all `[ok]`. Path audit: 1 flag (445, explained). Coverage: 505 afternoon stops, 399 on this sheet, 83 on other sheets; the
  7 okres-290 stops and the 2 Prague stops without a city line that no line of this sheet serves are each served by a
  frequent line of a neighbouring oblast (coverage exceptions, below). No owner checks.

## Changed on 2 Nov (independent review `review-2026-11-01.md`: 46 PASS, 6 FIX, 0 ASK)

- **320:** the note's off-pattern list corrected. The slots 0:10 / 1:10 / 1:40 repeat at 17:10, 17:40 and 18:10, which are on
  the pattern; off it out of Prague are 12:00, 13:00, 14:40, 16:40, 18:40 and 19:15. Pattern and 3 buses unchanged. (The
  earlier "two triples" comparison was the same pattern mod 120 and decided nothing.)
- **341 and the owner check:** the only owner check is deleted. 311 Mořina, 341 Libeř, 341 Dolní Břežany, 347 Chýně, 356
  Statenice and 445 Vrané are real destination variants with real trips both ways at a fixed rate in the window, which
  Step 5 decides; the 25 Oct rule ("don't add them just for frequency") is about empty returns, not real trips. 341 Libeř's
  why now says "Libeř, Libeň".
- **347:** 347 Motol (every 480, 1 bus) dropped. Hostivice, Nouzov, Palouky and Průmyslová are on 365 and 386 (Kladensko,
  modelled both ways, about every 15 minutes 13–19), so the Motol trips are a sparse variant whose stops another line serves
  (Step 8): listed. Coverage exceptions added for the three Hostivice stops and for Praha, Zadní Jiviny and Praha, Na Hůrce
  (Prague stops without a city line, on 365's modelled legs; the second also on 386). −1 bus.
- **356:** 356 Velká Brána added, hourly at the inbound rate: Bořislavka :25 → Velká Brána (11 min); back read at the knot
  Horoměřice, v lipkách :41 (`knot_rt` 1, `rt` 11 by hand: the return trips start at v lipkách, one stop after the turn, and
  no afternoon trip runs Velká Brána → Bořislavka whole); typed 24 / 39; the :55 departures off the pattern. Its out leg is
  the audit's second FEWER row (2 slots for 4 departures), the inbound-rate case as 320 and 340. +1 bus.
- **409:** the note and why said one bus; the pattern and reality need two (the :05 bus returns at :38, the :35 bus at :08).
- **664:** 664 and 664 škola replaced by one circuit every 120 at the line's own anchor 13:30, the real one-bus round
  13:18 → Vonoklasy, 13:39 back, 13:51 → škola (2-minute turn, `lay` 2), 14:09 back, 14:18 → Vonoklasy, 14:31 back; typed
  17, 38, 50, 68, 77, 90; all six window slots exact; Černošice, Husova served by it. The earlier 16:00 anchor leaned on the
  282 rule, which does not apply (Husova is on no other line), and Step 8's fold-in was not tried. The back legs now repeat at
  15:39 / 16:31 against the real 15:56 / 16:34. −1 bus.
- **Coverage exception for Mníšek pod Brdy, rozcestí Kytín:** names 317 alone (319's modelled legs on the Příbramsko sheet end
  at Mníšek and do not pass it).
- **Notes and wording:** the sheet notes name 334 ↔ 317 at Smíchovské nádraží (22 of 25) and 331 ↔ 385 at Opatov (20 of 30)
  for the 2 Nov live map; 310's note says 17:48 runs to Nučice on the :49 slot; 447's why says its 16:46 / 16:52 repeat stands
  for the real 16:46 / 16:51 železniční stanice shuttle.

## Summary

| Line | Simutrans lines (every) | Slots, real minutes (out / back) | Buses |
|---|---|---|---|
| 308 | not modelled (Step 8) | – | 0 |
| 309 | 309 (120) | Zličín 15:22 odd hours / Radotín 16:13 even hours | 1 |
| 310 | 310 (60) | Zličín :49 / Rudná, Zdrav.stř. :16 (Nučice :21) | 1 |
| 311 | 311 (60), 311 Mořina (60) | Zličín :45 / Řevnice :12; Zličín :15 / Mořina :19 | 3 + 2 |
| 313 | 313 (60) | Radotín :43 / Černošice :55 (Choteč :19) | 2 |
| 320 | 320 (120) | Smíchovské nádraží 15:10, 15:40, 16:10 / Stříbrná Lhota 16:06, 16:36, 17:06 | 3 |
| 326 | 326 (30) | Opatov :03 :33 / Belnická :01 :31 | 2 |
| 327 | 327 (30) | Opatov :13 :43 / Jesenice :16 :46 | 2 |
| 331 | 331 (30) | Opatov :23 :53 / Zálepy :17 :47 | 4 |
| 334 | 334 (30) | Smíchovské nádraží :06 :36 / Psáry :21 :51 | 3 |
| 336 | 336 (20) | Zličín :13 :33 :53 / Jeneč :07 :27 :47 | 4 |
| 338 | 338 (60) | Smíchovské nádraží :58 / Pikovice :29 | 3 |
| 340 | 340 (60, six slots) | Dejvická :11 :17 :29 :41 :47 :59 / Levý Hradec :02 :09 :24 :32 :42 :54 | 6 |
| 341 | 341 (60), 341 Libeř (60), 341 Dolní Břežany (30) | :37 / Jílové :29; :07 / Libeř :09; :22 :52 / Dolní Břežany :16 :46 | 2 + 2 + 2 |
| 347 | 347 (60), 347 Chýně (60) | Zličín :43 / Hostivice :38; :03 / Chýně :32 | 2 + 1 |
| 355 | 355 (30) | Dejvická :10 :40 / Únětice :14 :44 | 3 |
| 356 | 356 (30), 356 Lichoceves (60), 356 Statenice (60), 356 Velká Brána (60) | :15 :45 / Obchodní centrum Ruzyně :26 :56; :35 / Lichoceves :59; :05 / Statenice :25; :25 / Velká Brána :40 (v lipkách :41) | 3 + 1 + 1 + 1 |
| 358 | 358 (60) | Zličín :23 / Rudná, Hořelice :01 | 2 |
| 359 | 359 (60) | Suchdol :55 / Maxmiliánka :00 | 2 |
| 362 | not modelled (Step 8) | – | 0 |
| 390 | 390 (60) | Smíchovské nádraží :25 / Třebenice :11 | 3 |
| 409 | 409 (30) | Úholičky :05 :35 / Velké Přílepy :08 :38 | 2 |
| 418 | 418 (20) | Stodůlky :15 :35 :55 / Logport :03 :23 :43 | 1 |
| 419 | 419 (60), 419 Mokropsy (60) | Černošice :15 / Karlík :51; Černošice :45 round | 1 + 1 |
| 440 | 440 (60) | Štěchovice :12 / Masečín :25 | 1 |
| 441 | 441 (120) | Jílové 15:05, 15:45 / Luka nádraží 15:22, 16:04 | 1 |
| 444 | 444 (60) | Kamenice :29 / Davle, obec :27 | 2 |
| 445 | 445 (60), 445 Vrané (60) | Jílové :48 (Zahořany :08) / Oleško :10; Zahořany :38 / Vrané :03 | 3 + 1 |
| 446 | 446 (60) | kaple :12 :52 / Kytín :04 :44 | 1 |
| 447 | 447 (120, circuit) | náměstí 14:03 → Chouzavá 14:20 → náměstí 14:46 → OPS Magdaléna 14:52 | 1 |
| 448 | 448 (120) | Mníšek :04 hourly / Lety 13:46, 14:56 | 2 |
| 449 | 449 (90) | Mníšek 15:35 (14:05) / Bojov 16:10 (14:40) | 1 |
| 632 | 632 (60) | Řevnice :05 / Hostomice :24 | 2 |
| 664 | 664 (120, circuit) | Černošice 13:18 → Vonoklasy 13:39 → Černošice 13:51 → škola 14:09 → Černošice 14:18 → Vonoklasy 14:31 | 1 |
| 672 | 672 (90) | Všenory 15:30 (17:00) / Hlásná Třebaň 16:18 | 1 |
| 688 | 688 (60, circuit) | Mníšek :45 via nemocnice / Nový Knín :30 direct / Mníšek :15 direct / Nový Knín :55 via nemocnice | 3 |
| 748 | 748 (120) | Mníšek 13:37 / Bratřínov 13:51 | 1 |
| 751 | not modelled (one trip a day, 7:08) | – | 0 |
| 762 | 762 (60) | Jesenice :17 / Na Drahách :39 | 1 |
| **Total** | **45 Simutrans lines** | | **88** |

Bus counts are the builder's need from each pattern (Step 10), one Simutrans line at a time. Real buses swap between these
lines and the Prague city lines at Zličín, Dejvická, Smíchovské nádraží and Opatov (the chain tests show many 0–5 minute
links with 100, 107, 125, 145, 180, 249 …, which are city lines passing a hub), so the per-line totals are higher than the
operators' own. Pooling is an owner option, not applied.

## How some recurring questions were decided

- **Regular afternoon variants get a Simutrans line (Step 5), sparse ones are listed (Step 8).** Where a line's short or
  variant trips run at a fixed rate both ways in its afternoon window they are their own Simutrans line, even when all
  their stops are on the main line: 311 Mořina, 341 Libeř, 341 Dolní Břežany, 347 Chýně, 356 Statenice, 356 Velká Brána
  (at its inbound rate, hourly), 445 Vrané. Step 5 decides them; they are not an owner question (review, 2 Nov). Sparse or
  irregular variants whose stops other lines serve are listed (Step 8): 313 Choteč (Radotín :13 odd hours), 347 Motol,
  390 Štěchovice (irregular), 409 Suchdol, 446 Dobříš, 449 Jíloviště, 688 Dobříš, 748 Řitka, 444 Jílové – Kamenice.
- **Serve every place.** Černošice, Husova (one afternoon trip, no other line) is served by the 664 circuit, which folds the
  school round into the line's own bus (Step 8 fold-in). The nine coverage exceptions are not roadside exceptions: each stop
  is served all afternoon by a modelled line of a neighbouring oblast (below).
- **Outstation lines** (buses sleep at the outer end, the afternoon is an outflow from Prague): 320 (Stříbrná Lhota), 340
  (Roztoky), 390 (Třebenice), 338 (Pikovice) and 313 (Roblín / Choteč) were timed at the inbound rate; the extra departures
  from Prague are listed. 340 shows as FEWER in the audit; on the others the inbound rate equals the window's slots ±1.
  356 Velká Brána is timed the same way (hourly, as its returns from v lipkách), the second FEWER row.
- **Anchors and windows set by hand**, each because the automatic window held a stray or a variant rather than the line's
  own pattern (the 282 rule, as the pilot's 305): 338 → 15:30 (16:00 window put the second Pikovice slot on 17:34, 5 min
  off); 409 → 17:00 (in 15:30–17:30 the shuttle bus is away on the Suchdol round, no 15:38 from Velké Přílepy); 440 → 14:30
  (Masečín 16:30 five minutes late); 446 → 16:00 (13:00–15:00 is school extras on the same stops); 449 → 15:00 (the 16:00
  window holds the Jíloviště trips); 664 → 13:30 written explicitly (its automatic anchor, kept since the review); 390 sim
  window 15:00–17:00 (the line's anchor 14:20 comes from the Štěchovice short trips; the Třebenice trips before 15:00 run
  10 min later).
- **0-minute turns** (441 at Luka p.Medníkem, nádraží; 447 at Voznice, Chouzavá and OPS Magdaléna): real slots and running
  times kept, `lay: 0` on the departing leg, "0-minute turn as in the timetable" in the why; the Leave up to question is in
  the sheet notes once (engine session).
- **Terminus alias:** Roztoky, Přemyslovská → Roztoky, Levý Hradec (340's buses end at Přemyslovská and leave from Levý
  Hradec, the next stop of the loop). The alias also renames Přemyslovská inside 359's paths; Přemyslovská has no
  departure of its own there, so coverage is unaffected.

## Line by line

Each: (a) core points; (b) what the whole day shows; (c) Step 4 and the candidates; (d) the Simutrans lines; (e) knots;
(f) off the pattern 12–20 h; (g) buses.

**308 Praha, Zličín – Rudná – Nučice** (not modelled). 10 trips, 4 in 13–19: Zličín 13:10 → Nučice 13:32, back at once 13:32;
Nučice 14:40, 18:40 → Zličín, whose buses are 310's 14:19 and 18:18 Nučice trips (the chain test: 3 of 5 departures follow a
310 arrival). Step 8: every stop is on 311 (Chrášťany, Rudná, Nučice) and 310, except Rudná, Za Panskou zahradou, which 380
(Berounsko) serves every 30 → coverage exception. The 310-out / 308-back round every 240 (14:19 / 18:18, exact) was
considered and not added: it would be a bus for stops other lines serve.

**309 Praha, Zličín – Tachlovice – Třebotov – Kosoř – Praha, Nádraží Radotín.** (a) Zličín; Jinočany, náměstí; Tachlovice,
Jakubská náves; Kosoř; Radotín. (b) Exactly every 120 by one bus: Zličín :22 odd hours, Radotín :13 even hours. (c) Every 120
1 / 1 slot each way, filled; the only passing candidate with the real headway (every 240: 5 exact against 9). (d) 309
(120). (e) Jinočany, Tachlovice, Kosoř exact both ways. (f) Zličín 12:14, 8:53, 21:26; Radotín 5:43, 7:13. (g) 1 (waits 4 at
Radotín, 22 at Zličín). No stop of its own (Jinočany / Tachlovice on 310, Kosoř / Třebotov on 313, Chýnice on 301), kept as
the regular line it is.

**310 Praha, Zličín – Jinočany – Tachlovice – Nučice – Rudná, Zdrav.stř.** (a) Zličín; Jinočany; Nučice, Prokopská náves
(knot); Rudná, Zdrav.stř. (b) Afternoon :49 hourly to Rudná (13:49 only to Nučice), Rudná :16 back, a 2-minute turn (chain
4 of 7); Nučice short trips 14:19, 16:17, 17:48, 18:18 (two go back as 308). (c) Every 60: out 2 slots / 3 real (16:17 the
Nučice short), filled 2/2; back 2/2. Every 120 with two slots ties on exact hits and is longer. (d) 310 (60), out read to
Nučice (`core_to`), back read at Nučice (`knot`, mixed origins on its own path). (e) Jinočany, Nučice exact. (g) 1 (2 min at
Rudná). Its own stops: Nučice, bytovky; Tachlovice, Na vrškách; Rudná, Zdrav.stř.

**311 Praha, Zličín – Rudná – Nučice – Mořina – Lety – Dobřichovice – Řevnice.** (a) Zličín; Nučice; Mořina; Řevnice.
(b) Zličín :45 → Řevnice and Řevnice :12 back, hourly all day and exact (12 of 12 out); Mořina short trips Zličín :15
15:15–17:15 and Mořina :19 16:19, 17:19, their buses sleeping at Mořina. (c) 311: 2/2 both ways, exact. 311 Mořina (`notvia`
Řevnice so the through trips stay out): 2/2 both ways, exact. (d) 311 (60) and 311 Mořina (60). (e) Mořina and Nučice exact.
(f) Řevnice 5:22, 6:25, 10:05; Zličín 19:45, 21:00 to Mořina. (g) 3 + 2. 5 of 15 arrivals at Řevnice go on as 632 (notes).
Own stops: Lety, Mezouň, Nučice, železniční zastávka; Bubovice and Mořinka (okres Beroun) only here.

**313 Praha, Nádraží Radotín – Kosoř – Třebotov – Choteč – Roblín – Černošice.** (a) Radotín; Kosoř; Choteč (knot); Roblín;
Černošice, železniční zastávka. (b) Radotín :43 every hour (to Černošice 12:43–15:43, Choteč 16:43, Roblín 17:43–19:43);
Choteč :19 towards Radotín hourly 14:19–18:19 (15:21 is the 14:57 Černošice trip); the buses turn at Radotín in 3 min (8 of
16 chains). Plus Choteč short trips Radotín :13 odd hours. Buses sleep at Roblín / Choteč (first trips 4:07, 4:36, 5:20 start
there). (c) Every 60 :43 / :19 at Choteč: out 2 slots / 3 real (17:13 the Choteč short), back 2/2, 19 exact over the day;
two lines every 120 (:43 odd + :13 odd Choteč, back :19 split) give about 18 exact by a hand count for the same 2 buses,
so the single, simpler line wins.
(d) 313 (60), out read to Choteč, back read at Choteč; game path the 13:43 / 15:43 trips' (via Vysoký Újezd, Kozolupy and
Mořina, Trněný Újezd, 55 min, `rt` set by hand: the builder's median mixed the 45-min direct trips); back the 14:57 trip's
path with `knot_rt` 24 and `rt` 43 set by hand (the median 27 / 48 came from the morning trips). (e) Kosoř and Choteč exact
out; the card's knot check shows Choteč 3 min off back because it uses the median 27 (display only). (f) Radotín 13:13,
15:13, 17:13, 19:13 (Choteč), Černošice – Roblín shuttle 16:46 / 16:58, Roblín 18:33. (g) 2. Own stops: Choteč, Roblín (2),
Kala, Solopisky ZD; Mořina, Trněný Újezd (2, okres Beroun) only here.

**320 Praha, Smíchovské nádraží – Jíloviště – Řitka – Mníšek pod Brdy – Stříbrná Lhota.** (a) Smíchovské nádraží; Mníšek,
náměstí; Stříbrná Lhota. (b) Out :10 / :40 14:10–18:40; back Stříbrná Lhota hourly :06 with 16:36 extra; an outstation line
(the first trips 4:47–7:58 start at Stříbrná Lhota). (c) Window 15:30–17:30: out 4 real, back 3. Every 120 with three slots
each way = the inbound rate. Out triples tested: 15:40 / 16:10 / 17:10 (9 exact) needs 4 buses (one 113-min wait), 15:10 /
15:40 / 16:10 (8 exact) needs 3: by the 290 rule (choose the departures that fall off by the waits) the second, which is
also the plates' reading (the 15-min turns at Stříbrná Lhota). Every 60 :10 / :06 (2 buses) runs below the inbound rate
(2 slots for the window's 3 back departures, 16:36 off) and was not taken. (d) 320 (120). (e) Mníšek, náměstí exact.
(f) Out 12:00, 13:00, 14:40, 16:40, 18:40, 19:15 (the :40 departures of even hours are buses going home; 17:10, 17:40 and
18:10 are on the pattern); back 13:21, 18:21, 19:21; the náměstí shorts.
(g) 3. Own stops: Stříbrná Lhota (2), Na Kvíkalce, sídliště; the hlavní silnice stops of Jíloviště, Klínec, Líšnice.

**326 Praha, Opatov (Volha) – Vestec – Jesenice, Belnická.** (b) Opatov :03 / :33 (the Volha trips pass Opatov at the same
minutes until 16:00), Belnická :01 / :31, every 30 all afternoon. (c) 4/4 both ways. (d) 326 (30), read from Opatov (the
Volha – Opatov part is Prague). (g) 2. 13 of 38 arrivals at Opatov go on as 331 (notes). Own stops: Jesenice, bytovky;
Vestec, Šátalka.

**327 Praha, Opatov – Zdiměřice – Osnice – Jesenice [PZ].** (b) :13 / :43 and :16 / :46, every 30, exact; 1-minute turn at
Opatov (12 of 33 chains). (c) 4/4 both ways. (d) 327 (30), lay 1 at Opatov as the timetable turns. (g) 2. Own stops: the
Osnice, Kocanda and Zdiměřice stops (6).

**331 Praha, Opatov – Dolní Břežany – Ohrobec – Zálepy.** (b) :23 / :53 out (direct, 32 min), :17 / :47 back via Inovační,
Vestec, obchodní centrum and BIOCEV (45 min), every 30. (c) 4/4 both ways. (d) 331 (30). (f) 12:29, 13:14 (the long path
out). (g) 4. Own stops: Zálepy, Ohrobec (2), Na rovném, hřiště, Inovační, Vestec, obchodní centrum, BIOCEV.

**334 Praha, Smíchovské nádraží – Dolní Břežany – Jesenice – Psáry.** (b) :06 / :36 and :21 / :51, every 30 15:06–18:06,
hourly on the same minutes otherwise; every trip of the day on the pattern (24/24, 25/25). (g) 3. Own stops: Psáry (3).

**336 Praha, Zličín – Chýně – Hostivice – Jeneč, Lidická.** (b) Every 20 to Jeneč 14:53–17:13 (:13 :33 :53), back :07 :27
:47, 3-minute turn (11 of 18 chains); hourly to Hostivice, Ve Vilkách at midday and evening. (c) Every 20: 6/6 both ways.
(d) 336 (20). (f) 13:05, 13:29, 13:59, 14:28 (every 30 before the peak), the Ve Vilkách trips. (g) 4. Own stops: Chýně,
Městský úřad; Hostivice, Břve (2), Na Pískách, Ve Vilkách; Jeneč (2).

**338 Praha, Smíchovské nádraží – Davle – Štěchovice – Hradištko, Pikovice.** (b) Out :58 14:58–17:58; back 14:29, 15:29,
16:29, 17:34. (c) At the automatic 16:00 window the back leg has 16:29 and 17:29 (17:34 five off): 1 of 2 filled, FAIL; every
120 one slot each way passes (2 buses) but halves an hourly line (the 409/411 mistake, Opavsko rule 5). Anchor 15:30: 2/2
both ways, exact. (d) 338 (60). (f) 13:20, 14:25, 18:25, 19:20; Pikovice 17:34; zámek and Štěchovice shorts. (g) 3 (42 min at
Pikovice, 39 at Smíchovské nádraží; the real buses also run city lines at Smíchovské nádraží). Own stops: Pikovice (3),
Hradištko (5).

**340 Praha, Dejvická – Roztoky – Levý Hradec.** (a) Dejvická; Roztoky, nádraží (knot); Levý Hradec (alias of
Přemyslovská). (b) Peak out 8 an hour: :11 :17 :23 :41 :47 :53 to Přemyslovská, :29 :59 to Roztoky, nádraží, whose buses go on
at once as 359 round the town to Levý Hradec (18 of 18); back 6 an hour: Levý Hradec :02 :09 :24 :32 :54 (:24 / :54 are those
359 buses) and nádraží :50 (the 359 Levý Hradec :39 bus, 12 of 12). Buses sleep in Roztoky (5:21–6:00 first trips). (c) The
inbound rate is 6 an hour. Every 10 (one slot each way, 6 buses) fills every slot within 3 but has 9 + 16 exact; every 60
with six slots each way (12 typed values, 6 buses) has 25 + 21 exact, so it is taken. The audit's "every 48" with seven
slots is not a divisor of 60, needs 3 more buses and runs out at 7.5 an hour, against the inbound-rate rule. Out is FEWER
(12 slots for 16 departures), the approved outstation case. By the plates the departures that fall off are :23 and :53 (their
buses do not come back as 340). (d) 340 (60); the town round of 359 is not given its own line: its stops are on 359
(Suchdol – Maxmiliánka) and 340, so coverage holds; a 340 Roztoky circuit (Dejvická – nádraží – town – Levý Hradec –
Dejvická, every 30) would add about 2 buses for frequency only. The card says the game bus runs the direct road. (e) nádraží
exact; Levý Hradec 6 min late for the :29 / :59 slots (the real buses go round the town). (g) 6.

**341 Praha, Obchodní náměstí – Dolní Břežany – Libeř – Jílové u Prahy.** (b) Fixed hourly rotation all afternoon, exact:
:07 Libeř, :22 / :52 Dolní Břežany, obecní úřad, :37 Jílové; back :09, :16 / :46, :29. (c) Each 2/2 or 4/4, 13/13 and 17/18
exact. (d) 341 (60), 341 Libeř (60), 341 Dolní Břežany (30); `notvia` Jílové / Libeř keep the variants apart. (g) 2 + 2 + 2.
341 Libeř and 341 Dolní Břežany have no stop of their own; Step 5 gives them their lines (real destination variants). Own stops of 341: Jílové u Prahy, Radlík and
rozcestí Radlík; the Libeř, Dolní Břežany and Prague stops of the header are also on the variant lines.

**347 Praha, Zličín – Chýně – Hostivice.** (b) Zličín :43 (:50 midday and evening) → Hostivice, nádraží, :38 back; Chýně
short trips :03 / :32 15:03–18:32 by one bus; Motol trips 8:50 (Zličín → Motol) and 14:19 (Motol → Zličín). (c) 347 2/2 both
ways; 347 Chýně 2/2 both ways (`notvia` Hostivice, nádraží). (d) 347, 347 Chýně. The Motol trips are listed (Step 8): their
Hostivice, Nouzov, Palouky, Průmyslová and Praha, Zadní Jiviny, Na Hůrce are on 365 and 386 (Kladensko, modelled) →
coverage exceptions. (f) 12:50, 18:50, 19:52, the Břve evening trips, the two Motol trips. (g) 2 + 1.

**355 Praha, Dejvická – Horoměřice – Únětice.** (b) :10 / :40 and :14 / :44, every 30, 12:40–19:40, exact. (c) 4/4 both ways.
(g) 3 (29 min at Dejvická). Own stops: Horoměřice, Švejkova; LIDL.

**356 Praha, Bořislavka – Horoměřice – Statenice – Obchodní centrum Ruzyně / Lichoceves / Statenice.** (a) Bořislavka;
Horoměřice, v lipkách; Statenice (fork); Lichoceves; Obchodní centrum Ruzyně. (b) Out every 10 in a fixed rotation (:15 / :45
Obchodní centrum Ruzyně, :35 Lichoceves, :05 Statenice, :25 / :55 Velká Brána); back :26 / :56, :59, :25, v lipkách :41.
Automatic anchor 14:30 (window 14:00–16:00), kept. (c) 356 4/4 both ways; 356 Lichoceves 2/2 (back 2 slots for 3 departures:
14:04, 14:59, 15:59); 356 Statenice 2/2 (`notvia` u hřiště and Lichoceves keeps the through trips out). 356 Velká Brána
(since the review): out 7 trips 14:25–17:25 every 30, back 4 hourly from v lipkách :41; timed hourly at the inbound rate,
Bořislavka :25 and v lipkách :41 (knot, `knot_rt` 1, `rt` 11 by hand), out 2 slots for 4 departures (FEWER, the :55 off), back
2/2, all exact; `notvia` Statenice, Černý Vůl, hospoda keeps the through trips out. (d) 356 (30), 356 Lichoceves (60), 356
Statenice (60), 356 Velká Brána (60). (g) 3 + 1 + 1 + 1. Own stops: the Tuchoměřice stops (on 356), Statenice, Račanská (356
Lichoceves).

**358 Praha, Zličín – Chýně – Rudná, Hořelice.** (b) Zličín :23 (13:20, 14:14, 15:23–17:23, 18:30), Hořelice :01 (14:05–17:01).
(c) 2/2 both ways; every 120 one slot would need 1 bus but has fewer exact hits. (g) 2 (55 min at Zličín; 5 of 7 real
arrivals go on as 249). Own stop: Chýně, Na Vyhlídce.

**359 Praha, Suchdol – Únětice – Roztoky – Maxmiliánka.** (b) Suchdol :55, Maxmiliánka :00, hourly; the Roztoky, nádraží –
Levý Hradec town round is 340's (above). (c) 2/2 both ways. (g) 2. Every Suchdol arrival goes on as 107 (11 of 11; 107 is a
Prague city line, card 100–108 untouched). Own stops: the Roztoky town stops (6).

**362 Praha, Budějovická – Jílové u Prahy** (not modelled). Afternoon: Budějovická 14:53–17:53 hourly out, Jílové 16:00 back;
the buses come from and go on as 332 at Jílové (5 of 5). Step 8: every stop 13–19 is on 341 (Jílové, Pražská, Za Humny, Radlík,
rozcestí Radlík, Libeř) or in Prague.

**390 Praha, Smíchovské nádraží – Štěchovice – Slapy – Třebenice.** (b) Třebenice trips: Smíchovské nádraží 13:35, 14:35,
15:25, 16:25, 17:25, 18:40; Třebenice 13:56, 15:11, 16:11, 17:06. Štěchovice short trips irregular (above). Automatic anchor
14:20 (window 13:50–15:50): the Třebenice legs fail there (14:25 and 14:11 empty). (c) Sim window 15:00–17:00: every 60 :25 /
:11, 2/2 both ways. (d) 390 (60). (f) 13:35, 14:35, 18:40, 19:35; 12:41, 13:56, 17:06, 19:31; the Štěchovice shorts. (g) 3 (57
min at Třebenice, where the buses sleep). Own stops: Třebenice, Slapy (3).

**409 Úholičky – Velké Přílepy (– Praha, Suchdol).** (b) Shuttle every 30, Úholičky :05 / :35, Velké Přílepy :08 / :38; four
trips each way run through to Suchdol in the shuttle's slots (7:54, 8:54, 14:24, 15:54; 7:05, 8:05, 13:35, 15:05). (c) At
16:00 the back leg's 15:38 has no trip (the bus is on the Suchdol round): 3 of 4, FAIL. Anchor 17:00: 4/4 both ways, 22 + 20
exact. (d) 409 (30). (g) 2, as in reality (the :05 bus returns at :38, the :35 bus at :08; 20 min at Velké Přílepy; 6 of 18
arrivals go on as 622). The Suchdol trips are listed; Velké
Přílepy, Pražská and Statenice, Černý Vůl are 316's (Mělnicko) → coverage exceptions.

**418 Praha, Stodůlky – Jinočany, Logport.** (b) Every 30 13:25–15:55, every 20 15:55–17:55 (:15 :35 :55 / :03 :23 :43), hourly
otherwise. (c) Every 20 at 16:10: 6/6 both ways. The day-exact search prefers Logport :00 :20 :40 (the morning peak's minutes,
10 exact) over :03 :23 :43 (6 exact): the afternoon wins (method, "Which hour"), every window departure exact. (g) 1.

**419 Černošice – Dobřichovice – Karlík; Černošice-Mokropsy round.** (b) Karlík line hourly :15 / :51, exact; the Mokropsy round
Černošice :45 → Javorová, Na Ladech, Mokropsy železniční zastávka, škola → Černošice, hourly 14:45–17:45. (c) 2/2 each. (d) 419
(60), 419 Mokropsy (60, one circular leg). (g) 1 + 1. The 664 bus runs the round at 14:45 and 16:45 (chains 6 of 14); kept
separate. Own stops: Karlík, Randova, pod vinicí (419); Javorová, Na Ladech, u kamenného mostu, Masopustní náměstí, Mokropsy
železniční zastávka (419 Mokropsy).

**440 Štěchovice – Masečín.** (b) :12 / :25 hourly 14:12–18:12; Masečín 16:30. The 390 Štěchovice short trips' buses run 440
(9 of 9 short departures follow a 440 arrival). (c) A 390-short + 440 circuit every 60 (2 buses, against 1 + 2) was built and
fails Step 4 in every window (no 16:35 short from Štěchovice, the 16:30 from Masečín); 440 alone at anchor 14:30: 2/2 both ways.
(d) 440 (60). (g) 1. Own stops: Masečín (2), Nad Horou.

**441 Jílové u Prahy – Luka pod Medníkem.** (b) One bus: Jílové 14:10, 15:05, 15:45, 17:50, 18:50; back 14:27, 15:22, 16:04,
18:08, 19:08, mostly 0-minute turns. (c) Window 14:10–16:10 holds 3 each way; every 120 with two slots each way (15:05 /
15:45, 15:22 / 16:04) passes and needs 1 bus, 5 exact; 14:10 / 15:05 with 14:27 / 15:22 also 1 bus, 4 exact; three slots
need 3 buses. (d) 441 (120), back read at Luka p.Medníkem (knot), `lay: 0` at the nádraží. (g) 1. Own stops: 7 (Luka, Studené,
hřbitov, učiliště, Petrov, Bohuliby).

**444 Kamenice – Pohoří – Jílové u Prahy – Petrov – Davle.** (b) Kamenice → Davle through at :29 hourly 14:29–17:29; Davle
:26 (u pomníku) hourly towards Jílové, only 15:26 through to Kamenice; Jílové → Kamenice at other minutes. (c) Every 60: 2/2
out, back 2 slots / 3 real (15:57), exact. (d) 444 (60), terminal Davle, obec (the arrival stop; the departures from u pomníku
pass it 1 min later, `fr` obec so one terminus), back read to Jílové (`core_to`). (e) Jílové exact both ways. (f) Davle 13:16,
14:20, 15:56, 18:40; Kamenice 14:59, 18:44; Jílové – Kamenice trips; Těptín shorts. (g) 2. Own stops: 17 (Petrov, Pohoří,
Davle, Sázava, Čs.armády; Kamenice (4) of okres Praha-východ).

**445 Jílové u Prahy – Zvole – Vrané nad Vltavou – Březová-Oleško.** (b) Through hourly: Jílové :45 / :48 (Zahořany :08),
Oleško :10; Zahořany – Vrané shuttle :38 / :03. (c) 445: out read at Zahořany (knot) with `via` Jílové so the shuttle starts
stay out, 2/2, 9/9 exact; back read to Vrané (`core_to`), 2/2. 445 Vrané 2/2 both ways. (d) 445 (60), 445 Vrané (60). Path audit:
the 15:48 slot is the 15:45 trip via učiliště, Kovo, Průmyslová (game path via Pražská, Za Humny, `stops_via`, as 16:48);
named in the why. (g) 3 + 1. Own stops: Oleško area (3), Vrané (4).

**446 Mníšek pod Brdy, kaple – Kytín.** (b) :12 / :52 and :04 / :44 from 15:12; school extras 13:00–15:00. (c) Anchor 16:00 (the
282 rule): 4/4 both ways (16:11 one minute early). (d) 446 (60, two slots). (g) 1. No stop of its own (Kytín is on 447's
Chouzavá leg), kept as the regular shuttle it is. Dobříš trips listed (317 / 319).

**447 Mníšek pod Brdy, náměstí – železniční stanice / OPS Magdaléna / Voznice, Chouzavá.** (b) One bus on single trips
(above). (c) Every 120 circuit on the 14:03–15:00 round; each leg 1 slot, filled. (d) 447 (120, náměstí twice, pattern need).
(g) 1. Own stops: OPS Magdaléna, u hřbitova, železniční stanice, nad špejcharem, u Šibence; Voznice, Chouzavá (okres Příbram).

**448 Mníšek pod Brdy – Řitka – Všenory – Dobřichovice – Lety.** (b) Mníšek :04 hourly to 15:04; Lety 13:00, 13:46, 14:56,
15:46. (c) Window 13:00–15:00 (automatic anchor 13:30): every 60 :04 / :46 leaves 14:46 without a trip (FAIL); every 120 with
Mníšek :04 :04 and Lety 13:46 / 14:56 passes, 6 + 5 exact, 2 buses. (d) 448 (120). (g) 2. Own stops: Všenory (3), Černolice (2),
Řitka, u rybníka.

**449 Mníšek pod Brdy – Řitka – Klínec – Čisovice, Bojov.** (b) One bus, Bojov turns 4 min: 12:49, 14:05, 15:35, 17:20, 18:45;
13:25, 14:40, 16:10, 17:55; Jíloviště trips are 318's buses. (c) Anchor 15:00: every 90 1 slot out / 2 back, filled, 3 + 3
exact; every 120 passes at 16:00 with 1 + 1. (d) 449 (90). (g) 1. Own stops: Klínec, Spálený Mlýn, Čisovice, Bojov (2).

**632 Řevnice – Osov – Hostomice.** (b) :05 / :24 hourly, exact. (c) 2/2 both ways. (g) 2. Own stops: 17, all okres Beroun
(Svinaře, Skuhrov, Osov, Velký Chlumec, Hostomice, Lštěň).

**664 Černošice – Vonoklasy (+ škola).** (b) One bus: out :18 hourly; back 13:39, 14:31, 15:56, 16:34, 17:56, 18:57; school
rounds 12:51 / 13:09 and 13:51 / 14:09 (Kladenská, Husova, škola) between the Vonoklasy trips. (c) Since the review: one
circuit every 120 at the automatic anchor 13:30 (written explicitly) on the real 13:18–14:41 round: Černošice 13:18 →
Vonoklasy, 13:39 back, 13:51 → škola (2-minute turn, `lay` 2), 14:09 back, 14:18 → Vonoklasy, 14:31 back; typed 17, 38, 50,
68, 77, 90; every leg 1/1 in the window, exact. Earlier: 664 at 16:00 (15:56 / 16:34) plus 664 škola every 480, 2 buses.
(d) 664 (120, circuit; Černošice three times, pattern need). (f) Vonoklasy 12:39, 15:56, 17:56, 18:57; 12:51 / 13:09.
(g) 1. Own stops: Vonoklasy (3); Černošice, Husova.

**672 Všenory – Dobřichovice – Hlásná Třebaň.** (b) Všenory 14:00, 15:30, 17:00; Hlásná Třebaň 13:18, 14:58, 16:18, 17:33.
(c) Every 90: 2/2 out, 1/1 back, 3 + 2 exact; every 160/180 fewer. (g) 1. Own stops: Hlásná Třebaň (okres Beroun), Všenory,
Horní Mokropsy, Všenory, železniční zastávka.

**688 Mníšek pod Brdy – Nová Ves pod Pleší – Nový Knín.** (b) Every 30 14:15–17:15, alternating paths: :45 via the
hospital, :15 direct; back :30 direct, :55 via the hospital; the buses alternate (each turn 15–16 min). Automatic anchor 15:00.
(c) One circuit every 60 with four legs (`via` / `notvia` Nová Ves pod Pleší, nemocnice), each 2/2 filled. Two separate lines
(per path) need 4 buses; the circuit 3. (d) 688 (60, circuit). (g) 3. Own stops: 12 (Malá Hraštice, Nová Ves pod Pleší and
Nový Knín, okres Příbram; Zahořany, Rymaně, Hladový vrch). Dobříš trips listed (361).

**748 Mníšek pod Brdy – Čisovice – Bratřínov.** (b) One bus: 12:37, 13:37, 14:37, 16:07 out; 12:22, 13:51, 16:40 back; Řitka
shorts are 318's buses. (c) Every 120 13:37 / 13:51 (1-minute turn, lay 1): 1/1 back, out 1 slot / 2 real. (g) 1. Own stop:
Čisovice, železniční stanice (Bratřínov is also on 314).

**751 Řevnice – Mořina** (not modelled): one trip a day, 7:08, no stop of its own.

**762 Jesenice – Zlatníky-Hodkovice, Na Drahách.** (b) :17 / :39 hourly 13:17–17:39, exact. (g) 1. Own stop: Na Drahách.

## Step 4 per leg (from `schedule.json`)

Columns: slots (mod every) with the typed values in brackets; window slots; real departures in the window; window slots
with a real departure within 3 min; exact / within 3 / trips over the day (5–23).

| Simutrans line | Leg | Slots (typed) | Window slots | Real in window | Filled | Day ex/w3/n |
|---|---|---|---|---|---|---|
| 309 | Zličín → Nádraží Radotín | 1:22 (21) | 17:22 | 17:22 | 1/1 | 3/6/9 |
| 309 | Nádraží Radotín → Zličín | 0:13 (72) | 16:13 | 16:13 | 1/1 | 6/6/8 |
| 310 | Zličín → Rudná, Zdrav.stř. | :49 (48) | 15:49 16:49 | 15:49 16:17 16:49 | 2/2 | 5/7/17 |
| 310 | Rudná, Zdrav.stř. → Zličín | :16 (15) | 16:16 17:16 | 16:16 17:16 | 2/2 | 3/4/19 |
| 311 | Zličín → Řevnice, nádraží | :45 (44) | 15:45 16:45 | 15:45 16:45 | 2/2 | 12/12/12 |
| 311 | Řevnice, nádraží → Zličín | :12 (11) | 16:12 17:12 | 16:12 17:12 | 2/2 | 7/11/14 |
| 311 Mořina | Zličín → Mořina | :15 (14) | 16:15 17:15 | 16:15 17:15 | 2/2 | 3/4/9 |
| 311 Mořina | Mořina → Zličín | :19 (18) | 16:19 17:19 | 16:19 17:19 | 2/2 | 2/3/7 |
| 313 | Nádraží Radotín → Černošice, železniční zastávka | :43 (42) | 15:43 16:43 | 15:43 16:43 17:13 | 2/2 | 12/12/19 |
| 313 | Černošice, železniční zastávka → Nádraží Radotín | :55 (54) | 15:55 16:55 | 15:55 16:55 | 2/2 | 7/8/13 |
| 320 | Smíchovské nádraží → Mníšek, Stříbrná Lhota | 0:10, 1:10, 1:40 (9, 39, 69) | 15:40 16:10 17:10 | 15:40 16:10 16:40 17:10 | 3/3 | 8/8/21 |
| 320 | Mníšek, Stříbrná Lhota → Smíchovské nádraží | 0:06, 0:36, 1:06 (5, 65, 95) | 16:06 16:36 17:06 | 16:06 16:36 17:06 | 3/3 | 6/6/20 |
| 326 | Opatov → Jesenice, Belnická | :03 :33 (2) | 15:33 16:03 16:33 17:03 | 15:33 16:03 16:33 17:03 | 4/4 | 13/15/39 |
| 326 | Jesenice, Belnická → Opatov | :01 :31 (0) | 15:31 16:01 16:31 17:01 | 15:31 16:01 16:31 17:01 | 4/4 | 10/14/39 |
| 327 | Opatov → Jesenice [PZ] | :13 :43 (12) | 15:43 16:13 16:43 17:13 | 15:43 16:13 16:43 17:13 | 4/4 | 10/16/28 |
| 327 | Jesenice [PZ] → Opatov | :16 :46 (15) | 15:46 16:16 16:46 17:16 | 15:46 16:16 16:46 17:16 | 4/4 | 13/19/31 |
| 331 | Opatov → Dolní Břežany, Zálepy | :23 :53 (22) | 15:53 16:23 16:53 17:23 | 15:53 16:23 16:53 17:23 | 4/4 | 11/11/28 |
| 331 | Dolní Břežany, Zálepy → Opatov | :17 :47 (16) | 15:47 16:17 16:47 17:17 | 15:47 16:17 16:47 17:17 | 4/4 | 17/22/28 |
| 334 | Smíchovské nádraží → Psáry | :06 :36 (5) | 15:36 16:06 16:36 17:06 | 15:36 16:06 16:36 17:06 | 4/4 | 24/24/24 |
| 334 | Psáry → Smíchovské nádraží | :21 :51 (20) | 15:51 16:21 16:51 17:21 | 15:51 16:21 16:51 17:21 | 4/4 | 25/25/25 |
| 336 | Zličín → Jeneč, Lidická | :13 :33 :53 (12) | 15:33 … 17:13 (6) | the same 6 | 6/6 | 8/8/18 |
| 336 | Jeneč, Lidická → Zličín | :07 :27 :47 (6) | 15:47 … 17:27 (6) | the same 6 | 6/6 | 9/12/18 |
| 338 | Smíchovské nádraží → Hradištko, Pikovice, most | :58 (57) | 15:58 16:58 | 15:58 16:58 | 2/2 | 4/4/11 |
| 338 | Hradištko, Pikovice, most → Smíchovské nádraží | :29 (28) | 15:29 16:29 | 15:29 16:29 | 2/2 | 3/3/10 |
| 340 | Dejvická → Roztoky, Levý Hradec | :11 :17 :29 :41 :47 :59 (10, 16, 28, 40, 46, 58) | 12 slots 15:41–17:29 | 16 (the slots + 15:53 16:23 16:53 17:23) | 12/12 | 25/41/61 |
| 340 | Roztoky, Levý Hradec → Dejvická | :02 :09 :24 :32 :42 :54 (1, 8, 23, 31, 41, 53) | 12 slots 15:32–17:24 | the same 12 | 12/12 | 21/53/64 |
| 341 | Obchodní náměstí → Jílové, náměstí | :37 (36) | 15:37 16:37 | 15:37 16:37 | 2/2 | 13/13/13 |
| 341 | Jílové, náměstí → Obchodní náměstí | :29 (28) | 16:29 17:29 | 16:29 17:29 | 2/2 | 13/13/13 |
| 341 Libeř | Obchodní náměstí → Libeř | :07 (6) | 16:07 17:07 | 16:07 17:07 | 2/2 | 10/10/15 |
| 341 Libeř | Libeř → Obchodní náměstí | :09 (8) | 16:09 17:09 | 16:09 17:09 | 2/2 | 11/11/17 |
| 341 Dolní Břežany | Obchodní náměstí → Dolní Břežany, obecní úřad | :22 :52 (21) | 15:52 16:22 16:52 17:22 | the same 4 | 4/4 | 17/17/18 |
| 341 Dolní Břežany | Dolní Břežany, obecní úřad → Obchodní náměstí | :16 :46 (15) | 15:46 16:16 16:46 17:16 | the same 4 | 4/4 | 14/14/17 |
| 347 | Zličín → Hostivice, nádraží | :43 (42) | 15:43 16:43 | 15:43 16:43 | 2/2 | 4/5/17 |
| 347 | Hostivice, nádraží → Zličín | :38 (37) | 15:38 16:38 | 15:38 16:38 | 2/2 | 14/16/17 |
| 347 Chýně | Zličín → Chýně, nádraží | :03 (2) | 16:03 17:03 | 16:03 17:03 | 2/2 | 4/4/6 |
| 347 Chýně | Chýně, nádraží → Zličín | :32 (31) | 15:32 16:32 | 15:32 16:32 | 2/2 | 5/7/13 |
| 355 | Dejvická → Únětice | :10 :40 (9) | 15:40 16:10 16:40 17:10 | the same 4 | 4/4 | 15/15/29 |
| 355 | Únětice → Dejvická | :14 :44 (13) | 15:44 16:14 16:44 17:14 | the same 4 | 4/4 | 11/16/30 |
| 356 | Bořislavka → Obchodní centrum Ruzyně | :15 :45 (14) | 14:15 14:45 15:15 15:45 | the same 4 | 4/4 | 14/16/18 |
| 356 | Obchodní centrum Ruzyně → Bořislavka | :26 :56 (25) | 14:26 14:56 15:26 15:56 | the same 4 | 4/4 | 9/14/18 |
| 356 Lichoceves | Bořislavka → Lichoceves | :35 (34) | 14:35 15:35 | 14:35 15:35 | 2/2 | 3/5/12 |
| 356 Lichoceves | Lichoceves → Bořislavka | :59 (58) | 14:59 15:59 | 14:04 14:59 15:59 | 2/2 | 3/3/14 |
| 356 Statenice | Bořislavka → Statenice | :05 (4) | 14:05 15:05 | 14:05 15:05 | 2/2 | 4/4/12 |
| 356 Statenice | Statenice → Bořislavka | :25 (24) | 14:25 15:25 | 14:25 15:25 | 2/2 | 3/3/12 |
| 356 Velká Brána | Bořislavka → Horoměřice, Velká Brána | :25 (24) | 14:25 15:25 | 14:25 14:55 15:25 15:55 | 2/2 | 4/4/7 |
| 356 Velká Brána | Horoměřice, Velká Brána → Bořislavka (knot v lipkách :41) | :40 (39) | 14:40 15:40 | 14:40 15:40 | 2/2 | 4/4/5 |
| 358 | Zličín → Rudná, Hořelice | :23 (22) | 16:23 17:23 | 16:23 17:23 | 2/2 | 3/4/7 |
| 358 | Rudná, Hořelice → Zličín | :01 (0) | 16:01 17:01 | 16:01 17:01 | 2/2 | 2/4/6 |
| 359 | Suchdol → Roztoky, Maxmiliánka | :55 (54) | 15:55 16:55 | 15:55 16:55 | 2/2 | 6/6/11 |
| 359 | Roztoky, Maxmiliánka → Suchdol | :00 (59) | 16:00 17:00 | 16:00 17:00 | 2/2 | 7/8/11 |
| 390 | Smíchovské nádraží → Štěchovice, Třebenice | :25 (24) | 15:25 16:25 | 15:25 16:25 | 2/2 | 6/6/13 |
| 390 | Štěchovice, Třebenice → Smíchovské nádraží | :11 (10) | 15:11 16:11 | 15:11 16:11 | 2/2 | 2/2/12 |
| 409 | Úholičky, železniční zastávka → Velké Přílepy | :05 :35 (4) | 16:35 17:05 17:35 18:05 | the same 4 | 4/4 | 22/22/22 |
| 409 | Velké Přílepy → Úholičky, železniční zastávka | :08 :38 (7) | 16:38 17:08 17:38 18:08 | the same 4 | 4/4 | 20/20/21 |
| 418 | Stodůlky → Jinočany, Logport | :15 :35 :55 (14) | 15:55 … 17:35 (6) | the same 6 | 6/6 | 9/9/32 |
| 418 | Jinočany, Logport → Stodůlky | :03 :23 :43 (2) | 15:43 … 17:23 (6) | 15:40 16:03 16:23 16:43 17:03 17:23 | 6/6 | 6/25/31 |
| 419 | Černošice, železniční zastávka → Karlík | :15 (14) | 16:15 17:15 | 16:15 17:15 | 2/2 | 9/11/15 |
| 419 | Karlík → Černošice, železniční zastávka | :51 (50) | 15:51 16:51 | 15:51 16:51 | 2/2 | 13/13/16 |
| 419 Mokropsy | Černošice → Černošice (round) | :45 (44) | 15:45 16:45 | 15:45 16:45 | 2/2 | 4/5/9 |
| 440 | Štěchovice → Štěchovice, Masečín | :12 (11) | 14:12 15:12 | 14:12 15:12 | 2/2 | 5/6/13 |
| 440 | Štěchovice, Masečín → Štěchovice | :25 (24) | 14:25 15:25 | 14:25 15:25 | 2/2 | 4/4/13 |
| 441 | Jílové, náměstí → Luka p.Medníkem, nádraží | 1:05, 1:45 (4, 44) | 15:05 15:45 | 14:10 15:05 15:45 | 2/2 | 2/3/8 |
| 441 | Luka p.Medníkem, nádraží → Jílové, náměstí | 0:04, 1:22 (21, 63) | 15:22 16:04 | 14:27 15:22 16:04 | 2/2 | 3/4/8 |
| 444 | Kamenice, kulturní dům → Davle, obec | :29 (28) | 16:29 17:29 | 16:29 17:29 | 2/2 | 4/4/9 |
| 444 | Davle, obec → Kamenice, kulturní dům | :27 (26) | 16:27 17:27 | 15:57 16:27 17:27 | 2/2 | 3/3/12 |
| 445 | Jílové, náměstí → Březová-Oleško, Oleško | :48 (47) | 15:48 16:48 | 15:48 16:48 | 2/2 | 9/9/9 |
| 445 | Březová-Oleško, Oleško → Jílové, náměstí | :10 (9) | 16:10 17:10 | 16:10 17:10 | 2/2 | 15/18/20 |
| 445 Vrané | Okrouhlo, Zahořany → Vrané, železniční stanice | :38 (37) | 15:38 16:38 | 15:38 16:38 | 2/2 | 10/10/13 |
| 445 Vrané | Vrané, železniční stanice → Okrouhlo, Zahořany | :03 (2) | 16:03 17:03 | 16:03 17:03 | 2/2 | 10/10/13 |
| 446 | Mníšek, kaple → Kytín, náves | :12 :52 (11, 51) | 15:52 16:12 16:52 17:12 | 15:52 16:11 16:52 17:12 | 4/4 | 11/27/33 |
| 446 | Kytín, náves → Mníšek, kaple | :04 :44 (3, 43) | 15:44 16:04 16:44 17:04 | the same 4 | 4/4 | 11/24/34 |
| 447 | Mníšek, náměstí → Voznice, Chouzavá | 0:03 (62) | 14:03 | 14:03 15:11 | 1/1 | 1/1/3 |
| 447 | Voznice, Chouzavá → Mníšek, náměstí | 0:20 (79) | 14:20 | 14:20 15:29 | 1/1 | 1/1/3 |
| 447 | Mníšek, náměstí → OPS Magdaléna | 0:46 (105) | 14:46 | 14:46 | 1/1 | 1/1/3 |
| 447 | OPS Magdaléna → Mníšek, náměstí | 0:52 (111) | 14:52 | 14:52 | 1/1 | 1/1/3 |
| 448 | Mníšek, náměstí → Lety, K Libří | 0:04, 1:04 (3, 63) | 13:04 14:04 | 13:04 14:04 | 2/2 | 6/6/11 |
| 448 | Lety, K Libří → Mníšek, náměstí | 0:56, 1:46 (45, 115) | 13:46 14:56 | 13:00 13:46 14:56 | 2/2 | 5/5/12 |
| 449 | Mníšek, náměstí → Čisovice, Bojov | 0:35 of 90 (64) | 15:35 | 15:35 | 1/1 | 3/4/8 |
| 449 | Čisovice, Bojov → Mníšek, náměstí | 1:10 of 90 (9) | 14:40 16:10 | 14:40 16:10 | 2/2 | 3/4/8 |
| 632 | Řevnice, nádraží → Hostomice, náměstí | :05 (4) | 16:05 17:05 | 16:05 17:05 | 2/2 | 9/9/11 |
| 632 | Hostomice, náměstí → Řevnice, nádraží | :24 (23) | 16:24 17:24 | 16:24 17:25 | 2/2 | 4/6/10 |
| 664 | Černošice → Vonoklasy, samoobsluha | 1:18 (17) | 13:18 | 13:18 | 1/1 | 4/4/8 |
| 664 | Vonoklasy, samoobsluha → Černošice | 1:39 (38) | 13:39 | 13:39 | 1/1 | 1/1/7 |
| 664 | Černošice → Černošice, škola | 1:51 (50) | 13:51 | 13:51 | 1/1 | 1/1/3 |
| 664 | Černošice, škola → Černošice | 0:09 (68) | 14:09 | 13:09 14:09 | 1/1 | 1/1/2 |
| 664 | Černošice → Vonoklasy, samoobsluha | 0:18 (77) | 14:18 | 14:18 | 1/1 | 4/4/5 |
| 664 | Vonoklasy, samoobsluha → Černošice | 0:31 (90) | 14:31 | 14:31 | 1/1 | 1/2/5 |
| 672 | Všenory, Horní Mokropsy → Hlásná Třebaň | 0:30 of 90 (59) | 15:30 17:00 | 15:30 17:00 | 2/2 | 3/3/8 |
| 672 | Hlásná Třebaň → Všenory, Horní Mokropsy | 1:18 of 90 (17) | 16:18 | 16:18 | 1/1 | 2/2/8 |
| 688 | Mníšek, náměstí → Nový Knín (via nemocnice) | :45 (44) | 14:45 15:45 | 14:45 15:45 | 2/2 | 4/4/15 |
| 688 | Nový Knín → Mníšek, náměstí (direct) | :30 (29) | 14:30 15:30 | 14:30 15:30 16:20 | 2/2 | 2/2/5 |
| 688 | Mníšek, náměstí → Nový Knín (direct) | :15 (14) | 15:15 16:15 | 15:15 16:15 | 2/2 | 5/5/7 |
| 688 | Nový Knín → Mníšek, náměstí (via nemocnice) | :55 (54) | 14:55 15:55 | 14:55 15:55 | 2/2 | 4/4/20 |
| 748 | Mníšek, náměstí → Bratřínov | 1:37 (36) | 13:37 | 13:37 14:37 | 1/1 | 1/1/7 |
| 748 | Bratřínov → Mníšek, náměstí | 1:51 (50) | 13:51 | 13:51 | 1/1 | 1/1/8 |
| 762 | Jesenice [PZ] → Zlatníky-Hodkovice, Na Drahách | :17 (16) | 16:17 17:17 | 16:17 17:17 | 2/2 | 5/5/5 |
| 762 | Zlatníky-Hodkovice, Na Drahách → Jesenice [PZ] | :39 (38) | 15:39 16:39 | 15:39 16:39 | 2/2 | 5/5/6 |

Folding: one entry is evenly spaced on its line's interval: 448's Mníšek, náměstí (0:04 / 1:04 on every 120 = every 60,
Offset 3); the render folds it (as the pilot's 404 Zličín entry). 664's two Černošice → Vonoklasy entries are separate
circuit entries (17 and 77), not one entry. No other multi-slot entry is evenly spaced.

## Audits

- **Step 4:** 97 timed legs, 95 ok, 2 FEWER: 340 Dejvická → Levý Hradec (12 slots, 16 departures), the outstation case, and
  356 Velká Brána Bořislavka → Velká Brána (2 slots, 4 departures), timed at its inbound rate. No EMPTY, no MORE, no
  automatic fit.
- **Branch audit:** 12 legs read at a midpoint, all `[ok]` (310 ×2, 313 ×2, 340 ×2, 356 Velká Brána, 441 ×2, 444, 445 ×2):
  every window slot is a trip of the line's own path ending or starting on it.
- **Path audit:** 1 flag, 445 slot 15:48 = the 15:45 Jílové trip via učiliště, Kovo, Průmyslová instead of Pražská and Za
  Humny (two Jílové paths alternate; both sets of stops are on 341 / 441 / 444 too); named in the why.
- **Run notices:** none (the two "no slot in the window" notices went with 347 Motol and 664 škola).
- **Hub scan** (model departures within 1 min of another line at the same terminal, 14:00–18:00): Zličín 15:22 / 15:23 and
  17:22 / 17:23 (309, 358: real);
  Jesenice :16 / :17 (327, 762: real); Dejvická :10 / :11 (355, 340: real); Mníšek, náměstí 14:03 / 14:04 / 14:05 (447,
  448, 449: real), 14:45 / 14:46 and 16:45 / 16:46 (688, 447: real), 16:03 / 16:04 and 17:04 / 17:05 (model repeats of
  447 / 448 / 449, three different roads; the same pairs leave together at 14:03–14:05 in reality). None fixed.

## Coverage

- **Exceptions (7 stops of okres 290 and 2 Prague stops without a city line), each served all afternoon by a modelled line of
  a neighbouring oblast** — they hold only while those sheets keep those lines; check in the `--final` pass:
  - Rudná, Za Panskou zahradou: 380 (Berounsko), every 30 (308 is not modelled);
  - Velké Přílepy, Pražská and Statenice, Černý Vůl: 316 (Mělnicko), every 10 or more often (409's Suchdol trips are listed);
  - Mníšek pod Brdy, rozcestí Kytín: 317 (Příbramsko), every 30, 19 passings 13–19 (446's Dobříš trips are listed; 319's
    modelled legs do not pass it);
  - Hostivice, Nouzov, Palouky, Průmyslová and Praha, Na Hůrce: 365 and 386 (Kladensko), about every 15 minutes; Praha,
    Zadní Jiviny: 365 towards Stochov (10 passings) (347's Motol trips are listed).
- **Stops of other okresy that only this sheet's lines serve** (for the cross-sheet check): okres Beroun — 632's 17 stops
  (Svinaře, Halouny / škola; Skuhrov (4); Podbrdy; Vižina; Osov (4); Velký Chlumec (3); Hostomice, náměstí; Hostomice, Lštěň,
  rozcestí), Hlásná Třebaň (672), Bubovice, Bubovice, Višňovka, Mořinka (311), Mořina, Trněný Újezd and rozcestí Roblín (313);
  okres Praha-východ — Kamenice, kulturní dům, u Dvora, Těptín, Těptín, u Kozlího kamene (444); okres Příbram — Voznice,
  Chouzavá (447), Malá Hraštice (2), Nová Ves pod Pleší (4), Nový Knín (3) (688).
- **Stops of other okresy uncovered here, served by their own oblast's lines:** the Dobříš and Voznice stops of 446's Dobříš
  trips (317, 319, 392, 420) and the Starý Knín, Mokrovraty and Stará Huť stops of 688's Dobříš trips (361), all Příbramsko.

## Owner checks (0)

None. The one check of the first version (whether to drop six regular destination variants) was deleted on review: Step 5
decides it.

## Open questions and script problems

- **`run_oblast.py` line 40** had a literal newline inside an f-string (`print(f"` + newline + `coverage: …`), a syntax error
  under Python 3.14 from about 05:20 on 2 Nov; the first runs here used a scratch copy with the newline escaped. The
  coordinator fixed the script; every later run used it unchanged.
- **Knot check display:** a leg with `knot_rt` set by hand still shows the knot deviation computed from the median running
  time (313 back: Choteč 3 min off on the card although the model passes Choteč at the slot minute).
- **Terminus alias scope:** `terminus_alias` applies to every line's stops, so 359's path shows Levý Hradec twice where it
  passes Přemyslovská; harmless here, worth a note in the builder.
- **Scratchpad shared between the oblast designers:** my build helper once (05:43) ran another designer's `assemble.py` from
  the shared scratchpad root, which rewrote `oblasti/pribramsko/lines.json` from that designer's own fragments (their
  data, their script). My files moved to a private subfolder at once; the Příbramsko designer should check that file.
- **0-minute turns** (441, 447): the Leave up to question for an engine session, as on the pilot.
- **Task statement vs data:** 407 and 428 are in the Příbramsko oblast, not this one; this oblast has 52 lines as listed.
