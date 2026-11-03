> Superseded where `branch-review-2026-11-03.md` differs: 339, 841 (card text). The review stands.

# Benesovsko: the branch re-check (3 Nov 2026)

Method: `BRANCH_BRIEF.md`. For each flag of `audit-passing-2026-11-03-before.txt` the real trips (`data/derived/trips.json`,
`reading/<line>.txt`) were read at the stop where the variant leaves the trunk (not at the audit's flagged stop, which is only the
stop with the most off-pattern trips), both directions, 13:00–19:00. Times are minutes at that stop. Plates are from the
reading files (PID live map, 2 Nov; a plate list is a check, not proof, e.g. 7832 appears on trips too far apart to drive).

## Result in short
One missed branch (865 Pacov), one outstation line re-timed on the plates (382), one wrong card claim (339), four cards that
did not name every off-pattern trip (337, 651, 753, 865). Everything else is B, C, D or E and stays.

## EACH WAY flags
**865 — A: new Simutrans line `865 Pacov`.** Read at Pacov, železniční stanice: the town shuttle železniční stanice → autobusové nádraží → Pacov, Jetřichovská ul.křižovatka
runs out 13:50, 15:50, 17:50 (+ 15:05) and back 13:58, 15:58, 17:58 (+ 14:46), every 2 h at :50 / :58 all day (5:50, 7:50 … 19:50): 3 exact each way in the window, a 7-minute run
and a 1-minute turn at Jetřichovská. The card had called it "listed" (the stops are on 865). The Čechtice trips (Pacov :18, Čechtice :50, even hours) are the other hours, so the two are
one hourly service that alternates, as 381 does.
Change: `865 Pacov`, every 120: Pacov, železniční stanice → Pacov, Jetřichovská ul.křižovatka at 13:50 (typed 49), Jetřichovská → železniční stanice at 13:58 (typed 57), both `notvia` Bratřice
(keeps the Čechtice trips out of both legs; the 865 legs end at Čechtice and count no shuttle trip). Running time 7 and 7 min (the shuttle's own path: Poláček out, Za branou sídliště back).
Step 4 (window 14:30–16:30): out slots 15:50 against real 15:05, 15:50; back slots 15:58 against real 14:46, 15:58 (within ±1, all slots have a real trip); exact over the day 8 of 12 and 8 of 10 (off: the school extras
10:18, 15:05, 20:18, 22:13 and 11:30, 14:46). Both legs ok in `audit-step4`. 1 bus. Offered, not applied: the 865 buses run it in their Pacov layover on the live map (18101: Čechtice 12:50, shuttle 13:50 / 13:58, Pacov
14:18 → Čechtice, and again 16:50, shuttle 17:50 / 17:58, 18:18 → Lukavec; 18104 and 18106 do 15:50 / 15:58 between Čechtice 14:50 and Pacov 16:18), so pooled 865 + 865 Pacov need 2 buses, not 3. Card, `why` and the sheet notes say so. Flag cleared.
**339 — D + E; the card claim was wrong.** The audit's stop (Vestec, Šátalka) is passed by every trip; read at Kamenice, kulturní dům: towards Prague 13:16, 15:01, 16:01, 17:01, 18:01, 19:01 (Týnec :40 hourly) and
14:41, 15:41, 16:41 (Kamenice start); towards Týnec 13:58, 14:58, 15:58, 16:58, 17:58 (Prague :20), 16:28, 17:28 (Prague 15:50, 16:50) and 13:43, 15:13 (Prague 13:05, 14:35, ending at Kamenice).
The Kamenice shorts are 3 back (:41) against 2 out (13:05, 14:35): fewer than 3 each way, no branch. The card said the :41 shorts are the probable returns of the 15:50 / 16:50. The plates say no: 9932 (15:50) stays at Týnec,
9949 (16:50) is the 18:40 back; of the shorts only 14:35 → 15:41 is a pair (9365), the 14:41 (9361) and 16:41 (9163, after the 441) are run by buses that do not come from 339. The :20 / :40 buses are the circuit (9939, 9942: 14:20 out, 15:40 back, …) as modelled.
The Sulice, Želivec shorts (13:55, 16:16) follow 335 arrivals (7 of 7; 9133, 9172): carried by 335's buses (E). Change: card text only (note corrected). 3 → 3.
**383 — B.** Hourly Háje :40 (14:40–16:40) / :45 outside, Chocerady :11 / :06: the flagged trips are the same hourly line 5 to 10 min off the slots (Háje 12:45, 13:45, 17:45; Chocerady 13:06, 17:06, 18:06), named on the card.
The Ondřejov – Mukařov shorts are 12:53, 13:36 out and 13:38 back, 2 each way in the window. No change. 3 → 3.
**841 — E (scan artefact).** A loop line (Terminál → Sukova loop → Terminál → … → Hrazená Lhota): the flagged trips are the line's own hourly slots, Terminál :51 (12:51, 13:51, 14:51, 16:51) and Hrazená Lhota :23 (13:23, 14:23, 15:23, 17:23),
all exact; the audit's orientation test misreads the loop. The only real extras are the Domašín shorts 14:18 / 14:59, named. No change. 1 → 1.
**337 — B + E.** Read at Poříčí nad Sázavou, rozcestí Nové Městečko: towards Prague 13:56, 15:06, 16:06, 17:06, 18:06, 18:51 (Benešov 13:40, 14:50, 15:50, 16:50, 17:50, 18:35); towards Benešov 13:41, 14:46, 15:43, 16:31, 17:33, 18:31 (Praha 12:45, 13:50, 14:47, 15:35, 16:37, 17:35).
Hourly, on the slots except Benešov 13:40, 18:35 and Budějovická 12:45, 13:50, 14:47 (10 to 15 min off). The Benešov – Nespeky shorts (Benešov 14:25, 15:29; Nespeky 15:02; 12:40 / 12:39 before) are 2 out and 1 back in the window and run on as 651
(4 of 4 arrivals, 6 of 6 departures at Nespeky). Change: the four off minutes added to the card. 3 → 3.
**651 — C + E.** Read at Pyšely, náměstí: Pyšely → Senohraby / Hrusice 14:33, 15:33, 16:34 (+ 13:07, 17:35, 18:58 through from Nespeky) is hourly and held by the 651 circuit (14:33 Hrusice, 15:33 Senohraby, exact);
Nespeky ↔ Pyšely runs after 337's arrivals (Nespeky 14:10, 14:44, 15:48; Pyšely 13:52, 14:55). The rest is one trip each, no repeating minute: Nespeky → Senohraby 12:59, 17:27, 18:50; Senohraby → Nespeky 18:15; Hrusice → Nespeky 17:00.
Change: these trips added to the card. 2 → 2.
**753 — C.** A school line of single trips: Benešov → Týnec 13:35, → Netvořice 16:35, 18:35; Týnec → Neveklov 13:30, → Benešov 14:30, 15:35; Neveklov → Týnec 14:37; Netvořice → Týnec 17:44; Netvořice → Benešov 12:43. No minute repeats 3 times in one direction.
Change: 12:43 added to the card's list. 1 → 1.
**332 — B (already its own line).** Read at Jílové u Prahy, náměstí: towards Neveklov 13:42, 14:41 (through from Prague 12:57, 13:57), 15:30, 16:30, 17:30, 18:30; towards Prague 14:02, 15:02, 15:59 (ends at Jílové), 16:47, 17:47.
`332 Neveklov` already holds the hourly branch at the anchor (Jílové :30, Neveklov :51 / :46); the flagged trips are the early-afternoon phase (:41 out, :06 back), named on the card. No change. 10 → 10.
**795 — C.** Hourly from 16:00 (Vlašim :00, Zruč :35), modelled at 17:00. Before that no repeating minute: Vlašim 13:10, 14:45 (zbrojovka), Zruč 12:40, 15:10, and the Trhový Štěpánov shorts 14:10 / 14:39; named on the card. No change. 3 → 3.

## ONE WAY flags
- **382 — D; claim and pattern corrected, +1 bus.** Prague → Sázava 13:15, 14:20, 14:50, 15:20, 15:50, 16:20, 16:50, 17:20, 18:20 (9) against Sázava → Prague 13:30 … 17:30 and 18:15 (6): a true outstation (Sázava starts 4:25 to 7:23). The card said the :20 departures are the buses going home
  and kept the :50 because "the :48 arrivals turn into it in 2 minutes". The plates say the opposite: 9953, 9947 and 9377 run Háje 14:20 / 15:20 / 16:20 → Sázava → back 16:30 / 17:30 / 18:15 → Háje (turn 32 min, then out at :20 again); the :50 buses (9180, 9375, 9178) and the 17:20 (9371) do not come back
  before 20:00. No bus makes the 2-minute turn. Method: pick the departures that fall off by the plates (and the waits). Change: Háje leg `at` :50 → :20 (typed 49 → 19), `lay` 2 removed, note and `why` rewritten (waits 32 at Háje, 52 at Sázava), :50 listed as going home. Exact hits 3 → 5 of the day's departures. 3 → 4 buses.
  Step 4 FEWER on the Háje leg stays (4 real in the window, 2 slots: the outstation rule, said on the card). If the coordinator prefers the cheaper pattern the old values are :50 / lay 2 / 3 buses.
- **755 — D, kept.** Outstation: read at Neveklov, towards Neveklov 8 (Benešov 13:50, 15:05 and 17:00 through to Měřín, 15:20, 15:50, 16:20, 18:05, 18:50), towards Benešov 5 (Neveklov 12:45, 15:15, 18:30; Měřín 13:45, 16:02). Card text holds. 2 → 2.
- **408 — C.** Tábor shorts at no repeating minute (Chyšky 13:29; Tábor → Jistebnice 14:25, → Sedlec-Prčice 16:20, → Benešov 17:05); the way back from Tábor (13:05, 13:45, 15:00, 18:20) is timed at the Votice knot as the card says. 7 → 7.
- **752 — B + C.** Jílové hourly :00 / :10 with 13:05, 18:05 / 12:50, 17:05, 18:04 off; the Týnec shorts (Benešov 13:35, 14:25, 15:30, 17:35; Týnec 14:13, 15:25, 16:05, 18:05) have no repeating minute, 2 of each pair modelled as `752 Týnec`. 5 → 5.
- **488 — C.** Netvořice shorts 13:50 out, 13:43 and 15:53 back; 13:10 and 17:50 from Benešov off the hourly-ish pattern. 3 → 3.
- **532 — C.** Votice town shuttles (13:20, 13:25) and 13:00 → Jankov, 17:10 → Vlčkovice; 2 each way. 1 → 1.
- **794 — C.** Kácov 12:44, 14:44, 17:42 against the modelled 15:52; Vlašim 15:45 → Zdislavice, 18:15 → Trhový Štěpánov. 1 → 1.
- **796 — B.** Hourly :35 / :56 from 14:35, :40 / :11 before; the flagged trips are the earlier phase, named. 3 → 3.
- **X390 (200390) — C.** One bus: Rabyně 12:10, 14:10, 16:10, 17:40; Slapy 13:15, 15:25, 16:55, 18:15. 1 → 1.
- **842 — C.** Vlašim → Čechtice shorts 14:20, 15:30, 16:20, 18:40 against Čechtice 14:22, 16:22: 2 back, below 3. 3 → 3.
- **847, 568 — E (scan artefact).** One-way circles (Dolní Kralovice :44 even hours, Miličín :45 hourly): the flagged trips are the circle's own slots (the audit's slot offsets fail on a circle); the one real extra is 847 at 18:04, named on its card. 1 → 1 each.

Other "going home" / "sleep" claims checked: 339, 382 (above), 755 (kept).

## Result
| line | verdict | change | buses before → after |
|---|---|---|---|
| 339 | D + E | card corrected (no model change) | 3 → 3 |
| 383 | B | none | 3 → 3 |
| 841 | E (scan artefact) | none | 1 → 1 |
| 865 | A | new line `865 Pacov` every 120 (:50 / :58, notvia Bratřice); pooling with 865 offered, not applied | 2 → 3 |
| 337 | B + E | off-pattern trips added to the card | 3 → 3 |
| 651 | C + E | off-pattern trips added to the card | 2 → 2 |
| 753 | C | 12:43 added to the card | 1 → 1 |
| 332 | B | none (the branch is already `332 Neveklov`) | 10 → 10 |
| 795 | C | none | 3 → 3 |
| 755 | D | none | 2 → 2 |
| 408 | C | none | 7 → 7 |
| 752 | B + C | none | 5 → 5 |
| 488 | C | none | 3 → 3 |
| 532 | C | none | 1 → 1 |
| 794 | C | none | 1 → 1 |
| 796 | B | none | 3 → 3 |
| 382 | D | Háje :50 → :20 (typed 49 → 19), `lay` 2 removed, card corrected on the plates; old values :50 / lay 2 / 3 buses | 3 → 4 |
| X390 (200390) | C | none | 1 → 1 |
| 842 | C | none | 3 → 3 |
| 847 | E (scan artefact) | none | 1 → 1 |
| 568 | E (scan artefact) | none | 1 → 1 |

Oblast total: 138 → 140. Audits after `run_oblast.py benesovsko`: Step 4 154 timed legs, 151 ok, 3 FEWER (339, 382, 755: the outstation rule, said on their cards; same three as before), branch unchanged, path unchanged (759, explained in the v1 method check),
passing 8 EACH WAY (865 cleared) and 12 ONE WAY, each with the verdict above.
