# Ada combined search

Updated: 2026-11-12T09:27:45.130859+00:00

State: **running**. Run **ada-memory-r2-job-56-20261111**; gpu with 16 preparation workers.
Verified replicated cursor: **10,644,620,800**.
New replicated logical patches: **60,620,800** in 236,800 chunks.
Combined verified selected patches, including parents: **60,620,800**.
Fresh interval: `[10584000000, 10648000000]`; replicated: `[10584000000, 10644620800]`.
Local cursor: 10,645,079,552; physical tasks group up to 2 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 1671.2571201086976, 'elapsed_seconds': 8128.757426287979, 'inflight': 1, 'max_outstanding': 3, 'maximum_item_payload_bytes': 134217728, 'maximum_prepared_payload_bytes': 15352064, 'mean_ready_depth': 0.4685793686125502, 'outstanding': 2, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 402653184, 'preparation_batch_windows': 16, 'preparation_batches': 14894, 'prepare_wall_seconds': 8128.320847567171, 'producer_wait_capacity_seconds': 0.014968985924497247, 'producer_wait_full_seconds': 2814.4953340644715, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 0, 'ready_depth_seconds': {'0': 4319.78940223041, '1': 3808.9680224145995}, 'ready_limit': 1, 'reserved_bytes': 268435456}; buffer: {'flush_count': 29786, 'flush_seconds': 275.6239831793355, 'pending_bytes': 36656, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **7,504 patches/s**; new independent GMP audits: 1,862.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

This run uses its assigned child claim. Historical coverage is imported only for a recorded continuation; fresh claims keep their reference parent separate. A shared coordinator holds the original parent lease.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.

An independent exact symmetry proof excludes cells [10881882043, 11250000001) for absolute residuals at most 100. These 368,117,958 cells are analytic coverage with zero native visits. Native counters above retain their journal meaning. The controller stops after the crossing native window; overlapping native and analytic intervals are counted once. See [the exact proof](evidence/analytic-tail-proof.json).
