# Boole combined search

Updated: 2026-11-12T10:42:58.158798+00:00

State: **running**. Run **boole-range-r3-20261111-25-recovery1**; gpu with 16 preparation workers.
Verified replicated cursor: **8,658,636,544**.
New replicated logical patches: **58,636,544** in 229,049 chunks.
Combined verified selected patches, including parents: **58,636,544**.
Fresh interval: `[8600000000, 8664000000]`; replicated: `[8600000000, 8658636544]`.
Local cursor: 8,659,238,656; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.1782237512525171, 'elapsed_seconds': 7218.212972307927, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7683761, 'mean_ready_depth': 0.9993332320029439, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 14458, 'prepare_wall_seconds': 7216.103901542374, 'producer_wait_capacity_seconds': 0.018931835307739675, 'producer_wait_full_seconds': 4649.903394995723, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 4.8128704759292305, '1': 7213.400098902057}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 28983, 'flush_seconds': 222.85912248957902, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **8,203 patches/s**; new independent GMP audits: 1,808.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
