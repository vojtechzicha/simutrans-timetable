# Pak request: VZ-DPMostLitvinov-bus (from the Most–Litvínov bus sheet, 29 Sep 2026)

For the pak128 session (simutrans-custom-czech-pak128-bd). Sheet: `Most-Litvinov Bus Vypravenost.html`, pipeline
`pipeline/most-litvinov-bus` (mapping in `assets/pak_map.json`). Checked against the pak source tree
`C:\Users\vojte\Developer\simutrans-custom-czech-pak128\build\VZ-DPMostLitvinov-bus\` at main b84c15c.

Operator of every bus below: Dopravní podnik měst Mostu a Litvínova, a.s. (DPmML). No subcontractor runs a city line.

## Already in the pak (used as they are)

| Real type | Object | Livery | Cars on the sheet at 16:00 |
|---|---|---|---|
| SOR NB 12 (12 m) | `VZ-DPMostLitvinov-NB_12-mostzlutocervena-NB_12` | white-yellow-red | 30 |
| SOR NS 12 (12 m) | `VZ-DPMostLitvinov-SOR_NS_12-mostzlutocervena-SOR_NS_12` | white-yellow-red | 12 |
| SOR NB 18 (18 m) | `VZ-DPMostLitvinov-SOR_NB_18-mostzlutocervena-SOR_NB_18-A` + `-B` | white-yellow-red | 1 (194) |
| SOR NS 18 (18 m) | `VZ-DPMostLitvinov-SOR_NS_18-mostzlutocervena-SOR_NS_18-A` + `-B` | white-yellow-red | 1 (97) |
| Irisbus Citelis 18M (18 m) | `VZ-DPMostLitvinov-Citelis_18M-mostzlutocervena-Citelis_18M-A` + `-B` | white-yellow-red | 1 (98) |
| Iveco Urbanway 18M (18 m) | `VZ-DPMostLitvinov-Urbanway_18M-mostzlutocervena-Urbanway_18M-A` + `-B` | white-yellow-red | 1 (99) |

Advertising wraps (45 "Home Care Barborka", 46 "Mostečtí lvi") map to the normal white-yellow-red object.

## Requested (the sheet shows these names, marked "requested"; all three types are on the sheet at 16:00)

1. **SOR NB 12, Prague city scheme red-white** — `VZ-DPMostLitvinov-NB_12-prahacervenobila-NB_12`
   - Car **83** (ex-DPP 3574, 2009, in DPmML service since 10/2024, Most garage). Register paint: "městské schéma,
     červeno-bílá" (the DPP red-white scheme); it wore DPmML white-yellow-red 8/2024–2026 and is red-white again now.
   - Length 12 m, 8 car units like `NB_12`. **On the sheet** (line 30).
2. **SOR NB 18, Prague city scheme red-white** — `VZ-DPMostLitvinov-SOR_NB_18-prahacervenobila-SOR_NB_18-A` + `-B`
   - Car **189** (ex-DPP 6668, 2011, in service since 12 Sep 2026, Litvínov garage), still in DPP red-white.
   - Length 18 m, 8 + 8 like the existing NB 18. **On the sheet** (the tram replacement buses, Chempark – Citadela),
     placed there by the user's rule of 29 Sep: every fleet type and livery on a line.
3. **MAN ND 313 Lion's City DD, BVG yellow** — proposed `VZ-DPMostLitvinov-Lions_City_DD-bvgzluta-Lions_City_DD`
   - Cars **153** and **154** (ex-BVG Berlin 3293 and its sister, 2007/2008, in DPmML service since 8/2023, Most
     garage). Three-axle double-decker, 13.7 m. 154 wore the "Olympijský festival 2024" wrap 11/2023–8/2024.
   - DPmML runs them only at weekends on the summer line 16 to Jezero Most. By the user's coverage rule of 29 Sep,
     **153 is on the sheet on line 16** (marked "normally weekends only"); 154 is not used.

## Not needed

- `Citelis_12M` (the only Citelis 12M, 120, is a driving-school bus) and the `E_Way_12M` demonstrator are not used.
- The two Crossway 12M (1, 3) and the coaches are contract fleet, not city buses.
