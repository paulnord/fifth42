# Ada combined search

Updated: 2026-11-12T15:06:38.624069+00:00

State: **running**. Run **ada-memory-r2-job-59-20261111**; gpu with 16 preparation workers.
Verified replicated cursor: **10,788,615,680**.
New replicated logical patches: **12,615,680** in 49,280 chunks.
Combined verified selected patches, including parents: **12,615,680**.
Fresh interval: `[10776000000, 10840000000]`; replicated: `[10776000000, 10788615680]`.
Local cursor: 10,788,654,592; physical tasks group up to 2 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 305.0990116415778, 'elapsed_seconds': 1819.9265120589407, 'inflight': 1, 'max_outstanding': 3, 'maximum_item_payload_bytes': 134217728, 'maximum_prepared_payload_bytes': 15350125, 'mean_ready_depth': 0.5128970470023362, 'outstanding': 2, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 402653184, 'preparation_batch_windows': 16, 'preparation_batches': 3086, 'prepare_wall_seconds': 1819.7209156362806, 'producer_wait_capacity_seconds': 0.0030203850474208593, 'producer_wait_full_seconds': 717.4126834757626, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 0, 'ready_depth_seconds': {'0': 886.4915755366674, '1': 933.4349337962922}, 'ready_limit': 1, 'reserved_bytes': 268435456}; buffer: {'flush_count': 6171, 'flush_seconds': 49.46315174002666, 'pending_bytes': 37253, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **6,944 patches/s**; new independent GMP audits: 386.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

This run uses its assigned child claim. Historical coverage is imported only for a recorded continuation; fresh claims keep their reference parent separate. A shared coordinator holds the original parent lease.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.

An independent exact symmetry proof excludes cells [10881882043, 11250000001) for absolute residuals at most 100. These 368,117,958 cells are analytic coverage with zero native visits. Native counters above retain their journal meaning. The controller stops after the crossing native window; overlapping native and analytic intervals are counted once. See [the exact proof](evidence/analytic-tail-proof.json).
