# Boole combined search

Updated: 2026-11-11T21:00:01.382619+00:00

State: **running**. Run **boole-range-r3-20261111-19-recovery1**; gpu with 16 preparation workers.
Verified replicated cursor: **8,232,349,440**.
New replicated logical patches: **16,349,440** in 63,865 chunks.
Combined verified selected patches, including parents: **16,349,440**.
Fresh interval: `[8216000000, 8280000000]`; replicated: `[8216000000, 8232349440]`.
Local cursor: 8,232,742,656; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.14500590169336647, 'elapsed_seconds': 1806.5639020570088, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7681764, 'mean_ready_depth': 0.9991677344674684, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 4070, 'prepare_wall_seconds': 1806.4293680033297, 'producer_wait_capacity_seconds': 0.005341382056940347, 'producer_wait_full_seconds': 1084.7045745907817, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 1.5035390279372223, '1': 1805.060361189011}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 8159, 'flush_seconds': 59.6427249890985, 'pending_bytes': 96095, 'pending_chunks': 5}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **9,222 patches/s**; new independent GMP audits: 509.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
