# Data sources

Every source the pipelines use, with the quirks that cost time. Per-sheet usage is on each sheet's page in the app and in its
pipeline README (`mirror/pipeline/<x>/README.md`). Raw downloads are kept, dated, in the working folder
`pipeline/<x>/data/raw/<kind>/<date>/` — never in this repo.

## Timetables

| Source | Used by | Notes |
|---|---|---|
| **CIS JŘ JDF** — `ftp.cisjr.cz` (`pub/jdf/JDF.zip` bus export ~107 MB; city export `draha/mestske`) | Ostrava tram/trolleybus/bus, Most–Litvínov, Pardubice, Havířov/Karviná/Orlová, all ODIS sheets | Bus lines are in the **bus** export, not the city one; Opava trolleybuses 905201–4 are in the city export. Version choice: latest "valid from" among versions valid on the day, ties → shortest validity. JDF 1.10/1.11 column differences (Zasspoje arr/dep idx 10/11). |
| **CIS JŘ rail (CZPTT XML)** — `ftp.cisjr.cz/draha/celostatni/szdc/<year>/JR<year>.zip` | MD-CR, all local-rail sheets, RegioJet/Leo Express | One XML per train; monthly folders are gzip výluka variants → ignored. Parsed once into `md-cr/data/derived/trains.json` (71 MB, day bitmaps). **No engineering works** in it. JR2027 from 13 Dec 2026. |
| **CIS JŘ NeTEx** — `ftp.cisjr.cz/netex/` | early sheets (Pardubice v1, Most termini) | `NeTEx_DrahyMestske.zip` (trolleybus), `NeTEx_VerejnaLinkovaDoprava.zip` (bus); filter by operator IČO. |
| **IDS JMK GTFS** — `kordis-jmk.cz/gtfs/gtfs.zip` | Brno tram/trolleybus/bus | No kurz numbers in block_id; trams route_type 0, trolleybus **800**, bus 3. Feed splits long workings at timing points (Úzká, Královo Pole…). Tram timetable switched Tue 29 Sep. |
| **PID GTFS** (Prague) | Prague tram/trolleybus/bus | Trolleybus route_type 11. Has shapes (used for wire check). |
| **PMDP GTFS** — `jizdnirady.pmdp.cz/jr/gtfs` | Plzeň tram/trolleybus/bus | Returns the zip directly. No shapes.txt, no blocks; trolleybus route_type 11. |
| **DPMO GTFS** — `dpmo.cz/doc/dpmo-olomouc-cz.zip` | Olomouc tram/bus | — |
| **pid.cz/zmeny/?type=vlaky**, ČD výluka PDFs `cd.cz/jizdni-rad/tratove-jizdni-rady/files/cz-k<KJŘ>-2026vyluka<NN>.pdf` | rail sheets | The only place engineering works show up. Read PDFs with pymupdf word coordinates. |

## Vehicles (who ran what)

| Source | Used by | Notes |
|---|---|---|
| **bmhd.cz** — `vypravenost.php?datum=&linka=`, `/evidence-dpmb/vozovna/{m,p}`, `vozp.php` | Brno | WAF 403 for plain curl: full Chrome UA + Accept + Accept-Language, ~2 s between requests. Kurz → cars with notes (ráno/odpoledne/výměna), no times. Weekday odd kurz = Pisárky, even = Medlánky. |
| **seznam-autobusu.cz** — `/vypravenost/<city>?datum=`, `/vypravenost/odis/vypis?datum=|linka=`, `/seznam?…&page=N`, `/seznam?spz=` | Praha, Plzeň, Olomouc (`mhd-ol`), Ostrava history, Most, Havířov/Karviná/Orlová, ODIS, Pardubice | WAF: full Chrome UA + Accept-Language. Line pages are **not in date order** — read every page. Register ids: DPMO 134, DPmML 399, Transdev Slezsko 28, Transdev Morava 7546, Z-Group 240, MDPO 338. No DPO tram records after 26 Jun 2026. e-buses under `trakce=elektrobus`. prov=1 register misses some running buses → plate lookups. |
| **DPO live API** — `POST https://dashboard.dpo.cz/api/server` body `{"endpoint":"transport/vehicle/list?page=dashboard&withTripId=1&vehicleStates=ride","apiMethod":"GET","data":{},"host":null}` | Ostrava tram/trolleybus/bus | vehicleNumber, routeID, serviceID (= kurz). **No history**: poll on the vehicle day, keep the machine awake. |
| **ODIS live map** — `POST https://mpvnet.cz/Odis/map/mapData` body `{"w":16.7,"s":49.4,"e":18.84,"n":50.45,"zoom":13,"showStops":false,"mapFilterId":null}` | Havířov/Karviná/Orlová, all ODIS regional, Ostrava Hranečník cards | Needs `Content-Type: application/json`, `Origin: https://mpvnet.cz`, `Referer: https://mpvnet.cz/odis/map` (else 400). Decode utf-8-sig. Row `cn` = licence\|line\|trip\|stop\|delay\|…\|start\|final\|1\|PLATE. Trip = JDF spoj number. Plate → seznam-autobusu vid → fleet number. No history; the 20 Oct 13:00–19:30 whole-region poll is in `havirov-karvina-orlova/data/raw/2026-10-20/live/`. |
| **mhd-ostrava.cz**, Wikipedia | Ostrava trolleybus battery sections | JDF doesn't mark battery sections. |
| **Photos** (seznam-autobusu galleries) | Most–Litvínov bus | Destination displays read off 114 photos (`assets/photo_lines.json`) when no records exist. |
| **vagonweb.cz** — `/razeni/vlak.php?zeme=%C4%8CD&kategorie=Os&cislo=…&rok=2026` | rail circuits | `zeme` must be `%C4%8CD` (not `CD`); needs PHPSESSID cookie + referer (`local-rail/vagonweb.py`). Planned type + sighted units per date. |

## Infrastructure

| Source | Used by | Notes |
|---|---|---|
| **OSM Overpass** `trolley_wire=yes` | Prague, Plzeň, Opava trolleybus battery sections (`03b_offwire.py`, `offwire.py`) | Needs `Accept: application/json` (else 406); Plzeň: a plain tool UA works where a browser UA is refused. Main server gave 502s on 22 Oct; the `maps.mail.ru` mirror worked. |
| prazsketramvaje.cz, bmhd.cz track plan, spvd.cz, Wikipedia, OSM | the Termini sheets (12 Sep) | Loop track counts. |
| Most city GIS `mapy.mesto-most.cz/koop/rest/services/mhd/FeatureServer/0` | Most | Returns empty — no allocation data exists for DPmML. |

## Rate limits and etiquette
- Operator sites (dpmp.cz) rate-limit: 429, then refuse connections — fetch sparingly.
- Keep every download as fetched, in a dated raw folder, so a rebuild never needs the network.
