---
name: evening-courses-and-pairs
description: Type history must leave out late-evening courses and keep coupled pairs as pairs; check raw records before trusting a type share
metadata:
  type: feedback
---

User caught it on 18 Oct 2026 ("solo trams are not working on line 7"; "1359 … highly likely it was 2 Varios coupled. Make sure your research is correct"). The Ostrava sheet had put single Vario LF cars on 4, 7 and 8. Their history came from 9xx evening courses (out to the night lines 18/19), and the roster code had split coupled pairs into singles. In the day records, 1359 ran as 1360 + 1359.

**Why:** a weighted type share mixes all-day records; evening and night runs use different (short) vehicles than the 16:00 peak.
**How to apply:** for any city, before trusting a type on a line, look at the raw records by course group and by single vs coupled. Leave out evening and night course groups. Never collapse a recorded coupled pair to a single. When correcting a published sheet, rebase on it and swap only the wrong units (Ostrava `04b_rebase.py`), since the owner has already built those trams in the game. Coupled pairs do run, e.g. on Ostrava 1/2, so keep them where the records show them. Related: [[ostrava-tram-vypravenost]], [[designed-vehicles-roster-rule]], [[prague-tram-peak-fleet]]
