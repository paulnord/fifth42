# Ada combined search

Updated: 2026-11-11T23:56:42.898247+00:00

State: **running**. Run **ada-memory-r2-recovery-52-20261111**; gpu with 16 preparation workers.
Verified replicated cursor: **10,379,297,024**.
New replicated logical patches: **42,201,088** in 164,848 chunks.
Combined verified selected patches, including parents: **51,297,024**.
Fresh interval: `[10337095936, 10392000000]`; replicated: `[10337095936, 10379297024]`.
Local cursor: 10,379,712,768; physical tasks group up to 2 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 1244.458651606692, 'elapsed_seconds': 5123.397290227003, 'inflight': 1, 'max_outstanding': 3, 'maximum_item_payload_bytes': 134217728, 'maximum_prepared_payload_bytes': 15353284, 'mean_ready_depth': 0.41209828572947427, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 402653184, 'preparation_batch_windows': 16, 'preparation_batches': 10386, 'prepare_wall_seconds': 5121.734667240176, 'producer_wait_capacity_seconds': 0.01024019904434681, 'producer_wait_full_seconds': 1438.79301064834, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 3012.054046687437, '1': 2111.343240413582}, 'ready_limit': 1, 'reserved_bytes': 402653184}; buffer: {'flush_count': 20768, 'flush_seconds': 148.6113943081582, 'pending_bytes': 36669, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **8,302 patches/s**; new independent GMP audits: 1,299.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

This run uses its assigned child claim. Historical coverage is imported only for a recorded continuation; fresh claims keep their reference parent separate. A shared coordinator holds the original parent lease.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.

An independent exact symmetry proof excludes cells [10881882043, 11250000001) for absolute residuals at most 100. These 368,117,958 cells are analytic coverage with zero native visits. Native counters above retain their journal meaning. The controller stops after the crossing native window; overlapping native and analytic intervals are counted once. See [the exact proof](evidence/analytic-tail-proof.json).
