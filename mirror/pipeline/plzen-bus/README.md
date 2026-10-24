# Plzeň buses (PMDP)

Published at https://claude.ai/artifact/LE4trKFDZjkAjpX2EhvJCa (republish to the same URL after a rebuild). Maintained by session simutrans-timetable-a2.

The Plzeň bus sheet. It has no scripts of its own: `scripts/run.py` runs the Plzeň trolleybus pipeline's scripts (`../plzen-trolleybus/scripts`) with `--base` pointing here, in the way the Brno bus pipeline builds on `../brno-trolleybus`. The raw data (PMDP GTFS, seznam-autobusu.cz day overviews, per-line lists, line histories, PMDP register) is stored once in `../plzen-trolleybus/data/raw` and read from there. The shared rules are in `../README.md`; the method, sources and fetch steps are in `../plzen-trolleybus/README.md`.

| State file | Network | Vehicles | Output (project root) |
|---|---|---|---|
| `states/2026-09-29.json` | Tue 29 Sep 2026 (GTFS service day 29 Sep) | Fri 18 Sep 2026 | Plzeň Bus Peak Fleet.html |

```
cd pipeline/plzen-bus/scripts
python run.py --state 2026-09-29
```

This folder holds: `states/` (the bus state), `data/derived/<state>/` (timetable, fleet), `assets/pak_map.json`, `pak_request.md` and this README. Built by session simutrans-timetable-a2 on 29 Sep 2026; not published yet.

## Scope

Every PMDP city bus line with afternoon-peak service (≥ 3 trips in 15:00–18:00 and a 16:xx departure): 20, 21, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 38, 39, 40, 41, 42, 51. Left out:
- 23, 36, 37, 43, 50, 58: no trip in 15:00–18:00; 56 (Vinice – Město Touškov): one each way;
- night lines N1–N6, N11, N12.

**Subcontractors.** The PMDP GTFS has one agency, and every bus logged on 18 Sep resolved to the PMDP register (`04_fleet.py` would show another operator's car with its operator and the `VZ-Plzen-bus` package; `01_fetch.py --operator <id> autobus` fetches that operator's register). None ran a PMDP line in the peak, so there is nothing to request for them.

## Decisions

- **Day and network:** as for the trolleybuses: vehicles Fri 18 Sep 2026 (23–25 and 29 Sep have 0–4 bus records), network Tue 29 Sep 2026.
- **Circuits and branches (from `propose.py --route-type 3`):**
  - **28** alternates between Papírna Bukovec and Bukovec: one line with CAN Husova twice (`turn: 28|CAN Husova`, since both are turning points).
  - **33 + 40** form a loop: 33 goes out by the Lochotín hospital and 40 comes back by Lochotín, and the other way round (8 of 10 and 8 of 11 in the chaining). Two Simutrans lines, one per direction: `33` (33 out, 40 back) and `40` (40 out, 33 back). 40 has no record since 31 Aug: since September its buses are logged as 33 kurzy, so both lines share the 33 kurzy (records "33").
  - **42** has one record ever (Dec 2024), while 26 is logged with 5 weekday kurzy and needs only 2. Both run Bory – Lhota. Inferred and marked "not confirmed" on the sheet: 42 runs on 26 kurzy (records "26"; 42 takes the highest numbers).
  - Branches as their own lines: **26N** (Bory – Nová Ves, hourly), **30P** (Borská pole – Sídliště Košutka, every 30), **41K** (Vinice – Křimice, every 30). Their kurzy are the highest of the record line (a choice).
  - 24 and 25 (both Bory – Bolevec, different routes) stay separate: each has its own kurzy.
  - 32 Škoda VIII. brána → NC Černice (2 trips in 15–18 h) is not a peak trip.
- **Stop types:** every entry is a turning point (−1). No through stops on these lines.
- **Need** = max(cycle, on the road per record line), as on the trolleybus sheet. On 18 Sep: 69 counted, 14 not needed, none short, none designed. The designed-vehicle path (history → real cars, roster types first, leftovers "not needed") was tested on 42 with 26's history and works; it is not needed with the 26 pool.
- **Pak:** no PMDP bus objects exist; seven types are "requested" in `VZ-PMDP-bus`, in two liveries (`pmdpcervenobila` for SOR NB 12, Urbino 18 III/IV and the midibuses; `pmdpcervenocernobila` for SOR NS 12 and NS 18). Advert wraps map to the normal livery. Articulated: `-A` + `-B` (the Brno bus convention).

## How to update

1. Fetch new data with the trolleybus pipeline (`../plzen-trolleybus/scripts/run.py --state … --fetch`), then the bus lists of the new vehicle day: `python run.py --state 2026-09-29 --fetch` here (per-line lists and registers into `../plzen-trolleybus/data/raw`).
2. Copy the state, set the dates (the same vehicle day as the trolleybus sheet), and run `python ../../plzen-trolleybus/scripts/03_timetable.py --state <new> --base ..` to check rates, approximations and `not modelled`.
3. Re-check the 40 and 42 pools: if seznam-autobusu.cz logs 40 or 42 again, give them their own records.
4. `python run.py --state <new>`. For a short line, fetch its history first (`01_fetch.py --history <line> --since <date>` in the trolleybus scripts).
