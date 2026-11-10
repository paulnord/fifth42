# Boole combined search

Updated: 2026-11-10T11:17:14.626629+00:00

State: **stopped**. Run **boole-delegated-20261109-00**; gpu with 16 preparation workers.
Verified replicated cursor: **7,063,224,064**.
New replicated logical patches: **63,224,064** in 246,969 chunks.
Combined verified selected patches, including parents: **63,224,064**.
Fresh interval: `[7000000000, 7064000000]`; replicated: `[7000000000, 7063224064]`.
Local cursor: 7,064,000,000; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 95.97753678186564, 'elapsed_seconds': 5184.904621037014, 'inflight': 0, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482240, 'mean_ready_depth': 2.0807265803570925, 'outstanding': 0, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 250000, 'prepare_wall_seconds': 5183.914113582054, 'producer_wait_capacity_seconds': 0.16054392309160903, 'producer_wait_full_seconds': 2278.25829502556, 'ready': 0, 'ready_depth_seconds': {'0': 858.7099837583373, '1': 820.8265585020999, '2': 548.561926233815, '3': 2956.8061502127675}, 'ready_limit': 3, 'reserved_bytes': 0}; buffer: {'flush_count': 31329, 'flush_seconds': 177.82138487772318, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **12,343 patches/s**; new independent GMP audits: 1,954.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
