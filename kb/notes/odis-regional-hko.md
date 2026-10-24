---
name: odis-regional-hko
description: "ODIS regional sheet Havířovsko/Karvinsko/Orlovsko (21 Oct 2026) — pipeline/odis-regional-hko, scope by licence prefix, every line hand-set by the regional method, 67 buses"
metadata:
  node_type: memory
  type: project
  originSessionId: 1098259d-3349-4d59-bd20-53ed11629b4d
  modified: 2026-10-21T16:59:10.960Z
---

"ODIS Regional Havirovsko Karvinsko Orlovsko.html" (project root, artifact https://claude.ai/artifact/SFgd2KE6xRv9PLKtS5qMnw, v1 21 Oct 2026), built by `pipeline/odis-regional-hko` (README has every decision and the update recipe). Owner's ask: "Now we've done regional lines - study deeply the rules. Can you do ODIS Regionals - Orlovsko, Karvinsko, Havířovsko?"

- **Scope = kraj contract areas by licence prefix:** 912xxx Havířovsko (I+II), 873xxx Karvinsko, 874xxx Orlovsko (871 Českotěšínsko, 863 Frýdecko-Místecko, 904 Hlučínsko). Confirmed by live-map branches (pr. Havířov/Karviná/Orlová), fleet prefixes (42-/43-, 52-, 51-) and register notes ("provozní oblast …"). 553 = 873553 + 874553, merged by ODIS number.
- **440, 441, 442, 531, 534, 535 stay on the Ostrava sheet** (Hranečník cards); listed and linked, not repeated.
- Every line hand-set in `config.lines` (bus-schedule-method v3): legs with `at` / `knot`+`knot_at` / `core_to` / `via` / `notvia` / `untimed` / `stops_via`. Shift variants every 480 (451 Elektrárna, 553 Autopal, 559 Kovošrot, 582 ČSM, 453, 460, 563). Where a variant takes one hour of an hourly line, the main line is every 480 with seven slots (559, 582). 543 re-paired from plate chains. Shift/sparse lines whose stops other lines serve are listed (444, 446, 455, 457, 461, 463, 540, 541, 550, 554, 557, 564).
- 29 lines → 37 Simutrans lines, 67 buses (65 seen on the 20 Oct live map, 2 designed); 42 buses really on the road at 16:00, so pooling is an open owner option. Coverage 372/372.
- **Choices put to the owner (To check, top):** 451 and 533 modelled at 16:00, not their busiest 13–15; 451 Elektrárna 12:45 instead of 13:00; 582 regular route instead of its diversion to 30 Nov.
- **Open question asked:** does the save already hold any of these regional lines (pak session f3 mentioned an ODIS migration plan)? If yes, keep in-game buses (fewest moves).

Second sheet on the same scripts: [[odis-regional-tfj]].

Related: [[havirov-karvina-orlova-coordination]], [[core-points-repeating-interval-rule]], [[regional-vs-local-rules]], [[every-stop-covered-rule]], [[odis-live-map-source]].
