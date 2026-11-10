# Boole combined search

Updated: 2026-11-10T21:04:27.873139+00:00

State: **running**. Run **boole-preparation-20261110-07-r1**; gpu with 16 preparation workers.
Verified replicated cursor: **7,464,271,616**.
New replicated logical patches: **16,271,616** in 63,561 chunks.
Combined verified selected patches, including parents: **16,271,616**.
Fresh interval: `[7448000000, 7512000000]`; replicated: `[7448000000, 7464271616]`.
Local cursor: 7,464,480,512; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.15311738348100334, 'elapsed_seconds': 1442.9184106189641, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7681009, 'mean_ready_depth': 0.9973896817114761, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 4010, 'prepare_wall_seconds': 1441.7365254783654, 'producer_wait_capacity_seconds': 0.005147959105670452, 'producer_wait_full_seconds': 717.65149504703, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 3.766473776078783, '1': 1439.1519343028776}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 8039, 'flush_seconds': 50.22161090490408, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **11,375 patches/s**; new independent GMP audits: 502.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
