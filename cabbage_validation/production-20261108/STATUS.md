# Cabbage combined search

Updated: 2026-11-10T13:21:00.776014+00:00

State: **running**. Run **cabbage-extended-rotation-20261110T110534Z**; gpu with 16 preparation workers.
Verified replicated cursor: **1,186,076,928**.
New replicated logical patches: **180,241,152** in 704,067 chunks.
Combined verified selected patches, including parents: **686,076,928**.
Fresh interval: `[1005835776, 2250000000]`; replicated: `[1005835776, 1186076928]`.
Local cursor: 1,187,548,416; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 3307.0750580700114, 'elapsed_seconds': 8116.026068721025, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 514645, 'mean_ready_depth': 0.14629195298071804, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 709621, 'prepare_wall_seconds': 8113.529102579516, 'producer_wait_capacity_seconds': 0.44003528280882165, 'producer_wait_full_seconds': 144.37722842145013, 'ready': 0, 'ready_depth_seconds': {'0': 7262.7137009043945, '1': 673.6603797489079, '2': 25.307037723367102, '3': 154.3449496133253}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 88759, 'flush_seconds': 494.37473023228813, 'pending_bytes': 107657, 'pending_chunks': 6}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **22,366 patches/s**; new independent GMP audits: 5,544.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
