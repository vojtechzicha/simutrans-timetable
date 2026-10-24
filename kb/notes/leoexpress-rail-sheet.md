---
name: leoexpress-rail-sheet
description: Leo Express rail lines Simutrans sheet (done 2026-09-26) — built with the RegioJet pipeline, carrier 3616, two lines
metadata:
  type: project
---

**ARCHIVED 10 Oct 2026** (user: "archive all (all done)", trains only): the page moved to `archive/`. It had already been superseded by the MD-CR v4 game lines ([[md-cr-rail-sheet]], also archived).

Leo Express sheet done 2026-09-26: leoexpress-lines.html in project root, artifact https://claude.ai/artifact/TQewhSff6xiK6whk3EKxZL. Same format and method as [[regiojet-rail-sheet]].

Leo Express in JR2026 = carrier 3616 only (35 train files, 20 regular Tue–Thu trips). Two lines: Praha – Ostrava (variants to Bohumín → PL, to Čadca → Prešov, one-way to Ostrava hl. n.) and Praha – Přerov – Břeclav (→ Bratislava, since 30 Apr 2026). No depot runs are published, so stabling points are suggested. Border stations (Zebrzydowice, Chałupki, Kúty) are not passenger stops in the data.

**How to apply:** the build scripts were copies of the RegioJet build.py with carrier/line tables swapped; for another operator do the same (session scratchpads get cleared, so the scripts may have to be rewritten). Needs a JR2027 refresh like the RJ sheet.
