# ODIS Novojičínsko, Bílovecko (regional + town buses, vypravenost sheet)

Output: `ODIS Novojicinsko Bilovecko.html` in the project root, published at the URL in `config.json` → `artifact_url` (republish to the same URL). Built on 21 Oct 2026 after the owner asked for the next ODIS sheets ("Yes, do those next sheets"), one of three built in parallel (Opavsko and Bruntálsko are the others).

This folder holds only the sheet's config, authoring scripts and data. The scripts are the shared ones in `../odis-regional-hko/scripts/`, run with `--base odis-regional-novojicinsko`. The method is `../bus-schedule-method.md` (v3; v4 since the 25 Oct 2026 method check), as on the Havířovsko/Karvinsko/Orlovsko and Těšínsko/Třinecko/Frýdecko sheets; the town lines take the same method.

## Scope

| Section | Licences | Operator | Fleet | Town pak |
|---|---|---|---|---|
| Novojičínsko Východ | 883xxx | Z-Group bus, pr. Kopřivnice | 63- | – |
| Novojičínsko Západ | 882xxx | Transdev Morava, pr. Nový Jičín | 62- | – |
| Bílovecko | 884xxx | Transdev Morava, pr. Ostrava | 64- | – |
| MHD Nový Jičín | 886xxx | ARRIVA autobusy | plates (01b) | VZ-MHDNovyJicin-bus |
| MHD Studénka | 887611 | Transdev Morava | 62-/64- | VZ-MHDStudenka-bus |

- 90 ODIS numbers. 63 are modelled as 70 Simutrans lines, 108 buses by the pattern after the 25 Oct method check, as published (v5: 108, of which 107 seen on the 20 Oct live map and 1 designed); five lines need one bus fewer and five one more, and the roster is rebuilt with `keep_roster`.
- Elsewhere: 351, 355, 980, 985 (a few trips on 883 licences) are Frýdecko-Místecko lines on the Těšínsko/Třinecko/Frýdecko sheet, which since 22 Oct reads their 883 trips too and has the Z-Group buses seen on them (63-1005, 63-1011, 63-1308; this sheet refilled 656, 657 Kunčice and 661 from its spare buses); 261, 263, 270, 285, 678 go to the Opavsko sheet (most trips there). 655 is modelled HERE (883655 holds 41 of its 45 trips) — the Těšínsko sheet lists 863655's 4 trips as modelled here (resolved 21 Oct).
- Not modelled (`config.unmodelled`): shift lines 331, 372, 675; sparse lines 265, 633, 636, 637, 645, 649, 664, 674; morning-only 639, 666, 695; 651 (its trips are on 657 Kunčice); 602, 603, 604 (in the 601–604 circuit).

## Sources

As the other ODIS sheets (CIS JŘ JDF of 20 Oct 2026 and the ODIS live poll of Tue 20 Oct, both stored by the Havířov/Karviná/Orlová pipeline). Fleet: `01c_fleet.py` fetched the seznam-autobusu registers of Z-Group bus (carrier 240) and Transdev Morava (7546) into `data/raw/2026-10-20/fleet/`; ARRIVA's Nový Jičín town buses and a few unlisted plates come from `01b_plates.py` (`plates.json`).

## Decisions (21 Oct 2026)

- **Network state:** diversions running to 11–12 Dec (286, 623, 641 via Příbor Štramberská, 662, 673 via Březová škola, 679, 692, 693) are modelled as they run; 629 (to 3 Dec, times only), 929 (to 12 Nov) and 643 (16–31 Oct) use `regular_not_diversion`.
- **601–604 town circuit:** the live map shows ARRIVA's three buses running 602 → 601 → 604 → 603 in turn (three buses leave the bus station at :10 every hour). One Simutrans line every 60 with three buses, 1-min turns as in reality (`lay` 1 on the 602 and 601 legs). Four separate lines would need a fourth bus ARRIVA does not run.
- **Coverage variants** (each the only afternoon service somewhere): 287 Pustá Polom (Nový Dvůr, 16:47 one way), 286 Hradec, 620 Pohoř, 621 Ostrava, 625 Tísek (via u kostela), 653 to Frenštát station past Continental, 653 Kopřivnice (town loop inside 883653), 656 back via pod Dílem, 657 Kunčice (657 + 651 trips, via Žuchov/Rákovec), 661 Frenštát circle, 690 to Tymphany, 671 to Skřipov, 619 via Hrabětice točna, 927 via Hranice Tř.1.máje, 632 via Contera Park, 643 Bartošovice round, 379, 929.
- **Hand-set after review** (`authoring/nj_spec.py`): 288, 629, 673 on their real afternoon rounds; 611 hourly at the peak; 603's Tesco return rt 23; 643 as its real three-leg round.
- **Method check, 25 Oct 2026** (`method-check-2026-10-25.md`, method v4): every fitted row was given the Step 4 test per direction; the 80 failing legs of 47 lines were set by hand (every leg of those lines now has typed `at` / `knot_at` values), so 135 of 139 timed legs pass. The four left: 635 and 641 out of Frenštát / Dubina (more buses come back to Kopřivnice than leave around the shift changes, timed at the Kopřivnice rate, by hand) and the 17:10 slots of 602 / 603 in the 601–604 circuit (after their last trip). 287 no longer counts the Pustá Polom trip, and 620 no longer counts the Pohoř trips (each is its own Simutrans line).
- **Bus-saving moves** (25 Oct 2026): where a slot moved by at most 3 min (inside the Step 4 tolerance, with 3-min turns) saves a bus, it is moved and the card says so (286, 371, 374, 622, 655, 656, 665, 690, 696). The builder's older shortest-round moves of up to 6 min broke Step 4 and are gone.
- **Owner checks** on the page: the 601–604 circuit; 655 on this sheet; 698's four slots; 618's three slots (three buses, or every 72 with two); 620 Pohoř every 180 (one bus, or every 120 with two slots each way and three); 370 every 90 (two buses, or every 240 with one); the Kopřivnice town loop.

## Pak

`config.pak.rules`: VZ-ODIS-bus for regional buses (Setra S 415 LE business bila, SOR CN 12 / CN 9,5 / CNG 12 / CNG 10,5 transdev, Crossway LE Line transdev, Crossway LE City bila, Citywide LE 12M CNG bila, BORS SOR CN 12 borszlutomodra); VZ-MHDNovyJicin-bus (SOR EBN 9,5 červená metalíza) and VZ-MHDStudenka-bus (SOR BN 12). All confirmed by the pak fleet desk on 21 Oct. Two drawn for this sheet: Crossway LE Line 12M in Z-Group livery (6Z9 6492) → `VZ-ODIS-Crossway_LE_Line_12M-bilazelenomodra` (21 Oct), and ARRIVA's red-black SOR BN 10,5 (7577, 2TT 8558) → `VZ-MHDNovyJicin-SOR_BN_10_5-cervenocerna` (22 Oct, pak main 0fda6a6; layout unverified, since no photo after the 2025 repaint exists; the name stays if the art is corrected). No stand-ins left.

## Authoring and review (`authoring/`)

- `nj_spec.py` writes `config.lines` (+ notes from `nj_notes.py`); `nj_config.py` writes everything else (versions, other sheets, area_home, pak, texts, network state, owner checks, unmodelled reasons, artifact_url). Both idempotent.
- `groups.py L,...` (trips grouped by ends, `--stops` for paths), `dump.py`, `review.py` for the hand review; `divcmp.py` compares diversion and regular versions.

## How to update

1. New poll day / JDF: point `snapshot`, `vehicle_day`, labels, `jdf.zip`, `live.dir` at it; `01c_fleet.py --refresh` if the registers changed.
2. Re-check diversions (`authoring/divcmp.py`) and `nj_config.py`.
3. From `../odis-regional-hko/scripts`: `python -X utf8 run.py --base odis-regional-novojicinsko` (run `01c_fleet.py` first when the fleet changed).
4. Review changed lines with `authoring/dump.py`; adjust `nj_spec.py`, rerun it and the pipeline. Build the Ostrava, HKO and Těšínsko sheets first (this one excludes their buses).
5. Republish to `artifact_url`.
