# Ada combined search

Updated: 2026-11-10T01:35:28.795561+00:00

State: **running**. Run **ada-suballocation-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **4,702,244,992**.
New replicated logical patches: **70,944,768** in 277,128 chunks.
Combined verified selected patches, including parents: **952,244,992**.
Fresh interval: `[4631300224, 7000000000]`; replicated: `[4631300224, 4702244992]`.
Local cursor: 4,702,603,392; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 1471.9240148270037, 'elapsed_seconds': 3648.1828234010027, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482301, 'mean_ready_depth': 0.5377106739046941, 'outstanding': 4, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 278020, 'prepare_wall_seconds': 3646.17828924855, 'producer_wait_capacity_seconds': 0.17629412305541337, 'producer_wait_full_seconds': 478.1546847790014, 'ready': 3, 'ready_depth_seconds': {'0': 2762.4320947443484, '1': 325.8826245177188, '2': 43.820089520013425, '3': 516.0480136469123}, 'ready_limit': 3, 'reserved_bytes': 33554432}; buffer: {'flush_count': 34752, 'flush_seconds': 190.13465559633914, 'pending_bytes': 18420, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **116 GiB**;
free-space reserve: 8 GiB.
Observed rate: **19,509 patches/s**; new independent GMP audits: 2,173.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
