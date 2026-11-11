# Ada combined search

Updated: 2026-11-11T19:29:03.182049+00:00

State: **running**. Run **ada-allocated-r3-01-20261111**; gpu with 16 preparation workers.
Verified replicated cursor: **10,284,190,976**.
New replicated logical patches: **20,190,976** in 78,871 chunks.
Combined verified selected patches, including parents: **20,190,976**.
Fresh interval: `[10264000000, 10328000000]`; replicated: `[10264000000, 10284190976]`.
Local cursor: 10,284,281,856; physical tasks group up to 1 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 2284.5487771221087, 'elapsed_seconds': 3615.8907772299717, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 1923649, 'mean_ready_depth': 0.22048935357331995, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batch_windows': 1, 'preparation_batches': 79223, 'prepare_wall_seconds': 3615.2939317203127, 'producer_wait_capacity_seconds': 0.05518215452320874, 'producer_wait_full_seconds': 171.42734583100537, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 0, 'ready_depth_seconds': {'0': 3263.616575872118, '1': 112.64166621648474, '2': 34.273848391429055, '3': 205.35868568794103}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 11127, 'flush_seconds': 101.26133510895306, 'pending_bytes': 279604, 'pending_chunks': 4}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **5,609 patches/s**; new independent GMP audits: 619.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

This run uses its assigned child claim. Historical coverage is imported only for a recorded continuation; fresh claims keep their reference parent separate. A shared coordinator holds the original parent lease.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
