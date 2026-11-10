# Cabbage combined search

Updated: 2026-11-10T09:40:27.586990+00:00

State: **running**. Run **cabbage-extended-next-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **901,551,616**.
New replicated logical patches: **401,551,616** in 1,568,561 chunks.
Combined verified selected patches, including parents: **401,551,616**.
Fresh interval: `[500000000, 2250000000]`; replicated: `[500000000, 901551616]`.
Local cursor: 903,303,680; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 7331.193146097066, 'elapsed_seconds': 18056.13058857195, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 514657, 'mean_ready_depth': 0.1395285367229788, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 1574618, 'prepare_wall_seconds': 18050.70590121008, 'producer_wait_capacity_seconds': 0.9707621725974604, 'producer_wait_full_seconds': 315.927460647712, 'ready': 0, 'ready_depth_seconds': {'0': 16257.170254730969, '1': 1419.6869018567377, '2': 38.161715384048875, '3': 341.1117157592089}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 196957, 'flush_seconds': 1062.6447775745182, 'pending_bytes': 87274, 'pending_chunks': 5}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **22,314 patches/s**; new independent GMP audits: 12,302.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
