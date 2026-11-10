# Ada combined search

Updated: 2026-11-10T04:21:05.039894+00:00

State: **running**. Run **ada-suballocation-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **4,893,739,136**.
New replicated logical patches: **262,438,912** in 1,025,152 chunks.
Combined verified selected patches, including parents: **1,143,739,136**.
Fresh interval: `[4631300224, 7000000000]`; replicated: `[4631300224, 4893739136]`.
Local cursor: 4,894,322,816; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 5368.478435397497, 'elapsed_seconds': 13586.688573224994, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482928, 'mean_ready_depth': 0.5613108356227262, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 1027109, 'prepare_wall_seconds': 13580.168902080157, 'producer_wait_capacity_seconds': 0.6511324887978844, 'producer_wait_full_seconds': 1890.796622171707, 'ready': 0, 'ready_depth_seconds': {'0': 10184.292724837898, '1': 1208.9467694326304, '2': 162.93848690739833, '3': 2030.5105910450802}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 128388, 'flush_seconds': 710.1830812777043, 'pending_bytes': 92085, 'pending_chunks': 5}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **116 GiB**;
free-space reserve: 8 GiB.
Observed rate: **19,353 patches/s**; new independent GMP audits: 8,025.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
