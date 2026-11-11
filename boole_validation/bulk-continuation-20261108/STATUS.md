# Boole combined search

Updated: 2026-11-11T17:15:12.154656+00:00

State: **running**. Run **boole-range-r3-20261111-18**; gpu with 16 preparation workers.
Verified replicated cursor: **8,195,416,064**.
New replicated logical patches: **5,798,144** in 22,649 chunks.
Combined verified selected patches, including parents: **43,416,064**.
Fresh interval: `[8189617920, 8216000000]`; replicated: `[8189617920, 8195416064]`.
Local cursor: 8,195,973,120; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.16513944289181381, 'elapsed_seconds': 671.9424063839833, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7681615, 'mean_ready_depth': 0.9988386936398201, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 1552, 'prepare_wall_seconds': 671.7473004567437, 'producer_wait_capacity_seconds': 0.001973641978111118, 'producer_wait_full_seconds': 398.4730317504727, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 0.7803286002599634, '1': 671.162075393775}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 3108, 'flush_seconds': 21.59701157984091, 'pending_bytes': 38391, 'pending_chunks': 2}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **9,450 patches/s**; new independent GMP audits: 194.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
