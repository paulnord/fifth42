# Cabbage search on large storage

Updated: 2026-11-09T03:29:33.142341+00:00

State: **running**. Run **cabbage-bulk-20261108T234202Z**; gpu with 16 preparation workers.
Current cursor: **2,272,559,488**.
New committed patches: **9,076,480** in 35,455 chunks.
Combined verified selected patches, including parents: **22,559,488**.
Fresh interval: `[2263483008, 3000000000]`; committed: `[2263483008, 2272559488]`.

Journal storage: **separate large disk on Ada**. New journal cap: **128 GiB**;
free-space reserve: 8 GiB.
Observed rate: **685 patches/s**; new independent GMP audits: 277.
Deadline: **2026-11-09T09:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under the unchanged original reservation.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
