# Branch check of the regional sheets (25 Oct 2026, after the 292 split)

Owner, on the published Opavsko v8: "looking at 292 I see in peak half of the services going to Chuchelná, half going to
Strahovice, kaple - but you model as one line?" Then, on a side-agent note that other lines are read the same way: "Unless
you'll show me a good reason why you have not modelled this as two branches, do the check mentioned".

There was no good reason. 292's Ostrava leg counted every trip passing Píšť, Mýto (`core_to`), before the fork past Bělá, so
it passed Step 4 with two Strahovice trips while the Simutrans line ended at Chuchelná. 292 is now two lines (Opavsko README,
"292 split"). This file is the check of every other line read the same way, on all five regional sheets.

## Check 1: legs read at a midpoint (`audit/branch_check.py`)

A leg is read at a midpoint when its trips count at a core point short of its terminal (`core_to`) or at a knot past its
start (`knot` + `knot_at`). For each of the 63 such legs, the trips it stands for are classed by where they really end (or
start): at the terminal, on the leg's own path (a short working), **beyond** (it passes the terminal and runs on: the line
is cut where they meet) or **branch** (it never reaches the terminal and ends or starts off the path, which is what hid
292's Strahovice trips). Every window slot is checked the same way.

53 legs are clean. The other ten, and the verdicts:

| Leg | What the check found | Verdict |
|---|---|---|
| HKO 582, both ways (Albrechtice) | Horní Suchá, škola trips | Beyond: škola is 4 min past dvůr on the same road; škola is on 582 ČSM and MHD 413. Fine. |
| TFJ 732, both ways (Český Těšín) | Jablunkov trips | Beyond: they pass Třinec, autobusová stanice; Jablunkov is on 781–783. Fine. |
| **TFJ 314 (Baška)** | 3 of the 4 slots were trips that start or end at Revoluční; the line ended at the station | **Fixed:** the town end is Revoluční (below). |
| **TFJ 340 (Revoluční)** | the 14:12, its only afternoon trip, runs via Kunčice; the modelled way out took the 5:50's path via Hrabůvka | **Fixed:** out via Kunčice (below). |
| Opavsko 246 out (Dolní Životice) | one Hlavnice trip (15:51) | One trip; Hlavnice is on 248 and 259. Fine. |
| Opavsko 263 back (Pustá Polom) | one Hlubočec trip (15:21) | One trip; Hlubočec is on 264. Fine. |
| Opavsko 281 out (Kobeřice) | Strahovice trips 15:48, 16:13 | One way only (buses going home; no 281 trip back from Strahovice); Strahovice is on 255 and 292 Strahovice. Fine, on the card. |
| Novojičínsko 371 out (Hukvaldy) | one Horní Sklenov trip (15:50) | One trip; Horní Sklenov is on 305 (TFJ sheet). Fine, on the card. |
| 314 back, 340 out (after the fix) | the 15:59 slot is the 15:35 trip to the station; the 14:12 ends at Revoluční | Kept: with 15:19 (a Revoluční trip) 314 needs 3 buses, not 2; 340 runs on to Frýdlant for its 12:06 back. On the cards. |

**One branch past a midpoint is listed, not modelled: TFJ 732 to Havířov, Podlesí, Těšínská.** It is read at Český Těšín and
forks in Havířov: Třinec → Podlesí 14:10, 14:15 (pod Kanadou), 15:50 and Podlesí → Třinec 12:25, 13:05, 15:15, 17:30, against
about twice that to Havířov, Město. The reading is right (the Podlesí trips are not counted on the Město line), and every
Podlesí stop is on the Havířov town lines (402, 410, 411, 413, 417), so by Step 8 it is listed on the card. Modelling it is
the owner's choice. A first look, not built: every 240 with two slots each way hits Třinec 14:10 / 15:50 and Podlesí 13:05 /
15:15 exactly; one bus cannot chain them (out 14:10, back 15:15, in at Třinec 16:05, after the 15:50), so about 2 buses.

## Check 2: does each slot's trip run on the modelled path? (`audit/path_check.py`)

The wider question: for every timed leg, the real trip each window slot stands for, and the stops it serves that the
modelled stop list skips. This found 246: its way back took the path through Hertice that skips Dolní Životice, while its
:12 slot stands for the Dolní Životice trips (13:47, 14:47), so in the game nothing ran back from Dolní Životice. **Fixed**
(below).

After the fixes, 51 slots on the five sheets stand for a trip that leaves the modelled path somewhere along the way. These
are path variants (a loop through a village, a detour to a works gate, a different street in town): the line follows the
commonest afternoon path and every skipped stop is on some modelled line (coverage: 0 uncovered on all five sheets). They
are **not reviewed yet**, one by one, against the method's path-variant rule (one circuit out on one path and back on the
other, or `stops_via` for a one-trip deviation):

- HKO: 448 (Hrabová), 451 both ways (Prostřední Suchá, Kaufland), 452 both ways, 553 (Elektrárna Dětmarovice).
- TFJ: 304 ×2 (Místek, poliklinika), 306 ×2, 348, 714 (Lyžbice), 723 (Svibice), 750, 980 (Staříč).
- Opavsko: 241 both ways (Zálužné, Lhotka), 248, 253, 263, 264 (Podvihov, Komárov), 555 ×4 (Nový Bohumín); 246's short
  trips' own street (U Sušárny, Latarna).
- Novojičínsko: 615 ×3, 620, 621 Ostrava, 625 Tísek, 628, 653, 656, 657 Kunčice, 670 ×3, 698 ×4 (Tymphany), 927 ×2.
- Bruntálsko: 822 (Chomýž), 862 (Karlov), 874, 909.

## Fixes (all five sheets are held until the owner answers the regional policy question)

- **Opavsko 292:** two lines, each every 160. 292 Ostrava Offset 72 (real 15:33), Chuchelná, železniční stanice Offset 0
  (real 14:21); 292 Strahovice Ostrava Offset 12 (real 14:33), Strahovice, kaple Offset 75 (real 15:36). Buses 24-1007,
  24-0004 (was 24-1116, 24-1007).
- **Opavsko 246:** the way back runs via the Jakartovice villages, Mladecko, točna and Dolní Životice, hor.konec + střed (as
  17:32 runs), not via U Sušárny. Typed values and buses unchanged.
- **TFJ 314:** the town end is Frýdek, Revoluční (via magistrát, T.G.Masaryka, Na Veselé), not the station. Revoluční
  Offset 85, Also at 116 (real 14:26, 14:57, both exact); Janovice Offset 34, Also at 71 (real 14:12, 15:35); every 120,
  2 buses, as before the fix. (The every-120 row itself is from the held 25 Oct check; published v5 is every 240.)
- **TFJ 340:** the way out runs Ostrava – Kunčice (Frýdecká, škola, nádraží Kunčice, Areál OZO) – Hrabová – Vratimov, as the
  14:12, and from Místek on via Baška, Janovice and Pržno to Frýdlant, as the 22:05 (the only full trip through Kunčice).
  Typed values and bus unchanged.

## Shared-script fixes found on the way (`odis-regional-hko/scripts`, all five sheets)

- `05_schedule`: a leg read at a knot listed its stops only from the knot on (28 legs; 281 back from Třebom began at
  Kobeřice, 292 back from Chuchelná at Hlučín). Its path now comes from the trips that run the leg from its terminal. Only
  the stop lists and the knot checks changed; no typed value, interval or bus count.
- `05_schedule`: the knot check compares the modelled time with every trip the leg stands for that passes the point, not
  only the trips that run the whole leg (369 at Šenov: 130 → 0; 292 Strahovice at Hlučín: 67 → 3). Display only.
- `04_roster` (`keep_roster`): where a line now needs fewer buses than it had, the published bus with the closest evidence
  stays, not the first listed (292: 24-1007, which ran both pattern trips; TFJ: 732 keeps 73-0013, 73-0031 moves to 735 in
  place of a designed bus, 783 keeps 74-1102).

## Open, for the held rebuild

- The regional policy question (A/B/C) still holds all five sheets, the HKO town sheet and the Ostrava sheet.
- TFJ's held schedule (150 buses) leaves 724 one bus short in the roster step, with either keep order.
- The Novojičínsko and Bruntálsko rosters exclude the earlier sheets' plates: rebuild them after TFJ and Opavsko.
