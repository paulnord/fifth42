# Cabbage combined search

Updated: 2026-11-11T00:00:08.534418+00:00

State: **running**. Run **cabbage-extended-upgrade-20261110**; gpu with 16 preparation workers.
Verified replicated cursor: **2,160,489,728**.
New replicated logical patches: **621,640,704** in 2,428,284 chunks.
Combined verified selected patches, including parents: **1,660,489,728**.
Fresh interval: `[1538849024, 2250000000]`; replicated: `[1538849024, 2160489728]`.
Local cursor: 2,165,815,040; physical tasks group up to 8 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 2; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 2167.2993175346637, 'elapsed_seconds': 14908.50646683498, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 3841026, 'mean_ready_depth': 0.23452898118267557, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 153026, 'prepare_wall_seconds': 14907.81578183407, 'producer_wait_capacity_seconds': 0.11305033130338416, 'producer_wait_full_seconds': 458.60534026898677, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 11412.029632679827, '1': 3496.4768326221383}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 306371, 'flush_seconds': 1751.2828090739786, 'pending_bytes': 30030, 'pending_chunks': 3}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **42,026 patches/s**; new independent GMP audits: 19,129.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
