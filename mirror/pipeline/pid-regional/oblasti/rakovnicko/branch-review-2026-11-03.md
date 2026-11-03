# rakovnicko: review of the branch re-check, 3 Nov 2026

Independent of the designer's `branch-check-2026-11-03.md`: every EACH WAY flag of `audit-passing-2026-11-03-before.txt`, every
ONE WAY flag with 2 each way, every changed card and every card that says buses go home were re-read from
`data/derived/trips.json` at the flagged stop (passing times, wherever the trip starts or ends) and against the 2 Nov live map
(`scripts/observed.py <line> 2026-11-02`). The coordinator's second `passing_check.py` fix (knot legs) changed one flag after
the designer finished (575, now ONE WAY with 2 each way); it has its verdict below. After my change `run_oblast.py rakovnicko`
runs clean: Step 4 62 timed legs, 61 ok, 1 FEWER (404, explained on the card); branch audit no flag; path audit the three v1
flags (415, 760, 575), explained in the why texts; passing audit 2 lines EACH WAY (304, 711), both named on the cards.

## Per line

| line | verdict | PASS / FIX | what I checked, what I changed |
|---|---|---|---|
| 304 | B / D | PASS | At Stochov, Slovanka II one variant; 13:00 – 15:00 seven to Prague against three back, 15:30 – 17:30 level (3 Rakovník, 4 Kukulova), so the every-120 three-slot rows (window 15:30, 16:00, 16:40 / 15:58, 16:53, 17:23 exact, ±1 on the way back) stand. The Rakovník – Zličín trips are three one way (13:20, 14:00, 15:30) with nothing back from Zličín; live map: 8392 → 305 15:07, 8342 → 404 15:40, 8408 → 404 17:43, as the corrected card says. |
| 415 | A (Žatec – Kadaň) | **FIX** | Read at Žatec, autobusové nádraží, Žatec – Kadaň is hourly both ways 13:30 – 18:30 (towards Kadaň 13:30, 14:35, 15:35, 16:30, 17:30, 18:30; towards Prague 13:30, 14:30, 15:30, 16:25, 17:30, 18:25) while the modelled 415 passes only every 2 h. The odd hours are three each way at a repeating minute (±5): Zličín 13:05, 14:40, 17:00 (there 14:35, 16:30, 18:30) and Kadaň 13:47, 15:47, 17:50 (there 14:30, 16:25, 18:25; the 15:47 and 17:50 end at Žatec). The designer filed C because at Zličín and Kadaň there is no fixed minute; the 381 rule reads at the stop where the variant turns. Added **415 Žatec** every 120: Kadaň 15:47 → Žatec (38 min, the 15:47's path via the Chbany villages), Žatec 16:30 → Kadaň (35 min, the 14:40's path via the Chbany rozcestí stops); `notvia` Praha, Zličín out of Kadaň (the shorts only) and `via` Nové Strašecí, Palackého out of Žatec (the 14:40 only), so neither leg counts 415's own :10 / :50 trips; window slots 15:47 / 16:30 = real, exact; 1 bus. The slots at 14:30 / 18:30 and 13:47 stand for the Zličín 13:05 and 17:00 and the Kadaň 13:47, which 415 lists as off its pattern at the Prague end. Live map: the shorts' buses 8385 (Zličín 13:05 → Kadaň → Žatec 15:47) and 8409 (Zličín 14:40 → Kadaň → Žatec 17:50) are Prague buses on their way home. Note rewritten. 3 → 4 buses. |
| 711 | C | PASS | At Třeboc 15:25, 16:25, 17:55 towards Rakovník and 13:27, 15:02, 16:00, 18:07 towards Louny: no repeating minute; the Louny – Třeboc trips (2 out, 1 back before 19:00) are named on the card. |
| 561 | C | PASS | Single school trips to Senomaty, Nouzov, Petrovice, Řeřichy and the town loop; the Senomaty 17:33 is carried by 581 Senomaty. |
| 562 | C / D | PASS | Trips to and from the Transdev garage stop at no repeating minute; all on the card. |
| 584 | C | PASS | Out 13:15, 14:30 (Vinařice), 15:30, 16:30 to three ends; back 13:00, 14:00 from Lhota pod Džbánem and 16:51, 18:51 from Krupá, Šustna (which start short of Mutějovice): two phases, nothing three times each way. |
| 575 | C | PASS (verdict added) | Newly ONE WAY 2 each way at Všetaty, rozcestí Lašovice after the knot fix: out 14:47 (Zvíkovec), 15:19 (Tytry), 16:12 (Slabce, pošta), 17:12 (Kostelík); back 13:16, 14:12, 15:42, 16:12, 18:17 from five different ends. School-day single trips, all named on the card; every 144 on one bus stands. |
| 404 | D | PASS | Out of Zličín :10 and :40 hourly; towards Prague nothing passes Ruda, u rybníka after 15:45. Live map: 8344 (15:10), 8343 (17:10), 8402 (18:10) end in Rakovník; 8389 (16:10) goes on as a 581 at 17:11. The Step 4 FEWER row stays explained. |
| 576 | D | PASS | Out 13:30, 14:40, 15:30, 16:30, 18:30; back 16:04 only. Live map: 8390 14:40 → 16:04 (the modelled round); 8330 16:30 → 574 at 17:21; 8342 18:30 is the 304 / 404 bus 8342 going home. The corrected card holds. |
| 578 | C | PASS | The flag was the loop-line artefact; gone after the first passing_check fix. |
| 560, 760 | C / E | PASS | School-day extras around the alternating hourly pattern (560); the :04 back trips via Vroutek and Kryry against the game line's path via Podbořany, nemocnice (760), as the cards say. |
| 563 | D | PASS | Live map: 8383 runs 563 11:00, 12:24, 14:35, 15:54 and ends at Milostín; 8373 runs the 17:30 to Mutějovice and is not seen again. |

Grep of `lines.json` for "going home", "garage", "outflow", "outstation", "sleep": the claims are on 304, 404, 563 and 576 only;
all four checked above on the live map.

Oblast `notes`: unchanged (the 304 Zličín question is settled there by the designer).

## Totals
Simutrans lines: v1 30 → designer 30 → review 31 (415 Žatec). Buses: v1 47 → designer 47 → review **48** (+1 for 415 Žatec).
