---
name: odis-save-old-lines
description: "The save's existing ODIS lines (800xxx) predate the fork and are wrong; the owner is rebuilding them from the ODIS sheets, so never fit the sheets to the old convoys"
metadata:
  node_type: memory
  type: project
  originSessionId: 1098259d-3349-4d59-bd20-53ed11629b4d
  modified: 2026-10-22T16:56:25.787Z
---

On 22 Oct 2026 the fleet desk exported FORK-CZR-VZ.sve (saved 18:14). It holds 577 ODIS lines named 800NNN[suffix] (560 road, 17 tram). Most lines on the HKO regional, TFJ, Opavsko and Novojičínsko sheets exist there with convoys, Opava 201–204 included. Only 8 of the Bruntálsko sheet's 40 lines do.

The owner: "The OLD lines ARE WRONG THO - I am redoing it. They were created before the fork."

**Why:** those lines were built before the fork's timetable features, so their vehicles and minutes are no guide.
**How to apply:** the ODIS sheets are the target. Don't rework rosters to keep the old convoys (the "fewest moves" rule doesn't apply to them). Don't infer anything from them either: the old 204 runs electric-only, but that doesn't prove the new 204 route is wired. The export TSV (one row per 800… line: convoys, states, vehicle objects) is in the fleet desk's scratchpad if a count is ever needed.

Related: [[odis-regional-hko]], [[odis-regional-opavsko]], [[pak-fleet-desk]], [[savegame-rename-service]].
