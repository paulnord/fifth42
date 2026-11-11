# Boole combined search

Updated: 2026-11-11T16:12:43.645169+00:00

State: **running**. Run **boole-preparation-20261110-18-r1**; gpu with 16 preparation workers.
Verified replicated cursor: **8,168,951,552**.
New replicated logical patches: **16,951,552** in 66,217 chunks.
Combined verified selected patches, including parents: **16,951,552**.
Fresh interval: `[8152000000, 8216000000]`; replicated: `[8152000000, 8168951552]`.
Local cursor: 8,169,135,872; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.15842551196692511, 'elapsed_seconds': 1804.3189915010007, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7681453, 'mean_ready_depth': 0.9991299797039565, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 4175, 'prepare_wall_seconds': 1804.1047201236943, 'producer_wait_capacity_seconds': 0.005435911763925105, 'producer_wait_full_seconds': 1064.0092541124905, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 1.5697917031939141, '1': 1802.749197357858}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 8362, 'flush_seconds': 61.6011514190468, 'pending_bytes': 115281, 'pending_chunks': 6}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **9,473 patches/s**; new independent GMP audits: 522.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
