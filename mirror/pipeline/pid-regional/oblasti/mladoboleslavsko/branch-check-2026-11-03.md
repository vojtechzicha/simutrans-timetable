> Superseded where `branch-review-2026-11-03.md` differs: 716 (card text). The review stands.

# Mladoboleslavsko: branch re-check, 3 Nov 2026

Why: the owner found that short workings and branches had been filed as "off the pattern" because trips were grouped by start and
end stop (381 Zásmuky). Queue: the 8 EACH WAY and 10 ONE WAY flags of `audit-passing-2026-11-03-before.txt` (rerun after the coordinator's loop fix of `passing_check.py`: the only change here is that 716 no longer prints). Every flag was read
again from `data/derived/trips.json` and `reading/<line>.txt` at the flagged stop and at the stops where a variant leaves the
trunk. Minutes below are the times of the off-pattern trips at the flagged stop (→ and ← as the audit prints them); the
whole-day trips are in the reading files.

**Result:** 2 missed branches modelled (767 Krpy, 716 Sychrov), every other flag is a pattern the card
already names or an artefact. Simutrans lines 55 → 57, buses 93 → 95. `run_oblast.py` is clean: Step 4 has the same 4 failing
legs as before (722, 737 ×3, the approximations on the owner checks), branch audit one explained `[beyond]` (712), path audit the 7
explained 442 / 442 Dražice paths. No uncovered stop.

## EACH WAY

**737** (@ Mladá Boleslav, rozcestí Podlázky 0.5): → 13:54 14:34 14:44 17:04 17:29 17:59 18:29; ← 13:08 13:41 14:16 14:31 17:51
18:51. **B.** These are the line's own trips on its two paths, 5–30 min off the :00 / :30 slots. Via Čistá: out of Mladá Boleslav
13:00 13:45 14:35 15:30 16:30 17:20 18:20, back from Bělá 12:40 13:50 14:30 15:30 17:25 18:25. Direct: out 14:15 15:00 16:00 16:55
17:50, back 13:20 14:10 15:00 16:30. Each path is about hourly but with gaps of 45–60 min and no repeating minute, so the row stays
approximate on the owner checks. No branch hides in it: the only Čistá-only trips are Mladá Boleslav 14:25 → Čistá and Čistá 12:57
→ Mladá Boleslav (the 732 chain). No change.

**442** (@ Benátky nad Jizerou, Vaněčkova): → 13:17 13:52 14:33 15:09 15:33 16:02 16:52; ← 13:02 13:26 14:04 16:10 17:17. **C.** All
Dražice shuttle trips (one bus, 1–5 min turns). Out of Benátky 13:00 13:24 14:02 14:38 14:58 15:15 15:38 16:08 16:58 17:15; back from
Dražice, dvůr 13:10 13:45 14:26 14:48 15:05 15:26 15:55 16:45 17:05. Two paths: short (Dražická, u hřbitova, Na Štěpničce) and long
(Husovo náměstí, Vaněčkova; 7 of the 10 outs and 6 of the 9 backs). Neither path has a repeating minute (long out :00 :24 :02 :38
:38 :08 :15; short out :58 :15 :58), so no second line (1 Nov rule: one line per path only when both run regularly). The model
(5 slots per 2 h, short path) is the rate of the shuttle. Card: added the two paths and why one line. No other change.

**767** (@ Kropáčova Vrutice, rozcestí Krpy): → 13:43 16:38 17:38 18:38; ← 13:18 16:17 17:17 18:22. **A.** Read at the stops it passes,
the Bezno – Krpy shuttle is hourly: Bezno 15:58, 16:58, 18:03 → Krpy (:58, :58, :03); Krpy 16:37, 17:37, 18:37 → Bezno (all
:37); 3 each way, 20 min each way. The old card called it "listed, runs only over stops of 767", but the 767 line itself runs
every 240, so Bezno – Krpy had one bus in 4 hours instead of one an hour. **Change:** new Simutrans line **767 Krpy**, every 60,
Bezno :58 → Krpy (rt 20), Krpy :37 → Bezno (rt 20), `notvia` Dolní Slivno on both legs so the full-length trips are not counted,
window 15:50–17:50 by hand. Step 4: out slots 15:58 16:58 = real 15:58 16:58 (exact); back slots 16:37 17:37 = real 16:37 17:37
(exact); fill 100 %. Whole day: out 2 of 3 exact (18:03 is 5 min off, listed), back 3 of 3. Turn 1 min at Bezno as in the timetable.
**1 bus** (767: 1 → 2). The 767 line is unchanged. Off the pattern on the card: Dolní Slivno 13:29, Bezno 18:58 → Dolní Slivno.

**775** (@ Luštěnice, Zelená): → 13:31 14:31 18:06 18:46; ← 13:26 14:05 15:06 15:16 15:46. **C.** Luštěnice local trips (Brodecká –
Sluneční – Zelená: 15:02, 18:44) and the Horky nad Jizerou trips: out Mladá Boleslav 13:40, Zalužany ŠKODA 14:15, Luštěnice, Zelená
15:46 → Benátky; back Horky 14:20, 15:45. Horky: toward it 12:56 14:15 15:26 15:56, from it 12:57 14:20 15:45 (gaps 79, 71, 30 / 83, 85 min), from different
origins and to different ends, no repeating minute. Card already lists them. No change.

**427** (@ Rokytá, Dolní Rokytá, rozcestí): → 14:07 15:07 16:47 18:12 18:57; ← 16:16 18:04 18:23. **C.** Mnichovo Hradiště →
Mimoň 13:40 15:25 17:45 18:40 (gaps 105 / 140 / 55), Mimoň → Mnichovo Hradiště 14:32 15:35 16:35 17:50; the 16:20 and 17:41 Kuřívody
shorts are 1 each way. The modelled 15:25 trip is the one by Horní Rokytá; the others pass Dolní Rokytá by the direct road. No
repeating minute on the Mnichovo Hradiště side. Card already lists them. No change.

**715** (@ Bakov nad Jizerou, náměstí): → 13:02 14:02 15:32; ← 13:17 14:17 14:52 17:37. **C.** A school line in pieces: Mnichovo
Hradiště → Bakov 13:39, 15:09; Bakov → Mnichovo Hradiště 14:15; Mladá Boleslav 13:00 → Mnichovo Hradiště; Mladá Boleslav 14:35 →
Žehrov; Bakov 17:35 → Žehrov. Different ends and minutes, 2 trips of any one kind. Card already lists them. No change.

**431** (@ Předměřice nad Jizerou, u kostela): → 13:29 15:29 17:35; ← 13:28 15:28 17:43. **C.** Three different pairs: Předměřice
13:29 → Benátky and 15:29 → Bezno with Boreč 12:29 and Benátky 15:02 arriving 1 min before (one bus, 2 each way every 2 h at
:28 / :29), and Lysá 17:17 → Kochánky and back 17:39 (a different branch). Not 3 each way on one branch. Card already lists them.
No change.

**714** (@ Mladá Boleslav, autobusové stanoviště): → 13:17 14:27 15:02; ← 14:00 15:10 17:05. **C.** Out of Mladá Boleslav: Sobotka
13:05, Kněžmost 14:00, Srbsko 14:30, Kněžmost 15:10, Srbsko 17:05, Dobšín 19:05; back at Kněžmost, náměstí 13:35 14:05 14:40 15:40
17:35. Read at Kněžmost, náměstí beyond Kněžmost: out 13:35 (Sobotka) 14:55 17:35, back 14:58 (Sobotka, ends there) 17:35: 3 out,
2 back, so the "buses sleep at Srbsko and Dobšín" claim and the "17:05 bus going home" stand. No repeating minute on the short
trips (:00 :30 :10). No change.

## ONE WAY

- **732** C: out Bezdědice 15:24 17:19 18:19, back Čistá 14:44 15:48 17:43 18:43; the hour 16 has no trip either way, so an hourly
  pattern fails Step 4; the real rate (3 out, 4 back in 6 h) is nearer every 120. Listed on the card; the 13:15 Březovice → Bezdědice
  5-min trip is also off the pattern.
- **315** C: Mladá Boleslav shorts 13:35 14:05 14:35 → Mnichovo Hradiště and 13:55 14:25 → Praha, one pulse 13:35–14:35, not an
  afternoon pattern; listed on the card.
- **345** C: Mnichovo Hradiště, náměstí 13:43 13:53 → Mladá Boleslav, Mladá Boleslav 14:30 → Mnichovo Hradiště, Praha 13:45 →
  Mladá Boleslav; one of each kind; listed.
- **412** C, card corrected: Praha → Mladá Boleslav 13:30 14:45 15:45 and back 14:30 16:30 (3 out, 2 back, no repeating minute).
  The old claim "the buses sleep in Jičín and Mladá Boleslav, so Praha sends more out" is true only by one trip (6 leave Praha and
  5 arrive 13:00–19:00), so the card now gives the counts.
- **467** E (scan artefact): the ČSAD stop is the alias of u hřbitova (`terminus_alias`); the audit reads the raw stop. The flagged
  Mladá Boleslav :30 trips (13:30 14:30 15:30 16:30) and Mělník 13:33 are the hourly :30 slots and the Mělník short.
- **716** A (loop): the Mužský round passes the Sychrov loop at 15:26 and 17:06, and the three loop-only trips Mnichovo Hradiště
  13:47, 15:50, 17:45 (34 min, back by the same road, so each stop is passed both ways) are a regular 2-hourly service the old card
  called "listed". Together they make a bus through Sychrov about every hour (13:06 14:08 15:26 16:11 17:06 18:06). **Change:** new
  Simutrans line **716 Sychrov**, every 120, one loop leg Mnichovo Hradiště, dopravní terminál → same, slot 15:47 (typed 46), `notvia`
  Boseň, Mužský so the Mužský rounds are not counted; default window 15:00–17:00: slot 15:47 vs real 15:50 (3 min); loops 13:47
  (exact) 15:50 (3) 17:45 (2); the 5:00 and 10:40 loops are off. **1 bus** (716: 1 → 2). Before the coordinator's fix the audit kept
  printing 716 ONE WAY because it kept one time per stop name and read the loop at its arrival; after the coordinator's fix of `passing_check.py` the 716 flag is gone
  (the original flag was real: the old 716 had no leg for the loops).
- **699** C: Chotětov → Mladá Boleslav 12:40 and 14:45 are off the :10 slots (the 13:10 and 15:10 returns are 769's, carried); 17:10
  is on a slot but runs by Písková Lhota where the 769 trips run by Doubravička, which is all the flag at Písková Lhota shows.
- **712** C: Mladá Boleslav → Katusice 13:10 15:15, Katusice → Mladá Boleslav 15:48, Katusice 13:40 → Bělá; 2 or 1 of each; listed.
- **724** C: Mladá Boleslav 12:30 14:40 → Libáň (10 min off the slots) and Březno 15:32 → Řitonice; listed.
- **725** C: Mladá Boleslav 12:30 and 17:30, Zelenecká Lhota and Záhuby trips at single minutes; listed.

Other claims checked by the passing reading: 714 (above), 412 (above), 720 ("buses sleep in Semily and Rokytnice": Praha → Semily
13:15 14:15 17:15 18:15 against Semily → Praha 13:50 15:50; at Turnov, Terminál 6 pass each way, balanced, so the claim stands).
722 and 737 keep their owner checks.

## Table

| Line | Verdict | Change | Buses before → after |
|---|---|---|---|
| 737 | B | none | 4 → 4 |
| 442 | C | card: the two Dražice paths and why one line | 4 → 4 |
| 767 | A | new Simutrans line 767 Krpy (Bezno :58 / Krpy :37, every 60, window 15:50–17:50) | 1 → 2 |
| 775 | C | none | 3 → 3 |
| 427 | C | none | 1 → 1 |
| 715 | C | none | 2 → 2 |
| 431 | C | none | 3 → 3 |
| 714 | C | none (claims checked) | 2 → 2 |
| 732 | C | none | 1 → 1 |
| 315 | C | none | 8 → 8 |
| 345 | C | none | 5 → 5 |
| 412 | C | card: counts instead of "buses sleep" | 3 → 3 |
| 467 | E | none (alias artefact) | 4 → 4 |
| 716 | A | new Simutrans line 716 Sychrov (loop, :47 every 120) | 1 → 2 |
| 699 | C | none | 2 → 2 |
| 712 | C | none | 2 → 2 |
| 724 | C | none | 1 → 1 |
| 725 | C | none | 2 → 2 |

**Oblast total: 93 → 95 buses, 55 → 57 Simutrans lines.**

## For the owner (in-game change list)

- New line **767 Krpy**: Bezno → Kropáčova Vrutice, Krpy, Departure every 60, typed 57 (real :58); Krpy → Bezno typed 36 (real :37);
  1 bus. 767 itself is unchanged.
- New line **716 Sychrov**: loop from Mnichovo Hradiště, dopravní terminál through náměstí, za zámkem, Podolí, Dolení Kruhy, Hoření
  Kruhy, Sychrov, Pazderna, u rybníka, Sychrov and back, every 120, typed 46 (real 15:47, 13:47, 17:47 odd hours); 1 bus.

## Could not decide

- 716 Sychrov (a judgement call, not settled): each loop trip passes every Sychrov stop twice (Podolí 13:57 and 14:13, Pazderna 14:05
  and 14:11), so read at Podolí it is 3 out and 3 back at a repeating 2-hour minute, and the fixed audit shows it covered. The counter
  argument is Step 8: every stop of the loop is already on the Mužský round, so the loop adds frequency, not a stop. +1 bus.
- The 767 Krpy window (15:50–17:50) and the 18:03 trip 5 min off :58 are my hand choices; the other windows that pass Step 4 for
  both legs do not exist (an hourly :58 / :37 pair has 18:03 and no 17:58).
