# Ada combined search

Updated: 2026-11-11T20:29:18.522714+00:00

State: **running**. Run **ada-allocated-r3-01-20261111**; gpu with 16 preparation workers.
Verified replicated cursor: **10,304,361,472**.
New replicated logical patches: **40,361,472** in 157,662 chunks.
Combined verified selected patches, including parents: **40,361,472**.
Fresh interval: `[10264000000, 10328000000]`; replicated: `[10264000000, 10304361472]`.
Local cursor: 10,304,379,904; physical tasks group up to 1 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 4566.916630666819, 'elapsed_seconds': 7222.3575764829875, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 1923649, 'mean_ready_depth': 0.2208642442500665, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batch_windows': 1, 'preparation_batches': 157539, 'prepare_wall_seconds': 7221.171342618007, 'producer_wait_capacity_seconds': 0.11033143982058391, 'producer_wait_full_seconds': 344.50224030885147, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 0, 'ready_depth_seconds': {'0': 6519.420725283853, '1': 222.85368866560748, '2': 67.94262578943744, '3': 412.1405358630582}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 22167, 'flush_seconds': 200.93462350440677, 'pending_bytes': 349517, 'pending_chunks': 5}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **5,584 patches/s**; new independent GMP audits: 1,231.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

This run uses its assigned child claim. Historical coverage is imported only for a recorded continuation; fresh claims keep their reference parent separate. A shared coordinator holds the original parent lease.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
