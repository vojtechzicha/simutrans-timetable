---
name: odis-regional-novojicinsko
description: ODIS Novojičínsko Východ/Západ + Bílovecko + MHD Nový Jičín/Studénka sheet (21 Oct 2026) — pipeline/odis-regional-novojicinsko via HKO scripts --base; 108 buses; 601–604 observed circuit
metadata:
  node_type: memory
  type: project
  originSessionId: 1098259d-3349-4d59-bd20-53ed11629b4d
  modified: 2026-10-21T18:58:38.636Z
---

"ODIS Novojicinsko Bilovecko.html" (artifact https://claude.ai/artifact/YFgUu62jD8YqfpuoL8FZpp, v1 21 Oct 2026), one of the three sheets after the owner said "Yes, do those next sheets".

- Areas: 883 Novojičínsko Východ (Z-Group bus Kopřivnice, 63-), 882 Novojičínsko Západ (Transdev Morava NJ, 62-), 884 Bílovecko (Transdev Morava Ostrava, 64-), 886 MHD Nový Jičín (ARRIVA), 887 Studénka (Transdev Morava).
- Config written by `authoring/nj_spec.py` (+ nj_notes.py) and `nj_config.py`; review tools groups.py/dump.py/review.py/divcmp.py there.
- 63 lines → 70 Simutrans lines, 108 buses (107 seen, 1 designed); 18 listed unmodelled.
- NJ town lines = one observed circuit 601–604 (3 ARRIVA buses rotate 602→601→604→603), lay 1 at the bus station.
- 655 modelled here (883655 = 41 of 45 trips) although TFJ also models 863655 — duplicate flagged to the parent.
- Short diversions 629/643/929 → regular; to-12-Dec diversions modelled as run.
- Pak confirmed by the fleet desk. Z-Group Crossway LE Line 12M (6Z9 6492, Kroměříž bus, green-blue, no kraj ring) was drawn and installed 21 Oct as VZ-ODIS-Crossway_LE_Line_12M-bilazelenomodra-Crossway_LE_Line_12M (in nj_config.py, sheet v3). ARRIVA SOR BN 10,5 no. 7577 (2TT 8558): the owner un-parked it, installed 22 Oct as VZ-MHDNovyJicin-SOR_BN_10_5-cervenocerna-SOR_BN_10_5 (main 0fda6a6; layout unverified, no photo after the repaint). Sheet v5 has 0 stand-ins; looked-up SOR lengths without "M" (BN 10,5, EBN/CN 9,5) fixed via shared lib.tlen.

Related: [[odis-regional-tfj]], [[odis-regional-hko]], [[pak-fleet-desk]], [[hand-review-schedules-rule]], [[every-stop-covered-rule]].
