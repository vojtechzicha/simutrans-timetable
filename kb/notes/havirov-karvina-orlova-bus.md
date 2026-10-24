---
name: havirov-karvina-orlova-bus
description: "Havířov/Karviná/Orlová MHD bus sheet (20 Oct 2026) — pipeline/havirov-karvina-orlova, ODIS live map gives plates, imports Ostrava bus rules, VZ-MHD<Town> pak"
metadata:
  node_type: memory
  type: project
  originSessionId: 4860251d-9567-4507-9501-0ec6574bc42e
  modified: 2026-10-20T03:20:43.318Z
---

"Havirov-Karvina-Orlova Bus Vypravenost.html" (project root, artifact https://claude.ai/artifact/UmPg6guEAbmSune5YnFTVb, v11 final on 20 Oct 2026: 60 buses observed live, 11 designed, need 68), built by `pipeline/havirov-karvina-orlova` (the README has every decision and the update recipe). The owner asked on 20 Oct 2026: "Similar to Ostrava and in coordination". The lines are Transdev Slezsko MHD: Havířov 401–421 + 434, Orlová 501–505, Karviná 511–520.

- **ODIS live map with plates:** POST https://mpvnet.cz/Odis/map/mapData. It needs the Origin and Referer headers. Each row gives licence|line|course|…|start|final|1|PLATE. It has no history, so poll it on the vehicle day. Start the poller detached (Start-Process), because the Ostrava poller lost its peak to sleep. The 20 Oct poll is whole-region and unfiltered, at the owner's request via 0b.
- **Rules are imported** from ostrava/scripts/lib.py and ostrava-bus/scripts/lib.py, never copied, so the Ostrava bus session 0b's rule changes flow in. See [[havirov-karvina-orlova-coordination]].
- **Karviná circular lines** 511/512/516/518/519 get one branch with a = b. 414 is occasional and not modelled.
- **Coverage rule (owner, 20 Oct):** every afternoon stop must be on a Simutrans line. Hand-set lines (`line_overrides`) cover the 401/406 ring, 514 (520 carried), the Orlová trunk by core points (501 + 501B every 480, 504 every 240 with 503 as its Důl Lazy leg) and long-interval lines for sparse trips (402B/411B/515/515B every 480, 418 every 240, 420 every 160; 513 carried by 514). No daily lines (owner). See [[every-stop-covered-rule]], [[core-points-repeating-interval-rule]]. See [[every-stop-covered-rule]].
- **Pak:** use only the VZ-MHDHavirov/-Karvina/-Orlova objects. Pak session f3 asked for this on 20 Oct, and it bars CZ-ODIS/CZR-ODIS on town lines. Gaps go to `pak_request.md`.
- **Records:** seznam-autobusu line pages are not in date order, so read every page. 2026 has few records, so the window starts 2025-01-01. The prov=1 register misses some running buses (Dekstra 448), so `01d_plates.py` looks plates up.

Related: [[ostrava-bus-vypravenost]], [[never-ship-without-vehicles]], [[size-from-suggested-pattern]], [[model-line-at-its-peak]].

- **Live assignment:** buses swap lines all afternoon (Havířov ring 401/406/413/403/417/402, Karviná circulars), so each bus fills one Simutrans line it was seen on, by augmenting-path matching (04_roster step 4). A hand-set line takes a bus whose trip runs along its route (both ends on it).
