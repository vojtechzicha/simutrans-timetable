---
name: prague-trolleybus-peak-fleet
description: Prague trolleybus sheet (2026-09-29) — pipeline/praha-trolleybus; OSM wire for battery sections; pak already has VZ-<City>-trolleybus objects; not yet verified by Brno
metadata:
  node_type: memory
  type: project
  originSessionId: e03a85dc-f430-434a-99fb-e6daceff5db2
  modified: 2026-09-29T14:40:58.693Z
---

"Prague Trolleybus Peak Fleet.html" (project root), artifact https://claude.ai/artifact/7P7BZSczRixGop15Fd6zmX. Built 2026-09-29 by `pipeline/praha-trolleybus` (a copy of pipeline/praha, plus `03b_offwire.py`). Its README lists every decision. Companion to [[prague-tram-peak-fleet]].

Non-obvious findings:
- The pak128 checkout already has trolleybus objects for six cities in `build/VZ-<City>-trolleybus/`, so there was no need to wait for the pak session. They are waytype=road with an electric engine, so the wire is information only.
- There is no official battery-section source. The sections come from OSM `trolley_wire=yes` (Overpass needs `Accept: application/json`, else 406) against the GTFS shapes.
- The user's rule to have the Brno session verify splits and pools was NOT done. Brno c6 and Ostrava 10 weren't live on 2026-09-29, and the 52/58 branch splits are unverified.
- The trolleybus display rules a–e were agreed with the Brno (3a) and Ostrava (f5) trolleybus sessions. Prague differs on one point: block turns count as loops (−1 min), as in the tram sheet.

**How to apply:** for an update, follow the README recipe there. For another city's trolleybuses, reuse 03b_offwire.py and the pak folder listing.
