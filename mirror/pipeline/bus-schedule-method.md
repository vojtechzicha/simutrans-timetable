# Bus schedule method: regional lines and small towns

**Scope: regional lines and small-town networks** (Havířov, Karviná, Orlová and towns like them). Big-city networks (Ostrava, Prague, Olomouc) don't use this method: their local lines are modelled at their afternoon peak, with their unique stops. Depot runs are never modelled anywhere. (Owner, 20 Oct 2026, to the Ostrava session: "these rules are for the regional lines, not for local lines"; "for local lines we model the afternoon peak and unique stops"; "depot runs are never modelled"; and to the Havířov/Karviná/Orlová session: "Ostrava/Prague/Olomouc - these big cities don't use the method. Only smaller ones like Orlova/Karvina do use it".) If you can't tell whether a town counts as small, ask the owner. Put any exception on a big-city sheet to the owner with the supporting facts, and don't decide it yourself (Ostrava 57 "garáže" was approved this way).

Version 3 (20 Oct 2026): no daily lines, 480 at most. Version 2 was sharpened after a test run by a smaller model on the Ostrava sheet's ODIS lines (`ostrava-bus/method-check-odis-2026-10-20.md`).

Version 4 (25 Oct 2026): the rules below from the hand check of the Hlučínsko lines 281, 282, 290, 292 (worked example:
`odis-regional-opavsko/method-check-2026-10-25.md`). They override anything older in this document.

## Rules added on 25 Oct 2026 (v4)

- **A scripted fit is never shipped unchecked.** Every row the builder fitted (`at: 'auto'`) gets the Step 4 test per
  direction before publishing, written into a dated `method-check-<date>.md` in the sheet's folder (owner: "that's the point
  of you doing it, so you'll not produce incorrect results"). Tools: `audit/step4.py` (one direction: real departures, a
  candidate's window slots, fill, exact hits, off-pattern trips) and `audit/step4_regional.py` (every leg of the regional
  sheets, with the passing-candidate search). A leg fails Step 4 when its window slots differ from the real departures by
  more than 1, or fewer than 80 % of its window slots have a real departure within 3 min. If a passing pattern exists, use it;
  if none does, the simplest even pattern at the real rate, approximate and on the To check list (rule 4 of Step 4).
- **Outstation lines.** Where the buses sleep at the far ends (garages or villages: the first morning trips start there),
  the afternoon sends more buses out of the city than come back, and Step 5b cannot pair the surplus across lines. Time the
  line both ways at its inbound rate and list the extra outbound departures (buses going home) as off the pattern. Its
  outbound row then has fewer slots than real departures; say why on the card.
- **No empty-return lines just for frequency** (owner: "Unless those empty runs add something really needed and specific,
  don't add them just for frequency"). In the game a line repeats all day, so an empty return shuttles back every period.
  Add one only for something specific, such as a stop that has no other service (387, 543B, 553 Orlová kept their reasons).
- **Which departures fall off the pattern:** choose by the plates (the buses that go home or on to another line) and by the
  waits the choice makes (290: leaving 16:19 off, not 14:59, needs 4 buses instead of 5).
- **An exact multi-slot row on a long interval beats a simpler interval that fails Step 4** (290: every 120 with four slots
  each way, exact, 4 buses, against every 40 with 3 buses and two departures missed; owner: "290 uses more buses").
- **Mixed origins: read at the knot.** When a line's trips towards the city start at different far ends (292: Píšť,
  Chuchelná, Strahovice), time the way back at the knot they all pass (`knot` + `knot_at`), not at one terminal.
- **Model hour set by hand** (`anchor`) when the line's busiest two hours are shuttles whose stops are on the line anyway
  (282's Hlučín – Závada shuttles): model the hour where the line's own pattern runs.
- **Typed values and their real times:** work the real time out from each typed value (+61 at loops, mod every); never pair
  two separately sorted lists.
- **Buses already in the game:** rebuild with `keep_roster` (the sheet's published roster in `data/published/`), so each
  published bus stays on its Simutrans line wherever it is still seen on that line's trips; give the owner the in-game change
  list (old → new per entry, buses in / out).
- **Owner choices** go on the sheet's owner checks with the cheaper option and its bus cost; once the owner decides, remove
  the check and record the decision on the card and in the README.

This is how to turn a real bus timetable (CIS JŘ JDF trips) into Simutrans lines for the owner's fork. Follow the steps in order, and do the checks at the end before publishing. The method was worked out with the owner on 20 Oct 2026 on the Havířov/Karviná/Orlová sheet (`havirov-karvina-orlova/`, reference code and examples). Regional lines are harder than town lines: they pass several towns, have more variants and share points with other lines. They need every step.

The owner's own words:
- "501 is the only line running to Dětmarovice, how can we not model that?" Every place must be served.
- "Is the lines the best schedule that fits my intent (not necessarily the scripts)?" Check every line by hand. Script output is a draft.
- "Look at how I did in the save game Ex4 … I defined it in core points, created a repeating interval and it suddenly made sense." Use core points and a repeating interval.
- "Time the Koukolná branch from the terminal, just calculate the departure so it is in correct time in the knot at nádraží (and in similar way at other stops)." Buses are timed at terminals, worked back from the knot.

## What the fork's timetable can do (fixed facts)

- Each schedule entry can carry: **Departure every** (interval in minutes, 0 = no timetable), **Offset**, up to 7 **Also at** values, and **Leave up to**.
- Values are whole minutes. The interval must divide 1440, or the pattern restarts at midnight. Allowed: 10, 12, 15, 20, 30, 36, 40, 45, 48, 60, 72, 80, 90, 96, 120, 144, 160, 180, 240, 288, 360, 480.
- **480 (8 hours) is the longest interval, and not preferred** (owner, 20 Oct 2026: "Now I don't like 1440 lines - in game that is not found. 8 hrs should be the very maximal interval (still not preferred). If the only way to model 1440 is 1440 reconsider - we can bend the reality a bit."). Never use 720 or 1440. A line that runs once a day is never seen in the game. Prefer divisors of 60, then the others. Use an odd one (72, 45 …) only where it fits clearly better: 383's 75-min spacing fits every 72 (worst 3 / 9 min) much better than every 80 (5 / 20).
- **Offsets count from 01:00:** typed value = (real minute − 60) mod interval. At a loop terminus, subtract 1 more: (real − 61) mod interval. Example: a departure at 9:06 on every 480 from a loop → (546 − 61) mod 480 = 5.
- One Simutrans line follows one route. Branches and variants need their own Simutrans line, or one circuit line that visits them in turn.
- The owner types every value by hand. Keep the number of timed entries small.

## Which hour the pattern stands for

The Simutrans pattern repeats all day, but it stands for the line's **afternoon peak**: its busiest 2 hours in 13:00–18:00, or 16:00 if that is within one departure of 15:00–17:00 (`lib.line_anchor`). Read the whole day to find the minutes, the phase and the variants. Where the afternoon differs from the rest of the day, the afternoon wins:
- 442 is hourly at midday and 5 an hour in the afternoon, so it is modelled at 5 an hour.
- When a slot changes line number during the afternoon (534's :25 becomes 535's from 16:25), take the line that runs it at the anchor.
- A line with no afternoon service is modelled at its daytime pattern (502 runs 8:01–14:34).

## Step 1: list every trip of the whole day

For each line, take all trips of the vehicle day, both directions, with the time at every stop. Read 5:00–23:00, not only the afternoon. A pattern that looks irregular in 15:00–17:00 is often regular over the day (514 runs :27 / :48 / :25 from 9:00 to 19:00).

## Step 2: choose the core points

Core points are:
- **termini**, where buses turn and wait;
- **knots**, where branches or variants split or join;
- **shared hubs** with other lines.

A town line has 2–4. A regional line may have 4–6: its terminal in each town and the junctions.

Special cases:
- **A loop end with two stop names** (arrives at one stop, leaves from the next: Havířov, Město, nemocnice / železniční stanice; Podlesí, Těšínská / autobusové nádraží): alias the two as one terminus (`config.terminus_alias`). The departure stop is where the timetable goes.
- **A stop the route passes twice** (383 passes rozcestí Bludovice out and back on its long path): choose a core point the route passes once. If there is none, use the first passing and say so on the card.

Examples:
- 501/504 Orlová: Lazy, Lutyně, autobusové nádraží, and Dětmarovice, železniční stanice (the knot, where the Elektrárna and Koukolná extensions split off).
- Ex4 in the save: Warszawa / Kraków, Bohumín, Břeclav, Wien / Budapest.

## Step 3: read each trip at the core points it passes

For every trip, write down its time at each core point it passes. Use the passing time, not where the trip starts or ends. A Koukolná → Lazy trip that leaves Koukolná at 18:09 counts as Dětmarovice, železniční stanice 18:18. Trip ends in the timetable are often artefacts: the same bus goes on as another line number, or a trip is split at a hub. Counting only trips that start and end at the core points misses most of them.

Trips that never touch the line's main core point (535's Horník ↔ Karviná shuttles) are a variant of their own. Handle them in Step 5 or Step 8: their own Simutrans line only if they serve stops no other line serves, otherwise list them.

## Step 4: find the repeating interval at the main knot

Group trips by the core points they pass (their variant: where they go beyond the knot). Take the main variant, the one with the most trips. At its knot, try every interval from the list above. For each interval, choose the minute(s) that the most real core-point times hit:
1. most times **exactly** on the minute;
2. then most within ±1 min;
3. then the smallest worst deviation.

Never choose by smallest worst deviation first. That put 504 at :01 instead of its real :06.

**Choosing between intervals.** Exact hits alone always favour the shortest interval: every 15 catches more trips and leaves its slots empty. So:
1. **Number of slots:** count the real departures in the model window (the anchor's 2 hours, see "Which hour"). The candidate's slots in the same window must equal that number, ±1. 5 departures an hour means 5 slots an hour, as every 60 with 5 slots, or every 12 if they are evenly spaced. Try k = 1 … 8 slots per interval.
2. **Every slot needs a real departure** within ±3 min, in at least 80 % of the window's slots. Otherwise the pattern is too dense.
3. Among the candidates that pass 1 and 2: the most departures exactly on the minute over the whole day, then within ±1, then the simplest (fewest slots, then the longer interval), then the smallest worst deviation.
4. If nothing passes, keep the simplest even pattern at the real rate. Mark it approximate with its worst deviation and put it on the To check list with the slower option.

Write down the trips more than 3 min off the pattern. They go on the card as "off the pattern".

Example: Orlová trunk at Lazy, whole day: 8:06, 9:06, 10:06, 11:06, 12:00, 15:06, 16:06, 17:06, 18:06, 18:56. That is every 60 at :06. 12:00 and 18:56 are off the pattern.

## Step 5: split destination variants onto longer intervals (Ex4)

When a share of the departures goes somewhere else, give each destination its own Simutrans line on a longer interval. Offset the lines so they don't run together at the shared knot. Together they must give the real frequency.
- Ex4: Ex4/1 every 240; Ex4/2 and Ex4/3 every 480, at other offsets.
- Orlová, hourly trunk at Lazy :06:
  - 501, to Dětmarovice: odd hours, written as every 480 with three slots (11:06, 13:06, 15:06 …);
  - 501B, beyond to Koukolná: the fourth slot (9:06, 17:06), every 480;
  - 504, turning at Lutyně: even hours, every 240, alternating two paths.
- Check every slot of the combined pattern at the knot. No two lines may share a minute, and there must be no gap the real timetable doesn't have.

### Step 5b: pair lines at a shared terminal

Do this before giving any line its own pattern. At every terminal shared by several lines, count each line's arrivals and departures per hour in the model hour.
- If one line arrives more often than it leaves, and another leaves more often than it arrives by the same number, the extra buses change line number at that terminal.
- Model them as a circuit: out on one line's path, back on the other's.
- What is left of each line is balanced and stays a separate Simutrans line.

Examples:
- 401/406 Havířov: 406 Podlesí → Pašůvka goes on as 401 Pašůvka → Šumbark → Prostřední Suchá, then as 406 back to Podlesí. Each line is half of the ring.
- 442/441: 442 sends 5 an hour out to Podlesí and brings 3 back; 441 sends 1 and brings 3. So 442's :05 / :10 come back as 441's :32 / :47. That pair is one circuit; the rest of 442 and of 441 stay separate lines.
- 534/535: each line alone is unbalanced. Together they give every 30 both ways at Hranečník, so they become two balanced hourly lines.

The live feed confirms such a pairing: the same plate shows up on both line numbers.

## Step 6: time the terminals, worked back from the knots

This is where buses differ from trains. A train can be held at a junction. A bus waits only at its terminal.
- **Put the timetable on the entry where the bus leaves its terminal.**
- If the bus must pass a knot at time K, the terminal departure is **K − running time from the terminal to the knot**. Take the running time from the real trips' stop times.
- **The knot gets no timetable** (Departure every 0).
- Examples:
  - 501B must pass Dětmarovice, železniční stanice at :18. The running time Koukolná → station is 9 min, so Koukolná departs at :09 (10:09, 18:09; the real one is 18:09).
  - 406 must pass Prostřední Suchá, železniční stanice at :28 / :58. It turns at Pašůvka, 2 min before the station, so Pašůvka departs at :26 / :56.
- **Approximate lines:** compare each slot with the real trip it stands for, the nearest real departure at the terminal. The knot deviation is that slot's deviation, plus any difference in running time. Write it per slot. If it is worse than the row's own worst deviation, the line goes on the To check list (383).
- After working back, check every knot: compute the time the bus passes each knot in the model, and compare it with the real times there. Write both on the sheet. A regional line passing three knots must hit all three; if it can't, say which one is off and by how much.
- **Empty returns:** a leg with no real trip (the real bus goes on as another line) is untimed (Departure every 0). The bus waits at the next terminal, where the next real trip starts. Examples: 418 back from Bludovice; 417B back from Podlesí.
- **Loops:** a departure from a loop is set 1 min early (Step 0 formula). Write the real minute under every typed value.

## Step 7: both ends at the same rate, and balanced

First check the balance at each shared terminal across all its lines (Step 5b). Then check each Simutrans line. Two lines can each be unbalanced and balance together; pair them, don't force each one.

- Each end of a Simutrans line sends the same number of buses per hour (or per interval). Otherwise buses pile up at one end.
- A circuit on a long interval (240, 480) has to have the same number of departures on every leg in one period.
- A one-way leg needs a return, timed or empty, so the bus comes back.

## Step 8: fold sparse lines into a line they belong to

A line with one or two trips a day is often another line's slot by another path, or its return. Put it in that line as one of its legs, and list it as carried by that line.
- 503 (14:00 Lazy → Lutyně via Důl Lazy) is the trunk's even-hour slot by the other path. It became a leg of 504, a circuit every 240 that alternates the two paths.
- 520 (Staré Město → Fryštát) is how the 514 buses return. It is the last leg of 514's circuit.

Only where neither fits, **bend the sparse trips onto a repeating slot** of at most 480 min:
- Look for the interval the real trips already have. Shift lines repeat every 480: 515's trips are back from Důl Darkov 6:10 / 14:10 / 22:10. 420's two trips are 160 min apart, so it runs every 160.
- Otherwise use the longest interval that keeps one real trip exact: 402B Stonava every 480 at 12:23, with its repeats at 4:23 and 20:23, clear of the afternoon peak.
- A one-bus sequence of several trips becomes a circuit on the shortest period that holds it: 418 Podlesí + Šenov every 240.
- List the trips this leaves off the pattern.

**Only for stops nobody else serves.** If every stop of a sparse variant is already on another Simutrans line, list the variant with that line's name, and don't add a line or a bus. 440's Kartonážka trips are exactly every 480, but DPO 41 serves Kartonážka. Add a long-interval line only where it is a place's only service (Stonava, Důl Darkov, Lapačka).

## Step 9: every stop on a Simutrans line

Every stop the sheet's lines serve in 13:00–19:00 must be on some modelled Simutrans line, or be listed with the reason (e.g. "one trip, over stops 410 serves"). Check it sheet-wide (`roster.json` → `uncovered` must be empty). On each card, list the trips that are not on one of its Simutrans lines, and the Simutrans lines that cover their stops.

## Step 10: size from the pattern

A line's bus count follows one bus round its own slots, using the real running times.
- **At each terminal:** at least 3 min. Use the real turnaround where the timetable chains closer (Hranečník :03 → :05 is 2 min), but never less than 1 min.
- **Before an empty return** (untimed leg): 0 min. The bus leaves on arrival, and the timed terminal after it absorbs the wait. The number of first-entry slots in one round is the bus count (`lib.override_need`, `pattern_need`). Never size from the raw timetable. Real buses swap lines at terminals, so per-line totals are higher than the operator's. Say so per town or region, and offer pooling as an option, never as the default.

## Step 11: review by hand, then list what is doubtful

For every line, put its whole-day core-point times next to the Simutrans values, and ask:
- Do the main variant's trips land on the slots?
- Are variant minutes folded into a main row and spoiling an exact pattern? (417 lost its exact hourly pattern this way.)
- Did a narrow window force a long interval on an hourly line? (409 and 411 got every 120 this way.)
- Is any timetable at a pass-through point instead of a terminal?

Each doubtful row goes on the "To check" list, with its off-pattern trips and a slower option where one fits.

## Common mistakes (all seen on 20 Oct 2026)

| Mistake | Effect | Fix |
|---|---|---|
| Fitting only the 15:30–17:30 band | 409 every 120 (30 min off); 514 3 buses instead of 2 | Read the whole day (Step 1) |
| Grouping trips by start/end stop pair | 501 lost Dětmarovice; 505's rotation and the 401/406 ring broke into wrong shuttles | Passing times at core points (Step 3) |
| Folding variant minutes into the main row | 417's exact hourly pattern became approximate | Variants get their own line or are listed (Steps 5, 11) |
| Slot chosen by smallest worst deviation | 504 at :01 instead of :06 | Exact minutes first (Step 4) |
| Timetable at a knot the bus passes through | 501B timed at the station, waited there | Time the terminal, work back (Step 6) |
| A daily timetable (every 1440) | Never seen in the game | At most 480: bend the trips onto a repeating slot (Step 8) |
| Unbalanced circuit on a long interval | Buses pile up at one end | Same count on every leg (Step 7) |
| Treating a 1–2-trip line as its own line | Extra bus, no pattern | Fold it into the line it belongs to (Step 8) |
| Checking balance line by line at a shared terminal | 442/441 and 534/535 look broken | Pair surpluses and deficits across lines (Step 5b) |
| Choosing the interval by exact hits alone | Every 15 always wins, with empty slots | Slots must match real departures (Step 4) |
| A line for a variant whose stops another line serves | Extra bus | List it with that line (Step 8) |

## Checks before publishing

1. Every line was read over the whole day at its core points, and the sheet says which core points.
2. The model hour is the line's afternoon anchor; the whole day was used only for minutes, phase and variants.
3. Each Simutrans line: interval divides 1440 and is at most 480 (no daily lines); offsets use (real − 60, − 1 at loops) mod interval; real times are written under the typed values.
4. Timetables only at terminals. Knot times are computed and compared with the real ones.
5. Shared terminals were balanced across lines first (Step 5b); then each Simutrans line: both ends at the same rate, long-interval circuits balanced.
6. Combined variants at a shared knot don't coincide and give the real frequency.
7. `uncovered` is empty, or every exception has a reason.
8. Needs follow the pattern. Pooling options are named, not applied.
9. Off-pattern trips are listed per row, and doubtful rows are on the To check list.
10. The README of the pipeline records every hand-set line and why.
