---
name: size-from-suggested-pattern
description: Always size every line's vehicle need from the schedule pattern the sheet suggests, not from the raw timetable at the peak moment
metadata:
  type: feedback
---

User rule (20 Oct 2026, Ostrava bus 21): "You should always size it from the pattern you are suggesting - for all lines."
Bus 21 had been sized at 4 from the every-20 timetable around 16:00, plus the tail of buses still on the road, while the sheet suggested every 40, which 2 buses run. The user had found 3 enough in the game.

**Why:** the owner types the suggested pattern into Simutrans; a need from another pattern is wrong in the game.
**How to apply:** compute the schedule first, then the need by following a vehicle round the suggested slots (real running times, minimum layover); Ostrava's `lib.pattern_need` does this. Don't add "variant extra" buses for unmodelled variants. When needs drop on a published sheet, mark the extras "not needed (park it)" rather than reshuffling (fewest moves), and show what the slower option would need on rows to check. Related: [[schedule-both-ends-same-rate]], [[shortest-terminal-wait-rule]], [[city-pipelines]]
