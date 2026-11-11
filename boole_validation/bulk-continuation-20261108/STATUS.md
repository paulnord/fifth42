# Boole combined search

Updated: 2026-11-11T06:55:05.086523+00:00

State: **running**. Run **boole-preparation-20261110-13-r1**; gpu with 16 preparation workers.
Verified replicated cursor: **7,840,608,000**.
New replicated logical patches: **8,608,000** in 33,625 chunks.
Combined verified selected patches, including parents: **8,608,000**.
Fresh interval: `[7832000000, 7896000000]`; replicated: `[7832000000, 7840608000]`.
Local cursor: 7,841,298,176; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.15200726385228336, 'elapsed_seconds': 898.7588927929755, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7680184, 'mean_ready_depth': 0.9988786811222616, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 2256, 'prepare_wall_seconds': 898.700025053462, 'producer_wait_capacity_seconds': 0.002917761099524796, 'producer_wait_full_seconds': 495.7024958739057, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 1.0077931130072102, '1': 897.7510974799516}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 4517, 'flush_seconds': 31.355953506135847, 'pending_bytes': 38085, 'pending_chunks': 2}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **10,269 patches/s**; new independent GMP audits: 282.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
