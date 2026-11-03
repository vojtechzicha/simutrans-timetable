> Superseded where `branch-review-2026-11-03.md` differs: 637 (the review restored "buses going home" on live-map evidence). The review stands. The 631 / 649 pooling owner check was moved to the 649 card by the coordinator (pooling options are never owner checks).

# berounsko: the branch re-check, 3 Nov 2026

Work queue: the 6 EACH WAY and 11 ONE WAY flags of `audit-passing-2026-11-03-before.txt`, plus every card that says "going home" or "sleep". Every trip 13:00-19:00 was read at the stops it passes (`trips.json`, `reading/<line>.txt`), not by where it starts or ends. The rule applied: >= 3 each way 13:00-19:00 at a repeating minute, read where the variant leaves the trunk -> its own Simutrans line (Step 4 must pass), else a written reason.

**Result: one missed branch (631 Nižbor, u lípy), one wrong card claim (637), everything else stays.** Buses 65 -> 67.

## The audit script, before and after the fix
The before-file was made with a `passing_check.py` that (a) took the time offsets of a knot leg's stops from trips of both directions (no order check), and (b) marked every trip of a loop line off the pattern. Because of (a), 631's leg "Nižbor, Šnárová -> Všeradice (knot Beroun)" got offsets of about :16-:18 at Hýskov and Stradonice lávka from the opposite-direction trips, so the real Nižbor, u lípy -> Beroun trips 13:14, 14:14, 15:09, 16:09 counted as "on the pattern" and 631 showed only as ONE WAY (0 each way) instead of 4 each way. I found it by hand before the script was fixed: I read all 13 knot legs of my two oblasts (berounsko 384, 548, 631, 639, 641, 643, 825; praha-vychod 482, 657, 391, 461, 490, 765) and re-screened every line with two other tests (a trip counts as matched only at the leg's own `fr` / knot / `to` time; and start-end pairs with >= 3 each way). Only 631 turned up. The fixed script (knot order check, loop fix) confirms it: with `631 u lípy` taken out of the schedule it flags 631 EACH WAY, 4 each way at Nižbor, u lípy (out 13:25, 14:21, 15:28, 16:28; back 13:14, 14:14, 15:09, 16:09). The loop fix removed 861 from the flags (below).

## EACH WAY flags

**531** (Příbram, Archiv). Hořovice -> Archiv 12:05, 12:47, 13:25, 13:57, 14:35, 14:57; Archiv -> Hořovice 13:51, 14:21, 14:51, 15:21 (on to Jince), 15:51, 16:51. **E.** The hourly :57 trips running four stops past the model terminus (Příbram, autobusové nádraží) into Příbram town. At the bus station the Archiv starts pass at :57 and the 13:57 / 14:57 trips arrive at :56 (on the pattern); the rest are the school extras the card names (13:25, 14:35 out; 14:21 and Zdaboř 13:11 back). The stops beyond (Archiv, II. and III. poliklinika, Na Cihelně, Československé armády) are on Příbramsko 393, 395, 471, 472, 501 (checked in its schedule). No change.

**641** (Zdice, škola). Out via Trubín - Svatá - Zdice, škola: Beroun 13:00, 14:02 (on to Hořovice, on the pattern at Zdice :28 / :30), 14:07, 16:00, 18:00 (the last three end at Zdice, škola and run on as 640 :30). Back via Zdice, škola - Černín - Levín: Hořovice 12:50, 15:20; Zdice 14:32, 17:52. **C.** The way back has no repeating minute (:50, :32, :20, :52) and the three Trubín trips have no return on that road. Zdice shorts: Beroun -> Zdice 14:07, 15:37, 16:00, 18:00 and Zdice -> Beroun 13:57, 14:32, 17:52 (:07 :37 :00 :00 / :57 :32 :52, no repeating minute). The card lists them and says the Trubín trips run on as 640. Their stops are covered: Trubín and Svatá by 638, Zdice škola / Černín / Levín by 384 and 394. No change.

**643** (Podluhy, Na drahách). Hořovice, náměstí -> Podluhy 13:00, 14:00, 16:35; Podluhy -> Cerhovice 13:05, -> Tlustice 14:10 (Křešín round, back 14:56), Podluhy -> Hořovice 15:45, 17:45. **E.** Podluhy is a 5-minute spur off Hořovice and each short is the spur leg of a through trip (Hořovice 13:00 -> Podluhy 13:05 -> Cerhovice; Podluhy 15:45 after the 15:14 Třenice trip). Out 3, back 2, no repeating minute; the card lists the shorts and the Křešín round (Křešín and Felbabka are on 531). No change.

**394** (Zdice, náměstí). Read at Králův Dvůr, u zámku 13:00-19:00: out of Nové Butovice 20 (to Zdice 14: 13:40, 14:15, 15:00, 15:15, 15:30, 16:00, 16:30, 17:00, 17:20, 17:30, 17:45, 18:00, 18:30, 18:50; Počaply shorts 6: 14:40, 15:45, 16:15, 16:45, 17:10, 18:15), back toward Prague 12 (Zdice 13:28, 14:00, 14:33, 15:03, 15:33, 16:03, 16:33, 17:03, 17:33, 18:38, 18:58 and Králův Dvůr 15:30). **D.** True outstation: the Počaply shorts have one return in the afternoon (15:30 from Králův Dvůr, u zámku) and the extra Zdice departures at :15 / :45 are not matched either. The card says this and is right (the buses sleep at Zdice and Králův Dvůr, every 10 min into Prague 6:04-7:34). No change.

**526** (Hředle [BE 2]). Zdice -> Hředle 17:15, 18:47, back 17:24, 18:56; Zdice -> Žebrák 13:25; Bzová -> Zdice 12:50. **C.** One bus's fixed 120-minute sequence; the Hředle rounds come after the sequence and are not hourly (17:15, 18:47). Hředle is on the circuit, the card lists them. No change.

**529** (Hvozdec, myslivna). Hořovice -> Hvozdec 13:15, 15:05, 18:50; back 13:22, 15:12, 18:57 (6-minute shuttle). **B.** About every 110 min; no allowed interval fits; every 120 at 17:00 is the nearest (15:05 and 18:50 are 5 and 10 min off, 13:15 is 15 off). The card says so. No change.

## ONE WAY flags

| line | flag | verdict and reason |
|---|---|---|
| **631** | 0 each way, 6 one way at Králův Dvůr, u zámku | **A, fixed**, see below |
| **637** | 2 each way, 4 one way at Beroun, pod dálnicí | **C/E, card claim corrected.** The flagged inbound trips (Kublov 13:08, 14:08, 16:08, Roztoky 17:36) are on the :08 slots; the stop is on the outbound road only (path stop). The card said the 16:00-18:00 trips to Nový Jáchymov are "buses going home, they sleep there". Read at Nový Jáchymov: 16:00-19:00 three trips in (arrive 16:29, 17:29, 18:29) and two back through it (Roztoky, Placanda 17:36, a 638 bus running on, and Nový Jáchymov 19:00 -> Králův Dvůr); over the whole afternoon 6 out and 5 back; beyond it the Kublov end has 3 out and 4 back (13:00-15:00 / 13:08-16:08). So they are short workings of the hourly line, not buses going home. Card reworded; the model is unchanged (the 16:00-18:00 trips already count at `core_to` Nový Jáchymov) |
| **640** | 2 each way, 4 one way at Zdice, škola | **E.** The 13:08, 14:43, 16:28, 18:28 start at Zdice, škola, one stop before the leg's first stop Zdice, náměstí; 16:28 and 18:28 are the :30 slots (through trips from 641 via Trubín, on the card), 14:43 and 13:08 are off and named |
| **825** | 2 each way, 3 one way at Loděnice | **C/E.** The Mořina road variants (13:07 Mořinka, 13:14 and 18:49 back via Lužce, 18:14 out, 13:54 Loděnice -> Mezouň, Letník) are named on the card; the stops are on Praha-západ 311 or on the owner check |
| **380** | 1 each way, 11 one way at Praha, Vypich | **E.** Vypich is the stop the buses arrive at, the leg is timed at Kukulova (terminus alias); the Rudná shorts 14:30, 15:05, 16:05 run one way only, are listed, and their stops are on 380 |
| **384** | 1 each way, 4 one way at Tlustice | **C.** Zdice -> Hořovice 15:55 and 18:00, Hořovice -> Zdice 13:34, Zličín -> Hořovice 12:00 and 17:50 (the 17:50 sits in the :50 Zdice slot): named on the card with the reason. No repeating minute |
| **633** | 1 each way, 4 one way at Tetín, křižovatka | **C/D.** Zdejcina out 13:03, 14:03 (Liteň), 17:03, 18:03, 19:03 (Tetín), back from Tetín 16:29, 18:35: the evening Tetín shorts have one return in three; named on the card. At Tetín the two lines together give the hourly line (6 out, 6 back) |
| **527** | 1 each way, 3 one way at Cerhovice | **C.** One bus shuttling 12:31-16:34 (Žebrák 13:03, Cerhovice 13:44, Buzuluk 14:34 ...); the card names them |
| **548** | 1 each way, 3 one way at Záluží, v Brance | **C.** The extras 14:00-15:30 (Hořovice 14:37, Zbiroh 14:12 and 15:25) are named on the card, the anchor is 16:00 |
| **636** | 1 each way, 3 one way at Hýskov | **C/E.** Hýskov - Chyňava shorts 14:25, 15:20 out and 14:45, 15:45 back (2 each way, none after 15:51) and the 12:35 / 13:10 round; the stops are on Kladensko 630, named on the card |
| **861** | 0 each way, 3 one way at Beroun, sídliště | **E, artefact.** One-way loop from Beroun, autobusové nádraží (13:14, 14:04, 14:54 on the every-48 slots 13:16, 14:04, 14:52); the flag came from the loop bug and is gone with the fixed script |

## 631 - the one missed branch (verdict A)

Real trips Beroun / Králův Dvůr - Hýskov - Nižbor, u lípy, not via Šnárová, read at Nižbor, u lípy and at Beroun, autobusové nádraží:
- toward u lípy: Králův Dvůr 12:25 (Beroun :32), 13:25 (:32), 14:21 (:28), then Beroun 15:28, 16:28 (arrive u lípy 12:55, 13:55, 14:51, 15:51, 16:51)
- toward Beroun: u lípy 13:14, 14:14, 15:09, 16:09 (arrive Beroun 13:36, 14:36, 15:31, 16:31)

4 each way 13:00-19:00, hourly, at :28 (:32 once) and :09 (:14 twice), until 16:30. The old card filed them as "run through with 649". They do, but they are also a regular hourly branch of the trunk Beroun - Hýskov - Nižbor, so by the rule they are their own line. On the 2 Nov live map the same bus runs the whole round Beroun -> u lípy -> Žloukovice (649) -> u lípy -> Beroun: plates 9563 (12:25), 9794 (13:25 and 16:28), 9610 (14:21), 9565 (15:28), 5 of 5 rounds.

Change in `lines.json` (631): new Simutrans line **631 u lípy**, every 60:
- Beroun, autobusové nádraží -> Nižbor, u lípy, `at` [28], `notvia` Nižbor, Šnárová (keeps the Šnárová trips out), 23 min
- Nižbor, u lípy -> Beroun, autobusové nádraží, `at` [9], `notvia` Nižbor, Šnárová, 22 min
- no `lay` 0 (the bus waits 57 min at Beroun and 18 min at u lípy); **2 buses**.

Step 4: window 14:30-16:30, slots 15:28 / 16:28 out and 15:09 / 16:09 back = the real departures, all exact (out: 6 trips over the day, 3 exact, worst 4 min; back: 5 trips, 2 exact, 13:14 and 14:14 are 5 min later, the 7:24 morning trip is off). The builder's Step 4 audit: 87 timed legs, 87 ok. Card note, `why` and 649's note updated (a circuit with 631 u lípy would need 2 buses instead of 3).

New owner check "631, 649": the two are one bus round, so pooling = one circuit, 2 buses instead of 3 (-1 bus). Not applied. The oblast note on through running was updated.

Still listed on the card and still flagged (explained): Šnárová 13:32 -> Beroun, Králův Dvůr 13:56 -> Šnárová, Šnárová 17:36 -> Tmaň, Všeradice 13:50, 16:51, 18:13. The 13:25 and 14:21 start at Králův Dvůr, u zámku 7 min before Beroun (the new leg starts at Beroun, where the anchor trips 15:28 and 16:28 start), which is why they still show at Králův Dvůr in the passing audit.

## Audits after the change
- Step 4: 87 timed legs, 87 ok (before 85).
- Branch audit: the same flags as before, all explained on the cards (380; 384 and 384 Hořovice, the 17:20 Počaply short; 825 x2, the Prof. Veselého end).
- Path audit: 6 as before (384 17:20, 531 Křešín, 631 Málkov spur, 641 x2 Trubín and Zdice škola roads, 825 Prof. Veselého), all named on the cards.
- Passing audit (fixed script): 6 EACH WAY and 10 ONE WAY flags (861 gone), each with the verdict above; none changed its verdict. Nothing uncovered.

## Summary

| line | verdict | change | buses before -> after |
|---|---|---|---|
| 531 | E | none (Archiv end is Příbram town, stops on Příbramsko) | 3 -> 3 |
| 641 | C | none | 3 -> 3 |
| 643 | E | none | 1 -> 1 |
| 394 | D | none (card right) | 4 -> 4 |
| 526 | C | none | 1 -> 1 |
| 529 | B | none | 1 -> 1 |
| 637 | C/E | card claim "buses going home" corrected, model unchanged | 3 -> 3 |
| 640 | E | none | 2 -> 2 |
| 825 | C/E | none | 4 -> 4 |
| 380 | E | none | 6 -> 6 |
| 384 | C | none | 5 -> 5 |
| 633 | C/D | none | 2 -> 2 |
| 527 | C | none | 1 -> 1 |
| 548 | C | none | 2 -> 2 |
| 636 | C/E | none | 1 -> 1 |
| 861 | E | none | 1 -> 1 |
| **631** | **A** | **new Simutrans line 631 u lípy (every 60, :28 / :09, 2 buses); note, why, 649 note, oblast note, owner check "631, 649"** | **3 -> 5** |
| 649 | - | note only (circuit with 631 u lípy would save a bus) | 1 -> 1 |

**berounsko bus total 65 -> 67** (41 Simutrans lines, was 40).
