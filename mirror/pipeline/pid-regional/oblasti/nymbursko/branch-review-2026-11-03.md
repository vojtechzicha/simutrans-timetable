# Branch review, PID Nymbursko, 3 Nov 2026 (independent reviewer)

Reviewed the designer's `branch-check-2026-11-03.md` against `data/derived/trips.json`, `schedule.json`, the 2 Nov live map
(`scripts/observed.py 430 / 705 2026-11-02`) and `kb/lessons.md`. Every verdict below was re-derived from the trips read at
the flagged stop (every trip passing it 13:00–19:00, wherever it starts or ends), then compared with the designer's. A second
scan of my own ran over every line of the sheet: off-pattern trips at every stop by direction, a search for a repeating
minute (period 60 / 120 / 180 / 240, tolerance ±3 and ±6) with ≥ 3 trips each way, every timed leg's real trips 13:00–19:00
against its slots, and every trip end that is not a modelled terminal.

`lines.json` is unchanged by the designer (diff against v1 in the repo: empty) and unchanged by me.

## Per flagged line

| Line | Flag | My reading at the flagged stop (13:00–19:00) | Verdict | Designer | Result |
|---|---|---|---|---|---|
| 430 | EACH WAY 4 / 5 at Milovice, železniční stanice | Towards Lipník off the :36 row: 13:40 (Lysá 13:16, the pre-14:00 phase), 14:25, 15:25, 17:25 (the Lysá :01 trips: 14:01 ends Milovice, 15:01 runs to Lipník, 17:01 ends Balonka). Towards Lysá off the :07 row: 13:10, 14:10 (Lipník 12:52, 13:52, the :52 phase before 16:07), 14:30, 15:55, 17:55 (Milovice shorts; 17:51 from Balonka). Three :01 trips out, but their returns are 14:30, 15:55, 17:55: two at :55 and one 25 min away. Plates: four buses each doing one short round (8568 14:01 / 14:30, 8558 15:07 / 15:55, 8561 17:01 / 17:51, 8553 19:01 / 19:51), confirmed in `430_observed_2026-11-02.json`. Not ≥ 3 each way at a repeating minute. The closest thing to a branch in this oblast: at period 120 the 15:01 / 17:01 out and 15:55 / 17:55 back are 2 each way, the 14:01 / 14:30 pair is an hour off. Stops of all these trips are on 430 (the :07 way back serves Tyršova, Sportovní and Park Mirakulum). | C (B for the phase before 14:00) | C / B | PASS |
| 705 | EACH WAY 3 / 4 at Kutná Hora, Karlov, Na Rovinách | Towards Čáslav off: 13:06, 14:06 (Kolín 12:20, 13:20 → Karlov shorts), 13:36 (Kolín 12:50 → Čáslav), 15:36 (Kolín, PZKO-TOYOTA 14:32). Towards Kolín off: 13:54, 14:54 (Karlov shorts), 18:29 (Čáslav 18:01 → Volárna, 5 min off :24). The Kolín – Kutná Hora shorts: out 12:20, 13:20, 16:20 (two inside the window), back at Kolín 14:50, 15:40, 17:40 (two at :40). Buses 8687 and 1604 as the designer says. Not ≥ 3 each way at a repeating minute. At Kolín, nádraží the two Simutrans lines together give :50 every hour towards Čáslav (12:50–18:50, as real) and 705 Kolín's :56 / 705's :56 back; the 12:50 Kolín → Čáslav trip sits on that :50 pulse and is flagged at Karlov only because the audit's slot offset there is a median over two Kutná Hora paths (a tolerance artefact, not an off-pattern trip). | C | C | PASS |
| 432 | ONE WAY 2 / 3 at Mladá Boleslav | Lysá 11:46, 12:46, 13:46 (hourly :46 before 14:01) and Mladá Boleslav 11:48, 12:48, 14:33: the line's own pattern in its earlier phase, same path. 2 each way at Milovice (13:04 / 14:04 out, 13:40 / 15:25 back), no third. | B | B | PASS |
| 436 | ONE WAY 2 / 3 at Čachovice | Nymburk 13:10, 14:10 (:10 before the :20 phase); Lipník 13:15, 14:42 (via Všejany), 15:16 (5 min off the :21 slot). No branch. | B | B | PASS |
| 585 | ONE WAY 1 / 3 at Vršce, farma | Jičín 15:35 → Kopidlno, 16:35 → Poděbrady via Vršce (the slot trip, path audit explains it), Jičín, železniční stanice 18:30 → Chroustov, Kopidlno 13:02 → Jičín. A line of 2–3 trips a day each way. | C | C | PASS |

## Sheet-wide scan (my own)
- No stop of any line has ≥ 3 off-pattern trips each way at a repeating minute. Stops with 2 each way: 430 (above), 432 (above),
  436, 497 (Nymburk, nemocnice: Kostomlátky trips 16:35 / 16:39 against 15:18 / 16:04), 679 (Pňov-Předhradí: Velim – Oseček
  13:53 / 15:23 against 15:32 / 15:35), 705 (above). None has a third trip within 6 min of a shared minute.
- Trip ends that are not a modelled terminal, 12:00–19:00: 497 → Kostomlaty nad Labem (12:25, 15:14, 17:44: three ends at
  :25 / :14 / :44, no pattern; the stops are on 497's path) and → Loučeň (16:05, 18:05); 541 Dymokury → Podmoky (14:15, 16:15);
  598 Kopidlno ends (12:35, 15:35); 705 Karlov shorts (above). None ≥ 3 each way.
- Legs where the real rate 13:00–19:00 differs from the slots by ≥ 2 (398, 433 Zálabí, 497, 539, 541, 598, 676, 705 Kolín):
  all are either the other hour carried by the line's second Simutrans line (541 Dlouhopolsko / Městec Králové, 598 Nová Ves /
  Dubečno, 676 / 676 Seletice, 705 / 705 Kolín, 433 / 433 Zálabí) or a line modelled at its busiest two hours as the method
  says (398 every 30 at 15:00–17:00, hourly before and after; 497 and 539 hourly until 16:40 / 16:31). Not branch questions.
- `lines.json` carries no "going home", "garage", "outstation" or "sleep" claim; the through-running statements (433 → 434,
  497, 538 → 541) are chain counts, not reasons for an off-pattern trip. Nothing to check against plates.

## Audits after `run_oblast.py nymbursko` (rerun by me, identical to the designer's)
Step 4: 81 timed legs, 81 ok. Branch audit: 12 legs read at a midpoint, all ok. Path audit: 1 flag (585 Jičín 16:35 via Vršce,
explained in the `why`). Passing audit: 2 EACH WAY (430, 705) + 3 ONE WAY (432, 436, 585), all explained above. Coverage:
unchanged (Jičín, železniční stanice the one explained exception; six stops of other okresy for the `--final` pass).

## Summary
| Line | Verdict | Change | Buses |
|---|---|---|---|
| 430 | C | none | 3 → 3 |
| 705 | C | none | 3 + 2 → 3 + 2 |
| 432 | B | none | 2 → 2 |
| 436 | B | none | 2 → 2 |
| 585 | C | none | 2 → 2 |

No FIX rows. Oblast total: 37 Simutrans lines, **68 → 68** buses.
