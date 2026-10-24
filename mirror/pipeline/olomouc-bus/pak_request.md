# Olomouc buses (DPMO): pak objects for the peak sheet

State 2026-09-29, vehicles of 2026-09-29. Operator of every bus: DPMO (Dopravní podnik města Olomouce); no subcontractor runs a city line.
Package VZ-DPOlomouc-bus. Status is read from the local pak checkout (assets/pak_objects.json). Advert wraps (CVR) use the type's normal livery.

| Type | Livery | Length | Objects | Status | Buses counted in the peak | Not needed (shown dimmed) |
|---|---|---|---|---|---|---|
| SOR NS 12 electric | DPMO white-blue-red | 12 m (8 car units) | `VZ-DPOlomouc-SOR_NS_12_electric-dpmobilomodrocervena-SOR_NS_12_electric` | installed | 501 | - |
| Solaris Alpino 8.6 | DPMO white-blue-red | 8.6 m (6 car units) | `VZ-DPOlomouc-Alpino_8_6-dpmobilomodrocervena-Alpino_8_6` | installed | 552 | 551 |
| Solaris Urbino 12 II | white | 12 m (8 car units) | `VZ-DPOlomouc-Urbino_12-bila-Urbino_12` | **requested** | - | 615 |
| Solaris Urbino 12 II | lime green | 12 m (8 car units) | `VZ-DPOlomouc-Urbino_12-zelena-Urbino_12` | installed | 616, 617, 618 | - |
| Solaris Urbino 12 III | DPMO white-blue-red | 12 m (8 car units) | `VZ-DPOlomouc-Urbino_12-dpmobilomodrocervena-Urbino_12` | installed | 619, 622, 629, 631, 634, 635, 637, 638, 640, 642, 643, 644 | 620, 621, 623, 626, 627, 628, 630, 632, 633, 636, 639, 641 |
| Solaris Urbino 12 IV | DPMO white-blue-red | 12 m (8 car units) | `VZ-DPOlomouc-Urbino_12_IV-dpmobilomodrocervena-Urbino_12_IV` | installed | 645, 646, 648, 649, 650, 651, 658, 659, 660, 661, 662, 664, 665, 666 | 647, 652, 653, 654, 655, 656, 657, 663 |
| Solaris Urbino 18 III | DPMO white-blue-red | 18 m (16 car units) | `VZ-DPOlomouc-Urbino_18-dpmobilomodrocervena-Urbino_18-A` + `VZ-DPOlomouc-Urbino_18-dpmobilomodrocervena-Urbino_18-B` | installed | 406, 407, 409, 412, 414, 415 | 408, 410, 411, 413 |
| Solaris Urbino 18 IV | DPMO white-blue-red | 18 m (16 car units) | `VZ-DPOlomouc-Urbino_18_IV-dpmobilomodrocervena-Urbino_18_IV-A` + `VZ-DPOlomouc-Urbino_18_IV-dpmobilomodrocervena-Urbino_18_IV-B` | installed | 417, 418, 420, 421, 422, 424, 425, 426, 427, 428 | 416, 419, 423 |

## Requests

- None: every bus counted in the peak has an installed object.

Optional (only on buses marked not needed now; needed if they are counted after a data refresh):
- Solaris Urbino 12 II, white (615; paint bílá): `VZ-DPOlomouc-Urbino_12-bila-Urbino_12`
