# Boole combined search

Updated: 2026-11-10T13:45:08.290340+00:00

State: **running**. Run **boole-delegated-20261109-02**; gpu with 16 preparation workers.
Verified replicated cursor: **7,171,645,184**.
New replicated logical patches: **43,645,184** in 170,489 chunks.
Combined verified selected patches, including parents: **43,645,184**.
Fresh interval: `[7128000000, 7192000000]`; replicated: `[7128000000, 7171645184]`.
Local cursor: 7,172,169,472; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 53.14062471414218, 'elapsed_seconds': 3620.8028955740156, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482367, 'mean_ready_depth': 2.1736963474305195, 'outstanding': 4, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 172047, 'prepare_wall_seconds': 3620.183769628522, 'producer_wait_capacity_seconds': 0.1130428533651866, 'producer_wait_full_seconds': 1625.3011012645438, 'ready': 3, 'ready_depth_seconds': {'0': 500.07024762325455, '1': 539.1179366462165, '2': 413.43603940471075, '3': 2168.1786711398163}, 'ready_limit': 3, 'reserved_bytes': 33554432}; buffer: {'flush_count': 21537, 'flush_seconds': 120.99533007893478, 'pending_bytes': 55251, 'pending_chunks': 3}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **12,163 patches/s**; new independent GMP audits: 1,345.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
