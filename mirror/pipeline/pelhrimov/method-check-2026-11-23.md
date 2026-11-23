# Method check, Pelhřimov: MHD and VDV lines, 23 Nov 2026 (bus schedule method v4)

Every timed leg tested with Step 4 (`audit/step4_regional.py pelhrimov`): window slots = real departures ± 1, and ≥ 80 % of window
slots with a real departure within 3 min. Also run with `AUDIT_SHEETS=pelhrimov`: `branch_check.py` (3 legs read at a midpoint,
all ok), `path_check.py` (3 flags) and `passing_check.py` (1 EACH WAY, 4 ONE WAY), each explained below.

`passing_check.py` was fixed for JDF sheets the same day: it compared the schedule's stop names (expanded by the sheet's `nm`) with
the raw JDF names in trips.json, so every stop read as off the pattern (14 false EACH WAY flags here). It now reads a JDF sheet's
trips through the same `nm` + terminus alias; GTFS sheets (PID, no `jdf` in config) are compared as before.

## Changes made because of the tests

- **3:** one line every 60 alternating the ways failed (EMPTY); the passing patterns are used (every 180 / every 240).
- **305, 324 (IRREGULAR), 325, 281 Libkova Voda (EMPTY):** the default window ran past the end of the line's pattern (305's last
  pattern trip is 16:03, 324's 15:32, 325's back trips 14:57 / 15:59, the Libkova Voda shuttle 16:01): model hour set by hand inside
  the run (method v4, "Model hour set by hand"); all four pass.
- **905 → Jindřichův Hradec (EMPTY):** the slot moves from :39 to :34 at 16:34 ("the afternoon wins"): the passing :34 is used.
- **905 Nová Včelnice (EMPTY):** the 17:27 turns at Jarošov, rozcestí: the leg is read there (`core_to`); passes.

## Verdicts on the legs that still fail Step 4

- **1, both legs (FEWER):** one bus's real circuit every 120; the window also holds two other buses' shift trips at no repeating
  minute; the passing candidates (every 160 one way, every 180 the other) cannot run against each other (Step 7).
- **250 Humpolec, out (FEWER):** outstation line at its inbound rate (5 out, 2 back at the Poliklinika; Humpolec garage).
- **300 Jihlava, Jihlava → Pelhřimov (FEWER):** the Jihlava :10 extras (13:10, 14:10, 15:10; one back at 14:04) are buses going to
  the Pelhřimov garage: three one way, one back, no branch. The line runs at the hourly rate both ways.
- **300 Pacov, Pelhřimov → Pacov (EMPTY):** hourly :31, with 14:36 5 min late (the 13:40 from Jihlava runs 5 min slower). The
  passing candidate (every 180) cannot run against the hourly way back (Pacov :50). Kept.

## Other flags

- **path_check 250 at 15:12** (the village trip; the villages are on 250 Humpolec), **325 at 14:38** (it takes the road past
  Rynárecká and ACHP, which the town lines serve; the line runs through Vokov and Dobrá Voda as the 15:38 does), **905 at 17:07**
  (Myslotín and Ondřejov are on the out leg; the way back follows the 14:12 through Jindřichův Hradec, Průmyslová).
- **passing_check:** 1 EACH WAY (shift extras, above); 250 ONE WAY (the Humpolec garage runs and the 13:02 / 13:53 trips 10 min off);
  300 ONE WAY at Vyskytná, rozcestí (the Jihlava :10 extras; that roadside stop is the one coverage exception); 3 ONE WAY (loop trips
  off the pattern); 905 ONE WAY at Ondřejov, obchvat (the :49 trips take the bypass, the line follows the village path).
- **Coverage:** 332 afternoon stops, 331 on a line; Vyskytná, rozcestí is an exception (a roadside stop of Vyskytná, whose village
  stop is on 300 and 321), with its reason on the page.

## The audit table

## pelhrimov: 56 timed legs, 51 ok, 1 EMPTY, 0 MORE, 4 FEWER (0 auto, 56 hand); failing: 5 FIXABLE, 0 IRREGULAR

| Line | Simutrans line | Every | Entry | Class | Fit | Window slots | Real in window | Passing candidate |
|---|---|---|---|---|---|---|---|---|
| 1 | 1 | 120 | Pelhřimov, silo → Táborská | FEWER | hand | 14:40 | 14:40 15:45 16:15 16:35 | FIXABLE: every 160 0:15 0:35 1:20 2:25 (5 exact over the day) |
| 1 | 1 | 120 | Pelhřimov, Táborská → silo | FEWER | hand | 15:30 | 14:49 15:30 16:18 | FIXABLE: every 180 0:30 1:18 2:49 (4 exact over the day) |
| 250 | 250 Humpolec | 240 | Pelhřimov, autobusové nádraží → Poliklinika | FEWER | hand |  | 14:23 15:13 | FIXABLE: every 480 6:23 7:13 (2 exact over the day) |
| 300 | 300 Jihlava | 60 | Jihlava, autobusové nádraží → autobusové nádraží | FEWER | hand | 14:40 15:40 | 14:10 14:40 15:10 15:40 | FIXABLE: every 30 :10 (19 exact over the day) |
| 300 | 300 Pacov | 60 | Pelhřimov, autobusové nádraží → autobusové nádraží | EMPTY | hand | 14:31(-) 15:31 | 14:36 15:31 | FIXABLE: every 180 0:31 2:36 (4 exact over the day) |
