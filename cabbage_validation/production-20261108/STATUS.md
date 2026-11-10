# Cabbage combined search

Updated: 2026-11-10T14:36:19.005509+00:00

State: **running**. Run **cabbage-extended-rotation-20261110T110534Z**; gpu with 16 preparation workers.
Verified replicated cursor: **1,286,688,512**.
New replicated logical patches: **280,852,736** in 1,097,081 chunks.
Combined verified selected patches, including parents: **786,688,512**.
Fresh interval: `[1005835776, 2250000000]`; replicated: `[1005835776, 1286688512]`.
Local cursor: 1,287,438,592; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 5160.076335752907, 'elapsed_seconds': 12634.262553139008, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 514722, 'mean_ready_depth': 0.14747183324443983, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 1099823, 'prepare_wall_seconds': 12630.389944522758, 'producer_wait_capacity_seconds': 0.6826127344975248, 'producer_wait_full_seconds': 225.12881888385164, 'ready': 0, 'ready_depth_seconds': {'0': 11302.6203654345, '1': 1042.460908451234, '2': 46.80688283214113, '3': 242.37439542915672}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 137564, 'flush_seconds': 770.229287088383, 'pending_bytes': 71771, 'pending_chunks': 4}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **22,274 patches/s**; new independent GMP audits: 8,593.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
