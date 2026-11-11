# Boole combined search

Updated: 2026-11-11T01:48:14.917901+00:00

State: **running**. Run **boole-preparation-20261110-10-r1**; gpu with 16 preparation workers.
Verified replicated cursor: **7,649,656,576**.
New replicated logical patches: **9,656,576** in 37,721 chunks.
Combined verified selected patches, including parents: **9,656,576**.
Fresh interval: `[7640000000, 7704000000]`; replicated: `[7640000000, 7649656576]`.
Local cursor: 7,649,828,608; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.14781151135684922, 'elapsed_seconds': 913.2696867639897, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7679636, 'mean_ready_depth': 0.9988061845375067, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 2383, 'prepare_wall_seconds': 913.1991036625113, 'producer_wait_capacity_seconds': 0.0031375099788419902, 'producer_wait_full_seconds': 484.2934244456119, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 1.0902729535009712, '1': 912.1794112905045}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 4769, 'flush_seconds': 29.32086611405248, 'pending_bytes': 38052, 'pending_chunks': 2}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **10,675 patches/s**; new independent GMP audits: 298.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
