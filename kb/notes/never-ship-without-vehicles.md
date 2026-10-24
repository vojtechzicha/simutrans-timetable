---
name: never-ship-without-vehicles
description: "A fleet/vypravenost sheet must always show vehicles assigned to lines; never publish \"vehicles pending\" — use provisional sightings + history-designed cars with real numbers"
metadata:
  node_type: memory
  type: feedback
  originSessionId: b0e0d2a3-0b49-4682-957a-d187cf469167
  modified: 2026-09-29T17:18:11.223Z
---

A fleet or vypravenost sheet must never be published without vehicles on its lines. On 29 Sep 2026 the Ostrava bus sheet went out as "vehicles pending", waiting for the next day's live peak. The user said "you are missing the vehicle assignment to lines" and pointed to the Prague bus session.

**Why:** the vehicle-to-line assignment is the point of these sheets. A sheet with only needs is incomplete, even if better data comes tomorrow.

**How to apply:** always fill every line, in this order:
1. Observed data, the best available (even post-peak sightings, marked provisional).
2. Other days' records.
3. Designed vehicles with **real car numbers**: history on the line, home depot, main type, not used elsewhere that day. Mark them "designed, not recorded", with the reason.

Replace this with better observations later. For sizing, use max(round-trip need, buses on the road in 16:00–16:59, with the cycle layover). Related: [[prague-bus-lines-check]], [[ostrava-bus-vypravenost]], [[prague-tram-peak-fleet]].
