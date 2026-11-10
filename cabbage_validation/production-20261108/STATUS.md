# Cabbage combined search

Updated: 2026-11-10T07:40:10.268649+00:00

State: **running**. Run **cabbage-extended-next-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **742,004,224**.
New replicated logical patches: **242,004,224** in 945,329 chunks.
Combined verified selected patches, including parents: **242,004,224**.
Fresh interval: `[500000000, 2250000000]`; replicated: `[500000000, 742004224]`.
Local cursor: 743,600,640; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 4392.4783000760945, 'elapsed_seconds': 10843.555429313972, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 514228, 'mean_ready_depth': 0.14020238933287232, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 951171, 'prepare_wall_seconds': 10840.274530290219, 'producer_wait_capacity_seconds': 0.5846801243023947, 'producer_wait_full_seconds': 188.741090630705, 'ready': 0, 'ready_depth_seconds': {'0': 9750.029773615592, '1': 869.6062946845195, '2': 21.071995269856416, '3': 202.84736494300887}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 118976, 'flush_seconds': 636.9947846805444, 'pending_bytes': 104666, 'pending_chunks': 6}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **22,437 patches/s**; new independent GMP audits: 7,432.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
