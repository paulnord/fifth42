# Ada combined search

Updated: 2026-11-13T00:11:19.846505+00:00

State: **running**. Run **ada-sharing-30-6857e3975a144414**; gpu with 16 preparation workers.
Verified replicated cursor: **8,974,077,696**.
New replicated logical patches: **1,351,680** in 5,280 chunks.
Combined verified selected patches, including parents: **1,351,680**.
Fresh interval: `[8972726016, 8984000000]`; replicated: `[8972726016, 8974077696]`.
Local cursor: 8,974,520,064; physical tasks group up to 2 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 55.99233445688151, 'elapsed_seconds': 163.1682731959736, 'inflight': 1, 'max_outstanding': 3, 'maximum_item_payload_bytes': 134217728, 'maximum_prepared_payload_bytes': 15357160, 'mean_ready_depth': 0.2271184839888684, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 402653184, 'preparation_batch_windows': 16, 'preparation_batches': 434, 'prepare_wall_seconds': 162.72254986758344, 'producer_wait_capacity_seconds': 0.0004454797599464655, 'producer_wait_full_seconds': 9.121961768367328, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 126.10973863559775, '1': 37.058530843351036}, 'ready_limit': 1, 'reserved_bytes': 402653184}; buffer: {'flush_count': 864, 'flush_seconds': 6.856818754808046, 'pending_bytes': 35141, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **10,844 patches/s**; new independent GMP audits: 55.
Deadline: **2026-11-13T09:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

This run covers its assigned sealed r4 suffix under an unchanged original child claim. The predecessor journal is provenance; only this run's native interval advances here. The renewed coordinator holds the original parent lease until the new cutoff.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
