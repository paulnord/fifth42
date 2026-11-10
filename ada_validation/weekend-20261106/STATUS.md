# Ada combined search

Updated: 2026-11-10T12:37:33.463285+00:00

State: **running**. Run **ada-suballocation-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **5,438,105,728**.
New replicated logical patches: **806,805,504** in 3,151,584 chunks.
Combined verified selected patches, including parents: **1,688,105,728**.
Fresh interval: `[4631300224, 7000000000]`; replicated: `[4631300224, 5438105728]`.
Local cursor: 5,439,096,960; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 15813.182281242043, 'elapsed_seconds': 43376.04231428204, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482928, 'mean_ready_depth': 0.6609120412690913, 'outstanding': 4, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 3155204, 'prepare_wall_seconds': 43355.674492263934, 'producer_wait_capacity_seconds': 2.0047423659125343, 'producer_wait_full_seconds': 7075.710897745623, 'ready': 3, 'ready_depth_seconds': {'0': 30542.296321494563, '1': 4531.584383102134, '2': 770.3205405655317, '3': 7531.841067957808}, 'ready_limit': 3, 'reserved_bytes': 33554432}; buffer: {'flush_count': 394400, 'flush_seconds': 3150.3808581017074, 'pending_bytes': 18410, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **116 GiB**;
free-space reserve: 8 GiB.
Observed rate: **18,622 patches/s**; new independent GMP audits: 24,651.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
