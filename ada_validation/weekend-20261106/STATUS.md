# Ada combined search

Updated: 2026-11-10T09:52:05.910531+00:00

State: **running**. Run **ada-suballocation-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **5,262,690,432**.
New replicated logical patches: **631,390,208** in 2,466,368 chunks.
Combined verified selected patches, including parents: **1,512,690,432**.
Fresh interval: `[4631300224, 7000000000]`; replicated: `[4631300224, 5262690432]`.
Local cursor: 5,263,577,216; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 12759.62040708086, 'elapsed_seconds': 33448.151780138025, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482928, 'mean_ready_depth': 0.6147301793631885, 'outstanding': 4, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 2469587, 'prepare_wall_seconds': 33432.498943429906, 'producer_wait_capacity_seconds': 1.5674865245819092, 'producer_wait_full_seconds': 5168.589373320399, 'ready': 3, 'ready_depth_seconds': {'0': 24373.9484937854, '1': 3099.2761214008206, '2': 462.4692697788705, '3': 5512.457894070947}, 'ready_limit': 3, 'reserved_bytes': 33554432}; buffer: {'flush_count': 308698, 'flush_seconds': 1955.5137857641676, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **116 GiB**;
free-space reserve: 8 GiB.
Observed rate: **18,901 patches/s**; new independent GMP audits: 19,294.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
