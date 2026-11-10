# Boole combined search

Updated: 2026-11-10T14:43:07.026248+00:00

State: **running**. Run **boole-delegated-20261109-03**; gpu with 16 preparation workers.
Verified replicated cursor: **7,213,428,480**.
New replicated logical patches: **21,428,480** in 83,705 chunks.
Combined verified selected patches, including parents: **21,428,480**.
Fresh interval: `[7192000000, 7256000000]`; replicated: `[7192000000, 7213428480]`.
Local cursor: 7,213,948,672; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 22.48767040646635, 'elapsed_seconds': 1814.3592602080316, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482033, 'mean_ready_depth': 2.21711356232676, 'outstanding': 4, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 85406, 'prepare_wall_seconds': 1814.045560640574, 'producer_wait_capacity_seconds': 0.05432275321800262, 'producer_wait_full_seconds': 825.1893282530946, 'ready': 3, 'ready_depth_seconds': {'0': 222.45418752654223, '1': 267.5240836146986, '2': 218.02652558474801, '3': 1106.3544626520597}, 'ready_limit': 3, 'reserved_bytes': 33554432}; buffer: {'flush_count': 10696, 'flush_seconds': 60.3784110310371, 'pending_bytes': 36829, 'pending_chunks': 2}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **12,048 patches/s**; new independent GMP audits: 668.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
