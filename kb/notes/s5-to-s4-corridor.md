---
name: s5-to-s4-corridor
description: "Trains S5 → S4 sheet (15 Oct 2026, artifact v8, 29 vehicles; U12 cut at Most = game track end; U13 Most – Žatec západ in full): S5/S45/R45/S50/R24/S54/S40/S44 + S57/U12/U13/Lužná (cut at Blatno u Jesenice) + Straškov; build_s5.py; S57/U12/U13 hourly; 4021 every 72"
metadata:
  node_type: memory
  type: project
  originSessionId: e9b5fede-a5b9-4e20-aab2-33579bfb8991
  modified: 2026-10-14T14:45:11.554Z
---

On 14 Oct 2026 the user asked: "Now do the S5 (included) to S4 corridor (excluded)", following [[s75-beroun-rakovnik]] (S75 sheet left as is, not archived).

**Scope (user answers, 14 Oct 2026):**
- PID core: S5, S45, R45, S50, R24, S54, S40, S44. Non-PID, all chosen: Rakovník – Blatno (1057), Rakovník – Most – Osek (4012), Lužná – Žatec – Jirkov (4014), Vraňany – Straškov (4022), Roudnice – Bříza obec (4021).
- **Game track ends at Blatno u Jesenice** ("The track ends in Blato u Jesenice, rest should be in full").
- 4021 has no clock-face; user chose **every 72** (1 vehicle), offset = (time − 60) mod 72.
- Out: S4 itself, Kralupy – Neratovice (1043), Louny/Žatec/Chomutov/Most onward lines.

**Sheet:** `pipeline/local-rail/build_s5.py` → `Trains S5 to S4.html`; artifact https://claude.ai/artifact/9V24sqWFpnjztqobgL1CLP (v3: S5 + S45, R45, R24 at Praha-Bubny for the Masarykovo closure to 12 Dec; early-November works not modelled, see [[rail-engineering-works-check]]). README section has the full table. Choices I made (user not yet asked): S40 Louny separate from S40 (types differ).

**v4 (14 Oct 2026):** the user, relayed by the pak128 session, asked to "simplify the S57 and U12 lines - pick the best pattern to be more uniform". The user's names: S57 = 1057 Rakovník – Blatno u Jesenice (the user said "to Blatná" but meant Blatno), U12 = 4012 Rakovník – Osek město. Both now run every 60 on one real pair that crosses at real crossing stations each hour. S57 is 16716 :48 / 16773 :53, crossing at Oráčov, 2 vehicles; the alternative is 16774 / 16719. U12 is 6714 :12 / 6707 :30, 5 vehicles. `check_meetings.py` checks single-track meetings for any pair.

**Why:** the user wants uniform lines over 2-hourly circuits through every real family.

**How to apply:** prefer one uniform pattern on real trains that cross at real crossing stations, and check it with check_meetings.py.

**How to apply:** wait for user feedback on the choices above; rules in [[rail-design-rules]], [[find-every-train-feedback]]. Followed the same day by [[ex7-r17-veseli]].

**15 Oct 2026, U13 added (sheet v6, artifact v8, 29 vehicles):** the user asked "then add to it U13 in full?". U13 = CIS 4013 Most – Žatec západ (KJŘ 123, RegioJet ÚK 654), the whole line, hourly on Os 6519 :42 / 6520 :30. The trains cross at Volevčice, with timing points at Obrnice (out) and Počerady (in); 5-min real turn at Žatec západ; 2 vehicles. The save had an empty Os123 [U13] line. R25, U52 and 4011 share the track but are not on the sheet. U-line numbers = CIS 40xx (U12 = 4012, U13 = 4013, U14 = 4014).
