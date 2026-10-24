---
name: core-points-repeating-interval-rule
description: Owner's Ex4 method for irregular lines — read trips at core points over the whole day, find the repeating interval, split destination variants onto longer offset intervals
metadata:
  type: feedback
---

On 20 Oct 2026, on the Havířov/Karviná/Orlová sheet, the owner said: "Look at how I did in the save game Ex4 - there is also a very irregular service, but I defined it in core points, created a repeating interval and it suddenly made sense." In the save, Ex4/1 runs every 240, and Ex4/2 and Ex4/3 every 480, one line per destination. Each is timetabled only at core points (the termini, Bohumín, Břeclav).

**Scope:** regional lines and small-town networks (Havířov, Karviná, Orlová); not Ostrava, Prague, Olomouc (see [[regional-vs-local-rules]]).

**Why:** a fit made only on the afternoon band, by terminus pair, makes irregular lines look random. Read at core points over the whole day, they usually repeat. The Orlová 501/504 turned out to be one hourly bus: Lazy :06, Dětmarovice, železniční stanice :18.

**How to apply:**
- Take each trip's time at the core points it passes, not its start or end.
- Read the whole operating day.
- Choose the repeating interval.
- Give each destination variant its own Simutrans line on a longer interval (240/480), offset so the lines don't coincide. The owner also accepts merging a sparse line into another as one of its legs, for example 503 as 504's path variant.
- Time only the core points, and name the trips that don't fit.

- **Buses differ from trains (owner, 20 Oct):** time the terminal and work back from the knot. Terminal departure = knot time − running time; the knot gets no timetable. 501B leaves Koukolná :09 to pass the station :18; 406 leaves Pašůvka :26 / :56.

- **No daily lines (owner, 20 Oct):** "8 hrs should be the very maximal interval (still not preferred) … we can bend the reality a bit." Never use 1440 or 720. Bend sparse trips onto a repeating slot of at most 480: the interval they already have (shift lines every 480; 420's trips 160 apart), a circuit on the shortest period that holds a one-bus sequence (418 every 240), or fold them into the line they belong to (513 on 514).

The full step-by-step method for any model is `pipeline/bus-schedule-method.md`. Reference: `pipeline/havirov-karvina-orlova/README.md`, section "Core points". Related: [[hand-review-schedules-rule]], [[every-stop-covered-rule]], [[simutrans-fork-schedule-spec]].
