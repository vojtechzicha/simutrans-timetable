---
name: ex7-r17-veseli
description: "Ex7 + R17 sheet (14 Oct 2026): Praha – Tábor cut at Veselí nad Lužnicí (game track end), no depot runs, 4 + 4 vehicles; build_ex7_r17.py"
metadata:
  node_type: memory
  type: project
  originSessionId: e9b5fede-a5b9-4e20-aab2-33579bfb8991
  modified: 2026-10-14T14:47:56.010Z
---

User, 14 Oct 2026: "Research Ex7 and R17 - but for both the track ends in Veselí nad Lužnicí; neither has access to depot unless you have concrete evidence of one in Prague."

- **Game track ends at Veselí nad Lužnicí** on the Praha – Tábor – České Budějovice line (treat as a hard end for any later line there).
- **Depot rule:** model a Praha depot run only with concrete evidence (CIS empty runs); Ex7/R17 have none.
- Sheet `pipeline/local-rail/build_ex7_r17.py` → `Ex7 R17 Praha Veselí.html`; artifact https://claude.ai/artifact/Efb4CMZVvtNDZj7rsB5Wr5. R17 :46/:38 (4 veh), Ex7 :21/:23 (4 veh).
- Ex7 doesn't stop at Veselí in reality; the script adds the passing minute as the terminus.

Related: [[s5-to-s4-corridor]], [[rail-design-rules]], [[r49-benesov-local]].
