# Pak requests from the PID regional sheets

From pipeline/pid-regional/scripts/04_vehicles.py (2026-11-02 live map). Buses on the twelve oblast sheets whose type and livery have no object in VZ-PID-bus (regional) or VZ-MHD<Town>-bus (town lines). They are shown as "requested" on the sheets, never as a stand-in (rules/pak-objects.md). "?" = the vehicle window of the live map names no type for the bus (and the bus is not in the register); the second poll day may name it.

| Real type | Wanted object | Buses | Operators | Paint (register) | Example numbers | Sheets |
|---|---|---|---|---|---|---|
| ? | ? (paint unknown) | 11 | ARRIVA CITY 3, ČSAD Benešov 2, Okresní autobusová doprava Kolín 2,  2, ARRIVA STŘEDNÍ ČECHY 1, ČSAD AUTOBUSY České Budějovice 1 | paint not in the register 11 | 1000, 1013, 1466, 1468, 1469, 17265, 4146, 7965 | benesovsko, kolinsko, nymbursko, praha-vychod, praha-zapad, pribramsko |
