# Boole combined search

Updated: 2026-11-10T08:51:10.185210+00:00

State: **running**. Run **boole-extra-20261109-b**; gpu with 16 preparation workers.
Verified replicated cursor: **434,552,064**.
New replicated logical patches: **134,552,064** in 525,594 chunks.
Combined verified selected patches, including parents: **134,552,064**.
Fresh interval: `[300000000, 500000000]`; replicated: `[300000000, 434552064]`.
Local cursor: 435,165,440; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 1514.9761714562774, 'elapsed_seconds': 7230.369443153031, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 514009, 'mean_ready_depth': 0.5795771106659765, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 527961, 'prepare_wall_seconds': 7228.543343865022, 'producer_wait_capacity_seconds': 0.323579813411925, 'producer_wait_full_seconds': 943.0094999512658, 'ready': 0, 'ready_depth_seconds': {'0': 5365.918777295155, '1': 639.7453254440334, '2': 123.30471370520536, '3': 1101.4006260185852}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 66098, 'flush_seconds': 347.0304440166801, 'pending_bytes': 51745, 'pending_chunks': 3}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **18,691 patches/s**; new independent GMP audits: 4,125.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
