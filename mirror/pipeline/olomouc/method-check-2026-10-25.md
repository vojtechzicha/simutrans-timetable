# Method check, 25 Oct 2026: Olomouc trams, Olomouc buses, Most–Litvínov trams, Most–Litvínov buses

Owner, 25 Oct 2026: "that's the point of you doing it, so you'll not produce incorrect results." I checked every Simutrans row of
the four sheets against the real timetable and the rules in `kb/rules/fork-schedule.md`, `city-fleet-sheets.md` and
`bus-sheets.md`. These are city networks, so I used the afternoon-peak method, not the regional whole-day one (see question Q1).

The offset-origin fix from earlier today is kept: typed = (real − 60 − 1 at loops) mod every. Below, *real* means the timetable
minute. For a typed value v it is (v + 61) mod every at a loop, v + 60 elsewhere, counted from 01:00.

## What was checked, per row

For every timed entry I took the real departures of that direction 13:00–19:00. I included folded variants. Trips starting at a
folded stop were read where they pass the terminus. I then checked:

1. the current pattern's longest exact run, and how far it covers the line's own busiest 2 h in 13:00–18:00 (15:00–17:00 when
   that is within one departure of the busiest 2 h);
2. the peak departures off the pattern, and the slots with no real departure behind them;
3. every other exact pattern (intervals dividing 1440, up to 120 min, at most 8 slots), at the same rate first;
4. the rules: both ends of a line at the same rate, offset < interval, at most 8 slots, evenly spaced slots folded, −1 only at
   loops, and no 720/1440 on bus sheets.

Tools: the scratch search and report scripts of this session, plus `pipeline/audit/city_systemic.py`. Each change was rebuilt
from stored data (`python -X utf8`, no fetch) and diffed with `pipeline/audit/htmldiff.py` against
`pipeline/_snapshots/2026-10-25/html/` and against the sheet as it stood before this check.

**Rule check after the changes:** ORIGIN, RANGE, FOLD and RATE are all 0 for all four sheets (olomouc 14 rows, olomouc-bus 37,
most-litvinov 8, most-litvinov-bus 29).

## Most–Litvínov buses (`pipeline/most-litvinov-bus`)

### Finding 1: RATE on line 10, Most, nádraží ⇄ Obrnice, sídliště. Fixed.

The sheet had Most every 45 at 15:11 / 15:41 (2.67 an hour) and Obrnice every 60 at :08 :34 (2 an hour). That is not one rate.

Real departures, from Most: 13:26 13:41 14:11 14:26 14:41 15:11 15:41 15:56 16:26 17:11 17:56 18:26 18:56. From Obrnice: 13:19
13:48 14:08 14:23 14:44 15:08 15:34 16:08 16:29 16:53 17:34 18:23 18:50. The line has two path variants (via Rudolice, náměstí or
direct, 10–20 min). From 13:30 to 16:12 three buses run it, and two after that (the sheet sizes at 16:00: 2 buses).

Candidates at 2 an hour, both ends:

| Pattern | Most, nádraží | Obrnice, sídliště | Buses |
|---|---|---|---|
| every 30 / every 60, best exact | every 30 :11 :41, exact 14:41–15:41 (3 departures) | every 60 :08 :34, exact 15:08–16:08 (3) | 2 |
| every 30 approximate | :11 :41, largest deviation 15 min (15:56, 16:26) | :08 :38, largest deviation 15 min (16:53) | 2 |
| **every 120, 4 slots (chosen)** | 15:11 15:41 15:56 16:26, **exact 15:11–17:11 (5)** | 15:34 16:08 16:29 16:53, **exact 15:34–17:34 (5)** | 2 |

By the fit rule, the 2-hour cycle wins: it has the longest exact run at the shared rate, and the every-30 and every-60 options
cover only 3 of 5 (60 %, under the 80 % threshold). I checked the pattern need with the card's running times (Most → Obrnice 16,
Obrnice → Most 13) and a 3-min layover: 2 buses, the number assigned. It holds while Obrnice → Most takes at most 15 min and Most
→ Obrnice at most 20 min. At the slowest variant times (20 / 19) it needs 3 buses. Every 30 holds with 2 buses at any variant
time.

How it is set: `config.schedule_override["10"]`, a new mechanism in `05_schedule.py` modelled on the tram pipeline's. The line
card note says the same. The renderer now prints real clock times for intervals that do not divide 60. It used to print
"11, 41 (mod 45)".

### Finding 2: RATE on line 13, Lom, Loučná, Libkovická ⇄ Litvínov, Janov, otočka. Fixed.

The Lom end was every 60 at :12 :57 (2 an hour) and Janov every 15 at :13 (4 an hour). The Janov row folded in the Osek and Lom
ČSA trips that start at Janov. At the Lom end those trips start at other stops (Osek, Kolonie; Lom, Československé armády), so
they were left out of the Lom row.

Evidence (`data/derived/trips.json`, stop sequences): **every** trip of 13 passes both Janov, otočka and Lom, Loučná,
Libkovická. The Osek and ČSA trips run on from Libkovická, and the Křížatky trips start two stops before Janov. Read at those two
stops:
- Janov → Lom: :13 :28 :43 :58 without a gap, 12:58–18:43.
- Libkovická → Janov: :12 :27 :42 :57 without a gap, 13:27–18:57. (12:27 and 12:57 also run; 13:12 does not.)

New rows: every 15 at both ends, exact 13:13–18:43 and 13:27–18:57. The fit window starts at 13:00. How it is set:
`config.core_points["13"]`, which reads each trip at the core points it passes (the bus-sheet rule). The old "Other variants"
rows are gone, including a stray Osek, Kolonie → Janov "every 60, Offset 30" row. The card note explains the change.

Buses: 7 are assigned (round trip 4 plus 3 for the branch variants). Sized from the new pattern (Janov turns in 0 min in the
timetable, Lom in 3) the line needs **5**, so 2 stay unused in the game. No vehicle moved; see Q3.

### Rows checked and left

- **9** (loop, Most, Dopravní podnik, 1 bus): every 30 :16 :46, exact only 15:46–16:16 (2 departures). In 15:00–17:00 there are
  2 real departures and 4 slots, and the real line runs about once an hour (13:01 14:01 14:46 15:46 16:16 17:01 18:01). No exact
  pattern at 1 an hour covers the peak. The options are every 60 :46 (exact 14:46–15:46, 16:16 off by 30) and every 60 :01 (all
  day, the peak trips off by 15). Left for the owner (Q4); it is the busier pattern.
- **12** (Chempark shift line): Chempark every 30 :21 :51, exact 14:51–15:51 (3). The other end has "every 0" with the real
  departures. 14:26 is off the pattern. Sparse; the line's peak is 13:52–15:52, so the fit sits inside it. Left.
- **14**: Horní Jiřetín :03 :26 holds 13:26–16:26. The only break is the extra 14:28 (a second bus on the direct route). Litvínov
  every 30 :01, exact 13:01–16:01. Both 2 an hour. Left.
- **27, 31**: sparse 15:00–20:00 fits (every 60, 2 departures) with the other end untimed, as the README describes. Left.
- **5, 15, 16, 17, 20, 22, 23, 25, 30**: exact over 2.5 to 6 h, same rate at both ends. Left.
- **Tram replacement** (Chempark ⇄ Citadela): every 15 at the tram-4 minutes, 15:36–19:06. Before 15:36 the tram-1 shift trips
  (:12 :27 :42 :57) double it. The line's own busiest 2 h is therefore 13:28–15:28 (8 an hour), but tram 1 is modelled at 16:00
  by the owner's decision of 28 Sep. Left.

## Olomouc buses (`pipeline/olomouc-bus`)

### The 3 approximate rows

- **12, Holice → Řepčín** (every 60 :23 :58, partial). The cause was the alias: Průmyslová (two stops past Holice) is folded into
  Holice, but its trips were fitted at their Průmyslová minute. The GTFS stop times show they pass Holice **4 min later**:
  13:43 → 13:47, 14:23 → 14:27, 15:03 → 15:07, 16:03 → 16:07, 16:23 → 16:27. Read at Holice, both ends of 12 run **every 20 at
  :07 :27 :47, 13:47–16:27, 9 departures in a row each**. Then at 16:47 one bus runs only to Hlavní nádraží and one goes to the
  garage, and from 17:00 the line runs every 30.

  The sheet had set 2 an hour from the 16:00–16:59 hour alone (16:07, 16:27). That left an exact run of 2 departures. Fixed:
  `rate` 3 and `fit.overrides` on both ends set every 20 at :07. The 4 buses already assigned hold it: pattern need 4, round 80
  min with the real running times 36 / 35. The rows show "set by hand, exact 13:47–16:27; added :47". The :47 slot is the
  short / garage trip.

  General fix in `03_timetable.py`: a trip from a folded stop that passes the terminus is fitted at its time there (`dep_fit`;
  `common.gtfs_trips` now also returns stop times). Needs still use the real ends. Side effects, both corrections:
  - **25** Hlavní nádraží → Nový Dvůr moves from :22 (the Kaufland minute) to :26, the real departure from Hlavní nádraží.
  - **19** Holice's exact run now reads 13:57–17:17. Its values are unchanged.
- **21, Aquapark → Hlavní nádraží** (every 30 :21, set by hand): the real 16:51 runs to the garage. Every 30 keeps the line
  balanced with Hlavní nádraží every 30 (14:12–17:12). No exact or better pattern exists: at 2 an hour the best alternative is a
  2-hour cycle exact 14:11–15:51 that loses 16:21. Left. The row now shows its exact span, 14:51–16:21.
- **26, Hlavní nádraží → Topolany** (every 60 :55, partial): real 14:55, 15:55, then 17:00, which is 5 min after the slot. The
  line is hourly and irregular with 1 bus, so there is no exact repeating pattern and no slower option. Left. A note on the sheet
  now gives the largest deviation (5 min).

### Exact rows with a short run

**Labelling fix.** Six rows had one departure in 16:00–16:59 and no repeating run, but the sheet labelled them "exact 16:38–16:38".
These are 18 (both ends), 25 Hlavní nádraží, 28 Technologický park, and 31 (both ends). They now read "single: hourly at the only
16:xx departure", followed by the other real departures 15:00–17:59. Text only; no values changed.

Checked and left:
- **11R / 11L.** From 15:00 to 16:20, Hlavní nádraží sends a bus every 10 min, alternating Radíkov :00 :20 :40 and Lošov :10 :30
  :50. From 16:20 the line runs every 30. 11R Hlavní nádraží is every 60 :00 :20 :35, exact 16:00–16:35. Every 20 :00 is
  exact 15:00–16:20, has the same single 5-min miss in 15:00–17:00, and is simpler, but it leaves a 20-min gap at Hlavní
  nádraží where today's has 15-min gaps, so it was left. 11L at 2 an hour (16:10, 16:50) and 3 an hour score the same in
  15:00–17:00. Its own busiest 2 h (14:18–16:18) is 3 an hour (Q5). Left.
- **14, 15, 20.** Irregular, and in the middle of a change of headway at 16:00. No same-rate pattern beats the current one in
  15:00–17:00. 20's own busiest 2 h (13:16–15:16) is every 20 from Farmak (Q5). Left.
- **18 Tržnice.** :38 (16:38) against :33 (13:33, 14:33, 15:33, exact 13:33–15:33). Both are 5 min off once in 15:00–17:00, a
  tie at the sheet's window. Left (Q6).
- **22 Šlechtitelů.** Every 60 :08 :40 against every 30 :08: both are 2 min off once in the peak. :40 is closer to the
  afternoon's :38–:41 departures, so it was left.
- **13, 16, 17, 19, 21 Hlavní nádraží, 27 (every 45), 28 Tržnice.** Exact over 1 to 4 h. Left.

Text fix: the schedule section said "the offset is minutes after midnight modulo the interval". It now gives the 01:00 origin.

## Olomouc trams (`pipeline/olomouc`)

All 14 rows are every 15 (lines 1, 2, 3, 4, 6, 7) or every 30 (line 5), exact over about 4 h (13:00–17:00 or longer). Rates are
equal at both ends. Loops (Fibichova, Nová Ulice, Neředín, Pavlovičky) are −1. U Kapličky (stub) keeps the real minute: 3 :06,
5 :00. The departures listed as "outside" are the minute shifting after about 17:00 (for example 1 Nová Ulice :09 → :07). The
line 6 minors are depot runs, not modelled. The 3 and 5 pool interleaves at U Kapličky (:06 :21 :36 :51 and :00 :30). Nothing to
change. Rebuilt: identical to the snapshot.

## Most–Litvínov trams (`pipeline/most-litvinov`)

Lines 2 and 4 are every 15, exact 13:00–19:00, with equal rates. Line 3 (morning only) is every 15, 5:00–6:30 and 5:12–6:12, which
is its whole service. Line 1 is the owner's designed every-60 shuttle (28 Sep), :08 / :42. Today's `loop_shift` change (order of R
kept) leaves these single-slot rows as they were. Nothing to change. Rebuilt: identical to the snapshot.

## In-game changes (old = published values)

| Sheet | Line, entry | Old: every / Offset / Also at (real) | New: every / Offset / Also at (real) |
|---|---|---|---|
| Most bus | 10 Most, nádraží → Obrnice | 45 / 10 / 40 (sheet: 15:11, 15:41, 15:56, 16:26, every 45) | **120 / 10 / 40, 55, 85** (15:11, 15:41, 15:56, 16:26, every 2 h) |
| Most bus | 10 Obrnice → Most, nádraží | 60 / 7 / 33 (:08, :34) | **120 / 33 / 67, 88, 112** (15:34, 16:08, 16:29, 16:53, every 2 h) |
| Most bus | 13 Lom, Loučná, Libkovická → Janov | 60 / 11 / 56 (:12, :57) | **15 / 11 / –** (:12 :27 :42 :57) |
| Most bus | 13 Janov → Lom, Loučná, Libkovická | 15 / 12 / – | unchanged |
| Most bus | 13 Osek, Kolonie → Janov ("Other variants") | 60 / 30 / – | dropped: not a stop of the Janov – Loučná line |
| Olomouc bus | 12 Řepčín, železárny → Holice | 60 / 6 / 26 (:07, :27) | **20 / 6 / –** (:07 :27 :47) |
| Olomouc bus | 12 Holice → Řepčín, železárny | 60 / 22 / 57 (:23, :58) | **20 / 6 / –** (:07 :27 :47) |
| Olomouc bus | 25 Hlavní nádraží → Nový Dvůr | 60 / 21 / – (:22) | **60 / 25 / –** (:26) |

The Most bus 10 row also had an offset-origin fix earlier today (every 45: 40 / 25). That value is replaced by the row above.
Olomouc bus 27 keeps today's offset-origin fix (every 45: Offset 15 → 0). No vehicle moves: Most bus 10 keeps 2 buses and 13 keeps
7; Olomouc bus 12 keeps 4.

## Questions for the owner

- **Q1. Is Most–Litvínov a "small town" for the regional whole-day method?** The sheet uses the city afternoon-peak method.
  Under the whole-day method these sparse and irregular lines would come out differently: 9, 10, 12, 27, 31.
- **Q2. Line 10, Most bus.** Its own busiest 2 h is 13:12–15:12, at 3 an hour with 3 buses: every 60 :11 :26 :41 from Most,
  exact 13:26–15:11, and :08 :23 :44 from Obrnice, exact 14:08–15:08. The sheet sizes at 16:00 with 2 buses. Also, the 2-hour
  pattern needs the direct-route running times (see above); every 30 at both ends is the simple fallback (up to 15 min off).
- **Q3. Line 13, Most bus.** The Osek, Kolonie branch (6 trips each way 13:00–19:00) and the Lom, Československé armády branch
  (hourly, Janov :28 / ČSA :14, 6 each way) pass the "regular afternoon branch" test (at least 3 each way 13:00–19:00). No modelled
  line serves their stops. Should they become their own Simutrans lines, interleaved on the 15-min trunk? As the sheet stands, the
  pattern needs 5 buses and 7 are assigned.
- **Q4. Line 9, Most bus.** Keep every 30 :16 :46 (about twice the real service in the peak), or use every 60 :46 or :01? It needs
  1 bus either way.
- **Q5. Own-peak anchoring on the Olomouc bus sheet.** 11L (14:18–16:18) and 20 (13:16–15:16) run 3 an hour at their own peak.
  The sheet models 16:00, where they are changing to every 30. At every 20, 20 needs 6 buses (5 are assigned). 11L needs 3 (as
  assigned) with the timetable's 2-min turn at Lošov, and 4 with a 3-min turn.
- **Q6. Olomouc bus 18, Tržnice.** :38 (the 16:38 trip) or :33 (13:33–15:33 exact)? They tie at 15:00–17:00.

## Files changed

- `most-litvinov-bus/scripts/05_schedule.py`: the `core_points` and `schedule_override` mechanisms.
- `most-litvinov-bus/scripts/06_render.py`: real clock times for intervals that do not divide 60.
- `most-litvinov-bus/config.json`: `core_points["13"]`, `schedule_override["10"]`, line notes 10 and 13.
- `most-litvinov-bus/README.md`: decisions.
- `olomouc-bus/scripts/common.py`: `gtfs_trips` also returns stop times.
- `olomouc-bus/scripts/03_timetable.py`: `dep_fit` for folded stops, and the `override` flag on rows.
- `olomouc-bus/scripts/05_render.py`: "single" and "set by hand" labels.
- `olomouc-bus/states/2026-09-29.json`: 12 `rate` 3 with two `fit.overrides`, 12 text, 26 note, schedule text.
- `olomouc-bus/README.md`: decisions.
- Rebuilt: `Most-Litvinov Bus Vypravenost.html` and `Olomouc Bus Peak Fleet.html`. The two tram sheets were rebuilt and are
  unchanged.

Not mine, left in place: `most-litvinov-bus/data/derived/schedule-VZ MacBook Pro.json` is a OneDrive conflict copy of an older
`schedule.json` (the published values). The pipeline does not read it.
