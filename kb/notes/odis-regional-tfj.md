---
name: odis-regional-tfj
description: ODIS sheet Těšínsko/Třinecko/Frýdecko + MHD Č.Těšín/F-M/Třinec (21 Oct 2026) — pipeline/odis-regional-tfj built by the HKO scripts with --base; 127 buses; town paks by rules
metadata:
  node_type: memory
  type: project
  originSessionId: 1098259d-3349-4d59-bd20-53ed11629b4d
  modified: 2026-10-21T18:15:55.946Z
---

"ODIS Tesinsko Trinecko Frydecko.html" (project root, artifact https://claude.ai/artifact/2LecoKwCYb2Lmk1sRDTjrx, v1 21 Oct 2026). Owner's ask: separate sheet for Českotěšínsko, Frýdeckomístecko, Třinecko, Jablunkovsko "with special sections for MHD Cesky Tesin, Frydek-Mistek and Trinec".

- **Areas by licence prefix:** 871 Českotěšínsko, 863 Frýdecko-Místecko, 861 Jablunkovsko–Třinecko (one contract area, Jablunkov branch 74-) — Transdev Slezsko; MHD 875 Český Těšín + 866 Třinec = ARRIVA autobusy (IČO 25945408, Třinec garage), 865 Frýdek-Místek = Transdev. Frýdlantsko (864, 32- buses) added 21 Oct as a fourth area (owner: "do those next sheets"); 340 kept as a shift line for Kunčice station.
- **No scripts of its own:** `odis-regional-hko/scripts/run.py --base odis-regional-tfj`; config is written by `odis-regional-tfj/authoring/tfj_spec.py` (lines + notes from tfj_notes.py) and `tfj_config.py` (pak rules, texts, network state, owner checks, unmodelled reasons). Edit those, rerun them, then the pipeline.
- 383/387 stay on the Ostrava sheet, 365 on the HKO regional sheet, 655 on the Novojičínsko sheet (21 Oct). HKO sheet must be built first (this one excludes its buses).
- ARRIVA plates looked up via `01b_plates.py` (plates.json); TESIN 001/004 are in the register number first ("001 TESIN"): Scania Citywide LF 10,9M 2018, found 22 Oct (no guess left).
- 22 Oct (sheet v5): 980/985's Z-Group licences 883980/883985 read in via `jdf.extra_lics`, Z-Group in `live.carriers`; 985 = in-then-out rounds every 480 + 985B out only (empty return); Z-Group 63-1005, 63-1011, 63-1308 now on this sheet (NJ refilled from spares, v4).
- Town buses → VZ-MHDTrinec/CeskyTesin/FrydekMistek-bus; regional (kraj logo) bus on a town line keeps VZ-ODIS. 3 stand-ins (SOR ICNG 12 demo, white ARRIVA Dekstra, Crossway LE Line 3ČSAD).
- 80 lines → 98 Simutrans lines, 142 buses (138 seen, 4 designed) with Frýdlantsko; 18 listed unmodelled (Hyundai shift lines, sparse, town shift/midday).
- Owner checks put: 731 regular route (Stonava diversion to 30 Nov), 784 back :19 vs real :25 (+1 bus), 302 Tesco as Riviéra–Tesco shuttle, 706 two branch lines.
- Joint shortest-round fix (21 Oct, shared 05_schedule.py): lay at an end = real turn if under 3 min, so slots aren't moved off a 1-min real turn; HKO output unchanged by it.

Related: [[odis-regional-hko]], [[hand-review-schedules-rule]], [[every-stop-covered-rule]], [[regional-vs-local-rules]], [[odis-live-map-source]].
