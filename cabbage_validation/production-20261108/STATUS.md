# Cabbage combined search

Updated: 2026-11-10T11:20:42.247270+00:00

State: **running**. Run **cabbage-extended-rotation-20261110T110534Z**; gpu with 16 preparation workers.
Verified replicated cursor: **1,025,511,168**.
New replicated logical patches: **19,675,392** in 76,857 chunks.
Combined verified selected patches, including parents: **525,511,168**.
Fresh interval: `[1005835776, 2250000000]`; replicated: `[1005835776, 1025511168]`.
Local cursor: 1,026,154,752; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 362.76810979051515, 'elapsed_seconds': 895.0080353509984, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 514397, 'mean_ready_depth': 0.14149147391813002, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 78965, 'prepare_wall_seconds': 894.7225316145341, 'producer_wait_capacity_seconds': 0.0491185582941398, 'producer_wait_full_seconds': 14.799608837871347, 'ready': 0, 'ready_depth_seconds': {'0': 802.1202459856286, '1': 74.97998865623958, '2': 2.067382830369752, '3': 15.840417257801164}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 9877, 'flush_seconds': 54.78716938087018, 'pending_bytes': 35826, 'pending_chunks': 2}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **22,427 patches/s**; new independent GMP audits: 617.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
