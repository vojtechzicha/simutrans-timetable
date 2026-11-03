> 3 Nov 2026: re-checked for branches read by trip ends instead of where trips pass (the 381 Zásmuky case). Where `branch-check-2026-11-03.md` or `branch-review-2026-11-03.md` differs from this file, the 3 Nov files stand (the review over the check).

# Method check: PID Mělnicko (okres Mělník, prefix 250), 2 Nov 2026

Designed line by line with `../../DESIGN_BRIEF.md` (including "Learned on the pilot") and the bus schedule method v4
(`mirror/pipeline/bus-schedule-method.md` in the repo), after the pilot's review (`../rakovnicko/review-2026-11-01.md`).
The design is `lines.json` in this folder; `python -X utf8 pid-regional/scripts/run_oblast.py melnicko` rebuilds
`data/derived/schedule.json` and the three audits. It is written by a scratch design source (`scratchpad/melnicko/design.py`),
so `lines.json` is valid JSON at every save; the final file was checked to be exactly that design.

- **Data:** PID GTFS of 1 Nov 2026, service day Mon 2 Nov 2026 (school day): `data/derived/trips.json`, the whole-day
  readings `data/derived/reading/<L>.txt` (every trip at its core points, paths, the 0-minute chain test). **Live map:** the
  2 Nov poll had only started (a few morning plates at 4:00–6:00 in the readings, no afternoon chains), so Step 5b rests on the
  0-minute chain test alone; every pairing it shows is named in `notes` as "to confirm with the live map", and where an
  outstation row had to drop departures they were chosen by the shortest waits, not by plates.
- **Step 4**, per leg: in the Simutrans line's window (anchor −30 … +90) the slots equal the real departures ±1, and ≥ 80 % of
  the slots have a real departure within 3 min; then most exact over the day (5–23 h), then within 1, then the simplest; on
  one-departure-per-window lines the real 13–18 h headway decides, never "the longer interval". Each leg was searched with a
  scratch helper (every interval of the method's list, 1–8 slots placed on the window's real departures) and the slot subsets
  of outstation rows were ranked by the bus need of the pair (cyclic matching, as the builder's slot need), then set by hand.
- **Typed values** are (real − 61) mod every: every terminus is a loop. The builder writes them; the table at the end gives
  each typed value with the real time worked out from it ((typed + 61) mod every, shown at its occurrence in or after the model
  window). Hand checks, one per line, all agree: 348 Obříství Ládví 16:36 → (996 − 61) mod 60 = 35; 377 Letňany 15:46 →
  (946 − 61) mod 120 = 45; 400 Varnsdorf Letňany 16:10 → 909 mod 120 = 69; 410 Letňany 17:00 → 959 mod 480 = 479; 370
  Postřižín Kobylisy 14:13 → 792 mod 120 = 72; 663 Úžice Kralupy 17:26 → 985 mod 480 = 25; 474 Na Brabčově :09 → 8.
- **Result (after the 2 Nov review, see "Changed on 2 Nov"):** 36 lines → 34 modelled as **45 Simutrans lines, 108 buses**;
  470 and 480 not modelled. No night, replacement,
  Haló or Prague-sheet companion line is in this oblast. `run_oblast.py` runs clean. Step 4 audit: 91 timed legs, 90 ok,
  1 FEWER (370 Postřižín out of Kobylisy, the outstation case). Branch audit: 11 legs read at a midpoint, 8 `[ok]`, 3 flags
  explained below. Path audit: 1 slot trip off the modelled path (370 Kobylisy 14:58), explained below. Coverage: 507 afternoon stops, 482 on this
  sheet's lines, **0 uncovered of okres Mělník, 0 outside the Středočeský kraj** (13 coverage exceptions, each with its
  reason); 12 stops of other Středočeský okresy are on no line here (listed below for the `--final` pass). No approximate row;
  one owner check (the sheet's roadside-stop check).

## Changed on 2 Nov (after the review `review-2026-11-01.md`)

The independent review found 31 PASS, 5 FIX, 0 ASK; applied with the coordinator's two changes (the owner check is kept as the
sheet's one roadside-stop check; 693 gets the five-leg circuit so the two Katusice stops on no other sheet are served).
- **413:** `stops_via` Straškov-Vodochody, škola removed from the way back (only the 12:10 and 14:10 run that road; the window
  slot trips 15:15 and 16:15 skip it). The builder now takes the slot trips' road, 71 min (checked; no hand `rt` needed). The
  school stop is a coverage exception: one afternoon passing (14:41), 380 m from Straškov-Vodochody, served hourly. 3 buses.
- **466:** `stops_via` Vraňany removed from the way out: that road skipped Spomyšl and Spomyšl, u lávky, the line's core
  point. The out row now runs the :55 slot trips' road (Býkev – Spomyšl – Nové Ouholice), 66 min (the builder's median of the
  15:55 and 16:55, 65 and 68 min, with the 14:50 and 18:00 around the window); path audit clean for 466. The way back keeps the
  Staré Ouholice road of its 15:55 slot trip. Vraňany (village) is a coverage exception, 230 m from Vraňany, škola on 464.
  4 buses.
- **480:** moved to `unmodelled` (−1 bus). Its stops Kostelec nad Labem, u váhy / závod / Jiřice, Neratovice, sídliště and
  Libiš, Ke Spolaně / Spolana 3 / Spolana 4 are on 482 every 30 (Praha-východ sheet); Neratovice, Lobkovice, škola / V Lukách /
  statek (one afternoon trip, 13:41) are exceptions 350, 350 and 540 m from Lobkovice, hřbitov, which 482 serves every 30. The
  review also named Lobkovice, hřbitov among them; no trip of this oblast serves it, so it needs no exception here (10
  exceptions, not 11).
- **668:** `668 Mělnické Vtelno` removed (−1 bus); its 15:15 / 16:20 round is listed on 668's note; Řepín, Libeňská is a
  coverage exception (two afternoon passings, 660 m from Řepín on 668).
- **691:** the why names the out row's road via Medonosy, Chudolazy – Medonosy – Osinalice – Nové Osinalice – Vidim, Dolní
  (the 14:47's own road, 49 min).
- **693:** one circuit every 480 on the bus's real afternoon sequence, five legs: Mšeno, železniční stanice 13:48 → Okna
  (35 min), Okna 14:23 → Mšeno, železniční stanice (24 min, 0-minute turn), Mšeno, železniční stanice 15:02 → Katusice
  (38 min), Katusice 15:45 → Nosálov (21 min), Nosálov → Mšeno, železniční stanice untimed (empty, 14 min). Each slot is the
  real trip; still 1 bus (waits 15 at Mšeno, 5 at Katusice, 0 at Okna). Katusice, Doubravice and Katusice, Trnová (on no line
  of any sheet) and Katusice and Sudoměř are now on a line here.
- **Owner check:** rewritten as the sheet's one roadside-stop check: the six exceptions near a served stop of the same village
  (Straškov-Vodochody, škola; Vraňany; Řepín, Libeňská; Neratovice, Lobkovice ×3) with distance and trips, and the cost of
  serving them all: +2 buses (668 Mělnické Vtelno, 480) plus the two routings (413 via the school, 466 via Vraňany).
- **Notes:** added 475 → 747 at Mělník (0-minute chain), the cross-sheet 482 chains with 476 / 470 / 747 at Mělník, 856 → 857
  at Kralupy and 349's possible 0-minute turn at Ládví (6 buses instead of 7), all for the live map; 368's note says Zlonín is
  on 656 (Praha-východ sheet).
- Unchanged: every PASS line. Totals 47 → 45 Simutrans lines, 110 → 108 buses.

## Script problems

- `pid-regional/scripts/run_oblast.py` had a newline inside an f-string at line 40 (`print(f"` + a real line break +
  `coverage: …`), a SyntaxError, from about 05:20 to 05:30 on 2 Nov. I ran a scratch copy with the one-character fix (`\n`)
  until the coordinator fixed the real script; every run after that, and every result here, is from the real script. Not
  patched by me.
- Not a script bug, but worth knowing for the parallel designers: the session scratchpad is shared, and a helper file of mine
  there (`s4.py`) was edited by another session within minutes. I moved my helpers to `scratchpad/melnicko/` (design source `design.py` + `texts.py`, which write `lines.json`); two
  stale files of mine in the scratchpad root (a scratch copy of the runner and its patcher) had already been removed by someone else.
- The knot check on the cards (`knots`) compares the model with the median running time of all the leg's trips, not with the
  `stops_via` path the game line takes: 369 Štětí shows Mlazice 5 min early though the game bus on the Ješovice path passes it
  at :23 (said on the card). Untimed legs with no real trip on them (410 Jablonné, 480) list only their two end stops.

## Summary

| Line | Simutrans lines (every) | Slots, real minutes (out / back) | Buses |
|---|---|---|---|
| 316 | 316 (60), 316 Kralupy (60) | Bořislavka :00 :10 :20 :40 :50 / Holubice :07 :17 :27 :37 :57; Bořislavka :30 / Kralupy :28 | 7 + 2 |
| 348 | 348 Obříství (60), 348 Libiš (120), 348 (120) | Ládví :36 / Obříství :57; Ládví 16:06, 17:06 / Libiš 16:32, 17:17; Ládví :21 :51 / U Vojtěcha 15:36, 15:51, 16:21, 16:51 | 3 + 3 + 4 |
| 349 | 349 (15) | Ládví :10 / Podolí :14, every 15 | 7 |
| 351 | 351 (30), 351 Čakovičky (30) | Letňany :10 / Neratovice :07; Letňany :25 / Čakovičky :03 | 4 + 3 |
| 368 | 368 (60) | Ládví :15 :33 :55 / Předboj :12 :32 :52 | 4 |
| 369 | 369 Štětí (60), 369 (60) | Ládví :00 / Štětí :56 (Mlazice :23); Ládví :30 / Mlazice :53 | 4 + 3 |
| 370 | 370 (60), 370 Postřižín (120) | Kobylisy :20 :58 / Kralupy :16 :56; Kobylisy 14:13, 14:35, 15:15, 15:28 / u kapličky 14:25, 14:45, 15:05, 16:00 | 4 + 3 |
| 372 | 372 (120) | Kobylisy 17:05 / Kralupy 16:55 | 2 |
| 377 | 377 (120), 377 Brázdim (120) | Letňany 15:46, 16:46, 17:25 / Kostelec 15:41, 16:26, 16:56; Letňany 15:34, 16:34, 16:58 / Kostelec 15:56, 16:41, 17:26 | 3 + 3 |
| 400 | 400 (120), 400 Varnsdorf (120), 400 Rumburk (480) | Letňany 15:30 / Nový Bor 16:25; Letňany 16:10 / Varnsdorf 16:28; Rumburk 13:13 / empty return | 3 + 4 + 1 |
| 410 | 410 (480), 410 Jablonné (480) | Letňany 17:00 / Mimoň, Žitavská 14:27; Jablonné 14:40 / empty return | 1 + 1 |
| 413 | 413 (60) | Letňany :37 / Litoměřice :15 (the slot trips' road, without the school) | 3 |
| 464 | 464 (120) | Mělník 15:35, 16:35 / Horní Beřkovice 15:39, 17:24 | 3 |
| 466 | 466 (60) | Mělník :55 / Kralupy :55 | 4 |
| 468 | 468 (120) | Černouček 15:43 / Dolní Beřkovice 16:10 | 1 |
| 470 | not modelled (Step 8) | – | 0 |
| 473 | 473 (120), 473 Zálezlice (120) | Neratovice 16:31 / Kralupy 16:55; Neratovice 15:31 / Zálezlice 16:01 | 2 + 1 |
| 474 | 474 (60) | Na Brabčově :09 (Slovany :12) / Dobřeň :53 (Podolí :44) | 3 |
| 475 | 475 (60) | Mělník :50 / Horní Počaply :40 | 2 |
| 476 | 476 (60) | Mělník :27 / Nedomice :24 (Kostelec :32) | 2 |
| 479 | 479 (60) | Kostomlatského :21 / Korycany :49 | 1 |
| 480 | not modelled (stops on 482, Praha-východ sheet; Lobkovice ×3 exceptions) | – | 0 |
| 646 | 646 (60) | Mělník :36 / Kralupy :40 | 2 |
| 658 | 658 (90) | Neratovice 16:08 / Odolena Voda, závod 16:51 | 1 |
| 663 | 663 Úžice (480); the Odolena Voda trips listed | Kralupy 17:26 / Úžice, logistické centrum 18:15 | 1 |
| 668 | 668 (120) | Mělník 16:30 / Mšeno 15:30 | 1 |
| 689 | 689 (480, circuit) | Mšeno 14:06 → Stránka, Ostrý 14:15 → Mšeno, Hradsko 14:38 → Mšeno | 1 |
| 690 | 690 (120) | Mšeno 14:29 / Kadlín 14:42 | 1 |
| 691 | 691 (240) | Mělník 14:47 / Vidim 15:45 | 1 |
| 692 | 692 (240) | Pšovka 16:24 / Kokořín 15:15 | 1 |
| 693 | 693 (480, five-leg circuit) | Mšeno, železniční stanice 13:48 → Okna 14:23 → Mšeno, železniční stanice 15:02 → Katusice 15:45 → Nosálov → Mšeno | 1 |
| 694 | 694 (480) | Liběchov 15:30 / Kokořín 14:43 | 1 |
| 695 | 695 (480) | Mělník 16:15 / Mšeno 13:15 | 1 |
| 696 | 696 (120) | Mělník 16:45 / Mšeno 15:45 | 1 |
| 747 | 747 (60) | Mělník :05 / Všetaty :10 (Byšice :23) | 2 |
| 857 | 857 (120) | Zákolany 16:16 / Kralupy, obchodní centrum 16:43 | 2 |
| **Total** | **45 Simutrans lines** | | **108** |

Bus counts are the builder's need from each pattern (Step 10), one Simutrans line at a time; real buses swap between these
lines (the chain tests show 466 ↔ 464 at Spomyšl, 692 ↔ 691 at Liběchov, 476 → 480 at Nedomice), so the per-line totals are
higher than the operators' own. Pooling is named in `notes` as an option, not applied.

## Line by line

Each line's card (`note`, each sim line's `why`) gives the route, the real minutes, what is off the pattern and why it is
split as it is; this section adds the reasoning and the rejected options. Window = the model window; "slots / real" = Step 4.

**316 Praha, Bořislavka – Holubice (– Kralupy).** Core: Bořislavka, Velké Přílepy, Holubice, Kralupy, železniční stanice.
Whole day: every 15 off-peak, every 10 from 14:40 to 17:20 out of Bořislavka (the :30 to Kralupy hourly 14:30–17:30); back at
Holubice :07 :17 :27 :37 :57 + Kralupy :28 passing Holubice :47. Holubice is the commonest end; Kralupy the outer end (okres
Mělník, the town stops Minice … V Zátiší are 316 and 857 only). Two lines (Ex4): five slots an hour to Holubice, `notvia`
Kralupy, and hourly Kralupy; combined every 10, no shared minute. Window 15:30–17:30: 10/10 and 10/10 exact; Kralupy 2/2 and
2/2. Rejected: every 10 to Holubice (the :30 slot is a Kralupy trip); every 12 (draft) fills 60 %. Need 7 + 2; the 54-min
Bořislavka wait is the :30 gap (pooling option in `notes`).

**348 Praha, Ládví – Neratovice, U Vojtěcha / Libiš, obec / Obříství.** Core: Ládví, U Vojtěcha, Libiš, obec, Obříství. Out
of Ládví exactly every 15 from 14:06 (:06 Libiš, :21 :51 U Vojtěcha, :36 Obříství). Back at U Vojtěcha every 15 too, but the
Libiš and U Vojtěcha starts swap (Libiš 14:51, 15:21, 16:36, 17:21, 18:21; U Vojtěcha 14:36, 15:36, 15:51, 16:21, 16:51,
17:36, 17:51, 18:36), so hourly rows per end fail: Libiš back every 60 at :17 leaves 16:17 empty (fill 50 %), at :32 leaves
15:32 empty; U Vojtěcha back every 30 at :21/:51 leaves 17:21 empty (75 %). Each end its own line (Ex4): Obříství every 60
(exact 14:36–18:36 / 14:57–17:57), Libiš and U Vojtěcha every 120 on the window's real trips (290 precedent). In the window
the three ends balance (2/2, 2/2, 4/4). Considered: one line to U Vojtěcha with the Libiš trips read at U Vojtěcha (every 60,
three slots, exact) — rejected, it would cut the Libiš extension (trips starting beyond the line's end, the 292 lesson);
Libiš's stops are also on 348 Obříství. Need 3 + 3 + 4.

**349 Praha, Ládví – Mělník, Podolí (– Mlazice).** Core: Ládví, Byškovice, Mělník, autobusové nádraží, Podolí, Mlazice.
Every 15 both ways all afternoon; window 8/8 and 8/8 exact. The :55 trips and 17:25–18:25 run on to Mlazice and no bus comes
back from Mlazice after 9:30 except 17:10 (Podolí 17:14): an outstation extension, not a branch with a return, so no
empty-return line (25 Oct rule); Pšovka, Loděnická, Mlazice are on 369. Need 7 (real 11-min turn at Podolí kept).

**351 Praha, Letňany – Čakovičky – Neratovice.** Core: Letňany, Hovorčovice, Čakovičky, Neratovice, železniční stanice.
Two exact every-30 lines (Neratovice :10/:07, Čakovičky :25/:03; `notvia` Kojetice on the Čakovičky legs). 4/4 each, all
exact; 15:34 back (via Neratovice, III.ZŠ) within 3. Kojetice is 351's own stop (on 351). Need 4 + 3.

**368 Praha, Ládví – Předboj (– Kojetice, Tůmovka).** Core: Ládví, Líbeznice, II, Předboj, Kojetice, Tůmovka. Out :15 :33
:55, back :12 :32 :52 at Předboj; the Tůmovka trips turn there in 0 min (13 of 13) and pass Předboj both ways, so they are
read at Předboj; Tůmovka is a stop of 348 and 369 (every 15). Considered: a 368 Kojetice line — the branch alone gives 2 out /
3 back in the window, no row passes both ways. Window 6/6 exact out, 5 real for 6 slots back (17:12 empty, 83 %). Need 4.
Zlonín (2 school trips Líbeznice, II → Zlonín, 13:07 and 14:02) is listed (okres Praha-východ; below).

**369 Praha, Ládví – Mělník, Mlazice / Štětí.** Core: Ládví, Tůmovka, Mělník, autobusové nádraží, Mlazice, Štětí, závod.
Ládví :00 Štětí / :30 Mlazice, back at Mlazice :23 / :53, exact hourly. Ješovice (Liběchov, Ješovice and u lípy) is served
only by the even-hour Štětí trips and two back; their alternation is not a 2-hour pattern (out 12:00, 14:00, 16:00; back
14:56, 15:56 — consecutive hours), so no every-120 split passes (tested: the Ješovice back line would leave 16:56 empty);
one Štětí line runs the Ješovice path (`stops_via`, knot Mlazice :23 with knot_rt 27). Mlazice starts `notvia` Štětí; the
Štětí back leg `via` Štětí so the knot reading takes no Mlazice start. Window 2/2 each, exact. Need 4 + 3.

**370 Praha, Kobylisy – Odolena Voda – Postřižín – Kralupy.** Core: Kobylisy, Odolena Voda, Dolní náměstí, Postřižín, u
kapličky, Veltrusy, Chvatěruby, Kralupy. Anchor 14:40 (window 14:10–16:10). Kralupy trips out are all via Veltrusy in the
window (:20, :58), back mostly via Chvatěruby (:16, :56; :25 via Veltrusy hourly) — a path circuit (`stops_via` Veltrusy out,
Chvatěruby back). Kralupy 4/4 out, 4 slots for 5 real back (15:25 off). The Odolena Voda trips end one stop short of
Postřižín, u kapličky, on the same road: one line 370 Postřižín (out `core_to` Odolena Voda, back read at Odolena Voda,
`notvia` Kralupy). It is outstation (window: 8 out, 4 back; the buses start at Odolena Voda and Postřižín in the morning):
every 120 at the inbound rate, four slots each way; of the 8 departures the 4 kept were chosen by the shortest waits (3 buses;
the first four in the window need 5). Audit FEWER on the out row (4 slots for 8). Need 4 + 3.

**372 Praha, Kobylisy – Úžice – Dřínov – Zlosyň – Kralupy.** Core: Kobylisy, Odolena Voda, Úžice, Zlosyň, Kralupy. The
Kralupy trips: Kobylisy 15:05, 17:05, 19:05 (every 120), Kralupy 13:42, 14:12, 14:47, 16:55, 17:55. One trip each way in the
window: every 120 (the real 13–18 h Kralupy headway; every 240 would hold them with 1 bus but halve the line). Dřínov and Úžice
stops are 372's own and on its path (out via Dřínov, náves, back via Újezdec). Zlosyň, Úžice and Odolena Voda shorts are
listed (outstation, no returns). Need 2.

**377 Praha, Letňany – Kostelec nad Labem.** Core: Letňany, Čakovice, Sluhy, Brázdim, Nový Brázdim, Kostelec. The two
middle paths (via Sluhy and Mratín, via Brázdim and Polerady) alternate trip by trip both ways, and all eight of their stops
other than Veleň are only on 377 (okres Praha-východ), so one line per path. Window per path: 4 out, 3 back (every 15 at
Kostelec, every 12 out of Letňany): every 120 three slots each way at the inbound rate; the dropped out departure per path
(16:22 Sluhy, 15:58 Brázdim) chosen by the shortest waits (3 buses each; other triples need 3–4). Need 3 + 3.

**400 Praha, Letňany – Mělník – Česká Lípa – Nový Bor – Varnsdorf – Rumburk.** Core: Letňany, Mělník, Dubá, Česká Lípa,
Nový Bor, Varnsdorf, Rumburk. Out hourly to Nový Bor (:30, via Dubá) and to Varnsdorf (:10, direct); back 1 per 2 hours from
each end in the window (Nový Bor 16:25, Varnsdorf 16:28): outstation, both at the inbound rate every 120 (Varnsdorf every 240
would need 2 buses instead of 4, but the real headway is 2 hours). `via` / `notvia` keep the ends apart (Varnsdorf trips pass
Nový Bor). The Nový Bor back row takes the 16:25's own path (`stops_via` Jestřebí, Újezd and Nový Bor, Pihel, pošta). The
Rumburk stops have only the 13:13: 400 Rumburk every 480 with the 13:13 timed and an empty return (1 bus; timing the real
18:40 out too needs 2 buses; timing the 8:40 out puts an unreal 16:40 slot in the window, Step 4 EMPTY). Need 3 + 4 + 1.

**410 Jablonné v Podj. – Mimoň – Doksy – Dubá – Mělník – Praha.** Liberecký licence; 4 afternoon trips. Every stop beyond
Dubá is only on 410 (25 Liberecký stops served 13–19): 410 every 480 on the one-bus round Mimoň, Žitavská 14:27 → Letňany
16:40, 17:00 → Mimoň (15:00 out off; with 15:00 timed it needs 2 buses), and 410 Jablonné every 480 for the 14:40 Jablonné →
Doksy (Jablonné, Stráž, Brniště, Noviny stops) with an empty return. Need 1 + 1.

**413 Praha, Letňany – Litoměřice.** Hourly exact (Letňany :37, Litoměřice :15 with 17:15 missing). Anchor 15:00 by hand
(the 16:00 window holds 17:15, a slot without a trip; 305 precedent): 2/2 and 2/2 exact. The way back runs the slot trips'
road (71 min); Straškov-Vodochody, škola (12:10, 14:10 only) is a coverage exception (changed on 2 Nov). Need 3.

**464 Mělník – Lužec – Spomyšl – Horní Beřkovice.** Core: Mělník, Podolí, Lužec, Spomyšl, Jeviněves, Horní Beřkovice,
točna. Out :35 hourly; back from Horní Beřkovice 12:44, 15:39, 17:24 (and shorts). Every 120 with the window's two each way,
exact (out 6 exact over the day, back 2). Rejected: every 60 back (:39 leaves 16:39 empty); the one-slot every-120 row
Mělník 16:35 / Horní Beřkovice 17:24 (1 bus, 4 exact against 8) — the method takes the exact two-slot row (290 precedent),
so it is noted on the card, not an owner check. Need 3.

**466 Mělník – Spomyšl – Nelahozeves – Kralupy.** Core: Mělník, Hořín, Brozánky, Spomyšl, Nelahozeves, u starého mostu,
Kralupy, železniční stanice, obchodní centrum. Hourly: Mělník :55 (:50 at 12:50, 14:50), Kralupy žst :55 back (read with
`core_to` Spomyšl: the odd-hour trips end there and go on as 464). Window 2/2 and 2/2 exact. The line has two roads through
Nová Ves; the stops of the Veltrusy – Staré Ouholice – Vepřek road and Vraňany village are only on 466, so the way back takes
that road (`stops_via` Staré Ouholice, its 15:55 slot trip's road); the way out runs the :55 slot trips' road via Spomyšl
(changed on 2 Nov: the Vraňany road skipped Spomyšl); Vraňany village is a coverage exception. Need 4.

**468 Mělník – Dolní Beřkovice – Černouček.** Own stops Cítov and Dolní Beřkovice, Josefka / železniční stanice /
Komenského are on the Černouček – Dolní Beřkovice shuttles (14:43, 15:43 / 15:10, 16:10, 2-min turns); every 120 on the
window's shuttle, 1 bus (every 60 leaves 16:43 and 17:10 empty). The Mělník trips' other stops are on 475. Need 1.

**470 Kralupy – Chlumín – Obříství – Mělník: not modelled (Step 8).** 3 + 4 afternoon trips at no fixed minute; every stop on
modelled lines (reason in `unmodelled`). Modelled it would be every 240, Mělník 16:27 / Kralupy 15:20, 1 bus.

**473 Neratovice – Zálezlice – Kralupy.** Core: Neratovice, Kojetická, Neratovice, železniční stanice, Obříství, Štěpánský
most, Zálezlice, Kozárovice, Všestudy, Kralupy. Neratovice hourly :31 alternating Zálezlice (odd hours, 3-min turn) and
Kralupy (even hours): two every-120 lines, together hourly as real. Window 1/1 each, exact. Need 2 + 1.

**474 Mělník – Kokořín – Dobřeň.** Hourly all day (Slovany :12 out, Podolí :44 back). All trips on one road, ending at Dobřeň,
Kokořín or Mělník, MŠ Chloumek: one line to Dobřeň (`core_to` MŠ Chloumek out, knot Podolí back). Anchor 16:00 by hand
(the auto window 13:10–15:10 holds the 13:18 MŠ Chloumek school short at Podolí 13:39, 5 min off :44, a slot without a trip;
282 rule). 2/2 each, exact. Need 3.

**475 Mělník – Horní Počaply.** Exact hourly :50 / :40. Need 2.

**476 Mělník – Kostelec nad Labem – Nedomice (– Brandýs).** Hourly :27 out, :32 back at Kostelec, náměstí (knot: the back
trips start at Brandýs, Kostelec or Nedomice). Anchor 15:00 by hand (the 16:00 window holds 17:15, 12 min off :27; 305
precedent). 2/2 each, exact. Branch audit `beyond`: the Brandýs trips start beyond Nedomice (okres Praha-východ; listed).
Need 2.

**479 Neratovice town line.** Exact hourly 13:21–16:21 / 13:49–16:49, one bus; anchor 15:00 by hand (17:38 is 17 min off).
Need 1.

**480 Všetaty – Kostelec – Neratovice: not modelled (changed on 2 Nov).** Four afternoon trips worked by the 476 buses; the
13:41 Kostelec, Martinská → Všetaty is this oblast's only service of ten stops, but seven of them are on 482 every 30 (the
Praha-východ sheet) and the three Lobkovice stops are 350–540 m from Lobkovice, hřbitov on 482: coverage exceptions. Need 0
(it was every 480 with an empty return, 1 bus).

**646 Mělník – Nová Ves – Kralupy.** Exact hourly :36 / :40. Need 2.

**658 Neratovice – Kojetice – Předboj – Odolena Voda.** Works trips at no fixed minute; Kojetice, železniční stanice has no
other line. Window (16:00 anchor) holds Neratovice 16:08, Odolena Voda 16:10 and 16:51: every 90 on the 16:08 / 16:51 round
(1 bus). The 15:29 / 16:10 round has 4 exact over the day against 2 but needs a hand window (it fails the 16:00 window); not
chosen. Need 1.

**663 Kralupy – Chvatěruby – Odolena Voda (– Úžice, logistické centrum).** The Odolena Voda trips (4 + 2) are sparse and
every stop is on 370 and 370 Postřižín (checked: removing their row left no stop uncovered); listed (Step 8). Úžice,
logistické centrum has only the 17:26 / 18:15 pair: 663 Úžice every 480. Need 1.

**668 Mělník – Řepín / Kanina – Mšeno (– Mělnické Vtelno).** No fixed minute; the Mšeno trips run either through Řepín or
through Kanina. Every 120 on the window's one-bus round (Mělník 16:30 via Řepín, Mšeno 15:30 via Kanina; 17:29 back is its
repeat within 1 min): both roads' own stops on one line. The Mělnické Vtelno round (15:15 / 16:20) is listed; Řepín, Libeňská is a coverage exception (changed on 2 Nov; it was 668
Mělnické Vtelno every 480, 1 bus). Need 1.

**689, 690, 691, 692, 693, 694, 695, 696 (Kokořín and Mšeno school lines).** Each has stops of its own (listed on the
cards), so each is a line on one real round, 1 bus each: 689 every 480 (the school loop, 3 legs, 0-min turn at Ostrý),
690 every 120 (real headway about 2 h; 0-min turn at Kadlín), 691 every 240 (14:47 / 15:45; repeat 18:47 for the real
19:00), 692 every 240 (16:24 / 15:15), 693 every 480 (a five-leg circuit on the bus's real sequence: the Okna loop — Okna, Luka, odbočka and Doksy, Žďár are
in Liberecký kraj — then the 15:02 to Katusice and the 15:45 to Nosálov, changed on 2 Nov), 694 every 480, 695 every 480 (16:15 / 13:15; every 120 or 240 put unreal back slots into the window), 696 every 120
(16:45 / 15:45, the window's round). Slots outside the window are named on the cards ("no slot in the window" in the
builder output: 691 out, 692 back, 693, 694 back, 695 back).

**747 Mělník – Byšice – Všetaty.** Anchor 13:50 (window 13:20–15:20). Out :05 (to Všetaty, Hostín or Konětopy; `core_to`
Hostín), back read at Byšice :23 (13:23 starts there). 2/2 each, exact. Branch audit `beyond`: the 14:05 slot trip runs on
to Konětopy (okres Praha-východ; listed). Need 2.

**857 Zákolany – Kralupy.** Zákolany :16 and Kralupy, obchodní centrum :43 every 2 hours; the odd-hour Kralupy town trips
(Minice 13:42, 15:42, 17:42 ↔ obchodní centrum 13:43, 15:43, 17:43; 3 each way, a regular short working) run over 857's own path
and are listed, as the pilot's Zličín shorts on 304 (a row of their own every 120 would need 2 buses; Minice – železniční
stanice also has 316 Kralupy hourly). Every 120, 1/1 each, exact. Need 2.

## Audit flags explained

- **Step 4 FEWER**: 370 Postřižín Kobylisy → u kapličky, 4 slots for 8 real (the outstation case, inbound rate).
- **Branch `[BRANCH]` 370 Postřižín back** (knot Odolena Voda): the 13:28 Kozomín, rozcestí → Kobylisy trip passes Odolena
  Voda at 13:35 and is off the pattern (its stops are on 370). **`[beyond]` 476 back**: the window slot 15:24 at Nedomice is the
  15:03 from Brandýs n.L.-St.Bol., nádraží; the game bus starts at Nedomice. **`[beyond]` 747 out**: the 14:05 slot trip runs
  on from Všetaty to Konětopy. Both named on the cards.
- **Path**: 370 Kobylisy 14:58 runs via Odolena Voda, závod and Klecany, D8 Park (skipping the centre; on the card). The two
  466 flags of the first design are gone (its out row now runs the slot trips' road).

## Shared terminals: departures within 3 min of each other (Step 5, bunching)

Game departures 14:00–18:00 at every stop where two or more Simutrans lines start, checked by script from `schedule.json`:
- **Praha, Ládví:** 349 and 368 both at :55 (real: 15:55 to Mlazice and 15:55 to Předboj; 349 runs by the D8, 368 by Líbeznice);
  369 :30, 368 :33, 348 Obříství :36 (all real minutes; 348 / 368 / 369 share Ládví – Líbeznice, the real timetable spaces them
  3 min). The lines of one real line never share a minute: 348's three at :06 / :21 / :36 / :51, 369's two at :00 / :30.
- **Praha, Letňany:** 351 and 400 Varnsdorf at 14:10 and 16:10, 351 Čakovičky and 377 at 17:25, 377 Brázdim / 413 / 351 at
  :34 / :37 / :40 — all real minutes, different roads after Letňany. 377's two lines are at least 12 min apart at both ends.
- **Kralupy nad Vltavou, železniční stanice:** 372, 466, 473 at 16:55 and 370 at 16:56 — all real (three roads: Veltrusy –
  Zlosyň, Nelahozeves, Veltrusy – Všestudy, and Chvatěruby). At 14:55 the same three meet again only because 372 and 473 repeat
  every 120 (real 14:47 and 14:44); 372 and 473 share the town and Veltrusy, as they do at the real 16:55.
- **Mělník, autobusové nádraží:** 464 :35 and 646 :36 (real; both by Pivovar and Podolí); 691 14:47 and 475 14:50 (real); 696
  14:45 is a repeat (real 15:05) on the Rousovice road, no shared stop with 691 / 475. 476 :27 and 668 16:30 leave on different
  roads.
- **Neratovice, železniční stanice:** 658 16:08 after 351 16:07 (real); 658's repeats 14:38 and 17:38 sit 1 min after 351's
  14:37 / 17:37 (every-90 repeats of a works line; both run to Kojetická first).
- **Kobylisy, Bořislavka, Kostelec nad Labem, Neratovice, Kojetická, Mšeno, Kokořín:** no two departures within 3 min (the 370
  pair, 316's two lines and 473's two lines interleave as the real ones do).

## Coverage

- Okres Mělník and outside the Středočeský kraj: 0 uncovered. 13 coverage exceptions (`coverage_exceptions`, each with its
  trips and distance): seven 480 stops on 482 every 30 (Kostelec nad Labem, u váhy / závod / Jiřice, Neratovice, sídliště,
  Libiš, Ke Spolaně / Spolana 3 / Spolana 4) and the six roadside stops of the owner check (Straškov-Vodochody, škola; Vraňany;
  Řepín, Libeňská; Neratovice, Lobkovice, škola / V Lukách / statek). Distances are from the GTFS stop coordinates.
- Stops of other Středočeský okresy served 13–19 only by this oblast's lines (for the `--final` pass):
  - **not on any line here** (12): Zlonín (368's two school trips; on 656, Praha-východ sheet);
    Brandýs n.L.-St.Bol., nádraží, náměstí, most, u brány, autobusové stanoviště, Proboštská jezera and Borek (476's Brandýs
    extension, okres Praha-východ — Brandýs is expected on that sheet); Konětopy, Dřísy, Dřísy, železniční stanice, Křenek (747's 14:05 and
    13:30, okres Praha-východ; on 669 there). Katusice, Doubravice and Trnová (on no other sheet), Katusice and Sudoměř
    (okres Mladá Boleslav) are now on 693's circuit.
  - **on a line here and on no other line of this oblast** (to keep in mind when the sibling sheets are compared): Praha-západ:
    Holubice ×4, Horoměřice ×3, Statenice ×2, Tursko, Velké Přílepy ×3 (316, 857); Praha-východ: Bašť ×3, Předboj, u rybníka
    (368), Mratín ×2, Sluhy ×2 (377), Brázdim ×2, Polerady, rozcestí, Veleň, u pomníku (377 Brázdim), Hovorčovice ×2, Měšice
    ×3, Nová Ves [PH] (351), Odolena Voda ×5, Klecany ×2, Klíčany, Zdiby ×3 (370, 372), Veliká Ves (479, 658); Kladno:
    Otvovice ×2, Zákolany ×2 (857).

## Owner checks (1)

1. **The sheet's roadside-stop check.** Six stops with one or two afternoon passings, each near a served stop of the same
   village, are coverage exceptions: Straškov-Vodochody, škola (413 12:10, 14:10; 380 m from Straškov-Vodochody, 413 hourly);
   Vraňany (466 12:50, 14:50; 230 m from Vraňany, škola on 464); Řepín, Libeňská (the 668 Mělnické Vtelno round 15:15 / 16:20;
   660 m from Řepín on 668); Neratovice, Lobkovice, škola, V Lukách, statek (480 13:41; 350, 350, 540 m from Lobkovice,
   hřbitov, 482 every 30). Serving them all costs +2 buses (668 Mělnické Vtelno every 480, 480 every 480 with an empty return)
   plus two routings without a bus (413 back via the school, every trip 5 min longer; 466 out via Vraňany village, a road that
   skips Spomyšl). The design leaves them as exceptions.

## Open for the 2 Nov live map

- The through-running in `notes` (466 ↔ 464 at Spomyšl, 692 ↔ 691 at Liběchov, 476 → 480 at Nedomice, 694 → 692 at
  Kokořín, 475 → 747 at Mělník; cross-sheet 482 with 476 / 470 / 747 at Mělník and 856 → 857 at Kralupy; 349's possible
  0-minute turn at Ládví) — if confirmed, 464 + 466 could become one pool or circuit (the owner's call).
- Which out-of-Prague departures the buses use to go home on the outstation rows (370 Postřižín, 372, 377, 400, 369's
  16:45 / 17:45), and on 464 / 466 at Mělník — the dropped departures were chosen by waits.
- 348's three lines and 316 + 316 Kralupy: whether the real buses swap ends (pooling options).

## Step 4 per leg (from `schedule.json`)

Typed → real: the real time worked out from each typed value, (typed + 61) mod every, shown at its occurrence in (or after
the start of) the model window. Filled = window slots with a real departure within 3 min. Exact / within 3 / trips counts the
leg's own trips 5–23 h.

| Simutrans line | Leg (timed entry) | Typed → real | Window slots | Real in window | Filled | Exact / within 3 / trips, 5–23 h |
|---|---|---|---|---|---|---|
| 348 Obříství (every 60) | Praha, Ládví → Obříství | 35 → :36 | 15:36 16:36 | 15:36 16:36 | 2/2 | 5/7/17 |
| 348 Obříství (every 60) | Obříství → Praha, Ládví | 56 → :57 | 15:57 16:57 | 15:57 16:57 | 2/2 | 4/5/18 |
| 348 Libiš (every 120) | Praha, Ládví → Libiš, obec | 5 → 17:06; 65 → 16:06 | 16:06 17:06 | 16:06 17:06 | 2/2 | 6/6/18 |
| 348 Libiš (every 120) | Libiš, obec → Praha, Ládví | 16 → 17:17; 91 → 16:32 | 16:32 17:17 | 16:32 17:17 | 2/2 | 3/4/19 |
| 348 (every 120) | Praha, Ládví → Neratovice, U Vojtěcha | 20 → 17:21; 50 → 15:51; 80 → 16:21; 110 → 16:51 | 15:51 16:21 16:51 17:21 | 15:51 16:21 16:51 17:21 | 4/4 | 11/11/17 |
| 348 (every 120) | Neratovice, U Vojtěcha → Praha, Ládví | 35 → 15:36; 50 → 15:51; 80 → 16:21; 110 → 16:51 | 15:36 15:51 16:21 16:51 | 15:36 15:51 16:21 16:51 | 4/4 | 7/8/18 |
| 349 (every 15) | Praha, Ládví → Mělník, Podolí | 9 → :10 every 15 | 15:40 15:55 16:10 16:25 16:40 16:55 17:10 17:25 | 15:40 15:55 16:10 16:25 16:40 16:55 17:10 17:25 | 8/8 | 19/19/30 |
| 349 (every 15) | Mělník, Podolí → Praha, Ládví | 13 → :14 every 15 | 15:44 15:59 16:14 16:29 16:44 16:59 17:14 17:29 | 15:44 15:59 16:14 16:29 16:44 16:59 17:14 17:29 | 8/8 | 16/25/32 |
| 368 (every 60) | Praha, Ládví → Předboj | 14 → :15; 32 → :33; 54 → :55 | 15:33 15:55 16:15 16:33 16:55 17:15 | 15:33 15:55 16:15 16:33 16:55 17:15 | 6/6 | 12/18/28 |
| 368 (every 60) | Předboj → Praha, Ládví | 11 → :12; 31 → :32; 51 → :52 | 15:32 15:52 16:12 16:32 16:52 17:12 | 15:32 15:52 16:12 16:32 16:52 | 5/6 | 8/13/31 |
| 369 Štětí (every 60) | Praha, Ládví → Štětí, závod | 59 → :00 | 16:00 17:00 | 16:00 17:00 | 2/2 | 14/14/14 |
| 369 Štětí (every 60) | Štětí, závod → Praha, Ládví (knot Mělník, Mlazice) | 55 → :56 | 15:56 16:56 | 15:56 16:56 | 2/2 | 9/11/15 |
| 369 (every 60) | Praha, Ládví → Mělník, Mlazice | 29 → :30 | 15:30 16:30 | 15:30 16:30 16:45 | 2/2 | 18/18/25 |
| 369 (every 60) | Mělník, Mlazice → Praha, Ládví | 52 → :53 | 15:53 16:53 | 15:53 16:08 16:53 | 2/2 | 11/13/21 |
| 351 (every 30) | Praha, Letňany → Neratovice, železniční stanice | 9 → :10 every 30 | 15:40 16:10 16:40 17:10 | 15:40 16:10 16:40 17:10 | 4/4 | 11/11/27 |
| 351 (every 30) | Neratovice, železniční stanice → Praha, Letňany | 6 → :07 every 30 | 15:37 16:07 16:37 17:07 | 15:34 16:07 16:37 17:07 | 4/4 | 18/23/26 |
| 351 Čakovičky (every 30) | Praha, Letňany → Čakovičky | 24 → :25 every 30 | 15:55 16:25 16:55 17:25 | 15:55 16:25 16:55 17:25 | 4/4 | 13/13/21 |
| 351 Čakovičky (every 30) | Čakovičky → Praha, Letňany | 2 → :03 every 30 | 15:33 16:03 16:33 17:03 | 15:33 16:03 16:33 17:03 | 4/4 | 8/10/20 |
| 316 (every 60) | Praha, Bořislavka → Holubice | 9 → :10; 19 → :20; 39 → :40; 49 → :50; 59 → :00 | 15:40 15:50 16:00 16:10 16:20 16:40 16:50 17:00 17:10 17:20 | 15:40 15:50 16:00 16:10 16:20 16:40 16:50 17:00 17:10 17:20 | 10/10 | 27/29/50 |
| 316 (every 60) | Holubice → Praha, Bořislavka | 6 → :07; 16 → :17; 26 → :27; 36 → :37; 56 → :57 | 15:37 15:57 16:07 16:17 16:27 16:37 16:57 17:07 17:17 17:27 | 15:37 15:57 16:07 16:17 16:27 16:37 16:57 17:07 17:17 17:27 | 10/10 | 16/36/51 |
| 316 Kralupy (every 60) | Praha, Bořislavka → Kralupy nad Vltavou, železniční stanice | 29 → :30 | 15:30 16:30 | 15:30 16:30 | 2/2 | 5/5/11 |
| 316 Kralupy (every 60) | Kralupy nad Vltavou, železniční stanice → Praha, Bořislavka | 27 → :28 | 16:28 17:28 | 16:28 17:28 | 2/2 | 3/5/11 |
| 370 (every 60) | Praha, Kobylisy → Kralupy nad Vltavou, železniční stanice | 19 → :20; 57 → :58 | 14:20 14:58 15:20 15:58 | 14:20 14:58 15:20 15:58 | 4/4 | 7/12/31 |
| 370 (every 60) | Kralupy nad Vltavou, železniční stanice → Praha, Kobylisy | 15 → :16; 55 → :56 | 14:16 14:56 15:16 15:56 | 14:16 14:56 15:16 15:25 15:56 | 4/4 | 8/8/27 |
| 370 Postřižín (every 120) | Praha, Kobylisy → Postřižín, u kapličky | 14 → 15:15; 27 → 15:28; 72 → 14:13; 94 → 14:35 | 14:13 14:35 15:15 15:28 | 14:13 14:28 14:35 14:45 15:15 15:28 15:35 15:45 | 4/4 | 7/9/27 |
| 370 Postřižín (every 120) | Postřižín, u kapličky → Praha, Kobylisy (knot Odolena Voda, Dolní náměstí) | 4 → 15:05; 59 → 16:00; 84 → 14:25; 104 → 14:45 | 14:25 14:45 15:05 16:00 | 14:25 14:45 15:05 16:00 | 4/4 | 5/7/27 |
| 372 (every 120) | Praha, Kobylisy → Kralupy nad Vltavou, železniční stanice | 4 → 17:05 | 17:05 | 17:05 | 1/1 | 3/3/8 |
| 372 (every 120) | Kralupy nad Vltavou, železniční stanice → Praha, Kobylisy | 114 → 16:55 | 16:55 | 16:55 | 1/1 | 2/2/11 |
| 377 (every 120) | Praha, Letňany → Kostelec nad Labem, Martinská | 24 → 17:25; 45 → 15:46; 105 → 16:46 | 15:46 16:46 17:25 | 15:46 16:22 16:46 17:25 | 3/3 | 3/6/26 |
| 377 (every 120) | Kostelec nad Labem, Martinská → Praha, Letňany | 40 → 15:41; 85 → 16:26; 115 → 16:56 | 15:41 16:26 16:56 | 15:41 16:26 16:56 | 3/3 | 6/13/26 |
| 377 Brázdim (every 120) | Praha, Letňany → Kostelec nad Labem, Martinská | 33 → 15:34; 93 → 16:34; 117 → 16:58 | 15:34 16:34 16:58 | 15:34 15:58 16:34 16:58 | 3/3 | 4/10/26 |
| 377 Brázdim (every 120) | Kostelec nad Labem, Martinská → Praha, Letňany | 25 → 17:26; 55 → 15:56; 100 → 16:41 | 15:56 16:41 17:26 | 15:56 16:41 17:26 | 3/3 | 8/15/26 |
| 400 (every 120) | Praha, Letňany → Nový Bor, autobusové nádraží | 29 → 15:30 | 15:30 | 15:30 16:30 | 1/1 | 6/6/12 |
| 400 (every 120) | Nový Bor, autobusové nádraží → Praha, Letňany | 84 → 16:25 | 16:25 | 16:25 | 1/1 | 3/3/6 |
| 400 Varnsdorf (every 120) | Praha, Letňany → Varnsdorf, autobusové nádraží | 69 → 16:10 | 16:10 | 16:10 17:10 | 1/1 | 2/2/7 |
| 400 Varnsdorf (every 120) | Varnsdorf, autobusové nádraží → Praha, Letňany | 87 → 16:28 | 16:28 | 16:28 | 1/1 | 4/4/10 |
| 400 Rumburk (every 480) | Rumburk, železniční stanice → Praha, Letňany | 252 → 21:13 | – | – | 0/0 | 1/1/1 |
| 400 Rumburk (every 480) | Praha, Letňany → Rumburk, železniční stanice | untimed (empty return) | | | | |
| 410 (every 480) | Praha, Letňany → Mimoň, Žitavská | 479 → 17:00 | – | 15:00 | 0/0 | 1/1/2 |
| 410 (every 480) | Mimoň, Žitavská → Praha, Letňany | 326 → 14:27 | 14:27 | 14:27 | 1/1 | 1/1/2 |
| 410 Jablonné (every 480) | Jablonné v Podj., železniční stanice → Doksy, autobusové nádraží | 339 → 14:40 | 14:40 | 14:40 | 1/1 | 1/1/1 |
| 410 Jablonné (every 480) | Doksy, autobusové nádraží → Jablonné v Podj., železniční stanice | untimed (empty return) | | | | |
| 413 (every 60) | Praha, Letňany → Litoměřice, autobusové nádraží | 36 → :37 | 14:37 15:37 | 14:37 15:37 | 2/2 | 13/13/14 |
| 413 (every 60) | Litoměřice, autobusové nádraží → Praha, Letňany | 14 → :15 | 15:15 16:15 | 15:15 16:15 | 2/2 | 10/10/13 |
| 658 (every 90) | Neratovice, železniční stanice → Odolena Voda, závod | 7 → 16:08 | 16:08 | 16:08 | 1/1 | 1/2/8 |
| 658 (every 90) | Odolena Voda, závod → Neratovice, železniční stanice | 50 → 16:51 | 16:51 | 16:10 16:51 | 1/1 | 1/2/8 |
| 663 Úžice (every 480) | Kralupy nad Vltavou, železniční stanice → Úžice, logistické centrum | 25 → 17:26 | – | – | 0/0 | 1/1/3 |
| 663 Úžice (every 480) | Úžice, logistické centrum → Kralupy nad Vltavou, železniční stanice | 74 → 18:15 | – | 14:46 | 0/0 | 1/1/4 |
| 464 (every 120) | Mělník, autobusové nádraží → Horní Beřkovice, točna | 34 → 15:35; 94 → 16:35 | 15:35 16:35 | 15:35 16:35 | 2/2 | 6/6/7 |
| 464 (every 120) | Horní Beřkovice, točna → Mělník, autobusové nádraží | 23 → 17:24; 38 → 15:39 | 15:39 17:24 | 15:39 17:24 | 2/2 | 2/2/4 |
| 466 (every 60) | Mělník, autobusové nádraží → Kralupy nad Vltavou, železniční stanice | 54 → :55 | 15:55 16:55 | 15:55 16:55 | 2/2 | 4/4/11 |
| 466 (every 60) | Kralupy nad Vltavou, železniční stanice → Mělník, autobusové nádraží | 54 → :55 | 15:55 16:55 | 15:55 16:55 | 2/2 | 6/7/12 |
| 468 (every 120) | Černouček → Dolní Beřkovice | 42 → 15:43 | 15:43 | 15:43 | 1/1 | 1/1/5 |
| 468 (every 120) | Dolní Beřkovice → Černouček | 69 → 16:10 | 16:10 | 16:10 | 1/1 | 1/2/5 |
| 473 (every 120) | Neratovice, Kojetická → Kralupy nad Vltavou, železniční stanice | 90 → 16:31 | 16:31 | 16:31 | 1/1 | 4/4/6 |
| 473 (every 120) | Kralupy nad Vltavou, železniční stanice → Neratovice, Kojetická | 114 → 16:55 | 16:55 | 16:55 | 1/1 | 2/3/7 |
| 473 Zálezlice (every 120) | Neratovice, Kojetická → Zálezlice, Kozárovice | 30 → 15:31 | 15:31 | 15:31 | 1/1 | 3/3/4 |
| 473 Zálezlice (every 120) | Zálezlice, Kozárovice → Neratovice, Kojetická | 60 → 16:01 | 16:01 | 16:01 | 1/1 | 1/2/7 |
| 474 (every 60) | Mělník, Na Brabčově → Dobřeň, Střezivojice (knot Mělník, Slovany) | 8 → :09 | 16:09 17:09 | 16:09 17:09 | 2/2 | 11/11/14 |
| 474 (every 60) | Dobřeň, Střezivojice → Mělník, Na Brabčově (knot Mělník, Podolí) | 52 → :53 | 15:53 16:53 | 15:53 16:53 | 2/2 | 6/6/13 |
| 475 (every 60) | Mělník, autobusové nádraží → Horní Počaply | 49 → :50 | 15:50 16:50 | 15:50 16:50 | 2/2 | 11/12/15 |
| 475 (every 60) | Horní Počaply → Mělník, autobusové nádraží | 39 → :40 | 15:40 16:40 | 15:40 16:40 | 2/2 | 7/11/15 |
| 476 (every 60) | Mělník, autobusové nádraží → Nedomice, křížek | 26 → :27 | 15:27 16:27 | 15:27 16:27 | 2/2 | 5/5/8 |
| 476 (every 60) | Nedomice, křížek → Mělník, autobusové nádraží (knot Kostelec nad Labem, náměstí) | 23 → :24 | 15:24 16:24 | 15:24 16:24 | 2/2 | 7/7/12 |
| 479 (every 60) | Neratovice, Kostomlatského → Neratovice, Korycany | 20 → :21 | 15:21 16:21 | 15:21 16:21 | 2/2 | 4/4/8 |
| 479 (every 60) | Neratovice, Korycany → Neratovice, Kostomlatského | 48 → :49 | 14:49 15:49 | 14:49 15:49 | 2/2 | 4/4/9 |
| 646 (every 60) | Mělník, autobusové nádraží → Kralupy nad Vltavou, železniční stanice | 35 → :36 | 15:36 16:36 | 15:36 16:36 | 2/2 | 8/8/15 |
| 646 (every 60) | Kralupy nad Vltavou, železniční stanice → Mělník, autobusové nádraží | 39 → :40 | 15:40 16:40 | 15:40 16:40 | 2/2 | 11/13/15 |
| 668 (every 120) | Mělník, autobusové nádraží → Mšeno | 89 → 16:30 | 16:30 | 16:30 | 1/1 | 1/1/10 |
| 668 (every 120) | Mšeno → Mělník, autobusové nádraží | 29 → 15:30 | 15:30 | 15:30 17:29 | 1/1 | 1/2/9 |
| 689 (every 480) | Mšeno → Stránka, Ostrý | 305 → 14:06 | 14:06 | 14:06 | 1/1 | 1/1/3 |
| 689 (every 480) | Stránka, Ostrý → Mšeno, Hradsko | 314 → 14:15 | 14:15 | 14:15 | 1/1 | 1/1/3 |
| 689 (every 480) | Mšeno, Hradsko → Mšeno | 337 → 14:38 | 14:38 | 14:38 | 1/1 | 1/1/3 |
| 690 (every 120) | Mšeno → Kadlín | 88 → 14:29 | 14:29 | 14:29 | 1/1 | 1/1/6 |
| 690 (every 120) | Kadlín → Mšeno | 101 → 14:42 | 14:42 | 13:15 14:42 | 1/1 | 1/1/7 |
| 691 (every 240) | Mělník, autobusové nádraží → Vidim | 106 → 18:47 | – | – | 0/0 | 1/1/3 |
| 691 (every 240) | Vidim → Mělník, autobusové nádraží | 164 → 15:45 | 15:45 | 15:45 | 1/1 | 1/1/4 |
| 692 (every 240) | Mělník, Pšovka → Kokořín | 203 → 16:24 | 16:24 | 16:24 | 1/1 | 1/1/3 |
| 692 (every 240) | Kokořín → Mělník, Pšovka | 134 → 19:15 | – | – | 0/0 | 1/1/3 |
| 693 (every 480) | Mšeno, železniční stanice → Okna, obec | 287 → 21:48 | – | – | 0/0 | 1/1/1 |
| 693 (every 480) | Okna, obec → Mšeno, železniční stanice | 322 → 22:23 | – | – | 0/0 | 1/1/1 |
| 693 (every 480) | Mšeno, železniční stanice → Katusice | 361 → 23:02 | – | – | 0/0 | 1/1/1 |
| 693 (every 480) | Katusice → Nosálov | 404 → 15:45 | 15:45 | 15:45 | 1/1 | 1/1/2 |
| 693 (every 480) | Nosálov → Mšeno, železniční stanice | untimed (empty return) | | | | |
| 694 (every 480) | Liběchov → Kokořín | 389 → 15:30 | 15:30 | 15:30 | 1/1 | 1/1/3 |
| 694 (every 480) | Kokořín → Liběchov | 342 → 22:43 | – | – | 0/0 | 2/2/3 |
| 695 (every 480) | Mělník, autobusové nádraží → Mšeno | 434 → 16:15 | 16:15 | 16:15 | 1/1 | 2/2/5 |
| 695 (every 480) | Mšeno → Mělník, autobusové nádraží | 254 → 21:15 | – | – | 0/0 | 1/1/3 |
| 696 (every 120) | Mělník, autobusové nádraží → Mšeno | 104 → 16:45 | 16:45 | 16:45 | 1/1 | 1/1/3 |
| 696 (every 120) | Mšeno → Mělník, autobusové nádraží | 44 → 15:45 | 15:45 | 15:45 | 1/1 | 1/1/4 |
| 747 (every 60) | Mělník, autobusové nádraží → Všetaty, železniční stanice | 4 → :05 | 14:05 15:05 | 14:05 15:05 | 2/2 | 7/7/10 |
| 747 (every 60) | Všetaty, železniční stanice → Mělník, autobusové nádraží (knot Byšice) | 9 → :10 | 14:10 15:10 | 14:10 15:10 | 2/2 | 7/7/8 |
| 857 (every 120) | Zákolany → Kralupy nad Vltavou, obchodní centrum | 75 → 16:16 | 16:16 | 16:16 | 1/1 | 3/3/6 |
| 857 (every 120) | Kralupy nad Vltavou, obchodní centrum → Zákolany | 102 → 16:43 | 16:43 | 16:43 | 1/1 | 4/4/6 |

45 Simutrans lines, 108 buses
