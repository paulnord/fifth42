# Boole combined search

Updated: 2026-11-10T02:31:28.772439+00:00

State: **running**. Run **boole-overnight-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **3,674,658,816**.
New replicated logical patches: **204,255,744** in 797,874 chunks.
Combined verified selected patches, including parents: **674,658,816**.
Fresh interval: `[3470403072, 3750000000]`; replicated: `[3470403072, 3674658816]`.
Local cursor: 3,675,554,560; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 1372.953071565018, 'elapsed_seconds': 11376.23579185101, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482160, 'mean_ready_depth': 0.9780580852055422, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 801009, 'prepare_wall_seconds': 11373.427696506726, 'producer_wait_capacity_seconds': 0.5035214502131566, 'producer_wait_full_seconds': 2147.7759930048487, 'ready': 0, 'ready_depth_seconds': {'0': 6304.43473222258, '1': 1766.3901723886956, '2': 556.0034365232568, '3': 2749.407449996448}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 100293, 'flush_seconds': 585.3796598699992, 'pending_bytes': 72904, 'pending_chunks': 4}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **18,023 patches/s**; new independent GMP audits: 6,258.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
