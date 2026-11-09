# Ada combined search

Updated: 2026-11-09T20:09:15.920188+00:00

State: **running**. Run **ada-buffered-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **4,399,596,928**.
New replicated logical patches: **753,664** in 2,944 chunks.
Combined verified selected patches, including parents: **649,596,928**.
Fresh interval: `[4398843264, 11250000001]`; replicated: `[4398843264, 4399596928]`.
Local cursor: 4,399,990,144; physical tasks group up to 2 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 8; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 60.44397107028635, 'elapsed_seconds': 90.22413269605022, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 962825, 'mean_ready_depth': 0.08622838203811849, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 4367, 'prepare_wall_seconds': 90.2029550690786, 'producer_wait_capacity_seconds': 0.0025487717939540744, 'producer_wait_full_seconds': 0.08718683442566544, 'ready': 0, 'ready_depth_seconds': {'0': 85.44478948478354, '1': 2.7548828263534233, '2': 1.0483795718173496, '3': 0.9760796710615978}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 545, 'flush_seconds': 2.8758759889169596, 'pending_bytes': 243261, 'pending_chunks': 7}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **8,785 patches/s**; new independent GMP audits: 35.
Deadline: **2026-11-09T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under the unchanged original reservation.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
