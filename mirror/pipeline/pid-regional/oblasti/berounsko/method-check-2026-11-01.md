# Method check: PID Berounsko (okres Beroun, prefix 210), 1 Nov 2026

Designed line by line with `../../DESIGN_BRIEF.md` (including "Learned on the pilot") and the bus schedule method v4
(`../../../bus-schedule-method.md`), checked against the owner's corrections in `kb/lessons.md` and the pilot review
(`../rakovnicko/review-2026-11-01.md`). The design is `lines.json` here; `python -X utf8 pid-regional/scripts/run_oblast.py
berounsko` rebuilds `data/derived/schedule.json` and the three audits.

- **Data:** PID GTFS of 1 Nov 2026, service day Mon 2 Nov 2026 (school day): `data/derived/trips.json` and the whole-day reading
  `data/derived/reading/<L>.txt` (every trip at its core points, the paths, the 0-minute chain test). The live map of 2 Nov
  had only morning buses when this was designed, so no plate chains were used; where a choice depends on them it says so.
- **Step 4**, per leg: in the Simutrans line's window (anchor −30 … +90, or a `window` set by hand where stated) the slots
  equal the real departures ±1 and ≥ 80 % of the slots have a real departure within 3 min; then most exact over the day,
  then the simplest; an hourly row is not halved by a passing every 120 (Opavsko rule 5); on one-departure-per-window lines
  the real 13–18 h headway decides.
- **Typed values** are (real − 61) mod every (every terminus is a loop); the builder writes them, and the real time of every
  typed value is in the table below. Checked by hand on one leg per line, e.g. 380 Kukulova :12 → (732 − 61) mod 30 = 11,
  547 Hořovice 14:40 → (880 − 61) mod 480 = 339, 861 14:04 → (844 − 61) mod 48 = 15.
- **Result (after the 2 Nov review):** 29 lines → 28 modelled as **40 Simutrans lines, 65 buses**; 952 (night line) listed
  automatically. `run_oblast.py` runs clean. Step 4 audit: **85 timed legs, 85 ok**. Branch audit: 19 legs read at a
  midpoint, 14 `[ok]`, 5 flags explained below. Path audit: 6 slots, all explained below. Coverage: 413 afternoon stops,
  397 on this sheet's lines; the 8 okres-210 stops left out each have a reason (`coverage_exceptions`: 7 on a neighbouring
  sheet's modelled line or the near-stop owner check); 0 uncovered outside the kraj.
- **First version (1 Nov):** 38 Simutrans lines, 66 buses, 81 legs; the changes are listed in "Changed on 2 Nov" below.

## Summary

| Line | Simutrans lines (every) | Slots, real minutes (out / back) | Buses |
|---|---|---|---|
| 380 | 380 (30) | Kukulova :12 :42 / Počaply, Obchodní centrum :02 :32 | 6 |
| 384 | 384 (60), 384 Hořovice (60) | Zličín :50 / Zdice :48; Zličín :20 / Hořovice :52 (Zdice :18) | 2 + 3 |
| 394 | 394 (30) | Nové Butovice :00 :30 / Zdice :03 :33 | 4 |
| 526 | 526 (120, circuit) | Zdice 14:30 → Žebrák 14:56 → Zdice 15:10 → Bzová 15:42 → Zdice 16:15 → Knížkovice 16:20 | 1 |
| 527 | 527 (120) | Žebrák 15:23 / Komárov, Buzuluk 15:59 | 1 |
| 528 | 528 (60) | Hořovice :15 / Broumy :02 | 2 |
| 529 | 529 (120) | Hořovice 17:00 / Hvozdec 17:07 | 1 |
| 531 | 531 (60) | Hořovice, železniční stanice :57 / Příbram, autobusové nádraží :57 | 3 |
| 544 | 544 (60), 544 Hořovice (240) | Zaječov :08 / Komárov :34; Hořovice 13:52 → Mrtník 14:09 → Hořovice 14:52 → Zaječov (untimed back) | 1 + 1 |
| 545 | 545 Strašice (120), 545 Zaječov (120) | Hořovice 15:40 / Strašice 16:45; Hořovice 16:35 / Zaječov 18:00 | 1 + 1 |
| 546 | 546 (60) | Hořovice :09 / Rokycany :40 | 3 |
| 547 | 547 (480) | Hořovice 14:40 / Cerhovice 15:15 (= 7:15) | 1 |
| 548 | 548 (120), 548 Praskolesy (120) | nemocnice 16:07 / Zbiroh 16:55; Praskolesy 15:00 (nemocnice 15:07) / Zbiroh 15:55 | 1 + 1 |
| 631 | 631 (60, circuit) | Šnárová :32 (Beroun :00) → Všeradice :57 → Beroun :02 | 3 |
| 633 | 633 (120), 633 Tetín (120) | Zdejcina 16:16 / Liteň 17:19; Zdejcina 15:28 / Tetín 16:29 | 1 + 1 |
| 634 | 634 (60) | Hostomice :25 / Všeradice, železniční zastávka :41 | 1 |
| 636 | 636 (60) | Loděnice :45 / Železná :22 | 1 |
| 637 | 637 (60), 637 Řevnice (120) | Beroun :00 / Kublov :08; Beroun 14:05 / Řevnice 15:14 | 2 + 1 |
| 638 | 638 (180), 638 Branov (180), 638 Skryje (180), 638 Liteň (120) | Beroun 14:30 / Broumy 15:53; Beroun 13:30 / Branov 14:24; Beroun 15:25 / Skryje 16:26; Beroun 17:01 / Liteň 17:34 | 1 + 1 + 1 + 1 |
| 639 | 639 Dobříš (120), 639 Hostomice (120), 639 Lštěň (480) | Hořovice 15:00 / Dobříš 14:55 (Hostomice 15:25); Hořovice 14:00 / Hostomice 14:35; Hostomice 13:10 / Lštěň 13:14 | 2 + 1 + 1 |
| 640 | 640 (60) | Zdice :30 / Jince :31 | 2 |
| 641 | 641 (60) | Beroun :09 (Zdice :28) / Hořovice, nemocnice :20 | 3 |
| 642 | 642 (240) | Hořovice 15:38 → Jince (untimed to Lochovice) → Lochovice 17:38 (= 13:38) | 1 |
| 643 | 643 (120) | Podluhy 16:40 (Hořovice :50) / Třenice 17:14 | 1 |
| 649 | 649 (60) | Nižbor, u lípy :51 / Žloukovice :02 | 1 |
| 825 | 825 (120, 3 slots), 825 Mořina (120) | Popovice 15:10 15:40 16:10 / nemocnice 15:40 16:10 16:40 (Prof.Veselého +1); Popovice 16:39 / Mořina 16:28 | 2 + 2 |
| 861 | 861 (48, loop) | Beroun, autobusové nádraží 14:04 (13:16, 14:52) | 1 |
| X384 (210384) | X384 (30) | Králův Dvůr, škola :00 :30 / Levín :08 :38 | 1 |
| 952 | not modelled (night line, automatic) | – | 0 |
| **Total** | **40 Simutrans lines** | | **65** |

Bus counts are the builder's need from each pattern (Step 10), one Simutrans line at a time. Arriva Střední Čechy runs every
line and its buses swap lines at Beroun, Hořovice and Zdice (chains in the notes), so the totals are higher than the
operator's own; pooling is an owner option, not applied.

## Step 4 per leg (from `schedule.json`)

Slots in real minutes (for intervals over 60: their 13–19 h repeats), typed values in brackets; window slots against the
real departures in the window; filled = window slots with a real departure within 3 min; exact / within 3 / trips over the day
(5–23 h, the leg's own trips).

| Simutrans line | Leg | Slots, real (typed) | Window slots | Real in window | Filled | Day exact / within 3 / trips |
|---|---|---|---|---|---|---|
| 380 | Praha, Kukulova → Králův Dvůr, Počaply, Obchodní centrum | :12 :42 (11) | 15:42 16:12 16:42 17:12 | 15:42 16:12 16:42 17:12 | 4/4 | 22/24/29 |
| 380 | Králův Dvůr, Počaply, Obchodní centrum → Praha, Kukulova | :02 :32 (1) | 15:32 16:02 16:32 17:02 | 15:32 16:02 16:32 17:02 | 4/4 | 9/10/21 |
| 384 | Praha, Zličín → Zdice, náměstí | :50 (49) | 15:50 16:50 | 15:50 16:50 | 2/2 | 9/9/14 |
| 384 | Zdice, náměstí → Praha, Zličín | :48 (47) | 15:48 16:48 | 15:48 16:48 | 2/2 | 5/5/14 |
| 384 Hořovice | Praha, Zličín → Hořovice, náměstí B.Němcové | :20 (19) | 16:20 17:20 | 16:20 17:20 | 2/2 | 9/9/13 |
| 384 Hořovice | Hořovice, náměstí B.Němcové → Praha, Zličín (knot Zdice, náměstí) | :52 (51) | 15:52 16:52 | 15:52 16:52 | 2/2 | 6/7/12 |
| 394 | Praha, Nové Butovice → Zdice, náměstí | :00 :30 (29) | 15:30 16:00 16:30 17:00 | 15:30 16:00 16:30 17:00 17:20 | 4/4 | 8/8/27 |
| 394 | Zdice, náměstí → Praha, Nové Butovice | :03 :33 (2) | 15:33 16:03 16:33 17:03 | 15:33 16:03 16:33 17:03 | 4/4 | 7/15/33 |
| 526 | Zdice, náměstí → Žebrák, náměstí | 14:30, 16:30, 18:30 (89) | 14:30 | 14:30 | 1/1 | 2/2/5 |
| 526 | Žebrák, náměstí → Zdice, náměstí | 14:56, 16:56, 18:56 (115) | 14:56 | 14:56 | 1/1 | 1/1/4 |
| 526 | Zdice, náměstí → Bzová | 13:10, 15:10, 17:10 (9) | 15:10 | 15:10 | 1/1 | 1/1/3 |
| 526 | Bzová → Zdice, náměstí | 13:42, 15:42, 17:42 (41) | 15:42 | 15:42 | 1/1 | 1/1/3 |
| 526 | Zdice, náměstí → Zdice, Knížkovice | 14:15, 16:15, 18:15 (74) | 16:15 | 16:15 | 1/1 | 1/1/7 |
| 526 | Zdice, Knížkovice → Zdice, náměstí | 14:20, 16:20, 18:20 (79) | 16:20 | 16:20 | 1/1 | 2/2/7 |
| 527 | Žebrák, náměstí → Komárov, Buzuluk | 13:23, 15:23, 17:23 (22) | 15:23 | 15:23 | 1/1 | 1/1/2 |
| 527 | Komárov, Buzuluk → Žebrák, náměstí | 13:59, 15:59, 17:59 (58) | 15:59 | 15:59 | 1/1 | 1/1/3 |
| 528 | Hořovice, náměstí B.Němcové → Broumy, radnice | :15 (14) | 16:15 17:15 | 16:15 17:15 | 2/2 | 8/8/10 |
| 528 | Broumy, radnice → Hořovice, náměstí B.Němcové | :02 (1) | 16:02 17:02 | 16:02 17:02 | 2/2 | 7/7/8 |
| 529 | Hořovice, náměstí B.Němcové → Hvozdec | 13:00, 15:00, 17:00 (119) | 17:00 | 17:00 | 1/1 | 1/1/7 |
| 529 | Hvozdec → Hořovice, náměstí B.Němcové | 13:07, 15:07, 17:07 (6) | 17:07 | 17:07 | 1/1 | 1/1/8 |
| 531 | Hořovice, železniční stanice → Příbram, autobusové nádraží | :57 (56) | 15:57 16:57 | 15:57 16:57 | 2/2 | 9/9/13 |
| 531 | Příbram, autobusové nádraží → Hořovice, železniční stanice | :57 (56) | 15:57 16:57 | 15:57 16:57 | 2/2 | 11/11/14 |
| 544 | Zaječov → Komárov | :08 (7) | 16:08 17:08 | 16:08 17:08 | 2/2 | 2/2/5 |
| 544 | Komárov → Zaječov | :34 (33) | 16:34 17:34 | 16:34 17:34 | 2/2 | 3/3/4 |
| 544 Hořovice | Hořovice, náměstí B.Němcové → Hvozdec, Mrtník | 13:52, 17:52 (51) | 13:52 | 13:52 | 1/1 | 1/1/1 |
| 544 Hořovice | Hvozdec, Mrtník → Hořovice, náměstí B.Němcové | 14:09, 18:09 (68) | 14:09 | 14:09 | 1/1 | 1/1/2 |
| 544 Hořovice | Hořovice, náměstí B.Němcové → Zaječov | 14:52, 18:52 (111) | 14:52 | 14:52 | 1/1 | 1/1/1 |
| 544 Hořovice | Zaječov → Hořovice, náměstí B.Němcové | untimed | | | | |
| 545 Strašice | Hořovice, náměstí B.Němcové → Strašice, ObÚ | 13:40, 15:40, 17:40 (39) | 15:40 | 15:40 | 1/1 | 2/2/3 |
| 545 Strašice | Strašice, ObÚ → Hořovice, náměstí B.Němcové | 14:45, 16:45, 18:45 (104) | 16:45 | 15:45 16:45 | 1/1 | 1/1/2 |
| 545 Zaječov | Hořovice, náměstí B.Němcové → Zaječov | 14:35, 16:35, 18:35 (94) | 16:35 | 16:35 | 1/1 | 4/4/10 |
| 545 Zaječov | Zaječov → Hořovice, náměstí B.Němcové | 14:00, 16:00, 18:00 (59) | 18:00 | 18:00 | 1/1 | 2/2/9 |
| 546 | Hořovice, náměstí B.Němcové → Rokycany, autobusové nádraží | :09 (8) | 16:09 17:09 | 16:09 17:09 | 2/2 | 9/9/9 |
| 546 | Rokycany, autobusové nádraží → Hořovice, náměstí B.Němcové | :40 (39) | 15:40 16:40 | 15:40 16:40 | 2/2 | 5/5/9 |
| 547 | Hořovice, náměstí B.Němcové → Cerhovice, náměstí | 14:40 (339) | – | – | 0/0 | 1/1/1 |
| 547 | Cerhovice, náměstí → Hořovice, náměstí B.Němcové | 15:15 (374) | – | – | 0/0 | 1/1/1 |
| 548 | Hořovice, nemocnice → Zbiroh, náměstí | 14:07, 16:07, 18:07 (66) | 16:07 | 16:07 | 1/1 | 3/3/5 |
| 548 | Zbiroh, náměstí → Hořovice, nemocnice | 14:55, 16:55, 18:55 (114) | 16:55 | 16:55 | 1/1 | 3/3/6 |
| 548 Praskolesy | Praskolesy → Zbiroh, náměstí (knot Hořovice, nemocnice) | 13:00, 15:00, 17:00 (119) | 15:00 | 15:00 | 1/1 | 4/4/5 |
| 548 Praskolesy | Zbiroh, náměstí → Praskolesy | 13:55, 15:55, 17:55 (54) | 15:55 | 15:55 | 1/1 | 2/2/4 |
| 631 | Nižbor, Šnárová → Všeradice (knot Beroun, autobusové nádraží) | :32 (31) | 14:32 15:32 | 14:32 15:32 | 2/2 | 4/9/10 |
| 631 | Všeradice → Beroun, autobusové nádraží | :57 (56) | 14:57 15:57 | 14:57 15:57 | 2/2 | 2/2/11 |
| 631 | Beroun, autobusové nádraží → Nižbor, Šnárová | :02 (1) | 15:02 16:02 | 15:02 16:02 | 2/2 | 6/14/18 |
| 633 | Beroun, Zdejcina → Liteň, náměstí | 14:16, 16:16, 18:16 (75) | 16:16 | 16:16 | 1/1 | 1/1/4 |
| 633 | Liteň, náměstí → Beroun, Zdejcina | 13:19, 15:19, 17:19 (18) | 17:19 | 15:20 17:19 | 1/1 | 1/2/4 |
| 633 Tetín | Beroun, Zdejcina → Tetín, křižovatka | 13:28, 15:28, 17:28 (27) | 15:28 | 15:28 17:03 | 1/1 | 1/1/6 |
| 633 Tetín | Tetín, křižovatka → Beroun, Zdejcina | 14:29, 16:29, 18:29 (88) | 16:29 | 16:29 | 1/1 | 1/3/7 |
| 634 | Hostomice, náměstí → Všeradice, železniční zastávka | :25 (24) | 16:25 17:25 | 16:25 17:25 | 2/2 | 3/3/7 |
| 634 | Všeradice, železniční zastávka → Hostomice, náměstí | :41 (40) | 16:41 17:41 | 16:41 17:41 | 2/2 | 4/5/7 |
| 636 | Loděnice → Železná | :45 (44) | 14:45 15:45 | 14:45 15:45 | 2/2 | 4/4/9 |
| 636 | Železná → Loděnice | :22 (21) | 14:22 15:22 | 14:22 15:22 | 2/2 | 5/5/8 |
| 637 | Beroun, autobusové nádraží → Kublov, Slovanka | :00 (59) | 14:00 15:00 | 14:00 15:00 | 2/2 | 11/11/16 |
| 637 | Kublov, Slovanka → Beroun, autobusové nádraží | :08 (7) | 14:08 15:08 | 14:08 15:08 | 2/2 | 5/5/5 |
| 637 Řevnice | Beroun, autobusové nádraží → Řevnice, nádraží | 14:05, 16:05, 18:05 (64) | 14:05 | 14:05 | 1/1 | 1/2/9 |
| 637 Řevnice | Řevnice, nádraží → Beroun, autobusové nádraží | 13:14, 15:14, 17:14 (13) | 15:14 | 15:14 | 1/1 | 1/1/3 |
| 638 | Beroun, autobusové nádraží → Broumy, radnice | 14:30, 17:30 (89) | 17:30 | 17:30 | 1/1 | 2/2/4 |
| 638 | Broumy, radnice → Beroun, autobusové nádraží | 15:53, 18:53 (172) | 15:53 | 15:53 | 1/1 | 1/1/3 |
| 638 Branov | Beroun, autobusové nádraží → Branov | 13:30, 16:30 (29) | 13:30 | 13:30 | 1/1 | 2/2/3 |
| 638 Branov | Branov → Beroun, autobusové nádraží | 14:24, 17:24 (83) | 14:24 | 14:24 | 1/1 | 1/1/2 |
| 638 Skryje | Beroun, autobusové nádraží → Skryje | 15:25, 18:25 (144) | 15:25 | 15:25 | 1/1 | 1/1/3 |
| 638 Skryje | Skryje → Beroun, autobusové nádraží | 13:26, 16:26 (25) | 16:26 | 16:26 | 1/1 | 1/1/3 |
| 638 Liteň | Beroun, autobusové nádraží → Liteň, náměstí | 13:01, 15:01, 17:01 (0) | 17:01 | 17:01 | 1/1 | 1/1/4 |
| 638 Liteň | Liteň, náměstí → Beroun, autobusové nádraží | 13:34, 15:34, 17:34 (33) | 17:34 | 15:42 17:34 | 1/1 | 1/1/4 |
| 639 Dobříš | Hořovice, náměstí B.Němcové → Dobříš, náměstí | 13:00, 15:00, 17:00 (119) | 15:00 | 15:00 | 1/1 | 4/4/5 |
| 639 Dobříš | Dobříš, náměstí → Hořovice, náměstí B.Němcové (knot Hostomice, náměstí) | 14:55, 16:55, 18:55 (114) | 14:55 | 14:55 | 1/1 | 3/3/6 |
| 639 Hostomice | Hořovice, náměstí B.Němcové → Hostomice, náměstí | 14:00, 16:00, 18:00 (59) | 14:00 | 14:00 | 1/1 | 4/4/6 |
| 639 Hostomice | Hostomice, náměstí → Hořovice, náměstí B.Němcové | 14:35, 16:35, 18:35 (94) | 14:35 | 14:35 | 1/1 | 1/1/7 |
| 639 Lštěň | Hostomice, náměstí → Hostomice, Lštěň | 13:10 (249) | 13:10 | 13:10 | 1/1 | 1/1/1 |
| 639 Lštěň | Hostomice, Lštěň → Hostomice, náměstí | 13:14 (253) | 13:14 | 13:14 | 1/1 | 1/1/2 |
| 640 | Zdice, náměstí → Jince, sokolovna | :30 (29) | 15:30 16:30 | 15:30 16:30 | 2/2 | 4/4/8 |
| 640 | Jince, sokolovna → Zdice, náměstí | :31 (30) | 15:31 16:31 | 15:31 16:31 | 2/2 | 7/7/10 |
| 641 | Beroun, autobusové nádraží → Hořovice, nemocnice (knot Zdice, náměstí) | :09 (8) | 14:09 15:09 | 14:11 15:07 | 2/2 | 1/6/11 |
| 641 | Hořovice, nemocnice → Beroun, autobusové nádraží | :20 (19) | 14:20 15:20 | 14:20 15:20 | 2/2 | 3/3/9 |
| 642 | Hořovice, náměstí B.Němcové → Jince, náměstí | 15:38 (157) | 15:38 | 15:38 | 1/1 | 1/1/1 |
| 642 | Jince, náměstí → Lochovice, náměstí | untimed | | | | |
| 642 | Lochovice, náměstí → Hořovice, náměstí B.Němcové | 13:38, 17:38 (37) | – | – | 0/0 | 1/1/2 |
| 643 | Podluhy, Na drahách → Cerhovice, Třenice (knot Hořovice, náměstí B.Němcové) | 14:40, 16:40, 18:40 (99) | 16:40 | 16:40 | 1/1 | 2/2/4 |
| 643 | Cerhovice, Třenice → Podluhy, Na drahách | 13:14, 15:14, 17:14 (13) | 17:14 | 17:14 | 1/1 | 2/2/4 |
| 649 | Nižbor, u lípy → Nižbor, Žloukovice | :51 (50) | 15:51 16:51 | 15:51 16:51 | 2/2 | 3/4/7 |
| 649 | Nižbor, Žloukovice → Nižbor, u lípy | :02 (1) | 16:02 17:02 | 16:02 17:02 | 2/2 | 3/4/8 |
| 825 | Králův Dvůr, Popovice → Beroun, nemocnice | 13:10, 13:40, 14:10, 15:10, 15:40, 16:10, 17:10, 17:40, 18:10 (9, 39, 69) | 15:40 16:10 17:10 | 15:40 16:10 16:39 17:10 | 3/3 | 12/15/22 |
| 825 | Beroun, nemocnice → Králův Dvůr, Popovice (knot Beroun, Prof.Veselého) | 13:40, 14:10, 14:40, 15:40, 16:10, 16:40, 17:40, 18:10, 18:40 (39, 69, 99) | 15:40 16:10 16:40 | 15:40 16:10 16:40 17:10 | 3/3 | 12/15/23 |
| 825 Mořina | Králův Dvůr, Popovice → Mořina | 14:39, 16:39, 18:39 (98) | 16:39 | 16:39 | 1/1 | 2/3/7 |
| 825 Mořina | Mořina → Králův Dvůr, Popovice | 14:28, 16:28, 18:28 (87) | 16:28 | 16:28 | 1/1 | 1/1/7 |
| 861 | Beroun, autobusové nádraží → Beroun, autobusové nádraží | 13:16, 14:04, 14:52, 15:40, 16:28, 17:16, 18:04, 18:52 (15) | 13:16 14:04 14:52 | 13:14 14:04 14:54 | 3/3 | 1/3/9 |
| X384 | Králův Dvůr, škola → Králův Dvůr, Levín | :00 :30 (29) | 15:30 16:00 16:30 17:00 | 15:30 16:00 16:30 17:00 | 4/4 | 21/21/24 |
| X384 | Králův Dvůr, Levín → Králův Dvůr, škola | :08 :38 (7) | 15:38 16:08 16:38 17:08 | 15:38 16:09 16:38 17:08 | 4/4 | 17/22/24 |

## Changed on 2 Nov (independent review, `review-2026-11-01.md`)

- **545:** split into 545 Strašice (every 120, Hořovice 15:40 / Strašice 16:45, typed 39 / 104, 1 bus) and 545 Zaječov
  (every 120, window 16:30–18:30, Hořovice 16:35 / Zaječov 18:00, `notvia` Strašice and Olešná, typed 94 / 59, 1 bus).
- **548:** the Ex4 pair: 548 every 120 (nemocnice 16:07 / Zbiroh 16:55, typed 66 / 114) and 548 Praskolesy every 120
  (Praskolesy 15:00 via the knot nemocnice 15:07 / Zbiroh 15:55, typed 119 / 54); 2 buses instead of 3.
- **636:** 636 Hýskov removed (its stops are on Kladensko 630); −1 bus.
- **638:** owner check deleted; the two-bus chain named in the notes as a pooling option.
- **639:** split into 639 Dobříš (every 120, Hořovice 15:00 / Dobříš 14:55 at Hostomice 15:25, typed 119 / 114, 2 buses) and
  639 Hostomice (every 120, Hořovice 14:00 / Hostomice 14:35, typed 59 / 94, 1 bus); owner check deleted; 639 Lštěň unchanged.
- **825:** 825 Mořinka → 825 Mořina (to Mořina, back from Mořina 16:28, typed 87, `rt` 67, the 16:28's stops by hand);
  Mořinka, Vysoký Újezd, sokolovna (on 311) and Mezouň, Letník (owner check) are coverage exceptions.
- **X384 (210384):** new, every 30 (škola :00 / :30, Levín :08 / :38, typed 29 / 7), 1 bus; the two X384 coverage exceptions
  are gone.
- **Wording:** 384 Hořovice (the 17:20 game trip has no real Hořovice counterpart), 640 (the 16:31 ends at Hostomice), the
  544 Hořovice → shuttle chain and the 638 chain in the notes.
- **Owner checks:** 3 → 1 (the near-stop check, now two stops).
- **Totals:** 38 → 40 Simutrans lines, 66 → 65 buses; 81 → 85 timed legs, all pass. Every other line unchanged.

## Line by line

**380 Praha, Kukulova – Rudná – Loděnice – Beroun – Králův Dvůr, Počaply** (core: Kukulova, Zličín, Beroun, Lidl, Počaply,
Obchodní centrum). Whole day: Kukulova every 30 at :12 / :42 from 6:15 to 19:12 (12:17 off), Obchodní centrum :27 hourly
until 13:27, then :02 / :32 14:02–18:32 (17:33), 19:41. Buses arrive at Vypich and leave Kukulova: `terminus_alias`. One
line every 30 at the anchor 16:00, both window rows 4/4 exact. The 17:42 Kukulova trip ends at Králův Dvůr, Počaply via
Počaply, škola (counted at U Tří zvonků: branch audit `[BRANCH]`, no window slot is that trip). Off 12–20 h: Kukulova
12:17, Obchodní centrum 12:27, 13:27, 19:41; listed: Rudná, Vypich → Zličín / Vypich 14:30, 15:05, 16:05. 6 buses.
Chain test: 7 of 22 arrivals at Obchodní centrum leave again within 5 min; the model's turn there is 7 min.

**384 Praha, Zličín – Zdice – Hořovice** (core: Zličín, Králův Dvůr, u zámku, Zdice, Hořovice). Out of Zličín every 30:
:50 to Zdice (13:50–18:50; 12:00, 13:00 off), :20 to Hořovice (13:20, 14:20, 16:20, 18:20, 19:20; 15:20 and 17:20 only to
Králův Dvůr, Počaply; 17:50 extra). Into Prague at Zdice every 30: :48 Zdice starts (13:48–17:48, 14:18 too) and :18 the
Hořovice trips (Hořovice :52, 14:52–18:52). Ex4, one Simutrans line per end. Both lines' Zličín legs read to U Tří zvonků
and both back legs at Zdice, so the trips compete by slot: the Počaply shorts fall in 384 Hořovice's :20 slots (15:20,
17:20; branch audit `[SLOT-BRANCH]`, path audit 17:20 — explained: a short working two stops off the line at the Počaply
garage, the game bus runs on to Hořovice; without it the hourly Hořovice row would have an empty 17:20 slot: the real Hořovice departure after 16:20 is 17:50, 30 min later, so the row would fail Step 4, and every 120 out against the hourly :52 back would break the same rate at both ends; this is the only every-60 row that passes. **Changed on 2 Nov (wording):** the 17:20 game trip has no real Hořovice counterpart; it stands for the 17:20 Počaply short and the 18:00 Zdice → Hořovice short together, as the why now says), and the 17:50
Hořovice trip falls in 384's :50 slot (`[beyond]`, outside the window). Step 4: all four legs 2/2 exact. The Hořovice :52
buses come either from Zličín :20 or from the Zdice → Hořovice shorts 15:55 and 18:00 (which bring the 14:50 and 16:50
Zdice buses on), listed. 2 + 3 buses.

**394 Praha, Nové Butovice – Beroun – Zdice** (core: Nové Butovice, Králův Dvůr, u zámku, Zdice). Outstation: 5:20–7:34 every
10 min Zdice → Prague; afternoon Zdice :03 / :33 14:33–17:33 into Prague, Nové Butovice every 15 out (:00 / :30 Zdice, :15
/ :45 Počaply). Inbound rate every 30: Nové Butovice :00 / :30, Zdice :03 / :33; window out 4 slots for 5 departures (15:30,
16:00, 16:30, 17:00, 17:20) filled 4/4, back 4/4 exact. Off 12–20 h out: 12:40, 13:40, 14:15, 15:15, 17:20, 17:45, 18:50,
19:10, 19:50 and the seven Počaply shorts (buses going home); back 12:28, 13:28, 18:38, 18:58 (14:00 is 3 min early, on the pattern). The 15:30 Králův Dvůr,
u zámku → Nové Butovice listed. No empty return (owner, 25 Oct). 4 buses. Chain test: 394 ↔ Prague 142 at Nové Butovice
(21 of 37), named in the notes.

**526 Zdice – Žebrák / Bzová / Knížkovice** (core: Zdice, Žebrák, Bzová, Knížkovice). The afternoon is one bus in a fixed
sequence (chain test: 3 of 3 at Hředle, 7 of 7 at Knížkovice, 2 of 3 at Bzová turn within 5 min). Its 14:30–16:30 round is
exactly 120 min, so a 6-leg circuit every 120 (the 418 rule), anchor 15:00 by hand so the window holds the whole round:
every leg 1/1 exact. 0-minute turns at Zdice (15:10) and Knížkovice (16:20) with `lay` 0. Žebrák → Zdice takes the 14:56
trip's path via Hředle and Zdice, autoservis (`stops_via`; the builder had picked the 13:46's Bavoryně path on a tie). Off:
13:25 → Žebrák, 13:46 → Zdice, 12:50 from Bzová, Knížkovice 12:30, 14:10, 19:15; listed: the Hředle shorts 17:15, 18:47.
1 bus. Bzová, Chlustina (2), Hředle, Zdice, Knížkovice, autoservis and Žebrák, Sedlec are only on 526.

**527 Komárov, Buzuluk – Cerhovice – Žebrák** (core: Žebrák, Cerhovice, Buzuluk). 6 afternoon trips by one bus, last at 16:34.
Every 120 on the 15:23 / 15:59 round, anchor 15:30 by hand (window 15:00–17:00: the line ends at 16:34, so the automatic
16:00 window would hold a 17:23 repeat without a trip). Both legs 1/1 exact. Off: Buzuluk 14:34; listed: Cerhovice shorts.
Every 240 was the other candidate (same exact count); every 120 is nearer the real 13–17 h headway (Buzuluk 14:34, 15:59).
1 bus. Komárov, Lidový dům and Sokolovice are its own.

**528 Hořovice – Žebrák – Březová – Kublov – Broumy** (core: Hořovice, Březová, Broumy). Hourly :15 / :02, 8 + 7 exact over the
day; anchor 16:00, 2/2 both ways. 2 buses. Březová shorts 13:15 and 20:15 listed.

**529 Hořovice – Hvozdec** (core: Hořovice, Hvozdec). A 6-min shuttle about every 110 min (13:15, 15:05, 17:00, 18:50).
Every 120 at 17:00 (the window's trip, exact); 15:00 / 19:00 repeats 5 / 10 min off; every 96 and 144 were worse. 1 bus.

**531 Hořovice – Jince – Příbram** (core: Hořovice, železniční stanice, náměstí, Jince, sokolovna, Příbram, autobusové nádraží).
Hourly :57 from Hořovice, železniční stanice and :57 from Příbram, autobusové nádraží (the 13:51–16:51 Archiv starts pass it
at :57), 9 + 11 exact over the day. The automatic anchor (13:40) holds the school extras from Hořovice, náměstí (13:25,
14:35; Archiv 14:21, Zdaboř 13:11): anchor 16:00 by hand, both legs 2/2 exact. Příbram arrivals end at "Příbram,
autobusové nádraží (ul. Čs.armády)" and departures leave "Příbram, autobusové nádraží": `terminus_alias`. The out leg takes
the 15:57 / 17:57 path via Felbabka, rozcestí and Křešín (`stops_via`; Felbabka, rozcestí has no other modelled line); the
path audit flags 15:51 Archiv back via Křešín (explained: the way back is direct, as 16:51). 2-minute real turn at Hořovice.
3 buses. Its Příbram, Archiv / Zdaboř variants leave 8 okres-Příbram stops to the Příbramsko sheet (see the end).

**544 Hořovice – Komárov – Zaječov** (core: Hořovice, Buzuluk, Komárov, Malá Víska, Zaječov). Afternoon: hourly Zaječov :08 →
Komárov / Komárov :34 → Zaječov 16:08–17:48 and single trips (Hořovice 13:52 → Mrtník, Mrtník 14:09 → Buzuluk; Hořovice
14:52 → Zaječov via Neřežín; Zaječov 13:38 → Hořovice; Buzuluk 13:32 → Zaječov). 544: the shuttle every 60, anchor 16:30 by
hand (window 16:00–18:00, where it runs; at 16:00 the 15:34 slot would be empty), 2/2 exact both ways, 1 bus. 544 Hořovice:
Chaloupky, Neřežín (1.1 km from Chaloupky), Hvozdec, Mrtník and Komárov, Na Kocábce have no other line; one bus's real
sequence 13:52–15:24 every 240 (window 13:30–15:30), 1/1 exact each, the way back from Zaječov untimed — Zaječov 13:38 →
Hořovice cannot be on that bus in any period (it leaves 14 min before the 13:52 and takes 26), so it is off the pattern
(its stops are on both lines). 1 + 1 buses. Chain: the Mrtník bus goes on as 545 Buzuluk 14:20 → Olešná (2 of 2).

**545 Hořovice – Zaječov – Těně – Strašice** (core: Hořovice, Buzuluk, Zaječov, Strašice). Exactly hourly at Zaječov (:59 out
14:59–18:59, :00 back 16:00–19:00), with the ends alternating: Strašice trips out of Hořovice 14:35 (via the station),
15:40, 17:40 (direct), back from Strašice 15:45, 16:45; Zaječov trips out 16:35, 18:35, back 14:20, 18:00, 19:00; the
Olešná branch (13:30, 13:59, 14:54, Buzuluk 14:20) kept out with `notvia` Olešná [BE] and listed. **Changed on 2 Nov:** the
one-line design (every 120, two slots each way, Zaječov trips run on to Strašice in the game) is split, one Simutrans line
per end, so no game trip runs past its real terminus: **545 Strašice** every 120, Hořovice 15:40 → Strašice 16:15 (35, the
direct road), Strašice 16:45 → Hořovice 17:25 (40), typed 39 / 104, window 15:30–17:30 1/1 exact each way (Strašice 15:45 is
the second real departure in the window, 60 before the slot), 1 bus; **545 Zaječov** every 120 with its own window
16:30–18:30 (the Zaječov trips' peak, as the 544 shuttle's 16:00–18:00), Hořovice 16:35 → Zaječov 16:59 (24, via the
station and Letná), Zaječov 18:00 → Hořovice 18:25, typed 94 / 59, 1/1 exact each way, 1 bus (61-min wait at Zaječov, as
the real bus). Together Zaječov keeps :59 out and :00 back every hour, no shared minute. Off: Hořovice 14:35, Strašice 15:45,
Zaječov 14:20, 19:00. 1 + 1 buses, as before. Těně (Plzeňský kraj) is its own.

**546 Hořovice – Strašice – Dobřív – Rokycany** (core: Hořovice, Komárov, Strašice, Rokycany). Hourly :09 / :40, 9 + 5 exact,
2/2 both ways. 3 buses (66 min each way). Shorts listed. 18 stops only on 546 (Jivina; Dobřív, Rokycany, Strašice, Huť…).

**547 Hořovice – Kařez – Cerhovice** (core: Hořovice, Komárov, Cerhovice). Five trips a day, one after 13:00 (14:40 →
Cerhovice). Kařez, Kařez, u Jednoty, Kařízek (Plzeňský kraj) and Osek, u Anýže have no other line: every 480 on the 14:40 and
the 7:15 Cerhovice → Hořovice, which falls at 15:15, one minute after the 15:14 arrival (1 bus). No slot in the window (both
named in the why). The Komárov trips (7:11, 9:50, 10:11) listed.

**548 Hořovice, nemocnice – Cerhovice – Zbiroh / Praskolesy** (core: nemocnice, železniční stanice, Cerhovice, Zbiroh,
Praskolesy). Hourly from 15:07: nemocnice :07, Zbiroh :55; the automatic anchor 14:40 window fails (the 14:00–15:30 extras
14:12, 14:37, 15:25), so anchor 16:00 by hand. **Changed on 2 Nov:** the Praskolesy trips are through trips of the same hourly
pattern (Praskolesy 13:00 and 15:00 → Zbiroh pass nemocnice 13:07, 15:07; Zbiroh 17:55 → Praskolesy), not a shuttle, and the
1 Nov design counted the 15:00 twice and sized a 7-min shuttle with a 104-min wait (3 buses). Now the Ex4 pair (501 / 501B):
**548** every 120, nemocnice 16:07 → Zbiroh 16:47, Zbiroh 16:55 → nemocnice 17:31, typed 66 / 114, window 15:30–17:30 1/1
exact each way, 1 bus; **548 Praskolesy** every 120, window 14:30–16:30, Praskolesy 15:00 → Zbiroh read at the knot nemocnice
15:07 (typed 119; 47 min, the 15:00 trip's road), Zbiroh 15:55 → Praskolesy (typed 54, read to nemocnice: the real 15:55 ends
there and the game bus runs 7 min on, as the real 17:55 does; stops and `rt` 43 set by hand to the 17:55's road, because
the builder's tie-break took the 14:12's detour via Cerhovice, škola), 1/1 exact each way, 1 bus. Combined at nemocnice :07
out and :55 in every hour, no shared minute; Praskolesy 13:00 / 15:00 and Zbiroh 17:55 → Praskolesy are now exact. Off: Zbiroh
14:12 → Praskolesy, 14:37, 15:25. 1 + 1 buses (was 2 + 1).

**631 Nižbor, Šnárová – Beroun – Suchomasty – Všeradice** (core: Šnárová, Beroun, Králův Dvůr, u zámku, Suchomasty, Všeradice).
A through line from 14:32: Šnárová :32 → Beroun :00 → Všeradice :56 (via Vinařice, Nesvačily, Podbrdy), 1-min turn, :57
back via Bykoš → Beroun :39, then :02 → Šnárová :30 (chain test: 10 of 19 at Šnárová, 8 of 12 at Všeradice, 8 of 19 at
Beroun). One circuit every 60 (3 buses), the Všeradice-bound leg read at the knot Beroun :00 (it also takes the Beroun-start
13:00, 14:00). Anchor 15:00 by hand: the automatic 13:40 window holds 13:50 / 14:57 from Všeradice (7 off) and the
Beroun-start trips; at 15:00 all three legs are 2/2 exact. Off: Všeradice 13:50, 16:51, 18:13. Path audit: 15:57 Všeradice
runs via Málkov, Jednota (on the out leg's `stops_via`). Listed: Šnárová 13:32 → Beroun, Králův Dvůr 13:56 → Šnárová,
17:36 → Tmaň, the u lípy trips (through with 649).

**633 Beroun, Zdejcina – Tetín – Liteň** (core: Zdejcina, Beroun, autobusové nádraží, Tetín, křižovatka, Liteň). Two buses,
one per end in the 15–18 h window (see note). Ex4, two lines every 120 on the two real rounds at the automatic anchor 15:50:
633 Zdejcina 16:16 / Liteň 17:19 (15:20 one minute off), 633 Tetín 15:28 / 16:29 (`notvia` Liteň), each leg 1/1 exact. One
line with the Tetín shorts as short workings also passes (every 120 two slots, 2 buses) but would send them to Liteň in the
game: the split is the same cost and real. Off: 13:03, 14:03, 13:13, 14:13; 17:03, 18:03, 19:03, 18:35. 1 + 1 buses.

**634 Hostomice – Lážovice – Všeradice, železniční zastávka** (core: Hostomice, Osov, škola, Všeradice). Hourly :25 / :41
14:25–17:41 with no trip at 15:25 / 15:41. At the automatic 13:30 (13:20 is 5 min off :25) and at 16:00 (the 15:25 / 15:41 gap) the window fails, so the
anchor is 16:30 by hand (window 16:00–18:00), 2/2 exact both ways. One-way loop: out direct 13 min, back via Podbrdy, Vižina,
Osov 18 min. 1 bus. Osov, škola short (13:00) listed.

**636 Loděnice – Železná (– Chyňava – Hýskov)** (core: Loděnice, Železná, Chyňava, škola, Hýskov). Hourly Loděnice :45 /
Železná :22, 4 + 5 exact, 2/2 both ways, 1 bus. **Changed on 2 Nov:** 636 Hýskov (every 240 on the Loděnice 12:35 → Hýskov /
Hýskov 13:10 → Loděnice round, 1 bus) is removed: its four Chyňava stops (Libečov, u mostu; u Nováků; u Jonášů; škola) are on
Kladensko's modelled 630 (every 60 both ways), Step 8. The round and the Hýskov – Chyňava, škola shorts are listed in the note
as "stops on Kladensko 630"; the four stops are coverage exceptions with that reason. −1 bus.

**637 Kublov – Beroun – Řevnice** (core: Beroun, Nový Jáchymov, Kublov, Liteň, Řevnice). West branch hourly Beroun :00 /
Kublov :08 (11 + 5 exact); after 16:00 the Beroun :00 trips end at Nový Jáchymov (buses going home: Nový Jáchymov 4:37–6:57
start the day) and nothing comes back from Kublov after 16:08. The automatic 16:00 window holds those home runs, so the
anchor is 14:00 by hand, where the line's own pattern runs both ways (2/2 exact). The Nový Jáchymov trips count as short
workings (core_to). Trubská (1.2 km from Trubská, rozcestí 1.0) is only on the 15:00 / 15:08 trips: `stops_via` Trubská on
both legs (53 / 50 min instead of 48 / 47). East branch: one bus's round 14:05 → Řevnice / 15:14 → Beroun, every 120, 1/1
exact (16:03 → Liteň within 2 counts). 2 + 1 buses.

**638 Beroun – Broumy – Branov / Skryje, Beroun – Liteň** (core: Beroun, Králův Dvůr, u zámku, Broumy, Branov, Skryje, Liteň).
South-west: Beroun hourly :30 with the end rotating (13:30 Branov, 14:30 Broumy, 15:25 Skryje, 16:30 Branov, 17:30 Broumy).
Ex4: three lines every 180 (each end's trips are 180 apart: Branov 13:30 / 16:30, Broumy 14:30 / 17:30), offset as the real
rotation: 638 (Broumy, `notvia` Branov, Skryje) at the automatic 16:10 window, 638 Branov (window 13:00–15:00) and 638
Skryje (window 15:00–17:00) by hand, every leg 1/1 exact. 3 buses where the timetable chains them on 2 (owner check). Liteň
branch: Beroun 13:59, 14:57, 17:01 / Liteň 14:30, 15:42, 17:34 — no hourly minute passes (15:59 has no trip); every 120 on
the 17:01 / 17:34 round (1/1 exact; 15:42 eight off in the window, real 2 vs 1 slot), 1 bus, for Koněprusy, jeskyně and
Bykoš, odbočka Vinařice. 1 + 1 + 1 + 1 buses.

**639 Hořovice – Lochovice – Hostomice – Dobříš** (core: Hořovice, Lochovice, Hostomice, Malý Chlumec, Dobříš). Hořovice :00
hourly, the ends alternating 50/50 (Dobříš 13:00, 15:00, 17:00 to Malý Chlumec; Hostomice 14:00, 16:00); back at Hostomice
:25 / :35 (Dobříš 12:55, 14:35, 16:55 pass it 13:25, 15:25, 17:25; Hostomice starts 14:35, 16:25). **Changed on 2 Nov:** the
one line every 60 to Dobříš (3 buses) sent the Hostomice buses on to Dobříš (Osov, Velký Chlumec and Dobříš hourly where the
real is every 2 h; the 292 case); the 1 Nov owner check called the split +1 bus, but with the Hostomice pair 14:00 / 14:35
(the real 5-min turn) it costs the same. **639 Dobříš** every 120, window 14:30–16:30, Hořovice 15:00 → Dobříš (`via` Malý
Chlumec; 66 min; the 17:00 repeat is the real 17:00 to Malý Chlumec, the game bus runs 12 min on), Dobříš 14:55 → Hořovice
timed at the knot Hostomice 15:25 (`knot_rt` 30 pinned: the real 14:35 dwells about 20 min on the way, so the game leaves
14:55 to pass Hostomice at the real 15:25), typed 119 / 114, 1/1 exact, 2 buses; **639 Hostomice** every 120, window
13:30–15:30, Hořovice 14:00 → Hostomice 14:30, Hostomice 14:35 → Hořovice (`notvia` Dobříš and Malý Chlumec), typed 59 / 94,
1/1 exact, 1 bus (the real 16:00 / 16:25 pair would need 2: 116-min wait; 16:25 and 12:25 are off). Together Hořovice :00
hourly, no shared minute. 639 Lštěň unchanged (every 480, 13:10 / 13:14, 1 bus; Hostomice, Lštěň 1.9 km from Hostomice,
náměstí). The owner check on 639 is deleted. 2 + 1 + 1 buses, as before.

**640 Zdice – Lochovice – Hostomice – Jince** (core: Zdice, Lochovice, Hostomice, Jince, sokolovna). Zdice :30 (15:30, 16:30,
18:30), Jince :31 every hour 13:31–18:31 (14:31 from Čenkov; 13:31, 16:31, 18:31 end at Hostomice and count as short
workings, `core_to` Hostomice). The automatic 13:30 window (only Lochovice shorts) fails; anchor 16:00, 2/2 exact both ways.
2 buses. **Changed on 2 Nov (wording):** the why now says that the 16:31 (and 13:31, 18:31) end at Hostomice and the game bus runs on 27 min to Zdice, which no real bus does. Through running: 641 Beroun → Zdice, škola (14:07, 16:00, 18:00) continues as 640 14:43, 16:28, 18:28 (3 of 4
departures at Zdice, škola follow a 641 arrival) — named in the notes; not a circuit, because the 641 Trubín trips' stops
are all on 638 and 384.

**641 Beroun – Zdice – Praskolesy – Hořovice, nemocnice** (core: Beroun, Králův Dvůr, u zámku, Zdice, Praskolesy, nemocnice).
Hořovice :20 hourly 14:20–16:20 (12:50 off). Beroun → Hořovice 13:00 and 14:02 via Trubín, Svatá and Zdice, škola (56 min),
15:07 and 17:07 direct (47): no Beroun minute holds both, so the leg is read at the knot Zdice :28 (they pass 13:28, 14:30,
15:26, 17:26), Beroun = :28 − 19 (direct) = :09; window 2/2 within 2 (14:11 at the terminal for the 14:02, 15:07).
Every 120 with one slot each way also passes (5 exact) but halves an hourly line (Opavsko rule 5, the 409 / 411 mistake).
Game path set by hand to the direct road (`stops`, `rt` 47; the builder had taken the Trubín path on a 2:2 tie); back via
Levínský vršek, `rt` 51 (the 15:20 runs via Zdice, škola and Levín in 60: path audit, explained). 3 buses.

**642 Hořovice – Praskolesy – Lochovice – Jince** (core: Hořovice, Praskolesy, Lochovice, Jince, náměstí). Three afternoon
trips (Lochovice 13:38 → Hořovice, Hořovice 15:38 → Jince, Praskolesy 18:38 → Lochovice). Its own stops (Lochovice,
Netolice, ústav, železniční stanice, Obora, papírna I; Jince, Rejkovice, lopatárna) need a line: every 240 on one bus,
Hořovice 15:38 → Jince (exact), untimed to Lochovice, Lochovice 17:38 (= 13:38) → Hořovice. 1 bus.

**643 Podluhy – Hořovice – Cerhovice, Třenice** (core: Podluhy, Hořovice, Cerhovice, Třenice). 0-minute turns at both ends
(10 of 10 at Podluhy, 4 of 5 at Třenice). Through trips Podluhy → Třenice about every 2 h (13:05, 14:50 from Hořovice,
16:40), Třenice → Podluhy 15:14, 17:14. Every 120 timed through Hořovice :50 (Podluhy 16:40), Třenice 17:14; anchor 16:00 by
hand (the automatic 13:30 window holds the Podluhy and Křešín shorts and a 13:14 Třenice slot with no trip). 1/1 exact each
way, 1 bus. Listed: the Podluhy shorts, Cerhovice, náměstí – Třenice shorts, the 14:10–15:10 Křešín round.

**649 Nižbor, u lípy – Žloukovice** (core: u lípy, Žloukovice). Hourly :51 / :02, 2/2 exact both ways, 1 bus. Every 649 trip
follows a 631 Beroun / Králův Dvůr → u lípy arrival (6 of 6) and 5 of 7 arrivals go on as 631: a through pair. A circuit
Beroun → u lípy → Žloukovice → u lípy → Beroun would need 2 buses (the 631 legs take 22 min each way), so it does not save
a bus (Step 5b): kept separate, named in the note.

**825 Králův Dvůr, Popovice – Beroun, nemocnice / Mořina** (core: Popovice, nemocnice, Prof.Veselého, Mořina). Town line every
30 out of Popovice (:10 / :40) with every other :40 a Mořina trip (14:39, 16:39); towards Popovice every 30 at
Prof.Veselého (:11 / :41) with the Mořina 13:14 / 16:28 and Loděnice 14:49 trips in the gaps. 825 every 120 with three
slots each way (out read to Hostímská so the 17:10 that ends at Prof.Veselého counts; back at the knot Prof.Veselého) and
the Mořina line on the fourth (501 / 501B): 3/3 and 1/1 exact. **Changed on 2 Nov:** 825 Mořinka becomes **825 Mořina**: the
slot trip 16:39 ends at Mořina 18:00 (only the 13:07 reaches Mořinka), and the way back follows the 16:28 itself (direct via
Kozolupy, Bubovice, Loděnice, Svatý Jan pod Skalou, nemocnice; stops set by hand because the afternoon Mořina trips run three
roads and the builder's tie-break would take the 13:14's; `rt` 67, typed 87) instead of the 8:33 Mořinka trip's road via
Vysoký Újezd, sokolovna and Mezouň, Letník (+27 min that no afternoon bus runs). Mořinka and Vysoký Újezd, sokolovna are on
Praha-západ's modelled 311 (coverage exceptions with that reason); Mezouň, Letník (one afternoon trip, 825 Loděnice 13:54 →
Letník 14:14; 0.35 km from Mezouň, on 311) goes into the near-stop owner check. Need stays 2 (16:39 → Mořina 18:00, 18:28 →
Popovice 19:35, 20:39). Branch audit: 825 out `[SLOT-BRANCH]` (17:10 ends at Prof.Veselého, the stop after nemocnice) and
back `[BRANCH]` (Mořina trips owned by 825 Mořina, the Loděnice 14:49 off the pattern) — explained. 2 + 2 buses.

**861 Beroun town line** (core: Beroun, autobusové nádraží, Karla Čapka). One-way 22-min loop at 13:14, 14:04, 14:54 (every 50)
and 16:00 (to Karla Čapka only); earlier :00 / :14. Every 48 (worst 2 min; every 60 at :14 fails the window, 14:14 has no
trip; every 45 leaves 13:14 and 14:54 five off). 3/3 within 2 in the window, 1 bus. Its eight stops (Obchodní … Karla Čapka) are
only on 861.

**X384 (210384) Králův Dvůr, škola – Levín (– Zdice)** (core: škola, Na knížecí, Levín). **New on 2 Nov:** the replacement
line for the Levín works is in both the 29 Sep and the 1 Nov feeds, so these are long works, modelled as they run (the
long-works rule; `00_config.py` no longer lists bus X lines automatically). Every 30 all day: škola :00 / :30 → Levín
:08 / :38 (8 min), at once back :08 / :38 → škola :17 / :47 via Počaply, Plzeňská, Jungmannova and Zahořany, Pod Hájem
(24 of 24 Levín arrivals leave again within 0–5 min; `lay` 0); the 16:38 and 18:37 end at Na knížecí (`core_to`, short
workings). One line every 30, window 15:30–17:30 4/4 exact out, 4/4 within 1 back, 21 + 17 exact over the day, typed 29 / 7,
1 bus (the live map shows one bus, ROŠERO 8705, doing it). It is the only service of Králův Dvůr, škola and Králův Dvůr,
Levín, so the two coverage exceptions of 1 Nov are gone. Listed: Na knížecí 6:03 → Levín, škola 7:10 → Zdice.

**952** night line: listed automatically.

## Audits

- **Branch audit** (19 legs read at a midpoint): `[ok]` 14. Flags: 380 out `[BRANCH]` (17:42 to Počaply via škola, no window
  slot); 384 out `[beyond]` (the 17:50 Hořovice trip in the Zdice line's :50 slot, outside the window); 384 Hořovice out
  `[SLOT-BRANCH]` (the 15:20 / 17:20 Počaply shorts); 825 out `[SLOT-BRANCH]` and back `[BRANCH]` — all explained above.
- **Path audit** (6 slots; the 545 16:35 flag is gone with the split): 384 Hořovice 17:20 (Počaply short); 531 back 15:57
  (= 15:51 Archiv via Křešín); 631 back 15:57 (via Málkov, Jednota); 641 out 14:09 (= 14:02 via Trubín) and
  back 15:20 (via Zdice, škola and Levín); 825 out 17:10 (ends at Prof.Veselého). Each is a variant path of a real slot trip,
  named in the line's why or note; every stop it skips is on the row's other trips or on another modelled line.

## Coverage (Step 9)

413 stops served 13:00–19:00, 397 on this sheet's Simutrans lines. Okres Beroun stops not on a modelled line, all in
`coverage_exceptions`:
- on a neighbouring sheet's modelled line (cross-sheet dependencies for the `--final` pass): Chyňava, Libečov, u mostu;
  Chyňava, u Nováků; Chyňava, u Jonášů; Chyňava, škola → Kladensko 630 (every 60 both ways); Mořinka and Vysoký Újezd,
  sokolovna → Praha-západ 311 (hourly);
- the near-stop owner check: Zaječov, u hřbitova (545's Olešná trips only, 0.65 km from Zaječov) and Mezouň, Letník (825's
  13:54 only, 0.35 km from Mezouň, which 311 serves).
Also cross-sheet: Hostomice, Lštěň, rozcestí (on the way to Lštěň, not on 639 Lštěň's two stops) → Praha-západ 632; Osov and
Vižina are also on 632. The 8 okres-Příbram stops only 531's Archiv / Zdaboř variants serve (Příbram, Archiv, II. and III.
poliklinika, Na Cihelně, Československé armády, Seifertova, Zdaboř, Žežická, Zdaboř, nemocnice) → the Příbramsko sheet; if it
does not cover them, 531's Příbram end moves to Archiv. Outside the kraj: none uncovered (Strašice, Těně, Dobřív, Rokycany,
Kařez, Kařízek, Zbiroh, Týček, Cheznovice on 545 Strašice, 546, 547, 548). Places served only by a line kept for them: 544
Hořovice (Neřežín, Mrtník, Na Kocábce), 547 (Kařez, Kařízek, Osek, u Anýže), 548 Praskolesy (Kotopeky ×2), 638 Liteň
(Koněprusy, jeskyně, Bykoš, odbočka Vinařice), 639 Lštěň, 642 (Lochovice ×5, Rejkovice, lopatárna), X384 (Králův Dvůr, škola
and Levín); `stops_via` for Trubská (637) and Felbabka, rozcestí (531).

Stops of another Středočeský okres that only this oblast's lines serve, all on this sheet's lines (for the `--final`
pass): okres Příbram — Jince (7 stops, with Rejkovice), Čenkov (3), Hluboš (2), Bratkovice, Dominikální Paseky, rozcestí,
Trhové Dušníky, Na Homoli, Křešín [PB] (531 / 640 / 642), Dobříš, Na Hradci, pod Hradcem, sanatorium, Trnová, dvůr,
U Slovanky (639 Dobříš); okres Praha-západ — Nučice, rozcestí Krahulov, Rudná, Celní úřad, Hewlett-Packard, Vypich (380);
okres Rakovník — Skryje, Suchá jedle and U ručiček (638 Skryje).

## Bunching at the hubs

Every shared minute in the model is a real one: Beroun, autobusové nádraží :00 (631 to Všeradice and 637 to Kublov, as real,
sharing Delvita – Králův Dvůr, u zámku), 17:00 / 17:01 (637, 638 Liteň, opposite directions); Hořovice, náměstí 17:00 (529
and 639, different roads), 15:38 / 15:40 (642, 545, different roads); Zdice 14:30 and 16:30 (526 west, 640 south, as real).
Towards Prague at Zdice 394 :03, 384 Hořovice :18, 394 :33, 384 :48 interleave every 15 as in reality. 638's three every-180
lines keep Beroun's :25 / :30 rotation; 633 Tetín (:28) and 633 (:16) alternate at Zdejcina; 825 and 825 Mořina give
Popovice and Prof.Veselého every 30 without a shared minute; the two 545 lines keep Zaječov :59 out / :00 back hourly, the two 548 lines nemocnice :07 / :55, the two 639 lines Hořovice :00.

## Script problems

- `run_oblast.py` had a syntax error (an f-string broken across lines, line 40) from about 05:20 on 2 Nov; the coordinator
  fixed it. Before that I ran it once through a wrapper in my scratchpad that repaired the string in memory (the script
  file was not changed); every result above comes from the fixed script.
- `05_schedule.py` picks a leg's path by `Counter.most_common` among the afternoon trips; on a tie it takes the first trip's
  path, which can be the minority variant (526 Žebrák → Zdice took the 13:46 Bavoryně path, 641 the Trubín path). Fixed here
  with `stops_via` / `stops`, and on 2 Nov again on 548 Praskolesy (the 14:12 detour via Cerhovice, škola) and 825 Mořina (three
  roads from Mořina); a tie-break by the window's slot trips would avoid it.
- (1 Nov) 825 Mořinka's back leg got a running time of 97 from the builder where its one trip took 94; gone with the 2 Nov
  direct path.
- 2 Nov: `00_config.py` no longer lists bus X lines automatically; X384 is designed above.

## Owner check (1)

**545, 825 — the sheet's near-stop exceptions:** Zaječov, u hřbitova (0.65 km from Zaječov, which 545 serves hourly; only the
545 Olešná trips pass it: Hořovice 13:30 → Olešná, Olešná 13:59 and 14:54 → Hořovice) and Mezouň, Letník (0.35 km from
Mezouň, which Praha-západ 311 serves; only 825's Loděnice 13:54 → Letník 14:14). Serving them: Zaječov, u hřbitova with
545 Olešná every 240 (13:30 / 13:59, both exact), +1 bus; Mezouň, Letník on every 825 Mořina return by the 8:33 Mořinka
trip's road (0 buses, +27 min on each return) or as 825 Letník every 480 on the 13:54, +1 bus. "u hřbitova" is a village
stop, not a rozcestí, so the roadside rule does not literally cover it; that is why it is the owner's call.

Deleted on 2 Nov: 639 (the split is cost-neutral, the rules decide) and 638 (the circuit leaves Beroun without its 16:30
departure; the two-bus chain is now a pooling fact in the notes).

## Open questions

- The 0–2-minute real turns (526, 529, 531, 544 Hořovice, 547, 631, 639 Lštěň, 643, X384) assume the fork's automatic
  "Leave up to" lets a bus that arrives on the real minute leave although the loop rule typed the departure 1 min early —
  the engine question from the pilot, to confirm once for all sheets.
- The through-running pairs in the notes (the 638 two-bus chain, 544 Hořovice 14:52 → the 16:08 shuttle, 649 ↔ 631, 641 → 640, 526 ↔ 641, 631 ↔ 637, 633 → 638, 638 → 637, 544 → 545,
  546 → 545, 642 → 639, 548 → 642, 825 → 380 / 384 / 636, 394 ↔ 142) wait for the 2 Nov live map; none changes a line here
  unless the owner chooses pooling.
- 531's Příbram end: Příbram, autobusové nádraží (where the window trips end) or Archiv (where the 13:51–16:51 start); Archiv
  would cover the 8 okres-Příbram stops above if the Příbramsko sheet does not.
