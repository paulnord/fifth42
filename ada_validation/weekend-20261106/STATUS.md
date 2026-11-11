# Ada combined search

Updated: 2026-11-11T20:59:21.203366+00:00

State: **running**. Run **ada-allocated-r3-01-20261111**; gpu with 16 preparation workers.
Verified replicated cursor: **10,314,112,000**.
New replicated logical patches: **50,112,000** in 195,750 chunks.
Combined verified selected patches, including parents: **50,112,000**.
Fresh interval: `[10264000000, 10328000000]`; replicated: `[10264000000, 10314112000]`.
Local cursor: 10,314,326,528; physical tasks group up to 1 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 5712.280880183738, 'elapsed_seconds': 9031.804437625979, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 1924556, 'mean_ready_depth': 0.2216193810092276, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batch_windows': 1, 'preparation_batches': 196522, 'prepare_wall_seconds': 9030.335126967693, 'producer_wait_capacity_seconds': 0.13828712177928537, 'producer_wait_full_seconds': 433.39339907554677, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 0, 'ready_depth_seconds': {'0': 8150.937622119032, '1': 278.000500890892, '2': 84.97653383290162, '3': 517.889780102123}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 27680, 'flush_seconds': 250.31184003007365, 'pending_bytes': 279628, 'pending_chunks': 4}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **5,570 patches/s**; new independent GMP audits: 1,536.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

This run uses its assigned child claim. Historical coverage is imported only for a recorded continuation; fresh claims keep their reference parent separate. A shared coordinator holds the original parent lease.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
