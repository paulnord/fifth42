# Boole combined search

Updated: 2026-11-11T04:14:15.783508+00:00

State: **running**. Run **boole-preparation-20261110-11-r1**; gpu with 16 preparation workers.
Verified replicated cursor: **7,741,320,960**.
New replicated logical patches: **37,320,960** in 145,785 chunks.
Combined verified selected patches, including parents: **37,320,960**.
Fresh interval: `[7704000000, 7768000000]`; replicated: `[7704000000, 7741320960]`.
Local cursor: 7,742,074,624; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.15904741658596322, 'elapsed_seconds': 3613.109363758005, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7681946, 'mean_ready_depth': 0.9989944749814845, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 9290, 'prepare_wall_seconds': 3611.7536243994255, 'producer_wait_capacity_seconds': 0.012276232242584229, 'producer_wait_full_seconds': 1940.3965206879657, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 3.6330697498633526, '1': 3609.476291898114}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 18615, 'flush_seconds': 128.95237938285572, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **10,528 patches/s**; new independent GMP audits: 1,162.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
