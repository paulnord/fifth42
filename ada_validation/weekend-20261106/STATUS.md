# Ada combined search

Updated: 2026-11-12T13:04:15.020659+00:00

State: **running**. Run **ada-memory-r2-job-58-20261111**; gpu with 16 preparation workers.
Verified replicated cursor: **10,737,886,720**.
New replicated logical patches: **25,886,720** in 101,120 chunks.
Combined verified selected patches, including parents: **25,886,720**.
Fresh interval: `[10712000000, 10776000000]`; replicated: `[10712000000, 10737886720]`.
Local cursor: 10,737,952,256; physical tasks group up to 2 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 670.7989278131863, 'elapsed_seconds': 3615.4626260889927, 'inflight': 1, 'max_outstanding': 3, 'maximum_item_payload_bytes': 134217728, 'maximum_prepared_payload_bytes': 15349119, 'mean_ready_depth': 0.4958449809754139, 'outstanding': 2, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 402653184, 'preparation_batch_windows': 16, 'preparation_batches': 6319, 'prepare_wall_seconds': 3615.1504534160485, 'producer_wait_capacity_seconds': 0.006280257948674262, 'producer_wait_full_seconds': 1362.7963840997545, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 0, 'ready_depth_seconds': {'0': 1822.7536266836105, '1': 1792.7089970504167}, 'ready_limit': 1, 'reserved_bytes': 268435456}; buffer: {'flush_count': 12637, 'flush_seconds': 129.89419350994285, 'pending_bytes': 146627, 'pending_chunks': 4}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **7,158 patches/s**; new independent GMP audits: 790.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

This run uses its assigned child claim. Historical coverage is imported only for a recorded continuation; fresh claims keep their reference parent separate. A shared coordinator holds the original parent lease.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.

An independent exact symmetry proof excludes cells [10881882043, 11250000001) for absolute residuals at most 100. These 368,117,958 cells are analytic coverage with zero native visits. Native counters above retain their journal meaning. The controller stops after the crossing native window; overlapping native and analytic intervals are counted once. See [the exact proof](evidence/analytic-tail-proof.json).
