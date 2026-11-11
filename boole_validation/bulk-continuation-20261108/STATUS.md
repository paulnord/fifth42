# Boole combined search

Updated: 2026-11-11T15:57:41.431507+00:00

State: **running**. Run **boole-preparation-20261110-18-r1**; gpu with 16 preparation workers.
Verified replicated cursor: **8,160,517,888**.
New replicated logical patches: **8,517,888** in 33,273 chunks.
Combined verified selected patches, including parents: **8,517,888**.
Fresh interval: `[8152000000, 8216000000]`; replicated: `[8152000000, 8160517888]`.
Local cursor: 8,160,616,192; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.15566051681526005, 'elapsed_seconds': 902.0313761470024, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7681305, 'mean_ready_depth': 0.9989628977515801, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 2090, 'prepare_wall_seconds': 900.4345128264977, 'producer_wait_capacity_seconds': 0.002753945009317249, 'producer_wait_full_seconds': 530.6254672639188, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 0.9354963383520953, '1': 901.0958773786551}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 4183, 'flush_seconds': 30.44247320847353, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **9,478 patches/s**; new independent GMP audits: 262.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
