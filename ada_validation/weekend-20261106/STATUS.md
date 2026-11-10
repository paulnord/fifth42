# Ada combined search

Updated: 2026-11-10T00:33:36.611651+00:00

State: **stopped**. Run **ada-overnight-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **4,631,300,224**.
New replicated logical patches: **66,344,448** in 259,158 chunks.
Combined verified selected patches, including parents: **881,300,224**.
Fresh interval: `[4564955776, 11250000001]`; replicated: `[4564955776, 4631300224]`.
Local cursor: 4,631,300,224; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 1383.4049991670763, 'elapsed_seconds': 3395.24011923495, 'inflight': 0, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482129, 'mean_ready_depth': 0.5203752891233331, 'outstanding': 0, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 259158, 'prepare_wall_seconds': 3393.377237972163, 'producer_wait_capacity_seconds': 0.17003102274611592, 'producer_wait_full_seconds': 425.47865526983514, 'ready': 0, 'ready_depth_seconds': {'0': 2590.899249349837, '1': 302.64274818229023, '2': 40.938041526882444, '3': 460.7600758179906}, 'ready_limit': 3, 'reserved_bytes': 0}; buffer: {'flush_count': 32395, 'flush_seconds': 177.279150374874, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **120 GiB**;
free-space reserve: 8 GiB.
Observed rate: **19,540 patches/s**; new independent GMP audits: 2,025.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under the unchanged original reservation.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
