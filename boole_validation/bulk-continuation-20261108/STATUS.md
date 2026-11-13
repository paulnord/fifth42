# Boole combined search

Updated: 2026-11-13T00:56:22.151554+00:00

State: **running**. Run **boole-shared-deadline-r1-32-overnight-20261112**; gpu with 16 preparation workers.
Verified replicated cursor: **9,073,786,624**.
New replicated logical patches: **25,786,624** in 100,729 chunks.
Combined verified selected patches, including parents: **25,786,624**.
Fresh interval: `[9048000000, 9112000000]`; replicated: `[9048000000, 9073786624]`.
Local cursor: 9,074,247,424; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.1573461857624352, 'elapsed_seconds': 3721.8600269340677, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7683087, 'mean_ready_depth': 0.9994029723843397, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 6394, 'prepare_wall_seconds': 3719.259804969537, 'producer_wait_capacity_seconds': 0.00806889042723924, 'producer_wait_full_seconds': 2588.248256877181, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 2.2220504976576194, '1': 3719.637973716366}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 12807, 'flush_seconds': 99.12195294047706, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **7,034 patches/s**; new independent GMP audits: 800.
Deadline: **2026-11-13T09:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
