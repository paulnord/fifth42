# Boole combined search

Updated: 2026-11-10T13:29:58.555341+00:00

State: **running**. Run **boole-delegated-20261109-02**; gpu with 16 preparation workers.
Verified replicated cursor: **7,160,735,232**.
New replicated logical patches: **32,735,232** in 127,872 chunks.
Combined verified selected patches, including parents: **32,735,232**.
Fresh interval: `[7128000000, 7192000000]`; replicated: `[7128000000, 7160735232]`.
Local cursor: 7,161,126,656; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 40.425312818435486, 'elapsed_seconds': 2713.5474676740123, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482055, 'mean_ready_depth': 2.171436611672748, 'outstanding': 3, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 129068, 'prepare_wall_seconds': 2713.088754396711, 'producer_wait_capacity_seconds': 0.08480301534291357, 'producer_wait_full_seconds': 1216.9258581809117, 'ready': 2, 'ready_depth_seconds': {'0': 378.3190418916638, '1': 401.2787425001152, '2': 310.83147076750174, '3': 1623.1182115947013}, 'ready_limit': 3, 'reserved_bytes': 25165824}; buffer: {'flush_count': 16157, 'flush_seconds': 90.89528054965194, 'pending_bytes': 18420, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **12,175 patches/s**; new independent GMP audits: 1,009.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
