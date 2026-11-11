# Ada combined search

Updated: 2026-11-11T16:35:49.142252+00:00

State: **running**. Run **ada-preparation-rotation-02-20261110**; gpu with 16 preparation workers.
Verified replicated cursor: **6,911,303,040**.
New replicated logical patches: **28,606,464** in 111,744 chunks.
Combined verified selected patches, including parents: **3,161,303,040**.
Fresh interval: `[6882696576, 7000000000]`; replicated: `[6882696576, 6911303040]`.
Local cursor: 6,912,376,192; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 342.81590803177096, 'elapsed_seconds': 1830.0049927110085, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7690463, 'mean_ready_depth': 0.44439551238956315, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 7242, 'prepare_wall_seconds': 1829.0738506671623, 'producer_wait_capacity_seconds': 0.007010598434135318, 'producer_wait_full_seconds': 553.429346586985, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 1016.7589825017494, '1': 813.2460064112674}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 14480, 'flush_seconds': 90.00438161037164, 'pending_bytes': 18425, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 8 GiB.
Observed rate: **16,205 patches/s**; new independent GMP audits: 906.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
