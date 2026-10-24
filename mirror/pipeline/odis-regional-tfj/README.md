# ODIS Těšínsko, Třinecko, Frýdecko (regional + town buses, vypravenost sheet)

Output: `ODIS Tesinsko Trinecko Frydecko.html` in the project root, published at the URL in `config.json` → `artifact_url` (republish to the same URL). Built on 21 Oct 2026, when the owner asked: "Can we now in separate sheet do Českotěšínsko, Frýdeckomístecko (probably the names are slightly different), Třinecko and Jablunkovsko? With special sections for MHD Cesky Tesin, Frydek-Mistek and Trinec?"

This folder holds only the sheet's config and data. The scripts are the shared ones in `../odis-regional-hko/scripts/`, run with `--base odis-regional-tfj`. The method is `../bus-schedule-method.md` (v3), the same as on the Havířovsko/Karvinsko/Orlovsko sheet; the three town networks are small towns and take the same method (as Havířov does).

## Scope

| Section | Licences | Operator | Fleet | Town pak |
|---|---|---|---|---|
| Českotěšínsko | 871xxx | Transdev Slezsko, provozovna Český Těšín | 73- | – |
| Frýdecko-Místecko | 863xxx | Transdev Slezsko, provozovna Frýdek-Místek | 33- | – |
| Frýdlantsko (added 21 Oct, owner: "do those next sheets") | 864xxx | Transdev Slezsko, provozovna Frýdek-Místek | 32- | – |
| Jablunkovsko–Třinecko (one contract area) | 861xxx | Transdev Slezsko, provozovna Jablunkov | 74- | – |
| MHD Český Těšín | 875xxx | ARRIVA autobusy (IČO 25945408), Třinec garage | no prefix | VZ-MHDCeskyTesin-bus |
| MHD Frýdek-Místek | 865xxx | Transdev Slezsko, provozovna Frýdek-Místek | – | VZ-MHDFrydekMistek-bus |
| MHD Třinec | 866xxx | ARRIVA autobusy, Třinec garage | 71- / plates | VZ-MHDTrinec-bus |

- 101 ODIS numbers. 80 are modelled as 98 Simutrans lines, 142 buses (138 seen on the live map, 4 designed). Frýdlantsko adds 10 lines, 12 Simutrans lines, 15 buses.
- Elsewhere: 383 and 387 (Frýdecko licences) are on the Ostrava sheet (section All lines at Hranečník); 365 Havířov – Frýdek-Místek (863365 + 912365) is on the Havířovsko/Karvinsko/Orlovsko regional sheet. 655 Frenštát – Trojanovice (863655 + 883655) is on the Novojičínsko/Bílovecko sheet since 21 Oct (883655 holds 41 of its 45 trips). Their stops count as covered and their buses stay there.
- Not modelled (`config.unmodelled`, with the reason): the Hyundai shift lines 385, 386, 741, 740, 776; the sparse lines 352, 751, 752, 763; the town shift and midday lines 705, 710, 711, 725, 317, 319; 315 (its afternoon trips are the out half of 316's round, see below); 320 and 398 (no Tuesday trips).
- Frýdlantsko: 340 is a shift line every 480 because Ostrava, Kunčice, nádraží Kunčice has no other afternoon line; 343 Podolánky and 345 Hutě are every-480 variants for places only they serve; 348 is hourly from Frýdlant in the afternoon (3 buses, as real), its Bílá – Ostravice evening short trips have no line of their own; 341, 347 run one bus on the real round (341: Frýdlant 16:34 / Janovice 17:00; 347: out :30, back :57).

## Sources

As the HKO sheet: CIS JŘ JDF of 20 Oct 2026 and the ODIS live map poll of Tue 20 Oct 2026 (both stored by the Havířov/Karviná/Orlová pipeline), the Transdev Slezsko register (`fleet.json`). New here:

- **ARRIVA's buses** are not in that register. `01b_plates.py` (on when `config.plate_lookup` is true) looks each unknown plate up on seznam-autobusu.cz and stores `data/raw/2026-10-20/plates.json`. Plates looked up once are kept, found or not (`--refresh` asks again for the ones not found). TESIN 001 and TESIN 004 (vanity plates) are in the register number first, "001 TESIN" / "004 TESIN" (Scania Citywide LF 10,9M, 2018, MHD Český Těšín white-yellow); since 22 Oct the lookup tries that spelling, and the old `plate_guess` is gone.
- **980 and 985's Z-Group trips (22 Oct):** both lines also hold licences of Z-Group's Novojičínsko Východ area (883980, 883985: Ostrava – Frenštát short trips). `jdf.extra_lics` reads them into this sheet's lines, and `live.carriers` includes Z-Group so their buses are seen (63-1005, 63-1011 on 985; 63-1308 on 980, looked up by plate). This sheet comes before Novojičínsko in the bus precedence, so those three buses are here and the Novojičínsko sheet refilled its lines from its own spare buses.
- **pak128**: `config.pak.packages` lists the four installed packages read for objects; `config.pak.rules` picks the object per bus (first match of area kind, type, paint; `~` = stand-in, listed in `pak_request.md`). A regional bus with the kraj logo on a town line keeps its VZ-ODIS-bus object.

## Decisions (21 Oct 2026)

- **Network state:** the diversion timetables that run to 12 Dec (770, 786, 787, 315, 316, 704, 716, 721, 722) are modelled as they run. 731's diversion (28 Aug – 30 Nov, the Stonava mines works, as 582 on the HKO sheet) is short, so `regular_not_diversion` keeps the regular route.
- **Variants without a stop of their own come off** (Step 8): 731's shift trips to Karviná, Důl Darkov and 783's trips via the Hraniční přechod (783 Ski areál serves those stops), and the whole of 740.
- **Shortest-round pairing** (both ends of an auto-fitted two-terminal line): at most a few minutes on frequent lines, a third of the interval on sparse ones, so one bus can work both ends. Since 21 Oct the minimum wait at an end is the real timetable's own turn where that is under 3 min, so a slot is no longer moved off a timetable that turns in 1 min (738 at Svibice; 303 Hodoňovice; 304). Moves are written on the card.
- **Hand-set after review** (`authoring/tfj_spec.py`):
  - 301 every 30 with two slots, :03 and :13, at both ends (four an hour, uneven).
  - 302 Tesco: the trunk trips that run on from Riviéra to Tesco at the shift changes are a Riviéra – Tesco shuttle every 480 (13:41, 14:11, 14:41; back 13:52, 14:22, 14:52), so the every-30 trunk is not doubled.
  - 316: one bus goes out as 315 (via Chlebovice) and back as 316 (via Zelinkovice); the Simutrans line 316 is that round, every 90, using both lines' trips. 316 Riviéra is hourly at the peak (:21 / :12).
  - 773 and 771 Hluchová: every 480 on their afternoon trips (773 timed at Nýdek, náměstí 12:33 with a knot).
  - 782 (Návsí – Radvanov – Jablunkov), 721 Mosty and 358 Steel: manual every 480 / 60 rounds from the real trips.
  - 985 (22 Oct, with the 883985 trips): the Frenštát short trips are an afternoon burst out of Ostrava every 30, 14:33 – 16:03. 985 = the two in-then-out rounds the live map shows (Frenštát 12:47 → Ostrava 14:33 out, 32-1002; Frenštát 14:42 → Ostrava 16:03 out, 63-1011), every 480; 985B = Ostrava 15:03 and 15:33 out only with an empty return (33-1015; 63-1005, which came in on 980 at 14:17), as 543B on the HKO sheet. Both legs `notvia` Rožnov, whose trips are 985 Rožnov's (unchanged).
- **Owner checks** on the page: 731 regular route; 784's back slot :19 (two buses) instead of the real :25 (three); the 302 Tesco shuttle; 706 as two branch lines (as until 15:00) rather than the later combined trip; 985 as the burst (985 + 985B) rather than the old two-way every 90.

## Roster

As the HKO sheet, plus:
- other sheets: the town sheet, the Ostrava cards and the HKO regional sheet's roster (one bus, one sheet; 162 plates);
- `designed_same_area`: a designed bus is first one that ran the same area's lines that day (ARRIVA's town buses have no fleet-number prefix to pick by); then the area fleet by `areas[].near` prefixes.

## Authoring and review tools (`authoring/`)

- `tfj_spec.py` writes `config.lines` (the line specs and notes from `tfj_notes.py`); it keeps the unmodelled reasons. `tfj_config.py` writes everything else (pak rules, texts, areas, network state, owner checks, reasons). Both are idempotent: rerun them after editing, then the pipeline.
- `dump.py [L,...]` and `review.py L,...` print each Simutrans line's slots, joint moves, fits and the afternoon/whole-day real departures, for the hand review.

## How to update

1. A new poll day: the Havířov/Karviná/Orlová poller must run 13:00–19:30 (whole region). Point `snapshot`, `vehicle_day`, labels, `jdf.zip`, `live.dir` at it (in `authoring/tfj_config.py` if you rebuild the config, else in `config.json`).
2. Re-check the diversions (`data/derived/versions.json`) and the network state.
3. From `../odis-regional-hko/scripts`: `python -X utf8 run.py --base odis-regional-tfj`.
4. Review the To check list and each changed line with `authoring/dump.py`; adjust `authoring/tfj_spec.py`, rerun it and the pipeline.
5. Run the HKO sheet first when both change: this sheet excludes its buses.
6. Republish to `artifact_url`.
