# Cabbage combined search

Updated: 2026-11-10T11:35:46.516605+00:00

State: **running**. Run **cabbage-extended-rotation-20261110T110534Z**; gpu with 16 preparation workers.
Verified replicated cursor: **1,044,905,216**.
New replicated logical patches: **39,069,440** in 152,615 chunks.
Combined verified selected patches, including parents: **544,905,216**.
Fresh interval: `[1005835776, 2250000000]`; replicated: `[1005835776, 1044905216]`.
Local cursor: 1,046,490,880; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 728.2353196452605, 'elapsed_seconds': 1795.998118871008, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 514397, 'mean_ready_depth': 0.1419309914273916, 'outstanding': 2, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 158245, 'prepare_wall_seconds': 1795.4462640298298, 'producer_wait_capacity_seconds': 0.0980277078342624, 'producer_wait_full_seconds': 29.846378518966958, 'ready': 1, 'ready_depth_seconds': {'0': 1609.3573307731422, '1': 150.35404410940828, '2': 4.306479998631403, '3': 31.98026316880714}, 'ready_limit': 3, 'reserved_bytes': 16777216}; buffer: {'flush_count': 19792, 'flush_seconds': 110.05957482208032, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **22,477 patches/s**; new independent GMP audits: 1,237.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
