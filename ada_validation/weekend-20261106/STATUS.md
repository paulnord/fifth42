# Ada combined search

Updated: 2026-11-09T23:42:25.262403+00:00

State: **running**. Run **ada-overnight-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **4,571,220,608**.
New replicated logical patches: **6,264,832** in 24,472 chunks.
Combined verified selected patches, including parents: **821,220,608**.
Fresh interval: `[4564955776, 11250000001]`; replicated: `[4564955776, 4571220608]`.
Local cursor: 4,571,701,888; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 130.07833574007964, 'elapsed_seconds': 330.8790437509888, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 481878, 'mean_ready_depth': 0.5282019700223557, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 25662, 'prepare_wall_seconds': 330.71414631203515, 'producer_wait_capacity_seconds': 0.016594667453318834, 'producer_wait_full_seconds': 41.56179911229992, 'ready': 0, 'ready_depth_seconds': {'0': 250.11686398054007, '1': 31.678940624115057, '2': 4.1576932416064665, '3': 44.92554521368584}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 3207, 'flush_seconds': 17.707391927891877, 'pending_bytes': 110470, 'pending_chunks': 6}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **120 GiB**;
free-space reserve: 8 GiB.
Observed rate: **19,850 patches/s**; new independent GMP audits: 201.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under the unchanged original reservation.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
