# Boole combined search

Updated: 2026-11-11T03:03:35.969260+00:00

State: **running**. Run **boole-preparation-20261110-10-r1**; gpu with 16 preparation workers.
Verified replicated cursor: **7,697,342,208**.
New replicated logical patches: **57,342,208** in 223,993 chunks.
Combined verified selected patches, including parents: **57,342,208**.
Fresh interval: `[7640000000, 7704000000]`; replicated: `[7640000000, 7697342208]`.
Local cursor: 7,697,800,960; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.16345035785343498, 'elapsed_seconds': 5435.479577587976, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7684274, 'mean_ready_depth': 0.9989125441561366, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 14097, 'prepare_wall_seconds': 5435.308949440194, 'producer_wait_capacity_seconds': 0.01809417235199362, 'producer_wait_full_seconds': 2885.2647844569874, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 5.910841820877977, '1': 5429.568733557127}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 28236, 'flush_seconds': 188.75163443910424, 'pending_bytes': 76094, 'pending_chunks': 4}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **10,621 patches/s**; new independent GMP audits: 1,762.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
