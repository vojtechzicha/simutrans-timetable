# Workflow: update, create, publish, sync

## Where things live
| What | Where | In git? |
|---|---|---|
| Working folder (pipelines run here, raw data 1.1 GB) | `D:/OneDrive/Documents/Personal/Transport Fun/Simutrans-Timetable/` | no |
| Sheets as built | working folder root (active) and `archive/` | copied to `public/sheets/<slug>.html` |
| Pipeline code, configs, READMEs | working folder `pipeline/<x>/` | mirrored to `mirror/pipeline/` (no `data/`) |
| Per-sheet metadata (hand-written) | `data/catalog.json` | yes |
| Publish history mined from transcripts | `data/provenance.json` (`python -I tools/mine_transcripts.py`) | yes |
| What the app shows (generated) | `data/sheets.json` (`pnpm sync`) | yes |
| Rules, lessons, notes | `kb/` | yes |
| The owner's view of each sheet | its claude.ai artifact (URL in the catalog) **and** this web app | — |

The working folder is the source of truth for pipelines and data; this repo is the source of truth for rules and the catalogue.
**Sync is one-way: working folder → repo.** Never edit `public/sheets/*.html` or `mirror/` by hand; change the pipeline and rebuild.

## Refresh an existing sheet ("make it up to date")
1. Open the sheet in the app: check its **data day** (vehicle day / network date), sources and the pipeline's update recipe
   (`mirror/pipeline/<x>/README.md` → "How to update"). Decide what's stale: timetable (new GTFS/JDF/JR), vehicles (new peak
   day), or pak objects.
2. In the working folder, fetch into **new dated raw folders** (`run.py --fetch`, `01_fetch.py …`; live feeds must be polled *on*
   the vehicle day over the peak, machine kept awake).
3. Copy the state/config to a new state name (or update `config.json`), pointing at the new dates; set `compare_with` to the old one.
4. `python scripts/run.py --state <name>` (or the sheet's `build_*.py`). Stdlib-only Python; run from the pipeline folder.
5. Compare the "What changes" table and schedules against the previous state. For a sheet already in the game: **rebase, fewest
   moves** (`04b_rebase.py`), not a fresh roster.
6. Hand-review (bus sheets: every approximate row; coverage check; bunching scans), then publish:
   - republish to the **same artifact URL** (Artifact tool: `read` the URL first in a new conversation, then publish with `url`);
   - `pnpm sync` here, check the report, commit, push → Vercel redeploys.
7. Tell the owner what changed **and the in-game change list**: line, entry, old → new Every/Offset/Also at, vehicles in/out.
8. Update `data/catalog.json` (dataDay, status, notes) and, if a rule changed, `kb/rules/*` + an entry in `kb/lessons.md`.

Known refresh triggers:
- **13 Dec 2026** national timetable change (JR2027): every rail sheet; RegioJet ÚK takes over U1/U3/U32/U51/U54; most city feeds too.
- **18 Dec 2026** end of the Prague Nákladové nádraží Žižkov – Ohrada closure: reverse change sheet against state `2026-10-12`.
- Masarykovo nádraží works end 12 Dec 2026 (S5/R45/R24/S54 back from Praha-Bubny).
- Ostrava bus 582 / TFJ 731 diversions to 30 Nov; Novojičínsko diversions to 12 Dec.
- New pak objects installed (stand-ins `≈` can become exact): re-run the fleet/render steps.

## Create a new sheet
1. Read the rule set for the kind: [city fleet](rules/city-fleet-sheets.md), [bus](rules/bus-sheets.md) (+ `bus-schedule-method.md`
   for regional/small-town), [rail](rules/rail-sheets.md) (+ `rail-design-rules.md`), and [fork schedule](rules/fork-schedule.md).
2. Start from the nearest pipeline (`--base` reuse for ODIS; import libs read-only rather than copying). Follow the folder layout in
   `mirror/pipeline/README.md`: `README.md`, `states/` or `config.json`, numbered `scripts/` + `run.py`, `assets/`, `data/raw/<kind>/<date>/`,
   `data/derived/`.
3. Inventory first (every trip / every train / every stop), then design, size from the pattern, assign real vehicles, pak objects
   (ask the fleet desk), sticky header (fleet sheets) or plain tables (rail design pages).
4. Run the publish checklist below, publish as a claude.ai artifact, add a `data/catalog.json` entry, `pnpm sync`, commit, push.

## Publish checklist
- [ ] Every line/train/stop of the scope is modelled or listed under Not modelled with a reason.
- [ ] Both ends of every Simutrans line at the same rate; no ½ minutes; offsets < interval; ≤ 8 slots; evenly spaced slots folded.
- [ ] Loop −1 applied where (and only where) it should be, stated on the page, real minutes shown.
- [ ] Vehicle need sized from the suggested pattern; every line has vehicles (observed → other days → designed with real numbers).
- [ ] Every vehicle shows numbers · depot / full type · length / pak core; spares marked "not needed"; every roster type used.
- [ ] Approximate rows and owner choices listed in "To check" with the slower option.
- [ ] Bunching scan at shared termini, junctions and trunks (bus); engineering works checked (rail); track ends respected (rail).
- [ ] Sticky bar works at 390 px and 1400 px (fleet sheets).
- [ ] In-game change list prepared (if the sheet was already published).

## The web app
- `pnpm dev` — local preview; `pnpm build` — static build (Next.js App Router, all pages prerendered).
- `pnpm sync` — copy sheets + pipeline code from the working folder, rebuild `data/sheets.json`; prints new/changed/removed sheets and
  sheets missing a catalogue entry. `SIMUTRANS_SOURCE=<path>` overrides the folder; `pnpm sync -- --dry` reports only.
- `python -I tools/mine_transcripts.py` — refresh `data/provenance.json` (first/last publish, artifact URLs) from local transcripts;
  run before `pnpm sync` when sheets were published from another folder's sessions.
- Deploy: push to `main` on GitHub → Vercel builds automatically.
- The repo is **public**: never commit raw downloads, transcripts, user messages, credentials or the owner's email.
