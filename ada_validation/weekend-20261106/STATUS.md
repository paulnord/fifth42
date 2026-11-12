# Ada combined search

Updated: 2026-11-12T10:06:19.418209+00:00

State: **running**. Run **ada-memory-r2-job-57-20261111**; gpu with 16 preparation workers.
Verified replicated cursor: **10,661,017,088**.
New replicated logical patches: **13,017,088** in 50,848 chunks.
Combined verified selected patches, including parents: **13,017,088**.
Fresh interval: `[10648000000, 10712000000]`; replicated: `[10648000000, 10661017088]`.
Local cursor: 10,661,488,128; physical tasks group up to 2 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 379.65736800583545, 'elapsed_seconds': 1823.1030850850511, 'inflight': 1, 'max_outstanding': 3, 'maximum_item_payload_bytes': 134217728, 'maximum_prepared_payload_bytes': 15348142, 'mean_ready_depth': 0.47562816105410805, 'outstanding': 1, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 402653184, 'preparation_batch_windows': 16, 'preparation_batches': 3293, 'prepare_wall_seconds': 1822.8260141508654, 'producer_wait_capacity_seconds': 0.00335100619122386, 'producer_wait_full_seconds': 650.4842903513927, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 0, 'ready_depth_seconds': {'0': 955.9839163919678, '1': 867.119167771074}, 'ready_limit': 1, 'reserved_bytes': 134217728}; buffer: {'flush_count': 6586, 'flush_seconds': 41.80239965941291, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **7,398 patches/s**; new independent GMP audits: 412.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

This run uses its assigned child claim. Historical coverage is imported only for a recorded continuation; fresh claims keep their reference parent separate. A shared coordinator holds the original parent lease.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.

An independent exact symmetry proof excludes cells [10881882043, 11250000001) for absolute residuals at most 100. These 368,117,958 cells are analytic coverage with zero native visits. Native counters above retain their journal meaning. The controller stops after the crossing native window; overlapping native and analytic intervals are counted once. See [the exact proof](evidence/analytic-tail-proof.json).
