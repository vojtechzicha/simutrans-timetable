# Method check of the active rail sheets, 25 October 2026

Owner: "verify all sheets with this level of detail … that's the point of you doing it, so you'll not produce incorrect
results." Checked against `../rail-design-rules.md`, this README, and kb `rules/rail-sheets.md`, `rules/fork-schedule.md`,
`lessons.md`. Owner decisions recorded there were kept; only demonstrable errors were changed.

Sheets and builders (all five have a builder; none is hand-written):

| Sheet | Builder | Result |
|---|---|---|
| `Ex7 R17 Praha Veselí.html` | `build_ex7_r17.py` | text only (listing gaps) |
| `S75 Beroun Rakovník.html` | `build_s75.py` | documented out trip corrected, **no in-game change**; works listed |
| `S9 S2 R17 R49 Ex7.html` | `build_s9_s2.py` (imports R17/Ex7 from `build_ex7_r17.py`, R49 from `build_benesov.py`) | text only |
| `Trains S4 to S3.html` | `build_s4.py` | text only (listing gaps, works re-check) |
| `Trains S5 to S4.html` | `build_s5.py` | **S40 Slaný entry offset 89 → 91**; text |

Before any change all five rebuilt byte-identical to `../_snapshots/2026-10-25/html/` (S9 sheet: identical except line
endings; the snapshot has LF, a rebuild on this machine writes CRLF — `htmldiff.py` 0/0). After the changes
`htmldiff.py` shows only the intended rows (counts at the end).

## How it was checked

Scripts written for this check (verify, cover and junction stayed in the session scratchpad; their logic is described here so they can be redone; check_track.py and check_followers.py are saved in this folder):

- **verify** — for every line: each leg stop by stop at game minutes (shifts applied), every stay ≥ 5 min marked; every
  timed entry with its offset; the round trip recomputed leg by leg from the real minutes and rounded up to the interval
  (compared with the builder's cycle and vehicles); and every real workday train 12:00 – 20:59 of the line's services at
  the leg's first common station, marked when it falls on the game slot. All offsets are produced by
  `base.offset() = (real − 60) mod interval` from the real departure + whole-hour shift; I recomputed a sample by hand
  for every interval used (30, 60, 72, 120, 15) — listed per sheet below.
- **cover** — the inventory rerun with *all* services, to find workday trains of other line numbers (including trains
  with no CIS line number) that run 2+ consecutive stations of a line.
- **junction** — services that touch exactly one station of a sheet and have no workday train (Sat 3 – Sun 11 Oct).
- **check_track.py** (now in this folder) — every line laid out as the game runs it (each leg repeated at its interval,
  12:00 – 21:00, on the raw CIS minutes incl. passing points); every pair of opposite trains is followed to where they
  meet; an open-line meeting is flagged unless real workday trains also meet on open line on that segment (= double
  track), a station meeting is flagged where real trains never cross. Flags were checked by hand with
  `check_meetings.py`.
- **check_followers.py** (now in this folder) — for every "timing point" entry, the closest non-Os real train passing the same station in the same
  direction 0 – 8 min after the held train's minute (13:00 – 19:59, folded on the line's interval).
- **Cross-sheet same minute** — all timed entries of the five sheets compared per station and minute (mod 240).
- **Works** — pid.cz/zmeny/?type=vlaky read on 25 October, plus the detail pages of every item touching these lines.

## Engineering works (check 6), state on 25 October 2026

Model week Mon–Fri 5 – 9 Oct; today 25 Oct (Sunday; next workday 26 Oct).

| Works (pid.cz) | Dates | On model week | Today | Sheet treatment |
|---|---|---|---|---|
| Praha Masarykovo nádraží closed (R24, R42, S4, S5, S54) | 1 Jun – 12 Dec | yes | yes | modelled (Praha-Bubny), unchanged |
| Uhříněves – Strančice, workday restrictions (R17, R49, S9; XS9) | 12 Oct – 3 Nov | no | yes | modelled as "until 3 November" lines (S9 sheet), unchanged |
| Kolín – Velký Osek (S2, XS2): S2 does not stop at Kolín-Zálabí, Veltruby on workdays 6–20 (from 16 Jun) | 12 Jan – 11 Dec | yes | yes | **was not on the S9 sheet**; CIS JŘ already has it, time-dependent: the daytime trains pass both stops (Os 25837 Veltruby 17:20½, Kolín-Zálabí 17:23; Os 25840 15:34 / 15:36½; Os 25827 14:20½ / 14:23), the trains after 20:00 stop there (Os 5856 Kolín 20:30 → Zálabí 20:32; Os 5855 Veltruby 22:21 – 22:22), records valid to 11 Dec. So the design is already the works state — note added |
| Rakovník – Roztoky u Křivoklátu by bus (S75) | 29 Sep – 8 Nov | yes | yes | owner rule 14 Oct: not modelled (ends early Nov). **Was missing on the S75 sheet** — added |
| Rakovník – Blatno u Jesenice by day (S57, S75, XS57) | 19 – 31 Oct | no | yes | short, listed on S5; **added on S75** (touches only Os 7713 to Rakovník západ; Os 7725 runs after the 8:00 – 18:26 window) |
| U14 Měcholupy – Žatec by bus | 13 Jul – 9 Nov | yes | yes | owner rule: not modelled, listed (S5), unchanged |
| Hostivice – Středokluky – Noutonice by bus XS54 (S54) | 26 – 30 Oct | no | starts tomorrow | **new**, short → listed on S5 |
| (Benešov –) Strančice – Uhříněves, nights (R17, S9) | 6 – 9 Nov | no | no | nights only → mentioned on Ex7 sheet |

**No modelled works state has ended.** The S6 (to 19 Oct) and S65 states are on the archived Beroun sheet, not on these
five. The S4 sheet listed two short items that are over (S4 Roztoky – Kralupy 17 Oct, R20 nights 13 – 17 Oct); marked
as over. Not re-checked: ČD-only / Ústí-region items (Roudnice – Ústí 29 – 30 Oct, the German Monday works for Ex5),
and the carriers of U12, U13 and the Straškov lines (DLB, RegioJet ÚK, ČD) beyond what PID lists.

Coming ends to act on: Uhříněves – Říčany 3 Nov (switch S9 Milovice / R49 back from the "until 3 November" versions,
drop XS9), S75 bus 8 Nov, U14 bus 9 Nov, Kolín works 11 Dec, Masarykovo 12 Dec, JR2027 on 13 Dec (full refresh).

## Ex7 · R17 Praha – Veselí nad Lužnicí

1. **Inventory / ends.** R17 15 + 15 modelled, shorts R 731, 737, 734, 703 listed; Ex7 11 / 12 modelled. Both cut at
   Veselí nad Lužnicí (track end). **Finding:** R 326 and R 324 (Gmünd – Veselí 12:38 / 18:38 – Tábor :58 – :00 –
   Benešov :29 – :31 – Praha hl. n. :10) run exactly on R17's slot but were on neither sheet: CIS JŘ has no line
   number at their first stop (Gmünd NÖ), and the inventory uses `inv_svcs={'17'}`. Fixed: `extra_real` on R17 (they
   now appear in its real-train list, which is hourly 5:38 – 21:38 from Veselí). **Finding:** SC 500 (Ostrava – Praha
   hl. n. 20:26 – 20:31 – Tábor 21:25 – 21:27 – Veselí 21:38 – České Budějovice, CIS category 94 = SC, no line number)
   was not listed; added to "Ex7 outside the afternoon". The Praha hl. n. – Vršovice – Zahradní Město trains of other
   lines (S8/S88, S9, R49, R9, R18, R19, Ex3, private carriers) added to "Not part of this sheet".
2. **Offsets** (every 60 = minute): R17 Praha :46 (R 721 14:46), Benešov :29 (15:29), Tábor :00 (16:00), Veselí :38
   (R 712 15:38½ → :38), Tábor :00, Benešov :31; Ex7 Praha :21 (Ex 537 15:21), Tábor :23, Veselí :23 (Ex 530 passes
   16:23½), Tábor :37. Every afternoon train is on the slot (R17 12:46 – 20:46 out; Ex7 12:21, 14:21 – 18:21 out,
   12:23 – 16:23 and 18:23 back). Correct.
3. **Timed stops.** Termini, Benešov and Tábor (important, 2 min); no stay ≥ 5; double track, no crossings; Ex7 and
   R17 never overtake each other. Praha hl. n. stays 36 min (R17, in :10 / out :46) and 42 min (Ex7, :39 / :21) are
   fixed by the real minutes and there is no depot evidence (owner, 14 Oct) — left, owner item.
4. **Vehicles.** R17 93 + 19 + 92 + 36 = 240 → 4; Ex7 73 + 49 + 76 + 42 = 240 → 4. Correct.
5. Hourly both ways; afternoon peak out of Praha hourly. Correct.
6. See works table: Uhříněves – Říčany listed, not modelled on this sheet (it is on the S9 sheet). Re-check line added.
7. `check_track.py build_ex7_r17`: 0 flags.

## S75 Beroun – Rakovník

1. **Inventory.** 16 + 16 modelled; Rakovník západ runs, Os 7703 from Zdice and the off-pattern trains listed. Other
   services: only S6 on Beroun – Beroun-Závodí (described). **Finding (junction rule, 13 Oct):** Rakovník – Kralovice
   (S58, CIS 1058) has no workday trains and was not named; added to "Not part of this sheet".
2. **Offsets** (every 60): Beroun :59 (Os 7745 14:59 / 7717 15:59 / 7719 16:59), Zbečno :26 (7745 15:26½, 7717
   16:26½), Rakovník :56 (Os 7718 15:56). Correct; unchanged.
3. **Timed stops.** Termini and the Zbečno crossing towards Rakovník. Beroun 10 min. Correct.
4. **Vehicles.** 3 (180 min). Correct; unchanged.
5. Hourly both ways from the peak (14:59 – 16:59 out). Correct.
6. **Finding:** the sheet (13 Oct, before the works rule) listed no works. Added Rakovník – Roztoky bus (29 Sep – 8 Nov,
   not modelled by the owner's 14 Oct rule) and the Rakovník – Blatno day works.
7. **Finding (crossing):** the line was documented on Os 7717 (Beroun 15:59 → Rakovník 16:57). Its arrival at
   Rakovník (:57) is after the hourly back train's departure (:56), so every hour the documented pattern has both
   trains on the single track Chlum u Rakovníka – Rakovník: `check_meetings.py 7717 7718 Beroun Rakovník 60` →
   "CONFLICT Chlum u Rakovníka – Rakovník 16:56". Os 7719 (16:59) also conflicts (Zbečno – Újezd). Os 7745 (14:59 →
   15:55) crosses Os 7718 only at Zbečno (`check_meetings.py 7745 7718 …` → "cross at Zbečno 15:25"), exactly as the
   real 7745 × 7716 and 7717 × 7718 pairs do. **Changed** `rep_out` 7717 → 7745. Typed values identical (59 / 26 /
   56), vehicles 3; the page now says Zbečno 3 min (was 4), Rakovník 61 min (was 59), round trip on 7745's minutes, and
   a visible correction note. `check_track.py build_s75`: 1 flag before, 0 after.

## S9 · S2 · R49 · R17 · Ex7

1. **Inventory.** No gaps; all S9 / S2 / R49 shorts listed. **Findings (cover):** S3, S30, S34, R43, R21 (Praha hl. n. –
   Vysočany – Rajská zahrada), Ex3, Ex6 / EC to Vysočany, R9, R18, R19 and the private carriers' trains were not named
   in "Other lines on this track" — added; R 324 / 326 via the R17 fix. Junction check: only seasonal weekend specials.
2. **Offsets** recomputed: S9 Benešov (30): Praha :21 (Os 2549 15:21), Vršovice :26, Hostivař :06 (15:36),
   Uhříněves :12 (15:42), Říčany :19, Strančice :26, Senohraby :05, Čerčany :13; back Benešov :05 (Os 2548 15:35),
   Čerčany :13, Senohraby :22, Strančice :02, Říčany :09. S9 Milovice (30): Milovice :03 (Os 9147 15:33), Lysá :16,
   Čelákovice :25, Horní Počernice :07, Vysočany :16, Praha hl. n. :01 (16:31), Hostivař :16, Uhříněves :22; back
   Strančice :22 (Os 9142 15:52), Říčany :00, Uhříněves :08, Hostivař :14, Praha :04 (16:34), Vysočany :11, Horní
   Počernice :20. S2 Kolín (60): Praha :54 (Os 25837 15:54), …, Kolín :32 (Os 25840 15:32), Nymburk :07. S2 Nymburk
   (120, step 60): Praha 79 = S:19 (Os 5831 14:19), Lysá 116 = S:56; Nymburk 37 = L:37 (Os 5838 15:37), Lysá 61 = S:01;
   Praha 19 = L:19 (Os 5843 17:19), Lysá 62 = S:02; Nymburk 103 = S:43 (Os 5850 18:43), Lysá 1 = L:01. R49 Tábor (120):
   Holešovice 65 (Sp 2483 16:05), hl. n. 75, Říčany 98, Benešov 7, Tábor 65 (Sp 2478 15:05 + 3 h), Benešov 109. R49
   Olbramovice: Holešovice 5 (2483 − 1 h), hl. n. 15, Říčany 38, Benešov 67, Olbramovice 36 (Sp 2474 7:36 + 10 h),
   Benešov 49, hl. n. 101. XS9 (15): Háje 2, Uhříněves 0 / 10, Říčany 10. Every afternoon S9 / S2 train is on its slot
   (S9 Benešov 12:21 – 19:51, S9 Milovice 14:33 – 18:33, S2 Kolín 12:54 – 17:54). All correct.
3. **Timed stops.** Every stay ≥ 5 is timed (S9 M Lysá 7, Praha 9 / 6; S2 Nymburk hl. n. 12 / 10; S2 N Lysá 7 / 8;
   R49 Říčany 5). Follower check on every timing point of S9 Benešov, S9 Milovice, S2 Kolín and S2 Nymburk: no faster train within 6 min except Praha-Vršovice :26 (S9
   Benešov; RegioJet 1010 / 1012 / 1014 pass 3 min later, every 2 h — four tracks there, real order) and Praha-Vysočany
   :26 (S2 Nymburk; R43 Sp 1542 – 1546 4½ min and R 1148 – 1152 4 min later, which leave the S2 line right there). The
   notes' claims (R17 6 min at Čerčany, R49 7 min at Říčany, R10 6 – 7 min at Poděbrady / Velký Osek) are confirmed.
   Left (owner-requested timing points; reported). Praha hl. n. stays: S2 Kolín 52, S2 Nymburk 42 (real minutes; the
   page already offers the one-circuit S2 at 17 min) — owner item.
4. **Vehicles.** 5 + 7 + 4 + 3 + 2 + 2 + 4 + 4 = 31 (+ 6 temporary S9 Milovice, 2 + 2 R49, 6 XS9). All recomputed.
5. Both ways at the same rate; S9 30 from the peak, S2 hourly. Correct.
6. Uhříněves – Říčany still in force (modelled). **Finding:** Kolín – Velký Osek works missing (see table); note added
   on S2 Kolín, with "take Veltruby / Kolín-Zálabí out of Os231/1 if it still stops there".
7. `check_track.py build_s9_s2` (normal and works): 1 flag, R49 Tábor × R49 Olbramovice "Praha-Hostivař – Rokytka
   odbočka" — a false flag: Sp 2478 runs Hostivař 16:23½ → Malešice → Rokytka 16:41 and Sp 2483 Rokytka 16:08 → Eden →
   Hostivař 16:27, different tracks. The single-track works section is described by the builder's `single_track()`.

## Trains S4 to S3

1. **Inventory / ends.** No gaps; R20, Ex5, R15 cut at Ústí, R23 to Ústí hl. n. (stabling at Ústí západ, owner).
   **Findings (cover):** S49 (CIS 1049, 34 trains each way Praha-Podbaba – Roztoky), Sp 1494 / 1495 (S40 Praha-Holešovice
   – Slaný), R49 on Praha hl. n. – Holešovice and U52 (CIS 4052, Sp Žatec – Libochovice – Lovosice – Ústí every 2 h:
   Lovosice 13:21, 15:21, 17:21, Ústí 14:17, 16:17, 18:17) were not listed (U52 was filed under "Beyond Ústí"). Added
   one bullet. Junction check: only weekend branches (4103, 4104, 4105, 4920), covered by "Lovosice branches" / "Beyond
   Ústí".
2. **Offsets** recomputed (all equal): S4 :14 / :12; S4 Ústí :44, Kralupy :23, TPs :30 / :38 / :53 / :03, Lovosice :29;
   Ústí :05, Lovosice :31, TPs :39 / :52 / :02 / :17 / :25, Kralupy :42; 2nd unit :44 / :42 with coupling; R20 Praha Jih
   :28, hl. n. :47, Kralupy :19, Lovosice :59, Ústí :42, Lovosice :57, Kralupy :40, to Jih :27; Ex5 Jih 66, hl. n. 91 (EC
   176 12:31 = S:31), Ústí 73 (S:13), to Jih 42; R15 Jih 6, hl. n. 31 (L:31), Ústí 14 (L:14), to Jih 102; R23 Kolín 20
   (L:20), Nymburk 45, Mělník 84, Ústí západ 18, 31 / 80 empty, Ústí hl. n. 93 (S:33), Ústí západ 100, Mělník 32,
   Nymburk 72; S32 Lysá 78, Mělník 112, Ústí západ 63, Mělník 4; U32 3 / 64; S43 :27 / :59; S23 :36, Brandýs :00, :34,
   Brandýs :01. Every afternoon train of each pattern on its slot. U32 from Štětí S:04 has real trains only at 14:04 and
   16:04 (17:12 and 19:50 otherwise); `check_track` finds no conflict from the extra game trains.
3. **Timed stops.** All stays ≥ 5 timed (S4 Ústí Kralupy 8 / 9, Lovosice 5; S23 Brandýs 7). Follower check: no faster
   train within 6 min of any S4 Ústí timing point (closest R 685 – 689 7½ min at Nelahozeves, as on the page).
4. **Vehicles.** 2 + 5 + 2 + 5 + 2 + 2 + 3 + 2 + 1 + 1 + 2 = 27. Correct.
5. Correct.
6. Masarykovo modelled; re-check line added (17 Oct S4 and R20 night works over).
7. `check_track.py build_s4`: 0 flags.

## Trains S5 to S4

1. **Inventory / ends.** No gaps; S57 cut at Blatno u Jesenice, U12 at Most (track ends), U13 and Lužná – Jirkov in full
   (owner). **Finding:** Os 19746 (Praha-Zličín 7:02 → Hostivice 7:10 → Noutonice 7:37, an S65 number) unlisted; added
   to "S54 extras". Junction check: weekend branches at Chomutov / Most and Kralovice, Kolešovice, 4105 already listed.
2. **Offsets** recomputed (all equal to the builder): S5 + S45 :34, Kladno :25, :49, Kladno :31, Praha-Dejvice :10;
   S45 L:45 / 63; R45 63 (Sp 1570 14:03½), Kladno 103, 6, 14; S50 105 (Os 19708 14:45), Lužná 32, 69; R24 3, 43, 22, 74;
   S54 31 / 56 / 91 / 118; S57 :48 / :53 / Oráčov :14; U12 :09 / :28 / :00 / :22 / :03 / :37 / :02 / :27; Jirkov line 82
   / 23 / 62; U13 :42 / :48 / :30 / :55; S40 Louny 55 / 88 / 97 / 34; S40 114 / 91 (was 89); S44 :26 / :49; Vraňany
   circuit 99 / 9 / 41 / 68; Roudnice – Bříza (72): 2 (14:14: (854 − 60) mod 72) and 35 (14:47). Correct apart from S40
   below.
3. **Timed stops.** All stays ≥ 5 timed (S50 Lužná 6, U12 Hřivice 7 / 8, Jirkov line Žatec 17, S5 Dejvice 5). Long
   stays: S40 / S40 Louny 112 min at Kralupy (alternative circuit already on the page), S50 104 and S45 95 at Kladno,
   R24 54 at Rakovník — all real minutes, reported.
4. **Vehicles.** 4 + 1 + 1 + 2 + 2 + 1 + 2 + 4 + 2 + 2 + 3 + 2 + 1 + 1 + 1 = 29. S40 still 2 after the fix.
5. Correct (S57 / U12 hourly by owner choice; 4021 every 72 by owner choice).
6. Works bullet extended with the 25 Oct re-check and the new S54 bus (26 – 30 Oct).
7. **Finding (crossing):** S40 was out Os 9712 (Kralupy 14:54, předměstí 14:57½ – 14:58) with back Os 9735 (Slaný
   16:29, předměstí 16:55½ – 16:56½, Kralupy 17:00). Every 2 h the back train leaves Kralupy předměstí before the :54
   gets there, so they meet on the single track Kralupy – Kralupy předměstí: `check_meetings.py 9712 9735 "Kralupy n.V."
   Slaný 120` → "CONFLICT Kralupy n.V. – Kralupy nad Vltavou předměstí 14:56". Kralupy předměstí is where the real S40
   trains cross almost every hour (9708 × 9733, 9710 × 9709, 9712 × 9711, 9714 × 9713, 9716 × 9715, 9732 × 9737,
   9736 × 9739, 9718 × 9717); only 9735 × 9730 (16:29 / 16:22) cross at Zvoleněves. **Changed** `rep_in` 9735 → Os 9711 (Slaný 14:31, the 9712's real partner):
   `check_meetings.py 9712 9711 …` → "cross at Kralupy nad Vltavou předměstí 14:57". Slaný entry 89 (S:29) → 91 (S:31);
   stays Slaný 64 → 66, Kralupy 114 → 112; 2 vehicles. Kept the :54 out (it pairs with S40 Louny's L:55 for the hourly
   Kralupy :55) rather than moving it to 18:52. `check_track.py build_s5`: 1 flag before, 0 after.

## Cross-sheet

Same station, same minute (mod 240), all five sheets: only Praha hl. n. :31 / :91 / :151 / :211, R15 / Ex5 towards Ústí
and S9 Milovice towards Strančice — opposite directions, real minutes. The known Ex7 / S9 Benešov :21 at Praha hl. n.
(documented on the S9 sheet) and the S50 / U12 :09 at Rakovník and S40 Louny / U12 :37 at Louny (documented on the S5
sheet, different lines) remain as before.

## Left for the owner (not changed)

- Praha hl. n. stays over 20 min, all fixed by real minutes: S2 Kolín 52 (one S2 circuit would give 17 — offered on the
  S9 sheet), S2 Nymburk 42, Ex7 42, R17 36 (no depot evidence for Ex7 / R17).
- S40 and S40 Louny stand 112 min at Kralupy (one circuit: 4 vehicles instead of 5, offered on the S5 sheet).
- U52 Lovosice – Ústí every 2 h is on the built S4 corridor but comes off the unbuilt Libochovice branch: model a
  Lovosice – Ústí cut? (not done; new line).
- S75 back trip runs 53 min with no timed stop before Beroun (sheet of 13 Oct, before the 15 Oct "all-stops trains run
  fast in the game" lesson); a Zbečno timing point towards Beroun (:26) would hold the crossing if the game train runs
  early. Not added (design change, not an error).
- XS9 6 buses rests on an assumed 5-min turn at Říčany (unchanged, on the page).
- Timing point at Praha-Vršovice, inconsistent between the two S9 lines: S9 Milovice is *not* timed there because "a
  train passes 3 min behind" (its note), but S9 Benešov *is* timed there (:26) with RegioJet 1010 / 1012 / 1014 passing
  3 min behind every 2 h (`check_followers.py`). Vršovice has four tracks, so it may be fine; either drop S9 Benešov's
  Vršovice :26 entry or keep it — your call. Not changed.
- Praha-Vysočany :26 on S2 Nymburk has R43 / R21 4 – 4½ min behind, but they turn off onto their own line there.

## Diff against the snapshots (`../audit/htmldiff.py`)

| Sheet | Lines out / in | Table rows changed |
|---|---|---|
| Ex7 R17 Praha Veselí | 4 / 5 | none (notes, real-train list, Not modelled) |
| S75 Beroun Rakovník | 11 / 14 | Zbečno stay text "arrives :22, 4 min" → ":23, 3 min"; Rakovník "59 min" → "61 min"; round trip on 7745 (offsets unchanged) |
| S9 S2 R17 R49 Ex7 | 3 / 6 | none (header note, S2 Kolín note, R17 list, Not modelled) |
| Trains S4 to S3 | 2 / 4 | none (header note, Not modelled) |
| Trains S5 to S4 | 9 / 12 | S40 Slaný 89 S:29 → 91 S:31, stay 64 → 66; Kralupy stay 114 → 112; round trip |

## For the orchestrator (outside this check's bounds)

- `S9 S2 R17 R49 Ex7.html` was rebuilt on Windows and now has CRLF line endings; the snapshot (and the repo copy) has
  LF. Content diff is as listed above; a git diff will show every line changed. The other four already had CRLF.
- kb notes now out of date (not edited here): `kb/notes/s75-beroun-rakovnik.md` (Zbečno wait ":22 – :26" → the page
  now shows Os 7745, :23 – :26, 3 min; Rakovník 61 min), `kb/notes/s5-to-s4-corridor.md` (S40 back :31), and
  `kb/rules/rail-sheets.md` could name `check_track.py` / `check_followers.py` next to `check_meetings.py`. No rule
  changed, so no lessons.md entry is needed for this check.
