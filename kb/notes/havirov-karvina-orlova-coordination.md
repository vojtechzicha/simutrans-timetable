---
name: havirov-karvina-orlova-coordination
description: Session a4 builds pipeline/havirov-karvina-orlova on the Ostrava bus lib (read-only); message it on lib API or rule changes
metadata:
  type: project
---
From 20 Oct 2026, session a4 (simutrans-timetable-a4) builds a Havířov / Karviná / Orlová MHD bus sheet in pipeline/havirov-karvina-orlova. It imports ostrava/scripts/lib.py and ostrava-bus/scripts/lib.py read-only and edits no ostrava* file.

**Why:** the owner asked for it "like Ostrava, in coordination". The Transdev buses designed on the Hranečník ODIS cards (odis.json, vehicle day 30 Sep) must not also appear on a4's sheet.

**How to apply:**
- Message a4 before changing any shared lib signature: branch_pairs, line_anchor, interleave, plans, pattern_need, circuitize, path_variants.
- Forward any new rule the owner gives for Ostrava buses.
- Regional ODIS lines use VZ-ODIS-bus (pak session f3, main 6f7b639, 20 Oct 2026; adopted on the Ostrava sheet as v23). Town lines use VZ-MHD<Town>. CZ-ODIS / CZR-ODIS are only for the old save.

Related: [[ostrava-bus-vypravenost]], [[model-line-at-its-peak]].

**From 21 Oct 2026, a third sheet uses the same data:** `pipeline/odis-regional-hko` (session 6b, [[odis-regional-hko]]) reads a4's JDF, live poll and fleet.json, and the Ostrava `odis.json`. It drops every plate that the HKO roster or the Hranečník cards count, so a bus stays on one sheet. Whenever either of those sheets re-rosters, re-run `04_roster.py` there.
