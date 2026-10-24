---
name: prague-bus-lines-check
description: "Prague bus sheet (2026-09-29) — all PID 100–299 lines vs save game; pipeline/praha-bus; non-DPP = VZ-Praha objects, never DPP stand-ins; ferries live on the tram sheet"
metadata:
  node_type: memory
  type: project
  originSessionId: e03a85dc-f430-434a-99fb-e6daceff5db2
  modified: 2026-09-29T16:07:28.005Z
---

"Prague Bus Lines Check.html" (project root), artifact https://claude.ai/artifact/BvCHHf2Wb56SsjMuQgA9ZF, built by `pipeline/praha-bus` (README has every decision). It has a game check (every save-game line 100100–100299 vs PID GTFS, filterable to "to fix") plus full line cards for all 163 bus lines.

User rulings made during this build (2026-09-29):
- Include ALL Prague city bus lines, not only broken ones.
- Separate sheets stay single-mode; ferries go on the Prague tram/metro sheet (done: ferry block in pipeline/praha).
- Non-DPP lines must be exactly as good as DPP ones. Never map non-DPP cars to DPP or other-city stand-ins. Liveries matter like tram colours.

Pak naming from the VZ pak session (simutrans-custom-czech-pak128-bd):
- DPP cars: `VZ-DPPraha-<Type>-<livery>-<id>`.
- Every other operator shares one package: `VZ-Praha-<Type>-<livery>-<id>`, with no operator in the name.
- Advert wraps map to the type's normal livery.
- Ferries: `VZ-Praha-water`.
- `assets/pak_objects.json` is read from the pak build, so the "requested" marks clear by themselves.

Non-obvious:
- `cycle_need` on the main terminus pair undercounts lines with branches (191: 6 vs 15 on the road). The need is max(cycle_need, peak buses on road with 3 min layover).
- Fans leave 12 lines unlogged on all six days. Their designed buses now carry real car numbers: from line history since 1 Sep (or since 2025), else free cars of the operator's fleet. See [[designed-vehicles-roster-rule]].
- `07_halt_renames.py` writes a TSV of misspelt game stop names for [[savegame-rename-service]]. It is NOT sent; the user must decide.

Related: [[prague-tram-peak-fleet]], [[prague-trolleybus-peak-fleet]], [[city-pipelines]]
