# Ada search on large storage

Updated: 2026-11-09T15:00:05.658560+00:00

State: **stopped**. Run **ada-bulk-20261108**; gpu with 16 preparation workers.
Current cursor: **4,385,553,536**.
New committed patches: **57,405,440** in 224,240 chunks.
Combined verified selected patches, including parents: **635,553,536**.
Fresh interval: `[4328148096, 11250000001]`; committed: `[4328148096, 4385553536]`.

Journal storage: **separate large disk on Ada**. New journal cap: **128 GiB**;
free-space reserve: 8 GiB.
Observed rate: **1,035 patches/s**; new independent GMP audits: 1,752.
Deadline: **2026-11-09T09:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under the unchanged original reservation.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
