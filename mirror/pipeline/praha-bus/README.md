# Praha (city buses, PID 100–299): pipeline

Output: `Prague Bus Lines Check.html` in the project root, published at https://claude.ai/artifact/BvCHHf2Wb56SsjMuQgA9ZF. Built by session simutrans-timetable-5a on 29 Sep 2026. Shared rules: `../README.md`.

The user asked for three things. First, every Prague city bus line in the save game (numbered 100100–100299), with its buses and stops, checked against the current PID timetable, filterable to the lines to fix: no vehicles, or stops that don't match. Second, all PID bus lines, not only the broken ones. Third, the same line cards as the tram and trolleybus sheets, with other operators' lines treated exactly like DPP's. Trolleybus 275 is on the trolleybus sheet and the ferries are on the tram sheet, so this sheet is buses only.

```
python scripts/run.py --state 2026-09-29            # rebuild from stored raw data (also refreshes pak_objects.json from the pak checkout)
python scripts/run.py --state <new> --fetch         # download missing timetable, registers and deployment records first
```

## Sources

| What | Where | Stored in |
|---|---|---|
| Game lines | Export from the save-game session (simutrans-122-0-58): every line named 100100–100299 with its buses, entries, halts and waypoints | `data/raw/game/<date>/lines.json` |
| Timetable | `https://data.pid.cz/PID_GTFS.zip`. Lines come from `route_sub_agencies.txt` → `route_licence_number` 100100–100299 with route_type 3 | `data/raw/gtfs/<export date>/gtfs.zip` |
| Deployment records per line and day | `https://seznam-autobusu.cz/vypravenost/pid/vypis?datum=YYYY-MM-DD&linka=N` (car ids in `/vuz/<id>/vypravenost` links) | `data/raw/vypravenost/<date>/<line>.html` |
| Fleet registers (in-service buses, 100 a page) | `https://seznam-autobusu.cz/seznam?iddopravce=<id>&trakce=autobus&prov=1&vcetneSluzebnich=1&page=N`: DPP 106, Arriva City 89, Stenbus 77, About Me 209, ČSAD Střední Čechy 398, Martin Uher 64, ČSAD Polkost 459, Vega Tour 1224, Arriva Střední Čechy 1329, Umbrella City Lines 11174, ČSAD Benešov 27 | `data/raw/register/<date>/dpp_bus_N.html`, `op_<slug>_N.html` |
| Single cars missing from the lists | `https://seznam-autobusu.cz/vuz/<id>` (Aranea cars, new DPP electric buses) | `data/raw/register/<date>/vuz_<id>.html` |
| Pak objects | pak checkout `C:\Users\vojte\Developer\simutrans-custom-czech-pak128\build\VZ-DPPraha-bus`, `VZ-Praha-bus`, `VZ-Praha-water` | `assets/pak_objects.json` (with the commit) |

seznam-autobusu.cz returns 403 to plain curl, so use `common.fetch` (full browser headers) and keep 2 s between requests. Garage codes in the register: Klí Klíčov, Kač Kačerov, Řep Řepy, Hos Hostivař, Vrš Vršovice, Stře Střešovice, Mal Malešice (Arriva City; the register's own count "Praha-Malešice"), BnL Brandýs nad Labem, Kla Kladno. Stenbus's "PID" is a division, not a garage, so it stays blank. The date-range search on the records site is a POST form that keeps its state in the session; GET parameters for it return 403, so the pipeline asks per day.

## Steps (scripts/)

| Script | Does |
|---|---|
| `00_pak_objects.py` | Lists the object names in the Prague bus and ferry packages of the pak checkout into `assets/pak_objects.json`. |
| `01_fetch_sources.py` | Fetches the GTFS and the registers. With `--cars`, also the single car pages for record ids the lists lack. |
| `01_fetch_records.py` | Fetches deployment records for every line on `vehicle_date`. It also fetches `extra_days_non_dpp` for lines not run by DPP (for the pak session) and for lines with fewer courses logged than they need. |
| `02_gtfs_lines.py` | Per line: stop patterns, the main pattern per direction, headway, runtime, the Simutrans schedule (`runfit`, core 16:00–17:00, all termini −1 min) and the buses needed. |
| `02_register.py` | Registers and car pages → `data/derived/vehicles_<date>.json`, keyed by the register's car id. |
| `03_compare.py` | Game lines against PID: stops missing, extra, in place of another, order, and misspelt names. |
| `04_courses.py` | Courses → vehicles with livery and pak object. Fills in courses from other days, then designs any still missing. |
| `05_render.py` | The page. |
| `06_pak_request.py` | What the VZ pak session needs, in `data/derived/<state>/pak_request.json`. |
| `07_halt_renames.py` | Proposed game halt renames (misspellings of the PID name), in the save-game session's TSV format. Nothing is sent. |

## Decisions (state 2026-09-29)

- **Days:**
  - The timetable is PID's export of 29 Sep, service date Wed 30 Sep.
  - Vehicles are from Fri 25 Sep. Records from 21–24 and 29 Sep fill in lines and courses nobody logged on the 25th; the card marks them "logged <day> Sep".
  - The game export is autosave04 of 29 Sep, 17:22.
- **Buses needed:**
  - The need is the larger of two counts.
    - `cycle_need`: the main terminus pair, with a 3-min layover.
    - Buses on the road: every trip of every pattern holds a bus from departure to arrival plus the terminus layover, taking the peak count in 16:00–16:59. The layover is min(3 min, the shortest timetabled turnaround at that terminus in 15:00–18:00), as in `cycle_need`; a flat 3 min overcounted lines that turn in 0–2 min (from the Ostrava bus session, 29 Sep: total 805 → 796).
  - The first count alone misses branches and short workings. Line 191 needs 6 by round trip but 15 on the road; 139 needs 8 against 16. These lines are listed in the card's need text.
  - Where more courses are logged than needed, all are shown. The records have no times, so courses that run only in the morning peak or on school trips can't be told apart.
- **Designed buses:** courses still missing after the other days are "designed, not recorded", always with a real car. User, 29 Sep: real car numbers, and the line's whole roster.
  - Other-day fill-ins, and every designed car, must be active in the register. They must also not be out anywhere in PID on the vehicle date; `data/raw/vypravenost/<date>/overview.html` (the seznam-autobusu.cz day overview) is the check.
  - Designed cars come from the line's own history, `vypis?linka=L&since=2026-09-01`, all pages, working days preferred.
  - A line with no September record falls back to the latest 3 pages since 2025-01-01 (`history_fallback_*` in the state).
  - The picks first cover every bus type in the line's history that the logged buses lack, so each roster type is represented. They then take the newest first.
  - The free history cars left over are listed on the card, dimmed, as "not needed". They are not counted.
  - When the history has too few free cars, free active buses of the line's own types come next, then the operator's usual city-line types, then any city-sized type. The garages of the line's cars go first. Line 226 needed the last step.
  - Result on 29 Sep: 18 designed from history, 27 from the operator's fleet, 33 "not needed". Eight lines have no record at all since 2025: 186, 203, 211, 220, 226, 235, 243, 248.
- **Logged surplus (user, 29 Sep, confirmed via the Brno session):** where more courses are logged than a line needs, exactly the need stays counted. One of every type among the line's buses is kept first (most frequent type first), then the lowest course numbers. The rest are marked "not needed", dimmed at the bottom of the card, and left out of the counts, garages and pak totals. On 29 Sep that is 213 buses, so 797 are counted. This replaces the earlier "keep the operator's slack" on this sheet.
- **Game check:**
  - A game halt matches a PID stop by any of its " / " names, ignoring "Praha," and the stand letter. Abbreviations and misspellings match fuzzily (similarity ≥ 0.85) and are listed as names to fix, without counting as a difference.
  - `halt_aliases` in the state covers names PID abbreviates: VÚ Běchovice.
  - Layover stands (a name containing "odstav") are skipped.
  - The round trip is split at the PID termini and each half is compared with the best PID pattern of that direction. Circular lines are compared whole.
  - Terminus hand-over is allowed: trips end at Letiště and start at Terminál 1.
  - "To fix" means any of: no vehicles, stops that differ, a line not in PID, or a PID line with peak trips and no game line.
- **Liveries** come from the register's current paint:
  - schéma PID šedá → `pidsedocervena`
  - schéma PID červeno-bílo-modrá → `pidcervenomodrobila`
  - městské schéma červeno-bílá → `dppcervenobila` for DPP, `mestskacervenobila` for other operators
  - Veolia → `veoliacervenoseda`
  - bílá → `bila`
  - DPP červená (coach red with the gold Praha skyline, Tourismo RHD 8002) → `dppcervena`.
- CVR Fashion Arena → `fashionarena`: the one advert wrap with its own objects (Vega Tour 8420 and 8421 on line 238; user, via the pak session, 29 Sep). Stenbus 1700 turquoise with a yellow stripe → `tyrkysovozluta`.
- Advert wraps (CVR) and liveries the pak has no slug for get no object of their own; this is the pak session's rule. They take the most common normal livery of the same operator, type and year. Failing that, `pidsedocervena` for cars from 2020 on, else the operator's older scheme.
- **Pak objects:** named by the VZ pak session's scheme (29 Sep 2026, revised the same day).
  - DPP cars: `VZ-DPPraha-<Type>-<livery>-<id>` in VZ-DPPraha-bus.
  - Every other operator: `VZ-Praha-<Type>-<livery>-<id>` in one shared package, VZ-Praha-bus. The operator is not part of the name, and operators share an object per type and livery.
  - Articulated buses are `-A` + `-B`.
  - Type tokens reuse the DPP ones for the same model (`assets/pak_requested.json`). The id differs only for the DPP SOR objects: NB_12, NB_18, BN_12.
  - A name missing from `pak_objects.json` is shown as "requested". Stand-ins from DPP or other cities are not used (user, 29 Sep).
- **Vehicle cell:** number · garage (other operators: operator · garage) / full type · length / pak core. The livery is added where the type has more than one.

## Hand-set schedule rows (method check 25 Oct 2026)

`schedule_overrides` in the state (`02_gtfs_lines.py` applies it, `05_render.py` shows it) replaces a line's terminus rows with hand-set ones: `rows` = list of `{o, d, every, real, why}` with optional `extra` (peak trips left out of the model, HH:MM) and `approx` (no exact run shown). The script works out each row's exact run and its largest deviation in 15:00–17:59 from the trips. Write-up: `../praha/method-check-2026-10-25.md`.

- Different rates at the two ends: 107 (every 4 both ends), 110 (every 15), 122 (hourly), 143 and 157 (every 15 with 2 slots), 189 (every 6), 211 (3 an hour), 232 (every 30; the 5 peak extras have no trip back).
- More slots than departures: 176 (every 15 with 2 slots, not every 60 with 7), 187 (every 90 with 8 slots, the timetable's own 90-min repeat), 207 (every 6).
- The card's two rows were the ends of two different routes: 102 (long line and short working interworked: one circuit line), 103, 111, 139, 226 (line plus its short working), 191 (three lines); all their rows are given.
- Branches with ≥ 3 peak trips get their own rows (user, 28 Oct 2026: "The Prague buses 109 does not have VU Bechovice branch. Is it reasonable?" → "do include - and also for the other lines"): 109, 113, 120, 138, 146, 160, 174, 177, 186, 197 and 221 carry their main rows unchanged plus a row pair per branch, the values proposed in the 25 Oct write-up, interleaved as the timetable runs them. 177's Chodov – Volha is a two-bus shuttle (the trip numbers chain); the save runs it as an extension of 100177, so splitting it off is the owner's choice. 174's Luka short working has no game line. Those rows are grouped into Simutrans lines (next point).
- Each Simutrans line on its own (owner, 28 Oct 2026: "Is it truly one line as you describe? Or are those two independent lines? Look at Ostrava, that shows it."; 30 Oct: "is 109 two lines or one? I am still unsure. In Ostrava, that was so clear." and "Never change lines 100-108"). `scripts/simlines.py` groups a branch card's rows (state `simlines.auto`: 110, 109, 111, 113, 120, 138, 139, 146, 160, 174, 177, 186, 191, 197, 221, 226) into Simutrans lines with the Ostrava bus lib, read-only: separate branch lines, or circuits where they save at least 1 bus. Each line is sized from its own schedule, and the card's need is their sum. The card says up front how many Simutrans lines there are, which game line each one is typed into (a game line two circuits share, 113's 100113S, is named as not needed), and their buses. Each line's rows sit under its own heading, and the buses are split over the lines in course order. `simlines.game_label` overrides the game-line text (177B: the save runs Volha as an extension of 100177). 102 and 103 are not split (`simlines.circuit` stays empty): cards 100–108 stay as published on 28 Oct. `lib.circuitize` can give two jobs the same return slot (110: Čakovice :00 and :15 both back at :35). simlines.py moves a slot claimed twice to the row's next free slot, and falls back to separate lines if the slots still don't match the rows. The waits in a line's heading are listed origin first; dict order had varied from run to run.
- 110 Třeboradický hřbitov (owner, 30 Oct 2026: "The 110 line does not have a branch to Třebovice. Either model it as a real life or for it to use 1 vehicle"): the :30 Čakovice trip runs on past Obchodní centrum Čakovice about hourly from 13:00 to 19:00 (6 out, 5 back), so it is a regular afternoon branch (20 Oct rule). The 25 Oct check had counted only 15:00–17:59. Rows every 60: Čakovice out :00, :15, :45 and back :05, :35, :50; Třeboradice out :30 and back :12. simlines.py makes 110A (Čakovice :00/:15, 2 buses, 100110) and 110B (a circuit of Třeboradice :30/:12 plus Čakovice :45/:05, 2 buses, 100110T extended), 4 buses as before. A plain Třeboradice line would need 2 buses on its own: back at Hloubětín :37, it waits for the next :30.
- Not changed, for the owner: the school lines 251–280 (1–4 trips a day) still show an hourly fit.
- The card text now says how the 01:00 origin changes typed values where a row's interval does not divide 60 (116, 131, 187, 218).

## Regional companions (owner, 30 Oct 2026)

"Now could you do the companion PID lines" / "Definitley include those that share buses so we have a full list. Also those that are
"proložené" like 113/333." / "I am 100% sure 301/352 are continuations of 174" / "Pool if they pool in real live" / "Include if they are
interleaved in the real timetiable". State `regional`:

- **through**: every trip of the regional line starts or ends at the minute a city trip ends or starts at the same stop (PID GTFS of
  30 Sep; 0 min, no exception): 174 → 301 and 352 at Luka (28 + 68 trips), 186 → 396 at Vinoř / Nádraží Satalice (35). `02_gtfs_lines`
  joins each pair into one trip, so the card models the through lines (352 Kukulova – Jinočany every 20, 301 Kukulova – Chýnice hourly,
  186B Černý Most – Přezletice hourly). 174's old "174A Luka, a line to build" is gone: those trips are 301 and 352, as the save runs them.
- **pooled**: the city line's courses also run the regional line (vehicle records of 25 Sep: 111 courses 2, 3, 4, 6, 7 → 329; 161
  courses 1, 2, 3, 5, 6 → 312; 229 courses 1–9 and 11 → 364 and 366). Its trips join the city line's card and Simutrans lines.
- **interleaved** (proložené): own buses, a shared stretch where its departures fall in the city line's gaps (real minutes): 113 / 333
  (Kačerov – Písnice, 13 stops), 129 / 318 (Smíchovské nádraží – Baně, 13), 122 / 363 (Opatov – Újezd u Průhonic, 10), 228 / 325
  (Benice – Nádraží Uhříněves, 8; 325 sits half-way between 228's departures), 182 and 209 / 376 and 378 (Kbely – Letňany, 7). Own card
  after the city line, with the shared stretch and the two lines' merged spacing per direction.
- Left out at the owner's choice: 157 / 327, 157 / 331, 215 / 326 and 161 / 355 (one bus on one day). Ruled out: 321 (Letňany – Brandýs),
  331 (Opatov), 302 / 182 (11 stops shared, not coordinated).
- How the set was found: there is no through-running data for these lines. The national JDF export (CIS JŘ, 20 Oct) has PID lines
  but their `Navaznosti.txt` rows are only timed waits and train connections; PID GTFS `block_id` is empty. Through lines: the
  0-minute trip-chain test over every city × regional pair (only 174/301, 174/352 and 186/396 chain at 100 %; the rest, under 45 %, are
  chance coincidences at hubs). Pooled: přejezd notes in the city lines' records. Interleaved: the longest shared run of peak
  patterns touching the regional line's end, ≥ 7 stops, with its departures in the city line's gaps.
- Hand-set rows (real minutes): 111 + 329 Škvorec hourly :04 / :23; 161 at :10/:20 and :06/:16 every 30 with 312 every 30 at :00 / :14;
  229 Královice every 30 :04 / :16, 364 hourly :19 / :41, 366 hourly :49 / :12 (its 15:04 and 16:04 start at Mukařov and leave Doubek at
  :12; terminus alias Mukařov → Doubek); 174 and 186 as above; 318 Jíloviště every 30 at :03 :10 :25 / :06 :21 :29 with Řitka (:48 / :28)
  and Trnová (:18 / :07) hourly; 363 Todice hourly :00 / :12, Čestlice :15 / :56 (back trips irregular, approximate), Chomutovice :30 /
  :12; 333 Oleško every 30 :19 / :23 and Zvole every 30 :04 / :14. 325, 376 and 378 fit by themselves (every 60).
- Game lines: a second export of the save (`data/raw/game/2026-10-30-regional/lines.json`, FORK-CZR-VZ.sve of 30 Oct, from the
  engine session; 500 lines 100300–100960, only the sheet's lines are read). `03_compare` puts a through or pooled line's game line on
  its city card and compares it with that line's own patterns (`via`). A Simutrans line typed into a regional game line is named by it
  (352, 301, 364, 366). `simlines.game_label` sets 186's lines (100186S; 100186 + 100396) and 229's two Doubek lines (by "o → d :mm").
- Vehicles: the interleaved lines' courses come from the day overview of 25 Sep (no per-line page was fetched: seznam-autobusu.cz
  answered 429 all afternoon). Lines with no record (318, 325, 378) get real active buses of the operator's most common type,
  numbered cars only, designed after every city line so no city card's picks move. `bus_types.json` gained lengths only for the
  types these cards use (Setra S 415 LE business, S 515 LE, Citaro C2 GÜ, Crossway LE LINE 12M, SOR ICN 10,5); a Solaris Urbino 12 III
  length had moved 226's designed bus, so it was left out. Five objects were requested from the fleet desk on 30 Oct.
- Cards 100–108 are byte-identical to v11 (owner: "Never change lines 100-108").

## Pak session hand-off

`06_pak_request.py` writes, for the pak session (simutrans-custom-czech-pak128-bd):
- VZ-Praha: every type × livery seen on a city line on any recorded day, with car numbers, operators, the operators' fleet counts, and the cars mapped from wraps.
- VZ-DPPraha: the active DPP fleet types × liveries that have no object. The pak rule is that the whole active DPP fleet is in VZ.

When the pak session reports new objects, run `00_pak_objects.py` (or `run.py`) and the "requested" marks disappear on their own.

## How to update

1. Ask the save-game session for a new export → `data/raw/game/<date>/lines.json`, then set `game_raw`.
   Also ask for the regional lines (100300 and up) → `data/raw/game/<date>-regional/lines.json`, then set `regional.game_raw`.
2. New timetable: set `gtfs.raw` and `gtfs.service_date` (a normal weekday on the feed).
3. New vehicles: set `vehicle_date`, `extra_days_non_dpp` and `register_raw`.
4. Run `python scripts/run.py --state <new> --fetch`.
5. Check the printed counts (courses by source, designed lines, requested objects) and republish to the same artifact URL.
