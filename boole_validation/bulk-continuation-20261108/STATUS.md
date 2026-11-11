# Boole combined search

Updated: 2026-11-11T08:10:18.538671+00:00

State: **running**. Run **boole-preparation-20261110-13-r1**; gpu with 16 preparation workers.
Verified replicated cursor: **7,886,671,616**.
New replicated logical patches: **54,671,616** in 213,561 chunks.
Combined verified selected patches, including parents: **54,671,616**.
Fresh interval: `[7832000000, 7896000000]`; replicated: `[7832000000, 7886671616]`.
Local cursor: 7,887,177,472; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.1667626003618352, 'elapsed_seconds': 5411.705488352978, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7681636, 'mean_ready_depth': 0.9991184715284459, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 13455, 'prepare_wall_seconds': 5411.4752354198135, 'producer_wait_capacity_seconds': 0.017414419911801815, 'producer_wait_full_seconds': 3004.6199132414768, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 4.770569927641191, '1': 5406.934915885329}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 26964, 'flush_seconds': 189.24828601628542, 'pending_bytes': 19045, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **10,182 patches/s**; new independent GMP audits: 1,682.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
