# Ada combined search

Updated: 2026-11-10T08:06:44.510663+00:00

State: **running**. Run **ada-suballocation-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **5,147,125,888**.
New replicated logical patches: **515,825,664** in 2,014,944 chunks.
Combined verified selected patches, including parents: **1,397,125,888**.
Fresh interval: `[4631300224, 7000000000]`; replicated: `[4631300224, 5147125888]`.
Local cursor: 5,148,479,616; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 10592.188616521773, 'elapsed_seconds': 27129.554449221003, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482928, 'mean_ready_depth': 0.5893549814459772, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 2020197, 'prepare_wall_seconds': 27116.73993350251, 'producer_wait_capacity_seconds': 1.2817230629152618, 'producer_wait_full_seconds': 4052.142079386045, 'ready': 0, 'ready_depth_seconds': {'0': 20120.78401744383, '1': 2357.1196446529357, '2': 323.1339446543134, '3': 4328.516841698904}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 252524, 'flush_seconds': 1400.9159932321054, 'pending_bytes': 92096, 'pending_chunks': 5}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **116 GiB**;
free-space reserve: 8 GiB.
Observed rate: **19,063 patches/s**; new independent GMP audits: 15,783.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
