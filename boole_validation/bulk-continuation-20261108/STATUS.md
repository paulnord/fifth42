# Boole combined search

Updated: 2026-11-11T21:45:08.826079+00:00

State: **running**. Run **boole-range-r3-20261111-19-recovery1**; gpu with 16 preparation workers.
Verified replicated cursor: **8,257,107,712**.
New replicated logical patches: **41,107,712** in 160,577 chunks.
Combined verified selected patches, including parents: **41,107,712**.
Fresh interval: `[8216000000, 8280000000]`; replicated: `[8216000000, 8257107712]`.
Local cursor: 8,257,736,192; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.15326224162708968, 'elapsed_seconds': 4520.103417690028, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7682667, 'mean_ready_depth': 0.9992581719374816, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 10187, 'prepare_wall_seconds': 4519.965302243771, 'producer_wait_capacity_seconds': 0.013439731963444501, 'producer_wait_full_seconds': 2708.225427414058, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 3.353137460711878, '1': 4516.750278129301}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 20412, 'flush_seconds': 152.98394707706757, 'pending_bytes': 96105, 'pending_chunks': 5}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **9,229 patches/s**; new independent GMP audits: 1,274.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
