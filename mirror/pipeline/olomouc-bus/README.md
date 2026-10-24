# Olomouc city buses (DPMO): peak fleet pipeline

Output: `Olomouc Bus Peak Fleet.html` in the project root (published at https://claude.ai/artifact/MJz5Q7xYehTCPKhpBDfLHG). Built by session simutrans-timetable-a2 on 29 Sep 2026.
Shared rules: `../README.md`. The Olomouc tram sheet is `../olomouc` (maintained by another session; **this folder never writes to it**,
it only reads its stored GTFS).

```
cd pipeline/olomouc-bus/scripts
python run.py --state 2026-09-29            # rebuild from stored raw data (02 -> 05)
python run.py --state 2026-09-29 --fetch    # first fetch what is missing (day pages, histories, register, car pages)
python 01_fetch.py --state <s> --overviews 2026-09-01 2026-09-30   # day overviews, to choose a vehicle day
python propose.py --state <s> --groups 11 12 16                    # leg chaining, a helper for the state's simutrans_lines
```

Python 3, standard library only. `scripts/common.py` holds self-contained copies of the shared helpers (fit rule, cycle and
circuit need, mark_spares, seznam-autobusu parsers); its docstring names the files they come from.

## Scope

All DPMO bus lines with afternoon-peak service on Tue 29 Sep 2026: 11–22, 25–28, 31 (17 lines, 18 Simutrans lines).
Left out (no departure 16:00–16:59): 10 (last 15:55), 24 (last 15:20), 29 (morning only), 42 (last 15:44), night lines 50–52.
**No subcontractor** runs an Olomouc city line: the GTFS has one agency (DPMO), and every car in the line histories since
1 Jan 2025 is a DPMO bus.

## Sources

| What | URL | Stored in |
|---|---|---|
| Timetable | `https://www.dpmo.cz/doc/dpmo-olomouc-cz.zip` (DPMO GTFS, version 17 Sep 2026, valid to 12 Dec 2026). Downloaded again on 29 Sep: byte-identical, so the tram pipeline's copy is read by path. | `../olomouc/data/raw/gtfs/2026-09-17/gtfs.zip` (`common.gtfs_path`; a copy in `data/raw/gtfs/<date>/` here would win) |
| Day overviews (coverage) | `https://seznam-autobusu.cz/vypravenost/mhd-ol?datum=D` | `data/raw/vypravenost/overview/<date>.html` (weekdays 1–29 Sep) |
| Records per line, vehicle day | `.../vypravenost/mhd-ol/vypis?datum=D&linka=L` | `data/raw/vypravenost/2026-09-29/<line>.html` |
| Line histories | `.../vypis?strana=N&linka=L&since=2025-01-01` (all pages) | `data/raw/vypravenost/history/2025-01-01/<line>_p<N>.html` |
| Fleet register | `https://seznam-autobusu.cz/seznam?page=N&iddopravce=134&trakce=autobus&prov=1&vcetneSluzebnich=1` (+ `trakce=elektrobus`, empty) | `data/raw/register/2026-09-29/` |
| Cars missing from the register listing | `https://seznam-autobusu.cz/vuz/<id>`: 501 (SOR NS 12 electric, in service) and 625 (Urbino 12 III, laid up long-term) | `data/raw/car/<id>.html` |
| Pak objects | local checkout `C:/Users/vojte/Developer/simutrans-custom-czech-pak128/build/VZ-DPOlomouc-bus` (main b84c15c; DPMO buses from commit 0c2cc6a), read only | `assets/pak_objects.json` (snapshot, refreshed by 04 when the checkout is there) |

Fetching: plain browser User-Agent, ~1.2 s between requests.

## Steps

1. `01_fetch.py` downloads raw data (see its docstring).
2. `02_parse.py`: register + car pages → `vehicles_<date>.json`; day records; day overview car list; coverage table; histories.
3. `03_timetable.py`: network table, schedule fit per stop entry (one rate per Simutrans line), need per Simutrans line.
4. `04_fleet.py`: logged buses, logged surplus ("not needed"), designed buses, free history cars ("not needed"), pak objects;
   writes `fleet.json`, `pak_request.json` and `../pak_request.md` (for the pak session; the user sends it).
5. `05_render.py`: the HTML (Brno bus page style copied into `assets/`; sticky bar with lines, depot, sections and `#q` search).

## Decisions (state 2026-09-29)

- **Vehicle day: Tue 29 Sep 2026**, the network day itself. DPMO bus records are thin: Fri 25 Sep has none, Fri 18 Sep (the tram
  sheet's day) has none; the whole of September has 1–10 bus records a day except 29 Sep (29 buses on 15 of the 17 peak lines,
  fetched 29 Sep ~19:40). One real day. **Records for 29 Sep may still grow:** re-fetch (`01_fetch.py --day --refresh`) and re-run.
- **Records carry no kurz, no time and no note** for buses, so every logged bus counts for its line. Line 11 has two Simutrans lines;
  its logged bus goes to 11R (a choice).
- **Logged surplus** (user rule, 29 Sep): 12 (6 logged, need 4) and 14 (4, need 3) → `mark_spares`: one of each type kept first,
  type ties broken by the line's 2026 roster (so on 14 the electric 501 stays and the Urbino 12 II 615 goes); with no kurz numbers,
  buses listed later on the record page are dropped first.
- **Designed buses** (user rules of 29 Sep): 21 buses on 11R, 11L, 13, 15, 16, 17, 19, 20, 21, 25, all with real car numbers from
  the line's weekday history (2026 records first, then 2025), in service, not in the 29 Sep day overview, used once. Roster =
  logged types + types with ≥ 2 weekday records on the line in 2026 (a single record is a one-off substitute; e.g. the one
  Urbino 12 III on 16). Picks cover lacking roster types first, then by recency. Lines served largest need first.
  Free history cars left over are listed once, dimmed, as "not needed", on the Simutrans line where they last ran (26 buses).
- **Garage runs:** Ladova and Na Střelnici (by the Dolní Hejčínská garage) are depot stops; trips to or from them are left out.
- **Aliases** (`alias`): 12 and 19 Průmyslová → Holice (two stops further); 14 Čistička → Ahold, Civilní obrana → Panelárna;
  25 Kaufland → Hlavní nádraží (next door); 28 Tržnice, plocha → Tržnice.
- **Line shapes:** 11 split into 11R (Radíkov) and 11L (Lošov, Svolinského): buses switch between ends, Also at can't change
  the route. 16 is one circuit Tabulový vrch – Nové Sady – Centrum Haná, Nové Sady a through stop (the feed splits trips there).
  14: Panelárna – Ahold, with Ahold → Hlavní nádraží merged into the Ahold row; its Hlavní nádraží → Panelárna short trips are not
  modelled. 21: Tabulový vrch trips merged into the rows, rate forced to 2/h, Aquapark set every 30 (override: the 16:51 runs to
  the garage). 25: Hlavní nádraží – Nový Dvůr, short trips not modelled. 27: circular, every 45. 31: Hlavní nádraží – Sigma,
  Týneček trips not modelled.
- **Need** = circuit need (3 min layover or the terminus's own shorter turnaround; skip round trips waiting over max(30, interval)),
  raised per real line to the most buses on the road at once 16:00–16:59 (12: 3 → 4, 14: 1 → 3, 20: 4 → 5, 25: 1 → 2). Total 47.
- **Every turning point −1 min**, through stops real minute (shared bus rule of 29 Sep).
- **Pak:** every counted bus has an installed VZ-DPOlomouc-bus object (Urbino 12 II/III share Urbino_12; 616–618 lime green have
  their own object). Only 615 (plain white Urbino 12 II) has none; it is "not needed" now, so it is listed as optional in
  `pak_request.md`. Advert wraps → normal DPMO livery.
- **Depot:** one garage, Dolní Hejčínská (register code DH).

## How to update

1. New GTFS: download into `data/raw/gtfs/<version date>/gtfs.zip` (or rely on `../olomouc`), set `gtfs.raw` / `service_date` in a
   copied state, run `propose.py` on changed lines and review `simutrans_lines`, `alias`, `fit.overrides`, `not_peak`.
2. New vehicles: `01_fetch.py --overviews <from> <to>`, pick the weekday with the most bus records (prefer the last one before
   the network date), set `vehicle_date`, then `run.py --fetch` (add `--refresh` to 01_fetch for pages already stored).
3. `python run.py --state <new>`; check shortfalls, designed picks and `pak_request.md`; send new requests to the pak session via the user.
