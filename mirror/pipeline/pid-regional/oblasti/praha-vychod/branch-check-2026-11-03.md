> Superseded where `branch-review-2026-11-03.md` differs: 335 (card text). The review stands.

# praha-vychod: the branch re-check, 3 Nov 2026

Work queue: the 9 EACH WAY and 12 ONE WAY flags of `audit-passing-2026-11-03-before.txt`, plus every card that says "going home", "sleep" or "outstation" (371, 335, 669, 653). Every trip 13:00-19:00 was read at the stops it passes (`trips.json`, `reading/<line>.txt`), not by where it starts or ends. The rule applied: >= 3 each way 13:00-19:00 at a repeating minute, read where the variant leaves the trunk -> its own Simutrans line (Step 4 must pass), else a written reason.

**Result: no missed branch in this oblast; one wrong card claim (303), three cards completed (335, 354, 411), 343 / 344 exact times.** The model is unchanged: 128 buses before and after, 69 Simutrans lines. I looked hardest at 371 (Klecany), 335, 353, 303 and 343, the ones that could be read as a branch; the reasons are below. Judgement calls are marked **(call)**.

I also read the six knot legs of this oblast by hand (482, 657, 391, 461, 490, 765), because the first `passing_check.py` took stop offsets of a knot leg from trips of both directions and could mark a short working as on the pattern (see the berounsko file, where it hid 631 u lípy). Nothing hidden here. I reran the audit with the fixed script (knot order check, loop fix): 9 EACH WAY and 9 ONE WAY flags (was 9 and 12); the loop flags 346, 287391 and 761 are gone (artefacts), 302 now shows 1 each way (its 13:04 matches the :01 slot) and 354 lost the 17:01 (it matches). No verdict changed. 490 (Strančice - Ondřejov - Stříbrná Skalice) folds the four Ondřejov turns into the Stříbrná Skalice line to keep the trunk's 1.5 an hour; the Stříbrná Skalice trips alone are 5 in six hours (passing Ondřejov :01, :29, :29, :59, :59), so there is no repeating minute to split on. That is a design choice (the card says so), not a missed branch.

## EACH WAY flags

**371** (Zdiby, u Celnice; the Klecany branch). Read at Klecany, u hřbitova: toward Astrapark / Klecánky / Vodochody 19 trips 13:00-19:00 (Kobylisy :08 :23 :38 :53 from 14:08 to 17:08, then 17:23, 17:40, 18:10, 18:40, plus 13:08, 13:40), back 11 (13:38, 14:12, 14:35, 15:02, 15:33, 16:03, 16:26, 17:02, 17:33, 18:03, 18:58). **D.** True outstation: four an hour out, two an hour back (at u hřbitova :07 / :37), nothing that starts further out and passes it (the Řež trips use :17 / :47). The Klecany ends are already their own Simutrans lines (371 Astrapark, 371 Klecánky, 371 Vodochody) timed at the inbound rate; the card's reason is right. The Řež flag part (Kobylisy 13:50, 17:50, 18:20, 18:50 five minutes after the :15 / :45 slots; Řež 13:15, 13:55, 14:25 ten minutes off) is **B**, the line's own approximate pattern. No change.

**411** (Zdiby, u Celnice). Holosmetky: Kobylisy 13:05, 14:05, 14:55, 15:55, 16:55, 18:31; back 13:28, 14:20, 15:16, 16:16, 17:16, 18:46. Brnky: Kobylisy 13:15, 14:15, 15:25, 16:25, 17:35; back 13:42, 14:38, 15:42, 16:44, 17:58. **B.** Two hourly services that drift (:05 / :15 until 14:20, :55 / :25 at 14:55-16:55, later again): the minutes the model holds are the anchor's (:55 / :16 and :25 / :42). The Brnky drift is already on the owner check; the card did not name the Holosmetky trips off the :55 / :16 slots (Kobylisy 13:05, 14:05, 18:31; Holosmetky 13:28, 14:20, 18:46), now added. No model change.

**353** (Praha, Černý Most). Černý Most -> Čertousy shorts 15:28, 15:58, 16:58, 17:28 (4), back Čertousy -> Černý Most 16:04, 16:34 (2; also 12:54, arriving 13:05). **D.** Inside Prague, every stop is on the main 353 trips (Svémyslice -> Černý Most pass Čertousy :19 / :49); out 4 against back 2, so the "each way 4" of the audit comes from adding the Svémyslice 14:55 extra and the 12:54. The card lists them and is right. No change.

**354** (Praha, Černý Most). Mochov: Černý Most 13:00, 13:15, 14:00, 15:00, 16:00, 17:00, 18:15, 18:30; Mochov 13:11, 13:41, 14:41, 14:51, 15:31, 16:31, 17:45, 18:13. Mochovská: Černý Most 14:30, 15:30, 16:30, 17:35; Mochovská 15:06, 16:06, 17:01. **C.** The hourly :00 / :31 and :30 / :06 patterns are modelled (two Simutrans lines); the rest has different minutes (:11 :41 :41 :51 :45 :13 back; :15 :15 :30 out). The card named the Mochov extras 13:11-14:51; added Černý Most 13:15, 18:15, 18:30 and Mochov 17:45, 18:13. No model change.

**335** (Sulice, Želivec). Out of Budějovická via Hlubočinka (H): 14:05, 15:05, 16:06, 17:20, 18:20; via Radějovice (R): 13:34, 14:40, 15:31, 16:33, 17:52, 18:52. Back from Kamenice, all by the R road: 13:16, 14:23, 15:10, 16:24, 17:09, 18:38. Kamenice -> Želivec shorts 13:46, 16:06 (go on as 339). **D.** Read at Hlubočinka, obchodní centrum: 11 out, 6 back; the extra five are the H trips, which have no way back on their road. The model takes H out (the only service of Sulice, Hlubočinka) and R back, both at 1 an hour, and lists the R trips out as extras. Card right; the R list lacked 18:52, now added. No other change.

**343** (Nehvizdy, škola) **(call)**. Extra Horoušany -> Nehvizdy 13:15, 14:20, 15:20, back 13:30, 14:30, 15:30: three each way, hourly, but only until 15:30, and the second 344 bus does them (9 of 9 chains). **E.** Same route as the Nehvizdy round already modelled in the 344 circuit (:50 / :00 hourly), no new stop; it is extra frequency of the 13:00-15:30 stretch only, and the 16:00 peak has one round an hour. A second round would fill the 344 bus's wait (0 buses) but would be wrong at the anchor. Card now gives the exact times. If the coordinator reads the rule literally (3 each way, 13:00-19:00) this is the one to overrule: it would be a second 343 round in the 344 circuit, window 14:00-16:00, no extra bus.

**303** (Sibřina, škola) **(call)**. Via Sibřina, škola / Na Paloučku: out Šestajovice, Za Stodolami 12:57, Černý Most 13:33, 14:33; back 13:04, 14:04, 15:04. Three each way, hourly (:15 out, :10 back at škola), **none after 15:20**, every later trip goes direct. **E.** A path variant of the early afternoon, not of the peak. The card said "those stops are on 765": true for Sibřina, škola (765 hourly), **wrong for Sibřina, Na Paloučku**, which is on 329 of the Prague bus sheet. Card corrected, with the reason there is no line.

**666** (Nový Vestec, u mostu). Out 13:05, 14:05, 15:35, 16:35, 18:03, 19:03, each back +17 (13:22, 14:22, 15:52, 16:52, 18:22, 19:22). **C.** One route, pairs of hourly trips with 90-minute gaps; the model holds the 15:35 / 16:35 pair at :35 / :52, the other pairs are named on the card as 30 min off. No new stop. No change.

**670** (Hlavenec). Brandýs, nádraží 12:58 -> Mečeříž, 14:01 -> Sudovo Hlavno, Brandýs 18:05 -> Mečeříž; back Kostelní Hlavno 13:40, 15:07, Sudovo Hlavno 14:28, Mečeříž 18:32. **C.** Different ends and minutes, the hourly :37 / :02 line is modelled; the card names the shorts. No change.

## ONE WAY flags

| line | flag | verdict and reason |
|---|---|---|
| **373** | 2 each way, 5 one way at Úžice, Netřeba | **C.** Two roads in no regular order: via Úžice out 13:55, 14:42, 16:12, 18:12, back 14:50, 15:38, 16:24; direct out 15:32, 16:52, 17:32, 18:52, back 13:52, 17:11, 17:45, 18:21. No repeating minute on either road; the card puts the direct road out and the Úžice road back so both are on the line. No change |
| **302** | 2 each way (1 with the fixed script), 3 one way at Praha, U Vodojemu | **E.** Letňany 13:34 (Vinořská), Veleň 12:36, 13:37, Vinořská 14:04 are before the pattern settles (:01 / :24 / :44 out, :32 / :12 / :52 back from 14:24); the stop is passed only by some paths. No new branch |
| **492** | 2 each way, 3 one way at Jevany, Bohumil | **C.** Kostelec 13:04, 13:49, Voděrady 12:52, 13:52, 15:52 skip or take the Bohumil stop; hourly :54 / :52 is modelled. The card says some trips skip it |
| **667** | 2 each way, 3 one way at Tuřice | **C.** The Otradovice road (12:56, 13:56), the Horky trips (12:55, 14:57) and Benátky 15:45; named on the card, hourly :26 / :15 modelled |
| **374** | 1 each way, 4 one way at Klecany, Ahold | **C.** Out via Ahold 13:30, 14:00, 17:30, 18:00; back via Ahold 13:36, 14:08, 14:38, 16:38, 17:38, 18:14 (direct back 12:56, 15:11, 16:11, 17:11, 19:01). The road alternates in no regular order and has the :00 / :30 grid on both; the card puts the Ahold road on the way back |
| **489** | 1 each way, 4 one way at Všestary, Menčice | **C.** Menčice / Vávrov roads alternate in either direction; Louňovice - Mukařov shuttles 13:04, 15:14 / 13:15, 15:21 (2 each way) and Strančice 18:34 -> Klokočná are named on the card, their stops are on the line |
| **669** | 1 each way, 4 one way at Křenek | **D.** The Křenek road (Dřísy, železniční stanice) is taken out only: 12:56, 13:56, 15:35, 17:35, never back in the afternoon; its stops are on 669 Mečeříž. Outstation card checked: Sudovo Hlavno 6 out (15:05-17:35) against 5 back, the 16:35 left off is the one trip whose bus (8022) has no later trip in the reading; wording right |
| **482** | 1 each way, 3 one way at Kly, Krauzovna | **E.** The Pražská -> Mělník :22 trips (14:22, 15:22, 16:22) take a road the other trips do not; they are in the every-30 peak pattern. No change |
| **346** | 0 each way, 13 one way at Praha, Černý Most | **E, artefact.** One-way loop starting and ending at Černý Most; flag gone with the fixed script |
| **287391** | 0 each way, 6 one way at Úvaly, ž. s. | **E, artefact.** Loop that passes its start stop; one bus on every trip (7981); flag gone with the fixed script |
| **761** | 0 each way, 5 one way at Velké Popovice | **E, artefact.** Loop; 14:55, 16:55, 17:55 on the :55 slot, 13:21 and 15:50 off, named; flag gone with the fixed script |
| **375** | 0 each way, 3 one way at Praha, Českomoravská | **E.** Brandýs 12:53, 13:13, 18:08 sit on the edge of the every-15 band (13:13-17:48); card says so |

Claims "buses sleep / going home" checked by the passing reading: 371 (19 out, 11 back at Klecany), 335 (11 out, 6 back at Hlubočinka), 669 (6 out, 5 back at Sudovo Hlavno; one bus does not return), 653 (out 14:02, 15:50, 18:52, back 14:40, 16:47; the 18:52 has no return) - all right as written.

## Audits (unchanged by my edits)
- Step 4: 140 timed legs, 137 ok. The 3 that do not pass are by design and on the cards: 371 Astrapark and 335 have fewer slots out than real departures (the outstation rule, the extras are listed), 411 Brnky is the approximate row on the owner check.
- Branch audit: 13 legs, all [ok]. Path audit: 5 slots (669 Křenek, 373 Úžice, 461 Dolní Lomnice, 489 x2 Vávrov / Menčice), all named on the cards.
- Passing audit (fixed script): 9 EACH WAY and 9 ONE WAY flags (the three loop lines gone), each with the verdict above; none changed its verdict. Uncovered: only the stops already explained.

## Summary

| line | verdict | change | buses before -> after |
|---|---|---|---|
| 371 | D (Klecany), B (Řež) | none | 8 -> 8 |
| 411 | B | card: Holosmetky off-pattern trips added | 2 -> 2 |
| 353 | D | none | 4 -> 4 |
| 354 | C | card: later extras added | 3 -> 3 |
| 335 | D | card: 18:52 added to the Radějovice trips | 3 -> 3 |
| 343 | E (call) | card: exact extra times (and 344's note) | 2 -> 2 (344: 3 -> 3) |
| 303 | E (call) | card claim corrected (Na Paloučku is 329, Prague sheet; the variant ends 15:20) | 4 -> 4 |
| 666 | C | none | 1 -> 1 |
| 670 | C | none | 1 -> 1 |
| 373 | C | none | 3 -> 3 |
| 302 | E | none | 4 -> 4 |
| 492 | C | none | 2 -> 2 |
| 667 | C | none | 2 -> 2 |
| 374 | C | none | 3 -> 3 |
| 489 | C | none | 2 -> 2 |
| 669 | D | none | 3 -> 3 |
| 482 | E | none | 7 -> 7 |
| 346 | E | none | 2 -> 2 |
| 287391 | E | none | 1 -> 1 |
| 761 | E | none | 1 -> 1 |
| 375 | E | none | 7 -> 7 |

**praha-vychod bus total 128 -> 128** (69 Simutrans lines, unchanged).
