# praha-vychod: review of the branch re-check, 3 Nov 2026

Independent of the designer's notes: every EACH WAY flag of `audit-passing-2026-11-03-before.txt` and `-now.txt`, every ONE WAY flag with 2 each way, every changed card and every "going home / sleep / outstation" claim was re-read from `data/derived/trips.json` with my own passing reader (every trip 13:00–19:00 at the stop, wherever it starts or ends), and the live-map buses were pulled with `scripts/observed.py` for 335, 371, 343, 344, 303, 669, 653, 666. The diff against v1 (repo mirror) is card text only: 303, 335, 343, 344, 354, 411.

**Result: no missed branch; the model stands (128 buses, 69 Simutrans lines). One card claim (335) is rewritten so that it says what the plates show. The two open calls (343, 303) stay E, decided by the method as written below.**

## EACH WAY flags

| line | stop | my reading 13:00–19:00 | verdict | result |
|---|---|---|---|---|
| 371 | Klecany, u hřbitova | out to the Klecany ends 19 (Astrapark 12, Klecánky 5, Vodochody 2; four an hour 15:00–17:00 at :07 / :22 / :37 / :52), back 10 (Astrapark 13:42, 15:37, 16:07, 17:37; Klecánky 14:17, 15:07, 16:37, 17:07, 18:08; Vodochody 14:47): two an hour at :07 / :37. Řež trips use :34 / :04 out and :27 / :57 back, none of them on the Klecany road | D: true outstation; 371 Astrapark and 371 Klecánky every 120 give exactly the real :07 / :37 back. Řež: Kobylisy :15 / :45 from 14:15 to 17:15, :20 / :50 before and after (B, 5 min) | PASS |
| 411 | Zdiby | Holosmetky out 13:05, 14:05, 14:55, 15:55, 16:55, 18:31; back 13:28, 14:20, 15:16, 16:16, 17:16, 18:46. Brnky out 13:15, 14:15, 15:25, 16:25, 17:35; back 13:42, 14:38, 15:42, 16:44, 17:58 | B: :55 / :16 exact 14:55–17:16, two trips at :05 before it; Brnky approximate on the owner check | PASS |
| 353 | Praha, Čertousy | shorts out 15:28, 15:58, 16:58, 17:28; back 12:54, 16:04, 16:34 | D/C: 4 out, 2 back in the window, inside Prague, on the main line's stops | PASS |
| 354 | Mochov | back 13:11, 13:41, 14:41, 14:51, 15:31, 16:31, 17:45, 18:13; out arrivals 13:27, 13:42, 14:27, 15:27, 16:27, 17:33, 18:42, 18:57 | C: :00 / :31 exact in 15:00–17:00; :41 has only 13:41, 14:41 (and 12:41) | PASS |
| 335 | Hlubočinka / Radějovice | out 11 (Hlubočinka road 14:05, 15:05, 16:06, 17:20, 18:20; Radějovice road 13:34, 14:40, 15:31, 16:33, 17:52, 18:52), back 6, all by the Radějovice road | D, see below | FIX (card) |
| 343 / 344 | Nehvizdy, škola | arrivals 13:22, 13:57, 14:27, 15:27, 15:57, 16:57, 17:57, 18:57; departures 13:30, 14:00, 14:30, 15:30, 16:00, 17:00, 18:00, 19:00: eight rounds in six hours, the :50 / :00 round missing at 14:50 and extra :20 / :30 rounds at 13:15, 14:20, 15:20 | E, see below | PASS |
| 303 | Sibřina, škola | out 13:22 (Za Stodolami 12:57), 14:15 (13:33), 15:15 (14:33); back 13:10, 14:10, 15:10; nothing after 15:15 all day (the morning has 7:22, 9:35 / 7:42) | E, see below | PASS |
| 666 | Káraný, pošta | out arrivals 13:17, 14:17, 15:47, 16:47, 18:15, 19:15; back 13:22, 14:22, 15:52, 16:52, 18:22, 19:22 | C: one route; in the 15:00–17:00 window only :35 / :52 passes Step 4 (a :05 row has no real trip at 15:05, 16:05); the other pairs are 30 min off and named | PASS |
| 670 | Hlavenec | Brandýs 15:37, 16:37, 18:05 → Mečeříž; Mečeříž 16:02, 17:02, 18:32; shorts nádraží 12:58, 14:01, Kostelní Hlavno 13:40, 15:07, Sudovo Hlavno 14:28 | C | PASS |

### 335 — FIX (card only)
Read at Hlubočinka, obchodní centrum: 11 out, 6 back. Read on the Radějovice road: 6 out, 6 back, so by the passing reading alone the Radějovice trips have returns and the Hlubočinka trips (5 out, 0 back on their road) do not. The plates decide which trips are the surplus (the 290 rule): on the 2 Nov live map the Radějovice buses went on to 444 at Kamenice (13:34 9172, 14:40 9141, 15:31 9136, 17:52 9133, 18:52 9181; the 16:33 bus 9148 was next seen on the line at 18:20), while the Hlubočinka buses came back as the line's returns (15:05 9133 → 16:24, 16:06 9181 → 17:09, 17:20 9172 → 18:38). So the model (out by the Hlubočinka road at 16:06 / 17:20, back 16:24 / 17:09, every 120) stands for the trips whose buses come back, and the card's "going home" claim is right in substance but was written as if only 15:31 and 16:33 were off. Rewritten:
- "The Radějovice trips 15:31 and 16:33 out are buses going home (off the pattern)." → "The Radějovice trips out (13:34, 14:40, 15:31, 16:33, 17:52, 18:52) are off the pattern: they are the trips whose buses stay out there. On the 2 Nov live map the Radějovice buses went on to 444 at Kamenice (9172, 9141, 9136, 9133, 9181; the 16:33 bus 9148 was next seen on the line at 18:20), while the Hlubočinka buses came back as the line's 16:24, 17:09 and 18:38 (9133, 9181, 9172). Read at Hlubočinka, obchodní centrum the afternoon is 11 trips out and 6 back."
Model unchanged (3 buses). The Step 4 FEWER on the out leg is the outstation rule, on the card.

### 343 / 344 — E (a call, decided by the method)
Three each way at :20 / :30 (13:15 is 5 off) 13:15–15:30, as the designer says. I did not add a second Nehvizdy round, for three reasons from the method, not from the peak hour alone: (1) the Nehvizdy round is already a modelled leg of the 344 circuit (:50 / :00 hourly), so no stop and no destination is missing; the extra rounds are frequency, and the real service is 8 rounds in 6 hours, not two an hour (the :50 round is missing at 14:50); (2) as a leg of the 344 circuit (where the Nehvizdy round lives) its window is the circuit's 15:00–17:00, and a :20 / :30 leg would have real trips in 1 of its 2 window slots (15:20 only; 16:20 does not run), which fails Step 4; a standalone "343 Nehvizdy" line would get its own window (about 13:30–15:30, where 14:20 and 15:20 are real) and pass, so this reason only rules out the circuit leg, not a separate line; (3) either form puts three Nehvizdy rounds a day in the game that do not run (16:20, 17:20, 18:20), on stops the circuit already serves hourly. Reasons (1) and (3) carry the call. The live map confirms the designer's chains: 8145 did 13:48 → Horoušany 14:20 → Nehvizdy 14:20 / 14:30 → Horoušany 14:37 → Černý Most; 8062 the same at 15:20 / 15:30; from 15:48 the :48 bus (8020) turned at Horoušany without the round. If the coordinator reads the branch rule literally (3 each way in 13:00–19:00 is enough), the change is one leg pair in the 344 circuit (Horoušany :20 → Nehvizdy, Nehvizdy :30 → Horoušany, every 60, 0 extra buses) and the circuit becomes every 30 with four legs. Card text (343 and 344) gives the exact extra times. PASS as E.

### 303 — E (a call, decided by the method)
Three each way through Sibřina, škola and Na Paloučku, hourly, 12:57–15:15; from 15:33 every trip is direct, both ways, and the direct trips run every 30 all afternoon at :03 / :33 and :07 / :37. The škola road takes the :33 / :04 slot of the every-30 line only until 15:15, so a line for it would either halve 303 (the :33 slot going via škola at 16:33 and 17:33, when it runs direct) or add trips that do not exist. The method's rule for a slot that changes during the afternoon (534 / 535: take what runs it at the anchor) applies: the path at the anchor is direct. Sibřina, škola is on 765 (hourly) and Sibřina, Na Paloučku on the Prague bus sheet's 329 (its Květnice row runs Sibřina, Na Paloučku – Květnice – Dobročovice), checked in `stop_lines.json` and the Prague lines check sheet. The designer's corrected note says all this. PASS.

## ONE WAY flags with 2 each way
- 373 (Úžice, Netřeba): via Úžice out 13:31 (12:55), 14:31 (13:55), 15:18 (14:42), 16:48 (16:12), 18:48 (18:12); back 13:01, 15:01, 15:49, 16:35; direct out 15:32, 16:52, 17:32, back 13:52, 17:11, 17:45, 18:21. No three at one minute on either road; the model has the direct road out and the Úžice road back, exact in the window. C. PASS.
- 302 (U Vodojemu): the flagged 12:36, 13:04, 13:34, 13:37, 14:04 are before the every-20 pattern settles (from 14:24 the stop sees :03 / :27 / :47 out and :59 / :11 / :31 back). E. PASS.
- 492 (Jevany, Bohumil): out via Bohumil 13:08, 13:53, 14:58, 15:58, 17:58 (16:57 skips it); back via Bohumil 13:10, 14:10, 16:10 (12:52, 13:52, 15:52), skipped by 14:52, 16:52, 18:37. The out leg serves Bohumil, the back leg follows its slot trip's road. C. PASS.
- 667 (Tuřice): out :26 hourly from 14:26 (12:56, 13:56 via Otradovice); back 14:23, 16:23, 17:23, 18:23 on the :15 Benátky slot, the Horky trips 12:55 / 14:57 pass Tuřice 13:13 / 15:15 (8 min off), 15:45 8 off. C. PASS.
- 1-each-way flags (374 Ahold road, 489 Menčice / Vávrov roads, 669 Křenek road out only, 482 Pražská :22 trips, 375 band edge, 346 / 287391 / 761 loop artefacts, gone with the fixed script): no repeating minute each way; the cards name them. PASS.

## "going home / sleep / outstation" claims, by the passing reading and the plates
- 371 Klecany: 19 out, 10 back at u hřbitova. Right.
- 335: see above (FIX, card only).
- 669: Sudovo Hlavno 13:00–19:00 is 10 out (incl. the Mečeříž / Kostelní Hlavno trips) and 7 back; of the 15:05–17:35 every-30 trips 6 out, 5 back; the 16:35 bus (8022) was next seen on 379 at 19:45, every other out trip came back on 669 (8041: 15:05 → 15:33, 16:05 → 16:48, 17:35 → 18:13; 8120: 15:35 → 16:18, 17:05 → 17:33). The card's "16:35 is the departure left off" is exactly what the plates show. Křenek road: out only (13:24, 14:24, 15:54, 17:54), on 669 Mečeříž. Right.
- 653: 14:02 (1647) → 14:40 back, 15:50 (1625) → 16:47 back, 18:52 (1628) last trip of its day. "The bus sleeps at Poddubí" holds for the 18:52. Right.

## Audits after the rerun (`run_oblast.py praha-vychod`)
- Step 4: 140 timed legs, 137 ok; the 3 are by design and on the cards (371 Astrapark and 335 out legs FEWER = the outstation rule, 411 Brnky EMPTY = the approximate row on the owner check).
- Branch audit: 13 legs, all [ok]. Path audit: 5 slots (669 Křenek, 373 Úžice, 461 Dolní Lomnice, 489 Vávrov / Menčice), all named on the cards.
- Passing audit: 9 EACH WAY, 9 ONE WAY, each with a verdict above. Uncovered: only stops of other okresy (374 Postřižín, 667 Benátky / Horky, 876 Lobkovice), for the `--final` pass.

## Summary
| line | result | change |
|---|---|---|
| 335 | FIX | note: the off-pattern Radějovice trips named in full with the 2 Nov plates (Radějovice buses → 444, Hlubočinka buses → the 16:24 / 17:09 / 18:38); model unchanged |
| 343 / 344 | PASS (E, call) | none; the literal-rule alternative is written above (0 buses) |
| 303 | PASS (E, call) | none |
| 371, 411, 353, 354, 666, 670, 373, 302, 492, 667, 669, 653 and the 1-each-way flags | PASS | none |

**praha-vychod: 128 buses, 69 Simutrans lines** (unchanged from v1).
