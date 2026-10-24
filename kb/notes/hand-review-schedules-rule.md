---
name: hand-review-schedules-rule
description: "Scripted schedule fits are a draft; check every line by hand against its real departures and bus chains before publishing, hand-set where the fit is an artefact"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 4860251d-9567-4507-9501-0ec6574bc42e
  modified: 2026-10-20T05:27:31.431Z
---

On 20 Oct 2026, on the Havířov/Karviná/Orlová sheet, the owner asked: "Is the lines the best schedule that fits my intent (not necessarily the scripts)? Or can you do a version that fits better". A hand review found artefacts of the shared fit:
- merged variant minutes made the exactly hourly 417 approximate;
- the sparse-band fallback gave every 120 to the hourly 409 and 411;
- a minimax slot rule set 504 at :01 instead of its real :06;
- daily timetables were exact for sporadic lines (418, 420, 513).

**Why:** the owner cares about the schedule that reproduces the real operation, not about what the algorithm outputs.

**How to apply:**
- Before publishing, dump each line's real departures at its peak per direction, plus how its buses chain their trips, next to the suggested rows, and judge every approximate row.
- Hand-set (`line_overrides`) wherever the main pair alone fits exactly, or where one bus runs a fixed sequence. Use a daily circuit only if each leg sends the same number of buses.
- Hand-set legs follow the regular run, and odd trips are listed as off the pattern on the To check list with any slower option.

Reference: `pipeline/havirov-karvina-orlova/README.md`, section "Hand review". Related: [[every-stop-covered-rule]], [[schedule-both-ends-same-rate]], [[model-line-at-its-peak]].
