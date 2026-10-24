---
name: r18-luhacovice-coupled
description: "R18 Slovácký expres Praha – Staré Město – Luhačovice as fork coupled lines (9 Oct 2026); 11 vehicles; build_r18.py; fork coupling feature"
metadata:
  type: project
---

**ARCHIVED 10 Oct 2026** (user: "archive all (all done)"): page in `archive/R18 Slovácký expres.html`, build_r18.py writes there. Work moved on to [[beroun-plzen-pribram-trains]].

On 9 Oct 2026 the user archived the Benešov sheet ([[r49-benesov-local]]) and asked for "the R to Luhačovice … coupling trains. One line doing Praha -> Staré Město …, some doing the full Luhačovice track with diesel locomotive".

The fork has coupling (engine `C:\Users\vojte\Developer\simutrans-122.0\CLAUDE.md`, "Coupling trains", example R12a/R12b Brno – Zábřeh – Šumperk/Jeseník). The joining line's schedule entry says "Couple with X, wait up to N min". The trains part at the first stop where their next stops differ. The fork's mixed traction leaves a diesel idle under the wire.

Design: `pipeline/local-rail/build_r18.py`. Output: `R18 Slovácký expres.html`. Artifact: https://claude.ai/artifact/V8hoXRQ3jnL3DbpR941PQ3
- R18 (primary): RAILL 193 + Staré Město Bmz. Every 120, 5 vehicles.
- R18 Luhačovice (joining): 750.7 + 5 through coaches. Every 120, 6 vehicles. It couples at Praha odstavné nádraží and at Staré Město towards Praha.
- Real parity is kept: Staré Město wait 1 h 18, Luhačovice 1 h 11. A 9-vehicle short-turn version would put trains in invented hours; it was offered, not built.
- Depot ends use the real Praha Jih runs.

**Why:** the user wants the real train's split modelled.

**How to apply:** use this coupling pattern for other split/through-coach trains. Only the joining line carries "Couple with". Related: [[rail-design-rules]], [[simutrans-fork-schedule-spec]].
