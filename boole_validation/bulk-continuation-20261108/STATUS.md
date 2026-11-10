# Boole combined search

Updated: 2026-11-10T02:16:28.399949+00:00

State: **running**. Run **boole-overnight-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **3,658,893,056**.
New replicated logical patches: **188,489,984** in 736,289 chunks.
Combined verified selected patches, including parents: **658,893,056**.
Fresh interval: `[3470403072, 3750000000]`; replicated: `[3470403072, 3658893056]`.
Local cursor: 3,659,459,072; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 1267.1512644530158, 'elapsed_seconds': 10470.817662874993, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482160, 'mean_ready_depth': 0.9771524727790388, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 737728, 'prepare_wall_seconds': 10468.230512266338, 'producer_wait_capacity_seconds': 0.463691642973572, 'producer_wait_full_seconds': 1974.93668366567, 'ready': 0, 'ready_depth_seconds': {'0': 5806.353759301943, '1': 1625.6176064016763, '2': 510.571124669048, '3': 2528.2751718523214}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 92369, 'flush_seconds': 538.7700112957391, 'pending_bytes': 72893, 'pending_chunks': 4}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **18,034 patches/s**; new independent GMP audits: 5,764.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
