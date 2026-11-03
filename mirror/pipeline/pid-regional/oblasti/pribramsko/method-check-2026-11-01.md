> 3 Nov 2026: re-checked for branches read by trip ends instead of where trips pass (the 381 Zásmuky case). Where `branch-check-2026-11-03.md` or `branch-review-2026-11-03.md` differs from this file, the 3 Nov files stand (the review over the check).

# Method check: PID Příbramsko (okres Příbram with Dobříš and Sedlčany, prefixes 300 / 305), 1–2 Nov 2026

Designed line by line with `../../DESIGN_BRIEF.md` (including "Learned on the pilot") and the bus schedule method v4
(`../../../bus-schedule-method.md`), then corrected on 2 Nov after the independent review (`review-2026-11-01.md`: 50 PASS,
10 FIX, 1 ASK; every FIX row applied as the review details it, see "Changed on 2 Nov"). The design is `lines.json` in this
folder; `python -X utf8 pid-regional/scripts/run_oblast.py pribramsko` rebuilds `data/derived/schedule.json` and the
three audits.

- **Data:** PID GTFS of 1 Nov 2026, service day Mon 2 Nov 2026 (school day): `data/derived/trips.json` and the whole-day
  readings `data/derived/reading/<L>.txt` (every trip at its core points, the paths, the 0-minute chain test). The live
  map was being polled while this was designed; its morning plates already show every 393 trip on a 395 course (the
  393 / 395 pairing below). The other through-running in `notes` waits for the afternoon plates; no decision rests on it.
- **Step 4**, per leg: in the Simutrans line's model window (anchor −30 … +90, or a window set by hand where stated) the
  slots equal the real departures ±1, and ≥ 80 % of the slots have a real departure within 3 min; then most departures
  exact over the day (5–23), then within 1, then the simplest; on one-departure-per-window lines the real 13–18 h headway
  decides (Opavsko rule 2), and where the exact counts tie the rate decides (Step 11: 551, 522). Every two-terminal line
  was searched both ways together with a scratch helper (every interval dividing 1440 up to 480, 1–8 slots on the
  window's real departures, the same count both ways, need by `slot_need`), then set by hand; one-bus sequences of
  several trips became circuits on the shortest period that holds them.
- **Typed values** are (real − 61) mod every: every terminus is a loop. The builder writes them; the per-line sections
  below give the real minutes and the typed values side by side.
- **Running times** were checked leg by leg against the slot trips' own times: set by hand where the median mixed paths
  (522 out 27, 450 Skoupý out 32, 450 Milevsko 50, 454 towards Sedlčany 83, 496 out 37, 506 Zavržice back 45, 509 out 43,
  551 42 / 53). The review's item 6 also lists 407 back 160, 416 out 145, 420 out 130, 478 out 99, 509 back 36 and 520
  out 40 on PASS lines; they change no bus count and no typed value and were not applied (the instruction for the fixes
  was to leave PASS lines alone); the whys of 509 and 520 name both times.
- **Result:** 61 lines: 58 modelled as **81 Simutrans lines, 127 buses**; 513 and 565 not modelled (Step 8: 513's
  afternoon trips are legs of 559; 565 has one afternoon trip, over 500's and 501's stops); 961 is the night line
  (automatic). `run_oblast.py` runs clean. Step 4 audit: 181 timed legs, 178 ok, 3 FEWER (360 out of Prague:
  outstation; 393 and 395 back from Drkolnov: the Step 5b split of one set of departures between two Simutrans lines),
  0 EMPTY. Branch audit: 14 legs read at a midpoint, 11 ok, 3 flags explained below. Path audit: 6 flags, explained
  below. Coverage: 909 afternoon stops, 901 on this sheet, 4 coverage exceptions (the one owner check), 4 stops of okres
  Praha-západ (Hradištko, 437's real start only; on 338 and 488) left to the final cross-sheet pass.

## Changed on 2 Nov (after the review)

- **393:** owner check deleted (a real line with 25 peak departures is not optional); notes and why: the morning plates
  of 2 Nov already show every 393 trip on a 395 course. Values unchanged (typed 14 / 59 out, 11 / 35 back), 6 buses.
- **450:** the Skoupý out leg `rt` 34 → 32 (the 14:50's own time); the Kuní wording corrected (the 14:50 arrives 15:22
  and the Kuní hop leaves 15:30; the real 0-minute chain is Kuní 15:40 → the Obděnice shuttle, one bus either way in the
  game). **450 Milevsko** now starts at Dobříš on the real through trip: Dobříš 15:25 → Milevsko (88 min), Milevsko 17:20
  → Sedlčany, Sedlčany 18:15 → Milevsko (rt 50), Milevsko 20:40 → Dobříš (the real 4:40 in the 8-hour repeat); typed 384
  / 19 / 74 / 219, still 1 bus, four real trips; it now serves Přeborov, rozcestí 0.5 and Borotice, Dražetice, rozcestí and
  Borotice, Čelina, rozcestí, so those two exceptions are gone.
- **454:** the leg towards Sedlčany follows its slot trip, the 16:45, via Nedrahovice, Lipský mlýn (`stops_via`, rt 83;
  Nedrahovice village stays on the leg towards Tábor); the Lipský mlýn exception is gone. Note corrected: Sedlčany 15:20
  is 55 min from the slot, not 5. 454 Sedlec-Prčice kept: it is the only afternoon service of seven stops (the review
  closed my open question). Typed values unchanged (104 / 74; 14 / 99).
- **496 Koupě:** the 17:05 → Koupě and 17:20 back added to the same every-240 circuit (typed 4 / 19), same 1 bus; six
  legs, all real.
- **505:** every 72 (approximate, failed Step 4 at its 17:07 slot) → every 120, Orlov 15:55 / Kozičín 16:25, exact,
  typed 54 / 84, same 1 bus; owner check deleted.
- **511:** every 120 → every 240 with both afternoon rounds: Příbram 14:35, 16:15 (typed 94, 194), Březnice 15:05, 16:10
  (124, 189), same 2 buses; the way back keeps the Chraštice path (Svojšice, Kletice and Svojšice, rozcestí).
- **515:** modelled (was Step 8): every 120, Příbram 16:00 → Hřiměždice, Vestec, Vestec 16:50 → Příbram (typed 59 / 109),
  1 bus; anchor 16:00 set by hand (the busiest stretch is the Čelina trips). The Čelina trips are listed; Nečín, Žebrák
  stays a coverage exception on them. +1 Simutrans line, +1 bus.
- **522:** every 160 → every 180 (Rožmitál 14:35, 17:35 exact; Hvožďany 15:07), typed 94 / 126, same 1 bus.
- **524:** the five afternoon trips as one bus every 480 in six legs: Březnice 14:40 → Leletice, 15:05 → Březnice, 15:30
  → Hvožďany via Volenice, Bubovice, Zliv (`lay` 0), 16:45 → Březnice, 17:10 → Leletice, Leletice 20:41 → Březnice (the
  real 4:41 in the repeat); typed 339 / 364 / 389 / 464 / 9 / 220, 1 bus; the Zliv exception is gone.
- **551:** every 240 → every 120 (typed unchanged 14 / 69), same 1 bus; the window set by hand to 13:00–15:00 (anchor
  13:30), the line's one full round of the afternoon, because the 16:10 repeat has no trip (the real 16:55 from Krásná
  Hora goes to Kamýk). 15:20 is 5 min from the 15:15 repeat.
- **472 (ASK):** design unchanged (3 buses); the cheaper row is now an owner check (below).
- **Coverage owner check** rewritten for the four remaining stops with their costs (3 buses to serve all).
- **Wording only:** 520 (the game line runs via Svaté Pole and Daleké Dušníky, Druhlice; back via Obory and Nečín,
  Jablonce), 437 (out via Korkyně and Čím, back via Slapy and Buš), 509 (out via II.poliklinika, Školní kruhový objezd and
  Zdaboř, nemocnice, back via Karla Pobudy and Kladenská), 516 (out via Solopysky, rozcestí and Chramosty, back via
  Břekova Lhota), 508 (12:00, 13:00, 14:00 are its hourly :00 trips, not extras), 486 (it meets 754 at Osečany in the
  morning), the 395, 521 and 754 notes trimmed to card text (the reasoning is here), and the notes name 508 → 501 at
  Šachetní and 503 ↔ 502 at Svatá Hora as the MHD Příbram rotation (pooling option, live-map item).

## Script problems and process notes

- `run_oblast.py` had a raw newline inside an f-string (line 40, "unterminated f-string literal") from about 05:20 on 2 Nov;
  for the first runs I used a corrected copy in my scratchpad; the coordinator fixed the script and every later run used
  the real script.
- The scratchpad is shared by all designers: at 05:43 another designer's helper ran my `assemble.py` by mistake and
  rewrote this `lines.json` from my fragments of that moment. I moved my helpers into `scratchpad/pribramsko/`, reassembled
  and checked that `lines.json` equals my fragments (no foreign line, no lost change).
- Cosmetic: `run_oblast.py`'s "no slot in the window" line prints the first slot of the period (for example "slots 7:16
  stand for 15:16" for a 15:16 slot on every 480) and pairs it with the nearest trip of the whole day (496: "5:00 stand for
  5:00", the 4:57 morning trip). The whys name the afternoon trip each such slot stands for.
- The builder's running time is the median of the leg's own trips, which mixes paths on lines with variants; see the
  hand-set `rt` above.
- The path audit compares each slot's trip with a path chosen from the leg's other trips, so a leg whose slot trip is the
  path minority is not flagged (454's leg towards Sedlčany, found by the review): worth a line in the audit's notes for the
  other oblasti.

## Decisions that shape the sheet

- **393 + 395 (Step 5b).** 393 is a peak-direction express: 18 trips into Prague 4:25–7:50, 25 out 13:05–20:25, none back
  in the afternoon. At Příbram, Drkolnov 395 sends 5 an hour towards Prague (every 12, 16:12–18:00) and brings 3; 393
  brings 2 (its :00 / :15 trips; the :30 / :45 end at Jiráskovy sady and go on as 472 and 521) and sends none. So 393 is a
  circuit out on 393 at :00 / :15, back on 395 at :12 / :36 (6 buses), and 395 keeps every 20 out and :00 / :24 / :48
  back (9 buses); both back legs show FEWER in the audit because they share one set of 395 departures (9 real in the
  window = 6 + 3). The morning plates of 2 Nov show every 393 trip on a 395 course. Anchor of 395 set to 16:00 so both
  are read in one window: the hand-anchor rule of the method is meant for shuttles on the line's own stops, so this is a
  stretch of it, made for the pair; at the automatic anchor 14:20 the way back runs every 10 at :16–:56 and the two lines
  bring 6 an hour to Drkolnov against 5 departures, the same split in a less regular form.
- **Outstation lines** (buses sleep at the far end, timed at the inbound rate, extra outbound departures off the pattern):
  360 (Sedlčany), 361 (Nový Knín, Dobříš), 521 (Rožmitál, Věšín), 522 (Hvožďany), 478 (Mirovice shorts), 407, 428
  (Prachatice, Vimperk: every 480 on the real pair of one bus). No empty-return line for them.
- **Circuits from one bus's real sequence** (Step 8): 319 (the buses alternate Šibence and Rymaně), 438 and 451 (every
  288), 486, 496 Koupě, 504 Hluboš, 524, 450 Milevsko, 559 (with the 513 Vrchotice trips), 450 (with the 549 Kuní trip).
  Each cross-line fold rests on the 0-minute chains in the reading (559 ↔ 513 at Sedlec-Prčice) or on the timing of one
  bus (450's Kuní hop: 1 bus either way) and saves a bus.
- **Long-distance lines** (Step 8): 407 (Prachatice), 416 (Sušice), 420 (Milevsko), 428 (Vimperk), 472 Strakonice and 478
  (Písek) every 480 on one real afternoon round each, 1 bus; their sparse variants whose stops are on them are listed (407's
  Prague – Písek trips, 428's Prague – Strakonice trips, 472's Uzenice / Blatná trips beyond Březnice).
- **Every place served** (owner, 2 Nov): a line every 480 for a stop no other line serves, also beyond the kraj: 392 Žírovy,
  500 Solenice (Drsník, Nepřejov, Větrov, with an empty return), 501 Bytíz, 502 Brod, 506 Zavržice, 507, 510, 511
  Hořejany, 520 Kamýk, 524, 530, 567, 477 Bezdědovice, 478 Chraštice, 450 Milevsko. Stops within about 1 km of a served
  stop and served by variant trips only are the four coverage exceptions (one owner check).
- **Short-turn lines** kept by Ex4: 392 Dobříš (a regular short working, 7 out and 6 back 13–19) and 454 Sedlec-Prčice (the
  only afternoon service of seven stops).
- **Anchors set by hand:** 395 (16:00, the 393 pair), 515 (16:00, the Vestec round; the busiest stretch is the Čelina
  trips), 516 (15:00, the line ends at 16:18), 520 (15:00) and 552 (14:30) and 522 (15:00), where the 16:00 window holds
  no trip one way; 551 (13:30, its one full round); 754 (16:00, its busiest stretch is the Sestrouň shuttles). Windows
  set per Simutrans line: 392 (14:30–16:30), 504 Hluboš (13:00–15:40, the round), 754 Sestrouň (13:00–15:30), 495 Nepomuk
  (15:00–17:00).

## Audit flags, explained

- **Step 4 FEWER:** 360 Smíchovské nádraží → Sedlčany (2 slots for 4 departures; the :15 departures are buses going home:
  the outstation case); 393 and 395 Drkolnov → Smíchovské nádraží (see above). No EMPTY row.
- **Branch audit:** `[SLOT-BRANCH] 472` and `521`: their 16:21 / 16:36 slots are trips that start at Příbram, Jiráskovy
  sady, one stop before autobusové nádraží (ul. Čs.armády), not at the bus-station bay: the 393 buses going on (the chains
  at Jiráskovy sady). The game bus starts from autobusové nádraží; the path is the same from the next stop. `[BRANCH] 521
  Věšín`: two of its three afternoon trips start at Jiráskovy sady for the same reason; its slot 15:36 starts at the bay.
- **Path audit (6):** 454 Sedlec-Prčice (the short trips take three paths; the game line runs out via Janov – Radeč –
  Martinice – Malkovice and back via Měšetice – Doublovičky – Mezné; 17:15 and 16:40 take the other roads, whose stops are
  on these and on 454); 506 (out trips alternate via Kaufland and via Evropská; Evropská is on the way back); 520 (the
  14:45 runs via Obořiště, Vyšehrad, Ouběnice, stops of 517 and 420); 521 (the 16:34 from Jiráskovy sady also runs via
  Sedlice, Hoděmyšl and Rožmitál, křižovatka; both stops are on the modelled lines, Hoděmyšl on 521's way back and on 521
  Věšín); 523 (the 17:10 runs via zámek Kozel; the game line goes out via Husova and Kozel, back via Žákava and Nezvěstice,
  mosty, so every stop is on it). Every flag is named in the line's why.

## Bunching at shared stops (same minute in the model, 13:00–18:00)

Smíchovské nádraží :00 (317, 393), :15 (393, 395), :45 (360, 392 Dobříš), :50 (314, 319), 16:20 (319, 416), 15:35 (395,
407), 13:35 (395, 428): all real. Sedlčany :10 and :15 pulses (556, 754 Sestrouň; 360, 450 Obděnice, 454 Sedlec-Prčice,
518, 519, 549, 552, 559): the real :15 pulse, on different roads. Model artefacts, accepted and named on the cards:
Svatá Hora 14:25 (502 and 502 Brod; every trunk minute is taken), Dobříš 16:45 (520's repeat and 520 Kamýk), Březnice
13:05 towards Příbram (472 and 511, different roads beyond Tochovice), Příbram 14:55 (471 and 472, different roads),
Rožmitál 13:40 (495 towards Březnice, 495 Nepomuk the other way).

## Stops of other Středočeský okresy served only by this sheet's lines (for the final pass)

- Praha-západ (290): Bojanovice (Malá Lečice, u Hesů, Senešnice, chaty, restaurace), Davle, Pod Račany, Sloup, Sloup, U
  Jeřábu, Hvozdnice, Hvozdnice, chaty (all on 314); Mníšek pod Brdy, u hřiště (319). Hradištko, zámek, u rybníčku,
  Rajchardov and Brunšov are on 437's real 13:55 start only (not on the modelled 437) and on 338 and 488 of Praha-západ.
- Benešov (200): Heřmaničky, Březina, Dědkov, Křenovičky (556); Křečovice, Větrov, Maršovice, Zaječí, rozcestí, Neveklov,
  Doloplazy, rozcestí, Tisem (754); Střezimíř, náměstí (454); Vojkov, Křenovice, Zahrádka and the Votice stops (519). All
  are on modelled lines here.

## Open questions

- None that the design waits for. The afternoon plates of 2 Nov will show the through-running named in `notes` (500 →
  510, 522 → 524, 551 → 552, 567 → 472, the MHD Příbram rotation); pooling is the owner's option.

## Summary

| Line | Simutrans line | Every | Slots, real minutes (per timed leg, at its terminal) | Buses |
|---|---|---|---|---|
| 314 | 314 | 60 | Praha, Smíchovské nádraží :50 | Nová Ves pod Pleší :07 | 3 |
| 317 | 317 | 30 | Praha, Smíchovské nádraží :00 / :30 | Dobříš, náměstí :03 / :33 | 5 |
| 319 | 319 | 120 | Praha, Smíchovské nádraží 12:50, 13:50, 14:50, 15:50, 16:50, 17:50, 18:50, 19:50 | Mníšek pod Brdy, železniční zastávka Rymaně 12:26, 13:38, 14:26, 15:38, 16:26, 17:38, 18:26, 19:38 | Praha, Smíchovské nádraží 12:20, 13:20, 14:20, 15:20, 16:20, 17:20, 18:20, 19:20 | Mníšek pod Brdy, u Šibence 12:13, 13:13, 14:13, 15:13, 16:13, 17:13, 18:13, 19:13 | 3 |
| 360 | 360 | 60 | Praha, Smíchovské nádraží :45 | Sedlčany, autobusové stanoviště :15 | 3 |
| 361 | 361 | 120 | Praha, Smíchovské nádraží 12:05, 14:05, 16:05, 18:05 | Dobříš, náměstí 12:15, 14:15, 16:15, 18:15 | 2 |
| 392 | 392 | 60 | Praha, Smíchovské nádraží :25 | Příbram, autobusové nádraží :46 | 3 |
| 392 | 392 Dobříš | 120 | Praha, Smíchovské nádraží 12:45, 13:45, 14:45, 15:45, 16:45, 17:45, 18:45, 19:45 | Dobříš, náměstí 12:58, 13:46, 14:58, 15:46, 16:58, 17:46, 18:58, 19:46 | 2 |
| 392 | 392 Žírovy | 480 | Příbram, autobusové nádraží 15:16 | Buková u Příbramě 15:44 | 1 |
| 393 | 393 | 60 | Praha, Smíchovské nádraží :00 / :15 | Příbram, Drkolnov :12 / :36 | 6 |
| 395 | 395 | 60 | Praha, Smíchovské nádraží :15 / :35 / :55 | Příbram, Drkolnov :00 / :24 / :48 | 9 |
| 407 | 407 | 480 | Praha, Smíchovské nádraží 15:35 | Prachatice, autobusové nádraží 19:50 | 1 |
| 416 | 416 | 480 | Sušice, nábřeží 13:00 | Praha, Smíchovské nádraží 16:20 | 1 |
| 420 | 420 | 480 | Milevsko, autobusové stanoviště 13:55 | Praha, Smíchovské nádraží 17:05 | 1 |
| 428 | 428 | 480 | Praha, Smíchovské nádraží 13:35 | Vimperk, autobusové nádraží 16:15 | 1 |
| 437 | 437 | 120 | Nový Knín 13:10, 15:10, 17:10, 19:10 | Štěchovice 12:00, 14:00, 16:00, 18:00 | 1 |
| 438 | 438 | 288 | Kovářov, Chrást 13:25, 18:13 | Milevsko, ZVVZ 14:45, 19:33 | Kovářov, Chrást 15:50 | Milevsko, autobusové stanoviště 12:17, 17:05 | 1 |
| 439 | 439 | 120 | Nový Knín 12:35, 14:35, 16:35, 18:35 | Chotilsko, Živohošť 13:20, 15:20, 17:20, 19:20 | 1 |
| 450 | 450 | 120 | Sedlčany, autobusové stanoviště 12:50, 14:50, 16:50, 18:50 | Petrovice [PB 2] 13:30, 15:30, 17:30, 19:30 | Petrovice, Kuní 13:35, 15:35, 17:35, 19:35 | Petrovice [PB 2] 13:50, 15:50, 17:50, 19:50 | 1 |
| 450 | 450 Obděnice | 120 | Sedlčany, autobusové stanoviště 13:15, 15:15, 17:15, 19:15 | Petrovice [PB 2] 12:00, 14:00, 16:00, 18:00 | 1 |
| 450 | 450 Milevsko | 480 | Dobříš, náměstí 15:25 | Milevsko, autobusové stanoviště 17:20 | Sedlčany, autobusové stanoviště 18:15 | Milevsko, autobusové stanoviště 12:40 | 1 |
| 451 | 451 | 288 | Milevsko, autobusové stanoviště 12:50, 17:38 | Klučenice 13:43, 18:31 | Milevsko, autobusové stanoviště 15:10, 19:58 | Krásná Hora nad Vltavou 16:05 | 1 |
| 454 | 454 | 120 | Tábor, autobusové nádraží 12:45, 14:45, 16:45, 18:45 | Sedlčany, autobusové stanoviště 12:15, 14:15, 16:15, 18:15 | 2 |
| 454 | 454 Sedlec-Prčice | 120 | Sedlčany, autobusové stanoviště 13:15, 15:15, 17:15, 19:15 | Sedlec-Prčice, náměstí 12:40, 14:40, 16:40, 18:40 | 1 |
| 471 | 471 | 120 | Příbram, autobusové nádraží 12:55, 14:55, 16:55, 18:55 | Solenice 12:00, 14:00, 16:00, 18:00 | 1 |
| 471 | 471 Klučenice | 120 | Solenice 12:07, 14:07, 16:07, 18:07 | Klučenice 13:15, 15:15, 17:15, 19:15 | 1 |
| 472 | 472 | 120 | Příbram, autobusové nádraží 12:21, 12:55, 14:21, 14:55, 16:21, 16:55, 18:21, 18:55 | Březnice, autobusové stanoviště 12:25, 13:05, 14:25, 15:05, 16:25, 17:05, 18:25, 19:05 | 3 |
| 472 | 472 Strakonice | 480 | Příbram, autobusové nádraží 12:00 | Strakonice, autobusové nádraží 14:25 | 1 |
| 477 | 477 | 144 | Blatná, železniční stanice 12:16, 14:40, 17:04, 19:28 | Březí [pásmo 9 2] 13:11, 15:35, 17:59 | 1 |
| 477 | 477 Bezdědovice | 480 | Blatná, Palackého 14:05 | Bezdědovice, Dobšice 14:15 | 1 |
| 478 | 478 | 480 | Příbram, autobusové nádraží 12:15 | Písek, autobusové nádraží 15:15 | 1 |
| 478 | 478 Chraštice | 480 | Mirovice, náměstí 16:00 | Chraštice 16:15 | 1 |
| 486 | 486 | 480 | Sedlčany, autobusové stanoviště 13:15 | Osečany 14:30 | Nalžovice, Chlum 15:33 | 1 |
| 495 | 495 | 120 | Březnice, autobusové stanoviště 12:50, 13:40, 14:50, 15:40, 16:50, 17:40, 18:50, 19:40 | Rožmitál pod Třemšínem, autobusové stanoviště 12:35, 13:40, 14:35, 15:40, 16:35, 17:40, 18:35, 19:40 | 2 |
| 495 | 495 Pňovice | 360 | Březnice, autobusové stanoviště 15:35 | Rožmitál pod Třemšínem, autobusové stanoviště 12:10, 18:10 | 1 |
| 495 | 495 Nepomuk | 120 | Rožmitál pod Třemšínem, autobusové stanoviště 13:40, 15:40, 17:40, 19:40 | Nepomuk, sídliště 13:55, 15:55, 17:55, 19:55 | 1 |
| 495 | 495 Mirovice | 120 | Březnice, autobusové stanoviště 13:30, 15:30, 17:30, 19:30 | Mirovice, náměstí 12:15, 14:15, 16:15, 18:15 | 1 |
| 496 | 496 | 480 | Březnice, autobusové stanoviště 13:00 | Blatná, Sádlov 14:17 | 1 |
| 496 | 496 Koupě | 240 | Březnice, autobusové stanoviště 14:40, 18:40 | Bělčice, Záhrobí 15:05, 19:05 | Březnice, autobusové stanoviště 15:40, 19:40 | Koupě 15:55, 19:55 | Březnice, autobusové stanoviště 13:05, 17:05 | Koupě 13:20, 17:20 | 1 |
| 500 | 500 | 180 | Příbram, autobusové nádraží 13:50, 16:50, 19:50 | Petrovice [PB 2] 12:50, 15:50, 18:50 | 2 |
| 500 | 500 Solenice | 480 | Příbram, autobusové nádraží 15:05 | 1 |
| 501 | 501 | 120 | Příbram, Šachetní 12:35, 13:05, 13:55, 14:35, 15:05, 15:55, 16:35, 17:05, 17:55, 18:35, 19:05, 19:55 | Dubno, učiliště 12:25, 13:00, 13:30, 14:25, 15:00, 15:30, 16:25, 17:00, 17:30, 18:25, 19:00, 19:30 | 2 |
| 501 | 501 Bytíz | 480 | Příbram, Šachetní 15:25 | Příbram, Bytíz, věznice 16:02 | 1 |
| 502 | 502 | 60 | Příbram, Svatá Hora :15 / :25 / :35 / :45 / :55 | Příbram, Zdaboř, komerční zóna :00 / :10 / :20 / :30 / :50 | 5 |
| 502 | 502 Žežice | 60 | Příbram, Svatá Hora :05 | Příbram, Žežice :35 | 1 |
| 502 | 502 Brod | 480 | Příbram, Svatá Hora 14:25 | Příbram, Brod, obec 14:55 | 1 |
| 503 | 503 | 60 | Příbram, Svatá Hora :50 | 1 |
| 504 | 504 | 120 | Příbram, autobusové nádraží 12:01, 14:01, 16:01, 18:01 | Sádek 12:31, 14:31, 16:31, 18:31 | 1 |
| 504 | 504 Hluboš | 240 | Příbram, autobusové nádraží 13:01, 17:01 | Bratkovice, Dominikální Paseky 13:31, 17:31 | Příbram, autobusové nádraží 15:01, 19:01 | Hluboš 15:35, 19:35 | 1 |
| 505 | 505 | 120 | Příbram, Orlov 13:55, 15:55, 17:55, 19:55 | Příbram, Kozičín 12:25, 14:25, 16:25, 18:25 | 1 |
| 506 | 506 | 120 | Příbram, Svatá Hora areál 12:20, 13:25, 14:20, 15:25, 16:20, 17:25, 18:20, 19:25 | Příbram, Zdaboř, Červená 12:10, 13:10, 14:10, 15:10, 16:10, 17:10, 18:10, 19:10 | 2 |
| 506 | 506 Zavržice | 480 | Příbram, Svatá Hora areál 13:05 | Příbram, Zavržice 14:03 | 1 |
| 507 | 507 | 480 | Příbram, Zdaboř, Žežická 15:08 | Lhota u Příbramě, točna 15:45 | 1 |
| 508 | 508 | 60 | Příbram, Svatá Hora :10 | 1 |
| 509 | 509 | 120 | Trhové Dušníky 12:12, 14:12, 16:12, 18:12 | Láz, Horní 12:58, 14:58, 16:58, 18:58 | 1 |
| 510 | 510 | 480 | Příbram, autobusové nádraží 14:45 | Smolotely 15:40 | 1 |
| 511 | 511 | 240 | Příbram, autobusové nádraží 12:15, 14:35, 16:15, 18:35 | Březnice, autobusové stanoviště 12:10, 15:05, 16:10, 19:05 | 2 |
| 511 | 511 Hořejany | 480 | Tochovice, ObÚ 13:10 | Tochovice, Hořejany 13:15 | 1 |
| 512 | 512 | 120 | Příbram, autobusové nádraží 12:31, 14:31, 16:31, 18:31 | Obecnice 13:00, 15:00, 17:00, 19:00 | 1 |
| 514 | 514 | 120 | Dobříš, náměstí 12:35, 14:35, 16:35, 18:35 | Županovice 13:20, 15:20, 17:20, 19:20 | 1 |
| 515 | 515 | 120 | Příbram, autobusové nádraží 12:00, 14:00, 16:00, 18:00 | Hřiměždice, Vestec 12:50, 14:50, 16:50, 18:50 | 1 |
| 516 | 516 | 120 | Sedlčany, autobusové stanoviště 13:25, 15:25, 17:25, 19:25 | Dublovice, Zvírotice 13:55, 15:55, 17:55, 19:55 | 1 |
| 517 | 517 | 60 | Dobříš, náměstí :55 | Příbram, autobusové nádraží :49 | 2 |
| 518 | 518 | 90 | Sedlčany, autobusové stanoviště 12:15, 13:45, 15:15, 16:45, 18:15, 19:45 | Křečovice, Hořetice 12:53, 14:23, 15:53, 17:23, 18:53 | 1 |
| 519 | 519 | 60 | Votice, autobusové stanoviště :10 | Sedlčany, autobusové stanoviště :15 | 2 |
| 520 | 520 | 120 | Dobříš, náměstí 12:45, 14:45, 16:45, 18:45 | Hřiměždice, Vestec 13:25, 15:25, 17:25, 19:25 | 1 |
| 520 | 520 Kamýk | 480 | Dobříš, náměstí 16:45 | Kamýk nad Vltavou, u Mášů 14:24 | 1 |
| 521 | 521 | 120 | Příbram, autobusové nádraží 12:36, 13:06, 14:36, 15:06, 16:36, 17:06, 18:36, 19:06 | Rožmitál pod Třemšínem, autobusové stanoviště 12:08, 13:38, 14:08, 15:38, 16:08, 17:38, 18:08, 19:38 | 2 |
| 521 | 521 Věšín | 120 | Příbram, autobusové nádraží 13:36, 15:36, 17:36, 19:36 | Věšín, Buková 12:55, 14:55, 16:55, 18:55 | 1 |
| 522 | 522 | 180 | Rožmitál pod Třemšínem, autobusové stanoviště 14:35, 17:35 | Hvožďany 12:07, 15:07, 18:07 | 1 |
| 523 | 523 | 120 | Plzeň, Terminál Hlavní nádraží 13:27, 15:27, 17:27, 19:27 | Rožmitál pod Třemšínem, autobusové stanoviště 13:10, 15:10, 17:10, 19:10 | 2 |
| 524 | 524 | 480 | Březnice, autobusové stanoviště 14:40 | Hvožďany, Leletice 15:05 | Březnice, autobusové stanoviště 15:30 | Hvožďany 16:45 | Březnice, autobusové stanoviště 17:10 | Hvožďany, Leletice 12:41 | 1 |
| 525 | 525 | 120 | Nový Knín 12:00, 13:05, 14:00, 15:05, 16:00, 17:05, 18:00, 19:05 | 1 |
| 530 | 530 | 480 | Příbram, autobusové nádraží 14:50 | Kamýk nad Vltavou, u školky 15:45 | 1 |
| 549 | 549 | 180 | Sedlčany, autobusové stanoviště 12:15, 15:15, 18:15 | Klučenice 13:05, 16:05, 19:05 | 1 |
| 551 | 551 | 120 | Sedlčany, autobusové stanoviště 13:15, 15:15, 17:15, 19:15 | Krásná Hora nad Vltavou 12:10, 14:10, 16:10, 18:10 | 1 |
| 552 | 552 | 120 | Sedlčany, autobusové stanoviště 13:15, 15:15, 17:15, 19:15 | Kamýk nad Vltavou 12:35, 14:35, 16:35, 18:35 | 1 |
| 556 | 556 | 120 | Sedlčany, autobusové stanoviště 13:10, 15:10, 17:10, 19:10 | Sedlec-Prčice, náměstí 13:55, 15:55, 17:55, 19:55 | 1 |
| 559 | 559 | 480 | Sedlčany, autobusové stanoviště 15:15 | Sedlec-Prčice, náměstí 16:00 | Sedlec-Prčice, Vrchotice, Na Františku 16:10 | Sedlec-Prčice, náměstí 16:20 | 1 |
| 567 | 567 | 480 | Příbram, Jiráskovy sady 14:36 | Rožmitál pod Třemšínem, autobusové stanoviště 15:30 | 1 |
| 754 | 754 | 60 | Příbram, autobusové nádraží :25 | Benešov, Terminál :35 | 4 |
| 754 | 754 Sestrouň | 120 | Sedlčany, autobusové stanoviště 13:10, 15:10, 17:10, 19:10 | Sedlčany, Sestrouň 13:18, 15:18, 17:18, 19:18 | 1 |
| 513 | not modelled |  |  | 0 |
| 565 | not modelled |  |  | 0 |
| **Total** | **81 Simutrans lines** | | | **127** |

Bus counts are the builder's need from each pattern (Step 10), one Simutrans line at a time. Real buses swap between these
lines at Příbram, Sedlčany, Březnice, Rožmitál and Dobříš all day (the chains named in the notes), so the per-line totals
are higher than the operators' own; pooling is an owner option, not applied.

## Owner checks (2)

1. **472**: 472 Příbram – Březnice is set every 120 with Příbram 16:21 / 16:55 (II.poliklinika 16:26 / 17:00) and Březnice 16:25 / 17:05: 7 departures exact over the day, 3 buses (the 16:55 bus waits 50 min at Březnice and 69–75 min at Příbram). *Other option:* Příbram 15:40 / 16:21 (II.poliklinika 15:45 / 16:26, typed 39 / 80), the same Březnice slots: 6 exact over the day, 2 buses (−1), both buses turn in 4–5 min at Březnice and 34–35 min at Příbram.
2. **coverage**: Four stops served 13:00–19:00 only by variant trips, each close to a stop a modelled line serves, are coverage exceptions: Stará Huť, Karla Čapka (0.50 km from Stará Huť, Knínská), Nečín, Žebrák (0.46 km from Nečín, Lipiny), Mladý Smolivec, Starý Smolivec, I (0.14 km from Starý Smolivec, II), Bohutín, Vysoká Pec, sídliště (0.33 km from Bohutín, Vysoká Pec). *Other option:* Serve them all: 3 more buses (a 361 Karla Čapka line every 480 with an empty return, 1; a 515 Čelina line every 480, 1; 522 routed via Starý Smolivec, I misses the 15:07 and needs a second bus, 1; 509 via Vysoká Pec, sídliště, a 2-minute detour its slot trips do not make, 0).

## Not modelled

- **513**: Step 8: its afternoon trips are the Sedlec-Prčice – Vrchotice, Na Františku shuttles (13:40, 16:00, back 10 min later), run by the 559 bus between its trips (the 0-minute chains at Sedlec-Prčice, 3 of 3): they are legs of Simutrans line 559. Its Sedlčany – Sedlec-Prčice trip (18:15) runs over stops of 454, 450 and 549.
- **565**: Step 8: seven trips 8:05–13:05 Jiráskovy sady – Sázky – Slivických bojovníků (one to Jesenice at 10:05); in 13:00–19:00 only the 13:05 to Slivických bojovníků, whose stops (náměstí T.G.M., Milínská, Mixova, Sázky, Slivických bojovníků) are on 500 and 501. Jesenice, Jestřabinec and Jerusalem have no trip 13:00–19:00.
- **961**: night line (automatic).

## Coverage exceptions

- **Stará Huť, Karla Čapka**: 361 only: the 13:55 Dobříš → Stará Huť, Karla Čapka trip (and 7:22 in the morning); a street stop 0.50 km from Stará Huť, Knínská (361).
- **Bohutín, Vysoká Pec, sídliště**: 509 only, on two trips (15:37, 16:42) that leave the road; 0.33 km from Bohutín, Vysoká Pec (509, 521, 567).
- **Nečín, Žebrák**: 515's Borotice, Čelina trips only (4 passings 13:00–19:00); 0.46 km from Nečín, Lipiny (520, 515). Serving it would need a 515 Čelina line every 480 (Příbram 14:40, Čelina 13:53), 1 bus.
- **Mladý Smolivec, Starý Smolivec, I**: 522 only, on the 16:05 and 19:05 out of Rožmitál (a path the game line does not take); 0.14 km from Starý Smolivec, II, on the way back of 522.

## Line by line

Each section: core points; the reading in words (the card's note); per Simutrans line its interval, need and waits, and
per leg the slots in real minutes with the typed values, running time and wait, the Step 4 result in the model window,
the day's exact / within 3 / trips counts and the trips off the pattern 12–20 h (generated from `schedule.json` after the
last run, so every number is the builder's own).

### 314 Praha,Smíchovské nádraží - Davle - Nová Ves pod Pleší

- **Core points:** Praha, Smíchovské nádraží; Davle, u pomníku; Bratřínov; Nová Ves pod Pleší. Anchor 16:00.
- **Reading:** Praha, Smíchovské nádraží – Zbraslav – Davle – Hvozdnice – Bojanovice – Bratřínov – Velká Lečice – Nová Ves pod Pleší. Hourly in the afternoon, exact: Smíchovské nádraží :50 (12:50–17:50), Nová Ves pod Pleší :07 (14:07–17:07; 12:37 and 18:17 off). Listed: the Bratřínov short trips (Davle 13:49 → Bratřínov, Smíchovské nádraží 18:50 → Bratřínov) and the morning Malá Lečice – Nová Ves shuttles; their stops are on 314.
- **314** every 60, need 3 (waits {"Praha, Smíchovské nádraží": [37], "Nová Ves pod Pleší": [10]}): Smíchovské nádraží :50 → Nová Ves pod Pleší via Davle, Hvozdnice, Bojanovice, Bratřínov and Velká Lečice (67 min); Nová Ves :07 back (66 min).
  - Smíchovské nádraží → Nová Ves pod Pleší: slots :50 (typed 49); rt 67, lay 3. Step 4: ok, window 15:30–17:30: slots 15:50 16:50; real 15:50 16:50; filled 2/2. Day (5–23) exact/within 3/trips 6/6/10; off the pattern: 19:55 (12–20 h).
  - Nová Ves pod Pleší → Smíchovské nádraží: slots :07 (typed 6); rt 66, lay 3. Step 4: ok, window 15:30–17:30: slots 16:07 17:07; real 16:07 17:07; filled 2/2. Day (5–23) exact/within 3/trips 4/4/10; off the pattern: 12:37, 18:17 (12–20 h).

### 317 Praha,Smíchovské nádraží - Mníšek pod Brdy - Dobříš

- **Core points:** Praha, Smíchovské nádraží; Mníšek pod Brdy, náměstí; Mníšek pod Brdy, u Šibence; Dobříš, náměstí. Anchor 16:00.
- **Reading:** Praha, Smíchovské nádraží – Jíloviště – Mníšek pod Brdy – Voznice – Dobříš, náměstí. Every 30 all afternoon: Smíchovské nádraží :00 / :30 (12:30–19:30; 17:00 and 18:00 end at Mníšek, u Šibence) and Dobříš :03 / :33 (11:33–18:33), exact. The 17:00 short is read at u Šibence and run on to Dobříš in the game. Half of the 317 departures from Dobříš follow a 517 arrival within 5 min (a timed connection, two operators). The Prague bus sheet may later pool 317 with 318.
- **317** every 30, need 5 (waits {"Praha, Smíchovské nádraží": [28], "Dobříš, náměstí": [8]}): Smíchovské nádraží :00 / :30 → Dobříš, náměstí via Jíloviště, Mníšek pod Brdy and Voznice; Dobříš :03 / :33 back the same way.
  - Smíchovské nádraží → náměstí: slots :00 / :30 (typed 29); rt 55, lay 3. Step 4: ok, window 15:30–17:30: slots 15:30 16:00 16:30 17:00; real 15:30 16:00 16:30 17:00; filled 4/4. Day (5–23) exact/within 3/trips 23/23/30; off the pattern: none (12–20 h).
  - náměstí → Smíchovské nádraží: slots :03 / :33 (typed 2); rt 59, lay 3. Step 4: ok, window 15:30–17:30: slots 15:33 16:03 16:33 17:03; real 15:33 16:03 16:33 17:03; filled 4/4. Day (5–23) exact/within 3/trips 23/23/24; off the pattern: none (12–20 h).

### 319 Praha,Smíchovské nádraží - Mníšek pod Brdy - Dobříš - Příbram

- **Core points:** Praha, Smíchovské nádraží; Mníšek pod Brdy, náměstí; Mníšek pod Brdy, u Šibence; Mníšek pod Brdy, železniční zastávka Rymaně; Příbram, Jiráskovy sady. Anchor 16:00.
- **Reading:** Praha, Smíchovské nádraží – Mníšek pod Brdy, two ends: u Šibence (out :20 hourly 14:20–17:20, back :13, plus 14:43) and železniční zastávka Rymaně (out :50 hourly 14:50–17:50, back 15:38, 16:26, 17:38). The buses alternate the two ends (the 0-5 minute chains at Smíchovské nádraží: 8 of 19 arrivals go straight out again as 319), so one circuit line every 120 with two slots on each leg, all exact. The Praha – Dobříš – Příbram trips of licence 104319 (out 6:18–9:36, back from Příbram 14:01, 15:06, 16:00) run over stops of 317 and 395 and are listed, as are the 18:20 / 18:50 trips to Mníšek, náměstí.
- **319** every 120, need 3 (waits {"Praha, Smíchovské nádraží (1)": [5], "Praha, Smíchovské nádraží (3)": [17], "Mníšek pod Brdy, železniční zastávka Rymaně (2)": [5], "Mníšek pod Brdy, u Šibence (4)": [25]}): Circuit Smíchovské nádraží → Mníšek, železniční zastávka Rymaně (via náměstí, u hřiště, Čisovická, Hladový vrch) → Smíchovské nádraží → Mníšek, u Šibence → Smíchovské nádraží; every 120 with 15:50 / 16:50 and 16:20 / 17:20 out, 15:38 / 16:26 and 16:13 / 17:13 back, as the buses alternate the two ends.
  - Smíchovské nádraží → železniční zastávka Rymaně: slots 12:50, 13:50, 14:50, 15:50, 16:50, 17:50, 18:50, 19:50 (typed 49, 109); rt 31, lay 3. Step 4: ok, window 15:30–17:30: slots 15:50 16:50; real 15:50 16:50; filled 2/2. Day (5–23) exact/within 3/trips 4/4/4; off the pattern: none (12–20 h).
  - železniční zastávka Rymaně → Smíchovské nádraží: slots 12:26, 13:38, 14:26, 15:38, 16:26, 17:38, 18:26, 19:38 (typed 37, 85); rt 37, lay 3. Step 4: ok, window 15:30–17:30: slots 15:38 16:26; real 15:38 16:26; filled 2/2. Day (5–23) exact/within 3/trips 3/4/8; off the pattern: none (12–20 h).
  - Smíchovské nádraží → u Šibence: slots 12:20, 13:20, 14:20, 15:20, 16:20, 17:20, 18:20, 19:20 (typed 19, 79); rt 28, lay 3. Step 4: ok, window 15:30–17:30: slots 16:20 17:20; real 16:20 17:20; filled 2/2. Day (5–23) exact/within 3/trips 4/4/5; off the pattern: none (12–20 h).
  - u Šibence → Smíchovské nádraží: slots 12:13, 13:13, 14:13, 15:13, 16:13, 17:13, 18:13, 19:13 (typed 12, 72); rt 32, lay 3. Step 4: ok, window 15:30–17:30: slots 16:13 17:13; real 16:13 17:13; filled 2/2. Day (5–23) exact/within 3/trips 3/3/5; off the pattern: 14:43 (12–20 h).

### 360 Praha,Smíchovské nádraží - Sedlčany

- **Core points:** Praha, Smíchovské nádraží; Praha, Na Plácku; Sedlčany, autobusové stanoviště. Anchor 16:00.
- **Reading:** Praha, Smíchovské nádraží – Zbraslav – Davle – Štěchovice – Nové Dvory – Chotilsko – Křepenice – Nalžovice – Sedlčany. The buses sleep at Sedlčany (4:00–7:10 seven trips into Prague). Hourly at :45 both ways 8:45–12:45; in the afternoon Prague sends every 30 (:15 / :45, 13:45–18:15) and Sedlčany hourly (13:35, 14:20, 15:20, 16:15, 17:15, 18:15). An outstation line, timed at the inbound rate: every 60, Smíchovské nádraží :45, Sedlčany :15. The :15 departures from Prague are buses going home (off the pattern), as are Sedlčany 13:35, 14:20, 15:20 (5–10 min off) and the evening trips.
- **360** every 60, need 3 (waits {"Praha, Smíchovské nádraží": [4], "Sedlčany, autobusové stanoviště": [3]}): Smíchovské nádraží :45 → Sedlčany, autobusové stanoviště by the one path via Davle, Štěchovice, Nové Dvory, Korkyně, Chotilsko and Nalžovice (87 min); Sedlčany :15 back (86 min).
  - Smíchovské nádraží → autobusové stanoviště: slots :45 (typed 44); rt 87, lay 3. Step 4: not passed as a plain row (FEWER, explained under "Audit flags"), window 15:30–17:30: slots 15:45 16:45; real 15:45 16:15 16:45 17:15; filled 2/2. Day (5–23) exact/within 3/trips 11/11/21; off the pattern: 14:15, 15:15, 16:15, 17:15, 18:15, 18:55, 19:50 (12–20 h).
  - autobusové stanoviště → Smíchovské nádraží: slots :15 (typed 14); rt 86, lay 3. Step 4: ok, window 15:30–17:30: slots 16:15 17:15; real 16:15 17:15; filled 2/2. Day (5–23) exact/within 3/trips 3/3/18; off the pattern: 12:45, 13:35, 14:20, 15:20 (12–20 h).

### 361 Praha,Smíchovské nádraží - Štěchovice - Dobříš

- **Core points:** Praha, Smíchovské nádraží; Štěchovice; Nový Knín; Dobříš, náměstí. Anchor 16:00.
- **Reading:** Praha, Smíchovské nádraží – Davle – Štěchovice – Slapy – Buš – Čím – Korkyně – Nový Knín – Mokrovraty – Stará Huť – Dobříš. Out of Prague hourly at :05 (12:05–17:05 to Dobříš; 18:05 and 19:05 end at Nový Knín); towards Prague from Dobříš only 12:25, 14:05, 15:05, 16:15, 17:45, 19:35. The buses sleep at Nový Knín and Dobříš (4:25–7:20 the first trips start there): an outstation line, timed at the inbound rate of its 16:00 window, every 120: Smíchovské nádraží 16:05 (even hours :05), Dobříš 16:15. Off the pattern: Smíchovské nádraží 13:05, 15:05, 17:05, 19:05; Dobříš 14:05, 15:05, 17:45. Listed: the Dobříš – Nový Knín shuttles (Dobříš 14:35, 16:40, 18:40; Nový Knín 12:47, 15:47); their stops are on 361.
- **361** every 120, need 2 (waits {"Praha, Smíchovské nádraží": [26], "Dobříš, náměstí": [40]}): Smíchovské nádraží 16:05 (every 2 h at even hours :05) → Dobříš, náměstí via Štěchovice, Slapy, Nový Knín and Stará Huť (90 min); Dobříš 16:15 back (84 min). The 18:05 slot is the real trip to Nový Knín, run on to Dobříš in the game.
  - Smíchovské nádraží → náměstí: slots 12:05, 14:05, 16:05, 18:05 (typed 64); rt 90, lay 3. Step 4: ok, window 15:30–17:30: slots 16:05; real 16:05 17:05; filled 1/1. Day (5–23) exact/within 3/trips 7/7/14; off the pattern: 13:05, 15:05, 17:05, 19:05 (12–20 h).
  - náměstí → Smíchovské nádraží: slots 12:15, 14:15, 16:15, 18:15 (typed 74); rt 84, lay 3. Step 4: ok, window 15:30–17:30: slots 16:15; real 16:15; filled 1/1. Day (5–23) exact/within 3/trips 1/1/11; off the pattern: 12:25, 14:05, 15:05, 17:45, 19:35 (12–20 h).

### 392 Praha,Smíchovské nádraží - Dobříš - Rosovice - Příbram

- **Core points:** Praha, Smíchovské nádraží; Dobříš, náměstí; Buková u Příbramě; Příbram, autobusové nádraží. Anchor 16:00.
- **Reading:** Praha, Smíchovské nádraží – Voznice – Dobříš – Rosovice – Buková – Pičín – Suchodol – Občov – Příbram, autobusové nádraží. Three kinds of trip: (1) through Prague – Příbram, hourly exact: Smíchovské nádraží :25 (14:25, 15:25, 16:25; 17:45 and 19:45 off), Příbram :46 (14:46–17:46); the bus that arrives at Příbram at :46 leaves again at :46 (0-minute turn as in the timetable). (2) Prague – Dobříš short trips: Smíchovské nádraží 14:05, 15:05, 15:45, 16:45, 17:25, 18:05, 18:25; Dobříš 14:46, 15:46, 16:58, 17:46, 18:10, 18:50: 392 Dobříš, every 120 with 15:45 / 16:45 out and 15:46 / 16:58 back. (3) Příbram – Buková via Pičín, Žírovy (15:16 out, 15:44 back), the only service of Pičín, Žírovy and Pičín, Revoluční: 392 Žírovy, every 480. The Příbram – Dobříš local trips (12:49, 18:27; Dobříš 13:37) are listed; their stops are on 392.
- **392** every 60, need 3 (waits {"Praha, Smíchovské nádraží": [11], "Příbram, autobusové nádraží": [0]}): Smíchovské nádraží :25 → Příbram, autobusové nádraží via Voznice, Dobříš, Rosovice, Buková, Pičín, Kotenčice, Suchodol and Občov (81 min); Příbram :46 back the same way (86 min). The bus turns at Příbram in 0 minutes as in the timetable (arrives :46, leaves :46). Model window 14:30–16:30 for this line (the line's own hourly pattern; the 16:00 window would hold 17:25, where the real trip leaves 17:45).
  - Smíchovské nádraží → autobusové nádraží: slots :25 (typed 24); rt 81, lay 3. Step 4: ok, window 14:30–16:30: slots 15:25 16:25; real 15:25 16:25; filled 2/2. Day (5–23) exact/within 3/trips 3/3/6; off the pattern: 17:45, 19:45 (12–20 h).
  - autobusové nádraží → Smíchovské nádraží: slots :46 (typed 45); rt 88, lay 0. Step 4: ok, window 14:30–16:30: slots 14:46 15:46; real 14:46 15:46; filled 2/2. Day (5–23) exact/within 3/trips 5/5/6; off the pattern: none (12–20 h).
- **392 Dobříš** every 120, need 2 (waits {"Praha, Smíchovské nádraží": [19, 7], "Dobříš, náměstí": [36, 24]}): Short trips Smíchovské nádraží 15:45 / 16:45 → Dobříš, náměstí via Voznice (37 min) and Dobříš 15:46 / 16:58 back (40 min), every 120; the other short trips (14:05, 15:05, 17:25, 18:05, 18:25 out; 14:46, 17:46, 18:10, 18:50 back) are off the pattern.
  - Smíchovské nádraží → náměstí: slots 12:45, 13:45, 14:45, 15:45, 16:45, 17:45, 18:45, 19:45 (typed 44, 104); rt 37, lay 3. Step 4: ok, window 15:30–17:30: slots 15:45 16:45; real 15:45 16:45 17:25; filled 2/2. Day (5–23) exact/within 3/trips 4/4/12; off the pattern: 14:05, 15:05, 17:25, 18:05, 18:25 (12–20 h).
  - náměstí → Smíchovské nádraží: slots 12:58, 13:46, 14:58, 15:46, 16:58, 17:46, 18:58, 19:46 (typed 45, 117); rt 40, lay 3. Step 4: ok, window 15:30–17:30: slots 15:46 16:58; real 15:46 16:58; filled 2/2. Day (5–23) exact/within 3/trips 3/3/13; off the pattern: 14:46, 18:10, 18:50 (12–20 h).
- **392 Žírovy** every 480, need 1 (waits {"Příbram, autobusové nádraží": [432], "Buková u Příbramě": [4]}): Příbram, autobusové nádraží 15:16 → Pičín, Žírovy, Revoluční → Buková u Příbramě (24 min) and Buková 15:44 → Příbram the same way (20 min), every 480: the real afternoon round, kept because Pičín, Žírovy and Pičín, Revoluční have no other line.
  - autobusové nádraží → Buková u Příbramě: slots 15:16 (typed 375); rt 24, lay 3. Step 4: no slot in the window (named in the why). Day (5–23) exact/within 3/trips 1/1/2; off the pattern: none (12–20 h).
  - Buková u Příbramě → autobusové nádraží: slots 15:44 (typed 403); rt 20, lay 3. Step 4: ok, window 15:30–17:30: slots 15:44; real 15:44; filled 1/1. Day (5–23) exact/within 3/trips 1/1/2; off the pattern: none (12–20 h).

### 393 Praha,Smíchovské nádraží - Příbram

- **Core points:** Praha, Smíchovské nádraží; Příbram, Jiráskovy sady; Příbram, Drkolnov; Příbram, Březové Hory. Anchor 16:00.
- **Reading:** Express Praha, Smíchovské nádraží – Drásov – Dubno – Příbram (no stop in Dobříš). One-directional: 18 trips into Prague 4:25–7:50, 25 out of Prague 13:05–20:25, none back in the afternoon. Out every 20 at :05 / :25 / :45 until 14:45, then every 15 to 17:45: :00 and :15 to Drkolnov (Březové Hory from 17:15), :30 and :45 to Jiráskovy sady only. The Drkolnov buses go back to Prague as 395 trips (Step 5b: at Drkolnov 395 sends 5 an hour towards Prague and brings 3, 393 brings 2 and sends none). So 393 is a circuit: out on 393 at :00 / :15, back on 395 at :12 / :36. The :30 / :45 trips that end at Jiráskovy sady are off the pattern (their buses go on as 472 and 521 or to the garage; every stop of theirs is on the circuit).
- **393** every 60, need 6 (waits {"Praha, Smíchovské nádraží": [30, 21], "Příbram, Drkolnov": [10, 19]}): Out: Smíchovské nádraží :00 / :15 → Příbram, Drkolnov by the motorway, Drásov, Dubno and Jiráskovy sady (62 min). Back: Drkolnov :12 / :36 on the 395 path through Dobříš, náměstí (78 min), the 395 departures the 393 buses run (Step 5b; the morning plates of 2 Nov show every 393 trip on a 395 course).
  - Smíchovské nádraží → Drkolnov: slots :00 / :15 (typed 14, 59); rt 62, lay 3. Step 4: ok, window 15:30–17:30: slots 16:00 16:15 17:00 17:15; real 16:00 16:15 17:00 17:15; filled 4/4. Day (5–23) exact/within 3/trips 8/8/19; off the pattern: 13:05, 13:25, 13:45, 14:05, 14:25, 14:45, 18:30, 18:45, 19:05, 19:25 (12–20 h).
  - Drkolnov → Smíchovské nádraží: slots :12 / :36 (typed 11, 35); rt 78, lay 3. Step 4: not passed as a plain row (FEWER, explained under "Audit flags"), window 15:30–17:30: slots 15:36 16:12 16:36 17:12; real 15:36 15:48 16:12 16:24 16:36 16:48 17:00 17:12 17:24; filled 4/4. Day (5–23) exact/within 3/trips 8/11/61; off the pattern: 12:00, 12:20, 12:40, 13:00, 13:24, 13:46, 13:56, 14:16, 14:26, 14:46, 14:56, 15:16, 15:26, 15:48, 16:24, 16:48, 17:00, 17:24, 17:48, 18:00, 18:20, 18:40, 19:00, 19:30 (12–20 h).

### 395 Praha,Smíchovské nádraží - Dobříš - Příbram

- **Core points:** Praha, Smíchovské nádraží; Dobříš, náměstí; Příbram, Jiráskovy sady; Příbram, Drkolnov; Příbram, Březové Hory. Anchor 16:00 (set by hand, see the reading).
- **Reading:** Praha, Smíchovské nádraží – Dobříš (through the town, náměstí) – Dubno – Příbram, Jiráskovy sady – Drkolnov, some trips 3 min on to Březové Hory. Out of Prague every 20 all day (:15 / :35 / :55). Towards Prague every 20 until 12:20, then 5 an hour (every 12, :00 :12 :24 :36 :48, from 16:12 to 18:00): two of the five are the 393 express buses going back (Simutrans line 393, :12 / :36), so 395 runs every 20 out and :00 / :24 / :48 back. Anchor 16:00, set by hand for the 393 / 395 pair.
- **395** every 60, need 9 (waits {"Praha, Smíchovské nádraží": [9, 17, 13], "Příbram, Drkolnov": [20, 24, 16]}): Smíchovské nádraží :15 / :35 / :55 → Příbram, Drkolnov via Dobříš, náměstí and Dubno; Drkolnov :00 / :24 / :48 back the same way (trips from Březové Hory are read as they pass Drkolnov). The other two returns an hour (:12 / :36) are the 393 buses.
  - Smíchovské nádraží → Drkolnov: slots :15 / :35 / :55 (typed 14, 34, 54); rt 69, lay 3. Step 4: ok, window 15:30–17:30: slots 15:35 15:55 16:15 16:35 16:55 17:15; real 15:35 15:55 16:15 16:35 16:55 17:15; filled 6/6. Day (5–23) exact/within 3/trips 49/51/54; off the pattern: none (12–20 h).
  - Drkolnov → Smíchovské nádraží: slots :00 / :24 / :48 (typed 23, 47, 59); rt 78, lay 1. Step 4: not passed as a plain row (FEWER, explained under "Audit flags"), window 15:30–17:30: slots 15:48 16:00 16:24 16:48 17:00 17:24; real 15:36 15:48 16:12 16:24 16:36 16:48 17:00 17:12 17:24; filled 5/6. Day (5–23) exact/within 3/trips 18/25/61; off the pattern: 12:20, 12:40, 13:12, 13:36, 13:56, 14:16, 14:36, 14:56, 15:16, 15:36, 16:12, 16:36, 17:12, 17:36, 18:20, 18:40, 19:30 (12–20 h).

### 407 Prachatice - Písek - Praha

- **Core points:** Praha, Smíchovské nádraží; Milín; Písek, autobusové nádraží; Prachatice, autobusové nádraží. Anchor 16:00.
- **Reading:** Praha, Smíchovské nádraží – Příbram – Milín – Mirotice – Písek (licence 371407) and on via Protivín, Vodňany, Bavorov to Prachatice (licence 370407), Jihočeský kraj. The Prachatice trips are two a day each way: Prachatice 6:10 and 11:50 to Prague, Prague 14:00 and 15:35 to Prachatice (the buses sleep in Prachatice). 407: every 480 on Prague 15:35 / Prachatice 11:50 (the real pair of one bus), the only service of Protivín, Vodňany, Bavorov, Strunkovice, Vitějovice, Žernovice, Hájek and Prachatice. The Prague – Písek trips (Prague 13:00, 17:35; Písek 15:00, 18:00 in the afternoon) run over 407's stops and are listed (Step 8), as is Prague 15:10 → Milín.
- **407** every 480, need 1 (waits {"Praha, Smíchovské nádraží": [60], "Prachatice, autobusové nádraží": [105]}): Smíchovské nádraží 15:35 → Příbram → Milín → Mirotice → Písek → Protivín → Vodňany → Bavorov → Prachatice (150 min); Prachatice 11:50 back (160 min; repeats 19:50, 3:50): one bus, every 480.
  - Smíchovské nádraží → autobusové nádraží: slots 15:35 (typed 394); rt 150, lay 3. Step 4: ok, window 15:30–17:30: slots 15:35; real 15:35; filled 1/1. Day (5–23) exact/within 3/trips 1/1/2; off the pattern: 14:00 (12–20 h).
  - autobusové nádraží → Smíchovské nádraží: slots 19:50 (typed 169); rt 165, lay 3. Step 4: no slot in the window (named in the why). Day (5–23) exact/within 3/trips 1/1/2; off the pattern: none (12–20 h).

### 416 Sušice - Blatná - Praha

- **Core points:** Sušice, nábřeží; Blatná, železniční stanice; Praha, Smíchovské nádraží. Anchor 16:00.
- **Reading:** Sušice – Horažďovice – Kadov – Blatná – Mirotice – Příbram – Praha (Plzeňský and Jihočeský kraj). Two trips each way a day; the afternoon pair is one bus: Sušice 13:00 → Smíchovské nádraží 15:25, out again 16:20 → Sušice 18:45. Every 480 on that round, 1 bus: the only service of Sušice, Rabí, Horažďovice, Kadov, Lom, Blatná, Vrbenská and the other Blatná – Sušice stops.
- **416** every 480, need 1 (waits {"Sušice, nábřeží": [135], "Praha, Smíchovské nádraží": [52]}): Sušice, nábřeží 13:00 → Horažďovice → Kadov → Blatná → Příbram → Smíchovské nádraží (145 min); Smíchovské nádraží 16:20 back (145 min): the real afternoon round, every 480.
  - nábřeží → Smíchovské nádraží: slots 13:00 (typed 239); rt 148, lay 3. Step 4: no slot in the window (named in the why). Day (5–23) exact/within 3/trips 1/1/2; off the pattern: none (12–20 h).
  - Smíchovské nádraží → nábřeží: slots 16:20 (typed 439); rt 145, lay 3. Step 4: ok, window 15:30–17:30: slots 16:20; real 16:20; filled 1/1. Day (5–23) exact/within 3/trips 1/1/2; off the pattern: none (12–20 h).

### 420 Praha,Smíchovské nádraží - Milevsko

- **Core points:** Praha, Smíchovské nádraží; Dobříš, náměstí; Kamýk nad Vltavou; Krásná Hora nad Vltavou; Milevsko, autobusové stanoviště. Anchor 16:00.
- **Reading:** Praha, Smíchovské nádraží – Dobříš – Kamýk nad Vltavou – Krásná Hora nad Vltavou – Kovářov – Hrejkovice – Milevsko (Jihočeský kraj). Two through trips each way a day: Milevsko 4:40 and 13:55 to Prague, Prague 8:25 and 17:05 to Milevsko (130 min); the afternoon pair is one bus (Milevsko 13:55 → Smíchovské nádraží 16:05, out again 17:05 → Milevsko 19:15). Bent onto every 480 at that round, 1 bus. Kept because Hrejkovice and Milevsko, škola I have no other line. Listed: the Prague – Dobříš short trips (14:45, 16:05 out; 6:10, 7:00, 8:45 in), over stops of 317 and 392.
- **420** every 480, need 1 (waits {"Milevsko, autobusové stanoviště": [160], "Praha, Smíchovské nádraží": [58]}): Milevsko, autobusové stanoviště 13:55 → Hrejkovice, Kovářov, Krásná Hora nad Vltavou, Kamýk nad Vltavou, Dobříš → Smíchovské nádraží (130 min); Smíchovské nádraží 17:05 → Milevsko the same way (130 min). The real afternoon round of one bus, every 480 (repeats 5:55 / 21:55 and 9:05 / 1:05; the real 4:40 and 8:25 are off).
  - autobusové stanoviště → Smíchovské nádraží: slots 13:55 (typed 294); rt 132, lay 3. Step 4: no slot in the window (named in the why). Day (5–23) exact/within 3/trips 1/1/1; off the pattern: none (12–20 h).
  - Smíchovské nádraží → autobusové stanoviště: slots 17:05 (typed 4); rt 130, lay 3. Step 4: ok, window 15:30–17:30: slots 17:05; real 17:05; filled 1/1. Day (5–23) exact/within 3/trips 1/1/2; off the pattern: none (12–20 h).

### 428 Vimperk - Strakonice - Praha

- **Core points:** Praha, Smíchovské nádraží; Strakonice, autobusové nádraží; Vimperk, autobusové nádraží. Anchor 14:00.
- **Reading:** Praha, Smíchovské nádraží – Příbram – Strakonice – Volyně – Čkyně – Vimperk (Jihočeský kraj). The buses sleep at Vimperk: Vimperk 5:35, 8:15 to Prague, Prague 13:35, 14:50 to Vimperk. 428: every 480 on Prague 13:35 / Vimperk 8:15 (16:15 in the repeats), 1 bus; the only service of Strakonice (Volyňská, Ellerova-Hvězda, sídliště 1.máje, PS), Malenice, Volyně, Čkyně and Vimperk. Off: Prague 14:50, Vimperk 5:35. The Prague – Strakonice trips (licence 371428; Strakonice 14:25 → Prague in the afternoon) run over 428's stops and are listed.
- **428** every 480, need 1 (waits {"Praha, Smíchovské nádraží": [185], "Vimperk, autobusové nádraží": [30]}): Smíchovské nádraží 13:35 → Příbram → Strakonice → Volyně → Čkyně → Vimperk (130 min); Vimperk 8:15 back (135 min; repeats 16:15, 0:15): one bus, every 480.
  - Smíchovské nádraží → autobusové nádraží: slots 13:35 (typed 274); rt 130, lay 3. Step 4: ok, window 13:30–15:30: slots 13:35; real 13:35 14:50; filled 1/1. Day (5–23) exact/within 3/trips 1/1/2; off the pattern: 14:50 (12–20 h).
  - autobusové nádraží → Smíchovské nádraží: slots 16:15 (typed 434); rt 135, lay 3. Step 4: no slot in the window (named in the why). Day (5–23) exact/within 3/trips 1/1/2; off the pattern: none (12–20 h).

### 437 Nový Knín - Nové Dvory - Štěchovice - Hradištko

- **Core points:** Nový Knín; Nové Dvory [PB]; Štěchovice; Hradištko, zámek. Anchor 13:40.
- **Reading:** Nový Knín – Nové Dvory – Štěchovice (– Hradištko, okres Praha-západ). Three afternoon trips by one bus: Nový Knín 13:10 → Štěchovice 13:42, Hradištko, zámek 13:55 → Štěchovice 14:00 → Nový Knín 14:39, Nový Knín 15:05 → Štěchovice (the line ends at 15:31). Every 120 at the line's window 13:10–15:10: Nový Knín 13:10, Štěchovice 14:00 (the Hradištko trip read as it passes Štěchovice), 1 bus; 15:05 is 5 min off. Nové Dvory and Nové Dvory, Krámy have no other line.
- **437** every 120, need 1 (waits {"Nový Knín": [31], "Štěchovice": [21]}): Nový Knín 13:10 → Korkyně → Čím → Korkyně, Křížov → Nové Dvory, Krámy → Nové Dvory → Slapy, Na Polesí → Štěchovice (29 min in the model; the 13:10 runs this road via Čím in 32); Štěchovice 14:00 → Slapy → Buš → Nové Dvory → Korkyně → Nový Knín (39 min; the real trip starts at Hradištko, zámek 13:55). Every 120.
  - Nový Knín → Štěchovice: slots 13:10, 15:10, 17:10, 19:10 (typed 9); rt 29, lay 3. Step 4: ok, window 13:10–15:10: slots 13:10; real 13:10 15:05; filled 1/1. Day (5–23) exact/within 3/trips 1/1/3; off the pattern: 15:05 (12–20 h).
  - Štěchovice → Nový Knín: slots 12:00, 14:00, 16:00, 18:00 (typed 59); rt 39, lay 3. Step 4: ok, window 13:10–15:10: slots 14:00; real 14:00; filled 1/1. Day (5–23) exact/within 3/trips 1/1/3; off the pattern: none (12–20 h).

### 438 Milevsko - Petrovice - Kovářov,Chrást

- **Core points:** Milevsko, autobusové stanoviště; Milevsko, ZVVZ; Kovářov, Chrást. Anchor 16:00.
- **Reading:** Milevsko – Petrovice, Kojetín – Kovářov, Chrást (Jihočeský kraj; Kojetín and Petrovice in okres Příbram). One bus all afternoon in a fixed sequence: Milevsko 12:40 → Chrást 13:23, Chrást 13:25 → Milevsko, ZVVZ 14:14, ZVVZ 14:45 → Chrást 15:43, Chrást 15:50 → Milevsko 16:30, Milevsko 17:05 → Chrást 17:48. Modelled as that one-bus circuit Chrást 13:25 → ZVVZ → Chrást 15:50 → autobusové stanoviště 17:05 → Chrást, every 288 (the shortest period that holds it), all four slots exact, 1 bus: the only service of Chrást, Zahořany, Předbořice, Řenkov and the Milevsko town stops ZVVZ, železniční stanice, Nádražní sídliště, Mírové náměstí. Off: Milevsko 12:40.
- **438** every 288, need 1 (waits {"Kovářov, Chrást (1)": [26], "Kovářov, Chrást (3)": [7], "Milevsko, ZVVZ (2)": [30], "Milevsko, autobusové stanoviště (4)": [35]}): Chrást 13:25 → Petrovice, Kojetín → Milevsko → ZVVZ (49 min); ZVVZ 14:45 → Milevsko → Chrást (58 min); Chrást 15:50 → Milevsko, autobusové stanoviště (40 min); Milevsko 17:05 → Chrást (43 min). One bus, every 288.
  - Chrást → ZVVZ: slots 13:25, 18:13 (typed 168); rt 50, lay 3. Step 4: no slot in the window (named in the why). Day (5–23) exact/within 3/trips 1/1/1; off the pattern: none (12–20 h).
  - ZVVZ → Chrást: slots 14:45, 19:33 (typed 248); rt 58, lay 3. Step 4: no slot in the window (named in the why). Day (5–23) exact/within 3/trips 1/1/2; off the pattern: none (12–20 h).
  - Chrást → autobusové stanoviště: slots 15:50 (typed 25); rt 40, lay 3. Step 4: ok, window 15:30–17:30: slots 15:50; real 15:50; filled 1/1. Day (5–23) exact/within 3/trips 1/1/4; off the pattern: 13:25 (12–20 h).
  - autobusové stanoviště → Chrást: slots 12:17, 17:05 (typed 100); rt 42, lay 3. Step 4: ok, window 15:30–17:30: slots 17:05; real 17:05; filled 1/1. Day (5–23) exact/within 3/trips 1/1/5; off the pattern: 12:40, 15:03 (12–20 h).

### 439 Nový Knín - Chotilsko

- **Core points:** Nový Knín; Chotilsko, Živohošť. Anchor 16:00.
- **Reading:** Nový Knín – Chotilsko – Lipí – Křeničná – Sejcká Lhota – Záborná Lhota – Živohošť: one bus, rounds of about 100 min (Nový Knín 13:15, 14:55, 16:35; Živohošť 13:55, 15:35, 17:20). No interval of the list holds 100 min on the minute; every 120 on the 16:35 / 17:20 round (the real round of the bus), 1 bus. Off: Nový Knín 13:15, 14:55; Živohošť 13:55, 15:35.
- **439** every 120, need 1 (waits {"Nový Knín": [46], "Chotilsko, Živohošť": [13]}): Nový Knín 16:35 → Chotilsko → Lipí → Křeničná → Živohošť (32 min); Živohošť 17:20 back (29 min). Every 120.
  - Nový Knín → Živohošť: slots 12:35, 14:35, 16:35, 18:35 (typed 94); rt 32, lay 3. Step 4: ok, window 15:30–17:30: slots 16:35; real 16:35; filled 1/1. Day (5–23) exact/within 3/trips 1/1/4; off the pattern: 13:15, 14:55 (12–20 h).
  - Živohošť → Nový Knín: slots 13:20, 15:20, 17:20, 19:20 (typed 19); rt 29, lay 3. Step 4: ok, window 15:30–17:30: slots 17:20; real 15:35 17:20; filled 1/1. Day (5–23) exact/within 3/trips 1/1/4; off the pattern: 13:55, 15:35 (12–20 h).

### 450 Dobříš - Sedlčany - Milevsko

- **Core points:** Sedlčany, autobusové stanoviště; Petrovice [PB 2]; Milevsko, autobusové stanoviště; Dobříš, náměstí. Anchor 14:30.
- **Reading:** Dobříš – Drhovy – Borotice – Sedlčany – Nechvalice – Petrovice – Kojetín – Milevsko (Jihočeský kraj). The afternoon is Sedlčany – Petrovice shuttles on two alternating paths: via Skoupý (Sedlčany 13:15, 14:50, 17:30; Petrovice 12:35, 15:50) and via Obděnice (Sedlčany 15:15; Petrovice 14:00, also via Radešice and Bratříkovice), plus the through trips Dobříš 15:25 → Milevsko, Milevsko 13:35 and 17:20 → Sedlčany and Sedlčany 18:15 → Milevsko. One Simutrans line per path: 450 (via Skoupý; in the game its bus also runs the 549 Petrovice – Kuní trip, 15:30 / 15:35, between its 15:22 arrival and the 15:50; in reality the Kuní bus goes on at 15:40 as the Obděnice shuttle and the 15:50 is another bus's, one bus either way) and 450 Obděnice, each every 120, exact; 450 Milevsko every 480 on the real Dobříš – Milevsko – Sedlčany – Milevsko – Dobříš round of one bus, the only service of Přeborov, rozcestí 0.5 and the two Borotice rozcestí stops. Listed: Milevsko 13:35, the Obděnice shuttle 15:40.
- **450** every 120, need 1 (waits {"Sedlčany, autobusové stanoviště (1)": [28], "Petrovice [PB 2] (2)": [8], "Petrovice [PB 2] (4)": [10], "Petrovice, Kuní (3)": [0]}): Sedlčany 14:50 → Nechvalice → Petrovice, Skoupý → Petrovice (32 min, set by hand to the 14:50's own time); Petrovice 15:30 → Kuní and Kuní 15:35 back (the 549 trip, run by this bus in the game; it turns at Kuní at once, as in the timetable); Petrovice 15:50 → Skoupý → Sedlčany (32 min). Every 120, 1 bus.
  - autobusové stanoviště → Petrovice [PB 2]: slots 12:50, 14:50, 16:50, 18:50 (typed 109); rt 32, lay 3. Step 4: ok, window 14:00–16:00: slots 14:50; real 14:50; filled 1/1. Day (5–23) exact/within 3/trips 1/1/4; off the pattern: 13:15, 17:30 (12–20 h).
  - Petrovice [PB 2] → Kuní: slots 13:30, 15:30, 17:30, 19:30 (typed 29); rt 5, lay 3. Step 4: ok, window 14:00–16:00: slots 15:30; real 15:30; filled 1/1. Day (5–23) exact/within 3/trips 1/1/2; off the pattern: none (12–20 h).
  - Kuní → Petrovice [PB 2]: slots 13:35, 15:35, 17:35, 19:35 (typed 34); rt 5, lay 0. Step 4: ok, window 14:00–16:00: slots 15:35; real 15:35; filled 1/1. Day (5–23) exact/within 3/trips 1/1/2; off the pattern: none (12–20 h).
  - Petrovice [PB 2] → autobusové stanoviště: slots 13:50, 15:50, 17:50, 19:50 (typed 49); rt 32, lay 3. Step 4: ok, window 14:00–16:00: slots 15:50; real 15:50; filled 1/1. Day (5–23) exact/within 3/trips 1/1/2; off the pattern: 12:35 (12–20 h).
- **450 Obděnice** every 120, need 1 (waits {"Sedlčany, autobusové stanoviště": [32], "Petrovice [PB 2]": [14]}): Sedlčany 15:15 → Nechvalice → Petrovice, Obděnice → Petrovice (31 min); Petrovice 14:00 (every 120: 16:00) → Obděnice → Radešice → Nechvalice, Bratříkovice → Sedlčany (43 min), as the 14:00 runs. Every 120, 1 bus.
  - autobusové stanoviště → Petrovice [PB 2]: slots 13:15, 15:15, 17:15, 19:15 (typed 14); rt 31, lay 3. Step 4: ok, window 14:00–16:00: slots 15:15; real 15:15; filled 1/1. Day (5–23) exact/within 3/trips 1/1/2; off the pattern: none (12–20 h).
  - Petrovice [PB 2] → autobusové stanoviště: slots 12:00, 14:00, 16:00, 18:00 (typed 59); rt 43, lay 3. Step 4: ok, window 14:00–16:00: slots 14:00; real 14:00; filled 1/1. Day (5–23) exact/within 3/trips 1/1/3; off the pattern: none (12–20 h).
- **450 Milevsko** every 480, need 1 (waits {"Dobříš, náměstí (1)": [76], "Milevsko, autobusové stanoviště (2)": [27], "Milevsko, autobusové stanoviště (4)": [95], "Sedlčany, autobusové stanoviště (3)": [14]}): One bus every 480 on the real through trips: Dobříš 15:25 → Drhovy → Borotice (Dražetice, rozcestí; Čelina, rozcestí) → Sedlčany → Petrovice → Milevsko (88 min); Milevsko 17:20 → Přeborov, rozcestí 0.5 → Petrovice → Sedlčany (41 min); Sedlčany 18:15 → Milevsko (50 min, set by hand to the 18:15's own time); Milevsko 20:40 → Sedlčany → Dobříš (89 min; the real 4:40 in the 8-hour repeat).
  - náměstí → autobusové stanoviště: slots 15:25 (typed 384); rt 88, lay 3. Step 4: ok, window 14:00–16:00: slots 15:25; real 15:25; filled 1/1. Day (5–23) exact/within 3/trips 1/1/1; off the pattern: none (12–20 h).
  - autobusové stanoviště → autobusové stanoviště: slots 17:20 (typed 19); rt 41, lay 3. Step 4: no slot in the window (named in the why). Day (5–23) exact/within 3/trips 1/1/3; off the pattern: 13:35 (12–20 h).
  - autobusové stanoviště → autobusové stanoviště: slots 18:15 (typed 74); rt 50, lay 3. Step 4: no slot in the window (named in the why). Day (5–23) exact/within 3/trips 1/1/3; off the pattern: 16:12 (12–20 h).
  - autobusové stanoviště → náměstí: slots 12:40 (typed 219); rt 89, lay 3. Step 4: no slot in the window (named in the why). Day (5–23) exact/within 3/trips 0/0/0; off the pattern: none (12–20 h).

### 451 Milevsko – Kovářov – Milešov – Krásná Hora nad Vltavou

- **Core points:** Milevsko, autobusové stanoviště; Kovářov; Klučenice; Krásná Hora nad Vltavou. Anchor 16:00.
- **Reading:** Milevsko – Hrejkovice – Kovářov – Klučenice (– Milešov – Krásná Hora nad Vltavou). One bus all afternoon: Milevsko 12:50 → Klučenice, Klučenice 13:43 → Milevsko, Milevsko 15:10 → Krásná Hora, Krásná Hora 16:05 → Milevsko, Milevsko 17:20 → Klučenice. Modelled as that circuit every 288 (the shortest period that holds the first four trips), exact on them, 1 bus: the Milevsko-side stops (Něžovice, Dmýštice, Níkovice, Pechova Lhota, Kovářov, škola) have no other line here. Off: Milevsko 17:20 (18 min from the 17:38 repeat).
- **451** every 288, need 1 (waits {"Milevsko, autobusové stanoviště (1)": [48], "Milevsko, autobusové stanoviště (3)": [55], "Klučenice (2)": [21], "Krásná Hora nad Vltavou (4)": [6]}): Milevsko 12:50 → Kovářov → Klučenice (32 min) and Klučenice 13:43 back (32 min); Milevsko 15:10 → Kovářov → Klučenice, Planá → Milešov → Krásná Hora nad Vltavou (49 min) and Krásná Hora 16:05 back (45 min). One bus, every 288.
  - autobusové stanoviště → Klučenice: slots 12:50, 17:38 (typed 133); rt 32, lay 3. Step 4: no slot in the window (named in the why). Day (5–23) exact/within 3/trips 1/1/2; off the pattern: 17:20 (12–20 h).
  - Klučenice → autobusové stanoviště: slots 13:43, 18:31 (typed 186); rt 32, lay 3. Step 4: no slot in the window (named in the why). Day (5–23) exact/within 3/trips 1/1/2; off the pattern: none (12–20 h).
  - autobusové stanoviště → Krásná Hora nad Vltavou: slots 15:10, 19:58 (typed 273); rt 49, lay 3. Step 4: no slot in the window (named in the why). Day (5–23) exact/within 3/trips 1/1/2; off the pattern: none (12–20 h).
  - Krásná Hora nad Vltavou → autobusové stanoviště: slots 16:05 (typed 40); rt 45, lay 3. Step 4: ok, window 15:30–17:30: slots 16:05; real 16:05; filled 1/1. Day (5–23) exact/within 3/trips 1/1/2; off the pattern: none (12–20 h).

### 454 Tábor - Sedlec-Prčice - Sedlčany

- **Core points:** Sedlčany, autobusové stanoviště; Sedlec-Prčice, náměstí; Střezimíř, náměstí; Tábor, autobusové nádraží. Anchor 16:00.
- **Reading:** Sedlčany – Jesenice – Sedlec-Prčice – Střezimíř – Borotín – Chotoviny – Tábor (Jihočeský kraj). Through trips: Tábor 12:45, 13:45, 14:50, 16:45, 18:45; Sedlčany 14:20, 15:20, 16:15, 18:20. Every 120 at the line's 16:00 window: Tábor :45 even hours (12:45, 16:45, 18:45 exact), Sedlčany 16:15, 2 buses; towards Sedlčany the game line runs via Nedrahovice, Lipský mlýn as the 16:45 does. Sedlčany – Sedlec-Prčice short trips run every 2 h (Sedlčany 15:15, 17:15; Sedlec-Prčice 14:40, 16:40): 454 Sedlec-Prčice, every 120, exact, the only afternoon service of Jesenice, Boudy, Martinice and Mezné, Kosova Hora, Dohnalova Lhota and Janov, Nedrahovice, Radeč and Sedlec-Prčice, Malkovice. Off: Tábor 13:45 and 14:50 (5 min); Sedlčany 14:20 and 18:20 (5 min) and 15:20 (55 min); the Střezimíř trips 13:10 / 13:15.
- **454** every 120, need 2 (waits {"Tábor, autobusové nádraží": [64], "Sedlčany, autobusové stanoviště": [7]}): Tábor, autobusové nádraží 16:45 (even hours :45) → Chotoviny → Borotín → Střezimíř → Sedlec-Prčice → Jesenice → Nedrahovice, Lipský mlýn → Sedlčany (83 min, the 16:45's own road and time, which leaves Nedrahovice village aside); Sedlčany 16:15 back through Nedrahovice village (86 min). Every 120.
  - autobusové nádraží → autobusové stanoviště: slots 12:45, 14:45, 16:45, 18:45 (typed 104); rt 83, lay 3. Step 4: ok, window 15:30–17:30: slots 16:45; real 16:45; filled 1/1. Day (5–23) exact/within 3/trips 4/4/8; off the pattern: 13:45, 14:50 (12–20 h).
  - autobusové stanoviště → autobusové nádraží: slots 12:15, 14:15, 16:15, 18:15 (typed 74); rt 86, lay 3. Step 4: ok, window 15:30–17:30: slots 16:15; real 16:15; filled 1/1. Day (5–23) exact/within 3/trips 1/1/9; off the pattern: 14:20, 15:20, 18:20 (12–20 h).
- **454 Sedlec-Prčice** every 120, need 1 (waits {"Sedlčany, autobusové stanoviště": [7], "Sedlec-Prčice, náměstí": [57]}): Sedlčany 15:15 (odd hours :15) → Jesenice → Sedlec-Prčice, náměstí (31 min); Sedlec-Prčice 16:40 (even hours :40) back (30 min). Every 120. The short trips take three paths: the game line runs out via Janov, Dohnalova Lhota, Radeč, Mezné, Martinice and Malkovice (as the 15:15) and back via Měšetice, Doublovičky, Mezné, Radeč and Janov (as the 14:40); the 17:15 (via Doublovičky) and 16:40 (via Nedrahovice, the 454 road) run over stops of these two paths and of 454.
  - autobusové stanoviště → náměstí: slots 13:15, 15:15, 17:15, 19:15 (typed 14); rt 28, lay 3. Step 4: ok, window 15:30–17:30: slots 17:15; real 17:15; filled 1/1. Day (5–23) exact/within 3/trips 3/3/3; off the pattern: none (12–20 h).
  - náměstí → autobusové stanoviště: slots 12:40, 14:40, 16:40, 18:40 (typed 99); rt 28, lay 3. Step 4: ok, window 15:30–17:30: slots 16:40; real 16:40; filled 1/1. Day (5–23) exact/within 3/trips 2/2/3; off the pattern: none (12–20 h).

### 471 Příbram - Solenice - Milevsko

- **Core points:** Příbram, autobusové nádraží; Solenice; Klučenice; Milevsko, autobusové stanoviště. Anchor 16:00.
- **Reading:** Příbram – Milín – Pečice – Cetyně – Bohostice – Solenice, beyond to Milešov and Klučenice (and one trip on to Milevsko). Příbram – Solenice is one bus shuttling (Příbram 15:15, 16:55, 18:55; Solenice 16:00, 17:50): 471, every 120 at its 16:00 window, Příbram 16:55, Solenice 16:00, exact. Solenice – Klučenice is a second bus (Solenice 16:07, 17:52; Klučenice 15:30, 17:15): 471 Klučenice, every 120, Solenice 16:07, Klučenice 17:15. Off: Příbram 15:15, Solenice 17:50, 17:52, Klučenice 15:30. Listed: Příbram 13:35 → Klučenice, 14:20 → Bohostice, Milín 15:55 → Milevsko, Klučenice 18:35 → Milešov (their stops are on 471, 451 and 549).
- **471** every 120, need 1 (waits {"Příbram, autobusové nádraží": [14], "Solenice": [24]}): Příbram, autobusové nádraží 16:55 → Brod → Milín → Pečice → Cetyně → Bohostice → Solenice (41 min); Solenice 16:00 back (41 min). Every 120, 1 bus.
  - autobusové nádraží → Solenice: slots 12:55, 14:55, 16:55, 18:55 (typed 114); rt 41, lay 3. Step 4: ok, window 15:30–17:30: slots 16:55; real 16:55; filled 1/1. Day (5–23) exact/within 3/trips 2/2/8; off the pattern: 13:35, 15:15 (12–20 h).
  - Solenice → autobusové nádraží: slots 12:00, 14:00, 16:00, 18:00 (typed 59); rt 41, lay 3. Step 4: ok, window 15:30–17:30: slots 16:00; real 16:00; filled 1/1. Day (5–23) exact/within 3/trips 1/1/7; off the pattern: 12:30, 17:50 (12–20 h).
- **471 Klučenice** every 120, need 1 (waits {"Solenice": [33], "Klučenice": [49]}): Solenice 16:07 → Milešov, Přední Chlum → Milešov → Klučenice, Kosobudy → Klučenice (19 min); Klučenice 17:15 back (19 min). Every 120, 1 bus.
  - Solenice → Klučenice: slots 12:07, 14:07, 16:07, 18:07 (typed 66); rt 19, lay 3. Step 4: ok, window 15:30–17:30: slots 16:07; real 16:07; filled 1/1. Day (5–23) exact/within 3/trips 1/1/5; off the pattern: 14:16, 17:52 (12–20 h).
  - Klučenice → Solenice: slots 13:15, 15:15, 17:15, 19:15 (typed 14); rt 19, lay 3. Step 4: ok, window 15:30–17:30: slots 17:15; real 15:30 17:15; filled 1/1. Day (5–23) exact/within 3/trips 1/1/4; off the pattern: 15:30 (12–20 h).

### 472 Strakonice - Blatná - Příbram

- **Core points:** Příbram, autobusové nádraží; Příbram, II.poliklinika; Březnice, autobusové stanoviště; Uzenice; Blatná, železniční stanice; Strakonice, autobusové nádraží. Anchor 15:50.
- **Reading:** Příbram – Narysov – Vysoká – Třebsko – Tochovice – Březnice, beyond to Uzenice, Blatná and Strakonice (Jihočeský kraj). Příbram – Březnice runs about hourly at uneven minutes: out of Příbram 12:55, 14:00, 14:45 (to Uzenice), 15:40 (to Uzenice), 16:19 and 17:19 from Jiráskovy sady (393 buses going on), 16:55 (to Blatná), 18:19 (to Blatná); back from Březnice 13:05, 14:00, 14:55, 16:25, 17:05, 19:37. Read at II.poliklinika (all trips pass it): 472, every 120 with two slots each way in the line's window 15:20–17:20, exact (Příbram 16:21, 16:55; Březnice 16:25, 17:05), 3 buses. The trips beyond Březnice are cut there in the game; their stops are on 472 Strakonice, every 480 on the one through round (Příbram 12:00 → Strakonice, Strakonice 14:25 → Příbram). Off: Příbram 12:55, 14:00, 14:45, 15:40; Březnice 13:05, 14:00, 14:55, 19:37; the Uzenice and Blatná trips beyond Březnice (listed, stops on 472 Strakonice).
- **472** every 120, need 3 (waits {"Příbram, autobusové nádraží": [75, 69], "Březnice, autobusové stanoviště": [4, 50]}): Příbram, autobusové nádraží 16:21 and 16:55 (II.poliklinika 16:26 / 17:00) → Zdaboř → Narysov → Vysoká → Třebsko → Modřovice → Chrást → Tochovice → Horčápsko → Březnice (40 min); Březnice 16:25 and 17:05 back (41 min). Every 120. 16:21 stands for the 16:19 from Jiráskovy sady. The game line runs via Vysoká u Příbramě, as the slot trips do.
  - autobusové nádraží → autobusové stanoviště: slots 12:21, 12:55, 14:21, 14:55, 16:21, 16:55, 18:21, 18:55 (typed 80, 114); knot II.poliklinika 0:26, 1:00; rt 40, lay 3. Step 4: ok, window 15:20–17:20: slots 16:21 16:55; real 15:40 16:21 16:55; filled 2/2. Day (5–23) exact/within 3/trips 4/5/14; off the pattern: 14:00, 14:45, 15:40, 17:21 (12–20 h).
  - autobusové stanoviště → autobusové nádraží: slots 12:25, 13:05, 14:25, 15:05, 16:25, 17:05, 18:25, 19:05 (typed 4, 84); rt 41, lay 3. Step 4: ok, window 15:20–17:20: slots 16:25 17:05; real 16:25 17:05; filled 2/2. Day (5–23) exact/within 3/trips 3/3/9; off the pattern: 14:00, 14:55, 19:37 (12–20 h).
- **472 Strakonice** every 480, need 1 (waits {"Příbram, autobusové nádraží": [219], "Strakonice, autobusové nádraží": [15]}): Příbram 12:00 → Březnice → Drahenice → Uzenice → Myštice → Blatná → Sedlice → Radomyšl → Strakonice (130 min); Strakonice 14:25 back (116 min): the one through round, every 480.
  - autobusové nádraží → autobusové nádraží: slots 12:00 (typed 179); rt 130, lay 3. Step 4: no slot in the window (named in the why). Day (5–23) exact/within 3/trips 1/1/1; off the pattern: none (12–20 h).
  - autobusové nádraží → autobusové nádraží: slots 14:25 (typed 324); rt 116, lay 3. Step 4: no slot in the window (named in the why). Day (5–23) exact/within 3/trips 1/1/2; off the pattern: none (12–20 h).

### 477 Blatná - Bělčice - Březí

- **Core points:** Blatná, železniční stanice; Blatná, Palackého; Bezdědovice, Dobšice; Březí [pásmo 9 2]. Anchor 14:30.
- **Reading:** Blatná – Bělčice – Hostišovice – Tisov – Hvožďany – Březí (Jihočeský kraj; Hvožďany in okres Příbram). One bus: Blatná 11:45, 14:40, 17:05; Březí 12:50, 15:35 (rounds of about 145 min). Every 144: Blatná 14:40 (17:04 for 17:05), Březí 15:35 (12:47 for 12:50), 1 bus. 477 Bezdědovice: the Blatná – Bezdědovice, Dobšice shuttle (Palackého 14:05, Dobšice 14:15 back to the station), every 480, the only service of Bezdědovice. Off: Blatná 11:45.
- **477** every 144, need 1 (waits {"Blatná, železniční stanice": [48], "Březí [pásmo 9 2]": [15]}): Blatná, železniční stanice 14:40 → Bělčice → Hostišovice → Tisov → Hvožďany → Březí (40 min); Březí 15:35 back (41 min). Every 144, 1 bus.
  - železniční stanice → Březí [pásmo 9 2]: slots 12:16, 14:40, 17:04, 19:28 (typed 99); rt 40, lay 3. Step 4: ok, window 14:00–16:00: slots 14:40; real 14:40; filled 1/1. Day (5–23) exact/within 3/trips 1/2/4; off the pattern: none (12–20 h).
  - Březí [pásmo 9 2] → železniční stanice: slots 13:11, 15:35, 17:59 (typed 10); rt 41, lay 3. Step 4: ok, window 14:00–16:00: slots 15:35; real 15:35; filled 1/1. Day (5–23) exact/within 3/trips 1/1/3; off the pattern: 12:50 (12–20 h).
- **477 Bezdědovice** every 480, need 1 (waits {"Blatná, Palackého": [455], "Bezdědovice, Dobšice": [1], "Blatná, železniční stanice": [0]}): Blatná, Palackého 14:05 → Bezdědovice → Dobšice (9 min); Dobšice 14:15 → Blatná, železniční stanice (12 min); then on to Palackého. Every 480.
  - Palackého → Dobšice: slots 14:05 (typed 304); rt 9, lay 3. Step 4: ok, window 14:00–16:00: slots 14:05; real 14:05; filled 1/1. Day (5–23) exact/within 3/trips 1/1/2; off the pattern: none (12–20 h).
  - Dobšice → železniční stanice: slots 14:15 (typed 314); rt 12, lay 1. Step 4: ok, window 14:00–16:00: slots 14:15; real 14:15; filled 1/1. Day (5–23) exact/within 3/trips 1/1/1; off the pattern: none (12–20 h).
  - železniční stanice → Palackého: untimed (empty run, 3 min).

### 478 Příbram - Mirovice - Písek

- **Core points:** Příbram, autobusové nádraží; Chraštice; Mirovice, náměstí; Písek, autobusové nádraží. Anchor 16:00.
- **Reading:** Příbram – Zbenice – Kozárovice – Chraštice – Mirovice (Jihočeský kraj) – Mirotice – Předotice – Písek. One through round a day in the afternoon (Příbram 12:15 → Písek, Písek 15:15 → Příbram): 478, every 480, 1 bus. The Příbram – Mirovice trips (12:55, 14:45, 16:35, 18:25 out, 12:30 back) are buses going home to Mirovice (an outstation; their stops are on 478) and are off the pattern. 478 Chraštice: the Mirovice – Boješice – Řeteč – Chraštičky – Chraštice shuttle (16:00 / 16:15; also 12:25 / 12:52), every 480, the only service of Boješice, Řeteč, Chraštičky and Ohař.
- **478** every 480, need 1 (waits {"Příbram, autobusové nádraží": [197], "Písek, autobusové nádraží": [80]}): Příbram, autobusové nádraží 12:15 → Zbenice → Kozárovice → Chraštice → Mirovice → Mirotice → Předotice → Písek (99 min); Písek 15:15 back the same way (103 min): the afternoon through round, every 480.
  - autobusové nádraží → autobusové nádraží: slots 12:15 (typed 194); rt 100, lay 3. Step 4: no slot in the window (named in the why). Day (5–23) exact/within 3/trips 1/1/2; off the pattern: none (12–20 h).
  - autobusové nádraží → autobusové nádraží: slots 15:15 (typed 374); rt 103, lay 3. Step 4: no slot in the window (named in the why). Day (5–23) exact/within 3/trips 1/1/2; off the pattern: none (12–20 h).
- **478 Chraštice** every 480, need 1 (waits {"Mirovice, náměstí": [451], "Chraštice": [1]}): Mirovice, náměstí 16:00 → Ohař → Boješice → Řeteč → Chraštičky → Chraštice (14 min); Chraštice 16:15 back the same way (14 min, a 1-minute turn as in the timetable): every 480.
  - náměstí → Chraštice: slots 16:00 (typed 419); rt 14, lay 3. Step 4: ok, window 15:30–17:30: slots 16:00; real 16:00; filled 1/1. Day (5–23) exact/within 3/trips 1/1/2; off the pattern: 12:25 (12–20 h).
  - Chraštice → náměstí: slots 16:15 (typed 434); rt 14, lay 1. Step 4: ok, window 15:30–17:30: slots 16:15; real 16:15; filled 1/1. Day (5–23) exact/within 3/trips 1/1/2; off the pattern: 12:52 (12–20 h).

### 486 Sedlčany - Křepenice - Osečany

- **Core points:** Sedlčany, autobusové stanoviště; Nalžovice, Chlum; Radíč; Osečany. Anchor 16:00.
- **Reading:** Sedlčany – Kňovice – Nalžovice – Křepenice – Radíč – Osečany, with Nalžovice, Chlum trips. One bus a day in a sequence: Sedlčany 13:15 → Osečany 13:58, Osečany 14:30 → Nalžovice, Chlum 14:41, Chlum 15:33 → Osečany 15:48 (Osečany 18:30 → Radíč). Modelled as that sequence every 480 with an empty return from Osečany to Sedlčany (in reality the bus stays at Osečany; it meets 754 there in the morning), 1 bus: Křepenice, Radíč and the Nalžovice, Chlum stops have no other line.
- **486** every 480, need 1 (waits {"Sedlčany, autobusové stanoviště (1)": [299], "Osečany (2)": [32], "Osečany (4)": [0], "Nalžovice, Chlum (3)": [52]}): Sedlčany 13:15 → Nalžovice → Křepenice → Radíč → Osečany (43 min); Osečany 14:30 → Radíč → Nalžovice, Chlum (11 min); Chlum 15:33 → Radíč → Osečany (15 min); then empty to Sedlčany. Every 480, 1 bus.
  - autobusové stanoviště → Osečany: slots 13:15 (typed 254); rt 43, lay 3. Step 4: no slot in the window (named in the why). Day (5–23) exact/within 3/trips 1/1/1; off the pattern: none (12–20 h).
  - Osečany → Chlum: slots 14:30 (typed 329); rt 11, lay 3. Step 4: no slot in the window (named in the why). Day (5–23) exact/within 3/trips 1/1/1; off the pattern: none (12–20 h).
  - Chlum → Osečany: slots 15:33 (typed 392); rt 15, lay 3. Step 4: ok, window 15:30–17:30: slots 15:33; real 15:33; filled 1/1. Day (5–23) exact/within 3/trips 1/1/1; off the pattern: none (12–20 h).
  - Osečany → autobusové stanoviště: untimed (empty run, 28 min).

### 495 Nepomuk - Březnice - Mirovice

- **Core points:** Rožmitál pod Třemšínem, autobusové stanoviště; Březnice, autobusové stanoviště; Nepomuk, sídliště; Mirovice, náměstí. Anchor 14:10.
- **Reading:** A network around Rožmitál and Březnice: Rožmitál – Březnice by two roads (via Bezděkov, Hlubyně and Vševily, or via Pňovice and Přední Poříčí), Rožmitál – Nepomuk (okres Příbram) and Březnice – Počaply – Mirovice (Jihočeský kraj). One Simutrans line per road: 495 (via Hlubyně: Březnice 13:40, 14:50, Rožmitál 13:40, 14:35; every 120, two slots each way, exact; 2 buses), 495 Pňovice (Březnice 15:35, Rožmitál 18:10; every 360; 1 bus), 495 Nepomuk (Rožmitál 15:40, Nepomuk 15:55; every 120; 1 bus) and 495 Mirovice (Březnice 15:30, Mirovice 14:15; every 120; 1 bus). Off: Březnice 12:45, 17:35, 19:01; Rožmitál 16:10, 13:45 (5 min), Nepomuk 15:55 → Březnice beyond Rožmitál; Mirovice 13:15, 16:00, 19:23; Březnice 12:00, 17:45; the Rožmitál – Pňovice local trips 14:40 / 14:46.
- **495** every 120, need 2 (waits {"Březnice, autobusové stanoviště": [50, 55], "Rožmitál pod Třemšínem, autobusové stanoviště": [35, 40]}): Březnice 13:40 / 14:50 → Vševily → Hlubyně → Bezděkov pod Třemšínem → Rožmitál (15 min); Rožmitál 13:40 / 14:35 back the same way (15 min). Every 120. 13:40 out of Březnice is the 13:15 from Mirovice running on; 13:40 from Rožmitál runs on to Počaply.
  - autobusové stanoviště → autobusové stanoviště: slots 12:50, 13:40, 14:50, 15:40, 16:50, 17:40, 18:50, 19:40 (typed 39, 109); rt 15, lay 1. Step 4: ok, window 13:40–15:40: slots 13:40 14:50; real 13:40 14:50; filled 2/2. Day (5–23) exact/within 3/trips 2/2/7; off the pattern: 12:45, 17:35 (12–20 h).
  - autobusové stanoviště → autobusové stanoviště: slots 12:35, 13:40, 14:35, 15:40, 16:35, 17:40, 18:35, 19:40 (typed 39, 94); rt 15, lay 3. Step 4: ok, window 13:40–15:40: slots 13:40 14:35; real 13:40 14:35; filled 2/2. Day (5–23) exact/within 3/trips 2/2/6; off the pattern: 16:05 (12–20 h).
- **495 Pňovice** every 360, need 1 (waits {"Březnice, autobusové stanoviště": [194], "Rožmitál pod Třemšínem, autobusové stanoviště": [144]}): Březnice 15:35 → Přední Poříčí → Pňovice → Rožmitál (11 min); Rožmitál 18:10 back (11 min; 12:10 in the repeats). Every 360, 1 bus.
  - autobusové stanoviště → autobusové stanoviště: slots 15:35 (typed 154); rt 11, lay 3. Step 4: ok, window 13:40–15:40: slots 15:35; real 15:35; filled 1/1. Day (5–23) exact/within 3/trips 1/1/6; off the pattern: 19:01 (12–20 h).
  - autobusové stanoviště → autobusové stanoviště: slots 12:10, 18:10 (typed 309); rt 11, lay 3. Step 4: no slot in the window (named in the why). Day (5–23) exact/within 3/trips 2/2/5; off the pattern: 12:20, 16:10 (12–20 h).
- **495 Nepomuk** every 120, need 1 (waits {"Rožmitál pod Třemšínem, autobusové stanoviště": [95], "Nepomuk, sídliště": [6]}): Rožmitál 15:40 / 17:40 → Zalány → Nepomuk, sídliště (9 min); Nepomuk 15:55 / 13:55 / 17:55 back (10 min). Every 120, 1 bus; model window 15:00–17:00 (at the line's 14:10 window the 13:45 is 5 min from the :40 slot).
  - autobusové stanoviště → sídliště: slots 13:40, 15:40, 17:40, 19:40 (typed 39); rt 9, lay 3. Step 4: ok, window 15:00–17:00: slots 15:40; real 15:40; filled 1/1. Day (5–23) exact/within 3/trips 2/2/7; off the pattern: 13:45 (12–20 h).
  - sídliště → autobusové stanoviště: slots 13:55, 15:55, 17:55, 19:55 (typed 54); rt 10, lay 3. Step 4: ok, window 15:00–17:00: slots 15:55; real 15:55; filled 1/1. Day (5–23) exact/within 3/trips 3/3/7; off the pattern: 12:10 (12–20 h).
- **495 Mirovice** every 120, need 1 (waits {"Březnice, autobusové stanoviště": [61], "Mirovice, náměstí": [31]}): Březnice 15:30 → Počaply → Plíškovice → Mirovice, náměstí (14 min); Mirovice 14:15 back (14 min). Every 120, 1 bus.
  - autobusové stanoviště → náměstí: slots 13:30, 15:30, 17:30, 19:30 (typed 29); rt 14, lay 3. Step 4: ok, window 13:40–15:40: slots 15:30; real 15:30; filled 1/1. Day (5–23) exact/within 3/trips 1/1/4; off the pattern: 12:00, 17:45 (12–20 h).
  - náměstí → autobusové stanoviště: slots 12:15, 14:15, 16:15, 18:15 (typed 74); rt 14, lay 3. Step 4: ok, window 13:40–15:40: slots 14:15; real 14:15; filled 1/1. Day (5–23) exact/within 3/trips 1/1/4; off the pattern: 13:15, 16:00, 19:23 (12–20 h).

### 496 Březnice - Bělčice - Blatná

- **Core points:** Březnice, autobusové stanoviště; Bělčice, Záhrobí; Koupě; Blatná, Sádlov. Anchor 14:40.
- **Reading:** Březnice – Hudčice – Koupě – Bělčice (Jihočeský kraj), with trips to Záhrobí and on to Blatná, Sádlov. Afternoon: Březnice 12:57 → Sádlov, Sádlov 14:17 → Březnice (496, every 480, the only service of Sádlov, Závišín and Bělčice, ZD); and one bus running Březnice 14:40 → Bělčice, Záhrobí, 15:05 back, 15:40 → Koupě, 15:55 back, 17:05 → Koupě, 17:20 back: 496 Koupě, that sequence as a circuit every 240, the only service of Záhrobí, Hudčice and Koupě.
- **496** every 480, need 1 (waits {"Březnice, autobusové stanoviště": [370], "Blatná, Sádlov": [40]}): Březnice 13:00 (the 12:57 from the railway station) → Hudčice → Koupě → Bělčice → Závišín → Blatná, Sádlov (37 min); Sádlov 14:17 back (33 min). Every 480.
  - autobusové stanoviště → Sádlov: slots 13:00 (typed 239); rt 37, lay 3. Step 4: no slot in the window (named in the why). Day (5–23) exact/within 3/trips 3/3/3; off the pattern: none (12–20 h).
  - Sádlov → autobusové stanoviště: slots 14:17 (typed 316); rt 33, lay 3. Step 4: ok, window 14:10–16:10: slots 14:17; real 14:17; filled 1/1. Day (5–23) exact/within 3/trips 3/3/3; off the pattern: none (12–20 h).
- **496 Koupě** every 240, need 1 (waits {"Březnice, autobusové stanoviště (1)": [70], "Březnice, autobusové stanoviště (3)": [15], "Březnice, autobusové stanoviště (5)": [60], "Bělčice, Záhrobí (2)": [2], "Koupě (4)": [5], "Koupě (6)": [5]}): Březnice 14:40 → Hudčice → Koupě → Bělčice → Záhrobí (23 min) and Záhrobí 15:05 back (20 min); Březnice 15:40 → Hudčice → Koupě (10 min) and Koupě 15:55 back (10 min); Březnice 17:05 → Koupě and 17:20 back (10 min each). The one-bus sequence, every 240.
  - autobusové stanoviště → Záhrobí: slots 14:40, 18:40 (typed 99); rt 23, lay 3. Step 4: ok, window 14:10–16:10: slots 14:40; real 14:40; filled 1/1. Day (5–23) exact/within 3/trips 1/1/3; off the pattern: 12:05 (12–20 h).
  - Záhrobí → autobusové stanoviště: slots 15:05, 19:05 (typed 124); rt 20, lay 2. Step 4: ok, window 14:10–16:10: slots 15:05; real 15:05; filled 1/1. Day (5–23) exact/within 3/trips 1/1/2; off the pattern: none (12–20 h).
  - autobusové stanoviště → Koupě: slots 15:40, 19:40 (typed 159); rt 10, lay 3. Step 4: ok, window 14:10–16:10: slots 15:40; real 15:40; filled 1/1. Day (5–23) exact/within 3/trips 1/1/1; off the pattern: none (12–20 h).
  - Koupě → autobusové stanoviště: slots 15:55, 19:55 (typed 174); rt 10, lay 3. Step 4: ok, window 14:10–16:10: slots 15:55; real 15:55; filled 1/1. Day (5–23) exact/within 3/trips 1/1/1; off the pattern: none (12–20 h).
  - autobusové stanoviště → Koupě: slots 13:05, 17:05 (typed 4); rt 10, lay 3. Step 4: no slot in the window (named in the why). Day (5–23) exact/within 3/trips 1/1/1; off the pattern: none (12–20 h).
  - Koupě → autobusové stanoviště: slots 13:20, 17:20 (typed 19); rt 10, lay 3. Step 4: no slot in the window (named in the why). Day (5–23) exact/within 3/trips 1/1/2; off the pattern: 13:05 (12–20 h).

### 500 Příbram - Krásná Hora nad Vltavou - Petrovice

- **Core points:** Příbram, autobusové nádraží; Jablonná, Horní Hbity; Kamýk nad Vltavou; Krásná Hora nad Vltavou; Petrovice [PB 2]. Anchor 16:00.
- **Reading:** Příbram – Milín, Buk – Radětice – Jablonná, Horní Hbity – Dolní Hbity – Zduchovice – Kamýk nad Vltavou – Svatý Jan – Krásná Hora nad Vltavou – Krašovice – Petrovice. Through trips about every 3 h: Příbram 10:50, 13:45, 16:50 (19:00 to Krásná Hora); Petrovice 12:00, 15:50. Every 180 at the line's 16:00 window: Příbram 16:50 (13:50 for the real 13:45, 5 min off), Petrovice 15:50, 2 buses. Listed: Příbram – Horní Hbity trips 12:00, 17:50 (they go on as 510 to Smolotely, the 0-minute chains at Horní Hbity), Příbram 15:05 → Solenice, Horní Hbity 15:16 → Krásná Hora, Krásná Hora 16:25 → Petrovice; their stops are on 500, 471 and 510. 500 Solenice: the 15:05 to Solenice via Drsník, Nepřejov and Větrov, every 480 with an empty return, the only afternoon service of those three places.
- **500** every 180, need 2 (waits {"Příbram, autobusové nádraží": [174], "Petrovice [PB 2]": [49]}): Příbram, autobusové nádraží 16:50 → Milín, Buk → Radětice → Horní Hbity → Kamýk nad Vltavou → Krásná Hora nad Vltavou → Petrovice (71 min); Petrovice 15:50 back the same way (66 min). Every 180.
  - autobusové nádraží → Petrovice [PB 2]: slots 13:50, 16:50, 19:50 (typed 49); rt 71, lay 3. Step 4: ok, window 15:30–17:30: slots 16:50; real 16:50; filled 1/1. Day (5–23) exact/within 3/trips 2/2/4; off the pattern: 13:45 (12–20 h).
  - Petrovice [PB 2] → autobusové nádraží: slots 12:50, 15:50, 18:50 (typed 169); rt 66, lay 3. Step 4: ok, window 15:30–17:30: slots 15:50; real 15:50; filled 1/1. Day (5–23) exact/within 3/trips 1/1/3; off the pattern: 12:00 (12–20 h).
- **500 Solenice** every 480, need 1 (waits {"Příbram, autobusové nádraží": [378], "Solenice": [0]}): Příbram 15:05 → Milín, Buk → Radětice → Pečice, Drsník → Horní Hbity → Dolní Hbity, Nepřejov → Solenice, Větrov → Solenice (41 min), then empty back to Příbram (in reality the bus goes on at Solenice). Every 480, for Drsník, Nepřejov and Větrov, which have no other trip here.
  - autobusové nádraží → Solenice: slots 15:05 (typed 364); rt 54, lay 3. Step 4: no slot in the window (named in the why). Day (5–23) exact/within 3/trips 1/1/1; off the pattern: none (12–20 h).
  - Solenice → autobusové nádraží: untimed (empty run, 48 min).

### 501 MHD Příbram 501 Šachetní - Milínská - Jiráskovy sady - Dubno,učiliště - Bytíz,věznice

- **Core points:** Příbram, Šachetní; Příbram, Jiráskovy sady; Příbram, Nová Hospoda Polní; Dubno, učiliště; Příbram, Bytíz, věznice. Anchor 15:00.
- **Reading:** Šachetní – Drkolnov – Milínská – Jiráskovy sady – Nová Hospoda – Dubno, učiliště, some trips 3 min on to Bytíz, věznice (the prison). Every 30 at :05 / :35 until 15:05 (back from Dubno :00 / :30); then Šachetní 15:25 (Bytíz), 15:55 (Nová Hospoda Polní short), 16:45, 17:05 (short), 17:45 (Bytíz), 18:05. Read at Nová Hospoda Polní (all trips pass it). 501: every 120 with three slots each way in the line's window 14:30–16:30 (Šachetní 14:35, 15:05, 15:55; Dubno 15:00, 15:30 and the Polní short 16:27), exact; the shorts are run on to Dubno in the game. 501 Bytíz takes the prison trips (every 480, Šachetní 15:25, Bytíz 16:02). Off the pattern: Šachetní 13:35, 16:45, 18:05; Dubno 13:35, 14:30 (to Jiráskovy sady), 17:10; the Bytíz trips 14:05 / 14:37 and 17:45 / 18:12.
- **501** every 120, need 2 (waits {"Příbram, Šachetní": [18, 33, 43], "Dubno, učiliště": [8, 3, 3]}): Šachetní 14:35, 15:05, 15:55 → Dubno, učiliště via Drkolnov, Milínská, Jiráskovy sady and Nová Hospoda (22 min); back timed at Nová Hospoda Polní 15:02, 15:32, 16:27 (Dubno 15:00, 15:30; 16:27 is a short trip that starts at Polní). Every 120.
  - Šachetní → učiliště: slots 12:35, 13:05, 13:55, 14:35, 15:05, 15:55, 16:35, 17:05, 17:55, 18:35, 19:05, 19:55 (typed 4, 54, 94); rt 22, lay 3. Step 4: ok, window 14:30–16:30: slots 14:35 15:05 15:55; real 14:35 15:05 15:55; filled 3/3. Day (5–23) exact/within 3/trips 10/10/20; off the pattern: 12:05, 13:35, 16:45, 18:05 (12–20 h).
  - učiliště → Šachetní: slots 12:25, 13:00, 13:30, 14:25, 15:00, 15:30, 16:25, 17:00, 17:30, 18:25, 19:00, 19:30 (typed 29, 84, 119); knot Nová Hospoda Polní 0:27, 1:02, 1:32; rt 22, lay 3. Step 4: ok, window 14:30–16:30: slots 15:00 15:30 16:25; real 15:00 15:30 16:25; filled 3/3. Day (5–23) exact/within 3/trips 8/8/19; off the pattern: 12:30, 13:35, 14:00, 17:10, 18:45 (12–20 h).
- **501 Bytíz** every 480, need 1 (waits {"Příbram, Šachetní": [418], "Příbram, Bytíz, věznice": [12]}): Šachetní 15:25 → Dubno, učiliště → Bytíz, věznice (25 min); Bytíz 16:02 back (25 min): one afternoon round of the prison trips, every 480, kept because Bytíz, věznice has no other line.
  - Šachetní → Bytíz, věznice: slots 15:25 (typed 384); rt 25, lay 3. Step 4: ok, window 14:30–16:30: slots 15:25; real 15:25; filled 1/1. Day (5–23) exact/within 3/trips 1/1/5; off the pattern: 14:05, 17:45 (12–20 h).
  - Bytíz, věznice → Šachetní: slots 16:02 (typed 421); rt 25, lay 3. Step 4: ok, window 14:30–16:30: slots 16:02; real 14:37 16:02; filled 1/1. Day (5–23) exact/within 3/trips 1/1/4; off the pattern: 14:37, 18:12 (12–20 h).

### 502 MHD Příbram 502 Brod,obec - Zdaboř - II. poliklinika - Svatá Hora

- **Core points:** Příbram, Svatá Hora; Příbram, II.poliklinika; Příbram, Zdaboř, Žežická; Příbram, Zdaboř, komerční zóna; Příbram, Žežice; Příbram, Brod, obec. Anchor 14:30.
- **Reading:** Town trunk Svatá Hora – Jiráskovy sady – autobusové nádraží – II.poliklinika – Zdaboř – komerční zóna. Every 10 from Svatá Hora 13:05–15:55 (:05 runs on to Žežice, 14:25 to Brod, obec), then every 15 to 19:05; back from komerční zóna every 10, from Žežice hourly at :35. Modelled at the line's anchor (window 14:00–16:00), Ex4: 502 komerční zóna takes five of the six slots an hour, 502 Žežice the :05, 502 Brod the one Brod round. Off the pattern: the every-15 departures after 16:00 that fall between the slots, the Žežická short trips before 13:00, 16:30 Žežice → komerční zóna.
- **502** every 60, need 5 (waits {"Příbram, Svatá Hora": [5, 5, 5, 5, 5], "Příbram, Zdaboř, komerční zóna": [5, 5, 55, 5, 5]}): Svatá Hora :15 / :25 / :35 / :45 / :55 → Zdaboř, komerční zóna via Jiráskovy sady, autobusové nádraží (ul. Čs.armády), II.poliklinika and Zdaboř, nemocnice (20 min); komerční zóna :00 / :10 / :20 / :30 / :50 back via náměstí T.G.M. and Balbínova. 15:35 is a Žežická short trip, run on to komerční zóna in the game.
  - Svatá Hora → Zdaboř, komerční zóna: slots :15 / :25 / :35 / :45 / :55 (typed 14, 24, 34, 44, 54); rt 20, lay 3. Step 4: ok, window 14:00–16:00: slots 14:15 14:25 14:35 14:45 14:55 15:15 15:25 15:35 15:45 15:55; real 14:15 14:35 14:45 14:55 15:15 15:25 15:35 15:45 15:55; filled 9/10. Day (5–23) exact/within 3/trips 42/42/59; off the pattern: 16:20, 16:50, 17:05, 17:50, 18:05, 18:20, 18:50, 19:05, 19:50 (12–20 h).
  - Zdaboř, komerční zóna → Svatá Hora: slots :00 / :10 / :20 / :30 / :50 (typed 9, 19, 29, 49, 59); rt 20, lay 3. Step 4: ok, window 14:00–16:00: slots 14:00 14:10 14:20 14:30 14:50 15:00 15:10 15:20 15:30 15:50; real 14:00 14:10 14:20 14:30 14:50 15:10 15:20 15:30 15:55; filled 8/10. Day (5–23) exact/within 3/trips 26/26/41; off the pattern: 13:15, 15:55, 16:25, 16:40, 16:55, 17:25, 17:40, 18:25, 18:40 (12–20 h).
- **502 Žežice** every 60, need 1 (waits {"Příbram, Svatá Hora": [5], "Příbram, Žežice": [5]}): Svatá Hora :05 → komerční zóna → Žežice, Žežičky, u křížku → Žežice (25 min); Žežice :35 back (25 min); 1 bus, the only service of the Žežice stops.
  - Svatá Hora → Žežice: slots :05 (typed 4); rt 25, lay 3. Step 4: ok, window 14:00–16:00: slots 14:05 15:05; real 14:05 15:05; filled 2/2. Day (5–23) exact/within 3/trips 9/9/16; off the pattern: 17:20, 18:35, 19:30 (12–20 h).
  - Žežice → Svatá Hora: slots :35 (typed 34); rt 25, lay 3. Step 4: ok, window 14:00–16:00: slots 14:35 15:35; real 14:35 15:35; filled 2/2. Day (5–23) exact/within 3/trips 8/8/17; off the pattern: 17:50, 19:00, 19:55 (12–20 h).
- **502 Brod** every 480, need 1 (waits {"Příbram, Svatá Hora": [425], "Příbram, Brod, obec": [7]}): Svatá Hora 14:25 → Zdaboř, Brodská → Brod, obec (23 min) and Brod 14:55 back (25 min): the one afternoon round, every 480, kept because Brod, obec has no other line. In the game it leaves Svatá Hora with the trunk's :25 bus (in reality the 14:25 is that slot's trip); every trunk minute is taken, so it cannot be moved off it.
  - Svatá Hora → Brod, obec: slots 14:25 (typed 324); rt 23, lay 3. Step 4: ok, window 14:00–16:00: slots 14:25; real 14:25; filled 1/1. Day (5–23) exact/within 3/trips 1/1/3; off the pattern: none (12–20 h).
  - Brod, obec → Svatá Hora: slots 14:55 (typed 354); rt 25, lay 3. Step 4: ok, window 14:00–16:00: slots 14:55; real 14:55; filled 1/1. Day (5–23) exact/within 3/trips 1/1/3; off the pattern: none (12–20 h).

### 503 MHD Příbram 503 Svatá Hora - Milínská - Zdaboř - Drkolnov - Březové Hory - Aut.nádr. - Svatá Hora

- **Core points:** Příbram, Svatá Hora; Příbram, Jiráskovy sady; Příbram, Březové Hory. Anchor 16:00.
- **Reading:** Circular Svatá Hora – Milínská – Nový rybník – Zdaboř – Drkolnov – Březové Hory – Kaufland – autobusové nádraží – Svatá Hora, 41 min. Hourly at :05 until 12:05, then 13:20, 14:20, 14:50, 15:20, 15:50, 16:50, 17:50. In its 16:00 window hourly at :50, exact (14:50–17:50); 14:20 and 15:20 (the every-30 extra) and 13:20 off the pattern.
- **503** every 60, need 1 (waits {"Příbram, Svatá Hora": [19]}): Svatá Hora :50 → Jiráskovy sady → Milínská → Nový rybník → Zdaboř, nemocnice → Drkolnov → Březové Hory → Kaufland → autobusové nádraží (ul. Čs.armády) → Svatá Hora, one circle of 41 min.
  - Svatá Hora → Svatá Hora: slots :50 (typed 49); rt 41, lay 3. Step 4: ok, window 15:30–17:30: slots 15:50 16:50; real 15:50 16:50; filled 2/2. Day (5–23) exact/within 3/trips 3/3/13; off the pattern: 12:05, 13:20, 14:20, 15:20 (12–20 h).

### 504 Příbram - Sádek - Hluboš

- **Core points:** Příbram, autobusové nádraží; Sádek; Bratkovice, Dominikální Paseky; Hluboš. Anchor 16:00.
- **Reading:** Příbram, autobusové nádraží – Kovohutě – Lhota u Příbramě – Obecnice – Drahlín – Sádek, beyond to Bratkovice, Dominikální Paseky and Hluboš. Out of Příbram hourly at :01, the destination alternating: even hours to Sádek (14:01, 16:01, 18:01), 13:01 and 17:01 to Bratkovice, Dominikální Paseky, 15:01 to Hluboš. Back from Sádek 14:26, 16:31, 18:26, from Bratkovice 13:31, from Hluboš 15:35 (the bus turns there in 0 minutes). Two Simutrans lines, both exact: 504 (Sádek, every 120) and 504 Hluboš (one bus every 240: Bratkovice at 13:01, Hluboš at 15:01, as the real bus runs them). Off the pattern: Sádek 14:26 and 18:26 (5 min from the 16:31 slot), the 17:01 Bratkovice trip has no return.
- **504** every 120, need 1 (waits {"Příbram, autobusové nádraží": [65], "Sádek": [7]}): Příbram, autobusové nádraží 16:01 (even hours :01) → Lhota u Příbramě → Obecnice → Drahlín → Sádek (23 min); Sádek 16:31 back (25 min). Every 120.
  - autobusové nádraží → Sádek: slots 12:01, 14:01, 16:01, 18:01 (typed 60); rt 23, lay 3. Step 4: ok, window 15:30–17:30: slots 16:01; real 16:01; filled 1/1. Day (5–23) exact/within 3/trips 4/4/5; off the pattern: none (12–20 h).
  - Sádek → autobusové nádraží: slots 12:31, 14:31, 16:31, 18:31 (typed 90); rt 25, lay 3. Step 4: ok, window 15:30–17:30: slots 16:31; real 16:31; filled 1/1. Day (5–23) exact/within 3/trips 1/1/4; off the pattern: 14:26, 18:26 (12–20 h).
- **504 Hluboš** every 240, need 1 (waits {"Příbram, autobusové nádraží (1)": [52], "Příbram, autobusové nádraží (3)": [62], "Bratkovice, Dominikální Paseky (2)": [2], "Hluboš (4)": [0]}): One bus every 240: Příbram 13:01 → Sádek → Bratkovice, Dominikální Paseky (28 min), back 13:31 (28 min); Příbram 15:01 → Sádek → Bratkovice → Hluboš (34 min), back 15:35 (0-minute turn as in the timetable, 34 min). The repeat 17:01 is the real 17:01 to Bratkovice. Model window 13:00–15:40, the round it stands for.
  - autobusové nádraží → Dominikální Paseky: slots 13:01, 17:01 (typed 0); rt 28, lay 3. Step 4: ok, window 13:00–15:40: slots 13:01; real 13:01; filled 1/1. Day (5–23) exact/within 3/trips 2/2/3; off the pattern: none (12–20 h).
  - Dominikální Paseky → autobusové nádraží: slots 13:31, 17:31 (typed 30); rt 28, lay 2. Step 4: ok, window 13:00–15:40: slots 13:31; real 13:31; filled 1/1. Day (5–23) exact/within 3/trips 1/1/2; off the pattern: none (12–20 h).
  - autobusové nádraží → Hluboš: slots 15:01, 19:01 (typed 120); rt 34, lay 3. Step 4: ok, window 13:00–15:40: slots 15:01; real 15:01; filled 1/1. Day (5–23) exact/within 3/trips 1/1/3; off the pattern: none (12–20 h).
  - Hluboš → autobusové nádraží: slots 15:35, 19:35 (typed 154); rt 34, lay 0. Step 4: ok, window 13:00–15:40: slots 15:35; real 15:35; filled 1/1. Day (5–23) exact/within 3/trips 1/1/2; off the pattern: none (12–20 h).

### 505 MHD Příbram 505 Orlov - Aut.nádr. - II.poliklinika - Lazec - Kozičín

- **Core points:** Příbram, Orlov; Příbram, K Podlesí; Příbram, autobusové nádraží (ul. Čs.armády); Příbram, Kozičín. Anchor 16:00.
- **Reading:** Orlov – Podlesí – autobusové nádraží – II.poliklinika – Březové Hory – Lazec – Kozičín: one bus shuttling all afternoon, a round every 65 min (Orlov 12:10, 13:45, 14:50, 15:55, 17:40; Kozičín 13:05, 14:15, 15:20, 16:25 to autobusové nádraží, 18:10). Every 120 at its 16:00 window, Orlov 15:55, Kozičín 16:25, exact, 1 bus; the 65-minute rounds 14:50 / 15:20 and 17:40 / 18:10 are off the pattern (no interval of the list holds 65 min).
- **505** every 120, need 1 (waits {"Příbram, Orlov": [59], "Příbram, Kozičín": [3]}): Orlov 15:55 (every 120) → Podlesí → autobusové nádraží → Březové Hory → Kozičín (27 min); Kozičín 16:25 back (31 min; the real trip ends at autobusové nádraží, the game bus runs on to Orlov), 1 bus.
  - Orlov → Kozičín: slots 13:55, 15:55, 17:55, 19:55 (typed 54); rt 27, lay 3. Step 4: ok, window 15:30–17:30: slots 15:55; real 15:55; filled 1/1. Day (5–23) exact/within 3/trips 1/1/8; off the pattern: 12:10, 13:45, 14:50, 17:40 (12–20 h).
  - Kozičín → Orlov: slots 12:25, 14:25, 16:25, 18:25 (typed 84); rt 31, lay 3. Step 4: ok, window 15:30–17:30: slots 16:25; real 16:25; filled 1/1. Day (5–23) exact/within 3/trips 1/1/9; off the pattern: 13:05, 14:15, 15:20, 18:10 (12–20 h).

### 506 MHD Příbram 506 Zavržice - Zdaboř - Fialka - II.poliklinika - Aut.nádr. - Koperníkova - Svatá Hora areál

- **Core points:** Příbram, Svatá Hora areál; Příbram, Jiráskovy sady; Příbram, autobusové nádraží (ul. Čs.armády); Příbram, Zdaboř, Červená; Příbram, Zavržice. Anchor 16:00.
- **Reading:** Svatá Hora areál – Koperníkova – Jiráskovy sady – Nemocnice – autobusové nádraží – II.poliklinika – Zdaboř – Fialka – Zdaboř, Červená. Hourly: Svatá Hora areál :20 (15:20, 16:20; 17:25), Červená :10 (13:10–18:10), exact as every 120 with 16:20 / 17:25 out. The trips alternate two paths between autobusové nádraží and II.poliklinika: via Evropská and Lidl or via Kaufland and průmyslová zóna (the Kaufland stops are on 503, 505 and 508). Three trips a day run on via Narysov to Zavržice (13:05 out, 14:03 back in the afternoon): 506 Zavržice, every 480, the only service of Zavržice.
- **506** every 120, need 2 (waits {"Příbram, Svatá Hora areál": [38, 33], "Příbram, Zdaboř, Červená": [16, 11]}): Svatá Hora areál 16:20 / 17:25 → Zdaboř, Červená (34 min); Červená :10 hourly back via Evropská, Lidl and Československé armády (37 min), every 120. The out trips alternate paths: 16:20 runs via Kaufland, průmyslová zóna and Hornických učňů (the path the game line takes), 17:25 via Evropská, Lidl and Československé armády (2 min shorter); the Evropská stops are on the way back.
  - Svatá Hora areál → Zdaboř, Červená: slots 12:20, 13:25, 14:20, 15:25, 16:20, 17:25, 18:20, 19:25 (typed 24, 79); rt 34, lay 3. Step 4: ok, window 15:30–17:30: slots 16:20 17:25; real 16:20 17:25; filled 2/2. Day (5–23) exact/within 3/trips 5/5/11; off the pattern: 14:05, 15:20 (12–20 h).
  - Zdaboř, Červená → Svatá Hora areál: slots 12:10, 13:10, 14:10, 15:10, 16:10, 17:10, 18:10, 19:10 (typed 9, 69); rt 37, lay 3. Step 4: ok, window 15:30–17:30: slots 16:10 17:10; real 16:10 17:10; filled 2/2. Day (5–23) exact/within 3/trips 9/9/12; off the pattern: none (12–20 h).
- **506 Zavržice** every 480, need 1 (waits {"Příbram, Svatá Hora areál": [377], "Příbram, Zavržice": [15]}): Svatá Hora areál 13:05 → Zdaboř, Červená → Narysov → Zavržice (43 min); Zavržice 14:03 back the same way (45 min): the afternoon round, every 480, for Zavržice (no other line).
  - Svatá Hora areál → Zavržice: slots 13:05 (typed 244); rt 43, lay 3. Step 4: no slot in the window (named in the why). Day (5–23) exact/within 3/trips 1/1/3; off the pattern: 18:05 (12–20 h).
  - Zavržice → Svatá Hora areál: slots 14:03 (typed 302); rt 45, lay 3. Step 4: no slot in the window (named in the why). Day (5–23) exact/within 3/trips 1/1/2; off the pattern: none (12–20 h).

### 507 MHD Příbram 507 Jiráskovy sady - Sázky - Zdaboř - II.poliklinika - Aut.nádr. - Kovohutě - Lhota u Příbramě,točna

- **Core points:** Příbram, Zdaboř, Žežická; Příbram, autobusové nádraží (ul. Čs.armády); Příbram, Kovohutě; Lhota u Příbramě, točna. Anchor 14:40.
- **Reading:** A sparse town line of single trips (13:13 Slivických bojovníků → Kovohutě, 14:18 Kovohutě → Jiráskovy sady, 14:40 Kovohutě → Žežická, 15:08 Žežická → Lhota u Příbramě, točna, 15:45 točna → Šachetní, 15:53 Žežická → Jiráskovy sady). Kept for its own stops, Lhota u Příbramě, točna and DISA, as one bus on the real 15:08 / 15:45 round, every 480, with an empty return from Šachetní to Žežická. The other trips are listed: their stops are on 504 (Kovohutě, RAVAK, Obecnická, Lhota) and 500 (Sázky, Slivických bojovníků, Mixova).
- **507** every 480, need 1 (waits {"Příbram, Zdaboř, Žežická": [411], "Lhota u Příbramě, točna": [9], "Příbram, Šachetní": [0]}): Zdaboř, Žežická 15:08 → II.poliklinika → autobusové nádraží → DISA → Kovohutě → Lhota u Příbramě, točna (28 min); točna 15:45 → DISA → autobusové nádraží → Drkolnov → Šachetní (28 min); then empty to Žežická. Every 480.
  - Zdaboř, Žežická → točna: slots 15:08 (typed 367); rt 28, lay 3. Step 4: ok, window 14:10–16:10: slots 15:08; real 15:08; filled 1/1. Day (5–23) exact/within 3/trips 1/1/3; off the pattern: none (12–20 h).
  - točna → Šachetní: slots 15:45 (typed 404); rt 28, lay 3. Step 4: ok, window 14:10–16:10: slots 15:45; real 15:45; filled 1/1. Day (5–23) exact/within 3/trips 1/1/1; off the pattern: none (12–20 h).
  - Šachetní → Zdaboř, Žežická: untimed (empty run, 4 min).

### 508 MHD Příbram 508 Svatá Hora - Aut.nádr. - Březové Hory - Drkolnov - Zdaboř - Milínská - Svatá Hora

- **Core points:** Příbram, Svatá Hora; Příbram, Jiráskovy sady; Příbram, Březové Hory; Příbram, Šachetní. Anchor 16:00.
- **Reading:** Circular the other way round: Svatá Hora – autobusové nádraží – Kaufland – Březové Hory – Šachetní – Drkolnov – Zdaboř – Nový rybník – Milínská – Svatá Hora, 41 min. Hourly: at :10 in the morning (9:10–11:10) and from 15:10 (15:10–18:10), at :00 at midday (12:00, 13:00, 14:00), with extras at 13:40 (to Šachetní only), 14:38 (from Jiráskovy sady) and 15:40. Modelled hourly at :10, exact from 15:10; the :00 trips and the extras are off the pattern.
- **508** every 60, need 1 (waits {"Příbram, Svatá Hora": [19]}): Svatá Hora :10 → Jiráskovy sady → autobusové nádraží (ul. Čs.armády) → Kaufland → Březové Hory → Šachetní → Drkolnov → Zdaboř → Nový rybník → Milínská → Svatá Hora, one circle of 41 min.
  - Svatá Hora → Svatá Hora: slots :10 (typed 9); rt 41, lay 3. Step 4: ok, window 15:30–17:30: slots 16:10 17:10; real 15:40 16:10 17:10; filled 2/2. Day (5–23) exact/within 3/trips 8/8/12; off the pattern: 12:00, 13:00, 14:00, 15:40 (12–20 h).

### 509 Trhové Dušníky - Příbram - Láz

- **Core points:** Trhové Dušníky; Příbram, autobusové nádraží; Příbram, Jiráskovy sady; Láz, Horní. Anchor 14:30.
- **Reading:** Trhové Dušníky – Příbram (autobusové nádraží, ul. Čs.armády, Jiráskovy sady) – Březové Hory – Bohutín – Láz, Horní: one bus shuttling the through line all afternoon, rounds of 85–100 min (Trhové Dušníky 14:12, 15:37, 17:17; Láz 14:58, 16:42, 17:58). Every 120 at the line's window 14:00–16:00: Trhové Dušníky 14:12, Láz 14:58, exact; the other trips are off the pattern (no interval of the list holds the uneven rounds).
- **509** every 120, need 1 (waits {"Trhové Dušníky": [40], "Láz, Horní": [3]}): Trhové Dušníky 14:12 → Příbram (Jinecká, Fibichova, Jiráskovy sady, autobusové nádraží (ul. Čs.armády)) → II.poliklinika → Školní kruhový objezd → Zdaboř, nemocnice → Březové Hory → Bohutín → Láz, Horní (43 min); Láz 14:58 back via Bohutín, Březové Hory, Karla Pobudy, Kladenská and náměstí 17.listopadu (34 min in the model; the 14:58 takes 36). Every 120.
  - Trhové Dušníky → Horní: slots 12:12, 14:12, 16:12, 18:12 (typed 71); rt 43, lay 3. Step 4: ok, window 14:00–16:00: slots 14:12; real 14:12 15:37; filled 1/1. Day (5–23) exact/within 3/trips 1/1/5; off the pattern: 15:37, 17:17 (12–20 h).
  - Horní → Trhové Dušníky: slots 12:58, 14:58, 16:58, 18:58 (typed 117); rt 34, lay 3. Step 4: ok, window 14:00–16:00: slots 14:58; real 14:58; filled 1/1. Day (5–23) exact/within 3/trips 1/1/4; off the pattern: 16:42, 17:58 (12–20 h).

### 510 Příbram - Smolotely

- **Core points:** Příbram, autobusové nádraží; Jablonná, Horní Hbity; Smolotely. Anchor 15:10.
- **Reading:** Příbram – Svatá Hora – Háje – Jablonná, Placy – Jablonná – Horní Hbity – Dolní Hbity – Smolotely. Afternoon: Příbram 14:45 → Smolotely, Smolotely 15:40 → Příbram (and 12:50); the Horní Hbity – Smolotely trips (12:29, 18:19) are 500 buses going on (0-minute chains at Horní Hbity). Every 480 at the 14:45 / 15:40 round, 1 bus: Smolotely and Jablonná, Placy have no other line.
- **510** every 480, need 1 (waits {"Příbram, autobusové nádraží": [391], "Smolotely": [21]}): Příbram, autobusové nádraží 14:45 → Svatá Hora → Háje → Jablonná → Horní Hbity → Smolotely (34 min); Smolotely 15:40 back (34 min): the afternoon round, every 480.
  - autobusové nádraží → Smolotely: slots 14:45 (typed 344); rt 34, lay 3. Step 4: ok, window 14:40–16:40: slots 14:45; real 14:45; filled 1/1. Day (5–23) exact/within 3/trips 1/1/2; off the pattern: none (12–20 h).
  - Smolotely → autobusové nádraží: slots 15:40 (typed 399); rt 34, lay 3. Step 4: ok, window 14:40–16:40: slots 15:40; real 15:40; filled 1/1. Day (5–23) exact/within 3/trips 1/1/2; off the pattern: 12:50 (12–20 h).

### 511 Příbram - Milín - Březnice

- **Core points:** Příbram, autobusové nádraží; Tochovice, ObÚ; Chraštice; Březnice, autobusové stanoviště. Anchor 13:40.
- **Reading:** Příbram – Milín – Tochovice – Březnice, autobusové stanoviště. Through trips Příbram 12:35, 14:35, 16:15; Březnice 12:45, 15:05 (via Chraštice), 16:10. Every 240 holds both afternoon rounds, exact: Příbram 14:35, 16:15; Březnice 15:05, 16:10; the game line takes the 15:05 path via Chraštice back (Svojšice, Kletice and Svojšice, rozcestí are on it only). Off the pattern: Příbram 12:35, Březnice 12:45. Listed: the Tochovice – Chraštice – Hořejany local trips (13:10, 13:20, 13:54, 17:05, 17:30, 18:02), stops on 511 and 478 except Tochovice, Hořejany. 511 Hořejany: the Tochovice – Hořejany trip (13:10 / 13:15), every 480, the only service of Hořejany.
- **511** every 240, need 2 (waits {"Příbram, autobusové nádraží": [5, 80], "Březnice, autobusové stanoviště": [114, 39]}): Příbram, autobusové nádraží 14:35 and 16:15 → Milín → Tochovice → Březnice (56 min); Březnice 15:05 and 16:10 back via Chraštice and Tochovice (65 min, the path of the 15:05; the 16:10 runs direct in 60). Every 240, 2 buses.
  - autobusové nádraží → autobusové stanoviště: slots 12:15, 14:35, 16:15, 18:35 (typed 94, 194); rt 56, lay 3. Step 4: ok, window 13:10–15:10: slots 14:35; real 14:35; filled 1/1. Day (5–23) exact/within 3/trips 2/2/4; off the pattern: 12:35 (12–20 h).
  - autobusové stanoviště → autobusové nádraží: slots 12:10, 15:05, 16:10, 19:05 (typed 124, 189); rt 65, lay 3. Step 4: ok, window 13:10–15:10: slots 15:05; real 15:05; filled 1/1. Day (5–23) exact/within 3/trips 2/2/4; off the pattern: 12:45 (12–20 h).
- **511 Hořejany** every 480, need 1 (waits {"Tochovice, ObÚ": [471], "Tochovice, Hořejany": [1]}): Tochovice, ObÚ 13:10 → Hořejany (4 min) and 13:15 back (4 min): the one afternoon trip to Hořejany (1.4 km from the next stop), every 480.
  - ObÚ → Hořejany: slots 13:10 (typed 249); rt 4, lay 3. Step 4: ok, window 13:10–15:10: slots 13:10; real 13:10; filled 1/1. Day (5–23) exact/within 3/trips 1/1/2; off the pattern: none (12–20 h).
  - Hořejany → ObÚ: slots 13:15 (typed 254); rt 4, lay 1. Step 4: ok, window 13:10–15:10: slots 13:15; real 13:15; filled 1/1. Day (5–23) exact/within 3/trips 1/1/2; off the pattern: none (12–20 h).

### 512 Příbram - Obecnice - Sádek

- **Core points:** Příbram, autobusové nádraží; Obecnice; Sádek. Anchor 16:00.
- **Reading:** Příbram, autobusové nádraží – Podlesí – Obecnice, Oseč – Obecnice (some trips on to Sádek). Afternoon: Příbram 14:31, 16:31 to Obecnice; Obecnice 15:10, 17:00 back; Sádek trips 12:41, 19:01, 19:41 (stops on 504). Every 120 in the line's 16:00 window: Příbram 16:31 (14:31 too), Obecnice 17:00; 15:10 is off the pattern.
- **512** every 120, need 1 (waits {"Příbram, autobusové nádraží": [70], "Obecnice": [10]}): Příbram, autobusové nádraží 16:31 (even hours :31) → Podlesí, Nové Podlesí → Obecnice, Oseč → Obecnice (19 min); Obecnice 17:00 back (21 min). Every 120.
  - autobusové nádraží → Obecnice: slots 12:31, 14:31, 16:31, 18:31 (typed 90); rt 19, lay 3. Step 4: ok, window 15:30–17:30: slots 16:31; real 16:31; filled 1/1. Day (5–23) exact/within 3/trips 2/2/5; off the pattern: 19:01 (12–20 h).
  - Obecnice → autobusové nádraží: slots 13:00, 15:00, 17:00, 19:00 (typed 119); rt 21, lay 3. Step 4: ok, window 15:30–17:30: slots 17:00; real 17:00; filled 1/1. Day (5–23) exact/within 3/trips 2/2/8; off the pattern: 12:50, 15:10, 19:50 (12–20 h).

### 514 Dobříš - Drevníky - Županovice

- **Core points:** Dobříš, náměstí; Drevníky; Županovice. Anchor 16:00.
- **Reading:** Dobříš – Rybníky – Drhovy – Borotice – Drevníky – Županovice: one bus, rounds of about 100 min (Dobříš 15:00, 16:35, 18:15; Županovice 13:30, 15:40, 17:20; Dobříš 13:40 → Drevníky). Every 120 on the 16:35 / 17:20 round, 1 bus. Off: Dobříš 15:00, 18:15; Županovice 13:30, 15:40; the Drevníky short 13:40.
- **514** every 120, need 1 (waits {"Dobříš, náměstí": [40], "Županovice": [10]}): Dobříš 16:35 → Rybníky → Drhovy → Borotice → Drevníky → Županovice (35 min); Županovice 17:20 back (35 min). Every 120.
  - náměstí → Županovice: slots 12:35, 14:35, 16:35, 18:35 (typed 94); rt 35, lay 3. Step 4: ok, window 15:30–17:30: slots 16:35; real 16:35; filled 1/1. Day (5–23) exact/within 3/trips 1/1/5; off the pattern: 15:00, 18:15 (12–20 h).
  - Županovice → náměstí: slots 13:20, 15:20, 17:20, 19:20 (typed 19); rt 35, lay 3. Step 4: ok, window 15:30–17:30: slots 17:20; real 15:40 17:20; filled 1/1. Day (5–23) exact/within 3/trips 1/1/5; off the pattern: 13:30, 15:40 (12–20 h).

### 515 Příbram - Nečín - Borotice

- **Core points:** Příbram, autobusové nádraží; Nečín; Hřiměždice, Vestec; Borotice, Čelina. Anchor 16:00 (set by hand, see the reading).
- **Reading:** Příbram – Dubno – Drásov – Višňová – Ouběnice – Daleké Dušníky – Nečín, then to Hřiměždice, Vestec or via Nečín, Žebrák and Drevníky to Borotice, Čelina: the one direct Příbram – Nečín line. Afternoon: Příbram 14:40 → Čelina, 16:00 and 17:40 → Vestec; Čelina 13:53 and Vestec 16:50 → Příbram; the Nečín – Čelina pair 13:08 / 13:25. Every 120 at 16:00 (anchor set by hand: the busiest stretch, 13:00–15:00, is the Čelina trips and the Nečín – Čelina pair; the line's own Vestec round runs at 16:00): Příbram 16:00 → Vestec, Vestec 16:50 → Příbram, both exact, 1 bus. Off the pattern: Příbram 17:40; the Čelina trips (14:40, 13:53, 13:08 / 13:25), listed: their stops are on 515, 514, 525 and 360 except Nečín, Žebrák (a coverage exception).
- **515** every 120, need 1 (waits {"Příbram, autobusové nádraží": [25], "Hřiměždice, Vestec": [5]}): Příbram, autobusové nádraží 16:00 → Dubno → Drásov → Višňová → Ouběnice → Daleké Dušníky → Nečín → Hřiměždice → Vestec (45 min); Vestec 16:50 back the same way (45 min). Every 120, 1 bus.
  - autobusové nádraží → Vestec: slots 12:00, 14:00, 16:00, 18:00 (typed 59); rt 45, lay 3. Step 4: ok, window 15:30–17:30: slots 16:00; real 16:00; filled 1/1. Day (5–23) exact/within 3/trips 1/1/3; off the pattern: 17:40 (12–20 h).
  - Vestec → autobusové nádraží: slots 12:50, 14:50, 16:50, 18:50 (typed 109); rt 45, lay 3. Step 4: ok, window 15:30–17:30: slots 16:50; real 16:50; filled 1/1. Day (5–23) exact/within 3/trips 1/1/2; off the pattern: none (12–20 h).

### 516 Sedlčany - Dublovice

- **Core points:** Sedlčany, autobusové stanoviště; Dublovice, Zvírotice. Anchor 15:00 (set by hand, see the reading).
- **Reading:** Sedlčany – Dublovice – Chramosty – Zvírotice: last trips of the day Sedlčany 13:15, 15:25, back from Zvírotice 13:55, 15:55. Anchor set to 15:00 by hand (the line ends at 16:18; at 16:00 the window would hold slots after the service). Every 120: Sedlčany 15:25, Zvírotice 15:55 (13:55 too), 1 bus; 13:15 off (10 min). Zvírotice and Chramosty have no other line.
- **516** every 120, need 1 (waits {"Sedlčany, autobusové stanoviště": [67], "Dublovice, Zvírotice": [4]}): Sedlčany 15:25 → Sedlecká → Solopysky, rozcestí → Příčovy, rozcestí → Dublovice → Chramosty → Zvírotice (26 min); Zvírotice 15:55 back via Dublovice, Břekova Lhota, Třebnice, rozcestí and Oříkov, rozcestí (23 min). Every 120.
  - autobusové stanoviště → Zvírotice: slots 13:25, 15:25, 17:25, 19:25 (typed 24); rt 26, lay 3. Step 4: ok, window 14:30–16:30: slots 15:25; real 15:25; filled 1/1. Day (5–23) exact/within 3/trips 1/1/3; off the pattern: 13:15 (12–20 h).
  - Zvírotice → autobusové stanoviště: slots 13:55, 15:55, 17:55, 19:55 (typed 54); rt 23, lay 3. Step 4: ok, window 14:30–16:30: slots 15:55; real 15:55; filled 1/1. Day (5–23) exact/within 3/trips 2/2/3; off the pattern: none (12–20 h).

### 517 Dobříš - Příbram

- **Core points:** Dobříš, náměstí; Příbram, autobusové nádraží; Příbram, Jiráskovy sady. Anchor 16:00.
- **Reading:** Dobříš, náměstí – Obořiště – Dlouhá Lhota – Drásov – Dubenec – Bytíz – Háje – Svatá Hora – Příbram, autobusové nádraží. Hourly all day, exact: Dobříš :55 (11:55–16:55; 17:55 has no trip), Příbram :49 (11:49–17:49). Most 517 arrivals at Dobříš meet a 317 departure to Prague within 5 min (a timed connection; two operators).
- **517** every 60, need 2 (waits {"Dobříš, náměstí": [27], "Příbram, autobusové nádraží": [19]}): Dobříš, náměstí :55 → Příbram, autobusové nádraží via Obořiště, Dlouhá Lhota, Drásov, Skalka, Bytíz, Háje and Svatá Hora (35 min); Příbram :49 back (39 min).
  - náměstí → autobusové nádraží: slots :55 (typed 54); rt 35, lay 3. Step 4: ok, window 15:30–17:30: slots 15:55 16:55; real 15:55 16:55; filled 2/2. Day (5–23) exact/within 3/trips 8/8/13; off the pattern: none (12–20 h).
  - autobusové nádraží → náměstí: slots :49 (typed 48); rt 39, lay 3. Step 4: ok, window 15:30–17:30: slots 15:49 16:49; real 15:49 16:49; filled 2/2. Day (5–23) exact/within 3/trips 12/12/14; off the pattern: 19:45 (12–20 h).

### 518 Sedlčany - Prosenická Lhota - Křečovice

- **Core points:** Sedlčany, autobusové stanoviště; Prosenická Lhota, Klimětice; Křečovice, Hořetice. Anchor 16:00.
- **Reading:** Sedlčany – Štětkovice – Prosenická Lhota – Klimětice – Křečovice, Hořetice. One bus every 90 in the afternoon, exact: Sedlčany 15:15, 16:45, 18:15; Hořetice 15:53, 17:23 (a 1-minute turn as in the timetable). 13:15 Sedlčany → Klimětice and 13:50 back are short trips on the same road (off the pattern).
- **518** every 90, need 1 (waits {"Sedlčany, autobusové stanoviště": [15], "Křečovice, Hořetice": [1]}): Sedlčany 15:15 / 16:45 → Štětkovice → Prosenická Lhota → Klimětice → Křečovice, Hořetice (37 min); Hořetice 15:53 / 17:23 back (37 min). Every 90, 1 bus.
  - autobusové stanoviště → Hořetice: slots 12:15, 13:45, 15:15, 16:45, 18:15, 19:45 (typed 44); rt 37, lay 3. Step 4: ok, window 15:30–17:30: slots 16:45; real 16:45; filled 1/1. Day (5–23) exact/within 3/trips 3/3/4; off the pattern: none (12–20 h).
  - Hořetice → autobusové stanoviště: slots 12:53, 14:23, 15:53, 17:23, 18:53 (typed 82); rt 37, lay 1. Step 4: ok, window 15:30–17:30: slots 15:53 17:23; real 15:53 17:23; filled 2/2. Day (5–23) exact/within 3/trips 2/2/3; off the pattern: none (12–20 h).

### 519 Sedlčany - Votice

- **Core points:** Sedlčany, autobusové stanoviště; Votice, autobusové stanoviště. Anchor 16:00.
- **Reading:** Sedlčany – Kosova Hora – Vojkov – Votice (okres Benešov), two licences run alternately. Hourly: Votice :10 (13:10–18:10), exact; Sedlčany 13:20, 14:00, 15:05, 16:15, 17:15, 19:15, modelled :15 (16:15, 17:15, 19:15 exact). Off: Sedlčany 13:20, 14:00, 15:05; Votice 12:30. The Votice-side stops are on this line only within the PID sheets.
- **519** every 60, need 2 (waits {"Votice, autobusové stanoviště": [17], "Sedlčany, autobusové stanoviště": [26]}): Votice, autobusové stanoviště :10 → Vojkov → Kosova Hora → Sedlčany (39 min); Sedlčany :15 back (38 min). Every 60.
  - autobusové stanoviště → autobusové stanoviště: slots :10 (typed 9); rt 39, lay 3. Step 4: ok, window 15:30–17:30: slots 16:10 17:10; real 16:10 17:10; filled 2/2. Day (5–23) exact/within 3/trips 6/6/11; off the pattern: 12:30 (12–20 h).
  - autobusové stanoviště → autobusové stanoviště: slots :15 (typed 14); rt 38, lay 3. Step 4: ok, window 15:30–17:30: slots 16:15 17:15; real 16:15 17:15; filled 2/2. Day (5–23) exact/within 3/trips 4/4/11; off the pattern: 13:20, 14:00, 15:05 (12–20 h).

### 520 Dobříš - Nečín - Kamýk nad Vltavou

- **Core points:** Dobříš, náměstí; Nečín; Hřiměždice, Vestec; Kamýk nad Vltavou, u Mášů. Anchor 15:00 (set by hand, see the reading).
- **Reading:** Dobříš – Daleké Dušníky – Nečín – Hřiměždice, Vestec (one trip a day on to Kamýk nad Vltavou via Velká, Sedla). Afternoon: Dobříš 12:55, 14:45, 15:55, 18:45; Vestec 13:31, 15:25, 18:05, each a 0-minute turn at Vestec (the chains, 7 of 9). Anchor set to 15:00 by hand: the 16:00 window holds no trip towards Dobříš (15:25 and 18:05 lie outside). 520: every 120, Dobříš 14:45, Vestec 15:25 (0-minute turn as in the timetable), 1 bus. 520 Kamýk: the Kamýk trips (Dobříš 16:45 out, Kamýk 6:24 in the morning back, the bus sleeps at Kamýk), every 480, the only service of Kamýk nad Vltavou, Velká, Sedla. Off: Dobříš 12:55, 15:55, 18:45; Vestec 13:31, 18:05; the Daleké Dušníky short 14:05.
- **520** every 120, need 1 (waits {"Dobříš, náměstí": [52], "Hřiměždice, Vestec": [5]}): Dobříš 14:45 → Dobříš, lom → Svaté Pole → Daleké Dušníky, Druhlice → Nečín → Hřiměždice → Vestec (35 min on the game line's road; the 14:45 itself runs via Obořiště, Vyšehrad, Ouběnice and Ostrov in 40 min, stops of 517 and 420); Vestec 15:25 back at once via Obory and Nečín, Jablonce (0-minute turn as in the timetable; 28 min). Every 120. Its 16:45 repeat leaves Dobříš with 520 Kamýk (in reality the 16:45 is the Kamýk trip and the Vestec trip leaves 15:55).
  - náměstí → Vestec: slots 12:45, 14:45, 16:45, 18:45 (typed 104); rt 35, lay 3. Step 4: ok, window 14:30–16:30: slots 14:45; real 14:45 15:55; filled 1/1. Day (5–23) exact/within 3/trips 2/2/7; off the pattern: 12:55, 15:55 (12–20 h).
  - Vestec → náměstí: slots 13:25, 15:25, 17:25, 19:25 (typed 24); rt 28, lay 0. Step 4: ok, window 14:30–16:30: slots 15:25; real 15:25; filled 1/1. Day (5–23) exact/within 3/trips 1/1/6; off the pattern: 12:25, 13:31, 18:05 (12–20 h).
- **520 Kamýk** every 480, need 1 (waits {"Dobříš, náměstí": [105], "Kamýk nad Vltavou, u Mášů": [302]}): Dobříš 16:45 → Nečín → Jablonce → Velká, Sedla → Kamýk nad Vltavou, u Mášů (37 min); Kamýk 6:24 back (36 min; repeats 14:24, 22:24): the real pair of the bus that sleeps at Kamýk, every 480.
  - náměstí → u Mášů: slots 16:45 (typed 464); rt 37, lay 3. Step 4: no slot in the window (named in the why). Day (5–23) exact/within 3/trips 1/1/1; off the pattern: none (12–20 h).
  - u Mášů → náměstí: slots 14:24 (typed 323); rt 36, lay 3. Step 4: no slot in the window (named in the why). Day (5–23) exact/within 3/trips 1/1/1; off the pattern: none (12–20 h).

### 521 Příbram - Rožmitál pod Třemšínem - Věšín

- **Core points:** Příbram, autobusové nádraží; Příbram, Březové Hory; Rožmitál pod Třemšínem, autobusové stanoviště; Věšín, Buková. Anchor 16:00.
- **Reading:** Příbram, autobusové nádraží (some trips from Jiráskovy sady, 393 buses going on) – Březové Hory – Bohutín – Láz – Vranovice – Sedlice – Rožmitál pod Třemšínem, every 2nd hour on to Věšín, Buková. Out of Příbram every 30, back from Rožmitál hourly; the buses sleep at Rožmitál and Věšín (outstation, timed at the inbound rate). 521: every 120, Příbram 15:06, 16:36, Rožmitál 15:38, 16:08. 521 Věšín: every 120, Příbram :36 odd hours, Věšín 16:55. Off: Příbram 14:06, 16:06, 18:06 (buses going home), Rožmitál 13:48, 18:08; Věšín 13:00, 14:15.
- **521** every 120, need 2 (waits {"Příbram, autobusové nádraží": [32, 32], "Rožmitál pod Třemšínem, autobusové stanoviště": [64, 4]}): Příbram, autobusové nádraží 15:06 and 16:36 (Březové Hory 15:15 / 16:45) → Bohutín → Láz, Jamky → Vranovice → Sedlice → Rožmitál (28 min); Rožmitál 15:38 and 16:08 back (26 min). Every 120. 16:36 stands for the 16:34 from Jiráskovy sady.
  - autobusové nádraží → autobusové stanoviště: slots 12:36, 13:06, 14:36, 15:06, 16:36, 17:06, 18:36, 19:06 (typed 5, 95); knot Březové Hory 0:45, 1:15; rt 28, lay 2. Step 4: ok, window 15:30–17:30: slots 16:36 17:06; real 16:06 16:36 17:06; filled 2/2. Day (5–23) exact/within 3/trips 6/6/14; off the pattern: 14:06, 16:06 (12–20 h).
  - autobusové stanoviště → autobusové nádraží: slots 12:08, 13:38, 14:08, 15:38, 16:08, 17:38, 18:08, 19:38 (typed 37, 67); rt 26, lay 3. Step 4: ok, window 15:30–17:30: slots 15:38 16:08; real 15:38 16:08; filled 2/2. Day (5–23) exact/within 3/trips 3/3/11; off the pattern: 13:48, 15:08, 19:12 (12–20 h).
- **521 Věšín** every 120, need 1 (waits {"Příbram, autobusové nádraží": [2], "Věšín, Buková": [43]}): Příbram, autobusové nádraží 15:36 (odd hours :36; Březové Hory :45) → Rožmitál → Starý Rožmitál → Věšín, Buková (36 min); Věšín 16:55 back (39 min). Every 120.
  - autobusové nádraží → Buková: slots 13:36, 15:36, 17:36, 19:36 (typed 35); knot Březové Hory 1:45; rt 36, lay 2. Step 4: ok, window 15:30–17:30: slots 15:36; real 15:36; filled 1/1. Day (5–23) exact/within 3/trips 4/4/6; off the pattern: 12:16 (12–20 h).
  - Buková → autobusové nádraží: slots 12:55, 14:55, 16:55, 18:55 (typed 114); rt 39, lay 3. Step 4: ok, window 15:30–17:30: slots 16:55; real 16:55; filled 1/1. Day (5–23) exact/within 3/trips 1/1/6; off the pattern: 12:15, 13:00, 14:15 (12–20 h).

### 522 Rožmitál pod Třemšínem - Hvožďany

- **Core points:** Rožmitál pod Třemšínem, autobusové stanoviště; Rožmitál pod Třemšínem, Hutě p.Tř., Zadní; Hvožďany. Anchor 15:00 (set by hand, see the reading).
- **Reading:** Rožmitál – Voltuš – Hutě pod Třemšínem – Roželov – Hvožďany. Out of Rožmitál every 90 (14:35, 16:05, 17:35, 19:05), back from Hvožďany only 12:27 and 15:07: the buses sleep at Hvožďany or go on there as 524 to Březnice (16:43 → 16:45). An outstation line, timed at its inbound rate: every 180, Rožmitál 14:35 (17:35 exact too), Hvožďany 15:07, 1 bus. Anchor set to 15:00 by hand: the 16:00 window holds no trip towards Rožmitál. Off: Rožmitál 16:05, 19:05 (buses going home or on as 524). Listed: the Rožmitál – Hutě, Zadní shuttles 13:05 / 13:19 (stops on 522).
- **522** every 180, need 1 (waits {"Rožmitál pod Třemšínem, autobusové stanoviště": [110], "Hvožďany": [5]}): Rožmitál 14:35 → Voltuš → Hutě, Zadní → Roželov → Hvožďany (27 min, the direct path of the 14:35, set by hand; the 16:05 and 19:05 run via Starý Smolivec, I, Pozdyně and Planiny in 38 min); Hvožďany 15:07 back via Pozdyně, Planiny, Mýta and Starý Smolivec, II (38 min). Every 180, 1 bus.
  - autobusové stanoviště → Hvožďany: slots 14:35, 17:35 (typed 94); rt 27, lay 3. Step 4: ok, window 14:30–16:30: slots 14:35; real 14:35 16:05; filled 1/1. Day (5–23) exact/within 3/trips 2/2/5; off the pattern: 16:05, 19:05 (12–20 h).
  - Hvožďany → autobusové stanoviště: slots 12:07, 15:07, 18:07 (typed 126); rt 38, lay 3. Step 4: ok, window 14:30–16:30: slots 15:07; real 15:07; filled 1/1. Day (5–23) exact/within 3/trips 1/1/4; off the pattern: 12:27 (12–20 h).

### 523 Plzeň - Spálené Poříčí - Rožmitál pod Třemšínem

- **Core points:** Rožmitál pod Třemšínem, autobusové stanoviště; Plzeň, Terminál Hlavní nádraží. Anchor 16:00.
- **Reading:** Rožmitál – Věšín, Teslíny – Spálené Poříčí – Nezvěstice – Starý Plzenec – Plzeň (Plzeňský kraj). Every 2 h: Plzeň :27 at odd hours (11:27–19:27, exact), Rožmitál 13:04, 15:10, 17:10. Every 120: Plzeň 15:27, Rožmitál 15:10 (17:10 exact, 13:04 6 min off), 2 buses.
- **523** every 120, need 2 (waits {"Plzeň, Terminál Hlavní nádraží": [52], "Rožmitál pod Třemšínem, autobusové stanoviště": [25]}): Plzeň 15:27 → Starý Plzenec → Šťáhlavy, Husova → zámek Kozel → Nezvěstice → Spálené Poříčí → Věšín → Rožmitál (78 min); Rožmitál 15:10 back via Žákava and Nezvěstice, mosty (82 min). Every 120. The trips take two paths each way: the game line runs out on the 17:27 / 19:27 path (via Husova and Kozel) and back on the 13:04 path (via Žákava and Nezvěstice, mosty), so every stop is on it; the 15:27 runs direct (1 min shorter) and the 15:10 via Kozel.
  - Terminál Hlavní nádraží → autobusové stanoviště: slots 13:27, 15:27, 17:27, 19:27 (typed 26); rt 78, lay 3. Step 4: ok, window 15:30–17:30: slots 17:27; real 17:27; filled 1/1. Day (5–23) exact/within 3/trips 5/6/7; off the pattern: none (12–20 h).
  - autobusové stanoviště → Terminál Hlavní nádraží: slots 13:10, 15:10, 17:10, 19:10 (typed 9); rt 85, lay 3. Step 4: ok, window 15:30–17:30: slots 17:10; real 17:10; filled 1/1. Day (5–23) exact/within 3/trips 2/2/6; off the pattern: 13:04 (12–20 h).

### 524 Březnice - Hvožďany

- **Core points:** Březnice, autobusové stanoviště; Hvožďany; Hvožďany, Leletice. Anchor 16:00.
- **Reading:** Březnice – Volenice – Pročevily – Hvožďany – Leletice. The afternoon is one bus: Březnice 14:40 → Leletice, Leletice 15:05 → Březnice, Březnice 15:30 → Hvožďany via Volenice, Bubovice, Zliv, Hvožďany 16:45 → Březnice (the 522 bus going on, the chains at Hvožďany), Březnice 17:10 → Leletice. Modelled as that sequence every 480, its way back from Leletice on the real 4:41 in the repeat, 1 bus: Leletice, Jamky, Javory, Vacíkov, Pročevily and Zliv have no other line.
- **524** every 480, need 1 (waits {"Březnice, autobusové stanoviště (1)": [95], "Březnice, autobusové stanoviště (3)": [0], "Březnice, autobusové stanoviště (5)": [7], "Hvožďany, Leletice (2)": [1], "Hvožďany, Leletice (6)": [187], "Hvožďany (4)": [57]}): One bus every 480 on its five afternoon trips: Březnice 14:40 → Volenice → Pročevily → Hvožďany → Leletice (24 min), Leletice 15:05 back (25 min); Březnice 15:30 → Volenice, Bubovice, Zliv → Hvožďany (18 min; it leaves the moment the 15:05 arrives, as in the timetable), Hvožďany 16:45 back via Zliv (18 min); Březnice 17:10 → Leletice (24 min); Leletice 20:41 back (25 min; the real 4:41 in the 8-hour repeat).
  - autobusové stanoviště → Leletice: slots 14:40 (typed 339); rt 24, lay 3. Step 4: no slot in the window (named in the why). Day (5–23) exact/within 3/trips 1/1/3; off the pattern: 12:00 (12–20 h).
  - Leletice → autobusové stanoviště: slots 15:05 (typed 364); rt 25, lay 1. Step 4: no slot in the window (named in the why). Day (5–23) exact/within 3/trips 1/1/1; off the pattern: none (12–20 h).
  - autobusové stanoviště → Hvožďany: slots 15:30 (typed 389); rt 18, lay 0. Step 4: ok, window 15:30–17:30: slots 15:30; real 15:30; filled 1/1. Day (5–23) exact/within 3/trips 1/1/4; off the pattern: none (12–20 h).
  - Hvožďany → autobusové stanoviště: slots 16:45 (typed 464); rt 18, lay 3. Step 4: ok, window 15:30–17:30: slots 16:45; real 16:45; filled 1/1. Day (5–23) exact/within 3/trips 1/1/2; off the pattern: none (12–20 h).
  - autobusové stanoviště → Leletice: slots 17:10 (typed 9); rt 24, lay 3. Step 4: ok, window 15:30–17:30: slots 17:10; real 17:10; filled 1/1. Day (5–23) exact/within 3/trips 1/1/1; off the pattern: none (12–20 h).
  - Leletice → autobusové stanoviště: slots 12:41 (typed 220); rt 24, lay 3. Step 4: no slot in the window (named in the why). Day (5–23) exact/within 3/trips 0/0/1; off the pattern: 12:35 (12–20 h).

### 525 Nový Knín - Borotice - Nový Knín

- **Core points:** Nový Knín; Nový Knín, Libčice. Anchor 16:00.
- **Reading:** Circular Nový Knín – Libčice – Borotice, Dražetice – Chramiště – Kozí Hory – mlýn – Pod Sady – Nový Knín, about 25 min. Hourly at :05 (13:05, 14:05, 15:05, 17:05 (to Libčice only)), but 16:00 and 18:10. Every 120 with :05 at odd hours and 16:00 at even hours, exact (13:05, 15:05, 16:00, 17:05); 14:05 and 18:10 off. 1 bus.
- **525** every 120, need 1 (waits {"Nový Knín": [35, 25]}): Nový Knín 15:05 / 16:00 → Libčice → Borotice, Dražetice → Chramiště → Kozí Hory → mlýn → Pod Sady → Nový Knín, one circle. Every 120; 17:05 is a trip to Libčice only, run round the circle in the game.
  - Nový Knín → Nový Knín: slots 12:00, 13:05, 14:00, 15:05, 16:00, 17:05, 18:00, 19:05 (typed 4, 59); rt 30, lay 3. Step 4: ok, window 15:30–17:30: slots 16:00 17:05; real 16:00 17:05; filled 2/2. Day (5–23) exact/within 3/trips 4/4/12; off the pattern: 12:15, 14:05, 18:10, 19:15 (12–20 h).

### 530 Příbram - Kamýk nad Vltavou

- **Core points:** Příbram, autobusové nádraží; Dolní Hbity; Dolní Hbity, Luhy; Kamýk nad Vltavou, u školky. Anchor 16:00.
- **Reading:** Příbram – Háje – Dolní Hbity – Luhy – Třtí – Kamýk nad Vltavou, u školky. Last trips of the day in the afternoon: Příbram 14:50 → Kamýk 15:42, Kamýk 15:45 → Příbram 16:37 (one bus, 3-min turn), Příbram 16:20 → Kamýk. Every 480 at the 14:50 / 15:45 round, 1 bus: Luhy, Smrčí, Třtí and Kamýk, u školky have no other line. Off: Příbram 16:20; the Dolní Hbity shorts 12:35–13:03.
- **530** every 480, need 1 (waits {"Příbram, autobusové nádraží": [373], "Kamýk nad Vltavou, u školky": [3]}): Příbram, autobusové nádraží 14:50 → Dolní Hbity → Luhy → Třtí → Kamýk nad Vltavou, u školky (52 min); Kamýk 15:45 back (52 min): the afternoon round, every 480.
  - autobusové nádraží → u školky: slots 14:50 (typed 349); rt 52, lay 3. Step 4: no slot in the window (named in the why). Day (5–23) exact/within 3/trips 1/1/4; off the pattern: 16:20 (12–20 h).
  - u školky → autobusové nádraží: slots 15:45 (typed 404); rt 52, lay 3. Step 4: ok, window 15:30–17:30: slots 15:45; real 15:45; filled 1/1. Day (5–23) exact/within 3/trips 1/1/2; off the pattern: none (12–20 h).

### 549 Sedlčany - Krásná Hora nad Vltavou - Klučenice

- **Core points:** Sedlčany, autobusové stanoviště; Vysoký Chlumec, pivovar; Krásná Hora nad Vltavou; Klučenice; Petrovice [PB 2]. Anchor 16:00.
- **Reading:** Sedlčany – Vysoký Chlumec – Krásná Hora nad Vltavou – Vletice – Klučenice. Afternoon: Sedlčany 12:15, 15:15 → Klučenice (every 180) and 16:15 → Krásná Hora; Klučenice 13:25 → Sedlčany, 16:05 → Krásná Hora; Krásná Hora 18:10 → Sedlčany. Every 180: Sedlčany 15:15 (12:15 too), Klučenice 16:05 read to Krásná Hora (the game bus runs on to Sedlčany), 1 bus. Off: Sedlčany 16:15, Klučenice 13:25, Krásná Hora 18:10. The Petrovice – Kuní trip (15:30 / 15:35) is run by the 450 bus and is a leg of Simutrans line 450.
- **549** every 180, need 1 (waits {"Sedlčany, autobusové stanoviště": [83], "Klučenice": [3]}): Sedlčany 15:15 → Vysoký Chlumec → Krásná Hora nad Vltavou → Vletice → Klučenice (47 min); Klučenice 16:05 → Krásná Hora (18 min, real end) and on to Sedlčany in the game. Every 180.
  - autobusové stanoviště → Klučenice: slots 12:15, 15:15, 18:15 (typed 134); rt 47, lay 3. Step 4: no slot in the window (named in the why). Day (5–23) exact/within 3/trips 2/2/2; off the pattern: none (12–20 h).
  - Klučenice → autobusové stanoviště: slots 13:05, 16:05, 19:05 (typed 4); rt 47, lay 3. Step 4: ok, window 15:30–17:30: slots 16:05; real 16:05; filled 1/1. Day (5–23) exact/within 3/trips 1/1/3; off the pattern: 13:25 (12–20 h).

### 551 Sedlčany - Kamýk nad Vltavou - Krásná Hora nad Vltavou

- **Core points:** Sedlčany, autobusové stanoviště; Svatý Jan, rozcestí; Kamýk nad Vltavou; Krásná Hora nad Vltavou. Anchor 13:30 (set by hand, see the reading).
- **Reading:** Sedlčany – Oříkov – Vysoký Chlumec, Hradce – Svatý Jan – Krásná Hora nad Vltavou (17:15 via Kamýk). Afternoon: Sedlčany 13:15, 15:20, 17:15; Krásná Hora 14:10 → Sedlčany (via Kamýk), 16:55 → Kamýk (goes on as 552). Every 120 on the 13:15 / 14:10 round, read in its window 13:00–15:00 (anchor set by hand: the line's one full round of the afternoon; the 13:00–15:00 and 15:00–17:00 stretches tie, and at 16:00 the window would hold the 16:10 repeat, whose real trip leaves Krásná Hora at 16:55 for Kamýk): 13:15 and 17:15 exact, 15:20 is 5 min from the 15:15 repeat; 1 bus. Off: Krásná Hora 16:55.
- **551** every 120, need 1 (waits {"Sedlčany, autobusové stanoviště": [12], "Krásná Hora nad Vltavou": [13]}): Sedlčany 13:15 / 17:15 → Oříkov → Hradce → Svatý Jan, rozcestí → Krásná Hora nad Vltavou (42 min, set by hand); Krásná Hora 14:10 → Kamýk → Svatý Jan → Sedlčany (53 min, set by hand), as the 14:10 runs. Every 120. The 17:15 repeat runs via Kamýk nad Vltavou in reality (11 min longer); the game line takes the direct path of the 13:15.
  - autobusové stanoviště → Krásná Hora nad Vltavou: slots 13:15, 15:15, 17:15, 19:15 (typed 14); rt 42, lay 3. Step 4: ok, window 13:00–15:00: slots 13:15; real 13:15; filled 1/1. Day (5–23) exact/within 3/trips 3/3/4; off the pattern: 15:20 (12–20 h).
  - Krásná Hora nad Vltavou → autobusové stanoviště: slots 12:10, 14:10, 16:10, 18:10 (typed 69); rt 53, lay 3. Step 4: ok, window 13:00–15:00: slots 14:10; real 14:10; filled 1/1. Day (5–23) exact/within 3/trips 1/1/2; off the pattern: none (12–20 h).

### 552 Sedlčany - Kamýk nad Vltavou

- **Core points:** Sedlčany, autobusové stanoviště; Svatý Jan, rozcestí; Kamýk nad Vltavou. Anchor 14:30 (set by hand, see the reading).
- **Reading:** Sedlčany – Třebnice – Svatý Jan – Hojšín – Kamýk nad Vltavou: one bus, Sedlčany 13:15, 15:15, 18:45 and Kamýk 12:30, 14:35, 17:10 (a 1-minute turn at Sedlčany 15:14 / 15:15). Anchor set to 14:30 by hand: in the 16:00 window the line has no departure from Sedlčany (15:15 and 18:45 lie outside it). Every 120: Sedlčany 15:15 (13:15 too), Kamýk 14:35, exact. Off: Kamýk 17:10, Sedlčany 18:45.
- **552** every 120, need 1 (waits {"Sedlčany, autobusové stanoviště": [1], "Kamýk nad Vltavou": [36]}): Sedlčany 15:15 / 13:15 → Třebnice → Svatý Jan → Kamýk nad Vltavou (44 min); Kamýk 14:35 back (39 min). Every 120, 1 bus (the real 1-minute turn at Sedlčany).
  - autobusové stanoviště → Kamýk nad Vltavou: slots 13:15, 15:15, 17:15, 19:15 (typed 14); rt 44, lay 1. Step 4: ok, window 14:00–16:00: slots 15:15; real 15:15; filled 1/1. Day (5–23) exact/within 3/trips 2/2/5; off the pattern: 18:45 (12–20 h).
  - Kamýk nad Vltavou → autobusové stanoviště: slots 12:35, 14:35, 16:35, 18:35 (typed 94); rt 39, lay 3. Step 4: ok, window 14:00–16:00: slots 14:35; real 14:35; filled 1/1. Day (5–23) exact/within 3/trips 1/1/5; off the pattern: 12:30, 17:10 (12–20 h).

### 556 Sedlec-Prčice - Sedlčany

- **Core points:** Sedlčany, autobusové stanoviště; Heřmaničky, železniční stanice; Sedlec-Prčice, náměstí. Anchor 16:00.
- **Reading:** Sedlčany – Kosova Hora – Heřmaničky, železniční stanice (okres Benešov) – Mrákotice – Sedlec-Prčice. Every 2 h, exact: Sedlčany odd hours :10 (13:10, 15:10, 17:10), Sedlec-Prčice odd hours :55 (13:55, 15:55; 18:10 off), a 1-minute turn at Sedlec-Prčice as in the timetable; 1 bus. Listed: Sedlec-Prčice 12:35 → Heřmaničky and Heřmaničky 13:02 → Sedlec-Prčice (stops on 556). The Heřmaničky stops are on this line only within the PID sheets.
- **556** every 120, need 1 (waits {"Sedlčany, autobusové stanoviště": [27], "Sedlec-Prčice, náměstí": [1]}): Sedlčany 15:10 → Kosova Hora → Heřmaničky, železniční stanice → Chotětice → Sedlec-Prčice (44 min); Sedlec-Prčice 15:55 back (48 min). Every 120.
  - autobusové stanoviště → náměstí: slots 13:10, 15:10, 17:10, 19:10 (typed 9); rt 44, lay 3. Step 4: ok, window 15:30–17:30: slots 17:10; real 17:10; filled 1/1. Day (5–23) exact/within 3/trips 3/3/5; off the pattern: none (12–20 h).
  - náměstí → autobusové stanoviště: slots 13:55, 15:55, 17:55, 19:55 (typed 54); rt 48, lay 1. Step 4: ok, window 15:30–17:30: slots 15:55; real 15:55; filled 1/1. Day (5–23) exact/within 3/trips 2/2/5; off the pattern: 18:10 (12–20 h).

### 559 Sedlčany - Nechvalice - Sedlec-Prčice

- **Core points:** Sedlčany, autobusové stanoviště; Nechvalice; Sedlec-Prčice, náměstí; Sedlec-Prčice, Vrchotice, Na Františku. Anchor 16:00.
- **Reading:** Sedlčany – Nechvalice – Myslkov – Sedlec-Prčice: three afternoon trips (Sedlec-Prčice 14:00, 16:20 → Sedlčany; Sedlčany 15:15 → Sedlec-Prčice). Between them the same bus runs the 513 shuttle to Vrchotice, Na Františku (15:58 arrive, 16:00 out, 16:10 back, 16:20 on as 559; also 13:40 / 14:00), the 0-minute chains at Sedlec-Prčice. So 559 is one circuit every 480 with the 513 legs, 1 bus: Nechvalice, Myslkov, Matějov and the Vrchotice stops have no other line. Off: Sedlec-Prčice 14:00 and the 13:40 shuttle.
- **559** every 480, need 1 (waits {"Sedlčany, autobusové stanoviště (1)": [372], "Sedlec-Prčice, náměstí (2)": [2], "Sedlec-Prčice, náměstí (4)": [0], "Sedlec-Prčice, Vrchotice, Na Františku (3)": [0]}): Sedlčany 15:15 → Nechvalice → Myslkov → Sedlec-Prčice (43 min); 16:00 → Uhřice → Jetřichovice → Vrchotice, Na Františku (10 min) and 16:10 back (0-minute turn as in the timetable; the 513 trips); Sedlec-Prčice 16:20 → Sedlčany (43 min; the bus arrives from Vrchotice at 16:20 and leaves at once, as in the timetable). Every 480, 1 bus.
  - autobusové stanoviště → náměstí: slots 15:15 (typed 374); rt 43, lay 3. Step 4: no slot in the window (named in the why). Day (5–23) exact/within 3/trips 1/1/3; off the pattern: none (12–20 h).
  - náměstí → Vrchotice, Na Františku: slots 16:00 (typed 419); rt 10, lay 2. Step 4: ok, window 15:30–17:30: slots 16:00; real 16:00; filled 1/1. Day (5–23) exact/within 3/trips 1/1/3; off the pattern: 13:40 (12–20 h).
  - Vrchotice, Na Františku → náměstí: slots 16:10 (typed 429); rt 10, lay 0. Step 4: ok, window 15:30–17:30: slots 16:10; real 16:10; filled 1/1. Day (5–23) exact/within 3/trips 1/1/3; off the pattern: 13:50 (12–20 h).
  - náměstí → autobusové stanoviště: slots 16:20 (typed 439); rt 43, lay 0. Step 4: ok, window 15:30–17:30: slots 16:20; real 16:20; filled 1/1. Day (5–23) exact/within 3/trips 1/1/3; off the pattern: 14:00 (12–20 h).

### 567 Příbram - Třebsko - Rožmitál pod Třemšínem

- **Core points:** Příbram, Jiráskovy sady; Třebsko; Rožmitál pod Třemšínem, Strýčkovy; Rožmitál pod Třemšínem, autobusové stanoviště. Anchor 16:00.
- **Reading:** Příbram, Jiráskovy sady – Bohutín – Vysoká u Příbramě – Narysov – Třebsko – Modřovice – Strýčkovy – Nesvačily – Rožmitál. Afternoon: Jiráskovy sady 14:36 → Rožmitál 15:20; Rožmitál 13:35 and 15:30 → Třebsko (the bus goes on as 472 there), Třebsko 17:11 → Rožmitál. Every 480 at the 14:36 / 15:30 round, 1 bus; the 15:30 is read to Třebsko and the game bus runs on to Jiráskovy sady. Strýčkovy, Nesvačily, Nový Dvůr, Modřovice, rozcestí and Vysoká u Příbramě, Rusalka have no other line.
- **567** every 480, need 1 (waits {"Příbram, Jiráskovy sady": [378], "Rožmitál pod Třemšínem, autobusové stanoviště": [10]}): Jiráskovy sady 14:36 → Bohutín → Vysoká u Příbramě, Rusalka → Narysov → Třebsko → Strýčkovy → Rožmitál (44 min); Rožmitál 15:30 → Strýčkovy → Třebsko (14 min, real end) and on to Jiráskovy sady in the game. Every 480.
  - Jiráskovy sady → autobusové stanoviště: slots 14:36 (typed 335); rt 44, lay 3. Step 4: no slot in the window (named in the why). Day (5–23) exact/within 3/trips 1/1/1; off the pattern: none (12–20 h).
  - autobusové stanoviště → Jiráskovy sady: slots 15:30 (typed 389); rt 48, lay 3. Step 4: ok, window 15:30–17:30: slots 15:30; real 15:30; filled 1/1. Day (5–23) exact/within 3/trips 1/1/3; off the pattern: 13:35 (12–20 h).

### 754 Příbram - Sedlčany - Benešov

- **Core points:** Příbram, autobusové nádraží; Sedlčany, autobusové stanoviště; Sedlčany, Sestrouň; Benešov, Terminál. Anchor 16:00 (set by hand, see the reading).
- **Reading:** Příbram – Dubno – Drásov – Sedlčany – Osečany – Křečovice – Neveklov – Tisem – Bystřice – Benešov, Terminál. Hourly through trips, passing Sedlčany at :15 towards Benešov and leaving Benešov at :35 (:30 before 15:00). 754: every 60, timed at Sedlčany :15 and Benešov :35; anchor 16:00, set by hand (the busiest stretch is the Sestrouň shuttles). 754 Sestrouň: the Sedlčany – Zberaz – Sestrouň shuttle (13:10, 15:10, 18:10, back 8 min later), every 120, the only service of Zberaz, koupaliště and Sestrouň. Listed: Příbram → Sedlčany 13:20, 14:30, 18:25 and Benešov 18:35 → Sedlčany.
- **754** every 60, need 4 (waits {"Příbram, autobusové nádraží": [7], "Benešov, Terminál": [29]}): Příbram, autobusové nádraží → Dubno → Drásov → Sedlčany (passing :15) → Osečany → Křečovice → Neveklov → Bystřice → Benešov, Terminál; Benešov :35 back the same way. Every 60.
  - autobusové nádraží → Terminál: slots :25 (typed 24); knot autobusové stanoviště 0:15; rt 101, lay 3. Step 4: ok, window 15:30–17:30: slots 16:25 17:25; real 16:25 17:25; filled 2/2. Day (5–23) exact/within 3/trips 10/10/12; off the pattern: none (12–20 h).
  - Terminál → autobusové nádraží: slots :35 (typed 34); rt 103, lay 3. Step 4: ok, window 15:30–17:30: slots 15:35 16:35; real 15:35 16:35; filled 2/2. Day (5–23) exact/within 3/trips 5/5/11; off the pattern: 12:20, 13:30, 14:30 (12–20 h).
- **754 Sestrouň** every 120, need 1 (waits {"Sedlčany, autobusové stanoviště": [105], "Sedlčany, Sestrouň": [0]}): Sedlčany, autobusové stanoviště 15:10 (odd hours :10) → koupaliště → Zberaz → Sestrouň (8 min); Sestrouň 15:18 back (0-minute turn as in the timetable, 7 min). Every 120; window 13:00–15:30, where the shuttle runs (13:10, 15:10; the 18:10 is off).
  - autobusové stanoviště → Sestrouň: slots 13:10, 15:10, 17:10, 19:10 (typed 9); rt 8, lay 3. Step 4: ok, window 13:00–15:30: slots 13:10 15:10; real 13:10 15:10; filled 2/2. Day (5–23) exact/within 3/trips 2/2/5; off the pattern: 18:10 (12–20 h).
  - Sestrouň → autobusové stanoviště: slots 13:18, 15:18, 17:18, 19:18 (typed 17); rt 7, lay 0. Step 4: ok, window 13:00–15:30: slots 13:18 15:18; real 13:18 15:18; filled 2/2. Day (5–23) exact/within 3/trips 2/2/5; off the pattern: 18:18 (12–20 h).
