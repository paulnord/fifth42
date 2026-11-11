# Boole combined search

Updated: 2026-11-11T13:31:22.186872+00:00

State: **running**. Run **boole-preparation-20261110-16-r1**; gpu with 16 preparation workers.
Verified replicated cursor: **8,076,340,992**.
New replicated logical patches: **52,340,992** in 204,457 chunks.
Combined verified selected patches, including parents: **52,340,992**.
Fresh interval: `[8024000000, 8088000000]`; replicated: `[8024000000, 8076340992]`.
Local cursor: 8,076,918,528; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 0.15906262409407645, 'elapsed_seconds': 5417.471911517961, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7682388, 'mean_ready_depth': 0.999150680748261, 'outstanding': 2, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 12911, 'prepare_wall_seconds': 5417.187571679242, 'producer_wait_capacity_seconds': 0.01681763434316963, 'producer_wait_full_seconds': 3107.6272082749056, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 4.601161920232698, '1': 5412.870748327754}, 'ready_limit': 1, 'reserved_bytes': 25165824}; buffer: {'flush_count': 25862, 'flush_seconds': 186.3651626475621, 'pending_bytes': 134154, 'pending_chunks': 7}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **9,760 patches/s**; new independent GMP audits: 1,614.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
