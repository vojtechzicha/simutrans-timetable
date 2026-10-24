---
name: odis-live-map-source
description: ODIS live map (mpvnet.cz) gives line, trip and number plate per bus for all ODIS carriers; a4 polls it 20 Oct 13:00–19:30
metadata:
  type: reference
---
ODIS live map: POST https://mpvnet.cz/Odis/map/mapData with body {"w":16.7,"s":49.4,"e":18.84,"n":50.45,"zoom":13,"showStops":false,"mapFilterId":null}.
- Headers: Content-Type application/json, Origin https://mpvnet.cz, Referer https://mpvnet.cz/odis/map. Without them it returns 400.
- Decode as utf-8-sig.
- Each row: cr = carrier and branch; cn = "licence|line|trip|stop|delay|…|start|final|1|PLATE|…". The plate maps to the seznam-autobusu vid and fleet number.

Session a4 polls the whole region every minute, Tue 20 Oct 2026 13:00–19:30, into pipeline/havirov-karvina-orlova/data/raw/2026-10-20/live/. Reading it is allowed.
- It could give observed Transdev buses for the Hranečník ODIS cards: 383, 387, 440–442, 531, 534, 535.
- Those cards' vehicle day is 30 Sep, and a4's own sheet uses 20 Oct, so using it means coordinating with a4 so no bus sits on both sheets.

Related: [[havirov-karvina-orlova-coordination]].

Used on the Ostrava bus sheet's ODIS cards (20 Oct 2026): cn trip number = JDF trip (spoj) number, so a sighting gives the exact trip; compact file pipeline/ostrava-bus/data/raw/2026-10-20/odis_live.json (01e_odis_live.py), plates joined via havirov-karvina-orlova fleet.json vid.

Also used by the ODIS regional sheet ([[odis-regional-hko]], 21 Oct 2026). Its `01_live.py` keeps a compact copy, `live_compact.json`, of every Transdev Slezsko sighting from the whole poll, keyed licence + trip.
