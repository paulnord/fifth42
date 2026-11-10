# Boole combined search

Updated: 2026-11-10T19:29:45.235171+00:00

State: **running**. Run **boole-delegated-20261109-06**; gpu with 16 preparation workers.
Verified replicated cursor: **7,415,095,040**.
New replicated logical patches: **31,095,040** in 121,465 chunks.
Combined verified selected patches, including parents: **31,095,040**.
Fresh interval: `[7384000000, 7448000000]`; replicated: `[7384000000, 7415095040]`.
Local cursor: 7,415,336,704; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 47.72759134974331, 'elapsed_seconds': 2727.9505901610246, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 487141, 'mean_ready_depth': 2.112022541204322, 'outstanding': 2, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 121966, 'prepare_wall_seconds': 2727.5165243071388, 'producer_wait_capacity_seconds': 0.07856807525968179, 'producer_wait_full_seconds': 1255.5248522175825, 'ready': 1, 'ready_depth_seconds': {'0': 438.99527250858955, '1': 411.3165964509826, '2': 282.73962012364063, '3': 1594.8991003378178}, 'ready_limit': 3, 'reserved_bytes': 16777216}; buffer: {'flush_count': 15271, 'flush_seconds': 91.58201579179149, 'pending_bytes': 73668, 'pending_chunks': 4}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **11,444 patches/s**; new independent GMP audits: 953.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
