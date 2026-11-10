# Boole combined search

Updated: 2026-11-10T16:42:40.269430+00:00

State: **running**. Run **boole-delegated-20261109-04**; gpu with 16 preparation workers.
Verified replicated cursor: **7,298,401,792**.
New replicated logical patches: **42,401,792** in 165,632 chunks.
Combined verified selected patches, including parents: **42,401,792**.
Fresh interval: `[7256000000, 7320000000]`; replicated: `[7256000000, 7298401792]`.
Local cursor: 7,299,112,704; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 45.513343605503906, 'elapsed_seconds': 3615.9120278499904, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482260, 'mean_ready_depth': 2.2218805914618587, 'outstanding': 4, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 167940, 'prepare_wall_seconds': 3614.2777527309954, 'producer_wait_capacity_seconds': 0.10697815334424376, 'producer_wait_full_seconds': 1660.7664644834003, 'ready': 3, 'ready_depth_seconds': {'0': 448.9636958219926, '1': 520.8727642056765, '2': 424.9747095594066, '3': 2221.1008572629653}, 'ready_limit': 3, 'reserved_bytes': 33554432}; buffer: {'flush_count': 21022, 'flush_seconds': 117.52571428351803, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **11,889 patches/s**; new independent GMP audits: 1,313.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
