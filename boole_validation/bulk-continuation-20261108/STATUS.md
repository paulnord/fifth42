# Boole combined search

Updated: 2026-11-10T12:02:42.781812+00:00

State: **running**. Run **boole-delegated-20261109-01**; gpu with 16 preparation workers.
Verified replicated cursor: **7,097,159,424**.
New replicated logical patches: **33,159,424** in 129,529 chunks.
Combined verified selected patches, including parents: **33,159,424**.
Fresh interval: `[7064000000, 7128000000]`; replicated: `[7064000000, 7097159424]`.
Local cursor: 7,097,487,104; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 45.45409002027009, 'elapsed_seconds': 2709.697894098994, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482111, 'mean_ready_depth': 2.1152190404799462, 'outstanding': 4, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 130717, 'prepare_wall_seconds': 2709.230618117319, 'producer_wait_capacity_seconds': 0.0826190029620193, 'producer_wait_full_seconds': 1194.6768826934276, 'ready': 3, 'ready_depth_seconds': {'0': 416.3299981164164, '1': 423.8301829848788, '2': 300.83874027145794, '3': 1568.6989720062702}, 'ready_limit': 3, 'reserved_bytes': 33554432}; buffer: {'flush_count': 16360, 'flush_seconds': 91.87205338245258, 'pending_bytes': 18420, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **12,348 patches/s**; new independent GMP audits: 1,022.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
