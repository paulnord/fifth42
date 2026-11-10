# Ada combined search

Updated: 2026-11-10T02:20:33.677148+00:00

State: **running**. Run **ada-suballocation-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **4,754,983,040**.
New replicated logical patches: **123,682,816** in 483,136 chunks.
Combined verified selected patches, including parents: **1,004,983,040**.
Fresh interval: `[4631300224, 7000000000]`; replicated: `[4631300224, 4754983040]`.
Local cursor: 4,755,345,536; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 2536.935298689292, 'elapsed_seconds': 6350.838872437016, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482301, 'mean_ready_depth': 0.5455660391415357, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 483887, 'prepare_wall_seconds': 6347.765460228897, 'producer_wait_capacity_seconds': 0.30663365457439795, 'producer_wait_full_seconds': 848.3162537888275, 'ready': 0, 'ready_depth_seconds': {'0': 4790.413924745924, '1': 570.0425582656753, '2': 76.38771545741474, '3': 913.9946732270182}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 60485, 'flush_seconds': 332.38377769087674, 'pending_bytes': 128911, 'pending_chunks': 7}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **116 GiB**;
free-space reserve: 8 GiB.
Observed rate: **19,505 patches/s**; new independent GMP audits: 3,781.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
