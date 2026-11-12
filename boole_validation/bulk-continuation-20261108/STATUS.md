# Boole combined search

Updated: 2026-11-12T22:39:47.507450+00:00

State: **running**. Run **boole-range-r3-20261111-30-recovery2**; gpu with 16 preparation workers.
Verified replicated cursor: **8,959,803,136**.
New replicated logical patches: **25,942,272** in 101,337 chunks.
Combined verified selected patches, including parents: **39,803,136**.
Fresh interval: `[8933860864, 8984000000]`; replicated: `[8933860864, 8959803136]`.
Local cursor: 8,960,263,936; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.20310466235969216, 'elapsed_seconds': 3610.200453906087, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7681479, 'mean_ready_depth': 0.9993670874257616, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 6434, 'prepare_wall_seconds': 3607.7220972989453, 'producer_wait_capacity_seconds': 0.008629680960439146, 'producer_wait_full_seconds': 2476.1547884010943, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 2.2849387727910653, '1': 3607.915512643289}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 12907, 'flush_seconds': 99.77736542490311, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **7,297 patches/s**; new independent GMP audits: 805.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
