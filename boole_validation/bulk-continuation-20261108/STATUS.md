# Boole combined search

Updated: 2026-11-11T00:08:48.440204+00:00

State: **running**. Run **boole-preparation-20261110-09-r1**; gpu with 16 preparation workers.
Verified replicated cursor: **7,585,136,384**.
New replicated logical patches: **9,136,384** in 35,689 chunks.
Combined verified selected patches, including parents: **9,136,384**.
Fresh interval: `[7576000000, 7640000000]`; replicated: `[7576000000, 7585136384]`.
Local cursor: 7,585,867,520; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.15566349652362987, 'elapsed_seconds': 899.0514514779788, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7681484, 'mean_ready_depth': 0.9985752916481488, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 2394, 'prepare_wall_seconds': 897.7911095597665, 'producer_wait_capacity_seconds': 0.0032290362869389355, 'producer_wait_full_seconds': 466.33345877967076, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 1.2808828516863286, '1': 897.7705653663143}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 4790, 'flush_seconds': 32.79377226391807, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **10,894 patches/s**; new independent GMP audits: 300.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
