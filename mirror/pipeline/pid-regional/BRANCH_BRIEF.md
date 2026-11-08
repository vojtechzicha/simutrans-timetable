# PID regional: the branch re-check (3 Nov 2026)

Written 3 Nov 2026 for the subagents that re-check the twelve oblast sheets (v1, published 2 Nov), two oblasts each, and for
the reviewers who verify them. Read `DESIGN_BRIEF.md` (same folder) first: everything there still holds.

## Why
The owner, 3 Nov 2026: "381 you haven't done the Zásmuky branch. That is not off the pattern, looking at all our rules in the
timeframe, I clearly see 381 runs Zásmuky/Čáslav switching. This is weird. Verify specifically and then … you may have to
correct everywhere."

381 Praha, Háje – Zásmuky – Kutná Hora – Čáslav was modelled as one hourly line (Háje :00, Čáslav :48). Its Háje :30 trips to
Zásmuky, náměstí (14:30, 15:30, 16:30, 17:30) were filed as "the Zásmuky garage's buses going home" and listed, because only
one trip *starts* at Zásmuky towards Prague in the afternoon (16:21). But the Kutná Hora, hlavní nádraží → Háje 13:40 and 14:40
trips pass Zásmuky at 14:21 and 15:21. Read at Zásmuky, náměstí (method Step 3: the time a trip passes a core point, not where it
starts or ends), the branch runs 4 out and 3 back 13:00–19:00, every hour at :39 / :21. The afternoon-branch rule (20/30 Oct,
≥ 3 trips each way 13:00–19:00 → its own Simutrans line) applies. On the 2 Nov live map the buses switch between the two ends at
Háje (1683 and 9373 came in from Čáslav and went out at 16:30 / 17:30 to Zásmuky; 9372 ran Háje 14:30 → Zásmuky and back at
16:21). The designer and the line-by-line reviewer both missed it: they grouped trips by start and end, the method's own listed
failure ("Grouping trips by start/end stop pair … 501 lost Dětmarovice").

**Fixed (the worked example):** `oblasti/kutnohorsko/lines.json` → 381 now has `381` (unchanged) and `381 Zásmuky` every 60:
Háje :30 → Zásmuky, náměstí (`notvia` Bečváry, so the Čáslav trips do not count for it), Zásmuky, náměstí :21 → Háje (`notvia`
Čáslav, Kalabousek, so the Kutná Hora trips count and the Čáslav ones do not), `lay` 0 at Háje as on 381; 3 buses; both legs
exact in the window; note and why rewritten. The rule in short:

- **Read at the stop where the variant leaves the trunk.** Count every trip that passes it, wherever the trip starts or ends.
- **≥ 3 trips each way 13:00–19:00 there, at a repeating minute → its own Simutrans line** (Step 4 must pass), or a written reason.
- **The outstation rule ("buses going home", "the garage", "they sleep there") applies only to what is left after that
  reading:** the return trips really are not there, even counting trips that start further out and pass the point.

## The new audit
`pipeline/audit/passing_check.py`, now run by `run_oblast.py` as `data/derived/audit-passing.txt`. For each modelled PID
line it reads every real trip 13:00–19:00 at every stop it passes and marks the stops where no modelled slot of the line passes
within 3 min in the same direction (a trip that meets a slot somewhere on a leg counts as on the pattern for the whole leg).
- **EACH WAY** = at one stop, ≥ 3 such trips each way. The work queue: every one gets a verdict.
- **ONE WAY** = ≥ 3 one way, < 3 the other. Check the card's reason (going home / to another line / irregular).
- The flagged stop is the one with the most such trips; the trips listed are all those off the pattern there (→ / ← = the two
  directions, · = no direction found).
- It flags more than the 381 case: trips 4–10 min off an approximate row, irregular extras, Prague-end peak extras, sparse trips to
  several ends. Those are fine once the card says so. It does not know about other numbers: a trip carried by another line's
  ring (`lines` on a leg) counts as covered.
- The state before this re-check (with 381 already fixed) is in `audit-passing-2026-11-03-before.txt`.

## Per EACH WAY flag: one verdict
- **A — missed branch / short working / path variant** that runs regularly (≥ 3 each way 13:00–19:00 read at the stop where it
  leaves the trunk, at a repeating minute): give it its own Simutrans line like 381 Zásmuky. Step 4 per leg (window slots = real
  ±1, ≥ 80 % within 3 min). Use `notvia` / `via` so each leg counts only its own trips (the builder counts every trip that passes
  `fr` and `core_to`, wherever it starts or ends). Size from the pattern; `lay` 0 only for a real 0-minute turn or where the
  line's own buses turn at that terminal on the minute (say which). A path variant on the same ends (via a village): one
  circuit line out by one road and back by the other where the paths alternate (kb/rules/fork-schedule.md, Prague 329), and
  the `why` names the road (owner, 1 Nov 2026: "Is it the line going via Květnice or not.").
- **B — approximate row:** the trips are the line's own pattern 4–10 min off its slots, already stated on the card or on
  owner_checks. No change unless a branch hides in them.
- **C — irregular:** different minutes or different ends, no repeating pattern of ≥ 3 each way. Listed on the card; check the card
  names them.
- **D — true outstation:** read at the stop, the other direction really has far fewer trips (count trips that start further out
  and pass it). Keep; the card's reason must be right.
  - *Added 3 Nov evening, after 402:* write a D as counts at the stop (out N, back M off the slot) **and the plates**
    (`audit-plates.txt`: the buses end their day there or run on). A sentence about where trips start ("Zruč starts 4:24,
    6:29 only") is not a reason, even when the verdict happens to be right. Buses that come back empty are peak extras, not
    buses going home: the card says so.
- **E — other** (carried by another number, a scan artefact, rail replacement…): say what.

Then the ONE WAY flags: check each card's claim the same way, and look hardest at those with 2 each way. A third trip 4–6 min off
can still make a regular branch. Also grep your two oblasts' `lines.json` for "going home", "garage", "outflow", "outstation",
"sleep" and check each claim by the passing reading.

## Rules that still hold
- No empty-return lines just for frequency. Exact beats approximate. Intervals divide 1440, ≤ 480. Typed values are the builder's.
- owner_checks only for real choices (an approximation with its slower option; a line kept or dropped for a stop). Never re-ask what a
  rule decides. A pooling option is written on the card (the buses seen doing it, the buses saved), never on owner_checks.
- One Simutrans line per branch; pooling between them is an option on the card, never applied.
- Card text: short, full stop names, no abbreviations (AS, žst, rozc., nám.), each sim line has a `why` with route and running
  time. Update the line's `note` where the pattern description changes (it is what the owner reads).
- A line you do not need to change: leave it alone.

## Scope
- Edit only `oblasti/<id>/lines.json` of your oblasts, and write `oblasti/<id>/branch-check-2026-11-03.md`.
- Do not touch the scripts, `config.json` files, other oblasts, vehicles / roster, renders, the KB, git, or the Prague sheet.
  The live-map poller is running until 20:15 (python): never kill python processes.
- Run from the pipeline folder: `python -X utf8 pid-regional/scripts/run_oblast.py <id>` (no `--final`). After your changes its
  Step 4, branch, path and passing audits must be clean or explained. For one line's trips: `python -X utf8 audit/passing_check.py
  . <line>` and `data/derived/reading/<line>.txt`, `data/derived/trips.json`.
- Vehicles come later from the live map (the coordinator reruns the cross-oblast steps). Do not size by the save game.

## branch-check-2026-11-03.md
Per flagged line, short: the real trips at the flagged stop both ways (minutes), the verdict letter, the change (Simutrans line
added or changed: every, slots, buses), the Step 4 result of a new leg. Then a table: line | verdict | change | buses before →
after, and the oblast's bus total before → after. Your final message: that table per oblast, and anything you could not decide.

## For the reviewers (Fable)
You did not design this. For each of your oblasts, independently:
1. Diff `oblasti/<id>/lines.json` against v1 in the repo (`C:\Users\vojte\Developer\simutrans-timetable\mirror\pipeline\pid-regional\oblasti\<id>\lines.json`;
   Kutnohorsko's 381 change is the coordinator's).
2. For every EACH WAY flag in `audit-passing-2026-11-03-before.txt` and every ONE WAY flag with 2 each way, re-derive the
   verdict from `trips.json` yourself, then compare with the designer's. Do the same for every changed line, and for every card
   in your oblasts that claims buses go home / to a garage.
3. Check every new or changed Simutrans line: slots real (Step 4), `notvia` / `via` really separate the legs (look at the leg's
   trips in `schedule.json`), running times, `lay`, buses, the card text, nothing else on the line broken.
4. Fix what is wrong directly in `lines.json`, rerun `run_oblast.py <id>`, and write `oblasti/<id>/branch-review-2026-11-03.md`:
   per line PASS / FIX with what you changed. Final message: the FIX rows and the bus totals.
