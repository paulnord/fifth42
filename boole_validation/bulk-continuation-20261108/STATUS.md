# Boole combined search

Updated: 2026-11-12T02:56:03.486286+00:00

State: **running**. Run **boole-range-r3-20261111-22-recovery1**; gpu with 16 preparation workers.
Verified replicated cursor: **8,423,552,768**.
New replicated logical patches: **15,552,768** in 60,753 chunks.
Combined verified selected patches, including parents: **15,552,768**.
Fresh interval: `[8408000000, 8472000000]`; replicated: `[8408000000, 8423552768]`.
Local cursor: 8,423,923,456; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.15896506991703063, 'elapsed_seconds': 1804.6411253260449, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7688034, 'mean_ready_depth': 0.9991705701361565, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 3882, 'prepare_wall_seconds': 1802.8032746599056, 'producer_wait_capacity_seconds': 0.005168196395970881, 'producer_wait_full_seconds': 1115.9416276359698, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 1.4968197018606588, '1': 1803.1443020831794}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 7773, 'flush_seconds': 56.66194668516982, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **8,805 patches/s**; new independent GMP audits: 486.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
