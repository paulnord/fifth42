# Ada search on large storage

Updated: 2026-11-09T05:32:09.055011+00:00

State: **running**. Run **ada-bulk-20261108**; gpu with 16 preparation workers.
Current cursor: **4,350,627,712**.
New committed patches: **22,479,616** in 87,811 chunks.
Combined verified selected patches, including parents: **600,627,712**.
Fresh interval: `[4328148096, 11250000001]`; committed: `[4328148096, 4350627712]`.

Journal storage: **separate large disk on Ada**. New journal cap: **128 GiB**;
free-space reserve: 8 GiB.
Observed rate: **1,050 patches/s**; new independent GMP audits: 686.
Deadline: **2026-11-09T09:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under the unchanged original reservation.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
