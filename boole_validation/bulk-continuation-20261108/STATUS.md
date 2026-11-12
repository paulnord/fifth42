# Boole combined search

Updated: 2026-11-12T07:04:47.718404+00:00

State: **running**. Run **boole-range-r3-20261111-24-recovery1**; gpu with 16 preparation workers.
Verified replicated cursor: **8,550,909,440**.
New replicated logical patches: **14,909,440** in 58,240 chunks.
Combined verified selected patches, including parents: **14,909,440**.
Fresh interval: `[8536000000, 8600000000]`; replicated: `[8536000000, 8550909440]`.
Local cursor: 8,551,314,944; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.15416403266135603, 'elapsed_seconds': 1804.3351428849855, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7680725, 'mean_ready_depth': 0.9991935655003041, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 3738, 'prepare_wall_seconds': 1802.3489360655658, 'producer_wait_capacity_seconds': 0.005043595214374363, 'producer_wait_full_seconds': 1141.551934469957, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 1.4550754282390699, '1': 1802.8800647767494}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 7481, 'flush_seconds': 54.97758425329812, 'pending_bytes': 19215, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **8,480 patches/s**; new independent GMP audits: 468.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
