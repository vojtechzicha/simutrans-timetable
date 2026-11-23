# MHD Pelhřimov + VDV 250 (vypravenost sheet)

Output: `MHD Pelhrimov.html` in the project root, published on the site (no artifact). Built on 23 Nov 2026 at the owner's
request: "create MHD Pelhřimov sheet with 250 VDV line extra". Small-town network + one regional line, so the whole sheet uses
the bus schedule method (`../bus-schedule-method.md`, v4).

## Scope

- **MHD Pelhřimov**: licences 355001–355004 (lines 1–4), ICOM transport a.s., provozovna Pelhřimov (JDF line type A, town).
  `config.jdf.line_numbers` maps them to 1–4 (the shared `02_timetable.py` would otherwise number them 001–004).
- **VDV 250** Pelhřimov – Humpolec – Havlíčkův Brod, Dopravní terminál: licence 357250, ČSAD AUTOBUSY České Budějovice a.s.,
  provozovna Oblast Humpolecko.
- Two areas in `config.areas`, each with its operator's IČO (ICOM 46346040, ČSAD ČB 26060451).

## Sources

| What | Where | Notes |
|---|---|---|
| Timetable | CIS JŘ bus JDF export of 23 Nov 2026, `data/raw/jdf/2026-11-23/JDF.zip` | Every version ends 12 Dec 2026 (JR2027 not yet in the export). MHD 3 and 4 have a diversion version 1 Oct – 30 Nov (same stops, some departures 1 min later): the regular version is modelled (`regular_not_diversion`). |
| Live vehicles | VDV live map `https://mapavdv.kr-vysocina.cz/` (Kraj Vysočina): `GET Ajax/GetPoints` (every vehicle: id, position, licence, final stop, delay; JSON, no key) and `GET Ajax/OpenInfoWindow?id=<id>` (HTML: "Linka / spoj 355003 / 16", "Číslo vozidla 3-4515") | No history: poll on the vehicle day. `scripts/01_live_poll.py` keeps every GetPoints answer (gzip) and the info window of every point on the sheet's licences. A ČSAD bus shows twice, once with its VDV number (64-10021) and once with its plate (7J84832), at the same place on the same trip: `01_live.py` pairs them. The ICOM town buses showed only the VDV number (3-4515) on 23 Nov. |
| Fleet register | seznam-autobusu.cz lists `seznam?iddopravce=602` (ICOM transport) and `232` (ČSAD AUTOBUSY ČB), read in the owner's Chrome on 23 Nov 2026 → `data/raw/register/2026-11-23/browser_read.json` | Scripts get HTTP 429 there (see `kb/sources.md`). Kept: the Pelhřimov depot of ICOM (39 buses; the four "MHD Pelhřimov" ones are Isuzu Novociti Life, blue with a white fade) and the Pelhřimov and Humpolec depots of ČSAD ČB (Iveco Crossway LE LINE 10,8M / 12M / 14,5M in VDV paint). Neither operator has fleet numbers in the register; the join is by plate. |
| pak128 | `C:/Users/vojte/Developer/simutrans-custom-czech-pak128`, `build/VZ-VDV-bus`, `build/VZ-MHDPelhrimov-bus` | Crossway LE LINE 10,8M and 14,5M exist in VDV paint. The 12M in VDV paint and the Novociti Life in ICOM blue were asked from the art session simutrans-122-0-c1 on 23 Nov 2026 (owner: "ask the art session, I saw you doing the nearest match"); `config.pak.rules` already names them, so the "≈" marks clear when they are built. |

## Steps (`python -X utf8 scripts/run.py`)

Sheet-local: `01_live.py` (poll → `data/raw/<snapshot>/live_compact.json`, keyed by VDV vehicle number), `01c_fleet.py`
(register → `data/derived/fleet.json`, same keys), `06_render.py` (a copy of the HKO renderer with the VDV wording; presentation
only). The schedule, roster and coverage steps are the ODIS regional ones run unchanged with `--base pelhrimov`
(`odis-regional-hko/scripts`: `02_timetable`, `03_read`, `05_schedule`, `04_roster`). Hand-set texts, notes and pak rules:
`authoring/set_texts.py` (rerun after editing). The poller runs on its own:

`Start-Process python -ArgumentList '-X','utf8','01_live_poll.py','<end, e.g. 2026-11-24T20:00>' -WorkingDirectory <scripts> -WindowStyle Hidden -RedirectStandardOutput ..\data\raw\live\poll_<date>.log`
with `keep_awake.py <end>` beside it.

## Decisions (23 Nov 2026)

- **Line 1**: one Simutrans circuit every 120 following the real afternoon bus (silo 14:40 → Táborská, 15:30 → silo, 15:45 →
  Starý Pelhřimov, 16:15 → silo), exact on all four; 1 bus where separate Táborská and Starý Pelhřimov lines need 2. The
  14:00–14:45 shift extras and the short Táborská – bus station trips are off the pattern (no repeating minute).
- **Line 3**: a loop from the bus station run both ways; each way its own Simutrans line. First designed as one line every 60
  alternating the ways (:15 / :45), which failed Step 4; the passing patterns are used: via the railway station every 180 at
  16:15 / 16:50, via Pod Floriánem every 240 at 15:45 / 16:57. Paths: via Křemešnická and via Skrýšov, so every stop is on a line.
- **Lines 2 and 4**: shift/school lines whose stops are all on 1 and 3; not modelled (Step 8).
- **250**: hourly, Pelhřimov :43 / Havlíčkův Brod :12, 3 buses. **250 Humpolec** (short trips to Humpolec, Poliklinika) is an
  outstation line at its inbound rate, every 240 (13:18 / 17:18 out, 14:07 / 18:07 back); it runs via Kojčice, Vadčice,
  Dehtáře and Velký Rybník, obec, village stops only detour trips serve (every place served).
- Need 7 (MHD 3, VDV 4). Coverage complete (65 afternoon stops). Audits: `method-check-2026-11-23.md`.

## Vehicles

Version 1 (23 Nov) has no buses: the VDV map keeps no history and the evening of 23 Nov is not the peak. The poller runs all of
Tue 24 Nov (05:00–20:00 every minute); version 2 names the bus on every line. Open question for v2: whether the ICOM town buses
ever show a plate on the map; if not, they are named by VDV number with the type unknown (`config.vdv_numbers` can map a VDV
number to its plate once known).

## How to update

1. On a weekday, start the poller before 05:00 (or before 13:00 for the afternoon only) with `keep_awake.py`.
2. Set `snapshot`, `vehicle_day` and the labels in `config.json`; refresh the JDF into a new dated folder and point `jdf.zip` at it.
3. `python -X utf8 scripts/run.py`; check the To check list, the audits (`audit/step4_regional.py pelhrimov`, and
   `AUDIT_SHEETS=pelhrimov` for `branch_check.py`, `path_check.py`, `passing_check.py`).
4. `pnpm sync` in the repo, commit and push (the site is where it is published).
