# Cabbage combined search

Updated: 2026-11-10T13:36:05.988947+00:00

State: **running**. Run **cabbage-extended-rotation-20261110T110534Z**; gpu with 16 preparation workers.
Verified replicated cursor: **1,207,154,432**.
New replicated logical patches: **201,318,656** in 786,401 chunks.
Combined verified selected patches, including parents: **707,154,432**.
Fresh interval: `[1005835776, 2250000000]`; replicated: `[1005835776, 1207154432]`.
Local cursor: 1,207,549,696; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 3675.5396777870483, 'elapsed_seconds': 9016.966190425039, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 514645, 'mean_ready_depth': 0.14695657311188035, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 787384, 'prepare_wall_seconds': 9014.199296120962, 'producer_wait_capacity_seconds': 0.48827288986649364, 'producer_wait_full_seconds': 160.9666602628422, 'ready': 0, 'ready_depth_seconds': {'0': 8066.4430109360255, '1': 748.360343079723, '2': 29.74639905395452, '3': 172.41643667430617}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 98483, 'flush_seconds': 549.054156680475, 'pending_bytes': 125607, 'pending_chunks': 7}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **22,339 patches/s**; new independent GMP audits: 6,152.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
