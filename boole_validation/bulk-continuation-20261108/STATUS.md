# Boole combined search

Updated: 2026-11-12T19:42:37.126595+00:00

State: **running**. Run **boole-range-r3-20261111-29-recovery1**; gpu with 16 preparation workers.
Verified replicated cursor: **8,909,575,936**.
New replicated logical patches: **53,575,936** in 209,281 chunks.
Combined verified selected patches, including parents: **53,575,936**.
Fresh interval: `[8856000000, 8920000000]`; replicated: `[8856000000, 8909575936]`.
Local cursor: 8,910,099,968; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.16712850972544402, 'elapsed_seconds': 7221.117861335981, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7682238, 'mean_ready_depth': 0.99941114177718, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 13193, 'prepare_wall_seconds': 7220.945423544268, 'producer_wait_capacity_seconds': 0.017773882718756795, 'producer_wait_full_seconds': 4898.747096395236, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 4.2522119206842035, '1': 7216.865646705381}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 26439, 'flush_seconds': 199.21846198604908, 'pending_bytes': 79308, 'pending_chunks': 4}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **7,482 patches/s**; new independent GMP audits: 1,649.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
