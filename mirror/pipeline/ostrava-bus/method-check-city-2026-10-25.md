# Method check of the Ostrava city sheets and the Havířov/Karviná/Orlová town sheet (25 Oct 2026)

The owner asked to "verify all sheets with this level of detail" after a hand check found scripted rows wrong ("that's the
point of you doing it, so you'll not produce incorrect results"). This file covers four sheets:

| Sheet | Pipeline | Rule set |
|---|---|---|
| Ostrava Tram Vypravenost | `ostrava/` | big city: each line at its own afternoon peak, rows exact over the longest stretch |
| Ostrava Trolleybus Vypravenost | `ostrava-trolleybus/` | big city |
| Ostrava Bus Vypravenost, DPO lines only | `ostrava-bus/` | big city (the Hranečník ODIS cards and the sad B. Němcové section are not part of this check) |
| Havířov-Karviná-Orlová Bus Vypravenost | `havirov-karvina-orlova/` | small town: `../bus-schedule-method.md` v4, Step 4 on every row |

Data: each sheet's own stored trips (`data/derived/trips.json`, JDF of the sheet's day); no fetch. Typed values are
(real − 61) mod every (every terminus is a loop on these sheets, offsets count from 01:00); real times below are clock times.
Tools (scratchpad, not part of the pipelines): a per-row dump of each row's own trips in the line's window
[anchor − 30, anchor + 90] with each departure's distance to its slot and the exact candidates at every interval dividing
1440; and, for the town sheet, `audit/step4.py`'s test applied to every timed row as rendered (window slots = real
departures ± 1, and ≥ 80 % of window slots with a real departure within 3 min; then a search for a passing pattern).

## Summary of changes

| Sheet | Line | Entry | Old | New | Buses |
|---|---|---|---|---|---|
| Ostrava bus | 21 | both | approximate, up to 1 / 0 min off | same values, labelled as the timetable within 1 min (`schedule_overrides`) | 4 → 4 |
| Ostrava bus | all | To check list | 5 rows (only approximate rows with more slots than real departures) | 18 rows: every approximate DPO row | — |
| Ostrava bus | 38 | slower option | every 60, up to 18 min off | every 40, Hranečník :24 / Bartovice :25 (`check_alt`) | 2 (option) |
| Town | 515 | Fryštát → Důl Darkov | every 480, Offset 233 (12:54) | every 480, Offset 201 (12:22) | 1 → 1 |
| Town | 420 | Zelené Město → Podlesí | every 160, Offset 82 (13:03, 15:43) | every 160, Offset 80 (13:01, 15:41) | 1 → 1 |
| Town | 419 | both | automatic every 60, Šumbark Offset 24 (:25) / obchodní dům Offset 54 (:55) | hand-set every 160, Šumbark Offset 69, Also at 119 (15:30, 16:20) / obchodní dům Offset 89, Also at 159 (15:50, 17:00) | 1 → 1 |
| Town | 411 | both | every 60, Podlesí Offset 4 (:05) / Adámek Offset 32 (:33) | every 480, Podlesí Offset 308, Also at 364, 469 (14:09, 15:05, 16:50) / Adámek Offset 20, Also at 337, 392 (17:21, 14:38, 15:33) | 1 → 1 |

No vehicle moved on any sheet. The tram and trolleybus sheets are unchanged (rebuilt byte-identical to the snapshot).

## The audit's counts, reconciled

`audit/city_systemic.py` reads `derived/schedule.json` (and `odis.json['schedule']`), which still hold the automatic fits of
lines whose rows are set by hand elsewhere. So its "approximate" counts are not the rows on the sheets:

- **Ostrava bus, 28:** 20 are DPO rows (21, 26, 29, 38, 52, 62, 64, 67, 79, 83, 96), all judged below. 8 are the automatic
  fits of the ODIS lines 383, 442, 534, 535 in `odis.json['schedule']`; their cards use the hand-set `hand_lines` instead
  (Hranečník section, out of scope). After this check: 26 (21's two rows are no longer approximate).
- **Town, 31:** 29 are automatic rows of lines that `line_overrides` replace or carry (401, 405, 409, 411, 417, 418, 420,
  501, 502, 504, 513, 514, 516, 517, 520); they are not on the sheet. The other 2 are 419, the only automatic approximate
  line the sheet showed; it is now hand-set too. The count stays 31 because `05_schedule.py` still writes those automatic
  rows. The rows on the sheet are 77 timed entries: the automatic rows of 402, 403, 404, 410, 412, 413, 415, 416, 421, 434,
  511, 512, 518, 519 and the hand-set legs in `roster.json`.
- **41 ORIGIN (ostrava-bus): a false alarm, confirmed.** The owner's hand line has two Hrabůvka, Poliklinika entries with
  `loop: false` (Poliklinika is a through stop of the circuit from Výškovice, not a loop terminus). So typed = (real − 60)
  mod 60 = 22 / 52, as on the sheet; the audit's 21 / 51 assume a loop. Left as it is.

## Ostrava bus: the 20 approximate DPO rows

Per row: the real departures of the row's own trips in the line's window, with each one's distance from the slot.

| Line | Entry | Set | Real departures in the window (distance) | Verdict |
|---|---|---|---|---|
| 21 | Hranečník → Horní Datyně | every 20, :16 | 13:40–15:40: 13:55 (1), 14:16, 14:36, 14:56, 15:16, 15:36 (0) | **exact within 1 min** (13:35 and 13:55 run at :15 / :35 / :55, then :16); mislabelled |
| 21 | Horní Datyně → Hranečník | every 20, :19 | 13:59 … 15:39 all 0 (exact 13:39–16:19) | **exact**; mislabelled |
| 26 | Proskovice → Dubina | every 30, :26 | 15:30–17:30: 15:31, 15:51, 16:31, 16:51 (5 each) | irregular for the line; see below |
| 29 | Hranečník → Šenov | every 60, :21 | 16:24 (3), 17:19 (2) | irregular: drifts from :24 to :19 at 17:00; within 3 min |
| 29 | Šenov → Hranečník | every 60, :53 | 15:56 (3), 16:51 (2) | irregular, within 3 min |
| 38 | Hranečník → Bartovice | every 30, :27 | 15:51 (6), 16:24 (3), 17:04 (7), 17:26 (1) | irregular; slower option every 40, see below |
| 38 | Bartovice → Hranečník | every 30, :25 | 15:46 (9), 16:25 (0), 17:04 (9), 17:24 (1) | irregular at every 30; every 40 is exact, see below |
| 52 | Šilheřovice → Křižíkova | every 30, :05 | 13:30–15:30: 13:35, 14:05, 14:35 (0), 14:55, 15:15 (10) | irregular: the line's own peak straddles a phase change from :05/:35 to :15/:45 (14:55 extra) |
| 52 | Křižíkova → Šilheřovice | every 30, :07 | 13:36 (1), 14:04, 14:40, 15:10 (3) | irregular (:06/:36, then :10/:40 from 14:40), within 3 min |
| 62 | Nová huť garáže → Sámova | every 60, :06 | none in 15:30–17:30; the line's two shift trips are 14:10 and 15:02 | sparse; already on the list |
| 64 | Svinov → Hýlov | every 60, :15 | 16:05 (10), 16:25 (10), 17:25 (10) | see below: 16:05 and 17:25 are Klimkovice, centrum short trips merged into the row |
| 64 | Hýlov → Svinov | every 60, :47 | 15:45 (2), 16:50 (3) | irregular after 15:45, within 3 min |
| 67 | Křižíkova → Hlučín AN | every 60, :01 | 13:10–15:10: 13:16 (15), 13:56 (5), 14:46 (15) | irregular (gaps 40, 50, 90 min) |
| 67 | Hlučín AN → Křižíkova | every 60, :16 | 13:26 (10), 14:06 (10) | irregular |
| 79 | both | every 120 | one trip each way in the window (17:40 / 17:46; the other is 13:00 / 13:06) | a two-trip line; already on the list |
| 83 | both | every 120 | Dubina 15:02 (0); Mošnov 14:40 (1), 16:55 (14) | a two-to-three-trip line; already on the list |
| 96 | Poliklinika → Korýtko | every 60, :38 | 13:40–15:40: 13:43 (5), 14:38, 15:38 (0) | irregular (:43 → :38 at 14:38) |
| 96 | Korýtko → Poliklinika | every 60, :06 | 14:08 (2), 15:03 (3) | :06 is the shortest-wait choice: the real bus turns at Korýtko in 0 min (13:43 arr 14:08 → 14:08), so :03 would need a second bus |

Findings:
- **21 (changed, label only).** Both rows are the real timetable (within 1 min), and both ends are at the same rate. They
  were marked approximate because `plans` falls back to an averaged slot when the two ends' strict exact runs differ (the
  out end alone fitted every 45). Set in `config.schedule_overrides['21']` with the same real minutes and a `label`, so the
  card says "the timetable within 1 min (method check, 25 Oct 2026)" instead of "approximate", and the rows stay off the
  To check list. `05_schedule.py` passes an override's `label` on; `06_render.py` uses it in place of "set by the owner …
  spaced from the other branch" (that text stays for the owner's spacing overrides). Typed values unchanged; 4 buses. Files touched on this sheet: `config.json` (`schedule_overrides['21']`, `check_alt['38']`, `check_alt_why`), `scripts/05_schedule.py` (passes an override's `label` on), `scripts/06_render.py` (the label text, every approximate DPO row on the To check list, `check_alt`, each row's own window in the table).
- **38 (option offered).** The line's own timetable from 13:00 to 17:00 is every 40 with 2 buses: from Bartovice,
  Ještěrka 13:04, 13:44, 14:24, 15:06, 15:46, 16:25, 17:04 (all within 1 min of :25); from Hranečník 13:11–15:51 at :31,
  then 16:24 and 17:04 (7 min earlier). After 17:04 it steps up to about every 20 (17:24/17:26, 17:47, 18:09), which is
  where the band's fourth departure comes from. Every 30 (now) matches the band's count, 4 each way, but every slot is up
  to 7 / 9 min off. Every 40 (Hranečník :24, Bartovice :25) has 3 slots against 4 real departures: Bartovice exact, Hranečník
  2 of 3 exact (15:44 against 15:51), 2 buses (waits 24 and 23 min). It is fewer departures than the band, so it is the
  slower option, not a fix. It replaces the computed one (every 60, up to 18 min off) on the To check list and the cards
  (`config.check_alt['38']`). Owner's choice; switch both ends together.
- **26.** Proskovice runs in pairs, :31 / :51, from 14:51 to 16:51 (exact every 60 with two slots, the same rate as now).
  But the Dubina end is the owner's spacing override (every 30 :07, 22 Oct, from 59), and :31 / :51 against :07 / :37
  needs 3 buses instead of 2 (the :37 bus reaches Proskovice at :52, just after :51). Left approximate, on the list.
- **64.** The Hýlov trips themselves are hourly :15 / :45 from 13:15 to 15:45 (3 each way), then 16:25 / 16:50; the
  "up to 10 min" comes from the Klimkovice, centrum short trips (16:05, 17:25, 18:05) folded into the row. The pattern is the
  line's own; only the last trips shift by 10 min. Left, on the list.
- **29, 52, 67, 96:** genuinely irregular in the line's window, no exact pattern at the same rate covers it; no slower
  option fits (the computed alternatives are faster). Left, on the list. **62, 79, 83:** sparse shift / two-trip lines,
  already on the list since 20 Oct.

**To check list (changed).** It listed only approximate rows with more slots in the window than real departures (5).
The rule is that every approximate row is listed with its slower option ("Anything approximate is labelled with its largest
deviation, and listed for the owner to check with the slower alternative"). `06_render.py` now lists every approximate DPO
row (the Hranečník ODIS cards keep their own list), with a card note that says how far off the slots are; the table shows
each row's own window (it said 15:30–17:30 for all, wrong for lines anchored elsewhere). 5 → 18 rows: 26, 29 ×2, 38 ×2,
52 ×2, 62, 64 ×2, 67 ×2, 79 ×2, 83 ×2, 96 ×2.

### Exact rows with short stretches (Ostrava bus)

Every exact row whose exact run is under an hour or leaves real departures of the window outside it was dumped. None is
wrong; the short labels come from extra trips that break the strict run:
- 31 Nová huť garáže → Výškovice ("exact 13:07–14:07"): really :07 / :27 / :47 to 15:07, plus a 14:15 extra.
- 48 PZ jih → Opavská ("13:08–13:58"): every 10 at :x8 to 16:18, plus four shift-end extras 14:07–14:13.
- 61 Výškovice → Hranečník ("15:40–16:40"): every 20 at :00 / :20 / :40 from 13:00 to 16:40, plus 14:50 and 15:30.
- 45 Rudná → Poruba: every 20 from 15:04; 13:51–14:48 is the shift-end surge (5 departures in an hour), outside the run.
- 24, 98: the line winds down inside its window (24 every 10 → 20 → 30; 98 every 20 → 30 at 14:15); the row takes the
  longest exact stretch. 59: the owner's spacing overrides (21 Oct). 30, 33, 55: exact to 16:30–16:45, then the evening shift.

## Ostrava trams and trolleybuses

No approximate rows. Every exact row was dumped against the band 15:30–17:30. All runs cover the band or most of it; the
departures outside them are phase shifts at the end of the peak, or pull-ins:
- Tram 13 Zábřeh → Hranečník: 16:47, 17:07, 17:27 are run-ins to Moravská Ostrava, Plynárny (depot direction, merged as
  pull-ins; depot runs are never modelled). Tram 4: every 20 until 15:34, then the 4A / 4B every 30 from 15:54. Tram 5: the
  rows run from 16:10 / 16:33 to the evening; 15:37–16:17 is irregular. Trolleybus 104 Náměstí Republiky → Michálkovice
  ("exact 16:00–17:00"): every 10 all afternoon, drifting 1 min (:x0 / :x1). Trolleybus 103, 105, 107: every 20 to 16:23–16:52,
  then the timetable shifts by 2–7 min.
- Checked, nothing to change. Both sheets rebuild byte-identical to the 25 Oct snapshot.

## Havířov / Karviná / Orlová: Step 4 on every row

77 timed entries on the sheet. In each row's own window (the hand line's `window`; for automatic rows the anchor's band):
**50 passed and 27 failed** before this check; **57 pass and 20 fail** after it. Every remaining fail is explained below.

### Changed (Step 4 failed, a passing pattern exists, same bus, no recorded owner decision against it)

- **515 Fryštát → Důl Darkov.** Window 11:40–15:00 has one real departure, 12:22; the slot was 12:54 (32 min off; chosen
  over the whole day to sit near 4:54 and 20:56). Now 12:22 (the afternoon wins, method "Which hour"). The back slot
  14:10 is unchanged (exact, also 22:10). Typed 233 → 201. 1 bus; the same bus (50-1004).
- **420 Zelené Město → Podlesí.** Real 13:03 and 15:38, 155 min apart, on an every-160 line; at 13:03 / 15:43 the 15:38 trip
  was 5 min off (1 of 2 window slots within 3 min). At 13:01 / 15:41 both are within 3 (2 and 3 min). Out of Podlesí (12:30,
  15:10, exactly 160 apart) unchanged. Typed 82 → 80. 1 bus, the same (40-4004).
- **419 Šumbark ⇄ Město, obchodní dům** (the only automatic approximate line on the sheet). One bus shuttling irregularly:
  Šumbark 13:15, 14:10, 15:30, 16:20, 18:07, 19:00; obchodní dům 13:50, 14:50, 15:50, 17:00, 18:30. The automatic every 60
  at :25 / :55 had **no real departure within 3 min all day** (all 5–25 min off): Step 4 0 of 2 window slots. No hourly
  phase passes (15:30 and 16:20 are 50 min apart). Every 160 with two slots each way passes and is the real afternoon:
  Šumbark 15:30, 16:20 (repeating 18:10, 19:00 = real 18:07, 19:00), obchodní dům 15:50, 17:00 (repeating 18:30 = real).
  Window 15:00–19:00: 3 of 3 each way. 1 bus, the same designed bus (40-4005). Set in `line_overrides['419']`. The simpler
  option (every 60 at :25 / :55, 1 bus) is in its `why` and goes to the owner.
- **411 Podlesí ⇄ Horní Bludovice, Adámek.** One bus back to back: Podlesí 14:09, 15:05, 16:50; Adámek 14:38, 15:33, 17:21
  (18:25 to Lapačka is 411B). The hourly hand-set (Podlesí :05, Adámek :33) had 4 slots in 14:00–18:00 with only 15:05 /
  15:33 on a real trip (14:09 / 14:38 4–5 min off, nothing at 16:05 / 16:33, 16:50 / 17:21 12–15 min off): 1 of 4. No
  hourly or 2-hourly pattern passes. Every 480 with the three trips each way is exact (3 of 3), the 290 precedent ("an
  exact multi-slot row on a long interval beats a simpler interval that fails Step 4"). 1 bus, the same (40-2002). In the
  game it repeats at 6:09 / 7:05 / 8:50 (real 6:05) and 22:09–1:21. The simpler option (hourly, 1 bus) goes to the owner.

Each of these lines' cards and the README record the change. The four lines leave the "Hand-set rows to check" list
(20 → 16).

### Left, with the reason

Window-edge effects (the sheet's own check counts slots over the span of the real departures, and they pass it):
- 401B Prostřední Suchá → Šumbark :58: 15:58, 16:58 real; the 17:58 slot is after the shuttle's last return (the 17:29 bus
  goes on as another line). 409 Šumbark → Podlesí :52: the evening line starts at Podlesí 16:46, so the 16:52 slot of the
  16:00–19:30 window has no trip. 505 Lutyně, pošta → Věřňovice: the 19:07 slot is after the circuit's last round; its
  15:12 start (from Lutyně AN) is 5 min off :07 and is on the To check list.
- 402 Albrechtice → Šumbark every 30 :07: one trip missing (16:37) in an otherwise exact every 30 (14:07–19:07); 3 of 4 = 75 %.
- 511 (circular) every 60 :10 / :30: exact all day to 16:30, then 16:50, 17:40 (the evening form); the 17:10 slot is empty.

Recorded owner structure (on the sheet's To check list where it has trips off the pattern):
- 501 / 501B / 504 (Ex4, the owner's own method and request "Could we take 503 to be one of the legs of the 501/504?"):
  501's 13:06 and 14:18 slots have no trip (the README's accepted differences); 504's legs fail one by one because the circuit
  alternates two paths; together its Lazy slots are every 120 at :06 (12:00 and 14:00 real, 6 min off).
- 502 (daytime line, the method document's own example): hourly :01 / :18 with gaps at 11 and 13 h.
- 402B, 411B, 418, 515B, 420's every 160 (no daily lines, "bend the reality a bit"): one slot per sparse trip group.
- 514 (with 520 and 513 carried): whole-day reading by a4. In the afternoon window its 520 leg (:25) has 0 of 4 slots
  within 3 min (real 15:30, 17:30, 18:12, and 513's short returns 16:20, 18:28). :30 would put the bus into Fryštát at
  :30 for the :27 departure, a third bus. Left, on the list.
- 516 and 517: "left as approximate on purpose" (README); on the list.

Not changed although it fails, put to the owner:
- **410B Podlesí ⇄ Dolní Datyně** (automatic). Podlesí → Dolní Datyně is hourly (12:05, 13:10, 14:10, 15:15) but only every
  second bus comes back to Podlesí (13:35, 15:32); the others go on towards Šumbark as 410A. The row from Dolní Datyně at :32
  is labelled "exact", but its 14:32 slot has no trip (1 of 2 window slots). By the v4 outstation rule the branch would run
  at the inbound rate: every 120 with the same offsets (Podlesí Offset 11 = 13:12 / 15:12, Dolní Datyně Offset 31 = 13:32 /
  15:32), 1 bus. Tried through `line_overrides` (410A and 410B hand-set with the same values): the bus matching of
  hand-set lines then moved buses on 404, 405, 406, 410, 417 and 421, so it was reverted. It needs either the owner's
  go-ahead to rebalance those buses, or a per-row override in the town 05_schedule (the Ostrava `schedule_overrides`), which
  this pipeline does not have.

### Exact automatic rows

Short exact stretches checked: 410 (2-trip rows, above), 421 (3 trips 13:41–15:42, the line's whole afternoon), 512
(4 slots exact in the window), 518 (hourly :30; its :05 trips, 14:05, 15:05, 18:05, 19:05, are a second pattern outside the window). All
other automatic rows pass Step 4; their exact runs span 2–5 hours.

## Vehicles and verification

- Every change was rebuilt and diffed against `_snapshots/2026-10-25/html` with `audit/htmldiff.py`; `roster.json` was
  diffed against the pre-change copy after each change.
- Ostrava bus: no need or vehicle changed (21's need stays 4; the rest are labels). The snapshot predates nothing here;
  its Hranečník ODIS cards and the sad B. Němcové section are byte-identical: `07_odis.py` and `04_roster.py` write the
  waits of hand-set lines (five ODIS cards, DPO 57) in a hash-dependent order (`lib.slot_need` iterates a set), and
  `08_hubs.py` now picks up a newer Opavsko card text for 290 ("The owner chose this over every 40 …"). So the published
  `odis.json` and `hubs.json` were kept for the render, and `04_roster.py` was run with `PYTHONHASHSEED=4`, which writes
  57's waits in the published order (the roster is otherwise identical to the published one except 21's approximate flag). A fresh `run.py` would add that Opavsko sentence to the 290 hub card; that is the Opavsko sheet's change, not this
  one's.
- Town: the same buses on every line; only two "seen at" times moved by 2–4 min with the slots (40-4004 13:13 → 13:11,
  40-2002 14:15 → 14:19). The pak table row "SOR NBG 18, Havířov city blue, 8 + 8" now reads "9 + 5": `06_render.py` reads
  the installed pak's lengths, which changed after 20 Oct; not a schedule change.
- **To reproduce the published bus sheet:** `python scripts/run.py`, then copy `odis.json` and `hubs.json` back from
  `../_snapshots/2026-10-25/derived/ostrava-bus/` (identical to the published ones), then
  `PYTHONHASHSEED=4 python scripts/04_roster.py && python scripts/06_render.py` (from `scripts/`). The lasting fix is to make
  `slot_need` in `ostrava-bus/scripts/lib.py` iterate a sorted list instead of a set (one line in the shared lib; not done here).
- 419's card now shows its hand-set line's table ("every 50 min" / "single trip" in 15:00–17:00, "buses" without "at 16:00"):
  the renderer's usual display for hand-set lines, not a modelling claim; the schedule rows are the values to type.
- `audit/city_systemic.py` after the changes: no RANGE, FOLD or RATE on the four sheets; ORIGIN only the 41 false alarm;
  Ostrava bus approximate 28 → 26.
