# Mělnicko: review of the branch re-check, 3 Nov 2026

Independent of the designer's notes: every EACH WAY flag of `audit-passing-2026-11-03-before.txt` and of the knot-fixed
`audit-passing-2026-11-03-now.txt`, every ONE WAY flag with 2 each way, every changed line and every "going home / garage / sleep"
claim was re-read from `data/derived/trips.json` at the flagged stop and at the stop where the variant leaves the trunk, counting
every trip that passes the stop wherever it starts or ends (the 381 reading). Live-map buses from `scripts/observed.py <line>
2026-11-02`. The designer's last pass (369 note, 370 section) was read before any edit.

**Result: two FIX rows (466, 369), everything else PASS.** Buses 110 → 115, Simutrans lines 45 → 47. `run_oblast.py melnicko`:
Step 4 95 timed legs, 94 ok, 1 FEWER (370 Postřižín, the v1 outstation row, unchanged); branch and path audits clean for the changed
lines; passing audit 9 EACH WAY (was 11: 466 and 369 gone), 10 ONE WAY, all with a verdict below.

## FIX

**466 Mělník – Kralupy nad Vltavou — FIX (town end; a missed short working).**
1. *Town end.* Read at Kralupy: of the six afternoon departures towards Mělník five start at obchodní centrum (12:45, 13:45, 14:45,
   15:45, 16:45; only the 17:55 at the station) and the 16:55 from Mělník ends there (the 14:50 and 15:55 at the station, 10 min before
   it). Both window slot trips out of Kralupy are obchodní centrum trips. The v1 line turned at the station, so the game bus stopped
   10 min short of where the real buses turn (the 314 rule: the town end the slot trips use); that is what the EACH WAY flag at obchodní
   centrum (4 each way) was. Changed: both legs end at Kralupy nad Vltavou, obchodní centrum; the Mělník → obchodní centrum leg keeps
   `core_to` železniční stanice (the station-ending trips count), the obchodní centrum → Mělník leg is read at the station as a knot
   (`knot_at` 55, so the 17:55 counts too) and timed back to obchodní centrum :45 (typed 44). Step 4 2/2 and 2/2 in the window, both
   exact; 4 buses as before. `rt` of the way back set by hand to 81 (the 13:45 / 15:45 road: 59 min to Spomyšl + the 16:45's 22 min
   Spomyšl → Mělník); the builder's median (94) mixed the trips that go round by Lužec. The 14:45, 16:45 and 17:55 run direct via Nové
   Ouholice — named on the card (the remaining ONE WAY flag at Nové Ouholice, 2 + 3, is exactly those three).
2. *466 Nelahozeves.* The designer's verdict C grouped the Kralupy – Nelahozeves shuttles by their ends ("3 each way at Kralupy but go
   to two different ends, 2 + 2 to Nelahozeves") — the start/end grouping of the 381 lesson. Read at Nelahozeves, u starého mostu, every
   shuttle passes it: out 15:44 (the 15:25, on to Veltrusy), 16:44, 17:44 and 18:44 (the 18:15 from obchodní centrum), back 16:11 (the
   16:06 from Veltrusy), 17:11, 18:11 — hourly at :44 / :11, 4 out and 3 back in 13:00–19:00, and with the :14 / :41 Mělník trips the
   Kralupy – Nelahozeves road runs every 30 minutes from 15:14. Verdict A. New Simutrans line `466 Nelahozeves`, every 60: Kralupy,
   železniční stanice :25 → Nelahozeves, u starého mostu (19 min), u starého mostu :11 → železniční stanice (19 min), `notvia` Spomyšl
   and Hořín, Brozánky (keeps every Mělník trip out, the Vraňany-road ones too; leg trips in `schedule.json`: 15:25, 16:25, 17:25, 18:25,
   18:55 and 16:11, 17:11, 18:11, nothing else). Step 4: window slots 16:25, 17:25 and 16:11, 17:11 = the real departures, 100 % exact.
   2 buses (waits 27 at Nelahozeves, 55 at Kralupy). On the 2 Nov live map the shuttles ran on the Mělník buses in their Kralupy layover
   (8058: Mělník 14:50 → station 16:00, 16:25 → Nelahozeves, 17:11 back, 17:55 → Mělník; 8081 an hour later), so pooling 466 with
   466 Nelahozeves is named in `notes`, not applied.
   Buses 4 → 6.

**369 Praha, Ládví – Mělník – Štětí — FIX (the :45 / :12 stream is modelled; the designer's E is overturned).**
Read at Zlonín, rozcestí, Mělník, Podolí and Mlazice: besides Ládví :00 (Štětí) and :30 (Mlazice), the road carries a third hourly
stream in the afternoon — out of Ládví 15:45 (to Podolí), 16:45, 17:45 (to Mlazice), i.e. Zlonín :04, Podolí :34; back Podolí 14:12,
15:12 and Mlazice 16:08, i.e. Podolí :12, Zlonín :46 — 3 each way at a repeating minute, same road and stops as the :30 trips (the 15:45
ends 3 stops short, at Podolí). The designer is right that it is not a branch, not a path variant and not separable from the :30 trips
by `via` / `notvia` (so a line of its own cannot pass Step 4 as the builder reads legs, and the brief's verdict A — "read at the stop
where it leaves the trunk" — has no such stop). But it is not "off the pattern" either: in the peak the Ládví – Mělník road runs three
times an hour each way, the model stands for the peak (method, "Which hour": 442 is modelled at 5 an hour), and Step 4's own ordering
prefers the row with more exact hits when both pass (Ládví :30 + :45: 22 exact of 28 against 18; Mlazice :53 + :08 read at Podolí: 14
against 11). The one-slot row passed only by the ±1 tolerance (3 real against 2 slots each way in the 16:00 window). Changed: 369's
Ládví leg `at` [30, 45] with `core_to` Mělník, Podolí (the 15:45 counts); the way back read at the knot Mělník, Podolí, `knot_at`
[57, 12], `knot_rt` 4 (the 14:12 and 15:12 start at Podolí; Mlazice is timed :53 and :08, typed 52 and 7); the line's anchor set to
15:30 by hand (window 15:00–17:00 — the builder's own busiest two hours were 14:50–16:50; the 16:00 window cuts the stream's last trip
back, so its 17:12 slot would be empty there). Step 4 in the window: out 15:30, 15:45, 16:30, 16:45 = 4 slots, 4 real, exact; back at
Podolí 15:12, 15:57, 16:12, 16:57 = 4 slots, 4 real, exact; 369 Štětí unchanged (15:00, 16:00 / 15:23, 16:23 at Mlazice, exact). Branch
and path audits ok. 6 buses (was 3). The stream runs 14:12–18:38 and on the 2 Nov live map it was 349 buses doing one 369 round each
between their 349 trips (8203: 369 14:12 then 349 15:40; 8213: 369 15:12 and 16:45; 8205: 349 15:10, 369 16:08 and 17:45; 8206: 349,
369 15:45, 349 16:54) — named on the card and as a pooling fact in `notes` (not an owner check: pooling is a card option). The
simpler one-slot row also passes Step 4 (by the ±1 tolerance) and would save 3 buses; since both rows are exact, Step 4's rule 3 (more
exact hits) decides for the two-slot row and the cheaper option is one sentence in the note, not an owner check (the coordinator's
3 Nov correction: checks only for an approximation with its slower option or a line kept / dropped for a stop). The designer's sentence
"its legs cannot be told from the :30 trips by `via` or `notvia`" (builder jargon on the owner's card) is gone. Buses 7 → 10.

## PASS (re-derived)

| Line | Flag | Reading at the stop (13:00–19:00) | Verdict | Designer |
|---|---|---|---|---|
| 857 | EACH WAY (before) | At Kralupy, železniční stanice every hour both ways: :55 towards obchodní centrum (even hours from Zákolany, odd from Minice), :55 away (even to Zákolany, odd to Minice). The town section is hourly in reality, every 120 in v1. `857 Minice` every 120 (obchodní centrum 15:43 → Minice 24 min, Minice 15:42 → obchodní centrum 26 min, `notvia` Zákolany): leg trips in `schedule.json` are 13:43, 15:43, 17:43 and 13:42, 15:42, 17:42 plus morning / evening ones, no Zákolany trip; window 1/1 exact each way; typed 42 / 41 (loop −1); 2 buses; the 13:43 on to Dolany, Debrno and the 17:42 on to Synthos pass Minice and are on the slot. Pooling fact (7309) in the note and `notes`. | A, correct | A ✓ |
| 368 | EACH WAY 8/8 at Kojetice, Tůmovka | The :15 / :33 trips run one stop past Předboj to Tůmovka and turn in 0 min (13 of 13); read at Předboj they are the :12 / :32 / :52 slot trips. Over 13:00–19:00 Předboj is the majority end (9 of 16 out end there; from 16:15 every trip), so the 314 rule keeps the game end at Předboj; Tůmovka is on 348 and 369. | E | E ✓ |
| 372 | EACH WAY 5/5 at Úžice | Out :34 hourly 14:34–18:34 (Zlosyň and Kralupy in turn) + Dřínov 13:57, Úžice shorts 16:57, 17:57; back 13:15, 14:15, 14:55, 15:25, 17:00, 17:33, 18:33 — no minute three times. At Zlosyň: out :48 hourly (5), back 13:58, 14:33, 15:03, 17:11, 18:11. Every 120 at the window's pair stands (2 real out against 1 slot at Zlosyň, ±1). The Zlosyň shorts have no return at a repeating minute; the designer's text fix is right (8039, the 14:03, goes on as 374). | D / C | D / C ✓ |
| 668 | EACH WAY 4/4 at Nebužely | Out 13:36, 14:20 (Řepín → Mšeno), 15:05, 15:46 (Mělnické Vtelno), 16:50, 17:51; back 13:08, 14:23, 15:43, 16:10 (→ Řepín), 16:42 (Vtelno), 17:42. No repeating minute, three ends. | C | C ✓ |
| 370 | EACH WAY 3/3 at Kralupy (before), 8/8 at Zdiby (now) | Kralupy trunk: out :20 (14:20–17:20) and :58 / :55 (14:58–18:55), extras 13:00, 13:35, 13:43, 16:15, 18:25; back :16 / :56 until 15:56, then the :16 becomes :25 via Veltrusy (15:25, 16:25, 17:25) — a time-band shift after the anchor window 14:10–16:10, B. Shorts read at Odolena Voda, Dolní náměstí: 16 out (Odolena Voda :09 hourly, Postřižín :59 hourly) against 9 back (14:05, 14:30, 14:50, 15:10, 16:05, 16:35, 17:20, 18:00, 18:10 — no minute three times): the outstation row 370 Postřižín at the inbound rate (knot 14:30, 14:50, 15:10, 16:05) is right, the one Step 4 FEWER is that choice. | B + D | B / D ✓ |
| 348 | EACH WAY 3/3 at Libiš, u slávisty | From 14:06 out :06 Libiš / :36 Obříství hourly, exact; back Obříství :57 hourly; Libiš 15:17, 16:32, 17:17, 18:17 (+ 13:24, 13:54, 14:46, 18:54): the every-120 pair 16:32 / 17:17 is the only row passing Step 4 (hourly :17 fails on 16:32). Flags = trips before 14:06 and the Libiš / U Vojtěcha swap. | B / C | B / C ✓ |
| 400 | EACH WAY 3/3 at Varnsdorf | Towards Varnsdorf hourly :10 from Letňany (14:10–17:10, arriving 17:03–19:57); back 14:28, 16:28, 17:58, 18:58 (two minutes, two each): hourly fails Step 4 (16:00 window holds only 16:28), every 120 at 16:28 exact. At Česká Lípa 6 towards Prague, 10 away. The outstation sentence was wrong (1085, 1088 come back as 17:58, 18:58) and is corrected; the model is the inbound rate either way. | C / D | C ✓ |
| 692 | EACH WAY 3/3 at Šemanovice | Shuttle out 13:00, 14:00, 16:00 (:00), back 13:45, 14:15, 16:15 (:15 twice, :45 once, 30 min apart): no third trip within 6 min. School shuttle; stops on 692. | C | C ✓ |
| 473 | EACH WAY 3/3 at Zálezlice | Out :58 hourly 15:58–18:58 (Zálezlice and Kralupy in turn), 13:21, 14:28, 15:13 off; back 13:26, 14:31, 15:16, 16:01, 17:25, 18:06, 18:55 — no minute three times. The two every-120 lines stand. | C | C ✓ |
| 658 | EACH WAY 3/3 at Veliká Ves | Works trips 13:20, 14:20, 15:07, 15:50, 16:29 out, 13:52, 14:52, 15:34, 16:22, 17:03 back: no minute. Every 90 on the 16:08 / 16:51 round. | C | C ✓ |
| 377 | ONE WAY 1/11 at Veleň | Peak out every 12 (15:22–16:58, 4 an hour), back every 15 (3 an hour); 20 against 18 in 13:00–19:00. Two path lines at the inbound rate; the text fix is right. | D | D ✓ |
| 349 | ONE WAY 1/5 at Pšovka | 14:55, 15:55, 16:55, 17:25, 17:55 on to Mlazice, back from Mlazice only 17:10 (the 349 buses come back on 369's :12 stream, see 369). Line ends at Podolí; Pšovka, Loděnická, Mlazice on 369. | D | D ✓ |
| 476 | ONE WAY 1/3 at Ovčáry | Brandýs → Mělník 13:03, 14:03, 15:03 pass Nedomice :24 and Kostelec :32 — on the knot slot; flagged only at the stops beyond Nedomice; out only 6:35. | D | D ✓ |
| 464 | ONE WAY 0/6 at Spomyšl | Horní Beřkovice → Mělník 12:44, 15:39, 17:24; shorts 14:04, 16:27 (→ Spomyšl), 14:39 (→ Vraňany); Spomyšl 14:45, 16:45 → Mělník are the 466 buses, carried by 466's way back (`core_to` Spomyšl, the game bus runs on). | C | C ✓ |
| 475 | ONE WAY 0/3 at Staré Brozánky | Same minutes, the way back calls at Hořín, Brozánky until 15:40 and at Staré Brozánky from 16:40; both stops are on the line (out at Staré Brozánky, back at Brozánky); the card names the road. | E | E ✓ |
| 316, 663, 351, 696 | ONE WAY 2/4, 2/4, 2/3, 2/3 | 316: hourly from 14:30, 13:05, 13:20, 13:45, 14:38, 18:36 off. 663: 12:56, 13:56, 14:36, 16:26 out, 15:13, 18:15 back, no minute. 351: three back trips via III.ZŠ 3 min before the slot. 696: sparse school trips. | C / B | ✓ |
| 466 Nelahozeves / Veltrusy shuttles | listed by the designer as C | see FIX 466 | A | C ✗ |

Cards claiming buses go home / sleep: 349 (right), 370 Postřižín (right, counted above), 372 ("the buses sleep out": the first 372 trip of
the day leaves Kralupy 5:28, right; the Zlosyň sentence corrected by the designer), 377 and 400 corrected by the designer — checked, right.
The oblast `notes` keep the general sentence.

## Table

| Line | Verdict | Change | Buses before → after |
|---|---|---|---|
| 466 | A (town end + short working) | both legs end at obchodní centrum (station as knot :55, obchodní centrum :45, typed 44; `rt` 81 by hand); new `466 Nelahozeves` every 60 (station :25 → u starého mostu, :11 back, typed 24 / 10, `notvia` Spomyšl, Hořín, Brozánky); note, whys, `notes` | 4 → 6 |
| 369 | A-type stream on the trunk | 369 Ládví `at` [30, 45] + `core_to` Podolí (typed 29, 44); Mlazice → Ládví read at knot Podolí [57, 12], `knot_rt` 4 (typed 52, 7); anchor 15:30; note (the 3-bus one-slot option named there), why; `notes` pooling fact 349 / 369; no owner check | 7 → 10 |
| 857 | A | designer's `857 Minice` verified, no change | 4 → 4 |
| 372, 377, 400, 475 | D / C / E | designer's text fixes verified, no change | unchanged |
| 368, 370, 348, 668, 692, 473, 658, 316, 663, 351, 696, 349, 476, 464 | as above | none | unchanged |

**Oblast bus total: 108 (v1) → 110 (designer) → 115 (review).** Simutrans lines 45 → 46 → 47.

## Audits after the rerun
- Step 4: 95 timed legs, 94 ok, 1 FEWER = 370 Postřižín (v1 outstation row, explained on its card).
- Branch: 369 (core_to Podolí, knot Podolí), 466 (core_to station / Spomyšl) all ok; 370 Postřižín, 476, 747 "beyond" as in v1.
- Path: 370 D8 Park trip, as in v1.
- Passing: 9 EACH WAY (368, 372, 668, 370, 348, 400, 692, 473, 658 — all with a verdict above), 10 ONE WAY (466 at Nové Ouholice: the
  three direct trips, named on the card; the rest as before).
- No "SLOT WITHOUT A REAL TRIP"; the "no slot in the window" lines are the v1 long-interval lines (400 Rumburk, 410, 663 Úžice, 691–695).
