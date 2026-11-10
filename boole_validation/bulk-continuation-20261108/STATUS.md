# Boole combined search

Updated: 2026-11-10T06:15:58.465288+00:00

State: **running**. Run **boole-extra-20261109-a**; gpu with 16 preparation workers.
Verified replicated cursor: **262,319,104**.
New replicated logical patches: **162,319,104** in 634,059 chunks.
Combined verified selected patches, including parents: **162,319,104**.
Fresh interval: `[100000000, 300000000]`; replicated: `[100000000, 262319104]`.
Local cursor: 263,384,576; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 2073.9679811545648, 'elapsed_seconds': 9022.497246210987, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 547184, 'mean_ready_depth': 0.5478109174998536, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 637651, 'prepare_wall_seconds': 9020.307355157624, 'producer_wait_capacity_seconds': 0.3886565800639801, 'producer_wait_full_seconds': 1124.8718700918253, 'ready': 0, 'ready_depth_seconds': {'0': 6847.702374808083, '1': 711.8811213042354, '2': 157.99987518345006, '3': 1304.9138743052026}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 79837, 'flush_seconds': 438.4206020218553, 'pending_bytes': 103442, 'pending_chunks': 6}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **18,090 patches/s**; new independent GMP audits: 4,982.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
