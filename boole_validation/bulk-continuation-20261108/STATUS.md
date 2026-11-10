# Boole combined search

Updated: 2026-11-10T03:41:47.794187+00:00

State: **stopped**. Run **boole-overnight-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **3,748,655,872**.
New replicated logical patches: **278,252,800** in 1,086,925 chunks.
Combined verified selected patches, including parents: **748,655,872**.
Fresh interval: `[3470403072, 3750000000]`; replicated: `[3470403072, 3748655872]`.
Local cursor: 3,750,000,000; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 1859.1915447802166, 'elapsed_seconds': 15575.472821110976, 'inflight': 0, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482295, 'mean_ready_depth': 0.9821944243715061, 'outstanding': 0, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 1092176, 'prepare_wall_seconds': 15571.566268076946, 'producer_wait_capacity_seconds': 0.6870724938926287, 'producer_wait_full_seconds': 2963.349256061716, 'ready': 0, 'ready_depth_seconds': {'0': 8612.718915471574, '1': 2411.668815735262, '2': 766.7815165526699, '3': 3784.30357100151}, 'ready_limit': 3, 'reserved_bytes': 0}; buffer: {'flush_count': 136747, 'flush_seconds': 802.2706184110139, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **17,950 patches/s**; new independent GMP audits: 8,533.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
