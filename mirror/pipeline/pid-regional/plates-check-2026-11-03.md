# Plates check of the "going home" cards — 3 Nov 2026, evening

Why: after the branch re-check the owner asked about 402 (Roztyly → Zruč 15:20, 17:35, 18:20, filed as "buses going home").
The designer and the Fable reviewer both had the passing times at Zruč and two of the plates, but the sentence they wrote
as the reason was about where trips start ("Zruč starts 4:24, 6:29 only"), the 381 mistake in words, after the rule had
been changed. So the check is now mechanical: `scripts/plates_check.py`
(run by `run_oblast.py`, writes `data/derived/audit-plates.txt`) takes every trip the passing audit lists as off the pattern
and looks up on the live map (2 and 3 Nov) what its bus did next: ended its day, ran another line, or came back on the line
(on a slot, or off the pattern too). CHECK = a card saying the buses go home / sleep out, where most buses in the main
direction came back.

## 402 — the verdict was right
Read at Zruč nad Sázavou 13:00–19:00 the trips no slot passes are 15:20, 16:35 (15 min late) and 17:35 out (the 18:20 is on
the slot) and only 15:19 back: every trip towards Prague comes from Čáslav and the every-120 slot passes 14:19, 16:19 and
18:19, leaving the 14:36 from Čáslav. 3 out, 1 back, not a branch (381 had 4 out, 3 back at :21). On 3 Nov
7925, 7671 and 7672 left Zruč at 4:24, 4:36 and 6:29 and ended their day there on the 15:20, 17:35 and 18:20 (the same three
on 2 Nov). The card now gives these counts and the plates. Every 120 stays (3 buses); hourly would double the off-peak, which
runs every 2 h all day.

## The 39 cards with "going home / sleep / garage / outstation"
10 are not flagged by the passing audit at all (fewer than 3 trips off the pattern either way: 381, 387, 771, 600, 720, 653,
311, 428, 522, 563). Of the rest, no model was wrong. Four cards described the buses wrongly and are corrected (wording only,
no typed value or bus changes):
- **340** — the :23 / :53 are peak extras whose buses come back empty (8880 / 8801 and 1468, four of five runs), not buses
  going home.
- **371** — the Astrapark extras 15:53, 16:08, 16:53: their buses were back at Kobylisy with no trip and went out again
  17:08–17:40; only the 16:23 bus ended its day. "Outstation end" → "outflow end".
- **370** — the Odolena Voda / Postřižín extras: most buses come back to Kobylisy empty (8198 after the 14:45, 1241 after the
  16:45), not "the buses sleep at Odolena Voda".
- **360** — the card had the buses the wrong way round: the :45 buses (13:45–16:45) go on from Sedlčany as 450, 549, 551,
  552; the :15 buses come back on the :15 two hours later (7209, 7201, 7202), and the 17:15 and 18:15 end there. The :45
  slot stays: the line's minute all day, and the game bus turns in 3 min (3 buses; with :15, 4).

## CHECK lines that stay, with their verdict
| Line | CHECK | Verdict |
|---|---|---|
| 300 | 9 of 15 Veleslavín → out came back | The card's "sleep" sentence is the morning; the plates are on the card (five Kladno shorts come back as the Rozdělov trips, 8883's Hřebeč runs one way). Kladensko review checked them on the 2 Nov map. Right. |
| 669 | 3 of 4 came back | The flagged trips are the via-Křenek path variants (15:35, 17:35), whose buses come back on the slot trips 16:18, 18:13. The model already runs 6 out, 6 back 15:00–19:00 against the real 6 / 5. Right. |
| 360 | 4 of 6 / 3 of 5 came back | The :15 buses come back on the :15 slot; card corrected (above). The "sleep at Sedlčany" sentence is the morning (7:10 and earlier into Prague; 7227, 7232 end there). Right. |
| 520 | 3 of 3 came back | Bus 9604's local Dobříš – Hřiměždice / Daleké Dušníky trips, irregular minutes; the card's "sleeps" is 520 Kamýk's bus, other trips. Right. |
| 361 | 4 of 6 / 3 of 5 came back | Bus 1120's local Dobříš – Nový Knín / Stará Huť trips (irregular); the card already says the Dobříš buses turn and come back (every 60 since the re-check). Right. |
| 304 | 6 of 7 came back | The card already says the 13:00–15:00 Rakovník buses come back from Kukulova 14:38–16:53; "sleep in Rakovník" is the morning. Right. |
