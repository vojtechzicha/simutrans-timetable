# PID regional sheets: the line-by-line review brief

Written 1 Nov 2026. A designer has set every line of one oblast (`pid-regional/oblasti/<id>/lines.json`, its method check
`method-check-2026-11-01.md`). You review it **line by line, independently**: the owner asked to "comb line by line, look at my
usual notes (there seems to be lot of them usually) and make sure it is polished". The owner's usual notes are their
corrections in `kb/lessons.md` (repo `C:\Users\vojte\Developer\simutrans-timetable`). Your job is to find what the owner would
catch, before the owner sees it. Do not trust the designer's conclusions: check them against the data.

## Read first
- Repo: `kb/lessons.md` (all of it), `mirror/pipeline/bus-schedule-method.md` (v4, all of it), `kb/rules/bus-sheets.md`,
  `kb/rules/fork-schedule.md`.
- Working folder `D:\OneDrive\Documents\Personal\Transport Fun\Simutrans-Timetable\pipeline`: `pid-regional/DESIGN_BRIEF.md`
  (what the designer was asked), `odis-regional-hko/README.md` "How a line is set" (leg format).

## For every line of the oblast
Data: `pid-regional/oblasti/<id>/data/derived/reading/<L>.txt` (every trip of the day at the core points, the paths, the
0-minute chain test, and — when present — the buses the live map saw), `schedule.json` (what the builder made of the design:
per Simutrans line its legs, slots `real`, typed `set`, window, `trips` with `dev`, `stat`, `knots`, `need`, `waits`),
`audit-step4.md`, `audit-branch.txt`, `audit-path.txt`, and the `_coverage` entry of schedule.json.

Check, at least:
1. **Pattern = reality.** Write down the line's real afternoon departures per direction at the terminal (or knot) and compare
   them with the slots. Exact minutes where the timetable is exact (owner: "I HOPE you are not adjusting but trying to fit the
   real timetable"). Every window slot has a real trip within 3 min; slots = real departures ±1 (Step 4).
2. **Interval sanity.** Divides 1440, ≤ 480, never 720/1440; folded evenly spaced slots; ≤ 8 slots; offsets from 01:00 with
   the loop −1 (the builder does it — verify one typed value per line by hand: (real − 61) mod every).
3. **Both ends same rate**; circuits balanced; no empty-return line just for frequency (only for a stop nobody else serves).
4. **Branches / variants** (owner on 292: "half of the services going to Chuchelná, half going to Strahovice - but you model
   as one line?"): every regular afternoon branch (≥ 3 trips each way 13:00–19:00) has its own Simutrans line or is explained;
   a leg read at a midpoint does not stand for another branch's trips (branch/path audits).
5. **The line's peak** (owner on Ostrava 23: model each line at its own afternoon peak; regular afternoon branches count even
   if not at 16:00 exactly).
6. **Coverage**: every stop of this okres served 13:00–19:00 is on a modelled line or has a reason. A line in `unmodelled`
   whose stops another line covers: name the line and check it really serves those stops in the afternoon (owner on 501:
   "the only line running to Dětmarovice, how can we not model that?").
7. **Sizing** follows the pattern (owner: "You should always size it from the pattern you are suggesting - for all lines");
   no silly waits (a bus waiting most of an interval at one end when the slots could turn it faster — shortest terminal wait).
8. **Interleaving / bunching**: lines sharing a terminus or trunk do not leave at the same minute where reality spaces them
   (owner: "if the real timetable interleaves, you should interleave"; "39 and 35 now is 10-minutes apart in the shared sections
   right?").
9. **Through-running / pairing** (0-minute chain test, Step 5b): where every trip of one line continues as another, is it
   modelled or at least named? (Owner on 301/352: "I am 100% sure 301/352 are continuations of 174 - why don't you know?")
10. **Owner checks**: every approximation is on the To check list with the slower option and its bus cost; nothing doubtful
    was silently decided ("Never silently pick the busier pattern").
11. **Wording** on notes: plain, no abbreviations, full stop names; says what the line is and why it is modelled so.
12. **Settled since the pilot (do not re-open):** every place is served, also outside the Středočeský kraj (owner, 2 Nov 2026:
    "Yes, serve every place"); a real 0-minute turn keeps its real slots, with `"lay": 0` on the departing leg (the fork's
    automatic "Leave up to" lets the bus leave); owner_checks only for real choices (the pilot's 13 checks were cut to 0:
    outstation rate, no empty returns, exact beats approximate, only-service lines, Step 5b and pooling are all decided by
    the rules). A check that re-asks a rule is a FIX. Two kinds of check stay: real approximations or pooling with their
    options, and the ONE sheet-wide roadside-stop check (DESIGN_BRIEF: roadside stops of a covered village as coverage
    exceptions, collected into one check with the bus cost of serving them all).

## Output
Write `pid-regional/oblasti/<id>/review-2026-11-01.md`: a table, one row per line of the oblast (including unmodelled ones):
line · verdict (PASS / FIX / ASK OWNER) · what is wrong, with the real minutes as evidence · the concrete fix (the lines.json
change). Then a short list of cross-line problems (bunching, coverage, pairing). Do not edit lines.json yourself.
Final message: the counts (PASS / FIX / ASK), and every FIX and ASK row in one line each.
