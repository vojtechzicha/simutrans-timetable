# Mladoboleslavsko: review of the branch re-check, 3 Nov 2026

Independent of the designer's `branch-check-2026-11-03.md`. Every EACH WAY flag of `audit-passing-2026-11-03-before.txt` and
`audit-passing-2026-11-03-now.txt`, every ONE WAY flag with 2 each way, both new Simutrans lines and every card that says buses
sleep or go home were re-read from `data/derived/trips.json` at the flagged stop and at the stop where the variant leaves the
trunk (every trip that passes it, wherever it starts or ends), checked against `kb/lessons.md`, and where it mattered against the
2 Nov live map (`scripts/observed.py 716 / 767 2026-11-02`, the BUS column of `reading/<line>.txt`).

**Result: both new lines PASS (767 Krpy, 716 Sychrov); one card text FIX (716's "one bus"); every other verdict holds.**
`run_oblast.py mladoboleslavsko` after the fix: 57 Simutrans lines, 95 buses; Step 4 111 of 115 legs ok and the same 4 EMPTY as
before (722, 737 ×3: the approximations on the owner checks, kept); branch audit the one explained `[beyond]` (712); path audit the
7 explained 442 / 442 Dražice paths; no uncovered stop; passing audit 7 EACH WAY, 9 ONE WAY, all explained below or on the cards.

## FIX

### 716 — card text only
The note began "One bus: Mnichovo Hradiště 15:05 → round Sychrov → Mužský … plus Sychrov loops 13:47, 15:50, 17:45". That cannot be
one bus (the Mužský round is at Mužský 15:59–16:22 while the 15:50 loop runs), and the live map shows three: 8611 on the Mužský trips
(12:17, 13:42, 15:05, 16:22), 8663 on the 13:47 and 17:45 loops (727 and 733 in between), 8621 on the 15:50 loop (733, 345, 315, 717
around it). Note rewritten: the round and the loops, the buses seen, "the loops are a second bus, as modelled". No model change.

## PASS — the new lines

### 767 Krpy (A, every 60, 1 bus) — PASS
Read at Kropáčova Vrutice, rozcestí Krpy 13:00–19:00: towards Krpy 13:15 (Bezno → Dolní Slivno), 15:12 (Mladá Boleslav → Dolní
Slivno), 16:17, 17:17, 18:22 (Bezno → Krpy), 19:17; towards Bezno 13:40, 15:40 (Dolní Slivno → Bezno), 16:38, 17:38, 18:38 (Krpy →
Bezno). The Bezno – Krpy shuttle is 3 each way at :58 / :37 (18:03 is 5 min off), hourly: a branch by the 381 rule, so its own
line is right; the v1 card's "runs only over stops of 767 and is listed" left Bezno – Krpy with one bus in 4 hours in the game.
`notvia` Dolní Slivno separates it: schedule.json shows exactly the 3 + 3 shuttle trips on the Krpy legs (15:58, 16:58, 18:03;
16:37, 17:37, 18:37) and the 767 legs unchanged (4 / 9 trips, Dolní Slivno 13:29 and Bezno 18:58 off, named). Window 15:50–17:50:
out 15:58 16:58 = real, back 16:37 17:37 = real, exact; running time 20 min each way as the trips. `lay` 1 at Bezno: the timetable
chains Krpy :37 → Bezno :57 → :58; on 2 Nov these were two buses alternating with 699 (8607 ran 15:58 and 16:37, 8552 16:58, 17:37
and 18:03), but one game bus with the 1-minute turn holds the pattern (the method allows the real chaining, never under 1 min).
Why and note: full names, the three real trips named, the 18:03 named. 1 bus (767: 1 → 2).

### 716 Sychrov (A, every 120, 1 bus) — PASS, a judgement call decided for the line
The designer's own doubt: every stop of the loop is on the Mužský round (Step 8: a sparse variant over served stops is listed, not
modelled). Read at Mnichovo Hradiště, Podolí: the loops pass 13:57 / 14:13, 16:00 / 16:16, 17:55 / 18:11 (each loop serves every
stop both ways), the Mužský round 15:15 / 16:55. So Sychrov has 3 round trips 13:00–19:00 at a repeating 2-hour minute (13:47,
15:50, 17:45: all within 3 min of :47), which is the 20/30 Oct threshold for a regular afternoon branch (≥ 3 each way 13:00–19:00),
and the loops double Sychrov's afternoon service (about hourly with the round, every 2 hours without). Step 8's "list it" is for
one- or two-trip variants; the 110 Třeboradický hřbitov lesson (30 Oct) says model a regular branch as in real life. Step 4: window
15:00–17:00 slot 15:47 against real 15:50 (3 min, within); :47 has 1 exact (13:47) and all 3 within 3, better than :50 (17:45 is 5 off).
`notvia` Boseň, Mužský keeps the round out: schedule.json shows the 5 loop trips (5:00, 10:40 off; 13:47, 15:50, 17:45) and the 716 legs
unchanged. Running time 34 min as the trips. The live map confirms a second bus is real (above). 1 bus (716: 1 → 2). Kept as A.

## PASS — the other flags (the designer's verdict holds; my reading)

| Line | Flag | My reading at the stop (13:00–19:00) | Verdict |
|---|---|---|---|
| 737 | EACH WAY 6/8 | At rozcestí Podlázky 0.5, out of Mladá Boleslav via Čistá 13:00, 13:45, 14:35, 15:30, 16:30, 17:20, 18:20 and direct 14:15, 15:00, 16:00, 16:55, 17:50; back from Bělá via Čistá 13:50, 14:30, 15:30, 17:25, 18:25, direct 13:20, 14:10, 15:00, 16:30. Each path about hourly but drifting 5–30 min; the only Čistá-only trips are 14:25 out and 12:57 back (732's buses). Approximate rows, owner check kept. | B, PASS |
| 442 | EACH WAY 5/7 | Dražice shuttle, one bus: out of Benátky 13:00, 13:24, 14:02, 14:38, 14:58, 15:15, 15:38, 16:08, 16:58, 17:15; back 13:10, 13:45, 14:26, 14:48, 15:05, 15:26, 15:55, 16:45, 17:05. No minute repeats three times; two paths (7 of 10 outs and 6 of 9 backs by Husovo náměstí and Vaněčkova, the rest by Dražická) neither regular, so one line (1 Nov rule). Note: the game line takes the short path although the long one is commoner; Husovo náměstí and Vaněčkova are on 431, 768 and 442's own way back, and the why says so — left as the v1 reviewer accepted it. | C, PASS |
| 775 | EACH WAY 4/5 | At Luštěnice, Zelená: Horky trips 14:05, 15:16 out (13:40 from Mladá Boleslav, 14:15 from Zalužany), 14:31, 15:56 back (Horky 14:20, 15:45); local 15:06, 18:46; Zelená 15:46 → Benátky. Different origins and ends, no repeating minute. | C, PASS |
| 427 | EACH WAY 3/5 | At Rokytá, Dolní Rokytá, rozcestí towards Mimoň 13:57, 15:07, 15:42, 16:37 (Kuřívody), 18:02, 18:57; back 15:06, 16:05, 17:06, 17:51 (Kuřívody), 18:23. The back has three at :05 / :06 (Mimoň 14:32, 15:35, 16:35), the out none, so hourly cannot pass both ways (both ends at the same rate); every 120 on the 15:25 / 16:35 pair stands, 15:35 and 17:50 listed. | C, PASS |
| 715 | EACH WAY 3/4 | Bakov náměstí: Mnichovo Hradiště → Bakov 14:02, 15:32; Bakov → Mnichovo Hradiště 14:17; Mladá Boleslav 13:17 → Mnichovo Hradiště, 14:52 → Žehrov; Bakov 15:42, 17:37 → Žehrov; Žehrov 13:02, 17:12 → Bakov / Mladá Boleslav. Pieces of a school line, 2 of any kind. | C, PASS |
| 431 | EACH WAY 3/3 | Předměřice, u kostela: 13:29 → Benátky and 15:29 → Bezno (with 12:29 Boreč and 15:02 Benátky arriving a minute before, one bus every 2 h), Lysá 17:17 → Kochánky 17:35 and 17:39 back 17:43 — three different pairs. | C, PASS |
| 714 | EACH WAY 3/3 | Read beyond Kněžmost, náměstí: out 13:35 (Sobotka round), 14:55, 17:35 (Srbsko); back 14:58 (Sobotka → Kněžmost, ends), 17:35 (Dobšín 17:10). 3 out, 1–2 back: the "sleep at Srbsko and Dobšín" and "17:05 going home" claims hold; the Kněžmost shorts (14:00, 15:10; 13:35, 14:05, 14:40) have no repeating minute. | C + D, PASS |
| 732 | ONE WAY 2/4 | Bezdědice → Čistá 15:24, 17:19, 18:19; Čistá → Bezdědice 14:44, 15:48, 17:43, 18:43. Not a branch (same ends). Two at :19 and three at :43 / :44 with hour 16 empty both ways; hourly would pass Step 4 only in 17:00–19:00, outside the anchor rule's 13:00–18:00, so the every-120 round stands (1 bus either way). | C, PASS |
| 315 | ONE WAY 2/3 | Mladá Boleslav → Mnichovo Hradiště shorts 13:35, 14:05, 14:35 (a 13:35–14:35 pulse, nothing the other way), Mladá Boleslav 13:55, 14:25 → Praha; listed. | C, PASS |
| 345 | ONE WAY 2/3 | Mnichovo Hradiště, náměstí 13:43, 13:53 → Mladá Boleslav, 14:30 back, Praha 13:45 → Mladá Boleslav: one of each. | C, PASS |
| 412 | ONE WAY 2/3 | Praha → Mladá Boleslav 13:30, 14:45, 15:45; back 14:30, 16:30. Not 3 at one minute either way; the designer's count sentence replaces the "buses sleep" claim, right. | C, PASS |
| 467 | ONE WAY 1/6 | Roudnice nad Labem, ČSAD is the alias of u hřbitova; the audit reads the raw stop. The flagged :30 trips are the slots. | E, PASS |
| 699 / 712 / 724 / 725 | ONE WAY 1/3 | Single trips at single minutes as the designer lists them (699 Chotětov 12:40, 14:45 off :10, 17:10 by Písková Lhota; 712 Katusice 13:10, 15:15, 15:48, 13:40; 724 Libáň 12:30, 14:40, Březno 15:32; 725 single Záhuby / Vlčí Pole trips). | C, PASS |
| 720 | card claim | Praha → Semily 13:15, 14:15, 17:15, 18:15 against Semily → Praha 13:50, 15:50; at Turnov 6 each way: "sleep in Semily and Rokytnice" holds. | D, PASS |

722 and 737 keep their owner checks (the data gives no reason to change them).

## For the owner (in-game change list)
As in the designer's `branch-check-2026-11-03.md`: new **767 Krpy** (Bezno typed 57, Krpy typed 36, every 60, 1 bus) and new
**716 Sychrov** (dopravní terminál typed 46, every 120, loop through Podolí, Dolení Kruhy, Hoření Kruhy, Sychrov, Pazderna, u rybníka
and back, 1 bus). 767 and 716 themselves unchanged. This review changes no value.

## Totals
Mladoboleslavsko: 55 → 57 Simutrans lines, 93 → 95 buses (767 Krpy +1, 716 Sychrov +1). Unchanged by this review.
