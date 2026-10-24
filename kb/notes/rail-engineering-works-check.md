---
name: rail-engineering-works-check
description: "Rail sheets: CIS JŘ annual data has no engineering works — check pid.cz/zmeny and ČD výlukové JŘ; model long-term works, skip ones ending soon"
metadata:
  node_type: memory
  type: feedback
  originSessionId: e9b5fede-a5b9-4e20-aab2-33579bfb8991
  modified: 2026-10-14T15:08:06.949Z
---

The CIS JŘ annual data (`trains.json`, downloaded 29 Sep 2026) has no engineering-works variants. On 14 Oct 2026 the user caught it: "don't they end at Praha-Bubny because of engineering works? Isn't some of this true for the other lines". Masarykovo nádraží was closed 1 Jun – 12 Dec 2026, so S5/R45/R24/S54 ended at Praha-Bubny and R24/R45 also stopped at Výstaviště. I had published the sheet with Masarykovo.

User decision, same day: "don't do those ending in early november, do include the Masarykovo one".

**Why:** the user builds the current state in the game; a stale terminus means redoing lines.

**How to apply:**
- Before presenting any rail sheet, check pid.cz/zmeny/?type=vlaky (it lists each change with dates). For lines outside PID, check the carrier's notices.
- ČD works timetables are at `https://www.cd.cz/jizdni-rad/tratove-jizdni-rady/files/cz-k<KJŘ>-2026vyluka<NN>.pdf`. Read them with pymupdf word coordinates, because pdftotext -layout misaligns the columns.
- Model works that last many months, as with the Prague tram rule. Leave the regular timetable for works that end within a few weeks, and list both kinds on the page.
- The Masarykovo works timetable kept the annual minutes from Bubny onward.

Related: [[rail-design-rules]], [[s5-to-s4-corridor]], [[prague-tram-peak-fleet]].
