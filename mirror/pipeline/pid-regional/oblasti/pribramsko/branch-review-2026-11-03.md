# Branch review, PID Příbramsko, 3 Nov 2026 (independent reviewer)

Reviewed the designer's `branch-check-2026-11-03.md` and the edited `lines.json` (diff against v1 in the repo: 361 every 120 →
every 60 with `anchor` 14:30 and an owner check; card text on 319, 360, 392, 393, 395, 454, 478, 495, 520, 521) against
`data/derived/trips.json`, `schedule.json`, the 2 Nov live map (`scripts/observed.py <line> 2026-11-02` for 360, 361, 393, 478,
500, 521, 522, 524, 549, 551, 552, 567, 754, 319, 450) and `kb/lessons.md`. Every EACH WAY verdict and every "going home" claim was
re-derived from the trips read at the flagged stop (every trip passing it 13:00–19:00, wherever it starts or ends). A scan of my own
then ran over every line: off-pattern trips at every stop by direction, a repeating-minute search (period 60 / 120 / 180 / 240,
tolerance ±3 and ±6) with ≥ 3 trips each way, every timed leg's real trips 13:00–19:00 against its slots, and every trip end that is
not a modelled terminal.

**Result: the designer's one model change (361) is right and stands; no missed branch (no verdict A). Five card texts were
wrong or incomplete by the plates and are fixed (522, 524, 567, 501, the sheet notes). No bus count changes.**

## The model change: 361 Praha – Štěchovice – Nový Knín – Dobříš → PASS

- Read at Štěchovice 13:00–19:00 (every 361 trip passes it): towards Dobříš 13:42, 14:42, 15:42, 16:42, 17:42, 18:42 (6, the
  Prague :05 trips, all exact); towards Prague 13:15, 14:55, 15:55, 17:05, 18:35 (5; Dobříš 12:25, 14:05, 15:05, 16:15, 17:45).
  6 out and 5 back: the return trips are there. v1's "outstation at half the inbound rate" read the single 16:15 in the 15:30–17:30
  band; the brief's rule (the outstation rule only applies to what is left after the passing reading) makes that wrong, as the
  designer says.
- Step 4 in the hand window 14:00–16:00 (`schedule.json`): out leg slots 14:05, 15:05 = real 14:05, 15:05, exact 2/2, 11 of 14
  trips of the day exact (off: 7:20, 20:15, 21:15 to Nový Knín); back leg slots 14:05, 15:05 = real 14:05, 15:05, exact 2/2, over
  the day 2 of 11 (the uneven morning minutes and 12:25, 16:15, 17:45, 19:35). Both legs pass.
- The hand anchor: 14:00–16:00 and 15:00–17:00 tie at 6 departures (I counted the same), so the default is 16:00 and its
  15:30–17:30 band, where every 60 fails the back leg (16:15 is 10 min off the :05 slot) and every 120 at 16:05 / 16:15 passes.
  So the window choice decides the model, and it is a real choice between two exact-in-window patterns: hourly (4 buses, the
  Prague departures exact all afternoon, the trips from Dobříš approximate over the day) or every 120 (2 buses, half the hourly
  Prague departures off the pattern, which is exactly what the owner objected to on 381). The owner check is therefore a real
  choice, not a re-asked rule; kept as written.
- Buses: 4 follows from the slots (Prague :05 → Dobříš :35, wait 30, Dobříš :05 → Prague :29, wait 36: a 240-min round). The
  live map shows five buses on the line proper in the afternoon (1124, 1137, 1140, 1141, 1145) and 1120 on the Nový Knín
  shuttles; 1140's day (Prague 13:05, back 15:05, out 17:05, back 19:35) is the hourly round the model runs. No `lay` needed.
- `core_to` Nový Knín on the out leg counts the 18:05 / 19:05 trips (card says so). No `notvia` needed (one path).
- The Nový Knín shuttles are not a branch: out of Dobříš 14:35, 16:40, 18:40 (:40 every 120, the 14:35 five minutes early) but back
  only 15:47 in the window (12:47 before it); one bus, 1120. Card names them. Stará Huť, Karla Čapka stays the explained coverage
  exception (one trip, 13:55).
- Card and `why`: facts checked (6 / 5 at Štěchovice, the tie, the off list, 4 buses, waits 36 / 30). PASS.

## EACH WAY flags, re-derived

| Line | Flag (before) | My reading at the flagged stop and where the variant leaves the trunk | Verdict | Designer | Result |
|---|---|---|---|---|---|
| 502 | 6 / 8 at Československé armády | One path. Every 10 until 16:13, every 15 after: the every-15 trips fall between the five every-10 slots (my repeating-minute search finds them at :07 / :37 and :28 / :58, three each way after 16:00: the phase change, not a branch). Modelled at the 14:00–16:00 peak as the method says; card says so. | B | B | PASS |
| 395 | 6 / 7 at Březové Hory | The Prague 11:55–15:35 trips that run 3 min past Drkolnov to Březové Hory and the 12:35–15:31 trips that start there: the 395 pattern itself; the only stop off the game leg is Březové Hory (on 503, 505, 508, 521). The 16:00 window's slot trips end at Drkolnov (the 393 ones from 17:15 at Březové Hory; Drkolnov still the majority), so the town end is right. Designer's card sentence verified. | B | B | PASS |
| 360 | 5 / 6 at Smíchovské nádraží | At Davle, obec: 11 out 13:15–18:45 (:15 and :45), 6 back (13:42, 14:32, 15:17, 16:17, 17:12, 18:12). The :15 departures from Prague (14:15–18:15, five at one minute) have no return at a repeating minute: the off back trips are the tail of the morning :45 pattern (Sedlčany 11:45, 12:45), the 13:35, and 14:20 / 15:20 which are the hourly :15 row 5 min late. Plates (`360_observed`): 7228 360 14:45 → 549 16:15; 7229 360 13:45 → 450 15:15 → 551 17:15 → 549 18:10 → 552 18:45; 7503 360 15:45 → 450 17:30; 7506 360 16:45 → 450 18:15. The card's new sentence is right. Outstation; no empty return (rule). | D | D | PASS |
| 505 | 4 / 5 at Orlov, kaplička | One bus, 65-min rounds. My search finds a coincidental repeat (13:46, 17:41, 18:44 and 13:35, 17:35, 18:40 within ±3) with nothing in the three hours between: every 60 at those minutes would leave 14:43–16:43 empty (fails the 80 %). No allowed interval holds 65. v1 review already moved it from every 72 to every 120. | B | B | PASS |
| 501 | 3 / 6 at Žižkova (now 6 / 7 at pod Kaňkou after the audit fix) | At pod Kaňkou 12 out, 12 back 13:00–19:00; off the every-120 three-slot row and 501 Bytíz: out 13:35, 14:05 (Bytíz), 16:45, 17:45 (Bytíz), 18:05, 18:40 (to Jiráskovy sady); back Dubno 13:35, 14:00, 14:37 (Bytíz), 17:10, 18:12 (Bytíz), 18:45. Minutes :35 / :05 / :45 / :45 / :05 / :40 and :35 / :00 / :37 / :10 / :12 / :45: no three at one minute. The prison round runs 3 times each way (Šachetní 14:05, 15:25, 17:45; Bytíz 14:37, 16:02, 18:12) 80–140 min apart: a destination variant, already its own line (501 Bytíz, every 480 on the 15:25 / 16:02 round); no interval of the list holds the three. Card lacked Šachetní 18:40, Dubno 14:00 and 18:45 in its off list. | C | C | **FIX** (card: off list completed) |
| 392 | 3 / 4 at Voznice, polesí | Off the three Simutrans lines: Prague 14:05, 15:05, 18:05 → Dobříš (:05 three times, but 16:05 and 17:05 do not exist), 17:25, 18:25; Dobříš 14:46, 18:10, 18:50 back (no shared minute). The Prague – Dobříš shorts as a whole (7 out, 6 back) are already `392 Dobříš` (:45 out, 15:46 / 16:58 back every 120, exact in the window). Designer's correction (17:46 is the 15:46 slot two hours on) verified. | C | C | PASS |
| 454 | 3 / 4 at Nedrahovice, Úklid | Through Nedrahovice village towards Sedlčany: Tábor 12:45, 13:45, 14:50 (at Úklid 13:54, 14:59, 15:59) and the 454 Sedlec-Prčice 16:40 (16:59); via Lipský mlýn: 16:45 and 18:45 only. Towards Tábor every trip runs through the village (14:31, 15:31, 16:31 on the slot, 18:31). So the village road is the regular path and Lipský mlýn the variant (2 trips a day, one in the window). The game line goes out via Lipský mlýn because that is the 16:45 window slot trip's road (the v1 review's fix, the owner's 1 Nov rule "the row follows its slot trip") and it keeps Nedrahovice, Lipský mlýn served; the village stops are served on the way back. The designer named both roads on the card as the 329 precedent asks. A judgement, left as it is; the alternative (out through the village, Lipský mlýn a coverage exception or a 480 line) is noted below for the coordinator. | C (path variant named) | C | PASS |
| 472 | 3 / 4 at Třebsko | Off: 13:49 (Třebsko → Příbram, the 567 bus going on), Březnice 14:00 and 14:55 → Příbram; Příbram 14:00 → Březnice, 14:45 and 15:40 → Uzenice, Jiráskovy sady 17:19. Minutes :49 / :18 / :13 and :18 / :03 / :02 / :43: two within 5 min each way, never three. Already an approximate row on owner_checks. | C | C | PASS |
| 511 | 3 / 4 at Tochovice, železniční stanice | Off: Příbram 12:35 → Březnice (13:07), Tochovice 13:20 → Chraštice (13:22), 17:30 → Březnice (17:32); Březnice 12:45 (13:08), Chraštice 13:54 → Příbram (14:08), Březnice 17:05 → Tochovice (17:28), Chraštice 18:02 → Tochovice (18:16; bus 9618 from the 478 17:25). Only 13:08 / 14:08 share a minute. | C | C | PASS |
| 495 | 3 / 3 at Březnice | Off: Počaply 14:05 → Březnice (14:11), Mirovice 16:00 (16:14), Březnice 17:35 → Rožmitál; Nepomuk 15:55 → Březnice (16:20), Rožmitál 16:10 → Březnice (16:21), Březnice 17:45 → Mirovice. Six single trips, no shared minute; four Simutrans lines already, one per road. Designer's addition (Počaply 14:05) verified. | C | C | PASS |
| 509 | 3 / 3 at Litavka | One bus, rounds of 85 and 100 min (15:38, 17:18, 18:38 out; 14:08, 17:13, 18:33 back at Litavka). No interval holds 85 / 100. | C | C | PASS |
| 520 | 3 / 3 at Svaté Pole, u kostela | Off: Vestec 13:31 (13:53), Daleké Dušníky 14:22 (14:28), Vestec 18:05 (18:29); Dobříš 12:55 (13:01), 14:05 → Daleké Dušníky (14:11), 15:55 (16:01). 13:01 / 16:01 share a minute, no third. One bus. Designer's correction (18:45 is the 14:45 slot four hours on) verified. | C | C | PASS |

## ONE WAY flags and the "going home" claims, checked by the passing reading and the plates

| Line | Claim on the card | Evidence | Result |
|---|---|---|---|
| 393 | the six :30 / :45 trips ending at Jiráskovy sady go on as 472 (:30) and 521 (:45); "or to the garage" removed | `393_observed`: 9875 15:36 393 → 16:39 472; 9862 15:57 → 16:54 521; 9872 16:41 → 17:21 472; 9860 16:49 → 17:45 521; 9880 17:35 → 18:31 472; 9874 17:44 → 18:41 521. All six. | PASS |
| 521 | even-hour :06 trips off; "the 16:06 bus goes on as 495 and the 14:06 bus comes back as the 15:38"; 8 out against 5 back at Březové Hory | 14:06 = 9557, 15:38 = 9557; 16:06 = 9558 → 495 18:10. Read at Rožmitál towards Příbram there are 8 trips (13:12 and 14:28 from Věšín, 13:48, 15:08, 15:38, 16:08, 17:08 from Věšín 16:55, 18:08) against 11 out: an every-60 :06 / :08 alternative would hit no more trips than the every-120 two-slot pair plus 521 Věšín (9 slots for 8 back trips). The Jiráskovy sady flag (4 one way) is the starts one stop before the modelled `fr`, on the slots from Březové Hory. | PASS |
| 478 | Příbram – Mirovice trips are buses going home (at Kozárovice 4 towards Mirovice, 1 back); they go on as 495 and the Chraštice shuttle | Kozárovice reading agrees (13:01, 13:41, 15:31, 17:21 against 16:12). 9609 14:45 → Chraštice shuttle 16:00 / 16:15; 9567 18:25 → 495 19:23; 9618 17:25 → Chraštice → 511 18:02; 9557 16:35 ends at Mirovice. | PASS |
| 360 | see above | plates above | PASS |
| 319 | 104319 trips are commuter trips back to Prague (Příbram 14:01, 15:06, 16:00; Dobříš 13:03), none out | 9921 14:02 → 393 17:08; 9873 15:06 → 392 17:31; 9871 16:22 → 395 18:21; 7916 (a 317 bus) 13:03. | PASS |
| 754 | none back; the buses stay in Sedlčany, 7206 goes on as the Sestrouň shuttle and 516 | 7206 13:27 754 → 15:15 / 15:22 754 Sestrouň → 15:29 / 15:55 516. | PASS |
| 500 | Horní Hbity trips go on as 510 | 7223 17:52 500 → 18:20 510; 7221 12:08 500 → 12:31 510. | PASS |
| 551 | Krásná Hora 16:55 → Kamýk goes on as 552 | 7501 16:55 551 → 17:10 552. | PASS |
| 549 / 450 | the 450 bus runs the 549 Petrovice – Kuní trip | 7505: 450 13:15, 14:00, 14:50, 549 15:30 / 15:35, 450 15:40 / 15:46. | PASS |
| 522 | "the buses sleep at Hvožďany **or go on there as 524 to Březnice (16:43 → 16:45)**"; off trips "buses going home or on as 524" | `522_observed` / `524_observed`: 9612 runs 14:35, 15:07, 16:05 and is not seen again after Hvožďany; 9832 runs 17:35 and is not seen again. The 524 16:45 Hvožďany → Březnice is 9567, the 524's own bus (out 15:30). The timetable chain is not run through. | **FIX** (card) |
| 524 | "The afternoon is one bus … Hvožďany 16:45 → Březnice (**the 522 bus going on**, the chains at Hvožďany)" | Three buses shared the five trips (9459 14:40 / 15:05, 9567 15:30 / 16:45, 9615 17:10); the 16:45 is 9567. The every-480 one-bus sequence is a Step 8 construction and stays; the claim about real buses is corrected. | **FIX** (card) |
| 567 | "Rožmitál 13:35 and 15:30 → Třebsko (**the bus goes on as 472 there**)" | 9832: 13:35 567 → 13:49 472 Třebsko → Příbram (true); 15:30 567 → waits at Třebsko → 17:11 567 back to Rožmitál (not 472). | **FIX** (card) |
| sheet `notes` | "Seen in the timetable, for the 2 Nov live map: … 522 buses go on as 524 at Hvožďany; … 567 goes on as 472 at Třebsko" | as above: 500 → 510 and 551 → 552 confirmed, 567 → 472 on the 13:35 only, 522 → 524 not run. | **FIX** (notes) |
| 407, 471, 514, 515, 450, 506, 507, 519 | sparse or one-bus lines, lists on the cards | my scan: ≤ 2 off trips one way at any shared minute; lists match the trips | PASS |
| 508 | after the loop fix of the audit: 1 / 4 at Šachetní (13:00, 14:00 :00 trips; 13:40, 14:38, 15:40 extras) | the card names them; 503 and 525 are no longer flagged | PASS |
| 428, 416, 420 | far-end lines, "the buses sleep in Vimperk / Prachatice" | two trips a day each way, lists match | PASS |

## Sheet-wide scan (my own), what else turned up
- Repeating-minute hits with ≥ 3 each way: 360 (the :15 extras against the morning :45 tail — outstation, above), 395 (the
  Březové Hory extension), 454 (the village road, above), 502 (the every-15 phase), 505 (the coincidence above). No other line.
- Trip ends not at a modelled terminal, ≥ 3 in 12:00–19:00: 393 Jiráskovy sady (6) and Březové Hory (5), 395 Březové Hory
  (9 starts, 5 ends), 472 Jiráskovy sady starts (3), 501 Nová Hospoda Polní (3 each way, the shorts the model runs on to Dubno),
  521 Jiráskovy sady starts (4), 361 Nový Knín (4). All explained on the cards.
- The v1 method check still says "outstation at the inbound rate" for 361 and "buses going home" for 360; not in this task's scope.

## Changes I made (`lines.json`, card text only; no model, slot or bus change)
1. **522** note: "sleep at Hvožďany or go on there as 524 (16:43 → 16:45)" → sleep at Hvožďany (9612 after the 16:05, 9832 after
   the 17:35; the 524 16:45 is the 524's own bus 9567); "buses going home or on as 524" → "buses going home".
2. **524** note: "The afternoon is one bus" → the trips chain into one bus's sequence; "the 522 bus going on" → the bus that
   went out at 15:30; the 2 Nov buses named (9459, 9567, 9615).
3. **567** note: the 13:35's bus goes on as 472 13:49; the 15:30's waits at Třebsko and comes back as the 17:11.
4. **501** note: off list completed with Šachetní 18:40 (to Jiráskovy sady), Dubno 14:00 and 18:45; the three prison rounds
   80–140 min apart named as the reason for every 480.
5. Sheet **notes**: the chain list is now "Checked on the 2 Nov live map" with the result per chain (500 → 510 and 551 → 552
   confirmed with plates; 567 → 472 on the 13:35 only; 522 → 524 not run through), the timetable-only items kept apart.

## For the coordinator (not changed)
- **454:** the regular road out of Tábor in the afternoon is through Nedrahovice village (12:45, 13:45, 14:50 and every trip
  back); the game line goes out via Lipský mlýn because that is the 16:00 window's slot trip and it keeps Nedrahovice,
  Lipský mlýn served (its only afternoon trips are the 16:45 and 18:45). Routing the out leg through the village would need
  Nedrahovice, Lipský mlýn as a coverage exception (a mill stop; the village's other stops are served) or a 454 Lipský mlýn
  line every 480 on the 16:45 (+1 bus). The owner approved this shape on 329 once the card named the road; the card now does.
- **361:** the owner check is the only real choice on this sheet from the re-check (4 buses hourly vs 2 buses every 120).

## Audits after `run_oblast.py pribramsko` (rerun by me after the edits; run identical to the designer's)
Step 4: 181 timed legs, 178 ok, 3 FEWER (360 Smíchovské nádraží → Sedlčany: the :15 extras; 393 / 395 Drkolnov → Smíchovské
nádraží: the shared 12-minute return), as before. Branch audit: 14 legs read at a midpoint, `[SLOT-BRANCH]` 472 and 521 (Jiráskovy
sady starts, explained in the v1 method check); 361 ok. Path audit: the same 6 flags (454 Sedlec-Prčice twice, 506, 520, 521, 523),
all explained in the lines' `why`. Passing audit (fixed for loop legs): 12 EACH WAY, 16 ONE WAY; 503 and 525 gone, 508 down to 1 / 4,
501 now read at pod Kaňkou (above), 361 ONE WAY at Dobříš, železniční stanice (the shuttles and the uneven trips back). Coverage:
unchanged (Stará Huť, Karla Čapka; Bohutín, Vysoká Pec, sídliště; Nečín, Žebrák; Mladý Smolivec, Starý Smolivec, I explained;
four Hradištko stops of okres Praha-západ for the `--final` pass).

## Summary
| Line | Verdict | Change | Buses |
|---|---|---|---|
| 361 | E (designer's change verified) | none beyond the designer's | 4 → 4 (v1: 2) |
| 502, 395, 360, 505, 392, 454, 472, 511, 495, 509, 520 | B / D / C | none | unchanged |
| 501 | C | **FIX** card: off list + Šachetní 18:40, Dubno 14:00, 18:45 | 3 → 3 |
| 522 | D | **FIX** card: no 524 through-run, buses sleep at Hvožďany (plates) | 1 → 1 |
| 524 | — | **FIX** card: 16:45 is the 524's own bus 9567; three buses shared the trips | 1 → 1 |
| 567 | — | **FIX** card: only the 13:35 goes on as 472 | 1 → 1 |
| sheet notes | — | **FIX**: chain list with the live-map result per chain | — |
| 393, 521, 478, 319, 754, 500, 551, 360 claims | verified by plates | none | unchanged |
| all other flags | B / C / D / E | none | unchanged |

Oblast total: 81 Simutrans lines, **129 → 129** buses (v1: 127).
