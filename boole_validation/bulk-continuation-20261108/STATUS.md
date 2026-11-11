# Boole combined search

Updated: 2026-11-11T12:00:53.180995+00:00

State: **stopped**. Run **boole-preparation-20261110-15-r1**; gpu with 16 preparation workers.
Verified replicated cursor: **8,023,699,200**.
New replicated logical patches: **63,699,200** in 248,825 chunks.
Combined verified selected patches, including parents: **63,699,200**.
Fresh interval: `[7960000000, 8024000000]`; replicated: `[7960000000, 8023699200]`.
Local cursor: 8,024,000,000; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 0.17123968340456486, 'elapsed_seconds': 6507.221618713986, 'inflight': 0, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7682014, 'mean_ready_depth': 0.9989218312640757, 'outstanding': 0, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 15625, 'prepare_wall_seconds': 6505.363241960062, 'producer_wait_capacity_seconds': 0.02004618098726496, 'producer_wait_full_seconds': 3706.6121121490723, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 0, 'ready_depth_seconds': {'0': 7.015880037040915, '1': 6500.205735806958}, 'ready_limit': 1, 'reserved_bytes': 0}; buffer: {'flush_count': 31346, 'flush_seconds': 224.58897880540462, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **9,835 patches/s**; new independent GMP audits: 1,954.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
