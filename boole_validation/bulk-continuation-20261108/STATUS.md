# Boole combined search

Updated: 2026-11-10T16:12:26.947146+00:00

State: **running**. Run **boole-delegated-20261109-04**; gpu with 16 preparation workers.
Verified replicated cursor: **7,277,170,432**.
New replicated logical patches: **21,170,432** in 82,697 chunks.
Combined verified selected patches, including parents: **21,170,432**.
Fresh interval: `[7256000000, 7320000000]`; replicated: `[7256000000, 7277170432]`.
Local cursor: 7,277,559,552; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 23.697395440016408, 'elapsed_seconds': 1801.9988823820022, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482030, 'mean_ready_depth': 2.2084986557782162, 'outstanding': 4, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 83723, 'prepare_wall_seconds': 1801.691843826964, 'producer_wait_capacity_seconds': 0.05341087648412213, 'producer_wait_full_seconds': 828.6689782402827, 'ready': 3, 'ready_depth_seconds': {'0': 231.21068092127098, '1': 262.33857282291865, '2': 207.97534658183577, '3': 1100.47428115597}, 'ready_limit': 3, 'reserved_bytes': 33554432}; buffer: {'flush_count': 10486, 'flush_seconds': 58.305569364805706, 'pending_bytes': 128907, 'pending_chunks': 7}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **11,891 patches/s**; new independent GMP audits: 655.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
