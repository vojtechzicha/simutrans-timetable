---
name: regiojet-rail-sheet
description: RegioJet rail lines Simutrans sheet (done 2026-09-26) — data source, carrier codes, notation the user wants (L/S hours), depots and waiting spots
metadata:
  type: project
---

**ARCHIVED 10 Oct 2026** (user: "archive all (all done)", trains only): the page moved to `archive/`. It had already been superseded by the MD-CR v4 game lines ([[md-cr-rail-sheet]], also archived).

RegioJet rail sheet done 2026-09-26: regiojet-lines.html in project root, artifact https://claude.ai/artifact/WgToBBtsy9HSNG64rWM3jA.

User wants rail lines grouped by shared path, one variant per distinct path, each with stopping pattern, 1–2 depot visits and waiting spots with frequency + offset in Czech notation "every 2 h at L:07" (L = odd hours, S = even hours).

**How to apply:** rail data = CIS JŘ ftp.cisjr.cz/draha/celostatni/szdc/<year>/JR<year>.zip (one CZPTT XML per train; monthly folders are gzip "zip" výluka variants → ignore per [[simutrans-city-sheet-rules]]). Carrier = ResponsibleRU: 3246 RegioJet, 3752 RegioJet ÚK, 1154 ČD, 3736 Trilex (Länderbahn), 3616 Leo Express. Passenger stop = TrainActivityType 0001/0028/0029/0030. Foreign destination in CZPTTHeader/CZForeign*Location. From 13 Dec 2026 RJ ÚK runs whole U1/U3/U32/U51/U54 — sheet will need a JR2027 refresh.
