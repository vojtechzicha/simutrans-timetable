---
name: spares-not-needed-rule
description: "Fleet sheets: surplus vehicles (logged or history) beyond a line's need are marked \"not needed\", keeping every roster type; afternoon-only duties dropped first"
metadata:
  node_type: memory
  type: feedback
  originSessionId: a53fa21d-8dbc-4fdc-bf31-4d8362899694
  modified: 2026-09-29T17:31:02.056Z
---

When a line has more vehicles than it needs, keep exactly the need counted and mark the rest "not needed". This covers both surplus logged that day and leftover history cars when vehicles are designed.

How to choose which to keep:
- Keep one of every vehicle type in the line's roster first, most frequent type first.
- Among the rest, drop afternoon-only duties ("odpoledne" / "odpolední kurz") first, then the highest kurz numbers.
- A substitute bus on a trolleybus line is not a roster type, so it goes first.

Show "not needed" vehicles dimmed at the bottom of the line card, and leave them out of every count, the depots and the pak totals.

**Why:** the user said on 2026-09-29: "if you have in history more cars than is needed, show the not needed in marker. Pick the not needed in general rule to not skip any type". Asked about the ambiguity, they confirmed it also covers logged surplus, and picked the afternoon-only tie-break. Before this, sheets kept logged surplus counted as "operator's slack".

**How to apply:** every city fleet sheet. The shared text is in pipeline/README.md under "Roster coverage and spares". The code is `mark_spares` in pipeline/brno-trolleybus/scripts/common.py. Related: [[vehicle-type-always-visible]], [[brno-bus-peak-fleet]], [[brno-trolleybus-peak-fleet]].
