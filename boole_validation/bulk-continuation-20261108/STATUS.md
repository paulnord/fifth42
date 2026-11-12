# Boole combined search

Updated: 2026-11-12T07:34:54.544693+00:00

State: **running**. Run **boole-range-r3-20261111-24-recovery1**; gpu with 16 preparation workers.
Verified replicated cursor: **8,566,243,072**.
New replicated logical patches: **30,243,072** in 118,137 chunks.
Combined verified selected patches, including parents: **30,243,072**.
Fresh interval: `[8536000000, 8600000000]`; replicated: `[8536000000, 8566243072]`.
Local cursor: 8,566,374,144; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.1590622451622039, 'elapsed_seconds': 3608.9921285909368, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7685457, 'mean_ready_depth': 0.9992801090335863, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 7410, 'prepare_wall_seconds': 3606.996584012639, 'producer_wait_capacity_seconds': 0.010006838361732662, 'producer_wait_full_seconds': 2295.2377888027113, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 2.598078621318564, '1': 3606.394047759706}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 14847, 'flush_seconds': 111.40494307281915, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **8,407 patches/s**; new independent GMP audits: 927.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
