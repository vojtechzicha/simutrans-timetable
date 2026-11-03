# Kolínsko: review of the branch re-check, 3 Nov 2026

Independent of the designer's notes: every EACH WAY flag of `audit-passing-2026-11-03-before.txt` (662, 235002, 659) and of the
knot-fixed `audit-passing-2026-11-03-now.txt` (662, 235002), every ONE WAY flag with 2 each way (661, 822, 826, 235006, 435, 536,
660, 821), the others (235009, 460, 675, 491) and the changed line 659 were re-read from `data/derived/trips.json` at the flagged stop and
at the stop where the variant leaves the trunk, counting every trip that passes it wherever it starts or ends. Live-map buses from
`scripts/observed.py 675 2026-11-02`.

**Result: no model change; one card text FIX (675); the 662 owner check kept as a real choice.** Buses 71 → 71, 39 Simutrans lines.
`run_oblast.py kolinsko`: Step 4 77 of 77 ok; branch and path audits as in v1 (536 explained); passing 2 EACH WAY (662, 235002), 12 ONE
WAY, all with a verdict below; the one uncovered stop of the okres (Velký Osek, nádraží) is explained as in v1.

## FIX

**675 Kolín – Cerhenice – Pečky — FIX (card text only).** The note said the 14:03 and 18:03 Cerhenice buses "end there (their next trip
open for the live map)". The 2 Nov live map settles it: 8596 ran the 14:03 and went on as 679 at 15:16; the 18:03's bus (8596 again)
ended its day there; 1648 ran the 16:03 and came back as the 17:30 — the round `675 Cerhenice` models. The note now says so (a check
that waits on vehicle evidence is settled by it). Model unchanged: read at Cerhenice, Náměstí Míru, out :30 / :31 hourly (6), back 14:30,
16:30, 17:30, 18:30 — the Pečky trips every 120 plus the one Cerhenice start; 675 every 120 + 675 Cerhenice every 480 give the window's
3 out and 2 back exactly. D, claim right.

## PASS (re-derived)

**662 Čelákovice – Český Brod – Kouřim, the Kounice – Mochov shuttle — PASS (C; owner check kept).** At Kounice 13:00–19:00: out of
Mochov 13:27, 14:27, 15:27, 16:27 (:27), 17:33, 18:57 → Kounice :45; back 13:23, 14:33, 15:13, 16:13, 17:27, 17:55 → Mochov 13:41, 14:51,
15:31, 16:31, 17:45, 18:13. Read at Vykáň the same: out :38 four times, back :30, :40, :20, :20, :34, :02. Six each way, but the way back
repeats no minute three times (15:13 / 16:13 only; 13:23, 14:33, 17:27 are 10, 20, 14 min off an hourly :13), so the brief's A does not
apply and C does. Every stop is served hourly (Kounice by 661, Vyšehořovice – Vykáň – Černíky by 662). The trips are the Praha-východ
sheet's 354 buses: 354 Černý Most :00 reaches Mochov :27 and leaves Mochov :31, the shuttle leaves Mochov :27 and is back for :31
(the Praha-východ 354 card names the 12-of-17 chain). Is the owner check a real choice? Yes: a used branch (6 each way, the owner's 20
Oct "used branch in afternoon peak; just not at 16:00 exactly") whose way back fits no exact row is exactly "an approximation with its
slower option" — the designer offers the approximate line (`662 Kounice` every 60, Mochov :27 → Kounice, Kounice :13 → Mochov, 2 buses,
worst 20 min off on the way back) against listing it. Kept. Note that a 354 extension to Kounice on the Praha-východ sheet would carry
it with the 354 buses it really runs on; that is that sheet's question, named here for the coordinator.

**235002 MHD Kolín 2 — PASS (E).** At Šťáralka: every 20 both ways 13:16–16:56 / 13:15–17:15, then every 30 (17:01, 17:31, 18:01, 18:31 /
17:41, 18:11, 18:41). A time band, same route, anchor 14:50 at the every-20 pattern. The card says "then every 30".

**659 Český Brod – Kostelec nad Černými lesy – Stříbrná Skalice — PASS (C; the stop-path change is right).** Before the knot fix the
audit read Krupá 3/3: out 13:55, 14:55 (the :55 trips, 5 min before the :00 slot that starts at 16:00) and 15:25 (→ Kostelec); back 12:58
(→ Krupá), 13:50, 14:50 (Kostelec → Český Brod). Read at Krupá towards Český Brod: :31 hourly from 14:31 (the Stříbrná Skalice trips) +
13:09, 14:01, 15:01 — the Kostelec shorts repeat :01 twice only; towards Kostelec the 15:25 is one trip. No branch of 3 each way at a
repeating minute; the 13:55 / 14:55 are B (5 min off), the shorts C, all on the card. The out leg's road: the 16:00, 17:00, 18:00 (and
12:25) call at Prusice, rozcestí, the 13:55, 14:55 (and 19:00) at Prusice; the back trips all at Prusice. The window's slot trips are
16:00 and 17:00, so `stops_via` Prusice, rozcestí on the out leg is the slot trips' road (the 1 Nov rule, 329), Prusice stays on the way
back, and Prusice, rozcestí (okres Praha-východ, no other line on any sheet) is covered. Leg stops and `rt` 71 checked in
`schedule.json` (the Nučice – Výžerky – Nučice double passing is the real 16:00 path). Step 4 2/2 and 2/2 exact, 3 buses, unchanged.

**536 Kolín – Žiželice — PASS (one circuit line).** Out: 15:57, 17:57 by the Žiželice loop (58 min), 14:40, 16:57, 18:47 direct (46);
back: 15:26, 17:19 by the loop, 16:29, 18:29 direct — each path every 120 each way, alternating. The KB rule (`kb/rules/fork-schedule.md`:
path variants, one direction, two paths, alternating → one circuit line out on one path, back on the other) and the 329 precedent (the
owner, 1 Nov: "otherwise I agree with the way you modeled it" once the note said which road) give the circuit; two path lines every 120
would be 4 buses for 3 and approximate (the loop-road back trips 15:26 / 17:19 repeat no minute). The card names both roads and the
cost of the alternative. The brief's sentence "one line per path when both run regularly" overstates the 1 Nov lesson, which was about
naming the road; the KB rule is the one applied here. The ONE WAY flag at Žiželice, škola (2 + 3) is the loop-road back trips, named.

| Line | Flag | Reading (13:00–19:00) | Verdict | Designer |
|---|---|---|---|---|
| 661 | 2/3 at Semice | Lysá :15 hourly; Český Brod 15:00, 16:00, then 17:30, 18:30 (the 660 buses), 13:55; Semice short pair 15:40 / 16:02. | C | C ✓ |
| 822 | 2/4 at Plaňany | Kolín :19 hourly 13:19–16:19 (15:19 to Kouřim only), 17:24; Český Brod :30 from 15:30; towards Kolín past Kouřim 13:02, 14:02 (Klášterní Skalice), 14:56 (Kouřim), 16:07, 17:07, 18:07 — the Kouřim-only trips are 2 + 1. | C | C ✓ |
| 826 | 2/4 at Poříčany | 13:19, 14:14, 15:44, 16:46 out; 13:00, 14:00, 14:37, 15:30, 17:14, 18:44 back: about every 1½–2 h, the every-120 pair exact twice each. | C | C ✓ |
| 821 | 2/3 at Ždánice | Hourly :00 both ways at Ždánice; the flagged trips are those beyond Kouřim (Ždánice 14:00 → Horní Kruty, Kolín 15:02 → Horní Kruty, Horní Kruty 15:39 and 17:44 back, Ždánice 14:00 → Kolín): read at Horní Kruty, out :21 hourly (5, three of them the Sázava trips) and back 14:39, 15:39, 16:44, 17:44, 18:44 — the Horní Kruty end has 2 out / 2 back of its own; the v1 owner check (821 Horní Kruty, +1) already offers it. | C | C ✓ |
| 675 | 1/3 at Velim | see FIX (text) | D | D ✓ |
| 491 | 0/4 at Louňovice | 13:29–16:29 are the Mukařov :32 trips starting 3 min earlier at Louňovice, I.hráz (381, 382, 387 serve it on other sheets). | E | E ✓ |
| 435 | 2/3 at Říčany, podhradí | Klučov 13:32, 14:32 (:32), then :37 hourly; Říčany :00 hourly, 13:05 off. | B | B ✓ |
| 660 | 2/3 at Tuchoraz | Český Brod :00 hourly from 16:00 (12:55, 14:15, 15:10 before), Kostelec :02 from 15:02 (13:47 before). | C | C ✓ |
| 235006, 235009 | 2/3, 1/3 | factory and Štítary shift trips, no minute. | C | C ✓ |
| 460 | 1/3 at Zásmuky | school-day single trips (14:30, 14:45, 16:30, 18:20 / 14:22, 15:10, 16:25). | C | C ✓ |

Cards claiming buses go home / garage / sleep / outstation: only 675 ("the outstation rule") — the counts are right (3 out to Cerhenice,
1 back), the "end there" sentence replaced by the live-map facts.

## Table

| Line | Verdict | Change | Buses before → after |
|---|---|---|---|
| 675 | D | note: the live-map facts (8596 → 679; 1648 = the 16:03 / 17:30 round) | 2 → 2 |
| 662 | C | none (owner check kept as a real choice; 354 extension named for the Praha-východ sheet) | 3 → 3 |
| 659 | C | designer's `stops_via` Prusice, rozcestí verified, no change | 3 → 3 |
| 536, 235002, 661, 822, 826, 821, 491, 435, 660, 235006, 235009, 460 | as above | none | unchanged |

**Oblast bus total: 71 → 71.** Simutrans lines 39.

## Audits after the rerun
- Step 4: 77 timed legs, 77 ok.
- Branch: 536 "beyond" (the Žiželice, Loukonosy trip), as in v1, explained. Path: 536 loop road, MHD Kolín 1, 889 Chotutice, as in v1.
- Passing: 2 EACH WAY (662, 235002), 12 ONE WAY, all with a verdict above.
- Coverage: 468 of 473 afternoon stops on this sheet; Velký Osek, nádraží explained (705 on the Nymbursko sheet).
