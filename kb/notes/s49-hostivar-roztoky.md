---
name: s49-hostivar-roztoky
description: "S49 Praha-Hostivař – Libeň – Roztoky sheet (9 Oct 2026): every 30, 3 vehicles; build_s49.py; PID S-line = CIS svc 10xx"
metadata:
  type: project
---

**ARCHIVED 10 Oct 2026** (user: "archive all (all done)"): page in `archive/S49 Hostivař Roztoky.html`, build_s49.py writes there.

On 9 Oct 2026, while R18 ([[r18-luhacovice-coupled]]) awaited feedback, the user asked "can you change the local trains to S49 in the meanwhile". I first misread that as renaming the 220 Os on the archived Benešov sheet. The user meant the Praha-Hostivař – Roztoky line: "nah, I mean Praha-Hostivař - Roztoky line".

Sheet: `pipeline/local-rail/build_s49.py` writes `S49 Hostivař Roztoky.html`. Artifact: https://claude.ai/artifact/EVZrB7zSxCzxEU2rGfsaLk
- One line, every 30: Hostivař :03 / :33, Roztoky :15 / :45, 3 vehicles.
- The off-peak Libeň – Roztoky short trains are listed, not modelled.
- vagonweb has no composition for these trains.

**Why:** the user names lines by their PID/ČD label, and CIS JŘ encodes PID lines in the service number. S-line = 1000 + number (S8 = 1008, S49 = 1049, S88 = 1088). R-line = 1100 + number (R49 = 1149). R18 = svc 18.

**How to apply:** when the user gives a line label, find it by service number in the data. If the request is ambiguous, ask before editing; don't rename things on archived sheets. Related: [[rail-design-rules]].
