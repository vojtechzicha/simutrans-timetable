# Method check: PID Rakovnicko (okres Rakovník, prefix 310), 1–2 Nov 2026

The pilot oblast of the PID regional sheets, designed by hand line by line with `../../DESIGN_BRIEF.md` and the bus schedule
method v4 (`../../../bus-schedule-method.md`). The design is `lines.json` in this folder; `python -X utf8
pid-regional/scripts/run_oblast.py rakovnicko` rebuilds `data/derived/schedule.json` and the three audits.

**2 Nov 2026 revision.** The independent review (`review-2026-11-01.md`: 11 PASS, 12 FIX, 1 ASK) was applied, with the owner's
decision on its ASK (571, 2 Nov: "Yes, serve every place": every stop no other modelled line serves gets a Simutrans line, also
outside the Středočeský kraj) and the brief's new section "Learned on the pilot". Changes: 561 Řeřichy dropped (no stop of its
own); 562 Lubná back on the 15:54 (3-min turn) and out on the 15:30's direct path; 0-minute turns (573, 584, 584 Vinařice) with
the real running times and `lay` 0; 574 and 571 stay (owner); the out-of-kraj stops now count, so 415 is shown via the Chbany
villages out and Želeč / Deštnice back, 711 runs to Louny, Luna and gains 711 Domoušice, and 760 comes back via Podbořany,
nemocnice; owner checks 13 → 1 (the roadside stops); card text short and without abbreviations. The 1 Nov reasoning per line is
kept below, with the 2 Nov change under it; where they differ the change wins.

- **Data:** PID GTFS of 1 Nov 2026, service day Mon 2 Nov 2026 (school day): `data/derived/trips.json`, the whole-day reading
  `data/derived/reading/<L>.txt`. The live map of 2 Nov had only the early morning when this was run (the reading says
  "live: yes"); the afternoon plate chains were not available, so the chain questions are in `notes` for the live map.
- **Step 4**, per leg: in the Simutrans line's model window (anchor −30 … +90) the slots equal the real departures ±1, and
  ≥ 80 % of the slots have a real departure within 3 min; then most exact over the day (5–23), then within 1, then the
  simplest; on one-departure-per-window lines the real 13–18 h headway decides. Both directions were searched together (every
  interval of the method's list, 1–8 slots on the window's real departures, the same count both ways, need by the builder's
  slot matching), then set by hand.
- **Typed values** are (real − 61) mod every: every terminus is a loop; the builder writes them.
- **How it was run (2 Nov):** `pid-regional/scripts/run_oblast.py` as found at 05:22 on 2 Nov does not parse (line 40:
  `print(f"` followed by a line break, an unterminated f-string). I did not edit it; I ran the same file in memory with that
  one line break written as `\n` (scratch wrapper), so every step and check is the script's own.
- **Result:** 24 lines → 22 modelled as **30 Simutrans lines, 47 buses**; 570 and XS75 (992075) not modelled. Step 4 audit: 60
  timed legs, 59 ok, 1 FEWER (404 out of Zličín, the outstation case the owner approved on 290). Branch audit: 12 legs read at a
  midpoint, all `[ok]`. Path audit: 3 flags, explained (415, 575, 760). No "SLOT WITHOUT A REAL TRIP"; the "no slot in the
  window" legs are named below. Coverage: 4 okres-310 stops and 2 out-of-kraj stops not on a line, each with a reason; one owner
  check.

## Summary

| Line | Simutrans lines (every) | Slots, real minutes (out / back) | Buses |
|---|---|---|---|
| 304 | 304 (120) | Rakovník 15:30, 16:00, 16:40 / Kukulova 15:58, 16:53, 17:23 | 5 |
| 305 | 305 (60) | Zličín :05 / Karlovy Vary :30 | 5 |
| 404 | 404 (120) | Zličín :40 (14:40, 15:40) / Kralovice 14:40, 15:45 | 4 |
| 415 | 415 (120) | Zličín 16:10 / Kadaň 16:50 | 3 |
| 417 | 417 (60) | Zličín :50 / Mšec :20 | 3 |
| 560 | 560 (120), 560 Kolešovice (120) | Rakovník 15:00 / Kryry 16:14 (Hořovičky 16:22); Rakovník 16:00 / Kolešovice 15:30 | 1 + 1 |
| 561 | 561 (240) | Šamotka 14:10 / Kolešovice 16:30 (the real 20:30) | 1 |
| 562 | 562 (120), 562 Lubná (240) | garáže 15:35 / hasičský záchranný sbor 14:18; Rakovník 15:30 / Lubná, závod 15:54 | 1 + 1 |
| 563 | 563 (180) | Rakovník 17:30 (14:30) / Mutějovice 15:54 | 1 |
| 570 | not modelled (Step 8) | – | 0 |
| 571 | 571 (480) | Rakovník 14:50 / Chříč 15:30 | 1 |
| 572 | 572 (120), 572 Slabce (480) | Rakovník 15:00 / Krakovec 15:30; Rakovník 18:30 / Slabce, pošta 16:44 | 1 + 1 |
| 573 | 573 (120), 573 Šípy (480) | Čistá 14:15 / Hořovičky 15:08; Čistá 15:30 / Břežany 15:57 | 1 + 1 |
| 574 | 574 (480) | Skryje 17:20 / untimed return | 1 |
| 575 | 575 (144) | Rakovník 14:35, 16:59 / Zvíkovec 15:35 (Slabce, Kostelík 15:45) | 1 |
| 576 | 576 (240) | Rakovník 14:40 / Skryje 16:04 | 1 |
| 577 | 577 (240) | Rakovník 16:35 / Stochov, Slovanka II 14:46 | 1 |
| 578 | 578 (240, circular) | Rakovník 14:45 → Rakovník | 1 |
| 579 | 579 (240, circuit) | Branov 14:35 → Nezabudice 15:23 → Branov 13:30 (17:30) → Leontýn 14:17 (18:17) | 1 |
| 581 | 581 (120), 581 Nové Strašecí (240), 581 Senomaty (240) | Rakovník 15:30 / Lišany 16:25; Rakovník 16:30 / Pecínov 14:07; Rakovník 17:10 / Senomaty 17:33 | 1 + 1 + 1 |
| 584 | 584 (120), 584 Vinařice (480) | Rakovník 13:15 / Lhota 14:00; Rakovník 14:30 / Vinařice 15:25 | 1 + 1 |
| 711 | 711 (240), 711 Domoušice (480) | Rakovník, železniční zastávka západ 14:20 / Louny, Luna 15:55 (autobusové nádraží 16:00); Louny 14:00 / Solopysky 14:30 | 1 + 1 |
| 760 | 760 (60) | Rakovník :30 / Podbořany :15 (Hořovičky :44) | 3 |
| XS75 | not modelled (replacement bus, automatic) | – | 0 |
| **Total** | **30 Simutrans lines** | | **47** |

Bus counts are the builder's need from each pattern (Step 10), one Simutrans line at a time; real buses swap between these
lines (the chain tests show 304 ↔ 577 at Stochov, 561 ↔ 581 at Senomaty, 562 → 561 / 560 at Rakovník), so the per-line totals
are higher than the operators' own. Pooling is an owner option, not applied. The review's 45 assumed 574 dropped; the owner
kept it, and 711 Domoušice was added for the out-of-kraj rule.

## Step 4 per leg (from `schedule.json`)

Columns: slots (mod every; typed values in brackets), window slots, real departures in the window, window slots with a real
departure within 3 min, exact / within 3 / trips over the day (5–23).

| Simutrans line | Leg | Slots (typed) | Window slots | Real in window | Filled | Day ex/w3/n |
|---|---|---|---|---|---|---|
| 304 | Rakovník AS → Kukulova | 0:00, 0:40, 1:30 (typed 29, 59, 99) | 15:30 16:00 16:40 | 15:30 16:00 16:40 | 3/3 | 9/9/26 |
| 304 | Kukulova → Rakovník AS | 0:53, 1:23, 1:58 (typed 22, 57, 112) | 15:58 16:53 17:23 | 15:58 16:28 16:53 17:23 | 3/3 | 5/6/24 |
| 305 | Zličín → Karlovy Vary, terminál | :05 (typed 4) | 15:05 16:05 | 15:05 16:05 | 2/2 | 8/8/10 |
| 305 | Karlovy Vary, terminál → Zličín | :30 (typed 29) | 14:30 15:30 | 14:30 15:30 | 2/2 | 8/8/10 |
| 404 | Zličín → Kralovice | 0:40, 1:40 (typed 39, 99) | 14:40 15:40 | 14:40 15:10 15:40 16:10 | 2/2 | 8/8/16 |
| 404 | Kralovice → Zličín | 0:40, 1:45 (typed 44, 99) | 14:40 15:45 | 14:40 15:45 | 2/2 | 2/2/8 |
| 415 | Zličín → Kadaň, AN | 0:10 (typed 69) | 16:10 | 16:10 17:00 | 1/1 | 2/2/7 |
| 415 | Kadaň, AN → Zličín | 0:50 (typed 109) | 16:50 | 16:50 | 1/1 | 5/6/8 |
| 417 | Zličín → Mšec | :50 (typed 49) | 13:50 14:50 | 13:50 14:50 | 2/2 | 6/6/11 |
| 417 | Mšec → Zličín | :20 (typed 19) | 14:20 15:20 | 14:20 15:20 | 2/2 | 6/6/9 |
| 560 | Rakovník AS → Kryry, Strojetice, křižovatka | 1:00 (typed 119) | 15:00 | 14:45 15:00 | 1/1 | 3/3/7 |
| 560 | Kryry, Strojetice, křižovatka → Rakovník AS | 0:14 (typed 73) | 16:14 | 16:14 | 1/1 | 1/1/7 |
| 560 Kolešovice | Rakovník AS → Kolešovice | 0:00 (typed 59) | 16:00 | 16:00 | 1/1 | 3/3/9 |
| 560 Kolešovice | Kolešovice → Rakovník AS | 1:30 (typed 29) | 15:30 | 14:30 15:30 | 1/1 | 2/2/9 |
| 577 | Rakovník AS → Stochov, Slovanka II | 0:35 (typed 214) | 16:35 | 16:35 | 1/1 | 1/1/3 |
| 577 | Stochov, Slovanka II → Rakovník AS | 2:46 (typed 105) | – | 16:56 | 0/0 | 2/2/4 |
| 760 | Rakovník AS → Podbořany, AN | :30 (typed 29) | 15:30 16:30 | 15:30 16:30 | 2/2 | 8/8/12 |
| 760 | Podbořany, AN → Rakovník AS | :15 (typed 14) | 16:15 17:15 | 16:15 17:15 | 2/2 | 9/9/12 |
| 561 | Šamotka → Kolešovice | 2:10 (typed 69) | 14:10 | 14:10 | 1/1 | 1/1/2 |
| 561 | Kolešovice → Rakovník AS | 0:30 (typed 209) | – | – | 0/0 | 1/1/1 |
| 561 | Rakovník AS → Šamotka | untimed | | | | |
| 562 | garáže Transdev Stř.Č. → hasičský záchr.sbor | 1:35 (typed 34) | 15:35 | 14:50 15:35 | 1/1 | 3/3/11 |
| 562 | hasičský záchr.sbor → garáže Transdev Stř.Č. | 0:18 (typed 77) | 14:18 | 14:18 | 1/1 | 2/2/8 |
| 562 Lubná | Rakovník AS → Lubná, závod | 3:30 (typed 149) | 15:30 | 15:30 | 1/1 | 1/1/3 |
| 562 Lubná | Lubná, závod → Rakovník AS | 3:54 (typed 173) | 15:54 | 14:24 15:54 | 1/1 | 1/1/5 |
| 563 | Rakovník AS → Mutějovice | 2:30 (typed 89) | – | – | 0/0 | 2/2/4 |
| 563 | Mutějovice → Rakovník AS | 0:54 (typed 173) | 15:54 | 15:54 | 1/1 | 1/1/3 |
| 571 | Rakovník AS → Chříč | 6:50 (typed 349) | – | – | 0/0 | 1/1/2 |
| 571 | Chříč → Rakovník AS | 7:30 (typed 389) | 15:30 | 15:30 | 1/1 | 1/1/2 |
| 572 | Rakovník AS → Krakovec | 1:00 (typed 119) | 15:00 | 15:00 | 1/1 | 1/1/4 |
| 572 | Krakovec → Rakovník AS | 1:30 (typed 29) | 15:30 | 15:30 | 1/1 | 1/1/3 |
| 572 Slabce | Rakovník AS → Slabce, pošta | 2:30 (typed 89) | – | – | 0/0 | 1/1/4 |
| 572 Slabce | Slabce, pošta → Rakovník AS | 0:44 (typed 463) | 16:44 | 16:44 | 1/1 | 1/1/3 |
| 573 | Čistá → Hořovičky | 0:15 (typed 74) | 14:15 | 14:15 | 1/1 | 3/3/4 |
| 573 | Hořovičky → Čistá | 1:08 (typed 7) | 15:08 | 15:08 | 1/1 | 2/2/4 |
| 573 Šípy | Čistá → Břežany | 7:30 (typed 389) | 15:30 | 15:30 | 1/1 | 1/1/2 |
| 573 Šípy | Břežany → Čistá | 7:57 (typed 416) | 15:57 | 15:57 | 1/1 | 1/1/2 |
| 574 | Skryje → Křivoklát, žz | 1:20 (typed 19) | 17:20 | 17:20 | 1/1 | 1/1/1 |
| 574 | Křivoklát, žz → Skryje | untimed | | | | |
| 575 | Rakovník AS → Zvíkovec | 0:11 (typed 94) | 16:59 | 17:00 | 1/1 | 1/2/5 |
| 575 | Zvíkovec → Rakovník AS | 1:11 (typed 10) | 15:35 | 15:35 | 1/1 | 1/1/5 |
| 576 | Rakovník AS → Skryje | 2:40 (typed 99) | – | 16:30 | 0/0 | 1/1/7 |
| 576 | Skryje → Rakovník AS | 0:04 (typed 183) | 16:04 | 16:04 | 1/1 | 1/1/5 |
| 578 | Rakovník AS → Rakovník AS | 2:45 (typed 104) | 14:45 | 14:45 | 1/1 | 1/1/4 |
| 579 | Branov → Nezabudice | 2:35 (typed 94) | 14:35 | 14:35 | 1/1 | 1/1/3 |
| 579 | Nezabudice → Branov | 3:23 (typed 142) | 15:23 | 15:23 | 1/1 | 1/1/2 |
| 579 | Branov → Roztoky, Leontýn | 1:30 (typed 29) | – | – | 0/0 | 1/1/2 |
| 579 | Roztoky, Leontýn → Branov | 2:17 (typed 76) | 14:17 | 14:17 | 1/1 | 1/1/2 |
| 581 | Rakovník AS → Lišany, u rybníka | 1:30 (typed 29) | 15:30 | 15:30 | 1/1 | 2/2/7 |
| 581 | Lišany, u rybníka → Rakovník AS | 0:25 (typed 84) | 16:25 | 16:25 | 1/1 | 3/3/8 |
| 581 Nové Strašecí | Rakovník AS → Nové Strašecí, Pecínov | 0:30 (typed 209) | 16:30 | 16:30 | 1/1 | 1/1/4 |
| 581 Nové Strašecí | Nové Strašecí, Pecínov → Rakovník AS | 2:07 (typed 66) | – | – | 0/0 | 1/1/2 |
| 581 Senomaty | Rakovník AS → Senomaty | 1:10 (typed 9) | 17:10 | 17:10 | 1/1 | 1/1/2 |
| 581 Senomaty | Senomaty → Rakovník AS | 1:33 (typed 32) | – | – | 0/0 | 1/1/6 |
| 584 | Rakovník AS → Mutějovice, Lhota p.Džbánem | 1:15 (typed 14) | 13:15 | 13:15 | 1/1 | 1/1/4 |
| 584 | Mutějovice, Lhota p.Džbánem → Rakovník AS | 0:00 (typed 59) | 14:00 | 13:00 14:00 | 1/1 | 1/1/2 |
| 584 Vinařice | Rakovník AS → Vinařice [pásmo 7 2] | 6:30 (typed 329) | 14:30 | 14:30 | 1/1 | 1/1/2 |
| 584 Vinařice | Vinařice [pásmo 7 2] → Rakovník AS | 7:25 (typed 384) | – | – | 0/0 | 1/1/2 |
| 711 | žz západ → Louny, Luna | 2:20 (typed 79) | 14:20 | 14:20 | 1/1 | 1/1/7 |
| 711 | Louny, Luna → žz západ | 3:55 (typed 174) | 15:55 | 15:55 | 1/1 | 2/2/6 |
| 711 Domoušice | Louny, AN → Domoušice, Solopysky | 6:00 (typed 299) | – | – | 0/0 | 2/2/2 |
| 711 Domoušice | Domoušice, Solopysky → Louny, AN | 6:30 (typed 329) | 14:30 | 14:30 | 1/1 | 2/2/2 |

## The lines

### 304 Praha,Kukulova/Vypich - Rakovník (Transdev Střední Čechy s.r.o.; 71 trips, 25 in 13–19)
- **Core points:** Rakovník, autobusové stanoviště | Nové Strašecí, Palackého | Stochov, Slovanka II | Praha, Zličín | Praha, Kukulova. Model window 15:30–17:30 (the line's anchor).
- **Card:** Rakovník – Lužná – Ruda – Nové Strašecí – Stochov – Praha, Zličín – Praha, Vypich, where the buses arrive, and Praha, Kukulova, where they leave (one terminus). The buses sleep in Rakovník, so the afternoon is an outflow from Prague: from 15:30 to 17:30 Rakovník sends 15:30 (to Zličín only), 16:00, 16:40 and Kukulova 15:58, 16:28, 16:53, 17:23. Timed at the rate towards Prague, every 120 with three slots each way; Kukulova 16:28 and the Rakovník departures 13:00–15:00 (buses going to Prague for the peak) are off the pattern, and the Prague-only trips (Kukulova → Zličín 13:39, 15:45; Zličín → Stochov 16:30) are listed.
- **Reasoning (1 Nov):** Rakovník – Lužná – Ruda – Nové Strašecí – Stochov, Slovanka II – Praha, Zličín – Motol – Vypich / Kukulova. Buses arrive at Praha, Vypich and leave for Rakovník from Praha, Kukulova (terminus_alias: one terminus, timed at Kukulova). Whole day: Rakovník towards Prague hourly at :00 from 9:05 to 12:00, every 20 min 13:00–14:40 (13:20 and 14:00 end at Zličín), then 15:00, 15:30 (to Zličín), 16:00, 16:40, 17:30, 18:40; Kukulova towards Rakovník hourly at :53 9:53–11:53, then 12:48, 13:18, 14:08, 14:38, 15:23, 15:58, 16:28, 16:53, 17:23, 18:05, 19:08. The buses sleep at Rakovník (4:00–5:40 the first trips start there), so the afternoon is an outflow from Prague: 13:00–15:00 Rakovník sends 7 and Kukulova 3; 15:30–17:30 Kukulova sends 4 and Rakovník 3 (with the 15:30 Zličín short). Modelled at 16:00 (the line's anchor, window 15:30–17:30) at the inbound rate: every 120 with three slots each way (the 290 precedent; every 30 / 40 / 60 leave Rakovník slots without a trip). Off the pattern 12–20 h: Rakovník 12:30, 13:00, 13:20, 13:40, 14:20, 15:00 (10–20 min from the slots: the buses positioning to Prague for the peak), 19:35; Kukulova 12:48, 13:18, 14:08, 14:38, 16:28, 18:05, 19:08. Listed (no stop of their own, all on 304's path): Kukulova → Zličín 13:39, 15:45; Zličín → Vypich 12:15; Zličín 16:30 → Stochov (goes on as 577 16:56); Stochov 15:24 → Vypich (the 577 14:50 bus); Rakovník → Zličín 13:20, 14:00, 19:35. Step 5b: the 0-minute chains at Stochov, Slovanka II (3/3 arrivals, 2/2 departures) are 577 through-running, noted on 577. Prague stops count as covered by the Prague bus sheet.
- **Changed on 2 Nov:** Owner check removed (the inbound-rate rule decides). Live-map items in `notes`: the Rakovník – Zličín trips 13:20, 14:00, 15:30 and the 304 ↔ 404 / 304 → 306 chains at Praha, Zličín.
- **304**, every 120, 5 buses: Rakovník 15:30, 16:00, 16:40 and Kukulova 15:58, 16:53, 17:23 via Lužná, Ruda, Nové Strašecí and Stochov, Slovanka II: 69 min to Vypich, 78 min back. The 15:30 is a Rakovník – Zličín trip that the game bus runs on to Kukulova.
  - Step 4: autobusové stanoviště → Kukulova: window slots 15:30 16:00 16:40 / real 15:30 16:00 16:40, filled 3/3; day exact 9, within 3 9 of 26; off 12–20 h 12:30, 13:00, 13:20, 13:40, 14:20, 15:00, 19:35; Kukulova → autobusové stanoviště: window slots 15:58 16:53 17:23 / real 15:58 16:28 16:53 17:23, filled 3/3; day exact 5, within 3 6 of 24; off 12–20 h 12:48, 13:18, 14:08, 14:38, 16:28, 18:05, 19:08.

### 305 Praha,Zličín - Karlovy Vary (Transdev Střední Čechy s.r.o.; 24 trips, 10 in 13–19)
- **Core points:** Praha, Zličín | Stochov, Slovanka II | Nové Strašecí, Palackého | Krupá, Šustna | Hořovičky | Karlovy Vary, terminál. Model window 14:30–16:30 (anchor set by hand).
- **Card:** Praha, Zličín – Stochov – Nové Strašecí – Krupá – Hořovičky – Lubenec – Bochov – Karlovy Vary, hourly all afternoon: Zličín :05 (no 17:05) and Karlovy Vary :30 (no 13:30), exact. Modelled at 15:00, because the 16:00 window holds Zličín's missing 17:05. Off the pattern: Zličín 5:10, 20:45; Karlovy Vary 4:40, 5:35, 7:15 and 22:00 (to Hořovičky).
- **Reasoning (1 Nov):** Praha, Zličín – Stochov – Nové Strašecí – Řevničov – Krušovice – Krupá, Šustna – Hořesedly – Hořovičky – Lubenec – Bochov – Karlovy Vary. Hourly all afternoon: Zličín :05 (10:05, 12:05–16:05, 18:05; 17:05 has no trip), Karlovy Vary :30 (10:30, 12:30, 14:30–19:30; 13:30 has no trip), exact on every trip, running 137 / 139 min. The auto anchor (16:00) puts Zličín's missing 17:05 into the window, a slot without a trip, so the anchor is set to 15:00 (window 14:30–16:30), where the line's own hourly pattern runs (the 282 rule). Off: Zličín 5:10, 20:45; Karlovy Vary 4:40, 5:35, 7:15, 22:00 (to Hořovičky; the morning trips 3:54 Krupá and 4:30 Stochov start in the okres). Hořesedly, Krušovice and Řevničov have no other line in okres Rakovník.
- **Changed on 2 Nov:** Owner check removed: exact hourly is the method's answer (8 of 10 exact each way).
- **305**, every 60, 5 buses: Zličín :05 / Karlovy Vary :30 on one path via Řevničov, Krušovice, Krupá, Šustna and Hořesedly: 137 min out, 139 min back.
  - Step 4: Zličín → terminál: window slots 15:05 16:05 / real 15:05 16:05, filled 2/2; day exact 8, within 3 8 of 10; off 12–20 h none; terminál → Zličín: window slots 14:30 15:30 / real 14:30 15:30, filled 2/2; day exact 8, within 3 8 of 10; off 12–20 h none.

### 404 Praha,Zličín - Rakovník - Kralovice - Manětín - Nečtiny (Transdev Střední Čechy s.r.o.; 45 trips, 16 in 13–19)
- **Core points:** Praha, Zličín | Ruda, u rybníka | Rakovník, autobusové stanoviště | Čistá | Břežany | Kralovice. Model window 14:30–16:30 (anchor set by hand).
- **Card:** Praha, Zličín – Ruda, u rybníka – Rakovník – Lubná – Petrovice – Čistá – Břežany – Kralovice. Out of Zličín every 30 from 14:10 to 18:10 (:40 to Kralovice, :10 to Rakovník only), into Prague hourly only until 15:45 (Rakovník 13:30, 14:35; Kralovice 14:40, 15:45): the buses sleep in Rakovník. Timed at the rate towards Prague: Zličín every 60 at :40 (14:40 is a Rakovník trip, run on to Kralovice) and Kralovice 14:40, 15:45; the :10 departures from Zličín are buses going home, off the pattern (the Step 4 audit's FEWER row).
- **Reasoning (1 Nov):** Praha, Zličín – R6 – Ruda, u rybníka – Rakovník – Lubná – Petrovice – Všesulov – Čistá – Břežany – Kožlany – Kralovice. Out of Zličín every 30 from 14:10 to 18:10: :40 to Kralovice (15:40, 16:40, 17:40; 14:40 only to Rakovník) and :10 to Rakovník / Rakovník, Plzeňská (15:10, 16:10, 17:10, 18:10; 14:10 to Kralovice). Into Prague hourly at Rakovník :30 / :35 (13:30, 14:35 start at Rakovník; Kralovice 14:40, 15:45 pass Rakovník 15:30, 16:35), and nothing from Kralovice after 15:45 (17:40, 18:40, 19:40 run Kralovice → Rakovník only). An outstation line: the buses sleep at Rakovník (5:00–8:00 Rakovník → Zličín) and come home on the :10 departures. Timed at the inbound rate, window 14:30–16:30 (the line's anchor 15:00): every 120, Zličín 14:40 and 15:40 (that entry is every 60 at :40) and Kralovice 14:40 and 15:45, both exact. The Zličín leg counts the Rakovník shorts (core_to Rakovník, autobusové stanoviště): its 14:40 slot is the 14:40 Zličín → Rakovník trip, run on to Kralovice in the game. Off the pattern: Zličín 14:10, 15:10, 16:10, 17:10, 18:10, 19:10 (buses going home: the audit's FEWER row, 2 slots for 4 departures, the owner-approved outstation case). Listed: Rakovník → Zličín 13:30, 14:35 (Rakovník, Plzeňská 6:13); Kralovice → Rakovník 17:40, 18:40, 19:40; Zličín → Čistá 20:45, Čistá → Rakovník 21:57; their stops are all on 404's path. 570 (LEXTRANS) runs the same corridor and is carried here and by 581 / 711 / 562 (see unmodelled).
- **Changed on 2 Nov:** Owner check removed: the FEWER row is the outstation case approved on 290; the two options it offered break the 25 Oct and 290 rules.
- **404**, every 120, 4 buses: Zličín :40 and Kralovice 14:40 / 15:45 by the motorway via Ruda, u rybníka, then Rakovník, Plzeňská, Lubná, Petrovice, Všesulov, Čistá, Břežany and Kožlany: 95 min out, 93 min back.
  - Step 4: Zličín → Kralovice: window slots 14:40 15:40 / real 14:40 15:10 15:40 16:10, filled 2/2; day exact 8, within 3 8 of 16; off 12–20 h 14:10, 15:10, 16:10, 17:10, 18:10, 19:10; Kralovice → Zličín: window slots 14:40 15:45 / real 14:40 15:45, filled 2/2; day exact 2, within 3 2 of 8; off 12–20 h none.

### 415 Praha,Zličín - Kadaň (Transdev Střední Čechy s.r.o., UMBRELLA CITY LINES s.r.o.; 33 trips, 13 in 13–19)
- **Core points:** Praha, Zličín | Krupá, Šustna | Mutějovice | Svojetín, ObÚ | Žatec, autobusové nádraží | Kadaň, autobusové nádraží. Model window 15:30–17:30 (anchor set by hand).
- **Card:** Praha, Zličín – Krupá, Šustna – Mutějovice – Svojetín – Měcholupy – Žatec – Kadaň. Kadaň → Prague every 2 hours at :50 all day; Zličín → Kadaň about two per 2 hours at no fixed minute (13:05, 14:15, 16:10, 17:00, 18:10). Modelled at 16:00: the 13:00–15:00 window is the variant via Nové Strašecí, Rynholec and Lány (Zličín 14:40, 18:40; Kadaň 13:47; listed, its stops are on 417, 304 and 581); Zličín 13:05, 14:15 and 17:00 are off the pattern. The Chbany and Deštnice villages (Ústecký kraj) have no other line, so each direction is shown by the path that serves them.
- **Reasoning (1 Nov):** Praha, Zličín – R6 – Krupá, Šustna – Mutějovice – Nesuchyně – Milostín – Svojetín – Měcholupy – Žatec – Kadaň (two licences, 100415 + 104415, Transdev and Umbrella, merged). Kadaň → Prague every 2 h at :50 all day (8:50, 10:50, 12:50, 14:47, 16:50, 18:50); Zličín → Kadaň about two per 2 h in the afternoon at no fixed minute (11:00, 13:05, 14:15, 16:10, 17:00, 18:10). Variant via Nové Strašecí, Rynholec, Lány and Stochov, Slovanka I (Zličín 6:45, 11:40, 14:40, 18:40; Kadaň 13:47): its stops are on 417, 304 and 581, so it is listed (Step 8; `notvia` Nové Strašecí, Palackého keeps it out of the rows). Kadaň → Žatec shorts 15:47, 17:50 and Žatec – Kadaň trips are Ústecký kraj only. Anchor set to 16:00: the auto anchor (13:30) window is the Nové Strašecí trips (13:47, 14:40) and the 14:15 extra; at 16:00 the line's own two-hourly pattern runs (the 282 rule). Every 120: Zličín 16:10 (16:10, 18:10 exact; 14:15 is 5 min off), Kadaň 16:50 (exact five times). Off 12–20 h: Zličín 13:05, 14:15, 17:00. Svojetín, ObÚ has no other line.
- **Changed on 2 Nov:** The out-of-kraj stops now count (owner, 2 Nov): out shown by the 14:15 trip's path via the Chbany villages (`stops_via` Chbany, Vikletice; rt 118 set by hand, the builder's median 133 mixed in the 6:45 via Nové Strašecí), back by the 12:50 / 18:50 path via Měcholupy, Želeč and Deštnice (`stops_via` Deštnice, 140 min). Chbany, Poláky, točna (110 m from Chbany, Poláky) is a coverage exception, in the one owner check. Need unchanged, 3.
- **415**, every 120, 3 buses: Zličín 16:10 and Kadaň 16:50 every 120; out shown by the 14:15 trip's path via the Chbany villages (Vikletice, Vadkovice, Malé Krhovice, 118 min; the 16:10 itself takes the main road, 115 min), back via Měcholupy, Želeč, Deštnice and Svojetín, ObÚ (140 min; the 16:50 skips Deštnice, 134 min), so every stop of 415 is on the line.
  - Step 4: Zličín → autobusové nádraží: window slots 16:10 / real 16:10 17:00, filled 1/1; day exact 2, within 3 2 of 7; off 12–20 h 13:05, 14:15, 17:00; autobusové nádraží → Zličín: window slots 16:50 / real 16:50, filled 1/1; day exact 5, within 3 6 of 8; off 12–20 h none.

### 417 Praha,Zličín - Nové Strašecí - Mšec (ARRIVA CITY a.s.; 31 trips, 10 in 13–19)
- **Core points:** Praha, Zličín | Stochov, Slovanka | Lány, náměstí | Nové Strašecí, Palackého | Mšec. Model window 13:30–15:30 (anchor set by hand).
- **Card:** Praha, Zličín – Velká Dobrá – Stochov – Lány – Rynholec – Nové Strašecí – Mšecké Žehrovice – Mšec, hourly: Zličín :50, Mšec :20 (no 16:20), exact. Modelled at 14:00, where both directions run; the Nové Strašecí – Zličín trips (13:35 and 18:50 in, 17:50 and 22:25 out) and the morning Lány and Stochov trips are listed.
- **Reasoning (1 Nov):** Praha, Zličín – Velká Dobrá – Tuchlovice – Stochov – Lány – Rynholec – Nové Strašecí – Mšecké Žehrovice – Mšec. Hourly: Zličín :50 (12:20, 13:50–16:50 to Mšec, 17:50 to Nové Strašecí), Mšec :20 (11:20, 14:20, 15:20, 17:20; 16:20 has no trip), exact; modelled at the line's anchor 14:00 (window 13:30–15:30). Listed (stops on 417's path): Nové Strašecí → Zličín 13:35, 18:50; Zličín → Nové Strašecí 17:50, 22:25; the morning Lány, nám. → Zličín and Zličín → Stochov, nám. shorts. Mšec, Mšecké Žehrovice and Nové Strašecí, Libeň have no other line.
- **417**, every 60, 3 buses: Zličín :50 / Mšec :20 via Stochov, Slovanka, Lány and Rynholec: 68 min out, 71 min back.
  - Step 4: Zličín → Mšec: window slots 13:50 14:50 / real 13:50 14:50, filled 2/2; day exact 6, within 3 6 of 11; off 12–20 h 12:20, 19:30; Mšec → Zličín: window slots 14:20 15:20 / real 14:20 15:20, filled 2/2; day exact 6, within 3 6 of 9; off 12–20 h none.

### 560 Rakovník - Kryry,Strojetice (Transdev Střední Čechy s.r.o.; 35 trips, 12 in 13–19)
- **Core points:** Rakovník, autobusové stanoviště | Kolešovice | Hořovičky | Kryry, Strojetice, křižovatka. Model window 14:30–16:30 (the line's anchor).
- **Card:** Rakovník – Olešná – Kněževes – Kolešovice – Hořovičky – Kryry, Strojetice, křižovatka: Rakovník :00 hourly 13:00–17:00, alternating Kolešovice and Hořovičky or Kryry (plus 14:45 to Kryry); towards Rakovník Kolešovice :30 hourly 14:30–17:30. Two Simutrans lines give that trunk: 560 (odd hours, out round the Hořesedly – Děkov loop, back via Hokov and Heřmanov) and 560 Kolešovice (even hours). Off the pattern: Rakovník 14:45; Hořovičky 12:34, 14:02, 18:00; Kryry 17:14; Kolešovice 14:30.
- **Reasoning (1 Nov):** Rakovník – Olešná – Chrášťany – Kněževes – Kolešovice – Hořovičky – Kryry, Strojetice. Out of Rakovník hourly at :00 13:00–17:00 (13:00 Hořovičky, 14:00 Kolešovice, 15:00 Kryry, 16:00 Kolešovice, 17:00 Hořovičky) plus 14:45 Kryry; towards Rakovník, read at Kolešovice, hourly at :30 14:30–17:30 (14:30, 15:30 start at Kolešovice; 16:30, 17:30 are Kryry 16:14 / 17:14) plus Hořovičky 14:02 (Kolešovice 14:10) and 18:00. The Hořovičky / Kryry trips run a one-way loop: out round Hořesedly – Děkov – Vrbice – Kolešov – Bukov, back by Hokov and Heřmanov. Two Simutrans lines (Ex4), together hourly at Rakovník :00 and at Kolešovice :30 as the real trunk: 560 to Kryry, Strojetice, křižovatka (Rakovník :00 odd hours, Kryry :14 even hours; both window slots are Kryry trips: 15:00 out, 16:14 back) and 560 Kolešovice (Rakovník :00 even, Kolešovice :30 odd; the even-hour :30 would meet 560 there). The Hořovičky trips count in 560's rows: out read to Hořovičky (core_to), back read at Hořovičky :22 (knot; mixed origins on the line's own path). Off 12–20 h: Rakovník 14:45 (Kryry); Hořovičky 12:34, 14:02, 18:00 (Kryry-time 12:26, 13:54, 17:52), Kryry 17:14; Kolešovice 14:30. Kněževes, železniční zastávka is on the Hořovičky 18:00 (12:34, 6:56) trips only, which run back via Kněževes žz and Rakovník, nemocnice instead of Hokov / Heřmanov: a coverage exception. 760 shares the trunk (Rakovník :30, Kolešovice ~:55 back): no shared minute.
- **560**, every 120, 1 bus: Rakovník :00 odd hours to Kryry by the 15:00 trip's path via Hořesedly, Děkov and Bukov (56 min); back from Kryry :14 even hours (Hořovičky :22) via Hokov and Heřmanov (40 min); the Hořovičky trips count in both rows.
  - Step 4: autobusové stanoviště → křižovatka: window slots 15:00 / real 14:45 15:00, filled 1/1; day exact 3, within 3 3 of 7; off 12–20 h 14:45; křižovatka → autobusové stanoviště: window slots 16:14 / real 16:14, filled 1/1; day exact 1, within 3 1 of 7; off 12–20 h 12:26, 13:54, 17:14, 17:52.
- **560 Kolešovice**, every 120, 1 bus: Rakovník :00 even hours via Přílepy (28 min), Kolešovice :30 odd hours back (24 min); the even-hour :30 would meet 560 at Kolešovice.
  - Step 4: autobusové stanoviště → Kolešovice: window slots 16:00 / real 16:00, filled 1/1; day exact 3, within 3 3 of 9; off 12–20 h none; Kolešovice → autobusové stanoviště: window slots 15:30 / real 14:30 15:30, filled 1/1; day exact 2, within 3 2 of 9; off 12–20 h 14:30.

### 561 Rakovník - Řeřichy - Kolešovice (Transdev Střední Čechy s.r.o.; 40 trips, 11 in 13–19)
- **Core points:** Rakovník, Šamotka | Rakovník, autobusové stanoviště | Senomaty | Řeřichy | Kolešovice. Model window 14:00–16:00 (the line's anchor).
- **Card:** Rakovník, Šamotka – Rakovník, autobusové stanoviště – nemocnice – Senomaty (Nouzov loop) – Šanov – Petrovice – Zavidov – Řeřichy – Oráčov – Kolešovice, a school-day line of single trips. One Simutrans line every 240 on its longest trip, Šamotka 14:10 → Kolešovice 15:26, back on the Kolešovice 20:30 a period later; it holds every stop of the line. Listed (stops on 561, 562 or 581 Senomaty): Šamotka 12:45 → Senomaty, střelnice 13:00 → hasičský záchranný sbor, 14:00 → Nouzov, Nouzov 14:40 → Šamotka, Šamotka 15:10 → Petrovice, Senomaty 15:13 → Rakovník, střelnice 15:16 → Rakovník, 16:30 → Řeřichy, Řeřichy 17:10 → Petrovice, 18:30 → Řeřichy, Řeřichy 19:05 → Rakovník; Senomaty 17:33 → Rakovník runs on 581 Senomaty.
- **Reasoning (1 Nov):** Rakovník, Šamotka – Rakovník AS – nemocnice – Senomaty (Nouzov loop) – Šanov – Petrovice – Zavidov – Václavy – Řeřichy (– Pšovlky – Švihov – Oráčov – Zderaz – Kolešovice). A school-day line of single trips. Towards Senomaty, at Rakovník AS: 13:00 (from Šamotka 12:45, to Senomaty), 14:00 (to Nouzov), 14:30 (from Šamotka 14:10, to Kolešovice), 15:30 (from Šamotka 15:10, to Petrovice), 16:30 and 18:30 (to Řeřichy); towards Rakovník: 14:40 Nouzov → Šamotka, 15:13 and 17:33 Senomaty → AS, 19:05 Řeřichy → AS, 20:30 Kolešovice → AS. The buses sleep out (4:25–6:38 the first trips start at Petrovice, Řeřichy, Oráčov). Two Simutrans lines: 561 (every 240, the full route Šamotka 14:10 → Kolešovice, back from Kolešovice 16:30 = the 20:30 a period later, then untimed to Šamotka) and 561 Řeřichy (every 480, AS 16:30 → Řeřichy, Řeřichy 19:05 → AS). Together at AS towards Senomaty: 14:30, 16:30, 18:30 (real 14:30, 16:30, 18:30). Senomaty → AS 17:33 is the way back of 581 Senomaty (the 581/561 ring at Senomaty, Step 5b); 15:13 is off it. Listed (every stop on 561, 561 Řeřichy, 562 or 581 Senomaty): 12:45 Šamotka → Senomaty (goes on as 581 13:18), 13:00 střelnice → hasič, 14:00 AS → Nouzov, 14:40 Nouzov → Šamotka, 15:10 Šamotka → Petrovice, 15:16 střelnice → AS, 17:10 Řeřichy → Petrovice. Window 14:00–16:00 (the line's anchor 14:30); 561 Řeřichy has its own window 16:00–18:00, where its trips run.
- **Changed on 2 Nov:** 561 Řeřichy dropped (review): it served no stop of its own, and its 16:30 → Řeřichy and 19:05 Řeřichy → Rakovník trips are listed. Live-map item: 561 Šamotka 14:10 → Kolešovice 15:26 is followed by 560 Kolešovice 15:30 (if the plates confirm it, one circuit would save a bus).
- **561**, every 240, 1 bus: Šamotka 14:10 → Kolešovice via the town loop (Autostop, Tesco), Senomaty with the Nouzov loop, Šanov, Petrovice, Zavidov, Řeřichy and Oráčov (76 min); Kolešovice 16:30 (the real 20:30, a period later) back to the autobusové stanoviště (60 min), then untimed to Šamotka.
  - Step 4: Šamotka → Kolešovice: window slots 14:10 / real 14:10, filled 1/1; day exact 1, within 3 1 of 2; off 12–20 h none; Kolešovice → autobusové stanoviště: window slots – / real –, filled 0/0; day exact 1, within 3 1 of 1; off 12–20 h none; autobusové stanoviště → Šamotka untimed.

### 562 Lubná - Rakovník - Olešná (Transdev Střední Čechy s.r.o.; 33 trips, 12 in 13–19)
- **Core points:** Lubná, závod | Rakovník, garáže Transdev Stř.Č. | Rakovník, autobusové stanoviště | Rakovník, hasičský záchr.sbor. Model window 14:10–16:10 (the line's anchor).
- **Card:** Rakovník's town service: Rakovník, garáže Transdev (a public stop with a timetable, not a depot run) – Komenského náměstí – autobusové stanoviště – nemocnice – hasičský záchranný sbor, from garáže at :35 in the morning and 13:35, 15:35 in the afternoon, with trips on to Lubná, Senec and Olešná. Two Simutrans lines: 562 (garáže ↔ hasičský záchranný sbor) and 562 Lubná (autobusové stanoviště ↔ Lubná, závod, the only service of Průhon). Listed (stops on 562, 562 Lubná, 560, 760 and 572): garáže 13:35, hasičský záchranný sbor 13:48 → Lubná, Lubná 14:24 → autobusové stanoviště, garáže 14:50 → střelnice, 15:00 → garáže, hasičský záchranný sbor 15:52 → autobusové stanoviště, Olešná 16:31 → garáže, 17:45 → garáže.
- **Reasoning (1 Nov):** Lubná, závod – Rakovník, garáže Transdev – Komenského nám. – AS – nemocnice – hasičský záchranný sbor (– Olešná, Senec). Rakovník's town service, one or two buses: garáže → AS → hasič hourly at :35 in the morning (7:40, 8:35, 9:35, 10:35) and 13:35, 15:35 (14:50 to střelnice) in the afternoon; hasič → garáže 8:18, 9:18, 14:18; Lubná trips 13:48 (hasič → Lubná), 14:24 (Lubná → AS), 15:30 (AS → Lubná), 15:54 (Lubná → Olešná), Olešná 16:31 → garáže; ends 17:53. 'Rakovník, garáže Transdev Stř.Č.' is a public stop with a timetable (not a depot run) and the only service of seven town stops (Malinovského, O.Beníškové, 3.ZŠ, Riegrova, S.K.Neumanna, Komenského nám., Průhon), so it is modelled. Two Simutrans lines: 562 garáže ↔ hasič every 120 (garáže 15:35, hasič 14:18) and 562 Lubná AS ↔ Lubná, závod every 240 (AS 15:30, Lubná 14:24). Window 14:10–16:10 (the line's anchor 14:40). Listed (stops on 562, 562 Lubná, 560, 760): 13:35 garáže → hasič, 13:48 hasič → Lubná, 14:50 garáže → střelnice, 15:00 AS → garáže, 15:52 hasič → AS, 15:54 Lubná → Olešná, 16:31 Olešná → garáže, 17:45 AS → garáže.
- **Changed on 2 Nov:** 562 Lubná back slot 15:54 (the same bus after a 3-min turn, typed 173; was 14:24 with a 150-min wait) and out on the 15:30's direct path (`notvia` Lubná, Filipka, 21 min; the loop via Filipka and Senec is on 572). Pooling check removed.
- **562**, every 120, 1 bus: Garáže 15:35 → hasičský záchranný sbor via Komenského náměstí, the autobusové stanoviště and nemocnice (16 min), hasičský záchranný sbor 14:18 back (17 min); every 60 would leave the garáže 14:35 slot without a trip.
  - Step 4: garáže Transdev Stř.Č. → hasičský záchr.sbor: window slots 15:35 / real 14:50 15:35, filled 1/1; day exact 3, within 3 3 of 11; off 12–20 h 12:35, 14:50; hasičský záchr.sbor → garáže Transdev Stř.Č.: window slots 14:18 / real 14:18, filled 1/1; day exact 2, within 3 2 of 8; off 12–20 h 13:48.
- **562 Lubná**, every 240, 1 bus: Autobusové stanoviště 15:30 → garáže, Průhon → Lubná, závod direct (21 min); Lubná, závod 15:54 → autobusové stanoviště, the same bus after a 3-min turn (the real trip runs on to Olešná).
  - Step 4: autobusové stanoviště → závod: window slots 15:30 / real 15:30, filled 1/1; day exact 1, within 3 1 of 3; off 12–20 h none; závod → autobusové stanoviště: window slots 15:54 / real 14:24 15:54, filled 1/1; day exact 1, within 3 1 of 5; off 12–20 h 12:22, 14:24.

### 563 Rakovník - Kounov - Mutějovice (Transdev Střední Čechy s.r.o.; 12 trips, 3 in 13–19)
- **Core points:** Rakovník, autobusové stanoviště | Milostín | Svojetín | Kounov, rozcestí | Mutějovice. Model window 15:30–17:30 (the line's anchor).
- **Card:** Rakovník – Olešná – Nesuchyně – Milostín – Svojetín, Veclov – Janov – Kounov – Mutějovice: Rakovník 14:35 and 17:30 out, Mutějovice 15:54 (to Milostín) and 12:24 (to Rakovník) back; the bus sleeps at Mutějovice. Every 180 on one bus; Rakovník 14:35 (5 min off) and Mutějovice 12:24 are off the pattern.
- **Reasoning (1 Nov):** Rakovník – Olešná – Chrášťany – Nesuchyně – Milostín – Svojetín (Veclov) – Janov – Kounov – Mutějovice. Afternoon: Rakovník 14:35 and 17:30 → Mutějovice, Mutějovice 15:54 → Kounov – Janov – Svojetín – Veclov → Milostín (ends there) and 12:24 → Rakovník; the bus sleeps at Mutějovice (4:25, 6:24 start there). Its stops Chrášťany Nový Dvůr rozc., Svojetín Veclov (+ rozc.), Janov, Kounov (rozc., škola, u mostu) have no other line, so it is modelled (Step 8). Every 180 (one bus): Rakovník at :30 (5:30, 17:30 exact; 14:35 is 5 min off) and Mutějovice 15:54 (read to Milostín, core_to); a back slot at the 12:24 phase would leave the bus 5 min short at Mutějovice (2 buses). Off: Rakovník 14:35, Mutějovice 12:24.
- **563**, every 180, 1 bus: Rakovník :30 every 3 hours (the real 17:30) via Svojetín, Veclov and Kounov (54 min); Mutějovice 15:54 back by the 12:24 trip's path (61 min), whereas the real 15:54 ends at Milostín.
  - Step 4: autobusové stanoviště → Mutějovice: window slots – / real –, filled 0/0; day exact 2, within 3 2 of 4; off 12–20 h 14:35; Mutějovice → autobusové stanoviště: window slots 15:54 / real 15:54, filled 1/1; day exact 1, within 3 1 of 3; off 12–20 h 12:24.

### 571 Rakovník - Čistá,Kůzová (Transdev Střední Čechy s.r.o.; 12 trips, 4 in 13–19)
- **Core points:** Rakovník, autobusové stanoviště | Všesulov | Chříč. Model window 15:30–17:30 (the line's anchor).
- **Card:** Rakovník – Lubná – Petrovice – Zavidov – Všesulov – Šípy – Slatina – Chříč (Plzeňský kraj), with Kůzová and Břežany trips. Kept for Slatina and Chříč, which no other line serves (owner, 2 Nov 2026: "Yes, serve every place"): the real round Rakovník 14:50 → Chříč 15:27, Chříč 15:30 → Rakovník, every 480. Listed: Kůzová 12:52 → Rakovník and Rakovník 15:30 → Šípy → Břežany (stops on 404, 573 and 573 Šípy).
- **Reasoning (1 Nov):** Rakovník – Lubná – Petrovice – Zavidov – Všesulov – Šípy – Čistá, Kůzová / Slatina – Chříč. Four afternoon trips: Kůzová 12:52 → Rakovník, Rakovník 14:50 → Chříč 15:27, Chříč 15:30 → Rakovník, Rakovník 15:30 → Šípy, Čistá → Břežany. In okres Rakovník every stop is on 404 and 573 / 573 Šípy, but Slatina and Chříč (Plzeňský kraj, outside PID's oblasti) have no other line, so the Chříč pair is kept as a long-interval line (Step 8, 402B rule): every 480, Rakovník 14:50 / Chříč 15:30, the real 3-minute turn. On the owner checks. Listed: the Kůzová and Břežany trips (stops on 573, 573 Šípy, 404).
- **Changed on 2 Nov:** Kept by the owner's decision of 2 Nov ("Yes, serve every place"); owner check removed.
- **571**, every 480, 1 bus: Rakovník 14:50 → Chříč via Lubná, Příčina, Petrovice, Zavidov, Všesulov and Šípy (37 min); Chříč 15:30 back after the real 3-min turn (40 min).
  - Step 4: autobusové stanoviště → Chříč: window slots – / real –, filled 0/0; day exact 1, within 3 1 of 2; off 12–20 h none; Chříč → autobusové stanoviště: window slots 15:30 / real 15:30, filled 1/1; day exact 1, within 3 1 of 2; off 12–20 h none.

### 572 Rakovník - Krakovec - Zvíkovec (Transdev Střední Čechy s.r.o.; 15 trips, 6 in 13–19)
- **Core points:** Rakovník, autobusové stanoviště | Krakovec | Slabce, pošta | Zvíkovec. Model window 14:30–16:30 (anchor set by hand).
- **Card:** Rakovník – Lubná – Senec – Hvozd – Malinová – Krakov – Krakovec (– Zhoř – Slabce, pošta – Zvíkovec). The Krakovec trips turn at once (Rakovník 15:00 → Krakovec 15:27 → 15:30 → Rakovník), modelled at 15:00; the Slabce trips (Slabce 16:44 → Rakovník, Rakovník 18:30 → Slabce → Zvíkovec) are 572 Slabce, every 480, the only service of Krakovec, Zhoř, rozcestí. Off the pattern: Rakovník 16:45, Krakovec 13:00.
- **Reasoning (1 Nov):** Rakovník – Lubná – Senec – Hvozd – Malinová – Krakov – Krakovec (– Zhoř – Slabce, pošta – Zvíkovec). Afternoon: Krakovec 13:00 → Rakovník; Rakovník 15:00 → Krakovec 15:27 → 15:30 → Rakovník (one bus, 3-min turn); Slabce 16:44 → Krakovec 17:00 → Rakovník; Rakovník 16:45 → Krakovec; Rakovník 18:30 → Slabce → Zvíkovec (sleeps there; 20:16 back). Two Simutrans lines: 572 Rakovník ↔ Krakovec every 120 at the real 15:00 / 15:30 turn (anchor 15:00 by hand: in the auto 16:00 window the only Krakovec trips are 16:45 and the Slabce trip, which no every-120 or -90 row holds with one bus) and 572 Slabce every 480 (Slabce 16:44, Rakovník 18:30) for Krakovec, Zhoř, rozcestí, which no other line serves (on the owner checks). Off: Rakovník 16:45, Krakovec 13:00. The Zvíkovec part of the 18:30 trip is on 575.
- **Changed on 2 Nov:** Owner check removed: Krakovec, Zhoř, rozcestí has seven trips a day and no other line, so the method keeps 572 Slabce.
- **572**, every 120, 1 bus: Rakovník :00 odd hours → Krakovec via Lubná, Senec and Hvozd (25 min), Krakovec :30 odd hours back (25 min).
  - Step 4: autobusové stanoviště → Krakovec: window slots 15:00 / real 15:00, filled 1/1; day exact 1, within 3 1 of 4; off 12–20 h 16:45; Krakovec → autobusové stanoviště: window slots 15:30 / real 15:30, filled 1/1; day exact 1, within 3 1 of 3; off 12–20 h 13:00.
- **572 Slabce**, every 480, 1 bus: Rakovník 18:30 → Krakovec, Zhoř, rozcestí → Slabce, pošta (38 min; the real trip goes on to Zvíkovec); Slabce, pošta 16:44 back (41 min).
  - Step 4: autobusové stanoviště → pošta: window slots – / real –, filled 0/0; day exact 1, within 3 1 of 4; off 12–20 h none; pošta → autobusové stanoviště: window slots 16:44 / real 16:44, filled 1/1; day exact 1, within 3 1 of 3; off 12–20 h none.

### 573 Břežany - Čistá - Jesenice - Hořovičky (LEXTRANS BUS s.r.o.; 15 trips, 9 in 13–19)
- **Core points:** Čistá | Čistá, Kůzová | Hořovičky | Břežany. Model window 14:00–16:00 (anchor set by hand).
- **Card:** Čistá – Kůzová – Lhota – Žďár – Jesenice – Hořovičky (LEXTRANS), every 2 hours on one bus: Čistá :15 (12:15, 14:15, 16:15), Hořovičky :08 (13:08, 15:08), modelled at 14:30 (the 16:00 window holds only the 17:15 by the shorter path, 7 min off). The Čistá – Šípy – Břežany loop (15:30 / 15:57) is 573 Šípy, every 480, the only service of Všesulov, obchod and of Šípy's own stops. Listed: Čistá 18:00 → Kůzová → Čistá, Čistá 8:47 → Břežany, Břežany 7:32 → Čistá.
- **Reasoning (1 Nov):** Čistá – Kůzová – Lhota – Žďár – Jesenice – Hořovičky (LEXTRANS) and the Čistá – Šípy – Břežany loop. Every 2 h, one bus: Čistá :15 (12:15, 14:15, 16:15) → Hořovičky :08, which turns at once (13:08, 15:08; 17:15 by the shorter path not via Velká Chmelištná and Otěvěky, 40 min). Anchor set to 14:30: the auto 16:00 window holds only the 17:15 (7 min off :08); the line's own pattern is the 14:15 / 15:08 round. The Šípy loop (Čistá 15:30 → Všesulov obchod, Šípy, Bělbožice, zahradnictví → Břežany 15:54, Břežany 15:57 → Čistá; 7:05 / 7:32 in the morning) is another bus and the only service of Všesulov, obchod (Šípy's stops are also on the Šípy trips of 571), so it is 573 Šípy, every 480 (on the owner checks). Listed: Čistá 18:00 → Kůzová → 18:26 Čistá (stops on 573), Čistá → Břežany 8:47 and Břežany → Čistá 7:32 direct.
- **Changed on 2 Nov:** 0-minute turn at Hořovičky with the real running time (53) and `lay` 0 (was rt 52); owner checks removed.
- **573**, every 120, 1 bus: Čistá :15 even hours → Hořovičky via Kůzová, Žďár and Jesenice (53 min); Hořovičky :08 odd hours back via Jesenice, Chotěšov (52 min), a 0-minute turn as in the timetable.
  - Step 4: Čistá → Hořovičky: window slots 14:15 / real 14:15, filled 1/1; day exact 3, within 3 3 of 4; off 12–20 h none; Hořovičky → Čistá: window slots 15:08 / real 15:08, filled 1/1; day exact 2, within 3 2 of 4; off 12–20 h 17:15.
- **573 Šípy**, every 480, 1 bus: Čistá 15:30 → Všesulov, obchod, Šípy, Bělbožice → Břežany (24 min); Břežany 15:57 → Čistá direct (5 min).
  - Step 4: Čistá → Břežany: window slots 15:30 / real 15:30, filled 1/1; day exact 1, within 3 1 of 2; off 12–20 h none; Břežany → Čistá: window slots 15:57 / real 15:57, filled 1/1; day exact 1, within 3 1 of 2; off 12–20 h none.

### 574 Radnice - Liblín - Zvíkovec - Skryje - Křivoklát (Transdev Střední Čechy s.r.o.; 1 trips, 1 in 13–19)
- **Core points:** Skryje | Nezabudice | Křivoklát, železniční zastávka. Model window 15:30–17:30 (the line's anchor).
- **Card:** Skryje – Hřebečníky, Týřovice – Nezabudice, U Rozvědčíka – Nezabudice – Křivoklát, one trip a day (Skryje 17:20 → Křivoklát, železniční zastávka 17:53; Plzeňský licence 471574). Kept for Nezabudice, U Rozvědčíka, which no other line serves (owner, 2 Nov 2026: "Yes, serve every place"): every 480 at the real 17:20, with an untimed return.
- **Reasoning (1 Nov):** Skryje – Hřebečníky, Týřovice – Nezabudice (U Rozvědčíka, přívoz) – Roztoky, Višňová – Křivoklát: one trip a day (Skryje 17:20 → Křivoklát, železniční zastávka 17:53; licence 471574, Plzeňský kraj). Nezabudice, U Rozvědčíka has no other line, so it is modelled as the 402B case: every 480 at the real 17:20 (repeats 1:20, 9:20) with an untimed return (no trip runs back; an empty return is allowed for a stop nobody else serves). On the owner checks (the alternative is a coverage exception, 1 bus fewer).
- **Changed on 2 Nov:** Kept by the owner's decision of 2 Nov (the only service of Nezabudice, U Rozvědčíka), overriding the review's FIX; owner check removed.
- **574**, every 480, 1 bus: Skryje 17:20 → Nezabudice, U Rozvědčíka → Křivoklát, železniční zastávka (33 min); back untimed, as no trip runs back (33 min assumed).
  - Step 4: Skryje → železniční zastávka: window slots 17:20 / real 17:20, filled 1/1; day exact 1, within 3 1 of 1; off 12–20 h none; železniční zastávka → Skryje untimed.

### 575 Rakovník - Pavlíkov - Zvíkovec (Transdev Střední Čechy s.r.o.; 18 trips, 8 in 13–19)
- **Core points:** Rakovník, autobusové stanoviště | Pavlíkov, pošta | Slabce, pošta | Slabce, Kostelík | Zvíkovec. Model window 15:30–17:30 (the line's anchor).
- **Card:** Rakovník – Pavlíkov – Panoší Újezd – Slabce – Kostelík – Zvíkovec: Rakovník 14:35 → Zvíkovec → 15:35 → Rakovník on one bus, Rakovník 17:00 → Slabce, Kostelík → 17:50 back, and Pavlíkov trips 15:00 → Tytry, 15:36 → Rakovník. Every 144 holds both afternoon trips out (14:35, 17:00) on one bus; the way back is shown via Pavlíkov, Tytry, Skřivaň and Chlum, which no other line serves. Off the pattern: Zvíkovec 12:26, Kostelík 17:50; listed: the Pavlíkov trips and Slabce, pošta 13:53 and 16:00.
- **Reasoning (1 Nov):** Rakovník – Pavlíkov (Chlum, Skřivaň, Tytry) – Panoší Újezd – Slabce (pošta, Kostelík) – Zvíkovec. Afternoon: Rakovník 14:35 → Zvíkovec 15:27 → 15:35 → Rakovník 16:24 (one bus), Rakovník 17:00 → Slabce, Kostelík 17:50 → 17:50 → Rakovník; Zvíkovec 12:26 → Rakovník via Tytry, Skřivaň and Chlum; Pavlíkov shuttles Rakovník 15:00 → Tytry 15:35, Tytry 15:36 → Rakovník; Rakovník 16:00 → Slabce, pošta; Slabce 13:53 → Rakovník (the 576 13:30 bus). Every 144 fits clearly better than the plain intervals (the method's 72 / 383 rule): Rakovník 14:35 and 16:59 (the 17:00, 1 min) out, Zvíkovec 15:35 back (read at Slabce, Kostelík 15:45, so the Kostelík trips count), one bus; every 120 or 240 hold one of the two out trips only. Off 12–20 h: Zvíkovec 12:26, Kostelík 17:50 (Zvíkovec-time 17:40); listed: the Pavlíkov shuttles and the 16:00 / 13:53 Slabce, pošta trips (stops on 575, 576, 572).
- **Changed on 2 Nov:** Owner check removed: the way back via Tytry, Skřivaň and Chlum is the 1 Nov variant-path rule, named on the card with its running time.
- **575**, every 144, 1 bus: Rakovník 14:35 (16:59 a period later stands for the real 17:00) → Zvíkovec via Pavlíkov and Slabce (52 min); Zvíkovec 15:35 back via Tytry, Skřivaň and Chlum, the 12:26 trip's path (69 min; the 15:35 itself runs direct in 49 min).
  - Step 4: autobusové stanoviště → Zvíkovec: window slots 16:59 / real 17:00, filled 1/1; day exact 1, within 3 2 of 5; off 12–20 h none; Zvíkovec → autobusové stanoviště: window slots 15:35 / real 15:35, filled 1/1; day exact 1, within 3 1 of 5; off 12–20 h 12:26, 17:40.

### 576 Rakovník - Slabce - Skryje (Transdev Střední Čechy s.r.o.; 16 trips, 6 in 13–19)
- **Core points:** Rakovník, autobusové stanoviště | Slabce, pošta | Skryje. Model window 15:30–17:30 (the line's anchor).
- **Card:** Rakovník – Pavlíkov – Panoší Újezd – Slabce – Hracholusky – Hřebečníky – Skryje. The buses sleep at Skryje, so the afternoon sends more out (13:30 and 15:30 to Slabce; 14:40, 16:30, 18:30 to Skryje) than come back (16:04): timed at the rate towards Rakovník, every 240 on the real round Rakovník 14:40 → Skryje 15:24, Skryje 16:04 → Rakovník. Rakovník 16:30 and 18:30 (buses going home) and Skryje 12:34 are off the pattern.
- **Reasoning (1 Nov):** Rakovník – Pavlíkov – Panoší Újezd – Slabce – Hracholusky – Hřebečníky – Skryje. Afternoon: Rakovník 13:30 and 15:30 → Slabce, pošta; 14:40, 16:30, 18:30 → Skryje; Skryje 16:04 → Rakovník (and 12:34, 20:19). An outstation line: the buses sleep at Skryje (4:27, 6:39 start there; 22:30 ends there), so the afternoon sends more out than come back. Timed at the inbound rate (one per 4 h): every 240, Rakovník 14:40 / Skryje 16:04, the real round of one bus (14:40 → 15:24, 16:04 → 16:54). Off the pattern: Rakovník 16:30, 18:30 (buses going home), Skryje 12:34; listed: the Slabce, pošta shorts 13:30, 15:30 (the 13:30 bus comes back as 575 13:53).
- **Changed on 2 Nov:** Owner check removed: the outstation rule decides.
- **576**, every 240, 1 bus: Rakovník 14:40 → Skryje via Pavlíkov, Slabce and Hracholusky (46 min); Skryje 16:04 back (50 min).
  - Step 4: autobusové stanoviště → Skryje: window slots – / real 16:30, filled 0/0; day exact 1, within 3 1 of 7; off 12–20 h 16:30, 18:30; Skryje → autobusové stanoviště: window slots 16:04 / real 16:04, filled 1/1; day exact 1, within 3 1 of 5; off 12–20 h 12:34.

### 577 Rakovník - Stochov (Transdev Střední Čechy s.r.o.; 9 trips, 4 in 13–19)
- **Core points:** Rakovník, autobusové stanoviště | Nový Dům | Lány, náměstí | Stochov, Slovanka II. Model window 15:30–17:30 (the line's anchor).
- **Card:** Rakovník – Nový Dům – Ruda – Lány – Stochov, Slovanka II: Rakovník 12:50, 14:50, 16:35 out, Stochov 14:40 (from Stochov, náměstí) and 16:56 back. It runs through as 304 at Stochov (577 14:50 → 304 15:24 to Prague; 304 16:30 from Zličín → 577 16:56), so it is timed on its own pair, every 240: Rakovník 16:35, Stochov 14:46. Off the pattern: Rakovník 12:50, 14:50; Stochov 16:56.
- **Reasoning (1 Nov):** Rakovník – Nový Dům – Ruda (sv. Alžběta, osada Brejl) – Lány – Stochov, Slovanka II (– Stochov, nám.). Afternoon: Rakovník 12:50 (→ Stochov, nám.), 14:50, 16:35 (→ nám.); Stochov, nám. 14:40 (Slovanka 14:46) and Slovanka 16:56 → Rakovník. Step 5b: the 0-minute chain test at Stochov, Slovanka II shows 577 running through as 304: 577 14:50 → Slovanka 15:22 goes on as 304 15:24 → Vypich, and 304 Zličín 16:30 → Slovanka 16:55 comes back as 577 16:56 (also 6:46, 8:11 in the morning). 577 is kept its own Simutrans line (one line per real line; the through circuit would not save a bus) and timed every 240 on its other pair: Rakovník 16:35 / Slovanka II 14:46, both exact (6:46 too), one bus. Off: Rakovník 12:50, 14:50 (the 304 through bus), Stochov 16:56 (from 304), 8:11. Ruda, osada Brejl has no other line in okres Rakovník; Lány, samota Píně, Vašírovská lísa, Lesní, náměstí (okres Kladno) are served only by 577 too.
- **577**, every 240, 1 bus: Rakovník 16:35 → Stochov, Slovanka II via Nový Dům, Ruda, osada Brejl and Lány (32 min; the real trip goes on to Stochov, náměstí); Stochov, Slovanka II 14:46 back (33 min).
  - Step 4: autobusové stanoviště → Slovanka II: window slots 16:35 / real 16:35, filled 1/1; day exact 1, within 3 1 of 3; off 12–20 h 12:50, 14:50; Slovanka II → autobusové stanoviště: window slots – / real 16:56, filled 0/0; day exact 2, within 3 2 of 4; off 12–20 h 16:56.

### 578 Rakovník - Nezabudice - Křivoklát - Rakovník (Transdev Střední Čechy s.r.o.; 7 trips, 3 in 13–19)
- **Core points:** Rakovník, autobusové stanoviště | Pavlíkov, pošta | Nezabudice | Křivoklát, železniční zastávka | Nový Dům. Model window 14:30–16:30 (anchor set by hand).
- **Card:** A circular line Rakovník – Pavlíkov – Všetaty – Velká Buková – Nezabudice – Křivoklát – Městečko – Ruda – Nový Dům – Rakovník, run both ways round (6:10 and 12:00 via Nový Dům first, 12:15 and 14:45 via Pavlíkov first, 77 min), plus a Nezabudice trip 17:20 / 17:50. One circuit every 240 at the real 14:45, modelled at 15:00 (the 16:30 window holds only the Nezabudice trip, whose stops are on the circuit); 12:00 and 12:15 are off the pattern.
- **Reasoning (1 Nov):** Rakovník – Pavlíkov – Všetaty – Velká Buková – Nezabudice – Křivoklát – Městečko – Ruda – Nový Dům – Rakovník, a circular line both ways round: 6:10 and 12:00 via Nový Dům first, 12:15 and 14:45 via Pavlíkov first (77 min); plus Rakovník 17:20 → Nezabudice → 17:50 → Rakovník (out and back on the circuit's own stops) and Křivoklát 4:33 → Rakovník. Modelled as one circuit leg Rakovník → Rakovník every 240 at the 14:45 (anchor 15:00 by hand: the auto anchor 16:30 sits on the 17:20 shuttle, whose stops are on the circuit; the 282 rule). Off: 12:00, 12:15; listed: the 17:20 / 17:50 Nezabudice shuttle. Všetaty, háj. Čepiny, Malá Buková odb., Křivoklát Písky, Městečko Požáry and Pařeziny have no other line.
- **578**, every 240, 1 bus: Rakovník 14:45 round via Pavlíkov, Všetaty, Nezabudice, Křivoklát, Městečko and Nový Dům back to Rakovník (77 min).
  - Step 4: autobusové stanoviště → autobusové stanoviště: window slots 14:45 / real 14:45, filled 1/1; day exact 1, within 3 1 of 4; off 12–20 h 12:00, 12:15.

### 579 Skryje - Křivoklát - Branov (Autobusová doprava Kohout s.r.o.; 19 trips, 7 in 13–19)
- **Core points:** Branov | Roztoky, Chaloupky | Křivoklát, železniční zastávka | Nezabudice | Roztoky, Leontýn. Model window 14:00–16:00 (anchor set by hand).
- **Card:** Branov – Karlova Ves – Roztoky – Křivoklát – Velká Buková – Nezabudice and Branov – Placanda – Karlov – Leontýn, one bus in a fixed sequence from 12:03 to 17:12. Modelled as that bus's circuit every 240, at 14:30: Branov 14:35 → Nezabudice, Nezabudice 15:23 → Branov, Branov 17:30 → Leontýn, Leontýn 18:17 → Branov (the real 13:30 and 14:17 a period earlier). Off the pattern: Branov 12:03, Nezabudice 12:50; listed: the Amalín loop 16:05 / 16:28 and Branov 16:55 → Roztoky, škola.
- **Reasoning (1 Nov):** Branov – Karlova Ves – Roztoky (Chaloupky, škola) – Křivoklát – Městečko – Velká Buková – Nezabudice, and Branov – Placanda – Karlov – Leontýn (Kohout). One bus runs a fixed sequence from Branov 12:03 to 17:12: Branov 12:03 → Nezabudice 12:49, 12:50 → Branov 13:29, 13:30 → Leontýn 13:47, 14:17 → Branov 14:34, 14:35 → Nezabudice 15:21, 15:23 → Branov 16:02, 16:05 → Amalín 16:26 → 16:28 → Branov 16:51, 16:55 → Roztoky, škola (the chain test: 4 of 8 Branov arrivals leave again within 2 min). Modelled as that bus's circuit on the shortest period that holds it (Step 8, the 418 case): every 240, Branov → Nezabudice 14:35, Nezabudice → Branov 15:23, Branov → Leontýn 13:30 (17:30 in the period), Leontýn → Branov 14:17 (18:17), all exact; one bus (pattern_need, Branov twice). Anchor set to 14:30 (the auto 16:00 window holds only the Amalín loop and the Roztoky trip). Off: Branov 12:03, Nezabudice 12:50; listed: the Amalín loop 16:05 / 16:28 (Amalín on 578; its Roztoky most / U Eremita on 579) and Branov 16:55 → Roztoky, škola.
- **579**, every 240, 1 bus: Branov → Nezabudice via Roztoky and Křivoklát (46 min), Nezabudice → Branov via Roztoky, Višňová (39 min), Branov → Roztoky, Leontýn via Placanda and Karlov and back (17 min each).
  - Step 4: Branov → Nezabudice: window slots 14:35 / real 14:35, filled 1/1; day exact 1, within 3 1 of 3; off 12–20 h 12:03; Nezabudice → Branov: window slots 15:23 / real 15:23, filled 1/1; day exact 1, within 3 1 of 2; off 12–20 h 12:50; Branov → Leontýn: window slots – / real –, filled 0/0; day exact 1, within 3 1 of 2; off 12–20 h none; Leontýn → Branov: window slots 14:17 / real 14:17, filled 1/1; day exact 1, within 3 1 of 2; off 12–20 h none.

### 581 Senomaty - Rakovník - Nové Strašecí (Transdev Střední Čechy s.r.o.; 30 trips, 10 in 13–19)
- **Core points:** Senomaty | Lubná | Rakovník, autobusové stanoviště | Lužná, železniční stanice | Lišany, u rybníka | Rynholec | Nové Strašecí, Pecínov. Model window 15:30–17:30 (anchor set by hand).
- **Card:** Senomaty – Lubná – Rakovník – Lužná – Lišany – Ruda – Nové Strašecí, Pecínov: east of Rakovník the Lišany trips leave hourly at :30 from 15:30 and the Nové Strašecí trips at 13:15 and 16:30; west of Rakovník single trips to Senomaty. Three Simutrans lines, one per end: 581 (Lišany), 581 Nové Strašecí, and 581 Senomaty, a ring out on 581 and back on 561 (581 17:10 reaches Senomaty 17:32 and goes on as 561 17:33; 561 12:45 comes back as 581 13:18). Off the pattern or listed: Lubná 14:10 → Lišany, Lišany 14:55, Rakovník 12:00 and 13:15 to Nové Strašecí, Rynholec 12:54 → Lubná, Rakovník 14:50 → Senomaty, Senomaty 13:18.
- **Reasoning (1 Nov):** Senomaty – Lubná – Rakovník – Lužná – Lišany – Ruda – Nové Strašecí (Rynholec, Pecínov). East of Rakovník: shuttles Rakovník → Lišany, u rybníka at :30 (15:30, 17:30, 20:30; 9:40, 6:05) and back from Lišany (14:55, 16:25, 10:25, 8:15, 7:12); Nové Strašecí trips Rakovník 12:00, 16:30 → Rynholec and 13:15 → Pecínov (out via Lišany, back via Lužná, lesní správa without Lišany), Rynholec 12:54 → Lubná, Pecínov 14:07 → Rakovník → Senomaty. West: Rakovník 11:45, 14:50, 17:10 → Senomaty / Hostokryje, Senomaty 13:18 → Rakovník. Three Simutrans lines (Ex4, one per end): 581 (Lišany, every 120: Rakovník 15:30, Lišany 16:25), 581 Nové Strašecí (every 240: Rakovník 16:30, Pecínov 14:07) and 581 Senomaty (every 240, a ring). Step 5b at Senomaty: 581 17:10 → Senomaty 17:32 goes on as 561 17:33 → Rakovník, and 561 Šamotka 12:45 → Senomaty 13:17 comes back as 581 13:18 (0-minute chains, 2 of 2): 581 Senomaty runs out on 581's path (Lubná, Hostokryje, Brant) and back on 561's (Zákonův mlýn, nemocnice), one bus; the plain Rakovník – Senomaty row that passes Step 4 needs 2 buses. Anchor set to 16:00: the auto 13:40 window is the through trips (Rynholec – Lubná, Pecínov – Senomaty, Lubná – Lišany) and the 13:15 Pecínov trip; the Lišany shuttle runs 15:30–17:30. At Rakovník towards Lužná the rows interleave (:30 odd hours Lišany, 16:30 / 20:30 Nové Strašecí). Off / listed: 14:30 Lubná → Lišany, 14:55 Lišany, 12:00 / 13:15 Nové Strašecí, 12:54 Rynholec → Lubná, 14:50 Rakovník → Senomaty, 13:18 Senomaty (all stops on the three rows).
- **Changed on 2 Nov:** Owner check removed: the ring has the Step 5b evidence (0-minute chains 2 of 2) and saves a bus.
- **581**, every 120, 1 bus: Rakovník :30 odd hours → Lišany, u rybníka via Lužná (20 min), Lišany :25 even hours back (20 min).
  - Step 4: autobusové stanoviště → u rybníka: window slots 15:30 / real 15:30, filled 1/1; day exact 2, within 3 2 of 7; off 12–20 h 14:30; u rybníka → autobusové stanoviště: window slots 16:25 / real 16:25, filled 1/1; day exact 3, within 3 3 of 8; off 12–20 h 14:55.
- **581 Nové Strašecí**, every 240, 1 bus: Rakovník 16:30 → Lužná, Lišany, Ruda, Nové Strašecí → Pecínov (41 min; the real trip ends at Rynholec); Pecínov 14:07 → Nové Strašecí, Lužná → Rakovník, not via Lišany (43 min).
  - Step 4: autobusové stanoviště → Pecínov: window slots 16:30 / real 16:30, filled 1/1; day exact 1, within 3 1 of 4; off 12–20 h 12:00, 13:15; Pecínov → autobusové stanoviště: window slots – / real –, filled 0/0; day exact 1, within 3 1 of 2; off 12–20 h none.
- **581 Senomaty**, every 240, 1 bus: Rakovník 17:10 → Lubná, Hostokryje, Brant → Senomaty on 581 (21 min); Senomaty 17:33 → Zákonův mlýn, nemocnice → Rakovník on 561's trip (12 min).
  - Step 4: autobusové stanoviště → Senomaty: window slots 17:10 / real 17:10, filled 1/1; day exact 1, within 3 1 of 2; off 12–20 h 14:50; Senomaty → autobusové stanoviště: window slots – / real –, filled 0/0; day exact 1, within 3 1 of 6; off 12–20 h 13:18, 15:13, 19:18.

### 584 Rakovník - Mutějovice,Lhota pod Džbánem - Vinařice (Transdev Střední Čechy s.r.o.; 20 trips, 10 in 13–19)
- **Core points:** Rakovník, autobusové stanoviště | Krupá, Šustna | Mutějovice | Mutějovice, Lhota p.Džbánem | Vinařice [pásmo 7 2]. Model window 13:00–15:00 (anchor set by hand).
- **Card:** Rakovník – Lišany – Krupá – Mutějovice – Lhota pod Džbánem, and from Mutějovice via Třeboc, Džbán, Kroučová and Pochvalov to Vinařice. Rakovník 12:15 and 13:15 run to Lhota and turn at once as 13:00 and 14:00; Rakovník 14:30 runs to Vinařice and turns at once as 15:25. Two Simutrans lines: 584 (Lhota, every 120, modelled at 13:30 where the Lhota trips run) and 584 Vinařice (every 480); off the pattern or listed: Rakovník 12:15, 15:30 and 16:30 to Lhota or Mutějovice, Lhota 13:00, Krupá, Šustna 16:51 and 18:51 → Rakovník.
- **Reasoning (1 Nov):** Rakovník – Lišany – Krupá – Hředle – Mutějovice – Lhota pod Džbánem, and Mutějovice – Třeboc, Džbán – Kroučová – Pochvalov – Smilovice – Kozojedy – Vinařice. Lhota: Rakovník 12:15, 13:15 → Lhota (via Nesuchyně, 45 min), which turn at once as 13:00, 14:00 → Rakovník (4 of 4 arrivals at Lhota leave within 0 min), then 15:30 → Lhota 16:07 → Mutějovice; 16:30 → Mutějovice; Krupá, Šustna 16:51, 18:51 → Rakovník. Vinařice: Rakovník 14:30 → Vinařice 15:25 → 15:25 → Rakovník 16:20 (also 5:35, and 4:12, 6:27 back). Two Simutrans lines: 584 (Lhota, every 120: Rakovník 13:15, Lhota 14:00) and 584 Vinařice (every 480: Rakovník 14:30, Vinařice 15:25). Anchor set to 13:30: the hourly Lhota pattern runs 12:15–14:35, and at 16:00 no trip leaves Lhota for Rakovník. Off: Rakovník 12:15, 15:30; Lhota 13:00. Listed: 16:07 Lhota → Mutějovice, 16:30 → Mutějovice, the Krupá → Rakovník trips (stops on 584, 711).
- **Changed on 2 Nov:** 0-minute turns at Lhota and Vinařice with the real running times (45, 55) and `lay` 0 (were 44, 54); owner checks removed.
- **584**, every 120, 1 bus: Rakovník 13:15 → Lhota via Krupá, Mutějovice and Nesuchyně (45 min); Lhota 14:00 back (35 min), a 0-minute turn as in the timetable.
  - Step 4: autobusové stanoviště → Lhota p.Džbánem: window slots 13:15 / real 13:15, filled 1/1; day exact 1, within 3 1 of 4; off 12–20 h 12:15, 15:30; Lhota p.Džbánem → autobusové stanoviště: window slots 14:00 / real 13:00 14:00, filled 1/1; day exact 1, within 3 1 of 2; off 12–20 h 13:00.
- **584 Vinařice**, every 480, 1 bus: Rakovník 14:30 → Vinařice via Mutějovice, Kroučová and Pochvalov (55 min); Vinařice 15:25 back (55 min), a 0-minute turn as in the timetable.
  - Step 4: autobusové stanoviště → Vinařice [pásmo 7 2]: window slots 14:30 / real 14:30, filled 1/1; day exact 1, within 3 1 of 2; off 12–20 h none; Vinařice [pásmo 7 2] → autobusové stanoviště: window slots – / real –, filled 0/0; day exact 1, within 3 1 of 2; off 12–20 h none.

### 711 Louny - Ročov - Rakovník (Dopravní společnost Ústeckého kraje, příspěvková organizace; 26 trips, 9 in 13–19)
- **Core points:** Louny, Luna | Louny, autobusové nádraží | Třeboc | Rakovník, autobusové stanoviště | Rakovník, železniční zastávka západ. Model window 14:20–16:20 (the line's anchor).
- **Card:** Louny, Luna – Louny – Cítoliby – Ročov – Třeboc – Hředle – Krupá – Lišany – Rakovník, run by the Ústecký kraj: through trips Rakovník 13:00, 14:20 (from železniční zastávka západ, to Louny, Luna), 17:30 and Louny 12:25 (from Luna), 16:00, plus Louny – Třeboc and Louny – Domoušice, Solopysky trips. 711 runs every 240 on one bus's real round (Rakovník, železniční zastávka západ 14:20 → Louny, Luna; Louny 16:00 → Rakovník), so Třeboc, Louny, sokolovna and Luna, Prokopova and sídliště gen.Kholla are on a line; 711 Domoušice, every 480, is the Louny 14:00 → Solopysky → 14:30 → Louny round, the only service of Solopysky. Off the pattern: Rakovník 13:00, 17:30, Louny 12:30; the Louny – Třeboc trips are listed.
- **Reasoning (1 Nov):** Louny – Cítoliby – Líšťany – Brodec – Ročov – Třeboc – Hředle – Krupá – Lišany – Rakovník (AS / žz západ), DSÚK (Ústecký kraj). Through trips: Rakovník 13:00, 14:20 (from žz západ, AS 14:35), 17:30 → Louny; Louny 12:25 (AN 12:30), 16:00 → Rakovník (12:25 on to žz západ); plus Louny – Třeboc and Louny – Domoušice shorts (Louny 15:00, 17:30, 19:00 → Třeboc; Třeboc 16:00, 19:30 → Louny; 14:00 / 14:30 Domoušice). Třeboc and Třeboc, obchod have no other line, so the through pair is kept (Step 8): every 240, žz západ 14:20 (read at Rakovník AS 14:35, knot_rt 15) and Louny 16:00, the real round of one bus (Louny 12:25 → žz 13:40, 14:20 → Louny 15:35, 16:00 → Rakovník 16:59). The Rakovník end is žz západ so Prokopova, gen.Kholla and žz západ are on the line (570's Step 8 needs Prokopova). Off 12–20 h: Rakovník 13:00, 17:30; Louny 12:30; listed: the Louny – Třeboc / Domoušice shorts (Ústecký kraj; Třeboc is on the line).
- **Changed on 2 Nov:** The out-of-kraj stops now count: the Louny end is Louny, Luna (out core_to Louny, autobusové nádraží; back knot there), so Louny, sokolovna and Luna are on the line; new 711 Domoušice, every 480, Louny 14:00 → Solopysky 14:30 → Louny (0-minute turn, `lay` 0; 6:00 / 6:30 exact too), the only service of Domoušice, Solopysky (1.9 km from Ročov, Třebocká, so not a roadside case). +1 bus.
- **711**, every 240, 1 bus: Rakovník, železniční zastávka západ 14:20 (autobusové stanoviště 14:35) → Louny, autobusové nádraží → Louny, Luna via Třeboc and Ročov (78 min); Louny, Luna 15:55 → Louny, autobusové nádraží 16:00 → Rakovník (the real 16:00 starts at the autobusové nádraží and ends at the autobusové stanoviště).
  - Step 4: železniční zastávka západ → Luna: window slots 14:20 / real 14:20, filled 1/1; day exact 1, within 3 1 of 7; off 12–20 h 12:45, 17:15; Luna → železniční zastávka západ: window slots 15:55 / real 15:55, filled 1/1; day exact 2, within 3 2 of 6; off 12–20 h 12:25.
- **711 Domoušice**, every 480, 1 bus: Louny, autobusové nádraží 14:00 → Ročov → Domoušice, Solopysky (30 min) and back at 14:30 (30 min), a 0-minute turn as in the timetable; the 6:00 / 6:30 round is exact too.
  - Step 4: autobusové nádraží → Solopysky: window slots – / real –, filled 0/0; day exact 2, within 3 2 of 2; off 12–20 h none; Solopysky → autobusové nádraží: window slots 14:30 / real 14:30, filled 1/1; day exact 2, within 3 2 of 2; off 12–20 h none.

### 760 Rakovník - Podbořany (Transdev Střední Čechy s.r.o.; 26 trips, 11 in 13–19)
- **Core points:** Rakovník, autobusové stanoviště | Kolešovice | Hořovičky | Podbořany, autobusové nádraží. Model window 15:30–17:30 (the line's anchor).
- **Card:** Rakovník – Olešná – Kněževes – Kolešovice – Hořovičky – Kryry – Vroutek – Podbořany, hourly: Rakovník :30, and towards Rakovník Hořovičky :44 from 11:44 to 18:44, exact. Podbořany's minutes vary with the path inside the town (:04, :07, :15), so the way back is read at Hořovičky; the way back is shown by the 16:15 trip's path via Podbořany, nemocnice, which no other line serves. 560 runs the same road at the other half hour.
- **Reasoning (1 Nov):** Rakovník – Olešná – Chrášťany – Kněževes – Kolešovice – Hořesedly – Hořovičky – Kryry – Vroutek – Podbořany. Hourly all day: Rakovník :30 (8:30, 10:30, 12:30–16:30, 18:30; 11:35, 17:30 none), Hořovičky :44 towards Rakovník from 11:44 to 18:44, exact. The Podbořany departures vary (:04, :07, :15) with the path inside the Podbořany area (via Očihov or not, via nemocnice), so the way back is read at Hořovičky (mixed origins), and Podbořany's time is Hořovičky − 40 = :04. Off: Rakovník 4:15, 5:10, 6:15, 11:35, 22:35; Podbořany 4:24, 5:28, 6:10. 560 shares Rakovník – Kolešovice at the other half hour.
- **Changed on 2 Nov:** The out-of-kraj stops now count: the way back is shown via Podbořany, nemocnice (`stops_via`), timed so the bus passes Hořovičky at :44 (`knot_rt` 29: Podbořany :15, the real 16:15, 64 min in all; most real trips leave at :04 via Vroutek and Kryry, which are on the way out). Path flag on the 17:15 slot (the 17:07 via Vroutek). Need unchanged, 3.
- **760**, every 60, 3 buses: Rakovník :30 → Podbořany via Kolešovice, Hořovičky, Kryry and Vroutek (75 min); back from Podbořany :15 via Podbořany, nemocnice (the real 16:15, 29 min to Hořovičky :44, 64 min in all), so the bus passes Hořovičky at :44 as all the real trips do (most leave Podbořany at :04 via Vroutek and Kryry, 40 min to Hořovičky).
  - Step 4: autobusové stanoviště → autobusové nádraží: window slots 15:30 16:30 / real 15:30 16:30, filled 2/2; day exact 8, within 3 8 of 12; off 12–20 h none; autobusové nádraží → autobusové stanoviště: window slots 16:15 17:15 / real 16:15 17:15, filled 2/2; day exact 9, within 3 9 of 12; off 12–20 h none.

## Not modelled
- **570** (Rakovník - Čistá - Kralovice): Step 8: three afternoon trips (Kralovice 12:40 → Rakovník, Rakovník 14:15 → Kralovice, Kralovice 15:10 → Čistá, Čistá 18:27 → Rakovník) on 404's corridor; every stop it serves 13:00–19:00 is on modelled lines: Kralovice, Kožlany, Břežany, Čistá, Všesulov, Zavidov, Petrovice, Příčina and Senomaty, Hostokryje, rozcestí on 404; Lubná, Lubná, pod vrškem and Lubná, závod on 562 Lubná and 581 Senomaty; Rakovník, zem.závod and sídliště gen.Kholla on 581 Senomaty; Rakovník, Prokopova and železniční zastávka západ on 711. Its 12:40 from Kralovice fills 404's midday gap (404 leaves Kralovice 11:40 and 14:40).
- **XS75 (992075)** Beroun – Nižbor (České dráhy): replacement bus for engineering works, not modelled automatically (`00_config`).
- **561 Řeřichy** (a Simutrans line of 1 Nov) was dropped on 2 Nov: no stop of its own (Step 8).

## Checks across the sheet

**Legs with no slot in their window** (run_oblast's "no slot in the window"; Step 4 says nothing about them), with the real trip
each slot is: 577 back = Stochov, Slovanka II 14:46 (the 14:40 from Stochov, náměstí; 6:46 is exact too; the window's real
16:56 is the 304 bus coming back as 577); 561 back = Kolešovice 20:30 (16:30 is its repeat); 563 out = Rakovník 17:30 (5:30
too); 571 out = Rakovník 14:50; 572 Slabce out = Rakovník 18:30; 576 out = Rakovník 14:40 (the window's real 16:30 is a bus
going home to Skryje); 579 Branov → Leontýn = Branov 13:30; 581 Nové Strašecí back = Pecínov 14:07; 581 Senomaty back = the 561
trip Senomaty 17:33; 584 Vinařice back = Vinařice 15:25; 711 Domoušice out = Louny 14:00 (6:00 too).

**Legs read at a midpoint** (`audit-branch.txt`, all `[ok]`): 304 out (core_to Zličín: the 15:30 Zličín trip), 404 out
(core_to Rakovník: the 14:40 Rakovník trip), 560 out (core_to Hořovičky) and back (knot Hořovičky), 760 back (knot Hořovičky),
561 out (core_to Řeřichy), 563 back (core_to Milostín), 575 out (core_to Slabce, Kostelík) and back (knot Slabce, Kostelík),
581 Nové Strašecí out (core_to Rynholec), 711 out (knot Rakovník, autobusové stanoviště; core_to Louny, autobusové nádraží) and
back (knot Louny, autobusové nádraží; core_to Rakovník, autobusové stanoviště). In every case the trips that end or start short
do so on the line's own path; branches have their own Simutrans lines or `notvia`.

**Path audit flags** (`audit-path.txt`, 3): 415 out, the 16:10 slot trip takes the main road past the Chbany rozcestí stops
(Přeskaky, Vadkovice, Malé Krhovice, rozcestí) while the row is shown via the Chbany villages; those rozcestí stops are on the
way back. 575 out, the 16:59 slot is the 17:00 Rakovník → Slabce, Kostelík trip via Pavlíkov, Skřivaň and Tytry, which are on
the way back. 760 back, the 17:15 slot stands for the 17:07 Podbořany trip via Podbořany, OSP, ČSAD, Vroutek and Kryry, which
are on the way out.

**Anchors set by hand:** 305 15:00 (16:00 holds Zličín's missing 17:05); 404 15:00 and 417 14:00 (the auto ones, written down);
415 16:00 (13:00–15:00 is the Nové Strašecí variant); 572 15:00 (the real 15:00 / 15:30 turn); 573 14:30 (16:00 holds only the
17:15 by the shorter path); 578 15:00 (16:30 is the Nezabudice trip on the circuit's stops); 579 14:30 (16:00 holds only the
Amalín loop); 581 16:00 (13:40 is the through trips); 584 13:30 (no Lhota → Rakovník trip after 14:00). Own `window`: 572 Slabce
15:30–17:30.

**Running times and turns set by hand:** 415 out rt 118 (the 14:15 trip's own time on the path shown; the builder's median
mixed in the 6:45 via Nové Strašecí, 133); 575 back rt 69 (the 12:26 trip on the path shown; the builder gave 74); 711 `knot_rt`
15 (Rakovník, železniční zastávka západ 14:20 → autobusové stanoviště 14:35); 760 `knot_rt` 29 (Podbořany 16:15 → Hořovičky 16:44
via nemocnice); `lay` 0 on the legs leaving Hořovičky (573), Lhota and Vinařice (584) and Domoušice, Solopysky (711 Domoušice):
real 0-minute turns, real running times, as the brief now says. This assumes the fork's automatic "Leave up to" lets a bus that
arrives on the real minute leave although the loop rule types the departure 1 min early; it is an engine question, noted once in
`notes`, to confirm when an engine session is live.

**Prague end.** 304, 305, 404, 415, 417 are timed at both terminals (Zličín, Kukulova). 304's buses arrive at Praha, Vypich and
leave from Praha, Kukulova (`terminus_alias`); the move sits inside 304's Kukulova waits (14, 14, 9 min).

**Bunching.** Every same-minute departure at Rakovník, autobusové stanoviště in the game is also real (15:30: 304, 581 and
404 passing; 15:00: 560 and 572; 16:30: 581 Nové Strašecí and 404 passing), as the review checked; 560 / 760 interleave as the
real timetable does.

## Coverage (Step 9)

Stops of okres Rakovník served 13:00–19:00 and on no modelled Simutrans line, each in `coverage_exceptions`:
- Kněževes, železniční zastávka: only on 560's Hořovičky 18:00, whose way back skips Hokov and Heřmanov (560's own stops);
  380 m from Kněževes, u mlýna (560, 560 Kolešovice, 760). A roadside stop → the one owner check.
- Pustověty, Roztoky, nádraží [RA], Rakovník (the railway station): only the XS75 rail replacement bus.

Outside the Středočeský kraj (now this sheet's to serve, owner 2 Nov): every stop is on a line except
- Chbany, Poláky, točna: the turning loop 110 m from Chbany, Poláky (on 415), only on 415 Kadaň 14:47. A roadside stop → the one
  owner check.
- Chlum u Rakovníka: only XS75.

Served now because of the 2 Nov rule: Měcholupy, Želeč and Deštnice (415 back), Chbany, Malé Krhovice, Vadkovice, Vikletice,
Vikletice, přehrada and Soběsuky, rozcestí (415 out), Louny, sokolovna and Louny, Luna (711), Domoušice, Solopysky (711
Domoušice), Podbořany, nemocnice (760 back); and as before Slatina, Chříč (571), Kryry, Strojetice, křižovatka (560).

Another Středočeský okres: Stochov, Slovanka I (okres Kladno; 415's Nové Strašecí variant) is left to the Kladensko sheet and the
`--final` pass. Lines 580 and 625 (Kladensko) also serve okres Rakovník.

## Owner check (in `lines.json`)

1. **Roadside stops** Kněževes, železniční zastávka (380 m from Kněževes, u mlýna) and Chbany, Poláky, točna (110 m from Chbany,
   Poláky) are coverage exceptions; serving both costs +2 buses (a line every 480 on each one's real trip, with an untimed
   return).

The twelve other checks of 1 Nov were removed: the review showed each asked what the method or the owner already decides
(outstation rate 304 / 404 / 576, exact hourly 305, only-service lines 571 / 572 Slabce / 573 Šípy / 574 / 584 Vinařice, the
1 Nov variant-path rule 575, Step 5b with chain evidence 581, the standard pooling option 562, 0-minute turns 573 / 584). The
every-480 lines (571, 572 Slabce, 573 Šípy, 574, 584 Vinařice, 711 Domoušice) are named in `notes` as information.

## Open questions

- For the 2 Nov live map (afternoon): where the 304 Rakovník – Zličín trips (13:20, 14:00, 15:30) go on; the 304 ↔ 404 (4 of
  12 304 departures at Zličín follow a 404 arrival) and 304 → 306 (3 of 8 arrivals) chains at Praha, Zličín; whether 561
  Šamotka 14:10 → Kolešovice 15:26 goes on as 560 Kolešovice 15:30 (one circuit would save a bus); 562 → 561 at Rakovník,
  střelnice and 562 → 560 at the autobusové stanoviště. All are in `notes`.
- Engine: does "Leave up to" let a bus leave on arrival when the loop rule typed the departure 1 min early (the 0-minute turns)?
- The save has one-convoy lines 100304 … 100760 (and 100580, 100625 for Kladensko) without timetables; the publish step gives the
  in-game change list. New Simutrans lines against them: 560 Kolešovice, 562 Lubná, 572 Slabce, 573 Šípy, 581 Nové Strašecí,
  581 Senomaty, 584 Vinařice, 711 Domoušice; 570 (100570) is not modelled.

## Suggestions for the brief and the scripts (for the next 11 oblasti)

Already taken into the brief's "Learned on the pilot" (2 Nov): full stop names; each line's own stops in the reading; `core_to`
vs `knot`; checking `rt` / `knot_rt`; slots standing for real trips ("no slot in the window"); 0-minute turns with `lay` 0;
serve every place; outstation lines with a Prague end; same-minute departures at a hub; no abbreviations; through-running in
notes; short card text; owner checks only for real choices. Still open:
1. **`run_oblast.py` does not parse** (as of 05:22 on 2 Nov): line 40 has `print(f"` and a line break inside the f-string
   (it should be `"\ncoverage: …`). Every designer run fails until it is fixed.
2. **`stops_via` mixes running times**: on a knot leg it mixes knot-read and terminal-read trips in the median (575: 74 vs 69),
   and on any leg the median can take trips of another variant that passes the same stop (415: the 6:45 via Nové Strašecí, 133
   vs 118). Use the trips of the path shown, near the window.
3. **`knot` running time is a whole-day median** (711: 10 for a 15-min afternoon run); compute it near the window as `rt` is.
4. **`stops_via` picks the path but the leg's typed minute stays the slot trip's**: where the shown path is longer or shorter
   than the slot trip's (575, 415, 760), the card has to say both times; the builder could print both.
5. **The Step 4 audit's FIXABLE** search ignores the other direction (404).
6. **`03b_draft.py`** reports "fill 1.0" next to designs that fail Step 4 (304); mark failing draft rows.
7. **415's reading path 1** lists "Krupá, Šustna" twice; check the GTFS stop merge.
8. **Out-of-kraj variant stops**: with "serve every place", long lines into other kraje (305, 404, 415, 711, 760) pick up stops
   on minor variants there (Chbany, Deštnice, Podbořany, nemocnice, Louny, Luna). The reading's "stops only this line serves"
   line should include them, marked by kraj, so they are seen on the first pass, not after the review.
9. `00_config.py` loads a shared `lines.json` and never uses it.
