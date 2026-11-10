# Cabbage combined search

Updated: 2026-11-10T00:16:26.267489+00:00

State: **running**. Run **cabbage-extended-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **2,651,492,736**.
New replicated logical patches: **78,999,808** in 308,593 chunks.
Combined verified selected patches, including parents: **401,492,736**.
Fresh interval: `[2572492928, 3000000000]`; replicated: `[2572492928, 2651492736]`.
Local cursor: 2,651,666,816; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 1061.8257309773471, 'elapsed_seconds': 3416.0856211709906, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482186, 'mean_ready_depth': 0.32741530376532796, 'outstanding': 4, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 308612, 'prepare_wall_seconds': 3413.544127384259, 'producer_wait_capacity_seconds': 0.19937451073201373, 'producer_wait_full_seconds': 125.60476914286846, 'ready': 3, 'ready_depth_seconds': {'0': 2713.124005778518, '1': 463.98678523109993, '2': 62.432561518158764, '3': 176.54226769221714}, 'ready_limit': 3, 'reserved_bytes': 33554432}; buffer: {'flush_count': 38596, 'flush_seconds': 222.2772063553566, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **23,113 patches/s**; new independent GMP audits: 2,412.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
