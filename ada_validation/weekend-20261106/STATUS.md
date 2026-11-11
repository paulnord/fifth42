# Ada combined search

Updated: 2026-11-11T21:29:29.212431+00:00

State: **running**. Run **ada-allocated-r3-01-20261111**; gpu with 16 preparation workers.
Verified replicated cursor: **10,324,254,208**.
New replicated logical patches: **60,254,208** in 235,368 chunks.
Combined verified selected patches, including parents: **60,254,208**.
Fresh interval: `[10264000000, 10328000000]`; replicated: `[10264000000, 10324254208]`.
Local cursor: 10,324,310,272; physical tasks group up to 1 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 6850.136160134978, 'elapsed_seconds': 10842.268381069007, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 1924556, 'mean_ready_depth': 0.22372787075985212, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batch_windows': 1, 'preparation_batches': 235577, 'prepare_wall_seconds': 10840.508993524069, 'producer_wait_capacity_seconds': 0.16573282040189952, 'producer_wait_full_seconds': 526.5543586329441, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 0, 'ready_depth_seconds': {'0': 9776.86164333875, '1': 333.91188532242086, '2': 102.67882178950822, '3': 628.8160300673335}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 33196, 'flush_seconds': 304.7484593897243, 'pending_bytes': 279614, 'pending_chunks': 4}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **5,562 patches/s**; new independent GMP audits: 1,841.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

This run uses its assigned child claim. Historical coverage is imported only for a recorded continuation; fresh claims keep their reference parent separate. A shared coordinator holds the original parent lease.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
