# Cabbage combined search

Updated: 2026-11-10T06:09:51.472157+00:00

State: **running**. Run **cabbage-extended-next-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **620,680,704**.
New replicated logical patches: **120,680,704** in 471,409 chunks.
Combined verified selected patches, including parents: **120,680,704**.
Fresh interval: `[500000000, 2250000000]`; replicated: `[500000000, 620680704]`.
Local cursor: 622,378,496; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 2187.512769211142, 'elapsed_seconds': 5423.130489581963, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 513941, 'mean_ready_depth': 0.14245732287810237, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 477665, 'prepare_wall_seconds': 5421.470123228501, 'producer_wait_capacity_seconds': 0.2944762706756592, 'producer_wait_full_seconds': 96.25300804158906, 'ready': 0, 'ready_depth_seconds': {'0': 4866.571131788369, '1': 443.6133946199552, '2': 9.886630120454356, '3': 103.05933210119838}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 59749, 'flush_seconds': 319.17172117100563, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **22,512 patches/s**; new independent GMP audits: 3,732.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
