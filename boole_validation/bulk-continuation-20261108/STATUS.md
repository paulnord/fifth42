# Boole combined search

Updated: 2026-11-12T02:10:43.875700+00:00

State: **running**. Run **boole-range-r3-20261111-21-recovery1**; gpu with 16 preparation workers.
Verified replicated cursor: **8,399,998,720**.
New replicated logical patches: **55,998,720** in 218,745 chunks.
Combined verified selected patches, including parents: **55,998,720**.
Fresh interval: `[8344000000, 8408000000]`; replicated: `[8344000000, 8399998720]`.
Local cursor: 8,400,385,792; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.16438922355882823, 'elapsed_seconds': 6322.522873304901, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7683246, 'mean_ready_depth': 0.9992755420491571, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 13762, 'prepare_wall_seconds': 6320.688199788216, 'producer_wait_capacity_seconds': 0.017657223623245955, 'producer_wait_full_seconds': 3886.9889521135483, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 4.580399155034684, '1': 6317.942471339949}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 27572, 'flush_seconds': 208.17445553583093, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **8,914 patches/s**; new independent GMP audits: 1,721.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
