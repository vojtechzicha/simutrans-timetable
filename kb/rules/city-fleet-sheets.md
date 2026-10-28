# City MHD fleet sheets (trams, trolleybuses, buses)

The per-vehicle "Peak Fleet" / "Vypravenost" sheets: for each real line, the Simutrans line(s), their schedule values, and the
actual cars (by fleet number) that ran it at the afternoon peak, plus depot lists and the pak128 objects to use.
The canonical shared text is `mirror/pipeline/README.md` ("Shared rules"); this page consolidates it with every later owner ruling.
Bus-specific rules (regional vs local, coverage, hand review) are in [bus-sheets.md](bus-sheets.md).

## What the owner originally asked for (Pardubice, 25 Sep 2026)
Model the weekday **afternoon peak**; if a line has no PM peak service but runs in the morning, use the morning times. Exclude
night, school-only and off-peak-only lines (but the flight-bound airport line 90 was wanted anyway). Show line stop patterns
both ways with variants distinguished, stops → lines, terminals with leaving frequency, headway + offsets ("every 15 at :02 :17"),
bus vs trolleybus, battery sections, přípoje / přímé spoje, výluky (long-term = model as it runs; short-term = regular state),
vehicle category per line. Accessibility is not wanted.

## Which day
- **Vehicles:** afternoon peak of the last weekday before the target date. If the city has no records that day, use the latest
  complete weekday (preferably a Friday) and say so on the sheet. "Yesterday's state" on a Sunday = vehicles from the last weekday,
  network as of yesterday (confirmed 28 Sep).
- **Network:** the timetable in force on the target date. Short-term closures → regular state; long-term → as they run.
- **Peak:** ~15:00–17:00, reference hour 16:00 — but each line is anchored at **its own busiest 2 h in 13:00–18:00**, unless
  15:00–17:00 is within one departure of it (owner, 20 Oct: Ostrava bus 23 "20 minutes is the most common afternoon pattern").
- Morning-only duties are left out and listed under "Not counted". Evening/night course groups are left out of type history.
- Swaps: notes carry no time — resolve from where cars turned up later that day, else list the replacement and name the replaced.

## Vehicle display (owner, 28 Sep 2026: "Don't use cryptic")
- Full type names, full stop and depot names; **no abbreviations anywhere**.
- Coupled set = `A + B`, numbers and types in the same order. Never collapse a recorded coupled pair to a single.
- Every vehicle is a **3-line cell**: (1) numbers · depot, (2) full types · length, (3) pak core.
- The type must be **visible next to every vehicle** — never only in a tooltip or a summary count ("I can't tell the type from
  this", 28 Sep). Group vehicles under a visible type label if helpful.
- Full object names, section chains, liveries and car units appear **once**, in the "Pak128 objects" table.
- Owner preference (Ostrava bus, 20 Oct): collapse the "not needed" vehicles.

## Page header (owner, 29 Sep 2026)
Every fleet sheet has the Prague-tram-style **sticky bar**: line badges, depot links with counts + section links, and a vehicle
search (`#q`) highlighting every `[data-v]`. Anchors use `scroll-margin-top: var(--stick)` with `--stick` = bar height + 8 px set by
script on load/resize (a fixed margin hides headings on phones). Drop-in: `pipeline/brno/scripts/sticky.py`.
Verify in a real browser (Playwright, `channel='msedge'`) at 1400 px and 390 px.

## Sizing: how many vehicles a line needs
- **Size from the pattern the sheet suggests**, for every line (owner, 20 Oct: "You should always size it from the pattern you are
  suggesting - for all lines"). Follow a vehicle round the suggested slots with real running times and the minimum layover
  (`ostrava/scripts/lib.py` `pattern_need`). No "variant extra" vehicles for unmodelled variants.
- Tram cities: `cycle_need` (`brno|plzen|praha|olomouc/scripts/common.py`): follow a vehicle leaving ~16:00 round its trip, taking
  at each end the first departure ≥ layover later (3 min default, or the terminus's own shorter turnaround, e.g. Prague 31 at
  Vysočanská 1 min). **Don't size by FIFO trip chaining** — depot pull-outs make it miscount (Brno 10: 7 instead of 4–5).
- Buses with branches: need = max(round-trip need, buses on the road 16:00–16:59 with the cycle layover)
  (Prague 191: 6 vs 15 on the road).
- Keep the operator's slack only when carrying a recorded surplus into a new timetable; otherwise the spares rule applies.
- **Shortest terminal wait by default** (owner, 18 Oct): don't model interworking/line swaps at the peak if each line turns faster on
  its own (Ostrava 1 + 2 stay separate). Model a cross-line circuit only when the weekday peak is observed doing it.
- Cross-branch circuits for star lines only where they save ≥ 1 vehicle ("where it significantly shortens wait, do it", 20 Oct).

## Splits, branches, pools
- Where course (kurz) numbers mark a branch, split by range (Brno 5S = kurzy 21–27; Prague 17 = 1–17 / 21–37).
- Otherwise size each branch by need and pick the cars — prefer peak-only courses — and say on the sheet that the pick is a choice.
- Spares: keep on the main line when the other branch is a reinforcement (Brno 8); split evenly between two full branches (Prague 22).
- **Short workings** are their own line only if they are a *peak trip*: ≥ 3 trips 15:00–17:59, no depot at either end, at least one
  departure 16:00–16:59 (owner ruling 28 Sep: Prague 3/9/22 shorts ending 15:38–15:47 are not peak trips), and they run alongside the
  main pattern rather than replacing it after the peak. Otherwise list "not a peak trip, not modelled".
- Bus branches (Ostrava rule): ≥ 6 trips 15–18 h, a 16:xx departure, no garage end; regular afternoon branches (≥ 3 trips each way
  13:00–19:00) are modelled too (owner on 23 Záblatí, 20 Oct).
- **A branch that is its own Simutrans line gets its own rows** on the card, every time. "Own Simutrans line" without
  values is not done (owner, 28 Oct, Prague 109 VÚ Běchovice: "Is it reasonable?" → "do include - and also for the other
  lines"). Give each branch its Every / Offset / Also at, interleaved with the main rows, and say what the split costs:
  separate Simutrans lines can't interwork, so per-line needs can add up to more than the card's one count (109: 5 + 3 vs 7).
  A branch with no game line yet (Prague 177 Volha, 174 Luka) goes on the in-game change list as a line to build.
- **Branches sharing a terminus must interleave** as the real timetable does (owner, 20 Oct: "if the real timetable interleaves, you
  should interleave. I thought that is the whole point?"). Fit them together on one interval; scan for bunching at shared termini
  **and** at junctions/intermediate stops (23 at Rychvald, rozcestí), and across different lines on shared trunks
  (`check_trunks.py`, `check_cross_lines.py`, `space_corridor.py` in ostrava-bus). Fix only model artefacts, not real bunching.
- **Shared pools** (one Simutrans line for two real lines, e.g. Prague 5 + 6; or two lines from one pool, Olomouc 3 + 5) are the
  owner's modelling choice: mark them, with the real share that runs through. Don't pool silently; offer it.

## Designed vehicles, spares, "never ship without vehicles"
- **Never publish a sheet without vehicles on its lines** (29 Sep: "you are missing the vehicle assignment to lines"). Fill every
  line in this order: observed data (even post-peak sightings, marked provisional) → other days' records → designed vehicles.
- **Designed vehicles get real car numbers** ("fetch older records and use real car numbers"): from the line's own history, active,
  home depot, main type, and not out anywhere that day (check the day overview/live feed). Mark "designed, not recorded" with the
  date of the history record. If history runs out: free active cars of the line's own types, then the operator's usual types.
- **Roster coverage:** every vehicle type in the line's full roster (history + logged) must be represented among the vehicles used.
- **Spares "not needed"** (owner, 29 Sep, covers logged surplus too): keep exactly the need counted — one of every roster type first
  (most frequent first), then drop afternoon-only duties ("odpoledne"), then the highest kurz numbers. A substitute bus on a
  trolleybus line goes first. Show the rest dimmed at the bottom of the card as "not needed", excluded from all counts, depots and
  pak totals. Code: `brno-trolleybus/scripts/common.py` `mark_spares`; `praha-bus/scripts/04_courses.py`.
- **Fleet-wide coverage** when the whole roster is designed (Most–Litvínov bus): every fleet type **and livery** appears on some line,
  weekend-only cars marked "normally weekends only", articulated only on lines that already run articulated; per-line needed vs
  assigned table.
- Type history: leave out late-evening/night course groups and keep coupled pairs (owner, 18 Oct, Ostrava 7: "solo trams are not
  working on line 7"; "Make sure your research is correct"). Look at raw records by course group before trusting a type share.
- Owner type choices override observations when given (Ostrava bus `config.owner_types`: Urbino 10 on 50 and 40C).

## Changing a published sheet (the owner has already built it in the game)
- **Fewest moves.** Rebase on the published roster and swap only what's wrong (`ostrava/scripts/04b_rebase.py`,
  `praha/scripts/04b_rebase.py`). When needs drop, mark extras "not needed (park it)" rather than reshuffling.
- **Change sheets** for network changes (Prague, 13 Oct): keep the trams already in the game, move as few as possible, show what changed
  per line, new lines in full, only the trams that must change visible, everything else folded (`assets/page_changes.html`).
- **Always end with the list of in-game changes** (owner, 22 Oct): per line and terminus entry, old → new Departure every / Offset /
  Also at, and every vehicle to add/remove — including earlier changes in the session the owner may not have entered yet.

## Pak objects
See [pak-objects.md](pak-objects.md).

## Timetable data rules
- GTFS: use calendar + calendar_dates of the service day. Keep the feed's export date in the raw folder name.
- JDF (CIS JŘ): among line versions valid on the day, the latest "valid from" wins, ties go to the shortest validity.
- See [../sources.md](../sources.md) for every feed and its quirks.
