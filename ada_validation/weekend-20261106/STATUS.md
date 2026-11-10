# Ada combined search

Updated: 2026-11-10T03:50:58.483388+00:00

State: **running**. Run **ada-suballocation-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **4,859,574,400**.
New replicated logical patches: **228,274,176** in 891,696 chunks.
Combined verified selected patches, including parents: **1,109,574,400**.
Fresh interval: `[4631300224, 7000000000]`; replicated: `[4631300224, 4859574400]`.
Local cursor: 4,859,818,112; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 4665.043888628017, 'elapsed_seconds': 11780.702939410985, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482387, 'mean_ready_depth': 0.5575842832240295, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 892378, 'prepare_wall_seconds': 11775.03170531994, 'producer_wait_capacity_seconds': 0.5657072466565296, 'producer_wait_full_seconds': 1623.443569918687, 'ready': 0, 'ready_depth_seconds': {'0': 8843.123626365152, '1': 1051.2833313855226, '2': 141.43646961380728, '3': 1744.8595112445182}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 111547, 'flush_seconds': 616.1275455119903, 'pending_bytes': 36838, 'pending_chunks': 2}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **116 GiB**;
free-space reserve: 8 GiB.
Observed rate: **19,392 patches/s**; new independent GMP audits: 6,972.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
