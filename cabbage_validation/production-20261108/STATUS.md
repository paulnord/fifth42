# Cabbage combined search

Updated: 2026-11-09T22:50:32.091246+00:00

State: **running**. Run **cabbage-buffered-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **2,557,893,760**.
New replicated logical patches: **190,552,064** in 744,344 chunks.
Combined verified selected patches, including parents: **307,893,760**.
Fresh interval: `[2367341696, 3000000000]`; replicated: `[2367341696, 2557893760]`.
Local cursor: 2,559,792,256; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 2656.3729936016607, 'elapsed_seconds': 8363.66786214296, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482508, 'mean_ready_depth': 0.3121453510713978, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 751595, 'prepare_wall_seconds': 8361.036552314763, 'producer_wait_capacity_seconds': 0.4733795259380713, 'producer_wait_full_seconds': 276.6424053556402, 'ready': 0, 'ready_depth_seconds': {'0': 6699.112437468779, '1': 1115.34959287307, '2': 152.28704470733646, '3': 396.9187862618128}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 94009, 'flush_seconds': 538.303987909283, 'pending_bytes': 54670, 'pending_chunks': 3}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **22,996 patches/s**; new independent GMP audits: 5,872.
Deadline: **2026-11-09T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under the unchanged original reservation.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
