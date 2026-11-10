# Boole combined search

Updated: 2026-11-10T05:15:48.753926+00:00

State: **running**. Run **boole-extra-20261109-a**; gpu with 16 preparation workers.
Verified replicated cursor: **196,751,360**.
New replicated logical patches: **96,751,360** in 377,935 chunks.
Combined verified selected patches, including parents: **96,751,360**.
Fresh interval: `[100000000, 300000000]`; replicated: `[100000000, 196751360]`.
Local cursor: 198,144,768; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 1252.4145847901236, 'elapsed_seconds': 5416.607068526966, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 546826, 'mean_ready_depth': 0.5420546314282259, 'outstanding': 4, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 383198, 'prepare_wall_seconds': 5408.432223804935, 'producer_wait_capacity_seconds': 0.23334902909118682, 'producer_wait_full_seconds': 661.6771555912565, 'ready': 3, 'ready_depth_seconds': {'0': 4121.47163993615, '1': 427.2584265488549, '2': 94.79248215281405, '3': 773.0845190891414}, 'ready_limit': 3, 'reserved_bytes': 33554432}; buffer: {'flush_count': 47976, 'flush_seconds': 262.7765681023593, 'pending_bytes': 17150, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **18,108 patches/s**; new independent GMP audits: 2,994.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
