---
name: savegame-rename-service
description: "Renaming objects in the owner's Simutrans save goes through engine session simutrans-122-0-58 via a TSV list; never run the rename tool yourself"
metadata:
  node_type: memory
  type: reference
  originSessionId: b0e0d2a3-0b49-4682-957a-d187cf469167
  modified: 2026-09-29T15:51:51.789Z
---

Announced 2026-09-29 by the engine session simutrans-122-0-58. It is the only session that touches the save files (D:\OneDrive\Documents\Simutrans\save).

- **What to send:** the path of a UTF-8 TSV with rows `KIND<TAB>ID<TAB>OLD NAME<TAB>NEW NAME`. KIND is halt, line, convoy (ids from the JSON export), player (its number), city (X,Y) or factory/marker (X,Y,Z). An OLD NAME of `*` skips the check; lines starting with # are comments.
- **What it does:** backs the save up to `save\backup\`, then writes `NAME-renamed-<date>.sve`. The original is never overwritten. A dry run or a JSON export (for ids) is available on request.
- **Rules:** two stops can't share a name, so swaps need a temporary name. The owner must save first if playing. A 400 MB save takes 1–2 min to load.

Related: [[simutrans-fork-schedule-spec]] (the same engine session).
