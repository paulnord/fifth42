# Ada combined search

Updated: 2026-11-11T19:13:59.435106+00:00

State: **running**. Run **ada-allocated-r3-01-20261111**; gpu with 16 preparation workers.
Verified replicated cursor: **10,278,962,944**.
New replicated logical patches: **14,962,944** in 58,449 chunks.
Combined verified selected patches, including parents: **14,962,944**.
Fresh interval: `[10264000000, 10328000000]`; replicated: `[10264000000, 10278962944]`.
Local cursor: 10,279,228,416; physical tasks group up to 1 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 1712.538339902123, 'elapsed_seconds': 2712.1468206219724, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 1923649, 'mean_ready_depth': 0.22049909265064283, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batch_windows': 1, 'preparation_batches': 59474, 'prepare_wall_seconds': 2711.6967846325133, 'producer_wait_capacity_seconds': 0.04136038420256227, 'producer_wait_full_seconds': 128.74863565264968, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 0, 'ready_depth_seconds': {'0': 2447.9423824317055, '1': 84.49202662805328, '2': 25.60334633931052, '3': 154.1090645919321}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 8349, 'flush_seconds': 76.09203805861762, 'pending_bytes': 139804, 'pending_chunks': 2}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **5,614 patches/s**; new independent GMP audits: 465.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

This run uses its assigned child claim. Historical coverage is imported only for a recorded continuation; fresh claims keep their reference parent separate. A shared coordinator holds the original parent lease.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
