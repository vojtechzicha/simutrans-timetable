---
name: local-rail-062-064
description: "Local (Os) rail lines around Mladá Boleslav designed in chat 3 Oct 2026 — 062, 064, 064N schedules; user likes uneven Nymburk running"
metadata:
  node_type: memory
  type: project
  originSessionId: d8b73c98-95bf-4e88-8c04-c228f701b2a3
  modified: 2026-10-03T11:44:10.970Z
---

On 2026-10-03 the user started designing local Os lines from the JR2026 CIS JŘ data in `pipeline/md-cr/data/derived/trains.json`, answered in chat only (no sheet yet). The user calls lines by KJŘ table number: 062 = Nymburk – Mladá Boleslav (not Chlumec – Křinec), 076 = MB – Mšeno – Mělník (Friday-only on workdays). S35 = svc 1035, S31 = 1031, 064 = svc 1036.

Agreed design (all every 120, Leave up to 30). **Offsets below were written even-first; the user said odd hours come first (+60 for even), so swap ±60 — the artifact already uses the corrected values** (e.g. 062 Nymburk 4, MB město 66):
- 062 Nymburk – MB město, 1 vehicle: Nymburk offset 64 (L:04), MB město 6, MB hl. n. towards Nymburk 14.
- 064 MB hl. n. – Mladějov v Čechách, 2 vehicles: MB hl. n. 84, Mladějov 34, Dolní Bousov towards MB 62.
- 064N Nymburk – MB – Mladějov, 2 vehicles (absorbs the Nymburk 15:32/16:32 extras and the MB 14:38 return): Nymburk 92, MB hl. n. outbound 22 (wait moved from MB město, which has little space; real Os 8544 waits at hl. n. 17:12/17:22), Mladějov 94, Dolní Bousov towards MB 2, MB hl. n. towards Nymburk 41 (was 38; trains only arrive :38).

- 064 Lomnice extension (summer-only in reality) proposed: all 064 to Lomnice nad Popelkou with ~1 h layover there, 3 vehicles (offsets MB hl. n. 84, Lomnice 118, Mladějov→MB 34, Dolní Bousov 62); user hadn't decided standard vs summer.
- 260 Česká Třebová – Svitavy (Os/Sp only, proposed 3 Oct): Os ČT – Letovice 1 vehicle (ČT 67, Letovice 9); Sp ČT – Letovice 2 vehicles (ČT 48, Letovice 33); Kolín – Svitavy Os extras are 010 tails. Then proposed merging instead: all 010 Os Kolín – ČT – Svitavy hourly (Kolín 44, ČT→Svitavy 7, Svitavy 38, ČT→Kolín 59), 6 vehicles, replacing the separate Os ČT – Letovice; Svitavy – Letovice left to the Sp (stops everywhere there).

- **ARCHIVED 9 Oct 2026**: the page moved to `archive/Local Trains 010 062 064 260.html`.
- Artifact published 2026-10-03 and updated the same day: 'Local Trains 010 062 064 260.html' in the project root, https://claude.ai/artifact/CCNUijhQeBxE244KKbKyF3 (hand-written, no pipeline). Total 15 vehicles.
- 010/260 final (user: model the Kolín – Svitavy through trains, they are dear to them; never extend 010 past Svitavy). Offsets are odd-first:
  - 010S Kolín – Svitavy, 4 vehicles, copies Os 5015 out and Os 5020 back, with a 1 h 17 min wait at Svitavy so it alternates with the 260 Os.
  - 010 Kolín – Česká Třebová, 3 vehicles, keeps the real 1 min turn.
  - 260 Os Česká Třebová – Letovice, 1 vehicle, at the real times.
  - 260 Sp, 2 vehicles.
- In reality the 010 through trains replace 260 Os slots; there is no separate 260 Os then.

**Why:** I offered to even out Nymburk (062 and 064N both in odd hours, 28/92 min gaps); the user declined: "don't fix, I like it uneven".

**How to apply:** don't "fix" uneven combined headways at shared stations unless asked. Related: [[md-cr-rail-sheet]], [[simutrans-fork-schedule-spec]].
