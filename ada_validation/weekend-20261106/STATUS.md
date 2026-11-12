# Ada combined search

Updated: 2026-11-12T02:08:28.988242+00:00

State: **running**. Run **ada-memory-r2-job-53-20261111**; gpu with 16 preparation workers.
Verified replicated cursor: **10,443,245,056**.
New replicated logical patches: **51,245,056** in 200,176 chunks.
Combined verified selected patches, including parents: **51,245,056**.
Fresh interval: `[10392000000, 10456000000]`; replicated: `[10392000000, 10443245056]`.
Local cursor: 10,443,466,240; physical tasks group up to 2 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 1492.6480856394628, 'elapsed_seconds': 6333.810530790011, 'inflight': 1, 'max_outstanding': 3, 'maximum_item_payload_bytes': 134217728, 'maximum_prepared_payload_bytes': 15352743, 'mean_ready_depth': 0.42253047842588304, 'outstanding': 2, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 402653184, 'preparation_batch_windows': 16, 'preparation_batches': 12560, 'prepare_wall_seconds': 6333.440284660552, 'producer_wait_capacity_seconds': 0.01327422889880836, 'producer_wait_full_seconds': 1857.4606114511844, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 0, 'ready_depth_seconds': {'0': 3657.58253520343, '1': 2676.2279938335996}, 'ready_limit': 1, 'reserved_bytes': 268435456}; buffer: {'flush_count': 25118, 'flush_seconds': 180.67034431209322, 'pending_bytes': 36656, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **8,122 patches/s**; new independent GMP audits: 1,570.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

This run uses its assigned child claim. Historical coverage is imported only for a recorded continuation; fresh claims keep their reference parent separate. A shared coordinator holds the original parent lease.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.

An independent exact symmetry proof excludes cells [10881882043, 11250000001) for absolute residuals at most 100. These 368,117,958 cells are analytic coverage with zero native visits. Native counters above retain their journal meaning. The controller stops after the crossing native window; overlapping native and analytic intervals are counted once. See [the exact proof](evidence/analytic-tail-proof.json).
