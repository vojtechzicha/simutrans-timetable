> 3 Nov 2026: re-checked for branches read by trip ends instead of where trips pass (the 381 Zásmuky case). Where `branch-check-2026-11-03.md` or `branch-review-2026-11-03.md` differs from this file, the 3 Nov files stand (the review over the check).

# Method check: PID Kolínsko (okres Kolín), designed 2 Nov 2026

Bus schedule method v4 (`mirror/pipeline/bus-schedule-method.md`), applied line by line to the 31 designed lines of the
oblast (22 regional lines 435 … 826 and the nine MHD Kolín town lines 235001 … 235009), and since 2 Nov 889 (PID Haló) for
Chotutice. 888 (PID Haló) and XS2 (991002, rail replacement Velký Osek – Kolín) are left out automatically.

- **Data looked at, per line:** `data/derived/reading/<L>.txt` in full (every trip of Mon 2 Nov 2026 with its times at the
  core points, the paths, the 0–5 min chain test, the stops only this line serves), `trips.json` for full stop names and
  paths, `line_class.json`, `../../data/derived/stop_lines.json` and `stop_okres.json`; for 705 at Velký Osek the Nymbursko
  `trips.json` (read only).
- **Candidate search:** for every line both directions were searched with a scratchpad helper (not a pipeline file): every
  interval dividing 1440 up to 480, 1–8 slots placed on the window's real departures, Step 4 per direction (window slots =
  real ±1, ≥ 80 % filled within 3 min), ranked by exact hits over the day (5–23), then within 1, then fewest slots, then
  buses (slot matching with a 3-min wait). Every adopted row was then checked in the builder's `schedule.json` (window
  slots, running time, knot check, waits, need) and the three audits.
- **Typed values** are (real − 61) mod every (every terminus is a loop); each one below was recomputed from its real time.
- **Live map:** at design time the 2 Nov poll held only the morning (5:00–5:30; the afternoon poll runs 12:00–20:00), so
  the reading's "afternoon buses" sections were empty. Every Step 5b pairing below rests on the timetable's 0–5 min chain
  test alone and is marked "open for the live map".
- **Result (after the review of 2 Nov, `review-2026-11-01.md`, and 889 Chotutice):** 32 lines → 39 Simutrans lines,
  71 buses. `run_oblast.py kolinsko`: 77 timed legs, 77 pass Step 4 (0 EMPTY, 0 MORE, 0 FEWER); branch audit 1 [beyond] +
  2 [SLOT-BRANCH], path audit 4 slots — all design choices, explained under 536, MHD Kolín 1 and 889; coverage 473
  afternoon stops, 1 explained exception (Velký Osek, nádraží), 0 outside the kraj uncovered. Owner checks 3.

## Summary

| Line | Simutrans lines | Every | Slots (real minutes) | Buses |
|---|---|---|---|---|
| 435 Klučov – Český Brod – Říčany | 435 | 60 | Klučov :37 / Říčany :00 | 3 |
| 460 Bečváry – Zásmuky – Plaňany – Třebovle | 460; 460 Radim | 240; 480 | 14:02 / 15:25; 12:02 / 13:32 | 1 + 1 |
| 487 Kolín – Uhlířské Janovice – Kácov – Vlašim | 487 | 120 | Kolín 15:33 / Vlašim 16:55 | 3 |
| 491 Český Brod – Doubravčice – Mukařov | 491 | 60 | Český Brod :30 / Mukařov :32 | 2 |
| 534 Kolín – Týnec – Labské Chrčice | 534 | 120 | Kolín 15:06 / Labské Chrčice 15:13 | 2 |
| 535 Kolín – Týnec – Hlavečník | 535 | 120 | Kolín 16:15 / Hlavečník 16:09 | 2 |
| 536 Kolín – Býchory – Žiželice | 536 | 60 | Kolín :57 / Žiželice :29 (Býchory :57) | 3 |
| 537 Kolín – Býchory, škola – Jestřabí Lhota | 537 | 80 | Kolín 13:55 / Jestřabí Lhota 14:31 | 1 |
| 659 Český Brod – Kostelec – Stříbrná Skalice | 659 | 60 | Český Brod :00 / Stříbrná Skalice :37 | 3 |
| 660 Český Brod – Kostelec nad Černými lesy | 660; 660 Doubravčice | 60; 480 | :00 / :02; Kostelec 15:20 (untimed back) | 2 + 1 |
| 661 Český Brod – Lysá nad Labem | 661 | 60 | Český Brod :00 / Lysá :15 | 2 |
| 662 Čelákovice – Český Brod – Kouřim | 662 | 60 | Čelákovice :53 / Kouřim :14 | 3 |
| 675 Kolín – Cerhenice – Pečky | 675; 675 Cerhenice | 120; 480 | 15:03 / 16:14; 16:03 / 17:30 | 1 + 1 |
| 681 Kolín – Uhlířské Janovice – Petrovice II | 681; 681 Petrovice | 60; 480 | :07 / :00; 13:40, 15:30 / 14:06, 15:56 | 2 + 1 |
| 698 Poříčany – Velenka – Semice | 698 (circuit) | 120 | 17:05 / 17:24; 16:05 / 16:22 | 1 |
| 702 Kolín – Červené Pečky – Suchdol | 702 | 60 | Kolín :02 / Suchdol :35 | 1 |
| 706 Žiželice – Kolín – Zásmuky – Uhlířské Janovice | 706 | 60 | Žiželice :03 / Uhlířské Janovice :12 (Kolín :47 / :13) | 4 |
| 707 Kolín circle | 707 | 60 | Kolín :57 | 1 |
| 821 Kolín – Kouřim – Sázava | 821; 821 Kouřim | 120; 120 | 16:02 / Sázava 16:19; 17:02 / Kouřim 16:15 | 2 + 1 |
| 822 Kolín – Kouřim – Český Brod | 822; 822 Klášterní Skalice | 60; 120 | :19 / :30; Kouřim 15:24 / 15:30 | 4 + 1 |
| 824 Kolín – Kouřim – Ždánice | 824 | 60 | Kolín :32 / Ždánice :31 | 2 |
| 826 Pečky – Český Brod – Břežany II | 826 | 120 | Pečky 15:16 (Český Brod 16:00) / Břežany 16:37 | 2 |
| 889 Pečecko, PID Haló (for Chotutice) | 889 Chotutice | 480 | Pečky 20:12 / Kouřim 20:39 | 1 |
| MHD Kolín 1 | MHD Kolín 1 | 20 | Za Jízdárnou :03 / Sendražice :17 | 4 |
| MHD Kolín 2 | MHD Kolín 2 | 20 | Štítary :16 / Šťáralka :15 | 3 |
| MHD Kolín 3 | MHD Kolín 3; MHD Kolín 3 Atletický stadion | 60; 60 | U Vodárny :35 / zimní stadion :05; :05 / :35 | 1 + 1 |
| MHD Kolín 4 | MHD Kolín 4 | 60 | Tesco :47 / Retailpark Ovčáry :30 | 2 |
| MHD Kolín 5 | MHD Kolín 5 | 480 | Polepy 13:44, 15:04, 16:44 / Silo 14:23, 15:43, 17:37 | 1 |
| MHD Kolín 6 | MHD Kolín 6 | 480 | Tesco 13:17 / PZKO-TOYOTA 13:50 | 1 |
| MHD Kolín 7 | MHD Kolín 7 | 480 | U Vodárny 13:00 / PZKO-TOYOTA 14:10 | 1 |
| MHD Kolín 8 | MHD Kolín 8 (circle) | 60 | Karlovo náměstí :20 | 1 |
| MHD Kolín 9 | MHD Kolín 9 | 60 | Štítary :46 / Veltruby :20 (Spálenka :31) | 2 |
| **Total** | **39** | | | **71** (54 regional, 17 MHD) |

## Hand-set anchors (each against the automatic one)

The builder's anchor is the busiest 2 h in 13:00–18:00, or 16:00; the window is anchor −30 to +90, applied to the terminal
time (also for legs read at a knot).

| Line | Auto | Set | Why the automatic window fails |
|---|---|---|---|
| 534 | 16:00 | 15:30 | 15:30–17:30 holds only Kolín 17:26, the one departure off the line's own :06 (13:06, 15:06, 19:06). |
| 659 | 14:20 | 16:00 | The automatic 13:50–15:50 is set by the Kostelec short trips, whose stops are all on 659 (the 282 rule); at 16:00 the line's own :00 / :37 run (4 + 4 exact against 2 + 4 for :55). |
| 661 | 16:00 | 15:00 | In 15:30–17:30 Český Brod changes from :00 (16:00) to :30 (17:30): no hourly row passes, and every 120 would halve an hourly line (mistakes table, 409/411). |
| 702 | 16:00 | 15:00 | 15:30–17:30 holds the hour without a trip (no 17:02, no 17:35): every 60 fills 1 of 2. |
| 706 | 16:00 | 15:30 | The legs are read at Kolín, nádraží but the window is applied to the terminal time: Žiželice 17:33 (Kolín 18:17) falls outside and the 17:03 slot is empty (1 of 2). |
| 822 | 14:10 | 15:30 | The automatic 13:40–15:40 has no Český Brod departure (the first is 15:30) and its Kouřim – Kolín trips (13:54 from Klášterní Skalice, 14:56) are off the line's pattern. |
| MHD Kolín 1 | 16:00 | 15:00 | 15:30–17:30 holds the change from every 20 to every 30 (16:43 → 17:13): every 20 fills 4 of 6 out of Za Jízdárnou. At 15:00 every slot each way is a real departure. |
| 821 | 14:30 | 16:00 | At 14:30 the Sázava return falls on :14 (2 exact, 12:14 and 14:14); at 16:00 it is :19 (5 exact) and every window slot of 821 and 821 Kouřim is a real trip (added after the review). |

## Line by line

### 435 Klučov, Skramníky – Český Brod – Doubek – Říčany, Wolkerova
- (a) Core: Klučov, Skramníky; Český Brod, železniční stanice; Doubek; Říčany, Wolkerova.
- (b) Whole day: Klučov 10:02, 11:32, 13:32, 14:32, then :37 hourly 15:37–17:37, 19:37; Říčany 13:05, then :00 hourly
  14:00–17:00, 19:00. Exact at Český Brod (:00 / :57) and Doubek.
- (c) Step 4 (window 15:30–17:30): Klučov :37 2 slots / 2 real, 2 filled; Říčany :00 2 / 2, 2 filled. Every 120 with two
  slots ties on exact hits; every 60 is the simplest.
- (d) 435 every 60: Klučov typed 36 (:37), Říčany 59 (:00). Path from the afternoon trips (out via Kollárova, back via
  muzeum, Jana Kouly).
- (e) Knots: Český Brod 16:00 / 16:57, Doubek 16:30 / 16:25, all exact.
- (f) Off: Klučov 13:32, 14:32 (5 min), 10:02, 11:32; Říčany 13:05, 10:05, 8:05. Listed: Český Brod – Vrátkov and
  Říčany – Doubek shorts (morning, evening), Český Brod, nemocnice 12:55 → Klučov, Masarykovo náměstí 18:03 → Klučov.
- (g) 3 buses (waits 17 / 6). Chain: 5 of 14 Říčany departures follow a 686 arrival (Praha-východ line): in notes.

### 460 Bečváry, Červený Hrádek – Zásmuky – Plaňany – Třebovle, Miškovice
- (a) Core: Bečváry, Červený Hrádek; Zásmuky, náměstí; Plaňany, náměstí; Třebovle, Miškovice.
- (b) Single school trips. Whole route only twice in the afternoon: 12:02 → 13:30 (via Radim, ObÚ) → 13:32 → Zásmuky
  14:22; 14:02 → 15:24 → 15:25 → 16:53. Plus Zásmuky shorts (14:45, 15:10), Bečváry 16:02 → Polní Voděrady, the
  Plaňany ↔ Třebovle pair 17:30 / 17:39, Bečváry 17:52 → Zásmuky. Own stops: twelve, all on the two through trips;
  Radim, ObÚ only on the 12:02 (it is also on 675's 6:21 morning trip only).
- (c) One every-240 line holds either round with 1 bus; with both rounds in one line, or the 12:02 path in the 14:02 slot
  (88 min, arrives 15:30 for a 15:25 return), it needs 2 buses. Step 4 at the anchor 14:00 (13:30–15:30): 460 Bečváry 1
  slot / 1 real; Třebovle 1 / 2 (13:32 and 15:25), filled.
- (d) 460 every 240: Bečváry typed 61 (14:02), Třebovle 144 (15:25), 1-minute turn. 460 Radim every 480 (`via` Radim,
  ObÚ): Bečváry 181 (12:02), Třebovle 271 (13:32, read to Zásmuky with `core_to`; the game bus runs on to Bečváry). Its
  out leg has no slot in the window (the 12:02 stands for itself; named in the why).
- (e) Knots: 460 Zásmuky 14:30, Plaňany 15:16 exact, Třebovle 15:27 against 15:24 (the median running time includes the
  Radim path); back Plaňany 15:33, Zásmuky 16:25, Bečváry 16:53 exact.
- (g) 1 + 1. Radim is a separate village (not a roadside stop), so it is kept by the "serve every place" rule (in notes,
  not an owner check).

### 487 Kolín – Uhlířské Janovice – Kácov – Vlašim, Terminál
- (b) Kolín 9:33, 11:33, 13:33, 15:33, 17:23, 19:23; Vlašim 10:55, 12:55, 14:55, 16:55; UJ shorts 14:18 / 15:05; morning
  Kácov / Kladruby trips.
- (c) Window 15:30–17:30: Kolín 1 slot / 2 real (15:33, 17:23), filled; Vlašim 1 / 1. Every 120 :33 / :55: 4 + 4 exact.
- (d) Typed 32 (15:33) / 114 (16:55). 92 min each way. (e) Uhlířské Janovice 16:10 / 17:50, Kácov 16:33 / 17:27 exact.
- (f) Off: 17:23, 19:23 (10 min early), 5:38. (g) 3 buses (waits 110 at Vlašim, 66 at Kolín). Vlašim chains with 790,
  426, 455 (3–4 of 9): in notes. Kácov, Zderadiny / Zderadinky / rozcestí k železniční stanice (okres Kutná Hora) and
  Bečváry, Poďousy, Kořenice, Chotouchov are 487's own: on the line.

### 491 Český Brod – Doubravčice – Mukařov [PH]
- (b) Český Brod :30 hourly 14:30–18:30 (13:25); towards Český Brod past Mukařov :32 (13:32–16:32 from Louňovice,
  I.hráz 3 min earlier; 17:32, 18:32 from Mukařov).
- (c) Window: 2 / 2 filled each way; :30 / :32 7 + 8 exact.
- (d) Typed 29 / 31; 26 min each way. Far end modelled at Mukařov: Louňovice, I.hráz is 3 min beyond and served by 381,
  382, 387 (other sheets), so the extension would add the stop only (the 314 rule is about choosing a branch, here the
  slot trips pass Mukařov).
- (e) Doubravčice, Mukařov, Český Brod exact. (f) Off: 13:25, 12:25, 11:25, 9:55; 20:07. (g) 2 buses.
- Step 5b: 491 arrivals :58 → 660 :00 and 660 arrivals :30 → 491 :30 (4 of 6 each way in 13–19, 0–2 min), but 660's :00
  departures follow 661's :55 arrivals just as often (4 of 5), so the timetable cannot say which line feeds 660. Kept apart;
  a 491 + 660 circuit every 60 (3 buses instead of 4) is in the notes, open for the live map (not an owner check since the
  review).

### 534 Kolín – Týnec nad Labem – Labské Chrčice
- (b) Kolín 11:06, 13:06, 15:06, 17:26, 19:06; Labské Chrčice 13:13, 15:13, 17:13, 19:13 (odd hours); morning Týnec
  shorts.
- (c) At the set anchor 15:30 (15:00–17:00): 1 / 1 filled each way; :06 / :13 odd 4 + 4 exact. At 16:00 the only Kolín
  departure in the window is 17:26.
- (d) Typed 5 (15:06) / 12 (15:13). 41 min. (g) 2 buses (waits 86 / 72). The only line to Labské Chrčice and Labské
  Chrčice, ObÚ (Pardubický kraj): served.

### 535 Kolín – Týnec nad Labem – Hlavečník
- (b) Kolín 12:15, 14:20, 16:15, 18:15 (+ 15:35 → Konárovice, ObÚ); Hlavečník 12:09, 14:09, 16:09.
- (c) Window 1 / 1 each way; every 120 :15 / :09: 4 + 3 exact. (d) Typed 74 / 68; 56 min.
- (f) Off: Kolín 14:20 (5 min). Listed: 15:35 → Konárovice, ObÚ. (g) 2 buses. Hlavečník and Hlavečník, u pomníku
  (Pardubický kraj), Bělušice and Uhlířská Lhota are 535's own: served.
- Step 5b: 535 arrives Kolín :05 and 534 leaves :06 (13:05 → 13:06, 15:05 → 15:06); 534's :54 arrivals precede 535's
  :15 / :20. One 534/535 circuit every 120 (Kolín – Labské Chrčice – Kolín – Hlavečník – Kolín, 41 + 86 + 41 + 21 + 56 +
  58 + 56 + 1 = 360) needs 3 buses instead of 4: pooling, owner checks; the plates will tell. The timetable chains the trips
  into three rounds (the evidence in the check): Hlavečník 14:09 → Kolín 15:05 → 15:06 → Labské Chrčice 15:47 → 17:13 →
  Kolín 17:54 → 18:15 → Hlavečník; Labské Chrčice 13:13 → Kolín 13:54 → 14:20 → Hlavečník 15:16 → 16:09 → Kolín 17:05 →
  17:26 → Labské Chrčice 18:07 → 19:13 → Kolín; Kolín 13:06 → Labské Chrčice 13:47 → 15:13 → Kolín 15:54 → 16:15 →
  Hlavečník 17:11.

### 536 Kolín – Býchory – Žiželice
- (a) Core: Kolín, nádraží; Býchory (the knot both paths pass); Žiželice, Loukonosy; Žiželice, náměstí.
- (b) Out of Kolín 14:40 (direct), then :57 hourly: 15:57 (loop), 16:57 (direct), 17:57 (loop), 18:47 (direct), 19:57
  (loop). From Žiželice 15:26 (loop), 16:29 (direct), 17:19 (loop), 18:29 (direct); past Býchory 16:02, 16:57, 17:57,
  18:57. The loop path (Radovesnice II, Rozehnaly, Hradišťko II, škola, Pod Vinicí, Loukonosy) holds four of 536's own
  stops; the direct path passes Žiželice, Končice (also on 706).
- (c) Candidates: per path every 120 (Loukonosy: Kolín 15:57 / Žiželice 17:19, 2 buses; Končice: 16:57 / 16:29, 2 buses),
  or one hourly line. Hourly back read at Žiželice :29 fails (17:29 slot has 17:19 10 min off); read at Býchory :57 with
  the direct running time (`knot_rt` 28, Žiželice :29) every window slot is real (16:29, 17:29 = the 17:19 loop trip
  passing Býchory 17:57), 2 / 3 filled.
- (d) 536 every 60, a circuit as 329 Květnice: out by the loop (`stops_via` Loukonosy, rt 58), back direct (`stops_via`
  Končice, rt 46, read at Býchory). Typed 56 (:57) / 28 (:29).
- (e) Býchory out 16:15 / 17:15 exact. The builder's knot check shows 8 min at Žiželice and Kolín: it takes the median
  offset over both paths (display only; the slot trips' own times are exact at Kolín and Býchory).
- Audits: branch [beyond] and path flag on the 17:29 back slot (a loop trip on the direct leg) — the design, named in the
  why. The path-variant rule (one circuit out on one path, back on the other; 329 Květnice) decides it, so the two-line
  option (4 buses) is a sentence in the note, not an owner check (since the review).
- (f) Off: Kolín 14:40, 18:47; Žiželice 15:26 (Býchory 16:02, 5 min). Listed: Býchory 13:32 → Kolín, Loukonosy 13:55 →
  Kolín. (g) 3 buses (waits 34 / 42).

### 537 Kolín – Konárovice – Býchory, škola – Jestřabí Lhota
- (b) One bus 12:35–15:45: Kolín 12:35 → JL 13:11 → 13:11 → Kolín 13:50 → 13:55 → JL 14:31 → 14:31 → Konárovice, ObÚ
  14:48 → 14:52 → JL 15:06 → 15:06 → Kolín 15:45 (0-minute turns at JL, 4 of 4).
- (c) Anchor 13:40 (13:10–15:10): Kolín 1 departure (13:55), Jestřabí Lhota 3 (13:11, 14:31, 15:06). Every 480 or
  240 with one slot fails the count at JL (1 slot for 3); every 120 at JL 15:06 leaves 13:06 empty. Every 80 (the real
  80-min spacing of Kolín 12:35 / 13:55 and JL 13:11 / 14:31): Kolín 1 / 1, JL 2 / 3, all filled.
- (d) Typed 54 (13:55) / 10 (13:11, 14:31), `lay` 0 at JL; the JL leg is read to Konárovice, ObÚ (`core_to`) because the
  14:31 ends there. (e) Konárovice 14:17 / 13:28 / 14:48 exact; Kolín 15:10 shows 35 (the 14:31 ends at Konárovice).
- (f) Off: JL 15:06 → Kolín, 6:30, 7:06 morning. (g) 1 bus. Only service of Býchory, škola (not a roadside stop).

### 659 Český Brod – Kostelec nad Černými lesy – Stříbrná Skalice
- (b) Český Brod → Stříbrná Skalice 12:25, 13:55, 14:55, 16:00, 17:00 (to the station), 18:00, 19:00 (to the station);
  Stříbrná Skalice, náměstí 13:33, 14:37, 15:37, 16:37, 17:37; Kostelec shorts 13:50, 14:50 → Český Brod, 15:25 →
  Kostelec, 12:58 → Krupá; 19:37 → Krupá.
- (c) Anchor 16:00 (set): :00 / :37 2 / 2 filled each way, 4 + 4 exact. At the automatic 14:20 :55 / :37 passes with
  2 + 4.
- (d) Typed 59 / 36; 71 min each way; out by the 13:55 / 14:55 path (Prusice, Nučice loop); 16:00 and 18:00 run via
  Prusice, rozcestí (also on 387), the 17:00 ends at the station (`core_to`).
- (e) Kostelec, the station, Český Brod exact. (f) Off: 13:55, 14:55 (5 min), 12:25; 13:33. (g) 3 buses.

### 660 Český Brod – Tuchoraz – Kostelec nad Černými lesy (+ Doubravčice)
- (b) Český Brod 14:15, 15:10, then :00 16:00–20:00; Kostelec 13:47, then :02 15:02–18:02, 19:07. Doubravčice trips:
  Kostelec 13:45 → Doubravčice 14:02, 15:20 → 15:37; Doubravčice 7:15 → Kostelec.
- (c) 2 / 2 filled each way; :00 / :02 7 + 10 exact. (d) 660 typed 59 / 1, 28 min. 660 Doubravčice every 480, typed 379
  (15:20), untimed back (19 min, the 7:15 path; where the real bus goes is open for the live map); no slot in the window
  (named in the why).
- (f) Off: Český Brod 14:15, 15:10, 12:55; Kostelec 13:47, 12:32, 19:07; Doubravčice 13:45. (g) 2 + 1.
- Štíhlice (village stop, okres Praha-východ; 7:15 to Kostelec, 13:45 and 15:20 from Kostelec) is served by no other line
  on any sheet: the sheet's one coverage owner check — keep 660 Doubravčice (1 bus) or an exception (Štíhlice,
  Doubravčická, the village's other stop, on 491 hourly).

### 661 Český Brod – Lysá nad Labem
- (b) Lysá :15 hourly 14:15–18:15 (19:25); Český Brod 12:25, 13:55, 15:00, 16:00, 17:30, 18:30.
- (c) At 15:00 (set): :00 / :15 2 / 2 filled each way. At 16:00 no hourly row passes (Český Brod 16:00, 17:30).
- (d) Typed 59 / 14; 40 min. (f) Off: Český Brod 13:55, 17:30, 18:30 (the last two are the 660 buses arriving at :30);
  Lysá 12:50, 19:25. Listed: Lysá 15:40 → Semice 15:53, Semice 16:02 → Lysá 16:15; evening Starý Vestec trips.
- (g) 2 buses. Bříství, Bříství, Svárov, Lysá nad Labem, Litol, u mostu (okres Nymburk) are 661's own: on the line.

### 662 Čelákovice, Toušeňská – Mochov – Český Brod – Kouřim
- (b) Čelákovice :53 hourly 12:52–18:53; Kouřim :14 hourly 14:14–19:14; the bus leaves Kouřim on arrival (8 of 13).
- (c) 2 / 2 filled each way; 7 + 6 exact. (d) Typed 52 / 13, `lay` 0 at Kouřim (0-minute turn); 81 / 79 min.
- (f) Listed: Český Brod → Čelákovice 12:43, 13:44; Čelákovice → Vykáň 15:23, 16:23; the Kounice – Mochov shuttle
  (licence 231662, 13:23–18:57, about hourly): Kounice is on 661, Černíky … Mochov on 662; 12 of its 13 Mochov arrivals
  go on as 354 (Praha-východ). (g) 3 buses.

### 675 Kolín – Cerhenice – Pečky (+ Cerhenice shorts)
- (b) Kolín :03 hourly: 13:13, 15:03, 17:03 to Pečky; 14:03, 16:03, 18:03 to Cerhenice, Náměstí Míru. Pečky 14:14,
  16:14, 18:14. From Cerhenice only 17:30 (and 8:20, 12:35 Cerhýnky).
- (c) 675: window 1 / 1 each way, 3 + 3 exact. 675 Cerhenice: an outstation shape (3 out, 1 back in 13–19), so by the
  outstation rule it is timed at the inbound rate: one real return a day, the 402B case (Step 8), every 480 on the real
  16:03 / 17:30 round (every 240 ties on exact hits but adds a 12:03 / 13:30 round with no real trip). Its return has no
  slot inside the line's 15:30–17:30 window (17:30 is the edge): the sparse case, the why names the trip.
- (d) 675 typed 2 (15:03) / 73 (16:14), 43 min. 675 Cerhenice every 480, typed 422 (16:03) / 29 (17:30), 27 min, `notvia`
  Pečky both ways (the Pečky trips pass Cerhenice and belong to 675).
- (f) Off: Kolín 13:13 (10 min); Kolín 14:03 and 18:03 → Cerhenice (their buses end there; next trips open for the live
  map: 702 and 821 arrivals at Kolín :58 precede 675's :03). (g) 1 + 1.

### 681 Kolín – Uhlířské Janovice (+ Petrovice II)
- (b) Kolín :07 hourly 12:07–16:07, 18:07–22:07 (no 17:07); Uhlířské Janovice :00 (14:00, 15:00, 17:00, 19:00; no
  16:00); 0-minute turns at UJ (5 of 14). Petrovice II: UJ 13:40, 15:30 → Losiny; Losiny 14:06, 15:56 → UJ; 12:36 →
  Kolín.
- (c) Anchor 14:30 (automatic): 2 / 2 filled each way, 9 + 8 exact. Petrovice: every 480 with both afternoon rounds,
  Uhlířské Janovice 13:40, 15:30 / Losiny 14:06, 15:56, holds all four trips exact (4 against 2 for every 120 at 15:30 /
  15:56, which also put 13:40 / 14:06 10 min off) with the same bus: Step 4 rule 3. Window: 1 / 1 and 2 / 2 filled.
- (d) 681 typed 6 / 59, `lay` 0 at UJ; rt 63 back (the 14:00 / 15:00 trips; the 17:00 takes 53: the knot check's 10 min
  at Kolín is that median, display only). 681 Petrovice typed 279, 389 / 305, 415, 2-min turns, 1 bus (60 min at
  Uhlířské Janovice between the rounds).
- (g) 2 + 1. Petrovice II and its villages, Onomyšl, Suchdol, Dobřeň / Solopysky / Malenovice, Kochánov, Zbizuby, Vlková
  (okres Kutná Hora) are served only by 681: on these lines.

### 698 Poříčany – Velenka – Semice
- (b) One bus: Poříčany 13:00, 14:00 (Semice), then 15:05 Semice, 16:05 Velenka, 17:05 Semice, 18:05 Velenka, 19:05
  Semice, 20:05 Velenka; back Semice 13:19 (via Hradištko), 14:24, 15:24, 17:24, 19:24; Velenka 16:22, 18:22. 0-minute
  turns at Semice (7 of 9).
- (c) One every-60 line fails (Velenka 16:22 against a Semice :24 slot, 12 min). The circuit every 120 with Poříčany twice
  (Plzeň 4 precedent) is the bus's own sequence: each leg 1 / 1 filled.
- (d) Typed 4 (17:05 → Semice), 23 (Semice 17:24, `lay` 0), 64 (16:05 → Velenka, `notvia` Semice), 81 (Velenka 16:22,
  `notvia` Semice). 1 bus (pattern_need; 19 + 0 + 19 + 22 + 9 + 8 + 9 + 34 = 120).
- (f) Off: 13:00, 14:00 → Semice; 13:19, 14:24 back. The Hradištko stops are also on 443 (Nymbursko).

### 702 Kolín – Červené Pečky – Suchdol
- (b) Kolín :02 hourly (no 17:02; 14:02 only to Opatovice), Suchdol :35 (no 17:35; 14:44 from Opatovice).
- (c) At 15:00 (set): 2 / 2 filled each way; 7 + 7 exact. Both legs read at Opatovice (`core_to` out, `knot` back).
- (d) Typed 1 / 34; 23 min. (g) 1 bus (waits 10 / 4). Nine own stops (Nebovidy, Červené Pečky): on the line.

### 706 Žiželice – Kolín – Zásmuky – Uhlířské Janovice
- (b) At Kolín, nádraží towards Uhlířské Janovice :47 (13:47–16:47, then 18:17, 19:17); towards Žiželice :13
  (15:13–19:13). At the ends Žiželice 12:56, 14:03, 15:03, 16:03, 17:33, 18:33; UJ 14:18, 15:12, 16:12, 17:18, 18:18.
- (c) Read at Kolín (both directions pass it; trips starting at Kolín count as mixed origins on the line's own path):
  2 / 2 filled each way at 15:30 (set); 5 + 7 exact at the knot.
- (d) Typed 2 (Žiželice :03 = Kolín :47 − 44) / 11 (UJ :12 = Kolín :13 − 61); 105 min each way.
- (e) Kolín exact both ways; Zásmuky exact; UJ 16:48 against 16:42 for the 15:03, which skips Vavřinec (99 min; named in
  the why since the review).
- (f) Off: Žiželice 17:33, 18:33 (Kolín 18:17, 19:17, 30 min). UJ 14:18, 17:18, 18:18 leave 6 min after :12 but pass
  Kolín at :13, so they are on the pattern at the knot. Listed: PZKO-TOYOTA 14:31 → Žiželice, Skvrňov / Zásmuky shorts. (g) 4 buses.

### 707 Kolín circle (Starý Kolín – Svatý Mikuláš – Hlízov)
- (b) Kolín 12:57, 13:57 (circle 56 min), 14:57 (to Hlízov, u váhy); 5:32, 6:30 morning. Window 13:50–15:50: 2 / 2
  filled (the 14:57 read to Hlízov with `core_to`). Every 60 typed 56, 1 bus. Only service of Starý Kolín and Svatý
  Mikuláš, Svatá Kateřina.

### 821 Kolín – Kouřim – Horní Kruty – Sázava
- (b) Kolín :02 hourly: even hours to Sázava (12:02–18:02), 15:02 to Horní Kruty, 17:02 to Kouřim. Back past Kouřim at
  :15 every hour: Sázava 14:14, 16:19, 18:19 (Kouřim :15 odd), Ždánice, u Jánů 14:00 and Horní Kruty 15:39 (Kouřim
  14:15, 16:15). Horní Kruty 17:44 → Kouřim 18:15.
- (c) Anchor 16:00 by hand (since the review): there the Sázava return is :19, 5 exact over the day (5:19, 8:19, 10:19,
  16:19, 18:19), against :14's 2 at the automatic 14:30; window 15:30–17:30: 821 Kolín 16:02, Sázava 16:19; 821 Kouřim
  Kolín 17:02 (a real Kouřim-ender), Kouřim 16:15 (Horní Kruty 15:39) — 1 / 1 each, all real.
- (d) 821 typed 61 (16:02) / 78 (16:19), 104 / 99 min, 2 buses (104 + 33 + 99 + 4 = 240). 821 Kouřim typed 1 (17:02) /
  74 (16:15), `notvia` Sázava, turning at Kouřim (1 bus). Of its slot trips, Kolín 15:02 → Horní Kruty 16:21 and Horní
  Kruty 15:39 → Kolín 16:58 run beyond Kouřim (both chain with 772, 2 of 2), Kolín 17:02 → Kouřim 17:45 and Horní Kruty
  17:44 → Kouřim 18:15 really end at Kouřim. Running the same slots to Horní Kruty needs 2 buses (78 min there): owner
  check.
- (f) Off: Sázava 12:14, 14:14 (5 min early). Listed: Horní Kruty 17:44 → Kouřim; Ždánice, u Jánů 14:00 → Horní Kruty.

### 822 Kolín – Plaňany – Kouřim – Český Brod (+ Klášterní Skalice)
- (b) Kolín 12:36 (to Vitice), 13:19, 14:19, 15:19 (to Kouřim), 16:19, 17:24, 18:24 (Kouřim), 19:09 (Kouřim); Český Brod
  12:25, 15:30, 16:30, 17:30, 18:30 (Kouřim), 19:30 (Kouřim); Kouřim 14:56 → Kolín; Klášterní Skalice 13:54 → Kolín;
  the 4-min Kouřim ↔ Klášterní Skalice shuttle 13:45 / 15:24 / 17:24 (back 15:30, 17:30), 6 of 6 turning at once.
- (c) At 15:30 (set): 2 / 2 filled each way (both legs read to Kouřim, `core_to`), 4 + 5 exact. Shuttle every 120:
  15:24 and 17:24 / 15:30 and 17:30, 2 + 2 exact.
- (d) 822 typed 18 / 29; 96 / 89 min; 4 buses (waits 35 at Český Brod, 20 at Kolín). 822 Klášterní Skalice typed 23 /
  29, 1 bus. (e) The builder's 7 min at Kolín back is the all-day median (96) against the window's 89, display only.
- (f) Off: Kolín 17:24, 18:24 (5 min), 19:09, 12:36; Český Brod 12:25; Kouřim 14:56, 13:54 from Klášterní Skalice;
  shuttle 13:45.

### 824 Kolín – Toušice – Kouřim – Ždánice
- (b) Kolín :32 hourly 14:32–16:32 (13:02; 17:32 to Kouřim), Ždánice :31 hourly 14:31–17:31. (c) 2 / 2 filled each
  way. (d) Typed 31 / 30; 57 min; 2-min turn at Ždánice as in the timetable. (g) 2 buses.

### 826 Pečky – Klučov – Poříčany – Český Brod – Břežany II
- (b) Towards Břežany through Český Brod 14:00 (from Poříčany 13:19), 14:30 (Pečky 13:48), 16:00 (15:15), 17:00 (16:15);
  Břežany II 13:07, 14:37, 16:37 (to Klučov, Skramníky), 18:07.
- (c) Out read at Český Brod (`knot`; the Poříčany start is on the line's own path), back to Český Brod (`core_to`).
  Every 120 :00 / :37 even hours: 2 + 2 exact, 1 / 2 filled each way at the automatic anchor 13:30; every 90 ties on hits
  and buses, 120 is the longer interval.
- (d) Typed 15 (Pečky 15:16 = Český Brod 16:00 − 44) / 96 (16:37); 67 / 79 min. (g) 2 buses (waits 80 / 14).
- (f) Off: Pečky 13:48, 16:15; Břežany 13:07, 18:07. Listed: Poříčany school trips 12:58, 14:35; Pečky 19:15 → Klučov.

### 889 Pečecko, PID Haló — 889 Chotutice (added 2 Nov)
- (a) Core: Pečky, železniční stanice; Chotutice, Průběžná; Plaňany, náměstí; Kouřim.
- (b) Evening only, on demand with fixed times: Pečky 20:12, 22:08, 0:08 → Dobřichov → Radim → Chotutice → Radim, ObÚ →
  Plaňany → Vrbčany → Třebovle, Miškovice → Klášterní Skalice → Kouřim (27 min); Kouřim 20:39, 22:39 → Pečky (26 min), the
  bus turning at Kouřim in 0 min (2 of 2); Pečky – Ratenice – Poděbrady trips 21:08–0:42. Chotutice has no other bus at any
  hour; by the owner's PID Haló decision of 2 Nov 2026 (places whose only service is Haló get a line from its fixed trips,
  at most every 480) it is modelled.
- (d) Every 480 on the 20:12 / 20:39 round: Pečky typed 191, Kouřim 218, `lay` 0 at Kouřim. The sim window is set to
  20:00–22:00 where the fixed trips run (the line has no afternoon trip; the 16:00 window would test nothing): 1 / 1 filled
  each way. The game path keeps the named stops only (`stops` set by hand: Chotutice, Průběžná, Radim, ObÚ, Pečky, Hynkův
  mlýn on the way back); the on-demand virtual stops (virtuální zastávka) are left out, so the path audit flags both slots
  (their trips pass those points) — by design.
- (f) Off: Pečky 22:08, Kouřim 22:39 and 0:08 (the second and third rounds); the Poděbrady trips (Ratenice is also on 498,
  Vrbová Lhota is okres Nymburk). (g) 1 bus.

### MHD Kolín 1 (235001)
- (b) Za Jízdárnou :03 / :23 / :43 13:03–16:43 (14:43 and 15:43 replaced by Zibohlavy trips 14:37, 15:37), then 17:13,
  17:43 (to nádraží), 18:13; Sendražice, II :17 / :37 / :57 13:18–17:17 (13:58 and 14:57 to Zibohlavy), then 17:48,
  18:49; nádraží → Za Jízdárnou shorts.
- (c) At 15:00 (set): every 20, 6 slots / 6 real, 6 filled each way (out read at nemocnice, back to nemocnice). At 16:00
  every 20 fills 4 of 6 out.
- (d) Typed 2 / 16; 29 / 31 min; 4 buses (waits 5 / 15).
- Audits: [SLOT-BRANCH] ×2 and one path flag: two of the six window slots each way are the Zibohlavy trips, read at
  nemocnice. Folded into the trunk's slots as 452 in 451's (HKO): Kolín, Zibohlavy keeps 706 hourly (:13 / :47 at Kolín).
  A separate Zibohlavy line would leave the trunk's :43 slots without a trip (fails Step 4) for a stop already served.

### MHD Kolín 2 (235002)
- (b) Every 20 13:16–16:36 / 13:36–16:55, then every 30. Automatic anchor 14:50: 6 / 6 filled each way. Typed 15 / 14;
  21 / 20 min; 1-min turn at Štítary (25 of 38). 3 buses. Off: 17:01–18:31 (every 30), Štítary – nádraží shorts.

### MHD Kolín 3 (235003)
- (b) U Vodárny :05 (via Atletický stadion, 30 min, from 12:05) and :35 (direct, 27 min); zimní stadion :05 and :35;
  31 of 31 arrivals at zimní stadion leave again within 0–5 min: the :05 bus leaves at :35 (0 min), the :35 bus at :05.
- (d) Two lines every 60, one per path: MHD Kolín 3 (`notvia` Atletický stadion) typed 34 / 4; MHD Kolín 3 Atletický
  stadion (`via`) typed 4 / 34, `lay` 0. Both 2 / 2 filled each way. 1 + 1 bus. Atletický stadion (own stop) on the
  second line, Tovární, Hřbitovní, Veltrubská, Dymokurská, tiskárny, Táboritská, u nemocnice on both.

### MHD Kolín 4 (235004)
- (b) Tesco :47 hourly, Retailpark Ovčáry :30 hourly (12:30, 15:30–19:30; 13:37, 14:34 off). 2 / 2 filled each way.
  Typed 46 / 29; 36 / 44 min. 2 buses. No own stop.

### MHD Kolín 5 (235005)
- (b) Polepy 13:44, 15:04, 16:44 → Říční; Silo 14:23, 15:43, 17:37 → Polepy; the bus goes Říční → Silo (12 min).
- (c) Every 480 with three slots each way holds all six afternoon trips exactly (6 against 3 for every 180) with the same
  bus: Step 4 rule 3, the 290 precedent. Window 15:30–17:30: Polepy 16:44 1 / 1, Silo 15:43 1 / 1. The two ends are
  different stops, so the legs do not chain (pattern_need).
- (d) Polepy typed 283, 363, 463 (13:44, 15:04, 16:44); Silo typed 322, 402, 36 (14:23, 15:43, 17:37; the last wraps past
  midnight), `stops_via` Kolín, Spel on the Silo leg (only the 14:23 and 15:43 serve Spel, the line's own stop; the 17:37
  skips it), `lay` 0 at Silo (the 12-min reposition from Říční is the real turn). 1 bus. Own stops Silo, Spel, U Borků: on
  the line.

### MHD Kolín 6 (235006)
- (b) Shift trips around 5:00–6:20, 13:17–15:11, 21:03–23:03 (see note). Window 13:10–15:10: 1 slot / 2 real each way.
- (d) Every 480: Tesco typed 256 (13:17), PZKO-TOYOTA 289 (13:50, via PZKO CEVA, its only service). 1 bus. Off: 13:37,
  14:45, 14:15 → nádraží, the CEVA shuttle, evening trips; 5:18 is 1 min off the 5:17 repeat.

### MHD Kolín 7 (235007)
- (b) U Vodárny 5:00, 13:00, 21:00; PZKO-TOYOTA 6:15, 14:10, 22:15: exactly every 8 h. Every 480: typed 239 / 309. The
  out leg ends at PZKO TOYOTA TSUSHO so the NIPPON / TSUSHO loop is on the line (the trip passes PZKO-TOYOTA twice, and
  the builder takes the first passing). 1 bus.

### MHD Kolín 8 (235008)
- (b) Karlovo náměstí :20, 9:20–16:20, a 30-min circle; 17:20 ends at U Vodárny (`core_to`). 2 / 2 filled; 9 exact.
  Every 60 typed 19. 1 bus.

### MHD Kolín 9 (235009)
- (b) Štítary 15:46 (to Veltruby), 16:46, 17:46 (to Spálenka); Veltruby 14:50, 16:20 (0-minute turn, 3 of 3), Spálenka
  17:31, 18:31 → Štítary.
- (c) Every 60 (since the review): Štítary :46, back read at the knot Spálenka :31 (Veltruby :20). With the window applied
  at the terminal, as the builder does, the out slots 15:46, 16:46 and the back slots 16:20, 17:20 (= Spálenka 17:31) are
  all real trips (2 / 2 each way). My first check said "every 60 fails back (15:31 slot empty)": that applied the window at
  the knot, wrongly. Every 120 had kept only half the afternoon (16:46 and 17:31 off).
- (d) Typed 45 (:46) / 19 (Veltruby :20 = Spálenka :31 − 11), `lay` 0. 2 buses (34 + 0 + 39 + 47 = 120), as the two real
  buses. The 16:46 and 17:46 end at Spálenka and run on 6 min to Veltruby in the game; the 17:31 and 18:31 start at
  Spálenka (named in the why).

## Shared stops: Step 5b, interleaving, bunching
- **Kolín, nádraží** (most of the oblast's lines): the game departures are the real minutes — :02 (702, 821), :03 (675), :06 (534 odd),
  :07 (681), :15 (535 even), :19 (822), :32 (824), :33 (487 odd), :55 / :35 (537), :57 (536, 707), 706 passing :47 /
  :13. Same-minute pairs (702/821 at :02, 536/707 at :57) are real and leave on different roads. Every Simutrans line is
  balanced in its window; the real imbalances (675 Cerhenice 3 out / 1 back; 821's Kouřim-ending trips) are buses going
  on to other lines, open for the live map.
- **Český Brod, železniční stanice**: :00 (659, 660 — both real, same first stops, as in the timetable; 661 15:00 /
  16:00; 435 and 826 passing), :30 (491, 822), 662 passing :44. Pairings 491 ↔ 660 and 660 ↔ 661 (notes, live map).
- **Kouřim**: 662 :14 (0-minute turn), 821 :45 / :15, 822 :18 / :07, 824 :17 / :43, Klášterní Skalice shuttle :24 /
  :34 — no shared minute that the timetable does not have.

## Coverage
- Okres Kolín: every stop served 13:00–19:00 is on a modelled line except Velký Osek, nádraží (exception: on this sheet
  only XS2 serves it; 705, Nymbursko sheet, passes it all afternoon). No roadside exception was needed, so there is no
  sheet-wide roadside owner check.
- Outside the Středočeský kraj: Labské Chrčice, Labské Chrčice, ObÚ (534), Hlavečník, Hlavečník, u pomníku (535): served.
- **Other Středočeský okresy, served only by this sheet's lines** (for the `--final` pass): Kutná Hora — Kácov,
  Zderadinky; Kácov, Zderadiny; Kácov, rozcestí k železniční stanice (487); Onomyšl, Křečovice, rozcestí; Onomyšl,
  Miletín; Onomyšl, Rozkoš; Petrovice II; Petrovice II, Boštice / Losiny / Nové Nespeřice / Tlučeň; Suchdol, Dobřeň;
  Suchdol, Malenovice, rozcestí; Suchdol, Solopysky; Uhlířské Janovice, Kochánov; Zbizuby, Vlková (681); Rašovice,
  Jindice; Rašovice, Mančice, rozcestí (487, 681); Svatý Mikuláš, Svatá Kateřina (707). Praha-východ — Konojedy (3),
  Kostelec nad Černými lesy, Chaloupky / Komenského / Svatbín, Oplany (2), Prusice, Vlkančice (5) (659); Kostelec nad
  Černými lesy, Truba, Kozojedy [PH], Štíhlice (660); Čelákovice, Sedlčánky (662); Štíhlice, Doubravčická (491).
  Nymburk — Bříství, Bříství, Svárov, Lysá nad Labem, Litol, u mostu, Kounice (661); Chrást [NB], Chrást, hostinec,
  Hradištko, Kersko U Pramene (698); Hořany, Milčice, křižovatka (826); Vykáň (662). All are on modelled lines here.
- **PID Haló** (owner, 2 Nov 2026: "Yes, model a line" where Haló is a place's only 13:00–19:00 service): 888
  Českobrodsko and 889 Pečecko run only 20:12–0:42, so `stop_lines.json` (afternoon service) has no 888 / 889 entry and no
  stop of okres Kolín qualifies. The stops only they serve are on-demand virtual stops (virtuální zastávka) in villages whose
  other stops are on modelled lines, Pečky, Hynkův mlýn (also on 675 at 6:21), Kostelec nad Černými lesy, Trativody and u
  křížku (okres Praha-východ) and the village of Chotutice (okres Kolín), which no line serves at any hour except 889 in
  the evening (Pečky 20:12, 22:08, 0:08 → Kouřim; Kouřim 20:39, 22:39 → Pečky). The owner's Haló decision decides it
  (coordinator, 2 Nov): 889 Chotutice every 480 on the 20:12 / 20:39 round, 1 bus.
- **Other okresy uncovered here** (their sheets' lines serve them): Louňovice, I.hráz (491's 3-min start; 381, 382, 387);
  Prusice, rozcestí (659's 16:00 / 18:00 path; 387); Hradištko, Hradištko, chaty, Hradištko, Kersko Branaldova (698's
  13:19 and 7:20; 443).

## Owner checks (3)
1. 821 Kouřim turns at Kouřim (1 bus; two of its afternoon slot trips really end there, two run on to Horní Kruty) or runs
   to Horní Kruty (2 buses).
2. Pooling 534 + 535 at Kolín as one circuit (−1 bus): the timetable chains the trips into three rounds; the plates will
   confirm.
3. Štíhlice, the sheet's one coverage choice: 660 Doubravčice (1 bus) or an exception (Štíhlice, Doubravčická on 491).

Removed by the review: 536 (decided by the path-variant rule) and the 491 + 660 pooling (the timetable cannot tell 491
from 661 as 660's feeder; in the notes, open for the live map). Removed after it: Chotutice (decided by the owner's Haló
rule; now 889 Chotutice).

## Open questions and script notes
- **Live map:** every pairing in the notes (491 ↔ 660, 660 ↔ 661, 535 → 534, 702 / 821 → 675, 821 ↔ 772, 821 ↔ 824,
  662 shuttle ↔ 354, 435 ↔ 686, 487 at Vlašim, 826 → 433, MHD 4 → MHD 6) and the next trips of the 675 Cerhenice and
  660 Doubravčice buses are to be checked against the 2 Nov afternoon plates.
- **0-minute turns** (537, 662, 681, 698, MHD Kolín 3 Atletický stadion, MHD Kolín 9) use `lay` 0 as the pilot's 573;
  the Leave up to behaviour is an engine question (in notes once).
- **Script notes:**
  1. `run_oblast.py` line 40 had a literal newline inside the `coverage:` f-string (SyntaxError, about 05:20–05:35 on
     2 Nov); the coordinator fixed it. My first run used a scratchpad wrapper that repaired the string in memory; every
     later run used the fixed script.
  2. The builder's knot check (05_schedule `finish`) takes the median offset over all of a leg's matched trips, not the
     leg's own `rt` / `stops_via` / `knot_rt`, so legs mixing paths show deviations that are not in the model: 536
     (Žiželice 8 / 4 min, Kolín 8), 681 (Kolín 10), 822 (Kolín 7), 826 (Pečky 7). Display only.
  3. `run_oblast.py` printed coverage exceptions as "UNCOVERED here … – reason"; it now prints them as "explained" (fixed
     by the coordinator).
  4. For legs read at a knot the Step 4 window is applied to the terminal time, so a line read at a hub can lose a window
     slot at the window edge (706 at 16:00); worth a line in the brief.
  5. Process, not a script: the parallel oblast sessions share one scratchpad folder and use the same file names
     (`texts.py`, `dump.py`, `run5.txt`); another session's files replaced mine there at 06:05. `lines.json` and this file
     were not affected (they live in the oblast folder); my later edits were made directly on `lines.json`. Worth telling
     the designers to work in a subfolder named after their oblast.

## Changed on 2 Nov (after `review-2026-11-01.md`)
- **491:** owner check (pooling with 660) removed; the notes say a 491 + 660 circuit would be 3 buses instead of 4, open for
  the live map. Rows unchanged.
- **535 / 534:** owner check kept, with the timetable's three bus rounds as evidence. Rows unchanged.
- **536:** owner check removed (path-variant rule); the note keeps "two lines every 120, one per path, would need 4 buses".
  Rows unchanged.
- **660:** the Štíhlice check reworded as the sheet's one coverage choice. Rows unchanged.
- **675 Cerhenice:** every 120 → 480 (Kolín 16:03, typed 62 → 422; Cerhenice 17:30, typed 29); hand window 16:00–18:00
  removed; Kolín 14:03 and 18:03 listed as off. 1 bus.
- **681 Petrovice:** every 120 → 480 with two slots each way (Uhlířské Janovice 13:40, 15:30, typed 279, 389; Losiny
  14:06, 15:56, typed 305, 415); all four afternoon trips exact. 1 bus.
- **706:** why names the 15:03 slot trip skipping Vavřinec (99 min). Rows unchanged.
- **821:** anchor 16:00 by hand; Sázava return 14:14 → 16:19 (typed 73 → 78, rt 102 → 99); 821 Kouřim written at its window
  trips 17:02 / 16:15 (typed 1 / 74 unchanged). Owner check kept, with the two trips that really end at Kouřim. 2 + 1 buses.
- **MHD Kolín 5:** every 180 → 480 with three slots each way (Polepy 13:44, 15:04, 16:44, typed 283, 363, 463; Silo 14:23,
  15:43, 17:37, typed 322, 402, 36), `stops_via` Kolín, Spel and `lay` 0 on the Silo leg. 1 bus.
- **MHD Kolín 9:** every 120 → 60 (Štítary :46, typed 45; Veltruby :20 = Spálenka :31, typed 79 → 19), 1 → 2 buses; the
  "every 60 fails" claim corrected.
- **PID Haló:** checked under the owner's 2 Nov rule. No stop has Haló as its only 13:00–19:00 service (888 / 889 run only
  in the evening), but Chotutice has no other bus at all: the coordinator ruled it decided by the owner's Haló decision, so
  **889 Chotutice** is new, every 480 on 889's fixed 20:12 / 20:39 round (Pečky typed 191, Kouřim typed 218, `lay` 0, sim
  window 20:00–22:00, named stops only), +1 bus. Its owner check is deleted.
- **Notes:** the Kounice – Mochov shuttle (231662) continuing 354 at Mochov, for the Praha-východ sheet; the every-480
  sentence now lists seven lines.
- Totals: 39 Simutrans lines, 69 → 71 buses (MHD Kolín 9 +1, 889 Chotutice +1). Rerun `run_oblast.py kolinsko`: 77 of
  77 timed legs pass Step 4; branch audit as before, path audit 4 slots (the two new ones are 889's virtual stops, by
  design); coverage unchanged.
- Script note: `00_config.py` keeps the automatic "PID Haló: on-demand service" reason for 889 in `config.json`'s
  `unmodelled` although 889 is now designed; `06_render.py` and `07_index.py` take the schedule first, so it does not show,
  but the config carries both.
