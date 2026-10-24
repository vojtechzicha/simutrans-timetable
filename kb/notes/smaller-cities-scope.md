---
name: smaller-cities-scope
description: "\"Smaller cities\" sheet scope agreed with the user on 2026-09-29: Olomouc tram, Pardubice rebuild, Plzeň trolleybus+bus, Olomouc bus, Most–Litvínov bus"
metadata:
  node_type: memory
  type: project
  originSessionId: b043ac4c-1647-425c-9154-303ee80b8dbc
  modified: 2026-09-29T17:40:18.869Z
---

On 2026-09-29 session 5a handed the "smaller cities" to session a2. When asked, the user chose:
- Pardubice (rebuilt and republished 29 Sep, v2; Fri 25 Sep vehicles, 29 Sep network): rebuild as `pipeline/pardubice`, a per-vehicle trolleybus + bus sheet. It keeps the file name "Pardubice MHD Peak Sheet.html" and the artifact https://claude.ai/artifact/KrzshkuVv9T5GqpiUKLJ7y. The old per-line sheet is backed up in `pipeline/pardubice/legacy/`.
- New sheets: Plzeň trolleybus, Plzeň bus, Olomouc bus, Most–Litvínov bus (`pipeline/plzen-trolleybus`, `plzen-bus`, `olomouc-bus`, `most-litvinov-bus`).
- Olomouc tram (`pipeline/olomouc`) was taken over from 9e/5a. On 29 Sep it got the logged-surplus "not needed" patch and the phone header, and was republished to the same URL (0 not needed: recorded = need on every line).

Tram folders owned by others (plzen → 3a; most-litvinov → b5) are read-only for the new bus/trolleybus pipelines.

**Why:** the user wants every city's sheets under the same shared rules ([[spares-not-needed-rule]], [[designed-vehicles-roster-rule]], [[sticky-header-all-sheets]], [[never-ship-without-vehicles]]).
**How to apply:** pak requests for the new sheets go to the VZ pak session as each pipeline's `pak_request.md` (type × livery × car numbers). Related: [[olomouc-tram-peak-fleet]], [[simutrans-city-sheet-rules]].

Published 29 Sep 2026:
- Olomouc bus: https://claude.ai/artifact/MJz5Q7xYehTCPKhpBDfLHG. Vehicle day is Tue 29 Sep, because there are no bus records on 18/25 Sep.
- Most–Litvínov bus: https://claude.ai/artifact/TUU9pmZU3fcjJK95Fe4ZPN. All designed from plates and photos. The badge reads "Tram replacement", not NAD.
- Plzeň trolleybus: https://claude.ai/artifact/B9vVcHutYdXdg4sscpA1gR
- Plzeň bus: https://claude.ai/artifact/LE4trKFDZjkAjpX2EhvJCa
  Both Plzeň sheets use Fri 18 Sep vehicles. No VZ-PMDP trolleybus or bus pak existed, so all objects were requested.

User rulings for Most bus: every fleet type and livery must be on a line, with long buses on lines that run articulated buses. No October version. Each line keeps exactly its needed count, shown in a table.
