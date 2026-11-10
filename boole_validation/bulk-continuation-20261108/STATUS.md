# Boole combined search

Updated: 2026-11-10T11:32:42.717021+00:00

State: **running**. Run **boole-delegated-20261109-01**; gpu with 16 preparation workers.
Verified replicated cursor: **7,074,977,280**.
New replicated logical patches: **10,977,280** in 42,880 chunks.
Combined verified selected patches, including parents: **10,977,280**.
Fresh interval: `[7064000000, 7128000000]`; replicated: `[7064000000, 7074977280]`.
Local cursor: 7,075,307,264; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 14.935994477651548, 'elapsed_seconds': 907.0348969949991, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482111, 'mean_ready_depth': 2.12391572015938, 'outstanding': 2, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 43940, 'prepare_wall_seconds': 906.8700693934225, 'producer_wait_capacity_seconds': 0.027869440615177155, 'producer_wait_full_seconds': 398.92406271072105, 'ready': 1, 'ready_depth_seconds': {'0': 136.39110756997252, '1': 141.8768430473865, '2': 101.7120028694626, '3': 527.0549425581703}, 'ready_limit': 3, 'reserved_bytes': 16777216}; buffer: {'flush_count': 5503, 'flush_seconds': 30.680822903232183, 'pending_bytes': 36830, 'pending_chunks': 2}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **12,397 patches/s**; new independent GMP audits: 344.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
