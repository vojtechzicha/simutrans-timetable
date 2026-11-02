# PID regional sheets: the design brief for one oblast

Written 1 Nov 2026 for the sessions (and subagents) that design one oblast each. The owner asked: "Do the full PID. Divide it
per oblast (like Mladoboleslavsko), all PID lines should be in. Then use Fable and/or subagents to comb line by line, look at
my usual notes (there seems to be lot of them usually) and make sure it is polished."

The owner builds every value by hand in their own Simutrans fork, so a wrong minute or a missing stop costs them real work.
Precision matters more than prose. Script output is a draft; your judgement line by line is the product.

## Read first (all of them, in full)

Repo `C:\Users\vojte\Developer\simutrans-timetable` (the knowledge base):
1. `CLAUDE.md`, `kb/README.md`, `kb/workflow.md`.
2. `mirror/pipeline/bus-schedule-method.md` — **the method, v4. Every line here is a regional line (or a small-town line:
   MHD Benešov, Kolín, Příbram, Říčany, Vlašim, Beroun), so this method applies in full.** Its "Checks before publishing"
   must pass.
3. `kb/rules/bus-sheets.md`, `kb/rules/fork-schedule.md`.
4. `kb/lessons.md` — the owner's corrections, in their words. These are "the usual notes": the owner will check your lines
   against exactly these, so check them first yourself.

Working folder `D:\OneDrive\Documents\Personal\Transport Fun\Simutrans-Timetable\pipeline` (the pipelines; run here):
5. `odis-regional-hko/README.md`, section "How a line is set (`config.lines[L]`)" — the leg format you write.
6. Worked examples: `odis-regional-opavsko/method-check-2026-10-25.md` (a method check, step by step) and the `lines` of
   `odis-regional-hko/config.json` (501/504, 543, 451, 553 show knots, variants on long intervals, empty returns, `via`/`notvia`).
7. `odis-regional-hko/scripts/05_schedule.py` docstring (what the builder does with your legs).

## Your oblast

- Folder: `pid-regional/oblasti/<id>/`. **You edit only `lines.json` there, and you write `method-check-2026-11-01.md` there.**
  Nothing else: not the scripts, not other oblasts, not the Prague bus sheet, not the KB. If a script is wrong, describe the
  bug in your method check and your final message; do not patch it.
- Input per line: `data/derived/reading/<L>.txt` (every trip of Mon 2 Nov 2026 with its time at each core point, the paths,
  the 0-minute chain test at its ends), `data/derived/line_class.json` (label, name, licences, operators, why it is on this
  sheet), `../../data/derived/stop_okres.json` (each stop's okres: licence prefix 200..310, null for Prague and other kraje).
- Line keys are the PID number (`"560"`), or the licence for town lines named "MHD n" (`"205001"` = MHD Benešov 1; the label
  is in line_class.json).
- Run: `python -X utf8 pid-regional/scripts/run_oblast.py <id>` from the pipeline folder (`--draft` also prints a first guess
  for the lines not yet in lines.json; it is a guess, never a result). It writes `data/derived/schedule.json`, prints each
  Simutrans line (every, slots, exact/within 3/real count, off-pattern, empty slots, running time, need) and the coverage
  check, and writes three audits: `audit-step4.md`, `audit-branch.txt`, `audit-path.txt`.

## What lines.json holds

```json
{
 "lines": {"560": {"core": [...], "note": "the reading in words", "anchor": "16:00 (optional)",
                   "sim": [{"name": "560", "every": 60, "legs": [{"fr": "...", "to": "...", "at": [0]}, {"fr": "...", "to": "...", "at": [30]}], "why": "..."}]}},
 "unmodelled": {"563": "why it is not modelled (Step 8: every stop it serves 13-19 is on these lines: ...)"},
 "terminus_alias": {"stop where buses arrive": "stop they leave from"}, "terminus_alias_why": "",
 "coverage_exceptions": {"stop": "why no modelled line serves it"},
 "owner_checks": [["560", "what is doubtful (with the real departures)", "the other option and its bus cost"]],
 "notes": "anything the sheet's intro should say about this oblast"
}
```
Stop names in legs are exactly as in the reading files (they are the ones the builder matches). `at` values are minutes for
intervals dividing 60, else "H:MM" clock times (taken mod every). Typed values and the loop −1 are computed by the builder.

## Every line of the oblast must end in exactly one of
1. `lines` — designed by the method; or
2. `unmodelled` — with a concrete reason (Step 8: a sparse or shift line whose afternoon stops are all on modelled lines —
   name those lines; a line with no afternoon trips and no stop of its own). Night lines, replacement buses (X…), PID Haló,
   lines with no trips on the day and the Prague bus sheet's companions are filled in automatically; leave them.

## The method, the points that matter most here
- Read the whole day (5–23) at core points; model the line's afternoon anchor (its busiest 2 h in 13:00–18:00, or 16:00).
- Step 4 for every timed leg: slots in the model window = real departures ±1, and ≥ 80 % of slots with a real departure
  within 3 min; then most exact over the day, then simplest. If nothing passes: the simplest even pattern at the real rate,
  approximate, **on owner_checks** with the slower option. Never ship an `at: "auto"` row you have not checked.
- Intervals divide 1440, **max 480, never 720/1440**; ≤ 8 slots per entry; both ends at the same rate; fold evenly spaced
  slots (the builder writes them folded).
- Time the **terminals**, worked back from knots (`knot` + `knot_at`); knots get no timetable.
- **Variants and branches:** each destination its own Simutrans line on a longer interval (Ex4), offset so they do not
  coincide; a leg read at a midpoint must not mix another branch's trips (`notvia`); after any change the branch and path
  audits must be clean or explained.
- **Step 5b:** at shared terminals pair surpluses across lines before giving each its own pattern. Evidence: the reading's
  0-minute chain test (a line whose every trip continues as another is a through line or a circuit). The live map is polled
  on Mon 2 Nov afternoon; its bus chains will be added to the reading files later — if you need them for a decision, say so
  in owner_checks instead of guessing.
- **Outstation lines** (buses sleep at the far end): time both ways at the inbound rate, list the extra outbound peak
  departures as off the pattern. **No empty-return lines just for frequency** — only for a stop nobody else serves.
- **Step 8:** fold sparse lines into the line they belong to; a long-interval line only where it is a place's only service.
  Long-distance lines with a few trips a day (to Karlovy Vary, Liberec, Chomutov, Tábor…) are bent onto a repeating slot
  of at most 480 at their afternoon trips.
- **Step 9 coverage:** every stop of **your okres** (stop_okres.json = your prefix) **and every stop outside the Středočeský
  kraj** (stop_okres null, not "Praha, ") served 13:00–19:00 must be on a modelled Simutrans line of this sheet or listed in
  coverage_exceptions with a reason — `run_oblast.py` prints both as "UNCOVERED here". Stops in Prague count as covered by
  the Prague bus sheet. Stops of another Středočeský okres are covered by that oblast's sheet and checked across all sheets
  at the end (`--final`); list in your method check any of them that only your lines serve. Run without `--final` while
  designing (the other oblasts are being designed at the same time).
- **Step 10:** needs come from the pattern (the builder). No vehicles now: buses are assigned later from the live map.
- **Shortest terminal wait by default**; a cross-line circuit only where the evidence shows the buses doing it, and only
  where it saves ≥ 1 bus. Pooling is an owner option, never silent.
- One Simutrans line per real line; offer pooling as an option. Keep the owner's typing small: timetables only at termini.
- **Say which route a row runs** (owner, 1 Nov 2026, Prague 329: "Is it the line going via Květnice or not." → "please do put
  the note there, so I know"): where a Simutrans line's trips take a variant path (via a village, a detour), name it in the
  line's `why` with the running time used. Every sim line gets a `why`.

## Learned on the pilot (Rakovnicko, 1 Nov 2026)
- **Stop names:** legs must use the full names. The reading files print them in full in "core (full names)" and in the path
  lines; the trip rows shorten them. When unsure, take the name from `data/derived/trips.json`.
- **Each line's own stops:** the reading's "stops only this line serves 13:00-19:00 (okres)" line is the coverage question
  for that line: if it is in `unmodelled`, those stops lose all service.
- **`core_to` vs `knot`:** `core_to` (a point before `to`) catches trips that **end** short of the terminal; trips that
  **start** short of `fr` need a `knot` + `knot_at` (they are read at the knot). Use both on a line whose trips do both.
- **Running times:** check `rt` on every leg in the builder output. The median can mix paths (a `stops_via` leg read at a
  knot) or the whole day (knot running time); set `rt` / `knot_rt` by hand to the slot trip's own time when it differs, and say so.
- **A slot must stand for a real trip.** `run_oblast.py` prints "SLOT WITHOUT A REAL TRIP" (fix it) and "no slot in the
  window" (a sparse line: name the real trip each slot stands for in the line's `why`). Step 4 says nothing about such legs.
- **0-minute real turns** (the timetable sends the arriving bus straight back): keep the real slots and the real running
  times, and give the departing leg `"lay": 0` so the bus count takes the real 0-minute turn (tested on 573: 2 buses → 1).
  This assumes the fork's "Leave up to" (automatic, half the gap; kb/rules/fork-schedule.md) lets a bus that arrives on the
  real minute leave although the loop rule typed the departure 1 min early — an engine question to confirm when an engine
  session is live; the sheet notes it once. Say "0-minute turn as in the timetable" in the `why`. Not an owner check.
- **Every place is served, inside or outside the kraj** (owner, 2 Nov 2026, asked about 571 Rakovník – Slatina – Chříč in
  Plzeňský kraj: "Yes, serve every place"; and 20 Oct: "501 is the only line running to Dětmarovice, how can we not model
  that?"): a stop that no other modelled line serves gets a Simutrans line, at most every 480, the cheapest pattern that
  holds a real trip — also where the stop lies in another kraj (a PID line's far end in Plzeňský, Ústecký, Liberecký…). A roadside
  stop (rozcestí / odbočka / křižovatka) of a village whose other stops a modelled line serves, within about 1 km of one of
  them, may instead be a coverage exception naming that stop and the distance; collect such stops in ONE owner check for the
  sheet with the bus cost of serving them all, not one check per line.
- **Outstation lines with a Prague end** (buses sleep in the district town; the morning peaks into Prague, the afternoon out):
  the rule is unchanged. Model the line's own afternoon anchor window; time both ends at the rate of the trips **towards
  Prague** in that window (the inbound rate); the extra departures from Prague (buses going home) are off the pattern and
  listed on the card. No empty-return line for them.
- **Different lines leaving a hub at the same minute** is fine when the real timetable does it; interleave only where the real
  timetable interleaves (fix model artefacts, never real bunching).
- **No abbreviations** in `note`, `why` or owner checks (owner: "Don't use cryptic"): full stop names as in the reading
  ("autobusové stanoviště", not AS; "železniční zastávka", not žz), no NS / KV / rozc. / nám.
- **Name the through-running you see** (Step 5b): a 0–5 min chain at a terminal that covers most trips of a pair of lines
  goes into `notes` even when you keep the lines separate; the live map of 2 Nov will confirm it.
- **Card text is short.** `note`: 2–4 plain sentences — the line's route, its pattern in real minutes, what is off the
  pattern and why the Simutrans lines are split as they are. Each sim line's `why`: one or two sentences (route, running
  time, the real trip a sparse slot stands for). The step-by-step reasoning goes to the method check, not the card.
- **owner_checks are for real choices:** an approximation with its slower option, a pooling option, a line kept or dropped
  for a stop. Do not ask what the method already decides (every 480 is allowed; a line modelled at its anchor is the rule).

## The method check file (`method-check-2026-11-01.md`)
Per line, short: core points; what the whole day shows (the pattern in real minutes); the Simutrans lines chosen and why;
Step 4 result per leg (window slots vs real departures, exact/within 3); off-pattern trips; any owner check. Then a summary
table (line, Simutrans lines, every, buses) and a list of open questions. A reviewer will read this against the reading files
and the lessons, line by line, so say what you looked at.

## Done means
- every line in `lines` or `unmodelled`; `run_oblast.py` runs clean;
- every timed leg passes Step 4, or is an approximation on owner_checks with its slower option;
- `audit-branch.txt` and `audit-path.txt` have no unexplained flag;
- no uncovered stop of your okres without a reason;
- the method check is written. Final message: the summary table, totals (Simutrans lines, buses), the owner checks, and
  anything you could not decide.
