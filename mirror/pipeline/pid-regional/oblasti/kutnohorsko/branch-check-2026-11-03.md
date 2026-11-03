> Superseded where `branch-review-2026-11-03.md` differs: 805 and 381 Zásmuky (card text). The review stands.

# Kutnohorsko: the branch re-check (3 Nov 2026)

Method: `BRANCH_BRIEF.md`. For each flag of `audit-passing-2026-11-03-before.txt` the real trips (`data/derived/trips.json`,
`reading/<line>.txt`) were read at the stop where the variant leaves the trunk (not at the audit's flagged stop, which is only
the stop with the most off-pattern trips), both directions, 13:00–19:00. Times are minutes at that stop. Live-map plates are
from the reading files (2 Nov).

## 381 — A, fixed by the coordinator: 381 Zásmuky every 60, +3 buses (checked)
Read at Zásmuky, náměstí 13:00–19:00:
- towards Zásmuky: :09 hourly (13:09–18:09, on to Čáslav) and :39 (15:39, 16:39, 17:39, 18:39 = Háje 14:30, 15:30, 16:30, 17:30, ending there);
- towards Prague: :51 hourly from Čáslav (13:51–18:51) and :21 (14:21 = Kutná Hora 13:40, 15:21 = Kutná Hora 14:40, 16:21 = Zásmuky start).
The branch is 4 out and 3 back at a repeating minute. Both legs are exact: Háje :30 (14:30, 15:30, 16:30, 17:30; 4 of 4), Zásmuky :21
(14:21, 15:21, 16:21; 3 of 3). `notvia` separates the legs: the Háje leg (notvia Bečváry) counts none of the Čáslav trips, the Zásmuky leg
(notvia Čáslav, Kalabousek) counts the two Kutná Hora trips and the Zásmuky start and none of the Čáslav ones; 381's own legs
(Háje 13:00–17:00, Čáslav 13:48–17:48) count none of the branch trips. The card's live-map sentences hold (1683 and 9373 came in from
Čáslav and left Háje 16:30 / 17:30 to Zásmuky; 9372 ran Háje 14:30 → Zásmuky and back at 16:21), and so does "the garage" (the Zásmuky starts are 4:21 and 4:51 only, and the 17:30 bus ends there).
One change: `window` 15:00–17:00 on 381 Zásmuky. With the default window (15:30–17:30) the Zásmuky leg had the slot 17:21 with no real trip
(the branch's last return is 16:21), so `audit-step4` printed EMPTY. In 15:00–17:00 both legs are exact (slots 15:30, 16:30 / 15:21, 16:21 = the real trips).
Typed values, running times and buses (3) are unchanged.

## EACH WAY flags
**805 — C (irregular), no change.** Read at Kutná Hora, Hlouška, Na Špici (all Kolín trips pass it):
- towards Kutná Hora / Zruč: 13:19 (Zruč), 14:19 (bus station), 15:19 (Zruč), 15:49 (bus station), 16:29 (Karlov), 16:49 (bus station), 17:19 (Zruč), 18:19 (bus station), 19:19 (bus station);
- towards Kolín: 13:11, 13:41 (bus station), 14:31, 15:01 (Karlov), 15:31 (bus station), 15:51 (Zruč), 16:51 (Zruč), 17:31 (Karlov), 18:31 (Zruč).
The Zruč trips (Kolín 12:57, 14:57, 16:57; Zruč 14:36, 15:40, 17:20) are the modelled line; the rest is shorts to two different ends. Kolín → bus station:
13:57, 15:27, 16:27, 17:53, 18:57 (5 out), bus station → Kolín 13:06, 13:36, 15:26 (3 back); Kolín → Karlov 16:03, Karlov → Kolín 14:19, 14:49, 17:19. Minutes at the
bus station: out :57 / :27 / :27 / :53 / :57, back :06 / :36 / :26: there is no repeating minute, so no Step 4 pattern holds the day (the best, every 120 at Kolín 15:27 /
bus station 15:26, is exact in 14:30–16:30 and 26 to 30 min off at 13:57 and 17:53), and the Karlov shorts go to another end. The existing owner check keeps this as the
approximation with its slower option (+1 bus). Card and check name all the trips; every stop is on 805 or 785. Plates (2 Nov): 7602 alone runs 13:57, 15:26, 16:03, 17:19, 18:57, so
this is a real working; it is the case closest to 381 and the one to look at again if the owner wants it modelled.
**781 — C, no change.** Read at Žleby, náměstí (781's own junction): towards Žleby 13:07, 15:07, 17:07 (the modelled Potěhy trips), 16:12 (Čáslav 15:50, ends there), 18:42 (Čáslav 18:18, ends at Kamenné Mosty);
towards Čáslav 14:01, 16:01 (the Okřesaneč trips), 17:08 (Žleby short), 19:08 (Kamenné Mosty). Four different ends, no repeating minute with 3 each way. The Okřesaneč trips (13:45, 15:45) are the
740 buses coming back (7660: 740 13:13, 781 13:45; 7629: 740 15:13, 781 15:45): 2 rounds in the window, not 3. The card names every one of them.
**742 — C, no change.** Čáslav :13 is hourly 15:13–18:13 but to four ends: Ledeč 15:13, Zbýšov 16:13, Třebětín 17:13, Žáky 18:13; back Ledeč 12:17 / 17:47 (to Zbýšov), Podolí 14:45, Zbýšov 16:38, Žáky 18:28, Dobrovítov 14:18.
Read at Žáky, Dolní Štrampouch: away 13:55, 15:25, 16:25, 17:25, 18:25, towards Čáslav 13:13, 14:38, 15:43, 16:48, 18:28 (drifting minutes). Each end has one or two trips. The card names all of them.

## ONE WAY flags
- **533 — C.** 2 each way: Žiželice 13:04, 15:04 → Chlumec; Chlumec 13:40, 15:40 → Žiželice (one 536 bus, 7592, between its own trips). No third trip (the 17:16 from Kutná Hora is the line's own trip 20 min late). Card names them.
- **783 — B.** Hourly at Žehušice (:05–:10 each way); the trunk (Kutná Hora 16:06, 18:06; Čáslav 16:43) and the Žehušice shorts (Čáslav 13:48, Žehušice 14:10) are 5 to 10 min off their slots, stated on the card.
- **782 — B.** Hourly Kutná Hora :41–:46 / Vrdy :43–:48; the flagged trips (12:46, 13:46, 14:46, 13:48, 14:39 from Žižkov) are 4 to 5 min off the :41 / :43 slots, stated on the card.
- **402 — D.** Read at Zruč nad Sázavou, Sázavan: towards Prague 14:19, 15:19, 16:19, 18:19 (all from Čáslav), towards Zruč / Čáslav 13:41, 15:41, 16:41 (Roztyly 15:20 ends), 17:56 (16:35), 18:56 (17:35 ends).
  The Roztyly → Zruč trips 15:20, 17:35, 18:20 have no Zruč → Roztyly trip in the afternoon (Zruč starts 4:24, 6:29 only); 7671 and 7672 end there after 17:35 / 18:20. The card's "buses going home to Zruč" holds.

Other "going home" claims checked: 387 (Uhlířské Janovice starts 4:27–6:57, afternoon 4 towards Prague against 6 out: true), 771 (Soběšín starts 4:52, 6:06, 6:54; 7549 and 7637 end there: true), 381 (above).

## Result
| line | verdict | change | buses before → after |
|---|---|---|---|
| 381 | A (coordinator) | 381 Zásmuky every 60 (checked); window 15:00–17:00 added, values unchanged | 5+3 → 5+3 |
| 805 | C | none (owner check kept) | 2 → 2 |
| 781 | C | none | 1 → 1 |
| 742 | C | none | 2 → 2 |
| 533 | C | none | 2 → 2 |
| 783 | B | none | 4 → 4 |
| 782 | B | none | 2 → 2 |
| 402 | D | none | 3 → 3 |

Oblast total: 70 → 70 (70 is the state inherited, with the coordinator's 381 Zásmuky +3, so v1 as published was 67; this re-check adds 0). Audits after `run_oblast.py kutnohorsko`: Step 4 86 of 86 legs ok (EMPTY on 381 Zásmuky gone), branch and path unchanged
(481 and 746 path flags as before), passing: 3 EACH WAY and 4 ONE WAY remain, each with the verdict above (the flag list is the same trips, now explained).
