# Boole combined search

Updated: 2026-11-10T12:17:47.756092+00:00

State: **running**. Run **boole-delegated-20261109-01**; gpu with 16 preparation workers.
Verified replicated cursor: **7,108,237,056**.
New replicated logical patches: **44,237,056** in 172,801 chunks.
Combined verified selected patches, including parents: **44,237,056**.
Fresh interval: `[7064000000, 7128000000]`; replicated: `[7064000000, 7108237056]`.
Local cursor: 7,108,660,992; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 59.5858866685885, 'elapsed_seconds': 3610.7867007229943, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482111, 'mean_ready_depth': 2.114313769328023, 'outstanding': 4, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 174109, 'prepare_wall_seconds': 3610.1750292831566, 'producer_wait_capacity_seconds': 0.10995512857334688, 'producer_wait_full_seconds': 1590.846346311795, 'ready': 3, 'ready_depth_seconds': {'0': 550.5417449888191, '1': 568.7413091122871, '2': 408.91620722290827, '3': 2082.587438629009}, 'ready_limit': 3, 'reserved_bytes': 33554432}; buffer: {'flush_count': 21786, 'flush_seconds': 122.44688403198961, 'pending_bytes': 18415, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **12,343 patches/s**; new independent GMP audits: 1,361.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
