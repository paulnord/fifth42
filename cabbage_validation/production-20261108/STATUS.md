# Cabbage combined search

Updated: 2026-11-10T03:17:03.956563+00:00

State: **running**. Run **cabbage-extended-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **2,896,434,304**.
New replicated logical patches: **323,941,376** in 1,265,396 chunks.
Combined verified selected patches, including parents: **646,434,304**.
Fresh interval: `[2572492928, 3000000000]`; replicated: `[2572492928, 2896434304]`.
Local cursor: 2,898,065,792; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 4413.083298314887, 'elapsed_seconds': 14259.336414219986, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482297, 'mean_ready_depth': 0.34051203995188956, 'outstanding': 2, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 1271594, 'prepare_wall_seconds': 14254.902863452327, 'producer_wait_capacity_seconds': 0.8222393040196039, 'producer_wait_full_seconds': 589.1262546458747, 'ready': 1, 'ready_depth_seconds': {'0': 11289.634087626007, '1': 1890.7921796673327, '2': 272.04688670800533, '3': 806.8632592276554}, 'ready_limit': 3, 'reserved_bytes': 16777216}; buffer: {'flush_count': 159034, 'flush_seconds': 927.7521336640348, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **22,826 patches/s**; new independent GMP audits: 9,935.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
