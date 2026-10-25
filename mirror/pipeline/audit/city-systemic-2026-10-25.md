# City sheets: rule checks


Per row (one terminus entry): interval P, slots `real` (clock minutes mod P from midnight) and typed `set`.
  ORIGIN  typed values are not (real - 60 - 1 at loops) mod P: the fork counts offsets from 01:00 (owner, 3 Oct; fixed on the
          Ostrava sheets 20 Oct). Only intervals not dividing 60 can differ; the error is (60 mod P) minutes.
  RANGE   a typed value outside 0..P-1, not a whole minute, or more than 8 slots (Offset + 7 Also at)
  FOLD    two or more evenly spaced slots not written as the plain interval ("every 60, Offset 17, Also at 47" is every 30)
  RATE    the two directions of one terminus pair have different departures per hour (both ends at the same rate)
Approximate rows (exact = false) are counted, not judged here.
| Pipeline | Source | Rows | Approximate | ORIGIN | RANGE | FOLD | RATE |
|---|---|---|---|---|---|---|---|
| praha | data\derived\2026-10-12\timetable.json | 58 | 1 | 53 | 0 | 0 | 2 |
| praha-trolleybus | data\derived\2026-09-27\timetable.json | 14 | 4 | 4 | 0 | 0 | 0 |
| brno | data\derived\from-2026-09-29\timetable.json | 26 | 0 | 2 | 0 | 0 | 0 |
| brno-bus | data\derived\2026-09-29\timetable.json | 90 | 4 | 0 | 0 | 0 | 0 |
| brno-trolleybus | data\derived\2026-09-29\timetable.json | 36 | 0 | 0 | 0 | 0 | 0 |
| plzen | data\derived\2026-09-27\timetable.json | 8 | 0 | 4 | 0 | 0 | 0 |
| plzen-bus | data\derived\2026-09-29\timetable.json | 47 | 6 | 0 | 0 | 0 | 1 |
| plzen-trolleybus | data\derived\2026-09-29\timetable.json | 26 | 11 | 6 | 0 | 0 | 0 |
| olomouc | data\derived\2026-09-27\timetable.json | 14 | 0 | 0 | 0 | 0 | 0 |
| olomouc-bus | data\derived\2026-09-29\timetable.json | 37 | 3 | 1 | 0 | 0 | 0 |
| most-litvinov | derived/schedule.json | 8 | 0 | 0 | 0 | 0 | 0 |
| most-litvinov-bus | derived/schedule.json | 30 | 0 | 1 | 0 | 0 | 2 |
| ostrava | derived/schedule.json | 34 | 0 | 0 | 0 | 0 | 0 |
| ostrava-trolleybus | derived/schedule.json | 22 | 0 | 0 | 0 | 0 | 0 |
| ostrava-bus | derived/schedule.json | 146 | 28 | 2 | 0 | 0 | 0 |
| havirov-karvina-orlova | derived/schedule.json | 66 | 31 | 0 | 0 | 0 | 0 |

## Rows

| Pipeline | Check | Line | Entry | Every | Real | Typed | Expected / note |
|---|---|---|---|---|---|---|---|
| praha | ORIGIN | 1 | Sídliště Petřiny → Výstaviště | 8 | [7] | [6] | [2] |
| praha | ORIGIN | 1 | Výstaviště → Sídliště Petřiny | 8 | [3] | [2] | [6] |
| praha | ORIGIN | 2 | Náměstí Bratří Synků → Sídliště Petřiny | 8 | [1] | [0] | [4] |
| praha | ORIGIN | 2 | Sídliště Petřiny → Náměstí Bratří Synků | 8 | [4] | [3] | [7] |
| praha | ORIGIN | 3 | Březiněveská → Levského | 8 | [2] | [1] | [5] |
| praha | ORIGIN | 3 | Levského → Březiněveská | 8 | [7] | [6] | [2] |
| praha | ORIGIN | 4 | Čechovo náměstí → Radlická | 8 | [5] | [4] | [0] |
| praha | ORIGIN | 4 | Radlická → Čechovo náměstí | 8 | [3] | [2] | [6] |
| praha | ORIGIN | 5 | Nádraží Holešovice → Slivenec | 8 | [2] | [2] | [6] |
| praha | ORIGIN | 5 | Slivenec → Nádraží Holešovice | 8 | [0] | [7] | [3] |
| praha | ORIGIN | 6 | Nádraží Holešovice → Kubánské náměstí | 8 | [0] | [0] | [4] |
| praha | ORIGIN | 6 | Kubánské náměstí → Nádraží Holešovice | 8 | [3] | [2] | [6] |
| praha | ORIGIN | 7 | Kotlářka → Bílá labuť | 8 | [2] | [1] | [5] |
| praha | ORIGIN | 7 | Bílá labuť → Kotlářka | 8 | [6] | [6] | [2] |
| praha | ORIGIN | 8 | Starý Hloubětín → Nádraží Podbaba | 8 | [7] | [6] | [2] |
| praha | ORIGIN | 8 | Nádraží Podbaba → Starý Hloubětín | 8 | [2] | [1] | [5] |
| praha | ORIGIN | 11 | Spořilov → Ústřední dílny DP | 8 | [5] | [4] | [0] |
| praha | ORIGIN | 11 | Ústřední dílny DP → Spořilov | 8 | [3] | [2] | [6] |
| praha | ORIGIN | 12 | Lehovec → Sídliště Barrandov | 8 | [6] | [5] | [1] |
| praha | ORIGIN | 12 | Sídliště Barrandov → Lehovec | 8 | [6] | [5] | [1] |
| praha | ORIGIN | 13 | Olšanské hřbitovy → Zvonařka | 8 | [0] | [7] | [3] |
| praha | ORIGIN | 13 | Zvonařka → Olšanské hřbitovy | 8 | [1] | [1] | [5] |
| praha | ORIGIN | 15 | Olšanské hřbitovy → Sídliště Barrandov | 8 | [6] | [5] | [1] |
| praha | ORIGIN | 15 | Sídliště Barrandov → Olšanské hřbitovy | 8 | [2] | [1] | [5] |
| praha | ORIGIN | 17 | Březiněveská → Libuš | 8 | [7] | [6] | [2] |
| praha | ORIGIN | 17 | Libuš → Březiněveská | 8 | [5] | [5] | [1] |
| praha | ORIGIN | 17 | Vozovna Kobylisy → Levského | 8 | [0] | [7] | [3] |
| praha | ORIGIN | 17 | Levského → Vozovna Kobylisy | 8 | [5] | [4] | [0] |
| praha | ORIGIN | 18 | Vozovna Pankrác → Nádraží Podbaba | 8 | [6] | [5] | [1] |
| praha | ORIGIN | 18 | Nádraží Podbaba → Vozovna Pankrác | 8 | [6] | [5] | [1] |
| praha | ORIGIN | 19 | Pankrác → Depo Hostivař | 8 | [5] | [5] | [1] |
| praha | ORIGIN | 19 | Depo Hostivař → Pankrác | 8 | [3] | [2] | [6] |
| praha | ORIGIN | 20 | Dědina → Levského | 8 | [2] | [1] | [5] |
| praha | ORIGIN | 20 | Levského → Dědina | 8 | [3] | [2] | [6] |
| praha | ORIGIN | 21 | Slivenec → Kubánské náměstí | 8 | [4] | [3] | [7] |
| praha | ORIGIN | 21 | Kubánské náměstí → Slivenec | 8 | [4] | [3] | [7] |
| praha | ORIGIN | 22 | Bílá Hora → Zahradní Město | 8 | [2] | [1] | [5] |
| praha | ORIGIN | 22 | Nádraží Hostivař → Vypich | 8 | [4] | [3] | [7] |
| praha | ORIGIN | 22 | Zahradní Město → Bílá Hora | 8 | [6] | [5] | [1] |
| praha | ORIGIN | 22 | Vypich → Nádraží Hostivař | 40 | [2, 10, 26] | [1, 9, 25] | [5, 21, 29] |
| praha | ORIGIN | 23 | Bílá labuť → Královka | 32 | [26] | [26] | [30] |
| praha | ORIGIN | 24 | Vozovna Kobylisy → Spořilov | 8 | [3] | [2] | [6] |
| praha | ORIGIN | 24 | Spořilov → Vozovna Kobylisy | 8 | [0] | [7] | [3] |
| praha | ORIGIN | 25 | Výstaviště → Bílá Hora | 8 | [7] | [6] | [2] |
| praha | ORIGIN | 25 | Bílá Hora → Výstaviště | 8 | [5] | [4] | [0] |
| praha | ORIGIN | 26 | Dědina → Nádraží Hostivař | 8 | [6] | [5] | [1] |
| praha | ORIGIN | 26 | Nádraží Hostivař → Dědina | 8 | [7] | [6] | [2] |
| praha | ORIGIN | 30 | Sídliště Ďáblice → Spojovací | 8 | [3] | [2] | [6] |
| praha | ORIGIN | 30 | Spojovací → Sídliště Ďáblice | 8 | [5] | [4] | [0] |
| praha | ORIGIN | 31 | Spojovací → Vysočanská | 8 | [2] | [1] | [5] |
| praha | ORIGIN | 31 | Vysočanská → Spojovací | 8 | [5] | [4] | [0] |
| praha | ORIGIN | 37 | Spojovací → Lehovec | 8 | [0] | [7] | [3] |
| praha | ORIGIN | 37 | Lehovec → Spojovací | 8 | [0] | [7] | [3] |
| praha | RATE | 22 | Nádraží Hostivař → Vypich |  |  |  | 7.50 vs 4.50 an hour |
| praha | RATE | 23 | Královka → Bílá labuť |  |  |  | 3.00 vs 1.88 an hour |
| praha-trolleybus | ORIGIN | 52 | Na Knížecí → Waltrovka | 8 | [7] | [6] | [2] |
| praha-trolleybus | ORIGIN | 52 | Na Knížecí → Jinonice | 8 | [3] | [2] | [6] |
| praha-trolleybus | ORIGIN | 52 | Jinonice → Na Knížecí | 8 | [2] | [1] | [5] |
| praha-trolleybus | ORIGIN | 52 | Waltrovka → Na Knížecí | 8 | [3] | [2] | [6] |
| brno | ORIGIN | 12 | Technologický park → Komárov | 14 | [4, 8, 13] | [3, 7, 12] | [3, 8, 13] |
| brno | ORIGIN | 12 | Komárov → Technologický park | 14 | [4, 9, 13] | [3, 8, 12] | [4, 8, 13] |
| plzen | ORIGIN | 4 | Košutka → Bory | 8 | [0] | [7] | [3] |
| plzen | ORIGIN | 4 | Bory → Košutka | 8 | [6] | [5] | [1] |
| plzen | ORIGIN | 4 | Košutka → Univerzita | 8 | [4] | [3] | [7] |
| plzen | ORIGIN | 4 | Univerzita → Košutka | 8 | [0] | [7] | [3] |
| plzen-bus | RATE | 26 | Bory → Lhota |  |  |  | 1.00 vs 2.00 an hour |
| plzen-trolleybus | ORIGIN | 10 | Tylova → Čechurov | 24 | [20] | [19] | [7] |
| plzen-trolleybus | ORIGIN | 10 | Čechurov → Tylova | 24 | [1] | [0] | [12] |
| plzen-trolleybus | ORIGIN | 10 | Tylova → Černice | 24 | [8] | [7] | [19] |
| plzen-trolleybus | ORIGIN | 10 | Černice → Tylova | 24 | [8] | [7] | [19] |
| plzen-trolleybus | ORIGIN | 12 | Božkov → Nová Hospoda | 45 | [6, 14, 21, 28, 35, 43] | [5, 13, 20, 27, 34, 42] | [5, 12, 19, 27, 35, 43] |
| plzen-trolleybus | ORIGIN | 16 | Sídliště Bory → Doubravka | 48 | [6, 13, 18, 24, 29, 35, 41, 47] | [5, 12, 17, 23, 28, 34, 40, 46] | [0, 5, 11, 16, 22, 28, 34, 41] |
| olomouc-bus | ORIGIN | 27 | Tržnice → Tržnice | 45 | [16] | [15] | [0] |
| most-litvinov-bus | ORIGIN | 10 | Most, nádraží → Obrnice, sídliště | 45 | [11, 41] | [10, 40] | [25, 40] |
| most-litvinov-bus | RATE | 10 | Most, nádraží → Obrnice, sídliště |  |  |  | 2.67 vs 2.00 an hour |
| most-litvinov-bus | RATE | 13 | Lom, Loučná, Libkovická → Litvínov, Janov, otočka |  |  |  | 2.00 vs 4.00 an hour |
| ostrava-bus | ORIGIN | 41 | Hrabůvka, Poliklinika → Vratimov, náměstí | 60 | [22] | [22] | [21] |
| ostrava-bus | ORIGIN | 41 | Hrabůvka, Poliklinika → Vratimov, Kartonážka | 60 | [52] | [52] | [51] |
