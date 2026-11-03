# Pak requests from the PID regional sheets

From pipeline/pid-regional/scripts/04_vehicles.py (2026-11-02 live map). Buses on the twelve oblast sheets whose type and livery have no object in VZ-PID-bus (regional) or VZ-MHD<Town>-bus (town lines). They are shown as "requested" on the sheets, never as a stand-in (rules/pak-objects.md). "?" = the vehicle window of the live map names no type for the bus (and the bus is not in the register); the second poll day may name it.

| Real type | Wanted object | Buses | Operators | Paint (register) | Example numbers | Sheets |
|---|---|---|---|---|---|---|
| ? | ? (paint unknown) | 6 | ČSAD Benešov 2, Okresní autobusová doprava Kolín 2, ARRIVA STŘEDNÍ ČECHY 1, ČSAD AUTOBUSY České Budějovice 1 | paint not in the register 6 | 1000, 17265, 7965, 7966, 8610, 8624 | benesovsko, kolinsko, nymbursko, pribramsko |
| Iveco Crossway LE LINE 14,5M | VZ-PID-Crossway_LE_Line_14_5M-<bílá & polep VDV, zelené šipky> (Iveco Crossway LE LINE 14,5M) | 4 | ČSAD AUTOBUSY České Budějovice 3, ABOUT ME 1 | bílá & polep VDV, zelené šipky 4 | 18151, 18152, 18153, 18154 | benesovsko |
| Iveco Crossway LE LINE 10,8M | VZ-PID-Crossway_LE_Line_10_8M-<bílá & polep VDV, zelené šipky> (Iveco Crossway LE LINE 10,8M) | 4 | ČSAD AUTOBUSY České Budějovice 4 | bílá & polep VDV, zelené šipky 4 | 18101, 18102, 18104, 18106 | benesovsko |
| Scania Citywide LE 12M | VZ-PID-Citywide_LE_12M-<Doprava Ústeckého kraje, zelená> (Scania Citywide LE 12M) | 4 | Dopravní společnost Ústeckého kraje 4 | Doprava Ústeckého kraje, zelená 4 | 12536, 12555, 12557, 12559 | kladensko |
| ? | ? (schéma PID, šedá s červenými svislými pruhy) | 3 | ARRIVA CITY 3 | schéma PID, šedá s červenými svislými pruhy 3 | 1466, 1468, 1469 | praha-zapad |
| SOR CN 8,5 | SOR CN 8,5 (červená) | 1 | ARRIVA CITY 1 | červená 1 | 9034 | benesovsko |
| SKD Iveco Stratos LE 37 | VZ-PID-Stratos_LE_37-<světle zelená> (SKD Iveco Stratos LE 37) | 1 | ČSAD Liberec 1 | světle zelená 1 | 10759 | mladoboleslavsko |
| Irisbus Crossway LE 10,8M | VZ-PID-Irisbus_Crossway_LE_10_8M-<bílá> (Irisbus Crossway LE 10,8M) | 1 | ČSAD Liberec 1 | bílá 1 | 10642 | mladoboleslavsko |
| Iveco Crossway LE CITY 12M | VZ-PID-Crossway_LE_City_12M-<městské schéma, červeno-bílá & modrá střecha> (Iveco Crossway LE CITY 12M) | 1 | Dopravní podnik hl. m. Prahy 1 | městské schéma, červeno-bílá & modrá střecha 1 | 4510 | praha-vychod |
| Setra S 415 LE business | VZ-PID-Setra_S_415_LE_business-<Doprava Ústeckého kraje, zelená> (Setra S 415 LE business) | 1 | UMBRELLA CITY LINES 1 | Doprava Ústeckého kraje, zelená 1 | 12425 | rakovnicko |
