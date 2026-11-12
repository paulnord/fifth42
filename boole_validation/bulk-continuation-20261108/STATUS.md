# Boole combined search

Updated: 2026-11-12T14:22:07.707362+00:00

State: **running**. Run **boole-range-r3-20261111-27-recovery1**; gpu with 16 preparation workers.
Verified replicated cursor: **8,763,541,248**.
New replicated logical patches: **35,541,248** in 138,833 chunks.
Combined verified selected patches, including parents: **35,541,248**.
Fresh interval: `[8728000000, 8792000000]`; replicated: `[8728000000, 8763541248]`.
Local cursor: 8,763,950,848; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.15584877610672265, 'elapsed_seconds': 4509.873379384051, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7682331, 'mean_ready_depth': 0.9993554131867143, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 8770, 'prepare_wall_seconds': 4507.677459637518, 'producer_wait_capacity_seconds': 0.011865656357258558, 'producer_wait_full_seconds': 2966.4191932303365, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 2.9070016199257225, '1': 4506.966374474112}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 17560, 'flush_seconds': 135.66523023042828, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **7,963 patches/s**; new independent GMP audits: 1,097.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
