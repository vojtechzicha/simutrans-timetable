# Rail line design rules (Simutrans fork)

These rules were worked out with the user on 3 Oct 2026, while designing the local lines 062, 064, 064N, 010S, 010, 260 Os and 260 Sp.
The result is `Local Trains 010 062 064 260.html`. The user called it "lovingly gotten correct".
They apply to every rail sheet: local trains, MD-CR long-distance, RegioJet and Leo Express.

## 1. Find what really runs
- **Source:** the national CIS JŘ timetable (`md-cr/data/derived/trains.json`, one record per train with a day bitmap).
- **Day:** a normal workday.
  - Check all five days Mon–Fri of an ordinary week (e.g. 5–9 Oct 2026). A train counts only if it runs every day you model.
  - Public holidays are not workdays. A weekend train that shows up on a Monday or Wednesday holiday is still a weekend train.
  - Seasonal workday trains are not part of the standard model. This covers summer-only trains (e.g. Mladějov – Lomnice nad Popelkou, 5 June – 31 August) and Friday-only trains (e.g. 076). List them, and offer a separate version if the user wants one.
- **Lines:** the user names local lines by KJŘ table number (062 = Nymburk – Mladá Boleslav, 076 = Mladá Boleslav – Mšeno – Mělník). Check the station sequence in the data before you name a route; don't trust memory.
- **Categories:** for local lines the user wants Os and Sp only. Ignore long-distance trains and, when asked, other carriers (e.g. Arriva R22 on 062).
- **Look at the whole day,** then design from the afternoon. List every train with its real times, its origin and destination beyond the line, and its stop pattern. The stop pattern includes request stops (x, TrainActivityType 0030) and stations that are passed without stopping.
- **Find every train on the line, not only the ones that reach its ends (user, 5 Oct 2026).**
  - Search by **every station of the line** and group the trains by the stretch of the line they run. Searching only by the termini once missed 014 Kolín – Uhlířské Janovice, 235 Kutná Hora hl. n. – Kutná Hora město and 012 Pečky – Bošice / Plaňany. The user had to point the first two out from memory.
  - Typical patterns to expect:
    - peak short workings to an intermediate station;
    - town-only shuttles at one end;
    - through trains from a neighbouring line;
    - trains that run one stop past the usual terminus.
  - Every stretch must be either modelled or listed under Not modelled, with its trains and times, **before** the design is shown.
  - `local-rail/build_012_014_235.py` does this in `inventory()`. It stops the build on any undecided stretch, and the page shows an "Every workday train on these lines" table. New line scripts must keep this check.
  - **Also check every junction for branch lines with no workday trains (user, 13 Oct 2026).** Březnice – Rožmitál pod Třemšínem runs only on weekends and holidays, in season. The inventory, which looks at workday trains on the line's own stations, could not see it, and the user missed it.
    - List every train on any day that touches exactly one station of the sheet. These are branches and other lines leaving at a junction.
    - Put each one either on the page or under Not modelled. Say plainly when a branch has no workday service.
    - A branch with no workday service is not modelled (user, 13 Oct 2026: "If rožmitál has no weekday service, it should not be in"). List it under Not modelled with its days and times.
  - A data record can have several date variants under the same train number. Use the one that runs on the modelled workdays.
- **Whole minutes only (user, 5 Oct 2026).** The game has no half minutes. Show every time rounded down, as the printed timetable does, and compute stays from the rounded times.

## 2. Model the real structure ("most like the real thing")
- **One Simutrans line per real train pattern.** A Simutrans line runs all day at one interval. "Also at" cannot change the route.
- **Through-running:** join two patterns into one line only where the real trains do run through.
  - Never extend a line past its real terminus to save a vehicle. 010 stays Kolín – Svitavy and must not reach Letovice.
- **Real trains that run through only sometimes** become their own line. Example: the two Kolín – Svitavy pairs became 010S.
  - Give that line the hours the regular line doesn't use, so the two alternate. Accept the extra vehicle this costs.
- **Real trains the user cares about must be modelled,** even when they are only a short episode in reality. Ask before dropping a train as a tail.
- **Branches and short workings:** a separate line, with offsets that interleave with the main line. Example: 064N carries the Nymburk extras of 064.
- **Keep stays at big main-line stations short (user, 5 Oct 2026).** Examples: Kolín, Pečky, Kutná Hora hl. n.
  - Where a long and a short branch line turn at the same main-line station, check whether one shared circuit line would cut the stay. Example: 014 Kolín → Ledečko → Kolín → Uhlířské Janovice → Kolín went from 91 to 31 min at Kolín and from 4 to 3 vehicles.
  - Set the shared station to stop type **terminal** in each of its entries (the fork supports it), so nobody rides through.
  - **Share a line only where the same vehicles really run both parts.** Check vagonweb.cz řazení for the planned type and the sighted units per date. Same-day sightings show how a unit moves between trains. `local-rail/vagonweb.py` does this; vagonweb needs `zeme=ČD` URL-encoded, plus a session cookie and a referer.
  - If the types differ, or the units don't move between the two parts, keep separate lines. Example: the 235 Kutná Hora město shuttle runs on 810s of its own.
  - Don't move real times to shorten a stay. If the real arrival and departure minutes fix the stay, say so (Pečky: in :46, out :12).
- **Lines that share a section get opposite hours,** so they alternate on that section in both directions.
  - Check both directions. Extending one line by an hour flips its return parity. Example: 064 to Lomnice collided with 064N inbound.
- **Uneven combined headways at a shared station are fine.** The user likes them (Nymburk 062 L:04 and 064N L:32). Don't "fix" them unless asked.
- **Two lines must never leave the same station, in the same direction, in the same minute.**

## 3. Timetable values (fork)
- **Interval:** 60 or 120 min for these lines, taken from the afternoon clock-face pattern. Use the real minute. Rail has no loop rule.
- **Offsets:** odd hours come first (user, 3 Oct 2026).
  - With interval 120: offset = minute for odd hours (L:04 → 4) and minute + 60 for even hours (S:06 → 66).
  - With interval 60: offset = minute.
  - For any other interval (240), confirm the convention with the user first.
- **Leave up to:** 30 min on every entry at interval 120. Automatic at 60.
- **Timed stops (timetable entries).** Set them per direction:
  - every terminus departure;
  - every stop where the train stays **5 min or more** (crossings such as Dolní Bousov 7 min, long stops such as Přelouč 11–13 min, Záboří 8 min, Choceň 6 min, Zámrsk 5–6 min);
  - every junction or wait point where the line waits for its slot (Česká Třebová 9 min, MB hl. n. 10 min);
  - every station where the train **reverses** (changes direction), whatever its stay. Example: Leo Express at Přerov, 4 min (user, 4 Oct 2026). In `v4_lines.json` this is `force_timed`.
- **Check each timed departure against the arrival there.** A departure must come after the arrival. 064N at MB hl. n. was :38 while trains arrived at :38; it was fixed to :41.
- **Important stations, not every stop (user, 4 Oct 2026).** Time the real termini, stays of 5 min or more, the stop before Brno hl. n., and the line's important stations. For R9 those are Kolín, Havlíčkův Brod and Tišnov (`timed` in `v4_lines.json`). An every-stop version was rejected.
- **Never invent dwell times.** Use real times only.
- **The stop before Brno hl. n. is always timed (user, 4 Oct 2026),** in each direction, at its real departure. Examples: Pardubice or Česká Třebová (Ex3), Brno-Židenice (RegioJet), Brno-Královo Pole (R9) and Blansko (R19) going south, and Břeclav going north.
  - **Do not move any stay off Brno hl. n.** Brno keeps its real stay, and it is timed by the usual 5-minute rule. One session cut Brno to 1 min and moved the wait to the stop before; the user rejected that.
  - In `v4_lines.json` this is `time_before`.
- **Depot ends (user, 4 Oct 2026).** The R lines Praha – Brno start and end at the odstavné nádraží at both cities.
  - **Praha:** R9/R19 really start and end at Praha-Vršovice (a passenger stop), running from and to the depot Praha Jih. Use those real times. Check the raw data for depot runs before assuming the hl. n. is the terminus.
  - **Brno:** the 15 min from the depot cover the run and the dwell at the hl. n. together.
  - The depot departs 15 min before the real hl. n. departure, and the train reaches the depot 15 min after the real hl. n. arrival.
  - Each real terminus (hl. n.) is timed in both directions: at its real departure, and on the arriving side at its real arrival minute (the train then leaves for the depot).
  - In `v4_lines.json` this is `depot`.
- **Long waits go where there is room** (MB hl. n., not MB město). Ask the user when unsure.
- **Operator turn limits (user):** Leo Express turns at Praha hl. n. in 20 min at most. Move its return slot, not the Praha departure, and say by how much on the page.
- **Real tight turns** (010 at Česká Třebová, in at :58, out at :59) may stay. Say that the long stops on the way back win the time back.

## 4. Vehicles
- **For every line, write one vehicle's full round trip** with clock times: departure, timed stops, arrival, the wait at each end, and back to the same departure.
- **The round trip must be a whole multiple of the interval.** The vehicle waits for its next slot, so 2 h 14 min at interval 120 becomes 4 h.
- **Vehicles = round trip ÷ interval.** Show the arithmetic.
- **Say where the slack sits** (e.g. 1 h 46 min at MB hl. n., 1 h 28 min at Kolín).

## 5. Presentation
- **Simple page, like the chat tables.** The user doesn't like the MD-CR look. Use one plain column, light and dark themes, and no decoration.
  - Start with a vehicle summary table: line, route, every, round trip, vehicles, area totals.
  - For each area, list in a few bullets how the lines share track, per direction.
  - For each line, give:
    - the stations, with (x) for request stops;
    - a timetable entries table: stop, direction, every, offset, real time (L/S notation), stay;
    - the round trip table, with long stays highlighted;
    - the real trains it matches, with train numbers;
    - the differences from reality.
  - End with a "Not modelled" list.
- **Corrections to earlier advice** are marked visibly on the page.
- **Notation:** L = odd hours, S = even hours. Use full station names; expand data abbreviations (Záboří n.L. → Záboří nad Labem).
