---
name: shortest-terminal-wait-rule
description: "Default to the shortest wait at a terminus — don't model interworking (line swaps) at the peak if the timetable lets each line turn faster on its own"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 5fc4f1eb-5ab6-4d45-b8f2-cd49a4f98331
  modified: 2026-10-18T17:57:59.114Z
---

User rule (18 Oct 2026, Ostrava 1 + 2): "We should always use the default that makes the wait at the terminal as short as possible."

Ostrava lines 1 and 2 share course numbers and swap trams at Hlavní nádraží at some time of day (records; holiday live feed). But at the weekday peak each line turns in 3 min, against 8 min for a swap, so they stay separate Simutrans lines. Model a cross-line circuit only when a weekday-peak observation shows it.

**Why:** holiday or whole-day evidence doesn't prove the peak pattern, and the longer wait costs an extra tram.
**How to apply:** before pooling or chaining lines, compare the turnaround on each line's own timetable with the swap's turnaround. Pick the shorter one unless the peak itself is observed doing the swap. Related: [[ostrava-tram-vypravenost]], [[schedule-both-ends-same-rate]]
