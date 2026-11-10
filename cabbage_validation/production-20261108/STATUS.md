# Cabbage combined search

Updated: 2026-11-10T02:01:42.502845+00:00

State: **running**. Run **cabbage-extended-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **2,795,366,528**.
New replicated logical patches: **222,873,600** in 870,600 chunks.
Combined verified selected patches, including parents: **545,366,528**.
Fresh interval: `[2572492928, 3000000000]`; replicated: `[2572492928, 2795366528]`.
Local cursor: 2,796,055,168; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 3021.68750926567, 'elapsed_seconds': 9737.501244679966, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482297, 'mean_ready_depth': 0.33628687621328074, 'outstanding': 2, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 873076, 'prepare_wall_seconds': 9734.459058301814, 'producer_wait_capacity_seconds': 0.5639643965405412, 'producer_wait_full_seconds': 385.34624466020614, 'ready': 1, 'ready_depth_seconds': {'0': 7716.2405832762015, '1': 1302.0425206759246, '2': 185.1030640071258, '3': 534.1150756687275}, 'ready_limit': 3, 'reserved_bytes': 16777216}; buffer: {'flush_count': 109194, 'flush_seconds': 634.54830355983, 'pending_bytes': 18214, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **22,948 patches/s**; new independent GMP audits: 6,821.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
