# Boole combined search

Updated: 2026-11-12T14:37:10.487768+00:00

State: **running**. Run **boole-range-r3-20261111-27-recovery1**; gpu with 16 preparation workers.
Verified replicated cursor: **8,771,055,360**.
New replicated logical patches: **43,055,360** in 168,185 chunks.
Combined verified selected patches, including parents: **43,055,360**.
Fresh interval: `[8728000000, 8792000000]`; replicated: `[8728000000, 8771055360]`.
Local cursor: 8,771,088,128; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.15820013277698308, 'elapsed_seconds': 5413.032721376978, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7682331, 'mean_ready_depth': 0.9993670315940043, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 10514, 'prepare_wall_seconds': 5407.9198412447, 'producer_wait_capacity_seconds': 0.014256663154810667, 'producer_wait_full_seconds': 3559.133704375592, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 3.426275773323141, '1': 5409.606442683726}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 21052, 'flush_seconds': 162.90702892036643, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **7,954 patches/s**; new independent GMP audits: 1,315.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
