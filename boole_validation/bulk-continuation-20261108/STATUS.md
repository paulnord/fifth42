# Boole combined search

Updated: 2026-11-10T08:36:07.983853+00:00

State: **running**. Run **boole-extra-20261109-b**; gpu with 16 preparation workers.
Verified replicated cursor: **417,560,832**.
New replicated logical patches: **117,560,832** in 459,222 chunks.
Combined verified selected patches, including parents: **117,560,832**.
Fresh interval: `[300000000, 500000000]`; replicated: `[300000000, 417560832]`.
Local cursor: 418,390,016; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 1327.7733442460303, 'elapsed_seconds': 6328.180990985013, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 513930, 'mean_ready_depth': 0.578660947679401, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 462433, 'prepare_wall_seconds': 6326.58428772178, 'producer_wait_capacity_seconds': 0.28353140130639076, 'producer_wait_full_seconds': 824.3560532649863, 'ready': 0, 'ready_depth_seconds': {'0': 4698.468671788811, '1': 559.9173894655542, '2': 107.43096713739214, '3': 962.3639618632733}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 57895, 'flush_seconds': 302.87836268893443, 'pending_bytes': 69003, 'pending_chunks': 4}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **18,704 patches/s**; new independent GMP audits: 3,613.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
