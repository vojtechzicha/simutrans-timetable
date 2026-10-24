---
name: ostrava-trolleybus-vypravenost
description: "Ostrava trolleybus per-vehicle PM-peak sheet (2026-09-29) — observed live roster, pipeline/ostrava-trolleybus reuses the tram lib, battery sections"
metadata:
  node_type: memory
  type: project
  originSessionId: b0e0d2a3-0b49-4682-957a-d187cf469167
  modified: 2026-09-29T14:44:55.272Z
---

"Ostrava Trolleybus Vypravenost.html" (project root, artifact https://claude.ai/artifact/HFHXt2UZ1NE1SE6KYQAMXp), built by `pipeline/ostrava-trolleybus` (README has the update recipe). Asked 2026-09-29 as "same as Ostrava trams, same level of info"; see [[ostrava-tram-vypravenost]].

- **Roster is observed**, not designed: DPO live feed (vehicleType "troll") polled on Tue 29 Sep 2026 from 16:29, so the vehicle day is that Tuesday rather than the tram sheet's Fri 25 Sep. seznam-autobusu still gets DPO trolleybus records from tram-bus.cz (unlike trams), but the rows carry no time and DPO duties interline heavily (1xx: 101/106/107; 2xx: 102/103/105/108/109; 8xx: 104 + 101), so they are only a cross-check.
- **The live feed has no history**, so an update needs the poller running over a weekday peak.
- Live trip start/final names don't follow the JDF branches, so the 101/107 branches (the battery legs beyond Hranečník) are decided by longitude.
- Battery sections come from mhd-ostrava.cz and Wikipedia (the JDF doesn't mark them). Battery cars: 26Tr 3731–3740 and all 36Tr. The 27Tr have supercapacitors only.
- The pak repo is readable locally: `C:\Users\vojte\Developer\simutrans-custom-czech-pak128\build\VZ-<City>-trolleybus\`.
- Parallel trolleybus sheets on 2026-09-29: Brno (session 3a, pipeline/brno-trolleybus) and Praha (5a). 3a's shared trolleybus rules were agreed: 3-line cell, battery sections per line, a bus on a trolleybus line counted separately, and loop −1.

**20 Oct 2026:** schedule unchanged under the refined rule. Added real-minute subtitles and the Fit column; 106 Dědičná noted as ended. Artifact version 3.
- **Pak 2cdf3f3 (20 Oct 2026):** 27Tr livery is chosen by paint (3805-3810 blue-yellow). 3813-3818 use 27TrSolaris_partial ('27Tr (2024)', electric). 27Tr rear section is length 6.
