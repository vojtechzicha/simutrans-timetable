# berounsko: review of the branch re-check, 3 Nov 2026

Independent of the designer's notes: every EACH WAY flag of `audit-passing-2026-11-03-before.txt` and `-now.txt`, every ONE WAY flag with 2 each way, every changed line and every "going home / sleep" claim was re-read from `data/derived/trips.json` with my own passing reader (every trip 13:00–19:00 at the stop, wherever it starts or ends), and the live-map buses were pulled with `scripts/observed.py` for 631, 649, 637, 531, 641, 394. The diff against v1 (repo mirror) is: 631 note + new Simutrans line `631 u lípy`, 649 note, 637 note, the oblast note and one owner check.

**Result: 631 u lípy PASS as designed; one card claim the designer "corrected" was right the first time (637) and is restored with the evidence; the oblast note's bus total was stale. Model unchanged otherwise. Buses 67 (designer's figure confirmed).**

## Changed lines

### 631 u lípy — PASS
- Read at Nižbor, u lípy 13:00–19:00 (my reading): the trunk passes :28 out (13:28, 14:26, 15:28, 16:28, 17:29, 18:27) and :36 back; the shorts turn there: out 13:55 (Králův Dvůr 13:25), 14:51 (Králův Dvůr 14:21), 15:51, 16:51 (Beroun 15:28, 16:28); back 13:14, 14:14, 15:09, 16:09. 4 each way, hourly, until 16:30: verdict A, as the designer found.
- Legs in `schedule.json`: out leg counts 6 trips (8:31, 12:25, 13:25, 14:21, 15:28, 16:28; the 14 Šnárová trips are kept out by `notvia`), back leg 5 trips (7:24, 13:14, 14:14, 15:09, 16:09). No Šnárová trip in either leg.
- Step 4: out window 14:30–16:30 slots 15:28, 16:28 = real, exact (day: 3 exact of 6, worst 4); back slots 15:09, 16:09 = real, exact (13:14, 14:14 are 5 later). Running times 23 / 22 as the 15:28 and 15:09 run. Knot check: the model reaches Beroun :31, the real 15:31 / 16:31.
- Terminal: Beroun, autobusové nádraží is right. The anchor trips (15:28, 16:28) start there and all four returns end there; the 13:25 and 14:21 start at Králův Dvůr, u zámku 7 min earlier (a stop 631's Všeradice leg serves), which is why they still show at Králův Dvůr in the passing audit (2 each way there, explained).
- `lay`: default (3); the slots fix the waits (57 at Beroun, 18 at u lípy), so 2 buses is the pattern's own count. At u lípy the trunk (:28 / :36) and the shorts (:51 / :09) do not coincide; together Beroun – u lípy is 2 an hour each way 13:00–17:00 as in the timetable.
- Card: note and why say the route, the minutes, the Králův Dvůr starts and the 649 through-running. OK.
- Owner check "631, 649": a real choice. The 2 Nov live map shows one bus on each afternoon round Beroun → u lípy → Žloukovice → u lípy → Beroun (9794 13:25, 9610 14:21, 9565 15:28, 9794 16:28; 9563 at 12:25), so pooling is what happens in reality (2 buses) and the rule (one line per real line) gives 3. Stays an owner check, not applied.

### 637 — FIX (card only)
The designer replaced "16:00–18:00 to Nový Jáchymov: buses going home, they sleep there" with "short workings of the hourly line, not buses going home". The passing reading says the opposite: at Nový Jáchymov 13:00–19:00 is 6 out, 5 back, but 16:00–19:00 is 3 out (16:00, 17:00, 18:00) against 1 back (Roztoky, Placanda 17:36; the Nový Jáchymov 19:00 → Králův Dvůr is after the window). Five morning trips start at Nový Jáchymov (4:37, 5:22, 5:52, 6:21, 6:57), and on the 2 Nov live map 9809 (16:00) and 9570 (17:00) ended their day there; 9594 (18:00) came back as the 19:00. So they are buses going home at an outstation; the model is unchanged (hourly both ways at the 14:00 anchor, the Nový Jáchymov trips counted at `core_to`).
- note: "…(the automatic 16:00 holds the Nový Jáchymov short workings). Read at Nový Jáchymov the evening is three trips out … so they are short workings of the hourly line, not buses going home." → "…(the automatic 16:00 holds the trips that end at Nový Jáchymov). Read at Nový Jáchymov, 13:00–19:00 is 6 trips out and 5 back, but 16:00–19:00 is 3 out (16:00, 17:00, 18:00) against 1 back (Roztoky, Placanda 17:36, a 638 bus running on): the 16:00–18:00 trips are buses going home. Nový Jáchymov is an outstation (five morning trips 4:37–6:57 start there; on the 2 Nov live map 9809 and 9570 ended their day there after the 16:00 and 17:00, and 9594 came back from the 18:00 as the 19:00 → Králův Dvůr). They stay on the :00 slots, counted at Nový Jáchymov."
- why: "the 16:00–18:00 Nový Jáchymov trips count as short workings" → "the 16:00–18:00 trips to Nový Jáchymov (buses going home) count on the :00 slots at Nový Jáchymov".
- The ONE WAY flag at Beroun, pod dálnicí (Kublov 13:08, 14:08, 16:08, Placanda 17:36) is a path stop of the back road the 15:08 (Trubská) trip does not use; those trips are on the :08 slots. E, as the designer said.

### 649, oblast note, owner check — PASS / FIX
649's note (one circuit with 631 u lípy would need 2 buses instead of 3) is right. The oblast note still said "per-line totals (65 buses)": → 67.

## EACH WAY flags (before and now files are the same six)

| line | stop | my reading 13:00–19:00 | verdict | result |
|---|---|---|---|---|
| 531 | Příbram, Archiv | out to Archiv 12:47→13:52, 13:25→14:22, 13:57→15:02, 14:35→15:32, 14:57→16:02; back from Archiv 13:51, 14:21, 14:51, 15:21 (→ Jince), 15:51, 16:51. At the bus station the :57 slots both ways are on the pattern (15:57 and 16:57 out end at the station; 15:51 and 16:51 back start at Archiv) | E: a terminal question, not a branch; the Archiv end runs 13:00–17:00 and the station end after; the four stops beyond are Příbram town, on Příbramsko lines. Extending 531 to Archiv would cost no bus (71 + 43 + 64 + 2 = 180) but moves the end into Příbramsko's stops; left as designed | PASS |
| 641 | Zdice, škola | out via Trubín – Svatá 13:26, 14:28, 14:33, 16:26, 18:26 (four at :26–:28); back via škola – Černín – Levín 13:23, 14:33, 15:53, 17:53 (:23 :33 :53 :53); nothing comes back by the Trubín road | C: the Trubín road is one-way, the back road irregular; 13:00 / 14:02 sit on the knot slots Zdice :28, the 14:07 / 16:00 / 18:00 end at Zdice, škola and run on as 640 (16:28, 18:28 on 640's :30); Trubín, Svatá on 638, škola / Černín / Levín on 384, 394 | PASS |
| 643 | Podluhy, Na drahách | arrive 13:05, 14:05, 14:45, 15:45, 16:40, 17:45; depart 13:05, 14:10, 15:45, 16:40, 17:45 (0-minute turns); the 15:14 / 17:14 Třenice trips and 16:35 / 16:40 are the every-120 round the model holds, the rest are the 5-minute spur to Hořovice and the Křešín round | E | PASS |
| 394 | Zdice / Králův Dvůr | out of Nové Butovice 20 (Zdice :00 / :30 + :15 / :45 extras 14:15, 15:15, 17:20, 17:45 + Počaply shorts 14:40, 15:45, 16:15, 16:45, 17:10, 18:15), back 12 (Zdice :03 / :33 + Králův Dvůr 15:30) | D: the Počaply shorts have one return; timed both ways at the inbound every 30 | PASS |
| 526 | Hředle | out 13:33, 14:38, 15:18, 16:38, 17:23, 18:55; back 13:11, 15:03, 16:03, 17:24, 18:56 | C: no three at one minute back; Hředle is on the circuit's Žebrák → Zdice leg | PASS |
| 529 | Hvozdec | 13:15, 15:05, 17:00, 18:50 out, +7 back | B: every 120 at 17:00, 15:05 five off, 13:15 and 18:50 15 / 10 off; same bus either way | PASS |

## ONE WAY flags with 2 each way
- 637: see above (FIX, card only).
- 640: 13:08, 14:43, 16:28, 18:28 start at Zdice, škola one stop before Zdice, náměstí; 16:28 / 18:28 pass náměstí 16:30 / 18:30 on the :30 slot, 14:43 and 13:08 are off and named. E. PASS.
- 825: at Loděnice the Mořina road back is 13:14, 16:28, 18:49 (+ Loděnice 14:49), out 13:07 (Mořinka), 14:39, 16:39, 18:14: no repeating minute beyond the modelled 16:39 / 16:28 every 120. C. PASS.
- The 1-each-way flags (380 Vypich alias, 384 Tlustice 12:00 / 13:34 / 15:55 / 17:50 / 18:00, 633 Tetín 3 out 2 back, 527, 548, 636 Chyňava 2 each way, 861 loop artefact) have no repeating minute each way; the cards name them. PASS.

## Other "going home / sleep" claims
394 (buses sleep at Zdice and Králův Dvůr; 20 out, 12 back at Králův Dvůr, u zámku): right. 637: corrected back, see above. No other such claim on this sheet.

## Audits after the rerun (`run_oblast.py berounsko`)
- Step 4: 87 timed legs, 87 ok.
- Branch audit: 19 legs; the same flags as v1 (380 one Počaply end, 384 / 384 Hořovice the 17:20 Počaply short), all on the cards; 631 and 637 legs [ok].
- Path audit: 6 slots, all named on the cards (384 17:20, 531 Křešín, 631 Málkov spur, 641 Trubín and Levín roads, 825 Prof. Veselého).
- Passing audit: 6 EACH WAY, 10 ONE WAY, each with a verdict above. Uncovered: only the Příbram town stops of 531 (Příbramsko).

## Summary
| line | result | change |
|---|---|---|
| 631 u lípy | PASS | none (2 buses, as designed) |
| 637 | FIX | note and why: the 16:00–18:00 Nový Jáchymov trips are buses going home (outstation), with the morning starts and the 2 Nov plates; model unchanged |
| oblast note | FIX | "(65 buses)" → "(67 buses)" |
| 531, 641, 643, 394, 526, 529, 640, 825, 649 and the 1-each-way flags | PASS | none |

**berounsko: 67 buses, 41 Simutrans lines** (v1: 65, 40).
