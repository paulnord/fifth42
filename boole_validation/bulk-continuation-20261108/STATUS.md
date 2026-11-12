# Boole combined search

Updated: 2026-11-12T18:27:16.069831+00:00

State: **running**. Run **boole-range-r3-20261111-29-recovery1**; gpu with 16 preparation workers.
Verified replicated cursor: **8,876,168,960**.
New replicated logical patches: **20,168,960** in 78,785 chunks.
Combined verified selected patches, including parents: **20,168,960**.
Fresh interval: `[8856000000, 8920000000]`; replicated: `[8856000000, 8876168960]`.
Local cursor: 8,876,510,976; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.15622023842297494, 'elapsed_seconds': 2705.1856039100094, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7681486, 'mean_ready_depth': 0.9993402619168423, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 4994, 'prepare_wall_seconds': 2702.873326248373, 'producer_wait_capacity_seconds': 0.006693682516925037, 'producer_wait_full_seconds': 1827.5826961703133, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 1.7847104648826644, '1': 2703.4008899451}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 10007, 'flush_seconds': 73.38039552839473, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **7,558 patches/s**; new independent GMP audits: 625.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
