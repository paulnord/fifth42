# Boole combined search

Updated: 2026-11-10T19:44:52.819563+00:00

State: **running**. Run **boole-delegated-20261109-06**; gpu with 16 preparation workers.
Verified replicated cursor: **7,425,220,352**.
New replicated logical patches: **41,220,352** in 161,017 chunks.
Combined verified selected patches, including parents: **41,220,352**.
Fresh interval: `[7384000000, 7448000000]`; replicated: `[7384000000, 7425220352]`.
Local cursor: 7,425,711,872; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 63.29660858324496, 'elapsed_seconds': 3640.376706155017, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 487141, 'mean_ready_depth': 2.111071177342054, 'outstanding': 4, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 162692, 'prepare_wall_seconds': 3638.719229482638, 'producer_wait_capacity_seconds': 0.10502480313880369, 'producer_wait_full_seconds': 1673.6074188231723, 'ready': 3, 'ready_depth_seconds': {'0': 584.1240076622926, '1': 551.8803554913029, '2': 379.90304252435453, '3': 2124.469299497083}, 'ready_limit': 3, 'reserved_bytes': 33554432}; buffer: {'flush_count': 20370, 'flush_seconds': 122.44017653306946, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **11,440 patches/s**; new independent GMP audits: 1,272.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
