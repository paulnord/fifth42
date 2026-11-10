# Cabbage combined search

Updated: 2026-11-10T11:05:43.881999+00:00

State: **running**. Run **cabbage-extended-rotation-20261110T110534Z**; gpu with 16 preparation workers.
Verified replicated cursor: **1,005,837,824**.
New replicated logical patches: **2,048** in 8 chunks.
Combined verified selected patches, including parents: **505,837,824**.
Fresh interval: `[1005835776, 2250000000]`; replicated: `[1005835776, 1005837824]`.
Local cursor: 1,005,864,448; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: None; buffer: {'flush_count': 0, 'flush_seconds': 0.0, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **0 patches/s**; new independent GMP audits: 0.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
