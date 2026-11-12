# Boole combined search

Updated: 2026-11-12T21:54:39.322323+00:00

State: **running**. Run **boole-range-r3-20261111-30-recovery2**; gpu with 16 preparation workers.
Verified replicated cursor: **8,940,285,696**.
New replicated logical patches: **6,424,832** in 25,097 chunks.
Combined verified selected patches, including parents: **20,285,696**.
Fresh interval: `[8933860864, 8984000000]`; replicated: `[8933860864, 8940285696]`.
Local cursor: 8,940,418,816; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.19643882440868765, 'elapsed_seconds': 907.4788734780159, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7681479, 'mean_ready_depth': 0.999097869927185, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 1602, 'prepare_wall_seconds': 905.1144352604169, 'producer_wait_capacity_seconds': 0.002133030677214265, 'producer_wait_full_seconds': 624.5211190527771, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 0.8186613722937182, '1': 906.6602094958071}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 3227, 'flush_seconds': 23.0366451558657, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **7,220 patches/s**; new independent GMP audits: 201.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
