> Superseded where `branch-review-2026-11-03.md` differs: 466 and 369 (the review added 466 Nelahozeves and a second 369 slot; Mělnicko is 115 buses, not 110). The review stands.

# Mělnicko: the branch re-check, 3 Nov 2026

Method: `BRANCH_BRIEF.md`. Work queue: the 10 EACH WAY and 10 ONE WAY flags of `audit-passing-2026-11-03-before.txt` for this oblast
(the brief's count of 11 EACH WAY includes 857, now fixed). For each line I read every real trip 13:00–19:00 at the flagged stop and at the
other stops where it leaves the trunk, in both directions, counting trips that start further out and pass the stop
(`data/derived/trips.json`, `reading/<line>.txt`, and a stop-by-stop listing of every stop with 2 or more unmatched trips each way).
A branch needs 3 or more trips each way at a repeating minute, and Step 4 per leg. Times below are trip starts, as in the audit.

After the coordinator's two fixes of `passing_check.py` (loop lines; stop offsets of knot legs from one direction only) the audit reads
11 EACH WAY and 9 ONE WAY: 369 moved from ONE WAY to EACH WAY and the 370 flag moved to Zdiby, u Celnice (both below). Every other flag has
the same trips as before. Knot legs of this oblast: 369 Štětí (knot Mělník, Mlazice), 370 Postřižín (Odolena Voda), 474, 476, 747; only
369 and 370 changed. No loop leg (fr = to).

**Result:** one real miss, 857 (now `857 Minice`). Every other flag is the line's own pattern read at a stop the modelled leg does not
list, a time-band change, peak extras, an outstation or an irregular set. Five card texts were wrong or incomplete and are corrected
(369, 372, 377, 400, 475). Buses 108 → 110.

## EACH WAY flags

**857 (Zákolany – Kralupy), A, fixed.** Flagged at Kralupy, železniční stanice (3 each way). Out of Kralupy, obchodní centrum :43 at odd
hours 13:43 (on to Dolany nad Vltavou, Debrno), 15:43, 17:43 (to Minice); Minice → obchodní centrum :42 at odd hours 13:42, 15:42, 17:42
(the 17:42 on to Kralupy, Synthos). Exact, 3 each way, and they alternate with the Zákolany trips of the even hours (OC :43 → Zákolany
12:43, 14:43, 16:43), so the town section Minice – obchodní centrum is hourly in reality and was every 2 hours in the model. The v1 card
listed them because their stops are on 857 (an extra bus); the afternoon-branch rule does not ask that.
Change: new Simutrans line `857 Minice`, every 120: Kralupy, obchodní centrum → Kralupy, Minice at 15:43 (24 min), Kralupy, Minice →
Kralupy, obchodní centrum at 15:42 (26 min), both legs `notvia` Zákolany so the Zákolany trips do not count for it (leg trips checked
in `schedule.json`: 13:43, 15:43, 17:43 and 13:42, 15:42, 17:42 plus the morning and late shuttles; no Zákolany trip). No `lay` change (3 min).
Step 4: window slot 15:43 against the real 15:43 and 15:42 against 15:42, exact; slots = real in the window, 100 % within 3 min.
Buses: 857 2 (unchanged) + 857 Minice 2 = 4 (was 2). Pooling the two is the owner's option (7309 ran Zákolany 14:16 → obchodní centrum 15:08
and obchodní centrum 15:43 → Minice on the live map); noted on the card and in `notes`, not applied.

**368, E, no change.** Flagged at Kojetice, Tůmovka (8 each way): Ládví → Tůmovka 12:58, 13:23, 14:15, 14:33, 15:15, 15:33, 16:15, 17:57;
Tůmovka → Ládví 13:33, 13:56, 14:48, 15:08, 15:48, 16:08, 16:48, 18:32. These are the :15 / :33 slot trips of 368 itself, which run one stop
past Předboj and turn there (13 of 13 arrivals): out of Ládví on the :15 / :33 slots, back from Předboj on :52 / :12 / :32, all on the
pattern. The stop is on 348 and 369. The card says it.

**372, D (outstation) + C, card corrected.** Flagged at Úžice [ME] (5 each way): out 13:28 (Dřínov), 14:03, 16:05, 18:05 (Zlosyň), 16:28,
17:28 (Úžice); back 12:37, 13:42, 14:12, 17:00 (Úžice), 17:55. Read at Úžice the way out is :34 hourly 14:34–18:34 (alternating Zlosyň and
Kralupy) and the way back has no repeating minute (14:15, 14:55, 15:25, 17:00, 17:33, 18:33). At Zlosyň: out :48 hourly 14:48–18:48, back
13:58, 14:33, 15:03, 17:11, 18:11 (nothing between 15:03 and 17:11). At Odolena Voda, Dolní náměstí: 12 out, 7 back. The Zlosyň trips have
no return of their own (no branch of 3 each way); the Kralupy trips are the modelled slot. Kept every 120 (2 buses). Card: "buses going home"
for the Zlosyň trips replaced by what the stops show (8039, the 14:03, goes on as 374 Máslovice 15:11, so it is not a garage run).

**466, E, no change.** Flagged at Kralupy, obchodní centrum (4 each way): out of OC 13:45, 14:45, 15:45, 16:45, 18:15, back into OC
12:50, 13:55, 16:06 (Veltrusy), 16:55. OC is the other Kralupy terminal, 10 min before the station: the :55 slot at the station is the
OC :45 trip (4 of the 5 departures 13:55–17:55 start at OC); the leg is read from the station, so OC is not on it. OC is on 646 and 857.
The Kralupy – Nelahozeves / Veltrusy shuttles (out 15:25 Veltrusy, 16:25, 17:25 Nelahozeves; back 16:06 Veltrusy, 17:11, 18:11
Nelahozeves) are 3 each way at Kralupy but go to two different ends (2 + 2 to Nelahozeves): C, listed on the card.

**369, E (extra stream of 349 buses), card text rewritten.** New EACH WAY flag at Zlonín, rozcestí, 3 each way: out of Ládví 15:45
(to Podolí), 16:45, 17:45 (to Mlazice) = Zlonín :04 (16:04, 17:04, 18:04); back from Podolí 14:12, 15:12 and from Mlazice 16:08 = Zlonín
:46 (14:46, 15:46, 16:46). Exactly hourly at the trunk stop in both directions, so it is the closest thing in this oblast to the 381 test.
Why it is still not a line: (1) it is the same road and ends as 369's own :30 trips (Podolí and Mlazice are 4 stops apart), an extra
frequency 15 min after the :30 in the peak, not a branch, short working or other path (nothing at 14:45 or 18:45); the buses are 349 buses
(349/25, /21, /26, /29) that come back as the :12 trips and go out again as the :45 ones, so it is 349 / 369 through-running; (2) tested as
a line `369 Podolí` (Ládví :45 → Podolí, Podolí :12 → Ládví, `notvia` Štětí): the legs cannot be separated from the :30 trips by `via` /
`notvia`, so the real departures in the window are doubled (4 real against 2 slots, FEWER) and the way back is EMPTY (slot 17:12, the last
real back is 16:08); every 120 is FEWER too (1 slot against 4 real out and 3 real back in the window). It would also cost +3 buses (every 60) or +2 (every 120). Not added, removed again. Change: 369 note now
states the stream, its minutes and why it is off the pattern (it listed 16:45 and 17:45 as "extra departures out of Prague" and the
shorts separately).

**668, C.** Flagged at Nebužely, u hřbitova (4 each way): out 13:05, 14:12 (Řepín), 15:15 (Mělnické Vtelno), 17:20 (Řepín); back 12:53,
14:09, 15:53 (Řepín), 16:20 (Mělnické Vtelno). No repeating minute, ends differ (Mšeno, Řepín, Mělnické Vtelno). Card says so. No change.

**370, D (shorts) + B / C (Kralupy extras), no change.** After the knot fix the flagged stop is Zdiby, u Celnice (8 each way), which every 370
trip passes. Off the pattern there: out 13:35, 13:43, 18:25 (Kralupy), 13:53, 15:35, 17:35 (Postřižín), 14:28, 14:45, 15:45, 16:45, 17:45,
18:45 (Odolena Voda); back 12:31, 13:25, 13:49, 15:25, 17:25 (Kralupy), 13:28 (Kozomín), 16:30, 18:05 (Postřižín). Read as two sets:
- Kralupy trips: the extras at other minutes before the :20 / :58 pattern (13:35, 13:43) and after 16:00, and the hourly :25 backs via
  Veltrusy (15:25, 16:25, 17:25), the :16 slot's trips 9 min later by the other road (B). Outs on the slots are all via Veltrusy.
- The Odolena Voda / Postřižín shorts (370 Postřižín): 13:00–19:00 17 out (9 Odolena Voda, 8 Postřižín) against 9 back (7 Postřižín, 2
  Odolena Voda); in the anchor window 14:10–16:10, 8 out against 4 back. Out at :45 to Odolena Voda is hourly (14:45 … 18:45, 5 trips)
  but no back trip repeats a minute (Postřižín 14:00, 14:25, 16:00, 16:30, 17:15, 17:55, 18:05; Odolena Voda 14:50, 15:10), so 3 each way
  at a repeating minute fails on the way back; most outs are followed by the same bus 5–45 min later, the six without a return are the
  imbalance. This is the outstation row of v1 (4 slots every 120 at the inbound rate, 14:28, 14:45, 15:35, 15:45 left off by the shortest
  waits): claim checked, kept. The one Step 4 FEWER (370 Postřižín out, 4 slots against 8 real) is that choice, unchanged.

**348, B / C, no change.** Flagged at Libiš, u slávisty (3 each way): out 12:45, 13:15, 13:51 (all before the every-15 pattern starts at
14:06); back 13:24, 13:54, 14:12, 14:46, 18:17, 18:54. The Libiš / U Vojtěcha swap is on the card. No change.

**400, C, card corrected.** Flagged at Varnsdorf, autobusové nádraží (3 each way): towards Varnsdorf 10:40, 12:40 (arriving 13:26 and 15:26), 14:45 (from Nový Bor), 15:10;
from Varnsdorf 15:28 (to Nový Bor), 17:58, 18:58. Letňany → Varnsdorf is :10 hourly (14:10–17:10) but from Varnsdorf the way back is :28 every 2 hours until 16:28
and hourly :58 only from 17:58, so no hourly leg passes Step 4 (the window holds one real back departure, 16:28, and an hourly row needs a second slot with a real trip within 3 min); kept every 120. At Česká Lípa 13:00–19:00:
6 towards Prague, 10 away. Wrong claim fixed: "the other departures out of Prague are buses going home". The 14:10 and 15:10 buses (1085, 1088)
come back as the 17:58 and 18:58. Buses 8 → 8.

**692, C.** Flagged at Kokořín, Šemanovice (3 each way): Kokořín ↔ Šemanovice shuttle out 13:00, 14:00, 16:00 (:00), back 13:45, 14:15, 16:15
(no single minute: :45, :15, :15), a school-day shuttle (also 8:15 and 11:00 out earlier in the day). Its stops are on 692. Card lists it. No change.

**473, C.** Flagged at Zálezlice, Kozárovice (3 each way): out 12:54, 14:01, 14:44; back 14:31, 14:44, 18:06 (+ 18:25). The :31 alternation starts
15:31; the early trips are at other minutes. Card lists all. No change.

**658, C.** Flagged at Veliká Ves (3 each way): works trips, out of Neratovice 12:59, 13:59, 14:46, 15:29, from Odolena Voda 13:40, 14:40, 16:10:
no repeating minute. Kojetice, železniční stanice (only 658) keeps the line. No change.

## ONE WAY flags

| Line | Verdict and reading |
|---|---|
| 316 | C. Flagged at Kralupy, železniční stanice (2 + 4): the hourly Kralupy trip starts 14:30; off the pattern 13:05, 13:20, 13:45, 14:38 before it and 18:36 after it. Card lists them. |
| 663 | C. Zlončice (2 + 4): out 12:56, 13:56, 14:36, 16:26, back 15:13, 18:15: no minute repeats; stops on 370. Úžice, logistické centrum is its own line. |
| 351 | B. Neratovice, III.ZŠ (2 + 3): the 13:04, 14:04, 15:34 back trips run via III.ZŠ and leave 3 min before the :07 / :37 slot. Same ends. |
| 696 | C. Mělnické Vtelno (2 + 3): sparse school-day trips; shuttles 12:43 / 13:03 and 18:32 / 19:03 listed. |
| 377 | D / E, card corrected. Veleň, Mírovice (1 + 11): the 11 unmatched outs are the off-peak :25 / :40 / :55 departures; the peak is every 12 min out, every 15 min back (8 against 6 in 15:30–17:30, 20 against 18 in 13:00–19:00). "Buses going home, they sleep at Kostelec" is not what the stops show; the card now gives the counts. |
| 349 | D. Mělník, Pšovka (1 + 5): 14:55 … 18:25 out to Mlazice, back only 17:10. Claim right; Pšovka, Loděnická and Mlazice are on 369. |
| 476 | D. Ovčáry (1 + 3): the Brandýs extension 13:03, 14:03, 15:03 back, out only 6:35. Listed on the card. |
| 464 | C. Spomyšl (0 + 6): Horní Beřkovice shorts 14:04, 14:39, 16:27 and the 466 buses 14:45, 16:45. Card lists them. |
| 475 | E. Hořín, Brozánky, Staré Brozánky (0 + 3): the way back calls at Hořín, Brozánky on 12:38, 13:40, 14:38, 15:40 and at Staré Brozánky from 16:40. Same ends and minutes. Card now says which road the game line takes. |

## Cards claiming "going home", "garage", "sleep", "outstation"
349 right; 370 right (see above); 372, 377 and 400 corrected; the oblast `notes` paragraph is general and conditional ("where more leave Prague than come back") and stays.

## Table

| Line | Verdict | Change | Buses before → after |
|---|---|---|---|
| 857 | A | new `857 Minice`, every 120, OC 15:43 → Minice, Minice 15:42 → OC, `notvia` Zákolany; note and `notes` pooling | 2 → 4 |
| 372 | D / C | card text only | 2 → 2 |
| 377 | D / E | card text only | 6 → 6 |
| 400 | C | card text only | 8 → 8 |
| 475 | E | card text and `why` (road of the way back) | 2 → 2 |
| 368, 466 | E | none | 4 → 4, 4 → 4 |
| 668, 348, 473, 658, 692, 316, 663, 696, 464 | C | none | unchanged |
| 370 | D + B/C | none | 7 → 7 |
| 351 | B | none | unchanged |
| 349, 476 | D | none | unchanged |
| 369 | E | note rewritten (the :45 / :12 stream); a `369 Podolí` line was tested and dropped (Step 4 fails) | 7 → 7 |

**Oblast bus total: 108 → 110.**

## Audits after `run_oblast.py melnicko`
- Step 4: 93 timed legs, 92 ok, 1 FEWER = 370 Postřižín out (v1, explained above and in the v1 review).
- Branch: 370 Postřižín (Kozomín trip), 476 and 747 (beyond), unchanged from v1 and explained on their cards.
- Path: 370 D8 Park trip, unchanged, explained on the card.
- Passing (both fixes): 11 EACH WAY (368, 372, 466, 668, 370, 348, 400, 692, 473, 658, 369), 9 ONE WAY (316, 663, 351, 696, 377, 349, 476, 464, 475), all given a verdict above (857 gone).
