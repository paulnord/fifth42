# Cabbage combined search

Updated: 2026-11-10T02:31:53.893910+00:00

State: **running**. Run **cabbage-extended-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **2,835,046,784**.
New replicated logical patches: **262,553,856** in 1,025,601 chunks.
Combined verified selected patches, including parents: **585,046,784**.
Fresh interval: `[2572492928, 3000000000]`; replicated: `[2572492928, 2835046784]`.
Local cursor: 2,836,999,040; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 3578.27458578191, 'elapsed_seconds': 11541.779179041972, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482297, 'mean_ready_depth': 0.3384841407838921, 'outstanding': 4, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 1032462, 'prepare_wall_seconds': 11538.181382100855, 'producer_wait_capacity_seconds': 0.6670215807971545, 'producer_wait_full_seconds': 467.24200036824914, 'ready': 3, 'ready_depth_seconds': {'0': 9141.367092079367, '1': 1537.6471354381647, '2': 219.232778893027, '3': 643.5321717704064}, 'ready_limit': 3, 'reserved_bytes': 33554432}; buffer: {'flush_count': 129128, 'flush_seconds': 751.5687560483348, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **22,896 patches/s**; new independent GMP audits: 8,067.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
