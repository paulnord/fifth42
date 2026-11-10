# Boole combined search

Updated: 2026-11-10T15:13:12.750433+00:00

State: **running**. Run **boole-delegated-20261109-03**; gpu with 16 preparation workers.
Verified replicated cursor: **7,234,883,328**.
New replicated logical patches: **42,883,328** in 167,513 chunks.
Combined verified selected patches, including parents: **42,883,328**.
Fresh interval: `[7192000000, 7256000000]`; replicated: `[7192000000, 7234883328]`.
Local cursor: 7,235,596,032; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 46.28359333291883, 'elapsed_seconds': 3622.8502876060084, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482211, 'mean_ready_depth': 2.212448878441548, 'outstanding': 4, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 170129, 'prepare_wall_seconds': 3622.246052685601, 'producer_wait_capacity_seconds': 0.10815063654445112, 'producer_wait_full_seconds': 1651.3497059897636, 'ready': 3, 'ready_depth_seconds': {'0': 454.96863764483714, '1': 530.9030305380584, '2': 426.46783101186156, '3': 2210.5107876712573}, 'ready_limit': 3, 'reserved_bytes': 33554432}; buffer: {'flush_count': 21312, 'flush_seconds': 119.89242036105134, 'pending_bytes': 92068, 'pending_chunks': 5}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **12,020 patches/s**; new independent GMP audits: 1,330.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
