# Ada combined search

Updated: 2026-11-10T06:51:33.100049+00:00

State: **running**. Run **ada-suballocation-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **5,063,542,912**.
New replicated logical patches: **432,242,688** in 1,688,448 chunks.
Combined verified selected patches, including parents: **1,313,542,912**.
Fresh interval: `[4631300224, 7000000000]`; replicated: `[4631300224, 5063542912]`.
Local cursor: 5,064,728,704; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 8860.810604188184, 'elapsed_seconds': 22610.93189907202, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482928, 'mean_ready_depth': 0.5802255940195568, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 1692510, 'prepare_wall_seconds': 22600.201966806722, 'producer_wait_capacity_seconds': 1.073312487336807, 'producer_wait_full_seconds': 3301.0965172908036, 'ready': 0, 'ready_depth_seconds': {'0': 16826.554444679583, '1': 1981.600467766868, '2': 270.4900327027426, '3': 3532.286953100818}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 211563, 'flush_seconds': 1172.3606775507214, 'pending_bytes': 110501, 'pending_chunks': 6}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **116 GiB**;
free-space reserve: 8 GiB.
Observed rate: **19,162 patches/s**; new independent GMP audits: 13,223.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
