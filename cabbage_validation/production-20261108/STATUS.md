# Cabbage combined search

Updated: 2026-11-10T00:46:31.625420+00:00

State: **running**. Run **cabbage-extended-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **2,692,829,568**.
New replicated logical patches: **120,336,640** in 470,065 chunks.
Combined verified selected patches, including parents: **442,829,568**.
Fresh interval: `[2572492928, 3000000000]`; replicated: `[2572492928, 2692829568]`.
Local cursor: 2,693,224,832; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 1629.265914039337, 'elapsed_seconds': 5228.329284585954, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482186, 'mean_ready_depth': 0.32944239850817486, 'outstanding': 4, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 471556, 'prepare_wall_seconds': 5226.644730220956, 'producer_wait_capacity_seconds': 0.3045114485430531, 'producer_wait_full_seconds': 196.811872068909, 'ready': 3, 'ready_depth_seconds': {'0': 4151.9475207042415, '1': 704.4490146336029, '2': 97.81391969748074, '3': 274.11882855865406}, 'ready_limit': 3, 'reserved_bytes': 33554432}; buffer: {'flush_count': 58974, 'flush_seconds': 340.80386151222046, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **23,080 patches/s**; new independent GMP audits: 3,685.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
