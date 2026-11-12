# Boole combined search

Updated: 2026-11-12T06:14:15.133349+00:00

State: **running**. Run **boole-range-r3-20261111-23-recovery1**; gpu with 16 preparation workers.
Verified replicated cursor: **8,525,573,888**.
New replicated logical patches: **53,573,888** in 209,273 chunks.
Combined verified selected patches, including parents: **53,573,888**.
Fresh interval: `[8472000000, 8536000000]`; replicated: `[8472000000, 8525573888]`.
Local cursor: 8,525,973,248; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.16363816906232387, 'elapsed_seconds': 6319.938778185984, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7682956, 'mean_ready_depth': 0.9993033959502836, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 13178, 'prepare_wall_seconds': 6317.972224077443, 'producer_wait_capacity_seconds': 0.017853305558674037, 'producer_wait_full_seconds': 3975.9723048056476, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 4.402492556837387, '1': 6315.53628323914}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 26404, 'flush_seconds': 204.3657494375948, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **8,539 patches/s**; new independent GMP audits: 1,648.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
