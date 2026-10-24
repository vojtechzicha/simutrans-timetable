# Knowledge base: Simutrans timetables

The owner is rebuilding real Czech public transport — city trams, trolleybuses and buses, ODIS regional buses, and rail — in their
own fork of **Simutrans 122.0** with a custom Czech **pak128** (VZ objects), in one large save game. Each "sheet" is an HTML page
that turns the real timetable and real vehicle allocation into exactly what they type into the game: one row per Simutrans line and
terminus entry with *Departure every / Offset / Also at*, and (for city sheets) the actual vehicles by fleet number with their pak
object. 44 sheets were built between 12 Sep and 22 Oct 2026 across ~20 parallel Claude Code sessions; this KB consolidates all of
their rules, memories and lessons.

## Read in this order
1. [workflow.md](workflow.md) — where things live, how to refresh/create/publish, the publish checklist, the web app.
2. [rules/fork-schedule.md](rules/fork-schedule.md) — the game's timetable fields and how real departures map to them (every sheet).
3. The rules for the kind of sheet you're touching:
   - [rules/city-fleet-sheets.md](rules/city-fleet-sheets.md) — trams, trolleybuses, city buses (per-vehicle peak fleet sheets)
   - [rules/bus-sheets.md](rules/bus-sheets.md) — big-city vs regional/small-town bus rules, coverage, hand review
   - [rules/rail-sheets.md](rules/rail-sheets.md) — rail method, game track ends, engineering works, CIS JŘ conventions
   - [rules/pak-objects.md](rules/pak-objects.md) — VZ object naming, stand-ins, fleet desk
4. [sources.md](sources.md) — every data feed with its quirks (WAF headers, live APIs without history…).
5. [lessons.md](lessons.md) — the owner's corrections in order, with quotes. Skim before presenting anything.
6. [related-projects.md](related-projects.md) — engine fork, pak repo, save game, rename service, other sessions.
7. [notes/](notes/) — the 62 original per-topic memory notes, verbatim (per-sheet history, decisions, open points).
   `notes/_original-MEMORY-index.md` is their old one-line index.

Full method documents (verbatim, synced from the working folder):
- `mirror/pipeline/README.md` — shared city rules, folder layout, the per-city decisions table
- `mirror/pipeline/rail-design-rules.md` — the rail method
- `mirror/pipeline/bus-schedule-method.md` — the regional/small-town bus method with its pre-publish checks
- `mirror/pipeline/<x>/README.md` — each pipeline's sources, steps, every manual decision, and "How to update"

## The sheet families
| Family | Sheets | Built by |
|---|---|---|
| City tram peak fleet | Praha, Brno (closure + from 29 Sep), Plzeň, Olomouc, Ostrava, Most–Litvínov | `pipeline/<city>` |
| City trolleybus / bus | Praha (trolleybus + bus lines check), Brno, Plzeň, Ostrava, Olomouc bus, Most bus, Pardubice (both modes) | `pipeline/<city>-<mode>` |
| Small towns | Havířov / Karviná / Orlová (Transdev MHD) | `pipeline/havirov-karvina-orlova` |
| ODIS regional | Havířovsko-Karvinsko-Orlovsko, Těšínsko-Třinecko-Frýdecko, Opavsko (+ Opava trolleybuses), Novojičínsko, Bruntálsko | `pipeline/odis-regional-*` (shared scripts in `-hko`) |
| Rail (active) | S9/S2/R17/R49/Ex7, S75, S5→S4, S4→S3, Ex7+R17 Veselí | `pipeline/local-rail/build_*.py` |
| Rail (archived) | MD-CR long distance, RegioJet, Leo Express, local trains 010/062/064/260, 012/014/210/212/235, R49 Benešov, R18, S49, west of Praha | md-cr / local-rail / hand-written |
| Termini (reference, 12 Sep) | Praha, Brno, Ostrava, Olomouc, Most–Litvínov tram termini | engine session, no pipeline (inputs to the tram pipelines) |

## Glossary
- **vypravenost** — which vehicle ran which duty (kurz) on a day; **kurz / course / pořadí** — a vehicle duty number on a line.
- **smyčka** — turning loop (−1 min rule); **úvrať** — stub/turn-back terminus (real minute).
- **výluka** — engineering works / closure; **NAD** — rail/tram replacement bus; **odstavné nádraží** — stabling yard.
- **L / S hours** — odd (lichá) / even (sudá) hours in "every 2 h at L:07".
- **KJŘ** — rail timetable table number (062, 014…); **JDF** — Czech bus/city timetable exchange format (CIS JŘ); **CIS JŘ** — national
  timetable information system; **ODIS** — Moravian-Silesian integrated transport; **PID** — Prague integrated transport;
  **IDS JMK** — South Moravian integrated transport.
- **Designed** vehicle — not recorded that day, picked by rule from the line's history with a real car number.
- **Stand-in (≈)** — nearest pak object used until the exact one exists.
- **Fleet desk** — the pak session that answers which vehicle objects exist and takes requests.
