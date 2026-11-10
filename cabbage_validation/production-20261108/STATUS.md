# Cabbage combined search

Updated: 2026-11-10T00:01:25.857418+00:00

State: **running**. Run **cabbage-extended-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **2,629,605,760**.
New replicated logical patches: **57,112,832** in 223,097 chunks.
Combined verified selected patches, including parents: **379,605,760**.
Fresh interval: `[2572492928, 3000000000]`; replicated: `[2572492928, 2629605760]`.
Local cursor: 2,630,950,784; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 783.0691320570768, 'elapsed_seconds': 2514.6271614779835, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482186, 'mean_ready_depth': 0.323569571005164, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 227561, 'prepare_wall_seconds': 2513.826942576561, 'producer_wait_capacity_seconds': 0.14711475011426955, 'producer_wait_full_seconds': 91.38703907775925, 'ready': 0, 'ready_depth_seconds': {'0': 2001.1944941006368, '1': 340.5948470849544, '2': 45.45147350174375, '3': 127.38634592964081}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 28460, 'flush_seconds': 163.073172899778, 'pending_bytes': 36447, 'pending_chunks': 2}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **23,147 patches/s**; new independent GMP audits: 1,778.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
