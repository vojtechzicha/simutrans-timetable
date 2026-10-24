---
name: most-tram-vypravenost
description: "Most–Litvínov tram per-vehicle peak sheet (done 2026-09-28) — no allocation data exists, roster designed by operator rules; pak VZ-DPMostLitvinov"
metadata:
  node_type: memory
  type: project
  originSessionId: bc38834b-4e71-40d9-9f27-368436ac6fb5
  modified: 2026-09-28T16:01:14.591Z
---

Sheet done 2026-09-28: "Most-Litvinov Tram Vypravenost.html" in project root, artifact https://claude.ai/artifact/FxHCAC84oCJA7qkbCKiQZi. Same format as [[ostrava-tram-vypravenost]].

- **No allocation data for DPmML anywhere:** seznam-autobusu has zero records, and the city live layer (mapy.mesto-most.cz/koop/rest/services/mhd/FeatureServer/0) returns empty.
- **Roster designed by operator rules:** EVO2 on line 4, VarioLF+ line 2 only, fixed T3M.3 pairs on line 1 shift trips.
- **Network:** from 1 Mar 2026, Chempark–Citadela is replacement buses (Litvínov modernisation), so trips are cut at Záluží, Chempark. Busiest moment is 15:00 (Chempark shift change), not 16:00. Line 3 is morning-only.
- **Data:** JDF lines 575001–575004, JDF 1.11 format (Zasspoje arr/dep at idx 10/11).
- **Fleet:** seznam-autobusu iddopravce=399.
- **Pak:** VZ-DPMostLitvinov-*-mostzlutocervena-*; one livery, 5 exact types.

**Pipeline (2026-09-28):** pipeline/most-litvinov/ (README, config.json with the designed roster, scripts, raw/derived). Update = follow its README recipe.
