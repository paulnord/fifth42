# Ada combined search

Updated: 2026-11-10T07:06:36.385394+00:00

State: **running**. Run **ada-suballocation-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **5,081,213,056**.
New replicated logical patches: **449,912,832** in 1,757,472 chunks.
Combined verified selected patches, including parents: **1,331,213,056**.
Fresh interval: `[4631300224, 7000000000]`; replicated: `[4631300224, 5081213056]`.
Local cursor: 5,081,559,168; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 9208.547658072377, 'elapsed_seconds': 23514.335891654016, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482928, 'mean_ready_depth': 0.5820396857714577, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 1758230, 'prepare_wall_seconds': 23503.1865388102, 'producer_wait_capacity_seconds': 1.115108000638429, 'producer_wait_full_seconds': 3448.6679454261903, 'ready': 0, 'ready_depth_seconds': {'0': 17487.264236449613, '1': 2056.916164601629, '2': 281.10596041107783, '3': 3689.049529359676}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 219778, 'flush_seconds': 1218.142816970183, 'pending_bytes': 110497, 'pending_chunks': 6}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **116 GiB**;
free-space reserve: 8 GiB.
Observed rate: **19,142 patches/s**; new independent GMP audits: 13,737.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
