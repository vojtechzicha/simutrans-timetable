> Superseded where `branch-review-2026-11-03.md` differs: 522, 524, 567, 501 (card text). The review stands.

# Branch re-check, PID Příbramsko, 3 Nov 2026

Re-check for the systemic error the owner found on 381 Zásmuky (short workings and branches filed as "off the pattern" or
"buses going home" because trips were grouped by start and end stop). Work queue: the passing audit of 3 Nov
(`../../audit-passing-2026-11-03-before.txt`): 13 EACH WAY flags (502, 395, 361, 360, 505, 501, 392, 454, 472, 511, 495,
509, 520) and 17 ONE WAY flags (407, 471, 521, 514, 515, 508, 478, 450, 500, 506, 507, 519, 754, 393, 503, 319, 525).

**Method.** Each flagged line was read at the stops its trips pass (`data/derived/trips.json`, `reading/<L>.txt`), not by
where they start and end: every trip of the line passing the flagged stop and the stop where a variant leaves the trunk,
13:00–19:00, both directions, with its time at that stop, marked by whether a modelled slot of the line meets it within 3 min
(`*` below = none does). Then three scans over the whole sheet: (1) the afternoon trips of every line grouped by their two
ends, (2) for every modelled leg the trips it carries that end short of or start after the leg's ends, (3) a repeating
minute (period 60, 120, 180 or 240 min, tolerance ±3 and ±6 min) among the off-pattern trips at every stop of every line,
plus (4) every timed leg's real trips in 13:00–19:00 against its slots in the same six hours (a line modelled at half its real
rate). Plates are from the 2 Nov live map.

**Result: no missed branch (no verdict A) in this oblast.** One line was modelled at half its real rate on a wrong "outstation"
reason and is changed (361: every 120 → every 60, 2 → 4 buses); ten cards are corrected or completed where a claim or an off-pattern list
was wrong or missing (360, 392, 393, 395, 454, 478, 495, 520, 521, 319). Everything else is left alone.

## The change: 361 Praha – Štěchovice – Nový Knín – Dobříš (EACH WAY, 5 each way, 7 one way at Stará Huť, železniční zastávka) → E

Why it was flagged. The line was modelled every 120 (Smíchovské nádraží 16:05, Dobříš 16:15) as an "outstation line, timed at
the inbound rate of its 16:00 window". Read at Štěchovice, 13:00–19:00 (every 361 trip passes it):
- towards Dobříš: 13:42, 14:42, 15:42, 16:42, 17:42, 18:42 (the Prague :05 trips: hourly, exact);
- towards Prague: 13:15, 14:55, 15:55, 17:05, 18:35 (Dobříš 12:25, 14:05, 15:05, 16:15, 17:45: about hourly, uneven minutes).

6 out against 5 back is not "far fewer" (verdict D needs that). The buses do sleep at the far end (the first trips of the day
start at Nový Knín and Dobříš), but in the afternoon those from Dobříš turn and come back about hourly, so the inbound rate is
hourly in the 14:00–16:00 window; v1 took the half rate from the single trip from Dobříš (16:15) in the 15:30–17:30 band of the
16:00 anchor. The plates show the buses turning at Dobříš and coming back (1140: Praha 13:05, back 15:05, out 17:05, back 19:35; 1137: out 14:05, back 16:15, out 18:05;
1141: back 12:25, out 15:05, back 17:45). So the "off the pattern" Prague departures 13:05, 15:05, 17:05, 19:05 are half of an
hourly service, not buses going home. The other off-pattern trips are the Dobříš – Nový Knín shuttles (Dobříš 13:55 to Stará
Huť, Karla Čapka, 14:35, 16:40, 18:40; Nový Knín 12:47, 15:47): 4 out and 2 back. Out of Dobříš the 14:35 / 16:40 / 18:40 do
repeat a minute (:40 every 120, the 14:35 five minutes early), so that direction alone would pass a one-way test, but the way
back has only two trips (Nový Knín 12:47, 15:47, not 120 apart), so the branch test (≥ 3 each way) fails; one bus (1120) with
40–108 min between its trips. Left as listed.

Change (`lines.json`, `361`):
- `anchor` "14:30" (window 14:00–16:00). 14:00–16:00 and 15:00–17:00 tie at 6 departures; the default picks 15:00–17:00 and its
  fit band 15:30–17:30. 14:00–16:00 holds the hourly pairs: Smíchovské nádraží 14:05, 15:05 and Dobříš 14:05, 15:05, all
  exact. Hand-set anchors for the same reason exist on 551 (this sheet: "the 13:00–15:00 and 15:00–17:00 stretches tie") and 398 (Nymbursko).
- Simutrans line `361`: every **60**, Smíchovské nádraží → Dobříš, náměstí at :05 (core_to Nový Knín as before, so the 18:05 and
  19:05 trips to Nový Knín are on it), Dobříš, náměstí → Smíchovské nádraží at :05. Typed value 4 on both legs (real :05, loop
  terminus −1).
- Step 4 (window 14:00–16:00): out leg slots 14:05, 15:05 against real 14:05, 15:05, exact 2/2, 11 of its 14 trips of the day
  exact; back leg slots 14:05, 15:05 against real 14:05, 15:05, exact 2/2; over the day only 2 of 11 trips from Dobříš are
  exact (12:25, 16:15, 17:45, 19:35 and the mornings are uneven), listed on the card as off the pattern. 4 buses (waits 36 at
  Smíchovské nádraží, 30 at Dobříš); the 2 Nov live map shows five buses on the line proper.
- Owner check added (the slower option): every 120 at the 16:00 window, 2 buses, half of the Prague departures off the pattern.
- Note and `why` rewritten (no "outstation" claim; says why the anchor is by hand).

**In-game change list for 361 (if the owner built it from v1):** Smíchovské nádraží → Dobříš: every 120, typed 64 (real 16:05) →
every 60, typed 4 (real :05); Dobříš → Smíchovské nádraží: every 120, typed 74 (real 16:15) → every 60, typed 4 (real :05);
buses 2 → 4. Nothing else on the sheet changes.

## EACH WAY flags left as they are

Times at the flagged stop, 13:00–19:00 (`*` = off every slot). "+" and "−" are the two directions named per line.

### 502 Svatá Hora – Zdaboř – Žežice – Brod (6 each way, 8 one way at Příbram, Československé armády) → B
- Žežice / komerční zóna → Svatá Hora: 13:04, 13:12, 13:27*, 13:42, 13:52 … every 10 to 15:52, then 16:07*, 16:22, 16:37*, 16:52, 17:07*, 17:22, 17:37*, 17:52, 18:07*, 18:22, 18:37*, 18:52
- Svatá Hora → komerční zóna: every 10 to 16:13, then 16:28*, 16:43, 16:58*, 17:13, 17:28*, 17:43, 17:58*, 18:13, 18:28*, 18:43, 18:58*

One path, no variant: the frequency drops from every 10 to every 15 at about 16:00; the model stands for the 14:00–16:00 peak
(every 10: five trunk slots and the Žežice slot an hour) and the every-15 trips fall between its slots. The card says it
("then every 15 to 19:05 … the every-15 departures after 16:00 that fall between the slots"). The Žežice trips after 16:00
(Svatá Hora 17:20, 18:35; Žežice 16:30 short, 17:50) follow the same every-15 grid. No change.

### 395 Praha – Dobříš – Příbram (6 each way, 7 one way at Příbram, Březové Hory) → B (card sentence added)
- towards Březové Hory: 13:07*, 13:47*, 14:07*, 15:07*, 15:27*, 16:47* (the :15 / :35 / :55 Prague departures 11:55–15:35 that run 3 min beyond Drkolnov)
- from Březové Hory: 13:07*, 13:19*, 13:31*, 14:21*, 14:51*, 15:11*, 15:31* (pass Drkolnov 3 min later)

Only the stop Březové Hory itself is off the game leg (it ends at Drkolnov); every other stop of these trips is covered. The stop
is on 503, 505, 508 and 521. Same pattern, no branch. Card: sentence added saying so. Also checked: the 393 / 395 return pairing
(:00 :24 :48 and :12 :36) is unchanged.

### 360 Praha – Štěchovice – Sedlčany (5 each way, 6 one way at Praha, Smíchovské nádraží) → D (card claim made exact)
- Davle, obec: towards Sedlčany 13:15, 14:15, 14:45*, 15:15, 15:45*, 16:15, 16:45*, 17:15, 17:45*, 18:15, 18:45* (11); towards Prague 13:42*, 14:32*, 15:17*, 16:17*, 17:12, 18:12 (6)
- Smíchovské nádraží: out 13:45, 14:15*, 14:45, 15:15*, 15:45, 16:15*, 16:45, 17:15*, 17:45, 18:15*, 18:55*; in 13:11*, 14:11*, 15:01*, 15:46*, 16:46*, 17:41, 18:41

Prague sends two an hour (:15 and :45), Sedlčany one: the other direction really has far fewer trips, counted at a stop in
the middle of the line. The card's "buses going home" is now the plate evidence: the extra buses carry on from Sedlčany as the local
lines (7228: 360 14:45, 549 16:15; 7229: 360 13:45, 450 15:15, 551 17:15, 552 18:45; 7503, 7506: 360, then 450 17:30 / 18:15).
Also corrected: "Sedlčany 13:35, 14:20, 15:20 (5–10 min off)" is 20, 5 and 5 min off the :15 slot. No model change.

### 505 Orlov – Kozičín (4 each way, 5 one way at Příbram, Orlov, kaplička) → B
Orlov → Kozičín 13:46*, 14:51*, 15:56, 17:41*, 18:44*; Kozičín → Orlov 13:35*, 14:45*, 15:50*, 17:35*, 18:40*. One bus, 65-min
rounds (Orlov 13:45, 14:50, 15:55; Kozičín 14:15, 15:20, 16:25), on one path. Every 60 would need a second bus and fails
Step 4 (only 15:55 would be within 3 min); no allowed interval holds 65. The 17:24 short and 18:43 loop to K Podlesí are
single trips. Card names all. No change.

### 501 Šachetní – Dubno, Bytíz (3 each way, 6 one way at Příbram, Žižkova) → C
Šachetní → Dubno 13:21, 13:51*, 14:21*, 14:51, 15:21, 15:41, 16:11, 17:01*, 17:21, 18:01*, 18:21*; Dubno → Šachetní 13:05,
13:40*, 14:05*, 14:35*, 14:45, 15:05, 15:35, 16:10, 16:30, 17:15, 17:35, 18:20, 18:50. Every 30 until 15:05, then 15:25 (Bytíz),
15:55 (Polní short), 16:45, 17:05 (short), 17:45 (Bytíz), 18:05, 18:40: no repeating minute. The Bytíz round runs 3 times each
way (Šachetní 14:05, 15:25, 17:45; Bytíz 14:37, 16:02, 18:12) but the gaps are 80 / 140 and 85 / 130 min, not a pattern; the
15:25 / 16:02 round is already the line 501 Bytíz. Card names all. No change.

### 392 Praha – Dobříš – Příbram (3 each way, 4 one way at Voznice, polesí) → C (card list corrected)
Smíchovské nádraží → Dobříš direction: 13:14, 14:34*, 14:54, 15:34*, 15:54, 16:14, 16:54, 17:14, 17:54, 18:14, 18:34*, 18:54; back:
14:54*, 15:40, 15:54, 16:46, 17:06, 17:42, 17:54, 18:18*, 18:42, 18:58*. The Prague – Dobříš short trips (14:05, 15:05, 15:45,
16:45, 17:25, 18:05, 18:25; Dobříš 14:46, 15:46, 16:58, 17:46, 18:10, 18:50) are already the line `392 Dobříš` (hourly :45 out,
15:46 / 16:58 back every 120). The rest has no minute: :05 three times (14:05, 15:05, 18:05, but not 16:05 or 17:05), :25 twice,
and the way back has no repeating minute. Correction: the card listed Dobříš 17:46 as off the pattern; it is the 15:46 slot two
hours on. No model change.

### 454 Sedlčany – Sedlec-Prčice – Tábor (3 each way, 4 one way at Nedrahovice, Úklid) → C (card sentence corrected)
Tábor → Sedlčany 13:54*, 14:59*, 15:59*, 16:59*; Sedlčany → Tábor 14:31*, 15:31*, 16:26, 18:31*. The line is hourly until about
15:20 (Tábor 12:45, 13:45, 14:50; Sedlčany 14:20, 15:20, 16:15) and every 2 h after (Tábor 16:45, 18:45; Sedlčany 18:20); 16:59* is
the Sedlec-Prčice short 16:40 (its own line). Path variant: the Tábor trips 12:45, 13:45 and 14:50 and every trip from Sedlčany
run through Nedrahovice village, the 16:45 and 18:45 via Lipský mlýn (the game line goes out via Lipský mlýn, back through the
village); the village path has 3 trips in the window out and 4 back, but out they fall at :45 / :45 / :50 and the model's
slot is 16:45: not a second regular line, and the Nedrahovice stops are served on the way back. Card: "Tábor 13:45 and 14:50
(5 min)" corrected (13:45 is an hour off the slot) and the two roads named. No model change.

### 472 Příbram – Březnice – Uzenice – Blatná – Strakonice (3 each way, 4 one way at Třebsko) → C
Příbram → Březnice 13:17, 14:18*, 15:03*, 16:02*, 16:43, 17:17, 17:43*, 18:43; back 13:23, 13:49*, 14:18*, 15:13*, 15:58, 16:43, 17:23.
About hourly at uneven minutes (the model's two slots per 120 are an hourly rate). Beyond Březnice: Příbram → Uzenice 14:45, 15:40,
→ Blatná 16:55, 18:19 (four out), Uzenice 15:40 → Březnice, Strakonice 14:25 → Příbram, Blatná 19:35 (two or three back, none at a
repeating minute): listed on the card, stops on 472 Strakonice. Card names all. No change.

### 511 Příbram – Tochovice – Březnice (3 each way, 4 one way at Tochovice, železniční stanice) → C
Příbram → Březnice 13:07*, 13:22*, 15:09, 16:47, 17:32*; back 13:08*, 14:08*, 15:38, 16:36, 17:28*, 18:16*. The starred trips are the
Tochovice – Chraštice – Březnice local trips (13:20, 13:54, 17:05, 17:30, 18:02) and the 12:35 / 12:45 through trips; no repeating
minute. Card lists them. No change.

### 495 Rožmitál – Březnice – Nepomuk – Mirovice (3 each way, 3 one way at Březnice, autobusové stanoviště) → C (card list completed)
Towards Rožmitál 13:40, 14:11*, 14:29, 14:50, 15:35, 16:14*, 17:35*; the other way (towards Mirovice, or from Rožmitál) 13:55, 14:50, 15:30,
16:20*, 16:21*, 17:45*, 18:21. Already four Simutrans lines, one per road. The starred trips are single trips at unlike minutes (Počaply 14:05 → Březnice,
Mirovice 16:00, Březnice 17:35 and 17:45, Rožmitál 16:10, Nepomuk 15:55 beyond Rožmitál). Card: Počaply 14:05 → Březnice added to
the off list. No model change.

### 509 Trhové Dušníky – Láz (3 each way, 3 one way at Trhové Dušníky, Litavka) → C
One bus, uneven rounds of 85–100 min (Trhové Dušníky 14:12, 15:37, 17:17; Láz 14:58, 16:42, 17:58): 14:13 / 15:38* / 17:18* / 18:38* and
14:08* / 15:33 / 17:13* / 18:33*. No allowed interval holds 85 and 100. Card says so. No change.

### 520 Dobříš – Nečín – Hřiměždice, Vestec (3 each way, 3 one way at Svaté Pole, u kostela) → C (card list corrected)
Vestec → Dobříš 13:53*, 14:28*, 15:47, 18:29*; Dobříš → Vestec 13:01*, 14:11*, 14:51, 16:01*, 16:51, 18:51. One bus, irregular rounds
(Dobříš 12:55, 14:05 short, 14:45, 15:55, 18:45). Correction: the card listed Dobříš 18:45 as off the pattern; it is the 14:45 slot
four hours on. No model change.

## ONE WAY flags

| Line | Flag | Reading | Verdict |
|---|---|---|---|
| 407 | 2 / 4 at Praha | long line, 3–4 trips a day each way (Praha 13:00, 14:00, 15:10, 15:35, 17:35; Písek 15:00, 18:00; Prachatice 11:50); card says Prachatice two a day each way, the rest listed | C, no change |
| 471 | 2 / 4 at Solenice | one bus shuttle; Příbram 15:15, 16:55, 18:55; Solenice 12:30, 16:00, 17:50; Klučenice 105-min rounds; card lists all | C, no change |
| 521 | 2 / 4 at Jiráskovy sady | the four starred trips are the :34 trips that start at Jiráskovy sady, one stop before the modelled start (393 buses going on; already explained by the v1 branch audit note). Read at Březové Hory, Rožmitálská: 11 trips out against 8 back. Out of Příbram to Rožmitál 13:06, 14:06, 14:34, 15:06, 16:06, 16:34, 17:06, 18:34 (8) against 13:48, 15:08, 15:38, 16:08, 18:08 back (5); the model carries 15:06 / 16:36 and 15:38 / 16:08. | D (card corrected) |
| 514 | 2 / 3 at Svaté Pole | one bus, rounds of 95–100 min (Dobříš 15:00, 16:35, 18:15; Županovice 13:30, 15:40, 17:20; Dobříš 13:40 short); card names all | B, no change |
| 515 | 2 / 3 at Nečín | one bus; Příbram 14:40 (Čelina), 16:00, 17:40 (Vestec); Čelina 13:53, Vestec 16:50; card names all | C, no change |
| 508 | 1 / 8 at Šachetní | **scan artefact**: a circle (leg from Svatá Hora to Svatá Hora, same name at both ends), see below. Real: hourly :10 exact 15:10–18:10; off: :00 trips 13:00, 14:00, extras 13:40, 14:38, 15:40, all named on the card | E, no change |
| 503 | 0 / 6 at Školní kruhový objezd | same artefact. Real: hourly :50 exact 14:50–17:50; off: 13:20, 14:20, 15:20; card names them | E, no change |
| 525 | 0 / 5 at Nový Knín, mlýn | same artefact. Real: 13:05, 14:05, 15:05, 16:00, 17:05 (Libčice only), 18:10; card names 14:05, 18:10 | E, no change |
| 478 | 1 / 6 at Zbenice | outstation: read at Kozárovice 13:00–19:00 four trips run towards Mirovice (13:41, 15:31, 17:21 and the 12:15 through trip at 13:01) and one back (the 15:15 from Písek, 16:12). Plates: 9603 (12:55 → 495 14:15), 9567 (18:25 → 495 19:23), 9609 (14:45 → Chraštice shuttle 16:00 / 16:15). Card claim stands, now says where the buses go | D, card sentence added |
| 450 | 1 / 3 at Nechvalice | Sedlčany – Petrovice shuttles on two paths and the through trips, all single at unlike minutes; card lists them | C, no change |
| 500 | 1 / 3 at Krásná Hora | through trips every 3 h (Příbram 13:45, 16:50, 19:00; Petrovice 12:00, 15:50), the shorts named on the card (the 17:50 goes on as 510: plate 7223) | C, no change |
| 506 | 1 / 3 at Žižkova | hourly at :20 / :25 / :10 as the card says; 14:05, 15:20, 18:05 listed | B, no change |
| 507 | 1 / 3 at Žežická | six single trips of a sparse town line, card lists all | C, no change |
| 519 | 1 / 3 at Votice | hourly both ways; Votice :10 exact, Sedlčany 13:20, 14:00, 15:05 then :15 exact; card lists the three | B, no change |
| 754 | 1 / 3 at Višňová | Příbram → Sedlčany 13:20, 14:30, 18:25 and Benešov 18:35 → Sedlčany; none back (the buses stay in Sedlčany, 7206 goes on as the Sestrouň shuttle and 516); card lists them | D, no change |
| 393 | 0 / 14 at Praha | out every 20 at :05 / :25 / :45 until 14:45 (before the modelled :00 / :15 window); the :30 / :45 trips to Jiráskovy sady 15:30–17:45 (six): all six buses go on as 472 (:30 trips) or 521 (:45 trips) at Jiráskovy sady, plates 9875, 9872, 9880 / 9862, 9860, 9874. No return in the afternoon (they are 472 / 521 trips back). Card said "or to the garage": corrected | E (card corrected) |
| 319 | 0 / 5 at Praha | the 104319 Prague – Dobříš – Příbram trips are commuter trips back to Prague in the afternoon (Příbram 14:01, 15:06, 16:00, Dobříš 13:03), none out: stops on 317 and 395. Card gave the Příbram trips; Dobříš 13:03 added | D (card sentence added) |

## Scan artefact of the passing audit: circular legs (503, 508, 525)
`passing_check.py` takes each slot's time at every stop of the leg from the leg's own trips as `time at the stop − time at fr`,
using `dict(zip(stops, times))`. On a leg that starts and ends at the same stop (a circle: Svatá Hora → Svatá Hora, Nový Knín
→ Nový Knín) the dict keeps the arrival time for that stop, so `time at fr` is the trip's end and every offset is short by the
length of the round (41 / 30 min): no real trip meets a slot, and every trip of the line is listed as off. The real
fit is exact for 503 (:50), 508 (:10 from 15:10) and near-exact for 525; the lists above are the real off-pattern trips. Script not
patched (not in scope); the coordinator may want to guard `fr == to`.

## Cards checked for "going home", "garage", "outstation", "sleep"
360 (D, plates), 361 (rewritten: not an outstation), 393 ("or to the garage" removed: all six end trips go on, plates), 407 and 428
(few trips a day from far ends, the lists match the trips: Prachatice 6:10 / 11:50 and Prague 14:00 / 15:35; Vimperk 5:35 / 8:15 and
Prague 13:35 / 14:50), 478 (D), 500, 520 Kamýk, 522 (out of Rožmitál 14:35, 16:05, 17:35, back only 15:07: D, the 16:43 → 16:45
chain as 524 is the Hvožďany plate 9567), 551, 567, 521 (rewritten, see the table).

## Summary

| Line | Verdict | Change | Buses before → after |
|---|---|---|---|
| 502 | B | none | 7 → 7 |
| 395 | B | card sentence (Březové Hory) | 9 → 9 |
| **361** | **E** | **every 120 → every 60, :05 / :05, anchor 14:30; card, why, owner check** | **2 → 4** |
| 360 | D | card: plate evidence for the extra buses, off minutes | 3 → 3 |
| 505 | B | none | 1 → 1 |
| 501 | C | none | 3 → 3 |
| 392 | C | card: 17:46 not off | 6 → 6 |
| 454 | C | card: Tábor 13:45, the two roads | 3 → 3 |
| 472 | C | none | 4 → 4 |
| 511 | C | none | 3 → 3 |
| 495 | C | card: Počaply 14:05 | 5 → 5 |
| 509 | C | none | 1 → 1 |
| 520 | C | card: 18:45 not off | 2 → 2 |
| 407, 471, 514, 515, 450, 500, 506, 507, 519, 754 | B / C / D | none | unchanged |
| 521 | D | card: off list and "going home" claim | 3 → 3 |
| 478 | D | card: where the buses go | 2 → 2 |
| 393 | E | card: "or to the garage" removed | 6 → 6 |
| 319 | D | card: Dobříš 13:03 | 3 → 3 |
| 503, 508, 525 | E (scan artefact) | none | unchanged |

Oblast total (sum of the builder's needs, 81 Simutrans lines): **127 → 129**.

## Audits after `run_oblast.py pribramsko`
- Step 4: 181 timed legs, 178 ok, 3 FEWER, as before: 360 Smíchovské nádraží → Sedlčany (2 slots for 4 departures: the extra
  :15 buses, verdict D above) and 393 / 395 Drkolnov → Smíchovské nádraží (the shared 12-minute return pairing). 361's two legs pass.
- Branch audit: 14 legs read at a midpoint, 11 ok; `[SLOT-BRANCH]` 472 and 521 and `[BRANCH]` 521 Věšín as before (the slot trips
  16:21 / 16:36 / 15:36 start at Jiráskovy sady, one stop before the modelled start; explained in the v1 method check, "Audit
  flags"). 361 ok.
- Path audit: the same 6 flags as before (454 Sedlec-Prčice twice, 506, 520, 521, 523), all explained in the v1 method check and
  in the lines' `why`.
- Passing audit: 12 EACH WAY and 18 ONE WAY. 361 has moved from EACH WAY to ONE WAY (flagged at Dobříš, železniční stanice: the
  Nový Knín shuttles and the uneven trips back, as above); the others are the flags explained in this file.
- Coverage: unchanged (no new uncovered stop; the explained exceptions are the v1 ones).

## Could not decide
- 361: the choice of the 14:00–16:00 window over the default 15:00–17:00 is a judgement (the two tie); it is on owner_checks with
  the slower option. If the coordinator prefers the default anchor, the alternative that passes Step 4 is every 120 as in v1.
- The v1 method check (`method-check-2026-11-01.md`) still says "buses going home" for 360 and "outstation … inbound rate" for 361;
  it is not mine to edit in this task.
