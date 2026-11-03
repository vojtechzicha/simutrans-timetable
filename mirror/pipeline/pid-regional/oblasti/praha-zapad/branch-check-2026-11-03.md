> Superseded where `branch-review-2026-11-03.md` differs: 340 / 359 (the review split 340 into 340 and 340 Masarykova). The review stands.

# Praha-západ: branch re-check, 3 Nov 2026

Why: the owner found that short workings and branches had been filed as "off the pattern" because trips were grouped by start and
end stop (381 Zásmuky). Queue: the 8 EACH WAY and 12 ONE WAY flags of `audit-passing-2026-11-03-before.txt` (rerun after the coordinator's loop fix of `passing_check.py`: no change in this oblast). Every flag was read
again from `data/derived/trips.json` and `reading/<line>.txt` at the flagged stop and at the stops where a variant leaves the
trunk. Minutes below are the times of the off-pattern trips at the flagged stop (→ and ← as the audit prints them).

**Result:** 1 missed branch modelled (390 Štěchovice); every other flag is a pattern the card already names, an approximate row,
a trip carried by another number or an artefact of the audit. Simutrans lines 45 → 46, buses 88 → 90. `run_oblast.py` is clean:
Step 4 has the same 2 FEWER legs as before (340 out of Dejvická, 356 Velká Brána out of Bořislavka, both outstation rows timed at
the inbound rate, verified below), branch audit all `[ok]`, path audit the one explained 445 path, no uncovered stop.

## EACH WAY

**390** (@ Praha, Zbraslavské náměstí): → 13:48 14:08 14:48 15:48 16:48 17:48 18:53; ← 13:16 14:16 14:31 14:56 15:56 17:41 17:56.
**A.** Read at Štěchovice, where the Třebenice variant leaves the trunk, the line has two services out of Praha: Třebenice :25 (12:25,
15:25, 16:25, 17:25) and a second one at :35 all afternoon (13:35 and 14:35 go on to Třebenice, 15:35, 16:35, 17:35 end at
Štěchovice, with 13:55). The Štěchovice short trips are 4 out (13:55 15:35 16:35 17:35) and 4 back (13:55 14:35 15:35 17:35), hourly
at :35 from 15:35. The old card filed them as "listed: their stops are on 390 and their buses run 440". **Change:** new Simutrans line
**390 Štěchovice**: Smíchovské nádraží → Štěchovice (rt 35) and Štěchovice → Smíchovské nádraží (rt 34), `notvia` Štěchovice,
Třebenice on both legs (so the Třebenice trips are not counted), window 15:00–17:00 (as 390). **Every 60 fails Step 4:** out slots
15:35 16:35 are real, but of the back slots 15:35 16:35 only 15:35 has a real departure (Štěchovice has no 16:35), so 1 of 2
back slots is empty (audit: EMPTY, FIXABLE every 120); no other 2-hour window passes for both legs. **Every 120**
at 15:35 (odd hours) passes: slots 15:35 = real 15:35 (and 16:35 out as the second real), back 15:35 = real 15:35; whole day out
3 of 8 exact, back 2 of 9; 17:35 is exact both ways. 2 buses (every 60 would also need 2). No owner check: a passing pattern exists, so Step 4
rule 3 decides; the hourly pattern is named in the line's `why`. Card: pooling with 440 is an option (the buses wait about 85 min at each end).
Off the pattern on the card: 13:55 both ways, Smíchovské nádraží 16:35, Štěchovice 14:35. The 390 Třebenice line is unchanged
(3 buses).

**359** (@ Roztoky, rozcestí Žalov): → 13:41 14:46 15:19 15:50 16:20 16:50 17:20 17:50 18:20 18:49; ← 13:39 14:39 15:41 16:41 17:43.
**E in time and buses, but a regular town path that is NOT modelled (open item, first below).** The Roztoky town round is regular both ways: nádraží → Levý Hradec at :13 / :43 (15:12 15:43 16:13 16:43 17:13
17:43 18:13 18:42, every 30) and Levý Hradec → nádraží hourly at :39 (14:37 15:39 16:39 17:41). It is the continuation of the 340
:29 / :59 trips: 18 of 18 340 arrivals at nádraží are followed by a 359 departure within 0–5 min and 12 of 12 340 departures from
nádraží follow a 359 arrival, so 340's slots :29 / :59 and its :42 back slot stand for it (same buses, no second bus). Its stops
are on 359 (Suchdol – Maxmiliánka, hourly) and 340. Limit: the game bus of the 340 slot runs the direct road, so 17. listopadu,
Masarykova, Solníky and Obránců míru get the hourly 359 only, not the two extra an hour of the real round. Not changed (a separate
round line, tested only in thought, would double the buses; the fix would be a 340 + 359 circuit with the :29 / :59 slots moved out of
340, cost untested).

**444** (@ Kamenice, u Dvora): → 13:12 14:12 14:54 16:51 17:21; ← 15:01 16:01 17:01 18:20 18:46. **C.** Jílové → Kamenice 12:55 13:55
14:37 16:34 17:04 (5 trips, no repeating minute), Kamenice → Jílové 13:29 18:44 (2), and the Kamenice → Těptín 5-minute shorts
15:59 16:59 18:18 (one way only; there is no Těptín → Kamenice trip in the afternoon). All stops are
on 444. Card lists them. No change.

**356** (@ Statenice, Černý Vůl, hospoda): → 13:23 13:43 18:13 18:37; ← 13:33 14:13 18:13 18:41. **C.** The four-destination rotation
is regular 14:00–18:00; at the edges it drifts: Bořislavka 13:10 (Statenice, 5 min off :05), 13:30 (Lichoceves, 5 off :35), 18:00
(Lichoceves, 25 off), 18:12 and 18:38 (Statenice), 18:24 (Obchodní centrum Ruzyně, 9 off); Statenice 13:30 (5 off :25) and 18:38
(13 off); Lichoceves 14:04 and 18:04 (5 off :59) and 17:19 (20 off). Single trips at different minutes. Card now lists them. No
change. Velká Brána: at Horoměřice, v lipkách 6 trips an hour leave Bořislavka and 5 return (15:00–16:00: out 15:05 15:15 15:25
15:35 15:45 15:55, back 15:11 15:23 15:31 15:41 15:53), so the "inbound rate, :55 off the pattern" claim stands (one more out
than back: the :55 trip is the one without a return).

**688** (@ Nový Knín, Starý Knín): → 13:09 13:37 14:45 17:45; ← 13:00 13:50 15:50 18:20. **C.** The Dobříš trips: Mníšek → Dobříš
12:35 13:05 (Nový Knín 14:42) 17:15 19:05, Dobříš → Mníšek 12:45 13:35 15:35 18:05; no repeating minute. Their
Dobříš stops are on 361 (Příbramsko). Card lists them. No change.

**418** (@ Praha, Stodůlky): → 13:25 14:25 15:25 18:25; ← 14:16 15:16 18:16 18:56. **B.** The shuttle's own every-30 regime before
15:55 (Stodůlky :25 / :55, Logport :10 / :40) and the hourly trips after 18:00. The peak (every 20, 15:55–17:55) is the modelled
pattern; one line cannot hold two rates. Card says so. No change.

**447** (@ Mníšek pod Brdy, železniční stanice): → 13:21 15:51 16:51 18:36; ← 13:20 15:50 18:34. **C.** Single trips at different
minutes: the železniční stanice shuttles 13:16 / 13:21, 18:30 / 18:36, 19:40 / 19:46, the Chouzavá trips 15:11 / 15:29. The 16:46 /
16:51 shuttle is what the OPS Magdaléna repeat 16:46 / 16:52 stands for. **Card corrected:** it listed 16:46 as off the pattern; it is
a slot. No other change.

**449** (@ Řitka, hlavní silnice): → 13:41 15:34 18:11; ← 13:04 16:17 16:47 17:35. **C.** The Bojov rounds (Mníšek 12:49, 14:05,
15:35, 17:20, 18:45; Bojov 13:25, 14:40, 16:10, 17:55: gaps 76 / 90 / 105 / 85 min) and the Jíloviště trips (Mníšek 16:05 16:35,
Jíloviště 15:19; 318 buses). No repeating minute. Card lists them. No change.

## ONE WAY

- **320** D (claim verified): 11 buses leave Smíchovské nádraží 13:00–19:00 (13:00, then :10 / :40 14:10–18:40) and 7 come back from
  Stříbrná Lhota (13:21 14:06 15:06 16:06 16:36 17:06 18:21), and nothing passes Mníšek náměstí towards Praha from further out;
  the morning trips start at Stříbrná Lhota (8 between 4:47 and 8:36). The outstation rule stands: inbound rate, 14:40, 16:40,
  18:40 listed.
- **336** B: the every-30 regime before the 14:53 peak (Zličín 13:05 13:29 13:59 14:28); the card says so.
- **310** C: Zličín → Nučice 14:19 16:17 18:18 (3 out), back 14:40 and 18:40 as 308 (2 back; the 16:17 bus has no return trip) — not 3
  each way; card says the 14:19 and 18:18 buses go back as 308.
- **338** C: Smíchovské nádraží 13:20 14:25 18:25 19:20, Štěchovice 13:25, Hradištko zámek 12:53, Pikovice 17:34; no repeating minute;
  listed.
- **446** B: the school extras 14:15–14:40 before the 15:12 pattern; the card says so.
- **340** E (artefact) and D (claim verified): the 26 "off" trips are all arrivals at Přemyslovská (the buses end there from 15:11 and
  leave from Levý Hradec, a terminal pair; the leg's stops end at Levý Hradec), including the slot trips. The going-home claim holds: in
  16:00–17:00 8 buses leave Dejvická (:11 :17 :23 :29 :41 :47 :53 :59) and 6 pass Roztoky, nádraží towards Dejvická (16:02 16:10
  16:17 16:32 16:40 16:50); the early trips start in Roztoky. Step 4 FEWER stays (6 slots for 8 outs, the inbound rate).
- **326** E: the flagged stop is Praha, Volha (:22 / :52 starts before Opatov, in Prague, on the Prague bus sheet); the card says so.
- **748** D: Mníšek → Řitka 13:19 14:19 15:19 (hourly :19, three trips) are trips whose buses go on as 318 (3 of 3);
  there is no Řitka → Mníšek trip of 748; the card says so.
- **313** E: Radotín → Choteč 13:13 15:13 17:13 (19:13) is a 2-hourly shuttle of one bus (9578) whose returns Choteč 14:19, 16:19,
  18:19 are three of the hourly :19 back slots; only the way out is off the pattern (3 one way, not 3 each way). A line of its own
  would double the :19 backs. **Card now says so.**
- **441** C: Jílové 14:10 17:50 18:50 and Luka 14:27 (19:08) are rounds of one bus at different minutes; the 15:05 / 15:45 pair is the
  slot pair.
- **664** C: backs 15:56 17:56 18:57 are 17–26 min off the 13:39 / 14:31 repeats; the outs are on the :18 slot; card lists them.
- **445** E: Jílové 13:45 14:45 15:45 leave 3 min earlier by učiliště, Kovo and Průmyslová (the path audit's one explained flag);
  the 12:48 / 16:48 / 18:48 trips take Pražská and Za Humny; the path changes by time of day, it is not two parallel services.

Other claims checked by the passing reading: 311 Mořina ("buses sleep at Mořina": Zličín → Mořina 15:15 16:15 17:15, Mořina →
Zličín 16:19 17:19, so 3 out and 2 back at Mořina, the claim holds; own line since v1) and 390 Třebenice (hourly both ways at Štěchovice, so
"sleep" is only the early trips).

## Table

| Line | Verdict | Change | Buses before → after |
|---|---|---|---|
| 390 | A | new Simutrans line 390 Štěchovice (:35 odd hours, every 120, window 15:00–17:00) | 3 → 5 |
| 359 | E (town path not modelled, open) | none | 2 → 2 |
| 444 | C | none | 2 → 2 |
| 356 | C | card lists the drifting edge trips | 6 → 6 |
| 688 | C | none | 3 → 3 |
| 418 | B | none | 1 → 1 |
| 447 | C | card: 16:46 is a slot, not off the pattern | 1 → 1 |
| 449 | C | none | 1 → 1 |
| 320 | D | none (claim verified) | 3 → 3 |
| 336 | B | none | 4 → 4 |
| 310 | C | none | 1 → 1 |
| 338 | C | none | 3 → 3 |
| 446 | B | none | 1 → 1 |
| 340 | E / D | none (artefact; claim verified) | 6 → 6 |
| 326 | E | none | 2 → 2 |
| 748 | D | none | 1 → 1 |
| 313 | E | card: the shuttle's returns are the :19 slots | 2 → 2 |
| 441 | C | none | 1 → 1 |
| 664 | C | none | 1 → 1 |
| 445 | E | none | 4 → 4 |

**Oblast total: 88 → 90 buses, 45 → 46 Simutrans lines.**

## For the owner (in-game change list)

- New line **390 Štěchovice**: Praha, Smíchovské nádraží → Štěchovice, Departure every 120, typed 34 (real 15:35, 17:35, 13:35);
  Štěchovice → Praha, Smíchovské nádraží, every 120, typed 34 (real 15:35, 17:35); 2 buses. 390 itself is unchanged.

## Could not decide

- **359 Roztoky town round** (first): regular both ways (out :13 / :43, back :39) and a path variant between nádraží and Levý Hradec that
  the game bus of the 340 :29 / :59 slots does not take (direct road). I kept it as carried by 340; a 340 + 359 circuit (Dejvická →
  nádraží :59 on 340, nádraží → Levý Hradec by the town on 359, Levý Hradec :39 → nádraží, nádraží :50 → Dejvická) with the slots
  moved out of 340 was not built or measured. The reviewer may overturn this E to A.
- 313 Choteč shuttle: regular (out :13, back :19, every 120, one bus) but its returns are three of the hourly :19 back slots, so a
  line of its own would double the backs; left on the card.
- 390 Štěchovice hourly: matches 3 of 4 hours each way but fails Step 4 by one empty back slot (16:35); every 120 chosen by rule 3.
