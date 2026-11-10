# Cabbage combined search

Updated: 2026-11-10T21:29:41.099099+00:00

State: **running**. Run **cabbage-extended-upgrade-20261110**; gpu with 16 preparation workers.
Verified replicated cursor: **1,788,374,272**.
New replicated logical patches: **249,525,248** in 974,708 chunks.
Combined verified selected patches, including parents: **1,288,374,272**.
Fresh interval: `[1538849024, 2250000000]`; replicated: `[1538849024, 1788374272]`.
Local cursor: 1,790,078,976; physical tasks group up to 8 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 2; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 1000.8442514065537, 'elapsed_seconds': 5876.59067039995, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 3838766, 'mean_ready_depth': 0.16079693443034987, 'outstanding': 2, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 61248, 'prepare_wall_seconds': 5876.296525382611, 'producer_wait_capacity_seconds': 0.04465912270825356, 'producer_wait_full_seconds': 167.85143207153305, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 0, 'ready_depth_seconds': {'0': 4931.652903363691, '1': 944.9377647023066}, 'ready_limit': 1, 'reserved_bytes': 25165824}; buffer: {'flush_count': 122621, 'flush_seconds': 717.7118574290071, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **42,650 patches/s**; new independent GMP audits: 7,656.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
