> 3 Nov 2026: re-checked for branches read by trip ends instead of where trips pass (the 381 Zásmuky case). Where `branch-check-2026-11-03.md` or `branch-review-2026-11-03.md` differs from this file, the 3 Nov files stand (the review over the check).

# Method check: PID Mladoboleslavsko (okres Mladá Boleslav), 1–2 Nov 2026

Designed line by line with `../../../bus-schedule-method.md` (v4) and the pid-regional `DESIGN_BRIEF.md` (incl. "Learned on the pilot"), against the whole-day readings `data/derived/reading/<L>.txt` (PID GTFS of 1 Nov 2026, service day Mon 2 Nov 2026, a school day), with the owner’s lessons (`kb/lessons.md`) as the yardstick. The pilot review (Rakovnicko) was read for what a reviewer flags.

- **Step 4 test** per timed leg in its Simutrans line’s model window (anchor − 30 to + 90): window slots = real departures ± 1, and at least 80 % of window slots with a real departure within 3 min. Then most exact over the day, then the simplest. The tables below are generated from `schedule.json` after the final run (`run_oblast.py mladoboleslavsko`).
- **Typed values** are (real − 61) mod every (every terminus is a loop); the builder computes them and the tables show both.
- **Needs** are the builder’s, from the pattern (minimum wait 3 min, less where the real timetable turns closer; `lay: 0` only on the real 0-minute turns of 431 Stará Lysá and 733).
- Columns: *slots* = the slots 12:00–21:00 (minutes for intervals dividing 60); *window* = window slots / real departures in the window (✗ = slot with no real departure within 3 min); *on the minute* = exact / within 1 / within 3 of the trips the leg stands for over the day (5–23); *off* = its trips 10–21 h more than 3 min off a slot (with the deviation).

**Result:** 48 lines: 45 in `lines` (55 Simutrans lines, 93 buses), 3 in `unmodelled` (727, 769 carried by 699, XS35 automatic). Step 4: 112 timed legs, 108 pass; the 4 that fail are the approximations on the owner checks (722, 737 ×3). Branch audit: one flag explained (712). Path audit: 7 flags, all 442 and explained: the 14:31 slot trip of 442 and six slot trips of 442 Dražice run via Benátky nad Jizerou, Husovo náměstí and Vaněčkova (both stops on 431 and 768), while the game lines take the direct road (442 Dražice on the short road by Dražická, so the real 1–5 min turns hold with one bus). Coverage: 673 afternoon stops, 3 uncovered, all three coverage exceptions on one owner check.

## Changed on 2 Nov 2026 (after the independent review, `review-2026-11-01.md`)

- **735:** two lines (735 every 120 and 735 Brodek every 480, 2 buses) → one circuit every 240 with the Brodek trip as its last leg, 1 bus (typed 64 / 123 / 189).
- **767:** 767 Krpy deleted (the Bezno – Krpy shuttle runs only over 767’s own stops; its six trips are listed), anchor 14:30 by hand; its owner check removed; −1 bus.
- **775:** owner check removed (the two-slot row is the inbound rate; Step 4 rule 3 and the 290 rule decide); the row is unchanged.
- **737:** wording only: the deviations are 5–30 min, not up to 15 (note and owner check). **720:** the why names the Semily 17:50 / 19:50 repeats as without a real trip.
- **Sheet notes:** nine every-480 lines (735 Brodek gone); live-map pairings added: 737 → 775, 467 → 699 and 467 → 724 at Mladá Boleslav, 713 ↔ 718 at Sobotka.
- Totals 57 → 55 Simutrans lines, 95 → 93 buses; owner checks 5 → 3. Every other line is unchanged.

## Line by line

### 315  Praha,Černý Most - Benátky nad Jizerou - Mladá Boleslav - Mnichovo Hradiště

- **Core points:** Mnichovo Hradiště, dopravní terminál | Mladá Boleslav, autobusové stanoviště | Benátky nad Jizerou, autobusové stanoviště | Praha, Černý Most. Anchor 16:00 (set by hand).
- **Reading and choice:** Whole day: Praha, Černý Most → Mnichovo Hradiště every 30 at :10 / :40 from 12:10 to 17:40 (then 18:10, 18:40 to Mladá Boleslav only); Mnichovo Hradiště → Praha :28 / :53–:58 until 14:28, :03 / :33 from 15:03 to 17:33 (17:03 to Tuřice, 18:03 to Benátky). At Mladá Boleslav towards Praha the trips pass :10 / :40 all day; extra Mladá Boleslav starts 12:10, 13:55, 14:25. The computed anchor (13:50) sits on the school-time short trips Mladá Boleslav → Mnichovo Hradiště 13:35, 14:05, 14:35 and Mladá Boleslav → Praha 13:55, 14:25 (stops all on the line), so the anchor is 16:00 by hand (v4 rule, as 282 / 555). Chosen: every 30, Praha :10 / :40, Mnichovo Hradiště :03 / :33 (core_to Tuřice so the 17:03 Tuřice trip counts). Need 8 with at least 3 min at Praha (arrivals :10 / :40 = departures; 17 of 31 departures follow a 315 arrival): with a real 0-minute turn it would be 7, left for the live map.

| Simutrans line | Every | Entry | Slots (real) | Typed | Running time | Window | On the minute | Off the pattern | Need |
|---|---|---|---|---|---|---|---|---|---|
| 315 | 30 | Praha, Černý Most → Mnichovo Hradiště, dopravní terminál | :10 :40 | 9 | 95 | 15:40, 16:10, 16:40, 17:10 / 15:40, 16:10, 16:40, 17:10 | 18 / 18 / 18 of 22 | 20:15 (5) | 8 |
|  |  | Mnichovo Hradiště, dopravní terminál → Praha, Černý Most | :03 :33 | 2 | 97 | 15:33, 16:03, 16:33, 17:03 / 15:33, 16:03, 16:33, 17:03 | 10 / 10 / 11 of 25 | 11:58 (5), 12:28 (5), 12:53 (10), 13:28 (5), 13:55 (8), 14:28 (5), 18:38 (5), 19:38 (5), 20:48 (15) |  |

*Why on the card:* **315:** Praha, Černý Most :10 / :40 → Mnichovo Hradiště, dopravní terminál (95 min); dopravní terminál :03 / :33 → Praha (97 min), the 17:03 to Tuřice run on to Černý Most.

### 345  Praha,Černý Most - Mladá Boleslav - Hodkovice nad Mohelkou - Liberec

- **Core points:** Praha, Černý Most | Mladá Boleslav, autobusové stanoviště | Mnichovo Hradiště, náměstí | Liberec, autobusové nádraží. Anchor 16:00 (set by hand).
- **Reading and choice:** Whole day: Praha → Liberec :30 (12:30, 14:30–18:30, 20:30; 13:30 replaced by 13:45 to Mladá Boleslav), Liberec → Praha :40 (11:40, 13:40–18:40; 12:40 replaced by Mnichovo Hradiště, náměstí 13:23, which passes náměstí at the same :23 as the Liberec trips). Shorts Mnichovo Hradiště ↔ Mladá Boleslav 13:43, 13:53, 14:30 and Praha 12:45, 13:45, 21:30 → Mladá Boleslav, all over 345’s stops. Anchor 16:00 by hand (the busier 13:40–15:40 is those shorts). Each direction takes its own real path (towards Liberec via Paceřice, Rohanka and Žďárek, Hvězda; towards Praha via Paceřice, Husa), so both sets of own stops are covered. Need 5 (60 min at Praha; 4 with a 0-minute turn).

| Simutrans line | Every | Entry | Slots (real) | Typed | Running time | Window | On the minute | Off the pattern | Need |
|---|---|---|---|---|---|---|---|---|---|
| 345 | 60 | Praha, Černý Most → Liberec, autobusové nádraží | :30 | 29 | 115 | 15:30, 16:30 / 15:30, 16:30 | 7 / 7 / 7 of 11 | 10:35 (5), 11:35 (5) | 5 |
|  |  | Liberec, autobusové nádraží → Praha, Černý Most | :40 | 39 | 110 | 15:40, 16:40 / 15:40, 16:40 | 10 / 10 / 12 of 12 | – |  |

*Why on the card:* **345:** Praha :30 → Liberec via Paceřice, Rohanka and Žďárek, Hvězda (115 min); Liberec :40 → Praha via Paceřice, Husa, hlavní silnice (110 min), each direction by its own real path.

### 403  Praha,Černý Most - Dobrovice - Dolní Bousov

- **Core points:** Praha, Černý Most | Benátky nad Jizerou, autobusové stanoviště | Dobrovice, autobusové stanoviště | Rabakov | Dolní Bousov, náměstí. Anchor 16:00 (computed).
- **Reading and choice:** Whole day: Dobrovice → Praha 4:53, 7:10, 12:55, 15:30; Dolní Bousov 5:10 → Praha; Praha → Dobrovice 5:53, 11:40, 14:30; Praha 16:30 → Dolní Bousov, 18:30 → Žerčice; Dolní Bousov – Rabakov – Prodašice shorts. Reading 403 as unmodelled (Step 8) left eight okres stops uncovered (Semčice, Žerčice, pod Kobylnicí, Ledce, Ujkovice, Ujkovice, křižovatka, Prodašice, Dobrovice, Úherce, Brodce, Cukrovarská): among this sheet’s lines the 16:30 is their only afternoon service (Prodašice also has 463 of another oblast). So 403 runs every 480 on the real pair Praha 16:30 → Dolní Bousov / Dolní Bousov 5:10 → Praha (one bus: 105 + 175 + 106 + 94 = 480). The one-bus Dobrovice round (14:30 / 15:30, 3-min turn) and the 18:30 run over stops of 315 and 775 and are listed (Step 8).

| Simutrans line | Every | Entry | Slots (real) | Typed | Running time | Window | On the minute | Off the pattern | Need |
|---|---|---|---|---|---|---|---|---|---|
| 403 | 480 | Praha, Černý Most → Dolní Bousov, náměstí | 16:30 | 449 | 105 | 16:30 / 16:30 | 1 / 1 / 1 of 1 | – | 1 |
|  |  | Dolní Bousov, náměstí → Praha, Černý Most | 13:10 | 249 | 106 | none / none | 1 / 1 / 1 of 1 | – |  |

*Why on the card:* **403:** Praha 16:30 → Dolní Bousov via Benátky, Luštěnice, Dobrovice, Semčice and Rabakov (105 min); Dolní Bousov 5:10 → Praha (106 min), the real morning trip, which repeats at 13:10 and 21:10.

### 405  Špindlerův Mlýn - Vrchlabí - Jilemnice - Nová Paka - Jičín - Mladá Boleslav - Praha

- **Core points:** Praha, Černý Most | Mladá Boleslav, autobusové stanoviště | Sobotka, náměstí | Horka u St.Paky, autobusové stanoviště | Vrchlabí, autobusové stanoviště | Špindlerův Mlýn, autobusové stanoviště. Anchor 16:00 (computed).
- **Reading and choice:** Whole day: Praha :00 odd hours 9:00–17:00 (+ 7:05) to Špindlerův Mlýn, 14:35 and 19:00 to Vrchlabí; Špindlerův Mlýn :00 even hours 10:00–18:00 (13:55), plus Vrchlabí – Špindlerův Mlýn and Vrchlabí – Horka / Nová Paka shorts. Every 120 both ways, exact (5 of 6 / 5 of 7). Three kinds of stops are on one trip only in the afternoon: Vrchlabí, pivovar and nemocnice (the 11:00 from Praha), Jilemnice, Vejrychovsko and Studenec, Rovnáčov (the 18:00 from Špindlerův Mlýn), Dolní Branná, pošta and Studenec, Zálesní Lhota, křižovatka (the 14:35 to Vrchlabí, which skips Jilemnice). The first two are put on the main line’s paths (stops_via; the 575 precedent: no extra bus, named in the why); the 14:35 path cannot carry the main line (it skips Jilemnice), so 405 Vrchlabí every 480 on the real 14:35 with an empty return (one bus; a timed return on the 5:30 Vrchlabí → Praha would need 2 buses on 480). Need 405: 4 (120 min at Praha, the arrival minute is the departure minute; 3 with a 0-minute turn).

| Simutrans line | Every | Entry | Slots (real) | Typed | Running time | Window | On the minute | Off the pattern | Need |
|---|---|---|---|---|---|---|---|---|---|
| 405 | 120 | Praha, Černý Most → Špindlerův Mlýn, autobusové stanoviště | 13:00, 15:00, 17:00, 19:00 | 119 | 177 | 17:00 / 17:00 | 5 / 5 / 5 of 6 | – | 4 |
|  |  | Špindlerův Mlýn, autobusové stanoviště → Praha, Černý Most | 12:00, 14:00, 16:00, 18:00, 20:00 | 59 | 180 | 16:00 / 16:00 | 5 / 5 / 5 of 7 | 13:55 (5) |  |
| 405 Vrchlabí | 480 | Praha, Černý Most → Vrchlabí, autobusové stanoviště | 14:35 | 334 | 136 | none / none | 1 / 1 / 1 of 1 | – | 1 |
|  |  | Vrchlabí, autobusové stanoviště → Praha, Černý Most | untimed (empty return) | 0 | 150 | – | – | – |  |

*Why on the card:* **405:** Praha :00 odd hours → Špindlerův Mlýn by the 11:00 trip’s path through Vrchlabí, pivovar and nemocnice (177 min); Špindlerův Mlýn :00 even hours → Praha by the 18:00 trip’s path through Jilemnice, Vejrychovsko and Studenec, Rovnáčov (180 min). Both detours are the only afternoon service of those four stops. **405 Vrchlabí:** Praha 14:35 → Vrchlabí, autobusové stanoviště via Horka, Studenec, Zálesní Lhota and Dolní Branná (136 min), the real trip; empty return to Praha.

### 412  Praha,Černý Most - Mladá Boleslav - Jičín

- **Core points:** Praha, Černý Most | Mladá Boleslav, autobusové stanoviště | Sobotka, náměstí | Jičín, autobusové stanoviště. Anchor 16:00 (set by hand).
- **Reading and choice:** Whole day: Praha → Jičín :55 odd hours 7:55–13:55, then 16:00, 18:00, 20:00 (even :00); Jičín → Praha :35 even hours 10:35–16:35, 18:35 to Sobotka, 20:35 to Mladá Boleslav; Praha ↔ Mladá Boleslav shorts (13:30, 14:45, 15:45, 19:30 out; 14:30, 16:30 back). The computed anchor 14:00 put the Praha slot at 14:00 against the real 13:55 (5 min, Step 4 fail); its busy hours are the shorts, so 16:00 by hand: Praha 16:00 and Jičín 16:35 exact. Every 120 (the real headway; not stretched to 240, Opavsko rule). Need 3 (waits 115 at Praha and 70 at Jičín follow from the real minutes).

| Simutrans line | Every | Entry | Slots (real) | Typed | Running time | Window | On the minute | Off the pattern | Need |
|---|---|---|---|---|---|---|---|---|---|
| 412 | 120 | Praha, Černý Most → Jičín, autobusové stanoviště | 12:00, 14:00, 16:00, 18:00, 20:00 | 59 | 85 | 16:00 / 16:00 | 3 / 3 / 3 of 8 | 11:55 (5), 13:55 (5) | 3 |
|  |  | Jičín, autobusové stanoviště → Praha, Černý Most | 12:35, 14:35, 16:35, 18:35, 20:35 | 94 | 90 | 16:35 / 16:35 | 5 / 5 / 5 of 7 | – |  |

*Why on the card:* **412:** Praha :00 even hours → Jičín (85 min); Jičín :35 even hours → Praha (90 min), 18:35 runs only to Sobotka in reality.

### 427  Mimoň - Ralsko - Mnichovo Hradiště - Mladá Boleslav

- **Core points:** Mnichovo Hradiště, dopravní terminál | Ralsko, Kuřívody | Mimoň, autobusové stanoviště | Mimoň, Žitavská. Anchor 15:30 (set by hand).
- **Reading and choice:** Whole day: Mnichovo Hradiště → Mimoň 4:20, 5:28, 11:35, 13:40, 15:25, 17:45, 18:40 (to the autobusové stanoviště), Mladá Boleslav 6:25, 8:45, 14:30, 22:25; Mimoň → Mnichovo Hradiště 4:35, 5:25, 10:29, 14:32 (from the autobusové stanoviště), 15:35, 16:35, 17:50, and → Mladá Boleslav 4:15, 6:22, 12:15, 20:20; Kuřívody shorts 7:38 / 8:43, 16:20 / 17:41. No hourly or two-hourly minute holds both sides at the 16:00 window (Mnichovo Hradiště has no departure 15:30–17:30 but the Kuřívody short). The one bus that runs the core in the afternoon is Mimoň 14:32 → 15:20 / 15:25 → 16:30 / 16:35 → 17:20 (3–5 min turns); window 15:00–17:00 by hand on that round. Every 120, Mnichovo Hradiště 15:25 and Mimoň 16:35 exact; Mimoň 15:35 is the second window departure (±1). The out leg takes the 15:25’s real path (round Horní Rokytá and Hvězdov), the way back the 17:50’s (via the railway station): those stops have no other service. Rejected: every 60 (Mnichovo Hradiště :25 has no 16:25 / 17:25 trip).

| Simutrans line | Every | Entry | Slots (real) | Typed | Running time | Window | On the minute | Off the pattern | Need |
|---|---|---|---|---|---|---|---|---|---|
| 427 | 120 | Mnichovo Hradiště, dopravní terminál → Mimoň, Žitavská | 13:25, 15:25, 17:25, 19:25 | 24 | 65 | 15:25 / 15:25 | 1 / 1 / 2 of 7 | 11:35 (10), 13:40 (15), 17:45 (20), 18:40 (45) | 1 |
|  |  | Mimoň, Žitavská → Mnichovo Hradiště, dopravní terminál | 12:35, 14:35, 16:35, 18:35, 20:35 | 94 | 47 | 16:35 / 15:35, 16:35 | 1 / 1 / 1 of 5 | 10:29 (6), 15:35 (60), 17:50 (45) |  |

*Why on the card:* **427:** Mnichovo Hradiště 15:25 → Mimoň, Žitavská by its real path round Horní Rokytá and Ralsko, Ploužnice, školka and Hvězdov (65 min); Mimoň, Žitavská 16:35 → Mnichovo Hradiště via Mimoň, železniční stanice, the 17:50 trip’s path (47 min). Those detours are the only afternoon service of Horní Rokytá, otočka, Hvězdov and the station.

### 431  Skalsko - Benátky nad Jizerou - Lysá nad Labem

- **Core points:** Lysá nad Labem, železniční stanice | Předměřice nad Jizerou, u kostela | Benátky nad Jizerou, Husovo náměstí | Boreč, Žebice | Skalsko, náves. Anchor 14:30 (set by hand).
- **Reading and choice:** Whole day: a school line with 34 trips on many paths. Through trips Lysá 4:43, 14:02 → Skalsko, 16:07, 18:02 → Boreč, Žebice; Skalsko 13:29, 15:35 (6:27 to Kochánky), Boreč 4:29, 12:29, 17:35 → Lysá or Předměřice; Lysá – Benátky, Předměřice – Benátky – Kochánky shorts; Lysá local trips (13:34 Byšičky loop, 15:11 to Stará Lysá via Sojovice, 15:50 back, 17:17 / 17:39 Kochánky). Window 14:00–16:00 by hand on the round Lysá 14:02 → Skalsko 15:24 / 15:35 → Lysá 16:55. Every 120 Lysá :02 even (core_to Boreč, Žebice; 16:07 is 5 min off), Skalsko :35 odd; need 2. 431 Stará Lysá: the Lysá school bus (13:34 → Byšičky → 13:46, 15:11 → Čihadla → 15:50), every 480 as one circuit with two 0-minute turns, one bus; it is the only service of Sojovice (okres Mladá Boleslav, 1 km from Skorkov, which has no other line either) and of Lysá nad Labem, Byšičky and Ke Karlovu (okres Nymburk). The Kochánky / Předměřice / Benátky stops are on 431’s main path.

| Simutrans line | Every | Entry | Slots (real) | Typed | Running time | Window | On the minute | Off the pattern | Need |
|---|---|---|---|---|---|---|---|---|---|
| 431 | 120 | Lysá nad Labem, železniční stanice → Skalsko, náves | 12:02, 14:02, 16:02, 18:02, 20:02 | 61 | 82 | 14:02 / 14:02 | 2 / 2 / 2 of 3 | 16:07 (5) | 2 |
|  |  | Skalsko, náves → Lysá nad Labem, železniční stanice | 13:35, 15:35, 17:35, 19:35 | 34 | 83 | 15:35 / 15:35 | 1 / 1 / 1 of 2 | 13:29 (6) |  |
| 431 Stará Lysá | 480 | Lysá nad Labem, železniční stanice → Lysá nad Labem, Byšičky | 13:34 | 273 | 12 | none / 15:11 | 1 / 1 / 1 of 2 | 15:11 (97) | 1 |
|  |  | Lysá nad Labem, Byšičky → Lysá nad Labem, železniční stanice | 13:46 | 285 | 12 | none / none | 1 / 1 / 1 of 2 | – |  |
|  |  | Lysá nad Labem, železniční stanice → Stará Lysá, Čihadla | 15:11 | 370 | 39 | 15:11 / 15:11 | 1 / 1 / 1 of 1 | – |  |
|  |  | Stará Lysá, Čihadla → Lysá nad Labem, železniční stanice | 15:50 | 409 | 11 | 15:50 / 15:50 | 1 / 1 / 1 of 1 | – |  |

*Why on the card:* **431:** Lysá nad Labem, železniční stanice :02 even hours → Skalsko (82 min; 16:07 and 18:02 end at Boreč, Žebice); Skalsko :35 odd hours → Lysá (83 min). **431 Stará Lysá:** One bus as in reality, every 480: Lysá 13:34 → Byšičky → 13:46 → Lysá (0-minute turn as in the timetable), Lysá 15:11 → Sojovice → Stará Lysá, Čihadla (39 min) → 15:50 → Lysá (0-minute turn).

### 442  Mladá Boleslav - Benátky nad Jizerou - Lysá nad Labem

- **Core points:** Mladá Boleslav, autobusové stanoviště | Benátky nad Jizerou, autobusové stanoviště | Lysá nad Labem, železniční stanice | Benátky nad Jizerou, Dražice, dvůr. Anchor 14:50 (computed).
- **Reading and choice:** Whole day: Lysá → Mladá Boleslav :18 hourly 14:18–19:18 (16:18, 18:18 to Benátky; 12:06, 13:01 earlier), Mladá Boleslav → Lysá 12:23, 13:23, 14:31, 15:31, 16:36, 18:38, 20:53; Benátky – Dražice, dvůr shuttle about every 20–40 min all day on one bus (14 of 19 arrivals at Benátky followed by a 442 departure within 5 min). Computed anchor 14:50 (window 14:20–16:20), kept. 442 every 60: Mladá Boleslav :31 (14:31, 15:31 exact), Lysá :18 (core_to Benátky, so the 16:18 short counts); the way back takes the 17:18’s path round Dražice (stops_via závod): Benátky nad Jizerou, Dražice, závod has no other afternoon service. Need 3. 442 Dražice is kept as its own line although all its stops are also on 442’s way back round Dražice: it is not a sparse variant but an all-day shuttle (21–22 trips each way, one bus with 1–5 min turns, 14 of 19 arrivals at Benátky followed by a 442 departure), the review brief’s regular afternoon branch. Every 120 with five slots each way, all ten window departures exact, one bus (rt 6 / 8 on the short road by Dražická; the builder’s 9 / 10 min via Husovo náměstí needed 3 buses because the real 1-minute turns of the short-road trips then fail). Path audit: the 14:31 slot trip runs via Husovo náměstí and Vaněčkova (both on 431 and 768); named in the why.

| Simutrans line | Every | Entry | Slots (real) | Typed | Running time | Window | On the minute | Off the pattern | Need |
|---|---|---|---|---|---|---|---|---|---|
| 442 | 60 | Mladá Boleslav, autobusové stanoviště → Lysá nad Labem, železniční stanice | :31 | 30 | 58 | 14:31, 15:31 / 14:31, 15:31 | 4 / 4 / 5 of 12 | 10:58 (27), 12:23 (8), 13:23 (8), 16:36 (5), 18:38 (7), 20:53 (22) | 3 |
|  |  | Lysá nad Labem, železniční stanice → Mladá Boleslav, autobusové stanoviště | :18 | 17 | 59 | 15:18, 16:18 / 15:18, 16:18 | 6 / 6 / 7 of 14 | 10:36 (18), 12:06 (12), 13:01 (17) |  |
| 442 Dražice | 120 | Benátky nad Jizerou, autobusové stanoviště → Benátky nad Jizerou, Dražice, dvůr | 12:08, 12:38, 12:58, 13:15, 13:38, 14:08, 14:38, 14:58, 15:15, 15:38, 16:08, 16:38, 16:58, 17:15, 17:38, 18:08, 18:38, 18:58, 19:15, 19:38, 20:08, 20:38, 20:58 | 14, 37, 67, 97, 117 | 6 | 14:38, 14:58, 15:15, 15:38, 16:08 / 14:38, 14:58, 15:15, 15:38, 16:08 | 7 / 10 / 15 of 22 | 12:30 (8), 13:24 (9), 14:02 (6), 20:34 (4) | 1 |
|  |  | Benátky nad Jizerou, Dražice, dvůr → Benátky nad Jizerou, autobusové stanoviště | 12:26, 12:48, 13:05, 13:26, 13:55, 14:26, 14:48, 15:05, 15:26, 15:55, 16:26, 16:48, 17:05, 17:26, 17:55, 18:26, 18:48, 19:05, 19:26, 19:55, 20:26, 20:48 | 4, 25, 54, 85, 107 | 8 | 14:26, 14:48, 15:05, 15:26, 15:55 / 14:26, 14:48, 15:05, 15:26, 15:55 | 6 / 7 / 11 of 21 | 10:40 (8), 11:20 (6), 12:17 (9), 13:10 (5), 13:45 (10), 19:09 (4) |  |

*Why on the card:* **442:** Mladá Boleslav :31 → Lysá direct (58 min; 14:31 runs via Husovo náměstí, which 431 serves); Lysá :18 → Mladá Boleslav round Dražice, dvůr, Na Štěpničce and závod, the 17:18 trip’s path (59 min), závod’s only afternoon service; the 16:18 Benátky trip is run on to Mladá Boleslav. **442 Dražice:** Benátky nad Jizerou, autobusové stanoviště 14:38, 14:58, 15:15, 15:38, 16:08 → Dražice, dvůr (6 min, by Dražická); back 14:26, 14:48, 15:05, 15:26, 15:55 (8 min), every 120, one bus. The trips via Husovo náměstí and Vaněčkova (on 431 and 768) run the short way in the game.

### 467  Mladá Boleslav - Mělník - Roudnice nad Labem

- **Core points:** Mladá Boleslav, autobusové stanoviště | Mělník, autobusové nádraží | Roudnice nad Labem, u hřbitova. Anchor 16:00 (computed).
- **Reading and choice:** Whole day: Mladá Boleslav :30 hourly 5:30–18:30 (17:35), Roudnice nad Labem, u hřbitova :45 (4:45–17:45; 13:30, 14:30, 19:30 off by 15). Every 60, exact at both ends in the window. Terminus alias Roudnice nad Labem, ČSAD → u hřbitova (arriving buses pass u hřbitova at :06 and end at ČSAD at :07; departures leave u hřbitova), so ČSAD (Ústecký kraj) is on the line. Need 4.

| Simutrans line | Every | Entry | Slots (real) | Typed | Running time | Window | On the minute | Off the pattern | Need |
|---|---|---|---|---|---|---|---|---|---|
| 467 | 60 | Mladá Boleslav, autobusové stanoviště → Roudnice nad Labem, u hřbitova | :30 | 29 | 96 | 15:30, 16:30 / 15:30, 16:30 | 10 / 10 / 10 of 11 | 17:35 (5) | 4 |
|  |  | Roudnice nad Labem, u hřbitova → Mladá Boleslav, autobusové stanoviště | :45 | 44 | 100 | 15:45, 16:45 / 15:45, 16:45 | 7 / 7 / 7 of 11 | 13:30 (15), 14:30 (15), 19:30 (15) |  |

*Why on the card:* **467:** Mladá Boleslav :30 → Roudnice nad Labem, u hřbitova (96 min, on to ČSAD); u hřbitova :45 → Mladá Boleslav (100 min).

### 699  Mladá Boleslav - Chotětov - Bezno - Kadlín

- **Core points:** Mladá Boleslav, autobusové stanoviště | Chotětov | Bezno | Kadlín. Anchor 14:30 (computed).
- **Reading and choice:** Whole day: Mladá Boleslav → Chotětov :30 even hours 12:30–18:30 (+ morning); Chotětov → Mladá Boleslav 699 12:40, 14:45, 17:10 and 769 13:10, 15:10. Chain test: 2 of 3 769 departures at Chotětov follow a 699 arrival within 3 min (12:30 → 13:07 / 13:10; 14:30 → 15:07 / 15:10), so the 699 bus comes back as 769. Step 5b: one Simutrans line, out on 699, back on 699 + 769 (lines), every 120 at Chotětov :10 odd; the way back takes 769’s path (2 of 3 slot trips), which carries 769’s own stops. Saves a bus against a separate 769 line. Computed anchor 14:30, kept: Mladá Boleslav 14:30, Chotětov 15:10 exact. 699 Kadlín: Bezno 12:00, 15:00, 17:00 → Kadlín and back 12:28, 15:38, 17:38: every 120 Bezno :00 odd / Kadlín :38 odd, one bus; the Bezno – Velké Všelisy, Zamachy trips (14:05 / 14:43, 19:00) run over the same stops.

| Simutrans line | Every | Entry | Slots (real) | Typed | Running time | Window | On the minute | Off the pattern | Need |
|---|---|---|---|---|---|---|---|---|---|
| 699 | 120 | Mladá Boleslav, autobusové stanoviště → Chotětov | 12:30, 14:30, 16:30, 18:30, 20:30 | 89 | 37 | 14:30 / 14:30 | 4 / 4 / 4 of 8 | – | 1 |
|  |  | Chotětov → Mladá Boleslav, autobusové stanoviště | 13:10, 15:10, 17:10, 19:10 | 9 | 55 | 15:10 / 14:45, 15:10 | 3 / 3 / 3 of 8 | 12:40 (30), 14:45 (25), 20:40 (30) |  |
| 699 Kadlín | 120 | Bezno → Kadlín | 13:00, 15:00, 17:00, 19:00 | 119 | 19 | 15:00 / 15:00 | 2 / 2 / 2 of 4 | 12:00 (60) | 1 |
|  |  | Kadlín → Bezno | 13:38, 15:38, 17:38, 19:38 | 37 | 19 | 15:38 / 15:38 | 2 / 2 / 2 of 4 | 12:28 (50) |  |

*Why on the card:* **699:** Mladá Boleslav :30 even hours → Chotětov (37 min); Chotětov :10 odd hours → Mladá Boleslav by 769’s path through Doubravička and Strenice, Horecká (55 min; the 17:10 is a 699 trip by the direct road). **699 Kadlín:** Bezno :00 odd hours → Kadlín (19 min); Kadlín :38 odd hours → Bezno (19 min), one bus.

### 700  Harrachov - Tanvald - Železný Brod - Turnov - Praha

- **Core points:** Praha, Černý Most | Mladá Boleslav, autobusové stanoviště | Tanvald, Terminál u železniční stanice | Harrachov, autobusové nádraží. Anchor 16:00 (computed).
- **Reading and choice:** Whole day: Tanvald 6:00, 9:35 → Praha; Praha 15:15 → Harrachov, 17:45 → Tanvald. Seventeen stops of the Liberecký kraj (Tanvald, Desná, Kořenov, Harrachov…) have only the 15:15 in the afternoon, so 700 runs every 480 on it with an empty return (one bus; a return timed on Tanvald 6:00 or 9:35 needs 2 buses on 480). Prague :15 corridor: 720 13:15, 14:15, 700 15:15, 730 16:15, 720 17:15, 18:15 — the real hourly :15 towards Turnov.

| Simutrans line | Every | Entry | Slots (real) | Typed | Running time | Window | On the minute | Off the pattern | Need |
|---|---|---|---|---|---|---|---|---|---|
| 700 | 480 | Praha, Černý Most → Harrachov, autobusové nádraží | 15:15 | 374 | 150 | none / none | 1 / 1 / 1 of 1 | – | 1 |
|  |  | Harrachov, autobusové nádraží → Praha, Černý Most | untimed (empty return) | 0 | 150 | – | – | – |  |

*Why on the card:* **700:** Praha 15:15 → Harrachov (150 min), the real trip; empty return to Praha.

### 712  Mladá Boleslav - Katusice - Bělá pod Bezdězem

- **Core points:** Mladá Boleslav, autobusové stanoviště | Katusice | Březovice | Bělá pod Bezdězem, Atmos. Anchor 16:00 (computed).
- **Reading and choice:** Whole day: Bělá, Atmos → Mladá Boleslav :15 even hours (14:15, 16:15, 20:15; 6:20, 7:45 morning), Mladá Boleslav → Bělá / Březovice :35 even hours (10:35, 14:35 to Bezdědice, 16:35 to Březovice, 18:35; 12:00 to Březovice), Mladá Boleslav – Katusice shorts. Every 120, core_to Březovice so the 16:35 Březovice trip counts; branch audit [beyond]: the 14:35 slot trip goes on past Atmos to Bezdědice (732’s end), explained in the why. Need 2.

| Simutrans line | Every | Entry | Slots (real) | Typed | Running time | Window | On the minute | Off the pattern | Need |
|---|---|---|---|---|---|---|---|---|---|
| 712 | 120 | Mladá Boleslav, autobusové stanoviště → Bělá pod Bezdězem, Atmos | 12:35, 14:35, 16:35, 18:35, 20:35 | 94 | 59 | 16:35 / 16:35 | 5 / 5 / 5 of 8 | 12:00 (35) | 2 |
|  |  | Bělá pod Bezdězem, Atmos → Mladá Boleslav, autobusové stanoviště | 12:15, 14:15, 16:15, 18:15, 20:15 | 74 | 61 | 16:15 / 16:15 | 3 / 3 / 3 of 5 | – |  |

*Why on the card:* **712:** Mladá Boleslav :35 even hours → Bělá pod Bezdězem, Atmos (59 min; 16:35 ends at Březovice and 14:35 goes on to Bezdědice in reality); Bělá :15 even hours → Mladá Boleslav (61 min).

### 713  Mladá Boleslav - Obruby - Sobotka

- **Core points:** Mladá Boleslav, autobusové stanoviště | Dolní Bousov, Horní Bousov | Sobotka, náměstí. Anchor 16:00 (computed).
- **Reading and choice:** Whole day: Mladá Boleslav → Sobotka 6:10, 9:20, 11:20, 14:25, 16:20, 18:20; Sobotka 4:35, 6:50, 10:00, 12:35, 15:10, 17:00, 19:00 → Mladá Boleslav (4 of 6 Sobotka arrivals followed by a 713 departure within 5 min). Every 120 Mladá Boleslav :20 even / Sobotka :00 odd, both exact in the window, 2-minute turn as in reality, one bus.

| Simutrans line | Every | Entry | Slots (real) | Typed | Running time | Window | On the minute | Off the pattern | Need |
|---|---|---|---|---|---|---|---|---|---|
| 713 | 120 | Mladá Boleslav, autobusové stanoviště → Sobotka, náměstí | 12:20, 14:20, 16:20, 18:20, 20:20 | 79 | 38 | 16:20 / 16:20 | 2 / 2 / 2 of 6 | 11:20 (60), 14:25 (5) | 1 |
|  |  | Sobotka, náměstí → Mladá Boleslav, autobusové stanoviště | 13:00, 15:00, 17:00, 19:00 | 119 | 38 | 17:00 / 17:00 | 2 / 2 / 2 of 6 | 10:00 (60), 12:35 (25), 15:10 (10) |  |

*Why on the card:* **713:** Mladá Boleslav :20 even hours → Sobotka (38 min); Sobotka :00 odd hours → Mladá Boleslav (38 min), a 2-minute turn as in the timetable.

### 714  Mladá Boleslav - Kněžmost - Sobotka

- **Core points:** Mladá Boleslav, autobusové stanoviště | Kněžmost, náměstí | Kněžmost, Srbsko | Dobšín | Sobotka, škola. Anchor 16:00 (set by hand).
- **Reading and choice:** Whole day: Mladá Boleslav → Srbsko 5:50, 9:05, 11:35, 14:30, 17:05, 19:05 (Dobšín); Srbsko / Dobšín → Mladá Boleslav 4:42, 5:05, 6:47, 10:17, 12:37, 17:10 (Srbsko 17:17), 20:25; Mladá Boleslav 13:05 → Sobotka, škola, Sobotka, škola 14:10 → Kněžmost via Podkost; Mladá Boleslav ↔ Kněžmost, náměstí shuttles 13:35–16:02. The computed anchor 14:30 is the shuttles (stops on the line), so 16:00 by hand. The buses sleep at Srbsko and Dobšín (first trips start there), so the line runs at its inbound rate: one return 13–19 → 714 every 240, Mladá Boleslav 14:30 / Srbsko 17:17, both real, one bus; 17:05 and 19:05 are buses going home. An every-480 three-slot try left two of its slots with no real trip (SLOT WITHOUT A REAL TRIP) and was dropped. 714 Sobotka: a 3-leg circuit every 480 on the real 13:05 / 14:10 / Kněžmost 15:40, one bus (running times set to the slot trips’ own 61 and 48 min; the builder’s medians 68 / 42 mixed in the morning trips and cost a second bus); it is the only service of nine Libošovice and Sobotka stops (Královéhradecký kraj). No shared minute with 714 at Mladá Boleslav (13:05 / 14:30).

| Simutrans line | Every | Entry | Slots (real) | Typed | Running time | Window | On the minute | Off the pattern | Need |
|---|---|---|---|---|---|---|---|---|---|
| 714 | 240 | Mladá Boleslav, autobusové stanoviště → Kněžmost, Srbsko | 14:30, 18:30 | 89 | 40 | none / 17:05 | 1 / 1 / 1 of 7 | 11:35 (65), 17:05 (85), 19:05 (35) | 1 |
|  |  | Kněžmost, Srbsko → Mladá Boleslav, autobusové stanoviště | 13:17, 17:17 | 16 | 40 | 17:17 / 17:17 | 1 / 1 / 1 of 5 | 10:17 (60), 12:37 (40), 20:32 (45) |  |
| 714 Sobotka | 480 | Mladá Boleslav, autobusové stanoviště → Sobotka, škola | 13:05 | 244 | 61 | none / none | 1 / 1 / 1 of 2 | – | 1 |
|  |  | Sobotka, škola → Kněžmost, náměstí | 14:10 | 309 | 48 | none / none | 1 / 1 / 1 of 2 | – |  |
|  |  | Kněžmost, náměstí → Mladá Boleslav, autobusové stanoviště | 15:40 | 399 | 22 | 15:40 / 15:40 | 1 / 1 / 1 of 10 | 10:35 (175), 12:55 (165), 13:35 (125), 14:05 (95), 14:40 (60), 17:35 (115), 20:45 (175) |  |

*Why on the card:* **714:** Mladá Boleslav 14:30 → Kněžmost, Srbsko (40 min); Srbsko 17:17 → Mladá Boleslav (40 min; the trip starts at Dobšín 17:10). Both real, every 240. **714 Sobotka:** Mladá Boleslav 13:05 → Sobotka, škola via Branžež and Libošovice (61 min); Sobotka, škola 14:10 → Kněžmost, náměstí via Podkost, hrad Kost and Dobšín (48 min); Kněžmost 15:40 → Mladá Boleslav (22 min). All real, every 480, one bus.

### 715  Mladá Boleslav - Ptýrov - Mnichovo Hradiště - Žďár,Žehrov

- **Core points:** Mladá Boleslav, autobusové stanoviště | Bakov nad Jizerou, železniční zastávka | Mnichovo Hradiště, dopravní terminál | Žďár, Žehrov. Anchor 16:00 (computed).
- **Reading and choice:** Whole day: 36 trips in pieces: Bakov ↔ Žďár, Žehrov (Bakov 5:30, 8:40, 15:40, 17:35; Žehrov 16:28, 18:28), Mnichovo Hradiště ↔ Žehrov (6:35, 11:40, 16:45 out; 7:08, 9:33, 13:18, 15:38 back), Mnichovo Hradiště ↔ Bakov (6:09, 7:49, 9:49, 13:39, 15:09 out; 7:20, 10:40, 14:15 back), Mladá Boleslav trips (13:00 → Mnichovo Hradiště, 14:35 → Žehrov, 12:18 Žehrov → Mladá Boleslav). Two Simutrans lines on the two afternoon rounds that hold the line’s own stops (Ptýrov, Žďár, Nová Ves, Březina, Mnichovo Hradiště, Olšina / Dneboh): 715 Bakov :40 odd / Žehrov :28 even (3-min turn), 715 Mnichovo Hradiště :45 even / Žehrov :38 odd, one bus each, all window slots exact. The Mnichovo Hradiště – Bakov and Mladá Boleslav trips run over stops of these lines and of 315 (coverage clean) and are listed.

| Simutrans line | Every | Entry | Slots (real) | Typed | Running time | Window | On the minute | Off the pattern | Need |
|---|---|---|---|---|---|---|---|---|---|
| 715 | 120 | Bakov nad Jizerou, železniční zastávka → Žďár, Žehrov | 13:40, 15:40, 17:40, 19:40 | 39 | 45 | 15:40 / 15:40 | 1 / 1 / 1 of 4 | 17:35 (5) | 1 |
|  |  | Žďár, Žehrov → Bakov nad Jizerou, železniční zastávka | 12:28, 14:28, 16:28, 18:28, 20:28 | 87 | 46 | 16:28 / 16:28 | 2 / 2 / 2 of 2 | – |  |
| 715 Mnichovo Hradiště | 120 | Mnichovo Hradiště, dopravní terminál → Žďár, Žehrov | 12:45, 14:45, 16:45, 18:45, 20:45 | 104 | 30 | 16:45 / 16:45 | 1 / 1 / 1 of 3 | 11:40 (55) | 1 |
|  |  | Žďár, Žehrov → Mnichovo Hradiště, dopravní terminál | 13:38, 15:38, 17:38, 19:38 | 37 | 28 | 15:38 / 15:38 | 1 / 1 / 1 of 4 | 13:18 (20) |  |

*Why on the card:* **715:** Bakov nad Jizerou, železniční zastávka :40 odd hours → Žďár, Žehrov (45 min; 17:35 is 5 min off); Žehrov :28 even hours → Bakov (46 min), a 3-minute turn as in the timetable. **715 Mnichovo Hradiště:** Mnichovo Hradiště, dopravní terminál :45 even hours → Žďár, Žehrov (30 min); Žehrov :38 odd hours → Mnichovo Hradiště (28 min).

### 716  Boseň,Mužský - Mnichovo Hradiště,Sychrov - Boseň,Mužský

- **Core points:** Mnichovo Hradiště, dopravní terminál | Mnichovo Hradiště, Sychrov | Boseň, Mužský. Anchor 15:30 (set by hand).
- **Reading and choice:** Whole day: Mnichovo Hradiště – Sychrov loops (5:00, 10:40, 13:47, 15:50, 17:45; 34 min), Mnichovo Hradiště ↔ Boseň, Mužský (4:59, 6:14, 11:39, 15:05 out; 5:17, 6:42, 13:42, 16:22 back; 12:17 Mužský round). One bus runs 15:05 → (loop) → Mužský 15:59 / 16:22 → Mnichovo Hradiště (and on round the loop to 17:19). Every 120 on that round, window 15:00–17:00 by hand, both slots exact, one bus. The loops cover only stops that the 15:05’s path also serves (Step 8), listed.

| Simutrans line | Every | Entry | Slots (real) | Typed | Running time | Window | On the minute | Off the pattern | Need |
|---|---|---|---|---|---|---|---|---|---|
| 716 | 120 | Mnichovo Hradiště, dopravní terminál → Boseň, Mužský | 13:05, 15:05, 17:05, 19:05 | 4 | 54 | 15:05 / 15:05 | 1 / 1 / 1 of 4 | 11:39 (34), 12:45 (20) | 1 |
|  |  | Boseň, Mužský → Mnichovo Hradiště, dopravní terminál | 12:22, 14:22, 16:22, 18:22, 20:22 | 81 | 23 | 16:22 / 16:22 | 1 / 1 / 1 of 5 | 12:17 (5), 13:42 (40) |  |

*Why on the card:* **716:** Mnichovo Hradiště 15:05 → Mužský round the Sychrov loop (Podolí, Kruhy, Sychrov) and Lhotice (54 min); Mužský 16:22 → Mnichovo Hradiště (23 min).

### 717  Mnichovo Hradiště - Turnov

- **Core points:** Mnichovo Hradiště, dopravní terminál | Turnov, Na Lukách. Anchor 16:00 (computed).
- **Reading and choice:** Whole day: Turnov :32 even hours (8:32–16:32; 4:57, 7:07) and Mnichovo Hradiště :50 even hours (6:25, 7:50, 8:50–16:50), exact. Every 120; need 2 (each bus waits 65 at Turnov and 105 at Mnichovo Hradiště, as in the timetable). Every 240 (1 bus) would halve a two-hourly line (Opavsko rule: not pulled to 240).

| Simutrans line | Every | Entry | Slots (real) | Typed | Running time | Window | On the minute | Off the pattern | Need |
|---|---|---|---|---|---|---|---|---|---|
| 717 | 120 | Mnichovo Hradiště, dopravní terminál → Turnov, Na Lukách | 12:50, 14:50, 16:50, 18:50, 20:50 | 109 | 37 | 16:50 / 16:50 | 5 / 5 / 5 of 7 | – | 2 |
|  |  | Turnov, Na Lukách → Mnichovo Hradiště, dopravní terminál | 12:32, 14:32, 16:32, 18:32, 20:32 | 91 | 33 | 16:32 / 16:32 | 5 / 5 / 5 of 6 | – |  |

*Why on the card:* **717:** Mnichovo Hradiště :50 even hours → Turnov, Na Lukách (37 min); Turnov :32 even hours → Mnichovo Hradiště (33 min).

### 718  Mnichovo Hradiště - Dolní Bousov - Sobotka

- **Core points:** Mnichovo Hradiště, dopravní terminál | Kněžmost, náměstí | Dolní Bousov, náměstí | Sobotka, náměstí. Anchor 16:00 (computed).
- **Reading and choice:** Whole day: Mnichovo Hradiště :15 hourly to Sobotka (14:20; 17:15 to Malobratřice; 18:18 to Kněžmost), Sobotka :03 (8:03, 10:03, 13:03, 16:03 exact; 14:08, 15:05, 17:05). Every 60, Mnichovo Hradiště :15 with core_to Kněžmost, náměstí (the 17:15 Malobratřice trip is run on to Sobotka; branch audit ok: it ends on the path), Sobotka :03 (more exact over the day than :05: 4 against 2). 2-minute turns at Sobotka as in reality (7 of 11), need 2.

| Simutrans line | Every | Entry | Slots (real) | Typed | Running time | Window | On the minute | Off the pattern | Need |
|---|---|---|---|---|---|---|---|---|---|
| 718 | 60 | Mnichovo Hradiště, dopravní terminál → Sobotka, náměstí | :15 | 14 | 46 | 16:15, 17:15 / 16:15, 17:15 | 7 / 7 / 8 of 12 | 14:20 (5) | 2 |
|  |  | Sobotka, náměstí → Mnichovo Hradiště, dopravní terminál | :03 | 2 | 42 | 16:03, 17:03 / 16:03, 17:05 | 4 / 4 / 6 of 9 | 14:08 (5) |  |

*Why on the card:* **718:** Mnichovo Hradiště :15 → Sobotka (46 min; the 17:15 to Kněžmost, Malobratřice, otočka is run on to Sobotka); Sobotka :03 → Mnichovo Hradiště (42 min), a 2-minute turn as in the timetable.

### 719  Mladá Boleslav - Bítouchov - Bakov nad Jizerou,Zvířetice

- **Core points:** Mladá Boleslav, autobusové stanoviště | Bakov nad Jizerou, Zvířetice. Anchor 15:30 (set by hand).
- **Reading and choice:** Whole day: Mladá Boleslav 6:20, 10:45, 12:15, 14:45, 16:45; Zvířetice 4:35, 6:50, 11:25, 12:55, 15:25 (4 of 5 arrivals at Zvířetice followed by a departure within 1 min). Every 120 Mladá Boleslav :45 even / Zvířetice :25 odd, 1-minute turn, one bus; window 15:00–17:00 by hand because Zvířetice has no departure after 15:25 (the 16:00 window would leave the 17:25 slot empty).

| Simutrans line | Every | Entry | Slots (real) | Typed | Running time | Window | On the minute | Off the pattern | Need |
|---|---|---|---|---|---|---|---|---|---|
| 719 | 120 | Mladá Boleslav, autobusové stanoviště → Bakov nad Jizerou, Zvířetice | 12:45, 14:45, 16:45, 18:45, 20:45 | 104 | 39 | 16:45 / 16:45 | 3 / 3 / 3 of 5 | 12:15 (30) | 1 |
|  |  | Bakov nad Jizerou, Zvířetice → Mladá Boleslav, autobusové stanoviště | 13:25, 15:25, 17:25, 19:25 | 24 | 39 | 15:25 / 15:25 | 2 / 2 / 2 of 4 | 12:55 (30) |  |

*Why on the card:* **719:** Mladá Boleslav :45 even hours → Zvířetice (39 min); Zvířetice :25 odd hours → Mladá Boleslav (39 min), a 1-minute turn as in the timetable.

### 720  Rokytnice n.Jiz. - Vysoké n.Jiz. - Semily - Železný Brod - Turnov - Mladá Boleslav - Praha

- **Core points:** Praha, Černý Most | Mladá Boleslav, autobusové stanoviště | Turnov, Na Lukách | Semily, Terminál | Mladá Boleslav, hl.nádraží. Anchor 13:40 (computed).
- **Reading and choice:** Whole day: express Praha → Semily 6:15, 8:15, 10:15, 13:15, 14:15, 17:15 (Rokytnice), 18:15; Semily → Praha 4:45, 7:50, 8:50, 10:50, 13:50, 15:50 (+ 4:15 Rokytnice); Praha → Turnov 9:15, 11:15, 12:15, 16:45; Turnov → Praha 6:20, 12:25, 13:25, 15:25; stopping trips Mladá Boleslav, hlavní nádraží ↔ Semily 6:10, 14:10, 22:10 / 4:12, 12:04, 20:12 (exactly 480 apart). 720 express every 240 with two slots each way: Praha 13:15, 14:15 (and 17:15, 18:15, 9:15, 10:15, 6:15 a period apart: 6 of 7 exact), Semily 13:50, 15:50; with 700 15:15 and 730 16:15 no two lines share a Praha minute. The Turnov trips’ stops are all on 720 (Step 8), listed. 720 Semily every 480 on 14:10 / 20:12 (12:04 is 8 min off), one bus, the only service of 13 stops of the old road. Need 720: 3. **Changed on 2 Nov (review, wording only):** the why now says that the Semily repeats 17:50 and 19:50 have no real trip (the buses sleep in Semily and Rokytnice).

| Simutrans line | Every | Entry | Slots (real) | Typed | Running time | Window | On the minute | Off the pattern | Need |
|---|---|---|---|---|---|---|---|---|---|
| 720 | 240 | Praha, Černý Most → Semily, Terminál | 13:15, 14:15, 17:15, 18:15 | 14, 74 | 115 | 13:15, 14:15 / 13:15, 14:15 | 6 / 6 / 6 of 7 | – | 3 |
|  |  | Semily, Terminál → Praha, Černý Most | 13:50, 15:50, 17:50, 19:50 | 49, 169 | 115 | 13:50 / 13:50 | 3 / 3 / 3 of 6 | 10:50 (60) |  |
| 720 Semily | 480 | Mladá Boleslav, hl.nádraží → Semily, Terminál | 14:10 | 309 | 105 | 14:10 / 14:10 | 3 / 3 / 3 of 3 | – | 1 |
|  |  | Semily, Terminál → Mladá Boleslav, hl.nádraží | 12:12, 20:12 | 191 | 88 | none / none | 1 / 1 / 1 of 2 | 12:04 (8) |  |

*Why on the card:* **720:** Praha :15 at 13:15, 14:15, 17:15, 18:15 → Semily, Terminál (115 min); Semily :50 at 13:50, 15:50 → Praha (115 min); every 240. The Semily repeats 17:50 and 19:50 have no real trip (the buses sleep in Semily and Rokytnice). **720 Semily:** Mladá Boleslav, hlavní nádraží 14:10 → Semily by the old road through Turnov and Železný Brod (105 min); Semily 20:12 → Mladá Boleslav, hlavní nádraží (88 min); both real, every 480 (also 6:10, 4:12).

### 721  Český Dub - Všelibice,Vrtky - Mnichovo Hradiště

- **Core points:** Mnichovo Hradiště, dopravní terminál | Všelibice, Vrtky | Český Dub, náměstí. Anchor 16:00 (computed).
- **Reading and choice:** Whole day: Český Dub → Mnichovo Hradiště 4:55, 7:05, 13:35, 17:40; Mnichovo Hradiště → Český Dub 5:53, 10:33, 15:08, 17:43; Český Dub ↔ Vrtky 15:35 / 16:11. The one-bus round Český Dub 13:35 → 14:17 / 15:08 → 15:52 is every 240 (42 + 51 + 44 + 103); no slot falls in the 16:00 window (both slot trips named in the why). The 13:35 path (stops_via Severka) carries the Severka – Loukovičky – Bohumileč – Libíč – Březová – Borek stops, which only 721 serves.

| Simutrans line | Every | Entry | Slots (real) | Typed | Running time | Window | On the minute | Off the pattern | Need |
|---|---|---|---|---|---|---|---|---|---|
| 721 | 240 | Český Dub, náměstí → Mnichovo Hradiště, dopravní terminál | 13:35, 17:35 | 34 | 42 | none / none | 1 / 1 / 1 of 3 | 17:40 (5) | 1 |
|  |  | Mnichovo Hradiště, dopravní terminál → Český Dub, náměstí | 15:08, 19:08 | 127 | 44 | none / none | 1 / 1 / 1 of 4 | 10:33 (35), 17:43 (85) |  |

*Why on the card:* **721:** Český Dub 13:35 → Mnichovo Hradiště via Severka, Loukovičky, Bohumileč, Libíč, Březová and Borek (42 min); Mnichovo Hradiště 15:08 → Český Dub (44 min); the real round, every 240.

### 722  Český Dub - Hlavice - Mnichovo Hradiště

- **Core points:** Mnichovo Hradiště, dopravní terminál | Hlavice, Vápno, Na Písku | Český Dub, náměstí. Anchor 16:00 (computed).
- **Reading and choice:** Whole day: Český Dub :42 hourly (4:25, 5:32, 6:30, 9:32, 12:42, 13:42, 14:32, 15:42, 16:42, 18:42), Mnichovo Hradiště :33 (5:33, 6:33, 8:33, 12:33, 13:33, 14:33, 15:23, 16:33, 18:33). Every 60 at :33 / :42 fails Step 4 on the Mnichovo Hradiště side (window 15:33 and 16:33, real 15:23 and 16:33: 1 of 2 filled), and every hourly window holding 15:33 or 17:33 fails the same way. Kept hourly (Opavsko rule 5: an hourly line is not halved for one stray trip), approximate, on the owner checks with the exact every-120 row (1 bus).

| Simutrans line | Every | Entry | Slots (real) | Typed | Running time | Window | On the minute | Off the pattern | Need |
|---|---|---|---|---|---|---|---|---|---|
| 722 | 60 | Mnichovo Hradiště, dopravní terminál → Český Dub, náměstí | :33 | 32 | 50 | 15:33 ✗, 16:33 / 16:33 | 8 / 8 / 8 of 9 | 15:23 (10) | 2 |
|  |  | Český Dub, náměstí → Mnichovo Hradiště, dopravní terminál | :42 | 41 | 48 | 15:42, 16:42 / 15:42, 16:42 | 5 / 5 / 5 of 9 | 14:32 (10) |  |

*Why on the card:* **722:** Mnichovo Hradiště :33 → Český Dub (50 min); Český Dub :42 → Mnichovo Hradiště (48 min).

### 723  Kopidlno - Libáň - Březno - Mladá Boleslav

- **Core points:** Mladá Boleslav, autobusové stanoviště | Libáň, autobusové stanoviště | Kopidlno, náměstí. Anchor 16:00 (computed).
- **Reading and choice:** Whole day: Kopidlno :15 (4:15, 5:15, 8:15, 12:15, 13:15, 15:15, 17:15, 20:15), Mladá Boleslav :40 (5:30, 6:25, 8:40, 10:40, 13:40, 14:35, 16:40, 18:40, 22:30). Every 120, Kopidlno :15 odd / Mladá Boleslav :40 even, both exact in the window; need 2 (the real line also runs on two buses: Mladá Boleslav 13:40 → 14:43 / 15:15 → and 14:35 → 15:40 / 17:15 →).

| Simutrans line | Every | Entry | Slots (real) | Typed | Running time | Window | On the minute | Off the pattern | Need |
|---|---|---|---|---|---|---|---|---|---|
| 723 | 120 | Kopidlno, náměstí → Mladá Boleslav, autobusové stanoviště | 13:15, 15:15, 17:15, 19:15 | 14 | 60 | 17:15 / 17:15 | 4 / 4 / 4 of 8 | 12:15 (60), 20:15 (60) | 2 |
|  |  | Mladá Boleslav, autobusové stanoviště → Kopidlno, náměstí | 12:40, 14:40, 16:40, 18:40, 20:40 | 99 | 62 | 16:40 / 16:40 | 4 / 4 / 4 of 9 | 13:40 (60), 14:35 (5) |  |

*Why on the card:* **723:** Kopidlno :15 odd hours → Mladá Boleslav (60 min); Mladá Boleslav :40 even hours → Kopidlno (62 min).

### 724  Mladá Boleslav - Dlouhá Lhota - Libáň - Kopidlno

- **Core points:** Mladá Boleslav, autobusové stanoviště | Veselice, dvůr | Libáň, autobusové stanoviště. Anchor 16:00 (computed).
- **Reading and choice:** Whole day: Libáň → Mladá Boleslav 4:25, 5:30, 6:30, 7:30, 10:30, 12:25, 14:30, 16:30, 20:30; Mladá Boleslav → Libáň 5:30, 9:30, 11:30, 12:30, 14:40, 15:30, 17:30, 22:30. Every 120 on the one-bus ping-pong Mladá Boleslav 15:30 → 16:17 / 16:30 → 17:17 / 17:30, exact, one bus.

| Simutrans line | Every | Entry | Slots (real) | Typed | Running time | Window | On the minute | Off the pattern | Need |
|---|---|---|---|---|---|---|---|---|---|
| 724 | 120 | Mladá Boleslav, autobusové stanoviště → Libáň, autobusové stanoviště | 13:30, 15:30, 17:30, 19:30 | 29 | 47 | 15:30 / 15:30 | 5 / 5 / 5 of 8 | 12:30 (60), 14:40 (50) | 1 |
|  |  | Libáň, autobusové stanoviště → Mladá Boleslav, autobusové stanoviště | 12:30, 14:30, 16:30, 18:30, 20:30 | 89 | 51 | 16:30 / 16:30 | 5 / 5 / 5 of 8 | 12:25 (5) |  |

*Why on the card:* **724:** Mladá Boleslav :30 odd hours → Libáň (47 min); Libáň :30 even hours → Mladá Boleslav (51 min).

### 725  Mladá Boleslav - Markvartice - Sobotka

- **Core points:** Mladá Boleslav, autobusové stanoviště | Zelenecká Lhota, Záhuby | Sobotka, náměstí | Dolní Bousov, Vlčí Pole. Anchor 16:00 (computed).
- **Reading and choice:** Whole day: Mladá Boleslav → Sobotka 6:25, 14:30; Sobotka → Mladá Boleslav 8:15, 14:03, 16:03; Mladá Boleslav → Záhuby 10:30, 17:30, 19:35, 22:30 and Záhuby → Mladá Boleslav 4:25, 12:23, 20:23; Mladá Boleslav → Vlčí Pole 12:30, 15:30; local Záhuby / Vlčí Pole trips. 725 every 240 on the round 14:30 → Sobotka 15:45 / 16:03 → Mladá Boleslav (75 + 18 + 72 + 75), one bus; every 120 would leave the 16:30 slot empty. 725 Vlčí Pole every 480 on the 15:30 with an empty return (Dolní Bousov, Vlčí Pole has no stop of another line within 2 km); not every 180 (12:30 and 15:30 both exact) because every 180 would leave Mladá Boleslav at 18:30 together with 725.

| Simutrans line | Every | Entry | Slots (real) | Typed | Running time | Window | On the minute | Off the pattern | Need |
|---|---|---|---|---|---|---|---|---|---|
| 725 | 240 | Mladá Boleslav, autobusové stanoviště → Sobotka, náměstí | 14:30, 18:30 | 89 | 75 | none / none | 1 / 1 / 1 of 2 | – | 1 |
|  |  | Sobotka, náměstí → Mladá Boleslav, autobusové stanoviště | 12:03, 16:03, 20:03 | 182 | 72 | 16:03 / 16:03 | 1 / 1 / 1 of 3 | 14:03 (120) |  |
| 725 Vlčí Pole | 480 | Mladá Boleslav, autobusové stanoviště → Dolní Bousov, Vlčí Pole | 15:30 | 389 | 52 | 15:30 / 15:30 | 1 / 1 / 1 of 2 | 12:30 (180) | 1 |
|  |  | Dolní Bousov, Vlčí Pole → Mladá Boleslav, autobusové stanoviště | untimed (empty return) | 0 | 58 | – | – | – |  |

*Why on the card:* **725:** Mladá Boleslav 14:30 → Sobotka via Zelenecká Lhota, Záhuby and Markvartice (75 min); Sobotka 16:03 → Mladá Boleslav (72 min); both real, every 240. **725 Vlčí Pole:** Mladá Boleslav 15:30 → Dolní Bousov, Vlčí Pole (52 min), the real trip; empty return.

### 726  Mladá Boleslav - Nová Telib - Žerčice - Semčice

- **Core points:** Mladá Boleslav, autobusové stanoviště | Březno | Žerčice. Anchor 15:30 (set by hand).
- **Reading and choice:** Whole day: Mladá Boleslav → Žerčice 12:10, 14:45, 16:45 (6:15 to Semčice), → Březno 12:25; Žerčice → Mladá Boleslav 4:45, 6:55, 12:45, 15:25; Březno 13:02. One bus 14:45 → 15:17 / 15:25 → 15:53 / 16:45 → 17:13. Every 120, window 15:00–17:00 by hand: Žerčice has no departure after 15:25, so the 16:00 window would hold the Žerčice slot 17:25 with no trip (Step 4 fail) and the real 15:25 just outside it. One bus.

| Simutrans line | Every | Entry | Slots (real) | Typed | Running time | Window | On the minute | Off the pattern | Need |
|---|---|---|---|---|---|---|---|---|---|
| 726 | 120 | Mladá Boleslav, autobusové stanoviště → Žerčice | 12:45, 14:45, 16:45, 18:45, 20:45 | 104 | 30 | 16:45 / 16:45 | 2 / 2 / 2 of 4 | 12:10 (35) | 1 |
|  |  | Žerčice → Mladá Boleslav, autobusové stanoviště | 13:25, 15:25, 17:25, 19:25 | 24 | 28 | 15:25 / 15:25 | 1 / 1 / 1 of 3 | 12:45 (40) |  |

*Why on the card:* **726:** Mladá Boleslav :45 even hours → Žerčice (30 min); Žerčice :25 odd hours → Mladá Boleslav (28 min).

### 728  Mladá Boleslav - Skalsko - Mšeno

- **Core points:** Mladá Boleslav, autobusové stanoviště | Mšeno | Mšeno, škola. Anchor 14:10 (computed).
- **Reading and choice:** Whole day: Mšeno :08 even hours 4:08, 8:08, 12:08, 14:08, 16:08, 20:08 (6:06 via Stránka) — exact; Mladá Boleslav 6:28, 10:45, 12:45, 13:45, 14:40 (via Stránka), 17:45, 22:30. Computed anchor 14:10 (window 13:40–15:40), kept: Mladá Boleslav 13:45 and Mšeno 14:08 exact. Every 120, need 2. Stránka, Ostrý, rozcestí (okres Mělník) has no other line 13:00–19:00 than 728’s 14:40 (Stránka, Tajná and rozcestí and Mšeno, škola also have the Mělnicko lines 689, 690, 696), so the way back is shown on the 6:06 trip’s loop through Mšeno, škola and Stránka (stops_via; 81 min instead of 66; the need stays 2).

| Simutrans line | Every | Entry | Slots (real) | Typed | Running time | Window | On the minute | Off the pattern | Need |
|---|---|---|---|---|---|---|---|---|---|
| 728 | 120 | Mladá Boleslav, autobusové stanoviště → Mšeno | 13:45, 15:45, 17:45, 19:45 | 44 | 62 | 13:45 / 13:45, 14:40 | 2 / 2 / 2 of 7 | 10:45 (60), 12:45 (60), 14:40 (55) | 2 |
|  |  | Mšeno → Mladá Boleslav, autobusové stanoviště | 12:08, 14:08, 16:08, 18:08, 20:08 | 67 | 81 | 14:08 / 14:08 | 5 / 5 / 6 of 6 | – |  |

*Why on the card:* **728:** Mladá Boleslav :45 odd hours → Mšeno (62 min); Mšeno :08 even hours → Mladá Boleslav through Mšeno, škola and Stránka, the 6:06 trip’s path (81 min; the afternoon trips run direct in 66 min).

### 729  Mladá Boleslav - Doubravička - Boreč

- **Core points:** Mladá Boleslav, autobusové stanoviště | Doubravička | Boreč, Žebice. Anchor 16:00 (computed).
- **Reading and choice:** Whole day: Mladá Boleslav → Doubravička 6:15, 11:45, 14:30, 22:25, → Boreč 9:15, 16:45, 19:15; Doubravička → Mladá Boleslav 4:35, 6:50, 12:35, 15:35; Boreč 10:18, 17:43, 20:18. The Boreč trips are 150 min apart (not an allowed interval); every 120 left the Boreč slot 15:43 in the window with no trip, and every 144 or 160 hold the 16:45 / 17:43 round but none of the other trips (14:30, 19:15, 20:18 are 6–30 min off). Every 240 on the real round 16:45 → Boreč 17:41 / 17:43 → Mladá Boleslav 18:40, one bus. The Doubravička trips run over stops of the Boreč trips (Krnsko, Strenice) and are listed.

| Simutrans line | Every | Entry | Slots (real) | Typed | Running time | Window | On the minute | Off the pattern | Need |
|---|---|---|---|---|---|---|---|---|---|
| 729 | 240 | Mladá Boleslav, autobusové stanoviště → Boreč, Žebice | 12:45, 16:45, 20:45 | 224 | 56 | 16:45 / 16:45 | 1 / 1 / 1 of 7 | 11:45 (60), 14:30 (105), 19:15 (90) | 1 |
|  |  | Boreč, Žebice → Mladá Boleslav, autobusové stanoviště | 13:43, 17:43 | 42 | 57 | none / none | 1 / 1 / 1 of 3 | 10:18 (35), 20:18 (85) |  |

*Why on the card:* **729:** Mladá Boleslav 16:45 → Boreč, Žebice (56 min); Boreč 17:43 → Mladá Boleslav (57 min), a 2-minute turn as in the timetable; every 240.

### 730  Vítkovice,Horní Mísečky - Jilemnice - Semily - Turnov - Praha

- **Core points:** Praha, Černý Most | Mladá Boleslav, autobusové stanoviště | Vítkovice, hotel Praha | Vítkovice, Horní Mísečky. Anchor 16:00 (computed).
- **Reading and choice:** Whole day: Vítkovice, hotel Praha 5:49 → Praha; Praha 16:15 → Vítkovice, Horní Mísečky. Every 480 on the 16:15 with an empty return (18 stops beyond Semily have no other service), one bus.

| Simutrans line | Every | Entry | Slots (real) | Typed | Running time | Window | On the minute | Off the pattern | Need |
|---|---|---|---|---|---|---|---|---|---|
| 730 | 480 | Praha, Černý Most → Vítkovice, Horní Mísečky | 16:15 | 434 | 175 | 16:15 / 16:15 | 1 / 1 / 1 of 1 | – | 1 |
|  |  | Vítkovice, Horní Mísečky → Praha, Černý Most | untimed (empty return) | 0 | 175 | – | – | – |  |

*Why on the card:* **730:** Praha 16:15 → Vítkovice, Horní Mísečky (175 min), the real trip; empty return to Praha.

### 731  Mladá Boleslav - Katusice - Plužná

- **Core points:** Mladá Boleslav, autobusové stanoviště | Katusice | Březovice. Anchor 16:00 (computed).
- **Reading and choice:** Whole day: Mladá Boleslav :45 odd hours 9:45, 15:45, 17:45, 19:45 (+ 5:15, 6:15, 11:35, 14:30, 22:25), Březovice :33 odd 9:33, 15:33, 17:33; Katusice starts 4:35, 5:45, 6:55, 12:40, 13:40. Read back at the knot Katusice (:40 odd: 13:40, 15:40, 17:40 exact). Every 120, need 2 (two buses alternate: 14:30 → 15:33 and 15:45 → 17:33).

| Simutrans line | Every | Entry | Slots (real) | Typed | Running time | Window | On the minute | Off the pattern | Need |
|---|---|---|---|---|---|---|---|---|---|
| 731 | 120 | Mladá Boleslav, autobusové stanoviště → Březovice | 13:45, 15:45, 17:45, 19:45 | 44 | 42 | 15:45 / 15:45 | 4 / 4 / 4 of 6 | 14:30 (45) | 2 |
|  |  | Březovice → Mladá Boleslav, autobusové stanoviště (timed at Katusice) | 13:33, 15:33, 17:33, 19:33 | 32 | 42 | 15:33 / 15:33 | 4 / 4 / 4 of 8 | 12:33 (60), 20:36 (57) |  |

*Why on the card:* **731:** Mladá Boleslav :45 odd hours → Březovice (42 min); Březovice :33 odd hours → Mladá Boleslav (42 min; timed at Katusice :40).

### 732  Čistá - Bělá pod Bezdězem,Bezdědice

- **Core points:** Bělá pod Bezdězem, Bezdědice | Březovice | Čistá, hřiště | Čistá, škola. Anchor 16:00 (computed).
- **Reading and choice:** Whole day: Bezdědice → Čistá 4:34, 6:52, 10:54, 12:32, 15:24, 17:19, 18:19; Čistá → Bezdědice 6:14, 11:23, 14:44, 15:48, 17:43, 18:43; Březovice ↔ Bezdědice shorts. Hourly only after 17:00. Every 120 Bezdědice :19 odd / Čistá, škola :48 odd, both exact in the window (every 60 :19 / :43 leaves 16:19 / 16:43 empty; :24 / :48 leaves 17:24 empty). One bus. Chain: the Čistá, hřiště trips meet 737 (3 of 3 arrivals followed by a 737 departure), named in the notes.

| Simutrans line | Every | Entry | Slots (real) | Typed | Running time | Window | On the minute | Off the pattern | Need |
|---|---|---|---|---|---|---|---|---|---|
| 732 | 120 | Bělá pod Bezdězem, Bezdědice → Čistá, škola | 13:19, 15:19, 17:19, 19:19 | 18 | 19 | 17:19 / 17:19 | 1 / 1 / 1 of 6 | 10:54 (25), 12:32 (47), 15:24 (5), 18:19 (60) | 1 |
|  |  | Čistá, škola → Bělá pod Bezdězem, Bezdědice | 13:48, 15:48, 17:48, 19:48 | 47 | 19 | 15:48 / 15:48 | 1 / 1 / 1 of 6 | 11:23 (25), 14:46 (58), 17:43 (5), 18:43 (55) |  |

*Why on the card:* **732:** Bezdědice :19 odd hours → Čistá, škola (19 min); Čistá, škola :48 odd hours → Bezdědice (19 min).

### 733  Turnov - Vlastibořice - Sezemice - Loukovec,Hubálov - Mnichovo Hradiště

- **Core points:** Mnichovo Hradiště, dopravní terminál | Sezemice | Turnov, Na Lukách | Vlastibořice, obec. Anchor 16:00 (computed).
- **Reading and choice:** Whole day: Mnichovo Hradiště → Turnov :22 even hours (4:12, 9:12, 12:22, 14:22, 16:22), Turnov → Mnichovo Hradiště :35 even (6:25, 9:50, 14:35, 16:35; 12:30 to náměstí); Turnov ↔ Vlastibořice, obec 13:35 / 14:04, 15:35 / 16:04; Sezemice → Mnichovo Hradiště 13:08, 15:36, 18:08; Kobyly and Loukovec early trips. Chains at Turnov 5 of 10 and Vlastibořice 2 of 2 (0–4 min): one bus runs Mnichovo Hradiště 12:22 → Turnov 13:35 → Vlastibořice → Turnov 14:31 / 14:35 → Mnichovo Hradiště. Modelled as that circuit every 120 (Turnov twice), all four slots exact, two buses, 0-minute turn at Turnov as in the timetable; a plain line plus a Vlastibořice shuttle needs 3.

| Simutrans line | Every | Entry | Slots (real) | Typed | Running time | Window | On the minute | Off the pattern | Need |
|---|---|---|---|---|---|---|---|---|---|
| 733 | 120 | Mnichovo Hradiště, dopravní terminál → Turnov, Na Lukách | 12:22, 14:22, 16:22, 18:22, 20:22 | 81 | 73 | 16:22 / 16:22 | 3 / 3 / 3 of 5 | – | 2 |
|  |  | Turnov, Na Lukách → Vlastibořice, obec | 13:35, 15:35, 17:35, 19:35 | 34 | 27 | 15:35 / 15:35, 16:35 | 2 / 2 / 2 of 7 | 12:30 (55), 14:35 (60), 16:35 (60) |  |
|  |  | Vlastibořice, obec → Turnov, Na Lukách | 12:04, 14:04, 16:04, 18:04, 20:04 | 63 | 27 | 16:04 / 16:04, 17:08 | 2 / 2 / 2 of 9 | 13:08 (56), 15:09 (55), 17:08 (56), 19:11 (53) |  |
|  |  | Turnov, Na Lukách → Mnichovo Hradiště, dopravní terminál | 12:35, 14:35, 16:35, 18:35, 20:35 | 94 | 70 | 16:35 / 16:35 | 2 / 2 / 2 of 4 | – |  |

*Why on the card:* **733:** Circuit every 120: Mnichovo Hradiště :22 even → Turnov (73 min), Turnov :35 odd → Vlastibořice, obec (27 min, 0-minute turn as in the timetable), Vlastibořice :04 even → Turnov (27 min), Turnov :35 even → Mnichovo Hradiště (70 min).

### 734  Mnichovo Hradiště - Mohelnice nad Jizerou - Sezemice

- **Core points:** Mnichovo Hradiště, dopravní terminál | Sezemice. Anchor 16:00 (computed).
- **Reading and choice:** Whole day: Mnichovo Hradiště → Sezemice 4:45, 10:35, 12:45, 15:10, 17:45; Sezemice → Mnichovo Hradiště 5:10, 6:35, 7:15, 10:58. In the afternoon every 734 bus comes back as 733 from Sezemice (12:45 → 13:07 / 13:08, 15:10 → 15:32 / 15:36, 17:45 → 18:07 / 18:08; 3 of 3). Step 5b: one Simutrans line, out on 734, back on 733 (lines 733, only trips that start at Sezemice), every 240 on 15:10 / 15:36 (every 144 put 17:34 in the window with no trip), one bus.

| Simutrans line | Every | Entry | Slots (real) | Typed | Running time | Window | On the minute | Off the pattern | Need |
|---|---|---|---|---|---|---|---|---|---|
| 734 | 240 | Mnichovo Hradiště, dopravní terminál → Sezemice | 15:10, 19:10 | 129 | 22 | none / none | 1 / 1 / 1 of 4 | 10:35 (35), 12:45 (95), 17:45 (85) | 1 |
|  |  | Sezemice → Mnichovo Hradiště, dopravní terminál | 15:36, 19:36 | 155 | 29 | 15:36 / 15:36 | 1 / 1 / 1 of 2 | 18:08 (88) |  |

*Why on the card:* **734:** Mnichovo Hradiště 15:10 → Sezemice via Mohelnice and Chocnějovice (22 min); Sezemice 15:36 → Mnichovo Hradiště as 733 via Loukovec (29 min); every 240.

### 735  Kopidlno - Libáň - Dolní Bousov

- **Core points:** Kopidlno, náměstí | Libáň, autobusové stanoviště | Dolní Bousov, náměstí | Dětenice, Brodek. Anchor 14:30 (set by hand).
- **Reading and choice:** Whole day: Kopidlno → Dolní Bousov 6:50, 10:05, 14:05 (Libáň shorts 4:32, 12:05; 16:10 → Dětenice, Brodek); Dolní Bousov → Kopidlno 7:41, 13:10, 15:04. Window 14:00–16:00 by hand on the round 14:05 → 15:00 / 15:04 → 15:56 (the 16:00 window would put a Kopidlno slot at 16:05 against the Brodek trip 16:10). **Changed on 2 Nov (review):** first designed as 735 every 120 (14:05 / 15:04, 1 bus) plus 735 Brodek every 480 (16:10, empty return, 1 bus). Every 240 has the same exact hits as every 120 (10:05, 14:05; 15:04) and leaves no slot without a trip, and the 16:10 → Brodek is the same bus’s next trip (Dolní Bousov 15:00 → 15:04 and Kopidlno 15:56 → 16:10 are real turns), so 735 is now one circuit every 240: Kopidlno 14:05 → Dolní Bousov, Dolní Bousov 15:04 → Kopidlno, Kopidlno 16:10 → Dětenice, Brodek, empty return to Kopidlno via Libáň (55 + 4 + 50 + 14 + 30 + 34 + 53 = 240), one bus, −1 bus. Dětenice, Brodek (1.4 km from the next served stop) stays on a line.

| Simutrans line | Every | Entry | Slots (real) | Typed | Running time | Window | On the minute | Off the pattern | Need |
|---|---|---|---|---|---|---|---|---|---|
| 735 | 240 | Kopidlno, náměstí → Dolní Bousov, náměstí | 14:05, 18:05 | 64 | 55 | 14:05 / 14:05 | 2 / 2 / 2 of 3 | – | 1 |
|  |  | Dolní Bousov, náměstí → Kopidlno, náměstí | 15:04, 19:04 | 123 | 50 | 15:04 / 15:04 | 1 / 1 / 1 of 3 | 13:10 (114) |  |
|  |  | Kopidlno, náměstí → Dětenice, Brodek | 12:10, 16:10, 20:10 | 189 | 30 | none / none | 1 / 1 / 1 of 1 | – |  |
|  |  | Dětenice, Brodek → Kopidlno, náměstí | untimed (empty return) | 0 | 34 | – | – | – |  |

*Why on the card:* **735:** Circuit every 240, one bus: Kopidlno 14:05 → Dolní Bousov (55 min); Dolní Bousov 15:04 → Kopidlno (50 min); Kopidlno 16:10 → Libáň → Dětenice, Brodek (30 min); empty return from Brodek to Kopidlno via Libáň (34 min). All three timed trips are real.

### 736  Mladá Boleslav - Kněžmost - Dolní Bousov

- **Core points:** Mladá Boleslav, autobusové stanoviště | Kněžmost, náměstí | Dobšín | Dolní Bousov, náměstí. Anchor 16:00 (computed).
- **Reading and choice:** Whole day: Mladá Boleslav → Kněžmost / Dolní Bousov 5:20, 6:15, 9:50, 12:00, 13:25, 14:35, 15:50 (Dobšín), 17:50, 19:50; back Dobšín 4:21, Dolní Bousov 6:20, 12:15, 16:05, Kněžmost 11:35, 15:00, 18:35; Dolní Bousov ↔ Kněžmost shorts. Read at the knot Kněžmost, náměstí (out core_to, back knot): Mladá Boleslav :50 odd (9:50, 15:50, 17:50, 19:50 exact), Kněžmost :35 even (16:35, 18:35). Every 120 to Dolní Bousov, need 2; it covers the Kněžmost – Dobšín – Dolní Bousov stops only 736 serves. Rejected: every 240 on 14:35 / 16:05 (1 bus, 2 exact hits against 6).

| Simutrans line | Every | Entry | Slots (real) | Typed | Running time | Window | On the minute | Off the pattern | Need |
|---|---|---|---|---|---|---|---|---|---|
| 736 | 120 | Mladá Boleslav, autobusové stanoviště → Dolní Bousov, náměstí | 13:50, 15:50, 17:50, 19:50 | 49 | 65 | 15:50 / 15:50 | 4 / 4 / 4 of 9 | 12:00 (10), 13:25 (25), 14:35 (45) | 2 |
|  |  | Dolní Bousov, náměstí → Mladá Boleslav, autobusové stanoviště (timed at Kněžmost, náměstí) | 12:07, 14:07, 16:07, 18:07, 20:07 | 66 | 66 | 16:07 / 16:07 | 2 / 2 / 2 of 5 | 11:07 (60), 12:12 (5), 14:32 (25) |  |

*Why on the card:* **736:** Mladá Boleslav :50 odd hours → Dolní Bousov (65 min); Dolní Bousov :07 even hours → Mladá Boleslav, timed at Kněžmost :35 (66 min).

### 737  Mladá Boleslav - Čistá - Bělá pod Bezdězem

- **Core points:** Mladá Boleslav, autobusové stanoviště | Čistá, hřiště | Bělá pod Bezdězem, Atmos. Anchor 14:10 (computed).
- **Reading and choice:** Whole day: two paths alternating. Via Čistá: Mladá Boleslav 13:00, 13:45, 14:35, 15:30, 16:30, 17:20, 18:20, 19:05, 20:10; Bělá 12:00, 12:40, 13:50, 14:30, 15:30, 17:25, 18:25, 19:25, 20:45. Direct: Mladá Boleslav 12:00, 14:15, 15:00, 16:00, 16:55, 17:50; Bělá 13:20, 14:10, 15:00, 16:30. Computed anchor 14:10 (window 13:40–15:40), five departures each way. No pattern passes Step 4 there for either path (audit: only every 160 / 90 multi-slot rows that are not repeating patterns); the one-line every-60 row passed in a 16:00 window only by reading the direct 16:30 as a via-Čistá slot. Kept: 737 via Čistá every 60 :30 / :30 and 737 direct every 60 :00 / :00, interleaved, approximate, on the owner checks with the one-line option. Need 2 + 2. **Changed on 2 Nov (review, wording only):** the deviations were understated as “up to 15 min”; they are 5–30 min (13:50 and 13:20 are 20 off, the 16:30 direct back 30, as it falls between the direct line’s :00 slots); note and owner check corrected. The review’s optional anchor 15:00 (out legs exact there) was not taken, the backs stay approximate in every window.

| Simutrans line | Every | Entry | Slots (real) | Typed | Running time | Window | On the minute | Off the pattern | Need |
|---|---|---|---|---|---|---|---|---|---|
| 737 | 60 | Mladá Boleslav, autobusové stanoviště → Bělá pod Bezdězem, Atmos | :30 | 29 | 32 | 14:30 ✗, 15:30 / 13:45, 14:35, 15:30 | 3 / 3 / 3 of 17 | 10:00 (30), 11:00 (30), 13:00 (30), 13:45 (15), 14:35 (5), 17:20 (10), 18:20 (10), 19:05 (25), 20:10 (20) | 2 |
|  |  | Bělá pod Bezdězem, Atmos → Mladá Boleslav, autobusové stanoviště | :30 | 29 | 35 | 14:30, 15:30 / 13:50, 14:30, 15:30 | 2 / 2 / 2 of 16 | 10:00 (30), 11:00 (30), 12:00 (30), 12:40 (10), 13:50 (20), 17:25 (5), 18:25 (5), 19:25 (5), 20:45 (15) |  |
| 737 direct | 60 | Mladá Boleslav, autobusové stanoviště → Bělá pod Bezdězem, Atmos | :00 | 59 | 27 | 14:00 ✗, 15:00 / 14:15, 15:00 | 3 / 3 / 3 of 6 | 14:15 (15), 16:55 (5), 17:50 (10) | 2 |
|  |  | Bělá pod Bezdězem, Atmos → Mladá Boleslav, autobusové stanoviště | :00 | 59 | 30 | 14:00 ✗, 15:00 / 14:10, 15:00 | 2 / 2 / 2 of 6 | 13:20 (20), 14:10 (10), 16:30 (30) |  |

*Why on the card:* **737:** Mladá Boleslav :30 → Bělá via Čistá, hřiště (32 min); Bělá :30 → Mladá Boleslav via Čistá (35 min). **737 direct:** Mladá Boleslav :00 → Bělá by the direct road, not through Čistá (27 min); Bělá :00 → Mladá Boleslav direct (30 min).

### 738  Mnichovo Hradiště - Horní Bukovina - Mukařov,Vicmanov

- **Core points:** Mnichovo Hradiště, dopravní terminál | Horní Bukovina, Dolní Bukovina | Mukařov, Vicmanov. Anchor 16:00 (set by hand).
- **Reading and choice:** Whole day: Mnichovo Hradiště → Vicmanov 6:00, 13:15, 15:25, 17:15, → Dolní Bukovina 14:05; Vicmanov 5:05, 6:30, 13:50, 16:05; Dolní Bukovina 14:25. The computed anchor 14:20 holds the Dolní Bukovina short and the 13:15 / 13:50 pair (Mnichovo Hradiště slot 15:15 against the real 15:25 failed), so 16:00 by hand: Mnichovo Hradiště 17:15 and Vicmanov 16:05 exact, one bus. The short’s two stops of its own are coverage exceptions (owner check).

| Simutrans line | Every | Entry | Slots (real) | Typed | Running time | Window | On the minute | Off the pattern | Need |
|---|---|---|---|---|---|---|---|---|---|
| 738 | 120 | Mnichovo Hradiště, dopravní terminál → Mukařov, Vicmanov | 13:15, 15:15, 17:15, 19:15 | 14 | 30 | 17:15 / 17:15 | 2 / 2 / 2 of 4 | 15:25 (10) | 1 |
|  |  | Mukařov, Vicmanov → Mnichovo Hradiště, dopravní terminál | 12:05, 14:05, 16:05, 18:05, 20:05 | 64 | 27 | 16:05 / 16:05 | 1 / 1 / 1 of 4 | 13:50 (15) |  |

*Why on the card:* **738:** Mnichovo Hradiště :15 odd hours → Mukařov, Vicmanov (30 min); Vicmanov :05 even hours → Mnichovo Hradiště (27 min).

### 739  Mladá Boleslav - Bělá pod Bezdězem - Bakov nad Jizerou - Kněžmost

- **Core points:** Kněžmost, náměstí | Bakov nad Jizerou, železniční zastávka | Bělá pod Bezdězem, náměstí | Bělá pod Bezdězem, Atmos | Bělá pod Bezdězem, Dřevařská. Anchor 16:00 (computed).
- **Reading and choice:** Whole day: Kněžmost → Bělá 4:40, 5:55, 12:40 (Dřevařská), 14:43, 16:35, 18:35; Bělá → Kněžmost 4:41, 6:14, 12:31, 14:23 (Dřevařská), 16:28 (Dřevařská), 17:31; Bělá ↔ Bakov shorts. Read back at Bělá pod Bezdězem, náměstí, which all trips pass (:36 even: 12:36, 14:36, 16:36). Every 120, Kněžmost :35 even (core_to Bělá, náměstí) to Dřevařská, need 2 (two buses as in reality).

| Simutrans line | Every | Entry | Slots (real) | Typed | Running time | Window | On the minute | Off the pattern | Need |
|---|---|---|---|---|---|---|---|---|---|
| 739 | 120 | Kněžmost, náměstí → Bělá pod Bezdězem, Dřevařská | 12:35, 14:35, 16:35, 18:35, 20:35 | 94 | 47 | 16:35 / 16:35 | 2 / 2 / 2 of 5 | 12:40 (5), 14:43 (8) | 2 |
|  |  | Bělá pod Bezdězem, Dřevařská → Kněžmost, náměstí (timed at Bělá pod Bezdězem, náměstí) | 12:26, 14:26, 16:26, 18:26, 20:26 | 85 | 51 | 16:26 / 16:26, 17:26 | 3 / 3 / 3 of 5 | 17:26 (60) |  |

*Why on the card:* **739:** Kněžmost :35 even hours → Bělá pod Bezdězem, Dřevařská (47 min, the real trips end at Atmos); Dřevařská :26 even hours → Kněžmost, timed at Bělá, náměstí :36 (51 min).

### 763  Mladá Boleslav - Dobrovice - Dobrovice,Chloumek

- **Core points:** Mladá Boleslav, autobusové stanoviště | Dobrovice, autobusové stanoviště | Dobrovice, Chloumek. Anchor 14:20 (computed).
- **Reading and choice:** Whole day: Mladá Boleslav → Chloumek 12:05, 14:35, 17:05 (6:15 from Zalužany), → Dobrovice 6:55, 13:30; Chloumek → Mladá Boleslav 4:38, 6:58, 12:43, 15:43, 20:43. Computed anchor 14:20, kept: every 120 on the one-bus round 14:35 → 15:09 / 15:43 → 16:18, exact. A first try with Mladá Boleslav 17:05 left the 15:05 window slot empty.

| Simutrans line | Every | Entry | Slots (real) | Typed | Running time | Window | On the minute | Off the pattern | Need |
|---|---|---|---|---|---|---|---|---|---|
| 763 | 120 | Mladá Boleslav, autobusové stanoviště → Dobrovice, Chloumek | 12:35, 14:35, 16:35, 18:35, 20:35 | 94 | 34 | 14:35 / 14:35 | 1 / 1 / 1 of 4 | 12:05 (30), 17:05 (30) | 1 |
|  |  | Dobrovice, Chloumek → Mladá Boleslav, autobusové stanoviště | 13:43, 15:43, 17:43, 19:43 | 42 | 35 | 15:43 / 15:43 | 1 / 1 / 1 of 4 | 12:43 (60), 20:43 (60) |  |

*Why on the card:* **763:** Mladá Boleslav :35 even hours → Dobrovice, Chloumek (34 min); Chloumek :43 odd hours → Mladá Boleslav (35 min).

### 764  Mladá Boleslav - Dobrovice - Mcely

- **Core points:** Mladá Boleslav, autobusové stanoviště | Dobrovice, autobusové stanoviště | Mcely. Anchor 16:00 (computed).
- **Reading and choice:** Whole day: one bus all afternoon: Mladá Boleslav 13:00, 14:35, 17:45, 19:35 and Mcely 12:20, 16:25, 18:35, 20:25 (spacings 95–190 min). Every 120 options leave a window slot empty (Mladá Boleslav 15:45 / 16:35), so every 240 on 14:35 → 15:24 / 16:25 → 17:09 (20:25 is the same slot again), one bus.

| Simutrans line | Every | Entry | Slots (real) | Typed | Running time | Window | On the minute | Off the pattern | Need |
|---|---|---|---|---|---|---|---|---|---|
| 764 | 240 | Mladá Boleslav, autobusové stanoviště → Mcely | 14:35, 18:35 | 94 | 48 | none / none | 1 / 1 / 1 of 6 | 10:45 (10), 13:00 (95), 17:45 (50), 19:35 (60) | 1 |
|  |  | Mcely → Mladá Boleslav, autobusové stanoviště | 12:25, 16:25, 20:25 | 204 | 44 | 16:25 / 16:25 | 2 / 2 / 2 of 7 | 12:20 (5), 18:35 (110) |  |

*Why on the card:* **764:** Mladá Boleslav 14:35 → Mcely (48 min); Mcely 16:25 → Mladá Boleslav (44 min); both real, every 240.

### 766  Březno - Lhotky - Rabakov

- **Core points:** Březno | Lhotky | Rabakov. Anchor 16:00 (computed).
- **Reading and choice:** Whole day: Rabakov 4:35, 6:30, 14:40, 16:40 → Březno; Březno 5:58, 15:02, 17:02 → Rabakov; Březno ↔ Lhotky 12:43 / 12:54. Exactly every 120 in the afternoon (Rabakov :40 even, Březno :02 odd), one bus with 4-minute turns at Březno. Its Březno departures follow 726 arrivals (2 of 4).

| Simutrans line | Every | Entry | Slots (real) | Typed | Running time | Window | On the minute | Off the pattern | Need |
|---|---|---|---|---|---|---|---|---|---|
| 766 | 120 | Rabakov → Březno | 12:40, 14:40, 16:40, 18:40, 20:40 | 99 | 18 | 16:40 / 16:40 | 2 / 2 / 2 of 3 | – | 1 |
|  |  | Březno → Rabakov | 13:02, 15:02, 17:02, 19:02 | 1 | 16 | 17:02 / 17:02 | 2 / 2 / 2 of 3 | – |  |

*Why on the card:* **766:** Rabakov :40 even hours → Březno (18 min); Březno :02 odd hours → Rabakov (16 min).

### 767  Mladá Boleslav - Kropáčova Vrutice - Dolní Slivno

- **Core points:** Mladá Boleslav, autobusové stanoviště | Bezno | Kropáčova Vrutice, Krpy | Dolní Slivno. Anchor 14:30 (set by hand).
- **Reading and choice:** Whole day: Dolní Slivno → Mladá Boleslav 4:14, 6:22, 12:14, 20:19, → Bezno 5:24, 8:24, 10:24, 13:29, 15:29; Mladá Boleslav → Dolní Slivno 9:00, 11:00, 14:30, 22:30; Bezno ↔ Krpy shuttle hourly 15:58–18:58. 767 every 240 on the real round 14:30 → 15:26 / 15:29 (3-min turn) → Bezno, run on to Mladá Boleslav, one bus. **Changed on 2 Nov (review):** 767 Krpy (hourly Bezno :58 / Krpy :37, 1 bus, approximate) is deleted: the shuttle (Bezno 15:58, 16:58, 18:03 → Krpy; Krpy 16:37, 17:37, 18:37 → Bezno) runs only over stops 767 serves both ways (Chotětov, Hřivno, Sušno, Kropáčova Vrutice, rozcestí Krpy, Krpy), so it is listed (the 282 rule), and 767 is modelled at 14:30 by hand (window 14:00–16:00, which holds the real 14:30 and 15:29), where its own pattern runs; −1 bus, its owner check removed.

| Simutrans line | Every | Entry | Slots (real) | Typed | Running time | Window | On the minute | Off the pattern | Need |
|---|---|---|---|---|---|---|---|---|---|
| 767 | 240 | Mladá Boleslav, autobusové stanoviště → Dolní Slivno | 14:30, 18:30 | 89 | 56 | 14:30 / 14:30 | 2 / 2 / 2 of 4 | 11:00 (30) | 1 |
|  |  | Dolní Slivno → Mladá Boleslav, autobusové stanoviště | 15:29, 19:29 | 148 | 56 | 15:29 / 15:29 | 1 / 1 / 1 of 8 | 10:24 (65), 12:14 (45), 13:29 (120), 20:19 (50) |  |

*Why on the card:* **767:** Mladá Boleslav 14:30 → Dolní Slivno (56 min); Dolní Slivno 15:29 → Bezno, run on to Mladá Boleslav (56 min); every 240.

### 768  Benátky nad Jizerou - Dolní Slivno - Byšice

- **Core points:** Benátky nad Jizerou, autobusové stanoviště | Horní Slivno | Kropáčova Vrutice, Kojovice | Byšice. Anchor 15:00 (set by hand).
- **Reading and choice:** Whole day: Benátky → Kojovice 5:10, 5:50, 7:10, 12:12, 14:15, 16:15, 17:20, 18:15; → Byšice 10:15, 13:12, 15:20; Kojovice → Benátky 4:54, 6:04, 6:31, 8:44, 13:14, 15:14, 17:19; Byšice → Benátky 11:48, 14:14, 16:19. Ex4: 768 (Kojovice, notvia Byšice) every 120 Benátky :15 even / Kojovice :14 odd, 768 Byšice every 120 Benátky :20 odd / Byšice :19 even (1-minute turn), one bus each, so Benátky has one departure an hour. Window 14:30–16:30 by hand: the 16:00 window put the Kojovice slot at 17:14 against the real 17:19 and left the Byšice slots without trips (the real 15:20 / 16:19 sit just outside it).

| Simutrans line | Every | Entry | Slots (real) | Typed | Running time | Window | On the minute | Off the pattern | Need |
|---|---|---|---|---|---|---|---|---|---|
| 768 | 120 | Benátky nad Jizerou, autobusové stanoviště → Kropáčova Vrutice, Kojovice | 12:15, 14:15, 16:15, 18:15, 20:15 | 74 | 52 | 16:15 / 16:15 | 3 / 3 / 4 of 8 | 17:20 (55) | 1 |
|  |  | Kropáčova Vrutice, Kojovice → Benátky nad Jizerou, autobusové stanoviště | 13:14, 15:14, 17:14, 19:14 | 13 | 48 | 15:14 / 15:14 | 2 / 2 / 2 of 6 | 17:19 (5) |  |
| 768 Byšice | 120 | Benátky nad Jizerou, autobusové stanoviště → Byšice | 13:20, 15:20, 17:20, 19:20 | 19 | 58 | 15:20 / 15:20 | 1 / 1 / 1 of 3 | 10:15 (55), 13:12 (8) | 1 |
|  |  | Byšice → Benátky nad Jizerou, autobusové stanoviště | 12:19, 14:19, 16:19, 18:19, 20:19 | 78 | 56 | 16:19 / 16:19 | 1 / 1 / 1 of 3 | 11:48 (31), 14:14 (5) |  |

*Why on the card:* **768:** Benátky :15 even hours → Kropáčova Vrutice, Kojovice (52 min); Kojovice :14 odd hours → Benátky (48 min). **768 Byšice:** Benátky :20 odd hours → Byšice via Kojovice (58 min); Byšice :19 even hours → Benátky (56 min), a 1-minute turn as in the timetable.

### 775  Mladá Boleslav - Dobrovice - Luštěnice - Benátky nad Jizerou

- **Core points:** Mladá Boleslav, autobusové stanoviště | Dobrovice, autobusové stanoviště | Luštěnice, Sluneční | Horky nad Jizerou. Anchor 16:00 (computed).
- **Reading and choice:** Whole day: Mladá Boleslav → Luštěnice, Sluneční :35 (8:35, 10:35, 13:35, 15:35–18:35; 12:25, 20:25), → Horky 13:40, 14:30 (from Zalužany); back at Sluneční 4:14, 6:29, 10:29, 12:29, 13:29, 14:29 (from Horky 14:20), 15:54 (from Horky 15:45), 16:39 (from Benátky 16:20), 20:29; Luštěnice local trips, Smilovice and Benátky early trips. The buses sleep in Luštěnice (first trips start there); in the 16:00 window two come back (15:54, 16:39) against four out, and no hourly back minute fills both (every 60 at :29 left 16:29 and 17:29 empty). First design (outstation rule, one slot each way): every 120 Mladá Boleslav 15:35 / Sluneční 16:39, one bus, 4 trips on the minute. Final: every 120 with two slots each way, Mladá Boleslav :35 every hour and Sluneční 15:54 / 16:39 (the inbound rate is 2 per 2 hours in the window, so both ends run at it), all four window departures exact and 9 on the minute over the day, 3 buses (the returns come in 45 min apart, so one bus waits 111 min at Mladá Boleslav). By the method’s order (most exact first; the 290 rule) the exact row is on the sheet. **Changed on 2 Nov (review):** the owner check offering the 1-bus row is removed: that row sits below the inbound rate and passes only by the ±1 tolerance, so Step 4 rule 3 and the 290 rule decide; the row is unchanged.

| Simutrans line | Every | Entry | Slots (real) | Typed | Running time | Window | On the minute | Off the pattern | Need |
|---|---|---|---|---|---|---|---|---|---|
| 775 | 120 | Mladá Boleslav, autobusové stanoviště → Luštěnice, Sluneční | 12:35, 13:35, 14:35, 15:35, 16:35, 17:35, 18:35, 19:35, 20:35 | 34, 94 | 58 | 15:35, 16:35 / 15:35, 16:35 | 7 / 7 / 7 of 13 | 12:25 (10), 13:40 (5), 14:30 (5), 20:25 (10) | 3 |
|  |  | Luštěnice, Sluneční → Mladá Boleslav, autobusové stanoviště | 12:39, 13:54, 14:39, 15:54, 16:39, 17:54, 18:39, 19:54, 20:39 | 53, 98 | 50 | 15:54, 16:39 / 15:54, 16:39 | 2 / 2 / 2 of 10 | 10:29 (10), 12:29 (10), 13:29 (25), 14:29 (10), 20:29 (10) |  |

*Why on the card:* **775:** Mladá Boleslav :35 every hour → Luštěnice, Sluneční (58 min); Sluneční :54 odd hours and :39 even hours → Mladá Boleslav (50 min), the Horky and Benátky trips run from Sluneční in the game.

### 540345  Liberec - Hodkovice nad Mohelkou - Mladá Boleslav

- **Core points:** Liberec, autobusové nádraží | Mladá Boleslav, autobusové stanoviště. Anchor 16:00 (computed).
- **Reading and choice:** Whole day: Liberec 4:18, 12:25, 20:25 → Mladá Boleslav; Mladá Boleslav 6:20, 14:20, 22:15 → Liberec: two exact 480 series. Every 480 on 12:25 / 14:20, one bus (65 + 50 + 60 + 305); 4 of 6 trips on the minute. Chains: its Mladá Boleslav departures follow 345 arrivals (2 of 3), and at Liberec its departures follow 345 arrivals (2 of 3).

| Simutrans line | Every | Entry | Slots (real) | Typed | Running time | Window | On the minute | Off the pattern | Need |
|---|---|---|---|---|---|---|---|---|---|
| 540345 | 480 | Liberec, autobusové nádraží → Mladá Boleslav, autobusové stanoviště | 12:25, 20:25 | 204 | 65 | none / none | 2 / 2 / 2 of 2 | – | 1 |
|  |  | Mladá Boleslav, autobusové stanoviště → Liberec, autobusové nádraží | 14:20 | 319 | 60 | none / none | 2 / 2 / 2 of 3 | – |  |

*Why on the card:* **540345:** Liberec, autobusové nádraží 12:25 (and 20:25) → Mladá Boleslav (65 min); Mladá Boleslav 14:20 (and 6:20) → Liberec (60 min); every 480, one bus.

### Not modelled

- **727:** Unmodelled (Step 8): 5 trips a day, one in the afternoon (Rokytá, Horní Rokytá, otočka 13:25 → Mnichovo Hradiště 13:47); every stop is on 427’s game path round Horní Rokytá (the 15:25 trip) or on 738.
- **769:** Carried by 699 (see 699): its two afternoon trips Chotětov 13:10 and 15:10 are the way back of the 699 buses; morning 6:00 Mladá Boleslav → Chotětov and 6:55 Chotětov → Bezno are listed.
- **XS35 (992035):** XS35, the rail replacement bus Turnov – Mladá Boleslav for the railway works: left out automatically (replacement buses are not modelled; short works are modelled as the regular network). All its stops 13:00–19:00 are on modelled lines (coverage shows no stop of its own).

## Summary

| Line | Simutrans lines | Every | Slots in real minutes (first entry / second entry …) | Buses |
|---|---|---|---|---|
| 315 | 315 | 30 | :10 :40 / :03 :33 | 8 |
| 345 | 345 | 60 | :30 / :40 | 5 |
| 403 | 403 | 480 | 16:30 / 13:10 | 1 |
| 405 | 405 | 120 | 13:00, 15:00, 17:00, 19:00 / 12:00, 14:00, 16:00, 18:00, 20:00 | 4 |
| 405 | 405 Vrchlabí | 480 | 14:35 / untimed | 1 |
| 412 | 412 | 120 | 12:00, 14:00, 16:00, 18:00, 20:00 / 12:35, 14:35, 16:35, 18:35, 20:35 | 3 |
| 427 | 427 | 120 | 13:25, 15:25, 17:25, 19:25 / 12:35, 14:35, 16:35, 18:35, 20:35 | 1 |
| 431 | 431 | 120 | 12:02, 14:02, 16:02, 18:02, 20:02 / 13:35, 15:35, 17:35, 19:35 | 2 |
| 431 | 431 Stará Lysá | 480 | 13:34 / 13:46 / 15:11 / 15:50 | 1 |
| 442 | 442 | 60 | :31 / :18 | 3 |
| 442 | 442 Dražice | 120 | 12:08, 12:38, 12:58, 13:15, 13:38, 14:08, 14:38, 14:58, 15:15, 15:38, 16:08, 16:38, 16:58, 17:15, 17:38, 18:08, 18:38, 18:58, 19:15, 19:38, 20:08, 20:38, 20:58 / 12:26, 12:48, 13:05, 13:26, 13:55, 14:26, 14:48, 15:05, 15:26, 15:55, 16:26, 16:48, 17:05, 17:26, 17:55, 18:26, 18:48, 19:05, 19:26, 19:55, 20:26, 20:48 | 1 |
| 467 | 467 | 60 | :30 / :45 | 4 |
| 699 | 699 | 120 | 12:30, 14:30, 16:30, 18:30, 20:30 / 13:10, 15:10, 17:10, 19:10 | 1 |
| 699 | 699 Kadlín | 120 | 13:00, 15:00, 17:00, 19:00 / 13:38, 15:38, 17:38, 19:38 | 1 |
| 700 | 700 | 480 | 15:15 / untimed | 1 |
| 712 | 712 | 120 | 12:35, 14:35, 16:35, 18:35, 20:35 / 12:15, 14:15, 16:15, 18:15, 20:15 | 2 |
| 713 | 713 | 120 | 12:20, 14:20, 16:20, 18:20, 20:20 / 13:00, 15:00, 17:00, 19:00 | 1 |
| 714 | 714 | 240 | 14:30, 18:30 / 13:17, 17:17 | 1 |
| 714 | 714 Sobotka | 480 | 13:05 / 14:10 / 15:40 | 1 |
| 715 | 715 | 120 | 13:40, 15:40, 17:40, 19:40 / 12:28, 14:28, 16:28, 18:28, 20:28 | 1 |
| 715 | 715 Mnichovo Hradiště | 120 | 12:45, 14:45, 16:45, 18:45, 20:45 / 13:38, 15:38, 17:38, 19:38 | 1 |
| 716 | 716 | 120 | 13:05, 15:05, 17:05, 19:05 / 12:22, 14:22, 16:22, 18:22, 20:22 | 1 |
| 717 | 717 | 120 | 12:50, 14:50, 16:50, 18:50, 20:50 / 12:32, 14:32, 16:32, 18:32, 20:32 | 2 |
| 718 | 718 | 60 | :15 / :03 | 2 |
| 719 | 719 | 120 | 12:45, 14:45, 16:45, 18:45, 20:45 / 13:25, 15:25, 17:25, 19:25 | 1 |
| 720 | 720 | 240 | 13:15, 14:15, 17:15, 18:15 / 13:50, 15:50, 17:50, 19:50 | 3 |
| 720 | 720 Semily | 480 | 14:10 / 12:12, 20:12 | 1 |
| 721 | 721 | 240 | 13:35, 17:35 / 15:08, 19:08 | 1 |
| 722 | 722 | 60 | :33 / :42 | 2 |
| 723 | 723 | 120 | 13:15, 15:15, 17:15, 19:15 / 12:40, 14:40, 16:40, 18:40, 20:40 | 2 |
| 724 | 724 | 120 | 13:30, 15:30, 17:30, 19:30 / 12:30, 14:30, 16:30, 18:30, 20:30 | 1 |
| 725 | 725 | 240 | 14:30, 18:30 / 12:03, 16:03, 20:03 | 1 |
| 725 | 725 Vlčí Pole | 480 | 15:30 / untimed | 1 |
| 726 | 726 | 120 | 12:45, 14:45, 16:45, 18:45, 20:45 / 13:25, 15:25, 17:25, 19:25 | 1 |
| 728 | 728 | 120 | 13:45, 15:45, 17:45, 19:45 / 12:08, 14:08, 16:08, 18:08, 20:08 | 2 |
| 729 | 729 | 240 | 12:45, 16:45, 20:45 / 13:43, 17:43 | 1 |
| 730 | 730 | 480 | 16:15 / untimed | 1 |
| 731 | 731 | 120 | 13:45, 15:45, 17:45, 19:45 / 13:33, 15:33, 17:33, 19:33 | 2 |
| 732 | 732 | 120 | 13:19, 15:19, 17:19, 19:19 / 13:48, 15:48, 17:48, 19:48 | 1 |
| 733 | 733 | 120 | 12:22, 14:22, 16:22, 18:22, 20:22 / 13:35, 15:35, 17:35, 19:35 / 12:04, 14:04, 16:04, 18:04, 20:04 / 12:35, 14:35, 16:35, 18:35, 20:35 | 2 |
| 734 | 734 | 240 | 15:10, 19:10 / 15:36, 19:36 | 1 |
| 735 | 735 | 240 | 14:05, 18:05 / 15:04, 19:04 / 12:10, 16:10, 20:10 / untimed | 1 |
| 736 | 736 | 120 | 13:50, 15:50, 17:50, 19:50 / 12:07, 14:07, 16:07, 18:07, 20:07 | 2 |
| 737 | 737 | 60 | :30 / :30 | 2 |
| 737 | 737 direct | 60 | :00 / :00 | 2 |
| 738 | 738 | 120 | 13:15, 15:15, 17:15, 19:15 / 12:05, 14:05, 16:05, 18:05, 20:05 | 1 |
| 739 | 739 | 120 | 12:35, 14:35, 16:35, 18:35, 20:35 / 12:26, 14:26, 16:26, 18:26, 20:26 | 2 |
| 763 | 763 | 120 | 12:35, 14:35, 16:35, 18:35, 20:35 / 13:43, 15:43, 17:43, 19:43 | 1 |
| 764 | 764 | 240 | 14:35, 18:35 / 12:25, 16:25, 20:25 | 1 |
| 766 | 766 | 120 | 12:40, 14:40, 16:40, 18:40, 20:40 / 13:02, 15:02, 17:02, 19:02 | 1 |
| 767 | 767 | 240 | 14:30, 18:30 / 15:29, 19:29 | 1 |
| 768 | 768 | 120 | 12:15, 14:15, 16:15, 18:15, 20:15 / 13:14, 15:14, 17:14, 19:14 | 1 |
| 768 | 768 Byšice | 120 | 13:20, 15:20, 17:20, 19:20 / 12:19, 14:19, 16:19, 18:19, 20:19 | 1 |
| 775 | 775 | 120 | 12:35, 13:35, 14:35, 15:35, 16:35, 17:35, 18:35, 19:35, 20:35 / 12:39, 13:54, 14:39, 15:54, 16:39, 17:54, 18:39, 19:54, 20:39 | 3 |
| 540345 | 540345 | 480 | 12:25, 20:25 / 14:20 | 1 |
| 727 | – (not modelled) | | | 0 |
| 769 | – (not modelled) | | | 0 |
| **Total** | **55 Simutrans lines** | | | **93** |

## Owner checks

1. **427, 738, 763, 775:** Three stops left as coverage exceptions, each within 1 km of a stop the sheet serves: Kosmonosy, Průmyslová (378 m from Kosmonosy, Transcentrum; shift trips 427 13:13 and 14:36, 763 13:28, 775 14:17), Horní Bukovina, odbočka (795 m from Horní Bukovina, Dolní Bukovina) and Klášter Hradiště nad Jizerou, pod pivovarem (56 m from Klášter Hradiště nad Jizerou), the last two served only by 738 Dolní Bukovina 14:25 → Mnichovo Hradiště. *Option:* Serve them: 738 Dolní Bukovina every 480 on the real Mnichovo Hradiště 14:05 → Dolní Bukovina 14:25 → Mnichovo Hradiště 14:35 (+1 bus), and 427 Mladá Boleslav every 480 on the real Mladá Boleslav 14:30 → Kosmonosy, Průmyslová → Mimoň, autobusové stanoviště with an empty return (+1 bus): +2 buses.
2. **722:** Approximate: hourly Mnichovo Hradiště :33 / Český Dub :42 (2 buses); the real 15:23 and 14:32 are 10 min off their slots and there is no 17:33 or 17:42, so the 15:33 window slot has no trip. *Option:* Every 120, Mnichovo Hradiště :33 even hours (12:33, 14:33, 16:33, 18:33 all exact) and Český Dub :42 odd hours (13:42, 15:42), exact in the window but half the real service: 1 bus (one fewer).
3. **737:** Approximate: two hourly lines, 737 via Čistá (Mladá Boleslav :30, Bělá :30) and 737 direct (:00 / :00), 4 buses; the real minutes drift by 5–30 min (Mladá Boleslav 13:45, 14:15, 16:55, 17:20, 17:50; Bělá 14:10, 17:25; 13:50 and 13:20 are 20 min off, the 16:30 direct trip 30). *Option:* Only 737 via Čistá hourly (2 buses, two fewer); the direct trips (Mladá Boleslav 14:15, 15:00, 16:00, 16:55, 17:50; Bělá 13:20, 14:10, 15:00, 16:30) listed, their stops are all on 737.

## Coverage (Step 9)

- 673 stops served 13:00–19:00 by this oblast’s lines; 670 on its Simutrans lines; uncovered 3, each a coverage exception: Kosmonosy, Průmyslová (Factory stop by the Škoda works, 378 m from Kosmonosy, Transcentrum (315, 714, 736); served 13:00–19:00 only by four shift trips (427 13:13, 14:36; 763 13:28; 775 14:17). On the owner checks.); Horní Bukovina, odbočka (Roadside stop 795 m from Horní Bukovina, Dolní Bukovina (738); served 13:00–19:00 only by the 738 short trip Dolní Bukovina 14:25 → Mnichovo Hradiště. On the owner checks.); Klášter Hradiště nad Jizerou, pod pivovarem (56 m from Klášter Hradiště nad Jizerou (427, 715, 738); served 13:00–19:00 only by the 738 short trip Dolní Bukovina 14:25 → Mnichovo Hradiště. On the owner checks.)
- Every stop of okres Mladá Boleslav and every stop outside the Středočeský kraj is on a modelled line or one of those three exceptions (run_oblast: 0 uncovered of other okresy, 0 outside the kraj).
- **Stops of other Středočeský okresy that only this oblast’s lines serve** (for the `--final` cross-sheet pass; all are on a Simutrans line here):
  - okres Mělník: Cítov, Mělnická (467); Cítov, Roudnická (467); Stránka, Ostrý, rozcestí (728)
  - okres Nymburk: Lysá nad Labem, Byšičky (431 Stará Lysá); Lysá nad Labem, Dvorce (431, 431 Stará Lysá); Lysá nad Labem, Ke Karlovu (431 Stará Lysá); Lysá nad Labem, předměstí (431, 431 Stará Lysá); Lysá nad Labem, rozcestí Dvorce (431, 431 Stará Lysá); Stará Lysá (431, 431 Stará Lysá); Stará Lysá, hostinec (431, 431 Stará Lysá); Stará Lysá, Čihadla (431, 431 Stará Lysá)

## Bunching scan (shared stops, same first road, within 2 min)

Every model departure 12:00–20:00 at every first stop, against the other Simutrans lines leaving the same stop by the same next stop:
- Mladá Boleslav, autobusové stanoviště: 712 and 763 at :35 even hours (real together at 14:35; the model repeats it at 16:35 and 18:35), 728 and 731 at :45 odd hours (real together at 17:45; 13:45, 15:45, 19:45 are one real departure and one pattern repeat), 699 and 767 at 14:30 (real), 719 and 729 at 16:45 (real), 724 and 725 Vlčí Pole at 15:30 (real). Each pair shares only the first one or two stops (Jaselská VZP or U Sportu) before the lines part; the repeats come from exact real minutes on two-hourly patterns, and moving one line would leave its real minute, so they are kept (owner, 30 Oct: fit the real timetable).
- Mnichovo Hradiště, dopravní terminál: 721 15:08 and 734 15:10 (both real).
- Interleaving made on purpose: Praha, Černý Most towards Turnov :15 every hour from 720 (13:15, 14:15, 17:15, 18:15), 700 (15:15) and 730 (16:15), as in reality; 737 via Čistá :30 and 737 direct :00 at both ends; 768 Kojovice :15 even and 768 Byšice :20 odd at Benátky; 714 (14:30) and 714 Sobotka (13:05) at Mladá Boleslav; 725 (14:30, 18:30) and 725 Vlčí Pole (15:30, every 480 so that it never meets 725).

## Script problems seen

- Keys used that the HKO README section does not list: `stops` (an explicit stop list for a leg; 442 Dražice) and `starts: true` (only trips that start at `fr`; 734’s way back on 733, 431 Stará Lysá at Stará Lysá, Čihadla). Both are read by `05_schedule.py`.
- `pid-regional/scripts/run_oblast.py` line 40 had an f-string broken across two lines (`print(f"` + newline) from about 05:20, so every run failed with "unterminated f-string literal". I ran a corrected private copy for the first draft only; the coordinator then fixed the script and every later run (including the final one) used the original. Not patched by me.
- `05_schedule.py`: an untimed leg with no trip between its terminals (700 and 730: their returns start at Tanvald / Vítkovice, hotel Praha, not at the outer terminal) gets the stops `[fr, to]` only; harmless for coverage here (the out legs cover the stops), but the card shows a 2-stop empty return.
- `05_schedule.py`: a leg’s running time is the median of all its own full trips near the window, so a leg whose slot trip runs a short road mixes in the long-road trips (442 Dražice: 9 / 10 min instead of 6 / 8, which broke the real 1-minute turns and cost 2 extra buses; 714 Sobotka: 68 / 42 instead of 61 / 48). Set by hand (`rt`, and `stops` for 442 Dražice) and said in the whys.
- `03_read.py` chain test: at Praha, Černý Most the same-line "chains" (315, 345, 405) only show that arrival and departure minutes coincide in an hourly timetable; they cannot tell a 0-minute turn from a bus that waits a period. Left at the 3-minute minimum and put to the live map.
- The live map poll of 2 Nov was still in its morning when this was designed; the "afternoon buses" sections of the readings are empty, so no plate chain was used.

## Open questions (for the 2 Nov live map, not owner checks)

- 0-minute turns at Praha, Černý Most: 315 (8 buses → 7), 345 (5 → 4), 405 (4 → 3) if the arriving bus leaves on its arrival minute.
- 737 / 732 at Čistá, hřiště and 767 / 699 at Bezno: same buses? (would make 732 part of 737, and the Krpy shuttle part of 699’s day).
- 737 → 775 at Mladá Boleslav (5 of 15 departures), 467 → 699 (7 of 9) and 467 → 724 (5 of 10) at Mladá Boleslav, 713 ↔ 718 at Sobotka (2 of 6).
- 427: where the Mimoň 15:35 and 17:50 buses come from (the model runs one bus on the 15:25 / 16:35 round).
- 720 Turnov trips (Praha 12:15, 16:45; Turnov 12:25, 13:25, 15:25) and 733 at Turnov, Na Lukách (2 of 4 720 arrivals followed by a 733 departure).
