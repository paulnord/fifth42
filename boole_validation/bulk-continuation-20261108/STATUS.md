# Boole combined search

Updated: 2026-11-10T11:05:33.050754+00:00

State: **running**. Run **boole-delegated-20261109-00**; gpu with 16 preparation workers.
Verified replicated cursor: **7,055,441,664**.
New replicated logical patches: **55,441,664** in 216,569 chunks.
Combined verified selected patches, including parents: **55,441,664**.
Fresh interval: `[7000000000, 7064000000]`; replicated: `[7000000000, 7055441664]`.
Local cursor: 7,055,703,808; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 82.45539346896112, 'elapsed_seconds': 4508.064586278051, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482240, 'mean_ready_depth': 2.0831642891814695, 'outstanding': 4, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 217116, 'prepare_wall_seconds': 4507.282937342883, 'producer_wait_capacity_seconds': 0.13944098143838346, 'producer_wait_full_seconds': 1984.3623451371677, 'ready': 3, 'ready_depth_seconds': {'0': 741.6543093657237, '1': 715.8724915619823, '2': 476.44668407487916, '3': 2574.091099915444}, 'ready_limit': 3, 'reserved_bytes': 33554432}; buffer: {'flush_count': 27205, 'flush_seconds': 154.47464064939413, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **12,328 patches/s**; new independent GMP audits: 1,697.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
