# Boole combined search

Updated: 2026-11-12T16:38:23.933698+00:00

State: **running**. Run **boole-range-r3-20261111-28-recovery1**; gpu with 16 preparation workers.
Verified replicated cursor: **8,826,625,792**.
New replicated logical patches: **34,625,792** in 135,257 chunks.
Combined verified selected patches, including parents: **34,625,792**.
Fresh interval: `[8792000000, 8856000000]`; replicated: `[8792000000, 8826625792]`.
Local cursor: 8,827,092,736; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.15476269915234298, 'elapsed_seconds': 4508.094705439056, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7681953, 'mean_ready_depth': 0.9993712653511828, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 8546, 'prepare_wall_seconds': 4505.842123454437, 'producer_wait_capacity_seconds': 0.011290386668406427, 'producer_wait_full_seconds': 3004.850281650317, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 2.8343929514521733, '1': 4505.2603100975975}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 17118, 'flush_seconds': 124.22694177599624, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **7,762 patches/s**; new independent GMP audits: 1,069.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
