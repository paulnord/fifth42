# Boole combined search

Updated: 2026-11-11T08:40:24.843087+00:00

State: **running**. Run **boole-preparation-20261110-14-r1**; gpu with 16 preparation workers.
Verified replicated cursor: **7,904,995,072**.
New replicated logical patches: **8,995,072** in 35,137 chunks.
Combined verified selected patches, including parents: **8,995,072**.
Fresh interval: `[7896000000, 7960000000]`; replicated: `[7896000000, 7904995072]`.
Local cursor: 7,905,253,120; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.14942101371707395, 'elapsed_seconds': 911.8228944730363, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7679877, 'mean_ready_depth': 0.9988865112988362, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 2249, 'prepare_wall_seconds': 911.7698958634865, 'producer_wait_capacity_seconds': 0.002895824203733355, 'producer_wait_full_seconds': 508.5237904097885, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 1.0153025104664266, '1': 910.8075899825781}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 4506, 'flush_seconds': 31.007042165845633, 'pending_bytes': 19049, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **10,091 patches/s**; new independent GMP audits: 281.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
