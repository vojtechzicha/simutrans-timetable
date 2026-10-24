---
name: ostrava-tram-vypravenost
description: "Ostrava tram per-vehicle PM-peak sheet (done 2026-09-28) — sources, why the roster is designed, DPO live API, Simutrans schedule rule"
metadata:
  node_type: memory
  type: project
  originSessionId: bc38834b-4e71-40d9-9f27-368436ac6fb5
  modified: 2026-09-28T14:59:52.911Z
---

Sheet done 2026-09-28: "Ostrava Tram Vypravenost.html" in project root, artifact https://claude.ai/artifact/4JYPMdmaxEzKhkxg37fd8e. The user's ask: vehicles from Fri 25 Sep 2026 PM peak, network state as of Sun 27 Sep; per line trams + depot list (VP Poruba, VMO Moravská Ostrava).

Friday roster is **designed**, not observed: seznam-autobusu ODIS vypravenost (/vypravenost/odis/vypis?datum= or ?linka=, fed by tram-bus.cz) has no DPO tram records after 26 Jun 2026. Designed from JDF turn counts at 16:00 + ~11.6k weekday records Sep 2025–Jun 2026 + fleet register state (zar/dilny/doco) + DPO live feed.

DPO live API (no history): POST https://dashboard.dpo.cz/api/server with {"endpoint":"transport/vehicle/list?page=dashboard&withTripId=1&vehicleStates=ride","apiMethod":"GET","data":{},"host":null} → vehicleNumber, routeID, serviceID (= kurz). Polling it on a real weekday peak would give an observed roster to replace the designed one.

seznam-autobusu needs full Chrome UA + Accept-Language headers (WAF); /seznam lists paginate with &page=N. Simutrans schedule block follows the fork spec relayed by the Brno session (see [[brno-tram-peak-fleet]], [[simutrans-city-sheet-rules]]).

**Pipeline (2026-09-28):** everything re-runnable lives in pipeline/ostrava/ (README, config.json, scripts/01–06 + run.py, data/raw/<snapshot>, data/derived). Update = follow its README recipe, not the scratchpad. Live poller writes to pipeline/ostrava/data/raw/<date>/live/.

**18 Oct 2026 update:** the schedule table now follows Prague (a "real N" subtitle under Offset/Also at, plus a Fit column). Both ends of each line are matched to the same rate, which fixed 4 and 5; the Headway column comes from the fit. 1 + 2 stay separate under [[shortest-terminal-wait-rule]]; the circuit code waits in `config.circuits_off`. `live_until` = 20260928-1912 pins the published roster, which is unchanged at 95 trams. Republished as artifact version 13.
**18 Oct (later):** no single cars on 4/7/8 now. 9xx courses are left out of the history and pairs are kept. `04b_rebase.py` keeps the published roster (`data/published/roster_2026-09-28.json`) with 5 swaps; artifact version 14.
**20 Oct 2026:** `config.timetable` = JDF snapshot 2026-10-20, day 21 Oct (Don Bosco served again; 10/13 drop Dolní Vítkovice Hlubina). Minutes, needs and trams are unchanged. Version 15.
