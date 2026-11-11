# Boole combined search

Updated: 2026-11-11T21:15:07.697874+00:00

State: **running**. Run **boole-range-r3-20261111-19-recovery1**; gpu with 16 preparation workers.
Verified replicated cursor: **8,240,594,688**.
New replicated logical patches: **24,594,688** in 96,073 chunks.
Combined verified selected patches, including parents: **24,594,688**.
Fresh interval: `[8216000000, 8280000000]`; replicated: `[8216000000, 8240594688]`.
Local cursor: 8,241,131,264; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.1477616730844602, 'elapsed_seconds': 2716.0211988239316, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7681764, 'mean_ready_depth': 0.9992175752184281, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 6125, 'prepare_wall_seconds': 2715.9188959324383, 'producer_wait_capacity_seconds': 0.008076465514022857, 'producer_wait_full_seconds': 1628.2827882877318, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 2.1250797833199613, '1': 2713.8961165306973}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 12278, 'flush_seconds': 91.08192700333893, 'pending_bytes': 57664, 'pending_chunks': 3}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **9,233 patches/s**; new independent GMP audits: 766.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
