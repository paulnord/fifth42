# Boole combined search

Updated: 2026-11-11T01:08:56.870023+00:00

State: **running**. Run **boole-preparation-20261110-09-r1**; gpu with 16 preparation workers.
Verified replicated cursor: **7,624,650,496**.
New replicated logical patches: **48,650,496** in 190,041 chunks.
Combined verified selected patches, including parents: **48,650,496**.
Fresh interval: `[7576000000, 7640000000]`; replicated: `[7576000000, 7624650496]`.
Local cursor: 7,624,756,992; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.16841774940257892, 'elapsed_seconds': 4503.540611466975, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7681622, 'mean_ready_depth': 0.9987895798608858, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 11879, 'prepare_wall_seconds': 4498.0857072932995, 'producer_wait_capacity_seconds': 0.015881461615208536, 'producer_wait_full_seconds': 2348.742040908197, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 5.451172433444299, '1': 4498.0894352135365}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 23788, 'flush_seconds': 163.24234967702068, 'pending_bytes': 19027, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **10,802 patches/s**; new independent GMP audits: 1,485.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
