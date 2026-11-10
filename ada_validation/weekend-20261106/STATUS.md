# Ada combined search

Updated: 2026-11-10T13:37:42.574308+00:00

State: **running**. Run **ada-suballocation-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **5,502,353,536**.
New replicated logical patches: **871,053,312** in 3,402,552 chunks.
Combined verified selected patches, including parents: **1,752,353,536**.
Fresh interval: `[4631300224, 7000000000]`; replicated: `[4631300224, 5502353536]`.
Local cursor: 5,502,634,112; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 17086.02094665618, 'elapsed_seconds': 46981.57541634602, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482928, 'mean_ready_depth': 0.6682899866864427, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 3403178, 'prepare_wall_seconds': 46959.99290929327, 'producer_wait_capacity_seconds': 2.1620999790611677, 'producer_wait_full_seconds': 7798.35315998405, 'ready': 0, 'ready_depth_seconds': {'0': 32994.406016795954, '1': 4868.527708786423, '2': 827.1363694163156, '3': 8291.505320626311}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 425399, 'flush_seconds': 3385.3534991414053, 'pending_bytes': 36838, 'pending_chunks': 2}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **116 GiB**;
free-space reserve: 8 GiB.
Observed rate: **18,544 patches/s**; new independent GMP audits: 26,588.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
