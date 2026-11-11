# Ada combined search

Updated: 2026-11-11T18:58:55.517033+00:00

State: **running**. Run **ada-allocated-r3-01-20261111**; gpu with 16 preparation workers.
Verified replicated cursor: **10,274,085,376**.
New replicated logical patches: **10,085,376** in 39,396 chunks.
Combined verified selected patches, including parents: **10,085,376**.
Fresh interval: `[10264000000, 10328000000]`; replicated: `[10264000000, 10274085376]`.
Local cursor: 10,274,157,056; physical tasks group up to 1 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 1142.3436442008242, 'elapsed_seconds': 1808.624419153959, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 1923649, 'mean_ready_depth': 0.22016976582724238, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batch_windows': 1, 'preparation_batches': 39674, 'prepare_wall_seconds': 1808.3138913000585, 'producer_wait_capacity_seconds': 0.027569230878725648, 'producer_wait_full_seconds': 85.81841011112556, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 0, 'ready_depth_seconds': {'0': 1632.7615293855197, '1': 56.168794742494356, '2': 17.046663119923323, '3': 102.64743128407281}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 5566, 'flush_seconds': 50.52336866070982, 'pending_bytes': 349501, 'pending_chunks': 5}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **5,615 patches/s**; new independent GMP audits: 310.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

This run uses its assigned child claim. Historical coverage is imported only for a recorded continuation; fresh claims keep their reference parent separate. A shared coordinator holds the original parent lease.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
