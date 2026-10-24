# Simutrans timetables — start here

This repo is the home of the owner's Simutrans timetable work: a web app that shows every sheet with its sources, sync method and
dates, and a knowledge base (`kb/`) holding every rule and lesson from the sessions that built them (Sep–Oct 2026).

@AGENTS.md

## Before doing anything
- Read `kb/README.md`, then `kb/workflow.md`. For any sheet work read the matching `kb/rules/*.md` and skim `kb/lessons.md`.
- The pipelines and their 1.1 GB of raw data live in the **working folder**
  `D:/OneDrive/Documents/Personal/Transport Fun/Simutrans-Timetable/` (= `~/Documents/personal/transport fun/Simutrans-Timetable`).
  Run pipelines there, never from `mirror/` (it has no data). Then `pnpm sync` here.
- Per-sheet facts (sources, data day, pipeline, build command, artifact URL, status) are in `data/catalog.json`; generated
  `data/sheets.json` adds file hashes and publish history.

## Layout
- `app/` — Next.js 16 App Router site, fully static. `lib/` — data loaders. Read `node_modules/next/dist/docs/` before changing
  Next-specific code (this Next version differs from older training data).
- `public/sheets/<slug>.html` — sheet copies, served untouched in an iframe (each keeps its own design).
- `mirror/pipeline/` — pipeline code + READMEs copied from the working folder (no `data/`). Read-only here.
- `data/` — `catalog.json` (hand-written), `provenance.json` (mined), `sheets.json` (generated).
- `kb/` — rules, sources, workflow, lessons, related projects, and `notes/` (original memory notes verbatim).
- `tools/sync.mjs`, `tools/mine_transcripts.py`.

## Commands
- `pnpm dev`, `pnpm build`, `pnpm lint`
- `pnpm sync` (`-- --dry` to preview) — working folder → repo, rebuild `data/sheets.json`
- `python -I tools/mine_transcripts.py` — refresh `data/provenance.json` from `~/.claude/projects` transcripts
- Deploy = push `main`; Vercel builds it.

## Hard rules
- The repo is public: no raw downloads, transcripts, user messages, credentials or the owner's email in commits.
- Never edit `public/sheets/` or `mirror/` by hand — change the pipeline in the working folder, rebuild, sync.
- After changing any sheet the owner already uses, give them the in-game change list (old → new values, vehicles in/out).
- Engine repo `simutrans-122.0`: hands off, ask an engine session. Pak objects: ask the fleet desk session. Save renames: the engine's
  rename service only. Find live sessions with ListAgents.
- When a rule changes, update `kb/rules/*` and append to `kb/lessons.md` in the same commit.
