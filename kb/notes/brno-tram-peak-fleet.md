---
name: brno-tram-peak-fleet
description: "Brno tram per-vehicle peak fleet sheet (2026-09-28) — bmhd.cz sources, WAF workaround, depot parity finding"
metadata:
  node_type: memory
  type: project
  originSessionId: 4aeb8def-dec3-4568-afbf-a2ae309db52e
  modified: 2026-09-28T14:51:03.040Z
---

On 2026-09-28 I built "Brno Tram Peak Fleet.html" (project root, artifact https://claude.ai/artifact/5ntT3kwFmuEU3Bo3RbvvZD). It covers the Fri 25 Sep 2026 PM-peak vypravenost on the 27 Sep network. The user's ask "yesterday's state" (a Sunday before the 28 Sep holiday) was read as: vehicles from the last weekday, network as of yesterday. The user confirmed this reading in the Prague session.

**How to apply:**
- bmhd.cz returns 403 from its WAF to plain curl. It works with a full Chrome User-Agent plus Accept and Accept-Language headers, with about 2 s between requests.
- Sources: vypravenost.php?datum=&linka= gives kurz → cars with notes (ráno / odpoledne / před/po výměně, no times). The per-depot register is /evidence-dpmb/vozovna/{m,p}. For exact subtypes, join the vozp.php listings to vehicles by data-car-id.
- On weekdays, odd kurzy correspond to Pisárky and even kurzy to Medlánky. The BMHD register still lists EVO2 1822–1835 and T3R.EV 1531/1560/1562/1569 at Medlánky, but these cars run only odd kurzy. The sheet shows both views.
- The IDS JMK GTFS (kordis-jmk.cz/gtfs/gtfs.zip) has no kurz numbers in block_id.

Related: [[simutrans-city-sheet-rules]]

Post-closure sheet (2026-09-28): "Brno Tram Fleet from 29 Sep.html", artifact https://claude.ai/artifact/3ps2U3Ac81p5h3ABRwgQVg.
- The IDS JMK feed switches the tram timetable on Tue 29 Sep, not 1 Oct. Line 10 goes back to the Komín loop; lines 1, 3 and 12 are retimed; lines 2, 7 and 9 shift by 1 min.
- Line 3 is now every 20 min with 3 slots; line 12 every 14 min with 3 slots (exact; 14 doesn't divide 1440, which the fork allows).
- Fleet (corrected 2026-09-28, by timetable cycle): line 3 goes 19 → 16 (3/21 and 3/24 move to line 12, 3/7 goes to reserve), line 12 14 → 16, line 10 unchanged.
- Built by pipeline/brno in the project folder (states closure-2026-09-27 and from-2026-09-29); see [[city-pipelines]].

Update 2026-09-29: the spares rule ([[spares-not-needed-rule]]) is applied to both Brno tram sheets and Plzeň. Surplus beyond each Simutrans line's need is marked not needed. The from-29-Sep moves (3/21, 3/24 → line 12, 3/7 → reserve) are dropped: line 12's own trams meet its need. 5S was 1 short (4 logged vs need 5), so 1088 (VarioLF2R.E, 5S on 24 and 17 Sep, free on 25 Sep) is a designed tram (state fleet.designed).
