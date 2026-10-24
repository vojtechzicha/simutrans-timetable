---
name: odis-regional-bruntalsko
description: ODIS sheet Bruntálsko/Krnovsko/Rýmařovsko + MHD Krnov/Bruntál (21 Oct 2026) — pipeline/odis-regional-bruntalsko via HKO scripts --base; Transdev Morava; 63 buses
metadata:
  node_type: memory
  type: project
  originSessionId: 1098259d-3349-4d59-bd20-53ed11629b4d
  modified: 2026-10-21T18:56:12.312Z
---

"ODIS Bruntalsko Krnovsko Rymarovsko.html" (project root, artifact https://claude.ai/artifact/ApSB65b8skppcUGCfFHtnZ, v1 21 Oct 2026), built by a fork of the main session after the owner's "Yes, do those next sheets".

- **Areas:** 852 Krnovsko, 853 Bruntálsko, 854 Rýmařovsko, 856 MHD Krnov, 855 MHD Bruntál — all Transdev Morava pr. Bruntál (seznam-autobusu carrier 7546). Prefix→area from fleet numbers on the live map: 82-/83-/84- regional, 81- Krnov town.
- **No scripts of its own:** shared `odis-regional-hko/scripts --base odis-regional-bruntalsko`; config from `authoring/brn_spec.py` (+ brn_notes.py) and `brn_config.py` (also fixes SOR bus lengths in fleet.json until 01c_fleet tlen() handles "CN 10,5").
- 260/920 belong to the Opavsko sheet (other_sheets.opavsko). Short diversions 876/912/921 → regular timetables.
- 40 lines → 51 Simutrans lines, 63 buses (58 seen, 5 designed); coverage 471/471; unmodelled 803, 815, 852, 876, 914.
- Pak confirmed by the fleet desk: VZ-ODIS `transdev` livery, VZ-MHDKrnov `krnovbila`; no stand-ins.
- Owner checks: 877 :34/:24 vs real :40/:20 (+1 bus); 801 PZ as zone shuttle; 913 out 12:07 vs 5:55; 832 real minutes with 2 buses.

Related: [[odis-regional-tfj]], [[odis-regional-hko]], [[pak-fleet-desk]], [[hand-review-schedules-rule]].
