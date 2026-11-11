# Cabbage combined search

Updated: 2026-11-11T00:35:13.496379+00:00

State: **stopped**. Run **cabbage-extended-upgrade-20261110**; gpu with 16 preparation workers.
Verified replicated cursor: **2,247,943,936**.
New replicated logical patches: **709,094,912** in 2,769,902 chunks.
Combined verified selected patches, including parents: **1,747,943,936**.
Fresh interval: `[1538849024, 2250000000]`; replicated: `[1538849024, 2247943936]`.
Local cursor: 2,250,000,000; physical tasks group up to 8 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 2; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 2403.0941844097106, 'elapsed_seconds': 16983.76381372899, 'inflight': 0, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 3841026, 'mean_ready_depth': 0.24580078314708473, 'outstanding': 0, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 173621, 'prepare_wall_seconds': 16982.922510952805, 'producer_wait_capacity_seconds': 0.12885248911334202, 'producer_wait_full_seconds': 563.1007612666581, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 0, 'ready_depth_seconds': {'0': 12809.141363983275, '1': 4174.622446199704}, 'ready_limit': 1, 'reserved_bytes': 0}; buffer: {'flush_count': 347613, 'flush_seconds': 1975.2962398319505, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **41,859 patches/s**; new independent GMP audits: 21,703.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
