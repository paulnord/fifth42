# Ada combined search

Updated: 2026-11-12T09:51:16.001567+00:00

State: **running**. Run **ada-memory-r2-job-57-20261111**; gpu with 16 preparation workers.
Verified replicated cursor: **10,654,510,592**.
New replicated logical patches: **6,510,592** in 25,432 chunks.
Combined verified selected patches, including parents: **6,510,592**.
Fresh interval: `[10648000000, 10712000000]`; replicated: `[10648000000, 10654510592]`.
Local cursor: 10,654,811,648; physical tasks group up to 2 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 190.13805010239594, 'elapsed_seconds': 914.7771593530197, 'inflight': 1, 'max_outstanding': 3, 'maximum_item_payload_bytes': 134217728, 'maximum_prepared_payload_bytes': 15348142, 'mean_ready_depth': 0.4752946372972459, 'outstanding': 2, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 402653184, 'preparation_batch_windows': 16, 'preparation_batches': 1654, 'prepare_wall_seconds': 914.6686938401544, 'producer_wait_capacity_seconds': 0.0016956320032477379, 'producer_wait_full_seconds': 326.4247049209662, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 0, 'ready_depth_seconds': {'0': 479.98847901658155, '1': 434.7886781624984}, 'ready_limit': 1, 'reserved_bytes': 268435456}; buffer: {'flush_count': 3306, 'flush_seconds': 21.24060186871793, 'pending_bytes': 219923, 'pending_chunks': 6}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **7,401 patches/s**; new independent GMP audits: 207.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

This run uses its assigned child claim. Historical coverage is imported only for a recorded continuation; fresh claims keep their reference parent separate. A shared coordinator holds the original parent lease.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.

An independent exact symmetry proof excludes cells [10881882043, 11250000001) for absolute residuals at most 100. These 368,117,958 cells are analytic coverage with zero native visits. Native counters above retain their journal meaning. The controller stops after the crossing native window; overlapping native and analytic intervals are counted once. See [the exact proof](evidence/analytic-tail-proof.json).
