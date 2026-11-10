# Cabbage combined search

Updated: 2026-11-10T03:01:53.950750+00:00

State: **running**. Run **cabbage-extended-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **2,876,921,216**.
New replicated logical patches: **304,428,288** in 1,189,173 chunks.
Combined verified selected patches, including parents: **626,921,216**.
Fresh interval: `[2572492928, 3000000000]`; replicated: `[2572492928, 2876921216]`.
Local cursor: 2,877,620,352; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 4137.164935217355, 'elapsed_seconds': 13347.713809004985, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482297, 'mean_ready_depth': 0.3399994972988229, 'outstanding': 2, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 1191585, 'prepare_wall_seconds': 13343.555367989698, 'producer_wait_capacity_seconds': 0.7701595289399847, 'producer_wait_full_seconds': 548.3599270395353, 'ready': 1, 'ready_depth_seconds': {'0': 10570.044589694531, '1': 1770.1133751708549, '2': 254.5649196463055, '3': 752.9909235622617}, 'ready_limit': 3, 'reserved_bytes': 16777216}; buffer: {'flush_count': 149029, 'flush_seconds': 868.4601916427491, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **22,850 patches/s**; new independent GMP audits: 9,310.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
