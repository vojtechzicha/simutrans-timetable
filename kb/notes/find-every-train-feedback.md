---
name: find-every-train-feedback
description: "Rail lines: inventory every train at every station of the line (short workings, shuttles), never search by termini only; whole minutes only"
metadata:
  type: feedback
---

When designing a rail line, list every workday train that serves any station of the line, grouped by the stretch it runs. Do this before presenting anything. Each stretch must end up modelled or listed under Not modelled.

**Why:** on 5 Oct 2026 I searched only by the termini. That missed the 014 Kolín – Uhlířské Janovice peak trains and the 235 Kutná Hora hl. n. – město shuttles, which the user caught from memory. It also missed the 012 Pečky – Bošice/Plaňany trains. The user asked "Why have you not found them at the start? Can you update your procedures?"

**How to apply:**
- Use `inventory()` from `pipeline/local-rail/build_012_014_235.py`. It stops the build on undecided stretches and adds the coverage table to the page.
- The rule is written into `pipeline/rail-design-rules.md` §1.
- Watch for train numbers that have several date variants in the data; pick the one that runs on the modelled workdays.
- Show whole minutes only, never ½: the game can't do half minutes.

Related: [[rail-design-rules]], [[local-rail-012-014-235]].

**13 Oct 2026, second miss:** the user said "I'm missing trains to Rožmitál". Březnice – Rožmitál has only weekend and holiday trains, in season, so a workday inventory of the line's own stations can't see it. At every junction, also list trains on any day that touch only one station of the sheet. Rule §1 in `pipeline/rail-design-rules.md`.
