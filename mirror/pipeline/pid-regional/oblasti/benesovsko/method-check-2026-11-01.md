> 3 Nov 2026: re-checked for branches read by trip ends instead of where trips pass (the 381 Zásmuky case). Where `branch-check-2026-11-03.md` or `branch-review-2026-11-03.md` differs from this file, the 3 Nov files stand (the review over the check).

# Bus schedule method, PID Benešovsko (okres Benešov), 2 Nov 2026

Designed against `DESIGN_BRIEF.md`, the bus schedule method v4 (`mirror/pipeline/bus-schedule-method.md`), `kb/lessons.md` and the Rakovnicko pilot review. Data: PID GTFS of 1 Nov 2026, service day Mon 2 Nov 2026 (`data/derived/trips.json`), the whole-day readings (`data/derived/reading/<L>.txt`), the builder output (`schedule.json`) and the three audits. Every terminus is a loop: typed = (real − 61) mod every; the real minutes below are the slots, the typed values are the builder's. Live-map plates were not yet in the readings (only early-morning sightings), so every pairing below is from the 0–5-minute chain test and is to be confirmed on the 2 Nov live map.

How each line was done: the reading over 5–23 at the core points; the window is the line's anchor −30 / +90 (`line_anchor`, or set by hand where said); candidates searched per direction and jointly (every interval ≤ 480 dividing 1440, 1–8 slots on real departures, scratch tool `s4.py`), then the method's order by hand: window slots = real ±1 and ≥ 80 % filled, most exact over the day, then within 1, then simplest; the real 13–18 headway for one-trip windows; buses from the builder. Step 4 numbers per leg are from `schedule.json` (window slots, real departures in the window, filled; exact / within 3 / trips over 5–23 counted for that leg).

## Summary

| Line | Simutrans line | Every | Slots (real minutes) | Buses |
|---|---|---|---|---|
| 426 | 426 | 60 | :00 (Praha, Roztyly) / :50 (Vlašim, Terminál) | 3 |
| 426 | 426 Benešov | 60 | :10, :25, :55 (Benešov, Terminál) / :05, :20, :35 (Vlašim, Terminál) | 5 |
| 406 | 406 | 120 | 13:30 (Praha, Roztyly) / 13:20 (Vlašim, Terminál) / 12:30 (Praha, Roztyly) / 13:23 (Pacov, autobusové nádraží) | 4 |
| 401 | 401 | 60 | :30 (Praha, Roztyly) / :35 (Pelhřimov, autobusové nádraží) | 4 |
| 408 | 408 | 60 | :30 (Praha, Roztyly) / :45 (Tábor, autobusové nádraží) | 7 |
| 332 | 332 | 15 | :12 (Praha, Budějovická) / :02 (Jílové u Prahy, náměstí) | 7 |
| 332 | 332 Neveklov | 120 | 12:30, 13:30 (Jílové u Prahy, náměstí) / 12:46, 13:51 (Neveklov) | 3 |
| 337 | 337 | 120 | 12:50, 13:50 (Benešov, Terminál) / 12:37, 13:35 (Praha, Budějovická) | 3 |
| 339 | 339 | 60 | :20 (Praha, Budějovická) / :40 (Týnec nad Sázavou, železniční stanice) | 3 |
| 382 | 382 | 60 | :50 (Praha, Háje) / :30 (Sázava, autobusové stanoviště) | 3 |
| 383 | 383 | 60 | :40 (Praha, Háje) / :11 (Chocerady) | 3 |
| 651 | 651 | 120 | 12:33 (Pyšely, náměstí) / 13:00 (Hrusice) / 13:33 (Pyšely, náměstí) / 12:07 (Senohraby, železniční stanice) | 1 |
| 651 | 651 Nespeky | 120 | 12:55 (Pyšely, náměstí) / 13:48 (Nespeky) | 1 |
| 488 | 488 | 120 | 12:05, 12:50 (Benešov, Terminál) / 12:15, 13:15 (Štěchovice) | 3 |
| 553 | 553 | 120 | 12:35 (Benešov, Terminál) / 13:30 (Jankov, Odlochovice) | 1 |
| 558 | 558 | 120 | 12:37 (Votice, autobusové stanoviště) / 13:51 (Bystřice, železniční stanice) | 1 |
| 564 | 564 | 60 | :30 (Benešov, Terminál) / :35 (Votice, autobusové stanoviště) | 2 |
| 750 | 750 | 120 | 12:35 (Benešov, Terminál) / 13:32 (Kamberk) | 1 |
| 752 | 752 | 60 | :00 (Benešov, Terminál) / :10 (Jílové u Prahy, náměstí) | 3 |
| 752 | 752 Týnec | 120 | 12:25, 13:30 (Benešov, Terminál) / 12:05, 13:25 (Týnec nad Sázavou, železniční stanice) | 2 |
| 753 | 753 | 240 | 14:30 (Benešov, Terminál) / 15:57 (Neveklov) | 1 |
| 755 | 755 | 120 | 12:20 (Benešov, Terminál) / 13:15 (Neveklov) | 1 |
| 755 | 755 Měřín | 120 | 13:05 (Benešov, Terminál) / 12:01 (Rabyně, Měřín, zotavovna) | 1 |
| 756 | 756 | 240 | 14:12 (Neveklov) / 14:58 (Křečovice, Nová Živohošť) | 1 |
| 757 | 757 | 240 | 13:20 (Benešov, Terminál) / 15:20 (Bystřice, železniční stanice) | 1 |
| 758 | 758 | 180 | 14:50 (Benešov, Terminál) / 12:32 (Postupice, škola) | 1 |
| 759 | 759 | 120 | 12:04, 13:04 (Benešov, Terminál) / 12:02, 12:57 (Neveklov) | 2 |
| 759 | 759 Strážovice | 240 | 12:47 (Neveklov) / 13:21 (Křečovice, Strážovice) | 1 |
| 791 | 791 | 120 | 13:45 (Benešov, Terminál) / 13:07 (Uhlířské Janovice, náměstí) | 2 |
| 791 | 791 Čejkovice | 120 | 12:45 (Benešov, Terminál) / 12:33 (Český Šternberk, Čejkovice) | 2 |
| 796 | 796 | 60 | :35 (Benešov, Terminál) / :56 (Pyšely, náměstí) | 3 |
| 798 | 798 | 120 | 12:18 (Benešov, Terminál) / 13:31 (Sázava, autobusové stanoviště) | 2 |
| 799 | 799 | 60 | :49 (Benešov, Terminál) / :50 (Vlašim, Terminál) | 2 |
| 789 | 789 | 120 | 12:08 (Vlašim, Terminál) / 13:25 (Divišov, náměstí) | 2 |
| 790 | 790 | 60 | :06 (Vlašim, Terminál) / :20 (Divišov, náměstí) | 2 |
| 792 | 792 | 120 | 12:45 (Vlašim, Terminál) / 13:12 (Rataje, dolní) | 1 |
| 794 | 794 | 120 | 12:45 (Vlašim, Terminál) / 13:52 (Kácov, náměstí) | 1 |
| 795 | 795 | 60 | :00 (Vlašim, Terminál) / :35 (Zruč nad Sázavou, Sázavan) | 3 |
| 840 | 840 | 120 | 12:50 (Vlašim, Terminál) / 13:00 (Vlašim, Nesperská Lhota) | 1 |
| 841 | 841 | 60 | :51 (Vlašim, Terminál) / :23 (Vlašim, Hrazená Lhota) | 1 |
| 842 | 842 | 120 | 13:15 (Vlašim, Terminál) / 13:01 (Dolní Kralovice) | 2 |
| 842 | 842 Čechtice | 120 | 13:30 (Vlašim, Terminál) / 12:22 (Čechtice) | 1 |
| 843 | 843 | 240 | 14:45 (Vlašim, Terminál) / 13:13 (Čechtice) | 1 |
| 844 | 844 | 60 | :41 (Vlašim, Terminál) / :35 (Loket, u dálnice) | 2 |
| 846 | 846 | 60 | :17 (Dolní Kralovice) / :01 (Ledeč nad Sázavou, Husovo náměstí) | 2 |
| 847 | 847 | 120 | 12:44 (Dolní Kralovice) | 1 |
| 848 | 848 | 60 | :50 (Vlašim, Terminál) / :38 (Načeradec) | 2 |
| 848 | 848 Zdiměřice | 480 | 14:15 (Vlašim, Terminál) / 14:55 (Načeradec, Zdiměřice) | 1 |
| 849 | 849 | 120 | 12:50 (Vlašim, Terminál) / 13:26 (Čechtice, Jeníkov) | 1 |
| 455 | 455 | 120 | 12:55 (Vlašim, Terminál) / 12:00 (Mladá Vožice, autobusové stanoviště) | 1 |
| 453 | 453 | 120 | 12:45, 13:15, 13:45 (Tábor, autobusové nádraží) / 12:15, 13:15, 13:45 (Mladá Vožice, autobusové stanoviště) | 2 |
| 453 | 453 Vlašim | 120 | 12:15 (Tábor, autobusové nádraží) / 13:55 (Vlašim, Terminál) | 2 |
| 452 | 452 | 60 | :30 (Mladá Vožice, autobusové stanoviště) / :45 (Olbramovice, železniční stanice) | 2 |
| 459 | 459 | 60 | :10 (Tábor, autobusové nádraží) / :50 (Olbramovice, železniční stanice) | 3 |
| 456 | 456 | 120 | 13:10 (Miličín) / 12:03 (Rodná) | 1 |
| 457 | 457 | 180 | 12:05 (Tábor, autobusové nádraží) / 12:59 (Mezno, Mitrovice) | 1 |
| 532 | 532 | 240 | 15:10 (Votice, autobusové stanoviště) / 15:57 (Jankov, Bedřichovice) | 1 |
| 550 | 550 | 60 | :21 (Vlašim, Terminál) / :53 (Votice, Beztahov) | 3 |
| 554 | 554 | 60 | :57 (Votice, autobusové stanoviště) / :14 (Votice, Kaliště) | 1 |
| 554 | 554 Smilkov | 60 | :05 (Votice, autobusové stanoviště) / :15 (Smilkov) | 1 |
| 566 | 566 | 72 | 12:28 (Votice, autobusové stanoviště) / 13:03 (Vojkov) | 1 |
| 568 | 568 | 60 | :45 (Miličín) | 1 |
| 569 | 569 | 120 | 13:15 (Miličín) / 13:55 (Sedlec-Prčice, náměstí) | 1 |
| 465 | 465 | 480 | 15:16 (Chocerady) / 15:29 (Chocerady, Samechov) | 1 |
| 483 | 483 | 60 | :01 (Ostředek) / :32 (Vranov, Vranovská Lhota) | 1 |
| 485 | 485 | 240 | 14:50 (Týnec nad Sázavou, železniční stanice) / 15:35 (Rabyně, Nová Rabyně) | 1 |
| X390 | X390 | 120 | 12:10 (Rabyně, Nová Rabyně) / 12:55 (Slapy, Motorest) | 1 |
| 865 | 865 | 120 | 12:18 (Pacov, železniční stanice) / 12:50 (Čechtice) | 2 |
| 866 | 866 | 120 | 12:10 (Košetice) / 13:23 (Čechtice) | 1 |
| 867 | 867 | 120 | 12:22 (Ježov) / 13:03 (Buřenice) | 1 |
| MHD Benešov 1 | MHD Benešov 1 | 60 | :30 (Benešov, U Náhonu) / :06 (Benešov, Albert) | 1 |
| MHD Benešov 2 | MHD Benešov 2 | 60 | :10, :50 (Benešov, MŠ Úsměv) / :00, :40 (Benešov, Terminál) | 1 |
| MHD Benešov 2 | MHD Benešov 2 Mariánovice | 60 | :30 (Benešov, MŠ Úsměv) / :06 (Benešov, Mariánovice) | 1 |
| MHD Benešov 3 | MHD Benešov 3 | 60 | :40 (Benešov, Terminál) / :01 (Benešov, Vidlákova Lhota) | 1 |
| MHD Benešov 6 | MHD Benešov 6 | 120 | 12:21 (Benešov, Terminál) / 12:33 (Benešov, Konopiště, informační centrum) | 1 |
| **Total** | **75 Simutrans lines** | | | **138** |

Not modelled: 205004, 205005, 851, 886, 887. Owner checks: 0 (the 848 question was answered by the owner on 2 Nov).

Rows that pass Step 4 within 3 min but not on the minute: 566 (every 72: 14:52 / 15:27 for 14:55 / 15:30, the method's 383 example) and 755 Měřín back (Měřín 16:05 for 16:02, the zotavovna detour). Every other timed row in the window is exact (332 Neveklov and 337 were made exact on 2 Nov).

## Changed on 2 Nov (after the independent review, review-2026-11-01.md)

- **332 Neveklov:** every 60 (Jílové :30 / Neveklov :48) → every 120, Jílové 15:30 + 16:30, Neveklov 15:51 + 16:46 (typed 50, 105); exact; 3 buses as before. The off-pattern wording for 17:30 / 18:30 is gone (they are the :30 entry's own repeats).
- **337:** every 60 (:50 / :35) → every 120, Benešov 15:50 + 16:50 (folds to every 60, Offset 49), Budějovická 15:35 + 16:37 (typed 34, 96); exact; 3 buses.
- **382:** Háje :20 → :50 (typed 49, `lay` 2: the real 2-minute turn of the :48 arrivals); 4 → 3 buses; the :20 departures listed as the buses going home.
- **758:** every 240 → every 180, typed 109 / 151 unchanged; 1 bus.
- **842 Čechtice:** Vlašim 16:20 → 15:30 (typed 29), Čechtice 16:22 unchanged; 2 → 1 bus; Vlašim 14:20, 16:20, 18:40 listed.
- **843:** every 360 (Vlašim 12:15, Čechtice 13:13) → every 240 (Vlašim 14:45, typed 104; Čechtice 17:13, typed 12); 1 bus.
- **848 Zdiměřice:** kept by the owner's decision (Haló-only places get a line from their fixed trips); its round now also runs the Novotinky loop untimed, so Načeradec, Novotinky and Načeradec, Horní Lhota, u váhy are on a line and no longer coverage exceptions; the owner check is closed.
- **Wording:** 205005's reason names 408, 553, 564 and 759 (558 does not reach Křižíkova); notes name the pooling options 752 Týnec in the Jílové buses' Benešov layover and 453 Vlašim with 453, the alternative 651 Benešov circuit, and the owner's Haló decision.
- **X390** (200390, later on 2 Nov): no longer auto-listed (Slapy dam closure 2 Mar 2026 – 31 Dec 2027, a long work): designed as X390 every 120, Rabyně 16:10 / Slapy 16:55, 1 bus. The Neveklov, Nebřich, Slapská přehrada coverage exception is removed; the six Praha-západ stops are now on a line.
- **485 Měřín** dropped as a consequence (its only own stop, Rabyně, Blaženice, is on X390; Step 8); −1 bus.
- All other lines unchanged (PASS). Totals 75 Simutrans lines, 138 buses (was 140 before the review; X390 +1, 485 Měřín −1).

## Line by line

### 426 Praha,Roztyly - Benešov - Vlašim
- **Core points:** Praha, Roztyly | Benešov, Terminál | Vlašim, Terminál | Vlašim, zbrojovka. Anchor 16:00.
- **Reading:** Praha, Roztyly – Benešov, Terminál – Postupice – Chotýšany – Vlašim, Terminál. Every 15 minutes between Benešov and Vlašim (Benešov :10 / :25 / :40 / :55, Vlašim :05 / :20 / :35 / :50), one of the four an hour running through to Prague: Roztyly :00, Vlašim :50. Two Simutrans lines, one per destination: 426 (Prague) and 426 Benešov (the three short trips an hour). The Vlašim, zbrojovka trips (Benešov 13:10, 17:10 out; zbrojovka 14:32, 18:17 back) run in the short line's slots and are run to Vlašim, Terminál in the game (zbrojovka is on 453, 792, 794, 795, 841, 842, 843, 848, 849).
- **Choice:** Read at Vlašim and Benešov: the trunk is every 15 (Vlašim :05/:20/:35/:50, Benešov :10/:25/:40/:55) and only the :50 / :40 pair is the Prague trip, so the draft's every 15 for the whole line would have run the shorts to Prague (the 292 mistake). Split by destination; the Benešov line keeps the Prague trips out with `notvia` Praha, Roztyly. Roztyly: 13 of 15 arrivals leave again within 0–5 min (0-minute turn), so the Prague leg has `lay` 0 (3 buses instead of 4).
- **426**, every 60, 3 buses (window 15:30–17:30; waits Praha, Roztyly [0]; Vlašim, Terminál [40])
  - Praha, Roztyly → Vlašim, Terminál: :00, typed 59, 70 min [lay 0]. Step 4: window slots 16:00, 17:00 / real 16:00, 17:00, filled 2/2; day 14 exact / 14 within 3 of 15.
  - Vlašim, Terminál → Praha, Roztyly: :50, typed 49, 70 min. Step 4: window slots 15:50, 16:50 / real 15:50, 16:50, filled 2/2; day 13 exact / 13 within 3 of 13.
- **426 Benešov**, every 60, 5 buses (window 15:30–17:30; waits Benešov, Terminál [5, 50, 5]; Vlašim, Terminál [10, 25, 25])
  - Benešov, Terminál → Vlašim, Terminál: :10, :25, :55, typed 9, 24, 54, 30 min [notvia Praha, Roztyly]. Step 4: window slots 15:55, 16:10, 16:25, 16:55, 17:10, 17:25 / real 15:55, 16:10, 16:25, 16:55, 17:10, 17:25, filled 6/6; day 28 exact / 28 within 3 of 32.
  - Vlašim, Terminál → Benešov, Terminál: :05, :20, :35, typed 4, 19, 34, 30 min [notvia Praha, Roztyly]. Step 4: window slots 15:35, 16:05, 16:20, 16:35, 17:05, 17:20 / real 15:35, 16:05, 16:20, 16:35, 17:05, 17:20, filled 6/6; day 29 exact / 29 within 3 of 33. Off 12–20 h: 19:50.

### 406 Praha,Roztyly - Vlašim - Pacov
- **Core points:** Praha, Roztyly | Divišov, náměstí | Vlašim, Terminál | Pacov, autobusové nádraží. Anchor 16:00.
- **Reading:** Praha, Roztyly – Ostředek – Divišov – Vlašim – Načeradec – Lukavec – Pacov. Roztyly :30 every hour, alternating: even hours to Pacov (12:30, 14:30, 16:30, 18:30), odd hours to Vlašim only (13:30, 15:30, 17:30); towards Prague Vlašim :20 every hour (odd hours start at Vlašim, even hours are the Pacov :23 trips). The buses alternate between the two ends at Roztyly with 0-minute turns (16 of 18), so 406 is one circuit with Roztyly in it twice (the Plzeň 4 rule): 4 buses, against 5 as two lines.
- **Choice:** Two lines (406 Vlašim every 120 + 406 Pacov every 120) would need 2 + 3 = 5 buses; the timetable turns every 406 bus at Roztyly on the minute into the other branch (16 of 18 arrivals), which is one circuit, 4 buses (480-minute round: Roztyly 15:30 → Vlašim 16:40, 17:20 → Roztyly 18:30, → Pacov 20:37, 21:23 → Roztyly 23:30). The Vlašim legs keep Pacov trips out with `notvia`. The 401 / 408 chains at Roztyly (11 of 18) are the shared :30 minute, not through buses (other operators).
- **406**, every 120, 4 buses (window 15:30–17:30; waits Praha, Roztyly (1) [0]; Praha, Roztyly (3) [0]; Vlašim, Terminál (2) [40]; Pacov, autobusové nádraží (4) [46])
  - Praha, Roztyly → Vlašim, Terminál: 13:30 (every 120 from 12:00), typed 29, 70 min [notvia Pacov, autobusové nádraží; lay 0]. Step 4: window slots 15:30 / real 15:30, filled 1/1; day 8 exact / 8 within 3 of 10.
  - Vlašim, Terminál → Praha, Roztyly: 13:20 (every 120 from 12:00), typed 19, 70 min [notvia Pacov, autobusové nádraží]. Step 4: window slots 17:20 / real 17:20, filled 1/1; day 7 exact / 7 within 3 of 8.
  - Praha, Roztyly → Pacov, autobusové nádraží: 12:30 (every 120 from 12:00), typed 89, 127 min [lay 0]. Step 4: window slots 16:30 / real 16:30, filled 1/1; day 6 exact / 6 within 3 of 7.
  - Pacov, autobusové nádraží → Praha, Roztyly: 13:23 (every 120 from 12:00), typed 22, 127 min. Step 4: window slots 17:23 / real 17:23, filled 1/1; day 7 exact / 7 within 3 of 8.

### 401 Pelhřimov – Červená Řečice - Čechtice – Praha,Roztyly
- **Core points:** Pelhřimov, autobusové nádraží | Košetice | Loket, u dálnice | Praha, Roztyly. Anchor 16:00.
- **Reading:** Pelhřimov – Červená Řečice – Košetice – Čechtice – Loket, u dálnice – Praha, Roztyly (Vysočina operator). Exactly hourly all day: Roztyly :30, Pelhřimov :35. The Pelhřimov 15:35 and 17:35 trips end at Loket, u dálnice; they are read there and run to Prague in the game. Pelhřimov, Červená Řečice and Čechtice, Malá Paseka have no other line.
- **Choice:** Exact hourly both ways; the two Loket, u dálnice shorts (15:35, 17:35) are read with `core_to` Loket, u dálnice so the Pelhřimov :35 row is hourly without a gap (branch audit: `path` trips, on the line's own path).
- **401**, every 60, 4 buses (window 15:30–17:30; waits Praha, Roztyly [5]; Pelhřimov, autobusové nádraží [10])
  - Praha, Roztyly → Pelhřimov, autobusové nádraží: :30, typed 29, 115 min. Step 4: window slots 15:30, 16:30 / real 15:30, 16:30, filled 2/2; day 11 exact / 11 within 3 of 11.
  - Pelhřimov, autobusové nádraží → Praha, Roztyly: :35, typed 34, 110 min [core_to Loket, u dálnice]. Step 4: window slots 15:35, 16:35 / real 15:35, 16:35, filled 2/2; day 12 exact / 12 within 3 of 12.

### 408 Tábor - Sedlec-Prčice - Votice - Benešov - Praha
- **Core points:** Tábor, autobusové nádraží | Sedlec-Prčice, náměstí | Votice, autobusové stanoviště | Benešov, Terminál | Praha, Roztyly. Anchor 13:30.
- **Reading:** Tábor – Jistebnice – Sedlec-Prčice – Votice – Bystřice – Benešov – Praha, Roztyly (two licences merged). Out of Prague hourly at :30 (12:30–16:30, 18:30); towards Prague hourly at Votice :27 (13:27–16:27), from Tábor at no fixed minute (13:05, 13:45, 15:00 take three roads north of Tábor), so the way back is timed at the Votice knot and runs the Radkov road (Radkov, Radkov, Paseka and Balkova Lhota have no other line). Listed: Roztyly → Olbramovice 17:30, → Votice 19:30; Votice 17:12; Tábor → Benešov 17:05; the Tábor – Jistebnice / Nadějkov / Chyšky shorts.
- **Choice:** Tábor departures (13:05 via Černý Les 82 min to Votice, 13:45 via Radkov 102 min, 15:00 via Hůrka 87 min) have no common minute, but all pass Votice at :27, so the way back is read at the Votice knot (the mixed-origin rule, trips start on the line's own path). The out path (12:30–16:30 are all the same road) covers Černý Les, Makov, Pazderna and Tisová; the back path is put on the Radkov road (`stops_via` Radkov, `knot_rt` 102 = the 13:45 trip's own running time) so Radkov, Radkov, Paseka and Balkova Lhota are on a line. Auto anchor 13:30 kept: there Roztyly :30 and Votice :27 both hold.
- **408**, every 60, 7 buses (window 13:00–15:00; waits Praha, Roztyly [50]; Tábor, autobusové nádraží [33])
  - Praha, Roztyly → Tábor, autobusové nádraží: :30, typed 29, 162 min. Step 4: window slots 13:30, 14:30 / real 13:30, 14:30, filled 2/2; day 8 exact / 8 within 3 of 9.
  - Tábor, autobusové nádraží → Praha, Roztyly: :45, typed 44, 175 min, read at the knot Votice, autobusové stanoviště (:27, 102 min from Tábor, autobusové nádraží) [stops_via Radkov]. Step 4: window slots 13:45, 14:45 / real 13:45, 14:45, filled 2/2; day 6 exact / 6 within 3 of 10. Off 12–20 h: 15:30, 18:15.

### 332 Praha,Budějovická - Neveklov
- **Core points:** Praha, Budějovická | Jílové u Prahy, náměstí | Neveklov. Anchor 16:00.
- **Reading:** Praha, Budějovická – Vestec – Psáry – Jílové u Prahy, náměstí every 15 minutes (Budějovická :12, Jílové :02), and the Neveklov branch Jílové – Kamenný Přívoz – Krhanice – Lešany – Netvořice – Neveklov: from Jílové hourly at :30 (15:30–18:30; 12:57 and 13:57 run through from Prague), back 13:09, 14:06, 15:01, 15:51, 16:46 (the last two through to Prague). Two Simutrans lines: the trunk (Neveklov trips kept out) and 332 Neveklov between Jílové and Neveklov; Krhanice, most and Neveklov, Dalešice have no other line.
- **Choice:** Trunk: every 15 both ways, 8 departures each way in the window; the Neveklov trips are kept out of the trunk (`notvia` Neveklov), so its 16:47 Jílové slot is empty (7 of 8 filled, passes). Neveklov branch as its own line between Jílové and Neveklov: the out trips start at Jílové (:30), the back trips run on to Prague. Changed on 2 Nov after the review: every 120 with two slots each way, Jílové 15:30 + 16:30 (an every-60 entry at :30 once folded) and Neveklov 15:51 + 16:46, all exact, the same 3 buses; the first design's hourly :48 at Neveklov was 2–3 min off both trips. Path back via Dalešice (`stops_via`, the 16:46 road) for Neveklov, Dalešice.
- **332**, every 15, 7 buses (window 15:30–17:30; waits Praha, Budějovická [14]; Jílové u Prahy, náměstí [8])
  - Praha, Budějovická → Jílové u Prahy, náměstí: :12, typed 11, 42 min [notvia Neveklov]. Step 4: window slots 15:42, 15:57, 16:12, 16:27, 16:42, 16:57, 17:12, 17:27 / real 15:42, 15:57, 16:12, 16:27, 16:42, 16:57, 17:12, 17:27, filled 8/8; day 20 exact / 37 within 3 of 46. Off 12–20 h: 19:20.
  - Jílové u Prahy, náměstí → Praha, Budějovická: :02, typed 1, 41 min [notvia Neveklov]. Step 4: window slots 15:32, 15:47, 16:02, 16:17, 16:32, 16:47, 17:02, 17:17 / real 15:32, 15:47, 16:02, 16:17, 16:32, 17:02, 17:17, filled 7/8; day 16 exact / 23 within 3 of 46. Off 12–20 h: 12:11, 12:41, 13:11, 13:41, 18:22, 18:42.
- **332 Neveklov**, every 120, 3 buses (window 15:30–17:30; waits Jílové u Prahy, náměstí [39, 44]; Neveklov [28, 33])
  - Jílové u Prahy, náměstí → Neveklov: 12:30, 13:30 (every 120 from 12:00), typed 29, 89, 48 min. Step 4: window slots 15:30, 16:30 / real 15:30, 16:30, filled 2/2; day 4 exact / 5 within 3 of 10. Off 12–20 h: 12:15, 13:42, 14:41.
  - Neveklov → Jílové u Prahy, náměstí: 12:46, 13:51 (every 120 from 12:00), typed 50, 105, 60 min [stops_via Neveklov, Dalešice]. Step 4: window slots 15:51, 16:46 / real 15:51, 16:46, filled 2/2; day 2 exact / 2 within 3 of 10. Off 12–20 h: 13:09, 14:06, 15:01.

### 337 Praha,Budějovická - Benešov
- **Core points:** Benešov, Terminál | Nespeky | Kamenice, kulturní dům | Praha, Budějovická. Anchor 16:00 (set by hand).
- **Reading:** Benešov, Terminál – Poříčí nad Sázavou – Nespeky – Kamenice – Jesenice – Praha, Budějovická. Hourly in the afternoon: Benešov :50 (14:50–17:50), Budějovická 15:35, 16:37, 17:35, 18:37: every 120 with two slots each way holds all of them on the minute. Model hour set by hand to 16:00: the busiest stretch, 13:00–15:00, is the Benešov – Nespeky short trips (all on 337's own path). Those shorts (Benešov 14:25, 15:29; Nespeky 15:02) are listed: every one runs through at Nespeky as 651 to Pyšely (4 of 4 arrivals, 6 of 6 departures), see 651.
- **Choice:** Auto anchor 14:10 put the Nespeky shorts in the window (Benešov :50 then fails: 13:40 is 10 min off). Anchor 16:00 by hand (the 282 rule). Changed on 2 Nov after the review: every 120 with two slots each way, Benešov 15:50 + 16:50 (every 60 at :50 once folded) and Budějovická 15:35 + 16:37, exact on all four, the same 3 buses (the first design's hourly :35 was 2 min off 16:37 and 18:37). The Nespeky shorts are 337's own stops and chain 100 % into 651 at Nespeky; the 651 Benešov circuit is named in the notes as an alternative (it saves no bus).
- **337**, every 120, 3 buses (window 15:30–17:30; waits Benešov, Terminál [3, 1]; Praha, Budějovická [23, 21])
  - Benešov, Terminál → Praha, Budějovická: 12:50, 13:50 (every 120 from 12:00), typed 49, 109, 84 min. Step 4: window slots 15:50, 16:50 / real 15:50, 16:50, filled 2/2; day 6 exact / 6 within 3 of 14. Off 12–20 h: 13:40, 18:35.
  - Praha, Budějovická → Benešov, Terminál: 12:37, 13:35 (every 120 from 12:00), typed 34, 96, 72 min. Step 4: window slots 15:35, 16:37 / real 15:35, 16:37, filled 2/2; day 4 exact / 6 within 3 of 15. Off 12–20 h: 12:45, 13:50, 14:47, 19:30.

### 339 Praha,Budějovická - Týnec nad Sázavou
- **Core points:** Praha, Budějovická | Sulice, Želivec | Kamenice, kulturní dům | Týnec nad Sázavou, železniční stanice. Anchor 16:00.
- **Reading:** Praha, Budějovická – Jesenice – Sulice – Kamenice – Řehenice – Týnec nad Sázavou, železniční stanice. Týnec → Prague hourly at :40 (14:40–18:40); Prague → Týnec hourly at :20, every 30 (:20 / :50) 15:20–17:20. The first trips start at Týnec (3:53–6:44) and the last ones end there (20:10, 21:38, 0:19), so the line is timed both ways at its inbound rate (the outstation rule): the 15:50 and 16:50 from Prague are off the pattern; the Kamenice :41 shorts are their probable returns (live map to confirm). Listed: the Kamenice shorts (Prague 13:05, 14:35; Kamenice 14:41, 15:41, 16:41) and the Sulice, Želivec shorts (13:55, 16:16; 7 of 7 follow a 335 arrival there), all on 339's path.
- **Choice:** Window 15:30–17:30: Prague → Týnec 4 (15:50, 16:20, 16:50, 17:20), Týnec → Prague 2 (15:40, 16:40) plus the Kamenice shorts 15:41, 16:41. Every 30 out with the way back read at Kamenice (:01 from Týnec, :41 shorts, a knot on the line's path) fails: the 17:20 slot has no trip (3 of 4). The buses sleep at Týnec (3:53, 5:09, 5:39, 6:09 start there), so the outstation rule: hourly both ways at the inbound rate; FEWER in the audit (2 slots for 4 departures out of Prague) by design.
- **339**, every 60, 3 buses (window 15:30–17:30; waits Praha, Budějovická [31]; Týnec nad Sázavou, železniční stanice [23])
  - Praha, Budějovická → Týnec nad Sázavou, železniční stanice: :20, typed 19, 57 min. Step 4: window slots 16:20, 17:20 / real 15:50, 16:20, 16:50, 17:20, filled 2/2; day 5 exact / 5 within 3 of 15. Off 12–20 h: 15:50, 16:50, 18:05, 19:10.
  - Týnec nad Sázavou, železniční stanice → Praha, Budějovická: :40, typed 39, 69 min. Step 4: window slots 15:40, 16:40 / real 15:40, 16:40, filled 2/2; day 5 exact / 6 within 3 of 15. Off 12–20 h: 12:55.

### 382 Praha,Háje - Sázava
- **Core points:** Praha, Háje | Stříbrná Skalice, náměstí | Sázava, autobusové stanoviště. Anchor 16:00.
- **Reading:** Praha, Háje – Uhříněves – Říčany – Mukařov – Jevany – Stříbrná Skalice – Sázava, autobusové stanoviště. Sázava → Prague hourly at :30 (12:30–17:30); Prague → Sázava every 30 at :20 / :50 (14:20–17:20). The buses sleep at Sázava (4:25–7:23 the trips start there), so 382 is timed both ways at the inbound rate. Of the two Háje departures an hour it keeps the :50, which the :48 arrivals from Sázava turn into in 2 minutes (3 buses; the :20 would need 4); the :20 departures (14:20–18:20) are off the pattern, the buses going home. The Stříbrná Skalice morning shorts are listed.
- **Choice:** Outstation: 4 departures from Háje against 2 from Sázava in the window, the morning trips start at Sázava. Inbound rate hourly. Changed on 2 Nov after the review: the kept Háje departure is :50, not :20 — the :48 arrivals from Sázava leave again at :50 (a real 2-minute turn, `lay` 2), which needs 3 buses against 4 for :20 (the v4 rule: choose the kept departures by the waits, as 290). The :20 departures are the buses going home, listed. FEWER by design.
- **382**, every 60, 3 buses (window 15:30–17:30; waits Praha, Háje [2]; Sázava, autobusové stanoviště [22])
  - Praha, Háje → Sázava, autobusové stanoviště: :50, typed 49, 78 min [lay 2]. Step 4: window slots 15:50, 16:50 / real 15:50, 16:20, 16:50, 17:20, filled 2/2; day 3 exact / 3 within 3 of 17. Off 12–20 h: 12:30, 13:15, 14:20, 15:20, 16:20, 17:20, 18:20, 19:15.
  - Sázava, autobusové stanoviště → Praha, Háje: :30, typed 29, 78 min. Step 4: window slots 15:30, 16:30 / real 15:30, 16:30, filled 2/2; day 7 exact / 7 within 3 of 15. Off 12–20 h: 18:15.

### 383 Praha,Háje - Chocerady
- **Core points:** Praha, Háje | Mukařov [PH] | Ondřejov, náměstí | Chocerady. Anchor 15:00 (set by hand).
- **Reading:** Praha, Háje – Kolovraty – Říčany – Mukařov – Tehovec – Struhařov – Ondřejov – Chocerady. Hourly: Háje :40 and Chocerady :11 from 14:40 to 16:40 (the line's model hour set by hand to 15:00, where this pattern runs), :45 and :06 before 14:00 and from 17:00. Off the pattern 12–20 h: Háje 12:45, 13:45, 17:45, 18:45, 19:45; Chocerady 13:06, 17:06, 18:06, 19:21 (5 to 10 min off). The Ondřejov – Mukařov shorts (12:53, 13:36, 13:38) are listed.
- **Choice:** At 16:00 the Háje row passes at :40 but Chocerady needs :09 (0 exact: 16:11 and 17:06). Anchor 15:00 by hand, window 14:30–16:30, where both :40 and :11 hold (3 exact each).
- **383**, every 60, 3 buses (window 14:30–16:30; waits Praha, Háje [18]; Chocerady [21])
  - Praha, Háje → Chocerady: :40, typed 39, 70 min. Step 4: window slots 14:40, 15:40 / real 14:40, 15:40, filled 2/2; day 3 exact / 3 within 3 of 14. Off 12–20 h: 12:45, 13:45, 17:45, 18:45, 19:45.
  - Chocerady → Praha, Háje: :11, typed 10, 71 min. Step 4: window slots 15:11, 16:11 / real 15:11, 16:11, filled 2/2; day 3 exact / 3 within 3 of 13. Off 12–20 h: 13:06, 17:06, 18:06, 19:21.

### 651 Nespeky - Pyšely - Senohraby - Hrusice
- **Core points:** Pyšely, náměstí | Nespeky | Senohraby, železniční stanice | Hrusice. Anchor 15:10.
- **Reading:** Nespeky – Pyšely – Senohraby – Hrusice (ARRIVA). One bus in a fixed sequence in the afternoon, plus the Benešov 337 bus that runs on at Nespeky to Pyšely and back (337 14:25 → Nespeky 14:44 → 651 to Pyšely 14:51 → 14:55 → Nespeky 15:02 → 337 to Benešov). Two Simutrans lines: 651 is the 14:33–16:33 round of the Pyšely bus (Hrusice and Senohraby, exact), 651 Nespeky the Pyšely – Nespeky trips (Pyšely, hotel Doly has no other line). The Senohraby stops (okres Praha-východ) have no other line.
- **Choice:** Afternoon trips of the Pyšely bus: 14:33 → Hrusice, 15:00 → Pyšely, 15:33 → Senohraby, 16:07 → Pyšely, 16:19 loop, 16:34 → Hrusice (the next round); a 120-minute circuit, exact. The Pyšely – Nespeky trips (14:44, 14:55, 15:48) are the 337 bus running on at Nespeky (0-minute chains 4 of 4 / 6 of 6); hotel Doly needs them, so 651 Nespeky every 120 holds the real 14:55 / 15:48 pair (1 bus). The Zaječice – Pětihosty – Nová Ves loop stops are on the circuit's two Senohraby legs.
- **651**, every 120, 1 bus (window 14:40–16:40; waits Pyšely, náměstí (1) [15]; Pyšely, náměstí (3) [13]; Hrusice (2) [7]; Senohraby, železniční stanice (4) [22])
  - Pyšely, náměstí → Hrusice: 12:33 (every 120 from 12:00), typed 92, 20 min. Step 4: window slots 16:33 / real 16:34, filled 1/1; day 1 exact / 2 within 3 of 3.
  - Hrusice → Pyšely, náměstí: 13:00 (every 120 from 12:00), typed 119, 20 min. Step 4: window slots 15:00 / real 15:00, filled 1/1; day 2 exact / 2 within 3 of 3.
  - Pyšely, náměstí → Senohraby, železniční stanice: 13:33 (every 120 from 12:00), typed 32, 12 min. Step 4: window slots 15:33 / real 15:33, 16:34, filled 1/1; day 3 exact / 4 within 3 of 16. Off 12–20 h: 13:07, 14:33, 16:34, 18:58.
  - Senohraby, železniční stanice → Pyšely, náměstí: 12:07 (every 120 from 12:00), typed 66, 11 min. Step 4: window slots 16:07 / real 15:10, 16:07, filled 1/1; day 1 exact / 4 within 3 of 16. Off 12–20 h: 13:40, 15:10, 17:07, 18:15, 19:15.
- **651 Nespeky**, every 120, 1 bus (window 14:40–16:40; waits Pyšely, náměstí [59]; Nespeky [46])
  - Pyšely, náměstí → Nespeky: 12:55 (every 120 from 12:00), typed 114, 7 min. Step 4: window slots 14:55 / real 14:55, filled 1/1; day 1 exact / 1 within 3 of 13. Off 12–20 h: 12:31, 13:52, 17:18, 18:26.
  - Nespeky → Pyšely, náměstí: 13:48 (every 120 from 12:00), typed 47, 8 min. Step 4: window slots 15:48 / real 14:44, 15:48, filled 1/1; day 1 exact / 1 within 3 of 12. Off 12–20 h: 12:59, 14:10, 14:44, 17:27, 18:50.

### 488 Benešov - Netvořice - Štěchovice
- **Core points:** Benešov, Terminál | Netvořice, pošta | Štěchovice. Anchor 16:00.
- **Reading:** Benešov, Terminál – Václavice – Chrášťany – Netvořice – Krňany – Štěchovice. Afternoon out of Benešov 13:10, 14:50, 16:05, 16:50, 17:50; from Štěchovice 12:25, 14:15, 16:15, 17:15. In the model hour (16:00) two departures each way: every 120 with two slots each, exact (Benešov 14:50, 16:05, 16:50; Štěchovice 14:15, 16:15, 17:15). Off: Benešov 13:10, 17:50; Štěchovice 12:25. The Netvořice shorts (13:43, 13:50, 15:53, 19:10) and the evening Štěchovice – Netvořice trips run on 488's path and are listed.
- **Choice:** Window: Benešov 16:05, 16:50; Štěchovice 16:15, 17:15. Every 60 fails both ways (Benešov :50 leaves 15:50 without a trip; :05 leaves 17:05). Every 120 with two slots each way: all four exact, 3 exact over the day per direction; 3 buses. One slot each way also passes (±1) with 2 exact and 2 buses; the method takes the exact pair (more exact hits).
- **488**, every 120, 3 buses (window 15:30–17:30; waits Benešov, Terminál [37, 52]; Štěchovice [11, 26])
  - Benešov, Terminál → Štěchovice: 12:05, 12:50 (every 120 from 12:00), typed 64, 109, 59 min. Step 4: window slots 16:05, 16:50 / real 16:05, 16:50, filled 2/2; day 3 exact / 3 within 3 of 6. Off 12–20 h: 13:10, 17:50.
  - Štěchovice → Benešov, Terminál: 12:15, 13:15 (every 120 from 12:00), typed 14, 74, 58 min. Step 4: window slots 16:15, 17:15 / real 16:15, 17:15, filled 2/2; day 3 exact / 3 within 3 of 6. Off 12–20 h: 12:25.

### 553 Benešov - Jankov,Odlochovice
- **Core points:** Benešov, Terminál | Popovice | Jankov, Odlochovice. Anchor 16:00.
- **Reading:** Benešov, Terminál – Bystřice – Popovice – Jankov – Jankov, Odlochovice. Every 2 hours: Benešov :35 even hours (8:35–16:35), Odlochovice :30 odd hours (13:30, 15:30); the bus turns at Odlochovice in 2 minutes. Off: Benešov 19:15; Odlochovice 18:00.
- **Choice:** Every 120 exact at both ends; the real 2-minute turn at Odlochovice (13:28 → 13:30, 15:28 → 15:30) sets `lay` 2: 1 bus.
- **553**, every 120, 1 bus (window 15:30–17:30; waits Benešov, Terminál [16]; Jankov, Odlochovice [4])
  - Benešov, Terminál → Jankov, Odlochovice: 12:35 (every 120 from 12:00), typed 94, 51 min. Step 4: window slots 16:35 / real 16:35, filled 1/1; day 5 exact / 5 within 3 of 7. Off 12–20 h: 19:15.
  - Jankov, Odlochovice → Benešov, Terminál: 13:30 (every 120 from 12:00), typed 29, 49 min [lay 2]. Step 4: window slots 15:30 / real 15:30, filled 1/1; day 2 exact / 2 within 3 of 7. Off 12–20 h: 18:00.

### 558 Votice - Olbramovice - Benešov
- **Core points:** Votice, autobusové stanoviště | Bystřice, náměstí | Bystřice, železniční stanice | Benešov, Terminál. Anchor 16:00.
- **Reading:** Votice – Olbramovice – Ouběnice – Bystřice (– Benešov). Votice :37 every 2 hours (12:37 to Benešov, 14:37 to Bystřice, 16:37 to Ouběnice, rozcestí Jiřín); back from Bystřice, železniční stanice :51 (13:51 from Benešov, 15:51). Modelled Votice – Bystřice: the Benešov end is on 408. The 16:37 ends at Ouběnice, rozcestí Jiřín and runs to Bystřice in the game.
- **Choice:** Read Votice → Bystřice, železniční stanice with `core_to` Ouběnice, rozcestí Jiřín (the 16:37 ends there); back at Bystřice :51 (13:51 is the Benešov trip passing). The Benešov part is on 408.
- **558**, every 120, 1 bus (window 15:30–17:30; waits Votice, autobusové stanoviště [15]; Bystřice, železniční stanice [41])
  - Votice, autobusové stanoviště → Bystřice, železniční stanice: 12:37 (every 120 from 12:00), typed 96, 33 min [core_to Bystřice, Ouběnice, rozcestí Jiřín]. Step 4: window slots 16:37 / real 16:37, filled 1/1; day 5 exact / 5 within 3 of 7.
  - Bystřice, železniční stanice → Votice, autobusové stanoviště: 13:51 (every 120 from 12:00), typed 50, 31 min. Step 4: window slots 15:51 / real 15:51, filled 1/1; day 4 exact / 4 within 3 of 5.

### 564 Benešov - Vrchotovy Janovice - Votice
- **Core points:** Benešov, Terminál | Votice, autobusové stanoviště. Anchor 14:00.
- **Reading:** Benešov, Terminál – Bystřice – Drachkov – Vrchotovy Janovice – Olbramovice – Votice. Benešov :30 and Votice :35 all day, every 2 hours at midday (9:30, 11:30; 10:35, 12:35), hourly 13:30–14:35, then every 2 hours (16:30, 18:30). Modelled hourly at the line's anchor (14:00), which also puts the most trips on the minute over the day; the 15:30 and 17:30 slots have no trip in reality.
- **Choice:** Auto anchor 14:00 (window 13:30–15:30): hourly passes both ways, every 120 passes too; hourly puts 9 + 7 departures on the minute over the day against 5 + 6.
- **564**, every 60, 2 buses (window 13:30–15:30; waits Benešov, Terminál [3]; Votice, autobusové stanoviště [13])
  - Benešov, Terminál → Votice, autobusové stanoviště: :30, typed 29, 52 min. Step 4: window slots 13:30, 14:30 / real 13:30, 14:30, filled 2/2; day 8 exact / 8 within 3 of 9.
  - Votice, autobusové stanoviště → Benešov, Terminál: :35, typed 34, 52 min. Step 4: window slots 13:35, 14:35 / real 13:35, 14:35, filled 2/2; day 7 exact / 7 within 3 of 9.

### 750 Benešov - Louňovice pod Blaníkem - Kamberk
- **Core points:** Benešov, Terminál | Louňovice pod Blaníkem | Kamberk. Anchor 16:00.
- **Reading:** Benešov, Terminál – Postupice – Veliš – Louňovice pod Blaníkem – Kamberk. Benešov :35 (8:35–12:35, 15:35, 16:35, 18:35), to Louňovice or on to Kamberk; back at Louňovice :40 (9:40, 11:40, 13:40 from Kamberk, 15:40). Every 120, the even-hour :35 out of Benešov and the odd-hour :40 at Louňovice, with every trip run to Kamberk in the game (Kamberk, Předbořice and Louňovice, škola have no other line). Off: Benešov 14:05, 15:35; Louňovice 12:40, 17:55; Kamberk 16:27 → Louňovice.
- **Choice:** Every 60 fails at Louňovice (16:40 has no trip). Every 120: Benešov even-hour :35 (6 exact, read at Louňovice with `core_to`) and back read at Louňovice :40 odd hours (4 exact; Kamberk 13:32 passes Louňovice 13:40, 15:40 starts there). 1 bus. Kamberk gets every 120 in the game (really three trips in, two out).
- **750**, every 120, 1 bus (window 15:30–17:30; waits Benešov, Terminál [15]; Kamberk [9])
  - Benešov, Terminál → Kamberk: 12:35 (every 120 from 12:00), typed 94, 48 min [core_to Louňovice pod Blaníkem]. Step 4: window slots 16:35 / real 15:35, 16:35, filled 1/1; day 6 exact / 6 within 3 of 9. Off 12–20 h: 14:05, 15:35.
  - Kamberk → Benešov, Terminál: 13:32 (every 120 from 12:00), typed 31, 48 min, read at the knot Louňovice pod Blaníkem (13:40, 8 min from Kamberk). Step 4: window slots 15:32 / real 15:32, filled 1/1; day 5 exact / 5 within 3 of 8. Off 12–20 h: 12:32, 17:47.

### 752 Benešov - Týnec nad Sázavou - Jílové u Prahy
- **Core points:** Benešov, Terminál | Týnec nad Sázavou, železniční stanice | Krhanice | Jílové u Prahy, náměstí. Anchor 14:40.
- **Reading:** Benešov, Terminál – Týnec nad Sázavou – Krhanice – Kamenný Přívoz – Jílové u Prahy, náměstí, with Benešov – Týnec shorts. To Jílové hourly: Benešov :00 (14:00–17:00), Jílové :10 (14:10–16:10). Shorts: Benešov 13:35, 14:25, 15:30, 17:35; Týnec 14:13, 15:25, 16:05, 18:05. Two lines: 752 (Jílové) and 752 Týnec, each with its own road (752 via Úročnice and Krusičany, the shorts via Bukovany and Chlístov, Racek, osada, stops only 752 serves). Off: Benešov 13:05, 18:05; Jílové 12:50, 17:05, 18:04.
- **Choice:** Two destinations: Jílové hourly (Benešov :00 / Jílové :10, exact) and the Týnec shorts. Shorts first tried every 120 with one slot each way: FEWER at Týnec (3 departures 14:13, 15:25, 16:05 in the line's window 14:10–16:10). Every 120 with two slots each way (Benešov 14:25, 15:30; Týnec 15:25, 16:05) passes, 2 buses. Each Simutrans line has its own road (shorts `stops_via` Chlístov, Racek, osada out and Bukovany back), so all of 752's own stops are on a line.
- **752**, every 60, 3 buses (window 14:10–16:10; waits Benešov, Terminál [55]; Jílové u Prahy, náměstí [18])
  - Benešov, Terminál → Jílové u Prahy, náměstí: :00, typed 59, 52 min. Step 4: window slots 15:00, 16:00 / real 15:00, 16:00, filled 2/2; day 4 exact / 4 within 3 of 11. Off 12–20 h: 13:05, 18:05.
  - Jílové u Prahy, náměstí → Benešov, Terminál: :10, typed 9, 55 min. Step 4: window slots 14:10, 15:10 / real 14:10, 15:10, filled 2/2; day 3 exact / 3 within 3 of 10. Off 12–20 h: 12:50, 17:05, 18:04.
- **752 Týnec**, every 120, 2 buses (window 14:10–16:10; waits Benešov, Terminál [65, 40]; Týnec nad Sázavou, železniční stanice [37, 12])
  - Benešov, Terminál → Týnec nad Sázavou, železniční stanice: 12:25, 13:30 (every 120 from 12:00), typed 29, 84, 23 min [stops_via Chlístov, Racek, osada; notvia Jílové u Prahy, náměstí, Krhanice]. Step 4: window slots 14:25, 15:30 / real 14:25, 15:30, filled 2/2; day 2 exact / 2 within 3 of 10. Off 12–20 h: 13:35, 17:35, 19:05, 19:35.
  - Týnec nad Sázavou, železniční stanice → Benešov, Terminál: 12:05, 13:25 (every 120 from 12:00), typed 24, 64, 20 min [stops_via Bukovany [BN]; notvia Jílové u Prahy, náměstí, Krhanice]. Step 4: window slots 15:25, 16:05 / real 14:13, 15:25, 16:05, filled 2/2; day 3 exact / 3 within 3 of 11. Off 12–20 h: 14:13, 19:05.

### 753 Benešov - Týnec nad Sázavou -  Netvořice - Neveklov
- **Core points:** Benešov, Terminál | Týnec nad Sázavou, železniční stanice | Netvořice | Neveklov. Anchor 15:00.
- **Reading:** Benešov – Týnec nad Sázavou – Lešany – Kamenný Přívoz – Netvořice – Neveklov, a school line of single trips. The one afternoon round Benešov – Neveklov is 14:30 → 15:51 and Neveklov 15:57 → Benešov 17:20: every 240, one bus. It is the only service of Brodce, Zbořený Kostelec, Pecerady, Lešany, Brejlov, Kamenný Přívoz, Hostěradice and Neveklov, Ouštice. Listed: Benešov → Týnec 13:35, → Netvořice 16:35, 18:35; Týnec → Neveklov 13:30, → Benešov 14:30, 15:35; Neveklov → Týnec 14:37; Netvořice → Týnec 17:44.
- **Choice:** Only one Benešov – Neveklov round in the afternoon (14:30 / 15:57). Every 120 would add a bus with no more exact hits (the 16:35 and 18:35 go to Netvořice only); every 240 holds the round with 1 bus. Its two legs' paths cover all of 753's own stops.
- **753**, every 240, 1 bus (window 14:30–16:30; waits Benešov, Terminál [70]; Neveklov [6])
  - Benešov, Terminál → Neveklov: 14:30 (every 240 from 12:00), typed 89, 81 min. Step 4: window slots 14:30 / real 14:30, filled 1/1; day 1 exact / 1 within 3 of 1.
  - Neveklov → Benešov, Terminál: 15:57 (every 240 from 12:00), typed 176, 83 min. Step 4: window slots 15:57 / real 15:57, filled 1/1; day 1 exact / 1 within 3 of 3.

### 755 Benešov - Neveklov - Rabyně,Měřín
- **Core points:** Benešov, Terminál | Neveklov | Neveklov, Jablonná | Rabyně, Měřín | Rabyně, Měřín, zotavovna. Anchor 15:10.
- **Reading:** Benešov, Terminál – Václavice, Vatěkov – Neveklov – Stranný – Blažim – Jablonná – Rabyně, Měřín. Benešov – Neveklov trips 13:50, 15:20, 16:20, 18:05, 18:50 out, 12:45, 15:15, 18:30 back; through to Měřín 15:05 and 17:00 (to the zotavovna) out, Měřín 13:45 and 16:02 back. The buses sleep at Neveklov and Jablonná, so the afternoon sends more out of Benešov than come back (outstation): two lines at the inbound rate, 755 (Neveklov) and 755 Měřín, together Benešov 15:05 / 16:20 and Neveklov 15:15 / 16:33 every 2 hours. Off: Benešov 13:50, 15:20, 15:50 (to Jablonná), 18:05, 18:50; Neveklov 12:45, 18:30.
- **Choice:** Outstation: in the line's window (14:40–16:40) Benešov sends 15:05 (Měřín), 15:20, 15:50 (Jablonná), 16:20 and Neveklov sends 15:15 (and Měřín 16:02); the morning trips start at Neveklov and Jablonná. Two lines at the inbound rate, every 120 each (755: Benešov 16:20 / Neveklov 15:15, 1 bus; 755 Měřín: Benešov 15:05 / Měřín 16:02, read at Rabyně, Měřín with `core_to` and `knot`, 1 bus). The zotavovna, 3–4 min beyond Měřín on a dead end, is the line's only stop no other line serves; the real 15:05 bus turns at Měřín (15:57 → 16:02), the game bus also runs to the zotavovna, so its back slot is set at Měřín 16:05 (`knot_rt` 4 = the real zotavovna 14:48 → Měřín 14:52, `lay` 1), 3 min after the real 16:02: within Step 4's 3 minutes, on the card. FEWER on 755 out of Benešov by design.
- **755**, every 120, 1 bus (window 14:40–16:40; waits Benešov, Terminál [41]; Neveklov [35])
  - Benešov, Terminál → Neveklov: 12:20 (every 120 from 12:00), typed 79, 20 min [notvia Rabyně, Měřín]. Step 4: window slots 16:20 / real 15:20, 15:50, 16:20, filled 1/1; day 1 exact / 1 within 3 of 11. Off 12–20 h: 13:50, 15:20, 15:50, 18:05, 18:50.
  - Neveklov → Benešov, Terminál: 13:15 (every 120 from 12:00), typed 14, 24 min [notvia Rabyně, Měřín]. Step 4: window slots 15:15 / real 15:15, filled 1/1; day 1 exact / 2 within 3 of 9. Off 12–20 h: 12:45, 18:30.
- **755 Měřín**, every 120, 1 bus (window 14:40–16:40; waits Benešov, Terminál [8]; Rabyně, Měřín, zotavovna [1])
  - Benešov, Terminál → Rabyně, Měřín, zotavovna: 13:05 (every 120 from 12:00), typed 4, 55 min [core_to Rabyně, Měřín]. Step 4: window slots 15:05 / real 15:05, filled 1/1; day 1 exact / 1 within 3 of 2. Off 12–20 h: 17:00.
  - Rabyně, Měřín, zotavovna → Benešov, Terminál: 12:01 (every 120 from 12:00), typed 60, 56 min, read at the knot Rabyně, Měřín (12:05, 4 min from Rabyně, Měřín, zotavovna) [lay 1]. Step 4: window slots 16:01 / real 15:58, filled 1/1; day 0 exact / 1 within 3 of 2. Off 12–20 h: 13:41.

### 756 Neveklov - Křečovice
- **Core points:** Neveklov | Křečovice | Křečovice, Nahoruby | Křečovice, Nová Živohošť. Anchor 16:00.
- **Reading:** Neveklov – Maršovice, Vráce – Křečovice – Nahoruby – Nová Živohošť, a school line of single trips. Its one afternoon round is Neveklov 14:12 → Nová Živohošť 14:47 (via Křečovice and Nahoruby) and Nová Živohošť 14:58 → Neveklov 15:15 (via Lhotka, u Švarců and Stranný): every 240, one bus, the only service of Křečovice, Nahoruby (3 stops), Dráha, Lhotka, u Švarců, Nová Živohošť, Vráce and Řehovice, rozcestí. Listed: 15:35 Neveklov → Strážovice and the Křečovice – Nahoruby / Nová Živohošť shuttles.
- **Choice:** One round in the afternoon; every 240, 1 bus. No slot in the 16:00 window (the round is 14:12 / 14:58, named in the why).
- **756**, every 240, 1 bus (window 15:30–17:30; waits Neveklov [177]; Křečovice, Nová Živohošť [30])
  - Neveklov → Křečovice, Nová Živohošť: 14:12 (every 240 from 12:00), typed 71, 16 min. Step 4: no slot in the window (real there: none); day 1 exact / 1 within 3 of 3.
  - Křečovice, Nová Živohošť → Neveklov: 14:58 (every 240 from 12:00), typed 117, 17 min. Step 4: no slot in the window (real there: none); day 1 exact / 1 within 3 of 3.

### 757 Benešov - Bystřice
- **Core points:** Benešov, Terminál | Bystřice, železniční stanice. Anchor 13:40 (set by hand).
- **Reading:** Benešov – Konopiště – Bystřice, a sparse line: Benešov 9:20, 11:00, 13:20 and 16:20 (to Tvoršovice) out, Bystřice 10:12, 12:35, 15:20 back, and one Votice – Maršovice – Benešov trip each way (6:50, 16:10). Every 240 at the real 13:20 out / 15:20 back, one bus. Model hour set by hand to 13:40: the line's only afternoon round starts at 13:20, and the 16:00 window holds only the 16:20 short to Tvoršovice, which is off the pattern. It is the only service of Benešov, Ke Stadionu, Benica, Konopiště (Šiberna, sv. Anna, sádky) and Bystřice, Jarkovice.
- **Choice:** Every 240 on the real round 13:20 / 15:20. With the auto anchor (16:00) its 17:20 repeat fell in the window with only the 16:20 Tvoršovice short there (EMPTY); anchor set by hand to 13:40 (window 13:10–15:10, the line's own round).
- **757**, every 240, 1 bus (window 13:10–15:10; waits Benešov, Terminál [94]; Bystřice, železniční stanice [92])
  - Benešov, Terminál → Bystřice, železniční stanice: 13:20 (every 240 from 12:00), typed 19, 28 min. Step 4: window slots 13:20 / real 13:20, filled 1/1; day 2 exact / 2 within 3 of 3.
  - Bystřice, železniční stanice → Benešov, Terminál: 15:20 (every 240 from 12:00), typed 139, 26 min. Step 4: no slot in the window (real there: none); day 1 exact / 1 within 3 of 3. Off 12–20 h: 12:35.

### 758 Benešov - Popovice - Postupice
- **Core points:** Benešov, Terminál | Postupice, Pozov | Popovice | Postupice, škola. Anchor 16:00.
- **Reading:** Benešov – Struhařov – Postupice, Pozov – Popovice – Postupice, škola, a school line: Benešov 11:50, 14:50, 17:40 out, Postupice 13:12, 15:32 back. Every 180, the interval its Benešov trips have (11:50 and 14:50 exact, 17:50 for the 17:40), with Postupice 15:32 (2-minute turn at Postupice, škola; 13:12 off), one bus; the only service of Popovice, Mladovice (3 stops) and the Postupice villages Chudláz, Jezviny, Kopaniny, Miroslav, Nová Ves, Podlesí and Pozov.
- **Choice:** Changed on 2 Nov after the review: every 180, the interval its Benešov trips have (11:50 and 14:50 exact, 17:50 for the 17:40, 10 min), with Postupice 15:32 (2-minute turn at Postupice, škola, `lay` 2); the first design's every 240 held 14:50 only. Same typed values (109 / 151), 1 bus. Every 120 leaves a 16:50 slot without a trip in the window.
- **758**, every 180, 1 bus (window 15:30–17:30; waits Benešov, Terminál [100]; Postupice, škola [2])
  - Benešov, Terminál → Postupice, škola: 14:50 (every 180 from 12:00), typed 109, 40 min. Step 4: no slot in the window (real there: none); day 2 exact / 2 within 3 of 3. Off 12–20 h: 17:40.
  - Postupice, škola → Benešov, Terminál: 12:32 (every 180 from 12:00), typed 151, 38 min [lay 2]. Step 4: window slots 15:32 / real 15:32, filled 1/1; day 1 exact / 1 within 3 of 4. Off 12–20 h: 13:12.

### 759 Benešov - Maršovice - Křečovice,Strážovice - Neveklov
- **Core points:** Benešov, Terminál | Maršovice | Křečovice, Strážovice | Neveklov. Anchor 15:00 (set by hand).
- **Reading:** Benešov – Bystřice – Maršovice – Neveklov, plus Neveklov – Křečovice, Strážovice shorts. Benešov :04 hourly 14:04–16:04 (then 17:39), Neveklov 13:57, 14:57, 16:02; model hour set by hand to 15:00 (the 16:00 window holds one trip each way), every 120 with two slots each way, exact. The way back runs the 14:57 road via Jírovice, Kukačka, Tvoršovice and Zderadice (stops only 759 serves); the 16:02 really runs via Bystřice town (on 408, 558, 564). 759 Strážovice is the only service of Strnadice, Šebáňovice, rozcestí, Sedlečko, rozcestí and Hodětice.
- **Choice:** At 16:00 one trip each way (16:04, 16:02) and hourly :04 / :57 leave a window slot empty both ways. Anchor 15:00 by hand. Hourly :04 / :59 passes with 0 exact at Neveklov; every 120 with two slots each way (Neveklov 14:57 and 16:02 on the minute) passes with more exact hits, 2 buses either way. The two back slots run two roads in reality (14:57 via Jírovice, 16:02 via Bystřice town); the Simutrans line takes the Jírovice road (`stops_via`) because Jírovice, Kukačka and Zderadice have no other line; the path audit flags the 16:02, explained on the card. 759 Strážovice (Neveklov 12:47 / Strážovice 13:21, every 240) is the only service of Strnadice, Šebáňovice, rozcestí, Sedlečko, rozcestí and Hodětice.
- **759**, every 120, 2 buses (window 14:30–16:30; waits Benešov, Terminál [19, 24]; Neveklov [15, 20])
  - Benešov, Terminál → Neveklov: 12:04, 13:04 (every 120 from 12:00), typed 3, 63, 38 min. Step 4: window slots 15:04, 16:04 / real 15:04, 16:04, filled 2/2; day 4 exact / 4 within 3 of 6. Off 12–20 h: 17:39.
  - Neveklov → Benešov, Terminál: 12:02, 12:57 (every 120 from 12:00), typed 61, 116, 43 min [stops_via Bystřice, Jírovice]. Step 4: window slots 14:57, 16:02 / real 14:57, 16:02, filled 2/2; day 2 exact / 3 within 3 of 5. Off 12–20 h: 13:57.
- **759 Strážovice**, every 240, 1 bus (window 14:30–16:30; waits Neveklov [183]; Křečovice, Strážovice [11])
  - Neveklov → Křečovice, Strážovice: 12:47 (every 240 from 12:00), typed 226, 23 min. Step 4: no slot in the window (real there: none); day 1 exact / 1 within 3 of 2. Off 12–20 h: 16:57.
  - Křečovice, Strážovice → Neveklov: 13:21 (every 240 from 12:00), typed 20, 23 min. Step 4: no slot in the window (real there: none); day 1 exact / 2 within 3 of 2.

### 791 Benešov - Český Šternberk - Uhlířské Janovice
- **Core points:** Benešov, Terminál | Český Šternberk | Český Šternberk, Čejkovice | Uhlířské Janovice, náměstí. Anchor 16:00.
- **Reading:** Benešov – Struhařov – Třebešice – Divišov – Český Šternberk – Uhlířské Janovice. Benešov :45 every hour, alternating: odd hours to Uhlířské Janovice (13:48, 15:45, 17:45), even hours to Český Šternberk, Čejkovice (12:45, 14:45, 16:45); back from Uhlířské Janovice :07 odd hours (13:07–19:07) and from Čejkovice :33 even hours (14:33, 16:33). One Simutrans line per end, each every 120 and exact. Pooling option (not applied): the buses alternate between the two ends at Benešov, which as one circuit would need 3 buses instead of 4.
- **Choice:** Benešov :45 alternates by hour between the two ends, back from Uhlířské Janovice :07 odd and from Čejkovice :33 even: two lines every 120, both exact, 2 + 2 buses. One circuit B – Uhlířské Janovice – B – Čejkovice – B (360-minute round) would need 3; the timetable has no 0–5-minute chain at Benešov (the buses wait about 30 min there), so it is offered as pooling, not applied.
- **791**, every 120, 2 buses (window 15:30–17:30; waits Benešov, Terminál [91]; Uhlířské Janovice, náměstí [15])
  - Benešov, Terminál → Uhlířské Janovice, náměstí: 13:45 (every 120 from 12:00), typed 44, 67 min. Step 4: window slots 15:45 / real 15:45, filled 1/1; day 2 exact / 4 within 3 of 6.
  - Uhlířské Janovice, náměstí → Benešov, Terminál: 13:07 (every 120 from 12:00), typed 6, 67 min. Step 4: window slots 17:07 / real 17:07, filled 1/1; day 4 exact / 4 within 3 of 7.
- **791 Čejkovice**, every 120, 2 buses (window 15:30–17:30; waits Benešov, Terminál [92]; Český Šternberk, Čejkovice [66])
  - Benešov, Terminál → Český Šternberk, Čejkovice: 12:45 (every 120 from 12:00), typed 104, 42 min. Step 4: window slots 16:45 / real 16:45, filled 1/1; day 4 exact / 4 within 3 of 5.
  - Český Šternberk, Čejkovice → Benešov, Terminál: 12:33 (every 120 from 12:00), typed 92, 40 min. Step 4: window slots 16:33 / real 16:33, filled 1/1; day 3 exact / 3 within 3 of 4.

### 796 Benešov - Soběhrdy - Čerčany - Pyšely
- **Core points:** Benešov, Terminál | Pyšely, náměstí. Anchor 16:00.
- **Reading:** Benešov, Terminál – Soběhrdy – Přestavlky – Vranov – Čerčany – Pyšely, náměstí. Hourly: Benešov :35 (14:35–17:35; :40 before), Pyšely :56 (15:56–18:56; :11 before 15:00). Off: Benešov 12:40, 13:40; Pyšely 12:11, 13:11, 14:11, 15:21.
- **Choice:** Hourly :35 / :56 exact in the window; 3 buses (waits 51 at Benešov, 35 at Pyšely). Before 15:00 Pyšely runs at :11 (off).
- **796**, every 60, 3 buses (window 15:30–17:30; waits Benešov, Terminál [51]; Pyšely, náměstí [35])
  - Benešov, Terminál → Pyšely, náměstí: :35, typed 34, 46 min. Step 4: window slots 15:35, 16:35 / real 15:35, 16:35, filled 2/2; day 5 exact / 5 within 3 of 12. Off 12–20 h: 12:40, 13:40.
  - Pyšely, náměstí → Benešov, Terminál: :56, typed 55, 48 min. Step 4: window slots 15:56, 16:56 / real 15:56, 16:56, filled 2/2; day 4 exact / 4 within 3 of 12. Off 12–20 h: 12:11, 13:11, 14:11, 15:21.

### 798 Benešov - Čakov - Ostředek - Sázava
- **Core points:** Benešov, Terminál | Teplýšovice, Kochánov | Ostředek | Sázava, autobusové stanoviště. Anchor 14:30.
- **Reading:** Benešov – Struhařov – Teplýšovice – Čakov – Ostředek – Xaverov – Sázava. Every 2 hours: Benešov :18 even hours (exact 8:18–18:18), Sázava :31 (15:31, 17:31, 19:31; also 14:31). Off: Sázava 12:37, 14:31; the Sázava – Ostředek shuttle 13:31 / 14:00 is on 798's path.
- **Choice:** Every 120: Benešov even :18 (6 exact), Sázava odd :31 (15:31, 17:31, 19:31). The real 4-minute turn at Sázava (15:27 → 15:31) is in the pattern; 2 buses.
- **798**, every 120, 2 buses (window 14:00–16:00; waits Benešov, Terminál [98]; Sázava, autobusové stanoviště [4])
  - Benešov, Terminál → Sázava, autobusové stanoviště: 12:18 (every 120 from 12:00), typed 77, 69 min. Step 4: window slots 14:18 / real 14:18, filled 1/1; day 6 exact / 6 within 3 of 7.
  - Sázava, autobusové stanoviště → Benešov, Terminál: 13:31 (every 120 from 12:00), typed 30, 69 min. Step 4: window slots 15:31 / real 14:31, 15:31, filled 1/1; day 3 exact / 3 within 3 of 8. Off 12–20 h: 12:37, 14:31.

### 799 Vlašim - Chotýšany - Struhařov - Benešov
- **Core points:** Benešov, Terminál | Chotýšany | Bílkovice, u kapličky | Vlašim, Terminál. Anchor 14:00 (set by hand).
- **Reading:** Vlašim – Chotýšany – Struhařov – Benešov. Hourly 12:49–14:50 (Benešov :49, Vlašim :50, via Bílkovice, u kapličky), then Benešov 16:29, 17:59 and Vlašim 16:20 only. Model hour set by hand to 14:00, where the line's pattern runs (the 16:00 window holds one trip each way, both 20 min off any hourly slot). Off: Benešov 16:29, 17:59; Vlašim 16:20.
- **Choice:** Hourly only 12:49–14:50; the 16:00 window has Benešov 16:29 and Vlašim 16:20, 20 min off any hourly phase. The busiest two hours are 13:00–15:00, so anchor 14:00 by hand; hourly :49 / :50, 2 buses.
- **799**, every 60, 2 buses (window 13:30–15:30; waits Benešov, Terminál [7]; Vlašim, Terminál [15])
  - Benešov, Terminál → Vlašim, Terminál: :49, typed 48, 46 min. Step 4: window slots 13:49, 14:49 / real 13:49, 14:49, filled 2/2; day 4 exact / 4 within 3 of 7. Off 12–20 h: 16:29, 17:59.
  - Vlašim, Terminál → Benešov, Terminál: :50, typed 49, 52 min. Step 4: window slots 13:50, 14:50 / real 13:50, 14:50, filled 2/2; day 3 exact / 3 within 3 of 6. Off 12–20 h: 16:20.

### 789 Vlašim – Psáře - Divišov
- **Core points:** Vlašim, Terminál | Psáře | Divišov, náměstí. Anchor 16:00.
- **Reading:** Vlašim – Kladruby – Tehov – Psáře – Divišov. Every 2 hours: Vlašim :08 even hours (14:08, 16:08, 18:08), Divišov :25 odd hours (11:25–17:25). Exact on every afternoon trip.
- **Choice:** Every 120 exact (Vlašim even :08, Divišov odd :25). 2 buses (the Vlašim end waits 106 min, as the real buses do).
- **789**, every 120, 2 buses (window 15:30–17:30; waits Vlašim, Terminál [106]; Divišov, náměstí [19])
  - Vlašim, Terminál → Divišov, náměstí: 12:08 (every 120 from 12:00), typed 67, 58 min. Step 4: window slots 16:08 / real 16:08, filled 1/1; day 3 exact / 3 within 3 of 6.
  - Divišov, náměstí → Vlašim, Terminál: 13:25 (every 120 from 12:00), typed 24, 57 min. Step 4: window slots 17:25 / real 17:25, filled 1/1; day 4 exact / 4 within 3 of 6.

### 790 Vlašim - Libež - Divišov
- **Core points:** Vlašim, Terminál | Divišov, náměstí. Anchor 15:00 (set by hand).
- **Reading:** Vlašim – Libež – Všechlapy – Divišov. Hourly: Vlašim :06 (13:06–16:06, 18:06), Divišov :20 (13:20–17:20). Model hour set by hand to 15:00: the 16:00 window holds the missing 17:06 (the 305 rule). Its buses arrive at Vlašim at :50, the minute 426 leaves for Prague (8 of 8: the Vlašim connection, not a through bus).
- **Choice:** Hourly exact, but no 17:06 from Vlašim: the 16:00 window would hold an empty slot. Anchor 15:00 by hand (the 305 rule).
- **790**, every 60, 2 buses (window 14:30–16:30; waits Vlašim, Terminál [16]; Divišov, náměstí [45])
  - Vlašim, Terminál → Divišov, náměstí: :06, typed 5, 29 min. Step 4: window slots 15:06, 16:06 / real 15:06, 16:06, filled 2/2; day 8 exact / 8 within 3 of 9.
  - Divišov, náměstí → Vlašim, Terminál: :20, typed 19, 30 min. Step 4: window slots 15:20, 16:20 / real 15:20, 16:20, filled 2/2; day 7 exact / 7 within 3 of 9.

### 792 Vlašim - Vracovice - Rataje
- **Core points:** Vlašim, Terminál | Zdislavice | Rataje, dolní. Anchor 16:00.
- **Reading:** Vlašim – Vracovice – Zdislavice – Rataje. Every 2 hours: Vlašim :45 even hours (14:45 from ZŠ Vorlina, 16:45, 18:45), Rataje :12 odd hours (13:12–17:12), with a 5-minute turn at Rataje. Exact all afternoon.
- **Choice:** Every 120 exact, 5-minute turn at Rataje in the pattern; 1 bus.
- **792**, every 120, 1 bus (window 15:30–17:30; waits Vlašim, Terminál [70]; Rataje, dolní [5])
  - Vlašim, Terminál → Rataje, dolní: 12:45 (every 120 from 12:00), typed 104, 22 min. Step 4: window slots 16:45 / real 16:45, filled 1/1; day 5 exact / 5 within 3 of 5.
  - Rataje, dolní → Vlašim, Terminál: 13:12 (every 120 from 12:00), typed 11, 23 min. Step 4: window slots 17:12 / real 17:12, filled 1/1; day 4 exact / 4 within 3 of 7.

### 794 Vlašim - Trhový Štěpánov - Kácov
- **Core points:** Vlašim, Terminál | Trhový Štěpánov, náměstí | Kácov, náměstí. Anchor 16:00.
- **Reading:** Vlašim – Zdislavice – Javorník – Trhový Štěpánov – Tichonice – Kácov. Vlašim :45 even hours to Kácov (12:45, 14:45, 16:45); back from Kácov 12:44, 14:44, 15:52, 17:42 (no fixed minute). Every 120 at Vlašim :45 and Kácov 15:52; the Kácov 15:52 bus leaves Vlašim again at 16:45 on arrival (0-minute turn, 4 of 7). Off: Kácov 12:44, 14:44, 17:42; Vlašim 15:45 → Zdislavice and 18:15 → Trhový Štěpánov.
- **Choice:** Kácov departures have no fixed minute (12:44, 14:44, 15:52, 17:42); Kácov :52 odd is the only phase that passes in the window. The 15:52 bus leaves Vlašim at 16:45 on arrival (4 of 7 real 0-minute turns): `lay` 0, 1 bus.
- **794**, every 120, 1 bus (window 15:30–17:30; waits Vlašim, Terminál [0]; Kácov, náměstí [16])
  - Vlašim, Terminál → Kácov, náměstí: 12:45 (every 120 from 12:00), typed 104, 51 min [lay 0]. Step 4: window slots 16:45 / real 16:45, filled 1/1; day 3 exact / 3 within 3 of 6.
  - Kácov, náměstí → Vlašim, Terminál: 13:52 (every 120 from 12:00), typed 51, 53 min. Step 4: window slots 15:52 / real 15:52, filled 1/1; day 1 exact / 1 within 3 of 6. Off 12–20 h: 12:44, 14:44, 17:42.

### 795 Vlašim - Zruč nad Sázavou
- **Core points:** Vlašim, Terminál | Trhový Štěpánov, náměstí | Zruč nad Sázavou, Sázavan. Anchor 17:00 (set by hand).
- **Reading:** Vlašim – Kladruby – Trhový Štěpánov – Soutice – Hulice – Zruč nad Sázavou. Hourly from 16:00: Vlašim :00 (16:00–18:00, 19:00 to Trhový Štěpánov), Zruč :35 (16:35–18:35); before that no fixed minute (Vlašim 13:10, 14:45; Zruč 12:40, 15:10). Model hour set by hand to 17:00, where the hourly pattern runs. The Trhový Štěpánov shorts (12:10, 12:34, 14:10, 14:39) are on 795's path.
- **Choice:** No hourly phase passes at the auto anchor 14:40 (Vlašim 14:45, 16:00; Zruč 15:10 only). From 16:00 the line is exactly hourly (Vlašim :00, Zruč :35), so the anchor is set to 17:00 by hand; 3 buses.
- **795**, every 60, 3 buses (window 16:30–18:30; waits Vlašim, Terminál [30]; Zruč nad Sázavou, Sázavan [40])
  - Vlašim, Terminál → Zruč nad Sázavou, Sázavan: :00, typed 59, 55 min [core_to Trhový Štěpánov, náměstí]. Step 4: window slots 17:00, 18:00 / real 17:00, 18:00, filled 2/2; day 4 exact / 4 within 3 of 13. Off 12–20 h: 12:10, 13:10, 14:10, 14:45.
  - Zruč nad Sázavou, Sázavan → Vlašim, Terminál: :35, typed 34, 55 min. Step 4: window slots 16:35, 17:35 / real 16:35, 17:35, filled 2/2; day 4 exact / 4 within 3 of 9. Off 12–20 h: 12:40, 15:10.

### 840 Vlašim - Vlašim,Nesperská Lhota
- **Core points:** Vlašim, Terminál | Vlašim, Nesperská Lhota. Anchor 16:00.
- **Reading:** Vlašim town line to Nesperská Lhota. Vlašim 12:45, 14:50, 16:50 and Nesperská Lhota 12:55, 15:00, 17:00, each bus turning at Nesperská Lhota on arrival. Every 120, one bus: the only service of Nesperská Lhota, Polánka, Znosim and vodárna.
- **Choice:** Every 120 at Vlašim :50 / Nesperská Lhota :00 with the real 0-minute turn (5 of 5): 1 bus. The s4 search's every-480 rows with several slots were rejected (more slots than trips over the afternoon).
- **840**, every 120, 1 bus (window 15:30–17:30; waits Vlašim, Terminál [100]; Vlašim, Nesperská Lhota [0])
  - Vlašim, Terminál → Vlašim, Nesperská Lhota: 12:50 (every 120 from 12:00), typed 109, 10 min. Step 4: window slots 16:50 / real 16:50, filled 1/1; day 2 exact / 2 within 3 of 5. Off 12–20 h: 12:45.
  - Vlašim, Nesperská Lhota → Vlašim, Terminál: 13:00 (every 120 from 12:00), typed 119, 10 min [lay 0]. Step 4: window slots 17:00 / real 17:00, filled 1/1; day 2 exact / 2 within 3 of 5. Off 12–20 h: 12:55.

### 841 Vlašim,Hrazená Lhota - Vlašim
- **Core points:** Vlašim, Terminál | Vlašim, Domašín, náměstí | Vlašim, Hrazená Lhota. Anchor 14:20.
- **Reading:** Vlašim town line: Terminál – Sukova loop – Terminál – Městský úřad – sídliště – Domašín – Hrazená Lhota. Hourly: Terminál :51 (12:51–14:51, 16:51), Hrazená Lhota :23 (13:23–15:23, 17:23), each bus turning at Hrazená Lhota on arrival. Modelled at its anchor (14:20). Listed: the Domašín shorts 14:18 / 14:59.
- **Choice:** Hourly at the auto anchor 14:20, exact; 15:51 and 16:23 have no trip in reality (outside the window). 0-minute turn at Hrazená Lhota (4 of 7): 1 bus.
- **841**, every 60, 1 bus (window 13:50–15:50; waits Vlašim, Terminál [7]; Vlašim, Hrazená Lhota [0])
  - Vlašim, Terminál → Vlašim, Hrazená Lhota: :51, typed 50, 32 min. Step 4: window slots 13:51, 14:51 / real 13:51, 14:51, filled 2/2; day 5 exact / 5 within 3 of 7.
  - Vlašim, Hrazená Lhota → Vlašim, Terminál: :23, typed 22, 21 min [lay 0]. Step 4: window slots 14:23, 15:23 / real 14:23, 15:23, filled 2/2; day 5 exact / 5 within 3 of 7.

### 842 Vlašim - Borovnice - Studený - Dolní Kralovice
- **Core points:** Vlašim, Terminál | Čechtice | Dolní Kralovice. Anchor 16:00.
- **Reading:** Vlašim – Borovnice – Čechtice – Křivsoudov – Studený – Dolní Kralovice, with Vlašim – Čechtice shorts. To Dolní Kralovice every 2 hours: Vlašim :15 odd hours (13:15–17:15), Dolní Kralovice :01 odd hours (17:01, 19:01; 12:57 and 14:57 four minutes off). Shorts: Vlašim 14:20, 15:30, 16:20, 18:40; Čechtice 14:22, 16:22. One line per destination; the shorts' line is the real turn of the 15:30 bus (Čechtice 15:48, back 16:22); Vlašim 14:20, 16:20 and 18:40 are off the pattern.
- **Choice:** Dolní Kralovice every 120 (Vlašim odd :15, Dolní Kralovice odd :01, 4 exact; :57 even fails the window). The Čechtice shorts are a regular variant (5 out, 4 back a day), their own line every 120. Changed on 2 Nov after the review: Vlašim 15:30 / Čechtice 16:22, the real 34-minute turn of the 15:30 bus, 1 bus; the first design's Vlašim 16:20 had one more exact hit but waits of 104 and 100 min and 2 buses. Vlašim 14:20, 16:20 and 18:40 are listed.
- **842**, every 120, 2 buses (window 15:30–17:30; waits Vlašim, Terminál [88]; Dolní Kralovice [58])
  - Vlašim, Terminál → Dolní Kralovice: 13:15 (every 120 from 12:00), typed 14, 48 min. Step 4: window slots 17:15 / real 17:15, filled 1/1; day 3 exact / 3 within 3 of 8.
  - Dolní Kralovice → Vlašim, Terminál: 13:01 (every 120 from 12:00), typed 0, 46 min. Step 4: window slots 17:01 / real 17:01, filled 1/1; day 5 exact / 5 within 3 of 9. Off 12–20 h: 12:01, 12:57, 14:57.
- **842 Čechtice**, every 120, 1 bus (window 15:30–17:30; waits Vlašim, Terminál [50]; Čechtice [34])
  - Vlašim, Terminál → Čechtice: 13:30 (every 120 from 12:00), typed 29, 18 min [notvia Dolní Kralovice]. Step 4: window slots 15:30 / real 15:30, 16:20, filled 1/1; day 1 exact / 1 within 3 of 5. Off 12–20 h: 14:20, 16:20, 18:40.
  - Čechtice → Vlašim, Terminál: 12:22 (every 120 from 12:00), typed 81, 18 min [notvia Dolní Kralovice]. Step 4: window slots 16:22 / real 16:22, filled 1/1; day 2 exact / 2 within 3 of 3.

### 843 Vlašim - Křivsoudov - Čechtice
- **Core points:** Vlašim, Terminál | Mnichovice | Čechtice. Anchor 16:00.
- **Reading:** Vlašim – Kuňovice – Mnichovice – Strojetice – Křivsoudov – Čechtice, a sparse line: Vlašim 6:15, 10:15, 12:15, 14:45, 18:15; Čechtice 5:03, 6:57, 8:13, 13:12 (from škola), 15:48 (to Mnichovice), 17:13. Bent onto every 240 at its afternoon round, Vlašim 14:45 → Čechtice 15:23 and Čechtice 17:13 → Vlašim (13:12 is 1 min off the 13:13 repeat): one bus, the only service of Keblov, Mnichovice and Strojetice. Off: Vlašim 6:15, 10:15, 18:15 (30 min off the repeats) and 12:15; Čechtice 15:48 to Mnichovice.
- **Choice:** Changed on 2 Nov after the review: every 240 at the afternoon round, Vlašim 14:45 → Čechtice 15:23 and Čechtice 17:13 → Vlašim (13:12 is 1 min off the 13:13 repeat), 1 bus. The first design's every 360 at 12:15 / 13:13 followed the morning rhythm (6:15, 12:15, 18:15 exact) but ran nothing between 13:13 and 18:15; the sheet stands for the afternoon. Off: Vlašim 6:15, 10:15, 18:15 (30 min off the repeats), 12:15; Čechtice 15:48 to Mnichovice.
- **843**, every 240, 1 bus (window 15:30–17:30; waits Vlašim, Terminál [54]; Čechtice [110])
  - Vlašim, Terminál → Čechtice: 14:45 (every 240 from 12:00), typed 104, 38 min. Step 4: no slot in the window (real there: none); day 1 exact / 1 within 3 of 5. Off 12–20 h: 12:15, 18:15.
  - Čechtice → Vlašim, Terminál: 13:13 (every 240 from 12:00), typed 12, 38 min. Step 4: window slots 17:13 / real 17:13, filled 1/1; day 2 exact / 2 within 3 of 5.

### 844 Vlašim - Trhový Štěpánov - Loket
- **Core points:** Vlašim, Terminál | Trhový Štěpánov, městský úřad | Loket, u dálnice. Anchor 14:10.
- **Reading:** Vlašim – Kladruby – Trhový Štěpánov – Keblov – Loket, u dálnice. Hourly: Vlašim :41 (12:41–14:41, 16:41), Loket :35 (13:35–15:35). Modelled at its anchor (14:10). The Trhový Štěpánov – Loket trips 17:35 / 18:02 are on its path.
- **Choice:** Hourly at the auto anchor 14:10 (window 13:40–15:40), exact both ways; 15:41 has no trip (outside the window).
- **844**, every 60, 2 buses (window 13:40–15:40; waits Vlašim, Terminál [23]; Loket, u dálnice [10])
  - Vlašim, Terminál → Loket, u dálnice: :41, typed 40, 44 min. Step 4: window slots 13:41, 14:41 / real 13:41, 14:41, filled 2/2; day 6 exact / 6 within 3 of 7.
  - Loket, u dálnice → Vlašim, Terminál: :35, typed 34, 43 min. Step 4: window slots 14:35, 15:35 / real 14:35, 15:35, filled 2/2; day 5 exact / 5 within 3 of 7.

### 846 Dolní Kralovice - Ledeč nad Sázavou
- **Core points:** Dolní Kralovice | Loket, u dálnice | Ledeč nad Sázavou, Husovo náměstí. Anchor 16:00.
- **Reading:** Dolní Kralovice – Loket, u dálnice – Bernartice – Hněvkovice – Kožlí – Ledeč nad Sázavou (Vysočina). Exactly hourly: Dolní Kralovice :17 (17:17 ends at Loket, u dálnice and runs on in the game), Ledeč :01, with a 3-minute turn at Ledeč.
- **Choice:** Exactly hourly; the 17:17 to Loket, u dálnice read with `core_to`; real 3-minute turn at Ledeč. 2 buses.
- **846**, every 60, 2 buses (window 15:30–17:30; waits Dolní Kralovice [35]; Ledeč nad Sázavou, Husovo náměstí [3])
  - Dolní Kralovice → Ledeč nad Sázavou, Husovo náměstí: :17, typed 16, 41 min [core_to Loket, u dálnice]. Step 4: window slots 16:17, 17:17 / real 16:17, 17:17, filled 2/2; day 11 exact / 11 within 3 of 12.
  - Ledeč nad Sázavou, Husovo náměstí → Dolní Kralovice: :01, typed 0, 41 min. Step 4: window slots 16:01, 17:01 / real 16:01, 17:01, filled 2/2; day 11 exact / 11 within 3 of 11.

### 847 Dolní Kralovice - Snět - Dolní Kralovice
- **Core points:** Dolní Kralovice | Snět. Anchor 16:00.
- **Reading:** Dolní Kralovice – Blažejovice – Snět – Šetějovice – Dolní Kralovice, a one-way circle (27 min). Afternoon 12:44, 14:44, 16:44 (every 2 hours) and 18:04. One bus every 120; the only service of its seven villages.
- **Choice:** A one-way circle; one leg Dolní Kralovice → Dolní Kralovice every 120 at :44 (12:44, 14:44, 16:44 exact).
- **847**, every 120, 1 bus (window 15:30–17:30; waits Dolní Kralovice [93])
  - Dolní Kralovice → Dolní Kralovice: 12:44 (every 120 from 12:00), typed 103, 27 min. Step 4: window slots 16:44 / real 16:44, filled 1/1; day 3 exact / 3 within 3 of 8. Off 12–20 h: 18:04.

### 848 Vlašim - Pravonín - Načeradec,Zdiměřice
- **Core points:** Vlašim, Terminál | Pravonín | Načeradec | Načeradec, Zdiměřice. Anchor 15:10.
- **Reading:** Vlašim – Vracovice – Pravonín – Načeradec (– Zdiměřice). Hourly in the model hour (anchor 15:10): Vlašim :50 (14:50, 15:50; 12:50, 17:50, 19:50), Načeradec :38 (15:38, 16:38, 18:38). Off: Načeradec 12:08, 13:18, 14:48. The morning Zdiměřice round (Vlašim 6:15 → Zdiměřice 6:55 → Vlašim 7:34) is 848 Zdiměřice, every 480: by the owner's rule of 2 Nov 2026 the Načeradec villages whose only afternoon service is PID Haló 887 get a line from their fixed trips, and its bus also runs Haló's Novotinky loop, which has no fixed trip of its own.
- **Choice:** Every 120 with one slot each way was FEWER (Načeradec 14:48, 15:38, 16:38 in the window); hourly :50 / :38 passes both ways, 2 buses. 848 Zdiměřice: the owner decided on 2 Nov 2026 that places whose only afternoon service is PID Haló get a line from their fixed trips (at most every 480): it runs the real school round Vlašim 6:15 → Zdiměřice 6:55 → Načeradec (both slots real, Step 4 window set to 6:00–8:00), then untimed Haló 887's Načeradec – Horní Lhota, u váhy – Novotinky – Dolní Lhota – Vračkovice loop (18 min, those two stops have no fixed trip at all) and back to Vlašim; 1 bus, the same as before.
- **848**, every 60, 2 buses (window 14:40–16:40; waits Vlašim, Terminál [44]; Načeradec [20])
  - Vlašim, Terminál → Načeradec: :50, typed 49, 28 min [notvia Načeradec, Zdiměřice]. Step 4: window slots 14:50, 15:50 / real 14:50, 15:50, filled 2/2; day 5 exact / 5 within 3 of 8.
  - Načeradec → Vlašim, Terminál: :38, typed 37, 28 min [notvia Načeradec, Zdiměřice]. Step 4: window slots 15:38, 16:38 / real 14:48, 15:38, 16:38, filled 2/2; day 3 exact / 3 within 3 of 7. Off 12–20 h: 12:08, 13:18, 14:48.
- **848 Zdiměřice**, every 480, 1 bus (window 6:00–8:00; waits Vlašim, Terminál (1) [383]; Načeradec, Zdiměřice (2) [0]; Načeradec (3) [0]; Načeradec (4) [0])
  - Vlašim, Terminál → Načeradec, Zdiměřice: 14:15 (every 480 from 12:00), typed 314, 40 min. Step 4: window slots 6:15 / real 6:15, filled 1/1; day 1 exact / 1 within 3 of 1.
  - Načeradec, Zdiměřice → Načeradec: 14:55 (every 480 from 12:00), typed 354, 11 min [lay 0]. Step 4: window slots 6:55 / real 6:55, filled 1/1; day 1 exact / 1 within 3 of 1.
  - Načeradec → Načeradec: untimed (empty return), 18 min
  - Načeradec → Vlašim, Terminál: untimed (empty return), 28 min

### 849 Vlašim - Chmelná - Pravonín
- **Core points:** Vlašim, Terminál | Pravonín | Čechtice, Jeníkov. Anchor 16:00.
- **Reading:** Vlašim – Bolina – Zdislavice – Miřetice – Chmelná – Pravonín – Čechtice, Jeníkov. Every 2 hours: Vlašim :50 even hours (14:50, 16:50, 18:50), Jeníkov :26 odd hours (15:26, 17:26), turning at Jeníkov in 1 minute. Off: Vlašim 12:30; Jeníkov 13:06. No stop is 849's alone; it is kept as a regular 2-hourly line (7 trips each way a day), not a sparse one.
- **Choice:** Every 120 exact, real 1-minute turn at Jeníkov (5 of 6): 1 bus. The reading lists no stop only 849 serves; it is kept as a regular 2-hourly line (7 trips each way a day), not a sparse one.
- **849**, every 120, 1 bus (window 15:30–17:30; waits Vlašim, Terminál [48]; Čechtice, Jeníkov [1])
  - Vlašim, Terminál → Čechtice, Jeníkov: 12:50 (every 120 from 12:00), typed 109, 35 min. Step 4: window slots 16:50 / real 16:50, filled 1/1; day 3 exact / 3 within 3 of 6. Off 12–20 h: 12:30.
  - Čechtice, Jeníkov → Vlašim, Terminál: 13:26 (every 120 from 12:00), typed 25, 36 min [lay 1]. Step 4: window slots 17:26 / real 17:26, filled 1/1; day 2 exact / 2 within 3 of 7. Off 12–20 h: 13:06.

### 455 Mladá Vožice - Načeradec - Vlašim
- **Core points:** Vlašim, Terminál | Načeradec | Mladá Vožice, autobusové stanoviště. Anchor 16:00.
- **Reading:** Mladá Vožice – Vilice – Načeradec – Pravonín – Kondrac – Vlašim (Jihočeský operator). Every 2 hours all day: Vlašim :55 odd hours, Mladá Vožice :00 even hours, exact; the bus turns at Vlašim in 5 minutes. Its arrivals at Vlašim (:50) meet 426 to Prague.
- **Choice:** Every 120 exact both ways; the 5-minute turn at Vlašim (4 of 7) gives 1 bus.
- **455**, every 120, 1 bus (window 15:30–17:30; waits Vlašim, Terminál [5]; Mladá Vožice, autobusové stanoviště [21])
  - Vlašim, Terminál → Mladá Vožice, autobusové stanoviště: 12:55 (every 120 from 12:00), typed 114, 44 min. Step 4: window slots 16:55 / real 16:55, filled 1/1; day 5 exact / 5 within 3 of 7.
  - Mladá Vožice, autobusové stanoviště → Vlašim, Terminál: 12:00 (every 120 from 12:00), typed 59, 50 min. Step 4: window slots 16:00 / real 16:00, filled 1/1; day 4 exact / 4 within 3 of 6.

### 453 Tábor - Ratibořské Hory - Mladá Vožice - Vlašim
- **Core points:** Tábor, autobusové nádraží | Mladá Vožice, autobusové stanoviště | Vlašim, Terminál | Vlašim, zbrojovka. Anchor 16:00 (set by hand).
- **Reading:** Tábor – Ratibořské Hory – Mladá Vožice, every 30 minutes (Tábor :15 / :45, Mladá Vožice :15 / :45), the even-hour :15 out of Tábor running on to Vlašim (14:15, 16:15) and Vlašim :55 odd hours back (15:55, 17:55, passing Mladá Vožice at the even :45). Model hour set by hand to 16:00, where this holds; before 16:00 the Vlašim trips pass Mladá Vožice at 13:45 and 15:15. Two lines: 453 (three of the four 2-hour slots, Tábor – Mladá Vožice) and 453 Vlašim (the fourth). Off: Mladá Vožice 12:45, 14:45; Vlašim 12:55, 14:18.
- **Choice:** Trunk every 30 at both ends, the even :15 from Tábor to Vlašim. At the auto anchor (14:40) the Vlašim trip passes Mladá Vožice at 15:15 (odd), at 16:00 at 16:45 (even): the line is regular from 16:00 (Tábor :15/:45 to 19:15), so anchor 16:00 by hand, where the trunk's three slots per 2 hours are all real at both ends (the 14:40 window left one trunk slot empty, EMPTY in the first run). 0-minute turns at Tábor and Mladá Vožice (arrivals and departures on the same minutes): `lay` 0, 2 buses (4 with the default 3-minute wait). 453 Vlašim back by Ostrov and Hradiště (`stops_via` Hradiště) as the 15:55 runs.
- **453**, every 120, 2 buses (window 15:30–17:30; waits Tábor, autobusové nádraží [30, 30, 0]; Mladá Vožice, autobusové stanoviště [0, 0, 0])
  - Tábor, autobusové nádraží → Mladá Vožice, autobusové stanoviště: 12:45, 13:15, 13:45 (every 120 from 12:00), typed 14, 44, 104, 30 min [notvia Vlašim, Terminál; lay 0]. Step 4: window slots 15:45, 16:45, 17:15 / real 15:45, 16:45, 17:15, filled 3/3; day 16 exact / 16 within 3 of 21. Off 12–20 h: 18:15.
  - Mladá Vožice, autobusové stanoviště → Tábor, autobusové nádraží: 12:15, 13:15, 13:45 (every 120 from 12:00), typed 14, 44, 74, 30 min [notvia Vlašim, Terminál; lay 0]. Step 4: window slots 15:45, 16:15, 17:15 / real 15:45, 16:15, 17:15, filled 3/3; day 17 exact / 17 within 3 of 21. Off 12–20 h: 12:45, 14:45.
- **453 Vlašim**, every 120, 2 buses (window 15:30–17:30; waits Tábor, autobusové nádraží [60]; Vlašim, Terminál [27])
  - Tábor, autobusové nádraží → Vlašim, Terminál: 12:15 (every 120 from 12:00), typed 74, 73 min. Step 4: window slots 16:15 / real 16:15, filled 1/1; day 3 exact / 3 within 3 of 7.
  - Vlašim, Terminál → Tábor, autobusové nádraží: 13:55 (every 120 from 12:00), typed 54, 80 min [stops_via Hradiště]. Step 4: window slots 15:55 / real 15:55, filled 1/1; day 2 exact / 2 within 3 of 5. Off 12–20 h: 12:55, 14:18.

### 452 Olbramovice - Mladá Vožice - Oldřichov
- **Core points:** Mladá Vožice, autobusové stanoviště | Votice, autobusové stanoviště | Olbramovice, železniční stanice. Anchor 16:00.
- **Reading:** Mladá Vožice – Slapsko – Neustupov – Votice – Olbramovice, železniční stanice. Exactly hourly: Mladá Vožice :30, Olbramovice :45, with a 4-minute turn at Mladá Vožice.
- **Choice:** Exactly hourly; 4-minute turn at Mladá Vožice (8 of 15 chains). 2 buses.
- **452**, every 60, 2 buses (window 15:30–17:30; waits Mladá Vožice, autobusové stanoviště [4]; Olbramovice, železniční stanice [35])
  - Mladá Vožice, autobusové stanoviště → Olbramovice, železniční stanice: :30, typed 29, 40 min. Step 4: window slots 15:30, 16:30 / real 15:30, 16:30, filled 2/2; day 13 exact / 13 within 3 of 13.
  - Olbramovice, železniční stanice → Mladá Vožice, autobusové stanoviště: :45, typed 44, 41 min. Step 4: window slots 15:45, 16:45 / real 15:45, 16:45, filled 2/2; day 10 exact / 10 within 3 of 12.

### 459 Olbramovice - Tábor
- **Core points:** Tábor, autobusové nádraží | Miličín | Votice, autobusové stanoviště | Olbramovice, železniční stanice. Anchor 14:40.
- **Reading:** Tábor – Chotoviny – Sudoměřice – Mezno – Miličín – Votice – Olbramovice, železniční stanice. Exactly hourly: Tábor :10, Olbramovice :50. The Votice – Miličín shorts (14:18, 14:30) are on its path.
- **Choice:** Exactly hourly; 3 buses. 5 of 11 arrivals at Tábor go on as 453 (noted).
- **459**, every 60, 3 buses (window 14:10–16:10; waits Tábor, autobusové nádraží [27]; Olbramovice, železniční stanice [45])
  - Tábor, autobusové nádraží → Olbramovice, železniční stanice: :10, typed 9, 55 min. Step 4: window slots 14:10, 15:10 / real 14:10, 15:10, filled 2/2; day 11 exact / 11 within 3 of 11.
  - Olbramovice, železniční stanice → Tábor, autobusové nádraží: :50, typed 49, 53 min. Step 4: window slots 14:50, 15:50 / real 14:50, 15:50, filled 2/2; day 8 exact / 8 within 3 of 9.

### 456 Rodná - Mladá Vožice - Miličín
- **Core points:** Miličín | Mladá Vožice, autobusové stanoviště | Rodná. Anchor 16:00.
- **Reading:** Miličín – Neustupov – Šebířov – Mladá Vožice – Rodná. Every 2 hours: Miličín :10 odd hours (11:10–17:10), Rodná :03 even hours (12:03–16:03), exact. The Mladá Vožice – Rodná and Střezimíř shorts are morning or late only.
- **Choice:** Every 120 exact; 6-minute turn at Rodná; 1 bus.
- **456**, every 120, 1 bus (window 15:30–17:30; waits Miličín [19]; Rodná [6])
  - Miličín → Rodná: 13:10 (every 120 from 12:00), typed 9, 47 min. Step 4: window slots 17:10 / real 17:10, filled 1/1; day 4 exact / 4 within 3 of 5.
  - Rodná → Miličín: 12:03 (every 120 from 12:00), typed 62, 48 min. Step 4: window slots 16:03 / real 16:03, filled 1/1; day 3 exact / 3 within 3 of 5.

### 457 Tábor - Chotoviny - Nemyšl - Mezno,Mitrovice
- **Core points:** Tábor, autobusové nádraží | Mezno, Mitrovice. Anchor 16:00.
- **Reading:** Tábor – Chotoviny – Jedlany – Nemyšl – Mezno, Mitrovice, five trips a day each way (Tábor 6:05, 9:40, 12:40, 15:05, 18:20; Mezno 4:39, 6:49, 10:39, 13:39, 15:59), about every 3 hours. Bent onto every 180 at the afternoon round Tábor 15:05 / Mezno 15:59: one bus, the only service of its Jihočeský villages. Off: Tábor 12:40, 18:20; Mezno 13:39.
- **Choice:** Five trips a day each way about every 3 hours; every 180 at the afternoon round (Tábor 15:05 / Mezno 15:59), 1 bus. Every 180 at 12:40 / 13:39 has more exact hits but leaves both window slots empty; every 240 ties on exact hits but is not the line's real headway.
- **457**, every 180, 1 bus (window 15:30–17:30; waits Tábor, autobusové nádraží [87]; Mezno, Mitrovice [14])
  - Tábor, autobusové nádraží → Mezno, Mitrovice: 12:05 (every 180 from 12:00), typed 124, 40 min. Step 4: no slot in the window (real there: none); day 2 exact / 2 within 3 of 5. Off 12–20 h: 12:40, 18:20.
  - Mezno, Mitrovice → Tábor, autobusové nádraží: 12:59 (every 180 from 12:00), typed 178, 39 min. Step 4: window slots 15:59 / real 15:59, filled 1/1; day 1 exact / 1 within 3 of 4. Off 12–20 h: 13:39.

### 532 Votice,Beztahov - Jankov
- **Core points:** Votice, autobusové stanoviště | Votice, železniční stanice | Jankov, Bedřichovice. Anchor 13:50.
- **Reading:** Votice town shuttles (autobusové stanoviště – železniční stanice – Beztahov) and Votice – Neustupov – Jankov, Bedřichovice. The Bedřichovice round of the afternoon is Votice 15:10 → 15:44, Bedřichovice 15:57 → Votice 16:27: every 240, one bus, the only service of Bedřichovice, Čestín, Skrýšov, Broumovice, Vlčkovice and Votice, Amerika. Off: Votice 13:05; Bedřichovice 13:47. Listed: the town shuttles (stops on 550 and 554) and Votice, železniční stanice → Vlčkovice 17:10.
- **Choice:** The Bedřichovice round 15:10 / 15:57 every 240 (every 120 puts a 17:10 slot without a trip in the window), path out via Votice, Amerika (`stops_via`, the 13:05 road) so Amerika is on a line. The town shuttles and the Vlčkovice trips are listed (their stops are on this line, 550 and 554).
- **532**, every 240, 1 bus (window 13:20–15:20; waits Votice, autobusové stanoviště [163]; Jankov, Bedřichovice [13])
  - Votice, autobusové stanoviště → Jankov, Bedřichovice: 15:10 (every 240 from 12:00), typed 129, 34 min [stops_via Votice, Amerika]. Step 4: window slots 15:10 / real 15:10, filled 1/1; day 1 exact / 1 within 3 of 5. Off 12–20 h: 13:05.
  - Jankov, Bedřichovice → Votice, autobusové stanoviště: 15:57 (every 240 from 12:00), typed 176, 30 min. Step 4: no slot in the window (real there: 13:47); day 1 exact / 1 within 3 of 4. Off 12–20 h: 13:47.

### 550 Votice - Vlašim
- **Core points:** Vlašim, Terminál | Zvěstov, Roudný | Votice, autobusové stanoviště | Votice, železniční stanice | Votice, Beztahov. Anchor 16:00.
- **Reading:** Vlašim – Kondrac – Louňovice – Zvěstov – Ratměřice – Jankov – Votice, Beztahov. Hourly: Vlašim :14 (13:14–15:14) then :21 (16:21–18:21), Beztahov :53 (13:53–16:53). Modelled at :21 / :53 (16:00). The trips via Zvěstov, Roudný (14:53, 16:53, 18:28) serve Roudný and Libouň, rozcestí Roudný, stops only 550 serves; the way back runs that road. Off: Vlašim 13:14, 14:14, 15:14; Beztahov 18:28, 19:28.
- **Choice:** Hourly :21 / :53 at 16:00, exact (the :14 out of Vlašim before 15:30 is off). Back via Zvěstov, Roudný (`stops_via`, the 16:53 road; 52 min against 45 direct) for Roudný and Libouň, rozcestí Roudný. 3 buses.
- **550**, every 60, 3 buses (window 15:30–17:30; waits Vlašim, Terminál [36]; Votice, Beztahov [47])
  - Vlašim, Terminál → Votice, Beztahov: :21, typed 20, 45 min [core_to Votice, železniční stanice]. Step 4: window slots 16:21, 17:21 / real 16:21, 17:21, filled 2/2; day 4 exact / 5 within 3 of 10. Off 12–20 h: 13:14, 14:14, 15:14.
  - Votice, Beztahov → Vlašim, Terminál: :53, typed 52, 52 min [stops_via Zvěstov, Roudný]. Step 4: window slots 15:53, 16:53 / real 15:53, 16:53, filled 2/2; day 4 exact / 4 within 3 of 6. Off 12–20 h: 18:28, 19:28.

### 554 Votice,Kaliště - Heřmaničky
- **Core points:** Votice, autobusové stanoviště | Votice, Kaliště | Smilkov. Anchor 16:00.
- **Reading:** Votice – Kaliště and Votice – Smilkov, two hourly shuttles that one timetable chains (Smilkov :15 → Votice :24, wait, Votice :57 → Kaliště). Kaliště :14 back every hour 13:14–17:14; Votice → Kaliště :57 (13:57–15:57, 17:00); Votice → Smilkov :05 (14:05–18:05), Smilkov :15. One Simutrans line per end.
- **Choice:** One timetable chains the two shuttles (Smilkov 14:15 → Votice → Kaliště 15:08 → 15:14 → Votice); as a 4-leg circuit or as two shuttles it needs 2 buses either way, so two plain lines.
- **554**, every 60, 1 bus (window 15:30–17:30; waits Votice, autobusové stanoviště [32]; Votice, Kaliště [6])
  - Votice, autobusové stanoviště → Votice, Kaliště: :57, typed 56, 11 min. Step 4: window slots 15:57, 16:57 / real 15:57, 17:00, filled 2/2; day 3 exact / 6 within 3 of 8.
  - Votice, Kaliště → Votice, autobusové stanoviště: :14, typed 13, 11 min. Step 4: window slots 16:14, 17:14 / real 16:14, 17:14, filled 2/2; day 7 exact / 7 within 3 of 9.
- **554 Smilkov**, every 60, 1 bus (window 15:30–17:30; waits Votice, autobusové stanoviště [41]; Smilkov [1])
  - Votice, autobusové stanoviště → Smilkov: :05, typed 4, 9 min. Step 4: window slots 16:05, 17:05 / real 16:05, 17:05, filled 2/2; day 5 exact / 5 within 3 of 9. Off 12–20 h: 13:10.
  - Smilkov → Votice, autobusové stanoviště: :15, typed 14, 9 min [lay 1]. Step 4: window slots 16:15, 17:15 / real 16:15, 17:15, filled 2/2; day 4 exact / 4 within 3 of 8. Off 12–20 h: 13:38.

### 566 Vojkov - Votice
- **Core points:** Votice, autobusové stanoviště | Vojkov, Sledovice | Vojkov. Anchor 14:10.
- **Reading:** Votice – Olbramovice – Vrchotovy Janovice – Vojkov, school trips: Votice 13:40 and 14:55, Vojkov 14:15 and 15:30, one bus about every 75 minutes (2-minute turns at Vojkov). Every 72 (the 383 rule): both afternoon rounds within 3 minutes. The only service of Vojkov, Sledovice, Minartice and Bezmíř.
- **Choice:** Two rounds about 75 minutes apart (13:40 / 14:15, 14:55 / 15:30). Every 72 holds all four trips within 3 minutes (2 exact); every 120 holds two exactly and drops the second round; the method's 383 example (75-minute spacing → every 72).
- **566**, every 72, 1 bus (window 13:40–15:40; waits Votice, autobusové stanoviště [3]; Vojkov [2])
  - Votice, autobusové stanoviště → Vojkov: 12:28 (every 72 from 12:00), typed 39, 33 min. Step 4: window slots 13:40, 14:52 / real 13:40, 14:55, filled 2/2; day 1 exact / 2 within 3 of 3.
  - Vojkov → Votice, autobusové stanoviště: 13:03 (every 72 from 12:00), typed 2, 34 min [lay 2]. Step 4: window slots 14:15, 15:27 / real 14:15, 15:30, filled 2/2; day 1 exact / 2 within 3 of 3.

### 568 Miličín - Mezno - Miličín
- **Core points:** Miličín | Miličín, Petrovice | Mezno. Anchor 14:30 (set by hand).
- **Reading:** Miličín – Petrovice – Nové Dvory – Mezno – Miličín, a one-way circle (32 min): 11:15, 13:45, 14:45, 15:45. Hourly :45 at its afternoon trips (model hour set by hand to 14:30; the line ends at 16:17). The only service of Mezno and seven Miličín villages.
- **Choice:** Hourly :45 circle, exact 13:45, 14:45, 15:45; the line ends at 16:17, so anchor 14:30 by hand (the 16:00 window holds one trip).
- **568**, every 60, 1 bus (window 14:00–16:00; waits Miličín [28])
  - Miličín → Miličín: :45, typed 44, 32 min. Step 4: window slots 14:45, 15:45 / real 14:45, 15:45, filled 2/2; day 3 exact / 3 within 3 of 6.

### 569 Votice - Střezimíř - Miličín
- **Core points:** Votice, autobusové stanoviště | Miličín | Červený Újezd [BN] | Sedlec-Prčice, náměstí. Anchor 16:00.
- **Reading:** Votice – Miličín – Červený Újezd – Ješetice – Sedlec-Prčice. Miličín :15 odd hours to Sedlec (13:15 from Votice, 15:15, 17:15); Sedlec 13:48, 15:55, 17:45 back. Every 120 from Miličín, exact, with Sedlec 15:55; the Votice – Miličín part is on 459. Off: Sedlec 13:48, 17:45.
- **Choice:** Miličín :15 odd exact (4); Sedlec-Prčice back at no fixed minute (13:48, 15:55, 17:45); :55 is the only phase within 3 of the window's 15:55. 1 bus.
- **569**, every 120, 1 bus (window 15:30–17:30; waits Miličín [51]; Sedlec-Prčice, náměstí [12])
  - Miličín → Sedlec-Prčice, náměstí: 13:15 (every 120 from 12:00), typed 14, 28 min. Step 4: window slots 17:15 / real 17:15, filled 1/1; day 4 exact / 4 within 3 of 5.
  - Sedlec-Prčice, náměstí → Miličín: 13:55 (every 120 from 12:00), typed 54, 29 min. Step 4: window slots 15:55 / real 15:55, filled 1/1; day 1 exact / 1 within 3 of 5. Off 12–20 h: 13:48, 17:45.

### 465 Chocerady - Chocerady,Samechov
- **Core points:** Chocerady | Chocerady, Samechov. Anchor 16:00.
- **Reading:** Chocerady – Vlkovec – Růženín – Samechov, three short rounds a day (7:16, 13:26, 15:16 out, back 13 min later, 1-minute turn). Bent onto every 480 at 7:16 / 15:16 (both exact): one bus, the only service of Samechov, Růženín sídliště and Vlkovec, železniční stanice. Off: 13:26 / 13:39.
- **Choice:** Three rounds a day at no common interval; every 480 keeps two of them exact (7:16, 15:16), as Step 8's 'longest interval that keeps a real trip exact'.
- **465**, every 480, 1 bus (window 15:30–17:30; waits Chocerady [455]; Chocerady, Samechov [1])
  - Chocerady → Chocerady, Samechov: 15:16 (every 480 from 12:00), typed 375, 12 min. Step 4: no slot in the window (real there: none); day 2 exact / 2 within 3 of 3. Off 12–20 h: 13:26.
  - Chocerady, Samechov → Chocerady: 15:29 (every 480 from 12:00), typed 388, 12 min [lay 1]. Step 4: no slot in the window (real there: none); day 2 exact / 2 within 3 of 3. Off 12–20 h: 13:39.

### 483 Ostředek - Chocerady - Vranov,Vranovská Lhota
- **Core points:** Ostředek | Chocerady | Vranov, Vranovská Lhota. Anchor 16:00.
- **Reading:** Ostředek – Vodslivy – Chocerady – Komorní Hrádek – Vranov, Vranovská Lhota. One bus all day: Ostředek :01 every hour to Chocerady, every other one on to Vranovská Lhota (13:06, 15:01); back at Chocerady :48 every hour (from Vranovská Lhota at 13:32, 15:32). In the game every trip runs to Vranovská Lhota (the bus has the time: real 1- and 2-minute turns). Off: Chocerady 12:53, 14:28.
- **Choice:** One bus all day; two lines (Chocerady every 120 + Vranovská Lhota every 120) would need 2. One line every 60 running every trip to Vranovská Lhota, read at Chocerady (`core_to` out, `knot` back), holds every real departure (Ostředek :01, Chocerady :48) with the real 1- and 2-minute turns: 1 bus. The Chocerady shorts end on the line's own path (branch audit: ok).
- **483**, every 60, 1 bus (window 15:30–17:30; waits Ostředek [2]; Vranov, Vranovská Lhota [1])
  - Ostředek → Vranov, Vranovská Lhota: :01, typed 0, 30 min [core_to Chocerady; lay 2]. Step 4: window slots 16:01, 17:01 / real 16:01, 17:01, filled 2/2; day 9 exact / 9 within 3 of 11. Off 12–20 h: 13:06.
  - Vranov, Vranovská Lhota → Ostředek: :32, typed 31, 27 min, read at the knot Chocerady (:48, 16 min from Vranov, Vranovská Lhota) [lay 1]. Step 4: window slots 15:32, 16:32 / real 15:32, 16:32, filled 2/2; day 9 exact / 9 within 3 of 11. Off 12–20 h: 12:37, 14:12.

### 485 Týnec nad Sázavou - Netvořice - Rabyně,Měřín
- **Core points:** Týnec nad Sázavou, železniční stanice | Netvořice, pošta | Rabyně, Nová Rabyně | Rabyně, Měřín. Anchor 16:00.
- **Reading:** Týnec nad Sázavou – Chleby – Netvořice – Rabyně (Nová Rabyně or Měřín), a school line of single trips. Afternoon: Týnec 14:50 → Nová Rabyně 15:32, Nová Rabyně 15:35 → Netvořice; Netvořice 14:20 → Měřín 14:40, Měřín 14:52 → Týnec 15:33. Every 240, one bus: 485 is the only service of Chleby, Netvořice, Maskovice, Nedvězí and Strážovna; its bus returns to Týnec untimed over its own stops. Listed: the Měřín round (Netvořice 14:20 → Měřín, Měřín 14:52 → Týnec; its stops are on 485, 488, 755 Měřín and X390), the Týnec – Chářovice shuttles and Jablonná – Vysoký Újezd 16:36 / 16:50.
- **Choice:** Single school trips. Line 485 every 240 holds the 14:50 → Nová Rabyně and 15:35 → Netvořice trips with an untimed return Netvořice → Týnec over its own stops (Chleby [BN] has no other line); 1 bus. Changed on 2 Nov: 485 Měřín (every 240, Netvořice 14:20 → Měřín → 14:52, 1 bus) existed only for Rabyně, Blaženice; with X390 modelled Blaženice is on X390, and every other stop of that round is on 485, 488 or 755 Měřín, so it is dropped (Step 8) and the round is listed.
- **485**, every 240, 1 bus (window 15:30–17:30; waits Týnec nad Sázavou, železniční stanice [158]; Rabyně, Nová Rabyně [3]; Netvořice, pošta [0])
  - Týnec nad Sázavou, železniční stanice → Rabyně, Nová Rabyně: 14:50 (every 240 from 12:00), typed 109, 42 min. Step 4: no slot in the window (real there: none); day 1 exact / 1 within 3 of 2.
  - Rabyně, Nová Rabyně → Netvořice, pošta: 15:35 (every 240 from 12:00), typed 154, 17 min. Step 4: window slots 15:35 / real 15:35, filled 1/1; day 1 exact / 1 within 3 of 3. Off 12–20 h: 12:25.
  - Netvořice, pošta → Týnec nad Sázavou, železniční stanice: untimed (empty return), 20 min

### X390 Rabyně - Slapy
- **Core points:** Rabyně, Nová Rabyně | Neveklov, Nebřich, Slapská přehrada | Slapy, Motorest. Anchor 16:00.
- **Reading:** X390 Rabyně, Nová Rabyně – Blaženice – Jablonná – Nebřich – Slapská přehrada – Čím – Buš – Slapy, Motorest (ARRIVA): the replacement for line 390's closed section over the Slapy dam, which PID closes from 2 Mar 2026 to 31 Dec 2027, so it is modelled as it runs. One bus all day: Rabyně 12:10, 14:10, 16:10 (every 2 hours at :10) and 17:40; Slapy 13:15, 15:25, 16:55, 18:15 at no fixed minute. Every 120 at Rabyně :10 even hours and Slapy 16:55. Off: Rabyně 17:40; Slapy 13:15, 15:25, 18:15. The Rabyně – Chotilsko morning shorts are listed. It is the only service of Neveklov, Nebřich, Slapská přehrada and of Slapy, Jednota, Buš, Buš, pod Klíčem, Čím and Čím, Hrdlička (okres Praha-západ).
- **Choice:** Changed on 2 Nov: X390 is the replacement for line 390's closed section over the Slapy dam (PID notice 2 Mar 2026 – 31 Dec 2027, in the 29 Sep and 1 Nov feeds), a long closure, so modelled as it runs (the owner's rule for long works). One bus all day (9034, SOR CN 8,5, on the live map). In the window Rabyně has 16:10 and Slapy 16:55; Rabyně :10 every 2 hours (12:10, 14:10, 16:10 exact) and Slapy even :55 are the only phases that pass both ways (Slapy :15 or :25 odd leave the 17:15 / 17:25 window slot empty). 35 + 10 + 33 + 42 = 120: 1 bus.
- **X390**, every 120, 1 bus (window 15:30–17:30; waits Rabyně, Nová Rabyně [42]; Slapy, Motorest [10])
  - Rabyně, Nová Rabyně → Slapy, Motorest: 12:10 (every 120 from 12:00), typed 69, 35 min. Step 4: window slots 16:10 / real 16:10, filled 1/1; day 3 exact / 3 within 3 of 5. Off 12–20 h: 17:40.
  - Slapy, Motorest → Rabyně, Nová Rabyně: 12:55 (every 120 from 12:00), typed 114, 33 min. Step 4: window slots 16:55 / real 16:55, filled 1/1; day 1 exact / 1 within 3 of 5. Off 12–20 h: 13:15, 15:25, 18:15.

### 865 Pacov - Bratřice - Lukavec - Čechtice
- **Core points:** Pacov, železniční stanice | Pacov, Jetřichovská ul.křižovatka | Lukavec | Čechtice. Anchor 15:00.
- **Reading:** Pacov – Bratřice – Mezilesí – Lukavec – Čechtice (Vysočina), and Pacov town shuttles (železniční stanice – Jetřichovská křižovatka). Every 2 hours: Pacov :18 even hours to Čechtice (12:18–16:18), Čechtice :50 even hours (12:50–16:50), exact. The town shuttles' stops are on this line and 406; listed.
- **Choice:** Every 120 exact both ways; the real buses also need two (the 14:18 from Pacov reaches Čechtice after the 14:50 has left).
- **865**, every 120, 2 buses (window 14:30–16:30; waits Pacov, železniční stanice [40]; Čechtice [102])
  - Pacov, železniční stanice → Čechtice: 12:18 (every 120 from 12:00), typed 77, 50 min. Step 4: window slots 16:18 / real 16:18, filled 1/1; day 5 exact / 5 within 3 of 5.
  - Čechtice → Pacov, železniční stanice: 12:50 (every 120 from 12:00), typed 109, 48 min. Step 4: window slots 14:50 / real 14:50, filled 1/1; day 5 exact / 5 within 3 of 5.

### 866 Košetice - Křešín - Čechtice
- **Core points:** Košetice | Chýstovice | Čechtice. Anchor 16:00.
- **Reading:** Košetice – Chýstovice – Křešín – Čechtice (Vysočina). Every 2 hours: Košetice :10 even hours (14:10–18:10), Čechtice :23 odd hours (13:23–17:23; 13:21 and 15:21 start at Čechtice, škola). Exact.
- **Choice:** Every 120 exact; 1 bus.
- **866**, every 120, 1 bus (window 15:30–17:30; waits Košetice [21]; Čechtice [48])
  - Košetice → Čechtice: 12:10 (every 120 from 12:00), typed 69, 25 min. Step 4: window slots 16:10 / real 16:10, filled 1/1; day 3 exact / 3 within 3 of 4.
  - Čechtice → Košetice: 13:23 (every 120 from 12:00), typed 22, 26 min. Step 4: window slots 17:23 / real 17:23, filled 1/1; day 3 exact / 3 within 3 of 5.

### 867 Buřenice - Košetice - Hořice - Ježov
- **Core points:** Ježov | Košetice, Malá strana | Buřenice. Anchor 16:00.
- **Reading:** Ježov – Píšť – Hořice – Studený – Onšov – Košetice – Buřenice (Vysočina). Every 2 hours: Ježov :22 even hours (14:22 to Buřenice, 16:22 to Košetice), back at Košetice :09 odd hours (13:09 and 15:09 from Buřenice, 17:09 starting there). Exact.
- **Choice:** Back first timed at Buřenice :03: the 17:03 window slot had no trip (EMPTY: 17:09 starts at Košetice). Read at the Košetice, Malá strana knot (:09 odd, 5 exact, the 17:09 start is on the line's own path).
- **867**, every 120, 1 bus (window 15:30–17:30; waits Ježov [45]; Buřenice [7])
  - Ježov → Buřenice: 12:22 (every 120 from 12:00), typed 81, 34 min [core_to Košetice, Malá strana]. Step 4: window slots 16:22 / real 16:22, filled 1/1; day 4 exact / 4 within 3 of 4.
  - Buřenice → Ježov: 13:03 (every 120 from 12:00), typed 2, 34 min, read at the knot Košetice, Malá strana (13:09, 6 min from Buřenice). Step 4: window slots 17:03 / real 17:03, filled 1/1; day 5 exact / 5 within 3 of 5.

### MHD Benešov 1 MHD Benešov ORANŽOVÁ Albert - Nezvalova - Terminál - U Náhonu
- **Core points:** Benešov, U Náhonu | Benešov, Terminál | Benešov, Nemocnice Rudolfa a Stefanie | Benešov, Albert. Anchor 16:00.
- **Reading:** MHD Benešov 1 (orange): U Náhonu – Terminál – Nemocnice – Čerčanská – Albert. Hourly: U Náhonu :30, Albert :06, 1-minute turn at U Náhonu. In the afternoon the Albert end loops: out via Neumannova, K Tužince, Čerčanská, Nezvalova and Tylova, back direct via Tyršova (the morning trips run both ways round). The Terminál – U Náhonu shorts end at 12:49.
- **Choice:** Hourly exact; 1-minute turn at U Náhonu (16 of 24). The builder takes the afternoon paths (out via Čerčanská and Nezvalova, back direct), named on the card.
- **MHD Benešov 1**, every 60, 1 bus (window 15:30–17:30; waits Benešov, U Náhonu [1]; Benešov, Albert [7])
  - Benešov, U Náhonu → Benešov, Albert: :30, typed 29, 29 min [lay 1]. Step 4: window slots 15:30, 16:30 / real 15:30, 16:30, filled 2/2; day 16 exact / 16 within 3 of 17.
  - Benešov, Albert → Benešov, U Náhonu: :06, typed 5, 23 min. Step 4: window slots 16:06, 17:06 / real 16:06, 17:06, filled 2/2; day 10 exact / 10 within 3 of 18.

### MHD Benešov 2 MHD Benešov ZELENÁ MŠ Úsměv - Terminál - Černoleská - Mariánovice
- **Core points:** Benešov, MŠ Úsměv | Benešov, Terminál | Benešov, Mariánovice. Anchor 16:00.
- **Reading:** MHD Benešov 2 (green): MŠ Úsměv – Terminál every 20 minutes (MŠ Úsměv :10 / :30 / :50), the :30 running on to Mariánovice, back from Mariánovice :06 and from Terminál :00 / :40, each bus leaving MŠ Úsměv a minute after it arrives (45 of 52). Two lines: the Terminál shorts and 2 Mariánovice.
- **Choice:** Every 20 at MŠ Úsměv as two lines (shorts :10/:50, Mariánovice :30), with the real 1-minute turns at MŠ Úsměv (45 of 52): 1 + 1 buses.
- **MHD Benešov 2**, every 60, 1 bus (window 15:30–17:30; waits Benešov, MŠ Úsměv [1, 1]; Benešov, Terminál [21, 1])
  - Benešov, MŠ Úsměv → Benešov, Terminál: :10, :50, typed 9, 49, 9 min [notvia Benešov, Mariánovice; lay 1]. Step 4: window slots 15:50, 16:10, 16:50, 17:10 / real 15:50, 16:10, 16:50, 17:10, filled 4/4; day 30 exact / 30 within 3 of 31.
  - Benešov, Terminál → Benešov, MŠ Úsměv: :00, :40, typed 39, 59, 9 min [notvia Benešov, Mariánovice; lay 1]. Step 4: window slots 15:40, 16:00, 16:40, 17:00 / real 15:40, 16:00, 16:40, 17:00, filled 4/4; day 28 exact / 28 within 3 of 29.
- **MHD Benešov 2 Mariánovice**, every 60, 1 bus (window 15:30–17:30; waits Benešov, MŠ Úsměv [1]; Benešov, Mariánovice [14])
  - Benešov, MŠ Úsměv → Benešov, Mariánovice: :30, typed 29, 22 min [lay 1]. Step 4: window slots 15:30, 16:30 / real 15:30, 16:30, filled 2/2; day 18 exact / 18 within 3 of 18.
  - Benešov, Mariánovice → Benešov, MŠ Úsměv: :06, typed 5, 23 min. Step 4: window slots 16:06, 17:06 / real 16:06, 17:06, filled 2/2; day 18 exact / 18 within 3 of 20.

### MHD Benešov 3 MHD Benešov MODRÁ Buková Lhota - Pomněnice - Purkyňova - Terminál - Masarykovo náměstí
- **Core points:** Benešov, Terminál | Benešov, Buková Lhota | Benešov, Vidlákova Lhota. Anchor 15:00 (set by hand).
- **Reading:** MHD Benešov 3 (blue): Terminál – Purkyňova – Pomněnice – Žabovřesky – Zbožnice – Buková Lhota – Vidlákova Lhota. Hourly: Terminál :40, Vidlákova Lhota :01 until 16:01 (the bus leaves on arrival), :06 from 17:06. Model hour set by hand to 15:00, where the :01 pattern runs; 17:06–22:06 are 5 min off.
- **Choice:** Vidlákova Lhota :01 until 16:01, :06 from 17:06: at 16:00 neither passes (16:01 / 17:06). Anchor 15:00 by hand; the bus leaves Vidlákova Lhota on arrival (11 of 11), `lay` 0, 1 bus.
- **MHD Benešov 3**, every 60, 1 bus (window 14:30–16:30; waits Benešov, Terminál [21]; Benešov, Vidlákova Lhota [0])
  - Benešov, Terminál → Benešov, Vidlákova Lhota: :40, typed 39, 21 min. Step 4: window slots 14:40, 15:40 / real 14:40, 15:40, filled 2/2; day 11 exact / 11 within 3 of 11.
  - Benešov, Vidlákova Lhota → Benešov, Terminál: :01, typed 0, 18 min [lay 0]. Step 4: window slots 15:01, 16:01 / real 15:01, 16:01, filled 2/2; day 9 exact / 9 within 3 of 16. Off 12–20 h: 17:06, 18:06, 19:06.

### MHD Benešov 6 MHD Benešov ČERVENÁ Terminál - Konopiště, Růžová zahrada
- **Core points:** Benešov, Terminál | Benešov, Konopiště, informační centrum. Anchor 16:00.
- **Reading:** MHD Benešov 6 (red): Terminál – Konopiště, informační centrum, every 2 hours all day (Terminál :21 even hours, Konopiště :33). The only service of Konopiště, informační centrum.
- **Choice:** Every 120 exact all day; 1 bus.
- **MHD Benešov 6**, every 120, 1 bus (window 15:30–17:30; waits Benešov, Terminál [103]; Benešov, Konopiště, informační centrum [6])
  - Benešov, Terminál → Benešov, Konopiště, informační centrum: 12:21 (every 120 from 12:00), typed 80, 6 min. Step 4: window slots 16:21 / real 16:21, filled 1/1; day 6 exact / 6 within 3 of 6.
  - Benešov, Konopiště, informační centrum → Benešov, Terminál: 12:33 (every 120 from 12:00), typed 92, 5 min. Step 4: window slots 16:33 / real 16:33, filled 1/1; day 6 exact / 6 within 3 of 6.

## Not modelled
- **205004**: No afternoon trips: MHD Benešov 4 (pink) runs MŠ Úsměv – Terminál – U Náhonu hourly 4:50–13:09 only, interlined with lines 1 and 2 (6 of 6 arrivals at U Náhonu go on as 1, 6 of 6 at MŠ Úsměv as 2). Every stop is on MHD Benešov 1 and 2 (Step 8).
- **205005**: Sparse town shuttle: MHD Benešov 5 (yellow) runs Terminál – Křižíkova and back three times in the afternoon (13:21, 14:21, 16:21; 5 min each way). Every stop (Konopišťská, Jana Nohy, Benea, Křižíkova) is on 408, 553, 564 and 759 (Step 8).
- **851**: School trips only, ending 15:51: Čechtice, škola → Loket, u dálnice 13:28, 15:28 and Čechtice → Pravonín → Jeníkov 13:35, 15:25, all one-way. Every stop it serves 13–19 is on modelled lines: Čechtice, Křivsoudov and Loket on 401 and 842; Otročice, rozcestí, Borovnice, rozcestí, Kuňovice, Miřetice, Chmelná, Pravonín, Dobříkovice, Nakvasovice and Jeníkov on 842, 843 and 849 (Step 8).
- **886** (Bystřicko), **887** (Načeradecko): PID Haló, on demand (filled in automatically).

## Coverage (Step 9)
- 994 stops served 13:00–19:00 by this sheet's lines; 994 are on a modelled Simutrans line here. Uncovered of okres Benešov: none (no coverage exception): Neveklov, Nebřich, Slapská přehrada is on X390 and Načeradec, Novotinky and Horní Lhota, u váhy (Haló 887 only) are on 848 Zdiměřice's untimed loop since 2 Nov. None outside the Středočeský kraj: every Jihočeský and Vysočina stop of 401, 406, 408, 453, 455, 456, 457, 459, 846, 865, 866, 867 is on a line.
- First run's uncovered stops and their fixes: Rabyně, Blaženice → 485 Měřín (now X390); Strnadice, Šebáňovice, rozcestí, Sedlečko, rozcestí, Hodětice → 759 Strážovice; Maršovice, Zderadice, Bystřice, Jírovice, Jírovice, Kukačka → 759's way back via Jírovice; eight Načeradec stops → 848 Zdiměřice (kept by the owner's decision of 2 Nov, which also put Novotinky and Horní Lhota, u váhy on its round).
- Uncovered of another Středočeský okres: none. The Praha-západ stops Slapy, Jednota; Buš; Buš, pod Klíčem; Čím; Čím, Hrdlička (served only by X390) are on X390 since 2 Nov.
- Stops of other Středočeský okresy that only this sheet's lines serve (no trip of any other oblast's lines stops there 13–19): Kutná Hora: Zruč nad Sázavou, Nesměřice (795). Praha-východ: Kamenice, Valnovka / Ládví / Kuklík (337, 339); Vyžlovka, hotel Praha; Jevany, Spojovací; Konojedy, rozcestí; Stříbrná Skalice, Hradec / Propast / Hruškov / Vozlín; Vlkančice, Pyskočely, Plužiny (382); Ondřejov, Třemblat, rozcestí Mnichovice / rozcestí Zvánovice; Ondřejov, U Pily; Ondřejov, hřbitov (383); Senohraby, odbočka / U Zvoničky / u školy / železniční stanice; Pětihosty (651). Praha-západ: Psáry, Domov Laguna (332); Jílové u Prahy, Borek; Kamenný Přívoz (4 stops, 332 Neveklov and 752); Kamenný Přívoz, Kašparka / pošta / Hostěradice / Hostěradice, dom.důch. (753); Slapy, Jednota, Buš, Buš, pod Klíčem, Čím, Čím, Hrdlička (X390). Příbram: Sedlec-Prčice, rozcestí Mrákotice / u Milotů / Sušetice / Sušetice, U Šiků / Veletín / Veletín, rozcestí (408); Sedlec-Prčice, Záběhlice / Dvorce / Staré Mitrovice / rozcestí Rohov (569). All are on modelled lines here.

## Shared terminals, through-running and bunching
- **Step 5b.** Every Simutrans line is balanced on its own; no surplus at Benešov, Vlašim or Votice needed pairing across lines once the outstation lines (339, 382, 755) are at their inbound rate. Cross-line chains seen in the readings: 337 → 651 and 651 → 337 at Nespeky (4 of 4, 6 of 6: one bus, see 337/651); 408 → 453 (9 of 16) and 459 → 453 (5 of 11) at Tábor; 335 → 339 at Sulice, Želivec (7 of 7); 205004 → 205001 / 205002 (6 of 6). The 100 % chains into 426 at Vlašim (790 8 of 8, 455 7 of 7) and into MHD Benešov 2 / 3 at Benešov (798 7 of 10, 752 13 of 25) are the timed pulses (:50 at Vlašim, :40 at Benešov), not proof of one bus; the live map decides. No cross-line circuit was built: none of them would save a bus over the lines as modelled.
- **Bunching scan** (scratch `bunch.py`: game departures 14–18 h at Benešov, Vlašim, Votice, Neveklov, Čechtice, Týnec, Mladá Vožice, Tábor, Roztyly, flagging two lines leaving within 2 min onto the same next stop where one of them is not a real departure): only pattern repeats next to real departures — Benešov 14:04 / 14:05 (759 real, 488's even-hour repeat), 14:20 / 14:21 (755 repeat, MHD 6 real), 17:04 / 17:05 (759 and 755 Měřín repeats); Vlašim :50 (799's hourly repeat at 15:50–17:50 beside 426; in reality they leave together at 13:50 and 14:50), 16:50 (848 repeat beside 849), 17:05 / 17:06 (790 repeat beside 426 Benešov); Votice 16:55 / 16:57 and 17:55 / 17:57 (452 real, 554 repeat). Each pair shares one or two stops before the roads part; the same pairs leave together in the real timetable at the hours they really run. Nothing was moved off a real minute.

## Script notes
- `run_oblast.py` had a syntax error (an f-string broken across two lines at line 40) from about 05:20 on 2 Nov; the coordinator fixed it. The first runs here used `00_config.py`, `03_read.py`, `03b_draft.py` and `05_schedule.py` directly; every result in this check is from the fixed script.
- The trip rows of the reading files shorten stop names ("Týnec nad Sázavou, žst", "Votice, AS"); the legs and the card text use the full names from "core (full names)" and `trips.json`.
- `step4_regional.py` reports the three outstation rows as FEWER/FIXABLE ("every 30 :20"); its search ignores the other direction, so the FIXABLE rows there are the busier pattern the outstation rule rejects, not a missed fit.

## Open questions
- **Owner checks:** none open. The 848 Zdiměřice question was answered on 2 Nov 2026: "Yes, model a line" (places whose only afternoon service is PID Haló get a Simutrans line from their fixed trips, at most every 480).
- **Engine:** the 0-minute turns (`lay` 0 on 426, 406, 453, 794, 840, 841, MHD Benešov 3, 848 Zdiměřice) assume the automatic Leave up to lets a bus that arrives on the real minute leave although the loop rule typed it 1 min early, as on the Rakovnicko sheet; to confirm with an engine session.
- **Live map (2 Nov):** the pairings listed above; whether 339's 15:50 / 16:50 and 382's :50 Prague departures and 755's extra Benešov departures really end at the far end (the outstation reading); whether the 791 buses alternate between the two ends at Benešov (pooling option).
- **X390** is modelled since 2 Nov (the dam closure runs to 31 Dec 2027); when line 390 returns over the dam, X390 goes and 390 belongs to its own oblast.
