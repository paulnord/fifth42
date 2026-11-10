# Ada combined search

Updated: 2026-11-10T04:06:01.742041+00:00

State: **running**. Run **ada-suballocation-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **4,876,009,600**.
New replicated logical patches: **244,709,376** in 955,896 chunks.
Combined verified selected patches, including parents: **1,126,009,600**.
Fresh interval: `[4631300224, 7000000000]`; replicated: `[4631300224, 4876009600]`.
Local cursor: 4,877,095,040; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 5016.856757689326, 'elapsed_seconds': 12682.328396641999, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482387, 'mean_ready_depth': 0.5594803638182071, 'outstanding': 4, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 959748, 'prepare_wall_seconds': 12675.984046569443, 'producer_wait_capacity_seconds': 0.6084361008834094, 'producer_wait_full_seconds': 1756.2374243524391, 'ready': 3, 'ready_depth_seconds': {'0': 9513.150305153627, '1': 1129.8975078881485, '2': 152.22555051068775, '3': 1887.0550321685732}, 'ready_limit': 3, 'reserved_bytes': 33554432}; buffer: {'flush_count': 119968, 'flush_seconds': 663.0191098237992, 'pending_bytes': 18419, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **116 GiB**;
free-space reserve: 8 GiB.
Observed rate: **19,373 patches/s**; new independent GMP audits: 7,499.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
