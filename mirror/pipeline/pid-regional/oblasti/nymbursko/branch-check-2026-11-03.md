# Branch re-check, PID Nymbursko, 3 Nov 2026

Re-check for the systemic error the owner found on 381 Zásmuky (short workings and branches filed as "off the pattern" or
"buses going home" because trips were grouped by start and end stop). Work queue: the passing audit of 3 Nov
(`../../audit-passing-2026-11-03-before.txt`): 2 EACH WAY flags (430, 705) and 3 ONE WAY flags (432, 436, 585).

**Method.** Each flagged line was read at the stops its trips pass (`data/derived/trips.json`, `reading/<L>.txt`), not by
where they start and end: every trip of the line passing the flagged stop 13:00–19:00, both directions, with its time at that
stop, marked by whether a modelled slot of the line meets it within 3 min (`*` below = none does). A second pass counted, for
every line of the sheet, the afternoon trips by their two ends and, for every modelled leg, the trips it carries that end
short of or start after the leg's ends: no group of 3 trips with other ends turned up that the cards do not already name. A last pass looked for a repeating minute
(period 60, 120, 180 or 240 min, tolerance ±3 and ±6 min) among the off-pattern trips at every stop of every line: no line has
3 off-pattern trips each way at one repeating minute. The 2 Nov live map plates are quoted where they decide a chain.

**Result: no missed branch in this oblast.** The two EACH WAY flags are irregular short trips and a phase change, the three
ONE WAY flags are two lines' own hourly pattern in another phase (432, 436) and a sparse line (585). `lines.json` is unchanged; the five cards already name
every trip below (checked against the builder's off-pattern lists in `schedule.json`).

## Per flagged line

### 430 Lysá nad Labem – Milovice – Lipník: EACH WAY (4 each way, 5 one way at Milovice, železniční stanice) → C, with B for the early phase
Times at Milovice, železniční stanice, 13:00–19:00 (`*` = off every slot):
- towards Lysá: 13:10*, 14:10*, 14:30*, 15:25, 15:55*, 16:25, 17:25, 17:55*, 18:25
- towards Lipník: 13:40*, 14:25*, 14:55, 15:25*, 15:55, 16:55, 17:25*, 17:55, 18:55

What the starred trips are:
- **Phase before 14:00 (B):** Lipník 12:52, 13:52 (:52, hourly) and Lysá 13:16 (and 12:16) are the line's own hourly pattern
  in the phase before the timetable changes to Lysá :36 / Lipník :07 at 14:36 / 16:07 (the same step as 436's :10 → :20).
- **Lysá :01 via Park Mirakulum:** 14:01 (ends Milovice, železniční stanice), 15:01 (runs on to Lipník), 17:01 (ends
  Milovice, Balonka), 19:01 (just outside the window). Same minute, but three different ends and only two real short
  workings inside 13:00–19:00 (14:01, 17:01).
- **Milovice back to Lysá:** 14:30, 15:55, 17:51 (from Balonka, ≈ 17:55 at the station): minutes :30, :55, :55: no repeating
  minute. The plates show four buses each doing one short round with a 5–30 min wait at Milovice (8568 14:01 / 14:30, 8558
  15:07 from Lipník / 15:55, 8561 17:01 / 17:51, 8553 19:01 / 19:51), not one pattern.

The branch test (≥ 3 each way, 13:00–19:00, repeating minute) fails on the way back (three trips, three different minutes)
and on the way out (two shorts). The stops of these trips are all on 430; the model's way out (:36, direct) skips Tyršova,
Sportovní and Park Mirakulum, which the way back (:07) serves, as the line's `why` says. Card names every trip. **No change.**

### 705 Poděbrady – Kolín – Kutná Hora – Čáslav: EACH WAY (3 each way, 4 one way at Kutná Hora, Karlov, Na Rovinách) → C
Times at Kutná Hora, Karlov, Na Rovinách:
- towards Poděbrady (Čáslav → Kolín): 13:24, 13:54*, 14:24, 14:54*, 16:24, 17:24, 18:29*
- towards Čáslav: 13:06*, 13:36*, 14:06*, 14:36, 15:36*, 16:36, 18:36

The starred trips: the **Kolín – Kutná Hora short trips**. Out of Kolín 12:20 (bus 8687, Karlov 13:06), 13:20 (bus 1604, Karlov
14:06), 16:20 (bus 1604, to Kutná Hora, autobusové stanoviště); back 13:54 (bus 8687, on to Poděbrady), 14:54 (bus 1604, Kolín
15:40), 17:05 (bus 1604 from the bus station, Kolín 17:40). Three out and three back over the day, but the minutes do not
repeat (:20 / :20 / :20 with a 3-hour gap; :54 / :54 / :05) and bus 1604's rounds are 94, 86 and 45 min. Read at Karlov
only two pairs pass (the third pair uses the bus station); read at Kolín, nádraží, 13:00–19:00, three come back (14:50, 15:40,
17:40) against two out (13:20, 16:20). Not 3 each way at a repeating minute → irregular. The other starred trips are through
trips off their slot: Kolín 12:50 → Čáslav, Kolín, PZKO-TOYOTA 14:32 → Čáslav, Čáslav 18:01 → Volárna, Poděbrady 12:52 and
16:36. All named on the card; every stop is on 705 / 705 Kolín. **No change.**

### 432 Lysá nad Labem – Mladá Boleslav: ONE WAY (2 each way, 3 one way at Mladá Boleslav, autobusové stanoviště) → B
Lysá 11:46, 12:46, 13:46 (hourly :46 before 14:00), Mladá Boleslav 11:48, 12:48, 14:33 (and 19:33 to Milovice): the line's
own hourly pattern before the change to every 2 h (:01 / :03 from 14:03 / 16:01, exact in the window) and one extra; same
path, no branch. Card says it. **No change.**

### 436 Nymburk – Lipník: ONE WAY (2 each way, 3 one way at Čachovice, železniční stanice) → B
Nymburk 13:10, 14:10 (:10 before 15:00, :20 from 15:20), Lipník 13:15, 14:42 (via Všejany), 15:16 (5 min off the :21 slot).
The 15:16 is the hourly trip five minutes early, not a branch; 14:42 is one trip over stops of 432. Card names all.
**No change.**

### 585 Poděbrady – Jičín: ONE WAY (1 each way, 3 one way at Vršce, farma) → C
Jičín → Kopidlno 15:35, Jičín, železniční stanice → Chroustov 18:30, Kopidlno → Jičín 13:02, and the slot trip Jičín 16:35 →
Poděbrady (path via Vršce, explained in the `why` and by the path audit). A line of 2–3 trips a day each way; the shorts are
listed on the card, 18:30 is the recorded coverage exception. **No change.**

## Other cards checked
`lines.json` has no "going home", "garage", "outflow", "outstation" or "sleep" claim; the through-running claims on the
cards (433 → 434, 497, 538 → 541 …) are chain statistics, not reasons for an off-pattern trip.

## Summary

| Line | Verdict | Change | Buses before → after |
|---|---|---|---|
| 430 | C (B for the pre-14:00 phase) | none | 3 → 3 |
| 705 | C | none | 3 + 2 → 3 + 2 |
| 432 | B | none | 2 → 2 |
| 436 | B | none | 2 → 2 |
| 585 | C | none | 2 → 2 |

Oblast total (sum of the builder's needs, 37 Simutrans lines): **68 → 68**.

## Audits after `run_oblast.py nymbursko` (identical to the run before the re-check)
- Step 4: 81 timed legs, 81 ok, no failing leg.
- Branch audit: 12 legs read at a midpoint, all ok.
- Path audit: 1 flag, 585 Jičín 16:35 (off-path stops Žitětín, Labouň, farma, ObÚ, Cholenice): the 16:35 runs via Vršce and
  those stops are on the way out; the `why` says so.
- Passing audit: 2 EACH WAY + 3 ONE WAY, each explained above.
- Coverage: unchanged (one explained exception, Jičín, železniční stanice).

## Could not decide
Nothing in this oblast.
