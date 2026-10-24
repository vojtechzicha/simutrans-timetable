---
name: r49-benesov-local
description: "R49 + Benešov local trains sheet (9 Oct 2026): R49 every 60, 223 Sedlčany, 222 Vlašim, 220 Os circuit; 11 vehicles; pipeline/local-rail/build_benesov.py"
metadata:
  type: project
---

On 9 Oct 2026 the user asked to "archive all" (both local sheets went to `archive/`, see [[local-rail-012-014-235]] and [[posazavsky-pacifik-210-212]]). They then asked for R49 plus the local trains around Benešov: Sedlčany, Vlašim, and "other services south of Benešov and North of Tábor".

**ARCHIVED 9 Oct 2026** (user: "you can archive"). The page is in `archive/`, and the script writes there; the artifact is left at version 6.

Script: `pipeline/local-rail/build_benesov.py`, which reuses `build_012_014_235.run()`. Output: `Local Trains R49 Benešov.html`. Artifact: https://claude.ai/artifact/C1sFtgu1AKdCo28ce8FNeb

Lines:
- R49 (final after three rounds, 9 Oct):
  - Hourly Holešovice :05 / hl. n. :15. Every other train goes to Tábor: R49 Tábor, every 120, in the even hours (Holešovice S:05, Tábor S:05), 2 vehicles.
  - The odd hours turn at Olbramovice: R49 Olbramovice, every 120, 2 vehicles.
  - User: "continue to Tábor every 120mins - making it far from the local train". Even hours keep R49 31–39 min from the 220 Os.
  - The user called the result "good enough".
  - Out of Praha via hl. n. Back, R49 Tábor takes the Malešice bypass to Holešovice (Sp 2478 minutes; user okayed it because it's in the data). R49 Olbramovice comes back via hl. n. (Sp 2474), so hl. n. keeps an inbound R49 every 2 h.
- User quotes:
  - "R49 is clearly hourly between Praha hl.n. and Benešov u Prahy in afternoon peak. You know better about the holešovice mess and what to do after Benešov."
  - Earlier: hourly to Tábor was "a lot of trains (even R17 hourly)".
- Lesson: frequency comes from the afternoon peak in the peak direction (here outbound from Praha). Thin the outer section with short workings to a real short terminus. Don't average over the whole day, and don't make the user ask twice.
- 223 Sedlčany: every 60, 3 vehicles, reverses at Olbramovice.
- 222 Vlašim: every 60, 2 vehicles.
- 220 Os circuit Tábor – Olbramovice – Votice: every 120, 2 vehicles.

Not included (open points to raise with the user):
- R17 Praha – Tábor – České Budějovice.
- S9.
- The Os from České Budějovice, Veselí and Jindřichův Hradec that turn at Chotoviny, one stop north of Tábor.

**Why:** the user decides these scope questions.

**How to apply:** read the user's feedback on R49 every 60 and on the excluded services before changing `LINES`. Related: [[rail-design-rules]], [[find-every-train-feedback]].
