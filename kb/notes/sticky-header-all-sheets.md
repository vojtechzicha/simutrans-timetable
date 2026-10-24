---
name: sticky-header-all-sheets
description: "Every fleet/vypravenost sheet must have the Prague-tram-style sticky bar (lines, depots, sections, vehicle search); anchors must clear it on phones"
metadata:
  node_type: memory
  type: feedback
  originSessionId: e03a85dc-f430-434a-99fb-e6daceff5db2
  modified: 2026-09-29T15:03:36.176Z
---

The user likes the Prague tram sheet's sticky header and wants it on every fleet sheet (29 Sep 2026: "some newer artifacts don't … you're responsible for all of the files"). The bar holds line badges, depot links with counts plus section links, and a vehicle search that highlights `[data-v]`.

**Why:** The Brno, Plzeň and Brno-trolleybus sheets had only a non-sticky table of contents. The Ostrava and Most sheets had only a sticky line row.

**How to apply:**
- Build every new city sheet with the bar. The shared rule is in `pipeline/README.md` under "Page header". The drop-in implementation is `pipeline/brno/scripts/sticky.py`.
- Check it in a real browser with Playwright (`channel='msedge'`) at 1400 px and 390 px widths. Headless Edge `--screenshot` renders blank for scrolled or hash URLs.
- A fixed scroll-margin hid headings under the bar on phones, so it must be dynamic (`--stick` = bar height + 8).

Related: [[vehicle-type-always-visible]], [[city-pipelines]]
