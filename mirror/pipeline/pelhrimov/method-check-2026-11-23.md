# Method check, MHD Pelhřimov + VDV 250, 23 Nov 2026 (bus schedule method v4)

Every timed leg tested with Step 4 (`audit/step4_regional.py pelhrimov`): window slots = real departures ± 1, and ≥ 80 % of window
slots with a real departure within 3 min. Also run: `branch_check.py` (no leg is read at a midpoint), `path_check.py` (1 flag,
explained below) and `passing_check.py` (2 flags, explained below), all with `AUDIT_SHEETS=pelhrimov`.

## Verdicts on the legs that fail Step 4

- **1, silo → Táborská and Táborská → silo (FEWER).** Line 1 is one bus's real afternoon sequence as a circuit every 120
  (silo 14:40 → Táborská, Táborská 15:30 → silo, silo 15:45 → Starý Pelhřimov, Starý Pelhřimov 16:15 → silo), exact on all four.
  The window also holds the second and third buses' shift-change trips (14:00–14:45, 16:15, 16:35), at no repeating minute.
  The passing candidates (every 160 with four slots one way, every 180 with three the other) run the two ends at different
  rates, which Simutrans cannot run (Step 7), so they are not a design. Kept; reason on the card.
- **250 Humpolec, Pelhřimov → Poliklinika (FEWER).** Outstation line: at the Poliklinika 5 out, 2 back in the afternoon; the
  buses sleep at the Humpolec garage. Timed both ways at the inbound rate (every 240), the extra out trips off the pattern
  (v4 rule). The plates of Tue 24 Nov are to confirm "buses going home" (v2).
- **3 (changed after the first test).** The first design (one line every 60 alternating the two ways at :15 / :45) failed
  both legs (EMPTY). Step 4 found passing patterns, so they are used: via the station every 180 at 16:15 / 16:50, via Pod
  Floriánem every 240 at 15:45 / 16:57; both pass.

## Other flags

- **path_check, 250 at 15:12 from Havlíčkův Brod.** That slot's trip runs through Kojčice, Vadčice and Dehtáře, which the
  hourly line skips; those villages are on 250 Humpolec (the card says so).
- **passing_check, 1 EACH WAY.** Read at the bus station: 9 trips each way, 5 on the circuit; the rest are shift extras (above).
- **passing_check, 3 ONE WAY at Čajkovského.** Both ways of the loop pass Čajkovského, so every trip reads as one way.

## The audit table

## pelhrimov: 10 timed legs, 7 ok, 0 EMPTY, 0 MORE, 3 FEWER (0 auto, 10 hand); failing: 3 FIXABLE, 0 IRREGULAR

| Line | Simutrans line | Every | Entry | Class | Fit | Window slots | Real in window | Passing candidate |
|---|---|---|---|---|---|---|---|---|
| 1 | 1 | 120 | Pelhřimov, silo → Táborská | FEWER | hand | 14:40 | 14:40 15:45 16:15 16:35 | FIXABLE: every 160 0:15 0:35 1:20 2:25 (5 exact over the day) |
| 1 | 1 | 120 | Pelhřimov, Táborská → silo | FEWER | hand | 15:30 | 14:49 15:30 16:18 | FIXABLE: every 180 0:30 1:18 2:49 (4 exact over the day) |
| 250 | 250 Humpolec | 240 | Pelhřimov, autobusové nádraží → Poliklinika | FEWER | hand |  | 14:23 15:13 | FIXABLE: every 480 6:23 7:13 (2 exact over the day) |
