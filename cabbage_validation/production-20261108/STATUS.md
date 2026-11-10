# Cabbage combined search

Updated: 2026-11-10T08:55:23.296446+00:00

State: **running**. Run **cabbage-extended-next-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **842,744,832**.
New replicated logical patches: **342,744,832** in 1,338,847 chunks.
Combined verified selected patches, including parents: **342,744,832**.
Fresh interval: `[500000000, 2250000000]`; replicated: `[500000000, 842744832]`.
Local cursor: 843,630,080; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 6227.542824282369, 'elapsed_seconds': 15351.62792478595, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 514228, 'mean_ready_depth': 0.14033751750356743, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 1341444, 'prepare_wall_seconds': 15347.006699123187, 'producer_wait_capacity_seconds': 0.8241302923415788, 'producer_wait_full_seconds': 270.475869174581, 'ready': 0, 'ready_depth_seconds': {'0': 13812.640060128528, '1': 1215.34813631, '2': 31.85796646651579, '3': 291.7817611199571}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 167794, 'flush_seconds': 904.032616206503, 'pending_bytes': 52365, 'pending_chunks': 3}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **22,357 patches/s**; new independent GMP audits: 10,481.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
