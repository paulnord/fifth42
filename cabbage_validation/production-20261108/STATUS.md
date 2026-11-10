# Cabbage combined search

Updated: 2026-11-10T17:55:00.830464+00:00

State: **stopped**. Run **cabbage-extended-rotation-20261110T172254Z**; gpu with 16 preparation workers.
Verified replicated cursor: **1,538,849,024**.
New replicated logical patches: **42,676,736** in 166,706 chunks.
Combined verified selected patches, including parents: **1,038,849,024**.
Fresh interval: `[1496172288, 2250000000]`; replicated: `[1496172288, 1538849024]`.
Local cursor: 1,538,849,024; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 754.1193417129689, 'elapsed_seconds': 1908.278098714014, 'inflight': 0, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 514669, 'mean_ready_depth': 0.18001327470130576, 'outstanding': 0, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 166707, 'prepare_wall_seconds': 1907.5444836068782, 'producer_wait_capacity_seconds': 0.10382412996841595, 'producer_wait_full_seconds': 35.846011605346575, 'ready': 0, 'ready_depth_seconds': {'0': 1670.159623418178, '1': 175.71343682345469, '2': 19.41314966639038, '3': 42.99188447801862}, 'ready_limit': 3, 'reserved_bytes': 0}; buffer: {'flush_count': 20850, 'flush_seconds': 115.48338367266115, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **22,318 patches/s**; new independent GMP audits: 1,303.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
