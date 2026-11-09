# Cabbage combined search

Updated: 2026-11-09T23:00:05.801274+00:00

State: **stopped**. Run **cabbage-buffered-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **2,571,248,768**.
New replicated logical patches: **203,907,072** in 796,512 chunks.
Combined verified selected patches, including parents: **321,248,768**.
Fresh interval: `[2367341696, 3000000000]`; replicated: `[2367341696, 2571248768]`.
Local cursor: 2,572,492,928; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 2834.4970663606073, 'elapsed_seconds': 8923.929208419984, 'inflight': 0, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482508, 'mean_ready_depth': 0.3127396161600001, 'outstanding': 0, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 801373, 'prepare_wall_seconds': 8920.988449169905, 'producer_wait_capacity_seconds': 0.5048860154929571, 'producer_wait_full_seconds': 298.0967823843239, 'ready': 0, 'ready_depth_seconds': {'0': 7147.673127239628, '1': 1187.805648499576, '2': 162.2907427866594, '3': 426.15968706912827}, 'ready_limit': 3, 'reserved_bytes': 0}; buffer: {'flush_count': 100235, 'flush_seconds': 574.6563394712866, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **22,981 patches/s**; new independent GMP audits: 6,261.
Deadline: **2026-11-09T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under the unchanged original reservation.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
