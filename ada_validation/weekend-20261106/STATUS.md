# Ada combined search

Updated: 2026-11-11T17:23:46.266853+00:00

State: **running**. Run **ada-allocated-r3-00-20261111**; gpu with 16 preparation workers.
Verified replicated cursor: **6,937,910,656**.
New replicated logical patches: **14,188,544** in 55,424 chunks.
Combined verified selected patches, including parents: **3,187,910,656**.
Fresh interval: `[6923722112, 7000000000]`; replicated: `[6923722112, 6937910656]`.
Local cursor: 6,938,566,016; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 170.54873014451005, 'elapsed_seconds': 914.6112100899918, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7680760, 'mean_ready_depth': 0.4493584157041461, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 3594, 'prepare_wall_seconds': 913.7617265256704, 'producer_wait_capacity_seconds': 0.003509673580992967, 'producer_wait_full_seconds': 281.2103134477511, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 503.62296227173647, '1': 410.98824435129063}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 7184, 'flush_seconds': 45.38086242962163, 'pending_bytes': 18422, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **16,086 patches/s**; new independent GMP audits: 450.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

This run uses its assigned child claim. Historical coverage is imported only for a recorded continuation; fresh claims keep their reference parent separate. A shared coordinator holds the original parent lease.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
