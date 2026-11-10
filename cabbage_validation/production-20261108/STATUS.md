# Cabbage combined search

Updated: 2026-11-10T22:14:44.938511+00:00

State: **running**. Run **cabbage-extended-upgrade-20261110**; gpu with 16 preparation workers.
Verified replicated cursor: **1,900,951,296**.
New replicated logical patches: **362,102,272** in 1,414,462 chunks.
Combined verified selected patches, including parents: **1,400,951,296**.
Fresh interval: `[1538849024, 2250000000]`; replicated: `[1538849024, 1900951296]`.
Local cursor: 1,904,490,496; physical tasks group up to 8 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 2; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 1391.1286993338144, 'elapsed_seconds': 8588.312682773976, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 3838862, 'mean_ready_depth': 0.18360327162883333, 'outstanding': 2, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 89264, 'prepare_wall_seconds': 8587.959305466793, 'producer_wait_capacity_seconds': 0.06499395205173641, 'producer_wait_full_seconds': 232.94219093146967, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 0, 'ready_depth_seconds': {'0': 7011.470374652243, '1': 1576.8423063287046}, 'ready_limit': 1, 'reserved_bytes': 25165824}; buffer: {'flush_count': 178709, 'flush_seconds': 1040.0887033141335, 'pending_bytes': 19844, 'pending_chunks': 2}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **42,544 patches/s**; new independent GMP audits: 11,158.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
