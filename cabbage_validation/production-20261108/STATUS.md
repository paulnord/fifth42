# Cabbage combined search

Updated: 2026-11-10T21:44:42.126001+00:00

State: **running**. Run **cabbage-extended-upgrade-20261110**; gpu with 16 preparation workers.
Verified replicated cursor: **1,826,550,528**.
New replicated logical patches: **287,701,504** in 1,123,834 chunks.
Combined verified selected patches, including parents: **1,326,550,528**.
Fresh interval: `[1538849024, 2250000000]`; replicated: `[1538849024, 1826550528]`.
Local cursor: 1,828,362,752; physical tasks group up to 8 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 2; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 1135.3567644064897, 'elapsed_seconds': 6779.970491723972, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 3838862, 'mean_ready_depth': 0.16798963635602257, 'outstanding': 2, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 70620, 'prepare_wall_seconds': 6779.650043041736, 'producer_wait_capacity_seconds': 0.05132054688874632, 'producer_wait_full_seconds': 188.14460763998795, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 0, 'ready_depth_seconds': {'0': 5641.005712751707, '1': 1138.9647774092737}, 'ready_limit': 1, 'reserved_bytes': 25165824}; buffer: {'flush_count': 141387, 'flush_seconds': 826.2048090715543, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **42,628 patches/s**; new independent GMP audits: 8,828.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
