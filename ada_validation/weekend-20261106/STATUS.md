# Ada combined search

Updated: 2026-11-10T01:50:32.121983+00:00

State: **running**. Run **ada-suballocation-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **4,719,786,112**.
New replicated logical patches: **88,485,888** in 345,648 chunks.
Combined verified selected patches, including parents: **969,786,112**.
Fresh interval: `[4631300224, 7000000000]`; replicated: `[4631300224, 4719786112]`.
Local cursor: 4,720,257,152; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 1828.5571288306382, 'elapsed_seconds': 4553.539500112005, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482301, 'mean_ready_depth': 0.5408518654929444, 'outstanding': 4, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 347140, 'prepare_wall_seconds': 4551.0952589683, 'producer_wait_capacity_seconds': 0.21995453134877607, 'producer_wait_full_seconds': 601.056574636721, 'ready': 3, 'ready_depth_seconds': {'0': 3442.293219073501, '1': 408.1080612615333, '2': 54.7323846280342, '3': 648.4058342379285}, 'ready_limit': 3, 'reserved_bytes': 33554432}; buffer: {'flush_count': 43392, 'flush_seconds': 237.85618074447848, 'pending_bytes': 18412, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **116 GiB**;
free-space reserve: 8 GiB.
Observed rate: **19,516 patches/s**; new independent GMP audits: 2,713.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
