# Cabbage combined search

Updated: 2026-11-10T21:59:43.885652+00:00

State: **running**. Run **cabbage-extended-upgrade-20261110**; gpu with 16 preparation workers.
Verified replicated cursor: **1,865,136,128**.
New replicated logical patches: **326,287,104** in 1,274,559 chunks.
Combined verified selected patches, including parents: **1,365,136,128**.
Fresh interval: `[1538849024, 2250000000]`; replicated: `[1538849024, 1865136128]`.
Local cursor: 1,866,429,440; physical tasks group up to 8 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 2; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 1265.1656488965964, 'elapsed_seconds': 7683.740846364992, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 3838862, 'mean_ready_depth': 0.17560175507091877, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 79939, 'prepare_wall_seconds': 7683.385183275037, 'producer_wait_capacity_seconds': 0.05814433330669999, 'producer_wait_full_seconds': 211.2268232072238, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 6334.462466269149, '1': 1349.2783781317994}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 160042, 'flush_seconds': 934.2368271764717, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **42,582 patches/s**; new independent GMP audits: 9,993.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
