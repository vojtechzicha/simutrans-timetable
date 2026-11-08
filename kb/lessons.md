# Lessons: the owner's corrections, in order

Each entry is a mistake the owner caught (or a preference they stated) and the rule that came out of it. Quotes are verbatim.
The rules themselves are folded into `kb/rules/`; this log keeps the *why*. Detail per sheet is in `kb/notes/`.

## How the owner works (read first)
- They build every sheet in their live save game by hand, so **precision and the in-game consequence matter more than prose**.
  After a change, always list what to re-enter in the game.
- They check details against reality *and* memory, and will catch missing trains/stops. Do the research before presenting.
- They prefer **simple, functional game lines** over strict realism once both options are shown — but want the realistic one offered.
- They decide scope; for one-off workings decide yourself ("model what happens in reasonable matters"). Ask only real decisions,
  with the facts (trips, interval, vehicle cost, coverage).
- "Finish all, don't guess" (22 Oct): ask the session that knows (fleet desk, engine) instead of assuming.
- Archive, don't delete: old sheets go to `archive/` when the owner says "archive".

## September 2026 — city tram sheets
- **25 Sep (Pardubice):** first brief — afternoon peak, no night/school/off-peak lines, variants distinguished, výluky short vs long,
  vehicle category; accessibility not wanted.
- **28 Sep (Brno):** "I can't tell the type from this. Warn the others" → type visible next to every vehicle.
- **28 Sep (Prague):** "put it there in full… Don't use criptic. If coupled, use + with the same identifiers" → 3-line cell, full
  names, `A + B`, pak sync.
- **28 Sep:** "Ask the other simutrans code sessions to help you to convert it into ideal simutrans schedule (custom fork) settings.
  Like this can be every 7 mins at offset 6, this need 'Also at'" → fork schedule block on every sheet.
- **28 Sep:** "I want a time minute earlier if the tram must leave a smyčka (noted in all the HTMLs)" → loop −1 rule.
- **28 Sep:** "store how you did and process the data. When the timetable changes, I'll ask you to update… Not in memory or
  scratchpad, but in good format in the folder" → `pipeline/<city>/` with README + "How to update".
- **28 Sep:** "The 3,9,22 are not peak trips and should not be included" → short-working peak-trip test.
- **28 Sep:** Brno 8S — "I have it in Simutrans as two different lines, so I need a proper split" → splits sized by need.
- **28 Sep (Prague metro):** "I need intervals, lines and number of trains… The interval should also be in Simutrans units, the number
  of trains for A should be per branch."

## 29 Sep — trolleybuses, buses, rail v1
- "The Prague tram has this nice sticky header, but some newer artifacts don't… you're responsible for all of the files" → sticky bar.
- Ostrava bus shipped "vehicles pending": "you are missing the vehicle assignment to lines" → never ship without vehicles.
- "fetch older records and use real car numbers" → designed vehicles with real numbers; "show the not needed in marker… not to skip
  any type" → roster coverage + spares rule (also for trams/trolleybuses, and logged surplus).
- Most bus: "each type should be represented" → fleet-wide type × livery coverage.
- Prague bus: include **all** lines; non-DPP lines as good as DPP (no stand-ins); separate sheets stay single-mode (ferries on the tram
  sheet).
- MD-CR v1: "Make it more practical please. Do not focus on one hour, make a approximation of the common standard across peak."
  "Ex1 also goes to Warszawa." "Kysučan (R Žilina) goes every 4 hours. So why do you think every two hours?" → one headway from both
  ends, clock-face standard.

## Early October — rail method
- **3 Oct:** "don't fix, I like it uneven" (Nymburk) → don't even out combined headways.
- **3 Oct:** "odd is first, even is second (+60)" → odd-first offsets.
- **3 Oct:** "The 010s only run to svitavy, so why are we modelling to Letovice?… it is dear to me… do not extend 010 beyond
  Svitavy" → real structure, never extend past a terminus; model what the owner cares about.
- **3 Oct:** "Now we lovingly gotten in correct. Can you record all those rules? Because in MD-CR you did none of this careful
  planning" → `pipeline/rail-design-rules.md`. "I don't love MD-CR - keep it simple as you did here in chat" → plain pages.
- **3 Oct:** "count the number of trains based on the condition that only the first foreign station is included."
- **4 Oct:** "LE has to have short time on the Praha hl.n. - no more than 20 minutes"; add Přerov "where it has to rotate".
- **4 Oct:** "I wanted each station before Brno hl.n. to be timetabled, but any stay that should be in hl.n. should remain in hl.n."
- **4 Oct:** "Completely wrong… Do not invent dwell times, use real ones. From depot… dwell+travel is 15 minutes." Also: the LE delay
  came from the owner's own typo ("I may have errornously written them down") → check in-game entries before blaming offsets.
- **5 Oct:** "014 Aren't there peak trains to Uhlířská Janovice?… 235 Aren't there Kutná Hora only trains?" → find every train by
  every station.
- **5 Oct:** "it does? [vagonweb links]… I see řazení of these trains" → vagonweb works (zeme=ČD, cookie); share lines only if same
  vehicles. "now try to minimize the stays at the big main line stations."
- **8 Oct:** "Dobříš seems way too often - definitely not more than one vehicle"; "Why can't we use Also At for trains to Čisovice?";
  "I AM sure they are not standing at Praha hl.n. for more than 10-20 minutes"; then "I like the simplified lines before, restore the
  version before" → offer realism, accept the simpler choice.
- **8 Oct:** "R49 is clearly hourly between Praha hl.n. and Benešov… You know better about the holešovice mess" → frequency from the
  peak direction, don't make the owner ask twice.
- **9 Oct:** R18 — "I am sure we will model the situation with coupling trains" → fork coupling.
- **9 Oct:** "can you change the local trains to S49" → "nah, I mean Praha-Hostivař - Roztoky line" → ask on ambiguity; don't edit
  archived sheets.
- **10 Oct:** "1 hour at Praha hl.n. is too much… Praha-Libeň or Praha-Vršovice?"; "during peak the vehicle actually goes all the
  way to Malešice? If yes, model it so even if it requires extra vehicle"; "SHOW ME ONE TRAIN IN THE AFTERNOON PEAK GOING TO CASLAV"
  → verify claims with real trains before asserting.
- **11 Oct:** "add timetable at Liteň due to switching the cabin sides"; "R6 actually goes via S6 route… check again".
- **13 Oct:** "tracks end at Rokycany, Blatná and Čimelice"; "I'm missing trains to Rožmitál"; "If rožmitál has no weekday service, it
  should not be in" → junction check, no-workday branches out.
- **13 Oct (Prague closure):** "be smart with the changes - I'll be redoing it in game, so reduce the workload… if line only changed,
  mark which trams must change" → change sheets, fewest moves. "Can you add the NAD?"
- **14 Oct:** "don't they end at Praha-Bubny because of engineering works? Isn't some of this true for the other lines" → check
  výluky. "don't do those ending in early november, do include the Masarykovo one."
- **14 Oct:** "Bubny can have 4 trains max"; "R23 in reality goes back to západ to stable"; S4 coupling at Kralupy with an engine
  session. **15 Oct:** "S4 trains from Lovosice arrive way too early… add more waiting spots on the route" → timing points on
  all-stops runs. "why isn't there big table for S6 before the end of works?" → show works and final states in full.

## 18–22 Oct — Ostrava refinements, regional method
- **18 Oct:** "Prague trams had the real subtitles, I like them. Also if 1 and 2 interwork, it should be modelled" → real-minute
  subtitles; later ruling: shortest terminal wait by default.
- **18 Oct:** "how can it have less departures than arrivals?" → both ends same rate.
- **18 Oct:** "I am pretty sure solo trams are not working on line 7. WTF?" / "1359… highly likely it was 2 Varios coupled. Make sure
  your research is correct" → leave out evening courses, keep pairs; rebase with fewest swaps.
- **20 Oct:** "Model the 41 line as is at 14:00"; "can you collapse the not needed buses?"; "21/81 … shouldn't they be more aligned?";
  "why does the sheet still says every 40 minutes?"; "You should always size it from the pattern you are suggesting - for all lines."
- **20 Oct:** "looking at 23 you haven't scheduled the Záblatí střed, but it is a used branch in afternoon peak; just not at 16:00
  exactly" → model each line at its peak, regular afternoon branches. "if the real timetable interleaves, you should interleave. I
  thought that is the whole point?" "notice both 23 branches will depart at the same time from Rychvald rozcestí" → interleave at
  junctions too.
- **20 Oct:** "[screenshot] why is this not just departure every 30 minutes? Why is there so many errors?"; "31 does have uneven
  departures" → fold slots, hand-check approximations.
- **20 Oct (HKO):** "Do much better please - e.g. 501 is the only line running to Dětmarovice, how can we not model that?" → stop
  coverage. "Is the lines the best schedule that fits my intent (not necessarily the scripts)?" → hand review. "Look at how I did in
  the save game Ex4…" → core points + repeating interval. "Time the Koukolná branch from the terminal… write down this rule, so even
  lower models can do the regional lines files" → `bus-schedule-method.md`. "make sure you do not let the computer sleep."
- **20 Oct:** "I don't like 1440 lines - in game that is not found. 8 hrs should be the very maximal interval" → max 480.
- **20 Oct:** "these rules are for the regional lines, not for local lines… for local lines we model the afternoon peak and unique
  stops… depot runs are never modelled… line 57 [is] an exception to consider and ask" → regional vs local split.
- **20 Oct:** "Definitely 50, do not do 23 - do some from Poruba too" (Urbino 10 placement) → owner type choices.
- **21 Oct:** "Where is 534 and 535? Or have you skipped the Hranečník lines because they are at Ostrava's sheet? (if they are
  somewhere, I am fine with it)" → cross-sheet listing with links.
- **21 Oct:** "Can you verify… 59 line timings? So the two branches don't meet at Polanka at the same time?"; **22 Oct:** "39 and 35
  now is 10-minutes apart in the shared sections right?" → trunk and cross-line bunching scans.
- **22 Oct:** "if you did any changes recently, I'll need you to tell me which lines to check - they are already in game" → in-game
  change list after every change.
- **22 Oct:** "Do what needs to be done - ask the fleet session. Finish all, don't guess."
- **22 Oct:** "The OLD lines ARE WRONG THO - I am redoing it. They were created before the fork" → ODIS sheets are the target.
- **25 Oct:** "to the Ostrava sheet, similarly how we did the Hranečník, do the regional lines from Sad B.Němcové please. It will
  also show if you can use the kb well." → every ODIS line there was already on a regional sheet: hub section that reads them
  from their home sheet and links (no bus on two sheets).
- **25 Oct:** "Yes, I want you to check - that's the point of you doing it, so you'll not produce incorrect results." → scripted
  fits get the step-by-step method check before they ship; 281/282/290/292 rebuilt as outstation lines.
- **25 Oct:** "Unless those empty runs add something really needed and specific, don't add them just for frequency" → the
  281B/290B/292B empty-return lines (5 buses) were dropped; extra peak departures are listed, not modelled.
- **25 Oct:** "290 uses more buses, then verify all sheets with this level of detail" → full check of all 28 active sheets. Found:
  the 01:00 offset origin had only been fixed in the Ostrava pipelines; Brno, Olomouc, Plzeň, Praha and Most–Litvínov still
  counted from midnight on intervals not dividing 60 (and Pardubice was built before the 20 Oct fix). A rule fix must be applied
  to every copy of the shared code, then checked across all pipelines by script (`audit/city_systemic.py`), not sheet by sheet.
- **25 Oct:** "looking at 292 I see in peak half of the services going to Chuchelná, half going to Strahovice, kaple - but
  you model as one line?" → the 292 row was read at Píšť, Mýto, before the fork, so it "passed" Step 4 on two Strahovice
  trips while the line ended at Chuchelná; and its plates were read backwards. Now 292 + 292 Strahovice, each every 160.
  Then: "Unless you'll show me a good reason why you have not modelled this as two branches, do the check mentioned" →
  every leg read at a midpoint on the five regional sheets (`audit/branch_check.py`) and every slot's trip against the
  modelled path (`audit/path_check.py`): 314 (wrong town end), 340 (skipped the stop it exists for) and 246 (way back
  skipped its slot trips' stop) fixed; 51 path-variant slots listed for review. A Step 4 pass only says the minutes fit;
  check where each slot's trip actually goes.

## 28 Oct — Prague bus branches
- **28 Oct:** "The Prague buses 109 does not have VU Bechovice branch. Is it reasonable?" → no: the 25 Oct method check had
  left 11 lines (109, 113, 120, 138, 146, 160, 174, 177, 186, 197, 221) with branches marked "own Simutrans line" but no
  rows, as an open owner item. "Yes, do include - and also for the other lines" → every such branch gets its rows; an open
  item that only needs values is a gap, not a decision. Per-line bus needs and branches with no game line yet (174 Luka;
  177 Volha already runs as an extension of 100177) go on the change list.

## 30 Oct — Prague bus: how many Simutrans lines
- **28 Oct (later):** "Is it truly one line as you describe? Or are those two independent lines? Look at Ostrava, that shows
  it." → a session built `simlines.py` (each branch card split into Simutrans lines, Ostrava style) but never synced or
  published it, so the owner still saw v9. Unpublished pipeline work is invisible to the owner: finish and publish it, or
  say it is pending.
- **30 Oct:** "is 109 two lines or one? I am still unsure. In Ostrava, that was so clear." / "I don't care if one or two -
  just tell me if it is CLEAR OR NOT. I am asking about presentation." / "113 - is that one line, two lines, three lines - I
  JUST DON'T KNOW." → the question was about presentation, not bus counts. Answer that first. v10: each branch card starts
  with "N Simutrans lines" and, per line, its game line and buses. 113 had named 100113S under both of its circuits; now it
  is "not needed".
- **30 Oct:** "Never change lines 100-108" → the unpublished split had turned 102 into a circuit (4 → 5 buses). 102 and 103
  stay out of the split, and cards 100–108 are diffed against the published sheet before every publish.
- **30 Oct:** "The 110 line does not have a branch to Třebovice. Either model it as a real life or for it to use 1 vehicle" →
  Třeboradický hřbitov runs hourly 13:00–19:00 (6 out, 5 back) as the :30 Čakovice trip extended. The 25 Oct method check
  counted only 15:00–17:59 (2 each way) and called it "not a peak trip". Apply the 20 Oct afternoon-branch window (≥ 3 each
  way 13:00–19:00) to Prague as well. Modelled as in real life: 110B is a circuit that also takes the Čakovice :45, and 110
  still needs 4 buses.

## 30 Oct — Prague regional companions
- **30 Oct:** "Now could you do the companion PID lines to the local trains? I remember 111/321, 174/301/352, 113/331/333 (the PID
  number are my guess only)" → asked first what "companion" meant; "Definitley include those that share buses so we have a full
  list. Also those that are "proložené" like 113/333. Not the local train ones." Placement: on the Prague bus sheet.
- **30 Oct:** "I am 100% sure 301/352 are continuations of 174 - why don't you know? That might mean you are missing some
  Navaznosti.txt data." → JDF has no such data for PID and GTFS has no blocks; the evidence was in plain sight: every 301/352 trip
  leaves Luka the minute a 174 arrives. Run the 0-minute chain test before saying a pair is unproven. It also showed the published
  "174A Luka, a line to build" was wrong: those trips are 301/352, as the save already had them.
- **30 Oct:** "Pool if they pool in real live" / "Include if they are interleaved in the real timetiable. I HOPE you are not
  adjusting but trying to fit the real timetable." → pool only where the records show the city courses running the regional line;
  interleave only where the real departures sit in the gaps; rows always from real minutes.
- **30 Oct:** fleet desk: the "missing" regional buses already existed in `VZ-PID-bus`; look in every package before requesting.
- **30 Oct (after v12):** "the 111 seems to stretched. Could we have two variants? also looking at selected buses, it would be better
  (I don't think NB 12s are so used on 329)" → I started a hand-made split for 111; the owner stopped it: "This is specific for 111,
  decide smarter? Is it really best for 329 to have its own circuit?" Sizing every grouping showed 329 belongs with the Koloděje
  branch it extends (same 7 buses as its own line, shorter circuit). Offered the rule for every branch card with its effects; the owner
  chose "Only 111". Answer such a question with the options measured, not with the first fix that comes to mind. The records also
  showed 329 ran on 111's BN 12s, so those now sit on its line.
- **30 Oct:** "I see all 117 written as continues to 203 - isn't there something to consider?" → yes: 117's ten courses run 203
  too and 203 has no record, yet the sheet dimmed 7 of 117's buses and designed 4 for 203. Read the přejezd notes as data: the
  same fix found seven more pairs (195 → 158, 163 → 208, 227 → 226, 120 → 231, 162 → 169, 236 → 235, 245 → 248).
- **1 Nov:** "117 1916 BMD Neocity does not say which livery (PID new or PID old)" / "same for ABbout me SOR BN 9.5" → the
  Prague bus render counted only the liveries its own buses used, not the pak's objects, so a type whose sheet buses all share
  one livery hid it although the pak has two. The rule in `rules/pak-objects.md` was right; the code now counts both (v15:
  Neocity 8,5, SOR BN 9,5, SOR BN 12, Crossway LE Line 12M). Other city renders already read the installed pak objects.
- **1 Nov:** "I see that 329 has only one branch. Is it the line going via Květnice or not." → the :04 row out was the Květnice +
  Dobročovice trips and the :23 back the direct ones, but the card never said so. "yes, please do put the note there, so I know -
  otherwise I agree with the way you modeled it". When a row's trips run a variant route, name it in the row's note, with the
  running time used, and say where the game line differs.

## 1–3 Nov — PID regional, per oblast
- **1 Nov:** "Do the full PID. Divide it per "oblast" (like Mladoboleslavsko), all PID lines should be in. Then use Fable and/or
  subagents to comb line by line, look at my usual notes (there seems to be lot of them usually) and make sure it is polished."
  → twelve okres sheets by licence prefix plus an index of every PID route; a designer subagent per oblast and an independent
  Fable reviewer per oblast that checks every line against this file. The pilot review cut 13 owner checks to 1: the designer
  had re-asked what the rules decide. Ask only real choices.
- **1 Nov:** "Use more than a sample day - working day assumption holds from September to November" → seznam-autobusu.cz had
  put every scripted request behind a JavaScript browser check that day (it fails in an automated Chrome tab too); not
  circumvented. The PID live map (mapa.pid.cz, keyless) was polled on two working days instead: every bus on every line.
- **1 Nov:** "I will swap them all, no issue" (the save's 795 regional PID buses) → the save is a check column, not a base.
- **1 Nov:** "If you want me no to power down the computer, you must make sure you run caffeinate or something so it does not
  sleep" → the poller asks Windows for the system; a second guard (`keep_awake.py`) also holds the display, as Modern Standby
  can idle into standby with the screen off. Say which guards run whenever the owner must leave the machine on.
- **1 Nov:** "I am sure 318 runs some articulated buses" → it does (Citaro C2 GÜ 7952 seen on Sunday, all 318 buses run 317
  courses); passed to the Prague bus session with the evidence; the weekday mix from the 2 Nov poll.
- **2 Nov:** asked whether a line kept only for stops outside the Středočeský kraj (571 Rakovník – Slatina – Chříč) should be
  modelled: "Yes, serve every place" → the coverage rule has no kraj border.
- **2 Nov:** asked whether villages whose only afternoon service is PID Haló (on-demand, no timetable: 886 Bystřicko, 887
  Načeradecko, 888 Českobrodsko, 889 Pečecko) get a line: "Yes, model a line" → their fixed trips (often a school round)
  become a Simutrans line, at most every 480. "Serve every place" holds even where the afternoon service is on demand.
- **2 Nov:** fleet desk on the PID regional request: 20 of the "missing" types already existed in `VZ-Praha-bus` / `VZ-DPPraha-bus`;
  regional PID lines use those objects as they are, `VZ-PID-bus` holds only what they lack → `rules/pak-objects.md` corrected; search
  every pack before requesting.
- **2 Nov evening:** three pooling checks were written "if the 2 Nov live map shows…". The poll settled them before publishing:
  each pair ran on its own buses (534/535: 7628, 7616 / 7595, 7606; no 436–430–430–436 circuit; one 433 trip by a 434 bus), so
  the sheets' choice stood and the checks became notes. Settle evidence-bound checks when the evidence lands, before the owner
  reads them. Also: the live map leaves "Typ vozu" empty for some fleets (OAD Kolín, some Arriva City); a loader must let a later
  row with a type win over an earlier empty one (the first-row-wins loader hid nothing that day, but would have on day 2).

- **3 Nov:** "381 you haven't done the Zásmuky branch. That is not off the pattern, looking at all our rules in the timeframe, I
  clearly see 381 runs Zásmuky/Čáslav switching. This is weird. Verify specifically and then … you may have to correct
  everywhere." → the designer and the Fable reviewer had both read 381's Zásmuky trips by start and end: one trip starts at
  Zásmuky towards Prague, so the four Háje :30 trips looked like garage buses going home. Read at Zásmuky, the Kutná Hora →
  Háje 13:40 / 14:40 make it 4 out, 3 back, hourly; the 2 Nov live map shows buses switching between the ends at Háje. New
  line 381 Zásmuky (3 buses). The same reading was then run on every line of the twelve sheets (`audit/passing_check.py`,
  86 lines flagged for a verdict; `pid-regional/BRANCH_BRIEF.md`). A reviewer handed the designer's reading tends to confirm it:
  check outstation claims against the passing times, never the trip ends.
- **3 Nov:** the PID regional vehicle step had no keep_roster; a first v2 run moved 14 published buses (a chain 365 → 618 →
  600 → 628 to free one bus for a new line). Kept buses are now fixed and published designed buses reserved: 2 moves left.
  Run the change list (old → new) before publishing a sheet the owner may have built.
- **3 Nov:** a second Fable read of the five changes a reviewer (not a designer) had made agreed with all five patterns, but
  369's second slot had been made to pass Step 4 by a hand anchor (15:30); in the builder's window its back row has an empty
  17:12. Anchor removed, the row stays, the one-slot option (−3 buses) is an owner check. Changes made by a reviewer get a
  second reader too.
- **3 Nov (via the fleet desk):** "If something exists in the real PID, it should be modeled... include more liveries where
  needed" → no bus is out of scope for its paint (9034 Arriva City red included); the PID regional builder had put buses with a
  known non-PID paint (DÚK green, DPP city scheme, wraps) on the grey-red object, now they are requested.

## 2 Nov — Prague 130, lines moved to the 2 Nov network
- **2 Nov:** "Decide based on the timetable - is it fair to do the full run or not? As always - are there some stops without
  service" → 130 runs to Filmové ateliéry only 05:10–08:05 and 12:35–16:00; from 15:38 it short-turns at Řeporyjské náměstí and
  X130 (licence 101130, outside the sheet's 100100–100299 range, so never seen by the pipeline) runs Filmové ateliéry – Slivenec.
  The 16:00 peak is the short turn, so the game line is cut back. Before cutting a game line, list who serves each stop it drops
  in the game (here 301, 352, 104, 120, 170 and 105 do) and check the save already turns buses at the new end (100174R does).
- **2 Nov:** "later, look at updated 131 and 176 timetables - maybe the trolleybuses need update as wwell?" → from 2 Nov 131 and 176
  run as trolleybuses 51 and 53 (PID permanent change). Then "You're okay for changed lines to move to 2 Nov network, do not move vehicles
  in lines not affected if possible" → a feed diff found 11 changed bus lines. Moved: 7 of them plus 131/176 gone. Kept: 133, 161/312 and 209
  (temporary closures), 232 (only the route type changed) and 101 (frozen). Check every difference against PID's notices first: the older
  export had itself left out stops that the game already serves (149, 158, 166, 167).
- **2 Nov:** 318 from the PID live map (Mon 2 Nov, polled by the PID regional session): 19 buses on 83 trips. 13 of the 48 peak trips
  ran articulated, so 3 of the 11 counted buses are (Citaro C2 GÜ 7955, 7958; Martin Uher Urbino 18 IV 1161), and the owner was
  right. The buses carry 317 course numbers, but in the peak only 7952 went over to 317, so 317 is not pooled even though
  pooling was pre-approved. The pak already had Urbino 18 IV in VZ-PID; only the type token and the length were missing.

## 3 Nov — Prague circuits from 138 up, the 90-years paint
- **3 Nov:** "Is there any advantage in 138 being one line?" → one bus (12 → 11), at the cost of an 8-entry circuit in place of two
  game lines. Then "for Prague update all lines 138 and above for this rule - if originally it was two lines and you suggest collapsing,
  do it when there is bus saved and something more" → of the cards from 138 up, only 138, 139, 161 + 312, 197 and 226 put two game lines
  into one circuit; 318 and 363 extend one game line. 139, 197 and 226 save 1 bus each with a 4-entry circuit and stay. 138 splits again.
  161 + 312 had been a circuit that saved nothing (7 = 4 + 3): the 20 Oct "≥ 1 bus" check had let it through. The owner chose to split
  it but keep the 186 → 396 through line, both of which had been their own 30 Oct calls, so ask before reversing an owner's earlier
  decision even when a new rule covers it. Size the separate alternative with the same code (patch `circuitize` out), never by hand.
- **3 Nov:** the fleet desk drew the DPP 90-years paint (5025, 5050, trolleybus 509). The second NB 18 livery in the pak made the
  render name the livery on every NB 18, including cards 100–108; those cards now come from `assets/frozen_cards.json` (v20, byte for
  byte), so a pak or render change can no longer reach them.

## 2–7 Nov — Prague trolleybuses 51/53 (the hand-off that never came)
- **7 Nov:** "The trolleybus are not pdated and are not in line with buses, why?" → the bus sheet dropped 131/176 on 2 Nov (v18),
  while the trolleybus half waited for a 51/53 vehicle file the PID regional session was to write on Tue 3 Nov evening. Its
  poller did record the trolleybuses, but the session stopped before writing the file, and nothing tracked the open point, so for
  five days 131/176's peak service was on neither sheet. When one sheet waits on another session, the waiting side reads the
  stored raw data itself once the day has passed, instead of waiting for the file, and both sheets say the point is open.
  Then "yes" → trolleybus v6: 51 1 → 8, 53 1 → 6 from the 3 Nov poll, with 52/58/59 byte-identical. DPP rotates its SNG 12Ts daily
  between 51, 52 and 53, so most of 53's real cars were already on the published 52 card. 53 got 2 of its own map cars, the 512
  it already had, and 3 free SNG 12Ts (designed).

## 7 Nov — Prague 195 + 158
- **7 Nov:** "I see 158 uses 195 buses - design these together then" → 21 of 195's 24 logged courses go over to 158, which has no
  record of its own. Built first as one card with two Simutrans lines (the alternating circuit saved no bus: 19 either way), then,
  asked, "I meant as one line - but ship and publish all" → one circuit in place of 100195 + 100158, keeping the five buses already
  on 100158 (only 5162 parked). "Together" meant one line, not one card. The same publish shipped the X lines and IKEA left
  unpublished on 5 Nov: their 3–4 Nov records never came (seznam-autobusu blocks scripts), so the page now says their buses are
  designed, and IKEA runs on its own bus 9501 from the live map.

## 7 Nov — Prague trolleybus 52 and 58 (study the vehicles)
- **7 Nov:** "STILL NOT GOOD - why? you say 52 has two branches, courses show three, timetable say one, I am dissapointed. Study buses"
  → the 29 Sep sheet had split 52 and 58 into branch lines with the courses divided in course order, "a stated choice" with no
  vehicle evidence, and the spare 52/10 printed a third branch heading. The 3 Nov live map had every trolleybus's trips: every 52
  trolleybus alternates Waltrovka and Jinonice, and the 58 trolleybuses mix Miškovice and Čakovice. v7: each is one line with four
  entries (52 9, 58 13). The same "split in course order, a choice" stands on other city sheets (Brno, Ostrava, Plzeň, Prague
  trams 17/22); check them against vehicle trips whenever a live source exists.
- **7 Nov, later:** "if it needs more, keep it as two lines - just it was not clear. If two lines, look how buses do it. Decide again"
  → v7 had made 52 one line at a cost of one trolleybus; the complaint was the unclear card, not the split. v8: 52 back to 52A
  (Jinonice, 5) + 52B (Waltrovka, 3), laid out like the bus sheet's branch cards, same values and trolleybuses as v6; 58 stays one
  line (13 < 14). Read what the owner objects to before changing the model.

## 7 Nov — Prague 161 and 312
- **7 Nov:** "Is there a reason 161 does not go to Letiště?" → answered "no Letiště trip in either export, the save's 100161 is probably
  left over from an older network". The owner's timetable showed 161 "Bořislavka – Letiště, změna trasy (diversion)": it was a
  diversion. Then "the sheet sends them to Tuchoměřice?" → the 312 rows sit on 161's card, and the game check had read 100161
  against 312's trips. Then "yes, please, model these two properly (and potentially remove them from the regional sheet)" → both on
  the 26 Oct timetables (v23): 161 every 30 at :10/:20; 312 one circuit, hourly to škola and to Špejchar, 3 buses; 312 was not on any
  regional sheet. Before explaining why a line skips a stop, check PID's notices for a diversion.
## 8 Nov — Prague 177 one line
- **8 Nov:** "Could we make 177 one simutrans line? I like it more" → since 28 Oct the card had 177A (Mazurská, 21 buses) and 177B
  (the Chodov – Volha shuttle, 2 buses, "a line to build") and called keeping the save's extension an owner choice. v24: one circuit
  in 100177, which the save already runs that way, at 24 buses (one more). A clear request with a known cost needs no question back:
  build it, and put the cost and the real-life difference (the shuttle's own two buses) on the card.
