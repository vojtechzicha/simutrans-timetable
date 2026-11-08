# Kutnohorsko: review of the branch re-check (3 Nov 2026, Fable)

Independent of the designer's notes. Method: `BRANCH_BRIEF.md` "For the reviewers". The diff against v1
(`mirror/pipeline/pid-regional/oblasti/kutnohorsko/lines.json`) is the coordinator's 381 (`381 Zásmuky`, note, why) plus the
designer's `window` on it. Every EACH WAY and ONE WAY flag of `audit-passing-2026-11-03-before.txt` was re-derived from
`data/derived/trips.json` with my own reader (same coverage rule as `audit/passing_check.py`, each stop at the trip's first
passing), plus a scan of every stop of every line for uncovered trips repeating at one minute (±3) three times each way; the
"going home" claims (381, 387, 402, 771) checked by the passing reading. Plates: `scripts/observed.py` for 381 and 805 on 2 Nov.
Both reruns of `run_oblast.py kutnohorsko` (before and after my edit) are clean.

## 381 Zásmuky — PASS (A, the coordinator's; one clause added)
Legs: Háje :30 → Zásmuky, náměstí with `notvia` Bečváry counts 6:30, 14:30, 15:30, 16:30, 17:30 and 0:05 only, no Čáslav or Kutná
Hora trip; Zásmuky :21 → Háje with `notvia` Čáslav, Kalabousek counts the Kutná Hora starts (5:21, 7:21, 11:51, 14:21, 15:21,
22:51) and the Zásmuky starts (4:21, 4:51, 16:21), no Čáslav trip; 381's own legs count none of the branch trips (10/10/11 and
11/12/12). Window 15:00–17:00: 15:30, 16:30 / 15:21, 16:21, all exact; read at Zásmuky, náměstí every afternoon trip now sits on a
slot (:09 / :39 out, :21 / :51 back). Running times 69 / 69, 3 buses. Changed: the `why` now says why the window is 15:00–17:00
(the branch's own hour; its last return is 16:21), which the designer's edit did not.
On `lay` 0 at Háje: on the 2 Nov live map the real turn is a 30-minute one across the two lines (1683 and 9373 arrived from
Čáslav at :00 and left at :30 for Zásmuky; 9372 arrived from Zásmuky 17:30 and left 18:00 for Čáslav), as the card says. Pooled,
381 + 381 Zásmuky run 9 buses (540-min cycle); separate with lay 0, 5 + 3 = 8; with 3-minute waits 6 + 4 = 10. The card gives both
counts (3, or 4 with a 3-minute wait); the worked example of the brief, not changed.

## EACH WAY flags
**805 — FIX (card and owner-check text; verdict C stands).** Whole day at Kolín, nádraží: departures towards Kutná Hora at :53–:58
nearly every hour (4:53, 5:57, 6:58, 7:53, 8:57, 9:53, 10:57, 12:57, 13:57, 14:57, 16:57, 17:53, 18:57), the end alternating (Zruč
10:57, 12:57, 14:57, 16:57; bus station 7:53, 9:53, 13:57, 17:53, 18:57, 19:23), with 15:27, 16:03 (Karlov) and 16:27 in place of
15:57. Read at Hlouška, Na Špici 13:00–19:00 with every trip that passes it: towards Kutná Hora 13:19 Z, 14:19, 15:19 Z, 15:49,
16:29 K, 16:49, 17:19 Z, 18:19 (Z = Zruč, modelled; K = Karlov): the uncovered 14:19, 15:49, 16:29, 16:49, 18:19 have no three at one
minute inside the window (the 18:57 from Kolín passes at 19:19). Towards Kolín 13:11, 13:41 (bus station 13:06, 13:36), 14:31,
15:01 (Karlov 14:19, 14:49), 15:31 (bus station 15:26), 15:51 Z, 16:51 Z, 17:31 (Karlov 17:19), 18:31 Z: the shorts repeat at :31
three times (14:31, 15:31, 17:31), but from two ends and from the bus station alone at no fixed minute. The brief's test (three each
way at a repeating minute) holds one way only, so C and the +1 owner option are right; the card and the check said "no repeating
minute", which was wrong for the way back. Changed: the note and the owner check now state the Na Špici reading (:31 three times
towards Kolín, no three at one minute towards Kutná Hora within the window). Plates: 7602 runs 13:57, 15:26, 16:03, 17:19, 18:57
(one bus shuttling Kolín – Kutná Hora, with a 536 trip at 13:32); 7614 and 7610 (785 / 786 buses) run 14:19 → 15:27 and 14:49 →
16:27; 7552 (Zruč 15:40) runs 17:53. If the owner wants Kolín → Kutná Hora hourly in the game, as the :57 trunk is in reality,
the owner-check option (805 Kutná Hora every 120, Kolín 13:57 / bus station 15:26, 1 bus) is the way.

**781 — PASS (C).** At Žleby, náměstí the uncovered trips are 14:01, 16:01 (Okřesaneč → Čáslav, the 740 buses), 17:08 (Žleby
short), 16:12 (Čáslav 15:50 → Žleby) and 18:42 (18:18 → Kamenné Mosty): four ends, :01 only twice. `781 Potěhy` 13:07, 15:07,
17:07 exact (its way back is the 741 ring).

**742 — PASS (C).** Čáslav :13 hourly 15:13–18:13 to Ledeč, Zbýšov, Třebětín and Žáky (Žáky :25 four times); back 13:13, 14:38,
15:43, 16:48, 18:28 drifting 5 min an hour (no three within ±3; every 60 would fail Step 4 on the way back, 1 of 2 within 3 min).
The every-120 model (16:13 → Zbýšov; Podolí 14:45; `742 Dobrovítov` 13:38 / 14:18) is what passes; the card names the rest.

## ONE WAY flags
- **533 — PASS (C).** Žiželice 13:04, 15:04 / Chlumec 13:40, 15:40, exactly every 120 but two each way 13:00–19:00 with no third
  (17:16 is the trunk 20 min late); one 536 bus (7592).
- **783 — PASS (B; clean after the audit fix).** Trunk 16:06, 18:06 / 16:43 are 10 and 5 min off the every-120 slots (12:16,
  14:16 / 12:48, 14:48); Žehušice 13:48 / 14:10 the earlier pair; named.
- **782 — PASS (B).** 12:46, 13:46, 14:39 (from Žižkov) and 13:48 are 4–5 min off the :41 / :43 slots; named.
- **402 — PASS (D).** At Zruč nad Sázavou, Sázavan towards Prague 14:19, 15:19, 16:19, 18:19 (all from Čáslav :36); towards Zruč
  13:41, 15:41, 16:41 (Roztyly 15:20, ends), 17:56 (16:35), 18:56 (17:35, ends). The Zruč-ending trips have no afternoon return:
  the card's "going home to Zruč" holds; 14:36 and 16:35 named. Outside this re-check: Čáslav :36 runs 13:36, 14:36, 15:36, 17:36
  and the model is every 120 (3 buses); an hourly 402 would pass Step 4 in a 13:30–15:30 window at 5 buses, the v1 design choice,
  not changed.

## Other "going home" claims
- **387 — PASS.** Towards Prague 13:12, 14:57, 15:57, 17:12 against Háje :10 hourly; modelled at the inbound rate (two slots per
  120); 14:57 named.
- **771 — PASS.** The 13:00 round is the circuit; the 15:40 and 17:40 to Soběšín end there, the line has no later Soběšín →
  Uhlířské Janovice trip.

## Scan for missed branches
No stop of any line has uncovered trips repeating three times each way at one minute. Nothing missed.

## Result
| line | verdict | review | change by the reviewer |
|---|---|---|---|
| 381 Zásmuky | A (coordinator) | PASS | `why`: one clause on the 15:00–17:00 window |
| 805 | C | FIX | note and owner check state the Na Špici reading (:31 three times towards Kolín, none towards Kutná Hora) |
| 781, 742 | C | PASS | none |
| 533, 783, 782, 402 | C, B, B, D | PASS | none |
| 387, 771 | D claims | PASS | none |

Buses: 70 → 70 (67 of v1 + 3 for 381 Zásmuky). Audits after the rerun: Step 4 86 of 86 ok; branch 4 legs ok; path 2 (481, 746,
as in v1); passing 3 EACH WAY (805, 781, 742) and 3 ONE WAY (533, 402, 782), each with the verdict above.

## Addendum, 3 Nov evening (coordinator, after the owner asked about 402)
The 402 verdict (D) stands. Both files have the passing times at Zruč, but the reason sentence is about where trips start
("Zruč starts 4:24, 6:29 only") rather than the count off the slot. The reason by the passing reading and the plates: at Zruč the every-120 slot passes 14:19, 16:19, 18:19
towards Prague, leaving only 15:19, against 15:20, 16:35, 17:35 out (3 out, 1 back), and on the 3 Nov live map 7925, 7671, 7672 left Zruč at 4:24, 4:36,
6:29 and ended their day there on the 15:20, 17:35, 18:20. The card now says so. See `../../plates-check-2026-11-03.md`.
