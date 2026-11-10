# Boole combined search

Updated: 2026-11-10T15:57:23.578495+00:00

State: **running**. Run **boole-delegated-20261109-04**; gpu with 16 preparation workers.
Verified replicated cursor: **7,266,526,976**.
New replicated logical patches: **10,526,976** in 41,121 chunks.
Combined verified selected patches, including parents: **10,526,976**.
Fresh interval: `[7256000000, 7320000000]`; replicated: `[7256000000, 7266526976]`.
Local cursor: 7,266,799,104; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 11.225662232202012, 'elapsed_seconds': 904.4727789679891, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482030, 'mean_ready_depth': 2.2264245450249476, 'outstanding': 4, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 41988, 'prepare_wall_seconds': 903.3057691299473, 'producer_wait_capacity_seconds': 0.02686519967392087, 'producer_wait_full_seconds': 415.4012317183078, 'ready': 3, 'ready_depth_seconds': {'0': 110.92064029158792, '1': 130.38563544937642, '2': 106.14474684931338, '3': 557.0217554177507}, 'ready_limit': 3, 'reserved_bytes': 33554432}; buffer: {'flush_count': 5261, 'flush_seconds': 29.337836681108456, 'pending_bytes': 18421, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **11,879 patches/s**; new independent GMP audits: 329.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
