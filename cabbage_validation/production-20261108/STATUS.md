# Cabbage combined search

Updated: 2026-11-10T10:10:38.226242+00:00

State: **running**. Run **cabbage-extended-next-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **941,448,704**.
New replicated logical patches: **441,448,704** in 1,724,409 chunks.
Combined verified selected patches, including parents: **441,448,704**.
Fresh interval: `[500000000, 2250000000]`; replicated: `[500000000, 941448704]`.
Local cursor: 943,166,976; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 8073.718979158846, 'elapsed_seconds': 19870.623198321962, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 514657, 'mean_ready_depth': 0.13908470642271425, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 1730656, 'prepare_wall_seconds': 19864.65829744283, 'producer_wait_capacity_seconds': 1.066700181167107, 'producer_wait_full_seconds': 346.26512543670833, 'ready': 0, 'ready_depth_seconds': {'0': 17897.45118939405, '1': 1556.3999332925887, '2': 43.01636426761979, '3': 373.75571071571903}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 216472, 'flush_seconds': 1169.3915862541762, 'pending_bytes': 122160, 'pending_chunks': 7}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **22,287 patches/s**; new independent GMP audits: 13,521.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
