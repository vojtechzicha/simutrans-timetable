---
name: simutrans-fork-schedule-spec
description: "How the user's Simutrans fork timetables work (fields, units, Also at limit, variants) and how city sheets convert real departures into them"
metadata:
  node_type: memory
  type: reference
  originSessionId: 4aeb8def-dec3-4568-afbf-a2ae309db52e
  modified: 2026-09-28T15:00:08.694Z
---

Source: engine session simutrans-122-0-7c (engine checkout C:\Users\vojte\Developer\simutrans-122.0 at 2c42306). The owner routes engine questions through that session; the pak128 session doesn't answer them.

- The settings live per stop entry on the Scheduling tab. They only work when the calendar is on (minutes_per_month; the owner uses 480):
  - "Departure every (min)": 0 means no timetable.
  - "Offset (min)": must be less than the interval. User correction 2026-10-03: with a 120 interval, **odd hours come first** (offset 4 = L:04) and even hours are +60 (offset 66 = S:06). Don't assume offsets count from midnight. In general: offset = (real time − 60) mod interval. The user confirmed this for 240 (8:08 → 188).
  - "Also at (min)": up to 7 extra offsets, so at most 8 departures per cycle.
  - "Leave up to (min late)": defaults to automatic, half the gap.
- Values are whole minutes only. Use an interval that divides 1440, or the pattern restarts at midnight.
- Spacing is automatic within a line: each slot goes to one tram. Don't set per-vehicle offsets. Set the timetable on the termini (and timing points).
- "Also at" cannot change the route. Short workings and branches need their own line, with offsets chosen so the lines interleave; lines don't coordinate with each other. Don't model depot runs. Through-running is one line only if every tram runs through.
- There is no import, so the owner types the values in. JSON export exists: `simutrans -load NAME -export FILE.json`.

City-sheet rule, agreed with the Prague and Ostrava sessions on 2026-09-28: for each terminus, fit the longest exact run in the afternoon peak core, using the simplest interval that divides 60 and at most 8 slots. Show the matched time span, and list approximations (e.g. Brno 12, ±3 min) with their deviation. Related: [[simutrans-city-sheet-rules]], [[brno-tram-peak-fleet]]

Loop rule (user, 2026-09-28): a tram departing a loop (smyčka) is scheduled 1 min before the real timetable. Offset and each Also-at value become (real − 1) mod interval; the interval is unchanged. Stub and turn-back termini keep the real minute, and every sheet must state this visibly. The engine session confirmed it is valid: put the timetable on the boarding/departure entry, and keep values < interval and distinct.

**20 Oct 2026:** the Ostrava sheets (shared `ostrava/scripts/lib.py` loop_shift) had ignored the 01:00 origin for intervals not dividing 60, so bus every-40 rows were typed 20 min off. Now fixed. Check any sheet that uses intervals like 40, 45, 80, 90 or 120 for the same mistake.
- **Fold evenly spaced slots** (owner, 20 Oct 2026, Ostrava 27A): never write 'every 60, Offset 17, Also at 47' when it is 'every 30, Offset 17'. A shared interval from interleaving must be folded back per row before output.
