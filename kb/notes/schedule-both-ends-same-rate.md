---
name: schedule-both-ends-same-rate
description: Both ends of a Simutrans line must send the same number of trams an hour; check every schedule fit for this before publishing
metadata:
  node_type: memory
  type: feedback
  originSessionId: 5fc4f1eb-5ab6-4d45-b8f2-cd49a4f98331
  modified: 2026-10-18T17:58:04.153Z
---

User caught it on 18 Oct 2026 (Ostrava): line 4 Hranečník got 3 departures an hour while 4 arrived ("how can it have less departures than arrivals?"). Line 5 got every 60 with 3 uneven slots one way and 4 the other ("that would not work").

Cause: runfit fits each terminus on its own, so one end picks the pre-peak pattern and the other the peak pattern.

**Why:** in Simutrans, unequal rates at the two ends of a line can't run.
**How to apply:** after fitting, pair each A→B entry with its B→A entry. If the rates (slots × 60 / interval) differ, try every candidate rate (both fits, plus the real 16:00 hour) on both ends and keep the rate with the longest combined exact runs. Ostrava's `lib.plans` does this. Also flag uneven slot gaps and check they are real (4A's 10/20 is real because 4B fills the gaps). Applies to every city sheet. Related: [[simutrans-fork-schedule-spec]], [[shortest-terminal-wait-rule]]

**Refined 20 Oct 2026 (Ostrava bus/trolleybus, shared `ostrava/scripts/lib.py` plans):**
- Accept exact patterns with intervals dividing 1440 (bus 40 runs every 40). A run must overlap 15:30–17:30 by ≥ 30 min with ≥ 4 departures (3 if hourly, one slot).
- The same treatment applies when the rates agree but a run misses the peak. Never merge away a direction whose opposite direction is scheduled.
- Fallback: even approximate pattern, marked "approximate, up to N min off", with the real band minutes.
- The user wants doubtful rows marked for their own evaluation: approximate rows with more slots than real departures are flagged on the card and in an "Approximate schedules to check" list, with the slower alternative. Never silently pick the busier pattern.
- Real-minute subtitles must be worked out from each typed value (+1 at loops), not listed in fit order; it mislabelled patterns that wrap past :00.
- **Afternoon branches (20 Oct, owner on bus 23 Záblatí):** model regular afternoon branches (>= 3 trips each way 13:00–19:00), not only those busy at 16:00. Fit sparse ones over 13:00–19:00 with intervals up to 120. Pick both ends' offsets together for the shortest round, using the longest running time, or a mismatch makes a bus wait a whole interval.
- **Branches sharing a terminus must interleave (20 Oct, owner on bus 23):** fitting each branch alone bunched 23A/23B 7 min apart at Hranečník, while the real timetable alternates them every 40. After fitting, check the combined departures at each shared terminus. Where they bunch, use the alternation the timetable shows: a common interval with offsets apart (21/81, 23A/23B). On 20 Oct, bus 34, 44, 56 and 68 still bunch.
- **Match ends across aliases; merge near-duplicate slots** (owner, 20 Oct 2026, Ostrava 31 / 54): fit with aliased terminus names so a loop end with two stop names (31 garáže / jižní brána) is still rate-matched. Slots 1–2 min apart are one drifting departure (54 :x3 → :x2): never output 'every 60' with 7 slots for an every-10 line. After any schedule change, scan for rows whose slots-per-hour differ from the other end. Also: a row needs at least 2 real departures per slot (62: 2 trips must not become 2 slots an hour).
- **Prefer the exact own pattern** (20 Oct, via a4's hand check): folded variant minutes or a wind-down inside the model window must not turn an exactly regular pair into an approximation (Ostrava 49 sad BN every 20, 76 hourly; `lib.exactify`). Hand-check approximate rows against the main pair alone.
- **Whole-day repeating interval** (owner via a4, 20 Oct, save game Ex4): REGIONAL lines only — read trips at core points over 5–23, find the repeating interval, variants on longer offset intervals. Not for local city lines (owner, 20 Oct: local lines = afternoon peak + unique stops). See [[regional-vs-local-rules]].
