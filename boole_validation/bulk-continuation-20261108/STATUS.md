# Boole combined search

Updated: 2026-11-10T04:30:40.865632+00:00

State: **running**. Run **boole-extra-20261109-a**; gpu with 16 preparation workers.
Verified replicated cursor: **148,578,560**.
New replicated logical patches: **48,578,560** in 189,760 chunks.
Combined verified selected patches, including parents: **48,578,560**.
Fresh interval: `[100000000, 300000000]`; replicated: `[100000000, 148578560]`.
Local cursor: 149,216,256; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 626.0707505724858, 'elapsed_seconds': 2709.9590307580074, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 546557, 'mean_ready_depth': 0.5421778203036385, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 192116, 'prepare_wall_seconds': 2709.2928466888843, 'producer_wait_capacity_seconds': 0.11724701785715297, 'producer_wait_full_seconds': 333.0634161462076, 'ready': 0, 'ready_depth_seconds': {'0': 2060.9657575534657, '1': 215.11238595092436, '2': 47.47536517021945, '3': 386.4055213723914}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 24055, 'flush_seconds': 130.96282179432455, 'pending_bytes': 17086, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **18,142 patches/s**; new independent GMP audits: 1,501.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
