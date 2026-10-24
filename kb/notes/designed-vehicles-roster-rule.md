---
name: designed-vehicles-roster-rule
description: "Designed (unrecorded) vehicles on fleet sheets need real car numbers from line history, cover every roster type, and show spares as \"not needed\""
metadata:
  node_type: memory
  type: feedback
  originSessionId: e03a85dc-f430-434a-99fb-e6daceff5db2
  modified: 2026-09-29T17:26:11.625Z
---

When a line's recorded vehicles fall short of the need, every designed vehicle gets a real car number. Never use a blank "type only" placeholder. The car must come from the line's own history, be active, and not be out anywhere that day (check the day overview or live feed).

If the history holds more free cars than needed:
- Pick them so that every type in the line's full roster (history plus logged cars) is represented among the vehicles actually used.
- List the leftover free cars on the card with a "not needed" marker. They are not counted.

**Why:** the user said on 2026-09-29: "fetch older records and use real car numbers", then "if you have in history more cars than is needed, show the not needed in marker. Pick the not needed in general rule to not skip any type - each that is represented in full roster should be represented in actually used vehicles", and asked that other sessions be told too.

**How to apply:**
- Reference implementation: `pipeline/praha-bus/scripts/04_courses.py`. The rule text is in `pipeline/README.md` under "Roster coverage and spares".
- If the history runs out: free active cars of the line's own types first, then the operator's usual types.
- The choice of which to keep, and the logged-surplus case, are in [[spares-not-needed-rule]]. The user also said to apply that rule to trams and trolleybuses: "does it make sense for trams and trolleybuses as well? If yes, do so". The Prague sheets use it (spare patch in praha/praha-trolleybus 04_courses.py).
- Ownership on 29 Sep: 5a Prague bus/trolleybus/tram; 3a Brno sheets and Plzeň; b5 Ostrava bus/trolleybus/tram and Most; a2 Olomouc and the smaller cities.

Related: [[spares-not-needed-rule]], [[prague-bus-lines-check]], [[simutrans-city-sheet-rules]]

**Fleet-wide coverage (user, 29 Sep 2026, Most–Litvínov bus, where the whole roster is designed):** "put somewhere where other long buses are used, each type should be represented". Every city-fleet type AND livery must appear on some line, including weekend-only cars (marked "normally weekends only"). Articulated ones go only on lines that already run articulated buses. Each line still keeps exactly its needed count, and the displaced car becomes "not needed". Show a per-line table of needed vs assigned ("keep the needed amount of lines somewhere").
