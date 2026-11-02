# Method check: PID Kutnohorsko (okres Kutná Hora), designed 2 Nov 2026

Every line of the oblast set by hand with the bus schedule method v4 (`mirror/pipeline/bus-schedule-method.md`), the brief
(`pid-regional/DESIGN_BRIEF.md`, including "Learned on the pilot") and the owner's lessons (`kb/lessons.md`). The design is
`lines.json`; the builder's result is `data/derived/schedule.json`; the audits are `data/derived/audit-step4.md`,
`audit-branch.txt` and `audit-path.txt`.

- **Data:** PID GTFS of 1 Nov 2026, service day Mon 2 Nov 2026 (school day). For each line I read
  `data/derived/reading/<L>.txt` in full (every trip 5–23 at the core points, the paths, the 0–5 minute chain test) and,
  where a path or a time mattered, the trips themselves in `data/derived/trips.json`. The live map (2 Nov) had no afternoon
  buses yet when this was written; nothing below rests on plates.
- **Step 4 gate, per direction:** in the Simutrans line's model window the slots equal the real departures ±1, and at least
  80 % of the slots have a real departure within 3 min. Candidates were searched for both directions together (every
  interval dividing 1440 up to 480, the same 1–3 slots each way, slots on real departures of the afternoon), ranked by
  exact hits over the day 5–23, then within 1 min, then buses, then simplicity. Where that ranking would pull a 2-hourly line
  to a longer interval with more slots, the real 13:00–18:00 headway decided (the Opavsko rule), except where the longer
  interval keeps every real trip exact at no extra bus (788, 481, 746).
- **Result:** 84 timed legs, all pass Step 4 (`audit-step4.md`: 84 ok, 0 EMPTY, 0 MORE, 0 FEWER). No approximate row.
  Branch audit: 4 legs read at a midpoint, all ok. Path audit: 2 flags (481, 746, both explained). Coverage: 586 afternoon stops,
  582 on this sheet's lines; the other 4 are served only by the rail replacement buses XS28 / XS29 (exceptions).
- **Typed values** are (real − 61) mod every (every terminus is a loop), computed by the builder; checked by hand on 381
  (Háje 0:00 → 59; Čáslav :48 → 47), 402 (Roztyly 14:20 → 79; Čáslav 15:36 → 35), 742 (Čáslav 12:13 on 240 → 192) and 776
  (14:15 on 480 → 314).
- **Variants (Step 5 / Step 8):** a short working or variant gets its own Simutrans line where it runs regularly in the
  afternoon (at least 3 trips each way 13:00–19:00, the owner's 30 Oct rule for afternoon branches) or where it is a place's
  only service; sparser variants whose stops are all on modelled lines are listed on their card (561 Řeřichy / 285
  Dobroslavice precedent). No empty-return line anywhere.
- **0-minute turns** kept on their real minutes with `"lay": 0` on the departing leg (brief, tested on the pilot's 573):
  381 at Praha, Háje; 801 at Žižkov, poliklinika; 749 at Souňov and Čáslav, zem.škola; 770 Ostředek at Ostředek; 784 at
  Čáslav, autobusové stanoviště. 1-minute turns (783 Žehušice, 743, 788, 772) are taken by the builder from the slots.

## Script problems

1. `pid-regional/scripts/run_oblast.py` line 40 had a literal newline inside an f-string (`print(f"` + newline +
   `coverage: …`), a SyntaxError from the edit of 2 Nov 05:22 until the coordinator fixed it. My first runs went through an
   in-memory copy with that one string repaired (file untouched); every run after the fix used the script as it is.
2. The builder's running time is the median of the leg's trips near the window, which mixes paths: 749's Souňov →
   zem.škola gave 26 (the 13:56 runs via Vodranty in 30, the slot trip 15:56 direct in 21) and 784's Horka → Čáslav 30
   (14:20 runs 27, 15:25 via Semtěš 33). Both set by hand (`rt`) to the slot trip's own time; with the medians each line
   needs one bus more. Known from the pilot.
3. `path_check.py` flags a slot trip only for stops it serves off the modelled path, not for modelled stops it skips. So
   the legs shown via a variant stop (`stops_via`: 687 via Obrvaň, 785 via Všesoky, 746's way out via Polánka, 786 via
   Perštejnec, 710's two Heřmanův Městec stops) pass the audit although some of their slot trips run the other path; each
   is named in the line's `why`.
4. The scratchpad folder is shared by the parallel designer sessions (a sibling overwrote a helper file and one output file
   received another oblast's run). Not a pipeline script, but worth knowing: I kept everything in `scratchpad/kutnohorsko/`.

## Changed on 2 Nov after the review (`review-2026-11-01.md`: 29 PASS, 6 FIX, 1 ASK OWNER)

- **746:** every 120 (15:16 / 15:35) → every 240 with two slots each way, Uhlířské Janovice 13:08, 15:16 and Čáslav 15:35,
  18:05: the real pairs of the line's two buses, all four afternoon trips and the 11:16 exact (5 against 3), the same 2 buses.
  Typed 7 / 135 and 154 / 64. The variant paths sit on opposite slots (out: 13:08 via Polánka, 15:16 via Golf; back: 15:35
  via Polánka, 18:05 via Golf), so the way out is now shown via Malešov, Polánka (the 13:08's path, 77 min) and the way back
  via Vidice, Roztěž, Golf (the 18:05's path, 69 min). With Golf kept on the way out (the review's wording) the builder times
  the way back at the 15:35's 77 min, the 18:05 misses its 19:16 repeat by 6 min and the line needs 3 buses. Both variants
  stay covered; the path audit flags the 15:35 (via Polánka on a leg shown via Golf), named in the why.
- **742:** the way out reads to Zbýšov (`core_to`, with `notvia` Dobrovítov, Dědice, which is 742 Dobrovítov's trip) in the
  2-hour window 14:30–16:30, so the 16:13 slot stands for the counted real 16:13 Zbýšov short instead of passing through a
  4-hour window. Typed values and the bus unchanged; branch audit clean.
- **749:** the why no longer claims a 0-minute turn at zem.škola: the real 743 runs on to the bus station (16:21) and another
  bus starts the real 16:17; the game bus turns there. On the live-map list in `notes`.
- **776:** the loop direction on the card is corrected: the 14:15 runs Zruč → Horka II → Vlastějovice → Pertoltice,
  Machovice → Pertoltice → Dolní Pohleď → Zruč (the morning loop runs the other way round). The builder's stop list was
  already right.
- **783 / 801:** the pooling owner check is deleted (pooling is offered on the card, never asked). The 783 circuit (2 buses
  instead of 3) is in 783's note, 801 pooled with 801 Vrchlice (7 → 6, Lutan's real count) in 801's, both with their chains
  on the live-map list in `notes`.
- **805:** my claim that no pattern passes the short workings was wrong: the search mixed the Karlov and bus-station ends.
  Read alone, Kolín ↔ Kutná Hora, autobusové stanoviště (5 out / 3 back 13–19, the surplus towards the Kutná Hora garage)
  passes every 120 with one slot each way in 13:45–15:45 at the inbound rate: Kolín 13:57, bus station 15:26 (typed 56 / 25),
  1 bus. Still listed as designed; now on the owner checks (+1 bus).

## Set by hand (and why)

- **Anchors / windows** (the auto 16:00 window would hold a shifted trip or none): 402 anchor 14:30 (window 14:00–16:00,
  the 16:00 window holds only the 16:35 from Roztyly, 15 min off its :20); 533 window 14:00–16:00 (17:16 shifted); 710
  anchor 14:40 (no Chrudim 16:42); 740 anchor 15:00 (Golčův Jeníkov 17:05 is 5 off its :00); 783 and 783 Chvaletice
  14:00–16:00, 783 Žehušice 15:30–17:30; 786 14:00–16:00 (no Paběnice departure after 15:24); 805 14:30–16:30; 781
  Potěhy and 741 14:30–16:30; 742 14:30–16:30 (with `core_to` Zbýšov, so the 16:13 repeat stands for the real Zbýšov short);
  742 Dobrovítov 13:00–15:00; 749 14:00–16:00; 743 15:30–17:30; 746 14:30–16:30; 771 13:00–17:00 (one period of its
  every-240 circuit); 771 Kácov 12:00–14:00; 772 14:00–16:00; 772 okruh 12:30–14:30; 776 14:00–16:00; 778 14:30–16:30.
- **Running times:** 749 Souňov → zem.škola 21 (auto 26); 784 Horka → Čáslav 27 (auto 30); 785 Kolín → Kácov 88 (the
  13:25 trip, shown via Všesoky, auto 93): with 93 the bus misses the real 2-minute turn at Kácov and the line needs 3
  buses; in the game the 5-minute detour is absorbed by the entry's automatic Leave up to and the 50-minute wait at Kolín.
- **`notvia` / `via`:** 801 trunk `notvia` Starý Kolín and Hlízov (those trips are 801 Starý Kolín); 783 Žehušice `notvia`
  Kutná Hora, autobusové stanoviště (keeps the through trips on 783); 782 `notvia` / 782 Horka `via` Horka I, Svobodná
  Ves, střed; 781 Potěhy's way back (741 trips) `notvia` Zbýšov, Chlum (the Chlum trips also pass Potěhy); 770 Ostředek
  `notvia` Uhlířské Janovice.
- **`stops_via`** (a stop only a slot trip's path serves): 710 out via Heřmanův Městec, nádraží / back via náměstí; 746 out via
  Malešov, Polánka (the 13:08) and back via Vidice, Roztěž, Golf (the 18:05); 687 back via Obrvaň and Habrek (the 12:58 = 13:01 slot trip); 785 via
  Chlístovice, Všesoky (the 15:25); 786 via Kutná Hora, Perštejnec (the 14:15 slot trip); 771 Sázava → Soběšín via Ledečko
  (the 14:30 slot trip).
- **`core_to` / `knot`:** 742 `core_to` Zbýšov (`notvia` Dobrovítov, Dědice); 778 `core_to` Bohdaneč (the 16:30 ends there, run on to Zbraslavice); 801 Starý Kolín out
  `core_to` Hlízov, u váhy (the 16:44 ends there) and back read at the knot Hlízov, u váhy :40 (the 17:40 starts there;
  Starý Kolín :35 = :40 − 5).
- **`lines` (rings):** 781 Potěhy back on 741's trips; 749 back on 743's; 743 back on 749's.

## Line by line

Each entry: (a) core points, (b) the whole day at them, (c) the Simutrans lines and why, (d) Step 4 per leg (from
`schedule.json`), (e) off the pattern, (f) buses and terminal waits.
### 381
- (a) Praha, Háje; Zásmuky, náměstí; Kutná Hora, hlavní nádraží; Čáslav, železniční stanice; Čáslav, obchodní centrum.
- (b) Háje → Čáslav, obchodní centrum exactly :00 hourly 5:30–17:00 (18:00, 20:00, 22:05 to Čáslav, autobusové stanoviště); Čáslav, obchodní centrum → Háje exactly :48 4:48–17:48, 19:49. Háje – Zásmuky extras at :30 (14:30, 15:30, 16:30, 17:30; back 16:21; first trips 4:21, 4:51 start at Zásmuky, last 0:05 ends there: the Zásmuky garage), Kutná Hora, hlavní nádraží → Háje 11:10, 13:40, 14:40, 22:11 and Háje → Kutná Hora 5:45, 9:00, 11:00, 19:00. Chain test: 19 of 23 arrivals at Háje leave again within 0–5 min as 381 (the :00 arrival is the :00 departure); 2 of 4 at Kutná Hora, hlavní nádraží with 801.
- (c) One line every 60, both ends exact (every 30 would leave the Zásmuky half empty beyond Zásmuky; the Zásmuky extras are one-way outflow of garage buses, all on 381's stops, so no line for them). 0-minute turn at Háje with `lay` 0 (5 buses; with a 3-minute wait it would be 6).
- (d) **381** every 60:
  - Praha, Háje → Čáslav, obchodní centrum: window 15:30–17:30 slots 16:00, 17:00 / real 16:00, 17:00, 2 of 2 with a real departure within 3 min; over the day 10 exact, 10 within 3 of 11 (rt 132, wait before 0)
  - Čáslav, obchodní centrum → Praha, Háje: window 15:30–17:30 slots 15:48, 16:48 / real 15:48, 16:48, 2 of 2 with a real departure within 3 min; over the day 11 exact, 12 within 3 of 12 (rt 132, wait before 3)
- (e) Off the pattern: Háje :30 to Zásmuky (4), Zásmuky 16:21, Kutná Hora 13:40, 14:40 → Háje, Háje 18:00 / 19:00 shorts; nothing within the 13–19 trunk pattern is missing.
- (f) 381: 5 buses (waits Háje 0, obchodní centrum 36)

### 387
- (a) Praha, Háje; Kostelec nad Černými lesy, náměstí; Uhlířské Janovice, náměstí.
- (b) Háje → Uhlířské Janovice :10 hourly 14:10–18:10 (13:30, 19:30, 21:05, 23:05); Uhlířské Janovice → Háje 12:12, 13:12, 14:57, 15:57, 17:12, 19:42, and every 30–60 min in the morning from 4:27: the buses sleep at Uhlířské Janovice (outstation with a Prague end). Kostelec shorts 4:05, 7:00, 18:30.
- (c) Modelled at 16:00 at the rate of the trips towards Prague in the window (15:57, 17:12): hourly. Hourly :57 leaves 16:57 empty (17:12 is 15 off) and fails; every 120 with two slots each way passes exactly. Every 180 with three slots each way (Uhlířské Janovice 14:57, 15:57, 17:12) also passes with two more exact hits over the day, but its repeat at 14:12 leaves Uhlířské Janovice on the same minute as 770 (both run via Staňkovice), a departure the timetable does not have; every 120 repeats at 13:12 (real), 13:57, 15:12, 17:57 instead, so it was chosen. Háje's two slots fold to every 60 :10.
- (d) **387** every 120:
  - Praha, Háje → Uhlířské Janovice, náměstí: window 15:30–17:30 slots 16:10, 17:10 / real 16:10, 17:10, 2 of 2 with a real departure within 3 min; over the day 5 exact, 5 within 3 of 10 (rt 79, wait before 3)
  - Uhlířské Janovice, náměstí → Praha, Háje: window 15:30–17:30 slots 15:57, 17:12 / real 15:57, 17:12, 2 of 2 with a real departure within 3 min; over the day 4 exact, 4 within 3 of 11 (rt 78, wait before 3)
- (e) Off the pattern: Uhlířské Janovice 12:12, 14:57 (15 min), 19:42; Háje 13:30, 19:30 (20 min), the Kostelec shorts. The slots 13:57 and 15:12 at Uhlířské Janovice have no trip (outstation: the line runs at the inbound rate).
- (f) 387: 4 buses (waits Háje 40/55, náměstí 43/28)

### 402
- (a) Praha, Roztyly; Zruč nad Sázavou, Sázavan; Zbraslavice, náměstí; Čáslav, autobusové stanoviště.
- (b) Roztyly → Čáslav :20 of even hours 8:20–14:20 (6:50, then 16:35, 20:25); Čáslav → Roztyly :36 of odd hours 9:36–17:36 (6:51, 14:36); Roztyly → Zruč 15:20, 17:35, 18:20 and Zruč → Roztyly 4:24, 6:29 (buses sleeping at Zruč). Chain test: 5 of 10 departures at Roztyly follow a 197 arrival (city line, Prague sheet).
- (c) Every 120 at the line's own whole-day pattern, window 14:00–16:00 set by hand. Considered: the inbound-rate reading of that window (Čáslav 14:36 and 15:36 towards Prague) would make it hourly, with the Zruč shorts run on to Čáslav: 5 buses and Roztyly → Čáslav departures the timetable does not have, against one real extra (14:36); rejected. In the 16:00 window every 120 at 16:35 / 15:36 passes too but moves Roztyly off its :20 for one shifted trip (6 exact against 9).
- (d) **402** every 120:
  - Praha, Roztyly → Čáslav, autobusové stanoviště: window 14:00–16:00 slots 14:20 / real 14:20, 1 of 1 with a real departure within 3 min; over the day 4 exact, 4 within 3 of 7 (rt 124, wait before 3)
  - Čáslav, autobusové stanoviště → Praha, Roztyly: window 14:00–16:00 slots 15:36 / real 14:36, 15:36, 1 of 1 with a real departure within 3 min; over the day 5 exact, 5 within 3 of 7 (rt 124, wait before 3)
- (e) Off the pattern: Roztyly 16:35 (15 min), 20:25; Čáslav 14:36; the three Zruč shorts and the morning Zruč starts (all stops on 402).
- (f) 402: 3 buses (waits Roztyly 40, autobusové stanoviště 72)

### 801
- (a) Kutná Hora, hlavní nádraží; Kutná Hora, Žižkov, poliklinika; Starý Kolín, železniční zastávka; Kutná Hora, Vrchlice, V Cihelně.
- (b) A town line every 15 min. hlavní nádraží → poliklinika :05, :20 every hour, :35 of odd hours, and the Starý Kolín trip passing at :50 (Starý Kolín :35, Hlízov :40); :35 of even hours goes to Vrchlice, V Cihelně (12:35, 14:35, 16:35). poliklinika → hlavní nádraží :29, :59 every hour and :14 of even hours; :44 every hour to Starý Kolín (16:44 to Hlízov, u váhy only); Vrchlice → hlavní nádraží :11 of odd hours. From Hlízov 11:40 and 17:40 (the 17:35 from Starý Kolín does not run). Chain test: 46 of 56 arrivals at poliklinika leave again within 0–5 min (0-minute turns).
- (c) Three Simutrans lines (Ex4, one per end): 801 every 120 with five slots each way (the trunk; `notvia` Starý Kolín and Hlízov so the through trips stay on their line), 801 Starý Kolín every 60 (`core_to` / knot Hlízov, u váhy so 16:44 and 17:40 count), 801 Vrchlice every 120 (the only service of V Cihelně). Together hlavní nádraží → Žižkov runs :05, :20, :35, :50 as in reality, and the :35 alternates poliklinika / Vrchlice by hour. 0-minute turns at poliklinika (`lay` 0). One trunk bus waits 117 min at hlavní nádraží each period (out :05, :20 and :35 odd, back :29, :59 and :14 even: the even-hour :23 arrival has no trunk departure until the next :20); in reality that bus runs the Vrchlice round. Pooling 801 with 801 Vrchlice saves 1 bus (7 → 6), on the card, not asked.
- (d) **801** every 120:
  - Kutná Hora, hlavní nádraží → Kutná Hora, Žižkov, poliklinika: window 15:30–17:30 slots 15:35, 16:05, 16:20, 17:05, 17:20 / real 15:35, 16:05, 16:20, 17:05, 17:20, 5 of 5 with a real departure within 3 min; over the day 34 exact, 35 within 3 of 39 (rt 24, wait before 3)
  - Kutná Hora, Žižkov, poliklinika → Kutná Hora, hlavní nádraží: window 15:30–17:30 slots 15:59, 16:14, 16:29, 16:59, 17:29 / real 15:59, 16:14, 16:29, 16:59, 17:29, 5 of 5 with a real departure within 3 min; over the day 31 exact, 36 within 3 of 40 (rt 24, wait before 0)
- (d) **801 Starý Kolín** every 60:
  - Kutná Hora, Žižkov, poliklinika → Starý Kolín, železniční zastávka: window 15:30–17:30 slots 15:44, 16:44 / real 15:44, 16:44, 2 of 2 with a real departure within 3 min; over the day 11 exact, 11 within 3 of 13 (rt 39, wait before 3)
  - Starý Kolín, železniční zastávka → Kutná Hora, Žižkov, poliklinika: window 15:30–17:30 slots 15:35, 16:35 / real 15:35, 16:35, 2 of 2 with a real departure within 3 min; over the day 10 exact, 10 within 3 of 14 (rt 39, wait before 3)
- (d) **801 Vrchlice** every 120:
  - Kutná Hora, hlavní nádraží → Kutná Hora, Vrchlice, V Cihelně: window 15:30–17:30 slots 16:35 / real 16:35, 1 of 1 with a real departure within 3 min; over the day 5 exact, 5 within 3 of 7 (rt 27, wait before 3)
  - Kutná Hora, Vrchlice, V Cihelně → Kutná Hora, hlavní nádraží: window 15:30–17:30 slots 17:11 / real 17:11, 1 of 1 with a real departure within 3 min; over the day 5 exact, 6 within 3 of 7 (rt 27, wait before 3)
- (e) Off the pattern: 18:25 (5 min, the evening shift), 18:46 to Malín, the Fučíkova early / late trips, 18:30 Starý Kolín → Vrchlice.
- (f) 801: 4 buses (waits hlavní nádraží 117/27/27/12/12, poliklinika 0/15/0/15/15); 801 Starý Kolín: 2 buses (waits poliklinika 30, železniční zastávka 12); 801 Vrchlice: 1 bus (waits hlavní nádraží 57, V Cihelně 9)

### 802
- (a) Kutná Hora, Žižkov, poliklinika; Kutná Hora, autobusové stanoviště; Kutná Hora, Sedlec, Čechova.
- (b) Exactly hourly 8:10–17:10 from poliklinika (to Sedlec, Čechova; 17:10 on to Karlov, Na Rovinách), Čechova :36 8:36–16:36; morning trips to Karlov. One bus.
- (c) Every 60, exact. No stop of its own except Žižkov, u hřbitova, but a regular hourly line, not a sparse one, so it is modelled (Step 8 does not apply).
- (d) **802** every 60:
  - Kutná Hora, Žižkov, poliklinika → Kutná Hora, Sedlec, Čechova: window 15:30–17:30 slots 16:10, 17:10 / real 16:10, 17:10, 2 of 2 with a real departure within 3 min; over the day 11 exact, 11 within 3 of 13 (rt 17, wait before 3)
  - Kutná Hora, Sedlec, Čechova → Kutná Hora, Žižkov, poliklinika: window 15:30–17:30 slots 15:36, 16:36 / real 15:36, 16:36, 2 of 2 with a real departure within 3 min; over the day 9 exact, 10 within 3 of 12 (rt 14, wait before 3)
- (e) Off the pattern: The morning Karlov trips and the 17:34 Na Rovinách → Čechova.
- (f) 802: 1 bus (waits poliklinika 20, Čechova 9)

### 805
- (a) Kolín, nádraží; Kutná Hora, Hlouška, Na Špici; Kutná Hora, Karlov, celní úřad; Zbraslavice, náměstí; Zruč nad Sázavou, Sázavan.
- (b) Kolín → Zruč exactly :57 of odd hours (10:57–16:57; 4:53, 5:57, 8:57 to Zbraslavice); Zruč → Kolín 10:00, 14:36, 15:40, 17:20 (18:30 to Zbraslavice). Every trip passes Na Špici; the Zruč trips pass Karlov. Short workings: Kolín → Kutná Hora, autobusové stanoviště 13:57, 15:27, 16:27, 17:53, 18:57, 19:23 and back 13:06, 13:36, 15:26; Kolín → Karlov 16:03 and back 14:19, 14:49, 17:19. Chain test: 3 of 7 Zruč arrivals go on as 795 (Benešovsko), 2 of 3 Na Špici arrivals as 782.
- (c) 805 every 120 at Kolín 14:57 / Zruč 14:36 (the bus of the 14:30 arrival, 6-minute turn; with 15:40 instead the line needs 3 buses). The short workings, corrected on 2 Nov: my first search read both ends together at Na Špici and found only 3-slot rows with empty slots; the two ends are separate branches (the Karlov shorts turn on the Zruč road, the bus-station shorts leave it at Tylovo divadlo) and are judged alone. Kolín ↔ Karlov is 1 out / 3 back, an inflow: listed. Kolín ↔ autobusové stanoviště is 5 out / 3 back, the surplus towards the garage, and passes every 120 at the inbound rate in 13:45–15:45 (Kolín 13:57, bus station 15:26, 1 bus). Listed as designed (every stop is on 805 or 785); the line is on the owner checks (+1 bus).
- (d) **805** every 120:
  - Kolín, nádraží → Zruč nad Sázavou, Sázavan: window 14:30–16:30 slots 14:57 / real 14:57, 1 of 1 with a real departure within 3 min; over the day 4 exact, 4 within 3 of 5 (rt 93, wait before 3)
  - Zruč nad Sázavou, Sázavan → Kolín, nádraží: window 14:30–16:30 slots 14:36 / real 14:36, 15:40, 1 of 1 with a real departure within 3 min; over the day 1 exact, 1 within 3 of 4 (rt 97, wait before 3)
- (e) Off the pattern: Zruč 15:40, 17:20, 18:30; all Kolín – Kutná Hora and Kolín – Karlov short workings.
- (f) 805: 2 buses (waits nádraží 44, Sázavan 6)

### 785
- (a) Kolín, nádraží; Kutná Hora, autobusové stanoviště; Kutná Hora, Poličany; Kácov, náměstí.
- (b) Kolín → Kácov exactly :25 of odd hours 11:25–17:25; Kácov → Kolín :55 of odd hours 10:59 (4), 12:55, 14:55 (2-minute turn of the 13:25 bus). Kolín 12:35, 14:25 → Poličany, back Poličany 13:09, 14:59 → Kutná Hora only; Kácov – Čestín 14:25, 17:40.
- (c) Every 120, window 13:00–15:00 (the line's auto anchor 13:30). The way out is shown via Chlístovice, Všesoky (the 15:25's path, the only afternoon service of Všesoky) with the 13:25's 88 min (see Set by hand).
- (d) **785** every 120:
  - Kolín, nádraží → Kácov, náměstí: window 13:00–15:00 slots 13:25 / real 13:25, 1 of 1 with a real departure within 3 min; over the day 4 exact, 4 within 3 of 4 (rt 88, wait before 3)
  - Kácov, náměstí → Kolín, nádraží: window 13:00–15:00 slots 14:55 / real 14:55, 1 of 1 with a real departure within 3 min; over the day 2 exact, 2 within 3 of 3 (rt 100, wait before 2)
- (e) Off the pattern: The Poličany trips (one-way, their stops on 785) and the Kácov – Čestín shorts.
- (f) 785: 2 buses (waits nádraží 50, náměstí 2)

### 783
- (a) Kutná Hora, autobusové stanoviště; Žehušice, škola; Čáslav, autobusové stanoviště; Chvaletice, u městského úřadu; Bernardov.
- (b) Kutná Hora → Čáslav 9:06, 12:16, 14:16, 16:06, 18:06; Čáslav → Kutná Hora 9:38, 12:48, 14:48, 16:43. Čáslav – Žehušice shorts make Čáslav – Žehušice hourly with the trunk: Čáslav 13:48, 15:43, 17:43, Žehušice 14:10, 16:05, 18:05 (1-minute turns). Chvaletice exactly every 2 h (Kutná Hora 13:06, 15:06, Chvaletice 14:21, 16:21; one bus). Bernardov shorts 7:42, 11:21, 17:06 / 8:27, 12:27 (Bernardov is on the trunk path, so it is covered). Horka trips 4:14, 6:29, 6:42, 18:43. Chain test: 4 of 12 Kutná Hora arrivals go on as 533, 4 of 7 533 departures follow a 783 arrival.
- (c) Three lines every 120: 783 (Kutná Hora 14:16 / Čáslav 14:48), 783 Žehušice (3 trips each way, regular), 783 Chvaletice (only service of Chvaletice, Pardubický kraj). The Bernardov shorts are listed. Pooling option on the card (not asked): the trunk and the shorts chain at Čáslav with 12- and 21-minute turns, one circuit, 2 buses instead of 3; on the live-map list.
- (d) **783** every 120:
  - Kutná Hora, autobusové stanoviště → Čáslav, autobusové stanoviště: window 14:00–16:00 slots 14:16 / real 14:16, 1 of 1 with a real departure within 3 min; over the day 2 exact, 2 within 3 of 5 (rt 78, wait before 3)
  - Čáslav, autobusové stanoviště → Kutná Hora, autobusové stanoviště: window 14:00–16:00 slots 14:48 / real 14:48, 1 of 1 with a real departure within 3 min; over the day 2 exact, 2 within 3 of 4 (rt 75, wait before 3)
- (d) **783 Žehušice** every 120:
  - Čáslav, autobusové stanoviště → Žehušice, škola: window 15:30–17:30 slots 15:43 / real 15:43, 1 of 1 with a real departure within 3 min; over the day 2 exact, 2 within 3 of 6 (rt 21, wait before 3)
  - Žehušice, škola → Čáslav, autobusové stanoviště: window 15:30–17:30 slots 16:05 / real 16:05, 1 of 1 with a real departure within 3 min; over the day 2 exact, 2 within 3 of 5 (rt 17, wait before 1)
- (d) **783 Chvaletice** every 120:
  - Kutná Hora, autobusové stanoviště → Chvaletice, u městského úřadu: window 14:00–16:00 slots 15:06 / real 15:06, 1 of 1 with a real departure within 3 min; over the day 2 exact, 2 within 3 of 3 (rt 32, wait before 3)
  - Chvaletice, u městského úřadu → Kutná Hora, autobusové stanoviště: window 14:00–16:00 slots 14:21 / real 14:21, 1 of 1 with a real departure within 3 min; over the day 2 exact, 2 within 3 of 3 (rt 32, wait before 3)
- (e) Off the pattern: Kutná Hora 16:06, 18:06 (10 min), Čáslav 16:43 (5), Čáslav 13:48 and Žehušice 14:10 (5), the Bernardov and Horka trips.
- (f) 783: 2 buses (waits autobusové stanoviště 13, autobusové stanoviště 74); 783 Žehušice: 1 bus (waits autobusové stanoviště 81, škola 1); 783 Chvaletice: 1 bus (waits autobusové stanoviště 13, u městského úřadu 43)

### 782
- (a) Kutná Hora, autobusové stanoviště; Horka I, Svobodná Ves, střed; Žehušice, škola; Vrdy, kulturní dům.
- (b) Hourly. Kutná Hora → Vrdy 12:46 (direct), 13:46 (via Horka I, 55 min), 14:46 (from Fučíkova 14:39, direct), 15:41 (via Horka I), 16:41 (from Fučíkova 16:34, direct), 17:41 (to Horka I only), 18:41 (direct); Vrdy → Kutná Hora 12:44, 13:48, 14:44, 15:43, 16:43, 17:43, all direct (45 min).
- (c) The odd hours run via Horka I, the even hours direct, so two lines every 120 (Ex4, one per path) instead of one hourly line that would show half its slots on the wrong road: 782 (`notvia` Horka I) and 782 Horka (`via`). Together hourly :41 / :43, each one bus (the same 2 buses as one hourly line).
- (d) **782** every 120:
  - Kutná Hora, autobusové stanoviště → Vrdy, kulturní dům: window 15:30–17:30 slots 16:41 / real 16:41, 1 of 1 with a real departure within 3 min; over the day 2 exact, 2 within 3 of 6 (rt 45, wait before 3)
  - Vrdy, kulturní dům → Kutná Hora, autobusové stanoviště: window 15:30–17:30 slots 15:43 / real 15:43, 1 of 1 with a real departure within 3 min; over the day 2 exact, 2 within 3 of 5 (rt 45, wait before 3)
- (d) **782 Horka** every 120:
  - Kutná Hora, autobusové stanoviště → Vrdy, kulturní dům: window 15:30–17:30 slots 15:41 / real 15:41, 1 of 1 with a real departure within 3 min; over the day 1 exact, 1 within 3 of 2 (rt 55, wait before 3)
  - Vrdy, kulturní dům → Kutná Hora, autobusové stanoviště: window 15:30–17:30 slots 16:43 / real 16:43, 1 of 1 with a real departure within 3 min; over the day 2 exact, 4 within 3 of 4 (rt 47, wait before 3)
- (e) Off the pattern: 12:46, 13:46, 14:46 and 13:48 (5 min: before 15:00 the line runs at :46 / :48); 17:41 to Horka I.
- (f) 782: 1 bus (waits autobusové stanoviště 13, kulturní dům 17); 782 Horka: 1 bus (waits autobusové stanoviště 11, kulturní dům 7)

### 533
- (a) Kutná Hora, autobusové stanoviště; Týnec nad Labem, náměstí; Žiželice, náměstí; Chlumec nad Cidlinou, železniční stanice.
- (b) Chlumec → Kutná Hora exactly :40 of even hours 8:40–16:40; Kutná Hora → Chlumec :56 of even hours 8:56–14:56, then 17:16 and 18:56 (to Žiželice). Žiželice – Chlumec shuttle 13:04 / 13:40, 15:04 / 15:40 (and 5:30, 5:54); Chlumec 18:40 → Týnec.
- (c) Every 120, window 14:00–16:00 by hand. Chlumec (Královéhradecký kraj) is served only by 533, so the line runs to Chlumec. The Žiželice shuttle has two afternoon rounds and no stop of its own: listed (one bus saved).
- (d) **533** every 120:
  - Kutná Hora, autobusové stanoviště → Chlumec nad Cidlinou, železniční stanice: window 14:00–16:00 slots 14:56 / real 14:56, 1 of 1 with a real departure within 3 min; over the day 4 exact, 4 within 3 of 6 (rt 84, wait before 3)
  - Chlumec nad Cidlinou, železniční stanice → Kutná Hora, autobusové stanoviště: window 14:00–16:00 slots 14:40 / real 14:40, 1 of 1 with a real departure within 3 min; over the day 5 exact, 5 within 3 of 6 (rt 84, wait before 3)
- (e) Off the pattern: Kutná Hora 17:16 (20 min), 18:56; the Žiželice shuttle; Chlumec 18:40.
- (f) 533: 2 buses (waits autobusové stanoviště 52, železniční stanice 20)

### 786
- (a) Kutná Hora, autobusové stanoviště; Kutná Hora, Karlov, celní úřad; Petrovice I; Paběnice, ObÚ.
- (b) Kutná Hora → Paběnice exactly :15 of even hours 12:15–18:15 (5:20); Paběnice → Kutná Hora 13:19, 15:24 (4:14, 6:26). The 14:15 runs via Perštejnec (not Karlov).
- (c) Every 120, window 14:00–16:00 by hand, the way out via Perštejnec (the slot trip's own path, the only service of Perštejnec). Two buses, as the real line (Kutná Hora 14:15 leaves before the 13:19 bus is back at 14:20).
- (d) **786** every 120:
  - Kutná Hora, autobusové stanoviště → Paběnice, ObÚ: window 14:00–16:00 slots 14:15 / real 14:15, 1 of 1 with a real departure within 3 min; over the day 4 exact, 4 within 3 of 5 (rt 64, wait before 3)
  - Paběnice, ObÚ → Kutná Hora, autobusové stanoviště: window 14:00–16:00 slots 15:24 / real 15:24, 1 of 1 with a real departure within 3 min; over the day 1 exact, 1 within 3 of 3 (rt 61, wait before 3)
- (e) Off the pattern: Paběnice 13:19 (5 min).
- (f) 786: 2 buses (waits autobusové stanoviště 110, ObÚ 5)

### 788
- (a) Kutná Hora, autobusové stanoviště; Třebětín.
- (b) Kutná Hora → Třebětín 11:10, 13:15, 15:10, 17:15; Třebětín → Kutná Hora 12:12, 14:17, 16:12 (two buses, 1–2-minute turns).
- (c) Every 240 with two slots each way keeps all seven afternoon trips exact (every 120 at :15 / :12 would put 15:10 and 14:17 5 min off, same 2 buses).
- (d) **788** every 240:
  - Kutná Hora, autobusové stanoviště → Třebětín: window 15:30–17:30 slots 17:15 / real 17:15, 1 of 1 with a real departure within 3 min; over the day 4 exact, 4 within 3 of 5 (rt 61, wait before 2)
  - Třebětín → Kutná Hora, autobusové stanoviště: window 15:30–17:30 slots 16:12 / real 16:12, 1 of 1 with a real departure within 3 min; over the day 3 exact, 3 within 3 of 4 (rt 61, wait before 1)
- (e) Off the pattern: None in the afternoon.
- (f) 788: 2 buses (waits autobusové stanoviště 2/232, Třebětín 1/1)

### 481
- (a) Čáslav, autobusové stanoviště; Kutná Hora, autobusové stanoviště; Uhlířské Janovice, náměstí.
- (b) Čáslav → Uhlířské Janovice 12:14, 14:09, 16:14, 18:14; Uhlířské Janovice → Čáslav 12:39 (from the school 12:37), 14:30, 16:29, 19:30. Many paths (via Miskovice, Bylany / Onomyšl, Křečovice / Nepoměřice / Košice). Chain test: 3 of 9 arrivals at Uhlířské Janovice go on as 771, 3 as 687; at Kutná Hora 3 of 5 with 481 and 783.
- (c) Every 240 with two slots each way (6 exact against 5 for every 120 at :14 / :30, both 2 buses).
- (d) **481** every 240:
  - Čáslav, autobusové stanoviště → Uhlířské Janovice, náměstí: window 15:30–17:30 slots 16:14 / real 16:14, 1 of 1 with a real departure within 3 min; over the day 4 exact, 4 within 3 of 5 (rt 80, wait before 3)
  - Uhlířské Janovice, náměstí → Čáslav, autobusové stanoviště: window 15:30–17:30 slots 16:29 / real 16:29, 1 of 1 with a real departure within 3 min; over the day 2 exact, 3 within 3 of 6 (rt 82, wait before 3)
- (e) Off the pattern: Čáslav 18:14 (5 min); Uhlířské Janovice 12:39, 19:30; the school trip 15:28 to Onomyšl. Path audit: the 16:29 slot trip runs via Onomyšl, Křečovice, Nepoměřice and Košice, which are on 481's way out and on 746.
- (f) 481: 2 buses (waits autobusové stanoviště 18/22, náměstí 56/60)

### 710
- (a) Chrudim, autobusové stanoviště; Heřmanův Městec, nádraží; Heřmanův Městec, náměstí; Čáslav, železniční stanice.
- (b) Chrudim → Čáslav :42 hourly 11:42–17:42 without 12:42 (to Heřmanův Městec only) and 16:42; Čáslav → Chrudim :18 9:18–19:18 without 13:18 and 16:18. Via Heřmanův Městec, nádraží: 13:42, 14:42, 14:18, 19:18; via náměstí: 12:18, 15:18, 15:42, 17:18, 17:42.
- (c) One hourly line, window 14:10–16:10 (anchor 14:40), out via the station and back via the square (`stops_via`), so both Heřmanův Městec stops (outside the kraj, only 710) are on it. Two every-120 lines, one per stop, would need 4 buses against 3.
- (d) **710** every 60:
  - Chrudim, autobusové stanoviště → Čáslav, železniční stanice: window 14:10–16:10 slots 14:42, 15:42 / real 14:42, 15:42, 2 of 2 with a real departure within 3 min; over the day 6 exact, 6 within 3 of 8 (rt 60, wait before 3)
  - Čáslav, železniční stanice → Chrudim, autobusové stanoviště: window 14:10–16:10 slots 14:18, 15:18 / real 14:18, 15:18, 2 of 2 with a real departure within 3 min; over the day 7 exact, 7 within 3 of 8 (rt 59, wait before 3)
- (e) Off the pattern: The Chrudim – Heřmanův Městec shorts and the morning Podhořany trips.
- (f) 710: 3 buses (waits autobusové stanoviště 25, železniční stanice 36)

### 740
- (a) Čáslav, železniční stanice; Okřesaneč; Golčův Jeníkov, náměstí TGM.
- (b) Čáslav :13 hourly 13:13–18:13: even hours to Golčův Jeníkov, odd hours to Okřesaneč (13:13, 15:13; 20:13). Golčův Jeníkov → Čáslav 13:00, 15:00, 17:05 (10:02, 6:50); to Chotěboř only in the morning. Okřesaneč → Čáslav only in the morning (4:13–8:13: the buses sleep there). The 13:13 and 15:13 Okřesaneč buses go on at once as 781 via Žleby (Okřesaneč 13:44 → 13:45, 15:44 → 15:45, 2 of 2).
- (c) 740 every 120 at Čáslav 16:13 / Golčův Jeníkov 15:00 (1 bus, the real round). The Okřesaneč – Žleby ring has two afternoon rounds and no stop of its own (Okřesaneč and Hostovlice are on 740, the Žleby stops on 781 Potěhy): listed with 781. I first modelled it as a ring line (1 bus) and dropped it under the 3-trips rule.
- (d) **740** every 120:
  - Čáslav, železniční stanice → Golčův Jeníkov, náměstí TGM: window 14:30–16:30 slots 16:13 / real 16:13, 1 of 1 with a real departure within 3 min; over the day 3 exact, 3 within 3 of 6 (rt 42, wait before 3)
  - Golčův Jeníkov, náměstí TGM → Čáslav, železniční stanice: window 14:30–16:30 slots 15:00 / real 15:00, 1 of 1 with a real departure within 3 min; over the day 2 exact, 2 within 3 of 6 (rt 42, wait before 3)
- (e) Off the pattern: Golčův Jeníkov 17:05 (5 min); the Okřesaneč trips and their 781 returns; Čáslav 20:13.
- (f) 740: 1 bus (waits železniční stanice 31, náměstí TGM 5)

### 781
- (a) Čáslav, autobusové stanoviště; Žleby, náměstí; Žleby, Kamenné Mosty; Potěhy.
- (b) No through pattern of its own: Čáslav 12:45, 14:45, 16:45 → Žleby → Kamenné Mosty → Potěhy, where each goes on at once as 741 back to Čáslav (13:27, 15:27, 17:27; 3 of 3); Okřesaneč → Čáslav 13:45, 15:45 (the 740 buses); Kamenné Mosty → Čáslav 12:40, 19:00, Čáslav → Kamenné Mosty 11:18, 18:18; Žleby shorts 15:50, 17:08; Čáslav – Vrdy 13:18 / 13:34.
- (c) 781 Potěhy, a ring every 120 out on 781 and back on 741's Potěhy trips (`lines` 741, `notvia` Zbýšov, Chlum), exactly as the buses run; 1 bus. The rest are sparse trips over the ring's stops: listed.
- (d) **781 Potěhy** every 120:
  - Čáslav, autobusové stanoviště → Potěhy: window 14:30–16:30 slots 14:45 / real 14:45, 1 of 1 with a real departure within 3 min; over the day 3 exact, 3 within 3 of 4 (rt 41, wait before 3)
  - Potěhy → Čáslav, autobusové stanoviště: window 14:30–16:30 slots 15:27 / real 15:27, 1 of 1 with a real departure within 3 min; over the day 3 exact, 3 within 3 of 4 (rt 28, wait before 1)
- (e) Off the pattern: The Okřesaneč, Kamenné Mosty, Žleby and Vrdy trips.
- (f) 781 Potěhy: 1 bus (waits autobusové stanoviště 50, Potěhy 1)

### 741
- (a) Čáslav, autobusové stanoviště; Potěhy; Zbýšov, Chlum.
- (b) Čáslav → Zbýšov, Chlum 12:30 (from the station 12:28), 15:00, 17:15 (17:13); Chlum → Čáslav 12:10, 13:55, 16:00; one bus with a round of about 2 h 20. Potěhy → Čáslav 13:27, 15:27, 17:27 are the 781 buses (on 781 Potěhy).
- (c) Every 120 at Čáslav 15:00 / Chlum 16:00 (window 14:30–16:30): the round of the 15:00 bus (14-minute turn at Chlum). Every 144 holds the same two exactly and fits 12:30 better but not 13:55 / 17:15; the 2-hourly interval is the simpler one.
- (d) **741** every 120:
  - Čáslav, autobusové stanoviště → Zbýšov, Chlum: window 14:30–16:30 slots 15:00 / real 15:00, 1 of 1 with a real departure within 3 min; over the day 1 exact, 1 within 3 of 5 (rt 46, wait before 2)
  - Zbýšov, Chlum → Čáslav, autobusové stanoviště: window 14:30–16:30 slots 16:00 / real 16:00, 1 of 1 with a real departure within 3 min; over the day 1 exact, 1 within 3 of 4 (rt 58, wait before 3)
- (e) Off the pattern: Čáslav 12:30, 17:15 (15 min); Chlum 12:10, 13:55 (5 min); 19:13 to Bratčice.
- (f) 741: 1 bus (waits autobusové stanoviště 2, Chlum 14)

### 742
- (a) Čáslav, autobusové stanoviště; Zbýšov; Dobrovítov, Dědice; Ledeč nad Sázavou, Husovo náměstí; Ledeč nad Sázavou, Podolí.
- (b) Ledeč trips: Čáslav 6:23, 10:13, 12:13 (to Podolí), 15:13; Ledeč 6:22 (Podolí), 9:37, 12:17, 14:45 (Podolí), 17:47 (to Zbýšov). Shorts: Čáslav – Zbýšov 4:53–8:23 and 16:13 / 16:38; Čáslav 13:38 (zem.škola) → Dobrovítov, Dědice 14:15, back 14:18; Čáslav 17:13 → Třebětín (4:05 back); Čáslav – Žáky 18:13 / 18:28.
- (c) 742 every 240 at the real round of one bus, Čáslav 12:13 → Podolí 13:19, Podolí 14:45 → Čáslav 15:55 (both slot trips use Podolí, so the line ends there; the way out reads to Zbýšov, so the 16:13 repeat stands for the real Zbýšov short run on). Ledeč (Kraj Vysočina) and Kozlov are served only by 742. Every 240 with Čáslav 15:13 instead needs 2 buses. 742 Dobrovítov every 480: the only service of Dobrovítov, Dědice (a village part, not a roadside stop). The Zbýšov, Třebětín and Žáky shorts are sparse, over 742's stops: listed.
- (d) **742** every 240:
  - Čáslav, autobusové stanoviště → Ledeč nad Sázavou, Podolí: window 14:30–16:30 slots 16:13 / real 15:13, 16:13, 1 of 1 with a real departure within 3 min; over the day 2 exact, 2 within 3 of 8 (rt 66, wait before 3)
  - Ledeč nad Sázavou, Podolí → Čáslav, autobusové stanoviště: window 14:30–16:30 slots 14:45 / real 14:45, 1 of 1 with a real departure within 3 min; over the day 1 exact, 1 within 3 of 2 (rt 70, wait before 3)
- (d) **742 Dobrovítov** every 480:
  - Čáslav, autobusové stanoviště → Dobrovítov, Dědice: window 13:00–15:00 slots 13:43 / real 13:43, 1 of 1 with a real departure within 3 min; over the day 1 exact, 1 within 3 of 1 (rt 32, wait before 3)
  - Dobrovítov, Dědice → Čáslav, autobusové stanoviště: window 13:00–15:00 slots 14:18 / real 14:18, 1 of 1 with a real departure within 3 min; over the day 1 exact, 1 within 3 of 2 (rt 32, wait before 3)
- (e) Off the pattern: Čáslav 15:13, Ledeč 12:17, 17:47; the shorts.
- (f) 742: 1 bus (waits autobusové stanoviště 18, Podolí 86); 742 Dobrovítov: 1 bus (waits autobusové stanoviště 413, Dědice 3)

### 749
- (a) Čáslav, zem.škola; Souňov; Petrovice I.
- (b) Čáslav, zem.škola → Petrovice I 12:17, 14:17, 16:17 (via Souňov and Třebonín); Petrovice I → Souňov 13:19, 15:19 (17:19 on to Čáslav); Třebonín, rozcestí Chedrbí → Čáslav 13:54, 16:04 (the 743 buses). Chain test: both Souňov arrivals go on at once as 743 (13:56, 15:56), and the 743 trip from Souňov passes zem.škola at 16:17, the minute 749 leaves there.
- (c) 749, a ring every 120: zem.škola 14:17 → Petrovice I, 15:19 → Souňov, 15:56 → Čáslav, zem.škola (743's trip, `rt` 21, the 15:56's own) → 16:17. One bus, 0 slack (`lay` 0 at Souňov and zem.škola). The 0-minute turn is real at Souňov only: at zem.škola the real 743 runs on to the bus station (16:21) and another bus starts the real 16:17, so the game bus turns where reality changes buses (no stop or minute lost; B.Smetany and Hudební škola are on 743 and 381). Neither half has a way back of its own (749 ends at Souňov, 743's Souňov trips start there), so the ring is the line.
- (d) **749** every 120:
  - Čáslav, zem.škola → Petrovice I: window 14:00–16:00 slots 14:17 / real 14:17, 1 of 1 with a real departure within 3 min; over the day 3 exact, 3 within 3 of 3 (rt 56, wait before 0)
  - Petrovice I → Souňov: window 14:00–16:00 slots 15:19 / real 15:19, 1 of 1 with a real departure within 3 min; over the day 3 exact, 3 within 3 of 4 (rt 37, wait before 3)
  - Souňov → Čáslav, zem.škola: window 14:00–16:00 slots 15:56 / real 15:56, 1 of 1 with a real departure within 3 min; over the day 2 exact, 2 within 3 of 3 (rt 21, wait before 0)
- (e) Off the pattern: Čáslav 18:20 → Petrovice I (the bus going home).
- (f) 749: 1 bus (waits zem.škola 0, Petrovice I 6, Souňov 0)

### 743
- (a) Čáslav, autobusové stanoviště; Petrovice I; Třebonín, rozcestí Chedrbí.
- (b) Čáslav → Petrovice I 12:40 (from Budín 12:35), 14:55, 16:40 (via Močovice, Kluky, Souňov, Paběnice); Petrovice I → Třebonín, rozcestí Chedrbí 13:39, 15:49, each on at once as 749 to Čáslav (13:54, 16:04; 2 of 2). Souňov → Čáslav 13:56, 15:56 are the 749 buses. Čáslav, železniční stanice 11:22, 13:22 → Kluky, on as 746 to Uhlířské Janovice (2 of 2). Petrovice I is where the buses sleep (first trips 3:59–6:39).
- (c) 743, a ring every 120: Čáslav 16:40 → Petrovice I, 15:49 → Třebonín, 16:04 → Čáslav (749's trip). One bus.
- (d) **743** every 120:
  - Čáslav, autobusové stanoviště → Petrovice I: window 15:30–17:30 slots 16:40 / real 16:40, 1 of 1 with a real departure within 3 min; over the day 2 exact, 2 within 3 of 4 (rt 51, wait before 3)
  - Petrovice I → Třebonín, rozcestí Chedrbí: window 15:30–17:30 slots 15:49 / real 15:49, 1 of 1 with a real departure within 3 min; over the day 1 exact, 1 within 3 of 3 (rt 14, wait before 3)
  - Třebonín, rozcestí Chedrbí → Čáslav, autobusové stanoviště: window 15:30–17:30 slots 16:04 / real 16:04, 1 of 1 with a real departure within 3 min; over the day 1 exact, 1 within 3 of 3 (rt 13, wait before 1)
- (e) Off the pattern: Čáslav 14:55 (15 min), Petrovice I 13:39, Třebonín 13:54 (10 min); the Kluky through trips; the Budín town trips in the morning.
- (f) 743: 1 bus (waits autobusové stanoviště 23, Petrovice I 18, rozcestí Chedrbí 1)

### 746
- (a) Uhlířské Janovice, náměstí; Kluky [KH]; Čáslav, autobusové stanoviště.
- (b) Uhlířské Janovice → Čáslav 4:16, 6:18, 8:16, 11:16, 13:08, 15:16 (from the school 15:14); Čáslav → Uhlířské Janovice 6:20, 8:35, 15:35, 18:05; Kluky → Uhlířské Janovice 11:48, 13:48 (the 743 through trips). Two buses (13:08 / 15:35 and 15:14 / 18:05).
- (c) Every 240 with two slots each way, the two buses' real pairs (Uhlířské Janovice 13:08, 15:16; Čáslav 15:35, 18:05), window 14:30–16:30; changed on 2 Nov from every 120 (15:16 / 15:35, 3 exact). Out via Malešov, Polánka and Albrechtice (the 13:08's path, 77 min), back via Vidice, Roztěž, Golf (the 18:05's, 69 min), so every Vidice and Malešov stop is on it.
- (d) **746** every 240:
  - Uhlířské Janovice, náměstí → Čáslav, autobusové stanoviště: window 14:30–16:30 slots 15:16 / real 15:16, 1 of 1 with a real departure within 3 min; over the day 3 exact, 3 within 3 of 5 (rt 77, wait before 2)
  - Čáslav, autobusové stanoviště → Uhlířské Janovice, náměstí: window 14:30–16:30 slots 15:35 / real 15:35, 1 of 1 with a real departure within 3 min; over the day 2 exact, 2 within 3 of 4 (rt 69, wait before 3)
- (e) Off the pattern: The Kluky trips; the repeats 17:08 and 14:05 have no trip. Path audit: the 15:35 runs via Polánka on the leg shown via Golf (and the 15:14 via Golf on the leg shown via Polánka).
- (f) 746: 2 buses (waits náměstí 24/2, autobusové stanoviště 92/70)

### 780
- (a) Čáslav, železniční stanice; Třemošnice, autobusové stanoviště.
- (b) Exactly every 2 h: Čáslav :18 of even hours 10:18–18:18, Třemošnice :03 of odd hours 9:03–17:03; one bus with 26 min at Čáslav and 11 at Třemošnice. Morning trips to the bus station; the pair Čáslav 13:50 / Třemošnice 14:33 via Vrdy and Vinaře.
- (c) Every 120, exact (10 exact over the day). The Vrdy pair is one round over stops of 781, 782 and 784: listed (every 240 with three slots each way would take it, 2 buses).
- (d) **780** every 120:
  - Čáslav, železniční stanice → Třemošnice, autobusové stanoviště: window 13:50–15:50 slots 14:18 / real 14:18, 1 of 1 with a real departure within 3 min; over the day 5 exact, 5 within 3 of 5 (rt 34, wait before 3)
  - Třemošnice, autobusové stanoviště → Čáslav, železniční stanice: window 13:50–15:50 slots 15:03 / real 15:03, 1 of 1 with a real departure within 3 min; over the day 5 exact, 5 within 3 of 5 (rt 34, wait before 3)
- (e) Off the pattern: The Vrdy pair and the morning trips.
- (f) 780: 1 bus (waits železniční stanice 41, autobusové stanoviště 11)

### 784
- (a) Horka I, Svobodná Ves, horní; Vrdy, Dolní Bučice; Čáslav, autobusové stanoviště.
- (b) One bus all afternoon: Horka 13:25 → Dolní Bučice 13:44, 13:45 → Horka 14:10 (via Semtěš), 14:20 → Čáslav 14:47, 14:47 → Horka 15:20, 15:25 → Čáslav, železniční stanice 16:00, 16:18 → Horka 16:53, 17:20 → Dolní Bučice 17:49.
- (c) Every 180 with the two Čáslav rounds each way (Horka 14:20, 15:25; Čáslav 14:47, 16:20), 1 bus; `rt` 27 (see Set by hand) and the real 0-minute turn at Čáslav. Brambory, Starkoč and the Bílé Podolí stops have no other line. The Dolní Bučice shuttles run over the line's stops: listed.
- (d) **784** every 180:
  - Horka I, Svobodná Ves, horní → Čáslav, autobusové stanoviště: window 14:20–16:20 slots 14:20, 15:25 / real 14:20, 15:25, 2 of 2 with a real departure within 3 min; over the day 2 exact, 2 within 3 of 4 (rt 27, wait before 3)
  - Čáslav, autobusové stanoviště → Horka I, Svobodná Ves, horní: window 14:20–16:20 slots 14:47 / real 14:47, 1 of 1 with a real departure within 3 min; over the day 2 exact, 2 within 3 of 2 (rt 33, wait before 0)
- (e) Off the pattern: The Dolní Bučice shuttles 13:25, 13:45, 17:20 and the morning trips.
- (f) 784: 1 bus (waits horní 5/27, autobusové stanoviště 28/0)

### 687
- (a) Uhlířské Janovice, náměstí; Zbraslavice, náměstí; Bohdaneč; Ledeč nad Sázavou, Husovo náměstí.
- (b) Uhlířské Janovice → Ledeč exactly :38 of odd hours 11:38–17:38 (3:58, 6:23); Ledeč → Uhlířské Janovice 9:13, 12:58, 15:01 (from Podolí 14:59), 17:01, 19:13. Paths vary (Chřenovice; the 12:58 via Habrek and Obrvaň).
- (c) Every 120 at :38 / :01 (6 exact). Ledeč nad Sázavou, Husovo náměstí is the terminus; Podolí, 2 min on, is on 742. The way back is shown via Habrek and Obrvaň (the 12:58 = 13:01 slot trip), whose only afternoon service it is.
- (d) **687** every 120:
  - Uhlířské Janovice, náměstí → Ledeč nad Sázavou, Husovo náměstí: window 15:30–17:30 slots 15:38 / real 15:38, 1 of 1 with a real departure within 3 min; over the day 4 exact, 4 within 3 of 5 (rt 76, wait before 3)
  - Ledeč nad Sázavou, Husovo náměstí → Uhlířské Janovice, náměstí: window 15:30–17:30 slots 17:01 / real 17:01, 1 of 1 with a real departure within 3 min; over the day 2 exact, 3 within 3 of 6 (rt 84, wait before 3)
- (e) Off the pattern: Ledeč 19:13 (12 min); the morning Bohdaneč and 3:58 trips.
- (f) 687: 2 buses (waits náměstí 73, Husovo náměstí 7)

### 770
- (a) Uhlířské Janovice, náměstí; Sázava, autobusové stanoviště; Ostředek; Benešov, Terminál.
- (b) Uhlířské Janovice → Benešov exactly :12 (hourly in the morning, :12 of even hours 10:12–18:12); Benešov → Uhlířské Janovice :28 of even hours; Benešov → Ostředek :28 of odd hours 13:28–17:28 (19:33), Ostředek → Benešov :00 of even hours 14:00–18:00 (20:05), 0-minute turns at Ostředek (4 of 5).
- (c) 770 every 120 (2 buses) and 770 Ostředek every 120 (1 bus, 3 trips each way, regular), interleaved hourly at Benešov as in reality.
- (d) **770** every 120:
  - Uhlířské Janovice, náměstí → Benešov, Terminál: window 15:30–17:30 slots 16:12 / real 16:12, 1 of 1 with a real departure within 3 min; over the day 7 exact, 7 within 3 of 9 (rt 80, wait before 3)
  - Benešov, Terminál → Uhlířské Janovice, náměstí: window 15:30–17:30 slots 16:28 / real 16:28, 1 of 1 with a real departure within 3 min; over the day 7 exact, 7 within 3 of 8 (rt 80, wait before 3)
- (d) **770 Ostředek** every 120:
  - Benešov, Terminál → Ostředek: window 15:30–17:30 slots 17:28 / real 17:28, 1 of 1 with a real departure within 3 min; over the day 3 exact, 3 within 3 of 5 (rt 32, wait before 3)
  - Ostředek → Benešov, Terminál: window 15:30–17:30 slots 16:00 / real 16:00, 1 of 1 with a real departure within 3 min; over the day 3 exact, 3 within 3 of 6 (rt 32, wait before 0)
- (e) Off the pattern: Benešov 19:33 (5 min).
- (f) 770: 2 buses (waits náměstí 24, Terminál 56); 770 Ostředek: 1 bus (waits Terminál 56, Ostředek 0)

### 771
- (a) Uhlířské Janovice, náměstí; Soběšín; Sázava, autobusové stanoviště; Kácov, náměstí.
- (b) Afternoon: Sázava 12:30 → Kácov 13:40; Uhlířské Janovice 13:00 → Soběšín 13:37, 13:40 → Sázava 14:18, 14:30 → Soběšín 15:26 (via Ledečko), 15:50 → Uhlířské Janovice 16:26; Uhlířské Janovice 15:40, 17:40 → Soběšín (buses going home to Soběšín, where the morning trips start).
- (c) 771 a circuit every 240 at the real round of one bus (Soběšín twice; pattern need 1). 771 Kácov every 480 (Sázava 12:30; back 14:55 = the real Kácov 6:55 one period earlier): the only service of Zbizuby (three stops), Kácov, železniční stanice and Jirsíkova.
- (d) **771** every 240:
  - Uhlířské Janovice, náměstí → Soběšín: window 13:00–17:00 slots 13:00 / real 13:00, 15:40, 1 of 1 with a real departure within 3 min; over the day 1 exact, 1 within 3 of 4 (rt 37, wait before 3)
  - Soběšín → Sázava, autobusové stanoviště: window 13:00–17:00 slots 13:40 / real 13:40, 1 of 1 with a real departure within 3 min; over the day 1 exact, 1 within 3 of 1 (rt 38, wait before 3)
  - Sázava, autobusové stanoviště → Soběšín: window 13:00–17:00 slots 14:30 / real 14:30, 1 of 1 with a real departure within 3 min; over the day 1 exact, 1 within 3 of 2 (rt 56, wait before 3)
  - Soběšín → Uhlířské Janovice, náměstí: window 13:00–17:00 slots 15:50 / real 15:50, 1 of 1 with a real departure within 3 min; over the day 1 exact, 1 within 3 of 4 (rt 36, wait before 3)
- (d) **771 Kácov** every 480:
  - Sázava, autobusové stanoviště → Kácov, náměstí: window 12:00–14:00 slots 12:30 / real 12:30, 1 of 1 with a real departure within 3 min; over the day 1 exact, 1 within 3 of 1 (rt 70, wait before 3)
  - Kácov, náměstí → Sázava, autobusové stanoviště: window 12:00–14:00 slots none / real none, 0 of 0 with a real departure within 3 min; over the day 1 exact, 1 within 3 of 1 (rt 73, wait before 3)
- (e) Off the pattern: Uhlířské Janovice 15:40, 17:40 → Soběšín.
- (f) 771: 1 bus (waits náměstí (1) 34, Soběšín (2) 3, Soběšín (4) 24, autobusové stanoviště (3) 12); 771 Kácov: 1 bus (waits autobusové stanoviště 262, náměstí 75)

### 772
- (a) Uhlířské Janovice, náměstí; Vavřinec; Horní Kruty.
- (b) The Uhlířské Janovice loop 5:00, 7:05, 11:00, 12:30, 13:10 (30 min); Horní Kruty – Vavřinec exactly every 2 h (Horní Kruty 14:21, 16:21; Vavřinec 15:21, 17:21), whose bus also runs 821 at Horní Kruty (2 of 2).
- (c) 772 every 120 (the shuttle, only service of the Horní Kruty stops) and 772 okruh every 480 at 13:10 (only service of Vavřinec, Žíšov and Chmeliště and Uhlířské Janovice, Bláto and Kolínská).
- (d) **772** every 120:
  - Horní Kruty → Vavřinec: window 14:00–16:00 slots 14:21 / real 14:21, 1 of 1 with a real departure within 3 min; over the day 2 exact, 2 within 3 of 2 (rt 18, wait before 3)
  - Vavřinec → Horní Kruty: window 14:00–16:00 slots 15:21 / real 15:21, 1 of 1 with a real departure within 3 min; over the day 2 exact, 2 within 3 of 2 (rt 18, wait before 3)
- (d) **772 okruh** every 480:
  - Uhlířské Janovice, náměstí → Uhlířské Janovice, náměstí: window 12:30–14:30 slots 13:10 / real 12:30, 13:10, 1 of 1 with a real departure within 3 min; over the day 1 exact, 1 within 3 of 5 (rt 30, wait before 3)
- (e) Off the pattern: The 12:30 loop and the morning loops.
- (f) 772: 1 bus (waits Horní Kruty 42, Vavřinec 42); 772 okruh: 1 bus (waits náměstí 450)

### 773
- (a) Uhlířské Janovice, náměstí; Sázava, autobusové stanoviště.
- (b) Exactly every 2 h with one bus: Uhlířské Janovice :10 of odd hours 13:10–17:10 (7:10), Sázava :10 of even hours 12:10–16:10 (6:25).
- (c) Every 120, exact.
- (d) **773** every 120:
  - Uhlířské Janovice, náměstí → Sázava, autobusové stanoviště: window 15:30–17:30 slots 17:10 / real 17:10, 1 of 1 with a real departure within 3 min; over the day 4 exact, 4 within 3 of 4 (rt 36, wait before 3)
  - Sázava, autobusové stanoviště → Uhlířské Janovice, náměstí: window 15:30–17:30 slots 16:10 / real 16:10, 1 of 1 with a real departure within 3 min; over the day 3 exact, 3 within 3 of 4 (rt 38, wait before 3)
- (e) Off the pattern: None.
- (f) 773: 1 bus (waits náměstí 22, autobusové stanoviště 24)

### 787
- (a) Uhlířské Janovice, náměstí; Čestín; Zruč nad Sázavou, Sázavan.
- (b) One bus, a round of about 3 h: Uhlířské Janovice 9:05, 12:45, 15:30, 18:30; Zruč 11:37, 14:27, 16:37; Čestín – Zruč 14:41, 17:47.
- (c) Every 180 at 15:30 / 16:37 (the real 15:30 → 16:23, 16:37 → 17:30 round, 1 bus). Every 480 with two slots each way scores one exact hit more but is the longest interval for a 3-hourly line.
- (d) **787** every 180:
  - Uhlířské Janovice, náměstí → Zruč nad Sázavou, Sázavan: window 15:30–17:30 slots 15:30 / real 15:30, 1 of 1 with a real departure within 3 min; over the day 2 exact, 2 within 3 of 4 (rt 53, wait before 3)
  - Zruč nad Sázavou, Sázavan → Uhlířské Janovice, náměstí: window 15:30–17:30 slots 16:37 / real 16:37, 1 of 1 with a real departure within 3 min; over the day 1 exact, 1 within 3 of 5 (rt 53, wait before 3)
- (e) Off the pattern: Uhlířské Janovice 12:45 (15 min); Zruč 14:27; the Čestín shorts.
- (f) 787: 1 bus (waits náměstí 60, Sázavan 14)

### 845
- (a) Zruč nad Sázavou, Sázavan; Loket, Všebořice; Dolní Kralovice; Křelovice.
- (b) Exactly every 2 h: Zruč :51 of odd hours 5:51–15:51, Křelovice :05 of odd hours 7:05–17:05; Zruč – Dolní Kralovice and Dolní Kralovice – Křelovice shorts at irregular times (13:13, 14:20, 18:23; 13:05, 14:27).
- (c) Every 120, exact (8 exact over the day), 2 buses. The shorts run over the line's stops: listed.
- (d) **845** every 120:
  - Zruč nad Sázavou, Sázavan → Křelovice: window 14:20–16:20 slots 15:51 / real 15:51, 1 of 1 with a real departure within 3 min; over the day 4 exact, 4 within 3 of 4 (rt 64, wait before 3)
  - Křelovice → Zruč nad Sázavou, Sázavan: window 14:20–16:20 slots 15:05 / real 15:05, 1 of 1 with a real departure within 3 min; over the day 4 exact, 4 within 3 of 4 (rt 63, wait before 3)
- (e) Off the pattern: The shorts.
- (f) 845: 2 buses (waits Sázavan 103, Křelovice 10)

### 778
- (a) Zruč nad Sázavou, Sázavan; Pertoltice; Bohdaneč; Zbraslavice, náměstí.
- (b) Zruč → Zbraslavice 6:00, 14:30; Zruč → Bohdaneč 16:30; Zbraslavice → Zruč 8:30, 12:45, 15:30; Pertoltice → Zbraslavice 11:15, Pertoltice → Zruč 17:15 (the 776 bus, 2 of 2).
- (c) Every 120 at the real 14:30 → 15:20, 15:30 → 16:20 round (`core_to` Bohdaneč so the 16:30 counts as the next slot), 1 bus; the only service of the Bohdaneč and Pertoltice villages on it.
- (d) **778** every 120:
  - Zruč nad Sázavou, Sázavan → Zbraslavice, náměstí: window 14:30–16:30 slots 14:30 / real 14:30, 1 of 1 with a real departure within 3 min; over the day 2 exact, 2 within 3 of 3 (rt 50, wait before 3)
  - Zbraslavice, náměstí → Zruč nad Sázavou, Sázavan: window 14:30–16:30 slots 15:30 / real 15:30, 1 of 1 with a real departure within 3 min; over the day 1 exact, 1 within 3 of 3 (rt 50, wait before 3)
- (e) Off the pattern: Zbraslavice 12:45; Pertoltice 11:15, 17:15.
- (f) 778: 1 bus (waits Sázavan 10, náměstí 10)

### 776
- (a) Zruč nad Sázavou, Sázavan; Pertoltice; Vlastějovice.
- (b) Five trips a day: loops 6:50 (Zruč → Dolní Pohleď → Pertoltice → Vlastějovice → Horka II → Zruč), 6:55 (via Řendějov) and 14:15 (the other way round: Zruč → Horka II → Vlastějovice → Pertoltice, Machovice → Pertoltice → Dolní Pohleď → Zruč) and Zruč → Pertoltice 10:35, 16:35 (the 16:35 bus goes on as 778 at 17:15).
- (c) 776 every 480 at the 14:15 loop, 1 bus: the only service of Vlastějovice (six stops) and Pertoltice, Machovice.
- (d) **776** every 480:
  - Zruč nad Sázavou, Sázavan → Zruč nad Sázavou, Sázavan: window 14:00–16:00 slots 14:15 / real 14:15, 1 of 1 with a real departure within 3 min; over the day 1 exact, 1 within 3 of 3 (rt 52, wait before 3)
- (e) Off the pattern: The 16:35 to Pertoltice (its stops are on the loop).
- (f) 776: 1 bus (waits Sázavan 428)

## Not modelled

The rail replacement buses XS26 (992026), XS27 (992027), XS28 (992028) and XS29 (992029), automatically. Every one of the
32 regular lines is in `lines`. Variants listed on their cards instead of a Simutrans line (Step 8: two rounds or fewer in
the afternoon, every stop on a modelled line): 381 Zásmuky and Kutná Hora shorts; 402 Zruč shorts; 533 Žiželice – Chlumec
shuttle; 740 Okřesaneč with its 781 returns; 742 Zbýšov, Třebětín and Žáky shorts; 780 Vrdy pair; 781 Kamenné Mosty, Žleby
and Vrdy trips; 783 Bernardov and Horka trips; 784 Dolní Bučice shuttles; 785 Poličany trips and Kácov – Čestín shorts;
805 Kolín – Kutná Hora and Kolín – Karlov short workings (the bus-station ones on the owner checks); 845 Dolní Kralovice shorts; 776 Zruč –
Pertoltice; 743 → 746 Kluky through trips.

## Cross-line checks

- **Rings modelled** (0-minute chains in the timetable; in each, one number goes out and the other comes back, so neither has a line of its own without an empty return): 781 Potěhy (781 → 741 at
  Potěhy, 3 of 3), 749 (749 → 743 at Souňov, 2 of 2, and back out at zem.škola on the same minute), 743 (743 → 749 at
  Třebonín, rozcestí Chedrbí, 2 of 2). Named, not modelled: 740 → 781 at Okřesaneč (2 of 2), 743 → 746 at Kluky (2 of 2),
  776 → 778 at Pertoltice (2 of 2), 533 ↔ 783 and 481 ↔ 783 at Kutná Hora, autobusové stanoviště, 481 → 771 / 687 at
  Uhlířské Janovice, 805 → 782 at Na Špici, 801 ↔ 381 at hlavní nádraží, and the other sheets' lines at the ends (795 at
  Zruč, 821 at Horní Kruty, 847 at Dolní Kralovice, 750 / 754 / 796 / 553 at Benešov, 483 at Ostředek, 197 / 175 / 183 /
  203 / 227 / 240 at Praha, Háje and Roztyly). The 2 Nov live map should confirm the rings, and show the third bus of the real 749 16:17 at zem.škola, 783's trunk ↔ Žehušice chain at Čáslav (12 / 21 min) and 801's Vrchlice round (all in `notes`).
- **Bunching at the hubs** (model departures 12:00–19:00 at Kutná Hora, autobusové stanoviště and hlavní nádraží, Čáslav,
  autobusové stanoviště and železniční stanice, Uhlířské Janovice and Zruč): every same-minute pair is real except three
  repeats outside their windows, none on a shared road: Čáslav 13:43 (783 Žehušice to Chotusice, real 13:48, and 742
  Dobrovítov to Žáky), Uhlířské Janovice 18:30 (481 towards Rašovice, real 19:30, and 787 towards Čestín), Kutná Hora
  18:15 (785 passing towards Kolín and 786 towards Úmonín). The 387 / 770 clash at Uhlířské Janovice 14:12 (both via
  Staňkovice) that every 180 would have made decided 387's interval. Real pairs kept: 785 and 786 at :15, 481 and 788 at
  15:10, 710 and 780 at Čáslav :18, 772 and 773 at Uhlířské Janovice 13:10, 381 and 801 Starý Kolín at hlavní nádraží :50.
  Kolín – Kutná Hora interleaves as in reality (805 :57, 785 :25 of odd hours).
- **Coverage:** every stop of okres Kutná Hora and outside the kraj served 13:00–19:00 is on a Simutrans line here,
  except Černíny, Černíny, Zavadilka, Zruč nad Sázavou (railway station) and Hodkov zastávka, served only by XS28 / XS29
  (exceptions with the reason). The long-interval lines each hold stops nobody else serves: 742 Dobrovítov (Dobrovítov,
  Dědice), 771 Kácov (Zbizuby ×3, Kácov, železniční stanice, Jirsíkova), 772 okruh (4), 776 (7), 783 Chvaletice
  (Chvaletice ×2).
- **Stops of other Středočeský okresy that only this sheet's lines serve** (for the `--final` pass; checked against the
  other oblasts' trips): okres Benešov: Kozmice, Kozmice, Kácova Lhota, Petroupim, Petroupim, Petroupec, Petroupim,
  Sembratec, Sázava, Dojetřice, Sázava, Dojetřice, háj., Sázava, u Martina (770), Sázava, škola (773), Loket, Radíkovice,
  Loket, Všebořice, Loket, Všebořice, rozcestí (845); okres Kolín: Grunta (785), Libenice (785, 805), Horní Kruty,
  Újezdec, rozcestí (387, 773), Krakovany, Krakovany, Božec, Lipec, Radovesnice II, u mostu, Týnec nad Labem, u mostu
  (533), Malotice, Ratboř, rozcestí Těšínky, Zásmuky, Doubravčany, Zásmuky, Dupanda, Zásmuky, rozcestí Vršice (381),
  Starý Kolín, železniční zastávka (801). All are on this sheet's Simutrans lines.

## Owner checks

One (since 2 Nov): **805**, the Kolín – Kutná Hora, autobusové stanoviště short workings (5 out / 3 back 13–19 at no fixed
minute), listed as designed (0 buses, every stop on 805 / 785) against a line 805 Kutná Hora every 120 at Kolín 13:57 / bus
station 15:26 (typed 56 / 25), at the inbound rate, +1 bus. Pooling (783 circuit −1, 801 with 801 Vrchlice −1) is on the
cards, not asked. Not asked either, because the rules decide them: the outstation rate of 387 and 402, the long-interval
only-service lines, the 3-trip threshold for variants, the rings with chain evidence, 0-minute turns.

## Summary

| Line | Simutrans lines | Every | Slots (real minutes) | Buses |
|---|---|---|---|---|
| 381 | 381 | 60 | Háje :00 / Čáslav, obchodní centrum :48 | 5 |
| 387 | 387 | 120 | Háje :10 hourly / Uhlířské Janovice :57 and :12 of odd hours (15:57, 17:12) | 4 |
| 402 | 402 | 120 | Roztyly :20 even / Čáslav :36 odd | 3 |
| 481 | 481 | 240 | Čáslav 14:09, 16:14 / Uhlířské Janovice 14:30, 16:29 | 2 |
| 533 | 533 | 120 | Kutná Hora :56 even / Chlumec :40 even | 2 |
| 687 | 687 | 120 | Uhlířské Janovice :38 odd / Ledeč :01 odd | 2 |
| 710 | 710 | 60 | Chrudim :42 / Čáslav, železniční stanice :18 | 3 |
| 740 | 740 | 120 | Čáslav, železniční stanice :13 even / Golčův Jeníkov :00 odd | 1 |
| 741 | 741 | 120 | Čáslav :00 odd / Zbýšov, Chlum :00 even | 1 |
| 742 | 742; 742 Dobrovítov | 240; 480 | Čáslav 12:13 / Podolí 14:45; Čáslav 13:43 / Dědice 14:18 | 1 + 1 |
| 743 | 743 (ring with 749) | 120 | Čáslav :40 even / Petrovice I :49 odd / Třebonín :04 even | 1 |
| 746 | 746 | 240 | Uhlířské Janovice 13:08, 15:16 / Čáslav 15:35, 18:05 | 2 |
| 749 | 749 (ring with 743) | 120 | zem.škola :17 even / Petrovice I :19 odd / Souňov :56 odd | 1 |
| 770 | 770; 770 Ostředek | 120; 120 | Uhlířské Janovice :12 even / Benešov :28 even; Benešov :28 odd / Ostředek :00 even | 2 + 1 |
| 771 | 771; 771 Kácov | 240; 480 | Uhlířské Janovice 13:00, Soběšín 13:40, Sázava 14:30, Soběšín 15:50; Sázava 12:30 / Kácov 14:55 | 1 + 1 |
| 772 | 772; 772 okruh | 120; 480 | Horní Kruty :21 even / Vavřinec :21 odd; loop 13:10 | 1 + 1 |
| 773 | 773 | 120 | Uhlířské Janovice :10 odd / Sázava :10 even | 1 |
| 776 | 776 | 480 | loop 14:15 | 1 |
| 778 | 778 | 120 | Zruč :30 even / Zbraslavice :30 odd | 1 |
| 780 | 780 | 120 | Čáslav, železniční stanice :18 even / Třemošnice :03 odd | 1 |
| 781 | 781 Potěhy (ring with 741) | 120 | Čáslav :45 even / Potěhy :27 odd | 1 |
| 782 | 782; 782 Horka | 120; 120 | Kutná Hora :41 even / Vrdy :43 odd; Kutná Hora :41 odd / Vrdy :43 even | 1 + 1 |
| 783 | 783; 783 Žehušice; 783 Chvaletice | 120 each | Kutná Hora 14:16 / Čáslav 14:48; Čáslav :43 odd / Žehušice :05 even; Kutná Hora :06 odd / Chvaletice :21 even | 2 + 1 + 1 |
| 784 | 784 | 180 | Horka 14:20, 15:25 / Čáslav 14:47, 16:20 | 1 |
| 785 | 785 | 120 | Kolín :25 odd / Kácov :55 odd | 2 |
| 786 | 786 | 120 | Kutná Hora :15 even / Paběnice :24 odd | 2 |
| 787 | 787 | 180 | Uhlířské Janovice 15:30 / Zruč 16:37 | 1 |
| 788 | 788 | 240 | Kutná Hora 13:15, 15:10 / Třebětín 14:17, 16:12 | 2 |
| 801 | 801; 801 Starý Kolín; 801 Vrchlice | 120; 60; 120 | hlavní nádraží :05 :20, :35 odd / poliklinika :29 :59, :14 even; poliklinika :44 / Starý Kolín :35; hlavní nádraží :35 even / V Cihelně :11 odd | 4 + 2 + 1 |
| 802 | 802 | 60 | poliklinika :10 / Sedlec, Čechova :36 | 1 |
| 805 | 805 | 120 | Kolín :57 odd / Zruč 14:36 | 2 |
| 845 | 845 | 120 | Zruč :51 odd / Křelovice :05 odd | 2 |
| **Total** | **41 Simutrans lines** (32 real lines) | | | **67** (68 with the 805 owner check) |

## Open questions

1. The rings (749, 743, 781 Potěhy) and the named chains rest on the timetable's 0–5 minute chain test; the 2 Nov live map
   should show the same buses on both numbers.
2. 785's way out is shown via Chlístovice, Všesoky with the 13:25's 88 minutes (the 15:25's path takes 93). If the fork's
   automatic Leave up to does not absorb a 3-minute late arrival at Kácov, the line needs a third bus (engine question).
3. The 0-minute turns typed 1 min early at a loop (381 Háje, 801 poliklinika, 749, 770 Ostředek, 784 Čáslav) rely on the
   same Leave up to reading as the pilot's 573.
