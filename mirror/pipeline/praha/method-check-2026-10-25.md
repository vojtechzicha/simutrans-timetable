# Prague sheets: method check, 25 Oct 2026

Sheets: **Prague Tram Peak Fleet** (pipeline `praha`, state 2026-10-12, with the metro, ferry and NAD rows), **Prague Trolleybus
Peak Fleet** (`praha-trolleybus`, state 2026-09-27) and **Prague Bus Lines Check** (`praha-bus`, state 2026-09-29).

Rules applied (kb `rules/fork-schedule.md`, `rules/city-fleet-sheets.md`, `lessons.md`): each line at its own afternoon peak; the
longest stretch one interval + offset + Also at reproduces exactly; approximate rows labelled with their largest deviation and the
slower option; both ends of a Simutrans line at one rate; at least 2 real departures per slot; ≤ 8 slots; intervals dividing 1440;
loop −1 only at loops; branches and short workings as their own Simutrans lines, interleaved; depot runs never modelled.
Typed values: (real − 60 − 1 at loops) mod every (the 01:00 origin fix made earlier today stays as it is).

Method: every row was compared with the GTFS trips of its own terminus pair (tram/metro/ferry: export 2026-10-13, service day
20 Oct; trolleybus: export 2026-09-28, 29 Sep; bus: export 2026-09-29, 30 Sep): which real departures 15:00–17:59 fall on a
slot, which slots have no departure, how far the others are off, and the exact runs a stricter search finds (intervals dividing
1440 up to 120, ≤ 8 slots, ≥ 4 departures, ≥ 2 per slot, overlapping 15:30–17:30 by ≥ 30 min). Rates were paired per terminus
pair. Every change was rebuilt (`scripts/run.py`, stored raw data only) and diffed against the 25 Oct snapshot.

## 1. Prague Tram Peak Fleet

**Checked:** all 58 tram rows, metro A/B/C, ferries P1–P6, NAD X9 and X25.

### Changed

**22 Vypich → Nádraží Hostivař** (was every 40, Offset 1, Also at 9, 25 on the published sheet; 21, 29, 5 after this morning's
offset fix). Real departures: 14:42 14:50 15:06 15:22 15:30 15:46 16:02 16:10 16:18 … every 8 … 17:54, then every 10.
From 16:02 to 17:54 it is every 8 at :02 without a gap (15 departures); before that the 15:14, 15:38 and 15:54 slots start at
Nad Džbánem (15:07, 15:31, 15:47; trams from Vozovna Vokovice that join the route at Brusnice in the Vypich slot: Vypich 15:06
is at Brusnice 15:15, Nad Džbánem 15:07 at 15:23, Vypich 15:22 at 15:31). The fit had picked the every-40 run 14:42–16:10
(8 departures) because runfit only keeps runs overlapping its 15:30–16:30 core by ≥ 30 min, and the every-8 run starting at 16:02
overlaps it by 28. Every 40 with 3 slots is 4.5 trams an hour against 7.5 from Nádraží Hostivař, which cannot run.
**New: every 8, Offset 5** (real :02; check (5 + 61) mod 8 = 2), via `schedule_overrides["22"]["Vypich"]`.

**23 Královka – Bílá labuť** (was Královka every 60, Offset 7, Also at 11, 43 = 3 an hour fitted to 3 departures; Bílá labuť
every 32, Offset 26, 1.9 an hour). Real: Královka 15:12 15:44 16:08 16:40 17:12 17:42 18:08; Bílá labuť 15:22 15:54 16:26 16:50
17:22 (17:54 goes to Brusnice). 2 an hour all afternoon, gaps 24–32 min, three trams on an 88–90 min round (`cycle_need` 3).

| Candidate | Královka | Bílá labuť | Verdict |
|---|---|---|---|
| every 30, real :12 / :22 | 3 of 6 on the slot (15:12, 17:12, 17:42), up to 4 off (16:08) | 2 of 5 on (15:22, 17:22), up to 4 off (16:26) | **chosen**: one slot, divides 60, own minutes |
| every 30, real :11 / :23 | up to 3 off, none on a slot | up to 3 off, none on a slot | not the timetable's own minutes |
| every 32 | no every-32 run | exact 15:22–16:26 (3 dep.), then 16:50 and 17:22 8 min off | 8 min off, one end only |
| every 120, 4 slots (real 8, 40, 72, 104 / 26, 50, 82, 114) | exact 15:12–17:12 (5 dep.) | exact 15:22–17:22 (5 dep.) | rejected: 5 departures on 4 slots, under 2 a slot; the 120-min repeat is a coincidence of the drifting 3-tram round |

**New: Královka every 30, Offset 11** (real :12, loop −1), **Bílá labuť every 30, Offset 22** (real :22, street stop, no shift),
approximate, up to 4 min off; `schedule_overrides["23"]` with the new `"approx": true` key (the override code could only take
exact slots before; with an off-slot pattern it would have crashed or listed real trips as "extra departures").

Both are `kind: minor` in `changes.lines`, so the change sheet lists them ("Schedule corrected 25 Oct …"); 23's old text
("Královka 1 min earlier") described the superseded pattern. No tram moves: needs come from the trips (22 branches 17 + 17, 23: 3).

**Display:** the no-loop rows typed on every 8 (5 and 6 at Nádraží Holešovice, 7 Bílá labuť, 13 Zvonařka, 17 Libuš, 19 Pankrác)
said "no loop · as timetabled" with no real minute, while the typed value is real − 4 since the 01:00 fix (Zvonařka: typed 5,
real :01). They now show "real N" and "no loop · no 1-min shift". Values unchanged.

### Checked, unchanged

- All other tram rows: every real departure 15:00–17:59 is on a slot or ≤ 3 min off at the window edges. Short exact stretches
  are broken only by an empty slot that a depot run or pull-out fills: 6 Nádraží Holešovice (17:04 to Vozovna Strašnice),
  6 Kubánské náměstí (15:47, 15:07; pull-outs Vozovna Strašnice 15:02, 15:42), 7 Bílá labuť (one empty slot at 15:18; 17:10 goes to Vozovna Motol),
  7 Kotlářka (17:14 to Vozovna Žižkov), 10 Sídliště Řepy (15:15/15:35/15:55 start at Hotel Golf), 22 Zahradní Město (15:18,
  15:42; Vozovna Strašnice pull-outs), 31 (15:17, 15:41; Vozovna Hloubětín 15:10, 15:34), 3 Levského (15:03–15:27 is the Nádraží
  Braník branch, ruled not a peak trip on 28 Sep). The typed values are right for the whole peak.
- 9 Sídliště Řepy (the one approximate tram row before): every 4, real :01, the Hotel Golf slots documented; correct.
- Metro A (both branches every 6, interleaved 3 apart on the trunk) and B (every 5 with 2 slots both ways): exact, one rate.
- Ferries P1–P6: exact, one rate each. NAD X9 (every 4) and X25 (circular, every 4): exact.

### Open (owner's decision)

- **Metro C** runs at two rates: Letňany → Háje every 12 with 5 slots (25 an hour), Háje → Letňany every 8 with 3 slots
  (22.5 an hour). Real: Letňany 21 / 25 / 23 departures in the 15, 16 and 17 o'clock hours, Háje 18 / 23 / 25; 48 each way in
  16:00–17:59. Proposal: both ends every 5 with 2 slots (24 an hour, like B): Letňany Offset 1, Also at 3; Háje Offset 1,
  Also at 4 (up to 1 min off). Alternative 25 an hour: every 12, Letňany 2, 4, 6, 9, 11; Háje 0, 3, 5, 7, 10. The metro block
  has no override hook, so this was not changed.
- The change sheet still files the 14 lines whose only change is today's offset fix under "Unchanged lines … Nothing to do".

## 2. Prague Trolleybus Peak Fleet

**Checked:** all 14 rows; nothing changed (rebuild identical).

- 52: both branches every 8; at Na Knížecí they leave 4 min apart (Waltrovka :07, Jinonice :03) and arrive 4 apart (Jinonice
  :02 + 14, Waltrovka :03 + 9). 58: both branches every 12, 6 min apart at Palmovka both ways. 59: every 3 both ways, exact
  15:29–17:47 and 15:46–18:01. One rate everywhere.
- 51 and 53 (one trolleybus each, hand-set hourly approximations of 29 Sep): 53 has no regular pattern (gaps 44–83 min), hourly
  stays. **51 has an exact pattern the fit missed** (it searched intervals ≤ 60): every 120 with 2 slots. Hradčanská 14:44 15:32
  16:44 17:32 (real 92, 44: Offset 31, Also at 103), Bořislavka 15:12 16:24 17:12 (real 72, 24: Offset 11, Also at 83; 14:23 is
  1 min early, 17:56 starts the evening pattern). Same number of trips as the hourly row, which is up to 16 min off. Left for
  the owner, since it is a one-vehicle hand decision.
- Note: `Prague Trolleybus Peak Fleet-VZ MacBook Pro.html` in the working-folder root is a OneDrive conflict copy of the sheet
  from before the offset fix.

## 3. Prague Bus Lines Check

**Checked:** all 303 rows (164 lines). The pipeline had no override mechanism, so `02_gtfs_lines.py` gained a small one
(`schedule_overrides` in the state: hand-set rows replace the main-pattern rows on a card; the script works out each row's exact
run and its largest deviation 15:00–17:59; `extra` lists peak trips left out, `approx` hides the run). After the change:
ORIGIN 0, RANGE 0, FOLD 0, RATE 0, every interval divides 1440. No bus or course changed (only `gtfs_lines.json` and the
schedule rows of 17 cards differ).

### Changed (17 lines; old = published sheet)

| Line | Entry | Old (every / Offset / Also at) | New | Evidence |
|---|---|---|---|---|
| 107 | Dejvická → Suchdol | 30 / 3 / 8, 11, 14, 19, 23, 26 | **4 / 2** (approx., ≤ 2) | 7 slots on 8 departures 16:09–16:39; 45 departures 15–18 at 2–7 min gaps |
| 107 | Suchdol → Dejvická | 5 / 4 | **4 / 0** (approx., ≤ 2) | 47 departures 15–18 (15.7 an hour); every 5 exact only 16:00–16:45; slower option every 5 |
| 110 | Obchodní centrum Čakovice → Hloubětín | 60 / 4 / 34, 49 | **15 / 4** | every 15 at :05; the :20 slots before 17:00 come from Třeboradický hřbitov (15:12, 16:12) |
| 110 | Hloubětín → Obchodní centrum Čakovice | 15 / 14 | 15 / 14 | unchanged (15:30, 17:30 go to Třeboradický hřbitov) |
| 111 | Skalka → Koloděje | 60 / 33 | 60 / 33 | hourly :34; extras 16:49, 17:04 listed |
| 111 | Koloděje → Skalka | — | **60 / 10** | hourly :11; extras 17:26, 17:41 listed |
| 111 | Skalka → Dubeč | — | **30 / 18** | :19/:49 |
| 111 | Dubeč → Skalka | 30 / 3 | 30 / 3 | the card had paired Skalka → Koloděje with Dubeč → Skalka (1 vs 2 an hour); Dubeč is the short working of the Koloděje line |
| 122 | Újezd u Průhonic → Opatov | 45 / 38 | **60 / 23** | hourly :24 13:24–16:24, 19:24; 17:09, 18:09 run 15 min early; every 45 was 2 departures |
| 143 | Dejvická → Stadion Strahov | 45 / 3 / 9, 13, 18, 26, 33, 41 | **15 / 3 / 11** | :04 :12 :19 :27 :34 :42 :49 every hour, :57 runs as :55 + :59 (the extra bus) |
| 157 | Násirovo náměstí → Kačerov | 60 / 3 / 11, 20, 29, 39, 47, 55 | **15 / 2 / 9** | exact 15:10–15:48 and 16:40–17:33; one bus fewer 15:56–16:30 (≤ 3 off); no regular slower option (7 an hour repeats only 15:40–16:48) |
| 176 | Stadion Strahov → Karlovo náměstí | 60 / 1 / 8, 16, 23, 31, 46, 53 | **15 / 1 / 8** | every 7.5 pattern; the timetable leaves out 15:17, 16:39, 17:32; no regular slower option (the gap moves round the hour) |
| 176 | Karlovo náměstí → Stadion Strahov | 60 / 59 / 7, 14, 22, 29, 37, 52 | **15 / 14 / 7** | leaves out 15:45, 17:08, 18:00 |
| 187 | Nádraží Holešovice (circular) | 60 / 59 / 6, 21, 36, 44, 51 | **90 / 36 / 51, 66, 74, 81, 89, 6, 21** | every 15 at :07 plus 2 extras every 90 min (15:45 16:00, 17:15 17:30): exact 13:00–18:37 (30 dep.); simpler option every 15 / 6 without the extras |
| 189 | Sídliště Lhotka → Kačerov | 15 / 5 / 13 | **6 / 1** (approx., ≤ 3) | Kačerov sends every 6 (10 an hour), Lhotka every 7–8 (8); slower option 8 an hour both ends |
| 207 | Ohrada → Staroměstská | 36 / 1 / 7, 13, 19, 25, 33 | **6 / 1** | every 6 from 15:32; every seventh bus 2 min late (16:10, 16:52, 17:34) |
| 211 | Sídliště Rohožník → Nádraží Klánovice | 30 / 22 | **60 / 22 / 42, 52** | :23 :43 :53 every hour (no 16:43), matching 3 an hour from Klánovice |
| 232 | Smíchovské nádraží → Na Knížecí | 30 / 0 / 7 | **30 / 7** | :08/:38 all day; the 5 peak extras (15:01 15:46 16:01 16:31 17:01) have no trip back |
| 102 | Kobylisy → Sídliště Bohnice; Sídliště Bohnice → Šimůnkova | — | **15 / 2; 15 / 0** | the long line Šimůnkova – Kobylisy – Sídliště Bohnice and its short working Kobylisy – Sídliště Bohnice are interworked (60-min round, 4 buses = need): one circuit line, Bohnice twice and Kobylisy three times in the schedule |
| 103 | Březiněves → Ládví; Ládví → Ďáblice | — | **15 / 6; 15 / 4** | Březiněves line and its short working to Ďáblice, every 15 from 16:00, :05 / :13 at Ládví |
| 139 | Komořany → Želivského; Želivského → Sídliště Zbraslav | — | **15 / 4; 15 / 13** | Sídliště Zbraslav line and its short working to Komořany, :06 / :14 at Želivského |
| 191 | Terminál 1 → Na Knížecí; Na Knížecí → Dědina; Na Knížecí → OC Ruzyně; OC Ruzyně → Na Knížecí | — | **20 / 4; 60 / 18 / 31, 51; 60 / 11 / 38, 58; 60 / 0 / 27, 47** | three lines from Na Knížecí (Letiště; Dědina; one stop on to OC Ruzyně), interleaved :05 :12 :19 :25 :32 :39 :45 :52 :59 |
| 226 | Lipany → Háje; Háje → Benice | — | **60 / 54; 60 / 36** | hourly Benice line and its hourly short working to Lipany, :37 / :07 at Háje |

Rows whose values stayed but now carry a hand-set reason: 102 Šimůnkova → Bohnice, Bohnice → Kobylisy; 103 Ládví → Březiněves,
Ďáblice → Ládví; 122 Opatov; 139 Želivského → Komořany, Zbraslav → Želivského; 143 Stadion Strahov; 157 Kačerov; 189 Kačerov;
191 Na Knížecí → Letiště, Dědina; 207 Staroměstská; 211 Klánovice; 226 Háje → Lipany, Benice → Háje; 232 Na Knížecí.
Where an interval does not divide 60 (116, 131, 187, 218) the card now also says how the 01:00 origin changes the typed value.

Checked and left: 131 (every 48 with 7 slots both ways: every 6 with every eighth bus missing, exact 14+ departures, 8.75 an
hour both ends), 190 and 200 (both ends at one rate; 200's every-3 stretch from Kobylisy 16:32–18:20 cannot be matched at
Bohnice, so the shared every-15-with-4 row stays), the alias pairs 100, 138, 174, 184, 246 (one terminus with two stop names).

### Open (owner's decision)

- **School lines 251–280** (1–6 trips a day, mostly one at 7:xx) show "every 60, Offset N" fitted to that trip. By the brief
  (school-only lines excluded; sparse trips listed, not modelled) they should say "not modelled". Not changed.
- **Branches with ≥ 3 peak trips but no rows** (the card says "own Simutrans line" without values). Proposed rows, all exact
  fits of the real trips, interleaved as the timetable runs them:

| Line | Entry | Every / Offset / Also at | Real fit |
|---|---|---|---|
| 109 | Palmovka → VÚ Běchovice; back | 30 / 8; 30 / 22 | exact 14:09–17:39; 14:23–18:53 |
| 113 | Kačerov → Točná; Točná → Kačerov | 30 / 0; 30 / 21 | exact 13:01–19:31; 14:52–17:52 |
| 113 | Kačerov → Písnice; Písnice → Kačerov | 30 / 15; 30 / 15 | exact 13:16–19:16; 14:46–17:46 |
| 120 | Na Knížecí → Nádraží Radotín; back | 30 / 28; 30 / 14 | exact 13:29–17:59; 14:15–19:15 |
| 138 | Ústavy Akademie věd → Sídliště Skalka; back | 30 / 16; 30 / 13 | exact 15:17–17:17; 15:44–17:44 |
| 146 | Želivského → Vinice Hrdlořezy; back | 30 / 29; 30 / 26 | exact 14:30–19:30; 13:57–19:27 |
| 160 | Dejvická → Výhledy; back | 60 / 24; 60 / 22 | exact 13:25–18:25; 13:23–17:23 |
| 174 | Kukulova → Třebonice; Třebonice → Vypich | 20 / 5; 20 / 9 | exact 15:26–17:06; 16:10–17:50 |
| 174 | Kukulova → Řeporyjské náměstí; back to Vypich | 60 / 37 / 57; 60 / 2 / 42 | :38/:58 (16:37 1 min early); exact 15:03–16:43 |
| 177 | Chodov → Volha; Volha → Chodov | 15 / 0 / 8; 15 / 1 / 8 | exact 15:31–17:24; 15:09–16:17 |
| 186 | Černý Most → Vinoř; back | 60 / 16; 60 / 50 | exact 14:17–19:17; 14:51–18:51 |
| 197 | Smíchovské nádraží → Sídliště Písnice; back | 15 / 9; 15 / 14 | exact 14:40–17:25; 15:15–18:15 |
| 221 | Klánovice → Nádraží Klánovice-sever; back | 30 / 12; 30 / 29 | exact 14:43–19:13; 14:30–19:30 |

  The bus need on these cards is one count for the whole line (max of round trip and buses on the road); it is not split by branch.

## 4. Verification

- Before any change, rebuilding all three states reproduced the current HTML (with this morning's offset fix) exactly (0 lines).
- After the changes: tram cards differ only in the 22 Vypich row, the two 23 rows, the 22/23 change texts and the six no-loop
  subtitles; the 22 card moved from "Unchanged lines" to the small edits; derived data: only lines 22 and 23 of `timetable.json`.
  Trolleybus: identical. Bus: only the schedule rows and "other stop patterns" notes of the 17 changed cards, and the 01:00 sentence on 4 cards;
  `courses`/vehicle files byte-identical.
- `audit/city_systemic.py`: praha and praha-trolleybus ORIGIN / RANGE / FOLD / RATE 0 (praha approximate 1 → 4: 9 Řepy,
  22 Vypich, 23 both ends). praha-bus (not in that script): the same checks run on its rows, all 0.
- Superseded rows in `audit/city-changes-2026-10-25.md`: tram 22 Vypich (→ 21, 29, 5) and 23 Bílá labuť (→ 30); bus 122 Újezd
  (→ 23), 143 Dejvická (→ 33, …) and 207 Ohrada (→ 13, …).
