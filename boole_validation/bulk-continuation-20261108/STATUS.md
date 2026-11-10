# Boole combined search

Updated: 2026-11-10T23:15:38.350424+00:00

State: **running**. Run **boole-preparation-20261110-08-r1**; gpu with 16 preparation workers.
Verified replicated cursor: **7,550,762,752**.
New replicated logical patches: **38,762,752** in 151,417 chunks.
Combined verified selected patches, including parents: **38,762,752**.
Fresh interval: `[7512000000, 7576000000]`; replicated: `[7512000000, 7550762752]`.
Local cursor: 7,551,536,896; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.1679422130691819, 'elapsed_seconds': 3610.674145490979, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7681667, 'mean_ready_depth': 0.9987730168571092, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 9650, 'prepare_wall_seconds': 3609.4024633549852, 'producer_wait_capacity_seconds': 0.01217531884321943, 'producer_wait_full_seconds': 1868.5980594769353, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 4.430234000959899, '1': 3606.2439091799897}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 19333, 'flush_seconds': 132.09684278070927, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **10,944 patches/s**; new independent GMP audits: 1,207.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
