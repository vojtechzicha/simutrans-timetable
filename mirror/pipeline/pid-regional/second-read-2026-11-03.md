# PID regional: second read of the five reviewer changes, 3 Nov 2026

Independent of the designers' and reviewers' notes. For each change the real trips were re-read from `oblasti/<id>/data/derived/trips.json`
at the stop where the variant leaves the trunk, both directions, 13:00–19:00, counting every trip that passes the stop wherever it starts
or ends (the 381 reading); the implementation from `data/derived/schedule.json` (each leg's own trips, slots, typed values, running times,
waits, need) and `schedule-log.txt`; the buses from `data/derived/<line>_observed_2026-11-02.json` (already written by the reviewers; not
rerun). The builder's own anchor for every line was recomputed with `lib.line_anchor` (busiest 2 h in 13:00–18:00; stays at 16:00 unless the
busiest window has 2 or more departures more than 15:00–17:00). Rules: `BRANCH_BRIEF.md`, `DESIGN_BRIEF.md`, `bus-schedule-method.md`
Steps 3, 4, 10 and the outstation rule, `kb/rules/bus-sheets.md`, `kb/lessons.md`. No `lines.json`, script or config was edited.

**Verdicts: 1 AGREE, 2 AGREE, 3 AGREE, 4 AGREE, 5 AGREE on the pattern / DISAGREE on three points of the implementation (anchor,
owner check, note).** The one proposed `lines.json` change is on 369 (section 5); it leaves the bus count at 10 and gives the owner the
3-bus option as a check.

---

## 1. Kladensko 306 — new `306 Jeneč` every 60, +2 buses, `306 Hostouň` read at the knot — AGREE

**Read at Jeneč, Lidická, 13:00–19:00** (the Jeneč shorts' terminal; every 306 trip that passes it).

Towards Jeneč and beyond (Zličín departure in brackets):
13:13 Kladno (12:50) · 13:33 **Jeneč end** (13:10) · 14:08 Kladno (13:45) · 14:38 Hostouň (14:15) · 15:08 Kladno (14:45) · 15:28 Hostouň (15:05) ·
**15:48 Jeneč end** (15:25) · 16:08 Kladno (15:45) · 16:28 Hostouň (16:05) · **16:48 Hostouň** (16:25) · 17:08 Kladno (16:45) · 17:28 Hostouň (17:05) ·
**17:48 Jeneč end** (17:25) · 18:08 Jeneč end (17:45) · 18:28 Jeneč, vysílací středisko (18:05) · **18:48 Jeneč end** (18:25).
So at Jeneč, Lidická the afternoon is every 20: :08 Kladno, :28 Hostouň, **:48 four times (15:48, 16:48, 17:48, 18:48)**, the 16:48 being a
Hostouň trip that is 20 min off the Hostouň line's own :28 minute and exactly on the Jeneč one.

Towards Prague:
13:20 Jeneč start · 13:50 Kladno 12:59 · 14:20 Jeneč start · 14:50 Kladno 14:08 · 15:10 Hostouň 14:55 · **15:30 Jeneč start** · 15:50 Kladno 14:59 ·
16:10 Hostouň 15:55 · **16:30 Jeneč start** · 16:50 Kladno 16:10 · 17:10 Hostouň 16:55 · **17:30 Hostouň 17:15** · 17:51 Kladno 17:11 · 18:11 Hostouň 17:56 ·
18:41 Kladno 18:03.
So :50 Kladno, :10 Hostouň, **:30 three times (15:30, 16:30, 17:30)**, the 17:30 being the Hostouň 17:15, 20 min off that line's :10 and on the Jeneč
minute. (13:20 and 14:20 are the earlier phase, 10 min off.)

**Verdict A.** 4 out and 3 back at a repeating minute in 13:00–19:00, read at the stop — the same count and the same mechanism as 381 Zásmuky
(the third trip each way is a trip of another variant passing the point on the branch's minute). The designer's C came from grouping by ends
(only 2 + 2 start or end at Jeneč, Lidická at the :25 / :30 minute). Hourly beats every 120 by Step 4 rule 3 (hourly: 4 + 3 exact over the
afternoon; every 120 at the odd hours: 2 + 2).

**Implementation (schedule.json, anchor 16:00 set by hand in v1, unchanged, window 15:30–17:30):**
- `306 Jeneč` out Zličín :25 → Jeneč, Lidická, `notvia` Kladno: own trips 15:25, **16:25 (→ Hostouň)**, 17:25, 18:25, 19:25 exact; window slots
  16:25, 17:25 = real; rt 23 (15:25 → 15:48). Back Jeneč, Lidická :30 → Zličín: own trips 15:30, 16:30, **17:30 (Hostouň 17:15 → Zličín)** exact;
  window 15:30, 16:30 = real; rt 25. Typed 24 / 29 (loop −1). Need 2 (waits 30 at Zličín, 42 at Jeneč).
- The split works as described: both lines' out legs are now read between Zličín and Jeneč, Lidická with the same `notvia`, so the builder
  assigns each trip to the nearer slot (:05 Hostouň / :25 Jeneč); the Hostouň out leg's own trips are 15:05, 16:05, 17:05 (exact) only. The
  Hostouň back leg is read at the knot Jeneč, Lidická (`knot_at` 10, `knot_rt` 15): own trips 14:55, 15:55, 16:55, 17:56 exact / 1 off; typed
  value at Hostouň still 54 (:55). Nothing else on 306 moved (306 Kladno :45 / :10 and 306 Hostivice every 20 identical to v1).
- Live map (2 Nov, verified in the observed file): 8774 ran Jeneč 15:25 → 15:48, 16:30 → 16:55, then Hostouň 17:05 and 17:56; 8795 ran Jeneč
  15:30, Hostouň 16:05 / 16:55, Jeneč 17:45; the Hostouň 16:25 / 17:15 pair was 8811 (a Kladno-course bus). One Jeneč + Hostouň circuit in
  the game would be 35 + 15 + 40 + 50 + 23 + 42 + 25 + 10 = 240 min → 4 buses, the same as 2 + 2, so no pooling option: as the card says.
- Card: full stop names, the Jeneč :48 / :30 reading and the shared buses stated. Fine.

## 2. Rakovnicko 415 — new `415 Žatec` every 120, +1 bus — AGREE

**Read at Žatec, autobusové nádraží, 13:00–19:00.**

Towards Kadaň (all from Zličín; Zličín departure in brackets): 13:30 (11:40) · **14:35 (13:05)** · 15:35 (14:15) · **16:30 (14:40)** · 17:30 (16:10) ·
**18:30 (17:00)**. Hourly at :30–:35. The 415 slots (Zličín 16:10 every 120) pass at 13:30, 15:35, 17:30; the even hours **14:35, 16:30, 18:30 are
three trips at :30 ± 5** that 415 can only list (at Zličín they are 55, 30 and 50 min off its slot).

Towards Žatec / Prague (from Kadaň; Kadaň departure in brackets): 13:30 (12:50 → Zličín) · **14:30 (13:47 → Zličín via Nové Strašecí)** · 15:30
(14:47 → Zličín) · **16:25 (15:47, ends Žatec)** · 17:30 (16:50 → Zličín) · **18:25 (17:50, ends Žatec)**. Hourly at :25–:30; the 415 slots (Kadaň
:50 every 120) pass at 13:30, 15:30, 17:30; the even hours **14:30, 16:25, 18:25 are three trips at :25–:30**, two of them Kadaň → Žatec shorts.

Read at Kadaň the same shows as arrivals :05–:13 hourly (13:05 … 19:05) and departures :47–:50 hourly (12:50, 13:47, 14:47, 15:47, 16:50, 17:50,
18:50): Žatec – Kadaň is hourly both ways from 13:30 to 18:30, every 120 in v1.

**Verdict A.** 3 each way at a repeating minute, read at the stop. Not D: the trips back exist (two shorts and the 13:47). The designer filed C
because at Zličín and Kadaň the Prague end has no fixed minute, which is true of the Prague end and is already handled there by the outstation
rule (415 at the inbound every-120 rate, the Zličín 13:05, 14:15, 14:40, 17:00 listed). The 1-bus Kadaň – Žatec shuttle is the cheapest model
that gives the section its real hourly service, offset from 415 so the two never coincide (Kadaň → Žatec :47 odd / :50 even hours, Žatec → Kadaň
:30 even / :30–:35 odd).

**Implementation (anchor 16:00 set by hand in v1, unchanged, window 15:30–17:30):**
- Out Kadaň 15:47 → Žatec, `notvia` Praha, Zličín: own trips 15:47 (exact), 17:50 (3 off), 20:40 (off); window slot 15:47 = real. rt 38
  (15:47 → 16:25, via the Chbany villages as that trip runs). Typed 46 ((947 − 61) mod 120).
- Back Žatec 16:30 → Kadaň, `via` Nové Strašecí, Palackého: own trips 08:35 (5 off), 13:30 (off), 16:30 (exact), 20:30 (exact); window slot
  16:30 = real. rt 35 (16:30 → 17:05). Typed 89. The `via` is a device: of the three even-hour trips towards Kadaň only the 14:40 runs via Nové
  Strašecí, so the leg counts one of the three (the other two, Zličín 13:05 and 17:00, stay on 415 as off its pattern); the why says exactly
  this. No cleaner filter exists: all Žatec → Kadaň trips call at the same Žatec stops, and reading 415's own out leg at Žatec instead would
  fail its Step 4 (the 14:15 passes Žatec at 15:35, 5 off). Acceptable.
- Need 1 (waits 42 at Kadaň, 5 at Žatec). 415 itself unchanged (3 buses).
- Live map: 8385 (course 304/12) Zličín 13:05 → Kadaň → 15:47 → Žatec, then 584 towards Rakovník; 8409 (304/20) Zličín 14:40 → Kadaň → 17:50 →
  Žatec 18:25, then 584 Krupá, Šustna 18:51 → Rakovník. So the shorts are Rakovník buses on their way home via Žatec; "came from Prague" on the
  card is true, the home is Rakovník. Card nuance only.

## 3. Praha-západ 340 / 359 — `340` 4 slots + new `340 Masarykova`, same 6 buses, back leg `lay` 0 — AGREE

**Read at Roztoky, nádraží and Roztoky, Masarykova, 13:00–19:00.**

340 out of Dejvická, at nádraží: from 15:11 eight an hour, :25 :31 :37 :55 :01 :07 (Dejvická :11 :17 :23 :41 :47 :53, to Přemyslovská by the
direct road via Tyršovo náměstí, u rybníčku, rozcestí Žalov) and **:43 :13 (Dejvická :29 :59), ending at nádraží** — 15:29, 15:59, 16:29, 16:59,
17:29, 17:59 (+ 13:20, 14:25, 14:58, 18:28, 18:59). Each of these is followed the same minute by a 359 round nádraží :43 / :13 → Tyršovo
náměstí, 17. listopadu, **Masarykova :46 / :16**, Solníky, Obránců míru, rozcestí Žalov → Levý Hradec :53 / :23 — 10 rounds 13:00–19:00
(13:37, 14:42, 15:15, 15:46, 16:16, 16:46, 17:16, 17:46, 18:16, 18:45 at Masarykova).
Back: Levý Hradec :02 :09 :24 :32 :54 by the direct road, and the 359 round **Levý Hradec :39 → Masarykova :44 → nádraží :50** → 340 nádraží :50
→ Dejvická: 4 rounds (14:37, 15:39, 16:39, 17:41 from Levý Hradec).
Towards Levý Hradec via Masarykova: 10 trips at :16 / :46; back via Masarykova: 4 at :42–:46. Plus 359 Suchdol – Maxmiliánka hourly each way
through the same four town stops.

**Verdict A (path variant).** The :29 / :59 trips run a different road through Roztoky and do so every 30 minutes all afternoon; by the 381
rule and the owner's 329 rule (say which road a row runs; one line per path where both run regularly) they are their own Simutrans line. The
v1 line sent them by the direct road, so 17. listopadu, Masarykova, Solníky and Obránců míru had one bus an hour each way (359) where
reality has three towards Levý Hradec.

**Implementation (anchor 16:00, the builder's own — busiest 15:10–17:10 has 28 departures, 15:00–17:00 27 — window 15:30–17:30):**
- `340` out Dejvická :11 :17 :41 :47, `via` Roztoky, Tyršovo náměstí: own trips are only the Přemyslovská / Levý Hradec trips (the
  nádraží-ending :29 / :59 no longer count here); window 8 slots against 12 real (the :23 / :53 are the outstation remainder, as in v1 where it
  was 12 against 16), all 8 exact. Back read at the knot nádraží :10 :17 :40 :50 (Levý Hradec :02 :09 :32 :42, typed 1 8 31 41): window 8 = 8
  real, all exact. `lay` 0: the real turns are 0 min for the :11 and :41 buses (2 Nov: 8760 Dejvická 15:11 → Přemyslovská 15:32 → Levý Hradec
  15:32; 1469 16:41 → 17:02 → 17:02), 1 min for the :47 (1896 15:47 → 16:08 → 16:09) and 4 min for the :17 (whose real bus runs the 359 round at
  :39); the builder's waits at Levý Hradec come out [0, 1, 0, 4], need 4. This is the brief's "real 0-minute turn, say which" case and the why
  says which.
- `340 Masarykova` out Dejvická :29 :59 → nádraží, `notvia` Tyršovo náměstí: own trips 14:58, 15:29 … 18:59, window 4 = 4 real, exact; rt 14;
  typed 28 58. Untimed nádraží → Levý Hradec with `lines: ["359"]`: stops from the 359 rounds (Tyršovo náměstí, 17. listopadu, Masarykova,
  Solníky, Obránců míru, rozcestí Žalov, Přemyslovská), rt 9 (real 10; irrelevant to the typed values). Back read at the knot nádraží :02 :32
  (Levý Hradec :24 :54, typed 23 53), `lay` 1 (the round arrives :23 / :53, the 340 leaves :24 / :54 — 2 Nov: 8800 15:59 → 16:13 round → 16:24
  back, 17:59 → 18:13 …; 8814 15:29 → 15:43 → 15:54, 16:29 → 16:43 → 16:54, 17:29 → 17:43). Window 4 = 4 real, exact. Need 2. 4 + 2 = 6 = v1.
- `via` / `notvia` Tyršovo náměstí separates the two out legs cleanly (verified on both trip lists); the two back legs share the knot reading
  and split by nearest slot (:02 / :32 → Masarykova, :10 :17 :40 :50 → 340), verified.
- What stays simplified, stated on the 359 card: the hourly Levý Hradec :39 round back through the town (4 trips) is carried by 340's :42
  slot on the direct road, so towards nádraží the four town stops keep 359's hourly only. That is the content behind the remaining
  `[EACH WAY] 359 (340 Masarykova, 359)` flag at rozcestí Žalov (its 10 → trips are the untimed leg's rounds, an audit artefact; its 4 ← are
  these :39 rounds). A 0-bus way to model it would be a third line (Dejvická :17 → Přemyslovská direct, Levý Hradec :39 → town round → nádraží
  → Dejvická, 1 bus taken from 340's 4) at the cost of a third line to type; I do not require it — the written reason is the 329-style
  note, and the owner accepted that for 329. Record the flag as explained, not clean.

## 4. Mělnicko 466 — town end to obchodní centrum, new `466 Nelahozeves` every 60, +2 buses — AGREE

**Read at Nelahozeves, u starého mostu, 13:00–19:00** (the Kralupy – Nelahozeves shorts' terminal).

Towards Nelahozeves / Mělník (from Kralupy): 13:14 OC 12:45 → Mělník · 14:14 OC 13:45 → Spomyšl · 15:14 OC 14:45 → Mělník · **15:44 station 15:25 →
Veltrusy** · 16:14 OC 15:45 → Spomyšl · **16:44 station 16:25 → u starého mostu (end)** · 17:14 OC 16:45 → Mělník · **17:44 station 17:25 → u starého
mostu (end)** · 18:14 station 17:55 → Mělník · **18:44 OC 18:15 → Nová Ves**. So :14 hourly (the Mělník trips) and **:44 four times (15:44, 16:44,
17:44, 18:44)**.
Towards Kralupy: 13:41 Mělník 12:50 · 14:41 Mělník 13:55 · 15:41 Mělník 14:50 · **16:11 Veltrusy 16:06 → OC** · 16:41 Mělník 15:55 · **17:11 u starého
mostu start** · 17:41 Mělník 16:55 · **18:11 u starého mostu start** · 18:41 Mělník 18:00. So :41 hourly and **:11 three times (16:11, 17:11, 18:11)**.
From 15:14 the Kralupy – Nelahozeves road has a bus every 30 minutes each way. The :25 / :11 minute is also the morning's (07:30 / 08:11) and
the evening's (20:25 / 21:07).

**Verdict A.** 4 out, 3 back at a repeating minute, read at the stop. The designer's C ("2 + 2 to Nelahozeves, the rest to Veltrusy / Nová
Ves") is the grouping by ends. The stops beyond u starého mostu (u kaštanu, Veltrusy, Staré Ouholice, Nová Ves) are on 466's own legs.

**Town end.** At obchodní centrum: departures towards Mělník 12:45, 13:45, 14:45, 15:45, 16:45, 18:15 (the 17:55 starts at the station);
arrivals from Mělník 14:10, 15:10, 18:12 (12:50, 13:55, 16:55), the 14:50, 15:55 and 18:00 end at the station. Both window slot trips out of
Kralupy (15:45, 16:45) start at obchodní centrum, so the 314 rule puts the Kralupy end there; the station stays the timed knot on the way back
(`knot_at` 55, so the 17:55 counts) and `core_to` on the way out (so the station-ending 14:50 / 15:55 count). Right.

**Implementation (anchor 16:00, the builder's own — busiest 15:20–17:20 has 9, 15:00–17:00 8 — window 15:30–17:30):**
- `466`: out Mělník :55 → obchodní centrum, `core_to` station: window 15:55, 16:55 = real, exact; rt 77 (16:55 → 18:12). Back obchodní centrum
  :45 (typed 44) read at the knot station :55: window 15:45, 16:45 = real, exact; `rt` 81 by hand (obchodní centrum 13:45 → Spomyšl 14:44 = 59,
  plus 22 Spomyšl → Mělník; the builder's median of 94 mixed the Lužec road) — stated in the why. Need 4 as before.
- `466 Nelahozeves`: out station :25 → u starého mostu, `notvia` Spomyšl, Hořín, Brozánky: own trips 15:25 (→ Veltrusy), 16:25, 17:25, 18:25
  (obchodní centrum 18:15), 20:25, 22:25 exact, 05:32 / 07:30 / 18:55 off; no Mělník trip (verified). Window 16:25, 17:25 = real. Back u starého
  mostu :11 → station: own trips 05:11, 08:11, **16:11 (Veltrusy 16:06)**, 17:11, 18:11, 21:11 exact; window 16:11, 17:11 = real. rt 19 / 19.
  Typed 24 / 10. Need 2 (waits 55 at the station, 27 at Nelahozeves).
- Live map (verified): 8058 Mělník 14:50 → station 16:00, 16:25 → Nelahozeves, 17:11 back, 17:55 → Mělník; 8081 Mělník 15:55 → 17:00, 17:25 →
  Nelahozeves, 18:11 back, 18:55 → u kaštanu; 8077 ran the Veltrusy pair 15:25 / 16:06 and then obchodní centrum 16:45 → Mělník. The shuttles
  are the Mělník buses' layover work, so 466 + 466 Nelahozeves as one circuit (Mělník → Kralupy → Nelahozeves → Kralupy → Mělník, 300 min) would
  need 5 buses instead of 4 + 2 — the pooling fact is in `notes`, not applied, as the rules say. Game 6 buses against 6 real on 466 in the
  afternoon (8109, 8019, 8058, 8081, 8077, 1058).
- Card: full names, the reading at u starého mostu stated, the three direct trips (14:45, 16:45, 17:55 via Nové Ouholice) named — that is the
  remaining ONE WAY flag at Nové Ouholice. Fine.

## 5. Mělnicko 369 — second hourly slot (Ládví :45, Mlazice :08 at the knot Podolí :12), anchor 15:30, 7 → 10 buses — AGREE on the pattern, DISAGREE on the anchor, the missing owner check and one sentence of the note

**Read at Praha, Ládví and Mělník, Podolí, 13:00–19:00, every trip, both lines.**

Ládví out: 13:00 Štětí · 13:30 Mlazice · 14:00 Š · 14:30 M · 15:00 Š · 15:30 M · **15:45 Podolí** · 16:00 Š · 16:30 M · **16:45 Mlazice** · 17:00 Š ·
17:30 M · **17:45 Mlazice** · 18:00 Š · 18:30 M. The :45 stream: **15:45, 16:45, 17:45** — three trips at one minute (and 07:45 in the morning).
Podolí towards Prague: 13:27 (Štětí 13:01) · 13:57 (Mlazice 13:53) · **14:12 Podolí start** · 14:27 Š · 14:57 M · **15:12 Podolí start** · 15:27 Š ·
15:57 M · **16:12 (Mlazice 16:08)** · 16:27 Š · 16:57 M · 17:27 Š · 17:57 M · 18:27 Š · 18:57 M. The :12 stream: **14:12, 15:12, 16:12** — three
trips at one minute.
So the Ládví – Mělník road runs three an hour each way in the peak: :00 / :30 / :45 out of Ládví, :27 / :57 / :12 at Podolí — but the third
stream runs **15:45–17:45 out and 14:12–16:12 back**, two and a half hours each way, offset by about an hour and a half between directions.

**Is it a pattern the rules model?** It is 3 each way at a repeating minute in 13:00–19:00, counted at the core points (the 15:45 passes
Mělník, autobusové nádraží, a listed core point, so Step 3 counts it on the Ládví → Mlazice direction even though it ends at Podolí; the
14:12 and 15:12 are read at the knot Podolí). It is not a branch or a path variant but an extra peak frequency on the trunk, half of it short
workings to or from Podolí. The method models the afternoon peak ("442 is hourly at midday and 5 an hour in the afternoon, so it is modelled
at 5 an hour"; the owner on 23: "a used branch in afternoon peak; just not at 16:00 exactly"), so the question is what Step 4 says in the
model window.

**Step 4, computed from trips.json for the Mlazice line (notvia Štětí), one-slot row (Ládví :30 / Podolí :57) against two-slot (:30 :45 /
:57 :12):**

| window | out :30 only | out :30 :45 | back :57 only | back :57 :12 |
|---|---|---|---|---|
| **15:30–17:30 (the builder's own anchor 16:00)** | 2 slots vs **4 real** (15:30 15:45 16:30 16:45): **count fails** | 4 = 4, all exact | 2 slots vs 3 real (15:57 16:12 16:57): passes | 4 slots vs 3 real, **17:12 empty**: 3/4 = 75 %, **fill fails** |
| 15:00–17:00 (the reviewer's anchor 15:30) | 2 vs 4: fails | 4 = 4 exact | 2 vs 4 (15:12 15:57 16:12 16:57): fails | 4 = 4 exact |
| 14:50–16:50 (the builder's busiest stretch) | 2 vs 4: fails | 4 = 4 exact | 2 vs 4: fails | 4 = 4 exact |
| 15:10–17:10 (tied busiest) | 2 vs 4: fails | 4 = 4 exact | 2 vs 4: fails | 4 = 4 exact |
| 14:30–16:30 | 2 vs 3: passes | 14:45 empty: fails | 2 vs 4: fails | 4 = 4 exact |
| 16:00–18:00 | 2 vs 4: fails | 4 = 4 exact | 2 vs 3: passes | 17:12 empty: fails |

- **The one-slot row passes Step 4 in no afternoon window** once the 15:45 is counted. In v1 it passed in 15:30–17:30 only because the leg was
  read to Mlazice (`core_to` Mlazice), which dropped the 15:45 — the start/end grouping the 381 lesson is about. The reviewer's note sentence
  "the one-slot row … also passes Step 4 by one trip's tolerance" is therefore wrong for the row as now defined: in the window the note names
  (15:00–17:00) it fails both legs, 2 slots against 4 departures.
- **The two-slot row is exact both ways in every window that starts 14:50–15:12**, including the builder's own busiest stretch 14:50–16:50
  (12 departures of the line; 15:00–17:00 and 15:30–17:30 have 11; the builder stays at 16:00 because the difference is under 2). In the
  builder's default window 15:30–17:30 it is exact out of Ládví and has **one empty slot back (17:12)**: the stream's last trip back is 16:12.
- **The anchor.** `"anchor": "15:30"` was set by hand; `line_anchor` on 369's trips gives 16:00 (busiest [14:50, 16:50], 12, against 11 at
  15:00–17:00; not moved). The note's "window 15:00–17:00, the line's busiest two hours" is not what the builder's measure says (it is a tie
  with 15:30–17:30 at 11; the busiest is 14:50–16:50 at 12). So the anchor was moved to the one window where the row audits clean. The move does
  not manufacture the pattern — the row is exact in the builder's own busiest stretch too — but it hides that in the method's default window the
  back row is approximate (3 of 4 slots), and an approximate row with a cheaper option is exactly what the brief keeps owner checks for.
- **Exact over the day** (fit window 05:00–23:00): out two-slot 22 of 28, one-slot 18 of 28 (the :45 adds 07:45, 15:45, 16:45, 17:45 and nothing
  else); back two-slot 14 of 23, one-slot 11 of 23 (the :12 adds the three stream trips). The second slot stands for 4 + 3 real trips a day and
  runs about 19 times a day in the game. That is the same ratio as 381 Zásmuky (4 / 3, 3 buses, the owner's worked example), 306 Jeneč (5 / 3)
  and 466 Nelahozeves (4 / 3) today.
- **Buses.** Two slots: 369 6 + 369 Štětí 4 = 10; one slot: 3 + 4 = 7. Live map 2 Nov (verified): 369's :00 / :30 pattern ran on seven 369-course
  buses (8272, 8232, 8275, 8269, 8276, 8282, 8233); the six stream trips ran on four 349-course buses between 349 trips (8203: 369 14:12 then 349
  15:40; 8213: 369 15:12 and 16:45; 8206: 349 13:50, 14:50, 369 15:45, 349 16:54; 8205: 349 15:10, 369 16:08 and 17:45). Real 349 used 9 buses
  and 369 7, 16 in all; the game has 349 at 7, so 349 + 369 is 14 with one slot and 17 with two. The two-slot model is the one nearer the real
  fleet; the +3 is the price of not pooling, and pooling is a card option, not applied.
- Implementation otherwise right: slots real (Ládví 15:30 15:45 16:30 16:45 all exact; Podolí 14:12 15:12 15:57 16:12 16:57 exact, Mlazice 16:08 →
  Podolí 16:12 with `knot_rt` 4), `core_to` Podolí makes the 15:45 count, the knot at Podolí reads the 14:12 / 15:12 starts, rt 53 / 58 as the
  trips run, typed 29 44 / 52 7, need 6 (waits 24 / 54 at Ládví, 45 / 15 at Mlazice), 369 Štětí unchanged and exact in both windows (Ládví 16:00
  17:00; Štětí 15:56 16:56 read at Mlazice :23).

**So: a second slot is what Steps 3 and 4 give at the peak, and the one-slot row is not a passing alternative — it is the slower option.** By
Step 4 rule 4 (the pattern at the real rate, marked approximate, on the To check list with the slower option) and bus-sheets.md ("Never
silently pick the busier pattern"), the row stays, the anchor goes back to the builder's, and the choice goes to the owner as a check — which
is also the brief's own definition of a permitted check ("an approximation with its slower option"). Keeping the 15:30 anchor would be
tolerable only with the note corrected and the check added anyway; I recommend removing it so the audit shows the empty 17:12 the check is about.

**Proposed `oblasti/melnicko/lines.json` changes (old → new):**

(a) `lines.369`: remove the hand anchor.
```
old:   "anchor": "15:30"
new:   (key removed; the builder's anchor is 16:00, window 15:30–17:30)
```

(b) `lines.369.note`, the sentence beginning "Two Simutrans lines:":
```
old:   Two Simutrans lines: 369 Štětí hourly, and 369 with two slots an hour (Ládví :30 and :45, Mlazice :53 and :08), modelled at 15:30 (window 15:00–17:00, the line's busiest two hours), where both slots are exact each way (the one-slot row, Ládví :30 and Mlazice :53 only, also passes Step 4 by one trip's tolerance and would need 3 buses instead of 6; the two-slot row has more exact hits, so it is the one kept).
new:   Two Simutrans lines: 369 Štětí hourly, and 369 with two slots an hour (Ládví :30 and :45, Mlazice :53 and :08), the second slot being this peak stream. In the 15:30–17:30 window it is exact out of Ládví and has one empty slot back (17:12: the stream's last trip back is 16:12), so the row is approximate there and the one-slot row (Ládví :30 and Mlazice :53 only, 3 buses instead of 6, the :45 / :12 trips listed) is the option on the owner check; a one-slot row does not pass Step 4 in any afternoon window once the 15:45 is counted (4 departures against 2 slots).
```

(c) `lines.369.sim[1].why` (the `369` line), the sentence "Both slots exact each way in the window; the :45 / :12 slot runs 14:12–18:38 in reality, on 349 buses.":
```
old:   Both slots exact each way in the window; the :45 / :12 slot runs 14:12–18:38 in reality, on 349 buses. 6 buses.
new:   Out of Ládví both slots are exact in the window; back, the :12 slot stands for Podolí 14:12, 15:12 and Mlazice 16:08 (17:12 has no trip). The :45 / :12 stream runs 14:12–18:38 in reality, on 349 buses. 6 buses.
```

(d) `owner_checks`: append one row (the existing roadside-stop row stays).
```
new row:
["369",
 "Second hourly slot (Ládví :45, Mlazice :08) for the afternoon stream Ládví 15:45, 16:45, 17:45 and Podolí 14:12, 15:12, Mlazice 16:08: three each way at one minute, but it runs 14:12–17:45 only, so in the 15:30–17:30 window the :12 slot at 17:12 has no trip (approximate; exact in 14:50–16:50). On 2 Nov the six trips ran on 349 buses 8203, 8205, 8206 and 8213 between their 349 trips. 6 buses on 369, 10 with 369 Štětí.",
 "One slot only, Ládví :30 and Mlazice :53, with the :45 / :12 trips listed: 3 buses on 369 (7 with 369 Štětí), saves 3. Or keep the two slots and pool 369 with 349, whose buses run the stream (real 349 + 369 ran 16 buses on 2 Nov; the game has 7 + 10 = 17)."]
```

After (a) `run_oblast.py melnicko` will show the 369 back leg with `empty 1` (17:12) in Step 4; that is the approximation the check explains.
Bus effect of the change: **0** as applied (10 buses on 369 stay); **−3** if the owner takes the one-slot option.

---

## Summary

| # | change | my reading at the stop (13:00–19:00) | verdict | buses | bus effect of my change |
|---|---|---|---|---|---|
| 1 | Kladensko 306 Jeneč every 60 (+2); 306 Hostouň read at the knot Jeneč, Lidická | Jeneč, Lidická: out :48 ×4 (15:48, 16:48 Hostouň, 17:48, 18:48), back :30 ×3 (15:30, 16:30, 17:30 Hostouň); both window legs exact; legs split by nearest slot, Hostouň typed values unchanged | **AGREE** (A) | 8 → 10 | 0 |
| 2 | Rakovnicko 415 Žatec every 120 (+1) | Žatec: even hours 14:35 / 16:30 / 18:30 towards Kadaň, 14:30 / 16:25 / 18:25 towards Žatec, against 415's odd-hour slots; shuttle legs 15:47 / 16:30 exact, isolated by `notvia` Zličín and `via` Nové Strašecí (a device, stated on the card) | **AGREE** (A) | 3 → 4 | 0 |
| 3 | Praha-západ 340 → 340 (4 slots, lay 0) + 340 Masarykova (:29 / :59 via the town) | Masarykova: 10 rounds towards Levý Hradec at :16 / :46, 4 back at :42–:46; both lines exact in the window; 0-minute turns are real (8760, 1469); the :39 round back stays on 340's :42 direct slot, said on the 359 card (residual flag explained, not clean) | **AGREE** (A, path variant) | 6 → 6 | 0 |
| 4 | Mělnicko 466 end at obchodní centrum + 466 Nelahozeves every 60 (+2) | u starého mostu: out :44 ×4 (15:44 Veltrusy, 16:44, 17:44, 18:44 Nová Ves), back :11 ×3 (16:11 Veltrusy, 17:11, 18:11); window legs exact; `notvia` Spomyšl / Hořín, Brozánky keeps every Mělník trip out; obchodní centrum is where 5 of 6 departures start | **AGREE** (A) | 4 → 6 | 0 |
| 5 | Mělnicko 369 second slot (Ládví :45, Mlazice :08 via knot Podolí :12), anchor 15:30 (+3) | Ládví 15:45, 16:45, 17:45; Podolí 14:12, 15:12, 16:12 — 3 each way at one minute. Two-slot row exact in 14:50–17:10 windows, one empty slot (17:12) in the builder's 15:30–17:30; one-slot row fails Step 4's count in every afternoon window once the 15:45 counts. Anchor moved by hand; note claims the one-slot row passes (false) | **AGREE on the two slots; DISAGREE on anchor 15:30, no owner check, note sentence** → remove the anchor, add the owner check with the 3-bus option, fix note and why | 7 → 10 | **0** (−3 if the owner takes the option) |

Totals as applied: Kladensko 163, Rakovnicko 48, Praha-západ 90, Mělnicko 115 — unchanged by this read; Mělnicko 112 if the owner chooses the
one-slot 369.
