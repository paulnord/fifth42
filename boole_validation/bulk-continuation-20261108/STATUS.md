# Boole combined search

Updated: 2026-11-11T22:56:19.614490+00:00

State: **running**. Run **boole-range-r3-20261111-20-recovery1**; gpu with 16 preparation workers.
Verified replicated cursor: **8,295,890,688**.
New replicated logical patches: **15,890,688** in 62,073 chunks.
Combined verified selected patches, including parents: **15,890,688**.
Fresh interval: `[8280000000, 8344000000]`; replicated: `[8280000000, 8295890688]`.
Local cursor: 8,296,382,208; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.14589576644357294, 'elapsed_seconds': 1795.2809389249887, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7682926, 'mean_ready_depth': 0.9991677755858365, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 3978, 'prepare_wall_seconds': 1793.4653471398633, 'producer_wait_capacity_seconds': 0.005693270941264927, 'producer_wait_full_seconds': 1088.2956055677496, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 1.4940743977203965, '1': 1793.7868622973328}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 7968, 'flush_seconds': 60.253888742648996, 'pending_bytes': 96097, 'pending_chunks': 5}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **9,071 patches/s**; new independent GMP audits: 498.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
