# Boole search on large storage

Updated: 2026-11-09T10:24:16.483380+00:00

State: **running**. Run **boole-bulk-20261108**; gpu with 16 preparation workers.
Current cursor: **3,297,648,128**.
New committed patches: **24,389,888** in 95,273 chunks.
Combined verified selected patches, including parents: **297,648,128**.
Fresh interval: `[3273258240, 3750000000]`; committed: `[3273258240, 3297648128]`.

Journal storage: **separate large disk on Ada**. New journal cap: **128 GiB**;
free-space reserve: 8 GiB.
Observed rate: **675 patches/s**; new independent GMP audits: 745.
Deadline: **2026-11-09T09:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under the unchanged original reservation.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
