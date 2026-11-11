# Ada combined search

Updated: 2026-11-11T17:08:42.710131+00:00

State: **running**. Run **ada-allocated-r3-00-20261111**; gpu with 16 preparation workers.
Verified replicated cursor: **6,923,724,160**.
New replicated logical patches: **2,048** in 8 chunks.
Combined verified selected patches, including parents: **3,173,724,160**.
Fresh interval: `[6923722112, 7000000000]`; replicated: `[6923722112, 6923724160]`.
Local cursor: 6,924,017,024; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 2.0725165250478312, 'elapsed_seconds': 10.000902610016055, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7677700, 'mean_ready_depth': 0.44905323028445, 'outstanding': 2, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 39, 'prepare_wall_seconds': 9.968898522900417, 'producer_wait_capacity_seconds': 4.071707371622324e-05, 'producer_wait_full_seconds': 3.0922291068709455, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 0, 'ready_depth_seconds': {'0': 5.509961811185349, '1': 4.4909376227878965}, 'ready_limit': 1, 'reserved_bytes': 25165824}; buffer: {'flush_count': 76, 'flush_seconds': 0.39843228296376765, 'pending_bytes': 73649, 'pending_chunks': 4}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **15,561 patches/s**; new independent GMP audits: 5.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

This run uses its assigned child claim. Historical coverage is imported only for a recorded continuation; fresh claims keep their reference parent separate. A shared coordinator holds the original parent lease.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
