# Boole combined search

Updated: 2026-11-12T09:27:42.218100+00:00

State: **running**. Run **boole-range-r3-20261111-25-recovery1**; gpu with 16 preparation workers.
Verified replicated cursor: **8,621,645,568**.
New replicated logical patches: **21,645,568** in 84,553 chunks.
Combined verified selected patches, including parents: **21,645,568**.
Fresh interval: `[8600000000, 8664000000]`; replicated: `[8600000000, 8621645568]`.
Local cursor: 8,622,212,864; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.16618260485120118, 'elapsed_seconds': 2698.9611239678925, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7680672, 'mean_ready_depth': 0.9992612141984004, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 5410, 'prepare_wall_seconds': 2696.9180183227872, 'producer_wait_capacity_seconds': 0.007077751331962645, 'producer_wait_full_seconds': 1739.4345318960259, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 1.99395082751289, '1': 2696.9671698104357}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 10841, 'flush_seconds': 84.04161070671398, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **8,206 patches/s**; new independent GMP audits: 677.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
