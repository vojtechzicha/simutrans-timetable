---
name: plzen-tram-peak-fleet
description: "Plzeň tram peak fleet sheet (2026-09-28) — sources, day choice, line 4 modelling, pak stand-ins pending VZ-PMDP objects"
metadata:
  node_type: memory
  type: project
  originSessionId: 4aeb8def-dec3-4568-afbf-a2ae309db52e
  modified: 2026-09-28T16:08:03.008Z
---

"Plzeň Tram Peak Fleet.html" (project root, artifact https://claude.ai/artifact/J5W3n79YLXAjgruuhtSjam) was built on 2026-09-28.

- **Vehicles:** from Fri 18 Sep 2026. seznam-autobusu mhd-plzen has no tram records for 23–25 Sep, and 18 Sep is the latest complete Friday: 51 sets / 68 cars, all from Vozovna Slovany.
- **Timetable:** PMDP GTFS at jizdnirady.pmdp.cz/jr/gtfs. The URL returns the zip directly, valid from 22 Sep.
- **Line 4 modelling:** one Simutrans line Košutka → Bory → Košutka → Univerzita, because trams alternate between the branches. It has two Košutka entries, 4 min apart, every 8 each.
- **Pak:** The pak128 session added the whole PMDP fleet to VZ-PMDP-tram.pak (main 6547eb6). Every peak type now has an exact object, so the sheet has no stand-ins.

The Olomouc sheet was handed to the Prague session (simutrans-timetable-9e); the user said Plzeň was this session's city after Brno. Related: [[brno-tram-peak-fleet]], [[simutrans-fork-schedule-spec]]
