# Cabbage combined search

Updated: 2026-11-09T22:05:24.834525+00:00

State: **running**. Run **cabbage-buffered-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **2,497,111,168**.
New replicated logical patches: **129,769,472** in 506,912 chunks.
Combined verified selected patches, including parents: **247,111,168**.
Fresh interval: `[2367341696, 3000000000]`; replicated: `[2367341696, 2497111168]`.
Local cursor: 2,497,899,648; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 1796.7546344591537, 'elapsed_seconds': 5650.096412473009, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482508, 'mean_ready_depth': 0.3091173412941661, 'outstanding': 2, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 509217, 'prepare_wall_seconds': 5648.315467266017, 'producer_wait_capacity_seconds': 0.32064084289595485, 'producer_wait_full_seconds': 180.64545467251446, 'ready': 1, 'ready_depth_seconds': {'0': 4529.320842150424, '1': 756.575832765142, '2': 102.63226261502132, '3': 261.56747436139267}, 'ready_limit': 3, 'reserved_bytes': 16777216}; buffer: {'flush_count': 63694, 'flush_seconds': 361.4330265329336, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **23,059 patches/s**; new independent GMP audits: 3,979.
Deadline: **2026-11-09T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under the unchanged original reservation.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
