# Boole combined search

Updated: 2026-11-10T01:31:19.222501+00:00

State: **running**. Run **boole-overnight-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **3,610,132,480**.
New replicated logical patches: **139,729,408** in 545,818 chunks.
Combined verified selected patches, including parents: **610,132,480**.
Fresh interval: `[3470403072, 3750000000]`; replicated: `[3470403072, 3610132480]`.
Local cursor: 3,610,995,712; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 947.6651487406343, 'elapsed_seconds': 7767.939901534992, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482160, 'mean_ready_depth': 0.9738352966892972, 'outstanding': 2, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 548932, 'prepare_wall_seconds': 7766.015005763329, 'producer_wait_capacity_seconds': 0.3447562617366202, 'producer_wait_full_seconds': 1455.4202409865102, 'ready': 1, 'ready_depth_seconds': {'0': 4314.167621743458, '1': 1209.94951106573, '2': 376.72375493729487, '3': 1867.0990125785465}, 'ready_limit': 3, 'reserved_bytes': 16777216}; buffer: {'flush_count': 68729, 'flush_seconds': 399.35786161525175, 'pending_bytes': 91101, 'pending_chunks': 5}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **18,087 patches/s**; new independent GMP audits: 4,289.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
