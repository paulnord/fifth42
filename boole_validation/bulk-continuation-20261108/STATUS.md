# Boole combined search

Updated: 2026-11-12T00:55:26.652804+00:00

State: **running**. Run **boole-range-r3-20261111-21-recovery1**; gpu with 16 preparation workers.
Verified replicated cursor: **8,359,956,224**.
New replicated logical patches: **15,956,224** in 62,329 chunks.
Combined verified selected patches, including parents: **15,956,224**.
Fresh interval: `[8344000000, 8408000000]`; replicated: `[8344000000, 8359956224]`.
Local cursor: 8,360,283,904; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.1516412200871855, 'elapsed_seconds': 1796.9774682379793, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7683246, 'mean_ready_depth': 0.9991524735150755, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 3954, 'prepare_wall_seconds': 1795.2149732515682, 'producer_wait_capacity_seconds': 0.0050879885675385594, 'producer_wait_full_seconds': 1097.9683440905064, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 1.522983767092228, '1': 1795.4544822408352}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 7916, 'flush_seconds': 58.754710932960734, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **9,007 patches/s**; new independent GMP audits: 495.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
