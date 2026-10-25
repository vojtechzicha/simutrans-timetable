# Bus schedule method, applied to the Novojičínsko/Bílovecko sheet (25 Oct 2026)

The owner asked for every sheet to be checked as the Hlučínsko lines were (`../odis-regional-opavsko/method-check-2026-10-25.md`): "verify all sheets with this level of detail", and earlier "that's the point of you doing it, so you'll not produce incorrect results". The regional audit of 25 Oct (`../audit/audit-regional-2026-10-25.md`) found 80 of this sheet's 139 timed legs failing Step 4 (published v5: 59 ok). Every Simutrans line with a failing leg was read again by hand, both directions together, against `../bus-schedule-method.md` (v4). After the check 135 of 139 timed legs pass; the four left are judged by hand below.

- **Data:** the sheet's JDF trips for Tue 20 Oct 2026 (`data/derived/trips.json`), the whole-day reading (`data/derived/reading/<L>.txt`) and the ODIS live-map plate chains (13:00–19:30).
- **Step 4 test**, per direction, in the line's model hours (anchor −30 to +90 min): the window slots must equal the real departures ±1, and at least 80 % of the slots need a real departure within 3 min.
- **Typed values** are (real − 61) mod every: every terminus is a loop. The real times below are worked out from each typed value, (value + 61) mod every.
- **Bus counts** are the builder's (`05_schedule.py`, `slot_need`), checked again with 3-min turns at the terminals (Step 10), shorter only where the real bus turns faster (667 at Heřmanice).

## How each row was chosen

Candidates were searched per line with the same interval and the same number of slots both ways (Step 7), every interval dividing 1440 up to 480, slots on or within 3 min of the window's real departures. Then, in order:

1. **Step 4 both ways.** On an outstation line (v4) the busier direction is timed at the other's rate and its extra departures, buses going home or on to another line, are off the pattern (615 out of Nový Jičín; 635 and 641 the other way round, into Kopřivnice).
2. **Every direction with real departures in the model hours keeps a slot there.** A direction with none there (the trips start later or turn short) gets its slot outside the model hours, on a real trip: 379, 619, 625 Tísek, 638, 679. These were IRREGULAR in the audit and now pass.
3. **At about the real rate:** an interval per slot more than about twice the line's afternoon headway is not used while a closer one passes (370: every 240 with one bus passes, but Řepiště would get a bus every 4 h).
4. **Most departures on the minute over the whole day, then within 1 min** (Step 4 rule 3). A row that needs more buses wins only with at least two more exact departures per extra bus; which departures fall off is decided by the plates, keeping the buses that stay on the line (v4).
5. **Plain intervals** (divisors of 60, 90, 120, 180, 240) unless an odd one is clearly better (two more exact departures, or a bus fewer).
6. **A slot moved by at most 3 min to save a bus** (still within Step 4): 286, 371, 374, 622, 655, 656, 665, 690, 696. The builder's older shortest-round moves of up to 6 min broke Step 4 and are gone.

No empty-return line was added. 287 no longer counts the 16:47 to Pustá Polom (`notvia` Nový Dvůr: it is 287 Pustá Polom's trip), and 620 no longer counts the Pohoř trips (`notvia` Pohoř: they are 620 Pohoř's), so neither is modelled twice.

## Summary

| Line | Published (v5) | Step 4 (v5) | Now | Buses |
|---|---|---|---|---|
| 286 | every 60, Hlubočec 14:34, 15:34 / Svinov nádraží 14:43, 15:43 | Hlubočec→Svinov nádraží EMPTY; Svinov nádraží→Hlubočec EMPTY | every 120, Hlubočec 14:43, 15:50 / Svinov nádraží 14:59, 15:49 | 2 → 2 |
| 287 | every 60, Kyjovice 16:22, 17:22 / Svinov nádraží 15:41, 16:41 | Kyjovice→Svinov nádraží EMPTY; Svinov nádraží→Kyjovice EMPTY | every 120, Kyjovice 16:42 / Svinov nádraží 15:37 | 2 → 1 |
| 628 | every 180, Bílovec 12:35, 15:35, 18:35 (outside the model hours) / Dubina 13:49 | Dubina→Bílovec EMPTY | every 120, Bílovec 13:43 / Dubina 14:44 | 1 → 1 |
| 671 | every 90, Svinov mosty 15:50, 17:20 / Skřipov 15:35, 17:05 | Svinov mosty→Skřipov EMPTY; Skřipov→Svinov mosty EMPTY | every 80, Svinov mosty 16:10 / Skřipov 16:15 | 2 → 2 |
| 672 | every 90, Slatina 14:37, 16:07 / Svinov mosty 15:20 | Slatina→Svinov mosty EMPTY; Svinov mosty→Slatina EMPTY | every 144, Slatina 16:04 / Svinov mosty 14:30 | 1 → 1 |
| 679 | every 120, Zbyslavice 14:04 / Svinov nádraží 14:45 | Svinov nádraží→Zbyslavice EMPTY | every 180, Zbyslavice 15:45 / Svinov nádraží 13:40, 16:40, 19:40 (outside the model hours) | 1 → 1 |
| 692 | every 60, Bílovec 15:49, 16:49 | Bílovec→Bílovec EMPTY | every 180, Bílovec 15:44, 17:19 | 1 → 1 |
| 693 | every 90, Bílovec 13:44, 15:14 | Bílovec→Bílovec EMPTY | every 120, Bílovec 13:44, 14:49 | 1 → 1 |
| 613 | every 60, Fulnek 16:08, 17:08 / Studénka 16:11, 17:11 | Fulnek→Studénka EMPTY; Studénka→Fulnek EMPTY | every 96, Fulnek 15:58 / Studénka 16:11 | 2 → 2 |
| 614 | every 120, Odry 14:45 / Nový Jičín 13:30 | Odry→Nový Jičín EMPTY | every 120, Odry 14:50 / Nový Jičín 13:30 | 2 → 2 |
| 615 | every 60, Nový Jičín 14:35, 15:35 / Luboměř 14:05, 15:05 | Nový Jičín→Luboměř EMPTY; Luboměř→Nový Jičín EMPTY | every 80, Nový Jičín 14:05, 15:25 / Luboměř 13:58, 15:18 | 3 → 2 |
| 618 | every 60, Fulnek 14:10, 15:10 / Nový Jičín 14:29, 15:29 | Fulnek→Nový Jičín EMPTY; Nový Jičín→Fulnek EMPTY | every 120, Fulnek 14:10, 14:45, 15:25 / Nový Jičín 14:00, 14:35, 15:12 | 2 → 3 |
| 620 | every 60, Nový Jičín 13:50, 14:50 / Odry 13:58, 14:58 | Nový Jičín→Odry EMPTY; Odry→Nový Jičín FEWER | every 120, Nový Jičín 13:40, 15:10 / Odry 13:58, 14:33 | 2 → 2 |
| 620 Pohoř | every 120, Nový Jičín 15:15 / Pohoř 14:08 | Pohoř→Nový Jičín EMPTY | every 180, Nový Jičín 15:15 / Pohoř 13:20 | 1 → 1 |
| 621 | every 90, Nový Jičín 14:12, 15:42 / Frýdek-Místek 14:06, 15:36 | Nový Jičín→Frýdek-Místek EMPTY; Frýdek-Místek→Nový Jičín EMPTY | every 160, Nový Jičín 15:17, 15:47 / Frýdek-Místek 14:06, 14:36 | 2 → 2 |
| 621 Ostrava | every 120, Nový Jičín 14:37 / Mor.Ostrava Náměstí Republiky 15:15 | Nový Jičín→Mor.Ostrava Náměstí Republiky EMPTY | every 120, Nový Jičín 14:42 / Mor.Ostrava Náměstí Republiky 15:18 | 2 → 2 |
| 622 | every 90, Nový Jičín 15:47 / Mořkov 14:40, 16:10 | Nový Jičín→Mořkov EMPTY; Mořkov→Nový Jičín EMPTY | every 120, Nový Jičín 14:32, 15:20 / Mořkov 14:55, 16:07 | 1 → 1 |
| 625 | every 180, Nový Jičín 16:32 / Bílovec 17:16 | Nový Jičín→Bílovec EMPTY | every 120, Nový Jičín 16:37 / Bílovec 17:16 | 1 → 2 |
| 625 Tísek | every 180, Nový Jičín 12:27, 15:27, 18:27 (outside the model hours) / Tísek 16:22 | Tísek→Nový Jičín EMPTY | every 240, Nový Jičín 15:32 / Tísek 14:24, 18:24 (outside the model hours) | 1 → 1 |
| 619 | every 180, Fulnek 16:25 / Jeseník n.Odrou 15:38 | Fulnek→Jeseník n.Odrou EMPTY; Jeseník n.Odrou→Fulnek EMPTY | every 180, Fulnek 14:48, 17:48 (outside the model hours) / Jeseník n.Odrou 15:45 | 1 → 1 |
| 927 | every 180, Nový Jičín 16:01 / Hranice 16:55 | Hranice→Nový Jičín EMPTY | every 180, Nový Jičín 16:01 / Hranice 17:00 | 1 → 1 |
| 665 | every 90, Nový Jičín 15:45, 17:15 / Mořkov 16:40 | Nový Jičín→Mořkov EMPTY; Mořkov→Nový Jičín EMPTY | every 120, Nový Jičín 16:17 / Mořkov 15:52 | 1 → 1 |
| 667 | every 60, Nový Jičín 15:40, 16:40 / Starý Jičín 16:29, 17:29 | Nový Jičín→Starý Jičín EMPTY; Starý Jičín→Nový Jičín EMPTY | every 120, Nový Jičín 15:35 / Starý Jičín 16:06 | 2 → 1 |
| 677 | every 90, Nový Jičín 16:36 / Svinov nádraží 16:35 | Nový Jičín→Svinov nádraží EMPTY | every 120, Nový Jičín 16:06 / Svinov nádraží 15:35 | 2 → 2 |
| 689 | every 60, Nový Jičín 15:45, 16:45 / Bernartice n.Odrou 16:10, 17:10 | Nový Jičín→Bernartice n.Odrou EMPTY; Bernartice n.Odrou→Nový Jičín EMPTY | every 120, Nový Jičín 15:45 / Bernartice n.Odrou 16:10 | 1 → 1 |
| 696 | every 30, Nový Jičín 14:30, 15:00, 15:30, 16:00 / Frenštát u škol 14:20, 14:50, 15:20, 15:50 | Nový Jičín→Frenštát u škol EMPTY; Frenštát u škol→Nový Jičín EMPTY | every 120, Nový Jičín 14:38, 15:10, 15:30, 16:03 / Frenštát u škol 14:20, 14:45, 15:20, 15:57 | 3 → 3 |
| 697 | every 120, Nový Jičín 14:25 / Kopřivnice 14:21 | Nový Jičín→Kopřivnice EMPTY | every 96, Nový Jičín 15:13 / Kopřivnice 14:38 | 2 → 2 |
| 987 | every 60, Nový Jičín 13:55, 14:55 / Valašské Meziříčí 13:30, 14:30 | Nový Jičín→Valašské Meziříčí EMPTY; Valašské Meziříčí→Nový Jičín EMPTY | every 180, Nový Jičín 13:55, 15:20 / Valašské Meziříčí 13:30, 15:05 | 2 → 2 |
| 988 | every 60, Nový Jičín 15:40, 16:40 / Valašské Meziříčí 15:30, 16:30 | Nový Jičín→Valašské Meziříčí EMPTY; Valašské Meziříčí→Nový Jičín EMPTY | every 120, Nový Jičín 16:40 / Valašské Meziříčí 16:15 | 2 → 2 |
| 379 | every 180, Petřvald 15:38 / Zábřeh Kotva 16:42 | Zábřeh Kotva→Petřvald EMPTY | every 180, Petřvald 15:38 / Zábřeh Kotva 14:57, 17:57 (outside the model hours) | 1 → 1 |
| 670 | every 60, Nový Jičín 16:05, 17:05 / Dubina 15:50, 16:50 | Nový Jičín→Dubina EMPTY; Dubina→Nový Jičín EMPTY | every 120, Nový Jičín 15:55, 17:05 / Dubina 16:20, 17:20 | 3 → 3 |
| 370 | every 60, Dubina 15:43, 16:43 / Řepiště 16:08, 17:08 | Dubina→Řepiště EMPTY; Řepiště→Dubina EMPTY | every 90, Dubina 16:19 / Řepiště 16:02 | 1 → 2 |
| 371 | every 60, Dubina 15:55, 16:55 / Kozlovice 16:09, 17:09 | Dubina→Kozlovice EMPTY; Kozlovice→Dubina EMPTY | every 120, Dubina 16:58 / Kozlovice 16:12 | 2 → 1 |
| 373 | every 60, Dubina 14:20, 15:20 / Kopřivnice 14:44, 15:44 | Kopřivnice→Dubina EMPTY | every 120, Dubina 14:20, 15:20 / Kopřivnice 14:38, 15:43 | 3 → 3 |
| 374 | every 60, Svinov mosty 14:25, 15:25 / Trnávka 14:35, 15:35 | Svinov mosty→Trnávka EMPTY | every 120, Svinov mosty 14:21, 15:25 / Trnávka 14:35, 15:32 | 2 → 2 |
| 376 | every 60, Dubina 16:05, 17:05 / Hukvaldy 16:03, 17:03 | Dubina→Hukvaldy EMPTY | every 120, Dubina 16:10, 17:05 / Hukvaldy 16:03, 17:03 | 2 → 2 |
| 634 | every 60, Kopřivnice 14:38, 15:38 / Frenštát u škol 14:28, 15:28 | Kopřivnice→Frenštát u škol EMPTY; Frenštát u škol→Kopřivnice EMPTY | every 90, Kopřivnice 15:38 / Frenštát u škol 14:28, 15:58 | 2 → 2 |
| 635 | every 60, Kopřivnice 14:18, 15:18 / Frenštát u škol 14:25, 15:25 | Kopřivnice→Frenštát u škol EMPTY; Frenštát u škol→Kopřivnice EMPTY | every 120, Kopřivnice 14:18, 15:28 / Frenštát u škol 14:25, 15:55 | 2 → 2 |
| 638 | every 90, Kopřivnice 16:37 / Hukvaldy 15:36, 17:06 | Kopřivnice→Hukvaldy EMPTY; Hukvaldy→Kopřivnice EMPTY | every 180, Kopřivnice 12:14, 15:14, 18:14 (outside the model hours) / Hukvaldy 15:51 | 1 → 1 |
| 641 | every 60, Kopřivnice 14:25, 15:25 / Dubina 15:00, 16:00 | Dubina→Kopřivnice FEWER | every 60, Kopřivnice 14:25, 15:25 / Dubina 15:00, 16:00 | 3 → 3 |
| 644 | every 120, Kopřivnice 16:40 / Štramberk 17:12 | Kopřivnice→Štramberk EMPTY; Štramberk→Kopřivnice EMPTY | every 180, Kopřivnice 15:45 / Štramberk 16:12 | 1 → 1 |
| 646 | every 60, Nový Jičín 14:30, 15:30 / Kopřivnice 14:10, 15:10 | Nový Jičín→Kopřivnice FEWER; Kopřivnice→Nový Jičín EMPTY | every 90, Nový Jičín 14:00, 14:30, 15:30 / Kopřivnice 14:10, 14:40 | 2 → 3 |
| 653 | every 60, Kopřivnice 16:10, 17:10 / Frenštát u škol 15:55, 16:55 | Kopřivnice→Frenštát station EMPTY | every 120, Kopřivnice 17:15 / Frenštát u škol 15:55 | 2 → 2 |
| 655 | every 30, Frenštát u škol 15:48, 16:18, 16:48, 17:18 / Trojanovice 15:35, 16:05, 16:35, 17:05 | Frenštát u škol→Trojanovice EMPTY; Trojanovice→Frenštát u škol EMPTY | every 120, Frenštát u škol 16:05, 16:55, 17:18 / Trojanovice 15:40, 16:20, 17:10 | 1 → 2 |
| 656 | every 60, Frenštát u škol 13:50, 14:50 / Trojanovice 14:05, 15:05 | Frenštát u škol→Trojanovice EMPTY; Trojanovice→Frenštát u škol EMPTY | every 180, Frenštát u škol 13:15, 13:55, 14:49 / Trojanovice 13:33, 14:11, 15:05 | 1 → 1 |
| 657 Kunčice | every 180, Frenštát u škol 13:45 / Kunčice p.Ondřejníkem 12:06, 15:06, 18:06 (outside the model hours) | Frenštát u škol→Kunčice p.Ondřejníkem EMPTY | every 120, Frenštát u škol 14:00 / Kunčice p.Ondřejníkem 13:06 | 1 → 1 |
| 690 | every 60, Nový Jičín 15:40, 16:40 / Tymphany 15:30, 16:30 | Nový Jičín→Tymphany EMPTY; Tymphany→Nový Jičín EMPTY | every 96, Nový Jičín 15:54 / Tymphany 16:40 | 2 → 1 |
| 698 | every 60, Nový Jičín 13:10, 13:30, 14:10, 14:30 / Kopřivnice 13:15, 13:35, 14:15, 14:35 | Nový Jičín→Kopřivnice EMPTY | every 120, Nový Jičín 13:10, 13:30, 14:20, 14:45 / Kopřivnice 13:15, 13:35, 14:15, 14:35 | 4 → 4 |
| 699 | every 60, Nový Jičín 16:25, 17:25 / Kopřivnice 16:25, 17:25 | Nový Jičín→Kopřivnice EMPTY; Kopřivnice→Nový Jičín EMPTY | every 120, Nový Jičín 16:25 / Kopřivnice 16:55 | 2 → 2 |
| 601–604 | every 60, Nový Jičín 16:10, 17:10 / Nový Jičín 15:50, 16:50 / Nový Jičín 16:10, 17:10 / Nový Jičín 16:10, 17:10 / Šenov u N.Jičína 15:46, 16:46 | Nový Jičín→Nový Jičín EMPTY; Nový Jičín→Šenov u N.Jičína EMPTY | every 60, Nový Jičín 16:10, 17:10 / Nový Jičín 15:50, 16:50 / Nový Jičín 16:10, 17:10 / Nový Jičín 16:10, 17:10 / Šenov u N.Jičína 15:46, 16:46 | 3 → 3 |
| **Total (sheet)** | | | | **108 → 108** |

Window times are shown; legs whose slots fall outside the model hours show their afternoon times. The full typed values are in each section.

## 286 Opava-Hradec nad Moravicí-Hlubočec-Hrabyně-Ostrava-Vratimov

- **(a) Core points:** Hlubočec, točna · Ostrava, Svinov, nádraží · Hradec n.Moravicí, železniční stanice. Model hours 14:10–16:10.
- **(b) Afternoon (12–20 h, model hours in bold, read at the terminal):** Hlubočec → Svinov nádraží 13:33, **14:43**, **15:48**, 17:58; Svinov nádraží → Hlubočec 12:44, 13:49, **14:59**, **15:49**, 17:05.
- **(c) Step 4.** Published every 60: Hlubočec slots 14:34(-) 15:34(-) for real 14:43 15:48: EMPTY; Svinov nádraží slots 14:43(-) 15:43(-) for real 14:59 15:49: EMPTY. every 60 (published :34 / :43): 2 slots / 2 real, 0 of 2 within 3, FAIL both ways (Svinov 14:59 and 15:49 are 50 min apart, no hourly minute hits both). Every 90, one slot: passes (1 / 2), 5 exact over the day. Every 120, two slots each way: passes (2 / 2, all four exact), 5 exact. Every 180, two slots: passes, 5 exact.
- **(d) Simutrans line 286:** Hlubočec, točna → Svinov nádraží: every 120, Offset 49 (real 13:50 · 15:50 · 17:50 · 19:50), Also at 102 (real 12:43 · 14:43 · 16:43 · 18:43); Ostrava, Svinov, nádraží → Hlubočec: every 120, Offset 48 (real 13:49 · 15:49 · 17:49 · 19:49), Also at 118 (real 12:59 · 14:59 · 16:59 · 18:59).
  Step 4 now: Hlubočec 14:43 15:50 for 14:43 15:48: ok; Svinov nádraží 14:59 15:49 for 14:59 15:49: ok. Exact and ±1 counts tie; 120 keeps every trip of the two buses that stay on the line all afternoon (64-1010 13:49 → 14:43 → 15:49, 64-1004 14:59 → 15:48), every 90 drops 15:48 and 15:49. 15:48 is typed as 15:50: with the model's 48-min running time the bus from 14:59 would turn in 1 min (the real one turns in 5); 3 min keeps it at two buses.
- **(e) Knots** (model passing time, min from the nearest real time of trips that run the whole leg): Hlubočec → Ostrava, Svinov, nádraží 15:32 (2), 16:39 (4); Svinov nádraží → Hlubočec, točna 15:45 (2), 16:35 (2).
- **(f) Off the pattern 12–20 h** (min off): Hlubočec 13:33 (17), 17:58 (8); Svinov nádraží 12:44 (15), 17:05 (6).
- **(g) Need:** 2 → 2 (waits Hlubočec 6, 3; Svinov nádraží 22, 19).

## 287 Pustá Polom-Kyjovice-Horní Lhota-Velká Polom-Ostrava

- **(a) Core points:** Kyjovice, has.zbroj. · Ostrava, Svinov, nádraží. Model hours 15:30–17:30.
- **(b) Afternoon (12–20 h, model hours in bold, read at the terminal):** Kyjovice → Svinov nádraží 12:17, 13:17, 14:12, 15:22, **16:42**; Svinov nádraží → Kyjovice 13:30, 14:35, 14:52, **15:37**, 18:47.
- **(c) Step 4.** Published every 60: Kyjovice slots 16:22(-) 17:22(-) for real 16:42: EMPTY; Svinov nádraží slots 15:41(-) 16:41(-) for real 15:37 16:47: EMPTY. every 60 (published :22 / :41): Kyjovice 16:22, 17:22 for one real 16:42, 0 of 2 FAIL; Svinov 15:41 (15:37 within 4) and 16:41, FAIL. The window 15:30–17:30 has one departure each way (Svinov 16:47 is 287 Pustá Polom's trip, now left to it with `notvia` Nový Dvůr, so it is not counted twice). Every 60 / 80 / 90 / 96 put a second, empty slot in the window: FAIL. Every 120 one slot: passes both ways, exact.
- **(d) Simutrans line 287:** Kyjovice, has.zbroj. → Svinov nádraží: every 120, Offset 101 (real 12:42 · 14:42 · 16:42 · 18:42); Ostrava, Svinov, nádraží → Kyjovice: every 120, Offset 36 (real 13:37 · 15:37 · 17:37 · 19:37).
  Step 4 now: Kyjovice 16:42 for 16:42: ok; Svinov nádraží 15:37 for 15:37: ok. 64-0002 runs exactly this round (15:37 out, 16:42 back). Need 2 → 1.
- **(e) Knots** (model passing time, min from the nearest real time of trips that run the whole leg): Kyjovice → Ostrava, Svinov, nádraží 17:21 (0); Svinov nádraží → Kyjovice, has.zbroj. 16:15 (0).
- **(f) Off the pattern 12–20 h** (min off): Kyjovice 12:17 (25), 13:17 (35), 14:12 (30), 15:22 (40); Svinov nádraží 13:30 (7), 14:35 (58), 14:52 (45), 18:47 (50).
- **(g) Need:** 2 → 1 (waits Kyjovice 27; Svinov nádraží 16).

## 628 Ostrava-Stará Ves nad Ondřejnicí-Jistebník-Bílovec

- **(a) Core points:** Bílovec, železniční stanice · Jistebník, železniční stanice · Ostrava, Dubina. Model hours 13:20–15:20.
- **(b) Afternoon (12–20 h, model hours in bold, read at the terminal):** Bílovec → Dubina **13:43**, 15:45, 18:35; Dubina → Bílovec **14:44**, 16:49, 19:49.
- **(c) Step 4.** Published every 180: Bílovec slots none for real 13:43: ok; Dubina slots 13:49(-) for real 14:44: EMPTY. published every 180 (Bílovec 12:35 / 15:35, Dubina 13:49): Dubina slot 13:49 empty (real 14:44), FAIL; Bílovec had no window slot for 13:43. Every 120, 144, 160, 180 with one slot each way all pass, exact in the window.
- **(d) Simutrans line 628:** Bílovec, železniční stanice → Dubina: every 120, Offset 42 (real 13:43 · 15:43 · 17:43 · 19:43); Ostrava, Dubina → Bílovec: every 120, Offset 103 (real 12:44 · 14:44 · 16:44 · 18:44).
  Step 4 now: Bílovec 13:43 for 13:43: ok; Dubina 14:44 for 14:44: ok. Every 120 also puts 15:43 and 16:44 within 2 and 5 min of the real 15:45 and 16:49 (the second round); the others do not. 64-1014's round 13:43 → 14:44.
- **(e) Knots** (model passing time, min from the nearest real time of trips that run the whole leg): Bílovec → Jistebník, železniční stanice 14:06 (7); Bílovec → Ostrava, Dubina 14:28 (7); Dubina → Bílovec, železniční stanice 15:29 (2); Dubina → Jistebník, železniční stanice 15:10 (0).
- **(f) Off the pattern 12–20 h** (min off): Bílovec 18:35 (52); Dubina 16:49 (5), 19:49 (55).
- **(g) Need:** 1 → 1 (waits Bílovec 12; Dubina 13).

## 671 Skřipov-Těškovice-Bítov-Klimkovice-Ostrava

- **(a) Core points:** Ostrava, Svinov, mosty · Bílovec, Výškovice, restaurace · Skřipov, U Kostela. Model hours 15:30–17:30.
- **(b) Afternoon (12–20 h, model hours in bold, read at the terminal):** Svinov mosty → Skřipov 13:30, 14:45, **16:10**, 18:50; Skřipov → Svinov mosty 13:05, 14:05, 15:15, **16:15**, 18:55.
- **(c) Step 4.** Published every 90: Svinov mosty slots 15:50(-) 17:20(-) for real 16:10: EMPTY; Skřipov slots 15:35(-) 17:05(-) for real 16:15: EMPTY. published every 90 (Svinov 15:50 / 17:20, Skřipov 15:35 / 17:05): 0 of 2 within 3 each way, FAIL. Every 80, one slot: passes both (1 / 1), Svinov exact 4 times over the day (5:30, 13:30, 16:10, 18:50). Every 120 / 160 one slot pass with 3 exact.
- **(d) Simutrans line 671:** Ostrava, Svinov, mosty → Skřipov: every 80, Offset 29 (real 12:10 · 13:30 · 14:50 · 16:10 · 17:30 · 18:50); Skřipov, U Kostela → Svinov mosty: every 80, Offset 34 (real 12:15 · 13:35 · 14:55 · 16:15 · 17:35 · 18:55); passes Bílovec, Výškovice, restaurace at 12:24 · 13:44 · 15:04 · 16:24 · 17:44 · 19:04.
  Step 4 now: Svinov mosty 16:10 for 16:10: ok; Skřipov 16:15 for 16:15: ok. Most exact. Výškovice is the knot: the return is timed at Skřipov so the bus passes Výškovice at 16:24, as the 16:15 from Skřipov does.
- **(e) Knots** (model passing time, min from the nearest real time of trips that run the whole leg): Svinov mosty → Bílovec, Výškovice, restaurace 16:48 (0); Svinov mosty → Skřipov, U Kostela 16:57 (1); Skřipov → Ostrava, Svinov, mosty 17:04 (2).
- **(f) Off the pattern 12–20 h** (min off): Svinov mosty 14:45 (5); Skřipov 13:05 (30), 14:05 (30), 15:15 (20).
- **(g) Need:** 2 → 2 (waits Svinov mosty 27; Skřipov 37).

## 672 Bílovec-Slatina-Tísek-Klimkovice-Ostrava

- **(a) Core points:** Slatina · Ostrava, Svinov, mosty. Model hours 14:30–16:30.
- **(b) Afternoon (12–20 h, model hours in bold, read at the terminal):** Slatina → Svinov mosty 12:19, **14:44**, **16:04**, 17:46; Svinov mosty → Slatina 13:50, **14:30**, **14:50**, 17:00, 19:30.
- **(c) Step 4.** Published every 90: Slatina slots 14:37(-) 16:07 for real 14:44 16:04: EMPTY; Svinov mosty slots 15:20(-) for real 14:30 14:50: EMPTY. published every 90 (Slatina 14:37 / 16:07, Svinov 15:20): Slatina 14:37 7 off (real 14:44), Svinov 15:20 empty (real 14:30, 14:50), FAIL. Every 160 / 120 with two slots each way pass (all four exact) but need 3 buses; every 144 / 160 with one slot each way pass with one bus.
- **(d) Simutrans line 672:** Slatina → Svinov mosty: every 144, Offset 39 (real 13:40 · 16:04 · 18:28); Ostrava, Svinov, mosty → Slatina: every 144, Offset 89 (real 12:06 · 14:30 · 16:54 · 19:18).
  Step 4 now: Slatina 16:04 for 14:44 16:04: ok; Svinov mosty 14:30 for 14:30 14:50: ok. One bus (64-1009) works the line all afternoon, Svinov 14:30 → Slatina 16:04 → Svinov 17:00. The extra window departures are other lines' buses: Slatina 14:44 is 64-1015 (on to 673), Svinov 14:50 is 64-1002 (to Bílovec). Of the one-bus rows, every 144 puts the next Svinov slot at 16:54, closest to the real 17:00 (160: 17:10).
- **(e) Knots** (model passing time, min from the nearest real time of trips that run the whole leg): Slatina → Ostrava, Svinov, mosty 16:44 (0); Svinov mosty → Slatina 15:11 (0).
- **(f) Off the pattern 12–20 h** (min off): Slatina 12:19 (63), 14:44 (64), 17:46 (42); Svinov mosty 13:50 (40), 14:50 (20), 17:00 (6), 19:30 (12).
- **(g) Need:** 1 → 1 (waits Slatina 53; Svinov mosty 10).

## 679 Zbyslavice-Klimkovice-Vřesina-Ostrava

- **(a) Core points:** Zbyslavice, střed · Klimkovice, centrum · Ostrava, Svinov, nádraží. Model hours 13:50–15:50.
- **(b) Afternoon (12–20 h, model hours in bold, read at the terminal):** Zbyslavice → Svinov nádraží **14:05**, **15:45**, 16:45, 18:05, 19:35; Svinov nádraží → Zbyslavice 16:40, 17:20, 18:45.
- **(c) Step 4.** Published every 120: Zbyslavice slots 14:04 for real 14:05 15:45: ok; Svinov nádraží slots 14:45(-) for real none: EMPTY. published every 120 (Zbyslavice 14:04, Svinov 14:45): the Svinov slot 14:45 has no trip to Zbyslavice (the 13:05, 14:05, 14:45 from Svinov turn at Klimkovice), IRREGULAR in the audit (no Svinov → Zbyslavice trip in 13:50–15:50). Every 180: Zbyslavice 15:45 (1 slot / 2 real, exact), Svinov 16:40 (exact; its slots 13:40 and 16:40 fall outside the window, so 0 slots / 0 real): passes both.
- **(d) Simutrans line 679:** Zbyslavice, střed → Svinov nádraží: every 180, Offset 164 (real 12:45 · 15:45 · 18:45); Ostrava, Svinov, nádraží → Zbyslavice: every 180, Offset 39 (real 13:40 · 16:40 · 19:40).
  Step 4 now: Zbyslavice 15:45 for 14:05 15:45: ok; Svinov nádraží none for none: ok. The afternoon buses reach Zbyslavice on 288 and 674, not on 679 (Step 5b across lines at Zbyslavice). 64-2003 runs 15:45 → 16:40 exactly. A shorter interval puts a Svinov slot inside the window where there is no trip.
- **(e) Knots** (model passing time, min from the nearest real time of trips that run the whole leg): Zbyslavice → Klimkovice, centrum 15:59 (0); Zbyslavice → Ostrava, Svinov, nádraží 16:25 (0); Svinov nádraží → Zbyslavice, střed 2:24 (203*); Svinov nádraží → Klimkovice, centrum 2:12 (203*).
- **(f) Off the pattern 12–20 h** (min off): Zbyslavice 14:05 (80), 16:45 (60), 18:05 (40), 19:35 (50); Svinov nádraží 17:20 (40), 18:45 (55).
- **(g) Need:** 1 → 1 (waits Zbyslavice 81; Svinov nádraží 15).

## 692 Bílovec-Bítov-Těškovice-Slatina-Bílovec

- **(a) Core points:** Bílovec, železniční stanice. Model hours 15:30–17:30.
- **(b) Afternoon (12–20 h, model hours in bold, read at the terminal):** Bílovec → Bílovec 12:49, 14:14, 14:49, **15:44**, **17:19**, 19:37.
- **(c) Step 4.** Published every 60: Bílovec slots 15:49(-) 16:49(-) for real 15:44 17:19: EMPTY. published every 60 :49: 15:49 and 16:49, 0 of 2 within 3 (real 15:44, 17:19), FAIL. Every 96 :44: passes, 1 exact, 2 within 1. Every 120 / 180 two slots: pass, both exact.
- **(d) Simutrans line 692:** Bílovec, železniční stanice → Bílovec: every 180, Offset 78 (real 14:19 · 17:19), Also at 163 (real 12:44 · 15:44 · 18:44).
  Step 4 now: Bílovec 15:44 17:19 for 15:44 17:19: ok. Every 180 also lands 12:44 and 14:19 within 5 min of the real 12:49 and 14:14 and needs one bus (120 needs two).
- **(e) Knots** (model passing time, min from the nearest real time of trips that run the whole leg): Bílovec → Bílovec, železniční stanice 15:44 (0), 17:19 (0).
- **(f) Off the pattern 12–20 h** (min off): Bílovec 12:49 (5), 14:14 (5), 14:49 (30), 19:37 (42).
- **(g) Need:** 1 → 1 (waits Bílovec 36, 46).

## 693 Bílovec-Slatina-Těškovice-Bítov-Bílovec

- **(a) Core points:** Bílovec, železniční stanice. Model hours 13:40–15:40.
- **(b) Afternoon (12–20 h, model hours in bold, read at the terminal):** Bílovec → Bílovec 12:54, **13:44**, **14:49**, 17:14, 18:24.
- **(c) Step 4.** Published every 90: Bílovec slots 13:44 15:14(-) for real 13:44 14:49: EMPTY. published every 90 (13:44, 15:14): 15:14 empty (real 14:49), FAIL. Every 120 / 144 two slots: pass, both exact, equal counts.
- **(d) Simutrans line 693:** Bílovec, železniční stanice → Bílovec: every 120, Offset 43 (real 13:44 · 15:44 · 17:44 · 19:44), Also at 108 (real 12:49 · 14:49 · 16:49 · 18:49).
  Step 4 now: Bílovec 13:44 14:49 for 13:44 14:49: ok. Plain interval preferred.
- **(e) Knots** (model passing time, min from the nearest real time of trips that run the whole leg): Bílovec → Bílovec, železniční stanice 13:44 (0), 14:49 (0).
- **(f) Off the pattern 12–20 h** (min off): Bílovec 12:54 (5), 17:14 (25), 18:24 (25).
- **(g) Need:** 1 → 1 (waits Bílovec 18, 8).

## 613 Fulnek-Pustějov-Studénka

- **(a) Core points:** Fulnek, náměstí · Studénka, železniční stanice. Model hours 15:30–17:30.
- **(b) Afternoon (12–20 h, model hours in bold, read at the terminal):** Fulnek → Studénka 13:20, 14:38, **15:58**, **17:08**; Studénka → Fulnek 14:01, 15:11, **16:11**, 17:46.
- **(c) Step 4.** Published every 60: Fulnek slots 16:08(-) 17:08 for real 15:58 17:08: EMPTY; Studénka slots 16:11 17:11(-) for real 16:11: EMPTY. published every 60 (Fulnek :08, Studénka :11): Fulnek 16:08 empty (real 15:58), Studénka 17:11 empty, FAIL. Every 96 one slot: passes (Fulnek 1 / 2, Studénka 1 / 1), exact 2, within 1 4. Every 120 one slot: passes, exact 2, within 1 2, one bus. Every 72 and 80 fail (72: an empty Studénka slot at 17:23; 80: Fulnek 15:58 and 17:08 are 70 min apart).
- **(d) Simutrans line 613:** Fulnek, náměstí → Studénka: every 96, Offset 33 (real 12:46 · 14:22 · 15:58 · 17:34 · 19:10); Studénka, železniční stanice → Fulnek: every 96, Offset 46 (real 12:59 · 14:35 · 16:11 · 17:47 · 19:23).
  Step 4 now: Fulnek 15:58 for 15:58 17:08: ok; Studénka 16:11 for 16:11: ok. Within ±1 decides (96: 17:47 for the real 17:46, 5:00 for 4:59); two buses as published.
- **(e) Knots** (model passing time, min from the nearest real time of trips that run the whole leg): Fulnek → Studénka, železniční stanice 16:32 (4); Studénka → Fulnek, náměstí 16:45 (1).
- **(f) Off the pattern 12–20 h** (min off): Fulnek 13:20 (34), 14:38 (16), 17:08 (26); Studénka 14:01 (34), 15:11 (36).
- **(g) Need:** 2 → 2 (waits Fulnek 50; Studénka 72).

## 614 Odry-Fulnek-Nový Jičín

- **(a) Core points:** Odry, autobusová stanice · Nový Jičín, autobusové nádraží. Model hours 13:10–15:10.
- **(b) Afternoon (12–20 h, model hours in bold, read at the terminal):** Odry → Nový Jičín 12:35, **13:45**, **14:50**, 18:45; Nový Jičín → Odry 12:00, **13:30**, 15:30, 17:10.
- **(c) Step 4.** Published every 120: Odry slots 14:45(-) for real 13:45 14:50: EMPTY; Nový Jičín slots 13:30 for real 13:30: ok. published every 120 (Odry 14:45, NJ 13:30): Odry 14:45 5 off the real 14:50, FAIL. Every 120 with Odry 14:50: passes both, exact.
- **(d) Simutrans line 614:** Odry, autobusová stanice → Nový Jičín: every 120, Offset 109 (real 12:50 · 14:50 · 16:50 · 18:50); Nový Jičín, autobusové nádraží → Odry: every 120, Offset 29 (real 13:30 · 15:30 · 17:30 · 19:30).
  Step 4 now: Odry 14:50 for 13:45 14:50: ok; Nový Jičín 13:30 for 13:30: ok. One minute changed.
- **(e) Knots** (model passing time, min from the nearest real time of trips that run the whole leg): Odry → Nový Jičín, autobusové nádraží 15:50 (0); Nový Jičín → Odry, autobusová stanice 14:27 (1).
- **(f) Off the pattern 12–20 h** (min off): Odry 12:35 (15), 13:45 (55), 18:45 (5); Nový Jičín 12:00 (30), 17:10 (20).
- **(g) Need:** 2 → 2 (waits Odry 22; Nový Jičín 100).

## 615 Luboměř, Heltinov-Spálov-Odry-Jeseník nad Odrou-Nový Jičín

- **(a) Core points:** Luboměř, Heltinov · Odry, autobusová stanice · Nový Jičín, autobusové nádraží. Model hours 13:40–15:40.
- **(b) Afternoon (12–20 h, model hours in bold, read at the terminal):** Nový Jičín → Luboměř **14:05**, **14:35**, **15:25**, 16:05, 17:35, 18:35; Luboměř → Nový Jičín 13:05, **13:58**, **15:16**, 17:06.
- **(c) Step 4.** Published every 60: Nový Jičín slots 14:35 15:35(-) for real 14:05 14:35 15:25: EMPTY; Luboměř slots 14:05(-) 15:05(-) for real 13:58 15:16: EMPTY. published every 60 (NJ :35, Heltinov :05): NJ 15:35 empty (that trip turns at Odry), Heltinov 14:05 / 15:05 empty (real 13:58, 15:16), FAIL. Every 120 two slots each way (NJ 14:05, 14:35; Heltinov 13:58, 15:16): passes, 7 exact, four buses. Every 80 one slot: passes both ways (NJ 14:05, 15:25 exact; Heltinov 13:58, 15:18), two buses.
- **(d) Simutrans line 615:** Nový Jičín, autobusové nádraží → Luboměř: every 80, Offset 64 (real 12:45 · 14:05 · 15:25 · 16:45 · 18:05 · 19:25); Luboměř, Heltinov → Nový Jičín: every 80, Offset 57 (real 12:38 · 13:58 · 15:18 · 16:38 · 17:58 · 19:18).
  Step 4 now: Nový Jičín 14:05 15:25 for 14:05 14:35 15:25: ok; Luboměř 13:58 15:18 for 13:58 15:16: ok. Outstation line (v4): buses sleep at Heltinov; 62-1006 (14:35) and 62-1008 (17:35) end their day there. Timed at the inbound rate; the extra departures out of Nový Jičín are buses going home. Every 120 would put the home run 14:35 on the pattern and wait long at both ends (four buses).
- **(e) Knots** (model passing time, min from the nearest real time of trips that run the whole leg): Nový Jičín → Luboměř, Heltinov 15:12 (4), 16:32 (1); Nový Jičín → Odry, autobusová stanice 14:38 (0), 15:58 (5); Luboměř → Odry, autobusová stanice 14:40 (1), 16:00 (2); Luboměř → Nový Jičín, autobusové nádraží 15:18 (1), 16:38 (1).
- **(f) Off the pattern 12–20 h** (min off): Nový Jičín 14:35 (30), 16:05 (40), 17:35 (30), 18:35 (30); Luboměř 13:05 (27), 17:06 (28).
- **(g) Need:** 3 → 2 (waits Nový Jičín 6; Luboměř 3).

## 618 Fulnek-Suchdol nad Odrou, Kletné-Nový Jičín

- **(a) Core points:** Fulnek, železniční stanice · Nový Jičín, autobusové nádraží. Model hours 14:00–16:00.
- **(b) Afternoon (12–20 h, model hours in bold, read at the terminal):** Fulnek → Nový Jičín 12:10, **14:10**, **14:45**, **15:25**, 17:40; Nový Jičín → Fulnek 12:45, **14:00**, **14:35**, **15:12**, 16:32, 18:35.
- **(c) Step 4.** Published every 60: Fulnek slots 14:10 15:10(-) for real 14:10 14:45 15:25: EMPTY; Nový Jičín slots 14:29(-) 15:29(-) for real 14:00 14:35 15:12: EMPTY. published every 60 (Fulnek :10, NJ :29): Fulnek 15:10 empty, NJ 14:29 / 15:29 empty, FAIL. Every 120 three slots each way: passes, all six window departures exact, 8 exact over the day, three buses. Every 72 one slot: passes (Fulnek 14:10, 15:22; NJ 14:00, 15:12), 4 exact, two buses.
- **(d) Simutrans line 618:** Fulnek, železniční stanice → Nový Jičín: every 120, Offset 24 (real 13:25 · 15:25 · 17:25 · 19:25), Also at 69 (real 12:10 · 14:10 · 16:10 · 18:10), 104 (real 12:45 · 14:45 · 16:45 · 18:45); Nový Jičín, autobusové nádraží → Fulnek: every 120, Offset 11 (real 13:12 · 15:12 · 17:12 · 19:12), Also at 59 (real 12:00 · 14:00 · 16:00 · 18:00), 94 (real 12:35 · 14:35 · 16:35 · 18:35).
  Step 4 now: Fulnek 14:10 14:45 15:25 for 14:10 14:45 15:25: ok; Nový Jičín 14:00 14:35 15:12 for 14:00 14:35 15:12: ok. All six window trips are buses that stay on the line (62-1010 14:10 / 15:12, 62-3007 14:00 / 14:45, 62-1005 14:35 / 15:25). Four more exact; +1 bus, on the owner checks.
- **(e) Knots** (model passing time, min from the nearest real time of trips that run the whole leg): Fulnek → Nový Jičín, autobusové nádraží 14:49 (0), 15:24 (0), 16:04 (0); Nový Jičín → Fulnek, železniční stanice 14:37 (1), 15:12 (1), 15:49 (1).
- **(f) Off the pattern 12–20 h** (min off): Fulnek 17:40 (15); Nový Jičín 12:45 (10).
- **(g) Need:** 2 → 3 (waits Fulnek 7, 12, 20; Nový Jičín 31, 23, 36).

## 620 Odry-Suchdol nad Odrou-Nový Jičín

- **(a) Core points:** Nový Jičín, autobusové nádraží · Odry, autobusová stanice · Odry, Pohoř, dolní konec. Model hours 13:20–15:20.
- **(b) Afternoon (12–20 h, model hours in bold, read at the terminal):** Nový Jičín → Odry **13:40**, **15:10**, 16:50; Odry → Nový Jičín **13:58**, **14:33**, 15:50, 18:08.
- **(c) Step 4.** Published every 60: Nový Jičín slots 13:50(-) 14:50(-) for real 13:40 14:00 15:10 15:15: EMPTY; Odry slots 13:58 14:58 for real 13:35 13:58 14:33 14:58: FEWER. published every 60 (NJ :50, Odry :58) counted the Pohoř trips on 620 too (they pass Odry). Now `notvia` Pohoř on both legs. Window: NJ 13:40, 15:10; Odry 13:58, 14:33. Every 90 one slot: passes, 3 exact. Every 120 two slots: passes, 5 exact. Every 160 two slots: passes, 6 exact (the extra one is 20:30).
- **(d) Simutrans line 620:** Nový Jičín, autobusové nádraží → Odry: every 120, Offset 9 (real 13:10 · 15:10 · 17:10 · 19:10), Also at 39 (real 13:40 · 15:40 · 17:40 · 19:40); Odry, autobusová stanice → Nový Jičín: every 120, Offset 57 (real 13:58 · 15:58 · 17:58 · 19:58), Also at 92 (real 12:33 · 14:33 · 16:33 · 18:33).
  Step 4 now: Nový Jičín 13:40 15:10 for 13:40 15:10: ok; Odry 13:58 14:33 for 13:58 14:33: ok. Plain 120 over 160 (one coincidental exact minute).
- **(e) Knots** (model passing time, min from the nearest real time of trips that run the whole leg): Nový Jičín → Odry, autobusová stanice 14:20 (0), 15:50 (7); Odry → Nový Jičín, autobusové nádraží 14:37 (3), 15:12 (7).
- **(f) Off the pattern 12–20 h** (min off): Nový Jičín 16:50 (20); Odry 15:50 (8), 18:08 (10).
- **(g) Need:** 2 → 2 (waits Nový Jičín 40, 35; Odry 17, 12).

## 620 Pohoř Odry-Suchdol nad Odrou-Nový Jičín

- **(a) Core points:** Nový Jičín, autobusové nádraží · Odry, autobusová stanice · Odry, Pohoř, dolní konec. Model hours 13:20–15:20.
- **(b) Afternoon (12–20 h, model hours in bold, read at the terminal):** Nový Jičín → Pohoř 12:45, **14:00**, **15:15**, 18:25; Pohoř → Nový Jičín **13:20**, **14:48**, 16:08.
- **(c) Step 4.** Published every 120: Nový Jičín slots 15:15 for real 14:00 15:15: ok; Pohoř slots 14:08(-) for real 13:20 14:48: EMPTY. published every 120 (NJ 15:15, Pohoř 16:08, 62-1012's round): Pohoř slot 14:08 empty (real 13:20, 14:48), FAIL. Every 120 one slot each way (NJ 15:15, Pohoř 14:48): passes, two buses. Every 120 two slots each way: passes, all four window departures exact, three buses. Every 180 one slot each way (NJ 15:15, Pohoř 13:20): passes, exact, one bus.
- **(d) Simutrans line 620 Pohoř:** Nový Jičín, autobusové nádraží → Pohoř: every 180, Offset 134 (real 12:15 · 15:15 · 18:15); Odry, Pohoř, dolní konec → Nový Jičín: every 180, Offset 19 (real 13:20 · 16:20 · 19:20).
  Step 4 now: Nový Jičín 15:15 for 14:00 15:15: ok; Pohoř 13:20 for 13:20 14:48: ok. Two more exact minutes are not worth two more buses: every 180 with one bus, as published; the two-slot row (three buses) is on the owner checks. 14:00 and 14:48 (the round of 62-1021) are off the pattern. Pohoř has no other line.
- **(e) Knots** (model passing time, min from the nearest real time of trips that run the whole leg): Nový Jičín → Odry, autobusová stanice 15:55 (0); Nový Jičín → Odry, Pohoř, dolní konec 16:05 (0); Pohoř → Nový Jičín, autobusové nádraží 14:09 (5); Pohoř → Odry, autobusová stanice 13:30 (5).
- **(f) Off the pattern 12–20 h** (min off): Nový Jičín 12:45 (30), 14:00 (75), 18:25 (10); Pohoř 14:48 (88), 16:08 (12).
- **(g) Need:** 1 → 1 (waits Nový Jičín 66; Pohoř 15).

## 621 Nošovice-Frýdek-Místek-Příbor-Nový Jičín

- **(a) Core points:** Nový Jičín, autobusové nádraží · Frýdek-Místek, Frýdek, autobusové nádraží · Ostrava, Mor.Ostrava, Náměstí Republiky. Model hours 14:00–16:00.
- **(b) Afternoon (12–20 h, model hours in bold, read at the terminal):** Nový Jičín → Frýdek-Místek 12:35, 13:12, **14:12**, **15:17**, **15:47**, 18:27, 19:37; Frýdek-Místek → Nový Jičín 12:11, **14:06**, **14:36**, 18:40.
- **(c) Step 4.** Published every 90: Nový Jičín slots 14:12 15:42(-) for real 14:12 15:17 15:47: EMPTY; Frýdek-Místek slots 14:06 15:36(-) for real 14:06 14:36: EMPTY. published every 90 (NJ 14:12 / 15:42, Frýdek 14:06 / 15:36): 15:42 and 15:36 empty, FAIL. Every 160 two slots each way: passes (NJ 15:17, 15:47; Frýdek 14:06, 14:36), 6 exact, two buses. Every 120 two slots: passes, 6 exact, three buses.
- **(d) Simutrans line 621:** Nový Jičín, autobusové nádraží → Frýdek-Místek: every 160, Offset 56 (real 12:37 · 15:17 · 17:57), Also at 86 (real 13:07 · 15:47 · 18:27); Frýdek-Místek, Frýdek, autobusové nádraží → Nový Jičín: every 160, Offset 15 (real 14:36 · 17:16 · 19:56), Also at 145 (real 14:06 · 16:46 · 19:26).
  Step 4 now: Nový Jičín 15:17 15:47 for 14:12 15:17 15:47: ok; Frýdek-Místek 14:06 14:36 for 14:06 14:36: ok. Fewer buses at equal exactness. 14:12 (63-1403) goes on to 641 at Frýdek.
- **(e) Knots** (model passing time, min from the nearest real time of trips that run the whole leg): Nový Jičín → Frýdek-Místek, Frýdek, autobusové nádraží 15:59 (6), 16:29 (6); Frýdek-Místek → Nový Jičín, autobusové nádraží 14:48 (9), 15:18 (0).
- **(f) Off the pattern 12–20 h** (min off): Nový Jičín 13:12 (5), 14:12 (65), 19:37 (60); Frýdek-Místek 12:11 (15), 18:40 (46).
- **(g) Need:** 2 → 2 (waits Nový Jičín 25, 25; Frýdek-Místek 43, 43).

## 621 Ostrava Nošovice-Frýdek-Místek-Příbor-Nový Jičín

- **(a) Core points:** Nový Jičín, autobusové nádraží · Frýdek-Místek, Frýdek, autobusové nádraží · Ostrava, Mor.Ostrava, Náměstí Republiky. Model hours 14:00–16:00.
- **(b) Afternoon (12–20 h, model hours in bold, read at the terminal):** Nový Jičín → Mor.Ostrava Náměstí Republiky **14:42**, 16:37; Mor.Ostrava Náměstí Republiky → Nový Jičín **14:48**, **15:18**, 17:15, 19:20.
- **(c) Step 4.** Published every 120: Nový Jičín slots 14:37(-) for real 14:42: EMPTY; Mor.Ostrava Náměstí Republiky slots 15:15 for real 14:48 15:18: ok. published every 120 (NJ 14:37, Ostrava 15:15): NJ 14:37 5 off the real 14:42, FAIL. Every 120 NJ 14:42, Ostrava 15:18: passes, exact, two buses.
- **(d) Simutrans line 621 Ostrava:** Nový Jičín, autobusové nádraží → Mor.Ostrava Náměstí Republiky: every 120, Offset 101 (real 12:42 · 14:42 · 16:42 · 18:42); Ostrava, Mor.Ostrava, Náměstí Republiky → Nový Jičín: every 120, Offset 17 (real 13:18 · 15:18 · 17:18 · 19:18).
  Step 4 now: Nový Jičín 14:42 for 14:42: ok; Mor.Ostrava Náměstí Republiky 15:18 for 14:48 15:18: ok. The builder's shortest-round move undone.
- **(e) Knots** (model passing time, min from the nearest real time of trips that run the whole leg): Nový Jičín → Ostrava, Mor.Ostrava, Náměstí Republiky 15:51 (1); Mor.Ostrava Náměstí Republiky → Nový Jičín, autobusové nádraží 16:28 (1).
- **(f) Off the pattern 12–20 h** (min off): Nový Jičín 16:37 (5); Mor.Ostrava Náměstí Republiky 14:48 (30).
- **(g) Need:** 2 → 2 (waits Nový Jičín 16; Mor.Ostrava Náměstí Republiky 83).

## 622 Mořkov-Hodslavice-Nový Jičín

- **(a) Core points:** Mořkov, železniční stanice · Nový Jičín, autobusové nádraží. Model hours 14:30–16:30.
- **(b) Afternoon (12–20 h, model hours in bold, read at the terminal):** Nový Jičín → Mořkov 13:05, **14:35**, **15:20**, 17:40; Mořkov → Nový Jičín **14:55**, **16:10**.
- **(c) Step 4.** Published every 90: Nový Jičín slots 15:47(-) for real 14:35 15:20: EMPTY; Mořkov slots 14:40(-) 16:10 for real 14:55 16:10: EMPTY. published every 90 (NJ 14:17 / 15:47, Mořkov 14:40 / 16:10): NJ 15:47 empty, Mořkov 14:40 empty, FAIL. Every 120 two slots each way, exact: passes, two buses; every 160 two slots: passes, 5 exact, two buses; every 72 one slot: passes, one bus.
- **(d) Simutrans line 622:** Nový Jičín, autobusové nádraží → Mořkov: every 120, Offset 19 (real 13:20 · 15:20 · 17:20 · 19:20), Also at 91 (real 12:32 · 14:32 · 16:32 · 18:32); Mořkov, železniční stanice → Nový Jičín: every 120, Offset 66 (real 12:07 · 14:07 · 16:07 · 18:07), Also at 114 (real 12:55 · 14:55 · 16:55 · 18:55).
  Step 4 now: Nový Jičín 14:32 15:20 for 14:35 15:20: ok; Mořkov 14:55 16:07 for 14:55 16:10: ok. Every 120 with NJ 14:35 → 14:32 and Mořkov 16:10 → 16:07 (3 min each) works with one bus and 3-min turns.
- **(e) Knots** (model passing time, min from the nearest real time of trips that run the whole leg): Nový Jičín → Mořkov, železniční stanice 14:52 (3), 15:40 (0); Mořkov → Nový Jičín, autobusové nádraží 15:17 (0), 16:29 (3).
- **(f) Off the pattern 12–20 h** (min off): Nový Jičín 13:05 (15), 17:40 (20).
- **(g) Need:** 1 → 1 (waits Nový Jičín 3, 3; Mořkov 3, 27).

## 625 Nový Jičín-Pustějov-Bílovec-Tísek-Slatina

- **(a) Core points:** Nový Jičín, autobusové nádraží · Bílovec, restaurace Beseda · Tísek, obecní úřad. Model hours 15:30–17:30.
- **(b) Afternoon (12–20 h, model hours in bold, read at the terminal):** Nový Jičín → Bílovec 12:37, 14:37, **16:40**; Bílovec → Nový Jičín 12:04, **17:16**, 19:04.
- **(c) Step 4.** Published every 180: Nový Jičín slots 16:32(-) for real 16:40: EMPTY; Bílovec slots 17:16 for real 17:16: ok. published every 180 (NJ 16:32, Bílovec 17:16): NJ 16:32 8 off the real 16:40, FAIL (a 6-min shortest-round move). Every 120 / 180 / 240 one slot each way: pass, two buses. No one-bus row passes: the 16:40 bus reaches Bílovec at 17:21, after the 17:16 leaves (62-1011 and 62-1023 are two buses).
- **(d) Simutrans line 625:** Nový Jičín, autobusové nádraží → Bílovec: every 120, Offset 96 (real 12:37 · 14:37 · 16:37 · 18:37); Bílovec, restaurace Beseda → Nový Jičín: every 120, Offset 15 (real 13:16 · 15:16 · 17:16 · 19:16).
  Step 4 now: Nový Jičín 16:37 for 16:40: ok; Bílovec 17:16 for 17:16: ok. Every 120 at NJ :37 (12:37 and 14:37 exact, 16:37 for 16:40) is the most exact. Need 1 → 2.
- **(e) Knots** (model passing time, min from the nearest real time of trips that run the whole leg): Nový Jičín → Bílovec, restaurace Beseda 17:18 (3); Bílovec → Nový Jičín, autobusové nádraží 18:01 (7).
- **(f) Off the pattern 12–20 h** (min off): Bílovec 12:04 (48), 19:04 (12).
- **(g) Need:** 1 → 2 (waits Nový Jičín 43; Bílovec 118).

## 625 Tísek Nový Jičín-Pustějov-Bílovec-Tísek-Slatina

- **(a) Core points:** Nový Jičín, autobusové nádraží · Bílovec, restaurace Beseda · Tísek, obecní úřad. Model hours 15:30–17:30.
- **(b) Afternoon (12–20 h, model hours in bold, read at the terminal):** Nový Jičín → Tísek 13:07, **15:32**, 18:27; Tísek → Nový Jičín 13:22, 14:24.
- **(c) Step 4.** Published every 180: Nový Jičín slots none for real 15:32: ok; Tísek slots 16:22(-) for real none: EMPTY. published every 180 (NJ 15:27, Tísek 16:22): NJ 15:27 5 off the real 15:32; the Tísek slot 16:22 has no trip (none leaves Tísek for Nový Jičín 15:30–17:30), IRREGULAR in the audit. Every 240, NJ 15:32 and Tísek 14:24: the Tísek slots 10:24, 14:24, 18:24 all fall outside the window, so 0 slots / 0 real; passes both ways, both exact.
- **(d) Simutrans line 625 Tísek:** Nový Jičín, autobusové nádraží → Tísek: every 240, Offset 151 (real 3:32 · 7:32 · 11:32 · 15:32 · 19:32 · 23:32); Tísek, obecní úřad → Nový Jičín: every 240, Offset 83 (real 2:24 · 6:24 · 10:24 · 14:24 · 18:24 · 22:24).
  Step 4 now: Nový Jičín 15:32 for 15:32: ok; Tísek none for none: ok. 62-1023 runs 15:32 out to Tísek and comes back via Bílovec as 625's 17:16 (Step 5b inside the line).
- **(e) Knots** (model passing time, min from the nearest real time of trips that run the whole leg): Nový Jičín → Tísek, obecní úřad 16:22 (6); Tísek → Nový Jičín, autobusové nádraží 3:22 (157*).
- **(f) Off the pattern 12–20 h** (min off): Nový Jičín 13:07 (95), 18:27 (65); Tísek 13:22 (62).
- **(g) Need:** 1 → 1 (waits Nový Jičín 10; Tísek 130).

## 619 Fulnek-Suchdol nad Odrou-Jeseník nad Odrou-Jeseník nad Odrou,Blahutovice

- **(a) Core points:** Fulnek, železniční stanice · Jeseník n.Odrou, Blahutovice, restaurace. Model hours 15:30–17:30.
- **(b) Afternoon (12–20 h, model hours in bold, read at the terminal):** Fulnek → Jeseník n.Odrou 13:25, 17:48; Jeseník n.Odrou → Fulnek **15:45**, 18:55.
- **(c) Step 4.** Published every 180: Fulnek slots 16:25(-) for real none: EMPTY; Jeseník n.Odrou slots 15:38(-) for real 15:45: EMPTY. published every 180 (Fulnek 16:25, Blahutovice 15:38): Fulnek 16:25 empty (no Fulnek departure 15:30–17:30), Blahutovice 15:38 7 off the real 15:45, IRREGULAR / FAIL. Every 180 with Fulnek 17:48 (its slots fall outside the window: 0 / 0) and Blahutovice 15:45: passes, one bus.
- **(d) Simutrans line 619:** Fulnek, železniční stanice → Jeseník n.Odrou: every 180, Offset 107 (real 14:48 · 17:48); Jeseník n.Odrou, Blahutovice, restaurace → Fulnek: every 180, Offset 164 (real 12:45 · 15:45 · 18:45).
  Step 4 now: Fulnek none for none: ok; Jeseník n.Odrou 15:45 for 15:45: ok. 62-1024's round is 17:48 → 18:55; 13:25 is 62-3001 on its way to 616.
- **(e) Knots** (model passing time, min from the nearest real time of trips that run the whole leg): Fulnek → Jeseník n.Odrou, Blahutovice, restaurace 3:32 (153*); Jeseník n.Odrou → Fulnek, železniční stanice 16:29 (0).
- **(f) Off the pattern 12–20 h** (min off): Fulnek 13:25 (83); Jeseník n.Odrou 18:55 (10).
- **(g) Need:** 1 → 1 (waits Fulnek 79; Jeseník n.Odrou 14).

## 927 Kopřivnice-Příbor-Nový Jičín-Hranice

- **(a) Core points:** Nový Jičín, autobusové nádraží · Hranice, autobusová stanice. Model hours 15:30–17:30.
- **(b) Afternoon (12–20 h, model hours in bold, read at the terminal):** Nový Jičín → Hranice 13:01, **16:01**, 18:31; Hranice → Nový Jičín 13:55, **17:00**, 19:50.
- **(c) Step 4.** Published every 180: Nový Jičín slots 16:01 for real 16:01: ok; Hranice slots 16:55(-) for real 17:00: EMPTY. published every 180 (NJ 16:01, Hranice 16:55): Hranice 16:55 5 off the real 17:00, FAIL. Every 180 Hranice 17:00: passes, exact, one bus (every 90 is equal on exact minutes but needs two).
- **(d) Simutrans line 927:** Nový Jičín, autobusové nádraží → Hranice: every 180, Offset 0 (real 13:01 · 16:01 · 19:01); Hranice, autobusová stanice → Nový Jičín: every 180, Offset 59 (real 14:00 · 17:00).
  Step 4 now: Nový Jičín 16:01 for 16:01: ok; Hranice 17:00 for 17:00: ok. One value changed.
- **(e) Knots** (model passing time, min from the nearest real time of trips that run the whole leg): Nový Jičín → Hranice, autobusová stanice 16:34 (0); Hranice → Nový Jičín, autobusové nádraží 17:35 (0).
- **(f) Off the pattern 12–20 h** (min off): Nový Jičín 18:31 (30); Hranice 13:55 (5), 19:50 (10).
- **(g) Need:** 1 → 1 (waits Nový Jičín 86; Hranice 17).

## 665 Mořkov-Životice u Nového Jičína-Nový Jičín

- **(a) Core points:** Mořkov, železniční stanice · Nový Jičín, autobusové nádraží. Model hours 15:30–17:30.
- **(b) Afternoon (12–20 h, model hours in bold, read at the terminal):** Nový Jičín → Mořkov 14:15, 14:50, **16:15**; Mořkov → Nový Jičín 12:10, 13:45, 15:10, **15:55**, 18:10.
- **(c) Step 4.** Published every 90: Nový Jičín slots 15:45(-) 17:15(-) for real 16:15: EMPTY; Mořkov slots 16:40(-) for real 15:55: EMPTY. published every 90 (NJ 15:45 / 17:15, Mořkov 16:40): all window slots empty (real NJ 16:15, Mořkov 15:55), FAIL. Every 120 exact (NJ 16:15, Mořkov 15:55): passes, two buses.
- **(d) Simutrans line 665:** Nový Jičín, autobusové nádraží → Mořkov: every 120, Offset 76 (real 12:17 · 14:17 · 16:17 · 18:17); Mořkov, železniční stanice → Nový Jičín: every 120, Offset 51 (real 13:52 · 15:52 · 17:52 · 19:52).
  Step 4 now: Nový Jičín 16:17 for 16:15: ok; Mořkov 15:52 for 15:55: ok. NJ 16:17 and Mořkov 15:52 (2 and 3 min) work with one bus and 3-min turns, as published.
- **(e) Knots** (model passing time, min from the nearest real time of trips that run the whole leg): Nový Jičín → Mořkov, železniční stanice 16:37 (2); Mořkov → Nový Jičín, autobusové nádraží 16:14 (3).
- **(f) Off the pattern 12–20 h** (min off): Nový Jičín 14:50 (33); Mořkov 12:10 (18), 13:45 (7), 15:10 (42), 18:10 (18).
- **(g) Need:** 1 → 1 (waits Nový Jičín 3; Mořkov 75).

## 667 Nový Jičín-Starý Jičín, Heřmanice

- **(a) Core points:** Nový Jičín, autobusové nádraží · Starý Jičín, Heřmanice, točna. Model hours 15:30–17:30.
- **(b) Afternoon (12–20 h, model hours in bold, read at the terminal):** Nový Jičín → Starý Jičín 12:40, 13:55, 15:05, **15:35**, 17:40; Starý Jičín → Nový Jičín 13:04, 13:29, 14:39, 15:29, **16:06**.
- **(c) Step 4.** Published every 60: Nový Jičín slots 15:40(-) 16:40(-) for real 15:35: EMPTY; Starý Jičín slots 16:29(-) 17:29(-) for real 16:06: EMPTY. published every 60 (NJ :40, Heřmanice :29): 15:40 / 16:40 and 16:29 / 17:29 empty, FAIL. The window 15:30–17:30 has one departure each way; only every 120 or longer passes. Every 120 and 180: pass, exact.
- **(d) Simutrans line 667:** Nový Jičín, autobusové nádraží → Starý Jičín: every 120, Offset 34 (real 13:35 · 15:35 · 17:35 · 19:35); Starý Jičín, Heřmanice, točna → Nový Jičín: every 120, Offset 65 (real 12:06 · 14:06 · 16:06 · 18:06).
  Step 4 now: Nový Jičín 15:35 for 15:35: ok; Starý Jičín 16:06 for 16:06: ok. 62-1014 runs 15:35 → 16:05, turns in 1 min, 16:06 back: one bus. Every 120 is closer to the real hourly rate than 180. Need 2 → 1.
- **(e) Knots** (model passing time, min from the nearest real time of trips that run the whole leg): Nový Jičín → Starý Jičín, Heřmanice, točna 16:05 (0); Starý Jičín → Nový Jičín, autobusové nádraží 16:38 (5).
- **(f) Off the pattern 12–20 h** (min off): Nový Jičín 12:40 (55), 13:55 (20), 15:05 (30), 17:40 (5); Starý Jičín 13:04 (58), 13:29 (37), 14:39 (33), 15:29 (37).
- **(g) Need:** 2 → 1 (waits Nový Jičín 62; Starý Jičín 1).

## 677 Nový Jičín-Studénka-Klimkovice-Ostrava

- **(a) Core points:** Nový Jičín, autobusové nádraží · Studénka, železniční stanice · Ostrava, Svinov, nádraží. Model hours 15:30–17:30.
- **(b) Afternoon (12–20 h, model hours in bold, read at the terminal):** Nový Jičín → Svinov nádraží 12:06, 15:06, **16:06**; Svinov nádraží → Nový Jičín 13:35, **15:35**, **16:35**, 17:35.
- **(c) Step 4.** Published every 90: Nový Jičín slots 16:36(-) for real 16:06: EMPTY; Svinov nádraží slots 16:35 for real 15:35 16:35: ok. published every 90 (NJ 16:36, Svinov 16:35): NJ 16:36 30 off the real 16:06, FAIL. Every 120 NJ 16:06, Svinov 15:35: passes, 5 exact (12:06, 16:06; 13:35, 15:35, 17:35), two buses.
- **(d) Simutrans line 677:** Nový Jičín, autobusové nádraží → Svinov nádraží: every 120, Offset 65 (real 12:06 · 14:06 · 16:06 · 18:06); Ostrava, Svinov, nádraží → Nový Jičín: every 120, Offset 34 (real 13:35 · 15:35 · 17:35 · 19:35).
  Step 4 now: Nový Jičín 16:06 for 16:06: ok; Svinov nádraží 15:35 for 15:35 16:35: ok. Most exact.
- **(e) Knots** (model passing time, min from the nearest real time of trips that run the whole leg): Nový Jičín → Studénka, železniční stanice 16:34 (0); Nový Jičín → Ostrava, Svinov, nádraží 17:27 (0); Svinov nádraží → Nový Jičín, autobusové nádraží 17:00 (7); Svinov nádraží → Studénka, železniční stanice 16:31 (7).
- **(f) Off the pattern 12–20 h** (min off): Nový Jičín 15:06 (60); Svinov nádraží 16:35 (60).
- **(g) Need:** 2 → 2 (waits Nový Jičín 73; Svinov nádraží 8).

## 689 Bernartice nad Odrou-Nový Jičín

- **(a) Core points:** Bernartice n.Odrou, točna · Nový Jičín, autobusové nádraží. Model hours 15:30–17:30.
- **(b) Afternoon (12–20 h, model hours in bold, read at the terminal):** Nový Jičín → Bernartice n.Odrou 13:45, 14:45, **15:45**, 19:50; Bernartice n.Odrou → Nový Jičín 14:10, 15:10, **16:10**.
- **(c) Step 4.** Published every 60: Nový Jičín slots 15:45 16:45(-) for real 15:45: EMPTY; Bernartice n.Odrou slots 16:10 17:10(-) for real 16:10: EMPTY. published every 60 (NJ :45, Bernartice :10): 16:45 and 17:10 empty (the hourly rounds end at 16:10), FAIL. Every 120: passes, 4 exact (13:45, 15:45; 14:10, 16:10).
- **(d) Simutrans line 689:** Nový Jičín, autobusové nádraží → Bernartice n.Odrou: every 120, Offset 44 (real 13:45 · 15:45 · 17:45 · 19:45); Bernartice n.Odrou, točna → Nový Jičín: every 120, Offset 69 (real 12:10 · 14:10 · 16:10 · 18:10).
  Step 4 now: Nový Jičín 15:45 for 15:45: ok; Bernartice n.Odrou 16:10 for 16:10: ok. One bus as published.
- **(e) Knots** (model passing time, min from the nearest real time of trips that run the whole leg): Nový Jičín → Bernartice n.Odrou, točna 16:02 (0); Bernartice n.Odrou → Nový Jičín, autobusové nádraží 16:28 (0).
- **(f) Off the pattern 12–20 h** (min off): Nový Jičín 14:45 (60), 19:50 (5); Bernartice n.Odrou 15:10 (60).
- **(g) Need:** 1 → 1 (waits Nový Jičín 77; Bernartice n.Odrou 8).

## 696 Nový Jičín-Veřovice-Frenštát pod Radhoštěm

- **(a) Core points:** Nový Jičín, autobusové nádraží · Frenštát p.Radh., u škol. Model hours 14:10–16:10.
- **(b) Afternoon (12–20 h, model hours in bold, read at the terminal):** Nový Jičín → Frenštát u škol 12:05, 12:45, 13:20, 13:55, **14:35**, **15:10**, **15:30**, **16:05**, 16:30, 17:00, 17:30, 18:40; Frenštát u škol → Nový Jičín 12:05, 13:10, 13:45, **14:20**, **14:30**, **14:45**, **15:20**, **16:00**, 16:25, 17:20, 18:40, 19:25.
- **(c) Step 4.** Published every 30: Nový Jičín slots 14:30(-) 15:00(-) 15:30 16:00(-) for real 14:35 15:10 15:30 16:05: EMPTY; Frenštát u škol slots 14:20 14:50(-) 15:20 15:50(-) for real 14:20 14:30 14:45 15:20 16:00: EMPTY. published every 30 (NJ :00 / :30, u škol :20 / :50): 3 of 4 NJ slots empty, 2 of 4 u škol slots empty, FAIL. Every 120 four slots each way: passes, all 8 slots exact, 18 exact over the day, four buses (five with 3-min turns). Every 160 four slots: passes, exact in the window, 13 exact, three buses, but 25–30 min off at 13:55 and 16:30. Every 90 three slots: passes, four buses.
- **(d) Simutrans line 696:** Nový Jičín, autobusové nádraží → Frenštát u škol: every 120, Offset 9 (real 13:10 · 15:10 · 17:10 · 19:10), Also at 29 (real 13:30 · 15:30 · 17:30 · 19:30), 62 (real 12:03 · 14:03 · 16:03 · 18:03), 97 (real 12:38 · 14:38 · 16:38 · 18:38); Frenštát p.Radh., u škol → Nový Jičín: every 120, Offset 19 (real 13:20 · 15:20 · 17:20 · 19:20), Also at 56 (real 13:57 · 15:57 · 17:57 · 19:57), 79 (real 12:20 · 14:20 · 16:20 · 18:20), 104 (real 12:45 · 14:45 · 16:45 · 18:45).
  Step 4 now: Nový Jičín 14:38 15:10 15:30 16:03 for 14:35 15:10 15:30 16:05: ok; Frenštát u škol 14:20 14:45 15:20 15:57 for 14:20 14:30 14:45 15:20 16:00: ok. Every 120 keeps the line's every-30 rhythm; NJ 14:35 → 14:38, 16:05 → 16:03 and u škol 16:00 → 15:57 (2–3 min) make it three buses, as published. 14:30 from u škol (62-3014, from the station) is the fifth window departure, off the pattern.
- **(e) Knots** (model passing time, min from the nearest real time of trips that run the whole leg): Nový Jičín → Frenštát p.Radh., u škol 15:17 (3), 15:49 (0), 16:09 (0), 16:42 (2); Frenštát u škol → Nový Jičín, autobusové nádraží 14:58 (6), 15:23 (0), 15:58 (0), 16:35 (3).
- **(f) Off the pattern 12–20 h** (min off): Nový Jičín 12:45 (7), 13:20 (10), 13:55 (8), 16:30 (8), 17:00 (10); Frenštát u škol 12:05 (8), 13:10 (10), 13:45 (12), 14:30 (10), 16:25 (5), 18:40 (5), 19:25 (5).
- **(g) Need:** 3 → 3 (waits Nový Jičín 3, 12, 7, 5; Frenštát u škol 11, 3, 3, 8).

## 697 Nový Jičín-Mořkov-Kopřivnice-Nový Jičín

- **(a) Core points:** Nový Jičín, autobusové nádraží · Kopřivnice, autobusové nádraží. Model hours 14:00–16:00.
- **(b) Afternoon (12–20 h, model hours in bold, read at the terminal):** Nový Jičín → Kopřivnice 12:28, **15:13**, 16:43, 18:25; Kopřivnice → Nový Jičín 12:01, **14:23**, **14:38**, 16:21, 18:35.
- **(c) Step 4.** Published every 120: Nový Jičín slots 14:25(-) for real 15:13: EMPTY; Kopřivnice slots 14:21 for real 14:23 14:38: ok. published every 120 (NJ 14:25, Kopřivnice 14:21): NJ 14:25 empty (real 15:13), FAIL. Every 90: passes, 4 exact, three buses; every 96: passes (NJ 15:13, Kopřivnice 14:38), 3 exact, two buses; every 120 (NJ 15:13, Kopřivnice 14:23): passes, 2 exact, two buses.
- **(d) Simutrans line 697:** Nový Jičín, autobusové nádraží → Kopřivnice: every 96, Offset 84 (real 12:01 · 13:37 · 15:13 · 16:49 · 18:25); Kopřivnice, autobusové nádraží → Nový Jičín: every 96, Offset 49 (real 13:02 · 14:38 · 16:14 · 17:50 · 19:26).
  Step 4 now: Nový Jičín 15:13 for 15:13: ok; Kopřivnice 14:38 for 14:23 14:38: ok. Every 96 serves the same window departures on the minute as every 90 with one bus fewer.
- **(e) Knots** (model passing time, min from the nearest real time of trips that run the whole leg): Nový Jičín → Kopřivnice, autobusové nádraží 16:10 (1); Kopřivnice → Nový Jičín, autobusové nádraží 15:34 (3).
- **(f) Off the pattern 12–20 h** (min off): Nový Jičín 12:28 (27), 16:43 (6); Kopřivnice 12:01 (35), 14:23 (15), 16:21 (7), 18:35 (45).
- **(g) Need:** 2 → 2 (waits Nový Jičín 72; Kopřivnice 4).

## 987 Nový Jičín-Hodslavice-Valašské Meziříčí

- **(a) Core points:** Nový Jičín, autobusové nádraží · Valašské Meziříčí, autobusová stanice. Model hours 13:30–15:30.
- **(b) Afternoon (12–20 h, model hours in bold, read at the terminal):** Nový Jičín → Valašské Meziříčí 12:20, **13:55**, **15:20**, 16:45, 18:55; Valašské Meziříčí → Nový Jičín **13:30**, **14:35**, **15:05**, 16:10, 17:55, 19:25.
- **(c) Step 4.** Published every 60: Nový Jičín slots 13:55 14:55(-) for real 13:55 15:20: EMPTY; Valašské Meziříčí slots 13:30 14:30(-) for real 13:30 14:35 15:05: EMPTY. published every 60 (NJ :55, VM :30): NJ 14:55 and VM 14:30 empty, FAIL. Every 180 two slots each way: passes (NJ 13:55, 15:20; VM 13:30, 15:05), 6 exact, two buses. Every 160 two slots: 6 exact, two buses. Every 120: 6 exact, three buses.
- **(d) Simutrans line 987:** Nový Jičín, autobusové nádraží → Valašské Meziříčí: every 180, Offset 54 (real 13:55 · 16:55 · 19:55), Also at 139 (real 12:20 · 15:20 · 18:20); Valašské Meziříčí, autobusová stanice → Nový Jičín: every 180, Offset 29 (real 13:30 · 16:30 · 19:30), Also at 124 (real 12:05 · 15:05 · 18:05).
  Step 4 now: Nový Jičín 13:55 15:20 for 13:55 15:20: ok; Valašské Meziříčí 13:30 15:05 for 13:30 14:35 15:05: ok. Plain 180 at equal counts. 14:35 from VM is 62-1013, which came out on 988 (987 and 988 swap buses at Valašské Meziříčí).
- **(e) Knots** (model passing time, min from the nearest real time of trips that run the whole leg): Nový Jičín → Valašské Meziříčí, autobusová stanice 14:22 (0), 15:47 (0); Valašské Meziříčí → Nový Jičín, autobusové nádraží 13:58 (0), 15:33 (0).
- **(f) Off the pattern 12–20 h** (min off): Nový Jičín 16:45 (10), 18:55 (35); Valašské Meziříčí 14:35 (30), 16:10 (20), 17:55 (10), 19:25 (5).
- **(g) Need:** 2 → 2 (waits Nový Jičín 82, 82; Valašské Meziříčí 43, 43).

## 988 Nový Jičín-Starý Jičín-Lešná-Valašské Meziříčí

- **(a) Core points:** Nový Jičín, autobusové nádraží · Valašské Meziříčí, autobusová stanice. Model hours 15:30–17:30.
- **(b) Afternoon (12–20 h, model hours in bold, read at the terminal):** Nový Jičín → Valašské Meziříčí 12:15, 13:00, 14:15, 15:25, **16:40**, 18:40; Valašské Meziříčí → Nový Jičín 12:05, 13:20, 14:30, **16:15**, 17:30, 19:30.
- **(c) Step 4.** Published every 60: Nový Jičín slots 15:40(-) 16:40 for real 16:40: EMPTY; Valašské Meziříčí slots 15:30(-) 16:30(-) for real 16:15: EMPTY. published every 60 (NJ :40, VM :30): 15:40, 15:30, 16:30 empty, FAIL. The window 15:30–17:30 has one departure each way. Every 80 and 120 one slot: pass, 3 exact.
- **(d) Simutrans line 988:** Nový Jičín, autobusové nádraží → Valašské Meziříčí: every 120, Offset 99 (real 12:40 · 14:40 · 16:40 · 18:40); Valašské Meziříčí, autobusová stanice → Nový Jičín: every 120, Offset 74 (real 12:15 · 14:15 · 16:15 · 18:15).
  Step 4 now: Nový Jičín 16:40 for 16:40: ok; Valašské Meziříčí 16:15 for 16:15: ok. Plain 120.
- **(e) Knots** (model passing time, min from the nearest real time of trips that run the whole leg): Nový Jičín → Valašské Meziříčí, autobusová stanice 17:24 (1); Valašské Meziříčí → Nový Jičín, autobusové nádraží 17:01 (1).
- **(f) Off the pattern 12–20 h** (min off): Nový Jičín 12:15 (25), 13:00 (20), 14:15 (25), 15:25 (45); Valašské Meziříčí 12:05 (10), 13:20 (55), 14:30 (15), 17:30 (45), 19:30 (45).
- **(g) Need:** 2 → 2 (waits Nový Jičín 99; Valašské Meziříčí 52).

## 379 Ostrava,Zábřeh-Krmelín-Stará Ves nad Ondřejnicí-Petřvald-Trnávka

- **(a) Core points:** Petřvald, náměstí · Ostrava, Zábřeh, Kotva. Model hours 15:30–17:30.
- **(b) Afternoon (12–20 h, model hours in bold, read at the terminal):** Petřvald → Zábřeh Kotva 12:58, 14:18, **15:38**; Zábřeh Kotva → Petřvald 13:42, 14:57.
- **(c) Step 4.** Published every 180: Petřvald slots 15:38 for real 15:38: ok; Zábřeh Kotva slots 16:42(-) for real none: EMPTY. published every 180 (Petřvald 15:38, Zábřeh 16:42): the Zábřeh slot 16:42 has no trip to Petřvald, náměstí (after 15:38 the line runs short trips), IRREGULAR in the audit. Every 180 with Zábřeh 14:57: its slots 11:57, 14:57, 17:57 fall outside the window (0 / 0); Petřvald 15:38 exact: passes.
- **(d) Simutrans line 379:** Petřvald, náměstí → Zábřeh Kotva: every 180, Offset 157 (real 12:38 · 15:38 · 18:38); Ostrava, Zábřeh, Kotva → Petřvald: every 180, Offset 116 (real 14:57 · 17:57).
  Step 4 now: Petřvald 15:38 for 15:38: ok; Zábřeh Kotva none for none: ok. 63-1321 runs 14:57 → 15:38 with a 5-min turn: one bus.
- **(e) Knots** (model passing time, min from the nearest real time of trips that run the whole leg): Petřvald → Ostrava, Zábřeh, Kotva 16:12 (0); Zábřeh Kotva → Petřvald, náměstí 3:33 (470*); Zábřeh Kotva → Ostrava, Zábřeh, Kotva 2:57 (470*).
- **(f) Off the pattern 12–20 h** (min off): Petřvald 12:58 (20), 14:18 (80); Zábřeh Kotva 13:42 (75).
- **(g) Need:** 1 → 1 (waits Petřvald 5; Zábřeh Kotva 105).

## 670 Nový Jičín-Sedlnice-Mošnov-Stará Ves nad Ondřejnicí-Ostrava

- **(a) Core points:** Nový Jičín, autobusové nádraží · Ostrava, Dubina. Model hours 15:40–17:40.
- **(b) Afternoon (12–20 h, model hours in bold, read at the terminal):** Nový Jičín → Dubina 12:04, 13:01, 15:05, **15:55**, **17:08**, **17:38**; Dubina → Nový Jičín 13:50, 14:50, **16:20**, **17:20**, 18:45, 19:55.
- **(c) Step 4.** Published every 60: Nový Jičín slots 16:05(-) 17:05 for real 15:55 17:08 17:38: EMPTY; Dubina slots 15:50(-) 16:50(-) for real 16:20 17:20: EMPTY. published every 60 (NJ :05, Dubina :50): NJ 16:05 empty, Dubina 15:50 / 16:50 empty, FAIL. Every 120 two slots each way: passes (NJ 15:55, 17:05; Dubina 16:20, 17:20), 5 exact, three buses. Every 160: 5 exact, three buses. Every 180 two slots (NJ 15:55, 17:38): passes, 4 exact, two buses, but 30 min off at 15:05 and 17:08.
- **(d) Simutrans line 670:** Nový Jičín, autobusové nádraží → Dubina: every 120, Offset 4 (real 13:05 · 15:05 · 17:05 · 19:05), Also at 54 (real 13:55 · 15:55 · 17:55 · 19:55); Ostrava, Dubina → Nový Jičín: every 120, Offset 19 (real 13:20 · 15:20 · 17:20 · 19:20), Also at 79 (real 12:20 · 14:20 · 16:20 · 18:20).
  Step 4 now: Nový Jičín 15:55 17:05 for 15:55 17:08 17:38: ok; Dubina 16:20 17:20 for 16:20 17:20: ok. Every 120 keeps 63-1324 (15:05, 16:20, 17:08), which stays on the line, on the pattern; every 180 drops it and keeps 17:38 (63-1206, on to 621). Three buses as published.
- **(e) Knots** (model passing time, min from the nearest real time of trips that run the whole leg): Nový Jičín → Ostrava, Dubina 16:53 (3), 18:03 (2); Dubina → Nový Jičín, autobusové nádraží 17:12 (4), 18:12 (2).
- **(f) Off the pattern 12–20 h** (min off): Nový Jičín 12:04 (9), 13:01 (4), 17:38 (17); Dubina 13:50 (30), 14:50 (30), 18:45 (25), 19:55 (25).
- **(g) Need:** 3 → 3 (waits Nový Jičín 55, 45; Dubina 16, 26).

## 370 Ostrava-Krmelín-Paskov-Řepiště

- **(a) Core points:** Ostrava, Dubina · Řepiště, u kříže. Model hours 15:30–17:30.
- **(b) Afternoon (12–20 h, model hours in bold, read at the terminal):** Dubina → Řepiště 12:49, 13:49, 15:19, **16:19**, 17:49; Řepiště → Dubina 13:02, 14:02, 14:52, **16:02**, **17:02**, 19:22.
- **(c) Step 4.** Published every 60: Dubina slots 15:43(-) 16:43(-) for real 16:19: EMPTY; Řepiště slots 16:08(-) 17:08(-) for real 16:02 17:02: EMPTY. published every 60 (Dubina :43, Řepiště :08): all four window slots empty (6-min shortest-round moves), FAIL. Every 60 at the real minutes fails too (the window holds Dubina 16:19 only). Every 90 one slot: passes, 4 exact (16:19, 17:49; 13:02, 16:02), two buses. Every 120: 3 exact, two buses. Every 240: passes, 3 exact, one bus.
- **(d) Simutrans line 370:** Ostrava, Dubina → Řepiště: every 90, Offset 18 (real 13:19 · 14:49 · 16:19 · 17:49 · 19:19); Řepiště, u kříže → Dubina: every 90, Offset 1 (real 13:02 · 14:32 · 16:02 · 17:32 · 19:02).
  Step 4 now: Dubina 16:19 for 16:19: ok; Řepiště 16:02 for 16:02 17:02: ok. Every 90 is the closest to the real hourly rate that passes. Need 1 → 2; every 240 with one bus is on the owner checks.
- **(e) Knots** (model passing time, min from the nearest real time of trips that run the whole leg): Dubina → Řepiště, u kříže 16:41 (0); Řepiště → Ostrava, Dubina 16:25 (0).
- **(f) Off the pattern 12–20 h** (min off): Dubina 12:49 (30), 13:49 (30), 15:19 (30); Řepiště 14:02 (30), 14:52 (20), 17:02 (30), 19:22 (20).
- **(g) Need:** 1 → 2 (waits Dubina 84; Řepiště 51).

## 371 Ostrava-Brušperk-Hukvaldy-Kozlovice

- **(a) Core points:** Ostrava, Dubina · Hukvaldy, hotel · Kozlovice, střed. Model hours 15:30–17:30.
- **(b) Afternoon (12–20 h, model hours in bold, read at the terminal):** Dubina → Kozlovice 13:45, 14:20, **15:50**, **16:55**, 17:55, 18:55, 19:55; Kozlovice → Dubina 14:15, 15:15, **16:15**, 17:45, 19:20.
- **(c) Step 4.** Published every 60: Dubina slots 15:55(-) 16:55 for real 15:50 16:55: EMPTY; Kozlovice slots 16:09(-) 17:09(-) for real 16:15: EMPTY. published every 60 (Dubina :55, Kozlovice :09 = Hukvaldy :20): Dubina 15:55 5 off 15:50, Kozlovice 16:09 / 17:09 empty, FAIL. Every 120 exact (Dubina 16:55, Kozlovice 16:15): passes, 4 exact, two buses. Every 90: 4 exact, two buses.
- **(d) Simutrans line 371:** Ostrava, Dubina → Kozlovice: every 120, Offset 117 (real 12:58 · 14:58 · 16:58 · 18:58); Kozlovice, střed → Dubina: every 120, Offset 71 (real 12:12 · 14:12 · 16:12 · 18:12); passes Hukvaldy, hotel at 12:23 · 14:23 · 16:23 · 18:23.
  Step 4 now: Dubina 16:58 for 15:50 16:55: ok; Kozlovice 16:12 for 16:15: ok. Dubina 16:55 → 16:58 and Kozlovice 16:15 → 16:12 (3 min each) work with one bus and 3-min turns. Hukvaldy, hotel is the knot: the return is timed so the bus passes it at 16:23.
- **(e) Knots** (model passing time, min from the nearest real time of trips that run the whole leg): Dubina → Hukvaldy, hotel 17:33 (57*); Dubina → Kozlovice, střed 17:44 (57*); Kozlovice → Ostrava, Dubina 16:55 (3).
- **(f) Off the pattern 12–20 h** (min off): Dubina 13:45 (47), 14:20 (38), 15:50 (52), 17:55 (57), 19:55 (57); Kozlovice 15:15 (57), 17:45 (27), 19:20 (52).
- **(g) Need:** 2 → 1 (waits Dubina 3; Kozlovice 28).

## 373 Ostrava-Petřvald-Trnávka-Příbor-Kopřivnice

- **(a) Core points:** Kopřivnice, autobusové nádraží · Ostrava, Dubina. Model hours 13:50–15:50.
- **(b) Afternoon (12–20 h, model hours in bold, read at the terminal):** Dubina → Kopřivnice 12:20, **14:20**, **15:20**, 16:20, 17:20, 18:20; Kopřivnice → Dubina **14:38**, **15:43**, 16:38, 17:44, 18:44.
- **(c) Step 4.** Published every 60: Dubina slots 14:20 15:20 for real 14:20 15:20: ok; Kopřivnice slots 14:44(-) 15:44 for real 14:38 15:43: EMPTY. published every 60 (Dubina :20, Kopřivnice :44): Kopřivnice 14:44 6 off the real 14:38, FAIL. Every 60 Kopřivnice :41: passes (within 3), 0 exact there. Every 120 two slots: passes, Kopřivnice 14:38 and 15:43 exact (the real timetable alternates :38 / :43), 10 exact.
- **(d) Simutrans line 373:** Ostrava, Dubina → Kopřivnice: every 120, Offset 19 (real 13:20 · 15:20 · 17:20 · 19:20), Also at 79 (real 12:20 · 14:20 · 16:20 · 18:20); Kopřivnice, autobusové nádraží → Dubina: every 120, Offset 42 (real 13:43 · 15:43 · 17:43 · 19:43), Also at 97 (real 12:38 · 14:38 · 16:38 · 18:38).
  Step 4 now: Dubina 14:20 15:20 for 14:20 15:20: ok; Kopřivnice 14:38 15:43 for 14:38 15:43: ok. Most exact; three buses as published.
- **(e) Knots** (model passing time, min from the nearest real time of trips that run the whole leg): Dubina → Kopřivnice, autobusové nádraží 15:22 (0), 16:22 (0); Kopřivnice → Ostrava, Dubina 15:39 (7), 16:44 (2).
- **(f) Off the pattern 12–20 h** (min off): Kopřivnice 18:44 (6).
- **(g) Need:** 3 → 3 (waits Dubina 31, 36; Kopřivnice 16, 21).

## 374 Ostrava,Svinov-Stará Ves nad Ondřejnicí-Brušperk-Trnávka

- **(a) Core points:** Ostrava, Svinov, mosty · Trnávka, požární zbrojnice. Model hours 13:50–15:50.
- **(b) Afternoon (12–20 h, model hours in bold, read at the terminal):** Svinov mosty → Trnávka **13:50**, **14:20**, **15:25**, 16:25, 17:30, 18:30; Trnávka → Svinov mosty 12:30, **14:35**, **15:35**, 16:35, 17:35.
- **(c) Step 4.** Published every 60: Svinov mosty slots 14:25(-) 15:25 for real 13:50 14:20 15:25: EMPTY; Trnávka slots 14:35 15:35 for real 14:35 15:35: ok. published every 60 (Svinov :25, Trnávka :35): Svinov 14:25 5 off the real 14:20, FAIL. Every 120 two slots each way exact: passes, three buses. Every 180 two slots: passes, two buses, 30–60 min off later.
- **(d) Simutrans line 374:** Ostrava, Svinov, mosty → Trnávka: every 120, Offset 24 (real 13:25 · 15:25 · 17:25 · 19:25), Also at 80 (real 12:21 · 14:21 · 16:21 · 18:21); Trnávka, požární zbrojnice → Svinov mosty: every 120, Offset 31 (real 13:32 · 15:32 · 17:32 · 19:32), Also at 94 (real 12:35 · 14:35 · 16:35 · 18:35).
  Step 4 now: Svinov mosty 14:21 15:25 for 13:50 14:20 15:25: ok; Trnávka 14:35 15:32 for 14:35 15:35: ok. Every 120 with Svinov 14:20 → 14:21 and Trnávka 15:35 → 15:32 works with two buses and 3-min turns, as the two real buses (63-1346, 63-1338) do. 13:50 is 63-1351 on its way to 634.
- **(e) Knots** (model passing time, min from the nearest real time of trips that run the whole leg): Svinov mosty → Trnávka, požární zbrojnice 15:12 (1), 16:16 (0); Trnávka → Ostrava, Svinov, mosty 15:21 (0), 16:18 (3).
- **(f) Off the pattern 12–20 h** (min off): Svinov mosty 13:50 (25), 16:25 (4), 17:30 (5), 18:30 (9); Trnávka 12:30 (5).
- **(g) Need:** 2 → 2 (waits Svinov mosty 3, 4; Trnávka 17, 18).

## 376 Ostrava-Stará Ves nad Ondřejnicí-Brušperk-Fryčovice-Příbor-Kopřivnice

- **(a) Core points:** Ostrava, Dubina · Hukvaldy, Rychaltice, pod mostem. Model hours 15:10–17:10.
- **(b) Afternoon (12–20 h, model hours in bold, read at the terminal):** Dubina → Hukvaldy 12:40, 13:05, **16:10**, **17:05**; Hukvaldy → Dubina 13:18, 13:58, 15:03, **16:03**, **17:03**, 19:03.
- **(c) Step 4.** Published every 60: Dubina slots 16:05(-) 17:05 for real 16:10 17:05: EMPTY; Hukvaldy slots 16:03 17:03 for real 16:03 17:03: ok. published every 60 (Dubina :05, Rychaltice :03): Dubina 16:05 5 off the real 16:10, FAIL. Every 120 two slots each way: passes, all exact, 7 exact over the day.
- **(d) Simutrans line 376:** Ostrava, Dubina → Hukvaldy: every 120, Offset 4 (real 13:05 · 15:05 · 17:05 · 19:05), Also at 69 (real 12:10 · 14:10 · 16:10 · 18:10); Hukvaldy, Rychaltice, pod mostem → Dubina: every 120, Offset 2 (real 13:03 · 15:03 · 17:03 · 19:03), Also at 62 (real 12:03 · 14:03 · 16:03 · 18:03).
  Step 4 now: Dubina 16:10 17:05 for 16:10 17:05: ok; Hukvaldy 16:03 17:03 for 16:03 17:03: ok. Two buses as published.
- **(e) Knots** (model passing time, min from the nearest real time of trips that run the whole leg): Dubina → Hukvaldy, Rychaltice, pod mostem 16:40 (2), 17:35 (2); Hukvaldy → Ostrava, Dubina 16:34 (1), 17:34 (2).
- **(f) Off the pattern 12–20 h** (min off): Dubina 12:40 (25); Hukvaldy 13:18 (15), 13:58 (5).
- **(g) Need:** 2 → 2 (waits Dubina 32, 37; Hukvaldy 23, 28).

## 634 Kopřivnice-Lichnov-Frenštát pod Radhoštěm

- **(a) Core points:** Kopřivnice, autobusové nádraží · Frenštát p.Radh., u škol. Model hours 14:20–16:20.
- **(b) Afternoon (12–20 h, model hours in bold, read at the terminal):** Kopřivnice → Frenštát u škol 12:38, 13:08, **14:28**, **15:38**, 16:38, 18:15; Frenštát u škol → Kopřivnice 12:35, 13:20, **14:28**, **14:58**, **15:58**, 17:28, 19:20.
- **(c) Step 4.** Published every 60: Kopřivnice slots 14:38(-) 15:38 for real 14:28 15:38: EMPTY; Frenštát u škol slots 14:28 15:28(-) for real 14:28 14:58 15:58: EMPTY. published every 60 (Kopřivnice :38, u škol :28): Kopřivnice 14:38 empty (real 14:28), u škol 15:28 empty, FAIL. Every 90: passes (Kopřivnice 15:38; u škol 14:28, 15:58), 6 exact, two buses. Every 180 two slots: passes, 7 exact, three buses.
- **(d) Simutrans line 634:** Kopřivnice, autobusové nádraží → Frenštát u škol: every 90, Offset 67 (real 12:38 · 14:08 · 15:38 · 17:08 · 18:38); Frenštát p.Radh., u škol → Kopřivnice: every 90, Offset 87 (real 12:58 · 14:28 · 15:58 · 17:28 · 18:58).
  Step 4 now: Kopřivnice 15:38 for 14:28 15:38: ok; Frenštát u škol 14:28 15:58 for 14:28 14:58 15:58: ok. One more exact minute is not worth a bus; the trips every 90 leaves off are buses going on to other lines (63-1303 to 657, 63-1304 to 638).
- **(e) Knots** (model passing time, min from the nearest real time of trips that run the whole leg): Kopřivnice → Frenštát p.Radh., u škol 16:14 (0); Frenštát u škol → Kopřivnice, autobusové nádraží 15:05 (0), 16:35 (0).
- **(f) Off the pattern 12–20 h** (min off): Kopřivnice 13:08 (30), 14:28 (20), 16:38 (30), 18:15 (23); Frenštát u škol 12:35 (23), 13:20 (22), 14:58 (30), 19:20 (22).
- **(g) Need:** 2 → 2 (waits Kopřivnice 33; Frenštát u škol 74).

## 635 Kopřivnice-Frenštát pod Radhoštěm

- **(a) Core points:** Kopřivnice, autobusové nádraží · Frenštát p.Radh., u škol. Model hours 14:00–16:00.
- **(b) Afternoon (12–20 h, model hours in bold, read at the terminal):** Kopřivnice → Frenštát u škol 13:51, **14:18**, **15:28**; Frenštát u škol → Kopřivnice 13:20, **14:05**, **14:15**, **14:25**, **15:55**.
- **(c) Step 4.** Published every 60: Kopřivnice slots 14:18 15:18(-) for real 14:18 15:28: EMPTY; Frenštát u škol slots 14:25 15:25(-) for real 14:05 14:15 14:25 15:55: EMPTY. published every 60 (Kopřivnice :18, u škol :25): Kopřivnice 15:18 empty (real 15:28), u škol 15:25 empty, FAIL. u škol has four window departures (14:05, 14:15, 14:25, 15:55) against Kopřivnice's two: no row with the same slots both ways passes.
- **(d) Simutrans line 635:** Kopřivnice, autobusové nádraží → Frenštát u škol: every 120, Offset 27 (real 13:28 · 15:28 · 17:28 · 19:28), Also at 77 (real 12:18 · 14:18 · 16:18 · 18:18); Frenštát p.Radh., u škol → Kopřivnice: every 120, Offset 54 (real 13:55 · 15:55 · 17:55 · 19:55), Also at 84 (real 12:25 · 14:25 · 16:25 · 18:25).
  Step 4 now: Kopřivnice 14:18 15:28 for 14:18 15:28: ok; Frenštát u škol 14:25 15:55 for 14:05 14:15 14:25 15:55: FEWER. Reverse outstation: the Continental shift change sends buses back to Kopřivnice, where they go on as 634, 646 and 653. Timed at the Kopřivnice rate (every 120, two slots each way); u škol keeps 14:25 and 15:55 (63-1003's own round 15:28 → 15:55) and lists 14:05, 14:15 off: FEWER by hand.
- **(e) Knots** (model passing time, min from the nearest real time of trips that run the whole leg): Kopřivnice → Frenštát p.Radh., u škol 14:42 (2), 15:52 (2); Frenštát u škol → Kopřivnice, autobusové nádraží 14:43 (0), 16:13 (0).
- **(f) Off the pattern 12–20 h** (min off): Kopřivnice 13:51 (23); Frenštát u škol 13:20 (35), 14:05 (10), 14:15 (10).
- **(g) Need:** 2 → 2 (waits Kopřivnice 5, 45; Frenštát u škol 105, 5).

## 638 Kopřivnice-Příbor,Hájov-Hukvaldy

- **(a) Core points:** Kopřivnice, autobusové nádraží · Hukvaldy, Dolní Sklenov, rozcestí. Model hours 15:30–17:30.
- **(b) Afternoon (12–20 h, model hours in bold, read at the terminal):** Kopřivnice → Hukvaldy 13:27, 14:27, 15:14, 17:39; Hukvaldy → Kopřivnice 12:36, 14:16, **15:51**, 18:36.
- **(c) Step 4.** Published every 90: Kopřivnice slots 16:37(-) for real none: EMPTY; Hukvaldy slots 15:36(-) 17:06(-) for real 15:51: EMPTY. published every 90 (Kopřivnice 16:37, Sklenov 15:36 / 17:06): all slots empty (no Kopřivnice departure 15:30–17:30; Sklenov real 15:51), IRREGULAR / FAIL. Every 180 with Kopřivnice 15:14 (slots 12:14, 15:14, 18:14 outside the window: 0 / 0) and Sklenov 15:51 exact: passes, one bus.
- **(d) Simutrans line 638:** Kopřivnice, autobusové nádraží → Hukvaldy: every 180, Offset 133 (real 12:14 · 15:14 · 18:14); Hukvaldy, Dolní Sklenov, rozcestí → Kopřivnice: every 180, Offset 170 (real 12:51 · 15:51 · 18:51).
  Step 4 now: Kopřivnice none for none: ok; Hukvaldy 15:51 for 15:51: ok. 63-1010's round: 15:14 out to Rychaltice, 15:46 back past Sklenov 15:51.
- **(e) Knots** (model passing time, min from the nearest real time of trips that run the whole leg): Kopřivnice → Kopřivnice, autobusové nádraží 0:14 (306*); Kopřivnice → Hukvaldy, Dolní Sklenov, rozcestí 0:40 (300*); Hukvaldy → Kopřivnice, autobusové nádraží 16:10 (0).
- **(f) Off the pattern 12–20 h** (min off): Kopřivnice 13:27 (73), 14:27 (47), 17:39 (35); Hukvaldy 12:36 (15), 14:16 (85), 18:36 (15).
- **(g) Need:** 1 → 1 (waits Kopřivnice 124; Hukvaldy 11).

## 644 Kopřivnice-Štramberk

- **(a) Core points:** Kopřivnice, autobusové nádraží · Štramberk, Libotín, koupaliště. Model hours 15:30–17:30.
- **(b) Afternoon (12–20 h, model hours in bold, read at the terminal):** Kopřivnice → Štramberk 12:00, **15:45**, **17:10**, 18:40; Štramberk → Kopřivnice 13:12, **16:12**, 17:52, 19:12.
- **(c) Step 4.** Published every 120: Kopřivnice slots 16:40(-) for real 15:45 17:10: EMPTY; Štramberk slots 17:12(-) for real 16:12: EMPTY. published every 120 (Kopřivnice 16:40, Libotín 17:12): both slots empty (real 15:45, 17:10; 16:12), FAIL. Every 180: passes, 4 exact (15:45; 13:12, 16:12, 19:12), one bus. Every 90 (Kopřivnice 15:42 / 17:12 within 3): passes, 3 exact, one bus.
- **(d) Simutrans line 644:** Kopřivnice, autobusové nádraží → Štramberk: every 180, Offset 164 (real 12:45 · 15:45 · 18:45); Štramberk, Libotín, koupaliště → Kopřivnice: every 180, Offset 11 (real 13:12 · 16:12 · 19:12).
  Step 4 now: Kopřivnice 15:45 for 15:45 17:10: ok; Štramberk 16:12 for 16:12: ok. Most exact.
- **(e) Knots** (model passing time, min from the nearest real time of trips that run the whole leg): Kopřivnice → Štramberk, Libotín, koupaliště 16:08 (2); Štramberk → Kopřivnice, autobusové nádraží 16:37 (0).
- **(f) Off the pattern 12–20 h** (min off): Kopřivnice 12:00 (45), 17:10 (85), 18:40 (5); Štramberk 17:52 (80).
- **(g) Need:** 1 → 1 (waits Kopřivnice 128; Štramberk 3).

## 646 Kopřivnice-Štramberk-Rybí-Nový Jičín

- **(a) Core points:** Kopřivnice, autobusové nádraží · Nový Jičín, autobusové nádraží. Model hours 13:40–15:40.
- **(b) Afternoon (12–20 h, model hours in bold, read at the terminal):** Nový Jičín → Kopřivnice 13:30, **14:00**, **14:30**, **15:10**, **15:30**, 16:40; Kopřivnice → Nový Jičín 13:10, **14:10**, **14:40**.
- **(c) Step 4.** Published every 60: Nový Jičín slots 14:30 15:30 for real 14:00 14:30 15:10 15:30: FEWER; Kopřivnice slots 14:10 15:10(-) for real 14:10 14:40: EMPTY. published every 60 (NJ :30, Kopřivnice :10): NJ 2 slots / 4 real, Kopřivnice 15:10 empty, FAIL. Every 90 two slots each way: passes (NJ 14:00, 14:30, 15:30 for 4 real; Kopřivnice 14:10, 14:40), all exact, three buses. No two-bus row passes.
- **(d) Simutrans line 646:** Nový Jičín, autobusové nádraží → Kopřivnice: every 90, Offset 59 (real 12:30 · 14:00 · 15:30 · 17:00 · 18:30), Also at 89 (real 13:00 · 14:30 · 16:00 · 17:30 · 19:00); Kopřivnice, autobusové nádraží → Nový Jičín: every 90, Offset 9 (real 13:10 · 14:40 · 16:10 · 17:40 · 19:10), Also at 69 (real 12:40 · 14:10 · 15:40 · 17:10 · 18:40).
  Step 4 now: Nový Jičín 14:00 14:30 15:30 for 14:00 14:30 15:10 15:30: ok; Kopřivnice 14:10 14:40 for 14:10 14:40: ok. 15:10 (63-1341) is off the pattern. Need 2 → 3.
- **(e) Knots** (model passing time, min from the nearest real time of trips that run the whole leg): Nový Jičín → Kopřivnice, autobusové nádraží 14:34 (0), 15:04 (0), 16:04 (0); Kopřivnice → Nový Jičín, autobusové nádraží 14:47 (1), 15:17 (1).
- **(f) Off the pattern 12–20 h** (min off): Nový Jičín 13:30 (30), 15:10 (20), 16:40 (20).
- **(g) Need:** 2 → 3 (waits Nový Jičín 12, 72; Kopřivnice 36, 6).

## 653 Frenštát pod Radhoštěm-Tichá-Kopřivnice

- **(a) Core points:** Kopřivnice, autobusové nádraží · Kopřivnice, železniční stanice · Frenštát p.Radh., u škol. Model hours 15:30–17:30.
- **(b) Afternoon (12–20 h, model hours in bold, read at the terminal):** Kopřivnice → Frenštát station 12:00, 13:10, 14:10, 15:15, **17:15**; Frenštát u škol → Kopřivnice 12:00, 13:00, 14:25, **15:55**, **16:55**.
- **(c) Step 4.** Published every 60: Kopřivnice slots 16:10(-) 17:10(-) for real 17:15: EMPTY; Frenštát u škol slots 15:55 16:55 for real 15:55 16:55: ok. published every 60 (Kopřivnice :10, u škol :55): Kopřivnice 16:10, 17:10 empty (real 17:15), FAIL. Every 120: passes (Kopřivnice 17:15; u škol 15:55 for 15:55 and 16:55), 5 exact, two buses.
- **(d) Simutrans line 653:** Kopřivnice, autobusové nádraží → Frenštát station: every 120, Offset 14 (real 13:15 · 15:15 · 17:15 · 19:15); Frenštát p.Radh., železniční stanice → Frenštát u škol: Departure every 0 (no timetable); Frenštát p.Radh., u škol → Kopřivnice: every 120, Offset 54 (real 13:55 · 15:55 · 17:55 · 19:55).
  Step 4 now: Kopřivnice 17:15 for 17:15: ok; Frenštát u škol 15:55 for 15:55 16:55: ok. Two buses as published.
- **(e) Knots** (model passing time, min from the nearest real time of trips that run the whole leg): Kopřivnice → Kopřivnice, železniční stanice 17:19 (245*); Kopřivnice → Frenštát p.Radh., u škol 17:44 (246*); Frenštát u škol → Kopřivnice, autobusové nádraží 16:23 (2); Frenštát u škol → Kopřivnice, železniční stanice 16:19 (2).
- **(f) Off the pattern 12–20 h** (min off): Kopřivnice 12:00 (45), 13:10 (5), 14:10 (55); Frenštát u škol 12:00 (5), 13:00 (55), 14:25 (30), 16:55 (60).
- **(g) Need:** 2 → 2 (waits Kopřivnice 51; Frenštát station 0; Frenštát u škol 122).

## 655 Frenštát pod Radhoštěm-Trojanovice

- **(a) Core points:** Frenštát p.Radh., u škol · Trojanovice, restaurace Ráztoka. Model hours 15:30–17:30.
- **(b) Afternoon (12–20 h, model hours in bold, read at the terminal):** Frenštát u škol → Trojanovice 12:18, 13:08, 13:48, 14:18, 14:50, 15:25, **16:05**, **16:58**, **17:18**, 19:18; Trojanovice → Frenštát u škol 12:35, 13:25, 14:00, 14:35, 15:05, **15:40**, **16:20**, **17:10**, 17:30, 19:30.
- **(c) Step 4.** Published every 30: Frenštát u škol slots 15:48(-) 16:18(-) 16:48(-) 17:18 for real 16:05 16:58 17:18: EMPTY; Trojanovice slots 15:35(-) 16:05(-) 16:35(-) 17:05(-) for real 15:40 16:20 17:10: EMPTY. published every 30 (u škol :18 / :48, Ráztoka :05 / :35): 3 of 4 and 4 of 4 slots empty, FAIL. Every 120 three slots each way: passes, all exact, three buses. Every 180 three slots: passes, one more exact, three buses, but 30–47 min off at 12:18, 14:50, 15:25.
- **(d) Simutrans line 655:** Frenštát p.Radh., u škol → Trojanovice: every 120, Offset 17 (real 13:18 · 15:18 · 17:18 · 19:18), Also at 64 (real 12:05 · 14:05 · 16:05 · 18:05), 114 (real 12:55 · 14:55 · 16:55 · 18:55); Trojanovice, restaurace Ráztoka → Frenštát u škol: every 120, Offset 9 (real 13:10 · 15:10 · 17:10 · 19:10), Also at 39 (real 13:40 · 15:40 · 17:40 · 19:40), 79 (real 12:20 · 14:20 · 16:20 · 18:20).
  Step 4 now: Frenštát u škol 16:05 16:55 17:18 for 16:05 16:58 17:18: ok; Trojanovice 15:40 16:20 17:10 for 15:40 16:20 17:10: ok. Every 120 with u škol 16:58 → 16:55 (3 min) works with two buses. Each real round is another bus (63-1207, 63-1347, 63-1203, 63-1011). Need 1 → 2.
- **(e) Knots** (model passing time, min from the nearest real time of trips that run the whole leg): Frenštát u škol → Trojanovice, restaurace Ráztoka 16:17 (0), 17:07 (3), 17:30 (0); Trojanovice → Frenštát p.Radh., u škol 15:52 (0), 16:32 (0), 17:22 (0).
- **(f) Off the pattern 12–20 h** (min off): Frenštát u škol 12:18 (13), 13:08 (10), 13:48 (17), 14:18 (13), 14:50 (5), 15:25 (7); Trojanovice 12:35 (15), 13:25 (15), 14:00 (20), 14:35 (15), 15:05 (5), 17:30 (10), 19:30 (10).
- **(g) Need:** 1 → 2 (waits Frenštát u škol 23, 116, 13; Trojanovice 3, 3, 10).

## 656 Frenštát pod Radhoštěm-Trojanovice,Bystré

- **(a) Core points:** Frenštát p.Radh., u škol · Trojanovice, Bystré, Maralův kopec. Model hours 13:10–15:10.
- **(b) Afternoon (12–20 h, model hours in bold, read at the terminal):** Frenštát u škol → Trojanovice **13:15**, **13:55**, **14:50**, 15:50, 16:50, 18:15; Trojanovice → Frenštát u škol **13:35**, **14:10**, **15:05**, 16:05, 17:05, 18:35.
- **(c) Step 4.** Published every 60: Frenštát u škol slots 13:50(-) 14:50 for real 13:15 13:55 14:50: EMPTY; Trojanovice slots 14:05(-) 15:05 for real 13:35 14:10 15:05: EMPTY. published every 60 (u škol :50, Bystré :05): 13:50 and 14:05 empty (the window 13:10–15:10 holds 63-1204's two extra rounds), FAIL. Every 120 three slots each way: passes, 8 exact, two buses. Every 180 three slots: passes, 7 exact, one bus.
- **(d) Simutrans line 656:** Frenštát p.Radh., u škol → Trojanovice: every 180, Offset 14 (real 13:15 · 16:15 · 19:15), Also at 54 (real 13:55 · 16:55 · 19:55), 108 (real 14:49 · 17:49); Trojanovice, Bystré, Maralův kopec → Frenštát u škol: every 180, Offset 32 (real 13:33 · 16:33 · 19:33), Also at 70 (real 14:11 · 17:11), 124 (real 12:05 · 15:05 · 18:05).
  Step 4 now: Frenštát u škol 13:15 13:55 14:49 for 13:15 13:55 14:50: ok; Trojanovice 13:33 14:11 15:05 for 13:35 14:10 15:05: ok. One exact minute is not worth a bus. u škol 14:50 → 14:49, Bystré 13:35 → 13:33 and 14:10 → 14:11 keep one bus with 3-min turns at the model's running times.
- **(e) Knots** (model passing time, min from the nearest real time of trips that run the whole leg): Frenštát u škol → Trojanovice, Bystré, Maralův kopec 13:27 (8), 14:07 (1), 15:01 (2); Trojanovice → Frenštát p.Radh., u škol 13:46 (2), 14:24 (1), 15:18 (0).
- **(f) Off the pattern 12–20 h** (min off): Frenštát u škol 15:50 (25), 16:50 (5), 18:15 (26); Trojanovice 16:05 (28), 17:05 (6), 18:35 (30).
- **(g) Need:** 1 → 1 (waits Frenštát u škol 51, 3, 19; Trojanovice 3, 5, 3).

## 657 Kunčice Frenštát pod Radhoštěm-Tichá-Kunčice pod Ondřejníkem-Frýdlant nad Ostravicí

- **(a) Core points:** Frenštát p.Radh., u škol · Frýdlant n.Ost., zahradnictví. Model hours 13:00–15:00.
- **(b) Afternoon (12–20 h, model hours in bold, read at the terminal):** Frenštát u škol → Kunčice p.Ondřejníkem 12:20, **14:00**, 16:45, 17:45, 19:02; Kunčice p.Ondřejníkem → Frenštát u škol 12:46, **13:06**, 18:06.
- **(c) Step 4.** Published every 180: Frenštát u škol slots 13:45(-) for real 14:00: EMPTY; Kunčice p.Ondřejníkem slots none for real 13:06: ok. published every 180 (u škol 13:45, Kunčice 12:06 / 15:06): u škol 13:45 15 off the real 14:00, FAIL. Every 120 and 160: pass, 4 exact each.
- **(d) Simutrans line 657 Kunčice:** Frenštát p.Radh., u škol → Kunčice p.Ondřejníkem: every 120, Offset 59 (real 12:00 · 14:00 · 16:00 · 18:00); Kunčice p.Ondřejníkem, železniční stanice → Frenštát u škol: every 120, Offset 5 (real 13:06 · 15:06 · 17:06 · 19:06).
  Step 4 now: Frenštát u škol 14:00 for 14:00: ok; Kunčice p.Ondřejníkem 13:06 for 13:06: ok. Plain 120, one bus.
- **(e) Knots** (model passing time, min from the nearest real time of trips that run the whole leg): Kunčice p.Ondřejníkem → Frenštát p.Radh., u škol 13:26 (0).
- **(f) Off the pattern 12–20 h** (min off): Frenštát u škol 12:20 (20), 16:45 (45), 17:45 (15), 19:02 (58); Kunčice p.Ondřejníkem 12:46 (20), 18:06 (60).
- **(g) Need:** 1 → 1 (waits Frenštát u škol 27; Kunčice p.Ondřejníkem 48).

## 690 Nový Jičín-Rybí-Štramberk-Kopřivnice

- **(a) Core points:** Nový Jičín, autobusové nádraží · Kopřivnice, autobusové nádraží · Kopřivnice, Tymphany. Model hours 15:30–17:30.
- **(b) Afternoon (12–20 h, model hours in bold, read at the terminal):** Nový Jičín → Tymphany 13:45, **15:55**, 17:40, 18:40, 19:40; Tymphany → Nový Jičín 12:05, 14:15, 14:30, **15:40**, **16:40**, 17:30, 18:35, 19:55.
- **(c) Step 4.** Published every 60: Nový Jičín slots 15:40(-) 16:40(-) for real 15:55: EMPTY; Tymphany slots 15:30(-) 16:30(-) for real 15:40 16:40: EMPTY. published every 60 (NJ :40, Tymphany :30): all slots empty (real NJ 15:55; Tymphany 15:40, 16:40), FAIL. Every 96: passes, exact in the window both ways, two buses with 3-min turns. Every 144: passes, one more exact (8:40, 20:40), one bus, NJ 3 min off. Every 180: two buses.
- **(d) Simutrans line 690:** Nový Jičín, autobusové nádraží → Tymphany: every 96, Offset 29 (real 12:42 · 14:18 · 15:54 · 17:30 · 19:06); Kopřivnice, Tymphany → Nový Jičín: every 96, Offset 75 (real 13:28 · 15:04 · 16:40 · 18:16 · 19:52); passes Kopřivnice, autobusové nádraží at 12:02 · 13:38 · 15:14 · 16:50 · 18:26.
  Step 4 now: Nový Jičín 15:54 for 15:55: ok; Tymphany 16:40 for 15:40 16:40: ok. Every 96 with NJ 15:55 → 15:54 works with one bus. The knot is Kopřivnice bus station: the return is timed at Tymphany so the bus passes it at 16:50.
- **(e) Knots** (model passing time, min from the nearest real time of trips that run the whole leg): Nový Jičín → Kopřivnice, autobusové nádraží 16:28 (106*); Nový Jičín → Kopřivnice, Tymphany 16:37 (106*); Tymphany → Nový Jičín, autobusové nádraží 17:24 (50*).
- **(f) Off the pattern 12–20 h** (min off): Nový Jičín 13:45 (33), 17:40 (10), 18:40 (26), 19:40 (34); Tymphany 12:05 (13), 14:15 (47), 14:30 (34), 15:40 (36), 17:30 (46), 18:35 (19).
- **(g) Need:** 2 → 1 (waits Nový Jičín 6; Tymphany 3).

## 698 Nový Jičín-Rybí-Kopřivnice

- **(a) Core points:** Nový Jičín, autobusové nádraží · Kopřivnice, autobusové nádraží. Model hours 13:10–15:10.
- **(b) Afternoon (12–20 h, model hours in bold, read at the terminal):** Nový Jičín → Kopřivnice 12:10, 12:40, **13:10**, **13:30**, **14:20**, **14:45**, 15:10, 15:30, 16:40; Kopřivnice → Nový Jičín 12:55, **13:15**, **13:35**, **13:55**, **14:15**, **14:35**, 15:15, 16:15.
- **(c) Step 4.** Published every 60: Nový Jičín slots 13:10 13:30 14:10(-) 14:30(-) for real 13:10 13:30 14:20 14:45: EMPTY; Kopřivnice slots 13:15 13:35 14:15 14:35 for real 13:15 13:35 13:55 14:15 14:35: ok. hand-set every 60 (NJ :10 / :30, Kopřivnice :15 / :35): NJ 14:10, 14:30 empty (real 14:20, 14:45), FAIL. Every 120 four slots each way: passes, all exact (NJ 4 / 4, Kopřivnice 4 / 5), 14 exact over the day, four buses.
- **(d) Simutrans line 698:** Nový Jičín, autobusové nádraží → Kopřivnice: every 120, Offset 9 (real 13:10 · 15:10 · 17:10 · 19:10), Also at 29 (real 13:30 · 15:30 · 17:30 · 19:30), 79 (real 12:20 · 14:20 · 16:20 · 18:20), 104 (real 12:45 · 14:45 · 16:45 · 18:45); Kopřivnice, autobusové nádraží → Nový Jičín: every 120, Offset 14 (real 13:15 · 15:15 · 17:15 · 19:15), Also at 34 (real 13:35 · 15:35 · 17:35 · 19:35), 74 (real 12:15 · 14:15 · 16:15 · 18:15), 94 (real 12:35 · 14:35 · 16:35 · 18:35).
  Step 4 now: Nový Jičín 13:10 13:30 14:20 14:45 for 13:10 13:30 14:20 14:45: ok; Kopřivnice 13:15 13:35 14:15 14:35 for 13:15 13:35 13:55 14:15 14:35: ok. Same four buses as published; the owner check is updated.
- **(e) Knots** (model passing time, min from the nearest real time of trips that run the whole leg): Nový Jičín → Kopřivnice, autobusové nádraží 13:40 (2), 14:00 (2), 14:50 (2), 15:15 (1); Kopřivnice → Nový Jičín, autobusové nádraží 13:47 (0), 14:07 (0), 14:47 (0), 15:07 (0).
- **(f) Off the pattern 12–20 h** (min off): Nový Jičín 12:10 (10), 12:40 (5), 16:40 (5); Kopřivnice 12:55 (20), 13:55 (20).
- **(g) Need:** 4 → 4 (waits Nový Jičín 38, 23, 23, 33; Kopřivnice 35, 25, 20, 35).

## 699 Nový Jičín-Příbor-Kopřivnice

- **(a) Core points:** Nový Jičín, autobusové nádraží · Kopřivnice, autobusové nádraží. Model hours 15:30–17:30.
- **(b) Afternoon (12–20 h, model hours in bold, read at the terminal):** Nový Jičín → Kopřivnice 12:55, 14:25, 15:10, **15:45**, **16:25**, 18:25; Kopřivnice → Nový Jičín 12:55, 13:25, 14:25, 15:25, **16:55**, 19:25.
- **(c) Step 4.** Published every 60: Nový Jičín slots 16:25 17:25(-) for real 15:45 16:25: EMPTY; Kopřivnice slots 16:25(-) 17:25(-) for real 16:55: EMPTY. published every 60 (NJ :25, Kopřivnice :25): NJ 17:25, Kopřivnice 16:25 / 17:25 empty, FAIL. Every 120 (NJ 16:25, Kopřivnice 16:55): passes, 8 exact over the day (14:25, 16:25, 18:25 …; 12:55, 16:55 …), two buses.
- **(d) Simutrans line 699:** Nový Jičín, autobusové nádraží → Kopřivnice: every 120, Offset 84 (real 12:25 · 14:25 · 16:25 · 18:25); Kopřivnice, autobusové nádraží → Nový Jičín: every 120, Offset 114 (real 12:55 · 14:55 · 16:55 · 18:55).
  Step 4 now: Nový Jičín 16:25 for 15:45 16:25: ok; Kopřivnice 16:55 for 16:55: ok. Most exact.
- **(e) Knots** (model passing time, min from the nearest real time of trips that run the whole leg): Nový Jičín → Kopřivnice, autobusové nádraží 17:08 (0); Kopřivnice → Nový Jičín, autobusové nádraží 17:39 (0).
- **(f) Off the pattern 12–20 h** (min off): Nový Jičín 12:55 (30), 15:10 (45), 15:45 (40); Kopřivnice 13:25 (30), 14:25 (30), 15:25 (30), 19:25 (30).
- **(g) Need:** 2 → 2 (waits Nový Jičín 45; Kopřivnice 107).

## Left as they are, judged by hand

- **635, Frenštát, u škol → Kopřivnice (FEWER, 2 slots for 4 real departures).** The Continental shift change sends four buses back to Kopřivnice in 14:05–15:55 against two out (14:18, 15:28); the extra ones work 634, 646 and 653 from Kopřivnice. No pattern with the same number of slots both ways passes (Frenštát would need four); timed at the Kopřivnice rate, 14:05 and 14:15 off, as the outstation rule does the other way round. The section above has its rows.
- **641, Ostrava, Dubina → Kopřivnice (FEWER, 2 slots for 4).** Unchanged (every 60, Kopřivnice :25, Dubina :00; now typed by hand). Kopřivnice is exactly hourly at :25 all day; the Tatra shift change brings 14:28 and 15:28 back from Ostrava-Hrabůvka besides the :00 trips, and those buses end at the Kopřivnice garage (63-1333, 63-1310) or go on (63-1403 to 638, 63-1340 to 699). 14:55 out (63-1330, a shift trip, on to 376) is off the pattern too. Every 120 with three slots each way passes both ways but needs four buses for shift extras every 2 h all day. Card note rewritten.
- **601–604, the 602 and 603 legs (EMPTY: the 17:10 slot).** 602 runs at :10 every hour 8:10–16:10 and 603 to Tesco at :10 (8:10–10:10, 15:10, 16:10); the model hours run to 17:30, so their 17:10 slots have no trip. The circuit is the one ARRIVA ran on 20 Oct (owner check); the audit's candidate, every 120, would halve every town line in it. Kept; the card says why and the sheet lists the slots under To check.

## Buses, roster and owner checks

- **Need by the pattern:** 108 → 108. Fewer: 287 2 → 1, 615 3 → 2, 667 2 → 1, 371 2 → 1, 690 2 → 1. More: 618 2 → 3, 625 1 → 2, 370 1 → 2, 646 2 → 3, 655 1 → 2.
- **Roster:** not rebuilt here. `config.keep_roster` = `data/published/roster_v5.json`, so the shared `04_roster.py` keeps each published bus on its Simutrans line wherever it is still seen on that line's trips; the orchestrator runs it, the render and the cross-sheet checks.
- **Owner checks (7):** the 601–604 circuit, 655 on this sheet and the Kopřivnice loop as before; 698 reworded (every 120, four slots each way, four buses); new: 618 (three slots each way and three buses, or every 72 with two), 620 Pohoř (every 180 with one bus, or every 120 with two slots each way and three), 370 (every 90 with two buses, or every 240 with one).
- **To check list:** 101 rows before, 42 now: 40 legs with a real departure more than 3 min off inside the model hours (the off-pattern trips above, mostly buses going home or on to another line) and the two 17:10 slots of 601–604.
- **Card artefacts (knot devs marked * above):** the builder compares a knot only with trips that run the whole leg. Where the modelled trip ends short (371's 16:55 turns at Hukvaldy, hotel; 690's 15:55 at Kopřivnice bus station; 653's Kopřivnice end) the nearest full-leg trip is far away. A leg whose slots fall outside the model hours (379, 619, 625 Tísek, 638, 679) is checked at its slot residue, so the card shows a night time (625 Tísek: 3:22). Neither is a fault of the pattern.

## Notes for the owner

- The window rule sets several intervals: where the model hours hold one departure each way (287, 667, 689, 988) only every 120 or longer passes, though the line runs about hourly earlier in the afternoon; the earlier trips are listed off the pattern.
- Lines with no trip in one direction during the model hours (379, 619, 625 Tísek, 638, 679) get an interval that puts that slot outside the model hours too, on a real trip; that is why they pass now.
- Rows moved by up to 3 min to save a bus (rule 6) could be typed on the exact minutes for one more bus each: 286 (3 buses), 371 (2), 374 (3), 622 (2), 655 (3), 656 (3), 665 (2), 690 (2), 696 (4, or 5 with 3-min turns).

- **Fold rule** (`kb/rules/fork-schedule.md`: a row whose slots are evenly spaced is written at the shorter interval): three entries here are every 120 with two slots 60 min apart, which is every 60 with one offset. The builder has one interval per Simutrans line, so the data and the card show every 120 + Also at; in the game they can be typed as every 60: 373 Dubina Offset 19 (real :20), 670 Dubina Offset 19 (real :20), 376 Rychaltice Offset 2 (real :03). 373 Dubina and 376 Rychaltice are then the same as published (v5).

