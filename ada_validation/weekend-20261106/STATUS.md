# Ada combined search

Updated: 2026-11-12T19:01:02.309264+00:00

State: **stopped**. Run **ada-memory-r2-job-60-20261111**; gpu with 16 preparation workers.
Verified replicated cursor: **10,881,886,464**.
New replicated logical patches: **41,886,464** in 163,619 chunks.
Combined verified selected patches, including parents: **41,886,464**.
Fresh interval: `[10840000000, 10904000000]`; replicated: `[10840000000, 10881886464]`.
Local cursor: 10,881,886,464; physical tasks group up to 2 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 794.062910152832, 'elapsed_seconds': 6305.231141049997, 'inflight': 0, 'max_outstanding': 3, 'maximum_item_payload_bytes': 134217728, 'maximum_prepared_payload_bytes': 15354053, 'mean_ready_depth': 0.5547796034017133, 'outstanding': 0, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 402653184, 'preparation_batch_windows': 16, 'preparation_batches': 10227, 'prepare_wall_seconds': 6304.477951210574, 'producer_wait_capacity_seconds': 0.010504877893254161, 'producer_wait_full_seconds': 2630.288129738532, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 0, 'ready_depth_seconds': {'0': 2807.2175058651483, '1': 3498.0136317878496}, 'ready_limit': 1, 'reserved_bytes': 0}; buffer: {'flush_count': 20454, 'flush_seconds': 188.45615077915136, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **6,643 patches/s**; new independent GMP audits: 1,279.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

This run uses its assigned child claim. Historical coverage is imported only for a recorded continuation; fresh claims keep their reference parent separate. A shared coordinator holds the original parent lease.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.

An independent exact symmetry proof excludes cells [10881882043, 11250000001) for absolute residuals at most 100. These 368,117,958 cells are analytic coverage with zero native visits. Native counters above retain their journal meaning. The controller stops after the crossing native window; overlapping native and analytic intervals are counted once. See [the exact proof](evidence/analytic-tail-proof.json).
