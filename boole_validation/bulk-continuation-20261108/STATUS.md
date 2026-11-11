# Boole combined search

Updated: 2026-11-11T16:49:26.577861+00:00

State: **stopped**. Run **boole-preparation-20261110-18-r1**; gpu with 16 preparation workers.
Verified replicated cursor: **8,189,617,920**.
New replicated logical patches: **37,617,920** in 146,945 chunks.
Combined verified selected patches, including parents: **37,617,920**.
Fresh interval: `[8152000000, 8216000000]`; replicated: `[8152000000, 8189617920]`.
Local cursor: 8,189,617,920; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 0.16502600588137284, 'elapsed_seconds': 3982.519450899039, 'inflight': 0, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7681453, 'mean_ready_depth': 0.9992040096572884, 'outstanding': 0, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 9186, 'prepare_wall_seconds': 3980.744470991136, 'producer_wait_capacity_seconds': 0.012022887356579304, 'producer_wait_full_seconds': 2351.5413159308955, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 0, 'ready_depth_seconds': {'0': 3.1700441025896, '1': 3979.349403876462}, 'ready_limit': 1, 'reserved_bytes': 0}; buffer: {'flush_count': 18402, 'flush_seconds': 136.44448204583023, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **9,445 patches/s**; new independent GMP audits: 1,149.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
