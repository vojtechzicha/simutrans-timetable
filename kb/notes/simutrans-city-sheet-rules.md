---
name: simutrans-city-sheet-rules
description: "How the user wants city transit reference sheets built for their Simutrans \"transformation\" (Pardubice done 2026-09-25)"
metadata:
  node_type: memory
  type: project
  originSessionId: b398b318-70c3-4152-a076-9b9889b6db85
  modified: 2026-09-28T15:09:23.925Z
---

User models real Czech city MHD networks in Simutrans, city by city. Pardubice sheet done 2026-09-25 (pardubice-mhd.html in project root, artifact https://claude.ai/artifact/KrzshkuVv9T5GqpiUKLJ7y).

Rules they gave: model the weekday **afternoon peak**; if a line has no PM peak service but runs in the morning, use morning times. Exclude night, school-only and off-peak-only lines. But when asked, they wanted the flight-bound airport line 90 included anyway. Output: one HTML page with line list (stop patterns both ways, variants distinguished), stops→lines, terminals with departure frequency, headway + minute offsets from terminals (e.g. "every 15 min at :02 :17"), trolleybus vs bus, battery sections, přípoje/přímé spoje, výluky (long-term = model as-is; short-term = use regular state), vehicle category per line (12 m / 18 m / midi). Accessibility is not wanted.

Added 2026-09-28 (tram sheets, shared across the Brno/Prague/Ostrava sessions): no abbreviations anywhere (full type names, full stop and depot names). Vehicle cell = numbers / full types / pak128 core ("≈" = substitute); full object chains appear once in a "Pak128 objects" table. Each line gets a "Simutrans schedule" block in the fork's fields: Departure every / Offset / Also at (≤7) / Leave up to, with the interval dividing 60. **Departures from a loop (smyčka) are set 1 min before the timetable**, and the sheet says so; the timetable goes on the boarding entry.

Since 2026-09-28 the user wants each city's method and data stored in pipeline/<city>/ in the project folder (shared rules in pipeline/README.md), not in memory or scratchpad, ready for timetable updates.

**How to apply:** best data source is CIS JŘ NeTEx on ftp.cisjr.cz/netex/ (trolleybus lines are in NeTEx_DrahyMestske.zip, buses in NeTEx_VerejnaLinkovaDoprava.zip; filter by operator ICO). Vehicle allocation: seznam-autobusu.cz/vypravenost/<city>?datum=. dpmp.cz-style operator sites rate-limit (429, then refuse connections), so fetch sparingly.
