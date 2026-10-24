---
name: beroun-plzen-pribram-trains
description: "ARCHIVED 13 Oct 2026. Trains west of Praha sheet: S7, Liteňka, S6/S65, R16, S70, Příbram line, R26, S20; cut at the game's track ends Rokycany/Blatná/Čimelice; 33 vehicles; build_beroun.py"
metadata:
  node_type: memory
  type: project
  originSessionId: 294c6d25-bab6-48aa-ad87-d14e632837cf
  modified: 2026-10-15T17:59:25.539Z
---

On 10 Oct 2026 the user archived all the older train sheets and asked for "S7, Beroun-Plzeň, Beroun-Příbram -> wherever, Liteňka and other trains around it - no need to go north of Beroun and stay west of Vltava". The same day they added S20 Kolín – Havlíčkův Brod, with "only the correct terminus for these trains".

- **Sheet:** `pipeline/local-rail/build_beroun.py` writes `Trains Beroun Plzeň Příbram.html` in the project root. The filename stays, even though the game has no Plzeň.
- **Artifact:** https://claude.ai/artifact/HopRNc92gS41cs9kQ6jroj (v8, 13 Oct; ARCHIVED the same day, file in archive/). The README has the full table.

**Game track ends (user, 13 Oct 2026):** "in game we have some specialities - the tracks end at Rokycany, Blatná and Čimelice". Every line that went further now ends there, at its real minutes. The script uses `cut` legs, and `cut_at` so that through trains still count as the line's real trains. Changes:
- R16 Praha – Rokycany: 3 vehicles. The 7-min turn at Rokycany joins two real minutes; it is not a real turn. The alternative is 4 vehicles.
- S70 Beroun – Rokycany: 2 vehicles, 1 h 54 min at Rokycany.
- Os Hořovice – Rokycany: 1 vehicle.
- S60 Beroun – Blatná, on the real Blatná trains: 2 vehicles.
- Os Březnice – Čimelice: 1 vehicle.
- R26 Praha – Čimelice, keeping the Malešice depot runs: 4 vehicles.
- Dropped: the Plzeň Sp shuttles, Blatná – Strakonice, and Rokycany – Příkosice. I assumed the Mirošov branch isn't built and haven't confirmed it; the README has the recipe to restore it.

Total: 43 → 33 vehicles. Then the user asked for Rožmitál, and I added it as a `season` line. It has no workday trains, only weekends and holidays from 25 Apr to 28 Sep. The user then said "If rožmitál has no weekday service, it should not be in", so in v8 it is listed under Not modelled and the total is 33 again. The user's verdict on the sheet was "otherwise great work". S7, S7 Řevnice, S76, S6, S6 Nučice, S65 and S20 are unchanged.

**Earlier user decisions that still hold:**
- R26 runs from and to the Malešice depot (1 h at Praha hl. n. was too much).
- Liteň is timed both ways (reversal, 11 Oct).
- S20 has two termini, Havlíčkův Brod and Čáslav.

**15 Oct 2026 (reopened):** S6 is one combined line (Beroun + Nučice). The final Smíchov S6 counts in the total (31). The works version "S6 until 19 October" (Praha-Zlíchov) has its own full section, because the user asked "why isn't there big table for S6 befor the end of works?". It is a `temporary` line with the same vehicles, not counted. When a line has a works state and a final state, show both in full, not one squeezed into a note. Artifact v11.

**Ex6 added 15 Oct 2026 (v12, 35 vehicles):** two lines every 2 h, Ex6 Cheb (IC Západní expres) and Ex6 München (EC / alex). They run Praha-Vysočany – Praha hl. n. – Rokycany (the real trains pass Rokycany without stopping), with 2 + 2 vehicles. S70 is timed at Hořovice for the overtake. Rokycany holds up to 3 trains. The game save had Ex6/1–Ex6/4 placeholder lines with no vehicles. The user said "the latest file"; I took it to mean this sheet, the one updated last that has the Rokycany line, not the S4 one.

**How to apply:**
- Treat Rokycany, Blatná and Čimelice as hard ends for any future line in this area.
- The sheet was archived without answers on the R16 7-min turn at Rokycany, the Příkosice branch, or R16 via Holešovice. Don't chase them unless the user reopens the sheet.
- R16 never reaches Vysočany. A turn as Sv to Holešovice can't be checked: CIS JŘ has no Sv trains, so it needs real times from the user.
- Same rules as [[rail-design-rules]] and [[find-every-train-feedback]].
