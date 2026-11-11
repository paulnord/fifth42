# Ada combined search

Updated: 2026-11-11T22:56:33.316481+00:00

State: **running**. Run **ada-memory-r2-recovery-52-20261111**; gpu with 16 preparation workers.
Verified replicated cursor: **10,349,750,528**.
New replicated logical patches: **12,654,592** in 49,432 chunks.
Combined verified selected patches, including parents: **21,750,528**.
Fresh interval: `[10337095936, 10392000000]`; replicated: `[10337095936, 10349750528]`.
Local cursor: 10,349,809,920; physical tasks group up to 2 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 369.66491618263535, 'elapsed_seconds': 1512.0750903800363, 'inflight': 1, 'max_outstanding': 3, 'maximum_item_payload_bytes': 134217728, 'maximum_prepared_payload_bytes': 15353284, 'mean_ready_depth': 0.4102464571366465, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 402653184, 'preparation_batch_windows': 16, 'preparation_batches': 3082, 'prepare_wall_seconds': 1510.6293801402207, 'producer_wait_capacity_seconds': 0.0030349886510521173, 'producer_wait_full_seconds': 421.23654341476504, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 891.751638350077, '1': 620.3234487529844}, 'ready_limit': 1, 'reserved_bytes': 402653184}; buffer: {'flush_count': 6160, 'flush_seconds': 44.99395020271186, 'pending_bytes': 36656, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **8,343 patches/s**; new independent GMP audits: 386.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

This run uses its assigned child claim. Historical coverage is imported only for a recorded continuation; fresh claims keep their reference parent separate. A shared coordinator holds the original parent lease.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.

An independent exact symmetry proof excludes cells [10881882043, 11250000001) for absolute residuals at most 100. These 368,117,958 cells are analytic coverage with zero native visits. Native counters above retain their journal meaning. The controller stops after the crossing native window; overlapping native and analytic intervals are counted once. See [the exact proof](evidence/analytic-tail-proof.json).
