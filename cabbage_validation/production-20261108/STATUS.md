# Cabbage combined search

Updated: 2026-11-10T12:50:55.999774+00:00

State: **running**. Run **cabbage-extended-rotation-20261110T110534Z**; gpu with 16 preparation workers.
Verified replicated cursor: **1,145,954,816**.
New replicated logical patches: **140,119,040** in 547,340 chunks.
Combined verified selected patches, including parents: **645,954,816**.
Fresh interval: `[1005835776, 2250000000]`; replicated: `[1005835776, 1145954816]`.
Local cursor: 1,147,393,536; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 2569.697367976187, 'elapsed_seconds': 6312.470898750005, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 514645, 'mean_ready_depth': 0.14620247970958902, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 552882, 'prepare_wall_seconds': 6310.532266484282, 'producer_wait_capacity_seconds': 0.3427625115145929, 'producer_wait_full_seconds': 111.66586435830686, 'ready': 0, 'ready_depth_seconds': {'0': 5647.561965021945, '1': 526.2609288830427, '2': 19.306041980336886, '3': 119.34196188271744}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 69155, 'flush_seconds': 385.3728980359738, 'pending_bytes': 35886, 'pending_chunks': 2}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **22,399 patches/s**; new independent GMP audits: 4,320.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
