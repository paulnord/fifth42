# Cabbage combined search

Updated: 2026-11-10T06:55:02.878463+00:00

State: **running**. Run **cabbage-extended-next-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **681,418,240**.
New replicated logical patches: **181,418,240** in 708,665 chunks.
Combined verified selected patches, including parents: **181,418,240**.
Fresh interval: `[500000000, 2250000000]`; replicated: `[500000000, 681418240]`.
Local cursor: 683,174,656; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 3290.2160442219465, 'elapsed_seconds': 8137.833039132005, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 514059, 'mean_ready_depth': 0.1415026370467851, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 715317, 'prepare_wall_seconds': 8135.360297988402, 'producer_wait_capacity_seconds': 0.4394546222756617, 'producer_wait_full_seconds': 143.36868589778896, 'ready': 0, 'ready_depth_seconds': {'0': 7309.907302623906, '1': 658.2057699733996, '2': 15.840832170739304, '3': 153.87913352291798}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 89475, 'flush_seconds': 478.6811230746098, 'pending_bytes': 121486, 'pending_chunks': 7}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **22,478 patches/s**; new independent GMP audits: 5,589.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
