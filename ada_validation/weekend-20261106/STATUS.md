# Ada combined search

Updated: 2026-11-10T03:20:46.833487+00:00

State: **running**. Run **ada-suballocation-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **4,824,309,888**.
New replicated logical patches: **193,009,664** in 753,944 chunks.
Combined verified selected patches, including parents: **1,074,309,888**.
Fresh interval: `[4631300224, 7000000000]`; replicated: `[4631300224, 4824309888]`.
Local cursor: 4,825,090,176; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 3958.4900822945638, 'elapsed_seconds': 9970.170165900025, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482387, 'mean_ready_depth': 0.5537027319944903, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 756812, 'prepare_wall_seconds': 9965.361567353364, 'producer_wait_capacity_seconds': 0.47968946519540623, 'producer_wait_full_seconds': 1359.8809599673841, 'ready': 0, 'ready_depth_seconds': {'0': 7495.067293743952, '1': 892.4810855185497, '2': 119.83598383929348, '3': 1462.7858020372223}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 94601, 'flush_seconds': 521.6974771661335, 'pending_bytes': 73674, 'pending_chunks': 4}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **116 GiB**;
free-space reserve: 8 GiB.
Observed rate: **19,432 patches/s**; new independent GMP audits: 5,913.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
