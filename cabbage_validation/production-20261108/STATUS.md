# Cabbage combined search

Updated: 2026-11-09T22:20:25.942368+00:00

State: **running**. Run **cabbage-buffered-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **2,518,072,704**.
New replicated logical patches: **150,731,008** in 588,793 chunks.
Combined verified selected patches, including parents: **268,072,704**.
Fresh interval: `[2367341696, 3000000000]`; replicated: `[2367341696, 2518072704]`.
Local cursor: 2,518,578,560; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 2082.4035028102808, 'elapsed_seconds': 6551.065908868972, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482508, 'mean_ready_depth': 0.3104679537604974, 'outstanding': 4, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 589956, 'prepare_wall_seconds': 6548.9702953117085, 'producer_wait_capacity_seconds': 0.37136412167456, 'producer_wait_full_seconds': 212.1514506553649, 'ready': 3, 'ready_depth_seconds': {'0': 5248.943572664517, '1': 876.5886285529705, '2': 119.29372106469236, '3': 306.2399856647826}, 'ready_limit': 3, 'reserved_bytes': 33554432}; buffer: {'flush_count': 73793, 'flush_seconds': 420.1429742821492, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **23,043 patches/s**; new independent GMP audits: 4,610.
Deadline: **2026-11-09T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under the unchanged original reservation.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
