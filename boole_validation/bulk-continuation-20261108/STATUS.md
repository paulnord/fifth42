# Boole combined search

Updated: 2026-11-10T07:20:55.312015+00:00

State: **running**. Run **boole-extra-20261109-b**; gpu with 16 preparation workers.
Verified replicated cursor: **334,037,504**.
New replicated logical patches: **34,037,504** in 132,959 chunks.
Combined verified selected patches, including parents: **34,037,504**.
Fresh interval: `[300000000, 500000000]`; replicated: `[300000000, 334037504]`.
Local cursor: 334,121,216; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 380.9276374557521, 'elapsed_seconds': 1810.919376018981, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 513842, 'mean_ready_depth': 0.5739530953299498, 'outstanding': 4, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 132970, 'prepare_wall_seconds': 1804.6847028547782, 'producer_wait_capacity_seconds': 0.08167654275894165, 'producer_wait_full_seconds': 229.58319999091327, 'ready': 3, 'ready_depth_seconds': {'0': 1348.104773809202, '1': 160.29610789142316, '2': 28.46880712750135, '3': 274.04968637088314}, 'ready_limit': 3, 'reserved_bytes': 33554432}; buffer: {'flush_count': 16652, 'flush_seconds': 86.75895519938786, 'pending_bytes': 17230, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **18,787 patches/s**; new independent GMP audits: 1,039.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
