# Boole combined search

Updated: 2026-11-11T01:33:14.015219+00:00

State: **running**. Run **boole-preparation-20261110-10-r1**; gpu with 16 preparation workers.
Verified replicated cursor: **7,640,002,048**.
New replicated logical patches: **2,048** in 8 chunks.
Combined verified selected patches, including parents: **2,048**.
Fresh interval: `[7640000000, 7704000000]`; replicated: `[7640000000, 7640002048]`.
Local cursor: 7,640,223,232; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.14457219507312402, 'elapsed_seconds': 9.989434017974418, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7676766, 'mean_ready_depth': 0.9702212642395118, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 26, 'prepare_wall_seconds': 8.765887736983132, 'producer_wait_capacity_seconds': 3.667006967589259e-05, 'producer_wait_full_seconds': 4.263421765121166, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 0.2974694260628894, '1': 9.691961301956326}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 48, 'flush_seconds': 0.2746766221243888, 'pending_bytes': 19026, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **9,539 patches/s**; new independent GMP audits: 4.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
