# Boole combined search

Updated: 2026-11-11T23:56:31.288678+00:00

State: **running**. Run **boole-range-r3-20261111-20-recovery1**; gpu with 16 preparation workers.
Verified replicated cursor: **8,328,967,936**.
New replicated logical patches: **48,967,936** in 191,281 chunks.
Combined verified selected patches, including parents: **48,967,936**.
Fresh interval: `[8280000000, 8344000000]`; replicated: `[8280000000, 8328967936]`.
Local cursor: 8,329,115,392; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.15690391696989536, 'elapsed_seconds': 5410.620264115976, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7682926, 'mean_ready_depth': 0.9992752047327639, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 11978, 'prepare_wall_seconds': 5408.834858539281, 'producer_wait_capacity_seconds': 0.01715882366988808, 'producer_wait_full_seconds': 3281.655935195042, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 3.921589160338044, '1': 5406.698672155733}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 24003, 'flush_seconds': 181.34692938928492, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **9,066 patches/s**; new independent GMP audits: 1,498.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
