---
name: shared-circuit-vagonweb-rule
description: "Rail: cut main-line station stays with shared circuit lines (terminal stop type), but only where vagonweb shows the same vehicles run both parts"
metadata:
  type: feedback
---

Keep stays at big main-line stations (Kolín, Pečky, Kutná Hora hl. n.) short. When a long and a short line turn at the same main-line station, one circuit line can cut the stay. The fork has a terminal stop type for the shared station.

Share a Simutrans line only if the same vehicles really run both parts. Check vagonweb.cz řazení: the planned type, plus the units sighted on the same day moving between the trains. The user said: "mainly use vagonweb for razeni - we should not share the simutrans line if different vehicles are used on the different long/short part".

**Why:** the user wants realistic vehicle workings and less platform blocking at main stations. 014 went from 91 to 31 min at Kolín, with 3 vehicles instead of 4.

**How to apply:**
- Use `pipeline/local-rail/vagonweb.py <relace> <train numbers>`.
- vagonweb needs `zeme=%C4%8CD`; with `CD` the page has no composition. It also needs a session cookie and a referer. I first wrongly concluded the data wasn't there, and the user had to point it out.
- Don't move real times to shorten stays; say when the real minutes fix them.
- Exception (8–9 Oct 2026, 210 at Praha hl. n.): the user chose circuits of two branches with the same type (847), even though sightings keep units on one branch. They chose this over a realistic variant with empty runs to sidings (Praha-Libeň, from the raw CIS locations). Offer both; the user may prefer the simpler line.
- Full rule in `pipeline/rail-design-rules.md`. Related: [[find-every-train-feedback]], [[local-rail-012-014-235]].
