# Cabbage combined search

Updated: 2026-11-10T07:55:07.383701+00:00

State: **running**. Run **cabbage-extended-next-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **762,324,224**.
New replicated logical patches: **262,324,224** in 1,024,704 chunks.
Combined verified selected patches, including parents: **262,324,224**.
Fresh interval: `[500000000, 2250000000]`; replicated: `[500000000, 762324224]`.
Local cursor: 763,459,072; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 4758.814346353756, 'elapsed_seconds': 11744.92164006998, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 514228, 'mean_ready_depth': 0.1408182205334971, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 1029125, 'prepare_wall_seconds': 11741.368695623882, 'producer_wait_capacity_seconds': 0.6325745506328531, 'producer_wait_full_seconds': 207.18254788749618, 'ready': 0, 'ready_depth_seconds': {'0': 10560.088026292739, '1': 938.4701969722519, '2': 23.661479294183664, '3': 222.70193669979926}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 128730, 'flush_seconds': 690.1933673369349, 'pending_bytes': 69804, 'pending_chunks': 4}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **22,415 patches/s**; new independent GMP audits: 8,041.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
