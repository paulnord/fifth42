# Cabbage combined search

Updated: 2026-11-10T04:33:33.088534+00:00

State: **stopped**. Run **cabbage-extended-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **2,998,114,688**.
New replicated logical patches: **425,621,760** in 1,662,585 chunks.
Combined verified selected patches, including parents: **748,114,688**.
Fresh interval: `[2572492928, 3000000000]`; replicated: `[2572492928, 2998114688]`.
Local cursor: 3,000,000,000; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 5812.128500651626, 'elapsed_seconds': 18826.769209024962, 'inflight': 0, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482297, 'mean_ready_depth': 0.34532782527661154, 'outstanding': 0, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 1669950, 'prepare_wall_seconds': 18820.760694766068, 'producer_wait_capacity_seconds': 1.0809961535851471, 'producer_wait_full_seconds': 820.1251202141284, 'ready': 0, 'ready_depth_seconds': {'0': 14894.419427959656, '1': 2468.660636668792, '2': 358.32079155003885, '3': 1105.3683493894641}, 'ready_limit': 3, 'reserved_bytes': 0}; buffer: {'flush_count': 208859, 'flush_seconds': 1219.9585488077719, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **22,705 patches/s**; new independent GMP audits: 13,047.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
