> Superseded where `branch-review-2026-11-03.md` differs: 306 (the review added 306 Jeneč). The review stands. The review's 365 / 389 pooling owner check was moved to the cards by the coordinator (pooling options are never owner checks).

# kladensko: the branch re-check, 3 Nov 2026

Method: every flagged line was read from `data/derived/trips.json` and the 2 Nov live-map chains in `reading/<line>.txt`, by variant (first and last stop) and by the stops the trips pass, then each slot assignment was checked in `schedule.json` (`trips`, `dev`). A regular branch needs three trips each way 13:00 - 19:00 at a repeating minute where it leaves the trunk, counting trips that start further out and pass. Three branches were missed (365 Unhošť, 342 Knovíz, 389 Chomutov) and are now lines; everything else is the line's own pattern, an irregular working, a true outstation or a scan artefact, with the wrong card claims corrected.

After the change: `run_oblast.py kladensko` runs clean. Step 4: 133 timed legs, 132 ok, one FEWER (300 Kladno out leg, unchanged from v1, explained on the card). Branch audit: no new flag (the [beyond] of 650 is v1's). Path audit: the three v1 flags (858, 342, 306) are explained on the cards. Passing audit (rerun after the coordinator's loop-line fix): 7 lines EACH WAY (300, 306, 330, 399, 555, 350, 587; all B, C, D or E above, named on the cards) and 13 ONE WAY, no loop-line artefact in this oblast.

## 300 - EACH WAY, 9 each way, 15 one way at Praha, Nádraží Veleslavín
Off the pattern there (before): towards Prague (→) 12:50 13:00 13:50 14:45 14:50 15:25 15:50 17:08 18:00; from Prague (←) 13:30 14:30 14:45 15:15 15:30 15:38 16:30 16:38 16:45 17:20 17:28 17:40 18:20 18:28 18:40.
Variants at Nádraží Veleslavín: Smečno through trips (out hourly :00, exact; back :20 from 15:20, the 13:00, 14:00, 14:50 before are the same trips in another phase: B). Kladno shorts: out 14:15, 15:15, 15:45, 16:15, 16:45, 17:20, 17:40, 18:20, 18:40; back from Rozdělov 13:50, 15:25, 16:20, 17:00, 18:00, 18:20. Libušín shorts: out 14:30, 15:30, 16:30 (hourly, exact), back 14:30, 14:45, 15:50, 17:08 with no repeating minute (C). Hřebeč: out 15:38, 16:38, 17:28, 18:28, back 13:22 only (D, stops on 322). Sítná 14:45: one trip. Read at Kladno, u kostela with the Libušín and Smečno trips that pass it: 18 out and 17 back 13:00 – 19:00, so the afternoon is not a one-way outflow. Live map: five shorts come back as Rozdělov trips an hour or so later (14:15 → 15:25, 15:15 → 16:20, 16:15 → 17:00, 16:45 → 18:00, 17:20 → 18:20), the 15:45 and 18:40 go on as 324, the 17:40 as 616, the 18:20 ends.
**Verdict E (Kladno shorts: the surplus continues as 324 / 616, claim corrected), B (Smečno phase), C (Libušín), D (Hřebeč).** No line changed: 300 Kladno stays at the rate back from Kladno (the Step 4 FEWER row for its out leg stays, explained: two slots against four outs, the other outs are buses of 324 / 616 or the 18:20). Card: 'buses going home' replaced by the live-map facts, 14:15 taken off the off-pattern list (it is the 16:15 slot's repeat), the Libušín reason rewritten (no repeating minute back, instead of 'stops are on 300').

## 306 - EACH WAY, 6 each way, 8 one way at Praha, Zličín
Off the pattern there (before): towards Prague (→) 14:09 14:39 15:30 16:30 17:15 18:35; from Prague (←) 13:10 13:30 14:00 14:30 15:25 16:25 17:25 18:25.
Hostivice, Ve Vilkách shorts: every 30 before the every-20 stretch starts at 14:55 (Zličín 13:30, 14:00, 14:30; back 14:09, 14:39) and back 18:35 (9 min before :44): the line's own pattern in another phase. Jeneč, Lidická: out 13:10, 15:25, 17:25, 17:45, 18:25, 18:55; back 13:20, 14:20, 15:30, 16:30: out is :25 every 2 h from 15:25, back is hourly in two phases (:20, then :30), no minute with three trips both ways. Counting the trips that pass Jeneč, Lidická as the rule asks: the hourly Hostouň :05 trips pass it at :28 (15:28, 16:28, 17:28) and the Hostouň extras 16:25 and 17:15 pass at 16:48 and 17:30, so a Jeneč leg needs `notvia` Hostouň (else it passes Step 4 on Hostouň trips, the 292 failure); that leaves only its own trips (out 15:25, 17:25, 18:25; back 13:20, 14:20, 15:30, 16:30), the 16:25 slot of an hourly line has no trip, and only the every-120 option on the card (Zličín 17:25, Jeneč 16:30, 1 bus) passes. It stays an option, not a line. Hostouň 16:25 out and 17:15 back: one round. Kladno 12:59, 14:59, 18:03: variant paths, listed.
**Verdict B (Hostivice phase), C (Jeneč).** No line changed. Card: the Hostivice phase (13:30 – 14:30, 14:09, 14:39) and 18:35 added to the off-pattern list.

## 330 - EACH WAY, 6 each way, 7 one way at Praha, Nádraží Veleslavín
Off the pattern there (before): towards Prague (→) 13:28 14:13 14:33 15:08 16:43 16:55 17:35; from Prague (←) 14:20 15:55 16:55 17:33 17:53 18:33.
Veleslavín – Kladno: every 15 at the anchor (14:45 – 16:45), every 20 after 17:00 and 20 – 30 min before 14:20: the line's own shoulders (B); Havlíčkovo náměstí 16:55 (10 min) and 17:35 (5 min) were missing from the card's off list. Libušín (via Vinařice): out 14:50, 15:55, 16:55, 17:53 (hourly about :55), back 13:31, 15:46, 17:01 (no repeating minute) and 18:46 to Kladno, AN only; read at Kladno, Havlíčkovo náměstí it is four out, three back. Live map: the 15:55 returns as the 17:01, the 16:55 stays at Libušín, the 17:53 returns as the 18:46 to Kladno. A two-slot every-120 version (out 14:50, 15:55; back 15:46, 17:01) does not pass Step 4: 17:01 is 15:01 mod 120, a back slot inside the 14:45 - 16:45 window with no trip, so the one-round version stays.
**Verdict B (Veleslavín – Kladno), D (Libušín, claim corrected).** No line changed (330 Libušín keeps one round every 120 on 14:50 / 15:46). Card: 'buses going home' replaced by the live-map facts; 16:55 and 17:35 added to the off list.

## 399 - EACH WAY, 5 each way, 8 one way at Praha, Nádraží Veleslavín
Off the pattern there (before): towards Prague (→) 13:59 16:41 17:01 17:41 18:01; from Prague (←) 13:15 13:45 14:10 14:40 17:25 17:45 18:25 18:45.
One variant, Veleslavín – Kladno, Energie, same stops all day: every 30 at midday (out 13:15, 13:45, 14:10, 14:40; back 13:59), every 15 at the anchor, every 20 after 17:05 (out 17:25, 17:45, 18:25, 18:45; back 16:41, 17:01, 17:41, 18:01). The shoulders are the line's own pattern 5 – 10 min off the every-15 slots. No branch hidden.
**Verdict B.** None; the card already names the shoulders and the every-20 stretch.

## 365 - EACH WAY, 5 each way, 6 one way at Hostivice, centrum
Off the pattern there (before): towards Prague (→) 14:35 15:35 16:35 16:45 17:45 17:59; from Prague (←) 12:40 14:55 15:55 16:55 18:05.
Hostivice, centrum: from Motol 14:55, 15:55, 16:55, 18:05 (and 19:05) out, back 14:35, 15:35, 16:35, 17:59, 19:00: an hourly short working between the Stochov trips (Motol :25 out, Stochov :22 back), five each way read at Hostivice, Jeneček. It ends at Unhošť, náměstí until 16:35 and at Hostivice, Ve Vilkách from 16:55 (the 16:55, 18:05 out and the 17:59, 19:00 back). The card listed it as 'stops on 365'.
**Verdict A.** New Simutrans line 365 Unhošť, every 60: Motol :55 → Unhošť, náměstí (34 min), Unhošť :35 → Motol (35 min), `notvia` Kyšice keeps the Stochov trips out. Step 4: window 14:00 – 16:00, slots 14:55 15:55 = real 14:55 15:55 and back slots 14:35 15:35 = real 14:35 15:35 (out 2 of 2 exact, back 3 of 3 exact: 14:35, 15:35, 16:35; the 16:55 meets the :55 slot at Motol but ends at Ve Vilkách, so the leg does not count it). 2 buses. Judgment call: the strict count of trips that end at Unhošť is 2 out, 3 back; the line stands on the family count at Hostivice, Jeneček (5 each way), with the model hour's end (Unhošť); the Ve Vilkách end stays listed (two each way, stops on 306). The game line could instead end at Hostivice, Ve Vilkách; that would not match the model hour.

## 555 - EACH WAY, 3 each way, 5 one way at Žilina
Off the pattern there (before): one direction (→) 12:45 14:05 16:05; the other direction (←) 12:58 13:26 14:38 14:48 17:48.
Žilina: the line's own :35 out / :44 – :48 back pattern, 4 – 14 min off its slots (back 12:58, 13:26 from Újezd, 14:48, 17:48, 18:48), Kladno 12:45 (midday phase) and 16:05 (extra). Kladno – Běleč 14:05 and Běleč 14:38 – Kladno: one each way. No branch.
**Verdict B + C.** None to lines; card: 12:45 and 12:58 added (they pass Žilina after 13:00).

## 342 - EACH WAY, 3 each way, 4 one way at Stehelčeves, ObÚ
Off the pattern there (before): from Prague (→) 15:02 16:02 17:02 18:02; towards Prague (←) 14:39 15:53 16:53.
At Stehelčeves, ObÚ: four trips out of Prague at :02 to Knovíz (15:02, 16:02, 17:02, 18:02) and, towards Prague, three at :16 (Slaný 14:39, Knovíz 15:53, 16:53). Read at Knovíz (where the branch ends): arrivals :46, and the three back pass at 14:51 (the Slaný 14:39), 15:53, 16:53 - the hourly second service beside the main :09 / :32 line. Two buses (7705, 7706) run it; none comes back at 17:53 or 18:53 (the first trip of the day, 4:53, starts at Knovíz). The card listed it ('only two come back').
**Verdict A.** New Simutrans line 342 Knovíz, every 60: Veleslavín :02 → Knovíz (44 min), Knovíz :53 → Veleslavín (43 min), `notvia` Slaný keeps the main trips and the 14:39 out. Step 4: window 15:30 – 17:30, slots 16:02 17:02 = real 16:02 17:02; back slots 15:53 16:53 = real 15:53 16:53; 4 of 4 and 2 of 2 exact. 2 buses (waits 26 at Veleslavín, 7 at Knovíz). Judgment call: the trips that end or start at Knovíz are 4 out, 2 back; the third back trip is the Slaný 14:39 passing Knovíz (it stays on the main 342 as an extra).

## 350 - EACH WAY, 3 each way, 4 one way at Svrkyně
Off the pattern there (before): towards Prague (→) 13:20 15:01 17:15 18:18; from Prague (←) 12:50 14:05 17:05.
Svrkyně: the Kladno line's own minutes after the anchor (Kladno 13:20, 17:15, 18:18, 19:15, 12 – 17 min off the :03; Dejvická 12:50, 15 min off the :35), and the Noutonice tails of the Velké Přílepy shorts (14:05, 17:05 out, 15:01 back), which run two stops past Velké Přílepy and are covered by that line. No branch.
**Verdict B.** None to lines; card: 19:15 and Dejvická 12:50 added.

## 389 - EACH WAY, 3 each way, 3 one way at Údlice, rozcestí Pražská
Off the pattern there (before): one direction (→) 13:40 15:40 17:40; the other direction (←) 13:34 15:34 17:34.
Údlice, rozcestí Pražská: Louny, autobusové nádraží → Chomutov 13:34, 15:34, 17:34 and Chomutov → Louny 13:40, 15:40, 17:40 (odd hours, exact), the shuttles that make Louny – Chomutov hourly with the through trips (Louny :34 and Chomutov :40 every hour). Live map: the through buses run them in their wait at Chomutov (7760: Prague 13:15, Chomutov 15:40 → Louny, Louny 17:34 → Chomutov, Chomutov 18:48 → Prague). The card listed them ('stops on 389').
**Verdict A.** New Simutrans line 389 Chomutov, every 120: Louny, autobusové nádraží 13:34 → Chomutov, železniční stanice (40 min), Chomutov 13:40 → Louny (43 min), `notvia` Veleslavín keeps the through trips out. Step 4: window 15:30 – 17:30, slot 15:34 = real 15:34 and slot 15:40 = real 15:40; 3 of 3 exact each way (13:34, 15:34, 17:34 / 13:40, 15:40, 17:40). 2 buses; pooled with 389 as the real buses run it, 4 buses instead of 3 + 2 (option on the card, not applied).

## 587 - EACH WAY, 3 each way, 3 one way at Vinařice, rozcestí Třebichovice
Off the pattern there (before): one direction (→) 13:10 14:10 14:50; the other direction (←) 13:32 14:32 16:12.
Vinařice, rozcestí Třebichovice: Smečno → Libušín 13:10, 14:10 and Slaný → Libušín 14:50; Libušín → Smečno 13:32, Libušín → Slaný 14:32, Libušín → Drnek 16:12: school-day shuttles and long trips with different ends and no repeating minute (at the stop :21, :21, :00 towards Libušín, :36, :36, :16 back). Two each way of the same variant.
**Verdict C.** None; the card lists every one of them and the stop is a coverage exception.

## 627 - ONE WAY, 2 each way, 5 one way at Smečno
Off the pattern there (before): one direction (→) 13:40 14:40; the other direction (←) 13:07 14:01 14:40 15:29 18:10.
Smečno: Slaný → Smečno 13:40, 14:40 (hourly :40, then every 90: 15:40, 17:10, 18:40, which the model keeps) and Smečno → Slaný 13:07, 14:01, 14:40, 15:29, 18:10: mostly 324 buses from Prague going on (8 of 14 within 5 min), no repeating minute back.
**Verdict C.** None; the card says it.

## 388 - ONE WAY, 2 each way, 4 one way at Slaný, železniční stanice
Off the pattern there (before): towards Prague (→) 13:36 14:16 14:46 18:36; from Prague (←) 12:40 13:40.
One variant; the pattern shifts at 14:30 and 18:30 (Slaný 13:36, 14:16, 14:46, 18:36; Veleslavín 12:40, 13:40).
**Verdict B.** None; the card names them.

## 619 - ONE WAY, 2 each way, 4 one way at Třtice, u brodku
Off the pattern there (before): one direction (→) 12:15 13:35 15:35 18:05; the other direction (←) 14:32.
Out of Kladno 12:15, 13:35, 14:35, 15:35, 16:35, 18:05, back only Třtice 14:32 and Ročov 16:27 (Řevničov 12:49 and 19:41 pass Třtice outside the band): counting the trips that start further out, two come back against five out. The buses sleep at Třtice and Řevničov (4:14, 5:17 starts).
**Verdict D.** None; the card's 'buses going home' stands.

## 626 - ONE WAY, 2 each way, 4 one way at Pchery, Theodor
Off the pattern there (before): one direction (→) 14:07 14:25; the other direction (←) 12:39 13:39 14:04 17:39.
The Theodor shorts change from :39 to :09 at 14:04 (Kladno 12:39, 13:39, 14:04; Theodor 14:07, 14:25); the Velvary trips 13:09, 14:34. The line's own pattern in an earlier phase.
**Verdict B.** None; the card names them.

## 324 - ONE WAY, 2 each way, 3 one way at Smečno
Off the pattern there (before): one direction (→) 13:49 15:09; the other direction (←) 13:00 15:00 15:10.
Smečno – Slaný shuttles 13:00, 15:00 / 13:49, 15:09 and Kladno, gymnasium → Smečno 15:10: two each way, no repeating minute.
**Verdict C.** None; the card lists them.

## 307 - ONE WAY, 1 each way, 8 one way at Úhonice, škola
Off the pattern there (before): from Prague (→) 13:10 13:40 14:50 15:20 15:50 16:20 16:50 17:20; towards Prague (←) 14:16.
Zličín → Červený Újezd [PZ] 14:50 – 17:20 every 30 (six), no afternoon trip back; the morning goes the other way (6:26, 6:56, 7:26); two buses run it alternately; the stop is on 307 Unhošť. Úhonice 13:40 / 14:16: one each way. Unhošť shorts 17:05 and 18:05 (second departure of the hour): the 17:05's bus is not seen again that day, the 18:05's comes back as the 19:16; 17:35 is on the :35 slot.
**Verdict D (Červený Újezd), C (Úhonice), claim corrected (Unhošť).** None to lines; card: 'buses going home' for 17:35 and 18:05 corrected.

## 322 - ONE WAY, 1 each way, 3 one way at Tuchoměřice, rozcestí
Off the pattern there (before): from Prague (→) 14:00; towards Prague (←) 12:36 13:36 17:37.
Kladno 12:36, 13:36, 17:37, 18:37 (the line's own minute 10 min later) and Veleslavín 14:00 (5 min). No branch.
**Verdict B.** None; the card names them.

## 708 - ONE WAY, 1 each way, 3 one way at Slaný, modelářské středisko
Off the pattern there (before): one direction (→) 13:00; the other direction (←) 14:08 16:02 18:02.
Scan artefact: the game line's out leg runs via Slaný, Masarykovo náměstí (as the 11:28 does); the 14:08, 16:02, 18:02 take Slaný, modelářské středisko (a stop of 388, every 30), so that stop shows as off the leg's path.
**Verdict E.** None; the line's why says it.

## 858 - ONE WAY, 1 each way, 3 one way at Třebusice
Off the pattern there (before): one direction (→) 13:12; the other direction (←) 12:35 14:40 16:40.
Path variant in one direction: back from Slaný 12:35, 14:40, 16:40 via Brandýsek and Třebusice (stops of 620 and 342), 13:46 and 15:40 via Slaný, Netovice; out is one path. The game line takes the Netovice path; Třebusice and Brandýsek are served by 620 and 342.
**Verdict E.** None to lines; the line's why now names the two paths.

## 593 - ONE WAY, 0 each way, 5 one way at Velvary, železniční stanice
Off the pattern there (before): one direction (→) -; the other direction (←) 13:01 14:01 14:55 16:55 18:55.
Through running at Velvary: 13:01 is the back of the Slaný 11:33, 14:55 follows the Velvary – Hobšovice 14:01, 16:55 comes in on a 596 trip from Straškov; Slaný → Velvary runs every 2 h, so Velvary → Slaný at :55 is hourly only because of those buses.
**Verdict E.** None to lines; card: the reasons added to the off list.

## 220630 - ONE WAY, 0 each way, 4 one way at Chyňava, Lhotka u Berouna, náves
Off the pattern there (before): one direction (→) 12:13 12:43 13:39 14:13; the other direction (←) -.
Path variant: the Kladno trips 12:13 – 14:13 (and the Beroun trips back to 15:18) also pass Chyňava, Lhotka u Berouna, náves; the game line serves it on the way back (stops_via) and skips it on the way out, as the trips after 15:30 do.
**Verdict E.** None to lines; card: the sentence added.

## Table

| line | verdict | change | buses before → after |
|---|---|---|---|
| 300 | E (Kladno shorts: the surplus continues as 324 / 616, claim corrected), B (Smečno phase), C (Libušín), D (Hřebeč) | none (card claims corrected) | 6 → 6 |
| 306 | B (Hostivice phase), C (Jeneč) | none (card: Hostivice phase added) | 8 → 8 |
| 330 | B (Veleslavín – Kladno), D (Libušín, claim corrected) | none (card claims corrected) | 7 → 7 |
| 399 | B | none | 7 → 7 |
| 365 | A | new line 365 Unhošť (every 60, Motol :55 / Unhošť :35) | 4 → 6 |
| 555 | B + C | none | 3 → 3 |
| 342 | A | new line 342 Knovíz (every 60, Veleslavín :02 / Knovíz :53) | 3 → 5 |
| 350 | B | none | 5 → 5 |
| 389 | A | new line 389 Chomutov (every 120, Louny :34 / Chomutov :40) | 8 → 10 |
| 587 | C | none | 1 → 1 |
| 627 | C | none | 1 → 1 |
| 388 | B | none | 4 → 4 |
| 619 | D | none | 2 → 2 |
| 626 | B | none | 3 → 3 |
| 324 | C | none | 7 → 7 |
| 307 | D (Červený Újezd), C (Úhonice), claim corrected (Unhošť) | none (card claim corrected) | 5 → 5 |
| 322 | B | none | 3 → 3 |
| 708 | E | none | 2 → 2 |
| 858 | E | none (why extended) | 3 → 3 |
| 593 | E | none (card extended) | 1 → 1 |
| 220630 | E | none (card extended) | 7 → 7 |

**kladensko bus total (sum of the Simutrans lines' needs): 155 → 161.**

## Other cards that say buses go home, sleep or are an outflow (checked against the live-map chains)
- 300, 330, 307: checked above; the claims were wrong in part and are corrected on the cards.
- 600: Kladno 13:55 and 15:55 to Vinařice are the last trips of buses 8798 and 8817 on the live map (both end there); the card's 'buses going home' holds.
- 619: holds (above).
- Kladensko oblast note ('the Prague lines are outstation lines ... buses sleep in Kladno, Slaný, Libušín, Unhošť'): true of the first trips of the day; in the afternoon 300 is level at Kladno (18 out, 17 back), while 330 Libušín, 342 Knovíz, 600 and 619 send more out than back (confirmed above); the note was left as written.

