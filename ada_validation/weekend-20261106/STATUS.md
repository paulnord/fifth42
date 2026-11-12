# Ada combined search

Updated: 2026-11-12T00:22:19.072125+00:00

State: **stopped**. Run **ada-memory-r2-recovery-52-20261111**; gpu with 16 preparation workers.
Verified replicated cursor: **10,392,000,000**.
New replicated logical patches: **54,904,064** in 214,469 chunks.
Combined verified selected patches, including parents: **64,000,000**.
Fresh interval: `[10337095936, 10392000000]`; replicated: `[10337095936, 10392000000]`.
Local cursor: 10,392,000,000; physical tasks group up to 2 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 1602.3460345505737, 'elapsed_seconds': 6626.947140834993, 'inflight': 0, 'max_outstanding': 3, 'maximum_item_payload_bytes': 134217728, 'maximum_prepared_payload_bytes': 15354889, 'mean_ready_depth': 0.41308986488045957, 'outstanding': 0, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 402653184, 'preparation_batch_windows': 16, 'preparation_batches': 13405, 'prepare_wall_seconds': 6626.379963906133, 'producer_wait_capacity_seconds': 0.01320351124741137, 'producer_wait_full_seconds': 1868.8161540461006, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 0, 'ready_depth_seconds': {'0': 3889.422438050504, '1': 2737.524698977475}, 'ready_limit': 1, 'reserved_bytes': 0}; buffer: {'flush_count': 26809, 'flush_seconds': 192.5722638895968, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **8,285 patches/s**; new independent GMP audits: 1,676.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

This run uses its assigned child claim. Historical coverage is imported only for a recorded continuation; fresh claims keep their reference parent separate. A shared coordinator holds the original parent lease.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.

An independent exact symmetry proof excludes cells [10881882043, 11250000001) for absolute residuals at most 100. These 368,117,958 cells are analytic coverage with zero native visits. Native counters above retain their journal meaning. The controller stops after the crossing native window; overlapping native and analytic intervals are counted once. See [the exact proof](evidence/analytic-tail-proof.json).
