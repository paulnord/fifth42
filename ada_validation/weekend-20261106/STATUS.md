# Ada combined search

Updated: 2026-11-12T03:06:21.276569+00:00

State: **running**. Run **ada-memory-r2-job-54-20261111**; gpu with 16 preparation workers.
Verified replicated cursor: **10,470,123,008**.
New replicated logical patches: **14,123,008** in 55,168 chunks.
Combined verified selected patches, including parents: **14,123,008**.
Fresh interval: `[10456000000, 10520000000]`; replicated: `[10456000000, 10470123008]`.
Local cursor: 10,470,581,760; physical tasks group up to 2 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 418.2075207203161, 'elapsed_seconds': 1822.366864191019, 'inflight': 1, 'max_outstanding': 3, 'maximum_item_payload_bytes': 134217728, 'maximum_prepared_payload_bytes': 15353207, 'mean_ready_depth': 0.4338493712220498, 'outstanding': 2, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 402653184, 'preparation_batch_windows': 16, 'preparation_batches': 3559, 'prepare_wall_seconds': 1822.1180250991601, 'producer_wait_capacity_seconds': 0.0035927044227719307, 'producer_wait_full_seconds': 559.4794213349232, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 0, 'ready_depth_seconds': {'0': 1031.7341429998633, '1': 790.6327181651723}, 'ready_limit': 1, 'reserved_bytes': 268435456}; buffer: {'flush_count': 7117, 'flush_seconds': 51.66778332658578, 'pending_bytes': 183281, 'pending_chunks': 5}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **7,998 patches/s**; new independent GMP audits: 445.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

This run uses its assigned child claim. Historical coverage is imported only for a recorded continuation; fresh claims keep their reference parent separate. A shared coordinator holds the original parent lease.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.

An independent exact symmetry proof excludes cells [10881882043, 11250000001) for absolute residuals at most 100. These 368,117,958 cells are analytic coverage with zero native visits. Native counters above retain their journal meaning. The controller stops after the crossing native window; overlapping native and analytic intervals are counted once. See [the exact proof](evidence/analytic-tail-proof.json).
