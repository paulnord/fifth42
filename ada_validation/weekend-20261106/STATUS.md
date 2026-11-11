# Ada combined search

Updated: 2026-11-11T20:14:14.767640+00:00

State: **running**. Run **ada-allocated-r3-01-20261111**; gpu with 16 preparation workers.
Verified replicated cursor: **10,299,155,200**.
New replicated logical patches: **35,155,200** in 137,325 chunks.
Combined verified selected patches, including parents: **35,155,200**.
Fresh interval: `[10264000000, 10328000000]`; replicated: `[10264000000, 10299155200]`.
Local cursor: 10,299,380,736; physical tasks group up to 1 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 3999.3781930689, 'elapsed_seconds': 6327.302517578006, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 1923649, 'mean_ready_depth': 0.22077173098412828, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batch_windows': 1, 'preparation_batches': 138185, 'prepare_wall_seconds': 6326.26300086343, 'producer_wait_capacity_seconds': 0.09662927396129817, 'producer_wait_full_seconds': 301.41629526828183, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 0, 'ready_depth_seconds': {'0': 5711.463950872945, '1': 195.5028021056205, '2': 59.62056471488904, '3': 360.71519924351014}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 19435, 'flush_seconds': 176.38105230033398, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **5,591 patches/s**; new independent GMP audits: 1,080.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

This run uses its assigned child claim. Historical coverage is imported only for a recorded continuation; fresh claims keep their reference parent separate. A shared coordinator holds the original parent lease.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
