# ODIS Opavsko, Vítkovsko, Hlučínsko + MHD Opava (regional and town buses, trolleybuses; vypravenost sheet)

Output: `ODIS Opavsko Vitkovsko Hlucinsko.html` in the project root, published at the URL in `config.json` → `artifact_url` (republish to the same URL). Built on 21 Oct 2026 after the owner asked for the next ODIS sheets ("Yes, do those next sheets") and then: "Do include trolleybuses - consider a different method but do include them".

This folder holds only the sheet's config, data and authoring scripts. The pipeline scripts are the shared ones in `../odis-regional-hko/scripts/`, run with `--base odis-regional-opavsko`. The method is `../bus-schedule-method.md` (v3); the Opava town network (buses and trolleybuses) takes the same method as a small town.

## Scope

| Section | Licences | Operator | Fleet | Pak |
|---|---|---|---|---|
| Opavsko | 902xxx | Z-Group bus, pr. Opava | 22- | VZ-ODIS-bus |
| Vítkovsko | 903xxx | Z-Group bus, pr. Opava | 23- | VZ-ODIS-bus |
| Hlučínsko | 904xxx | Transdev Slezsko pr. Ostrava (some 24- buses registered under Transdev Morava) | 24- | VZ-ODIS-bus |
| MHD Opava, trolleybuses | 905201–905204 (`mhd-opava-trol`, prefix 90520) | Městský dopravní podnik Opava | 3xx | VZ-DPOpava-trolleybus |
| MHD Opava, buses | 905xxx | MDPO | 1xx, 40x | VZ-DPOpava-bus |

- 70 ODIS numbers: 59 modelled as 73 Simutrans lines, 125 vehicles (115 seen on the 20 Oct live map, 10 designed).
- Not modelled (`config.unmodelled`): 214, 256, 275 (sparse / shift, stops on other lines), 283 (two trips), 228 and 229 (night lines).
- Lines shared with other sheets (the sheet with most trips models them): 615, 620, 691, 692, 693 are on the Novojičínsko/Bílovecko sheet; this sheet models 260 and 920 (also Bruntálsko/Rýmařovsko licences), 261, 263, 270, 285, 678 (also Novojičínsko/Bílovecko licences) and 555 (904555; the HKO sheet lists it).

## Sources and what is special here

- **Trolleybuses:** 905201–905204 are not in the bus JDF. `jdf.extra_zips` adds CIS JŘ's city-transport export (`data/raw/2026-10-20/JDF_mestske.zip`, https://portal.cisjr.cz/pub/draha/mestske/JDF.zip, downloaded 21 Oct 2026); the shared `02_timetable.py` reads it with the same version rule and records `traction` (T).
- **Fleet:** `config.fleet.carriers` = Z-Group bus (seznam-autobusu 240), Transdev Slezsko (28), MDPO (338, incl. trolleybuses) and Transdev Morava (7546, for Hlučínsko's 24- buses) → `01c_fleet.py` → `data/derived/fleet.json`. MDPO sends `MDPO<number>` instead of a plate to the live map: `live_plate` maps it.
- **Looked-up plates** (`plates.json`, `01b_plates.py`): `authoring/fix_plates.py` rewrote their paints from all current layers (the shared parser keeps only the last layer: "logo dopravy MSK" instead of "bílá & červené logo Transdev & logo dopravy MSK").
- **Line 204:** MDPO notice (https://www.mdpo.cz/pro-cestujici/aktuality-doprava/omezeni-provozu-mhd-na-ul-vrchni-v-opave): Vrchní street repairs, one-way 12–20 Oct, full closure 21–23 Oct; on 20 Oct 204 ran with replacement buses (trips 40xx, Citelis 150–157). Short works → 204 is modelled as the regular trolleybus line. Its trolleybuses are designed by `authoring/fill_designed.py` (config `fill_designed`): MDPO trolleybuses not in service 15:30–17:30. The shared roster cannot design them (it only takes vehicles that ran the area's lines that day, or fleet numbers with an `NN-` prefix).
- **Overhead wire (22 Oct 2026):** `authoring/offwire.py` checks each trolleybus route against the OSM wire, the same test as `../praha-trolleybus/scripts/03b_offwire.py` (10 m samples, 25 m tolerance, a section is off-wire under a third), with the OSM route relations as the path because the JDF has no shapes. Raw data in `data/raw/osm/2026-10-22/` (Overpass, `Accept: application/json`; overpass-api.de often answers 502, maps.mail.ru's mirror worked): `trolley_wire.json` = `way["trolley_wire"="yes"](49.88,17.78,50.00,18.02); out geom tags;`, `trolleybus_routes.json` = `relation["route"="trolleybus"](49.90,17.83,49.98,17.98); out geom;`, `stops.json` = bus_stop / platform / stop_position nodes in the same box, `out body;`. Result (`data/derived/offwire.json`, a table on each trolleybus card): 201–203 under the wire all the way; 204 off it Ratibořská – Vrchní – U Cukrovaru – Pekařská – Divadlo (2.0 km without wire) and Kylešovice, Bílovecká – Hlavní – škola (0.6 km in a straight line between the stops, about 1 km by the JDF's whole-km distances). Both 204 relations are `complete=no` and stop at Bílovecká: the script adds a missing end from the line's timetable stops when every OSM platform of those stops is over 60 m from the wire (here: none within 100 m). Cross-check: Wikipedia (Trolejbusová doprava v Opavě) marks škola, Hlavní, Vrchní, U Cukrovaru and Pekařská as partial-trolleybus stops, and 202's Malé Hoštice trip (once a day, not modelled).
- **Auxiliary drive:** the register's vehicle pages (`data/raw/2026-10-22/vuz/<number>_<id>.html`, seznam-autobusu.cz/vuz/<id>, fetched with the shared browser headers) give "alternativní pohon": baterie on 32 Tr 314–323, dieselagregát on 26 Tr 305–306, nothing on the rest. `authoring/alt_drive.py` writes `alt` onto fleet.json and the roster (the page shows "+ battery" / "+ diesel generator" after the type), and `fill_designed` takes only those for 204 (`alt`, battery first). On 20 Oct 317, 318, 320, 321, 322 and 316 ran 202/203 in the window, so 204 has 315, 314, 319, 323 (battery) and 305 (diesel generator).
- **Off-wire objects (22 Oct, fleet desk, pak main 684fc09):** `VZ-DPOpava-32Tr-mdpobilocervena-32Tr_battery` (battery) for 314–323 and `VZ-DPOpava-26Tr-mdpobilocervena-26TrDG` (diesel) for 305–306, chosen by the pak rules '32 Tr battery' / '26 Tr diesel generator' (the shared 06 matches a vehicle's `alt` with its type). 324–328 stay electric (the register gives them no alternative drive; the desk notes the register's attribute isn't always filled in).
- The save's old ODIS lines (800…, incl. an electric-only 204) predate the fork and are being rebuilt by the owner (22 Oct): nothing on this sheet is fitted to them.
- **Pak:** fleet desk answer of 21 Oct (via the parent session): Z-Group white + kraj logo = `bila`; Hlučínsko = red ring `bilacervenykruh` or `transdev`; MDPO = `VZ-DPOpava-bus` / `VZ-DPOpava-trolleybus` (advert wraps in plain livery, final); SOR BNG 10,5 loan = permanent stand-in `VZ-MHDHavirov-SOR_BNG_10_5-havirovmodra`. The desk promised `VZ-ODIS-SOR_CNG_12-bilacervenykruh` (not needed on this roster after the paint fix).

## Decisions (21 Oct 2026)

- **Network state:** short diversions → regular route (`regular_not_diversion`): 241, 243, 262 (Psychiatrická léčebna, to 23 Nov), 253 (Služovice, obecní úřad, to 31 Oct), 256, 275, 284 (Dolní Benešov, Zábřeh, Mexiko, 16–21 Oct). Diversions to the end of the timetable year run as they are: 234, 242, 261 (Březová, střed) and 263, 264.
- **Variants** (each covers stops no other line serves): 236 Podlesí, 237 Dvorce, 241 Lipina, 245 zámek, 249 Tábor, 250 Krnov / Holasovice, 253 Vrbka, 260 Heřmanice, 262 Skřipov, 285 Dobroslavice, 293 ŽD, 920 Rýmařov / Opava. One-trip deviations are taken with `stops_via` (216 OPAVIA, 217 Otice, 232 Hvězdová, 238 Loučky, 241 Zálužné, 252 Albertovec, 261 Hladké Životice / Gručovice, 262 Slatina, 267 Jezdkovice, 678 Bravantice Lidl). `terminus_alias` joins Opava, Jaktař škola (town JDF) and Opava, Jaktař, škola (regional).
- **Hand-set after review:** 204 (three slots :00/:24/:36), 217 (hourly :04/:25, rt 20), 247 (15:00/17:00), 248 (hourly :53/:45), 261 (every 120, 14:22/14:35), 920 (every 120 Šumperk / Rýmařov alternating at :17, Opava variant 13:24/15:02).
- **Owner checks** on the page: 204 as trolleybus (with auxiliary-drive trolleybuses) vs as it ran; 217 Divadlo trips; regular routes of 241/243/262; the 920 split.

## Authoring and review (`authoring/`)

- `opa_spec.py` → `config.lines` (+ `opa_notes.py`); `opa_config.py` → everything else (pak rules, texts, areas, network state, owner checks, reasons, area_home, fill_designed, artifact_url). Both idempotent.
- `ends.py`, `dump.py`, `review.py`, `view.py`, `suggest.py`, `divcmp.py`: review tools pointed at this folder.

## How to rebuild

From `../odis-regional-hko/scripts`:
1. `python -X utf8 run.py --base odis-regional-opavsko`
2. (automatic: `run.py` runs `config.post_roster` after 04_roster: `authoring/offwire.py` (wire check), `authoring/alt_drive.py` (battery / diesel marks), `authoring/fill_designed.py` (204's trolleybuses). For a new wire state, fetch the three Overpass files into a new `data/raw/osm/<date>/` and pass `--osm <date>` or change the default.)
3. `python -X utf8 06_render.py --base odis-regional-opavsko`
4. Republish to `artifact_url`.

After a new 01b plate lookup, run `authoring/fix_plates.py` once before step 1's 04/06.
