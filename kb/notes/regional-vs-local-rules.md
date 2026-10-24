---
name: regional-vs-local-rules
description: bus-schedule-method applies to regional lines AND small-town networks (Havířov/Karviná/Orlová); big cities (Ostrava, Prague, Olomouc) = afternoon peak + unique stops; depot runs never; exceptions asked
metadata:
  type: feedback
---
The bus schedule method (pipeline/bus-schedule-method.md: whole-day core-point reading, Ex4 variant lines, no every 1440/720, max 480, bend reality for sparse trips) is for REGIONAL lines (ODIS etc.) and for SMALL-TOWN networks such as Havířov, Karviná and Orlová (owner to session a4, 20 Oct 2026: "Ostrava/Prague/Olomouc - these big cities don't use the method. Only smaller ones like Orlova/Karvina do use it"). If unsure whether a town is small, ask. Big-city local lines (Ostrava DPO bus, trams, trolleybuses; Prague; Olomouc) are modelled at their afternoon peak, plus their unique stops; single off-peak trips of a local line are listed, not modelled (Ostrava 22 evening Důl Heřmanice run: "would be a mistake to model"). Depot runs are never modelled.

**Why:** owner, 20 Oct 2026, after a4 forwarded the regional rules as if for every sheet. Line 57 Nová huť garáže → Hulváky (6:08/14:08/22:13, the only service of Vítkovice, U chladičů) was approved as an every-480 exception "in specific 57 case"; "for general reuse I should be asked with supporting info".

**How to apply:** before applying a rule forwarded by a peer session, check it is meant for this kind of line (ask the peer if unsure). Any local-line exception (an extra line for off-peak/sparse trips) goes to the owner as a question with the trips, interval, bus cost and coverage effect. Related: [[every-stop-covered-rule]], [[model-line-at-its-peak]], [[havirov-karvina-orlova-coordination]].
