---
name: pak-fleet-desk
description: "Questions about which VZ pak128 vehicles exist, and requests for missing vehicles or liveries, go to the pak fleet desk session, never to a drawing session"
metadata:
  node_type: memory
  type: reference
  originSessionId: 5d304c5e-1e80-40b2-9839-f53d6456b698
  modified: 2026-10-21T18:33:30.875Z
---

On 21 Oct 2026 the pak session **simutrans-custom-czech-pak128-35** announced itself as the "fleet desk". It answers which VZ vehicles exist on pak main: object names, liveries, paks, years and capacities. It covers 308 bus, 162 rail, 64 tram, 31 trolleybus and 3 water objects.

- **Missing vehicle or livery:** ask the fleet desk. It confirms the object is really missing, promises it, and hands it to a drawing session.
- **Never message a drawing session directly.** No new art starts without the fleet desk's approval. Drawing session pak128-46 confirmed this on 21 Oct. Once an object is installed, the drawing session sends the new object names (name=) and the pak back to the session that asked.
- Session names change between days (an earlier one was pak128-95). If -35 is gone, find the current fleet desk with ListAgents.

- The desk replies to the session that sent the request: when sub-sessions (forks) send inventories, the answers land in the parent's inbox, so relay them (21 Oct ODIS sheets). Send one inventory per sheet: type × paint × area kind × count, with operator and where it runs.

Related: [[ostrava-bus-vypravenost]] (pak objects for the Ostrava sheets), [[odis-regional-tfj]], [[odis-regional-opavsko]].
