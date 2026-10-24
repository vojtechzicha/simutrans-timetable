---
name: vehicle-type-always-visible
description: "In fleet/vypravenost sheets every listed vehicle must show its type visibly, never only via hover or summary counts"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 4aeb8def-dec3-4568-afbf-a2ae309db52e
  modified: 2026-09-28T14:54:02.661Z
---

Every list of vehicles (by line, by depot) must show each vehicle's type on the page. A good way is to group the vehicles under a visible type label, with length and exact subtypes.

**Why:** In the Brno Tram Peak Fleet depot list, the type appeared only in hover tooltips and in a "14× LF2+LF, 10× 2×EVO2" summary line. The user said "I can't tell the type from this" (2026-09-28).

**How to apply:** Any city fleet or depot sheet. Never rely on title attributes or aggregate counts to convey a per-vehicle attribute. Related: [[brno-tram-peak-fleet]], [[simutrans-city-sheet-rules]]

Update (2026-09-28): the user wants full type names (no shorthand), coupled sets as "A + B" in the same order, and the pak128 object mapped for every vehicle. They also want it compact, showing only the "core of the pak name". The format agreed across the Brno, Prague and Ostrava sheets:
- A 3-line vehicle cell: numbers · depot / full types / pak core.
- Pak core = the final segment of the object name. Add the livery only when the pak has several livery objects for that type.
- Full object chains, liveries and car units go once, in the Pak128 objects table.
- Impossible sets are sent to the pak128 session to fix (it added EVO2 pairs and T3P for Brno).
