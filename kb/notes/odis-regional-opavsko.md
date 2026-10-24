---
name: odis-regional-opavsko
description: ODIS sheet Opavsko/Vítkovsko/Hlučínsko + MHD Opava buses and trolleybuses (21 Oct 2026) — pipeline/odis-regional-opavsko via HKO scripts --base; 125 vehicles; 204 designed trolleybuses post-step
metadata:
  node_type: memory
  type: project
  originSessionId: 1098259d-3349-4d59-bd20-53ed11629b4d
  modified: 2026-10-21T19:03:33.825Z
---

"ODIS Opavsko Vitkovsko Hlucinsko.html" (artifact https://claude.ai/artifact/K5ZeDCY2YYqV1Sz3tQwj3j, v1 21 Oct 2026, v6 22 Oct with the wire check and off-wire objects). Areas 902 Opavsko + 903 Vítkovsko (Z-Group bus, 22-/23-), 904 Hlučínsko (Transdev Slezsko pr. Ostrava, 24-), 905 MHD Opava (MDPO). Owner insisted: "do include trolleybuses".

- Opava trolleybuses 905201–905204 come from CIS JŘ city-transport JDF (draha/mestske) via `jdf.extra_zips`; area `mhd-opava-trol` (prefix 90520, listed before the bus area).
- MDPO live plates are `MDPO<num>` → `fleet.carriers[].live_plate`; seznam-autobusu ids: Z-Group 240, MDPO 338, Transdev Morava 7546.
- 204 ran with replacement buses 12–23 Oct (Vrchní street works) → modelled as regular trolleybus; designed trolleybuses via sheet-local `authoring/fill_designed.py` run between 04_roster and 06_render (shared roster can't design them). Parent's ordered roster pass must run it too.
- **Wire (22 Oct, sheet v5):** `authoring/offwire.py` = OSM relations vs OSM trolley_wire (Prague 03b method). 201–203 fully wired; 204 unwired Ratibořská–Vrchní–Pekařská–Divadlo (2.0 km) + Kylešovice Bílovecká–škola (0.6 km; OSM relation complete=no, end added from timetable stops). Matches Wikipedia's partial-trolleybus stops. Overpass main server gave 502s; maps.mail.ru mirror worked.
- **Auxiliary drive** from register vehicle pages ("alternativní pohon"): battery 32 Tr 314–323, diesel generator 26 Tr 305–306, none on others (incl. 32 Tr 324–328, 36 Tr). `alt_drive.py` marks them; 204 designed = 315, 314, 319, 323 + 305 (316 was out on 203). The earlier 303/304 picks couldn't leave the wire. Objects installed 22 Oct (pak main 684fc09): 32Tr_battery for 314–323, 26TrDG for 305–306, picked by pak rules on type + `alt` (sheet v6).
- Pak (fleet desk): VZ-ODIS `bila` (Z-Group), `bilacervenykruh`/`transdev` (Hlučínsko), VZ-DPOpava-bus/-trolleybus; BNG 10,5 loan = VZ-MHDHavirov stand-in.
- Shared-line split: models 260/920 (vs Bruntálsko), 261/263/270/285/678 (vs Novojičínsko), 555; 615/620/691–693 on the NJ sheet.
- Rebuild recipe + decisions in the folder README; authoring scripts opa_spec/opa_config/opa_notes.

Related: [[odis-regional-tfj]], [[odis-regional-hko]], [[pak-fleet-desk]], [[rail-engineering-works-check]].
