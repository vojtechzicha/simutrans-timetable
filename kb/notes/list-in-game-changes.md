---
name: list-in-game-changes
description: "After changing a published sheet, always tell the owner exactly which lines/rows to re-enter in the game, because the lines are already set up in their save"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 5d304c5e-1e80-40b2-9839-f53d6456b698
  modified: 2026-10-22T16:10:47.952Z
---

After any change to a published fleet sheet, end with a list of what the owner must change in the game. For each item give the line, the terminus entry, the old and new "Departure every / Offset / Also at" values, and any bus to add or remove.

**Why:** on 2026-10-22 the owner said "if you did any changes recently, I'll need you to tell me which lines to check - they are already in game". The sheets drive a live save game, so a silent republish leaves the game out of step with the sheet.

**How to apply:** the list covers every row whose set minutes changed and every vehicle that joined or left a line. Include changes from earlier in the session that the owner may not have entered yet. Related: [[ostrava-bus-vypravenost]], [[savegame-rename-service]].
