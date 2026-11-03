> Superseded where `branch-review-2026-11-03.md` differs: 675 (card text). The review stands.

# Kolínsko: the branch re-check, 3 Nov 2026

Method: `BRANCH_BRIEF.md`. Work queue: the 3 EACH WAY and 12 ONE WAY flags of `audit-passing-2026-11-03-before.txt` for this oblast. After the coordinator's fix of
`passing_check.py` for loop lines I reran it: Mělnicko's flags are unchanged; here the 659 EACH WAY flag (Krupá) and the 460 flag went
away and 659 appeared as ONE WAY at Prusice, rozcestí (see 659); 661 reads 2 + 3 instead of 2 + 4. The tables below use the corrected flags.
For each line I read every real trip 13:00–19:00 at the flagged stop and at the other stops where it leaves the trunk, both directions,
counting trips that start further out and pass the stop (`data/derived/trips.json`, `reading/<line>.txt`, plus a stop-by-stop listing
of every stop with 2 or more unmatched trips each way). A branch needs 3 or more trips each way at a repeating minute, and Step 4 per
leg. Times below are trip starts, as in the audit.

**Result:** no line is added; 659's out leg now follows the road of its window trips. The strongest candidate, the Kounice – Mochov shuttle on 662, has 6 trips each way but its way back has
no repeating minute; it is on the owner checks as an approximate line (+2 buses) instead of being modelled. Every other flag is the
line's own pattern read at a stop the modelled leg does not list, a time-band change, an irregular set or a true outstation. No card
claim was wrong; the 662 card now gives the shuttle's real minutes. Buses 71 → 71.

## EACH WAY flags

**662 (Čelákovice – Kouřim), C for the way back, owner check added.** Flagged at Kounice (6 each way). Kounice – Mochov shuttle, 18 min over
Vyšehořovice and Vykáň (it leaves 662's road at Černíky for Kounice, which is on 661):
- out of Mochov 12:42, 13:27, 14:27, 15:27, 16:27, 17:33, 18:57 (:27 four times, then 6 and 84 min later);
- back from Kounice 13:23, 14:33, 15:13, 16:13, 17:27, 17:55 (:23, :33, :13, :13, :27, :55: no repeating minute).
It runs on the 354 buses (bus 1688: 354 Černý Most 13:00 → Mochov 13:27 → Kounice 13:45, back 14:33 → Mochov 14:51 → 354 to Prague 14:51;
12 of its 13 Mochov arrivals go on as 354, and 12 of 13 Mochov departures follow a 354 arrival). The other off-pattern pair at Vykáň, Čelákovice → Vykáň 15:23, 16:23, has no
return and is listed.
Step 4 for the shuttle as a line, tried: Mochov :30 → Kounice and Kounice :13 → Mochov, every 60, anchor 16:00: the way out passes (slots
15:30, 16:30 against 15:27, 16:27), the way back fails (EMPTY: slots 16:13 and 17:13, no real trip near 17:13; real in the window 16:13 and
17:27, 74 min apart, so no hourly minute fits both). Only with the anchor of 662 moved to 15:00 and the way out at :27 does it pass (all 79 legs ok, need 2),
by choosing the window, not by the trips. Verdict: not a line here (a way back without a repeating minute is the 381 test failing).
It is a choice for the owner, so it is on the owner checks with its cost: 662 Kounice every 60, Mochov :27 → Kounice, Kounice :13 → Mochov,
approximate on the way back (15:13, 16:13 exact; 13:23, 14:33, 17:27 are 10, 20, 14 min off), 2 buses (+2).
Change: 662 `note` (shuttle minutes and reason), one owner check. No Simutrans line change.

**235002 (MHD Kolín 2), E.** Flagged at Kolín, Šťáralka (4 each way): Štítary → Šťáralka 17:01, 17:31, 18:01, 18:31 and Šťáralka → Štítary
17:41, 18:11, 18:41 (+ the short 14:08): the line runs every 20 until 16:56 / 17:15 and every 30 afterwards. A time-band change on the same
route, not a branch; the model stands for the afternoon peak (anchor 14:50, every 20). The card says "then every 30". No change.

**659, C; stop path corrected.** Before the fix flagged EACH WAY at Krupá [KO] (3 each way: out 13:55, 14:55, 15:25; back 12:58, 13:50, 14:50).
With the corrected audit that flag is gone and the same stop reads ONE WAY: Kostelec → Krupá 12:58 and Kostelec → Český Brod 13:50, 14:50
against one trip the other way (Český Brod → Kostelec 15:25): a short working of 3 trips on two minutes, one way, stops on 659, listed on
the card. The 13:55 and 14:55 main trips (5 min before the :00 slot) are on the card.
The first corrected run also flagged Prusice, rozcestí (ONE WAY, 3): Český Brod 16:00, 17:00, 18:00 → Stříbrná Skalice go via Prusice,
rozcestí, the back trips (:37, all via Prusice) and the 13:55, 14:55 outs go via Prusice. The leg's stop list followed the minority
13:55 / 14:55 road, so the window's own trips (16:00, 17:00) were off the modelled path and Prusice, rozcestí was on no leg (it is a stop of
okres Praha-východ that no other sheet serves, listed in the run as uncovered in another okres). Out by one road, back by the other is the
fork-schedule circuit rule (as 536, 329), so the fix is the out leg's road, not a second line.
Change: out leg `stops_via` Prusice, rozcestí; the `why` now names that road and says the 13:55 and 14:55 call at Prusice. Times, slots
and buses are unchanged (Step 4 still 77 of 77, 3 buses); Prusice, rozcestí is covered by 659 (468 stops on this sheet, was 467).

## ONE WAY flags

| Line | Verdict and reading |
|---|---|
| 661 | C. Semice, střed (2 + 3 after the fix): Lysá leaves hourly at :15; Český Brod leaves :00 until 16:00, then 17:30 and 18:30 (the 660 buses arriving at :30), 13:55 and 12:25 earlier. The 15:40 / 16:02 Semice short is one pair. Card says it. |
| 822 | C. Plaňany, Blinka (2 + 4): towards Kolín 12:25, 13:54 (Klášterní Skalice), 14:56 (Kouřim), 16:30 (96 min run); from Kolín 12:36 (to Vitice), 17:24. The Kouřim-only trips (Kolín → Kouřim 15:19, 18:24, 19:09; Český Brod → Kouřim 18:30) are not 3 each way. Card lists them. |
| 826 | C. Poříčany, železniční stanice (2 + 4): sparse every 1½–2 h line; out 12:58, 13:07, 14:35, 18:07, back 13:48, 16:15. Modelled every 120 on the two exact pairs. |
| 235006 | C / shift line. PZKO-TOYOTA (2 + 3): factory shuttles 13:37 / 14:01 / 14:15 / 14:40 / 14:45. Card says so. |
| 435 | B. Říčany, podhradí (2 + 3): Klučov 13:32, 14:32 leave at :32 and 15:37 on at :37 (5 min), Říčany 13:05, Český Brod 12:55. On the card. |
| 536 | C. Žiželice, škola (2 + 3): the way back 13:55 (Loukonosy), 15:26, 17:19 goes by the loop, 16:29 and 18:29 direct; out 15:57 and 17:57 by the loop, 16:57 and 18:47 direct. The paths alternate, so the card keeps the one circuit line (out by the loop, back direct) of the fork-schedule rule and the 329 precedent (3 buses; two path lines would be 4). |
| 660 | C. Tuchoraz, U Sadů (2 + 3): hourly :00 / :02 from 16:00, before it 12:55, 14:15, 15:10, 13:47. On the card. |
| 821 | C. Ždánice, u Jánů (2 + 3): the Horní Kruty ends are 14:00 (from Ždánice), 15:02 out and 14:00 (to Kolín), 15:39, 17:44 back: 2 out against 3 back at no common minute. Already an owner check (821 Horní Kruty, +1 bus). |
| 235009 | C / shift line. Kolín, Štítary (1 + 3): arrivals 13:01 (Spálenka), 14:14, 14:50 (Veltruby); card lists the afternoon trips. |
| 460 | C. School-day single trips (Zásmuky 14:45, 15:10; Bečváry 16:02, 17:52); no longer flagged after the audit fix. On the card. |
| 675 | D. Velim, škola (1 + 3): Kolín → Cerhenice 14:03, 16:03, 18:03 (every 120 at :03), back only 17:30; the Pečky returns pass Cerhenice. 3 out, 1 back: outstation, claim right (the 14:03 bus, 8596, goes on as 679 from Velim, škola 15:13). |
| 491 | E. Louňovice, I.hráz (0 + 4): 13:29 … 16:29 are the Mukařov :32 back trips starting 3 min earlier at Louňovice; the leg is read at Mukařov. On the card; Louňovice, I.hráz is on 381, 382, 387 (other sheets). |

## Cards claiming "going home", "garage", "sleep", "outstation"
Only 675 ("outstation rule"): right. None of the others uses those words.

## Table

| Line | Verdict | Change | Buses before → after |
|---|---|---|---|
| 662 | C (way back) | note and one owner check (Kounice line, +2) | 3 → 3 |
| 235002 | E | none | 3 → 3 |
| 659 | C | out leg `stops_via` Prusice, rozcestí, `why`; no change to times or buses | 3 → 3 |
| 661, 822, 826, 435, 536, 660, 821, 460, 235009, 235006 | C (435: B) | none | unchanged |
| 675 | D | none | unchanged |
| 491 | E | none | unchanged |

**Oblast bus total: 71 → 71.**

## Audits after `run_oblast.py kolinsko`
- Branch: 536 (beyond, the Žiželice, Loukonosy trip), unchanged and explained on its card.
- Path: 536 (the loop road of the alternating path), MHD Kolín 1 (Zibohlavy), 889 Chotutice (virtual stops): unchanged from v1 and explained in the v1 method check.
- Passing (corrected script): 2 EACH WAY (662, 235002), 12 ONE WAY (822, 826, 235006, 435, 536, 660, 661, 821, 235009, 659, 675, 491), all given a verdict above. Loop lines here (707, MHD Kolín 8) are not flagged.
- Step 4: 77 timed legs, 77 ok (unchanged by the 659 change).
