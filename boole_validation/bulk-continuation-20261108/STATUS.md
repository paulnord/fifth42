# Boole combined search

Updated: 2026-11-12T04:59:02.257217+00:00

State: **running**. Run **boole-range-r3-20261111-23-recovery1**; gpu with 16 preparation workers.
Verified replicated cursor: **8,487,149,312**.
New replicated logical patches: **15,149,312** in 59,177 chunks.
Combined verified selected patches, including parents: **15,149,312**.
Fresh interval: `[8472000000, 8536000000]`; replicated: `[8472000000, 8487149312]`.
Local cursor: 8,487,575,296; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.15097672841511667, 'elapsed_seconds': 1799.717122095055, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7681233, 'mean_ready_depth': 0.9991802998884739, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 3786, 'prepare_wall_seconds': 1797.7943650335073, 'producer_wait_capacity_seconds': 0.005160767585039139, 'producer_wait_full_seconds': 1126.8088524572086, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 1.4752258455846459, '1': 1798.2418937693583}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 7583, 'flush_seconds': 58.38309482275508, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **8,611 patches/s**; new independent GMP audits: 474.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
