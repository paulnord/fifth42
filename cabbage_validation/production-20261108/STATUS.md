# Cabbage combined search

Updated: 2026-11-11T18:30:44.450439+00:00

State: **running**. Run **cabbage-extended-r3-cap100-20261111**; gpu with 16 preparation workers.
Verified replicated cursor: **9,292,769,024**.
New replicated logical patches: **52,769,024** in 206,129 chunks.
Combined verified selected patches, including parents: **52,769,024**.
Fresh interval: `[9240000000, 9304000000]`; replicated: `[9240000000, 9292769024]`.
Local cursor: 9,293,115,136; physical tasks group up to 2 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 8; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 1732.4096910306253, 'elapsed_seconds': 5160.807821571012, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 3844354, 'mean_ready_depth': 0.2604845520895211, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 4, 'preparation_batches': 51842, 'prepare_wall_seconds': 5159.90191795188, 'producer_wait_capacity_seconds': 0.03735728812171146, 'producer_wait_full_seconds': 1094.875475081266, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 3816.497104332957, '1': 1344.310713822022}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 25966, 'flush_seconds': 267.84245210315567, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **10,285 patches/s**; new independent GMP audits: 1,621.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.

Residual band: **0 < |a^5+b^5-c^5| <= 100**. All exact hits remain in status.json.
Below 12: []
Equal to 12: []
At most 42: []
From 43 through 100: []
