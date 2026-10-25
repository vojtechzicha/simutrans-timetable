# Local rail lines

> **ARCHIVED (user, 9 Oct 2026):** both sheets are done and moved to `archive/`: `Local Trains 010 062 064 260.html` (hand-written) and `Local Trains 012 014 210 212 235.html`. `build_012_014_235.py` now writes into `archive/`. Both artifacts are left as they were: KXnUf8bh9Ck1W2xBiJuSQR at version 9 and CCNUijhQeBxE244KKbKyF3. Don't continue them unless the user brings them back. Work moved on to R49 and the local trains around Benešov.

Os/Sp lines designed with `../rail-design-rules.md`. Data: `../md-cr/data/derived/trains.json` (CIS JŘ JR2026). A train counts only if it runs on all five days Mon–Fri 5–9 Oct 2026.

`check_track.py` (25 Oct 2026) lays a sheet's lines out as the game runs them and flags trains that meet where the real timetable never has a meeting (single-track conflicts); see its docstring. `check_followers.py` (same day) lists, for every timing point, the closest faster real train behind it (the follower check of the S9 sheet, which had been only in a scratchpad).

## S9 · S2 · R49 · R17 · Ex7 (16 Oct 2026, current)

`python pipeline/local-rail/build_s9_s2.py` writes `S9 S2 R17 R49 Ex7.html` in the project root. Artifact: https://claude.ai/artifact/KRDg2WHmtB5D5SV88D8Ptp

User (16 Oct 2026): one sheet with S9/R17/R49/Ex7, keep the existing variants and add a version for the current Uhříněves – Říčany works for each; model S9 together with S2 "with more timetabled stops in good passing loops (otherwise it is too fast - similar problem to S4)". The game's S9/S2 (Os221/1, Os221/2, Os231/1, Os231/2) "were done without looking at timetable".
- R17 and Ex7 are imported from build_ex7_r17.py, R49 Tábor / Olbramovice from build_benesov.py (unchanged designs; the 220/222/223 locals stay archived).
- S9 Benešov (2549/2548, every 30, 5 veh), S9 Milovice (9147/9142 Milovice – Strančice, every 30, 7), S2 Kolín (25837/25840, 6-min real Kolín turn, no depot stop, 4), S2 Nymburk (4-leg circuit 5831/5838/5843/5850 through both real alternating patterns, every 120 step 60, 3). Total 31.
- Timing points ('TP') only at stations with loops where no faster train follows within ~6 min (scratchpad follower check: next same-direction train at the station, and whether it overtakes). E.g. S9 Benešov towards Praha not timed after Říčany (R49 2478/2480 closes to 1 min at Hostivař).
- Works (PID + ČD VJR-vlaky-221, workdays 12 Oct – 3 Nov, 5:20 – 21:30): S9 Os 91xx cut at Uhříněves (same minutes; PDF arrival 16:52), R49 out (and Sp 2474 in) add Kolovraty + Strančice stops, morning R 728/730/732 add Říčany. Copies `'<train> výluka'` in load(); 'temporary' lines S9 Milovice / R49 Tábor / R49 Olbramovice "until 3 November". S9 Benešov, R17, Ex7, S2 unchanged. `single_track()` lists Uhříněves – Říčany occupancy: 3 opposite-direction overlaps an hour at real minutes (hence ČD's 5 – 10 min delays).
- The one same-minute flag is real: Ex7 and S9 Benešov both leave Praha hl. n. at :21 (parallel tracks to Hostivař).
- XS9 (user, 16 Oct 2026: add it, "use the actual vypravenost", else the real operator's bus): synthetic legs `XS9_OUT` / `XS9_IN` (Háje 15:02, Říčany 15:55; PID JR-linka-XS9 PDF images, same minutes in PID GTFS L2209 of 16 Oct). Every 15, 5-min min turn, 6 buses; 'temporary' (not in totals). No real vypravenost: seznam-autobusu.cz has 0 XS9 records (2026 and Nov 2025), GTFS has no blocks; carrier is ČD, subcontractor unpublished. Bus: MAN Lion's Intercity LE 12 PID grey-red (pakset session's pick). The save has an empty placeholder line 100999 {XS9}.
- Page has a "What the works are" section (D0 crossing near Říčany; back from the 2025 temporary alignment; single track Uhříněves – Říčany).
- Save export: the simutrans-122-0 session can export the save to JSON (`-load NAME -export`, see the fork's CLAUDE.md).
- **Method check 25 Oct 2026** (`method-check-2026-10-25.md`): no entry or vehicle changes. Added: the Kolín – Velký Osek works note on S2 Kolín (12 Jan – 11 Dec 2026, S2 skips Kolín-Zálabí and Veltruby workdays 6–20; CIS JŘ already has Os 25837 / 25840 passing them), R 326 / 324 from Gmünd in R17's real trains (svc None at their Austrian first stop, so the svc-17 inventory missed them), SC 500, and S3/S30/S34/R43/R21, Ex3/Ex6/EC, R9/R18/R19 in the "other lines" bullet. Uhříněves – Říčany works still in force (pid.cz, 25 Oct).

## Ex7 + R17 Praha – Tábor – Veselí nad Lužnicí (14 Oct 2026, superseded by the S9 · S2 sheet)

`python pipeline/local-rail/build_ex7_r17.py` writes `Ex7 R17 Praha Veselí.html` in the project root. Artifact: https://claude.ai/artifact/Efb4CMZVvtNDZj7rsB5Wr5

User (14 Oct 2026): "Research Ex7 and R17 - but for both the track ends in Veselí nad Lužnicí; neither has access to depot unless you have concrete evidence of one in Prague." CIS JŘ has no empty runs for either (all start/end at Praha hl. n.), so no depot.

| Line | Every | Vehicles |
|---|---|---|
| R17 Praha :46 → Veselí :19; Veselí :38 → Praha :10 (Benešov, Tábor timed; 19 min Veselí, 36 min Praha) | 60 | 4 |
| Ex7 Praha :21 → Veselí :34; Veselí :23 → Praha :39 (Tábor timed; 49 min Veselí, 42 min Praha) | 60 | 4 |

- Ex7 passes Veselí without stopping; the script's `load()` wrapper adds Veselí as a stop at the real passing minute from the CIS location list (only in this script).
- Vehicles: loco + coaches; RAILL 193 since 14 June 2026, ČD 380 before (vagonweb). R17 "Lužnice" trains to České Velenice change to a 754 at Veselí.
- 25 Oct 2026 (method check): R17 `extra_real` lists R 326 / 324 Gmünd – Praha (Veselí 12:38 / 18:38, the line's minutes; no CIS line number at their first stop). SC 500 (Praha 20:31 → ČB, stops at Veselí) and the Praha-approach trains added to Not modelled; works re-checked on pid.cz. No entry or vehicle changes.

## Trains from S4 to the S3 corridor (14 Oct 2026, current)

`python pipeline/local-rail/build_s4.py` writes `Trains S4 to S3.html` in the project root.

Scope (user, 14 Oct 2026): "finish all pid trains and related branch lines with what's missing (it should be the S4 - S3 corridor ...) The main tracks are built all the way to Usti (so include even some fast trains)".
- **What the game already has:** the pak128 session exported the save (FORK-CZR-VZ.sve, 19:44, 161 rail lines with vehicles). S3, S30, S34, R43, R21, S35, R22 and the whole east sector already run there; this sheet adds only what is missing.
- **Fast trains:** R20, Ex5 and R15 cut at Ústí hl. n. ("only in praha-usti sense"). R23 runs Kolín – Ústí in full.
- **Depot:** R20 and Ex5 run from and to Praha Jih, on the real empty-run minutes ("should definitely go to Praha jih"). Praha Jih is the depot the R9/R19 sheet calls Praha odstavné nádraží.
- **Track:** Mělník – Štětí – Ústí západ, Neratovice – Všetaty – MB and Mělník – Mšeno are built. The Lovosice branches are not.
- **Left out:** S22 has no afternoon trains (S9 Milovice covers it), S27 is out by the user's choice, and Mšeno has no workday trains.

| Area | Line | Every | Vehicles |
|---|---|---|---|
| S4 + fast | S4 Praha-Bubny – Kralupy (471) | 60 | 2 |
| | S4 Ústí Praha-Bubny – Ústí hl. n. (640.2; CIS 1004 / 4004; primary of the coupled pair) | 60 | 5 |
| | S4 Ústí 2nd unit Bubny – Kralupy (640.2, fork coupling: parts at Kralupy towards Ústí, couples there towards Praha, coupled through Bubny) | 60 | 2 |
| | R20 Praha Jih – Praha hl. n. – Ústí (162 + push-pull) | 60 | 5 |
| | Ex5 rj "Berliner" Praha Jih – Praha hl. n. – Ústí (193 + ComfortJet) | 120 | 2 |
| | R15 Praha Jih – Praha hl. n. – Ústí (193 + InterJet; depot runs copied from Ex5's real minutes in the other hours) | 120 | 2 |
| Right bank | R23 Kolín – Mělník – Ústí hl. n. (RegioJet 665; stables at Ústí západ between trips, as the real train does: empty runs of 3 min, times designed) | 120 | 3 |
| | S32 Lysá – Mělník – Ústí západ (162 + Bdmtee) | 120 | 2 |
| | U32 Ústí západ – Štětí (same set) | 120 | 1 |
| Neratovice | S43 Kralupy – Neratovice (810; 8 / 5-min turns) | 60 | 1 |
| | S23 Čelákovice – Brandýs – Neratovice (810; crossing at Brandýs) | 60 | 2 |
| | **Total** | | **27** |

- **Ex5 data:** the trains run under a Tue–Fri record and a Monday record (Monday works in Germany, ending at Děčín). Their Holešovice – Ústí minutes are the same, so `load()` merges them; otherwise neither record counts as all-five-days.
- **Masarykovo closure:** S4 starts at Praha-Bubny. The ČD works timetable (cz-k120-2026vyluka03) names S4 but prints no S4 times, so the annual Bubny minutes are used. R42, which the user built by hand, is also on PID's list: its first two morning trains from Praha and first three afternoon trains into Praha start and end at Praha-Vysočany.
- **v2 (user, 14 Oct 2026):** "Bubny can have 4 trains max", "use [coupling at Kralupy] smartly", "R15 should go to Praha jih", and "Usti also can store trains at its depot run (11 minutes)". A minute-by-minute count over 2 h shows Bubny holds at most 2 trains; v1's "four or five" was wrong. The S4 shorts can't share the coupled unit, because the fork parts a pair only where the next stops differ, and S4 and S4 Ústí stop identically between Bubny and Kralupy. The pak128 session confirmed that line coupling ignores vehicle constraints. The synthetic depot legs come from `DEPOT_RUNS` in `load()`. v3: "R23 in reality goes back to západ to stable then returns to hl.n." R23 now uses Ústí hl. n. L:31 → Ústí západ L:34, then S:20 → hl. n. S:23. The S4 coupling engine work went to session simutrans-122-0-36, with R18/1 and R18/2 as the regression case.
- **v6 (user, 15 Oct 2026, from the built game):** S4 Ústí reached Lovosice 21 min and Kralupy 36 min before departure. The CIS departures were checked for every train of the day (Ústí :05, Lovosice :29 out / :31 in), and the line got `TP` timing-point `wait_points` at real minutes. Towards Ústí: Nelahozeves :30, Vraňany :38, Hněvice :53, Roudnice :03. Towards Praha: Bohušovice :39, Roudnice :52, Hněvice :02, Vraňany :17, Nelahozeves :25. Outbound they stop at Roudnice because R15 / Ex5 (not timed before Ústí) follow and overtake at Lovosice. Inbound, R20 is timed at Lovosice :57 and overtakes at Kralupy. U54 (4054) was not added: it has no afternoon pattern.
- **Checked against the save:** R23 at Kolín and Nymburk does not collide with S2 (Os231/1, /2) or R22.
- 25 Oct 2026 (method check): no entry or vehicle changes. Added to Not modelled: S49 (1049) on Praha-Podbaba – Roztoky, Sp 1494 / 1495, R49 on hl. n. – Holešovice, and U52 (4052, every 2 h Lovosice – Ústí, comes off the unbuilt Libochovice branch; moved out of "Beyond Ústí"); works re-checked on pid.cz. `check_track.py build_s4`: no meetings outside real crossing places.

## Trains from S5 to the S4 corridor (14 Oct 2026)

`python pipeline/local-rail/build_s5.py` writes `Trains S5 to S4.html` in the project root. Artifact: https://claude.ai/artifact/9V24sqWFpnjztqobgL1CLP

Scope (user, 14 Oct 2026): "Now do the S5 (included) to S4 corridor (excluded)". Asked: the PID core plus all four outer groups; "The track ends in Blato u Jesenice, rest should be in full". 4021 runs every 72 (user's choice; one unit, no clock-face). `base.FULL` is extended only inside this script (Kralupy nad Vltavou, Praha Masarykovo nádraží), so the other sheets rebuild unchanged.

| Area | Line | Every | Vehicles |
|---|---|---|---|
| S5 family + S54 | S5 + S45 Praha-Bubny – Kladno – Kralupy (814; S5 to Kladno-Ostrovec runs through as S45 on workdays) | 60 | 4 |
| | S45 Kladno – Kladno-Ostrovec shuttle (814) | 120 | 1 |
| | R45 Praha-Bubny – Kladno-Ostrovec (814.2; 14 min at Bubny) | 120 | 1 |
| | S50 Kladno – Rakovník (814; 1 h 44 at Kladno forced) | 120 | 2 |
| | R24 Praha-Bubny – Rakovník (Arriva 845; 15 min at Bubny) | 120 | 2 |
| | S54 circuit Hostivice – Noutonice / Středokluky (810; 3-min turn Noutonice) | 120 | 1 |
| Rakovník | S57 Rakovník – Blatno (KJŘ 161 cut at Blatno; hourly Os 16716 :48 / Os 16773 :53, crossing at Oráčov; 810/814) | 60 | 2 |
| | U12 Rakovník – Most (KJŘ 126 cut at Most, game track end; DLB 654; hourly Os 6718 :09 / Os 6711 :03 from Most, crossings Svojetín, Hřivice, Lenešice; reverses Louny) | 60 | 4 |
| | Os Lužná – Jirkov (KJŘ 124, DLB 654; 6-min Jirkov turn) | 120 | 2 |
| | U13 Most – Žatec západ (KJŘ 123 in full, RegioJet ÚK 654; hourly Os 6519 Most :42 / Os 6520 Žatec západ :30, crossing at Volevčice, timed Obrnice out and Počerady in; real 5-min turn at Žatec západ; added 15 Oct) | 60 | 2 |
| Kralupy | S40 Louny (814 out, 810 back, so separate from S40) | 120 | 3 |
| | S40 Kralupy – Slaný | 120 | 2 |
| | S44 Kralupy – Velvary (810; 4-min Velvary turn) | 60 | 1 |
| Straškov | Os Vraňany – Straškov / Horní Beřkovice circuit (841) | 120 | 1 |
| | Os Roudnice – Bříza obec (841) | 72 | 1 |
| | **Total** | | **29** |

- **Engineering works (v3, user 14 Oct 2026):** Masarykovo nádraží is closed 1 Jun – 12 Dec 2026, so S5 + S45, R45 and R24 start and end at Praha-Bubny. The ČD works timetable (cz-k120-2026vyluka03) keeps the annual minutes from Bubny. R45 and R24 also stop at Praha-Výstaviště, added in the script's `load()` wrapper at the passing minute; R24's Bubny and Výstaviště minutes were confirmed on 14 Oct by Arriva's works timetable linked from PID (Bubny L:03, Výstaviště L:06; back Výstaviště S:46, Bubny S:48). Not modelled (user: "don't do those ending in early november"): U14 Měcholupy – Žatec by bus until 9 Nov, and S75 Rakovník – Roztoky by bus until 8 Nov.
- **S57 and U12 simplified (v4, 14 Oct 2026):** the user asked, relayed by the pak128 session, to "simplify the S57 and U12 lines - pick the best pattern to be more uniform" (S57 = 1057, U12 = 4012). Both now run every 60 on one real pair that crosses at real crossing stations every hour; before, they were 2-hourly circuits through all the real families (4 and 5 vehicles). `check_meetings.py` (out train vs. the back train repeated every hour, on single track) found S57 pairs that work: 16716 × 16773 (Oráčov, used, 8 min at Rakovník), 16774 × 16719 (Pšovlky, the alternative on the page, 9 min at Blatno), 16718 × 16773 and 16776 × 16721 (both Pšovlky). For U12 to Osek only 6714 × 6707 worked hourly. v5 (user, 14 Oct 2026: "now U12 I have built only to Most"): U12 is cut at Most, on 6718 :09 × 6711 :03 from Most (also crosses cleanly; 6714 × 6707 is the other option), 4 vehicles, sheet total 27.
- Alternatives on the page: S57 on Os 16774 / 16719 (2 vehicles), S40 as one circuit (4 instead of 5).
- **U13 added (v6, 15 Oct 2026):** the user asked "then add to it U13 in full?". U13 = CIS 4013 Most – Žatec západ, the whole line, every 60 on Os 6519 / 6520 (`check_meetings.py 6519 6520 Most "Žatec západ" 60`: crossing at Volevčice). The save has an empty placeholder Os123 [U13]. The U12 trains outside the pattern on Most – Obrnice are listed (LISTED pair). R25, U52 (4052) and 4011 also use parts of the line; they are not on the sheet. Sheet total 27 → 29, artifact version 8.
- Half-minute arrivals matter for tight turns: Vraňany is in 15:35½, out 15:41, so the turn is set to 5 (with 6 the builder adds a whole interval).
- **S40 corrected (method check, 25 Oct 2026):** `rep_in` 9735 (Slaný 16:29) → 9711 (Slaný 14:31). With :29 the back train left Kralupy předměstí (:56) before the S:54 from Kralupy (Os 9712) got there (:57½), so they met on the single track Kralupy – předměstí (`check_meetings.py 9712 9735 "Kralupy n.V." Slaný 120`: CONFLICT; 9712 × 9711: cross at předměstí, as every real pair does). In-game change: S40 Slaný entry offset 89 → 91 (S:29 → S:31); still 2 vehicles, 29 in all. Also listed: S54 bus 26 – 30 Oct (pid.cz), Os 19746.
- Not modelled: R45 Praha-Bubny peak trains (incl. Sp 1576 to Blatno), single Sp to/from Blatno, S5/S45/S50 off-pattern and morning trains, S54 Bubny pair and weekend Slaný extension, S40 16–19 peak extras, shorts on 4012/4014/4021/4022, no-workday branches (Kralovice, Kolešovice, 4105, Zlonice – Straškov).

## S75 Beroun – Křivoklát – Rakovník (13 Oct 2026, current)

`python pipeline/local-rail/build_s75.py` writes `S75 Beroun Rakovník.html` in the project root. Artifact: https://claude.ai/artifact/8Ci1ZEfk4aNP89HntfvTbH

Scope (user, 13 Oct 2026): "continue with trains north of Beroun up to S5 (excluding it)". Asked the follow-up: "Only S75 Beroun – Rakovník", and all track is built in the game.
- In JR2026, S5 is Praha Masaryk. – Kladno – Kralupy (1005/1045, R45 = 1145). The user counts Kladno – Rakovník (S50 = 1050, R24) as the S5 family, so it is out.
- Also out: S54 Hostivice – Středokluky – Noutonice, and all lines beyond Rakovník.

| Line | Every | Vehicles |
|---|---|---|
| S75 Beroun – Rakovník (847 RegioFox) | 60 | 3 |

- Pattern: Beroun :59, Rakovník :56. This is the afternoon peak: 14:59, 15:59, 16:59 out; 14:57 and 15:56 back. The two directions cross at Zbečno, where the train to Rakovník waits :22 – :26 (timed as a wait point).
- The turns are 10 min at Beroun and 59 min at Rakovník. The alternative :12 return crosses at Roztoky and needs 3 vehicles too, but puts 54 min at Beroun, so it was rejected under the short main-line stay rule.
- The real line is irregular outside the peak; all those trains are listed under Not modelled.
- **Corrected 25 Oct 2026 (method check):** `rep_out` 7717 → 7745. 7717 reaches Rakovník at :57, after the :56 back leaves, so the documented pattern met on the single track Chlum u Rakovníka – Rakovník (`check_meetings.py 7717 7718 Beroun Rakovník 60`: CONFLICT); 7745 (14:59 → 15:55) crosses only at Zbečno. No in-game change (Beroun :59, Zbečno :26, Rakovník :56, 3 vehicles); Zbečno stay 4 → 3 min, Rakovník 59 → 61 min on the page. Works now listed: Rakovník – Roztoky by bus 29 Sep – 8 Nov (not modelled, owner rule of 14 Oct), Rakovník – Blatno by day 19 – 31 Oct; Kralovice (S58) as a no-workday branch.

## Trains west of Praha: S7, Liteňka, S6, S65, Beroun – Plzeň, Příbram line, R16, R26 (10 Oct 2026, ARCHIVED 13 Oct)

**13 Oct 2026 (user):** "in game we have some specialities - the tracks end at Rokycany, Blatná and Čimelice". The lines that went further now end there, at their real minutes. They use `cut` legs of the real trains, plus a new per-line `cut_at` so that through trains still count as the line's real trains. In the shared builder, `lab()` also shows a train's time at the leg's start.
- Dropped as wholly beyond the track: Os Rokycany – Příkosice and Os Blatná – Strakonice.
- I assumed the Mirošov branch is not built. If it is, re-add `p175`: svc 3221, every 60, rep 27818/27821, turns [8, 12], 1 vehicle, and put 3221 back in `LOCAL`.
- 43 → 33 vehicles. Then the user said "I'm missing trains to Rožmitál". Březnice – Rožmitál has no workday trains in JR2026, only weekend and holiday trains from 25 Apr to 28 Sep, so the workday inventory couldn't see it. It was added as a `season` line, then removed at the user's request: "If rožmitál has no weekday service, it should not be in". It is now listed under Not modelled. Total 33. The sheet was archived the same day: it is in `archive/`, and the artifact is at v8. Also fixed: S60 leaves Březnice towards Beroun at L:43, not L:42.

**15 Oct 2026 (user): the Praha-Smíchov works, modelled ("I want to model both please - you need to validate that in Zlíchov only one vehicle occupies the track").** The user asked for this although the S6 closure ends on 19 Oct; it overrides the S5-sheet rule "don't do those ending in early november" for this sheet.
- S6: Praha-Smíchov – Praha-Zlíchov closed 1 Jul – 19 Oct 2026, 21:00 (PID; ČD works timetable cz-k173-2026vyluka07, no replacement). Every train starts and ends at the temporary stop Praha-Zlíchov. The CIS data already has Zlíchov as a passing point at the works minutes (:48 out, :08 / :38 in), so `load()` in build_beroun.py swaps the Smíchov terminus for it.
- S65: Praha-Smíchov – Praha-Zličín closed 13 Aug – 30 Nov 2026, trains cancelled without replacement (ČD closure 22963; no works PDF exists for it). `load()` cuts every 1065 train at Praha-Zličín, at the annual minutes.
- Checked: all 95 S6/S65 workday trains match the PID GTFS of 29 Sep (Wed 7 Oct) to the minute.
- S6 is now **one line** for the Beroun and Nučice trains (legs 19916, 19923, 19966, 19967; Zlíchov terminal, 10-min turns). Two separate lines would put two trains at Zlíchov for 10 min every half hour. vagonweb backs the shared line: 847 006 + 847 018 ran Os 19923 and then Os 19968 on 4 Jun 2026. This replaces the earlier "offered but not done" note.
- `one_at_a_time()` checks Praha-Zlíchov, the Hlubočepy – Zlíchov track and Praha-Zličín over 13:00 – 16:59 and stops the build on a clash. Result: Zlíchov :08 – :18 and :38 – :48; Zličín :36 – :19.
- Vehicles: S6 5 → 4, S65 3 → 2, so the sheet total is 33 → 31. Republished as artifact v9.
- Not modelled: the short S7/R16 works at Smíchov (20 Oct – 13 Nov, a few days each).
- **Final S6, the same day (user: "prepare the final S6 after exclusion but with the combined line"):** `S6_WORKS = False` in build_beroun.py. S6 runs from Praha-Smíchov at the annual minutes and stays one combined line. Turns are `[10, 5, 10, 5]`, so it stands 5 min at Smíchov (in :11 → out :16, in :41 → out :46) instead of 35. Still 4 vehicles. The vagonweb sighting is exactly this turn (Os 19923 in 17:11, Os 19968 out 17:16). `inv_svcs={'1006'}` stops S7 trains from counting as Smíchov – Beroun stretches. The Zlíchov entries are kept in the S6 notes. `S6_WORKS = True` rebuilds the works version, including its Zlíchov checks. S65 stays at Praha-Zličín until 30 Nov; after that, drop the 1065 part of `load()`. Republished as artifact v10, 31 vehicles.
- **Both S6 on one page, the same day (user: "why isn't there big table for S6 befor the end of works?"):** with `S6_WORKS = False`, `load()` also makes Zlíchov copies of the S6 trains (by_num keys `"<train> Zlíchov"`, real numbers kept, not in the workday list so the inventory counts each train once). Line `s6z` "S6 until 19 October" runs on them as a full section (entries, round trip, real trains). It has `'temporary'` (the base builder leaves it out of the area and page totals, and shows "(4, the S6 vehicles, until 19 October)") and `'same_vehicles_as': 'S6'` (grouped with S6 in the same-minute check). The Zlíchov checks in `track_checks()` now always run. Artifact v11, still 31 vehicles.
- **Ex6 to Rokycany (user, 15 Oct 2026: "add me to the latest file Ex6 to Rokycany please"):** the hourly Ex6 path is two lines every 120 with their own coaches. **Ex6 Cheb** is IC Západní expres 55x/56x (legs IC 560 / 561). **Ex6 München** is EC 35x out and alex RE 35x back (legs EC 352 / RE 357). The real trains pass Rokycany without stopping, so `load()` makes copies cut there at the passing minute (keys `"<train> Rokycany"`), and `ex6_real()` fills their real-train lists by direction. The Praha end is real: Vysočany :22 → hl. n. :28 – :35, back hl. n. :21 → Vysočany :34 / :31. The trains turn 21 min at Rokycany and stand 48 / 51 min at Vysočany, with 2 + 2 vehicles. `base.CATS` gets '63' IC and '50' EC. S70 is timed at Hořovice both ways (Ex6 München overtakes it there). Rokycany holds up to 3 trains (L:49 – L:56), Vysočany 1. Not modelled: the Pendolino 503 / 504 and rj 512 / 515 slots. Artifact v12, 35 vehicles.

`python pipeline/local-rail/build_beroun.py` writes `archive/Trains Beroun Plzeň Příbram.html`. Artifact: https://claude.ai/artifact/HopRNc92gS41cs9kQ6jroj

Scope (user, 10 Oct 2026): "S7, Beroun-Plzeň, Beroun-Příbram -> wherever, Liteňka and other trains around it - no need to go north of Beroun and stay west of Vltava". So no Rakovník line, no Ex6/EC on Beroun – Plzeň, no other Plzeň-hub lines (all listed).

| Area | Line | Every | Vehicles |
|---|---|---|---|
| S7 and Liteňka | S7 Praha hl. n. – Beroun (471) | 30 | 4 |
| | S7 Řevnice, Praha-Smíchov – Řevnice (162 + double-deck push-pull, so own line) | 30 | 3 |
| | S76 Liteňka Zadní Třebaň – Lochovice (814; crossing at Všeradice) | 120 | 2 |
| Smíchov | S6 Smíchov – Beroun (847) | 60 | 3 |
| | S6 Nučice (847) | 60 | 2 |
| | S65 Smíchov – Zličín – Hostivice (reverses) – Rudná (810) | 60 | 3 |
| Beroun – Rokycany (cut 13 Oct) | R16 "Berounka" Praha – Rokycany (193 + coaches; 7-min turn at Rokycany joins two real minutes) | 60 | 3 |
| | S70 Beroun – Rokycany (650; 1 h 54 min at Rokycany) | 120 | 2 |
| | Os Hořovice – Rokycany (650; what is left of the Os/Sp chain via Plzeň) | 120 | 1 |
| Příbram line (cut 13 Oct) | S60 Beroun – Příbram – Blatná (814; the real Blatná trains 7914/7913) | 120 | 2 |
| | Os Březnice – Čimelice (814) | 120 | 1 |
| | R26 Praha – Čimelice (Arriva 845; from and to the Praha-Malešice depot, the real peak empty runs) | 120 | 4 |
| Kolín – Čáslav – Havlíčkův Brod (added 10 Oct) | S20 Kolín – Havlíčkův Brod (650.2; 1020, Vysočina part svc None) | 120 | 2 |
| | S20 Čáslav (650.2; the odd-hour trains that end at Čáslav) | 120 | 1 |
| | **Total** | | **33** |

- PID labels from the CIS line number (S6 = 1006, S60 = 1060, S70 = 1070, S76 = 1076). The non-PID lines are named by route.
- Os/Sp Hořovice – Plzeň – Přeštice (user, 10 Oct: "as it truly is in reality"): one line through the real chain of the 650s. Hořovice L:12 → Plzeň (ends), Sp Plzeň S:03 → Rokycany, Sp S:42 → Plzeň, Sp L:03 → Rokycany, Os S:03 → Přeštice, Os L:09 → Hořovice. Plzeň and Rokycany are terminal at each leg start. The minutes allow only this chain. It replaced the first version (Os line waiting at Rokycany plus a separate Sp line), also 3 vehicles.
- R26 Praha end (user, 10 Oct: 1 h at hl. n. too much; then "if the peak vehicle really goes to Malešice, model it even with an extra vehicle"): the afternoon-peak R 1172 / R 1171 run from and to Praha-Malešice (via Vršovice – Eden – Zahradní Město, never Libeň), so the line uses their raw minutes. Depot S:53 → hl. n. L:03 – L:22; hl. n. S:22 – S:29 → Malešice L:01. 5 vehicles; `Praha-Malešice` is in `DEPOTS`. A Vršovice version (v2, 4 vehicles) was replaced.
- S20 (user, 10 Oct: "add Kolín -> Světlá nad Sázavou -> wherever ... just these, no other local branches - only the correct terminus for these trains"): workday Kolín S:34 → Havlíčkův Brod (even hours), L:34 → Čáslav (odd hours); Havlíčkův Brod L:05 → Kolín, Čáslav S:58 → Kolín. Two lines, real termini; Žďár/Jihlava through trains are weekend or morning only. Out: R9, Sp Praha – Kutná Hora, 235 through trains, Čáslav – Třemošnice.
- S60 to Strakonice confirmed (user: "if you truly think the through trains are closer to reality, do it that way"): in the 13–19 window 6 of 8 trains run through, and from Beroun 3 of the 4 afternoon trains go to Strakonice.
- S60 (user asked to reverify): PID S60 = line 1060 = Beroun – Březnice only. Every train runs on as 3160, to Blatná, and about half to Strakonice (Beroun 11:01, 13:01, 15:01, 19:01). In the afternoon 6 of 8 run through, so the line stays Beroun – Strakonice; the page lists all day's ends.
- Done 15 Oct 2026 (see above): one shared S6 line, at Praha-Zlíchov during the works. R26 with the Malešice depot runs would need 5 vehicles.
- Builder additions: `circuit` (stations in leg order), `B` (route label), `cat_of` (Os/Sp per real train), per-line `inv_svcs` (R16/R26 inventory only their own trains), `mid` (a leg boundary that is not a terminus: direction, route and B end run through it), and `dur()` for round trips that are not whole hours (S49 had said "1 h" for 1 h 30). `vagonweb.py` takes the operator as a 5th argument (Arriva = ARV).

## S49 Praha-Hostivař – Roztoky u Prahy (9 Oct 2026, ARCHIVED 10 Oct)

> **ARCHIVED (user, 10 Oct 2026: "archive all (all done)"):** the page is in `archive/S49 Hostivař Roztoky.html` and `build_s49.py` writes there. Artifact EVZrB7zSxCzxEU2rGfsaLk left as published (its round trip label still says "1 h"; the rebuilt file says 1 h 30 min).

`python pipeline/local-rail/build_s49.py` writes `archive/S49 Hostivař Roztoky.html`. Artifact: https://claude.ai/artifact/EVZrB7zSxCzxEU2rGfsaLk

- PID S49 = CIS service 1049. In the morning and afternoon peaks it runs every 30 min the whole way (Hostivař :03 / :33, Roztoky :15 / :45). Outside the peaks only the hourly :33 / :15 trains run to Hostivař; the others turn at Praha-Libeň (listed, not modelled).
- One line every 30, 3 vehicles. Real turns: 12 min at Roztoky, 20 min at Hostivař. Only the termini are timed. Route via Malešice (no stop) – Libeň – Holešovice; no Praha hl. n.
- vagonweb has no composition for S49 numbers, so the unit type is open.
- Builder: interval 30 shows the real time as ":03 and :33 every hour".
- Misunderstanding on the way (user, 9 Oct): "change the local trains to S49" meant this line, not renaming the 220 Os on the archived Benešov sheet. The rename was reverted, and that sheet rebuilds identically.

## R18 Slovácký expres, coupled (9 Oct 2026, ARCHIVED 10 Oct)

> **ARCHIVED (user, 10 Oct 2026):** the page is in `archive/R18 Slovácký expres.html` and `build_r18.py` writes there. Artifact V8hoXRQ3jnL3DbpR941PQ3 left as published. The old RegioJet and Leo Express pages (`regiojet-lines.html`, `leoexpress-lines.html`) moved to `archive/` the same day.

`python pipeline/local-rail/build_r18.py` writes `archive/R18 Slovácký expres.html`. Artifact: https://claude.ai/artifact/V8hoXRQ3jnL3DbpR941PQ3

The real train (vagonweb 2026, every workday R18): a RAILL 193 Praha-Vršovice – Staré Město and a ČD 750.7 Staré Město – Luhačovice. Five coaches run through to Luhačovice; one Bmz runs only to Staré Město. The fork's coupling (engine `CLAUDE.md`, "Coupling trains", R12a/R12b) models it:

| Line | Vehicles in the game | Every | Timed (offset) | Vehicles |
|---|---|---|---|---|
| R18 (primary) | 193 + Staré Město Bmz; Praha odstavné nádraží – Vršovice – Staré Město | 120 | depot S:34 (94), Vršovice S:47 (107), hl. n. S:58 (118), Pardubice S:02 (62), Olomouc L:31 (31), Staré Město L:36 (36, terminal, waits 1 h 18); back Přerov S:15 (75), Olomouc S:31 (91), Pardubice S:00 (60), hl. n. L:11 (11), Vršovice → depot L:21 (21) | 5 |
| R18 Luhačovice (joining) | 750.7 + 5 through coaches; depot – Vršovice – Luhačovice | 120 | same as R18 on the shared part, plus Staré Město out S:33 (93), Luhačovice S:31 (91, waits 1 h 11), Uherský Brod S:57 (117, crossing); **Couple with R18, wait up to 10 min** at the depot entry and at Staré Město towards Praha | 6 |

- The pair stays coupled through the Praha end (same next stops) and parts at Staré Město going out. Under the wire the 750.7 is idle (fork mixed traction). The coaches can't change engine in Simutrans, so the 750.7 rides to Praha, which isn't real.
- Real parity is kept on purpose: Luhačovice out S:31 and Staré Město L:36, both real. With 5-min turns the lines would need 9 vehicles but would run on invented hours.
- Praha end: the real empty runs Praha Jih ↔ Vršovice from the raw CIS locations (`depot_leg`, `{'raw': ...}`).
- Not modelled: the one-a-day R18s (Zlín, Veselí, Přerovský zubr, Olomouc – Luhačovice, early and late ones). The inventory covers only R18 (svc 18) trains (`run(..., inv_svcs={'18'})`).
- Builder additions: `depot_leg` (raw empty runs), `couple` (couple entries shown in the Stay column), `couple_with` (the joining line shares its primary's slots in the same-minute check), and `FULL` "St. Město u U.H.". Archived sheets: only the expanded station name changed in their coverage tables.

## R49 · local trains around Benešov (9 Oct 2026, ARCHIVED the same day)

> **ARCHIVED (user, 9 Oct 2026):** the page is in `archive/Local Trains R49 Benešov.html`, and `build_benesov.py` writes there. The artifact C1sFtgu1AKdCo28ce8FNeb is left at version 6. Work moved on to the R trains to Luhačovice.

`python pipeline/local-rail/build_benesov.py` writes `archive/Local Trains R49 Benešov.html`. Artifact: https://claude.ai/artifact/C1sFtgu1AKdCo28ce8FNeb

The script only holds the design (`LINES`, `LISTED`, `NOT_MODELLED`, `SHARED`, `HEAD`). It builds with `build_012_014_235.run()`, which now takes another sheet's lines and texts; the archived sheet still rebuilds byte-identical. `run(..., along=True)` keeps a train's run unbroken through stations of the sheet's other lines (an Os stopping at Mezno is still on the R49 route).

| Line | Real route (svc) | Every | Timed | Vehicles |
|---|---|---|---|---|
| R49 Tábor | Praha-Holešovice – Praha hl. n. – Benešov – Tábor; back via Malešice – Libeň, not hl. n. (1149) | 120 | Holešovice S:05 (65), hl. n. S:15 (75), Říčany S:38 (98), Benešov L:07 (7) / S:49 (109), Tábor S:05 (65); Holešovice in L:45 | 2 |
| R49 Olbramovice | Praha-Holešovice – Olbramovice, both ways via hl. n. | 120 | Holešovice L:05 (5), hl. n. L:15 (15), Říčany L:38 (38), Benešov S:07 (67) / L:49 (49), Olbramovice L:36 (36, waits 1 h 18), hl. n. back S:41 (101) | 2 |
| 223 Sedlčany | Benešov – Olbramovice (reverses) – Sedlčany (1098) | 60 | Benešov :33, Olbramovice :50 / :25, Sedlčany :53, Štětkovice in :07 (crossing) | 3 |
| 222 Vlašim | Benešov – Vlašim (1099) | 60 | Benešov :32, Vlašim :26, Postupice in :48 (crossing) | 2 |
| 220 Os | circuit Tábor → Olbramovice → Votice → Olbramovice → Tábor (1090) | 120 | Tábor S:39 (99), Olbramovice → Votice L:42 (42), Votice S:11 (71), Olbramovice → Tábor S:42 (102); Olbramovice and Votice terminal | 2 |

- R49 (user, 9 Oct 2026), three rounds:
  - Hourly to Tábor: too many next to R17.
  - Then: "model R49 properly ... Praha-Benešov is more often".
  - Finally: "R49 is clearly hourly between Praha hl.n. and Benešov u Prahy in afternoon peak. You know better about the holešovice mess and what to do after Benešov".
- R49 design:
  - Hourly from Praha-Holešovice :05 (hl. n. :15) to Olbramovice, the real afternoon short terminus (Sp 2481/2480). Olbramovice has room; S9 turns at Benešov.
  - Every other train goes on to Tábor (user, 9 Oct: "continue to Tábor every 120mins - making it far from the local train"). It runs in the even hours: Holešovice S:05 (the real 16:05 and 18:05), Tábor S:05. That keeps it 31–39 min from the 220 Os both ways; odd hours would give only 21–26 min. The real Tábor departures (odd hours) move by an hour.
  - Praha end (user, 9 Oct: "okay with Malešovice bypass if it is in the data"). In CIS JŘ every afternoon R49 to Holešovice runs Hostivař → Malešice → Libeň (7 min, no passengers) → Holešovice (Sp 2478, 2480); so does the early 2473 out.
  - R49 Tábor comes back that way, on the minutes of Sp 2478 (Holešovice L:45, 20 min turn).
  - R49 Olbramovice comes back via hl. n. on the minutes of Sp 2474, so hl. n. keeps an R49 towards Praha every 2 h.
  - Everything out of Praha runs via hl. n. (Sp 2483).
  - The R49 Olbramovice sets wait 1 h 18 at Olbramovice (in S:18, out L:36), because S:36 is R49 Tábor coming through. 2 + 2 vehicles; the sheet has 11.
  - Builder: `{'cut': (train, from, to)}` legs (part of a real train) and `shift` (move a whole line by whole hours).
- The real afternoon R49 trains to Praha skip hl. n. (Říčany → Malešice → Libeň → Holešovice). The page prints a separate "Back:" stations line when the return calls at other stations.
- vagonweb: R49 is filed as Sp "Sázava" (relace CZ-220), and `vagonweb.py` now takes a category and train name (`... CZ-220 2483 Sp Sázava`). It is a 362 locomotive with five coaches; the locals are all planned 841.3.
- Listed, not modelled: R17 and the other long-distance trains, S9 and the other Praha trains, the Os from České Budějovice, Veselí and Jindřichův Hradec that turn at Chotoviny, the R49 short trains, and the early and late Os.

The 010 / 062 / 064 / 260 sheet (`Local Trains 010 062 064 260.html`) was hand-written on 3 Oct 2026 and has no script here.

## 012 · 014 · 235 · Posázavský pacifik 210 · 212 (5 and 8 Oct 2026)

`python pipeline/local-rail/build_012_014_235.py` writes `Local Trains 012 014 210 212 235.html` in the project root (until 8 Oct 2026 it was `Local Trains 012 014 235.html`). Artifact: https://claude.ai/artifact/KXnUf8bh9Ck1W2xBiJuSQR

### Posázavský pacifik (8 Oct 2026)

| Line | Real route (svc) | Every | Timed | Vehicles |
|---|---|---|---|---|
| 210 Čerčany + Čisovice | circuit Praha hl. n. → Čisovice → Praha hl. n. → Čerčany → Praha hl. n. (1088 + 1008) | 240, Also at | Praha → Čisovice 15 (135, 195); Vršovice 30 (150, 210); Čisovice 37 (97, 157); Praha → Čerčany 115 (175, 235); Týnec 53 (113, 233); Čerčany 17 (77, 137); Jílové 63 (123, 183); both Praha entries terminal | 6 |
| 210 Čerčany + Dobříš | circuit Praha hl. n. → Dobříš → Praha hl. n. → Čerčany → Praha hl. n. | 240 | Praha → Dobříš 75, Vršovice 90, Dobříš 186, Praha → Čerčany 55, Týnec 173, Čerčany 197, Jílové 3; both Praha entries terminal | 2 |
| 212 | Čerčany – Zruč nad Sázavou (1080) | 120 | Čerčany L:16 (16), Zruč L:08 (8); towards Čerčany Ledečko S:05 (65), Sázava S:22 (82), Samechov S:38 (98) | 2 |
| 212 Sázava | Čerčany – Sázava (1080) | 120 | Čerčany S:16 (76), Sázava L:22 (22), Samechov towards Čerčany L:38 (38) | 1 |
| 212 Havlíčkův Brod | Zruč nad Sázavou – Ledeč – Světlá nad Sázavou – Havlíčkův Brod (1082) | 60 | Zruč :56 (5 min turn), Ledeč nad Sázavou towards Havlíčkův Brod :31 (9 min, crossing), Havlíčkův Brod :37 | 3 |

- 210 (user, 8 Oct 2026): no long stays at Praha hl. n., and at most one vehicle's worth of Dobříš.
  - 210 is two circuits through Praha hl. n.: in from Čerčany :04 → out to the Dobříš branch :15 (11 min); in from the Dobříš branch :34 → out to Čerčany :55 (21 min). Every 240: Dobříš takes one hour in four, and Čisovice the other three through Also at.
  - Both branches run 847 RegioFox, though vagonweb sightings show the units mostly staying on one branch. The circuit is a game simplification the user chose.
- Variant tried and rejected (9 Oct 2026): separate lines with the real empty runs to the Praha-Libeň sidings (S8: Os 9020 hl. n. 19:14 → Libeň 19:20; Os 9013 Libeň 14:29 → hl. n. 14:35) and 15-min depot ends for the Dobříš branch, 9 vehicles. The user preferred the simpler circuits. The `depot_leg()` builder code went with it; the variant script is only in that session's scratchpad.
- Builder options added for 210:
  - `step`: legs move by whole hours inside interval 240.
  - `turns`: the turn before each next leg. For Čisovice it is 60, which gives the real 1 h 15 min wait that the Also-at slot order produces.
  - `also`: Also-at offsets. Vehicles = cycle ÷ interval × slots. The page lists the smallest slot as Offset and the rest as Also at.
- Also at cannot change the route, so the trains that really start or end at Praha-Vršovice (depot runs) run from and to Praha hl. n. in the game.
- 212 Čerčany – Zruč is two 810s alternating (810 501 and 545 on 18 Jun). 212 Sázava is an 814. Zruč – Havlíčkův Brod is 841s with a real 5-minute turn at Zruč (841 009 on 18 Jun).
- `min_turn` per line: Čerčany 8 min (210) and Zruč 5 min (212 Havlíčkův Brod) are real turns. The default 10 min would add a vehicle to each line.
- 212 even hours from Čerčany: only the 14:16 goes to Ledečko on workdays. The 16:16 and 18:16 end at Sázava (CIS JŘ and vagonweb). The 14:16 814 rides back attached to Os 9222 Zruč 14:06, which is "814 Ledečko – Čerčany" in the plan. Together with Zruč → Kácov → Zruč, that is a once-a-day move bringing the two 814s to Čerčany, so it is listed, not modelled.
- `svc` can be a list: the trains from Havlíčkův Brod have no svc at their first stop.
- Hourly lines (every 60) show the real time as ":55 every hour". "Leave up to" stays automatic.
- `inventory()` now splits each train into runs of consecutive stops on the line. Without that, S9 Praha – Benešov trains, which stop at Praha hl. n., Praha-Vršovice and Čerčany, looked like Praha – Čerčany trains. A stretch that mixes modelled trains with others (Praha – Skochovice: the S8 trains plus the Davle short) gets one row for each kind. The 012/014/235 inventory is unchanged.

The design is the `LINES` list in the script: one real train each way per line, plus wait points that aren't long stays. Everything else is read from the data: times, stations, timed stops, round trip, vehicles and the real-train lists.

| Line | Real route (svc) | Every | Timed | Vehicles |
|---|---|---|---|---|
| 012 | Pečky – Kouřim (1011) | 120 | Pečky S:12 (72), Kouřim L:10 (10), Plaňany towards Pečky L:29 (29) — crossing | 1 |
| 012 short | Pečky – Bošice (1011) | 120 | Pečky L:12 (12), Bošice S:16 (76), Plaňany towards Pečky S:29 (89) — crossing | 1 |
| 014 | circuit Kolín – Ledečko – Kolín – Uhlířské Janovice – Kolín (1018) | 120 | Kolín → Ledečko S:47 (107), Ledečko S:07 (67), Ratboř towards Kolín L:02 (2), Kolín → Uhlířské Janovice L:47 (47), Uhlířské Janovice L:33 (33), Ratboř towards Kolín S:02 (62); both Kolín entries stop type terminal | 3 |
| 235 | Kutná Hora hl. n. – Zruč nad Sázavou (1028) | 120 | Kutná Hora L:05 (5), Zruč L:21 (21), Zbraslavice towards Kutná Hora S:01 (61) — 17 min, Malešov towards Kutná Hora S:28 (88) — 5 min | 2 |
| 235 short | Kutná Hora hl. n. – Zbraslavice (1028) | 120 | Kutná Hora S:05 (65), Zbraslavice L:01 (1), Malešov towards Kutná Hora L:28 (28) — 5 min | 1 |
| 235 město | Kutná Hora hl. n. – Kutná Hora město (1028) | 120 | hl. n. L:14 (14), město S:32 (92) | 1 |

- **Third pass (user, 5 Oct 2026): short stays at main-line stations.**
  - 014 became one shared circuit, because vagonweb shows the same 814 units alternating between the branches. Kolín now has 31 min instead of 91, and the line needs 3 vehicles instead of 4, so 9 in total.
  - 012 and 235 stay separate. 012 shares its 810s, but Pečky's stay is fixed at 26 min by the real :46/:12. 235's město shuttle uses its own 810s.
  - The script supports lines made of several legs (`legs`, `terminal`).
  - `vagonweb.py` reads the compositions.
- **Second pass (user, 5 Oct 2026).**
  - The user asked about the peak Uhlířské Janovice trains on 014 and the Kutná Hora-only trains on 235, which became 014 short and 235 město. That made 9 vehicles.
  - **012 short** was found by the new train inventory: Pečky has a train every hour at :12, to alternating ends.
  - **Coverage check:** `inventory()` groups every workday train by the stretch it runs on each line. The build stops on any stretch that is neither modelled nor in `LISTED`, and the page shows the table under "Every workday train on these lines". That makes 10 vehicles.
  - **Whole minutes only:** the game has no half minutes. Every time is rounded down, as in the printed timetable, and stays are computed from the rounded times.
- **235 short** is the real afternoon Kutná Hora – Zbraslavice trains (15:01, 16:05, 17:01) in the hours between the Zruč trains. Together the two lines give Kutná Hora – Zbraslavice an hourly service, as in reality.
  - Os 19215 Kolín 13:41 → Zbraslavice (svc 1020) is the same vehicle's one through run, and is not modelled.
- **Offsets:** odd hours first, (time − 60) mod 120, the user-confirmed rule. See the note in `../md-cr/README.md` about the fork source counting from midnight.
