# Boole combined search

Updated: 2026-11-12T22:54:48.107156+00:00

State: **running**. Run **boole-range-r3-20261111-30-recovery2**; gpu with 16 preparation workers.
Verified replicated cursor: **8,966,547,200**.
New replicated logical patches: **32,686,336** in 127,681 chunks.
Combined verified selected patches, including parents: **46,547,200**.
Fresh interval: `[8933860864, 8984000000]`; replicated: `[8933860864, 8966547200]`.
Local cursor: 8,966,659,840; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.20527219213545322, 'elapsed_seconds': 4515.107073900057, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7681479, 'mean_ready_depth': 0.9993884827334898, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 8006, 'prepare_wall_seconds': 4514.948923105025, 'producer_wait_capacity_seconds': 0.010699046892113984, 'producer_wait_full_seconds': 3107.484146338422, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 2.7610640358179808, '1': 4512.346007964225}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 16061, 'flush_seconds': 124.56571518385317, 'pending_bytes': 118947, 'pending_chunks': 6}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **7,261 patches/s**; new independent GMP audits: 1,001.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
