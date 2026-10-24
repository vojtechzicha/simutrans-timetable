---
name: rail-design-rules
description: "The careful rail-line design method the user approved on 3 Oct 2026 (real structure, odd-first offsets, timed long stops, round-trip vehicle counts, simple page); full text in pipeline/rail-design-rules.md"
metadata:
  node_type: memory
  type: feedback
  originSessionId: d8b73c98-95bf-4e88-8c04-c228f701b2a3
  modified: 2026-10-03T20:03:09.152Z
---

The full rules are in `pipeline/rail-design-rules.md` in the project folder. Read it before designing any rail sheet, local or long-distance.

On 3 Oct 2026 the user called the local design "lovingly gotten correct". They said MD-CR had "none of this careful planning" and asked for MD-CR to be redone with these rules.

In short:
- **Real workday trains, Mon–Fri.** Seasonal and Friday-only trains are listed, not modelled.
- **Model the real structure.** Join trains into one line only where they really run through, and never extend past a real terminus. Partial through trains become their own line in alternate hours.
- **Lines on a shared section alternate hours.** Uneven combined headways are fine.
- **Offsets are odd hours first** (interval 120: minute for L, minute + 60 for S).
- **Leave up to 30.**
- **Timed stops:** termini, every stay of 5 min or more, and every wait point, per direction. Each timed departure must come after the arrival.
- **Vehicles:** write a full clock round trip, rounded up to a multiple of the interval, then vehicles = round trip ÷ interval.
- **Page:** plain chat-like tables.

**Why:** the user checks every detail against reality and against the game, and wants functional lines that look like the real thing.

**How to apply:** follow the file. Ask when it is unclear which real trains the user cares about. Related: [[local-rail-062-064]], [[simple-sheet-style]], [[simutrans-fork-schedule-spec]], [[md-cr-rail-sheet]].
