# Ada combined search

Updated: 2026-11-10T12:52:36.911853+00:00

State: **running**. Run **ada-suballocation-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **5,454,493,824**.
New replicated logical patches: **823,193,600** in 3,215,600 chunks.
Combined verified selected patches, including parents: **1,704,493,824**.
Fresh interval: `[4631300224, 7000000000]`; replicated: `[4631300224, 5454493824]`.
Local cursor: 5,455,073,408; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 16136.75284377992, 'elapsed_seconds': 44278.95332203101, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482928, 'mean_ready_depth': 0.6625030261831761, 'outstanding': 2, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 3217605, 'prepare_wall_seconds': 44258.55048434448, 'producer_wait_capacity_seconds': 2.0444387195748277, 'producer_wait_full_seconds': 7253.408870018204, 'ready': 1, 'ready_depth_seconds': {'0': 31163.977352054033, '1': 4613.293870730675, '2': 783.3995939373854, '3': 7718.282504487899}, 'ready_limit': 3, 'reserved_bytes': 16777216}; buffer: {'flush_count': 402200, 'flush_seconds': 3204.5988869743887, 'pending_bytes': 73674, 'pending_chunks': 4}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **116 GiB**;
free-space reserve: 8 GiB.
Observed rate: **18,603 patches/s**; new independent GMP audits: 25,138.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
