# Method check: PID Nymbursko (okres Nymburk), 2 Nov 2026

The 31 lines of the Nymbursko oblast, designed line by line with the bus schedule method v4
(`mirror/pipeline/bus-schedule-method.md`), the design brief (`../../DESIGN_BRIEF.md`, including "Learned on the pilot") and the
pilot review (`../rakovnicko/review-2026-11-01.md`). Design: `lines.json`; builder output: `data/derived/schedule.json`.

- **Data:** PID GTFS of 1 Nov 2026, service day Mon 2 Nov 2026 (school day); the whole-day reading `data/derived/reading/<L>.txt`
  for every line (all trips 3:00–24:00 at the core points, paths, 0–5 min chain test), and `data/derived/trips.json` for the
  times at other stops (705's sections, 540's Dymokury times). The live-map plates of the afternoon are not in the reading
  files yet; where a decision would need them it says so (owner checks 1 and 3).
- **Step 4**, per timed leg, in the line's model window (anchor −30 to +90): window slots = real departures ±1, and at least 80 %
  of the window slots with a real departure within 3 min. Then the most departures exactly on the minute over the day.
- **Typed values** are (real − 61) mod every (every terminus a loop); all 81 timed entries were recomputed from `schedule.json`
  and match. Evenly spaced entries are folded by the render (833 Sadská 15:33 / 16:33 on every 120 = every 60, Offset 32).
- **Final run** (`run_oblast.py nymbursko`): Step 4 audit 81 timed legs, 81 ok (0 EMPTY, 0 MORE, 0 FEWER); branch audit 12 legs
  read at a midpoint, all ok; path audit 1 flag (585, explained below); coverage: 470 afternoon stops, 463 on this sheet,
  0 uncovered of okres Nymburk, 1 outside the kraj (Jičín, železniční stanice: coverage exception, owner check 2), 6 of other
  Středočeský okresy (on other sheets, see the end).

Every one of the 31 lines is modelled (none unmodelled). Changed on 2 Nov after the independent review
(`review-2026-11-01.md`: 27 PASS, 1 FIX, 3 ASK OWNER): 434 split from 433's town trips (433 Zálabí added, +1 bus), the coverage
owner check reworded and extended to 833 Nymburk, a third owner check (the 434 ring), and notes for 853, 679 and 434. Each
changed line says so below; the final run above is after the changes. Each line below: (a) core points, (b) whole day, (c) Simutrans lines,
(d) Step 4 per leg (window slots / real departures in the window / filled; exact and within 3 min over the day 5–23),
(e) off the pattern, (f) buses.

## Prague lines

**398 Praha, Černý Most – Poděbrady**
- (a) Poděbrady, železniční stanice; Sadská; Praha, Černý Most.
- (b) Poděbrady → Praha every 15–30 min in the morning peak (4:08–8:38), hourly at :38 at midday, then every 30 at :08 / :38
  14:38–16:38, then 17:18, 18:08, 19:38, 21:36. Praha → Poděbrady :15 / :45 13:45–17:45 (17:15 only to Sadská), then
  18:45 (Sadská), 19:25, 20:35, 21:45. The buses sleep at Poděbrady and Sadská (first trips 4:08–5:53 start there); in
  15:00–17:00 the two ends are balanced (4 and 4), so no outstation correction is needed.
- Anchor 15:30 by hand (window 15:00–17:00): the default 16:00 window ends with Poděbrady 17:18, 10 min off the :08 slot (fill
  3 of 4, Step 4 FAIL); 15:00–17:00 is where the line's own every-30 pattern runs (the 305 precedent).
- (c) **398** every 30: Poděbrady :08 / :38 (typed 7), Praha, Černý Most :15 / :45 (typed 14).
- (d) Poděbrady → Praha 4/4/4 (15:08 15:38 16:08 16:38), 15 exact of 23; Praha → Poděbrady 4/4/4 (15:15 15:45 16:15 16:45),
  16 exact of 22. Knots Sadská and both ends exact.
- (e) Poděbrady 12:53, 17:18, the morning peak extras; Praha 19:25, 20:35; the Sadská shorts listed.
- (f) 5 buses (63 min each way; waits 4 at Černý Most, 20 at Poděbrady). The chain test at Černý Most shows 398 → 398 in 12 of
  26 and many city lines (the terminal is a hub); nothing to pair.

**425 Praha, Černý Most – Městec Králové – Trutnov**
- (a) Praha, Černý Most; Městec Králové, náměstí; Hořice, autobusové stanoviště; Trutnov, autobusové stanoviště.
- (b) Praha :10 every 2 h 7:10–17:10 (11:10 only to Hořice, 19:10 only to Městec Králové, 20:10); Trutnov 5:02, 6:02, 8:32,
  10:32, 14:27, 16:27, 18:32 (the afternoon two at :27 via Dvůr Králové n.L., ZOO); Hořice 13:22 → Praha.
- (c) **425** every 120: Praha 15:10 / 17:10 (typed 9), Trutnov 14:27 / 16:27 (typed 86). The return row takes the 14:27 / 16:27
  path so Dvůr Králové n.L., ZOO (no other line) is on it.
- (d) Praha → Trutnov 1/1/1 (17:10), 5 exact of 6; Trutnov → Praha 1/1/1 (16:27), 2 exact of 7 (the :32 trips are 5 off).
- (e) Trutnov 5:02, 6:02, 8:32, 10:32, 18:32; Praha 20:10; the Hořice and Městec shorts listed.
- (f) 3 buses (138 / 143 min; waits 59 at Trutnov, 20 at Praha). All stops past Městec Králové are in Královéhradecký kraj and
  are on this row.

## Lysá nad Labem and Milovice

**430 Lysá nad Labem – Milovice – Lipník**
- (a) Lysá nad Labem, železniční stanice; Milovice, Park Mirakulum; Milovice, Balonka; Lipník.
- (b) Lysá :36 → Lipník hourly 14:36–19:36 by the direct road through Milovice (skips Tyršova, Sportovní, Park Mirakulum);
  Lipník :07 → Lysá hourly 16:07–19:07 via Park Mirakulum (12:52, 13:52, 15:07 to Milovice only). Plus Lysá – Milovice
  short trips (Lysá 14:01, 15:01 to Lipník via Park Mirakulum, 17:01, 19:01, 20:36; Milovice 14:30, 15:55, 17:51, 19:51).
- (c) **430** every 60: Lysá :36 (typed 35), Lipník :07 (typed 6). The short trips are every 1–2 h with all their stops on 430's
  two rows (Step 8: listed, no line).
- (d) Lysá → Lipník 2/2/2 (15:36 16:36; real 15:36 16:36), 8 exact of 11; Lipník → Lysá 2/2/2 (16:07 17:07), 4 exact of 9.
- (e) Lysá 12:16, 13:16, 15:01; Lipník 12:52, 13:52, 20:52; the shorts.
- (f) 3 buses (37 / 41 min; waits 54 at Lipník, 48 at Lysá). Owner check 1: pooled with 436 at Lipník it would be 4 buses for
  both lines instead of 5.

**432 Lysá nad Labem – Milovice – Vlkava – Mladá Boleslav**
- (a) Lysá nad Labem, železniční stanice; Milovice, Park Mirakulum; Vlkava, náves; Mladá Boleslav, autobusové stanoviště.
- (b) Hourly at :46 / :48 from both ends until 13:46 / 12:48, then every 2 h: Lysá 16:01, 18:01, 20:01; Mladá Boleslav 14:03,
  14:33, 16:03, 18:03, 19:33 (to Milovice), 22:23 (to Milovice).
- (c) **432** every 120: Lysá 16:01 (typed 60), Mladá Boleslav 16:03 (typed 62).
- (d) Lysá → Mladá Boleslav 1/1/1, 3 exact of 9; Mladá Boleslav → Lysá 1/1/1, 3 exact of 10.
- (e) Lysá 11:46, 12:46, 13:46; Mladá Boleslav 11:48, 12:48, 14:33, 19:33 and the morning.
- (f) 2 buses (the two cross; 76 / 75 min; waits 46 / 43). Chain at Lysá: 4 of 11 arrivals go on as 442 (another sheet), noted.

**434 Nymburk – Straky – Milovice – Benátky nad Jizerou**
- (a) Nymburk, hl.nádraží; Straky; Milovice, železniční stanice; Benátky nad Jizerou, autobusové stanoviště.
- (b) Nymburk :24 hourly 14:24–18:24 (13:09, 12:09 before); Benátky :34 hourly 14:34–18:34 (16:34 only to Milovice,
  železniční stanice; 12:49, 13:44 before). The bus waits 56 min at Nymburk (arrives :28, leaves :24).
- **Step 5b / pooling.** 433's town trips (hl.nádraží :34 → Zálabí, Zálabí :00 → hl.nádraží) fit that wait: the chain test
  has "4 of 11 departures of 434 follow a 433 arrival within 0–5 min" (14:24, 16:24, 17:24, 18:24 after the :19 arrivals),
  so a ring would carry both on 3 buses instead of 3 + 1. But the evidence is one-sided: the other half (434 arrives :28,
  433 leaves :34) is a 6-min gap outside the test; the ring closes in reality only twice (15:28 → 16:24 and 16:28 → 17:24: the
  16:34 Benátky trip ends at Milovice, and no town trip follows the 18:28); both lines are balanced on their own (no surplus to
  pair); Nymburk, hl.nádraží is a timed pulse; and the only plates in the data put 434's morning buses on 497 (8616: 497
  Milovice 4:25 → Nymburk 5:16 → 434 5:29; 8569: 434 Benátky 4:09 → Nymburk 5:03 → 497 5:44) and the town bus 8570 on 676.
  497 fits the same gap (434 arrives :28 → 497 :40; 497 arrives :13 → 434 :24). So the lines are modelled apart and the
  ring is owner check 3, for the 2 Nov live map.
- (c) **434** every 60: Nymburk :24 → Benátky (typed 23); Benátky :34 → Nymburk, read to Milovice, železniční stanice
  (`core_to`) so the 16:34 short counts (typed 33). 433's town trips are 433 Zálabí (see 433).
- (d) Nymburk → Benátky 2/2/2 (16:24 17:24), 5 exact of 10; Benátky → Nymburk 2/2/2 (15:34 16:34), 5 exact of 13. Branch
  audit ok (16:34 is the Milovice short; its knot check at Nymburk shows 60, the trip does not reach Nymburk).
- (e) Nymburk 12:09, 13:09; Benátky 12:49, 13:44 (to Milovice) and the morning.
- (f) 3 buses, round 180 min (waits 19 at Benátky, 56 at Nymburk).
- **Changed on 2 Nov** (review FIX): was "434 + 433 Zálabí", one ring of four legs, 3 buses for both lines. Now 434 alone
  (3 buses, typed values unchanged 23 / 33) and 433 Zálabí (1 bus, typed 33 / 59); the ring is owner check 3 (−1 bus if the
  live map shows it). Pooling is an owner option, never silent; the earlier version rested on a timing fit.

**497 Nymburk – Kostomlaty nad Labem – Milovice**
- (a) Nymburk, hl.nádraží; Kostomlaty nad Labem, železniční stanice; Milovice, železniční stanice; Kamenné Zboží.
- (b) Nymburk :40 hourly 12:40–16:40 (13:44); Milovice :25 hourly 13:25–16:25, each the bus that has just arrived (0-minute
  turn, 5 of 8 in the chain test); the line ends with the 16:40 / 17:44. Short trips Nymburk → Kostomlaty, železniční
  stanice 15:14, 17:44, Nymburk 16:00 → Kostomlátky, u kapličky → 16:25 back, Nymburk 14:19 → Kamenné Zboží → 14:33 back.
- Anchor 15:00 by hand: the default 16:00 window takes in Milovice 17:25, which does not run (fill 1 of 2, FAIL).
- (c) **497** every 60: Nymburk :40 (typed 39), Milovice :25 (typed 24, `lay` 0: 0-minute turn as in the timetable; with the
  builder's 1-min floor the bus would miss it and the line would need 3 buses). **497 Kamenné Zboží** every 480: Nymburk 14:19
  (typed 318), Kamenné Zboží 14:33 (typed 332, `lay` 0): Kamenné Zboží has no other line (serve every place), the cheapest
  pattern holding its one afternoon round.
- (d) 497: Nymburk → Milovice 2/2/2 (14:40 15:40), 4 exact of 7; Milovice → Nymburk 2/2/2 (15:25 16:25), 5 exact of 6.
  497 Kamenné Zboží: out no window slot (the 14:19 stands for itself; named in the why), back 1/1/1 (14:33).
- (e) Nymburk 13:44 and the morning; the Kostomlaty and Kostomlátky shorts listed.
- (f) 2 + 1 buses (497: 45 / 48 min, wait 27 at Nymburk, 0 at Milovice).
- Chains: 497 ↔ 897 at Kostomlaty nad Labem, železniční stanice in the morning (7:17, 8:50, 10:45 at 0 min); in the afternoon the
  15:14 short arrives 15:36 and 897 leaves 15:50, likely the same bus. Named in the notes, not modelled (no bus saved).

**897 Kostomlaty nad Labem – Ostrá – Lysá nad Labem**
- (a) Lysá nad Labem, železniční stanice; Lysá nad Labem, Litol, Palackého; Stratov; Kostomlaty nad Labem, železniční stanice.
- (b) Lysá 13:47, 15:47 (via Lysá nad Labem, škola, Ostrá, náves and Ostrá, Šnepov; 6:52, 8:25 direct); Kostomlaty 10:45, 12:50,
  14:50, 15:50, 16:50 (the last trip of the day).
- (c) **897** every 120: Lysá :47 at odd hours (typed 46), Kostomlaty :50 at even hours (typed 109). The out row takes the
  13:47 / 15:47 path, so Ostrá, náves and Šnepov are on it; the back row the direct one (12:50, 16:50); every stop of 897 is on
  one of the two (nine of them have no other line).
- (d) Lysá → Kostomlaty 1/1/1 (15:47), 2 exact of 4; Kostomlaty → Lysá 1 slot / 2 real (15:50, 16:50) / 1 filled, 3 exact of 5.
- (e) Kostomlaty 15:50, 10:45 (5 off) and the morning.
- (f) 1 bus (31 / 25 min; waits 32 and 32).

## Nymburk

**433 Nymburk – Kostelní Lhota – Pečky**
- (a) Nymburk, hl.nádraží; Nymburk, náměstí; Nymburk, Zálabí; Pečky, železniční stanice.
- (b) Hourly all day: Nymburk :04 6:04–19:04, Pečky :15 5:15–19:15, no exception in 12 trips each way. Town short trips
  hl.nádraží :34 → Zálabí 15:34–19:34 (5:34, 7:19, 7:34 morning; 20:04, 21:04, 22:04 evening) and Zálabí :00 → hl.nádraží
  14:00, 16:00, 17:00, 18:00 (7:00, 8:00; 20:32, 22:29): an hourly short working of 5 trips each way 13:00–19:00 (the
  afternoon-branch threshold is 3), so its own Simutrans line; every stop of it is also on 433's main row.
- (c) **433** every 60: Nymburk :04 (typed 3), Pečky :15 (typed 14). **433 Zálabí** every 60: hl.nádraží :34 → Zálabí (typed
  33), Zálabí :00 → hl.nádraží (typed 59), both `notvia` Pečky, železniční stanice so the Pečky trips stay on 433.
- (d) 433: Nymburk → Pečky 2/2/2, 12 exact of 12; Pečky → Nymburk 2/2/2, 12 exact of 12. 433 Zálabí: hl.nádraží → Zálabí 2/2/2
  (15:34 16:34), 7 exact of 11; Zálabí → hl.nádraží 2/2/2 (16:00 17:00), 6 exact of 8.
- (e) 433 Zálabí: hl.nádraží 20:04, 21:04, 22:04 and Zálabí 20:32, 22:29 (evening town trips at other minutes), the morning.
- (f) 2 + 1 buses (433: 37 / 36 min, waits 34 at Pečky, 13 at Nymburk; 433 Zálabí: 19 / 19 min, waits 7 at Zálabí, 15 at
  hl.nádraží).
- **Changed on 2 Nov** (review FIX on 434): the town trips were legs of the 434 ring; now their own line 433 Zálabí, 1 bus.

**436 Nymburk – Vlkava – Lipník**
- (a) Nymburk, hl.nádraží; Vlkava, náves; Lipník.
- (b) Nymburk :10 hourly 12:10–14:10, then :20 15:20–20:20 (17:20 and 19:20 only to Vlkava, náves);
  Lipník :21 14:21, 16:21, 17:21, 18:21 (13:15, 14:42 via Všejany, 15:16).
- (c) **436** every 60: Nymburk :20 read to Vlkava, náves (`core_to`, so the 17:20 short counts; typed 19), Lipník :21 (typed 20).
- (d) Nymburk → Lipník 2/2/2 (16:20 17:20), 6 exact of 14; Lipník → Nymburk 2/2/2 (16:21 17:21), 4 exact of 11. Branch audit ok.
- (e) Nymburk 12:10, 13:10, 14:10 (10 min off); Lipník 13:15, 14:42, 15:16 and the morning.
- (f) 2 buses (34 / 35 min; waits 27 at Lipník, 24 at Nymburk). Owner check 1 (with 430).

**443 Nymburk – Sadská – Čelákovice**
- (a) Nymburk, hl.nádraží; Sadská; Přerov nad Labem, u skanzenu; Čelákovice, železniční stanice; Čelákovice, Toušeňská.
- (b) Hourly 8:02–18:02 from Nymburk and 8:55–18:55 from Toušeňská, all exact; morning 5:28 / 6:28 / 6:02 and 5:46 / 6:27 / 7:00,
  evening shorts to Sadská and Přerov nad Labem.
- (c) **443** every 60: Nymburk :02 (typed 1), Toušeňská :55 (typed 54).
- (d) 2/2/2 both ways; 9 exact of 11 each way.
- (f) 3 buses (59 / 60 min; waits 54 at Toušeňská, 7 at Nymburk). Chain: 10 of 13 443 arrivals at Nymburk are followed by a
  676 departure, but a 443 + 676 circuit needs 5 buses, the same as apart (3 + 2), and Nymburk is a timed hub, so nothing to pair.

**493 Nymburk – Poděbrady**
- (a) Poděbrady, železniční stanice; Nymburk, hl.nádraží.
- (b) Hourly all day: Nymburk :04, Poděbrady :30 (arrives :29, 1-min turn, 12 of 14 in the chain test); 6:34 and 7:00 extra.
- (c) **493** every 60: Nymburk :04 (typed 3), Poděbrady :30 (typed 29; the builder takes the real 1-min turn).
- (d) 2/2/2 both ways; 13 exact of 14 each way.
- (f) 1 bus (25 / 25 min; waits 1 at Poděbrady, 9 at Nymburk).

**499 Nymburk – Loučeň – Semčice – Mladá Boleslav**
- (a) Nymburk, hl.nádraží; Loučeň; Mladá Boleslav, autobusové stanoviště.
- (b) Nymburk :05 hourly (16:05, 18:05 only to Loučeň; 19:05 none; 20:05); Mladá Boleslav :45 hourly 11:45–18:45 except 17:45
  (13:40 via Charvatce).
- (c) **499** every 60: Nymburk :05 read to Loučeň (`core_to`; typed 4), Mladá Boleslav :45 (typed 44).
- (d) Nymburk → Mladá Boleslav 2/2/2 (16:05 Loučeň short, 17:05), 12 exact of 13; Mladá Boleslav → Nymburk 2/2/2 (15:45
  16:45), 9 exact of 12. Branch audit ok.
- (e) Mladá Boleslav 13:40 (5 off; its Charvatce stops are on Mladoboleslavsko's 764), 22:25 and the morning shorts from Loučeň.
- (f) 3 buses (62 / 65 min; waits 38 at Mladá Boleslav, 15 at Nymburk).

**541 Nymburk – Úmyslovice – Městec Králové – Dlouhopolsko**
- (a) Nymburk, hl.nádraží; Městec Králové, náměstí; Dlouhopolsko.
- (b) Nymburk :09 hourly: even hours to Dlouhopolsko (10:09–18:09), odd hours to Městec (13:09, 15:09, 17:09; 20:09).
  Towards Nymburk Městec :05 hourly: from Dlouhopolsko :46 at odd hours (11:46–17:46, passing Městec :05 at even hours) and from
  Městec itself at odd hours (13:05, 15:05, 17:05). Městec town loops 7:15 and 16:15 via Sloveč, Kamilov.
- The real buses alternate the two ends (Městec 13:59 → 15:05 → Nymburk 15:56 → 16:09 → Dlouhopolsko 17:18 → 17:46 → Nymburk
  18:56: one bus, 13-min turns at Nymburk), so one
  circuit, not two Ex4 lines: two lines every 120 would need 2 + 2 = 4 buses, the circuit 3. The bus that waits at Městec
  (arrives :59, leaves :05 an hour later) runs the 16:15 loop in that wait, so Sloveč, Kamilov (no other line; not a roadside
  stop) is served at no extra bus.
- (c) **541** every 120, five legs: Nymburk → Dlouhopolsko 16:09 (typed 68); Dlouhopolsko → Nymburk 15:46 (typed 45); Nymburk →
  Městec 15:09 / 17:09, not via Dlouhopolsko (typed 8); Městec loop 16:15 (typed 74); Městec → Nymburk 17:05, not via
  Dlouhopolsko (typed 4).
- (d) 1/1/1 on all five (16:09, 15:46, 17:09, 16:15, 17:05); exact over the day 5 of 6, 4 of 6, 3 of 6, 1 of 2, 3 of 5.
- (e) Nymburk 8:09, 20:09; Městec 8:05, 10:05; the 7:15 loop; the morning.
- (f) 3 buses, round 360 min (waits 28 at Dlouhopolsko, 13 and 13 at Nymburk, 16 and 30 at Městec). Chain 538 → 541 at Městec
  (538 arrives 17:01, 541 leaves 17:05; 3 of 8): pooling would not save a bus (538's 72-min round does not fit the 66-min wait).
- **Changed on 2 Nov** (review, method check only): the bus chain quoted in (b) was wrong ("17:09 → Městec → 19:05 back": the
  last Městec → Nymburk trip is 17:05); replaced by a real one. The design is unchanged.

**673 Nymburk – Oskořínek – Křinec**
- (a) Nymburk, hl.nádraží; Křinec, Sovenice (the knot: the short trips end there); Křinec, náměstí; Křinec, škola.
- (b) Nymburk :05 at odd hours all day (5:05–19:05; 13:05 and 15:05 to Křinec, škola, 17:05 and 19:05 to Sovenice; 6:10, 6:40
  morning). Towards Nymburk at Sovenice: 8:15, 10:15, 16:15, 18:15 at even hours :15, plus 13:15 and 14:06 (škola 14:00).
- (c) **673** every 120: Nymburk 17:05 read to Sovenice (`core_to`; typed 4), out by the 15:05 path via Nový Dvůr (`stops_via`,
  50 min; Nový Dvůr has no other line); Křinec, škola → Nymburk read at Sovenice :15 (`knot`, škola :09; typed 68).
- (d) Out 1/1/1 (17:05 Sovenice short), 7 exact of 9; back 1/1/1 (16:09), 4 exact of 9. Branch audit ok both.
- (e) Sovenice 13:15 (60), škola 14:00 (9) and the morning.
- (f) 1 bus (50 / 41 min; waits 14 at škola, 15 at Nymburk).

**674 Nymburk – Křinec – Rožďalovice**
- (a) Nymburk, hl.nádraží; Křinec, náměstí; Rožďalovice, náměstí; Rožďalovice, železniční stanice.
- (b) Nymburk :05 at even hours (8:05–20:05; 8:05, 10:05, 20:05 only to Křinec, 16:05 only to Košík, Tuchom); back from
  Rožďalovice, železniční stanice 13:48, 15:48 (náměstí 13:49, 15:49), Košík, Tuchom 16:59 (0-min turn), Křinec 12:47.
- (c) **674** every 120: Nymburk :05 read to Křinec, náměstí (`core_to`; typed 64); Rožďalovice, náměstí :49 (typed 48). The
  buses arrive at náměstí and leave from the station one stop back; the row is timed at náměstí (no terminus alias: náměstí is a
  through stop of 463 and 542), and Rožďalovice, železniční stanice is on 463.
- (d) Out 1/1/1 (16:05 Tuchom short), 7 exact of 9; back 1/1/1 (15:49), 2 exact of 3. Branch audit ok.
- (e) Košík, Tuchom 16:59, Křinec 12:47, the morning.
- (f) 2 buses (the two cross; 60 / 64 min; waits 44 at Rožďalovice, 72 at Nymburk). Every 240 would need 1 bus but halves a
  two-hourly line (the method keeps the real headway; Opavsko rule 2).

**676 Nymburk – Loučeň – Seletice**
- (a) Nymburk, hl.nádraží; Jíkev; Loučeň; Seletice.
- (b) Nymburk :00 hourly 12:00–19:00: Seletice at 12:00, 15:00, 17:00, 19:00, Loučeň at 13:00, 14:00, 16:00, Jíkev at 18:00.
  Towards Nymburk hourly at Loučeň :19 12:19–17:19: from Seletice :06 at 13:06 and 16:06, from Loučeň otherwise; Jíkev 18:27.
- Ex4 (a fork past the reading point, the 292 lesson): each end its own line every 120, the Loučeň line `notvia` Seletice.
  Seletice at odd hours out / even hours back (15:00, 17:00, 19:00; 16:06), so Loučeň takes even hours out / odd back (14:00,
  16:00; 15:19, 17:19): together hourly :00 at Nymburk and :19 at Loučeň, as the timetable runs. (Loučeň at even :19 would
  meet the Seletice bus at Loučeň.) Mcely and Seletice are covered by 676 Seletice.
- (c) **676** every 120: Nymburk 16:00 (typed 59), Loučeň 17:19 (typed 18). **676 Seletice** every 120: Nymburk 17:00 (typed
  119), Seletice 16:06 (typed 65).
- (d) 676: out 1/1/1, 3 exact of 4; back 1/1/1, 2 exact of 4. 676 Seletice: out 1/1/1, 3 exact of 7; back 1/1/1, 2 exact of 6.
- (e) Nymburk 12:00, 13:00 and Loučeň 12:19, 14:19, Seletice 13:06 (the ends swap hours before 15:00); the Jíkev shorts.
- (f) 1 + 1 buses (31 / 31 min, waits 48 at Loučeň; 44 / 44, waits 22 at Seletice; 10 at Nymburk each).

**833 Nymburk – Hořátev – Sadská – Pečky**
- (a) Sadská; Pečky, železniční stanice; Nymburk, hl.nádraží.
- (b) Sadská :33 hourly 12:33–18:33 → Pečky; Pečky → Sadská 13:15, 14:12, 14:48, 16:12, 17:15, 18:12 (even :12, odd :15).
  Through Nymburk: Nymburk 13:34, 14:34 → Sadská, Sadská 14:39 → Nymburk via Písty, Pečky 10:06, 12:06 → Nymburk, Nymburk 6:34,
  9:04 → Pečky.
- Anchor 16:00 by hand: the default (13:40, window 13:10–15:10) is the Nymburk trips and the 14:48 extra; the shuttle's own
  pattern runs all afternoon (the 282 rule).
- (c) **833** every 120: Pečky 16:12 and 17:15 (typed 14, 71), Sadská 15:33 and 16:33 (typed 32, 92 = every 60, Offset 32). Every
  60 at :12 passes too (3 exact, the :15 trips within 3), but the two-slot row has 5 exact over the day, the method's order.
  **833 Nymburk** every 480: Nymburk 13:34 (typed 273), Sadská 14:39 (typed 338): Hořátev, prodejna, Hořátev, Technologický park
  and Písty (villages, not roadside stops) and Zvěřínek, rozcestí Hořátev have no other line.
- (d) 833: Pečky → Sadská 2/2/2 (16:12 17:15), 5 exact of 11; Sadská → Pečky 2/2/2 (15:33 16:33), 7 exact of 11. 833 Nymburk: no
  window slots (13:34 and 14:39 stand for themselves, named in the why).
- (e) Pečky 14:48, 12:06 / 10:06 (through), Nymburk 14:34, the morning.
- (f) 1 + 1 buses (12 / 12 min, waits 9 and 6 at Sadská, 30 and 27 at Pečky; 33 / 40 min).
- **Changed on 2 Nov** (review ASK OWNER): 833 Nymburk stays (the rule), but its stops sit near hourly stops of the same
  places (GTFS coordinates: Hořátev, prodejna 90 m from Hořátev, ZD on 433; Zvěřínek, rozcestí Hořátev 396 m from Zvěřínek on
  443; Písty 717 m from Písty, Temac on 443; Hořátev, Technologický park 1.3 km from Hořátev, ZD). Added to the coverage owner
  check (owner check 2): keep, or four coverage exceptions, −1 bus.

## Poděbrady

**498 Poděbrady – Ratenice – Pečky**: (a) Poděbrady, železniční stanice; Poděbrady, Přední Lhota, u Kopečků; Ratenice; Pečky,
železniční stanice. (b) Hourly all day, Poděbrady :20, Pečky :15 (7:05, 8:50, 5:45 extra). (c) **498** every 60, typed 19 / 14.
(d) 2/2/2 both ways; 12 exact of 14, 13 of 14. (f) 2 buses (25 / 25; the two cross, waits 30 at Pečky, 40 at Poděbrady).
Ratenice (okres Kolín) has no other line.

**539 Poděbrady – Křečkov**: (a) Poděbrady, železniční stanice; Křečkov. (b) Poděbrady :12 hourly 13:12–16:12, 18:12; Křečkov :31
13:31–16:31 (2-min turn, 6 of 8 in the chain test); morning trips. Anchor 15:00 by hand: the default window takes in the 17:12
that does not run. (c) **539** every 60, typed 11 / 30. (d) 2/2/2 both ways (15:12 16:12; 14:31 15:31), 6 of 8 and 7 of 8 exact.
(e) 18:12, morning. (f) 1 bus (17 / 16; 2-min turn at Křečkov, 25 at Poděbrady).

**540 Poděbrady – Dymokury – Záhornice**
- (a) Poděbrady, železniční stanice; Pátek, u váhy; Dymokury (the knot); Záhornice, u Tylů.
- (b) At Dymokury hourly both ways, exact: from Poděbrady :42 (12:42–18:42), towards Poděbrady :22 (12:22–18:22). The ends vary
  with the path: Poděbrady :08 (13:08, 15:08, 16:08, 17:08 to Dymokury only, 18:08) or :05 via Křečkov (12:05, 14:05);
  Záhornice :07 (14:07, 16:07, 17:07; direct, 15 min to Dymokury) or :02 via Chotěšice, Nová Ves (13:02, 15:02; 20 min);
  18:22 starts at Dymokury.
- (c) **540** every 60: Poděbrady :08 read to Dymokury (`core_to`, so the 17:08 counts), `notvia` Křečkov (the 12:05 / 14:05 are
  listed; Křečkov is on 539), by the 16:08 path via Poděbrady, Jeronýmova and Chotěšice, Nová Ves (`stops_via`, 54 min; typed 7);
  Záhornice :07 read at Dymokury :22 (`knot`, mixed origins on the line's own path) with `knot_rt` 15 set by hand to the slot
  trips' own time (the median would be 20, the Nová Ves path), so the row leaves :07 by the direct road, 49 min (typed 6).
- (d) Out 2/2/2 (16:08 17:08), 8 exact of 10; back 2/2/2 (16:07 17:07), 9 exact of 11. Branch audit ok both. The card's knot check
  shows 5 min at Dymokury and Poděbrady on the way back: it uses the median offset of all the leg's trips (54 min, the Nová Ves
  path), not the row's 49; the slot trips themselves pass Dymokury at :22.
- (f) 2 buses (waits 5 at Záhornice, 12 at Poděbrady).

**542 Poděbrady – Dymokury – Rožďalovice**: (a) Poděbrady, železniční stanice; Podmoky, ObÚ; Dymokury; Rožďalovice, náměstí.
(b) Every 2 h: Poděbrady :15 at even hours 10:15–18:15, Rožďalovice :44 at even hours 12:44–16:44 (8:44); Dymokury → Podmoky
shorts 14:15, 16:15. (c) **542** every 120, typed 74 / 103. (d) 1/1/1 both ways; 5 exact of 7, 4 of 6. (e) the morning; shorts
listed. (f) 2 buses (the two cross; waits 92 at Rožďalovice, 33 at Poděbrady). Seven stops have no other line (Viničná Lhota,
Ledečky, Podlužany, Nové Zámky, Černá Hora, Na Drážce, Vrbice, kulturní dům), all on the row.

**543 Poděbrady – Opolany – Hradčany**
- (a) Poděbrady, železniční stanice; Žehuň; Žehuň, u rybníka; Hradčany, ObÚ.
- (b) Poděbrady :55 at even hours (12:55, 14:55 → Hradčany; 16:55 → Žehuň, u rybníka; 9:55 → Žehuň; 19:05); Hradčany 14:07
  (via Sány, 48 min), 16:13 (not via Sány, 42 min); Žehuň 12:19, Žehuň, u rybníka 18:20. One bus, turning at Poděbrady in 0 min
  (14:55 and 16:55 each leave the minute the previous trip arrives; 4 of 6 in the chain test).
- (c) **543** every 120: Poděbrady 16:55 read to Žehuň, u rybníka (`core_to`), `lay` 0 (0-minute turn as in the timetable; typed
  114); Hradčany 16:13, `notvia` Sány (typed 72), so the row is the 16:13's own path and 42 min: with the 14:07's path (via Sány,
  48 min) the bus would miss the 16:55 and the line would need 2 buses. Sány and Opolany, Opolánky, k železniční zastávka are on
  the way out (and on 705).
- (d) Out 1/1/1 (16:55), 3 exact of 5; back 1/1/1 (16:13), 1 exact of 1 (the 14:07 is listed). Branch audit ok.
- (e) Poděbrady 19:05, Žehuň, u rybníka 18:20, Hradčany 14:07, the morning.
- (f) 1 bus (46 / 42 min; wait 32 at Hradčany, 0 at Poděbrady).

**585 Poděbrady – Kopidlno – Jičín (Královéhradecký kraj)**
- (a) Poděbrady, železniční stanice; Kopidlno, náměstí; Jičín, autobusové stanoviště; Chroustov.
- (b) Poděbrady → Jičín 6:09, 10:24, 13:24, 16:24; Jičín → Poděbrady 6:35, 9:35, 13:35 (via Jičíněves, Keteň, Kopidlno, Pševes,
  Kopidlno, žel.přejezd), 16:35 (via Vršce). Jičín – Kopidlno / Chroustov local trips: Jičín 12:35, 15:35 → Kopidlno, Kopidlno
  13:02 → Jičín, Jičín 14:35 → Chroustov, Chroustov 15:16 → Jičín (2-min turn), Jičín, železniční stanice 18:30 → Chroustov.
- Every 180 (13:24 → 16:24, 13:35 → 16:35 are 3 h apart). The bus of 13:24 waits at Jičín 14:28–16:35 and the Chroustov round
  14:35 → 15:16 fits in it; Chroustov has the only service of Židovice and Běchary (Královéhradecký kraj), so the Chroustov round
  is a leg of the same circuit: 0 extra buses (as one line on its own it would cost 1).
- (c) **585** every 180, four legs: Poděbrady 16:24 (typed 23); Jičín → Chroustov 14:35 (typed 94); Chroustov → Jičín 15:16 (typed
  135); Jičín → Poděbrady 16:35 (typed 34) by the 13:35 path via Keteň (`stops_via`, 60 min). 13:35 and 16:35 are the same slot
  on every 180, so the row's path is the 13:35's, which holds three stops nothing else serves; the Vršce stops the 16:35 takes
  are on the way out.
- (d) Poděbrady → Jičín 1/1/1, 3 exact of 4; Jičín → Poděbrady 1/1/1, 2 exact of 4; the two Chroustov legs have no window slot
  (14:35 and 15:16 are the real trips, named in the why). Path audit: the one flag of the sheet, 585's 16:35 slot trip runs via
  Vršce, off the row's Keteň path, as intended.
- (e) Poděbrady 6:09, Jičín 6:35, 9:35, 18:35 (the 18:30 from Jičín, železniční stanice, read at the bus station); the Kopidlno
  shorts listed.
- (f) 2 buses, round 360 min (waits 7 and 37 at Jičín, 2 at Chroustov, 109 at Poděbrady).
- **Changed on 2 Nov** (review ASK OWNER): the Jičín, železniční stanice exception and its owner check reworded. The stop is
  493 m from Jičín, autobusové stanoviště (GTFS coordinates) with one afternoon trip, so it is a second stop of the same town,
  not a stop "the rule wants served": the exception is recommended; the alternatives are the invented hop (0 buses) or its own
  line every 480 (+1 bus). It now shares owner check 2 with 833 Nymburk. The design is unchanged.

**598 Poděbrady – Městec Králové – Kněžice – Chotěšice**
- (a) Poděbrady, železniční stanice; Městec Králové, náměstí; Kněžice, Dubečno; Chotěšice, Nová Ves.
- (b) Poděbrady :15 hourly 12:15–18:15: even hours to Chotěšice, Nová Ves (12:15, 14:15, 16:15), odd to Kněžice, Dubečno (13:15,
  15:15; 17:15 only to Městec Králové), 18:15 and 20:15 Dubečno, 22:45 Městec. Back: Nová Ves :39 at odd hours (13:39, 15:39,
  17:39), Dubečno :47 at even hours (14:47, 16:47; 11:47), Městec 13:08, 19:13.
- As 541: the buses alternate the two ends (arrive Poděbrady :42, leave :15 for the other end), one circuit every 120 needs 3
  buses, two Ex4 lines 2 + 2.
- (c) **598** every 120, four legs: Poděbrady → Nová Ves 16:15 (typed 74); Nová Ves → Poděbrady 15:39 (typed 38); Poděbrady →
  Dubečno 17:15 read to Městec Králové (`core_to`), `notvia` Nová Ves (typed 14); Dubečno → Poděbrady 16:47, `notvia` Nová Ves
  (typed 106).
- (d) 1/1/1 on all four; exact over the day 3 of 5, 3 of 4, 3 of 9, 2 of 4. Branch audit ok (17:15 is the Městec short).
- (e) Poděbrady 18:15, 20:15 (Dubečno at even hours after 18:00), 22:45; Městec 13:08, 19:13; the morning.
- (f) 3 buses, round 360 min (waits 21 at Nová Ves, 32 at Dubečno, 33 and 33 at Poděbrady).

**678 Poděbrady – Cerhenice – Pečky**: (a) Poděbrady, železniční stanice; Oseček; Cerhenice, Náměstí Míru; Pečky, železniční
stanice. (b) Poděbrady :05 at even hours 8:05–18:05 (hourly in the morning), Pečky :14 at odd hours 9:14–17:14, 18:14, 20:14
(Cerhenice). (c) **678** every 120, typed 64 / 13. (d) 1/1/1 both ways; 7 exact of 10, 5 of 9. (e) Pečky 18:14, the morning.
(f) 1 bus (40 / 40; waits 29 at Pečky, 11 at Poděbrady).

**679 Kolín – Velim – Poděbrady**: (a) Kolín, nádraží; Velim, škola; Oseček; Poděbrady, železniční stanice. (b) Kolín :00 at even
hours 10:00–18:00, Poděbrady :10 at odd hours 11:10–19:10 and 15:15; one bus with a 2-min turn at Kolín (4 of 9 in the chain
test). (c) **679** every 120, typed 59 / 9. (d) 1/1/1 both ways; 5 exact of 7, 4 of 8. (e) Poděbrady 15:15 (5), the morning; Velim,
škola → Oseček shorts listed. (f) 1 bus (48 / 48; 2-min turn at Kolín, 22 at Poděbrady). Six of its stops (okres Kolín) have no
other line. **Changed on 2 Nov** (review): the chain 679 ↔ 821 at Kolín, nádraží (6 of 9 arrivals followed by an 821 departure,
5 of 9 departures after an 821 arrival; 821 is on the Kolínsko sheet) is now named in the sheet notes for the live map. The
design is unchanged.

**705 Poděbrady – Kolín – Kutná Hora – Čáslav**
- (a) Poděbrady, železniční stanice; Kolín, nádraží; Kutná Hora, Karlov, Na Rovinách; Čáslav, obchodní centrum.
- (b) Kolín → Čáslav hourly at Kolín :50 (12:50–18:50), Čáslav, obchodní centrum → Kolín hourly :56 (11:59–18:01, Kolín :10).
  Through to and from Poděbrady (via Opolany, Sány, Velký Osek, Veltruby): Poděbrady 15:42, 17:41 (Kolín 16:50, 18:50; the 12:52
  runs via Kolín, PZKO-TOYOTA), 16:36 to Kolín only; towards Poděbrady at Kolín 12:40 (start), 14:10 (Čáslav, zem.škola 12:55),
  14:50 (Kutná Hora 13:54), 16:10 (Čáslav 14:59, ends at Libice nad Cidlinou, u sokolovny), 18:10 (Čáslav 16:56). Kolín – Kutná
  Hora shorts 12:20, 13:20, 16:20 out, 11:54, 14:54, 17:05 back.
- 705 is this sheet's line (licence 27x705), and its stops in okres Kolín and Kutná Hora (Velký Osek, Červené Pečky, Miskovice,
  Kutná Hora, Neškaredice, Perštejnec, Třebešice) have no other line, so it is modelled to Čáslav. Ex4: from 15:00 the through
  trips pass Kolín at even hours and the Kolín – Čáslav trips at odd hours, both ways, so two lines every 120 give the hourly
  Kolín – Čáslav run with no shared minute.
- (c) **705** every 120: Poděbrady 15:42 (typed 41) by the Velký Osek path (`stops_via`; `rt` 139, the 15:42's own; the median
  was 140); Čáslav → Poděbrady read at Kolín :10 (`knot`, kr 74 → Čáslav :56, typed 115), `core_to` Libice nad Cidlinou, u kostela
  (a stop every through trip passes, so the 14:59 to Libice counts; u sokolovny is skipped by the 6:59 / 8:29 path), `rt` 141, the
  16:56's own. **705 Kolín** every 120: Kolín 15:50 (typed 49), Čáslav 15:56 (typed 55), both `notvia` Libice nad Cidlinou,
  u kostela so the through trips stay on 705.
- (d) 705: out 1/1/1 (15:42), 1 exact and 2 within 3 of 5 (17:41); back 1/1/1 (16:56), 4 exact of 8. 705 Kolín: out 1/1/1 (15:50),
  2 exact of 6; back 1/1/1 (15:56), 2 exact, 4 within 3 of 6. Branch audit ok.
- (e) Poděbrady 12:52 (Toyota), 16:36, Kolín 12:40, 12:50, 14:50 (Toyota start), Čáslav 18:01 (to Volárna), the Kutná Hora shorts,
  the morning. The Toyota stops (Kolín, PZKO-TOYOTA, PZKO - Thermo King, Sendražice, Ovčárecká, Strojírny) are on Kolínsko's town
  lines 235004 / 235006 / 235007 and 706.
- (f) 3 + 2 buses (139 / 141 min, waits 55 at Čáslav, 25 at Poděbrady; 74 / 74 min, waits 52 at Čáslav, 40 at Kolín).

## Městec Králové

**463 Městec Králové – Rožďalovice – Dobrovice – Mladá Boleslav**
- (a) Městec Králové, náměstí; Rožďalovice, náměstí; Mladá Boleslav, autobusové stanoviště; Rožďalovice, Hasina.
- (b) Městec → Mladá Boleslav 5:55, 9:15, 13:45, 15:45, 17:15, 19:45; Mladá Boleslav → Městec 9:05, 13:05, 14:30, 18:05 and → Rožďalovice
  5:15, 6:30, 11:05, 16:05, 22:25; Rožďalovice → Mladá Boleslav 4:06, 7:51, 12:11; Rožďalovice → Městec 5:02, 13:07; Městec 12:15 →
  Rožďalovice; Rožďalovice 14:31 → Hasina; Hasina 6:40 → Městec.
- Anchor 16:00 by hand: the default (13:30, window 13:00–15:00) is the 13:07 short, the 14:31 Hasina trip and the 14:30 extra,
  and its Mladá Boleslav slot would be empty; the line's own two-hourly pattern runs from 15:45 (the 282 rule).
- (c) **463** every 120: Městec 15:45 (typed 44); Mladá Boleslav 16:05 read to Rožďalovice, náměstí (`core_to`; typed 64).
  **463 Hasina** every 480: Rožďalovice, náměstí 14:31 → Hasina (typed 330), Hasina 14:40 → náměstí (typed 339; the real 6:40,
  480 min earlier): Hasina, Hasina, Stará Hasina and Rožďalovice, ústav have no other line.
- (d) 463: out 1 slot / 2 real (15:45, 17:15) / 1 filled, 3 exact of 6; back 1/1/1 (16:05), 2 exact of 9. Branch audit ok. 463
  Hasina: no window slots (named in the why).
- (e) Městec 17:15 (30 off), 9:15; Mladá Boleslav 13:05, 14:30, the morning; the Městec – Rožďalovice shorts listed.
- (f) 2 + 1 buses (90 / 90 min, waits 50 at Mladá Boleslav, 10 at Městec; Hasina 5 / 7 min).

**538 Městec Králové – Dymokury – Křinec**: (a) Městec Králové, náměstí; Křinec, náměstí. (b) Every 2 h all day, Městec :49
(9:49–19:49), Křinec :33 (8:33–18:33), exact; morning trips and 21:33. (c) **538** every 120, typed 48 / 92. (d) 1/1/1 both
ways; 6 exact of 9 each way. (f) 1 bus (28 / 28; waits 16 at Křinec, 48 at Městec). Křinec, železniční stanice has no other line.

**599 Městec Králové – Opočnice – Dobšice**: (a) Městec Králové, náměstí; Opočnice; Dobšice, Libněves. (b) Every 2 h all day:
Městec :10 at even hours, Libněves :12 at odd hours (6:15, 5:17, 7:07 morning, 5 off). (c) **599** every 120, typed 69 / 11. Its
reading lists no stop of its own (all on 541, 542, 543, 598), but Step 8 folds sparse and shift lines; 599 runs 15 trips a day,
every 2 h, so it is a line of its own (1 bus). (d) 1/1/1 both ways; 5 exact of 6, 5 of 7. (f) 1 bus (27 / 27; waits 35 / 31).

**853 Městec Králové – Nový Bydžov (Královéhradecký kraj)**
- (a) Městec Králové, náměstí; Hlušice, kulturní dům; Nový Bydžov, Terminál HD.
- (b) One bus all afternoon: Městec 13:00 → round the Hlušice spur → Nový Bydžov 13:49; Nový Bydžov 14:25 → direct → Městec 14:58;
  Městec 15:05 → Hlušice → Nový Bydžov 15:54; Nový Bydžov 17:02 → Hlušice → Městec 17:45. Morning 4:35, 6:10, 6:41, 7:16, 7:46,
  11:02.
- (c) **853** every 240: Městec 15:05 (typed 124), Nový Bydžov 17:02 (typed 1) by the 17:02's path via Hlušice (`stops_via`, 43
  min). Every 120 fails Step 4 (the Městec 17:00 and Nový Bydžov 16:25 window slots have no trip; 13:00 → 15:05 and 14:25 → 17:02
  are not 2 h apart), every 240 holds one exact round with 1 bus.
- (d) Out: no window slot (15:05 stands for itself); back 1/1/1 (17:02). Path audit clean after `stops_via`.
- (e) Městec 13:00, Nový Bydžov 14:25, the morning.
- (f) 1 bus (49 / 43 min; waits 68 at Nový Bydžov, 80 at Městec). All 13 stops past Sloveč, Střihov (Královéhradecký kraj) are on
  the line.
- **Changed on 2 Nov** (review): one sentence on the card: a four-leg circuit every 480 (13:00, 14:25, 15:05, 17:02, all exact)
  would hold all four afternoon trips for the same 1 bus, at four typed entries instead of two. The design is unchanged.

## Summary

| Line | Simutrans lines | Every | Slots (real) | Buses |
|---|---|---|---|---|
| 398 | 398 | 30 | Poděbrady :08 :38; Praha, Černý Most :15 :45 | 5 |
| 425 | 425 | 120 | Praha 15:10; Trutnov 16:27 | 3 |
| 430 | 430 | 60 | Lysá :36; Lipník :07 | 3 |
| 432 | 432 | 120 | Lysá 16:01; Mladá Boleslav 16:03 | 2 |
| 433 | 433; 433 Zálabí | 60; 60 | Nymburk :04, Pečky :15; Nymburk, hl.nádraží :34, Zálabí :00 | 2 + 1 |
| 434 | 434 | 60 | Nymburk :24; Benátky :34 | 3 |
| 436 | 436 | 60 | Nymburk :20; Lipník :21 | 2 |
| 443 | 443 | 60 | Nymburk :02; Čelákovice, Toušeňská :55 | 3 |
| 463 | 463; 463 Hasina | 120; 480 | Městec 15:45, Mladá Boleslav 16:05; Rožďalovice 14:31, Hasina 14:40 | 2 + 1 |
| 493 | 493 | 60 | Nymburk :04; Poděbrady :30 | 1 |
| 497 | 497; 497 Kamenné Zboží | 60; 480 | Nymburk :40, Milovice :25; Nymburk 14:19, Kamenné Zboží 14:33 | 2 + 1 |
| 498 | 498 | 60 | Poděbrady :20; Pečky :15 | 2 |
| 499 | 499 | 60 | Nymburk :05; Mladá Boleslav :45 | 3 |
| 538 | 538 | 120 | Městec 15:49; Křinec 16:33 | 1 |
| 539 | 539 | 60 | Poděbrady :12; Křečkov :31 | 1 |
| 540 | 540 | 60 | Poděbrady :08; Záhornice :07 (Dymokury :22) | 2 |
| 541 | 541 (circuit) | 120 | Nymburk 16:09 → Dlouhopolsko; Dlouhopolsko 15:46; Nymburk 15:09 → Městec; Městec loop 16:15; Městec 17:05 | 3 |
| 542 | 542 | 120 | Poděbrady 16:15; Rožďalovice 16:44 | 2 |
| 543 | 543 | 120 | Poděbrady 16:55; Hradčany 16:13 | 1 |
| 585 | 585 (circuit) | 180 | Poděbrady 16:24; Jičín 14:35 → Chroustov; Chroustov 15:16; Jičín 16:35 | 2 |
| 598 | 598 (circuit) | 120 | Poděbrady 16:15 → Nová Ves; Nová Ves 15:39; Poděbrady 17:15 → Dubečno; Dubečno 16:47 | 3 |
| 599 | 599 | 120 | Městec 16:10; Dobšice, Libněves 17:12 | 1 |
| 673 | 673 | 120 | Nymburk 17:05; Křinec, škola 16:09 (Sovenice 16:15) | 1 |
| 674 | 674 | 120 | Nymburk 16:05; Rožďalovice, náměstí 15:49 | 2 |
| 676 | 676; 676 Seletice | 120; 120 | Nymburk 16:00, Loučeň 17:19; Nymburk 17:00, Seletice 16:06 | 1 + 1 |
| 678 | 678 | 120 | Poděbrady 16:05; Pečky 17:14 | 1 |
| 679 | 679 | 120 | Kolín 16:00; Poděbrady 17:10 | 1 |
| 705 | 705; 705 Kolín | 120; 120 | Poděbrady 15:42, Čáslav 16:56 (Kolín 18:10); Kolín 15:50, Čáslav 15:56 | 3 + 2 |
| 833 | 833; 833 Nymburk | 120; 480 | Pečky 16:12 17:15, Sadská 15:33 16:33; Nymburk 13:34, Sadská 14:39 | 1 + 1 |
| 853 | 853 | 240 | Městec 15:05; Nový Bydžov 17:02 | 1 |
| 897 | 897 | 120 | Lysá 15:47; Kostomlaty 16:50 | 1 |
| **31 lines** | **37 Simutrans lines** | | | **68** |

Owner checks (3): (1) 430 + 436 pooled at Lipník, 4 buses instead of 5, if the live map shows it; (2) coverage near stops of the
same place: Jičín, železniční stanice as an exception (recommended; or the invented hop, 0 buses, or every 480, +1 bus) and
833 Nymburk kept (rule; or four coverage exceptions, −1 bus); (3) 434 and 433's Nymburk town trips as one ring, 3 buses for both
instead of 4, if the live map shows the 434 buses on the :34 / :00 town trips (497 is the other candidate). Buses: 68 as
modelled; 65 if the owner takes all three options.

## Shared stops: same-minute departures (check 6)

Every timed slot of the sheet is a real departure minute (all window slots exact), so no same-minute departure below is made by
the model; each is in the real timetable, on a different road or as the real pulse after the trains:
- Nymburk, hl.nádraží: 433 and 493 both leave :04 (to Pečky and to Poděbrady; they share V Kolonii – nemocnice – náměstí –
  Zálabí, as in reality); 499 :05 with 673 :05 at odd hours and 674 :05 at even hours (three roads); 443 :02, 541 :09, 436 :20,
  434 :24, 433 Zálabí :34, 497 :40, 676 / 676 Seletice :00.
- Pečky, železniční stanice: 433, 498 and 833's 17:15 leave :15 (to Nymburk, Poděbrady and Sadská); 678 :14 at odd hours.
- Poděbrady, železniční stanice: 398 and 540 both leave :08 (Prague road and Pátek road); 539 :12, 542 and 598 :15 (at even hours
  both, e.g. 16:15, as in the timetable; they share the road to Choťánky, Vrčení, then 542 turns to Pátek, Nové Mlýny and 598 to
  Odřepsy), 678 :05 at even hours, 679 :10 at odd hours, 498 :20, 585 :24, 493 :30, 705 :42, 543 :55.
- Ex4 pairs and circuits do not coincide: 676 and 676 Seletice alternate at Nymburk :00 and at Loučeň :19 / :31; 705 and
  705 Kolín alternate at Kolín (:50 out, :10 in); 598's two ends alternate at Poděbrady :15 and 541's at Nymburk :09; 833 and
  833 Nymburk meet at Sadská at different minutes (14:07 / 14:39 against :24 / :33); 463 and 463 Hasina at Rožďalovice
  (16:11 / 17:07 against 14:31 / 14:47).

## Other okresy and other sheets (for the `--final` pass)

Stops of other Středočeský okresy served 13:00–19:00 that no other oblast's line serves, so only this sheet covers them (all are
on the lines above): okres Kolín: Ratenice (498); Pečky, kulturní dům (433, 498); Žehuň, u rybníka (543, 599); Cerhenice,
Cerhenice, Za Dráhou (678); Pňov-Předhradí, Předhradí, Pňov, Klipec, Velim, železniční stanice, Velim, Vítězov, Křečhoř, Kamhajek
(679); Velký Osek, škola, Velký Osek, Šanghaj, Červené Pečky, železniční stanice, Dobešovice, Amálka, Dolany, Čertovka (705).
Okres Kutná Hora: Miskovice, Hořany, Kutná Hora, Perštejnec, rozcestí, Kutná Hora, Neškaredice, Třebešice [KH] (705). Okres
Mladá Boleslav: Lipník (430, 436); Všejany, Všejany, Vanovice, Čachovice, Vlkava, náves, Vlkava, Bor, Smilovice, Bratronice,
Luštěnice, Dobrovice, Libichov, hlavní silnice (432); Vlkava, kulturní dům, Čachovice, železniční stanice, Čachovice, Struhy,
Hostinec, Čachovice, Struhy (436); Prodašice, křižovatka (463); Dobrovice, Holé Vrchy, Ctiměřická, Ctiměřice, Semčice, zdravotní
středisko, Pěčice, Jabkenice, Jabkenice, křižovatka, Chudíř (499). Okres Praha-východ: Čelákovice, rozcestí Sedlčánky (443).

Uncovered here but served by another oblast's lines (checked in their trips): Charvatce, Charvatce, na pile (499's 13:40
variant; Mladoboleslavsko 764); Kolín, PZKO-TOYOTA, PZKO - Thermo King, Sendražice, Ovčárecká, Strojírny (705's Toyota trips;
Kolínsko 235004 / 235006 / 235007, 706). Mcely is also on Mladoboleslavsko's 764, and is covered here by 676 Seletice.

Stops outside the Středočeský kraj: 35 served 13:00–19:00 (425, 585, 853), all on this sheet's lines except Jičín, železniční
stanice (owner check 2).

## Script notes (not patched)

- `run_oblast.py` had an f-string broken across lines (line 40, "unterminated f-string literal") from about 05:20; the
  coordinator fixed it, and every run above is with the fixed script.
- Knot check on sparse legs: for a leg with no window slot the model times are taken from the slot residues (`real`, 0:00–every)
  instead of clock times near the real trips, so the card shows deviations of 120–720 min (463 Hasina, 497 Kamenné Zboží, 585's
  Chroustov legs, 833 Nymburk, 853). The slots themselves are right (the run's own "no slot in the window" check finds the real
  trip for each).
- Knot check on a leg whose trips take two paths uses the median offset of all the leg's whole trips, not the row's `rt` /
  `knot_rt`, so 540's way back and 543 show 5–6 min where the slot trips are exact.
- 541's town loop is a leg with `fr` = `to` (Městec Králové, náměstí → Městec Králové, náměstí). The builder handles it (stops,
  rt 20, pattern_need), but `06_render` has not been run on such a leg yet: untested, not a known bug.
- The draft printout (`--draft`) and the scratch files of parallel designers share one scratchpad folder: a file named
  `draft1.txt` was overwritten by another oblast's run. Worth a per-oblast file name in the brief.

## Open questions

- The 2 Nov live map: decides the 430 / 436 pool at Lipník (owner check 1) and the 434 / 433 Zálabí ring (owner check 3, with
  497 as the other candidate for 434's Nymburk gap), and confirms or corrects the chains named in the notes (497 ↔ 897, 538 → 541,
  432 / 897 → 442, 679 ↔ 821 at Kolín, 434 → 768 at Benátky).
- 0-minute turns (497 Milovice, 497 Kamenné Zboží, 543 Poděbrady) are typed 1 min before the arrival minute; the entry's Leave up
  to has to let the arriving bus go (the engine question open since the Rakovnicko pilot).
