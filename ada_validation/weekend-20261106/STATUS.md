# Ada combined search

Updated: 2026-11-11T20:44:17.311796+00:00

State: **running**. Run **ada-allocated-r3-01-20261111**; gpu with 16 preparation workers.
Verified replicated cursor: **10,309,216,768**.
New replicated logical patches: **45,216,768** in 176,628 chunks.
Combined verified selected patches, including parents: **45,216,768**.
Fresh interval: `[10264000000, 10328000000]`; replicated: `[10264000000, 10309216768]`.
Local cursor: 10,309,331,968; physical tasks group up to 1 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 5140.232689369179, 'elapsed_seconds': 8126.837183989002, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 1923881, 'mean_ready_depth': 0.22120926804584293, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batch_windows': 1, 'preparation_batches': 176998, 'prepare_wall_seconds': 8125.515146017482, 'producer_wait_capacity_seconds': 0.12425210693618283, 'producer_wait_full_seconds': 388.64405667374376, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 0, 'ready_depth_seconds': {'0': 7335.132516641868, '1': 250.43864097079495, '2': 76.50501287577208, '3': 464.7610127585358}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 24919, 'flush_seconds': 225.2668245420209, 'pending_bytes': 419430, 'pending_chunks': 6}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **5,575 patches/s**; new independent GMP audits: 1,383.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

This run uses its assigned child claim. Historical coverage is imported only for a recorded continuation; fresh claims keep their reference parent separate. A shared coordinator holds the original parent lease.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
