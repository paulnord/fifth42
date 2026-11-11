# Boole combined search

Updated: 2026-11-11T06:39:53.208985+00:00

State: **stopped**. Run **boole-preparation-20261110-12-r1**; gpu with 16 preparation workers.
Verified replicated cursor: **7,831,453,440**.
New replicated logical patches: **63,453,440** in 247,865 chunks.
Combined verified selected patches, including parents: **63,453,440**.
Fresh interval: `[7768000000, 7832000000]`; replicated: `[7768000000, 7831453440]`.
Local cursor: 7,832,000,000; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 0.17139731923816726, 'elapsed_seconds': 6196.742602253042, 'inflight': 0, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7681653, 'mean_ready_depth': 0.9988020156167469, 'outstanding': 0, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 15625, 'prepare_wall_seconds': 6195.016402908601, 'producer_wait_capacity_seconds': 0.020254204864613712, 'producer_wait_full_seconds': 3383.2107611966785, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 0, 'ready_depth_seconds': {'0': 7.423598414519802, '1': 6189.319001388503}, 'ready_limit': 1, 'reserved_bytes': 0}; buffer: {'flush_count': 31314, 'flush_seconds': 218.0115741029731, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **10,327 patches/s**; new independent GMP audits: 1,954.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
