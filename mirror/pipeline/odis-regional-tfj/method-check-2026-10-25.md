# Bus schedule method, applied to the Těšínsko/Třinecko/Frýdecko sheet (25 Oct 2026)

After the hand check of the Hlučínsko lines found every scripted row wrong, the owner asked: "verify all sheets with this
level of detail" ("that's the point of you doing it, so you'll not produce incorrect results"). The Step 4 audit of this
sheet (`../audit/audit-regional-2026-10-25.md`) found 88 of its 184 timed legs failing: 84 EMPTY (a window slot with no
real departure within 3 min) and 4 FEWER, on 60 Simutrans lines of 55 real lines. Each of those lines was checked by hand,
both directions together, against `../bus-schedule-method.md` (v4), as in `../odis-regional-opavsko/method-check-2026-10-25.md`.
The published state is sheet v5 (`data/published/roster_v5.json`).

- **Data:** the sheet's JDF trips for Tue 20 Oct 2026 (`data/derived/trips.json`), the whole-day reading
  (`data/derived/reading/<L>.txt`) and the ODIS live-map plate chains (`chains.json`, 13:00–19:30).
- **Every row was built with 05_schedule's own code** and is what `05_schedule.py --base odis-regional-tfj` now prints.
  After the rebuild, `../audit/step4_regional.py odis-regional-tfj` gives **180 of 184 timed legs ok, 1 EMPTY, 3 FEWER**
  (before: 96 ok, 84 EMPTY, 4 FEWER). The four are listed at the end with why. Coverage stays at 0 uncovered (854
  afternoon stops: 769 on this sheet's lines, 85 on other sheets').
- **Typed values** are (real − 61) mod every: every terminus is a loop. The real times under each value are worked out from
  the value itself.

## How each line was decided (one rule for all)

1. **Read points first.** Where a line has a variant Simutrans line, the main rows no longer count the variant's trips
   (`via` / `notvia`): 745 Třanovice, 771 Hluchová (Setinka), 781 Hrčava, 783 (only trips through to Bukovec), 706 (the later
   combined trips), 707 (the short circle), 343 Podolánky, 345 Hutě, 351 Bebek, 358 Steel, and 344's Hyundai shift trips.
   Trips towards a hub that start at different places are read where they all pass: 980 back at Rožnov, 312 back at the
   poliklinika, 314 at Baška, železniční stanice. The model hour is set by hand only where the line's own pattern runs
   elsewhere:
   - 708 and 302 end their every-30 inside the default window;
   - 303 changes paths at 16:27;
   - 343 runs only one outstation trip after 16:06;
   - 345 and 715 got their default anchor from trips that are not the line's own pattern (345: a 14:05 hop and the Hutě
     trips; 715: one short trip);
   - 316's round gets a window of its own, 14:00–16:00, as 285 has on the Opavsko sheet.
2. **One interval per Simutrans line, the same number of slots per period at both ends** (Step 7).
3. **Each direction passes Step 4** (window slots = real departures ± 1, at least 80 % of the window slots with a real
   departure within 3 min) **and keeps the real rate.** Its slots in 13:00–18:00 are at least the real departures there
   minus 1. The ±1 tolerates a ragged count, but it must not halve a line. The bound is a lower one only: the pattern
   stands for the peak, so a line keeps its peak rate where service thins later (method: "the afternoon wins").
   Exceptions, each named on its card:
   - the outstation shape: one direction is timed at the other direction's rate, and the extras are buses going on to
     another line, listed with their plates (FEWER by design);
   - shift lines repeat every 480 (Step 8: 703, 358, 308 Mitrovice, as 709 already did).
4. **Ranking among the candidates that pass**, in this order:
   1. need at most the published need;
   2. most exact on the window's real departures, both directions;
   3. fewest typed values;
   4. most exact over the day, 5–23;
   5. fewer buses;
   6. intervals dividing 60 first, then the others (at most 480, never 720 or 1440; an odd interval only where clearly
      better);
   7. smallest worst deviation.

   Where no candidate passes at the published need, the cheapest passing one is taken, and the cheaper option goes on the
   owner checks with its bus count. Two slots within 3 min of the same trip count once (that rejected a fake 4-bus pass on
   301). A turn shorter than 3 min counts only where the real timetable turns that fast (Step 10).
5. **A leg that passed was not touched** unless the other direction forced it. Where one leg of a line was set by hand,
   both were set explicitly, so the builder's joint pairing cannot move the untouched one.
6. **If nothing passes,** the simplest even pattern at the real rate is kept, approximate, on the To check list (Step 4
   rule 4). Only 980's out row ended there (below).

## Step 5b: buses change line at the hubs all afternoon

From the live map, 13:00–17:00, buses arrive on one line and leave on another:
- Třinec, autobusová stanice: 69 changes among the Třinec town lines and the 732–787 regional lines;
- Český Těšín: 19 at the bus station and 12 at the railway station;
- Frýdlant, železniční stanice: 18;
- Místek, Riviéra and poliklinika: 8 and 14.

This is the HKO Frýdek-Místek corridor case (365–369): one Simutrans line per real line is kept, and pooling a hub's buses
is the owner's choice (not applied). A line's in/out imbalance at a hub shows which departures are buses going on to
another line or home. Those are the extras that fall off the pattern: 732 from Havířov, 745 from Hnojník, 750 from Frýdek
(plates on their cards).

## Totals

| Group | Lines | Buses before → after |
|---|---|---|
| Jablunkovsko–Třinecko (861) | 764, 766, 770, 771, 781, 783, 784, 787 | 18 → 18 (770 +1, 783 −1) |
| Českotěšínsko (871), MHD Český Těšín (875) | 721–723, 732–738, 745–754 | 23 → 24 (738 +1, 722 +1, 732 −1) |
| MHD Třinec (866) | 702–716 | 14 → 18 (702, 703, 708, 716 +1 each) |
| MHD Frýdek-Místek (865) | 301–318 | 28 → 30 (301 +1, 314 +1) |
| Frýdecko-Místecko (863), Frýdlantsko (864) | 341–348, 351, 358, 980, 985 | 32 → 32 |
| **Sheet (schedule need, all lines)** | | **143 → 150** |

Each +1 has an owner check with the cheaper option: 770, 738, 722, 702, 703, 708, 716, 301 and 314. The old 784 check is
gone: 784 is exact at two buses now. The 706 check carries the new numbers. A new check for 358 offers listing its shift
trips with 358 Steel (Step 8, one bus less), and one for 980 puts its passing every-120 row (same seven buses, 8 typed
values) against the kept every 30. 731, 302 Tesco and 985 are unchanged.

## Summary

| Line | Published (v5) | Step 4 | Now | Buses |
|---|---|---|---|---|
| 764 | every 90, Třinec :05 / :35 (13:35, 15:05) | 15:05 slot empty | every 180, Třinec 13:35 and 14:20, exact | 1 → 1 |
| 766 | every 90, Třinec :05 / :35 (16:35) | 16:35 slot empty (real 15:40) | every 120, Třinec 15:40 | 1 → 1 |
| 770 | every 60, station :44 / Paseky :00 | 14:44, 14:00 and 15:00 slots empty | every 180, two slots each way, exact (station 13:45, 14:51; Paseky 13:30, 15:05) | 1 → 2 |
| 771 | every 90, station 13:50 / Nýdek 15:00 | 15:20 and 15:00 slots empty | every 120, station 13:50 / Nýdek 14:00, Setinka trips left out | 1 → 1 |
| 771 Hluchová | every 480, 12:25 / 12:47 | passes | unchanged | 1 → 1 |
| 781 | every 60, Návsí :03 / Šance :30 | 15:03 and 14:30 slots empty | every 120, Návsí 14:03 + 14:43 / Šance 14:35 + 15:30, exact, Hrčava trips left out | 2 → 2 |
| 781 Hrčava | every 180, Jablunkov 15:00 / Hrčava 14:06 | passes | unchanged | 1 → 1 |
| 783 | every 30, Třinec :05 / :35, Bukovec :12 / :42 | 1 of 4 and 0 of 4 slots filled | every 180, three slots each way, exact (Třinec 13:28, 14:15, 15:13; Bukovec 13:32, 14:17, 15:17), through trips to Bukovec only | 4 → 3 |
| 783 Písečná, 783 Ski areál | every 90 / every 480 | pass | unchanged | 1 + 1 |
| 784 | every 60, Návsí :55 / Přelač :19 | 15:55, 15:19 and 16:19 slots empty | every 180, two slots each way, exact (Návsí 14:55, 16:00; Přelač 14:30, 16:25) | 2 → 2 |
| 787 | every 90, Paseky 14:10 / Jablunkov 14:50 | Paseky slots 21 min off (14:10, 15:40 empty) | every 120, Paseky :58 odd hours / Jablunkov 14:50 | 1 → 1 |
| 787 Třinec | every 90, Třinec 14:59 / Paseky 15:24 | passes | unchanged | 1 → 1 |
| 732 | every 60, Třinec :55 (Těšín :15) / Havířov :02 | 13:55 slot empty; both Havířov slots empty, 5 departures for 2 slots | every 180, Třinec 13:25 14:55 (Těšín 13:45 15:15) / Havířov 13:52 14:27, exact; from Havířov FEWER by design | 3 → 2 |
| 733 | every 90, Těšín 13:45 / U Stonávky 14:50 | all three window slots empty | every 120, Těšín 14:50 / U Stonávky 15:29, exact | 1 → 1 |
| 734 | every 90, Třinec 14:12 / Těšín 14:35 | 3 of 4 slots empty | every 180, Třinec 14:20 15:30 / Těšín 15:05 16:05, exact | 1 → 1 |
| 735 | every 60, Těšín :50 / Těrlicko :35 | Těrlicko 15:35, 16:35 empty (one real departure, 16:52) | every 96, Těšín 16:50 / Těrlicko 16:52, exact | 2 → 2 |
| 736 | every 60, Těšín :20 / Chotěbuz :40 | all four slots empty | every 160, Těšín 13:35 14:25 / Chotěbuz 13:55 14:45, exact | 1 → 1 |
| 738 | every 30, Slovenská :17 :47 / Karviná :12 :42 | 2 of 4 slots empty each way | every 90, four slots each way (6/6 and 4/5 exact) | 3 → 4 |
| 745 | every 60, Lhotka :31 / Hnojník :12, Třanovice trips counted in | 3 of 4 slots empty | every 120, Lhotka 14:16 / Hnojník 15:37, Třanovice trips separated; Hnojník FEWER by design | 1 → 1 |
| 745 Třanovice | every 90, Lhotka 14:51 / Třanovice 15:36 | 15:36 empty | every 120, Lhotka 15:31 / Třanovice 16:06, exact | 1 → 1 |
| 747 | every 90, Těšín 16:15 / Střítež 16:50 | both empty | every 60, Těšín :45 / Střítež :15, exact | 1 → 1 |
| 748 | every 90, Střítež 16:44 / Řeka 16:26 | both empty | every 120, Střítež 16:11 17:11 / Řeka 15:40 16:30, exact | 1 → 1 |
| 750 | every 60, Třinec :30 / Frýdek :40 | 3 of 4 slots empty; 5 Frýdek departures for 2 slots | every 180, Třinec 13:50 14:20 / Frýdek 14:50 15:40, exact; Frýdek FEWER by design | 2 → 2 |
| 754 | every 60, Třinec :25 / Těšín :20 | 15:25, 15:20 empty; 4 Třinec departures for 2 slots | every 144, Třinec 13:45 14:22 15:30 / Těšín 13:40 14:20 15:10, exact | 2 → 2 |
| 721 | every 40 (14:11, 14:51, 15:31) | 14:11 empty (14:15) | every 120, 14:15 14:51 15:31, exact | 1 → 1 |
| 721 Mosty | every 60, station :55 / Antoníček :19 | 14:55 and 15:19 5 min off 15:00 / 15:24 | every 144, station 13:55 15:00 / Antoníček 14:19 15:24, exact | 1 → 1 |
| 722 | every 40 (13:35, 14:15, 14:55) | 2 of 3 slots empty; 5 trips | every 180, five slots, exact | 1 → 2 |
| 723 | every 60, station :35 / Horní Žukov :00 | 16:35 slot 4 min off 16:39 | every 60, station :37 / Horní Žukov :00 | 1 → 1 |
| 702 | every 40, Kanada :05 (13:25, 14:05, 14:45) / bus station :30 (13:10, 13:50, 14:30) | 14:45 and 14:30 slots empty; 3 slots for 7 departures back | every 90, four slots each way, exact on 10 of 12 | 1 → 2 |
| 703 | every 90, bus station 13:18 / PZ 13:42 | 14:48 and 13:42 slots empty | every 480 (shift line), bus station 13:18, 13:30 / PZ 14:03, 14:08 | 1 → 2 |
| 704 | every 60, bus station :45 / Podlesí :04 | 13:45, 14:04, 15:04 slots empty | every 120, bus station 13:35, 14:45 / Podlesí 13:52, 15:00 | 1 → 1 |
| 706 | every 60, bus station :35 / Kojkovice :00 | 13:35, 13:00, 14:00 slots empty | every 120, bus station 13:40, 14:35 / Kojkovice 13:05, 13:55 | 1 → 1 |
| 706 Osůvky | every 60, bus station :35 / Osůvky :05 | 14:35, 14:05 slots empty | every 120, bus station 13:35, 14:30 / Osůvky 13:05, 14:01 | 1 → 1 |
| 707 | every 60 :35 | 2 slots for 4 departures (the short circle counted) | every 60 :35, short circle off the row | 1 → 1 |
| 708 | every 60, bus station :45 / Kamionka :09 | 2 slots for 4 departures back | every 30, bus station :15 / Kamionka :09, model hour 15:10–17:10 | 1 → 2 |
| 712 | every 60, station :40 / Tyra :03 | 14:40 slot empty | every 120, station 14:22, 15:40 / Tyra 15:00, 15:44 (pila 15:02, 15:46) | 2 → 2 |
| 712 Kozinec | every 240, 14:35 / 14:58 | passes | unchanged | 1 → 1 |
| 714 | every 90, bus station 13:37 / ves 13:00 | 14:30 slot empty | every 120, bus station 13:37, 14:30 / ves 13:00, 14:03 | 1 → 1 |
| 715 | every 30 :20 / :50 | 13:20 and 14:20 slots empty | every 60 :10 / :50, model hour 16:00 | 2 → 2 |
| 716 | every 90, bus station 15:48 / Guty 16:30 | every slot empty | every 120, bus station 14:20, 15:35 / Guty 16:10, 16:55 | 1 → 2 |
| 301 | every 30, :03 / :13 both ends | Marlenka 6 of 8 slots (its :13 are :23 from 14:23) | every 60, Riviéra :03 :13 :33 :43, Marlenka :03 :23 :33 :43, exact | 4 → 5 |
| 302 | every 30, skládka :12, Riviéra :27, model 15:30–17:30 | Riviéra 17:27 slot empty (last trip 16:57) | same values, model hours 15:00–17:00 (anchor 15:30) | 3 → 3 (+1 Tesco) |
| 303 | every 60 :35 / :27; Hodoňovice :59 / :52, model 15:30–17:30 | Baška 0 of 2, Kamenec 1 of 2 (back pattern ends 15:27 / 15:52) | same values, model hours 14:00–16:00 (anchor 14:30) | 2 + 2 → 2 + 2 |
| 305 | every 60, station :08, Sklenov :59 | 17:08 slot 4 min off 17:12 | every 120, station 16:08 / 17:12 (even :08, odd :12), Sklenov :59 | 2 → 2 |
| 308 | every 90 (Záhoří 16:27, poliklinika 15:58 / 17:28) | both legs 1 slot empty | every 120, Záhoří :57 / poliklinika :28 on the odd hours | 1 → 1 |
| 308 Mitrovice | every 180 (poliklinika 15:04, Mitrovice 14:01 / 17:01) | 17:01 slot empty (IRREGULAR) | every 480 on the real round 13:19 / 14:01 | 1 → 1 |
| 310 | every 40 (14:20, 15:00, 15:40 …) | 1 of 3 | every 30 at :00 / :30 | 1 → 1 |
| 311 | every 30, Riviéra :23, U kříže :12 | U kříže 14:12 slot empty (3 of 4) | every 60, Riviéra :23 :53, U kříže :03 :42 | 3 → 3 |
| 312 | every 60, station :35, Brušperk :20 | station 2 slots for 4 trips; 14:20 slot empty | every 96, station 14:35 / 15:35 (13:59), Brušperk 14:47 / 15:20, back read at poliklinika | 2 → 2 |
| 313 | every 120, station 14:38 / Nošovice 14:10 | 14:38 slot empty | every 120, station 13:31, Nošovice 14:10 | 1 → 1 |
| 314 | every 240, station 14:44, Janovice 13:45 (station trips only) | 14:44 slot empty (IRREGULAR) | every 120 read at Baška station, two slots each way | 1 → 2 |
| 316 | every 90, poliklinika 15:42, centrum 16:15 | 17:12 slot empty | same values, own model hours 14:00–16:00 (sim window) | 1 → 1 (+1 Riviéra) |
| 318 | every 60, poliklinika :52, Ondráš :11 | 14:52 slot empty | every 240, poliklinika 13:50 / 14:58, Ondráš 14:10 / 15:10 | 2 → 2 |
| 351 | every 60, Ostrava :43 / Lipové :16 | Lipové 16:16, 17:16 slots empty (the one real 15:31 is a Bebek trip) | every 120, Ostrava 13:43 / 15:43 (odd hours), Lipové 16:26 (even hours); Bebek trips out of the main row | 3 → 3 (351 Bebek 2 → 2, unchanged) |
| 358 | every 180, Krytý bazén 13:01 / Hyundai 14:25 | 16:01 slot empty (IRREGULAR) | every 480, Krytý bazén 13:03 / Hyundai 14:25, exact all day; Steel trips out of the main row | 1 → 1 (358 Steel unchanged) |
| 980 | every 30, Ostrava :23 / Rožnov :05 | out 13:53 slot empty (3 of 4); back FEWER (6 real with the Frenštát starts, 4 slots) | same typed values; back read at Rožnov (passes); out approximate | 7 → 7 |
| 985 Rožnov | every 120, Ostrava :53 (even) / Rožnov :15 (odd) | Rožnov 17:15 slot empty | every 180, Ostrava 13:53 / 16:53, Rožnov 16:35 / 19:35 | 2 → 2 |
| 985, 985B | burst rows (owner check) | pass | unchanged | 2 + 2 |
| 341 | every 90, Frýdlant 16:34 / Janovice 17:00 | 13:34, 15:04, 14:00 slots empty | every 120, Frýdlant 14:19 (even) / Janovice 15:00 (odd) | 1 → 1 |
| 343 | every 90, Frýdlant :20/:50 pattern / Kněhyně 16:05 | Kněhyně 16:05 empty (real 15:48 is the Podolánky bus) | model hour 14:00 (hand); every 80, Frýdlant 14:10 / Kněhyně 14:35; Podolánky trips out of the main row | 1 → 1 (343 Podolánky unchanged) |
| 344 | every 60, Frýdlant :05 / Ondráš :20 | 14:05, 15:05, 14:20 empty | every 120, Frýdlant 14:30 + 15:10, Ondráš 13:20 + 14:10; Hyundai trips out of the rows | 2 → 2 |
| 345 | every 60, Frýdlant :55 / Malenovice :25 (model hour 14:00) | 13:55, 14:55, 14:25 empty | model hour 16:00 (hand); same typed values, exact; Hutě trips out of the main row | 1 → 1 (345 Hutě unchanged) |
| 346 | loop every 60 at :52 | 14:52 empty | every 90, 13:54 + 14:22 (two slots) | 1 → 1 |
| 347 | every 60, Frýdlant :30 / transformátor :57 | Frýdlant 14:30 empty (real 14:25) | every 120, Frýdlant 14:25 + 15:30, transformátor :57 (two slots) | 1 → 1 |
| 348 | every 60, Frýdlant :53 / Bílá :16 | Bílá 14:16 empty (real 14:31) | every 120, Frýdlant :53 (two slots), Bílá 14:31 + 15:16 | 3 → 3 |
| **Sheet** | | | | **143 → 150** |

## Jablunkovsko–Třinecko (861): 764, 766, 770, 771, 781, 783, 784, 787

Rate test (added after the first pass: Step 4's ±1 must not halve a line): per direction, the pattern's slots in 13:00–18:00 are within ±1 of the real departures there (variant trips of another row and outstation extras excepted). Slots / real, 13:00–18:00: 764 4/3; 766 3/3; 770 4/5 and 3/3; 771 3/4 and 2/2 (the Setinka trips are 771 Hluchová's); 781 4/4 and 5/4; 783 5/6 and 5/5; 784 4/4 and 4/5; 787 3/4 and 2/2. Ranking among the candidates that pass both: (1) need no higher than the published need (where nothing passes there, the lowest passing need, with the cheaper option on the owner checks: 770); (2) most exact on the window's real departures; (3) fewest typed values; (4) most exact over the day; (5) fewer buses; (6) divisors of 60; (7) worst deviation. Buses are never cut for a worse fit.

Step 5b at the hubs (live map 20 Oct, 13:00–17:30): the Jablunkov-branch buses change line at Třinec AS all afternoon (783 ↔ 771, 764 ↔ 787, 784 → 770, 769 → 764 …; the live map shows 50+ changes), as on the HKO Frýdek-Místek corridor, so one Simutrans line per real line is kept and pooling is the owner's option. Per line the counts at Třinec AS are close to balanced (783 in 8 / out 9, 764 4 / 4, 771 3 / 3, 787 3 / 3); 766 brings 5 in and sends 2 out (its Záolší trips end there). Out of Třinec, 783 sends a bunch 13:00–15:13 into the valley, and those buses stay there for the Návsí / Jablunkov – Bukovec shorts (below).

### 764 Třinec – Vendryně – Karpentná – Třinec (loop)

- **(a) Core point:** Třinec, autobusová stanice (loop). Model hours 13:30–15:30.
- **(b) Day:** 6:30, 8:35, 10:35, 12:35, **13:35, 14:20**, 16:35, 18:35 (every 2 h at :35, with 13:35 and 14:20 in the afternoon); 14:40 runs to Záolší only.
- **(c) Step 4** (window 2 real): published every 90 (13:35, 15:05) 1 of 2 FAIL; every 120 13:35: 1 slot, exact 1 over the day; every 180 13:35: 1 slot, exact 3; **every 180, 13:35 + 14:20**: 2 of 2, exact, 4 exact over the day (13:35, 14:20, 16:35, 10:35).
- **(d) Simutrans line 764:** every 180, Třinec Offset 34, Also at 79 (real 13:35, 14:20; also 10:35, 11:20, 16:35, 17:20). Buses 74-1112 (13:35), 74-1117 (14:20).
- **(e) Knots:** the loop has no other core point.
- **(f) Off the pattern 12–20 h:** 12:35, 18:35 (60).
- **(g) Need:** 1 (waits 7, 97).

### 766 Třinec – Karpentná – Vendryně – Třinec (loop, the other way)

- **(a)** Třinec, autobusová stanice. Model hours 15:30–17:30.
- **(b) Day:** 9:35, 11:35, 13:35, **15:40**, 20:35, 22:30 (13:24 is a Záolší – Třinec trip passing the bus station).
- **(c) Step 4** (window 1 real): published every 90 (16:35) 0 of 1 FAIL; **every 120 15:40**: 1 of 1 exact, worst 55; every 180 15:40 the same, worst 89; every 240 worst 115; every 120 15:38 within 3 of 4 trips but 0 exact.
- **(d) Simutrans line 766:** every 120, Třinec Offset 39 (real 15:40; odd hours :40). Bus 74-1123.
- **(f) Off the pattern:** 13:24 (16), 13:35 (5); 9:35 and 11:35 are 5 min early against it too.
- **(g) Need:** 1 (wait 76).

### 770 Bystřice, žst – Paseky

- **(a) Core points:** Bystřice, železniční stanice; Bystřice, Paseky, konečná. Model hours 13:30–15:30.
- **(b) Afternoon:** station 13:10 (from Třinec), **13:45, 14:51**, 15:55, 17:45, 18:50; Paseky **13:30, 15:05**, 16:50, 18:00, 19:00 (the 14:00 from Paseky runs to Třinec without the station, so it is not on this leg). 13:00–18:00: 5 out, 3 back.
- **(c) Step 4 + rate:** published station :44 1 of 2 FAIL, Paseky :00 0 of 2 FAIL. Station hourly :48 would pass, but no hourly Paseky slot does (13:30 and 15:05 are 95 min apart). Every 120 one slot each way (station 13:45 / Paseky 15:05, 1 bus) passes Step 4 but fails the rate (station 3 slots for 5 real). Every 120 two slots each way fails the rate at Paseky (6 for 3). Passing both, all at 2 buses: **every 180, station 13:45 + 14:51 / Paseky 13:30 + 15:05** (2 of 2 each, exact; rate 4/5 and 3/3; 6 exact over the day), every 160 (4 exact), every 144 (4 exact).
- **(d) Simutrans line 770:** every 180, station Offset 44, Also at 110 (real 13:45, 14:51; also 16:45, 17:51, 10:45, 11:51), Paseky Offset 29, Also at 124 (real 13:30, 15:05; also 16:30, 18:05, 12:05). Buses on the real trips: 74-4002 (13:45), 74-1116 (13:30), 74-1126 (14:51 → 15:05).
- **(e) Knots:** model at Paseky 13:57 / 15:03 (real 14:00 / 15:01); back at the station 13:40 / 15:15, exact.
- **(f) Off the pattern 12–20 h:** station 13:10, 15:55, 17:45 (6), 18:50; Paseky 16:50 (20), 18:00 (5), 19:00. Their stops are all on this line.
- **(g) Need:** 2 (was 1; waits station 90, 71; Paseky 84, 65). Owner check: one bus every 120 (station 13:45, Paseky 15:05) at half the real rate.

### 771 Bystřice, žst – Nýdek, náměstí

- **(a) Core points:** Bystřice, železniční stanice; Nýdek, náměstí; Hluchová, Setinka. Model hours 13:50–15:50.
- **Read points:** the published row counted the Setinka trip (Třinec 14:50, station 15:10, náměstí 15:18, Setinka) as its own 15:10; it is 771 Hluchová's variant, so both main rows are now `notvia` Setinka.
- **(b) Afternoon:** station 13:05, **13:50**, 16:45, 17:45, 18:45; Nýdek **14:00, 15:10**, 18:00, 19:00 (morning 8:00, 12:00).
- **(c) Step 4:** published every 90 (station 13:50, 15:20; Nýdek 15:00) 1 of 2 and 0 of 1 FAIL. **Every 120, station 13:50 / Nýdek 14:00**: 1 of 1 and 1 slot for 2 real, exact; 5 exact over the day (Nýdek 8:00, 12:00, 14:00, 18:00 on the minute); every 180 13:50 / 14:00: 4 exact, worst 88.
- **(d) Simutrans line 771:** every 120, station Offset 49 (real 13:50, odd hours :50), Nýdek Offset 59 (real 14:00, even hours :00). The same bus as on the live map (74-1116: 13:50 out, 14:00 back, a 2-min turn).
- **(e) Knots:** náměstí 13:58 (real 13:58); back at the station 14:10 (real 14:10).
- **(f) Off the pattern:** station 13:05, 16:45, 17:45 (5), 18:45; Nýdek 15:10, 19:00.
- **(g) Need:** 1 (waits station 100, Nýdek 2). 771 Hluchová unchanged (every 480, 12:25 / 12:47).

### 781 Návsí – Jablunkov – Mosty, Šance

- **(a) Core points:** Návsí, železniční stanice; Mosty u Jablunkova, Šance, opevnění; Jablunkov AS; Hrčava. Model hours 14:10–16:10.
- **Read points:** the Hrčava trips via Šance (Návsí 10:58, 18:58; Třinec 22:23) are 781 Hrčava's, so both main rows are now `notvia` Hrčava.
- **(b) Afternoon:** Návsí 12:58, 14:03, **14:43** (the Třinec through trip, 74-1105), **16:03**, 17:03, 18:03; Šance 12:25, 13:25, **14:35, 15:30**, 17:30, 18:30. The hourly pattern has holes: no 15:03 (its bus ran the 14:43) and no 16:30 back (a Hrčava trip instead).
- **(c) Step 4 + rate:** published every 60 :03 / :30: 15:03 and 14:30 slots empty, 1 of 2 each, FAIL; every 60 cannot hold 14:43 and 16:03 (80 min apart). Every 120 one slot each way (Návsí 16:03 / Šance 15:30) fails the rate (2 slots for 4 real). Passing both at ≤ 2 buses (published 2): **every 120 two slots each way, Návsí 14:03 + 14:43 / Šance 14:35 + 15:30** (2 of 2 each, exact, 4 exact in the window; rate 4/4 and 5/4; 7 exact over the day); every 180 two slots (4 in the window, 5 over the day); every 144, every 160 (4 over the day). Every 90 one slot each way (Návsí 14:43 / Šance 15:30) passes at 1 bus but is exact on only 2 window departures and 3 over the day: not taken (no bus is cut for a worse fit).
- **(d) Simutrans line 781:** every 120, Návsí Offset 62, Also at 102 (real 14:03, 14:43: even hours :03 and :43); Šance Offset 29, Also at 94 (real 15:30 odd hours, 14:35 even hours). Plates: 7E18816 14:03 → 14:35 (2-min turn at Šance); 74-1105 14:43 → 15:30 → 16:03.
- **(e) Knots:** Jablunkov out 14:48 / 16:08 (real 14:50 / 16:08); back Jablunkov 15:00 / 15:55 and Návsí 15:03 / 15:58, exact.
- **(f) Off the pattern 12–20 h:** Návsí 12:58 (15), 17:03 (20); Šance 12:25 (10), 13:25 (5), 18:30 (5).
- **(g) Need:** 2 (waits Návsí 60, 45; Šance 4, 19). 781 Hrčava unchanged.

### 783 Třinec – Návsí – Jablunkov – Bukovec

- **(a) Core points:** Třinec AS; Návsí, nadjezd; Jablunkov AS (the knot: the way back is read there); Bukovec, škola; Písečná točna. Model hours 13:20–15:20.
- **Read points:** the published out row counted every trip Třinec → Jablunkov, so the 14:00 Ski areál trip (783 Ski areál) and the 14:18 Třinec → Písečná trip (also on 783 Písečná) were in it. Both main rows now count the trips that run through to Bukovec (`via` Bukovec, škola); the Jablunkov shorts are listed.
- **(b) Afternoon:** out of Třinec 12:05, 13:00, **13:28, 14:15, 14:35, 15:13**, 16:10, 18:18 (hourly :05 in the morning); Bukovec → Třinec **13:32, 14:17, 15:15** (Jablunkov 13:52, 14:37, 15:37), 16:37; morning 12:12, 12:32, 13:07.
- **(c) Step 4:** published every 30 (Třinec :05 / :35, Bukovec :12 / :42): 1 of 4 and 0 of 4 filled, FAIL; every 30 :15 / :17 2 of 4 each FAIL; every 60 :15 / :17 (2 buses): Třinec 2 slots for 4 real, FAIL. Passing, 3 buses: every 180 three slots (13:28, 14:15, 15:13 / 13:32, 14:17, 15:17), 7 exact over the day, worst 28; every 160 (13:28, 14:35, 15:13 / same back), 7 exact, worst 27; every 120 three slots, 6 exact. **Every 180** chosen: 3 h rather than the odd 160 (no clearer fit), and it leaves off 14:35, whose bus (74-1112) stays in the valley (Bukovec 15:37 → Návsí), not 14:15, which comes back.
- **(d) Simutrans line 783:** every 180. Třinec Offset 27, Also at 74, 132 (real 13:28, 14:15, 15:13); Bukovec Offset 31, Also at 76, 136 (real 13:32, 14:17, 15:17), timed from Jablunkov :52 / :37 / :37 (knot +20). Plates: 74-1102 13:28 → 14:17; 74-1122 14:15 → 15:15; 74-1102 15:13 → 16:37 (off); Bukovec 13:32 is 74-1124, in from Návsí 13:00.
- **(e) Knots:** out Jablunkov 13:59, 14:46, 15:44 (real 14:00, 14:50, 15:50: the later trips take 35–37 min, the median 31); back Jablunkov, Návsí nadjezd and Třinec exact.
- **(f) Off the pattern 12–20 h:** out 12:05 (8), 13:00, 14:35 (20), 16:10 (18), 18:18 (5); back 12:32 (15), 13:07 (25), 16:37 (5). The Návsí – Bukovec (13:00, 16:00, 17:05, 18:10), Jablunkov – Bukovec (14:25), Bukovec – Návsí / Jablunkov (13:50, 14:42, 15:37, 17:37, 18:37) and Třinec – Jablunkov (17:05; back 16:32, 17:32, 18:32) shorts: their stops are on 783.
- **(g) Need:** 3 (was 4; waits Třinec 11, 26, 178; Bukovec 15, 32, 2). 783 Písečná (every 90, Návsí 14:05 / Písečná 15:15) and 783 Ski areál (every 480, 14:00) pass and are unchanged.

### 784 Návsí – Dolní Lomná – Horní Lomná, Horní Přelač

- **(a) Core points:** Návsí, železniční stanice; Horní Lomná, střed (knot, the way back is read there); Horní Přelač. Model hours 14:30–16:30.
- **(b) Afternoon:** Návsí 12:55, 13:55, **14:55, 16:00**, 17:00, 18:05, 19:00; Přelač 12:25, 13:25, **14:30, 15:30, 16:25**, 17:25, 18:30. The 16:00 turns at Horní Lomná, střed and comes back at 16:28 (74-1113), counted at the knot as 16:25.
- **(c) Step 4:** published Návsí :55 1 of 2, Přelač :19 0 of 2, FAIL (the :19 was set 6 min early to save a bus). Every 60 :55 / :25 1 of 2 each FAIL; every 60 :58 / :28 passes (0 exact, 3 buses); every 60 :57 / :32 passes (0 exact, 2 buses). **Every 180, Návsí 14:55 + 16:00 / Přelač 14:30 + 16:25**: 2 of 2 each, exact, 11 exact over the day, 2 buses.
- **(d) Simutrans line 784:** every 180, Návsí Offset 114, Also at 179 (real 14:55, 16:00; also 11:55, 13:00, 17:55, 19:00), Přelač Offset 24, Also at 89 (real 16:25, 14:30; also 13:25, 17:30, 19:25). Plates: 74-1110 in at Přelač 14:29, out 14:30; 74-1113 16:00 → 16:28.
- **(e) Knots:** Horní Lomná 15:22 for the 14:55 slot (5 min off the real passing; the 16:00 slot compares 60 off only because its real trip turns there and the check uses the trips to Přelač); back Návsí 15:03 exact.
- **(f) Off the pattern 12–20 h:** out 12:55 (5), 13:55, 17:00, 18:05 (10), 19:55; back 12:25, 15:30, 17:25 (5), 18:30.
- **(g) Need:** 2 (waits 57, 57 / 56, 56), as seen. The owner check ":19 instead of :25" no longer applies.

### 787 Jablunkov – Návsí – Milíkov – Bystřice, Na Paseky

- **(a) Core points:** Bystřice, Na Paseky; Jablunkov AS; Třinec AS. Model hours 14:10–16:10.
- **(b) Afternoon:** Paseky → Jablunkov 12:56, 13:56, **14:44, 16:01**, 17:56, 19:01; Jablunkov → Paseky 12:25, **14:15, 14:50**, then 20:23. In between the buses run Košařiska and Milíkov shorts.
- **(c) Step 4 + rate:** published every 90 Paseky 14:10 / 15:40 (moved 21 min off for the shortest round) 0 of 2 FAIL; Jablunkov 14:50 passes. Every 90 Paseky 14:44 / Jablunkov 14:50 passes but needs 2 buses. Every 180 Paseky 16:01 / Jablunkov 14:50 (1 bus, exact) fails the rate at Paseky (2 slots for 4 real 13:00–18:00). **Every 120, Paseky :58 odd hours / Jablunkov :50 even hours**: 1 slot for 2 real each way, within 3 min (Paseky 13:58, 15:58, 17:58 against 13:56, 16:01, 17:56), Jablunkov 14:50 exact; rate 3/4 and 2/2; 1 bus. :58 rather than :59 (same score): closer to the three real trips together.
- **(d) Simutrans line 787:** every 120, Paseky Offset 57 (real 15:58 odd hours), Jablunkov Offset 109 (real 14:50 even hours). Bus 74-1001 on the live map: Jablunkov 14:50 → Paseky 15:19 → Košařiska → Paseky 16:01 → Jablunkov 16:38.
- **(e) Knots:** Jablunkov 16:35 (real 16:38); Paseky 15:29 (real 15:19: the 14:50 runs the shorter path).
- **(f) Off the pattern 12–20 h:** Paseky 12:56, 14:44 (46), 19:01; Jablunkov 12:25, 14:15. The Košařiska and Milíkov shorts (stops on 787).
- **(g) Need:** 1 (waits Paseky 34, Jablunkov 15). 787 Třinec unchanged (every 90, Třinec 14:59 / Paseky 15:24, passes).

### Legs left failing or FEWER by design (Jablunkovsko–Třinecko)

- None left failing. The rows with fewer slots than real departures in the window (771, 781, 787: 1 slot for 2; 784 back: 2 for 3; 783 out: 3 for 4) pass the ±1 rule and the 13:00–18:00 rate test.
- 783 (published 4 buses): no more exact option passes at ≤ 4 (four slots back would leave one of four window slots empty, 75 %). Every 160 (worst 27) ties every 180 (worst 28) on every other count; every 180 is kept by the v4 rule that the plates decide which departure falls off: 160 drops 14:15, whose bus (74-1122) comes back from Bukovec at 15:15; 180 drops 14:35, whose bus (74-1112) stays in the valley (Bukovec 15:37 → Návsí).
- 771 Hluchová and 781 Hrčava have a real departure in the window and no slot (every 480 / every 180 on their own pairs); they pass the audit (no window slot) and were not changed.

## Českotěšínsko (871) and MHD Český Těšín (875): 721–723, 732–754

Data: the sheet's trips (`data/derived/trips.json`), the whole-day reading (`data/derived/reading/<L>.txt`) and the live-map
plate chains (`chains.json`). Every candidate was built with 05_schedule's own `build()`; typed values are (real − 61) mod
every, worked out from each value. Tests per direction: Step 4 in the model window, and the rate test (the pattern's slots in
13:00–18:00 at least the real departures there − 1). Ranking of the candidates that pass both: need at most the published
need → most exact on the window's real departures → fewest typed values → most exact over the day → fewer buses → divisors
of 60 → worst deviation. A leg whose real departures are buses of other lines (outstation shape, below) is exempt and stays
FEWER by design.

**Step 5b.** The 73- buses of Transdev Český Těšín swap lines at the Český Těšín and Třinec bus stations all afternoon (one bus
works 732, 733, 734, 736 and 735 between 12:30 and 17:00). One Simutrans line per real line is kept, as on the HKO 365–369
corridor; a line's in/out imbalance at a terminal says which departures are buses going on to another line. At Havířov, Město,
station 732 has 6 arrivals and 8 departures (12:30–17:00); at Frýdek, autobusové nádraží 750 has 6 and 8, the two extra
buses coming in on 739 and 751.

Leg stops are unchanged on every line (coverage unaffected). Owner checks added: 738 (every 30, 3 buses) and 722 (every 40,
1 bus), the cheaper options that fail Step 4.

### 732 Jablunkov – Třinec – Český Těšín – Těrlicko – Havířov
- **(a) Core points:** Třinec AS; Český Těšín AS (the knot every trip passes; out trips read there); Havířov, Město, station. Model hours 13:00–15:00.
- **(b) Afternoon:** towards Havířov, Město (at Těšín) 12:15 (Těšín short), 12:35, 13:18, **13:45, 15:15**, 15:40, 17:15 (from Třinec 12:15, 13:00, 13:25, 14:55, 15:15, 16:55); from Havířov 12:30, **13:17, 13:52, 14:07, 14:27, 14:35**, 16:02, 16:30, 18:02. The Třinec – Havířov, Podlesí, Těšínská trips 14:10, 14:15, 15:50 (back 13:05, 15:15) end at the other Havířov terminus.
- **(c) Step 4:** no pattern passes both ways (5 departures from Havířov against 2 towards it): the line runs at the rate towards Havířov, the Havířov row FEWER by design. Towards Havířov: every 60 :55 (published) 1 of 2; every 90 at 13:25 2/2 exact (2 buses); **every 180 with 13:25 and 14:55 and Havířov 13:52, 14:27: 2/2 exact, Havířov 2 of 5, 2 buses**; every 120 the same fit, 3 buses. Rate 13–18 towards Havířov: 4 slots, 4 real.
- **(d) Simutrans line 732:** every 180. Třinec Offset 24, Also at 114 (real 13:25 / 16:25, 14:55 / 17:55), timed at Těšín 13:45 / 15:15; Havířov Offset 51, Also at 86 (real 13:52 / 16:52, 14:27 / 17:27). 13:25 → 14:27 is the turn of 73-0016 (in 14:23), 13:52 that of 73-0009 (in 13:20). The other Havířov departures are buses going on to other lines: 13:17 (73-0019, on as 733 from Třinec), 14:07 (73-0021, ends at Těšín, on as 734), 14:35 (73-0013, on to Jablunkov).
- **(e) Knots:** out passes Těšín at 13:45 / 15:15 (exact) and reaches Havířov 2–3 min after the real arrivals; back passes Těšín at 14:40 / 15:15 (real 14:40 / 15:07–15:20).
- **(f) Off the pattern 12–20 h:** towards Havířov 12:15, 12:58, 15:20, 16:55 (Třinec times); from Havířov 12:30, 13:17, 14:07, 14:35, 16:02, 16:30, 18:02; the Podlesí trips.
- **(g) Need:** 2 (waits Třinec 56 / 1, Havířov 57 / 2). Published 3.

### 733 Český Těšín – Těrlicko, Hradiště, U Stonávky
- **(a)** Těšín AS; U Stonávky. Model hours 13:40–15:40.
- **(b)** Out 13:15, **14:50**, 16:45, 18:35; back 12:41, **13:41, 15:29**, 17:10, 19:32. Kaménka shorts 13:40, 14:35; Třinec shorts.
- **(c)** Published every 90: 0 of 2 and 0 of 1. Every 96 fails back (15:17 slot, 15:29 real). **Every 120, Těšín 14:50 / U Stonávky 15:29:** 1/1 and 1/2, exact, 1 bus (worst 55); 14:50 / 13:41 the same counts, worst 60; every 144 / 160 / 180 worse. Rate 13–18: 2 slots for 3 out, 3 for 3 back.
- **(d)** every 120: Těšín Offset 109 (real 12:50, 14:50, 16:50), U Stonávky Offset 28 (real 13:29, 15:29, 17:29).
- **(e)** U Stonávky reached 15:10 (exact); Těšín 15:51 (1 min).
- **(f)** Out 13:15 (25), 16:45 (5), 18:35 (15); back 12:41, 13:41 (12), 17:10 (19).
- **(g)** 1 (waits Těšín 59, U Stonávky 19).

### 734 Třinec – Český Těšín (short trips)
- **(a)** Třinec AS; Těšín AS. Model hours 14:10–16:10.
- **(b)** Třinec 12:40, **14:20, 15:30**, 17:30, 19:10; Těšín 13:05, 14:05, **15:05, 16:05**.
- **(c)** Published every 90: 0/2 and 1/2. No hourly minute takes 14:20 and 15:30. One slot every 120 (15:30 / 16:05): passes Step 4 but only 2 slots in 13–18 for 4 Těšín departures (rate fails). **Every 180, two slots each way:** 2/2 exact both ways, rate 3 for 3 and 3 for 4, 1 bus; every 144 / 160 the same in the window, fewer exact over the day.
- **(d)** every 180: Třinec Offset 79, Also at 149 (real 14:20 / 17:20, 15:30 / 12:30 / 18:30); Těšín Offset 4, Also at 124 (real 13:05 / 16:05, 15:05 / 12:05 / 18:05).
- **(e)** Těšín reached 14:39 / 15:49 (0–1 min), Třinec 15:24 / 16:24 (1–2 min).
- **(f)** Třinec 12:40, 17:30 (10), 19:10; Těšín 14:05 (buses from and to 732, 733, 750). 73-0021 turns at Třinec 15:26 → 15:30.
- **(g)** 1 (waits Třinec 4 / 54, Těšín 15 / 25).

### 735 Český Těšín – Těrlicko
- **(a)** Těšín AS; Těrlicko, střed. Model hours 15:30–17:30.
- **(b)** Out 13:00, 14:50 (from Třinec), **15:50, 16:50**, 18:55; back 12:35, 13:35, 15:09, **16:52**, 17:38, 19:25.
- **(c)** Published every 60: out 2/2, back 0 of 2 (one real departure in the window, so no hourly back slot can pass, and the out row has to change with it). Every 120 at 15:50 / 16:52: 1 bus, but 2 slots in 13–18 for 4 real each way (rate fails). **Every 96, Těšín 16:50 / Těrlicko 16:52:** 1/2 and 1/1 exact, rate 3 for 4 both ways, 2 buses as published; every 90 at 16:50 / 16:52: the same in the window, fewer exact over the day.
- **(d)** every 96: Těšín Offset 85 (real 13:38, 15:14, 16:50, 18:26), Těrlicko Offset 87 (real 13:40, 15:16, 16:52, 18:28).
- **(e)** Těrlicko reached 17:16 (exact), Těšín 17:18 (1 min).
- **(f)** Out 12:15, 13:00, 14:50, 15:50 (36; its bus, 73-0031, comes back at 16:52), 18:55; back 12:35, 13:35 (5), 15:09 (7), 17:38, 19:25.
- **(g)** 2 (waits 69, 71).

### 736 Český Těšín – Chotěbuz
- **(a)** Těšín AS; Chotěbuz, hájenka. Model hours 13:30–15:30.
- **(b)** Out **13:35, 14:25, 14:55**, 16:20, 17:20, 18:55; back **13:55, 14:45, 15:20**, 16:40, 17:40, 19:20.
- **(c)** Published every 60: 0/2 both ways. **Every 160, Těšín 13:35, 14:25 / Chotěbuz 13:55, 14:45:** 2/3 each, 4 of 4 exact, rate 4 for 5 both ways, 1 bus, 5 exact over the day; every 160 at 13:35 / 14:55 and 13:55 / 15:20: the same in the window, rate 3 for 5 back; every 120 three slots: 6 of 6 exact, 2 buses.
- **(d)** every 160: Těšín Offset 4, Also at 114 (real 14:25 / 17:05, 13:35 / 16:15 / 18:55); Chotěbuz Offset 24, Also at 134 (real 14:45 / 17:25, 13:55 / 16:35). The two rounds of 73-0003.
- **(e)** Chotěbuz reached 13:53 / 14:43, Těšín 14:14 / 15:04 (0–1 min).
- **(f)** Out 12:17, 14:55 (30; 73-0031), 16:20 (5), 17:20 (15); back 12:35, 15:20, 16:40, 17:40, 19:20.
- **(g)** 1 (waits Těšín 11 / 71, Chotěbuz 1 / 1).

### 738 Svibice, Slovenská – Karviná, Fryštát
- **(a)** Slovenská; Karviná, autobusové nádraží. Model hours 13:50–15:50.
- **(b)** Slovenská 13:22, **13:52, 14:17, 14:37, 14:57, 15:22, 15:47**, then 16:17, 16:47, 17:10; Karviná 13:12, 13:29, **13:57, 14:34, 14:52, 15:12, 15:39**, then 16:12, 16:32, 17:09. Every 30 at :17 / :47 and :12 / :42 runs 8:00–13:00.
- **(c)** Published every 30: 2 of 4 filled each way. With the model hour moved to 15:30, 16:00, 16:30 or 17:00 no every 30 or every 60 passes either (not a window-edge effect). No pattern passes at 3 buses. **Every 90, four slots each way:** Slovenská 6/6 exact, Karviná 5 slots for 5, 4 exact (the 14:09 slot; 13:57 is 12 off), 4 buses, 19 exact over the day; every 120 with five slots: the same window exact, one more value each way; every 96 / 72: fewer exact, 4–6 buses.
- **(d)** every 90: Slovenská Offset 6, Also at 26, 51, 76 (real 14:37, 14:57, 13:52 / 15:22, 14:17 / 15:47); Karviná Offset 3, Also at 21, 41, 68 (real 14:34, 14:52, 15:12, 15:39).
- **(e)** Karviná reached on every real arrival (0 min); Slovenská 0–3 min except the 14:09 slot.
- **(f)** Slovenská 12:17, 13:22, 16:17, 16:47, 17:10, 18:17, 19:47 (5–10 min); Karviná 12:07, 13:12, 13:29, 13:57, 16:12, 16:32, 17:42, 19:12 (5–12 min).
- **(g)** 4 (waits Slovenská 14/21/21/14, Karviná 1/8/8/1). Every 30 needs 3: owner check.

### 745 Komorní Lhotka – Hnojník (– Třanovice)
- **(a)** Lhotka, konečná; Hnojník, obch.stř.; Třanovice, křižovatka. Model hours 14:10–16:10. The main rows now leave out the Třanovice trips (`notvia`), which were also counted in them.
- **(b)** Lhotka → Hnojník only: 12:21, **14:16**, 17:31, 18:31, 19:11, 20:11; Hnojník → Lhotka: 13:07, 14:02, **14:35, 15:05, 15:37**, 18:12, 18:57, 19:37, 20:47. Lhotka → Třanovice 13:21, **14:51, 15:31**, 16:31; Třanovice → Lhotka 12:01, **16:06**, 17:06 (and the Třanovice → Hnojník shorts 13:34, 15:11).
- **(c)** Published 745 every 60: 1 of 2, 0 of 2; 745 Třanovice every 90: out 1/1, back 0/1. Main: 1 out against 3 back; the extra Hnojník departures are buses of other rows (15:05: 73-0022, in on 750's short from Třinec; 15:37: 73-0028 back from Třanovice by the 15:11 short), so the Hnojník row is FEWER by design. **Every 120, Lhotka 14:16 / Hnojník 15:37:** 1/1, 1 bus, 3 exact over the day (Hnojník 14:35: 2). Třanovice: **every 120, Lhotka 15:31 / Třanovice 16:06:** 1/2 and 1/1 exact, 1 bus; 14:51 / 16:06 the same counts but its bus returns by the Hnojník short (wait 55). Rate 13–18: 2 for 2 (Lhotka), 3 for 4 and 2 for 2 (Třanovice).
- **(d)** 745 every 120: Lhotka Offset 75 (real 14:16, 16:16), Hnojník Offset 36 (real 13:37, 15:37). 745 Třanovice every 120: Lhotka Offset 30 (real 13:31, 15:31), Třanovice Offset 65 (real 14:06, 16:06).
- **(e)** Hnojník passed 14:29 (1 min) and 15:44 / 16:12 (exact); Lhotka 15:49 (2 min), 16:23 (exact).
- **(f)** Main out 12:21, 17:31–20:11; back 13:07, 14:02, 14:35, 15:05, 18:12–20:47. Třanovice out 13:21, 14:51, 16:31; back 12:01, 17:06.
- **(g)** 1 + 1 (waits Lhotka 25, Hnojník 69; Lhotka 68, Třanovice 15).

### 747 Český Těšín – Střítež
- **(b)** Out 14:45, **15:45, 16:45**; back 13:54, 15:20, **16:15, 17:15**. Model hours 15:30–17:30.
- **(c)** Published every 90: 0/1 both. **Every 60 :45 / :15:** 2/2 exact each way, 1 bus, 5 exact over the day; every 144 / 160 / 180 with two slots each way: the same in the window, more values.
- **(d)** every 60: Těšín Offset 44 (real :45), Střítež Offset 14 (real :15).
- **(e)** Střítež 16:05 / 17:05 (exact); Těšín 16:35 / 17:35 (1 min). **(f)** Out 12:35; back 13:54, 15:20 (5). **(g)** 1 (waits 11, 10).

### 748 Střítež – Řeka
- **(b)** Střítež 15:14, **16:11, 17:11**, 19:01; Řeka **15:40, 16:30**, 17:35. Model hours 15:30–17:30. One bus (73-0027) shuttles from 15:14.
- **(c)** Published every 90: 0/1 both. No hourly Řeka minute takes 15:40 and 16:30; every 48 fills 2 of 3. **Every 120, two slots each way:** 2/2 exact each way, 1 bus, worst 29; every 180 / 360 the same in the window, worst 65+.
- **(d)** every 120: Střítež Offset 10, Also at 70 (real 15:11 / 17:11 and 16:11: the hourly :11), Řeka Offset 39, Also at 89 (real 15:40 / 17:40 and 16:30).
- **(e)** Řeka 16:26 / 17:26 (exact); Střítež 15:54 / 16:44 (1 min). **(f)** 17:35 (5), 19:01, the Třinec – Řeka trips. **(g)** 1.

### 750 Třinec – Hnojník – Dobrá – Frýdek-Místek
- **(a)** Třinec AS; Frýdek, autobusové nádraží. Model hours 13:50–15:50.
- **(b)** Out of Třinec 12:35, 12:50, 13:25, **13:50, 14:20**, 16:45, 17:30, 18:30; out of Frýdek 12:25, 13:18, **14:20, 14:35, 14:50, 15:35, 15:40**, 16:40, 17:40, 18:30.
- **(c)** No pattern passes both ways (2 against 5): the line runs at Třinec's rate, the Frýdek row FEWER by design. Every 60 cannot take both Třinec departures (30 min apart). One slot every 120 (13:50 / 14:50): 1 bus, but 3 slots in 13–18 for 5 real (rate fails). **Every 180, Třinec 13:50, 14:20 / Frýdek 14:50, 15:40:** 2/2 exact, rate 4 for 5, 2 buses as published; every 144 the same in the window, fewer exact over the day; every 120 with two slots: 3–4 buses.
- **(d)** every 180: Třinec Offset 49, Also at 79 (real 13:50 / 16:50, 14:20 / 17:20); Frýdek Offset 109, Also at 159 (real 14:50 / 17:50, 15:40 / 12:40 / 18:40). The rounds of 73-0026 (13:50 → 14:50) and 73-0006 (14:20 → 15:40). The extra Frýdek departures are buses that came in on 739 and 751: 13:18 (73-0007), 14:20 (73-0001), 15:35 (73-0005), 16:40 (73-0038); 14:35 is 73-0024 (on as 754).
- **(e)** Frýdek reached 14:44 / 15:14 (0 / 10 min, the 14:20 trip runs longer); Třinec 15:43 / 16:33 (10 / 0 min: the median running time includes the Jablunkov trips).
- **(f)** Out 12:35, 12:50, 13:25, 16:45 (5), 17:30 (10), 18:30; back 12:25, 13:18, 14:20, 14:35, 15:35 (5), 16:40, 17:40 (10), 18:30.
- **(g)** 2 (waits Třinec 73 / 53, Frýdek 26 / 6).

### 754 Třinec – Ropice – Český Těšín
- **(b)** Třinec 13:10, **13:45, 14:15, 14:22, 15:30**, 16:15, 17:25; Těšín 12:55, **13:40, 14:20, 15:10**, 16:10, 17:20. Model hours 13:40–15:40. Each trip is a different bus going on to another line.
- **(c)** Published every 60: 2 slots for 4 Třinec departures, 15:25 and 15:20 empty. Every 180 with three slots (13:45, 14:15, 15:30): exact, but 5 slots in 13–18 for 7 Třinec departures (rate fails). **Every 144, three slots each way:** 3/4 and 3/3, 6 of 6 exact, rate 7 for 7 and 6 for 5, 2 buses; every 120 three slots: 3 buses.
- **(d)** every 144: Třinec Offset 5, Also at 44, 81 (real 15:30 / 13:06, 13:45 / 16:09, 14:22 / 16:46); Těšín Offset 39, Also at 79, 129 (real 13:40 / 16:04, 14:20 / 16:44, 15:10 / 12:46 / 17:34).
- **(e)** Těšín 14:13 / 14:50 / 15:58 (0–6 min); Třinec 14:09 / 14:49 / 15:39 (exact). **(f)** Třinec 12:15, 13:10 (4), 14:15 (7), 16:15 (6), 17:25, 18:25; Těšín 12:10, 12:55, 16:10 (6), 17:20, 18:20, 19:40. **(g)** 2.

### 721, 721 Mosty, 722 (MHD Český Těšín circles)
- **(a)** Český Těšín, station (both circles); Mosty, osada Antoníček. Model hours 721 13:40–15:40, 722 13:20–15:20.
- **(b)** 721: 12:46, 13:25, **14:15, 14:51, 15:31**, 15:50, 17:14. 721 Mosty: station 12:55, **13:55, 15:00**, 16:26; Antoníček 13:19, **14:19, 15:24**, 16:44. 722: 12:21, **13:22, 14:01, 14:25, 14:55, 15:15**, 16:05, 16:35, 18:15.
- **(c)** 721: published every 40 2 of 3 (14:11 slot); every 40 at :13 / :53 / :33 3/3 within 2, 0 exact; **every 120 three slots 3/3 exact, 1 bus** (worst 19; 144 / 160 / 180 the same counts, worst 32–50). 721 Mosty: published every 60 :55 / :19 both 1 of 2; every 60 :58 / :22 2/2 within 3, 0 exact; every 120 two slots exact but 2 buses (the bus is back at the station at 15:55, too late for the next 15:55); **every 144 two slots 2/2 exact both ways, 1 bus** (worst 24; 160 / 180 worst 46–55). 722: published every 40 1 of 3; no 1-bus pattern holds five trips with 14:55 and 15:15 20 min apart; **every 180 five slots 5/5 exact, 2 buses**; every 144 / 160 / 240 five slots: fewer exact over the day; every 90 four slots: 4 exact.
- **(d)** 721 every 120: Offset 30, Also at 74, 110 (real 15:31, 14:15, 14:51). 721 Mosty every 144: station Offset 54, Also at 119 (real 13:55 / 16:19, 15:00 / 17:24), Antoníček Offset 78, Also at 143 (real 14:19 / 16:43, 15:24 / 13:00), back empty. 722 every 180: Offset 21, Also at 60, 84, 114, 134 (real 13:22, 14:01, 14:25, 14:55, 15:15).
- **(e)** Circles exact at the station; 721 Mosty back at the station 14:42 / 15:47 (exact against the real returns).
- **(f)** 721 12:46 (5), 13:25 (6), 15:50, 17:14, 19:59; 721 Mosty 12:55, 12:19, 13:19, 16:26 (7); 722 12:21 (6), 16:05, 16:35.
- **(g)** 721 1, 721 Mosty 1, 722 2 (was 1; every 40 with one bus is on the owner checks).

### 723 Český Těšín, station – Horní Žukov
- **(b)** Station 14:35, **15:35, 16:39**, 18:53; Horní Žukov 15:00, **16:00, 17:02**, 18:23. Model hours 15:30–17:30.
- **(c)** Published: station :35 1 of 2 (16:39 4 min off), Horní Žukov :00 2/2 (passes, kept). **Station :37:** 2/2 within 2, 1 bus. Every 180 with two exact slots each way also passes at 1 bus but rewrites the passing Horní Žukov row and turns an hourly line into a long multi-slot row, so not taken.
- **(d)** every 60: station Offset 36 (real :37), timed so the bus passes the bus station at :44; Horní Žukov Offset 59 (real :00).
- **(e)** Bus station 15:44 / 16:44 against 15:42 / 16:46. **(f)** 18:53, 18:23, 19:15. **(g)** 1.

### Failing legs left as they are, with why
- 732 from Havířov, 745 from Hnojník, 750 from Frýdek: FEWER by design (2, 1 and 2 slots for 5, 3 and 5 real departures in the window): each line runs at the rate of its other direction, and the extra departures are buses going on to other lines or a variant's bus (plates above). No line here is left approximate or IRREGULAR.
- 748's Střítež row is the hourly :11 written as two values on every 120 (05_schedule has one interval per Simutrans line, so it cannot be folded to every 60 there).

## MHD Třinec (866): 702–716

Hub: Třinec, autobusová stanice (with Třinec žst and Sosna nemocnice). **Step 5b:** the live map shows buses changing line at
the bus station all afternoon (13:00–17:30: 50 line changes among 702–716, 732–735, 750–754, 763–787 on 20 Oct, e.g.
1TE3305 702 → 704 → 709, 71-1153 708 → 702 → 706 → 704, 2TE1601 716 → 702 → 716). As on the HKO Frýdek-Místek corridor
(365–369), one Simutrans line per real line is kept; pooling the Třinec town buses would be the owner's choice. The in/out
counts at the bus station (708 +4, 716 +1, 703 −1 …) come from trips that start or end at the station or the Kanada stand,
not from buses piling up: every line below is balanced on its own pattern.

**How the candidates were ranked** (the sheet-wide rule, final form of 25 Oct): each direction must pass Step 4 and keep
the real rate: its slots in 13:00–18:00 are at least the real departures there − 1 (a lower bound: the pattern stands for the
peak, so it keeps the peak rate when service thins later), and a window with two or more departures is not halved. Then:
need at most the published need, most exact on the window's departures, fewest typed values, most exact over the day,
fewer buses, divisors of 60 (an odd interval only where clearly better, method Step 0), smallest worst deviation. Where no
passing option keeps the published need, the lowest passing need is taken and the cheaper option goes on the owner checks
with its bus delta (702, 703, 708, 716). Read points come first, each with its reason: variants with no stop of their own
come off the main row (706, 707), and the model hour is set by hand only where the line's own pattern runs elsewhere (708,
715). A turn under 3 min counts only where the real timetable turns that fast (Step 10): 05's lay rule takes the slots' own
gap, which makes 708 look like a one-bus line on slots 2–3 min off the timetable. 707's published row passes once its short
circle is off the row and is kept as typed.

Rate test (slots / real departures 13:00–18:00, each direction): 702 14/6, 14/8; 703 2/4, 2/2 (shift line every 480, see 703); 704 5/6, 6/4; 706 5/2, 6/3
and 706 Osůvky 5/2, 5/2 (with the combined trips, which serve both branches: 5/5, 6/5 and 5/4, 5/4); 707 5/5; 708 10/5,
10/5; 712 5/5, 6/5; 714 5/3, 5/3; 715 10/9; 716 5/4, 4/3.

Typed values below are (real − 61) mod every (every terminus is a loop).

### 702 Kanada, školy – bus station – station

- **(a) Core points:** Třinec, Kanada, školy; Třinec, autobusová stanice. Model hours 13:00–15:00.
- **(b) Afternoon:** from Kanada 12:50, **13:05, 13:25, 13:50, 14:05, 14:55**, 15:22, 18:12; from the bus station (read
  there, the station trips included) 12:40, 12:45, **13:05, 13:10, 13:35, 13:50, 14:05, 14:35, 14:55**, 15:10, 18:05. The line
  runs only 12:40–15:22 and in the morning; every trip is on a bus that comes from or goes on to another line (71-1153 708 →
  702 13:10 / 13:25 → 706; 1TD1410 709 → 708 → 702 14:35 / 14:55 / 15:10 / 15:22; 2TE1601 716 → 702 14:05 → 716).
- **(c) Step 4:** published every 40: Kanada 13:25 14:05 14:45(-), 3 slots / 5 real, 2 of 3 FAIL; bus station 13:10 13:50
  14:30(-), 3 slots / 7 real FAIL. No pattern passes with one bus. Every 45 (:20 / :37 both ends) passes, 6 / 5 and 6 / 7
  slots, 5 of 6 filled, but 2 + 3 exact in the window; **every 90 with four slots** passes, 6 / 5 and 6 / 7, 5 of 6 filled
  each way, 5 + 5 exact in the window, 17 over the day.
- **(d) Simutrans line 702:** every 90. Kanada, školy Offset 4, Also at 24, 49, 64 (real 13:05, 13:25, 13:50, 14:05; the
  14:35 slot has no trip); bus station Offset 4, Also at 24, 34, 64 (real 13:05, 13:25, 13:35, 14:05; 13:25 has no trip).
- **(e) Knots:** each end is the other's knot; model within 0–2 min of the real arrivals except 14:13 / 14:43 at the bus
  station (real 14:19 for 14:05, slower trip).
- **(f) Off the pattern 12–20 h:** from Kanada 12:50 (15), 15:22 (2, on), 18:12 (8); from the bus station 12:40 (5), 12:45
  (10), 13:10 (5), 13:50 (15), 15:10 (5).
- **(g) Need:** 2 (+1; waits Kanada 18, 23, 23, 13; bus station 2, 7, 22, 12). Owner check: one bus every 40 as before.

### 703 Bus station – Konská, PZ

- **(a) Core points:** Třinec, autobusová stanice; Třinec, Konská, PZ konečná. Model hours 13:10–15:10.
- **(b) Afternoon:** the shift change. Out (at the bus station) 12:10, **13:18, 13:21** (from Kamionka), **13:30**, 17:30;
  back from PZ 12:25, **14:03, 14:08**, 18:12 (and 14:03 to Terasa, not via the bus station). Plates: 2TE1612 13:18 → 14:08,
  1TE3309 13:30 → 14:03, 1TE3304 13:10 Kamionka → 14:03 Terasa. The other shifts: 5:14–5:30 / 6:05, 6:10; 21:23 / 22:05–22:15.
- **(c) Step 4:** published every 90: 13:18 14:48(-) 1 of 2 FAIL; PZ 13:42(-) FAIL. One slot each way fails the count (1
  slot for 3 departures out). Two slots each way, 2 slots / 3 real, 2 of 2, exact; back 2 / 2 exact, on every 120, 240 or
  480 alike in the window. Every 120 hits one more trip over the day (17:30), but it would run the works trips every 2 h all
  day. 703 is a shift line (its trips are the shift changes at 5:15, 13:20 and 21:25, back 6:05, 14:05, 22:05), and shift
  lines repeat every 480 (method Step 8; 709 on this sheet): **every 480** puts the other two shifts within 2–5 min (out
  5:18 / 5:30 against 5:14, 5:15, 5:30; 21:18 / 21:30 against 21:23, 21:26; back 6:03 / 6:08 against 6:05 / 6:10, 22:03 /
  22:08 against 22:05 / 22:10). Its out row has 2 slots in 13:00–18:00 against 4 real (13:18, 13:21, 13:30, 17:30): the
  burst is one shift change, and 17:30 is a single extra round (shift-line exception to the rate test).
- **(d) Simutrans line 703:** every 480. Bus station Offset 257, Also at 269 (real 13:18, 13:30; 5:18 / 5:30, 21:18 /
  21:30); PZ Offset 302, Also at 307 (real 14:03, 14:08; 6:03 / 6:08, 22:03 / 22:08).
- **(e) Knots:** PZ reached 13:28 / 13:40 (real 13:28 / 13:41); the bus station 14:15 / 14:20 against 14:26 / 14:33 (the
  real trips go round via Konská žst).
- **(f) Off the pattern 12–20 h:** 12:10, 12:25 (one round), 13:21 (3, on), 17:30 / 18:12 (one round), 7:49 / 7:59 in the
  morning; their stops are on the line.
- **(g) Need:** 2 (+1; waits PZ 35, 28). Owner check: one bus, the 13:30 / 14:03 round off.

### 704 Bus station – Konská, Podlesí

- **(a) Core points:** Třinec, autobusová stanice; Třinec, Konská, Podlesí konečná. Model hours 13:30–15:30.
- **(b) Afternoon:** out **13:35, 14:30, 14:45**, 16:45, 17:10, 17:45 (:45 most of the morning); back **13:52, 15:00**, 17:04,
  17:27, 18:05 (:03 in the morning). 1TE3305 13:35 → 13:52, 71-1151 14:45 → 15:00, 71-1153 14:30 out only.
- **(c) Step 4:** published every 60: 13:45(-) 14:45, 1 of 2 FAIL; Podlesí 14:04(-) 15:04(-) FAIL. **Every 120** (bus station
  odd :35 / even :45, Podlesí odd :52 / :00): 2 / 3 and 2 / 2, all filled, 4 exact in the window, 7 over the day; every 180
  the same but worst 40 against 33.
- **(d) Simutrans line 704:** every 120. Bus station Offset 34, Also at 104 (real 13:35, 14:45); Podlesí Offset 51, Also at
  119 (real 13:52, 15:00).
- **(e) Knots:** Podlesí reached 13:51 / 15:01 (real 13:51 / 14:57); the bus station 14:07 / 15:15 (real 14:10 / 15:15).
- **(f) Off the pattern 12–20 h:** 14:30 (15), 17:10 (25), 17:45 (10); back 12:07 (15), 17:04 (4), 17:27 (25), 18:05 (13).
- **(g) Need:** 1 (waits bus station 37, 19; Podlesí 1 and 3: the real bus turns 14:57 → 15:00).

### 706 and 706 Osůvky (bus station – Kojkovice / Osůvky – Borek)

- **(a) Core points:** Třinec, autobusová stanice; Kojkovice, konečná; Osůvky, konečná. Model hours 13:00–15:00.
- **Read points:** until 15:00 the two branches run separately; from 15:35 (and at 8:35, 10:45, 5:35, 11:35) one trip an hour
  runs via Osůvky and Borek to Kojkovice (:35 out, :00 / :55 back). Those combined trips were counted in both rows and spoiled
  the day statistics; they are now off both (`notvia` Osůvky / Borek on the Kojkovice row, Kojkovice on the Osůvky row). Their
  stops stay covered (Borek and Osůvky on 706 Osůvky).
- **(b) Afternoon:** Kojkovice row out 12:40, **13:40, 14:35**; back 12:00, **13:05, 13:55**, 15:00. Osůvky row out 12:45,
  **13:35, 14:30**; back **13:05, 14:01**, 14:56 (to the station). 2TE1603 runs the Kojkovice row 13:40 → 13:55 → 14:35 → 15:00;
  71-1153 and 2TE1609 the Osůvky row.
- **(c) Step 4:** published every 60 :35 / :00 and :35 / :05: Kojkovice 13:35(-) 14:35, 13:00(-) 14:00(-) FAIL; Osůvky 13:35
  14:35(-), 13:05 14:05(-) FAIL (no hourly slot catches 13:05 and 13:55). Every 120 with two slots each way passes both rows,
  2 / 2 exact each way. Kojkovice: every 120 within 1 on 5 day trips, every 180 and 240 on 4. Osůvky: every 180 within 1 on
  5, every 120 on 4, every 144 one more exact (5:53, not clearly better). One interval for both, so the bus station departures
  stay 5 min apart (every 120 + every 180 would send both at 16:35): every 120 (equal exact sum, smaller worst deviation).
- **(d) Simutrans line 706:** every 120. Bus station Offset 39, Also at 94 (real 13:40, 14:35); Kojkovice Offset 4, Also at 54
  (real 13:05, 13:55). **706 Osůvky:** every 120. Bus station Offset 34, Also at 89 (real 13:35, 14:30); Osůvky Offset 4, Also
  at 60 (real 13:05, 14:01).
- **(e) Knots:** within 0–2 min at the far ends; the bus station 9–10 min early for the second back trip (real 13:55 → 14:20
  and 14:01 → 14:27 run slower).
- **(f) Off the pattern 12–20 h:** Kojkovice 12:40 (5), 12:00 (5), 15:00 (5); Osůvky 12:45 (15); the combined trips 15:35–18:35
  and 16:00–19:00.
- **(g) Need:** 1 + 1 (waits bus station 24, 19 / 8, 9; Kojkovice 17, 2; Osůvky 21, 12). The owner check for the later
  combined shape (one line every 60, one bus) stays, with these numbers.

### 707 Circle via Horní and Dolní Líštná

- **(a) Core points:** Třinec, autobusová stanice (loop). Model hours 13:40–16:40.
- **Read points:** the short circle to Horní Líštná, státní hranice only (12:10, 14:39, 1TD1303) and the morning trips that
  skip Valovka have no stop of their own; the row now counts the full circle only (`via` Horní Líštná, Valovka).
- **(b)/(c) Step 4:** published every 60 :35: 2 slots for 13:40, 14:35, 14:39, 15:35, FEWER; with the short circle off: 14:35
  15:35 against 13:40, 14:35, 15:35, 2 / 3, both filled, PASS. Hourly :35 from 14:35 to 18:35 (17:37, 2 off).
- **(d) Simutrans line 707:** every 60, Offset 34 (real :35), unchanged.
- **(f) Off the pattern 12–20 h:** 12:45 (10), 13:40 (5); the short circles 12:10, 14:39.
- **(g) Need:** 1.

### 708 Bus station – Lyžbice, Kamionka

- **(a) Core points:** Lyžbice, Kamionka; Třinec, autobusová stanice. **Model hours 15:10–17:10** (anchor 15:40, set by hand).
- **(b) Afternoon:** out (at the bus station; 14:45, 15:15, 15:45 come from the station) **14:45, 15:15, 15:45, 16:15, 16:45**,
  then nothing; back 15:13, **15:39, 16:09, 16:39, 17:09**. In the morning every 30 too (8:15–12:15, back :14 / :44).
- **Model hour:** the default 15:30–17:30 runs past the end of the every-30 run (out ends 16:45), so every 30 leaves its
  17:15 slot empty (3 of 4, 75 %) and fails on the window edge only. The model hour is set to the run, 15:10–17:10.
- **(c) Step 4:** published every 60 (:45 / :09): out 2 / 3 PASS, back 2 slots for 4 departures FEWER. At 15:10–17:10, **every
  30 :15 / :09**: out 4 / 4 exact, back 4 slots / 5 real, 4 exact (15:13 is 4 off). The only one-bus "passes" rest on turns
  the real buses don't make: every 90 with two slots at the default window (a 2-min turn at the bus station, 1 + 2 exact) and
  every 30 :18 / :07 at 15:10–17:10 (a 1-min turn; the real buses wait 26 min there). With Step 10's 3-min turn both need two
  buses (checked with `lay` 3), so the exact every 30 takes the second bus. Every 240 with four slots (two buses, default
  window) would only match the thinning tail.
- **(d) Simutrans line 708:** every 30. Bus station Offset 14 (real :15, :45); Kamionka Offset 8 (real :09, :39). The plates
  run it so: 1TD1410 16:15 → 16:39, 71-1157 16:45 → 17:09, 1TE3309 15:45 → 16:09.
- **(e) Knots:** exact both ways.
- **(f) Off the pattern 12–20 h:** 12:14, 12:44 back (5, the morning minutes), 15:13 (4).
- **(g) Need:** 2 (+1; waits bus station 26, Kamionka 15). Owner check: one bus every 60 as before.

### 712 Station – Tyra

- **(a) Core points:** Třinec, železniční stanice; Tyra, pila (the knot); Tyra, hájenka. Model hours 14:20–16:20 (the line's
  anchor; 712 Kozinec shares it).
- **(b) Afternoon:** from the station 13:33, **14:22, 15:40**, 16:40, 17:40, 18:40 (:40 most of the day); back at pila
  13:58, **15:02, 15:46**, 16:05, 17:10, 18:09 (hájenka 15:01, 15:45). 71-1157 14:22 → 15:01, 2TE1603 15:40 → 16:05 → 16:40.
- **(c) Step 4:** published every 60 :40: 14:40(-) 15:40, 1 of 2 FAIL (back :03 passes). **Every 120**: station 14:22, 15:40
  2 / 2 exact; back 15:00, 15:44 2 slots / 3 real, exact at pila; 7 exact over the day. Every 240: same window, 7 exact but
  fewer within 1 and worst 75 against 32.
- **(d) Simutrans line 712:** every 120. Station Offset 39, Also at 81 (real 13:40/15:40 odd hours, 14:22/16:22 even hours);
  Tyra, hájenka Offset 43, Also at 119 (real 15:44, 15:00; passing pila 15:46, 15:02, `knot_at`).
- **(e) Knots:** pila exact on the way back; out the 14:22 trip takes 35 min to pila (model 27, 8 min early); the sheet's
  70 for the 15:40 slot compares it with trips that run on to hájenka (the 15:40 ends at pila, 16:03).
- **(f) Off the pattern 12–20 h:** 13:33 (7), 16:40 and 18:40 (18, even hours), 20:10; back 12:55 (5), 13:56 (12), 16:03 (19),
  17:08 (8), 18:07 (23), 19:10 (10). 15:15 from the bus station to hájenka (71-1151) is not a station trip.
- **(g) Need:** 2 (unchanged; waits station 14, 16; hájenka 43, 45). 712 Kozinec (every 240, 14:35 / 14:58, passes) unchanged.

### 714 Bus station – Oldřichovice, ves

- **(a) Core points:** Třinec, autobusová stanice; Oldřichovice, ves. Model hours 13:00–15:00.
- **(b) Afternoon:** out 12:40 (from the station), **13:37, 14:30**, 15:45; back **13:00, 14:03**, 16:05 (14:55 runs to
  restaurace only). 71-1154 13:37 → 14:03, 2TE1603 12:35 → 13:00.
- **(c) Step 4:** published every 90: 13:37 passes, ves 13:00 14:30(-) FAIL. **Every 120**: 2 / 2 exact each way; every 180
  the same window, one fewer within 1.
- **(d) Simutrans line 714:** every 120. Bus station Offset 36, Also at 89 (real 13:37, 14:30); ves Offset 62, Also at 119
  (real 14:03, 13:00).
- **(e) Knots:** ves reached 13:53 / 14:46 (real 14:01 / 14:51); the bus station 13:20 / 14:23 (real 13:20 / 14:25).
- **(f) Off the pattern 12–20 h:** 12:40 (10), 15:45 (8); 16:05 (2, on).
- **(g) Need:** 1 (waits bus station 6, 16; ves 11, 7).

### 715 Circle from Sosna hospital

- **(a) Core points:** Třinec, Dolní Líštná, Sosna nemocnice (loop). **Model hours 15:30–17:30** (anchor 16:00, set by hand).
- **(b) Day:** the circle leaves Sosna at **:10 and :50** 8:10–12:10 and 14:50–17:10 (two buses: 2TE1605 on :10, 1TE3304 on
  :50 in the morning); 13:25, 13:50, 14:15 between are a midday rhythm, and 13:30 from the bus station is a short trip to
  Sosna. The card's "every 30 (:20 / :50)" was wrong.
- **Model hour:** line_anchor moved to 13:50 because of the 13:30 short trip (its stops are on the circle, the 282 case); by
  the circle's own Sosna departures, 13:20–15:20 (5) has one more than 15:00–17:00 (4), so it stays at 16:00.
- **(c) Step 4:** published every 30 :20: 13:20(-) 13:50 14:20(-) 14:50 FAIL. At 16:00, **every 60 :10 / :50**: 15:50 16:10
  16:50 17:10, 4 / 4 exact; 17 exact over the day. At 13:50 only multi-slot rows pass (every 120 with :15, :50, 1:10, 1:50, 2
  buses), which break the line's day pattern.
- **(d) Simutrans line 715:** every 60, Offset 9, Also at 49 (real :10, :50).
- **(f) Off the pattern 12–20 h:** 13:25 (15), 14:15 (5), 18:00 (10), 18:35 (15), 19:55 (5).
- **(g) Need:** 2 (unchanged; waits 11, 11).

### 716 Bus station – Nebory – Guty

- **(a) Core points:** Třinec, autobusová stanice; Guty, konečná. Model hours 15:30–17:30.
- **(b) Afternoon:** out 12:15, 13:10, **14:20**, **15:35, 16:20**, 18:48; back 12:50, 15:00, **16:10, 16:55**, 19:25 (13:40 runs
  to Kanada). Two rounds in the window: 2TE1609 15:35 → 16:10, 2TE1604 16:20 → 16:55 (2TE1601 14:20 → 15:00 before); both
  buses turn at Guty in 1 min.
- **(c) Step 4:** published every 90: 15:48(-) 17:18(-), 16:30(-) FAIL. One slot each way passes the window count (1 slot / 2
  real) but halves the line (bus station 13:00–18:00: 2–3 slots for 4); **every 120 with two slots each way**: 2 / 2 exact
  both ways, 5 / 4 and 4 / 3 slots in 13:00–18:00, 7 exact over the day; every 180 the same window, 4 exact over the day.
- **(d) Simutrans line 716:** every 120. Bus station Offset 34, Also at 79 (real 15:35, 14:20 / 16:20); Guty Offset 69, Also at
  114 (real 16:10, 16:55).
- **(e) Knots:** Guty reached 16:08 / 16:53 (real 16:09 / 16:54), the bus station 16:40 / 17:25 (real 16:42 / 17:27).
- **(f) Off the pattern 12–20 h:** 12:15 (5), 13:10 (25), 18:48 (28); back 12:50 (5), 15:00 (5), 19:25 (30).
- **(g) Need:** 2 (+1; waits bus station 98, 8; Guty 1, 1: the real turns). Owner check: one bus every 120, half the rate.

### Failing legs left as they are (MHD Třinec)

None: every timed leg of 702–716 passes Step 4 now (703 out keeps the shift line's every 480 against the rate test, see 703). Legs passing on the ±1 count: 703 out (two slots for three
departures; 13:21 is 3 min off the 13:18 slot), 704 out (14:30 off), 707 (13:40 off), 712 back (16:03 off). 702 and 708 keep
their peak rate all day (14 and 10 slots in 13:00–18:00 against 6–8 and 5 real), as the rule says: the pattern stands for
the peak.

## MHD Frýdek-Místek (865): 301–318

Step 4 per direction in each line's model window; the real-rate test (pattern slots in 13:00–18:00 ≥ real − 1);
ranking: need ≤ published → window exact → fewest typed values → day exact → fewer buses → divisors of 60. Slots must
stand for distinct real departures (two slots within 3 min of one trip don't count twice: that rejected a 4-bus "every 30
:00 / :05" for 301 that hit no trip on the minute). Lays are the real 3-min turns (a 2-bus every-90 option for 312 that
turned in 1 min, against the real 3, was rejected). Typed values are (real − 61) mod every.

### Step 5b at the hubs (live map, 13:00–17:30)

- **Riviéra:** 301 brings 2 more buses in than it sends out, 302 and 311 one fewer each; ten buses change line there
  (301 → 311, 311 → 301, 301 → 302 …). The shapes balance across the three lines; one Simutrans line per real line is
  kept (HKO 365–369 precedent), pooling is the owner's choice.
- **Frýdek station / poliklinika:** 312 sends 8 out of the station and brings 5 back there and 3 to the poliklinika: its
  way back is read at the poliklinika (below). 308 and 314 leave the poliklinika more often than they arrive (+3, +2):
  their buses come from 312, 307 and 309.

Not changed: 304, 306, 307, 309 (pass), 302 Tesco, 316 Riviéra (pass).

### 301 Riviéra – Lískovec, Marlenka

- **(a)** Riviéra; Lískovec, Marlenka. Model hours 14:10–16:10.
- **(b)** Riviéra 14:13, 14:33, 14:43, 15:03, 15:13, 15:33, 15:43, 16:08 (then every 30 at :08 / :38). Marlenka 14:03,
  14:23, 14:33, 14:43, 15:03, 15:23, 15:33, 15:43, 16:03, 16:23. Until 14:03 Marlenka runs :03 :13 :33 :43; from 14:23 the
  :13 becomes :23: the Riviéra :43 bus runs on past Marlenka to Řepiště, U kříže and comes back through Marlenka at :23
  (1TC2114: Riviéra 13:43 → U kříže 14:14, 14:17 → Riviéra 14:48).
- **(c)** Published every 30 :03 / :13: Riviéra 8 slots / 8 real, 7 filled, pass; Marlenka 8 / 8, 6 filled (14:13, 15:13
  empty), FAIL. Every 30 :03 / :23 at Marlenka: :53 slots empty, FAIL. **Every 60, Riviéra :03 :13 :33 :43, Marlenka :03
  :23 :33 :43**: 8 / 8 each, Riviéra 7 filled (16:03 slot, real 16:08), Marlenka 8 exact. The only passing pattern (a
  4-bus every 30 :00 / :05 passes the letter of Step 4 with two slots on each :03 and none on :13 / :43: rejected).
- **(d)** Every 60. Riviéra Offset 2, Also at 12, 32, 42 (real :03, :13, :33, :43); Marlenka Offset 2, Also at 22, 32, 42
  (real :03, :23, :33, :43). **Fold:** the Riviéra row is evenly spaced (it is every 30, Offset 2, Also at 12, as
  published); 05_schedule writes one interval per Simutrans line, so it prints every 60 with four values (shared script).
- **(e)** Marlenka and Riviéra exact for every window slot (16:03 slot: 5 min, the 16:08).
- **(f)** Off: the every-30 :08 / :38 trips from 16:08 (5 min), Marlenka 12:13, 13:13 (10), 17:53; evening 18:23, 18:55, 19:55.
- **(g)** Need 5 (was 4): waits Riviéra 5, 5, 55, 5; Marlenka 15, 5, 5, 5. The cheaper published pattern (4 buses) is on
  the owner checks. Rate 13–18: 20 slots against 16 real at Riviéra: service thins to every 30 after 16:00.

### 302 Frýdecká skládka – Riviéra

- **(a)** Frýdecká skládka; Riviéra; Tesco. Model hours 15:00–17:00 (anchor set by hand to 15:30).
- **(b)** Skládka every 30 at :12 / :42 12:12–17:42; Riviéra :27 / :57 12:27–16:57, then 18:36.
- **(c)** At the default anchor 16:00 (15:30–17:30) Riviéra has 4 slots, 3 real, 17:27 empty: 75 %, FAIL; skládka 4 / 4
  exact. The pattern ends inside that window, so the model hours move to where it runs (282 / 451 / 533 precedent): 15:00–
  17:00, both legs 4 / 4 exact. Rate 13–18 at Riviéra 10 against 8: service thins after 16:57.
- **(d)** Every 30, skládka Offset 11 (real :12), Riviéra Offset 26 (real :27): unchanged. 302 Tesco unchanged.
- **(e)** Exact. **(f)** Off: skládka 19:33, Riviéra 18:36. **(g)** 3 (+1 Tesco), unchanged.

### 303 Dobrá – Frýdek – Baška, 303 Hodoňovice

- **(a)** Dobrá, VÚHŽ; Baška, Obecní úřad; Frýdek, Dobrovského; Hodoňovice, Kamenec. Model hours 14:00–16:00 (anchor 14:30).
- **(b)** Dobrá :35 8:35–16:35; Baška :27 7:27–15:27, then 16:59 (from Kamenec 16:47 via Baška); Dobrovského :59
  7:59–16:59; Kamenec :52 (8:47, 10:47 at :47), last 15:52, then 17:52. From 16:27 the back trips swap paths: Baška 16:27 and
  17:27 run to Frýdek, Dobrovského (722, 692), Kamenec 16:47 runs to Dobrá (598).
- **(c)** Default 15:30–17:30: Baška 2 slots / 1 real, 0 filled; Kamenec 2 / 1, 1 filled: FAIL. 14:00–16:00: all four legs 2 / 2 exact.
- **(d)** Unchanged: 303 every 60, Dobrá Offset 34 (:35), Baška 26 (:27); 303 Hodoňovice Dobrovského 58 (:59), Kamenec 51 (:52).
- **(e)** Obecní úřad exact both ways; Kamenec 0 / 5. **(f)** Off: Baška 16:59; the Baška → Dobrovského trips 16:27,
  17:27 and Kamenec 16:47 (their stops are on the two lines); Dobrá 18:05. **(g)** 2 + 2, unchanged.

### 305 Frýdek, station – Horní Sklenov

- **(a)** Frýdek, železniční stanice; Horní Sklenov, restaurace. Model hours 15:30–17:30.
- **(b)** Out 13:09, 14:23, 15:08, 16:08, 17:12, 18:36; back 13:59, 15:09, 15:59, 16:59, 18:02.
- **(c)** Published :08: 16:08, 17:08 (17:12 is 4 off): 1 of 2, FAIL. Every 60 :09: 2 / 2 within 3, none exact.
  **Every 120, even hours :08 / odd hours :12**: 16:08, 17:12 exact. Back :59 2 / 2 exact.
- **(d)** Every 120. Station Offset 11, Also at 67 (real 13:12, 15:12, 17:12; 14:08, 16:08, 18:08); Sklenov Offset 58,
  Also at 118 (real 13:59, 15:59, 17:59; 14:59, 16:59). **Fold:** the Sklenov row is every 60 Offset 58 written on 120.
- **(e)** Sklenov 1 / 1; station exact. **(f)** Off: 14:23, 15:08 (4), 18:36; back 15:09, 19:24. **(g)** 2 (waits 28, 24 / 7, 3).

### 308 Skalice, Záhoří – poliklinika, 308 Mitrovice

- **(a)** Skalice, Záhoří; Místek, poliklinika; Nová Bělá, Mitrovice. Model hours 15:30–17:30.
- **(b)** Poliklinika → Záhoří 14:28 (from Mitrovice), 15:28, 16:13, 17:28; Záhoří → poliklinika 14:57, 15:57, 17:57.
  Mitrovice: out 9:49, 13:19, 15:04 (from the station); back 5:01, 7:01, 10:21, 14:01.
- **(c)** Published every 90: Záhoří 16:27 slot 0 / 1; poliklinika 15:58 empty, 1 of 2: FAIL. Every 60 :57 / :28: 16:57 and
  16:28 slots empty, 1 of 2 each: FAIL. **Every 120 odd hours, Záhoří :57, poliklinika :28**: Záhoří 1 / 1, poliklinika 1
  slot / 2 real, filled; rate 3 / 3 and 3 / 4. 308 Mitrovice every 180: its 17:01 slot has no trip; every 480 on the
  real round (733: poliklinika 13:19 → Mitrovice 13:46, 14:01 back) has no window slot and keeps the day's rate (3 a day).
- **(d)** 308 every 120: Záhoří Offset 56 (real 13:57, 15:57, 17:57), poliklinika Offset 27 (real 13:28, 15:28, 17:28).
  308 Mitrovice every 480: poliklinika Offset 258 (real 13:19), Mitrovice Offset 300 (real 14:01).
- **(e)** Exact. **(f)** Off: 14:57 (60), 16:13 (45), the 14:28 Mitrovice through trip; Mitrovice 15:04 out.
  Paskov, nadjezd and Břehy have no other line. **(g)** 1 + 1, unchanged.

### 310 poliklinika circle

- **(a)** Poliklinika. Model hours 14:10–16:10.
- **(b)** 12:15, 13:15, 14:15, 14:30, 15:00, 15:30, 16:00, 17:00, 18:03 (hourly :15 until 14:15, every 30 14:30–16:00).
- **(c)** Published every 40: 14:20, 15:00, 15:40: 1 of 3, FAIL. **Every 30 :00**: 4 slots / 5 real, exact. Every 60
  :00 :15 :30 (5 exact) needs 2 buses; every 180 with four slots (1 bus) is as exact in the window with four typed values.
  Rate 13–18: 10 against 7: the every-30 stretch is 14:30–16:00, hourly outside.
- **(d)** Every 30, Offset 29 (real :00, :30). **(f)** Off: 12:15, 13:15, 14:15 (15). **(g)** 1 (wait 7).

### 311 Riviéra – Řepiště, U kříže

- **(a)** Riviéra; Řepiště, U kříže. Model hours 13:10–15:10.
- **(b)** Riviéra :23 / :53 to 17:23. U kříže :12 / :42 until 13:42, then 14:03, 14:42, 15:03, 15:42, 16:03, then 17:12.
- **(c)** Published every 30 :12 at U kříže: 13:12, 13:42, 14:12 (empty), 14:42: 75 %, FAIL. **Every 60, U kříže :03 /
  :42**: 13:42, 14:03, 14:42, 15:03, 4 slots / 5 real, exact; Riviéra :23 / :53 4 / 4 exact. Rate 13–18 at U kříže 10
  against 8: the back trips thin after 16:03.
- **(d)** Every 60. Riviéra Offset 22, Also at 52 (real :23, :53; **fold:** every 30 Offset 22, as published); U kříže
  Offset 2, Also at 41 (real :03, :42).
- **(e)** Exact. **(f)** Off: U kříže 12:12, 13:12, 17:12 (9), 18:15, 19:15; Riviéra 18:34, 19:35. **(g)** 3 (waits 4, 13 / 13, 4).

### 312 Frýdek, station – Brušperk

- **(a)** Frýdek, železniční stanice; Místek, poliklinika (read point of the way back); Brušperk, točna. Model hours 13:50–15:50.
- **(b)** Out 14:02, 14:35, 15:05, 15:35, 16:05, 16:35, 17:35. Back from Brušperk 13:47, 15:20, 16:40 (to the station),
  14:47, 15:41, 17:20, 18:20 (ending at the poliklinika). The plates go out and back on the line (609 14:02 → 14:47, 711
  14:35 → 15:20, 597 15:05 → 15:41 and 16:35 → 17:20, 731 15:35 → 16:40).
- **(c)** Published every 60: station 2 slots for 4 trips, FAIL; back read at the station (only half the trips): 14:20
  empty, FAIL. Back read at the poliklinika: every 30 out passes, every 30 back can't (:20 / :50 75 %). Every 90 with two
  slots (2 buses) turns in 1 min at both ends against the real 3: rejected. **Every 96, station 14:35 / 15:35, Brušperk
  14:47 / 15:20**: out 3 slots / 4 real (13:59 for 14:02), back 2 / 3, 4 exact; 2 buses with 3–6 min turns. Every 180 with
  three slots (6 of 7 exact) needs 3.
- **(d)** Every 96. Station Offset 10, Also at 46 (real 13:59, 15:35, 17:11, 18:47; 14:35, 16:11, 17:47); Brušperk Offset
  58, Also at 91 (real 13:11, 14:47, 16:23, 17:59; 13:44, 15:20, 16:56, 18:32).
- **(e)** Brušperk 3, 0, 0. **(f)** Off: out 12:40, 15:05, 16:05 (6), 16:35, 17:35, 18:32; back 12:27, 15:41, 16:40,
  17:20, 18:20 (12), 19:18. **(g)** 2 (waits 6, 3 / 6, 3).

### 313 Frýdek, station – Nošovice

- **(a)** Nošovice, střed; Frýdek, železniční stanice. Model hours 13:30–15:30.
- **(b)** Out 12:38, 13:31, 16:38; back 14:10, 15:00, 17:07 (and Sviadnov trips).
- **(c)** Published even hours :38: 14:38 empty, FAIL. **Every 120, odd hours :31 / even hours :10**: 1 / 1 and 1 / 2, exact.
- **(d)** Station Offset 30 (real 13:31, 15:31, 17:31); Nošovice Offset 69 (real 14:10, 16:10), unchanged.
- **(e)** Exact. **(f)** Off: 12:38, 16:38; back 15:00, 17:07. **(g)** 1.

### 314 Frýdek – Baška – Janovice

Corrected by the branch check (`../audit/branch-check-2026-10-25.md`): (b) below shows the afternoon trips use Revoluční,
yet the row kept the station as its town end, so three of its four slots were trips of the other end. The town end is now
Frýdek, Revoluční (Revoluční Offset 85, Also at 116, real 14:26, 14:57, exact; Janovice Offset 34, Also at 71, real 14:12,
15:35), 2 buses; the Baška slots are unchanged.

- **(a)** Frýdek, Revoluční (was the station); Baška, železniční stanice (the knot every trip passes); Janovice, konečná. Model hours 14:10–16:10.
- **(b)** The afternoon trips start at the poliklinika (13:33, 14:20, 17:06) or Revoluční (14:57, 16:07), not the station,
  and end at Janovice, konečná or škola. At Baška station: towards Janovice 13:52, 14:39, 15:10, 16:20, 17:25, 18:53;
  towards Frýdek 13:12, 14:36, 15:19, 15:59, 16:58, 18:03, 19:37. Buses 724 and 709 run it.
- **(c)** Published every 240 counted only the trips from the station (5 a day): 14:44 slot empty, IRREGULAR. Read at Baška:
  **every 120, two slots each way**: towards Janovice 2 / 2 exact, towards Frýdek 2 slots / 3 real exact; rate 5 / 5 and
  5 / 6. No 1-bus pattern keeps the real rate (every 80 with one slot passes Step 4 with 3–4 slots in 13–18 against 5–6).
- **(d)** Every 120. Station Offset 0, Also at 89 (real 13:01, 15:01, 17:01; 14:30, 16:30: passing Baška 14:39, 15:10);
  Janovice Offset 36, Also at 73 (real 13:37, 15:37, 17:37; 14:14, 16:14: passing Baška 14:36, 15:59). `stops_via` keeps
  each leg's full path (otherwise the stop list would start at the knot).
- **(e)** Baška exact by construction. The sheet's knot check at Janovice / Frýdek shows 167–198 / 84 min: it compares with
  the few trips that run the whole station – konečná path (morning and evening), not with these.
- **(f)** Off at Baška: 13:52, 16:20, 17:25 out; 13:12, 15:19, 16:58, 18:03 back. Staré Město, u hřbitova, Baška station and
  rozcestí Janovice have no other line. **(g)** 2 (was 1): waits station 19, 13; Janovice 73, 5. Owner check: the
  published one-bus pattern.

### 316 Palkovice round (315 out, 316 back)

- **(a)** Místek, poliklinika; Palkovice, centrum. Model hours 14:00–16:00 (sim window).
- **(b)** Out (315) 13:12, 14:13, 15:42; back (316) 13:43, 14:45, 16:15; nothing later.
- **(c)** At the line's 15:30–17:30: 15:42, 17:12 (empty): FAIL. The round ends inside that window (whose other trips are
  316 Riviéra's, which pass there), so this Simutrans line gets its own hours, as 285 on the Opavsko sheet: 14:00–16:00,
  out 14:12 / 15:42 (14:13, 15:42), back 14:45, exact.
- **(d)** Unchanged: every 90, poliklinika Offset 71 (real 14:12, 15:42), centrum Offset 14 (real 14:45, 16:15).
- **(e)** Centrum 1 / 0. **(f)** Off: 13:12, 13:43. **(g)** 1 (+1 Riviéra), unchanged.

### 318 poliklinika – Raškovice – Krásná, hotel Visalaje

- **(a)** Místek, poliklinika; Raškovice, hotel Ondráš (knot, where the short trips turn); hotel Visalaje. Model hours 13:00–15:00.
- **(b)** Full route out 13:50, 14:58, 16:58, 18:58; back from Visalaje 13:42, 14:48, 16:00, 18:05 (Ondráš 14:10, 15:10,
  16:28, 18:26). Ondráš shorts: 12:33, 13:15 out (734), 13:03, 13:53 back.
- **(c)** Published every 60 :52: 13:52, 14:52 (empty), FAIL. Every 240 on the full-route rounds (**poliklinika 13:50 /
  14:58, Ondráš 14:10 / 15:10**): out 2 slots / 3 real, back 2 / 3, all exact. The same with the shorts (13:15 / 13:53) is
  as exact in the window and hits one more trip over the day, but folds the short variant into the row (Step 11); not taken.
- **(d)** Every 240. Poliklinika Offset 49, Also at 117 (real 13:50, 17:50; 14:58, 18:58); Visalaje Offset 47, Also at
  107 (real 13:48, 17:48; 14:48, 18:48; the 13:42 trip takes 6 min longer to Ondráš, so it is 13:48 here).
- **(e)** Ondráš 2 / 0 out, 14:10 / 15:10 back; poliklinika 0 / 0. **(f)** Off: the shorts, out 16:58, back 16:00, 18:05.
  **(g)** 2 (waits 16, 128 / 4, 116).

### Left as they are / by design

- 302 Tesco and 308 Mitrovice have no trip in their window (every 480, Step 8 lines for places only they serve); the audit
  counts them as passing.
- Rate test above the real count (service thins after the peak; the pattern stands for the peak): 301 after 16:00, 302
  after 16:57, 310 outside 14:30–16:00, 311 (back) after 16:03.
- Fold (shared 05_schedule writes one interval per Simutrans line): the 301 Riviéra, 305 Sklenov and 311 Riviéra rows are
  evenly spaced and fold to every 30 / every 60 by the kb rule.

## Frýdecko-Místecko (863) and Frýdlantsko (864): 341–348, 351, 358, 980, 985

Rules applied (the uniform policy of this check): variant trips with a row of their own (351 Bebek, 358 Steel, 343 Podolánky,
345 Hutě) and shift trips with no row (344's Hyundai trips) are not read into the main rows; Step 4 per direction plus the
13:00–18:00 lower bound (slots ≥ real − 1); ranking: need ≤ published, most exact in the window, fewest typed values, most exact
over the day, fewer buses, divisors of 60, worst deviation. Typed values are (real − 61) mod every (every terminus is a loop).
Every result below was built with 05_schedule's own code.

No bus changes in this group. 340, 342 and 349 pass and were not touched.

### 351 Ostrava – Frýdek – Raškovice – Morávka, Lipové
- **(a) Core points:** Ostrava, Náměstí Republiky; Frýdek, autobusové nádraží (knot: trips from Ostrava and from Místek,
  Anenská join here); Morávka, Lipové. Model hours 15:30–17:30.
- **(b) Afternoon:** towards Morávka, at Frýdek AN: 13:39 (Bebek), 14:25 (Ostrava 13:43), 15:25 (Bebek), 15:50 (Ostrava 15:08),
  16:25 (15:43), 17:22 (16:43), 18:22 (Bebek), plus Anenská 12:34 / 19:24 and the Ostrava – Frýdek shorts 14:15, 16:13, 18:15.
  From Lipové: 12:56 and 14:16 (to Ostrava), 16:26 (to Místek, Anenská via Frýdek žst, not via the bus station), 21:58; the
  Bebek trips pass Lipové at 15:31, 17:21, 19:50.
- **Outstation:** the plates show the buses going out and staying (33-1013 out 13:43, 33-1007 out 16:43, both end at Lipové;
  32-1109 out 15:43 goes on to 314). Only 33-1022 (14:16) and 32-1110 (16:26) come back, both brought out on other trips.
- **Reading fixed first:** the main rows also counted the Bebek trips (the published back row's only window departure, 15:31, is
  the Bebek bus, which 351 Bebek already models). Now `notvia` Bebek both ways, and the back row is read to Frýdek,
  železniční stanice so the 16:26 counts.
- **(c) Step 4 (window: out 15:43, 16:40 at the Frýdek reading; back 16:26):** every 60 back fails (one real, two slots: 1 of 2).
  Passing: every 120 out 1:43 / back 0:26, need 3, window exact 2, day exact 4; every 120 out 0:40 / back 0:26, need 2, day exact
  3 (13:43 and 15:43 off, 16:40 on); every 72 (1:04 / 0:50), need 3, day exact 3. Taken: the first.
- **(d) Simutrans line 351:** every 120. Ostrava Offset 42 (real 13:43, 15:43, 17:43; knot Frýdek AN 14:25, 16:25),
  Lipové Offset 85 (real 14:26, 16:26).
- **(e) Knots:** out Lipové 17:07 exact. Back: the knot check shows 130 min at Ostrava for the 16:26 slot because the real
  16:26 ends at Místek, Anenská (via Frýdek, železniční stanice 17:04), not at Ostrava.
- **(f) Off the pattern 12–20 h:** out 12:00 (Anenská 12:34), 15:08, 16:43 (going home), 18:50 (Anenská 19:24); back 12:56
  (30), 14:16 (10). 351 Bebek's 17:42 slot passes Frýdek AN 3 min before 351's 17:43 slot (every 120 against every 180).
- **(g) Need:** 3 (waits Ostrava 120, Lipové 79). The cheaper passing option (even hours :40, two buses) loses the exact
  13:43 / 15:43; it is not an owner check because the chosen row keeps the published need.

### 358 Krytý bazén – Nošovice, Hyundai
- **(a)** Místek, Krytý bazén; Nošovice, PZ Hyundai – hlavní brána. Model hours 14:10–16:10.
- **(b)** A shift line: Krytý bazén 5:03, 13:03, 21:03; Hyundai 6:25, 14:25, 22:25. The Steel trips (Riviéra 4:53, 12:53,
  20:53 via Krytý bazén 8 min later; IZS 14:17 via Hyundai 14:28) were read into the main rows too (`notvia` Steel now).
- **(c)** Published every 180 at 13:01: the 16:01 slot has no trip (IRREGULAR, no window departure out). Every 480 (Step 8,
  shift lines repeat every 480) is exact on all three trips each way.
- **(d) Simutrans line 358:** every 480. Krytý bazén Offset 242 (real 5:03, 13:03, 21:03), Hyundai Offset 324 (real 6:25, 14:25,
  22:25). 358 Steel unchanged (Offset 232 / 316: Riviéra 12:53, IZS 14:17).
- **(e)** Hyundai 13:30 exact; Krytý bazén 14:49 (real 14:54).
- **(f)** none on the rows; the Frýdek AN – Hyundai trips (9:55, 10:30, 14:50, 15:58, 19:30) have no row (stops on 351, 357, 358).
- **(g)** 1. Owner check added: its stops are all on 358 Steel, so Step 8 would list it with 358 Steel (one bus less).

### 980 Ostrava – Frýdek – Frenštát – Rožnov (approximate, typed values unchanged)
- **(a)** Ostrava, Náměstí Republiky; Frenštát, u škol; Rožnov, autobusová stanice. Model hours 13:30–15:30.
- **(b)** Out of Ostrava 12:50, 13:40, 14:05 (Z-Group short to Frenštát), 14:23, 14:53, 15:23, 15:53, 16:23, 17:25 (short),
  17:55. From Rožnov 12:50, 13:35, 14:05, 14:35, 15:05, 16:05, 17:35; Frenštát starts 13:32, 14:17 (Z-Group), 15:42, 17:27.
  985 Rožnov fills the corridor's shoulders (Ostrava 13:53, 16:53; Rožnov 15:35, 16:35).
- **(c)** The back row counted the Frenštát starts (FEWER: 6 real, 4 slots); read at Rožnov it is exact 4 of 4. Out: every 30
  :23 leaves 13:53 without a trip (13:40 is 13 min off), 3 of 4. Hand anchors 14:10–15:00 do not help (out starts 14:23,
  back stops after 15:05, so one window slot is always empty). The only rows passing both ways at 7 buses are every 120 with
  four slots (out 13:40, 14:23, 14:53, 15:23; back every 30): they put a :40 slot in every odd hour (15:40 against the real
  15:53, 17:40 against 17:55), 8 typed values, and within 3 min over the day drops from 17 to 13 of 22. Every 180 four slots
  needs 8 buses, every 90 four slots 10. Kept every 30, the simplest pattern at the real rate (rule 4: approximate, To check).
- **(d)** every 30, Ostrava Offset 22 (real :23), Rožnov Offset 4 (real :05). Knot Frenštát :27 / :57.
- **(e)** Frenštát 13:57, 14:27, 14:57, 15:27 exact on the way back; Ostrava arrivals within 1–4 min; out, Frenštát
  and Rožnov within 3 min except the 13:53 slot (18).
- **(f)** out 13:40 (13), 14:05 (12, Z-Group short); back 12:10, 12:50; the Frenštát starts listed above.
- **(g)** 7 (waits Ostrava 20, Rožnov 12).

### 985 Rožnov
- **(b)** Ostrava → Rožnov 5:55, 11:20, 12:20, 13:13, 13:53, 16:53; Rožnov → Ostrava 4:20, 11:35, 15:35, 16:35, 19:35.
- **(c)** Window 15:30–17:30: out 16:53, back 15:35, 16:35. Published Rožnov odd :15 (17:15, no trip) fails. Every 60 out fails
  (one real, two slots). Passing at 2 buses: every 180 Ostrava 1:53 / Rožnov 1:35 (window exact 2, day exact 4); every 180 with
  Rožnov 0:35 (day 3); every 120 :53 even / :35 even (day 2). Taken: the first.
- **(d)** every 180. Ostrava Offset 52 (real 13:53, 16:53, 19:53), Rožnov Offset 34 (real 13:35, 16:35, 19:35).
- **(e)** Frenštát 16:57 and Ostrava 18:10 exact; Rožnov arrival 3 min late.
- **(f)** out 12:20, 13:13 (11:20); back 15:35 (60).
- **(g)** 2 (waits Ostrava 103, Rožnov 67). Its minutes are 980's (:53 out, :35 back), as the real 985 trips are the shoulders
  of 980's every 30; the published row already shared Ostrava :53.

### 341 Frýdlant – Janovice
- **(b)** Frýdlant 6:06, 9:04, 11:04, 14:19, 16:34, 18:04; Janovice 6:28, 9:30, 12:30, 15:00, 17:00, 18:30 (13:34 → Janovice,
  škola and 14:00 back are short trips; the old note's "13:34, 15:04" were not konečná trips).
- **(c)** Window 13:10–15:10: 14:19 / 15:00. Published every 90 (13:34, 15:04 / 14:00 slots) fails both. Every 120 :19 even /
  :00 odd, need 1, day exact 3; every 180 and 160 day exact 2.
- **(d)** every 120. Frýdlant Offset 78 (real 12:19, 14:19, 16:19), Janovice Offset 119 (real 13:00, 15:00, 17:00).
- **(e)** Janovice 14:43, Frýdlant 15:23 exact. **(f)** Frýdlant 16:34, 18:04 (15); Janovice 12:30, 18:30 (30).
- **(g)** 1 (waits Frýdlant 56, Janovice 17).

### 343 Frýdlant – Čeladná, restaurace Kněhyně
- **(b)** Frýdlant 12:20 (Podolánky), 14:10, 15:00 (Podolánky), 16:50; Kněhyně 11:58, 13:08 (Podolánky bus), 14:35,
  15:48 (Podolánky bus); then the Čeladná station – Kněhyně shorts 17:20–19:40.
- **Model hour by hand, 14:00:** after 16:06 only the 16:50 runs out, and its bus (32-1006) stays in Čeladná for the shorts; the
  line's own round (32-1101) is 12:20–16:06. The published back slot stood for the Podolánky bus, which 343 Podolánky already
  models (`notvia` Podolánky now).
- **(c)** Window 13:30–15:30: 14:10 / 14:35. Every 80 (0:50 / 1:15) and every 160 (same slots) both exact in the window, day
  exact 4; worst 30 against 73, so every 80; every 120 (14:10 / 14:35) day exact 2.
- **(d)** every 80. Frýdlant Offset 69 (real 12:50, 14:10, 15:30, 16:50), Kněhyně Offset 14 (real 13:15, 14:35, 15:55).
  343 Podolánky unchanged (15:00 / 15:35, every 480).
- **(e)** Kněhyně 14:32, Frýdlant 14:56 exact. **(f)** none 12–20 h on the row. **(g)** 1 (waits Frýdlant 34, Kněhyně 3).

### 344 Frýdlant – Raškovice
- **(b)** Frýdlant 12:05, 12:35 (Hyundai), 13:35, 14:30, 15:10, 16:05, 18:05; Ondráš 12:20, 13:20, 14:10, 14:50 (Hyundai
  14:25), 15:20, 17:08, 19:08.
- **(c)** Window 13:20–15:20 (Hyundai trips out): out 13:35, 14:30, 15:10; back 13:20, 14:10. No hourly slot passes (out best
  2 of 3, back 1 of 2). Every 120 two slots each way: out 14:30 + 15:10 / back 13:20 + 14:10, need 2, window exact 4, day
  exact 5, worst 25; out 13:35 + 14:30 the same with worst 30; every 180 variants worst 60.
- **(d)** every 120. Frýdlant Offset 9, Also at 89 (real 13:10 / 15:10 / 17:10 and 12:30 / 14:30 / 16:30); Ondráš Offset 19,
  Also at 69 (real 13:20 / 15:20 / 17:20 and 14:10 / 16:10). Plates: 13:20 → 14:30 (32-1108), 14:10 → 15:10 (32-1102).
- **(e)** Ondráš within 1 min; Frýdlant arrivals 7 min early (median running time). **(f)** out 12:05, 13:35, 16:05, 18:05 (25);
  back 12:20 (10), 17:08, 19:08 (12). **(g)** 2 (waits Frýdlant 37 / 47, Ondráš 22 / 32).

### 345 Frýdlant – Malenovice
- **Model hour by hand, 16:00:** line_anchor moved it to 14:00 only because of the 14:05 zahradnictví – station hop and the Hutě
  trips (a row of their own, now `notvia` Hutě); on the line's own trips its busiest two hours are within one departure of
  15–17, so 16:00 stands.
- **(c)** Window 15:30–17:30: 15:55, 16:55 / 16:25, 17:25: every 60 :55 / :25 exact 4 of 4, typed 2; every 160 and 180 with two
  slots also exact but four typed values. At 14:00 the best was every 120 (two buses) or every 160 (one bus, 3 exact).
- **(d)** unchanged typed values: every 60, Frýdlant Offset 54 (real :55), Malenovice Offset 24 (real :25).
- **(f)** 13:30, 14:40 out; 13:42, 14:55 back. **(g)** 1 (waits 18 / 18). No in-game change.

### 346 Frýdlant – Pstruží loop
- **(b)** at the station 12:52 (from zahradnictví), 13:54, 14:22 (zahradnictví), 15:24, 15:52 (zahradnictví), 17:20, 18:50.
- **(c)** Window 13:50–15:50: 13:54, 14:22, 15:24. Published every 60 :52: 14:52 empty. Every 90 two slots exact 3 of 3, day
  exact 5, need 1; every 160 / 180 three slots day 3.
- **(d)** every 90. Offset 53, Also at 81 (real 13:54 / 15:24 / 16:54 and 12:52 / 14:22 / 15:52). **(g)** 1 (waits 2, 36).

### 347 Frýdlant – Palkovice, transformátor
- **(b)** Frýdlant 12:45, 13:55, 14:25, 15:30 (later trips end at Tomis parkoviště); transformátor 13:07, 14:22, 14:57, 15:57.
- **(c)** Window 14:20–16:20: out 14:25, 15:30; back 14:22, 14:57, 15:57. Published Frýdlant :30: 14:30 empty (5 min).
  Every 60 :28 / :57 passes (window exact 2). Every 120 two slots (out 14:25 + 15:30, back :57 hourly) exact 4, worst 25; every
  144 / 160 / 180 two slots also exact 4, worst 35–50.
- **(d)** every 120. Frýdlant Offset 29, Also at 84 (real 13:30 / 15:30 / 17:30 and 14:25 / 16:25); transformátor Offset 56,
  Also at 116 (real :57 every hour; timed at Tomis parkoviště :00).
- **(e)** transformátor 14:43 / 15:48 (real 14:45 / 15:48). **(f)** out 12:45 (20), 13:55 (25); back 13:07 (10), 14:22 (25).
- **(g)** 1 (waits 10 / 15, 14 / 9).

### 348 Frýdlant – Ostravice – Bílá
- **(b)** Frýdlant 12:23, 13:53, 14:53, 15:53; Bílá 12:01, 14:31, 15:16; then Bílá – Ostravice shorts (Bílá :06 from 16:06).
- **(c)** Window 13:40–15:40: out 13:53, 14:53; back 14:31, 15:16. Published Bílá :16: 14:16 empty. Every 120 (hourly :53 /
  14:31 + 15:16) need 3, window exact 4, day exact 8; every 240 the same slots, day exact 6; one slot each way: every 120
  (13:53 / 15:16) 2 buses, every 180 (13:53 / 15:16) 1 bus — both drop half of the window's departures.
- **(d)** every 120. Frýdlant Offset 52, Also at 112 (real :53 every hour); Bílá Offset 15, Also at 90 (real 13:16 / 15:16 /
  17:16 and 14:31 / 16:31).
- **(e)** Ostravice 14:04 / 15:04 exact; Bílá arrivals 6 min late (median). **(f)** 12:23 out, 12:01 back.
- **(g)** 3 (waits Frýdlant 44 / 59, Bílá 40 / 55).

### Left approximate in this group
- **980 out of Ostrava:** 3 of 4 window slots (13:53 for the real 13:40); see above for why the every-120 four-slot row that
  passes at 7 buses was not taken. On the To check list.

### Notes
- 347 back (transformátor :57 every hour) and 348 out (Frýdlant :53 every hour) are written as two values on every 120:
  05_schedule keeps one interval per Simutrans line and does not fold per row, so the sheet will print them unfolded.

## Legs still failing the audit, with why

- **980 out of Ostrava (EMPTY, approximate, To check):** every 30 at :23. Its 13:53 slot stands for the real 13:40 (13 min
  off), so 3 of the 4 window slots are filled. Hand anchors 14:10–15:00 don't help: the out row starts at 14:23, and the back
  row pauses after 15:05. The only rows that pass both ways at 7 buses are every 120 with four slots: out 13:40, 14:23,
  14:53, 15:23, back every 30. They add a :40 departure to every odd hour (15:40 against the real 15:53, 17:40 against
  17:55), need 8 typed values instead of 2, and cut the trips within 3 min over the day from 17 to 13 of 22. Every 180 with
  four slots needs 8 buses, every 90 with four slots 10. So every 30, the simplest pattern at the real rate, is kept (Step 4
  rule 4). This is a deliberate exception to "an exact multi-slot row beats a simpler failing one": the multi-slot row makes
  up departures over the day. It is on the owner checks. The back row now passes, read at Rožnov. The typed values are
  unchanged.
- **732 from Havířov, 745 from Hnojník, 750 from Frýdek (FEWER by design):** 2, 1 and 2 slots for 5, 3 and 5 real departures
  in the window. Each line runs at the rate of its other direction. The extra departures are buses going on to other lines
  or a variant's bus (plates on each card): 732's extras go on to 733 / 734 or to Jablunkov; 745's are a 750 short's bus and
  the Třanovice bus; 750's came in on 739 and 751.

No leg was left IRREGULAR. The audit's three IRREGULAR legs (308 Mitrovice, 314, 358) are now every 480 on their real round
(308 Mitrovice, 358) or every 120 read at Baška (314).

## For the orchestrator

- **Fold rule (shared 05_schedule):** 05 writes one interval per Simutrans line, so these rows will print unfolded against
  the kb fold rule ("never write every 60 … Also at …, it is every 30"):
  - 301 Riviéra (every 60 :03 :13 :33 :43, which is every 30 :03 / :13);
  - 311 Riviéra (every 60 :23 :53 = every 30);
  - 305 Sklenov (every 120 :59 twice = every 60);
  - 347 back (:57) and 348 out (:53), both every 120 typed twice = every 60;
  - 748 Střítež (every 120 :11 twice = every 60).

  The owner can type them folded. Whether 05 or 06 should fold per row is a shared-script decision.
- **Shared minutes:** 985 Rožnov and 980 leave Ostrava at the same :53 and Rožnov at the same :35. Every passing 985 Rožnov
  slot does this, and the published row already shared Ostrava :53. 351's 17:43 and 351 Bebek's 17:42 pass Frýdek 3 min
  apart.
- **Roster:** need 143 → 150. 04_roster (keep_roster = roster_v5) must place the new buses and the moved ones; the in-game
  change list per entry is below (vehicles in / out follow from the roster run).
- **Audit tool:** `step4_regional.py` counts a pass when two slots sit within 3 min of the same trip. It gave a fake pass
  for 301 (every 30 :00 / :05, no trip on the minute), rejected here. Other sheets may meet it too.

## In-game change list (typed values)

Per Simutrans line and timed entry: old → new Departure every / Offset / Also at, with the real time each value stands for
((value + 61) mod every; for intervals over 60 the times between 12:00 and 20:00). Entries not listed are unchanged. Buses in /
out follow from the roster run (keep_roster = roster_v5).

- **301** (need 4 → 5)
  - Riviéra: every 30, Offset 2, Also at 12 (real :03; :13) → **every 60, Offset 2, Also at 12, 32, 42 (real :03; :13; :33; :43)**
  - Marlenka: every 30, Offset 2, Also at 12 (real :03; :13) → **every 60, Offset 2, Also at 22, 32, 42 (real :03; :23; :33; :43)**
- **305** (need 2 → 2)
  - železniční stanice: every 60, Offset 7 (real :08) → **every 120, Offset 11, Also at 67 (real 13:12/15:12/17:12/19:12; 12:08/14:08/16:08/18:08)**
  - restaurace: every 60, Offset 58 (real :59) → **every 120, Offset 58, Also at 118 (real 13:59/15:59/17:59/19:59; 12:59/14:59/16:59/18:59)**
- **308** (need 1 → 1)
  - Záhoří: every 90, Offset 26 (real 13:27/14:57/16:27/17:57/19:27) → **every 120, Offset 56 (real 13:57/15:57/17:57/19:57)**
  - poliklinika: every 90, Offset 87 (real 12:58/14:28/15:58/17:28/18:58) → **every 120, Offset 27 (real 13:28/15:28/17:28/19:28)**
- **308 Mitrovice** (need 1 → 1)
  - poliklinika: every 180, Offset 123 (real 12:04/15:04/18:04) → **every 480, Offset 258 (real 13:19)**
  - Mitrovice: every 180, Offset 60 (real 14:01/17:01) → **every 480, Offset 300 (real 14:01)**
- **310** (need 1 → 1)
  - poliklinika: every 40, Offset 39 (real :20) → **every 30, Offset 29 (real :00)**
- **311** (need 3 → 3)
  - Riviéra: every 30, Offset 22 (real :23) → **every 60, Offset 22, Also at 52 (real :23; :53)**
  - U kříže: every 30, Offset 11 (real :12) → **every 60, Offset 2, Also at 41 (real :03; :42)**
- **312** (need 2 → 2)
  - železniční stanice: every 60, Offset 34 (real :35) → **every 96, Offset 10, Also at 46 (real 12:23/13:59/15:35/17:11/18:47; 12:59/14:35/16:11/17:47/19:23)**
  - točna: every 60, Offset 19 (real :20) → **every 96, Offset 58, Also at 91 (real 13:11/14:47/16:23/17:59/19:35; 12:08/13:44/15:20/16:56/18:32)**
- **313** (need 1 → 1)
  - železniční stanice: every 120, Offset 97 (real 12:38/14:38/16:38/18:38) → **every 120, Offset 30 (real 13:31/15:31/17:31/19:31)**
- **314** (need 1 → 2)
  - železniční stanice: every 240, Offset 103 (real 14:44/18:44) → **every 120, Offset 0, Also at 89 (real 13:01/15:01/17:01/19:01; 12:30/14:30/16:30/18:30)**
  - konečná: every 240, Offset 44 (real 13:45/17:45) → **every 120, Offset 36, Also at 73 (real 13:37/15:37/17:37/19:37; 12:14/14:14/16:14/18:14)**
- **318** (need 2 → 2)
  - poliklinika: every 60, Offset 51 (real :52) → **every 240, Offset 49, Also at 117 (real 13:50/17:50; 14:58/18:58)**
  - hotel Visalaje: every 60, Offset 48 (real :49) → **every 240, Offset 47, Also at 107 (real 13:48/17:48; 14:48/18:48)**
- **341** (need 1 → 1)
  - železniční stanice: every 90, Offset 33 (real 12:04/13:34/15:04/16:34/18:04/19:34) → **every 120, Offset 78 (real 12:19/14:19/16:19/18:19)**
  - konečná: every 90, Offset 59 (real 12:30/14:00/15:30/17:00/18:30) → **every 120, Offset 119 (real 13:00/15:00/17:00/19:00)**
- **343** (need 1 → 1)
  - železniční stanice: every 90, Offset 49 (real 12:20/13:50/15:20/16:50/18:20/19:50) → **every 80, Offset 69 (real 12:50/14:10/15:30/16:50/18:10/19:30)**
  - restaurace Kněhyně: every 90, Offset 4 (real 13:05/14:35/16:05/17:35/19:05) → **every 80, Offset 14 (real 13:15/14:35/15:55/17:15/18:35/19:55)**
- **344** (need 2 → 2)
  - železniční stanice: every 60, Offset 4 (real :05) → **every 120, Offset 9, Also at 89 (real 13:10/15:10/17:10/19:10; 12:30/14:30/16:30/18:30)**
  - hotel Ondráš: every 60, Offset 19 (real :20) → **every 120, Offset 19, Also at 69 (real 13:20/15:20/17:20/19:20; 12:10/14:10/16:10/18:10)**
- **346** (need 1 → 1)
  - železniční stanice: every 60, Offset 51 (real :52) → **every 90, Offset 53, Also at 81 (real 12:24/13:54/15:24/16:54/18:24/19:54; 12:52/14:22/15:52/17:22/18:52)**
- **347** (need 1 → 1)
  - železniční stanice: every 60, Offset 29 (real :30) → **every 120, Offset 29, Also at 84 (real 13:30/15:30/17:30/19:30; 12:25/14:25/16:25/18:25)**
  - transformátor: every 60, Offset 56 (real :57) → **every 120, Offset 56, Also at 116 (real 13:57/15:57/17:57/19:57; 12:57/14:57/16:57/18:57)**
- **348** (need 3 → 3)
  - železniční stanice: every 60, Offset 52 (real :53) → **every 120, Offset 52, Also at 112 (real 13:53/15:53/17:53/19:53; 12:53/14:53/16:53/18:53)**
  - zámeček: every 60, Offset 15 (real :16) → **every 120, Offset 15, Also at 90 (real 13:16/15:16/17:16/19:16; 12:31/14:31/16:31/18:31)**
- **351** (need 3 → 3)
  - Náměstí Republiky: every 60, Offset 42 (real :43) → **every 120, Offset 42 (real 13:43/15:43/17:43/19:43)**
  - Lipové: every 60, Offset 15 (real :16) → **every 120, Offset 85 (real 12:26/14:26/16:26/18:26)**
- **358** (need 1 → 1)
  - Krytý bazén: every 180, Offset 0 (real 13:01/16:01/19:01) → **every 480, Offset 242 (real 13:03)**
  - PZ Hyundai - hlavní brána: every 180, Offset 84 (real 14:25/17:25) → **every 480, Offset 324 (real 14:25)**
- **702** (need 1 → 2)
  - školy: every 40, Offset 24 (real :05) → **every 90, Offset 4, Also at 24, 49, 64 (real 13:05/14:35/16:05/17:35/19:05; 13:25/14:55/16:25/17:55/19:25; 12:20/13:50/15:20/16:50/18:20/19:50; 12:35/14:05/15:35/17:05/18:35)**
  - autobusová stanice: every 40, Offset 9 (real :30) → **every 90, Offset 4, Also at 24, 34, 64 (real 13:05/14:35/16:05/17:35/19:05; 13:25/14:55/16:25/17:55/19:25; 12:05/13:35/15:05/16:35/18:05/19:35; 12:35/14:05/15:35/17:05/18:35)**
- **703** (need 1 → 2)
  - autobusová stanice: every 90, Offset 17 (real 13:18/14:48/16:18/17:48/19:18) → **every 480, Offset 257, Also at 269 (real 13:18; 13:30)**
  - PZ konečná: every 90, Offset 41 (real 12:12/13:42/15:12/16:42/18:12/19:42) → **every 480, Offset 302, Also at 307 (real 14:03; 14:08)**
- **704** (need 1 → 1)
  - autobusová stanice: every 60, Offset 44 (real :45) → **every 120, Offset 34, Also at 104 (real 13:35/15:35/17:35/19:35; 12:45/14:45/16:45/18:45)**
  - Podlesí konečná: every 60, Offset 3 (real :04) → **every 120, Offset 51, Also at 119 (real 13:52/15:52/17:52/19:52; 13:00/15:00/17:00/19:00)**
- **706** (need 1 → 1)
  - autobusová stanice: every 60, Offset 34 (real :35) → **every 120, Offset 39, Also at 94 (real 13:40/15:40/17:40/19:40; 12:35/14:35/16:35/18:35)**
  - konečná: every 60, Offset 59 (real :00) → **every 120, Offset 4, Also at 54 (real 13:05/15:05/17:05/19:05; 13:55/15:55/17:55/19:55)**
- **706 Osůvky** (need 1 → 1)
  - autobusová stanice: every 60, Offset 34 (real :35) → **every 120, Offset 34, Also at 89 (real 13:35/15:35/17:35/19:35; 12:30/14:30/16:30/18:30)**
  - konečná: every 60, Offset 4 (real :05) → **every 120, Offset 4, Also at 60 (real 13:05/15:05/17:05/19:05; 12:01/14:01/16:01/18:01)**
- **708** (need 1 → 2)
  - autobusová stanice: every 60, Offset 44 (real :45) → **every 30, Offset 14 (real :15)**
  - Kamionka: every 60, Offset 8 (real :09) → **every 30, Offset 8 (real :09)**
- **712** (need 2 → 2)
  - železniční stanice: every 60, Offset 39 (real :40) → **every 120, Offset 39, Also at 81 (real 13:40/15:40/17:40/19:40; 12:22/14:22/16:22/18:22)**
  - hájenka: every 60, Offset 2 (real :03) → **every 120, Offset 43, Also at 119 (real 13:44/15:44/17:44/19:44; 13:00/15:00/17:00/19:00)**
- **714** (need 1 → 1)
  - autobusová stanice: every 90, Offset 36 (real 12:07/13:37/15:07/16:37/18:07/19:37) → **every 120, Offset 36, Also at 89 (real 13:37/15:37/17:37/19:37; 12:30/14:30/16:30/18:30)**
  - ves: every 90, Offset 89 (real 13:00/14:30/16:00/17:30/19:00) → **every 120, Offset 62, Also at 119 (real 12:03/14:03/16:03/18:03; 13:00/15:00/17:00/19:00)**
- **715** (need 2 → 2)
  - Sosna nemocnice: every 30, Offset 19 (real :20) → **every 60, Offset 9, Also at 49 (real :10; :50)**
- **716** (need 1 → 2)
  - autobusová stanice: every 90, Offset 77 (real 12:48/14:18/15:48/17:18/18:48) → **every 120, Offset 34, Also at 79 (real 13:35/15:35/17:35/19:35; 12:20/14:20/16:20/18:20)**
  - konečná: every 90, Offset 29 (real 12:00/13:30/15:00/16:30/18:00/19:30) → **every 120, Offset 69, Also at 114 (real 12:10/14:10/16:10/18:10; 12:55/14:55/16:55/18:55)**
- **721** (need 1 → 1)
  - železniční stanice: every 40, Offset 30 (real :11) → **every 120, Offset 30, Also at 74, 110 (real 13:31/15:31/17:31/19:31; 12:15/14:15/16:15/18:15; 12:51/14:51/16:51/18:51)**
- **721 Mosty** (need 1 → 1)
  - železniční stanice: every 60, Offset 54 (real :55) → **every 144, Offset 54, Also at 119 (real 13:55/16:19/18:43; 12:36/15:00/17:24/19:48)**
  - osada Antoníček: every 60, Offset 18 (real :19) → **every 144, Offset 78, Also at 143 (real 14:19/16:43/19:07; 13:00/15:24/17:48)**
- **722** (need 1 → 2)
  - železniční stanice: every 40, Offset 34 (real :15) → **every 180, Offset 21, Also at 60, 84, 114, 134 (real 13:22/16:22/19:22; 14:01/17:01; 14:25/17:25; 14:55/17:55; 12:15/15:15/18:15)**
- **723** (need 1 → 1)
  - železniční stanice: every 60, Offset 34 (real :35) → **every 60, Offset 36 (real :37)**
- **732** (need 3 → 2)
  - autobusová stanice: every 60, Offset 54 (real :55) → **every 180, Offset 24, Also at 114 (real 13:25/16:25/19:25; 14:55/17:55)**
  - železniční stanice: every 60, Offset 1 (real :02) → **every 180, Offset 51, Also at 86 (real 13:52/16:52/19:52; 14:27/17:27)**
- **733** (need 1 → 1)
  - autobusová stanice: every 90, Offset 44 (real 12:15/13:45/15:15/16:45/18:15/19:45) → **every 120, Offset 109 (real 12:50/14:50/16:50/18:50)**
  - U Stonávky: every 90, Offset 19 (real 13:20/14:50/16:20/17:50/19:20) → **every 120, Offset 28 (real 13:29/15:29/17:29/19:29)**
- **734** (need 1 → 1)
  - autobusová stanice: every 90, Offset 71 (real 12:42/14:12/15:42/17:12/18:42) → **every 180, Offset 79, Also at 149 (real 14:20/17:20; 12:30/15:30/18:30)**
  - autobusová stanice: every 90, Offset 4 (real 13:05/14:35/16:05/17:35/19:05) → **every 180, Offset 4, Also at 124 (real 13:05/16:05/19:05; 12:05/15:05/18:05)**
- **735** (need 2 → 2)
  - autobusová stanice: every 60, Offset 49 (real :50) → **every 96, Offset 85 (real 12:02/13:38/15:14/16:50/18:26)**
  - střed: every 60, Offset 34 (real :35) → **every 96, Offset 87 (real 12:04/13:40/15:16/16:52/18:28)**
- **736** (need 1 → 1)
  - autobusová stanice: every 60, Offset 19 (real :20) → **every 160, Offset 4, Also at 114 (real 14:25/17:05/19:45; 13:35/16:15/18:55)**
  - hájenka: every 60, Offset 39 (real :40) → **every 160, Offset 24, Also at 134 (real 12:05/14:45/17:25; 13:55/16:35/19:15)**
- **738** (need 3 → 4)
  - Slovenská: every 30, Offset 16 (real :17) → **every 90, Offset 6, Also at 26, 51, 76 (real 13:07/14:37/16:07/17:37/19:07; 13:27/14:57/16:27/17:57/19:27; 12:22/13:52/15:22/16:52/18:22/19:52; 12:47/14:17/15:47/17:17/18:47)**
  - autobusové nádraží: every 30, Offset 11 (real :12) → **every 90, Offset 3, Also at 21, 41, 68 (real 13:04/14:34/16:04/17:34/19:04; 13:22/14:52/16:22/17:52/19:22; 12:12/13:42/15:12/16:42/18:12/19:42; 12:39/14:09/15:39/17:09/18:39)**
- **745** (need 1 → 1)
  - konečná: every 60, Offset 30 (real :31) → **every 120, Offset 75 (real 12:16/14:16/16:16/18:16)**
  - obch.stř.: every 60, Offset 11 (real :12) → **every 120, Offset 36 (real 13:37/15:37/17:37/19:37)**
- **745 Třanovice** (need 1 → 1)
  - konečná: every 90, Offset 20 (real 13:21/14:51/16:21/17:51/19:21) → **every 120, Offset 30 (real 13:31/15:31/17:31/19:31)**
  - křižovatka: every 90, Offset 65 (real 12:36/14:06/15:36/17:06/18:36) → **every 120, Offset 65 (real 12:06/14:06/16:06/18:06)**
- **747** (need 1 → 1)
  - autobusová stanice: every 90, Offset 14 (real 13:15/14:45/16:15/17:45/19:15) → **every 60, Offset 44 (real :45)**
  - Obecní úřad: every 90, Offset 49 (real 12:20/13:50/15:20/16:50/18:20/19:50) → **every 60, Offset 14 (real :15)**
- **748** (need 1 → 1)
  - Obecní úřad: every 90, Offset 43 (real 12:14/13:44/15:14/16:44/18:14/19:44) → **every 120, Offset 10, Also at 70 (real 13:11/15:11/17:11/19:11; 12:11/14:11/16:11/18:11)**
  - konečná: every 90, Offset 25 (real 13:26/14:56/16:26/17:56/19:26) → **every 120, Offset 39, Also at 89 (real 13:40/15:40/17:40/19:40; 12:30/14:30/16:30/18:30)**
- **750** (need 2 → 2)
  - autobusová stanice: every 60, Offset 29 (real :30) → **every 180, Offset 49, Also at 79 (real 13:50/16:50/19:50; 14:20/17:20)**
  - autobusové nádraží: every 60, Offset 39 (real :40) → **every 180, Offset 109, Also at 159 (real 14:50/17:50; 12:40/15:40/18:40)**
- **754** (need 2 → 2)
  - autobusová stanice: every 60, Offset 24 (real :25) → **every 144, Offset 5, Also at 44, 81 (real 13:06/15:30/17:54; 13:45/16:09/18:33; 14:22/16:46/19:10)**
  - autobusová stanice: every 60, Offset 19 (real :20) → **every 144, Offset 39, Also at 79, 129 (real 13:40/16:04/18:28; 14:20/16:44/19:08; 12:46/15:10/17:34/19:58)**
- **764** (need 1 → 1)
  - autobusová stanice: every 90, Offset 34 (real 12:05/13:35/15:05/16:35/18:05/19:35) → **every 180, Offset 34, Also at 79 (real 13:35/16:35/19:35; 14:20/17:20)**
- **766** (need 1 → 1)
  - autobusová stanice: every 90, Offset 34 (real 12:05/13:35/15:05/16:35/18:05/19:35) → **every 120, Offset 39 (real 13:40/15:40/17:40/19:40)**
- **770** (need 1 → 2)
  - železniční stanice: every 60, Offset 43 (real :44) → **every 180, Offset 44, Also at 110 (real 13:45/16:45/19:45; 14:51/17:51)**
  - konečná: every 60, Offset 59 (real :00) → **every 180, Offset 29, Also at 124 (real 13:30/16:30/19:30; 12:05/15:05/18:05)**
- **771** (need 1 → 1)
  - železniční stanice: every 90, Offset 49 (real 12:20/13:50/15:20/16:50/18:20/19:50) → **every 120, Offset 49 (real 13:50/15:50/17:50/19:50)**
  - náměstí: every 90, Offset 29 (real 12:00/13:30/15:00/16:30/18:00/19:30) → **every 120, Offset 59 (real 12:00/14:00/16:00/18:00)**
- **781** (need 2 → 2)
  - železniční stanice: every 60, Offset 2 (real :03) → **every 120, Offset 62, Also at 102 (real 12:03/14:03/16:03/18:03; 12:43/14:43/16:43/18:43)**
  - opevnění: every 60, Offset 29 (real :30) → **every 120, Offset 29, Also at 94 (real 13:30/15:30/17:30/19:30; 12:35/14:35/16:35/18:35)**
- **783** (need 4 → 3)
  - autobusová stanice: every 30, Offset 4 (real :05) → **every 180, Offset 27, Also at 74, 132 (real 13:28/16:28/19:28; 14:15/17:15; 12:13/15:13/18:13)**
  - škola: every 30, Offset 11 (real :12) → **every 180, Offset 31, Also at 76, 136 (real 13:32/16:32/19:32; 14:17/17:17; 12:17/15:17/18:17)**
- **784** (need 2 → 2)
  - železniční stanice: every 60, Offset 54 (real :55) → **every 180, Offset 114, Also at 179 (real 14:55/17:55; 13:00/16:00/19:00)**
  - Horní Přelač: every 60, Offset 18 (real :19) → **every 180, Offset 24, Also at 89 (real 13:25/16:25/19:25; 14:30/17:30)**
- **787** (need 1 → 1)
  - Na Paseky: every 90, Offset 69 (real 12:40/14:10/15:40/17:10/18:40) → **every 120, Offset 57 (real 13:58/15:58/17:58/19:58)**
  - autobusová stanice: every 90, Offset 19 (real 13:20/14:50/16:20/17:50/19:20) → **every 120, Offset 109 (real 12:50/14:50/16:50/18:50)**
- **985 Rožnov** (need 2 → 2)
  - Náměstí Republiky: every 120, Offset 112 (real 12:53/14:53/16:53/18:53) → **every 180, Offset 52 (real 13:53/16:53/19:53)**
  - autobusová stanice: every 120, Offset 14 (real 13:15/15:15/17:15/19:15) → **every 180, Offset 34 (real 13:35/16:35/19:35)**
