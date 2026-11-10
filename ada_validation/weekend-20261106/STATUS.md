# Ada combined search

Updated: 2026-11-10T23:54:01.009111+00:00

State: **running**. Run **ada-preparation-20261110**; gpu with 16 preparation workers.
Verified replicated cursor: **6,130,129,792**.
New replicated logical patches: **242,794,496** in 948,416 chunks.
Combined verified selected patches, including parents: **2,380,129,792**.
Fresh interval: `[5887335296, 7000000000]`; replicated: `[5887335296, 6130129792]`.
Local cursor: 6,131,358,592; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 3067.7771351632546, 'elapsed_seconds': 12935.528992692998, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7682185, 'mean_ready_depth': 0.34493134533155717, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 59538, 'prepare_wall_seconds': 12933.38562219916, 'producer_wait_capacity_seconds': 0.05909259436884895, 'producer_wait_full_seconds': 2374.9401345969527, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 8473.659571983037, '1': 4461.869418024959}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 119072, 'flush_seconds': 771.6331215206883, 'pending_bytes': 18416, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **64 GiB**;
free-space reserve: 8 GiB.
Observed rate: **18,852 patches/s**; new independent GMP audits: 7,443.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
