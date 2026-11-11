# Ada combined search

Updated: 2026-11-11T19:44:07.036733+00:00

State: **running**. Run **ada-allocated-r3-01-20261111**; gpu with 16 preparation workers.
Verified replicated cursor: **10,289,073,664**.
New replicated logical patches: **25,073,664** in 97,944 chunks.
Combined verified selected patches, including parents: **25,073,664**.
Fresh interval: `[10264000000, 10328000000]`; replicated: `[10264000000, 10289073664]`.
Local cursor: 10,289,340,928; physical tasks group up to 1 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 2855.7026897928445, 'elapsed_seconds': 4519.500605557987, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 1923649, 'mean_ready_depth': 0.22078291310809675, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batch_windows': 1, 'preparation_batches': 98967, 'prepare_wall_seconds': 4518.750854723505, 'producer_wait_capacity_seconds': 0.06894598132930696, 'producer_wait_full_seconds': 214.86925464845262, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 0, 'ready_depth_seconds': {'0': 4079.0706621059217, '1': 140.3506269362988, '2': 42.76006332866382, '3': 257.3192519650911}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 13904, 'flush_seconds': 126.09662185085472, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **5,606 patches/s**; new independent GMP audits: 774.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

This run uses its assigned child claim. Historical coverage is imported only for a recorded continuation; fresh claims keep their reference parent separate. A shared coordinator holds the original parent lease.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
