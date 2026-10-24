---
name: s4-s3-corridor
description: "Trains S4 → S3 sheet (14 Oct 2026, v2 27 vehicles): S4, S4 Ústí + coupled 2nd unit to Kralupy, R20/Ex5/R15 via Praha Jih, R23 stabled at Ústí západ, R23 full, S32, U32, S43, S23; only lines missing from the game; build_s4.py"
metadata:
  node_type: memory
  type: project
  originSessionId: e9b5fede-a5b9-4e20-aab2-33579bfb8991
  modified: 2026-10-15T17:25:12.731Z
---

On 14 Oct 2026 the user asked to "finish all pid trains and related branch lines with what's missing (it should be the S4 - S3 corridor but some might have slipped up. The main tracks are built all the way to Usti (so include even some fast trains on the corridor to usti)".

**Sheet:** `pipeline/local-rail/build_s4.py` writes `Trains S4 to S3.html`. Artifact https://claude.ai/artifact/UkDVhoRyabQp2EPeQNMKeD (v2). The README has a section on it.

**Scope (user answers, 14 Oct 2026):**
- The east sector was "done manually" in the game. The pak128 session exported the save headless (FORK-CZR-VZ.sve 19:44): `rail_lines.md` lists 161 lines with vehicles. S3, S30, S34, R43, R21, S35, R22, S1, S2, S9, S12, S21, S61, R41 and R42 all exist there, so the sheet adds only missing lines.
- **Fast trains:** R20, Ex5 and R15 are cut at Ústí ("only in praha-usti sense"). R23 runs Kolín – Ústí "in full". "R20, R5/Ex5 should definitely go to Praha jih" (the same depot as Praha odstavné nádraží).
- **S22** "only if they actually have any trains": it has none in the afternoon, so it is not modelled. **S27** is out. **S23** is in.
- **Track:** Mělník – Štětí – Ústí západ, Neratovice – MB and Mělník – Mšeno are built. Mšeno has no workday trains. The Lovosice branches are not built.

**Findings:**
- Ex5 is ČD rj "Berliner". Its Tue–Fri and Monday records have the same Praha – Ústí minutes, so `load()` merges them.
- R23 is RegioJet 665.
- S4 starts at Praha-Bubny. The ČD works timetable gives no S4 times, so it uses the annual minutes.
- R42, built by hand by the user, is affected by the Masarykovo closure: some peak trains start and end at Praha-Vysočany. The user has been told.
- The R24 Bubny minutes were confirmed from the Arriva works timetable (S5 sheet v7).

**v2 user decisions (14 Oct 2026):**
- Bubny holds max 4 trains. A minute-by-minute count shows 2.
- Use the fork coupling at Kralupy. S4 Ústí now has a joining 640.2 line to Kralupy.
- "R15 should go to Praha jih". Its depot runs copy Ex5's minutes in the opposite hours.
- The Ústí depot run takes 11 min and may store trains with long pauses. Then: "R23 in reality goes back to západ to stable", so R23 stables at Ústí západ (3-min empty runs).
- For S4 coupling, the user spun up engine session simutrans-122-0-36. I briefed it with the S4 / S4 Ústí / 2nd-unit timetable and the R18/1–R18/2 regression case, and it aligns implementation details with the user. Its result: the unit line must list the same stops as S4 Ústí (next-stop rule), and the coupling offsets must match. Tested OK with the real minutes. Engine fix cc6f047 (late primary) is committed but not installed. Kralupy needs about one tile of slack beyond one 640.2 at the Ústí end for a same-track coupling, otherwise the unit jumps track (cosmetic). Sheet at v5.
- **15 Oct 2026, v6:** the user built the S4 coupling, and it works at Kralupy. In the game S4 Ústí ran far faster than the real train: it reached Lovosice 21 min early and Kralupy 36 min early. I added real-minute timing points (Nelahozeves, Vraňany, Hněvice, Roudnice, plus Bohušovice inbound). They stop short of where R15 or Ex5 (outbound, overtaking at Lovosice) or R20 (inbound, overtaking at Kralupy) would come up behind S4. Rule: in the game, trains with many short stops run fast, so give long all-stops runs intermediate timing points at stations with passing tracks. U54 (4054) was declined: it has no afternoon pattern, and Hněvice north is a single 5:32 train.
- Coupling ignores pak constraints (pak128 session). The fork parts a pair only where the next stops differ.

**How to apply:** for future corridors, check the game's line list first and ask the pak128 session for an export when the game is closed. Rules are in [[rail-design-rules]]; the previous sheet is [[s5-to-s4-corridor]].
