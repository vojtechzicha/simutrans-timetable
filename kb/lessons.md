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
