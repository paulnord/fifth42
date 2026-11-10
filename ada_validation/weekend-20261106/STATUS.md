# Ada combined search

Updated: 2026-11-10T04:51:11.686653+00:00

State: **running**. Run **ada-suballocation-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **4,927,930,496**.
New replicated logical patches: **296,630,272** in 1,158,712 chunks.
Combined verified selected patches, including parents: **1,177,930,496**.
Fresh interval: `[4631300224, 7000000000]`; replicated: `[4631300224, 4927930496]`.
Local cursor: 4,928,708,736; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 6070.18052385631, 'elapsed_seconds': 15388.719619812036, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482928, 'mean_ready_depth': 0.5652343987228203, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 1161101, 'prepare_wall_seconds': 15381.345896669838, 'producer_wait_capacity_seconds': 0.7359913565451279, 'producer_wait_full_seconds': 2163.11568928021, 'ready': 0, 'ready_depth_seconds': {'0': 11517.975956232869, '1': 1364.6372526804334, '2': 184.7228016750887, '3': 2321.383608462638}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 145137, 'flush_seconds': 803.1095209271298, 'pending_bytes': 92075, 'pending_chunks': 5}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **116 GiB**;
free-space reserve: 8 GiB.
Observed rate: **19,315 patches/s**; new independent GMP audits: 9,072.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
