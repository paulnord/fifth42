# Ada combined search

Updated: 2026-11-12T23:57:56.736969+00:00

State: **running**. Run **ada-sharing-30-7b1e3c6c84954267**; gpu with 16 preparation workers.
Verified replicated cursor: **8,972,267,264**.
New replicated logical patches: **3,393,536** in 13,256 chunks.
Combined verified selected patches, including parents: **3,393,536**.
Fresh interval: `[8968873728, 8984000000]`; replicated: `[8968873728, 8972267264]`.
Local cursor: 8,972,330,752; physical tasks group up to 2 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 105.9331654352136, 'elapsed_seconds': 310.35981555795297, 'inflight': 1, 'max_outstanding': 3, 'maximum_item_payload_bytes': 134217728, 'maximum_prepared_payload_bytes': 15357648, 'mean_ready_depth': 0.2247056204835352, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 402653184, 'preparation_batch_windows': 16, 'preparation_batches': 826, 'prepare_wall_seconds': 309.9066837866558, 'producer_wait_capacity_seconds': 0.0008962784195318818, 'producer_wait_full_seconds': 17.11074068886228, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 240.62021813483443, '1': 69.73959492810536}, 'ready_limit': 1, 'reserved_bytes': 402653184}; buffer: {'flush_count': 1648, 'flush_seconds': 12.67225256038364, 'pending_bytes': 35157, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **10,875 patches/s**; new independent GMP audits: 104.
Deadline: **2026-11-13T09:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

This run covers its assigned sealed r4 suffix under an unchanged original child claim. The predecessor journal is provenance; only this run's native interval advances here. The renewed coordinator holds the original parent lease until the new cutoff.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
