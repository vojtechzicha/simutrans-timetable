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

- 70 ODIS numbers: 59 modelled as 73 Simutrans lines, 126 vehicles (116 seen on the 20 Oct live map, 10 designed). Was 125 vehicles before the 25 Oct hand check of 281, 282, 290 and 292.
- After the 25 Oct check of the rest of the sheet (below): 72 Simutrans lines (285 Dobroslavice folded into 285), and the schedule (`05_schedule`) needs 133 buses, 7 more than 126.
- After the 292 split (25 Oct, below): 73 Simutrans lines, still 133 buses; the roster was rebuilt in the working folder (`04_roster` with `keep_roster` = v8), not published.
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
- **Variants** (each covers stops no other line serves): 236 Podlesí, 237 Dvorce, 241 Lipina, 245 zámek, 249 Tábor, 250 Krnov / Holasovice, 253 Vrbka, 260 Heřmanice, 262 Skřipov, 293 ŽD, 920 Rýmařov / Opava (285 Dobroslavice was one until 25 Oct: all its stops are on 285, so it is listed on the 285 card now). One-trip deviations are taken with `stops_via` (216 OPAVIA, 217 Otice, 232 Hvězdová, 238 Loučky, 241 Zálužné, 252 Albertovec, 261 Hladké Životice / Gručovice, 262 Slatina, 267 Jezdkovice, 678 Bravantice Lidl). `terminus_alias` joins Opava, Jaktař škola (town JDF) and Opava, Jaktař, škola (regional).
- **Hand-set after review:** 204 (three slots :00/:24/:36), 217 (hourly :04/:25, rt 20), 247 (15:00/17:00), 248 (hourly :53/:45), 261 (every 120, 14:22/14:35), 920 (every 120 Šumperk / Rýmařov alternating at :17, Opava variant 13:24/15:02).
- **Owner checks** on the page: 204 as trolleybus (with auxiliary-drive trolleybuses) vs as it ran; 217 Divadlo trips; regular routes of 241/243/262; the 920 split. Added 25 Oct (below): 241/252/262 with fewer buses, 215/233/264 with one bus, 248 every 120. The shared 06 writes the number of checks as a word up to seven, so this sheet is at its limit.

## Hlučínsko lines at sad B. Němcové, checked by hand (25 Oct 2026)

The owner asked for 281, 282, 290 and 292 to be checked step by step ("that's the point of you doing it, so you'll not
produce incorrect results"). Their 21 Oct rows were automatic fits and all failed Step 4. The check is in
`method-check-2026-10-25.md`.
- **Outstation lines:** the buses sleep at the far ends (Hať garage, Třebom, Strahovice, Chuchelná, Píšť), so the afternoon
  sends more buses out of Ostrava than come back (19 out, 12 in at sad B. Němcové, 14:00–17:00). Each line is timed both
  ways at its inbound rate; the extra peak departures (buses going home) are off the pattern. v7 had them on B lines with
  empty returns (5 more buses); the owner: "Unless those empty runs add something really needed and specific, don't add them
  just for frequency". They served no stop of their own, so v8 dropped them.
- **290:** every 120 with four slots each way, exact (Ostrava 14:44, 14:59, 15:24, 15:49; Hať 14:47, 15:31, 16:07, 16:37).
- **281:** Třebom :58, timed so the bus passes Kobeřice at :13 (was Třebom :16, 15–20 min off); Ostrava :18 unchanged.
- **282:** every 120 (Píšť :55 is exactly every 2 h; Ostrava :53), model hour set to 16:00 (`anchor`) because its busiest
  stretch was the Hlučín – Závada shuttles.
- **292:** v8 had one line, every 80, Ostrava 14:33 / 15:53 → Chuchelná, back timed at Hlučín :59. Wrong: it read the
  trips at Píšť, Mýto, before the fork, and both its Ostrava slots were Strahovice trips (see "292 split" below).
- Needs 9 → 10. `config.keep_roster` (`data/published/roster_v6.json`, new opt-in step in the shared 04_roster) keeps the
  published buses where they are still seen on their line: 281 24-0004 → 24-0002, 290 + 24-1111, nothing else moves.
  290: the owner chose the four exact slots and 4 buses over every 40 with 3 (25 Oct 2026: "290 uses more buses").

## 292 split by destination (25 Oct 2026)

Owner, after v8: "looking at 292 I see in peak half of the services going to Chuchelná, half going to Strahovice, kaple -
but you model as one line?" Past Bělá the line forks; the v8 row counted every trip passing Píšť, Mýto (`core_to`), so it
"passed" Step 4 with two Strahovice trips (14:33, 15:53) while the Simutrans line ended at Chuchelná, and the plates were
read the wrong way round (the 14:33 and 15:53 buses stay at Strahovice; 24-1007's 15:33 Chuchelná trip is the one that
comes back, via Strahovice at 16:43). Now one line per destination (method Step 5), each every 160, together the inbound
rate (every 80 at Hlučín), 2 buses as before:
- **292** (Chuchelná, železniční stanice): Ostrava 15:33, Chuchelná 14:21, both exact; `notvia` Strahovice, so the
  Strahovice trips via the station don't count for it. Bus 24-1007 (it runs both trips in reality).
- **292 Strahovice:** Ostrava 14:33 exact, via Chuchelná, železniční stanice (`stops_via`, as that trip runs); back from
  Strahovice 15:36, timed at Hlučín 16:19 / 13:39 (`knot_at`, `notvia` the station) for the Píšť trips 15:53 / 13:18,
  within 3 min. Bus 24-0004 (seen on the 14:33).
- Off the pattern by the plates: 14:58 (83-1052 stays at Chuchelná), 15:53 (24-1009 stays at Strahovice), 13:53
  (24-1116 goes on as 293), the Ostrava – Chuchelná – Strahovice – Ostrava rounds (15:33 → 16:43, 17:04 → 18:53).
- Simpler alternative on the card (not an owner check: the sheet is at seven): one line every 80 through both ends.
- Shared-script fixes found on the way (all five regional sheets, typed values unchanged): a leg timed at a knot listed
  its stops only from the knot on (28 legs, e.g. 281 back from Třebom started at Kobeřice); `05_schedule` now takes the
  path from the trips that run the leg from its terminal, and its knot check compares with every trip the leg stands
  for. `04_roster`'s `keep_roster` keeps the published bus with the closest evidence when a line needs fewer buses (292
  keeps 24-1007, not 24-1116).

- **Branch check of every line read at a midpoint** (`../audit/branch-check-2026-10-25.md`): on this sheet **246**'s way
  back now runs via the Jakartovice villages and Dolní Životice, as 17:32 runs (its :12 slot stands for the Dolní Životice
  trips; v8 listed the way back only from Dolní Životice on, and listed from the terminal its commonest path skips Dolní
  Životice); typed values and buses unchanged. 263 (Hlubočec), 281
  (Strahovice, one way) and 246's Hlavnice trip are single or one-way trips whose stops are on other lines.

## The rest of the sheet, checked by hand (25 Oct 2026)

Every leg the regional Step 4 audit (`../audit/audit-regional-2026-10-25.md`) listed as failing was checked by hand with the
same method; the reading and the candidates are in `method-check-2026-10-25.md` ("The rest of the sheet"). All rows are
hand-set now (no `at: 'auto'` on the changed lines).
- **Set exact in the model window** (every leg passes Step 4): 212, 216, 218, 219 every 120 with three or four slots;
  220 hourly with two; 238 every 90; 240, 242 every 120 with two; 245 every 80; 249 every 120; 270 every 80; 293 every 96
  (every 120 would leave Hlučín on 293 ŽD's 13:05); 678 every 144 (every 120 needs 3 buses for the same two departures).
- **Model hour set by hand to 16:00 (`anchor`)**, as 282: 075 (its :02 / :22 extras made 13:40–15:40 the busiest) and 555
  (two Bohumín, Nový Bohumín short trips did). **285** is timed in its own afternoon (`window` 13:00–15:00): its Štítina
  trips end at 15:50.
- **Inbound rate (outstation, owner rule of 25 Oct):** 236 (buses sleep at Budišov), 263 (at Pustá Polom), 284 (its buses
  go on from Štěpánkovice); the extra departures are off the pattern.
- **Variants listed, not folded in:** 242's express pair via Jelenice (Vítkov 14:30, Opava 14:45; `via` Branka u Opavy);
  285 Dobroslavice is no longer a line (all its stops are on 285, and it counted 285's own trips past Dobroslavice).
- **Kept approximate:** 251 and 248 hourly (a narrow window must not halve an hourly line), 254 every 90 (no pattern passes
  both ways), 217 and 920 (their owner checks).
- **Buses:** 215, 233, 264 +1 (exact departures one bus cannot chain), 241 +2, 252 +1, 262 +1, 285 +1 and 285 Dobroslavice
  −1: 126 → 133. The cheaper options are on the owner checks (241/252/262 −4, 215/233/264 −3, 248 −1).

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
