# Boole combined search

Updated: 2026-11-10T14:58:03.903134+00:00

State: **running**. Run **boole-delegated-20261109-03**; gpu with 16 preparation workers.
Verified replicated cursor: **7,224,176,384**.
New replicated logical patches: **32,176,384** in 125,689 chunks.
Combined verified selected patches, including parents: **32,176,384**.
Fresh interval: `[7192000000, 7256000000]`; replicated: `[7192000000, 7224176384]`.
Local cursor: 7,224,700,672; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 34.30359097814653, 'elapsed_seconds': 2710.517302430002, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482211, 'mean_ready_depth': 2.2142208763698052, 'outstanding': 4, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 127377, 'prepare_wall_seconds': 2710.0609851646004, 'producer_wait_capacity_seconds': 0.08099268801743165, 'producer_wait_full_seconds': 1234.9713070517173, 'ready': 3, 'ready_depth_seconds': {'0': 337.92006528313505, '1': 397.8257979552145, '2': 320.4561165081104, '3': 1654.315321943548}, 'ready_limit': 3, 'reserved_bytes': 33554432}; buffer: {'flush_count': 15955, 'flush_seconds': 89.91190852678847, 'pending_bytes': 92062, 'pending_chunks': 5}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **12,028 patches/s**; new independent GMP audits: 996.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
