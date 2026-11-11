# Cabbage combined search

Updated: 2026-11-11T17:15:23.261413+00:00

State: **running**. Run **cabbage-extended-r3-cap100-20261111**; gpu with 16 preparation workers.
Verified replicated cursor: **9,246,619,136**.
New replicated logical patches: **6,619,136** in 25,856 chunks.
Combined verified selected patches, including parents: **6,619,136**.
Fresh interval: `[9240000000, 9304000000]`; replicated: `[9240000000, 9246619136]`.
Local cursor: 9,246,678,784; physical tasks group up to 2 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 8; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 215.22111908299848, 'elapsed_seconds': 636.7509158739704, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 3842689, 'mean_ready_depth': 0.25796467440957577, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 4, 'preparation_batches': 6466, 'prepare_wall_seconds': 636.0482413643622, 'producer_wait_capacity_seconds': 0.004624992434401065, 'producer_wait_full_seconds': 132.95567795197712, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 472.49167021457106, '1': 164.25924269342795}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 3235, 'flush_seconds': 31.856155945453793, 'pending_bytes': 35286, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **10,390 patches/s**; new independent GMP audits: 203.
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
