---
name: every-stop-covered-rule
description: "Bus sheets must put every stop a line serves in the afternoon on a Simutrans line (or list why not); check coverage before publishing, hand-set rotating/split lines"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 4860251d-9567-4507-9501-0ec6574bc42e
  modified: 2026-10-20T03:44:17.915Z
---

On 20 Oct 2026, on the Havířov/Karviná/Orlová sheet, the owner said: "Do much better please - e.g. 501 is the only line running to Dětmarovice, how can we not model that?" The per-terminus-pair branch rule had dropped every sparse or one-way leg. That left out Dětmarovice, Hradiště, Stonava and Důl Darkov, and it reduced 505's rotating bus and the 401/406 ring to wrong shuttles.

**Why:** the owner builds the network in the game from the sheet. A place that no Simutrans line serves is simply missing, however few trips it gets.

**How to apply:**
- Before publishing any bus sheet, run a sheet-wide stop coverage check: every stop served 13:00–19:00 must be on some modelled Simutrans line, or be listed with its reason.
- Also list, per card, the trips that are not on any of the line's Simutrans lines.
- Lines whose buses rotate through branches, or that are halves of a ring across two line numbers, get a hand-set circuit (`line_overrides`, Ostrava 41 precedent).
- Sparse unique branches of REGIONAL lines: no every 1440/720 any more (owner, 20 Oct); use the repeating interval ≤ 480 (bus-schedule-method v3). Local city lines: only afternoon peak + unique stops; off-peak single trips are listed, exceptions asked (see [[regional-vs-local-rules]]). Depot runs never.
- Keep one Simutrans line per real line. Offer pooling as an option, but don't pool silently.

Reference implementation: `pipeline/havirov-karvina-orlova` (04_roster step 7, `lib.build_overrides`). Related: [[havirov-karvina-orlova-bus]], [[find-every-train-feedback]], [[model-line-at-its-peak]].
