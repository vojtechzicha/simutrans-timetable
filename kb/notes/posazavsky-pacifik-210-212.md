---
name: posazavsky-pacifik-210-212
description: "Posázavský pacifik 210/212 added 8 Oct 2026 to the 012/014/235 sheet (same artifact); 6 lines, 15 vehicles; open questions for the user"
metadata:
  node_type: memory
  type: project
  originSessionId: 294c6d25-bab6-48aa-ad87-d14e632837cf
  modified: 2026-10-08T21:23:32.453Z
---

**ARCHIVED 9 Oct 2026** together with the 012/014/235 sheet (`archive/`).

On 8 Oct 2026 the user asked to "build on this strong foundation, keep me the Kutná Hora ones shown and do all Posázavský pacific ones in the same guard". I read that as: add 210 and 212 to the same sheet and artifact as [[local-rail-012-014-235]], and keep everything that was already there.

Script: still `pipeline/local-rail/build_012_014_235.py`. It now writes `Local Trains 012 014 210 212 235.html`; the old HTML was removed. Artifact: same URL, KXnUf8bh9Ck1W2xBiJuSQR (version 5). The README has the table.

Lines:
- 210 Čerčany + Čisovice: circuit, every 240 with Also at (3 slots), 6 vehicles.
- 210 Čerčany + Dobříš: circuit, every 240, 2 vehicles; Dobříš 14:15/18:15 from Praha, 16:06 back.

Both 210 circuits go through Praha hl. n. (in :04 → out :15, in :34 → out :55).
- 212 Čerčany – Zruč: L:16, 2 vehicles.
- 212 Sázava: S:16, 1 vehicle.
- 212 Havlíčkův Brod: every 60, 3 vehicles.

The sheet has 23 vehicles in total.

**User feedback (8 Oct):**
- Dobříš every 2 h was "way too often", so it now has at most one vehicle.
- "Model what happens in reasonable matters": decide one-off workings yourself; don't ask.
- The user believed the Čerčany even-hour trains go to Ledečko. Only the 14:16 does; the 16:16 and 18:16 end at Sázava. The 14:16 814 returns attached to Os 9222. Explained on the page, and 212 Sázava was kept.

- The user asked why Also at wasn't used for Čisovice; it should have been. It fills hours a sparse line leaves free, within one route.
- On 8 Oct the user didn't want long stays at Praha hl. n. I first merged 210 into circuits.
- The user then said: "I AM sure they are not standing at Praha hl.n. for more than 10-20 minutes... If you can find a way without merging the lines, do it." The answer was the empty runs to the sidings in the raw CIS locations (Praha-Libeň), plus depot ends.
- I then built that sidings/depot variant (9 Oct). The user said: "I like the simplified lines before, restore the version before". So the circuits are final.
- Lesson: the user prefers simple game lines over strict realism, once both options have been shown. Offering the realistic variant was welcome.

**Why:** the user prefers sparse, realistic service on minor branches over filling every slot.

**How to apply:** use Also at (interval 240) for uneven hourly patterns before adding lines; offer circuits at big terminals; give minor branch ends the fewest vehicles that still show the real pattern; make one-off moves "Not modelled" with a reason instead of asking. Related: [[rail-design-rules]], [[shared-circuit-vagonweb-rule]], [[find-every-train-feedback]], [[local-rail-012-014-235]].
