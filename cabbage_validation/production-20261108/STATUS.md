# Cabbage combined search

Updated: 2026-11-10T04:32:26.980327+00:00

State: **running**. Run **cabbage-extended-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **2,998,114,688**.
New replicated logical patches: **425,621,760** in 1,662,585 chunks.
Combined verified selected patches, including parents: **748,114,688**.
Fresh interval: `[2572492928, 3000000000]`; replicated: `[2572492928, 2998114688]`.
Local cursor: 2,999,077,248; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 5799.005879528064, 'elapsed_seconds': 18781.723957701994, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482297, 'mean_ready_depth': 0.34510969762034455, 'outstanding': 2, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 1666115, 'prepare_wall_seconds': 18775.911729502608, 'producer_wait_capacity_seconds': 1.0785121088265441, 'producer_wait_full_seconds': 816.6261173165403, 'ready': 1, 'ready_depth_seconds': {'0': 14860.109452226432, '1': 2462.735286681156, '2': 357.617865159933, '3': 1101.2613529434311}, 'ready_limit': 3, 'reserved_bytes': 16777216}; buffer: {'flush_count': 208378, 'flush_seconds': 1217.133009969606, 'pending_bytes': 18225, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **22,707 patches/s**; new independent GMP audits: 13,017.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
