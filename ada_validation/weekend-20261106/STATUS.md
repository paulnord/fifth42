# Ada combined search

Updated: 2026-11-09T20:54:35.849412+00:00

State: **running**. Run **ada-buffered-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **4,432,788,096**.
New replicated logical patches: **33,944,832** in 132,597 chunks.
Combined verified selected patches, including parents: **682,788,096**.
Fresh interval: `[4398843264, 11250000001]`; replicated: `[4398843264, 4432788096]`.
Local cursor: 4,433,355,392; physical tasks group up to 2 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 8; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 1875.606139247946, 'elapsed_seconds': 2805.1443517720327, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 963958, 'mean_ready_depth': 0.08763053725301449, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 134446, 'prepare_wall_seconds': 2804.6885554625187, 'producer_wait_capacity_seconds': 0.07885687850648537, 'producer_wait_full_seconds': 4.359921094903257, 'ready': 0, 'ready_depth_seconds': {'0': 2655.576988280227, '1': 85.46223384316545, '2': 31.961314518062863, '3': 32.143814579583704}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 16807, 'flush_seconds': 96.52525271940976, 'pending_bytes': 34755, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **12,111 patches/s**; new independent GMP audits: 1,051.
Deadline: **2026-11-09T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under the unchanged original reservation.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
