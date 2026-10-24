---
name: s75-beroun-rakovnik
description: "S75 Beroun – Křivoklát – Rakovník sheet (13 Oct 2026): hourly :59/:56, crossing at Zbečno, 3 × 847; scope: only S75, the user counts Kladno – Rakovník (S50/R24) as the S5 family"
metadata:
  node_type: memory
  type: project
  originSessionId: 869cad64-eb55-4684-9c62-16b8936eb818
  modified: 2026-10-13T20:29:02.791Z
---

On 13 Oct 2026 the user archived the trains-west sheet ([[beroun-plzen-pribram-trains]]) and asked to "continue with trains north of Beroun up to S5 (excluding it)". Asked to choose, they picked "Only S75 Beroun – Rakovník", and said all track is built in the game.

- **Sheet:** `pipeline/local-rail/build_s75.py` writes `S75 Beroun Rakovník.html` in the project root.
- **Artifact:** https://claude.ai/artifact/8Ci1ZEfk4aNP89HntfvTbH
- **Line:** S75, every 60. Beroun :59 out, Rakovník :56 back. The afternoon peak runs 14:59, 15:59 and 16:59 out, and 14:57 and 15:56 back.
- **Crossing:** at Zbečno. The train to Rakovník waits there :22 – :26, and that stop is timed.
- **Vehicles:** 3 × ČD 847 RegioFox. They turn in 10 min at Beroun and 59 min at Rakovník.
- **Rejected alternative:** the :12 return. It crosses at Roztoky and also needs 3 vehicles, but it puts 54 min at Beroun.

**Scope facts:**
- In JR2026, S5 is Praha Masaryk. – Kladno – Kralupy (1005/1045, with R45 = 1145 on the same track).
- Kladno – Rakovník is S50 (1050) plus R24. The user treats it as part of the S5 family, so it is out.

**How to apply:** wait for the user's feedback. If the user widens the scope, the candidates are:
- S50/R24 Kladno – Rakovník;
- S54 Hostivice – Středokluky – Noutonice;
- the lines beyond Rakovník: 1057 to Jesenice, Žlutice and Bečov; 4012 to Louny and Most; 4014 via Lužná to Žatec and Chomutov.

Rules: [[rail-design-rules]], [[find-every-train-feedback]].
