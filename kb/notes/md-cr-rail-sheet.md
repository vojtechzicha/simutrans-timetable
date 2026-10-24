---
name: md-cr-rail-sheet
description: "MD-CR = all Czech long-distance trains (R/Ex/IC/EC/SC/rj/RJ/LE) grouped by peak line, timetable only; pipeline/md-cr; practical standards, foreign termini, long stops"
metadata:
  node_type: memory
  type: project
  originSessionId: 6267b721-9c15-412a-9404-df5b62b00871
  modified: 2026-10-04T14:27:38.281Z
---

**ARCHIVED 5 Oct 2026 (user: "archive all these").** The page moved to `archive/MD-CR.html`, the renderers write there, and the artifact is left at version 16. Don't work on it unless asked. The open points are in the README banner.

MD-CR.html in the project root, artifact https://claude.ai/artifact/DH4KCxqbx1KLvVvnxUNAQL, pipeline in `pipeline/md-cr/`.

**v4 (3 Oct 2026) is current.** It is the simplified, game-friendly design the user asked for: 8 clock-face lines (120/240) and 29 vehicles. Each operator leaves Praha every 2 h and alternates its branches.
- **Lines end at the first station after the border.** That station is the game end for the city beyond: Čadca for Žilina/Košice, Chałupki for Warszawa, Zebrzydowice for Kraków, Púchov for Ex2.
- **Vehicles are counted on that basis.** The user cared that Ex1 Poland and Ex1 Slovakia come out equal; they do, at 3 each.
- **Offset convention:** (real − 60) mod interval, confirmed for 240.
- **The EC Ostravan stays on Ex1, not on SC.** IC 503/504, rj 512/515 and SC 500 are part of the SC slot. JR2026 has no long-distance stop at Ústí nad Orlicí město; the user remembered an older Ex1 stop.
- **Brno pass (4 Oct 2026).** Added Ex3 Budapest via Bratislava and Ex3 Wien (every 120), RJ Budapest via Wien and RJ Bratislava (every 240), and LE Bratislava (every 480). Total 44 vehicles.
  - South ends (user): real times to Kúty or Hohenau, then 10 min per station: Kúty – Bratislava – Budapest, Hohenau – Wien – Budapest.
  - LE Bohumín became every 480 and alternates with LE Bratislava.
  - Not included, by the user's choice: Ex4, the R lines (R9/R19/R18), and the Ex3 north through trains.
- **Stop before Brno hl. n. (user, 4 Oct 2026).** On lines via Brno, the stop before Brno hl. n. gets a timed entry in each direction (`time_before` in `v4_lines.json`). **Never** move Brno's stay onto that stop. One session cut Brno to 1 min, and the user called that a misunderstanding. Brno keeps its real stay and is timed if the stay is 5 min or more.
- **R9 and R19 added (4 Oct 2026).** Both run every 120 and start and end at "Praha/Brno odstavné nádraží", 15 min beyond the hl. n. (user rule, `depot`). There is also my recommended branch, R9 Havlíčkův Brod – Brno every 240 (the off-hour and peak R9 trains), which the user may drop. The total is now 57 vehicles.
- **Focus on rychlíky + Leo Express (user, 4 Oct 2026).** Ex/SC/RJ lines are hidden on the page (`hidden` flag) and frozen: **never edit them**. LE is shown again, unchanged.
- **R lines: important stations only**, never every stop (rejected). Real termini are timed both ways: Praha-Vršovice (real depot runs from Praha Jih) and Brno hl. n. (depot 15 min, dwell included). No invented dwells; check the raw locations for depot runs. R9 times Kolín, Havlíčkův Brod and Tišnov.
- **Check the user's in-game entries before blaming offsets.** The LE 207-min delay came from Bratislava/Kúty typed as 240 instead of 480. The fork source counts slots from midnight; the sheet's −60 convention is user-confirmed, so mention the source but don't change the convention.
- **Leo Express must turn at Praha hl. n. in 20 min at most** (user, 4 Oct 2026). The LE returns are modelled 35 min earlier than real (`slot_B` plus `max_turn_A` in `v4_lines.json`). The total is now 27 vehicles.
- The design is in `assets/v4_lines.json`, built by `13_simple.py` and `12_render.py v4`.

**v3 (earlier the same day, replaced by v4).** It is built with [[rail-design-rules]] (scripts 10–12, design in `assets/v3_lines.json`). It covers only the trains via Ostrava (ČD Ex1, SC, RegioJet, Leo Express) plus Ex2, and Brno trains come in a later pass. Foreign ends are Warszawa, Kraków, Žilina and Košice only, timed from the first station after the border, with foreign times from vagonweb.cz and leoexpress.com. Sparse lines use interval 1440 with Also at; the user still has to confirm the offset convention (I assumed real − 60). Total 38 vehicles. The v2 notes below are history. The README holds all the rail rules and the update recipe. Built 2026-09-29, v2 the same evening.

The user wanted all R, Ex, IC, SC, rj and EC trains, plus RegioJet, Leo Express and other commercial trains, grouped by peak line. They asked for no local trains and **no fleet** (timetable only).

User feedback on v1 (29 Sep), which v2 follows:
- **Be practical:** no single-hour fit. Give each end the common clock-face standard across the afternoon (1/2/4 h, ±5 min).
- **Ex1 is Praha – Bohumín – Warszawa, not the route via Karviná.** Rychlík trains filed under an Expres number get their own line.
- **Handle branches like the city sheets, after asking the sessions.**
  - Chaining at the shared terminus decides: none alternate strictly, so all are branch lines.
  - Threshold: ≥3 trips 12–20 h, a departure 14–18 h, and a clock-face rhythm.
  - Tails: their minute is folded into the line, and they are listed visibly.
- **Design lines to the most common foreign terminal.** The foreign entry gets Departure every 0, and trains are held at the last Czech station.
- **Flag long stops per direction, with fork values** (passenger stops ≥5 min, no-passenger stops ≥2 min, border stays) so they aren't forgotten.
  R17 at Tábor is only 2 min in JR2026; the long R17 stop is Veselí nad Lužnicí (11–22 min).
- **One headway per line from both ends together** (Kysučan is 4-hourly; the busier end alone made it 2-hourly). Judge it on the afternoon, not the whole day, or peak-hourly lines like R9 drop to 2 h.

**Why:** this is the rail layer of the Simutrans transformation, next to [[regiojet-rail-sheet]] and [[leoexpress-rail-sheet]].

**How to apply:**
- Grouping uses `CZPassengerServiceNumber`, the state line number.
- Rail termini keep the real minute (no loop rule).
- "Leave up to" is 30 min at headways over 60.
- The sheet needs a JR2027 refresh after 13 Dec 2026.

Related: [[simutrans-fork-schedule-spec]].
