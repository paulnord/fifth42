# Ada combined search

Updated: 2026-11-10T10:52:13.386618+00:00

State: **running**. Run **ada-suballocation-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **5,327,730,816**.
New replicated logical patches: **696,430,592** in 2,720,432 chunks.
Combined verified selected patches, including parents: **1,577,730,816**.
Fresh interval: `[4631300224, 7000000000]`; replicated: `[4631300224, 5327730816]`.
Local cursor: 5,327,952,000; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 13830.993980011495, 'elapsed_seconds': 37054.52707341901, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482928, 'mean_ready_depth': 0.6348205074109722, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 2720980, 'prepare_wall_seconds': 37037.27855996054, 'producer_wait_capacity_seconds': 1.7276019942364655, 'producer_wait_full_seconds': 5842.7119993415545, 'ready': 0, 'ready_depth_seconds': {'0': 26574.570398726326, '1': 3664.6857710212935, '2': 587.5248004380846, '3': 6227.746102241334}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 340122, 'flush_seconds': 2426.960731897736, 'pending_bytes': 73665, 'pending_chunks': 4}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **116 GiB**;
free-space reserve: 8 GiB.
Observed rate: **18,799 patches/s**; new independent GMP audits: 21,258.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
