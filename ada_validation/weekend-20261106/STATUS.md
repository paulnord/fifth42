# Ada combined search

Updated: 2026-11-11T19:59:10.884647+00:00

State: **running**. Run **ada-allocated-r3-01-20261111**; gpu with 16 preparation workers.
Verified replicated cursor: **10,294,285,568**.
New replicated logical patches: **30,285,568** in 118,303 chunks.
Combined verified selected patches, including parents: **30,285,568**.
Fresh interval: `[10264000000, 10328000000]`; replicated: `[10264000000, 10294285568]`.
Local cursor: 10,294,369,280; physical tasks group up to 1 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 3426.538471162785, 'elapsed_seconds': 5423.241948757961, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 1923649, 'mean_ready_depth': 0.22070720414768744, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batch_windows': 1, 'preparation_batches': 118609, 'prepare_wall_seconds': 5422.350336846022, 'producer_wait_capacity_seconds': 0.08272523595951498, 'producer_wait_full_seconds': 257.9795621454832, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 0, 'ready_depth_seconds': {'0': 4895.221394505701, '1': 168.00216508773156, '2': 51.10876273154281, '3': 308.90962579200277}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 16675, 'flush_seconds': 151.37274336908013, 'pending_bytes': 69909, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **5,599 patches/s**; new independent GMP audits: 927.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

This run uses its assigned child claim. Historical coverage is imported only for a recorded continuation; fresh claims keep their reference parent separate. A shared coordinator holds the original parent lease.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
