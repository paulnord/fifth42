# Ada combined search

Updated: 2026-11-10T05:21:18.289951+00:00

State: **running**. Run **ada-suballocation-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **4,962,093,184**.
New replicated logical patches: **330,792,960** in 1,292,160 chunks.
Combined verified selected patches, including parents: **1,212,093,184**.
Fresh interval: `[4631300224, 7000000000]`; replicated: `[4631300224, 4962093184]`.
Local cursor: 4,962,961,536; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 6773.280537808081, 'elapsed_seconds': 17201.606105974002, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482928, 'mean_ready_depth': 0.5690920969151678, 'outstanding': 4, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 1295364, 'prepare_wall_seconds': 17193.10815876565, 'producer_wait_capacity_seconds': 0.8210340333171189, 'producer_wait_full_seconds': 2441.364360134059, 'ready': 3, 'ready_depth_seconds': {'0': 12855.497004827252, '1': 1521.227977112634, '2': 206.57325639144983, '3': 2618.307866420655}, 'ready_limit': 3, 'reserved_bytes': 33554432}; buffer: {'flush_count': 161920, 'flush_seconds': 896.6997298644856, 'pending_bytes': 18416, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **116 GiB**;
free-space reserve: 8 GiB.
Observed rate: **19,278 patches/s**; new independent GMP audits: 10,121.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
