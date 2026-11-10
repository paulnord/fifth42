# Cabbage combined search

Updated: 2026-11-10T01:46:41.047945+00:00

State: **running**. Run **cabbage-extended-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **2,774,978,688**.
New replicated logical patches: **202,485,760** in 790,960 chunks.
Combined verified selected patches, including parents: **524,978,688**.
Fresh interval: `[2572492928, 3000000000]`; replicated: `[2572492928, 2774978688]`.
Local cursor: 2,775,526,272; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 2740.187992416264, 'elapsed_seconds': 8835.369120179967, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482297, 'mean_ready_depth': 0.33540763767245974, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 792829, 'prepare_wall_seconds': 8832.599668275798, 'producer_wait_capacity_seconds': 0.5120716581004672, 'producer_wait_full_seconds': 346.04863665712764, 'ready': 0, 'ready_depth_seconds': {'0': 7000.872067572665, '1': 1186.158870194049, '2': 167.723130554019, '3': 480.61505108722486}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 99156, 'flush_seconds': 575.8379659737693, 'pending_bytes': 36432, 'pending_chunks': 2}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **22,966 patches/s**; new independent GMP audits: 6,194.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
