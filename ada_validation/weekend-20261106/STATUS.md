# Ada combined search

Updated: 2026-11-10T16:23:19.697179+00:00

State: **running**. Run **ada-suballocation-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **5,674,434,944**.
New replicated logical patches: **1,043,134,720** in 4,074,745 chunks.
Combined verified selected patches, including parents: **1,924,434,944**.
Fresh interval: `[4631300224, 7000000000]`; replicated: `[4631300224, 5674434944]`.
Local cursor: 5,674,895,488; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 20689.16018304514, 'elapsed_seconds': 56919.366911138, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482928, 'mean_ready_depth': 0.6849713209202334, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 4076132, 'prepare_wall_seconds': 56893.49150778097, 'producer_wait_capacity_seconds': 2.591038941522129, 'producer_wait_full_seconds': 9895.886725173099, 'ready': 0, 'ready_depth_seconds': {'0': 39850.042651856376, '1': 5638.490520945343, '2': 942.857794905547, '3': 10487.975942769728}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 509556, 'flush_seconds': 3881.7335954771843, 'pending_bytes': 73665, 'pending_chunks': 4}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **116 GiB**;
free-space reserve: 8 GiB.
Observed rate: **18,333 patches/s**; new independent GMP audits: 31,845.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
