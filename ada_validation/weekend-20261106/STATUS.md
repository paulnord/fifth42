# Ada combined search

Updated: 2026-11-10T15:23:01.027601+00:00

State: **running**. Run **ada-suballocation-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **5,612,339,584**.
New replicated logical patches: **981,039,360** in 3,832,185 chunks.
Combined verified selected patches, including parents: **1,862,339,584**.
Fresh interval: `[4631300224, 7000000000]`; replicated: `[4631300224, 5612339584]`.
Local cursor: 5,612,749,184; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 19386.190437091398, 'elapsed_seconds': 53303.924784867035, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482928, 'mean_ready_depth': 0.6785405753329936, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 3833596, 'prepare_wall_seconds': 53279.60215992987, 'producer_wait_capacity_seconds': 2.436064710491337, 'producer_wait_full_seconds': 9112.720798261289, 'ready': 0, 'ready_depth_seconds': {'0': 37373.38814104954, '1': 5361.059798075934, '2': 900.6145419873064, '3': 9668.86230299325}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 479222, 'flush_seconds': 3701.2380732692545, 'pending_bytes': 55242, 'pending_chunks': 3}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **116 GiB**;
free-space reserve: 8 GiB.
Observed rate: **18,411 patches/s**; new independent GMP audits: 29,950.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
