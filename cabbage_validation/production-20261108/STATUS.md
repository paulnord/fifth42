# Cabbage combined search

Updated: 2026-11-09T22:35:31.417793+00:00

State: **running**. Run **cabbage-buffered-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **2,537,933,952**.
New replicated logical patches: **170,592,256** in 666,376 chunks.
Combined verified selected patches, including parents: **287,933,952**.
Fresh interval: `[2367341696, 3000000000]`; replicated: `[2367341696, 2537933952]`.
Local cursor: 2,539,293,568; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 2371.06484582345, 'elapsed_seconds': 7462.459410768992, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482508, 'mean_ready_depth': 0.3108403576637319, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 671437, 'prepare_wall_seconds': 7460.105375427578, 'producer_wait_capacity_seconds': 0.42266086413292214, 'producer_wait_full_seconds': 243.82873001077678, 'ready': 0, 'ready_depth_seconds': {'0': 5979.053104630613, '1': 997.6334098884836, '2': 135.3185434276238, '3': 350.45435185026145}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 83983, 'flush_seconds': 479.6386094322661, 'pending_bytes': 109327, 'pending_chunks': 6}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **23,024 patches/s**; new independent GMP audits: 5,246.
Deadline: **2026-11-09T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under the unchanged original reservation.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
