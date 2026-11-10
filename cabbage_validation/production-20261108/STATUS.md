# Cabbage combined search

Updated: 2026-11-10T16:36:46.869483+00:00

State: **running**. Run **cabbage-extended-rotation-20261110T110534Z**; gpu with 16 preparation workers.
Verified replicated cursor: **1,443,536,384**.
New replicated logical patches: **437,700,608** in 1,709,768 chunks.
Combined verified selected patches, including parents: **943,536,384**.
Fresh interval: `[1005835776, 2250000000]`; replicated: `[1005835776, 1443536384]`.
Local cursor: 1,445,560,064; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 8107.06774341577, 'elapsed_seconds': 19856.422008958994, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 514722, 'mean_ready_depth': 0.1504643452584575, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 1717066, 'prepare_wall_seconds': 19850.352565882204, 'producer_wait_capacity_seconds': 1.0683780826511793, 'producer_wait_full_seconds': 364.5160071501741, 'ready': 0, 'ready_depth_seconds': {'0': 17749.59078091255, '1': 1621.8599635407445, '2': 89.09021708834916, '3': 395.8810463453992}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 214758, 'flush_seconds': 1225.5952799747465, 'pending_bytes': 17944, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **22,130 patches/s**; new independent GMP audits: 13,415.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
