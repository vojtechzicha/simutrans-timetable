# Praha-západ: review of the branch re-check, 3 Nov 2026

Independent of the designer's `branch-check-2026-11-03.md`. Every EACH WAY flag of `audit-passing-2026-11-03-before.txt` and
`audit-passing-2026-11-03-now.txt`, every ONE WAY flag with 2 each way, every changed line and every card that says buses sleep or
go home was re-read from `data/derived/trips.json` at the flagged stop and at the stop where the variant leaves the trunk (every trip
that passes it, wherever it starts or ends), checked against `kb/lessons.md`, and where it mattered against the 2 Nov live map
(`scripts/observed.py 340 / 390 / 359 2026-11-02`, and the BUS column of `reading/<line>.txt`).

**Result: one FIX in the model (340 / 359: the Roztoky town round is now the Simutrans line 340 Masarykova, 0 extra buses), one
PASS with a note (390 Štěchovice), the rest PASS.** `run_oblast.py praha-zapad` after the fix: 47 Simutrans lines, 90 buses; Step 4
99 of 101 legs ok and the same 2 FEWER as before (340 out of Dejvická and 356 Velká Brána, both outstation rows at the inbound
rate); branch audit all `[ok]`; path audit the one explained 445 path; no uncovered stop; passing audit as listed below.

## FIX

### 340 / 359 — the Roztoky town round (designer's open item: E → A)
Read at Roztoky, Masarykova 13:00–19:00: towards Levý Hradec the town round passes at 13:37, 14:42, 15:15, 15:46, 16:16, 16:46,
17:16, 17:46, 18:16, 18:45 (nádraží :13 / :43, every 30 from 15:12), towards nádraží at 14:42, 15:44, 16:44, 17:46 (Levý Hradec
:39 hourly). That is ≥ 3 each way at a repeating minute, a regular path variant of the 340 trips, so by the 381 rule and the
owner's 1 Nov rule (one line per path when both run regularly) it gets its own Simutrans line; the designer's reason for keeping it
unmodelled (same buses, same times, stops covered by 359 Suchdol) is true of the timing but hides the path: in the game the four
town stops (17. listopadu, Masarykova, Solníky, Obránců míru) had one bus an hour each way where reality has three towards Levý
Hradec and two towards nádraží.

The live map of 2 Nov shows the real operation is two clean one-bus hourly cycles with a 1-minute turn, not a bus-count problem:
bus 8800 ran Dejvická :59 → nádraží :13 → 359 round the town → Levý Hradec :23 → 340 :24 → Dejvická :45 → :59 all afternoon
(14:58, 15:59, 16:59, 17:59 out; 15:24, 16:24, 17:24 back), and bus 8814 the same at :29 → :43 → :53 → :54 → :15 → :29 (15:29,
16:29, 17:29 out; 15:54, 16:54 back).

**Change (`lines.json`):**
- `340` keeps the direct road with 4 slots: Dejvická :11 :17 :41 :47 (typed 10 16 40 46), Levý Hradec :02 :09 :32 :42 (typed 1 8
  31 41; the :42 is still the nádraží :50 bus read at the knot). `lay` 0 on the back leg: the real turns at Levý Hradec are
  0 min (:11 → :32 → :32, bus 8760; :41 → :02 → :02, bus 1469), 1 min (:47 → :08 → :09, bus 1896) and 4 min (:17 → :38 → :42),
  as the sheet already models 0-minute turns elsewhere (441, 447); without it the need came out 5 instead of the real 4.
  `via` Tyršovo náměstí on the out leg, so that the nádraží-ending :29 / :59 trips count only for 340 Masarykova (without it
  the builder read them on both legs and listed them as off the pattern on 340). Step 4: out 8 slots against 12 real in
  15:41–17:41 (the four :23 / :53 are the outstation remainder, so the row stays FEWER as before), all 8 exact; back 8 slots =
  8 real, all exact. **6 → 4 buses.**
- New `340 Masarykova`, every 60, three legs: Dejvická :29 :59 → Roztoky, nádraží (the 340 trips that end there, `notvia`
  Tyršovo náměstí so the through trips do not count; typed 28 58), nádraží → Levý Hradec untimed with `lines: ["359"]` (the
  round: Tyršovo náměstí, 17. listopadu, Masarykova, Solníky, Obránců míru, rozcestí Žalov, Přemyslovská; 9 min; no timetable,
  the bus goes straight on as the real 359 does at :13 / :43), Levý Hradec → Dejvická read at the knot nádraží :02 / :32
  (= Levý Hradec :24 / :54, typed 23 53), `lay` 1 as the timetable turns. Step 4: out 15:59 16:29 16:59 17:29 = real, exact;
  back 15:54 16:24 16:54 17:24 = real, exact. **2 buses.** Together with 340: 6, the same as the old single line.
- Cards: 340 note and why (two lines, one per path; the :23 / :53 going-home claim now names the buses: 8880 and 1468 ran them
  on 2 Nov and came back to Dejvická without a 340 trip), 359 note (the round out of nádraží is 340 Masarykova; the hourly :39
  round back is carried by 340's :42 slot on the direct road, so towards nádraží the four town stops keep this line's hourly
  service only), and the sheet `notes` sentence on 340 → 359.

**Passing audit after the fix:** `[EACH WAY] 359 (340 Masarykova, 359): 5 each way, 10 one way at Roztoky, rozcestí Žalov`. This is
an audit artefact, not a gap: `passing_check.py` takes a leg's slots from `real`, which is empty for an untimed leg, so the 8
nádraží → Levý Hradec rounds the new leg carries are still printed; the 4 Levý Hradec :39 → nádraží rounds are carried by 340's
:42 slot (direct road, said on both cards), and 13:25 Suchdol → Maxmiliánka is 30 min off :55 (listed). If the coordinator wants
the audit clean, the script would have to give an untimed leg the arrival times of the leg before it; timing the leg at nádraží
instead (`at` [13, 43], `lay` 0) would also clear it but puts a timetable on a knot the bus passes through (Step 6), so I did not.

### 340 — new EACH WAY flag since the knot fix (3 each way at Roztoky, u rybníčku): D + C, PASS
→ 15:23 15:53 16:23 16:53 17:23 17:53 (the :23 / :53) and 13:05, 13:55; ← 13:49, 14:16, 18:18. Read at u rybníčku 15:00–18:00:
8 out an hour, 6 back (Levý Hradec :02 :09 :24 :32 :54 and nádraží :50), and the buses sleep in Roztoky (first trips 5:21–6:00
start there). Which two outs fall off: the plates say :23 / :53 (8880 and 1468 ran them with no 340 trip back), so the designer's
choice stands: D. The three ← trips are single minutes before and after the peak (13:49 by 1896, 14:16 by 8800, 18:18 by 1468):
C. The flag stays (the :23 / :53 are off the pattern by the outstation rule) and both cards say why.

## PASS (the designer's verdict holds; my reading)

| Line | Flag | My reading at the stop (13:00–19:00) | Verdict |
|---|---|---|---|
| 390 | EACH WAY 7/7 (before), 4/5 (now) | At Štěchovice: Smíchovské nádraží → Štěchovice shorts arrive 14:30, 16:10, 17:10, 18:10 (13:55, 15:35, 16:35, 17:35 out); Štěchovice → Smíchovské nádraží shorts 13:55, 14:35, 15:35, 17:35. 3 at :35 each way → own line. Hourly fails Step 4 in every 2-hour window (no Štěchovice 16:35; out 15:35 16:35 17:35 but back 15:35 _ 17:35). Every 120 at :35 odd hours: window 15:00–17:00 one slot each way, both real; over the day out 3 of 8 exact, back 2 of 9 — more than the 1-bus alternative (out :35 even, back :35 odd: 1 and 2 exact), so Step 4 rule 3 keeps the designer's choice, 2 buses. `notvia` Třebenice separates the legs (schedule.json: 8 and 9 short trips, no Třebenice trip). 390 Třebenice unchanged (13 / 13 trips, 3 buses). Live map: the shorts are single trips of 361-course buses (1123 13:55 and 14:35, 1124 16:35 and 17:35, 1128, 1131, 1144, 1145) with 440 in between, so the pooling note is right. The remaining 4/5 flag is 13:55 both ways, 14:35 and 16:35 (even hours) and 390's 14:35, 18:40, 13:56, 17:06, all named on the card. | A, PASS (1-bus alternative noted here, not an owner check: both pass Step 4 and the rule decides by exact hits) |
| 444 | EACH WAY 5/8 | At Kamenice, u Dvora towards Kamenice: 13:12, 14:12, 14:54, 16:51, 17:21 (from Jílové), 16:03 (from Davle, the modelled :27 slot); towards Jílové: 13:29, 18:44 only, the rest go to Davle (:29, modelled) or Těptín (15:59, 16:59, 18:18, 5-minute shorts one way). No minute repeats three times either way. All stops on 444. | C, PASS |
| 356 | EACH WAY 4/7 | At Statenice, Černý Vůl, hospoda the four-destination rotation is exact 14:00–18:00; the flagged trips are the edges (Bořislavka 13:10, 13:30, 18:00, 18:12, 18:24, 18:38; Statenice 13:30, 18:38; Lichoceves 14:04, 17:19, 18:04), single minutes. Velká Brána: 6 out an hour from Bořislavka against 5 back past Horoměřice (v lipkách :41 is the only short return), so the :55 off-pattern claim holds. | C (+ D for Velká Brána), PASS |
| 688 | EACH WAY 4/5 | At Nový Knín, Starý Knín: towards Dobříš 13:09, 13:37, 14:45, 17:45; back 13:00, 13:50, 15:50, 18:20. Two at :45 and two at :50, never three. Dobříš stops on 361. | C, PASS |
| 418 | EACH WAY 4/4 | Stodůlky :25 / :55 until 15:25, :15 / :35 / :55 from 15:55 to 17:55, then hourly. The flagged trips are the every-30 regime (13:25, 14:25, 15:25; Logport 14:10, 15:10) and the evening (18:25; 18:10, 18:50). Modelled at the every-20 peak, one bus, as the card says. | B, PASS |
| 447 | EACH WAY 3/5 | Single shuttles 13:16 / 13:21, 18:30 / 18:36, the Chouzavá 15:11 / 15:29; the 16:46 / 16:51 is the OPS Magdaléna repeat's slot (card corrected by the designer, right). | C, PASS |
| 449 | EACH WAY 3/4 | Bojov rounds at Řitka: out 13:04, 14:20, 15:50, 17:35, 19:00; back 13:41, 14:56, 16:26, 18:11 — gaps 76–105 min, no repeating minute; modelled every 90 on the 14:05 / 15:35 rounds, exact. Jíloviště 16:05, 16:35 out, 15:19 back (318 buses). | C, PASS |
| 320 | ONE WAY 2/4 | At Mníšek pod Brdy, náměstí: 11 towards Stříbrná Lhota (13:00, then :10 / :40 14:10–18:40), 7 towards Praha (13:21, 14:06, 15:06, 16:06, 16:36, 17:06, 18:21), nothing from further out; morning trips start at Stříbrná Lhota. Inbound rate, every 120 with three slots each way exact; 14:40, 16:40, 18:40 off (their buses have no return within 15 min, the others turn in 15). | D, PASS |
| 336 | ONE WAY 2/4 | Every 30 before the every-20 peak from 14:53; card says so. | B, PASS |
| 310 | ONE WAY 2/3 | Nučice shorts at Tachlovice, Na vrškách: out 14:37, 16:35, 18:36 (every 120 at ~:36, 3), back only 14:17 (the 12:36 is before 13:00); the 14:19 and 18:18 buses go back as 308 (card). 3 one way, no empty return (Nučice is on 310's path). | C, PASS |
| 338 | ONE WAY 2/3 | At Štěchovice: Smíchovské nádraží 13:20 (38 min off :58), 14:25 (33 off), Štěchovice 13:25 → Pikovice, Hradištko zámek 12:53, Pikovice 17:34 (5 off :29): single minutes. | C, PASS |
| 446 | ONE WAY 2/3 | Kytín school extras 14:15–14:45 before the 15:12 pattern; card says so. | B, PASS |
| 326 | ONE WAY 1/6 | Praha, Volha :22 / :52 starts, in Prague (Prague bus sheet). | E, PASS |
| 748 | ONE WAY 1/5 | Mníšek → Řitka 13:19, 14:19, 15:19 are 318 buses; no 748 trip Řitka → Mníšek; stops on 320 and 448. | D, PASS |
| 313 | ONE WAY 1/3 | Radotín :13 → Choteč 13:13, 15:13, 17:13 (and 16:43); back from Choteč 14:19, 16:19, 17:19, 18:19 are the hourly :19 slots the model already has (knot Choteč). The shorts are 3 extra outs at the inbound rate's cost; an own line would double the :19 backs. Card now says so. | E, PASS |
| 441 | ONE WAY 1/3 | Jílové 14:10, 17:50, 18:50 and Luka 14:27 single rounds; 15:05 / 15:45 is the slot pair. | C, PASS |
| 664 | ONE WAY 1/3 | Vonoklasy → Černošice 15:56, 17:56, 18:57 are 17–26 min off the 13:39 / 14:31 repeats; card lists them. | C, PASS |
| 445 | ONE WAY 0/3 | The 13:45 14:45 15:45 Jílové departures take učiliště, Kovo, Průmyslová (the path audit's explained flag); the path changes by time of day. | E, PASS |
| 311 Mořina | card claim | Zličín → Mořina 15:15, 16:15, 17:15; Mořina → Zličín 16:19, 17:19; nothing from further out towards Zličín at :19 but the Řevnice :12 trips (on 311). 3 out, 2 back: the "sleep at Mořina" claim holds; own line since v1. | D, PASS |

Designer's card-only changes (313, 356, 447 notes): checked against the trips, all correct. 390 Štěchovice why and note: correct,
full stop names, running times 35 / 34 as the trips. 

## For the owner (in-game change list, this review's part)
- **340** (edit): Dejvická keeps typed 10 16 40 46 — remove 28 and 58; Levý Hradec keeps typed 1 8 31 41 — remove 23 and 53.
  4 buses (2 move to the new line). The Levý Hradec entry's 0-minute turns rely on the fork's automatic Leave up to, as the
  sheet's other 0-minute turns do.
- **340 Masarykova** (new): Praha, Dejvická → Lotyšská, Čínská, Nádraží Podbaba, Výzkumný ústav vodohospodářský, V Podbabě,
  Roztocká, Sedlecký přívoz → Roztoky, nádraží (no timetable) → Tyršovo náměstí, 17. listopadu, Masarykova, Solníky, Obránců
  míru, rozcestí Žalov, Přemyslovská → Levý Hradec, back by rozcestí Žalov, u rybníčku, Tyršovo náměstí, nádraží and the same
  Prague stops to Dejvická. Dejvická: Departure every 60, typed 28 and 58 (real :29 / :59). Levý Hradec: every 60, typed 23 and 53
  (real :24 / :54). 2 buses.
- **390 Štěchovice** (new, designer): as in `branch-check-2026-11-03.md`: typed 34 at both ends, every 120, 2 buses.

## Totals
Praha-západ: 45 → 47 Simutrans lines (390 Štěchovice, 340 Masarykova), 88 → 90 buses (390 Štěchovice +2; 340 split 6 → 4 + 2).
