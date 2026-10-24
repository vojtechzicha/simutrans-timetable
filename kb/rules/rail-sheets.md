# Rail sheets

The approved method (owner, 3 Oct 2026: "lovingly gotten correct") is `mirror/pipeline/rail-design-rules.md` — read it in full
before any rail sheet. This page is the summary plus every later ruling. Long-distance details: `mirror/pipeline/md-cr/README.md`;
local lines: `mirror/pipeline/local-rail/README.md` (one section per sheet).

## Method in short
- **Real workday trains, Mon–Fri** of an ordinary week; a train counts only if it runs every modelled day. Holidays aren't workdays.
  Seasonal and Friday-only trains are listed, not modelled. A branch with **no workday service is not modelled** (Rožmitál, 13 Oct).
- **Find every train** (5 Oct, 13 Oct): search by every station of the line, group by stretch (peak short workings, town shuttles,
  through trains, one-stop-past runs). At every junction also list trains *on any day* touching one station of the sheet. Every
  stretch is modelled or listed under Not modelled **before** the design is shown. `inventory()` in
  `local-rail/build_012_014_235.py` enforces it.
- **Model the real structure:** one Simutrans line per real train pattern; join only where trains really run through; never extend
  past a real terminus (010 stays Kolín – Svitavy). Partial through trains get their own line in alternate hours. Trains the owner
  cares about are modelled even if short-lived — ask before dropping.
- Lines on a shared section alternate hours; uneven combined headways are fine ("don't fix, I like it uneven").
- **Frequency** comes from the afternoon peak in the peak direction (R49 is hourly Praha–Benešov). Don't average the day.
  One headway per line judged from both ends together (Kysučan is 4-hourly).
- **Offsets odd hours first:** offset = (real − 60) mod interval. Leave up to 30.
- **Timed stops:** termini, every stay ≥ 5 min, every wait/crossing/overtake point, per direction; each timed departure after the
  arrival. The stop before Brno hl. n. gets a timed entry, but Brno's own stay is **never** moved onto it.
- **Vehicles:** full clock round trip, rounded up to a multiple of the interval; vehicles = round trip ÷ interval.
- Whole minutes only.
- **Page:** plain, chat-like tables ("I don't love MD-CR - keep it simple as you did here in chat"). Don't restyle city sheets.

## Depots, stays, sharing
- Keep stays at big main-line stations short (Kolín, Pečky, Kutná Hora hl. n., Praha hl. n. — "not more than 10–20 minutes";
  Leo Express turns at Praha hl. n. in ≤ 20 min).
- Depot runs only with concrete evidence (CIS empty runs / raw locations), e.g. R26 Malešice, R23 stabled at Ústí západ, R20/Ex5/R15
  to Praha Jih (= Praha odstavné nádraží), R9/R19 from odstavné nádraží 15 min beyond hl. n. (owner rule). No invented dwells.
- Share one Simutrans line between long and short runs **only if the same vehicles run both** — check vagonweb řazení
  (`local-rail/vagonweb.py`; needs `zeme=%C4%8CD`, a PHPSESSID cookie and a referer).
- Offer the realistic variant (sidings, empty runs) but expect the owner may prefer the simpler line once both are shown
  (210 at Praha hl. n.). Decide one-off workings yourself ("model what happens in reasonable matters").
- Use Also at (interval 240) for uneven hourly patterns before adding lines.
- Prefer one uniform pattern on real trains that cross at real crossing stations (S57/U12); check with `local-rail/check_meetings.py`.
- Station capacity limits from the owner: Praha-Bubny max 4 trains; Rokycany up to 3.

## Engineering works (14 Oct 2026)
CIS JŘ annual data has **no výluky**. Before presenting a rail sheet check `pid.cz/zmeny/?type=vlaky` and the carrier's notices;
ČD works PDFs: `https://www.cd.cz/jizdni-rad/tratove-jizdni-rady/files/cz-k<KJŘ>-2026vyluka<NN>.pdf` (read with pymupdf word
coordinates). Model works lasting many months (Masarykovo nádraží closed 1 Jun – 12 Dec 2026 → S5/R45/R24/S54 end at Praha-Bubny);
leave the regular timetable for works ending within weeks; list both kinds. When a line has a works state and a final state, show
both in full (S6 until 19 Oct).

## Game facts (what is built in the owner's save)
- **Track ends:** Rokycany, Blatná, Čimelice (west), Veselí nad Lužnicí (Praha – Tábor line), Blatno u Jesenice, Most (U12),
  Ústí nad Labem on the S4 corridor. Lovosice branches not built; Mšeno built but no workday trains. Treat these as hard ends.
- East sector was built by hand by the owner: check the save's line list before adding lines (S4 sheet adds only missing lines).
  Ask the fleet desk / engine session for a headless export when the game is closed.
- Placeholder lines without vehicles exist in the save (Ex6/1–4, Os123 [U13]).

## Naming conventions in CIS JŘ data
- Owner names local lines by KJŘ table number (062 = Nymburk – Mladá Boleslav, 076 = MB – Mšeno – Mělník). Check the station
  sequence in the data, don't trust memory.
- PID S-line = service 1000 + n (S49 = 1049), R-line = 1100 + n (R49 = 1149), U-line (Ústecký) = 4000 + n (U12 = 4012).
  Long-distance grouping uses `CZPassengerServiceNumber`.
- Carrier = ResponsibleRU: 1154 ČD, 3246 RegioJet, 3752 RegioJet ÚK, 3616 Leo Express, 3736 Trilex. Passenger stop =
  TrainActivityType 0001/0028/0029/0030 (0030 = request stop).
- Foreign ends (long distance): lines end at the first station after the border (Čadca, Chałupki, Zebrzydowice, Púchov, Kúty/Hohenau
  + 10 min per station beyond).

## Refresh
The rail data is JR2026 (`ftp.cisjr.cz/draha/celostatni/szdc/2026/JR2026.zip`, parsed by `md-cr/scripts/01_parse.py` into
`md-cr/data/derived/trains.json`). The national timetable changes on **13 Dec 2026** (JR2027): every rail sheet needs a refresh then
(RegioJet ÚK takes over U1/U3/U32/U51/U54).
