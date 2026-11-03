# Benešovsko: review of the branch re-check (3 Nov 2026, Fable)

Independent of the designer's notes. Method: `BRANCH_BRIEF.md` "For the reviewers". The diff against v1
(`mirror/pipeline/pid-regional/oblasti/benesovsko/lines.json`) touches 337, 339, 382, 651, 753, 865 and the sheet notes.
Every EACH WAY and ONE WAY flag of `audit-passing-2026-11-03-before.txt` was re-derived from `data/derived/trips.json` with my own
reader (same coverage rule as `audit/passing_check.py`, each stop read at the trip's first passing, which is the loop-line fix the
coordinator made meanwhile), plus a scan of every stop of every line for uncovered trips that repeat at one minute (±3) three
times each way. Plates: `scripts/observed.py` for 382, 865 and 339 on 2 Nov. Both reruns of `run_oblast.py benesovsko` (before
and after my edits) are clean.

## Changed lines
**865 — PASS (A).** Read at Pacov, železniční stanice 13:00–19:00: shuttle out 13:50, 15:50, 17:50 (+ 15:05), back arriving
14:05, 16:05, 18:06 (+ 14:53); at Jetřichovská křižovatka :57 / :58. Every 120 all day (5:50–19:50). `865 Pacov`: `notvia`
Bratřice keeps the Čechtice trips out of both legs (the leg counts the shuttle plus the 10:18 / 20:18 / 11:30 town shorts, off);
865's own legs count only the Čechtice trips (5/5/5). Window slot 15:50 against real 15:05, 15:50 and 15:58 against 14:46, 15:58
(±1, slot trips exact); exact 8 of 12 and 8 of 10 over the day; running times 7 / 7; the builder set lay 1 at Jetřichovská, the
real :57 → :58 turn; 1 bus. Plates: 18101 runs Čechtice 12:50 → Pacov, the 13:50 / 13:58 shuttle, 14:18 → Čechtice, and again
16:50 → 17:50 / 17:58 → 18:18; 18104 the 15:50, 18106 the 15:58 and 16:18. Pooling (2 buses) is real and is offered on the card,
not applied, as the brief rules. Card text correct.

**382 — PASS (D; the designer's :20).** Plates 2 Nov: 9953 Háje 14:20 → Sázava 16:30 → Háje 18:20; 9947 Sázava 13:30 → Háje
15:20 → Sázava 17:30 → Háje 19:15; 9377 Háje 12:30 → Sázava 14:30 → Háje 16:20 → Sázava 18:15. The :50 buses 9180 (14:50), 9375
(15:50), 9178 (16:50) and the 17:20 bus 9371 (in from 381) are not seen again before 20:00. The :48 arrivals leave at :20 (14:48 →
15:20, 15:48 → 16:20, 17:48 → 18:20, 18:48 → 19:15; 13:48 → 16:00 as 381): nobody makes the :48 → :50 turn the v1 card claimed.
Exact hits over the day: :20 five (14:20–18:20), :50 three. Waits 32 at Háje, 52 at Sázava: 4 buses. The 3-bus alternative existed
only through `lay 2`; with the method's default 3-minute layover :50 needs 78 + 22 + 78 + 62 = 240 min, 4 buses as well. So there
is no cheaper real option and no owner check: the evidence settles it (the 2 Nov rule). The card names 12:30, 13:15, 18:15 and the
:50s. Step 4 FEWER on the Háje leg (4 real in the window, 2 slots) is the outstation rule. Seen on the side: 381 and 382 share
courses at Háje (9377, 9367, 9375, 9371 carry 381 course numbers; 9948 came in on 382 at 13:48 and left on 381 at 16:00).

**339 — FIX (card text; D + E confirmed).** Read at Kamenice, kulturní dům 13:00–19:00: towards Prague uncovered 13:16 (Týnec
12:55), 14:41, 15:41, 16:41 (Kamenice starts); towards Týnec uncovered 13:43 (Prague 13:05, ends at Kamenice), 15:13 (14:35, ends),
16:28 (15:50), 17:28 (16:50), 18:43 (18:05). Three at :41 one way; the other way nothing repeats three times (:28 twice; 13:43 and
18:43 unrelated), so no branch. Plates: 9932 (15:50) is not seen after Týnec, 9949 (16:50) is the 18:40 back; 9365 runs 14:35 out and
15:41 back; 9361 the 14:41 then 332; 9163 the 16:41 after 441 trips. The designer's corrected claim holds. Changed: the note now
names Týnec 12:55 and Budějovická 18:05 (15 min off the :40 and :20), which it did not.

**337 — PASS (B + E).** At Nespeky: uncovered towards Prague 13:59 (Benešov 13:40), 14:44 (short), 18:54 (18:35); towards Benešov
13:38 (Budějovická 12:45), 14:43 (13:50), 15:40 (14:47) and the shorts 15:02, 15:48. The three Prague departures cluster at Nespeky
about :40, the trunk's own early phase 10–15 min off :35 / :37, now named. Shorts 2 out, 1 back, running on as 651.

**651 — PASS (C + E).** One trip each at Pyšely, náměstí (12:59, 13:52, 14:10, 14:44, 17:00, 17:27, 18:15, 18:50); no minute
repeats; named on the card.

**753 — PASS (C).** Singles; 13:05 and 18:05 are the only pair at one minute. 12:43 added by the designer.

## Other EACH WAY flags
**383 — PASS (B).** Whole day at Háje: :45 outside 14:40–16:40, :40 inside; window 14:30–16:30 holds 14:40, 15:40 exact and :45
would miss both by 5 (Step 4 fails). The uncovered trips are the :45 / :06 phase (Háje 12:45, 13:45, 17:45, 18:45; Chocerady 13:06,
17:06, 18:06), named; Ondřejov – Mukařov shorts 2 out, 1 back. My scan hits it at Mukařov, odbočka Tehovec (three at :41, three at
:22): the same trips, not a branch.

**841 — FIX (card text; E).** The EACH WAY flag was the audit's loop-line artefact (the trip passes Terminál twice and the stop
dict kept the arrival), fixed by the coordinator; after the fix 841 is ONE WAY at ZŠ Vorlina because the real Hrazená Lhota :23
trips run the Sukova loop again on the way back into Terminál and the model's inbound leg (21 min) ends at the first Terminál.
Added to the note: the game line runs the loop once per round, on the way out, its stops served hourly. Model hourly :51 / :23,
exact in the window, lay 0 at Hrazená Lhota (the real turn on arrival), 1 bus.

**847, 568 — PASS (E).** The same artefact (one-way circles, `fr` = `to`); clean after the fix. Cards name 847's 18:04 and 568's hours.

**332 — PASS (B).** The branch is `332 Neveklov` (Jílové :30 → Neveklov; Neveklov 15:51 / 16:46 → Jílové, exact in the window);
the flagged trips are its early phase (from Prague 12:57 / 13:57 passing Jílové :41 / :42; Neveklov 13:09, 14:06, 15:01 drifting
5 min an hour). The 332 trunk every 15 is exact.

**795 — PASS (C).** Hourly from 16:00 (Vlašim :00, Zruč :35) and modelled there; before it the :10 phase (13:10, 14:10 to Trhový
Štěpánov; Zruč 12:40, 15:10) and 14:42 from zbrojovka: no three at one minute in the window.

## ONE WAY flags
- **755 — PASS (D).** At Neveklov towards Neveklov 7 (13:50, 15:05 Měřín, 15:20, 15:50 Jablonná, 16:20, 17:00 Měřín, 18:05),
  towards Benešov 4 (Měřín 13:45, Neveklov 15:15, Měřín 16:02, Neveklov 18:30): outstation; 755 + 755 Měřín give 1 an hour each
  way, the inbound rate. FEWER on the Benešov leg is the rule.
- **408 — PASS (C).** Tábor singles to four ends (14:25 Jistebnice, 16:20 Sedlec-Prčice, 17:05 Benešov, 18:20 Prague).
- **752 — PASS (B + C).** Trunk hourly :00 / :10 with 13:05, 18:05 / 12:50, 17:05, 18:04 off; Týnec shorts 13:35, 14:25, 15:30,
  17:35 / 14:13, 15:25, 16:05, 18:05, `752 Týnec` every 120 with two slots each way holds four of them exact, 13:35 / 14:13 off.
- **488, 532, 794, X390 (200390), 842 — PASS (C).** Singles at no repeating minute (488: 13:10, 13:50, 17:50 / 15:53; 532 Votice
  13:00, 13:20, 13:25, 17:10; 794 Kácov 14:44, 17:42; X390 Slapy 13:15, 15:25, 18:15 / Rabyně 17:40; 842 Čechtice 14:20, 16:20,
  18:40 against 14:22, 16:22 back), named on the cards.
- **796 — PASS (B).** Pyšely 13:11, 14:11, 15:21 and Benešov 12:40, 13:40 are the :40 / :11 phase before 14:35; named.
- **382 — see above.**

## Scan for missed branches
Uncovered trips repeating three times each way at one stop: only 383 and 796 (the trunk's other phase, above) and 841 (the
artefact). No regular branch is missed on this sheet.

## Result
| line | verdict | review | change by the reviewer |
|---|---|---|---|
| 865 | A | PASS | none |
| 382 | D | PASS (:20, 4 buses; no owner check, the 3-bus turn is refuted by the plates) | none |
| 339 | D + E | FIX | note names Týnec 12:55 and Budějovická 18:05 |
| 841 | E | FIX | note says the Sukova loop runs once per round in the game |
| 337, 651, 753 | B + E, C + E, C | PASS | none |
| 383, 332, 795 | B, B, C | PASS | none |
| 755, 408, 752, 488, 532, 794, 796, X390, 842, 847, 568 | D, C, B + C, C, C, C, B, C, C, E, E | PASS | none |

Buses: 140 → 140 (the designer's 865 Pacov +1 and 382 +1 verified). Audits after the rerun: Step 4 154 timed legs, 151 ok,
3 FEWER (339, 382, 755: the outstation rule, on their cards); branch unchanged; path 1 (759, explained in the v1 method check);
passing 7 EACH WAY and 11 ONE WAY, each with the verdict above.
