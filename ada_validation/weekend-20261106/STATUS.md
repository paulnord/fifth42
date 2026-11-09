# Ada combined search

Updated: 2026-11-09T20:56:21.228869+00:00

State: **stopped**. Run **ada-buffered-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **4,434,273,664**.
New replicated logical patches: **35,430,400** in 138,400 chunks.
Combined verified selected patches, including parents: **684,273,664**.
Fresh interval: `[4398843264, 11250000001]`; replicated: `[4398843264, 4434273664]`.
Local cursor: 4,434,273,664; physical tasks group up to 2 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 8; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 1930.3168519030442, 'elapsed_seconds': 2886.816659414035, 'inflight': 0, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 963958, 'mean_ready_depth': 0.08762557750665668, 'outstanding': 0, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 138400, 'prepare_wall_seconds': 2886.148005686875, 'producer_wait_capacity_seconds': 0.08113178826170042, 'producer_wait_full_seconds': 4.4935854451032355, 'ready': 0, 'ready_depth_seconds': {'0': 2732.8611645224155, '1': 88.03608252288541, '2': 32.835330608009826, '3': 33.08407773269573}, 'ready_limit': 3, 'reserved_bytes': 0}; buffer: {'flush_count': 17302, 'flush_seconds': 98.96283269085689, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **12,119 patches/s**; new independent GMP audits: 1,082.
Deadline: **2026-11-09T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under the unchanged original reservation.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
