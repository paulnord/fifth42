# Boole combined search

Updated: 2026-11-13T00:41:20.339174+00:00

State: **running**. Run **boole-shared-deadline-r1-32-overnight-20261112**; gpu with 16 preparation workers.
Verified replicated cursor: **9,067,595,264**.
New replicated logical patches: **19,595,264** in 76,544 chunks.
Combined verified selected patches, including parents: **19,595,264**.
Fresh interval: `[9048000000, 9112000000]`; replicated: `[9048000000, 9067595264]`.
Local cursor: 9,067,933,184; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.15516298613511026, 'elapsed_seconds': 2821.6931690350175, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7681937, 'mean_ready_depth': 0.9993782530181011, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 4854, 'prepare_wall_seconds': 2821.467093134881, 'producer_wait_capacity_seconds': 0.00615088501945138, 'producer_wait_full_seconds': 1964.0302547205938, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 1.754376271739602, '1': 2819.9387898233254}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 9723, 'flush_seconds': 74.88938235247042, 'pending_bytes': 79428, 'pending_chunks': 4}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **7,043 patches/s**; new independent GMP audits: 607.
Deadline: **2026-11-13T09:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
