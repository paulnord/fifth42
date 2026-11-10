# Boole combined search

Updated: 2026-11-10T18:44:27.165237+00:00

State: **running**. Run **boole-delegated-20261109-06**; gpu with 16 preparation workers.
Verified replicated cursor: **7,384,002,048**.
New replicated logical patches: **2,048** in 8 chunks.
Combined verified selected patches, including parents: **2,048**.
Fresh interval: `[7384000000, 7448000000]`; replicated: `[7384000000, 7384002048]`.
Local cursor: 7,384,229,376; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 0.16979251289740205, 'elapsed_seconds': 9.746577943034936, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 481361, 'mean_ready_depth': 2.101916074030633, 'outstanding': 2, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 438, 'prepare_wall_seconds': 9.738212385971565, 'producer_wait_capacity_seconds': 0.0002803340321406722, 'producer_wait_full_seconds': 4.57618270086823, 'ready': 1, 'ready_depth_seconds': {'0': 1.6289154425030574, '1': 1.4811606628936715, '2': 0.9041717504733242, '3': 5.732328227139078}, 'ready_limit': 3, 'reserved_bytes': 16777216}; buffer: {'flush_count': 54, 'flush_seconds': 0.3143308159778826, 'pending_bytes': 92055, 'pending_chunks': 5}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **11,036 patches/s**; new independent GMP audits: 4.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
