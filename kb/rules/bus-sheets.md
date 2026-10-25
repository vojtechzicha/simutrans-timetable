# Bus sheets: city, small-town and ODIS regional

Applies on top of [city-fleet-sheets.md](city-fleet-sheets.md). The step-by-step method for regional lines is
`mirror/pipeline/bus-schedule-method.md` (owner's method, 20 Oct 2026) — read it in full before any regional or small-town sheet;
its "Checks before publishing" list must pass. A worked example: `mirror/pipeline/ostrava-bus/method-check-odis-2026-10-20.md`.

## Two kinds of bus line — pick the rule set first

| | **Big-city local lines** | **Regional lines + small-town networks** |
|---|---|---|
| Where | Ostrava DPO, Prague, Olomouc, Brno, Plzeň, Pardubice (all trams/trolleybuses too) | ODIS regional (all `odis-regional-*` sheets), Havířov / Karviná / Orlová town lines |
| Model | the afternoon peak + the line's unique stops | the whole day read at core points, repeating interval |
| Off-peak single trips | listed, **not** modelled (Ostrava 22 evening run "would be a mistake to model") | bent onto a repeating slot ≤ 480, or folded into the line they belong to |
| Exceptions | ask the owner, with trips, interval, bus cost and coverage effect (Ostrava 57 every 480 was an approved one-off) | — |

Owner, 20 Oct 2026: "Ostrava/Prague/Olomouc - these big cities don't use the method. Only smaller ones like Orlova/Karvina do use it."
If unsure whether a town is "small", ask. Before applying a rule forwarded by a peer session, check it is meant for this kind of line.
**Depot runs are never modelled**, in either kind.

## The regional method in brief (owner's "Ex4" method)
Owner, 20 Oct: "Look at how I did in the save game Ex4 — there is also a very irregular service, but I defined it in core points,
created a repeating interval and it suddenly made sense." (Ex4/1 every 240, Ex4/2 and Ex4/3 every 480, one line per destination,
timed only at core points.)
1. List every trip of the whole operating day (5–23).
2. Choose core points (termini, main knots).
3. Read each trip at the core points it passes, not its start/end.
4. Find the repeating interval at the main knot.
5. Give each destination variant its own Simutrans line on a longer interval (240/480), offset so they don't coincide. Where a variant
   takes one hour of an hourly line, the main line runs every 480 with seven slots and the variant takes the eighth.
6. Time the **terminals**, worked back from the knots: terminal departure = knot time − running time; the knot gets no timetable
   ("Time the Koukolná branch from the terminal, just calculate the departure so it is in correct time in the knot"). Buses, unlike
   trains, wait only at terminals.
7. Both ends at the same rate, balanced.
8. Fold sparse lines into the line they belong to (503 as 504's Důl Lazy leg; 513 carried by 514).
9. Every stop on a Simutrans line (coverage).
10. Size from the pattern.
11. Review by hand; list what is doubtful.
No every 1440 / 720 — max 480 ("we can bend the reality a bit"). Shift-change lines every 480.

## Stop coverage (owner, 20 Oct: "501 is the only line running to Dětmarovice, how can we not model that?")
- Before publishing any bus sheet, run a sheet-wide coverage check: every stop served 13:00–19:00 is on some **modelled** Simutrans
  line (the most common sequence of a scheduled direction — not just some trip of the line), or listed with its reason.
- Per card, list the trips that are on none of the line's Simutrans lines.
- Rotating buses, rings across two line numbers (401/406), sparse unique branches: hand-set circuits (`config.line_overrides`,
  Ostrava 41 precedent).
- One Simutrans line per real line; offer pooling as an option, never pool silently.

## Hand review (owner, 20 Oct: "Is the lines the best schedule that fits my intent (not necessarily the scripts)?")
- A scripted fit is a **draft**. Before publishing, dump each line's real peak departures per direction and how its buses chain
  trips, next to the suggested rows, and judge every approximate row.
- On a regional sheet, no `at: 'auto'` row ships without the Step 4 test per direction (window slots = real ±1, ≥ 80 % of
  slots with a real trip within 3 min), written into a dated method-check file (owner, 25 Oct 2026: "that's the point of you
  doing it, so you'll not produce incorrect results"). The Opavsko Hlučínsko lines 281/282/290/292 had all failed it.
- **Outstation lines:** where buses sleep at the far ends (Hať garage, Třebom, Strahovice…), the afternoon sends more buses
  out of the city than come back, and Step 5b can't pair them. Time the line both ways at the inbound rate and list the extra
  peak departures (buses going home) as off the pattern. **No empty-return lines just for frequency** (owner, 25 Oct 2026:
  "Unless those empty runs add something really needed and specific, don't add them just for frequency"): in the game a line
  repeats all day, so an empty return shuttles back every period. Add one only for something specific, e.g. a stop nobody
  else serves (387, 543B). Pick which departures fall off by the plates and by the waits (290: 16:19 off, not 14:59, needs
  4 buses instead of 5).
- **Forks past the reading point:** a leg read at a midpoint (`core_to` short of the terminal, or a `knot`) counts trips
  wherever they end, so Step 4 can pass on another branch's trips. 292 was read at Píšť, Mýto and its two Ostrava slots were
  Strahovice trips on a line that ended at Chuchelná (owner, 25 Oct 2026: "half of the services going to Chuchelná, half
  going to Strahovice, kaple - but you model as one line?"). One Simutrans line per end (Step 5, `notvia` for the other
  end); a knot may mix trips that start on the line's own path, never trips of another branch. Pick the town end the slot
  trips use (314: Revoluční, not the station). Run `pipeline/audit/branch_check.py` and `path_check.py` after any change;
  every flag is fixed or explained on the card (`pipeline/audit/branch-check-2026-10-25.md`).
- A sheet the owner may already have in the game is rebuilt with `keep_roster` (Ostrava bus; regional sheets' shared
  04_roster step 6): published buses stay on their line wherever they are still evidence for it.
- A multi-slot row on a long interval (290: every 120, four slots each way) is fine when it is exact in the window and no
  simpler interval passes Step 4; put the simpler option on the owner checks.
- Label every typed value with its own real time, worked out from the value (+61 at loops), never by zipping two sorted lists.
- Seen artefacts: merged variant minutes made an exactly hourly line approximate; sparse-band fallback gave every 120 to hourly
  lines; a minimax slot rule moved :06 to :01; daily timetables for sporadic lines.
- Hand-set (`line_overrides` / `schedule_overrides`) where the main pair alone fits exactly or one bus runs a fixed sequence.
- Doubtful rows go to a "To check" list at the top of the sheet with the slower option and its bus cost. Never silently pick the
  busier pattern.

## Live observation (vehicle day)
- DPO (Ostrava) and the ODIS live map have **no history**: poll on the vehicle day over the peak, with the machine kept awake
  (`keep_awake.py`, start the poller detached). The 30 Sep Ostrava poll lost half its peak to sleep.
- Buses swap lines all afternoon: each bus fills one Simutrans line it was seen on, by augmenting-path matching (HKO `04_roster`).
- ODIS sheets must not double-count a bus: each later sheet excludes plates counted by earlier ones (build order:
  Ostrava Hranečník cards → Havířov/Karviná/Orlová → HKO regional → TFJ / Opavsko / Novojičínsko / Bruntálsko).

## ODIS regional sheets specifics
- Scope = kraj contract area by **licence prefix** (912 Havířovsko, 873 Karvinsko, 874 Orlovsko, 871/863/864/861 TFJ, 902/903/904 +
  905 MHD Opava, 883/882/884 + 886/887 Novojičínsko, 852/853/854 + 856/855 Bruntálsko). Lines shared between sheets are listed and
  linked, not repeated (see each README's "other_sheets").
- **Hub sections on the Ostrava sheet** ("All lines at <stop>"): Hranečník's ODIS lines are modelled there (20 Oct, before the
  regional sheets). For a hub added later (sad Boženy Němcové, 25 Oct 2026), lines a regional sheet already models are shown as
  that sheet sets them, read from its derived data, and linked; their buses stay counted there (`ostrava-bus/scripts/08_hubs.py`,
  `config.hubs`). Moving a line between sheets is the owner's call: it changes two sheets and the in-game lines.
- All five run on `odis-regional-hko/scripts` with `--base odis-regional-<x>`; each sheet's config is written by its
  `authoring/*_spec.py` + `*_config.py`. Edit those, rerun them, then the pipeline.
- Short diversions → regular timetable; long diversions (to Nov/Dec) are modelled as run, or put to the owner as a choice.
- The save's old ODIS lines (800xxx) predate the fork and **are wrong** ("The OLD lines ARE WRONG THO - I am redoing it"): the
  sheets are the target; don't fit to old convoys and don't apply "fewest moves" to them.
- Town lines use `VZ-MHD<Town>` objects only; regional (kraj livery) buses use `VZ-ODIS-bus`. `CZ-ODIS` / `CZR-ODIS` are only for
  the old save.
