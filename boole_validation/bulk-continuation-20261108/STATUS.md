# Boole combined search

Updated: 2026-11-10T09:49:51.845418+00:00

State: **stopped**. Run **boole-extra-20261109-b**; gpu with 16 preparation workers.
Verified replicated cursor: **498,673,408**.
New replicated logical patches: **198,673,408** in 776,068 chunks.
Combined verified selected patches, including parents: **198,673,408**.
Fresh interval: `[300000000, 500000000]`; replicated: `[300000000, 498673408]`.
Local cursor: 500,000,000; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 2238.7972534035216, 'elapsed_seconds': 10723.237061018008, 'inflight': 0, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 514009, 'mean_ready_depth': 0.5795491473404547, 'outstanding': 0, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 781250, 'prepare_wall_seconds': 10720.462639142876, 'producer_wait_capacity_seconds': 0.47862880886532366, 'producer_wait_full_seconds': 1393.0380721369293, 'ready': 0, 'ready_depth_seconds': {'0': 7953.051444765646, '1': 954.298415413883, '2': 187.31711444677785, '3': 1628.5700837117038}, 'ready_limit': 3, 'reserved_bytes': 0}; buffer: {'flush_count': 97810, 'flush_seconds': 519.4205230435473, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **18,650 patches/s**; new independent GMP audits: 6,104.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
