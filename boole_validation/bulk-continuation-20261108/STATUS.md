# Boole combined search

Updated: 2026-11-10T16:27:34.258385+00:00

State: **running**. Run **boole-delegated-20261109-04**; gpu with 16 preparation workers.
Verified replicated cursor: **7,287,785,216**.
New replicated logical patches: **31,785,216** in 124,161 chunks.
Combined verified selected patches, including parents: **31,785,216**.
Fresh interval: `[7256000000, 7320000000]`; replicated: `[7256000000, 7287785216]`.
Local cursor: 7,288,372,992; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 34.70763118757168, 'elapsed_seconds': 2714.4330691510113, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482260, 'mean_ready_depth': 2.2202762922035406, 'outstanding': 4, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 126212, 'prepare_wall_seconds': 2712.973961534619, 'producer_wait_capacity_seconds': 0.08059398655313998, 'producer_wait_full_seconds': 1246.1497810658184, 'ready': 3, 'ready_depth_seconds': {'0': 340.91363237646874, '1': 389.4460113250534, '2': 314.8748946112464, '3': 1669.198529887246}, 'ready_limit': 3, 'reserved_bytes': 33554432}; buffer: {'flush_count': 15801, 'flush_seconds': 88.14454330696026, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **11,902 patches/s**; new independent GMP audits: 987.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
