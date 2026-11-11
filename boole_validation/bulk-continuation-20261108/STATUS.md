# Boole combined search

Updated: 2026-11-11T05:26:21.466777+00:00

State: **running**. Run **boole-preparation-20261110-12-r1**; gpu with 16 preparation workers.
Verified replicated cursor: **7,786,665,728**.
New replicated logical patches: **18,665,728** in 72,913 chunks.
Combined verified selected patches, including parents: **18,665,728**.
Fresh interval: `[7768000000, 7832000000]`; replicated: `[7768000000, 7786665728]`.
Local cursor: 7,786,819,328; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.1566895010182634, 'elapsed_seconds': 1803.178316613019, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7680798, 'mean_ready_depth': 0.9989624722589852, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 4584, 'prepare_wall_seconds': 1802.9821754297009, 'producer_wait_capacity_seconds': 0.0059231569757685065, 'producer_wait_full_seconds': 979.6370598542853, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 1.8708459354820661, '1': 1801.3074690875364}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 9174, 'flush_seconds': 62.39041536167497, 'pending_bytes': 57083, 'pending_chunks': 3}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **10,408 patches/s**; new independent GMP audits: 573.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
