> Superseded where `branch-review-2026-11-03.md` differs: 415 (the review added 415 Žatec). The review stands.

# rakovnicko: the branch re-check, 3 Nov 2026

Method: as for kladensko: every flagged line was read from `data/derived/trips.json` and the 2 Nov live-map chains in `reading/<line>.txt`, by variant and by the stops the trips pass, and each slot assignment was checked in `schedule.json`. No missed branch in this oblast: the lines are a single Rakovník - Prague line with an irregular afternoon rate, long-distance lines with sparse trips, and school-day lines of single trips, each already listed on its card.

After the change: `run_oblast.py rakovnicko` runs clean. Step 4: 60 timed legs, 59 ok, one FEWER (404, v1, explained: the :10 departures end in Rakovník). Branch audit: no flag. Path audit: the three v1 flags (415, 760, 575) are explained in the lines' why texts. Passing audit (rerun after the coordinator's loop-line fix): 3 lines EACH WAY (304, 415, 711) and 8 ONE WAY (578 dropped out as a loop artefact); all named above.

## 304 - EACH WAY, 7 each way, 11 one way at Stochov, Slovanka II
Off the pattern there (before): towards Prague (→) 12:30 13:00 13:20 13:40 14:20 15:00 15:24; from Prague (←) 12:48 13:18 14:08 14:38 16:28 16:30 18:05.
One variant (Rakovník – Praha), no branch. Between 13:00 and 15:00 Rakovník sends seven buses to Prague (13:00, 13:20, 13:40, 14:00, 14:20, 14:40, 15:00) and Prague sends three back (Kukulova 13:18, 14:08, 14:38); from 15:30 to 17:30 the ends are level (Rakovník 15:30, 16:00, 16:40, 17:30; Kukulova 15:23, 15:58, 16:28, 16:53, 17:23), so 'the afternoon is an outflow from Prague' was wrong. The model keeps three slots each way every 120 (the rate of that second stretch; the Step 4 window 15:30 - 17:30 holds 3 Rakovník and 4 Kukulova departures). The three Rakovník - Zličín trips (13:20, 14:00, 15:30) are not a branch: live map, their buses go on from Zličín as the 305 of 15:05 to Karlovy Vary (13:20) and as the 404 of 15:40 and 17:40 to Kralovice (14:00, 15:30). Stochov 15:24 -> Vypich and Zličín 16:30 -> Stochov: one trip each.
**Verdict B / D, claim corrected.** No line changed. Card: the outflow claim rewritten with the counts; the Kukulova off-pattern minutes completed (12:48, 13:18, 14:08, 14:38, 18:05); the Zličín trips' onward lines named. The oblast note's open question about those trips is settled.

## 415 - EACH WAY, 3 each way, 5 one way at Žatec, autobusové nádraží
Off the pattern there (before): towards Prague (→) 13:47 15:47 17:50; from Prague (←) 13:05 14:15 14:40 17:00.
Žatec: Zličín → Kadaň 13:05, 14:15, 14:40 (via Nové Strašecí), 17:00, 18:40 (via Nové Strašecí) at no fixed minute (about two per 2 h); Kadaň → Prague every 2 h at :50 (12:50, 14:47, 16:50, 18:50) with the 13:47 via Nové Strašecí; Kadaň → Žatec 15:47 and 17:50: two short workings two hours apart. The Nové Strašecí variant is two trips out and one back. No repeating minute, nothing with three each way.
**Verdict C.** None to lines; card: the two Kadaň → Žatec shorts added.

## 711 - EACH WAY, 3 each way, 3 one way at Třeboc
Off the pattern there (before): one direction (→) 13:00 16:00 17:30; the other direction (←) 12:25 15:00 17:30.
Třeboc: through trips Rakovník 13:00, 17:30 (and 14:20 on the slot), Louny 12:25 (from Luna), 16:00; Louny → Třeboc 15:00, 17:30, 19:00 and Třeboc → Louny 16:00, 19:30: two each way before 19:00, minutes :00 / :30 alternating. Sparse school-day line, nothing regular.
**Verdict C.** None to lines; card: the Louny - Třeboc times added.

## 561 - ONE WAY, 2 each way, 6 one way at Rakovník, autobusové stanoviště
Off the pattern there (before): one direction (→) 12:45 13:00 14:00 15:10 15:16 16:30; the other direction (←) 14:40 15:13.
Single school-day trips with different ends (Senomaty, Nouzov, Petrovice, Řeřichy, the town loop): every flagged trip is on the card's list. The 581 Senomaty line carries the 561 trip Senomaty 17:33 through its `lines`, so that trip counts as on the pattern; the rest are single trips.
**Verdict C.** None.

## 562 - ONE WAY, 2 each way, 5 one way at Rakovník, autobusové stanoviště
Off the pattern there (before): one direction (→) 14:24 14:50; the other direction (←) 13:48 15:00 15:52 16:31 17:45.
The town service with the Transdev garage stop (a public stop): garáže 14:50 → střelnice, autobusové stanoviště → garáže 12:30, 15:00, 17:45, Olešná 16:31 → garáže, hasičský záchranný sbor 15:52: single workings to and from the garage stop at no repeating minute; every one is on the card.
**Verdict C / D.** None.

## 584 - ONE WAY, 2 each way, 3 one way at Rakovník, rozcestí Cikánka
Off the pattern there (before): one direction (→) 15:30 16:30; the other direction (←) 13:00 16:51 18:51.
School trips in two phases: Rakovník 12:15, 13:15 (:15) then 15:30, 16:30 (:30); Lhota back 13:00, 14:00 (:00), Krupá, Šustna 16:51, 18:51. Two each way of each phase; all on the card.
**Verdict C.** None.

## 404 - ONE WAY, 1 each way, 5 one way at Ruda, u rybníka
Off the pattern there (before): from Prague (→) 14:10 15:10 16:10 17:10 18:10; the other direction (←) -.
Zličín → Rakovník :10 hourly (15:10, 16:10, 17:10, 18:10, 19:10) and → Kralovice :40 (15:40, 16:40, 17:40, 18:40) against Prague-bound trips only until 15:45 (Rakovník 13:30, 14:35; Kralovice 14:40, 15:45); no trip from further out passes Ruda, u rybníka towards Prague after that. Live map: the :10 buses end in Rakovník (15:10, 17:10, 18:10, 19:10), the 16:10 goes on as a local 581.
**Verdict D (checked on the live map).** None; the card's 'buses going home' stands. Step 4's FEWER row for 404 (v1) stays explained by it.

## 576 - ONE WAY, 1 each way, 4 one way at Všetaty, rozcestí
Off the pattern there (before): one direction (→) 13:30 15:30 16:30 18:30; the other direction (←) -.
Rakovník → Slabce / Skryje 13:30, 14:40, 15:30, 16:30, 18:30 against Skryje → Rakovník 16:04 (and Slabce, pošta 13:53 / 16:44 on 575 / 572): the buses sleep at Skryje. Live map: the 16:30's bus goes on as a 574 to Křivoklát, the 18:30's returns at 20:19, so 'buses going home' was not exact.
**Verdict D, claim corrected.** None to lines; card: the wording replaced with what the buses do.

## 578 - ONE WAY, 1 each way, 4 one way at Rakovník, autobusové stanoviště
Off the pattern there (before): one direction (→) 17:50; the other direction (←) 12:00 12:15 14:45 17:20.
A circular school line (Rakovník to Rakovník): the round at 12:00 / 12:15 / 14:45 and the Nezabudice trip 17:20 / 17:50; the model's round is the 14:45. The flag came from the loop line's terminal time and is gone after the coordinator's passing_check fix; the card names every trip.
**Verdict C (flag was a loop-line artefact).** None.

## 560 - ONE WAY, 1 each way, 3 one way at Rakovník, Čs.legií
Off the pattern there (before): one direction (→) 14:45; the other direction (←) 12:34 14:02 18:00.
Hořovičky → Rakovník 12:34, 14:02, 18:00 and Rakovník → Kryry 14:45 are the school-day trips around the alternating Kolešovice / Hořovičky / Kryry hourly pattern; all on the card.
**Verdict C.** None.

## 575 - ONE WAY, 1 each way, 3 one way at Pavlíkov, Skřivaň
Off the pattern there (before): one direction (→) 15:00 16:00 17:00; the other direction (←) -.
Rakovník → Pavlíkov, Tytry 15:00, → Slabce, pošta 16:00, → Slabce, Kostelík 17:00 (the model's 17:00 slot): three different ends, one trip each; on the card.
**Verdict C.** None.

## 760 - ONE WAY, 0 each way, 5 one way at Vroutek, Kryrská
Off the pattern there (before): one direction (→) -; the other direction (←) 13:04 14:04 15:04 17:07 18:04.
Scan artefact: the back trips :04 run via Vroutek and Kryry, the game line takes the 16:15's path via Podbořany, nemocnice (the only service of that stop); the Vroutek stops are on the out leg. The card says it.
**Verdict E.** None.

## Table

| line | verdict | change | buses before → after |
|---|---|---|---|
| 304 | B / D, claim corrected | none (card claim corrected) | 5 → 5 |
| 415 | C | none | 3 → 3 |
| 711 | C | none | 2 → 2 |
| 561 | C | none | 1 → 1 |
| 562 | C / D | none | 2 → 2 |
| 584 | C | none | 2 → 2 |
| 404 | D (checked on the live map) | none | 4 → 4 |
| 576 | D, claim corrected | none (card claim corrected) | 1 → 1 |
| 578 | C (flag was a loop-line artefact) | none | 1 → 1 |
| 560 | C | none | 2 → 2 |
| 575 | C | none | 1 → 1 |
| 760 | E | none | 3 → 3 |

**rakovnicko bus total (sum of the Simutrans lines' needs): 47 → 47.**

## Other cards that say buses go home, sleep or are an outflow (checked against the live-map chains)
- 304, 404, 576: checked above (304 and 576 corrected).
- 563: 'the bus sleeps at Mutějovice' holds: bus 8383 runs 563 Rakovník 11:00, back 12:24, Rakovník 14:35, Mutějovice 15:54 and ends at Milostín; 8373 runs the 17:30 to Mutějovice and is not seen again.

