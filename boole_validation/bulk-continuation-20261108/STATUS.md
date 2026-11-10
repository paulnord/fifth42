# Boole combined search

Updated: 2026-11-10T12:59:54.877690+00:00

State: **running**. Run **boole-delegated-20261109-02**; gpu with 16 preparation workers.
Verified replicated cursor: **7,138,836,224**.
New replicated logical patches: **10,836,224** in 42,329 chunks.
Combined verified selected patches, including parents: **10,836,224**.
Fresh interval: `[7128000000, 7192000000]`; replicated: `[7128000000, 7138836224]`.
Local cursor: 7,139,206,656; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 14.546157930919435, 'elapsed_seconds': 909.1752463500015, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 481986, 'mean_ready_depth': 2.1311696209262223, 'outstanding': 3, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 43418, 'prepare_wall_seconds': 909.0117552911397, 'producer_wait_capacity_seconds': 0.028405735443811864, 'producer_wait_full_seconds': 405.2516301267897, 'ready': 2, 'ready_depth_seconds': {'0': 136.77269299147883, '1': 140.38438267057063, '2': 98.83222715527518, '3': 533.1859427127056}, 'ready_limit': 3, 'reserved_bytes': 25165824}; buffer: {'flush_count': 5434, 'flush_seconds': 30.216833181970287, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **12,221 patches/s**; new independent GMP audits: 340.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
