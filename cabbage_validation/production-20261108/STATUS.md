# Cabbage search on large storage

Updated: 2026-11-09T13:16:24.055078+00:00

State: **running**. Run **cabbage-bulk-20261108T234202Z**; gpu with 16 preparation workers.
Current cursor: **2,296,480,640**.
New committed patches: **32,997,632** in 128,897 chunks.
Combined verified selected patches, including parents: **46,480,640**.
Fresh interval: `[2263483008, 3000000000]`; committed: `[2263483008, 2296480640]`.

Journal storage: **separate large disk on Ada**. New journal cap: **128 GiB**;
free-space reserve: 8 GiB.
Observed rate: **681 patches/s**; new independent GMP audits: 1,007.
Deadline: **2026-11-09T09:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under the unchanged original reservation.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
