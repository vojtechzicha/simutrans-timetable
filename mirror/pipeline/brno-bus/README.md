# Brno city buses (DPMB and BDS-BUS)

The Brno bus sheet is built from stored raw data by the scripts in this folder. It follows the trolleybus pipeline (`../brno-trolleybus`), the tram pipeline (`../brno`) and the shared rules in `../README.md`.
- `scripts/common.py` imports every generic helper from `../brno-trolleybus/scripts/common.py`: fetch, GTFS, `runfit`, `runfit_rate`, `circuit_need`, `turnarounds`. Those in turn come partly from the tram pipeline.
- The page style is the tram sheet's, plus the trolleybus sheet's `extra.css.html` (sticky header, search).

| State file | Network | Vehicles | Output (project root) | Artifact |
|---|---|---|---|---|
| `states/2026-09-29.json` | from Tue 29 Sep 2026 (service day 29 Sep; same as 25 Sep) | Fri 25 Sep 2026 | Brno Bus Peak Fleet.html | https://claude.ai/artifact/Q1cS9fRTKPNHJYbmsNPv3T |

```
cd pipeline/brno-bus/scripts
python run.py --state 2026-09-29
```

Python 3, standard library only. Maintained by session simutrans-timetable-3a.

## Scope

All Brno city bus lines with afternoon-peak service: 40–84, the peak express lines E50, E56 and E75, and the replacement line x75.

Left out:
- night lines N89–N99;
- school lines š85, š86, š88;
- rail replacement buses (xR…, xS…) and regional replacements (x333, x442, x514);
- 73 (one trip in the peak) and 80 (none).

## Sources

| What | URL | Stored in |
|---|---|---|
| Vehicle per kurz, one page per line | `https://www.bmhd.cz/vypravenost/vypravenost.php?datum=YYYY-MM-DD&linka=N` | `data/raw/vypravenost/<date>/L<N>.html` |
| DPMB bus register: Medlánky `m`, Slatina `s` | `https://www.bmhd.cz/evidence-dpmb/vozovna/{m,s}` + `vozp.php?...trakce=autobus` listings | `data/raw/register/<date>/` |
| Buses of other operators (BDS-BUS on 48 and 74) | `https://seznam-autobusu.cz/vuz/<id>`, linked from their vypravenost rows (`01_fetch.py --external <date>`) | `data/raw/external/<id>.html` |
| Timetable | IDS JMK GTFS, `route_type` 3. Shared with the tram pipeline (`common.gtfs_path`). | `../brno/data/raw/gtfs/2026-09-28/gtfs.zip` |
| Pak objects | local pak128 checkout, `build/VZ-DPBrno-bus` (main b84c15c), read only | `assets/pak.json` |

## Steps

1. `01_fetch.py`: `--vehicles <date>`, `--register`, `--external <date>`.
2. `02_parse.py`: vypravenost (with traction) and register, plus the external vehicles, keyed by registration.
3. `propose.py` (not in `run.py`): a helper for writing the state.
   - The feed has no vehicle blocks and splits long workings at timing points.
   - It chains trips first-in-first-out at each stop, prints each leg's successors, and drafts circuits.
   - The `simutrans_lines` in the state were written from its output, with the manual decisions listed below.
4. `03_timetable.py --state X`: fits every entry at one rate per line, then applies turn −1 or keeps the through-stop minute.
   - One-way lines get an untimed far end (`empty_return`).
   - Each line is sized with `circuit_need`. Minute subsets get their own copies of the trips, and a round trip that waits longer than the line's interval (at least 30 min) is skipped.
5. `04_fleet.py --state X`: picks the afternoon bus per kurz and shares record lines out between their Simutrans lines by need. Shortfalls are listed.
6. `05_render.py --state X`: writes the HTML.

## Decisions

- **Day:** vehicles from Fri 25 Sep, network from 29 Sep (unchanged), as on the tram and trolleybus sheets.
- **Stop types:** every turning point gets turn −1. A timing point the bus passes without turning keeps the real minute. An entry counts as a turn when the previous leg came from the stop this one goes to. Force either with `through` / `turn` in the state.
- **Circuits and splits (from `propose.py`):**
  - **40** runs as one circuit: Tovární → Úzká → Tuřany → Úzká → Tovární.
  - **41** splits into three lines: 41V (Ivanovice ↔ Vranov) and 41L (Ivanovice ↔ Lelekovice), each hourly, told apart by minute (`mod 60`), and 41M, the Královo Pole – Mácova shuttle.
  - **49** splits into two separate circuits: 49M (Hlavní nádraží – Modřice) and 49P (Mariánské náměstí – Přízřenice).
  - **57 + 66** splits into three lines:
    - 57L, the Lesná loop, with the number changing at Halasovo náměstí and Poliklinika Lesná;
    - 57U, Haškova – Útěchov;
    - 57V, Maloměřický most – Vranov.
  - **58** splits into 58Z (Židenice) and 58N (Novolíšeňská).
  - **68** gets its Myslivna branch as 68M.
  - **72** splits into 72L (Lesná) and 72S (Areál Slatina).
  - **77** splits into three lines: 77S (Slatinka), 77L (Letiště), and 77A, the one-way Areál Slatina → Úzká peak line.
  - **78** splits into 78N (Novolíšeňská – Areál Slatina) and 78M (Židenice – Modřice).
- **One-way peak lines:** E50 (Kamechy → Areál Slatina → Říčanská), E75 and 77A. The far end has no timetable, and the empty run back is estimated from the reverse-direction timetable (E50: 20 min, a guess).
- **Not modelled:** 72 Technologický park → Královo Pole, nádraží. It starts at 16:48, when 72 stops serving Lesná, so it is the post-peak form of the line.
- **Fit (after the Prague trolleybus review, 29 Sep):**
  - A Simutrans line's rate is the number of real 16:00–16:59 departures that most entries share (on a tie the lower).
  - Every entry must reproduce the whole 16:00 hour. The fit tries the shared core, then the 16:00 hour, then the 16:xx minutes repeated hourly.
  - Where an end runs more buses than the line's rate (77L Letiště), the sheet says partial and lists the real minutes not modelled.
  - E50 turns at Areál Slatina (`turn`).
- **Hand-set rows (method check of 25 Oct 2026, `pipeline/brno/method-check-2026-10-25.md`), in `fit.overrides` (key `<line id>|<line>|<from>|<to>`):**
  - **48** every 30 at both ends (Úzká :13, Prace, točna :04). Every other hour the :43 / :34 trip starts or ends two stops further at Prace, Mohyla míru; an override's `passing` lists those departures (minutes after midnight) so they count for the match, not for sizing. 48 has `period: 60` so `circuit_need` closes its 90-min round (the real 17:43 runs on to Mohyla míru).
  - **72L** at 4 an hour (`rate: 4`; Lesná :15 :25, Technologický park :08 :18): the Lesná section runs 4 an hour until about 17:00; the 16:48 slot is the bus that runs to Královo Pole instead.
  - **75** at 4 an hour (`rate: 4`; Tomkovo náměstí :01, Slatina :14): its every-15 peak form, which needs the same 4 buses.
  - A hand-set row that reproduces its first–last stretch exactly is shown as "partial, exact <span>" (`stretch` in timetable.json).
- **Need = max(circuit need, on the road)** (the Prague/Ostrava bus rule, 29 Sep): the most trips of a record group holding a bus at once in 16:00–16:59, each until arrival + min(3, the terminus's shortest turnaround). The extra goes to the main line. Only 75 rises (3 → 4, 7 out). On the trolleybus sheet the on-road count never exceeds the cycle need, so nothing changes there.
- **Swaps:** 52/28 and 67/7 keep the bus from before the swap, because the replacement worked another kurz in the afternoon (`fleet.keep_before`).
- **Unrecorded lines and their kurzy:** bmhd.cz files several lines under other line numbers. The sources are the IDS JMK timetable PDFs ("jede jako linka …"), jrbrno.cz joint timetables and trip codes, and bmhd.cz.
  - 54 runs on 52 kurzy (joint 52 + 54 timetable).
  - E50 runs on 50 kurzy 21–32.
  - 55 runs on 58 kurzy ("jede jako linka 58").
  - 66 runs on 57 kurzy (57/66 number change at Halasovo náměstí and Poliklinika Lesná).
  - 70 runs on 42 kurzy (joint 42 + 70 timetable).
  - E56 has its own kurzy, filed as **56** (`01_fetch.py` fetches line 56).
  - Inferred from jrbrno.cz alone, which still carries the winter 2025/26 data: 46 on 57 kurzy, and afternoon E75 on 58 kurzy.
- **Line 63** starts on 1 Oct 2026, so it is not in the 29 Sep network (`not_peak`). The service day is therefore Tue 29 Sep itself (`service_date` 20260929), not a later Friday.
- **x75** is the long-term Fryčajova closure (1 Nov 2025 – 31 Oct 2027), modelled as it runs.
- **Kurz allocation:** the records never name a branch. Kurzy of one record line are shared out by timetable need (a choice), and the record line's own main line takes the rest (its surplus is then marked not needed, see Spares). Pooled lines take their need from the highest kurz numbers.
- **Spares (user, 29 Sep):** where more vehicles were logged than a Simutrans line needs, exactly the need stays counted and the rest is marked "not needed" (`common.mark_spares` in brno-trolleybus): one of every vehicle type of the line is kept first (most frequent type first; a substitute bus on a trolleybus line is no type and goes first), then afternoon-only kurzy and the highest kurz numbers are dropped first. Not-needed vehicles are dimmed at the bottom of their card and left out of all counts, the depots and the pak totals. This replaces the earlier "operator's slack" rule.

## How to update

1. New timetable: refresh the GTFS in `../brno`, then copy the state and set `gtfs_date` and `service_date`.
   - Run `propose.py` on the lines that changed, and update `simutrans_lines`.
   - Run `03_timetable.py` and check the rates, spans and `not modelled` list.
2. New vehicles: `01_fetch.py --vehicles <Friday> --register --external <Friday>`. Set the dates and re-check `keep_before` and the shortfalls.
3. `python run.py --state <new>`, then re-publish.
   If `04_fleet.py` reports a shortfall, design the missing vehicles by the user's roster rule (pipeline/README.md, "Roster coverage and spares"; Prague bus 04_courses.py): take the line's history roster, first one free car of each type the used cars lack, then fill by recency. Show the leftover free history cars as "not needed" rows. On 29 Sep no Brno line was short, so no vehicles were designed.
4. **BDS-BUS pak objects:** built and installed by the pak session (VZ-Brno-bus.pak, main fb42eb7, 29 Sep); names in `assets/pak.json` and `data/derived/2026-09-29/vz_installed_objects.txt`.
