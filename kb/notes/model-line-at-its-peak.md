---
name: model-line-at-its-peak
description: Model each line at its own busiest afternoon stretch, not a fixed 16:00; branches at a shared terminus must interleave as the real timetable does
metadata:
  type: feedback
---

Owner, 20 Oct 2026 (Ostrava bus 23): "for 23 i see 20 minutes as the most common afternoon peak pattern - why are you seeing 40? Can we make sure we are representing the situation correctly across all lines?" Also: "if the real timetable interleaves, you should interleave. I thought that is the whole point?"

**Why:** a fixed 16:00 anchor modelled about 25 Ostrava bus lines in their wind-down (shift-change peaks fall 13:00–16:00). Branch patterns fitted one by one bunched at shared termini.
**How to apply:** anchor each line at its busiest 2 h in 13:00–18:00, unless 15:00–17:00 is within one departure of it (then keep the sheet's peak). Shift every fit, sizing and label window with the anchor. At shared termini, fit the branches together on one interval so their slots alternate as in reality, and check with a bunching scan. Ostrava bus: `lib.line_anchor`, `lib.interleave`. Related: [[schedule-both-ends-same-rate]], [[size-from-suggested-pattern]], [[shortest-terminal-wait-rule]]
- **Cross-branch circuits (owner, 20 Oct: "where it significantly shortens wait, do it"):** for star lines, choose the best assignment of returning buses to next slots at the shared terminus; split it into cycles, one Simutrans line each, adopted only if it saves >= 1 bus (Ostrava `lib.circuitize`: only 58 after the fix). Far-end slots must come from the fitted far row, not raw residues: v14 used raw residues and shipped legs off real departures. Always count each leg's slots against real departures before publishing. Don't promise savings from a wind-down observation: 23's "3 buses" was seen at 16:00 every 40, while its every-20 peak needs 4.
- **Path variants (owner, 20 Oct, line 28):** one direction running two paths between the same termini (28 Šenov–Václavovice via U Slívy / via střed, alternating) must not be one merged row; model as one circuit Simutrans line, out on one path and back on the other (`lib.path_variants`).
- **Path variants also when one path has a single own stop** (owner, 20 Oct: 32 Hlučínská vs Hálkova). Before saying a stop is covered, check it's on a *modelled* path (most common sequence of a scheduled direction), not just on some trip of the line.
- **Interleave at junctions too** (owner, 20 Oct, screenshot of 23 at Rychvald, rozcestí): a branch's far terminus that another branch passes through is a shared point; don't let both depart in the same minute there. Check intermediate stops, not just termini, when scanning for bunching.
- **Stop coverage rule** (owner on the HKO sheet, forwarded by a4 on 20 Oct; applies to all bus sheets): every stop served 13:00–19:00 must be on a modelled Simutrans line or listed with the reason (Ostrava: Coverage section in 06_render). Line-unique stops are never 'skipped stops' (49 Hrušov, Růžová). Daily (every 1440) lines for single-trip stops: ask the owner first on the Ostrava sheet.
