# Ada combined search

Updated: 2026-11-09T23:00:08.335413+00:00

State: **failed**. Run **ada-group4-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **4,564,955,776**.
New replicated logical patches: **130,682,112** in 510,477 chunks.
Combined verified selected patches, including parents: **814,955,776**.
Fresh interval: `[4434273664, 11250000001]`; replicated: `[4434273664, 4564955776]`.
Local cursor: 4,564,955,776; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 2620.3525779474294, 'elapsed_seconds': 6543.546872688981, 'inflight': 0, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482483, 'mean_ready_depth': 0.503261263960026, 'outstanding': 0, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 510478, 'prepare_wall_seconds': 6541.63352662907, 'producer_wait_capacity_seconds': 0.29716148786246777, 'producer_wait_full_seconds': 778.5945396098541, 'ready': 0, 'ready_depth_seconds': {'0': 5024.237967961119, '1': 592.4832606441341, '2': 79.84651109017432, '3': 846.9791290355497}, 'ready_limit': 3, 'reserved_bytes': 0}; buffer: {'flush_count': 63810, 'flush_seconds': 354.78312388644554, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **19,861 patches/s**; new independent GMP audits: 3,989.
Deadline: **2026-11-09T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: ['TimeoutError: Worker exceeded graceful stop allowance'].

The fresh trial starts at the exact final parent cursor under the unchanged original reservation.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
