# Simutrans fork: schedule fields and how sheets fill them

Every sheet ends in values the owner types by hand into their own fork of Simutrans 122.0. There is no import.
These are the facts about the fork and the conversion rules every sheet (city, bus, rail) follows.

Source of the engine facts: the engine sessions (`simutrans-122-0-*`, repo `C:\Users\vojte\Developer\simutrans-122.0`,
its `CLAUDE.md` has the "Coupling trains" section). Engine questions go to an engine session, never to the pak session.

## The fields (per stop entry, Scheduling tab)

| Field | Meaning |
|---|---|
| **Departure every (min)** | The interval. `0` = no timetable at this entry. |
| **Offset (min)** | First slot; must be `< interval`. |
| **Also at (min)** | Up to **7** extra offsets → at most **8 departures per cycle**. Cannot change the route. |
| **Leave up to (min late)** | Default automatic (half the gap). Rail sheets use 30 at headways over 60. |

- Only works with the calendar on (`minutes_per_month`; the owner plays at 480).
- Whole calendar minutes only. Never show ½ minutes; round down like the printed timetable.
- Use an interval that divides 1440, or the pattern restarts at midnight. Prefer intervals dividing 60.
- Spacing within a line is automatic: each slot goes to one vehicle. No per-vehicle offsets.
- Lines do not coordinate with each other: interleave them by choosing offsets.
- JSON export of a save: `simutrans -load NAME -export FILE.json` (ask the engine / fleet desk session; the game must be closed).

## Offsets: where minute 0 is

- **Rail and every interval that does not divide 60:** offset = **(real time − 60) mod interval** — "odd hours first".
  With interval 120, offset 4 = L:04 (odd hours), offset 66 = S:06 (even hours). User-confirmed for 120 and 240 (8:08 → 188).
- `mirror/pipeline/README.md` still says offsets "count from midnight": that wording predates the owner's 3 Oct correction —
  **this page wins**.
- City sheets with intervals dividing 60 are unaffected. A 20 Oct 2026 bug in the shared Ostrava `loop_shift` ignored the 01:00
  origin for intervals like 40/45/80/90/120 — check any sheet using such intervals.
- **Every city pipeline uses `(real − 60 − 1 at loops) mod interval`** (fixed 25 Oct 2026 in the Brno, Olomouc, Plzeň, Praha and
  Most–Litvínov copies, which still counted from midnight; the Prague metro / ferry rows too). After any change to a typed value,
  run `pipeline/audit/city_systemic.py`: it reports ORIGIN, RANGE (> 8 slots, out of range), FOLD and RATE (ends at different
  rates) for every city pipeline and must come back clean.
- **Fold evenly spaced slots:** never write "every 60, Offset 17, Also at 47" — it is "every 30, Offset 17". A shared interval
  from interleaving must be folded back per row before output.

## Loop termini (smyčka) — the −1 rule (owner, 28 Sep 2026)

- A vehicle departing a **loop** is set **1 minute before** the real departure, so it clears the loop on time.
  Offset and each Also at become `(real − 1) mod interval`; the interval is unchanged.
- **Stub and turn-back termini keep the real minute.** Through stops keep the real minute.
- Every sheet says this visibly and shows the real minutes under the typed values ("real N" subtitles). Work the subtitle out
  from each typed value (+1 at loops), never by listing fit order — that mislabelled patterns wrapping past :00.
- Trolleybus sheets treat every terminus as a loop (block turns included). Bus sheets (Ostrava, ODIS): all termini −1.
  Rail termini keep the real minute.
- Watch for text like "no loop" in source data — it once made the rule catch a through stop (Prague Nádraží Holešovice).

## Which entry carries the timetable

- The entry the vehicle **leaves from** (the boarding stop of a loop).
- Set timetables on termini and on timing points only.
- Buses: time the **terminal**, worked back from the knot (terminal departure = knot time − running time); the knot itself gets no
  timetable. Trains: time the stations where they wait (see [rail rules](rail-sheets.md)).

## Fitting real departures to the fields

- For each terminus and destination, take the longest stretch of the (line's own) afternoon peak that one interval + offset +
  Also-at set reproduces **exactly**. Clip to the pattern's first and last real departure; < 2 departures is never a fit.
- Prefer the simplest pattern (fewest slots, then shortest interval) among fits covering ≥ 80 % of the best.
  Prefer intervals dividing 60, then dividing 1440.
- De-duplicate candidate runs on (slots, start, end), not on the slot set alone (bug fixed 28 Sep in every `runfit` copy).
- Anything approximate is labelled with its largest deviation, and listed for the owner to check with the slower alternative.
- **Both ends at the same rate.** Unequal departures/hour at the two ends of a line cannot run in Simutrans (Ostrava 4, 18 Oct).
  Pair each A→B fit with its B→A fit; if rates differ, try every candidate rate on both ends (`ostrava/scripts/lib.py` `plans`).
- Merge near-duplicate slots 1–2 min apart (one drifting departure); a row needs ≥ 2 real departures per slot.
- Prefer the line's exact own pattern over an approximation caused by folded variants (`lib.exactify`).

## Separate lines, branches, short workings

- Short workings and branches are **separate Simutrans lines** (Also at can't change the route); their offsets interleave.
- Exception: a line whose vehicles alternate between branches is one line with the shared terminus in the schedule twice (Plzeň 4).
- Path variants (one direction, two paths, alternating) → one circuit line out on one path, back on the other (`lib.path_variants`).
- **Depot runs are never modelled** (except rail depot ends the owner asked for, e.g. Praha/Brno odstavné nádraží 15 min).
- Through-running is one line only if every vehicle runs through.

## Daily lines: forbidden for regional buses

- Owner, 20 Oct 2026: "I don't like 1440 lines - in game that is not found. 8 hrs should be the very maximal interval (still not
  preferred)… we can bend the reality a bit." Never every 1440 or 720 on bus sheets; max 480.
- Rail sheets used 1440 + Also at for sparse lines in the archived MD-CR v3; avoid it in new work.

## Coupling (rail)

- The fork can couple trains: the **joining** line's entry says "Couple with X, wait up to N min"; trains part at the first stop
  where their next stops differ. Only the joining line carries "Couple with". Coupling ignores pak constraints.
- Reference designs: R18 + R18 Luhačovice (`local-rail/build_r18.py`), S4 Ústí + 2nd unit to Kralupy (`build_s4.py`). The unit
  line must list the same stops as the line it rides with (next-stop rule) and coupling offsets must match.
- In the game, all-stops trains run faster than reality: give long all-stops runs intermediate timing points at stations with
  passing tracks.

## Terminal stop type

- The fork has a terminal stop type that lets one circuit line serve a long and a short line turning at the same station
  (cuts long main-station stays). Use only if the same vehicles really run both parts ([rail rules](rail-sheets.md)).
