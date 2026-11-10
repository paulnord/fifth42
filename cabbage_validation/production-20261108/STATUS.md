# Cabbage combined search

Updated: 2026-11-10T08:25:15.870243+00:00

State: **running**. Run **cabbage-extended-next-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **802,960,896**.
New replicated logical patches: **302,960,896** in 1,183,441 chunks.
Combined verified selected patches, including parents: **302,960,896**.
Fresh interval: `[500000000, 2250000000]`; replicated: `[500000000, 802960896]`.
Local cursor: 803,598,848; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 5492.056132551283, 'elapsed_seconds': 13548.860291822988, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 514228, 'mean_ready_depth': 0.14047983496821506, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 1185515, 'prepare_wall_seconds': 13544.776477300911, 'producer_wait_capacity_seconds': 0.728645421739202, 'producer_wait_full_seconds': 237.8797557146754, 'ready': 0, 'ready_depth_seconds': {'0': 12186.6836113655, '1': 1077.4440171925235, '2': 28.300347078766208, '3': 256.4323154842132}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 148289, 'flush_seconds': 797.1989252150524, 'pending_bytes': 104706, 'pending_chunks': 6}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **22,385 patches/s**; new independent GMP audits: 9,262.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
