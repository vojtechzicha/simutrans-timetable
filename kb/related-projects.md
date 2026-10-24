# Related projects and sessions

The timetable work is one of three Simutrans projects on this machine. Work was coordinated between parallel Claude Code sessions
with SendMessage; session names change between days, so find the live ones with **ListAgents** before messaging.

## The game
- **Engine fork:** `C:\Users\vojte\Developer\simutrans-122.0` (Simutrans 122.0 fork with timetables, coupling, terminal stop type,
  departure boards…). Its `CLAUDE.md` documents the schedule features ("Coupling trains"). **Hands off:** never edit/commit it or run
  `steam-fork.sh`; ask an engine session (`simutrans-122-0-*`). Engine questions go there, not to the pak session.
  Claude memory: `~/.claude/projects/C--Users-vojte-Developer-simutrans-122-0/memory/`.
- **Pak:** `C:\Users\vojte\Developer\simutrans-custom-czech-pak128` (VZ vehicle families, signals, stations). Built objects:
  `build/VZ-<City>-<mode>/`. Requests go through the **fleet desk** session (see [rules/pak-objects.md](rules/pak-objects.md)).
  Claude memory: `~/.claude/projects/C--Users-vojte-Developer-simutrans-custom-czech-pak128/memory/`.
- **Save game:** `D:\OneDrive\Documents\Simutrans\save\` — current save `FORK-CZR-VZ.sve` (~400 MB, migrated from the CZR pak to VZ
  objects by binary name rewrite). Only the engine's save session touches it.

## Services other sessions provide
- **Save-game rename service** (engine session, announced 29 Sep as `simutrans-122-0-58`): send the path of a UTF-8 TSV
  `KIND<TAB>ID<TAB>OLD NAME<TAB>NEW NAME` (KIND = halt, line, convoy, player, city (X,Y), factory/marker (X,Y,Z); OLD `*` skips the
  check; `#` comments). It backs up and writes `NAME-renamed-<date>.sve`. Two stops can't share a name (swaps need a temp name).
  **Never run the rename tool yourself**, and never send a list the owner hasn't approved (Prague `07_halt_renames.py` TSV is
  prepared, not sent).
- **Save export / line inventory:** the fleet desk or an engine session can export the save headless when the game is closed
  (`rail_lines.md` with 161 rail lines on 14 Oct; 577 ODIS 800xxx lines on 22 Oct).
- **Coupling / engine behaviour tests:** engine sessions (the S4 Kralupy coupling was tested by `simutrans-122-0-36`).

## Former timetable sessions (for reading old transcripts)
Sheets were built by parallel sessions named `simutrans-timetable-<xx>` in the OneDrive project folder. Their transcripts live in
`~/.claude/projects/D--OneDrive-Documents-Personal-Transport-Fun-Simutrans-Timetable/` (one JSONL per session; the session id of
each publish is in `data/provenance.json`). Owners at the time: c6 Brno/Plzeň trams (Brno = the method reference), 9e Prague/Olomouc
trams, 10 Ostrava/Most trams, 3a Brno bus/trolleybus, 5a Prague trolleybus/bus, a2 smaller cities, f5/b5/0b Ostrava
trolleybus/bus, a4 Havířov/Karviná/Orlová, 6b ODIS regional, b2 MD-CR. All of that now lives in this repo's KB.

## Files outside the repo that matter
- `D:/OneDrive/Documents/Personal/Transport Fun/Simutrans-Timetable/` — the **working folder**: sheets + `pipeline/` with raw data.
- `~/Documents/personal/transport fun/Trains.md`, `Train Durations.md` — older personal notes on trains (not used by pipelines).
